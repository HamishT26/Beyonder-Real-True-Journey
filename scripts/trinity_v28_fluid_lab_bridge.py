#!/usr/bin/env python3
"""Run the bounded v28 fluid-lab pilot in Ubuntu WSL and publish repo summaries."""

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
REPO_BUNDLE_MOUNT = f"{REPO_MOUNT}/project/v28-fluid-lab"
SANDBOX_ROOT = "/home/aletheon/v28-fluid-lab"
OUTPUT_JSON = ROOT / "docs" / "trinity-expansion" / "v28-fluid-lab-pilot-latest.json"
OUTPUT_MD = ROOT / "docs" / "trinity-expansion" / "v28-fluid-lab-pilot-latest.md"
OUTPUT_TRACE = ROOT / "docs" / "trinity-live-traces" / "v28-fluid-lab-pilot-v1.json"

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

    recommendations = []
    if summary["FAIL"] > 0:
        recommendations.append("Review FAIL results before promoting any fluid-lab outputs.")
    if summary["WARN"] > 0:
        recommendations.append("Capture WARN reasons in continuity before widening the fluid lane.")
    if summary["FAIL"] == 0 and summary["WARN"] == 0:
        recommendations.append("The bounded fluid capability suite completed cleanly.")

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
        "recommendations": recommendations,
        "next_steps": [
            "Keep the fluid pilot out of the shared suite until it is explicitly promoted.",
            "Use one bounded follow-up experiment only when the suite finishes without safety concerns.",
        ],
    }

    output_path = Path(suite.CONFIG["sandbox_root"]) / "artifacts" / f"fluid-suite-report-{execution_id}.json"
    output_path.write_text(json.dumps(report, indent=2) + "\\n", encoding="utf-8")
    print(output_path)
    """
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _run_wsl(
    args: list[str],
    *,
    timeout: int,
    user: str | None = None,
) -> subprocess.CompletedProcess[str]:
    command = ["wsl.exe", "-d", DISTRO]
    if user:
        command.extend(["-u", user])
    command.extend(["--", *args])
    try:
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=command,
            returncode=124,
            stdout=exc.stdout or "",
            stderr=exc.stderr or f"command timed out after {timeout} seconds",
        )


def _run_bash(script: str, *, timeout: int, user: str | None = None) -> subprocess.CompletedProcess[str]:
    return _run_wsl(["bash", "-lc", script], timeout=timeout, user=user)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _read_wsl_text(path: str) -> str:
    result = _run_bash(f"cat {shlex.quote(path)}", timeout=30)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"failed to read {path}")
    return result.stdout


def _read_wsl_json(path: str) -> dict[str, Any]:
    return json.loads(_read_wsl_text(path))


def _latest_match(pattern: str) -> str:
    result = _run_bash(f"ls -1t {pattern} 2>/dev/null | head -n 1", timeout=30)
    value = result.stdout.strip()
    if result.returncode != 0 or not value:
        raise RuntimeError(result.stderr.strip() or f"no match for {pattern}")
    return value


def _write_wsl_file(path: str, content: str, *, user: str | None = None) -> subprocess.CompletedProcess[str]:
    script = (
        f"cat > {shlex.quote(path)} <<'PY'\n"
        f"{content}"
        "\nPY\n"
        f"chmod +x {shlex.quote(path)}"
    )
    return _run_bash(script, timeout=30, user=user)


def _status_for(result: subprocess.CompletedProcess[str]) -> str:
    if result.returncode == 0:
        return "pass"
    if result.returncode == 124:
        return "timed_out"
    return "fail"


def _experiment_runner_code(experiment_kind: str) -> str:
    if experiment_kind == "package_installation":
        return textwrap.dedent(
            """\
            #!/usr/bin/env python3
            from __future__ import annotations

            import json
            import subprocess

            import fluid_experiment_runner as fer
            from fluid_experiment_runner import FluidExperimentRunner

            baseline_processes = subprocess.run(
                ["bash", "-lc", "ps -eo pid= | wc -l"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            try:
                process_budget = int((baseline_processes.stdout or "0").strip()) + 10
            except ValueError:
                process_budget = 64

            fer.MAX_CONCURRENT_PROCESSES = max(fer.MAX_CONCURRENT_PROCESSES, process_budget)

            runner = FluidExperimentRunner()
            proposal = runner.create_proposal(
                category="package_installation",
                title="Install bounded fluid pilot packages",
                description="Install ripgrep, fd-find, and jq inside the Ubuntu lane for the fluid pilot.",
                expected_outcome="Requested packages available in PATH after the experiment.",
                commands_or_code="ripgrep fd-find jq",
            )
            proposal.estimated_duration_seconds = 180
            result = runner.run_experiment(proposal)
            print(json.dumps({"experiment_id": result.experiment_id, "status": result.status, "category": proposal.category}))
            """
        )

    generated_code = textwrap.dedent(
        """\
        #!/usr/bin/env python3
        from pathlib import Path
        import json
        import shutil

        payload = {
            "rg": bool(shutil.which("rg")),
            "fd": bool(shutil.which("fd")),
            "jq": bool(shutil.which("jq")),
        }
        output_path = Path("tooling-snapshot.json")
        output_path.write_text(json.dumps(payload, indent=2) + "\\\\n", encoding="utf-8")
        print(output_path.read_text(encoding="utf-8").strip())
        """
    )

    return textwrap.dedent(
        f"""\
        #!/usr/bin/env python3
        from __future__ import annotations

        import json
        import subprocess

        import fluid_experiment_runner as fer
        from fluid_experiment_runner import FluidExperimentRunner

        baseline_processes = subprocess.run(
            ["bash", "-lc", "ps -eo pid= | wc -l"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        try:
            process_budget = int((baseline_processes.stdout or "0").strip()) + 10
        except ValueError:
            process_budget = 64

        fer.MAX_CONCURRENT_PROCESSES = max(fer.MAX_CONCURRENT_PROCESSES, process_budget)

        runner = FluidExperimentRunner()
        proposal = runner.create_proposal(
            category="code_generation",
            title="Generate bounded tooling snapshot utility",
            description="Create a small utility that records rg/fd/jq availability inside the fluid sandbox.",
            expected_outcome="A tooling snapshot JSON file is generated inside the experiment directory.",
            commands_or_code={json.dumps(generated_code)},
        )
        proposal.estimated_duration_seconds = 30
        result = runner.run_experiment(proposal)
        print(json.dumps({{"experiment_id": result.experiment_id, "status": result.status, "category": proposal.category}}))
        """
    )


def _summarize_discovery(discovery: dict[str, Any]) -> dict[str, Any]:
    tools = discovery.get("tools_available", {})
    capabilities = discovery.get("capabilities", {})
    recommendations = discovery.get("recommendations", [])
    available_count = sum(1 for value in tools.values() if value)
    missing_recommended = [
        tool
        for tool, present in (("rg", tools.get("rg")), ("fd", tools.get("fd")), ("jq", tools.get("jq")))
        if not present
    ]
    return {
        "environment": discovery.get("environment"),
        "available_tool_count": available_count,
        "missing_recommended_tools": missing_recommended,
        "languages_available": sorted(discovery.get("languages_available", {}).keys()),
        "network_outbound": bool(capabilities.get("network", {}).get("can_connect_outbound")),
        "wsl_detected": bool(capabilities.get("environment", {}).get("wsl", {}).get("is_wsl")),
        "recommendations": recommendations,
    }


def _summarize_suite(report: dict[str, Any]) -> dict[str, Any]:
    results = report.get("results", [])
    summary = report.get("summary", {})
    failed = [row["test_name"] for row in results if row.get("status") == "FAIL"]
    warned = [row["test_name"] for row in results if row.get("status") == "WARN"]
    return {
        "execution_id": report.get("execution_id"),
        "summary": summary,
        "failed_tests": failed,
        "warned_tests": warned,
        "recommendations": report.get("recommendations", []),
    }


def _summarize_experiment(result: dict[str, Any], kind: str) -> dict[str, Any]:
    return {
        "requested_kind": kind,
        "result_status": result.get("status"),
        "safety_violation_count": len(result.get("safety_violations", [])),
        "artifacts_created": result.get("artifacts_created", []),
        "learnings": result.get("learnings", []),
        "next_experiments_suggested": result.get("next_experiments_suggested", []),
    }


def main() -> int:
    generated_utc = _now_iso()
    trace: dict[str, Any] = {
        "generated_utc": generated_utc,
        "sandbox_root": SANDBOX_ROOT,
        "repo_bundle_mount": REPO_BUNDLE_MOUNT,
        "steps": {},
    }

    default_user_result = _run_bash("id -un", timeout=120)
    default_user = (default_user_result.stdout or "").strip() or "root"
    trace["steps"]["default_user"] = {
        "status": _status_for(default_user_result),
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
    prep_result = _run_bash(prep_script, timeout=300, user="root")
    trace["steps"]["sync_bundle"] = {
        "status": _status_for(prep_result),
        "stdout": prep_result.stdout.strip(),
        "stderr": prep_result.stderr.strip(),
    }
    if prep_result.returncode != 0:
        payload = {
            "generated_utc": generated_utc,
            "overall_status": "FAIL",
            "phase": "v28_omega",
            "pilot_state": "sync_failed",
            "sandbox_root": SANDBOX_ROOT,
            "repo_bundle_mount": REPO_BUNDLE_MOUNT,
            "blockers": [prep_result.stderr.strip() or "failed to sync the fluid bundle into WSL"],
        }
        _write_json(OUTPUT_JSON, payload)
        _write_text(
            OUTPUT_MD,
            "\n".join(
                [
                    "# V28 Fluid Lab Pilot",
                    "",
                    "- overall_status: `FAIL`",
                    "- pilot_state: `sync_failed`",
                    f"- blocker: `{payload['blockers'][0]}`",
                ]
            )
            + "\n",
        )
        _write_json(OUTPUT_TRACE, trace)
        print(json.dumps({"overall_status": payload["overall_status"], "pilot_state": payload["pilot_state"]}))
        return 1

    discovery_run = _run_bash(f"cd {shlex.quote(SANDBOX_ROOT)} && python3 capability_discovery_probe.py", timeout=240)
    trace["steps"]["discovery_run"] = {
        "status": _status_for(discovery_run),
        "stdout": discovery_run.stdout.strip(),
        "stderr": discovery_run.stderr.strip(),
    }
    discovery_path = _latest_match(f"{shlex.quote(SANDBOX_ROOT)}/artifacts/capability-discovery-*.json")
    discovery_payload = _read_wsl_json(discovery_path)

    suite_runner_path = f"{SANDBOX_ROOT}/_v28_fluid_suite_runner.py"
    suite_runner_write = _write_wsl_file(suite_runner_path, SUITE_RUNNER, user=default_user)
    trace["steps"]["suite_runner_write"] = {
        "status": _status_for(suite_runner_write),
        "stdout": suite_runner_write.stdout.strip(),
        "stderr": suite_runner_write.stderr.strip(),
    }
    if suite_runner_write.returncode != 0:
        raise RuntimeError(suite_runner_write.stderr.strip() or "failed to write suite runner into WSL sandbox")

    suite_run = _run_bash(f"cd {shlex.quote(SANDBOX_ROOT)} && python3 {shlex.quote(suite_runner_path)}", timeout=480)
    trace["steps"]["suite_run"] = {
        "status": _status_for(suite_run),
        "stdout": suite_run.stdout.strip(),
        "stderr": suite_run.stderr.strip(),
    }
    suite_path = suite_run.stdout.strip().splitlines()[-1].strip() if suite_run.stdout.strip() else _latest_match(
        f"{shlex.quote(SANDBOX_ROOT)}/artifacts/fluid-suite-report-*.json"
    )
    suite_payload = _read_wsl_json(suite_path)

    sudo_probe = _run_bash("sudo -n true >/dev/null 2>&1; printf '%s' $?", timeout=10)
    trace["steps"]["sudo_probe"] = {
        "status": _status_for(sudo_probe),
        "stdout": sudo_probe.stdout.strip(),
        "stderr": sudo_probe.stderr.strip(),
    }
    required_tools = discovery_payload.get("tools_available", {})
    missing_recommended_tools = [
        tool
        for tool, present in (("rg", required_tools.get("rg")), ("fd", required_tools.get("fd")), ("jq", required_tools.get("jq")))
        if not present
    ]
    experiment_kind = "code_generation"
    experiment_runner_path = f"{SANDBOX_ROOT}/_v28_fluid_experiment_runner.py"
    experiment_runner_write = _write_wsl_file(
        experiment_runner_path,
        _experiment_runner_code(experiment_kind),
        user=default_user,
    )
    trace["steps"]["experiment_runner_write"] = {
        "status": _status_for(experiment_runner_write),
        "stdout": experiment_runner_write.stdout.strip(),
        "stderr": experiment_runner_write.stderr.strip(),
    }
    if experiment_runner_write.returncode != 0:
        raise RuntimeError(experiment_runner_write.stderr.strip() or "failed to write experiment runner into WSL sandbox")

    experiment_run = _run_bash(f"cd {shlex.quote(SANDBOX_ROOT)} && python3 {shlex.quote(experiment_runner_path)}", timeout=600)
    trace["steps"]["experiment_run"] = {
        "status": _status_for(experiment_run),
        "stdout": experiment_run.stdout.strip(),
        "stderr": experiment_run.stderr.strip(),
    }
    experiment_result_path = ""
    try:
        experiment_result_path = _latest_match(f"{shlex.quote(SANDBOX_ROOT)}/artifacts/exp-*-result.json")
        experiment_payload = _read_wsl_json(experiment_result_path)
    except RuntimeError:
        experiment_payload = {
            "status": "FAILURE",
            "safety_violations": [],
            "artifacts_created": [],
            "learnings": [
                "The bounded follow-up experiment did not emit a result artifact.",
                "Review the experiment stdout and stderr in the fluid pilot trace before promoting this lane.",
            ],
            "next_experiments_suggested": [],
        }

    suite_summary = _summarize_suite(suite_payload)
    experiment_summary = _summarize_experiment(experiment_payload, experiment_kind)
    safety_violation_free = experiment_summary["safety_violation_count"] == 0
    suite_pass = suite_summary["summary"].get("FAIL", 0) == 0
    overall_status = "PASS" if suite_pass and safety_violation_free else "WARN"
    pilot_state = "completed_without_safety_violations" if suite_pass and safety_violation_free else "completed_with_followup_warnings"

    payload = {
        "generated_utc": generated_utc,
        "overall_status": overall_status,
        "phase": "v28_omega",
        "pilot_state": pilot_state,
        "sandbox_root": SANDBOX_ROOT,
        "repo_bundle_mount": REPO_BUNDLE_MOUNT,
        "sync_state": "synced",
        "discovery": {
            "status": "PASS" if trace["steps"]["discovery_run"]["status"] == "pass" else "WARN",
            "artifact_path": discovery_path,
            **_summarize_discovery(discovery_payload),
        },
        "suite": {
            "status": "PASS" if suite_pass else "WARN",
            "artifact_path": suite_path,
            **suite_summary,
        },
        "follow_up_experiment": {
            "status": "PASS" if experiment_summary["result_status"] == "SUCCESS" and safety_violation_free else "WARN",
            "artifact_path": experiment_result_path,
            **experiment_summary,
        },
        "package_install_targets_deferred": missing_recommended_tools,
        "fluid_lab_state": {
            "status": "pass" if overall_status == "PASS" else "warn",
            "sandbox_root": SANDBOX_ROOT,
            "discovery_completed": True,
            "suite_completed": True,
            "safety_violation_free": safety_violation_free,
            "follow_up_category": experiment_kind,
        },
        "next_steps": [
            "Keep the fluid pilot out of the shared suite until an explicit promotion lane proves deterministic wrapper behavior.",
            "Use package installation only as a separately approved follow-up if the bounded pilot needs rg, fd-find, or jq inside WSL.",
        ],
    }

    markdown = "\n".join(
        [
            "# V28 Fluid Lab Pilot",
            "",
            f"- overall_status: `{payload['overall_status']}`",
            f"- pilot_state: `{payload['pilot_state']}`",
            f"- sandbox_root: `{SANDBOX_ROOT}`",
            f"- suite_summary: `PASS={suite_summary['summary'].get('PASS', 0)} WARN={suite_summary['summary'].get('WARN', 0)} FAIL={suite_summary['summary'].get('FAIL', 0)} SKIP={suite_summary['summary'].get('SKIP', 0)}`",
            f"- follow_up_category: `{experiment_kind}`",
            f"- follow_up_status: `{experiment_summary['result_status']}`",
            "",
            "## Discovery",
            f"- available_tool_count: `{payload['discovery']['available_tool_count']}`",
            f"- missing_recommended_tools: `{', '.join(payload['discovery']['missing_recommended_tools']) or 'none'}`",
            f"- network_outbound: `{payload['discovery']['network_outbound']}`",
            "",
            "## Follow-Up",
            f"- safety_violation_free: `{safety_violation_free}`",
            f"- artifacts_created: `{len(experiment_summary['artifacts_created'])}`",
            f"- package_install_targets_deferred: `{', '.join(missing_recommended_tools) or 'none'}`",
        ]
    ) + "\n"

    _write_json(OUTPUT_JSON, payload)
    _write_text(OUTPUT_MD, markdown)
    _write_json(OUTPUT_TRACE, trace)

    print(json.dumps({"overall_status": payload["overall_status"], "pilot_state": payload["pilot_state"]}))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
