"""时间轴与时段判定"""


def month_text(round_no):
    """第 1 回合 = 大一 9 月，第 48 回合 = 大四 8 月"""
    index = (round_no - 1) % 12
    month = (8 + index) % 12 + 1
    year = (round_no - 1) // 12 + 1
    year_name = ["大一", "大二", "大三", "大四"][year - 1]
    return year_name, year, month


def stage_of(year, month):
    """判断当前时段（七个时段互不重叠：寒假与暑假分开）"""
    if year == 1 and month == 9:
        return "军训"
    if year == 4 and 3 <= month <= 5:
        return "实习"
    if year == 4 and month == 6:
        return "答辩"
    if month == 1 or month == 6:
        return "期末"
    if month == 2:
        return "寒假"
    if month == 7 or month == 8:
        return "暑假"
    return "常规"