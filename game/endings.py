"""结局算分与选取"""

import random


def judge_ending(endings, player):
    """每个结局算分，取最高分；同分随机取一个"""
    best_score = None
    best_list = []
    for ending in endings:
        score = 0
        for name, weight in ending["weights"].items():
            if name in player["attrs"]:
                score = score + player["attrs"][name] * weight
            else:
                score = score + player["tags"].count(name) * weight
        score = round(score, 1)
        if best_score is None or score > best_score:
            best_score = score
            best_list = [ending]
        elif score == best_score:
            best_list.append(ending)
    return random.choice(best_list)


# 升学院校分层（全部为 985），按毕业时的能力分从高到低匹配
SCHOOLS = [
    (130, "清华大学"), (128, "北京大学"),
    (115, "上海交通大学"), (113, "复旦大学"), (111, "浙江大学"),
    (100, "北京航空航天大学"), (98, "哈尔滨工业大学"), (96, "同济大学"),
    (88, "西安交通大学"), (86, "武汉大学"), (84, "华中科技大学"),
    (75, "大连理工大学"), (73, "湖南大学"), (71, "重庆大学"), (70, "山东大学"),
]


def judge_school(player):
    """升学类结局的院校：能力分 = 智力 × 10 + 家境 × 2，取不低于该分的最高档"""
    score = player["attrs"]["智力"] * 10 + player["attrs"]["家境"] * 2
    for line, name in SCHOOLS:
        if score >= line:
            return name
    return SCHOOLS[-1][1]
