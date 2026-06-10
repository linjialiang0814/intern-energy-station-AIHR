from services.data_service import get_dashboard_summary, get_intern_profile, get_intern_options, parse_intern_id
from services.export_service import build_dashboard_markdown, build_profile_markdown, dataframe_to_csv_bytes
from services.growth_plan_service import generate_growth_plan
from services.llm_service import call_llm
from services.mentor_feedback_service import analyze_mentor_feedback
from services.scoring_service import SCORE_WEIGHTS, evaluate_fit


def test_dashboard_summary_shape():
    summary = get_dashboard_summary()

    assert summary["metrics"]["total_interns"] == 20
    assert len(summary["dataset"]) == 20
    assert len(summary["role_summary"]) == 3
    assert summary["metrics"]["risk_count"] == len(summary["risk_records"])


def test_score_explanation_dimensions_match_fit_score():
    summary = get_dashboard_summary()
    record = summary["dataset"].iloc[0].to_dict()
    score = evaluate_fit(record)

    assert len(score.dimensions) == len(SCORE_WEIGHTS)
    assert score.level_explanation
    assert all(item.interpretation for item in score.dimensions)
    assert round(sum(item.contribution for item in score.dimensions), 2) == score.fit_score


def test_intern_profile_contains_tasks_and_actions():
    option = get_intern_options()[0]
    profile_data = get_intern_profile(parse_intern_id(option))

    assert len(profile_data["task_records"]) > 0
    assert len(profile_data["risk"].actions) > 0
    assert profile_data["score"].explanation


def test_ai_feature_fallback_outputs():
    option = get_intern_options()[0]
    profile = get_intern_profile(parse_intern_id(option))["profile"]

    analysis = analyze_mentor_feedback("本周完成了接口文档阅读，但代码提交较少，开会表达不够主动。", profile)
    growth_plan = generate_growth_plan(profile, "不知道接下来该重点学什么")

    assert analysis.strengths
    assert analysis.weaknesses
    assert analysis.mentor_actions
    assert analysis.ai_insight
    assert growth_plan.learning_focus
    assert growth_plan.recommended_tasks
    assert growth_plan.mentor_questions


def test_llm_fallback_without_key(monkeypatch):
    monkeypatch.delenv("ARK_API_KEY", raising=False)
    monkeypatch.delenv("VOLCENGINE_ARK_API_KEY", raising=False)
    monkeypatch.delenv("VOLCENGINE_API_KEY", raising=False)

    result = call_llm([{"role": "user", "content": "hello"}], fallback="fallback-ok")

    assert result.used_fallback is True
    assert result.provider == "fallback"
    assert result.content == "fallback-ok"


def test_export_outputs():
    summary = get_dashboard_summary()
    option = get_intern_options()[0]
    profile_data = get_intern_profile(parse_intern_id(option))

    dashboard_md = build_dashboard_markdown(summary)
    profile_md = build_profile_markdown(profile_data)
    csv_bytes = dataframe_to_csv_bytes(summary["dataset"].head(3))

    assert "# 实习能量站 HR 总览摘要" in dashboard_md
    assert "实习生个人画像" in profile_md
    assert "评分贡献拆解" in profile_md
    assert csv_bytes.startswith(b"\xef\xbb\xbf")
