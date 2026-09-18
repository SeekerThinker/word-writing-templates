"""Guard essential documentation facts; this is not a translation-quality review."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "README.md": ["在线开始", "下载 Word 模板", "12", "备份 JSON", "脚注", "AGENTS.md"],
    "README.en.md": ["Start writing online", "Download a Word template", "12", "Backup JSON", "footnotes", "AGENTS.md"],
    "CONTRIBUTING.md": ["12", "scripts/editor_copy_check.cjs", "双语维护", "真实浏览器"],
    "CONTRIBUTING.en.md": ["12", "scripts/editor_copy_check.cjs", "bilingual maintenance", "real browser"],
    "STABILITY.md": ["12", "在线编辑器", "JSON", "Word"],
    "MAINTAINERS.md": ["12", "editor-copy.js", "IndexedDB", "真实浏览器"],
    "AGENTS.md": ["最新", "AI", "main", "HARC"],
    "docs/快速开始.md": ["在线开始", "Word", "备份 JSON"],
    "docs/quick-start.md": ["browser", "Word", "Backup JSON"],
    "docs/在线编辑器.md": ["v3", "v2", "IndexedDB", "JSON", "分页", "表格", "脚注"],
    "docs/online-editor.md": ["v3", "v2", "IndexedDB", "JSON", "page breaks", "tables", "footnotes"],
    "docs/双语维护.md": ["语义", "编号", "README.en.md"],
    "docs/bilingual-maintenance.md": ["semantic", "numbering", "README.en.md"],
    "docs/项目决策.md": ["已确认", "待确定", "打赏"],
}

for path, phrases in REQUIRED.items():
    file = ROOT / path
    if not file.is_file():
        raise SystemExit(f"Missing project document: {path}")
    body = file.read_text(encoding="utf-8")
    for phrase in phrases:
        if phrase not in body:
            raise SystemExit(f"Missing documented contract {phrase!r} in {path}")

# Counterpart links can be relative within docs/; require the basename rather
# than incorrectly demanding a repository-root path in every Markdown link.
for chinese, english in (
    ("README.md", "README.en.md"),
    ("CONTRIBUTING.md", "CONTRIBUTING.en.md"),
    ("docs/快速开始.md", "docs/quick-start.md"),
    ("docs/在线编辑器.md", "docs/online-editor.md"),
    ("docs/双语维护.md", "docs/bilingual-maintenance.md"),
):
    if Path(english).name not in (ROOT / chinese).read_text(encoding="utf-8"):
        raise SystemExit(f"Missing English counterpart link in {chinese}")
    if Path(chinese).name not in (ROOT / english).read_text(encoding="utf-8"):
        raise SystemExit(f"Missing Chinese counterpart link in {english}")

print("Project documentation contract OK; semantic parity still needs human review")
