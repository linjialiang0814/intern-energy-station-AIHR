"""Export helpers for dashboard summaries, intern profiles and reports."""

from __future__ import annotations

from typing import Any

import pandas as pd


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Export dataframe as UTF-8 BOM CSV for Excel-friendly Chinese text."""
    return df.to_csv(index=False).encode("utf-8-sig")


def build_dashboard_markdown(summary: dict[str, Any]) -> str:
    metrics = summary["metrics"]
    role_summary = summary["role_summary"]
    risk_records = summary["risk_records"]

    lines = [
        "# 实习能量站 HR 总览摘要",
        "",
        "## 核心指标",
        "",
        f"- 实习生总数：{metrics['total_interns']}",
        f"- 高潜人数：{metrics['high_potential_count']}",
        f"- 稳定人数：{metrics['stable_count']}",
        f"- 风险预警人数：{metrics['risk_count']}",
        f"- 平均任务分：{metrics['avg_task_score']}",
        f"- 平均适岗分：{metrics['avg_fit_score']}",
        f"- 导师反馈率：{metrics['mentor_feedback_rate']}%",
        "",
        "## 岗位表现",
        "",
    ]

    for row in role_summary.itertuples(index=False):
        lines.append(
            f"- {row.role}：{row.interns} 人，平均任务分 {row.avg_task_score}，"
            f"平均适岗分 {row.avg_fit_score}，风险人数 {row.risk_cases}"
        )

    lines.extend(["", "## 重点风险对象", ""])
    if not risk_records:
        lines.append("- 暂无重点风险对象")
    else:
        for record in risk_records[:8]:
            lines.append(f"- {record['name']}｜{record['role']}｜{record['risk_level']}｜适岗分 {record['fit_score']}")
            if record["actions"]:
                lines.append(f"  - 建议动作：{record['actions'][0]}")

    return "\n".join(lines)


def build_profile_markdown(profile_data: dict[str, Any]) -> str:
    profile = profile_data["profile"]
    score = profile_data["score"]
    risk = profile_data["risk"]
    task_records = profile_data["task_records"]

    lines = [
        f"# {profile['name']} 实习生个人画像",
        "",
        "## 基础信息",
        "",
        f"- 岗位：{profile['role']}",
        f"- 学校/专业：{profile['school']} / {profile['major']}",
        f"- 导师：{profile['mentor_name']}（{profile['department']}）",
        f"- 当前周数：第 {int(profile['current_week'])} 周",
        f"- 适岗分：{score.fit_score}",
        f"- 适岗等级：{score.level}（{score.level_explanation}）",
        f"- 风险等级：{risk.risk_level}",
        "",
        "## 评分解释",
        "",
        score.explanation,
        "",
        "## 评分贡献拆解",
        "",
    ]

    for item in score.dimensions:
        lines.append(
            f"- {item.label}：原始分 {item.raw_score:.0f}，权重 {item.weight:.0%}，"
            f"贡献分 {item.contribution:.2f}，状态 {item.status}。{item.interpretation}"
        )

    lines.extend(["", "## 风险原因", ""])
    lines.extend(f"- {reason}" for reason in risk.reasons)

    lines.extend(["", "## 下一步行动建议", ""])
    lines.extend(f"- {action}" for action in risk.actions)

    lines.extend(["", "## 导师反馈", "", str(profile.get("feedback_text", "暂无反馈")), "", "## 任务记录", ""])
    for row in task_records.itertuples(index=False):
        lines.append(
            f"- 第 {row.week} 周：{row.task_name}，状态 {row.completion_status}，完成分 {row.completion_score}"
        )

    return "\n".join(lines)


def build_filename_safe_name(name: str) -> str:
    return "".join(ch for ch in name if ch.isalnum() or ch in {"-", "_"}) or "intern"
