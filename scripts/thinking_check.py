#!/usr/bin/env python3
"""Verify the thinking-first first-open experience in all generated templates."""
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
DIRECT_CUE = "从这里开始写。需要拆分时用“标题 2”；写一会儿后打开“导航窗格”，只看标题检查结构。"
BOOK_CUE = "从这里开始写正文。需要拆分时用“标题 2”；写一会儿后打开“导航窗格”检查整体结构。以后每个“标题 1”都会自动另起新页。"
ARTICLE_CUE = "从这里开始写正文。需要拆分时用“标题 2”；写一会儿后打开“导航窗格”检查整体结构。"


def paragraph_text(paragraph) -> str:
    return "".join((node.text or "") for node in paragraph.findall(".//w:t", NS)).strip()


def paragraph_style(paragraph) -> str | None:
    ppr = paragraph.find("w:pPr", NS)
    if ppr is None:
        return None
    style = ppr.find("w:pStyle", NS)
    return style.get(Q(W, "val")) if style is not None else None


def expected_cue(rel: str) -> str:
    if "/structured/books/" in f"/{rel}":
        return BOOK_CUE
    if "/structured/articles/" in f"/{rel}":
        return ARTICLE_CUE
    return DIRECT_CUE


def main() -> None:
    errors: list[str] = []
    files = sorted(TEMPLATES.rglob("*.dotx"))
    if len(files) != 24:
        errors.append(f"expected 24 templates, got {len(files)}")

    for path in files:
        rel = path.relative_to(TEMPLATES).as_posix()
        structured = "/structured/" in f"/{rel}"
        try:
            with zipfile.ZipFile(path) as zf:
                document = etree.fromstring(zf.read("word/document.xml"))
                body_paragraphs = [
                    p for p in document.findall(".//w:body/w:p", NS) if paragraph_text(p)
                ]
                text = "".join(paragraph_text(p) for p in body_paragraphs)
                cue = expected_cue(rel)
                if cue not in text:
                    errors.append(f"{rel}: missing thinking-first starter cue")
                if "导航窗格" not in text or "标题 2" not in text:
                    errors.append(f"{rel}: starter does not expose heading hierarchy + Navigation Pane")

                if not structured:
                    if len(body_paragraphs) != 3:
                        errors.append(
                            f"{rel}: direct-start must stay minimal with 3 non-empty paragraphs; got {len(body_paragraphs)}"
                        )
                    styles = [paragraph_style(p) for p in body_paragraphs]
                    if styles != ["Title", "Heading1", "BodyText"]:
                        errors.append(
                            f"{rel}: direct-start paragraph styles changed: {styles}"
                        )

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

    print("OK: 24 templates expose the thinking-first cue; 12 direct-start templates remain title + Heading 1 + body only")


if __name__ == "__main__":
    main()
