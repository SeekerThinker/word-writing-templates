# Contributing

Thank you for helping improve this project. It offers both Word templates and a browser editor that exports to Word. Protect the workflow **thinking → structure → recording / writing → layout**: ordinary users should need no setup, while maintainers handle the complexity.

[中文贡献说明](CONTRIBUTING.md) · [Website](https://seekerthinker.github.io/word-writing-templates/en/) · [Stability policy](STABILITY.md)

## Useful contributions

Documentation and translation fixes, compatibility reports from different Windows/macOS Word versions, improvements to headings and whole-document navigation, real table/footnote export fixes, and privacy-conscious automated checks are welcome. Do not assume that every set of notes must become a finished manuscript or add installation steps merely to introduce a feature.

## Before editing

Read `README.md`, `STABILITY.md`, and `MAINTAINERS.md`; for browser changes also read `docs/online-editor.md`. AI-assisted contributors should read `AGENTS.md`. **Create a working branch from fresh `main` before writing anything.** Never place a temporary file on `main` or probe branch existence by writing. Open a PR and inspect the diff for unexpected templates, release files, or private drafts. Do not commit private writing or payment credentials.

The v4 **public product matrix is 6 numbering presets × 2 platforms = 12 `.dotx` files**. The generator may still produce historic v3 compatibility copies internally; these are not 24 user templates. Each release package contains only six public templates for its platform. Public filenames, paths, stable download links, and the no-macro experience are protected by `STABILITY.md`.

## Tests and pull requests

For template or OOXML changes, install dependencies and run relevant checks:

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_templates.py
python scripts/thinking_support.py
python scripts/reference_support.py
python scripts/verify_templates.py
python scripts/compatibility_check.py
python scripts/thinking_check.py
python scripts/manuscript_check.py
python scripts/reference_check.py
python scripts/stability_check.py
python scripts/web_editor_export_check.py
```

For browser editor and bilingual site changes, at minimum run:

```bash
node --check site/editor.js
node --check site/editor-copy.js
node --check site/i18n.js
node --check site/app.js
node --check site/en/app.js
node scripts/editor_copy_check.cjs
python scripts/web_editor_export_check.py
```

The main build also runs PDF layout smoke checks, release package audits, and checks on Windows/macOS/Linux. **OOXML and PDF automation are not a substitute for hands-on Microsoft Word testing.** If you test a particular Word version, record the OS, version, template or exported document, reproduction steps, and actual observations; do not upload private manuscripts.

Changes to whole-document navigation, view switching, typing, local storage, tables, footnotes, or downloads also need a real browser interaction check. JavaScript syntax checks and static HTML assertions alone cannot establish that the UI works. Explicitly state when browser or real Word testing was not performed.

For backup schema changes, verify migration from the older v2 `body` field to v3 text blocks, JSON import/export, and preservation of tables/footnotes. Existing drafts must not be silently overwritten. `.docx` is for continuing in Word, **not** a browser-project backup that can be imported back into this editor; use JSON for recovery.

Public homepages, editors, and usage guides exist in Chinese and English. Changes to functionality, privacy claims, warnings, shortcuts, or steps must update both languages in the same PR, following the [bilingual maintenance guide](docs/bilingual-maintenance.md). Chinese product principles and terminology are the semantic baseline; English should read naturally and remain equivalent. Technical files can stay single-copy. Existing historical Chinese-only maintainer documents are not claimed to have full English mirrors yet.

In the PR description, explain the change, compatibility with existing templates/drafts, which tests ran, and which tests (especially real browser or Word) did not. Do not edit generated `templates/` manually in place of its generator; do not add VBA macros, installers, payment gates, or unrelated dependencies.
