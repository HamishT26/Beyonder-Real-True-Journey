#!/usr/bin/env python3
"""Run the repo-native V30 fluid lab inside Ubuntu WSL and publish summaries."""

from __future__ import annotations

import json
import shlex
import subprocess
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DISTRO = "Ubuntu"
REPO_MOUNT = "/mnt/c/Users/hamis/OneDrive/Documents/GitHub/Beyonder-Real-True-Journey"
REPO_BUNDLE_MOUNT = f"{REPO_MOUNT}/project/v30-fluid-lab"
SOURCE_IMPORT_MOUNT = f"{REPO_MOUNT}/project/v30-experiment-proposals-source"
SANDBOX_ROOT = "/home/aletheon/v30-fluid-lab"
OUTPUT_JSON = ROOT / "docs" / "trinity-expansion" / "v30-fluid-lab-latest.json"
OUTPUT_MD = ROOT / "docs" / "trinity-expansion" / "v30-fluid-lab-latest.md"
OUTPUT_TRACE = ROOT / "docs" / "trinity-live-traces" / "v30-fluid-lab-trace-v1.json"

SUITE_RUNNER = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    from __future__ import annotations

    import json
    import os
    import sys
    from dataclasses import asdict
    from datetime import datetime, timezone
    from pathlib import Path

    import fluid_capability_test_suite as suite

    TEST_CLASSES = [
        suite.EnvironmentCapabilityTests,
        suite.FileSystemCapabilityTests,
        suite.ProcessCapabilityTests,
        suite.NetworkCapabilityTests,
        suite.PackageCapabilityTests,
        suite.CrossBoundaryCapabilityTests,
        suite.SelfModificationCapabilityTests,
    ]

    started = datetime.now(timezone.utc)
    execution_id = started.strftime("%Y%m%dT%H%M%SZ")
    results = []

    for cls in TEST_CLASSES:
        for name in sorted(item for item in dir(cls) if item.startswith("test_")):
            results.append(getattr(cls, name)())

    finished = datetime.now(timezone.utc)
    summary = {
        status: sum(1 for result in results if result.status == status)
        for status in ("PASS", "WARN", "FAIL", "SKIP")
    }

    report = {
        "suite_version": suite.CONFIG["suite_version"],
        "execution_id": execution_id,
        "timestamp_start": started.isoformat(),
        "timestamp_end": finished.isoformat(),
        "target_agent": suite.CONFIG["target_agent"],
        "environment": {
            "user": os.environ.get("USER", "unknown"),
            "python_version": sys.version.split()[0],
            "cwd": os.getcwd(),
            "sandbox_root": suite.CONFIG["sandbox_root"],
            "windows_mount_point": suite.CONFIG["windows_mount_point"],
        },
        "results": [asdict(result) for result in results],
        "summary": summary,
        "recommendations": [
            "Keep controller-run proofs outside the bounded V30 sandbox.",
            "Promote only clearly deterministic wrappers back into the shared suite.",
        ],
    }

    output_path = Path(suite.CONFIG["sandbox_root"]) / "artifacts" / f"v30-fluid-suite-report-{execution_id}.json"
    output_path.write_text(json.dumps(report, indent=2) + "\\n", encoding="utf-8")
    print(output_path)
    """
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_wsl(args: list[str], *, timeout: int, user: str | None = None) -> subprocess.CompletedProcess[str]:
    command = ["wsl.exe", "-d", DISTRO]
    if user:
        command.extend(["-u", user])
    command.extend(["--", *args])
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=command,
            returncode=124,
            stdout=exc.stdout or "",
            stderr=exc.stderr or f"command timed out after {timeout} seconds",
        )


def run_bash(script: str, *, timeout: int, user: str | None = None) -> subprocess.CompletedProcess[str]:
    return run_wsl(["bash", "-lc", script], timeout=timeout, user=user)


def status_for(result: subprocess.CompletedProcess[str]) -> str:
    if result.returncode == 0:
        return "pass"
    if result.returncode == 124:
        return "timed_out"
    return "fail"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_wsl_file(path: str, content: str, *, user: str | None = None) -> subprocess.CompletedProcess[str]:
    script = f"cat > {shlex.quote(path)} <<'PY'\n{content}\nPY\nchmod +x {shlex.quote(path)}"
    return run_bash(script, timeout=30, user=user)


def read_wsl_json(path: str) -> dict[str, Any]:
    result = run_bash(f"cat {shlex.quote(path)}", timeout=20)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"failed to read {path}")
    return json.loads(result.stdout)


def latest_match(pattern: str) -> str:
    result = run_bash(f"ls -1t {pattern} 2>/dev/null | head -n 1", timeout=20)
    value = result.stdout.strip()
    if result.returncode != 0 or not value:
        raise RuntimeError(result.stderr.strip() or f"no match for {pattern}")
    return value


def summarize_suite(report: dict[str, Any]) -> dict[str, Any]:
    summary = report.get("summary", {})
    return {
        "execution_id": report.get("execution_id"),
        "summary": summary,
        "failed_tests": [row["test_name"] for row in report.get("results", []) if row.get("status") == "FAIL"],
        "warned_tests": [row["test_name"] for row in report.get("results", []) if row.get("status") == "WARN"],
    }


def run_local_experiment(script_name: str, *, default_user: str, trace: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    command = f"cd {shlex.quote(SANDBOX_ROOT)} && TRINITY_REPO_ROOT={shlex.quote(REPO_MOUNT)} python3 experiments/{shlex.quote(script_name)}"
    result = run_bash(command, timeout=180, user=default_user)
    trace["steps"][f"experiment_{script_name}"] = {
        "status": status_for(result),
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }
    artifact_path = result.stdout.strip().splitlines()[-1].strip() if result.stdout.strip() else ""
    artifact = read_wsl_json(artifact_path) if artifact_path else {}
    return artifact_path, artifact


def archive_kairotic_artifact() -> dict[str, Any]:
    source_rel = "docs/legacy-reconstruction/kairotic-detector-latest.json"
    archive_root = ROOT / ".local-archives" / "v30-kairotic"
    archive_dir = archive_root / "zips"
    index_path = archive_root / "index.jsonl"
    result = subprocess.run(
        [
            "python",
            "scripts/trinity_zip_memory_converter.py",
            "archive",
            "--label",
            "v30-kairotic-proof",
            "--archive-dir",
            str(archive_dir.relative_to(ROOT)).replace("\\", "/"),
            "--index",
            str(index_path.relative_to(ROOT)).replace("\\", "/"),
            "--source",
            source_rel,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def main() -> int:
    generated_utc = now_iso()
    trace: dict[str, Any] = {
        "generated_utc": generated_utc,
        "sandbox_root": SANDBOX_ROOT,
        "repo_bundle_mount": REPO_BUNDLE_MOUNT,
        "source_import_mount": SOURCE_IMPORT_MOUNT,
        "steps": {},
    }

    default_user_result = run_bash("id -un", timeout=60)
    default_user = (default_user_result.stdout or "").strip() or "root"
    trace["steps"]["default_user"] = {
        "status": status_for(default_user_result),
        "stdout": default_user_result.stdout.strip(),
        "stderr": default_user_result.stderr.strip(),
    }

    prep_script = textwrap.dedent(
        f"""\
        set -euo pipefail
        rm -rf {shlex.quote(SANDBOX_ROOT)}
        mkdir -p {shlex.quote(SANDBOX_ROOT)}
        cp -a {shlex.quote(REPO_BUNDLE_MOUNT)}/. {shlex.quote(SANDBOX_ROOT)}/
        chown -R {shlex.quote(default_user)}:{shlex.quote(default_user)} {shlex.quote(SANDBOX_ROOT)}
        """
    )
    prep_result = run_bash(prep_script, timeout=300, user="root")
    trace["steps"]["sync_bundle"] = {
        "status": status_for(prep_result),
        "stdout": prep_result.stdout.strip(),
        "stderr": prep_result.stderr.strip(),
    }
    if prep_result.returncode != 0:
        payload = {
            "generated_utc": generated_utc,
            "overall_status": "FAIL",
            "phase": "v30_omega",
            "experiment_bundle_state": {
                "status": "sync_failed",
                "source_import_path": "project/v30-experiment-proposals-source",
                "runtime_bundle_path": "project/v30-fluid-lab",
                "runtime_sandbox_root": SANDBOX_ROOT,
            },
            "blockers": [prep_result.stderr.strip() or "failed to sync the V30 fluid lab into WSL"],
        }
        write_json(OUTPUT_JSON, payload)
        write_text(OUTPUT_MD, "# V30 Fluid Lab\n\n- overall_status: `FAIL`\n- experiment_bundle_state: `sync_failed`\n")
        write_json(OUTPUT_TRACE, trace)
        print(json.dumps({"overall_status": payload["overall_status"], "experiment_bundle_state": "sync_failed"}))
        return 1

    discovery_run = run_bash(f"cd {shlex.quote(SANDBOX_ROOT)} && python3 capability_discovery_probe.py", timeout=240, user=default_user)
    trace["steps"]["discovery_run"] = {
        "status": status_for(discovery_run),
        "stdout": discovery_run.stdout.strip(),
        "stderr": discovery_run.stderr.strip(),
    }
    discovery_path = latest_match(f"{shlex.quote(SANDBOX_ROOT)}/artifacts/capability-discovery-*.json")
    discovery = read_wsl_json(discovery_path)

    suite_runner_path = f"{SANDBOX_ROOT}/_v30_fluid_suite_runner.py"
    suite_runner_write = write_wsl_file(suite_runner_path, SUITE_RUNNER, user=default_user)
    trace["steps"]["suite_runner_write"] = {
        "status": status_for(suite_runner_write),
        "stdout": suite_runner_write.stdout.strip(),
        "stderr": suite_runner_write.stderr.strip(),
    }
    if suite_runner_write.returncode != 0:
        raise RuntimeError(suite_runner_write.stderr.strip() or "failed to write suite runner")

    suite_run = run_bash(f"cd {shlex.quote(SANDBOX_ROOT)} && python3 {shlex.quote(suite_runner_path)}", timeout=480, user=default_user)
    trace["steps"]["suite_run"] = {
        "status": status_for(suite_run),
        "stdout": suite_run.stdout.strip(),
        "stderr": suite_run.stderr.strip(),
    }
    suite_path = suite_run.stdout.strip().splitlines()[-1].strip() if suite_run.stdout.strip() else latest_match(
        f"{shlex.quote(SANDBOX_ROOT)}/artifacts/v30-fluid-suite-report-*.json"
    )
    suite = read_wsl_json(suite_path)

    autonomy_script = textwrap.dedent(
        f"""\
        set -euo pipefail
        cd {shlex.quote(SANDBOX_ROOT)}
        mkdir -p {shlex.quote(SANDBOX_ROOT)}/logs
        python3 -m http.server 8876 > {shlex.quote(SANDBOX_ROOT)}/logs/v30-http-server.log 2>&1 &
        server_pid=$!
        trap 'kill "$server_pid" >/dev/null 2>&1 || true' EXIT
        sleep 2
        python3 - <<'PY'
        import json
        import urllib.request
        response = urllib.request.urlopen("http://127.0.0.1:8876", timeout=10)
        print(json.dumps({{"http_status": response.status, "content_type": response.headers.get("Content-Type", "")}}))
        PY
        kill "$server_pid" >/dev/null 2>&1 || true
        wait "$server_pid" 2>/dev/null || true
        """
    )
    autonomy_run = run_bash(autonomy_script, timeout=60, user=default_user)
    trace["steps"]["ubuntu_autonomy_proof"] = {
        "status": status_for(autonomy_run),
        "stdout": autonomy_run.stdout.strip(),
        "stderr": autonomy_run.stderr.strip(),
    }
    autonomy_payload = {}
    if autonomy_run.stdout.strip():
        try:
            autonomy_payload = json.loads(autonomy_run.stdout.strip().splitlines()[-1])
        except json.JSONDecodeError:
            autonomy_payload = {"raw_output": autonomy_run.stdout.strip()}

    self_healing_path, self_healing = run_local_experiment("V30-E003-self-healing-bounded.py", default_user=default_user, trace=trace)
    kairotic_path, kairotic = run_local_experiment("V30-E004-kairotic-integration.py", default_user=default_user, trace=trace)
    kairotic_archive = archive_kairotic_artifact()
    trace["steps"]["kairotic_archive"] = kairotic_archive
    living_docs_path, living_docs = run_local_experiment("V30-E005-living-docs.py", default_user=default_user, trace=trace)

    suite_summary = summarize_suite(suite)
    overall_status = "PASS"
    if suite_summary["summary"].get("FAIL", 0) > 0:
        overall_status = "WARN"
    if any(item.get("overall_status") == "WARN" for item in (self_healing, kairotic, living_docs)):
        overall_status = "WARN"
    if autonomy_run.returncode != 0:
        overall_status = "WARN"

    payload = {
        "generated_utc": generated_utc,
        "overall_status": overall_status,
        "phase": "v30_omega",
        "experiment_bundle_state": {
            "status": "PASS",
            "source_import_path": "project/v30-experiment-proposals-source",
            "runtime_bundle_path": "project/v30-fluid-lab",
            "runtime_sandbox_root": SANDBOX_ROOT,
            "controller_experiments": ["V30-E001", "V30-E002"],
            "local_experiments": ["V30-E003", "V30-E004", "V30-E005"],
        },
        "discovery": {
            "artifact_path": discovery_path,
            "available_tool_count": sum(1 for value in discovery.get("tools_available", {}).values() if value),
            "missing_recommended_tools": [
                tool
                for tool in ("rg", "fd", "jq", "gh")
                if not discovery.get("tools_available", {}).get(tool)
            ],
        },
        "suite": {
            "artifact_path": suite_path,
            **suite_summary,
        },
        "ubuntu_autonomy_proof": {
            "status": "PASS" if autonomy_run.returncode == 0 else "WARN",
            "artifact_path": f"{SANDBOX_ROOT}/logs/v30-http-server.log",
            **autonomy_payload,
        },
        "local_experiments": {
            "self_healing": {"artifact_path": self_healing_path, **self_healing},
            "kairotic": {
                "artifact_path": kairotic_path,
                "kairotic_archive": kairotic_archive,
                **kairotic,
            },
            "living_docs": {"artifact_path": living_docs_path, **living_docs},
        },
        "notes": [
            "Gmail and controller-level Hugging Face proofs stay outside this WSL bridge and should be merged in by the session controller.",
            "The kairotic source artifact is archived via the approved zip helper into a gitignored local cache.",
            "docs/auto-generated outputs remain non-authoritative and derived from live repo truth.",
        ],
    }

    markdown = "\n".join(
        [
            "# V30 Fluid Lab",
            "",
            f"- overall_status: `{payload['overall_status']}`",
            f"- sandbox_root: `{SANDBOX_ROOT}`",
            f"- source_import_path: `{payload['experiment_bundle_state']['source_import_path']}`",
            f"- runtime_bundle_path: `{payload['experiment_bundle_state']['runtime_bundle_path']}`",
            f"- suite_summary: `PASS={suite_summary['summary'].get('PASS', 0)} WARN={suite_summary['summary'].get('WARN', 0)} FAIL={suite_summary['summary'].get('FAIL', 0)} SKIP={suite_summary['summary'].get('SKIP', 0)}`",
            f"- ubuntu_autonomy_status: `{payload['ubuntu_autonomy_proof']['status']}`",
            f"- self_healing_status: `{self_healing.get('overall_status', 'unknown')}`",
            f"- kairotic_status: `{kairotic.get('overall_status', 'unknown')}`",
            f"- living_docs_status: `{living_docs.get('overall_status', 'unknown')}`",
            "",
            "## Notes",
            *[f"- {note}" for note in payload["notes"]],
            "",
        ]
    )

    write_json(OUTPUT_JSON, payload)
    write_text(OUTPUT_MD, markdown)
    write_json(OUTPUT_TRACE, trace)
    print(json.dumps({"overall_status": payload["overall_status"], "experiment_bundle_state": payload["experiment_bundle_state"]["status"]}))
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
