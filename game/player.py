"""玩家与天赋"""

import random


def new_player(shuyuan_list):
    """新的一局：书院随机分配，属性从 0 开始"""
    return {
        "shuyuan": random.choice(shuyuan_list),
        "major": "",
        "attrs": {"智力": 0.0, "体质": 0.0, "颜值": 0.0, "家境": 0.0},
        "tags": [],
        "seen": [],
        "months": [],
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
            player["attrs"][name] = player["attrs"][name] + value


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