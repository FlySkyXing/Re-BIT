"""近 5 局记录的读写与 txt 导出"""

import json

RECORDS_PATH = "save/records.json"


def load_records():
    """读存档（成就进度 + 近 5 局记录）"""
    with open(RECORDS_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)
    records.setdefault("provinces", [])
    return records


def save_records(records):
    """写回存档"""
    with open(RECORDS_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def save_record(records, game):
    """把本局加入记录，只保留最近 5 局"""
    records["games"].append(game)
    while len(records["games"]) > 5:
        records["games"].pop(0)


def export_records(records):
    """近 5 局逐局导出为 txt 到 exports/ 目录"""
    for game in records["games"]:
        name = "exports/" + game["date"] + "_" + game["ending"] + ".txt"
        with open(name, "w", encoding="utf-8") as f:
            f.write("书院：" + game["shuyuan"] + "　专业：" + game["major"] + "\n\n")
            for month in game["months"]:
                f.write(month["time"] + "　" + month["text"] + "\n")
            f.write("\n结局：" + game["ending"] + "\n")