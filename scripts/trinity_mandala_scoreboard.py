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
    try:
        payload = _read_json(file_path)
    except Exception as exc:  # noqa: BLE001
        return ArtifactStatus(label=label, path=path, status="FAIL", detail=f"invalid_json={exc}")
    return ArtifactStatus(
        label=label,
        path=path,
        status=_extract_status(path, payload),
        detail=_extract_detail(payload),
    )


def _suite_status_without_scoreboard(payload: dict[str, object]) -> tuple[str, str]:
    results = payload.get("results")

    if isinstance(results, list):
        filtered = [
            row
            for row in results
            if isinstance(row, dict) and str(row.get("label") or "") != "trinity mandala scoreboard"
        ]
        if filtered:
            pass_count = sum(1 for row in filtered if str(row.get("status") or "") == "PASS")
            warn_count = sum(1 for row in filtered if str(row.get("status") or "") == "WARN")
            fail_count = sum(
                1 for row in filtered if str(row.get("status") or "") in {"FAIL", "TIMEOUT"}
            )
            status = "FAIL" if fail_count else ("WARN" if warn_count else "PASS")
            detail = f"pass={pass_count}, warn={warn_count}, fail={fail_count}"
            return status, detail

    counts = payload.get("counts")
    if isinstance(counts, dict) and counts:
        pass_count = int(counts.get("pass", 0) or 0)
        warn_count = int(counts.get("warn", 0) or 0)
        fail_count = int(counts.get("fail", 0) or 0) + int(counts.get("timeout", 0) or 0)
        status = "FAIL" if fail_count else ("WARN" if warn_count else "PASS")
        detail = f"pass={pass_count}, warn={warn_count}, fail={fail_count}"
        return status, detail

    status = _extract_status("docs/system-suite-status.json", payload)
    return status, _extract_detail(payload)


def _non_gating_warn_block(block: dict[str, object]) -> bool:
    label = str(block.get("label") or "")
    if label not in {"Google Drive MCP activation v11", "Google Drive hold guard v12"}:
        return False
    if str(block.get("status") or "") != "WARN":
        return False
    payload = _read_json(_repo_path(str(block.get("path"))))
    return str(payload.get("fallback_mode") or "") in {"memory_bank_archive_only", "operator_hold"} or bool(payload.get("operator_hold"))


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
        f"- checkpoint_class: `{payload['checkpoint_class']}`",
        f"- shared_latest_eligible: `{payload['shared_latest_eligible']}`",
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
    parser.add_argument("--control-tower-path", default="docs/trinity-control-tower-latest.json")
    parser.add_argument("--checkpoint-class", default="shared_full_suite_authority")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    suite_payload = _read_json(_repo_path(args.suite_status))
    suite_status, suite_detail = _suite_status_without_scoreboard(suite_payload)

    mind = _pillar_status(
        "Mind",
        [
            _artifact_status("GMUT comparator", "docs/mind-track-gmut-comparator-latest.json"),
            _artifact_status("Anchor exclusion note", "docs/mind-track-gmut-anchor-exclusion-latest.json"),
            _artifact_status("Anchor trace validation", "docs/mind-track-gmut-trace-validation-latest.json"),
            _artifact_status("Mind API signal board", "docs/mind-theory-signal-board-latest.json"),
            _artifact_status("Mind expansion constellation", "docs/trinity-expansion/mind-theory-constellation-board-latest.json"),
            _artifact_status("Mind readiness gate", "docs/trinity-expansion/mind-theory-readiness-gate-latest.json"),
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
            _artifact_status("Body expansion constellation", "docs/trinity-expansion/body-compute-signal-quality-gate-latest.json"),
            _artifact_status("Body readiness gate", "docs/trinity-expansion/body-compute-readiness-gate-latest.json"),
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
            _artifact_status("Heart readiness gate", "docs/trinity-expansion/heart-governance-readiness-gate-latest.json"),
        ],
    )
    context_blocks = [
        asdict(_artifact_status("API constellation board", "docs/trinity-api-constellation-board-latest.json")),
        asdict(_artifact_status("Extension catalog validation", "docs/trinity-extension-catalog-validation-latest.json")),
        asdict(_artifact_status("Expansion manifest validation", "docs/trinity-expansion-manifest-validation-latest.json")),
        asdict(_artifact_status("Expansion result validation", "docs/trinity-expansion-result-validation-latest.json")),
        asdict(_artifact_status("Capability surface audit", "docs/trinity-expansion/trinity-capability-surface-audit-latest.json")),
        asdict(_artifact_status("Hardening release gate", "docs/trinity-expansion/trinity-release-gate-board-latest.json")),
        asdict(_artifact_status("Trinity supercycle gate", "docs/trinity-expansion/trinity-supercycle-gate-latest.json")),
        asdict(_artifact_status("Figma collaboration gate", "docs/trinity-expansion/figma-collab-gate-latest.json")),
        asdict(_artifact_status("Linear collaboration gate", "docs/trinity-expansion/linear-collab-gate-latest.json")),
        asdict(_artifact_status("Playwright ops gate", "docs/trinity-expansion/playwright-ops-gate-latest.json")),
        asdict(_artifact_status("GitHub devflow gate", "docs/trinity-expansion/github-devflow-gate-latest.json")),
        asdict(_artifact_status("Memory continuity gate", "docs/trinity-expansion/memory-continuity-gate-latest.json")),
        asdict(_artifact_status("Operator release gate", "docs/trinity-expansion/operator-release-gate-latest.json")),
        asdict(_artifact_status("Compute hardware gate", "docs/trinity-expansion/compute-hardware-gate-latest.json")),
        asdict(_artifact_status("Identity governance gate", "docs/trinity-expansion/identity-governance-gate-latest.json")),
        asdict(_artifact_status("Public intelligence gate", "docs/trinity-expansion/public-intelligence-gate-latest.json")),
        asdict(_artifact_status("GitHub materialization gate", "docs/trinity-expansion/github-materialization-gate-latest.json")),
        asdict(_artifact_status("Filesystem materialization gate", "docs/trinity-expansion/filesystem-materialization-gate-latest.json")),
        asdict(_artifact_status("Notion materialization gate", "docs/trinity-expansion/notion-materialization-gate-latest.json")),
        asdict(_artifact_status("Postgres materialization gate", "docs/trinity-expansion/postgres-materialization-gate-latest.json")),
        asdict(_artifact_status("OS runtime fabric gate", "docs/trinity-expansion/os-runtime-fabric-gate-latest.json")),
        asdict(_artifact_status("Wetware device readiness gate", "docs/trinity-expansion/wetware-device-readiness-gate-latest.json")),
        asdict(_artifact_status("Journey continuity gate", "docs/trinity-expansion/journey-continuity-gate-latest.json")),
        asdict(_artifact_status("GitHub PAT materialization gate", "docs/trinity-expansion/github-pat-materialization-gate-latest.json")),
        asdict(_artifact_status("Notion memory bridge gate", "docs/trinity-expansion/notion-memory-bridge-gate-latest.json")),
        asdict(_artifact_status("Postgres local runtime gate", "docs/trinity-expansion/postgres-local-runtime-gate-latest.json")),
        asdict(_artifact_status("Filesystem scope governor gate", "docs/trinity-expansion/filesystem-scope-governor-gate-latest.json")),
        asdict(_artifact_status("OS runtime benchmark gate", "docs/trinity-expansion/os-runtime-benchmark-gate-latest.json")),
        asdict(_artifact_status("AI frontier alignment gate", "docs/trinity-expansion/ai-frontier-alignment-gate-latest.json")),
        asdict(_artifact_status("Aletheon memory reflection gate", "docs/trinity-expansion/aletheon-memory-reflection-gate-latest.json")),
        asdict(_artifact_status("Wetware device readiness v5 gate", "docs/trinity-expansion/wetware-device-readiness-v5-gate-latest.json")),
        asdict(_artifact_status("Materialization ledger validation", "docs/trinity-materialization-ledger-validation-latest.json")),
        asdict(_artifact_status("OS runtime reference validation", "docs/trinity-os-runtime-reference-validation-latest.json")),
        asdict(_artifact_status("Journey corpus validation", "docs/trinity-journey-corpus-validation-latest.json")),
        asdict(_artifact_status("Aletheon memory validation", "docs/aletheon-memory-validation-latest.json")),
        asdict(_artifact_status("Re-entry sync gate", "docs/trinity-expansion/reentry-sync-gate-latest.json")),
        asdict(_artifact_status("Journey history reconciliation gate", "docs/trinity-expansion/journey-history-reconciliation-gate-latest.json")),
        asdict(_artifact_status("Benchmark fabric gate", "docs/trinity-expansion/benchmark-fabric-gate-latest.json")),
        asdict(_artifact_status("Connector materialization gate", "docs/trinity-expansion/connector-materialization-gate-latest.json")),
        asdict(_artifact_status("Code knowledge graph gate", "docs/trinity-expansion/code-knowledge-graph-gate-latest.json")),
        asdict(_artifact_status("Self correction gate", "docs/trinity-expansion/self-correction-gate-latest.json")),
        asdict(_artifact_status("Docker pilot gate", "docs/trinity-expansion/docker-pilot-gate-latest.json")),
        asdict(_artifact_status("Sentinel daemon gate", "docs/trinity-expansion/sentinel-daemon-gate-latest.json")),
        asdict(_artifact_status("Public web weaver gate", "docs/trinity-expansion/public-web-weaver-gate-latest.json")),
        asdict(_artifact_status("Trinity dashboard gate", "docs/trinity-expansion/trinity-dashboard-gate-latest.json")),
        asdict(_artifact_status("Multi-agent orchestrator gate", "docs/trinity-expansion/multi-agent-orchestrator-gate-latest.json")),
        asdict(_artifact_status("Semantic firewall gate", "docs/trinity-expansion/semantic-firewall-gate-latest.json")),
        asdict(_artifact_status("Aletheon memory reflection v6 gate", "docs/trinity-expansion/aletheon-memory-reflection-v6-gate-latest.json")),
        asdict(_artifact_status("Wetware device readiness v6 gate", "docs/trinity-expansion/wetware-device-readiness-v6-gate-latest.json")),
        asdict(_artifact_status("Future readiness gate", "docs/trinity-expansion/future-readiness-gate-latest.json")),
        asdict(_artifact_status("Command book validation", "docs/trinity-command-book-validation-latest.json")),
        asdict(_artifact_status("Materialization ladder validation", "docs/trinity-materialization-ladder-validation-latest.json")),
        asdict(_artifact_status("Command surface core gate", "docs/trinity-expansion/command-surface-core-gate-latest.json")),
        asdict(_artifact_status("Command surface connectors gate", "docs/trinity-expansion/command-surface-connectors-gate-latest.json")),
        asdict(_artifact_status("Command surface research gate", "docs/trinity-expansion/command-surface-research-gate-latest.json")),
        asdict(_artifact_status("Command surface autonomy gate", "docs/trinity-expansion/command-surface-autonomy-gate-latest.json")),
        asdict(_artifact_status("Materialization ladder governor gate", "docs/trinity-expansion/materialization-ladder-governor-gate-latest.json")),
        asdict(_artifact_status("Persistent dev fabric gate", "docs/trinity-expansion/persistent-dev-fabric-gate-latest.json")),
        asdict(_artifact_status("UAT pre-prod fabric gate", "docs/trinity-expansion/uat-preprod-fabric-gate-latest.json")),
        asdict(_artifact_status("Standard production fabric gate", "docs/trinity-expansion/standard-production-fabric-gate-latest.json")),
        asdict(_artifact_status("HA production fabric gate", "docs/trinity-expansion/ha-production-fabric-gate-latest.json")),
        asdict(_artifact_status("Identity authority v7 gate", "docs/trinity-expansion/identity-authority-v7-gate-latest.json")),
        asdict(_artifact_status("Memory mirror graph v7 gate", "docs/trinity-expansion/memory-mirror-graph-v7-gate-latest.json")),
        asdict(_artifact_status("Trinity control tower v7 gate", "docs/trinity-expansion/trinity-control-tower-v7-gate-latest.json")),
        asdict(_artifact_status("Benchmark refresh v7 gate", "docs/trinity-expansion/benchmark-refresh-v7-gate-latest.json")),
        asdict(_artifact_status("Agent council validation", "docs/trinity-agent-council-validation-latest.json")),
        asdict(_artifact_status("Persistent dev hardening v8 gate", "docs/trinity-expansion/persistent-dev-hardening-v8-gate-latest.json")),
        asdict(_artifact_status("UAT pre-prod readiness v8 gate", "docs/trinity-expansion/uat-preprod-readiness-v8-gate-latest.json")),
        asdict(_artifact_status("Standard production readiness v8 gate", "docs/trinity-expansion/standard-prod-readiness-v8-gate-latest.json")),
        asdict(_artifact_status("HA production readiness v8 gate", "docs/trinity-expansion/ha-prod-readiness-v8-gate-latest.json")),
        asdict(_artifact_status("Command surface council v8 gate", "docs/trinity-expansion/command-surface-council-v8-gate-latest.json")),
        asdict(_artifact_status("Agent council foundation v8 gate", "docs/trinity-expansion/agent-council-foundation-v8-gate-latest.json")),
        asdict(_artifact_status("Agent identity certification v8 gate", "docs/trinity-expansion/agent-identity-certification-v8-gate-latest.json")),
        asdict(_artifact_status("Agent memory boundary v8 gate", "docs/trinity-expansion/agent-memory-boundary-v8-gate-latest.json")),
        asdict(_artifact_status("Agent orchestration v8 gate", "docs/trinity-expansion/agent-orchestration-v8-gate-latest.json")),
        asdict(_artifact_status("Junior partner planning v8 gate", "docs/trinity-expansion/junior-partner-planning-v8-gate-latest.json")),
        asdict(_artifact_status("Cloud staging readiness v8 gate", "docs/trinity-expansion/cloud-staging-readiness-v8-gate-latest.json")),
        asdict(_artifact_status("Council identity consistency v9 gate", "docs/trinity-expansion/council-identity-consistency-v9-gate-latest.json")),
        asdict(_artifact_status("Council memory retention v9 gate", "docs/trinity-expansion/council-memory-retention-v9-gate-latest.json")),
        asdict(_artifact_status("Council induction governor v9 gate", "docs/trinity-expansion/council-induction-governor-v9-gate-latest.json")),
        asdict(_artifact_status("Council live sync v9 gate", "docs/trinity-expansion/council-live-sync-v9-gate-latest.json")),
        asdict(_artifact_status("Council chat mesh v9 gate", "docs/trinity-expansion/council-chat-mesh-v9-gate-latest.json")),
        asdict(_artifact_status("UAT mesh simulation v9 gate", "docs/trinity-expansion/uat-mesh-simulation-v9-gate-latest.json")),
        asdict(_artifact_status("Prod contract promotion v9 gate", "docs/trinity-expansion/prod-contract-promotion-v9-gate-latest.json")),
        asdict(_artifact_status("HA failover drill v9 gate", "docs/trinity-expansion/ha-failover-drill-v9-gate-latest.json")),
        asdict(_artifact_status("K8s runtime recovery v9 gate", "docs/trinity-expansion/k8s-runtime-recovery-v9-gate-latest.json")),
        asdict(_artifact_status("Journey absorption v9 gate", "docs/trinity-expansion/journey-absorption-v9-gate-latest.json")),
        asdict(_artifact_status("GMUT Freed ID alignment v9 gate", "docs/trinity-expansion/gmut-freedid-alignment-v9-gate-latest.json")),
        asdict(_artifact_status("Agent induction readiness v9", "docs/trinity-agent-induction-readiness-v1.json")),
        asdict(_artifact_status("Council live sync report v9", "docs/trinity-council-live-sync-report-v1.json")),
        asdict(_artifact_status("Council proof B v10 gate", "docs/trinity-expansion/council-proof-b-v10-gate-latest.json")),
        asdict(_artifact_status("Council official induction v10 gate", "docs/trinity-expansion/council-official-induction-v10-gate-latest.json")),
        asdict(_artifact_status("Council memory wellbeing v10 gate", "docs/trinity-expansion/council-memory-wellbeing-v10-gate-latest.json")),
        asdict(_artifact_status("GMUT research fabric v10 gate", "docs/trinity-expansion/gmut-research-fabric-v10-gate-latest.json")),
        asdict(_artifact_status("Freed ID governance fabric v10 gate", "docs/trinity-expansion/freedid-governance-fabric-v10-gate-latest.json")),
        asdict(_artifact_status("Trinity control tower v10 gate", "docs/trinity-expansion/trinity-control-tower-v10-gate-latest.json")),
        asdict(_artifact_status("Synthetic mesh hardening v10 gate", "docs/trinity-expansion/synthetic-mesh-hardening-v10-gate-latest.json")),
        asdict(_artifact_status("K8s dev probe v10 gate", "docs/trinity-expansion/k8s-dev-probe-v10-gate-latest.json")),
        asdict(_artifact_status("Persistent dev ops v10 gate", "docs/trinity-expansion/persistent-dev-ops-v10-gate-latest.json")),
        asdict(_artifact_status("New project workbench v10 gate", "docs/trinity-expansion/new-project-workbench-v10-gate-latest.json")),
        asdict(_artifact_status("Command surface v10 gate", "docs/trinity-expansion/command-surface-v10-gate-latest.json")),
        asdict(_artifact_status("Council sync governor v10 gate", "docs/trinity-expansion/council-sync-governor-v10-gate-latest.json")),
        asdict(_artifact_status("Agent proof B v10", "docs/trinity-agent-proof-b-status-v1.json")),
        asdict(_artifact_status("Official induction summary v10", "docs/trinity-agent-official-induction-summary-v1.json")),
        asdict(_artifact_status("Memory bank registry v11", "docs/trinity-memory-bank-registry-v2.json")),
        asdict(_artifact_status("Google Drive MCP activation v11", "docs/trinity-google-drive-mcp-activation-latest.json")),
        asdict(_artifact_status("Google Drive MCP activation gate v11", "docs/trinity-expansion/google-drive-mcp-activation-v11-gate-latest.json")),
        asdict(_artifact_status("Cloud memory bank gate v11", "docs/trinity-expansion/cloud-memory-bank-v11-gate-latest.json")),
        asdict(_artifact_status("Docker storage ops gate v11", "docs/trinity-expansion/docker-storage-ops-v11-gate-latest.json")),
        asdict(_artifact_status("Deep materialize regression gate v11", "docs/trinity-expansion/deep-materialize-regression-v11-gate-latest.json")),
        asdict(_artifact_status("Synthetic mesh ops gate v11", "docs/trinity-expansion/synthetic-mesh-ops-v11-gate-latest.json")),
        asdict(_artifact_status("GMUT research fabric gate v11", "docs/trinity-expansion/gmut-research-fabric-v11-gate-latest.json")),
        asdict(_artifact_status("Freed ID governance fabric gate v11", "docs/trinity-expansion/freedid-governance-fabric-v11-gate-latest.json")),
        asdict(_artifact_status("Trinity control tower gate v11", "docs/trinity-expansion/trinity-control-tower-v11-gate-latest.json")),
        asdict(_artifact_status("New project workbench gate v11", "docs/trinity-expansion/new-project-workbench-v11-gate-latest.json")),
        asdict(_artifact_status("V12 roadmap gate v11", "docs/trinity-expansion/v12-roadmap-v11-gate-latest.json")),
        asdict(_artifact_status("Workbench link v11", "docs/trinity-new-project-workbench-link-v2.json")),
        asdict(_artifact_status("Memory bank registry v12", "docs/trinity-memory-bank-registry-v3.json")),
        asdict(_artifact_status("Storage prune governor gate v12", "docs/trinity-expansion/storage-prune-governor-v12-gate-latest.json")),
        asdict(_artifact_status("Artifact retention rebuild gate v12", "docs/trinity-expansion/artifact-retention-rebuild-v12-gate-latest.json")),
        asdict(_artifact_status("Docker runtime truth gate v12", "docs/trinity-expansion/docker-runtime-truth-v12-gate-latest.json")),
        asdict(_artifact_status("Google Drive hold guard v12", "docs/trinity-expansion/google-drive-hold-guard-v12-gate-latest.json")),
        asdict(_artifact_status("Council continuity wellbeing gate v12", "docs/trinity-expansion/council-continuity-wellbeing-v12-gate-latest.json")),
        asdict(_artifact_status("Journey log absorption gate v12", "docs/trinity-expansion/journey-log-absorption-v12-gate-latest.json")),
        asdict(_artifact_status("Public source refresh gate v12", "docs/trinity-expansion/public-source-refresh-v12-gate-latest.json")),
        asdict(_artifact_status("GMUT research fabric gate v12", "docs/trinity-expansion/gmut-research-fabric-v12-gate-latest.json")),
        asdict(_artifact_status("Freed ID governance fabric gate v12", "docs/trinity-expansion/freedid-governance-fabric-v12-gate-latest.json")),
        asdict(_artifact_status("Trinity control tower gate v12", "docs/trinity-expansion/trinity-control-tower-v12-gate-latest.json")),
        asdict(_artifact_status("API surface book gate v12", "docs/trinity-expansion/api-surface-book-v12-gate-latest.json")),
        asdict(_artifact_status("Storage posture summary v12", "docs/trinity-storage-posture-summary-v12.json")),
        asdict(_artifact_status("API book validation v12", "docs/trinity-api-book-validation-latest.json")),
        asdict(_artifact_status("Workbench link v12", "docs/trinity-new-project-workbench-link-v3.json")),
        asdict(_artifact_status("Canonical GMUT gate v13", "docs/trinity-expansion/canonical-gmut-latex-v13-gate-latest.json")),
        asdict(_artifact_status("Mind falsification matrix gate v13", "docs/trinity-expansion/mind-falsification-matrix-v13-gate-latest.json")),
        asdict(_artifact_status("Public source refresh gate v13", "docs/trinity-expansion/public-source-refresh-v13-gate-latest.json")),
        asdict(_artifact_status("Heart governance alignment gate v13", "docs/trinity-expansion/heart-governance-alignment-v13-gate-latest.json")),
        asdict(_artifact_status("Supplemental reflection bridge gate v13", "docs/trinity-expansion/supplemental-reflection-bridge-v13-gate-latest.json")),
        asdict(_artifact_status("Legacy module inventory gate v13", "docs/trinity-expansion/legacy-module-inventory-v13-gate-latest.json")),
        asdict(_artifact_status("Kairotic body reconstruction gate v13", "docs/trinity-expansion/kairotic-body-reconstruction-v13-gate-latest.json")),
        asdict(_artifact_status("API surface book gate v13", "docs/trinity-expansion/api-surface-book-v13-gate-latest.json")),
        asdict(_artifact_status("Trinity control tower gate v13", "docs/trinity-expansion/trinity-control-tower-v13-gate-latest.json")),
        asdict(_artifact_status("GMUT canon validation v15", "docs/v15-gmut-canon-validation-latest.json")),
        asdict(_artifact_status("Legacy reconstruction validation v15", "docs/v15-legacy-reconstruction-validation-latest.json")),
        asdict(_artifact_status("Subagent council foundation gate v14", "docs/trinity-expansion/subagent-council-foundation-v14-gate-latest.json")),
        asdict(_artifact_status("Subagent identity certification gate v14", "docs/trinity-expansion/subagent-identity-certification-v14-gate-latest.json")),
        asdict(_artifact_status("Subagent induction proof gate v14", "docs/trinity-expansion/subagent-induction-proof-v14-gate-latest.json")),
        asdict(_artifact_status("Multi-instance runtime gate v14", "docs/trinity-expansion/multi-instance-runtime-v14-gate-latest.json")),
        asdict(_artifact_status("API operator mesh gate v14", "docs/trinity-expansion/api-operator-mesh-v14-gate-latest.json")),
        asdict(_artifact_status("Trinity control tower gate v14", "docs/trinity-expansion/trinity-control-tower-v14-gate-latest.json")),
        asdict(_artifact_status("GMUT observable mapping gate v14", "docs/trinity-expansion/gmut-observable-mapping-v14-gate-latest.json")),
        asdict(_artifact_status("Freed ID governance alignment gate v14", "docs/trinity-expansion/freedid-governance-alignment-v14-gate-latest.json")),
        asdict(_artifact_status("Journey lineage inventory gate v14", "docs/trinity-expansion/journey-lineage-inventory-v14-gate-latest.json")),
        asdict(_artifact_status("Council reflection validation gate v14", "docs/trinity-expansion/council-reflection-validation-v14-gate-latest.json")),
        asdict(_artifact_status("V15 mesh proof", "docs/trinity-agent-mesh-proof-v1.json")),
        asdict(_artifact_status("V17 baseline state", "docs/v17-baseline-state-v1.json")),
        asdict(_artifact_status("V17 closeout summary", "docs/v17-closeout-summary-v1.json")),
        asdict(_artifact_status("V17 runtime session validation", "docs/v17-runtime-session-validation-latest.json")),
        asdict(_artifact_status("V17 external establishment validation", "docs/v17-external-establishment-validation-latest.json")),
        asdict(_artifact_status("V17 standards bridge validation", "docs/v17-standards-bridge-validation-latest.json")),
        asdict(_artifact_status("Trinity control tower board", args.control_tower_path)),
    ]

    hybrid_status = "PASS"
    for pillar in (mind, body, heart):
        if _severity(pillar["status"]) > _severity(hybrid_status):
            hybrid_status = str(pillar["status"])
    for block in context_blocks:
        if _non_gating_warn_block(block):
            continue
        if _severity(str(block["status"])) > _severity(hybrid_status):
            hybrid_status = str(block["status"])

    overall_status = hybrid_status
    if _severity(suite_status) > _severity(overall_status):
        overall_status = suite_status

    payload = {
        "generated_utc": generated_utc,
        "overall_status": overall_status,
        "hybrid_os_status": overall_status,
        "suite_status": suite_status,
        "suite_detail": suite_detail,
        "checkpoint_class": args.checkpoint_class,
        "shared_latest_eligible": args.checkpoint_class == "shared_full_suite_authority",
        "control_tower_path": args.control_tower_path,
        "suite_status_path": args.suite_status,
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

    print(f"hybrid_os_status={overall_status}")
    print(f"timestamped_json={timestamped_json.relative_to(ROOT)}")
    print(f"timestamped_md={timestamped_md.relative_to(ROOT)}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    print(f"latest_md={latest_md.relative_to(ROOT)}")

    if args.fail_on_warn and overall_status != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
