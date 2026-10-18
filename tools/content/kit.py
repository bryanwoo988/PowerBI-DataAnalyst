"""Authoring helpers for the lesson source files (s1_start.py … s5_manage.py).

Every helper takes the English text first and the Chinese second and returns
the block shape js/content.js renders, so a lesson reads top to bottom like
the page it becomes. Inline HTML is limited to the tags tools/lint-content.mjs
allows: b, i, code, br, sub, sup.
"""


def T(en, zh):
    return {"en": en, "zh": zh}


def P(en, zh):
    return {"type": "p", "html": T(en, zh)}


def H(en, zh):
    return {"type": "h", "level": 2, "html": T(en, zh)}


def UL(*items, ordered=False):
    return {"type": "list", "ordered": ordered, "items": [T(en, zh) for en, zh in items]}


def OL(*items):
    return UL(*items, ordered=True)


def TABLE(headers, rows, caption=None):
    cell = lambda c: c if isinstance(c, str) else T(*c)
    b = {"type": "table", "headers": [cell(h) for h in headers], "rows": [[cell(c) for c in r] for r in rows]}
    if caption:
        b["caption"] = T(*caption)
    return b


def NOTE(kind, en, zh):
    """kind: note | key | caution | exam"""
    return {"type": "note", "kind": kind, "html": T(en, zh)}


def EXAM(en, zh):
    """An exam tip: what the question writers like to test."""
    return NOTE("exam", en, zh)


def CODE(text):
    return {"type": "code", "text": text.strip("\n")}


def FIG(src, alt, caption):
    return {"type": "figure", "src": src, "alt": T(*alt), "caption": T(*caption)}


def O(correct, en, zh, why_en="", why_zh=""):
    return {"html": T(en, zh), "correct": bool(correct), "why": T(why_en, why_zh)}


def Q(en, zh, *options):
    return {"type": "quiz", "q": T(en, zh), "options": list(options)}


def lesson(id, heading, minutes, takeaways, blocks, terms=(), url=None):
    return {
        "id": id,
        "heading": T(*heading),
        "min": minutes,
        "url": url,
        "takeaways": [T(en, zh) for en, zh in takeaways],
        "terms": list(terms),
        "blocks": blocks,
    }


def module(id, title, lessons, url=None):
    return {"id": id, "title": T(*title), "url": url, "sections": lessons}
