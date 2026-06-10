import streamlit as st

from services.auth_service import (
    build_intern_options,
    ensure_options,
    render_role_selector,
    render_scope_controls,
    require_page_access,
)
from services.data_service import clear_data_cache, get_evaluation_dataset, get_intern_profile, parse_intern_id
from services.mentor_feedback_service import analyze_mentor_feedback
from services.storage_service import load_feedback_history, save_mentor_feedback


st.set_page_config(page_title="导师带教助手", layout="wide")

st.title("导师带教助手")
st.caption("导师输入自然语言反馈，系统输出结构化评价、风险判断和下一步带教动作。")

role = render_role_selector()
require_page_access(role, "mentor_assistant")
dataset = get_evaluation_dataset()
scoped_dataset = render_scope_controls(role, dataset, "mentor_assistant")
options = ensure_options(build_intern_options(scoped_dataset))
selected = st.sidebar.selectbox("选择实习生", options)
intern_id = parse_intern_id(selected)
profile_data = get_intern_profile(intern_id)
profile = profile_data["profile"]

default_feedback = profile.get(
    "feedback_text",
    "本周完成了基础任务，但会议表达不够主动，阶段成果沉淀偏少。",
)

left, right = st.columns([1, 1])

with left:
    st.subheader(f"{profile['name']}｜{profile['role']}实习生")
    st.markdown(
        f"""
**导师**：{profile['mentor_name']}  
**当前周数**：第 {int(profile['current_week'])} 周  
**当前适岗分**：{profile['fit_score']}  
**当前风险等级**：{profile['risk_level']}
"""
    )

    feedback_text = st.text_area(
        "导师反馈",
        value=default_feedback,
        height=180,
        help="可以输入自然语言，例如：本周完成了接口文档阅读，但代码提交较少，开会表达不够主动。",
    )
    button_left, button_right = st.columns(2)
    analyze_clicked = button_left.button("生成结构化分析", type="primary")
    save_clicked = button_right.button("保存导师反馈")

with right:
    st.subheader("示例反馈")
    st.info(
        "小李本周完成了接口文档阅读，也能独立跑通测试环境。"
        "但是代码提交较少，开会时比较沉默，不太主动表达问题。"
    )
    st.write("这个模块体现的 AI 价值：把导师的主观反馈转成可复用、可跟进、可沉淀的结构化结论。")

st.divider()

if save_clicked:
    save_mentor_feedback(
        intern_id=profile["intern_id"],
        mentor_id=profile["mentor_id"],
        week=int(profile["current_week"]),
        feedback_text=feedback_text,
    )
    clear_data_cache()
    st.success("导师反馈已保存，个人画像和周报会读取最新反馈。")
    st.rerun()

if analyze_clicked or feedback_text:
    analysis = analyze_mentor_feedback(feedback_text, profile)

    c1, c2, c3 = st.columns(3)
    c1.metric("风险等级", analysis.risk_level)
    c2.metric("识别优点", len(analysis.strengths))
    c3.metric("改进点", len(analysis.weaknesses))
    source_text = "规则模板 fallback" if analysis.used_fallback else f"LLM：{analysis.llm_provider}"
    st.caption(f"生成来源：{source_text}")

    result_left, result_right = st.columns([1, 1])

    with result_left:
        st.subheader("结构化评价")
        st.write("优点：")
        for item in analysis.strengths:
            st.markdown(f"- {item}")

        st.write("问题 / 短板：")
        for item in analysis.weaknesses:
            st.markdown(f"- {item}")

        st.write("HR 建议：")
        for item in analysis.hr_actions:
            st.markdown(f"- {item}")

    with result_right:
        st.subheader("下周带教动作")
        for item in analysis.mentor_actions:
            st.markdown(f"- {item}")

        st.subheader("给实习生的反馈话术")
        st.success(analysis.message_to_intern)

        st.subheader("AI 补充洞察")
        st.info(analysis.ai_insight)

st.divider()
st.subheader("反馈历史")
history = load_feedback_history(intern_id)
if history.empty:
    st.caption("暂无新增反馈历史。保存一次导师反馈后会在这里显示。")
else:
    st.dataframe(
        history.rename(
            columns={
                "week": "周次",
                "feedback_text": "反馈内容",
                "created_at": "保存时间",
                "mentor_id": "导师 ID",
                "intern_id": "实习生 ID",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )
