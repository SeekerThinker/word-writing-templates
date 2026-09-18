# Online editor: keep the whole document in view

[中文](在线编辑器.md) · [Open the English editor](https://seekerthinker.github.io/word-writing-templates/en/editor.html) · [Project overview](../README.en.md)

The online editor is an alternative starting point, not a complete Word replacement. Organize and write in a browser, export a real `.docx`, and continue in desktop Word with heading levels, the Navigation Pane, tables, and footnotes. Or download a `.dotx` and work entirely in Word from the start.

## Move between the part and the whole

The heading tree stays on the left while the entire document is editable on the right. Select a heading to jump to its text; browsing the document also updates the active heading in the outline. Add and rename headings, change H1–H4 levels, move or drag a whole section, split, or merge it. Descendant headings and text move with their section.

**Full document** is a continuous editable view; **Focus** shows the selected section and its descendants; **Page preview** is read-only and gives an approximate paper-like view. Browser page breaks, font metrics, and printing cannot be guaranteed to match a particular Word version exactly.

## Write first, decide on presentation later

Choose the **document language** (中文 / English), the intended **Word platform** (Windows / macOS), and the **numbering preset** independently of the interface language. Chinese traditional and Chinese academic refer to numbering conventions, not Simplified/Traditional character conversion. You can turn heading numbering off without losing real Heading levels.

The body supports lightweight bold, italic, quotes, bullets, and numbered lists, plus **real tables and footnotes**. A table is a separate block with editable cells and add/remove row/column commands. A footnote has a reference position in the body and its own content and numbering. They export as native Word tables and footnotes, not screenshots or simulated end-of-document lists.

Heading 1–4, body, quote, table, and footnote shortcuts are shared by the browser and Word template for Windows/macOS. Browser-only section commands and export shortcuts appear in the editor's expandable shortcut panel.

## Local storage, backups, and recovery

The current draft is automatically saved **in this browser** (IndexedDB when available, with a localStorage fallback) and is not uploaded to the project server for saving. Local storage is not cross-device sync, and browser data can be removed.

Download a **Backup JSON** after important edits, especially before clearing site data, changing devices or browsers, or entering private browsing. Use **Import backup** to restore that JSON. Starting a new document or importing a backup may replace the current draft, so download a backup first. **Export Word** downloads a `.docx` for further work in Word.

The draft schema is currently **v3**: section content consists of text and table blocks, with footnotes stored separately. The editor attempts to migrate older v2 drafts that stored only a `body` string into text blocks; arbitrary JSON formats are not supported. Keep the original backup and download a new one after migrating.

## What a Word export retains

The browser retrieves the selected `.dotx` from the project's own site, uses its Word styles, numbering, page settings, and OOXML parts as the skeleton, then exports `.docx`. Headings are real Heading 1–4; tables and footnotes are native Word objects. In Word, you can continue editing headings, use the Navigation Pane, update a table of contents, and finish layout.

This is a **browser → Word** workflow. Importing arbitrary `.docx` files and repeated lossless Word/browser round trips are not currently supported. Word-specific features such as complex fields, tracked changes, and reference-manager fields belong in Word. Automated OOXML validation of all 12 templates does not replace hands-on testing in every Microsoft Word version.

## Privacy and dependencies

No account is required and draft contents remain local by default. Word export needs the project-hosted template packages and a JSZip script resource with integrity verification; first load or export may need a network connection. Local drafts do **not** mean the whole website is fully offline. Do not rely on browser storage as the only copy of important work.

The maintenance principle remains **zero setup for ordinary users; complexity stays with maintainers**. Report issues via [GitHub Issues](https://github.com/SeekerThinker/word-writing-templates/issues) using reproduction steps; you do not need to upload private writing.
