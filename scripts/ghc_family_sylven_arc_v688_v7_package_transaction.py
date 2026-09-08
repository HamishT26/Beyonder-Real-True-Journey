#!/usr/bin/env python3
"""Install the exact x1-frozen runtime artifacts into one isolated D-first target."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
BASE = Path("docs/sylven-arc/v688-v7")
X1 = "4b7459cdf681726b8d411d644dc6f8db70e83871"


def write_new(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write("\n")


def run(command: list[str], bank: Path, label: str, env: dict[str, str]) -> bytes:
    result = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (bank / f"{label}.stdout.txt").write_bytes(result.stdout)
    (bank / f"{label}.stderr.txt").write_bytes(result.stderr)
    if result.returncode:
        raise RuntimeError(f"{label}_exit_{result.returncode}")
    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    args = parser.parse_args()
    bank = args.bank.resolve()
    if bank.drive.upper() != "D:":
        raise RuntimeError("D_first_bank_required")
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() != X1:
        raise RuntimeError("exact_x1_head_required")
    if subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=ROOT, text=True).strip() == "":
        raise RuntimeError("expected_uncommitted_x2_tool_sources_missing")
    plan_path = ROOT / BASE / "x1/tool-package-plan.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    frozen = subprocess.check_output(["git", "show", f"{X1}:{BASE.as_posix()}/x1/tool-package-plan.json"], cwd=ROOT)
    if json.loads(frozen) != plan:
        raise RuntimeError("frozen_package_plan_changed")
    bank.mkdir(parents=True, exist_ok=False)
    write_new(bank / "package-transaction-invoked.json", {
        "state": "STARTED",
        "x1": X1,
        "direct_count": len(plan["packages"]),
        "global_python_mutated": False,
    })
    artifacts_dir = bank / "artifacts"
    site_dir = bank / "site"
    cache_dir = bank / "cache"
    temp_dir = bank / "tmp"
    artifacts_dir.mkdir()
    cache_dir.mkdir()
    temp_dir.mkdir()
    downloaded: list[dict[str, object]] = []
    env = {
        **os.environ,
        "PIP_CACHE_DIR": str(cache_dir),
        "TMP": str(temp_dir),
        "TEMP": str(temp_dir),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONUTF8": "1",
    }
    try:
        artifact_paths: list[Path] = []
        for item in plan["packages"]:
            target = artifacts_dir / item["artifact"]
            request = urllib.request.Request(item["url"], headers={"User-Agent": "ghc-family-bounded-package-transaction/1"})
            with urllib.request.urlopen(request, timeout=60) as response:
                data = response.read(40 * 1024 * 1024 + 1)
            digest = hashlib.sha256(data).hexdigest()
            if len(data) > 40 * 1024 * 1024:
                raise RuntimeError(f"artifact_size_ceiling:{item['name']}")
            if len(data) != item["bytes"] or digest != item["sha256"]:
                raise RuntimeError(f"artifact_fixity:{item['name']}")
            with target.open("xb") as stream:
                stream.write(data)
            artifact_paths.append(target)
            downloaded.append({
                "name": item["name"],
                "version": item["version"],
                "artifact": item["artifact"],
                "packagetype": item["packagetype"],
                "bytes": len(data),
                "sha256": digest,
                "direct": True,
            })
        run(
            [sys.executable, "-B", "-m", "pip", "install", "--target", str(site_dir), "--no-deps", "--no-compile", *map(str, artifact_paths)],
            bank,
            "pip-target-install",
            env,
        )
        smoke = r'''
import importlib.metadata as metadata
import json
import chess
from lark import Lark
import networkx as nx

versions={d.metadata["Name"].lower():d.version for d in metadata.distributions(path=[__import__("os").environ["GHC_OWNER_SITE"]])}
board=chess.Board("8/8/8/8/8/8/8/K6k w - - 0 1")
assert board.fen()=="8/8/8/8/8/8/8/K6k w - - 0 1"
assert chess.Move.from_uci("e2e4").uci()=="e2e4"
try: chess.Board("not a fen")
except Exception as exc: chess_error=type(exc).__name__
else: raise AssertionError("malformed_fen_accepted")

grammar=r''' + '"""start: "[" NAME ESCAPED_STRING "]"\nNAME: /[A-Za-z0-9_]+/\n%import common.ESCAPED_STRING\n%import common.WS\n%ignore WS"""' + r'''
parser=Lark(grammar,start="start")
assert parser.parse('[Event "Synthetic"]')
try: parser.parse('[Event "Synthetic"')
except Exception as exc: lark_error=type(exc).__name__
else: raise AssertionError("unterminated_tag_accepted")

graph=nx.Graph();graph.add_edges_from([("a","b"),("c","d")])
assert sorted(sorted(component) for component in nx.connected_components(graph))==[["a","b"],["c","d"]]
cycle=nx.DiGraph([("a","b"),("b","a")])
try: list(nx.topological_sort(cycle))
except Exception as exc: networkx_error=type(exc).__name__
else: raise AssertionError("cycle_accepted")

print(json.dumps({"versions":versions,"smokes":{
 "chess":{"accepting":True,"adverse_rejected":True,"error_class":chess_error},
 "lark":{"accepting":True,"adverse_rejected":True,"error_class":lark_error},
 "networkx":{"accepting":True,"adverse_rejected":True,"error_class":networkx_error}},
 "real_games":0,"participant_records":0,"independent_reproduction":False}))
'''
        smoke_env = {**env, "PYTHONPATH": str(site_dir), "GHC_OWNER_SITE": str(site_dir)}
        smoke_result = json.loads(run([sys.executable, "-B", "-X", "utf8", "-c", smoke], bank, "package-smokes", smoke_env))
        expected_versions = {item["name"].lower(): item["version"] for item in plan["packages"]}
        for name, version in expected_versions.items():
            if smoke_result["versions"].get(name) != version:
                raise RuntimeError(f"installed_version:{name}")
        queries = {"queries": [{"package": {"name": item["name"], "ecosystem": "PyPI"}, "version": item["version"]} for item in plan["packages"]]}
        advisory_request = urllib.request.Request(
            "https://api.osv.dev/v1/querybatch",
            data=json.dumps(queries).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "ghc-family-bounded-advisory-snapshot/1"},
        )
        with urllib.request.urlopen(advisory_request, timeout=60) as response:
            advisory_raw = json.load(response)
        results = advisory_raw.get("results", [])
        if len(results) != len(plan["packages"]):
            raise RuntimeError("osv_response_shape")
        advisories = [
            {"name": item["name"], "version": item["version"], "vulnerabilities": observed.get("vulns", [])}
            for item, observed in zip(plan["packages"], results)
        ]
        advisory = {
            "schema": "ghc.family.package-advisory-snapshot.v1",
            "source": "https://api.osv.dev/v1/querybatch",
            "queried_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "query_count": len(advisories),
            "packages": advisories,
            "exhaustive_security": False,
            "expiry": "Point-in-time advisory observation; requery is required for a future decision.",
        }
        write_new(bank / "package-advisory-snapshot.json", advisory)
        receipt = {
            "schema": "ghc.family.chess-package-transaction.v1",
            "owner": "Sylven Arc",
            "phase": "v688-v7",
            "x1": X1,
            "state": "COMPLETE",
            "direct_count": 3,
            "artifacts": downloaded,
            "install_scope": "isolated D-first owner target",
            "site": "D-first owner phase bank; private absolute path withheld from repository projection",
            "global_python_mutated": False,
            "dependency_resolution": "disabled for runtime packages; build isolation used only by pip for the frozen chess sdist",
            "smokes": smoke_result,
            "advisory_query_count": len(advisories),
            "advisory_vulnerability_count": sum(len(item["vulnerabilities"]) for item in advisories),
            "rollback": "Stop selecting the isolated target and retain its receipts; do not erase it automatically.",
            "boundary": "Same-owner software and point-in-time advisory evidence only; no real game, participant, tournament, deployment, exhaustive security, independent reproduction, professional, legal, cultural, Maori-authority, consciousness, Theory-of-Everything, or Stage 20 evidence.",
        }
        write_new(bank / "package-transaction.json", receipt)
        print(json.dumps({"state": receipt["state"], "packages": 3, "positive_smokes": 3, "adverse_smokes": 3, "advisory_vulnerabilities": receipt["advisory_vulnerability_count"]}, sort_keys=True))
    except Exception as exc:
        write_new(bank / "package-transaction-failure.json", {
            "state": "FAILED_RETAINED",
            "error_class": type(exc).__name__,
            "signature": str(exc),
            "downloaded": downloaded,
            "success_credit": 0,
            "recovery": "Inspect the exclusive bank and isolate only the failed dependency before another attempt.",
        })
        raise


if __name__ == "__main__":
    main()
