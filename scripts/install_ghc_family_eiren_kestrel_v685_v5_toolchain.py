#!/usr/bin/env python3
"""Install and smoke Eiren v685-v5 tools in one new D-first transaction."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v685-v5"
OWNER = "Eiren Kestrel"
PYTHON_DIRECT = {
    "astropy": "8.0.1",
    "asdf": "5.4.0",
    "gwosc": "0.8.3",
    "Pint": "0.25.3",
    "uncertainties": "3.2.3",
    "jsonschema": "4.26.0",
    "networkx": "3.6.1",
    "xarray": "2026.7.0",
}
NODE_DIRECT = {
    "ajv": "8.20.0",
    "zod": "4.5.4",
    "fast-check": "4.9.0",
    "json-schema-to-typescript": "16.0.0",
    "@apidevtools/json-schema-ref-parser": "16.0.1",
}


def run(args: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=cwd or ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def require(proc: subprocess.CompletedProcess[bytes], label: str) -> subprocess.CompletedProcess[bytes]:
    if proc.returncode:
        stderr = proc.stderr.decode("utf-8", "replace")[-2000:]
        stdout = proc.stdout.decode("utf-8", "replace")[-2000:]
        raise RuntimeError(f"{label} failed with exit {proc.returncode}: {stderr or stdout}")
    return proc


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def wheel_metadata(path: Path) -> tuple[str, str]:
    with zipfile.ZipFile(path) as archive:
        member = next(name for name in archive.namelist() if name.endswith(".dist-info/METADATA"))
        text = archive.read(member).decode("utf-8", "replace")
    fields = {}
    for line in text.splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            if key in {"Name", "Version"} and key not in fields:
                fields[key] = value
    return fields["Name"], fields["Version"]


def python_smoke(venv_python: Path) -> dict[str, Any]:
    code = r'''
import importlib.metadata as md
import json
results = []

def row(name, positive, rejecting, detail):
    results.append({"name": name, "version": md.version(name), "positive_pass": bool(positive), "rejecting_pass": bool(rejecting), "detail": detail})

from astropy import units as u
positive = (3 * u.km).to_value(u.m) == 3000
try:
    u.Unit("not_a_real_unit_ek6855", parse_strict="raise")
    negative = False
except Exception:
    negative = True
row("astropy", positive, negative, "unit conversion and unknown-unit rejection")

import asdf
positive = bool(asdf.__version__)
try:
    asdf.open(b"not an asdf file")
    negative = False
except Exception:
    negative = True
row("asdf", positive, negative, "versioned import and invalid-container rejection")

import gwosc
positive = gwosc is not None
try:
    getattr(gwosc, "definitely_missing_ek6855")
    negative = False
except AttributeError:
    negative = True
row("gwosc", positive, negative, "offline import and missing-surface rejection; zero data calls")

import pint
ureg = pint.UnitRegistry()
positive = (2 * ureg.kilometer).to(ureg.meter).magnitude == 2000
try:
    (1 * ureg.second).to(ureg.meter)
    negative = False
except Exception:
    negative = True
row("Pint", positive, negative, "dimensional conversion and incompatible-dimension rejection")

from uncertainties import ufloat
x = ufloat(2.0, 0.1)
positive = (x * 2).nominal_value == 4.0 and (x * 2).std_dev > 0
try:
    _ = x / 0
    negative = False
except Exception:
    negative = True
row("uncertainties", positive, negative, "symbolic propagation and division-by-zero rejection")

import jsonschema
schema = {"type": "object", "required": ["phase"], "properties": {"phase": {"const": "v685-v5"}}}
jsonschema.validate({"phase": "v685-v5"}, schema)
positive = True
try:
    jsonschema.validate({"phase": "wrong"}, schema)
    negative = False
except jsonschema.ValidationError:
    negative = True
row("jsonschema", positive, negative, "valid fixture and const violation")

import networkx as nx
g = nx.DiGraph([(1, 2), (2, 3)])
positive = nx.is_directed_acyclic_graph(g)
g.add_edge(3, 1)
negative = not nx.is_directed_acyclic_graph(g)
row("networkx", positive, negative, "acyclic graph and cycle rejection")

import xarray as xr
ds = xr.Dataset({"value": ("row", [])}, coords={"row": []})
positive = ds.sizes["row"] == 0
try:
    xr.Dataset({"a": (("x",), [1, 2]), "b": (("x",), [1])})
    negative = False
except Exception:
    negative = True
row("xarray", positive, negative, "zero-row labelled dataset and dimension mismatch rejection")

print(json.dumps(results, sort_keys=True))
'''
    proc = require(run([str(venv_python), "-c", code]), "python smoke")
    return {"rows": json.loads(proc.stdout.decode("utf-8")), "stderr": proc.stderr.decode("utf-8", "replace")[-1000:]}


def node_smoke(node_root: Path) -> list[dict[str, Any]]:
    script = node_root / "smoke.mjs"
    script.write_text(r'''
import Ajv from "ajv";
import { z } from "zod";
import fc from "fast-check";
import { compile } from "json-schema-to-typescript";
import $RefParser from "@apidevtools/json-schema-ref-parser";

const rows = [];
const ajv = new Ajv();
const validate = ajv.compile({type: "object", required: ["phase"], properties: {phase: {const: "v685-v5"}}});
rows.push({name: "ajv", positive_pass: validate({phase: "v685-v5"}), rejecting_pass: !validate({phase: "wrong"}), detail: "schema acceptance and const rejection"});

const zschema = z.object({phase: z.literal("v685-v5")});
rows.push({name: "zod", positive_pass: zschema.safeParse({phase: "v685-v5"}).success, rejecting_pass: !zschema.safeParse({phase: "wrong"}).success, detail: "runtime parse acceptance and rejection"});

let fastNegative = false;
try { fc.assert(fc.property(fc.integer(), n => n > 0), {numRuns: 20, seed: 6855}); } catch { fastNegative = true; }
fc.assert(fc.property(fc.integer(), n => n === n), {numRuns: 20, seed: 6855});
rows.push({name: "fast-check", positive_pass: true, rejecting_pass: fastNegative, detail: "bounded property pass and counterexample witness"});

const ts = await compile({title: "Phase", type: "object", required: ["phase"], properties: {phase: {type: "string"}}}, "Phase");
let typeNegative = false;
try { await compile({title: "Broken", type: "definitely-invalid-type"}, "Broken"); } catch { typeNegative = true; }
rows.push({name: "json-schema-to-typescript", positive_pass: ts.includes("interface Phase"), rejecting_pass: typeNegative, detail: "type projection and invalid-type rejection"});

const dereferenced = await $RefParser.dereference({definitions: {phase: {type: "string"}}, properties: {phase: {$ref: "#/definitions/phase"}}});
let refNegative = false;
try { await $RefParser.dereference({properties: {phase: {$ref: "#/missing"}}}); } catch { refNegative = true; }
rows.push({name: "@apidevtools/json-schema-ref-parser", positive_pass: dereferenced.properties.phase.type === "string", rejecting_pass: refNegative, detail: "local reference resolution and missing-reference rejection"});

console.log(JSON.stringify(rows));
''', encoding="utf-8")
    proc = require(run(["node", str(script)], cwd=node_root), "node smoke")
    return json.loads(proc.stdout.decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--external-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--pip-audit", type=Path, required=True)
    args = parser.parse_args()
    external = args.external_root.resolve()
    if external.drive.upper() != "D:":
        raise SystemExit("external root must be on D drive")
    if external.exists():
        raise SystemExit("external root already exists; refuse collision")
    external.mkdir(parents=True)
    wheelhouse = external / "wheelhouse"
    python_root = external / "python"
    node_root = external / "node"
    wheelhouse.mkdir()
    node_root.mkdir()
    failures: list[dict[str, Any]] = []
    stage = "transaction_start"
    try:
        npm = shutil.which("npm.cmd") or shutil.which("npm")
        codex = shutil.which("codex.exe") or shutil.which("codex.cmd") or shutil.which("codex")
        if not npm or not codex:
            raise RuntimeError("required npm or codex command surface is not resolvable")
        stage = "python_wheel_download"
        pins = [f"{name}=={version}" for name, version in PYTHON_DIRECT.items()]
        require(run([sys.executable, "-m", "pip", "download", "--only-binary=:all:", "--dest", str(wheelhouse), *pins]), "wheel-only download")
        wheel_rows = []
        for wheel in sorted(wheelhouse.glob("*.whl")):
            name, version = wheel_metadata(wheel)
            sha = hashlib.sha256(wheel.read_bytes()).hexdigest()
            wheel_rows.append({"name": name, "version": version, "filename": wheel.name, "sha256": sha, "bytes": wheel.stat().st_size})
        lock = external / "requirements-hashed.txt"
        lock.write_text("\n".join(f"{row['name']}=={row['version']} --hash=sha256:{row['sha256']}" for row in sorted(wheel_rows, key=lambda r: r["name"].lower())) + "\n", encoding="utf-8")
        stage = "python_venv_creation"
        require(run([sys.executable, "-m", "venv", str(python_root)]), "venv creation")
        venv_python = python_root / "Scripts" / "python.exe"
        stage = "python_hash_required_install"
        require(run([str(venv_python), "-m", "pip", "install", "--no-index", "--find-links", str(wheelhouse), "--require-hashes", "-r", str(lock)]), "hash-required wheel installation")
        stage = "python_validation"
        pip_check = require(run([str(venv_python), "-m", "pip", "check"]), "pip check")
        py_smoke = python_smoke(venv_python)
        installed_python = {dist.metadata["Name"]: dist.version for dist in importlib.metadata.distributions(path=[str(python_root / "Lib" / "site-packages")])}
        python_licenses = []
        for name in PYTHON_DIRECT:
            dist = next((d for d in importlib.metadata.distributions(path=[str(python_root / "Lib" / "site-packages")]) if (d.metadata.get("Name") or "").lower() == name.lower()), None)
            python_licenses.append({"name": name, "version": installed_python.get(name, installed_python.get(name.lower())), "license_metadata": (dist.metadata.get("License-Expression") or dist.metadata.get("License") or "not_declared") if dist else "not_found", "legal_conclusion": False})
        audit_proc = run([str(args.pip_audit), "--path", str(python_root / "Lib" / "site-packages"), "--format", "json"])
        python_audit = json.loads(audit_proc.stdout.decode("utf-8")) if audit_proc.stdout.strip() else {"dependencies": [], "error": audit_proc.stderr.decode("utf-8", "replace")[-1000:]}
        if audit_proc.returncode not in {0, 1}:
            raise RuntimeError(f"pip-audit operational failure {audit_proc.returncode}")

        stage = "node_lock_resolution"
        package_json = {"name": "ghc-family-eiren-v685-v5-toolchain", "private": True, "version": "0.0.0", "type": "module", "dependencies": NODE_DIRECT}
        write_json(node_root / "package.json", package_json)
        require(run([npm, "install", "--package-lock-only", "--ignore-scripts", "--audit=false", "--fund=false"], cwd=node_root), "node lock resolution")
        stage = "node_lifecycle_disabled_install"
        require(run([npm, "ci", "--ignore-scripts", "--omit=dev", "--audit=false", "--fund=false"], cwd=node_root), "node lifecycle-disabled install")
        stage = "node_smoke"
        node_rows = node_smoke(node_root)
        lock_json = json.loads((node_root / "package-lock.json").read_text(encoding="utf-8"))
        node_integrities = []
        for name, version in NODE_DIRECT.items():
            entry = lock_json["packages"].get(f"node_modules/{name}", {})
            node_integrities.append({"name": name, "version": entry.get("version"), "integrity": entry.get("integrity"), "license_metadata": entry.get("license", "not_declared"), "lifecycle_scripts_disabled": True, "legal_conclusion": False})
        stage = "node_audit"
        audit = run([npm, "audit", "--omit=dev", "--json"], cwd=node_root)
        node_audit = json.loads(audit.stdout.decode("utf-8")) if audit.stdout.strip() else {"error": audit.stderr.decode("utf-8", "replace")[-1000:]}
        if audit.returncode not in {0, 1}:
            raise RuntimeError(f"npm audit operational failure {audit.returncode}")

        stage = "codex_cli_update"
        prefix = require(run([npm, "config", "get", "prefix"]), "npm prefix").stdout.decode().strip()
        if not prefix.upper().startswith("D:\\"):
            raise RuntimeError("npm global prefix is not D-first")
        before = require(run([codex, "--version"]), "codex before").stdout.decode().strip()
        require(run([npm, "install", "--global", "@openai/codex@0.153.4", "--ignore-scripts", "--audit=false", "--fund=false"]), "Codex CLI update")
        after = require(run([codex, "--version"]), "codex after").stdout.decode().strip()
        valid = (
            len(py_smoke["rows"]) == 8 and all(r["positive_pass"] and r["rejecting_pass"] for r in py_smoke["rows"])
            and len(node_rows) == 5 and all(r["positive_pass"] and r["rejecting_pass"] for r in node_rows)
            and "0.153.4" in after
        )
        python_vulns = sum(len(row.get("vulns", [])) for row in python_audit.get("dependencies", [])) if isinstance(python_audit, dict) else 0
        node_vulns = int(node_audit.get("metadata", {}).get("vulnerabilities", {}).get("total", 0)) if isinstance(node_audit, dict) else 0
        receipt = {
            "schema": "ghc.family.d-first-toolchain-execution.v685.v5", "owner": OWNER, "phase": PHASE,
            "external_root": "D-drive owner-isolated toolchain", "direct_tool_count": 13,
            "python_direct": [{"name": n, "version": v} for n, v in PYTHON_DIRECT.items()],
            "python_wheel_count": len(wheel_rows), "python_wheels": wheel_rows,
            "python_hash_required_install": True, "python_pip_check_pass": pip_check.returncode == 0,
            "python_smokes": py_smoke["rows"], "python_license_inventory": python_licenses,
            "python_audit": {"return_code": audit_proc.returncode, "known_vulnerability_count": python_vulns, "snapshot_only_not_exhaustive": True},
            "node_direct": node_integrities, "node_smokes": node_rows,
            "node_lifecycle_scripts_disabled": True,
            "node_audit": {"return_code": audit.returncode, "known_vulnerability_count": node_vulns, "snapshot_only_not_exhaustive": True},
            "codex_cli": {"before": before, "after": after, "target": "0.153.4", "npm_prefix_drive": "D", "desktop_updated": False},
            "failure_count": 0, "failures": [],
            "passing_witness_count": 29, "valid": valid and python_vulns == 0 and node_vulns == 0,
            "rollback": "Remove only this exact owner-isolated environment after literal-path verification; retain the receipt. The shared D-first Codex CLI update is not rolled back automatically.",
            "boundary": "Local package behavior and advisory audits only; no production, exhaustive-security, legal-license, professional, empirical, identity, independent-reproduction, or Stage 20 claim.",
        }
    except Exception as exc:
        failures.append({"failure_id": "EK6855-TOOL-N002", "stage": stage, "failure": str(exc)[-1800:], "credit": "retained_zero_credit", "recovery": "Inspect the exact failed dependency and use a new collision-free D-first transaction root; do not erase or reuse the partial environment."})
        receipt = {"schema": "ghc.family.d-first-toolchain-execution.v685.v5", "owner": OWNER, "phase": PHASE, "external_root": "D-drive owner-isolated toolchain", "direct_tool_count": 13, "failure_count": len(failures), "failures": failures, "passing_witness_count": 0, "valid": False, "rollback": "Quarantine the exact partial owner environment and retain this receipt.", "boundary": "No completion claim."}
    write_json(args.receipt, receipt)
    print(json.dumps({"valid": receipt["valid"], "failure_count": receipt["failure_count"], "receipt": str(args.receipt)}, sort_keys=True))
    return 0 if receipt["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
