import re
import math
from typing import List, Tuple, Dict, Any


def calculate_gdi(prompt: str) -> float:
    """
    生成歧义指数(GDI) v1.1 最终版
    范围：0.0（完全确定）~ 1.0（完全歧义）
    最优生成区间：0.65 ~ 0.70
    """
    if not prompt.strip():
        return 0.0

    words = prompt.split()
    word_count = max(len(words), 1)

    # 约束分量（分级权重）
    strong_constraints = [
        "必须", "一定", "只能", "仅", "严格", "禁止", "不得", "不能",
        "不要", "避免", "绝不", "务必", "确保", "仅仅",
        "JSON格式", "表格形式", "列表形式", "分点说明", "步骤清晰",
        "精确到", "保留", "小数点后", "字数", "长度", "不超过"
    ]

    weak_constraints = [
        "根据", "按照", "遵循", "基于", "参考", "例如", "比如",
        "包括", "包含", "主要", "核心", "重点", "关键", "简洁",
        "高效", "准确", "具体", "详细", "清晰", "明确", "客观"
    ]

    number_matches = re.findall(r'(\d+)\s*(个|点|步|条|项|字|分钟|小时)', prompt)
    number_constraint_count = len(number_matches)

    strong_count = sum(1 for word in strong_constraints if word in prompt)
    weak_count = sum(1 for word in weak_constraints if word in prompt)

    constraint_score = (
        strong_count * 2.0 +
        weak_count * 0.8 +
        number_constraint_count * 3.0
    )

    constraint_density = min(constraint_score / word_count * 0.5, 1.0)

    # 歧义分量（生成自由度）
    freedom_keywords = [
        "创意", "想象", "发挥", "自由", "任意", "多种", "不同",
        "可能", "也许", "大概", "可以", "能够", "尝试", "探索",
        "故事", "小说", "诗歌", "散文", "设计", "方案", "想法",
        "脑洞", "虚构", "幻想", "创作", "灵感", "风格", "视角"
    ]

    freedom_count = sum(1 for word in freedom_keywords if word in prompt)
    freedom_density = min(freedom_count / word_count * 1.2, 1.0)

    # 结构系数
    sentence_count = len(re.split(r'[。！？\n]+', prompt.strip()))
    if sentence_count <= 2:
        structure_coeff = 0.6 + sentence_count * 0.2
    elif sentence_count <= 7:
        structure_coeff = 1.0
    else:
        structure_coeff = max(0.5, 1.0 - (sentence_count - 7) * 0.05)

    # 综合计算
    base_gdi = 0.5
    gdi = base_gdi + (freedom_density * 0.4) - (constraint_density * 0.5)
    gdi = gdi * structure_coeff

    return round(max(0.0, min(1.0, gdi)), 2)


def add_creative_modifier(prompt: str, delta: float) -> str:
    """
    根据GDI差距动态添加不同强度的创意修饰词
    """
    modifiers = [
        (0.05, "请适当发挥创意"),
        (0.15, "请发挥创意，提供多种可能性"),
        (0.30, "请大胆想象，从不同角度思考，不要局限于常规答案"),
        (1.00, "请完全放开脑洞，进行天马行空的创作，越有新意越好")
    ]

    for threshold, modifier in modifiers:
        if delta <= threshold:
            return f"{prompt}\n\n{modifier}"

    return prompt


def add_constraint_modifier(prompt: str, delta: float) -> str:
    """
    根据GDI差距动态添加不同强度的约束修饰词
    """
    modifiers = [
        (0.05, "请尽量准确客观"),
        (0.15, "请严格按事实回答，避免猜测"),
        (0.30, "请提供准确可验证的信息，基于已知事实，不要虚构内容"),
        (1.00, "请只陈述事实，不要添加任何主观判断或推测，确保信息100%准确")
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
            current_prompt = add_creative_modifier(current_prompt, abs(delta))
            action = "增加创意"
        else:
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


if __name__ == "__main__":
    test_prompts = [
        "写一篇关于人工智能未来的文章",
        "写一个Python函数实现快速排序",
        "介绍一下黑洞",
        "写一个奶茶店的营销文案",
        "解释一下什么是量子纠缠"
    ]
    
    for prompt in test_prompts:
        print(f"原始Prompt: {prompt}")
        print(f"原始GDI: {calculate_gdi(prompt):.2f}")
        optimized, _ = recursive_prompt_optimizer(prompt)
        print(f"优化后GDI: {calculate_gdi(optimized):.2f}")
        print("-" * 50)
