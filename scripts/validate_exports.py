"""Validate export helpers for CSV and Markdown outputs."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.data_service import get_dashboard_summary, get_intern_profile, get_intern_options, parse_intern_id
from services.export_service import build_dashboard_markdown, build_profile_markdown, dataframe_to_csv_bytes


def main() -> int:
    summary = get_dashboard_summary()
    option = get_intern_options()[0]
    profile = get_intern_profile(parse_intern_id(option))

    dashboard_md = build_dashboard_markdown(summary)
    profile_md = build_profile_markdown(profile)
    csv_bytes = dataframe_to_csv_bytes(summary["dataset"].head(3))

    checks = {
        "dashboard_md_has_title": "# 实习能量站 HR 总览摘要" in dashboard_md,
        "dashboard_md_has_metrics": "核心指标" in dashboard_md,
        "profile_md_has_title": "实习生个人画像" in profile_md,
        "profile_md_has_score": "评分贡献拆解" in profile_md,
        "csv_has_bom": csv_bytes.startswith(b"\xef\xbb\xbf"),
        "csv_has_content": len(csv_bytes) > 100,
    }

    for name, passed in checks.items():
        print(f"{name}: {passed}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
