#!/usr/bin/env python3
"""Cross-platform structural checks for the generated Word templates.

This script intentionally uses only Python's standard library so the same
checks can run on GitHub-hosted Windows, macOS and Linux runners. It does not
claim to launch Microsoft Word; it verifies the OOXML package, Unicode file
paths, template content type, numbering, fonts, shortcut customizations and
absence of macros.
"""
from __future__ import annotations

import platform
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WNE = "http://schemas.microsoft.com/office/word/2006/wordml"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
NS = {"w": W, "wne": WNE, "ct": CT}

EXPECTED_SHORTCUTS = ["0631", "0632", "0633", "0634", "0642", "0651", "0646", "065A"]
EXPECTED_FONTS = {
    "windows": {"宋体", "黑体", "楷体", "微软雅黑"},
    "macos": {"Songti SC", "PingFang SC", "Kaiti SC"},
}
REQUIRED_PARTS = {
    "[Content_Types].xml",
    "word/document.xml",
    "word/styles.xml",
    "word/numbering.xml",
    "word/customizations.xml",
    "word/_rels/document.xml.rels",
}
FORBIDDEN_MACRO_PARTS = {"word/vbaProject.bin", "word/vbaData.xml"}


def attr(ns: str, name: str) -> str:
    return f"{{{ns}}}{name}"


def check_one(path: Path, errors: list[str]) -> None:
    rel = path.relative_to(TEMPLATES)
    platform_name = rel.parts[0]
    try:
        with zipfile.ZipFile(path) as zf:
            bad = zf.testzip()
            if bad:
                errors.append(f"{rel}: corrupt member {bad}")
                return
            names = set(zf.namelist())
            missing = REQUIRED_PARTS - names
            if missing:
                errors.append(f"{rel}: missing {sorted(missing)}")
            forbidden = FORBIDDEN_MACRO_PARTS & names
            if forbidden:
                errors.append(f"{rel}: unexpected macro parts {sorted(forbidden)}")

            content_types = ET.fromstring(zf.read("[Content_Types].xml"))
            template_types = [
                node.get("ContentType")
                for node in content_types.findall("ct:Override", NS)
                if node.get("PartName") == "/word/document.xml"
            ]
            wanted_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml"
            if template_types != [wanted_type]:
                errors.append(f"{rel}: not a macro-free .dotx template: {template_types}")

            shortcuts = ET.fromstring(zf.read("word/customizations.xml"))
            codes = [n.get(attr(WNE, "kcmPrimary")) for n in shortcuts.findall(".//wne:keymap", NS)]
            if codes[:8] != EXPECTED_SHORTCUTS or len(codes) < 8:
                errors.append(f"{rel}: shortcut map differs: {codes}")

            numbering = ET.fromstring(zf.read("word/numbering.xml"))
            levels = numbering.findall("w:abstractNum/w:lvl", NS)
            if len(levels) != 4:
                errors.append(f"{rel}: expected 4 numbering levels, got {len(levels)}")

            styles = ET.fromstring(zf.read("word/styles.xml"))
            fonts: set[str] = set()
            for rfonts in styles.findall(".//w:rFonts", NS):
                for key in ("eastAsia", "ascii", "hAnsi", "cs"):
                    value = rfonts.get(attr(W, key))
                    if value:
                        fonts.add(value)
            expected = EXPECTED_FONTS.get(platform_name, set())
            if not expected.issubset(fonts):
                errors.append(f"{rel}: expected platform fonts {sorted(expected)}; found {sorted(fonts)}")

            document = ET.fromstring(zf.read("word/document.xml"))
            text = "".join((node.text or "") for node in document.findall(".//w:t", NS))
            if "在这里输入" not in text:
                errors.append(f"{rel}: missing beginner-facing placeholder text")
    except Exception as exc:
        errors.append(f"{rel}: {exc}")


def main() -> int:
    files = sorted(TEMPLATES.glob("*/*/*.dotx"))
    errors: list[str] = []
    if len(files) != 12:
        errors.append(f"expected 12 templates, got {len(files)}")
    for path in files:
        check_one(path, errors)

    host = f"{platform.system()} {platform.release()} / Python {platform.python_version()}"
    if errors:
        print(f"COMPATIBILITY CHECK FAILED on {host}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK: {len(files)} templates passed structural checks on {host}")
    print("Scope: OOXML/package compatibility only; Microsoft Word itself is not launched by this test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
