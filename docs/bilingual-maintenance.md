# Bilingual maintenance guide

[中文](双语维护.md) · [Project overview](../README.en.md)

## Scope and semantic baseline

The **public user experience** is maintained in Chinese and English: `site/index.html` ↔ `site/en/index.html` for the homepage; `site/editor.html` ↔ `site/en/editor.html` for the browser editor; `site/guide.html` ↔ `site/en/guide.html` for the Word usage guide; `docs/在线编辑器.md` ↔ `docs/online-editor.md` for the editor guide; and `README.md` ↔ `README.en.md` for the project overview.

Chinese product purpose and explicitly adopted user decisions are the **semantic baseline**. English need not be word-for-word, but must not add or omit functionality, steps, limitations, warnings, or material link meaning. When translation reveals a conceptual problem, correct the Chinese baseline and decision record before synchronizing English. Interface language, document language, and numbering presets are independent. “Chinese traditional chapter numbering” names a **numbering convention**, not Traditional Chinese characters; do not shorten it to an ambiguous “Traditional Chinese.”

## Synchronize within the same PR

A change to public behavior, steps, shortcuts, privacy/local-save statements, compatibility caveats, exported formats, tables, or footnotes must inspect and update both language versions in the same PR. Translating only HTML headings is insufficient: chooser messages and JavaScript-rendered content matter too. `site/editor.js`, `site/editor-copy.js`, `site/i18n.js`, and both localized `app.js` files can contain user-facing text.

Before merging, check that corresponding pages and links work in each language; switching languages preserves the appropriate page; initial browser-language detection respects a manual choice; both languages say that JSON backs up the browser project while `.docx` continues in Word; and page preview never promises exact Word pagination. Static automation can assert critical concepts and identifiers, but **matching keywords do not prove semantic parity**. Read both versions.

## Avoid unnecessary duplication

This guide **does not claim that every historical Chinese internal document already has an English mirror**. Python/JS sources, OOXML, template binaries, JSON structures, and tests can remain single-copy. Consolidate stale internal documents gradually and prioritize English instructions essential to outside contributors. Do not clone dozens of state files merely for formal pairings that will drift.

User-facing static pages may have separate, indexable language versions; shared implementation, templates, and tests should stay single-source where practical. Both languages should read naturally without sacrificing necessary safety information for the sake of polished prose.
