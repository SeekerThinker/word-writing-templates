// Lightweight DOM/MutationObserver regression test; no extra npm dependencies.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('site/editor-copy.js', 'utf8');

function checkLanguage(lang) {
  let active = 'viewContinuous';
  let callback;
  let writes = 0;
  let click;
  const note = {
    value: 'The editor set a short view hint.',
    get textContent() { return this.value; },
    set textContent(next) {
      if (++writes > 8) throw new Error('View copy entered an observer feedback loop');
      this.value = next;
      if (callback) callback(); // stronger than the browser's async delivery
    },
  };
  const button = { addEventListener(event, handler) { if (event === 'click') click = handler; } };
  const document = {
    documentElement: { lang },
    head: { appendChild() {} },
    title: '',
    createElement() { return { textContent: '' }; },
    querySelector(selector) {
      if (selector === '#viewNote') return note;
      if (selector === '.view-switch button[aria-pressed="true"]') return { id: active };
      return null;
    },
    querySelectorAll(selector) { return selector === '.view-switch button' ? [button] : []; },
  };
  class MutationObserver {
    constructor(fn) { callback = fn; }
    observe(target) { assert.equal(target, note); }
  }
  vm.runInNewContext(source, { document, MutationObserver, requestAnimationFrame: (fn) => fn() });
  const continuous = note.textContent;
  assert.ok(continuous.length > 30, 'continuous copy should be localized');
  assert.equal(writes, 1, 'initial view must settle after one write');
  active = 'viewPages';
  note.textContent = 'The editor switched to page preview.';
  assert.match(note.textContent, lang === 'en' ? /Pagination/ : /分页/);
  assert.equal(writes, 3, 'external update and one localized update only');
  active = 'viewFocus';
  click();
  assert.match(note.textContent, lang === 'en' ? /current section/ : /当前一节/);
  assert.equal(writes, 4, 'click should update copy once');
  active = 'viewContinuous';
  click();
  assert.equal(note.textContent, continuous, 'return to continuous view');
  assert.equal(writes, 5);
}

checkLanguage('zh-CN');
checkLanguage('en');
console.log('Bilingual editor view-copy observer regression OK');
