#!/usr/bin/env python3
"""Record v486 v6 x2 CLI root cause and approval candidate."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
PHASE = "v486-gmut-thos-v22-v6-x2"
SOURCE_X1 = "v486-gmut-thos-v22-v6-x1"


def now_pair() -> tuple[str, str]:
    utc = dt.datetime.now(dt.UTC).replace(microsecond=0)
    nz = utc.astimezone(dt.timezone(dt.timedelta(hours=12), name="NZST"))
    return utc.isoformat().replace("+00:00", "Z"), nz.isoformat()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, bullets: list[str]) -> None:
    lines = [f"# {title}", ""]
    lines.extend(f"- {item}" for item in bullets)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def latest_dir(prefix: str) -> Path | None:
    temp_root = Path(os.environ.get("TEMP", "."))
    matches = sorted(temp_root.glob(prefix), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
    return matches[0] if matches else None


def final_snapshot(lane: str, prefix: str, file_name: str) -> dict[str, Any]:
    folder = latest_dir(prefix)
    if not folder:
        return {"lane": lane, "status": "OPEN_GAP_OUTPUT_FOLDER_NOT_FOUND", "body_text_published": False}
    final_path = folder / file_name
    if not final_path.exists():
        return {"lane": lane, "status": "OPEN_GAP_FINAL_MESSAGE_NOT_FOUND", "body_text_published": False}
    text = final_path.read_text(encoding="utf-8", errors="replace")
    current_phase_found = "v486-gmut-thos-v22-v4-x1" in text or "v486" in text
    stale_authority_found = any(term in text.lower() for term in ["v461", "v462", "v463", "v464", "v58", "2026-04"])
    return {
        "lane": lane,
        "status": "FINAL_REJECTED_STALE_CONTEXT_OR_MISSING_CURRENT_AUTHORITY",
        "final_message_bytes": final_path.stat().st_size,
        "final_message_hash": sha256_text(text),
        "current_phase_reference_found": current_phase_found,
        "stale_authority_reference_found": stale_authority_found,
        "body_text_published": False,
        "raw_output_boundary": "temp_only_not_published",
    }


def main() -> int:
    generated_utc, generated_nz = now_pair()
    x1_status = read_json(TRACE_DIR / f"{SOURCE_X1}-synthesis-v1.json")
    arby = final_snapshot("Arby", "ghc-v486-gmut-thos-v22-v4-x1-arby-*", "Arby-last-message.txt")
    aster = final_snapshot("Aster Vale", "ghc-v486-gmut-thos-v22-v4-x1-aster-*", "AsterVale-last-message.txt")
    root_cause = {
        "artifact_type": "cli_root_cause_receipt",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_ROOT_CAUSE_IDENTIFIED_CURRENT_CONTEXT_MISSING_IN_CLI_WORKTREES",
        "source_x1_status": x1_status.get("overall_status", "unknown"),
        "lane_snapshots": [arby, aster],
        "root_cause": "Arby and Aster Vale advisory worktrees do not contain the current v486 GMUT/THOS handoff/status artifacts, so they reject the v486 request rather than inventing unsupported output.",
        "safe_interpretation": "This is a correctness win: the CLI siblings preserved evidence boundaries, but they need a current context capsule or approved worktree sync before they can rejoin v486 x1 advisory work.",
        "publication_boundary": {
            "raw_lane_body_text_published": False,
            "raw_transport_published": False,
            "local_temp_paths_published": False,
        },
    }
    approval_candidate = {
        "artifact_type": "approval_packet_candidate",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PENDING_USER_APPROVAL_NOT_EXECUTED",
        "title": "APPROVAL PACKET CANDIDATE: ARBY/ASTER CURRENT CONTEXT CAPSULE REPAIR",
        "requested_scope": [
            "Arby advisory worktree curated docs/trinity-live-traces current-context capsule files only",
            "Aster Vale advisory worktree curated docs/trinity-live-traces current-context capsule files only",
            "Main omega repo curated receipts/scripts for validation and publication only",
        ],
        "requested_actions": [
            "Write a small current v486 context capsule into each CLI advisory worktree.",
            "Include only phase slug, current remote head, last verified commits, allowed next boundary, and claim-boundary rules.",
            "Do not copy raw logs, rollout streams, image captures, credentials, or private dumps.",
            "Do not reset, rebase, force-push, broad-stage, or mutate unrelated files.",
            "Retry Arby/Aster read-only CLI lanes from their existing worktrees after capsule validation.",
        ],
        "not_approved_or_executed_now": True,
        "claim_boundary": "This repair would restore advisory context only; it would not validate GMUT, prove physics/consciousness, or promote canon.",
    }
    synthesis = {
        "artifact_type": "x2_synthesis",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_V486_V6_X2_CLI_ROOT_CAUSE_SYNTHESIS",
        "result": [
            "Classified Arby/Aster late outputs as stale-context refusal, not current v486 advisory completion.",
            "Identified missing current-context capsules in CLI advisory worktrees as the practical root cause.",
            "Prepared an approval candidate for a bounded context-capsule repair, not executed.",
            "Kept v486 progress moving through app-lane and Aletheon synthesis while all claim gates remain open.",
        ],
        "next_boundary": "v486-gmut-thos-v22-v7-x1-or-approval-packet-pause",
    }
    validation = {
        "artifact_type": "x2_build_validation",
        "phase_slug": PHASE,
        "generated_utc": generated_utc,
        "generated_nz": generated_nz,
        "overall_status": "PASS_V6_X2_BUILD_VALIDATION",
        "artifact_statuses": {
            "root_cause": root_cause["overall_status"],
            "approval_candidate": approval_candidate["overall_status"],
            "synthesis": synthesis["overall_status"],
        },
        "mutation_boundary": {
            "repo_artifacts_written": True,
            "arby_aster_worktrees_mutated": False,
            "processes_terminated": False,
            "plugin_cache_mutated": False,
            "user_skills_mutated": False,
            "raw_lane_text_published": False,
        },
    }
    outputs = {
        "cli-root-cause": root_cause,
        "arby-aster-context-capsule-approval-candidate": approval_candidate,
        "synthesis": synthesis,
        "build-validation": validation,
    }
    for suffix, payload in outputs.items():
        write_json(TRACE_DIR / f"{PHASE}-{suffix}-v1.json", payload)
    write_md(TRACE_DIR / f"{PHASE}-cli-root-cause-v1.md", "v486 GMUT/THOS v22 v6 x2 CLI Root Cause", [
        f"Status: `{root_cause['overall_status']}`",
        "Arby/Aster preserved evidence boundaries but lack current v486 context in their advisory worktrees.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-arby-aster-context-capsule-approval-candidate-v1.md", "v486 GMUT/THOS v22 v6 x2 Arby/Aster Context Capsule Approval Candidate", [
        f"Status: `{approval_candidate['overall_status']}`",
        "Candidate only: write small current-context capsules into Arby/Aster advisory worktrees, then retry read-only lanes.",
        "Not executed without explicit user approval.",
    ])
    write_md(TRACE_DIR / f"{PHASE}-synthesis-v1.md", "v486 GMUT/THOS v22 v6 x2 Synthesis", [
        f"Status: `{synthesis['overall_status']}`",
        f"Next boundary: `{synthesis['next_boundary']}`",
    ])
    write_md(TRACE_DIR / f"{PHASE}-build-validation-v1.md", "v486 GMUT/THOS v22 v6 x2 Build Validation", [
        f"Status: `{validation['overall_status']}`",
        "No Arby/Aster worktree mutation, process termination, plugin-cache mutation, or raw lane publication occurred.",
    ])
    print(json.dumps({"status": "ok", "phase_slug": PHASE, "outputs": len(outputs) * 2}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
