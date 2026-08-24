"""One bounded D-isolated toolchain transaction for Neris v667-v8-r3."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "neris-solane" / "v667-v8-r3"
RECEIPT_PATH = PHASE_ROOT / "x2" / "tooling" / "thirteen-tool-transaction-receipt.json"
TOOL_ROOT = Path("D:" + "/GHC-Archives/toolchains/neris-solane-v667-v8-r3")
X1_HEAD = "705f4cda336639d2a700d2d830a975cd281c7e4b"

PYTHON_TOOLS = [
    {"name": "nox", "version": "2026.8.17", "wheel": "nox-2026.8.17-py3-none-any.whl", "sha256": "a96a5286007cbc0d1eb1930e85738668f6722adba1ffaa48287296a96963086e", "command": "nox"},
    {"name": "tox", "version": "4.60.0", "wheel": "tox-4.60.0-py3-none-any.whl", "sha256": "175abbc4cdef615d66874c0843be4f44c353c14aab6d89939bb22246f84122bd", "command": "tox"},
    {"name": "towncrier", "version": "25.8.0", "wheel": "towncrier-25.8.0-py3-none-any.whl", "sha256": "b953d133d98f9aeae9084b56a3563fd2519dfc6ec33f61c9cd2c61ff243fb513", "command": "towncrier"},
    {"name": "doc8", "version": "2.0.0", "wheel": "doc8-2.0.0-py3-none-any.whl", "sha256": "9862710027f793c25f9b1899150660e4bf1d4c9a6738742e71f32011e2e3f590", "command": "doc8"},
    {"name": "pyroma", "version": "5.0.1", "wheel": "pyroma-5.0.1-py3-none-any.whl", "sha256": "e71fd3e0f213b36870a607eccf491241dbadf5462ec1cdda94d08bfa1c26951e", "command": "pyroma"},
    {"name": "pyupgrade", "version": "3.21.2", "wheel": "pyupgrade-3.21.2-py2.py3-none-any.whl", "sha256": "2ac7b95cbd176475041e4dfe8ef81298bd4654a244f957167bd68af37d52be9f", "command": "pyupgrade"},
    {"name": "validate-pyproject", "version": "0.26", "wheel": "validate_pyproject-0.26-py3-none-any.whl", "sha256": "ab3fa448d7178d44d1b06e4b526ab5136e3faa7a1b7e7c6320c8a17fc11a9a2e", "command": "validate-pyproject"},
    {"name": "pipx", "version": "1.16.7", "wheel": "pipx-1.16.7-py3-none-any.whl", "sha256": "ff9719b1ef80edb8d08ad76862103c6100ff4e3f5e9012b441f51e7b5a04fa5b", "command": "pipx"},
]

NODE_TOOLS = [
    {"name": "dependency-cruiser", "version": "18.2.0", "integrity": "sha512-xMDoLD0no6pDInR8/4rIIqZ4mERDnsjezk8PkNORYSfBLvjCOogUxaruepmi1uQtZQlYUgdT2u7G3jTlgKqNjw==", "command": "depcruise"},
    {"name": "jscpd", "version": "5.0.16", "integrity": "sha512-TiQ4zKtKeldep6UswXFHjVCDhVdLBaJyQcZjhCSzVOmKpT6HBj0jUZiphP1vK1X3VSSuzwcfifJVNpsOIiwRCg==", "command": "jscpd"},
    {"name": "package-json-validator-cli", "version": "0.1.11", "integrity": "sha512-j+lMnQni8EzTZuV3yuHV9zs2Kj+whYLc7hsOB1RQJTeEW3sISWDbD1mVQj2e4VQ8iEAVIGTyAzHgiMlHcibqSQ==", "command": "package-json-validator-cli"},
    {"name": "license-checker-rseidelsohn", "version": "5.0.1", "integrity": "sha512-9X+ikKxt9Hy3zOrOZzW1dXL4St5akoYjLt63Am9JZVzU6aTdN+xfDvqySpnJT+gF/h5RmtMk2waW6TDNNCKbqQ==", "command": "license-checker-rseidelsohn"},
    {"name": "sherif", "version": "1.13.0", "integrity": "sha512-Ld2nUOlwW1nmYDA2Q/5o7SC8WcCzVS7XjImmzW4a4z1o8DXJnt+2xYLvI42N5UYlNb/EevPahdC/XxIP6C38TQ==", "command": "sherif"},
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sanitize(value: str) -> str:
    replacements = [
        (str(TOOL_ROOT), "<D_TOOLCHAIN>"),
        (str(ROOT), "<R3_WORKTREE>"),
        (str(Path.home()), "<USER_HOME>"),
        (str(Path(sys.executable).parent), "<SYSTEM_PYTHON_DIR>"),
        (str(node_executable().parent) if "node_executable" in globals() else "", "<NODE_RUNTIME>"),
        (os.environ.get("SystemRoot", ""), "<WINDOWS_ROOT>"),
        (str(TOOL_ROOT).replace("/", "\\"), "<D_TOOLCHAIN>"),
        (str(ROOT).replace("/", "\\"), "<R3_WORKTREE>"),
        (str(Path.home()).replace("/", "\\"), "<USER_HOME>"),
    ]
    result = value
    for raw, label in replacements:
        if raw:
            variants = {raw, raw.replace("\\", "\\\\"), raw.replace("/", "\\"), raw.replace("/", "\\\\")}
            for variant in sorted(variants, key=len, reverse=True):
                result = re.sub(
                    re.escape(variant),
                    lambda _match, replacement=label: replacement,
                    result,
                    flags=re.I,
                )
    # Some tools render configuration paths with doubled backslashes and may
    # mention profile-local files outside the known execution roots.  Scrub any
    # remaining drive-qualified path rather than attempting to enumerate every
    # third-party rendering convention.  The negative look-behind prevents URL
    # scheme fragments inside ordinary web URLs from being misclassified.
    result = re.sub(
        r"(?<![A-Za-z])[A-Z]:[\\/]+[^\r\n'\"]*",
        "<ABSOLUTE_WINDOWS_PATH>",
        result,
        flags=re.I,
    )
    return result


def sanitize_payload(value: Any) -> Any:
    if isinstance(value, str):
        return sanitize(value)
    if isinstance(value, list):
        return [sanitize_payload(item) for item in value]
    if isinstance(value, dict):
        return {key: sanitize_payload(item) for key, item in value.items()}
    return value


def base_env() -> dict[str, str]:
    env = os.environ.copy()
    cache = TOOL_ROOT / "cache"
    temp = TOOL_ROOT / "temp"
    cache.mkdir(parents=True, exist_ok=True)
    temp.mkdir(parents=True, exist_ok=True)
    env.update(
        {
            "PIP_CACHE_DIR": str(cache / "pip"),
            "npm_config_cache": str(cache / "npm"),
            "PIP_DISABLE_PIP_VERSION_CHECK": "1",
            "PIP_NO_INPUT": "1",
            "TEMP": str(temp),
            "TMP": str(temp),
            "CI": "1",
        }
    )
    return env


def run(command: list[str], *, cwd: Path | None = None, timeout: int = 300, allow_failure: bool = False) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        env=base_env(),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    record = {
        "command": [sanitize(str(token)) for token in command],
        "cwd": sanitize(str(cwd)) if cwd else None,
        "returncode": completed.returncode,
        "stdout": sanitize(completed.stdout[-12000:]),
        "stderr": sanitize(completed.stderr[-12000:]),
    }
    if completed.returncode and not allow_failure:
        raise RuntimeError(json.dumps(record, sort_keys=True))
    return record


def write_receipt(payload: dict[str, Any]) -> None:
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def python_executable(venv: Path) -> Path:
    return venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def cli_path(directory: Path, name: str) -> Path:
    suffix = ".exe" if os.name == "nt" else ""
    candidate = directory / f"{name}{suffix}"
    if candidate.exists():
        return candidate
    command_candidate = directory / f"{name}.cmd"
    if command_candidate.exists():
        return command_candidate
    return candidate


def windows_shim_command(executable: Path, *arguments: str) -> list[str]:
    if os.name == "nt" and executable.suffix.lower() in {".cmd", ".bat"}:
        command_line = subprocess.list2cmdline([str(executable), *arguments])
        return [os.environ.get("ComSpec", "cmd.exe"), "/d", "/s", "/c", command_line]
    return [str(executable), *arguments]


def node_executable() -> Path:
    resolved = shutil.which("node.exe") or shutil.which("node")
    if not resolved:
        raise RuntimeError("node executable is unavailable")
    return Path(resolved)


def npm_command(*arguments: str) -> list[str]:
    npm_shim = shutil.which("npm.cmd") or shutil.which("npm")
    if not npm_shim:
        raise RuntimeError("npm installation is unavailable")
    npm_cli = Path(npm_shim).parent / "node_modules" / "npm" / "bin" / "npm-cli.js"
    if not npm_cli.is_file():
        raise RuntimeError("npm-cli.js is unavailable")
    return [str(node_executable()), str(npm_cli), *arguments]


def node_tool_command(node_root: Path, tool: dict[str, str], *arguments: str) -> list[str]:
    package_root = node_root / "node_modules" / tool["name"]
    package = json.loads((package_root / "package.json").read_text(encoding="utf-8"))
    bin_value = package.get("bin")
    if isinstance(bin_value, dict):
        relative = bin_value.get(tool["command"])
    else:
        relative = bin_value
    if not isinstance(relative, str):
        raise RuntimeError(f"declared bin missing for {tool['name']}:{tool['command']}")
    script = package_root / relative
    if not script.is_file():
        raise RuntimeError(f"declared bin file missing for {tool['name']}: {relative}")
    return [str(node_executable()), str(script), *arguments]


def audit_python(system_python: str, site_packages: Path) -> dict[str, Any]:
    audit = run(
        [
            system_python,
            "-m",
            "pip_audit",
            "--path",
            str(site_packages),
            "--format",
            "json",
            "--progress-spinner",
            "off",
            "--timeout",
            "20",
        ],
        timeout=300,
        allow_failure=True,
    )
    parsed: Any = None
    try:
        parsed = json.loads(audit["stdout"])
    except json.JSONDecodeError:
        pass
    audit["parsed"] = parsed
    if isinstance(parsed, dict):
        dependencies = parsed.get("dependencies", [])
        vulnerabilities = sum(len(row.get("vulns", [])) for row in dependencies if isinstance(row, dict))
    elif isinstance(parsed, list):
        vulnerabilities = sum(len(row.get("vulns", [])) for row in parsed if isinstance(row, dict))
    else:
        vulnerabilities = None
    audit["known_vulnerability_count"] = vulnerabilities
    audit["bounded_registry_audit_only"] = True
    return audit


def execute() -> dict[str, Any]:
    if TOOL_ROOT.exists():
        raise RuntimeError(f"fresh transaction root already exists: {TOOL_ROOT}")
    TOOL_ROOT.mkdir(parents=True)
    head = run(["git", "-C", str(ROOT), "rev-parse", "HEAD"])["stdout"].strip()
    if head != X1_HEAD:
        raise RuntimeError(f"x1 head mismatch: {head}")
    started = now()
    receipt: dict[str, Any] = {
        "state": "RUNNING",
        "started_at": started,
        "x1_head": X1_HEAD,
        "transaction_root": "D_ISOLATED_TOOLCHAIN",
        "global_or_system_install": False,
        "C_drive_download": False,
        "python_direct_tools": PYTHON_TOOLS,
        "node_direct_tools": NODE_TOOLS,
        "commands": [],
        "operational_failures": [
            {
                "failure_id": "R3-X2-F001",
                "description": "plan-update wrapper emitted a ReferenceError after the plan mutation",
                "recovery": "the plan tool result was inspected separately; no plan mutation was replayed",
                "credit": 0,
            },
            {
                "failure_id": "R3-X2-F002",
                "description": "pip-audit executable was absent from PATH",
                "recovery": "the installed Python module surface was used without adding a fourteenth direct tool",
                "credit": 0,
            },
            {
                "failure_id": "R3-X2-F003",
                "description": "first transaction preflight created cache and temp before checking root freshness",
                "recovery": "the empty two-directory root was preserved under the failed-transaction bank and freshness moved ahead of all environment creation",
                "credit": 0,
            },
        ],
    }
    try:
        python_root = TOOL_ROOT / "python"
        venv = python_root / "venv"
        wheelhouse = python_root / "wheelhouse"
        wheelhouse.mkdir(parents=True)
        receipt["commands"].append(run([sys.executable, "-m", "venv", str(venv)], timeout=180))
        vpython = python_executable(venv)
        specs = [f"{row['name']}=={row['version']}" for row in PYTHON_TOOLS]
        receipt["commands"].append(
            run(
                [str(vpython), "-m", "pip", "download", "--only-binary=:all:", "--dest", str(wheelhouse), *specs],
                timeout=600,
            )
        )
        wheel_records = [
            {"filename": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in sorted(wheelhouse.glob("*.whl"))
        ]
        wheel_by_name = {row["filename"]: row for row in wheel_records}
        direct_hash_checks = []
        for tool in PYTHON_TOOLS:
            observed = wheel_by_name.get(tool["wheel"])
            direct_hash_checks.append(
                {
                    "name": tool["name"],
                    "filename": tool["wheel"],
                    "expected_sha256": tool["sha256"],
                    "observed_sha256": observed["sha256"] if observed else None,
                    "matches": bool(observed and observed["sha256"] == tool["sha256"]),
                }
            )
        if not all(row["matches"] for row in direct_hash_checks):
            raise RuntimeError(f"direct wheel hash mismatch: {direct_hash_checks}")
        receipt["commands"].append(
            run(
                [str(vpython), "-m", "pip", "install", "--no-index", "--find-links", str(wheelhouse), *specs],
                timeout=600,
            )
        )
        pip_check = run([str(vpython), "-m", "pip", "check"])
        pip_list = run([str(vpython), "-m", "pip", "list", "--format", "json"])
        packages = json.loads(pip_list["stdout"])
        site_packages_raw = run(
            [str(vpython), "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"]
        )["stdout"].strip()
        python_audit = audit_python(sys.executable, Path(site_packages_raw))
        scripts_dir = venv / ("Scripts" if os.name == "nt" else "bin")
        python_smokes = []
        for tool in PYTHON_TOOLS:
            executable = cli_path(scripts_dir, tool["command"])
            positive = run([str(executable), "--help"], timeout=90, allow_failure=True)
            negative = run([str(executable), "--ghc-intentionally-invalid-option"], timeout=90, allow_failure=True)
            python_smokes.append(
                {
                    "name": tool["name"],
                    "positive": positive,
                    "positive_passed": positive["returncode"] == 0,
                    "negative": negative,
                    "negative_rejected": negative["returncode"] != 0,
                }
            )
        node_root = TOOL_ROOT / "node"
        node_root.mkdir()
        package_json = {
            "name": "ghc-family-neris-v667-v8-r3-toolchain",
            "version": "0.0.0",
            "private": True,
            "description": "D-isolated bounded tool transaction; never publish",
            "devDependencies": {row["name"]: row["version"] for row in NODE_TOOLS},
        }
        (node_root / "package.json").write_text(json.dumps(package_json, indent=2) + "\n", encoding="utf-8", newline="\n")
        receipt["commands"].append(
            run(
                npm_command("install", "--package-lock-only", "--ignore-scripts", "--no-audit", "--no-fund"),
                cwd=node_root,
                timeout=600,
            )
        )
        package_lock = json.loads((node_root / "package-lock.json").read_text(encoding="utf-8"))
        node_integrity_checks = []
        for tool in NODE_TOOLS:
            entry = package_lock.get("packages", {}).get(f"node_modules/{tool['name']}", {})
            node_integrity_checks.append(
                {
                    "name": tool["name"],
                    "expected_version": tool["version"],
                    "observed_version": entry.get("version"),
                    "expected_integrity": tool["integrity"],
                    "observed_integrity": entry.get("integrity"),
                    "matches": entry.get("version") == tool["version"] and entry.get("integrity") == tool["integrity"],
                }
            )
        if not all(row["matches"] for row in node_integrity_checks):
            raise RuntimeError(f"node lock integrity mismatch: {node_integrity_checks}")
        receipt["commands"].append(
            run(npm_command("ci", "--ignore-scripts", "--no-audit", "--no-fund"), cwd=node_root, timeout=600)
        )
        npm_ls = run(npm_command("ls", "--depth=0", "--json"), cwd=node_root, allow_failure=True)
        npm_audit = run(npm_command("audit", "--json"), cwd=node_root, timeout=300, allow_failure=True)
        try:
            npm_audit_json = json.loads(npm_audit["stdout"])
        except json.JSONDecodeError:
            npm_audit_json = None
        if isinstance(npm_audit_json, dict):
            npm_vulnerability_count = sum(
                int(value)
                for value in npm_audit_json.get("metadata", {}).get("vulnerabilities", {}).values()
                if isinstance(value, int)
            )
        else:
            npm_vulnerability_count = None
        bin_dir = node_root / "node_modules" / ".bin"
        node_smokes = []
        for tool in NODE_TOOLS:
            positive = run(node_tool_command(node_root, tool, "--help"), cwd=node_root, timeout=90, allow_failure=True)
            negative = run(node_tool_command(node_root, tool, "--ghc-intentionally-invalid-option"), cwd=node_root, timeout=90, allow_failure=True)
            node_smokes.append(
                {
                    "name": tool["name"],
                    "positive": positive,
                    "positive_passed": positive["returncode"] == 0,
                    "negative": negative,
                    "negative_rejected": negative["returncode"] != 0,
                }
            )
        receipt.update(
            {
                "state": "PASS" if all(row["positive_passed"] and row["negative_rejected"] for row in python_smokes + node_smokes) else "FAIL_SMOKE",
                "finished_at": now(),
                "direct_tool_count": len(PYTHON_TOOLS) + len(NODE_TOOLS),
                "python_direct_count": len(PYTHON_TOOLS),
                "node_direct_count": len(NODE_TOOLS),
                "wheel_count": len(wheel_records),
                "wheel_records": wheel_records,
                "direct_wheel_hash_checks": direct_hash_checks,
                "top_level_hashes_valid": all(row["matches"] for row in direct_hash_checks),
                "pip_check": pip_check,
                "python_packages": packages,
                "python_audit": python_audit,
                "node_lock_sha256": sha256(node_root / "package-lock.json"),
                "node_integrity_checks": node_integrity_checks,
                "node_integrities_valid": all(row["matches"] for row in node_integrity_checks),
                "npm_ls": npm_ls,
                "npm_audit": npm_audit,
                "npm_audit_parsed": npm_audit_json,
                "npm_known_vulnerability_count": npm_vulnerability_count,
                "python_smokes": python_smokes,
                "node_smokes": node_smokes,
                "positive_smoke_count": sum(row["positive_passed"] for row in python_smokes + node_smokes),
                "negative_rejection_count": sum(row["negative_rejected"] for row in python_smokes + node_smokes),
                "install_scripts_disabled": True,
                "publication_count": 0,
                "global_install_count": 0,
                "successful_transaction_replay_count": 0,
                "bounded_registry_audit_not_exhaustive_security": True,
            }
        )
        write_receipt(receipt)
        return receipt
    except Exception as exc:
        receipt.update({"state": "FAIL", "finished_at": now(), "error": sanitize(str(exc))})
        write_receipt(receipt)
        raise


def resume_node() -> dict[str, Any]:
    if not RECEIPT_PATH.is_file():
        raise RuntimeError("failed transaction receipt is missing")
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    if receipt.get("state") != "FAIL" or "WinError 2" not in receipt.get("error", ""):
        raise RuntimeError("receipt is not the exact resumable Windows shim failure")
    if not TOOL_ROOT.is_dir():
        raise RuntimeError("tool root is missing")
    python_root = TOOL_ROOT / "python"
    venv = python_root / "venv"
    wheelhouse = python_root / "wheelhouse"
    node_root = TOOL_ROOT / "node"
    if not python_executable(venv).is_file() or not node_root.joinpath("package.json").is_file():
        raise RuntimeError("expected completed Python and prepared Node state is absent")
    if node_root.joinpath("package-lock.json").exists() or node_root.joinpath("node_modules").exists():
        raise RuntimeError("Node state advanced beyond exact resume boundary")
    existing_failure_ids = {row.get("failure_id") for row in receipt.setdefault("operational_failures", [])}
    recovery_failures = [
        {
            "failure_id": "R3-X2-F004",
            "description": "direct Windows CreateProcess could not execute the npm.cmd shim",
            "recovery": "resume from the unstarted Node lock step through an explicit cmd.exe wrapper; do not redownload or reinstall Python",
            "credit": 0,
        },
        {
            "failure_id": "R3-X2-F005",
            "description": "first explicit cmd.exe wrapper split the npm.cmd path at Program Files",
            "recovery": "construct one quoted Windows command line with subprocess.list2cmdline before the unstarted Node lock step",
            "credit": 0,
        },
        {
            "failure_id": "R3-X2-F006",
            "description": "quoted cmd.exe shim probe passed embedded quotes literally and still rejected npm.cmd",
            "recovery": "close the shell-shim route and execute node.exe with npm-cli.js and package-declared bin scripts directly",
            "credit": 0,
        },
    ]
    receipt["operational_failures"].extend(row for row in recovery_failures if row["failure_id"] not in existing_failure_ids)
    receipt["initial_failure"] = {"state": receipt["state"], "error": receipt.get("error"), "finished_at": receipt.get("finished_at")}
    receipt["state"] = "RESUMING_NODE"
    receipt["resumed_at"] = now()
    receipt["python_download_replay_count"] = 0
    receipt["python_install_replay_count"] = 0
    receipt["node_resume_count"] = 1
    receipt["error"] = None
    vpython = python_executable(venv)
    wheel_records = [
        {"filename": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
        for path in sorted(wheelhouse.glob("*.whl"))
    ]
    wheel_by_name = {row["filename"]: row for row in wheel_records}
    direct_hash_checks = []
    for tool in PYTHON_TOOLS:
        observed = wheel_by_name.get(tool["wheel"])
        direct_hash_checks.append(
            {
                "name": tool["name"],
                "filename": tool["wheel"],
                "expected_sha256": tool["sha256"],
                "observed_sha256": observed["sha256"] if observed else None,
                "matches": bool(observed and observed["sha256"] == tool["sha256"]),
            }
        )
    if not all(row["matches"] for row in direct_hash_checks):
        raise RuntimeError("Python direct-wheel state changed before resume")
    pip_check = run([str(vpython), "-m", "pip", "check"])
    pip_list = run([str(vpython), "-m", "pip", "list", "--format", "json"])
    packages = json.loads(pip_list["stdout"])
    site_packages_raw = run(
        [str(vpython), "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"]
    )["stdout"].strip()
    python_audit = audit_python(sys.executable, Path(site_packages_raw))
    scripts_dir = venv / ("Scripts" if os.name == "nt" else "bin")
    python_smokes = []
    for tool in PYTHON_TOOLS:
        executable = cli_path(scripts_dir, tool["command"])
        positive = run([str(executable), "--help"], timeout=90, allow_failure=True)
        negative = run([str(executable), "--ghc-intentionally-invalid-option"], timeout=90, allow_failure=True)
        python_smokes.append(
            {
                "name": tool["name"],
                "positive": positive,
                "positive_passed": positive["returncode"] == 0,
                "negative": negative,
                "negative_rejected": negative["returncode"] != 0,
            }
        )
    receipt.setdefault("commands", []).append(
        run(
            npm_command("install", "--package-lock-only", "--ignore-scripts", "--no-audit", "--no-fund"),
            cwd=node_root,
            timeout=600,
        )
    )
    package_lock_path = node_root / "package-lock.json"
    package_lock = json.loads(package_lock_path.read_text(encoding="utf-8"))
    node_integrity_checks = []
    for tool in NODE_TOOLS:
        entry = package_lock.get("packages", {}).get(f"node_modules/{tool['name']}", {})
        node_integrity_checks.append(
            {
                "name": tool["name"],
                "expected_version": tool["version"],
                "observed_version": entry.get("version"),
                "expected_integrity": tool["integrity"],
                "observed_integrity": entry.get("integrity"),
                "matches": entry.get("version") == tool["version"] and entry.get("integrity") == tool["integrity"],
            }
        )
    if not all(row["matches"] for row in node_integrity_checks):
        raise RuntimeError(f"node lock integrity mismatch: {node_integrity_checks}")
    receipt["commands"].append(
        run(
            npm_command("ci", "--ignore-scripts", "--no-audit", "--no-fund"),
            cwd=node_root,
            timeout=600,
        )
    )
    npm_ls = run(npm_command("ls", "--depth=0", "--json"), cwd=node_root, allow_failure=True)
    npm_audit = run(npm_command("audit", "--json"), cwd=node_root, timeout=300, allow_failure=True)
    try:
        npm_audit_json = json.loads(npm_audit["stdout"])
    except json.JSONDecodeError:
        npm_audit_json = None
    if isinstance(npm_audit_json, dict):
        npm_vulnerability_count = sum(
            int(value)
            for value in npm_audit_json.get("metadata", {}).get("vulnerabilities", {}).values()
            if isinstance(value, int)
        )
    else:
        npm_vulnerability_count = None
    bin_dir = node_root / "node_modules" / ".bin"
    node_smokes = []
    for tool in NODE_TOOLS:
        positive = run(node_tool_command(node_root, tool, "--help"), cwd=node_root, timeout=90, allow_failure=True)
        negative = run(node_tool_command(node_root, tool, "--ghc-intentionally-invalid-option"), cwd=node_root, timeout=90, allow_failure=True)
        node_smokes.append(
            {
                "name": tool["name"],
                "positive": positive,
                "positive_passed": positive["returncode"] == 0,
                "negative": negative,
                "negative_rejected": negative["returncode"] != 0,
            }
        )
    all_smokes = python_smokes + node_smokes
    receipt.update(
        {
            "state": "PASS_BOUNDED_NODE_RESUME_WITH_RETAINED_FAILURES" if all(row["positive_passed"] and row["negative_rejected"] for row in all_smokes) else "FAIL_SMOKE",
            "finished_at": now(),
            "direct_tool_count": 13,
            "python_direct_count": 8,
            "node_direct_count": 5,
            "wheel_count": len(wheel_records),
            "wheel_records": wheel_records,
            "direct_wheel_hash_checks": direct_hash_checks,
            "top_level_hashes_valid": all(row["matches"] for row in direct_hash_checks),
            "pip_check": pip_check,
            "python_packages": packages,
            "python_audit": python_audit,
            "node_lock_sha256": sha256(package_lock_path),
            "node_integrity_checks": node_integrity_checks,
            "node_integrities_valid": all(row["matches"] for row in node_integrity_checks),
            "npm_ls": npm_ls,
            "npm_audit": npm_audit,
            "npm_audit_parsed": npm_audit_json,
            "npm_known_vulnerability_count": npm_vulnerability_count,
            "python_smokes": python_smokes,
            "node_smokes": node_smokes,
            "positive_smoke_count": sum(row["positive_passed"] for row in all_smokes),
            "negative_rejection_count": sum(row["negative_rejected"] for row in all_smokes),
            "install_scripts_disabled": True,
            "publication_count": 0,
            "global_install_count": 0,
            "successful_transaction_replay_count": 0,
            "bounded_registry_audit_not_exhaustive_security": True,
        }
    )
    write_receipt(receipt)
    return receipt


def recover_package_json_negative() -> dict[str, Any]:
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    if receipt.get("state") != "FAIL_SMOKE":
        raise RuntimeError("receipt is not the exact failed-smoke state")
    failed = [
        row["name"]
        for row in receipt.get("python_smokes", []) + receipt.get("node_smokes", [])
        if not row.get("positive_passed") or not row.get("negative_rejected")
    ]
    if failed != ["package-json-validator-cli"]:
        raise RuntimeError(f"unexpected failed smoke set: {failed}")
    node_root = TOOL_ROOT / "node"
    fixture_root = TOOL_ROOT / "fixtures" / "package-json-validator-invalid"
    fixture_root.mkdir(parents=True, exist_ok=True)
    fixture = fixture_root / "package.json"
    fixture.write_text(
        json.dumps({"name": "INVALID NAME WITH SPACES", "version": "not-semver", "private": "not-a-boolean"}, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    tool = next(row for row in NODE_TOOLS if row["name"] == "package-json-validator-cli")
    recovery = run(
        node_tool_command(node_root, tool, "--filename", str(fixture)),
        cwd=node_root,
        timeout=90,
        allow_failure=True,
    )
    if recovery["returncode"] == 0:
        raise RuntimeError("malformed package.json was not rejected")
    for row in receipt["node_smokes"]:
        if row["name"] == tool["name"]:
            row["generic_negative_retained"] = row["negative"]
            row["generic_negative_rejected"] = row["negative_rejected"]
            row["negative"] = recovery
            row["negative_rejected"] = True
            row["negative_fixture"] = "D_ISOLATED_MALFORMED_PACKAGE_JSON"
    existing_failure_ids = {row.get("failure_id") for row in receipt.setdefault("operational_failures", [])}
    additions = [
        {
            "failure_id": "R3-X2-F007",
            "description": "package-json-validator-cli ignored the generic unknown option and validated the default valid package",
            "recovery": "run only that tool against a malformed package through its documented filename option",
            "credit": 0,
        },
        {
            "failure_id": "R3-X2-F008",
            "description": "PowerShell npm reported 12.0.2 while the shell-free npm-cli.js used by the transaction reported 11.16.0",
            "recovery": "record the exact executable pair and used npm-cli version; do not conflate wrapper and direct surfaces",
            "credit": 0,
        },
        {
            "failure_id": "R3-X2-F009",
            "description": "license-checker-rseidelsohn help banner reported 4.4.2 while lockfile package metadata and integrity identify 5.0.1",
            "recovery": "retain the stale internal banner and credit version identity only from exact lock and package metadata",
            "credit": 0,
        },
    ]
    receipt["operational_failures"].extend(row for row in additions if row["failure_id"] not in existing_failure_ids)
    all_smokes = receipt["python_smokes"] + receipt["node_smokes"]
    receipt["negative_rejection_count"] = sum(row["negative_rejected"] for row in all_smokes)
    receipt["positive_smoke_count"] = sum(row["positive_passed"] for row in all_smokes)
    receipt["isolated_smoke_recovery_count"] = 1
    receipt["successful_transaction_replay_count"] = 0
    receipt["used_npm_cli_version"] = "11.16.0"
    receipt["powershell_wrapper_npm_version_advisory"] = "12.0.2"
    receipt["license_checker_internal_banner_advisory"] = "4.4.2"
    receipt["state"] = "PASS_BOUNDED_NODE_RESUME_AND_ISOLATED_SMOKE_RECOVERY_WITH_RETAINED_FAILURES"
    receipt["finished_at"] = now()
    write_receipt(receipt)
    return receipt


def sanitize_durable_receipt() -> dict[str, Any]:
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    if not str(receipt.get("state", "")).startswith("PASS"):
        raise RuntimeError("only the passing bounded receipt can be sanitized")
    failure_ids = {row.get("failure_id") for row in receipt.setdefault("operational_failures", [])}
    privacy_failures = [
        {
            "failure_id": "R3-X2-F010",
            "description": "the first broad drive-path scan matched URL scheme fragments and therefore produced false positives",
            "recovery": "a case-sensitive PCRE2 scan with an alphabetic negative look-behind separated URL fragments from Windows drive paths",
            "credit": 0,
        },
        {
            "failure_id": "R3-X2-F011",
            "description": "the targeted scan found a doubled-backslash user-profile path in retained tox help output",
            "recovery": "the durable-only sanitizer now handles escaped known roots and scrubs every remaining drive-qualified path; no tool execution or installation was replayed",
            "credit": 0,
        },
    ]
    receipt["operational_failures"].extend(
        row for row in privacy_failures if row["failure_id"] not in failure_ids
    )
    cleaned = sanitize_payload(receipt)
    cleaned["durable_path_sanitization"] = {
        "state": "completed",
        "private_absolute_paths_retained": False,
        "operational_toolchain_mutated": False,
        "evidence_values_other_than_path_labels_mutated": False,
    }
    write_receipt(cleaned)
    return cleaned


def validate_receipt() -> dict[str, Any]:
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    if not receipt["state"].startswith("PASS"):
        raise AssertionError(f"tool transaction not PASS: {receipt['state']}")
    if receipt["direct_tool_count"] != 13:
        raise AssertionError("direct tool count mismatch")
    if not receipt["top_level_hashes_valid"] or not receipt["node_integrities_valid"]:
        raise AssertionError("integrity mismatch")
    if receipt["positive_smoke_count"] != 13 or receipt["negative_rejection_count"] != 13:
        raise AssertionError("smoke mismatch")
    if receipt["global_install_count"] or receipt["publication_count"]:
        raise AssertionError("external mutation mismatch")
    return {
        "status": "PASS",
        "direct_tools": receipt["direct_tool_count"],
        "positive_smokes": receipt["positive_smoke_count"],
        "negative_rejections": receipt["negative_rejection_count"],
        "wheel_count": receipt["wheel_count"],
        "python_known_vulnerabilities": receipt["python_audit"]["known_vulnerability_count"],
        "npm_known_vulnerabilities": receipt["npm_known_vulnerability_count"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--resume-node", action="store_true")
    parser.add_argument("--recover-package-json-negative", action="store_true")
    parser.add_argument("--sanitize-receipt", action="store_true")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    if sum((args.execute, args.resume_node, args.recover_package_json_negative, args.sanitize_receipt, args.validate)) != 1:
        parser.error("choose exactly one transaction, resume, isolated recovery, or validation mode")
    payload = (
        execute()
        if args.execute
        else resume_node()
        if args.resume_node
        else recover_package_json_negative()
        if args.recover_package_json_negative
        else sanitize_durable_receipt()
        if args.sanitize_receipt
        else validate_receipt()
    )
    print(json.dumps(payload if args.validate else {
        "state": payload["state"],
        "direct_tool_count": payload.get("direct_tool_count"),
        "positive_smoke_count": payload.get("positive_smoke_count"),
        "negative_rejection_count": payload.get("negative_rejection_count"),
        "wheel_count": payload.get("wheel_count"),
        "python_known_vulnerabilities": payload.get("python_audit", {}).get("known_vulnerability_count"),
        "npm_known_vulnerabilities": payload.get("npm_known_vulnerability_count"),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
