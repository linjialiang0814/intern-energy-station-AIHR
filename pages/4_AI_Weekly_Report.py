import streamlit as st

from services.data_service import get_dashboard_summary
from services.report_service import generate_report_outline, generate_weekly_report


st.set_page_config(page_title="AI 周报生成", layout="wide")

st.title("AI 周报生成")
st.caption("把看板中的群体数据自动整理成 HR 可发送、可复盘的管理周报。")

summary = get_dashboard_summary()
metrics = summary["metrics"]

metric_cols = st.columns(5)
metric_cols[0].metric("实习生总数", metrics["total_interns"])
metric_cols[1].metric("高潜", metrics["high_potential_count"])
metric_cols[2].metric("风险预警", metrics["risk_count"])
metric_cols[3].metric("平均适岗分", metrics["avg_fit_score"])
metric_cols[4].metric("反馈覆盖率", f"{metrics['mentor_feedback_rate']}%")

st.divider()

outline = generate_report_outline(summary)
left, right = st.columns([0.8, 1.2])

with left:
    st.subheader("结构化周报要点")
    for title, items in outline.items():
        with st.expander(title, expanded=True):
            for item in items:
                st.markdown(f"- {item}")

with right:
    st.subheader("自动生成周报")
    report = generate_weekly_report(summary)
    st.text_area("周报正文", value=report, height=420)
    st.download_button(
        "下载周报 Markdown",
        data=report,
        file_name="intern_weekly_report.md",
        mime="text/markdown",
    )

st.info("当前版本使用规则与模板生成稳定周报；后续接入 LLM 后，可把同一份结构化数据交给模型润色和扩写。")
