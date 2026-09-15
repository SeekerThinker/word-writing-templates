#!/usr/bin/env python3
"""Validate the web editor's Word-export assumptions against every real template.

This does not replace browser interaction tests. It verifies the package boundary the
browser exporter relies on: each .dotx has the required Open XML parts, Heading 1–4
are real numbered styles, and a template package can be converted to a .docx with
new structured content while remaining readable by python-docx.
"""
from __future__ import annotations

import hashlib
import tempfile
import zipfile
from pathlib import Path

from docx import Document
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
NS = {"w": W, "ct": CT}
Q = lambda ns, tag: f"{{{ns}}}{tag}"

TEMPLATE_MAIN = "application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml"
DOCUMENT_MAIN = "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"

EXPECTED = {
    "books": ["书籍-中文传统.dotx", "书籍-章节数字.dotx", "书籍-纯数字.dotx"],
    "articles": ["文章-中文论文.dotx", "文章-数字层级.dotx", "文章-中文简洁.dotx"],
}

REQUIRED_PARTS = {
    "[Content_Types].xml",
    "word/document.xml",
    "word/styles.xml",
    "word/numbering.xml",
    "word/settings.xml",
    "word/customizations.xml",
}


def parse(data: bytes) -> etree._Element:
    return etree.fromstring(data)


def text_paragraph(style_id: str, text: str) -> etree._Element:
    p = etree.Element(Q(W, "p"), nsmap={"w": W})
    ppr = etree.SubElement(p, Q(W, "pPr"))
    pstyle = etree.SubElement(ppr, Q(W, "pStyle"))
    pstyle.set(Q(W, "val"), style_id)
    run = etree.SubElement(p, Q(W, "r"))
    node = etree.SubElement(run, Q(W, "t"))
    node.text = text
    return p


def patch_document(data: bytes) -> bytes:
    root = parse(data)
    body = root.find("w:body", NS)
    assert body is not None, "word/document.xml has no body"
    sectpr = body.find("w:sectPr", NS)
    preserved = etree.fromstring(etree.tostring(sectpr)) if sectpr is not None else None
    for child in list(body):
        body.remove(child)
    body.append(text_paragraph("Title", "Web editor export check"))
    for level in range(1, 5):
        body.append(text_paragraph(f"Heading{level}", f"Heading level {level}"))
        body.append(text_paragraph("BodyText", f"Body text under heading {level}."))
    if preserved is not None:
        body.append(preserved)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def patch_content_types(data: bytes) -> bytes:
    root = parse(data)
    main = None
    for override in root.findall("ct:Override", NS):
        if override.get("PartName") == "/word/document.xml":
            main = override
            break
    assert main is not None, "missing /word/document.xml content type override"
    assert main.get("ContentType") == TEMPLATE_MAIN, "source package is not a .dotx template"
    main.set("ContentType", DOCUMENT_MAIN)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def assert_styles(data: bytes) -> None:
    root = parse(data)
    for level in range(1, 5):
        style_id = f"Heading{level}"
        style = root.xpath(f"w:style[@w:styleId='{style_id}']", namespaces=NS)
        assert style, f"missing {style_id} style"
        num_id = style[0].xpath("w:pPr/w:numPr/w:numId/@w:val", namespaces=NS)
        assert num_id == ["1"], f"{style_id} must use numbering numId=1, got {num_id}"


def assert_numbering(data: bytes) -> None:
    root = parse(data)
    nums = root.xpath("w:num[@w:numId='1']/w:abstractNumId/@w:val", namespaces=NS)
    assert nums, "missing heading numbering numId=1"
    abstract_id = nums[0]
    abstract = root.xpath(f"w:abstractNum[@w:abstractNumId='{abstract_id}']", namespaces=NS)
    assert abstract, f"missing abstract numbering {abstract_id}"
    styles = abstract[0].xpath("w:lvl/w:pStyle/@w:val", namespaces=NS)
    assert styles[:4] == ["Heading1", "Heading2", "Heading3", "Heading4"], (
        f"heading numbering must bind Heading1–Heading4, got {styles[:4]}"
    )


def convert_sample(source: Path, target: Path) -> str:
    with zipfile.ZipFile(source) as zin:
        customizations = zin.read("word/customizations.xml")
        custom_hash = hashlib.sha256(customizations).hexdigest()
        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                data = zin.read(info.filename)
                if info.filename == "word/document.xml":
                    data = patch_document(data)
                elif info.filename == "[Content_Types].xml":
                    data = patch_content_types(data)
                zout.writestr(info, data)
    return custom_hash


def validate_template(path: Path) -> None:
    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
        missing = REQUIRED_PARTS - names
        assert not missing, f"{path}: missing package parts: {sorted(missing)}"
        assert_styles(zf.read("word/styles.xml"))
        assert_numbering(zf.read("word/numbering.xml"))
        doc = parse(zf.read("word/document.xml"))
        assert doc.find(".//w:body/w:sectPr", NS) is not None, f"{path}: missing section properties"

    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "sample.docx"
        customization_hash = convert_sample(path, output)
        # python-docx is an independent OOXML consumer. Reopening the generated
        # package catches malformed content types, XML, relationships, and styles.
        document = Document(output)
        paragraphs = [p for p in document.paragraphs if p.text]
        expected_styles = [
            "Title",
            "Heading 1", "Body Text",
            "Heading 2", "Body Text",
            "Heading 3", "Body Text",
            "Heading 4", "Body Text",
        ]
        actual_styles = [p.style.name for p in paragraphs]
        assert actual_styles == expected_styles, f"{path}: exported styles differ: {actual_styles}"
        with zipfile.ZipFile(output) as zf:
            content_types = parse(zf.read("[Content_Types].xml"))
            main = content_types.xpath(
                "ct:Override[@PartName='/word/document.xml']/@ContentType", namespaces=NS
            )
            assert main == [DOCUMENT_MAIN], f"{path}: export did not become a .docx main part"
            after_hash = hashlib.sha256(zf.read("word/customizations.xml")).hexdigest()
            assert after_hash == customization_hash, f"{path}: export unexpectedly changed template shortcuts"


def main() -> None:
    paths: list[Path] = []
    for platform in ("windows", "macos"):
        for kind, filenames in EXPECTED.items():
            for filename in filenames:
                paths.append(TEMPLATES / platform / kind / filename)
    missing = [str(path.relative_to(ROOT)) for path in paths if not path.exists()]
    if missing:
        raise SystemExit(f"missing templates: {missing}")
    for path in paths:
        validate_template(path)
        print(f"OK {path.relative_to(ROOT)}")
    print(f"Web editor Word-export package check OK ({len(paths)} templates)")


if __name__ == "__main__":
    main()
