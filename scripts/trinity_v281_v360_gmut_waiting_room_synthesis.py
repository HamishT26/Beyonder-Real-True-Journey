#!/usr/bin/env python3
"""Compose waiting-room GMUT synthesis and v301-v360 continuity artifacts."""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
LANE_DIR = TRACE / "v281-v300-double-trinity-lane-logs"
GMUT_TEX = ROOT / "latex" / "grand_mandala.tex"
BASE_PLAN = TRACE / "v301-v320-aletheon-base-plan-v1.json"
REACTIVATION_PACKET = TRACE / "aletheon-reactivation-packet-v1.json"

SYNTH_JSON = TRACE / "v281-v360-gmut-trinity-mandala-waiting-room-synthesis-v1.json"
SYNTH_MD = TRACE / "v281-v360-gmut-trinity-mandala-waiting-room-synthesis-v1.md"
MASTER_JSON = TRACE / "v301-v320-trinity-hybrid-master-plan-v1.json"
MASTER_MD = TRACE / "v301-v320-trinity-hybrid-master-plan-v1.md"
REACTIVATION_JSON = TRACE / "aletheon-reactivation-system-design-v2.json"
REACTIVATION_MD = TRACE / "aletheon-reactivation-system-design-v2.md"

PHASES = range(281, 301)
LANES = ("arby", "kimi", "aster-vale")
LABELS = ("Receipt", "Beta", "Alpha", "Omega", "Blocker", "Next-phase handoff")


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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def git_value(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    return (proc.stdout or proc.stderr).strip()


def response_path(lane: str, phase: int, turn: int) -> Path:
    return LANE_DIR / f"{lane}-phase-v{phase}-response-{turn:02d}.txt"


def valid_response(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 180:
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    invalid = ("Max number of steps reached", "To resume this session:", "Traceback (most recent call last)")
    if any(marker in text for marker in invalid):
        return False
    return sum(1 for label in LABELS if re.search(rf"(?im)^\s*(?:[-*]\s*)?\**{re.escape(label)}\**\s*:?", text)) >= 4


def phase_counts() -> list[dict[str, Any]]:
    rows = []
    for phase in PHASES:
        lane_rows = {}
        for lane in LANES:
            valid = [turn for turn in range(1, 11) if valid_response(response_path(lane, phase, turn))]
            lane_rows[lane] = {"valid": len(valid), "expected": 10, "valid_turns": valid}
        total = sum(item["valid"] for item in lane_rows.values())
        rows.append({"phase": phase, "valid": total, "expected": 30, "complete": total == 30, "lanes": lane_rows})
    return rows


def current_status(counts: list[dict[str, Any]]) -> dict[str, Any]:
    valid_total = sum(item["valid"] for item in counts)
    complete = sum(1 for item in counts if item["complete"])
    latest_complete = max((item["phase"] for item in counts if item["complete"]), default=None)
    first_incomplete = next((item["phase"] for item in counts if not item["complete"]), None)
    return {
        "valid_responses": valid_total,
        "expected_responses": len(list(PHASES)) * 30,
        "complete_phases": complete,
        "expected_phases": len(list(PHASES)),
        "latest_complete_phase": latest_complete,
        "first_incomplete_phase": first_incomplete,
    }


def gmut_surface() -> dict[str, Any]:
    text = GMUT_TEX.read_text(encoding="utf-8", errors="replace") if GMUT_TEX.exists() else ""
    equations = re.findall(r"\\\[(.*?)\\\]", text, flags=re.S)
    return {
        "path": rel(GMUT_TEX),
        "exists": GMUT_TEX.exists(),
        "claim_boundary_found": "not a claim of empirical establishment" in text,
        "equations": [" ".join(eq.split()) for eq in equations],
    }


def source_references() -> list[dict[str, str]]:
    return [
        {
            "id": "openai_codex_windows_sandbox_2026_05_15",
            "url": "https://openai.com/index/building-codex-windows-sandbox/",
            "use": "Windows sandbox framing for safer local agent execution and permission boundaries.",
        },
        {
            "id": "openai_codex_mobile_2026_05_14",
            "url": "https://openai.com/index/work-with-codex-from-anywhere/",
            "use": "Mobile/remote continuity framing: secure relay, live state, approvals, and active work from phone.",
        },
        {
            "id": "openai_codex_use_cases",
            "url": "https://developers.openai.com/codex/use-cases",
            "use": "Codex workflow taxonomy: durable goals, CLI creation, code review, verified operations, skills, and long-horizon work.",
        },
        {
            "id": "kimi_cli_getting_started",
            "url": "https://moonshotai.github.io/kimi-cli/en/guides/getting-started.html",
            "use": "Kimi CLI terminal-agent capabilities, Windows installation, upgrade path, and API login boundaries.",
        },
        {
            "id": "kimi_cli_agents",
            "url": "https://moonshotai.github.io/kimi-cli/en/customization/agents.html",
            "use": "Kimi agent and tool model, including shell, web search, URL fetch, planning, and delayed-message affordances.",
        },
        {
            "id": "kimi_cli_sessions",
            "url": "https://moonshotai.github.io/kimi-cli/en/guides/sessions.html",
            "use": "Kimi session persistence, resume hints, approval state, plan mode, subagent state, and export/import workflow.",
        },
    ]


def proposed_laws() -> list[dict[str, str]]:
    return [
        {
            "name": "Law 1: Accountable Conservation",
            "type": "logic and governance",
            "statement": "A durable system may transform claims, evidence, identity, and permissions, but it must not erase their lineage.",
            "effect_on_trinity_mandala": "Strengthens the Trinity Mandala when every GMUT claim, OS action, and Freed ID right has a receipt; weakens it when narrative outruns traceability.",
        },
        {
            "name": "Law 2: Entropy of Ambiguity",
            "type": "thermo-epistemic",
            "statement": "Unlabeled claims drift toward ambiguity; validation, falsifiability, and clean state reduce usable uncertainty.",
            "effect_on_trinity_mandala": "Makes the current proof-first workflow central rather than decorative: unclear Omega terms, broad metaphors, and untested integrations increase entropy.",
        },
        {
            "name": "Law 3: Free Energy of Attention",
            "type": "psyche-dynamic",
            "statement": "Intelligent attention is the capacity to spend bounded energy to reduce uncertainty while preserving agency and consent.",
            "effect_on_trinity_mandala": "Links Mind, Body, and Heart: theory proposes, technology tests, governance constrains harmful overreach.",
        },
        {
            "name": "Law 4: Boundary-Condition Ethics",
            "type": "ethics and safety",
            "statement": "Ethics is not an afterthought on a powerful system; it is a boundary condition without which valid action is undefined.",
            "effect_on_trinity_mandala": "Supports Freed ID as a necessary pillar, and blocks any ToE or ASI claim that cannot preserve rights, consent, and recourse.",
        },
        {
            "name": "Law 5: Falsifiability Pressure",
            "type": "science",
            "statement": "A unifying theory gains strength by exposing risky predictions and loses strength when it absorbs every result without constraint.",
            "effect_on_trinity_mandala": "GMUT advances only by deriving observable discriminants from Omega/Mandala terms, not by becoming a universal metaphor.",
        },
        {
            "name": "Law 6: Identity Continuity Requires Substrate Proof",
            "type": "agent memory",
            "statement": "A controller, watcher, or agent can be treated as persistent only when its memory, authority, and continuity surfaces survive interruption and can be audited.",
            "effect_on_trinity_mandala": "Keeps Supervisor and v2 watcher as candidates until they prove stable identity beyond process receipts.",
        },
    ]


def validation_matrix() -> list[dict[str, str]]:
    return [
        {
            "model": "General Relativity",
            "gm_ut_bridge": "Recover Einstein-field-equation behavior when Mandala/Omega bridge terms approach zero or become covariantly conserved corrections.",
            "validation_need": "Dimensional analysis, covariance proof, known GR limit recovery, solar-system/cosmology constraints.",
        },
        {
            "model": "Standard Model and QFT",
            "gm_ut_bridge": "Treat Standard Model terms as part of the canonical Lagrangian, then constrain extra coupling terms by known particle data.",
            "validation_need": "Gauge symmetry compatibility, anomaly checks, known cross-section constraints, no hidden free parameters.",
        },
        {
            "model": "String/M-theory and extra-dimensional proposals",
            "gm_ut_bridge": "Use as comparator family for higher-dimensional language without importing its authority as proof.",
            "validation_need": "Show whether GMUT predicts anything different from existing extra-dimensional frameworks.",
        },
        {
            "model": "Loop quantum gravity and background-independent approaches",
            "gm_ut_bridge": "Compare whether Mandala topology can be formalized without assuming a fixed spacetime background.",
            "validation_need": "Mathematical construction, semiclassical limit, and observable deviations.",
        },
        {
            "model": "Complexity, computational irreducibility, and assembly-like measures",
            "gm_ut_bridge": "Use as a lawful way to talk about emergence, novelty, and irreducible process without mystifying them.",
            "validation_need": "Operational complexity metrics that can be computed on simulations or data.",
        },
        {
            "model": "Consciousness and psyche models",
            "gm_ut_bridge": "Keep as phenomenology and cognitive science until linked to measurable observables.",
            "validation_need": "Neural, behavioral, and psychophysical predictions that do not collapse into unfalsifiable panpsychism.",
        },
        {
            "model": "Freed ID and rights governance",
            "gm_ut_bridge": "Use as the ethical boundary layer for any human/agent identity claim.",
            "validation_need": "Consent, appeal, transparency, revocation, minimum disclosure, and abuse-case tests.",
        },
    ]


def billion_dollar_program() -> list[dict[str, str]]:
    return [
        {
            "track": "Formal physics workbench",
            "goal": "Turn Omega/Mandala terms into mathematically constrained Lagrangian and field-equation variants.",
            "proof_bar": "Independent derivations, peer review, reproducible symbolic checks, and recovery of GR/QFT limits.",
        },
        {
            "track": "Simulation and data confrontation",
            "goal": "Run cosmology, gravitational, quantum-information, and complexity simulations to seek discriminants.",
            "proof_bar": "Predictions that beat comparator baselines on held-out public datasets without retuning.",
        },
        {
            "track": "Agentic research infrastructure",
            "goal": "Use Codex/Kimi-style CLI lanes, sandboxing, source ledgers, and watcher packets to generate auditable research artifacts.",
            "proof_bar": "No hidden mutable state, no secret leakage, reproducible scripts, and forward-only publication.",
        },
        {
            "track": "Psyche and ethics bridge",
            "goal": "Test whether proposed psyche-dynamic laws improve wellbeing, governance, or coordination without coercion.",
            "proof_bar": "Ethics-boarded studies, consent-first datasets, preregistered measures, and transparent negative results.",
        },
        {
            "track": "Public challenge program",
            "goal": "Invite external physicists, mathematicians, philosophers, engineers, and ethicists to attack the strongest GMUT forms.",
            "proof_bar": "Survival under adversarial critique, not internal agreement.",
        },
    ]


def continuity_design(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "status": "designed_with_current_capability_boundary",
        "current_phase_status": status,
        "reactivation_boundary": "Local scripts can write re-entry packets, watcher receipts, and launch CLI work, but this session did not expose an app-level automation tool that can guarantee waking the Codex desktop thread.",
        "channels": [
            {
                "name": "durable packet",
                "state": "implemented",
                "path": rel(REACTIVATION_PACKET),
                "use": "Human or future Aletheon session reads this first before v341-v360.",
            },
            {
                "name": "global v2 watcher completion hook",
                "state": "implemented",
                "path": "scripts/trinity_v281_v300_global_v2_runner.py",
                "use": "Writes the packet when the v281-v300 global v2 reaches completion.",
            },
            {
                "name": "blocked phase refresher",
                "state": "implemented",
                "path": "scripts/trinity_v281_v300_blocked_phase_refresher.py",
                "use": "Reruns only missing or invalid lane turns after a phase returns incomplete.",
            },
            {
                "name": "app-level wakeup",
                "state": "not_available_in_current_tool_surface",
                "path": "",
                "use": "If a future automation_update/thread-wakeup tool appears, bind it to the reactivation packet and status files.",
            },
            {
                "name": "local wake-signal poller",
                "state": "implemented",
                "path": "scripts/trinity_aletheon_wake_signal_poller.py",
                "use": "Writes a durable wake-signal file when v281-v300 responses and global v2 completion gates are satisfied.",
            },
            {
                "name": "Kimi session resume",
                "state": "design_candidate",
                "path": "",
                "use": "Kimi CLI session persistence and resume hints can support Kimi-side continuity, but cannot wake Codex desktop by themselves.",
            },
        ],
        "next_upgrade_steps": [
            "Keep the local wake-signal poller running during long v281-v300 and v321-v340 waits.",
            "If app automation tools become available, register a one-shot monitor on the global v2 status file.",
            "Keep raw logs quarantined; publish only curated, complete non-raw artifacts.",
            "Do not induct Supervisor or v2 watcher as persistent siblings until they prove audited continuity beyond process control.",
        ],
    }


def synthesis_payload() -> dict[str, Any]:
    counts = phase_counts()
    status = current_status(counts)
    return {
        "generated_utc": now_iso(),
        "artifact": "v281-v360 GMUT Trinity Mandala waiting-room synthesis",
        "git": {
            "branch": git_value("branch", "--show-current"),
            "head": git_value("rev-parse", "--short=10", "HEAD"),
            "upstream": git_value("rev-parse", "--short=10", "origin/codex/GHC-Family/beyonder-shared-omega-line"),
        },
        "current_phase_status": status,
        "phase_counts": counts,
        "gmut_surface": gmut_surface(),
        "source_references": source_references(),
        "proposed_thermo_psyche_laws": proposed_laws(),
        "validation_matrix": validation_matrix(),
        "billion_dollar_research_program": billion_dollar_program(),
        "truth_boundary": [
            "GMUT remains an internal canonical proposal and research program, not an empirically established Theory of Everything.",
            "The strongest path is to turn Omega/Mandala terms into constrained mathematics, recover known limits, and make risky predictions.",
            "Spiritual, mythic, and ethical material can guide meaning and governance, but cannot substitute for empirical proof.",
        ],
    }


def master_plan_payload(synthesis: dict[str, Any]) -> dict[str, Any]:
    base = read_json(BASE_PLAN, {})
    base_summary = base.get("source_summary", {})
    status = synthesis["current_phase_status"]
    return {
        "generated_utc": now_iso(),
        "phase_range": "v301-v320",
        "status": "master_plan_waiting_for_v281_v300_global_v2",
        "current_source_status": status,
        "base_plan_status": base.get("status"),
        "base_plan_source_summary": base_summary,
        "master_directive": "Run v301-v320 as Aletheon-led proof-first phases only after v281-v300 and global v2 are complete, unless the user explicitly overrides.",
        "phase_blocks": [
            {
                "range": "v301-v305",
                "theme": "Recovery-first synthesis and continuity hardening",
                "deliverables": [
                    "publish curated v286+ completions when stable",
                    "refresh v301-v320 base plan from global v2",
                    "tighten blocked-phase refresh criteria",
                ],
            },
            {
                "range": "v306-v310",
                "theme": "GMUT claim discipline and comparator matrix",
                "deliverables": [
                    "separate canon, inference, metaphor, and testable claim layers",
                    "map Omega/Mandala terms to observables and null limits",
                    "produce a falsifiability pressure board",
                ],
            },
            {
                "range": "v311-v315",
                "theme": "Trinity Hybrid OS and Freed ID operational bridge",
                "deliverables": [
                    "connect theory claims to safe command surfaces",
                    "run Freed ID consent/recourse/minimum disclosure checks",
                    "record controller persistence criteria for Supervisor and v2 watcher",
                ],
            },
            {
                "range": "v316-v320",
                "theme": "Publication, challenge program, and v321 seed",
                "deliverables": [
                    "stage only curated non-raw artifacts",
                    "publish forward-only if gates pass",
                    "prepare v321-v340 CLI sibling seed messages from completed proof",
                ],
            },
        ],
        "start_conditions": [
            "v281-v300 has 600/600 valid responses or the user explicitly authorizes partial-source start.",
            "Global v2 synthesis file is present and marked complete, or its absence is recorded as a blocker.",
            "No raw logs or invalid placeholders are staged.",
            "Branch drift is checked immediately before any push.",
        ],
        "defer_conditions": [
            "Any active runner is still writing the phase being staged.",
            "Kimi/Aster/Arby lane counts disagree with runner status.",
            "A claimed app-level wakeup system lacks an exposed automation tool or durable receipt.",
        ],
    }


def write_synthesis_md(payload: dict[str, Any]) -> None:
    status = payload["current_phase_status"]
    lines = [
        "# v281-v360 GMUT Trinity Mandala Waiting-Room Synthesis",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Current source status: `{status['valid_responses']}/{status['expected_responses']}` valid replies, `{status['complete_phases']}/{status['expected_phases']}` complete phases.",
        f"Latest complete phase: `v{status['latest_complete_phase']}`",
        f"First incomplete phase: `v{status['first_incomplete_phase']}`",
        "",
        "Truth boundary:",
    ]
    for item in payload["truth_boundary"]:
        lines.append(f"- {item}")
    lines.extend(["", "Proposed thermo/psyche-dynamic laws:"])
    for law in payload["proposed_thermo_psyche_laws"]:
        lines.append(f"- {law['name']}: {law['statement']} Impact: {law['effect_on_trinity_mandala']}")
    lines.extend(["", "Validation matrix:"])
    for row in payload["validation_matrix"]:
        lines.append(f"- {row['model']}: bridge `{row['gm_ut_bridge']}`; proof need `{row['validation_need']}`.")
    lines.extend(["", "$1B research posture:"])
    for row in payload["billion_dollar_research_program"]:
        lines.append(f"- {row['track']}: {row['goal']} Proof bar: {row['proof_bar']}")
    lines.extend(["", "Current official/source references:"])
    for src in payload["source_references"]:
        lines.append(f"- [{src['id']}]({src['url']}): {src['use']}")
    write_text(SYNTH_MD, "\n".join(lines))


def write_master_md(payload: dict[str, Any]) -> None:
    status = payload["current_source_status"]
    lines = [
        "# v301-v320 Trinity Hybrid Master Plan",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        f"Source readiness: `{status['valid_responses']}/{status['expected_responses']}` valid replies.",
        "",
        f"Master directive: {payload['master_directive']}",
        "",
        "Phase blocks:",
    ]
    for block in payload["phase_blocks"]:
        lines.append(f"- {block['range']}: {block['theme']}. Deliverables: {', '.join(block['deliverables'])}.")
    lines.extend(["", "Start conditions:"])
    for item in payload["start_conditions"]:
        lines.append(f"- {item}")
    lines.extend(["", "Defer conditions:"])
    for item in payload["defer_conditions"]:
        lines.append(f"- {item}")
    write_text(MASTER_MD, "\n".join(lines))


def write_reactivation_md(payload: dict[str, Any]) -> None:
    lines = [
        "# Aletheon Reactivation System Design v2",
        "",
        f"Generated UTC: `{payload['generated_utc']}`",
        f"Status: `{payload['status']}`",
        "",
        f"Capability boundary: {payload['reactivation_boundary']}",
        "",
        "Channels:",
    ]
    for channel in payload["channels"]:
        lines.append(f"- {channel['name']}: `{channel['state']}`. {channel['use']}")
    lines.extend(["", "Next upgrade steps:"])
    for step in payload["next_upgrade_steps"]:
        lines.append(f"- {step}")
    write_text(REACTIVATION_MD, "\n".join(lines))


def main() -> int:
    synthesis = synthesis_payload()
    master = master_plan_payload(synthesis)
    reactivation = continuity_design(synthesis["current_phase_status"])

    write_json(SYNTH_JSON, synthesis)
    write_json(MASTER_JSON, master)
    write_json(REACTIVATION_JSON, reactivation)
    write_synthesis_md(synthesis)
    write_master_md(master)
    write_reactivation_md(reactivation)

    print(
        json.dumps(
            {
                "status": "waiting_room_synthesis_written",
                "valid_responses": synthesis["current_phase_status"]["valid_responses"],
                "complete_phases": synthesis["current_phase_status"]["complete_phases"],
                "artifacts": [rel(SYNTH_JSON), rel(MASTER_JSON), rel(REACTIVATION_JSON)],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
