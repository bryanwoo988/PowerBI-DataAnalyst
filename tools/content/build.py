#!/usr/bin/env python3
"""Build data/*.json from the lesson sources in this folder.

    python3 tools/content/build.py

Writes index.json (courses, modules, lesson list), one cNN.json per module,
terms.json (glossary) and exam.json (the extra mock-exam questions).
data/releases.json is edited by hand. Deterministic: the same sources give
byte-identical files."""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
DATA = HERE.parent.parent / "data"

import s1_start, s2_prepare, s3_model, s4_visualize, s5_manage  # noqa: E402
from glossary import TERMS  # noqa: E402
from exam_bank import BANK  # noqa: E402

COURSES = [s1_start, s2_prepare, s3_model, s4_visualize, s5_manage]


def shuffle_options(module):
    """Lesson sources list the right answer anywhere, often first; shuffle
    each question's options with a seed from its id so the order is stable
    between builds but the answer is not always A."""
    for sec in module["sections"]:
        for i, b in enumerate(sec["blocks"]):
            if b["type"] == "quiz":
                random.Random(f"{module['id']}/{sec['id']}#{i}").shuffle(b["options"])


def write(name, obj):
    path = DATA / name
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return path


def main():
    DATA.mkdir(exist_ok=True)
    stages, chapters = [], []
    num = 0
    for course in COURSES:
        stage = dict(course.STAGE)
        stage["chapters"] = []
        for m in course.MODULES:
            shuffle_options(m)
            num += 1
            ch = {"id": m["id"], "num": num, "stage": stage["n"], "title": m["title"], "url": m["url"], "sections": m["sections"]}
            write(f"{m['id']}.json", ch)
            stage["chapters"].append(m["id"])
            chapters.append({
                "id": m["id"], "num": num, "stage": stage["n"], "title": m["title"],
                "minutes": sum(s["min"] or 0 for s in m["sections"]),
                "sections": [{"id": s["id"], "heading": s["heading"]} for s in m["sections"]],
            })
        stages.append(stage)
    write("index.json", {"app": {"en": "Power BI", "zh": "Power BI"}, "exam": "PL-300", "stages": stages, "chapters": chapters})
    write("terms.json", [{"id": i, "name": {"en": en, "zh": zh}, "def": {"en": [den], "zh": [dzh]}} for i, en, zh, den, dzh in TERMS])
    write("exam.json", BANK)
    lessons = sum(len(c["sections"]) for c in chapters)
    print(f"{len(stages)} courses, {len(chapters)} modules, {lessons} lessons, {len(TERMS)} terms, {len(BANK)} exam-bank questions")


if __name__ == "__main__":
    main()
