#!/usr/bin/env python3
"""Protect the public compatibility contract introduced in v3.0."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BOOKS = ["书籍-中文传统", "书籍-章节数字", "书籍-纯数字"]
ARTICLES = ["文章-中文论文", "文章-数字层级", "文章-中文简洁"]
PLATFORMS = ["windows", "macos"]


def expected_templates() -> set[str]:
    paths: set[str] = set()
    for platform in PLATFORMS:
        for stem in BOOKS:
            paths.add(f"templates/{platform}/books/{stem}.dotx")
            paths.add(f"templates/{platform}/structured/books/{stem}-常用结构.dotx")
        for stem in ARTICLES:
            paths.add(f"templates/{platform}/articles/{stem}.dotx")
            paths.add(f"templates/{platform}/structured/articles/{stem}-常用结构.dotx")
    return paths


def main() -> None:
    errors: list[str] = []

    version = (ROOT / "version.txt").read_text(encoding="utf-8").strip()
    if not version.startswith("3."):
        errors.append(f"stable contract expects a 3.x version, got {version!r}")

    expected = expected_templates()
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "templates").rglob("*.dotx")
    }
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing:
            errors.append("missing stable template paths: " + ", ".join(missing))
        if extra:
            errors.append("unexpected template paths: " + ", ".join(extra))

    forbidden = [
        ROOT / "scripts" / "build.py.b64",
    ]
    for path in forbidden:
        if path.exists():
            errors.append(f"obsolete maintenance artifact should not exist: {path.relative_to(ROOT)}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required_readme_fragments = [
        "releases/latest/download/Word-Writing-Templates-Windows.zip",
        "releases/latest/download/Word-Writing-Templates-macOS.zip",
        "STABILITY.md",
        "docs/结构化思考.md",
        "模板不会替你思考",
        "思考 → 结构 → 写作 → 排版",
    ]
    for fragment in required_readme_fragments:
        if fragment not in readme:
            errors.append(f"README is missing stable public reference: {fragment}")

    stability = ROOT / "STABILITY.md"
    if not stability.exists():
        errors.append("STABILITY.md is missing")

    thinking_doc = ROOT / "docs" / "结构化思考.md"
    if not thinking_doc.exists():
        errors.append("docs/结构化思考.md is missing")

    if errors:
        print("STABILITY CHECK FAILED")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    print("OK: v3 stable contract verified for 24 template paths, public downloads and thinking-first positioning")


if __name__ == "__main__":
    main()
