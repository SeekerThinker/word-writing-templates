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


def has_any(text: str, alternatives: tuple[str, ...]) -> bool:
    """Accept equivalent wording for a concept, not arbitrary exact hero copy."""
    return any(phrase in text for phrase in alternatives)


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
    for fragment in (
        "releases/latest/download/Word-Writing-Templates-Windows.zip",
        "releases/latest/download/Word-Writing-Templates-macOS.zip",
        "STABILITY.md",
    ):
        if fragment not in readme:
            errors.append(f"README is missing stable public reference: {fragment}")
    if not ("6 种编号" in readme and "12 个" in readme and "Windows" in readme and "macOS" in readme):
        errors.append("README is missing the 6-numbering × 2-platform = 12-template baseline")
    if not has_any(readme, ("整理和积累本身就是完整用途", "整理与积累本身就是完整用途")):
        errors.append("README is missing open-ended notes and accumulation positioning")
    if not has_any(readme, ("成稿是可选延伸", "文章、报告和书稿是可以继续发展的方向")):
        errors.append("README is missing optional-manuscript positioning")

    stability = ROOT / "STABILITY.md"
    if not stability.exists():
        errors.append("STABILITY.md is missing")
    else:
        text = stability.read_text(encoding="utf-8")
        if "一个编号方案只对应一个用户模板" not in text:
            errors.append("STABILITY.md is missing the v4 single-template principle")
        if not all(phrase in text for phrase in ("标题层级", "导航窗格", "思考")):
            errors.append("STABILITY.md is missing heading/Navigation Pane thinking principle")
        if not has_any(text, ("成稿是可选延伸，不是必然终点", "正式成稿是可选延伸", "正式成稿不是默认终点")):
            errors.append("STABILITY.md is missing the open-ended use principle")

    if errors:
        print("STABILITY CHECK FAILED")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    print("OK: v4 stable contract verified for paths, downloads and open-ended structured-thinking positioning")


if __name__ == "__main__":
    main()
