/* The glossary (data/terms.json, written for this app): lookups and the
   term sheet that opens when a key-term chip is tapped. */

import { pick, t } from './i18n.js';
import { el, loadData } from './content.js';

let byId = null;

export async function loadTerms() {
  if (!byId) byId = new Map((await loadData('terms')).map(x => [x.id, x]));
  return byId;
}

export const termById = id => byId?.get(id);

// Bottom sheet with the definition, the name in the other language, and
// the lessons that list the term.
export function openTermSheet(id, { lang, openSheet, lessons = [] }) {
  const term = termById(id);
  if (!term) return;
  const other = lang === 'zh' ? 'en' : 'zh';
  const alt = pick(term.name, other);
  openSheet(el('div', { class: 'term-sheet' },
    el('p', { class: 'term-sheet-kicker' }, t('glossary', null, lang)),
    el('h3', {}, pick(term.name, lang), alt && alt !== pick(term.name, lang) ? el('span', { class: 'abbr' }, ` · ${alt}`) : null),
    ...(term.def[lang] || term.def.en).map(p => el('p', { html: p })),
    lessons.length ? el('ul', { class: 'term-lessons' }, lessons.map(l => el('li', {}, el('a', { href: l.href }, l.title)))) : null));
}
