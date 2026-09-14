#!/usr/bin/env python3
"""Verify the v4 thinking-first single-template public experience."""
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

SUBJECT = "Word 结构化思考与写作模板"
BOOK_CUE = "从这里开始记录或展开内容。需要拆分时用“标题 2”；积累一些内容后打开“导航窗格”看看整体结构。以后每个“标题 1”都会自动另起新页。"
ARTICLE_CUE = "从这里开始记录或展开内容。需要拆分时用“标题 2”；积累一些内容后打开“导航窗格”看看整体结构。"


def paragraph_text(paragraph) -> str:
    return "".join((node.text or "") for node in paragraph.findall(".//w:t", NS)).strip()


def style_by_name(styles, name: str):
    for style in styles.findall("w:style", NS):
        node = style.find("w:name", NS)
        if node is not None and node.get(Q(W, "val")) == name:
            return style
    return None


def main() -> None:
    errors: list[str] = []
    all_files = sorted(TEMPLATES.rglob("*.dotx"))
    public_files = [
        p for p in all_files if "structured" not in p.relative_to(TEMPLATES).parts
    ]

    if len(all_files) != 24:
        errors.append(f"expected 24 internal build artifacts during v4 transition, got {len(all_files)}")
    if len(public_files) != 12:
        errors.append(f"expected 12 public unified templates, got {len(public_files)}")

    for path in public_files:
        rel = path.relative_to(TEMPLATES).as_posix()
        is_book = "/books/" in f"/{rel}"
        try:
            with zipfile.ZipFile(path) as zf:
                document = etree.fromstring(zf.read("word/document.xml"))
                styles = etree.fromstring(zf.read("word/styles.xml"))
                paragraphs = [p for p in document.findall(".//w:body/w:p", NS) if paragraph_text(p)]
                text = "".join(paragraph_text(p) for p in paragraphs)

                cue = BOOK_CUE if is_book else ARTICLE_CUE
                if cue not in text:
                    errors.append(f"{rel}: missing open-ended thinking-first starter cue")
                if "导航窗格" not in text or "标题 2" not in text:
                    errors.append(f"{rel}: does not expose heading hierarchy + Navigation Pane")
                if "从这里开始写正文" in text:
                    errors.append(f"{rel}: starter cue still assumes formal manuscript writing")

                if is_book:
                    for token in ("作者：在这里填写作者", "前言（可选）", "目录", "附录（可选）", "参考文献（可选）"):
                        if token not in text:
                            errors.append(f"{rel}: unified book template missing {token}")
                else:
                    for token in ("作者：在这里填写作者", "单位：在这里填写单位", "摘要（可选）", "关键词：", "参考文献（可选）"):
                        if token not in text:
                            errors.append(f"{rel}: unified article template missing {token}")

                structure = style_by_name(styles, "结构标题")
                outline = None if structure is None else structure.find(".//w:pPr/w:outlineLvl", NS)
                if outline is None or outline.get(Q(W, "val")) != "9":
                    errors.append(f"{rel}: optional 结构标题 must use outline level 9 to stay out of Navigation Pane")

                core = etree.fromstring(zf.read("docProps/core.xml"))
                subject = core.find("dc:subject", NS)
                if subject is None or subject.text != SUBJECT:
                    got = None if subject is None else subject.text
                    errors.append(f"{rel}: core subject {got!r} != {SUBJECT!r}")
        except Exception as exc:
            errors.append(f"{rel}: {exc}")

    if errors:
        print("THINKING EXPERIENCE CHECK FAILED")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    print("OK: 12 public templates support open-ended structured thinking with a clean Heading 1–4 tree")


if __name__ == "__main__":
    main()
