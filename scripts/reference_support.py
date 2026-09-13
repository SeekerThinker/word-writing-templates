#!/usr/bin/env python3
"""Add Word-native caption, note, and bibliography defaults to generated templates.

This is intentionally a post-generation OOXML pass. It keeps the core template
builder focused on writing structure while registering document-level reference
features that Microsoft Word understands. No macros, add-ins, or runtime
packages are embedded in the templates.

v2.8: Chinese figure/table caption labels and caption/source styles.
v2.9: footnote/endnote styles plus bibliography/reference-entry styles that
       remain friendly to Word citation fields and third-party citation tools.
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


def remove_child(parent, tag):
    child = parent.find(Q(tag))
    if child is not None:
        parent.remove(child)


def set_fonts(rpr, family):
    rfonts = rpr.find(Q('rFonts'))
    if rfonts is None:
        rfonts = etree.Element(Q('rFonts'))
        rpr.insert(0, rfonts)
    for attr in ('ascii', 'eastAsia', 'hAnsi', 'cs'):
        rfonts.set(Q(attr), family)


def clean_run_style(rpr, family, size_half_points, color='000000'):
    set_fonts(rpr, family)
    for tag in ('b', 'bCs', 'i', 'iCs'):
        remove_child(rpr, tag)
    c = set_child(rpr, 'color', color)
    for attr in ('themeColor', 'themeTint', 'themeShade'):
        c.attrib.pop(Q(attr), None)
    set_child(rpr, 'sz', size_half_points)
    set_child(rpr, 'szCs', size_half_points)


def style_by_name(styles, name):
    for style in styles.findall('w:style', NS):
        node = style.find('w:name', NS)
        if node is not None and node.get(Q('val')) == name:
            return style
    return None


def ensure_style(styles, style_id, name, style_type='paragraph', based_on=None, next_style=None):
    style = styles.find(f".//w:style[@w:styleId='{style_id}']", NS)
    if style is None:
        style = etree.SubElement(styles, Q('style'))
        style.set(Q('type'), style_type)
        style.set(Q('styleId'), style_id)
    set_child(style, 'name', name)
    if based_on:
        set_child(style, 'basedOn', based_on)
    if next_style and style_type == 'paragraph':
        set_child(style, 'next', next_style)
    return style


def make_quick_style(style):
    remove_child(style, 'semiHidden')
    remove_child(style, 'unhideWhenUsed')
    if style.find(Q('qFormat')) is None:
        style.append(etree.Element(Q('qFormat')))


def paragraph_props(style):
    ppr = style.find(Q('pPr'))
    if ppr is None:
        ppr = etree.SubElement(style, Q('pPr'))
    return ppr


def run_props(style):
    rpr = style.find(Q('rPr'))
    if rpr is None:
        rpr = etree.SubElement(style, Q('rPr'))
    return rpr


def style_caption(styles, family):
    style = ensure_style(styles, 'Caption', 'caption', based_on='Normal', next_style='Normal')
    make_quick_style(style)
    ppr = paragraph_props(style)
    set_child(ppr, 'jc', 'center')
    set_child(ppr, 'spacing', before='80', after='120', line='300', lineRule='auto')
    set_child(ppr, 'keepLines')
    set_child(ppr, 'widowControl')
    ind = ppr.find(Q('ind'))
    if ind is not None:
        ind.set(Q('firstLine'), '0')
    clean_run_style(run_props(style), family, '21')


def style_source(styles, family):
    style = style_by_name(styles, '图表来源')
    if style is None:
        style = ensure_style(styles, 'FigureTableSource', '图表来源', based_on='Normal', next_style='Normal')
        set_child(style, 'uiPriority', '50')
    make_quick_style(style)
    ppr = paragraph_props(style)
    set_child(ppr, 'jc', 'center')
    set_child(ppr, 'spacing', before='0', after='160', line='276', lineRule='auto')
    set_child(ppr, 'keepLines')
    ind = ppr.find(Q('ind'))
    if ind is None:
        ind = etree.SubElement(ppr, Q('ind'))
    ind.set(Q('firstLine'), '0')
    clean_run_style(run_props(style), family, '18', '5F5F5F')


def style_note_text(styles, family, style_id, name):
    style = ensure_style(styles, style_id, name, based_on='Normal', next_style=style_id)
    ppr = paragraph_props(style)
    set_child(ppr, 'spacing', before='0', after='0', line='240', lineRule='auto')
    set_child(ppr, 'widowControl')
    ind = ppr.find(Q('ind'))
    if ind is None:
        ind = etree.SubElement(ppr, Q('ind'))
    for attr in ('left', 'right', 'firstLine', 'hanging'):
        ind.attrib.pop(Q(attr), None)
    ind.set(Q('firstLine'), '0')
    clean_run_style(run_props(style), family, '18')


def style_note_reference(styles, family, style_id, name):
    style = ensure_style(styles, style_id, name, style_type='character', based_on='DefaultParagraphFont')
    rpr = run_props(style)
    clean_run_style(rpr, family, '16')
    set_child(rpr, 'vertAlign', 'superscript')


def style_bibliography(styles, family):
    style = ensure_style(styles, 'Bibliography', 'Bibliography', based_on='Normal', next_style='Bibliography')
    make_quick_style(style)
    set_child(style, 'uiPriority', '45')
    ppr = paragraph_props(style)
    set_child(ppr, 'spacing', before='0', after='80', line='300', lineRule='auto')
    set_child(ppr, 'widowControl')
    ind = ppr.find(Q('ind'))
    if ind is None:
        ind = etree.SubElement(ppr, Q('ind'))
    ind.set(Q('left'), '420')
    ind.set(Q('hanging'), '420')
    ind.attrib.pop(Q('firstLine'), None)
    clean_run_style(run_props(style), family, '21')


def style_reference_entry(styles, family):
    style = style_by_name(styles, '参考文献条目')
    if style is None:
        style = ensure_style(styles, 'ReferenceEntry', '参考文献条目', based_on='Bibliography', next_style='ReferenceEntry')
        set_child(style, 'uiPriority', '46')
    make_quick_style(style)
    ppr = paragraph_props(style)
    set_child(ppr, 'spacing', before='0', after='80', line='300', lineRule='auto')
    set_child(ppr, 'widowControl')
    ind = ppr.find(Q('ind'))
    if ind is None:
        ind = etree.SubElement(ppr, Q('ind'))
    ind.set(Q('left'), '420')
    ind.set(Q('hanging'), '420')
    ind.attrib.pop(Q('firstLine'), None)
    clean_run_style(run_props(style), family, '21')


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
    style_note_text(styles, family, 'FootnoteText', 'footnote text')
    style_note_reference(styles, family, 'FootnoteReference', 'footnote reference')
    style_note_text(styles, family, 'EndnoteText', 'endnote text')
    style_note_reference(styles, family, 'EndnoteReference', 'endnote reference')
    style_bibliography(styles, family)
    style_reference_entry(styles, family)
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
