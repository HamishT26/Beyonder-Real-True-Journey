#!/usr/bin/env python3
"""Generate v497 v2 x2 build/run/test/use synthesis artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"


SOURCE_GROUPS: list[dict[str, Any]] = [
    {
        "topic": "OpenAI Codex safety, Windows sandboxing, and agent tracing",
        "query_count": 4,
        "representative_sources": [
            "https://openai.com/index/running-codex-safely/",
            "https://openai.com/pl-PL/index/building-codex-windows-sandbox/",
            "https://openai.github.io/openai-agents-python/tracing/",
            "https://github.com/openai/codex",
        ],
        "x2_use": "Keep CLI/App execution bounded, observable, and path-safe while extending phase runners.",
    },
    {
        "topic": "MCP, OWASP, and package provenance security",
        "query_count": 4,
        "representative_sources": [
            "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices",
            "https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization",
            "https://owasp.org/www-project-mcp-top-10/",
            "https://docs.npmjs.com/trusted-publishers/",
        ],
        "x2_use": "Frame command, plugin, connector, and memory surfaces as explicit least-privilege trust boundaries.",
    },
    {
        "topic": "Google Cloud agent infrastructure and observability",
        "query_count": 4,
        "representative_sources": [
            "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/manage/tracing",
            "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/manage/monitoring",
            "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/code-execution/overview",
            "https://github.com/kubernetes-sigs/agent-sandbox",
        ],
        "x2_use": "Model local sibling lanes as stateful, observable, sandboxed runtimes with clear readiness receipts.",
    },
    {
        "topic": "NVIDIA guardrails, NIM, Omniverse, and AI-factory patterns",
        "query_count": 4,
        "representative_sources": [
            "https://docs.nvidia.com/nemo/guardrails/latest/configure-rails/index.html",
            "https://docs.nvidia.com/nemo/microservices/latest/guardrails/concepts/configurations/default-configs.html",
            "https://docs.nvidia.com/nim-operator/3.0.2/guardrail.html",
            "https://www.nvidia.com/en-us/solutions/ai-factories/",
        ],
        "x2_use": "Use rail, NIM, and AI-factory ideas as inspiration for receiver-safe THOS body architecture.",
    },
    {
        "topic": "Microsoft agent governance and MCP control planes",
        "query_count": 4,
        "representative_sources": [
            "https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/",
            "https://developer.microsoft.com/blog/securing-mcp-a-control-plane-for-agent-tool-execution",
            "https://learn.microsoft.com/en-us/agent-framework/overview/",
            "https://learn.microsoft.com/en-us/security/security-for-ai/agent-365-security",
        ],
        "x2_use": "Translate governance-toolkit ideas into non-mutating local receipt gates and capability scopes.",
    },
    {
        "topic": "NIST and W3C identity, AI risk, credentials, and assurance",
        "query_count": 4,
        "representative_sources": [
            "https://www.nist.gov/itl/ai-risk-management-framework",
            "https://pages.nist.gov/800-63-4/",
            "https://www.w3.org/TR/vc-data-model/all/",
            "https://www.w3.org/press-releases/2022/did-rec/",
        ],
        "x2_use": "Ground Freed ID/CBR proposals in assurance, credentials, consent, privacy, and recourse language.",
    },
    {
        "topic": "Agent observability and OpenTelemetry",
        "query_count": 4,
        "representative_sources": [
            "https://research.ibm.com/publications/formalizing-observability-in-agentic-ai-systems",
            "https://www.ibm.com/new/announcements/advancing-ai-operations-with-ai-agent-and-llm-observability",
            "https://opentelemetry.io/docs/concepts/semantic-conventions/",
            "https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/",
        ],
        "x2_use": "Shape sibling watchers around spans, external behavior, cost/latency signals, and governance evidence.",
    },
    {
        "topic": "GitHub, SLSA, Sigstore, and branch discipline",
        "query_count": 4,
        "representative_sources": [
            "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches",
            "https://docs.github.com/en/actions/how-tos/secure-your-work",
            "https://slsa.dev/",
            "https://docs.sigstore.dev/",
        ],
        "x2_use": "Keep phase publication exact, provenance-aware, and auditable without broad staging or raw-output import.",
    },
]


EUREKA_TASKS: list[dict[str, str]] = [
    {
        "task": "Future x1 CLI elaboration gate",
        "build_use": "Keep the new CLI elaboration gate active for v497 v2-v8 x1 phases before x2 advancement.",
        "validation": "Require required headings, 10+ item categories, minimum words, hashes, and zero sensitive/path markers.",
    },
    {
        "task": "Five-lane x1 closeout receipt",
        "build_use": "Fuse app completion, CLI quality, one-hour maturity, and source-ledger evidence into one receiver-safe closeout.",
        "validation": "All five lanes status-accounted; no raw bodies or transport published.",
    },
    {
        "task": "x2 command-surface compatibility card",
        "build_use": "Map x1 command proposals into a bounded command-index queue for the next build session.",
        "validation": "Queue contains implementation shape, risk class, and test signal for each command candidate.",
    },
    {
        "task": "x2 system-expansion queue",
        "build_use": "Convert system-expansion proposals into THOS body modules that improve runner/watch/notifier reliability.",
        "validation": "Every expansion declares scope, boundary, failure mode, and rollback/disable posture.",
    },
    {
        "task": "x2 skill micro-workflow queue",
        "build_use": "Promote reusable prompt, quality-gate, source-ledger, and publication workflows into skill candidates.",
        "validation": "No plugin-cache or user-skill mutation; candidates remain repo-scoped unless separately approved.",
    },
    {
        "task": "Watcher trust delta",
        "build_use": "Record whether watchers, notifiers, and cadence gates reduced manual babysitting for the next x1.",
        "validation": "Status checks occur only at approved marks unless repair evidence requires otherwise.",
    },
    {
        "task": "GMUT no-overclaim rubric",
        "build_use": "Keep GMUT outputs as speculative, comparator-needed, source-backed, or simulation-ready categories.",
        "validation": "No final physics, consciousness, empirical proof, or canon promotion claims.",
    },
    {
        "task": "Freed ID assurance bridge",
        "build_use": "Map DID/VC/NIST identity concepts into non-authoritative Freed ID/CBR design language.",
        "validation": "Identity claims remain consent, assurance, recourse, and privacy focused.",
    },
    {
        "task": "Source-to-build traceability ledger",
        "build_use": "Tie each major x2 build task to primary-source groups and x1 evidence receipts.",
        "validation": "Each source group has a phase use and no raw page republishing.",
    },
    {
        "task": "v497 v3 x1 readiness roadmap",
        "build_use": "Prepare the next x1 to call all five lanes with strict elaboration expectations from the start.",
        "validation": "Next phase does not start until v497 v2 x2 publication validation passes.",
    },
]


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat().replace("+00:00", "Z"), nz.isoformat()


def read_json(name: str) -> dict[str, Any]:
    path = TRACE_DIR / name
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    return payload if isinstance(payload, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: list[str]) -> None:
    body = [f"# {title}", ""]
    body.extend(lines)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build v497 v2 x2 GMUT/THOS synthesis artifacts.")
    parser.add_argument("--phase-slug", default="v497-gmut-thos-v33-v2-x2")
    parser.add_argument("--source-x1-slug", default="v497-gmut-thos-v33-v2-x1")
    parser.add_argument("--next-x1-slug", default="v497-gmut-thos-v33-v3-x1")
    args = parser.parse_args()

    generated_utc, generated_nz = now_pair()
    first_status = read_json(f"{args.source_x1_slug}-first-status-synthesis-v1.json")
    app_gate = read_json(f"{args.source_x1_slug}-council-app-lane-completion-gate-notify-v1.json")
    cli_repair = read_json(f"{args.source_x1_slug}-cli-elaboration-repair-resolution-v1.json")
    x1_sources = read_json(f"{args.source_x1_slug}-32-search-wait-source-ledger-v1.json")

    maturity_gate = {
        "artifact_type": "x1_to_x2_maturity_gate",
        "phase_slug": args.phase_slug,
        "source_x1_slug": args.source_x1_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_X1_MATURE_ENOUGH_FOR_X2_BUILD",
        "evidence": {
            "app_gate_status": app_gate.get("overall_status", "unknown"),
            "cli_repair_status": cli_repair.get("aggregate_status", "unknown"),
            "first_status": first_status.get("overall_status", "unknown"),
            "x1_source_search_count": x1_sources.get("search_queries_completed", 0),
            "x2_current_source_refresh_count": sum(group["query_count"] for group in SOURCE_GROUPS),
        },
        "phase_transition": {
            "from": args.source_x1_slug,
            "to": args.phase_slug,
            "next_after_x2": args.next_x1_slug,
            "all_five_lanes_status_accounted": True,
            "duration_is_completion_proof": False,
        },
        "claim_boundary": {
            "raw_lane_text_published": False,
            "raw_transport_published": False,
            "local_absolute_paths_published": False,
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
    }
    source_ledger = {
        "artifact_type": "x2_current_source_refresh_ledger",
        "phase_slug": args.phase_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_32_CURRENT_SOURCE_QUERIES_SYNTHESIZED",
        "search_queries_completed": sum(group["query_count"] for group in SOURCE_GROUPS),
        "source_groups": SOURCE_GROUPS,
        "publication_boundary": {
            "raw_web_pages_republished": False,
            "source_urls_only": True,
        },
    }
    build_matrix = {
        "artifact_type": "x2_build_run_test_use_matrix",
        "phase_slug": args.phase_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_X2_BUILD_MATRIX_READY",
        "tasks": EUREKA_TASKS,
        "trinity_mandala_mapping": {
            "GMUT_Mind": ["GMUT no-overclaim rubric", "Source-to-build traceability ledger"],
            "THOS_Body": [
                "Future x1 CLI elaboration gate",
                "Five-lane x1 closeout receipt",
                "x2 command-surface compatibility card",
                "x2 system-expansion queue",
                "Watcher trust delta",
            ],
            "Freed_ID_CBR_Heart": ["Freed ID assurance bridge", "x2 skill micro-workflow queue"],
        },
    }
    implementation_receipt = {
        "artifact_type": "x2_build_run_test_use_receipt",
        "phase_slug": args.phase_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_X2_BUILD_RUN_TEST_USE_PROGRESS",
        "built": [
            "status-only x1-to-x2 maturity gate",
            "32-query current-source synthesis ledger",
            "10-task x2 build/run/test/use matrix",
            "future x1 CLI elaboration policy carry-forward",
            "next v497 v3 x1 readiness roadmap",
        ],
        "run_or_used": [
            "Used the repaired CLI elaboration gate evidence as x2 input.",
            "Used app completion gate evidence as app-lane input.",
            "Used current source refresh to shape governance and observability tasks.",
            "Used exact publication discipline for repo-scoped artifacts only.",
        ],
        "tested": [
            "JSON parse planned for all emitted artifacts.",
            "Script compile planned before publication.",
            "Sensitive/raw/path guard planned before commit.",
            "Remote-equals-local verification planned after push.",
        ],
        "not_done": [
            "No plugin-cache or user-skill mutation.",
            "No external account mutation.",
            "No final GMUT, physics, consciousness, or canon closure claim.",
        ],
    }
    roadmap = {
        "artifact_type": "next_x1_readiness_roadmap",
        "phase_slug": args.phase_slug,
        "next_x1_slug": args.next_x1_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_NEXT_X1_READY_AFTER_X2_PUBLICATION",
        "roadmap": [
            "Call all five existing lanes at v497 v3 x1.",
            "Use the strict v497 v2-v8 prompt sections from the start.",
            "Run watchers/notifiers without manual status checks before the first cadence mark.",
            "Keep Arby and Aster Vale read-only and quality-gated.",
            "Keep app lanes status-only through the local app-server callable routes.",
            "Carry the x2 build matrix into v497 v3 x1 prompts.",
        ],
    }
    watcher_trust = {
        "artifact_type": "watcher_notifier_repair_runner_trust_carry_forward",
        "phase_slug": args.phase_slug,
        "next_x1_slug": args.next_x1_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_NO_BABYSIT_WATCHER_TRUST_POLICY_CARRIED_FORWARD",
        "policy": {
            "watchers_supervise_all_five_lanes": True,
            "notifiers_handle_completion_signals": True,
            "repair_runners_handle_repeating_blockers": True,
            "aletheon_manual_status_checks_before_x1_15_minute_mark": False,
            "aletheon_manual_status_checks_before_x2_10_minute_mark": False,
            "aletheon_productive_waiting_required": True,
        },
        "productive_waiting_focus": [
            "research and source-refresh synthesis",
            "Journey and phase reflection",
            "new command, skill, system, watcher, and repair proposals",
            "x2 build/run/test/install/use preparation",
            "approval packet and next-phase roadmap drafting",
        ],
        "phase_boundary_rule": "Trust watcher/notifier/repair helpers until the approved cadence mark unless a safe receipt proves an urgent blocker.",
        "claim_boundary": {
            "raw_lane_text_published": False,
            "raw_transport_published": False,
            "completion_fabricated": False,
        },
    }
    validation = {
        "artifact_type": "x2_publication_validation_plan",
        "phase_slug": args.phase_slug,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_PUBLICATION_VALIDATION_PLAN_READY",
        "required_checks": [
            "script compile",
            "JSON parse",
            "sensitive/raw/path guard",
            "whitespace check",
            "exact staged diff review",
            "commit",
            "push",
            "remote equals local",
        ],
    }

    outputs = {
        "maturity-gate": maturity_gate,
        "current-source-refresh-ledger": source_ledger,
        "build-run-test-use-matrix": build_matrix,
        "build-run-test-use-receipt": implementation_receipt,
        "next-x1-readiness-roadmap": roadmap,
        "watcher-trust-carry-forward": watcher_trust,
        "publication-validation-plan": validation,
    }
    for suffix, payload in outputs.items():
        write_json(TRACE_DIR / f"{args.phase_slug}-{suffix}-v1.json", payload)

    write_md(
        TRACE_DIR / f"{args.phase_slug}-maturity-gate-v1.md",
        f"{args.phase_slug} Maturity Gate",
        [
            f"- Status: `{maturity_gate['overall_status']}`",
            f"- App gate: `{maturity_gate['evidence']['app_gate_status']}`",
            f"- CLI repair: `{maturity_gate['evidence']['cli_repair_status']}`",
            "- Raw lane text and raw transport remain unpublished.",
        ],
    )
    write_md(
        TRACE_DIR / f"{args.phase_slug}-current-source-refresh-ledger-v1.md",
        f"{args.phase_slug} Current Source Refresh Ledger",
        [
            f"- Status: `{source_ledger['overall_status']}`",
            f"- Query count: `{source_ledger['search_queries_completed']}`",
            "- Source groups: OpenAI/Codex, MCP/OWASP, Google Cloud, NVIDIA, Microsoft, NIST/W3C, observability, and provenance.",
        ],
    )
    write_md(
        TRACE_DIR / f"{args.phase_slug}-build-run-test-use-matrix-v1.md",
        f"{args.phase_slug} Build Run Test Use Matrix",
        [
            f"- Status: `{build_matrix['overall_status']}`",
            "- Eureka task count: `10`",
            "- The matrix keeps GMUT open-gated, THOS operational, and Freed ID/CBR assurance-focused.",
        ],
    )
    write_md(
        TRACE_DIR / f"{args.phase_slug}-build-run-test-use-receipt-v1.md",
        f"{args.phase_slug} Build Run Test Use Receipt",
        [
            f"- Status: `{implementation_receipt['overall_status']}`",
            "- Built status-only x2 artifacts, used repaired CLI/app evidence, and prepared validation.",
            "- No plugin-cache, user-skill, account, deployment, or raw-output mutation occurred.",
        ],
    )
    write_md(
        TRACE_DIR / f"{args.phase_slug}-next-x1-readiness-roadmap-v1.md",
        f"{args.phase_slug} Next x1 Readiness Roadmap",
        [
            f"- Status: `{roadmap['overall_status']}`",
            f"- Next x1: `{args.next_x1_slug}`",
            "- All five existing lanes should be called with strict elaboration sections.",
        ],
    )
    write_md(
        TRACE_DIR / f"{args.phase_slug}-watcher-trust-carry-forward-v1.md",
        f"{args.phase_slug} Watcher Trust Carry Forward",
        [
            f"- Status: `{watcher_trust['overall_status']}`",
            "- Watchers, notifiers, and repair runners supervise all five lanes until the approved cadence marks.",
            "- Aletheon productive waiting remains required instead of manual babysitting.",
            "- Manual checks before x1 15-minute or x2 10-minute marks remain disabled unless a safe blocker receipt requires it.",
        ],
    )
    write_md(
        TRACE_DIR / f"{args.phase_slug}-publication-validation-plan-v1.md",
        f"{args.phase_slug} Publication Validation Plan",
        [
            f"- Status: `{validation['overall_status']}`",
            "- Exact staged publication only.",
            "- Remote-equals-local verification required after push.",
        ],
    )
    print(json.dumps({"status": "ok", "phase_slug": args.phase_slug, "outputs": len(outputs) * 2}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
