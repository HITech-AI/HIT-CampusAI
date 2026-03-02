# src/knowledge/knowledge_base.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# 加载预训练的向量化模型
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_knowledge_base(file_path: str) -> list[str]:
    """
    从文本文件加载知识库
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 按章节分割知识库内容
    sections = content.split('## ')
    return [f"## {sec}" for sec in sections if sec.strip()]

def build_faiss_index(knowledge: list[str]) -> tuple[faiss.IndexFlatL2, np.ndarray]:
    """
    构建FAISS向量索引
    """
    # 将文本向量化
    embeddings = model.encode(knowledge)
    # 构建索引
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings

def retrieve_relevant_knowledge(query: str, index: faiss.IndexFlatL2, knowledge: list[str], top_k: int = 3) -> list[str]:
    """
    根据查询检索最相关的知识库内容
    """
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    return [knowledge[i] for i in indices[0]]