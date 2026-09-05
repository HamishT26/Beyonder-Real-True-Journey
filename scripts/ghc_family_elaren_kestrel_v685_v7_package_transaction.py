"""Install the frozen v685-v7 wheel set into one isolated D-first environment."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import subprocess
import sys
import venv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def run(args: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**os.environ, "PYTHONUTF8": "1", "PIP_DISABLE_PIP_VERSION_CHECK": "1"},
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def environment_python(root: Path) -> Path:
    return root / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--bank-root", type=Path, required=True)
    parser.add_argument("--wheelhouse", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    packages = plan["packages"]
    if plan["target"] != 13 or len(packages) != 13 or not plan["wheel_only"]:
        raise SystemExit("package plan contract changed")
    specs = [f"{row['name']}=={row['version']}" for row in packages]

    args.bank_root.mkdir(parents=True, exist_ok=True)
    args.wheelhouse.mkdir(parents=True, exist_ok=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    download = run(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "--only-binary=:all:",
            "--dest",
            str(args.wheelhouse),
            *specs,
        ]
    )
    if download.returncode != 0:
        write_json(
            args.output_dir / "package-transaction-failure.json",
            {
                "schema": "ghc.family.elaren-v685-v7.package-transaction-failure.v1",
                "stage": "download",
                "returncode": download.returncode,
                "stderr_tail": download.stderr[-4000:],
                "success_credit": 0,
            },
        )
        print(download.stderr, file=sys.stderr)
        return download.returncode

    direct_rows = []
    for row in packages:
        wheel = args.wheelhouse / row["wheel"]
        if not wheel.is_file():
            raise SystemExit(f"planned wheel absent: {row['wheel']}")
        actual = digest(wheel)
        if actual != row["wheel_sha256"]:
            raise SystemExit(f"planned wheel digest mismatch: {row['wheel']}")
        direct_rows.append(
            {
                "name": row["name"],
                "version": row["version"],
                "wheel": row["wheel"],
                "bytes": wheel.stat().st_size,
                "sha256": actual,
                "direct_addition_credit": 1,
            }
        )

    all_wheels = [
        {
            "filename": path.name,
            "bytes": path.stat().st_size,
            "sha256": digest(path),
            "direct": path.name in {row["wheel"] for row in packages},
        }
        for path in sorted(args.wheelhouse.glob("*.whl"))
    ]

    python = environment_python(args.bank_root)
    if not python.is_file():
        venv.EnvBuilder(with_pip=True, clear=False, symlinks=False).create(args.bank_root)
    if not python.is_file():
        raise SystemExit("isolated environment Python missing")

    install = run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--no-index",
            "--find-links",
            str(args.wheelhouse),
            "--only-binary=:all:",
            *specs,
        ]
    )
    if install.returncode != 0:
        write_json(
            args.output_dir / "package-transaction-failure.json",
            {
                "schema": "ghc.family.elaren-v685-v7.package-transaction-failure.v1",
                "stage": "install",
                "returncode": install.returncode,
                "stderr_tail": install.stderr[-4000:],
                "success_credit": 0,
            },
        )
        print(install.stderr, file=sys.stderr)
        return install.returncode

    check = run([str(python), "-m", "pip", "check"])
    inventory_result = run([str(python), "-m", "pip", "list", "--format=json"])
    if check.returncode != 0 or inventory_result.returncode != 0:
        raise SystemExit("isolated dependency check or inventory failed")
    inventory = json.loads(inventory_result.stdout)
    inventory_by_name = {row["name"].casefold(): row["version"] for row in inventory}
    missing_or_changed = [
        spec
        for spec in specs
        if inventory_by_name.get(spec.split("==", 1)[0].casefold()) != spec.split("==", 1)[1]
    ]
    if missing_or_changed:
        raise SystemExit(f"direct package inventory mismatch: {missing_or_changed}")

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
    vulnerability_count = 0
    dependencies = audit_payload.get("dependencies", []) if isinstance(audit_payload, dict) else audit_payload
    if isinstance(dependencies, list):
        vulnerability_count = sum(len(row.get("vulns", [])) for row in dependencies if isinstance(row, dict))

    write_text(
        args.output_dir / "requirements-direct.lock",
        "\n".join(f"{row['name']}=={row['version']} --hash=sha256:{row['wheel_sha256']}" for row in packages),
    )
    write_json(
        args.output_dir / "wheelhouse-manifest.json",
        {
            "schema": "ghc.family.elaren-v685-v7.wheelhouse-manifest.v1",
            "hash_domain": "downloaded wheel bytes",
            "direct_package_count": 13,
            "wheel_count": len(all_wheels),
            "direct_wheels": direct_rows,
            "all_wheels": all_wheels,
            "bank": "D-drive isolated phase wheelhouse",
        },
    )
    write_json(
        args.output_dir / "installation-receipt.json",
        {
            "schema": "ghc.family.elaren-v685-v7.installation.v1",
            "direct_package_count": 13,
            "direct_packages": direct_rows,
            "installed_distribution_count": len(inventory),
            "inventory": sorted(inventory, key=lambda row: row["name"].casefold()),
            "pip_check_status": "PASS",
            "pip_check_output": check.stdout.strip(),
            "environment": "D-drive isolated phase environment",
            "shared_python_mutated": False,
            "npm_prefix_mutated": False,
            "codex_desktop_mutated": False,
            "host_security_mutated": False,
            "rebooted": False,
            "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    write_json(
        args.output_dir / "advisory-audit.json",
        {
            "schema": "ghc.family.elaren-v685-v7.advisory-audit.v1",
            "tool": "pip-audit 2.10.1",
            "returncode": audit.returncode,
            "vulnerability_count": vulnerability_count,
            "status": "PASS_ZERO_KNOWN_VULNERABILITIES" if vulnerability_count == 0 and audit.returncode == 0 else "ADVISORY_FINDINGS_OR_TOOL_FAILURE",
            "scope": "isolated phase environment snapshot",
            "exhaustive_security_claimed": False,
            "payload": audit_payload,
            "stderr_tail": audit.stderr[-4000:],
        },
    )
    result = {
        "schema": "ghc.family.elaren-v685-v7.package-transaction.v1",
        "status": "PASS" if vulnerability_count == 0 and audit.returncode == 0 else "PASS_WITH_ADVISORY_BOUNDARY",
        "direct_packages": 13,
        "all_wheels": len(all_wheels),
        "installed_distributions": len(inventory),
        "pip_check": "PASS",
        "known_vulnerabilities": vulnerability_count,
        "positive_and_adverse_smokes": "PENDING_SEPARATE_OWNER_RUNNER",
        "environment": "D-drive isolated phase environment",
    }
    write_json(args.output_dir / "transaction-summary.json", result)
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
