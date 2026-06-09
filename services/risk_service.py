"""Risk classification rules and action recommendations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from services.scoring_service import clamp_score


RISK_KEYWORDS = ["偏慢", "不足", "迷茫", "沉默", "不完整", "不够稳定", "拖延", "缺席", "质量较低"]


@dataclass(frozen=True)
class RiskAssessment:
    risk_level: str
    reasons: list[str]
    actions: list[str]


def find_risk_keywords(text: str, keywords: Iterable[str] = RISK_KEYWORDS) -> list[str]:
    """Return risk keywords that appear in mentor feedback."""
    return [keyword for keyword in keywords if keyword in (text or "")]


def classify_risk_level(fit_score: float, task_score: float, feedback_text: str = "") -> str:
    """Classify intern risk using score thresholds and feedback keywords."""
    fit_score = clamp_score(fit_score)
    task_score = clamp_score(task_score)
    keyword_hits = find_risk_keywords(feedback_text)

    if fit_score < 60 or task_score < 50:
        return "高风险"
    if fit_score < 70 or keyword_hits:
        return "需关注"
    return "低风险"


def build_risk_reasons(record: Mapping[str, object], feedback_text: str = "") -> list[str]:
    """Explain why the risk level was assigned."""
    fit_score = clamp_score(record.get("fit_score"))
    task_score = clamp_score(record.get("task_score"))
    initiative_score = clamp_score(record.get("initiative_score"))
    communication_score = clamp_score(record.get("communication_score"))
    keyword_hits = find_risk_keywords(feedback_text)

    reasons = []
    if fit_score < 60:
        reasons.append("适岗分低于 60，整体适配存在明显风险")
    elif fit_score < 70:
        reasons.append("适岗分低于 70，需要阶段性关注")

    if task_score < 50:
        reasons.append("任务完成度低于 50，交付节奏明显滞后")
    elif task_score < 65:
        reasons.append("任务完成度低于 65，短期交付稳定性不足")

    if initiative_score < 65:
        reasons.append("学习主动性评分偏低")
    if communication_score < 65:
        reasons.append("沟通协作评分偏低")
    if keyword_hits:
        reasons.append(f"导师反馈命中风险关键词：{'、'.join(keyword_hits)}")

    if not reasons:
        reasons.append("核心评分稳定，暂未识别明显风险")
    return reasons


def build_risk_actions(risk_level: str, reasons: list[str]) -> list[str]:
    """Generate deterministic next actions for HR and mentors."""
    if risk_level == "高风险":
        return [
            "HR 在本周安排一次 15 分钟阶段沟通，确认困难来源",
            "导师为下周拆解一个明确、可验收的小任务",
            "要求实习生提交一份本周问题清单和下一步计划",
        ]
    if risk_level == "需关注":
        return [
            "导师在下周例会前明确任务目标和验收标准",
            "实习生每两天同步一次进展，减少方向不清带来的等待",
            "HR 观察一周后复盘任务完成度和反馈质量",
        ]
    return [
        "继续保持现有带教节奏",
        "增加一个真实业务场景任务，沉淀可复用成果",
    ]


def assess_risk(record: Mapping[str, object], feedback_text: str = "") -> RiskAssessment:
    """Return risk level, reasons and recommended actions."""
    fit_score = clamp_score(record.get("fit_score"))
    task_score = clamp_score(record.get("task_score"))
    risk_level = classify_risk_level(fit_score, task_score, feedback_text)
    reasons = build_risk_reasons(record, feedback_text)
    actions = build_risk_actions(risk_level, reasons)
    return RiskAssessment(risk_level=risk_level, reasons=reasons, actions=actions)
