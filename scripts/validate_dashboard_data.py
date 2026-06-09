"""Validate data aggregation used by the first dashboard pages."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.data_service import get_dashboard_summary, get_intern_profile, get_intern_options, parse_intern_id


def main() -> int:
    summary = get_dashboard_summary()
    options = get_intern_options()
    first_profile = get_intern_profile(parse_intern_id(options[0]))

    metrics = summary["metrics"]
    dataset = summary["dataset"]
    role_summary = summary["role_summary"]
    risk_records = summary["risk_records"]

    checks = {
        "total_is_20": metrics["total_interns"] == 20,
        "dataset_rows_match": len(dataset) == 20,
        "role_summary_has_3_roles": len(role_summary) == 3,
        "intern_options_match": len(options) == 20,
        "risk_records_match": len(risk_records) == metrics["risk_count"],
        "profile_has_tasks": len(first_profile["task_records"]) > 0,
        "profile_has_actions": len(first_profile["risk"].actions) > 0,
    }

    for name, passed in checks.items():
        print(f"{name}: {passed}")

    print("metrics:", metrics)
    print("role_summary:")
    print(role_summary.to_string(index=False))

    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
