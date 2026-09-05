"""Correct only the vulnerable bootstrap pip in the isolated v685-v7 environment."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PIP_VERSION = "26.2.1"
PIP_WHEEL = "pip-26.2.1-py3-none-any.whl"
PIP_SHA256 = "71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**os.environ, "PYTHONUTF8": "1", "PIP_DISABLE_PIP_VERSION_CHECK": "1"},
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank-root", type=Path, required=True)
    parser.add_argument("--wheelhouse", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    python = args.bank_root / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.is_file():
        raise SystemExit("isolated environment Python missing")

    download = run(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "--only-binary=:all:",
            "--no-deps",
            "--dest",
            str(args.wheelhouse),
            f"pip=={PIP_VERSION}",
        ]
    )
    wheel = args.wheelhouse / PIP_WHEEL
    actual = hashlib.sha256(wheel.read_bytes()).hexdigest() if wheel.is_file() else None
    if download.returncode != 0 or actual != PIP_SHA256:
        write_json(
            args.output_dir / "pip-bootstrap-recovery-failure.json",
            {
                "schema": "ghc.family.elaren-v685-v7.pip-recovery-failure.v1",
                "download_returncode": download.returncode,
                "wheel_present": wheel.is_file(),
                "expected_sha256": PIP_SHA256,
                "observed_sha256": actual,
                "success_credit": 0,
            },
        )
        return 2

    install = run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--no-index",
            "--no-deps",
            "--force-reinstall",
            str(wheel),
        ]
    )
    version = run([str(python), "-m", "pip", "--version"])
    check = run([str(python), "-m", "pip", "check"])
    site_packages = args.bank_root / ("Lib/site-packages" if os.name == "nt" else "lib")
    audit = run(
        [
            sys.executable,
            "-m",
            "pip_audit",
            "--path",
            str(site_packages),
            "--format",
            "json",
        ]
    )
    try:
        audit_payload = json.loads(audit.stdout) if audit.stdout.strip() else []
    except json.JSONDecodeError:
        audit_payload = {"unparsed_stdout_tail": audit.stdout[-4000:]}
    dependencies = audit_payload.get("dependencies", []) if isinstance(audit_payload, dict) else audit_payload
    vulnerability_count = sum(
        len(row.get("vulns", [])) for row in dependencies if isinstance(row, dict)
    ) if isinstance(dependencies, list) else -1
    passed = (
        install.returncode == 0
        and version.returncode == 0
        and f"pip {PIP_VERSION}" in version.stdout
        and check.returncode == 0
        and audit.returncode == 0
        and vulnerability_count == 0
    )
    write_json(
        args.output_dir / "pip-bootstrap-wheel.json",
        {
            "schema": "ghc.family.elaren-v685-v7.pip-bootstrap-wheel.v1",
            "name": "pip",
            "version": PIP_VERSION,
            "wheel": PIP_WHEEL,
            "bytes": wheel.stat().st_size,
            "sha256": actual,
            "source": "PyPI current stable release metadata",
            "direct_phase_package_credit": 0,
            "purpose": "isolated bootstrap vulnerability correction only",
        },
    )
    write_json(
        args.output_dir / "advisory-recovery.json",
        {
            "schema": "ghc.family.elaren-v685-v7.advisory-recovery.v1",
            "status": "PASS" if passed else "FAIL",
            "original_audit_vulnerability_count": 7,
            "original_affected_distribution": "pip 25.0.1 bootstrap only",
            "original_audit_success_credit": 0,
            "recovery_scope": "isolated bootstrap pip only",
            "recovered_pip_version": PIP_VERSION,
            "install_returncode": install.returncode,
            "pip_check_returncode": check.returncode,
            "post_recovery_audit_returncode": audit.returncode,
            "post_recovery_vulnerability_count": vulnerability_count,
            "shared_python_mutated": False,
            "direct_phase_package_count_unchanged": 13,
            "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    write_json(
        args.output_dir / "post-recovery-audit.json",
        {
            "schema": "ghc.family.elaren-v685-v7.post-recovery-audit.v1",
            "status": "PASS_ZERO_KNOWN_VULNERABILITIES" if passed else "FAIL",
            "vulnerability_count": vulnerability_count,
            "returncode": audit.returncode,
            "scope": "isolated phase environment snapshot",
            "exhaustive_security_claimed": False,
            "payload": audit_payload,
            "stderr_tail": audit.stderr[-4000:],
        },
    )
    print(
        json.dumps(
            {
                "status": "PASS" if passed else "FAIL",
                "pip": PIP_VERSION,
                "pip_check": check.returncode,
                "known_vulnerabilities": vulnerability_count,
                "direct_phase_packages": 13,
            },
            separators=(",", ":"),
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
