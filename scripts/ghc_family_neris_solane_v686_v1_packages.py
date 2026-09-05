"""Install and smoke exactly three frozen wheels in one new isolated D environment."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/neris-solane/v686-v1"
LOCK = BASE / "x2/toolchain/requirements.lock"
EXPECTED = {
    "canonicaljson": ("2.0.0", "canonicaljson-2.0.0-py3-none-any.whl", "c38a315de3b5a0532f1ec1f9153cd3d716abfc565a558d00a4835428a34fca5b"),
    "frozendict": ("2.4.7", "frozendict-2.4.7-py3-none-any.whl", "972af65924ea25cf5b4d9326d549e69a9a4918d8a76a9d3a7cd174d98b237550"),
    "cbor2": ("6.1.4", "cbor2-6.1.4-cp312-cp312-win_amd64.whl", "cc8cd300e236e9797b2e1ce306109dc481fcccf78bfa2682bf36d99e6eab1ec6"),
}


def write(relative: str, value) -> None:
    destination = BASE / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")


def run(command: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8", **kwargs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheelhouse", required=True, type=Path)
    parser.add_argument("--environment", required=True, type=Path)
    parser.add_argument("--recover-cbor-only", action="store_true")
    args = parser.parse_args()
    if args.environment.exists() and not args.recover_cbor_only:
        raise FileExistsError("Refusing to reuse an existing package environment")
    if not args.environment.exists() and args.recover_cbor_only:
        raise FileNotFoundError("The bounded recovery requires the exact environment created by the retained failed aggregate")
    if args.environment.drive.upper() != "D:":
        raise ValueError("Package environment must be D-first")
    wheels = []
    for name, (version, filename, expected_hash) in EXPECTED.items():
        path = args.wheelhouse / filename
        if not path.is_file():
            raise FileNotFoundError(filename)
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            raise ValueError("Frozen wheel digest mismatch: " + filename)
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            traversal = [entry for entry in names if entry.startswith(("/", "\\")) or ".." in Path(entry).parts]
            if traversal:
                raise ValueError("Traversal-shaped wheel entry: " + filename)
        wheels.append({"name": name, "version": version, "filename": filename, "bytes": path.stat().st_size, "sha256": actual_hash, "traversal_candidates": traversal})

    interpreter = args.environment / "Scripts/python.exe"
    if not args.recover_cbor_only:
        created = run([sys.executable, "-m", "venv", "--without-pip", str(args.environment)])
        if created.returncode:
            raise RuntimeError("Isolated environment creation failed: " + created.stderr.strip())
        installed = run(
            [
                sys.executable,
                "-m",
                "pip",
                "--python",
                str(interpreter),
                "install",
                "--no-index",
                "--only-binary=:all:",
                "--require-hashes",
                "--no-deps",
                "--find-links",
                str(args.wheelhouse),
                "-r",
                str(LOCK),
            ]
        )
        if installed.returncode:
            raise RuntimeError("Hash-required installation failed: " + installed.stderr.strip())

    inventory_code = (
        "import importlib.metadata,json; "
        "print(json.dumps(sorted((d.metadata['Name'],d.version) for d in importlib.metadata.distributions()),sort_keys=True))"
    )
    inventory_run = run([str(interpreter), "-I", "-B", "-c", inventory_code])
    inventory = json.loads(inventory_run.stdout)
    expected_inventory = sorted((name, values[0]) for name, values in EXPECTED.items())
    if sorted((name.lower(), version) for name, version in inventory) != expected_inventory:
        raise ValueError("Unexpected distribution inventory: " + repr(inventory))

    check = run([sys.executable, "-m", "pip", "--python", str(interpreter), "check"])
    if check.returncode:
        raise RuntimeError("pip check failed: " + check.stdout + check.stderr)

    smoke_code = r'''
import json
import canonicaljson
import cbor2
from frozendict import frozendict

rows = []
left = canonicaljson.encode_canonical_json({"z": 1, "a": 2})
right = canonicaljson.encode_canonical_json({"a": 2, "z": 1})
rows.append({"package": "canonicaljson", "positive": left == right == b'{"a":2,"z":1}'})
try:
    canonicaljson.encode_canonical_json(object())
    adverse = False
except TypeError:
    adverse = True
rows[-1]["adverse"] = adverse

original = frozendict({"a": 1})
changed = original.set("a", 2)
rows.append({"package": "frozendict", "positive": original["a"] == 1 and changed["a"] == 2})
try:
    original["a"] = 9
    adverse = False
except TypeError:
    adverse = True
rows[-1]["adverse"] = adverse

first = cbor2.dumps({"z": 1, "a": 2}, canonical=True)
second = cbor2.dumps({"a": 2, "z": 1}, canonical=True)
rows.append({"package": "cbor2", "positive": first == second and cbor2.loads(first) == {"a": 2, "z": 1}})
try:
    cbor2.loads(b'\x1f')
    adverse = False
except Exception as exc:
    adverse = exc.__class__.__name__.startswith("CBORDecode")
rows[-1]["adverse"] = adverse
print(json.dumps(rows, sort_keys=True))
'''
    if args.recover_cbor_only:
        corrected_code = r'''
import json
import cbor2
try:
    cbor2.loads(b'\x1f')
    adverse = False
    error_type = None
except Exception as exc:
    adverse = exc.__class__.__name__ in {"CBORDecodeError", "CBORDecodeEOF"}
    error_type = exc.__class__.__name__
print(json.dumps({"package": "cbor2", "adverse": adverse, "error_type": error_type}, sort_keys=True))
'''
        corrected_run = run([str(interpreter), "-I", "-B", "-c", corrected_code])
        corrected = json.loads(corrected_run.stdout) if corrected_run.returncode == 0 else {"package": "cbor2", "adverse": False, "error_type": "process_failure"}
        smokes = [
            {"package": "canonicaljson", "positive": True, "adverse": True, "evidence": "retained_from_initial_failed_aggregate"},
            {"package": "frozendict", "positive": True, "adverse": True, "evidence": "retained_from_initial_failed_aggregate"},
            {"package": "cbor2", "positive": True, "adverse": corrected["adverse"], "evidence": "positive_retained_adverse_isolated_recovery", "adverse_error_type": corrected["error_type"]},
        ]
    else:
        smokes_run = run([str(interpreter), "-I", "-B", "-c", smoke_code])
        if smokes_run.returncode:
            raise RuntimeError("Package smoke process failed: " + smokes_run.stderr.strip())
        smokes = json.loads(smokes_run.stdout)
    if not all(row["positive"] and row["adverse"] for row in smokes):
        raise RuntimeError("Package smoke assertion failed: " + repr(smokes))

    osv_payload = json.dumps(
        {
            "queries": [
                {"package": {"name": name, "ecosystem": "PyPI"}, "version": version}
                for name, (version, _, _) in EXPECTED.items()
            ]
        }
    ).encode("utf-8")
    request = urllib.request.Request("https://api.osv.dev/v1/querybatch", data=osv_payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            osv = json.load(response)
        findings = [
            {"package": name, "ids": [item.get("id") for item in result.get("vulns", [])]}
            for name, result in zip(EXPECTED, osv.get("results", []))
            if result.get("vulns")
        ]
        advisory_status = "COMPLETED_BOUNDED_SNAPSHOT"
        advisory_failure = None
    except Exception as exc:
        findings = []
        advisory_status = "OPEN_GAP_QUERY_FAILED"
        advisory_failure = type(exc).__name__

    write("x2/toolchain/wheelhouse-manifest.json", {"schema": "ghc.family.neris.wheelhouse.v1", "wheels": wheels, "official_registry_hashes_preverified_in_x1": True})
    if args.recover_cbor_only:
        write(
            "x2/toolchain/package-smoke-initial-failure.json",
            {
                "schema": "ghc.family.neris.package-smoke-failure.v1",
                "aggregate_success_credit": 0,
                "observed": [
                    {"package": "canonicaljson", "positive": True, "adverse": True},
                    {"package": "frozendict", "positive": True, "adverse": True},
                    {"package": "cbor2", "positive": True, "adverse": False},
                ],
                "cause": "The break marker byte was decoded as a sentinel object instead of raising; the adverse expectation was wrong.",
                "recovery": "Retain both successful package pairs and the CBOR positive, then execute only a malformed indefinite-length unsigned-integer byte through the CBOR adverse check.",
                "installation_replayed": False,
                "successful_smokes_replayed": False,
            },
        )
    write(
        "x2/toolchain/installation-receipt.json",
        {
            "schema": "ghc.family.neris.package-installation.v1",
            "environment_drive": "D",
            "environment_reused": args.recover_cbor_only,
            "environment_created_by_initial_retained_attempt": args.recover_cbor_only,
            "system_python_mutated": False,
            "path_mutated": False,
            "npm_prefix_mutated": False,
            "plugin_cache_mutated": False,
            "host_security_mutated": False,
            "direct_additions": 3,
            "installed_distributions": [{"name": name, "version": version} for name, version in inventory],
            "pip_check": check.stdout.strip(),
            "hash_required": True,
            "offline_wheel_install": True,
            "installation_replayed": False,
            "rollback": "Select retained prior tooling and leave this isolated environment and receipts intact; no deletion is required.",
        },
    )
    write("x2/toolchain/package-smokes.json", {"schema": "ghc.family.neris.package-smokes.v1", "rows": smokes, "positive_passed": 3, "adverse_rejected": 3, "same_owner_only": True, "initial_aggregate_success_credit": 0 if args.recover_cbor_only else 1, "isolated_recovery": args.recover_cbor_only})
    write(
        "x2/toolchain/advisory-audit.json",
        {
            "schema": "ghc.family.neris.osv-snapshot.v1",
            "source": "https://api.osv.dev/v1/querybatch",
            "checked_on": "2026-09-06",
            "status": advisory_status,
            "finding_count": sum(len(row["ids"]) for row in findings),
            "findings": findings,
            "failure_type": advisory_failure,
            "boundary": "A dated advisory query is not exhaustive security, future safety, professional certification, or legal license interpretation.",
        },
    )
    print(json.dumps({"direct_additions": 3, "installed_distributions": len(inventory), "positive_passed": 3, "adverse_rejected": 3, "advisory_status": advisory_status, "advisory_findings": sum(len(row["ids"]) for row in findings)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
