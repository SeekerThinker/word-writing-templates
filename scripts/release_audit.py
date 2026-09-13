#!/usr/bin/env python3
"""Audit the user-facing ZIP packages before publishing a GitHub Release."""
from __future__ import annotations

import io
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ["书籍-中文传统", "书籍-章节数字", "书籍-纯数字"]
ARTICLES = ["文章-中文论文", "文章-数字层级", "文章-中文简洁"]


def expected_members(label: str, version: str) -> set[str]:
    root = f"Word结构化写作模板-{label}-v{version}"
    members = {
        f"{root}/00-开始使用.pdf",
        f"{root}/00-先看这里.txt",
    }
    for stem in BOOKS:
        members.add(f"{root}/书籍模板/{stem}.dotx")
        members.add(f"{root}/书籍模板/带常用结构/{stem}-常用结构.dotx")
    for stem in ARTICLES:
        members.add(f"{root}/文章模板/{stem}.dotx")
        members.add(f"{root}/文章模板/带常用结构/{stem}-常用结构.dotx")
    return members


def audit_zip(path: Path, label: str, version: str) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing release package: {path.relative_to(ROOT)}"]

    expected = expected_members(label, version)
    with zipfile.ZipFile(path) as outer:
        actual = {name for name in outer.namelist() if not name.endswith("/")}
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing:
            errors.append(f"{path.name}: missing files: {', '.join(missing)}")
        if extra:
            errors.append(f"{path.name}: unexpected files: {', '.join(extra)}")

        dotx_members = sorted(name for name in actual if name.endswith(".dotx"))
        if len(dotx_members) != 12:
            errors.append(f"{path.name}: expected 12 .dotx files, got {len(dotx_members)}")

        forbidden_suffixes = (".exe", ".msi", ".pkg", ".dmg", ".dotm", ".docm")
        for name in actual:
            if name.lower().endswith(forbidden_suffixes):
                errors.append(f"{path.name}: forbidden user-facing executable/macro file: {name}")

        for name in dotx_members:
            data = outer.read(name)
            try:
                with zipfile.ZipFile(io.BytesIO(data)) as inner:
                    inner_names = set(inner.namelist())
                    if "word/vbaProject.bin" in inner_names:
                        errors.append(f"{path.name}: macro payload found in {name}")
                    required = {"[Content_Types].xml", "word/document.xml", "word/styles.xml"}
                    if not required.issubset(inner_names):
                        errors.append(f"{path.name}: malformed .dotx package: {name}")
            except zipfile.BadZipFile:
                errors.append(f"{path.name}: invalid .dotx ZIP package: {name}")

    return errors


def main() -> None:
    version = (ROOT / "version.txt").read_text(encoding="utf-8").strip()
    packages = [
        (ROOT / "release" / f"Word结构化写作模板-Windows-v{version}.zip", "Windows"),
        (ROOT / "release" / f"Word结构化写作模板-macOS-v{version}.zip", "macOS"),
    ]

    errors: list[str] = []
    for path, label in packages:
        errors.extend(audit_zip(path, label, version))

    if errors:
        print("RELEASE AUDIT FAILED")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    print(f"OK: v{version} release packages verified (2 ZIPs, 12 templates each, no macros/installers)")


if __name__ == "__main__":
    main()
