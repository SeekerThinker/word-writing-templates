# Structured Thinking & Writing with Word

**Give your ideas levels. Keep the structure open to change. Let your thinking grow.**

This project turns Word into an aid for thinking and writing. Real heading levels let you name, group, and relate ideas, questions, notes, and source material; Word's Navigation Pane keeps the whole in view as you work on the details. A template cannot think for you, but it can make the shape of your thinking easier to see, examine, and rearrange.

**Organizing and accumulating notes are complete uses in their own right.** A paper, report, or book may follow, but is not a required destination. The project's priorities are **thinking → structure → recording / writing → layout**.

[中文 README](README.md) · [Website](https://seekerthinker.github.io/word-writing-templates/en/) · [Usage guide](https://seekerthinker.github.io/word-writing-templates/en/guide.html)

## Two ways to begin

**[Start writing online →](https://seekerthinker.github.io/word-writing-templates/en/editor.html)**

The browser editor keeps a heading tree alongside an editable, continuously scrolling full document. Rename headings, change levels, split or merge sections, and move a section together with its descendants. Switch to a read-only page preview or focus on one section when useful. The body supports lightweight bold, italic, quotes and lists, plus real tables and footnotes. Choose the document language, numbering preset, and intended Windows/macOS Word platform; export a `.docx` with real Heading 1–4, tables, and footnotes, then continue in desktop Word.

Drafts are saved **locally in this browser** by default and are not uploaded to the project server. This is not a cloud-sync service: regularly download a **Backup JSON** file for restoration, or export a `.docx` as a document, especially before clearing browser data, changing devices, or using private browsing. **Import backup** restores JSON; Word opens the exported `.docx`. The browser editor does **not** yet import arbitrary Word documents for lossless round trips. Page preview approximates paper layout; Word determines final page breaks. See the [online editor guide](docs/online-editor.md).

**[Download a Word template →](https://seekerthinker.github.io/word-writing-templates/en/#chooser)**

Alternatively, download the `.dotx` for your Windows or macOS setup and double-click it. Word creates a new document, leaving the original template unchanged. Use Heading 1–4 and the Navigation Pane to record, inspect, and rearrange your work. Optional table-of-contents, page numbers, captions, footnotes, and reference styles are ready when needed. No VBA macros or extra plugin are required.

[Windows package](https://github.com/SeekerThinker/word-writing-templates/releases/latest/download/Word-Writing-Templates-Windows.zip) · [macOS package](https://github.com/SeekerThinker/word-writing-templates/releases/latest/download/Word-Writing-Templates-macOS.zip)

## Template matrix and numbering

Version 4 keeps **one user template per numbering preset**: 6 presets × Windows/macOS = **12 `.dotx` files**. Interface language, document language, and numbering are separate choices. “Chinese traditional chapter numbering” describes a numbering convention, **not a Traditional Chinese character setting**.

| Type | Numbering | Example | Windows | macOS |
|---|---|---|---|---|
| Book | Chinese traditional chapter numbering | `第一章 → 第一节 → 一、 → （一）` | [Template](templates/windows/books/书籍-中文传统.dotx?raw=1) | [Template](templates/macos/books/书籍-中文传统.dotx?raw=1) |
| Book | Chapter + decimal | `Chapter 1 → 1.1 → 1.1.1 → 1.1.1.1` | [Template](templates/windows/books/书籍-章节数字.dotx?raw=1) | [Template](templates/macos/books/书籍-章节数字.dotx?raw=1) |
| Book | Pure decimal | `1 → 1.1 → 1.1.1 → 1.1.1.1` | [Template](templates/windows/books/书籍-纯数字.dotx?raw=1) | [Template](templates/macos/books/书籍-纯数字.dotx?raw=1) |
| Article | Chinese academic numbering | `一、 → （一） → 1. → （1）` | [Template](templates/windows/articles/文章-中文论文.dotx?raw=1) | [Template](templates/macos/articles/文章-中文论文.dotx?raw=1) |
| Article | Decimal hierarchy | `1 → 1.1 → 1.1.1 → 1.1.1.1` | [Template](templates/windows/articles/文章-数字层级.dotx?raw=1) | [Template](templates/macos/articles/文章-数字层级.dotx?raw=1) |
| Article | Compact Chinese numbering | `一、 → 1. → （1） → ①` | [Template](templates/windows/articles/文章-中文简洁.dotx?raw=1) | [Template](templates/macos/articles/文章-中文简洁.dotx?raw=1) |

For everyday notes and research material, the article presets are often a lighter start; books and extended work may call for the book presets. You need not decide on a final form before you begin.

## Move between the part and the whole

Heading levels help answer: What is this section about? What larger theme does it belong to? Which parts are peers or children? What's missing or repeated? Does the order make sense?

Write a little, give the material a name and a place, inspect the outline, move something, and return to the body. A complete outline is not a prerequisite, and formal publication is not the assumed goal. The [structured-thinking method](docs/结构化思考.md) and [Word template quick start](docs/快速开始.md) are currently in Chinese.

## Shared style shortcuts in the browser and Word

The browser editor and exported Word templates share shortcuts for headings, body text, quotes, tables, and footnotes. Browser-only section commands and export shortcuts are listed in the editor's shortcut panel.

| Action | Windows | macOS |
|---|---|---|
| Heading 1 / 2 / 3 / 4 | `Ctrl + Alt + 1 / 2 / 3 / 4` | `⌘ + ⌥ + 1 / 2 / 3 / 4` |
| Body text | `Ctrl + Alt + Z` | `⌘ + ⌥ + Z` |
| Table / table text | `Ctrl + Alt + B` | `⌘ + ⌥ + B` |
| Quote / special paragraph | `Ctrl + Alt + Q` | `⌘ + ⌥ + Q` |
| Insert footnote | `Ctrl + Alt + F` | `⌘ + ⌥ + F` |

## Compatibility and maintenance

Automation checks the 12 public templates' OOXML, numbering, styles, sections, and optional publication features, and checks exported Word packages for real tables, footnotes, and shortcut customizations. PDF layout smoke tests and OOXML checks **are not the same as testing every operation in Microsoft Word itself**. See [compatibility and testing](docs/兼容性与测试.md) (currently Chinese).

The [stability policy](STABILITY.md) protects filenames, the 12-template matrix, download URLs, and macro-free operation. See [maintainer notes](MAINTAINERS.md), [contribution instructions](CONTRIBUTING.md), and the [AI collaboration guide](AGENTS.md). The project is licensed under [MIT](LICENSE).

**Let heading levels carry your thinking and keep the whole visible. Your work can remain a collection of notes—or grow along the same structure into something more.**
