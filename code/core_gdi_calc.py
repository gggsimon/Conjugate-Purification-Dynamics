#!/usr/bin/env python3
"""
GDI 核心指标计算模块
支持中英文双语，自动检测语言选择 trigram(bigram for English)
"""

import jieba
import re
from collections import Counter
import math

def detect_language(text):
    """简单语言中英文检测：>30% 中文字符视为中文"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text.replace(' ', ''))
    if total_chars == 0:
        return 'unknown'
    return 'chinese' if (chinese_chars / total_chars) > 0.3 else 'english'


def calc_diversity_b(text, lang='auto'):
    """
    计算歧义分量 B（多样性）
    中文：trigram 多样性 = 不重复 trigram 数 / (总字数 - 2)
    英文：bigram 多样性 = 不重复 bigram 数 / (词数 - 1)
    """
    if lang == 'auto':
        lang = detect_language(text)

    if lang == 'chinese':
        chars = list(jieba.cut(text))
        n = len(chars)
        if n < 3:
            return 0.0
        trigrams = [tuple(chars[i:i+3]) for i in range(n - 2)]
        unique_trigrams = len(set(trigrams))
        return round(unique_trigrams / (n - 2), 4)
    else:
        tokens = text.strip().split()
        n = len(tokens)
        if n < 2:
            return 0.0
        bigrams = [tuple(tokens[i:i+2]) for i in range(n - 1)]
        unique_bigrams = len(set(bigrams))
        return round(unique_bigrams / (n - 1), 4)


def calc_specificity_a(text, lang='auto'):
    """
    计算确定性分量 A（特异性/低频词占比）
    低频词定义：在样本中出现的次数 <= 2
    """
    if lang == 'auto':
        lang = detect_language(text)

    if lang == 'chinese':
        tokens = list(jieba.cut(text))
    else:
        tokens = text.strip().split()

    n = len(tokens)
    if n == 0:
        return 0.0

    counts = Counter(tokens)
    rare_words = sum(1 for _, c in counts.items() if c <= 2)
    return round(rare_words / n, 4)


def calc_gdi(text, lang='auto'):
    """计算综合 GDI 分数 = A² + B²"""
    B = calc_diversity_b(text, lang)
    A = calc_specificity_a(text, lang)
    GDI = round(A**2 + B**2, 4)
    return B, A, GDI


def batch_calc(texts, lang='auto'):
    """批量计算多条文本的 GDI，返回平均值和标准差"""
    results = [calc_gdi(t, lang) for t in texts if t.strip()]
    if not results:
        return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    Bs, As, GDIs = zip(*results)
    return (
        round(np_mean(Bs), 4), round(np_std(Bs), 4),
        round(np_mean(As), 4), round(np_std(As), 4),
        round(np_mean(GDIs), 4), round(np_std(GDIs), 4)
    )

# 防止无 numpy 环境报错，用纯 Python 实现 mean/std
def np_mean(vals):
    return sum(vals) / len(vals)

def np_std(vals):
    m = np_mean(vals)
    return math.sqrt(sum((v - m)**2 for v in vals) / len(vals))


if __name__ == '__main__':
    # 自测
    test_zh = "人工智能正在深刻改变我们的生活方式和生产方式。"
    test_en = "Artificial intelligence is profoundly changing our lives."

    for txt, lang in [(test_zh, 'chinese'), (test_en, 'english')]:
        B, A, GDI = calc_gdi(txt, lang)
        print(f"[{lang}] B={B}, A={A}, GDI={GDI}")
