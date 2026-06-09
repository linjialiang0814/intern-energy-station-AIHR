"""Validate score explanation details for intern profiles."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.data_service import get_evaluation_dataset
from services.scoring_service import SCORE_WEIGHTS, evaluate_fit


def main() -> int:
    dataset = get_evaluation_dataset()
    failures = []

    for record in dataset.to_dict(orient="records"):
        score = evaluate_fit(record)
        contribution_sum = round(sum(item.contribution for item in score.dimensions), 2)
        checks = {
            "has_all_dimensions": len(score.dimensions) == len(SCORE_WEIGHTS),
            "contribution_matches_fit": abs(contribution_sum - score.fit_score) <= 0.01,
            "has_level_explanation": bool(score.level_explanation),
            "has_dimension_interpretation": all(item.interpretation for item in score.dimensions),
        }
        if not all(checks.values()):
            failures.append({"intern_id": record["intern_id"], "checks": checks})

    print(f"profiles_checked: {len(dataset)}")
    print(f"failures: {len(failures)}")
    if failures:
        print(failures[:3])
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
