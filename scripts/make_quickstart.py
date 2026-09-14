#!/usr/bin/env python3
from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

ROOT=Path(__file__).resolve().parents[1]
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
FONT='STSong-Light'
W,H=A4

MATRIX=[
 ('书籍｜中文传统','第一章 → 第一节 → 一、 → （一）'),
 ('书籍｜章节数字','第1章 → 1.1 → 1.1.1 → 1.1.1.1'),
 ('书籍｜纯数字','1 → 1.1 → 1.1.1 → 1.1.1.1'),
 ('文章｜中文论文','一、 → （一） → 1. → （1）'),
 ('文章｜数字层级','1 → 1.1 → 1.1.1 → 1.1.1.1'),
 ('文章｜中文简洁','一、 → 1. → （1） → ①'),
]

def txt(c,x,y,s,size=11):
    c.setFont(FONT,size); c.drawString(x,y,s)

def make(platform):
    iswin=platform=='windows'
    label='Windows' if iswin else 'macOS / MacBook'
    out=ROOT/'docs'/f'开始使用-{platform}.pdf'
    c=Canvas(str(out),pagesize=A4)
    c.setTitle(f'Word 结构化思考与写作模板集 - {label} 开始使用')
    x=22*mm; y=H-22*mm
    txt(c,x,y,'Word 结构化思考与写作模板集',19); y-=10*mm
    txt(c,x,y,f'{label}｜先用结构思考，再自然长成成稿',13); y-=10*mm

    txt(c,x,y,'第一次使用',13); y-=8*mm
    steps=[
      '1. 进入“书籍模板”或“文章模板”，选择喜欢的章节编号。',
      '2. 双击 .dotx。Word 会创建新文档，原模板不会被改坏。',
      '3. 大主题用“标题 1”；需要拆分时用“标题 2 / 3 / 4”。',
      '4. 写一会儿后打开“导航窗格”，只看标题检查整体结构。',
    ]
    for s in steps: txt(c,x,y,s,10.5); y-=7.2*mm

    y-=2*mm
    txt(c,x,y,'结构五问：并列吗？单一吗？完整吗？重复吗？顺序对吗？',10); y-=8*mm
    txt(c,x,y,'前言、摘要、作者信息、目录、参考文献等已经在模板里；暂时不用可以保留。',9.5); y-=6.5*mm
    txt(c,x,y,'这些可选区块不会进入导航窗格，导航窗格主要显示你的标题层级。',9.5); y-=10*mm

    txt(c,x,y,'常用快捷键（可选）',13); y-=8*mm
    pre='Ctrl + Alt +' if iswin else 'Command + Option +'
    rows=[('一级标题',pre+' 1'),('二级标题',pre+' 2'),('三级标题',pre+' 3'),('四级标题',pre+' 4'),('正文',pre+' Z'),('表格文字',pre+' B'),('引用',pre+' Q'),('插入脚注',pre+' F')]
    for i,(a,b) in enumerate(rows):
        col=i%2; row=i//2
        xx=x+col*82*mm; yy=y-row*7.2*mm
        txt(c,xx,yy,a,9.5); txt(c,xx+27*mm,yy,b,9.5)
    y-=34*mm
    txt(c,x,y,'不会快捷键也没关系，直接在 Word 的“样式”区域选择标题和正文即可。',9); y-=10*mm

    txt(c,x,y,'选模板只看编号',13); y-=8*mm
    for name,ex in MATRIX:
        txt(c,x,y,name,9.5); txt(c,x+46*mm,y,ex,9.5); y-=7*mm

    y-=3*mm
    txt(c,x,y,'一句话：标题层级承载思考，导航窗格提供全局视野，排版功能尽量不打断你。',9)
    c.showPage(); c.save(); print(out)

for p in ('windows','macos'): make(p)
