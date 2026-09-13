#!/usr/bin/env python3
"""Generate visual README previews from the built Word templates.

The preview is based on the actual generated .dotx file: a temporary copy is
filled with four heading levels, rendered headlessly by LibreOffice, and then
cropped into a compact PNG for GitHub README display.
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

import fitz  # PyMuPDF
from lxml import etree
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "previews"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
Q = lambda tag: f"{{{W}}}{tag}"

PREVIEWS = [
    ("book-cn-traditional", "templates/windows/books/书籍-中文传统.dotx", "书籍｜中文传统", "第一章 → 第一节 → 一、 → （一）", "适合中文专著、教材、长篇作品"),
    ("book-chapter-decimal", "templates/windows/books/书籍-章节数字.dotx", "书籍｜章节数字", "第1章 → 1.1 → 1.1.1 → 1.1.1.1", "适合技术书、教程、研究专著"),
    ("book-pure-decimal", "templates/windows/books/书籍-纯数字.dotx", "书籍｜纯数字", "1 → 1.1 → 1.1.1 → 1.1.1.1", "适合现代简洁型长文、电子书"),
    ("article-cn-academic", "templates/windows/articles/文章-中文论文.dotx", "文章｜中文论文", "一、 → （一） → 1. → （1）", "适合中文论文、报告、正式文章"),
    ("article-decimal", "templates/windows/articles/文章-数字层级.dotx", "文章｜数字层级", "1 → 1.1 → 1.1.1 → 1.1.1.1", "适合学术、研究、技术文章"),
    ("article-cn-compact", "templates/windows/articles/文章-中文简洁.dotx", "文章｜中文简洁", "一、 → 1. → （1） → ①", "适合长文章、随笔、内容写作"),
]


def paragraph(style_id: str, text: str) -> etree._Element:
    p = etree.Element(Q("p"))
    ppr = etree.SubElement(p, Q("pPr"))
    ps = etree.SubElement(ppr, Q("pStyle"))
    ps.set(Q("val"), style_id)
    r = etree.SubElement(p, Q("r"))
    t = etree.SubElement(r, Q("t"))
    t.text = text
    return p


def make_sample(src: Path, dst: Path, title: str, description: str) -> None:
    with zipfile.ZipFile(src, "r") as zin:
        files = {name: zin.read(name) for name in zin.namelist()}

    root = etree.fromstring(files["word/document.xml"])
    body = root.find("w:body", NS)
    assert body is not None
    sect = body.find("w:sectPr", NS)
    assert sect is not None

    for child in list(body):
        if child is not sect:
            body.remove(child)

    sample = [
        paragraph("af4", title),
        paragraph("1", "一级标题示例"),
        paragraph("21", "二级标题示例"),
        paragraph("31", "三级标题示例"),
        paragraph("41", "四级标题示例"),
        paragraph("a2", "这是正文示例。标题会自动编号，正文保持清晰统一的排版。"),
        paragraph("a2", description + "。"),
    ]
    insert_at = list(body).index(sect)
    for p in sample:
        body.insert(insert_at, p)
        insert_at += 1

    files["word/document.xml"] = etree.tostring(
        root, xml_declaration=True, encoding="UTF-8", standalone="yes"
    )
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)


def cjk_font(bold: bool = False) -> str:
    family = "Noto Sans CJK SC"
    try:
        result = subprocess.run(
            ["fc-match", "-f", "%{file}", family],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if result and Path(result).exists():
            return result
    except Exception:
        pass
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            return path
    raise RuntimeError("A CJK font is required. Install fonts-noto-cjk.")


def render_pdf(doc: Path, out_dir: Path) -> Path:
    office = shutil.which("libreoffice") or shutil.which("soffice")
    if not office:
        raise RuntimeError("LibreOffice is required to generate preview images.")
    subprocess.run(
        [office, "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(doc)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    pdf = out_dir / f"{doc.stem}.pdf"
    if not pdf.exists():
        raise RuntimeError(f"LibreOffice did not produce {pdf}")
    return pdf


def compose(pdf: Path, output: Path, title: str, numbering: str) -> None:
    doc = fitz.open(pdf)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(1.55, 1.55), alpha=False)
    raw = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

    crop = raw.crop((60, 35, raw.width - 60, min(raw.height, 680)))
    crop.thumbnail((980, 560), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (1100, 760), "white")
    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.truetype(cjk_font(True), 40)
    sub_font = ImageFont.truetype(cjk_font(False), 24)
    draw.text((60, 38), title, font=title_font, fill=(25, 25, 25))
    draw.text((60, 93), numbering, font=sub_font, fill=(90, 90, 90))

    x = (canvas.width - crop.width) // 2
    y = 150
    draw.rounded_rectangle(
        (x - 12, y - 12, x + crop.width + 12, y + crop.height + 12),
        radius=12,
        fill=(247, 247, 247),
        outline=(220, 220, 220),
        width=2,
    )
    canvas.paste(crop, (x, y))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="word-template-previews-") as tmp:
        tmp_path = Path(tmp)
        for slug, rel, title, numbering, description in PREVIEWS:
            src = ROOT / rel
            if not src.exists():
                raise FileNotFoundError(src)
            sample = tmp_path / f"{slug}.dotx"
            make_sample(src, sample, title, description)
            pdf = render_pdf(sample, tmp_path)
            compose(pdf, OUT / f"{slug}.png", title, numbering)
            print(f"generated: {OUT / f'{slug}.png'}")


if __name__ == "__main__":
    main()
