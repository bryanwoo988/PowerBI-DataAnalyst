import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import * as exam from '../js/exam.js';

const read = f => JSON.parse(readFileSync(new URL(`../data/${f}.json`, import.meta.url), 'utf8'));
const index = read('index');
const pool = exam.buildPool(index.chapters.map(c => read(c.id)), read('exam'));
const byKey = new Map(pool.map(q => [q.key, q]));

function memStore(init = {}) {
  const m = new Map(Object.entries(init));
  return { getItem: k => m.get(k) ?? null, setItem: (k, v) => m.set(k, String(v)), m };
}

test('the pool has lesson checks and bank questions, keys unique, no getting-started questions', () => {
  assert.equal(byKey.size, pool.length);
  assert.ok(pool.some(q => q.key.startsWith('x/')) && pool.some(q => /^c\d\d\//.test(q.key)));
  assert.ok(pool.every(q => exam.DOMAINS.includes(q.domain)));
  assert.ok(!pool.some(q => q.key.startsWith('c01/')));
});

test('every domain has enough questions for the full exam and for practice', () => {
  for (const d of exam.DOMAINS) {
    const n = pool.filter(q => q.domain === d).length;
    assert.ok(n >= exam.BLUEPRINT[d] && n >= exam.PRACTICE_SIZE, `domain ${d}: ${n}`);
  }
});

test('a full exam follows the blueprint, has no repeats and is timed', () => {
  const a = exam.createAttempt({ mode: 'full', pool, rng: exam.rngFrom(42), now: 0 });
  assert.equal(a.items.length, 50);
  assert.equal(new Set(a.items.map(i => i.key)).size, 50);
  for (const d of exam.DOMAINS) assert.equal(a.items.filter(i => byKey.get(i.key).domain === d).length, exam.BLUEPRINT[d]);
  assert.equal(a.minutes, 100);
  assert.equal(exam.secondsLeft(a, 60e3), 100 * 60 - 60);
  assert.equal(exam.secondsLeft(a, 200 * 60e3), 0);
});

test('options are shuffled but every original option is kept', () => {
  const a = exam.createAttempt({ mode: 'quick', pool, rng: exam.rngFrom(7) });
  for (const it of a.items) assert.deepEqual([...it.order].sort(), byKey.get(it.key).options.map((_, i) => i));
  assert.ok(a.items.some(it => it.order.some((v, i) => v !== i)));
});

test('domain practice stays in its domain; retry uses exactly the given keys', () => {
  const a = exam.createAttempt({ mode: 'domain', domain: 5, pool, rng: exam.rngFrom(3) });
  assert.ok(a.items.every(i => byKey.get(i.key).domain === 5));
  const keys = pool.slice(0, 4).map(q => q.key);
  const r = exam.createAttempt({ mode: 'retry', keys, pool, rng: exam.rngFrom(3) });
  assert.deepEqual(r.items.map(i => i.key).sort(), [...keys].sort());
});

test('scoring: right answers, unanswered count as wrong, points out of 1000, pass at 700', () => {
  const a = exam.createAttempt({ mode: 'quick', pool, rng: exam.rngFrom(9) });
  a.items.forEach((it, i) => {
    const q = byKey.get(it.key);
    const right = q.options.findIndex(o => o.correct);
    if (i < 7) a.answers[i] = right;                       // 7 right
    else if (i < 9) a.answers[i] = (right + 1) % q.options.length; // 2 wrong
  });                                                        // 1 unanswered
  const s = exam.score(a, byKey);
  assert.deepEqual([s.right, s.total, s.answered, s.points, s.pass], [7, 10, 9, 700, true]);
  assert.equal(s.wrong.length, 3);
  assert.equal(Object.values(s.perDomain).reduce((n, d) => n + d.total, 0), 10);
});

test('an attempt survives a reload, finishing moves it into the history', () => {
  const store = memStore();
  exam.init(store);
  exam.start(exam.createAttempt({ mode: 'quick', pool, rng: exam.rngFrom(1), now: 1000 }));
  exam.update(c => { c.answers[0] = 0; c.at = 3; });
  exam.init(store);
  assert.equal(exam.current().at, 3);
  assert.equal(exam.current().answers[0], 0);
  const h = exam.finish(byKey, 61000);
  assert.equal(h.seconds, 60);
  assert.equal(exam.current(), null);
  exam.init(store);
  assert.equal(exam.history().length, 1);
  assert.equal(exam.best('quick'), h.points);
  assert.equal(exam.best('full'), null);
});

test('corrupted storage falls back to an empty state', () => {
  exam.init(memStore({ 'pbi.exam.v1': 'not json' }));
  assert.equal(exam.current(), null);
  assert.deepEqual(exam.history(), []);
  const s = exam.sanitise({ current: { items: [{ key: 'x/p01', order: [0, 1] }], answers: { 0: 1, x: 2, 1: 'a' } }, history: [{ points: 'x' }, { points: 500, total: 10 }] });
  assert.deepEqual(s.current.answers, { 0: 1 });
  assert.equal(s.history.length, 1);
});
