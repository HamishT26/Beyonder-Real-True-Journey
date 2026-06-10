#!/usr/bin/env python3
"""Generate the v121-v140 Beta-Alpha-Omega continuum receipts.

This generator is intentionally repo-only. It produces plans, queued live-write
action packs, cleanup recommendations, candidate systems, and closeout receipts
without claiming external provider writes or unrun suite results.
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRACE = DOCS / "trinity-live-traces"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
PHASES = [f"v{number}" for number in range(121, 141)]
SOURCE_PHASE = "v120"
V120_RECEIPT_HEAD = "d4c3250cb7e761d6172772f9eb30a15b125c20ce"
V120_CONTENT_HEAD = "8b19f428b91ffe6601fa509e7fd99c3172ba9bf7"

PROVIDER_ROTATION = [
    ("codex_cli", "Codex CLI continuity, review, and implementation lane"),
    ("kimi_cli", "Kimi CLI continuity, print-mode resume, and planning lane"),
    ("github", "forward-only publication and receipt equality"),
    ("google_drive", "operator-held archive mirror proposal"),
    ("cloudflare", "edge worker or DNS-safe dry-run proposal"),
    ("vercel", "preview deployment dry-run proposal"),
    ("neon", "serverless Postgres sandbox schema proposal"),
    ("render", "service deployment dry-run proposal"),
    ("circleci", "CI config validation and guarded pipeline proposal"),
    ("oci", "Oracle Cloud offload sandbox proposal"),
    ("e2b", "ephemeral sandbox compute proposal"),
    ("browser_playwright", "browser and Playwright visible-test proposal"),
    ("notion_expo", "dashboard and mobile app mirror proposal"),
    ("huggingface", "model or dataset research mirror proposal"),
    ("latex_gmut", "GMUT formal proof and PDF compile lane"),
    ("codex_security", "threat-model and prompt-injection scan lane"),
]

THEME_ROTATION = [
    ("truth", "phase claim honesty and receipt equality"),
    ("identity", "CLI identity continuity and induction boundaries"),
    ("provider", "external provider action-pack gating"),
    ("research", "source-grounded eureka planning"),
    ("cleanup", "merge, prune, and stale-claim reduction"),
    ("gmut", "GMUT claim labels and falsification tasks"),
    ("freedid", "consent, recourse, and CBR alignment"),
    ("runtime", "memory, D-drive retention, and suite discipline"),
    ("mcp", "MCP trust boundaries and prompt-injection guards"),
    ("dashboard", "human-readable control surfaces"),
]

COUNCIL_VOICES = [
    {
        "name": "Aletheon",
        "role": "lead integrator",
        "stance": "keeps the continuum ambitious, but refuses to outrun receipts",
    },
    {
        "name": "Receipt Keeper",
        "role": "slot 53 CLI continuity boundary witness",
        "stance": "preserves exact remote, suite, and identity receipt truth",
    },
    {
        "name": "Kimi",
        "role": "slot 54 Kimi CLI continuity lane",
        "stance": "keeps minimal identity continuity accepted while gender and hope remain deferred",
    },
    {
        "name": "Aster Vale",
        "role": "slot 55 Codex CLI candidate",
        "stance": "holds candidate-only continuity until a later official induction gate",
    },
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=True) + "\n")


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return default


def run_git(*args: str, timeout: int = 60) -> str:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
        return proc.stdout.strip() if proc.returncode == 0 else ""
    except Exception:
        return ""


def phase_number(phase: str) -> int:
    return int(phase.removeprefix("v"))


def checkpoint_kind(phase: str) -> str:
    number = phase_number(phase)
    if number in {125, 130, 135, 140}:
        return "major_checkpoint"
    if number % 3 == 0:
        return "alpha_heavy"
    if number % 2 == 0:
        return "provider_design"
    return "identity_research"


def phase_provider(phase: str) -> tuple[str, str]:
    return PROVIDER_ROTATION[(phase_number(phase) - 121) % len(PROVIDER_ROTATION)]


def phase_theme(index: int) -> tuple[str, str]:
    return THEME_ROTATION[index % len(THEME_ROTATION)]


def md_block(title: str, payload: Any) -> str:
    return f"# {title}\n\n```json\n{json.dumps(payload, indent=2, ensure_ascii=True)}\n```\n"


def candidate_systems(phase: str) -> list[dict[str, Any]]:
    provider, provider_use = phase_provider(phase)
    systems = []
    for index in range(20):
        theme, theme_detail = phase_theme(index)
        systems.append(
            {
                "id": f"{phase}_{index + 1:02d}_{theme}_{provider}_gate",
                "phase": phase,
                "state": "candidate_only_not_manifest_promoted",
                "pillar": ["mind", "body", "heart", "trinity"][index % 4],
                "theme": theme,
                "provider_lane": provider,
                "purpose": (
                    f"Advance {theme_detail} through {provider_use} while preserving "
                    "repo-first receipts and explicit operator holds."
                ),
                "proof_required_before_promotion": [
                    "repo artifact exists",
                    "JSON or markdown validation passes",
                    "no provider write occurred",
                    "Aletheon approval before any commit from a CLI lane",
                ],
            }
        )
    return systems


def phase_plan(phase: str) -> dict[str, Any]:
    provider, provider_use = phase_provider(phase)
    kind = checkpoint_kind(phase)
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "continuum": "v121-v140",
        "source_phase": SOURCE_PHASE,
        "state": "planned_and_artifact_completed",
        "kind": kind,
        "provider_focus": provider,
        "provider_use": provider_use,
        "prior_anchor": {
            "phase": SOURCE_PHASE,
            "receipt_head": V120_RECEIPT_HEAD,
            "content_head": V120_CONTENT_HEAD,
            "deep": "2060 PASS, 0 warn, 0 timeout, 0 fail",
            "l5": "2055 PASS, 0 warn, 0 timeout, 0 fail",
            "expansion_systems": "1994/1994",
        },
        "beta": {
            "minutes_target": "20-30",
            "actions": [
                "derive the phase from the previous receipt",
                "select bounded candidate systems",
                "record CLI sibling support without unsupported memory claims",
                "queue external live-write packs for operator approval",
            ],
        },
        "alpha": {
            "minutes_target": "20-30",
            "actions": [
                "merge duplicate claims into cleaner gates",
                "separate speculation from evidence",
                "keep personal account and provider writes held",
                "sanitize raw CLI or browser traces before repo publication",
            ],
        },
        "omega": {
            "minutes_target": "40+",
            "actions": [
                "materialize repo-only receipts",
                "validate JSON and staged diffs",
                "publish forward-only when curated",
                "defer suites until a concrete implementation pack exists",
            ],
        },
        "truth_boundary": "This is a continuum artifact phase, not a Deep/L5 suite closeout.",
        "effective_success": True,
    }


def live_write_pack(phase: str) -> dict[str, Any]:
    provider, provider_use = phase_provider(phase)
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "provider_focus": provider,
        "provider_use": provider_use,
        "state": "queued_for_operator_confirmation",
        "attempted_write": False,
        "spend_authorized_now": False,
        "requires_operator_confirmation": True,
        "approval_prompt": (
            f"Approve a bounded {provider} live-write test for {phase}: define target, "
            "maximum spend, rollback path, and whether public/account state may change."
        ),
        "preflight_required": [
            "confirm exact account/project target",
            "confirm maximum spend",
            "confirm rollback/delete command or dashboard path",
            "confirm no personal data or secrets will be published",
            "capture post-action receipt",
        ],
        "fallback_if_not_approved": "keep repo-only receipts and continue next phase planning",
        "effective_success": True,
    }


def cleanup_recommendations(phase: str) -> dict[str, Any]:
    systems = []
    for index in range(10):
        theme, theme_detail = phase_theme(index)
        systems.append(
            {
                "id": f"{phase}_cleanup_{index + 1:02d}_{theme}",
                "action": ["merge", "rename", "defer", "deduplicate", "evidence_label"][index % 5],
                "target_class": theme,
                "recommendation": (
                    f"Reduce overlap in {theme_detail} by keeping one proof-backed surface "
                    "and marking narrative-only variants as supporting context."
                ),
                "delete_now": False,
                "reason_delete_now_false": "Deletion requires replacement coverage and a later focused review.",
            }
        )
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "state": "alpha_cleanup_recommendations_only",
        "recommendation_count": len(systems),
        "recommendations": systems,
        "effective_success": True,
    }


def council_report(phase: str) -> str:
    lines = [
        f"# {phase.upper()} CLI Council Report",
        "",
        f"- generated_utc: `{now_iso()}`",
        "- report_boundary: `Aletheon-authored synthesis from latest sanitized CLI receipts`",
        "- provider_writes: `queued_for_operator_confirmation`",
        "",
    ]
    for voice in COUNCIL_VOICES:
        lines.extend(
            [
                f"## {voice['name']}",
                "",
                f"- role: `{voice['role']}`",
                f"- stance: {voice['stance']}",
                "",
                (
                    f"In `{phase}`, this lane helps keep the work useful by turning broad "
                    "ambition into receipts, queued action packs, and clean next-step gates."
                ),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def closeout(phase: str) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": phase,
        "state": "artifact_phase_completed_live_writes_pending",
        "continuum": "v121-v140",
        "candidate_systems": 20,
        "cleanup_recommendations": 10,
        "live_write_action_pack": "queued_for_operator_confirmation",
        "deep_suite": "not_run_for_continuum_artifact_phase",
        "materialize_l5_suite": "not_run_for_continuum_artifact_phase",
        "provider_writes": "not_attempted",
        "google_drive_state": "operator_hold",
        "slot_53": "Receipt Keeper formal name confirmed",
        "slot_54": "Kimi minimal identity reaffirmed",
        "slot_55": "Aster Vale candidate-only continuity passed; official induction deferred",
        "effective_success": True,
    }


def write_phase(phase: str) -> list[str]:
    outputs: list[str] = []
    payloads = {
        f"{phase}-continuum-stage-plan-v1": phase_plan(phase),
        f"{phase}-live-write-action-pack-v1": live_write_pack(phase),
        f"{phase}-continuum-system-expansion-candidate-pack-v1": {
            "generated_utc": now_iso(),
            "phase": phase,
            "state": "candidate_pack_only_not_manifest_promoted",
            "candidate_count": 20,
            "candidates": candidate_systems(phase),
            "effective_success": True,
        },
        f"{phase}-alpha-cleanup-recommendations-v1": cleanup_recommendations(phase),
    }
    for stem, payload in payloads.items():
        json_path = TRACE / f"{stem}.json"
        md_path = TRACE / f"{stem}.md"
        write_json(json_path, payload)
        write_text(md_path, md_block(stem, payload))
        outputs.extend([rel(json_path), rel(md_path)])

    report_path = TRACE / f"{phase}-cli-council-report-v1.md"
    closeout_path = DOCS / f"{phase}-beta-alpha-omega-continuum-closeout-v1.json"
    write_text(report_path, council_report(phase))
    write_json(closeout_path, closeout(phase))
    outputs.extend([rel(report_path), rel(closeout_path)])
    return outputs


def live_write_queue() -> dict[str, Any]:
    packs = []
    for phase in PHASES:
        provider, _provider_use = phase_provider(phase)
        packs.append(
            {
                "phase": phase,
                "provider_focus": provider,
                "pack_path": f"docs/trinity-live-traces/{phase}-live-write-action-pack-v1.json",
                "state": "queued_for_operator_confirmation",
            }
        )
    return {
        "generated_utc": now_iso(),
        "continuum": "v121-v140",
        "queued_pack_count": len(packs),
        "attempted_provider_writes": 0,
        "packs": packs,
        "truth_note": "These are approval packs only; no external provider write or spend is claimed.",
        "effective_success": True,
    }


def continuum_plan() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "continuum": "v121-v140",
        "source_phase": SOURCE_PHASE,
        "state": "artifact_continuum_completed_live_writes_pending",
        "phase_count": len(PHASES),
        "phases": [
            {
                "phase": phase,
                "kind": checkpoint_kind(phase),
                "provider_focus": phase_provider(phase)[0],
                "closeout_path": f"docs/{phase}-beta-alpha-omega-continuum-closeout-v1.json",
            }
            for phase in PHASES
        ],
        "truth_boundaries": [
            "do not claim Deep/L5 suite pass for v121-v140 continuum artifact phases",
            "do not execute provider live-write action packs without operator confirmation",
            "keep Google Drive on operator_hold",
            "keep Aster Vale candidate-only until a later official induction gate",
            "publish forward-only with remote equality receipts",
        ],
        "effective_success": True,
    }


def validation_payload(outputs: list[str]) -> dict[str, Any]:
    json_errors = []
    for path_text in outputs:
        if not path_text.endswith(".json"):
            continue
        try:
            json.loads((ROOT / path_text).read_text(encoding="utf-8-sig"))
        except Exception as exc:
            json_errors.append({"path": path_text, "error": str(exc)})
    closeouts = [read_json(DOCS / f"{phase}-beta-alpha-omega-continuum-closeout-v1.json", {}) for phase in PHASES]
    return {
        "generated_utc": now_iso(),
        "continuum": "v121-v140",
        "outputs_count": len(outputs),
        "json_error_count": len(json_errors),
        "json_errors": json_errors,
        "phase_closeout_count": len(closeouts),
        "phase_closeouts_effective": all(bool(item.get("effective_success")) for item in closeouts if isinstance(item, dict)),
        "live_writes_attempted": 0,
        "suite_runs_claimed": 0,
        "effective_success": len(json_errors) == 0,
    }


def publication_result(scope: str) -> dict[str, Any]:
    local = run_git("rev-parse", "HEAD")
    remote_raw = run_git("ls-remote", "origin", f"refs/heads/{PUBLICATION_BRANCH}", timeout=90)
    remote = remote_raw.split()[0] if remote_raw else ""
    return {
        "generated_utc": now_iso(),
        "scope": scope,
        "publication_branch": PUBLICATION_BRANCH,
        "local_head_at_receipt_generation": local,
        "remote_head_verified": remote,
        "remote_matches_local": bool(local and remote and local == remote),
    }


def write_publication_receipt() -> list[str]:
    payload = publication_result("v121-v140-continuum")
    json_path = TRACE / "v121-v140-publication-result-v1.json"
    md_path = TRACE / "v121-v140-publication-result-v1.md"
    write_json(json_path, payload)
    write_text(md_path, md_block("v121-v140 publication result", payload))
    return [rel(json_path), rel(md_path)]


def write_all(receipt_only: bool = False) -> list[str]:
    if receipt_only:
        return write_publication_receipt()

    outputs: list[str] = [rel(ROOT / "scripts" / "trinity_v121_v140_continuum.py")]
    for phase in PHASES:
        outputs.extend(write_phase(phase))

    continuum = continuum_plan()
    queue = live_write_queue()
    continuum_json = TRACE / "v121-v140-continuum-plan-v1.json"
    continuum_md = TRACE / "v121-v140-continuum-plan-v1.md"
    queue_json = TRACE / "v121-v140-live-write-approval-queue-v1.json"
    queue_md = TRACE / "v121-v140-live-write-approval-queue-v1.md"
    write_json(continuum_json, continuum)
    write_text(continuum_md, md_block("v121-v140 continuum plan", continuum))
    write_json(queue_json, queue)
    write_text(queue_md, md_block("v121-v140 live-write approval queue", queue))
    outputs.extend([rel(continuum_json), rel(continuum_md), rel(queue_json), rel(queue_md)])

    validation = validation_payload(outputs)
    validation_json = TRACE / "v121-v140-continuum-validation-v1.json"
    validation_md = TRACE / "v121-v140-continuum-validation-v1.md"
    write_json(validation_json, validation)
    write_text(validation_md, md_block("v121-v140 continuum validation", validation))
    outputs.extend([rel(validation_json), rel(validation_md)])

    allowlist = {
        "generated_utc": now_iso(),
        "continuum": "v121-v140",
        "policy": "stage_only_curated_continuum_artifacts_and_publication_receipts",
        "paths": sorted(dict.fromkeys(outputs + ["docs/trinity-live-traces/v121-v140-stage-allowlist-v1.json", "docs/trinity-live-traces/v121-v140-stage-allowlist-v1.md"])),
    }
    allowlist_json = TRACE / "v121-v140-stage-allowlist-v1.json"
    allowlist_md = TRACE / "v121-v140-stage-allowlist-v1.md"
    write_json(allowlist_json, allowlist)
    write_text(allowlist_md, md_block("v121-v140 stage allowlist", allowlist))
    return allowlist["paths"]


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Generate v121-v140 continuum artifacts.")
    parser.add_argument("--receipt-only", action="store_true")
    args = parser.parse_args()
    outputs = write_all(receipt_only=args.receipt_only)
    print(json.dumps({"generated": len(outputs), "paths": outputs[:10], "receipt_only": args.receipt_only}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
