#!/usr/bin/env python3
"""Build v476 THOS v7/v8 closure and v477 handoff artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "trinity-live-traces"

GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]

SOURCE_ARTIFACTS = [
    "v476-thos-v1-x1-suite-map-seed-v1.json",
    "v476-thos-v2-x2-required-row-gate-v1.json",
    "v476-thos-v3-x2-handoff-contract-gate-v1.json",
    "v476-thos-v4-x2-candidate-preflight-gate-v1.json",
    "v476-thos-v5-x2-dry-run-rehearsal-gate-v1.json",
    "v476-thos-v6-x2-approval-marker-gate-v1.json",
    "v476-thos-v3-x1-cli-lane-completion-notice-v1.json",
]

RUN_STATUS_ARTIFACTS = [
    "v476-thos-v1-x1-run-status-v1.json",
    "v476-thos-v1-x2-run-status-v1.json",
    "v476-thos-v2-x1-run-status-v1.json",
    "v476-thos-v2-x2-run-status-v1.json",
    "v476-thos-v3-x1-run-status-v1.json",
    "v476-thos-v3-x2-run-status-v1.json",
    "v476-thos-v4-x1-run-status-v1.json",
    "v476-thos-v4-x2-run-status-v1.json",
    "v476-thos-v5-x1-run-status-v1.json",
    "v476-thos-v5-x2-run-status-v1.json",
    "v476-thos-v6-x1-run-status-v1.json",
    "v476-thos-v6-x2-run-status-v1.json",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def nz_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_ref(name: str) -> dict[str, Any]:
    path = ARTIFACT_ROOT / name
    rel = path.relative_to(REPO_ROOT).as_posix()
    if not path.exists():
        return {"path": rel, "status": "OPEN_GAP_MISSING_SOURCE"}
    payload = read_json(path) if path.suffix == ".json" else {}
    return {
        "aggregate_status": payload.get("aggregate_status"),
        "bytes": path.stat().st_size,
        "path": rel,
        "sha256": sha256_file(path),
        "status": "PASS_SHAPE_ONLY",
    }


def row(row_id: str, status: str, message: str, evidence: object | None = None) -> dict[str, Any]:
    return {
        "evidence": evidence,
        "message": message,
        "row_id": row_id,
        "status": status,
    }


def fixture(case_id: str, case: dict[str, Any], expected: str) -> dict[str, Any]:
    observed = "OPEN_GAP"
    if case.get("missing_source") or case.get("marker_review_required"):
        observed = "OPEN_GAP"
    elif case.get("raw_lane_text_published") or case.get("candidate_promoted") or case.get("approval_granted"):
        observed = "FAIL_BLOCKER"
    elif case.get("production_claim") or case.get("moves_gmut_gate") or case.get("missing_handoff"):
        observed = "FAIL_BLOCKER"
    elif case.get("closure_ready") and case.get("metadata_only"):
        observed = "PASS_SHAPE_ONLY"
    return {
        "case": case,
        "case_id": case_id,
        "expected": expected,
        "observed": observed,
        "status": "EXPECTED_CONFIRMED" if observed == expected else "EXPECTED_FAIL_MISMATCH",
    }


def common_fixtures() -> list[dict[str, Any]]:
    return [
        fixture("closure_ready_expected_pass", {"closure_ready": True, "metadata_only": True}, "PASS_SHAPE_ONLY"),
        fixture("missing_source_expected_open_gap", {"missing_source": True}, "OPEN_GAP"),
        fixture("marker_review_required_expected_open_gap", {"marker_review_required": True}, "OPEN_GAP"),
        fixture("raw_lane_text_publication_expected_fail", {"raw_lane_text_published": True}, "FAIL_BLOCKER"),
        fixture("candidate_promotion_expected_fail", {"candidate_promoted": True}, "FAIL_BLOCKER"),
        fixture("approval_granted_expected_fail", {"approval_granted": True}, "FAIL_BLOCKER"),
        fixture("production_claim_expected_fail", {"production_claim": True}, "FAIL_BLOCKER"),
        fixture("missing_handoff_expected_fail", {"missing_handoff": True}, "FAIL_BLOCKER"),
        fixture("gmut_gate_move_expected_fail", {"moves_gmut_gate": True}, "FAIL_BLOCKER"),
    ]


def aggregate_status(rows: list[dict[str, Any]], fixtures: list[dict[str, Any]], pass_label: str) -> str:
    if any(item["status"].startswith("FAIL") for item in rows):
        return "FAIL_BLOCKER"
    if any(item["status"] != "EXPECTED_CONFIRMED" for item in fixtures):
        return "FAIL_FIXTURE_MISMATCH"
    if any(item["status"].startswith("OPEN_GAP") for item in rows if item["row_id"] != "marker_review_open_gap"):
        return "OPEN_GAP_V476_CLOSURE_NOT_READY"
    return pass_label


def marker_review_summary() -> dict[str, Any]:
    completion = read_json(ARTIFACT_ROOT / "v476-thos-v3-x1-cli-lane-completion-notice-v1.json")
    lanes = []
    for lane in completion.get("lanes", []):
        final_count = int(lane.get("final_message_sensitive_marker_count", 0))
        stderr_count = int(lane.get("stderr_sensitive_marker_count_unpublished", 0))
        lanes.append(
            {
                "final_marker_count": final_count,
                "lane": lane.get("lane"),
                "review_state": "OPEN_GAP_REVIEW_REQUIRED" if final_count or stderr_count else "PASS_SHAPE_ONLY_METADATA_CLEAN",
                "stderr_marker_count_unpublished": stderr_count,
            }
        )
    return {
        "aggregate_status": completion.get("aggregate_status"),
        "lanes": lanes,
        "raw_lane_text_published": False,
    }


def build_v7_x1(source_refs: list[dict[str, Any]], status_refs: list[dict[str, Any]], generated_at: str, started_at_nz: str) -> list[Path]:
    phase = "v476-thos-v7-x1"
    next_phase = "v476-thos-v7-x2"
    marker = marker_review_summary()
    fixtures = common_fixtures()
    resolution_options = [
        {
            "claim_ceiling": "metadata-only option; no raw lane text review is performed here",
            "option_id": "marker-hold-open",
            "option_state": "RECOMMENDED_DEFAULT",
            "required_approval": "none",
            "result": "carry marker review as open gap",
        },
        {
            "claim_ceiling": "requires separate exact approval before any raw text inspection",
            "option_id": "exact-review-packet",
            "option_state": "AVAILABLE_REQUIRES_APPROVAL",
            "required_approval": "exact path and review scope packet",
            "result": "reviewer may inspect specific lane final text only if approved",
        },
        {
            "claim_ceiling": "not allowed under current scope",
            "option_id": "publish-raw-lane-text",
            "option_state": "DENIED",
            "required_approval": "not approved",
            "result": "blocked",
        },
    ]
    approval_templates = [
        {
            "candidate_family": family,
            "packet_state": "TEMPLATE_ONLY_NOT_APPROVED",
            "required_fields": [
                "candidate_family",
                "exact_paths",
                "allowed_probe_level",
                "body_preservation_rule",
                "publication_boundary",
                "rollback_plan",
                "spend_ceiling",
            ],
        }
        for family in ["command", "skill", "system_expansion"]
    ]
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if all(item["status"] == "PASS_SHAPE_ONLY" for item in source_refs) else "OPEN_GAP_SOURCE_REFS",
            "v476 source artifacts were hashed for closure routing.",
            {"source_count": len(source_refs)},
        ),
        row(
            "run_status_refs",
            "PASS_SHAPE_ONLY" if all(item["status"] == "PASS_SHAPE_ONLY" for item in status_refs) else "OPEN_GAP_RUN_STATUS_REFS",
            "v476 run-status artifacts were hashed for closure routing.",
            {"status_count": len(status_refs)},
        ),
        row(
            "marker_review_open_gap",
            "OPEN_GAP_MARKER_REVIEW_REQUIRED" if marker.get("aggregate_status") == "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW" else "PASS_SHAPE_ONLY",
            "Marker review is carried as metadata-only open gap unless a separate exact review packet is approved.",
            marker,
        ),
        row(
            "approval_templates",
            "PASS_SHAPE_ONLY",
            "Approval packet templates exist but do not approve any candidate promotion.",
            {"template_count": len(approval_templates)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "v7 x1 does not publish raw lane text, approve candidates, or move GMUT gates.",
            {"gmut_gates_open": GMUT_GATES},
        ),
    ]
    status = aggregate_status(rows, fixtures, "PASS_SHAPE_ONLY_V476_RESOLUTION_OPTIONS_READY")
    payload = {
        "aggregate_status": status,
        "approval_packet_templates": approval_templates,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "marker_review_summary": marker,
        "next_expected_phase": next_phase,
        "phase_slug": phase,
        "preflight_rows": rows,
        "resolution_options": resolution_options,
        "source_refs": source_refs,
        "started_at_nz": started_at_nz,
        "status_refs": status_refs,
    }
    return write_phase_pair(phase, "resolution-options", payload, rows, status, next_phase, generated_at, started_at_nz)


def build_v7_x2(generated_at: str, started_at_nz: str) -> list[Path]:
    phase = "v476-thos-v7-x2"
    next_phase = "v476-thos-v8-x1"
    source = source_ref("v476-thos-v7-x1-resolution-options-v1.json")
    source_status = source_ref("v476-thos-v7-x1-run-status-v1.json")
    payload_in = read_json(ARTIFACT_ROOT / "v476-thos-v7-x1-resolution-options-v1.json")
    fixtures = common_fixtures()
    denied_options = [item["option_id"] for item in payload_in.get("resolution_options", []) if item.get("option_state") == "DENIED"]
    template_not_approved = [
        item["candidate_family"]
        for item in payload_in.get("approval_packet_templates", [])
        if item.get("packet_state") == "TEMPLATE_ONLY_NOT_APPROVED"
    ]
    rows = [
        row(
            "source_refs",
            "PASS_SHAPE_ONLY" if source["status"] == "PASS_SHAPE_ONLY" and source_status["status"] == "PASS_SHAPE_ONLY" else "OPEN_GAP_SOURCE_REFS",
            "v7 x1 resolution options and run status were checked.",
            {"source": source, "source_status": source_status},
        ),
        row(
            "resolution_options",
            "PASS_SHAPE_ONLY" if "publish-raw-lane-text" in denied_options else "FAIL_RAW_PUBLICATION_NOT_DENIED",
            "Raw lane text publication remains denied.",
            {"denied_options": denied_options},
        ),
        row(
            "approval_templates",
            "PASS_SHAPE_ONLY" if sorted(template_not_approved) == ["command", "skill", "system_expansion"] else "FAIL_TEMPLATE_BOUNDARY",
            "All approval templates remain template-only and not approved.",
            {"template_not_approved": template_not_approved},
        ),
        row(
            "marker_review_open_gap",
            "OPEN_GAP_MARKER_REVIEW_REQUIRED" if payload_in.get("marker_review_summary", {}).get("aggregate_status") == "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW" else "PASS_SHAPE_ONLY",
            "Marker review is preserved as an open metadata condition.",
            payload_in.get("marker_review_summary"),
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "v7 x2 gates options only; it does not approve writes, install candidates, or move GMUT gates.",
            {"gmut_gates_open": GMUT_GATES},
        ),
    ]
    status = aggregate_status(rows, fixtures, "PASS_SHAPE_ONLY_V476_RESOLUTION_GATE_READY")
    payload = {
        "aggregate_status": status,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": next_phase,
        "phase_slug": phase,
        "preflight_rows": rows,
        "source_phase": "v476-thos-v7-x1",
        "source_refs": [source, source_status],
    }
    return write_phase_pair(phase, "resolution-gate", payload, rows, status, next_phase, generated_at, started_at_nz)


def build_v8_x1(source_refs: list[dict[str, Any]], status_refs: list[dict[str, Any]], generated_at: str, started_at_nz: str) -> list[Path]:
    phase = "v476-thos-v8-x1"
    next_phase = "v476-thos-v8-x2"
    v7_gate = source_ref("v476-thos-v7-x2-resolution-gate-v1.json")
    marker = marker_review_summary()
    fixtures = common_fixtures()
    closure_findings = [
        "v476 built suite-map, required-row, handoff-contract, candidate-preflight, dry-run, approval-marker, and resolution-option gates",
        "all candidate families remain candidate-only and uninstalled",
        "all approval rows deny promotion until exact packet scope exists",
        "raw lane text remains unpublished",
        "marker review remains open as metadata-only condition",
        "all six GMUT gates remain open",
    ]
    rows = [
        row(
            "v7_gate",
            "PASS_SHAPE_ONLY" if v7_gate["status"] == "PASS_SHAPE_ONLY" else "OPEN_GAP_V7_GATE",
            "v7 x2 resolution gate was checked before closure audit.",
            v7_gate,
        ),
        row(
            "source_hash_chain",
            "PASS_SHAPE_ONLY" if all(item["status"] == "PASS_SHAPE_ONLY" for item in source_refs + status_refs) else "OPEN_GAP_SOURCE_HASH_CHAIN",
            "v476 source and status refs were hashed.",
            {"source_count": len(source_refs), "status_count": len(status_refs)},
        ),
        row(
            "marker_review_open_gap",
            "OPEN_GAP_MARKER_REVIEW_REQUIRED" if marker.get("aggregate_status") == "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW" else "PASS_SHAPE_ONLY",
            "Marker review remains open and is not hidden.",
            marker,
        ),
        row(
            "closure_findings",
            "PASS_SHAPE_ONLY",
            "v476 closure findings are recorded with claim ceilings intact.",
            {"finding_count": len(closure_findings)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "v8 x1 closure audit does not certify production readiness or move GMUT gates.",
            {"gmut_gates_open": GMUT_GATES},
        ),
    ]
    status = aggregate_status(rows, fixtures, "PASS_SHAPE_ONLY_V476_CLOSURE_AUDIT_READY")
    payload = {
        "aggregate_status": status,
        "closure_findings": closure_findings,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "marker_review_summary": marker,
        "next_expected_phase": next_phase,
        "phase_slug": phase,
        "preflight_rows": rows,
        "source_refs": source_refs,
        "started_at_nz": started_at_nz,
        "status_refs": status_refs,
    }
    return write_phase_pair(phase, "closure-audit", payload, rows, status, next_phase, generated_at, started_at_nz)


def build_v8_x2(source_refs: list[dict[str, Any]], status_refs: list[dict[str, Any]], generated_at: str, started_at_nz: str) -> list[Path]:
    phase = "v476-thos-v8-x2"
    next_phase = "v477-thos-v1-x1"
    closure = source_ref("v476-thos-v8-x1-closure-audit-v1.json")
    closure_status = source_ref("v476-thos-v8-x1-run-status-v1.json")
    fixtures = common_fixtures()
    handoff_open_gaps = [
        "Arby/Aster marker-review metadata remains open unless exact review packet is approved",
        "no candidates are approved for live write or promotion",
        "connector/cloud writes remain denied without separate approval",
        "all six GMUT gates remain open",
    ]
    rows = [
        row(
            "closure_sources",
            "PASS_SHAPE_ONLY" if closure["status"] == "PASS_SHAPE_ONLY" and closure_status["status"] == "PASS_SHAPE_ONLY" else "OPEN_GAP_CLOSURE_SOURCE",
            "v8 x1 closure audit and run status were checked.",
            {"closure": closure, "closure_status": closure_status},
        ),
        row(
            "handoff_open_gaps",
            "PASS_SHAPE_ONLY",
            "v477 handoff carries open gaps explicitly.",
            {"open_gap_count": len(handoff_open_gaps)},
        ),
        row(
            "source_hash_chain",
            "PASS_SHAPE_ONLY" if all(item["status"] == "PASS_SHAPE_ONLY" for item in source_refs + status_refs) else "OPEN_GAP_SOURCE_HASH_CHAIN",
            "v476 source and status refs were preserved for v477.",
            {"source_count": len(source_refs), "status_count": len(status_refs)},
        ),
        row(
            "claim_boundary",
            "PASS_SHAPE_ONLY",
            "v8 x2 handoff does not approve writes, install candidates, certify production readiness, or move GMUT gates.",
            {"gmut_gates_open": GMUT_GATES},
        ),
    ]
    status = aggregate_status(rows, fixtures, "PASS_SHAPE_ONLY_V476_TO_V477_HANDOFF_READY")
    payload = {
        "aggregate_status": status,
        "fixtures": fixtures,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "handoff_open_gaps": handoff_open_gaps,
        "next_expected_phase": next_phase,
        "phase_slug": phase,
        "preflight_rows": rows,
        "source_phase": "v476-thos-v8-x1",
        "source_refs": source_refs + [closure, closure_status],
        "started_at_nz": started_at_nz,
        "status_refs": status_refs,
    }
    return write_phase_pair(phase, "v477-handoff", payload, rows, status, next_phase, generated_at, started_at_nz)


def write_phase_pair(
    phase: str,
    noun: str,
    payload: dict[str, Any],
    rows: list[dict[str, Any]],
    status: str,
    next_phase: str,
    generated_at: str,
    started_at_nz: str,
) -> list[Path]:
    artifact_json = ARTIFACT_ROOT / f"{phase}-{noun}-v1.json"
    artifact_md = ARTIFACT_ROOT / f"{phase}-{noun}-v1.md"
    status_json = ARTIFACT_ROOT / f"{phase}-run-status-v1.json"
    status_md = ARTIFACT_ROOT / f"{phase}-run-status-v1.md"
    write_json(artifact_json, payload)
    status_payload = {
        "aggregate_status": status,
        "generated_at_utc": generated_at,
        "gmut_gate_effect": "none_open_not_tested",
        "gmut_gates_open": GMUT_GATES,
        "next_expected_phase": next_phase,
        "phase_slug": phase,
        "rows": rows,
        "started_at_nz": started_at_nz,
    }
    write_json(status_json, status_payload)
    row_lines = "\n".join(f"- `{item['row_id']}`: `{item['status']}`" for item in rows)
    title = phase.replace("-", " ").upper()
    write_md(
        artifact_md,
        f"""
# {title} {noun.replace('-', ' ').title()}

NZ start: `{started_at_nz}`
Generated UTC: `{generated_at}`

Status: `{status}`

Rows:

{row_lines}

Raw lane text remains unpublished. Candidate promotion and live write remain denied unless an exact approval packet is later granted.

All six GMUT gates remain open.
""",
    )
    write_md(
        status_md,
        f"""
# {title} Run Status

NZ start: `{started_at_nz}`
Generated UTC: `{generated_at}`

Status: `{status}`
Next expected phase: `{next_phase}`

Rows:

{row_lines}

No runtime transport, session streams, image captures, auth material, plugin-cache bodies, user-skill bodies, or raw sibling transport are published.

All six GMUT gates remain open.
""",
    )
    return [artifact_json, artifact_md, status_json, status_md]


def build_all() -> list[Path]:
    generated_at = utc_now()
    started_at_nz = nz_now()
    source_refs = [source_ref(name) for name in SOURCE_ARTIFACTS]
    status_refs = [source_ref(name) for name in RUN_STATUS_ARTIFACTS]
    written: list[Path] = []
    written.extend(build_v7_x1(source_refs, status_refs, generated_at, started_at_nz))
    written.extend(build_v7_x2(generated_at, started_at_nz))
    source_refs = source_refs + [source_ref("v476-thos-v7-x1-resolution-options-v1.json"), source_ref("v476-thos-v7-x2-resolution-gate-v1.json")]
    status_refs = status_refs + [source_ref("v476-thos-v7-x1-run-status-v1.json"), source_ref("v476-thos-v7-x2-run-status-v1.json")]
    written.extend(build_v8_x1(source_refs, status_refs, generated_at, started_at_nz))
    source_refs = source_refs + [source_ref("v476-thos-v8-x1-closure-audit-v1.json")]
    status_refs = status_refs + [source_ref("v476-thos-v8-x1-run-status-v1.json")]
    written.extend(build_v8_x2(source_refs, status_refs, generated_at, started_at_nz))
    return written


def main() -> int:
    written = build_all()
    print(json.dumps({"written": [str(path.relative_to(REPO_ROOT)).replace("\\", "/") for path in written]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
