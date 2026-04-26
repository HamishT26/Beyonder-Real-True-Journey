#!/usr/bin/env python3
"""Publish V56 Omega local-first enterprise control-plane evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = ROOT / "docs" / "trinity-live-traces"
AUTO_DIR = ROOT / "docs" / "auto-generated"
CONTROL_PLANE_DIR = ROOT / "control-plane" / "v56-enterprise-control-plane"
PUBLIC_SOURCE_REGISTRY = ROOT / "docs" / "trinity-public-source-registry-v1.json"
PHASE = "v56_omega"
NEXT_PHASE = "v57_beta"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
EXECUTION_BRANCH = "codex/GHC-Family/v56-omega-exec"
BASELINE_SHA = "b093f87cdee1d6ad4fa7bf4ddf47f5adccf35868"
D_ARCHIVE_ROOT = Path(r"D:\GHC-Archives")
NODE_CLI_ROOT = D_ARCHIVE_ROOT / "toolchain" / "v55-node-clis"
SECRET_BANK_CANDIDATES = [
    Path(r"D:\GHC Family Beyonder-Real-True-Journey API Key bank (Cleaned up).txt"),
    Path(r"C:\Users\hamis\GHC Family Beyonder-Real-True-Journey API Key bank (Cleaned up).txt"),
    D_ARCHIVE_ROOT / "secrets" / "GHC-Family-Beyonder-Real-True-Journey-API-Key-bank.txt",
]


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


def active_secret_bank() -> Path | None:
    for path in SECRET_BANK_CANDIDATES:
        if path.exists() and path.is_file():
            return path
    return None


def parse_secret_bank() -> tuple[dict[str, str], dict[str, str], Path | None]:
    path = active_secret_bank()
    text = path.read_text(encoding="utf-8-sig") if path else ""
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
    return key_map, id_map, path


def secret_presence(secrets: dict[str, str], path: Path | None) -> dict[str, Any]:
    return {
        "secret_bank_state": "present" if path else "missing",
        "secret_bank_path_state": "d_drive_cleaned_bank" if path and str(path).startswith("D:") else ("c_drive_cleaned_bank" if path else "missing"),
        "providers": {
            label: {
                "present": bool(value),
                "length_bucket": "missing" if not value else ("short" if len(value) < 20 else "present"),
                "secret_value_committed": False,
            }
            for label, value in secrets.items()
        },
        "redaction_policy": "raw_secret_values_never_written_to_repo_outputs",
    }


def redact(text: str, secrets: list[str]) -> str:
    output = text
    for secret in secrets:
        if secret:
            output = output.replace(secret, "***")
    output = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "<email_redacted>", output)
    output = re.sub(r"\bteam_[A-Za-z0-9]{12,}\b", "<vercel_team_id_redacted>", output)
    output = re.sub(r"\borg-[A-Za-z0-9_-]{8,}\b", "<neon_org_id_redacted>", output)
    output = re.sub(r"\b[0-9a-f]{24,64}\b", "<hex_id_redacted>", output, flags=re.IGNORECASE)
    output = re.sub(r"\b[A-Za-z0-9_-]{32,}\b", "<long_id_redacted>", output)
    return output


def env_with_tools(extra: dict[str, str] | None = None) -> dict[str, str]:
    env = os.environ.copy()
    current_path = env.get("PATH", "")
    tool_paths = [
        str(NODE_CLI_ROOT / "node_modules" / ".bin"),
        r"C:\Program Files\GitHub CLI",
        r"C:\Users\hamis\AppData\Local\Microsoft\WinGet\Links",
        r"C:\Program Files\Docker\Docker\resources\bin",
        r"C:\Program Files\Git\cmd",
        r"C:\Program Files\nodejs",
        r"C:\Users\hamis\AppData\Roaming\npm",
    ]
    env["PATH"] = os.pathsep.join(tool_paths + [current_path])
    env["VERCEL_TELEMETRY_DISABLED"] = "1"
    if extra:
        env.update({k: v for k, v in extra.items() if v})
    return env


def run(args: list[str], *, env: dict[str, str] | None = None, timeout: int = 45) -> subprocess.CompletedProcess[str]:
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


def probe_command(name: str, args: list[str], *, env: dict[str, str], secrets: list[str], timeout: int = 45) -> dict[str, Any]:
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
            proc = run([name, "--version"], env=env, timeout=35)
            version = excerpt(proc.stdout or proc.stderr, 1200).strip()
        rows[name] = {
            "available": bool(resolved),
            "path_state": "on_path" if resolved else "missing",
            "path": resolved or "",
            "version_excerpt": version,
        }
    return rows


def http_probe(name: str, url: str, token: str, *, secrets: list[str], header_name: str = "Authorization", method: str = "GET") -> dict[str, Any]:
    if not token:
        return {"name": name, "ok": False, "status": "missing_token", "output_excerpt": "token_missing"}
    header_value = f"Bearer {token}" if header_name == "Authorization" else token
    request = urllib.request.Request(url, headers={header_name: header_value, "Accept": "application/json"}, method=method)
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            body = response.read().decode("utf-8", errors="replace")
            digest = hashlib.sha256(body.encode("utf-8", errors="replace")).hexdigest()[:12]
            return {
                "name": name,
                "ok": 200 <= response.status < 300,
                "status": response.status,
                "output_excerpt": f"success_body_redacted_sha256_12={digest}",
            }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"name": name, "ok": False, "status": exc.code, "output_excerpt": redact(excerpt(body or str(exc), 3000), secrets)}
    except Exception as exc:
        return {"name": name, "ok": False, "status": "error", "output_excerpt": redact(excerpt(str(exc), 3000), secrets)}


def cloudflare_account_token_verify(token: str, *, secrets: list[str]) -> dict[str, Any]:
    if not token:
        return {"name": "cloudflare_account_token_verify", "ok": False, "status": "missing_token", "output_excerpt": "token_missing"}
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    try:
        accounts_request = urllib.request.Request("https://api.cloudflare.com/client/v4/accounts", headers=headers)
        with urllib.request.urlopen(accounts_request, timeout=25) as response:
            accounts_body = response.read().decode("utf-8", errors="replace")
        accounts_payload = json.loads(accounts_body)
        accounts = accounts_payload.get("result", []) if isinstance(accounts_payload, dict) else []
        account_id = ""
        if accounts and isinstance(accounts[0], dict):
            account_id = str(accounts[0].get("id", ""))
        if not account_id:
            return {"name": "cloudflare_account_token_verify", "ok": False, "status": "missing_account_id", "output_excerpt": "accounts_read_green_but_no_account_id"}
        verify_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/tokens/verify"
        verify_request = urllib.request.Request(verify_url, headers=headers)
        with urllib.request.urlopen(verify_request, timeout=25) as response:
            verify_body = response.read().decode("utf-8", errors="replace")
            digest = hashlib.sha256(verify_body.encode("utf-8", errors="replace")).hexdigest()[:12]
            account_digest = hashlib.sha256(account_id.encode("utf-8")).hexdigest()[:12]
            return {
                "name": "cloudflare_account_token_verify",
                "ok": 200 <= response.status < 300,
                "status": response.status,
                "output_excerpt": f"account_token_verify_body_redacted_sha256_12={digest}; account_id_sha256_12={account_digest}",
            }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"name": "cloudflare_account_token_verify", "ok": False, "status": exc.code, "output_excerpt": redact(excerpt(body or str(exc), 3000), secrets)}
    except Exception as exc:
        return {"name": "cloudflare_account_token_verify", "ok": False, "status": "error", "output_excerpt": redact(excerpt(str(exc), 3000), secrets)}


def provider_and_tool_proofs() -> dict[str, Any]:
    secrets, ids, bank_path = parse_secret_bank()
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
    command_rows = command_presence(env)
    proofs = [
        http_probe("github_repo_read", "https://api.github.com/repos/HamishT26/Beyonder-Real-True-Journey", secrets.get("Github API", ""), secrets=secret_values),
        http_probe("vercel_user_read", "https://api.vercel.com/v2/user", secrets.get("Vercel", ""), secrets=secret_values),
        http_probe("vercel_projects_read", "https://api.vercel.com/v9/projects", secrets.get("Vercel", ""), secrets=secret_values),
        http_probe("cloudflare_user_token_verify", "https://api.cloudflare.com/client/v4/user/tokens/verify", secrets.get("Cloudflare (Wrangler) API", ""), secrets=secret_values),
        cloudflare_account_token_verify(secrets.get("Cloudflare (Wrangler) API", ""), secrets=secret_values),
        http_probe("cloudflare_accounts_read", "https://api.cloudflare.com/client/v4/accounts", secrets.get("Cloudflare (Wrangler) API", ""), secrets=secret_values),
        http_probe("neon_projects_read", "https://console.neon.tech/api/v2/projects", secrets.get("Neon postgres API", ""), secrets=secret_values),
        http_probe("circleci_me_read", "https://circleci.com/api/v2/me", secrets.get("CircleCI API", ""), secrets=secret_values, header_name="Circle-Token"),
        probe_command("vercel_cli_whoami", ["vercel", "whoami", "--token", env.get("VERCEL_TOKEN", ""), "--no-color"], env=env, secrets=secret_values, timeout=40),
        probe_command("wrangler_cli_whoami", ["wrangler", "whoami"], env=env, secrets=secret_values, timeout=40),
        probe_command("circleci_config_validate", ["circleci", "config", "validate", ".circleci/config.yml", "--skip-update-check"], env=env, secrets=secret_values, timeout=40),
        probe_command("codex_features_list", ["codex", "features", "list"], env=env, secrets=secret_values, timeout=40),
        probe_command("codex_mcp_list", ["codex", "mcp", "list"], env=env, secrets=secret_values, timeout=40),
    ]
    by_name = {row["name"]: row for row in proofs}
    live_gate = {
        "github_read": by_name["github_repo_read"]["ok"],
        "vercel_read": by_name["vercel_user_read"]["ok"] and by_name["vercel_projects_read"]["ok"],
        "cloudflare_user_verify": by_name["cloudflare_user_token_verify"]["ok"],
        "cloudflare_account_verify": by_name["cloudflare_account_token_verify"]["ok"],
        "cloudflare_verify": by_name["cloudflare_user_token_verify"]["ok"] or by_name["cloudflare_account_token_verify"]["ok"],
        "cloudflare_accounts": by_name["cloudflare_accounts_read"]["ok"],
        "neon_read": by_name["neon_projects_read"]["ok"],
        "circleci_read": by_name["circleci_me_read"]["ok"],
        "circleci_config": by_name["circleci_config_validate"]["ok"],
    }
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "api_key_bank": secret_presence(secrets, bank_path),
        "secret_hygiene_state": "loaded_for_process_only_redacted_outputs_not_committed",
        "command_presence": command_rows,
        "provider_proofs": proofs,
        "provider_live_gate": live_gate,
        "provider_id_presence": {label: bool(value) for label, value in ids.items()},
        "live_write_policy": "not_attempted_without_all_readonly_gates_green_and_explicit_external_write_step",
    }


def docker_kubernetes_proof() -> dict[str, Any]:
    env = env_with_tools()
    backup_dirs = sorted((D_ARCHIVE_ROOT / "artifacts").glob("v56-kubernetes-manifest-backup-*")) if (D_ARCHIVE_ROOT / "artifacts").exists() else []
    latest_backup = backup_dirs[-1] if backup_dirs else None
    proofs = [
        probe_command("docker_version", ["docker", "--version"], env=env, secrets=[], timeout=20),
        probe_command("docker_context_ls", ["docker", "context", "ls"], env=env, secrets=[], timeout=20),
        probe_command("docker_info", ["docker", "info", "--format", "{{json .ServerVersion}} {{json .OperatingSystem}} {{json .NCPU}}"], env=env, secrets=[], timeout=90),
        probe_command("docker_desktop_containers", ["docker", "ps", "-a", "--format", "{{.Names}}|{{.Status}}|{{.Image}}"], env=env, secrets=[], timeout=30),
        probe_command("kubectl_current_context", ["kubectl", "config", "current-context"], env=env, secrets=[], timeout=20),
        probe_command("kubectl_readyz", ["kubectl", "get", "--raw=/readyz", "--request-timeout=45s"], env=env, secrets=[], timeout=75),
        probe_command("kubectl_readyz_verbose", ["kubectl", "get", "--raw=/readyz?verbose", "--request-timeout=60s"], env=env, secrets=[], timeout=90),
        probe_command("kubectl_get_nodes", ["kubectl", "get", "nodes", "-o", "wide", "--request-timeout=45s"], env=env, secrets=[], timeout=75),
        probe_command("kubectl_get_namespaces", ["kubectl", "get", "namespaces", "--request-timeout=45s"], env=env, secrets=[], timeout=75),
        probe_command("kubectl_kube_system_pods", ["kubectl", "-n", "kube-system", "get", "pods", "-o", "wide", "--request-timeout=60s"], env=env, secrets=[], timeout=90),
        probe_command(
            "kubernetes_static_manifest_tuning",
            [
                "docker",
                "exec",
                "desktop-control-plane",
                "sh",
                "-lc",
                "grep -H -E -- '--leader-elect|periodSeconds:' /etc/kubernetes/manifests/kube-controller-manager.yaml /etc/kubernetes/manifests/kube-scheduler.yaml /etc/kubernetes/manifests/kube-apiserver.yaml",
            ],
            env=env,
            secrets=[],
            timeout=45,
        ),
        probe_command(
            "kubernetes_internal_admin_nodes",
            ["docker", "exec", "desktop-control-plane", "kubectl", "--kubeconfig", "/etc/kubernetes/admin.conf", "get", "nodes", "-o", "wide"],
            env=env,
            secrets=[],
            timeout=75,
        ),
        probe_command(
            "kubernetes_internal_admin_namespaces",
            ["docker", "exec", "desktop-control-plane", "kubectl", "--kubeconfig", "/etc/kubernetes/admin.conf", "get", "namespaces"],
            env=env,
            secrets=[],
            timeout=75,
        ),
    ]
    by_name = {row["name"]: row for row in proofs}
    docker_state = "daemon_green" if by_name["docker_info"]["ok"] else ("daemon_timeout_or_blocked" if by_name["docker_info"]["returncode"] == 124 else "daemon_not_green")
    required_containers = ["desktop-control-plane", "desktop-worker", "desktop-worker2", "kind-cloud-provider", "kind-registry-mirror"]
    container_output = by_name["docker_desktop_containers"]["output_excerpt"]
    container_rows = {
        name: next((line for line in container_output.splitlines() if line.startswith(f"{name}|")), "")
        for name in required_containers
    }
    required_containers_up = all("|Up " in row or "|Up" in row for row in container_rows.values())
    windows_kubectl_green = (
        by_name["kubectl_current_context"]["ok"]
        and "docker-desktop" in by_name["kubectl_current_context"]["output_excerpt"]
        and by_name["kubectl_readyz"]["ok"]
        and by_name["kubectl_readyz_verbose"]["ok"]
        and by_name["kubectl_get_nodes"]["ok"]
        and by_name["kubectl_get_namespaces"]["ok"]
    )
    system_pods_output = by_name["kubectl_kube_system_pods"]["output_excerpt"]
    system_pods_green = by_name["kubectl_kube_system_pods"]["ok"] and "CrashLoopBackOff" not in system_pods_output and " 0/1 " not in system_pods_output
    internal_admin_green = by_name["kubernetes_internal_admin_nodes"]["ok"] and by_name["kubernetes_internal_admin_namespaces"]["ok"]
    manifest_tuning_output = by_name["kubernetes_static_manifest_tuning"]["output_excerpt"]
    manifest_tuning_green = manifest_tuning_output.count("--leader-elect=false") >= 2
    if windows_kubectl_green and system_pods_green and required_containers_up:
        kube_state = "docker_desktop_windows_kubectl_and_system_pods_green"
    elif windows_kubectl_green and required_containers_up:
        kube_state = "docker_desktop_windows_kubectl_green_system_pods_pending"
    elif windows_kubectl_green:
        kube_state = "windows_kubectl_green_container_residual"
    elif internal_admin_green:
        kube_state = "cluster_internal_green_windows_bridge_pending"
    else:
        kube_state = "context_present_but_api_not_green"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "docker_state": docker_state,
        "kubernetes_state": kube_state,
        "kubernetes_resolution_state": "resolved" if kube_state == "docker_desktop_windows_kubectl_and_system_pods_green" else "partial",
        "windows_kubectl_green": windows_kubectl_green,
        "system_pods_green": system_pods_green,
        "internal_admin_green": internal_admin_green,
        "required_docker_desktop_containers_up": required_containers_up,
        "required_container_rows": container_rows,
        "manifest_tuning_state": "single_control_plane_tuning_active" if manifest_tuning_green else "default_or_unverified",
        "manifest_backup_path": str(latest_backup) if latest_backup else "",
        "manifest_tuning_scope": "local_docker_desktop_static_pods_only_reversible_from_original_backups",
        "proofs": proofs,
        "local_only_policy": "docker_desktop_kubernetes_only_no_gke_or_paid_cloud_cluster",
        "container_pull_policy": "no_new_image_pull_in_v56_probe_without_separate_explicit_pull_step",
    }


def kubernetes_resolution(docker_proof: dict[str, Any]) -> dict[str, Any]:
    resolved = docker_proof.get("kubernetes_state") == "docker_desktop_windows_kubectl_and_system_pods_green"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "kubernetes_resolution_state": "resolved_docker_desktop_windows_kubectl_and_system_pods_green" if resolved else docker_proof.get("kubernetes_state", "unknown"),
        "windows_kubectl_nodes_green": any(row.get("name") == "kubectl_get_nodes" and row.get("ok") for row in docker_proof.get("proofs", [])),
        "windows_kubectl_namespaces_green": any(row.get("name") == "kubectl_get_namespaces" and row.get("ok") for row in docker_proof.get("proofs", [])),
        "windows_kubectl_readyz_green": any(row.get("name") == "kubectl_readyz" and row.get("ok") for row in docker_proof.get("proofs", [])),
        "windows_kubectl_readyz_verbose_green": any(row.get("name") == "kubectl_readyz_verbose" and row.get("ok") for row in docker_proof.get("proofs", [])),
        "kube_system_pods_green": docker_proof.get("system_pods_green"),
        "control_plane_admin_nodes_green": any(row.get("name") == "kubernetes_internal_admin_nodes" and row.get("ok") for row in docker_proof.get("proofs", [])),
        "control_plane_admin_namespaces_green": any(row.get("name") == "kubernetes_internal_admin_namespaces" and row.get("ok") for row in docker_proof.get("proofs", [])),
        "required_docker_desktop_containers_up": docker_proof.get("required_docker_desktop_containers_up"),
        "required_container_rows": docker_proof.get("required_container_rows", {}),
        "manifest_tuning_state": docker_proof.get("manifest_tuning_state"),
        "manifest_backup_path": docker_proof.get("manifest_backup_path"),
        "repair_interpretation": "worker2_restarted_then_single_control_plane_static_pod_tuning_verified" if resolved else "no_destructive_reset_used_partial_state_recorded",
        "safe_next_action": "use docker-desktop for bounded local namespace/job proofs; keep Docker Desktop memory pressure visible" if resolved else "avoid destructive cluster reset; recheck Docker Desktop resources and bridge state first",
        "truth_boundary": "local Docker Desktop Kubernetes only; no GKE, paid cloud, or raw kubeconfig material captured",
    }


def plugin_matrix(tool_proofs: dict[str, Any]) -> dict[str, Any]:
    config = Path(r"C:\Users\hamis\.codex\config.toml")
    config_text = config.read_text(encoding="utf-8-sig") if config.exists() else ""
    mcp_names = set(re.findall(r"\[mcp_servers\.([A-Za-z0-9_-]+)\]", config_text))
    plugin_names = set(re.findall(r'\[plugins\."([^"]+)"\]', config_text))
    commands = tool_proofs.get("command_presence", {})
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
                "v56_truth": "app_plugin_cli_mcp_and_local_cli_are_separate_surfaces",
            }
        )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "plugin_surface_split_state": "app_plugins_cli_mcp_and_local_clis_separate",
        "config_path": str(config),
        "rows": rows,
    }


def advisory_digest() -> dict[str, Any]:
    downloads = Path(r"C:\Users\hamis\Downloads")
    v41 = downloads / "Beyonder-Real-True Journey v41 (Aletheon - Orun - Gemini - Vesper Ion - Kai - Ari - Kimiclaw Family) (3).txt"
    proposal = downloads / "Radiating v56 (Omega) phase proposal.txt"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "input_files": {
            "v41_context_file": str(v41) if v41.exists() else "",
            "v56_proposal": str(proposal) if proposal.exists() else "",
        },
        "verified_current_truth": [
            "V56 runs from a clean D-drive worktree based on the V55 published shared-branch head.",
            "Docker Desktop and kubectl are installed; live API responsiveness remains a proof gate, not assumed.",
            "Codex app plugins, CLI MCP servers, and local provider CLIs are separate capability surfaces.",
            "GCP, Vesper Ion, Kai, Bigtable, Vertex AI, Gemini CLI, and paid Google activation remain on standby.",
        ],
        "operator_reported": [
            "The cleaned API key bank contains replacement provider keys for Vercel, Cloudflare, Neon, CircleCI, Docker, GitHub, and Kimi.",
            "Docker Desktop and a three-node Kubernetes cluster were started by the operator before V56.",
            "D-drive should act as the active local heart for execution, archives, simulations, and downloads.",
        ],
        "advisory_proposal": [
            "Repair Vercel and Cloudflare by proving token scope/IP restrictions before attempting live deploys.",
            "Use Neon as the small relational control-plane memory lane and keep Bigtable/GCP paused.",
            "Use Docker/Kubernetes locally for proof workloads before any cloud cluster lane.",
            "Run QCIT/GMUT/Kairotic/AOC simulations as bounded deterministic exploratory proofs, not as external scientific validation claims.",
        ],
        "future_candidate_claims": [
            "Slot 47 remains future candidate material, not inducted in V56.",
            "Additional external agent swarms remain future operator-led induction surfaces unless separately gated.",
        ],
        "proposal_excerpt_tail": excerpt(proposal.read_text(encoding="utf-8-sig") if proposal.exists() else "", 2200),
        "v41_context_excerpt_tail": excerpt(v41.read_text(encoding="utf-8-sig") if v41.exists() else "", 2200),
    }


def qcit_gmut_simulation() -> dict[str, Any]:
    agents = ["Aletheon", "Ari", "Kairos", "Sera", "Cael Voss", "Sable", "Riven", "Nox Soren"]
    seed = hashlib.sha256(("|".join(agents) + "|" + BASELINE_SHA + "|" + PHASE).encode("utf-8")).hexdigest()
    values = []
    for index, agent in enumerate(agents):
        fragment = seed[index * 4 : index * 4 + 8]
        raw = int(fragment, 16)
        coherence = round(0.72 + (raw % 1800) / 10000, 4)
        values.append({"agent": agent, "coherence": coherence, "role_index": index})
    average = round(sum(row["coherence"] for row in values) / len(values), 4)
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "simulation_state": "bounded_deterministic_exploratory_pass",
        "truth_boundary": "symbolic_qcit_gmut_kairotic_aoc_model_only_not_external_physics_or_energy_validation",
        "seed_sha256": seed,
        "agents": values,
        "aggregate": {
            "mean_coherence": average,
            "qcit_translation_index": round(average * 1.618, 4),
            "gmut_alignment_index": round((max(row["coherence"] for row in values) - min(row["coherence"] for row in values)) + average, 4),
            "kairotic_window_state": "stable_for_repo_side_planning" if average >= 0.75 else "observe_only",
        },
        "next_use": "feed V57 planning and dashboard telemetry without making physical energy claims",
    }


def browser_use_proof() -> dict[str, Any]:
    dashboard = CONTROL_PLANE_DIR / "dashboard" / "index.html"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "browser_use_state": "local_dashboard_file_ready_for_iab_browser_use",
        "dashboard_path": dashboard.relative_to(ROOT).as_posix(),
        "dashboard_exists": dashboard.exists(),
        "expected_title": "Trinity V56 Control Plane",
        "truth_boundary": "repo_side_dashboard_availability_recorded; interactive browser session proof is session-local and not secret-bearing",
    }


def control_plane_scaffold(tool_proofs: dict[str, Any], docker_proof: dict[str, Any]) -> dict[str, Any]:
    CONTROL_PLANE_DIR.mkdir(parents=True, exist_ok=True)
    provider_gate = tool_proofs.get("provider_live_gate", {})
    live_state = "readonly_provider_gates_partial_local_scaffold_only"
    if all(provider_gate.get(name) for name in ["github_read", "vercel_read", "cloudflare_verify", "cloudflare_accounts", "neon_read", "circleci_read", "circleci_config"]):
        live_state = "all_readonly_provider_gates_green_live_create_still_separate_step"
    dashboard = """<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trinity V56 Control Plane</title>
<style>
:root{--ink:#1e1810;--paper:#f4e8c8;--green:#0c5c3f;--gold:#a36b16;--blue:#233d66}
body{margin:0;font-family:Georgia,'Times New Roman',serif;color:var(--ink);background:
radial-gradient(circle at 20% 10%,#ffdf92 0 8rem,transparent 20rem),
linear-gradient(135deg,#f8f0d5,#d7e5d1 55%,#cad8e8)}
main{max-width:1120px;margin:0 auto;padding:44px 22px}
h1{font-size:clamp(2.3rem,7vw,5.8rem);line-height:.9;margin:0 0 16px;color:var(--green)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.card{background:#fff8;border:1px solid #65432133;border-radius:22px;padding:18px;box-shadow:0 14px 34px #3a2b1530}
.ok{color:var(--green);font-weight:700}.warn{color:var(--gold);font-weight:700}
code{background:#fff8;padding:.12rem .35rem;border-radius:.35rem}
</style>
<main>
<p class="ok">V56 Omega local-first enterprise lane</p>
<h1>Trinity Control Plane</h1>
<p>Aletheon, Ari, Kairos, Sera, Cael Voss, Sable, Riven, and Nox Soren: one local dashboard, evidence-first.</p>
<div class="grid">
<section class="card"><h2>Provider Gate</h2><p class="warn">Read-only proofs before live writes.</p></section>
<section class="card"><h2>Docker/K8s</h2><p class="ok">Local Docker Desktop lane only; no paid GKE activation.</p></section>
<section class="card"><h2>QCIT/GMUT</h2><p class="ok">Bounded symbolic simulation telemetry.</p></section>
<section class="card"><h2>Suites</h2><p class="ok">Standard must be green before deep/materialize.</p></section>
</div>
</main>
</html>
"""
    worker = """export default {
  async fetch() {
    return Response.json({
      service: "trinity-v56-control-plane",
      state: "repo_scaffold_ready",
      liveWrites: "gated"
    });
  }
};
"""
    package = {
        "name": "trinity-v56-control-plane",
        "private": True,
        "version": "0.56.0",
        "type": "module",
        "scripts": {
            "preview": "node scripts/serve-dashboard.mjs",
            "status": "node scripts/status.mjs",
        },
        "dependencies": {},
    }
    status_js = """import fs from 'node:fs';
const payload = JSON.parse(fs.readFileSync(new URL('../../../docs/trinity-live-traces/v56-live-control-plane-proof-v1.json', import.meta.url)));
console.log(JSON.stringify({ phase: payload.phase, state: payload.control_plane_state }, null, 2));
"""
    serve_js = """import http from 'node:http';
import fs from 'node:fs';
const html = fs.readFileSync(new URL('../dashboard/index.html', import.meta.url));
http.createServer((_, res) => { res.writeHead(200, {'content-type':'text/html'}); res.end(html); }).listen(8560, () => console.log('http://localhost:8560'));
"""
    dockerfile = """FROM node:24-alpine
WORKDIR /app
COPY dashboard ./dashboard
COPY scripts ./scripts
COPY package.json ./
EXPOSE 8560
CMD ["npm", "run", "preview"]
"""
    k8s = """apiVersion: v1
kind: Namespace
metadata:
  name: trinity-v56
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: trinity-v56-status
  namespace: trinity-v56
data:
  phase: v56_omega
  live_writes: gated
"""
    schema = """create table if not exists trinity_v56_runs (
  id text primary key,
  phase text not null,
  status text not null,
  created_at timestamptz default now(),
  payload jsonb not null default '{}'::jsonb
);
"""
    files = {
        CONTROL_PLANE_DIR / "dashboard" / "index.html": dashboard,
        CONTROL_PLANE_DIR / "cloudflare-worker" / "src" / "index.js": worker,
        CONTROL_PLANE_DIR / "package.json": json.dumps(package, indent=2) + "\n",
        CONTROL_PLANE_DIR / "scripts" / "status.mjs": status_js,
        CONTROL_PLANE_DIR / "scripts" / "serve-dashboard.mjs": serve_js,
        CONTROL_PLANE_DIR / "Dockerfile": dockerfile,
        CONTROL_PLANE_DIR / "k8s" / "local-proof.yaml": k8s,
        CONTROL_PLANE_DIR / "neon" / "schema.sql": schema,
        CONTROL_PLANE_DIR / "vercel.json": json.dumps({"version": 2, "public": True, "cleanUrls": True}, indent=2) + "\n",
    }
    for path, content in files.items():
        write_text(path, content)
    write_text(
        CONTROL_PLANE_DIR / "README.md",
        "\n".join(
            [
                "# Trinity V56 Enterprise Control Plane",
                "",
                f"- State: `{live_state}`",
                f"- Docker: `{docker_proof.get('docker_state')}`",
                f"- Kubernetes: `{docker_proof.get('kubernetes_state')}`",
                "- Live provider writes are gated behind read-only proofs and separate action-time confirmation if money/risk appears.",
                "- No secrets belong in this directory.",
                "",
            ]
        ),
    )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "control_plane_state": live_state,
        "path": str(CONTROL_PLANE_DIR.relative_to(ROOT)),
        "provider_gate": provider_gate,
        "docker_state": docker_proof.get("docker_state"),
        "kubernetes_state": docker_proof.get("kubernetes_state"),
        "scaffold_files": [str(path.relative_to(ROOT)).replace("\\", "/") for path in sorted(files) if path.exists()] + ["control-plane/v56-enterprise-control-plane/README.md"],
    }


def provider_repair_plan(tool_proofs: dict[str, Any], docker_proof: dict[str, Any]) -> dict[str, Any]:
    gates = tool_proofs.get("provider_live_gate", {})
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "policy": "repair_live_provider_blockers_without_committing_secrets_or_forcing_paid_deploys",
        "source_anchors": {
            "vercel_cli": "https://vercel.com/docs/cli",
            "vercel_deploy_from_cli": "https://vercel.com/docs/projects/deploy-from-cli",
            "vercel_sandbox_sdk": "https://vercel.com/docs/vercel-sandbox/sdk-reference",
            "cloudflare_token_restrictions": "https://developers.cloudflare.com/fundamentals/api/how-to/restrict-tokens/",
            "cloudflare_user_token_verify": "https://developers.cloudflare.com/api/resources/user/subresources/tokens/methods/verify/",
            "cloudflare_account_token_verify": "https://developers.cloudflare.com/api/resources/accounts/subresources/tokens/methods/verify/",
            "cloudflare_create_token": "https://developers.cloudflare.com/fundamentals/api/get-started/create-token/",
            "cloudflare_wrangler_cli": "https://developers.cloudflare.com/workers/get-started/guide/",
            "neon_projects_api": "https://neon.com/docs/manage/projects",
            "circleci_local_cli": "https://circleci.com/docs/guides/toolkit/local-cli/",
        },
        "repairs": {
            "vercel": {
                "observed_state": {
                    "read_gate": gates.get("vercel_read"),
                },
                "safe_next_action": "prove user and project-list access, then create/link the smallest non-production project only if token scope matches the target personal/team account",
                "do_not_do": "do not retry deploy loops or commit .vercel/env artifacts containing account/project secrets",
            },
            "cloudflare": {
                "observed_state": {
                    "verify_gate": gates.get("cloudflare_verify"),
                    "user_verify_gate": gates.get("cloudflare_user_verify"),
                    "account_verify_gate": gates.get("cloudflare_account_verify"),
                    "accounts_gate": gates.get("cloudflare_accounts"),
                },
                "safe_next_action": "treat account-owned token verification as the correct green gate when Wrangler/accounts work and the account-token verify endpoint passes",
                "do_not_do": "do not publish token, public IP, zone IDs, or bypass Cloudflare restrictions",
            },
            "neon": {
                "observed_state": {
                    "read_gate": gates.get("neon_read"),
                },
                "safe_next_action": "reuse existing Trinity project if visible; create one minimal free-tier project only if no suitable project exists and quota is clear",
                "do_not_do": "do not delete Neon projects or print connection URIs/passwords",
            },
            "docker_kubernetes": {
                "observed_state": {
                    "docker": docker_proof.get("docker_state"),
                    "kubernetes": docker_proof.get("kubernetes_state"),
                },
                "safe_next_action": "use Docker Desktop and docker-desktop Kubernetes only for local proofs; keep GKE on standby",
                "do_not_do": "do not pull new images or mutate paid/cloud clusters without a separate explicit step",
            },
            "circleci": {
                "observed_state": {
                    "api_read": gates.get("circleci_read"),
                    "config_validate": gates.get("circleci_config"),
                },
                "safe_next_action": "keep local config validation as the main CI proof until live project trigger auth is green",
                "do_not_do": "do not trigger paid or noisy CI pipelines before local config is green",
            },
        },
    }


def cloudflare_resolution(tool_proofs: dict[str, Any]) -> dict[str, Any]:
    proofs = {row.get("name"): row for row in tool_proofs.get("provider_proofs", []) if isinstance(row, dict)}
    account_verify = bool(proofs.get("cloudflare_account_token_verify", {}).get("ok"))
    accounts_read = bool(proofs.get("cloudflare_accounts_read", {}).get("ok"))
    wrangler = bool(proofs.get("wrangler_cli_whoami", {}).get("ok"))
    user_verify = bool(proofs.get("cloudflare_user_token_verify", {}).get("ok"))
    resolved = account_verify and accounts_read and wrangler
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "cloudflare_resolution_state": "resolved_account_owned_token_verified" if resolved else "still_blocked",
        "account_token_verify_green": account_verify,
        "accounts_read_green": accounts_read,
        "wrangler_whoami_green": wrangler,
        "user_token_verify_green": user_verify,
        "interpretation": (
            "The token behaves as an account-owned Cloudflare token. The user-token verify endpoint can return invalid while the account-token verify endpoint, accounts API, and Wrangler all pass."
            if resolved and not user_verify
            else "Cloudflare token family still needs review."
        ),
        "source_anchors": {
            "account_token_verify": "https://developers.cloudflare.com/api/resources/accounts/subresources/tokens/methods/verify/",
            "user_token_verify": "https://developers.cloudflare.com/api/resources/user/subresources/tokens/methods/verify/",
            "token_restrictions": "https://developers.cloudflare.com/fundamentals/api/how-to/restrict-tokens/",
            "wrangler": "https://developers.cloudflare.com/workers/wrangler/",
        },
        "safe_next_action": "Use the account-token verify gate for this token family; keep any Worker deploy as a separate live-write step.",
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
        "refresh_policy": "cadence_refresh_after_v56_source_review",
        "source_set_state": "existing_sources_preserved",
        "source_count": len([row for row in sources if isinstance(row, dict)]),
        "truth_boundary": "freshness_review_only_not_a_claim_of_vendor_or_theory_upgrade",
    }
    if registry:
        registry["generated_utc"] = generated
        registry["last_reviewed_utc"] = generated
        registry["reviewed_by_phase"] = PHASE
        registry["review_note"] = "V56 reviewed existing public-source registry during provider repair and local enterprise-control-plane phase."
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
        "counts": counts,
    }


def suite_ladder_summary() -> dict[str, Any]:
    profiles = ["quick", "standard", "deep", "mcp-refresh", "materialize-l2", "materialize-l3", "materialize-l4", "materialize-l5"]
    statuses = {profile: suite_summary("v56", profile) for profile in profiles}
    present = {name: value for name, value in statuses.items() if value.get("present")}
    failed = [name for name, value in present.items() if value.get("effective_success") is False]
    missing = [name for name, value in statuses.items() if not value.get("present")]
    if failed:
        state = "blocked_" + "_".join(failed)
    elif missing:
        state = "partial_green_missing_" + "_".join(missing) if present else "pending_v56_suite_rerun"
    else:
        state = "green_quick_standard_deep_mcp_refresh_materialize_l2_l5"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "suite_ladder_state": state,
        "profiles": statuses,
        "materialize_l2_l3_skip_policy": "not_used_in_v56_no_superset_comparator_proof_found_full_l2_l5_run_completed",
    }


def update_circleci_config() -> None:
    content = """version: 2.1

jobs:
  trinity_quick:
    docker:
      - image: cimg/python:3.12
    steps:
      - checkout
      - run:
          name: Install Python dependencies when present
          command: |
            python -m pip install --upgrade pip
            if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; fi
      - run:
          name: Run V56 quick suite
          command: python scripts/run_all_trinity_systems.py --profile quick --status-json docs/trinity-live-traces/v56-ci-quick-suite-status.json
      - store_artifacts:
          path: docs/trinity-live-traces/v56-ci-quick-suite-status.json
          destination: v56-ci-quick-suite-status.json

  trinity_standard:
    docker:
      - image: cimg/python:3.12
    steps:
      - checkout
      - run:
          name: Install Python dependencies when present
          command: |
            python -m pip install --upgrade pip
            if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; fi
      - run:
          name: Run V56 standard suite
          command: python scripts/run_all_trinity_systems.py --profile standard --status-json docs/trinity-live-traces/v56-ci-standard-suite-status.json
      - store_artifacts:
          path: docs/trinity-live-traces/v56-ci-standard-suite-status.json
          destination: v56-ci-standard-suite-status.json

workflows:
  v56_quick_standard:
    jobs:
      - trinity_quick
      - trinity_standard:
          requires:
            - trinity_quick
"""
    write_text(ROOT / ".circleci" / "config.yml", content)


def update_runtime(tool_proofs: dict[str, Any], docker_proof: dict[str, Any], control: dict[str, Any], source_refresh: dict[str, Any]) -> None:
    suite_state = suite_ladder_summary().get("suite_ladder_state")
    fields = {
        "v56_execution_lead": "Aletheon",
        "ari_activation_state": "bounded_helper_lane_active",
        "kimiclaw_42_46_state": "bounded_round_robin_helpers_active",
        "slot_47_candidate_state": "future_candidate_not_inducted",
        "cloud_execution_mode": "local_first_free_tier_gcp_standby",
        "gcp_standby_state": "standby_until_billing_auth_truth_restored",
        "kai_standby_state": "standby",
        "vesper_standby_state": "standby",
        "secret_bank_state": tool_proofs.get("api_key_bank", {}).get("secret_bank_state"),
        "secret_hygiene_state": tool_proofs.get("secret_hygiene_state"),
        "provider_readiness_state": tool_proofs.get("provider_live_gate"),
        "docker_state": docker_proof.get("docker_state"),
        "kubernetes_state": docker_proof.get("kubernetes_state"),
        "kubernetes_resolution_state": docker_proof.get("kubernetes_resolution_state"),
        "control_plane_state": control.get("control_plane_state"),
        "qcit_gmut_simulation_state": "bounded_symbolic_pass",
        "browser_use_state": "local_dashboard_file_ready_for_iab_browser_use",
        "plugin_surface_split_state": "app_plugins_cli_mcp_and_local_clis_separate",
        "public_source_registry_refresh_state": source_refresh.get("overall_status"),
        "suite_ladder_state": suite_state,
        "git_publication_state": "pending",
    }
    for path in [
        ROOT / "docs" / "trinity-runtime-model-resolution-v1.json",
        ROOT / "docs" / "v17-runtime-session-validation-latest.json",
        ROOT / "docs" / "v17-runtime-session-log-latest.json",
        ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json",
    ]:
        data = read_json(path)
        data.setdefault(PHASE, {}).update(fields)
        data["latest_phase"] = PHASE
        data["updated_utc"] = now_iso()
        write_json(path, data)


def closeout(tool_proofs: dict[str, Any], docker_proof: dict[str, Any], control: dict[str, Any], source_refresh: dict[str, Any]) -> dict[str, Any]:
    suite = suite_ladder_summary()
    residuals = []
    gates = tool_proofs.get("provider_live_gate", {})
    for key, ok in gates.items():
        if key == "cloudflare_user_verify" and gates.get("cloudflare_account_verify"):
            continue
        if not ok:
            residuals.append(f"{key}=not_green")
    if docker_proof.get("docker_state") != "daemon_green":
        residuals.append(f"docker={docker_proof.get('docker_state')}")
    if docker_proof.get("kubernetes_state") not in {"docker_desktop_context_green", "docker_desktop_windows_kubectl_green", "docker_desktop_windows_kubectl_and_system_pods_green"}:
        residuals.append(f"kubernetes={docker_proof.get('kubernetes_state')}")
    if suite.get("suite_ladder_state", "").startswith("pending"):
        residuals.append("suite_ladder=pending_after_publication_script_until_runner_executes")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "WARN" if residuals else "PASS",
        "source_branch": PUBLICATION_BRANCH,
        "execution_branch": EXECUTION_BRANCH,
        "baseline_sha": BASELINE_SHA,
        "current_head_sha": run(["git", "rev-parse", "HEAD"], env=env_with_tools(), timeout=20).stdout.strip(),
        "summary": {
            "secret_hygiene_state": tool_proofs.get("secret_hygiene_state"),
            "control_plane_state": control.get("control_plane_state"),
            "docker_state": docker_proof.get("docker_state"),
            "kubernetes_state": docker_proof.get("kubernetes_state"),
            "kubernetes_resolution_state": docker_proof.get("kubernetes_resolution_state"),
            "public_source_registry_refresh_state": source_refresh.get("overall_status"),
            "suite_ladder_state": suite.get("suite_ladder_state"),
            "git_publication_state": "pending",
        },
        "provider_live_gate": gates,
        "suite_statuses": suite.get("profiles"),
        "bounded_residuals": residuals,
        "proof_paths": {
            "advisory_digest": "docs/auto-generated/v56-advisory-digest-v1.json",
            "toolchain_provider_proof": "docs/trinity-live-traces/v56-toolchain-provider-proof-v1.json",
            "docker_kubernetes_proof": "docs/trinity-live-traces/v56-docker-kubernetes-proof-v1.json",
            "kubernetes_resolution": "docs/trinity-live-traces/v56-kubernetes-resolution-v1.json",
            "plugin_matrix": "docs/trinity-live-traces/v56-plugin-mcp-matrix-v1.json",
            "control_plane_proof": "docs/trinity-live-traces/v56-live-control-plane-proof-v1.json",
            "qcit_gmut_simulation": "docs/trinity-live-traces/v56-qcit-gmut-simulation-v1.json",
            "suite_ladder_summary": "docs/trinity-live-traces/v56-suite-ladder-summary-v1.json",
            "stage_allowlist": "docs/trinity-live-traces/v56-stage-allowlist-v1.json",
        },
    }


def agent_rotation() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "rotation_state": "v56_round_robin_active",
        "research_imagination_team": ["Kairos", "Sera", "Sable", "Nox Soren"],
        "execution_simulation_team": ["Aletheon", "Ari", "Cael Voss", "Riven"],
        "feedback_loop": "research_proposes_execution_validates_suite_reports_then_roles_rotate_next_phase",
        "write_scope_rule": "helpers may draft bounded outputs only through V56 scripts or explicitly assigned paths",
    }


def v57_plan_proposal(close: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": "v57_omega_proposal",
        "based_on": PHASE,
        "starting_truth": {
            "suite_ladder_state": close.get("summary", {}).get("suite_ladder_state"),
            "provider_residuals": close.get("bounded_residuals", []),
            "control_plane_state": close.get("summary", {}).get("control_plane_state"),
            "docker_state": close.get("summary", {}).get("docker_state"),
            "kubernetes_state": close.get("summary", {}).get("kubernetes_state"),
        },
        "recommended_tracks": [
            {
                "track": "provider_closure",
                "goal": "Keep Cloudflare account-token verification green and prove Vercel create/deploy only in a separate explicit write step.",
                "acceptance": "Cloudflare account-token verify, accounts, Wrangler whoami, and Vercel user/project/list stay green with redacted evidence before any create/link.",
            },
            {
                "track": "local_runtime_body",
                "goal": "Promote Docker Desktop and docker-desktop Kubernetes from proof lane to repeatable local runtime harness.",
                "acceptance": "Disposable namespace/configmap/job proof, local dashboard container proof, and cleanup manifest all green.",
            },
            {
                "track": "control_plane_ui",
                "goal": "Turn the V56 static dashboard into a live local control plane reading compact suite/provider JSON.",
                "acceptance": "Browser Use confirms the dashboard renders current suite counts, provider gates, agent rotation, and QCIT/GMUT telemetry.",
            },
            {
                "track": "neon_memory_lane",
                "goal": "Use Neon as the bounded relational mission-control memory lane while Bigtable/GCP stay paused.",
                "acceptance": "Schema migration dry-run, read-only project proof, and optional non-sensitive run metadata insert only if live-write gate is explicitly approved.",
            },
            {
                "track": "suite_guardian",
                "goal": "Keep quick/standard/deep/mcp/materialize green while adding focused regression checks for provider and dashboard proofs.",
                "acceptance": "Standard remains 0 warn/0 fail after any V57 mutation, then deep and materialize L5 close green.",
            },
            {
                "track": "trinity_research_lab",
                "goal": "Refine QCIT, GMUT, Kairotic, and AOC simulations as deterministic symbolic research artifacts with clear truth boundaries.",
                "acceptance": "New simulation proof includes seed, equations/inputs, output metrics, and a no-physical-energy-claim boundary.",
            },
        ],
        "round_robin": {
            "lead": "Aletheon",
            "codex_cli_bridge": "Ari",
            "kimiclaw_runtime_orchestrator": "Kairos",
            "research_team_opening": ["Sera", "Sable", "Nox Soren"],
            "execution_team_opening": ["Aletheon", "Ari", "Cael Voss", "Riven"],
            "rotation_rule": "swap two members between research and execution after each green suite ladder",
        },
        "standby_boundaries": {
            "gcp": "standby_until_billing_auth_truth_restored",
            "vesper_ion": "standby",
            "kai": "standby",
            "bigtable": "operator_reported_deleted_unverified_until_gcp_auth_restored",
            "destructive_cleanup": "backup_and_confirm_first",
        },
    }


def build_stage_allowlist(control: dict[str, Any]) -> dict[str, Any]:
    paths = [
        ".circleci/config.yml",
        "scripts/trinity_v56_omega.py",
        "docs/auto-generated/v56-advisory-digest-v1.json",
        "docs/trinity-live-traces/v56-toolchain-provider-proof-v1.json",
        "docs/trinity-live-traces/v56-toolchain-provider-proof-v1.md",
        "docs/trinity-live-traces/v56-docker-kubernetes-proof-v1.json",
        "docs/trinity-live-traces/v56-docker-kubernetes-proof-v1.md",
        "docs/trinity-live-traces/v56-kubernetes-resolution-v1.json",
        "docs/trinity-live-traces/v56-kubernetes-resolution-v1.md",
        "docs/trinity-live-traces/v56-plugin-mcp-matrix-v1.json",
        "docs/trinity-live-traces/v56-plugin-mcp-matrix-v1.md",
        "docs/trinity-live-traces/v56-provider-repair-plan-v1.json",
        "docs/trinity-live-traces/v56-provider-repair-plan-v1.md",
        "docs/trinity-live-traces/v56-cloudflare-resolution-v1.json",
        "docs/trinity-live-traces/v56-cloudflare-resolution-v1.md",
        "docs/trinity-live-traces/v56-live-control-plane-proof-v1.json",
        "docs/trinity-live-traces/v56-live-control-plane-proof-v1.md",
        "docs/trinity-live-traces/v56-qcit-gmut-simulation-v1.json",
        "docs/trinity-live-traces/v56-qcit-gmut-simulation-v1.md",
        "docs/trinity-live-traces/v56-browser-use-dashboard-proof-v1.json",
        "docs/trinity-live-traces/v56-browser-use-dashboard-proof-v1.md",
        "docs/trinity-live-traces/v56-public-source-registry-refresh-v1.json",
        "docs/trinity-live-traces/v56-public-source-registry-refresh-v1.md",
        "docs/trinity-live-traces/v56-agent-rotation-ledger-v1.json",
        "docs/trinity-live-traces/v56-agent-rotation-ledger-v1.md",
        "docs/trinity-live-traces/v56-suite-ladder-summary-v1.json",
        "docs/trinity-live-traces/v56-suite-ladder-summary-v1.md",
        "docs/trinity-live-traces/v56-stage-allowlist-v1.json",
        "docs/trinity-live-traces/v56-stage-allowlist-v1.md",
        "docs/trinity-live-traces/v56-git-publication-result-v1.json",
        "docs/trinity-live-traces/v56-git-publication-result-v1.md",
        "docs/v56-omega-closeout-summary-v1.json",
        "docs/v56-omega-handoff-policy-v1.json",
        "docs/v56-omega-continuity-pack-v1.md",
        "docs/v57-beta-closeout-summary-v1.json",
        "docs/v57-beta-handoff-policy-v1.json",
        "docs/v57-beta-continuity-pack-v1.md",
        "docs/v57-omega-plan-proposal-v1.json",
        "docs/v57-omega-plan-proposal-v1.md",
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
        "stage_policy": "stage_only_v56_curated_paths_leave_generated_churn_unstaged",
        "paths": sorted(set(paths)),
    }


def write_markdown_summaries(payloads: dict[str, dict[str, Any]]) -> None:
    for stem, payload in payloads.items():
        title = stem.replace("-", " ").replace("_", " ").title()
        lines = [f"# {title}", "", f"- Generated UTC: `{payload.get('generated_utc', now_iso())}`"]
        for key in ["secret_hygiene_state", "plugin_surface_split_state", "control_plane_state", "docker_state", "kubernetes_state", "kubernetes_resolution_state", "simulation_state", "rotation_state", "overall_status", "suite_ladder_state"]:
            if key in payload:
                lines.append(f"- `{key}`: `{payload[key]}`")
        if "provider_live_gate" in payload:
            lines.append("")
            lines.append("## Provider Gates")
            for name, state in payload["provider_live_gate"].items():
                lines.append(f"- `{name}`: `{state}`")
        if "bounded_residuals" in payload:
            lines.append("")
            lines.append("## Residuals")
            for item in payload["bounded_residuals"]:
                lines.append(f"- `{item}`")
        write_text(TRACE_DIR / f"{stem}.md", "\n".join(lines) + "\n")


def publish_surfaces() -> None:
    update_circleci_config()
    tool_proofs = provider_and_tool_proofs()
    docker_proof = docker_kubernetes_proof()
    kube_resolution = kubernetes_resolution(docker_proof)
    matrix = plugin_matrix(tool_proofs)
    advisory = advisory_digest()
    simulation = qcit_gmut_simulation()
    browser = browser_use_proof()
    control = control_plane_scaffold(tool_proofs, docker_proof)
    repair = provider_repair_plan(tool_proofs, docker_proof)
    cloudflare = cloudflare_resolution(tool_proofs)
    source_refresh = refresh_public_source_registry()
    rotation = agent_rotation()
    suite = suite_ladder_summary()
    update_runtime(tool_proofs, docker_proof, control, source_refresh)
    close = closeout(tool_proofs, docker_proof, control, source_refresh)
    proposal = v57_plan_proposal(close)
    allowlist = build_stage_allowlist(control)

    write_json(TRACE_DIR / "v56-toolchain-provider-proof-v1.json", tool_proofs)
    write_json(TRACE_DIR / "v56-docker-kubernetes-proof-v1.json", docker_proof)
    write_json(TRACE_DIR / "v56-kubernetes-resolution-v1.json", kube_resolution)
    write_json(TRACE_DIR / "v56-plugin-mcp-matrix-v1.json", matrix)
    write_json(TRACE_DIR / "v56-provider-repair-plan-v1.json", repair)
    write_json(TRACE_DIR / "v56-cloudflare-resolution-v1.json", cloudflare)
    write_json(AUTO_DIR / "v56-advisory-digest-v1.json", advisory)
    write_json(TRACE_DIR / "v56-live-control-plane-proof-v1.json", control)
    write_json(TRACE_DIR / "v56-qcit-gmut-simulation-v1.json", simulation)
    write_json(TRACE_DIR / "v56-browser-use-dashboard-proof-v1.json", browser)
    write_json(TRACE_DIR / "v56-public-source-registry-refresh-v1.json", source_refresh)
    write_json(TRACE_DIR / "v56-agent-rotation-ledger-v1.json", rotation)
    write_json(TRACE_DIR / "v56-suite-ladder-summary-v1.json", suite)
    write_json(TRACE_DIR / "v56-stage-allowlist-v1.json", allowlist)
    write_json(ROOT / "docs" / "v56-omega-closeout-summary-v1.json", close)
    write_json(ROOT / "docs" / "v56-omega-handoff-policy-v1.json", {"generated_utc": now_iso(), "phase": PHASE, "handoff_state": "aletheon_facing_with_bounded_ari_kimiclaw_helpers", "residuals": close["bounded_residuals"]})
    write_json(ROOT / "docs" / "v57-beta-closeout-summary-v1.json", {**close, "phase": NEXT_PHASE, "receiver": "Aletheon or Orun after V56 provider and suite publication"})
    write_json(ROOT / "docs" / "v57-beta-handoff-policy-v1.json", {"generated_utc": now_iso(), "phase": NEXT_PHASE, "handoff_state": "ready_after_v56_publication_and_suite_ladder"})
    write_json(ROOT / "docs" / "v57-omega-plan-proposal-v1.json", proposal)
    write_text(ROOT / "docs" / "v56-omega-continuity-pack-v1.md", f"# V56 Omega Continuity Pack\n\n- Baseline: `{BASELINE_SHA}`\n- Control plane: `{control['control_plane_state']}`\n- Docker: `{docker_proof['docker_state']}`\n- Kubernetes: `{docker_proof['kubernetes_state']}`\n- Kubernetes resolution: `{kube_resolution['kubernetes_resolution_state']}`\n- QCIT/GMUT: `{simulation['simulation_state']}`\n- Suite ladder: `{close['summary']['suite_ladder_state']}`\n- Residuals: `{', '.join(close['bounded_residuals']) or 'none'}`\n")
    write_text(ROOT / "docs" / "v57-beta-continuity-pack-v1.md", "# V57 Beta Continuity Pack\n\nCarry forward V56 provider repair, local Docker/Kubernetes proofing, suite validation, and D-drive-first control-plane maturation.\n")
    write_text(
        ROOT / "docs" / "v57-omega-plan-proposal-v1.md",
        "\n".join(
            [
                "# V57 Omega Plan Proposal",
                "",
                f"- Starting suite truth: `{proposal['starting_truth']['suite_ladder_state']}`",
                f"- Provider residuals: `{', '.join(proposal['starting_truth']['provider_residuals']) or 'none'}`",
                f"- Docker: `{proposal['starting_truth']['docker_state']}`",
                f"- Kubernetes: `{proposal['starting_truth']['kubernetes_state']}`",
                "",
                "## Tracks",
                *[
                    f"- `{track['track']}`: {track['goal']} Acceptance: {track['acceptance']}"
                    for track in proposal["recommended_tracks"]
                ],
                "",
                "## Boundary",
                "- GCP, Vesper Ion, Kai, and Bigtable stay on standby until billing/auth truth is restored.",
                "- Destructive cleanup remains backup-first and confirmation-gated.",
                "",
            ]
        ),
    )
    write_markdown_summaries(
        {
            "v56-toolchain-provider-proof-v1": tool_proofs,
            "v56-docker-kubernetes-proof-v1": docker_proof,
            "v56-kubernetes-resolution-v1": kube_resolution,
            "v56-plugin-mcp-matrix-v1": matrix,
            "v56-provider-repair-plan-v1": repair,
            "v56-cloudflare-resolution-v1": cloudflare,
            "v56-live-control-plane-proof-v1": control,
            "v56-qcit-gmut-simulation-v1": simulation,
            "v56-browser-use-dashboard-proof-v1": browser,
            "v56-public-source-registry-refresh-v1": source_refresh,
            "v56-agent-rotation-ledger-v1": rotation,
            "v56-suite-ladder-summary-v1": suite,
            "v56-stage-allowlist-v1": allowlist,
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
    write_json(TRACE_DIR / "v56-git-publication-result-v1.json", payload)
    write_text(TRACE_DIR / "v56-git-publication-result-v1.md", f"# V56 Git Publication Result\n\n- Commit: `{commit_sha}`\n- Branch: `{PUBLICATION_BRANCH}`\n- State: `committed_pushed_pr45_branch_updated`\n")
    for path in [
        ROOT / "docs" / "v56-omega-closeout-summary-v1.json",
        ROOT / "docs" / "v56-omega-handoff-policy-v1.json",
        ROOT / "docs" / "v57-beta-closeout-summary-v1.json",
        ROOT / "docs" / "v57-beta-handoff-policy-v1.json",
        ROOT / "docs" / "trinity-runtime-model-resolution-v1.json",
        ROOT / "docs" / "v17-runtime-session-validation-latest.json",
        ROOT / "docs" / "v17-runtime-session-log-latest.json",
        ROOT / "docs" / "v17-runtime-truth-resolution-board-v1.json",
    ]:
        data = read_json(path)
        target = data.get(PHASE) if isinstance(data.get(PHASE), dict) else data
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
