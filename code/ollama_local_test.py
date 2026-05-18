#!/usr/bin/env python3
"""
Ollama 本地无对齐模型 GDI 实验脚本
逐温度原子调用，防 macOS SIGTERM
使用英文 Prompt 规避中文 trigram 饱和

用法：
  python ollama_local_test.py --temp 0.68    # 单温度测试
  python ollama_local_test.py --scan          # 全温度扫描（逐条手动运行）
"""

import json
import requests
import time
import os
import sys
import argparse

# ============ 配置 ============
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b-base"
PROMPT_EN = "Briefly describe the connection between human consciousness and artificial intelligence."
MAX_GEN_TOKENS = 128
OUTPUT_PATH = "../experiment_data/qwen3b_english_data.json"
# ==============================

def calculate_gdi(en_text):
    """英文文本 GDI 计算（bigram 多样性）"""
    tokens = en_text.strip().split()
    n = len(tokens)

    # 多样性 B（bigram）
    if n >= 2:
        bigrams = set(tuple(tokens[i:i+2]) for i in range(n-1))
        B = len(bigrams) / (n - 1)
    else:
        B = 0.0

    # 确定性 A（低频词占比）
    from collections import Counter
    counts = Counter(tokens)
    rare = sum(1 for _, c in counts.items() if c <= 2)
    A = rare / n if n > 0 else 0.0

    GDI = round(A**2 + B**2, 4)
    return round(B, 4), round(A, 4), GDI


def call_ollama(temp, prompt=PROMPT_EN):
    """单次调用 Ollama API"""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "options": {
            "temperature": temp,
            "num_predict": MAX_GEN_TOKENS,
            "top_p": 1.0,
            "frequency_penalty": 0,
            "presence_penalty": 0
        },
        "stream": False
    }
    try:
        resp = requests.post(OLLAMA_API, json=payload, timeout=30)
        return resp.json().get("response", "[NO_RESPONSE]")
    except Exception as e:
        return f"[ERROR: {e}]"


def run_single_temp(temp):
    """运行单个温度，保存结果"""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # 读取已有数据
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    print(f"🌡️  温度 T = {temp}")
    text = call_ollama(temp)
    B, A, GDI = calculate_gdi(text)

    data[str(temp)] = {
        "diversity_B": B,
        "specificity_A": A,
        "GDI_total": GDI,
        "sample_text": text[:200]
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"   B(多样性) = {B}")
    print(f"   A(确定性) = {A}")
    print(f"   GDI = {GDI}")
    print(f"✅ 已保存至 {OUTPUT_PATH}")
    return data


def main():
    parser = argparse.ArgumentParser(description="Ollama 本地模型 GDI 实验")
    parser.add_argument("--temp", type=float, help="指定单个温度（如 0.68）")
    parser.add_argument("--scan", action="store_true", help="打印全温度扫描指引")
    args = parser.parse_args()

    if args.temp:
        run_single_temp(args.temp)
    elif args.scan:
        temps = [0.10, 0.17, 0.23, 0.30, 0.39, 0.51, 0.60, 0.68, 0.77, 0.86, 1.00, 1.20, 1.45, 1.70, 2.00]
        print("📋 全温度扫描指引（逐条运行，避免 macOS SIGTERM）\n")
        for t in temps:
            print(f"python code/ollama_local_test.py --temp {t}")
        print(f"\n扫描完成后运行：python code/result_plot.py")
    else:
        print("请指定 --temp <值> 或 --scan")
        sys.exit(1)


if __name__ == "__main__":
    main()
