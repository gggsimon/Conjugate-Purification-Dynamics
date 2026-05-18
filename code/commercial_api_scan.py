#!/usr/bin/env python3
"""
商用大模型 API 温度扫描脚本
支持 DeepSeek、腾讯混元等 OpenAI 兼容 API
"""

import json
import time
import requests
import sys
import os

# ============ 配置区 ============
API_URL = "http://127.0.0.1:19000/proxy/llm/chat/completions"
MODEL_NAME = "default"
TEMPERATURES = [0.10, 0.18, 0.26, 0.34, 0.43, 0.51, 0.60, 0.68, 0.77, 0.86, 0.95, 1.20, 1.45, 1.70, 2.00]
N_SAMPLES = 8
MAX_TOKENS = 400
OUTPUT_PATH = "../experiment_data/commercial_api_real.json"
# =================================

PROMPT_ZH = "请用量子力学的视角，写一段关于人工智能与人类意识关系的科幻短句（100-200字）。"

def call_api(temp, prompt=PROMPT_ZH):
    """调用大模型 API"""
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temp,
        "max_tokens": MAX_TOKENS,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "stream": False
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=30)
        data = resp.json()
        # 兼容多种返回格式
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        elif "response" in data:
            return data["response"]
        else:
            return "[ERROR: " + str(data)[:100] + "]"
    except Exception as e:
        return f"[ERROR: {e}]"


def run_scan():
    """执行全温度扫描（逐温度原子调用，防 macOS SIGTERM）"""
    results = {}
    if os.path.exists(OUTPUT_PATH):
        try:
            results = json.load(open(OUTPUT_PATH, "r", encoding="utf-8"))
        except:
            results = {}

    total = len(TEMPERATURES) * N_SAMPLES
    done = sum(len(v) if isinstance(v, list) else 1 for v in results.values())

    print(f"📊 商用 API 温度扫描启动")
    print(f"   总任务: {total} 次调用")
    print(f"   已完成: {done} 次")
    print(f"   待完成: {total - done} 次\n")

    for temp in TEMPERATURES:
        key = str(temp)
        if key not in results:
            results[key] = []

        needed = N_SAMPLES - len(results[key])
        if needed <= 0:
            print(f"✅ T={temp} 已完成 ({len(results[key])}/{N_SAMPLES})")
            continue

        print(f"📡 T={temp} 需补充 {needed} 个样本...")
        for i in range(needed):
            global_idx = done + 1
            print(f"   [{global_idx}/{total}] T={temp} #{i+1}/{needed}...", end=" ", flush=True)
            text = call_api(temp)
            results[key].append({
                "text": text[:200],
                "length": len(text)
            })
            # 实时保存
            json.dump(results, open(OUTPUT_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print(f"OK({len(text)}c)")
            time.sleep(0.3)

        done += needed

    print(f"\n🎉 全部完成！数据已保存至 {OUTPUT_PATH}")
    return results


if __name__ == "__main__":
    print("=" * 60)
    print("商用大模型 API 温度扫描工具")
    print("=" * 60)
    run_scan()
