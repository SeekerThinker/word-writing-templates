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
    c.setTitle(f'Word 结构化写作模板集 - {label} 开始使用')
    x=22*mm; y=H-24*mm
    txt(c,x,y,'Word 结构化写作模板集',20); y-=12*mm
    txt(c,x,y,f'{label}｜3 步开始写作',14); y-=11*mm
    steps=[
      '1. 进入“书籍模板”或“文章模板”，选择喜欢的章节编号。',
      '2. 直接双击第一层的 .dotx 文件。Word 会自动创建新文档，原模板不会被改坏。',
      '3. 把“在这里输入……”替换成自己的标题和正文，然后继续写。',
    ]
    for s in steps: txt(c,x,y,s,11); y-=8*mm
    y-=2*mm
    txt(c,x,y,'需要更接近成稿？“带常用结构”版还带页码；书籍版另含章节自动换页与双面打印设置。',9); y-=11*mm
    txt(c,x,y,'常用快捷键',14); y-=9*mm
    pre='Ctrl + Alt +' if iswin else 'Command + Option +'
    rows=[('一级标题',pre+' 1'),('二级标题',pre+' 2'),('三级标题',pre+' 3'),('四级标题',pre+' 4'),('正文',pre+' Z'),('表格文字',pre+' B'),('引用',pre+' Q'),('插入脚注',pre+' F')]
    for i,(a,b) in enumerate(rows):
        col=i%2; row=i//2
        xx=x+col*82*mm; yy=y-row*8*mm
        txt(c,xx,yy,a,10); txt(c,xx+28*mm,yy,b,10)
    y-=38*mm
    txt(c,x,y,'提示：不会快捷键也没关系，可以直接在 Word 的“样式”区域选择标题和正文。',9); y-=12*mm
    txt(c,x,y,'选模板只看编号',14); y-=9*mm
    for name,ex in MATRIX:
        txt(c,x,y,name,10); txt(c,x+46*mm,y,ex,10); y-=7.5*mm
    y-=4*mm
    txt(c,x,y,'目录、页眉页码、双面打印、导航窗格等进阶功能，不会也不影响开始写作。',9)
    c.showPage(); c.save(); print(out)

for p in ('windows','macos'): make(p)
