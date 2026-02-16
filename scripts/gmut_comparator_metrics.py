#!/usr/bin/env python3
"""
Generate reproducible GMUT comparator metrics from latest Body artifacts.

Current scope (v0):
- Uses `docs/body-track-smoke-latest.json` simulation metrics.
- Computes deviation statistics against a baseline ratio of 1.0.
- Emits timestamped + latest JSON/markdown artifacts under docs/.
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict


def _extract_gamma_ratios(body_smoke_json: Path) -> Dict[str, float]:
    payload = json.loads(body_smoke_json.read_text(encoding="utf-8"))
    for step in payload.get("steps", []):
        if step.get("name") != "run_gmut_simulation":
            continue
        metrics = step.get("metrics", {})
        ratios = metrics.get("gamma_ratios", {})
        if isinstance(ratios, dict):
            return {str(key): float(value) for key, value in ratios.items()}
    return {}


def _markdown(generated_utc: str, payload: Dict[str, object]) -> str:
    return "\n".join(
        [
            "# GMUT Comparator Metrics Report",
            "",
            f"- generated_utc: `{generated_utc}`",
            f"- status: **{payload['status']}**",
            f"- baseline_ratio: `{payload['baseline_ratio']}`",
            f"- max_abs_deviation: `{payload['max_abs_deviation']}`",
            f"- mean_abs_deviation: `{payload['mean_abs_deviation']}`",
            f"- rmse: `{payload['rmse']}`",
            f"- rejection_threshold: `{payload['rejection_threshold']}`",
            "",
            "## Gamma ratios",
            "```json",
            json.dumps(payload["gamma_ratios"], indent=2),
            "```",
            "",
            "## Note",
            "Internal comparator metrics only (GMUT simulation vs baseline 1.0); not an external empirical fit.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate GMUT comparator metrics artifacts.")
    parser.add_argument(
        "--body-smoke-json",
        default="docs/body-track-smoke-latest.json",
        help="Body smoke JSON artifact containing simulation metrics.",
    )
    parser.add_argument(
        "--reports-dir",
        default="docs/mind-track-runs",
        help="Directory for timestamped outputs.",
    )
    parser.add_argument(
        "--latest-json",
        default="docs/mind-track-gmut-comparator-latest.json",
        help="Path for latest JSON output.",
    )
    parser.add_argument(
        "--latest-md",
        default="docs/mind-track-gmut-comparator-latest.md",
        help="Path for latest markdown output.",
    )
    parser.add_argument(
        "--rejection-threshold",
        type=float,
        default=0.12,
        help="Maximum allowed absolute deviation from baseline ratio.",
    )
    args = parser.parse_args()

    body_smoke_json = Path(args.body_smoke_json)
    if not body_smoke_json.exists():
        raise SystemExit(f"Missing input artifact: {body_smoke_json}")

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    ratios = _extract_gamma_ratios(body_smoke_json)
    if not ratios:
        raise SystemExit("No gamma ratio metrics found in body smoke artifact.")

    baseline = 1.0
    deviations = [abs(value - baseline) for value in ratios.values()]
    max_abs_deviation = max(deviations)
    mean_abs_deviation = sum(deviations) / len(deviations)
    rmse = math.sqrt(sum((value - baseline) ** 2 for value in ratios.values()) / len(ratios))
    status = "PASS" if max_abs_deviation <= args.rejection_threshold else "WARN"

    payload: Dict[str, object] = {
        "generated_utc": generated_utc,
        "status": status,
        "baseline_ratio": baseline,
        "gamma_ratios": ratios,
        "max_abs_deviation": round(max_abs_deviation, 8),
        "mean_abs_deviation": round(mean_abs_deviation, 8),
        "rmse": round(rmse, 8),
        "rejection_threshold": args.rejection_threshold,
    }

    latest_json = Path(args.latest_json)
    latest_md = Path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)

    timestamped_json = reports_dir / f"{stamp}-gmut-comparator-metrics.json"
    timestamped_md = reports_dir / f"{stamp}-gmut-comparator-metrics.md"
    markdown = _markdown(generated_utc, payload)

    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"status={status}")
    print(f"timestamped_json={timestamped_json}")
    print(f"timestamped_md={timestamped_md}")
    print(f"latest_json={latest_json}")
    print(f"latest_md={latest_md}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
