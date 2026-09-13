#!/usr/bin/env python3
from pathlib import Path
import zipfile
from lxml import etree
ROOT=Path(__file__).resolve().parents[1]
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; WNE='http://schemas.microsoft.com/office/word/2006/wordml'; CT='http://schemas.openxmlformats.org/package/2006/content-types'; PR='http://schemas.openxmlformats.org/package/2006/relationships'
NS={'w':W,'wne':WNE,'ct':CT,'pr':PR}; Q=lambda ns,tag:f'{{{ns}}}{tag}'
EXPECTED_CODES=['0631','0632','0633','0634','0642','0651','0646','065A']
EXPECTED_FONTS={'windows':{'body':'宋体','heading':'黑体','quote':'楷体','title':'微软雅黑'},'macos':{'body':'Songti SC','heading':'PingFang SC','quote':'Kaiti SC','title':'PingFang SC'}}
REQUIRED={'[Content_Types].xml','_rels/.rels','word/document.xml','word/_rels/document.xml.rels','word/styles.xml','word/numbering.xml','word/settings.xml','word/customizations.xml','docProps/core.xml','docProps/app.xml'}
EXTRA_STYLES=['结构标题','目录标题','摘要','关键词','参考文献','模板提示']

def style_by_name(root,name):
    for st in root.findall('w:style',NS):
        n=st.find('w:name',NS)
        if n is not None and n.get(Q(W,'val'))==name: return st
    return None

def font_of(st):
    if st is None:return None
    rp=st.find('w:rPr',NS); rf=rp.find('w:rFonts',NS) if rp is not None else None
    return rf.get(Q(W,'eastAsia')) if rf is not None else None

errors=[]; files=sorted((ROOT/'templates').rglob('*.dotx'))
if len(files)!=24: errors.append(f'expected 24 templates, got {len(files)}')
for p in files:
 platform=p.relative_to(ROOT/'templates').parts[0]
 structured='structured' in p.relative_to(ROOT/'templates').parts
 try:
  with zipfile.ZipFile(p) as z:
   if z.testzip(): errors.append(f'{p}: corrupt zip')
   miss=REQUIRED-set(z.namelist())
   if miss: errors.append(f'{p}: missing {sorted(miss)}')
   c=etree.fromstring(z.read('[Content_Types].xml')); d=[x.get('ContentType') for x in c.findall('ct:Override',NS) if x.get('PartName')=='/word/document.xml']
   if d!=['application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml']: errors.append(f'{p}: bad document content type {d}')
   cust=etree.fromstring(z.read('word/customizations.xml')); codes=[x.get(Q(WNE,'kcmPrimary')) for x in cust.findall('.//wne:keymap',NS)[:8]]
   if codes!=EXPECTED_CODES: errors.append(f'{p}: shortcuts {codes}')
   styles=etree.fromstring(z.read('word/styles.xml'))
   for name,role in [('Body Text','body'),('Title','title'),('heading 1','heading'),('AC','quote')]:
    got=font_of(style_by_name(styles,name)); want=EXPECTED_FONTS[platform][role]
    if got!=want: errors.append(f'{p}: {name} font {got!r} != {want!r}')
   for name in EXTRA_STYLES:
    if style_by_name(styles,name) is None: errors.append(f'{p}: missing utility style {name}')
   num=etree.fromstring(z.read('word/numbering.xml'))
   if len(num.findall('w:abstractNum/w:lvl',NS))!=4: errors.append(f'{p}: numbering is not four levels')
   rels=etree.fromstring(z.read('word/_rels/document.xml.rels'))
   if not any(r.get('Type','').endswith('/keyMapCustomizations') for r in rels): errors.append(f'{p}: missing shortcut relationship')
   doc=etree.fromstring(z.read('word/document.xml'))
   text=''.join((n.text or '') for n in doc.findall('.//w:t',NS))
   if '在这里输入' not in text: errors.append(f'{p}: missing beginner placeholder')
   if structured:
    if '参考文献（可选）' not in text: errors.append(f'{p}: structured template missing references block')
    if '/books/' in p.as_posix():
     if '前言（可选）' not in text or '附录（可选）' not in text: errors.append(f'{p}: structured book blocks missing')
     instr=' '.join((n.get(Q(W,'instr')) or '') for n in doc.findall('.//w:fldSimple',NS))
     if 'TOC' not in instr: errors.append(f'{p}: structured book missing TOC field')
    else:
     if '摘要（可选）' not in text or '关键词：' not in text: errors.append(f'{p}: structured article blocks missing')
 except Exception as e: errors.append(f'{p}: {e}')
if errors:
 print('VERIFY FAILED'); [print('-',e) for e in errors]; raise SystemExit(1)
print(f'OK: verified {len(files)} templates (12 direct-start + 12 structured)')
