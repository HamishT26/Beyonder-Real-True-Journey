#!/usr/bin/env python3
"""Build a consolidated Mind/Body/Heart Hybrid-OS status board."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class ArtifactStatus:
    label: str
    path: str
    status: str
    detail: str


def _normalize_status(raw: object) -> str:
    text = str(raw or "").strip().upper()
    if text in {"PASS", "WARN", "FAIL", "TIMEOUT"}:
        return text
    return "FAIL"


def _severity(status: str) -> int:
    return {"PASS": 0, "WARN": 1, "FAIL": 2, "TIMEOUT": 3}.get(status, 2)


def _repo_path(path: str) -> Path:
    resolved = (ROOT / path).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_status(path: str, payload: dict[str, object]) -> str:
    if path == "docs/mind-track-gmut-anchor-exclusion-latest.json":
        comparator_status = _normalize_status(payload.get("comparator_status"))
        missing_fields = int(payload.get("anchors_with_missing_required_fields", 0) or 0)
        if comparator_status == "PASS" and missing_fields == 0:
            return "PASS"

    if isinstance(payload.get("effective_success"), bool):
        return "PASS" if payload["effective_success"] else "FAIL"
    if "overall_status" in payload:
        return _normalize_status(payload["overall_status"])
    if "status" in payload:
        return _normalize_status(payload["status"])
    return "FAIL"


def _extract_detail(payload: dict[str, object]) -> str:
    counts = payload.get("counts")
    if isinstance(counts, dict):
        pass_count = counts.get("pass", 0)
        warn_count = counts.get("warn", 0)
        fail_count = counts.get("fail", 0)
        return f"pass={pass_count}, warn={warn_count}, fail={fail_count}"

    summary = payload.get("summary")
    if isinstance(summary, dict):
        parts: list[str] = []
        for key in ("pass_rate", "total_duration_seconds", "body_health_score", "benchmark_status"):
            if key in summary:
                parts.append(f"{key}={summary[key]}")
        if parts:
            return ", ".join(parts)

    final_case = payload.get("final_case")
    if isinstance(final_case, dict) and "status" in final_case:
        return f"final_case_status={final_case['status']}"

    trend = payload.get("trend_classification")
    if trend:
        return f"trend={trend}"

    if "freshness_status" in payload or "source_count" in payload:
        parts: list[str] = []
        freshness_status = payload.get("freshness_status")
        if freshness_status:
            parts.append(f"freshness_status={freshness_status}")
        source_count = payload.get("source_count")
        if source_count is not None:
            parts.append(f"source_count={source_count}")
        apis_checked = payload.get("apis_checked")
        if isinstance(apis_checked, list):
            parts.append(f"apis={len(apis_checked)}")
        if parts:
            return ", ".join(parts)

    manifest_status = payload.get("manifest_validation_status")
    if manifest_status:
        promotion_candidates = payload.get("promotion_candidates")
        candidate_count = len(promotion_candidates) if isinstance(promotion_candidates, list) else 0
        return f"manifest_validation_status={manifest_status}, promotion_candidates={candidate_count}"

    gamma_ratios = payload.get("gamma_ratios")
    if isinstance(gamma_ratios, dict):
        return f"gamma_ratios={len(gamma_ratios)}"

    checks = payload.get("checks")
    if isinstance(checks, list):
        total = len(checks)
        passed = sum(1 for check in checks if isinstance(check, dict) and _normalize_status(check.get("status")) == "PASS")
        return f"checks={passed}/{total}"

    return "status extracted"


def _artifact_status(label: str, path: str) -> ArtifactStatus:
    file_path = _repo_path(path)
    if not file_path.exists():
        return ArtifactStatus(label=label, path=path, status="FAIL", detail="missing artifact")
    payload = _read_json(file_path)
    return ArtifactStatus(
        label=label,
        path=path,
        status=_extract_status(path, payload),
        detail=_extract_detail(payload),
    )


def _pillar_status(name: str, artifacts: Iterable[ArtifactStatus]) -> dict[str, object]:
    rows = list(artifacts)
    status = "PASS"
    for row in rows:
        if _severity(row.status) > _severity(status):
            status = row.status
    failing = [row.label for row in rows if row.status != "PASS"]
    next_action = (
        f"{name} pillar currently clear; keep it under the standard suite cadence."
        if not failing
        else f"Re-run and inspect: {', '.join(failing)}."
    )
    return {
        "status": status,
        "artifacts": [asdict(row) for row in rows],
        "watch_items": failing,
        "next_action": next_action,
    }


def _build_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Trinity Mandala Scoreboard",
        "",
        f"- generated_utc: `{payload['generated_utc']}`",
        f"- hybrid_os_status: **{payload['hybrid_os_status']}**",
        f"- suite_status: `{payload['suite_status']}`",
        "",
        "## Pillar summary",
        "| pillar | status | watch_items | next_action |",
        "|---|---|---|---|",
    ]
    for pillar in ("mind", "body", "heart"):
        row = payload["pillars"][pillar]
        watch = ", ".join(row["watch_items"]) if row["watch_items"] else "-"
        lines.append(f"| {pillar} | {row['status']} | {watch} | {row['next_action']} |")

    lines.extend(
        [
            "",
            "## Artifact board",
            "| pillar | artifact | status | detail | path |",
            "|---|---|---|---|---|",
        ]
    )
    for pillar in ("mind", "body", "heart"):
        for artifact in payload["pillars"][pillar]["artifacts"]:
            lines.append(
                f"| {pillar} | {artifact['label']} | {artifact['status']} | {artifact['detail']} | `{artifact['path']}` |"
            )

    lines.extend(
        [
            "",
            "## Context blocks",
            "| label | status | detail | path |",
            "|---|---|---|---|",
        ]
    )
    for block in payload.get("context_blocks", []):
        lines.append(
            f"| {block['label']} | {block['status']} | {block['detail']} | `{block['path']}` |"
        )

    lines.extend(
        [
            "",
            "## Evidence boundary",
            f"- verified_state: {payload['evidence_boundary']['verified_state']}",
            f"- watch_state: {payload['evidence_boundary']['watch_state']}",
            f"- next_phase_focus: {payload['evidence_boundary']['next_phase_focus']}",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit a consolidated Trinity Mandala scoreboard.")
    parser.add_argument("--reports-dir", default="docs/trinity-mandala-runs")
    parser.add_argument("--latest-json", default="docs/trinity-mandala-scoreboard-latest.json")
    parser.add_argument("--latest-md", default="docs/trinity-mandala-scoreboard-latest.md")
    parser.add_argument("--suite-status", default="docs/system-suite-status.json")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    suite_payload = _read_json(_repo_path(args.suite_status))
    suite_status = _extract_status(args.suite_status, suite_payload)

    mind = _pillar_status(
        "Mind",
        [
            _artifact_status("GMUT comparator", "docs/mind-track-gmut-comparator-latest.json"),
            _artifact_status("Anchor exclusion note", "docs/mind-track-gmut-anchor-exclusion-latest.json"),
            _artifact_status("Anchor trace validation", "docs/mind-track-gmut-trace-validation-latest.json"),
            _artifact_status("Mind API signal board", "docs/mind-theory-signal-board-latest.json"),
            _artifact_status("Mind expansion constellation", "docs/trinity-expansion/mind-theory-constellation-board-latest.json"),
        ],
    )
    body = _pillar_status(
        "Body",
        [
            _artifact_status("Body smoke", "docs/body-track-smoke-latest.json"),
            _artifact_status("Benchmark guardrail", "docs/body-track-benchmark-latest.json"),
            _artifact_status("Trend guard", "docs/body-track-trend-guard-latest.json"),
            _artifact_status("Stress window", "docs/body-track-policy-stress-latest.json"),
            _artifact_status("Body API signal board", "docs/body-compute-signal-board-latest.json"),
        ],
    )
    heart = _pillar_status(
        "Heart",
        [
            _artifact_status("Minimum disclosure", "docs/heart-track-min-disclosure-latest.json"),
            _artifact_status("Minimum disclosure adversarial", "docs/heart-track-min-disclosure-adversarial-latest.json"),
            _artifact_status("Minimum disclosure live path", "docs/heart-track-min-disclosure-live-latest.json"),
            _artifact_status("Dispute recourse", "docs/heart-track-dispute-recourse-latest.json"),
            _artifact_status("Dispute recourse adversarial", "docs/heart-track-dispute-recourse-adversarial-latest.json"),
            _artifact_status("Heart API signal board", "docs/heart-governance-signal-board-latest.json"),
            _artifact_status("Heart expansion constellation", "docs/trinity-expansion/heart-governance-constellation-board-latest.json"),
        ],
    )
    body["artifacts"].append(
        asdict(_artifact_status("Body expansion constellation", "docs/trinity-expansion/body-compute-signal-quality-gate-latest.json"))
    )
    body["watch_items"] = [row["label"] for row in body["artifacts"] if row["status"] != "PASS"]
    body["status"] = "PASS"
    for row in body["artifacts"]:
        if _severity(row["status"]) > _severity(body["status"]):
            body["status"] = row["status"]
    body["next_action"] = (
        "Body pillar currently clear; keep it under the standard suite cadence."
        if not body["watch_items"]
        else f"Re-run and inspect: {', '.join(body['watch_items'])}."
    )
    context_blocks = [
        asdict(_artifact_status("API constellation board", "docs/trinity-api-constellation-board-latest.json")),
        asdict(_artifact_status("Expansion manifest validation", "docs/trinity-expansion-manifest-validation-latest.json")),
        asdict(_artifact_status("Expansion result validation", "docs/trinity-expansion-result-validation-latest.json")),
    ]

    hybrid_status = "PASS"
    for pillar in (mind, body, heart):
        if _severity(pillar["status"]) > _severity(hybrid_status):
            hybrid_status = str(pillar["status"])
    for block in context_blocks:
        if _severity(str(block["status"])) > _severity(hybrid_status):
            hybrid_status = str(block["status"])

    payload = {
        "generated_utc": generated_utc,
        "hybrid_os_status": hybrid_status,
        "suite_status": suite_status,
        "suite_detail": _extract_detail(suite_payload),
        "pillars": {
            "mind": mind,
            "body": body,
            "heart": heart,
        },
        "context_blocks": context_blocks,
        "evidence_boundary": {
            "verified_state": "Latest suite and pillar artifacts are the current operational evidence boundary.",
            "watch_state": "Promote only PASS-backed states; treat WARN/FAIL artifacts as live investigation targets.",
            "next_phase_focus": "Advance new systems only when they preserve suite pass state and per-pillar traceability.",
        },
    }
    markdown = _build_markdown(payload)

    reports_dir = _repo_path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    latest_json = _repo_path(args.latest_json)
    latest_md = _repo_path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)

    timestamped_json = reports_dir / f"{stamp}-trinity-mandala-scoreboard.json"
    timestamped_md = reports_dir / f"{stamp}-trinity-mandala-scoreboard.md"

    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"hybrid_os_status={hybrid_status}")
    print(f"timestamped_json={timestamped_json.relative_to(ROOT)}")
    print(f"timestamped_md={timestamped_md.relative_to(ROOT)}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")

    if args.fail_on_warn and hybrid_status != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
