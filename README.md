# HIT-CampusAI: 哈工大（深圳）校园AI生活助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Star History Chart](https://api.star-history.com/svg?repos=HITech-AI/HIT-CampusAI&type=Date)](https://star-history.com/#HITech-AI/HIT-CampusAI&Date)

## 项目简介
HIT-CampusAI 是为**哈尔滨工业大学（深圳）** 师生打造的一站式校园AI生活助手，基于哈工大AI开发平台国产多模态大模型构建，聚焦解决**深圳校区**校园生活中的信息查询、事务办理、服务推荐等核心痛点。

核心目标：用轻量化AI技术提升**深圳校区**师生校园生活效率，降低信息获取成本，同时提供可复用的校园AI应用开发模板，助力高校智慧校园建设。

## 核心功能（深圳校区专属）
### 📖 校园信息智能问答
- **深圳校区**校历/选课/请假/报销等办事流程解答
- **深圳校区**图书馆馆藏查询、借阅规则解答
- **深圳校区**交通、食堂营业时间/菜单查询
### 🍽️ 个性化生活推荐
- **深圳校区**食堂美食推荐（基于口味偏好、用餐时段）
- **深圳校区**活动（讲座/竞赛/社团/招聘会）智能提醒与日历同步
### 🧠 轻量心理健康支持
- 情绪疏导、压力缓解科普话术库（非专业诊疗，仅辅助）
### 🎯 交互方式
- 文字交互（支持中文普通话）
- 网页端Demo（适配PC/移动端，**深圳校区专属**）

## 技术架构
```mermaid
graph TD
    A[用户输入] --> B[文本解析模块]
    B --> C[深圳校区知识库检索（FAISS）]
    C --> D[哈工大AI平台国产大模型推理]
    D --> E[结果格式化输出]
    E --> F[Streamlit网页端展示]