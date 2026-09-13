#!/usr/bin/env python3
from pathlib import Path
import shutil, zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / 'version.txt').read_text(encoding='utf-8').strip()
BOOKS = ['书籍-中文传统.dotx', '书籍-章节数字.dotx', '书籍-纯数字.dotx']
ARTICLES = ['文章-中文论文.dotx', '文章-数字层级.dotx', '文章-中文简洁.dotx']

def build(platform):
    label = 'Windows' if platform == 'windows' else 'macOS'
    folder = f'Word结构化写作模板-{label}-v{VERSION}'
    stage = ROOT / 'build' / folder
    if stage.exists():
        shutil.rmtree(stage)
    (stage / '书籍模板').mkdir(parents=True)
    (stage / '文章模板').mkdir(parents=True)
    for name in BOOKS:
        shutil.copy2(ROOT / 'templates' / platform / 'books' / name, stage / '书籍模板' / name)
    for name in ARTICLES:
        shutil.copy2(ROOT / 'templates' / platform / 'articles' / name, stage / '文章模板' / name)
    shutil.copy2(ROOT / 'docs' / f'开始使用-{platform}.pdf', stage / '00-开始使用.pdf')
    shortcut = 'Ctrl + Alt' if platform == 'windows' else 'Command + Option'
    (stage / '先看这里.txt').write_text(
        'Word 结构化写作模板集\n\n'
        '最简单的用法：\n'
        '1. 进入“书籍模板”或“文章模板”。\n'
        '2. 双击一个 .dotx 文件。\n'
        '3. Word 会新建文档，直接改掉占位文字并开始写作。\n\n'
        f'本平台标题快捷键前缀：{shortcut}\n'
        '详细说明见 00-开始使用.pdf。\n', encoding='utf-8')
    out = ROOT / 'release' / f'{folder}.zip'
    out.parent.mkdir(exist_ok=True)
    entries = [stage / '00-开始使用.pdf', stage / '先看这里.txt']
    entries += [stage / '书籍模板' / n for n in BOOKS]
    entries += [stage / '文章模板' / n for n in ARTICLES]
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as archive:
        for p in entries:
            archive.write(p, p.relative_to(stage.parent))
    print(out)

for platform in ('windows', 'macos'):
    build(platform)
