"""Build a D-isolated, hash-recorded Vesper v669-v8 toolchain.

Only the three frozen direct packages and their resolver-selected wheel
dependencies are downloaded.  Installation is confined to the caller-supplied
phase root.  The script never changes global Python, npm, Windows, Codex,
environment-variable, registry, or security configuration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from email.parser import BytesParser
from pathlib import Path
from typing import Any

DIRECT = {
    "pint": {
        "version": "0.25.3",
        "wheel": "pint-0.25.3-py3-none-any.whl",
        "sha256": "27eb25143bd5de9fcc4d5a4b484f16faf6b4615aa93ece6b3373a8c1a3c1b97d",
    },
    "transitions": {
        "version": "0.9.3",
        "wheel": "transitions-0.9.3-py2.py3-none-any.whl",
        "sha256": "02463248f2b668d86f66636b1e3c9e8de84d93e22915247f4e1aa9ee1cae28aa",
    },
    "portion": {
        "version": "2.6.2",
        "wheel": "portion-2.6.2-py3-none-any.whl",
        "sha256": "86be115afafa776174dc5eac82afb6496c9fa3684f5b3a844c3139535c51085e",
    },
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def run(args: list[str], *, check: bool = True, timeout: int = 300) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=check, capture_output=True, text=True, timeout=timeout)


def wheel_metadata(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as archive:
        candidates = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        if len(candidates) != 1:
            raise RuntimeError(f"unexpected METADATA count for {path.name}: {len(candidates)}")
        message = BytesParser().parsebytes(archive.read(candidates[0]))
    return {
        "filename": path.name,
        "name": str(message["Name"]),
        "version": str(message["Version"]),
        "license_expression": str(message.get("License-Expression") or "not_declared"),
        "license_field": str(message.get("License") or "not_declared")[:300],
        "requires_dist": list(message.get_all("Requires-Dist") or []),
        "requires_python": str(message.get("Requires-Python") or "not_declared"),
        "sha256": digest(path),
    }


def smoke(venv_python: Path) -> list[dict[str, Any]]:
    cases = {
        "pint_positive_and_dimension_rejection": """
from pint import UnitRegistry
from pint.errors import DimensionalityError
u = UnitRegistry()
ratio = ((750 * u.gram) / (1000 * u.gram)).to_base_units().magnitude
assert abs(ratio - 0.75) < 1e-12
try:
    (1 * u.gram).to(u.second)
except DimensionalityError:
    print('positive=0.75;reject=dimensionality')
else:
    raise AssertionError('dimension mismatch accepted')
""",
        "transitions_positive_and_forbidden_transition": """
from transitions import Machine, MachineError
class Model: pass
model = Model()
Machine(model=model, states=['planned', 'mixing', 'bulk'], transitions=[['start', 'planned', 'mixing'], ['transfer', 'mixing', 'bulk']], initial='planned')
model.start(); model.transfer(); assert model.state == 'bulk'
try:
    model.start()
except MachineError:
    print('positive=bulk;reject=forbidden-transition')
else:
    raise AssertionError('forbidden transition accepted')
""",
        "portion_positive_and_outside_rejection": """
import portion as P
window = P.closed(18, 24)
assert 20 in window and 30 not in window
assert P.open(18, 24) != window
print('positive=20-in-window;reject=30-outside')
""",
    }
    rows: list[dict[str, Any]] = []
    for name, code in cases.items():
        result = run([str(venv_python), "-c", code])
        rows.append({"case": name, "exit_code": result.returncode, "passed": result.returncode == 0, "stdout": result.stdout.strip()})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    receipt_path = args.receipt.resolve()
    if root.drive.upper() != "D:":
        raise ValueError("toolchain root must be D-backed")
    if root.exists():
        raise FileExistsError("phase toolchain root already exists; inspect before any retry")
    wheelhouse = root / "wheelhouse"
    venv = root / "venv"
    wheelhouse.mkdir(parents=True)

    pins = [f"{name}=={row['version']}" for name, row in DIRECT.items()]
    download = run([
        sys.executable,
        "-m",
        "pip",
        "download",
        "--disable-pip-version-check",
        "--only-binary=:all:",
        "--dest",
        str(wheelhouse),
        *pins,
    ])
    wheels = sorted(wheelhouse.glob("*.whl"))
    metadata = [wheel_metadata(path) for path in wheels]
    by_filename = {row["filename"].lower(): row for row in metadata}
    direct_checks = []
    for name, expected in DIRECT.items():
        actual = by_filename.get(expected["wheel"].lower())
        direct_checks.append({
            "name": name,
            "expected_filename": expected["wheel"],
            "expected_sha256": expected["sha256"],
            "observed_sha256": None if actual is None else actual["sha256"],
            "passed": actual is not None and actual["sha256"] == expected["sha256"],
        })
    if not all(row["passed"] for row in direct_checks):
        raise RuntimeError(f"direct wheel hash mismatch: {direct_checks}")

    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True, timeout=300)
    venv_python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    install = run([
        str(venv_python),
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "--no-index",
        "--find-links",
        str(wheelhouse),
        *pins,
    ])
    pip_check = run([str(venv_python), "-m", "pip", "check"])
    inventory = json.loads(run([str(venv_python), "-m", "pip", "list", "--format=json"]).stdout)

    lock_path = root / "requirements-hashed.txt"
    lock_lines = [f"{row['name']}=={row['version']} --hash=sha256:{row['sha256']}" for row in sorted(metadata, key=lambda item: item["name"].lower())]
    lock_path.write_text("\n".join(lock_lines) + "\n", encoding="utf-8", newline="\n")
    audit = run([
        sys.executable,
        "-m",
        "pip_audit",
        "-r",
        str(lock_path),
        "--require-hashes",
        "--no-deps",
        "--disable-pip",
        "--format=json",
    ], check=False, timeout=300)
    try:
        audit_json: Any = json.loads(audit.stdout)
    except json.JSONDecodeError:
        audit_json = {"parse_state": "invalid_json", "stdout": audit.stdout[:1000]}
    vulnerability_count = 0
    if isinstance(audit_json, dict):
        dependencies = audit_json.get("dependencies", [])
        vulnerability_count = sum(len(row.get("vulns", [])) for row in dependencies if isinstance(row, dict))
    elif isinstance(audit_json, list):
        vulnerability_count = sum(len(row.get("vulns", [])) for row in audit_json if isinstance(row, dict))

    smokes = smoke(venv_python)
    payload = {
        "schema": "ghc.family.isolated-toolchain-receipt.v3",
        "owner": "Vesper Arlen",
        "phase": "v669-v8",
        "boundary": "Phase-namespaced D-isolated Python environment only; no global or host configuration mutation and no production fitness claim.",
        "direct_packages": pins,
        "direct_hash_checks": direct_checks,
        "download_exit_code": download.returncode,
        "install_exit_code": install.returncode,
        "pip_check": {"exit_code": pip_check.returncode, "stdout": pip_check.stdout.strip()},
        "pip_audit": {"exit_code": audit.returncode, "vulnerability_count": vulnerability_count, "result": audit_json},
        "installed_inventory": inventory,
        "lock_sha256": digest(lock_path),
        "root_alias": "D_PHASE_TOOLCHAIN_ROOT",
        "rollback": "remove only the verified phase-namespaced toolchain root after preserving this receipt; shared prefixes remain untouched",
        "shared_prefix_mutations": 0,
        "smokes": smokes,
        "wheel_count": len(metadata),
        "wheel_metadata": metadata,
        "passed": all(row["passed"] for row in direct_checks) and pip_check.returncode == 0 and audit.returncode == 0 and vulnerability_count == 0 and all(row["passed"] for row in smokes),
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    if not payload["passed"]:
        raise RuntimeError("isolated toolchain gates did not all pass; inspect retained receipt")


if __name__ == "__main__":
    main()
