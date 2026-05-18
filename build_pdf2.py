#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CPD 论文生成 PDF（fpdf2 + Arial Unicode）"""

from fpdf import FPDF
import os, re

FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
MD_PATH = "/Users/simon/.openclaw/workspace/Conjugate-Purification-Dynamics/paper/CPD_Theory_Draft.md"
OUT_PATH = "/Users/simon/.openclaw/workspace/Conjugate-Purification-Dynamics/paper/CPD_Theory_Draft.pdf"

class PDF(FPDF):
    def header(self):
        pass
    def footer(self):
        self.set_y(-15)
        self.set_font("CN", "", 8)
        self.cell(0, 10, f"第 {self.page_no()} 页", align="C")

pdf = PDF()
pdf.add_font("CN", "", FONT_PATH)
pdf.add_font("CN", "B", FONT_PATH)
pdf.set_auto_page_break(auto=True, margin=20)
pdf.set_margins(20, 20, 20)

def clean(s):
    """去掉 markdown 语法，保留文字"""
    s = re.sub(r'\$\$.*?\$\$', '', s, flags=re.DOTALL)   # 去掉 $$ 公式
    s = re.sub(r'\`.*?\`', '', s)                        # 去掉行内代码
    s = re.sub(r'\[.*?\]\(.*?\)', '', s)                # 去掉链接
    s = re.sub(r'[#*`>|\-]', '', s)                     # 去掉 markdown 符号
    s = s.replace('$$', '').replace('\\', '')
    return s.strip()

with open(MD_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

pdf.add_page()
pdf.set_font("CN", "B", 16)
pdf.multi_cell(0, 10, "共轭净化动力学：生成系统的守恒迭代理论与0.68临界常数提案", align="C")
pdf.ln(2)
pdf.set_font("CN", "", 11)
pdf.multi_cell(0, 7, "作者：道玄（独立研究者）", align="C")
pdf.multi_cell(0, 7, "状态：初步提案（Preliminary Proposal）—— 理论框架完整，部分实验验证进行中", align="C")
pdf.multi_cell(0, 7, "日期：2026-05-19", align="C")
pdf.ln(4)

in_code = False
for line in lines:
    stripped = line.strip()
    if not stripped:
        continue
    if stripped.startswith("```"):
        in_code = not in_code
        continue
    if in_code:
        pdf.set_font("CN", "", 8)
        pdf.multi_cell(0, 4, stripped[:120])
        continue

    # 标题
    if re.match(r'^# ', stripped):
        pdf.ln(3)
        pdf.set_font("CN", "B", 14)
        pdf.multi_cell(0, 9, clean(stripped[2:]))
        pdf.ln(1)
        continue
    if re.match(r'^## ', stripped):
        pdf.ln(2)
        pdf.set_font("CN", "B", 12)
        pdf.multi_cell(0, 8, clean(stripped[3:]))
        pdf.ln(1)
        continue
    if re.match(r'^### ', stripped):
        pdf.ln(1)
        pdf.set_font("CN", "B", 11)
        pdf.multi_cell(0, 7, clean(stripped[4:]))
        continue

    # 列表
    if stripped.startswith('- ') or stripped.startswith('* '):
        pdf.set_font("CN", "", 10)
        txt = clean(stripped[2:])
        pdf.multi_cell(0, 5, "  • " + txt)
        continue

    # 普通段落
    pdf.set_font("CN", "", 10)
    txt = clean(stripped)
    if txt:
        pdf.multi_cell(0, 5, txt)

pdf.output(OUT_PATH)
print(f"✅ PDF 已生成: {OUT_PATH}")
