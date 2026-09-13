"""成就判定"""


def check_achievements(achievements, player, event_text, ending_name, records):
    """检查成就，返回本局新达成的成就名列表

    - 结局：本局结局命中
    - 事件：本回合触发的（或判定结果的）文案命中
    - 属性：某属性达到指定值
    - 排名：综测排名在指定名次以内
    - 数值：玩家身上的数值字段达到指定值（如六级分数）
    - 全局：跨局累计（如走遍全国的省份数）
    """
    done = []
    for achievement in achievements:
        kind = achievement["type"]
        if kind == "结局" and achievement["value"] == ending_name:
            done.append(achievement["name"])
        if kind == "事件" and achievement["value"] == event_text:
            done.append(achievement["name"])
        if kind == "属性":
            for name, value in achievement["value"].items():
                if player["attrs"][name] >= value:
                    done.append(achievement["name"])
        if kind == "排名" and player["rank"] != 0 and player["rank"] <= achievement["value"]:
            done.append(achievement["name"])
        if kind == "数值":
            for name, value in achievement["value"].items():
                if player[name] >= value:
                    done.append(achievement["name"])
        if kind == "全局":
            for name, value in achievement["value"].items():
                if len(records[name]) >= value:
                    done.append(achievement["name"])
    return done