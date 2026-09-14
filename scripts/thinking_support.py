#!/usr/bin/env python3
"""Add compact thinking-first cues to generated Word templates.

The direct-start templates must stay visually minimal: title, one level-1 heading,
and one body paragraph. This post-processing step changes only the existing body
placeholder so first-time users discover the intended loop: write, split with
Heading 2 when needed, then use Word's Navigation Pane to inspect structure.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
DC = "http://purl.org/dc/elements/1.1/"
NS = {"w": W, "dc": DC}
Q = lambda ns, tag: f"{{{ns}}}{tag}"

DIRECT_OLD = "从这里开始写作。"
DIRECT_NEW = "从这里开始写。需要拆分时用“标题 2”；写一会儿后打开“导航窗格”，只看标题检查结构。"
BOOK_OLD = "从这里开始写正文。以后每个“标题 1”都会自动另起新页。"
BOOK_NEW = "从这里开始写正文。需要拆分时用“标题 2”；写一会儿后打开“导航窗格”检查整体结构。以后每个“标题 1”都会自动另起新页。"
ARTICLE_OLD = "从这里开始写正文。"
ARTICLE_NEW = "从这里开始写正文。需要拆分时用“标题 2”；写一会儿后打开“导航窗格”检查整体结构。"
SUBJECT = "Word 结构化思考与写作模板"


def paragraph_text(paragraph) -> str:
    return "".join((node.text or "") for node in paragraph.findall(".//w:t", NS))


def replace_paragraph_text(document, old: str, new: str) -> bool:
    """Replace one exact paragraph while preserving its paragraph style."""
    for paragraph in document.findall(".//w:body/w:p", NS):
        if paragraph_text(paragraph) != old:
            continue
        texts = paragraph.findall(".//w:t", NS)
        if not texts:
            continue
        texts[0].text = new
        for extra in texts[1:]:
            extra.text = ""
        return True
    return False


def expected_cue(path: Path) -> tuple[str, str]:
    rel = path.relative_to(TEMPLATES).as_posix()
    if "/structured/books/" in f"/{rel}":
        return BOOK_OLD, BOOK_NEW
    if "/structured/articles/" in f"/{rel}":
        return ARTICLE_OLD, ARTICLE_NEW
    return DIRECT_OLD, DIRECT_NEW


def patch_one(path: Path) -> None:
    with zipfile.ZipFile(path, "r") as zin:
        files = {name: zin.read(name) for name in zin.namelist()}

    document = etree.fromstring(files["word/document.xml"])
    old, new = expected_cue(path)
    current_text = "".join((node.text or "") for node in document.findall(".//w:t", NS))
    if new not in current_text:
        if not replace_paragraph_text(document, old, new):
            raise RuntimeError(f"{path.relative_to(ROOT)}: could not find expected starter paragraph")
        files["word/document.xml"] = etree.tostring(
            document, xml_declaration=True, encoding="UTF-8", standalone=True
        )

    core = etree.fromstring(files["docProps/core.xml"])
    subject = core.find("dc:subject", NS)
    if subject is None:
        subject = etree.SubElement(core, Q(DC, "subject"))
    subject.text = SUBJECT
    files["docProps/core.xml"] = etree.tostring(
        core, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)


def main() -> None:
    templates = sorted(TEMPLATES.rglob("*.dotx"))
    if len(templates) != 24:
        raise SystemExit(f"expected 24 templates before thinking-support patch, got {len(templates)}")

    for path in templates:
        patch_one(path)

    print("OK: added thinking-first starter cues to 24 templates without adding new paragraphs")


if __name__ == "__main__":
    main()
