import pandas as pd
import streamlit as st

from services.data_service import get_dashboard_summary


st.set_page_config(page_title="HR Dashboard", layout="wide")

summary = get_dashboard_summary()
metrics = summary["metrics"]
dataset = summary["dataset"]
role_summary = summary["role_summary"]
risk_distribution = summary["risk_distribution"]
level_distribution = summary["level_distribution"]

st.title("HR 总览看板")
st.caption("从 20 名实习生的任务进展、适岗评分和风险标签中，快速定位需要跟进的人和动作。")

metric_cols = st.columns(7)
metric_cols[0].metric("总人数", metrics["total_interns"])
metric_cols[1].metric("高潜", metrics["high_potential_count"])
metric_cols[2].metric("稳定", metrics["stable_count"])
metric_cols[3].metric("风险预警", metrics["risk_count"])
metric_cols[4].metric("平均任务分", metrics["avg_task_score"])
metric_cols[5].metric("平均适岗分", metrics["avg_fit_score"])
metric_cols[6].metric("导师反馈率", f"{metrics['mentor_feedback_rate']}%")

st.divider()

left, right = st.columns([1.1, 1])

with left:
    st.subheader("岗位表现概览")
    st.dataframe(
        role_summary.rename(
            columns={
                "role": "岗位",
                "interns": "人数",
                "avg_task_score": "平均任务分",
                "avg_fit_score": "平均适岗分",
                "risk_cases": "风险人数",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    chart_data = role_summary.set_index("role")[["avg_task_score", "avg_fit_score"]]
    st.bar_chart(chart_data)

with right:
    st.subheader("风险与适岗分布")
    risk_chart = risk_distribution.rename(columns={"risk_level": "风险等级", "count": "人数"}).set_index("风险等级")
    level_chart = level_distribution.rename(columns={"level": "适岗等级", "count": "人数"}).set_index("适岗等级")
    st.write("风险等级分布")
    st.bar_chart(risk_chart)
    st.write("适岗等级分布")
    st.bar_chart(level_chart)

st.divider()

rank_left, rank_right = st.columns(2)

with rank_left:
    st.subheader("Top 5 高潜实习生")
    top_table = summary["top_interns"][
        ["name", "role", "mentor_name", "fit_score", "level", "risk_level"]
    ].rename(
        columns={
            "name": "姓名",
            "role": "岗位",
            "mentor_name": "导师",
            "fit_score": "适岗分",
            "level": "适岗等级",
            "risk_level": "风险等级",
        }
    )
    st.dataframe(top_table, use_container_width=True, hide_index=True)

with rank_right:
    st.subheader("Bottom 5 需跟进实习生")
    bottom_table = summary["bottom_interns"][
        ["name", "role", "mentor_name", "fit_score", "level", "risk_level"]
    ].rename(
        columns={
            "name": "姓名",
            "role": "岗位",
            "mentor_name": "导师",
            "fit_score": "适岗分",
            "level": "适岗等级",
            "risk_level": "风险等级",
        }
    )
    st.dataframe(bottom_table, use_container_width=True, hide_index=True)

st.divider()

st.subheader("AI 风险摘要与行动建议")
if not summary["risk_records"]:
    st.success("当前暂无需 HR 重点跟进的风险对象。")
else:
    for record in summary["risk_records"][:5]:
        with st.expander(
            f"{record['name']}｜{record['role']}｜{record['risk_level']}｜适岗分 {record['fit_score']}",
            expanded=record["risk_level"] == "高风险",
        ):
            st.write(f"导师：{record['mentor_name']}")
            st.write("风险原因：")
            for reason in record["reasons"]:
                st.markdown(f"- {reason}")
            st.write("建议动作：")
            for action in record["actions"]:
                st.markdown(f"- {action}")

st.divider()

st.subheader("实习生明细")
display_columns = {
    "intern_id": "ID",
    "name": "姓名",
    "role": "岗位",
    "mentor_name": "导师",
    "current_week": "当前周",
    "task_score": "任务分",
    "fit_score": "适岗分",
    "level": "适岗等级",
    "risk_level": "风险等级",
    "ai_summary": "摘要",
}
st.dataframe(
    dataset[list(display_columns)].rename(columns=display_columns),
    use_container_width=True,
    hide_index=True,
)
