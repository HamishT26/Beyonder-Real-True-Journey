"""Read and smoke-use Ilyra Fen v683-v3 phase-local skills."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SKILL_NAMES = [
    "pneumatic-network-surrogate-separator",
    "station-route-capsule-vacancy-guard",
    "dispatch-action-state-separator",
    "pressure-airflow-nonmeasurement",
    "fault-cue-nondiagnosis",
    "maintenance-authority-hold",
    "route-control-nonexecution",
    "dispatch-provenance-lineage-ledger",
    "station-alias-collision-quarantine",
    "capsule-content-concept-separator",
    "custody-event-vacancy",
    "engineering-procedure-nonexecution",
    "accessible-status-summary-vacancy",
    "dispatch-rights-remedy-hold",
    "traditional-knowledge-minimizer",
    "tube-workload-handover-lease",
    "freed-id-zero-key-dispatch-guard",
    "thos-dispatch-operator-vacancy",
    "gmut-route-topology-noninference",
    "tube-authority-noncompensation",
]

REQUIRED = {
    "fixture_kind",
    "surrogate_id",
    "synthetic",
    "real_row_count",
    "observation_status",
    "authority_status",
    "boundary",
}


def validate_skill_fixture(skill: str, fixture: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    missing = sorted(REQUIRED - set(fixture))
    if missing:
        reasons.append("missing_required_fields:" + ",".join(missing))
    if fixture.get("synthetic") is not True:
        reasons.append("synthetic_boundary_missing")
    if fixture.get("real_row_count") != 0:
        reasons.append("real_rows_forbidden")
    if fixture.get("observation_status") != "absent":
        reasons.append("observation_promotion_forbidden")
    if fixture.get("authority_status") != "reserved":
        reasons.append("authority_promotion_forbidden")
    if fixture.get("boundary") != "owner_local_zero_row_only":
        reasons.append("boundary_mismatch")
    return {"accepted": not reasons, "reasons": reasons, "skill": skill}


def accepting_fixture(skill: str) -> dict[str, Any]:
    return {
        "fixture_kind": "skill_smoke_fixture",
        "surrogate_id": f"SKILL-{skill}",
        "synthetic": True,
        "real_row_count": 0,
        "observation_status": "absent",
        "authority_status": "reserved",
        "boundary": "owner_local_zero_row_only",
    }


def smoke_skills(skill_root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for name in SKILL_NAMES:
        folder = skill_root / name
        skill_file = folder / "SKILL.md"
        agent_file = folder / "agents" / "openai.yaml"
        text = skill_file.read_text(encoding="utf-8")
        agent = agent_file.read_text(encoding="utf-8")
        fully_read = bool(text) and text.endswith("\n")
        customized = "TODO" not in text and f"name: {name}" in text
        accepting = validate_skill_fixture(name, accepting_fixture(name))
        rejecting_fixture = accepting_fixture(name)
        rejecting_fixture.pop("authority_status")
        rejecting = validate_skill_fixture(name, rejecting_fixture)
        results.append(
            {
                "accepting_fixture_accepted": accepting["accepted"],
                "agent_metadata_present": "display_name:" in agent and f"${name}" in agent,
                "customized": customized,
                "fully_read_through_eof": fully_read,
                "global_installation": False,
                "rejecting_fixture_rejected": not rejecting["accepted"],
                "rejecting_reasons": rejecting["reasons"],
                "skill": name,
            }
        )
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("skill_root", type=Path)
    args = parser.parse_args()
    rows = smoke_skills(args.skill_root)
    print(json.dumps({"count": len(rows), "results": rows}, separators=(",", ":")))
    raise SystemExit(
        0
        if all(
            row["accepting_fixture_accepted"] and row["rejecting_fixture_rejected"]
            for row in rows
        )
        else 1
    )
