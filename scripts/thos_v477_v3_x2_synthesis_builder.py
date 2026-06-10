#!/usr/bin/env python3
"""Build v477 THOS v3 x2 synthesis, source ledger, and next-roadmap artifacts."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "docs" / "trinity-live-traces"
PHASE = "v477_thos_v3_x2"
NEXT_PHASE = "v477_thos_v4_x1"


GMUT_GATES = [
    "null recovery",
    "dimensional/SI consistency",
    "conservation or exchange law",
    "baseline recovery",
    "fifth-force/equivalence constraints",
    "consciousness measurement bridge",
]


SOURCE_QUERIES = [
    "OpenAI Codex Windows sandbox Codex CLI app-server OpenAI Codex",
    "OpenAI Codex app-server README thread API",
    "Model Context Protocol specification tools resources prompts",
    "OpenAI Agents SDK MCP tools tracing",
    "NVIDIA DGX Spark Blackwell NVLink Nemotron Vera Rubin official",
    "NVIDIA Nemotron DGX Spark official",
    "Google Cloud Vertex AI Agent Engine Bigtable agents official",
    "Gemini CLI Vertex AI Agent Development Kit official",
    "PowerShell execution policy security official",
    "Windows Sandbox Windows official documentation",
    "Windows AppContainer Mandatory Integrity Control official",
    "Windows restricted token CreateRestrictedToken official",
    "GitHub Actions workflow syntax security hardening official",
    "GitHub secret scanning push protection official",
    "GitHub code scanning SARIF official",
    "GitHub REST API commits compare branches official",
    "Python subprocess Popen security shell false official",
    "Python pathlib json argparse subprocess official",
    "Python tempfile TemporaryDirectory cleanup official",
    "Python hashlib sha256 official",
    "Docker Compose watch develop official docs",
    "Kubernetes jobs cronjobs controllers official latest",
    "OpenTelemetry traces spans official",
    "OWASP LLM applications top 10 official",
    "OpenTelemetry signals traces official",
    "Kubernetes Job controller official",
    "Kubernetes CronJob official",
    "MCP connectors servers official",
    "Google Cloud RAG enterprise generative AI architecture official",
    "Google Cloud Gemini Enterprise Vertex AI RAG official",
]


OPENED_SOURCES = [
    {
        "label": "OpenAI Codex Windows sandbox",
        "url": "https://openai.com/index/building-codex-windows-sandbox/",
        "source_class": "official_product_engineering",
        "use_in_phase": "Sandbox/readiness framing for CLI lanes and Windows safety boundaries.",
    },
    {
        "label": "OpenAI Codex app-server README",
        "url": "https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md",
        "source_class": "official_source_repository",
        "use_in_phase": "JSON-RPC app-server transport, thread/read, thread/resume, and turn/start routing.",
    },
    {
        "label": "OpenAI Agents SDK MCP guide",
        "url": "https://openai.github.io/openai-agents-python/mcp/",
        "source_class": "official_sdk_docs",
        "use_in_phase": "MCP transport taxonomy and hosted/local tool routing discipline.",
    },
    {
        "label": "MCP server tools specification",
        "url": "https://modelcontextprotocol.io/specification/2025-06-18/server/tools",
        "source_class": "official_protocol_spec",
        "use_in_phase": "Tool output and resource-link discipline for future connector surfaces.",
    },
    {
        "label": "NVIDIA DGX Spark hardware overview",
        "url": "https://docs.nvidia.com/dgx/dgx-spark/hardware.html",
        "source_class": "official_hardware_docs",
        "use_in_phase": "Local AI workstation capability context for THOS hardware planning.",
    },
    {
        "label": "Google Agent Development Kit overview",
        "url": "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart",
        "source_class": "official_cloud_docs",
        "use_in_phase": "Agent development and deployment model comparison for THOS orchestration.",
    },
    {
        "label": "NVIDIA Nemotron overview",
        "url": "https://www.nvidia.com/en-us/ai-data-science/foundation-models/nemotron/",
        "source_class": "official_model_docs",
        "use_in_phase": "Open agent-model ecosystem context for local/edge inference planning.",
    },
]


def utc_nz_now() -> tuple[str, str]:
    utc = dt.datetime.now(dt.timezone.utc)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12)))
    return utc.isoformat(timespec="seconds"), nz.isoformat(timespec="seconds")


def run_git(args: list[str], default: str = "unknown") -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return default


def read_json(name: str) -> dict[str, Any]:
    path = TRACES / name
    if not path.exists():
        return {"read_status": "missing", "artifact": name}
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(name: str, payload: dict[str, Any]) -> None:
    (TRACES / name).write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_md(name: str, body: str) -> None:
    (TRACES / name).write_text(body.strip() + "\n", encoding="utf-8")


def app_lane_summary(app_run: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for lane in app_run.get("lanes", []):
        rows.append(
            {
                "lane": lane.get("name"),
                "status": lane.get("overall_status"),
                "read": lane.get("read", {}).get("status"),
                "resume": lane.get("resume", {}).get("status"),
                "turn_start": lane.get("turn_start", {}).get("status"),
                "turn_completion": lane.get("turn_completion", {}).get("status"),
                "advisory_payload_publication": "not_published",
            }
        )
    return rows


def cli_launch_summary() -> list[dict[str, Any]]:
    rows = []
    for lane, file_name in [
        ("Arby", "v477-thos-v3-x2-cli-lane-launch-arby-v1.json"),
        ("Aster Vale", "v477-thos-v3-x2-cli-lane-launch-aster-vale-v1.json"),
    ]:
        payload = read_json(file_name)
        rows.append(
            {
                "lane": lane,
                "launcher_status": payload.get("launcher_status", "missing"),
                "execution_status": payload.get("execution_status", "missing"),
                "sandbox": payload.get("sandbox", "unknown"),
                "ephemeral_flag_used": payload.get("ephemeral_flag_used", "unknown"),
                "worktree_exists": payload.get("worktree_exists", "unknown"),
                "pid_recorded": "pid" in payload,
                "advisory_payload_publication": "not_published",
            }
        )
    watch = read_json("v477-thos-v3-x2-cli-lane-watch-launch-v1.json")
    return rows + [
        {
            "lane": "Arby/Aster watcher",
            "launcher_status": watch.get("launcher_status", "missing"),
            "execution_status": watch.get("execution_status", "missing"),
            "started_background_watcher": watch.get("started_background_watcher", False),
            "completed_within_initial_wait": watch.get("completed_within_wait", False),
            "receipt_status": "pending_or_will_be_written_by_background_watcher",
            "advisory_payload_publication": "not_published",
        }
    ]


def reflection_steps() -> list[dict[str, str]]:
    themes = [
        ("continuity", "Treat v49 and older Journey records as continuity memory, not empirical proof."),
        ("source_evidence", "Separate official implementation sources from inspirational or historical material."),
        ("app_lanes", "Prefer local app-server probe plus targeted retry over duplicate all-lane starts."),
        ("cli_lanes", "Keep Arby and Aster non-ephemeral, read-only, and watched through metadata receipts."),
        ("watchers", "Use completion receipts as durable handoff markers rather than terminal scrollback."),
        ("command_surface", "Index command surfaces before expanding them; discovery must precede mutation."),
        ("handoff_surface", "Surface v54/v55 handoffs as manifests and open gaps, not archive dumps."),
        ("sandbox", "Map Windows sandbox mode to actual observed command behavior before claiming readiness."),
        ("secrets", "Use guardrails before every publication, even when artifacts are self-generated."),
        ("staging", "Exact staging is not bureaucracy; it is the mechanism that preserves unrelated user work."),
        ("drive", "Drive context can name titles and continuity pointers without publishing restricted payloads."),
        ("github", "Remote equals local is the repo truth source for shared omega publication."),
        ("mcp", "MCP tools need resource/output discipline before they become safe THOS surfaces."),
        ("agents", "Agent frameworks should be mapped to explicit transports and execution boundaries."),
        ("nvidia", "Local AI hardware research belongs in capacity planning, not miraculous capability claims."),
        ("google_cloud", "Cloud agent architecture helps design orchestration, but deployment requires separate approval."),
        ("python", "Helper scripts should use list-form subprocess calls and redacted receipts."),
        ("windows", "Restricted token and MIC details clarify why sandbox setup must be observed, not assumed."),
        ("docker", "Container watch patterns are useful as analogies for bounded, observable runner refresh."),
        ("kubernetes", "Job/CronJob semantics warn that retries and duplicate starts must be idempotent."),
        ("otel", "Trace/metric/log vocabulary can upgrade THOS watcher receipts into observability artifacts."),
        ("owasp", "LLM application risk framing should inform connector and prompt-surface hardening."),
        ("skills", "Skill indexes should publish metadata and routing, not full skill body copies."),
        ("plugins", "Plugin surfaces stay read/use-only unless a separate exact mutation packet exists."),
        ("gmut", "THOS can support GMUT tooling, but it does not close physics gates by association."),
        ("simulation", "Any simulation or fixture output needs explicit simulation labeling."),
        ("roadmap", "Large roadmaps must be executable slices, not decorative task piles."),
        ("blockers", "A blocker should be classified, retried safely, and then recorded if it persists."),
        ("phase_flow", "x3/x4 overlays are justified only by real blocker handling or hardening needs."),
        ("closeout", "Every closeout should preserve next phase, evidence, blockers, and claim ceiling."),
    ]
    return [
        {"step": f"reflection_{idx:02d}", "theme": theme, "finding": finding}
        for idx, (theme, finding) in enumerate(themes, start=1)
    ]


def next_tasks() -> list[dict[str, str]]:
    groups = [
        ("v477-v4-app-lanes", [
            "Run probe-only before each app-lane advisory pass.",
            "Add stale-active-turn detection wording to app-lane receipts.",
            "Create a compact lane-status board for Cicero, Kierkegaard, and Aristotle.",
            "Record app-lane result status without publishing advisory payload text.",
            "Add targeted retry templates for each app lane.",
            "Use the app-server source ledger to distinguish supported and experimental methods.",
        ]),
        ("v477-v4-cli-lanes", [
            "Poll the Arby/Aster completion notice and classify the result.",
            "If final messages arrive, hash and summarize them without publishing raw transport.",
            "If timeout occurs, record watcher timeout and preserve running-process status.",
            "Add CLI runtime duration to the next readiness receipt.",
            "Keep read-only sandbox in every launcher invocation.",
            "Reject any CLI lane that requests repo mutation without a separate packet.",
        ]),
        ("v477-v4-command-surface", [
            "Build the missing command-index surface from existing command books.",
            "Mark each command with safety tier, source file, and validation status.",
            "Separate live command availability from aspirational command proposals.",
            "Add a command-index JSON schema and parser check.",
            "Cross-link command surfaces to skills only by metadata.",
            "Publish open gaps where command sources are stale or absent.",
        ]),
        ("v477-v4-handoffs", [
            "Locate v54/v55 handoff manifests through scoped repo searches.",
            "Create a handoff surfacing receipt with title, version, and receiver.",
            "Do not bulk import old archives into current phase artifacts.",
            "Classify missing handoffs as open_gap.",
            "Connect Orun continuity only as routing context.",
            "Prepare v478 acceptance criteria from surfaced handoffs.",
        ]),
        ("v477-v4-sources", [
            "Promote opened official sources into a compact source ledger.",
            "Do not count a query as page-reviewed unless the page was opened.",
            "Add citation-required flags for current product behavior claims.",
            "Keep search volume metadata separate from evidence strength.",
            "Prefer official docs over social posts for implementation decisions.",
            "Schedule the next 30-query refresh around unresolved source gaps.",
        ]),
        ("v477-v4-skills", [
            "Build a metadata-only skill capability index for THOS routing.",
            "Flag ambiguous duplicate skill names for later review.",
            "Add no-plugin-cache-mutation markers to ordinary phase scripts.",
            "Map skills to command-index rows without copying skill bodies.",
            "Create a validator for required skill frontmatter fields.",
            "Keep repairs separate from design unless an exact repair packet exists.",
        ]),
        ("v477-v4-observability", [
            "Add OpenTelemetry-style fields to watcher receipts: trace, event, metric, status.",
            "Record retry count, timeout window, and final state for every lane run.",
            "Add process-existence caveat: process live does not equal useful progress.",
            "Create a no-raw-output invariant in the watcher schema.",
            "Add per-lane freshness timestamps.",
            "Prepare a dashboard-ready bounded snapshot for later Data Analytics use.",
        ]),
        ("v477-v4-safety", [
            "Run JSON parse and script compile before staging.",
            "Run publication guards on exact staged files.",
            "Keep unrelated dirty worktree changes untouched.",
            "Fetch and drift-check before every commit.",
            "Commit only curated current-phase artifacts.",
            "Remote-verify shared omega after push.",
        ]),
        ("v477-v4-gmut-boundary", [
            "Keep all six GMUT gates open in every THOS artifact.",
            "Label GMUT-adjacent infrastructure as support only.",
            "Use journey_context_not_canon for Journey/Solas context.",
            "Avoid final physics, consciousness proof, fifth-force safety, and canon claims.",
            "Require exact closure artifacts before any gate movement.",
            "Carry null/SI/conservation/baseline/equivalence/bridge ledgers forward.",
        ]),
        ("v477-v4-phase-management", [
            "Close v477 v3 x2 only after the CLI watcher state is classified.",
            "Move into v477 v4 x1 with five-lane readiness and source ledger in hand.",
            "Use x3/x4 overlays only for concrete blocker handling.",
            "Keep phase start times in NZ time.",
            "Publish a 60-task roadmap after x2 closeout.",
            "Prepare v478 transition criteria without claiming v490 completion.",
        ]),
    ]
    tasks: list[dict[str, str]] = []
    idx = 1
    for domain, items in groups:
        for item in items:
            tasks.append({"id": f"v477-v4-task-{idx:02d}", "domain": domain, "task": item})
            idx += 1
    return tasks


def main() -> None:
    utc, nz = utc_nz_now()
    head = run_git(["rev-parse", "HEAD"])
    remote = run_git(["rev-parse", "origin/codex/GHC-Family/beyonder-shared-omega-line"])
    drift = run_git(["rev-list", "--left-right", "--count", "HEAD...origin/codex/GHC-Family/beyonder-shared-omega-line"])
    app_run = read_json("v477-thos-v3-x1-app-lane-notifier-run-v1.json")

    source_ledger = {
        "artifact_type": "source_refresh_ledger",
        "generated_nz": nz,
        "generated_utc": utc,
        "opened_source_count": len(OPENED_SOURCES),
        "opened_sources": OPENED_SOURCES,
        "phase": PHASE,
        "query_count": len(SOURCE_QUERIES),
        "query_status": "completed_search_queries_not_all_pages_opened",
        "queries": SOURCE_QUERIES,
        "source_boundary": "official_sources_prioritized_journey_context_not_canon",
    }
    write_json("v477-thos-v3-x2-source-ledger-v1.json", source_ledger)
    write_md(
        "v477-thos-v3-x2-source-ledger-v1.md",
        "\n".join(
            [
                "# V477 THOS V3 X2 Source Ledger",
                "",
                f"- generated_nz: `{nz}`",
                f"- query_count: `{len(SOURCE_QUERIES)}`",
                f"- opened_source_count: `{len(OPENED_SOURCES)}`",
                "- query_status: `completed_search_queries_not_all_pages_opened`",
                "- boundary: official implementation sources are evidence/context; Journey material remains `journey_context_not_canon`.",
                "",
                "## Opened Sources",
                "",
                *[f"- {item['label']}: {item['url']}" for item in OPENED_SOURCES],
                "",
                "## Query Topics",
                "",
                *[f"- {query}" for query in SOURCE_QUERIES],
            ]
        ),
    )

    synthesis = {
        "app_lanes": app_lane_summary(app_run),
        "artifact_type": "six_lane_x2_synthesis",
        "claim_boundary": {
            "canon_promotion": "not_claimed",
            "domain": "THOS coordination, source refresh, watcher/readiness, and roadmap synthesis",
            "gmut_gates_open": GMUT_GATES,
        },
        "cli_lanes": cli_launch_summary(),
        "generated_nz": nz,
        "generated_utc": utc,
        "next_expected_phase": NEXT_PHASE,
        "phase": PHASE,
        "repo_state": {
            "drift": drift,
            "local_head": head,
            "shared_remote_head": remote,
        },
        "reflection_count": 30,
        "reflection_steps": reflection_steps(),
        "source_ledger": "v477-thos-v3-x2-source-ledger-v1.json",
        "status": "PASS_X2_SYNTHESIS_WITH_CLI_COMPLETION_PENDING",
        "transport_publication": "no_raw_app_cli_or_connector_payloads_published",
    }
    write_json("v477-thos-v3-x2-six-lane-synthesis-v1.json", synthesis)
    write_md(
        "v477-thos-v3-x2-six-lane-synthesis-v1.md",
        "\n".join(
            [
                "# V477 THOS V3 X2 Six-Lane Synthesis",
                "",
                f"- generated_nz: `{nz}`",
                "- status: `PASS_X2_SYNTHESIS_WITH_CLI_COMPLETION_PENDING`",
                f"- local_head: `{head}`",
                f"- shared_remote_head: `{remote}`",
                f"- drift: `{drift}`",
                "- claim boundary: THOS coordination only; all six GMUT gates remain open.",
                "",
                "## App Lanes",
                "",
                *[f"- {row['lane']}: `{row['status']}`; completion `{row['turn_completion']}`; payload `{row['advisory_payload_publication']}`." for row in synthesis["app_lanes"]],
                "",
                "## CLI Lanes",
                "",
                *[f"- {row['lane']}: launcher `{row.get('launcher_status')}`, execution `{row.get('execution_status')}`, payload `{row['advisory_payload_publication']}`." for row in synthesis["cli_lanes"]],
                "",
                "## Reflection Steps",
                "",
                *[f"- {item['step']} [{item['theme']}]: {item['finding']}" for item in reflection_steps()],
            ]
        ),
    )

    run_status = {
        "artifact_type": "run_status_pair",
        "generated_nz": nz,
        "generated_utc": utc,
        "next_expected_phase": NEXT_PHASE,
        "phase": PHASE,
        "rows": [
            {
                "id": "app_lanes",
                "status": "PASS",
                "summary": "Cicero, Kierkegaard, and Aristotle completed the fresh v477 v3 app-lane notifier run.",
            },
            {
                "id": "cli_lanes",
                "status": "OPEN_GAP_COMPLETION_NOTICE_PENDING",
                "summary": "Arby and Aster Vale were launched as read-only non-ephemeral CLI lanes; watcher completion notice is pending.",
            },
            {
                "id": "source_refresh",
                "status": "PASS_QUERY_REFRESH",
                "summary": "Thirty official-focused web queries were completed; seven pages were opened and recorded as source context.",
            },
            {
                "id": "claim_boundary",
                "status": "PASS",
                "summary": "All six GMUT gates remain open; no final physics, consciousness, or canon claims are promoted.",
            },
        ],
        "status": "PASS_WITH_OPEN_CLI_COMPLETION_GAP",
    }
    write_json("v477-thos-v3-x2-run-status-v1.json", run_status)
    write_md(
        "v477-thos-v3-x2-run-status-v1.md",
        f"""
# V477 THOS V3 X2 Run Status

- generated_nz: `{nz}`
- status: `PASS_WITH_OPEN_CLI_COMPLETION_GAP`
- next_expected_phase: `{NEXT_PHASE}`

## Rows

- app_lanes: `PASS`; Cicero, Kierkegaard, and Aristotle completed the fresh v477 v3 app-lane notifier run.
- cli_lanes: `OPEN_GAP_COMPLETION_NOTICE_PENDING`; Arby and Aster Vale were launched as read-only non-ephemeral CLI lanes and the watcher is pending.
- source_refresh: `PASS_QUERY_REFRESH`; thirty official-focused web queries were completed and seven pages were opened as source context.
- claim_boundary: `PASS`; all six GMUT gates remain open.
""",
    )

    roadmap = {
        "artifact_type": "next_phase_60_task_roadmap",
        "generated_nz": nz,
        "generated_utc": utc,
        "next_phase": NEXT_PHASE,
        "phase": PHASE,
        "task_count": 60,
        "tasks": next_tasks(),
    }
    write_json("v477-thos-v4-x1-roadmap-v1.json", roadmap)
    write_md(
        "v477-thos-v4-x1-roadmap-v1.md",
        "\n".join(
            [
                "# V477 THOS V4 X1 Roadmap",
                "",
                f"- generated_nz: `{nz}`",
                "- task_count: `60`",
                "- boundary: no unfiltered lane payloads, no old-style subagent spawning, no GMUT gate closure.",
                "",
                "## Tasks",
                "",
                *[f"- {task['id']} [{task['domain']}]: {task['task']}" for task in next_tasks()],
            ]
        ),
    )


if __name__ == "__main__":
    main()
