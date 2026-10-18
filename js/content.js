/* Loading modules and turning their blocks into DOM.

   Knows nothing about routing. Inline text arrives as a small whitelisted
   subset of HTML written in tools/content/*.py: b, i, code, sub, sup, br
   (tools/lint-content.mjs checks it). */

import { pick, t } from './i18n.js';

const cache = new Map();
// Resolved against this module, not the page, so it works from any route or test page.
const DATA = new URL('../data/', import.meta.url);

async function json(name) {
  const path = new URL(name, DATA).href;
  if (!cache.has(path)) {
    cache.set(path, fetch(path).then(r => {
      if (!r.ok) throw new Error(`${path}: ${r.status}`);
      return r.json();
    }).catch(e => { cache.delete(path); throw e; }));
  }
  return cache.get(path);
}

export const loadIndex = () => json('index.json');
export const loadChapter = id => json(`${id}.json`);
export const loadData = name => json(`${name}.json`);

export function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v == null || v === false) continue;
    if (k === 'class') n.className = v;
    else if (k === 'html') n.innerHTML = v;
    else if (k.startsWith('on')) n.addEventListener(k.slice(2), v);
    else n.setAttribute(k, v === true ? '' : v);
  }
  for (const k of kids.flat(Infinity)) if (k != null) n.append(k instanceof Node ? k : String(k));
  return n;
}

// One language of a bilingual HTML value, as a fragment-ready string.
export const html = (value, lang) => pick(value, lang);

const NOTE_LABEL = { note: 'noteNote', key: 'noteKey', caution: 'noteCaution', exam: 'noteExam' };

function figure(b, ctx) {
  const src = typeof b.src === 'string' ? b.src : pick(b.src, ctx.lang);
  const img = el('img', { src, alt: pick(b.alt, ctx.lang), loading: 'lazy', decoding: 'async' });
  const cap = pick(b.caption, ctx.lang);
  const fig = el('figure', { class: 'figure' },
    el('button', { type: 'button', class: 'figure-zoom', 'aria-label': pick(b.alt, ctx.lang) || cap.replace(/<[^>]+>/g, ''), onclick: () => ctx.onZoom?.(src, cap) }, img),
    cap ? el('figcaption', { html: cap }) : null);
  return fig;
}

function table(b, ctx) {
  const L = ctx.lang;
  let headers, rows;
  if (b.by) ({ headers, rows } = b.by[L] || b.by.en);
  else { headers = b.headers.map(h => pick(h, L)); rows = b.rows.map(r => r.map(c => pick(c, L))); }
  const cap = pick(b.caption, L);
  // Each column gets a width class from its longest cell, so on a phone short
  // columns ("25–30%") stay on one line and prose columns keep a readable
  // width; a table wider than the screen then scrolls sideways instead of
  // squeezing every column.
  const widths = (headers || rows[0] || []).map((_, i) => colClass(Math.max(0, ...rows.map(r => textWidth(r[i])))));
  const head = headers?.length ? el('thead', {}, el('tr', {}, headers.map((h, i) =>
    el('th', { scope: 'col', class: textWidth(h) <= 18 ? `${widths[i]} th-one` : widths[i], html: h })))) : null;
  const scroll = el('div', { class: 'table-scroll', tabindex: '0' },
    el('table', { class: headers?.length >= 3 ? 'has-key' : null }, head,
      el('tbody', {}, rows.map(r => el('tr', {}, r.map((c, i) => el('td', { class: widths[i], html: c })))))));
  const hint = el('p', { class: 'table-hint', 'aria-hidden': 'true', hidden: true }, t('swipeTable', null, L));
  // Say "swipe" only when there is something to swipe to.
  if (typeof ResizeObserver === 'function') {
    new ResizeObserver(() => {
      const wide = scroll.scrollWidth > scroll.clientWidth + 2;
      hint.hidden = !wide;
      scroll.classList.toggle('is-wide', wide);
    }).observe(scroll);
  }
  return el('figure', { class: 'table-wrap' }, cap ? el('figcaption', { html: cap }) : null, scroll, hint);
}

// Rough display width of a cell: tags removed, CJK characters count double.
function textWidth(html) {
  const s = String(html ?? '').replace(/<[^>]*>/g, '').replace(/&[a-z#0-9]+;/gi, 'x').trim();
  let w = 0;
  for (const ch of s) w += /[\u2e80-\u9fff\uff00-\uffef]/.test(ch) ? 2 : 1;
  return w;
}
const colClass = w => (w <= 14 ? 'col-short' : w <= 40 ? 'col-mid' : 'col-long');

/* Quick check: tap an option, see whether it was right and
   why; every option's explanation opens once one is chosen. The choice is
   remembered (prefs.answers) under a key that is the same in both languages. */
export function quiz(b, ctx, key) {
  const L = ctx.lang;
  const chosen = ctx.answers?.[key];
  const li = el('div', { class: 'quiz-q', 'data-quiz': key });
  li.append(el('p', { class: 'quiz-label' }, t('checkUnderstanding', null, L)));
  li.append(el('div', { class: 'quiz-text', html: pick(b.q, L) }));
  const opts = el('div', { class: 'quiz-opts', role: 'list' });
  const hasAnswer = b.options.some(o => o.correct);
  const paint = pickedIdx => {
    [...opts.children].forEach((row, k) => {
      const o = b.options[k];
      row.classList.toggle('is-picked', k === pickedIdx);
      if (pickedIdx == null) return;
      row.classList.toggle('is-right', !!o.correct && hasAnswer);
      row.classList.toggle('is-wrong', k === pickedIdx && hasAnswer && !o.correct);
      row.querySelector('.quiz-why').hidden = !pick(o.why, L);
    });
    verdict.hidden = pickedIdx == null || !hasAnswer;
    if (pickedIdx != null && hasAnswer) {
      const ok = !!b.options[pickedIdx].correct;
      verdict.textContent = t(ok ? 'correct' : 'notQuite', null, L);
      verdict.className = `quiz-verdict ${ok ? 'is-ok' : 'is-no'}`;
      retry.hidden = ok;
    }
  };
  b.options.forEach((o, k) => {
    const row = el('div', { class: 'quiz-row', role: 'listitem' },
      el('button', { type: 'button', class: 'quiz-opt', html: pick(o.html, L), onclick: () => {
        ctx.onAnswer?.(key, k, !!o.correct);
        paint(k);
      } }),
      el('div', { class: 'quiz-why', hidden: true, html: pick(o.why, L) }));
    opts.append(row);
  });
  const verdict = el('p', { class: 'quiz-verdict', role: 'status', hidden: true });
  const retry = el('button', { type: 'button', class: 'button button-quiet quiz-retry', hidden: true, onclick: () => {
    ctx.onAnswer?.(key, null);
    [...opts.children].forEach(r => { r.className = 'quiz-row'; r.querySelector('.quiz-why').hidden = true; });
    verdict.hidden = true; retry.hidden = true;
  } }, t('tryAgain', null, L));
  li.append(opts, verdict, retry);
  if (chosen != null && chosen < b.options.length) paint(chosen);
  return li;
}

function block(b, ctx, key) {
  const L = ctx.lang;
  let node;
  switch (b.type) {
    case 'p': node = el('p', { html: pick(b.html, L) }); break;
    case 'h': node = el(b.level === 2 ? 'h3' : 'h4', { class: 'sub-h', html: pick(b.html, L) }); break;
    case 'list': {
      const items = b.items ? b.items.map(i => pick(i, L)) : (b.itemsBy[L] || b.itemsBy.en);
      node = el(b.ordered ? 'ol' : 'ul', {}, items.map((i, j) => el('li', { html: i, 'data-rk': `${key}.${j}` })));
      break;
    }
    case 'table': node = table(b, ctx); node.querySelectorAll('tbody tr').forEach((r, j) => { r.dataset.rk = `${key}.${j}`; }); break;
    case 'note': {
      const label = NOTE_LABEL[b.kind];
      const body = pick(b.html, L);
      node = el('aside', { class: `note note-${b.kind}` }, label ? el('p', { class: 'note-label' }, t(label, null, L)) : null, el('div', { html: body }));
      break;
    }
    case 'figure': node = figure(b, ctx); break;
    case 'quiz': node = quiz(b, ctx, key); break;
    case 'more':
      node = el('details', { class: 'more' }, el('summary', { html: pick(b.title, L) || '…' }),
        ...b.blocks.map((x, j) => block(x, ctx, `${key}.${j}`)).filter(Boolean));
      break;
    case 'code': node = el('pre', { class: 'code' }, el('code', {}, b.text)); break;
    default:
      console.warn('[content] unknown block type', b.type);
      return null;
  }
  if (['p', 'note'].includes(b.type)) node.dataset.rk = key;
  return node;
}

/* One lesson: key takeaways, the lesson itself, key terms. */
export function renderSection(chapter, sec, ctx) {
  const L = ctx.lang;
  const key = i => `${chapter.id}/${sec.id}#${i}`;
  const frag = document.createDocumentFragment();
  if (sec.takeaways?.length) frag.append(takeawayBox(sec, ctx, `${chapter.id}/${sec.id}#k`));
  sec.blocks.forEach((b, i) => { const n = block(b, ctx, key(i)); if (n) frag.append(n); });
  if (sec.terms?.length) frag.append(termChips(sec.terms, ctx));
  return frag;
}

export function takeawayBox(sec, ctx, keyBase, { open = true } = {}) {
  const L = ctx.lang;
  return el('details', { class: 'takeaways', open },
    el('summary', {}, el('span', { class: 'takeaways-icon', 'aria-hidden': 'true' }, '★'), t('takeaways', null, L)),
    el('ul', {}, sec.takeaways.map((x, j) => el('li', { html: pick(x, L), 'data-rk': `${keyBase}.${j}` }))));
}

export function termChips(ids, ctx) {
  return el('aside', { class: 'key-terms' },
    el('p', { class: 'key-terms-label' }, t('keyTerms', null, ctx.lang)),
    el('div', { class: 'chips' }, ids.map(id => {
      const term = ctx.terms?.get(id);
      return el('button', { type: 'button', class: 'chip term', 'data-term': id }, term ? pick(term.name, ctx.lang) : id.replace(/-/g, ' '));
    })));
}

/* Every quiz in a module, with the key it is stored under. */
export function quizzesOf(chapter) {
  const out = [];
  for (const sec of chapter.sections) {
    const walk = (blocks, base) => blocks.forEach((b, i) => {
      const key = `${base}${i}`;
      if (b.type === 'quiz' && b.options.some(o => o.correct)) out.push({ sec, block: b, key });
      if (b.type === 'more') walk(b.blocks, `${key}.`);
    });
    walk(sec.blocks, `${chapter.id}/${sec.id}#`);
  }
  return out;
}
