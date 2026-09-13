#!/usr/bin/env python3
"""Verify v2.8 Word-native caption and reference support in all templates."""
from pathlib import Path
import zipfile
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
Q = lambda tag: f'{{{W}}}{tag}'

errors = []
files = sorted((ROOT / 'templates').rglob('*.dotx'))

if len(files) != 24:
    errors.append(f'expected 24 templates, got {len(files)}')

for path in files:
    rel = path.relative_to(ROOT / 'templates')
    try:
        with zipfile.ZipFile(path) as zf:
            settings = etree.fromstring(zf.read('word/settings.xml'))
            styles = etree.fromstring(zf.read('word/styles.xml'))

            update = settings.find('w:updateFields', NS)
            if update is None or update.get(Q('val')) not in {'1', 'true', 'on'}:
                errors.append(f'{rel}: updateFields should be enabled')

            captions = settings.find('w:captions', NS)
            if captions is None:
                errors.append(f'{rel}: w:captions missing')
                continue
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
                else:
                    if node.get(Q('chapNum')) in {'1', 'true', 'on'}:
                        errors.append(f'{rel}: article {label} should use global numbering')

            caption_style = styles.find(".//w:style[@w:styleId='Caption']", NS)
            if caption_style is None:
                errors.append(f'{rel}: Caption style missing')
            else:
                name = caption_style.find('w:name', NS)
                if name is None or name.get(Q('val')) is None:
                    errors.append(f'{rel}: Caption style name missing')
                jc = caption_style.find('.//w:pPr/w:jc', NS)
                if jc is None or jc.get(Q('val')) != 'center':
                    errors.append(f'{rel}: Caption style should be centered')
                if caption_style.find('w:qFormat', NS) is None:
                    errors.append(f'{rel}: Caption style should be a quick style')

            source_style = None
            for style in styles.findall('.//w:style', NS):
                name = style.find('w:name', NS)
                if name is not None and name.get(Q('val')) == '图表来源':
                    source_style = style
                    break
            if source_style is None:
                errors.append(f'{rel}: 图表来源 style missing')
            else:
                jc = source_style.find('.//w:pPr/w:jc', NS)
                if jc is None or jc.get(Q('val')) != 'center':
                    errors.append(f'{rel}: 图表来源 style should be centered')
    except Exception as exc:
        errors.append(f'{rel}: {exc}')

if errors:
    print('REFERENCE CHECK FAILED')
    for error in errors:
        print('-', error)
    raise SystemExit(1)

print('OK: v2.8 caption labels and reference styles verified for 24 templates')
