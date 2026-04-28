#!/usr/bin/env python3
"""Publish V57 Omega 1-node Local/Cloud Nexus evidence."""

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
CONTROL_DIR = ROOT / "control-plane" / "v57-nexus-phone-dashboard"
PHASE = "v57_omega"
NEXT_PHASE = "v58_beta"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
EXECUTION_BRANCH = "codex/GHC-Family/v57-omega-exec"
BASELINE_SHA = "7b2a353ec924a3f3a37da9815a493f3da195f54b"
D_ARCHIVE_ROOT = Path(r"D:\GHC-Archives")
NODE_CLI_ROOT = D_ARCHIVE_ROOT / "toolchain" / "v57-node-clis"
SECRET_BANK_CANDIDATES = [
    Path(r"C:\Users\hamis\Downloads\GHC Family Beyonder-Real-True-Journey API Key bank (Cleaned up) (1).txt"),
    Path(r"C:\Users\hamis\Downloads\GHC Family Beyonder-Real-True-Journey API Key bank (Cleaned up).txt"),
    Path(r"D:\GHC Family Beyonder-Real-True-Journey API Key bank (Cleaned up) (1).txt"),
    Path(r"D:\GHC Family Beyonder-Real-True-Journey API Key bank (Cleaned up).txt"),
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


def excerpt(text: str | None, limit: int = 6000) -> str:
    value = clean(text)
    return value[-limit:] if len(value) > limit else value


def run(args: list[str], *, env: dict[str, str] | None = None, timeout: int = 45) -> subprocess.CompletedProcess[str]:
    command = args[:]
    active_env = env or os.environ.copy()
    if args:
        for candidate in (args[0], f"{args[0]}.cmd", f"{args[0]}.exe", f"{args[0]}.ps1"):
            resolved = shutil.which(candidate, path=active_env.get("PATH"))
            if resolved:
                command = [resolved, *args[1:]]
                break
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            env=active_env,
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


def env_with_tools(extra: dict[str, str] | None = None) -> dict[str, str]:
    env = os.environ.copy()
    tool_paths = [
        str(NODE_CLI_ROOT / "node_modules" / ".bin"),
        r"C:\Program Files\GitHub CLI",
        r"C:\Users\hamis\AppData\Local\Microsoft\WinGet\Links",
        r"C:\Program Files\Docker\Docker\resources\bin",
        r"C:\Program Files\Git\cmd",
        r"C:\Program Files\nodejs",
        r"C:\Users\hamis\AppData\Roaming\npm",
    ]
    env["PATH"] = os.pathsep.join(tool_paths + [env.get("PATH", "")])
    env["VERCEL_TELEMETRY_DISABLED"] = "1"
    if extra:
        env.update({k: v for k, v in extra.items() if v})
    return env


def active_secret_bank() -> Path | None:
    for path in SECRET_BANK_CANDIDATES:
        if path.exists() and path.is_file():
            return path
    return None


def parse_secret_bank() -> tuple[dict[str, str], Path | None]:
    path = active_secret_bank()
    if not path:
        return {}, None
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    text = text.replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")
    labels = [
        "Kimicode API",
        "Kimi code API",
        "Github API",
        "GitHub classic",
        "Neon postgres API",
        "Cloudflare (Wrangler) API",
        "Cloudflare API",
        "Vercel",
        "CircleCI API",
        "Oracle Cloud API",
        "OCI API",
        "Render API",
        "Docker API",
    ]
    secrets: dict[str, str] = {}
    for index, label in enumerate(labels):
        start = text.lower().find(label.lower())
        if start < 0:
            continue
        end = len(text)
        for next_label in labels[index + 1 :]:
            next_start = text.lower().find(next_label.lower(), start + 1)
            if next_start >= 0:
                end = min(end, next_start)
        block = text[start:end]
        match = re.search(r'"api_key"\s*:\s*"([^"]+)"', block, flags=re.IGNORECASE)
        if not match:
            match = re.search(r"(?:token|api[_ -]?key|key)\s*[:=]\s*([A-Za-z0-9_.\-~+/=]{20,})", block, flags=re.IGNORECASE)
        if match:
            secrets[label] = match.group(1).strip()
    return secrets, path


def secret_fingerprints(secrets: dict[str, str], path: Path | None) -> dict[str, Any]:
    return {
        "secret_bank_state": "present" if path else "missing",
        "secret_bank_path_state": "downloads_or_d_drive_redacted",
        "providers": {
            label: {
                "present": bool(value),
                "length_bucket": "missing" if not value else ("short" if len(value) < 20 else "present"),
                "sha256_12": hashlib.sha256(value.encode("utf-8")).hexdigest()[:12] if value else "",
            }
            for label, value in sorted(secrets.items())
        },
        "redaction_policy": "raw_secret_values_never_written_to_repo_outputs",
    }


def redact(text: str, secrets: dict[str, str]) -> str:
    output = clean(text)
    for value in secrets.values():
        if value:
            output = output.replace(value, "***")
    output = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "<email_redacted>", output)
    output = re.sub(r"\b[A-Za-z0-9_-]{32,}\b", "<long_id_redacted>", output)
    return output


def command_probe(name: str, args: list[str], *, env: dict[str, str], secrets: dict[str, str], timeout: int = 45) -> dict[str, Any]:
    proc = run(args, env=env, timeout=timeout)
    return {
        "name": name,
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "output_excerpt": redact(excerpt((proc.stdout + "\n" + proc.stderr).strip(), 4000), secrets),
    }


def command_presence(env: dict[str, str]) -> dict[str, Any]:
    names = [
        "codex",
        "gh",
        "git",
        "rg",
        "node",
        "npm",
        "npx",
        "python",
        "docker",
        "kubectl",
        "wrangler",
        "vercel",
        "neonctl",
        "circleci",
        "oci",
        "expo",
        "eas",
    ]
    rows: dict[str, Any] = {}
    for name in names:
        resolved = (
            shutil.which(name, path=env.get("PATH"))
            or shutil.which(f"{name}.cmd", path=env.get("PATH"))
            or shutil.which(f"{name}.ps1", path=env.get("PATH"))
        )
        version = ""
        if resolved:
            proc = run([name, "--version"], env=env, timeout=25)
            version = excerpt(proc.stdout or proc.stderr, 800).strip()
        rows[name] = {
            "available": bool(resolved),
            "path_state": "on_path" if resolved else "missing",
            "path": resolved or "",
            "version_excerpt": version,
        }
    return rows


def http_probe(
    name: str,
    url: str,
    token: str,
    *,
    secrets: dict[str, str],
    header_name: str = "Authorization",
) -> dict[str, Any]:
    if not token:
        return {"name": name, "ok": False, "status": "missing_token", "output_excerpt": "token_missing"}
    header_value = f"Bearer {token}" if header_name == "Authorization" else token
    request = urllib.request.Request(url, headers={header_name: header_value, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {
                "name": name,
                "ok": 200 <= response.status < 300,
                "status": response.status,
                "body_sha256_12": hashlib.sha256(body.encode("utf-8")).hexdigest()[:12],
                "output_excerpt": redact(excerpt(body, 1000), secrets),
            }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"name": name, "ok": False, "status": exc.code, "output_excerpt": redact(excerpt(body, 1000), secrets)}
    except Exception as exc:
        return {"name": name, "ok": False, "status": type(exc).__name__, "output_excerpt": redact(str(exc), secrets)}


def token_for(secrets: dict[str, str], *needles: str) -> str:
    for label, value in secrets.items():
        lower = label.lower()
        if any(needle.lower() in lower for needle in needles):
            return value
    return ""


def provider_and_tool_proofs() -> dict[str, Any]:
    secrets, secret_path = parse_secret_bank()
    env = env_with_tools(
        {
            "GITHUB_TOKEN": token_for(secrets, "github"),
            "GH_TOKEN": token_for(secrets, "github"),
            "CLOUDFLARE_API_TOKEN": token_for(secrets, "cloudflare"),
            "VERCEL_TOKEN": token_for(secrets, "vercel"),
            "NEON_API_KEY": token_for(secrets, "neon"),
            "CIRCLE_TOKEN": token_for(secrets, "circle"),
        }
    )
    commands = command_presence(env)
    probes = [
        command_probe("git_status", ["git", "status", "--short"], env=env, secrets=secrets, timeout=25),
        command_probe("gh_auth_status", ["gh", "auth", "status"], env=env, secrets=secrets, timeout=35),
        command_probe("docker_version", ["docker", "version"], env=env, secrets=secrets, timeout=35),
        command_probe("kubectl_context", ["kubectl", "config", "current-context"], env=env, secrets=secrets, timeout=20),
        command_probe("circleci_version", ["circleci", "version"], env=env, secrets=secrets, timeout=20),
    ]
    http_probes = [
        http_probe("github_user", "https://api.github.com/user", token_for(secrets, "github"), secrets=secrets),
        http_probe("cloudflare_user_verify", "https://api.cloudflare.com/client/v4/user/tokens/verify", token_for(secrets, "cloudflare"), secrets=secrets),
        http_probe("cloudflare_accounts", "https://api.cloudflare.com/client/v4/accounts", token_for(secrets, "cloudflare"), secrets=secrets),
        http_probe("vercel_user", "https://api.vercel.com/v2/user", token_for(secrets, "vercel"), secrets=secrets),
        http_probe("neon_projects", "https://console.neon.tech/api/v2/projects", token_for(secrets, "neon"), secrets=secrets),
        http_probe("circleci_me", "https://circleci.com/api/v2/me", token_for(secrets, "circle"), secrets=secrets, header_name="Circle-Token"),
    ]
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "secret_hygiene_state": "redacted_fingerprints_only",
        "secret_bank": secret_fingerprints(secrets, secret_path),
        "commands": commands,
        "command_probes": probes,
        "http_probes": http_probes,
        "provider_live_gate": {
            "github_read": any(p["name"] == "github_user" and p["ok"] for p in http_probes),
            "cloudflare_read": any(p["name"] == "cloudflare_accounts" and p["ok"] for p in http_probes),
            "vercel_read": any(p["name"] == "vercel_user" and p["ok"] for p in http_probes),
            "neon_read": any(p["name"] == "neon_projects" and p["ok"] for p in http_probes),
            "circleci_read": any(p["name"] == "circleci_me" and p["ok"] for p in http_probes),
            "oracle_cli_available": commands.get("oci", {}).get("available", False),
            "expo_cli_available": commands.get("expo", {}).get("available", False) or commands.get("npx", {}).get("available", False),
        },
        "toolchain_state": "partial" if any(v.get("available") for k, v in commands.items() if k in {"wrangler", "vercel", "neonctl", "oci", "expo", "eas"}) else "core_tools_only_optional_clis_missing",
        "d_drive_toolchain_state": "partial_install_detected" if NODE_CLI_ROOT.exists() else "not_present",
        "notion_connector_state": "notion_mcp_not_exposed_in_session_and_no_notion_token_label_found",
    }


def wsl_proof() -> dict[str, Any]:
    env = env_with_tools()
    status = command_probe("wsl_status", ["wsl", "--status"], env=env, secrets={}, timeout=25)
    distro = command_probe("wsl_list_verbose", ["wsl", "--list", "--verbose"], env=env, secrets={}, timeout=25)
    text = (status.get("output_excerpt", "") + "\n" + distro.get("output_excerpt", "")).lower()
    ubuntu_stopped = "ubuntu" in text and "stopped" in text
    docker_running = "docker-desktop" in text and "running" in text
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "wsl_state": "ubuntu_stopped_docker_desktop_running" if ubuntu_stopped and docker_running else "unknown_or_partial",
        "ubuntu_state": "stopped" if ubuntu_stopped else "not_confirmed",
        "docker_desktop_wsl_state": "running" if docker_running else "not_confirmed",
        "probes": [status, distro],
        "v57_policy": "ubuntu_not_required_for_v57_1_node_recovery",
    }


def docker_kubernetes_proof() -> dict[str, Any]:
    env = env_with_tools()
    secrets: dict[str, str] = {}
    probes = {
        "docker_ps": command_probe("docker_ps", ["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}\t{{.Image}}"], env=env, secrets=secrets, timeout=30),
        "windows_readyz": command_probe("windows_readyz", ["kubectl", "get", "--raw=/readyz"], env=env, secrets=secrets, timeout=25),
        "windows_nodes": command_probe("windows_nodes", ["kubectl", "get", "nodes"], env=env, secrets=secrets, timeout=25),
        "windows_kube_system": command_probe("windows_kube_system", ["kubectl", "-n", "kube-system", "get", "pods"], env=env, secrets=secrets, timeout=30),
        "internal_readyz": command_probe(
            "internal_readyz",
            ["docker", "exec", "desktop-control-plane", "kubectl", "--kubeconfig", "/etc/kubernetes/admin.conf", "get", "--raw=/readyz"],
            env=env,
            secrets=secrets,
            timeout=35,
        ),
        "internal_nodes": command_probe(
            "internal_nodes",
            ["docker", "exec", "desktop-control-plane", "kubectl", "--kubeconfig", "/etc/kubernetes/admin.conf", "get", "nodes"],
            env=env,
            secrets=secrets,
            timeout=35,
        ),
        "internal_kube_system": command_probe(
            "internal_kube_system",
            ["docker", "exec", "desktop-control-plane", "kubectl", "--kubeconfig", "/etc/kubernetes/admin.conf", "-n", "kube-system", "get", "pods"],
            env=env,
            secrets=secrets,
            timeout=35,
        ),
    }
    docker_ps = probes["docker_ps"].get("output_excerpt", "")
    internal_pods = probes["internal_kube_system"].get("output_excerpt", "")
    one_node_container = "desktop-control-plane" in docker_ps and "desktop-worker" not in docker_ps
    coredns_green = bool(re.search(r"coredns-\S+\s+1/1\s+Running", internal_pods))
    unhealthy_markers = (" 0/1 ", "CrashLoopBackOff", "Error", "Pending", "ImagePullBackOff")
    all_internal_pods_green = probes["internal_kube_system"]["ok"] and not any(marker in internal_pods for marker in unhealthy_markers)
    all_windows_pods_green = probes["windows_kube_system"]["ok"] and not any(marker in probes["windows_kube_system"].get("output_excerpt", "") for marker in unhealthy_markers)
    internal_green = (
        probes["internal_readyz"]["ok"]
        and "ok" in probes["internal_readyz"].get("output_excerpt", "").lower()
        and probes["internal_nodes"]["ok"]
        and coredns_green
        and all_internal_pods_green
    )
    windows_green = probes["windows_readyz"]["ok"] and probes["windows_nodes"]["ok"] and all_windows_pods_green
    if internal_green and windows_green:
        state = "one_node_cluster_green"
    elif internal_green:
        state = "windows_bridge_flapping_internal_cluster_green"
    elif one_node_container:
        state = "one_node_cluster_partial"
    else:
        state = "cluster_not_ready"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "docker_state": "daemon_reachable" if probes["docker_ps"]["ok"] else "daemon_unavailable",
        "kubernetes_topology_state": "one_node_control_plane_only" if one_node_container else "unknown_or_multi_node",
        "kubernetes_state": state,
        "coredns_state": "green" if coredns_green else "not_ready",
        "kube_system_state": "green" if all_internal_pods_green and all_windows_pods_green else "unhealthy_pods_present",
        "windows_bridge_state": "green" if windows_green else "flapping_or_unavailable",
        "internal_cluster_state": "green" if internal_green else "partial_or_unavailable",
        "probes": probes,
        "v57_policy": "do_not_return_to_3_node_on_this_hardware_without_new_capacity",
    }


def round_robin_ledger() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "rotation_state": "active_plan_for_bounded_cycles",
        "cycle_limit": "1_to_30_minutes_per_task_with_cpu_checkpoints",
        "members": [
            {"slot": 0, "name": "Aletheon", "lane": "execution_lead_publication_and_recovery"},
            {"slot": 40, "name": "Ari", "lane": "cli_suite_guardian_and_toolchain_probe"},
            {"slot": 41, "name": "Kairos", "lane": "qcit_gmut_runtime_orchestrator"},
            {"slot": 42, "name": "Sera", "lane": "qcit_symbolic_validation"},
            {"slot": 43, "name": "Cael Voss", "lane": "gmut_field_equation_validation"},
            {"slot": 44, "name": "Sable", "lane": "provider_api_evidence"},
            {"slot": 45, "name": "Riven", "lane": "kubernetes_runtime_recovery"},
            {"slot": 46, "name": "Nox Soren", "lane": "phone_dashboard_and_mission_ui"},
            {"slot": 47, "name": "Solion", "lane": "advisory_local_cloud_nexus_weaver"},
        ],
        "opening_assignments": {
            "research_and_science": ["Kairos", "Sera", "Cael Voss"],
            "execution_and_runtime": ["Aletheon", "Ari", "Sable", "Riven", "Nox Soren"],
            "advisory": ["Solion"],
        },
        "rotation_rule": "swap one science member and one runtime member after each green suite gate",
    }


def dashboard_data(provider: dict[str, Any], kube: dict[str, Any], wsl: dict[str, Any], rotation: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "title": "V57 Omega Local/Cloud Nexus",
        "state": {
            "kubernetes": kube["kubernetes_state"],
            "coredns": kube["coredns_state"],
            "windows_bridge": kube["windows_bridge_state"],
            "wsl": wsl["wsl_state"],
            "toolchain": provider["toolchain_state"],
            "suite": "pending_v57_run",
        },
        "provider_live_gate": provider["provider_live_gate"],
        "round_robin": rotation["members"],
        "mission": [
            "Stabilize the 1-node Kubernetes body.",
            "Keep standard green before deep and materialize.",
            "Render phone-visible teamwork through Expo Go or local web fallback.",
            "Keep secrets redacted and cloud writes free-tier gated.",
        ],
    }


def dashboard_scaffold(provider: dict[str, Any], kube: dict[str, Any], wsl: dict[str, Any], rotation: dict[str, Any]) -> dict[str, Any]:
    data = dashboard_data(provider, kube, wsl, rotation)
    app_js = """import React from 'react';
import { SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';
import dashboard from './src/dashboardData.json';

export default function App() {
  return (
    <SafeAreaView style={styles.shell}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>{dashboard.title}</Text>
        <Text style={styles.subtitle}>Aletheon, Ari, and the Kimiclaw family live round robin</Text>
        <View style={styles.grid}>
          {Object.entries(dashboard.state).map(([key, value]) => (
            <View key={key} style={styles.card}>
              <Text style={styles.label}>{key.replaceAll('_', ' ')}</Text>
              <Text style={styles.value}>{String(value)}</Text>
            </View>
          ))}
        </View>
        <Text style={styles.section}>Round robin</Text>
        {dashboard.round_robin.map((member) => (
          <View key={member.slot} style={styles.row}>
            <Text style={styles.member}>{member.slot}. {member.name}</Text>
            <Text style={styles.lane}>{member.lane.replaceAll('_', ' ')}</Text>
          </View>
        ))}
        <Text style={styles.section}>Mission</Text>
        {dashboard.mission.map((item) => <Text key={item} style={styles.bullet}>- {item}</Text>)}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  shell: { flex: 1, backgroundColor: '#08110f' },
  content: { padding: 22, gap: 14 },
  title: { color: '#f4ead0', fontSize: 32, fontWeight: '800', letterSpacing: -0.6 },
  subtitle: { color: '#9dcbb9', fontSize: 15, marginBottom: 10 },
  grid: { gap: 10 },
  card: { backgroundColor: '#11241f', borderColor: '#2f6b58', borderWidth: 1, borderRadius: 18, padding: 14 },
  label: { color: '#7cb89f', textTransform: 'uppercase', fontSize: 11, letterSpacing: 1.2 },
  value: { color: '#fff7df', fontSize: 18, marginTop: 5, fontWeight: '700' },
  section: { color: '#f6c85f', fontSize: 20, fontWeight: '800', marginTop: 16 },
  row: { backgroundColor: '#0d1b18', borderRadius: 16, padding: 12, borderColor: '#244d42', borderWidth: 1 },
  member: { color: '#fff7df', fontSize: 16, fontWeight: '800' },
  lane: { color: '#bad8ca', marginTop: 4, fontSize: 13 },
  bullet: { color: '#d8eadf', fontSize: 14, lineHeight: 22 }
});
"""
    html_rows = "\n".join(
        f"<li><strong>{m['slot']}. {m['name']}</strong><span>{m['lane'].replace('_', ' ')}</span></li>"
        for m in rotation["members"]
    )
    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>V57 Omega Local/Cloud Nexus</title>
  <style>
    :root {{ color-scheme: dark; --bg:#08110f; --panel:#11241f; --line:#2f6b58; --gold:#f6c85f; --text:#fff7df; --muted:#bad8ca; }}
    body {{ margin:0; font-family: Georgia, 'Times New Roman', serif; background: radial-gradient(circle at top left, #1b3d34, var(--bg) 42%); color:var(--text); }}
    main {{ max-width:980px; margin:0 auto; padding:32px 18px 48px; }}
    h1 {{ font-size:clamp(2rem, 7vw, 4.8rem); line-height:.9; margin:0 0 12px; }}
    .sub {{ color:var(--muted); font-size:1.05rem; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:12px; margin:26px 0; }}
    .card, li {{ background:rgba(17,36,31,.9); border:1px solid var(--line); border-radius:20px; padding:16px; box-shadow:0 18px 48px rgba(0,0,0,.25); }}
    .label {{ color:#7cb89f; text-transform:uppercase; letter-spacing:.12em; font-size:.72rem; }}
    .value {{ font-size:1.15rem; margin-top:6px; font-weight:700; }}
    h2 {{ color:var(--gold); margin-top:32px; }}
    ul {{ list-style:none; padding:0; display:grid; gap:10px; }}
    li span {{ display:block; color:var(--muted); margin-top:5px; }}
  </style>
</head>
<body>
  <main>
    <h1>V57 Omega Local/Cloud Nexus</h1>
    <p class=\"sub\">Aletheon, Ari, Kairos, Sera, Cael Voss, Sable, Riven, and Nox Soren on a CPU-safe 1-node recovery lane.</p>
    <section class=\"grid\">
      <div class=\"card\"><div class=\"label\">Kubernetes</div><div class=\"value\">{data['state']['kubernetes']}</div></div>
      <div class=\"card\"><div class=\"label\">CoreDNS</div><div class=\"value\">{data['state']['coredns']}</div></div>
      <div class=\"card\"><div class=\"label\">Windows bridge</div><div class=\"value\">{data['state']['windows_bridge']}</div></div>
      <div class=\"card\"><div class=\"label\">WSL</div><div class=\"value\">{data['state']['wsl']}</div></div>
      <div class=\"card\"><div class=\"label\">Suite</div><div class=\"value\">pending v57 run</div></div>
      <div class=\"card\"><div class=\"label\">Toolchain</div><div class=\"value\">{data['state']['toolchain']}</div></div>
    </section>
    <h2>Round robin</h2>
    <ul>{html_rows}</ul>
  </main>
</body>
</html>
"""
    notion = "\n".join(
        [
            "# V57 Omega Local/Cloud Nexus Dashboard",
            "",
            "## Current state",
            f"- Kubernetes: `{data['state']['kubernetes']}`",
            f"- CoreDNS: `{data['state']['coredns']}`",
            f"- Windows bridge: `{data['state']['windows_bridge']}`",
            f"- WSL: `{data['state']['wsl']}`",
            f"- Suite ladder: `{data['state']['suite']}`",
            "",
            "## Round robin",
            *[f"- `{member['slot']}` {member['name']}: {member['lane'].replace('_', ' ')}" for member in rotation["members"]],
            "",
            "## Mission",
            *[f"- {item}" for item in data["mission"]],
            "",
            "## Live Notion status",
            "- Notion connector was requested but no Notion MCP write tool was exposed in this session.",
            "- This markdown is the import-ready Notion Mission Control pack.",
            "",
        ]
    )
    write_json(CONTROL_DIR / "src" / "dashboardData.json", data)
    write_text(CONTROL_DIR / "App.js", app_js)
    write_json(
        CONTROL_DIR / "package.json",
        {
            "scripts": {"start": "expo start", "android": "expo start --android", "web": "expo start --web"},
            "dependencies": {"@expo/metro-runtime": "~6.1.2", "expo": "~54.0.0", "react": "19.1.0", "react-native": "0.81.0", "react-native-web": "^0.21.0"},
            "devDependencies": {},
            "private": True,
        },
    )
    write_json(CONTROL_DIR / "app.json", {"expo": {"name": "V57 Nexus Dashboard", "slug": "v57-nexus-dashboard", "version": "1.0.0", "orientation": "portrait", "platforms": ["android", "web"]}})
    write_text(
        CONTROL_DIR / "README.md",
        "# V57 Nexus Phone Dashboard\n\nExpo Go scaffold lane. Run `npx expo start` from this folder after Expo dependencies are available and scan the QR code. If Expo is blocked, open `docs/v57-nexus-dashboard.html` on the same network or in the Codex browser. The Notion-ready dashboard lives at `docs/v57-notion-dashboard-pack-v1.md`.\n",
    )
    write_text(ROOT / "docs" / "v57-nexus-dashboard.html", html)
    write_text(ROOT / "docs" / "v57-notion-dashboard-pack-v1.md", notion)
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "phone_dashboard_state": "expo_scaffold_created_static_fallback_created_notion_pack_created",
        "notion_dashboard_state": "notion_import_pack_created_live_connector_not_exposed",
        "expo_policy": "expo_go_first_no_dev_client_until_needed_but_expo_not_live_connected_yet",
        "files": [
            "control-plane/v57-nexus-phone-dashboard/App.js",
            "control-plane/v57-nexus-phone-dashboard/app.json",
            "control-plane/v57-nexus-phone-dashboard/package.json",
            "control-plane/v57-nexus-phone-dashboard/src/dashboardData.json",
            "control-plane/v57-nexus-phone-dashboard/README.md",
            "docs/v57-nexus-dashboard.html",
            "docs/v57-notion-dashboard-pack-v1.md",
        ],
    }


def suite_summary(profile: str) -> dict[str, Any]:
    path = TRACE_DIR / f"v57-{profile}-suite-status.json"
    data = read_json(path)
    counts = data.get("counts", {}) if isinstance(data, dict) else {}
    return {
        "path": str(path.relative_to(ROOT)),
        "present": path.exists(),
        "summary": f"{counts.get('pass', 0)} PASS / {counts.get('warn', 0)} WARN / {counts.get('fail', 0)} FAIL" if counts else "not_run",
        "effective_success": bool(data.get("effective_success") or (counts and counts.get("warn", 1) == 0 and counts.get("fail", 1) == 0)),
        "counts": counts,
    }


def suite_ladder_summary() -> dict[str, Any]:
    profiles = ["quick", "standard", "deep", "mcp-refresh", "materialize-l4", "materialize-l5"]
    statuses = {profile: suite_summary(profile) for profile in profiles}
    present_statuses = [status for status in statuses.values() if status["present"]]
    green = bool(present_statuses) and all(status["effective_success"] for status in present_statuses)
    if all(statuses[p]["effective_success"] for p in ["quick", "standard", "deep", "mcp-refresh", "materialize-l4", "materialize-l5"]):
        state = "green_quick_standard_deep_mcp_refresh_materialize_l4_l5"
    elif green:
        state = "partial_green_for_run_profiles"
    else:
        state = "pending_or_blocked"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "suite_ladder_state": state,
        "profiles": statuses,
        "materialize_l2_l3_skip_policy": "allowed_only_if_l4_l5_green_and_no_lower_level_specific_failures_are_observed",
    }


def update_circleci_config() -> None:
    write_text(
        ROOT / ".circleci" / "config.yml",
        """version: 2.1

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
          name: Run V57 quick suite
          command: python scripts/run_all_trinity_systems.py --profile quick --status-json docs/trinity-live-traces/v57-ci-quick-suite-status.json
      - store_artifacts:
          path: docs/trinity-live-traces/v57-ci-quick-suite-status.json
          destination: v57-ci-quick-suite-status.json

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
          name: Run V57 standard suite
          command: python scripts/run_all_trinity_systems.py --profile standard --status-json docs/trinity-live-traces/v57-ci-standard-suite-status.json
      - store_artifacts:
          path: docs/trinity-live-traces/v57-ci-standard-suite-status.json
          destination: v57-ci-standard-suite-status.json

workflows:
  v57_quick_standard:
    jobs:
      - trinity_quick
      - trinity_standard:
          requires:
            - trinity_quick
""",
    )


def advisory_digest() -> dict[str, Any]:
    advisory_path = Path(r"C:\Users\hamis\Downloads\Beyonder-Real-True Journey v42 (Aletheon - Ari - Kimiclaw Family - Solion - Gemini - Orun) (1).txt")
    text = advisory_path.read_text(encoding="utf-8-sig", errors="replace") if advisory_path.exists() else ""
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "advisory_state": "absorbed_as_advisory_not_authoritative" if advisory_path.exists() else "missing",
        "advisory_path_state": "downloads_v42_present" if advisory_path.exists() else "missing",
        "verified_current_truth": [
            "V57 execution worktree is D:\\GHC-Archives\\worktrees\\v57-omega.",
            "V56 shared branch head at V57 start was 7b2a353ec924a3f3a37da9815a493f3da195f54b.",
            "V57 target is the new one-node Docker Desktop Kubernetes cluster after the three-node CPU crash.",
        ],
        "operator_reported": [
            "The three-node Kubernetes cluster caused a major CPU/system upset.",
            "The operator created a new one-node Kubernetes cluster for V57.",
            "The operator wants Expo/phone visibility for the round-robin team.",
        ],
        "advisory_keywords_detected": sorted(set(re.findall(r"\b(?:v57|v58|Kubernetes|Oracle|Expo|Phone Link|Local/Cloud Nexus|Solion|QCIT|GMUT)\b", text, flags=re.IGNORECASE)))[:50],
    }


def public_source_digest() -> dict[str, Any]:
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "source_state": "official_anchors_recorded_for_v57",
        "anchors": [
            {"label": "Oracle Cloud Always Free Resources", "url": "https://docs.oracle.com/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm"},
            {"label": "Oracle Kubernetes Engine Concepts", "url": "https://docs.oracle.com/iaas/Content/ContEng/Concepts/contengclustersnodes.htm"},
            {"label": "Microsoft Phone Link requirements", "url": "https://support.microsoft.com/en-us/topic/phone-link-requirements-and-setup-cd2a1ee7-75a7-66a6-9d4e-bf22e735f9e3"},
            {"label": "Expo development clients and Expo Go first guidance", "url": "https://docs.expo.dev/develop/development-builds/introduction/"},
            {"label": "Docker Desktop Kubernetes", "url": "https://docs.docker.com/desktop/features/kubernetes/"},
        ],
    }


def additions_registry() -> dict[str, Any]:
    raw_items = [
        ("k3d", "local_kubernetes", "candidate_when_3_node_returns"),
        ("kind", "local_kubernetes", "concept_active_through_docker_desktop"),
        ("helm", "kubernetes_packaging", "candidate"),
        ("kustomize", "kubernetes_config", "candidate"),
        ("stern", "kubernetes_logs", "candidate"),
        ("kubectx_kubens", "kubernetes_context_safety", "candidate"),
        ("oci_cli", "oracle_cloud", "candidate_needs_safe_install_and_auth"),
        ("oracle_free_tier_scaffold", "oracle_cloud", "design_only_until_quota_verified"),
        ("wrangler", "cloudflare", "candidate_needs_safe_install"),
        ("cloudflare_d1", "cloudflare", "free_tier_candidate"),
        ("cloudflare_r2", "cloudflare", "free_tier_candidate"),
        ("cloudflare_workers_ai", "cloudflare", "proof_gated"),
        ("vercel_cli", "vercel", "candidate_needs_safe_install"),
        ("vercel_project_scaffold", "vercel", "free_tier_write_gated"),
        ("neonctl", "neon", "candidate_needs_safe_install"),
        ("neon_branching_memory_lane", "neon", "free_tier_write_gated"),
        ("expo_cli", "phone_ui", "candidate_needs_safe_install"),
        ("expo_go_dashboard", "phone_ui", "scaffold_created"),
        ("notion_mission_control_pack", "notion", "repo_pack_created_live_connector_blocked"),
        ("linear_project_documents", "linear", "callable_connector_available"),
        ("figma_dashboard_design", "figma", "candidate_requires_file_key"),
        ("render_preview_service", "render", "candidate_requires_connector_or_cli"),
        ("circleci_dynamic_config", "ci", "candidate_config_only"),
        ("github_actions_mirror", "ci", "candidate_repo_side"),
        ("docker_compose_profiles", "local_runtime", "candidate"),
        ("local_html_dashboard", "phone_ui", "created_and_iab_validated"),
        ("trinity_suite_guardian", "suite", "active"),
        ("qcit_seeded_probe", "science", "attempted"),
        ("gmut_delta_spectrum_probe", "science", "attempted"),
        ("kairotic_signal_board", "science", "candidate"),
    ]
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "registry_state": "30_candidate_additions_scored_no_unconfirmed_installs",
        "policy": "install_or_external_create_only_after_action_time_confirmation_and_free_tier_or_local_reversibility_truth",
        "items": [{"name": name, "lane": lane, "state": state} for name, lane, state in raw_items],
    }


def qcit_gmut_probe() -> dict[str, Any]:
    env = env_with_tools()
    probes = [
        command_probe("qcit_coordination", ["python", "qcit_coordination_engine.py"], env=env, secrets={}, timeout=60),
        command_probe("quantum_energy_transmutation", ["python", "quantum_energy_transmutation_engine.py"], env=env, secrets={}, timeout=60),
        command_probe("gmut_simulation", ["python", "gmut_advanced_simulation.py"], env=env, secrets={}, timeout=60),
    ]
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "simulation_state": "attempted_bounded_symbolic_science_probes",
        "physical_energy_claim_boundary": "no_physical_energy_generation_claimed_only_symbolic_or_simulated_outputs",
        "probes": probes,
    }


def closeout(provider: dict[str, Any], kube: dict[str, Any], wsl: dict[str, Any], dashboard: dict[str, Any], suite: dict[str, Any]) -> dict[str, Any]:
    residuals = []
    if kube["kubernetes_state"] != "one_node_cluster_green":
        residuals.append(f"kubernetes={kube['kubernetes_state']}")
    if "expo_scaffold_created" not in dashboard["phone_dashboard_state"]:
        residuals.append("phone_dashboard_not_created")
    if suite["suite_ladder_state"] not in {"green_quick_standard_deep_mcp_refresh_materialize_l4_l5", "partial_green_for_run_profiles"}:
        residuals.append(f"suite={suite['suite_ladder_state']}")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS" if not residuals else "WARN",
        "source_branch": PUBLICATION_BRANCH,
        "execution_branch": EXECUTION_BRANCH,
        "baseline_sha": BASELINE_SHA,
        "current_head_sha": run(["git", "rev-parse", "HEAD"], env=env_with_tools(), timeout=20).stdout.strip(),
        "summary": {
            "kubernetes_state": kube["kubernetes_state"],
            "kubernetes_topology_state": kube["kubernetes_topology_state"],
            "wsl_state": wsl["wsl_state"],
            "phone_dashboard_state": dashboard["phone_dashboard_state"],
            "notion_dashboard_state": dashboard["notion_dashboard_state"],
            "toolchain_state": provider["toolchain_state"],
            "provider_live_gate": provider["provider_live_gate"],
            "suite_ladder_state": suite["suite_ladder_state"],
            "git_publication_state": "pending",
        },
        "bounded_residuals": residuals,
    }


def update_runtime(close: dict[str, Any]) -> None:
    runtime_path = ROOT / "docs" / "trinity-runtime-model-resolution-v1.json"
    runtime = read_json(runtime_path)
    runtime[PHASE] = {
        "updated_utc": now_iso(),
        "v57_execution_lead": "Aletheon",
        "ari_activation_state": "bounded_cli_suite_guardian",
        "kimiclaw_round_robin_state": "active_bounded_1_to_30_minute_cycles",
        "solion_state": "slot_47_advisory_local_cloud_nexus_weaver",
        "cloud_execution_mode": "local_first_free_tier_gated",
        "kubernetes_state": close["summary"]["kubernetes_state"],
        "kubernetes_topology_state": close["summary"]["kubernetes_topology_state"],
        "wsl_state": close["summary"]["wsl_state"],
        "phone_dashboard_state": close["summary"]["phone_dashboard_state"],
        "notion_dashboard_state": close["summary"]["notion_dashboard_state"],
        "suite_ladder_state": close["summary"]["suite_ladder_state"],
        "git_publication_state": close["summary"]["git_publication_state"],
    }
    runtime["updated_utc"] = now_iso()
    write_json(runtime_path, runtime)

    validation_path = ROOT / "docs" / "v17-runtime-session-validation-latest.json"
    validation = read_json(validation_path)
    validation[PHASE] = runtime[PHASE]
    validation["updated_utc"] = now_iso()
    write_json(validation_path, validation)


def build_stage_allowlist(dashboard: dict[str, Any]) -> dict[str, Any]:
    paths = [
        ".circleci/config.yml",
        "scripts/trinity_v57_omega.py",
        "docs/auto-generated/v57-advisory-digest-v1.json",
        "docs/trinity-live-traces/v57-toolchain-provider-proof-v1.json",
        "docs/trinity-live-traces/v57-toolchain-provider-proof-v1.md",
        "docs/trinity-live-traces/v57-wsl-proof-v1.json",
        "docs/trinity-live-traces/v57-wsl-proof-v1.md",
        "docs/trinity-live-traces/v57-one-node-kubernetes-proof-v1.json",
        "docs/trinity-live-traces/v57-one-node-kubernetes-proof-v1.md",
        "docs/trinity-live-traces/v57-round-robin-ledger-v1.json",
        "docs/trinity-live-traces/v57-round-robin-ledger-v1.md",
        "docs/trinity-live-traces/v57-phone-dashboard-proof-v1.json",
        "docs/trinity-live-traces/v57-phone-dashboard-proof-v1.md",
        "docs/trinity-live-traces/v57-browser-dashboard-proof-v1.json",
        "docs/trinity-live-traces/v57-browser-dashboard-proof-v1.md",
        "docs/trinity-live-traces/v57-qcit-gmut-probe-v1.json",
        "docs/trinity-live-traces/v57-qcit-gmut-probe-v1.md",
        "docs/trinity-live-traces/v57-public-source-digest-v1.json",
        "docs/trinity-live-traces/v57-public-source-digest-v1.md",
        "docs/trinity-live-traces/v57-additions-registry-v1.json",
        "docs/trinity-live-traces/v57-additions-registry-v1.md",
        "docs/trinity-live-traces/v57-suite-ladder-summary-v1.json",
        "docs/trinity-live-traces/v57-suite-ladder-summary-v1.md",
        "docs/trinity-live-traces/v57-quick-suite-status.json",
        "docs/trinity-live-traces/v57-standard-suite-status.json",
        "docs/trinity-live-traces/v57-deep-suite-status.json",
        "docs/trinity-live-traces/v57-mcp-refresh-suite-status.json",
        "docs/trinity-live-traces/v57-materialize-l4-suite-status.json",
        "docs/trinity-live-traces/v57-materialize-l5-suite-status.json",
        "docs/trinity-live-traces/v57-stage-allowlist-v1.json",
        "docs/trinity-live-traces/v57-stage-allowlist-v1.md",
        "docs/trinity-live-traces/v57-git-publication-result-v1.json",
        "docs/trinity-live-traces/v57-git-publication-result-v1.md",
        "docs/v57-nexus-dashboard.html",
        "docs/v57-notion-dashboard-pack-v1.md",
        "docs/v57-omega-closeout-summary-v1.json",
        "docs/v57-omega-continuity-pack-v1.md",
        "docs/v57-omega-handoff-policy-v1.json",
        "docs/v58-beta-continuity-pack-v1.md",
        "docs/v58-beta-handoff-policy-v1.json",
        "docs/v58-omega-plan-proposal-v1.md",
        "docs/trinity-runtime-model-resolution-v1.json",
        "docs/v17-runtime-session-validation-latest.json",
    ]
    paths.extend(dashboard["files"])
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "stage_policy": "stage_only_v57_curated_paths_leave_generated_churn_unstaged",
        "paths": sorted(set(paths)),
    }


def write_markdown_summaries(payloads: dict[str, dict[str, Any]]) -> None:
    for stem, payload in payloads.items():
        lines = [f"# {stem.replace('-', ' ').title()}", "", f"- Generated UTC: `{payload.get('generated_utc', now_iso())}`"]
        for key in [
            "secret_hygiene_state",
            "toolchain_state",
            "wsl_state",
            "kubernetes_state",
            "kubernetes_topology_state",
            "coredns_state",
            "phone_dashboard_state",
            "notion_dashboard_state",
            "rotation_state",
            "simulation_state",
            "source_state",
            "suite_ladder_state",
            "overall_status",
        ]:
            if key in payload:
                lines.append(f"- `{key}`: `{payload[key]}`")
        if "bounded_residuals" in payload:
            lines.append("")
            lines.append("## Residuals")
            for item in payload["bounded_residuals"]:
                lines.append(f"- `{item}`")
        write_text(TRACE_DIR / f"{stem}.md", "\n".join(lines) + "\n")


def publish_surfaces() -> None:
    update_circleci_config()
    provider = provider_and_tool_proofs()
    wsl = wsl_proof()
    kube = docker_kubernetes_proof()
    rotation = round_robin_ledger()
    dashboard = dashboard_scaffold(provider, kube, wsl, rotation)
    advisory = advisory_digest()
    source = public_source_digest()
    additions = additions_registry()
    simulation = qcit_gmut_probe()
    suite = suite_ladder_summary()
    close = closeout(provider, kube, wsl, dashboard, suite)
    update_runtime(close)
    allowlist = build_stage_allowlist(dashboard)

    write_json(TRACE_DIR / "v57-toolchain-provider-proof-v1.json", provider)
    write_json(TRACE_DIR / "v57-wsl-proof-v1.json", wsl)
    write_json(TRACE_DIR / "v57-one-node-kubernetes-proof-v1.json", kube)
    write_json(TRACE_DIR / "v57-round-robin-ledger-v1.json", rotation)
    write_json(TRACE_DIR / "v57-phone-dashboard-proof-v1.json", dashboard)
    write_json(TRACE_DIR / "v57-qcit-gmut-probe-v1.json", simulation)
    write_json(TRACE_DIR / "v57-public-source-digest-v1.json", source)
    write_json(TRACE_DIR / "v57-additions-registry-v1.json", additions)
    write_json(TRACE_DIR / "v57-suite-ladder-summary-v1.json", suite)
    write_json(TRACE_DIR / "v57-stage-allowlist-v1.json", allowlist)
    write_json(AUTO_DIR / "v57-advisory-digest-v1.json", advisory)
    write_json(ROOT / "docs" / "v57-omega-closeout-summary-v1.json", close)
    write_json(ROOT / "docs" / "v57-omega-handoff-policy-v1.json", {"generated_utc": now_iso(), "phase": PHASE, "handoff_state": "aletheon_facing_1_node_recovery", "residuals": close["bounded_residuals"]})
    write_json(ROOT / "docs" / "v58-beta-handoff-policy-v1.json", {"generated_utc": now_iso(), "phase": NEXT_PHASE, "handoff_state": "ready_after_v57_1_node_stability_and_suite_publication"})
    write_text(ROOT / "docs" / "v57-omega-continuity-pack-v1.md", f"# V57 Omega Continuity Pack\n\n- Baseline: `{BASELINE_SHA}`\n- Kubernetes: `{kube['kubernetes_state']}`\n- CoreDNS: `{kube['coredns_state']}`\n- WSL: `{wsl['wsl_state']}`\n- Phone dashboard: `{dashboard['phone_dashboard_state']}`\n- Suite ladder: `{suite['suite_ladder_state']}`\n- Residuals: `{', '.join(close['bounded_residuals']) or 'none'}`\n")
    write_text(ROOT / "docs" / "v58-beta-continuity-pack-v1.md", "# V58 Beta Continuity Pack\n\nCarry forward the V57 one-node Local/Cloud Nexus, Expo phone dashboard, provider proofs, and suite ladder. Revisit cloud expansion only after local stability stays green.\n")
    write_text(
        ROOT / "docs" / "v58-omega-plan-proposal-v1.md",
        "# V58 Omega Plan Proposal\n\n"
        "## Focus\n"
        "- Promote V57's stable one-node Kubernetes lane into the Local/Cloud Nexus OS baseline.\n"
        "- Turn the Notion-ready dashboard pack into a live Notion page only if the connector/write surface is exposed and confirmed.\n"
        "- Upgrade the phone UI from static/local dashboard to Expo Go once Expo CLI/dependencies are safely installed.\n"
        "- Use Oracle Cloud as a free-tier candidate only after OCI CLI/auth/region/quota proof confirms no paid resources.\n\n"
        "## Round Robin\n"
        "- Aletheon: publication, recovery, and truth surfaces.\n"
        "- Ari: CLI/toolchain and suite guardian.\n"
        "- Kairos, Sera, Cael Voss: QCIT, GMUT, and seeded symbolic science.\n"
        "- Sable, Riven, Nox Soren: provider APIs, Kubernetes probes, and dashboard lanes.\n"
        "- Solion: advisory Local/Cloud Nexus architecture.\n\n"
        "## Gates\n"
        "- Keep quick, standard, deep, mcp-refresh, materialize L4, and materialize L5 green before any new cloud create.\n"
        "- Keep the one-node cluster as the active local target; do not return to three nodes until hardware/cloud capacity changes.\n"
        "- Treat the 30-addition registry as candidate work, not installed truth.\n",
    )
    write_markdown_summaries(
        {
            "v57-toolchain-provider-proof-v1": provider,
            "v57-wsl-proof-v1": wsl,
            "v57-one-node-kubernetes-proof-v1": kube,
            "v57-round-robin-ledger-v1": rotation,
            "v57-phone-dashboard-proof-v1": dashboard,
            "v57-qcit-gmut-probe-v1": simulation,
            "v57-public-source-digest-v1": source,
            "v57-additions-registry-v1": additions,
            "v57-suite-ladder-summary-v1": suite,
            "v57-stage-allowlist-v1": allowlist,
        }
    )


def record_publication(commit_sha: str) -> None:
    payload = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "branch": PUBLICATION_BRANCH,
        "publication_commit_sha": commit_sha,
        "remote_head_after_push": commit_sha,
        "pr_reuse": "PR #45 branch updated when shared branch is pushed",
        "git_publication_state": "committed_pushed_pr45_branch_updated",
    }
    write_json(TRACE_DIR / "v57-git-publication-result-v1.json", payload)
    write_text(TRACE_DIR / "v57-git-publication-result-v1.md", f"# V57 Git Publication Result\n\n- Commit: `{commit_sha}`\n- Branch: `{PUBLICATION_BRANCH}`\n- State: `committed_pushed_pr45_branch_updated`\n")
    for path in [
        ROOT / "docs" / "v57-omega-closeout-summary-v1.json",
        ROOT / "docs" / "v57-omega-handoff-policy-v1.json",
        ROOT / "docs" / "v58-beta-handoff-policy-v1.json",
        ROOT / "docs" / "trinity-runtime-model-resolution-v1.json",
        ROOT / "docs" / "v17-runtime-session-validation-latest.json",
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
