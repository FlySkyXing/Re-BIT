"""数据读取、书院与专业名单、分专业"""

import json
import random

# 四大书院与各自可选专业（见 docs/02-游戏设计.md）
SHUYUAN_MAJORS = {
    "睿信": ["计算机科学与技术", "软件工程", "人工智能", "电子信息工程", "通信工程", "自动化"],
    "求是": ["数学与应用数学", "应用物理学", "统计学", "化学", "化学工程与工艺", "生物技术", "生物医学工程"],
    "明德": ["工商管理", "经济学", "国际经济与贸易", "会计学", "法学", "英语", "工业设计"],
}

# 特立书院专业任选 = 其他三个书院的全部专业
SHUYUAN_MAJORS["特立"] = (SHUYUAN_MAJORS["睿信"] + SHUYUAN_MAJORS["求是"]
                        + SHUYUAN_MAJORS["明德"])

SHUYUAN_LIST = ["睿信", "求是", "明德", "特立"]


def load_data():
    """读四份 JSON 文案"""
    with open("data/talents.json", "r", encoding="utf-8") as f:
        talents = json.load(f)
    with open("data/events.json", "r", encoding="utf-8") as f:
        events = json.load(f)
    with open("data/endings.json", "r", encoding="utf-8") as f:
        endings = json.load(f)
    with open("data/achievements.json", "r", encoding="utf-8") as f:
        achievements = json.load(f)
    return talents, events, endings, achievements


def assign_major(player):
    """系统在本书院范围内随机分配专业"""
    player["major"] = random.choice(SHUYUAN_MAJORS[player["shuyuan"]])
    return player["major"]