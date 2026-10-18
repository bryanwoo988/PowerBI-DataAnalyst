# Power BI · PL-300

An offline, bilingual (English / 中文) study app for Microsoft's **PL-300:
Power BI Data Analyst** exam — lessons, quick checks inside each lesson, a
recap and module quiz for every module, and a scored mock exam. A static PWA:
no build step at run time, no CDN.

Live: <https://bryanwoo988.github.io/PowerBI-DataAnalyst/>

## What is inside

| Part | Contents |
|---|---|
| Courses | 5 courses, 14 modules, 58 lessons following Microsoft's PL-300 skills outline: Getting started · Prepare the data · Model the data · Visualize and analyze the data · Manage and secure Power BI |
| Quick checks | 87 questions inside the lessons, with instant feedback and explanations |
| Mock exam | 146-question pool (lesson checks + 63 exam-bank questions). Full exam: 50 questions in the official proportions (14/14/14/8), 100-minute timer, score out of 1000 against the 700 pass mark, results by skill area, every answer explained, retry wrong answers, history. Also practice by skill area (20) and quick quiz (10) |
| Study tools | Glossary of 111 terms, flashcards, search in both languages, highlights, notes, bookmarks, notes backup |

## Content and accuracy

The lessons and questions were written for this app, following the skills
listed in Microsoft's [PL-300 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/pl-300).
They are not Microsoft content and not real exam questions. Each lesson links
to the matching Microsoft Learn page. The app's score is the share of correct
answers on a 0–1000 scale; Microsoft's 700 is a scaled score, so the app's
score is a guide only. Power BI is a trademark of Microsoft; this app is not
affiliated with Microsoft.

## House conventions

First-run language picker (default English); English ⇄ 中文 that keeps your
place; light / dark / auto theme; six text sizes; offline after the first
visit; update prompt and "what's new" sheet; QR code, share and copy-link in
Settings; notes backup (export / import). See
[APP-STANDARDS.md](https://github.com/bryanwoo988/woobrothers.my/blob/main/APP-STANDARDS.md).

## Editing the content

Lessons live in `tools/content/s1_start.py` … `s5_manage.py`, the glossary in
`glossary.py`, the extra exam questions in `exam_bank.py`. Then:

```bash
python3 tools/content/build.py     # data/*.json
node tools/lint-content.mjs        # both languages, one right answer, links and terms exist
node tools/build-sw.mjs            # refresh the offline precache list
python3 tools/make-icons.py        # only after replacing icon.png
```

## Run it locally

```bash
python3 tools/serve.py             # http://127.0.0.1:4210/
```

The service worker is skipped on localhost unless you add `?sw=1`.

## Tests and checks

```bash
node --test 'tests/*.test.js'      # logic: exam, prefs, search, quizzes, SW, content lint
node tests/e2e.mjs                 # real browser at 375 px: a user's path, a full mock exam, every screen in both languages
```
