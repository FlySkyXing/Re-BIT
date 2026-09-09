"""成就判定"""


def check_achievements(achievements, player, event_text, ending_name):
    """检查三类成就，返回本局新达成的成就名列表

    - 结局类：本局结局命中
    - 事件类：本回合触发的特殊事件命中
    - 属性类：某属性达到指定数值
    """
    done = []
    for achievement in achievements:
        if achievement["type"] == "结局" and achievement["value"] == ending_name:
            done.append(achievement["name"])
        if achievement["type"] == "事件" and achievement["value"] == event_text:
            done.append(achievement["name"])
        if achievement["type"] == "属性":
            for name, value in achievement["value"].items():
                if player["attrs"][name] >= value:
                    done.append(achievement["name"])
    return done