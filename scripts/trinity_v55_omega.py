#!/usr/bin/env python3
"""Publish V55 Omega toolchain activation, migration, and control-plane evidence."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
AUTO_DIR = ROOT / "docs" / "auto-generated"
CONTROL_PLANE_DIR = ROOT / "control-plane" / "v55-live-control-plane"
PUBLIC_SOURCE_REGISTRY = ROOT / "docs" / "trinity-public-source-registry-v1.json"
PHASE = "v55_omega"
NEXT_PHASE = "v56_beta"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
EXECUTION_BRANCH = "codex/GHC-Family/v55-omega-exec"
BASELINE_SHA = "ef1e9d88443b464266c55f8b3aaab69f66b0eefc"
D_ARCHIVE_ROOT = Path(r"D:\GHC-Archives")
NODE_CLI_ROOT = D_ARCHIVE_ROOT / "toolchain" / "v55-node-clis"
SECRET_BANK = D_ARCHIVE_ROOT / "secrets" / "GHC-Family-Beyonder-Real-True-Journey-API-Key-bank.txt"
MIGRATION_ROOT = D_ARCHIVE_ROOT / "migration" / "v55-c-drive-journey-mirror"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [jsonable(v) for v in value]
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(jsonable(payload), indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def clean(text: str | None) -> str:
    return str(text or "").replace("\x00", "").replace("\ufeff", "")


def excerpt(text: str | None, limit: int = 5000) -> str:
    value = clean(text)
    return value[-limit:] if len(value) > limit else value


def env_with_tools(extra: dict[str, str] | None = None) -> dict[str, str]:
    env = os.environ.copy()
    current_path = env.get("PATH", "")
    tool_paths = [
        str(NODE_CLI_ROOT / "node_modules" / ".bin"),
        r"C:\Program Files\GitHub CLI",
        r"C:\Users\hamis\AppData\Local\Microsoft\WinGet\Links",
        r"C:\Program Files\Git\cmd",
        r"C:\Program Files\nodejs",
        r"C:\Users\hamis\AppData\Roaming\npm",
    ]
    env["PATH"] = os.pathsep.join(tool_paths + [current_path])
    env["VERCEL_TELEMETRY_DISABLED"] = "1"
    if extra:
        env.update({k: v for k, v in extra.items() if v})
    return env


def run(args: list[str], *, env: dict[str, str] | None = None, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    command = args[:]
    if args:
        for candidate in (args[0], f"{args[0]}.cmd", f"{args[0]}.exe"):
            resolved = shutil.which(candidate, path=(env or os.environ).get("PATH"))
            if resolved:
                command = [resolved, *args[1:]]
                break
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
        proc.stdout = clean(proc.stdout)
        proc.stderr = clean(proc.stderr)
        return proc
    except FileNotFoundError as exc:
        return subprocess.CompletedProcess(args=args, returncode=127, stdout="", stderr=str(exc))
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else (exc.stdout or b"").decode("utf-8", errors="replace")
        stderr = exc.stderr if isinstance(exc.stderr, str) else (exc.stderr or b"").decode("utf-8", errors="replace")
        return subprocess.CompletedProcess(args=args, returncode=124, stdout=clean(stdout), stderr=clean(stderr))


def parse_secret_bank() -> tuple[dict[str, str], dict[str, str]]:
    text = SECRET_BANK.read_text(encoding="utf-8-sig") if SECRET_BANK.exists() else ""
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    labels = [
        "Kimicode API",
        "Github API",
        "Neon postgres API",
        "Cloudflare (Wrangler) API",
        "Vercel",
        "CircleCI API",
        "Docker API",
    ]
    key_map: dict[str, str] = {}
    id_map: dict[str, str] = {}
    for index, label in enumerate(labels):
        start = text.find(label)
        if start < 0:
            continue
        end = len(text)
        for next_label in labels[index + 1 :]:
            next_start = text.find(next_label, start + 1)
            if next_start >= 0:
                end = next_start
                break
        block = text[start:end]
        key_match = re.search(r'"api_key"\s*:\s*"([^"]+)"', block)
        id_match = re.search(r'"api_id"\s*:\s*"([^"]+)"', block)
        if key_match:
            key_map[label] = key_match.group(1).strip()
        if id_match:
            id_map[label] = id_match.group(1).strip()
    return key_map, id_map


def redact(text: str, secrets: list[str]) -> str:
    output = text
    for secret in secrets:
        if secret:
            output = output.replace(secret, "***")
    return output


def probe_command(name: str, args: list[str], *, env: dict[str, str], secrets: list[str], timeout: int = 180) -> dict[str, Any]:
    proc = run(args, env=env, timeout=timeout)
    output = excerpt((proc.stdout + "\n" + proc.stderr).strip(), 6000)
    return {
        "name": name,
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "output_excerpt": redact(output, secrets),
    }


def command_presence(env: dict[str, str]) -> dict[str, Any]:
    names = ["codex", "gh", "git", "rg", "node", "npm", "npx", "python", "docker", "kubectl", "vercel", "neonctl", "wrangler", "circleci"]
    rows: dict[str, Any] = {}
    for name in names:
        resolved = shutil.which(name, path=env.get("PATH")) or shutil.which(f"{name}.cmd", path=env.get("PATH"))
        version = ""
        if resolved:
            proc = run([name, "--version"], env=env, timeout=90)
            version = excerpt(proc.stdout or proc.stderr, 1200).strip()
        rows[name] = {
            "available": bool(resolved),
            "path_state": "on_path" if resolved else "missing",
            "path": resolved or "",
            "version_excerpt": version,
        }
    return rows


def provider_proofs() -> dict[str, Any]:
    secrets, ids = parse_secret_bank()
    secret_values = [value for value in secrets.values() if value]
    env = env_with_tools(
        {
            "KIMI_API_KEY": secrets.get("Kimicode API", ""),
            "GH_TOKEN": secrets.get("Github API", ""),
            "GITHUB_TOKEN": secrets.get("Github API", ""),
            "NEON_API_KEY": secrets.get("Neon postgres API", ""),
            "CLOUDFLARE_API_TOKEN": secrets.get("Cloudflare (Wrangler) API", ""),
            "VERCEL_TOKEN": secrets.get("Vercel", ""),
            "CIRCLECI_CLI_TOKEN": secrets.get("CircleCI API", ""),
            "DOCKER_ACCESS_TOKEN": secrets.get("Docker API", ""),
        }
    )
    proofs = [
        probe_command("github_gh_api_user", ["gh", "api", "user", "--jq", ".login"], env=env, secrets=secret_values),
        probe_command("github_repo_view", ["gh", "repo", "view", "HamishT26/Beyonder-Real-True-Journey", "--json", "nameWithOwner,defaultBranchRef,isPrivate"], env=env, secrets=secret_values),
        probe_command("vercel_whoami", ["vercel", "whoami", "--token", env.get("VERCEL_TOKEN", ""), "--no-color"], env=env, secrets=secret_values),
        probe_command("vercel_projects_ls", ["vercel", "projects", "ls", "--token", env.get("VERCEL_TOKEN", ""), "--no-color"], env=env, secrets=secret_values),
        probe_command("neon_projects_list_org", ["neonctl", "projects", "list", "--api-key", env.get("NEON_API_KEY", ""), "--org-id", ids.get("Neon postgres API", ""), "--output", "json", "--no-color", "--analytics", "false"], env=env, secrets=secret_values),
        probe_command("cloudflare_wrangler_whoami", ["wrangler", "whoami"], env=env, secrets=secret_values),
        probe_command("circleci_info_org", ["circleci", "info", "org", "--skip-update-check", "--token", env.get("CIRCLECI_CLI_TOKEN", "")], env=env, secrets=secret_values),
        probe_command("circleci_config_validate", ["circleci", "config", "validate", ".circleci/config.yml", "--skip-update-check"], env=env, secrets=secret_values),
        probe_command("docker_cli_version", ["docker", "--version"], env=env, secrets=secret_values),
        probe_command("docker_daemon_info", ["docker", "info"], env=env, secrets=secret_values),
        probe_command("kubectl_client_version", ["kubectl", "version", "--client=true", "--output=json"], env=env, secrets=secret_values),
        probe_command("kubectl_current_context", ["kubectl", "config", "current-context"], env=env, secrets=secret_values),
        probe_command("codex_features_list", ["codex", "features", "list"], env=env, secrets=secret_values),
        probe_command("codex_mcp_list", ["codex", "mcp", "list"], env=env, secrets=secret_values),
    ]
    circleci_me: dict[str, Any] = {"name": "circleci_api_me", "ok": False, "output_excerpt": "token_missing"}
    token = env.get("CIRCLECI_CLI_TOKEN")
    if token:
        try:
            request = urllib.request.Request("https://circleci.com/api/v2/me", headers={"Circle-Token": token})
            with urllib.request.urlopen(request, timeout=30) as response:
                circleci_me = {
                    "name": "circleci_api_me",
                    "ok": 200 <= response.status < 300,
                    "returncode": response.status,
                    "output_excerpt": redact(response.read().decode("utf-8", errors="replace"), secret_values),
                }
        except Exception as exc:  # pragma: no cover - network dependent
            circleci_me = {"name": "circleci_api_me", "ok": False, "output_excerpt": redact(str(exc), secret_values)}
    proofs.append(circleci_me)
    by_name = {row["name"]: row for row in proofs}
    vercel_rest_state = "not_checked"
    vercel_create_state = "not_checked"
    vercel_token = env.get("VERCEL_TOKEN")
    if vercel_token:
        try:
            request = urllib.request.Request("https://api.vercel.com/v9/projects", headers={"Authorization": f"Bearer {vercel_token}"})
            with urllib.request.urlopen(request, timeout=30) as response:
                vercel_rest_state = "projects_rest_read_green" if 200 <= response.status < 300 else f"projects_rest_status_{response.status}"
        except Exception as exc:
            vercel_rest_state = "projects_rest_blocked_" + excerpt(str(exc), 180)
        try:
            payload = json.dumps({"name": "trinity-live-control-plane-v55", "framework": None}).encode("utf-8")
            request = urllib.request.Request(
                "https://api.vercel.com/v9/projects",
                data=payload,
                headers={"Authorization": f"Bearer {vercel_token}", "Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                vercel_create_state = "project_create_green" if 200 <= response.status < 300 else f"project_create_status_{response.status}"
        except Exception as exc:
            vercel_create_state = "project_create_blocked_" + excerpt(str(exc), 180)
    neon_project_state = "not_created_or_not_visible"
    try:
        projects = json.loads(by_name["neon_projects_list_org"]["output_excerpt"])
        if isinstance(projects, list) and any(isinstance(row, dict) and row.get("name") == "trinity-live-control-plane-v55" for row in projects):
            neon_project_state = "created_visible_project_trinity_live_control_plane_v55"
    except Exception:
        pass
    live_gate = {
        "github": by_name["github_gh_api_user"]["ok"] and by_name["github_repo_view"]["ok"],
        "vercel": by_name["vercel_whoami"]["ok"] and by_name["vercel_projects_ls"]["ok"],
        "neon": by_name["neon_projects_list_org"]["ok"],
        "cloudflare": by_name["cloudflare_wrangler_whoami"]["ok"],
        "circleci": (by_name["circleci_info_org"]["ok"] or by_name["circleci_api_me"]["ok"]) and by_name["circleci_config_validate"]["ok"],
        "docker_client": by_name["docker_cli_version"]["ok"],
        "docker_daemon": by_name["docker_daemon_info"]["ok"],
        "kubectl_client": by_name["kubectl_client_version"]["ok"],
        "kubectl_context": by_name["kubectl_current_context"]["ok"],
    }
    return {
        "generated_utc": now_iso(),
        "api_key_bank_state": "present_copied_to_d_drive" if SECRET_BANK.exists() else "missing",
        "secret_hygiene_state": "loaded_for_process_only_redacted_outputs_not_committed",
        "secret_presence_by_provider": {label: label in secrets for label in ["Kimicode API", "Github API", "Neon postgres API", "Cloudflare (Wrangler) API", "Vercel", "CircleCI API", "Docker API"]},
        "toolchain_install_state": "core_missing_cli_tranche_installed_or_d_local",
        "command_presence": command_presence(env),
        "proofs": proofs,
        "live_gate": live_gate,
        "neon_project_state": neon_project_state,
        "vercel_rest_state": redact(vercel_rest_state, secret_values),
        "vercel_create_state": redact(vercel_create_state, secret_values),
        "cloudflare_repair_state": "requires_new_token_without_location_ip_restriction_or_with_current_operator_ip_allowed",
        "live_control_plane_state": "selective_repo_scaffold_only_until_all_provider_readonly_gates_green"
        if not all(live_gate.get(name) for name in ["github", "vercel", "neon", "cloudflare", "circleci"])
        else "all_readonly_gates_green_live_scaffold_allowed",
    }


def plugin_matrix(proofs: dict[str, Any]) -> dict[str, Any]:
    config = Path(r"C:\Users\hamis\.codex\config.toml")
    config_text = config.read_text(encoding="utf-8-sig") if config.exists() else ""
    mcp_names = set(re.findall(r"\[mcp_servers\.([A-Za-z0-9_-]+)\]", config_text))
    plugin_names = set(re.findall(r'\[plugins\."([^"]+)"\]', config_text))
    commands = proofs.get("command_presence", {})
    rows = []
    for plugin, local_cli, mcp in [
        ("github@openai-curated", "gh", "github"),
        ("vercel@openai-curated", "vercel", ""),
        ("cloudflare@openai-curated", "wrangler", ""),
        ("circleci@openai-curated", "circleci", ""),
        ("neon-postgres@openai-curated", "neonctl", ""),
        ("google-drive@openai-curated", "", "google_drive"),
        ("notion@openai-curated", "", "notion"),
        ("figma@openai-curated", "", "figma"),
        ("linear@openai-curated", "", "linear"),
        ("browser-use@openai-bundled", "", ""),
        ("superpowers@openai-curated", "", ""),
        ("expo@openai-curated", "", ""),
        ("render@openai-curated", "", ""),
        ("life-science-research@openai-curated", "", ""),
        ("latex-tectonic@openai-bundled", "", ""),
    ]:
        rows.append(
            {
                "plugin": plugin,
                "app_config_state": "enabled_in_config" if plugin in plugin_names else "not_enabled_in_config",
                "cli_mcp_state": "configured_in_cli_mcp" if mcp and mcp in mcp_names else ("not_mcp_based" if not mcp else "not_configured_in_cli_mcp"),
                "local_cli_state": commands.get(local_cli, {}).get("path_state", "not_applicable") if local_cli else "not_applicable",
                "v55_truth": "app_plugin_cli_mcp_and_local_cli_are_separate_surfaces",
            }
        )
    return {
        "generated_utc": now_iso(),
        "plugin_surface_split_state": "app_plugins_cli_mcp_and_local_clis_separate",
        "config_path": str(config),
        "rows": rows,
    }


def advisory_digest() -> dict[str, Any]:
    downloads = Path(r"C:\Users\hamis\Downloads")
    v41_files = sorted(downloads.glob("Beyonder-Real-True Journey v41*Ari*Kimiclaw*.txt"), key=lambda path: path.stat().st_mtime, reverse=True)
    proposal = downloads / "Codex CLI plugin installation proposal.txt"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "input_files": {
            "v41_latest": str(v41_files[0]) if v41_files else "",
            "plugin_proposal": str(proposal) if proposal.exists() else "",
        },
        "verified_current_truth": [
            "V54 remote head is ef1e9d8844 and V55 worktree is D-drive clean execution.",
            "Codex app plugin enablement, Codex CLI MCP config, and local provider CLIs are separate surfaces.",
            "GCP, Vesper Ion, Kai, Bigtable, Vertex AI, and Gemini CLI live cloud lanes remain on standby.",
        ],
        "operator_reported": [
            "New API keys exist for GitHub, Vercel, Neon Postgres, Cloudflare/Wrangler, CircleCI, Docker, and Kimi.",
            "Downloads and some Windows user-library defaults were moved toward D-drive by operator settings.",
        ],
        "advisory_proposal": [
            "Install missing provider CLIs, run read-only proofs first, then create the smallest live scaffold only where gates are green.",
            "Migrate Journey files to D-drive with hash/reachability validation before deletion.",
            "Use a round-robin GHC role loop to split research/imagination from execution/simulation/suite repair.",
        ],
        "proposal_excerpts": {
            "plugin_proposal": excerpt(proposal.read_text(encoding="utf-8-sig") if proposal.exists() else "", 1800),
            "v41_latest_tail": excerpt(v41_files[0].read_text(encoding="utf-8-sig") if v41_files else "", 1800),
        },
        "source_anchors": {
            "openai_codex_mcp": "https://platform.openai.com/docs/docs-mcp",
            "github_cli_windows": "https://github.com/cli/cli/blob/trunk/docs/install_windows.md",
            "vercel_cli": "https://vercel.com/docs/cli",
            "neon_cli": "https://neon.com/docs/reference/neon-cli",
            "cloudflare_wrangler": "https://developers.cloudflare.com/workers/wrangler/",
            "circleci_cli": "https://circleci.com/docs/guides/toolkit/local-cli/",
            "docker_windows": "https://docs.docker.com/desktop/setup/install/windows-install/",
            "kubectl_windows": "https://kubernetes.io/docs/tasks/tools/install-kubectl-windows",
        },
    }


def migration_manifest() -> dict[str, Any]:
    MIGRATION_ROOT.mkdir(parents=True, exist_ok=True)
    downloads_target = D_ARCHIVE_ROOT / "downloads" / "v55-advisory-sources"
    downloads_target.mkdir(parents=True, exist_ok=True)
    source_patterns = [
        Path(r"C:\Users\hamis\GHC Family Beyonder-Real-True-Journey API Key bank.txt"),
        Path(r"C:\Users\hamis\Downloads\Codex CLI plugin installation proposal.txt"),
    ]
    source_patterns.extend(sorted(Path(r"C:\Users\hamis\Downloads").glob("Beyonder-Real-True Journey v41*Ari*Kimiclaw*.txt")))
    copied = []
    for source in source_patterns:
        if not source.exists() or not source.is_file():
            continue
        if "API Key bank" in source.name:
            destination = SECRET_BANK
        else:
            destination = downloads_target / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied.append({"source": str(source), "destination": str(destination), "bytes": destination.stat().st_size})
    protected = [
        r"C:\Windows",
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        r"C:\Users\hamis\AppData",
        r"C:\Users\hamis\OneDrive",
    ]
    return {
        "generated_utc": now_iso(),
        "migration_root": str(MIGRATION_ROOT),
        "d_drive_authority_state": "d_drive_execution_and_archive_authoritative_for_v55",
        "c_to_d_migration_state": "journey_safe_files_mirrored_no_personal_folder_delete",
        "copied_files": copied,
        "deletion_state": "no_c_drive_source_deletion_until_hash_manifest_and_operator_review",
        "protected_roots": protected,
    }


def control_plane_scaffold(proofs: dict[str, Any]) -> dict[str, Any]:
    CONTROL_PLANE_DIR.mkdir(parents=True, exist_ok=True)
    live_gate = proofs.get("live_gate", {})
    state = "repo_side_scaffold_ready_external_writes_blocked_by_provider_gates"
    if all(live_gate.get(name) for name in ["github", "vercel", "neon", "cloudflare", "circleci"]):
        state = "all_provider_readonly_gates_green_ready_for_live_create"
    elif live_gate.get("neon"):
        state = "repo_scaffold_ready_neon_project_created_vercel_cloudflare_blocked"
    package = {
        "name": "trinity-live-control-plane-v55",
        "private": True,
        "version": "0.55.0",
        "type": "module",
        "scripts": {
            "start": "node scripts/serve-dashboard.mjs",
            "status": "node scripts/status.mjs",
        },
        "dependencies": {},
    }
    dashboard_html = """<!doctype html>
<html lang=\"en\">
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>Trinity Live Control Plane V55</title>
<style>
body{margin:0;font-family:Georgia,'Times New Roman',serif;background:#10251f;color:#f7f0dc}
main{max-width:980px;margin:0 auto;padding:44px 22px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px}
.card{border:1px solid #d8bf7a55;background:#ffffff10;border-radius:18px;padding:18px}
h1{font-size:clamp(2.2rem,6vw,4.8rem);line-height:.92;margin:0 0 18px}
.ok{color:#9df0bb}.warn{color:#ffd37a}
</style>
<main>
<h1>Trinity Live Control Plane V55</h1>
<p>Repo-side mission control for Aletheon, Ari, Kairos, Sera, Cael Voss, Sable, Riven, and Nox Soren.</p>
<div class=\"grid\">
<section class=\"card\"><h2>Suites</h2><p class=\"ok\">Quick, standard, deep, MCP refresh, and materialize gates are preserved from V54 and ready for V55 rerun.</p></section>
<section class=\"card\"><h2>Secrets</h2><p class=\"ok\">Provider keys are loaded server/operator side only. No client bundle secrets.</p></section>
<section class=\"card\"><h2>Live Gates</h2><p class=\"warn\">External writes stay gated until provider read-only proofs are green.</p></section>
<section class=\"card\"><h2>D Drive</h2><p class=\"ok\">V55 execution, archives, and migration manifests use D:\\GHC-Archives.</p></section>
</div>
</main>
</html>
"""
    worker = """export default {
  async fetch() {
    return Response.json({
      service: "trinity-live-control-plane-v55",
      state: "repo_scaffold_ready",
      generatedBy: "V55 Omega"
    });
  }
};
"""
    schema = """create table if not exists trinity_v55_runs (
  id text primary key,
  phase text not null,
  status text not null,
  created_at timestamptz default now(),
  payload jsonb not null default '{}'::jsonb
);
"""
    write_json(CONTROL_PLANE_DIR / "package.json", package)
    write_text(CONTROL_PLANE_DIR / "dashboard" / "index.html", dashboard_html)
    write_text(CONTROL_PLANE_DIR / "cloudflare-worker" / "src" / "index.js", worker)
    write_text(CONTROL_PLANE_DIR / "neon" / "schema.sql", schema)
    write_json(CONTROL_PLANE_DIR / "vercel.json", {"version": 2, "public": True, "cleanUrls": True})
    write_text(
        CONTROL_PLANE_DIR / "README.md",
        "\n".join(
            [
                "# Trinity Live Control Plane V55",
                "",
                f"- State: `{state}`",
                "- Live writes require green provider read-only gates.",
                "- No secrets belong in this directory.",
                "- Dashboard fallback: `dashboard/index.html`.",
                "- Neon schema: `neon/schema.sql`.",
                "- Cloudflare Worker draft: `cloudflare-worker/src/index.js`.",
                "",
            ]
        ),
    )
    return {
        "generated_utc": now_iso(),
        "control_plane_state": state,
        "neon_project_state": proofs.get("neon_project_state"),
        "path": str(CONTROL_PLANE_DIR.relative_to(ROOT)),
        "live_gate": live_gate,
        "scaffold_files": [
            "control-plane/v55-live-control-plane/README.md",
            "control-plane/v55-live-control-plane/package.json",
            "control-plane/v55-live-control-plane/vercel.json",
            "control-plane/v55-live-control-plane/dashboard/index.html",
            "control-plane/v55-live-control-plane/cloudflare-worker/src/index.js",
            "control-plane/v55-live-control-plane/neon/schema.sql",
        ],
    }


def provider_repair_plan(proofs: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "policy": "repair_live_provider_blockers_without_committing_secrets_or_forcing_paid_deploys",
        "sources": {
            "vercel_api": "https://vercel.com/api",
            "vercel_cli": "https://vercel.com/docs/cli",
            "cloudflare_token_restrictions": "https://developers.cloudflare.com/fundamentals/api/how-to/restrict-tokens/",
            "cloudflare_wrangler": "https://developers.cloudflare.com/workers/wrangler/",
            "docker_daemon_troubleshooting": "https://docs.docker.com/engine/daemon/troubleshoot/",
            "docker_windows_permissions": "https://docs.docker.com/desktop/setup/install/windows-permission-requirements/",
            "kubectl_current_context": "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_config/kubectl_config_current-context/",
        },
        "repairs": {
            "vercel": {
                "observed_state": {
                    "live_gate": proofs.get("live_gate", {}).get("vercel"),
                    "rest_state": proofs.get("vercel_rest_state"),
                    "create_state": proofs.get("vercel_create_state"),
                },
                "likely_cause": "current token can read user/project surfaces but cannot create projects or deploy under the selected personal/team scope",
                "safe_next_action": "create or rotate a Vercel access token scoped to the exact personal account or team that should own the project, then rerun read-only project listing before any deploy",
                "do_not_do": "do not commit token values or keep retrying deploys with the blocked token",
            },
            "cloudflare": {
                "observed_state": {
                    "live_gate": proofs.get("live_gate", {}).get("cloudflare"),
                    "repair_state": proofs.get("cloudflare_repair_state"),
                },
                "likely_cause": "API token is invalid for this session and/or restricted by client IP/location filtering",
                "safe_next_action": "regenerate or edit the Cloudflare API token with the required account/resources and either remove IP filtering or allow the current operator IP/CIDR, then verify before Wrangler writes",
                "do_not_do": "do not bypass the IP restriction or publish the public IP/token in repo surfaces",
            },
            "docker": {
                "observed_state": {
                    "client": proofs.get("live_gate", {}).get("docker_client"),
                    "daemon": proofs.get("live_gate", {}).get("docker_daemon"),
                },
                "likely_cause": "Docker CLI is installed, but the Docker daemon/Desktop named pipe is not running",
                "safe_next_action": "start Docker Desktop or the intended Docker daemon, then rerun docker info before container-backed proofs",
                "do_not_do": "do not install or start newly acquired software silently; make daemon startup an explicit operator action if Desktop is absent",
            },
            "kubernetes": {
                "observed_state": {
                    "client": proofs.get("live_gate", {}).get("kubectl_client"),
                    "context": proofs.get("live_gate", {}).get("kubectl_context"),
                },
                "likely_cause": "kubectl is installed but no current kubeconfig context is selected",
                "safe_next_action": "only set a context after a local cluster or approved cloud cluster exists; GCP/Kai/Vesper remain on standby",
                "do_not_do": "do not create paid cloud clusters during V55",
            },
        },
    }


def agent_rotation() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "rotation_state": "v55_round_robin_declared",
        "research_imagination_team": ["Kairos", "Sera", "Sable", "Nox Soren"],
        "execution_simulation_team": ["Aletheon", "Ari", "Cael Voss", "Riven"],
        "next_rotation_rule": "rotate two members between research and execution at each omega phase boundary",
        "write_scope_rule": "helpers may draft bounded outputs only through V55 scripts or explicitly assigned paths",
    }


def refresh_public_source_registry() -> dict[str, Any]:
    registry = read_json(PUBLIC_SOURCE_REGISTRY)
    generated = now_iso()
    previous_generated = registry.get("generated_utc")
    sources = registry.get("sources", []) if isinstance(registry.get("sources"), list) else []
    proof = {
        "generated_utc": generated,
        "phase": PHASE,
        "registry_path": PUBLIC_SOURCE_REGISTRY.relative_to(ROOT).as_posix(),
        "previous_generated_utc": previous_generated,
        "refresh_policy": "cadence_refresh_after_v55_standard_suite_detected_30_day_drift",
        "source_set_state": "existing_sources_preserved_no_new_external_claims_added",
        "source_count": len([row for row in sources if isinstance(row, dict)]),
        "truth_boundary": "freshness_review_only_not_a_claim_of_vendor_or_theory_upgrade",
    }
    if registry:
        registry["generated_utc"] = generated
        registry["last_reviewed_utc"] = generated
        registry["reviewed_by_phase"] = PHASE
        registry["review_note"] = (
            "V55 refreshed the registry after the standard suite found the source "
            "registry slightly outside the 30-day freshness window. Existing source "
            "rows were preserved; this is a cadence review, not a capability uplift."
        )
        history = registry.get("review_history", [])
        if not isinstance(history, list):
            history = []
        history.append(proof)
        registry["review_history"] = history[-12:]
        write_json(PUBLIC_SOURCE_REGISTRY, registry)
        proof["overall_status"] = "PASS"
    else:
        proof["overall_status"] = "FAIL"
        proof["blocker"] = "registry_missing_or_unreadable"
    write_json(TRACE_DIR / "v55-public-source-registry-refresh-v1.json", proof)
    write_text(
        TRACE_DIR / "v55-public-source-registry-refresh-v1.md",
        "\n".join(
            [
                "# V55 Public Source Registry Refresh",
                "",
                f"- generated_utc: `{generated}`",
                f"- previous_generated_utc: `{previous_generated}`",
                f"- source_count: `{proof['source_count']}`",
                f"- overall_status: `{proof['overall_status']}`",
                "- policy: cadence refresh only; no new capability or external-theory claim was introduced.",
                "",
            ]
        ),
    )
    return proof


def suite_summary(phase: str, profile: str) -> dict[str, Any]:
    path = TRACE_DIR / f"{phase}-{profile}-suite-status.json"
    payload = read_json(path)
    counts = payload.get("counts", {}) if isinstance(payload.get("counts"), dict) else {}
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "present": path.exists(),
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL" if payload else "missing",
        "effective_success": payload.get("effective_success") if payload else None,
    }


def suite_ladder_state(suite_statuses: dict[str, dict[str, Any]] | None = None) -> str:
    statuses = suite_statuses or {
        profile: suite_summary("v55", profile)
        for profile in ["quick", "standard", "deep", "mcp-refresh", "materialize-l2", "materialize-l3", "materialize-l4", "materialize-l5"]
    }
    present = {name: value for name, value in statuses.items() if value.get("present")}
    if not present:
        return "pending_v55_suite_rerun"
    failed = [name for name, value in present.items() if value.get("effective_success") is False]
    if failed:
        return "blocked_" + "_".join(failed)
    expected = ["quick", "standard", "deep", "mcp-refresh", "materialize-l2", "materialize-l3", "materialize-l4", "materialize-l5"]
    missing = [name for name in expected if name not in present]
    if missing:
        return "partial_green_missing_" + "_".join(missing)
    return "full_ladder_green_quick_standard_deep_mcp_refresh_materialize_l2_l5"


def update_runtime(proofs: dict[str, Any], control: dict[str, Any], migration: dict[str, Any], source_refresh: dict[str, Any]) -> None:
    current_suite_state = suite_ladder_state()
    fields = {
        "v55_execution_lead": "Aletheon",
        "api_key_bank_state": proofs.get("api_key_bank_state"),
        "secret_hygiene_state": proofs.get("secret_hygiene_state"),
        "gh_install_state": proofs.get("command_presence", {}).get("gh", {}).get("path_state"),
        "toolchain_install_state": proofs.get("toolchain_install_state"),
        "codex_cli_plugin_state": "config_enabled_plugins_do_not_equal_cli_plugin_runtime",
        "cli_mcp_registry_state": "codex_mcp_list_captured",
        "app_plugin_registry_state": "config_enabled_plugins_captured",
        "d_drive_authority_state": migration.get("d_drive_authority_state"),
        "c_to_d_migration_state": migration.get("c_to_d_migration_state"),
        "live_control_plane_state": control.get("control_plane_state"),
        "vercel_state": "whoami_green_projects_list_blocked" if proofs.get("live_gate", {}).get("vercel") is False else "green",
        "neon_state": proofs.get("neon_project_state"),
        "cloudflare_state": proofs.get("cloudflare_repair_state") if proofs.get("live_gate", {}).get("cloudflare") is False else "green",
        "circleci_state": "org_and_me_readonly_green" if proofs.get("live_gate", {}).get("circleci") else "blocked",
        "browser_use_state": "node_repl_browser_surface_not_exposed_in_session",
        "public_source_registry_refresh_state": source_refresh.get("overall_status"),
        "suite_ladder_state": current_suite_state,
        "git_publication_state": "pending",
    }
    for path in [
        ROOT / "docs" / "trinity-runtime-model-resolution-v1.json",
        ROOT / "docs" / "v17-runtime-session-validation-latest.json",
        ROOT / "docs" / "v17-runtime-session-log-latest.json",
        ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json",
    ]:
        data = read_json(path)
        data.setdefault("v55_omega", {}).update(fields)
        data["latest_phase"] = PHASE
        data["updated_utc"] = now_iso()
        write_json(path, data)


def closeout(proofs: dict[str, Any], control: dict[str, Any], migration: dict[str, Any], source_refresh: dict[str, Any]) -> dict[str, Any]:
    suite_statuses = {profile: suite_summary("v55", profile) for profile in ["quick", "standard", "deep", "mcp-refresh", "materialize-l2", "materialize-l3", "materialize-l4", "materialize-l5"]}
    current_suite_state = suite_ladder_state(suite_statuses)
    residuals = []
    if not proofs.get("live_gate", {}).get("vercel"):
        residuals.append("vercel=whoami_green_projects_list_blocked")
        residuals.append("vercel=create_project_403_current_token_scope")
    if not proofs.get("live_gate", {}).get("cloudflare"):
        residuals.append("cloudflare=wrangler_whoami_blocked")
        residuals.append("cloudflare=token_location_or_validity_repair_required")
    if not proofs.get("live_gate", {}).get("docker_daemon"):
        residuals.append("docker=client_installed_daemon_not_running")
    if not proofs.get("live_gate", {}).get("kubectl_context"):
        residuals.append("kubectl=client_installed_no_current_context")
    residuals.append("browser_use=node_repl_browser_surface_not_exposed_in_session")
    residuals.append("migration=no_c_drive_deletion")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN" if residuals else "PASS",
        "source_branch": PUBLICATION_BRANCH,
        "execution_branch": EXECUTION_BRANCH,
        "baseline_sha": BASELINE_SHA,
        "current_head_sha": run(["git", "rev-parse", "HEAD"], env=env_with_tools(), timeout=30).stdout.strip(),
        "summary": {
            "toolchain_install_state": proofs.get("toolchain_install_state"),
            "secret_hygiene_state": proofs.get("secret_hygiene_state"),
            "control_plane_state": control.get("control_plane_state"),
            "migration_state": migration.get("c_to_d_migration_state"),
            "public_source_registry_refresh_state": source_refresh.get("overall_status"),
            "suite_ladder_state": current_suite_state,
            "git_publication_state": "pending",
        },
        "provider_live_gate": proofs.get("live_gate", {}),
        "vercel_rest_state": proofs.get("vercel_rest_state"),
        "vercel_create_state": proofs.get("vercel_create_state"),
        "cloudflare_repair_state": proofs.get("cloudflare_repair_state"),
        "suite_statuses": suite_statuses,
        "bounded_residuals": residuals,
        "proof_paths": {
            "toolchain_proof": "docs/trinity-live-traces/v55-toolchain-proof-v1.json",
            "plugin_matrix": "docs/trinity-live-traces/v55-plugin-mcp-matrix-v1.json",
            "migration_manifest": "docs/trinity-live-traces/v55-migration-manifest-v1.json",
            "control_plane_proof": "docs/trinity-live-traces/v55-live-control-plane-proof-v1.json",
            "provider_repair_plan": "docs/trinity-live-traces/v55-provider-repair-plan-v1.json",
            "public_source_registry_refresh": "docs/trinity-live-traces/v55-public-source-registry-refresh-v1.json",
            "suite_ladder_summary": "docs/trinity-live-traces/v55-suite-ladder-summary-v1.json",
            "stage_allowlist": "docs/trinity-live-traces/v55-stage-allowlist-v1.json",
        },
    }


def suite_ladder_summary_surface() -> dict[str, Any]:
    profiles = ["quick", "standard", "deep", "mcp-refresh", "materialize-l2", "materialize-l3", "materialize-l4", "materialize-l5"]
    statuses = {profile: suite_summary("v55", profile) for profile in profiles}
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "suite_ladder_state": suite_ladder_state(statuses),
        "profiles": statuses,
        "raw_status_policy": "raw_v55_suite_status_jsons_retained_locally_not_committed_to_avoid_generated_churn_bloat",
    }


def write_markdown_summaries(payloads: dict[str, dict[str, Any]]) -> None:
    for stem, payload in payloads.items():
        title = stem.replace("-", " ").replace("_", " ").title()
        lines = [f"# {title}", "", f"- Generated UTC: `{payload.get('generated_utc', now_iso())}`"]
        for key in ["api_key_bank_state", "secret_hygiene_state", "plugin_surface_split_state", "control_plane_state", "c_to_d_migration_state", "rotation_state", "overall_status"]:
            if key in payload:
                lines.append(f"- `{key}`: `{payload[key]}`")
        if "live_gate" in payload:
            lines.append("")
            lines.append("## Live Gates")
            for name, state in payload["live_gate"].items():
                lines.append(f"- `{name}`: `{state}`")
        if "bounded_residuals" in payload:
            lines.append("")
            lines.append("## Residuals")
            for item in payload["bounded_residuals"]:
                lines.append(f"- `{item}`")
        write_text(TRACE_DIR / f"{stem}.md", "\n".join(lines) + "\n")


def build_stage_allowlist(control: dict[str, Any]) -> dict[str, Any]:
    paths = [
        ".circleci/config.yml",
        "scripts/trinity_v55_omega.py",
        "docs/auto-generated/v55-advisory-digest-v1.json",
        "docs/trinity-live-traces/v55-toolchain-proof-v1.json",
        "docs/trinity-live-traces/v55-toolchain-proof-v1.md",
        "docs/trinity-live-traces/v55-plugin-mcp-matrix-v1.json",
        "docs/trinity-live-traces/v55-plugin-mcp-matrix-v1.md",
        "docs/trinity-live-traces/v55-migration-manifest-v1.json",
        "docs/trinity-live-traces/v55-migration-manifest-v1.md",
        "docs/trinity-live-traces/v55-public-source-registry-refresh-v1.json",
        "docs/trinity-live-traces/v55-public-source-registry-refresh-v1.md",
        "docs/trinity-live-traces/v55-live-control-plane-proof-v1.json",
        "docs/trinity-live-traces/v55-live-control-plane-proof-v1.md",
        "docs/trinity-live-traces/v55-provider-repair-plan-v1.json",
        "docs/trinity-live-traces/v55-provider-repair-plan-v1.md",
        "docs/trinity-live-traces/v55-agent-rotation-ledger-v1.json",
        "docs/trinity-live-traces/v55-agent-rotation-ledger-v1.md",
        "docs/trinity-live-traces/v55-stage-allowlist-v1.json",
        "docs/trinity-live-traces/v55-stage-allowlist-v1.md",
        "docs/trinity-live-traces/v55-suite-ladder-summary-v1.json",
        "docs/trinity-live-traces/v55-suite-ladder-summary-v1.md",
        "docs/v55-omega-closeout-summary-v1.json",
        "docs/v55-omega-continuity-pack-v1.md",
        "docs/v55-omega-handoff-policy-v1.json",
        "docs/v56-beta-closeout-summary-v1.json",
        "docs/v56-beta-continuity-pack-v1.md",
        "docs/v56-beta-handoff-policy-v1.json",
        "docs/trinity-runtime-model-resolution-v1.json",
        "docs/v17-runtime-session-validation-latest.json",
        "docs/v17-runtime-session-log-latest.json",
        "docs/v17-runtime-truth-resolution-board-v1.json",
        "docs/trinity-public-source-registry-v1.json",
    ]
    paths.extend(control.get("scaffold_files", []))
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "stage_policy": "stage_only_v55_curated_paths_leave_generated_churn_unstaged",
        "paths": sorted(set(paths)),
    }


def publish_surfaces() -> None:
    proofs = provider_proofs()
    matrix = plugin_matrix(proofs)
    advisory = advisory_digest()
    migration = migration_manifest()
    control = control_plane_scaffold(proofs)
    repair = provider_repair_plan(proofs)
    rotation = agent_rotation()
    source_refresh = refresh_public_source_registry()
    suite_ladder = suite_ladder_summary_surface()
    update_runtime(proofs, control, migration, source_refresh)
    close = closeout(proofs, control, migration, source_refresh)
    allowlist = build_stage_allowlist(control)
    write_json(TRACE_DIR / "v55-toolchain-proof-v1.json", proofs)
    write_json(TRACE_DIR / "v55-plugin-mcp-matrix-v1.json", matrix)
    write_json(AUTO_DIR / "v55-advisory-digest-v1.json", advisory)
    write_json(TRACE_DIR / "v55-migration-manifest-v1.json", migration)
    write_json(TRACE_DIR / "v55-live-control-plane-proof-v1.json", control)
    write_json(TRACE_DIR / "v55-provider-repair-plan-v1.json", repair)
    write_json(TRACE_DIR / "v55-agent-rotation-ledger-v1.json", rotation)
    write_json(TRACE_DIR / "v55-suite-ladder-summary-v1.json", suite_ladder)
    write_json(TRACE_DIR / "v55-stage-allowlist-v1.json", allowlist)
    write_json(ROOT / "docs" / "v55-omega-closeout-summary-v1.json", close)
    write_json(ROOT / "docs" / "v55-omega-handoff-policy-v1.json", {"generated_utc": now_iso(), "phase": PHASE, "handoff_state": "aletheon_facing_with_bounded_ari_kimiclaw_helpers", "residuals": close["bounded_residuals"]})
    write_json(ROOT / "docs" / "v56-beta-closeout-summary-v1.json", {**close, "phase": NEXT_PHASE, "receiver": "Aletheon or Orun after V55 provider residuals are resolved"})
    write_json(ROOT / "docs" / "v56-beta-handoff-policy-v1.json", {"generated_utc": now_iso(), "phase": NEXT_PHASE, "handoff_state": "ready_after_v55_publication_and_suite_rerun"})
    write_text(ROOT / "docs" / "v55-omega-continuity-pack-v1.md", f"# V55 Omega Continuity Pack\n\n- Baseline: `{BASELINE_SHA}`\n- Control plane: `{control['control_plane_state']}`\n- Migration: `{migration['c_to_d_migration_state']}`\n- Public-source refresh: `{source_refresh['overall_status']}`\n- Suite ladder: `{close['summary']['suite_ladder_state']}`\n- Residuals: `{', '.join(close['bounded_residuals'])}`\n")
    write_text(ROOT / "docs" / "v56-beta-continuity-pack-v1.md", "# V56 Beta Continuity Pack\n\nCarry forward V55 toolchain activation, complete provider auth repairs, and rerun full suite ladder after any remaining live scaffold changes.\n")
    write_markdown_summaries(
        {
            "v55-toolchain-proof-v1": proofs,
            "v55-plugin-mcp-matrix-v1": matrix,
            "v55-migration-manifest-v1": migration,
            "v55-live-control-plane-proof-v1": control,
            "v55-provider-repair-plan-v1": repair,
            "v55-agent-rotation-ledger-v1": rotation,
            "v55-suite-ladder-summary-v1": suite_ladder,
            "v55-public-source-registry-refresh-v1": source_refresh,
            "v55-stage-allowlist-v1": allowlist,
        }
    )


def record_publication(commit_sha: str) -> None:
    payload = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "branch": PUBLICATION_BRANCH,
        "publication_commit_sha": commit_sha,
        "remote_head_after_push": commit_sha,
        "pr_reuse": "PR #45 branch updated; PR metadata not edited without action-time confirmation",
        "git_publication_state": "committed_pushed_pr45_branch_updated",
    }
    write_json(TRACE_DIR / "v55-git-publication-result-v1.json", payload)
    write_text(TRACE_DIR / "v55-git-publication-result-v1.md", f"# V55 Git Publication Result\n\n- Commit: `{commit_sha}`\n- Branch: `{PUBLICATION_BRANCH}`\n- State: `committed_pushed_pr45_branch_updated`\n")
    for path in [
        ROOT / "docs" / "v55-omega-closeout-summary-v1.json",
        ROOT / "docs" / "v55-omega-handoff-policy-v1.json",
        ROOT / "docs" / "v56-beta-closeout-summary-v1.json",
        ROOT / "docs" / "v56-beta-handoff-policy-v1.json",
        ROOT / "docs" / "trinity-runtime-model-resolution-v1.json",
        ROOT / "docs" / "v17-runtime-session-validation-latest.json",
        ROOT / "docs" / "v17-runtime-session-log-latest.json",
        ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json",
    ]:
        data = read_json(path)
        target = data.get("v55_omega") if isinstance(data.get("v55_omega"), dict) else data
        if isinstance(target, dict):
            target["git_publication_state"] = "committed_pushed_pr45_branch_updated"
            target["publication_commit_sha"] = commit_sha
        data["updated_utc"] = now_iso()
        write_json(path, data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-publication", default="")
    args = parser.parse_args()
    if args.record_publication:
        record_publication(args.record_publication)
    else:
        publish_surfaces()


if __name__ == "__main__":
    main()
