"""事件筛选与生效"""

import random


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
    """筛出候选事件，按权重随机抽一条；没有候选返回 None"""
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


def apply_event(player, event, time_text):
    """应用事件效果，记入本局每月文本，返回变化文字"""
    changes = []
    for name, value in event["effects"].items():
        player["attrs"][name] = player["attrs"][name] + value
        changes.append(f"{name}{value:+}")
    for tag in event["tags"]:
        player["tags"].append(tag)
    if event["type"] == "特殊":
        player["seen"].append(event["text"])
    player["months"].append({"time": time_text, "text": event["text"]})
    return "，".join(changes)