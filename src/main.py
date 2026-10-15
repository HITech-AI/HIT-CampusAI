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

# 标题与副标题
st.title("🏫 HIT-CampusAI 哈工大（深圳）校园AI生活助手")
st.subheader("一站式校园 AI 生活助手 · 深圳校区专属版")
st.divider()

# 侧边栏
with st.sidebar:
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
st.markdown("- 本项目由哈工大（深圳）师生开源维护，欢迎提交 Issue 与 PR")
st.markdown("- 知识库持续扩充，覆盖办事流程、图书馆、食堂、交通等校园场景")