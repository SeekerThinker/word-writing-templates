#!/usr/bin/env python3
"""Make generated templates thinking-first and promote one public template per scheme.

The v3 generator still creates both historical start variants internally. v4 keeps
that mature generator path for now, but promotes the complete manuscript starter
to the short public filename. Users therefore see one template per numbering
scheme rather than choosing between "直接开始" and "带常用结构".

The public starter cue is deliberately open-ended: users may organize notes and
materials indefinitely, or continue into formal writing when useful. Optional
manuscript labels use outline level 9, so Word's Navigation Pane stays focused
on Heading 1–4: the user's actual thinking structure.
"""
from __future__ import annotations

import shutil
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
DIRECT_NEW = "从这里开始记录或展开内容。需要拆分时用“标题 2”；积累一些内容后打开“导航窗格”，只看标题检查整体结构。"
BOOK_OLD = "从这里开始写正文。以后每个“标题 1”都会自动另起新页。"
BOOK_NEW = "从这里开始记录或展开内容。需要拆分时用“标题 2”；积累一些内容后打开“导航窗格”看看整体结构。以后每个“标题 1”都会自动另起新页。"
ARTICLE_OLD = "从这里开始写正文。"
ARTICLE_NEW = "从这里开始记录或展开内容。需要拆分时用“标题 2”；积累一些内容后打开“导航窗格”看看整体结构。"
SUBJECT = "Word 结构化思考与写作模板"
BOOKS = ["书籍-中文传统", "书籍-章节数字", "书籍-纯数字"]
ARTICLES = ["文章-中文论文", "文章-数字层级", "文章-中文简洁"]
PLATFORMS = ["windows", "macos"]


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


def style_by_name(styles, name: str):
    for style in styles.findall("w:style", NS):
        node = style.find("w:name", NS)
        if node is not None and node.get(Q(W, "val")) == name:
            return style
    return None


def keep_optional_blocks_out_of_navigation(styles) -> None:
    structure = style_by_name(styles, "结构标题")
    if structure is None:
        raise RuntimeError("missing 结构标题 style")
    ppr = structure.find("w:pPr", NS)
    if ppr is None:
        ppr = etree.SubElement(structure, Q(W, "pPr"))
    outline = ppr.find("w:outlineLvl", NS)
    if outline is None:
        outline = etree.SubElement(ppr, Q(W, "outlineLvl"))
    outline.set(Q(W, "val"), "9")


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

    styles = etree.fromstring(files["word/styles.xml"])
    keep_optional_blocks_out_of_navigation(styles)
    files["word/styles.xml"] = etree.tostring(
        styles, xml_declaration=True, encoding="UTF-8", standalone=True
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


def promote_complete_templates() -> None:
    """Copy historical complete starters onto the stable short public paths."""
    for platform in PLATFORMS:
        for kind, stems in (("books", BOOKS), ("articles", ARTICLES)):
            for stem in stems:
                source = TEMPLATES / platform / "structured" / kind / f"{stem}-常用结构.dotx"
                target = TEMPLATES / platform / kind / f"{stem}.dotx"
                if not source.exists():
                    raise RuntimeError(f"missing complete template: {source.relative_to(ROOT)}")
                shutil.copy2(source, target)


def main() -> None:
    templates = sorted(TEMPLATES.rglob("*.dotx"))
    if len(templates) != 24:
        raise SystemExit(f"expected 24 internal build artifacts before v4 promotion, got {len(templates)}")

    for path in templates:
        patch_one(path)

    promote_complete_templates()

    public = [
        path for path in TEMPLATES.rglob("*.dotx")
        if "structured" not in path.relative_to(TEMPLATES).parts
    ]
    if len(public) != 12:
        raise SystemExit(f"expected 12 public unified templates, got {len(public)}")

    print("OK: 12 public templates now use the complete optional manuscript structure")
    print("OK: starter cues support notes or formal writing; Heading 1–4 remain the thinking tree")


if __name__ == "__main__":
    main()
