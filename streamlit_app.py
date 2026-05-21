import streamlit as st
import pandas as pd
from gdi_optimizer import calculate_gdi, recursive_prompt_optimizer


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
optimize_button = st.button("🚀 一键优化", type="primary", use_container_width=True)

st.divider()


# 结果展示区
if optimize_button and prompt.strip():
    with st.spinner("正在计算GDI并进行递归优化..."):
        original_gdi = calculate_gdi(prompt)
        
        optimized_prompt, history = recursive_prompt_optimizer(
            prompt, target_gdi, tolerance, max_iterations
        )
        
        final_gdi = history[-1]["gdi"]
        delta = final_gdi - original_gdi
        
        # 结果对比
        col1, col2 = st.columns(2)
        
        with col1:
            if original_gdi < 0.4:
                original_status = "过于死板"
            elif original_gdi < 0.6:
                original_status = "偏保守"
            elif original_gdi < 0.7:
                original_status = "已达最优"
            elif original_gdi < 0.9:
                original_status = "偏发散"
            else:
                original_status = "过于混乱"
            
            st.metric(
                label=f"原始 GDI ({original_status})",
                value=f"{original_gdi:.2f}",
                delta_color="off"
            )
            st.text_area("原始 Prompt", value=prompt, height=180, disabled=True)
        
        with col2:
            if abs(final_gdi - target_gdi) <= tolerance:
                final_status = "已达最优"
            elif final_gdi < target_gdi:
                final_status = "仍偏保守"
            else:
                final_status = "仍偏发散"
            
            st.metric(
                label=f"优化后 GDI ({final_status})",
                value=f"{final_gdi:.2f}",
                delta=f"{delta:+.2f}"
            )
            st.text_area("优化后 Prompt", value=optimized_prompt, height=180)
            
            # 一键复制按钮
            st.copy_button(
                "📋 复制优化后Prompt",
                data=optimized_prompt,
                type="secondary",
                use_container_width=True
            )
        
        st.divider()
        
        # 优化过程可视化
        st.subheader("📈 优化过程")
        
        history_df = pd.DataFrame(history)
        st.line_chart(
            history_df,
            x="iteration",
            y="gdi",
            use_container_width=True,
            color="#FF4B4B"
        )
        
        with st.expander("查看详细优化步骤"):
            for i, step in enumerate(history):
                st.write(f"**第 {step['iteration']} 步**")
                st.write(f"- GDI: {step['gdi']:.2f}")
                st.write(f"- 动作: {step['action']}")
                st.code(step['prompt'], language="text")
                if i < len(history) - 1:
                    st.divider()


# 页脚
st.divider()
st.caption("""
基于生成歧义指数(GDI)理论 | 开源地址： `https://github.com/guodongmin/cpd-alignment` 
""")
