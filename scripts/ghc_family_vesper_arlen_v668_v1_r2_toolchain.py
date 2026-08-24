#!/usr/bin/env python3
"""Install and smoke thirteen pinned tools in a D-isolated family bank.

The transaction never changes the user PATH, PowerShell profile, Codex desktop,
Windows features, host security, or sibling worktrees.  It records exact direct
pins and transitive archive/lock integrity, but does not claim exhaustive
security, production fitness, or legal license interpretation.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

PYTHON_PINS = {
    "commitizen": "4.18.0",
    "pre-commit-hooks": "6.0.0",
    "hatch": "1.18.0",
    "pytest-randomly": "4.1.0",
    "pytest-xdist": "3.8.0",
    "mkdocs": "1.6.1",
    "pycln": "2.6.0",
    "check-jsonschema": "0.38.0",
}
NODE_PINS = {
    "cspell": "10.1.0",
    "markdown-link-check": "3.15.0",
    "sort-package-json": "4.0.0",
    "audit-ci": "7.1.0",
    "@cyclonedx/cyclonedx-npm": "6.0.1",
}
EXPECTED_NPM_INTEGRITIES = {
    "cspell": "sha512-sCGe2PWuA7H8pJTYSSkq5G5u3FXJr8igAcVEsSAqdAdTArkOxCca4kPNfeRhno2Dy1QEz7KGnoVFggvIaCv01g==",
    "markdown-link-check": "sha512-EorpVYNu1Jpldk3OLrRrH7Hx/ofp1dCSAJeYuvb8MhKR/rIt6S0tgwbQYw66EZgRPu9lPvORfT6SkIe0dwn2Ow==",
    "sort-package-json": "sha512-6aYOlYI9AWioZ+rzu+4zKLmoFqJP0/fHDxrd7X04yqEibikY+5YVF0EYlyGn4v6X2PJY7yAUWV7oeP+i5rOm/g==",
    "audit-ci": "sha512-PjjEejlST57S/aDbeWLic0glJ8CNl/ekY3kfGFPMrPkmuaYaDKcMH0F9x9yS9Vp6URhuefSCubl/G0Y2r6oP0g==",
    "@cyclonedx/cyclonedx-npm": "sha512-/aU3bBC6qP6cV/qQ5SfUSygE/+2hQhwgg6sJML31/gZ96NyMvIUuwdk637H4z+LS/NryRT2kjR2wtD0qBEVVHQ==",
}
LABEL = "vesper-v668-v1-r2-recovery-01"
PLANNED_INCOMPATIBLE_PIN = {"package": "reuse", "version": "6.2.0", "state": "open_gap", "credit": 0}
BOUNDARY = (
    "Pinned registry metadata, local dependency audits, and bounded smokes are not exhaustive security, "
    "production certification, professional validation, or legal license advice."
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(command: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None, timeout: int = 600) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=timeout, check=False)


def command_receipt(result: subprocess.CompletedProcess[bytes]) -> dict[str, Any]:
    return {
        "exit_code": result.returncode,
        "stdout_sha256": digest(result.stdout),
        "stderr_sha256": digest(result.stderr),
        "stdout_bytes": len(result.stdout),
        "stderr_bytes": len(result.stderr),
    }


def require_exit(result: subprocess.CompletedProcess[bytes], expected_success: bool, label: str) -> dict[str, Any]:
    passed = result.returncode == 0 if expected_success else result.returncode != 0
    receipt = {"label": label, "expected": "zero" if expected_success else "nonzero", "passed": passed, **command_receipt(result)}
    if not passed:
        raise RuntimeError(f"smoke expectation failed for {label}: {receipt}")
    return receipt


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value) + b"\n")


def python_site(venv_root: Path) -> Path:
    return venv_root / "Lib" / "site-packages"


def direct_versions(python: Path) -> dict[str, str]:
    code = "import importlib.metadata,json; print(json.dumps({n:importlib.metadata.version(n) for n in " + repr(sorted(PYTHON_PINS)) + "},sort_keys=True))"
    result = run([str(python), "-c", code])
    if result.returncode:
        raise RuntimeError("unable to read installed Python direct versions")
    return json.loads(result.stdout.decode("utf-8"))


def lock_integrities(lock: dict[str, Any]) -> dict[str, str]:
    output: dict[str, str] = {}
    packages = lock.get("packages", {})
    for package in NODE_PINS:
        entry = packages.get(f"node_modules/{package}", {})
        output[package] = str(entry.get("integrity", ""))
    return output


def make_fixtures(root: Path) -> dict[str, Path]:
    root.mkdir(parents=True, exist_ok=True)
    paths = {
        "clean_py": root / "clean.py",
        "unused_py": root / "unused.py",
        "pytest_file": root / "test_smoke.py",
        "schema": root / "schema.json",
        "valid_json": root / "valid.json",
        "invalid_json": root / "invalid.json",
        "mkdocs_yml": root / "mkdocs.yml",
        "mkdocs_index": root / "docs" / "index.md",
        "spell_ok": root / "spell-ok.txt",
        "spell_bad": root / "spell-bad.txt",
        "links_ok": root / "links-ok.md",
        "links_bad": root / "links-bad.md",
        "package_valid": root / "package-valid.json",
        "package_invalid": root / "package-invalid.json",
    }
    paths["clean_py"].write_text("value = 1\n", encoding="utf-8", newline="\n")
    paths["unused_py"].write_text("import os\nvalue = 1\n", encoding="utf-8", newline="\n")
    paths["pytest_file"].write_text("def test_ok():\n    assert True\n", encoding="utf-8", newline="\n")
    write_json(paths["schema"], {"type": "object", "required": ["ok"], "properties": {"ok": {"const": True}}, "additionalProperties": False})
    write_json(paths["valid_json"], {"ok": True})
    write_json(paths["invalid_json"], {"ok": False})
    paths["mkdocs_yml"].write_text("site_name: bounded-smoke\ndocs_dir: docs\nsite_dir: site\n", encoding="utf-8", newline="\n")
    paths["mkdocs_index"].parent.mkdir(parents=True, exist_ok=True)
    paths["mkdocs_index"].write_text("# Bounded smoke\n", encoding="utf-8", newline="\n")
    paths["spell_ok"].write_text("archive provenance custody\n", encoding="utf-8", newline="\n")
    paths["spell_bad"].write_text("zzqvxxmisspelledtoken\n", encoding="utf-8", newline="\n")
    paths["links_ok"].write_text("[local](links-ok.md)\n", encoding="utf-8", newline="\n")
    paths["links_bad"].write_text("[missing](missing-local-file.md)\n", encoding="utf-8", newline="\n")
    write_json(paths["package_valid"], {"version": "1.0.0", "name": "bounded-smoke", "description": "fixture"})
    paths["package_invalid"].write_text("{invalid\n", encoding="utf-8", newline="\n")
    return paths


def python_smokes(python: Path, scripts: Path, fixtures: dict[str, Path]) -> list[dict[str, Any]]:
    executable = lambda name: str(scripts / f"{name}.exe")
    smokes: list[dict[str, Any]] = []
    smokes.append(require_exit(run([executable("cz"), "check", "--message", "feat: bounded provenance smoke"]), True, "commitizen-positive"))
    smokes.append(require_exit(run([executable("cz"), "check", "--message", "invalid message"]), False, "commitizen-reject"))
    smokes.append(require_exit(run([executable("check-json"), str(fixtures["valid_json"])]), True, "pre-commit-hooks-positive"))
    smokes.append(require_exit(run([executable("check-json"), str(fixtures["package_invalid"])]), False, "pre-commit-hooks-reject"))
    smokes.append(require_exit(run([executable("hatch"), "--version"]), True, "hatch-positive"))
    smokes.append(require_exit(run([executable("hatch"), "definitely-invalid-subcommand"]), False, "hatch-reject"))
    smokes.append(require_exit(run([str(python), "-m", "pytest", "-q", "-p", "no:cacheprovider", "--randomly-seed=17", str(fixtures["pytest_file"])]), True, "pytest-randomly-positive"))
    smokes.append(require_exit(run([str(python), "-m", "pytest", "--randomly-seed=not-an-integer", str(fixtures["pytest_file"])]), False, "pytest-randomly-reject"))
    smokes.append(require_exit(run([str(python), "-m", "pytest", "-q", "-p", "no:cacheprovider", "-n", "1", str(fixtures["pytest_file"])]), True, "pytest-xdist-positive"))
    smokes.append(require_exit(run([str(python), "-m", "pytest", "-n", "not-a-count", str(fixtures["pytest_file"])]), False, "pytest-xdist-reject"))
    smokes.append(require_exit(run([executable("mkdocs"), "build", "--strict", "--config-file", str(fixtures["mkdocs_yml"])], cwd=fixtures["mkdocs_yml"].parent), True, "mkdocs-positive"))
    smokes.append(require_exit(run([executable("mkdocs"), "build", "--config-file", str(fixtures["mkdocs_yml"].parent / "absent.yml")]), False, "mkdocs-reject"))
    smokes.append(require_exit(run([executable("pycln"), "--check", str(fixtures["clean_py"])]), True, "pycln-positive"))
    smokes.append(require_exit(run([executable("pycln"), "--check", str(fixtures["unused_py"])]), False, "pycln-reject"))
    smokes.append(require_exit(run([executable("check-jsonschema"), "--schemafile", str(fixtures["schema"]), str(fixtures["valid_json"])]), True, "check-jsonschema-positive"))
    smokes.append(require_exit(run([executable("check-jsonschema"), "--schemafile", str(fixtures["schema"]), str(fixtures["invalid_json"])]), False, "check-jsonschema-reject"))
    return smokes


def node_smokes(node_root: Path, fixtures: dict[str, Path]) -> list[dict[str, Any]]:
    bins = node_root / "node_modules" / ".bin"
    cmd = lambda name: str(bins / f"{name}.cmd")
    smokes: list[dict[str, Any]] = []
    cwd = fixtures["spell_ok"].parent
    smokes.append(require_exit(run([cmd("cspell"), "lint", "--no-progress", "--no-summary", fixtures["spell_ok"].name], cwd=cwd), True, "cspell-positive"))
    smokes.append(require_exit(run([cmd("cspell"), "lint", "--no-progress", "--no-summary", fixtures["spell_bad"].name], cwd=cwd), False, "cspell-reject"))
    smokes.append(require_exit(run([cmd("markdown-link-check"), "--quiet", fixtures["links_ok"].name], cwd=cwd), True, "markdown-link-check-positive"))
    smokes.append(require_exit(run([cmd("markdown-link-check"), "--quiet", fixtures["links_bad"].name], cwd=cwd), False, "markdown-link-check-reject"))
    smokes.append(require_exit(run([cmd("sort-package-json"), "--check", fixtures["package_valid"].name], cwd=cwd), False, "sort-package-json-unsorted-reject"))
    smokes.append(require_exit(run([cmd("sort-package-json"), fixtures["package_valid"].name], cwd=cwd), True, "sort-package-json-positive"))
    smokes.append(require_exit(run([cmd("sort-package-json"), fixtures["package_invalid"].name], cwd=cwd), False, "sort-package-json-invalid-reject"))
    smokes.append(require_exit(run([cmd("audit-ci"), "--version"]), True, "audit-ci-positive"))
    smokes.append(require_exit(run([cmd("audit-ci"), "--definitely-invalid-option"]), False, "audit-ci-reject"))
    smokes.append(require_exit(run([cmd("cyclonedx-npm"), "--version"]), True, "cyclonedx-npm-positive"))
    smokes.append(require_exit(run([cmd("cyclonedx-npm"), fixtures["package_invalid"].name], cwd=cwd), False, "cyclonedx-npm-reject"))
    return smokes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank-root", type=Path, required=True)
    parser.add_argument("--phase-root", type=Path, required=True)
    parser.add_argument("--resume-existing", action="store_true")
    args = parser.parse_args()
    bank = args.bank_root.resolve()
    phase = args.phase_root.resolve()
    if bank.drive.casefold() != "d:":
        raise SystemExit("bank root must resolve to the D drive")
    python_root = bank / "global-tools" / "python" / LABEL
    node_root = bank / "global-tools" / "node" / LABEL
    transaction_root = bank / "toolchains" / LABEL
    existing = [path.exists() for path in (python_root, node_root, transaction_root)]
    if any(existing) and not args.resume_existing:
        raise SystemExit("transaction targets already exist; require explicit resume or a fresh label")
    if args.resume_existing and not all(existing):
        raise SystemExit("resume requires all three exact transaction roots")
    wheels = transaction_root / "wheels"
    wheels.mkdir(parents=True, exist_ok=args.resume_existing)
    python_root.parent.mkdir(parents=True, exist_ok=True)
    node_root.mkdir(parents=True, exist_ok=True)

    setup_receipts: list[dict[str, Any]] = []
    venv_python = python_root / "core" / "Scripts" / "python.exe"
    venv_scripts = python_root / "core" / "Scripts"
    requirements = [f"{name}=={version}" for name, version in PYTHON_PINS.items()]
    if not args.resume_existing:
        create = run([sys.executable, "-m", "venv", str(python_root / "core")], timeout=300)
        setup_receipts.append({"step": "create-python-venv", **command_receipt(create)})
        if create.returncode:
            raise RuntimeError("Python venv creation failed")
        download = run([str(venv_python), "-m", "pip", "download", "--only-binary=:all:", "--dest", str(wheels), *requirements], timeout=900)
        setup_receipts.append({"step": "download-python-wheels", **command_receipt(download)})
        if download.returncode:
            raise RuntimeError("Python wheel download failed")
    wheel_rows = [{"filename": path.name, "sha256": digest(path.read_bytes()), "bytes": path.stat().st_size} for path in sorted(wheels.glob("*.whl"))]
    if not args.resume_existing:
        install = run([str(venv_python), "-m", "pip", "install", "--no-index", "--find-links", str(wheels), *requirements], timeout=900)
        setup_receipts.append({"step": "install-python-from-locked-wheel-bank", **command_receipt(install)})
        if install.returncode:
            raise RuntimeError("Python install failed")
    py_versions = direct_versions(venv_python)
    if py_versions != PYTHON_PINS:
        raise RuntimeError(f"Python direct pin mismatch: {py_versions}")
    if args.resume_existing:
        setup_receipts.append({"step": "resume-verify-python-direct-pins", "exit_code": 0, "verified_count": len(py_versions)})

    package_json = {"name": "ghc-family-vesper-v668-v1-r2-tools", "version": "0.0.0", "private": True, "description": "D-isolated bounded tool bank", "license": "UNLICENSED"}
    write_json(node_root / "package.json", package_json)
    node_specs = [f"{name}@{version}" for name, version in NODE_PINS.items()]
    npm_env = os.environ.copy()
    npm_env["npm_config_ignore_scripts"] = "true"
    npm_executable = shutil.which("npm.cmd") or shutil.which("npm")
    if not npm_executable:
        raise RuntimeError("npm command shim unavailable")
    node_lock_path = node_root / "package-lock.json"
    node_modules_path = node_root / "node_modules"
    if not (args.resume_existing and node_lock_path.exists() and node_modules_path.is_dir()):
        lock = run([npm_executable, "install", "--package-lock-only", "--ignore-scripts", "--no-audit", "--no-fund", "--save-exact", *node_specs], cwd=node_root, env=npm_env, timeout=900)
        setup_receipts.append({"step": "resolve-node-lock-with-scripts-disabled", **command_receipt(lock)})
        if lock.returncode:
            raise RuntimeError("Node lock resolution failed")
        ci = run([npm_executable, "ci", "--ignore-scripts", "--no-audit", "--no-fund"], cwd=node_root, env=npm_env, timeout=900)
        setup_receipts.append({"step": "install-node-lock-with-scripts-disabled", **command_receipt(ci)})
        if ci.returncode:
            raise RuntimeError("Node lock install failed")
    else:
        setup_receipts.append({"step": "resume-verify-existing-node-lock-and-modules", "exit_code": 0})
    lock_data = json.loads((node_root / "package-lock.json").read_text(encoding="utf-8"))
    direct_integrity = lock_integrities(lock_data)
    if direct_integrity != EXPECTED_NPM_INTEGRITIES:
        raise RuntimeError(f"Node direct integrity mismatch: {direct_integrity}")

    fixtures_root = transaction_root / "fixtures"
    fixtures = make_fixtures(fixtures_root)
    python_smoke_rows = python_smokes(venv_python, venv_scripts, fixtures)
    node_smoke_rows = node_smokes(node_root, fixtures)

    pip_audit_exe = shutil.which("pip-audit")
    if pip_audit_exe:
        pip_audit_command = [pip_audit_exe]
    elif importlib.util.find_spec("pip_audit") is not None:
        pip_audit_command = [sys.executable, "-m", "pip_audit"]
    else:
        raise RuntimeError("inherited pip-audit command unavailable")
    pip_audit = run([*pip_audit_command, "--path", str(python_site(python_root / "core")), "--format", "json", "--progress-spinner", "off"], timeout=900)
    pip_audit_payload: Any
    try:
        pip_audit_payload = json.loads(pip_audit.stdout.decode("utf-8"))
    except json.JSONDecodeError:
        pip_audit_payload = None
    pip_vulnerabilities = 0
    if isinstance(pip_audit_payload, dict):
        dependencies = pip_audit_payload.get("dependencies", [])
    elif isinstance(pip_audit_payload, list):
        dependencies = pip_audit_payload
    else:
        dependencies = []
    for row in dependencies:
        if isinstance(row, dict):
            pip_vulnerabilities += len(row.get("vulns", []))

    npm_audit = run([npm_executable, "audit", "--json"], cwd=node_root, env=npm_env, timeout=900)
    try:
        npm_audit_payload = json.loads(npm_audit.stdout.decode("utf-8"))
    except json.JSONDecodeError:
        npm_audit_payload = {}
    npm_vulnerabilities = int(npm_audit_payload.get("metadata", {}).get("vulnerabilities", {}).get("total", -1))

    audit_gate = pip_vulnerabilities == 0 and npm_vulnerabilities == 0 and pip_audit_payload is not None and npm_vulnerabilities >= 0
    transaction = {
        "schema": "ghc.family.toolchain.transaction.v1",
        "transaction_label": LABEL,
        "supersedes_quarantined_transaction_label": "vesper-v668-v1-r2",
        "resumed_after_verified_python_install": args.resume_existing,
        "state": "COMPLETED_BOUNDED_INSTALL" if audit_gate else "QUARANTINED_AUDIT_FINDINGS",
        "direct_tool_count": len(PYTHON_PINS) + len(NODE_PINS),
        "python_direct_pins": PYTHON_PINS,
        "python_direct_versions": py_versions,
        "planned_incompatible_pin": PLANNED_INCOMPATIBLE_PIN,
        "bounded_substitution": {"package": "pre-commit-hooks", "version": PYTHON_PINS["pre-commit-hooks"], "reason": "current reuse pin has no compatible Windows CPython 3.12 wheel"},
        "python_wheel_count": len(wheel_rows),
        "python_wheels": wheel_rows,
        "node_direct_pins": NODE_PINS,
        "node_direct_integrities": direct_integrity,
        "node_lock_sha256": digest((node_root / "package-lock.json").read_bytes()),
        "npm_install_scripts_disabled": True,
        "setup_receipts": setup_receipts,
        "positive_smoke_count": sum(row["expected"] == "zero" for row in python_smoke_rows + node_smoke_rows),
        "rejecting_smoke_count": sum(row["expected"] == "nonzero" for row in python_smoke_rows + node_smoke_rows),
        "all_smokes_passed": all(row["passed"] for row in python_smoke_rows + node_smoke_rows),
        "python_smokes": python_smoke_rows,
        "node_smokes": node_smoke_rows,
        "pip_audit": {**command_receipt(pip_audit), "parsed": pip_audit_payload is not None, "vulnerability_count": pip_vulnerabilities},
        "pip_audit_path_fallback_used": pip_audit_exe is None,
        "npm_audit": {**command_receipt(npm_audit), "parsed": bool(npm_audit_payload), "vulnerability_count": npm_vulnerabilities},
        "audit_gate_passed": audit_gate,
        "path_or_profile_mutated": False,
        "powershell_profile_mutated": False,
        "codex_desktop_updated": False,
        "windows_feature_changed": False,
        "host_security_changed": False,
        "rebooted": False,
        "D_isolated": True,
        "private_absolute_paths_recorded": False,
        "rollback": "Remove only the exact transaction-labelled D-isolated Python, Node, and transaction directories after literal-path verification.",
        "boundary": BOUNDARY,
    }
    write_json(transaction_root / "transaction.json", transaction)
    write_json(phase / "x2" / "toolchain" / "toolchain-transaction.json", transaction)
    write_json(phase / "x2" / "toolchain" / "installed-tool-catalog.json", {
        "transaction_label": LABEL,
        "supersedes_quarantined_transaction_label": "vesper-v668-v1-r2",
        "direct_tools": [
            *[{"ecosystem": "python", "package": name, "version": version, "state": "completed" if audit_gate else "exact_gate"} for name, version in PYTHON_PINS.items()],
            *[{"ecosystem": "node", "package": name, "version": version, "state": "completed" if audit_gate else "exact_gate"} for name, version in NODE_PINS.items()],
        ],
        "count": len(PYTHON_PINS) + len(NODE_PINS),
        "audit_gate_passed": audit_gate,
        "boundary": BOUNDARY,
    })
    print(json.dumps({"state": transaction["state"], "direct_tools": transaction["direct_tool_count"], "python_wheels": len(wheel_rows), "positive_smokes": transaction["positive_smoke_count"], "rejecting_smokes": transaction["rejecting_smoke_count"], "pip_vulnerabilities": pip_vulnerabilities, "npm_vulnerabilities": npm_vulnerabilities}, sort_keys=True))
    return 0 if audit_gate else 3


if __name__ == "__main__":
    raise SystemExit(main())
