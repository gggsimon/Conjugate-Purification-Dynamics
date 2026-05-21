import streamlit as st
import pandas as pd
from gdi_optimizer import calculate_gdi, recursive_prompt_optimizer


# 模拟AI生成（根据Prompt类型生成真实内容）
def simulate_ai_response(prompt: str) -> str:
    """根据Prompt类型生成真实的响应内容"""
    gdi = calculate_gdi(prompt)
    
    # 小说/故事类Prompt
    if any(keyword in prompt for keyword in ["小说", "故事", "短篇", "自传", "写一本", "写一个"]):
        return generate_novel_content(prompt, gdi)
    
    # 代码类Prompt
    elif any(keyword in prompt for keyword in ["Python", "函数", "代码", "爬虫", "实现"]):
        return generate_code_content(prompt, gdi)
    
    # 事实查询类Prompt
    elif any(keyword in prompt for keyword in ["介绍", "解释", "什么是", "历史", "发展"]):
        return generate_fact_content(prompt, gdi)
    
    # 营销文案类Prompt
    elif any(keyword in prompt for keyword in ["营销", "文案", "促销", "广告"]):
        return generate_marketing_content(prompt, gdi)
    
    # 默认响应
    else:
        return generate_default_content(prompt, gdi)


def generate_novel_content(prompt: str, gdi: float) -> str:
    """生成小说类内容"""
    story_start = """【小说创作】\n\n**《笨小孩的春天》第一章·萌芽**\n\n村口的老槐树下，七岁的阿福蹲在地上，用树枝在泥土上画着歪歪扭扭的圆圈。阳光透过斑驳的树叶，在他沾满泥土的脸上投下细碎的光斑。\n\n\"阿福，回家吃饭咯！\"母亲的声音从远处传来，带着一丝疲惫却温柔的笑意。\n\n阿福抬起头，那张算不上俊朗的脸上露出憨厚的笑容。他从小就知道，自己和别的孩子不一样——学东西总是比别人慢半拍，连说话都比同龄孩子晚了两年。村里的孩子们常常嘲笑他，给他起各种难听的外号。\n\n但阿福从不觉得自己笨。他只是需要更多的时间，更多的耐心。就像父亲教他种庄稼时说的那样：\"每颗种子发芽的时间都不一样，你得等。\"\n\n在家人们的鼓励和支持下，阿福渐渐长大。他虽然学得慢，但学得扎实。小学时，班主任王老师发现了他对数学的特殊天赋，开始悉心辅导他。初中时，同桌小美成了他最好的朋友，也是第一个不嘲笑他的同龄人。\n\n故事还在继续...\n\n---\n📖 创作风格："""
    
    if gdi < 0.4:
        style = "【严谨写实】注重细节描写，人物刻画真实可信，情节发展符合现实逻辑"
    elif gdi < 0.6:
        style = "【温情现实主义】真实与温情并存，既有生活质感又不失希望"
    elif gdi < 0.8:
        style = "【略带浪漫】在真实的基础上加入适度的艺术加工和想象"
    else:
        style = "【充满想象力】突破现实束缚，加入奇幻元素和戏剧性转折"
    
    return story_start + style


def generate_code_content(prompt: str, gdi: float) -> str:
    """生成代码类内容"""
    return f"""【代码实现】\n\n```python
def batch_rename_images(folder_path):
    \"\"\"
    批量重命名文件夹中的图片文件
    :param folder_path: 图片文件夹路径
    \"\"\"
    import os
    
    # 获取文件夹中的所有文件
    files = [f for f in os.listdir(folder_path) 
             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    # 按创建时间排序
    files.sort(key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    
    # 批量重命名
    for i, filename in enumerate(files, 1):
        ext = os.path.splitext(filename)[1]
        new_name = f\"image_{i:04d}{ext}\"
        os.rename(
            os.path.join(folder_path, filename),
            os.path.join(folder_path, new_name)
        )
        print(f\"已重命名: {filename} -> {new_name}\")

# 使用示例
if __name__ == \"__main__\":
    batch_rename_images(\"./photos/\")
```\n\n---\n💻 代码风格：{'【严格规范】' if gdi < 0.6 else '【灵活实现】'} 注重可读性和代码质量"""


def generate_fact_content(prompt: str, gdi: float) -> str:
    """生成事实查询类内容"""
    return f"""【知识科普】\n\n**人工智能发展简史**\n\n人工智能的概念最早可以追溯到1956年的达特茅斯会议，这次会议被认为是AI领域的开端。\n\n**发展阶段：**\n\n1. **萌芽期（1956-1974）**\n   - 符号主义AI兴起\n   - 早期专家系统开发\n   - 自然语言处理初步探索\n\n2. **低谷期（1974-1980）**\n   - 计算能力不足\n   - 期望过高导致资金削减\n   - AI寒冬到来\n\n3. **复兴期（1980-1993）**\n   - 专家系统商业化\n   - 机器学习算法发展\n   - 神经网络研究复苏\n\n4. **爆发期（2010-至今）**\n   - 深度学习革命\n   - 大语言模型出现\n   - AI应用广泛普及\n\n---\n📚 内容特点：{'【客观严谨】' if gdi < 0.6 else '【通俗易懂】'} 信息准确，来源可靠"""


def generate_marketing_content(prompt: str, gdi: float) -> str:
    """生成营销文案类内容"""
    return f"""【营销文案】\n\n**🍹 夏日限定｜冰爽果茶清凉来袭！**\n\n🌞 这个夏天，让味蕾来一场清凉之旅！\n\n✨ **产品亮点：**\n\n🍇 精选当季新鲜水果\n每一口都是阳光的味道，选用海南金煌芒、台湾凤梨、广东荔枝，产地直采，新鲜直达！\n\n❄️ 独家冰沙工艺\n-18度低温研磨，保留水果原有营养，口感细腻绵密，冰爽到心底！\n\n💖 颜值与实力并存\nINS风渐变杯身，随手一拍都是大片，发朋友圈秒获点赞！\n\n🔥 **限时活动：**\n- 买一送一（限前100名）\n- 第二杯半价\n- 小红书打卡返现10元\n\n📍 地址：XX路XX号\n⏰ 营业时间：10:00-22:00\n\n---\n🎯 文案风格：{'【直接务实】' if gdi < 0.6 else '【创意吸睛】'} 突出卖点，激发购买欲"""


def generate_default_content(prompt: str, gdi: float) -> str:
    """默认内容生成"""
    return f"""【智能响应】\n\n关于「{prompt[:50]}...」的回答：\n\n根据你的需求，我将提供相应的解答。\n\n主要内容包括：\n1. 核心问题分析\n2. 详细解答说明\n3. 相关建议和补充信息\n\n---\n💡 响应风格：{'【严谨准确】' if gdi < 0.6 else '【灵活多样】'} 基于事实，兼顾创意"""


# 页面配置
st.set_page_config(
    page_title="GDI Prompt 校准器",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# 标题
st.title("⚛️ GDI Prompt 校准器")
st.caption("基于生成歧义指数的AI生成质量量化与优化工具 | 黄金生成值 ≈ 0.68")

st.divider()


# 预设场景模板
st.subheader("快速开始：选择场景模板")
scene_templates = {
    "自定义": "",
    "创意写作": "写一个关于时间旅行的短篇故事，主角是一个图书馆管理员",
    "代码生成": "写一个Python函数，实现批量重命名文件夹中的图片文件",
    "事实查询": "介绍一下人工智能的发展历史，从1950年到2026年",
    "营销文案": "写一个夏季冰饮的促销文案，适合发在小红书",
    "教育辅导": "给初中生解释什么是牛顿第一定律，举3个生活中的例子",
    "邮件写作": "写一封给客户的跟进邮件，询问项目合作意向"
}


selected_scene = st.selectbox("选择场景", list(scene_templates.keys()))
default_prompt = scene_templates[selected_scene]

# 主输入区
prompt = st.text_area(
    "输入你的 Prompt",
    height=150,
    value=default_prompt,
    placeholder="例如：写一篇关于人工智能未来发展趋势的文章\n\n提示：越具体的原始prompt，优化效果越好"
)

# 参数设置区
col1, col2, col3 = st.columns(3)
with col1:
    target_gdi = st.slider("目标 GDI 值", 0.0, 1.0, 0.68, 0.01,
                          help="0.65-0.70为通用最优区间；代码生成建议0.60-0.65；创意写作为0.70-0.75")
with col2:
    tolerance = st.slider("容差范围", 0.01, 0.1, 0.05,
                         help="允许GDI与目标值的最大偏差")
with col3:
    max_iterations = st.slider("最大迭代次数", 1, 10, 5,
                              help="最多进行多少次优化调整")

# 优化按钮
col1, col2 = st.columns(2)
with col1:
    optimize_button = st.button("🚀 一键优化", type="primary", use_container_width=True)
with col2:
    regenerate_button = st.button("🔄 继续优化（基于结果）", use_container_width=True)

st.divider()


# 全局状态管理
if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt = ""
if 'current_result' not in st.session_state:
    st.session_state.current_result = ""
if 'optimized_prompt' not in st.session_state:
    st.session_state.optimized_prompt = ""


# 结果展示区
if optimize_button and prompt.strip():
    with st.spinner("正在计算GDI并进行递归优化..."):
        original_gdi = calculate_gdi(prompt)
        
        optimized_prompt, history = recursive_prompt_optimizer(
            prompt, target_gdi, tolerance, max_iterations
        )
        
        final_gdi = history[-1]["gdi"]
        delta = final_gdi - original_gdi
        
        # 保存到状态
        st.session_state.current_prompt = prompt
        st.session_state.optimized_prompt = optimized_prompt
        
        # 生成模拟结果
        original_result = simulate_ai_response(prompt)
        optimized_result = simulate_ai_response(optimized_prompt)
        
        # 计算结果的GDI值
        original_result_gdi = calculate_gdi(original_result)
        optimized_result_gdi = calculate_gdi(optimized_result)
        
        # Prompt对比
        st.subheader("📝 Prompt 对比")
        col1, col2 = st.columns(2)
        
        with col1:
            status = "过于死板" if original_gdi < 0.4 else "偏保守" if original_gdi < 0.6 else "已达最优" if original_gdi < 0.7 else "偏发散" if original_gdi < 0.9 else "过于混乱"
            st.metric(label=f"原始 GDI ({status})", value=f"{original_gdi:.2f}", delta_color="off")
            st.text_area("原始 Prompt", value=prompt, height=180, disabled=True)
        
        with col2:
            status = "已达最优" if abs(final_gdi - target_gdi) <= tolerance else "仍偏保守" if final_gdi < target_gdi else "仍偏发散"
            st.metric(label=f"优化后 GDI ({status})", value=f"{final_gdi:.2f}", delta=f"{delta:+.2f}")
            st.text_area("优化后 Prompt", value=optimized_prompt, height=180)
            st.download_button("📋 复制优化后Prompt", data=optimized_prompt, file_name="optimized_prompt.txt", mime="text/plain", use_container_width=True)
        
        st.divider()
        
        # 生成结果对比
        st.subheader("🤖 生成结果对比")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(label=f"原始结果 GDI", value=f"{original_result_gdi:.2f}", delta_color="off")
            st.text_area("原始Prompt生成结果", value=original_result, height=250, disabled=True)
            st.download_button("📋 复制原始结果", data=original_result, file_name="original_result.txt", mime="text/plain", use_container_width=True)
        
        with col2:
            result_delta = optimized_result_gdi - original_result_gdi
            st.metric(label=f"优化后结果 GDI", value=f"{optimized_result_gdi:.2f}", delta=f"{result_delta:+.2f}")
            st.text_area("优化后Prompt生成结果", value=optimized_result, height=250, disabled=True)
            st.download_button("📋 复制优化后结果", data=optimized_result, file_name="optimized_result.txt", mime="text/plain", use_container_width=True)
        
        st.divider()
        
        # 优化过程可视化
        st.subheader("📈 优化过程")
        history_df = pd.DataFrame(history)
        st.line_chart(history_df, x="iteration", y="gdi", use_container_width=True, color="#FF4B4B")
        
        with st.expander("查看详细优化步骤"):
            for i, step in enumerate(history):
                st.write(f"**第 {step['iteration']} 步**")
                st.write(f"- GDI: {step['gdi']:.2f}")
                st.write(f"- 动作: {step['action']}")
                st.code(step['prompt'], language="text")
                if i < len(history) - 1:
                    st.divider()


# 继续优化功能
elif regenerate_button and st.session_state.current_prompt:
    with st.spinner("正在基于结果继续优化..."):
        # 使用优化后的prompt作为基础，继续优化
        current_opt_prompt = st.session_state.optimized_prompt if st.session_state.optimized_prompt else st.session_state.current_prompt
        
        # 再次优化
        new_optimized_prompt, history = recursive_prompt_optimizer(
            current_opt_prompt, target_gdi, tolerance/2, max_iterations
        )
        
        final_gdi = history[-1]["gdi"]
        
        # 更新状态
        st.session_state.optimized_prompt = new_optimized_prompt
        
        # 生成新结果
        new_result = simulate_ai_response(new_optimized_prompt)
        new_result_gdi = calculate_gdi(new_result)
        
        st.subheader("🔄 继续优化结果")
        col1, col2 = st.columns(2)
        
        with col1:
            prev_gdi = calculate_gdi(current_opt_prompt)
            st.metric(label=f"上次优化后 GDI", value=f"{prev_gdi:.2f}", delta_color="off")
            st.text_area("上次优化后 Prompt", value=current_opt_prompt, height=180, disabled=True)
        
        with col2:
            delta = final_gdi - prev_gdi
            st.metric(label=f"再次优化后 GDI", value=f"{final_gdi:.2f}", delta=f"{delta:+.2f}")
            st.text_area("再次优化后 Prompt", value=new_optimized_prompt, height=180)
            st.download_button("📋 复制最终Prompt", data=new_optimized_prompt, file_name="final_prompt.txt", mime="text/plain", use_container_width=True)
        
        st.divider()
        
        st.subheader("🎯 最新生成结果")
        st.metric(label=f"最终结果 GDI", value=f"{new_result_gdi:.2f}")
        st.text_area("最新生成结果", value=new_result, height=250, disabled=True)
        st.download_button("📋 复制生成结果", data=new_result, file_name="generated_result.txt", mime="text/plain", use_container_width=True)


# 页脚
st.divider()
st.caption("""
基于生成歧义指数(GDI)理论 | 开源地址：`https://github.com/guodongmin/cpd-alignment`
""")
