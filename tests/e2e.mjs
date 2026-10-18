/* End-to-end check in a real browser (Playwright + Chromium):

     python3 tools/serve.py &          # http://127.0.0.1:4210/
     node tests/e2e.mjs                # PLAYWRIGHT=/path/to/playwright if not found

   1. A user's path: language picker, a lesson's quick check, the recap and
      "mastered", a glossary term, a full mock exam answered and scored,
      the review and the retry of wrong answers, settings with the QR code,
      search across languages.
   2. Every module, lesson and recap, and every exam and tool screen, in
      English and Chinese at 375 px wide: no script error, no "could not
      load", no sideways scrolling.
   Not part of `node --test` (it needs a browser and the dev server).
   SHOTS=dir saves screenshots of the main screens. */
import { createRequire } from 'module';
import fs from 'fs';
import { execSync } from 'child_process';
const require = createRequire(import.meta.url);
const PW = process.env.PLAYWRIGHT || `${execSync('npm root -g').toString().trim()}/playwright`;
const { chromium } = require(PW);
const BASE = process.env.BASE || 'http://127.0.0.1:4210/';
const SHOTS = process.env.SHOTS;
let failed = 0;
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 375, height: 760 } });
const errs = [];
p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
p.on('dialog', d => d.accept());
const ok = (c, msg) => { if (!c) failed++; console.log((c ? 'PASS ' : 'FAIL ') + msg); };
const go = async (hash, wait = 700) => { await p.goto(BASE + hash); await p.waitForTimeout(wait); };
const shot = async name => { if (SHOTS) await p.screenshot({ path: `${SHOTS}/${name}.png`, fullPage: false }); };

await p.goto(BASE);
await p.waitForTimeout(800);
ok(await p.isVisible('#picker'), 'first run shows the language picker');
await shot('picker');
await p.click('#picker [data-lang="en"]');
await p.waitForTimeout(600);
ok((await p.textContent('h1')).includes('Power BI'), 'home titled Power BI');
ok(await p.isVisible('.exam-home-card'), 'home links to the mock exam');
await shot('home-en');

// a lesson's quick check
await go('#/ch/c02/storage-modes', 1000);
const q = p.locator('.quiz-q').first();
ok(!!(await q.getAttribute('data-quiz')), 'lesson has a quick check');
await q.locator('.quiz-opt').first().click();
await p.waitForTimeout(200);
ok(await q.locator('.quiz-verdict').isVisible(), 'answering shows a verdict');
await shot('lesson-en');

// recap and mastered
await go('#/ch/c02/recap', 1000);
ok(await p.locator('.recap-quiz .quiz-q').count() >= 6, 'recap repeats the module questions');
await p.locator('.recap-foot button.button').first().click();
await p.waitForTimeout(500);
await go('#/stage/2');
ok(await p.locator('.ch-read').count() === 1, 'module marked as mastered');

// glossary term sheet
await go('#/ch/c06/star-schema', 1000);
await p.locator('.key-terms .chip').first().click();
await p.waitForTimeout(500);
ok(await p.isVisible('.term-sheet'), 'tapping a key term opens its sheet');
ok(await p.locator('.term-lessons a').count() >= 1, 'term sheet lists its lessons');

// full mock exam
await go('#/exam', 1200);
await shot('exam-home-en');
await p.locator('.exam-card-main button.button').click();
await p.waitForTimeout(800);
ok((await p.textContent('.exam-q')).includes('Question 1 of 50'), 'full exam has 50 questions');
ok(/⏱ \d+:\d\d/.test(await p.textContent('.exam-timer')), 'full exam shows a timer');
await shot('exam-q-en');
for (let i = 0; i < 50; i++) {
  await p.locator('.exam-opt').nth(i % 3).click();
  if (i === 4) await p.locator('.exam-flag').click();
  if (i < 49) await p.locator('.exam-nav .button:not(.button-quiet)').click();
}
ok(await p.locator('.exam-grid .is-done').count() === 50, 'all 50 answered in the overview grid');
ok(await p.locator('.exam-grid .is-flag').count() === 1, 'one question flagged');
await p.locator('.exam-nav .button:not(.button-quiet)').click();
await p.waitForTimeout(900);
const pts = Number(await p.textContent('.exam-points-n'));
ok(Number.isFinite(pts) && pts >= 0 && pts <= 1000, `scored ${pts} / 1000`);
ok(await p.locator('.exam-dom-row').count() === 4, 'result broken down into 4 skill areas');
ok(await p.locator('.exam-review-item').count() === 50, 'review lists all 50 answers');
await shot('exam-result-en');
await p.locator('.exam-only-wrong input').check();
const visibleOk = await p.locator('.exam-review-item.is-ok').evaluateAll(ns => ns.filter(n => n.offsetParent).length);
ok(visibleOk === 0, 'only-wrong filter hides correct answers');
const wrong = await p.locator('.exam-review-item.is-no').count();
if (wrong) {
  await p.locator('.page-exam-result .hero-actions .button').first().click();
  await p.waitForTimeout(800);
  ok((await p.textContent('.exam-q')).includes(`of ${wrong}`), `retry has the ${wrong} wrong answers`);
  await p.locator('.exam-foot a').click();
  await p.waitForTimeout(800);
  ok(await p.isVisible('.exam-resume'), 'a paused exam can be resumed');
}
await go('#/exam', 900);
ok(await p.locator('.exam-history li').count() >= 1, 'exam history lists the attempt');

// settings, search, Chinese
await go('#/settings', 900);
ok(await p.locator('.qr svg').count() === 1, 'settings shows the QR code');
await go('#/search', 800);
await p.fill('#search-input', '行级别安全性');
await p.waitForTimeout(400);
ok(await p.locator('.search-results a[href="#/ch/c14/rls"]').count() >= 1, 'Chinese search finds the RLS lesson in English mode');

// every screen in both languages
const index = await (await fetch(BASE + 'data/index.json')).json();
const routes = ['#/', '#/tools', '#/tools/glossary', '#/tools/cards', '#/tools/quiz', '#/tools/quiz/c07', '#/notes', '#/bookmarks', '#/settings', '#/share', '#/exam', '#/exam/result/0'];
for (const s of index.stages) routes.push(`#/stage/${s.n}`);
for (const c of index.chapters) { routes.push(`#/ch/${c.id}`, `#/ch/${c.id}/recap`); for (const s of c.sections) routes.push(`#/ch/${c.id}/${s.id}`); }
for (const L of ['en', 'zh']) {
  await p.evaluate(l => { const k = 'pbi.prefs.v1'; const v = JSON.parse(localStorage.getItem(k) || '{}'); v.lang = l; v.chosen = true; localStorage.setItem(k, JSON.stringify(v)); }, L);
  await p.reload();
  await p.waitForTimeout(600);
  ok((await p.getAttribute('html', 'lang')).startsWith(L), `switched to ${L}`);
  let bad = 0;
  for (const r of routes) {
    await p.goto(BASE + r);
    await p.waitForTimeout(250);
    const st = await p.evaluate(() => ({ wide: document.documentElement.scrollWidth > innerWidth + 1, err: !!document.querySelector('.error'), main: document.querySelector('#main').textContent.length }));
    if (st.wide || st.err || st.main < 20) { bad++; console.log(`  ${L} ${r}`, st); }
  }
  ok(bad === 0, `${routes.length} screens in ${L}: none broken or wider than 375 px`);
  if (L === 'zh') {
    await go('#/', 600); await shot('home-zh');
    await go('#/ch/c07/calculate', 900); await shot('lesson-zh');
    await go('#/exam/result/0', 900); await shot('exam-result-zh');
  }
}

ok(errs.length === 0, `no console errors${errs.length ? ': ' + errs.slice(0, 5).join(' | ') : ''}`);
await b.close();
if (SHOTS) console.log('screenshots in', SHOTS, fs.readdirSync(SHOTS).length);
process.exit(failed ? 1 : 0);
