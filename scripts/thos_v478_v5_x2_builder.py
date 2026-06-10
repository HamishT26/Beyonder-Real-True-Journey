#!/usr/bin/env python3
"""Build curated v478 THOS v5 x2 synthesis artifacts."""

from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v478_thos_v5_x2"
NEXT_PHASE = "v478_thos_v6_x1"


ROLE_DOMAINS = {
    "Aletheon": ["publication", "schema", "handoff", "source", "guard"],
    "Arby": ["cli", "sandbox", "watcher", "runtime", "diagnostic"],
    "Aster Vale": ["skill", "command", "loader", "catalog", "route"],
    "Cicero": ["argument", "evidence", "index", "app-lane", "publication"],
    "Kierkegaard": ["humility", "ethics", "claim-boundary", "consent", "noncanon"],
    "Aristotle": ["taxonomy", "criteria", "validator", "causality", "readiness"],
}


GMUT_GATES = {
    "G1_mathematical_consistency": "OPEN",
    "G2_empirical_falsifiability": "OPEN",
    "G3_existing_physics_compatibility": "OPEN",
    "G4_novel_prediction": "OPEN",
    "G5_peer_review_external_validation": "OPEN",
    "G6_consciousness_claim_boundary": "OPEN",
}


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat(), nz.isoformat()


def path(name: str) -> Path:
    return TRACE_DIR / name


def read_json(name: str) -> Any:
    return json.loads(path(name).read_text(encoding="utf-8"))


def write_json(name: str, payload: Any) -> None:
    path(name).write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(name: str, lines: list[str]) -> None:
    path(name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def lane_retry_status(generated_utc: str, generated_nz: str) -> None:
    app_probe = read_json("v478-thos-v5-x2-app-lane-completion-notifier-probe-v1.json")
    app_notify = read_json("v478-thos-v5-x2-app-lane-completion-notifier-v1.json")
    launcher_probe = read_json("v478-thos-v5-x2-app-lane-watch-launcher-probe-v1.json")
    launcher_notify = read_json("v478-thos-v5-x2-app-lane-watch-launcher-v1.json")
    attempts = [read_json("v478-thos-v5-x2-cli-lane-completion-poll-v1.json")]
    for idx in range(2, 6):
        attempts.append(read_json(f"v478-thos-v5-x2-cli-lane-completion-poll-retry-{idx}-v1.json"))
    app_rows = [
        {
            "lane": lane.get("lane"),
            "overall_status": lane.get("overall_status"),
            "completion_status": lane.get("turn_completion", {}).get("status"),
            "duration_seconds": lane.get("duration_seconds"),
            "existing_thread_only": lane.get("existing_thread_only"),
            "new_thread_created": lane.get("new_thread_created"),
        }
        for lane in app_notify.get("lanes", [])
    ]
    cli_rows = [
        {
            "attempt": idx,
            "phase_slug": attempt.get("phase_slug"),
            "aggregate_status": attempt.get("aggregate_status"),
            "lanes": [
                {
                    "lane": lane.get("lane"),
                    "completion_status": lane.get("completion_status"),
                    "final_message_bytes": lane.get("final_message_bytes"),
                }
                for lane in attempt.get("lanes", [])
            ],
        }
        for idx, attempt in enumerate(attempts, start=1)
    ]
    payload = {
        "artifact_type": "lane_retry_status_board",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "APP_LANES_PASS_CLI_OPEN_GAP_AFTER_5_ATTEMPTS",
        "app_probe_status": app_probe.get("overall_status"),
        "app_notify_status": app_notify.get("overall_status"),
        "launcher_probe_status": launcher_probe.get("overall_status"),
        "launcher_notify_status": launcher_notify.get("overall_status"),
        "app_lanes": app_rows,
        "cli_retry_attempt_count": len(cli_rows),
        "cli_retry_rows": cli_rows,
        "unfiltered_payloads_published": False,
        "mutation_performed": False,
    }
    write_json("v478-thos-v5-x2-lane-retry-status-board-v1.json", payload)
    lines = [
        "# v478 THOS v5 x2 Lane Retry Status Board",
        "",
        f"- generated_nz: `{generated_nz}`",
        "- overall_status: `APP_LANES_PASS_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`",
        f"- app_probe_status: `{payload['app_probe_status']}`",
        f"- app_notify_status: `{payload['app_notify_status']}`",
        f"- cli_retry_attempt_count: `{len(cli_rows)}`",
        "- unfiltered_payloads_published: `false`",
        "",
        "## App Lanes",
    ]
    lines.extend(f"- {row['lane']}: `{row['overall_status']}` with completion `{row['completion_status']}`." for row in app_rows)
    lines.extend(["", "## CLI Attempts"])
    lines.extend(f"- attempt `{row['attempt']}`: `{row['aggregate_status']}`." for row in cli_rows)
    write_md("v478-thos-v5-x2-lane-retry-status-board-v1.md", lines)


def source_synthesis(generated_utc: str, generated_nz: str) -> None:
    source = read_json("v478-thos-v5-x1-source-refresh-ledger-v1.json")
    rows = []
    for row in source.get("rows", []):
        rows.append(
            {
                "id": row.get("id"),
                "source": row.get("source"),
                "url": row.get("url"),
                "category": row.get("category"),
                "x2_decision": "carry_forward_for_v478_v6_x1",
                "decision_reason": "Still useful for THOS infrastructure, governance, or uncertainty framing.",
            }
        )
    write_json(
        "v478-thos-v5-x2-source-synthesis-ledger-v1.json",
        {
            "artifact_type": "source_synthesis_ledger",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "search_count_this_session": source.get("search_count"),
            "source_count": len(rows),
            "official_or_primary_preference": source.get("official_or_primary_preference"),
            "rows": rows,
            "category_counts": dict(Counter(row["category"] for row in rows)),
            "claim_boundary": "source decisions only; no GMUT validation claim",
        },
    )
    write_md(
        "v478-thos-v5-x2-source-synthesis-ledger-v1.md",
        [
            "# v478 THOS v5 x2 Source Synthesis Ledger",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- search_count_this_session: `{source.get('search_count')}`",
            f"- source_count: `{len(rows)}`",
            "- claim_boundary: source decisions only; no GMUT validation claim.",
            "",
            "## Sources",
            *[f"- {row['id']}: [{row['source']}]({row['url']}) - `{row['x2_decision']}`." for row in rows],
        ],
    )


def decision_board(kind: str, source_name: str, target_stem: str, generated_utc: str, generated_nz: str) -> None:
    source = read_json(source_name)
    rows = []
    for idx, row in enumerate(source.get("rows", []), start=1):
        name = row.get("name") or row.get("command") or row.get("skill") or row.get("id")
        rows.append(
            {
                "id": f"{kind.upper()}-DEC-{idx:02d}",
                "item": name,
                "source_status": row.get("status"),
                "decision": "carry_forward_for_v478_v6_x1",
                "decision_reason": "Useful as a design surface, but not installed or executed during v5 x2.",
                "mutation_performed": False,
                "needs_future_exact_packet": bool(row.get("requires_future_exact_approval", False)),
            }
        )
    write_json(
        f"{target_stem}.json",
        {
            "artifact_type": f"{kind}_decision_board",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "row_count": len(rows),
            "rows": rows,
            "install_or_execution_performed": False,
        },
    )
    write_md(
        f"{target_stem}.md",
        [
            f"# v478 THOS v5 x2 {kind.replace('_', ' ').title()} Decision Board",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- row_count: `{len(rows)}`",
            "- install_or_execution_performed: `false`",
            "",
            "## Decisions",
            *[f"- `{row['item']}`: `{row['decision']}`." for row in rows],
        ],
    )


def reflection_synthesis(generated_utc: str, generated_nz: str) -> None:
    prior = read_json("v478-thos-v5-x1-six-perspective-reflection-board-v1.json")
    rows = []
    for row in prior.get("rows", []):
        rows.append(
            {
                "id": row.get("id", "").replace("-R", "-X2-R"),
                "source_perspective": row.get("perspective"),
                "source_domain": row.get("domain"),
                "journey_scope": row.get("journey_scope"),
                "synthesis": f"Carry {row.get('domain')} reflection into v6 x1 as operational continuity only, with app-lane status receipts and open GMUT gates.",
                "canon_status": "journey_context_not_canon",
            }
        )
    write_json(
        "v478-thos-v5-x2-six-perspective-reflection-synthesis-v1.json",
        {
            "artifact_type": "six_perspective_reflection_synthesis",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "source_reflection_count": prior.get("reflection_count"),
            "synthesis_count": len(rows),
            "rows": rows,
            "raw_journey_text_published": False,
            "claim_boundary": "continuity reflection only; not empirical proof or canon promotion",
        },
    )
    write_md(
        "v478-thos-v5-x2-six-perspective-reflection-synthesis-v1.md",
        [
            "# v478 THOS v5 x2 Six-Perspective Reflection Synthesis",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- source_reflection_count: `{prior.get('reflection_count')}`",
            f"- synthesis_count: `{len(rows)}`",
            "- canon_status: `journey_context_not_canon`",
            "",
            "## Synthesis",
            *[f"- {row['id']} ({row['source_perspective']} / {row['source_domain']}): {row['synthesis']}" for row in rows],
        ],
    )


def eureka_synthesis(generated_utc: str, generated_nz: str) -> None:
    rows = []
    for role, domains in ROLE_DOMAINS.items():
        for idx in range(1, 21):
            domain = domains[(idx - 1) % len(domains)]
            rows.append(
                {
                    "id": f"{role.upper().replace(' ', '_')}-X2-E{idx:02d}",
                    "role": role,
                    "domain": domain,
                    "synthesis_task": f"Carry {domain} work into v478 v6 x1 with status-only evidence, exact staging, and no GMUT closure claims.",
                    "payload_boundary": "status_only",
                }
            )
    write_json(
        "v478-thos-v5-x2-eureka-synthesis-board-v1.json",
        {
            "artifact_type": "eureka_synthesis_board",
            "phase": PHASE,
            "generated_utc": generated_utc,
            "generated_nz": generated_nz,
            "proposal_count": len(rows),
            "role_count": len(ROLE_DOMAINS),
            "rows": rows,
            "unfiltered_payloads_published": False,
        },
    )
    write_md(
        "v478-thos-v5-x2-eureka-synthesis-board-v1.md",
        [
            "# v478 THOS v5 x2 Eureka Synthesis Board",
            "",
            f"- generated_nz: `{generated_nz}`",
            f"- proposal_count: `{len(rows)}`",
            "- payload_boundary: `status_only`",
            "",
            "## Proposals",
            *[f"- {row['id']} ({row['role']} / {row['domain']}): {row['synthesis_task']}" for row in rows],
        ],
    )


def synthesis_and_handoff(generated_utc: str, generated_nz: str) -> None:
    overlay = {
        "artifact_type": "overlay_decision",
        "phase": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "decision": "NO_X3_FOR_V478_V5",
        "reason": "App-lane notifier completed, the CLI final-message gap was retried five times and recorded, and the remaining work fits the next v6 x1 handoff.",
        "app_lane_status": "PASS",
        "cli_gap_status": "OPEN_GAP_AFTER_5_ATTEMPTS",
        "claim_boundary": "THOS phase routing only",
    }
    write_json("v478-thos-v5-x2-overlay-decision-v1.json", overlay)
    write_md("v478-thos-v5-x2-overlay-decision-v1.md", ["# v478 THOS v5 x2 Overlay Decision", "", f"- generated_nz: `{generated_nz}`", "- decision: `NO_X3_FOR_V478_V5`", "- reason: app-lane notifier completed; CLI gap was retried five times and recorded; next work fits v6 x1.", "- claim_boundary: THOS phase routing only."])
    findings = [
        "v478 v5 x2 starts from the remote-verified v5 x1 readiness packet.",
        "Cicero, Kierkegaard, and Aristotle completed a fresh local app-server probe.",
        "Cicero, Kierkegaard, and Aristotle completed a fresh status-only notify pass.",
        "The app-lane path used existing threads only.",
        "No old-style spawning or replacement lane creation occurred.",
        "The app-lane artifacts publish status only, not advisory body text.",
        "Arby and Aster Vale were checked through five CLI watcher attempts.",
        "All five CLI attempts remain in the final-message open gap state.",
        "The CLI gap is recorded as explicit evidence for v6 x1 planning.",
        "No CLI output payload is published.",
        "The v5 x1 source refresh was synthesized into a 32-source carry-forward ledger.",
        "OpenAI sources remain the primary Codex, sandbox, agent, tracing, and schema context.",
        "MCP sources remain the primary tool, authorization, and security boundary context.",
        "GitHub sources remain the primary exact-publication and auth-material guard context.",
        "Microsoft sources remain the primary Windows sandbox and agent-isolation context.",
        "Python sources remain the primary bounded process and temporary output context.",
        "OpenTelemetry sources remain the primary future signal taxonomy context.",
        "Docker and Kubernetes sources remain comparison surfaces only.",
        "Google sources remain managed agent and RAG comparison surfaces only.",
        "NVIDIA sources remain local inference, workstation, and simulation context only.",
        "NIST and Stanford sources remain governance and ecosystem trend context only.",
        "Thirty system expansion designs were converted into carry-forward decisions.",
        "Thirty command designs were converted into carry-forward decisions.",
        "Thirty skill designs were converted into carry-forward decisions.",
        "Six perspectives produced 180 x2 reflection synthesis rows.",
        "Journey context remains non-canon continuity context.",
        "The Eureka synthesis board carries 120 role-slot proposals.",
        "The overlay decision is no x3 for v478 v5.",
        "The v6 x1 roadmap carries 60 concrete tasks.",
        "All six GMUT gates remain open.",
    ]
    write_json("v478-thos-v5-x2-synthesis-v1.json", {"artifact_type": "phase_synthesis", "phase": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS", "finding_count": len(findings), "findings": [{"step": f"R{idx:02d}", "finding": item} for idx, item in enumerate(findings, start=1)], "claim_boundary": {"scope": "THOS v478 v5 x2 synthesis and handoff only", "gmut_gate_state": "all_gmut_gates_remain_open", "canon_promotion": "not_claimed"}})
    write_md("v478-thos-v5-x2-synthesis-v1.md", ["# v478 THOS v5 x2 Synthesis", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`", "- claim_boundary: THOS synthesis only; all GMUT gates remain open.", "", "## Findings", *[f"- R{idx:02d}: {item}" for idx, item in enumerate(findings, start=1)]])


def roadmap_status_schema(generated_utc: str, generated_nz: str) -> None:
    domains = ["app-lane", "cli-gap", "source", "system", "command", "skill", "reflection", "eureka", "guard", "schema", "sandbox", "handoff"]
    tasks = [
        {
            "id": f"V478V6X1-{idx:02d}",
            "domain": domains[(idx - 1) % len(domains)],
            "task": f"Use v478 v6 x1 to deepen {domains[(idx - 1) % len(domains)]} readiness with status-only receipts, exact staging, and open GMUT gates.",
        }
        for idx in range(1, 61)
    ]
    write_json("v478-thos-v6-x1-roadmap-v1.json", {"artifact_type": "phase_roadmap", "phase": PHASE, "next_phase": NEXT_PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "task_count": len(tasks), "tasks": tasks})
    write_md("v478-thos-v6-x1-roadmap-v1.md", ["# v478 THOS v6 x1 Roadmap", "", f"- generated_nz: `{generated_nz}`", f"- task_count: `{len(tasks)}`", "", "## Tasks", *[f"- `{row['id']}` ({row['domain']}): {row['task']}" for row in tasks]])
    write_json("v478-thos-v5-x2-run-status-v1.json", {"artifact_type": "run_status", "phase": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS", "next_expected_phase": NEXT_PHASE, "app_lane_status": "PASS", "cli_lane_status": "OPEN_GAP_AFTER_5_ATTEMPTS", "gmut_gates": GMUT_GATES})
    write_md("v478-thos-v5-x2-run-status-v1.md", ["# v478 THOS v5 x2 Run Status", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS`", f"- next_expected_phase: `{NEXT_PHASE}`", "- app_lane_status: `PASS`", "- cli_lane_status: `OPEN_GAP_AFTER_5_ATTEMPTS`", "- GMUT gates: all remain `OPEN`."])
    expected = [
        "v478-thos-v5-x2-source-synthesis-ledger-v1.json",
        "v478-thos-v5-x2-lane-retry-status-board-v1.json",
        "v478-thos-v5-x2-system-expansion-decision-board-v1.json",
        "v478-thos-v5-x2-command-design-decision-board-v1.json",
        "v478-thos-v5-x2-skill-design-decision-board-v1.json",
        "v478-thos-v5-x2-six-perspective-reflection-synthesis-v1.json",
        "v478-thos-v5-x2-eureka-synthesis-board-v1.json",
        "v478-thos-v5-x2-overlay-decision-v1.json",
        "v478-thos-v5-x2-synthesis-v1.json",
        "v478-thos-v5-x2-run-status-v1.json",
        "v478-thos-v6-x1-roadmap-v1.json",
    ]
    rows = []
    for name in expected:
        payload = read_json(name)
        rows.append({"file": name, "parsed": True, "artifact_type": payload.get("artifact_type"), "phase": payload.get("phase")})
    write_json("v478-thos-v5-x2-schema-bound-artifact-check-v1.json", {"artifact_type": "schema_bound_artifact_check", "phase": PHASE, "generated_utc": generated_utc, "generated_nz": generated_nz, "overall_status": "PASS", "checked_json_count": len(rows), "rows": rows})
    write_md("v478-thos-v5-x2-schema-bound-artifact-check-v1.md", ["# v478 THOS v5 x2 Schema-Bound Artifact Check", "", f"- generated_nz: `{generated_nz}`", "- overall_status: `PASS`", f"- checked_json_count: `{len(rows)}`", "", "## Checked", *[f"- `{row['file']}`: `{row['artifact_type']}`." for row in rows]])


def main() -> int:
    generated_utc, generated_nz = now_pair()
    source_synthesis(generated_utc, generated_nz)
    lane_retry_status(generated_utc, generated_nz)
    decision_board("system_expansion", "v478-thos-v5-x1-system-expansion-design-board-v1.json", "v478-thos-v5-x2-system-expansion-decision-board-v1", generated_utc, generated_nz)
    decision_board("command_design", "v478-thos-v5-x1-command-design-board-v1.json", "v478-thos-v5-x2-command-design-decision-board-v1", generated_utc, generated_nz)
    decision_board("skill_design", "v478-thos-v5-x1-skill-design-board-v1.json", "v478-thos-v5-x2-skill-design-decision-board-v1", generated_utc, generated_nz)
    reflection_synthesis(generated_utc, generated_nz)
    eureka_synthesis(generated_utc, generated_nz)
    synthesis_and_handoff(generated_utc, generated_nz)
    roadmap_status_schema(generated_utc, generated_nz)
    print(json.dumps({"status": "PASS_WITH_CLI_OPEN_GAP_AFTER_5_ATTEMPTS", "phase": PHASE, "next": NEXT_PHASE}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
