"""Generate mock data for the Intern Energy Station MVP.

The script prefers Faker when it is installed, but keeps a deterministic
fallback so stage-1 data preparation can run without network access.
"""

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

try:
    from faker import Faker
except ImportError:  # pragma: no cover - exercised when Faker is absent.
    Faker = None


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RANDOM_SEED = 20260608

ROLES = ["研发", "产品", "销售"]
ROLE_DISTRIBUTION = ["研发"] * 8 + ["产品"] * 6 + ["销售"] * 6

SCHOOLS = [
    "南京大学",
    "中山大学",
    "武汉大学",
    "浙江大学",
    "华中科技大学",
    "四川大学",
    "厦门大学",
    "同济大学",
    "北京邮电大学",
    "上海财经大学",
]

MAJORS_BY_ROLE = {
    "研发": ["计算机科学", "软件工程", "人工智能", "数据科学"],
    "产品": ["信息管理", "工业设计", "工商管理", "心理学"],
    "销售": ["市场营销", "国际商务", "电子商务", "传播学"],
}

FALLBACK_NAMES = [
    "李明",
    "王雨",
    "陈晨",
    "赵一凡",
    "周岚",
    "刘思源",
    "孙可",
    "黄子涵",
    "吴越",
    "郑晓",
    "何然",
    "郭嘉宁",
    "林舒",
    "马骁",
    "朱安琪",
    "胡辰",
    "高远",
    "唐悦",
    "谢宁",
    "许诺",
]

MENTORS = [
    ("M001", "王老师", "研发一部", "后端工程师"),
    ("M002", "张老师", "研发平台组", "前端工程师"),
    ("M003", "赵老师", "产品增长组", "产品经理"),
    ("M004", "刘老师", "产品体验组", "产品经理"),
    ("M005", "陈老师", "销售华东区", "销售经理"),
    ("M006", "周老师", "销售行业组", "客户经理"),
]

TASK_TEMPLATES = {
    "研发": [
        ("完成开发环境配置", "环境截图与运行记录"),
        ("阅读项目代码结构", "代码结构说明文档"),
        ("修复一个低风险缺陷", "代码提交记录"),
        ("参与一次代码评审", "评审记录与改进清单"),
        ("完成一个小型功能开发", "功能说明与测试记录"),
    ],
    "产品": [
        ("阅读已有 PRD", "PRD 阅读笔记"),
        ("完成竞品分析", "竞品分析表"),
        ("参与需求评审", "会议纪要与问题清单"),
        ("输出一个小需求原型", "原型链接与说明"),
        ("跟进一次上线反馈", "数据反馈分析"),
    ],
    "销售": [
        ("熟悉产品卖点", "产品卖点总结"),
        ("完成客户画像学习", "客户画像卡片"),
        ("旁听一次客户沟通", "沟通复盘记录"),
        ("准备一次模拟拜访", "拜访话术与问题清单"),
        ("跟进一个销售线索", "线索跟进记录"),
    ],
}

POSITIVE_FEEDBACK = [
    "学习速度较快，能按时完成阶段任务。",
    "文档阅读认真，对岗位要求理解逐步加深。",
    "能够主动向导师确认目标，任务交付比较稳定。",
    "协作态度积极，能及时同步进展。",
]

RISK_FEEDBACK = [
    "本周任务推进偏慢，遇到问题后主动沟通不足。",
    "对业务方向仍有迷茫，会议中表达比较沉默。",
    "交付质量不够稳定，需要导师给出更明确的节奏。",
    "反馈记录不完整，阶段成果沉淀偏少。",
]


@dataclass(frozen=True)
class Intern:
    intern_id: str
    name: str
    role: str
    school: str
    major: str
    mentor_id: str
    join_date: str
    current_week: int
    status: str


def make_fake():
    if Faker is None:
        return None
    fake = Faker("zh_CN")
    Faker.seed(RANDOM_SEED)
    return fake


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def choose_mentor(role: str, index: int) -> str:
    if role == "研发":
        return MENTORS[index % 2][0]
    if role == "产品":
        return MENTORS[2 + index % 2][0]
    return MENTORS[4 + index % 2][0]


def build_interns(fake) -> list[Intern]:
    interns: list[Intern] = []
    base_join_date = date(2026, 5, 11)
    shuffled_roles = ROLE_DISTRIBUTION[:]
    random.shuffle(shuffled_roles)

    for index, role in enumerate(shuffled_roles, start=1):
        name = fake.name() if fake else FALLBACK_NAMES[index - 1]
        current_week = random.randint(2, 5)
        join_date = base_join_date - timedelta(days=(current_week - 1) * 7)
        interns.append(
            Intern(
                intern_id=f"I{index:03d}",
                name=name,
                role=role,
                school=random.choice(SCHOOLS),
                major=random.choice(MAJORS_BY_ROLE[role]),
                mentor_id=choose_mentor(role, index),
                join_date=join_date.isoformat(),
                current_week=current_week,
                status="active",
            )
        )
    return interns


def build_mentors() -> list[dict]:
    return [
        {
            "mentor_id": mentor_id,
            "mentor_name": name,
            "department": department,
            "role": role,
        }
        for mentor_id, name, department, role in MENTORS
    ]


def build_weekly_tasks() -> list[dict]:
    rows = []
    for role, tasks in TASK_TEMPLATES.items():
        for week, (task_name, expected_output) in enumerate(tasks, start=1):
            rows.append(
                {
                    "task_id": f"T{role[0]}{week:02d}",
                    "role": role,
                    "week": week,
                    "task_name": task_name,
                    "task_description": f"第 {week} 周完成{task_name}，沉淀可复用材料。",
                    "expected_output": expected_output,
                    "weight": 20,
                }
            )
    return rows


def score_to_status(score: int) -> str:
    if score >= 85:
        return "completed"
    if score >= 60:
        return "in_progress"
    return "at_risk"


def classify_level(fit_score: float) -> str:
    if fit_score >= 85:
        return "高潜"
    if fit_score >= 70:
        return "稳定"
    if fit_score >= 60:
        return "需关注"
    return "高风险"


def classify_risk(fit_score: float, task_score: int, feedback_text: str) -> str:
    risk_keywords = ["偏慢", "不足", "迷茫", "沉默", "不完整", "不够稳定"]
    has_keyword = any(keyword in feedback_text for keyword in risk_keywords)
    if fit_score < 60 or task_score < 50:
        return "高风险"
    if fit_score < 70 or has_keyword:
        return "需关注"
    return "低风险"


def build_progress_and_feedback(interns: list[Intern], tasks: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    task_lookup = {(task["role"], int(task["week"])): task for task in tasks}
    progress_rows = []
    feedback_rows = []
    evaluation_rows = []

    for index, intern in enumerate(interns, start=1):
        base = random.randint(58, 96)
        if index in {4, 11, 17, 20}:
            base = random.randint(42, 66)

        completed_scores = []
        for week in range(1, intern.current_week + 1):
            task = task_lookup[(intern.role, min(week, 5))]
            score = max(35, min(100, base + random.randint(-12, 10)))
            completed_scores.append(score)
            progress_rows.append(
                {
                    "intern_id": intern.intern_id,
                    "task_id": task["task_id"],
                    "week": week,
                    "completion_status": score_to_status(score),
                    "completion_score": score,
                    "submission_text": f"已提交：{task['expected_output']}",
                    "updated_at": f"2026-06-{random.randint(1, 7):02d}",
                }
            )

        task_score = round(sum(completed_scores) / len(completed_scores))
        is_risky = task_score < 68 or index in {4, 11, 17, 20}
        feedback_text = random.choice(RISK_FEEDBACK if is_risky else POSITIVE_FEEDBACK)

        professional_score = max(40, min(100, task_score + random.randint(-8, 8)))
        communication_score = max(40, min(100, task_score + random.randint(-15, 10)))
        initiative_score = max(40, min(100, task_score + random.randint(-18, 12)))
        skill_match_score = max(40, min(100, task_score + random.randint(-10, 10)))
        mentor_score = round((professional_score + communication_score) / 2)

        fit_score = round(
            task_score * 0.30
            + mentor_score * 0.25
            + initiative_score * 0.20
            + communication_score * 0.15
            + skill_match_score * 0.10,
            2,
        )
        level = classify_level(fit_score)
        risk_level = classify_risk(fit_score, task_score, feedback_text)

        feedback_rows.append(
            {
                "feedback_id": f"F{index:03d}",
                "intern_id": intern.intern_id,
                "mentor_id": intern.mentor_id,
                "week": intern.current_week,
                "feedback_text": feedback_text,
                "professional_score": professional_score,
                "communication_score": communication_score,
                "initiative_score": initiative_score,
                "created_at": "2026-06-07",
            }
        )
        evaluation_rows.append(
            {
                "intern_id": intern.intern_id,
                "week": intern.current_week,
                "task_score": task_score,
                "mentor_score": mentor_score,
                "initiative_score": initiative_score,
                "communication_score": communication_score,
                "skill_match_score": skill_match_score,
                "fit_score": fit_score,
                "level": level,
                "risk_level": risk_level,
                "ai_summary": build_ai_summary(intern, level, risk_level, task_score),
            }
        )

    return progress_rows, feedback_rows, evaluation_rows


def build_ai_summary(intern: Intern, level: str, risk_level: str, task_score: int) -> str:
    if risk_level in {"需关注", "高风险"}:
        return (
            f"{intern.name}当前任务完成度为 {task_score} 分，处于{level}状态。"
            "建议导师下周明确一个可交付小任务，并由 HR 跟进一次阶段沟通。"
        )
    return (
        f"{intern.name}当前表现{level}，任务交付和岗位适配整体稳定。"
        "建议继续增加真实业务任务，沉淀可复用成果。"
    )


def main() -> None:
    random.seed(RANDOM_SEED)
    fake = make_fake()
    interns = build_interns(fake)
    mentors = build_mentors()
    tasks = build_weekly_tasks()
    progress, feedback, evaluations = build_progress_and_feedback(interns, tasks)

    write_csv(
        DATA_DIR / "interns.csv",
        [
            "intern_id",
            "name",
            "role",
            "school",
            "major",
            "mentor_id",
            "join_date",
            "current_week",
            "status",
        ],
        [intern.__dict__ for intern in interns],
    )
    write_csv(DATA_DIR / "mentors.csv", ["mentor_id", "mentor_name", "department", "role"], mentors)
    write_csv(
        DATA_DIR / "weekly_tasks.csv",
        ["task_id", "role", "week", "task_name", "task_description", "expected_output", "weight"],
        tasks,
    )
    write_csv(
        DATA_DIR / "intern_progress.csv",
        [
            "intern_id",
            "task_id",
            "week",
            "completion_status",
            "completion_score",
            "submission_text",
            "updated_at",
        ],
        progress,
    )
    write_csv(
        DATA_DIR / "mentor_feedback.csv",
        [
            "feedback_id",
            "intern_id",
            "mentor_id",
            "week",
            "feedback_text",
            "professional_score",
            "communication_score",
            "initiative_score",
            "created_at",
        ],
        feedback,
    )
    write_csv(
        DATA_DIR / "evaluation_results.csv",
        [
            "intern_id",
            "week",
            "task_score",
            "mentor_score",
            "initiative_score",
            "communication_score",
            "skill_match_score",
            "fit_score",
            "level",
            "risk_level",
            "ai_summary",
        ],
        evaluations,
    )

    generator = "Faker" if fake else "fallback name pool"
    print(f"Generated mock data in {DATA_DIR} using {generator}.")
    print(f"Interns: {len(interns)}, tasks: {len(tasks)}, progress rows: {len(progress)}")


if __name__ == "__main__":
    main()
