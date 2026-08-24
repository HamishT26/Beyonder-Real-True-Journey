#!/usr/bin/env python3
"""Run replay-guarded synthetic smokes for the Neris v667-v8-r2 tool set."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "neris-solane" / "v667-v8-r2"
D_ROOT = Path("D:/GHC-Archives")
CACHE_ROOT = D_ROOT / "tool-caches" / "neris-v667-v8-r2"
TEMP_ROOT = D_ROOT / "phase-temp" / "neris-v667-v8-r2" / "smokes"
PY_CORE = D_ROOT / "global-tools" / "python" / "neris-v667-v8-r2" / "core" / "Scripts"
PY_INSPECT = D_ROOT / "global-tools" / "python" / "neris-v667-v8-r2" / "wheel-inspect" / "Scripts"
NODE_BIN = D_ROOT / "global-tools" / "node" / "neris-v667-v8-r2" / "node_modules" / ".bin"
NODE_ENV = D_ROOT / "global-tools" / "node" / "neris-v667-v8-r2"
WHEEL_CORE = CACHE_ROOT / "wheels" / "core"
WHEEL_INSPECT = CACHE_ROOT / "wheels" / "wheel-inspect"

TOOLS = [
    "check-wheel-contents",
    "wheel-inspect",
    "pydistcheck",
    "import-linter",
    "pydoclint",
    "interrogate",
    "pytest-timeout",
    "spdx-tools",
    "publint",
    "arethetypeswrong",
    "npm-package-json-lint",
    "lockfile-lint",
    "syncpack",
]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def scrub(value: str) -> str:
    result = value
    for path, alias in (
        (str(D_ROOT), "<D_GHC_ARCHIVES>"),
        (str(ROOT), "<NERIS_OWNER_WORKTREE>"),
    ):
        result = result.replace(path, alias).replace(path.replace("\\", "/"), alias)
    return result[-3000:]


def run(argv: list[str], *, cwd: Path | None = None, timeout: int = 120) -> dict[str, Any]:
    env = os.environ.copy()
    env["NO_COLOR"] = "1"
    env["FORCE_COLOR"] = "0"
    env["npm_config_cache"] = str(D_ROOT / "tool-caches" / "npm-cache")
    labels = [Path(part).name if (":" in part or "\\" in part or "/" in part) else part for part in argv]
    try:
        completed = subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
        return {
            "argv_label": labels,
            "returncode": completed.returncode,
            "stdout_tail": scrub(completed.stdout),
            "stderr_tail": scrub(completed.stderr),
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode("utf-8", errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode("utf-8", errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        return {
            "argv_label": labels,
            "returncode": 124,
            "stdout_tail": scrub(stdout),
            "stderr_tail": scrub(stderr),
            "timed_out": True,
        }


def wheel(directory: Path, prefix: str) -> Path:
    matches = sorted(directory.glob(prefix + "*.whl"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one wheel for {prefix}; observed {len(matches)}")
    return matches[0]


def python_fixture(attempt: Path, documented: bool = True) -> Path:
    target = attempt / ("documented.py" if documented else "undocumented.py")
    if documented:
        text = '''"""Synthetic documented module."""

def add(left: int, right: int) -> int:
    """Add two integers.

    Parameters
    ----------
    left : int
        First value.
    right : int
        Second value.

    Returns
    -------
    int
        Sum of the values.
    """
    return left + right
'''
    else:
        text = "def add(left: int, right: int) -> int:\n    return left + right\n"
    write_text(target, text)
    return target


def package_fixture(path: Path, *, valid: bool) -> None:
    package = {
        "name": "neris-synthetic-package" if valid else "neris-synthetic-broken-package",
        "version": "1.0.0",
        "type": "module",
        "main": "./index.js" if valid else "./missing.js",
        "types": "./index.d.ts" if valid else "./missing.d.ts",
        "exports": {".": {"types": "./index.d.ts", "import": "./index.js"}} if valid else {".": "./missing.js"},
        "files": ["index.js", "index.d.ts"],
        "license": "MIT",
    }
    write_text(path / "package.json", json.dumps(package, ensure_ascii=False, indent=2, sort_keys=False))
    write_text(path / "index.js", "export const value = 1;")
    write_text(path / "index.d.ts", "export declare const value: number;")


def pack_package(path: Path) -> tuple[Path | None, dict[str, Any]]:
    npm = shutil.which("npm")
    if npm is None:
        raise RuntimeError("npm unavailable")
    receipt = run([npm, "pack", "--ignore-scripts", "--json"], cwd=path, timeout=120)
    if receipt["returncode"] != 0:
        return None, receipt
    payload = json.loads(receipt["stdout_tail"])
    if isinstance(payload, list):
        filename = payload[0]["filename"]
    elif isinstance(payload, dict) and len(payload) == 1:
        filename = next(iter(payload.values()))["filename"]
    else:
        raise RuntimeError("unrecognized npm pack JSON shape")
    return path / filename, receipt


def commands_for(tool: str, attempt: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    setup: list[dict[str, Any]] = []
    if tool == "check-wheel-contents":
        target = wheel(WHEEL_CORE, "check_wheel_contents-0.6.3-")
        exe = PY_CORE / "check-wheel-contents.exe"
        return run([str(exe), "--no-config", str(target)]), run([str(exe), "--no-config", "--toplevel", "absent_surface", str(target)]), setup
    if tool == "wheel-inspect":
        target = wheel(WHEEL_INSPECT, "wheel_inspect-1.8.0-")
        exe = PY_INSPECT / "wheel2json.exe"
        return run([str(exe), str(target)]), run([str(exe), str(attempt / "absent-1.0-py3-none-any.whl")]), setup
    if tool == "pydistcheck":
        target = wheel(WHEEL_CORE, "pydistcheck-0.11.3-")
        exe = PY_CORE / "pydistcheck.exe"
        return run([str(exe), str(target)]), run([str(exe), "--max-allowed-files", "0", str(target)]), setup
    if tool == "import-linter":
        good = attempt / "good"
        bad = attempt / "bad"
        for root, forbidden in ((good, False), (bad, True)):
            write_text(root / "layered" / "__init__.py", '"""Synthetic layered package."""')
            write_text(root / "layered" / "high.py", "from layered import low\nVALUE = low.VALUE")
            write_text(root / "layered" / "low.py", "from layered import high\nVALUE = 1" if forbidden else "VALUE = 1")
            write_text(
                root / ".importlinter",
                """[importlinter]
root_package = layered

[importlinter:contract:layers]
name = Synthetic layers
type = layers
layers =
    layered.high
    layered.low
""",
            )
        exe = PY_CORE / "lint-imports.exe"
        return run([str(exe), "--config", str(good / ".importlinter"), "--no-cache"], cwd=good), run([str(exe), "--config", str(bad / ".importlinter"), "--no-cache"], cwd=bad), setup
    if tool == "pydoclint":
        good = python_fixture(attempt, True)
        bad = python_fixture(attempt, False)
        write_text(
            bad,
            '''def add(left: int, right: int) -> int:
    """Add two integers.

    Parameters
    ----------
    left : int
        First value.
    absent : int
        Deliberately mismatched value.

    Returns
    -------
    str
        Deliberately mismatched return type.
    """
    return left + right
''',
        )
        exe = PY_CORE / "pydoclint.exe"
        args = ["--style", "numpy", "--skip-checking-short-docstrings", "false"]
        return run([str(exe), *args, str(good)]), run([str(exe), *args, str(bad)]), setup
    if tool == "interrogate":
        good = python_fixture(attempt, True)
        bad = python_fixture(attempt, False)
        exe = PY_CORE / "interrogate.exe"
        return run([str(exe), "--no-color", "--fail-under", "100", str(good)]), run([str(exe), "--no-color", "--fail-under", "100", str(bad)]), setup
    if tool == "pytest-timeout":
        good = attempt / "test_fast.py"
        bad = attempt / "test_slow.py"
        write_text(good, "def test_fast():\n    assert 2 + 2 == 4")
        write_text(bad, "import time\n\ndef test_slow():\n    time.sleep(1)")
        exe = PY_CORE / "python.exe"
        return run([str(exe), "-m", "pytest", "-q", "--timeout=1", str(good)]), run([str(exe), "-m", "pytest", "-q", "--timeout=0.05", str(bad)]), setup
    if tool == "spdx-tools":
        good = attempt / "valid.spdx.json"
        bad = attempt / "invalid.spdx.json"
        payload = {
            "spdxVersion": "SPDX-2.3",
            "dataLicense": "CC0-1.0",
            "SPDXID": "SPDXRef-DOCUMENT",
            "name": "Neris synthetic package fixture",
            "documentNamespace": "https://example.invalid/spdx/neris-synthetic-package-fixture-1",
            "creationInfo": {"created": "2026-08-24T00:00:00Z", "creators": ["Tool: Neris synthetic fixture"]},
            "packages": [{
                "name": "neris-synthetic-package",
                "SPDXID": "SPDXRef-Package",
                "downloadLocation": "NOASSERTION",
                "filesAnalyzed": False,
                "licenseConcluded": "NOASSERTION",
                "licenseDeclared": "MIT",
                "copyrightText": "NOASSERTION",
            }],
        }
        write_json(good, payload)
        broken = dict(payload)
        broken.pop("dataLicense")
        write_json(bad, broken)
        exe = PY_CORE / "pyspdxtools.exe"
        return run([str(exe), "--infile", str(good)]), run([str(exe), "--infile", str(bad)]), setup
    if tool == "publint":
        good = attempt / "good"
        bad = attempt / "bad"
        package_fixture(good, valid=True)
        package_fixture(bad, valid=False)
        exe = NODE_BIN / "publint.cmd"
        return run([str(exe), "run", str(good), "--pack", "false", "--level", "error"], cwd=attempt), run([str(exe), "run", str(bad), "--pack", "false", "--level", "error"], cwd=attempt), setup
    if tool == "arethetypeswrong":
        good = attempt / "good"
        bad = attempt / "bad"
        package_fixture(good, valid=True)
        package_fixture(bad, valid=False)
        good_tar, good_pack = pack_package(good)
        bad_tar, bad_pack = pack_package(bad)
        setup.extend([good_pack, bad_pack])
        if good_tar is None or bad_tar is None:
            return good_pack, bad_pack, setup
        exe = NODE_BIN / "attw.cmd"
        args = ["--no-definitely-typed", "--profile", "esm-only", "--format", "json", "--no-emoji", "--no-color"]
        return run([str(exe), *args, str(good_tar)], cwd=attempt, timeout=180), run([str(exe), *args, str(bad_tar)], cwd=attempt, timeout=180), setup
    if tool == "npm-package-json-lint":
        good = attempt / "good"
        bad = attempt / "bad"
        write_json(good / "package.json", {"name": "neris-valid", "version": "1.0.0", "license": "MIT"})
        write_json(bad / "package.json", {"version": "1.0.0", "license": "MIT"})
        config = attempt / "npmpackagejsonlint.config.json"
        write_json(config, {"rules": {"require-name": "error", "require-version": "error"}})
        exe = NODE_BIN / "npmPkgJsonLint.cmd"
        return run([str(exe), "--configFile", str(config), "good/**/package.json"], cwd=attempt), run([str(exe), "--configFile", str(config), "bad/**/package.json"], cwd=attempt), setup
    if tool == "lockfile-lint":
        good_lock = attempt / "good.yarn.lock"
        bad_lock = attempt / "bad.yarn.lock"
        integrity = "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA=="
        def lock_text(host: str) -> str:
            resolved = f"https://{host}/picocolors/-/picocolors-1.1.1.tgz"
            return (
                "# yarn lockfile v1\n\n"
                "picocolors@1.1.1:\n"
                "  version \"1.1.1\"\n"
                f"  resolved \"{resolved}\"\n"
                f"  integrity {integrity}\n"
            )
        write_text(good_lock, lock_text("registry.yarnpkg.com"))
        write_text(bad_lock, lock_text("untrusted.example.invalid"))
        exe = NODE_BIN / "lockfile-lint.cmd"
        common = ["--type", "yarn", "--validate-https", "--validate-integrity", "--empty-hostname", "false", "--allowed-hosts", "yarn"]
        return run([str(exe), "--path", good_lock.name, *common], cwd=attempt), run([str(exe), "--path", bad_lock.name, *common], cwd=attempt), setup
    if tool == "syncpack":
        good = attempt / "good"
        bad = attempt / "bad"
        for root, mismatch in ((good, False), (bad, True)):
            write_json(root / "package.json", {"name": "neris-workspace", "version": "1.0.0", "private": True, "workspaces": ["packages/*"]})
            write_json(root / "packages" / "a" / "package.json", {"name": "neris-a", "version": "1.0.0", "dependencies": {"picocolors": "1.1.1"}})
            write_json(root / "packages" / "b" / "package.json", {"name": "neris-b", "version": "1.0.0", "dependencies": {"picocolors": "1.0.0" if mismatch else "1.1.1"}})
        exe = NODE_BIN / "syncpack.cmd"
        return run([str(exe), "lint"], cwd=good), run([str(exe), "lint"], cwd=bad), setup
    raise RuntimeError(f"unknown tool: {tool}")


def run_tool(tool: str, *, recovery: bool) -> dict[str, Any]:
    if tool not in TOOLS:
        raise RuntimeError(f"unknown tool: {tool}")
    receipt_root = CACHE_ROOT / "smoke-receipts" / tool
    initial_path = receipt_root / "attempt-1.json"
    if recovery:
        if not initial_path.is_file():
            raise RuntimeError("recovery requires a retained initial receipt")
        prior_paths = [initial_path, *sorted(receipt_root.glob("attempt-*-recovery.json"))]
        prior_receipts = [json.loads(path.read_text(encoding="utf-8")) for path in prior_paths]
        current = max(prior_receipts, key=lambda row: int(row["attempt"]))
        if current.get("status") == "PASS":
            raise RuntimeError("successful smoke replay forbidden")
        attempt_number = int(current["attempt"]) + 1
        recovery_path = receipt_root / f"attempt-{attempt_number}-recovery.json"
        if recovery_path.exists():
            raise RuntimeError("recovery receipt already exists")
        receipt_path = recovery_path
    else:
        if initial_path.exists():
            raise RuntimeError("initial smoke receipt already exists")
        attempt_number = 1
        receipt_path = initial_path
    attempt = TEMP_ROOT / tool / f"attempt-{attempt_number}"
    if attempt.exists():
        raise RuntimeError("fresh smoke fixture directory already exists")
    attempt.mkdir(parents=True, exist_ok=False)
    positive, negative, setup = commands_for(tool, attempt)
    passed = positive["returncode"] == 0 and negative["returncode"] != 0 and not positive["timed_out"]
    receipt = {
        "schema": "ghc-family-replay-guarded-tool-smoke-v1",
        "owner": "Neris Solane",
        "phase": "v667-v8-r2",
        "tool": tool,
        "attempt": attempt_number,
        "status": "PASS" if passed else "FAILED_RETAINED_ZERO_CREDIT",
        "positive_passed": positive["returncode"] == 0,
        "negative_rejected": negative["returncode"] != 0,
        "positive": positive,
        "negative": negative,
        "setup": setup,
        "real_data_rows": 0,
        "participants": 0,
        "external_actions": 0,
        "network_calls": 0,
        "completion_credit": 1 if passed else 0,
        "failure_credit": 0,
        "boundary": "wholly synthetic same-owner smoke only; no exhaustive security fitness production legal cultural or authority claim",
    }
    write_json(receipt_path, receipt)
    print(json.dumps({"tool": tool, "attempt": attempt_number, "status": receipt["status"]}, sort_keys=True))
    return receipt


def aggregate() -> dict[str, Any]:
    selected = []
    retained_failures = []
    for tool in TOOLS:
        root = CACHE_ROOT / "smoke-receipts" / tool
        initial_path = root / "attempt-1.json"
        if not initial_path.is_file():
            raise RuntimeError(f"initial smoke receipt absent: {tool}")
        initial = json.loads(initial_path.read_text(encoding="utf-8"))
        if initial["status"] != "PASS":
            retained_failures.append(initial)
            recovery_paths = sorted(root.glob("attempt-*-recovery.json"))
            if not recovery_paths:
                raise RuntimeError(f"failed smoke has no isolated recovery: {tool}")
            recovery_receipts = [json.loads(path.read_text(encoding="utf-8")) for path in recovery_paths]
            retained_failures.extend(row for row in recovery_receipts if row["status"] != "PASS")
            current = max(recovery_receipts, key=lambda row: int(row["attempt"]))
        else:
            current = initial
        if current["status"] != "PASS":
            raise RuntimeError(f"current smoke is not passing: {tool}")
        selected.append(current)
    receipt = {
        "schema": "ghc-family-thirteen-tool-smoke-aggregate-v1",
        "owner": "Neris Solane",
        "phase": "v667-v8-r2",
        "status": "PASS",
        "direct_tool_count": 13,
        "positive_smoke_count": sum(row["positive_passed"] for row in selected),
        "negative_rejection_count": sum(row["negative_rejected"] for row in selected),
        "retained_failed_attempt_count": len(retained_failures),
        "successful_smoke_replay_count": 0,
        "selected_receipts": selected,
        "retained_failures": retained_failures,
        "boundary": "thirteen bounded fixture-local smokes are not a package-security certification or production fitness decision",
    }
    write_json(CACHE_ROOT / "thirteen-tool-smoke-aggregate.json", receipt)
    write_json(PHASE_ROOT / "x2" / "tooling" / "thirteen-tool-smoke-aggregate.json", receipt)
    print(json.dumps({"status": "PASS", "tools": 13, "retained_failed_attempts": len(retained_failures)}))
    return receipt


def record_interrupted(tool: str) -> dict[str, Any]:
    if tool not in TOOLS:
        raise RuntimeError(f"unknown tool: {tool}")
    attempt = TEMP_ROOT / tool / "attempt-1"
    receipt_path = CACHE_ROOT / "smoke-receipts" / tool / "attempt-1.json"
    if not attempt.is_dir() or receipt_path.exists():
        raise RuntimeError("interrupted marker requires an existing attempt directory and absent receipt")
    receipt = {
        "schema": "ghc-family-replay-guarded-tool-smoke-v1",
        "owner": "Neris Solane",
        "phase": "v667-v8-r2",
        "tool": tool,
        "attempt": 1,
        "status": "FAILED_RETAINED_ZERO_CREDIT",
        "positive_passed": False,
        "negative_rejected": False,
        "pre_receipt_exception": "npm 12 pack --json returned a package-keyed object where the first parser expected a list",
        "completion_credit": 0,
        "failure_credit": 0,
        "boundary": "retained pre-receipt failure; no tool success credit",
    }
    write_json(receipt_path, receipt)
    print(json.dumps({"tool": tool, "attempt": 1, "status": receipt["status"], "recorded": True}, sort_keys=True))
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", choices=TOOLS)
    parser.add_argument("--recover", action="store_true")
    parser.add_argument("--aggregate", action="store_true")
    parser.add_argument("--record-interrupted", action="store_true")
    args = parser.parse_args()
    if args.aggregate:
        aggregate()
        return 0
    if not args.tool:
        parser.error("--tool or --aggregate is required")
    if args.record_interrupted:
        record_interrupted(args.tool)
        return 0
    run_tool(args.tool, recovery=args.recover)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
