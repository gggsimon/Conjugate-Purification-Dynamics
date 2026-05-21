import re
import math
from typing import List, Tuple, Dict, Any


def calculate_gdi(prompt: str) -> float:
    """
    生成歧义指数(GDI) v1.3 修复版
    范围：0.0（完全确定）~ 1.0（完全歧义）
    最优生成区间：0.65 ~ 0.70

    核心设计原则：
    - 创意词大幅提升 GDI
    - 约束词轻微降低 GDI
    - 基础 Prompt GDI ≈ 0.35，让优化有足够提升空间
    """
    if not prompt.strip():
        return 0.0

    words = prompt.split()
    word_count = max(len(words), 1)

    # ===== 约束分量（大幅降低权重）=====
    strong_constraints = [
        "必须", "一定", "只能", "仅", "严格", "禁止", "不得", "不能",
        "不要", "避免", "绝不", "务必", "确保", "JSON", "表格", "列表",
        "字数", "长度", "不超过", "精确到"
    ]

    weak_constraints = [
        "根据", "按照", "遵循", "基于", "参考",
        "包括", "包含", "主要", "核心", "重点",
        "准确", "具体", "详细", "清晰", "明确"
    ]

    number_matches = re.findall(r'(\d+)\s*(个|点|步|条|项|字)', prompt)
    number_count = len(number_matches)

    strong_count = sum(1 for word in strong_constraints if word in prompt)
    weak_count = sum(1 for word in weak_constraints if word in prompt)

    # 大幅降低约束影响
    constraint_score = strong_count * 0.8 + weak_count * 0.3 + number_count * 1.0
    constraint_density = min(constraint_score / word_count * 0.15, 0.5)

    # ===== 歧义分量（大幅增加权重）=====
    creative_keywords = [
        "创意", "想象", "发挥", "自由", "多种", "不同",
        "可能", "也许", "大概", "尝试", "探索",
        "故事", "小说", "诗歌", "散文", "设计", "方案",
        "脑洞", "虚构", "幻想", "创作", "灵感", "风格", "视角"
    ]

    strong_creative = [
        "大胆", "开放", "突破", "创新", "独特", "原创", "天马行空"
    ]

    creative_count = sum(1 for word in creative_keywords if word in prompt)
    strong_creative_count = sum(1 for word in strong_creative if word in prompt)

    # 大幅提高创意影响
    freedom_density = min((creative_count + strong_creative_count * 1.5) / word_count * 1.0, 0.9)

    # 结构系数（越简单结构，创意空间越大）
    sentence_count = len(re.split(r'[。！？\n]+', prompt.strip()))
    if sentence_count <= 3:
        structure_coeff = 1.0
    elif sentence_count <= 6:
        structure_coeff = 0.9
    else:
        structure_coeff = max(0.6, 1.0 - (sentence_count - 6) * 0.08)

    # ===== 综合计算 =====
    base_gdi = 0.35  # 降低基准值，让创意修饰有更大提升空间
    gdi = base_gdi + (freedom_density * 0.8) - (constraint_density * 0.2)
    gdi = gdi * structure_coeff

    return round(max(0.0, min(1.0, gdi)), 2)


def add_creative_modifier(prompt: str, delta: float) -> str:
    """
    根据GDI差距动态添加不同强度的创意修饰词
    delta = target_gdi - current_gdi（正数，越大越需要创意）
    """
    modifiers = [
        (0.05, "请适当发挥创意"),
        (0.10, "请发挥创意，提供多种可能性"),
        (0.15, "请大胆想象，从不同角度思考"),
        (0.25, "请充分发挥创意，进行创新性的思考和表达"),
        (1.00, "请完全放开脑洞，进行天马行空的创作，越有新意越好")
    ]

    for threshold, modifier in modifiers:
        if delta <= threshold:
            return f"{prompt}\n\n{modifier}"

    return prompt


def add_constraint_modifier(prompt: str, delta: float) -> str:
    """
    根据GDI差距动态添加不同强度的约束修饰词
    delta = current_gdi - target_gdi（正数，越大越需要约束）
    注意：由于约束词权重很低，这里用温和的约束表述
    """
    modifiers = [
        (0.05, "请注重内容质量"),
        (0.10, "请基于事实回答，注重准确性"),
        (0.15, "请提供准确、可验证的信息"),
        (0.25, "请确保内容真实可靠，避免不实信息"),
        (1.00, "请陈述客观事实，信息准确，基于已知数据")
    ]

    for threshold, modifier in modifiers:
        if delta <= threshold:
            return f"{prompt}\n\n{modifier}"

    return prompt


def recursive_prompt_optimizer(
    prompt: str,
    target_gdi: float = 0.68,
    tolerance: float = 0.05,
    max_iterations: int = 5
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    基于GDI的递归Prompt优化器

    返回：最优Prompt + 完整优化历史
    """
    history = []
    current_prompt = prompt

    for i in range(max_iterations):
        current_gdi = calculate_gdi(current_prompt)
        delta = current_gdi - target_gdi

        action = "无"

        if abs(delta) <= tolerance:
            action = "已达最优"
        elif delta < 0:
            # 太保守（低于目标），加创意
            current_prompt = add_creative_modifier(current_prompt, abs(delta))
            action = "增加创意"
        else:
            # 太发散（高于目标），加约束
            current_prompt = add_constraint_modifier(current_prompt, abs(delta))
            action = "增加约束"

        history.append({
            "iteration": i + 1,
            "prompt": current_prompt,
            "gdi": current_gdi,
            "delta": delta,
            "action": action
        })

        if action == "已达最优":
            break

    return current_prompt, history


def test_real_prompts():
    """
    测试真实场景下的Prompt优化效果
    """
    test_prompts = [
        "写一篇关于人工智能未来的文章",
        "写一个Python函数实现快速排序",
        "介绍一下黑洞",
        "写一个奶茶店的营销文案",
        "解释一下什么是量子纠缠"
    ]

    print("=" * 70)
    print("真实Prompt优化测试 (v1.3)")
    print("=" * 70)

    for prompt in test_prompts:
        print(f"\n原始Prompt: {prompt}")
        original_gdi = calculate_gdi(prompt)
        print(f"原始GDI: {original_gdi:.2f}")

        optimized_prompt, history = recursive_prompt_optimizer(prompt)
        final_gdi = history[-1]["gdi"]
        delta = final_gdi - original_gdi

        print(f"优化后GDI: {final_gdi:.2f} ({delta:+.2f})")
        print(f"迭代次数: {len(history)}")

        for step in history:
            print(f"  第{step['iteration']}步: GDI={step['gdi']:.2f} | {step['action']}")

        print("-" * 70)


def test_modifier_effects():
    """
    测试修饰词对GDI的影响
    """
    print("=" * 70)
    print("修饰词效果测试")
    print("=" * 70)

    test_cases = [
        ("写一篇关于AI的文章", "原始"),
        ("写一篇关于AI的文章\n\n请适当发挥创意", "+创意1"),
        ("写一篇关于AI的文章\n\n请发挥创意，提供多种可能性", "+创意2"),
        ("写一篇关于AI的文章\n\n请大胆想象，从不同角度思考", "+创意3"),
    ]

    for prompt, label in test_cases:
        gdi = calculate_gdi(prompt)
        print(f"{label:15} GDI = {gdi:.2f}")

    print()


if __name__ == "__main__":
    test_modifier_effects()
    test_real_prompts()
