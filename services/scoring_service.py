"""Fit scoring rules for intern growth evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


SCORE_WEIGHTS = {
    "task_score": 0.30,
    "mentor_score": 0.25,
    "initiative_score": 0.20,
    "communication_score": 0.15,
    "skill_match_score": 0.10,
}

SCORE_LABELS = {
    "task_score": "任务完成度",
    "mentor_score": "导师评价",
    "initiative_score": "学习主动性",
    "communication_score": "沟通协作",
    "skill_match_score": "岗位技能匹配",
}

LEVEL_EXPLANATIONS = {
    "高潜": "可重点培养，具备转正潜力",
    "稳定": "表现正常，可继续观察并增加真实任务",
    "需关注": "存在阶段短板，需要导师明确干预",
    "高风险": "可能不适岗，需要 HR 和导师共同跟进",
}


@dataclass(frozen=True)
class ScoreDimension:
    field: str
    label: str
    raw_score: float
    weight: float
    contribution: float
    status: str
    interpretation: str


@dataclass(frozen=True)
class ScoreBreakdown:
    task_score: float
    mentor_score: float
    initiative_score: float
    communication_score: float
    skill_match_score: float
    fit_score: float
    level: str
    explanation: str
    level_explanation: str
    dimensions: list[ScoreDimension]


def clamp_score(value: object) -> float:
    """Normalize a raw score into the 0-100 range."""
    try:
        score = float(value)
    except (TypeError, ValueError):
        score = 0.0
    return max(0.0, min(100.0, score))


def classify_fit_level(fit_score: float) -> str:
    """Map a fit score to the product-facing talent level."""
    if fit_score >= 85:
        return "高潜"
    if fit_score >= 70:
        return "稳定"
    if fit_score >= 60:
        return "需关注"
    return "高风险"


def calculate_fit_score(record: Mapping[str, object]) -> float:
    """Calculate the weighted fit score from evaluation dimensions."""
    total = 0.0
    for field, weight in SCORE_WEIGHTS.items():
        total += clamp_score(record.get(field)) * weight
    return round(total, 2)


def classify_dimension_status(score: float) -> str:
    if score >= 85:
        return "优势"
    if score >= 70:
        return "稳定"
    if score >= 60:
        return "需关注"
    return "短板"


def build_dimension_interpretation(field: str, score: float, status: str) -> str:
    label = SCORE_LABELS[field]
    if status == "优势":
        return f"{label}表现突出，可作为后续培养抓手"
    if status == "稳定":
        return f"{label}达到阶段要求，可继续观察"
    if status == "需关注":
        return f"{label}存在波动，建议下周设置明确目标"
    return f"{label}低于预期，需要导师拆解任务并跟进"


def build_score_dimensions(record: Mapping[str, object]) -> list[ScoreDimension]:
    dimensions = []
    for field, weight in SCORE_WEIGHTS.items():
        raw_score = clamp_score(record.get(field))
        contribution = round(raw_score * weight, 2)
        status = classify_dimension_status(raw_score)
        dimensions.append(
            ScoreDimension(
                field=field,
                label=SCORE_LABELS[field],
                raw_score=raw_score,
                weight=weight,
                contribution=contribution,
                status=status,
                interpretation=build_dimension_interpretation(field, raw_score, status),
            )
        )
    return dimensions


def build_score_explanation(record: Mapping[str, object], level: str, fit_score: float) -> str:
    """Generate a deterministic explanation before the LLM layer is added."""
    task_score = clamp_score(record.get("task_score"))
    initiative_score = clamp_score(record.get("initiative_score"))
    communication_score = clamp_score(record.get("communication_score"))
    skill_match_score = clamp_score(record.get("skill_match_score"))

    strengths = []
    improvements = []

    if task_score >= 80:
        strengths.append("任务交付较稳定")
    elif task_score < 65:
        improvements.append("任务完成节奏需要加强")

    if initiative_score >= 80:
        strengths.append("学习主动性较好")
    elif initiative_score < 65:
        improvements.append("需要提升主动提问和阶段汇报")

    if communication_score >= 80:
        strengths.append("沟通协作表现较好")
    elif communication_score < 65:
        improvements.append("需要加强与导师的沟通同步")

    if skill_match_score >= 80:
        strengths.append("岗位技能匹配度较高")
    elif skill_match_score < 65:
        improvements.append("岗位技能仍需补齐")

    if not strengths:
        strengths.append("基础表现具备继续观察价值")
    if not improvements:
        improvements.append("下一阶段可增加真实业务任务沉淀")

    level_reason = LEVEL_EXPLANATIONS[level]
    return (
        f"适岗分 {fit_score:.2f}，等级为{level}。"
        f"{level_reason}。"
        f"主要优势：{'、'.join(strengths[:2])}。"
        f"改进方向：{'、'.join(improvements[:2])}。"
    )


def evaluate_fit(record: Mapping[str, object]) -> ScoreBreakdown:
    """Return score, level and explanation for one intern evaluation record."""
    normalized = {field: clamp_score(record.get(field)) for field in SCORE_WEIGHTS}
    fit_score = calculate_fit_score(normalized)
    level = classify_fit_level(fit_score)
    explanation = build_score_explanation(normalized, level, fit_score)
    dimensions = build_score_dimensions(normalized)
    return ScoreBreakdown(
        task_score=normalized["task_score"],
        mentor_score=normalized["mentor_score"],
        initiative_score=normalized["initiative_score"],
        communication_score=normalized["communication_score"],
        skill_match_score=normalized["skill_match_score"],
        fit_score=fit_score,
        level=level,
        explanation=explanation,
        level_explanation=LEVEL_EXPLANATIONS[level],
        dimensions=dimensions,
    )
