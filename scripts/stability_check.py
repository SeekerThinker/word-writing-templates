#!/usr/bin/env python3
"""Protect the public compatibility and positioning contract introduced in v4.0."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BOOKS = ["书籍-中文传统", "书籍-章节数字", "书籍-纯数字"]
ARTICLES = ["文章-中文论文", "文章-数字层级", "文章-中文简洁"]
PLATFORMS = ["windows", "macos"]


def expected_public_templates() -> set[str]:
    paths: set[str] = set()
    for platform in PLATFORMS:
        for stem in BOOKS:
            paths.add(f"templates/{platform}/books/{stem}.dotx")
        for stem in ARTICLES:
            paths.add(f"templates/{platform}/articles/{stem}.dotx")
    return paths


def main() -> None:
    errors: list[str] = []

    version = (ROOT / "version.txt").read_text(encoding="utf-8").strip()
    if not version.startswith("4."):
        errors.append(f"v4 stable contract expects a 4.x version, got {version!r}")

    expected = expected_public_templates()
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "templates").rglob("*.dotx")
        if "structured" not in path.relative_to(ROOT / "templates").parts
    }
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing:
            errors.append("missing stable public template paths: " + ", ".join(missing))
        if extra:
            errors.append("unexpected stable public template paths: " + ", ".join(extra))

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required_readme_fragments = [
        "releases/latest/download/Word-Writing-Templates-Windows.zip",
        "releases/latest/download/Word-Writing-Templates-macOS.zip",
        "6 种编号 × 2 个平台 = 12 个",
        "整理和积累本身就是完整用途",
        "成稿是可选延伸",
        "STABILITY.md",
    ]
    for fragment in required_readme_fragments:
        if fragment not in readme:
            errors.append(f"README is missing stable public reference: {fragment}")

    stability = ROOT / "STABILITY.md"
    if not stability.exists():
        errors.append("STABILITY.md is missing")
    else:
        text = stability.read_text(encoding="utf-8")
        if "一个编号方案只对应一个用户模板" not in text:
            errors.append("STABILITY.md is missing the v4 single-template principle")
        if "标题层级与导航窗格继续作为核心思考工作流" not in text:
            errors.append("STABILITY.md is missing the structured-thinking principle")
        if "成稿是可选延伸，不是必然终点" not in text:
            errors.append("STABILITY.md is missing the open-ended use principle")

    if errors:
        print("STABILITY CHECK FAILED")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    print("OK: v4 stable contract verified for paths, downloads and open-ended structured-thinking positioning")


if __name__ == "__main__":
    main()
