"""北理工重开模拟器 —— 游戏逻辑（不依赖 pygame）"""

import json
import random

# 四大书院与各自可选专业（专业名单待人类删改后更新）
SHUYUAN_MAJORS = {
    "睿信": ["计算机科学与技术", "软件工程", "人工智能", "电子信息工程", "通信工程", "自动化"],
    "求是": ["数学与应用数学", "应用物理学", "统计学", "化学", "化学工程与工艺", "生物技术", "生物医学工程"],
    "明德": ["工商管理", "经济学", "国际经济与贸易", "会计学", "法学", "英语", "工业设计"],
}

# 特立书院专业任选，可选范围 = 其他三个书院的全部专业
SHUYUAN_MAJORS["特立"] = (SHUYUAN_MAJORS["睿信"] + SHUYUAN_MAJORS["求是"]
                       + SHUYUAN_MAJORS["明德"])

ATTR_NAMES = ["智力", "体质", "颜值", "家境"]
TOTAL_POINTS = 20
MAX_ATTR = 10
TOTAL_ROUNDS = 48
MAJOR_ROUND = 13  # 第 13 回合（大二 9 月）开始分配专业


def load_data():
    """读三份数据文件"""
    with open("data/talents.json", "r", encoding="utf-8") as f:
        talents = json.load(f)
    with open("data/events.json", "r", encoding="utf-8") as f:
        events = json.load(f)
    with open("data/endings.json", "r", encoding="utf-8") as f:
        endings = json.load(f)
    return talents, events, endings


def new_player():
    """新的一局：书院随机分配，属性全 0 等玩家分配"""
    shuyuan = random.choice(list(SHUYUAN_MAJORS.keys()))
    return {
        "shuyuan": shuyuan,
        "major": "",
        "attrs": {"智力": 0, "体质": 0, "颜值": 0, "家境": 0},
        "tags": [],
        "seen": [],
    }


def draw_talents(talents):
    """开局抽 5 个天赋"""
    return random.sample(talents, 5)


def apply_talents(player, chosen):
    """应用选中的 3 个天赋"""
    for talent in chosen:
        if talent["shuyuan"] != "":
            player["shuyuan"] = talent["shuyuan"]
    for talent in chosen:
        for name, value in talent["effects"].items():
            player["attrs"][name] += value


def collect_boosts(chosen):
    """把天赋的抽事件加成汇总成 {标签: 倍率}"""
    boosts = {}
    for talent in chosen:
        for tag, times in talent["boost"].items():
            if tag in boosts:
                boosts[tag] = max(boosts[tag], times)
            else:
                boosts[tag] = times
    return boosts


def month_text(round_no):
    """第 1 回合 = 大一 9 月，第 48 回合 = 大四 8 月"""
    index = (round_no - 1) % 12
    month = (8 + index) % 12 + 1
    year = (round_no - 1) // 12 + 1
    year_name = ["大一", "大二", "大三", "大四"][year - 1]
    return year_name, year, month


def stage_of(year, month):
    """判断当前时段：军训 / 实习 / 期末 / 寒暑假 / 常规"""
    if year == 1 and month == 9:
        return "军训"
    if year == 4 and month >= 3 and month <= 5:
        return "实习"
    if month == 1 or month == 6:
        return "期末"
    if month == 2 or month == 7 or month == 8:
        return "寒暑假"
    return "常规"


def can_use(event, player, stage):
    """判断事件能否触发"""
    if event["stage"] != stage:
        return False
    for name, value in event["need"].items():
        if player["attrs"][name] < value:
            return False
    if event["shuyuan"] and player["shuyuan"] not in event["shuyuan"]:
        return False
    if event["major"] and player["major"] not in event["major"]:
        return False
    return True


def pick_event(events, player, stage, boosts):
    """筛选候选事件，按权重随机抽一条"""
    candidates = []
    weights = []
    for event in events:
        if not can_use(event, player, stage):
            continue
        if event["type"] == "特殊" and event["text"] in player["seen"]:
            continue
        weight = 1
        for tag, times in boosts.items():
            if tag in event["tags"]:
                weight = weight * times
        candidates.append(event)
        weights.append(weight)
    if len(candidates) == 0:
        return None
    return random.choices(candidates, weights=weights, k=1)[0]


def apply_event(player, event):
    """把事件效果应用到玩家身上，返回变化文字"""
    changes = []
    for name, value in event["effects"].items():
        player["attrs"][name] += value
        changes.append(f"{name}{value:+d}")
    for tag in event["tags"]:
        player["tags"].append(tag)
    if event["type"] == "特殊":
        player["seen"].append(event["text"])
    return "，".join(changes)


def assign_major(player):
    """系统在本书院范围内随机分配专业"""
    player["major"] = random.choice(SHUYUAN_MAJORS[player["shuyuan"]])
    return player["major"]


def judge_ending(endings, player):
    """每个结局算分，取最高分"""
    best = None
    best_score = 0
    for ending in endings:
        score = 0
        for name, weight in ending["weights"].items():
            if name in player["attrs"]:
                score += player["attrs"][name] * weight
            else:
                score += player["tags"].count(name) * weight
        if best is None or score > best_score:
            best = ending
            best_score = score
    return best