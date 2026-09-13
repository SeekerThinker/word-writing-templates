#!/usr/bin/env python3
"""Verify Word-native captions, notes, and bibliography styles in all templates."""
from pathlib import Path
import zipfile
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
Q = lambda tag: f'{{{W}}}{tag}'
FONTS = {'windows': '宋体', 'macos': 'Songti SC'}


def style_by_id(styles, style_id):
    return styles.find(f".//w:style[@w:styleId='{style_id}']", NS)


def style_by_name(styles, name):
    for style in styles.findall('.//w:style', NS):
        node = style.find('w:name', NS)
        if node is not None and node.get(Q('val')) == name:
            return style
    return None


def east_asia_font(style):
    if style is None:
        return None
    node = style.find('.//w:rPr/w:rFonts', NS)
    return node.get(Q('eastAsia')) if node is not None else None


errors = []
files = sorted((ROOT / 'templates').rglob('*.dotx'))

if len(files) != 24:
    errors.append(f'expected 24 templates, got {len(files)}')

for path in files:
    rel = path.relative_to(ROOT / 'templates')
    platform = rel.parts[0]
    expected_font = FONTS[platform]
    try:
        with zipfile.ZipFile(path) as zf:
            settings = etree.fromstring(zf.read('word/settings.xml'))
            styles = etree.fromstring(zf.read('word/styles.xml'))

            update = settings.find('w:updateFields', NS)
            if update is None or update.get(Q('val')) not in {'1', 'true', 'on'}:
                errors.append(f'{rel}: updateFields should be enabled')
            if settings.find('w:documentProtection', NS) is not None:
                errors.append(f'{rel}: document protection would interfere with citation tools')

            captions = settings.find('w:captions', NS)
            if captions is None:
                errors.append(f'{rel}: w:captions missing')
            else:
                by_name = {n.get(Q('name')): n for n in captions.findall('w:caption', NS)}
                for label in ('图', '表'):
                    if label not in by_name:
                        errors.append(f'{rel}: caption label {label} missing')
                        continue
                    node = by_name[label]
                    expected_pos = 'below' if label == '图' else 'above'
                    if node.get(Q('pos')) != expected_pos:
                        errors.append(f'{rel}: {label} position should be {expected_pos}')
                    if node.get(Q('numFmt')) != 'decimal':
                        errors.append(f'{rel}: {label} numbering should be decimal')
                    if '/books/' in path.as_posix():
                        if node.get(Q('chapNum')) not in {'1', 'true', 'on'}:
                            errors.append(f'{rel}: {label} should include chapter numbering')
                        if node.get(Q('heading')) != '1':
                            errors.append(f'{rel}: {label} should use Heading 1 as chapter source')
                        if node.get(Q('separator')) != 'hyphen':
                            errors.append(f'{rel}: {label} chapter separator should be hyphen')
                    elif node.get(Q('chapNum')) in {'1', 'true', 'on'}:
                        errors.append(f'{rel}: article {label} should use global numbering')

            caption_style = style_by_id(styles, 'Caption')
            if caption_style is None:
                errors.append(f'{rel}: Caption style missing')
            else:
                jc = caption_style.find('.//w:pPr/w:jc', NS)
                if jc is None or jc.get(Q('val')) != 'center':
                    errors.append(f'{rel}: Caption style should be centered')
                if caption_style.find('w:qFormat', NS) is None:
                    errors.append(f'{rel}: Caption style should be a quick style')

            source_style = style_by_name(styles, '图表来源')
            if source_style is None:
                errors.append(f'{rel}: 图表来源 style missing')
            else:
                jc = source_style.find('.//w:pPr/w:jc', NS)
                if jc is None or jc.get(Q('val')) != 'center':
                    errors.append(f'{rel}: 图表来源 style should be centered')

            for style_id in ('FootnoteText', 'EndnoteText'):
                style = style_by_id(styles, style_id)
                if style is None:
                    errors.append(f'{rel}: {style_id} style missing')
                    continue
                if east_asia_font(style) != expected_font:
                    errors.append(f'{rel}: {style_id} should use {expected_font}')
                sz = style.find('.//w:rPr/w:sz', NS)
                if sz is None or sz.get(Q('val')) != '18':
                    errors.append(f'{rel}: {style_id} should be 9 pt')

            for style_id in ('FootnoteReference', 'EndnoteReference'):
                style = style_by_id(styles, style_id)
                if style is None:
                    errors.append(f'{rel}: {style_id} style missing')
                    continue
                vert = style.find('.//w:rPr/w:vertAlign', NS)
                if vert is None or vert.get(Q('val')) != 'superscript':
                    errors.append(f'{rel}: {style_id} should be superscript')

            bibliography = style_by_id(styles, 'Bibliography')
            if bibliography is None:
                errors.append(f'{rel}: Bibliography style missing')
            else:
                if east_asia_font(bibliography) != expected_font:
                    errors.append(f'{rel}: Bibliography should use {expected_font}')
                ind = bibliography.find('.//w:pPr/w:ind', NS)
                if ind is None or ind.get(Q('left')) != '420' or ind.get(Q('hanging')) != '420':
                    errors.append(f'{rel}: Bibliography should have a 420-twip hanging indent')

            entry = style_by_name(styles, '参考文献条目')
            if entry is None:
                errors.append(f'{rel}: 参考文献条目 style missing')
            else:
                if east_asia_font(entry) != expected_font:
                    errors.append(f'{rel}: 参考文献条目 should use {expected_font}')
                ind = entry.find('.//w:pPr/w:ind', NS)
                if ind is None or ind.get(Q('left')) != '420' or ind.get(Q('hanging')) != '420':
                    errors.append(f'{rel}: 参考文献条目 should have a 420-twip hanging indent')
    except Exception as exc:
        errors.append(f'{rel}: {exc}')

if errors:
    print('REFERENCE CHECK FAILED')
    for error in errors:
        print('-', error)
    raise SystemExit(1)

print('OK: captions, note styles, and bibliography styles verified for 24 templates')
