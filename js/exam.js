/* The mock exam: building an attempt, scoring it, and keeping the history.

   Pure logic plus its own storage (like study.js); the screens are in
   examview.js. Questions come from two places: every in-lesson check
   (key "c07/calculate#9", domain = the module's course) and the extra
   exam bank (key "x/m04"). Course 1 (getting started) is not an exam domain.

   The app's score is the share of questions answered right, shown on a
   0–1000 scale next to the 700 pass mark. Microsoft's own score is scaled
   differently, so the result screen says this is a guide, not a prediction. */

const KEY = 'pbi.exam.v1';
export const DOMAINS = [2, 3, 4, 5];
// 50 questions in the official proportions: 25–30% × 3, 15–20% × 1.
export const BLUEPRINT = { 2: 14, 3: 14, 4: 14, 5: 8 };
export const FULL_MINUTES = 100;
export const PRACTICE_SIZE = 20;
export const QUICK_SIZE = 10;
export const PASS = 700;
const HISTORY_MAX = 30;

/* ---------- Question pool ---------- */

// chapters: loaded module JSON; bank: data/exam.json.
export function buildPool(chapters, bank) {
  const pool = [];
  for (const ch of chapters) {
    if (!DOMAINS.includes(ch.stage)) continue;
    for (const sec of ch.sections) {
      sec.blocks.forEach((b, i) => {
        if (b.type !== 'quiz' || !b.options.some(o => o.correct)) return;
        pool.push({ key: `${ch.id}/${sec.id}#${i}`, domain: ch.stage, q: b.q, options: b.options, ref: `${ch.id}/${sec.id}` });
      });
    }
  }
  for (const x of bank) pool.push({ key: `x/${x.id}`, domain: x.domain, q: x.q, options: x.options, ref: x.ref });
  return pool;
}

/* ---------- Randomness (seedable, so tests are repeatable) ---------- */

export function rngFrom(seed) {
  let s = (seed >>> 0) || 1;
  return () => {
    s ^= s << 13; s >>>= 0;
    s ^= s >> 17;
    s ^= s << 5; s >>>= 0;
    return s / 4294967296;
  };
}

export function shuffle(list, rng) {
  const a = [...list];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/* ---------- Attempts ---------- */

/* mode: 'full' (blueprint, timed), 'domain' (one domain), 'quick',
   'retry' (the given keys). Questions are drawn without repeats; options
   are shuffled per question and the order is kept with the attempt. */
export function createAttempt({ mode, domain = null, keys = null, pool, rng = Math.random, now = Date.now() }) {
  let picked;
  if (mode === 'full') {
    picked = DOMAINS.flatMap(d => shuffle(pool.filter(q => q.domain === d), rng).slice(0, BLUEPRINT[d]));
    picked = shuffle(picked, rng);
  } else if (mode === 'domain') {
    picked = shuffle(pool.filter(q => q.domain === domain), rng).slice(0, PRACTICE_SIZE);
  } else if (mode === 'retry') {
    const want = new Set(keys ?? []);
    picked = shuffle(pool.filter(q => want.has(q.key)), rng);
  } else {
    picked = shuffle(pool, rng).slice(0, QUICK_SIZE);
  }
  return {
    mode, domain,
    items: picked.map(q => ({ key: q.key, order: shuffle(q.options.map((_, i) => i), rng) })),
    answers: {},          // item index → original option index
    flagged: [],
    at: 0,                // the question on screen
    startedAt: now,
    minutes: mode === 'full' ? FULL_MINUTES : null,
  };
}

export function secondsLeft(attempt, now = Date.now()) {
  if (!attempt.minutes) return null;
  return Math.max(0, Math.round(attempt.minutes * 60 - (now - attempt.startedAt) / 1000));
}

export function score(attempt, byKey) {
  const perDomain = {};
  const wrong = [];
  let right = 0, answered = 0;
  attempt.items.forEach((it, i) => {
    const q = byKey.get(it.key);
    if (!q) return;
    const d = (perDomain[q.domain] ??= { right: 0, total: 0 });
    d.total++;
    const a = attempt.answers[i];
    if (a != null) answered++;
    if (a != null && q.options[a]?.correct) { right++; d.right++; }
    else wrong.push(it.key);
  });
  const total = attempt.items.length;
  const points = total ? Math.round(1000 * right / total) : 0;
  return { right, total, answered, points, pass: points >= PASS, perDomain, wrong };
}

/* ---------- Storage: the attempt in progress and the history ---------- */

let state = { current: null, history: [] };
let store = null;
const isObj = v => v && typeof v === 'object' && !Array.isArray(v);

export function sanitise(raw) {
  const out = { current: null, history: [] };
  if (!isObj(raw)) return out;
  const c = raw.current;
  if (isObj(c) && Array.isArray(c.items) && c.items.every(i => isObj(i) && typeof i.key === 'string' && Array.isArray(i.order))) {
    out.current = {
      mode: ['full', 'domain', 'quick', 'retry'].includes(c.mode) ? c.mode : 'quick',
      domain: DOMAINS.includes(c.domain) ? c.domain : null,
      items: c.items,
      answers: isObj(c.answers) ? Object.fromEntries(Object.entries(c.answers).filter(([k, v]) => /^\d+$/.test(k) && Number.isInteger(v))) : {},
      flagged: Array.isArray(c.flagged) ? c.flagged.filter(Number.isInteger) : [],
      at: Number.isInteger(c.at) ? c.at : 0,
      startedAt: Number.isFinite(c.startedAt) ? c.startedAt : Date.now(),
      minutes: Number.isFinite(c.minutes) ? c.minutes : null,
    };
  }
  if (Array.isArray(raw.history)) {
    out.history = raw.history.filter(h => isObj(h) && Number.isFinite(h.points) && Number.isFinite(h.total)).slice(0, HISTORY_MAX);
  }
  return out;
}

function load() { try { return JSON.parse(store?.getItem(KEY) || '{}'); } catch { return {}; } }
function save() { try { store?.setItem(KEY, JSON.stringify(state)); } catch { /* not persisted */ } }

export function init(storage = globalThis.localStorage) {
  store = storage ?? null;
  state = sanitise(load());
}

export const current = () => state.current;
export const history = () => state.history.map(h => ({ ...h }));

export function start(attempt) { state.current = attempt; save(); return attempt; }
export function update(fn) { if (state.current) { fn(state.current); save(); } }
export function abandon() { state.current = null; save(); }

/* Finish the attempt in progress: score it, put it at the top of the
   history (with what is needed to review it) and clear it. */
export function finish(byKey, now = Date.now()) {
  const a = state.current;
  if (!a) return null;
  const s = score(a, byKey);
  const entry = {
    at: now, mode: a.mode, domain: a.domain,
    right: s.right, total: s.total, points: s.points, pass: s.pass, perDomain: s.perDomain,
    seconds: Math.round((now - a.startedAt) / 1000),
    items: a.items, answers: a.answers,
  };
  state.history.unshift(entry);
  state.history = state.history.slice(0, HISTORY_MAX);
  state.current = null;
  save();
  return entry;
}

export function clearHistory() { state.history = []; save(); }

export function best(mode = 'full') {
  const list = state.history.filter(h => h.mode === mode);
  return list.length ? Math.max(...list.map(h => h.points)) : null;
}
