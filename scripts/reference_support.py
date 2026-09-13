#!/usr/bin/env python3
"""Add Word-native Chinese figure/table caption defaults to generated templates.

This is intentionally a post-generation OOXML pass. It keeps the core template
builder focused on writing structure while registering document-level caption
labels that Microsoft Word's References > Insert Caption command understands.
No macros, add-ins, or runtime dependencies are added to the templates.
"""
from __future__ import annotations

import zipfile
from pathlib import Path
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
Q = lambda tag: f'{{{W}}}{tag}'
NS = {'w': W}

BODY_FONTS = {'windows': '宋体', 'macos': 'Songti SC'}


def set_child(parent, tag, val=None, **attrs):
    child = parent.find(Q(tag))
    if child is None:
        child = etree.SubElement(parent, Q(tag))
    if val is not None:
        child.set(Q('val'), str(val))
    for key, value in attrs.items():
        child.set(Q(key), str(value))
    return child


def set_fonts(rpr, family):
    rfonts = rpr.find(Q('rFonts'))
    if rfonts is None:
        rfonts = etree.Element(Q('rFonts'))
        rpr.insert(0, rfonts)
    for attr in ('ascii', 'eastAsia', 'hAnsi', 'cs'):
        rfonts.set(Q(attr), family)


def clean_run_style(rpr, family, size_half_points, color):
    set_fonts(rpr, family)
    for tag in ('b', 'bCs', 'i', 'iCs'):
        node = rpr.find(Q(tag))
        if node is not None:
            rpr.remove(node)
    c = set_child(rpr, 'color', color)
    for attr in ('themeColor', 'themeTint', 'themeShade'):
        c.attrib.pop(Q(attr), None)
    set_child(rpr, 'sz', size_half_points)
    set_child(rpr, 'szCs', size_half_points)


def style_caption(styles, family):
    style = styles.find(".//w:style[@w:styleId='Caption']", NS)
    if style is None:
        style = etree.SubElement(styles, Q('style'))
        style.set(Q('type'), 'paragraph')
        style.set(Q('styleId'), 'Caption')
        set_child(style, 'name', 'caption')
        set_child(style, 'basedOn', 'Normal')
        set_child(style, 'next', 'Normal')
    semi = style.find(Q('semiHidden'))
    if semi is not None:
        style.remove(semi)
    if style.find(Q('qFormat')) is None:
        style.append(etree.Element(Q('qFormat')))
    ppr = style.find(Q('pPr'))
    if ppr is None:
        ppr = etree.SubElement(style, Q('pPr'))
    set_child(ppr, 'jc', 'center')
    set_child(ppr, 'spacing', before='80', after='120', line='300', lineRule='auto')
    set_child(ppr, 'keepLines')
    set_child(ppr, 'widowControl')
    ind = ppr.find(Q('ind'))
    if ind is not None:
        ind.set(Q('firstLine'), '0')
    rpr = style.find(Q('rPr'))
    if rpr is None:
        rpr = etree.SubElement(style, Q('rPr'))
    clean_run_style(rpr, family, '21', '000000')


def style_source(styles, family):
    existing = None
    for style in styles.findall('w:style', NS):
        name = style.find('w:name', NS)
        if name is not None and name.get(Q('val')) == '图表来源':
            existing = style
            break
    style = existing
    if style is None:
        style = etree.SubElement(styles, Q('style'))
        style.set(Q('type'), 'paragraph')
        style.set(Q('styleId'), 'FigureTableSource')
        set_child(style, 'name', '图表来源')
        set_child(style, 'basedOn', 'Normal')
        set_child(style, 'next', 'Normal')
        set_child(style, 'uiPriority', '50')
    if style.find(Q('qFormat')) is None:
        style.append(etree.Element(Q('qFormat')))
    ppr = style.find(Q('pPr'))
    if ppr is None:
        ppr = etree.SubElement(style, Q('pPr'))
    set_child(ppr, 'jc', 'center')
    set_child(ppr, 'spacing', before='0', after='160', line='276', lineRule='auto')
    set_child(ppr, 'keepLines')
    ind = ppr.find(Q('ind'))
    if ind is None:
        ind = etree.SubElement(ppr, Q('ind'))
    ind.set(Q('firstLine'), '0')
    rpr = style.find(Q('rPr'))
    if rpr is None:
        rpr = etree.SubElement(style, Q('rPr'))
    clean_run_style(rpr, family, '18', '5F5F5F')


def caption_defaults(settings, kind):
    update = settings.find(Q('updateFields'))
    if update is None:
        update = etree.SubElement(settings, Q('updateFields'))
    update.set(Q('val'), 'true')

    captions = settings.find(Q('captions'))
    if captions is None:
        captions = etree.SubElement(settings, Q('captions'))
    for node in list(captions.findall(Q('caption'))):
        if node.get(Q('name')) in {'图', '表'}:
            captions.remove(node)

    for name, pos in (('图', 'below'), ('表', 'above')):
        node = etree.SubElement(captions, Q('caption'))
        node.set(Q('name'), name)
        node.set(Q('pos'), pos)
        node.set(Q('numFmt'), 'decimal')
        if kind == 'books':
            node.set(Q('chapNum'), '1')
            node.set(Q('heading'), '1')
            node.set(Q('separator'), 'hyphen')


def patch(path: Path):
    rel = path.relative_to(ROOT / 'templates')
    platform = rel.parts[0]
    kind = 'books' if 'books' in rel.parts else 'articles'
    family = BODY_FONTS[platform]

    with zipfile.ZipFile(path, 'r') as zin:
        files = {name: zin.read(name) for name in zin.namelist()}

    styles = etree.fromstring(files['word/styles.xml'])
    settings = etree.fromstring(files['word/settings.xml'])
    style_caption(styles, family)
    style_source(styles, family)
    caption_defaults(settings, kind)
    files['word/styles.xml'] = etree.tostring(styles, xml_declaration=True, encoding='UTF-8', standalone=True)
    files['word/settings.xml'] = etree.tostring(settings, xml_declaration=True, encoding='UTF-8', standalone=True)

    tmp = path.with_suffix('.tmp')
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)
    tmp.replace(path)
    print(rel)


def main():
    files = sorted((ROOT / 'templates').rglob('*.dotx'))
    if len(files) != 24:
        raise SystemExit(f'expected 24 generated templates before reference support, got {len(files)}')
    for path in files:
        patch(path)


if __name__ == '__main__':
    main()
