"""Validate scoring and risk rules against generated CSV data."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.risk_service import assess_risk
from services.scoring_service import evaluate_fit


DATA_DIR = ROOT / "data"


def main() -> int:
    evaluations = pd.read_csv(DATA_DIR / "evaluation_results.csv")
    feedback = pd.read_csv(DATA_DIR / "mentor_feedback.csv")
    feedback_by_intern = feedback.set_index("intern_id")["feedback_text"].to_dict()

    score_mismatches = []
    risk_mismatches = []

    for record in evaluations.to_dict(orient="records"):
        scored = evaluate_fit(record)
        if abs(scored.fit_score - float(record["fit_score"])) > 0.001 or scored.level != record["level"]:
            score_mismatches.append(
                {
                    "intern_id": record["intern_id"],
                    "expected_score": record["fit_score"],
                    "actual_score": scored.fit_score,
                    "expected_level": record["level"],
                    "actual_level": scored.level,
                }
            )

        feedback_text = feedback_by_intern.get(record["intern_id"], "")
        assessed = assess_risk(record, feedback_text)
        if assessed.risk_level != record["risk_level"]:
            risk_mismatches.append(
                {
                    "intern_id": record["intern_id"],
                    "expected_risk": record["risk_level"],
                    "actual_risk": assessed.risk_level,
                }
            )

    print(f"evaluations: {len(evaluations)}")
    print(f"score_mismatches: {len(score_mismatches)}")
    print(f"risk_mismatches: {len(risk_mismatches)}")
    print("level_counts:")
    print(evaluations["level"].value_counts().to_string())
    print("risk_counts:")
    print(evaluations["risk_level"].value_counts().to_string())

    if score_mismatches:
        print("score mismatch samples:")
        print(score_mismatches[:5])
    if risk_mismatches:
        print("risk mismatch samples:")
        print(risk_mismatches[:5])

    return 1 if score_mismatches or risk_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
