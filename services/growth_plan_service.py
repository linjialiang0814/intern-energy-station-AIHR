"""Generate intern growth plans from role, week and current evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from services.llm_service import call_llm
from services.scoring_service import clamp_score


ROLE_FOCUS = {
    "研发": {
        "learning": ["熟悉代码结构", "完成小型开发任务", "沉淀调试和测试记录"],
        "task": "选择一个低风险缺陷或小需求，完成代码提交和自测记录",
        "deliverable": "代码提交记录、测试截图、问题复盘",
        "mentor_question": "这个任务的验收标准是什么？哪些边界条件需要重点关注？",
    },
    "产品": {
        "learning": ["理解业务流程", "学习需求分析方法", "练习输出结构化 PRD"],
        "task": "选择一个小需求，完成背景、用户场景、流程和验收标准梳理",
        "deliverable": "一页需求分析文档或低保真原型",
        "mentor_question": "这个需求真正解决的用户问题是什么？优先级如何判断？",
    },
    "销售": {
        "learning": ["熟悉产品卖点", "理解客户画像", "练习客户沟通话术"],
        "task": "围绕一个典型客户场景，准备一次模拟拜访和异议处理话术",
        "deliverable": "客户画像卡片、拜访话术、沟通复盘",
        "mentor_question": "客户最常见的异议是什么？我应该如何判断客户意向强弱？",
    },
}


@dataclass(frozen=True)
class GrowthPlan:
    stage: str
    roadmap_30_60_90: list[dict[str, str]]
    learning_focus: list[str]
    recommended_tasks: list[str]
    deliverables: list[str]
    mentor_questions: list[str]
    encouragement: str
    llm_provider: str
    used_fallback: bool


def classify_stage(week: int) -> str:
    if week <= 2:
        return "业务熟悉与基础上手"
    if week <= 4:
        return "小任务实践与反馈校准"
    return "独立承担小模块与成果沉淀"


def generate_30_60_90_roadmap(role: str) -> list[dict[str, str]]:
    """Return a role-specific 30-60-90 day growth roadmap."""
    roadmaps = {
        "研发": [
            {
                "阶段": "0-30 天",
                "目标": "熟悉代码库、开发流程和测试环境",
                "关键任务": "完成环境搭建、阅读核心模块、修复低风险缺陷",
                "交付物": "环境记录、代码提交、自测截图",
            },
            {
                "阶段": "31-60 天",
                "目标": "参与模块开发并形成稳定交付节奏",
                "关键任务": "完成小需求开发、补充单元测试、参与代码评审",
                "交付物": "需求代码、测试用例、评审记录",
            },
            {
                "阶段": "61-90 天",
                "目标": "独立承担小模块并沉淀复盘",
                "关键任务": "负责一个小模块闭环、定位线上问题、输出技术复盘",
                "交付物": "模块交付、问题复盘、改进建议",
            },
        ],
        "产品": [
            {
                "阶段": "0-30 天",
                "目标": "理解业务、用户和产品流程",
                "关键任务": "阅读业务资料、体验核心流程、完成竞品观察",
                "交付物": "业务流程图、竞品分析、问题清单",
            },
            {
                "阶段": "31-60 天",
                "目标": "参与需求分析和方案表达",
                "关键任务": "梳理用户场景、参与需求评审、输出小需求 PRD",
                "交付物": "PRD、低保真原型、验收标准",
            },
            {
                "阶段": "61-90 天",
                "目标": "跟进上线并用数据复盘效果",
                "关键任务": "推动需求上线、收集反馈、分析核心指标变化",
                "交付物": "上线复盘、数据分析、迭代建议",
            },
        ],
        "销售": [
            {
                "阶段": "0-30 天",
                "目标": "熟悉产品卖点、客户画像和销售流程",
                "关键任务": "学习产品资料、旁听客户沟通、整理常见问题",
                "交付物": "客户画像卡、产品话术、FAQ",
            },
            {
                "阶段": "31-60 天",
                "目标": "完成模拟拜访和真实客户跟进",
                "关键任务": "准备拜访脚本、参与客户会议、复盘异议处理",
                "交付物": "拜访记录、异议处理话术、跟进计划",
            },
            {
                "阶段": "61-90 天",
                "目标": "独立跟进低风险线索并沉淀方法",
                "关键任务": "推进线索转化、维护客户关系、总结销售策略",
                "交付物": "线索进展表、客户复盘、策略总结",
            },
        ],
    }
    return roadmaps.get(role, roadmaps["研发"])


def find_weak_dimensions(profile: Mapping[str, object]) -> list[str]:
    dimensions = [
        ("任务交付", clamp_score(profile.get("task_score"))),
        ("学习主动性", clamp_score(profile.get("initiative_score"))),
        ("沟通协作", clamp_score(profile.get("communication_score"))),
        ("岗位技能", clamp_score(profile.get("skill_match_score"))),
    ]
    weak = [name for name, score in dimensions if score < 70]
    return weak or ["业务理解深化"]


def generate_growth_plan(profile: Mapping[str, object], question: str = "") -> GrowthPlan:
    role = str(profile.get("role", "研发"))
    week = int(profile.get("current_week", profile.get("week", 1)))
    name = str(profile.get("name", "同学"))
    role_config = ROLE_FOCUS.get(role, ROLE_FOCUS["研发"])
    weak_dimensions = find_weak_dimensions(profile)
    stage = classify_stage(week)

    learning_focus = role_config["learning"][:]
    if "学习主动性" in weak_dimensions:
        learning_focus.append("建立固定的主动同步节奏")
    if "沟通协作" in weak_dimensions:
        learning_focus.append("提前准备会议问题并主动表达")
    if "岗位技能" in weak_dimensions:
        learning_focus.append("补齐岗位基础技能并形成学习笔记")

    recommended_tasks = [
        role_config["task"],
        f"围绕“{weak_dimensions[0]}”设置一个本周可验收目标",
        "每两天向导师同步一次进展、阻塞点和下一步计划",
    ]

    if question:
        recommended_tasks.append(f"针对当前困惑“{question}”，先拆成 1 个可向导师确认的具体问题")

    deliverables = [
        role_config["deliverable"],
        "本周问题清单与解决记录",
        "一段 3-5 句话的阶段复盘",
    ]

    mentor_questions = [
        role_config["mentor_question"],
        "本周最重要的一个交付物是什么？做到什么程度算达标？",
        "我当前最需要补齐的能力短板是哪一个？",
    ]

    fallback_encouragement = (
        f"{name}当前处于“{stage}”阶段，重点不是一次做完所有事，"
        "而是把任务拆小、及时反馈、沉淀成果。只要每周留下一个可展示的产出，成长路径就会越来越清晰。"
    )
    llm_result = call_llm(
        [
            {
                "role": "system",
                "content": "你是企业实习生成长教练，请给出温和、具体、可执行的中文建议。",
            },
            {
                "role": "user",
                "content": (
                    f"实习生：{name}\n岗位：{role}\n当前周次：{week}\n"
                    f"阶段：{stage}\n能力短板：{weak_dimensions}\n困惑：{question}\n"
                    "请生成一段 120 字以内的鼓励性成长建议。"
                ),
            },
        ],
        fallback=fallback_encouragement,
        max_tokens=220,
    )

    return GrowthPlan(
        stage=stage,
        roadmap_30_60_90=generate_30_60_90_roadmap(role),
        learning_focus=list(dict.fromkeys(learning_focus))[:5],
        recommended_tasks=recommended_tasks[:4],
        deliverables=deliverables,
        mentor_questions=mentor_questions,
        encouragement=llm_result.content,
        llm_provider=llm_result.provider,
        used_fallback=llm_result.used_fallback,
    )
