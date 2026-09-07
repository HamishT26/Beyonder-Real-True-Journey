#!/usr/bin/env python3
"""D-first hash-locked package transaction for Elowen Cairn v688-v5."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import urllib.request
import venv
from pathlib import Path
from typing import Any


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", check=False)


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "ghc-family-owner-package-transaction/1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def osv(name: str, version: str) -> dict[str, Any]:
    body = json.dumps({"package": {"name": name, "ecosystem": "PyPI"}, "version": version}).encode("utf-8")
    request = urllib.request.Request("https://api.osv.dev/v1/query", data=body, headers={"Content-Type": "application/json", "User-Agent": "ghc-family-owner-package-transaction/1"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        ids = sorted(row.get("id", "") for row in result.get("vulns", []) if row.get("id"))
        return {"package": name, "version": version, "query_succeeded": True, "advisory_ids": ids, "advisory_count": len(ids)}
    except Exception as exc:
        return {"package": name, "version": version, "query_succeeded": False, "advisory_ids": [], "advisory_count": None, "error_class": type(exc).__name__}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--bank", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    bank = args.bank.resolve()
    receipt_path = args.receipt.resolve()
    if receipt_path.exists():
        raise SystemExit("package transaction receipt already exists; replay refused")
    plan = json.loads((repo / "docs" / "elowen-cairn" / "v688-v5" / "x1" / "tool-package-plan.json").read_text(encoding="utf-8"))
    packages = plan["packages"]
    if bank.exists():
        raise SystemExit("package bank already exists; inspect before retry")
    bank.mkdir(parents=True, exist_ok=False)
    wheels = bank / "wheels"
    wheels.mkdir()
    downloads = []
    for package in packages:
        data = fetch(package["url"])
        digest = hashlib.sha256(data).hexdigest()
        if digest != package["sha256"]:
            raise RuntimeError(f"wheel hash mismatch for {package['name']}")
        target = wheels / package["wheel"]
        with target.open("xb") as handle:
            handle.write(data)
        downloads.append({"name": package["name"], "version": package["version"], "wheel": package["wheel"], "bytes": len(data), "sha256": digest, "hash_matches_frozen_plan": True})
    requirement_lines = [f"{row['name']}=={row['version']} --hash=sha256:{row['sha256']}" for row in packages]
    requirements = bank / "requirements.lock"
    requirements.write_text("\n".join(requirement_lines) + "\n", encoding="utf-8", newline="\n")
    environment = bank / "environment"
    venv.EnvBuilder(with_pip=True, clear=False, upgrade=False).create(environment)
    python = environment / "Scripts" / "python.exe"
    install = run([str(python), "-m", "pip", "install", "--disable-pip-version-check", "--no-index", "--only-binary=:all:", "--find-links", str(wheels), "--require-hashes", "-r", str(requirements)])
    if install.returncode:
        dump(receipt_path, {"schema": "ghc.family.package-transaction.v688.v5", "status": "INSTALL_FAILED", "downloads": downloads, "install_exit": install.returncode, "install_stderr_tail": install.stderr[-2000:], "failure_retained": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
        return 1
    version_code = "import json,importlib.metadata as m; print(json.dumps({n:m.version(n) for n in ['sgfmill','networkx','wcwidth']},sort_keys=True))"
    version_run = run([str(python), "-c", version_code])
    if version_run.returncode:
        raise RuntimeError(version_run.stderr)
    installed = json.loads(version_run.stdout)
    smoke_code = r'''
import json
from sgfmill import sgf
import networkx as nx
from wcwidth import wcswidth
result={}
game=sgf.Sgf_game.from_bytes(b'(;FF[4]GM[1]SZ[9];B[aa];W[])')
result['sgfmill_positive']={'size':game.get_size(),'main_sequence_nodes':len(game.get_main_sequence())}
try:
    sgf.Sgf_game.from_bytes(b'(;FF[4]GM[1]SZ[9]')
    result['sgfmill_adverse']={'refused':False,'error_class':None}
except Exception as exc:
    result['sgfmill_adverse']={'refused':True,'error_class':type(exc).__name__}
graph=nx.DiGraph([(0,1),(0,2),(1,3)])
cycle=nx.DiGraph([(0,1),(1,0)])
result['networkx_positive']={'dag':nx.is_directed_acyclic_graph(graph),'topological':list(nx.topological_sort(graph))}
result['networkx_adverse']={'cycle_refused_as_dag':not nx.is_directed_acyclic_graph(cycle)}
result['wcwidth_positive']={'width':wcswidth('B.W')}
result['wcwidth_adverse']={'control_width':wcswidth('B\x07W'),'refused':wcswidth('B\x07W')==-1}
print(json.dumps(result,sort_keys=True))
'''
    smoke_run = run([str(python), "-c", smoke_code])
    if smoke_run.returncode:
        raise RuntimeError(smoke_run.stderr)
    smokes = json.loads(smoke_run.stdout)
    smoke_valid = (
        smokes["sgfmill_positive"]["size"] == 9
        and smokes["sgfmill_positive"]["main_sequence_nodes"] == 3
        and smokes["sgfmill_adverse"]["refused"]
        and smokes["networkx_positive"]["dag"]
        and smokes["networkx_adverse"]["cycle_refused_as_dag"]
        and smokes["wcwidth_positive"]["width"] == 3
        and smokes["wcwidth_adverse"]["refused"]
    )
    audits = [osv(row["name"], row["version"]) for row in packages]
    advisory_complete = all(row["query_succeeded"] for row in audits)
    receipt = {
        "schema": "ghc.family.package-transaction.v688.v5",
        "status": "COMPLETE" if smoke_valid else "SMOKE_FAILED",
        "owner": "Elowen Cairn",
        "phase": "v688-v5",
        "d_first_isolated_environment": True,
        "system_python_mutated": False,
        "path_or_profile_mutated": False,
        "codex_desktop_updated": False,
        "host_security_weakened": False,
        "windows_features_changed": False,
        "rebooted": False,
        "downloads": downloads,
        "requirements": requirement_lines,
        "installed_versions": installed,
        "install_exit": install.returncode,
        "smokes": smokes,
        "positive_smoke_count": 3,
        "adverse_smoke_count": 3,
        "smoke_valid": smoke_valid,
        "advisory_snapshot": audits,
        "advisory_query_complete": advisory_complete,
        "advisory_finding_count": sum(row["advisory_count"] or 0 for row in audits),
        "advisory_boundary": "A bounded current snapshot is not exhaustive security, future assurance, license interpretation, production approval, or independent review.",
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    dump(receipt_path, receipt)
    print(json.dumps({"status": receipt["status"], "packages": len(packages), "positive": 3, "adverse": 3, "advisory_complete": advisory_complete, "advisories": receipt["advisory_finding_count"]}, sort_keys=True))
    return 0 if smoke_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
