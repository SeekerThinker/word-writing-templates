#!/usr/bin/env python3
"""Verify manuscript-oriented features in the 12 v4 public templates."""
from pathlib import Path
import zipfile
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
Q = lambda tag: f'{{{W}}}{tag}'

errors = []
files = sorted(
    p for p in (ROOT / 'templates').rglob('*.dotx')
    if 'structured' not in p.relative_to(ROOT / 'templates').parts
)

for path in files:
    rel = path.relative_to(ROOT / 'templates')
    try:
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
            document = etree.fromstring(zf.read('word/document.xml'))
            styles = etree.fromstring(zf.read('word/styles.xml'))
            settings = etree.fromstring(zf.read('word/settings.xml'))
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

                if settings.find('w:evenAndOddHeaders', NS) is None:
                    errors.append(f'{rel}: odd/even header mode missing')
                if settings.find('w:mirrorMargins', NS) is None:
                    errors.append(f'{rel}: mirrorMargins missing')

                h1 = styles.find(".//w:style[@w:styleId='Heading1']", NS)
                if h1 is None or h1.find('.//w:pageBreakBefore', NS) is None:
                    errors.append(f'{rel}: Heading 1 should start on a new page')
                if h1 is None or h1.find('.//w:keepNext', NS) is None:
                    errors.append(f'{rel}: Heading 1 should stay with following paragraph')

                pg_nodes = document.findall('.//w:sectPr/w:pgNumType', NS)
                formats = [node.get(Q('fmt')) for node in pg_nodes]
                starts = [node.get(Q('start')) for node in pg_nodes]
                if 'lowerRoman' not in formats or 'decimal' not in formats:
                    errors.append(f'{rel}: expected Roman front matter and decimal body numbering, got {formats}')
                if starts.count('1') < 2:
                    errors.append(f'{rel}: expected front/body numbering to restart at 1, got {starts}')

                for idx, sect in enumerate(sectprs):
                    mar = sect.find('w:pgMar', NS)
                    if mar is None or int(mar.get(Q('gutter'), '0')) < 200:
                        errors.append(f'{rel}: section {idx+1} should reserve print gutter')

                header_parts = [name for name in names if name.startswith('word/header') and name.endswith('.xml')]
                footer_parts = [name for name in names if name.startswith('word/footer') and name.endswith('.xml')]
                if len(header_parts) < 4:
                    errors.append(f'{rel}: expected separate odd/even running headers')
                if len(footer_parts) < 4:
                    errors.append(f'{rel}: expected front/body odd/even page-number footers')

                fields = []
                for name in header_parts + footer_parts:
                    root = etree.fromstring(zf.read(name))
                    fields.extend((node.get(Q('instr')) or '') for node in root.findall('.//w:fldSimple', NS))
                if not any('STYLEREF "Title"' in field for field in fields):
                    errors.append(f'{rel}: even-page book-title STYLEREF missing')
                if not any('STYLEREF "Heading 1"' in field for field in fields):
                    errors.append(f'{rel}: odd-page chapter STYLEREF missing')
                if sum('PAGE' in field for field in fields) < 4:
                    errors.append(f'{rel}: PAGE fields missing from front/body odd/even footers')
                for token in ('作者：在这里填写作者', '前言（可选）', '附录（可选）', '参考文献（可选）'):
                    if token not in text:
                        errors.append(f'{rel}: missing book manuscript block {token}')
                if '以后每个“标题 1”都会自动另起新页' not in text:
                    errors.append(f'{rel}: chapter page-break guidance missing')

            else:
                if '作者信息' not in style_names or '日期' not in style_names:
                    errors.append(f'{rel}: article metadata styles missing')
                for token in ('作者：在这里填写作者', '单位：在这里填写单位', '日期：在这里填写日期', '摘要（可选）', '关键词：', '参考文献（可选）'):
                    if token not in text:
                        errors.append(f'{rel}: missing article manuscript block {token}')

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

if len(files) != 12:
    errors.append(f'expected 12 public unified templates, got {len(files)}')

if errors:
    print('MANUSCRIPT CHECK FAILED')
    for error in errors:
        print('-', error)
    raise SystemExit(1)

print('OK: manuscript features verified for 12 public unified templates')
