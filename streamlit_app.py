import streamlit as st
import pandas as pd
from gdi_optimizer import calculate_gdi, recursive_prompt_optimizer


# 模拟AI生成（用于演示）
def simulate_ai_response(prompt: str) -> str:
    """模拟AI生成响应，基于prompt的GDI值调整输出风格"""
    gdi = calculate_gdi(prompt)
    
    if gdi < 0.4:
        return f"【精确回答模式】\n\n根据你的要求，我将提供准确、客观的信息：\n\n这是一个关于「{prompt[:30]}...」的回答。由于约束较强，回答将严格遵循事实，不添加额外内容。\n\n要点：\n1. 核心事实陈述\n2. 可验证的数据\n3. 简洁明了的表述"
    elif gdi < 0.6:
        return f"【平衡回答模式】\n\n关于「{prompt[:30]}...」，这里是我的回答：\n\n根据要求，我将提供既准确又有一定创造性的内容。\n\n主要内容：\n1. 核心信息概述\n2. 适当的扩展说明\n3. 保持客观中立的态度"
    elif gdi < 0.8:
        return f"【创意回答模式】\n\n关于「{prompt[:30]}...」，我有以下想法：\n\n在保证准确性的基础上，我将发挥创意，提供多种可能性：\n\n内容方向：\n1. 主要观点阐述\n2. 多角度思考\n3. 适当的想象和发挥\n4. 保持合理的边界"
    else:
        return f"【自由创作模式】\n\n关于「{prompt[:30]}...」，让我展开想象：\n\n由于自由度较高，我将进行更自由的创作：\n\n创作内容：\n1. 丰富的想象空间\n2. 多样化的可能性\n3. 打破常规的思路\n4. 充满创意的表达"


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
        
        with col2:
            result_delta = optimized_result_gdi - original_result_gdi
            st.metric(label=f"优化后结果 GDI", value=f"{optimized_result_gdi:.2f}", delta=f"{result_delta:+.2f}")
            st.text_area("优化后Prompt生成结果", value=optimized_result, height=250, disabled=True)
        
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


# 页脚
st.divider()
st.caption("""
基于生成歧义指数(GDI)理论 | 开源地址：`https://github.com/guodongmin/cpd-alignment`
""")
