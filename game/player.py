"""玩家与天赋"""

import random


def new_player(shuyuan_list):
    """新的一局：书院随机分配，属性从 0 开始"""
    return {
        "shuyuan": random.choice(shuyuan_list),
        "major": "",
        "attrs": {"智力": 0.0, "体质": 0.0, "颜值": 0.0, "家境": 0.0},
        "tags": [],
        "flags": [],
        "seen": [],
        "months": [],
    }


def draw_talents(talents):
    """开局抽 5 个天赋：逐个按等级概率（蓝 75% / 紫 20% / 金 5%）决定等级，再随机取一个"""
    rates = talents["tier_rates"]
    pool = talents["talents"]
    tiers = list(rates.keys())
    weights = list(rates.values())
    drawn = []
    while len(drawn) < 5:
        tier = random.choices(tiers, weights=weights, k=1)[0]
        candidates = [t for t in pool if t["tier"] == tier and t not in drawn]
        if len(candidates) == 0:
            candidates = [t for t in pool if t not in drawn]
        drawn.append(random.choice(candidates))
    return drawn


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

def collect_forces(chosen):
    """汇总天赋的强制事件规则（tags 非空的才算）"""
    forces = []
    for talent in chosen:
        rule = talent["force"]
        if len(rule["tags"]) > 0:
            forces.append(rule)
    return forces


def collect_rewind(chosen):
    """汇总天赋的回溯概率（百分比，取最大）"""
    rate = 0
    for talent in chosen:
        if talent["rewind"] > rate:
            rate = talent["rewind"]
    return rate