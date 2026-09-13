"""北理工重开模拟器 —— 网页版界面层（移动端适配）

本地运行：python web/main.py（需在 web/ 目录下执行，或先 cd web）
网页打包：pygbag web（在仓库根目录执行，服务端口 8000）
说明：本文件是根目录 main.py 的独立副本，额外做了三件事：
  1. 主循环改成 async —— pygbag 要求每帧 await 让出控制权给浏览器；
  2. 触屏适配 —— 手指轻触当左键点击（命中区自动放大）、上下滑滚动、左右滑翻页；
  3. 点击逻辑抽成 handle_click()，鼠标与手指共用同一套判定。
设计文档：docs/05-页面设计.md（竖屏 540 × 960，响应式等比缩放）
"""

import asyncio
import random
import time

import pygame

import game.data
import game.player
import game.timeline
import game.events
import game.endings
import game.achievements
import game.records

# 基准画幅
BASE_W = 540
BASE_H = 960

# 配色（见 docs/05-页面设计.md）
WHITE = (255, 255, 255)
BG_END = (198, 222, 208)
LINE = (227, 231, 238)
TEXT = (29, 33, 41)
TEXT_DIM = (84, 92, 106)
GREEN = (27, 152, 73)
GREEN_DARK = (14, 122, 56)
GREEN_LIGHT = (232, 244, 236)
BROWN = (161, 62, 11)
BROWN_LIGHT = (251, 240, 234)
DARK_GREEN = (0, 91, 48)

# 天赋等级配色（见 talent.md）
TIER_COLORS = {"蓝": (58, 118, 208), "紫": (128, 82, 198), "金": (198, 148, 24)}
TIER_NAMES = {"蓝": "稀有", "紫": "史诗", "金": "传说"}

FONT_PATH = "C:/Windows/Fonts/msyh.ttc"
PIXEL_FONT = "fonts/zpix.ttf"   # 开源像素字体 Zpix（OFL）
EMOJI_FONT = "C:/Windows/Fonts/seguiemj.ttf"   # 主字体缺字时的回退（如「特立✌」的 ✌）
LOG_TOP = 284
LOG_HEIGHT = 556

pygame.init()
screen = pygame.display.set_mode((BASE_W, BASE_H), pygame.RESIZABLE)
pygame.display.set_caption("北理工重开模拟器")
pygame.mixer.init()
click_sound = pygame.mixer.Sound("audio/click.wav")

# 缩放状态
scale = 1.0
offset_x = 0
offset_y = 0
font_cache = {}
bg_surface = None
bg_size = None
round_gradient_cache = {}
log_panel_cache = {}

# 游戏状态
scene = "首页"
player = None
boosts = {}
forces = []
rewind_rate = 0
rewind_used = False
talent_choices = []
chosen = []
attr_edit = {"智力": 0, "体质": 0, "颜值": 0, "家境": 0}
points_left = 20
round_no = 1
shown_time = ""
major_text = ""
ending = None
auto_on = False
auto_speed = 2
last_advance = 0
scroll = 0
log_scroll = 0
log_follow = True
detail_game = None
detail_from = "回顾"
message = ""
ending_school = ""
popup_text = ""
popup_until = 0

talents, events, endings, achievements = game.data.load_data()
records = game.records.load_records()


def update_scale():
    """按窗口大小算缩放系数与居中偏移"""
    global scale, offset_x, offset_y
    w, h = screen.get_size()
    scale = min(w / BASE_W, h / BASE_H)
    offset_x = (w - BASE_W * scale) / 2
    offset_y = (h - BASE_H * scale) / 2


def X(x):
    return int(x * scale + offset_x)


def Y(y):
    return int(y * scale + offset_y)


def S(v):
    return int(v * scale)


def to_base(pos):
    """屏幕坐标 → 基准坐标"""
    return ((pos[0] - offset_x) / scale, (pos[1] - offset_y) / scale)


def get_font(size, path=FONT_PATH):
    """按当前缩放取字体（带缓存）"""
    real = int(size * scale)
    if real < 8:
        real = 8
    key = (path, real)
    if key not in font_cache:
        font_cache[key] = pygame.font.Font(path, real)
    return font_cache[key]


def text_width(text, size, path=FONT_PATH):
    """按基准坐标返回文字宽度（含符号回退）"""
    return text_px_width(text, size, path) / scale


def mix(color_a, color_b, t):
    """两个颜色之间按比例取中间色"""
    return (int(color_a[0] + (color_b[0] - color_a[0]) * t),
            int(color_a[1] + (color_b[1] - color_a[1]) * t),
            int(color_a[2] + (color_b[2] - color_a[2]) * t))


def make_gradient(top, bottom, w, h):
    """生成竖向渐变位图（逐行画线）"""
    surf = pygame.Surface((w, h))
    for y in range(h):
        pygame.draw.line(surf, mix(top, bottom, y / h), (0, y), (w, y))
    return surf


def get_round_gradient(w, h, top, bottom, radius):
    """圆角渐变位图（带缓存，用于主按钮）"""
    key = (w, h, top, bottom, radius)
    if key not in round_gradient_cache:
        gradient = make_gradient(top, bottom, w, h).convert_alpha()
        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h), border_radius=radius)
        gradient.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        round_gradient_cache[key] = gradient
    return round_gradient_cache[key]


def draw_background():
    """画渐变背景 + 顶部装饰条（窗口尺寸变化时重建）"""
    global bg_surface, bg_size
    size = screen.get_size()
    if bg_size != size:
        bg_surface = make_gradient(WHITE, BG_END, size[0], size[1])
        bg_size = size
    screen.blit(bg_surface, (0, 0))


def has_symbol(text):
    """判断文字里是否含有主字体会渲染成方框的符号"""
    for ch in text:
        code = ord(ch)
        if 0x2600 <= code <= 0x27BF or 0x1F300 <= code <= 0x1FAFF:
            return True
    return False


def split_runs(text):
    """把文字按「是否符号」切段，返回 [[文字, 是否符号]]"""
    runs = []
    for ch in text:
        symbol = has_symbol(ch)
        if len(runs) > 0 and runs[-1][1] == symbol:
            runs[-1][0] = runs[-1][0] + ch
        else:
            runs.append([ch, symbol])
    return runs


def text_px_width(text, size, path=FONT_PATH, smooth=True):
    """按像素计算文字宽度；符号段用 emoji 字体"""
    width = 0
    for run, symbol in split_runs(text):
        if symbol:
            width = width + get_font(size, EMOJI_FONT).size(run)[0]
        else:
            width = width + get_font(size, path).size(run)[0]
    return width


def draw_text_px(text, px, py, size, color=TEXT, path=FONT_PATH, smooth=True):
    """在像素坐标处画一行字；符号段自动换 emoji 字体"""
    x = px
    for run, symbol in split_runs(text):
        if symbol:
            label = get_font(size, EMOJI_FONT).render(run, True, color)
        else:
            label = get_font(size, path).render(run, smooth, color)
        screen.blit(label, (x, py))
        x = x + label.get_width()


def draw_text(text, x, y, size, color=TEXT, path=FONT_PATH, smooth=True):
    """在基准坐标处画一行字"""
    draw_text_px(text, X(x), Y(y), size, color, path, smooth)


def draw_text_center(text, y, size, color=TEXT, path=FONT_PATH, smooth=True):
    """在基准坐标的水平居中位置画一行字"""
    px = X(BASE_W // 2) - text_px_width(text, size, path, smooth) // 2
    draw_text_px(text, px, Y(y), size, color, path, smooth)


def draw_text_right(text, x_right, y, size, color=TEXT_DIM):
    """在基准坐标 (x_right, y) 处右对齐画一行字"""
    draw_text_px(text, X(x_right) - text_px_width(text, size), Y(y), size, color)


def draw_title(text, x, y, size):
    """标题（无下划线）"""
    draw_text(text, x, y, size)


def wrap_text(text, font, max_width_base):
    """按像素宽度把长文本拆成多行"""
    lines = []
    line = ""
    for ch in text:
        if font.size(line + ch)[0] > S(max_width_base):
            lines.append(line)
            line = ch
        else:
            line = line + ch
    lines.append(line)
    return lines


def draw_card(rect, selected=False, fill=WHITE, bar=GREEN):
    """卡片：圆角 + 描边 + 左侧色条（色条颜色可指定，用于天赋等级）"""
    x, y, w, h = rect
    box = pygame.Rect(X(x), Y(y), S(w), S(h))
    pygame.draw.rect(screen, fill, box, border_radius=S(16))
    if selected:
        pygame.draw.rect(screen, GREEN, box, width=2, border_radius=S(16))
    else:
        pygame.draw.rect(screen, LINE, box, width=1, border_radius=S(16))
    pygame.draw.rect(screen, bar, (box.x, box.y + S(12), S(4), box.height - S(24)),
                     border_radius=S(2))


def draw_button(rect, text, size=19, primary=True, disabled=False):
    """画按钮；rect 用基准坐标 (x, y, w, h)"""
    x, y, w, h = rect
    box = pygame.Rect(X(x), Y(y), S(w), S(h))
    radius = S(12)
    if disabled:
        pygame.draw.rect(screen, (245, 247, 250), box, border_radius=radius)
        text_color = TEXT_DIM
    elif primary:
        screen.blit(get_round_gradient(box.width, box.height, GREEN, GREEN_DARK, radius),
                    (box.x, box.y))
        text_color = WHITE
    else:
        pygame.draw.rect(screen, WHITE, box, border_radius=radius)
        pygame.draw.rect(screen, GREEN, box, width=1, border_radius=radius)
        text_color = GREEN
    label = get_font(size).render(text, True, text_color)
    screen.blit(label, (box.x + (box.width - label.get_width()) // 2,
                        box.y + (box.height - label.get_height()) // 2))


def hit(rect, pos):
    """判断点击是否落在基准矩形内；手指轻触时把命中区向外放大 TOUCH_PAD"""
    x, y, w, h = rect
    if touch_mode:
        x = x - TOUCH_PAD
        y = y - TOUCH_PAD
        w = w + TOUCH_PAD * 2
        h = h + TOUCH_PAD * 2
    bx, by = to_base(pos)
    return x <= bx <= x + w and y <= by <= y + h


def fmt(value):
    """去掉多余小数位：5.0 → 5，8.5 → 8.5"""
    return str(round(value, 1))


def start_new_game():
    """回到开局页"""
    global scene, player, boosts, talent_choices, chosen, attr_edit, points_left
    global round_no, shown_time, major_text, ending, auto_on, auto_speed
    global scroll, log_scroll, log_follow, message, forces, rewind_rate, rewind_used
    player = game.player.new_player(game.data.SHUYUAN_LIST)
    boosts = {}
    forces = []
    rewind_rate = 0
    rewind_used = False
    talent_choices = game.player.draw_talents(talents)
    chosen = []
    attr_edit = {"智力": 0, "体质": 0, "颜值": 0, "家境": 0}
    points_left = 20
    round_no = 1
    shown_time = ""
    major_text = ""
    ending = None
    auto_on = False
    auto_speed = 2
    scroll = 0
    log_scroll = 0
    log_follow = True
    message = ""
    scene = "开局"


def write_record(ending_name):
    """把本局写入记录（只保留最近 5 局）"""
    this_game = {
        "date": time.strftime("%Y-%m-%d"),
        "gender": player["gender"],
        "shuyuan": player["shuyuan"],
        "major": player["major"],
        "ending": ending_name,
        "talents": [t["name"] for t in chosen],
        "months": player["months"],
    }
    game.records.save_record(records, this_game)
    game.records.save_records(records)


def show_round():
    """推进一个回合"""
    global round_no, shown_time, major_text, ending, scene, message, log_follow, rewind_used
    global ending_school, popup_text, popup_until
    if rewind_used is False and rewind_rate > 0 and random.randint(1, 100) <= rewind_rate:
        rewind_used = True
        round_no = 1
        player["major"] = ""
        player["seen"] = []
        player["flags"] = []
        player["rank_pcts"] = []
        player["months"].append({"time": "大一9月",
                                 "text": "【天赋·败者食尘！】时间倒流，你回到了大一 9 月。"})
    year_name, year, month = game.timeline.month_text(round_no)
    shown_time = year_name + str(month) + "月"
    stage = game.timeline.stage_of(year, month)
    major_text = ""
    if round_no == 13:
        major_text = "大二开学，你被分到「" + game.data.assign_major(player) + "」专业。"
        if player["org"] != "" and "组织部长" not in player["flags"]:
            player["flags"].append("组织部长")
            player["months"].append({"time": shown_time,
                                     "text": "你在「" + player["org"] + "」留任了部长。"})
    if round_no == 25 and "组织部长" in player["flags"] and "组织主席" not in player["flags"]:
        player["flags"].append("组织主席")
        player["months"].append({"time": shown_time,
                                 "text": "你在「" + player["org"] + "」当选了主席。"})
    pool = game.events.apply_forces(events, stage, round_no, forces)
    event = game.events.pick_event(pool, player, stage, boosts)
    applied_text = game.events.apply_event(player, event, shown_time)
    if event.get("visit") and event["visit"] not in records["provinces"]:
        records["provinces"].append(event["visit"])
    new_done = game.achievements.check_achievements(achievements, player, applied_text, "", records)
    if round_no in (5, 10, 17, 22, 29, 34):
        if round_no < 13:
            total = random.randint(280, 320)
        else:
            total = random.randint(45, 55)
        score = player["attrs"]["智力"] * 10 + player["term_bonus"]
        pct = game.endings.rank_percentile(score)
        rank = int(total * pct / 100)
        if rank < 1:
            rank = 1
        if rank > total:
            rank = total
        player["rank"] = rank
        player["term_bonus"] = 0
        player["rank_pcts"].append(pct)
        if rank == 1 and "Rank1" not in player["flags"]:
            player["flags"].append("Rank1")
        if rank > 1 and "Rank1" in player["flags"]:
            player["flags"].remove("Rank1")
        if rank <= 5 and "排名前5" not in player["flags"]:
            player["flags"].append("排名前5")
        if rank > 5 and "排名前5" in player["flags"]:
            player["flags"].remove("排名前5")
        player["months"].append({"time": shown_time,
                                 "text": "综测排名公布：你在年级排第 %d 名 / 共 %d 人。" % (rank, total)})
    for name in new_done:
        if name not in records["achievements"]:
            records["achievements"].append(name)
            message = "达成成就：" + name
            popup_text = "达成成就：" + name
            popup_until = pygame.time.get_ticks() + 3000
    log_follow = True
    round_no = round_no + 1
    if round_no > 48:
        ending = game.endings.judge_ending(endings, player)
        if "{school}" in ending["text"]:
            ending_school = game.endings.judge_school(player, ending.get("school") == "高位")
        else:
            ending_school = ""
        for name in game.achievements.check_achievements(achievements, player, "", ending["name"], records):
            if name not in records["achievements"]:
                records["achievements"].append(name)
                message = "达成成就：" + name
        write_record(ending["name"])
        scene = "结局"


def build_log():
    """把本局每月文本拼成待绘制的行（最新月份在顶端）：(文字, 颜色, 字号, 行高)"""
    lines = []
    for month in reversed(player["months"]):
        lines.append((month["time"], GREEN, 19, 32))
        for one in wrap_text(month["text"], get_font(18), 445):
            lines.append((one, TEXT, 18, 29))
        lines.append(("", TEXT, 18, 14))
    return lines


def get_log_panel(w, h):
    """日志区半透明白底（提升文字清晰度，带缓存）"""
    key = (w, h)
    if key not in log_panel_cache:
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (255, 255, 255, 180), (0, 0, w, h), border_radius=S(16))
        log_panel_cache[key] = panel
    return log_panel_cache[key]


def draw_log():
    """画月度日志（可滚动，默认跟到最新）"""
    global log_scroll
    lines = build_log()
    total = 0
    for line in lines:
        total = total + line[3]
    if log_follow:
        log_scroll = 0
    screen.blit(get_log_panel(S(480), S(LOG_HEIGHT)), (X(30), Y(LOG_TOP)))
    area = pygame.Rect(X(30), Y(LOG_TOP), S(480), S(LOG_HEIGHT))
    screen.set_clip(area)
    y = LOG_TOP - log_scroll
    for text, color, size, height in lines:
        if text != "":
            draw_text(text, 30, y, size, color)
        y = y + height
    screen.set_clip(None)


def draw_home():
    draw_text_center("BIT重开模拟器", 210, 64, TEXT, PIXEL_FONT, False)
    draw_button((120, 460, 300, 64), "开始游戏")
    draw_button((120, 540, 300, 64), "成  就", primary=False)
    draw_button((120, 620, 300, 64), "回  顾", primary=False)
    draw_button((120, 700, 300, 64), "退出游戏", primary=False)


def random_attr(names):
    """把剩余点数随机分到四项属性（每项不超过 10）"""
    global points_left
    while points_left > 0:
        name = random.choice(names)
        if attr_edit[name] < 10:
            attr_edit[name] = attr_edit[name] + 1
            points_left = points_left - 1


def clear_attr():
    """属性清零，剩余点数恢复 20"""
    global points_left
    for name in attr_edit:
        attr_edit[name] = 0
    points_left = 20


def draw_start():
    draw_title("选择天赋（5 选 2）", 30, 30, 22)
    for i in range(len(talent_choices)):
        talent = talent_choices[i]
        rect = (30, 62 + i * 74, 480, 66)
        selected = talent in chosen
        tier_color = TIER_COLORS[talent["tier"]]
        draw_card(rect, selected, GREEN_LIGHT if selected else WHITE, tier_color)
        draw_text(talent["name"], 50, 76 + i * 74, 19)
        draw_text(talent["desc"], 50, 102 + i * 74, 15, tier_color)
    draw_title("分配属性点（每项 0-10）", 30, 444, 22)
    draw_button((300, 440, 100, 36), "随机分配", size=14, primary=False)
    draw_button((410, 440, 100, 36), "清  零", size=14, primary=False)
    names = ["智力", "体质", "颜值", "家境"]
    for i in range(len(names)):
        name = names[i]
        y = 486 + i * 60
        draw_card((30, y, 480, 52))
        draw_text(name, 50, y + 14, 19)
        draw_text(str(attr_edit[name]), 180, y + 14, 19)
        draw_button((300, y + 4, 44, 44), "-", primary=False)
        draw_button((360, y + 4, 44, 44), "+", primary=False)
    draw_text("剩余点数：" + str(points_left), 50, 732, 19)
    draw_button((30, 850, 150, 64), "返回首页", size=17, primary=False)
    draw_button((195, 850, 315, 64), "开  始")


def draw_info_cards(x, y):
    """画「书院·专业」「天赋」「属性」三张信息卡片（从 y 起，纵向排列）"""
    line = "书院：" + player["shuyuan"]
    if player["major"] != "":
        line = line + "　专业：" + player["major"]
    draw_card((x, y, 480, 46), False, GREEN_LIGHT)
    draw_text(line, x + 20, y + 12, 19, GREEN)
    if len(chosen) > 0:
        draw_card((x, y + 54, 480, 46), False, BROWN_LIGHT, BROWN)
        draw_text("天赋：" + "　".join([t["name"] for t in chosen]), x + 20, y + 66, 19, BROWN)
    info = ""
    for name in ["智力", "体质", "颜值", "家境"]:
        info = info + name + " " + fmt(player["attrs"][name]) + "　"
    draw_card((x, y + 108, 480, 46), False, WHITE, DARK_GREEN)
    draw_text(info, x + 20, y + 120, 19, TEXT)


def draw_game():
    draw_text(shown_time, 30, 22, 26)
    draw_text_right(player["gender"], 510, 24, 22, GREEN)
    draw_info_cards(30, 62)
    if major_text != "":
        pygame.draw.rect(screen, GREEN, (X(30), Y(224), S(480), S(34)), border_radius=S(8))
        draw_text(major_text, 44, 231, 15, WHITE)
    pygame.draw.line(screen, LINE, (X(30), Y(270)), (X(510), Y(270)))
    draw_log()
    draw_button((30, 860, 150, 64), "继  续")
    draw_button((190, 860, 120, 64), "自动:开" if auto_on else "自动:关",
                size=15, primary=auto_on)
    draw_button((320, 860, 90, 64), str(auto_speed) + " 秒", size=15, primary=False)
    draw_button((420, 860, 90, 64), "暂  停", size=15, primary=False)


def draw_pause():
    """暂停页：下层游戏界面 + 半透明白遮罩 + 面板"""
    draw_game()
    w, h = screen.get_size()
    mask = pygame.Surface((w, h), pygame.SRCALPHA)
    mask.fill((255, 255, 255, 210))
    screen.blit(mask, (0, 0))
    draw_card((60, 330, 420, 300))
    draw_title("暂  停", 232, 362, 26)
    draw_button((120, 430, 300, 64), "继续游戏")
    draw_button((120, 520, 300, 64), "结束并返回首页", size=17, primary=False)


def draw_ending():
    draw_title("结局：" + ending["name"], 30, 30, 30)
    draw_info_cards(30, 80)
    y = 260
    for line in wrap_text(ending["text"].replace("{school}", ending_school), get_font(19), 480):
        draw_text(line, 30, y, 19)
        y = y + 34
    draw_button((30, 850, 150, 64), "回顾本局", size=15, primary=False)
    draw_button((195, 850, 150, 64), "返回首页", size=15, primary=False)
    draw_button((360, 850, 150, 64), "再来一局", size=15)


def draw_achievements():
    done = len(records["achievements"])
    draw_title("成就（已达成 " + str(done) + " / " + str(len(achievements)) + "）", 30, 30, 24)
    pygame.draw.line(screen, LINE, (X(30), Y(90)), (X(510), Y(90)))
    y = 105 - scroll
    for achievement in achievements:
        ok = achievement["name"] in records["achievements"]
        color = DARK_GREEN if ok else TEXT_DIM
        fill = GREEN_LIGHT if ok else WHITE
        draw_card((30, y, 480, 64), False, fill)
        draw_text(("✔ " if ok else "✘ ") + achievement["name"], 50, y + 10, 19, color)
        draw_text(achievement["desc"], 50, y + 36, 15, TEXT_DIM)
        y = y + 72
    draw_button((120, 860, 300, 64), "返回首页", primary=False)


def draw_review():
    draw_title("回顾（近5 局）", 30, 30, 24)
    pygame.draw.line(screen, LINE, (X(30), Y(90)), (X(510), Y(90)))
    games = records["games"]
    if len(games) == 0:
        draw_text("还没有记录，先去玩一局吧。", 30, 110, 19, TEXT_DIM)
    y = 105 - scroll
    for i in range(len(games)):
        item = games[len(games) - 1 - i]
        draw_card((30, y, 480, 80))
        draw_text("第 " + str(i + 1) + " 局（" + item.get("gender", "—") + "）", 50, y + 8, 19)
        draw_text(item["shuyuan"] + " · " + item["major"] + " · " + item["ending"],
                  50, y + 34, 15, TEXT_DIM)
        if len(item.get("talents", [])) > 0:
            draw_text("天赋：" + "　".join(item.get("talents", [])), 50, y + 56, 14, TEXT_DIM)
        y = y + 88
    draw_button((30, 860, 200, 64), "导出 txt", primary=False)
    draw_button((245, 860, 265, 64), "返回首页", primary=False)


def draw_detail():
    draw_title("本局回顾 · " + detail_game.get("gender", "—"), 30, 30, 24)
    if len(detail_game.get("talents", [])) > 0:
        draw_text_right("天赋：" + "　".join(detail_game.get("talents", [])), 510, 36, 15)
    pygame.draw.line(screen, LINE, (X(30), Y(90)), (X(510), Y(90)))
    y = 105 - scroll
    for month in detail_game["months"]:
        draw_text(month["time"], 30, y, 19, GREEN)
        y = y + 28
        for line in wrap_text(month["text"], get_font(15), 480):
            draw_text(line, 30, y, 15, TEXT_DIM)
            y = y + 26
        y = y + 12
    draw_button((120, 860, 300, 64), "返  回", primary=False)


update_scale()

# ---------- 移动端触屏适配 ----------
SWIPE_MIN = 40          # 滑动判定阈值（基准坐标像素）
TOUCH_PAD = 12          # 手指轻触时给按钮扩大的命中边距（基准坐标像素）
touch_mode = False      # 手指轻触时打开，让 hit() 自动放大命中区
finger = {"start": None, "time": 0}


def touch_pos(event):
    """手指坐标是 0~1 的归一化值，换算成屏幕像素坐标"""
    w, h = screen.get_size()
    return (int(event.x * w), int(event.y * h))


def handle_finger_up(end_pos):
    """手指抬起：位移小算轻触（当左键点击），位移大算滑动"""
    global touch_mode
    start = finger["start"]
    finger["start"] = None
    if start is None:
        return
    dx = end_pos[0] - start[0]
    dy = end_pos[1] - start[1]
    if abs(dx) < SWIPE_MIN and abs(dy) < SWIPE_MIN:
        touch_mode = True
        click_sound.play()
        handle_click(end_pos)
        touch_mode = False
        return
    handle_swipe(dx, dy)


def handle_swipe(dx, dy):
    """上下滑滚动（游戏页滚月度日志，其余页滚列表）；左右滑翻页"""
    global scene, scroll, log_scroll, log_follow, last_advance
    if abs(dy) >= abs(dx):
        if scene == "游戏":
            log_scroll = log_scroll - dy
            if log_scroll < 0:
                log_scroll = 0
            log_follow = False
        else:
            scroll = scroll - dy
            if scroll < 0:
                scroll = 0
        return
    if scene == "游戏":
        if dx < 0:
            show_round()
            last_advance = pygame.time.get_ticks()
        else:
            scene = "暂停"
    elif scene == "暂停":
        scene = "游戏"
    elif scene == "回顾详情":
        scene = detail_from
    elif scene == "成就" or scene == "回顾" or scene == "结局":
        scene = "首页"


def handle_click(pos):
    """按当前界面处理一次点击（鼠标左键与手指轻触共用）"""
    global running, scene, scroll, log_scroll, points_left, boosts, forces, rewind_rate
    global message, popup_text, popup_until, detail_game, detail_from
    if scene == "首页":
        if hit((120, 460, 300, 64), pos):
            start_new_game()
        elif hit((120, 540, 300, 64), pos):
            scroll = 0
            scene = "成就"
        elif hit((120, 620, 300, 64), pos):
            scroll = 0
            scene = "回顾"
        elif hit((120, 700, 300, 64), pos):
            running = False
    elif scene == "开局":
        for i in range(len(talent_choices)):
            if hit((30, 62 + i * 74, 480, 66), pos):
                talent = talent_choices[i]
                if talent in chosen:
                    chosen.remove(talent)
                elif len(chosen) < 2:
                    chosen.append(talent)
        names = ["智力", "体质", "颜值", "家境"]
        for i in range(len(names)):
            name = names[i]
            y = 486 + i * 60
            if hit((300, y + 4, 44, 44), pos) and attr_edit[name] > 0:
                attr_edit[name] = attr_edit[name] - 1
                points_left = points_left + 1
            if hit((360, y + 4, 44, 44), pos):
                if points_left > 0 and attr_edit[name] < 10:
                    attr_edit[name] = attr_edit[name] + 1
                    points_left = points_left - 1
        if hit((300, 440, 100, 36), pos):
            random_attr(names)
        if hit((410, 440, 100, 36), pos):
            clear_attr()
        if hit((30, 850, 150, 64), pos):
            scene = "首页"
        if hit((195, 850, 315, 64), pos):
            game.player.apply_talents(player, chosen)
            boosts = game.player.collect_boosts(chosen)
            forces = game.player.collect_forces(chosen)
            rewind_rate = game.player.collect_rewind(chosen)
            for name in names:
                player["attrs"][name] = float(attr_edit[name])
            player["months"].append({"time": "大一9月",
                                     "text": "你是一名" + player["gender"] + "生，是北理工的大一新生。"})
            if "北理新生" not in records["achievements"]:
                records["achievements"].append("北理新生")
                message = "达成成就：北理新生"
                popup_text = "达成成就：北理新生"
                popup_until = pygame.time.get_ticks() + 3000
            scene = "游戏"
            show_round()
            last_advance = pygame.time.get_ticks()
    elif scene == "游戏":
        if hit((30, 860, 150, 64), pos):
            show_round()
            last_advance = pygame.time.get_ticks()
        if hit((190, 860, 120, 64), pos):
            auto_on = not auto_on
            last_advance = pygame.time.get_ticks()
        if hit((320, 860, 90, 64), pos):
            if auto_speed == 1:
                auto_speed = 2
            elif auto_speed == 2:
                auto_speed = 4
            else:
                auto_speed = 1
        if hit((420, 860, 90, 64), pos):
            scene = "暂停"
    elif scene == "暂停":
        if hit((120, 430, 300, 64), pos):
            scene = "游戏"
        if hit((120, 520, 300, 64), pos):
            write_record("中途结束")
            scene = "首页"
    elif scene == "结局":
        if hit((30, 850, 150, 64), pos):
            detail_game = {"months": player["months"], "gender": player["gender"],
                           "talents": [t["name"] for t in chosen]}
            detail_from = "结局"
            scroll = 0
            scene = "回顾详情"
        elif hit((195, 850, 150, 64), pos):
            scene = "首页"
        elif hit((360, 850, 150, 64), pos):
            start_new_game()
    elif scene == "成就":
        if hit((120, 860, 300, 64), pos):
            scene = "首页"
    elif scene == "回顾":
        games = records["games"]
        for i in range(len(games)):
            if hit((30, 105 - scroll + i * 88, 480, 80), pos):
                detail_game = games[len(games) - 1 - i]
                detail_from = "回顾"
                scroll = 0
                scene = "回顾详情"
        if hit((30, 860, 200, 64), pos):
            game.records.export_records(records)
        if hit((245, 860, 265, 64), pos):
            scene = "首页"
    elif scene == "回顾详情":
        if hit((120, 860, 300, 64), pos):
            scene = detail_from


running = True


async def main():
    """主循环：桌面版与网页版共用；每帧 await 让出控制权（pygbag 要求）"""
    global running, scene, log_scroll, log_follow, scroll, last_advance
    while running:
        update_scale()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                if scene == "游戏":
                    log_scroll = log_scroll - event.y * 40
                    if log_scroll < 0:
                        log_scroll = 0
                    log_follow = False
                else:
                    scroll = scroll - event.y * 40
                    if scroll < 0:
                        scroll = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if scene == "游戏":
                        scene = "暂停"
                    elif scene == "暂停":
                        scene = "游戏"
                if scene == "游戏" and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    show_round()
                    last_advance = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and event.touch is False:
                click_sound.play()
                handle_click(event.pos)
            if event.type == pygame.FINGERDOWN:
                finger["start"] = touch_pos(event)
                finger["time"] = pygame.time.get_ticks()
            if event.type == pygame.FINGERUP:
                handle_finger_up(touch_pos(event))
        if scene == "游戏" and auto_on:
            now = pygame.time.get_ticks()
            if now - last_advance >= auto_speed * 1000:
                show_round()
                last_advance = now
        draw_background()
        if scene == "首页":
            draw_home()
        elif scene == "开局":
            draw_start()
        elif scene == "游戏":
            draw_game()
        elif scene == "暂停":
            draw_pause()
        elif scene == "结局":
            draw_ending()
        elif scene == "成就":
            draw_achievements()
        elif scene == "回顾":
            draw_review()
        else:
            draw_detail()
        if popup_text != "" and pygame.time.get_ticks() < popup_until:
            draw_card((20, 770, 340, 76), False, GREEN_LIGHT)
            draw_text(popup_text, 40, 788, 17, DARK_GREEN)
            draw_text("（成就已记录，可在首页「成就」查看）", 40, 814, 13, TEXT_DIM)
        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()


asyncio.run(main())
