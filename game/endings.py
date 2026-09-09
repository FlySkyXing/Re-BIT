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