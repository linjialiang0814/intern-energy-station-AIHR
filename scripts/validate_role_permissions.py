"""Validate role permission rules and scoped data visibility."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.auth_service import ROLE_HR, ROLE_INTERN, ROLE_MENTOR, ROLE_RECRUITER, can_access, scope_dataset
from services.data_service import get_evaluation_dataset


def main() -> int:
    dataset = get_evaluation_dataset()
    assert not dataset.empty

    assert can_access(ROLE_HR, "hr_dashboard")
    assert can_access(ROLE_RECRUITER, "hr_dashboard")
    assert not can_access(ROLE_MENTOR, "hr_dashboard")
    assert not can_access(ROLE_INTERN, "hr_dashboard")

    assert can_access(ROLE_MENTOR, "mentor_assistant")
    assert not can_access(ROLE_RECRUITER, "mentor_assistant")

    mentor_id = dataset.iloc[0]["mentor_id"]
    scoped_mentor = scope_dataset(dataset, ROLE_MENTOR, mentor_id=mentor_id)
    assert len(scoped_mentor) > 0
    assert set(scoped_mentor["mentor_id"]) == {mentor_id}

    intern_id = dataset.iloc[0]["intern_id"]
    scoped_intern = scope_dataset(dataset, ROLE_INTERN, intern_id=intern_id)
    assert len(scoped_intern) == 1
    assert scoped_intern.iloc[0]["intern_id"] == intern_id

    print("Role permission validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
