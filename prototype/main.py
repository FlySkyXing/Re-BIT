"""北理工重开模拟器 —— pygame 界面

运行：python main.py
"""

import pygame
import game

WIDTH = 800
HEIGHT = 600
FONT_PATH = "C:/Windows/Fonts/msyh.ttc"

BG = (24, 26, 34)
TEXT = (232, 232, 236)
DIM = (150, 152, 164)
BTN = (62, 92, 142)
BTN_ON = (96, 156, 214)
BTN_OFF = (58, 60, 72)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("北理工重开模拟器")
font_big = pygame.font.Font(FONT_PATH, 30)
font_mid = pygame.font.Font(FONT_PATH, 21)
font_small = pygame.font.Font(FONT_PATH, 17)

talents, events, endings = game.load_data()

# 按钮位置
CONFIRM_RECT = pygame.Rect(300, 530, 200, 50)
START_RECT = pygame.Rect(300, 530, 200, 50)
CONTINUE_RECT = pygame.Rect(280, 520, 180, 50)
AUTO_RECT = pygame.Rect(480, 520, 120, 50)
SPEED_RECT = pygame.Rect(620, 520, 140, 50)
AGAIN_RECT = pygame.Rect(300, 420, 200, 50)

# 全局游戏状态
state = "天赋"
player = None
boosts = {}
talent_choices = []
chosen = []
attr_edit = {"智力": 0, "体质": 0, "颜值": 0, "家境": 0}
points_left = game.TOTAL_POINTS
round_no = 1
shown_time = ""
event_text = ""
change_text = ""
major_text = ""
ending = None
auto_on = False
auto_speed = 2
last_advance = 0


def draw_text(text, x, y, font, color=TEXT):
    """在屏幕上画一行字"""
    screen.blit(font.render(text, True, color), (x, y))


def wrap_text(text, font, max_width):
    """按像素宽度把长文本拆成多行"""
    lines = []
    line = ""
    for ch in text:
        if font.size(line + ch)[0] > max_width:
            lines.append(line)
            line = ch
        else:
            line = line + ch
    lines.append(line)
    return lines


def draw_button(rect, text, font, on=False):
    """画一个按钮"""
    color = BTN_ON if on else BTN
    pygame.draw.rect(screen, color, rect, border_radius=8)
    label = font.render(text, True, (255, 255, 255))
    x = rect.x + (rect.width - label.get_width()) // 2
    y = rect.y + (rect.height - label.get_height()) // 2
    screen.blit(label, (x, y))


def start_new_game():
    """回到开局：抽天赋"""
    global state, player, boosts, talent_choices, chosen, attr_edit, points_left
    global round_no, shown_time, event_text, change_text, major_text
    global ending, auto_on, auto_speed
    player = game.new_player()
    boosts = {}
    talent_choices = game.draw_talents(talents)
    chosen = []
    attr_edit = {"智力": 0, "体质": 0, "颜值": 0, "家境": 0}
    points_left = game.TOTAL_POINTS
    round_no = 1
    shown_time = ""
    event_text = ""
    change_text = ""
    major_text = ""
    ending = None
    auto_on = False
    auto_speed = 2
    state = "天赋"


def show_round():
    """推进一个回合：分专业、抽事件、应用效果"""
    global round_no, shown_time, event_text, change_text, major_text, ending, state
    year_name, year, month = game.month_text(round_no)
    shown_time = year_name + str(month) + "月"
    stage = game.stage_of(year, month)
    major_text = ""
    if round_no == game.MAJOR_ROUND:
        major_text = "大二开学，你被分到「" + game.assign_major(player) + "」专业。"
    event = game.pick_event(events, player, stage, boosts)
    if event is None:
        event_text = shown_time + "，这个月没什么特别的事。"
        change_text = ""
    else:
        event_text = event["text"]
        change_text = game.apply_event(player, event)
    round_no = round_no + 1
    if round_no > game.TOTAL_ROUNDS:
        ending = game.judge_ending(endings, player)
        state = "结局"


def draw_talent_state():
    """抽天赋界面"""
    draw_text("抽取天赋：从下面 5 个里选 3 个", 50, 30, font_big)
    for i in range(len(talent_choices)):
        t = talent_choices[i]
        rect = pygame.Rect(50, 90 + i * 80, 700, 70)
        on = t in chosen
        pygame.draw.rect(screen, BTN_ON if on else BTN_OFF, rect, border_radius=8)
        draw_text(t["name"], rect.x + 16, rect.y + 10, font_mid)
        draw_text(t["desc"], rect.x + 16, rect.y + 40, font_small, DIM)
    draw_button(CONFIRM_RECT, "确定（已选 " + str(len(chosen)) + "/3）", font_mid, len(chosen) == 3)


def draw_attr_state():
    """分配属性界面"""
    draw_text("分配属性点：每项 0-10，共 20 点", 50, 30, font_big)
    for i in range(len(game.ATTR_NAMES)):
        name = game.ATTR_NAMES[i]
        y = 110 + i * 70
        draw_text(name, 120, y, font_mid)
        draw_text(str(attr_edit[name]), 330, y, font_mid)
        draw_button(pygame.Rect(390, y - 5, 44, 44), "-", font_mid)
        draw_button(pygame.Rect(460, y - 5, 44, 44), "+", font_mid)
    draw_text("剩余点数：" + str(points_left), 120, 410, font_mid)
    draw_button(START_RECT, "开始大学四年", font_mid, points_left == 0)


def draw_game_state():
    """游戏中界面"""
    draw_text(shown_time, 40, 24, font_big)
    line = "书院：" + player["shuyuan"]
    if player["major"] != "":
        line = line + "　专业：" + player["major"]
    draw_text(line, 300, 32, font_small, DIM)
    info = ""
    for name in game.ATTR_NAMES:
        info = info + name + " " + str(player["attrs"][name]) + "　"
    draw_text(info, 40, 80, font_mid)
    y = 150
    if major_text != "":
        for line in wrap_text(major_text, font_mid, 720):
            draw_text(line, 40, y, font_mid, (240, 220, 140))
            y = y + 32
        y = y + 8
    for line in wrap_text(event_text, font_mid, 720):
        draw_text(line, 40, y, font_mid)
        y = y + 32
    if change_text != "":
        draw_text("（" + change_text + "）", 40, y + 8, font_small, (140, 210, 160))
    draw_button(CONTINUE_RECT, "继续", font_mid)
    draw_button(AUTO_RECT, "自动:开" if auto_on else "自动:关", font_small, auto_on)
    draw_button(SPEED_RECT, str(auto_speed) + " 秒", font_small)


def draw_ending_state():
    """结局界面"""
    draw_text("结局：" + ending["name"], 50, 60, font_big)
    y = 140
    for line in wrap_text(ending["text"], font_mid, 700):
        draw_text(line, 50, y, font_mid)
        y = y + 34
    draw_text("书院：" + player["shuyuan"] + "　专业：" + player["major"], 50, 330, font_small, DIM)
    draw_button(AGAIN_RECT, "再来一次", font_mid)


start_new_game()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and state == "游戏":
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                show_round()
                last_advance = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if state == "天赋":
                for i in range(len(talent_choices)):
                    rect = pygame.Rect(50, 90 + i * 80, 700, 70)
                    if rect.collidepoint(pos):
                        t = talent_choices[i]
                        if t in chosen:
                            chosen.remove(t)
                        elif len(chosen) < 3:
                            chosen.append(t)
                if CONFIRM_RECT.collidepoint(pos) and len(chosen) == 3:
                    game.apply_talents(player, chosen)
                    boosts = game.collect_boosts(chosen)
                    state = "属性"
            elif state == "属性":
                for i in range(len(game.ATTR_NAMES)):
                    name = game.ATTR_NAMES[i]
                    y = 110 + i * 70
                    if pygame.Rect(390, y - 5, 44, 44).collidepoint(pos) and attr_edit[name] > 0:
                        attr_edit[name] = attr_edit[name] - 1
                        points_left = points_left + 1
                    if pygame.Rect(460, y - 5, 44, 44).collidepoint(pos):
                        if points_left > 0 and attr_edit[name] < game.MAX_ATTR:
                            attr_edit[name] = attr_edit[name] + 1
                            points_left = points_left - 1
                if START_RECT.collidepoint(pos) and points_left == 0:
                    player["attrs"] = attr_edit
                    state = "游戏"
                    show_round()
                    last_advance = pygame.time.get_ticks()
            elif state == "游戏":
                if CONTINUE_RECT.collidepoint(pos):
                    show_round()
                    last_advance = pygame.time.get_ticks()
                if AUTO_RECT.collidepoint(pos):
                    auto_on = not auto_on
                    last_advance = pygame.time.get_ticks()
                if SPEED_RECT.collidepoint(pos):
                    if auto_speed == 1:
                        auto_speed = 2
                    elif auto_speed == 2:
                        auto_speed = 4
                    else:
                        auto_speed = 1
            elif state == "结局":
                if AGAIN_RECT.collidepoint(pos):
                    start_new_game()
    if state == "游戏" and auto_on:
        now = pygame.time.get_ticks()
        if now - last_advance >= auto_speed * 1000:
            show_round()
            last_advance = now
    screen.fill(BG)
    if state == "天赋":
        draw_talent_state()
    elif state == "属性":
        draw_attr_state()
    elif state == "游戏":
        draw_game_state()
    else:
        draw_ending_state()
    pygame.display.flip()
pygame.quit()