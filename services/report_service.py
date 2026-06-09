"""Generate HR weekly reports from dashboard summary data."""

from __future__ import annotations

from typing import Any

import pandas as pd


def _format_role_summary(role_summary: pd.DataFrame) -> str:
    parts = []
    for row in role_summary.sort_values("avg_fit_score", ascending=False).itertuples(index=False):
        parts.append(
            f"{row.role}岗 {row.interns} 人，平均任务分 {row.avg_task_score}，"
            f"平均适岗分 {row.avg_fit_score}，风险人数 {row.risk_cases} 人"
        )
    return "；".join(parts)


def _format_risk_names(dataset: pd.DataFrame) -> str:
    risk_df = dataset[dataset["risk_level"] != "低风险"].sort_values(["risk_level", "fit_score"], ascending=[False, True])
    if risk_df.empty:
        return "暂无需重点跟进对象"
    names = [f"{row.name}（{row.role}，{row.risk_level}，{row.fit_score}分）" for row in risk_df.itertuples()]
    return "、".join(names[:6])


def generate_weekly_report(summary: dict[str, Any]) -> str:
    """Generate a concise HR weekly report with deterministic content."""
    metrics = summary["metrics"]
    dataset = summary["dataset"]
    role_summary = summary["role_summary"]
    risk_records = summary["risk_records"]

    high_risk = int((dataset["risk_level"] == "高风险").sum())
    watch = int((dataset["risk_level"] == "需关注").sum())
    low_risk = int((dataset["risk_level"] == "低风险").sum())
    role_text = _format_role_summary(role_summary)
    risk_names = _format_risk_names(dataset)

    actions = []
    for record in risk_records[:3]:
        if record["actions"]:
            actions.append(f"{record['name']}：{record['actions'][0]}")
    if not actions:
        actions.append("保持现有带教节奏，为高潜实习生增加真实业务任务")

    return (
        f"本周实习生整体情况：共 {metrics['total_interns']} 名实习生，"
        f"高潜 {metrics['high_potential_count']} 人，稳定 {metrics['stable_count']} 人，"
        f"需关注 {watch} 人，高风险 {high_risk} 人，低风险 {low_risk} 人。"
        f"平均任务分为 {metrics['avg_task_score']}，平均适岗分为 {metrics['avg_fit_score']}，"
        f"导师反馈覆盖率为 {metrics['mentor_feedback_rate']}%。\n\n"
        f"岗位表现：{role_text}。\n\n"
        f"重点风险对象：{risk_names}。\n\n"
        "下周建议动作：\n"
        + "\n".join(f"{index}. {action}" for index, action in enumerate(actions, start=1))
        + "\n\n"
        "管理建议：优先处理高风险对象的方向不清、任务拆解和沟通频率问题；"
        "对稳定和高潜实习生增加真实业务任务，沉淀可展示成果，便于后续招聘和转正评估。"
    )


def generate_report_outline(summary: dict[str, Any]) -> dict[str, list[str]]:
    """Return structured report blocks for page display."""
    dataset = summary["dataset"]
    risk_df = dataset[dataset["risk_level"] != "低风险"].sort_values("fit_score")

    return {
        "整体结论": [
            f"共 {summary['metrics']['total_interns']} 名实习生，平均适岗分 {summary['metrics']['avg_fit_score']}。",
            f"当前风险预警 {summary['metrics']['risk_count']} 人，导师反馈覆盖率 {summary['metrics']['mentor_feedback_rate']}%。",
        ],
        "风险名单": [
            f"{row.name}｜{row.role}｜{row.risk_level}｜适岗分 {row.fit_score}"
            for row in risk_df.head(6).itertuples()
        ]
        or ["暂无重点风险对象"],
        "下周动作": [
            "HR 优先跟进高风险对象，确认方向、资源和岗位适配问题。",
            "导师为需关注对象拆解更明确的小任务，并提高反馈频率。",
            "为高潜对象增加真实业务任务，沉淀可展示成果。",
        ],
    }
