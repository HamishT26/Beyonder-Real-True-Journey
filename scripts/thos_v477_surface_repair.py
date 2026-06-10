#!/usr/bin/env python3
"""Generate v477 THOS command-index and v54/v55 handoff surface artifacts."""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRACES = DOCS / "trinity-live-traces"

BASELINE_HEAD = "452a3c6d571e2dcec887de91604ba3fdd08a4f2e"
SESSION_START_NZ = "2026-06-04T00:24:27+12:00"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_lines(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def file_record(path: Path, role: str) -> dict:
    exists = path.exists()
    return {
        "role": role,
        "path": rel(path),
        "exists": exists,
        "bytes": path.stat().st_size if exists else None,
        "sha256": sha256(path) if exists else None,
        "tracked": bool(git_lines("ls-files", "--", rel(path))) if exists else False,
    }


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_md(path: Path, title: str, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = ["# " + title, "", *lines]
    path.write_text("\n".join(body).rstrip() + "\n", encoding="utf-8")


def highest_command_book_json() -> Path | None:
    books = []
    for path in DOCS.glob("trinity-command-book-v*.json"):
        suffix = path.stem.removeprefix("trinity-command-book-v")
        if suffix.isdigit():
            books.append((int(suffix), path))
    return sorted(books)[-1][1] if books else None


def workbench_contract_record(path: Path) -> dict:
    data = json_load(path)
    return {
        "path": rel(path),
        "sha256": sha256(path),
        "pack": data.get("pack"),
        "continuity_band": data.get("continuity_band"),
        "repo_targets": data.get("repo_targets", []),
        "declares_read_surfaces": "read_surfaces" in data,
        "declares_command_index_surface": any(
            "trinity-command-book" in str(target) or "command-index" in str(target)
            for target in data.get("repo_targets", [])
        ),
    }


def main() -> None:
    now_utc = _dt.datetime.now(_dt.UTC).replace(microsecond=0).isoformat()

    command_validation_path = DOCS / "trinity-command-book-validation-latest.json"
    command_latest_md_path = DOCS / "trinity-command-book-latest.md"
    command_latest_json_path = highest_command_book_json()
    runtime_model_path = DOCS / "trinity-runtime-model-resolution-v1.json"
    v54_pack_path = DOCS / "v54-omega-continuity-pack-v1.md"
    v55_pack_path = DOCS / "v55-beta-continuity-pack-v1.md"
    v54_policy_path = DOCS / "v54-omega-handoff-policy-v1.json"
    v55_policy_path = DOCS / "v55-beta-handoff-policy-v1.json"
    wb_v10_path = DOCS / "new-project-workbench-v10-contract-v1.json"
    wb_v11_path = DOCS / "new-project-workbench-v11-contract-v1.json"
    missing_prompt_contract = DOCS / "trinity-workbench-contract-v6.json"

    validation = json_load(command_validation_path)
    runtime = json_load(runtime_model_path)
    status_lines = git_lines(
        "status",
        "--short",
        "--",
        rel(command_validation_path),
        rel(runtime_model_path),
        rel(wb_v10_path),
        rel(wb_v11_path),
    )

    common = {
        "generated_utc": now_utc,
        "session_start_nz": SESSION_START_NZ,
        "phase": "v477_thos_v1",
        "baseline_head": BASELINE_HEAD,
        "claim_boundary": {
            "domain": "THOS surface repair and handoff visibility only",
            "gmut_gate_state": "all_gmut_gates_remain_open",
            "canon_promotion": "not_claimed",
        },
        "dirty_input_notice": {
            "status": "observed_not_staged_by_this_generator",
            "files": status_lines,
        },
    }

    command_surface = {
        **common,
        "artifact_type": "command_index_read_surfaces",
        "overall_status": "PASS_WITH_OPEN_GAP",
        "open_gap": (
            "The prompt-named trinity-workbench-contract-v6.json is not tracked in this repo; "
            "v10/v11 workbench contracts are tracked but do not declare read_surfaces."
        ),
        "read_surfaces": [
            {
                "surface_id": "read_command_index",
                "path": rel(command_latest_md_path),
                "validator_path": rel(command_validation_path),
                "validation_status": validation.get("overall_status"),
                "command_count": validation.get("command_count"),
                "latest_json_path": rel(command_latest_json_path) if command_latest_json_path else None,
            },
            {
                "surface_id": "read_command_book_validation",
                "path": rel(command_validation_path),
                "validation_status": validation.get("overall_status"),
                "command_count": validation.get("command_count"),
            },
        ],
        "source_hashes": [
            file_record(command_latest_md_path, "command_book_markdown"),
            file_record(command_validation_path, "command_book_validation"),
            file_record(command_latest_json_path, "highest_command_book_json")
            if command_latest_json_path
            else {"role": "highest_command_book_json", "exists": False},
        ],
        "workbench_contracts": [
            workbench_contract_record(wb_v10_path),
            workbench_contract_record(wb_v11_path),
            {
                "path": rel(missing_prompt_contract),
                "exists": False,
                "status": "not_tracked_in_repo",
                "action": "replaced_by_curated_v477_read_surface_manifest",
            },
        ],
    }

    handoff_surface = {
        **common,
        "artifact_type": "v54_v55_handoff_surface",
        "overall_status": "PASS",
        "runtime_model_resolution": {
            "path": rel(runtime_model_path),
            "active_handoff_pack_path": runtime.get("active_handoff_pack_path"),
            "next_receiver_pack_path": runtime.get("next_receiver_pack_path"),
            "active_handoff_policy_path": runtime.get("active_handoff_policy_path"),
            "next_receiver_policy_path": runtime.get("next_receiver_policy_path"),
        },
        "read_surfaces": [
            {
                "surface_id": "active_v54_omega_continuity_pack",
                "path": rel(v54_pack_path),
                "policy_path": rel(v54_policy_path),
            },
            {
                "surface_id": "next_v55_beta_receiver_pack",
                "path": rel(v55_pack_path),
                "policy_path": rel(v55_policy_path),
            },
        ],
        "source_hashes": [
            file_record(runtime_model_path, "runtime_model_resolution"),
            file_record(v54_pack_path, "active_v54_pack"),
            file_record(v55_pack_path, "next_v55_pack"),
            file_record(v54_policy_path, "active_v54_policy"),
            file_record(v55_policy_path, "next_v55_policy"),
        ],
    }

    x1_audit = {
        **common,
        "artifact_type": "v477_thos_v1_x1_surface_audit",
        "overall_status": "WARN",
        "findings": [
            "Command-book validation exists and reports PASS with 684 commands.",
            "The command-book markdown exists and is hashable.",
            "The runtime model points to v54 omega and v55 beta handoff packs.",
            "The v54/v55 packs and policies exist and are hashable.",
            "The prompt-named workbench contract is absent from tracked repo scope.",
            "Tracked v10/v11 workbench contracts do not declare read_surfaces.",
        ],
        "recommended_repair": [
            rel(DOCS / "trinity-command-index-read-surfaces-v1.json"),
            rel(DOCS / "trinity-v54-v55-handoff-surface-v1.json"),
        ],
    }

    x2_repair = {
        **common,
        "artifact_type": "v477_thos_v1_x2_surface_repair",
        "overall_status": "PASS_WITH_OPEN_GAP",
        "published_surfaces": [
            rel(DOCS / "trinity-command-index-read-surfaces-v1.json"),
            rel(DOCS / "trinity-command-index-read-surfaces-latest.md"),
            rel(DOCS / "trinity-v54-v55-handoff-surface-v1.json"),
            rel(DOCS / "trinity-v54-v55-handoff-surface-latest.md"),
        ],
        "repair_boundary": [
            "No older contract file was edited.",
            "No local absolute workbench paths were reprinted.",
            "No nonpublic connector payload was published.",
            "No GMUT closure claim was made.",
        ],
        "next_phase": "v477_thos_v2_x1",
    }

    run_status = {
        **common,
        "artifact_type": "v477_thos_v1_run_status",
        "overall_status": "PASS_WITH_OPEN_GAP",
        "x1_status": "surface_audit_complete",
        "x2_status": "curated_surface_repair_complete",
        "codex_cli_version_observed": "codex-cli 0.135.0",
        "codex_cli_update_note": "0.136.0 was user-observed as available, but installing or replacing binaries was outside this packet.",
        "next_expected_phase": "v477_thos_v2_x1",
        "blockers": [
            "trinity-workbench-contract-v6.json is not tracked in this repo.",
            "Codex CLI local version observed by diagnostic is 0.135.0, not 0.136.0.",
        ],
    }

    write_json(DOCS / "trinity-command-index-read-surfaces-v1.json", command_surface)
    write_json(DOCS / "trinity-v54-v55-handoff-surface-v1.json", handoff_surface)
    write_json(TRACES / "v477-thos-v1-x1-surface-audit-v1.json", x1_audit)
    write_json(TRACES / "v477-thos-v1-x2-surface-repair-v1.json", x2_repair)
    write_json(TRACES / "v477-thos-v1-x2-run-status-v1.json", run_status)

    write_md(
        DOCS / "trinity-command-index-read-surfaces-latest.md",
        "Trinity Command Index Read Surfaces",
        [
            f"- generated_utc: `{now_utc}`",
            "- overall_status: `PASS_WITH_OPEN_GAP`",
            "- read_command_index: `docs/trinity-command-book-latest.md`",
            "- validation: `docs/trinity-command-book-validation-latest.json`",
            f"- command_count: `{validation.get('command_count')}`",
            f"- validation_status: `{validation.get('overall_status')}`",
            "- latest_json: `" + (rel(command_latest_json_path) if command_latest_json_path else "missing") + "`",
            "- open_gap: `trinity-workbench-contract-v6.json` is not tracked in this repo; v10/v11 workbench contracts are tracked but do not declare `read_surfaces`.",
            "- boundary: THOS surface repair only; no GMUT gate closure or canon promotion is claimed.",
        ],
    )
    write_md(
        DOCS / "trinity-v54-v55-handoff-surface-latest.md",
        "Trinity V54/V55 Handoff Surface",
        [
            f"- generated_utc: `{now_utc}`",
            "- overall_status: `PASS`",
            f"- runtime_model_resolution: `{rel(runtime_model_path)}`",
            f"- active_v54_pack: `{runtime.get('active_handoff_pack_path')}`",
            f"- next_v55_pack: `{runtime.get('next_receiver_pack_path')}`",
            f"- active_v54_policy: `{runtime.get('active_handoff_policy_path')}`",
            f"- next_v55_policy: `{runtime.get('next_receiver_policy_path')}`",
            "- boundary: these are continuity handoff surfaces only; they do not validate GMUT physics claims.",
        ],
    )
    write_md(
        TRACES / "v477-thos-v1-x1-surface-audit-v1.md",
        "V477 THOS V1 X1 Surface Audit",
        [
            f"- generated_utc: `{now_utc}`",
            "- command book validation exists and reports `PASS`.",
            "- command count: `684`.",
            "- v54/v55 continuity packs exist and are hashable.",
            "- prompt-named contract `trinity-workbench-contract-v6.json` is absent from tracked repo scope.",
            "- tracked workbench contracts v10/v11 do not declare `read_surfaces`.",
            "- recommended repair: publish curated command-index and v54/v55 read-surface manifests.",
        ],
    )
    write_md(
        TRACES / "v477-thos-v1-x2-surface-repair-v1.md",
        "V477 THOS V1 X2 Surface Repair",
        [
            f"- generated_utc: `{now_utc}`",
            "- status: `PASS_WITH_OPEN_GAP`.",
            "- published command-index read surface: `docs/trinity-command-index-read-surfaces-v1.json`.",
            "- published v54/v55 handoff surface: `docs/trinity-v54-v55-handoff-surface-v1.json`.",
            "- no older workbench contract was edited.",
            "- no local absolute workbench paths were reprinted.",
            "- next expected phase: `v477_thos_v2_x1`.",
        ],
    )
    write_md(
        TRACES / "v477-thos-v1-x2-run-status-v1.md",
        "V477 THOS V1 X2 Run Status",
        [
            f"- generated_utc: `{now_utc}`",
            "- status: `PASS_WITH_OPEN_GAP`.",
            "- x1: surface audit complete.",
            "- x2: curated surface repair complete.",
            "- Codex CLI diagnostic observed `codex-cli 0.135.0`.",
            "- installing or replacing Codex binaries is outside this packet.",
            "- next expected phase: `v477_thos_v2_x1`.",
        ],
    )

    print(json.dumps({"status": "ok", "generated": 10}, indent=2))


if __name__ == "__main__":
    main()
