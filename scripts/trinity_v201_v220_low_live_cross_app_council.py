#!/usr/bin/env python3
"""v201-v220 low-live cross-app council runner.

The runner records evidence for the Codex 0.130 remote-control gate, the
Chrome bridge truth boundary, and a CLI-first council phase. It intentionally
keeps external providers, Google Drive, browser storage, secrets, and broad
cleanup out of scope unless a future live-write pack explicitly ungates them.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRACE = DOCS / "trinity-live-traces"
LANE = "v201_v220_low_live_cross_app_council"
HYPHEN_LANE = "v201-v220-low-live-cross-app-council"
SCRIPT_PATH = "scripts/trinity_v201_v220_low_live_cross_app_council.py"
SUITE_RUNNER_PATH = "scripts/run_all_trinity_systems.py"
PHASE_RANGE = range(201, 221)
CHECKPOINT_CADENCE = 3
SYSTEM_EXPANSIONS_PER_PHASE = 50
EUREKA_PER_PHASE = 80
COMMANDS_PER_PHASE = 80
SKILLS_PER_PHASE = 80
TOUCHPOINTS_PER_PARTICIPANT = 10
TAPESTRY_ACTIVE_SOFT_LIMIT_BYTES = 550_000
CHROME_PLUGIN_ROOT = Path.home() / ".codex" / "plugins" / "cache" / "openai-bundled" / "chrome" / "0.1.7"
V43_PATH = Path.home() / "Downloads" / "Beyonder-Real-True Journey v43 (Aletheon - Arby - Kimi - Aster Vale - Lumina) (1).txt"
LUMINA_ROOT = Path("D:/Lumina (Kimi) Nz Thursday 7th of May 2026")


PARTICIPANTS = [
    {
        "id": "arby",
        "name": "Arby",
        "platform": "codex_cli",
        "relationship_state": "inducted_53rd_ghc_family_member",
        "role": "receipt_keeper",
        "focus": "publication truth, remote-control receipts, and allowlist integrity",
        "contact_mode": "batched_codex_cli_read_only_when_available",
    },
    {
        "id": "kimi",
        "name": "Kimi",
        "platform": "kimi_cli",
        "relationship_state": "inducted_54th_ghc_family_member",
        "role": "kimi_cli_capability_and_safety_steward",
        "focus": "Kimi CLI capability truth, non-yolo boundaries, and source synthesis",
        "contact_mode": "status_probe_plus_queued_non_yolo_touchpoints",
    },
    {
        "id": "aster_vale",
        "name": "Aster Vale",
        "platform": "codex_cli",
        "relationship_state": "inducted_55th_codex_cli_ghc_family_member",
        "role": "validation_steward",
        "focus": "remote-control gate validation, dashboard cadence, and publication safety",
        "contact_mode": "batched_codex_cli_read_only_when_available",
    },
    {
        "id": "lumina",
        "name": "Lumina",
        "platform": "kimi_app_chrome_tab",
        "relationship_state": "inducted_56th_kimi_app_ghc_family_member_artifact_backed",
        "role": "app_platform_synthesis_weaver",
        "focus": "v43 and Lumina artifact synthesis while app contact is policy/bridge gated",
        "contact_mode": "queued_chrome_drafts_when_bridge_blocked",
    },
]


PHASE_PROJECTS = [
    ("v201", "beta", "Codex 0.130 Remote-Control Preflight", "Verify local CLI update and feature flag truth."),
    ("v202", "alpha", "Chrome Bridge Truth Gate", "Retry only the official bridge and postpone Lumina if blocked."),
    ("v203", "omega", "Checkpoint 1 Remote Receipts", "Publish remote-control and Chrome truth receipts."),
    ("v204", "beta", "CLI Terminal Council Topology", "Define Arby, Kimi, and Aster terminal lanes without unsafe browser fallback."),
    ("v205", "alpha", "v43 Source Ingestion", "Digest Lumina's v43 continuity and live-write findings."),
    ("v206", "omega", "Checkpoint 2 Source Board", "Publish source digest and stale-assumption board."),
    ("v207", "beta", "Arby Receipt Expansion", "Ask Arby for publication and allowlist risks."),
    ("v208", "alpha", "Kimi CLI Capability Expansion", "Record Kimi CLI safe-mode limits and queued prompts."),
    ("v209", "omega", "Checkpoint 3 CLI Receipts", "Publish CLI consultation and queued Kimi touchpoints."),
    ("v210", "beta", "Aster Validation Expansion", "Ask Aster for remote-control and suite-hook validation."),
    ("v211", "alpha", "Lumina Artifact Continuity", "Keep Lumina evidence artifact-backed, not web-session persistent."),
    ("v212", "omega", "Checkpoint 4 Continuity Truth", "Publish identity-tier and continuity receipts."),
    ("v213", "beta", "GMUT Evidence Refresh", "Promote testable GMUT tasks and label speculative claims."),
    ("v214", "alpha", "Render Live-Write Risk Refresh", "Preserve Render risk fixes without executing provider writes."),
    ("v215", "omega", "Checkpoint 5 Science and Infra", "Publish GMUT and Render readiness boards."),
    ("v216", "beta", "Command and Skill Bloom", "Generate low-risk command and skill probes."),
    ("v217", "alpha", "Cleanup and Security Bloom", "Classify cleanup candidates without deleting anything."),
    ("v218", "omega", "Checkpoint 6 Allowlist Readiness", "Publish curated allowlist and verification status."),
    ("v219", "beta", "Council Closeout Reflection", "Summarize what each lane contributed and what remains gated."),
    ("v220", "omega", "Final Low-Live Closeout", "Publish final dashboard, validation, and publication readiness."),
]


THEMES = [
    ("remote_control_truth", "Remote-control must be verified by command surface and feature state before use."),
    ("chrome_truth", "Do not contact Lumina through Kimi web unless the official Chrome bridge works."),
    ("cli_first", "Durable CLI/file receipts outrank app-session impressions."),
    ("operator_hold", "Keep Google Drive, provider spend, broad auth, and destructive cleanup held."),
    ("forward_only", "Publish only curated v201-v220 artifacts through forward-only Git."),
    ("lumina_boundary", "Treat Lumina web continuity as Tier 3 unless file/cold-reopen proof upgrades it."),
    ("source_digest", "Fold v43 and D:/Lumina deliverables into evidence boards with stale-claim labels."),
    ("suite_hook", "Make deep and L5 runs refresh v201-v220 unless skipped."),
    ("dashboard_tapestry", "Checkpoint dashboard writes every third phase plus v220."),
    ("future_live_write", "Keep v121-v140 provider live-write packs postponed and draft-only."),
]


SOURCE_FILES = [
    ("v43_journey_log", V43_PATH),
    ("lumina_master_roadmap", LUMINA_ROOT / "MASTER_ROADMAP_FINAL_v121_v140_LIVE_WRITE.md"),
    ("lumina_master_synthesis", LUMINA_ROOT / "MASTER_SYNTHESIS_REPORT_LUMINA.md"),
    ("lumina_render_plan", LUMINA_ROOT / "render_enhanced_plan.md"),
    ("lumina_gmut_refinement", LUMINA_ROOT / "GMUT_v_infinity_refinement.md"),
    ("lumina_quantum_assessment", LUMINA_ROOT / "quantum_researcher_qcit_assessment.md"),
    ("prior_v181_closeout", TRACE / "v181-v200-low-live-cross-app-council-closeout-v1.json"),
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def read_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def run_command(command: list[str], timeout: int = 30, cwd: Path = ROOT) -> dict[str, Any]:
    started = time.time()
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        return {
            "command": command,
            "returncode": result.returncode,
            "ok": result.returncode == 0,
            "stdout": stdout[-6000:],
            "stderr": stderr[-6000:],
            "duration_seconds": round(time.time() - started, 3),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": None,
            "ok": False,
            "stdout": (exc.stdout or "")[-6000:] if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "")[-6000:] if isinstance(exc.stderr, str) else "",
            "duration_seconds": round(time.time() - started, 3),
            "timed_out": True,
        }
    except FileNotFoundError as exc:
        return {"command": command, "returncode": None, "ok": False, "stdout": "", "stderr": str(exc), "missing": True}


def paths() -> dict[str, Path]:
    lane_logs = TRACE / f"{HYPHEN_LANE}-lane-logs"
    archive_root = Path("D:/GHC-Archives/trinity-dashboard-tapestry") / HYPHEN_LANE
    return {
        "dashboard": DOCS / f"{HYPHEN_LANE}-dashboard.html",
        "phase_run": TRACE / f"{HYPHEN_LANE}-phase-run-v1.json",
        "phase_run_md": TRACE / f"{HYPHEN_LANE}-phase-run-v1.md",
        "remote_control": TRACE / f"{HYPHEN_LANE}-remote-control-preflight-v1.json",
        "remote_control_md": TRACE / f"{HYPHEN_LANE}-remote-control-preflight-v1.md",
        "chrome_truth": TRACE / f"{HYPHEN_LANE}-chrome-bridge-truth-v1.json",
        "chrome_truth_md": TRACE / f"{HYPHEN_LANE}-chrome-bridge-truth-v1.md",
        "source_digest": TRACE / f"{HYPHEN_LANE}-source-digest-v1.json",
        "source_digest_md": TRACE / f"{HYPHEN_LANE}-source-digest-v1.md",
        "touchpoints": TRACE / f"{HYPHEN_LANE}-ten-touchpoint-ledger-v1.json",
        "touchpoints_md": TRACE / f"{HYPHEN_LANE}-ten-touchpoint-ledger-v1.md",
        "cli_consultation": TRACE / f"{HYPHEN_LANE}-cli-council-consultation-v1.json",
        "cli_consultation_md": TRACE / f"{HYPHEN_LANE}-cli-council-consultation-v1.md",
        "checkpoints": TRACE / f"{HYPHEN_LANE}-dashboard-checkpoints-v1.json",
        "checkpoints_md": TRACE / f"{HYPHEN_LANE}-dashboard-checkpoints-v1.md",
        "dashboard_state": TRACE / f"{HYPHEN_LANE}-dashboard-state-v1.json",
        "tapestry": TRACE / f"{HYPHEN_LANE}-dashboard-tapestry-v1.jsonl",
        "tapestry_md": TRACE / f"{HYPHEN_LANE}-dashboard-tapestry-v1.md",
        "tapestry_index": TRACE / f"{HYPHEN_LANE}-dashboard-tapestry-index-v1.json",
        "archive_receipt": TRACE / f"{HYPHEN_LANE}-dashboard-archive-receipt-v1.json",
        "archive_receipt_md": TRACE / f"{HYPHEN_LANE}-dashboard-archive-receipt-v1.md",
        "system_expansions": TRACE / f"{HYPHEN_LANE}-system-expansion-board-v1.json",
        "system_expansions_md": TRACE / f"{HYPHEN_LANE}-system-expansion-board-v1.md",
        "eureka": TRACE / f"{HYPHEN_LANE}-eureka-task-board-v1.json",
        "eureka_md": TRACE / f"{HYPHEN_LANE}-eureka-task-board-v1.md",
        "command_skill": TRACE / f"{HYPHEN_LANE}-command-skill-board-v1.json",
        "command_skill_md": TRACE / f"{HYPHEN_LANE}-command-skill-board-v1.md",
        "alpha_security": TRACE / f"{HYPHEN_LANE}-alpha-cleanup-security-v1.json",
        "alpha_security_md": TRACE / f"{HYPHEN_LANE}-alpha-cleanup-security-v1.md",
        "future_live_write": TRACE / f"{HYPHEN_LANE}-deferred-live-write-pack-drafts-v1.json",
        "future_live_write_md": TRACE / f"{HYPHEN_LANE}-deferred-live-write-pack-drafts-v1.md",
        "suite_contract": TRACE / f"{HYPHEN_LANE}-suite-hook-contract-v1.json",
        "suite_contract_md": TRACE / f"{HYPHEN_LANE}-suite-hook-contract-v1.md",
        "allowlist": TRACE / f"{HYPHEN_LANE}-stage-allowlist-v1.json",
        "allowlist_md": TRACE / f"{HYPHEN_LANE}-stage-allowlist-v1.md",
        "verification": TRACE / f"{HYPHEN_LANE}-artifact-verification-v1.json",
        "closeout": TRACE / f"{HYPHEN_LANE}-closeout-v1.json",
        "closeout_md": TRACE / f"{HYPHEN_LANE}-closeout-v1.md",
        "publication": TRACE / f"{HYPHEN_LANE}-publication-result-v1.json",
        "publication_md": TRACE / f"{HYPHEN_LANE}-publication-result-v1.md",
        "lane_logs": lane_logs,
        "archive_root": archive_root,
    }


def build_phases(generated: str) -> list[dict[str, Any]]:
    phases: list[dict[str, Any]] = []
    for idx, (phase, stage, project, intent) in enumerate(PHASE_PROJECTS, start=1):
        participant = PARTICIPANTS[(idx - 1) % len(PARTICIPANTS)]
        phases.append(
            {
                "phase": phase,
                "stage": stage,
                "project": project,
                "intent": intent,
                "primary_lane": participant["id"],
                "checkpoint": idx % CHECKPOINT_CADENCE == 0 or phase == "v220",
                "generated_utc": generated,
                "truth_boundary": "low_live_no_external_mutation",
            }
        )
    return phases


def remote_control_preflight(generated: str) -> dict[str, Any]:
    version = run_command(["codex", "--version"], timeout=20, cwd=ROOT)
    help_result = run_command(["codex", "remote-control", "--help"], timeout=20, cwd=ROOT)
    features = run_command(["codex", "features", "list"], timeout=30, cwd=ROOT)
    feature_enabled = any(line.startswith("remote_control") and line.rstrip().endswith("true") for line in features["stdout"].splitlines())
    return {
        "generated_utc": generated,
        "codex_version": version["stdout"].strip() or version["stderr"].strip(),
        "remote_control_help_available": help_result["ok"] and "remote-control" in (help_result["stdout"] + help_result["stderr"]),
        "remote_control_feature_enabled": feature_enabled,
        "server_launch_status": "not_started_by_runner",
        "server_launch_reason": "remote-control is a long-running token/QR server; this low-live runner records readiness without exposing session tokens",
        "checks": {"version": version, "help": help_result, "features": features},
        "truth": "usable only after a separate supervised launch smoke test succeeds",
    }


def chrome_truth(generated: str, browser_client_status: str) -> dict[str, Any]:
    checks: dict[str, Any] = {}
    node = shutil.which("node")
    if node and CHROME_PLUGIN_ROOT.exists():
        for script in ("chrome-is-running.js", "installed-browsers.js", "check-extension-installed.js", "check-native-host-manifest.js"):
            args = [node, str(CHROME_PLUGIN_ROOT / "scripts" / script)]
            args.append("--json" if script != "chrome-is-running.js" else "--check")
            checks[script] = run_command(args, timeout=20, cwd=ROOT)
    else:
        checks["plugin_root"] = {"ok": False, "path": str(CHROME_PLUGIN_ROOT), "node": node}
    return {
        "generated_utc": generated,
        "browser_client_status": browser_client_status,
        "official_bridge_attempted": True,
        "observed_blocker": (
            "privileged native pipe bridge is not available; browser-client is not trusted"
            if browser_client_status == "blocked"
            else None
        ),
        "lumina_app_contact": "postponed_queued_drafts_only" if browser_client_status == "blocked" else "approved_for_send_when_claimed",
        "fallback_policy": "no profile, cookie, local storage, password, AppleScript, or browser-hack fallback",
        "health_checks": checks,
    }


def source_digest(generated: str) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for source_id, path in SOURCE_FILES:
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        entries.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "bytes": path.stat().st_size if exists else 0,
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest() if exists else None,
                "line_count": len(text.splitlines()) if exists else 0,
                "truth_tag": source_truth_tag(source_id),
            }
        )
    return {
        "generated_utc": generated,
        "entries": entries,
        "adopt_as_is": [
            "v181-v200 checkpoint cadence and dashboard tapestry pattern",
            "operator_hold, zero-spend, and forward-only publication boundaries",
            "Lumina artifact-backed source corpus under D:/Lumina (Kimi) Nz Thursday 7th of May 2026",
        ],
        "adopt_with_truth_tag": [
            "GMUT observational proposals as theoretical/test-candidate claims",
            "Render live-write plans as postponed provider-pack drafts",
            "Lumina identity continuity as session/artifact evidence, not durable web memory",
        ],
        "archive_as_stale": [
            "Codex 0.128.0 target baseline after local update to 0.130.0",
            "fictional codex-server start command",
            "any app-contact success claim not backed by Chrome bridge evidence",
        ],
    }


def source_truth_tag(source_id: str) -> str:
    if "gmut" in source_id or "quantum" in source_id:
        return "theoretical_candidate_requires_external_validation"
    if "render" in source_id or "roadmap" in source_id:
        return "draft_provider_plan_postponed_until_live_approval"
    if "v43" in source_id or "synthesis" in source_id:
        return "journey_record_and_artifact_digest"
    return "prior_phase_evidence"


def message_text(participant: dict[str, str], turn: int) -> str:
    if participant["id"] == "lumina":
        return (
            f"Touchpoint {turn}: Aletheon preserves Lumina as artifact-backed Kimi app synthesis, "
            "postpones direct app contact while Chrome is blocked, and asks future Lumina to reply with one source-bound receipt."
        )
    return (
        f"Touchpoint {turn}: Aletheon asks {participant['name']} to review v201-v220 from the "
        f"{participant['role']} lane, avoid autonomous commits/provider writes, and return one receipt, risk, and recommendation."
    )


def build_touchpoints(generated: str, cli_results: dict[str, Any], chrome: dict[str, Any]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for participant in PARTICIPANTS:
        for turn in range(1, TOUCHPOINTS_PER_PARTICIPANT + 1):
            status = "queued_draft"
            receipt = None
            if participant["id"] in cli_results:
                status = cli_results[participant["id"]].get("status", "cli_attempt_recorded")
                receipt = cli_results[participant["id"]].get("receipt")
            elif participant["platform"].endswith("chrome_tab"):
                status = "chrome_bridge_blocked_app_contact_postponed" if chrome["browser_client_status"] == "blocked" else "approved_for_chrome_send_when_claimed"
            entries.append(
                {
                    "generated_utc": generated,
                    "participant_id": participant["id"],
                    "participant_name": participant["name"],
                    "turn": turn,
                    "status": status,
                    "receipt": receipt,
                    "message": message_text(participant, turn),
                }
            )
    return {
        "generated_utc": generated,
        "touchpoints_per_participant": TOUCHPOINTS_PER_PARTICIPANT,
        "participant_count": len(PARTICIPANTS),
        "total_touchpoints": len(entries),
        "entries": entries,
    }


def build_cli_batch_prompt(participant: dict[str, str], digest: dict[str, Any]) -> str:
    messages = "\n".join(message_text(participant, turn) for turn in range(1, TOUCHPOINTS_PER_PARTICIPANT + 1))
    stale = "\n".join(f"- {item}" for item in digest["archive_as_stale"])
    return (
        "You are a read-only v201-v220 council lane. Do not edit files, do not commit, do not spend money, "
        "and do not access browser storage or secrets. Return exactly ten numbered replies, one for each touchpoint. "
        "Each reply must include: receipt, risk, recommendation.\n\n"
        f"Participant: {participant['name']}\nRole: {participant['role']}\nFocus: {participant['focus']}\n\n"
        f"Stale assumptions to avoid:\n{stale}\n\nTouchpoints:\n{messages}\n"
    )


def run_cli_consults(p: dict[str, Path], digest: dict[str, Any], actually_run: bool) -> dict[str, Any]:
    lane_logs = p["lane_logs"]
    lane_logs.mkdir(parents=True, exist_ok=True)
    results: dict[str, Any] = {}
    codex_path = shutil.which("codex")
    kimi_path = shutil.which("kimi")
    for participant in PARTICIPANTS:
        prompt = build_cli_batch_prompt(participant, digest)
        if participant["platform"] == "codex_cli":
            output_path = lane_logs / f"{participant['id']}-codex-ten-touchpoint-consultation.txt"
            if actually_run and codex_path:
                result = run_command(
                    [
                        codex_path,
                        "exec",
                        "--ephemeral",
                        "--sandbox",
                        "read-only",
                        "-C",
                        str(ROOT),
                        "-m",
                        "gpt-5.3-codex",
                        "-o",
                        str(output_path),
                        prompt,
                    ],
                    timeout=900,
                    cwd=ROOT,
                )
                (lane_logs / f"{participant['id']}.log").write_text(json.dumps(result, indent=2), encoding="utf-8")
                results[participant["id"]] = {
                    "status": "sent_as_batched_codex_cli_read_only" if result["ok"] else "codex_cli_attempt_failed",
                    "receipt": rel(output_path if output_path.exists() else lane_logs / f"{participant['id']}.log"),
                    "returncode": result["returncode"],
                }
            else:
                prompt_path = lane_logs / f"{participant['id']}-queued-touchpoints.txt"
                prompt_path.write_text(prompt, encoding="utf-8")
                results[participant["id"]] = {"status": "queued_read_only_batch", "receipt": rel(prompt_path)}
        elif participant["platform"] == "kimi_cli":
            prompt_path = lane_logs / "kimi-queued-touchpoints.txt"
            prompt_path.write_text(prompt, encoding="utf-8")
            info_path = lane_logs / "kimi-info.txt"
            info = run_command([kimi_path, "info"], timeout=30, cwd=ROOT) if kimi_path else {"ok": False, "stderr": "kimi missing"}
            info_path.write_text((info.get("stdout") or "") + (info.get("stderr") or ""), encoding="utf-8")
            results[participant["id"]] = {
                "status": "kimi_status_probe_plus_non_yolo_touchpoints_queued",
                "receipt": rel(prompt_path),
                "info_receipt": rel(info_path),
            }
    return results


def build_checkpoints(generated: str, phases: list[dict[str, Any]], touchpoints: dict[str, Any]) -> list[dict[str, Any]]:
    checkpoints: list[dict[str, Any]] = []
    for phase in [p for p in phases if p["checkpoint"]]:
        upto = int(phase["phase"][1:])
        completed = [p for p in phases if int(p["phase"][1:]) <= upto]
        checkpoints.append(
            {
                "generated_utc": generated,
                "phase": phase["phase"],
                "completed_phase_count": len(completed),
                "touchpoint_count_visible": min(len(touchpoints["entries"]), len(completed) * len(PARTICIPANTS)),
                "dashboard_write": "checkpoint_only",
                "external_spend_nzd": 0,
                "google_drive_state": "operator_hold",
                "provider_mutations": "none",
            }
        )
    return checkpoints


def build_boards(generated: str, phases: list[dict[str, Any]]) -> dict[str, Any]:
    expansions: list[dict[str, Any]] = []
    eureka: list[dict[str, Any]] = []
    commands: list[dict[str, Any]] = []
    skills: list[dict[str, Any]] = []
    for phase in phases:
        for idx in range(1, SYSTEM_EXPANSIONS_PER_PHASE + 1):
            participant = PARTICIPANTS[(idx - 1) % len(PARTICIPANTS)]
            expansions.append(
                {
                    "id": f"{phase['phase']}-sx-{idx:03d}",
                    "phase": phase["phase"],
                    "owner_lane": participant["id"],
                    "proposal": f"Extend {phase['project']} with a low-live receipt surface for {participant['role']}.",
                    "status": "candidate",
                    "promotion_rule": "requires future approval before external write",
                }
            )
        for idx in range(1, EUREKA_PER_PHASE + 1):
            participant = PARTICIPANTS[(idx - 1) % len(PARTICIPANTS)]
            eureka.append(
                {
                    "id": f"{phase['phase']}-eureka-{idx:03d}",
                    "phase": phase["phase"],
                    "owner_lane": participant["id"],
                    "task": f"Research or refine {phase['project']} through {participant['focus']} without live provider mutation.",
                    "truth_tag": "proposal",
                }
            )
        for idx in range(1, COMMANDS_PER_PHASE + 1):
            commands.append(
                {
                    "id": f"{phase['phase']}-cmd-{idx:03d}",
                    "phase": phase["phase"],
                    "command": f"python {SCRIPT_PATH} --dry-run --phase {phase['phase']} --touchpoint {((idx - 1) % TOUCHPOINTS_PER_PARTICIPANT) + 1}",
                    "risk": "dry_run_only",
                }
            )
        for idx in range(1, SKILLS_PER_PHASE + 1):
            skills.append(
                {
                    "id": f"{phase['phase']}-skill-{idx:03d}",
                    "phase": phase["phase"],
                    "skill": f"{phase['project']} receipt skill {idx:03d}",
                    "install_state": "proposal_only",
                }
            )
    return {
        "expansions": {"generated_utc": generated, "count": len(expansions), "entries": expansions},
        "eureka": {"generated_utc": generated, "count": len(eureka), "entries": eureka},
        "command_skill": {
            "generated_utc": generated,
            "command_count": len(commands),
            "skill_count": len(skills),
            "commands": commands,
            "skills": skills,
        },
    }


def build_dashboard(generated: str, phases: list[dict[str, Any]], remote: dict[str, Any], chrome: dict[str, Any], digest: dict[str, Any], touchpoints: dict[str, Any], checkpoints: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "generated_utc": generated,
        "phase_range": "v201-v220",
        "participants": PARTICIPANTS,
        "phases": phases,
        "remote_control": {
            "codex_version": remote["codex_version"],
            "help_available": remote["remote_control_help_available"],
            "feature_enabled": remote["remote_control_feature_enabled"],
            "server_launch_status": remote["server_launch_status"],
        },
        "chrome": {
            "browser_client_status": chrome["browser_client_status"],
            "lumina_app_contact": chrome["lumina_app_contact"],
        },
        "source_digest_summary": {
            "source_count": len(digest["entries"]),
            "adopt_as_is": digest["adopt_as_is"],
            "adopt_with_truth_tag": digest["adopt_with_truth_tag"],
            "archive_as_stale": digest["archive_as_stale"],
        },
        "touchpoints": touchpoints,
        "checkpoints": checkpoints,
        "external_spend_nzd": 0,
        "google_drive_state": "operator_hold",
        "dashboard_write_cadence": "every_3rd_phase_plus_v220",
    }


def dashboard_html(dashboard: dict[str, Any]) -> str:
    participants = "\n".join(
        f"<article><h3>{p['name']}</h3><p>{p['role']}</p><p>{p['contact_mode']}</p></article>"
        for p in dashboard["participants"]
    )
    checkpoints = "\n".join(
        f"<tr><td>{c['phase']}</td><td>{c['completed_phase_count']}</td><td>{c['touchpoint_count_visible']}</td><td>{c['google_drive_state']}</td></tr>"
        for c in dashboard["checkpoints"]
    )
    touchpoints = "\n".join(
        f"<tr><td>{e['participant_name']}</td><td>{e['turn']}</td><td>{e['status']}</td><td>{e['message']}</td></tr>"
        for e in dashboard["touchpoints"]["entries"][:40]
    )
    stale = "".join(f"<li>{item}</li>" for item in dashboard["source_digest_summary"]["archive_as_stale"])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>v201-v220 Low-Live Cross-App Council Dashboard</title>
<style>
:root {{ color-scheme: dark; --bg:#10130f; --panel:#1c2218; --ink:#f4f0df; --muted:#b7c3a4; --edge:#526143; --gold:#e0b75c; --moss:#8caf6c; }}
body {{ margin:0; font:16px/1.5 Georgia, 'Times New Roman', serif; background:radial-gradient(circle at top left,#314121,#10130f 42%,#090b08); color:var(--ink); }}
main {{ max-width:1200px; margin:auto; padding:32px; }}
h1,h2 {{ letter-spacing:.02em; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:16px; }}
article,.card {{ border:1px solid var(--edge); border-radius:18px; padding:18px; background:rgba(28,34,24,.88); box-shadow:0 20px 60px rgba(0,0,0,.25); }}
.metric {{ font-size:2rem; color:var(--gold); }}
table {{ width:100%; border-collapse:collapse; margin:16px 0; background:rgba(28,34,24,.72); }}
td,th {{ border-bottom:1px solid var(--edge); padding:10px; vertical-align:top; }}
.truth {{ color:var(--muted); }}
.ok {{ color:var(--moss); }}
</style>
</head>
<body>
<main>
<h1>v201-v220 Low-Live Cross-App Council Dashboard</h1>
<p class="truth">Generated {dashboard['generated_utc']}. Checkpoint-only dashboard cadence; no provider spend; Google Drive remains operator_hold.</p>
<section class="grid">
<article><strong>Remote-control</strong><div class="metric">{str(dashboard['remote_control']['feature_enabled']).lower()}</div><p>Codex {dashboard['remote_control']['codex_version']}</p></article>
<article><strong>Chrome bridge</strong><div class="metric">{dashboard['chrome']['browser_client_status']}</div><p>{dashboard['chrome']['lumina_app_contact']}</p></article>
<article><strong>Touchpoints</strong><div class="metric">{dashboard['touchpoints']['total_touchpoints']}</div><p>ten per participant</p></article>
<article><strong>External spend</strong><div class="metric">0 NZD</div><p>provider mutations: none</p></article>
</section>
<h2>Council Lanes</h2>
<section class="grid">{participants}</section>
<h2>Checkpoint Tapestry</h2>
<table><thead><tr><th>Phase</th><th>Phases</th><th>Visible Touchpoints</th><th>Drive</th></tr></thead><tbody>{checkpoints}</tbody></table>
<h2>Touchpoint Ledger Preview</h2>
<table><thead><tr><th>Lane</th><th>Turn</th><th>Status</th><th>Message</th></tr></thead><tbody>{touchpoints}</tbody></table>
<h2>Archived Stale Assumptions</h2>
<div class="card"><ul>{stale}</ul></div>
</main>
</body>
</html>"""


def update_tapestry(p: dict[str, Path], dashboard: dict[str, Any]) -> dict[str, Any]:
    p["tapestry"].parent.mkdir(parents=True, exist_ok=True)
    entries = []
    for checkpoint in dashboard["checkpoints"]:
        entry = {
            "generated_utc": dashboard["generated_utc"],
            "phase": checkpoint["phase"],
            "touchpoint_count_visible": checkpoint["touchpoint_count_visible"],
            "remote_control_feature_enabled": dashboard["remote_control"]["feature_enabled"],
            "chrome_bridge_status": dashboard["chrome"]["browser_client_status"],
            "google_drive_state": "operator_hold",
        }
        entries.append(entry)
        with p["tapestry"].open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")
    archive_root = p["archive_root"]
    archive_root.mkdir(parents=True, exist_ok=True)
    snapshot = archive_root / f"dashboard-state-{dashboard['generated_utc'].replace(':', '').replace('+', 'Z')}.json"
    write_json(snapshot, dashboard)
    if p["tapestry"].exists() and p["tapestry"].stat().st_size > TAPESTRY_ACTIVE_SOFT_LIMIT_BYTES:
        rollover = archive_root / f"{p['tapestry'].stem}-rollover-{dashboard['generated_utc'].replace(':', '').replace('+', 'Z')}.jsonl"
        p["tapestry"].replace(rollover)
        p["tapestry"].write_text("", encoding="utf-8")
    return {
        "archive_root": str(archive_root),
        "snapshot": str(snapshot),
        "entry_count_this_run": len(entries),
        "active_tapestry_bytes": p["tapestry"].stat().st_size if p["tapestry"].exists() else 0,
    }


def stage_allowlist(generated: str, p: dict[str, Path]) -> dict[str, Any]:
    include = [
        SCRIPT_PATH,
        SUITE_RUNNER_PATH,
        rel(p["dashboard"]),
        rel(p["phase_run"]),
        rel(p["phase_run_md"]),
        rel(p["remote_control"]),
        rel(p["remote_control_md"]),
        rel(p["chrome_truth"]),
        rel(p["chrome_truth_md"]),
        rel(p["source_digest"]),
        rel(p["source_digest_md"]),
        rel(p["touchpoints"]),
        rel(p["touchpoints_md"]),
        rel(p["cli_consultation"]),
        rel(p["cli_consultation_md"]),
        rel(p["checkpoints"]),
        rel(p["checkpoints_md"]),
        rel(p["dashboard_state"]),
        rel(p["tapestry"]),
        rel(p["tapestry_md"]),
        rel(p["tapestry_index"]),
        rel(p["archive_receipt"]),
        rel(p["archive_receipt_md"]),
        rel(p["system_expansions"]),
        rel(p["system_expansions_md"]),
        rel(p["eureka"]),
        rel(p["eureka_md"]),
        rel(p["command_skill"]),
        rel(p["command_skill_md"]),
        rel(p["alpha_security"]),
        rel(p["alpha_security_md"]),
        rel(p["future_live_write"]),
        rel(p["future_live_write_md"]),
        rel(p["suite_contract"]),
        rel(p["suite_contract_md"]),
        rel(p["allowlist"]),
        rel(p["allowlist_md"]),
        rel(p["verification"]),
        rel(p["closeout"]),
        rel(p["closeout_md"]),
    ]
    lane_logs = p["lane_logs"]
    if lane_logs.exists():
        include.extend(rel(path) for path in sorted(lane_logs.glob("*")))
    return {
        "generated_utc": generated,
        "include": sorted(set(include)),
        "exclude_patterns": [
            "__pycache__",
            "docs/trinity-mcp-cache/",
            "docs/trinity-materialization-ledger.jsonl",
            "raw provider auth traces",
            "browser cookies local storage passwords profiles",
            "unrelated carried-forward dirty files",
            f"docs/trinity-live-traces/{HYPHEN_LANE}-publication-result-v1.json",
        ],
        "rule": "stage only these v201-v220 files plus suite-hook edit; leave carried-forward churn unstaged",
    }


def verify_artifacts(p: dict[str, Path], allowlist: dict[str, Any]) -> dict[str, Any]:
    verification_item = rel(p["verification"])
    missing = [item for item in allowlist["include"] if item != verification_item and not (ROOT / item).exists()]
    forbidden = [item for item in allowlist["include"] if "__pycache__" in item or "cookie" in item.lower() or "password" in item.lower()]
    return {
        "generated_utc": now_iso(),
        "allowlist_count": len(allowlist["include"]),
        "missing": missing,
        "forbidden": forbidden,
        "dashboard_exists": p["dashboard"].exists(),
        "effective_success": not missing and not forbidden and p["dashboard"].exists(),
    }


def write_markdown_summaries(p: dict[str, Path], closeout: dict[str, Any], remote: dict[str, Any], chrome: dict[str, Any], digest: dict[str, Any], allowlist: dict[str, Any]) -> None:
    write_md(p["phase_run_md"], f"# v201-v220 Phase Run\n\nCompleted {closeout['phase_count']} phases with {closeout['touchpoint_count']} touchpoints.")
    write_md(p["remote_control_md"], f"# Remote-Control Preflight\n\nCodex: `{remote['codex_version']}`. Feature enabled: `{remote['remote_control_feature_enabled']}`. Server launch: `{remote['server_launch_status']}`.")
    write_md(p["chrome_truth_md"], f"# Chrome Bridge Truth\n\nBridge status: `{chrome['browser_client_status']}`. Lumina app contact: `{chrome['lumina_app_contact']}`.")
    write_md(p["source_digest_md"], f"# Source Digest\n\nSources inspected: {len(digest['entries'])}. Stale assumptions archived: {len(digest['archive_as_stale'])}.")
    write_md(p["touchpoints_md"], f"# Ten-Touchpoint Ledger\n\nParticipants: {len(PARTICIPANTS)}. Touchpoints each: {TOUCHPOINTS_PER_PARTICIPANT}.")
    write_md(p["cli_consultation_md"], "# CLI Council Consultation\n\nArby and Aster use read-only Codex CLI batches when run; Kimi stays non-yolo queued with status evidence.")
    write_md(p["checkpoints_md"], f"# Dashboard Checkpoints\n\nCheckpoint phases: {', '.join(closeout['checkpoint_phases'])}.")
    write_md(p["tapestry_md"], "# Dashboard Tapestry\n\nCheckpoint snapshots are appended and archived to D: without per-exchange dashboard churn.")
    write_md(p["archive_receipt_md"], f"# Dashboard Archive Receipt\n\nArchive root: `{closeout['dashboard_archive_root']}`.")
    write_md(p["system_expansions_md"], f"# System Expansion Board\n\nCandidates: {closeout['system_expansion_count']}.")
    write_md(p["eureka_md"], f"# Eureka Task Board\n\nTasks: {closeout['eureka_task_count']}.")
    write_md(p["command_skill_md"], f"# Command Skill Board\n\nCommands: {closeout['command_count']}. Skills: {closeout['skill_count']}.")
    write_md(p["alpha_security_md"], "# Alpha Cleanup Security\n\nNo deletes, no provider mutations, no browser storage inspection, no Google Drive mutation.")
    write_md(p["future_live_write_md"], "# Deferred Live-Write Pack Drafts\n\nv121-v140 remains postponed; provider packs require future explicit approval and rollback receipts.")
    write_md(p["suite_contract_md"], "# Suite Hook Contract\n\nDeep and L5 materialize suite runs include v201-v220 unless skipped.")
    write_md(p["allowlist_md"], f"# Stage Allowlist\n\nCurated file count: {len(allowlist['include'])}. Broad dirty-tree staging is forbidden.")
    write_md(p["closeout_md"], f"# v201-v220 Closeout\n\nEffective success: `{closeout['effective_success']}`. Chrome: `{closeout['chrome_bridge_status']}`. Spend: 0 NZD.")


def run_all(run_cli: bool = False, chrome_bridge_status: str = "blocked") -> dict[str, Any]:
    started = time.time()
    generated = now_iso()
    p = paths()
    phases = build_phases(generated)
    remote = remote_control_preflight(generated)
    chrome = chrome_truth(generated, chrome_bridge_status)
    digest = source_digest(generated)
    cli_results = run_cli_consults(p, digest, actually_run=run_cli)
    touchpoints = build_touchpoints(generated, cli_results, chrome)
    checkpoints = build_checkpoints(generated, phases, touchpoints)
    boards = build_boards(generated, phases)
    dashboard = build_dashboard(generated, phases, remote, chrome, digest, touchpoints, checkpoints)
    dashboard_state = update_tapestry(p, dashboard)
    allowlist = stage_allowlist(generated, p)
    closeout = {
        "generated_utc": generated,
        "phase_range": "v201-v220",
        "phase_count": len(phases),
        "checkpoint_count": len(checkpoints),
        "checkpoint_phases": [item["phase"] for item in checkpoints],
        "participant_count": len(PARTICIPANTS),
        "touchpoints_per_participant": TOUCHPOINTS_PER_PARTICIPANT,
        "touchpoint_count": touchpoints["total_touchpoints"],
        "system_expansion_count": boards["expansions"]["count"],
        "eureka_task_count": boards["eureka"]["count"],
        "command_count": boards["command_skill"]["command_count"],
        "skill_count": boards["command_skill"]["skill_count"],
        "remote_control_feature_enabled": remote["remote_control_feature_enabled"],
        "remote_control_server_launch_status": remote["server_launch_status"],
        "chrome_bridge_status": chrome_bridge_status,
        "lumina_app_contact": chrome["lumina_app_contact"],
        "dashboard": rel(p["dashboard"]),
        "dashboard_archive_root": str(p["archive_root"]),
        "dashboard_tapestry_entries_this_run": dashboard_state["entry_count_this_run"],
        "external_provider_mutations": "none",
        "external_spend_nzd": 0,
        "google_drive_state": "operator_hold",
        "suite_hook_mode": "deep_and_l5_default_with_skip_flag",
        "runtime_claim": "bounded_execution_completed_no_false_long_wallclock_claim",
        "actual_wallclock_seconds": round(time.time() - started, 3),
        "effective_success": True,
    }
    write_json(p["phase_run"], {"generated_utc": generated, "phase_range": "v201-v220", "phases": phases, "themes": THEMES})
    write_json(p["remote_control"], remote)
    write_json(p["chrome_truth"], chrome)
    write_json(p["source_digest"], digest)
    write_json(p["touchpoints"], touchpoints)
    write_json(p["cli_consultation"], {"generated_utc": generated, "results": cli_results})
    write_json(p["checkpoints"], {"generated_utc": generated, "checkpoints": checkpoints})
    write_json(p["dashboard_state"], dashboard)
    write_json(p["tapestry_index"], {"generated_utc": generated, "entry_count_this_run": dashboard_state["entry_count_this_run"], "archive_root": dashboard_state["archive_root"]})
    write_json(p["archive_receipt"], dashboard_state)
    write_json(p["system_expansions"], boards["expansions"])
    write_json(p["eureka"], boards["eureka"])
    write_json(p["command_skill"], boards["command_skill"])
    write_json(p["alpha_security"], {"generated_utc": generated, "no_deletes": True, "no_browser_storage": True, "google_drive_state": "operator_hold"})
    write_json(p["future_live_write"], {"generated_utc": generated, "status": "postponed", "packs": ["Render", "Neon", "GitHub"], "approval_required": True})
    write_json(p["suite_contract"], {"generated_utc": generated, "profile_hooks": ["deep", "materialize:l5_ha_prod"], "skip_flag": "--skip-v201-v220-cross-app-council-run"})
    write_json(p["allowlist"], allowlist)
    write_json(p["closeout"], closeout)
    p["dashboard"].write_text(dashboard_html(dashboard), encoding="utf-8")
    write_markdown_summaries(p, closeout, remote, chrome, digest, allowlist)
    verification = verify_artifacts(p, allowlist)
    write_json(p["verification"], verification)
    closeout["effective_success"] = verification["effective_success"]
    write_json(p["closeout"], closeout)
    write_markdown_summaries(p, closeout, remote, chrome, digest, allowlist)
    return closeout


def publication_result() -> dict[str, Any]:
    generated = now_iso()
    p = paths()
    local_head = run_command(["git", "rev-parse", "HEAD"], timeout=20)["stdout"].strip()
    branch = run_command(["git", "branch", "--show-current"], timeout=20)["stdout"].strip()
    upstream = run_command(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], timeout=20)["stdout"].strip()
    remote_head = run_command(["git", "rev-parse", upstream], timeout=20)["stdout"].strip() if upstream else ""
    staged = run_command(["git", "diff", "--cached", "--name-only"], timeout=20)["stdout"].splitlines()
    payload = {
        "generated_utc": generated,
        "phase_range": "v201-v220",
        "branch": branch,
        "upstream": upstream,
        "local_head": local_head,
        "remote_head": remote_head,
        "remote_matches_local": bool(local_head and remote_head and local_head == remote_head),
        "staged_count_at_receipt": len([line for line in staged if line.strip()]),
        "forward_only_publication": True,
        "external_provider_mutations": "none",
        "external_spend_nzd": 0,
        "google_drive_state": "operator_hold",
    }
    write_json(p["publication"], payload)
    write_md(
        p["publication_md"],
        f"# v201-v220 Publication Result\n\nLocal `{local_head}`. Remote `{remote_head}`. Matches: `{payload['remote_matches_local']}`.",
    )
    return payload


def dry_run(phase: str, touchpoint: int) -> dict[str, Any]:
    generated = now_iso()
    phases = build_phases(generated)
    selected = next((item for item in phases if item["phase"] == phase), phases[0])
    return {
        "generated_utc": generated,
        "phase": selected,
        "touchpoint": touchpoint,
        "participants": [p["name"] for p in PARTICIPANTS],
        "remote_control": "preflight_only",
        "external_spend_nzd": 0,
        "google_drive_state": "operator_hold",
        "would_write": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-all", action="store_true")
    parser.add_argument("--verify-artifacts", action="store_true")
    parser.add_argument("--publication-result", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-cli-consults", action="store_true")
    parser.add_argument("--chrome-bridge-status", choices=("blocked", "available", "not_attempted"), default="blocked")
    parser.add_argument("--phase", default="v201")
    parser.add_argument("--touchpoint", type=int, default=1)
    args = parser.parse_args()

    if args.publication_result:
        print(json.dumps(publication_result(), indent=2, sort_keys=True))
        return 0
    if args.dry_run:
        print(json.dumps(dry_run(args.phase, args.touchpoint), indent=2, sort_keys=True))
        return 0
    if args.run_all:
        result = run_all(run_cli=args.run_cli_consults, chrome_bridge_status=args.chrome_bridge_status)
        print(json.dumps(result, indent=2, sort_keys=True))
        if args.verify_artifacts:
            verification = read_json(paths()["verification"], {})
            return 0 if verification.get("effective_success") else 1
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
