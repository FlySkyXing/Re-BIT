"""事件筛选与生效"""

import random


def can_use(event, player, stage):
    """判断事件能否触发：时段、属性下限、书院、专业、状态（flags）"""
    if stage not in event["stage"]:
        return False
    for name, value in event.get("need", {}).items():
        if player["attrs"][name] < value:
            return False
    for name, value in event.get("need_max", {}).items():
        if player["attrs"][name] >= value:
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
        chance = event.get("chance", 100)
        if event.get("chance_attr"):
            spec = event["chance_attr"]
            chance = spec["base"]
            for name, factor in spec["attrs"].items():
                chance = chance + player["attrs"][name] * factor
            if chance > spec["max"]:
                chance = spec["max"]
        if random.randint(1, 100) > chance:
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


def roll_check(player, event):
    """掷判定，返回 (结果分支, 分数)

    - 只算分（check.score）：返回 (None, 分数)，用于四六级这类只出分的判定
    - 多档（check.levels）：得分 = base + Σ(属性值 × 系数) + random(0, roll)，取 min 不超过得分的最高档
    - 二选一（success / fail）：base + Σ(属性值 × 系数) 作为成功率（夹 5~95），掷 1~100
    - 天赋 check_bonus 命中的标签会加成得分
    """
    check = event["check"]
    if "score" in check:
        spec = check["score"]
        val = spec["base"]
        for name, factor in spec["attrs"].items():
            val = val + player["attrs"][name] * factor
        val = val + random.randint(0, spec.get("roll", 0))
        if val > spec["max"]:
            val = spec["max"]
        return None, int(val)
    score = check["base"]
    for name, factor in check["attrs"].items():
        score = score + player["attrs"][name] * factor
    for tag, bonus in player["check_bonus"].items():
        if tag in event["tags"]:
            score = score + bonus
    if "levels" in check:
        score = score + random.randint(0, check.get("roll", 0))
        for level in check["levels"]:
            if score >= level["min"]:
                return level, None
        return check["levels"][-1], None
    if score > 95:
        score = 95
    if score < 5:
        score = 5
    if random.randint(1, 100) <= score:
        return check["success"], None
    return check["fail"], None


def apply_event(player, event, time_text):
    """应用事件效果，记入本局每月文本，返回最终显示文案（判定结果文案）

    - 事件带 check 时先掷判定（见 roll_check），判定结果决定文案与效果
    - flags_set 获得状态，flags_clear 移除状态
    - rank_bonus 累加到本学期的综测加分
    - set_org 记录加入的学生组织
    """
    text = event["text"]
    effects = event["effects"]
    flags_set = event.get("flags_set", [])
    rank_bonus = event.get("rank_bonus", 0)
    check = event.get("check")
    if check:
        result, got_score = roll_check(player, event)
        if got_score is None:
            text = result["text"]
            effects = result.get("effects", {})
            flags_set = result.get("flags_set", [])
            rank_bonus = rank_bonus + result.get("rank_bonus", 0)
        else:
            text = event["text"].replace("{score}", str(got_score))
            if event.get("score_field"):
                player[event["score_field"]] = got_score
    if event.get("set_org"):
        player["org"] = event["set_org"].replace("{shuyuan}", player["shuyuan"])
    player["term_bonus"] = player["term_bonus"] + rank_bonus
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
    text = text.replace("{shuyuan}", player["shuyuan"])
    if event["type"] == "特殊":
        player["seen"].append(event["text"])
    player["months"].append({"time": time_text, "text": text})
    return text