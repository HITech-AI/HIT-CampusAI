import streamlit as st

# 页面基础配置
st.set_page_config(
    page_title="HIT-CampusAI 校园AI生活助手",
    page_icon="🏫",
    layout="wide"
)

# 标题与大赛信息
st.title("🏫 HIT-CampusAI 哈工大校园AI生活助手")
st.subheader("哈尔滨工业大学AI智能创新大赛 · 校园创意赛道")
st.divider()

# 侧边栏（大赛进度+功能说明）
with st.sidebar:
    st.markdown("### 📅 大赛进度")
    st.markdown("✅ 2026.03.02 完成报名")
    st.markdown("🔨 2026.03.15 前 完成基础界面开发")
    st.markdown("### 📌 功能预告")
    st.markdown("- 校园智能问答（核心）")
    st.markdown("- 食堂美食推荐")
    st.markdown("- 校园活动提醒")

# 核心交互区（基础演示版）
st.markdown("### 💬 校园问题咨询（演示版）")
user_question = st.text_input(
    "请输入你的校园问题（例如：哈工大图书馆借阅规则？）",
    placeholder="输入后点击提交即可体验基础交互～"
)

if st.button("提交查询", type="primary"):
    if user_question:
        with st.spinner("正在检索校园知识库..."):
            # 演示版：固定回复，后续替换为真实问答逻辑
            st.success(f"【演示版】已收到你的问题：{user_question}")
            st.info("核心问答功能正在开发中，4月15日中期版本将上线完整能力！")
    else:
        st.warning("请输入问题后再提交～")

# 底部说明
st.divider()
st.markdown("#### 📝 说明")
st.markdown("- 本项目为哈工大AI大赛参赛作品，单人开发（一人成军）")
st.markdown("- 中期版本（2026.04.15）将上线完整的校园问答、食堂推荐功能")