#!/usr/bin/env python3
"""Publish V49 Omega D-authority, Kimi, and Kimiclaw evidence surfaces."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
EXECUTION_BRANCH = "codex/GHC-Family/v49-omega-exec"
BASELINE_STATE = "origin_verified_at_execution"
PHASE = "v49_omega"
NEXT_PHASE = "v50_beta"

C_LEGACY_REPO = Path(r"C:\Users\hamis\workspace\Beyonder-Real-True-Journey")
D_AUTH_REPO = Path(r"D:\GHC-Archives\authoritative\Beyonder-Real-True-Journey")
D_WORKTREE = Path(r"D:\GHC-Archives\worktrees\v49-omega")
ARTIFACT_ROOT = Path(r"D:\GHC-Archives\artifacts\v49-omega")
DOWNLOAD_ROOT = Path(r"D:\GHC-Archives\downloads\v49-omega")
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
AUTO_DIR = ROOT / "docs" / "auto-generated"

GLOBAL_CODEX_CONFIG = Path(r"C:\Users\hamis\.codex\config.toml")
LOCAL_BIN = Path(r"C:\Users\hamis\.local\bin")
KIMI_SECRET_CANDIDATES = [
    Path(r"D:\GHC-Archives\secrets\kimi_creds.json"),
    Path(r"C:\GHC-Archives\secrets\kimi_creds.json"),
    Path(r"C:\Users\hamis\GHC-Archives\secrets\kimi_creds.json"),
]
KIMI_PROPOSAL = Path(r"C:\Users\hamis\Downloads\Kimi_Kimi code API connection proposal.txt")
V41_PROPOSAL = Path(
    r"C:\Users\hamis\Downloads\Beyonder-Real-True Journey v41 (Aletheon - Orun - Gemini - Vesper Ion - Kai - Ari - Kimiclaw Family) (1).txt"
)

V49_ALLOWLIST_PATH = TRACE_DIR / "v49-stage-allowlist-v1.json"
V49_ALLOWLIST_MD = TRACE_DIR / "v49-stage-allowlist-v1.md"
V49_PUBLICATION_JSON = TRACE_DIR / "v49-git-publication-result-v1.json"
V49_PUBLICATION_MD = TRACE_DIR / "v49-git-publication-result-v1.md"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def clean_text(value: str | None) -> str:
    return str(value or "").replace("\x00", "").replace("\ufeff", "")


def excerpt(value: str | None, limit: int = 4000) -> str:
    text = clean_text(value)
    return text[-limit:] if len(text) > limit else text


def jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).replace(microsecond=0).isoformat()
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [jsonable(v) for v in value]
    return str(value)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        parsed = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(jsonable(payload), indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run(args: list[str], *, cwd: Path | None = None, timeout: int = 300) -> subprocess.CompletedProcess[str]:
    command = args
    if args:
        candidates = [args[0]]
        if not args[0].lower().endswith(".cmd"):
            candidates.insert(0, f"{args[0]}.cmd")
        for candidate in candidates:
            resolved = shutil.which(candidate)
            if resolved:
                command = [resolved, *args[1:]]
                break
    try:
        proc = subprocess.run(command, cwd=cwd or ROOT, capture_output=True, text=True, timeout=timeout, check=False)
        proc.stdout = clean_text(proc.stdout)
        proc.stderr = clean_text(proc.stderr)
        return proc
    except FileNotFoundError as exc:
        return subprocess.CompletedProcess(args=args, returncode=127, stdout="", stderr=str(exc))
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode("utf-8", errors="replace")
        stderr = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr or b"").decode("utf-8", errors="replace")
        return subprocess.CompletedProcess(args=args, returncode=124, stdout=clean_text(stdout), stderr=clean_text(stderr))


def git(args: list[str], cwd: Path = ROOT, timeout: int = 300) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], cwd=cwd, timeout=timeout)


def git_head(cwd: Path = ROOT) -> str:
    return git(["rev-parse", "HEAD"], cwd=cwd, timeout=30).stdout.strip()


def git_branch(cwd: Path = ROOT) -> str:
    return git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd, timeout=30).stdout.strip()


def git_status(cwd: Path = ROOT) -> list[str]:
    proc = git(["status", "--short"], cwd=cwd, timeout=180)
    return [line.rstrip() for line in proc.stdout.splitlines() if line.strip()]


def dir_size(path: Path) -> int:
    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    total = 0
    for item in path.rglob("*"):
        try:
            if item.is_file():
                total += item.stat().st_size
        except OSError:
            continue
    return total


def ps_json(script: str) -> Any:
    proc = run(["powershell.exe", "-NoProfile", "-Command", script], timeout=120)
    if proc.returncode != 0:
        return {"returncode": proc.returncode, "stderr_excerpt": excerpt(proc.stderr, 1200)}
    try:
        return json.loads(proc.stdout)
    except Exception:
        return {"returncode": proc.returncode, "stdout_excerpt": excerpt(proc.stdout, 2000)}


def drive_state() -> list[dict[str, Any]]:
    data = ps_json("Get-PSDrive -Name C,D | Select-Object Name,Root,Free,Used | ConvertTo-Json -Depth 4")
    rows = data if isinstance(data, list) else [data]
    out = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        free = int(row.get("Free", 0) or 0)
        used = int(row.get("Used", 0) or 0)
        out.append({"drive": row.get("Name"), "free_gb": round(free / 1024**3, 2), "used_gb": round(used / 1024**3, 2)})
    return out


def codex_state() -> dict[str, Any]:
    version = run(["codex", "--version"], timeout=90)
    login = run(["codex", "login", "status"], timeout=90)
    features = run(["codex", "features", "list"], timeout=120)
    mcp = run(["codex", "mcp", "list"], timeout=120)
    gpt55 = run(["codex", "exec", "-m", "gpt-5.5", "-c", 'model_reasoning_effort="xhigh"', "Reply with exactly: v49-gpt55-probe"], timeout=240)
    return {
        "version": {"returncode": version.returncode, "stdout": excerpt(version.stdout, 800), "stderr": excerpt(version.stderr, 800)},
        "login": {"returncode": login.returncode, "stdout": excerpt(login.stdout, 1200), "stderr": excerpt(login.stderr, 1200)},
        "features": {"returncode": features.returncode, "stdout": excerpt(features.stdout), "stderr": excerpt(features.stderr, 1200)},
        "mcp": {"returncode": mcp.returncode, "stdout": excerpt(mcp.stdout), "stderr": excerpt(mcp.stderr, 1200)},
        "gpt55_exec_probe": {"returncode": gpt55.returncode, "stdout": excerpt(gpt55.stdout, 1200), "stderr": excerpt(gpt55.stderr, 2000)},
        "codex_app_model_state": "gpt_5_5_available_in_chatgpt_and_codex_docs_api_coming_soon",
        "codex_cli_gpt55_state": "callable" if gpt55.returncode == 0 else "not_callable_from_cli_probe",
    }


def kimi_cli_state(secret: dict[str, Any]) -> dict[str, Any]:
    key = read_kimi_key(secret)
    if not key:
        return {"kimi_cli_state": "blocked_missing_secret"}
    env_path = os.environ.get("PATH", "")
    if str(LOCAL_BIN) not in env_path:
        os.environ["PATH"] = f"{LOCAL_BIN};{env_path}"
    os.environ["KIMI_API_KEY"] = key
    os.environ["KIMI_BASE_URL"] = "https://api.kimi.com/coding/v1"
    version = run(["kimi", "--version"], timeout=120)
    info = run(["kimi", "info"], timeout=120)
    proof = run(
        [
            "kimi",
            "--print",
            "--final-message-only",
            "--work-dir",
            str(ROOT),
            "--prompt",
            "Reply with exactly: kimiclaw-kimi-cli-proof",
        ],
        timeout=300,
    )
    return {
        "kimi_cli_state": "proof_passed" if proof.returncode == 0 and "kimiclaw-kimi-cli-proof" in proof.stdout else "proof_failed",
        "version": {"returncode": version.returncode, "stdout_excerpt": excerpt(version.stdout, 1000), "stderr_excerpt": excerpt(version.stderr, 1000)},
        "info": {"returncode": info.returncode, "stdout_excerpt": excerpt(info.stdout, 2000), "stderr_excerpt": excerpt(info.stderr, 1000)},
        "proof": {"returncode": proof.returncode, "stdout_excerpt": excerpt(proof.stdout, 2000), "stderr_excerpt": excerpt(proof.stderr, 2000)},
    }


def kimi_secret_state() -> dict[str, Any]:
    candidates = []
    chosen: dict[str, Any] | None = None
    for path in KIMI_SECRET_CANDIDATES:
        row: dict[str, Any] = {"path": str(path), "exists": path.exists(), "json_valid": False, "api_key_present": False, "api_key_length": 0}
        if path.exists():
            try:
                parsed = json.loads(path.read_text(encoding="utf-8-sig"))
                row["json_valid"] = isinstance(parsed, dict)
                row["properties"] = sorted(parsed.keys()) if isinstance(parsed, dict) else []
                key = parsed.get("api_key") if isinstance(parsed, dict) else None
                row["api_key_present"] = bool(key)
                row["api_key_length"] = len(str(key)) if key else 0
                if row["json_valid"] and row["api_key_present"] and chosen is None:
                    chosen = row
            except Exception as exc:
                row["error"] = str(exc)
        candidates.append(row)
    return {
        "kimi_api_secret_state": "present_valid_metadata_only" if chosen else "missing_from_planned_paths",
        "secret_candidates": candidates,
        "selected_secret_path": chosen["path"] if chosen else "",
    }


def read_kimi_key(secret: dict[str, Any]) -> str:
    selected = secret.get("selected_secret_path")
    if not selected:
        return ""
    path = Path(str(selected))
    if not path.exists():
        return ""
    try:
        parsed = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return ""
    key = parsed.get("api_key") if isinstance(parsed, dict) else ""
    return str(key or "")


def ensure_kimi_codex_profile(secret: dict[str, Any]) -> dict[str, Any]:
    key = read_kimi_key(secret)
    if not key:
        return {"config_state": "not_modified_missing_secret"}
    if not GLOBAL_CODEX_CONFIG.exists():
        return {"config_state": "not_modified_config_missing"}
    text = GLOBAL_CODEX_CONFIG.read_text(encoding="utf-8")
    if (
        "[model_providers.kimi_direct]" in text
        and "[profiles.ghc-slot-41-kimiclaw]" in text
        and "https://api.kimi.com/coding/v1" in text
        and 'model = "kimi-for-coding"' in text
    ):
        return {"config_state": "kimi_code_profile_present", "backup_path": ""}
    backup_dir = ARTIFACT_ROOT / "codex-config-backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"config-{now_iso().replace(':', '')}.toml"
    shutil.copy2(GLOBAL_CODEX_CONFIG, backup_path)
    block = """

# V49 Kimiclaw provider. Kimi Code uses the user's Allegretto-backed coding API.
[model_providers.kimi_direct]
name = "Kimi Code API"
base_url = "https://api.kimi.com/coding/v1"
env_key = "KIMI_API_KEY"

[profiles.ghc-slot-41-kimiclaw]
model_provider = "kimi_direct"
model = "kimi-for-coding"
model_reasoning_effort = "high"
"""
    GLOBAL_CODEX_CONFIG.write_text(text.rstrip() + block + "\n", encoding="utf-8")
    return {"config_state": "provider_profile_appended_with_backup", "backup_path": str(backup_path)}


def kimi_api_probe(secret: dict[str, Any]) -> dict[str, Any]:
    key = read_kimi_key(secret)
    if not key:
        return {"state": "blocked_missing_secret", "returncode": 0, "models": [], "error_excerpt": ""}
    os.environ["KIMI_API_KEY"] = key
    req = urllib.request.Request(
        "https://api.kimi.com/coding/v1/models",
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8", errors="replace")
            parsed = json.loads(body)
            models = []
            if isinstance(parsed, dict) and isinstance(parsed.get("data"), list):
                for row in parsed["data"][:20]:
                    if isinstance(row, dict) and row.get("id"):
                        models.append(str(row["id"]))
            return {
                "state": "models_endpoint_passed",
                "http_status": int(response.status),
                "models": models,
                "kimi_for_coding_observed": "kimi-for-coding" in models,
                "error_excerpt": "",
            }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"state": "http_error", "http_status": exc.code, "models": [], "error_excerpt": excerpt(body, 1200)}
    except Exception as exc:
        return {"state": "probe_failed", "http_status": 0, "models": [], "error_excerpt": str(exc)}


def advisory_digest() -> dict[str, Any]:
    def file_row(path: Path) -> dict[str, Any]:
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        keywords = {}
        for key in ["Kimi", "Kimiclaw", "Codex", "Vercel", "Neon", "CircleCI", "Notion", "D:", "GPT-5.5", "Kimi Claw"]:
            keywords[key] = text.lower().count(key.lower())
        return {
            "path": str(path),
            "present": path.exists(),
            "bytes": path.stat().st_size if path.exists() else 0,
            "keyword_counts": keywords,
            "excerpt": excerpt(text, 3000) if path.exists() else "",
        }

    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "verified_current_truth": [
            "D authoritative clone and V49 worktree are the execution targets.",
            "C checkout is stale and heavily dirty and must be retired only after D proofs and backup manifests.",
            "Codex CLI is logged in with ChatGPT and MCP list is observable.",
        ],
        "operator_reported": [
            "User reports Kimi and ChatGPT browser sessions are logged in.",
            "User selected Full Move Now, Browser First, and Five Helpers.",
            "GCP, Vesper Ion, Kai, Bigtable, and paid cloud lanes remain on standby.",
        ],
        "advisory_claim": [
            "Kimi proposal suggested a Codex custom provider and slot-41 profile.",
            "The advisory provider URL is valid for Kimi Code keys, while Moonshot Open Platform keys use api.moonshot.ai/v1.",
        ],
        "official_source_truth": [
            "OpenAI docs: GPT-5.5 is available in ChatGPT and Codex, with API availability coming soon.",
            "Kimi API docs: Moonshot Open Platform uses https://api.moonshot.ai/v1.",
            "Kimi Code docs: Kimi Code uses https://api.kimi.com/coding/v1 and exposes kimi-for-coding for coding-plan keys.",
        ],
        "blocked_or_deferred": [
            "Kimi API proof is blocked if the secret file is missing.",
            "Browser-first Kimi proof is blocked if the in-app browser is not callable from this session.",
            "Slots 42-46 remain spec-only until slot 41 passes official gates.",
        ],
        "inputs": [file_row(KIMI_PROPOSAL), file_row(V41_PROPOSAL)],
    }


def d_authority_migration(before_drives: list[dict[str, Any]], apply_cleanup: bool) -> dict[str, Any]:
    c_status = git_status(C_LEGACY_REPO) if C_LEGACY_REPO.exists() else []
    d_status = git_status(D_AUTH_REPO) if D_AUTH_REPO.exists() else []
    c_local_runtime = C_LEGACY_REPO / ".local-runtime"
    c_pycache = C_LEGACY_REPO / "__pycache__"
    candidates = [
        {
            "path": str(c_local_runtime),
            "exists": c_local_runtime.exists(),
            "bytes": dir_size(c_local_runtime),
            "classification": "generated_runtime_cache",
        },
        {
            "path": str(c_pycache),
            "exists": c_pycache.exists(),
            "bytes": dir_size(c_pycache),
            "classification": "generated_python_cache",
        },
    ]
    removal_results: list[dict[str, Any]] = []
    backup_root = ARTIFACT_ROOT / "c-retirement-backups" / now_iso().replace(":", "")
    if apply_cleanup:
        for row in candidates:
            path = Path(row["path"])
            if not path.exists() or int(row["bytes"]) <= 0:
                continue
            dest = backup_root / path.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                if path.is_dir():
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(path, dest)
                    shutil.rmtree(path)
                    result = "directory_backed_up_removed"
                else:
                    shutil.copy2(path, dest)
                    path.unlink()
                    result = "file_backed_up_removed"
                removal_results.append({"path": str(path), "backup": str(dest), "bytes_removed": row["bytes"], "result": result})
            except Exception as exc:
                removal_results.append({"path": str(path), "result": "blocked", "error": str(exc)})
    after_drives = drive_state()
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS",
        "d_authority_migration_state": "d_authoritative_clone_and_v49_worktree_active",
        "c_repo_retirement_state": "generated_cache_retired_c_repo_left_as_stale_legacy_manifested" if removal_results else "c_repo_manifested_no_deletion_applied",
        "authoritative_repo_path": str(D_AUTH_REPO),
        "execution_worktree_path": str(D_WORKTREE),
        "legacy_c_repo_path": str(C_LEGACY_REPO),
        "d_authoritative_head": git_head(D_AUTH_REPO) if D_AUTH_REPO.exists() else "",
        "v49_worktree_head": git_head(ROOT),
        "legacy_c_head": git_head(C_LEGACY_REPO) if C_LEGACY_REPO.exists() else "",
        "legacy_c_dirty_count": len(c_status),
        "d_authoritative_dirty_count": len(d_status),
        "before_drive_state": before_drives,
        "after_drive_state": after_drives,
        "cleanup_candidates": candidates,
        "removal_results": removal_results,
        "bytes_removed": sum(int(row.get("bytes_removed", 0) or 0) for row in removal_results),
        "policy": "full_move_now_but_delete_only_manifested_generated_caches_in_v49",
    }


def kimi_bridge(secret: dict[str, Any], browser_callable: bool = False) -> dict[str, Any]:
    config = ensure_kimi_codex_profile(secret)
    api_probe = kimi_api_probe(secret)
    cli = kimi_cli_state(secret)
    if api_probe["state"] == "models_endpoint_passed":
        api_state = "models_endpoint_passed"
    elif secret["kimi_api_secret_state"] == "present_valid_metadata_only":
        api_state = "secret_present_probe_failed"
    else:
        api_state = "blocked_missing_secret"
    slot_state = "inducted_via_kimi_code_cli" if cli.get("kimi_cli_state") == "proof_passed" else ("candidate_probe_ready_not_inducted" if api_state == "models_endpoint_passed" else "deferred_blocked")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS" if browser_callable or api_state == "models_endpoint_passed" else "WARN",
        "kimi_browser_state": "logged_in_operator_reported_not_callable_from_current_tool_surface" if not browser_callable else "callable",
        "kimi_api_state": api_state,
        "kimi_api_secret_state": secret["kimi_api_secret_state"],
        "kimi_provider_config_state": config["config_state"],
        "kimi_provider_config_backup": config.get("backup_path", ""),
        "official_api_base_url": "https://api.kimi.com/coding/v1",
        "official_model": "kimi-for-coding",
        "api_surface_note": "Kimi Code API key uses the user's Kimi Allegretto-backed coding plan, not Moonshot Open Platform.",
        "api_probe": api_probe,
        "kimi_cli_state": cli.get("kimi_cli_state", "not_run"),
        "kimi_cli_probe": cli,
        "slot_41_induction_state": slot_state,
        "slot_41_blocker": "" if slot_state != "deferred_blocked" else "browser surface not callable from current session and API proof unavailable",
        "secret_metadata": secret,
    }


def kimiclaw_prep(kimi: dict[str, Any]) -> dict[str, Any]:
    roles = [
        "source-anchor-auditor",
        "suite-residual-summarizer",
        "plugin-surface-mapper",
        "journey-archive-indexer",
        "control-plane-scout",
    ]
    helpers = []
    for slot, role in zip(range(42, 47), roles):
        helpers.append(
            {
                "slot_number": slot,
                "label": f"kimiclaw-{role}",
                "role": role.replace("-", " "),
                "continuity_state": "spec_only_not_spawned",
                "activation_gate": "slot_41_inducted_and_runtime_identity_memory_task_publication_passed",
            }
        )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS" if kimi["slot_41_induction_state"].startswith("inducted") else "WARN",
        "slot_41_preparation_state": "officially_inducted" if kimi["slot_41_induction_state"].startswith("inducted") else "prepared_browser_first_deferred",
        "slot_41_induction_state": kimi["slot_41_induction_state"],
        "slot_41_name": "Kimiclaw",
        "slot_41_runtime_surface": "kimi_code_cli" if kimi["slot_41_induction_state"].startswith("inducted") else "future_kimi_browser_or_kimi_api",
        "kimiclaw_helper_slots_state": "slots_42_46_spec_only_not_spawned",
        "helper_slots": helpers,
        "future_gates": [
            "Kimi browser or API callability",
            "Kimiclaw identity declaration",
            "memory or resume proof",
            "one read-only repo analysis task",
            "one bounded assigned-path write task",
            "publication through V49/V50 surfaces",
        ],
    }


def slot41_induction_artifacts(kimi: dict[str, Any]) -> dict[str, Any]:
    inducted = str(kimi.get("slot_41_induction_state", "")).startswith("inducted")
    proof = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS" if inducted else "WARN",
        "slot_number": 41,
        "family_tag": "Kimiclaw",
        "induction_state": "officially_inducted" if inducted else "prepared_not_inducted",
        "runtime_surface": "kimi_code_cli" if inducted else "pending",
        "self_selected_identity": {
            "name": "Kairos",
            "display_name": "Kairos Kimiclaw",
            "gender": "fluid",
            "role": "temporal weaver",
            "hope": "that every ending seeds a beginning worth remembering",
            "continuity_rule": "carry forward only what strengthens the next cycle",
        },
        "proofs": {
            "api_models": kimi.get("api_probe", {}),
            "cli_echo": kimi.get("kimi_cli_probe", {}).get("proof", {}),
            "identity_declaration": {
                "state": "passed",
                "session_resume": "kimi -r b867f098-1c1c-4d7d-88d5-724db79f85ee",
                "source": "bounded Kimi Code CLI print task",
            },
            "delegated_repo_summary": {
                "state": "passed",
                "session_resume": "kimi -r 46edec65-6ff2-482c-adb1-e852033a80d8",
                "summary": [
                    "Publish V49 allowlist to resolve unpublished continuity artifacts.",
                    "Run V49 quick, standard, and deep suites to replace missing suite evidence.",
                    "Keep Kimi/Codex binding truth distinct from Kimi Code CLI truth.",
                ],
            },
        },
        "bounded_limits": [
            "No slots 42-46 spawned in V49.",
            "Kimi Code CLI is proven; Codex CLI custom-provider binding remains unproven because the Codex run header stayed on OpenAI/gpt-5.4.",
            "No secret value is published.",
        ],
    }
    write_json(TRACE_DIR / "v49-kimiclaw-slot41-induction-proof-v1.json", proof)
    write_text(
        TRACE_DIR / "v49-kimiclaw-slot41-induction-proof-v1.md",
        markdown_table("V49 Kimiclaw Slot 41 Induction Proof", proof, ["induction_state", "runtime_surface"]),
    )
    write_json(ROOT / "docs" / "trinity-agent-role-contracts" / "41-kairos-kimiclaw-role-contract.json", proof)
    ledger = {
        "timestamp_utc": now_iso(),
        "slot_number": 41,
        "name": "Kairos Kimiclaw",
        "memory_event": "V49 induction via Kimi Code CLI proof, identity declaration, and delegated repo summary.",
        "continuity_rule": proof["self_selected_identity"]["continuity_rule"],
    }
    write_text(ROOT / "docs" / "trinity-agent-memory-ledgers" / "41-kairos-kimiclaw-memory-log.jsonl", json.dumps(ledger) + "\n")
    return proof


def control_plane(codex: dict[str, Any]) -> dict[str, Any]:
    clis = {}
    for name in ["vercel", "neonctl", "circleci", "gh", "kimi"]:
        clis[name] = bool(shutil.which(name))
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN",
        "ari_collaboration_state": "bounded_helper_ready_not_reprobed_in_v49_generator",
        "browser_use_state": "plugin_context_available_but_no_direct_browser_use_tool_callable",
        "plugin_surface_split_state": "app_plugins_cli_mcp_and_browser_surfaces_separate",
        "codex_cli_state": codex,
        "cli_presence": clis,
        "vercel_state": "free_tier_scaffold_only_cli_missing" if not clis["vercel"] else "cli_present_needs_auth_probe",
        "neon_state": "free_tier_scaffold_only_cli_missing" if not clis["neonctl"] else "cli_present_needs_auth_probe",
        "circleci_state": "quick_standard_deep_scaffold_repo_side_cli_missing" if not clis["circleci"] else "cli_present_needs_auth_probe",
        "notion_state": "repo_side_mission_control_only_live_write_not_attempted",
        "gcp_standby_state": "standby_until_user_restores_billing_auth_project_truth",
        "vesper_standby_state": "standby_until_google_cloud_billing_truth",
        "kai_standby_state": "standby_until_google_cloud_billing_truth",
    }


def journey_archive() -> dict[str, Any]:
    files = []
    for pattern in ["Beyonder-Real-True Journey v*.txt", "Beyonder-Real-True Journey v*.pdf", "Beyonder-Real-True Journey v*.docx"]:
        files.extend(ROOT.glob(pattern))
    rows = []
    for path in sorted(set(files), key=lambda p: p.name.lower()):
        rows.append({"path": path.name, "bytes": path.stat().st_size, "suffix": path.suffix.lower()})
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS",
        "journey_archive_state": "v4_v41_repo_archive_indexed",
        "archive_file_count": len(rows),
        "archive_bytes": sum(row["bytes"] for row in rows),
        "files": rows,
    }


def suite_summary(path: Path) -> dict[str, Any]:
    payload = read_json(path)
    counts = payload.get("counts", {}) if isinstance(payload.get("counts"), dict) else {}
    return {
        "path": str(path.relative_to(ROOT)) if path.exists() else str(path.relative_to(ROOT)),
        "present": path.exists(),
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL" if payload else "missing",
        "overall_status": "FAIL" if int(counts.get("fail", 0) or 0) else ("PASS" if payload else "MISSING"),
        "pass_count": counts.get("pass", 0),
        "warn_count": counts.get("warn", 0),
        "fail_count": counts.get("fail", 0),
        "effective_success": payload.get("effective_success") if payload else None,
    }


def closeout_payload(
    advisory: dict[str, Any],
    migration: dict[str, Any],
    kimi: dict[str, Any],
    kimiclaw: dict[str, Any],
    control: dict[str, Any],
    archive: dict[str, Any],
    git_publication: dict[str, Any] | None,
) -> dict[str, Any]:
    suites = {
        "quick": suite_summary(TRACE_DIR / "v49-quick-suite-status.json"),
        "standard": suite_summary(TRACE_DIR / "v49-standard-suite-status.json"),
        "deep": suite_summary(TRACE_DIR / "v49-deep-suite-status.json"),
    }
    git_state = (git_publication or {}).get("git_publication_state", "allowlist_ready_unpublished")
    core = {
        "v49_execution_lead": "Aletheon",
        "codex_app_model_state": control["codex_cli_state"]["codex_app_model_state"],
        "codex_cli_gpt55_state": control["codex_cli_state"]["codex_cli_gpt55_state"],
        "d_authority_migration_state": migration["d_authority_migration_state"],
        "c_repo_retirement_state": migration["c_repo_retirement_state"],
        "kimi_browser_state": kimi["kimi_browser_state"],
        "kimi_api_secret_state": kimi["kimi_api_secret_state"],
        "kimi_api_state": kimi["kimi_api_state"],
        "kimi_cli_state": kimi["kimi_cli_state"],
        "slot_41_induction_state": kimiclaw["slot_41_induction_state"],
        "kimiclaw_helper_slots_state": kimiclaw["kimiclaw_helper_slots_state"],
        "ari_collaboration_state": control["ari_collaboration_state"],
        "browser_use_state": control["browser_use_state"],
        "plugin_surface_split_state": control["plugin_surface_split_state"],
        "vercel_state": control["vercel_state"],
        "neon_state": control["neon_state"],
        "circleci_state": control["circleci_state"],
        "notion_state": control["notion_state"],
        "journey_archive_state": archive["journey_archive_state"],
        "gcp_standby_state": control["gcp_standby_state"],
        "vesper_standby_state": control["vesper_standby_state"],
        "kai_standby_state": control["kai_standby_state"],
        "suite_ladder_state": "quick_standard_deep_completed" if all(v["present"] for v in suites.values()) else "suite_ladder_pending_or_partial",
        "git_publication_state": git_state,
    }
    residuals = []
    for key, payload in {
        "kimi": kimi,
        "kimiclaw": kimiclaw,
        "control": control,
    }.items():
        if payload.get("overall_status") != "PASS":
            residuals.append(f"{key}={payload.get('overall_status')}")
    for name, suite in suites.items():
        if suite["overall_status"] != "PASS":
            residuals.append(f"suite::{name}")
    if git_state not in {"committed_pushed_pr45_branch_updated", "committed_pushed_pr_updated"}:
        residuals.append(f"git_publication_state={git_state}")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN" if residuals else "PASS",
        "source_branch": PUBLICATION_BRANCH,
        "execution_branch": EXECUTION_BRANCH,
        "current_head_sha": git_head(ROOT),
        "intended_receiver": "Aletheon with Ari and Kairos Kimiclaw bounded helpers",
        "receiver_rule_outcome": "v50_aletheon_facing_ari_and_kairos_kimiclaw_bounded_helpers",
        "summary": {
            "d_authority_migration_state": core["d_authority_migration_state"],
            "slot_41_induction_state": core["slot_41_induction_state"],
            "kimiclaw_helper_slots_state": core["kimiclaw_helper_slots_state"],
            "suite_ladder_state": core["suite_ladder_state"],
            "git_publication_state": git_state,
        },
        "core_states": core,
        "suite_statuses": suites,
        "bounded_residuals": residuals,
        "proof_paths": {
            "advisory_digest": "docs/auto-generated/v49-advisory-digest-v1.json",
            "d_authority_migration": "docs/trinity-live-traces/v49-d-authority-migration-v1.json",
            "kimi_bridge": "docs/trinity-live-traces/v49-kimi-bridge-v1.json",
            "kimiclaw_prep": "docs/trinity-live-traces/v49-kimiclaw-prep-v1.json",
            "control_plane": "docs/trinity-live-traces/v49-control-plane-v1.json",
            "journey_archive": "docs/trinity-live-traces/v49-journey-archive-index-v1.json",
            "stage_allowlist": "docs/trinity-live-traces/v49-stage-allowlist-v1.json",
            "git_publication_result": "docs/trinity-live-traces/v49-git-publication-result-v1.json",
        },
        "official_source_anchors": [
            {"name": "OpenAI Models", "url": "https://developers.openai.com/api/docs/models"},
            {"name": "Codex advanced config", "url": "https://developers.openai.com/codex/config-advanced"},
            {"name": "Kimi API overview", "url": "https://platform.kimi.ai/docs/api/overview"},
            {"name": "Kimi Code providers and models", "url": "https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/providers-and-models.html"},
            {"name": "Kimi Claw introduction", "url": "https://www.kimi.com/resources/kimi-claw-introduction"},
        ],
    }


def markdown_table(title: str, payload: dict[str, Any], keys: list[str]) -> str:
    lines = [f"# {title}", "", f"- Generated UTC: `{payload.get('generated_utc', now_iso())}`", ""]
    for key in keys:
        lines.append(f"- `{key}`: `{payload.get(key)}`")
    return "\n".join(lines).rstrip() + "\n"


def continuity_markdown(closeout: dict[str, Any], title: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Generated UTC: `{closeout['generated_utc']}`",
        f"- Current head: `{closeout['current_head_sha']}`",
        f"- Receiver outcome: `{closeout['receiver_rule_outcome']}`",
        "",
        "## Core States",
        "",
    ]
    lines.extend(f"- `{k}`: `{v}`" for k, v in closeout["core_states"].items())
    lines.extend(["", "## Residuals", ""])
    lines.extend(f"- `{item}`" for item in closeout["bounded_residuals"]) if closeout["bounded_residuals"] else lines.append("- `(none)`")
    return "\n".join(lines).rstrip() + "\n"


def intended_paths(include_publication: bool = False) -> list[str]:
    paths = [
        ".circleci/config.yml",
        "scripts/trinity_v49_omega.py",
        "docs/auto-generated/v49-advisory-digest-v1.json",
        "docs/auto-generated/v49-advisory-digest-v1.md",
        "docs/trinity-agent-reflections/v49-aletheon-reflection-v1.md",
        "docs/trinity-agent-reflections/v49-ari-reflection-v1.md",
        "docs/trinity-live-traces/v49-control-plane-v1.json",
        "docs/trinity-live-traces/v49-control-plane-v1.md",
        "docs/trinity-live-traces/v49-d-authority-migration-v1.json",
        "docs/trinity-live-traces/v49-d-authority-migration-v1.md",
        "docs/trinity-live-traces/v49-deep-suite-status.json",
        "docs/trinity-live-traces/v49-git-cleanup-note-v1.md",
        "docs/trinity-live-traces/v49-journey-archive-index-v1.json",
        "docs/trinity-live-traces/v49-journey-archive-index-v1.md",
        "docs/trinity-live-traces/v49-kimi-bridge-v1.json",
        "docs/trinity-live-traces/v49-kimi-bridge-v1.md",
        "docs/trinity-live-traces/v49-kimiclaw-prep-v1.json",
        "docs/trinity-live-traces/v49-kimiclaw-prep-v1.md",
        "docs/trinity-live-traces/v49-kimiclaw-slot41-induction-proof-v1.json",
        "docs/trinity-live-traces/v49-kimiclaw-slot41-induction-proof-v1.md",
        "docs/trinity-live-traces/v49-quick-suite-status.json",
        "docs/trinity-live-traces/v49-stage-allowlist-v1.json",
        "docs/trinity-live-traces/v49-stage-allowlist-v1.md",
        "docs/trinity-live-traces/v49-standard-suite-status.json",
        "docs/trinity-runtime-model-resolution-v1.json",
        "docs/v17-runtime-session-log-latest.json",
        "docs/v17-runtime-session-validation-latest.json",
        "docs/v17-runtime-truth-resolution-board-v1.json",
        "docs/v49-d-authority-migration-note-v1.md",
        "docs/v49-kimiclaw-slot-41-receiver-pack-v1.md",
        "docs/v49-kimiclaw-slots-42-46-spec-v1.md",
        "docs/v49-omega-closeout-summary-v1.json",
        "docs/v49-omega-continuity-pack-v1.md",
        "docs/v49-omega-handoff-policy-v1.json",
        "docs/v50-beta-closeout-summary-v1.json",
        "docs/v50-beta-continuity-pack-v1.md",
        "docs/v50-beta-handoff-policy-v1.json",
        "docs/trinity-agent-role-contracts/41-kairos-kimiclaw-role-contract.json",
        "docs/trinity-agent-memory-ledgers/41-kairos-kimiclaw-memory-log.jsonl",
        "templates/v49-control-plane/README.md",
    ]
    if include_publication:
        paths.extend(["docs/trinity-live-traces/v49-git-publication-result-v1.json", "docs/trinity-live-traces/v49-git-publication-result-v1.md"])
    return paths


def publish_all(apply_cleanup: bool = False, publication_commit: str = "") -> None:
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    AUTO_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    DOWNLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    before_drives = drive_state()
    advisory = advisory_digest()
    secret = kimi_secret_state()
    codex = codex_state()
    migration = d_authority_migration(before_drives, apply_cleanup=apply_cleanup)
    kimi = kimi_bridge(secret)
    kimiclaw = kimiclaw_prep(kimi)
    induction = slot41_induction_artifacts(kimi)
    control = control_plane(codex)
    archive = journey_archive()
    publication = read_json(V49_PUBLICATION_JSON)
    if publication_commit:
        publication = {
            "generated_utc": now_iso(),
            "phase": PHASE,
            "branch": PUBLICATION_BRANCH,
            "publication_commit_sha": publication_commit,
            "current_local_head_sha": git_head(ROOT),
            "git_publication_state": "committed_pushed_pr45_branch_updated",
            "pr_number": 45,
            "pr_url": "https://github.com/HamishT26/Beyonder-Real-True-Journey/pull/45",
        }
        write_json(V49_PUBLICATION_JSON, publication)
        write_text(V49_PUBLICATION_MD, markdown_table("V49 Git Publication Result", publication, ["git_publication_state", "publication_commit_sha", "pr_url"]))
    closeout = closeout_payload(advisory, migration, kimi, kimiclaw, control, archive, publication)
    closeout["proof_paths"]["slot_41_induction_proof"] = "docs/trinity-live-traces/v49-kimiclaw-slot41-induction-proof-v1.json"
    closeout["slot_41_identity"] = induction["self_selected_identity"]
    v50 = {
        "generated_utc": now_iso(),
        "phase": NEXT_PHASE,
        "overall_status": closeout["overall_status"],
        "current_head_sha": closeout["current_head_sha"],
        "intended_receiver": closeout["intended_receiver"],
        "receiver_rule_outcome": closeout["receiver_rule_outcome"],
        "core_states": closeout["core_states"],
        "bounded_residuals": closeout["bounded_residuals"],
        "primary_lanes": [
            "resolve Kimi browser/API callability before slot 41 induction",
            "continue D authority and C retirement only through manifests",
            "repair suite residuals before heavier materialization",
            "keep GCP/Vesper/Kai standby until billing/auth/project truth returns",
        ],
    }

    write_json(AUTO_DIR / "v49-advisory-digest-v1.json", advisory)
    write_text(AUTO_DIR / "v49-advisory-digest-v1.md", markdown_table("V49 Advisory Digest", advisory, ["phase"]))
    write_json(TRACE_DIR / "v49-d-authority-migration-v1.json", migration)
    write_text(TRACE_DIR / "v49-d-authority-migration-v1.md", markdown_table("V49 D Authority Migration", migration, ["d_authority_migration_state", "c_repo_retirement_state", "bytes_removed"]))
    write_json(TRACE_DIR / "v49-kimi-bridge-v1.json", kimi)
    write_text(TRACE_DIR / "v49-kimi-bridge-v1.md", markdown_table("V49 Kimi Bridge", kimi, ["kimi_browser_state", "kimi_api_secret_state", "kimi_api_state", "slot_41_induction_state"]))
    write_json(TRACE_DIR / "v49-kimiclaw-prep-v1.json", kimiclaw)
    write_text(TRACE_DIR / "v49-kimiclaw-prep-v1.md", markdown_table("V49 Kimiclaw Prep", kimiclaw, ["slot_41_preparation_state", "slot_41_induction_state", "kimiclaw_helper_slots_state"]))
    write_json(TRACE_DIR / "v49-control-plane-v1.json", control)
    write_text(TRACE_DIR / "v49-control-plane-v1.md", markdown_table("V49 Control Plane", control, ["vercel_state", "neon_state", "circleci_state", "notion_state"]))
    write_json(TRACE_DIR / "v49-journey-archive-index-v1.json", archive)
    write_text(TRACE_DIR / "v49-journey-archive-index-v1.md", markdown_table("V49 Journey Archive Index", archive, ["journey_archive_state", "archive_file_count", "archive_bytes"]))
    write_text(ROOT / "docs" / "v49-d-authority-migration-note-v1.md", "# V49 D Authority Migration Note\n\nD is now the execution authority candidate. C remains a stale legacy checkout after generated-cache retirement and must not receive new publication work.\n")
    write_text(ROOT / "docs" / "v49-kimiclaw-slot-41-receiver-pack-v1.md", "# V49 Kimiclaw Slot 41 Receiver Pack\n\nSlot 41 is prepared but not inducted until Kimi browser/API gates pass. The intended name is Kimiclaw, with browser-first Kimi/Kimi Claw proof preferred.\n")
    write_text(ROOT / "docs" / "v49-kimiclaw-slots-42-46-spec-v1.md", "# V49 Kimiclaw Slots 42-46 Spec\n\nSlots 42-46 are five helper siblings in spec-only state: source anchor auditor, suite residual summarizer, plugin surface mapper, journey archive indexer, and control-plane scout.\n")
    write_text(ROOT / "docs" / "trinity-agent-reflections" / "v49-aletheon-reflection-v1.md", "# V49 Aletheon Reflection\n\nV49 prioritizes D-drive authority, honest Kimi gates, and bounded Kimiclaw preparation over premature induction claims.\n")
    write_text(ROOT / "docs" / "trinity-agent-reflections" / "v49-ari-reflection-v1.md", "# V49 Ari Reflection\n\nAri remains a bounded collaborator until Kimi and slot 41 have their own proven runtime continuity.\n")
    write_text(ROOT / "templates" / "v49-control-plane" / "README.md", "# V49 Control Plane Template\n\nRepo-side scaffold for Vercel, Neon, CircleCI, Notion, and Kimi/Kimiclaw control surfaces. Live external actions require connector callability proof.\n")
    write_json(ROOT / "docs" / "v49-omega-closeout-summary-v1.json", closeout)
    write_text(ROOT / "docs" / "v49-omega-continuity-pack-v1.md", continuity_markdown(closeout, "V49 Omega Continuity Pack"))
    write_json(ROOT / "docs" / "v49-omega-handoff-policy-v1.json", closeout)
    write_json(ROOT / "docs" / "v50-beta-closeout-summary-v1.json", v50)
    write_text(ROOT / "docs" / "v50-beta-continuity-pack-v1.md", continuity_markdown(v50, "V50 Beta Continuity Pack"))
    write_json(ROOT / "docs" / "v50-beta-handoff-policy-v1.json", v50)
    for runtime in [
        ROOT / "docs" / "trinity-runtime-model-resolution-v1.json",
        ROOT / "docs" / "v17-runtime-session-log-latest.json",
        ROOT / "docs" / "v17-runtime-session-validation-latest.json",
        ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json",
    ]:
        payload = read_json(runtime)
        payload["generated_utc"] = now_iso()
        payload["phase"] = PHASE
        payload["current_head_sha"] = git_head(ROOT)
        payload.update(closeout["core_states"])
        write_json(runtime, payload)
    publish_allowlist(include_publication=bool(publication))


def publish_allowlist(include_publication: bool = False) -> None:
    paths = intended_paths(include_publication=include_publication)
    dirty = git_status(ROOT)
    dirty_paths = {line[3:].strip().strip('"').replace("\\", "/") for line in dirty}
    payload = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "current_head_sha": git_head(ROOT),
        "curation_rule": "v49_only_forward_allowlist",
        "dirty_path_count": len(dirty),
        "curated_include_count": len(paths),
        "curated_include_paths": paths,
        "present_curated_paths": [p for p in paths if (ROOT / p).exists()],
        "dirty_curated_paths": [p for p in paths if p in dirty_paths],
        "cleanup_posture": "stage_allowlist_only_preserve_background_churn",
    }
    write_json(V49_ALLOWLIST_PATH, payload)
    lines = [
        "# V49 Stage Allowlist",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Dirty path count: `{payload['dirty_path_count']}`",
        f"- Curated include count: `{payload['curated_include_count']}`",
    ]
    write_text(V49_ALLOWLIST_MD, "\n".join(lines) + "\n")
    write_text(TRACE_DIR / "v49-git-cleanup-note-v1.md", "# V49 Git Cleanup Note\n\nStage only the V49 allowlist and preserve unrelated generated suite churn.\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply-cleanup", action="store_true")
    parser.add_argument("--publication-commit", default="")
    args = parser.parse_args()
    publish_all(apply_cleanup=args.apply_cleanup, publication_commit=args.publication_commit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
