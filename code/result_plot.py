#!/usr/bin/env python3
"""
GDI 实验结果可视化 - 四联图
读取 experiment_data/*.json，绘制 Diversity / Specificity / GDI 曲线
"""

import json
import os
import sys

try:
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False
    print("⚠️  numpy/matplotlib 未安装，跳过绘图")


def load_data(filepath):
    """加载实验数据"""
    if not os.path.exists(filepath):
        print(f"❌ 数据文件不存在: {filepath}")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def plot_results(data, title, output_path):
    """绘制四联图"""
    if not HAS_PLOT:
        print("⚠️  跳过绘图（缺少 numpy/matplotlib）")
        return

    temps = sorted([float(k) for k in data.keys()])
    Bs = [data[str(t)]["diversity_B"] for t in temps]
    As = [data[str(t)]["specificity_A"] for t in temps]
    GDIs = [data[str(t)]["GDI_total"] for t in temps]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"GDI 温度扫描结果 — {title}", fontsize=14)

    # 子图1: Diversity B
    axes[0, 0].plot(temps, Bs, 'o-', color='steelblue', linewidth=2)
    axes[0, 0].set_title("Diversity B（歧义分量）")
    axes[0, 0].set_xlabel("Temperature")
    axes[0, 0].set_ylabel("B")
    axes[0, 0].grid(True, alpha=0.3)

    # 子图2: Specificity A
    axes[0, 1].plot(temps, As, 'o-', color='darkorange', linewidth=2)
    axes[0, 1].set_title("Specificity A（确定性分量）")
    axes[0, 1].set_xlabel("Temperature")
    axes[0, 1].set_ylabel("A")
    axes[0, 1].grid(True, alpha=0.3)

    # 子图3: GDI
    axes[1, 0].plot(temps, GDIs, 'o-', color='crimson', linewidth=2)
    axes[1, 0].set_title("GDI = A² + B²（综合分）")
    axes[1, 0].set_xlabel("Temperature")
    axes[1, 0].set_ylabel("GDI")
    axes[1, 0].grid(True, alpha=0.3)
    # 标注峰值
    max_idx = GDIs.index(max(GDIs))
    axes[1, 0].axvline(temps[max_idx], color='gray', linestyle='--', alpha=0.5)
    axes[1, 0].annotate(f"Peak @ T={temps[max_idx]}",
                         xy=(temps[max_idx], GDIs[max_idx]),
                         xytext=(5, 5), textcoords='offset points',
                         fontsize=9, color='gray')

    # 子图4: A 和 B 叠加
    axes[1, 1].plot(temps, As, 'o--', color='darkorange', label='A (Specificity)')
    axes[1, 1].plot(temps, Bs, 'o--', color='steelblue', label='B (Diversity)')
    axes[1, 1].plot(temps, GDIs, '-', color='crimson', label='GDI', linewidth=2)
    axes[1, 1].set_title("A / B / GDI 叠加")
    axes[1, 1].set_xlabel("Temperature")
    axes[1, 1].set_ylabel("Score")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"✅ 图表已保存: {output_path}")
    plt.close()


def main():
    print("=" * 50)
    print("GDI 结果可视化工具")
    print("=" * 50)

    # 查找数据文件
    data_dir = os.path.join(os.path.dirname(__file__), "../experiment_data")
    data_files = {
        "商用API": os.path.join(data_dir, "commercial_api_real.json"),
        "Qwen3B": os.path.join(data_dir, "qwen3b_pending.json"),
    }

    for name, path in data_files.items():
        print(f"\n📊 处理: {name}")
        print(f"   路径: {path}")
        data = load_data(path)
        if data:
            out_path = os.path.join(data_dir, f"{name.replace(' ', '_')}_chart.png")
            plot_results(data, name, out_path)
        else:
            print(f"   ⚠️  数据不可用，跳过")


if __name__ == "__main__":
    main()
