# src/main.py
import streamlit as st
from pathlib import Path
from src.knowledge.knowledge_base import load_knowledge_base, build_faiss_index, retrieve_relevant_knowledge
from src.api.llm_api import hit_llm_inference

# 页面基础配置
st.set_page_config(
    page_title="HIT-CampusAI 哈工大（深圳）校园AI生活助手",
    page_icon="🏫",
    layout="wide"
)

# 初始化知识库（只在首次加载时执行）
@st.cache_resource
def init_knowledge():
    knowledge_file = Path("src/knowledge/shenzhen_knowledge.txt")
    if not knowledge_file.exists():
        st.error("知识库文件不存在，请检查路径！")
        return None, None
    knowledge = load_knowledge_base(str(knowledge_file))
    index, _ = build_faiss_index(knowledge)
    return knowledge, index

knowledge, index = init_knowledge()

# 标题与大赛信息
st.title("🏫 HIT-CampusAI 哈工大（深圳）校园AI生活助手")
st.subheader("哈尔滨工业大学AI智能创新大赛 · 校园创意赛道 | 深圳校区专属版")
st.divider()

# 侧边栏
with st.sidebar:
    st.markdown("### 📅 大赛进度")
    st.markdown("✅ 2026.03.02 完成报名与知识库构建")
    st.markdown("🔨 2026.04.15 前 完成中期版本开发")
    st.markdown("### 📌 核心功能")
    st.markdown("- 深圳校区智能问答（核心）")
    st.markdown("- 食堂/商业配套推荐")
    st.markdown("- 校园地图导航")

# 核心交互区
st.markdown("### 💬 深圳校区校园问题咨询")
user_question = st.text_input(
    "请输入你的问题（例如：深圳大学城图书馆怎么借书？）",
    placeholder="输入后点击提交即可体验智能问答～"
)

if st.button("提交查询", type="primary"):
    if user_question and knowledge and index:
        with st.spinner("正在检索深圳校区知识库..."):
            # 1. 检索相关知识
            relevant_docs = retrieve_relevant_knowledge(user_question, index, knowledge)
            context = "\n".join(relevant_docs)
            
            # 2. 构建提示词
            prompt = f"""
            你是哈工大（深圳）的校园AI助手，请根据以下知识库信息，准确回答用户的问题。
            如果知识库中没有相关信息，请如实告知。

            知识库信息：
            {context}

            用户问题：
            {user_question}
            """
            
            # 3. 调用大模型
            answer = hit_llm_inference(prompt)
            
            # 4. 显示结果
            st.success(f"【深圳校区专属回答】")
            st.write(answer)
    else:
        st.warning("请输入问题后再提交～")

# 底部说明
st.divider()
st.markdown("#### 📝 说明")
st.markdown("- 本项目为哈工大AI大赛参赛作品，单人开发（一人成军）")
st.markdown("- 中期版本（2026.04.15）将上线完整的智能问答与生活推荐功能")