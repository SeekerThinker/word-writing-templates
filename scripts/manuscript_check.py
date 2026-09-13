#!/usr/bin/env python3
"""Verify the manuscript-oriented features in structured Word templates."""
from pathlib import Path
import zipfile
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
Q = lambda tag: f'{{{W}}}{tag}'

errors = []
files = sorted((ROOT / 'templates').rglob('*.dotx'))

for path in files:
    rel = path.relative_to(ROOT / 'templates')
    if 'structured' not in rel.parts:
        continue
    try:
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
            document = etree.fromstring(zf.read('word/document.xml'))
            styles = etree.fromstring(zf.read('word/styles.xml'))
            style_names = {
                node.get(Q('val'))
                for node in styles.findall('.//w:style/w:name', NS)
                if node.get(Q('val'))
            }
            text = ''.join((node.text or '') for node in document.findall('.//w:t', NS))
            sectprs = document.findall('.//w:sectPr', NS)

            if '/books/' in path.as_posix():
                if len(sectprs) < 3:
                    errors.append(f'{rel}: expected title/front/body sections, got {len(sectprs)}')

                pg_nodes = document.findall('.//w:sectPr/w:pgNumType', NS)
                formats = [node.get(Q('fmt')) for node in pg_nodes]
                starts = [node.get(Q('start')) for node in pg_nodes]
                if 'lowerRoman' not in formats or 'decimal' not in formats:
                    errors.append(f'{rel}: expected Roman front matter and decimal body numbering, got {formats}')
                if starts.count('1') < 2:
                    errors.append(f'{rel}: expected front/body numbering to restart at 1, got {starts}')

                header_parts = [name for name in names if name.startswith('word/header') and name.endswith('.xml')]
                footer_parts = [name for name in names if name.startswith('word/footer') and name.endswith('.xml')]
                if not header_parts:
                    errors.append(f'{rel}: running header missing')
                if len(footer_parts) < 2:
                    errors.append(f'{rel}: front/body page-number footers missing')

                fields = []
                for name in header_parts + footer_parts:
                    root = etree.fromstring(zf.read(name))
                    fields.extend((node.get(Q('instr')) or '') for node in root.findall('.//w:fldSimple', NS))
                if not any('STYLEREF' in field for field in fields):
                    errors.append(f'{rel}: running header is not linked to the Title style')
                if sum('PAGE' in field for field in fields) < 2:
                    errors.append(f'{rel}: page-number fields missing from front/body matter')
                if '作者：在这里填写作者' not in text:
                    errors.append(f'{rel}: title-page author placeholder missing')

            else:
                if '作者信息' not in style_names or '日期' not in style_names:
                    errors.append(f'{rel}: article metadata styles missing')
                for token in ('作者：在这里填写作者', '单位：在这里填写单位', '日期：在这里填写日期'):
                    if token not in text:
                        errors.append(f'{rel}: missing article metadata placeholder {token}')

                footer_parts = [name for name in names if name.startswith('word/footer') and name.endswith('.xml')]
                if not footer_parts:
                    errors.append(f'{rel}: article page-number footer missing')
                else:
                    fields = []
                    for name in footer_parts:
                        root = etree.fromstring(zf.read(name))
                        fields.extend((node.get(Q('instr')) or '') for node in root.findall('.//w:fldSimple', NS))
                    if not any('PAGE' in field for field in fields):
                        errors.append(f'{rel}: article PAGE field missing')

                page_number = document.find('.//w:sectPr/w:pgNumType', NS)
                if page_number is None or page_number.get(Q('fmt')) != 'decimal' or page_number.get(Q('start')) != '1':
                    errors.append(f'{rel}: article page numbering should start at decimal 1')
    except Exception as exc:
        errors.append(f'{rel}: {exc}')

if errors:
    print('MANUSCRIPT CHECK FAILED')
    for error in errors:
        print('-', error)
    raise SystemExit(1)

print('OK: structured manuscript features verified for 12 templates')
