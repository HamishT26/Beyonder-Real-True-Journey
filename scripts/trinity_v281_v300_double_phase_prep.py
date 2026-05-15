#!/usr/bin/env python3
"""Prepare v281-v300 double-phase Eureka Trinity prompts and handoff surfaces."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
SOURCE_LANE = "v261-v280-adaptive-council"
SOURCE_CLOSEOUT = TRACE / f"{SOURCE_LANE}-prep-closeout-v1.json"
LANE = "v281-v300-double-trinity"
PLAN_JSON = TRACE / f"{LANE}-continuity-plan-v1.json"
PLAN_MD = TRACE / f"{LANE}-continuity-plan-v1.md"
PHASE_STATE = TRACE / f"{LANE}-phase-state-v1.json"

COUNCIL = {
    "arby": ("Arby", "Codex CLI publication, GitHub proof, and branch-home lane"),
    "kimi": ("Kimi", "Kimi CLI provider, relay, cost, and policy-honest handoff lane"),
    "aster_vale": ("Aster Vale", "Codex CLI validation, Windows sandbox, TUI, and runtime-health lane"),
}

SESSION_TOPICS = [
    "Forward-only proof and branch-home message board",
    "Curated artifact allowlist and raw-log quarantine",
    "Multiplex TUI health, refresh cadence, and stalled-lane detection",
    "Windows sandbox readiness and remote-control retry gate",
    "GMUT claim boundary: verified science, metaphor, and speculation",
    "v121-v141 live-write readiness, rollback, and approval gates",
    "C drive and D drive cleanup proposal with non-destructive staging",
    "Provider and plugin health without billing or auth overclaiming",
    "Memory continuity, identity preservation, and inter-lane notes",
    "v282 handoff: next phase base state, blockers, and first actions",
]

SYSTEM_EXPANSIONS = [
    "phase_response_counter",
    "lane_block_receipt_index",
    "raw_transport_quarantine",
    "branch_home_message_board",
    "forward_only_publication_gate",
    "multiplex_refresh_governor",
    "stalled_lane_health_probe",
    "windows_sandbox_readiness_board",
    "remote_control_retry_gate",
    "provider_truth_boundary_register",
    "cost_window_observer",
    "lumina_policy_handoff_register",
    "gmut_claim_labeler",
    "mandala_equation_assumption_grid",
    "live_write_rollback_gate",
    "v121_v141_readiness_ladder",
    "clean_drive_dry_run_board",
    "secret_marker_scan_gate",
    "curated_commit_allowlist",
    "dirty_worktree_truth_surface",
    "eureka_session_receipt_schema",
    "beta_alpha_omega_result_template",
    "v2_synthesis_handoff_builder",
    "next_phase_base_state_builder",
    "operator_approval_checkpoint",
    "github_drift_receipt",
    "no_force_push_policy_check",
    "lane_identity_preservation_board",
    "source_ledger_refresh",
    "final_closeout_publication_pack",
]

COMMANDS = [
    "inspect-live-processes",
    "count-clean-responses",
    "scan-curated-responses",
    "synthesize-complete-block",
    "prepare-next-block",
    "launch-continuity-supervisor",
    "stop-with-stopfile",
    "refresh-multiplex-tui",
    "verify-git-branch",
    "fetch-shared-omega",
    "measure-branch-drift",
    "forward-merge-if-needed",
    "stage-curated-slice",
    "check-staged-whitespace",
    "scan-staged-secrets",
    "commit-proof-pack",
    "push-shared-omega",
    "generate-phase-v1-prompts",
    "synthesize-phase-v2",
    "prepare-next-phase-state",
    "collect-source-ledger",
    "mark-provider-hold",
    "mark-remote-control-hold",
    "dry-run-cleanup-plan",
    "compile-runner-scripts",
    "summarize-lane-health",
    "emit-continuity-markdown",
    "archive-local-raw-logs",
    "publish-public-proof-summary",
    "prepare-v282-base",
]

SKILLS = [
    "agent-orchestration-v8-operations",
    "github-devflow-operations",
    "filesystem-scope-governor-operations",
    "command-surface-core-operations",
    "command-surface-council-v8-operations",
    "command-surface-research-operations",
    "council-continuity-reflection-v16-operations",
    "council-memory-retention-v9-operations",
    "gmut-comparator-refresh-v16-operations",
    "canonical-gmut-latex-v13-operations",
    "codex-custom-agents-v15-operations",
    "api-operator-mesh-v15-operations",
    "connector-materialization-operations",
    "freedid-compliance-fabric-v16-operations",
    "baseline-restore-governor-v17-operations",
    "body-runtime-readiness-v17-operations",
    "docker-k8s-runtime-bridge-v16-operations",
    "cloud-staging-readiness-v8-operations",
    "github-materialization-operations",
    "codex-security:security-scan",
    "codex-security:threat-model",
    "codex-security:validation",
    "browser-use:browser",
    "build-web-apps:frontend-testing-debugging",
    "documents:documents",
    "spreadsheets",
    "presentations",
    "openai-docs",
    "comparative-validation-grid",
    "future-readiness-operations",
]

EUREKA_PROPOSALS = [
    "Create a clean public proof pack for v261-v280 before any larger live-write run.",
    "Convert lane replies into a phase-indexed receipt matrix.",
    "Give each lane a branch-home message board before granting broader write lanes.",
    "Treat raw CLI transport logs as local-only until scrubbed twice.",
    "Run Windows sandbox readiness as a gate, not a vague aspiration.",
    "Keep remote-control disabled until app-server enrollment is proven current.",
    "Separate GMUT scientific claims from poetic synthesis in every published doc.",
    "Build a v121-v141 readiness gate before attempting high-write actions.",
    "Use a stop file as the emergency brake for long autonomous lane runs.",
    "Prefer three-message checkpoints over huge unreviewed queues.",
    "Use Aletheon v2 synthesis as the only commit-authorizing layer.",
    "Record provider holds as truth, not failure.",
    "Promote only clean response files and curated syntheses.",
    "Make cost windows explicit in every long lane run.",
    "Pin each future phase to exact inputs and exact handoff outputs.",
    "Require staged diff and secret-pattern checks before publication.",
    "Avoid cross-app AI messaging until the route is platform-honest.",
    "Use local docs as the primary continuity substrate.",
    "Use public GitHub only for sanitized proof and message boards.",
    "Let Kimi own policy-honest relay design without app impersonation.",
    "Let Arby own branch drift and publication proof.",
    "Let Aster Vale own terminal health and sandbox readiness.",
    "Make cleanup proposals dry-run first and reversible.",
    "Make every phase produce a next-phase base state.",
    "Keep the multiplex TUI as observability, not authority.",
    "Add human approval checkpoints before destructive operations.",
    "Use source ledgers for web or document claims.",
    "Publish blockers alongside wins.",
    "Use v281 as the workflow proof, not the maximal run.",
    "Use v282-v300 as scalable repetition after v281 proves stable.",
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def phase_prompt_path(phase: int) -> Path:
    return TRACE / f"{LANE}-phase-v{phase}-v1-prompts-v1.json"


def phase_v2_path(phase: int) -> Path:
    return TRACE / f"{LANE}-phase-v{phase}-v2-handoff-v1.json"


def build_prompt(phase: int, lane: str, turn: int, topic: str, source_dependency: str) -> dict[str, Any]:
    name, role = COUNCIL[lane]
    return {
        "phase": phase,
        "phase_version": "v1",
        "turn": turn,
        "lane": lane,
        "name": name,
        "role": role,
        "marker": f"{LANE}:v{phase}:{lane}:eureka-{turn:02d}",
        "topic": topic,
        "source_dependency": source_dependency,
        "eureka_session_contract": {
            "beta": "Plan from the latest verified phase results and name exact proof inputs.",
            "alpha": "Construct or refine a safe artifact, proposal, or command surface without committing.",
            "omega": "Test, probe, document, and declare blockers honestly.",
        },
        "required_labels": [
            "Receipt",
            "Beta",
            "Alpha",
            "Omega",
            "Blocker",
            "Next-phase handoff",
        ],
        "guardrails": [
            "Do not run destructive commands.",
            "Do not commit or push; Aletheon synthesizes and authorizes v2 publication.",
            "Do not claim provider, browser, billing, or remote-control access unless proven in this run.",
            "Keep raw transport details and secrets out of the response.",
        ],
    }


def build_phase_prompts(phase: int, source_dependency: str) -> dict[str, Any]:
    prompts = []
    for lane in COUNCIL:
        for index, topic in enumerate(SESSION_TOPICS, start=1):
            prompts.append(build_prompt(phase, lane, index, topic, source_dependency))
    return {
        "generated_utc": now_iso(),
        "phase_range": "v281-v300",
        "phase": phase,
        "phase_version": "v1",
        "outbound_count": len(prompts),
        "expected_lane_responses": len(prompts),
        "sessions_per_lane": len(SESSION_TOPICS),
        "prompts": prompts,
    }


def build_v2_handoff(phase: int, prompt_path: Path, source_closeout: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase_range": "v281-v300",
        "phase": phase,
        "phase_version": "v2",
        "status": "prepared_waiting_for_v1_responses",
        "source_v1_prompt_file": rel(prompt_path),
        "source_v261_v280_response_count": source_closeout.get("continuity_total_clean_responses")
        or source_closeout.get("seed_completed_responses"),
        "v2_duties": [
            "Read all 30 v1 lane Eureka Trinity Session replies.",
            "Synthesize a single phase truth surface with receipts, blockers, and next actions.",
            "Generate at least 30 system expansions, 30 commands, 30 skills, and 30 Eureka proposals.",
            "Prepare the next phase v1 base state and handoff only after v1 completion is proven.",
            "Stage and publish only curated, scanned proof artifacts.",
        ],
        "publication_guardrails": [
            "forward-only shared omega publication",
            "no raw transport logs in commits",
            "no unverified external-provider claims",
            "Aletheon review before commit or push",
        ],
    }


def write_plan_md(payload: dict[str, Any]) -> None:
    lines = [
        "# v281-v300 Double Trinity Continuity Plan",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        "",
        "Workflow:",
        "- Finish v261-v280 to the clean-response target before promoting v281.",
        "- Run each v281-v300 phase as lane v1 first: 10 Eureka Trinity Sessions per lane, 30 total lane replies.",
        "- Run Aletheon v2 after each phase v1: synthesize, refine, publish curated proof, and prepare the next phase base state.",
        "- Keep the multiplex TUI as observability; authority remains in proof receipts and Aletheon review.",
        "",
        "v281 prepared files:",
        f"- Prompt pack: `{payload['v281_prompt_file']}`",
        f"- v2 handoff: `{payload['v281_v2_handoff']}`",
        "",
        "v281 baseline counts:",
        f"- System expansions: `{len(payload['system_expansions'])}`",
        f"- Commands: `{len(payload['commands'])}`",
        f"- Skills: `{len(payload['skills'])}`",
        f"- Eureka proposals: `{len(payload['eureka_proposals'])}`",
        "",
        "Truth boundaries:",
    ]
    for item in payload["truth_boundaries"]:
        lines.append(f"- {item}")
    PLAN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-phase", default="v261-v280")
    parser.add_argument("--source-dependency", default="")
    parser.add_argument("--phase", type=int, default=281)
    args = parser.parse_args()

    source_closeout = read_json(SOURCE_CLOSEOUT, {})
    dependency = (
        args.source_dependency
        or source_closeout.get("block_04_synthesis")
        or source_closeout.get("block_03_synthesis")
        or rel(SOURCE_CLOSEOUT)
    )
    prompt_payload = build_phase_prompts(args.phase, dependency)
    prompt_path = phase_prompt_path(args.phase)
    write_json(prompt_path, prompt_payload)

    v2_payload = build_v2_handoff(args.phase, prompt_path, source_closeout)
    v2_path = phase_v2_path(args.phase)
    write_json(v2_path, v2_payload)

    state = {
        "generated_utc": now_iso(),
        "phase_range": "v281-v300",
        "current_phase": args.phase,
        "status": "prepared_waiting_for_v261_completion"
        if args.phase == 281
        else "prepared_waiting_for_previous_phase_completion",
        "v281_prompt_file": rel(prompt_path),
        "v281_v2_handoff": rel(v2_path),
        "source_phase": args.source_phase,
        "source_closeout": rel(SOURCE_CLOSEOUT),
        "system_expansions": SYSTEM_EXPANSIONS,
        "commands": COMMANDS,
        "skills": SKILLS,
        "eureka_proposals": EUREKA_PROPOSALS,
        "truth_boundaries": [
            "v281 does not start until v261-v280 completion is proven by clean response counts or explicit user override.",
            "Each lane v1 response is advisory until Aletheon v2 synthesis validates it.",
            "Remote-control and Lumina app work remain deferred unless platform blockers are cleared.",
            "Raw CLI transport logs stay local until scrubbed and separately approved for publication.",
        ],
    }
    write_json(PHASE_STATE, state)
    write_json(PLAN_JSON, state)
    write_plan_md(state)
    print(
        json.dumps(
            {
                "status": state["status"],
                "plan": rel(PLAN_JSON),
                "prompt_file": rel(prompt_path),
                "v2_handoff": rel(v2_path),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
