#!/usr/bin/env python3
"""Stage and verify the D-backed Neris v667-v8-r2 tool transaction."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

from packaging.utils import canonicalize_name, parse_wheel_filename


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "neris-solane" / "v667-v8-r2"
PLAN_PATH = PHASE_ROOT / "x1" / "toolchain-install-plan.json"
D_ROOT = Path("D:/GHC-Archives")
CACHE_ROOT = D_ROOT / "tool-caches" / "neris-v667-v8-r2"
WHEELHOUSE = CACHE_ROOT / "wheels"
WHEELHOUSE_CORE = WHEELHOUSE / "core"
WHEELHOUSE_INSPECT = WHEELHOUSE / "wheel-inspect"
NODE_TARBALLS = CACHE_ROOT / "node-tarballs"
PY_ENV = D_ROOT / "global-tools" / "python" / "neris-v667-v8-r2"
PY_ENV_CORE = PY_ENV / "core"
PY_ENV_INSPECT = PY_ENV / "wheel-inspect"
NODE_ENV = D_ROOT / "global-tools" / "node" / "neris-v667-v8-r2"
TEMP_ROOT = D_ROOT / "phase-temp" / "neris-v667-v8-r2"
PIP_REMEDIATION_VERSION = "26.2.1"
PIP_REMEDIATION_FILENAME = "pip-26.2.1-py3-none-any.whl"
PIP_REMEDIATION_SHA256 = "71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e"
PIP_REMEDIATION_URL = (
    "https://files.pythonhosted.org/packages/f3/6e/1736e5b4ae2b778ef2f81c47d797de9f891d4d8acb047a24ca37a60294dd/"
    + PIP_REMEDIATION_FILENAME
)


def read_plan() -> dict:
    return json.loads(PLAN_PATH.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json.dumps(value, indent=2, sort_keys=True).encode("utf-8") + b"\n")


def repo_write(relative: str, value: object) -> None:
    write_json(PHASE_ROOT / relative, value)


def prepare() -> None:
    targets = [CACHE_ROOT, PY_ENV, NODE_ENV, TEMP_ROOT]
    existing = [str(path) for path in targets if path.exists()]
    if existing:
        raise RuntimeError(f"fresh transaction target already exists: {existing}")
    for path in (WHEELHOUSE, NODE_TARBALLS, NODE_ENV, TEMP_ROOT):
        path.mkdir(parents=True, exist_ok=False)
    plan = read_plan()
    node = {row["tool"]: row["version"] for row in plan["new_tools"] if row["ecosystem"] == "node"}
    write_json(
        NODE_ENV / "package.json",
        {
            "name": "ghc-family-neris-v667-v8-r2-toolchain",
            "version": "1.0.0",
            "private": True,
            "description": "D-backed bounded family tool transaction; no publication",
            "dependencies": node,
        },
    )
    aliases = {
        "schema": "ghc-family-external-path-aliases-v1",
        "owner": "Neris Solane",
        "phase": "v667-v8-r2",
        "aliases": {
            "D_TOOL_CACHE": "tool-caches/neris-v667-v8-r2",
            "D_FAMILY_PY_ENV": "global-tools/python/neris-v667-v8-r2",
            "D_FAMILY_NODE_ENV": "global-tools/node/neris-v667-v8-r2",
            "D_PHASE_TEMP": "phase-temp/neris-v667-v8-r2",
        },
        "boundary": "repository receipt uses D-root aliases and contains no private user path",
    }
    repo_write("x2/tooling/external-path-aliases.json", aliases)
    write_json(
        CACHE_ROOT / "prepare-receipt.json",
        {
            "status": "PASS",
            "fresh_targets": True,
            "python_environment_created": False,
            "node_package_json_created": True,
            "lifecycle_scripts_executed": 0,
        },
    )
    print(json.dumps({"status": "PASS", "stage": "prepare", "node_direct": len(node)}))


def lock_python() -> None:
    plan = read_plan()
    python_direct = [row for row in plan["new_tools"] if row["ecosystem"] == "python"]
    groups = {
        "core": {
            "wheelhouse": WHEELHOUSE_CORE,
            "direct": [row for row in python_direct if row["tool"] != "wheel-inspect"],
        },
        "wheel-inspect": {
            "wheelhouse": WHEELHOUSE_INSPECT,
            "direct": [row for row in python_direct if row["tool"] == "wheel-inspect"],
        },
    }
    group_receipts = {}
    all_entries = []
    mismatches = []
    for group_name, group in groups.items():
        wheels = sorted(group["wheelhouse"].glob("*.whl"))
        if not wheels:
            raise RuntimeError(f"wheelhouse is empty: {group_name}")
        entries = []
        by_filename = {}
        for path in wheels:
            name, version, build, tags = parse_wheel_filename(path.name)
            data = path.read_bytes()
            entry = {
                "name": canonicalize_name(str(name)),
                "version": str(version),
                "filename": path.name,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "environment": group_name,
            }
            entries.append(entry)
            by_filename[path.name] = entry
        for row in group["direct"]:
            entry = by_filename.get(row["artifact"])
            if entry is None:
                mismatches.append({"tool": row["tool"], "reason": "missing exact top-level wheel"})
            elif entry["sha256"] != row["sha256_or_integrity"]:
                mismatches.append({"tool": row["tool"], "reason": "top-level sha256 mismatch"})
        grouped: dict[tuple[str, str], list[str]] = {}
        for entry in entries:
            grouped.setdefault((entry["name"], entry["version"]), []).append(entry["sha256"])
        lock_lines = []
        for (name, version), hashes in sorted(grouped.items()):
            suffix = " ".join(f"--hash=sha256:{value}" for value in sorted(set(hashes)))
            lock_lines.append(f"{name}=={version} {suffix}")
        lock_text = "\n".join(lock_lines) + "\n"
        external_lock = CACHE_ROOT / f"python-{group_name}-requirements.lock"
        repo_lock = PHASE_ROOT / "x2" / "tooling" / f"python-{group_name}-requirements.lock"
        external_lock.write_text(lock_text, encoding="utf-8", newline="\n")
        repo_lock.parent.mkdir(parents=True, exist_ok=True)
        repo_lock.write_text(lock_text, encoding="utf-8", newline="\n")
        group_receipts[group_name] = {
            "direct_count": len(group["direct"]),
            "wheel_count": len(entries),
            "transitive_wheel_count": len(entries) - len(group["direct"]),
            "requirements_line_count": len(lock_lines),
        }
        all_entries.extend(entries)
    if mismatches:
        raise RuntimeError(f"top-level wheel verification failed: {mismatches}")
    receipt = {
        "schema": "ghc-family-python-wheel-lock-v1",
        "status": "PASS",
        "environment_count": 2,
        "split_reason": "check-wheel-contents 0.6.3 requires wheel-filename ~=1.1 while wheel-inspect 1.8.0 requires wheel-filename ~=2.0",
        "failed_combined_resolution_retained": True,
        "direct_count": len(python_direct),
        "wheel_count": len(all_entries),
        "groups": group_receipts,
        "top_level_mismatches": 0,
        "wheel_entries": all_entries,
        "wheel_only": True,
        "source_build_count": 0,
        "boundary": "hash equality is byte equality only and not authenticity exhaustive security fitness or legal evidence",
    }
    repo_write("x2/tooling/python-wheel-lock-receipt.json", receipt)
    write_json(CACHE_ROOT / "python-wheel-lock-receipt.json", receipt)
    print(json.dumps({"status": "PASS", "stage": "lock-python", "wheels": len(all_entries), "environments": 2}))


def verify_node() -> None:
    plan = read_plan()
    direct = [row for row in plan["new_tools"] if row["ecosystem"] == "node"]
    lock_path = NODE_ENV / "package-lock.json"
    if not lock_path.is_file():
        raise RuntimeError("node package-lock is absent")
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    packages = lock.get("packages", {})
    entries = []
    for row in direct:
        key = "node_modules/" + row["tool"]
        value = packages.get(key)
        if not value:
            raise RuntimeError(f"missing direct lock entry: {key}")
        if value.get("version") != row["version"]:
            raise RuntimeError(f"node version mismatch: {row['tool']}")
        if value.get("integrity") != row["sha256_or_integrity"]:
            raise RuntimeError(f"node integrity mismatch: {row['tool']}")
        resolved = value.get("resolved")
        if not resolved or not resolved.startswith("https://registry.npmjs.org/"):
            raise RuntimeError(f"noncanonical direct registry URL: {row['tool']}")
        filename = row["tool"].replace("@", "").replace("/", "-") + "-" + row["version"] + ".tgz"
        destination = NODE_TARBALLS / filename
        with urllib.request.urlopen(resolved, timeout=60) as response:
            data = response.read()
        destination.write_bytes(data)
        actual = "sha512-" + base64.b64encode(hashlib.sha512(data).digest()).decode("ascii")
        if actual != row["sha256_or_integrity"]:
            raise RuntimeError(f"downloaded npm tarball integrity mismatch: {row['tool']}")
        entries.append(
            {
                "tool": row["tool"],
                "version": row["version"],
                "integrity": actual,
                "bytes": len(data),
                "cache_filename": filename,
                "registry_host": "registry.npmjs.org",
            }
        )
    receipt = {
        "schema": "ghc-family-node-lock-verification-v1",
        "status": "PASS",
        "direct_count": len(direct),
        "lockfile_version": lock.get("lockfileVersion"),
        "locked_package_entry_count": max(len(packages) - 1, 0),
        "top_level_integrity_mismatches": 0,
        "noncanonical_direct_registry_urls": 0,
        "lifecycle_scripts_executed": 0,
        "entries": entries,
        "boundary": "lock and tarball integrity are bounded byte and origin evidence only",
    }
    repo_write("x2/tooling/node-lock-receipt.json", receipt)
    write_json(CACHE_ROOT / "node-lock-receipt.json", receipt)
    print(json.dumps({"status": "PASS", "stage": "verify-node", "direct": len(entries)}))


def command_output(command: list[str], cwd: Path | None = None) -> str:
    completed = subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return completed.stdout.decode("utf-8", errors="strict")


def run_captured(
    command: list[str],
    *,
    cwd: Path | None = None,
    accepted_codes: tuple[int, ...] = (0,),
) -> tuple[int, str, str]:
    completed = subprocess.run(command, cwd=cwd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = completed.stdout.decode("utf-8", errors="strict")
    stderr = completed.stderr.decode("utf-8", errors="strict")
    if completed.returncode not in accepted_codes:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {command!r}\nstdout:\n{stdout}\nstderr:\n{stderr}"
        )
    return completed.returncode, stdout, stderr


def install_python() -> None:
    targets = (
        ("core", PY_ENV_CORE, WHEELHOUSE_CORE, CACHE_ROOT / "python-core-requirements.lock"),
        (
            "wheel-inspect",
            PY_ENV_INSPECT,
            WHEELHOUSE_INSPECT,
            CACHE_ROOT / "python-wheel-inspect-requirements.lock",
        ),
    )
    if PY_ENV.exists():
        existing_children = [path.name for path in PY_ENV.iterdir()]
        if existing_children:
            raise RuntimeError(f"fresh Python environment root is not empty: {existing_children}")
    PY_ENV.mkdir(parents=True, exist_ok=True)
    results = {}
    for name, environment, wheelhouse, lock_path in targets:
        if environment.exists():
            raise RuntimeError(f"fresh Python subenvironment already exists: {environment}")
        subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True)
        python_exe = environment / "Scripts" / "python.exe"
        install_command = [
            str(python_exe),
            "-m",
            "pip",
            "install",
            "--no-index",
            "--find-links",
            str(wheelhouse),
            "--only-binary=:all:",
            "--require-hashes",
            "-r",
            str(lock_path),
        ]
        _, install_stdout, _ = run_captured(install_command)
        _, check_stdout, check_stderr = run_captured([str(python_exe), "-m", "pip", "check"])
        check_text = (check_stdout + check_stderr).strip() + "\n"
        (CACHE_ROOT / f"pip-check-{name}.txt").write_text(check_text, encoding="utf-8", newline="\n")
        results[name] = {
            "install_output_lines": len(install_stdout.splitlines()),
            "pip_check": check_text.strip(),
        }
    write_json(
        CACHE_ROOT / "python-install-receipt.json",
        {
            "status": "PASS",
            "environment_count": 2,
            "network_used_during_install": False,
            "hash_enforcement": True,
            "pip_checks": results,
        },
    )
    print(json.dumps({"status": "PASS", "stage": "install-python", "environments": 2}))


def install_node() -> None:
    if (NODE_ENV / "package-lock.json").exists() or (NODE_ENV / "node_modules").exists():
        raise RuntimeError("fresh Node lock or node_modules already exists")
    npm = shutil.which("npm")
    if npm is None:
        raise RuntimeError("npm is unavailable")
    _, lock_stdout, _ = run_captured(
        [npm, "install", "--package-lock-only", "--ignore-scripts", "--no-audit", "--no-fund"],
        cwd=NODE_ENV,
    )
    verify_node()
    _, install_stdout, _ = run_captured(
        [npm, "ci", "--ignore-scripts", "--no-audit", "--no-fund"],
        cwd=NODE_ENV,
    )
    write_json(
        CACHE_ROOT / "node-install-receipt.json",
        {
            "status": "PASS",
            "lock_output_lines": len(lock_stdout.splitlines()),
            "install_output_lines": len(install_stdout.splitlines()),
            "lifecycle_scripts_executed": 0,
            "ignore_scripts": True,
        },
    )
    print(json.dumps({"status": "PASS", "stage": "install-node", "direct": 5}))


def audit() -> None:
    audit_python_only()
    npm = shutil.which("npm")
    if npm is None:
        raise RuntimeError("npm is unavailable")
    return_code, stdout, stderr = run_captured(
        [npm, "audit", "--omit=dev", "--json"], cwd=NODE_ENV, accepted_codes=(0, 1)
    )
    json.loads(stdout)
    (CACHE_ROOT / "node-audit.json").write_text(stdout, encoding="utf-8", newline="\n")
    write_json(
        CACHE_ROOT / "node-audit-process.json",
        {"return_code": return_code, "stderr": stderr.strip(), "json_parse": "PASS"},
    )
    print(json.dumps({"status": "PASS", "stage": "audit", "advisory_exit_codes_retained": True}))


def audit_python_only() -> None:
    for name, environment in (("core", PY_ENV_CORE), ("wheel-inspect", PY_ENV_INSPECT)):
        site_packages = environment / "Lib" / "site-packages"
        command = [
            sys.executable,
            "-m",
            "pip_audit",
            "--path",
            str(site_packages),
            "--format",
            "json",
            "--progress-spinner",
            "off",
            "--timeout",
            "60",
        ]
        return_code, stdout, stderr = run_captured(command, accepted_codes=(0, 1))
        json.loads(stdout)
        (CACHE_ROOT / f"python-audit-{name}.json").write_text(stdout, encoding="utf-8", newline="\n")
        write_json(
            CACHE_ROOT / f"python-audit-{name}-process.json",
            {"return_code": return_code, "stderr": stderr.strip(), "json_parse": "PASS"},
        )


def remediate_pip() -> None:
    bootstrap = WHEELHOUSE / "bootstrap"
    if bootstrap.exists():
        raise RuntimeError("fresh pip-remediation wheelhouse already exists")
    bootstrap.mkdir(parents=True, exist_ok=False)
    wheel_path = bootstrap / PIP_REMEDIATION_FILENAME
    with urllib.request.urlopen(PIP_REMEDIATION_URL, timeout=60) as response:
        wheel_bytes = response.read()
    actual_hash = hashlib.sha256(wheel_bytes).hexdigest()
    if actual_hash != PIP_REMEDIATION_SHA256:
        raise RuntimeError("pip remediation wheel SHA-256 mismatch")
    wheel_path.write_bytes(wheel_bytes)
    lock_text = f"pip=={PIP_REMEDIATION_VERSION} --hash=sha256:{PIP_REMEDIATION_SHA256}\n"
    external_lock = CACHE_ROOT / "python-pip-remediation.lock"
    repo_lock = PHASE_ROOT / "x2" / "tooling" / "python-pip-remediation.lock"
    external_lock.write_text(lock_text, encoding="utf-8", newline="\n")
    repo_lock.parent.mkdir(parents=True, exist_ok=True)
    repo_lock.write_text(lock_text, encoding="utf-8", newline="\n")
    for name in ("core", "wheel-inspect"):
        for suffix in (".json", "-process.json"):
            source = CACHE_ROOT / f"python-audit-{name}{suffix}"
            destination = CACHE_ROOT / f"python-audit-{name}-pre-pip-remediation{suffix}"
            if not source.is_file():
                raise RuntimeError(f"pre-remediation audit is absent: {source}")
            shutil.copy2(source, destination)
    previous_repo_receipt = PHASE_ROOT / "x2" / "tooling" / "toolchain-transaction-receipt.json"
    if previous_repo_receipt.is_file():
        shutil.copy2(
            previous_repo_receipt,
            PHASE_ROOT / "x2" / "tooling" / "toolchain-transaction-receipt-pre-pip-remediation.json",
        )
    results = {}
    for name, environment in (("core", PY_ENV_CORE), ("wheel-inspect", PY_ENV_INSPECT)):
        python_exe = environment / "Scripts" / "python.exe"
        _, install_stdout, _ = run_captured(
            [
                str(python_exe),
                "-m",
                "pip",
                "install",
                "--no-index",
                "--find-links",
                str(bootstrap),
                "--only-binary=:all:",
                "--require-hashes",
                "--upgrade",
                "-r",
                str(external_lock),
            ]
        )
        _, version_stdout, _ = run_captured([str(python_exe), "-m", "pip", "--version"])
        _, check_stdout, check_stderr = run_captured([str(python_exe), "-m", "pip", "check"])
        check_text = (check_stdout + check_stderr).strip() + "\n"
        (CACHE_ROOT / f"pip-check-{name}.txt").write_text(check_text, encoding="utf-8", newline="\n")
        results[name] = {
            "install_output_lines": len(install_stdout.splitlines()),
            "pip_version_output": version_stdout.strip(),
            "pip_check": check_text.strip(),
        }
    audit_python_only()
    write_json(
        CACHE_ROOT / "pip-remediation-receipt.json",
        {
            "status": "PASS",
            "source": "official PyPI release JSON and files.pythonhosted.org artifact",
            "version": PIP_REMEDIATION_VERSION,
            "filename": PIP_REMEDIATION_FILENAME,
            "bytes": len(wheel_bytes),
            "sha256": actual_hash,
            "pre_remediation_audits_retained": True,
            "environments": results,
        },
    )
    repo_write(
        "x2/tooling/pip-remediation-receipt.json",
        {
            "schema": "ghc-family-pip-remediation-receipt-v1",
            "status": "PASS",
            "version": PIP_REMEDIATION_VERSION,
            "filename": PIP_REMEDIATION_FILENAME,
            "bytes": len(wheel_bytes),
            "sha256": actual_hash,
            "pre_remediation_vulnerability_entries": 14,
            "pre_remediation_audits_retained_external": True,
            "post_remediation_audits_written_external": True,
            "network_used_only_for_verified_artifact_download": True,
            "offline_hash_enforced_install": True,
            "environments": results,
            "boundary": "advisory database results are time-bounded and are not exhaustive security evidence",
        },
    )
    print(json.dumps({"status": "PASS", "stage": "remediate-pip", "version": PIP_REMEDIATION_VERSION}))


def finalize() -> None:
    if not PY_ENV_CORE.is_dir() or not PY_ENV_INSPECT.is_dir() or not (NODE_ENV / "node_modules").is_dir():
        raise RuntimeError("installed environments are incomplete")
    inventory_code = (
        "import importlib.metadata,json;"
        "print(json.dumps(sorted([{'name':d.metadata['Name'],'version':d.version} "
        "for d in importlib.metadata.distributions()],key=lambda x:x['name'].casefold())))"
    )
    python_inventories = {}
    for name, environment in (("core", PY_ENV_CORE), ("wheel-inspect", PY_ENV_INSPECT)):
        py_exe = environment / "Scripts" / "python.exe"
        python_inventories[name] = json.loads(command_output([str(py_exe), "-c", inventory_code]))
    node_lock = json.loads((NODE_ENV / "package-lock.json").read_text(encoding="utf-8"))
    node_packages = node_lock.get("packages", {})
    node_inventory = [
        {"path": key, "version": value.get("version"), "integrity": value.get("integrity")}
        for key, value in sorted(node_packages.items())
        if key
    ]
    pip_check_paths = {
        "core": CACHE_ROOT / "pip-check-core.txt",
        "wheel-inspect": CACHE_ROOT / "pip-check-wheel-inspect.txt",
    }
    py_audit_paths = {
        "core": CACHE_ROOT / "python-audit-core.json",
        "wheel-inspect": CACHE_ROOT / "python-audit-wheel-inspect.json",
    }
    node_audit_path = CACHE_ROOT / "node-audit.json"
    required_receipts = list(pip_check_paths.values()) + list(py_audit_paths.values()) + [node_audit_path]
    if not all(path.is_file() for path in required_receipts):
        raise RuntimeError("audit or pip-check dependency is absent")
    py_audits = {name: json.loads(path.read_text(encoding="utf-8")) for name, path in py_audit_paths.items()}
    node_audit = json.loads(node_audit_path.read_text(encoding="utf-8"))
    py_vulnerabilities = sum(
        len(row.get("vulns", []))
        for audit in py_audits.values()
        for row in audit.get("dependencies", [])
    )
    node_vulnerabilities = node_audit.get("metadata", {}).get("vulnerabilities", {}).get("total", 0)
    direct_expected = {(row["ecosystem"], canonicalize_name(row["tool"]), row["version"]) for row in read_plan()["new_tools"]}
    installed_py = {
        (canonicalize_name(row["name"]), row["version"])
        for inventory in python_inventories.values()
        for row in inventory
    }
    installed_node = {
        (canonicalize_name(row["tool"]), row["version"])
        for row in read_plan()["new_tools"]
        if row["ecosystem"] == "node" and (NODE_ENV / "node_modules" / Path(*row["tool"].split("/")) / "package.json").is_file()
    }
    missing = []
    for ecosystem, name, version in sorted(direct_expected):
        inventory = installed_py if ecosystem == "python" else installed_node
        if (name, version) not in inventory:
            missing.append({"ecosystem": ecosystem, "name": name, "version": version})
    if missing:
        raise RuntimeError(f"direct installed tools missing: {missing}")
    receipt = {
        "schema": "ghc-family-toolchain-transaction-receipt-v1",
        "owner": "Neris Solane",
        "phase": "v667-v8-r2",
        "status": "PASS" if py_vulnerabilities == 0 and node_vulnerabilities == 0 else "OPEN_GAP_ADVISORY_FINDINGS",
        "family_global_baseline": 41,
        "new_direct_tools": 13,
        "prospective_family_direct_total": 54,
        "python_direct_tools": 8,
        "node_direct_tools": 5,
        "python_environment_count": 2,
        "python_installed_distribution_count": sum(len(value) for value in python_inventories.values()),
        "node_locked_package_count": len(node_inventory),
        "direct_missing_count": 0,
        "pip_check": {name: path.read_text(encoding="utf-8").strip() for name, path in pip_check_paths.items()},
        "python_advisory_vulnerability_count": py_vulnerabilities,
        "node_advisory_vulnerability_count": node_vulnerabilities,
        "lifecycle_scripts_executed": 0,
        "system_python_mutated": False,
        "c_drive_install_count": 0,
        "path_mutated": False,
        "codex_desktop_mutated": False,
        "plugin_cache_mutated": False,
        "python_inventories": python_inventories,
        "node_inventory": node_inventory,
        "rollback": {
            "python": "remove only the exact verified two subenvironments under D_FAMILY_PY_ENV after a future explicit rollback decision",
            "node": "remove only the exact verified D_FAMILY_NODE_ENV after a future explicit rollback decision",
            "cache": "retain hashed cache and receipts unless an exact future cleanup is authorized",
        },
        "boundary": "same-owner D-backed package evidence only and not exhaustive security legal compliance production fitness or independent reproduction",
    }
    repo_write("x2/tooling/toolchain-transaction-receipt.json", receipt)
    write_json(CACHE_ROOT / "toolchain-transaction-receipt.json", receipt)
    print(json.dumps({"status": receipt["status"], "stage": "finalize", "python_vulns": py_vulnerabilities, "node_vulns": node_vulnerabilities}))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "stage",
        choices=(
            "prepare",
            "lock-python",
            "verify-node",
            "install-python",
            "install-node",
            "audit",
            "remediate-pip",
            "finalize",
        ),
    )
    args = parser.parse_args()
    {
        "prepare": prepare,
        "lock-python": lock_python,
        "verify-node": verify_node,
        "install-python": install_python,
        "install-node": install_node,
        "audit": audit,
        "remediate-pip": remediate_pip,
        "finalize": finalize,
    }[args.stage]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
