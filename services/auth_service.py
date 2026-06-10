"""Role and permission simulation helpers for the Streamlit demo."""

from __future__ import annotations

from typing import Iterable

import pandas as pd
import streamlit as st


ROLE_HR = "HR"
ROLE_MENTOR = "导师"
ROLE_INTERN = "实习生"
ROLE_RECRUITER = "招聘同学"

ROLES = [ROLE_HR, ROLE_MENTOR, ROLE_INTERN, ROLE_RECRUITER]

ROLE_DESCRIPTIONS = {
    ROLE_HR: "查看全局看板、个人画像、周报与导师反馈。",
    ROLE_MENTOR: "查看自己带教的实习生，并保存导师反馈。",
    ROLE_INTERN: "查看自己的画像与成长建议。",
    ROLE_RECRUITER: "查看整体适岗情况和风险名单，辅助招聘复盘。",
}

PAGE_PERMISSIONS = {
    "home": ROLES,
    "hr_dashboard": [ROLE_HR, ROLE_RECRUITER],
    "intern_profile": ROLES,
    "mentor_assistant": [ROLE_HR, ROLE_MENTOR],
    "weekly_report": [ROLE_HR, ROLE_RECRUITER],
    "growth_assistant": [ROLE_HR, ROLE_MENTOR, ROLE_INTERN],
}


def can_access(role: str, page_key: str) -> bool:
    """Return whether a role can access a page in the demo permission model."""
    return role in PAGE_PERMISSIONS.get(page_key, [])


def build_intern_options(dataset: pd.DataFrame) -> list[str]:
    """Build selector labels from an intern dataset."""
    if dataset.empty:
        return []
    return [
        f"{row.name} | {row.role} | {row.intern_id}"
        for row in dataset[["intern_id", "name", "role"]].itertuples(index=False)
    ]


def parse_option_id(option: str) -> str:
    """Extract the id segment from a Streamlit selector label."""
    return option.split("|")[-1].strip()


def scope_dataset(
    dataset: pd.DataFrame,
    role: str,
    mentor_id: str | None = None,
    intern_id: str | None = None,
) -> pd.DataFrame:
    """Apply role-specific data visibility rules to an intern dataset."""
    if role == ROLE_MENTOR and mentor_id:
        return dataset[dataset["mentor_id"] == mentor_id].copy()
    if role == ROLE_INTERN and intern_id:
        return dataset[dataset["intern_id"] == intern_id].copy()
    return dataset.copy()


def role_permission_summary() -> list[dict[str, str]]:
    """Return page permission rows for display and validation."""
    return [
        {
            "页面": "HR Dashboard",
            "可访问角色": "、".join(PAGE_PERMISSIONS["hr_dashboard"]),
            "说明": "全局指标、风险名单与导出。",
        },
        {
            "页面": "Intern Profile",
            "可访问角色": "、".join(PAGE_PERMISSIONS["intern_profile"]),
            "说明": "HR/招聘看全量，导师看带教范围，实习生看本人。",
        },
        {
            "页面": "Mentor Assistant",
            "可访问角色": "、".join(PAGE_PERMISSIONS["mentor_assistant"]),
            "说明": "导师反馈分析、保存与历史记录。",
        },
        {
            "页面": "AI Weekly Report",
            "可访问角色": "、".join(PAGE_PERMISSIONS["weekly_report"]),
            "说明": "管理周报与风险名单导出。",
        },
        {
            "页面": "Intern Growth Assistant",
            "可访问角色": "、".join(PAGE_PERMISSIONS["growth_assistant"]),
            "说明": "个人成长建议与导师辅导参考。",
        },
    ]


def render_role_selector() -> str:
    """Render the shared sidebar role selector."""
    role = st.sidebar.selectbox("当前角色（权限模拟）", ROLES, key="current_role")
    st.sidebar.caption(ROLE_DESCRIPTIONS[role])
    st.sidebar.info("当前仅为角色视角模拟，不等同于真实登录鉴权。")
    return role


def require_page_access(role: str, page_key: str) -> None:
    """Stop rendering when a simulated role has no access to the current page."""
    if can_access(role, page_key):
        return

    allowed = "、".join(PAGE_PERMISSIONS.get(page_key, []))
    st.warning(f"当前角色「{role}」无权访问该页面。可访问角色：{allowed}。")
    st.stop()


def render_scope_controls(role: str, dataset: pd.DataFrame, page_key: str) -> pd.DataFrame:
    """Render account simulation controls and return the visible intern dataset."""
    if role == ROLE_MENTOR:
        mentors = (
            dataset[["mentor_id", "mentor_name"]]
            .drop_duplicates()
            .sort_values(["mentor_name", "mentor_id"])
        )
        mentor_options = [f"{row.mentor_name} | {row.mentor_id}" for row in mentors.itertuples(index=False)]
        selected_mentor = st.sidebar.selectbox("模拟导师账号", mentor_options, key=f"{page_key}_mentor_scope")
        mentor_id = parse_option_id(selected_mentor)
        scoped = scope_dataset(dataset, role, mentor_id=mentor_id)
        st.sidebar.caption(f"当前仅显示该导师带教的 {len(scoped)} 名实习生。")
        return scoped

    if role == ROLE_INTERN:
        intern_options = build_intern_options(dataset)
        selected_intern = st.sidebar.selectbox("模拟实习生账号", intern_options, key=f"{page_key}_intern_scope")
        intern_id = parse_option_id(selected_intern)
        scoped = scope_dataset(dataset, role, intern_id=intern_id)
        st.sidebar.caption("当前仅显示本人数据。")
        return scoped

    st.sidebar.caption("当前角色可查看全部实习生数据。")
    return scope_dataset(dataset, role)


def ensure_options(options: Iterable[str]) -> list[str]:
    """Normalize options and stop the page with a clear message when empty."""
    normalized = list(options)
    if not normalized:
        st.warning("当前角色范围内暂无可查看的实习生数据。")
        st.stop()
    return normalized
