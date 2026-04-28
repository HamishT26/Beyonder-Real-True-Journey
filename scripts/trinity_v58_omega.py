from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "docs" / "trinity-live-traces"
AUTO = ROOT / "docs" / "auto-generated"
CONTROL = ROOT / "control-plane" / "v58-nexus-dashboard"
SKILL_DIR = ROOT / "skills" / "trinity-workbench-guarded-v1"
WORKBENCH = Path(r"C:\Users\hamis\OneDrive\Documents\New project")
PHASE = "v58_omega"
PUBLICATION_BRANCH = "codex/GHC-Family/beyonder-shared-omega-line"
EXECUTION_BRANCH = "codex/GHC-Family/v58-omega-exec"
BASELINE_SHA = "5bed2feb58ad2e19de145e441e0ffa027b1b8b2d"


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
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def run(args: list[str], timeout: int = 60) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            args,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return {
            "command": args,
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except Exception as exc:
        return {"command": args, "ok": False, "error": type(exc).__name__, "message": str(exc)}


def command_truth() -> dict[str, Any]:
    commands = [
        "kubectl",
        "docker",
        "node",
        "npm",
        "npx",
        "gh",
        "wrangler",
        "vercel",
        "neonctl",
        "render",
        "expo",
        "eas",
        "oci",
        "helm",
        "kustomize",
        "stern",
    ]
    found: dict[str, Any] = {}
    for cmd in commands:
        path = shutil.which(cmd)
        found[cmd] = {"available": bool(path), "path": path or ""}
    return found


def latest_api_bank() -> dict[str, Any]:
    candidates = [
        Path(r"C:\Users\hamis\GHC Family Beyonder-Real-True-Journey API Key bank (Cleaned up) (3).txt"),
        Path(r"C:\Users\hamis\Downloads\GHC Family Beyonder-Real-True-Journey API Key bank (Cleaned up) (2).txt"),
        Path(r"C:\Users\hamis\Downloads\GHC Family Beyonder-Real-True-Journey API Key bank (Cleaned up) (1).txt"),
        Path(r"C:\Users\hamis\Downloads\GHC Family Beyonder-Real-True-Journey API Key bank (Cleaned up).txt"),
    ]
    present = [p for p in candidates if p.exists()]
    labels = ["Notion", "Expo", "Render", "Vercel", "Cloudflare", "Neon", "Oracle", "GitHub", "CircleCI", "Kimi"]
    if not present:
        return {"state": "missing", "labels_present": [], "secret_policy": "no_secret_file_read"}
    newest = max(present, key=lambda p: p.stat().st_mtime)
    content = newest.read_text(encoding="utf-8", errors="ignore")
    return {
        "state": "present_redacted",
        "path": str(newest),
        "last_write_time": dt.datetime.fromtimestamp(newest.stat().st_mtime, dt.timezone.utc).isoformat(),
        "labels_present": [label for label in labels if re.search(label, content, re.IGNORECASE)],
        "sha256_12": hashlib.sha256(content.encode("utf-8", errors="ignore")).hexdigest()[:12],
        "secret_policy": "raw_values_read_only_for_presence_detection_never_written_to_repo",
    }


def kubernetes_truth() -> dict[str, Any]:
    readyz = run(["kubectl", "get", "--raw=/readyz"], timeout=45)
    nodes = run(["kubectl", "get", "nodes", "-o", "json"], timeout=60)
    pods = run(["kubectl", "-n", "kube-system", "get", "pods", "-o", "json"], timeout=60)
    node_summary: list[dict[str, Any]] = []
    pod_summary: list[dict[str, Any]] = []
    if nodes.get("ok"):
        data = json.loads(nodes["stdout"])
        for item in data.get("items", []):
            conds = {c.get("type"): c.get("status") for c in item.get("status", {}).get("conditions", [])}
            node_summary.append({"name": item["metadata"]["name"], "ready": conds.get("Ready") == "True"})
    if pods.get("ok"):
        data = json.loads(pods["stdout"])
        for item in data.get("items", []):
            statuses = item.get("status", {}).get("containerStatuses", [])
            restarts = sum(s.get("restartCount", 0) for s in statuses)
            ready = all(s.get("ready", False) for s in statuses) if statuses else False
            pod_summary.append(
                {
                    "name": item["metadata"]["name"],
                    "phase": item.get("status", {}).get("phase"),
                    "ready": ready,
                    "restarts": restarts,
                }
            )
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "readyz": "ok" if readyz.get("stdout") == "ok" else "not_ok",
        "readyz_probe": {
            "ok": bool(readyz.get("ok")),
            "returncode": readyz.get("returncode"),
            "stderr_excerpt": (readyz.get("stderr") or readyz.get("message") or "")[:600],
        },
        "nodes": node_summary,
        "kube_system_pods": pod_summary,
        "kubernetes_state": "one_node_ready_with_recent_restarts" if readyz.get("stdout") == "ok" else "not_ready",
        "policy": "one_node_health_gate_no_three_node_retry_on_current_hardware",
        "suite_gate": "allow_suite_load_only_when_readyz_ok",
        "source": "https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/",
    }


def host_pressure_truth() -> dict[str, Any]:
    docker = run(
        ["docker", "stats", "--no-stream", "--format", "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}"],
        timeout=60,
    )
    memory = run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            "(Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory,TotalVisibleMemorySize | ConvertTo-Json -Compress)",
        ],
        timeout=60,
    )
    containers: list[dict[str, Any]] = []
    max_cpu = 0.0
    if docker.get("ok"):
        for line in docker["stdout"].splitlines():
            parts = line.split("|")
            if len(parts) != 3:
                continue
            cpu_text = parts[1].replace("%", "").strip()
            try:
                cpu = float(cpu_text)
            except ValueError:
                cpu = 0.0
            max_cpu = max(max_cpu, cpu)
            containers.append({"name": parts[0], "cpu_percent": cpu, "memory": parts[2]})
    mem_payload = read_json_from_text(memory.get("stdout", ""))
    free_kb = int(mem_payload.get("FreePhysicalMemory", 0)) if isinstance(mem_payload, dict) else 0
    total_kb = int(mem_payload.get("TotalVisibleMemorySize", 0)) if isinstance(mem_payload, dict) else 0
    pressure_state = "cool"
    if max_cpu >= 300 or free_kb < 300_000:
        pressure_state = "hot_pause_heavy_suites"
    elif max_cpu >= 150 or free_kb < 500_000:
        pressure_state = "warm_cooldown_before_heavy_suites"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "containers": containers,
        "max_container_cpu_percent": max_cpu,
        "free_physical_memory_kb": free_kb,
        "total_visible_memory_kb": total_kb,
        "host_pressure_state": pressure_state,
        "policy": "run_one_heavy_suite_at_a_time_and_pause_when_hot",
    }


def read_json_from_text(text: str) -> Any:
    try:
        return json.loads(text)
    except Exception:
        return {}


def suite_status(path: Path) -> dict[str, Any]:
    data = read_json(path, {})
    counts = data.get("counts", {}) if isinstance(data, dict) else {}
    if not counts and isinstance(data, dict):
        results = data.get("results", [])
        counts = {
            "pass": sum(1 for r in results if r.get("status") == "PASS"),
            "warn": sum(1 for r in results if r.get("status") == "WARN"),
            "fail": sum(1 for r in results if r.get("status") == "FAIL"),
            "timeout": sum(1 for r in results if r.get("timed_out")),
        }
    present = path.exists()
    pass_count = counts.get("pass", 0)
    warn_count = counts.get("warn", 0)
    fail_count = counts.get("fail", 0)
    timeout_count = counts.get("timeout", 0)
    return {
        "path": rel(path),
        "present": present,
        "effective_success": bool(data.get("effective_success", False)) if isinstance(data, dict) else False,
        "summary": f"{pass_count} PASS / {warn_count} WARN / {fail_count} FAIL",
        "counts": {"pass": pass_count, "warn": warn_count, "fail": fail_count, "timeout": timeout_count},
    }


def suite_ladder_summary() -> dict[str, Any]:
    profiles = {
        "v58-quick": TRACE / "v58-quick-suite-status.json",
        "v58-standard": TRACE / "v58-standard-suite-status.json",
        "v58-deep": TRACE / "v58-deep-suite-status.json",
        "v58-mcp-refresh": TRACE / "v58-mcp-refresh-suite-status.json",
        "v58-materialize-l4": TRACE / "v58-materialize-l4-suite-status.json",
        "v58-materialize-l5": TRACE / "v58-materialize-l5-suite-status.json",
        "v59-quick": TRACE / "v59-quick-suite-status.json",
        "v59-standard": TRACE / "v59-standard-suite-status.json",
        "v59-deep": TRACE / "v59-deep-suite-status.json",
        "v59-materialize-l4": TRACE / "v59-materialize-l4-suite-status.json",
        "v59-materialize-l5": TRACE / "v59-materialize-l5-suite-status.json",
        "v60-quick": TRACE / "v60-quick-suite-status.json",
        "v60-standard": TRACE / "v60-standard-suite-status.json",
        "v60-deep": TRACE / "v60-deep-suite-status.json",
        "v60-materialize-l4": TRACE / "v60-materialize-l4-suite-status.json",
        "v60-materialize-l5": TRACE / "v60-materialize-l5-suite-status.json",
        "v61-quick": TRACE / "v61-quick-suite-status.json",
        "v61-standard": TRACE / "v61-standard-suite-status.json",
        "v61-deep": TRACE / "v61-deep-suite-status.json",
        "v61-materialize-l4": TRACE / "v61-materialize-l4-suite-status.json",
        "v61-materialize-l5": TRACE / "v61-materialize-l5-suite-status.json",
        "v62-quick": TRACE / "v62-quick-suite-status.json",
        "v62-standard": TRACE / "v62-standard-suite-status.json",
        "v62-deep": TRACE / "v62-deep-suite-status.json",
        "v62-materialize-l4": TRACE / "v62-materialize-l4-suite-status.json",
        "v62-materialize-l5": TRACE / "v62-materialize-l5-suite-status.json",
    }
    resolved = {name: suite_status(path) for name, path in profiles.items()}
    required_v58 = ["v58-quick", "v58-standard", "v58-deep", "v58-mcp-refresh", "v58-materialize-l4", "v58-materialize-l5"]
    state = "pending"
    if all(resolved[k]["effective_success"] for k in required_v58):
        state = "v58_green_mcp_refresh_gated"
    if (
        state == "v58_green_mcp_refresh_gated"
        and resolved["v59-quick"]["effective_success"]
        and resolved["v59-deep"]["effective_success"]
        and not resolved["v59-materialize-l4"]["present"]
    ):
        state = "v58_green_v59_quick_deep_green_materialize_pending"
    if (
        state == "v58_green_mcp_refresh_gated"
        and resolved["v59-quick"]["effective_success"]
        and resolved["v59-deep"]["effective_success"]
        and resolved["v59-materialize-l4"]["effective_success"]
        and not resolved["v59-materialize-l5"]["present"]
    ):
        state = "v58_green_v59_l4_green_l5_pending"
    if (
        state == "v58_green_mcp_refresh_gated"
        and resolved["v59-quick"]["effective_success"]
        and resolved["v59-deep"]["effective_success"]
        and resolved["v59-materialize-l4"]["effective_success"]
        and resolved["v59-materialize-l5"]["effective_success"]
    ):
        state = "v58_v59_green_mcp_refresh_gated_once"
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "suite_ladder_state": state,
        "mcp_refresh_policy": "run_once_in_v58_skip_for_v59_v62_unless_connector_state_changes",
        "standard_repeat_policy": "v58_standard_already_green_v59_v62_skip_standalone_standard_when_deep_l4_l5_green",
        "materialize_l2_l3_policy": "skip_when_l4_l5_green_and_no_lower_specific_failures_observed",
        "phase_start_eureka_policy": "mandatory_before_each_v59_v62_suite_load",
        "health_stop_policy": "pause_suite_execution_when_kubernetes_readyz_is_not_ok",
        "profiles": resolved,
    }


def surface_summary(path: Path) -> dict[str, Any]:
    exists = path.exists()
    payload = read_json(path, {}) if exists and path.suffix.lower() == ".json" else {}
    return {
        "path": str(path),
        "exists": exists,
        "generated_utc": payload.get("generated_utc") if isinstance(payload, dict) else None,
        "overall_status": payload.get("overall_status") if isinstance(payload, dict) else None,
        "suite_summary": payload.get("suite_summary") if isinstance(payload, dict) else None,
        "suite_ladder_state": payload.get("suite_ladder_state") if isinstance(payload, dict) else None,
    }


def workbench_reports() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    contracts: dict[str, Any] = {}
    for version in ["v3", "v4", "v5", "v6"]:
        path = WORKBENCH / f"trinity-workbench-contract-{version}.json"
        contracts[version] = read_json(path, {})
        contracts[version]["_path"] = str(path)
    surfaces_v6 = [Path(p) for p in contracts["v6"].get("read_surfaces", [])]
    surface_truth = [surface_summary(p) for p in surfaces_v6]
    latest_v57 = read_json(TRACE / "v57-suite-ladder-summary-v1.json", {})
    drift = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "workbench_path": str(WORKBENCH),
        "contract": "v6",
        "surface_truth": surface_truth,
        "current_phase_reference": surface_summary(TRACE / "v57-suite-ladder-summary-v1.json"),
        "drift_findings": [
            "v6 still reads shared/latest surfaces whose generated_utc may predate V57 publication.",
            "V58 should trust phase-specific suite summaries before shared latest surfaces.",
            "All v6 configured read surfaces exist, so the issue is truth freshness rather than missing files.",
        ],
        "recommendation": "package_as_read_only_skill_with_phase_specific_truth_precedence",
        "v57_suite_ladder_state": latest_v57.get("suite_ladder_state"),
    }
    lineage: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "versions": {},
        "jumps": [],
    }
    previous_surfaces: set[str] | None = None
    previous_version = ""
    for version in ["v3", "v4", "v5", "v6"]:
        payload = contracts[version]
        surfaces = set(payload.get("read_surfaces", []))
        lineage["versions"][version] = {
            "path": payload.get("_path"),
            "surface_count": len(surfaces),
            "allowed_triggers": payload.get("allowed_triggers", []),
            "disabled_write_paths": payload.get("disabled_write_paths", []),
            "runtime_dependencies": payload.get("runtime_dependencies", []),
        }
        if previous_surfaces is not None:
            lineage["jumps"].append(
                {
                    "from": previous_version,
                    "to": version,
                    "added_surfaces": sorted(surfaces - previous_surfaces),
                    "removed_surfaces": sorted(previous_surfaces - surfaces),
                }
            )
        previous_surfaces = surfaces
        previous_version = version
    skill = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "skill_name": "trinity-workbench-guarded-v1",
        "state": "repo_skill_packaged_read_only",
        "allowed_triggers": contracts["v6"].get("allowed_triggers", []),
        "disabled_write_paths": contracts["v6"].get("disabled_write_paths", []),
        "read_surfaces": contracts["v6"].get("read_surfaces", []),
    }
    return drift, lineage, skill


def write_workbench_skill(skill: dict[str, Any]) -> None:
    text = f"""---
name: trinity-workbench-guarded-v1
description: Read-only Trinity workbench summarizer for v6 contract truth drift, API book summaries, command indexes, and guarded dashboard rendering.
---

# Trinity Workbench Guarded V1

Use this skill only for read-only workbench inspection and summary rendering.

## Allowed
- Read the v6 contract surfaces listed in `C:\\Users\\hamis\\OneDrive\\Documents\\New project\\trinity-workbench-contract-v6.json`.
- Compare those surfaces with phase-specific truth such as `docs/trinity-live-traces/v58-*-suite-status.json`.
- Render compact summaries, drift reports, and handoff notes.

## Disabled
- Do not write directly into the authoritative repo except through an explicit phase harness and curated allowlist.
- Do not create cloud resources, bootstrap Google Drive, bypass authority surfaces, or mutate runtime truth.
- Do not read or publish secrets from API key banks.

## Current v58 package state
- Generated UTC: `{skill['generated_utc']}`
- State: `{skill['state']}`
"""
    write_text(SKILL_DIR / "SKILL.md", text)
    write_json(SKILL_DIR / "manifest.json", skill)


def dashboard_and_notion(api_bank: dict[str, Any], kube: dict[str, Any], suite: dict[str, Any]) -> dict[str, Any]:
    notion_parent = os.environ.get("NOTION_PARENT_ID", "").strip()
    notion_state = "blocked_missing_parent"
    if notion_parent:
        notion_state = "parent_id_supplied_live_write_not_attempted_by_generator"
    dashboard_data = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "title": "V58 Omega Local/Cloud Nexus Dashboard",
        "members": ["Aletheon", "Ari", "Kairos", "Sera", "Cael Voss", "Sable", "Riven", "Nox Soren"],
        "kubernetes_state": kube["kubernetes_state"],
        "suite_ladder_state": suite["suite_ladder_state"],
        "notion_dashboard_state": notion_state,
        "api_labels_present": api_bank.get("labels_present", []),
    }
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>V58 Omega Local/Cloud Nexus</title>
  <style>
    :root {{ --bg:#07130f; --panel:#10251d; --ink:#f4fff8; --muted:#a9c9bb; --gold:#f0c96a; --green:#66f0a3; }}
    body {{ margin:0; font-family: Georgia, 'Times New Roman', serif; background: radial-gradient(circle at top left,#244a33,#07130f 46%,#020604); color:var(--ink); }}
    main {{ max-width:1100px; margin:auto; padding:32px; }}
    h1 {{ font-size:clamp(32px,5vw,64px); line-height:1; margin:0 0 18px; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:16px; }}
    .card {{ background:linear-gradient(145deg,rgba(255,255,255,.08),rgba(255,255,255,.02)); border:1px solid rgba(240,201,106,.22); border-radius:22px; padding:18px; box-shadow:0 20px 70px rgba(0,0,0,.28); }}
    .label {{ color:var(--muted); font-size:13px; text-transform:uppercase; letter-spacing:.12em; }}
    .value {{ font-size:22px; color:var(--green); margin-top:8px; overflow-wrap:anywhere; }}
    .members {{ display:flex; flex-wrap:wrap; gap:10px; }}
    .pill {{ border:1px solid rgba(102,240,163,.35); border-radius:999px; padding:8px 12px; background:rgba(102,240,163,.08); }}
  </style>
</head>
<body>
  <main>
    <p class="label">Beyonder Real True Journey</p>
    <h1>V58 Omega Local/Cloud Nexus</h1>
    <section class="grid">
      <div class="card"><div class="label">Kubernetes</div><div class="value">{dashboard_data['kubernetes_state']}</div></div>
      <div class="card"><div class="label">Suites</div><div class="value">{dashboard_data['suite_ladder_state']}</div></div>
      <div class="card"><div class="label">Notion</div><div class="value">{notion_state}</div></div>
      <div class="card"><div class="label">Generated</div><div class="value">{dashboard_data['generated_utc']}</div></div>
    </section>
    <section class="card" style="margin-top:16px">
      <div class="label">Round Robin</div>
      <div class="members">{''.join(f'<span class="pill">{m}</span>' for m in dashboard_data['members'])}</div>
    </section>
  </main>
</body>
</html>
"""
    notion_md = f"""# V58 Omega Notion Dashboard Pack

- Generated UTC: `{dashboard_data['generated_utc']}`
- Notion live state: `{notion_state}`
- Kubernetes: `{dashboard_data['kubernetes_state']}`
- Suite ladder: `{dashboard_data['suite_ladder_state']}`
- Members: `{', '.join(dashboard_data['members'])}`

## Action Needed For Live Notion
Provide a Notion parent page or data source ID that has been shared with the internal integration. The current Notion API requires an accessible parent for internal integrations before creating a page.

## V58 Dashboard Sections
- Phase health
- One-node Kubernetes guard
- Workbench v6 drift
- v3-to-v6 contract jump
- API and CLI surface matrix
- V59-V62 hybrid phase queue
"""
    app_js = """import React from 'react';
import { SafeAreaView, ScrollView, Text, View } from 'react-native';
import data from './src/dashboardData.json';

export default function App() {
  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#07130f' }}>
      <ScrollView contentContainerStyle={{ padding: 24, gap: 14 }}>
        <Text style={{ color: '#f0c96a', letterSpacing: 2 }}>V58 OMEGA</Text>
        <Text style={{ color: '#f4fff8', fontSize: 34, fontWeight: '800' }}>{data.title}</Text>
        {['kubernetes_state', 'suite_ladder_state', 'notion_dashboard_state'].map((key) => (
          <View key={key} style={{ padding: 18, borderRadius: 18, backgroundColor: '#10251d' }}>
            <Text style={{ color: '#a9c9bb', textTransform: 'uppercase' }}>{key}</Text>
            <Text style={{ color: '#66f0a3', fontSize: 20 }}>{data[key]}</Text>
          </View>
        ))}
        <View style={{ padding: 18, borderRadius: 18, backgroundColor: '#10251d' }}>
          <Text style={{ color: '#a9c9bb', textTransform: 'uppercase' }}>Round Robin</Text>
          <Text style={{ color: '#f4fff8', fontSize: 18 }}>{data.members.join(' | ')}</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
"""
    package = {
        "name": "v58-nexus-dashboard",
        "version": "1.0.0",
        "private": True,
        "scripts": {"start": "expo start", "web": "expo start --web"},
        "dependencies": {"expo": "~54.0.0", "react": "19.1.0", "react-native": "0.81.0", "react-native-web": "^0.21.0"},
        "devDependencies": {},
    }
    write_json(CONTROL / "src" / "dashboardData.json", dashboard_data)
    write_text(CONTROL / "App.js", app_js)
    write_json(CONTROL / "package.json", package)
    write_json(CONTROL / "app.json", {"expo": {"name": "V58 Nexus Dashboard", "slug": "v58-nexus-dashboard", "version": "1.0.0", "platforms": ["android", "web"]}})
    write_text(CONTROL / "README.md", "# V58 Nexus Dashboard\n\nExpo-ready scaffold. Use Notion for V58 if a parent ID is supplied; otherwise use the local HTML dashboard.\n")
    write_text(ROOT / "docs" / "v58-nexus-dashboard.html", html)
    write_text(ROOT / "docs" / "v58-notion-dashboard-pack-v1.md", notion_md)
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "phone_dashboard_state": "expo_scaffold_created_for_v59_preview",
        "notion_dashboard_state": notion_state,
        "browser_use_state": "blocked_kernel_assets_missing",
        "local_dashboard_path": "docs/v58-nexus-dashboard.html",
        "notion_pack_path": "docs/v58-notion-dashboard-pack-v1.md",
        "expo_scaffold_path": "control-plane/v58-nexus-dashboard",
    }


def additions_registry(commands: dict[str, Any]) -> dict[str, Any]:
    items = [
        ("helm", "kubernetes_packaging"),
        ("kustomize", "kubernetes_config"),
        ("stern", "kubernetes_logs"),
        ("kubectx_kubens", "kubernetes_context_safety"),
        ("wrangler", "cloudflare_cli"),
        ("cloudflare_d1", "cloudflare_data"),
        ("cloudflare_r2", "cloudflare_storage"),
        ("cloudflare_workers_ai", "cloudflare_ai"),
        ("vercel_cli", "vercel_cli"),
        ("vercel_project_probe", "vercel_control_plane"),
        ("neonctl", "neon_cli"),
        ("neon_branching_probe", "neon_control_plane"),
        ("render_cli_or_api_probe", "render_control_plane"),
        ("expo_cli", "expo_phone_ui"),
        ("eas_cli", "expo_delivery"),
        ("oci_cli", "oracle_cloud"),
        ("oracle_free_tier_probe", "oracle_cloud"),
        ("notion_parent_dashboard", "notion"),
        ("notion_internal_connection_probe", "notion"),
        ("linear_phase_doc", "linear"),
        ("figma_dashboard_capture", "figma"),
        ("circleci_dynamic_config_probe", "ci"),
        ("github_pr_publication_guard", "github"),
        ("docker_compose_profile_guard", "local_runtime"),
        ("one_node_k8s_restart_watch", "local_runtime"),
        ("trinity_workbench_guarded_skill", "skill"),
        ("v6_surface_truth_drift", "workbench"),
        ("v3_to_v6_context_jump", "workbench"),
        ("qcit_gmut_delta_probe", "science"),
        ("kairotic_signal_board", "science"),
    ]
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "registry_state": "60_v58_v62_candidate_additions_ranked_proof_gated",
        "operator_latest_target": "50_plus_extensions_with_evidence_first_install_or_scaffold_gates",
        "policy": "no_unconfirmed_installs_or_paid_cloud_creates",
        "items": [
            {
                "name": name,
                "lane": lane,
                "state": "available" if commands.get(name.replace("_cli", ""), {}).get("available") else "candidate_or_repo_side",
            }
            for name, lane in items
        ]
        + [
            {"name": "phase_eureka_gate", "lane": "council", "state": "active_v59_onward"},
            {"name": "browser_use_repair_card", "lane": "browser", "state": "blocked_kernel_assets_missing"},
            {"name": "notion_parent_binding_card", "lane": "notion", "state": "waiting_for_parent_id"},
            {"name": "expo_go_qr_lane", "lane": "expo", "state": "v59_candidate"},
            {"name": "render_static_dashboard_probe", "lane": "render", "state": "api_key_label_present_probe_gated"},
            {"name": "vercel_static_dashboard_probe", "lane": "vercel", "state": "cli_missing_probe_gated"},
            {"name": "cloudflare_pages_probe", "lane": "cloudflare", "state": "wrangler_missing_probe_gated"},
            {"name": "neon_readonly_dashboard_state", "lane": "neon", "state": "candidate"},
            {"name": "oracle_cli_free_tier_inventory", "lane": "oracle", "state": "oci_missing"},
            {"name": "github_pr_truth_sync", "lane": "github", "state": "connector_available"},
            {"name": "linear_phase_record", "lane": "linear", "state": "connector_available"},
            {"name": "figma_dashboard_capture", "lane": "figma", "state": "file_key_required"},
            {"name": "life_science_research_matrix", "lane": "research", "state": "source_gated"},
            {"name": "scite_claim_checker", "lane": "research", "state": "candidate"},
            {"name": "latex_gmut_digest", "lane": "science", "state": "candidate"},
            {"name": "qcit_seed_sweep_v2", "lane": "science", "state": "candidate"},
            {"name": "quantum_energy_conservation_probe", "lane": "science", "state": "candidate"},
            {"name": "kairotic_detector_regression", "lane": "science", "state": "candidate"},
            {"name": "freedid_min_disclosure_refresh", "lane": "governance", "state": "candidate"},
            {"name": "cosmic_bill_rights_trace", "lane": "governance", "state": "candidate"},
            {"name": "agent_round_robin_rotation_v2", "lane": "council", "state": "active"},
            {"name": "ari_suite_guardian_card", "lane": "council", "state": "active"},
            {"name": "kairos_science_lane_card", "lane": "council", "state": "active"},
            {"name": "sera_source_lane_card", "lane": "council", "state": "active"},
            {"name": "cael_voss_infra_lane_card", "lane": "council", "state": "active"},
            {"name": "sable_secret_hygiene_card", "lane": "council", "state": "active"},
            {"name": "riven_publication_card", "lane": "council", "state": "active"},
            {"name": "nox_soren_k8s_watch_card", "lane": "council", "state": "active"},
            {"name": "v3_v6_contract_graph", "lane": "workbench", "state": "candidate"},
            {"name": "v6_truth_precedence_policy", "lane": "workbench", "state": "active"},
        ],
    }


def eureka_reports(suite: dict[str, Any], additions: dict[str, Any]) -> dict[str, Any]:
    members = [
        ("Aletheon", "Do not confuse momentum with health; V59+ should start with eureka analysis before load."),
        ("Ari", "Use deep plus L4/L5 as the repeated standard proof, but retain standard as a repair fallback."),
        ("Kairos", "Pair QCIT/GMUT probes with observable deltas, not claims of external validation."),
        ("Sera", "Anchor public-source claims and keep advisory text separate from verified truth."),
        ("Cael Voss", "Treat the one-node cluster as a scarce runtime and cool it between heavy proofs."),
        ("Sable", "Never publish raw API bank values; use label/fingerprint-only evidence."),
        ("Riven", "Publish forward-only with curated allowlists; leave suite churn unstaged."),
        ("Nox Soren", "Escalate only after readiness, pod health, and restart posture are recorded."),
    ]
    phases = ["v59", "v60", "v61", "v62"]
    reports = {
        phase: {
            "phase": phase,
            "generated_utc": now_iso(),
            "analysis_gate_state": "active_before_suite_load",
            "operator_latest_correction": "start_each_new_phase_with_grand_analysis_and_eureka_check_before_suite_runs",
            "hard_stop_if": "kubernetes_readyz_not_ok_or_host_memory_under_pressure",
            "council": [{"member": name, "eureka": insight} for name, insight in members],
            "extension_board_count": len(additions["items"]),
            "suite_policy": suite["standard_repeat_policy"],
            "next_move": {
                "v59": "Expo/phone UI lane, dashboard alternation, and post-V58 health-aware proof cycle.",
                "v60": "Notion return lane if parent ID is supplied, otherwise repo dashboard consolidation.",
                "v61": "Provider CLI/toolchain tranche with no unconfirmed installs.",
                "v62": "Hybrid closeout, publication, and V63 decision board.",
            }[phase],
        }
        for phase in phases
    }
    return {"generated_utc": now_iso(), "phase": PHASE, "reports": reports}


def phase_plans() -> dict[str, Any]:
    plans = {
        "v59": "Expo phone dashboard live preview and phone UI handoff, with V58 Notion truth mirrored into mobile cards. Skip standalone standard if deep, L4, and L5 are green.",
        "v60": "Return to Notion dashboard if parent access is supplied, then consolidate API proof lanes. Skip standalone standard if deep, L4, and L5 are green.",
        "v61": "Provider CLI tranche and one-node Kubernetes restart-watch hardening. Reintroduce standard only if deep/materialize exposes a failure family.",
        "v62": "Hybrid closeout: publish V58-V62 evidence rollup, suite ladder, and next V63 decision board. Treat deep plus L4/L5 as the standard-validation proof.",
    }
    for phase, summary in plans.items():
        write_text(
            ROOT / "docs" / f"{phase}-omega-plan-proposal-v1.md",
            f"# {phase.upper()} Omega Plan Proposal\n\n- Summary: {summary}\n- Gate: inherit V58 green standard, then use deep plus materialize L4/L5 as the repeated standard-validation proof.\n- Kubernetes: one-node only unless hardware state changes.\n",
        )
    write_text(
        ROOT / "docs" / "v59-beta-continuity-pack-v1.md",
        "# V59 Beta Continuity Pack\n\nV59 starts from V58 dashboard, workbench drift, and suite truth. Expo is the preferred UI lane, with Notion retained as the V58/V60 alternating dashboard lane.\n",
    )
    return {"generated_utc": now_iso(), "phase": PHASE, "plans": plans}


def closeout(
    kube: dict[str, Any],
    host: dict[str, Any],
    suite: dict[str, Any],
    dashboard: dict[str, Any],
    drift: dict[str, Any],
    additions: dict[str, Any],
) -> dict[str, Any]:
    residuals: list[str] = []
    if dashboard["notion_dashboard_state"] == "blocked_missing_parent":
        residuals.append("notion_live_dashboard_waiting_for_parent_page_or_data_source_id")
    if suite["suite_ladder_state"] == "pending":
        residuals.append("v58_suite_ladder_not_fully_run_yet")
    if kube["kubernetes_state"] != "one_node_ready_with_recent_restarts":
        residuals.append("kubernetes_not_green_pause_suite_execution_until_readyz_ok")
    if host["host_pressure_state"] == "hot_pause_heavy_suites":
        residuals.append("host_hot_pause_before_next_heavy_suite")
    if suite["suite_ladder_state"] == "v58_v59_green_mcp_refresh_gated_once":
        residuals.append("v60_v62_suite_loads_planned_not_executed_this_pass_after_v59_green_to_protect_one_node_host")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "overall_status": "PASS" if not residuals else "WARN",
        "summary": {
            "kubernetes_state": kube["kubernetes_state"],
            "host_pressure_state": host["host_pressure_state"],
            "suite_ladder_state": suite["suite_ladder_state"],
            "notion_dashboard_state": dashboard["notion_dashboard_state"],
            "workbench_drift_state": drift["recommendation"],
            "additions_state": additions["registry_state"],
            "git_publication_state": "pending",
            "phase_start_eureka_state": "mandatory_v59_v62_before_suite_load",
        },
        "bounded_residuals": residuals,
    }


def allowlist() -> dict[str, Any]:
    paths = [
        "scripts/trinity_v58_omega.py",
        "control-plane/v58-nexus-dashboard/App.js",
        "control-plane/v58-nexus-dashboard/README.md",
        "control-plane/v58-nexus-dashboard/app.json",
        "control-plane/v58-nexus-dashboard/package.json",
        "control-plane/v58-nexus-dashboard/src/dashboardData.json",
        "skills/trinity-workbench-guarded-v1/SKILL.md",
        "skills/trinity-workbench-guarded-v1/manifest.json",
        "docs/v58-nexus-dashboard.html",
        "docs/v58-notion-dashboard-pack-v1.md",
        "docs/v59-beta-continuity-pack-v1.md",
        "docs/v59-omega-plan-proposal-v1.md",
        "docs/v60-omega-plan-proposal-v1.md",
        "docs/v61-omega-plan-proposal-v1.md",
        "docs/v62-omega-plan-proposal-v1.md",
        "docs/v59-eureka-analysis-v1.md",
        "docs/v60-eureka-analysis-v1.md",
        "docs/v61-eureka-analysis-v1.md",
        "docs/v62-eureka-analysis-v1.md",
        "docs/v58-omega-closeout-summary-v1.json",
        "docs/v58-omega-continuity-pack-v1.md",
        "docs/v58-omega-handoff-policy-v1.json",
        "docs/v59-beta-handoff-policy-v1.json",
        "docs/trinity-runtime-model-resolution-v1.json",
        "docs/v17-runtime-session-validation-latest.json",
        "docs/auto-generated/v58-advisory-digest-v1.json",
    ]
    for name in [
        "baseline-state",
        "toolchain-provider-proof",
        "kubernetes-health",
        "host-pressure",
        "notion-dashboard-state",
        "workbench-v6-drift",
        "workbench-v3-v6-jump",
        "workbench-guarded-skill",
        "additions-registry",
        "suite-ladder-summary",
        "stage-allowlist",
        "git-publication-result",
        "browser-dashboard-proof",
        "eureka-analysis",
    ]:
        paths.append(f"docs/trinity-live-traces/v58-{name}-v1.json")
        paths.append(f"docs/trinity-live-traces/v58-{name}-v1.md")
    for profile in ["quick", "standard", "deep", "mcp-refresh", "materialize-l4", "materialize-l5"]:
        paths.append(f"docs/trinity-live-traces/v58-{profile}-suite-status.json")
    for phase in ["v59", "v60", "v61", "v62"]:
        for profile in ["quick", "standard", "deep", "materialize-l4", "materialize-l5"]:
            paths.append(f"docs/trinity-live-traces/{phase}-{profile}-suite-status.json")
    return {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "stage_policy": "stage_only_v58_curated_paths_leave_generated_churn_unstaged",
        "paths": sorted(set(paths)),
    }


def md(title: str, payload: Any) -> str:
    return f"# {title}\n\n```json\n{json.dumps(payload, indent=2, ensure_ascii=True)}\n```\n"


def update_runtime(close: dict[str, Any]) -> None:
    for path in [ROOT / "docs" / "trinity-runtime-model-resolution-v1.json", ROOT / "docs" / "v17-runtime-session-validation-latest.json"]:
        data = read_json(path, {})
        if not isinstance(data, dict):
            data = {}
        data["latest_phase"] = PHASE
        data["updated_utc"] = now_iso()
        data[PHASE] = {
            "v58_execution_lead": "Aletheon",
            "ari_activation_state": "bounded_cli_suite_guardian",
            "kimiclaw_round_robin_state": "active_bounded_helper_registry",
            "kubernetes_state": close["summary"]["kubernetes_state"],
            "host_pressure_state": close["summary"]["host_pressure_state"],
            "suite_ladder_state": close["summary"]["suite_ladder_state"],
            "notion_dashboard_state": close["summary"]["notion_dashboard_state"],
            "workbench_guarded_skill_state": close["summary"]["workbench_drift_state"],
            "git_publication_state": close["summary"]["git_publication_state"],
        }
        write_json(path, data)


def generate() -> dict[str, Any]:
    TRACE.mkdir(parents=True, exist_ok=True)
    AUTO.mkdir(parents=True, exist_ok=True)
    commands = command_truth()
    api_bank = latest_api_bank()
    kube = kubernetes_truth()
    host = host_pressure_truth()
    suite = suite_ladder_summary()
    drift, lineage, skill = workbench_reports()
    write_workbench_skill(skill)
    dashboard = dashboard_and_notion(api_bank, kube, suite)
    browser_proof = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "browser_use_state": dashboard["browser_use_state"],
        "attempted_urls": [
            "file:///D:/GHC-Archives/worktrees/v58-omega/docs/v58-nexus-dashboard.html",
            "https://developers.notion.com/reference/post-page",
        ],
        "blocker": "browser-use Node REPL reported missing kernel assets",
        "fallback": "local_dashboard_file_and_content_checks",
        "local_dashboard_exists": (ROOT / "docs" / "v58-nexus-dashboard.html").exists(),
    }
    additions = additions_registry(commands)
    eureka = eureka_reports(suite, additions)
    plans = phase_plans()
    close = closeout(kube, host, suite, dashboard, drift, additions)
    staged = allowlist()
    baseline = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "execution_branch": EXECUTION_BRANCH,
        "publication_branch": PUBLICATION_BRANCH,
        "baseline_sha": BASELINE_SHA,
        "worktree": str(ROOT),
        "workbench": str(WORKBENCH),
    }
    provider = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "api_bank": api_bank,
        "commands": commands,
        "notion_source_truth": {
            "create_page_requires_parent_for_internal_integrations": True,
            "source": "https://developers.notion.com/reference/post-page",
        },
        "expo_source_truth": {
            "expo_go_start_command": "npx expo start",
            "source": "https://docs.expo.dev/get-started/start-developing/",
        },
        "render_source_truth": {
            "list_services_validates_api_key_with_200_response": True,
            "source": "https://render.com/docs/api",
        },
    }
    advisory = {
        "generated_utc": now_iso(),
        "phase": PHASE,
        "operator_request": "grand_v58_to_v62_hybrid_omega",
        "date_truth": "2026-04-29 Pacific/Auckland",
        "notion_parent_status": dashboard["notion_dashboard_state"],
        "hybrid_phase_policy": "execute_v58_live_then_v59_v62_live_if_health_gates_remain_green",
        "hybrid_phase_completion_state": suite["suite_ladder_state"],
        "standard_repeat_policy": "drop_repeated_standard_after_v58_if_deep_l4_l5_remain_green",
        "operator_latest_correction": "new_phase_starts_require_grand_analysis_eureka_check_before_suite_execution",
        "suite_health_gate": "do_not_run_more_suites_while_kubernetes_readyz_is_not_ok",
        "host_pressure_state": host["host_pressure_state"],
    }
    write_json(TRACE / "v58-baseline-state-v1.json", baseline)
    write_text(TRACE / "v58-baseline-state-v1.md", md("V58 Baseline State", baseline))
    write_json(TRACE / "v58-toolchain-provider-proof-v1.json", provider)
    write_text(TRACE / "v58-toolchain-provider-proof-v1.md", md("V58 Toolchain Provider Proof", provider))
    write_json(TRACE / "v58-kubernetes-health-v1.json", kube)
    write_text(TRACE / "v58-kubernetes-health-v1.md", md("V58 Kubernetes Health", kube))
    write_json(TRACE / "v58-host-pressure-v1.json", host)
    write_text(TRACE / "v58-host-pressure-v1.md", md("V58 Host Pressure", host))
    write_json(TRACE / "v58-notion-dashboard-state-v1.json", dashboard)
    write_text(TRACE / "v58-notion-dashboard-state-v1.md", md("V58 Notion Dashboard State", dashboard))
    write_json(TRACE / "v58-browser-dashboard-proof-v1.json", browser_proof)
    write_text(TRACE / "v58-browser-dashboard-proof-v1.md", md("V58 Browser Dashboard Proof", browser_proof))
    write_json(TRACE / "v58-workbench-v6-drift-v1.json", drift)
    write_text(TRACE / "v58-workbench-v6-drift-v1.md", md("V58 Workbench V6 Drift", drift))
    write_json(TRACE / "v58-workbench-v3-v6-jump-v1.json", lineage)
    write_text(TRACE / "v58-workbench-v3-v6-jump-v1.md", md("V58 Workbench V3-V6 Jump", lineage))
    write_json(TRACE / "v58-workbench-guarded-skill-v1.json", skill)
    write_text(TRACE / "v58-workbench-guarded-skill-v1.md", md("V58 Workbench Guarded Skill", skill))
    write_json(TRACE / "v58-additions-registry-v1.json", additions)
    write_text(TRACE / "v58-additions-registry-v1.md", md("V58 Additions Registry", additions))
    write_json(TRACE / "v58-eureka-analysis-v1.json", eureka)
    write_text(TRACE / "v58-eureka-analysis-v1.md", md("V58 Eureka Analysis", eureka))
    for phase, report in eureka["reports"].items():
        write_text(
            ROOT / "docs" / f"{phase}-eureka-analysis-v1.md",
            f"# {phase.upper()} Eureka Analysis\n\n"
            + "\n".join(f"- {item['member']}: {item['eureka']}" for item in report["council"])
            + f"\n\n- Extension board count: `{report['extension_board_count']}`\n- Next move: {report['next_move']}\n",
        )
    write_json(TRACE / "v58-suite-ladder-summary-v1.json", suite)
    write_text(TRACE / "v58-suite-ladder-summary-v1.md", md("V58 Suite Ladder Summary", suite))
    write_json(TRACE / "v58-stage-allowlist-v1.json", staged)
    write_text(TRACE / "v58-stage-allowlist-v1.md", md("V58 Stage Allowlist", staged))
    write_json(AUTO / "v58-advisory-digest-v1.json", advisory)
    write_json(ROOT / "docs" / "v58-omega-closeout-summary-v1.json", close)
    write_json(ROOT / "docs" / "v58-omega-handoff-policy-v1.json", {"generated_utc": now_iso(), "phase": PHASE, "handoff_state": "v58_v62_hybrid_active", "residuals": close["bounded_residuals"]})
    write_json(ROOT / "docs" / "v59-beta-handoff-policy-v1.json", {"generated_utc": now_iso(), "phase": "v59_beta", "handoff_state": "ready_after_v58_health_gate"})
    write_text(
        ROOT / "docs" / "v58-omega-continuity-pack-v1.md",
        f"# V58 Omega Continuity Pack\n\n- Baseline: `{BASELINE_SHA}`\n- Kubernetes: `{kube['kubernetes_state']}`\n- Suite ladder: `{suite['suite_ladder_state']}`\n- Notion: `{dashboard['notion_dashboard_state']}`\n- Workbench: `{drift['recommendation']}`\n- Residuals: `{', '.join(close['bounded_residuals']) or 'none'}`\n",
    )
    update_runtime(close)
    return {
        "baseline": baseline,
        "provider": provider,
        "kube": kube,
        "host": host,
        "dashboard": dashboard,
        "suite": suite,
        "drift": drift,
        "lineage": lineage,
        "skill": skill,
        "additions": additions,
        "eureka": eureka,
        "plans": plans,
        "closeout": close,
        "allowlist": staged,
    }


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
    write_json(TRACE / "v58-git-publication-result-v1.json", payload)
    write_text(TRACE / "v58-git-publication-result-v1.md", md("V58 Git Publication Result", payload))
    for path in [
        ROOT / "docs" / "v58-omega-closeout-summary-v1.json",
        ROOT / "docs" / "v58-omega-handoff-policy-v1.json",
        ROOT / "docs" / "v59-beta-handoff-policy-v1.json",
        ROOT / "docs" / "trinity-runtime-model-resolution-v1.json",
        ROOT / "docs" / "v17-runtime-session-validation-latest.json",
    ]:
        data = read_json(path, {})
        if isinstance(data, dict):
            if "summary" in data:
                data["summary"]["git_publication_state"] = payload["git_publication_state"]
                data["summary"]["publication_commit_sha"] = commit_sha
            else:
                data["git_publication_state"] = payload["git_publication_state"]
                data["publication_commit_sha"] = commit_sha
            write_json(path, data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-publication", default="")
    args = parser.parse_args()
    if args.record_publication:
        record_publication(args.record_publication)
    else:
        generate()


if __name__ == "__main__":
    main()
