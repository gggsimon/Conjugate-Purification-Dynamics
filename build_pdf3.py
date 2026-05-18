#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CPD 论文 → PDF（reportlab + Arial Unicode）"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
import re, textwrap

FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
MD_PATH = "/Users/simon/.openclaw/workspace/Conjugate-Purification-Dynamics/paper/CPD_Theory_Draft.md"
OUT_PATH = "/Users/simon/.openclaw/workspace/Conjugate-Purification-Dynamics/paper/CPD_Theory_Draft.pdf"

# 注册中文字体
pdfmetrics.registerFont(TTFont("CN", FONT_PATH))

W, H = A4          # 595 x 842 pt
MARGIN = 2.5 * cm  # 左边距
LINE_H = 16          # 行高 pt
MAX_W = W - 2 * MARGIN

def clean(s):
    s = re.sub(r'\$\$.*?\$\$', '', s, flags=re.DOTALL)
    s = re.sub(r'`[^`]*`', '', s)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'[#*`>|\-]', '', s)
    s = s.replace('\\', '').replace('$$', '')
    return s.strip()

with open(MD_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

c = canvas.Canvas(OUT_PATH, pagesize=A4)
y = H - 3 * cm

def check_page(new_line_h=LINE_H):
    global y
    if y < 3 * cm:
        c.showPage()
        y = H - 3 * cm

def write_line(text, size=11, bold=False, indent=0):
    global y
    check_page()
    font = "CN"
    c.setFont(font, size)
    c.drawString(MARGIN + indent, y, text[:200])
    y -= LINE_H

def write_wrapped(text, size=10, indent=0, max_width=None):
    global y
    if not text.strip():
        return
    font = "CN"
    c.setFont(font, size)
    if max_width is None:
        max_width = MAX_W - indent
    chars_per_line = int(max_width / (size * 0.6))
    wrapped = textwrap.wrap(text, width=chars_per_line)
    for line in wrapped:
        check_page()
        c.setFont(font, size)
        c.drawString(MARGIN + indent, y, line)
        y -= LINE_H * (size / 10)

in_code = False
for line in lines:
    stripped = line.strip()
    if not stripped:
        y -= 4
        continue
    if stripped.startswith('```'):
        in_code = not in_code
        continue
    if in_code:
        write_line(stripped[:120], size=7, indent=10)
        continue

    # 一级标题
    if re.match(r'^# ', stripped):
        y -= 6
        write_line(clean(stripped[2:]), size=16, bold=True)
        y -= 4
        continue
    # 二级标题
    if re.match(r'^## ', stripped):
        y -= 4
        write_line(clean(stripped[3:]), size=13, bold=True)
        y -= 3
        continue
    # 三级标题
    if re.match(r'^### ', stripped):
        y -= 2
        write_line(clean(stripped[4:]), size=11, bold=True)
        continue
    # 列表
    if stripped.startswith('- ') or stripped.startswith('* '):
        write_wrapped("• " + clean(stripped[2:]), size=10, indent=10)
        continue
    # 普通段落
    cleaned = clean(stripped)
    if cleaned:
        write_wrapped(cleaned, size=10)

c.save()
print(f"✅ PDF 已生成: {OUT_PATH}")
