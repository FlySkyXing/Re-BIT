"""事件筛选与生效"""

import random


def can_use(event, player, stage):
    """判断事件能否触发：时段、属性下限、书院、专业、状态（flags）"""
    if stage not in event["stage"]:
        return False
    for name, value in event.get("need", {}).items():
        if player["attrs"][name] < value:
            return False
    if event.get("shuyuan") and player["shuyuan"] not in event["shuyuan"]:
        return False
    if event.get("major") and player["major"] not in event["major"]:
        return False
    for flag in event.get("flags_need", []):
        if flag not in player["flags"]:
            return False
    for flag in event.get("flags_forbid", []):
        if flag in player["flags"]:
            return False
    return True


def apply_forces(events, stage, round_no, forces):
    """按天赋的强制规则收窄候选事件池；没有命中规则、或收窄后为空，则不收窄"""
    for rule in forces:
        hit = False
        if rule["round"] != 0 and rule["round"] == round_no:
            hit = True
        if stage in rule["stages"]:
            hit = True
        if hit:
            picked = []
            for event in events:
                if stage not in event["stage"]:
                    continue
                for tag in rule["tags"]:
                    if tag in event["tags"]:
                        picked.append(event)
                        break
            if len(picked) > 0:
                return picked
    return events

def pick_event(events, player, stage, boosts):
    """筛出候选事件，按权重随机抽一条；没有候选返回 None

    - 事件自带 weight 作为基础权重（保底事件 weight 0.2）
    - 天赋 boost 命中的标签，权重再乘倍率
    - 先掷事件自带的 chance（默认 100），未通过则本月无事件
    """
    candidates = []
    weights = []
    for event in events:
        if not can_use(event, player, stage):
            continue
        if event["type"] == "特殊" and event["text"] in player["seen"]:
            continue
        if random.randint(1, 100) > event.get("chance", 100):
            continue
        weight = event.get("weight", 1)
        for tag, times in boosts.items():
            if tag in event["tags"]:
                weight = weight * times
        candidates.append(event)
        weights.append(weight)
    if len(candidates) == 0:
        return None
    return random.choices(candidates, weights=weights, k=1)[0]


def apply_event(player, event, time_text):
    """应用事件效果，记入本局每月文本，返回变化文字

    - 事件带 check 时先掷判定：成功率 = base + Σ(属性值 × 系数)，夹在 5~95
    - 判定结果决定文案与效果
    - flags_set 获得状态，flags_clear 移除状态
    """
    text = event["text"]
    effects = event["effects"]
    flags_set = event.get("flags_set", [])
    check = event.get("check")
    if check:
        rate = check["base"]
        for name, factor in check["attrs"].items():
            rate = rate + player["attrs"][name] * factor
        if rate > 95:
            rate = 95
        if rate < 5:
            rate = 5
        if random.randint(1, 100) <= rate:
            result = check["success"]
        else:
            result = check["fail"]
        text = result["text"]
        effects = result.get("effects", {})
        flags_set = result.get("flags_set", [])
    changes = []
    for name, value in effects.items():
        player["attrs"][name] = player["attrs"][name] + value
        changes.append(f"{name}{value:+}")
    for tag in event["tags"]:
        player["tags"].append(tag)
    for flag in flags_set:
        if flag not in player["flags"]:
            player["flags"].append(flag)
    for flag in event.get("flags_clear", []):
        if flag in player["flags"]:
            player["flags"].remove(flag)
    if event["type"] == "特殊":
        player["seen"].append(event["text"])
    player["months"].append({"time": time_text, "text": text})
    return "，".join(changes)