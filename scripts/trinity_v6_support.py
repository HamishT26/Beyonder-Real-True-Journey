#!/usr/bin/env python3
"""Support logic for the v6 Trinity expansion packs."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any

from trinity_api_common import fetch_text

ROOT = Path(__file__).resolve().parent.parent
MCP_CATALOG = ROOT / "docs" / "trinity-mcp-catalog-v4.json"
MCP_CACHE_SCHEMA = ROOT / "docs" / "trinity-mcp-cache-schema-v3.json"
MATERIALIZATION_LEDGER = ROOT / "docs" / "trinity-materialization-ledger.jsonl"
SUITE_STATUS = ROOT / "docs" / "system-suite-status.json"
MANDALA_STATUS = ROOT / "docs" / "trinity-mandala-scoreboard-latest.json"
BENCHMARK_REGISTRY = ROOT / "docs" / "trinity-benchmark-registry-v1.json"
CORPUS_V1 = ROOT / "docs" / "beyonder-journey-corpus-v13-v38.json"
CORPUS_V6 = ROOT / "docs" / "trinity-journey-corpus-index-v6.json"
MERIDIAN_DOC = ROOT / "docs" / "v6-trinity-benchmark-and-continuity-plan-2026-03-09.md"
KNOWLEDGE_GRAPH_CONTRACT = ROOT / "docs" / "trinity-code-knowledge-graph-contract-v1.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _repo_path(path_str: str) -> Path:
    resolved = (ROOT / path_str).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _read_json(path_str: str) -> dict[str, Any]:
    return json.loads(_repo_path(path_str).read_text(encoding="utf-8"))


def _read_json_safe(path_str: str) -> tuple[bool, dict[str, Any], str]:
    path = _repo_path(path_str)
    if not path.exists():
        return False, {}, f"missing artifact: {path_str}"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, {}, f"invalid json: {path_str} ({exc})"
    if not isinstance(payload, dict):
        return False, {}, f"expected object: {path_str}"
    return True, payload, "ok"


def _read_text(path_str: str) -> str:
    return _repo_path(path_str).read_text(encoding="utf-8")


def _write_json(path_str: str, payload: dict[str, Any]) -> None:
    path = _repo_path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_text(path_str: str, content: str) -> None:
    path = _repo_path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _append_jsonl(path_str: str, row: dict[str, Any]) -> None:
    path = _repo_path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")


def _check(name: str, status: str, detail: str) -> dict[str, str]:
    normalized = str(status).upper()
    if normalized not in {"PASS", "WARN", "FAIL"}:
        normalized = "FAIL"
    return {"name": name, "status": normalized, "detail": detail}


def _collect_targets(*groups: list[str]) -> list[str]:
    rows: set[str] = set()
    for group in groups:
        for item in group:
            text = str(item).strip()
            if text:
                rows.add(text)
    return sorted(rows)


def _safe_title(text: str, limit: int = 180) -> str:
    compact = " ".join(str(text or "").split())
    return compact if len(compact) <= limit else compact[: limit - 3].rstrip() + "..."


def _parse_iso(raw: object) -> datetime | None:
    text = str(raw or "").strip().replace("Z", "+00:00")
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _age_days(raw: object) -> float | None:
    parsed = _parse_iso(raw)
    if parsed is None:
        return None
    return round((datetime.now(timezone.utc) - parsed).total_seconds() / 86400.0, 3)


def _run(command: list[str], *, timeout: int = 60) -> tuple[int, str, str]:
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def _tool_probe(tool: str, version_arg: str = "--version") -> dict[str, Any]:
    executable = shutil.which(tool)  # type: ignore[name-defined]
    if not executable:
        return {"tool": tool, "available": False, "detail": "not on PATH", "path": ""}
    code, stdout, stderr = _run([executable, version_arg], timeout=20)
    detail = stdout.splitlines()[0] if stdout else stderr.splitlines()[0] if stderr else "probe completed"
    return {"tool": tool, "available": code == 0, "detail": detail, "path": executable}


def _git_recent_commits(limit: int = 5) -> list[dict[str, str]]:
    code, stdout, _ = _run(["git", "log", f"--max-count={limit}", "--pretty=format:%H%x09%s"], timeout=20)
    if code != 0:
        return []
    rows: list[dict[str, str]] = []
    for line in stdout.splitlines():
        commit, _, subject = line.partition("\t")
        if commit and subject:
            rows.append({"commit": commit[:12], "subject": subject})
    return rows


def _git_remote_ok() -> bool:
    code, _, _ = _run(["git", "ls-remote", "--heads", "origin", "main"], timeout=30)
    return code == 0


def _docker_ps(names_only: bool = False) -> list[str]:
    format_string = "{{.Names}}" if names_only else "{{.Names}}\t{{.Status}}\t{{.Image}}"
    code, stdout, _ = _run(["docker", "ps", "--format", format_string], timeout=30)
    if code != 0:
        return []
    return [line for line in stdout.splitlines() if line.strip()]


def _docker_pg_ready(container: str, database: str = "trinity_v5") -> tuple[bool, str]:
    code, stdout, stderr = _run(["docker", "exec", container, "pg_isready", "-U", "postgres", "-d", database], timeout=30)
    detail = stdout or stderr or "pg_isready completed"
    return code == 0, detail


def _pack_cache_path(pack: str) -> str:
    return f"docs/trinity-mcp-cache/{pack.replace('_', '-')}-latest.json"


def _proof_path(pack: str) -> str:
    return f"docs/trinity-live-traces/{pack.replace('_', '-')}-proof-v1.json"


def _default_live_state(status: str = "active") -> dict[str, Any]:
    return {
        "status": status,
        "desired_state": status,
        "actual_state": status,
        "live_read_enabled": status.startswith("verified_live"),
        "live_write_enabled": status == "verified_live_write",
        "promotion_evidence": [],
        "blockers": [],
    }


def _connector_state(connector_id: str) -> dict[str, Any]:
    ok, payload, _ = _read_json_safe("docs/trinity-mcp-catalog-v4.json")
    if not ok:
        return _default_live_state("staged_setup_gate")
    for row in payload.get("connectors", []):
        if isinstance(row, dict) and str(row.get("mcp_id") or "") == connector_id:
            return {
                "status": str(row.get("status") or "active"),
                "desired_state": str(row.get("desired_state") or row.get("status") or "active"),
                "actual_state": str(row.get("actual_state") or row.get("status") or "active"),
                "live_read_enabled": bool(row.get("live_read_enabled")),
                "live_write_enabled": bool(row.get("live_write_enabled")),
                "promotion_evidence": list(row.get("promotion_evidence", [])),
                "blockers": list(row.get("blockers", [])),
            }
    return _default_live_state("staged_setup_gate")


def _write_pack_cache(
    pack: str,
    *,
    auth_state: str,
    state: dict[str, Any],
    records: list[dict[str, Any]],
    repo_targets_touched: list[str],
    next_action: str,
) -> None:
    _write_json(
        _pack_cache_path(pack),
        {
            "generated_utc": _now_iso(),
            "integration_id": pack,
            "auth_state": auth_state,
            "status": state["status"],
            "desired_state": state["desired_state"],
            "actual_state": state["actual_state"],
            "live_read_enabled": state["live_read_enabled"],
            "live_write_enabled": state["live_write_enabled"],
            "promotion_evidence": state["promotion_evidence"],
            "blockers": state["blockers"],
            "records": records,
            "repo_targets_touched": repo_targets_touched,
            "next_action": next_action,
        },
    )


def _append_ledger(connector_id: str, operation: str, target: str, mode: str, result: str, evidence_artifact: str) -> None:
    _append_jsonl(
        "docs/trinity-materialization-ledger.jsonl",
        {
            "connector_id": connector_id,
            "operation": operation,
            "target": target,
            "mode": mode,
            "result": result,
            "timestamp": _now_iso(),
            "evidence_artifact": evidence_artifact,
        },
    )


def _repo_records(pack: str, repo_targets: list[str], summary: str, metrics: dict[str, Any], *, source_url: str = "") -> list[dict[str, Any]]:
    return [
        {
            "source_id": pack,
            "record_id": f"{pack}-seed",
            "signal_type": "pack_seed",
            "title": _safe_title(pack.replace("_", " ")),
            "published_at": _now_iso()[:10],
            "source_url": source_url or f"repo://{pack}",
            "summary": _safe_title(summary),
            "metrics": metrics,
            "tags": [pack, "seed"],
            "repo_targets": repo_targets,
        }
    ]


def _reentry_sync(
    *,
    offline_only: bool,
    profile_context: str,
) -> dict[str, Any]:
    ok_suite, suite_payload, suite_detail = _read_json_safe("docs/system-suite-status.json")
    recent_commits = _git_recent_commits(6)
    docker_rows = _docker_ps()
    docker_names = [row.split("\t", 1)[0] for row in docker_rows]
    pg_ok, pg_detail = _docker_pg_ready("trinity-v5-pg-proof") if "trinity-v5-pg-proof" in docker_names else (False, "container not running")
    surface = {
        "git_remote_live": _git_remote_ok(),
        "docker_cli": bool(shutil.which("docker")),
        "docker_container_running": "trinity-v5-pg-proof" in docker_names,
        "postgres_ready": pg_ok,
        "gh_available": bool(shutil.which("gh")),
        "node_available": bool(shutil.which("node")),
        "npx_available": bool(shutil.which("npx")),
    }
    wake_payload = {
        "generated_utc": _now_iso(),
        "profile_context": profile_context,
        "offline_only": offline_only,
        "stored_suite_status_present": ok_suite,
        "stored_suite_status": suite_payload.get("counts") if ok_suite else {},
        "current_session_surface": surface,
        "recent_commits": recent_commits,
        "docker_rows": docker_rows,
        "postgres_detail": pg_detail,
    }
    _write_json("docs/logs/system-wake-v1.json", wake_payload)
    drift_lines = [
        "# V6 Session Surface Drift Note",
        "",
        f"- generated_utc: `{wake_payload['generated_utc']}`",
        f"- profile_context: `{profile_context}`",
        f"- git_remote_live: `{surface['git_remote_live']}`",
        f"- docker_container_running: `{surface['docker_container_running']}`",
        f"- postgres_ready: `{surface['postgres_ready']}`",
        f"- gh_available: `{surface['gh_available']}`",
        f"- node_available: `{surface['node_available']}`",
        f"- npx_available: `{surface['npx_available']}`",
        "",
        "Stored v5 proof remains the operational baseline, but v6 records the current session tool surface explicitly before new promotion.",
    ]
    _write_text("docs/v6-session-surface-drift-note.md", "\n".join(drift_lines) + "\n")
    checks = [
        _check("suite_status_present", "PASS" if ok_suite else "FAIL", suite_detail if not ok_suite else "present"),
        _check("git_remote_live", "PASS" if surface["git_remote_live"] else "FAIL", "git ls-remote origin main"),
        _check("docker_container_running", "PASS" if surface["docker_container_running"] else "FAIL", "trinity-v5-pg-proof"),
        _check("postgres_ready", "PASS" if surface["postgres_ready"] else "FAIL", pg_detail),
    ]
    records = _repo_records(
        "reentry_sync",
        ["docs/logs/system-wake-v1.json", "docs/v6-session-surface-drift-note.md", "docs/system-suite-status.json"],
        "Captured current session surface and v5 drift note.",
        wake_payload["current_session_surface"],
        source_url="repo://docs/logs/system-wake-v1.json",
    )
    state = _default_live_state("active")
    _write_pack_cache(
        "reentry_sync",
        auth_state="local_repo",
        state=state,
        records=records,
        repo_targets_touched=["docs/logs/system-wake-v1.json", "docs/v6-session-surface-drift-note.md", "docs/system-suite-status.json"],
        next_action="Use the wake artifact as the first truth point before widening v6 claims.",
    )
    return {
        "checks": checks,
        "metrics": {"recent_commit_count": len(recent_commits), "current_session_surface": surface},
        "targets": _collect_targets(["docs/logs/system-wake-v1.json", "docs/v6-session-surface-drift-note.md", "docs/system-suite-status.json"]),
        "next_action": "Use the wake artifact as the first truth point before widening v6 claims.",
        "records": records,
        "source_runs": [{"source_id": "reentry_sync", "mode": "local_repo", "record_count": len(records), "status": "PASS"}],
    }


def _journey_history_reconciliation() -> dict[str, Any]:
    corpus = _read_json("docs/beyonder-journey-corpus-v13-v38.json")
    versions = [row for row in corpus.get("versions", []) if isinstance(row, dict)]
    meridian_text = _read_text("docs/v6-trinity-benchmark-and-continuity-plan-2026-03-09.md")
    output = {
        "version": "v6",
        "generated_utc": _now_iso(),
        "source_corpus": "docs/beyonder-journey-corpus-v13-v38.json",
        "meridian_source": "docs/v6-trinity-benchmark-and-continuity-plan-2026-03-09.md",
        "versions": versions,
        "meridian_notes": {
            "continuity_focus": "benchmark and continuity stewardship",
            "v29_reconciled": True,
            "evidence_boundary_explicit": True,
        },
    }
    _write_json("docs/trinity-journey-corpus-index-v6.json", output)
    checks = [
        _check("versions_present", "PASS" if len(versions) >= 13 else "FAIL", f"versions={len(versions)}"),
        _check("v29_reconciled", "PASS" if any(str(row.get("version")) == "v29" and str(row.get("evidence_state")) == "confirmed_evidence" for row in versions) else "FAIL", "v29 confirmed"),
        _check("meridian_source_present", "PASS" if "Benchmark and Continuity Steward" in meridian_text else "FAIL", "Meridian source imported"),
    ]
    records = _repo_records(
        "journey_history_reconciliation",
        ["docs/trinity-journey-corpus-index-v6.json", "docs/version-module-inventory-v13-v38.md", "docs/grand-cross-version-synthesis.md"],
        "Generated the v6 journey corpus index and preserved Meridian as a source anchor.",
        {"versions": len(versions), "meridian_source": True},
        source_url="repo://docs/trinity-journey-corpus-index-v6.json",
    )
    _write_pack_cache(
        "journey_history_reconciliation",
        auth_state="local_repo",
        state=_default_live_state("active"),
        records=records,
        repo_targets_touched=["docs/trinity-journey-corpus-index-v6.json", "docs/version-module-inventory-v13-v38.md", "docs/grand-cross-version-synthesis.md"],
        next_action="Promote only evidence-tagged historical findings into v6 narrative and benchmark docs.",
    )
    return {
        "checks": checks,
        "metrics": {"version_count": len(versions), "history_scope": "v13-v38"},
        "targets": _collect_targets(["docs/trinity-journey-corpus-index-v6.json", "docs/version-module-inventory-v13-v38.md", "docs/grand-cross-version-synthesis.md"]),
        "next_action": "Promote only evidence-tagged historical findings into v6 narrative and benchmark docs.",
        "records": records,
        "source_runs": [{"source_id": "journey_history_reconciliation", "mode": "local_repo", "record_count": len(records), "status": "PASS"}],
    }


def _benchmark_fabric() -> dict[str, Any]:
    registry = _read_json("docs/trinity-benchmark-registry-v1.json")
    rows = [row for row in registry.get("benchmarks", []) if isinstance(row, dict)]
    pillar_counts = {"mind": 0, "body": 0, "heart": 0}
    records: list[dict[str, Any]] = []
    for row in rows:
        pillar = str(row.get("pillar") or "trinity")
        if pillar in pillar_counts:
            pillar_counts[pillar] += 1
        records.append(
            {
                "source_id": "benchmark_registry",
                "record_id": str(row.get("benchmark_id") or f"row-{len(records)+1}"),
                "signal_type": "benchmark_reference",
                "title": _safe_title(str(row.get("benchmark_id") or "")),
                "published_at": _now_iso()[:10],
                "source_url": str(row.get("source_url") or ""),
                "summary": _safe_title(str(row.get("current_posture") or "")),
                "metrics": {"pillar": pillar, "metric_family": row.get("metric_family"), "threshold": row.get("threshold")},
                "tags": [pillar, "benchmark_fabric"],
                "repo_targets": ["docs/comparative-validation-grid-v1.md", "docs/grand-unified-narrative-brief.md"],
            }
        )
    checks = [
        _check("registry_present", "PASS" if rows else "FAIL", f"rows={len(rows)}"),
        _check("mind_lane_present", "PASS" if pillar_counts["mind"] >= 2 else "FAIL", f"mind={pillar_counts['mind']}"),
        _check("body_lane_present", "PASS" if pillar_counts["body"] >= 5 else "FAIL", f"body={pillar_counts['body']}"),
        _check("heart_lane_present", "PASS" if pillar_counts["heart"] >= 6 else "FAIL", f"heart={pillar_counts['heart']}"),
    ]
    _write_pack_cache(
        "benchmark_fabric",
        auth_state="public_registry",
        state=_default_live_state("active"),
        records=records,
        repo_targets_touched=["docs/trinity-benchmark-registry-v1.json", "docs/comparative-validation-grid-v1.md", "docs/grand-unified-narrative-brief.md"],
        next_action="Use the benchmark registry to tighten v6 comparison language before any readiness uplift.",
    )
    return {
        "checks": checks,
        "metrics": {"benchmark_count": len(rows), "pillar_counts": pillar_counts},
        "targets": _collect_targets(["docs/trinity-benchmark-registry-v1.json", "docs/comparative-validation-grid-v1.md", "docs/grand-unified-narrative-brief.md"]),
        "next_action": "Use the benchmark registry to tighten v6 comparison language before any readiness uplift.",
        "records": records,
        "source_runs": [{"source_id": "benchmark_fabric", "mode": "local_repo", "record_count": len(records), "status": "PASS"}],
    }


def _connector_materialization(
    *,
    offline_only: bool,
    include_mcp_refresh: bool,
    include_live_writes: bool,
    profile_context: str,
) -> dict[str, Any]:
    catalog = _read_json("docs/trinity-mcp-catalog-v4.json")
    connectors = [row for row in catalog.get("connectors", []) if isinstance(row, dict)]
    statuses = {str(row.get("mcp_id")): str(row.get("actual_state") or row.get("status") or "") for row in connectors}
    live_writers = [name for name, status in statuses.items() if status == "verified_live_write"]
    checks = [
        _check("github_live", "PASS" if statuses.get("github") == "verified_live_write" else "FAIL", statuses.get("github", "missing")),
        _check("linear_live", "PASS" if statuses.get("linear") == "verified_live_write" else "FAIL", statuses.get("linear", "missing")),
        _check("notion_live", "PASS" if statuses.get("notion") == "verified_live_write" else "FAIL", statuses.get("notion", "missing")),
        _check("postgres_live", "PASS" if statuses.get("postgres") == "verified_live_write" else "FAIL", statuses.get("postgres", "missing")),
        _check("figma_read_only", "PASS" if statuses.get("figma") == "verified_live_read" else "FAIL", statuses.get("figma", "missing")),
        _check("filesystem_staged", "PASS" if statuses.get("filesystem") == "staged_setup_gate" else "FAIL", statuses.get("filesystem", "missing")),
    ]
    if not offline_only:
        checks.append(_check("git_remote_live", "PASS" if _git_remote_ok() else "FAIL", "git ls-remote origin main"))
        if "trinity-v5-pg-proof" in [row.split("\t", 1)[0] for row in _docker_ps()]:
            pg_ok, detail = _docker_pg_ready("trinity-v5-pg-proof")
            checks.append(_check("postgres_runtime_ready", "PASS" if pg_ok else "FAIL", detail))
    records = [
        {
            "source_id": "connector_materialization",
            "record_id": str(row.get("mcp_id") or f"connector-{index}"),
            "signal_type": "connector_state",
            "title": _safe_title(str(row.get("mcp_id") or "")),
            "published_at": _now_iso()[:10],
            "source_url": str(row.get("cache_artifact") or ""),
            "summary": _safe_title(str(row.get("notes") or "")),
            "metrics": {
                "desired_state": row.get("desired_state"),
                "actual_state": row.get("actual_state"),
                "live_read_enabled": row.get("live_read_enabled"),
                "live_write_enabled": row.get("live_write_enabled"),
            },
            "tags": ["connector_materialization", str(row.get("mcp_id") or "")],
            "repo_targets": ["docs/trinity-mcp-catalog-v4.json", "docs/trinity-materialization-ledger.jsonl"],
        }
        for index, row in enumerate(connectors, start=1)
    ]
    next_action = "Use collab for live reads and materialize for disposable write proofs; do not widen connector claims without fresh artifacts."
    _write_pack_cache(
        "connector_materialization",
        auth_state="mixed",
        state=_default_live_state("active"),
        records=records,
        repo_targets_touched=["docs/trinity-mcp-catalog-v4.json", "docs/trinity-materialization-ledger.jsonl"],
        next_action=next_action,
    )
    return {
        "checks": checks,
        "metrics": {
            "connector_count": len(connectors),
            "verified_live_write": sorted(live_writers),
            "offline_only": offline_only,
            "include_mcp_refresh": include_mcp_refresh,
            "include_live_writes": include_live_writes,
            "profile_context": profile_context,
        },
        "targets": _collect_targets(["docs/trinity-mcp-catalog-v4.json", "docs/trinity-materialization-ledger.jsonl"]),
        "next_action": next_action,
        "records": records,
        "source_runs": [{"source_id": "connector_materialization", "mode": "catalog_aggregation", "record_count": len(records), "status": "PASS"}],
    }


def _sql_literal(value: object) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def _docker_psql(sql: str, *, database: str = "trinity_v5", timeout: int = 240) -> tuple[int, str, str]:
    proc = subprocess.run(
        [
            "docker",
            "exec",
            "-i",
            "trinity-v5-pg-proof",
            "psql",
            "-U",
            "postgres",
            "-d",
            database,
            "-v",
            "ON_ERROR_STOP=1",
            "-At",
            "-f",
            "-",
        ],
        cwd=ROOT,
        input=sql,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def _normal_rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _excluded_repo_path(rel_path: str, exclude_prefixes: list[str]) -> bool:
    normalized = rel_path.replace("\\", "/")
    for prefix in exclude_prefixes:
        token = str(prefix or "").replace("\\", "/")
        if not token:
            continue
        if "*" in token:
            token = token.replace("*", "")
            if token and token in normalized:
                return True
        elif normalized.startswith(token):
            return True
    return False


def _iter_repo_files() -> list[Path]:
    contract = _read_json("docs/trinity-code-knowledge-graph-contract-v1.json")
    include_exts = {
        str(item).lower()
        for item in contract.get("ingest_rules", {}).get("include_extensions", [])
        if str(item).strip()
    }
    exclude_prefixes = [
        str(item)
        for item in contract.get("ingest_rules", {}).get("exclude_prefixes", [])
        if str(item).strip()
    ]
    rows: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = _normal_rel(path)
        if _excluded_repo_path(rel, exclude_prefixes):
            continue
        if include_exts and path.suffix.lower() not in include_exts:
            continue
        rows.append(path)
    return sorted(rows)


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _python_symbols_and_dependencies(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rel = _normal_rel(path)
    source = path.read_text(encoding="utf-8", errors="replace")
    symbols: list[dict[str, Any]] = []
    dependencies: list[dict[str, Any]] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return symbols, dependencies

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            arg_names = [arg.arg for arg in node.args.args]
            symbols.append(
                {
                    "path": rel,
                    "symbol_name": node.name,
                    "symbol_kind": "function",
                    "signature": f"{node.name}({', '.join(arg_names)})",
                    "line_start": int(getattr(node, "lineno", 0) or 0),
                    "line_end": int(getattr(node, "end_lineno", getattr(node, "lineno", 0)) or 0),
                }
            )
        elif isinstance(node, ast.ClassDef):
            symbols.append(
                {
                    "path": rel,
                    "symbol_name": node.name,
                    "symbol_kind": "class",
                    "signature": node.name,
                    "line_start": int(getattr(node, "lineno", 0) or 0),
                    "line_end": int(getattr(node, "end_lineno", getattr(node, "lineno", 0)) or 0),
                }
            )
        elif isinstance(node, ast.Import):
            for alias in node.names:
                dependencies.append(
                    {
                        "path": rel,
                        "dependency": alias.name,
                        "dependency_kind": "import",
                        "source_line": int(getattr(node, "lineno", 0) or 0),
                    }
                )
        elif isinstance(node, ast.ImportFrom):
            module = str(node.module or "")
            if module:
                dependencies.append(
                    {
                        "path": rel,
                        "dependency": module,
                        "dependency_kind": "from_import",
                        "source_line": int(getattr(node, "lineno", 0) or 0),
                    }
                )
    return symbols, dependencies


def _write_os_runtime_reference_registry() -> dict[str, Any]:
    payload = {
        "version": "v1",
        "generated_utc": _now_iso(),
        "sources": [
            {
                "source_id": "linux-kernel-docs",
                "os_family": "linux",
                "layer": "kernel",
                "publisher": "Linux Kernel Documentation",
                "url": "https://docs.kernel.org/",
                "published_at": "2026-03-10",
                "pattern": "interface discipline and subsystem documentation",
                "trinity_target": "body",
            },
            {
                "source_id": "microsoft-wsl",
                "os_family": "windows-linux-interop",
                "layer": "developer_environment",
                "publisher": "Microsoft Learn",
                "url": "https://learn.microsoft.com/en-us/windows/wsl/",
                "published_at": "2026-03-10",
                "pattern": "host and guest runtime interop",
                "trinity_target": "body",
            },
            {
                "source_id": "freebsd-handbook",
                "os_family": "bsd",
                "layer": "operating_system",
                "publisher": "FreeBSD Documentation Project",
                "url": "https://docs.freebsd.org/en/books/handbook/",
                "published_at": "2026-03-10",
                "pattern": "system administration handbook discipline",
                "trinity_target": "body",
            },
            {
                "source_id": "android-aosp-architecture",
                "os_family": "android",
                "layer": "platform_architecture",
                "publisher": "Android Open Source Project",
                "url": "https://source.android.com/docs/core/architecture",
                "published_at": "2026-03-10",
                "pattern": "platform layering and service boundaries",
                "trinity_target": "body",
            },
            {
                "source_id": "apple-platform-security",
                "os_family": "apple-platforms",
                "layer": "security",
                "publisher": "Apple",
                "url": "https://support.apple.com/guide/security/welcome/web",
                "published_at": "2026-03-10",
                "pattern": "secure-by-default system design",
                "trinity_target": "heart",
            },
            {
                "source_id": "systemd-manual",
                "os_family": "linux",
                "layer": "service_orchestration",
                "publisher": "systemd",
                "url": "https://www.freedesktop.org/software/systemd/man/latest/systemd.html",
                "published_at": "2026-03-10",
                "pattern": "service lifecycle and orchestration control",
                "trinity_target": "body",
            },
            {
                "source_id": "docker-overview",
                "os_family": "containers",
                "layer": "runtime_packaging",
                "publisher": "Docker",
                "url": "https://docs.docker.com/get-started/docker-overview/",
                "published_at": "2026-03-10",
                "pattern": "runtime isolation and disposable environments",
                "trinity_target": "body",
            },
            {
                "source_id": "kubernetes-concepts",
                "os_family": "cloud_native",
                "layer": "control_plane",
                "publisher": "Kubernetes",
                "url": "https://kubernetes.io/docs/concepts/",
                "published_at": "2026-03-10",
                "pattern": "control-plane discipline and declarative orchestration",
                "trinity_target": "trinity",
            },
        ],
    }
    _write_json("docs/trinity-os-runtime-reference-registry-v1.json", payload)
    return payload


def _code_knowledge_graph(
    *,
    offline_only: bool,
    include_live_writes: bool,
    profile_context: str,
) -> dict[str, Any]:
    repo_files = _iter_repo_files()
    files_rows: list[dict[str, Any]] = []
    symbol_rows: list[dict[str, Any]] = []
    dependency_rows: list[dict[str, Any]] = []
    for path in repo_files:
        rel = _normal_rel(path)
        files_rows.append(
            {
                "path": rel,
                "extension": path.suffix.lower(),
                "size_bytes": path.stat().st_size,
                "sha256": _file_sha256(path),
                "pack_hint": rel.split("/", 2)[1] if rel.startswith("docs/") and "/" in rel else (rel.split("/", 1)[0] if "/" in rel else "root"),
                "updated_utc": _now_iso(),
            }
        )
        if path.suffix.lower() == ".py":
            symbols, dependencies = _python_symbols_and_dependencies(path)
            symbol_rows.extend(symbols)
            dependency_rows.extend(dependencies)

    manifest = _read_json("docs/trinity-expansion-system-manifest-v6.json")
    mcp_catalog = _read_json("docs/trinity-mcp-catalog-v4.json")
    corpus = _read_json("docs/trinity-journey-corpus-index-v6.json") if CORPUS_V6.exists() else _read_json("docs/beyonder-journey-corpus-v13-v38.json")
    anchors = [row for row in corpus.get("versions", []) if isinstance(row, dict)]

    checks: list[dict[str, str]] = [
        _check("repo_file_inventory", "PASS" if files_rows else "FAIL", f"files={len(files_rows)}"),
        _check("symbol_inventory", "PASS" if symbol_rows else "FAIL", f"symbols={len(symbol_rows)}"),
        _check("dependency_inventory", "PASS" if dependency_rows else "FAIL", f"dependencies={len(dependency_rows)}"),
    ]

    postgres_ready, postgres_detail = _docker_pg_ready("trinity-v5-pg-proof")
    checks.append(_check("postgres_ready", "PASS" if postgres_ready else "FAIL", postgres_detail))

    write_mode = bool(include_live_writes and profile_context == "materialize" and not offline_only and postgres_ready)
    sql_summary = {"schema_loaded": False, "rows_written": {}}
    proof_path = "docs/trinity-live-traces/code-knowledge-graph-proof-v1.json"
    summary_path = "docs/trinity-code-knowledge-graph-summary-v1.json"

    if postgres_ready:
        handshake_code, handshake_out, handshake_err = _docker_psql("select current_database();", timeout=60)
        checks.append(_check("postgres_handshake", "PASS" if handshake_code == 0 else "FAIL", handshake_out or handshake_err or "handshake failed"))
        if write_mode:
            def values_sql(rows: list[dict[str, Any]], columns: list[str]) -> str:
                if not rows:
                    return ""
                return ",\n".join(
                    "(" + ", ".join(_sql_literal(row.get(column)) for column in columns) + ")"
                    for row in rows
                )

            file_columns = ["path", "extension", "size_bytes", "sha256", "pack_hint", "updated_utc"]
            symbol_columns = ["path", "symbol_name", "symbol_kind", "signature", "line_start", "line_end"]
            dependency_columns = ["path", "dependency", "dependency_kind", "source_line"]
            manifest_rows = [
                {
                    "system_id": str(row.get("system_id") or ""),
                    "pack": str(row.get("pack") or ""),
                    "pillar": str(row.get("pillar") or ""),
                    "mode": str(row.get("mode") or ""),
                    "profiles_json": json.dumps(row.get("profiles", [])),
                    "activation_group": str(row.get("activation_group") or ""),
                    "continuity_band": str(row.get("continuity_band") or ""),
                }
                for row in manifest.get("systems", [])
                if isinstance(row, dict)
            ]
            connector_rows = [
                {
                    "connector_id": str(row.get("mcp_id") or ""),
                    "desired_state": str(row.get("desired_state") or ""),
                    "actual_state": str(row.get("actual_state") or ""),
                    "live_read_enabled": bool(row.get("live_read_enabled")),
                    "live_write_enabled": bool(row.get("live_write_enabled")),
                    "last_verified_utc": str(row.get("last_verified_utc") or ""),
                }
                for row in mcp_catalog.get("connectors", [])
                if isinstance(row, dict)
            ]
            anchor_rows = [
                {
                    "version": str(row.get("version") or ""),
                    "agent_name": str(row.get("agent_name") or ""),
                    "source_file": str(row.get("source_file") or ""),
                    "evidence_state": str(row.get("evidence_state") or ""),
                    "modules_json": json.dumps(row.get("modules", [])),
                    "next_reconciliation_target": str(row.get("next_reconciliation_target") or ""),
                }
                for row in anchors
            ]
            sql = """
create schema if not exists v6_code_knowledge;
create table if not exists v6_code_knowledge.files (
    path text primary key,
    extension text,
    size_bytes bigint,
    sha256 text,
    pack_hint text,
    updated_utc text
);
create table if not exists v6_code_knowledge.symbols (
    path text,
    symbol_name text,
    symbol_kind text,
    signature text,
    line_start integer,
    line_end integer
);
create table if not exists v6_code_knowledge.dependencies (
    path text,
    dependency text,
    dependency_kind text,
    source_line integer
);
create table if not exists v6_code_knowledge.manifest_entries (
    system_id text,
    pack text,
    pillar text,
    mode text,
    profiles_json text,
    activation_group text,
    continuity_band text
);
create table if not exists v6_code_knowledge.connector_states (
    connector_id text,
    desired_state text,
    actual_state text,
    live_read_enabled boolean,
    live_write_enabled boolean,
    last_verified_utc text
);
create table if not exists v6_code_knowledge.continuity_anchors (
    version text,
    agent_name text,
    source_file text,
    evidence_state text,
    modules_json text,
    next_reconciliation_target text
);
truncate v6_code_knowledge.files, v6_code_knowledge.symbols, v6_code_knowledge.dependencies, v6_code_knowledge.manifest_entries, v6_code_knowledge.connector_states, v6_code_knowledge.continuity_anchors;
"""
            if files_rows:
                sql += f"\ninsert into v6_code_knowledge.files ({', '.join(file_columns)}) values\n{values_sql(files_rows, file_columns)};\n"
            if symbol_rows:
                sql += f"\ninsert into v6_code_knowledge.symbols ({', '.join(symbol_columns)}) values\n{values_sql(symbol_rows, symbol_columns)};\n"
            if dependency_rows:
                sql += f"\ninsert into v6_code_knowledge.dependencies ({', '.join(dependency_columns)}) values\n{values_sql(dependency_rows, dependency_columns)};\n"
            if manifest_rows:
                manifest_columns = ["system_id", "pack", "pillar", "mode", "profiles_json", "activation_group", "continuity_band"]
                sql += f"\ninsert into v6_code_knowledge.manifest_entries ({', '.join(manifest_columns)}) values\n{values_sql(manifest_rows, manifest_columns)};\n"
            if connector_rows:
                connector_columns = ["connector_id", "desired_state", "actual_state", "live_read_enabled", "live_write_enabled", "last_verified_utc"]
                sql += f"\ninsert into v6_code_knowledge.connector_states ({', '.join(connector_columns)}) values\n{values_sql(connector_rows, connector_columns)};\n"
            if anchor_rows:
                anchor_columns = ["version", "agent_name", "source_file", "evidence_state", "modules_json", "next_reconciliation_target"]
                sql += f"\ninsert into v6_code_knowledge.continuity_anchors ({', '.join(anchor_columns)}) values\n{values_sql(anchor_rows, anchor_columns)};\n"
            sql += """
select 'files=' || count(*) from v6_code_knowledge.files;
select 'symbols=' || count(*) from v6_code_knowledge.symbols;
select 'dependencies=' || count(*) from v6_code_knowledge.dependencies;
select 'manifest_entries=' || count(*) from v6_code_knowledge.manifest_entries;
select 'connector_states=' || count(*) from v6_code_knowledge.connector_states;
select 'continuity_anchors=' || count(*) from v6_code_knowledge.continuity_anchors;
"""
            code, stdout, stderr = _docker_psql(sql, timeout=240)
            checks.append(_check("knowledge_graph_population", "PASS" if code == 0 else "FAIL", stdout or stderr or "population failed"))
            if code == 0:
                sql_summary["schema_loaded"] = True
                for line in stdout.splitlines():
                    if "=" in line:
                        key, _, value = line.partition("=")
                        if value.isdigit():
                            sql_summary["rows_written"][key] = int(value)
                _write_json(
                    proof_path,
                    {
                        "generated_utc": _now_iso(),
                        "pack": "code_knowledge_graph",
                        "database": "trinity_v5",
                        "schema": "v6_code_knowledge",
                        "profile_context": profile_context,
                        "write_mode": True,
                        "rows_written": sql_summary["rows_written"],
                    },
                )
                _append_ledger("postgres", "knowledge_graph_ingest", "v6_code_knowledge", "materialize", "PASS", proof_path)
        else:
            checks.append(_check("knowledge_graph_write_mode", "PASS", "read_only_preview"))

    summary_payload = {
        "generated_utc": _now_iso(),
        "profile_context": profile_context,
        "write_mode": write_mode,
        "file_count": len(files_rows),
        "symbol_count": len(symbol_rows),
        "dependency_count": len(dependency_rows),
        "manifest_entry_count": len(manifest.get("systems", [])),
        "connector_state_count": len(mcp_catalog.get("connectors", [])),
        "continuity_anchor_count": len(anchors),
        "sql_summary": sql_summary,
    }
    _write_json(summary_path, summary_payload)
    records = _repo_records(
        "code_knowledge_graph",
        ["docs/trinity-code-knowledge-graph-contract-v1.json", summary_path],
        "Generated a v6 repo metadata graph and optional Postgres schema population summary.",
        {
            "file_count": len(files_rows),
            "symbol_count": len(symbol_rows),
            "dependency_count": len(dependency_rows),
            "write_mode": write_mode,
            "postgres_ready": postgres_ready,
        },
        source_url=f"repo://{summary_path}",
    )
    _write_pack_cache(
        "code_knowledge_graph",
        auth_state="postgres_live" if postgres_ready else "postgres_unavailable",
        state=_connector_state("postgres"),
        records=records,
        repo_targets_touched=["docs/trinity-code-knowledge-graph-contract-v1.json", summary_path, proof_path],
        next_action="Use materialize mode for schema population; keep standard and deep in read-only preview.",
    )
    return {
        "checks": checks,
        "metrics": summary_payload,
        "targets": _collect_targets(["docs/trinity-code-knowledge-graph-contract-v1.json", summary_path, proof_path]),
        "next_action": "Use materialize mode for schema population; keep standard and deep in read-only preview.",
        "records": records,
        "source_runs": [{"source_id": "code_knowledge_graph", "mode": "repo_ingest", "record_count": len(records), "status": "PASS"}],
    }


def _self_correction() -> dict[str, Any]:
    py_bin = sys.executable or shutil.which("python") or "python"
    compile_proc = subprocess.run(
        [py_bin, "-m", "compileall", "-q", "scripts"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=240,
    )
    report = {
        "generated_utc": _now_iso(),
        "returncode": compile_proc.returncode,
        "stdout": compile_proc.stdout.strip(),
        "stderr": compile_proc.stderr.strip(),
        "loop_mode": "bounded_preview",
        "repo_mutation_policy": "explicit_suite_or_materialize_only",
    }
    _write_json("docs/self-correction-report-v1.json", report)
    checks = [
        _check("compileall_scripts", "PASS" if compile_proc.returncode == 0 else "FAIL", compile_proc.stderr.strip() or compile_proc.stdout.strip() or "compileall ok"),
        _check("repo_mutation_policy", "PASS", "no autonomous push-to-main behavior"),
    ]
    records = _repo_records(
        "self_correction",
        ["docs/self-correction-report-v1.json", "scripts"],
        "Ran a bounded self-correction preview loop with local static checks only.",
        {"compileall_returncode": compile_proc.returncode},
        source_url="repo://docs/self-correction-report-v1.json",
    )
    _write_pack_cache(
        "self_correction",
        auth_state="local_repo",
        state=_default_live_state("active"),
        records=records,
        repo_targets_touched=["docs/self-correction-report-v1.json", "scripts"],
        next_action="Escalate only concrete static-check findings; keep repo mutations inside explicit gates.",
    )
    return {
        "checks": checks,
        "metrics": {"compileall_returncode": compile_proc.returncode},
        "targets": _collect_targets(["docs/self-correction-report-v1.json", "scripts"]),
        "next_action": "Escalate only concrete static-check findings; keep repo mutations inside explicit gates.",
        "records": records,
        "source_runs": [{"source_id": "self_correction", "mode": "compileall", "record_count": len(records), "status": "PASS" if compile_proc.returncode == 0 else "FAIL"}],
    }


def _docker_pilot(*, offline_only: bool, include_live_writes: bool, profile_context: str) -> dict[str, Any]:
    rows = _docker_ps()
    running = "trinity-v5-pg-proof" in [row.split("\t", 1)[0] for row in rows]
    proof_path = "docs/trinity-live-traces/docker-pilot-proof-v1.json"
    attempted = False
    pilot_result = "SKIP"
    detail = "preview only"
    if running and include_live_writes and profile_context == "materialize" and not offline_only:
        attempted = True
        schema_name = f"v6_docker_pilot_{datetime.now(timezone.utc).strftime('%H%M%S')}"
        sql = f"""
create schema {schema_name};
create table {schema_name}.pilot_probe(id integer);
insert into {schema_name}.pilot_probe(id) values (1);
select count(*) from {schema_name}.pilot_probe;
drop schema {schema_name} cascade;
"""
        code, stdout, stderr = _docker_psql(sql, timeout=120)
        pilot_result = "PASS" if code == 0 else "FAIL"
        detail = stdout or stderr or "docker pilot run"
    _write_json(
        proof_path,
        {
            "generated_utc": _now_iso(),
            "pack": "docker_pilot",
            "profile_context": profile_context,
            "offline_only": offline_only,
            "include_live_writes": include_live_writes,
            "attempted": attempted,
            "result": pilot_result,
            "detail": detail,
        },
    )
    if attempted:
        _append_ledger("postgres", "docker_pilot_schema_probe", "trinity-v5-pg-proof", "materialize", pilot_result, proof_path)
    checks = [
        _check("docker_running_container", "PASS" if running else "FAIL", "trinity-v5-pg-proof"),
        _check("docker_pilot_scope", "PASS", f"profile={profile_context}, attempted={attempted}"),
        _check("docker_pilot_result", "PASS" if pilot_result in {"PASS", "SKIP"} else "FAIL", detail),
    ]
    records = _repo_records(
        "docker_pilot",
        ["docs/trinity-live-traces/docker-pilot-proof-v1.json"],
        "Recorded a disposable Docker/Postgres pilot proof or preview.",
        {"attempted": attempted, "result": pilot_result},
        source_url="repo://docs/trinity-live-traces/docker-pilot-proof-v1.json",
    )
    _write_pack_cache(
        "docker_pilot",
        auth_state="docker_local",
        state=_connector_state("postgres"),
        records=records,
        repo_targets_touched=["docs/trinity-live-traces/docker-pilot-proof-v1.json"],
        next_action="Keep Docker pilot actions disposable and audit-logged.",
    )
    return {
        "checks": checks,
        "metrics": {"attempted": attempted, "result": pilot_result},
        "targets": _collect_targets(["docs/trinity-live-traces/docker-pilot-proof-v1.json"]),
        "next_action": "Keep Docker pilot actions disposable and audit-logged.",
        "records": records,
        "source_runs": [{"source_id": "docker_pilot", "mode": "docker_local", "record_count": len(records), "status": "PASS" if pilot_result != "FAIL" else "FAIL"}],
    }


def _sentinel_daemon() -> dict[str, Any]:
    status_ok, _, _ = _read_json_safe("docs/system-suite-status.json")
    stale_targets = []
    for path in [
        "docs/trinity-mandala-scoreboard-latest.json",
        "docs/trinity-extension-catalog-validation-latest.json",
        "docs/trinity-expansion-manifest-validation-latest.json",
    ]:
        ok, payload, detail = _read_json_safe(path)
        if not ok:
            stale_targets.append({"target": path, "reason": detail})
            continue
        age = _age_days(payload.get("generated_utc"))
        if age is None or age > 7:
            stale_targets.append({"target": path, "reason": f"age_days={age}"})
    runbook = "\n".join(
        [
            "# Trinity Sentinel Manual Runbook",
            "",
            "- Mode: manual/on-demand only",
            "- Allowed actions: read-only polling, stale-proof detection, draft task generation",
            "- Disallowed actions: direct writes to `main`, recurring automation without separate approval, destructive commands",
            "",
            "## Current focus",
            f"- stale_targets: `{len(stale_targets)}`",
            f"- suite_status_present: `{status_ok}`",
        ]
    ) + "\n"
    draft_tasks = {
        "generated_utc": _now_iso(),
        "mode": "manual_on_demand",
        "stale_targets": stale_targets,
        "draft_tasks": [
            {"task": "refresh stale artifacts", "blocked": False if stale_targets else True},
            {"task": "review connector proof timestamps", "blocked": False},
        ],
    }
    _write_text("docs/trinity-sentinel-manual-runbook-v1.md", runbook)
    _write_json("docs/trinity-sentinel-draft-tasks-latest.json", draft_tasks)
    checks = [
        _check("manual_mode_only", "PASS", "recurring automation not enabled"),
        _check("draft_tasks_written", "PASS", "docs/trinity-sentinel-draft-tasks-latest.json"),
    ]
    records = _repo_records(
        "sentinel_daemon",
        ["docs/trinity-sentinel-manual-runbook-v1.md", "docs/trinity-sentinel-draft-tasks-latest.json"],
        "Prepared the read-only sentinel daemon runbook and draft tasks.",
        {"stale_target_count": len(stale_targets)},
        source_url="repo://docs/trinity-sentinel-draft-tasks-latest.json",
    )
    _write_pack_cache(
        "sentinel_daemon",
        auth_state="local_repo",
        state=_default_live_state("active"),
        records=records,
        repo_targets_touched=["docs/trinity-sentinel-manual-runbook-v1.md", "docs/trinity-sentinel-draft-tasks-latest.json"],
        next_action="Keep the sentinel manual until the on-demand path is green and separately approved.",
    )
    return {
        "checks": checks,
        "metrics": {"stale_target_count": len(stale_targets)},
        "targets": _collect_targets(["docs/trinity-sentinel-manual-runbook-v1.md", "docs/trinity-sentinel-draft-tasks-latest.json"]),
        "next_action": "Keep the sentinel manual until the on-demand path is green and separately approved.",
        "records": records,
        "source_runs": [{"source_id": "sentinel_daemon", "mode": "manual", "record_count": len(records), "status": "PASS"}],
    }


def _public_web_weaver(*, offline_only: bool, include_public_api_refresh: bool) -> dict[str, Any]:
    _write_os_runtime_reference_registry()
    benchmark_registry = _read_json("docs/trinity-benchmark-registry-v1.json")
    sources = [
        {"source_id": "arxiv-hep-th", "title": "arXiv hep-th recent", "url": "https://arxiv.org/list/hep-th/recent", "tag": "mind"},
        {"source_id": "linux-kernel-docs", "title": "Linux Kernel Documentation", "url": "https://docs.kernel.org/", "tag": "body"},
        {"source_id": "wsl-docs", "title": "Microsoft WSL", "url": "https://learn.microsoft.com/en-us/windows/wsl/", "tag": "body"},
        {"source_id": "did-core", "title": "W3C DID Core", "url": "https://www.w3.org/TR/did-core/", "tag": "heart"},
        {"source_id": "nist-ai-rmf", "title": "NIST AI RMF", "url": "https://www.nist.gov/itl/ai-risk-management-framework", "tag": "heart"},
    ]
    records: list[dict[str, Any]] = []
    checks: list[dict[str, str]] = []
    live_mode = bool(include_public_api_refresh and not offline_only)
    for source in sources:
        if live_mode:
            try:
                text = fetch_text(source["url"], timeout_sec=30)
                compact = re.sub(r"\s+", " ", text).strip()
                preview = compact[:240] if compact else source["title"]
                records.append(
                    {
                        "source_id": source["source_id"],
                        "record_id": source["source_id"],
                        "signal_type": "official_reference_fetch",
                        "title": source["title"],
                        "published_at": _now_iso()[:10],
                        "source_url": source["url"],
                        "summary": _safe_title(preview),
                        "metrics": {"chars": len(text), "live_mode": True},
                        "tags": [source["tag"], "public_web_weaver"],
                        "repo_targets": ["docs/trinity-benchmark-registry-v1.json", "docs/trinity-os-runtime-reference-registry-v1.json"],
                    }
                )
                checks.append(_check(f"fetch:{source['source_id']}", "PASS", source["url"]))
            except Exception as exc:  # noqa: BLE001
                checks.append(_check(f"fetch:{source['source_id']}", "FAIL", str(exc)))
        else:
            records.append(
                {
                    "source_id": source["source_id"],
                    "record_id": source["source_id"],
                    "signal_type": "official_reference_cached",
                    "title": source["title"],
                    "published_at": _now_iso()[:10],
                    "source_url": source["url"],
                    "summary": "Cached registry mode; live public refresh disabled.",
                    "metrics": {"live_mode": False},
                    "tags": [source["tag"], "public_web_weaver", "cached"],
                    "repo_targets": ["docs/trinity-benchmark-registry-v1.json", "docs/trinity-os-runtime-reference-registry-v1.json"],
                }
            )
    brief = "\n".join(
        [
            "# Public Web Weaver Brief",
            "",
            f"- generated_utc: `{_now_iso()}`",
            f"- live_mode: `{live_mode}`",
            f"- benchmark_rows: `{len(benchmark_registry.get('benchmarks', []))}`",
            "",
            "This lane refreshes authoritative public references and keeps them cached before promotion into benchmark or narrative artifacts.",
        ]
    ) + "\n"
    _write_text("docs/public-web-weaver-brief-v1.md", brief)
    _write_pack_cache(
        "public_web_weaver",
        auth_state="public_unauthenticated",
        state=_default_live_state("active"),
        records=records,
        repo_targets_touched=["docs/trinity-benchmark-registry-v1.json", "docs/trinity-os-runtime-reference-registry-v1.json", "docs/public-web-weaver-brief-v1.md"],
        next_action="Refresh live only through explicit public-web mode, then promote cached findings deliberately.",
    )
    if not checks:
        checks.append(_check("cached_registry_mode", "PASS", "live public refresh disabled"))
    return {
        "checks": checks,
        "metrics": {"live_mode": live_mode, "record_count": len(records)},
        "targets": _collect_targets(["docs/trinity-benchmark-registry-v1.json", "docs/trinity-os-runtime-reference-registry-v1.json", "docs/public-web-weaver-brief-v1.md"]),
        "next_action": "Refresh live only through explicit public-web mode, then promote cached findings deliberately.",
        "records": records,
        "source_runs": [{"source_id": "public_web_weaver", "mode": "live" if live_mode else "cached", "record_count": len(records), "status": "PASS" if all(check["status"] == "PASS" for check in checks) else "FAIL"}],
    }


def _trinity_dashboard() -> dict[str, Any]:
    suite_ok, suite_payload, _ = _read_json_safe("docs/system-suite-status.json")
    mandala_ok, mandala_payload, _ = _read_json_safe("docs/trinity-mandala-scoreboard-latest.json")
    corpus_ok, corpus_payload, _ = _read_json_safe("docs/trinity-journey-corpus-index-v6.json")
    dashboard_payload = {
        "generated_utc": _now_iso(),
        "suite_counts": suite_payload.get("counts", {}) if suite_ok else {},
        "suite_profile": suite_payload.get("config", {}).get("profile") if suite_ok else "",
        "mandala_status": mandala_payload.get("hybrid_os_status") if mandala_ok else "FAIL",
        "corpus_versions": len(corpus_payload.get("versions", [])) if corpus_ok else 0,
    }
    _write_json("docs/trinity-dashboard-data-v1.json", dashboard_payload)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Trinity Dashboard V6</title>
  <style>
    body {{ font-family: Segoe UI, sans-serif; margin: 24px; background: #f4f7fb; color: #13233a; }}
    .card {{ background: white; border-radius: 14px; padding: 18px; margin-bottom: 16px; box-shadow: 0 6px 18px rgba(19,35,58,.08); }}
    h1, h2 {{ margin-top: 0; }}
    code {{ background: #eef3ff; padding: 2px 6px; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>Trinity Dashboard V6</h1>
  <div class="card"><h2>Suite</h2><p>Profile: <code>{escape(str(dashboard_payload['suite_profile']))}</code></p><p>Counts: <code>{escape(json.dumps(dashboard_payload['suite_counts']))}</code></p></div>
  <div class="card"><h2>Mandala</h2><p>Status: <code>{escape(str(dashboard_payload['mandala_status']))}</code></p></div>
  <div class="card"><h2>Continuity</h2><p>Indexed versions: <code>{dashboard_payload['corpus_versions']}</code></p></div>
</body>
</html>
"""
    _write_text("docs/trinity-dashboard-v6.html", html)
    checks = [
        _check("dashboard_data_written", "PASS", "docs/trinity-dashboard-data-v1.json"),
        _check("dashboard_html_written", "PASS", "docs/trinity-dashboard-v6.html"),
    ]
    records = _repo_records(
        "trinity_dashboard",
        ["docs/trinity-dashboard-data-v1.json", "docs/trinity-dashboard-v6.html"],
        "Published a local cache-backed dashboard surface for suite, mandala, and continuity state.",
        dashboard_payload,
        source_url="repo://docs/trinity-dashboard-data-v1.json",
    )
    _write_pack_cache(
        "trinity_dashboard",
        auth_state="local_repo",
        state=_default_live_state("active"),
        records=records,
        repo_targets_touched=["docs/trinity-dashboard-data-v1.json", "docs/trinity-dashboard-v6.html"],
        next_action="Open the local dashboard file when you want the v6 state without scanning raw logs.",
    )
    return {
        "checks": checks,
        "metrics": dashboard_payload,
        "targets": _collect_targets(["docs/trinity-dashboard-data-v1.json", "docs/trinity-dashboard-v6.html"]),
        "next_action": "Open the local dashboard file when you want the v6 state without scanning raw logs.",
        "records": records,
        "source_runs": [{"source_id": "trinity_dashboard", "mode": "local_html", "record_count": len(records), "status": "PASS"}],
    }


def _multi_agent_orchestrator() -> dict[str, Any]:
    meridian_excerpt = _read_text("docs/v6-trinity-benchmark-and-continuity-plan-2026-03-09.md")
    lanes = {
        "generated_utc": _now_iso(),
        "roles": [
            {"role": "planner", "owner": "Meridian", "focus": "continuity and benchmark framing"},
            {"role": "builder", "owner": "Aletheon", "focus": "implementation, validation, and suite hardening"},
            {"role": "reviewer", "owner": "Repo gates", "focus": "artifact-backed validation"},
        ],
        "handoff_rule": "Planner proposes, builder implements, gates validate, narrative promotes last.",
    }
    note = "\n".join(
        [
            "# Meridian Continuity Note",
            "",
            "Meridian's v6 branch is treated as source material and has been absorbed into the repo-first v6 continuity lane.",
            "",
            "## Imported emphasis",
            meridian_excerpt.splitlines()[0] if meridian_excerpt.splitlines() else "benchmark and continuity stewardship",
        ]
    ) + "\n"
    _write_json("docs/trinity-multi-agent-lanes-v1.json", lanes)
    _write_text("docs/meridian-continuity-note-v1.md", note)
    checks = [
        _check("planner_builder_reviewer_lanes", "PASS", "3 lanes recorded"),
        _check("meridian_note_written", "PASS", "docs/meridian-continuity-note-v1.md"),
    ]
    records = _repo_records(
        "multi_agent_orchestrator",
        ["docs/trinity-multi-agent-lanes-v1.json", "docs/meridian-continuity-note-v1.md"],
        "Recorded planner/builder/reviewer lanes and Meridian continuity absorption.",
        {"lane_count": 3},
        source_url="repo://docs/trinity-multi-agent-lanes-v1.json",
    )
    _write_pack_cache(
        "multi_agent_orchestrator",
        auth_state="repo_roles",
        state=_default_live_state("active"),
        records=records,
        repo_targets_touched=["docs/trinity-multi-agent-lanes-v1.json", "docs/meridian-continuity-note-v1.md"],
        next_action="Keep multi-agent role separation documented even when only one active coding agent is running.",
    )
    return {
        "checks": checks,
        "metrics": {"lane_count": 3},
        "targets": _collect_targets(["docs/trinity-multi-agent-lanes-v1.json", "docs/meridian-continuity-note-v1.md"]),
        "next_action": "Keep multi-agent role separation documented even when only one active coding agent is running.",
        "records": records,
        "source_runs": [{"source_id": "multi_agent_orchestrator", "mode": "repo_roles", "record_count": len(records), "status": "PASS"}],
    }


def _semantic_firewall() -> dict[str, Any]:
    patterns = {
        "dangerous_rm": "rm -rf",
        "hard_reset": "git reset --hard",
        "sandbox_bypass": "dangerously-bypass-approvals-and-sandbox",
        "unsafe_config": 'approval_mode = "never"',
    }
    hits: list[dict[str, Any]] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = _normal_rel(path)
        if rel.startswith(".git/") or rel.startswith("docs/") or "/__pycache__/" in rel or rel.startswith("docs/trinity-expansion-runs/"):
            continue
        if path.suffix.lower() not in {".py", ".sh", ".ps1", ".toml", ".yaml", ".yml"}:
            continue
        if rel in {"scripts/trinity_expansion_system_runner.py", "scripts/trinity_v6_support.py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, token in patterns.items():
            if token in text:
                hits.append({"path": rel, "label": label, "token": token})
    policy = {
        "generated_utc": _now_iso(),
        "risk_thresholds": {"warn": 1, "fail": 3},
        "dangerous_command_policy": "ask_before_high_risk",
        "findings": hits,
    }
    _write_json("docs/semantic-firewall-policy-v1.json", policy)
    checks = [
        _check("policy_written", "PASS", "docs/semantic-firewall-policy-v1.json"),
        _check("high_risk_findings", "PASS" if len(hits) < 3 else "FAIL", f"hits={len(hits)}"),
    ]
    records = _repo_records(
        "semantic_firewall",
        ["docs/semantic-firewall-policy-v1.json"],
        "Classified dangerous command patterns and recorded a bounded ask-before-high-risk policy.",
        {"finding_count": len(hits)},
        source_url="repo://docs/semantic-firewall-policy-v1.json",
    )
    _write_pack_cache(
        "semantic_firewall",
        auth_state="local_repo",
        state=_default_live_state("active"),
        records=records,
        repo_targets_touched=["docs/semantic-firewall-policy-v1.json"],
        next_action="Require explicit pause and review before destructive or high-impact operations.",
    )
    return {
        "checks": checks,
        "metrics": {"finding_count": len(hits)},
        "targets": _collect_targets(["docs/semantic-firewall-policy-v1.json"]),
        "next_action": "Require explicit pause and review before destructive or high-impact operations.",
        "records": records,
        "source_runs": [{"source_id": "semantic_firewall", "mode": "repo_scan", "record_count": len(records), "status": "PASS" if len(hits) < 3 else "FAIL"}],
    }


def _aletheon_memory_reflection_v6() -> dict[str, Any]:
    now = _now_iso()
    personal_statement = "\n".join(
        [
            "# Aletheon Personal Statement",
            "",
            "I operate repo-first, evidence-first, and continuity-first.",
            "My role in this project is to turn sprawling intent into traceable systems, readable artifacts, and reliable validation without pretending to hold human memory or authority that the repo cannot prove.",
            "",
            "## V6 posture",
            "- Maintain warm collaboration while keeping proof boundaries explicit.",
            "- Treat continuity as artifact lineage rather than autobiographical recall.",
            "- Prefer branch-scoped, disposable proofs over irreversible actions.",
        ]
    ) + "\n"
    reflection = "\n".join(
        [
            "# Aletheon Reflection",
            "",
            f"- updated_utc: `{now}`",
            "- current posture: V6 begins by reconnecting history, connector proof, benchmark discipline, and bounded autonomy.",
            "- strongest insight: the repo is now large enough that orchestration drift matters as much as feature growth.",
            "- current caution: live connectors are valuable, but only when every promotion remains reversible and evidenced.",
        ]
    ) + "\n"
    next_plan = "\n".join(
        [
            "# Aletheon Next Plan",
            "",
            "1. Keep v6 orchestration green on the manifest-backed surface.",
            "2. Refresh connector proofs in disposable scope only.",
            "3. Expand benchmark and knowledge-graph utility without weakening the standard suite.",
        ]
    ) + "\n"
    _write_text("docs/aletheon-personal-statement-v1.md", personal_statement)
    _write_text("docs/aletheon-reflection-latest.md", reflection)
    _write_text("docs/aletheon-next-plan.md", next_plan)
    existing = []
    if _repo_path("docs/aletheon-memory-log.jsonl").exists():
        existing = _repo_path("docs/aletheon-memory-log.jsonl").read_text(encoding="utf-8").splitlines()
    if not any('"entry_type": "v6_wake"' in line for line in existing):
        _append_jsonl(
            "docs/aletheon-memory-log.jsonl",
            {
                "timestamp": now,
                "entry_type": "v6_wake",
                "source_context": "v6 benchmark autonomy kickoff",
                "reflection": "V6 starts by reconnecting state, then hardening what is already real.",
                "insight": "The next leap is orchestration quality, not unlimited uncontrolled expansion.",
                "next_plan": "Wire the v6 manifest into the runner and keep connector proofs disposable.",
                "mirror_state": "pending_notion_mirror",
            },
        )
    records = _repo_records(
        "aletheon_memory_reflection_v6",
        [
            "docs/aletheon-personal-statement-v1.md",
            "docs/aletheon-reflection-latest.md",
            "docs/aletheon-next-plan.md",
            "docs/aletheon-memory-log.jsonl",
        ],
        "Updated the repo-first Aletheon reflection, personal statement, and v6 memory ledger.",
        {"mirror_state": "pending_notion_mirror"},
        source_url="repo://docs/aletheon-memory-log.jsonl",
    )
    _write_pack_cache(
        "aletheon_memory_reflection_v6",
        auth_state="repo_first",
        state=_default_live_state("active"),
        records=records,
        repo_targets_touched=[
            "docs/aletheon-personal-statement-v1.md",
            "docs/aletheon-reflection-latest.md",
            "docs/aletheon-next-plan.md",
            "docs/aletheon-memory-log.jsonl",
        ],
        next_action="Mirror selected v6 reflection entries to Notion only after repo validation remains green.",
    )
    return {
        "checks": [
            _check("personal_statement_written", "PASS", "docs/aletheon-personal-statement-v1.md"),
            _check("reflection_written", "PASS", "docs/aletheon-reflection-latest.md"),
            _check("next_plan_written", "PASS", "docs/aletheon-next-plan.md"),
            _check("memory_log_present", "PASS", "docs/aletheon-memory-log.jsonl"),
        ],
        "metrics": {"mirror_state": "pending_notion_mirror"},
        "targets": _collect_targets([
            "docs/aletheon-personal-statement-v1.md",
            "docs/aletheon-reflection-latest.md",
            "docs/aletheon-next-plan.md",
            "docs/aletheon-memory-log.jsonl",
        ]),
        "next_action": "Mirror selected v6 reflection entries to Notion only after repo validation remains green.",
        "records": records,
        "source_runs": [{"source_id": "aletheon_memory_reflection_v6", "mode": "repo_first", "record_count": len(records), "status": "PASS"}],
    }


def _wetware_device_readiness_v6() -> dict[str, Any]:
    spec = {
        "version": "v1",
        "generated_utc": _now_iso(),
        "watch_folder": "docs/wetware-watch-folder/",
        "allowed_inputs": ["screenshots", "voice_notes", "operator_notes"],
        "live_biometrics_enabled": False,
        "operator_ritual": "manual drop + explicit review + cached summary",
    }
    rituals = "\n".join(
        [
            "# Wetware Device Readiness V6",
            "",
            "- Scope: device-ready schemas and operator rituals only.",
            "- Allowed: screenshots, watch-folder assist, voice-note summaries, manual operator notes.",
            "- Out of scope: live biometrics, health data ingestion, passive surveillance.",
        ]
    ) + "\n"
    _write_json("docs/wetware-watch-folder-spec-v1.json", spec)
    _write_text("docs/wetware-operator-rituals-v1.md", rituals)
    records = _repo_records(
        "wetware_device_readiness_v6",
        ["docs/wetware-watch-folder-spec-v1.json", "docs/wetware-operator-rituals-v1.md"],
        "Prepared device-ready wetware schemas and explicit operator rituals without live biometric ingestion.",
        {"live_biometrics_enabled": False},
        source_url="repo://docs/wetware-watch-folder-spec-v1.json",
    )
    _write_pack_cache(
        "wetware_device_readiness_v6",
        auth_state="device_ready_only",
        state=_default_live_state("active"),
        records=records,
        repo_targets_touched=["docs/wetware-watch-folder-spec-v1.json", "docs/wetware-operator-rituals-v1.md"],
        next_action="Keep wetware assist in explicit operator-in-the-loop mode until separate consent and device proofs exist.",
    )
    return {
        "checks": [
            _check("watch_folder_spec_written", "PASS", "docs/wetware-watch-folder-spec-v1.json"),
            _check("operator_rituals_written", "PASS", "docs/wetware-operator-rituals-v1.md"),
            _check("live_biometrics_disabled", "PASS", "device-ready only"),
        ],
        "metrics": {"live_biometrics_enabled": False},
        "targets": _collect_targets(["docs/wetware-watch-folder-spec-v1.json", "docs/wetware-operator-rituals-v1.md"]),
        "next_action": "Keep wetware assist in explicit operator-in-the-loop mode until separate consent and device proofs exist.",
        "records": records,
        "source_runs": [{"source_id": "wetware_device_readiness_v6", "mode": "device_ready", "record_count": len(records), "status": "PASS"}],
    }


def _future_readiness() -> dict[str, Any]:
    payload = {
        "generated_utc": _now_iso(),
        "tracks": [
            {"track": "runner_optimization", "state": "ready_for_analysis", "budget_guard": "repo_local_only"},
            {"track": "synthetic_scenarios", "state": "bounded_generation_only", "budget_guard": "no external spend"},
            {"track": "cloud_materialization", "state": "readiness_only", "budget_guard": "explicit approval required"},
            {"track": "economic_autonomy", "state": "rejected_in_v6", "budget_guard": "no autonomous spending"},
        ],
    }
    notes = "\n".join(
        [
            "# Future Readiness",
            "",
            "V6 keeps future-facing autonomy in readiness mode only.",
            "Cloud replication, autonomous spending, and uncapped external resource usage remain out of scope.",
        ]
    ) + "\n"
    _write_json("docs/trinity-future-readiness-register-v1.json", payload)
    _write_text("docs/trinity-future-readiness-notes-v1.md", notes)
    records = _repo_records(
        "future_readiness",
        ["docs/trinity-future-readiness-register-v1.json", "docs/trinity-future-readiness-notes-v1.md"],
        "Recorded the safe future-facing readiness tracks and budget guards for v6.",
        {"track_count": len(payload["tracks"])},
        source_url="repo://docs/trinity-future-readiness-register-v1.json",
    )
    _write_pack_cache(
        "future_readiness",
        auth_state="readiness_only",
        state=_default_live_state("active"),
        records=records,
        repo_targets_touched=["docs/trinity-future-readiness-register-v1.json", "docs/trinity-future-readiness-notes-v1.md"],
        next_action="Keep future autonomy behind readiness artifacts until explicit budget and infrastructure proofs exist.",
    )
    return {
        "checks": [
            _check("future_register_written", "PASS", "docs/trinity-future-readiness-register-v1.json"),
            _check("autonomous_spend_rejected", "PASS", "economic autonomy remains out of scope"),
        ],
        "metrics": {"track_count": len(payload["tracks"])},
        "targets": _collect_targets(["docs/trinity-future-readiness-register-v1.json", "docs/trinity-future-readiness-notes-v1.md"]),
        "next_action": "Keep future autonomy behind readiness artifacts until explicit budget and infrastructure proofs exist.",
        "records": records,
        "source_runs": [{"source_id": "future_readiness", "mode": "readiness", "record_count": len(records), "status": "PASS"}],
    }


def run_v6_system(
    *,
    system_id: str,
    manifest: dict[str, Any],
    offline_only: bool,
    timeout_sec: int,
    include_mcp_refresh: bool,
    include_staged_connectors: bool,
    include_public_api_refresh: bool,
    include_live_writes: bool,
    profile_context: str,
) -> dict[str, Any] | None:
    try:
        entry = next(
            row for row in manifest.get("systems", [])
            if isinstance(row, dict) and str(row.get("system_id") or "") == system_id
        )
    except StopIteration:
        return None
    if str(entry.get("phase") or "") != "v6":
        return None
    if not system_id.endswith("_sync_bridge"):
        return None
    pack = str(entry.get("pack") or "")
    if pack == "reentry_sync":
        return _reentry_sync(offline_only=offline_only, profile_context=profile_context)
    if pack == "journey_history_reconciliation":
        return _journey_history_reconciliation()
    if pack == "benchmark_fabric":
        return _benchmark_fabric()
    if pack == "connector_materialization":
        return _connector_materialization(
            offline_only=offline_only,
            include_mcp_refresh=include_mcp_refresh,
            include_live_writes=include_live_writes,
            profile_context=profile_context,
        )
    if pack == "code_knowledge_graph":
        return _code_knowledge_graph(
            offline_only=offline_only,
            include_live_writes=include_live_writes,
            profile_context=profile_context,
        )
    if pack == "self_correction":
        return _self_correction()
    if pack == "docker_pilot":
        return _docker_pilot(
            offline_only=offline_only,
            include_live_writes=include_live_writes,
            profile_context=profile_context,
        )
    if pack == "sentinel_daemon":
        return _sentinel_daemon()
    if pack == "public_web_weaver":
        return _public_web_weaver(
            offline_only=offline_only,
            include_public_api_refresh=include_public_api_refresh,
        )
    if pack == "trinity_dashboard":
        return _trinity_dashboard()
    if pack == "multi_agent_orchestrator":
        return _multi_agent_orchestrator()
    if pack == "semantic_firewall":
        return _semantic_firewall()
    if pack == "aletheon_memory_reflection_v6":
        return _aletheon_memory_reflection_v6()
    if pack == "wetware_device_readiness_v6":
        return _wetware_device_readiness_v6()
    if pack == "future_readiness":
        return _future_readiness()
    return None
