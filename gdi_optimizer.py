import streamlit as st
import pandas as pd
from gdi_optimizer import calculate_gdi, recursive_prompt_optimizer

# 页面配置
st.set_page_config(
    page_title="GDI Prompt优化器",
    page_icon="🎯",
    layout="wide"
)

# 初始化会话状态
if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt = ""
if 'current_result' not in st.session_state:
    st.session_state.current_result = ""
if 'optimized_prompt' not in st.session_state:
    st.session_state.optimized_prompt = ""

# 标题
st.title("🎯 GDI Prompt优化器")
st.caption("基于生成歧义指数(GDI)理论的智能Prompt优化工具")

# 场景模板
templates = {
    "小说创作": "写一篇关于[主题]的小说，包含生动的人物描写和情节发展",
    "代码生成": "写一个[语言]函数实现[功能]，包含详细注释",
    "文案撰写": "为[产品/服务]写一段营销文案，突出核心卖点",
    "知识问答": "详细解释[概念]，包括定义、原理和应用场景",
    "创意写作": "发挥想象，创作一个关于[主题]的创意故事"
}

# 参数设置
with st.expander("⚙️ 参数设置", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        target_gdi = st.slider("目标GDI值", min_value=0.5, max_value=0.8, value=0.68, step=0.01)
    with col2:
        tolerance = st.slider("容差范围", min_value=0.01, max_value=0.1, value=0.05, step=0.01)
    with col3:
        max_iterations = st.slider("最大迭代次数", min_value=3, max_value=10, value=5)

# 输入区域
st.subheader("📝 输入Prompt")
selected_template = st.selectbox("选择场景模板", list(templates.keys()), index=0)
template_prompt = templates[selected_template]
prompt = st.text_area("输入你的Prompt", value=template_prompt, height=150)

# 按钮区域
col1, col2 = st.columns([1, 4])
with col1:
    optimize_button = st.button("🚀 优化Prompt", use_container_width=True)
with col2:
    regenerate_button = st.button("🔄 继续优化", use_container_width=True, disabled=not st.session_state.current_prompt)

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


def simulate_ai_response(prompt: str) -> str:
    """
    根据Prompt类型生成模拟AI响应
    """
    if "小说" in prompt or "故事" in prompt:
        return generate_novel_content(prompt)
    elif "代码" in prompt or "函数" in prompt:
        return generate_code_content(prompt)
    elif "文案" in prompt or "营销" in prompt:
        return generate_copywriting_content(prompt)
    elif "解释" in prompt or "介绍" in prompt or "问答" in prompt:
        return generate_explanation_content(prompt)
    else:
        return generate_general_content(prompt)


def generate_novel_content(prompt: str) -> str:
    return """在家人们的鼓励和支持下，阿福渐渐长大。他虽然学得慢，但学得扎实。小学时，班主任王老师发现了他对数学的特殊天赋，开始悉心辅导他。初中时，同桌小美成了他最好的朋友，也是第一个不嘲笑他的同龄人。

阿福的数学成绩越来越好，甚至在全市数学竞赛中获得了三等奖。这个成绩对于别人来说可能不算什么，但对于阿福来说，却是他笨拙人生中的第一个高光时刻。

故事还在继续...

---
创作风格：【严谨写实】注重细节描写，人物刻画真实可信，情节发展符合现实逻辑"""


def generate_code_content(prompt: str) -> str:
    return """```python
def quick_sort(arr):
    \"\"\"
    快速排序算法实现
    
    参数:
        arr (list): 待排序的列表
    
    返回:
        list: 排序后的列表
    \"\"\"
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

# 测试
if __name__ == "__main__":
    test_arr = [3, 6, 8, 10, 1, 2, 1]
    print(quick_sort(test_arr))  # 输出: [1, 1, 2, 3, 6, 8, 10]
