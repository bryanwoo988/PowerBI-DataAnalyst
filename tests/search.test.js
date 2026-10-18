import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { buildIndex, search, normalise, plain } from '../js/search.js';

const read = f => JSON.parse(readFileSync(new URL(`../data/${f}.json`, import.meta.url), 'utf8'));
const index = buildIndex([read('c02')], read('terms'));

test('a Chinese query finds the lesson, titled in the reading language', () => {
  const hits = search(index, '存储模式', 'en');
  assert.ok(hits.some(h => h.route === '#/ch/c02/storage-modes'));
  assert.ok(hits.every(h => !/[一-鿿]/.test(h.title)), hits.map(h => h.title).join(' | '));
});
test('Latin search ignores case and accents', () => {
  assert.ok(search(index, 'DIRECTQUERY', 'zh').length > 0);
  assert.equal(normalise('Évaluation'), 'evaluation');
});
test('all words must match', () => {
  assert.ok(search(index, 'privacy level', 'en').length > 0);
  assert.equal(search(index, 'privacy zebra', 'en').length, 0);
});
test('glossary terms are found and open the term', () => {
  assert.ok(search(index, 'role-playing dimension', 'en').some(h => h.route === '#/term/role-playing-dimension'));
});
test('snippets contain no markup', () => {
  for (const h of search(index, 'import', 'en')) assert.ok(!/[<>]/.test(h.snippet), h.snippet);
  assert.equal(plain('<b>a</b> &amp; b'), 'a & b');
});
test('empty query returns nothing', () => assert.deepEqual(search(index, '  ', 'en'), []));
