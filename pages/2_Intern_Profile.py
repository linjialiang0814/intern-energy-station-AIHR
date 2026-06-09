import pandas as pd
import streamlit as st

from services.data_service import get_intern_options, get_intern_profile, parse_intern_id


st.set_page_config(page_title="实习生个人画像", layout="wide")

st.title("实习生个人画像")
st.caption("把个人基础信息、任务进度、能力评分、导师反馈和下一步动作放在同一个视图里。")

options = get_intern_options()
selected = st.sidebar.selectbox("选择实习生", options)
intern_id = parse_intern_id(selected)
data = get_intern_profile(intern_id)

profile = data["profile"]
score = data["score"]
risk = data["risk"]
task_records = data["task_records"]
ability_scores = data["ability_scores"]

header_left, header_right = st.columns([1.2, 1])

with header_left:
    st.subheader(f"{profile['name']}｜{profile['role']}实习生")
    info_cols = st.columns(4)
    info_cols[0].metric("当前周数", f"第 {int(profile['current_week'])} 周")
    info_cols[1].metric("适岗分", score.fit_score)
    info_cols[2].metric("适岗等级", score.level)
    info_cols[3].metric("风险等级", risk.risk_level)

    st.markdown(
        f"""
**学校/专业**：{profile['school']} / {profile['major']}  
**导师**：{profile['mentor_name']}（{profile['department']}）  
**入职日期**：{profile['join_date']}
"""
    )

with header_right:
    st.subheader("规则解释")
    st.info(score.explanation)

st.divider()

ability_left, action_right = st.columns([1, 1])

with ability_left:
    st.subheader("能力评分")
    ability_df = pd.DataFrame(
        [{"能力维度": key, "评分": value} for key, value in ability_scores.items()]
    ).set_index("能力维度")
    st.bar_chart(ability_df)

    for key, value in ability_scores.items():
        st.progress(int(value), text=f"{key}：{value:.0f}/100")

with action_right:
    st.subheader("风险原因")
    for reason in risk.reasons:
        st.markdown(f"- {reason}")

    st.subheader("下一步行动建议")
    for action in risk.actions:
        st.markdown(f"- {action}")

st.divider()

feedback_left, summary_right = st.columns([1, 1])

with feedback_left:
    st.subheader("导师反馈")
    st.write(profile.get("feedback_text", "暂无反馈"))

with summary_right:
    st.subheader("AI 摘要")
    st.success(profile.get("ai_summary", "暂无摘要"))

st.divider()

st.subheader("任务完成记录")
task_table = task_records[
    [
        "week",
        "task_name",
        "completion_status",
        "completion_score",
        "expected_output",
        "submission_text",
        "updated_at",
    ]
].rename(
    columns={
        "week": "周次",
        "task_name": "任务",
        "completion_status": "状态",
        "completion_score": "完成分",
        "expected_output": "预期交付物",
        "submission_text": "提交说明",
        "updated_at": "更新时间",
    }
)
st.dataframe(task_table, use_container_width=True, hide_index=True)
