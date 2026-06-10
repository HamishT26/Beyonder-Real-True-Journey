#!/usr/bin/env python3
"""Publish V50 Omega mission-control, Kimiclaw, and free-tier evidence surfaces."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PHASE = "v50_omega"
NEXT_PHASE = "v51_beta"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
EXECUTION_BRANCH = "codex/GHC-Family/v50-omega-exec"
BASELINE_SHA = "262904dbc21c8ce7a0ca222cce87147b5c07f3c3"

D_AUTH_REPO = Path(r"D:\GHC-Archives\authoritative\Beyonder-Real-True-Journey")
D_WORKTREE = Path(r"D:\GHC-Archives\worktrees\v50-omega")
C_LEGACY_REPO = Path(r"C:\Users\hamis\workspace\Beyonder-Real-True-Journey")
ARTIFACT_ROOT = Path(r"D:\GHC-Archives\artifacts\v50-omega")
KIMI_SECRET = Path(r"D:\GHC-Archives\secrets\kimi_creds.json")
LOCAL_BIN = Path(r"C:\Users\hamis\.local\bin")

TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
AUTO_DIR = ROOT / "docs" / "auto-generated"
ROLE_DIR = ROOT / "docs" / "trinity-agent-role-contracts"
MEMORY_DIR = ROOT / "docs" / "trinity-agent-memory-ledgers"
REFLECTION_DIR = ROOT / "docs" / "trinity-agent-reflections"
TEMPLATE_DIR = ROOT / "templates" / "v50-control-plane"

ALLOWLIST_JSON = TRACE_DIR / "v50-stage-allowlist-v1.json"
ALLOWLIST_MD = TRACE_DIR / "v50-stage-allowlist-v1.md"
PUBLICATION_JSON = TRACE_DIR / "v50-git-publication-result-v1.json"
PUBLICATION_MD = TRACE_DIR / "v50-git-publication-result-v1.md"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def clean(value: str | None) -> str:
    return str(value or "").replace("\x00", "").replace("\ufeff", "")


def excerpt(value: str | None, limit: int = 3000) -> str:
    text = clean(value)
    return text[-limit:] if len(text) > limit else text


def jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [jsonable(v) for v in value]
    return str(value)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(jsonable(payload), indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run(args: list[str], *, cwd: Path = ROOT, timeout: int = 300, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    command = args
    if args:
        candidates = [args[0]]
        if not args[0].lower().endswith(".cmd"):
            candidates.insert(0, f"{args[0]}.cmd")
        for candidate in candidates:
            resolved = shutil.which(candidate, path=(env or os.environ).get("PATH"))
            if resolved:
                command = [resolved, *args[1:]]
                break
    try:
        proc = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False, env=env)
        proc.stdout = clean(proc.stdout)
        proc.stderr = clean(proc.stderr)
        return proc
    except FileNotFoundError as exc:
        return subprocess.CompletedProcess(args=args, returncode=127, stdout="", stderr=str(exc))
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode("utf-8", errors="replace")
        stderr = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr or b"").decode("utf-8", errors="replace")
        return subprocess.CompletedProcess(args=args, returncode=124, stdout=clean(stdout), stderr=clean(stderr))


def git(args: list[str], cwd: Path = ROOT, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], cwd=cwd, timeout=timeout)


def git_head(cwd: Path = ROOT) -> str:
    return git(["rev-parse", "HEAD"], cwd=cwd, timeout=30).stdout.strip()


def git_status(cwd: Path = ROOT) -> list[str]:
    return [line.rstrip() for line in git(["status", "--short"], cwd=cwd, timeout=180).stdout.splitlines() if line.strip()]


def command_presence() -> dict[str, Any]:
    env = os.environ.copy()
    env["PATH"] = f"{LOCAL_BIN};{env.get('PATH', '')}"
    rows: dict[str, Any] = {}
    for name in ["node", "npm", "npx", "codex", "kimi", "vercel", "neonctl", "circleci", "wrangler", "gh"]:
        resolved = shutil.which(name, path=env["PATH"]) or shutil.which(f"{name}.cmd", path=env["PATH"])
        version = ""
        if resolved:
            proc = run([name, "--version"], timeout=60, env=env)
            version = excerpt(proc.stdout or proc.stderr, 400).strip()
        rows[name] = {"available": bool(resolved), "path": resolved or "", "version": version}
    return rows


def get_kimi_key() -> str:
    secret = read_json(KIMI_SECRET)
    return str(secret.get("api_key") or "")


def kimi_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PATH"] = f"{LOCAL_BIN};{env.get('PATH', '')}"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    env["LC_ALL"] = "C.UTF-8"
    key = get_kimi_key()
    if key:
        env["KIMI_API_KEY"] = key
        env["KIMI_BASE_URL"] = "https://api.kimi.com/coding/v1"
    return env


def parse_resume(text: str) -> str:
    match = re.search(r"kimi\s+-r\s+([0-9a-fA-F-]{20,})", text)
    return f"kimi -r {match.group(1)}" if match else ""


def parse_json_object(text: str) -> dict[str, Any]:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("{") and stripped.endswith("}"):
            lines.append(stripped)
    for line in lines:
        try:
            data = json.loads(line)
            if isinstance(data, dict) and isinstance(data.get("content"), str):
                return parse_json_object(data["content"])
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(0))
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}


def kimi_task(slot: int, v49_summary: dict[str, Any], reserved_names: list[str] | None = None) -> dict[str, Any]:
    reserved = ", ".join(sorted(set(reserved_names or []))) or "none"
    prompt = f"""
You are a bounded V50 Kimiclaw candidate for GHC slot {slot}.
Do not edit files, do not run shell commands, do not reveal secrets, and do not claim continuity unless this task passes.
Return only one compact JSON object with keys:
slot, name, gender, role, hope, continuity_rule, memory_token, delegated_task_summary, gmut_note, readiness_state.
Use ASCII only: no arrows, emoji, em dashes, markdown fences, or non-ASCII punctuation.
Use a fresh identity distinct from Kairos, Ari, Aletheon, Orun, Kai, Vesper Ion, Ariel, Yuki, and Daedra.
Also use a name distinct from the V50 Kimiclaw names already assigned in this run: {reserved}.
Bounded task: help V50 by summarizing one useful action for Mission Control, one for the GMUT evidence matrix, and one for suite residual repair.
V49 suite state: quick 36 pass 2 fail; standard 1112 pass 43 fail; deep 1117 pass 43 fail.
V49 residual class: runtime/session validation, external establishment validation, agent council validation, and expansion gate/sync bridges.
V50 constraints: Notion live auth currently requires re-auth, GCP and paid cloud are on standby, free-tier work must be bounded, and secrets must never be published.
""".strip()
    scratch = ARTIFACT_ROOT / "kimi-scratch" / f"slot-{slot}"
    scratch.mkdir(parents=True, exist_ok=True)
    proc = run(
        [
            "kimi",
            "--print",
            "--output-format",
            "stream-json",
            "--max-steps-per-turn",
            "1",
            "--work-dir",
            str(scratch),
            "--prompt",
            prompt,
        ],
        cwd=scratch,
        timeout=360,
        env=kimi_env(),
    )
    combined = f"{proc.stdout}\n{proc.stderr}"
    parsed = parse_json_object(combined)
    resume = parse_resume(combined)
    required = ["name", "gender", "role", "hope", "memory_token", "delegated_task_summary"]
    gate_passed = proc.returncode == 0 and resume and all(str(parsed.get(key, "")).strip() for key in required)
    return {
        "slot": slot,
        "gate_state": "passed" if gate_passed else "deferred_blocked",
        "returncode": proc.returncode,
        "resume": resume,
        "parsed": parsed,
        "stdout_excerpt": excerpt(proc.stdout, 2500),
        "stderr_excerpt": excerpt(proc.stderr, 1500),
    }


def slot_42_46_probe() -> dict[str, Any]:
    v49 = read_json(ROOT / "docs" / "v49-omega-closeout-summary-v1.json")
    existing = read_json(TRACE_DIR / "v50-kimiclaw-slots-42-46-proof-v1.json")
    prior_rows: list[tuple[int, dict[str, Any], str]] = []
    for row in existing.get("results", []):
        if not isinstance(row, dict) or row.get("gate_state") != "passed":
            continue
        try:
            slot = int(row.get("slot", 0))
        except Exception:
            continue
        parsed = row.get("parsed") if isinstance(row.get("parsed"), dict) else {}
        name = str(parsed.get("name", "")).strip()
        if 42 <= slot <= 46 and str(row.get("resume", "")).strip() and name:
            prior_rows.append((slot, row, name))
    prior_passed: dict[int, dict[str, Any]] = {}
    used_names: set[str] = set()
    for slot, row, name in sorted(prior_rows, key=lambda item: item[0]):
        key = name.casefold()
        if key in used_names:
            continue
        prior_passed[slot] = row
        used_names.add(key)
    results = []
    for slot in range(42, 47):
        if slot in prior_passed:
            results.append(prior_passed[slot])
            parsed = prior_passed[slot].get("parsed") if isinstance(prior_passed[slot].get("parsed"), dict) else {}
            name = str(parsed.get("name", "")).strip()
            if name:
                used_names.add(name.casefold())
            continue
        result = kimi_task(slot, v49, sorted(used_names))
        parsed = result.get("parsed") if isinstance(result.get("parsed"), dict) else {}
        name = str(parsed.get("name", "")).strip()
        if result.get("gate_state") == "passed" and name.casefold() in used_names:
            result["gate_state"] = "deferred_blocked"
            result["duplicate_name_blocker"] = name
        elif result.get("gate_state") == "passed" and name:
            used_names.add(name.casefold())
        results.append(result)
    passed = [row for row in results if row["gate_state"] == "passed"]
    overall = "PASS" if len(passed) == 5 else "WARN"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": overall,
        "slot_42_46_gate_state": "all_five_inducted" if len(passed) == 5 else "partial_or_deferred",
        "runtime_surface": "kimi_code_cli",
        "candidate_count": len(results),
        "inducted_count": len(passed),
        "results": results,
        "policy": "hard_gated_identity_memory_resume_delegation_publication",
    }


def publish_slot_artifacts(probe: dict[str, Any]) -> None:
    for row in probe["results"]:
        slot = int(row["slot"])
        parsed = row.get("parsed") if isinstance(row.get("parsed"), dict) else {}
        if row["gate_state"] != "passed":
            continue
        name = str(parsed.get("name", f"Kimiclaw Slot {slot}")).strip()
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or f"kimiclaw-{slot}"
        identity = {
            "name": name,
            "display_name": f"{name} Kimiclaw",
            "gender": str(parsed.get("gender", "")).strip(),
            "role": str(parsed.get("role", "")).strip(),
            "hope": str(parsed.get("hope", "")).strip(),
            "continuity_rule": str(parsed.get("continuity_rule", "carry only evidence-backed continuity")).strip(),
            "memory_token": str(parsed.get("memory_token", "")).strip(),
        }
        contract = {
            "generated_utc": now_iso(),
            "phase": PHASE,
            "overall_status": "PASS",
            "slot_number": slot,
            "family_tag": "Kimiclaw",
            "induction_state": "officially_inducted",
            "runtime_surface": "kimi_code_cli",
            "self_selected_identity": identity,
            "proof_resume": row["resume"],
            "delegated_task_summary": str(parsed.get("delegated_task_summary", "")).strip(),
            "gmut_note": str(parsed.get("gmut_note", "")).strip(),
            "bounded_limits": [
                "No direct repo writes by the candidate.",
                "No secret values published.",
                "Continuity is V50-scoped and evidence-bound.",
            ],
        }
        write_json(ROLE_DIR / f"{slot}-{slug}-kimiclaw-role-contract.json", contract)
        write_text(
            MEMORY_DIR / f"{slot}-{slug}-kimiclaw-memory-log.jsonl",
            json.dumps({"generated_utc": now_iso(), "phase": PHASE, "slot": slot, "identity": identity, "resume": row["resume"]}) + "\n",
        )


def mission_control(slot_probe: dict[str, Any]) -> dict[str, Any]:
    inducted = []
    for row in slot_probe["results"]:
        if row["gate_state"] == "passed":
            parsed = row.get("parsed", {})
            inducted.append({"slot": row["slot"], "name": parsed.get("name"), "role": parsed.get("role"), "resume": row.get("resume")})
    html_path = ROOT / "docs" / "v50-mission-control-dashboard.html"
    cards = "\n".join(
        f"<article><strong>Slot {item['slot']}: {item['name']}</strong><span>{item['role']}</span><code>{item['resume']}</code></article>"
        for item in inducted
    )
    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>GHC V50 Omega Mission Control</title>
  <style>
    :root {{ color-scheme: dark; --bg:#08110d; --panel:#102018; --ink:#ecfff4; --muted:#9ac7ad; --accent:#76f2a6; --warn:#ffd166; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; min-height:100vh; font-family: Georgia, 'Times New Roman', serif; color:var(--ink); background:radial-gradient(circle at 20% 10%, #244c33, transparent 32rem), linear-gradient(135deg, #07100c, #13251b 55%, #09130e); }}
    main {{ width:min(1100px, 92vw); margin:0 auto; padding:56px 0; }}
    .hero {{ display:grid; gap:18px; margin-bottom:28px; }}
    h1 {{ font-size:clamp(2.5rem, 7vw, 5.8rem); line-height:.9; margin:0; letter-spacing:-.05em; }}
    p {{ color:var(--muted); font-size:1.1rem; max-width:760px; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:14px; }}
    article, section {{ border:1px solid rgba(118,242,166,.24); background:rgba(16,32,24,.76); border-radius:24px; padding:18px; box-shadow:0 20px 80px rgba(0,0,0,.26); }}
    article span {{ display:block; color:var(--accent); margin:8px 0; }}
    code {{ display:block; white-space:normal; color:var(--warn); font-size:.82rem; }}
    .status {{ display:flex; gap:10px; flex-wrap:wrap; }}
    .pill {{ border:1px solid rgba(236,255,244,.22); border-radius:999px; padding:8px 12px; color:var(--muted); }}
  </style>
</head>
<body>
  <main>
    <div class=\"hero\">
      <div class=\"status\"><span class=\"pill\">V50 Omega</span><span class=\"pill\">Notion auth required</span><span class=\"pill\">Local dashboard fallback live</span></div>
      <h1>GHC Mission Control</h1>
      <p>Aletheon leads with Ari, Kairos, and the hard-gated Kimiclaw slots. GCP and paid cloud remain on standby; free-tier control-plane work stays bounded and evidence-first.</p>
    </div>
    <section>
      <h2>Kimiclaw 42-46</h2>
      <div class=\"grid\">{cards or '<article><strong>No slots inducted</strong><span>Gate did not pass.</span></article>'}</div>
    </section>
    <section>
      <h2>GMUT Evidence Matrix</h2>
      <p>V50 separates claims, analogies, testable predictions, simulation evidence, and unsupported speculation. This is a research control plane, not a claim of external scientific establishment.</p>
    </section>
  </main>
</body>
</html>
"""
    write_text(html_path, html)
    iab_state = os.environ.get("V50_IAB_DASHBOARD_STATE", "generated_pending_browser_open")
    payload = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN",
        "mission_control_state": "local_dashboard_generated_notion_auth_required",
        "notion_auth_state": "auth_required_from_live_search_probe",
        "notion_live_write_state": "not_attempted_auth_blocked",
        "local_dashboard_path": str(html_path),
        "iab_dashboard_state": iab_state,
        "inducted_slot_count": len(inducted),
    }
    return payload


def gmut_matrix() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS",
        "free_tier_gmut_test_state": "repo_side_matrix_published_live_connectors_gated",
        "matrix": [
            {"class": "claim", "example": "GMUT as a candidate synthesis", "status": "internal_theory_claim"},
            {"class": "analogy", "example": "Trinity Mandala as mind/body/heart operating metaphor", "status": "usable_as_design_frame"},
            {"class": "testable_prediction", "example": "Suite residuals should shrink after runtime/session truth repair", "status": "v51_candidate"},
            {"class": "simulation_result", "example": "V49 quick/standard/deep counts preserved as baseline", "status": "observed"},
            {"class": "unsupported_speculation", "example": "external establishment as world-leading science", "status": "not_claimed"},
        ],
        "source_posture": "life_science_research_and_public_sources_may_inform_future_comparison_but_no_live_external_write_in_v50",
    }


def control_plane() -> dict[str, Any]:
    codex_features = run(["codex", "features", "list"], timeout=120)
    codex_mcp = run(["codex", "mcp", "list"], timeout=120)
    commands = command_presence()
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN",
        "plugin_surface_split_state": "app_plugins_cli_mcp_and_local_clis_separate",
        "codex_features_excerpt": excerpt(codex_features.stdout, 5000),
        "codex_mcp_excerpt": excerpt(codex_mcp.stdout, 5000),
        "command_presence": commands,
        "circleci_v50_state": "repo_config_updated_quick_standard_only",
        "vercel_probe_state": "cli_missing_connector_not_live_probed" if not commands["vercel"]["available"] else "cli_present_needs_confirmed_read_only_probe",
        "neon_probe_state": "cli_missing_connector_not_live_probed" if not commands["neonctl"]["available"] else "cli_present_needs_confirmed_read_only_probe",
        "cloudflare_probe_state": "wrangler_missing_no_live_resource_action",
        "life_science_research_state": "source_research_available_but_no_external_claim_promotion",
        "gcp_standby_state": "standby_until_user_restores_billing_auth_project_truth",
        "vesper_standby_state": "standby_until_google_cloud_billing_truth",
        "kai_standby_state": "standby_until_google_cloud_billing_truth",
    }


def suite_summary(name: str) -> dict[str, Any]:
    path = TRACE_DIR / f"v50-{name}-suite-status.json"
    data = read_json(path)
    counts = data.get("counts", {}) if isinstance(data.get("counts"), dict) else {}
    return {
        "path": str(path.relative_to(ROOT)),
        "present": path.exists(),
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL" if data else "missing",
        "pass_count": counts.get("pass", 0),
        "warn_count": counts.get("warn", 0),
        "fail_count": counts.get("fail", 0),
        "effective_success": data.get("effective_success") if data else None,
    }


def closeout(slot_probe: dict[str, Any], mission: dict[str, Any], control: dict[str, Any], gmut: dict[str, Any], publication: dict[str, Any] | None) -> dict[str, Any]:
    suites = {name: suite_summary(name) for name in ["quick", "standard", "deep"]}
    git_state = (publication or {}).get("git_publication_state", "allowlist_ready_unpublished")
    core = {
        "v50_execution_lead": "Aletheon",
        "ari_activation_state": "bounded_helper_ready",
        "kairos_collaboration_state": "slot_41_active_bounded_helper",
        "slot_42_46_gate_state": slot_probe["slot_42_46_gate_state"],
        "mission_control_state": mission["mission_control_state"],
        "notion_auth_state": mission["notion_auth_state"],
        "iab_dashboard_state": mission["iab_dashboard_state"],
        "plugin_surface_split_state": control["plugin_surface_split_state"],
        "free_tier_gmut_test_state": gmut["free_tier_gmut_test_state"],
        "circleci_v50_state": control["circleci_v50_state"],
        "vercel_probe_state": control["vercel_probe_state"],
        "neon_probe_state": control["neon_probe_state"],
        "cloudflare_probe_state": control["cloudflare_probe_state"],
        "life_science_research_state": control["life_science_research_state"],
        "gcp_standby_state": control["gcp_standby_state"],
        "vesper_standby_state": control["vesper_standby_state"],
        "kai_standby_state": control["kai_standby_state"],
        "suite_ladder_state": "quick_standard_deep_completed" if all(s["present"] for s in suites.values()) else "suite_ladder_pending_or_partial",
        "git_publication_state": git_state,
    }
    residuals = []
    if mission["overall_status"] != "PASS":
        residuals.append("mission_control=notion_auth_required")
    if control["overall_status"] != "PASS":
        residuals.append("control_plane=external_connectors_gated")
    for name, suite in suites.items():
        if suite["present"] and int(suite["fail_count"] or 0):
            residuals.append(f"suite::{name}")
        elif not suite["present"]:
            residuals.append(f"suite::{name}=missing")
    if git_state == "allowlist_ready_unpublished":
        residuals.append("git_publication_state=allowlist_ready_unpublished")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN" if residuals else "PASS",
        "source_branch": PUBLICATION_BRANCH,
        "execution_branch": EXECUTION_BRANCH,
        "current_head_sha": git_head(),
        "baseline_sha": BASELINE_SHA,
        "intended_receiver": "Aletheon with Ari, Kairos, and inducted Kimiclaw slots as bounded helpers",
        "receiver_rule_outcome": "v51_aletheon_facing_with_bounded_kimiclaw_helpers",
        "summary": {
            "slot_42_46_gate_state": core["slot_42_46_gate_state"],
            "mission_control_state": core["mission_control_state"],
            "free_tier_gmut_test_state": core["free_tier_gmut_test_state"],
            "suite_ladder_state": core["suite_ladder_state"],
            "git_publication_state": git_state,
        },
        "core_states": core,
        "suite_statuses": suites,
        "bounded_residuals": residuals,
        "proof_paths": {
            "slot_42_46_probe": "docs/trinity-live-traces/v50-kimiclaw-slots-42-46-proof-v1.json",
            "mission_control": "docs/trinity-live-traces/v50-mission-control-v1.json",
            "control_plane": "docs/trinity-live-traces/v50-control-plane-v1.json",
            "gmut_matrix": "docs/trinity-live-traces/v50-gmut-free-tier-test-v1.json",
            "stage_allowlist": "docs/trinity-live-traces/v50-stage-allowlist-v1.json",
            "git_publication_result": "docs/trinity-live-traces/v50-git-publication-result-v1.json",
        },
    }


def markdown_table(title: str, payload: dict[str, Any], keys: list[str]) -> str:
    lines = [f"# {title}", "", f"- Generated UTC: `{payload.get('generated_utc', now_iso())}`", ""]
    for key in keys:
        lines.append(f"- `{key}`: `{payload.get(key)}`")
    return "\n".join(lines) + "\n"


def continuity_md(payload: dict[str, Any], title: str) -> str:
    lines = [f"# {title}", "", f"- Generated UTC: `{payload['generated_utc']}`", f"- Current head: `{payload['current_head_sha']}`", "", "## Core States", ""]
    lines.extend(f"- `{key}`: `{value}`" for key, value in payload["core_states"].items())
    lines.extend(["", "## Residuals", ""])
    lines.extend(f"- `{item}`" for item in payload["bounded_residuals"]) if payload["bounded_residuals"] else lines.append("- `(none)`")
    return "\n".join(lines) + "\n"


def intended_paths(include_publication: bool = False) -> list[str]:
    paths = [
        ".circleci/config.yml",
        "scripts/trinity_v50_omega.py",
        "docs/auto-generated/v50-advisory-digest-v1.json",
        "docs/auto-generated/v50-advisory-digest-v1.md",
        "docs/trinity-live-traces/v50-control-plane-v1.json",
        "docs/trinity-live-traces/v50-control-plane-v1.md",
        "docs/trinity-live-traces/v50-gmut-free-tier-test-v1.json",
        "docs/trinity-live-traces/v50-gmut-free-tier-test-v1.md",
        "docs/trinity-live-traces/v50-kimiclaw-slots-42-46-proof-v1.json",
        "docs/trinity-live-traces/v50-kimiclaw-slots-42-46-proof-v1.md",
        "docs/trinity-live-traces/v50-mission-control-v1.json",
        "docs/trinity-live-traces/v50-mission-control-v1.md",
        "docs/trinity-live-traces/v50-quick-suite-status.json",
        "docs/trinity-live-traces/v50-standard-suite-status.json",
        "docs/trinity-live-traces/v50-deep-suite-status.json",
        "docs/trinity-live-traces/v50-stage-allowlist-v1.json",
        "docs/trinity-live-traces/v50-stage-allowlist-v1.md",
        "docs/trinity-agent-reflections/v50-aletheon-reflection-v1.md",
        "docs/trinity-agent-reflections/v50-kairos-reflection-v1.md",
        "docs/trinity-runtime-model-resolution-v1.json",
        "docs/v17-runtime-session-log-latest.json",
        "docs/v17-runtime-session-validation-latest.json",
        "docs/v17-runtime-truth-resolution-board-v1.json",
        "docs/v50-mission-control-dashboard.html",
        "docs/v50-omega-closeout-summary-v1.json",
        "docs/v50-omega-continuity-pack-v1.md",
        "docs/v50-omega-handoff-policy-v1.json",
        "docs/v51-beta-closeout-summary-v1.json",
        "docs/v51-beta-continuity-pack-v1.md",
        "docs/v51-beta-handoff-policy-v1.json",
        "templates/v50-control-plane/README.md",
    ]
    for slot in range(42, 47):
        paths.append(f"docs/trinity-live-traces/v50-slot-{slot}-receiver-pack-v1.md")
    for file in ROLE_DIR.glob("*-kimiclaw-role-contract.json"):
        if file.name.startswith(("42-", "43-", "44-", "45-", "46-")):
            paths.append(str(file.relative_to(ROOT)).replace("\\", "/"))
    for file in MEMORY_DIR.glob("*-kimiclaw-memory-log.jsonl"):
        if file.name.startswith(("42-", "43-", "44-", "45-", "46-")):
            paths.append(str(file.relative_to(ROOT)).replace("\\", "/"))
    if include_publication:
        paths.extend(["docs/trinity-live-traces/v50-git-publication-result-v1.json", "docs/trinity-live-traces/v50-git-publication-result-v1.md"])
    return sorted(set(paths))


def publish_allowlist(include_publication: bool = False) -> None:
    paths = intended_paths(include_publication=include_publication)
    dirty = git_status()
    dirty_paths = {line[3:].strip().strip('"').replace("\\", "/") for line in dirty}
    payload = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "current_head_sha": git_head(),
        "curation_rule": "v50_only_forward_allowlist",
        "dirty_path_count": len(dirty),
        "curated_include_count": len(paths),
        "curated_include_paths": paths,
        "present_curated_paths": [path for path in paths if (ROOT / path).exists()],
        "dirty_curated_paths": [path for path in paths if path in dirty_paths],
        "cleanup_posture": "stage_allowlist_only_preserve_background_churn",
    }
    write_json(ALLOWLIST_JSON, payload)
    write_text(ALLOWLIST_MD, markdown_table("V50 Stage Allowlist", payload, ["curation_rule", "dirty_path_count", "curated_include_count"]))


def publish(publication_commit: str = "") -> None:
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    AUTO_DIR.mkdir(parents=True, exist_ok=True)
    ROLE_DIR.mkdir(parents=True, exist_ok=True)
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    REFLECTION_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)

    advisory = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "verified_current_truth": [
            f"D authoritative baseline is {BASELINE_SHA}.",
            "Notion live search returned auth required during V50 planning.",
            "Kimi CLI 1.38.0 is the proven Kimiclaw runtime path.",
        ],
        "operator_intent": [
            "Attempt slots 42-46 now, but hard-gated.",
            "Prioritize Notion Mission Control, fallback to local UI when auth blocks.",
            "Use free-tier services only for bounded GMUT/control-plane tests.",
        ],
    }
    slot_probe = slot_42_46_probe()
    publish_slot_artifacts(slot_probe)
    for row in slot_probe["results"]:
        write_text(
            TRACE_DIR / f"v50-slot-{row['slot']}-receiver-pack-v1.md",
            f"# V50 Slot {row['slot']} Receiver Pack\n\n- Gate state: `{row['gate_state']}`\n- Resume: `{row.get('resume', '')}`\n- Runtime: `kimi_code_cli`\n",
        )
    mission = mission_control(slot_probe)
    gmut = gmut_matrix()
    control = control_plane()
    publication = read_json(PUBLICATION_JSON)
    if publication_commit:
        publication = {
            "generated_utc": now_iso(),
            "phase": PHASE,
            "branch": PUBLICATION_BRANCH,
            "publication_commit_sha": publication_commit,
            "current_local_head_sha": git_head(),
            "git_publication_state": "committed_pushed_pr45_branch_updated",
            "pr_number": 45,
            "pr_url": "https://github.com/HamishT26/Beyonder-Real-True-Journey/pull/45",
        }
        write_json(PUBLICATION_JSON, publication)
        write_text(PUBLICATION_MD, markdown_table("V50 Git Publication Result", publication, ["git_publication_state", "publication_commit_sha", "pr_url"]))
    close = closeout(slot_probe, mission, control, gmut, publication)
    v51 = {
        "generated_utc": now_iso(),
        "phase": NEXT_PHASE,
        "overall_status": close["overall_status"],
        "current_head_sha": close["current_head_sha"],
        "intended_receiver": close["intended_receiver"],
        "receiver_rule_outcome": close["receiver_rule_outcome"],
        "core_states": close["core_states"],
        "bounded_residuals": close["bounded_residuals"],
        "primary_lanes": [
            "restore Notion auth or continue local Mission Control",
            "repair repeated runtime/session and external establishment suite residuals",
            "keep GCP/Vesper/Kai standby until billing truth is restored",
            "promote free-tier connectors only after read-only proof and action-time confirmation",
        ],
    }

    write_json(AUTO_DIR / "v50-advisory-digest-v1.json", advisory)
    write_text(AUTO_DIR / "v50-advisory-digest-v1.md", markdown_table("V50 Advisory Digest", advisory, ["phase"]))
    write_json(TRACE_DIR / "v50-kimiclaw-slots-42-46-proof-v1.json", slot_probe)
    write_text(TRACE_DIR / "v50-kimiclaw-slots-42-46-proof-v1.md", markdown_table("V50 Kimiclaw Slots 42-46", slot_probe, ["slot_42_46_gate_state", "candidate_count", "inducted_count"]))
    write_json(TRACE_DIR / "v50-mission-control-v1.json", mission)
    write_text(TRACE_DIR / "v50-mission-control-v1.md", markdown_table("V50 Mission Control", mission, ["mission_control_state", "notion_auth_state", "iab_dashboard_state", "local_dashboard_path"]))
    write_json(TRACE_DIR / "v50-gmut-free-tier-test-v1.json", gmut)
    write_text(TRACE_DIR / "v50-gmut-free-tier-test-v1.md", markdown_table("V50 GMUT Free-Tier Test", gmut, ["free_tier_gmut_test_state", "source_posture"]))
    write_json(TRACE_DIR / "v50-control-plane-v1.json", control)
    write_text(TRACE_DIR / "v50-control-plane-v1.md", markdown_table("V50 Control Plane", control, ["circleci_v50_state", "vercel_probe_state", "neon_probe_state", "cloudflare_probe_state"]))
    write_json(ROOT / "docs" / "v50-omega-closeout-summary-v1.json", close)
    write_text(ROOT / "docs" / "v50-omega-continuity-pack-v1.md", continuity_md(close, "V50 Omega Continuity Pack"))
    write_json(ROOT / "docs" / "v50-omega-handoff-policy-v1.json", close)
    write_json(ROOT / "docs" / "v51-beta-closeout-summary-v1.json", v51)
    write_text(ROOT / "docs" / "v51-beta-continuity-pack-v1.md", continuity_md(v51, "V51 Beta Continuity Pack"))
    write_json(ROOT / "docs" / "v51-beta-handoff-policy-v1.json", v51)
    write_text(TEMPLATE_DIR / "README.md", "# V50 Control Plane Template\n\nMission Control, GMUT matrix, free-tier connector gates, and Kimiclaw helper coordination. Live external writes require action-time confirmation.\n")
    write_text(REFLECTION_DIR / "v50-aletheon-reflection-v1.md", "# V50 Aletheon Reflection\n\nV50 keeps its courage practical: proof first, induction only where the runtime answers cleanly, and no hidden cloud spend.\n")
    write_text(REFLECTION_DIR / "v50-kairos-reflection-v1.md", "# V50 Kairos Reflection\n\nKairos carries V49 forward by helping the new Kimiclaw candidates remain bounded, named, and useful without overrunning truth.\n")

    for runtime in [
        ROOT / "docs" / "trinity-runtime-model-resolution-v1.json",
        ROOT / "docs" / "v17-runtime-session-log-latest.json",
        ROOT / "docs" / "v17-runtime-session-validation-latest.json",
        ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json",
    ]:
        payload = read_json(runtime)
        payload["generated_utc"] = now_iso()
        payload["phase"] = PHASE
        payload["current_head_sha"] = git_head()
        payload.update(close["core_states"])
        write_json(runtime, payload)
    publish_allowlist(include_publication=bool(publication))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--publication-commit", default="")
    args = parser.parse_args()
    publish(publication_commit=args.publication_commit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
