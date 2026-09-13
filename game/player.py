"""玩家与天赋"""

import random


def new_player(shuyuan_list):
    """新的一局：随机性别与书院，属性从 0 开始；性别写入 flags 供事件判定"""
    gender = random.choice(["男", "女"])
    return {
        "gender": gender,
        "shuyuan": random.choice(shuyuan_list),
        "major": "",
        "org": "",
        "attrs": {"智力": 0.0, "体质": 0.0, "颜值": 0.0, "家境": 0.0},
        "tags": [],
        "flags": [gender],
        "seen": [],
        "months": [],
        "term_bonus": 0,
        "rank": 0,
        "rank_pcts": [],
        "cet4": 0,
        "cet6": 0,
        "check_bonus": {},
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
    """应用选中的天赋：性别、书院、状态、判定加成，最后加属性"""
    for talent in chosen:
        if talent.get("gender"):
            player["gender"] = talent["gender"]
            for g in ("男", "女"):
                if g in player["flags"] and g != talent["gender"]:
                    player["flags"].remove(g)
            if talent["gender"] not in player["flags"]:
                player["flags"].append(talent["gender"])
        if talent["shuyuan"] != "":
            player["shuyuan"] = talent["shuyuan"]
        for flag in talent.get("flags_set", []):
            if flag not in player["flags"]:
                player["flags"].append(flag)
        for tag, bonus in talent.get("check_bonus", {}).items():
            player["check_bonus"][tag] = player["check_bonus"].get(tag, 0) + bonus
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