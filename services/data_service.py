"""CSV data loading and aggregation for dashboard pages."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd

from services.risk_service import assess_risk
from services.scoring_service import evaluate_fit


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def _read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name, encoding="utf-8-sig")


@lru_cache(maxsize=1)
def load_tables() -> dict[str, pd.DataFrame]:
    """Load all MVP CSV tables."""
    return {
        "interns": _read_csv("interns.csv"),
        "mentors": _read_csv("mentors.csv"),
        "weekly_tasks": _read_csv("weekly_tasks.csv"),
        "intern_progress": _read_csv("intern_progress.csv"),
        "mentor_feedback": _read_csv("mentor_feedback.csv"),
        "evaluation_results": _read_csv("evaluation_results.csv"),
    }


def get_evaluation_dataset() -> pd.DataFrame:
    """Return one row per intern with profile, mentor, feedback and evaluation."""
    tables = load_tables()
    interns = tables["interns"]
    mentors = tables["mentors"]
    feedback = tables["mentor_feedback"]
    evaluations = tables["evaluation_results"]

    dataset = (
        interns.merge(mentors, on="mentor_id", how="left", suffixes=("", "_mentor"))
        .merge(evaluations, on="intern_id", how="left")
        .merge(
            feedback[["intern_id", "feedback_text", "created_at"]],
            on="intern_id",
            how="left",
        )
    )
    return dataset.sort_values(["risk_level", "fit_score"], ascending=[False, True]).reset_index(drop=True)


def get_dashboard_summary() -> dict[str, Any]:
    """Build aggregate data for the HR Dashboard."""
    dataset = get_evaluation_dataset()
    tables = load_tables()
    feedback = tables["mentor_feedback"]

    total_interns = len(dataset)
    risk_count = int((dataset["risk_level"] != "低风险").sum())
    high_potential_count = int((dataset["level"] == "高潜").sum())
    stable_count = int((dataset["level"] == "稳定").sum())
    mentor_feedback_rate = round(len(feedback["intern_id"].dropna().unique()) / total_interns * 100, 1)

    role_summary = (
        dataset.groupby("role", as_index=False)
        .agg(
            interns=("intern_id", "count"),
            avg_task_score=("task_score", "mean"),
            avg_fit_score=("fit_score", "mean"),
            risk_cases=("risk_level", lambda values: int((values != "低风险").sum())),
        )
        .round({"avg_task_score": 1, "avg_fit_score": 1})
    )

    risk_distribution = (
        dataset["risk_level"]
        .value_counts()
        .reindex(["低风险", "需关注", "高风险"], fill_value=0)
        .rename_axis("risk_level")
        .reset_index(name="count")
    )

    level_distribution = (
        dataset["level"]
        .value_counts()
        .reindex(["高潜", "稳定", "需关注", "高风险"], fill_value=0)
        .rename_axis("level")
        .reset_index(name="count")
    )

    risk_records = []
    for record in dataset[dataset["risk_level"] != "低风险"].to_dict(orient="records"):
        assessment = assess_risk(record, record.get("feedback_text", ""))
        risk_records.append(
            {
                "name": record["name"],
                "role": record["role"],
                "mentor_name": record["mentor_name"],
                "fit_score": record["fit_score"],
                "risk_level": assessment.risk_level,
                "reasons": assessment.reasons,
                "actions": assessment.actions,
            }
        )

    return {
        "metrics": {
            "total_interns": total_interns,
            "high_potential_count": high_potential_count,
            "stable_count": stable_count,
            "risk_count": risk_count,
            "avg_task_score": round(float(dataset["task_score"].mean()), 1),
            "avg_fit_score": round(float(dataset["fit_score"].mean()), 1),
            "mentor_feedback_rate": mentor_feedback_rate,
        },
        "dataset": dataset,
        "role_summary": role_summary,
        "risk_distribution": risk_distribution,
        "level_distribution": level_distribution,
        "top_interns": dataset.nlargest(5, "fit_score"),
        "bottom_interns": dataset.nsmallest(5, "fit_score"),
        "risk_records": risk_records,
    }


def get_intern_options() -> list[str]:
    """Return display labels for intern selector."""
    dataset = get_evaluation_dataset()
    return [
        f"{row.name} | {row.role} | {row.intern_id}"
        for row in dataset[["intern_id", "name", "role"]].itertuples(index=False)
    ]


def parse_intern_id(option: str) -> str:
    """Extract intern id from a selector label."""
    return option.split("|")[-1].strip()


def get_intern_profile(intern_id: str) -> dict[str, Any]:
    """Return all data needed by the intern profile page."""
    tables = load_tables()
    dataset = get_evaluation_dataset()
    row = dataset[dataset["intern_id"] == intern_id]
    if row.empty:
        raise ValueError(f"Unknown intern_id: {intern_id}")

    profile = row.iloc[0].to_dict()
    progress = tables["intern_progress"]
    tasks = tables["weekly_tasks"]

    task_records = (
        progress[progress["intern_id"] == intern_id]
        .merge(tasks[["task_id", "task_name", "expected_output"]], on="task_id", how="left")
        .sort_values("week")
    )

    score = evaluate_fit(profile)
    risk = assess_risk(profile, profile.get("feedback_text", ""))

    ability_scores = {
        "任务交付": score.task_score,
        "导师评价": score.mentor_score,
        "学习主动性": score.initiative_score,
        "沟通协作": score.communication_score,
        "岗位技能": score.skill_match_score,
    }

    return {
        "profile": profile,
        "task_records": task_records,
        "score": score,
        "risk": risk,
        "ability_scores": ability_scores,
    }
