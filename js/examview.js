/* The mock-exam screens. Routes (app.js):
     #/exam              choose an exam, resume, history
     #/exam/run          the attempt in progress, one question at a time
     #/exam/result/N     result N of the history (0 = latest) and its review

   Unlike the in-lesson checks, the exam gives no feedback until the end,
   like the real one. Logic and storage live in exam.js. */

import { pick, t } from './i18n.js';
import { el, loadIndex, loadChapter, loadData } from './content.js';
import * as exam from './exam.js';

let pool = null, byKey = null, index = null;

export async function loadPool() {
  if (pool) return pool;
  index = await loadIndex();
  const [chapters, bank] = await Promise.all([Promise.all(index.chapters.map(c => loadChapter(c.id))), loadData('exam')]);
  pool = exam.buildPool(chapters, bank);
  byKey = new Map(pool.map(q => [q.key, q]));
  return pool;
}

const stageOf = n => index.stages.find(s => s.n === n);
const domainName = (n, L) => pick(stageOf(n).title, L);
const pct = (a, b) => (b ? Math.round(100 * a / b) : 0);
const clock = s => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;

function bar(value, total, cls = '') {
  const p = pct(value, total);
  return el('span', { class: `progress ${cls}`, role: 'progressbar', 'aria-valuenow': p, 'aria-valuemin': 0, 'aria-valuemax': 100 }, el('span', { style: `width:${p}%` }));
}

function modeLabel(h, L) {
  if (h.mode === 'full') return t('examFull', null, L);
  if (h.mode === 'domain') return `${t('examDomain', null, L)} · ${domainName(h.domain, L)}`;
  if (h.mode === 'retry') return t('examRetryWrong', null, L);
  return t('examQuick', null, L);
}

function when(ms, L) {
  const d = new Date(ms);
  const p = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
}

/* ---------- #/exam ---------- */
export async function examHome(L, { go }) {
  await loadPool();
  const startMode = (mode, domain = null) => {
    if (exam.current() && !confirm(t('examReplace', null, L))) return;
    exam.start(exam.createAttempt({ mode, domain, pool }));
    go('#/exam/run');
  };
  const cur = exam.current();
  const hist = exam.history();
  const best = exam.best('full');
  const counts = Object.fromEntries(exam.DOMAINS.map(d => [d, pool.filter(q => q.domain === d).length]));

  const resume = cur ? el('div', { class: 'card exam-resume' },
    el('p', {}, el('b', {}, t('examInProgress', null, L)), ' · ', modeLabel(cur, L), ' · ',
      t('examAnsweredOf', { done: Object.keys(cur.answers).length, total: cur.items.length }, L)),
    el('div', { class: 'hero-actions' },
      el('a', { class: 'button', href: '#/exam/run' }, t('examResume', null, L)),
      el('button', { type: 'button', class: 'button button-quiet', onclick: () => { if (confirm(t('examAbandonConfirm', null, L))) { exam.abandon(); go('#/exam', true); } } }, t('examAbandon', null, L)))) : null;

  const full = el('div', { class: 'card exam-card exam-card-main' },
    el('p', { class: 'kicker' }, 'PL-300'),
    el('h2', {}, t('examFull', null, L)),
    el('p', {}, t('examFullHint', { n: Object.values(exam.BLUEPRINT).reduce((a, b) => a + b, 0), min: exam.FULL_MINUTES }, L)),
    el('ul', { class: 'exam-blueprint' }, exam.DOMAINS.map(d => el('li', {},
      el('span', {}, domainName(d, L)), el('span', { class: 'muted' }, `${exam.BLUEPRINT[d]} · ${stageOf(d).weight}`)))),
    el('div', { class: 'hero-actions' },
      el('button', { type: 'button', class: 'button', onclick: () => startMode('full') }, t('examStart', null, L)),
      best != null ? el('span', { class: 'muted' }, t('examBest', { n: best }, L)) : null));

  const practice = el('div', { class: 'card exam-card' },
    el('h2', {}, t('examDomain', null, L)),
    el('p', {}, t('examDomainHint', { n: exam.PRACTICE_SIZE }, L)),
    el('div', { class: 'exam-domains' }, exam.DOMAINS.map(d => el('button', { type: 'button', class: `exam-domain stage-${d}`, onclick: () => startMode('domain', d) },
      el('span', { class: 'exam-domain-name' }, domainName(d, L)),
      el('span', { class: 'muted' }, `${stageOf(d).weight} · ${t('examPoolCount', { n: counts[d] }, L)}`)))));

  const quick = el('div', { class: 'card exam-card' },
    el('h2', {}, t('examQuick', null, L)),
    el('p', {}, t('examQuickHint', { n: exam.QUICK_SIZE }, L)),
    el('button', { type: 'button', class: 'button button-quiet', onclick: () => startMode('quick') }, t('examStart', null, L)));

  const histList = hist.length ? el('section', {},
    el('h2', { class: 'lib-h' }, t('examHistory', null, L)),
    el('ol', { class: 'exam-history' }, hist.map((h, i) => el('li', {}, el('a', { href: `#/exam/result/${i}` },
      el('span', { class: `exam-pill ${h.pass ? 'is-pass' : 'is-fail'}` }, String(h.points)),
      el('span', { class: 'exam-history-text' },
        el('span', {}, modeLabel(h, L)),
        el('span', { class: 'muted' }, `${when(h.at, L)} · ${t('recapScore', { done: h.right, total: h.total }, L)}`)))))),
    el('button', { type: 'button', class: 'rd-btn', onclick: () => { if (confirm(t('examClearConfirm', null, L))) { exam.clearHistory(); go('#/exam', true); } } }, t('examClear', null, L))) : null;

  return el('div', { class: 'page page-exam' },
    el('h1', {}, t('exam', null, L)),
    el('p', { class: 'lede' }, t('examLede', { pool: pool.length }, L)),
    resume, full, practice, quick, histList,
    el('p', { class: 'muted small' }, t('examDisclaimer', null, L)));
}

/* ---------- #/exam/run ---------- */
export async function examRun(L, { go, onLeave }) {
  await loadPool();
  const a = exam.current();
  if (!a) return examHome(L, { go });
  const host = el('div', { class: 'page page-exam-run' });
  const timer = el('span', { class: 'exam-timer', role: 'timer', 'aria-live': 'off' });

  const submit = (force = false) => {
    const cur = exam.current();
    const left = cur.items.length - Object.keys(cur.answers).length;
    if (!force && left > 0 && !confirm(t('examUnanswered', { n: left }, L))) return;
    if (!force && left === 0 && !confirm(t('examSubmitConfirm', null, L))) return;
    exam.finish(byKey);
    go('#/exam/result/0');
  };

  const tick = () => {
    const s = exam.secondsLeft(exam.current() ?? a);
    if (s == null) return;
    timer.textContent = `⏱ ${clock(s)}`;
    timer.classList.toggle('is-low', s < 300);
    if (s === 0 && exam.current()) submit(true);
  };
  if (a.minutes) { tick(); const id = setInterval(tick, 1000); onLeave(() => clearInterval(id)); }

  const paint = () => {
    const cur = exam.current();
    if (!cur) return;
    const i = Math.min(cur.at, cur.items.length - 1);
    const it = cur.items[i];
    const q = byKey.get(it.key);
    const flagged = cur.flagged.includes(i);
    const answered = Object.keys(cur.answers).length;
    const setAt = n => { exam.update(c => { c.at = n; }); paint(); window.scrollTo(0, 0); };

    const opts = el('div', { class: 'quiz-opts exam-opts', role: 'radiogroup', 'aria-label': t('pickAnswer', null, L) },
      it.order.map((orig, k) => {
        const on = cur.answers[i] === orig;
        return el('button', { type: 'button', role: 'radio', 'aria-checked': String(on), class: `quiz-opt exam-opt${on ? ' is-picked' : ''}`,
          onclick: () => { exam.update(c => { c.answers[i] = orig; }); paint(); } },
          el('span', { class: 'exam-letter' }, 'ABCDEFGH'[k]), el('span', { html: pick(q.options[orig].html, L) }));
      }));

    const grid = el('details', { class: 'exam-grid-wrap' },
      el('summary', {}, t('examOverview', { done: answered, total: cur.items.length }, L)),
      el('div', { class: 'exam-grid' }, cur.items.map((_, n) => el('button', {
        type: 'button', 'aria-label': t('examQuestionN', { n: n + 1, total: cur.items.length }, L),
        class: [cur.answers[n] != null ? 'is-done' : '', cur.flagged.includes(n) ? 'is-flag' : '', n === i ? 'is-here' : ''].join(' '),
        onclick: () => setAt(n),
      }, String(n + 1)))));

    host.replaceChildren(
      el('div', { class: 'exam-top' },
        el('span', { class: 'kicker' }, modeLabel(cur, L)),
        timer),
      bar(answered, cur.items.length),
      el('div', { class: 'card exam-q' },
        el('div', { class: 'exam-q-head' },
          el('span', { class: 'muted' }, t('examQuestionN', { n: i + 1, total: cur.items.length }, L), ' · ', domainName(q.domain, L)),
          el('button', { type: 'button', class: `exam-flag${flagged ? ' on' : ''}`, 'aria-pressed': String(flagged),
            onclick: () => { exam.update(c => { c.flagged = flagged ? c.flagged.filter(x => x !== i) : [...c.flagged, i]; }); paint(); } },
            flagged ? `⚑ ${t('examFlagged', null, L)}` : `⚐ ${t('examFlag', null, L)}`)),
        el('div', { class: 'quiz-text', html: pick(q.q, L) }),
        opts),
      el('div', { class: 'exam-nav' },
        el('button', { type: 'button', class: 'button button-quiet', disabled: i === 0, onclick: () => setAt(i - 1) }, `‹ ${t('prev', null, L)}`),
        i < cur.items.length - 1
          ? el('button', { type: 'button', class: 'button', onclick: () => setAt(i + 1) }, `${t('next', null, L)} ›`)
          : el('button', { type: 'button', class: 'button', onclick: () => submit() }, t('examSubmit', null, L))),
      grid,
      el('div', { class: 'exam-foot' },
        el('button', { type: 'button', class: 'rd-btn', onclick: () => submit() }, t('examSubmit', null, L)),
        el('a', { class: 'rd-btn', href: '#/exam' }, t('examPause', null, L))));
  };
  paint();
  return host;
}

/* ---------- #/exam/result/N ---------- */
export async function examResult(L, { n = 0, go }) {
  await loadPool();
  const h = exam.history()[n];
  if (!h) return examHome(L, { go });
  const doms = Object.keys(h.perDomain).map(Number).sort();
  const wrongKeys = h.items.filter((it, i) => !byKey.get(it.key)?.options[h.answers[i]]?.correct).map(it => it.key).filter(k => byKey.has(k));
  const skipped = h.items.filter((it, i) => h.answers[i] == null && byKey.has(it.key)).length;
  const answered = h.items.length - h.items.filter((_, i) => h.answers[i] == null).length;
  const weakest = doms.length > 1 ? doms.reduce((w, d) => (pct(h.perDomain[d].right, h.perDomain[d].total) < pct(h.perDomain[w].right, h.perDomain[w].total) ? d : w)) : null;

  const review = el('ol', { class: 'exam-review' }, h.items.map((it, i) => {
    const q = byKey.get(it.key);
    if (!q) return null;
    const mine = h.answers[i];
    const ok = mine != null && q.options[mine]?.correct;
    const [chId, secId] = q.ref ? q.ref.split('/') : [];
    // A question left blank keeps its answer hidden: handing in early must
    // not turn the exam into an answer sheet for the next attempt. Retry
    // shows it once the question has been tried.
    if (mine == null) {
      return el('li', { class: 'exam-review-item is-no is-skip' },
        el('p', { class: 'kicker' }, `${i + 1} · ${domainName(q.domain, L)} · — ${t('examSkipped', null, L)}`),
        el('div', { class: 'quiz-text', html: pick(q.q, L) }),
        el('p', { class: 'muted small' }, t('examSkippedHidden', null, L)));
    }
    return el('li', { class: `exam-review-item ${ok ? 'is-ok' : 'is-no'}`, 'data-ok': ok ? '1' : '0' },
      el('p', { class: 'kicker' }, `${i + 1} · ${domainName(q.domain, L)} · `, ok ? `✓ ${t('correct', null, L)}` : `✗ ${t(mine == null ? 'examSkipped' : 'notQuite', null, L)}`),
      el('div', { class: 'quiz-text', html: pick(q.q, L) }),
      el('ul', { class: 'exam-review-opts' }, it.order.map(orig => {
        const o = q.options[orig];
        const cls = [o.correct ? 'is-right' : '', orig === mine && !o.correct ? 'is-wrong' : ''].join(' ');
        const why = pick(o.why, L);
        return el('li', { class: cls },
          el('span', { html: pick(o.html, L) }),
          orig === mine ? el('span', { class: 'exam-yours' }, ` · ${t('examYourAnswer', null, L)}`) : null,
          why && (o.correct || orig === mine) ? el('span', { class: 'exam-why', html: why }) : null);
      })),
      chId ? el('p', { class: 'muted small' }, el('a', { href: `#/ch/${chId}/${secId}` }, `${t('examStudyLesson', null, L)} ›`)) : null);
  }));
  const onlyWrong = el('label', { class: 'exam-only-wrong' },
    el('input', { type: 'checkbox', onchange: e => review.classList.toggle('only-wrong', e.target.checked) }), ' ', t('examOnlyWrong', null, L));

  return el('div', { class: 'page page-exam-result' },
    el('p', { class: 'kicker' }, el('a', { href: '#/exam' }, t('exam', null, L)), ' · ', modeLabel(h, L)),
    el('h1', {}, t('examResult', null, L)),
    el('div', { class: `card exam-score ${h.pass ? 'is-pass' : 'is-fail'}` },
      el('div', { class: 'exam-points' }, el('span', { class: 'exam-points-n' }, String(h.points)), el('span', { class: 'muted' }, ' / 1000')),
      el('p', { class: 'exam-verdict' }, h.pass ? t('examPass', { n: exam.PASS }, L) : t('examFail', { n: exam.PASS }, L)),
      el('p', { class: 'muted' }, [t('recapScore', { done: h.right, total: h.total }, L), `${pct(h.right, h.total)}%`,
        answered < h.items.length ? t('examAnsweredOf', { done: answered, total: h.items.length }, L) : null,
        t('examTime', { t: clock(h.seconds) }, L), when(h.at, L)].filter(Boolean).join(' · '))),
    doms.length ? el('div', { class: 'card exam-domains-result' },
      el('h2', {}, t('examByDomain', null, L)),
      doms.map(d => el('div', { class: 'exam-dom-row' },
        el('span', { class: 'exam-dom-name' }, domainName(d, L)),
        el('span', { class: 'muted' }, `${h.perDomain[d].right}/${h.perDomain[d].total} · ${pct(h.perDomain[d].right, h.perDomain[d].total)}%`),
        bar(h.perDomain[d].right, h.perDomain[d].total, pct(h.perDomain[d].right, h.perDomain[d].total) >= 70 ? 'is-good' : 'is-weak'))),
      weakest ? el('p', { class: 'muted' }, t('examWeakest', { d: domainName(weakest, L) }, L), ' ', el('a', { href: `#/stage/${weakest}` }, `${t('examReview', null, L)} ›`)) : null) : null,
    el('div', { class: 'hero-actions' },
      wrongKeys.length ? el('button', { type: 'button', class: 'button', onclick: () => {
        if (exam.current() && !confirm(t('examReplace', null, L))) return;
        exam.start(exam.createAttempt({ mode: 'retry', keys: wrongKeys, pool }));
        go('#/exam/run');
      } }, skipped ? t('examRetryMixedN', { n: wrongKeys.length, wrong: wrongKeys.length - skipped, skip: skipped }, L) : t('examRetryWrongN', { n: wrongKeys.length }, L)) : null,
      el('a', { class: 'button button-quiet', href: '#/exam' }, t('examNew', null, L))),
    el('h2', { class: 'lib-h' }, t('examAnswers', null, L)),
    onlyWrong,
    review,
    el('p', { class: 'muted small' }, t('examDisclaimer', null, L)));
}
