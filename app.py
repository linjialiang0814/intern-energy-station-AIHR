import streamlit as st

from services.auth_service import render_role_selector, role_permission_summary
from services.data_service import get_dashboard_summary


st.set_page_config(
    page_title="实习能量站",
    page_icon="⚡",
    layout="wide",
)


summary = get_dashboard_summary()
metrics = summary["metrics"]
role = render_role_selector()

st.title("实习能量站")
st.subheader("AI 驱动的业务部实习生成长导航智能看板")

st.markdown(
    """
这个 Demo 面向 **HR、业务导师、实习生、招聘同学** 四类角色，围绕“看清现状、识别风险、给出行动”三件事展开。

当前版本先完成可演示主干：

- HR 总览看板：查看 20 名实习生整体进度、适岗分布和风险预警。
- 实习生个人画像：查看个人任务进展、能力评分、风险原因和下一步建议。
- 导师带教助手：把自然语言反馈转成结构化评价和带教动作。
- 实习生成长助手：按岗位、周次和短板生成本周成长建议。
- AI 周报生成：把群体数据整理成 HR 可发送的管理周报。
- 规则判断底座：用可解释评分模型支撑适岗度和风险等级。
"""
)

st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("实习生总数", metrics["total_interns"])
col2.metric("高潜人数", metrics["high_potential_count"])
col3.metric("需关注/高风险", metrics["risk_count"])
col4.metric("平均适岗分", metrics["avg_fit_score"])

st.subheader("推荐演示路径")
demo_steps = [
    ("1. HR Dashboard", "查看整体态势、风险分布、适岗排名，并导出看板摘要。"),
    ("2. Intern Profile", "选择一个风险实习生，解释适岗分来源、风险原因和行动建议。"),
    ("3. Mentor Assistant", "输入导师反馈，生成结构化分析和带教动作。"),
    ("4. Intern Growth Assistant", "模拟实习生提问，生成本周成长计划。"),
    ("5. AI Weekly Report", "生成 HR 周报，并下载 Markdown。"),
]
for title, desc in demo_steps:
    st.markdown(f"- **{title}**：{desc}")

st.info("当前版本支持火山方舟 LLM 增强；未配置 API Key 时会自动使用规则模板 fallback，保证 Demo 稳定可演示。")

st.subheader("角色视角与权限模拟")
st.write(f"当前模拟角色：**{role}**。这是一套演示用视角控制，不等同于真实登录鉴权。")
st.dataframe(role_permission_summary(), use_container_width=True, hide_index=True)
