"""结局判定与升学院校"""

import math
import random

# 升学院校分层：(能力分下限, 校名, 是否高于北理层级)
SCHOOLS = [
    (130, "清华大学", True),
    (128, "北京大学", True),
    (115, "中国科学院大学", True),
    (115, "上海交通大学", True),
    (113, "复旦大学", True),
    (111, "浙江大学", True),
    (100, "北京航空航天大学", True),
    (98, "哈尔滨工业大学", True),
    (96, "同济大学", False),
    (88, "西安交通大学", False),
    (86, "武汉大学", False),
    (84, "华中科技大学", False),
    (75, "大连理工大学", False),
    (73, "湖南大学", False),
    (71, "重庆大学", False),
    (70, "山东大学", False),
]

# 综测得分 → 年级百分位的两个参数：得分越高百分位越小
RANK_TOP = 28
RANK_SPAN = 54


def rank_percentile(score):
    """综测得分换算成年纪百分位（1 ~ 100，越小越好）"""
    pct = 100 - 100 * (score - RANK_TOP) / RANK_SPAN
    if pct < 1:
        pct = 1
    if pct > 100:
        pct = 100
    return pct


def average_rank(player):
    """平均综测百分位（6 次综测的均值）"""
    return sum(player["rank_pcts"]) / len(player["rank_pcts"])


def fits(ending, player):
    """硬门槛：need（属性下限 / 标签次数下限）、need_max（属性上限）、rank_max（平均百分位上限）"""
    for name, value in ending.get("need", {}).items():
        if name in player["attrs"]:
            if player["attrs"][name] < value:
                return False
        elif player["tags"].count(name) < value:
            return False
    for name, value in ending.get("need_max", {}).items():
        if player["attrs"][name] >= value:
            return False
    for flag in ending.get("flags_need", []):
        if flag not in player["flags"]:
            return False
    if "rank_max" in ending and average_rank(player) > ending["rank_max"]:
        return False
    return True


def ending_score(ending, player):
    """边际效用得分：每个因子的贡献取平方根（收益递减）再乘权重"""
    total = 0
    for name, weight in ending["weights"].items():
        if name in player["attrs"]:
            value = player["attrs"][name]
        else:
            value = player["tags"].count(name)
        total = total + math.sqrt(value) * weight
    return total


def pick(pool, player):
    """按竞争权重抽一个：权重 × 边际效用得分 × 随机系数"""
    weights = []
    for ending in pool:
        weight = ending["weight"] * ending_score(ending, player) * random.uniform(0.7, 1.3)
        if weight < 0.01:
            weight = 0.01
        weights.append(weight)
    return random.choices(pool, weights=weights, k=1)[0]


def judge_ending(endings, player):
    """① 延毕优先 ② 硬门槛过滤 ③ 升学类内部竞争 ④ 升学胜者与就业类竞争 ⑤ 待业兜底"""
    for ending in endings:
        if ending["kind"] == "学业" and fits(ending, player):
            return ending
    rise = []
    work = []
    for ending in endings:
        if ending["kind"] == "升学" and fits(ending, player):
            rise.append(ending)
        if ending["kind"] == "就业" and fits(ending, player):
            work.append(ending)
    if len(rise) == 0 and len(work) == 0:
        for ending in endings:
            if ending["kind"] == "兜底":
                return ending
    if len(rise) > 0:
        work.append(pick(rise, player))
    return pick(work, player)


def judge_school(player, high_only):
    """升学类院校：能力分 = 智力 × 10 + 家境 × 2，取不低于该分的最高档"""
    ability = player["attrs"]["智力"] * 10 + player["attrs"]["家境"] * 2
    school = ""
    for line, name, high in SCHOOLS:
        if high_only and high is False:
            continue
        school = name
        if ability >= line:
            return name
    return school