/* Language resolution and the interface string table.

   Every translatable value is a {en, zh} object; pick() is the single
   place that turns one into a string. Knows nothing about the DOM. */

import { get as getPrefs } from './prefs.js';

const FALLBACK = ['en', 'zh'];

// Each language named in itself: the first-run picker appears before any
// language has been chosen to label the others in.
export const LANG_NATIVE = { en: 'English', zh: '中文' };

export function current() {
  return getPrefs().lang;
}

export function pick(value, lang = current()) {
  if (value == null) return '';
  if (typeof value === 'string' || typeof value === 'number') return String(value);
  if (value[lang]) return value[lang];
  for (const f of FALLBACK) if (value[f]) return value[f];
  return '';
}

export function t(key, vars, lang = current()) {
  let s = pick(UI[key], lang);
  if (!s) console.warn(`[i18n] no UI string "${key}"`);
  if (vars) for (const [k, v] of Object.entries(vars)) s = s.replaceAll(`{${k}}`, String(v));
  return s;
}

export const UI = {
  appName: { en: 'Power BI', zh: 'Power BI' },
  tagline: {
    en: 'Study for the PL-300 Power BI Data Analyst exam: lessons, quick checks and a scored mock exam, in English and Chinese — offline',
    zh: '备考 PL-300 Power BI 数据分析师认证：课程、随堂小测和计分模拟考试，中英双语，可离线使用',
  },

  home: { en: 'Home', zh: '首页' },
  courseN: { en: 'Course {n}', zh: '课程 {n}' },
  examWeight: { en: '{w} of the exam', zh: '占考试 {w}' },
  chapterN: { en: 'Module {n}', zh: '第 {n} 单元' },
  chaptersCount: { en: '{n} modules', zh: '{n} 个单元' },
  pagesCount: { en: '{n} lessons', zh: '{n} 课' },
  minutes: { en: '{n} min', zh: '{n} 分钟' },
  progress: { en: '{done} of {total} mastered', zh: '已掌握 {done}/{total}' },
  continueReading: { en: 'Continue reading', zh: '继续上次阅读' },
  startHere: { en: 'Start with the first lesson', zh: '从第一课开始' },
  prev: { en: 'Previous', zh: '上一个' },
  next: { en: 'Next', zh: '下一个' },
  close: { en: 'Close', zh: '关闭' },
  source: { en: 'Source', zh: '来源' },
  lessonN: { en: 'Lesson {n}', zh: '第 {n} 课' },
  inThisModule: { en: 'In this module', zh: '本单元内容' },

  /* Study layer */
  takeaways: { en: 'Key takeaways', zh: '必会知识点' },
  keyTerms: { en: 'Key terms', zh: '关键词' },
  checkUnderstanding: { en: 'Quick check', zh: '随堂小测' },
  pickAnswer: { en: 'Pick an answer', zh: '选一个答案' },
  correct: { en: 'Correct', zh: '答对了' },
  notQuite: { en: 'Not quite', zh: '不太对' },
  tryAgain: { en: 'Try again', zh: '再试一次' },
  recap: { en: 'Recap', zh: '本单元复习' },
  recapHint: { en: 'Everything this module asked you to remember, on one card, with all its questions again.', zh: '这个单元要记住的重点整理在一张卡上，并附上本单元的全部题目。' },
  recapQuiz: { en: 'Module quiz', zh: '单元测验' },
  recapScore: { en: '{done} of {total} right', zh: '答对 {done}/{total}' },
  mastered: { en: "I've mastered this", zh: '我已掌握' },
  isMastered: { en: 'Mastered', zh: '已掌握' },
  readOriginal: { en: 'Read more on Microsoft Learn ↗', zh: '在 Microsoft Learn 阅读更多 ↗' },
  licence: {
    en: 'Study notes and questions written for this app, following Microsoft’s PL-300 skills outline. Not affiliated with or endorsed by Microsoft; Power BI is a trademark of Microsoft. The questions are practice material, not real exam questions.',
    zh: '本 App 的学习笔记和题目按照 Microsoft PL-300 考试技能大纲自行编写。与 Microsoft 无关，也未获其认可；Power BI 是 Microsoft 的商标。题目是练习材料，不是真实考题。',
  },
  noteNote: { en: 'Note', zh: '注意' },
  noteKey: { en: 'Key point', zh: '重点' },
  noteCaution: { en: 'Watch out', zh: '小心' },
  noteExam: { en: 'Exam tip', zh: '考试提示' },

  /* Mock exam */
  exam: { en: 'Mock exam', zh: '模拟考试' },
  examLede: {
    en: 'Test yourself like the real exam: no feedback until you finish, then a score, a breakdown by skill area, and every answer explained. {pool} questions in the pool.',
    zh: '像真正的考试一样测验自己：交卷前不显示对错，交卷后看到分数、各技能领域的成绩，以及每题的解释。题库共 {pool} 题。',
  },
  examFull: { en: 'Full mock exam', zh: '完整模拟考试' },
  examFullHint: { en: '{n} questions in the official proportions, {min}-minute timer. Pass mark 700 / 1000.', zh: '{n} 题，按官方比例出题，限时 {min} 分钟。及格线 700 / 1000。' },
  examDomain: { en: 'Practice one skill area', zh: '单项技能练习' },
  examDomainHint: { en: 'Up to {n} questions from one area, no timer.', zh: '从一个技能领域抽最多 {n} 题，不限时。' },
  examQuick: { en: 'Quick quiz', zh: '快速测验' },
  examQuickHint: { en: '{n} random questions from every area, no timer.', zh: '从所有领域随机抽 {n} 题，不限时。' },
  examPoolCount: { en: '{n} questions', zh: '{n} 题' },
  examStart: { en: 'Start', zh: '开始' },
  examBest: { en: 'Best: {n}', zh: '最高分：{n}' },
  examInProgress: { en: 'Exam in progress', zh: '考试进行中' },
  examAnsweredOf: { en: '{done} of {total} answered', zh: '已答 {done}/{total}' },
  examResume: { en: 'Resume', zh: '继续作答' },
  examAbandon: { en: 'Discard', zh: '放弃' },
  examAbandonConfirm: { en: 'Discard this attempt? Its answers will not be saved.', zh: '放弃这次作答？答案不会保存。' },
  examReplace: { en: 'An exam is in progress. Discard it and start a new one?', zh: '有一场考试正在进行。要放弃它并开始新的吗？' },
  examQuestionN: { en: 'Question {n} of {total}', zh: '第 {n} 题，共 {total} 题' },
  examFlag: { en: 'Mark for review', zh: '标记待复查' },
  examFlagged: { en: 'Marked', zh: '已标记' },
  examOverview: { en: 'All questions · {done}/{total} answered', zh: '全部题目 · 已答 {done}/{total}' },
  examSubmit: { en: 'Finish and see score', zh: '交卷看分数' },
  examPause: { en: 'Pause (answers are kept)', zh: '暂停（答案会保留）' },
  examUnanswered: { en: '{n} question(s) not answered. Finish anyway?', zh: '还有 {n} 题未作答。仍要交卷吗？' },
  examSubmitConfirm: { en: 'Finish the exam and see your score?', zh: '交卷并查看分数？' },
  examResult: { en: 'Your result', zh: '考试结果' },
  examPass: { en: 'Pass — at or above the {n} mark', zh: '及格——达到 {n} 分及格线' },
  examFail: { en: 'Below the {n} pass mark — keep practising', zh: '未达 {n} 分及格线——继续加油' },
  examTime: { en: 'time {t}', zh: '用时 {t}' },
  examByDomain: { en: 'By skill area', zh: '各技能领域' },
  examWeakest: { en: 'Weakest area: {d}.', zh: '最弱的领域：{d}。' },
  examReview: { en: 'Review the course', zh: '复习该课程' },
  examRetryWrong: { en: 'Retry wrong answers', zh: '重做错题' },
  examRetryWrongN: { en: 'Retry the {n} I got wrong', zh: '重做 {n} 道错题' },
  examNew: { en: 'New exam', zh: '新的考试' },
  examAnswers: { en: 'Answers and explanations', zh: '答案与解释' },
  examOnlyWrong: { en: 'Show only questions I got wrong', zh: '只显示答错的题目' },
  examYourAnswer: { en: 'your answer', zh: '你的答案' },
  examSkipped: { en: 'Not answered', zh: '未作答' },
  examStudyLesson: { en: 'Study this lesson', zh: '学习这一课' },
  examHistory: { en: 'Past attempts', zh: '历次成绩' },
  examClear: { en: 'Clear history', zh: '清除历史' },
  examClearConfirm: { en: 'Delete all past exam results?', zh: '删除所有历次考试成绩？' },
  examDisclaimer: {
    en: 'The app scores the share of questions you got right on a 0–1000 scale. Microsoft’s 700 is a scaled score whose formula is not published, so treat the result as a guide, not a prediction.',
    zh: '本 App 按答对比例换算成 0–1000 分。Microsoft 的 700 分是换算后的分数，其公式未公开，所以结果仅供参考，不能当作预测。',
  },
  examToolHint: { en: 'Timed full exam, practice by skill area, quick quizzes, scores and history.', zh: '限时完整考试、按技能领域练习、快速测验、分数和历史记录。' },
  examCta: { en: 'Take a mock exam', zh: '参加模拟考试' },

  /* Search and tools */
  search: { en: 'Search', zh: '搜索' },
  searchHint: { en: 'Search lessons and terms, in English or Chinese', zh: '搜索课程和名词（中英文都可以）' },
  noResults: { en: 'No results', zh: '找不到结果' },
  tools: { en: 'Tools', zh: '工具' },
  glossary: { en: 'Power BI glossary', zh: 'Power BI 术语表' },
  glossaryHint: { en: 'Every key term in the course, with a short definition in both languages.', zh: '课程中的所有关键词，附中英文简短定义。' },
  flashcards: { en: 'Flashcards', zh: '闪卡' },
  flashHint: { en: "Tap the card to see the definition. The deck is this module's key terms.", zh: '点卡片看解释。卡片是本单元的关键词。' },
  quiz: { en: 'Quick checks by module', zh: '各单元随堂小测' },
  quizHint: { en: 'Every quick-check question from the lessons, with instant feedback, by module.', zh: '课程中所有随堂小测题目，即时显示对错，按单元排列。' },
  favourites: { en: 'Favourite modules', zh: '收藏的单元' },
  favourite: { en: 'Add module to favourites', zh: '收藏这个单元' },
  unfavourite: { en: 'Remove from favourites', zh: '取消收藏' },
  bookmarks: { en: 'Bookmarks', zh: '书签' },
  highlights: { en: 'Highlights', zh: '画线' },
  notes: { en: 'Notes', zh: '笔记' },
  chapterNotes: { en: 'Module notes', zh: '各单元笔记' },
  myNotes: { en: 'My notes', zh: '我的笔记' },
  chapterNoteHint: { en: 'Notes for this module (saved automatically)', zh: '这个单元的笔记（自动保存）' },
  markHint: {
    en: 'Tap a paragraph to highlight it, add a note or bookmark it; long-press to mark just a few words. Tap ☆ to favourite the module.',
    zh: '点一下段落可以画线、写笔记或加书签；长按选取几个字，只标记那几个字。点 ☆ 收藏整个单元。',
  },
  saved: { en: 'Saved', zh: '已保存' },

  /* About, share, updates */
  info: { en: 'About', zh: '关于' },
  share: { en: 'Share', zh: '分享' },
  shareHint: { en: 'Scan to open the app in a browser', zh: '扫描二维码，用浏览器直接打开这个 App' },
  shareButton: { en: 'Share app link', zh: '分享 App 链接' },
  copyLink: { en: 'Copy link', zh: '复制链接' },
  copied: { en: 'Copied', zh: '已复制' },
  createdBy: { en: 'Apps created by Bryan Woo', zh: 'Apps created by Bryan Woo' },
  version: { en: 'Version', zh: '版本' },
  offline: { en: 'Offline', zh: '离线' },
  offlineReady: { en: 'Ready to use offline', zh: '已可离线使用' },
  offlineNotYet: { en: 'Offline download not finished yet', zh: '尚未完成离线下载' },
  contents: { en: 'Contents', zh: '目录' },
  allSources: { en: 'Official resources', zh: '官方资源' },
  updateReady: { en: 'A new version is ready', zh: '有新版本可以更新' },
  updateNow: { en: 'Update now', zh: '立即更新' },
  updateLater: { en: 'Later', zh: '稍后' },
  updatedTo: { en: 'Updated to v{v}', zh: '已更新到 v{v}' },
  allUpdates: { en: "What's new", zh: '更新记录' },
  ok: { en: 'OK', zh: '好的' },
  more: { en: 'More', zh: '更多' },
  progressTitle: { en: 'My progress', zh: '我的进度' },
  resetProgress: { en: 'Reset progress', zh: '重设进度' },
  resetConfirm: { en: 'Clear mastered modules and quick-check answers? Notes, highlights and exam history stay.', zh: '清除「已掌握」和随堂小测记录？笔记、画线和考试历史会保留。' },

  /* Bottom bar and settings */
  menu: { en: 'Menu', zh: '菜单' },
  settings: { en: 'Settings', zh: '设置' },
  language: { en: 'Language', zh: '语言' },
  theme: { en: 'Appearance', zh: '外观' },
  themeAuto: { en: 'Match system', zh: '跟随系统' },
  themeLight: { en: 'Light', zh: '浅色' },
  themeDark: { en: 'Dark', zh: '深色' },
  lightLooks: { en: 'Light theme', zh: '浅色主题' },
  darkLooks: { en: 'Dark theme', zh: '深色主题' },
  look_classic: { en: 'Classic', zh: '经典' },
  look_paper: { en: 'Paper', zh: '纸张' },
  look_mint: { en: 'Mint', zh: '薄荷' },
  look_lavender: { en: 'Lavender', zh: '薰衣草' },
  look_midnight: { en: 'Midnight', zh: '午夜' },
  look_oled: { en: 'OLED Black', zh: '纯黑 OLED' },
  look_slate: { en: 'Slate', zh: '石板' },
  look_grape: { en: 'Grape', zh: '葡萄' },
  textSize: { en: 'Text size', zh: '字号' },
  textSample: { en: 'A measure is evaluated in its filter context.', zh: '度量值在它的筛选上下文中计算。' },
  loadError: { en: 'Could not load this page', zh: '内容载入失败' },
};
