#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将 CPD_Theory_Draft.md 转为正式PDF（A4，中文字体，学术排版）"""

import subprocess, sys, os, re

# 检查是否有中文字体
font_paths = [
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]
FONT_PATH = None
for p in font_paths:
    if os.path.exists(p):
        FONT_PATH = p
        break

if not FONT_PATH:
    print("未找到中文字体，尝试安装字体或改用HTML转PDF方案")
    sys.exit(1)

print(f"使用字体: {FONT_PATH}")

# 方案：用 markdown -> html -> 系统打印 更可靠
# 先生成排版好的 HTML，然后用 wkhtmltopdf 或系统打印
# 但 wkhtmltopdf 未安装，改用 weasyprint（刚装了 fpdf2，试 weasyprint）
try:
    from weasyprint import HTML, CSS
    HAS_WEASYPRINT = True
except ImportError:
    HAS_WEASYPRINT = False

# 改用 markdown 转 html + weasyprint
import markdown

MD_PATH = "/Users/simon/.openclaw/workspace/Conjugate-Purification-Dynamics/paper/CPD_Theory_Draft.md"
OUT_PATH = "/Users/simon/.openclaw/workspace/Conjugate-Purification-Dynamics/paper/CPD_Theory_Draft.pdf"

with open(MD_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

# 转 HTML
html_body = markdown.markdown(md_content, extensions=["extra", "codehilite", "toc"])

html_full = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>
@font-face {{
    font-family: 'Chinese';
    src: url('file://{FONT_PATH}');
}}
body {{
    font-family: 'Chinese', 'PingFang SC', 'STHeiti', serif;
    font-size: 12pt;
    line-height: 1.8;
    max-width: 800px;
    margin: 40px auto;
    padding: 40px;
    color: #222;
}}
h1 {{ font-size: 20pt; text-align: center; margin-bottom: 10px; }}
h2 {{ font-size: 16pt; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 30px; }}
h3 {{ font-size: 14pt; margin-top: 20px; }}
code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-size: 10pt; }}
pre {{ background: #f4f4f4; padding: 12px; border-radius: 6px; overflow-x: auto; }}
blockquote {{ border-left: 4px solid #ccc; margin: 0; padding-left: 16px; color: #555; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

HTML(string=html_full).write_pdf(OUT_PATH)
print(f"✅ PDF 已生成: {OUT_PATH}")
