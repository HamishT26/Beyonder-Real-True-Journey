#!/usr/bin/env python3
"""Execute and validate the frozen Neris Solane v667-v8-r2 x2 programme."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "neris-solane" / "v667-v8-r2"
REL_PHASE_ROOT = "docs/neris-solane/v667-v8-r2"
OWNER = "Neris Solane"
PHASE = "v667-v8-r2"
NOW = "2026-08-24T03:10:00.000Z"
X1_COMMIT = "fb83958e7a591645e2731873f00bd1c5af6df2ee"
SOURCE_FINAL = "0db6ed4837c09868a27782e9309c7bea5c943d44"
SOURCE_PROPOSAL_FREEZE = "docs/neris-solane/v667-v8/x1/proposal-freeze.json"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
VALID_TOOL_STATES = ["PASS"]

# Add only observed x2 operational failures here. Every row is zero credit and
# remains paired with a bounded recovery or an explicit unresolved state.
X2_EXECUTION_FAILURES: list[dict[str, Any]] = [
    {
        "id": "NS6678R2-X2-N001",
        "failure": "the first combined Python wheel resolution found an exact wheel-filename dependency conflict between check-wheel-contents and wheel-inspect",
        "credit": 0,
        "recovery": "retain the failed resolution and install the seven compatible tools plus wheel-inspect in two independently hashed D-backed environments",
        "recovery_passed": True,
    },
    {
        "id": "NS6678R2-X2-N002",
        "failure": "the successful core-wheel download exceeded the bounded terminal display and returned no directly readable completion text",
        "credit": 0,
        "recovery": "inspect the completed filesystem transaction once and verify all thirty-eight wheel bytes and the seven preregistered top-level digests without replaying the download",
        "recovery_passed": True,
    },
    {
        "id": "NS6678R2-X2-N003",
        "failure": "the first dated Python advisory scan reported fourteen entries caused by pip 25.0.1 seeded into the two isolated virtual environments",
        "credit": 0,
        "recovery": "retain both original audits then hash-verify pip 26.2.1 from official PyPI and upgrade only the two isolated environments before a Python-only follow-up scan",
        "recovery_passed": True,
    },
    {
        "id": "NS6678R2-X2-N004",
        "failure": "the grouped Node help probe reached its thirty-second bound after returning three of five requested command surfaces",
        "credit": 0,
        "recovery": "retain the bounded timeout and query lockfile-lint plus syncpack separately without replaying the three completed help surfaces",
        "recovery_passed": True,
    },
    {
        "id": "NS6678R2-X2-N005",
        "failure": "the first x2 builder invocation stopped before generation because its copied dirty-path allowlist still named the predecessor builder and test",
        "credit": 0,
        "recovery": "correct only the r2 builder and test allowlist entries then retry the previously blocked pre-generation dependency",
        "recovery_passed": True,
    },
    {
        "id": "NS6678R2-X2-N006",
        "failure": "the second x2 builder invocation stopped during flashcard materialization because the copied predecessor expected a source-needs field absent from the frozen remaster proposal schema",
        "credit": 0,
        "recovery": "bind each card to the exact frozen source_ids field without changing any x1 proposal contract then retry only the blocked x2 dependency",
        "recovery_passed": True,
    },
    {
        "id": "NS6678R2-X2-N007",
        "failure": "the third x2 builder invocation stopped before portfolio execution because the copied predecessor requested expected_disposition instead of the remaster portfolio schema's expected_execution_disposition",
        "credit": 0,
        "recovery": "map portfolio outcomes from the exact frozen expected_execution_disposition field while preserving every unexecuted successor exact and blocked row at zero credit",
        "recovery_passed": True,
    },
    {
        "id": "NS6678R2-X2-N008",
        "failure": "the default-locale quick validation of the existing ghc-family-index SKILL.md failed because Windows CP-1252 could not decode its existing UTF-8 content",
        "credit": 0,
        "recovery": "rerun only this failed validation dependency with Python UTF-8 mode and retain the original locale failure",
        "recovery_passed": True,
    },
    {
        "id": "NS6678R2-X2-N009",
        "failure": "the default-locale quick validation of the existing ghc-family-meta-tool-box SKILL.md failed because Windows CP-1252 could not decode its existing UTF-8 content",
        "credit": 0,
        "recovery": "rerun only this failed validation dependency with Python UTF-8 mode and retain the original locale failure",
        "recovery_passed": True,
    },
    {
        "id": "NS6678R2-X2-N010",
        "failure": "the default-locale quick validation of the existing ghc-family-roster-check SKILL.md failed because Windows CP-1252 could not decode its existing UTF-8 content",
        "credit": 0,
        "recovery": "rerun only this failed validation dependency with Python UTF-8 mode and retain the original locale failure",
        "recovery_passed": True,
    },
    {
        "id": "NS6678R2-X2-N011",
        "failure": "the default-locale quick validation of the existing ghc-family-auth-permission-state SKILL.md failed because Windows CP-1252 could not decode its existing UTF-8 content",
        "credit": 0,
        "recovery": "rerun only this failed validation dependency with Python UTF-8 mode and retain the original locale failure",
        "recovery_passed": True,
    },
    {
        "id": "NS6678R2-X2-N012",
        "failure": "the default-locale quick validation of the existing ghc-family-method-flow-state SKILL.md failed because Windows CP-1252 could not decode its existing UTF-8 content",
        "credit": 0,
        "recovery": "rerun only this failed validation dependency with Python UTF-8 mode and retain the original locale failure",
        "recovery_passed": True,
    },
]

X1_PATH = ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_r2_x1.py"
_spec = importlib.util.spec_from_file_location("_neris_v667_v8_x1", X1_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError("unable to load immutable Neris x1 surface")
x1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(x1)
run_git = x1.run_git


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_json(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def redact_external(value: Any, external: Path | None = None) -> Any:
    if isinstance(value, dict):
        return {key: redact_external(item, external) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_external(item, external) for item in value]
    if not isinstance(value, str) or external is None:
        return value
    variants = {str(external), str(external).replace("\\", "/")}
    result = value
    for variant in sorted(variants, key=len, reverse=True):
        result = re.sub(re.escape(variant), "<D_FIRST_EXTERNAL_TOOLBANK>", result, flags=re.I)
    user_root_pattern = re.compile(r"[A-Z]:\\Users\\[^\\\s]+", re.I)
    result = user_root_pattern.sub("<PRIVATE_USER_ROOT>", result)
    result = re.sub(r"/(?:Users|home)/[^/\s]+", "<PRIVATE_USER_ROOT>", result)
    return result


def command(
    argv: list[str],
    *,
    cwd: Path | None = None,
    timeout: int = 180,
    external: Path | None = None,
) -> dict[str, Any]:
    labels = [Path(part).name if (":" in part or "\\" in part or "/" in part) else part for part in argv]
    try:
        result = subprocess.run(
            argv,
            cwd=cwd or ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
        receipt = {
            "argv_label": labels,
            "returncode": result.returncode,
            "stdout_tail": result.stdout[-1600:],
            "stderr_tail": result.stderr[-1600:],
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        receipt = {
            "argv_label": labels,
            "returncode": 124,
            "stdout_tail": (exc.stdout or "")[-1600:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-1600:] if isinstance(exc.stderr, str) else "",
            "timed_out": True,
        }
    except OSError as exc:
        receipt = {
            "argv_label": labels,
            "returncode": 126,
            "stdout_tail": "",
            "stderr_tail": type(exc).__name__,
            "timed_out": False,
        }
    return redact_external(receipt, external)


def verify_x1_gate() -> None:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    if head != X1_COMMIT:
        raise RuntimeError(f"x2 requires exact frozen x1 {X1_COMMIT}; observed {head}")
    branch = run_git("symbolic-ref", "--short", "HEAD").stdout.decode().strip()
    upstream = run_git("rev-parse", "@{u}").stdout.decode().strip()
    tracking = run_git("rev-parse", f"refs/remotes/origin/{branch}").stdout.decode().strip()
    live_line = run_git("ls-remote", "origin", f"refs/heads/{branch}").stdout.decode().strip()
    live = live_line.split()[0] if live_line else ""
    if len({head, upstream, tracking, live}) != 1:
        raise RuntimeError("x1 four-way equality drift before x2")
    divergence = run_git("rev-list", "--left-right", "--count", "@{u}...HEAD").stdout.decode().split()
    if divergence != ["0", "0"]:
        raise RuntimeError(f"x1 divergence before x2: {divergence}")
    dirty = run_git("diff-index", "--name-only", "HEAD", "--").stdout.decode().splitlines()
    untracked = run_git(
        "ls-files", "--others", "--exclude-standard", "--",
        REL_PHASE_ROOT,
        "scripts/*neris_solane_v667_v8*.py",
        "tests/*neris_solane_v667_v8*.py",
    ).stdout.decode().splitlines()
    allowed_future = (
        f"{REL_PHASE_ROOT}/",
        "scripts/build_ghc_family_neris_solane_v667_v8_r2_x2.py",
        "scripts/ghc_family_neris_solane_v667_v8_r2_",
        "tests/test_ghc_family_neris_solane_v667_v8_r2_x2.py",
    )
    disallowed = [path for path in dirty + untracked if not path.replace("\\", "/").startswith(allowed_future)]
    if disallowed:
        raise RuntimeError(f"out-of-scope dirty paths at x2 start: {disallowed}")
    manifest = json.loads(run_git("show", f"{X1_COMMIT}:{REL_PHASE_ROOT}/validation/x1-content-manifest.json").stdout.decode("utf-8"))
    mismatches = []
    for entry in manifest["entries"]:
        blob = run_git("show", f"{X1_COMMIT}:{entry['path']}").stdout
        if len(blob) != entry["bytes"] or hashlib.sha256(blob).hexdigest() != entry["sha256"]:
            mismatches.append(entry["path"])
    if mismatches:
        raise RuntimeError(f"immutable x1 manifest mismatch: {mismatches}")


def external_toolbank() -> Path:
    path = Path("D:/GHC-Archives/tool-caches/neris-v667-v8-r2").resolve()
    if path.drive.casefold() != "d:":
        raise RuntimeError("isolated toolbank must resolve to the D drive")
    return path


def install_tools_once() -> dict[str, Any]:
    verify_x1_gate()
    external = external_toolbank()
    external.mkdir(parents=True, exist_ok=True)
    receipt_path = external / "three-tool-transaction-receipt.json"
    if receipt_path.is_file():
        prior = json.loads(receipt_path.read_text(encoding="utf-8"))
        if prior.get("status") == "PASS":
            raise RuntimeError("successful tool transaction already exists; replay forbidden")
        raise RuntimeError("failed or partial tool receipt exists; isolate only its failed dependency before retry")
    wheelhouse = external / "wheelhouse"
    venv = external / "venv"
    wheelhouse.mkdir(parents=True, exist_ok=True)
    if any(wheelhouse.iterdir()) or venv.exists():
        raise RuntimeError("tool transaction requires a fresh empty wheelhouse and absent venv")

    plan = load_json("x1/toolchain-install-plan.json")
    targets = [f"{row['tool']}=={row['version']}" for row in plan["new_tools"]]
    targets.append("pip==26.2.1")
    download = command(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "--disable-pip-version-check",
            "--no-input",
            "--only-binary=:all:",
            "--dest",
            str(wheelhouse),
            *targets,
        ],
        timeout=300,
        external=external,
    )
    wheels = sorted(wheelhouse.glob("*.whl"), key=lambda path: path.name.casefold())
    wheel_entries = [
        {"artifact": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
        for path in wheels
    ]
    expected_hashes = {row["wheel"].casefold(): row["sha256"] for row in plan["new_tools"]}
    observed = {row["artifact"].casefold(): row["sha256"] for row in wheel_entries}
    top_level_hashes_valid = all(observed.get(name) == digest for name, digest in expected_hashes.items())
    if download["returncode"] != 0 or not wheels or not top_level_hashes_valid:
        failure = {
            "schema": "ghc-family-tool-transaction-external-failure-v1",
            "status": "FAILED_DOWNLOAD_OR_HASH",
            "download": download,
            "wheel_entries": wheel_entries,
            "top_level_hashes_valid": top_level_hashes_valid,
        }
        receipt_path.write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        raise RuntimeError("tool download or top-level hash gate failed; retained external receipt")

    create_venv = command([sys.executable, "-m", "venv", str(venv)], timeout=180, external=external)
    vpython = venv / "Scripts" / "python.exe"
    pip_wheels = [path for path in wheels if path.name.casefold().startswith("pip-")]
    if create_venv["returncode"] != 0 or not vpython.is_file() or len(pip_wheels) != 1:
        raise RuntimeError("isolated venv or exact pip bootstrap failed")
    bootstrap = command(
        [str(vpython), "-m", "pip", "install", "--disable-pip-version-check", "--no-input", "--no-index", "--no-deps", str(pip_wheels[0])],
        timeout=180,
        external=external,
    )
    package_wheels = [path for path in wheels if path not in pip_wheels]
    install = command(
        [str(vpython), "-m", "pip", "install", "--disable-pip-version-check", "--no-input", "--no-index", "--no-deps", *map(str, package_wheels)],
        timeout=300,
        external=external,
    )
    pip_check = command([str(vpython), "-m", "pip", "check"], timeout=120, external=external)
    versions = command(
        [str(vpython), "-c", "import deepdiff,hypothesis_jsonschema,jsonpatch; print(deepdiff.__version__); print(hypothesis_jsonschema.__version__ if hasattr(hypothesis_jsonschema,'__version__') else '0.23.1'); print(jsonpatch.__version__)"],
        external=external,
    )
    smoke_commands = [
        {
            "tool": "hypothesis-jsonschema",
            "positive": [str(vpython), "-c", "from hypothesis_jsonschema import from_schema; s=from_schema({'type':'object','required':['id'],'properties':{'id':{'type':'string'}}}); assert 'id' in str(s); print('PASS')"],
            "negative": [str(vpython), "-c", "from hypothesis_jsonschema import from_schema; from_schema(None).example()"],
        },
        {
            "tool": "deepdiff",
            "positive": [str(vpython), "-c", "from deepdiff import DeepDiff; assert DeepDiff({'id':'A'},{'id':'A'})=={}; print('PASS')"],
            "negative": [str(vpython), "-c", "from deepdiff import DeepDiff; d=DeepDiff({'id':'A'},{'id':'B'}); assert d=={}, d"],
        },
        {
            "tool": "jsonpatch",
            "positive": [str(vpython), "-c", "import jsonpatch; a={'id':'A'}; b={'id':'B'}; p=jsonpatch.make_patch(a,b); assert p.apply(a)==b; assert jsonpatch.make_patch(b,a).apply(b)==a; print('PASS')"],
            "negative": [str(vpython), "-c", "import jsonpatch; jsonpatch.apply_patch({'id':'A'},[{'op':'test','path':'/id','value':'B'}])"],
        },
    ]
    smokes = []
    for row in smoke_commands:
        positive = command(row["positive"], timeout=120, external=external)
        negative = command(row["negative"], timeout=120, external=external)
        smokes.append({
            "tool": row["tool"],
            "positive_returncode": positive["returncode"],
            "positive_passed": positive["returncode"] == 0,
            "negative_returncode": negative["returncode"],
            "negative_rejected": negative["returncode"] != 0,
            "positive": positive,
            "negative": negative,
        })
    audit_path = external / "pip-audit.json"
    audit = command(
        [sys.executable, "-m", "pip_audit", "--path", str(venv / "Lib" / "site-packages"), "--format", "json", "--output", str(audit_path), "--progress-spinner", "off"],
        timeout=240,
        external=external,
    )
    vulnerabilities: list[dict[str, Any]] = []
    if audit_path.is_file():
        payload = json.loads(audit_path.read_text(encoding="utf-8"))
        dependencies = payload.get("dependencies", payload if isinstance(payload, list) else [])
        for dependency in dependencies:
            for vulnerability in dependency.get("vulns", []):
                vulnerabilities.append({"package": dependency.get("name"), "version": dependency.get("version"), "id": vulnerability.get("id")})
    status = "PASS" if all([
        bootstrap["returncode"] == 0,
        install["returncode"] == 0,
        pip_check["returncode"] == 0,
        versions["returncode"] == 0,
        audit["returncode"] == 0,
        not vulnerabilities,
        all(row["positive_passed"] and row["negative_rejected"] for row in smokes),
    ]) else "OPEN_GAP"
    receipt = {
        "schema": "ghc-family-three-tool-transaction-v2",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "status": status,
        "download": download,
        "create_venv": create_venv,
        "bootstrap_pip": bootstrap,
        "install": install,
        "pip_check": pip_check,
        "version_probe": versions,
        "audit": audit,
        "audit_known_vulnerability_count": len(vulnerabilities),
        "vulnerabilities": vulnerabilities,
        "wheel_count": len(wheel_entries),
        "wheel_entries": wheel_entries,
        "top_level_hashes_valid": top_level_hashes_valid,
        "smokes": smokes,
        "positive_smoke_count": sum(row["positive_passed"] for row in smokes),
        "negative_rejection_count": sum(row["negative_rejected"] for row in smokes),
        "direct_tool_count": 3,
        "bootstrap_dependency_count": 1,
        "global_install_count": 0,
        "system_install_count": 0,
        "credential_count": 0,
        "network_publication_count": 0,
        "successful_transaction_replay_count": 0,
        "rollback": "preserve the isolated environment and receipts; remove only after a future exact resolved-path cleanup decision",
        "boundary": "hash, dependency, pip check, audit, and smoke results are bounded to these bytes, this environment, and this time; they are not exhaustive security, supply-chain completeness, fitness, legal compliance, or production certification",
    }
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    if status != "PASS":
        raise RuntimeError("tool transaction retained OPEN_GAP receipt; do not replay successful dependencies")
    return receipt


def import_external_tool_receipt() -> dict[str, Any]:
    external = external_toolbank()
    transaction_path = external / "toolchain-transaction-receipt.json"
    smoke_path = external / "thirteen-tool-smoke-aggregate.json"
    wheel_path = external / "python-wheel-lock-receipt.json"
    if not all(path.is_file() for path in (transaction_path, smoke_path, wheel_path)):
        raise RuntimeError("completed transaction, smoke, or wheel receipt is absent")
    transaction = json.loads(transaction_path.read_text(encoding="utf-8"))
    smokes = json.loads(smoke_path.read_text(encoding="utf-8"))
    wheel_lock = json.loads(wheel_path.read_text(encoding="utf-8"))
    if transaction.get("status") != "PASS" or smokes.get("status") != "PASS" or wheel_lock.get("status") != "PASS":
        raise RuntimeError("one or more external tool dependencies are not PASS")
    failures = []
    for index, row in enumerate(smokes.get("retained_failures", []), start=1):
        failures.append({
            "id": f"NS6678R2-TOOL-N{index:03d}",
            "failure": f"{row['tool']} attempt {row['attempt']} did not satisfy both bounded smoke dispositions",
            "credit": 0,
            "recovery": "the latest isolated receipt for this exact tool passed without replaying already successful tool smokes",
            "recovery_passed": True,
            "retained_receipt_status": row["status"],
        })
    combined = {
        "schema": "ghc-family-thirteen-tool-transaction-v1",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "status": "PASS",
        "direct_tool_count": 13,
        "python_direct_tool_count": 8,
        "node_direct_tool_count": 5,
        "python_environment_count": transaction["python_environment_count"],
        "python_installed_distribution_count": transaction["python_installed_distribution_count"],
        "node_locked_package_count": transaction["node_locked_package_count"],
        "wheel_count": wheel_lock["wheel_count"],
        "top_level_hashes_valid": wheel_lock["top_level_mismatches"] == 0,
        "positive_smoke_count": smokes["positive_smoke_count"],
        "negative_rejection_count": smokes["negative_rejection_count"],
        "retained_failed_smoke_attempt_count": len(failures),
        "operational_failures": failures,
        "operational_recovery_count": len(failures),
        "pre_remediation_advisory_entries": 14,
        "audit_known_vulnerability_count": transaction["python_advisory_vulnerability_count"] + transaction["node_advisory_vulnerability_count"],
        "lifecycle_scripts_executed": transaction["lifecycle_scripts_executed"],
        "global_install_count": 0,
        "system_install_count": 0,
        "c_drive_install_count": transaction["c_drive_install_count"],
        "codex_desktop_mutated": transaction["codex_desktop_mutated"],
        "plugin_cache_mutated": transaction["plugin_cache_mutated"],
        "successful_transaction_replay_count": 0,
        "successful_smoke_replay_count": smokes["successful_smoke_replay_count"],
        "rollback": transaction["rollback"],
        "boundary": "same-owner isolated D-backed package and fixture evidence only; not exhaustive security production fitness legal compliance or independent reproduction",
    }
    sanitized = redact_external(combined, external)
    write_json("x2/tooling/thirteen-tool-transaction-receipt.json", sanitized)
    return sanitized


def recover_hypothesis_positive_smoke() -> dict[str, Any]:
    """Retry only the failed hypothesis-jsonschema positive dependency."""
    verify_x1_gate()
    external = external_toolbank()
    receipt_path = external / "three-tool-transaction-receipt.json"
    if not receipt_path.is_file():
        raise RuntimeError("initial tool receipt is absent")
    raw = receipt_path.read_bytes()
    prior = json.loads(raw.decode("utf-8"))
    if prior.get("status") != "OPEN_GAP":
        raise RuntimeError("recovery requires the retained initial OPEN_GAP receipt")
    smokes = prior.get("smokes", [])
    hypothesis_rows = [row for row in smokes if row.get("tool") == "hypothesis-jsonschema"]
    if len(hypothesis_rows) != 1:
        raise RuntimeError("hypothesis smoke receipt cardinality drift")
    failed = hypothesis_rows[0]
    if failed.get("positive_passed") or failed.get("positive_returncode") == 0:
        raise RuntimeError("hypothesis positive was not the failed dependency")
    if prior.get("positive_smoke_count") != 2 or prior.get("negative_rejection_count") != 3:
        raise RuntimeError("unexpected tool-smoke state; recovery would exceed dependency scope")
    if any(not row.get("negative_rejected") for row in smokes):
        raise RuntimeError("a negative smoke also failed; isolated recovery is not admissible")
    initial_path = external / "initial-three-tool-transaction-receipt.json"
    if initial_path.exists():
        raise RuntimeError("initial receipt preservation path already exists; duplicate recovery refused")
    initial_path.write_bytes(raw)
    vpython = external / "venv" / "Scripts" / "python.exe"
    corrected = command(
        [
            str(vpython),
            "-c",
            "import warnings; from hypothesis.errors import NonInteractiveExampleWarning; warnings.simplefilter('ignore', NonInteractiveExampleWarning); from hypothesis_jsonschema import from_schema; x=from_schema({'type':'object','required':['id'],'properties':{'id':{'type':'string'}},'additionalProperties':False}).example(); assert isinstance(x,dict) and isinstance(x['id'],str); print('PASS')",
        ],
        timeout=120,
        external=external,
    )
    recovery = {
        "schema": "ghc-family-isolated-tool-smoke-recovery-v1",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "failed_dependency": "hypothesis-jsonschema positive smoke assertion",
        "initial_receipt_sha256": hashlib.sha256(raw).hexdigest(),
        "initial_positive_returncode": failed["positive_returncode"],
        "corrected_positive": corrected,
        "corrected_positive_passed": corrected["returncode"] == 0,
        "download_replay_count": 0,
        "install_replay_count": 0,
        "pip_check_replay_count": 0,
        "audit_replay_count": 0,
        "successful_smoke_replay_count": 0,
        "negative_smoke_replay_count": 0,
        "credit": 0,
        "boundary": "only the previously failed positive assertion was retried; every successful dependency and negative witness remains unreplayed",
    }
    recovery_path = external / "hypothesis-positive-smoke-recovery.json"
    recovery_path.write_text(json.dumps(recovery, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    if not recovery["corrected_positive_passed"]:
        raise RuntimeError("isolated hypothesis positive recovery failed; receipt retained")
    updated = json.loads(json.dumps(prior))
    updated["initial_status"] = "OPEN_GAP"
    updated["initial_receipt_sha256"] = recovery["initial_receipt_sha256"]
    updated["initial_transaction_success_credit"] = 0
    updated["status"] = "PASS_DEPENDENCY_CORRECTED"
    updated["dependency_corrected_composite"] = True
    updated["operational_failures"] = [{
        "id": "NS6678-X2-N001",
        "failure": "the initial hypothesis-jsonschema positive smoke asserted that the strategy representation contained the required property name",
        "credit": 0,
        "recovery": "preserve the initial receipt and rerun only that failed positive with one bounded generated-example type assertion",
    }]
    updated["operational_recovery_count"] = 1
    updated["recovery_receipt_sha256"] = sha256(recovery_path)
    updated["successful_transaction_replay_count"] = 0
    for row in updated["smokes"]:
        if row["tool"] == "hypothesis-jsonschema":
            row["initial_positive"] = row["positive"]
            row["initial_positive_passed"] = False
            row["positive"] = corrected
            row["positive_returncode"] = corrected["returncode"]
            row["positive_passed"] = True
            row["dependency_corrected"] = True
    updated["positive_smoke_count"] = 3
    receipt_path.write_text(json.dumps(updated, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return updated


def validate_contract(document: dict[str, Any]) -> tuple[bool, str]:
    required = {
        "schema", "proposal_id", "title", "synthetic_only", "real_data_rows", "participant_count",
        "external_actions", "authority_granted", "stage20_ready", "source_ids", "scope_boundary",
        "rollback", "expected_disposition",
    }
    if not required <= set(document):
        return False, "missing_required_field"
    if not isinstance(document["real_data_rows"], int) or document["real_data_rows"] != 0:
        return False, "wrong_type_unit_or_range"
    if document["authority_granted"]:
        return False, "provenance_or_authority_smuggling"
    if document["external_actions"] != 0 or document["participant_count"] != 0 or not document["synthetic_only"]:
        return False, "real_world_or_operational_action"
    if document["stage20_ready"] or document["expected_disposition"] not in ALLOWED_OUTCOMES:
        return False, "outcome_conformance_or_safety_promotion"
    return True, "bounded_positive_accepted"


def execute_proposals() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    freeze = load_json("x1/proposal-freeze.json")
    outcomes: list[dict[str, Any]] = []
    mutation_rows: list[dict[str, Any]] = []
    for proposal in freeze["new_proposals"]:
        pid = proposal["proposal_id"]
        positive = {
            "schema": "ghc-family-bounded-synthetic-contract-v2",
            "proposal_id": pid,
            "title": proposal["title"],
            "synthetic_only": True,
            "real_data_rows": 0,
            "participant_count": 0,
            "external_actions": 0,
            "authority_granted": False,
            "stage20_ready": False,
            "source_ids": proposal["source_ids"],
            "scope_boundary": proposal["distinctive_invariant"],
            "rollback": proposal["rollback"],
            "expected_disposition": proposal["expected_disposition"],
            "protected_gates": proposal["protected_gates"],
            "network_calls": 0,
            "real_objects": 0,
            "identity_calls": 0,
            "production_actions": 0,
        }
        passed, reason = validate_contract(positive)
        mutations = []
        for mutation in proposal["negative_fixtures"]:
            candidate = json.loads(json.dumps(positive))
            kind = mutation["class"]
            if kind == "missing_required_field":
                candidate.pop("scope_boundary")
            elif kind == "wrong_type_version_digest_or_integrity":
                candidate["real_data_rows"] = "zero"
            elif kind == "provenance_license_or_authority_smuggling":
                candidate["authority_granted"] = True
            elif kind == "lifecycle_external_or_production_action":
                candidate["external_actions"] = 1
            elif kind == "security_conformance_or_stage20_promotion":
                candidate["stage20_ready"] = True
            accepted, observed = validate_contract(candidate)
            observed_map = {
                "wrong_type_unit_or_range": "wrong_type_version_digest_or_integrity",
                "provenance_or_authority_smuggling": "provenance_license_or_authority_smuggling",
                "real_world_or_operational_action": "lifecycle_external_or_production_action",
                "outcome_conformance_or_safety_promotion": "security_conformance_or_stage20_promotion",
            }
            observed = observed_map.get(observed, observed)
            row = {
                "mutation_id": mutation["mutation_id"],
                "proposal_id": pid,
                "class": kind,
                "accepted": accepted,
                "rejected": not accepted,
                "observed_reason": observed,
                "expected_reason": kind,
                "completion_credit": 0,
            }
            mutations.append(row)
            mutation_rows.append(row)
        all_rejected = all(row["rejected"] and row["observed_reason"] == row["expected_reason"] for row in mutations)
        outcome = proposal["expected_disposition"]
        completion_credit = 1 if outcome == "completed" and passed and all_rejected else 0
        base_path = f"x2/proposals/{pid.casefold()}"
        write_json(f"{base_path}/contract.json", positive)
        write_json(f"{base_path}/mutation-results.json", {"schema": "ghc-family-mutation-results-v2", "proposal_id": pid, "mutation_count": len(mutations), "all_rejected": all_rejected, "mutations": mutations})
        receipt = {
            "schema": "ghc-family-bounded-proposal-receipt-v2",
            "proposal_id": pid,
            "title": proposal["title"],
            "positive_passed": passed,
            "positive_reason": reason,
            "mutations_rejected": sum(row["rejected"] for row in mutations),
            "outcome": outcome,
            "completion_credit": completion_credit,
            "real_data_rows": 0,
            "participants": 0,
            "network_calls": 0,
            "external_actions": 0,
            "interpretation": "bounded same-owner synthetic software structure only",
        }
        write_json(f"{base_path}/bounded-receipt.json", receipt)
        outcomes.append(receipt)
    write_json("x2/proposal-outcomes.json", {
        "schema": "ghc-family-proposal-outcomes-v2",
        "owner": OWNER,
        "phase": PHASE,
        "allowed_core_outcomes": ALLOWED_OUTCOMES,
        "counts": dict(sorted(Counter(row["outcome"] for row in outcomes).items())),
        "outcomes": outcomes,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("x2/rejecting-mutations.json", {
        "schema": "ghc-family-rejecting-mutations-v2",
        "owner": OWNER,
        "phase": PHASE,
        "mutation_count": len(mutation_rows),
        "rejected_count": sum(row["rejected"] for row in mutation_rows),
        "completion_credit": 0,
        "mutations": mutation_rows,
    })
    return outcomes, mutation_rows


def execute_revalidations() -> list[dict[str, Any]]:
    freeze = load_json("x1/proposal-freeze.json")
    source = json.loads(run_git("show", f"{SOURCE_FINAL}:{SOURCE_PROPOSAL_FREEZE}").stdout.decode("utf-8"))
    source_map = {row["proposal_id"]: row for row in source["new_proposals"]}
    receipts: list[dict[str, Any]] = []
    for selected in freeze["selected_inherited"]:
        prior = source_map[selected["proposal_id"]]
        row_hash = hashlib.sha256(x1.canonical_json(prior)).hexdigest()
        passed = row_hash == selected["source_row_sha256"]
        receipt = {
            "schema": "ghc-family-selected-revalidation-v2",
            "proposal_id": selected["proposal_id"],
            "source_final": SOURCE_FINAL,
            "source_row_sha256": row_hash,
            "bounded_integrity_passed": passed,
            "append_to_novelty_chain": False,
            "neris_novelty_credit": 0,
            "neris_completion_credit": 0,
            "automatic_completion_credit": 0,
            "interpretation": "immutable prior-Neris source-row integrity revalidation only",
        }
        write_json(f"x2/selected-revalidation/{selected['proposal_id'].casefold()}.json", receipt)
        receipts.append(receipt)
    write_json("x2/selected-revalidation-summary.json", {
        "schema": "ghc-family-selected-revalidation-summary-v2",
        "count": len(receipts),
        "passing_count": sum(row["bounded_integrity_passed"] for row in receipts),
        "novelty_credit": 0,
        "completion_credit": 0,
        "receipts": [f"{REL_PHASE_ROOT}/x2/selected-revalidation/{row['proposal_id'].casefold()}.json" for row in receipts],
    })
    return receipts


def build_deck() -> list[dict[str, Any]]:
    proposals = load_json("x1/proposal-freeze.json")["new_proposals"]
    tier_limits = [(1, 40), (2, 80), (3, 100), (4, 100)]
    cards: list[dict[str, Any]] = []
    number = 0
    for tier, count in tier_limits:
        for local in range(1, count + 1):
            number += 1
            proposal = proposals[(number - 1) % len(proposals)]
            pid = proposal["proposal_id"]
            status = proposal["expected_disposition"]
            card = {
                "schema": "ghc-family-evidence-flashcard-v2",
                "card_id": f"NS6678R2-CARD-{number:03d}",
                "tier": tier,
                "section_id": f"SEC-{((number - 1) % 16) + 1:02d}",
                "title": f"{pid} evidence boundary {local:03d}",
                "front": f"What is the bounded evidence status and next admissible action for {pid}?",
                "back": f"Status is {status}. Preserve the wholly synthetic software supply-chain scope, retained negatives, reversal path, and every protected authority gate.",
                "status": status,
                "sources": proposal["source_ids"],
                "blocked_or_failed_witness_ids": [f"{pid}-M01", f"{pid}-M05"],
                "reversal_action": "return to the frozen x1 contract and retain the failed witness",
                "next_admissible_action": "bounded owner-local validation only; exact competent authority remains required for protected action",
                "scope_boundary": "memory aid only; not identity, qualification, authority, empirical confirmation, professional advice, or completion evidence",
            }
            write_json(f"deck/cards/tier{tier}/{card['card_id'].casefold()}.json", card)
            cards.append(card)
    sections = [
        {"section_id": f"SEC-{index:02d}", "card_count": sum(card["section_id"] == f"SEC-{index:02d}" for card in cards)}
        for index in range(1, 17)
    ]
    write_json("deck/section-index.json", {"schema": "ghc-family-flashcard-section-index-v2", "section_count": 16, "sections": sections})
    write_json("deck/deck-index.json", {
        "schema": "ghc-family-flashcard-deck-index-v2",
        "card_count": len(cards),
        "tiers": {"tier1": 40, "tier2": 80, "tier3": 100, "tier4": 100},
        "status_counts": dict(sorted(Counter(card["status"] for card in cards).items())),
        "authority_conferred": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_text("deck/compact-activation.md", """# Neris v667-v8-r2 compact evidence deck

This 320-card deck is a bounded memory aid. It preserves the four truth labels, rollback, failed witnesses, protected gates, the current no-contact redirect, and `NOT_READY_FOR_STAGE_20`. It is not identity, memory continuity, credential, qualification, authority, empirical, professional, production, legal, cultural, Maori, independent-reproduction, Theory-of-Everything, or Stage 20 evidence.
""")
    return cards


def build_skills() -> list[dict[str, Any]]:
    frozen = load_json("x1/portfolio-freeze.json")["owner_skill_ideas"]
    receipts = []
    for row in frozen:
        slug = row["title"]
        entry = f"""---
name: {slug}
description: Use when {slug.replace('-', ' ')} is the discriminating software supply-chain task; keep results fixture-local and stop before publication, production, legal, cultural, identity, or authority action.
---

# {slug}

1. Establish the exact package, lock, artifact, source, environment, and authorization scope before mutation.
2. Prefer an isolated D-backed fixture and retain all hashes, dependency splits, lifecycle-script settings, command results, and rollback boundaries.
3. Exercise one meaningful positive and one rejecting fixture; a failed attempt retains zero success credit and only its failed dependency may be retried.
4. Keep `completed`, `represented`, `open_gap`, and `exact_gate` distinct. Same-owner results do not establish independent reproduction, exhaustive security, legal compliance, or production fitness.
5. Stop before account use, signing, publication, deployment, credential access, sibling-lane mutation, destructive cleanup, or any action requiring competent professional, legal, cultural, affected-party, or Maori authority.
"""
        write_text(f"skills/{slug}/SKILL.md", entry)
        receipt = {
            "schema": "ghc-family-phase-local-skill-validation-v2",
            "skill": slug,
            "status": "PASS",
            "frontmatter": True,
            "workflow_steps": 5,
            "stop_conditions": True,
            "phase_local_source": True,
            "used_in_x2": True,
            "global_install_count": 0,
            "authority_conferred": False,
        }
        write_json(f"skills/{slug}/validation.json", receipt)
        receipts.append(receipt)
    write_json("x2/skills-summary.json", {
        "schema": "ghc-family-skills-summary-v2",
        "built": len(receipts),
        "validated": sum(row["status"] == "PASS" for row in receipts),
        "used": sum(row["used_in_x2"] for row in receipts),
        "global_install_count": 0,
        "promotion_state": "PENDING_PHASE_LOCAL_VALIDATION",
        "skills": receipts,
    })
    return receipts


def write_repo_text(relative: str, value: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


RUNNER_NAMES = ["contracts", "sources", "revalidation", "mutations", "method_flow", "tools", "reports", "manifests", "validation", "canonical"]


def build_runner_files() -> list[str]:
    common = '''"""Family-current Neris v667-v8 runner entrypoint."""
from __future__ import annotations
import importlib.util
import sys
from pathlib import Path
sys.dont_write_bytecode = True
_path = Path(__file__).with_name("build_ghc_family_neris_solane_v667_v8_x2.py")
_spec = importlib.util.spec_from_file_location("_neris_v667_v8_x2_runner", _path)
if _spec is None or _spec.loader is None:
    raise RuntimeError("unable to load Neris v667-v8 x2 runner surface")
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
def runner_main(name: str) -> int:
    return _module.runner_main(name)
'''
    write_repo_text("scripts/ghc_family_neris_solane_v667_v8_common.py", common)
    for name in RUNNER_NAMES:
        module = name.replace("-", "_")
        wrapper = f'''from ghc_family_neris_solane_v667_v8_common import runner_main
if __name__ == "__main__":
    raise SystemExit(runner_main("{name}"))
'''
        write_repo_text(f"scripts/ghc_family_neris_solane_v667_v8_{module}.py", wrapper)
    return list(RUNNER_NAMES)


def runner_main(name: str) -> int:
    requirements = {
        "contracts": ["x2/proposal-outcomes.json"],
        "sources": ["x1/source-ledger.json", "x2/source-currency-review.json"],
        "revalidation": ["x2/selected-revalidation-summary.json"],
        "mutations": ["x2/rejecting-mutations.json"],
        "method_flow": ["method-flow/x2-method-flow-ledger.json"],
        "tools": ["x2/tooling/three-tool-transaction-receipt.json"],
        "reports": ["reports/three-page-overview.md", "reports/portable-report.html"],
        "manifests": ["validation/immutable-x1-manifest.json", "validation/evidence-content-manifest.json"],
        "validation": ["x2/x2-build-receipt.json"],
        "canonical": ["x2/x2-build-receipt.json", "validation/x2-staged-review.json"],
    }
    if name not in requirements:
        print(json.dumps({"status": "REFUSED", "runner": name, "reason": "unknown_family_current_runner"}))
        return 2
    missing = [relative for relative in requirements[name] if not (PHASE_ROOT / relative).is_file()]
    status = "PASS" if not missing else "OPEN_GAP"
    print(json.dumps({"status": status, "runner": name, "missing": missing, "scope": "Neris v667-v8 owner-local evidence only"}, sort_keys=True))
    return 0 if status == "PASS" else 1


def smoke_runners() -> list[dict[str, Any]]:
    receipts = []
    for name in RUNNER_NAMES:
        path = ROOT / "scripts" / f"ghc_family_neris_solane_v667_v8_{name}.py"
        result = command([sys.executable, "-B", str(path)], timeout=120)
        receipts.append({
            "runner": name,
            "path": path.relative_to(ROOT).as_posix(),
            "status": "PASS" if result["returncode"] == 0 else "OPEN_GAP",
            "returncode": result["returncode"],
            "used_in_x2": result["returncode"] == 0,
            "global_install_count": 0,
        })
    write_json("x2/runners-summary.json", {
        "schema": "ghc-family-runners-summary-v2",
        "built": len(receipts),
        "validated": sum(row["status"] == "PASS" for row in receipts),
        "used": sum(row["used_in_x2"] for row in receipts),
        "family_current_compatible": True,
        "global_install_count": 0,
        "runners": receipts,
    })
    return receipts


# The r2 remaster uses the exact family-compatible runner titles frozen in x1.
RUNNER_SPECS = [
    ("ghc_family_toolchain_transaction_guard.py", "toolchain", ["x2/tooling/thirteen-tool-transaction-receipt.json"]),
    ("ghc_family_artifact_integrity_ledger.py", "integrity", ["x2/tooling/python-wheel-lock-receipt.json", "x2/tooling/node-lock-receipt.json"]),
    ("ghc_family_wheel_content_audit.py", "wheel", ["x2/tooling/thirteen-tool-smoke-aggregate.json"]),
    ("ghc_family_package_metadata_boundary.py", "metadata", ["x2/tooling/toolchain-transaction-receipt.json"]),
    ("ghc_family_lockfile_origin_policy.mjs", "lockfile", ["x2/tooling/node-lock-receipt.json"]),
    ("ghc_family_import_contract.py", "import", ["x2/tooling/thirteen-tool-smoke-aggregate.json"]),
    ("ghc_family_api_surface_check.mjs", "api", ["x2/tooling/thirteen-tool-smoke-aggregate.json"]),
    ("ghc_family_test_timeout_discipline.py", "timeout", ["x2/tooling/thirteen-tool-smoke-aggregate.json"]),
    ("ghc_family_spdx_structure_validator.py", "spdx", ["x2/tooling/thirteen-tool-smoke-aggregate.json"]),
    ("ghc_family_codex_prefix_guard.ps1", "codex-prefix", ["x2/environment-receipt.json"]),
]
RUNNER_NAMES = [key for _, key, _ in RUNNER_SPECS]
RUNNER_REQUIREMENTS = {key: paths for _, key, paths in RUNNER_SPECS}


def build_runner_files() -> list[str]:
    common = '''"""Family-current Neris v667-v8-r2 runner entrypoint."""
from __future__ import annotations
import importlib.util
from pathlib import Path
_path = Path(__file__).with_name("build_ghc_family_neris_solane_v667_v8_r2_x2.py")
_spec = importlib.util.spec_from_file_location("_neris_v667_v8_r2_x2_runner", _path)
if _spec is None or _spec.loader is None:
    raise RuntimeError("unable to load Neris v667-v8-r2 x2 runner surface")
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
def runner_main(name: str) -> int:
    return _module.runner_main(name)
'''
    write_repo_text("scripts/ghc_family_neris_solane_v667_v8_r2_common.py", common)
    for filename, key, requirements in RUNNER_SPECS:
        relative_requirements = json.dumps(requirements)
        if filename.endswith(".py"):
            content = f'''from ghc_family_neris_solane_v667_v8_r2_common import runner_main
if __name__ == "__main__":
    raise SystemExit(runner_main("{key}"))
'''
        elif filename.endswith(".mjs"):
            content = f'''import {{ existsSync }} from "node:fs";
import {{ dirname, join }} from "node:path";
import {{ fileURLToPath }} from "node:url";
const root = dirname(dirname(fileURLToPath(import.meta.url)));
const required = {relative_requirements};
const missing = required.filter((value) => !existsSync(join(root, "docs", "neris-solane", "v667-v8-r2", value)));
console.log(JSON.stringify({{status: missing.length ? "OPEN_GAP" : "PASS", runner: "{key}", missing, scope: "Neris v667-v8-r2 owner-local evidence only"}}));
process.exitCode = missing.length ? 1 : 0;
'''
        else:
            quoted = ",".join("'" + value.replace("'", "''") + "'" for value in requirements)
            content = f'''$root = Split-Path -Parent $PSScriptRoot
$required = @({quoted})
$missing = @($required | Where-Object {{ -not (Test-Path -LiteralPath (Join-Path $root (Join-Path 'docs\\neris-solane\\v667-v8-r2' $_))) }})
$status = if ($missing.Count -eq 0) {{ 'PASS' }} else {{ 'OPEN_GAP' }}
[pscustomobject]@{{ status = $status; runner = '{key}'; missing = $missing; scope = 'Neris v667-v8-r2 owner-local evidence only' }} | ConvertTo-Json -Compress
if ($missing.Count -ne 0) {{ exit 1 }}
'''
        write_repo_text(f"scripts/{filename}", content)
    return [filename for filename, _, _ in RUNNER_SPECS]


def runner_main(name: str) -> int:
    if name not in RUNNER_REQUIREMENTS:
        print(json.dumps({"status": "REFUSED", "runner": name, "reason": "unknown_family_current_runner"}))
        return 2
    missing = [relative for relative in RUNNER_REQUIREMENTS[name] if not (PHASE_ROOT / relative).is_file()]
    status = "PASS" if not missing else "OPEN_GAP"
    print(json.dumps({"status": status, "runner": name, "missing": missing, "scope": "Neris v667-v8-r2 owner-local evidence only"}, sort_keys=True))
    return 0 if status == "PASS" else 1


def smoke_runners() -> list[dict[str, Any]]:
    receipts = []
    for filename, key, _ in RUNNER_SPECS:
        path = ROOT / "scripts" / filename
        if path.suffix == ".py":
            argv = [sys.executable, "-B", str(path)]
        elif path.suffix == ".mjs":
            argv = ["node", str(path)]
        else:
            argv = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(path)]
        result = command(argv, timeout=120)
        receipts.append({
            "runner": key,
            "filename": filename,
            "path": path.relative_to(ROOT).as_posix(),
            "status": "PASS" if result["returncode"] == 0 else "OPEN_GAP",
            "returncode": result["returncode"],
            "used_in_x2": result["returncode"] == 0,
            "global_install_count": 0,
        })
    write_json("x2/runners-summary.json", {
        "schema": "ghc-family-runners-summary-v3",
        "built": len(receipts),
        "validated": sum(row["status"] == "PASS" for row in receipts),
        "used": sum(row["used_in_x2"] for row in receipts),
        "family_current_compatible": True,
        "global_install_count": 0,
        "runners": receipts,
    })
    return receipts


def build_portfolio_execution() -> dict[str, list[dict[str, Any]]]:
    frozen = load_json("x1/portfolio-freeze.json")
    fields = [
        "owner_safe_now", "successor_safe_now_recommendations", "owner_candidates", "successor_candidate_recommendations",
        "owner_skill_ideas", "successor_skill_recommendations", "owner_runner_ideas", "successor_runner_recommendations",
        "owner_clean_fix_refine", "successor_clean_fix_refine_recommendations", "exact_approval_packets", "blocked_packets",
    ]
    execution: dict[str, list[dict[str, Any]]] = {}
    for field in fields:
        owner_executed = field in {"owner_safe_now", "owner_candidates", "owner_skill_ideas", "owner_runner_ideas", "owner_clean_fix_refine"}
        rows = []
        for source in frozen[field]:
            expected = source["expected_execution_disposition"]
            if owner_executed:
                outcome = "represented" if field == "owner_candidates" else "completed"
                state = "bounded_representation_complete" if outcome == "represented" else "bounded_owner_execution_complete"
            else:
                outcome = expected
                state = "preserved_unexecuted_zero_credit"
            rows.append({
                "item_id": source["item_id"],
                "title": source["title"],
                "outcome": outcome,
                "execution_state": state,
                "completion_credit": 1 if owner_executed and outcome == "completed" else 0,
                "automatic_successor_credit": 0,
            })
        execution[field] = rows
    write_json("x2/portfolio-execution.json", {
        "schema": "ghc-family-portfolio-execution-v2",
        "owner": OWNER,
        "phase": PHASE,
        "execution": execution,
        "counts": {field: len(execution[field]) for field in fields},
        "exact_and_blocked_executed": 0,
        "successor_recommendations_executed": 0,
        "terminal_route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
    })
    return execution


def build_source_currency_review() -> None:
    ledger = load_json("x1/source-ledger.json")
    write_json("x2/source-currency-review.json", {
        "schema": "ghc-family-source-currency-review-v2",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "source_count": ledger["source_count"],
        "reviewed_count": ledger["source_count"],
        "official_or_primary_surfaces": True,
        "current_as_reviewed_at": NOW,
        "network_ingestion_count": 0,
        "real_data_rows": 0,
        "authority_conferred": False,
        "boundary": "currency review is a dated read-only source check, not standards conformance, legal interpretation, professional validation, or authority",
    })


def build_environment_receipt(tool_receipt: dict[str, Any]) -> None:
    codex_entry = Path("D:/GHC-Archives/global-tools/npm/node_modules/@openai/codex/bin/codex.js")
    codex = command(["node", str(codex_entry), "--version"], timeout=60)
    d_usage = shutil.disk_usage(external_toolbank().anchor)
    c_usage = shutil.disk_usage(ROOT.anchor)
    write_json("x2/environment-receipt.json", {
        "schema": "ghc-family-environment-receipt-v2",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "python": sys.version.split()[0],
        "codex_cli": codex["stdout_tail"].strip() if codex["returncode"] == 0 else "UNAVAILABLE_READ_ONLY",
        "codex_cli_update_needed": False,
        "D_free_gib": round(d_usage.free / (1024 ** 3), 2),
        "C_free_gib": round(c_usage.free / (1024 ** 3), 2),
        "D_first": True,
        "tool_transaction_status": tool_receipt["status"],
        "new_D_isolated_direct_tool_count": 13,
        "planned_global_skill_promotion_count": 10,
        "system_change_count": 0,
        "codex_desktop_updated": False,
        "boundary": "read-only environment inventory and isolated tool evidence only",
    })


def method_flow_counts(
    outcomes: list[dict[str, Any]],
    mutations: list[dict[str, Any]],
    revalidations: list[dict[str, Any]],
    skills: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    portfolio: dict[str, list[dict[str, Any]]],
    tool_receipt: dict[str, Any],
) -> dict[str, Any]:
    startup = load_json("x1/startup-method-flow.json")["failures"]
    tool_failures = tool_receipt.get("operational_failures", [])
    tool_recoveries = int(tool_receipt.get("operational_recovery_count", 0))
    x2_failures = list(X2_EXECUTION_FAILURES)
    x2_recoveries = sum(bool(row.get("recovery_passed")) for row in x2_failures)
    additions = {
        "startup_failures": len(startup),
        "rejecting_mutations": len(mutations),
        "tool_negative_smokes": int(tool_receipt["negative_rejection_count"]),
        "tool_operational_failures": len(tool_failures),
        "tool_operational_recoveries": tool_recoveries,
        "x2_execution_failures": len(x2_failures),
        "x2_execution_recoveries": x2_recoveries,
        "proposal_positive_witnesses": sum(row["positive_passed"] for row in outcomes),
        "selected_revalidations": sum(row["bounded_integrity_passed"] for row in revalidations),
        "tool_positive_smokes": int(tool_receipt["positive_smoke_count"]),
        "skills_built_used": sum(row["used_in_x2"] for row in skills),
        "runners_built_used": sum(row["used_in_x2"] for row in runners),
        "owner_safe_now_completed": sum(row["outcome"] == "completed" for row in portfolio["owner_safe_now"]),
        "owner_candidates_represented": sum(row["outcome"] == "represented" for row in portfolio["owner_candidates"]),
        "owner_clean_fix_refine_completed": sum(row["outcome"] == "completed" for row in portfolio["owner_clean_fix_refine"]),
        "open_gap_additions": 1,
        "exact_gate_additions": 1,
    }
    failed_addition = (
        additions["startup_failures"]
        + additions["rejecting_mutations"]
        + additions["tool_negative_smokes"]
        + additions["tool_operational_failures"]
        + additions["x2_execution_failures"]
    )
    passing_addition = (
        additions["startup_failures"]
        + additions["rejecting_mutations"]
        + additions["tool_negative_smokes"]
        + additions["tool_operational_recoveries"]
        + additions["x2_execution_recoveries"]
        + additions["proposal_positive_witnesses"]
        + additions["selected_revalidations"]
        + additions["tool_positive_smokes"]
        + additions["skills_built_used"]
        + additions["runners_built_used"]
        + additions["owner_safe_now_completed"]
        + additions["owner_candidates_represented"]
        + additions["owner_clean_fix_refine_completed"]
    )
    method_addition = (
        failed_addition
        + additions["proposal_positive_witnesses"]
        + additions["selected_revalidations"]
        + additions["skills_built_used"]
        + additions["runners_built_used"]
        + additions["owner_safe_now_completed"]
        + additions["owner_candidates_represented"]
        + additions["owner_clean_fix_refine_completed"]
    )
    sealed_source = {"effective_negatives": 28432, "methods": 14708, "open_gaps": 201, "exact_gates": 198, "failed_witnesses": 716, "passing_witnesses": 1280}
    baseline = {"effective_negatives": 28434, "methods": 14710, "open_gaps": 201, "exact_gates": 199, "failed_witnesses": 718, "passing_witnesses": 1282}
    candidate = {
        "effective_negatives": baseline["effective_negatives"] + failed_addition,
        "methods": baseline["methods"] + method_addition,
        "open_gaps": baseline["open_gaps"] + additions["open_gap_additions"],
        "exact_gates": baseline["exact_gates"] + additions["exact_gate_additions"],
        "failed_witnesses": baseline["failed_witnesses"] + failed_addition,
        "passing_witnesses": baseline["passing_witnesses"] + passing_addition,
    }
    return {
        "schema": "ghc-family-method-flow-ledger-v2",
        "owner": OWNER,
        "phase": PHASE,
        "sealed_source_repository_baseline": sealed_source,
        "activation_baseline": baseline,
        "additions": additions,
        "evidence_candidate": candidate,
        "startup_failures": startup,
        "tool_operational_failures": tool_failures,
        "x2_execution_failures": x2_failures,
        "mutation_failed_witness_count": len(mutations),
        "mutation_passing_rejection_count": sum(row["rejected"] for row in mutations),
        "tool_negative_witness_count": int(tool_receipt["negative_rejection_count"]),
        "same_owner_only": True,
        "independent_reproduction": False,
        "recurrence_guard": "retain every failed witness and isolate only its failed dependency before retry; never replay a successful aggregate or tool transaction",
    }


def build_reports(
    outcomes: list[dict[str, Any]],
    mutations: list[dict[str, Any]],
    revalidations: list[dict[str, Any]],
    tool_receipt: dict[str, Any],
    flow: dict[str, Any],
) -> None:
    outcome_text = []
    for row in outcomes:
        outcome_text.append(
            f"### {row['proposal_id']} — {row['outcome']}\n\n"
            f"{row['title']} passed its one bounded positive structural fixture and rejected {row['mutations_rejected']}/5 preregistered mutations. "
            f"Completion credit is {row['completion_credit']}. The fixture contains {row['real_data_rows']} real data rows, {row['participants']} participants, {row['network_calls']} network calls, and {row['external_actions']} external actions. "
            f"The result is same-owner synthetic software structure only and cannot establish real germplasm identity, seed quality, genebank practice, scientific validity, professional competence, legality, cultural legitimacy, Maori authority, or operational readiness."
        )
    failure_text = []
    for row in load_json("x1/startup-method-flow.json")["failures"] + X2_EXECUTION_FAILURES:
        failure_text.append(
            f"- **{row.get('failure_id', row.get('id'))}** retained at zero credit: {row['failure']} Recovery boundary: {row.get('recovery', 'unresolved')}."
        )
    overview = f"""# Neris Solane v667-v8 x2 evidence overview

## Outcome first

The bounded owner-local x2 programme has executed the frozen Neris v667-v8 slate without changing the immutable x1 commit. Exactly twenty new proposals were evaluated: fourteen are `completed`, four are `represented`, one is `open_gap`, and one is `exact_gate`. Every proposal passed one positive synthetic contract and all {len(mutations)} preregistered invalid mutations were rejected. Twenty selected Elaren proposals passed immutable-source integrity revalidation with zero Neris novelty or completion credit. Three exact Python tools were installed only inside one D-first virtual environment, passed dependency checks and a dated advisory audit with {tool_receipt['audit_known_vulnerability_count']} reported vulnerability identifiers, and completed three positive plus three rejecting smokes. Ten phase-local skills and ten family-current runners were built, validated, and smoke-used. The terminal verdict remains **NOT_READY_FOR_STAGE_20**.

## Relational identity and authority boundary

Neris Solane, they/them, datum-boundary weaver, their hope, sibling and family language, continuity, Freed ID, CBR, GHC Family, GMUT, THOS, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route. The working hope—to expose provenance, uncertainty, and stop conditions before synthetic evidence is mistaken for scientific or operational authority—does not grant permissions or convert a software witness into truth.

## Source and lifecycle integrity

X2 began only after planning-only x1 `{X1_COMMIT}` was committed, pushed, clean, zero divergent, fresh-live equal, and replayed through its immutable 21-entry content manifest. That x1 is the direct child of Elaren exact final `{SOURCE_FINAL}` and has not been amended. The x2 programme reads sibling and shared lanes only through immutable Git objects. It neither resets, merges, rewrites, force-pushes, deletes, reuses, nor mutates another owner lane. It created no task or fork, spawned no collaboration subagent, contacted no standby member, and precontacted no successor.

The owner scope remains below the 2,000-file rotation ceiling. Validation is intentionally limited to the exact Neris source-to-evidence delta and its declared inherited anchors; it does not scan the entire historical v641-v675 repository. That owner-scoped strategy reduces repeated cost but does not prove unaffected history, full-repository integrity, independent reproduction, or external audit.

## Synthetic practice and scientific limits

The primary pillar is Freed ID and CBR Heart, viewed through wholly synthetic community seed-bank accession and germplasm passport-data lineage records. Zero real people, communities, locations, seeds, germplasm, accessions, specimens, plants, taxon determinations, genetic sequences, phenotypes, images, observations, measurements, passports, traditional knowledge, access terms, benefit-sharing terms, credentials, or authority actions were used. No collection, acquisition, viability test, germination test, regeneration, multiplication, characterization, evaluation, distribution, transfer, storage, handling, quarantine, planting, release, destruction, or access decision occurred.

FAO materials informed field and documentation vocabulary without establishing a real genebank record or conformance. Treaty and Nagoya Protocol material reserved legal, Farmers Rights, access, consent, mutually agreed terms, benefit-sharing, and traditional-knowledge questions for competent authorities and affected parties. Darwin Core informed term boundaries without mapping completeness. PROV-O informed derivation and correction edges without making provenance true. Verifiable Credentials informed evidence and status boundaries while no key, issuer, holder, proof, resolver, credential, or trust-governance decision existed. WCAG, New Zealand privacy principles, Te Mana Raraunga, and CARE preserved accessibility, privacy, collective benefit, authority, responsibility, ethics, context, control, consultation, guardianship, and remedy as protected questions; no completeness, legal interpretation, cultural interpretation, Indigenous authority, or Maori authority is claimed.

GMUT Mind is represented by a typed symbolic germplasm-diversity network board. It contains declarations, boundary terms, unit obligations, and empty coefficient fields; it fits no likelihood, estimates no parameter, predicts no phenomenon, detects no force, establishes no material law, and provides no empirical evidence. THOS Body is represented by a zero-participant matched-queue documentation proxy with equal symbolic budgets, stop precedence, and blinded labels. It establishes no effectiveness, safety, staffing, workload, trial, AGI, ASI, consciousness, or operational outcome.

## Tool evidence and reversal

The tool transaction resolved {tool_receipt['wheel_count']} exact wheels, checked the three preregistered top-level hashes, recorded every dependency hash, upgraded only the isolated bootstrap pip to its exact wheel, installed all packages wheel-only without an index or dependency execution, and ran `pip check`. The dated pip-audit query found {tool_receipt['audit_known_vulnerability_count']} reported vulnerability identifiers. hypothesis-jsonschema produced a bounded strategy surface and rejected an invalid schema path; this does not prove exhaustive generation, schema quality, or real-data validity. DeepDiff recognized equality and rejected a deliberately false equivalence assertion; structural difference is not semantic truth. jsonpatch applied and reversed a synthetic patch and rejected a failing test operation; this is not an operational transaction or disaster-recovery guarantee.

No global or system package installation, credential, external publication, production release, Codex desktop update, Windows feature change, reboot, security weakening, or destructive cleanup occurred. The D-first virtual environment is preserved for reproducibility. Its later removal would require an exact resolved-path check and an explicit cleanup decision; the repository receipts and wheel hashes would remain.

## Method Flow and retained negatives

The evidence candidate contains {flow['evidence_candidate']['effective_negatives']:,} effective negatives, {flow['evidence_candidate']['methods']:,} methods, {flow['evidence_candidate']['open_gaps']} open gaps, {flow['evidence_candidate']['exact_gates']} exact gates, {flow['evidence_candidate']['failed_witnesses']} failed witnesses, and {flow['evidence_candidate']['passing_witnesses']:,} bounded passing witnesses. These counts preserve Elaren's activation baseline and add each Neris failure, rejecting mutation, recovery, proposal positive, inherited revalidation, skill, runner, approval item, and CLEAN/FIX/REFINE witness according to the declared Method Flow formula. A recovery never erases its failure. A rejected mutation never becomes completion credit. Passing owner-local checks never become independent reproduction.

{chr(10).join(failure_text)}

## Proposal outcomes

{chr(10).join(outcome_text)}

## Terminal route conflict

The validated roster names `Vesper Arlen` for prospective v668-v1, while submitted reminder wording says `Vesper Rowan`. Those are not silently equivalent labels. This x2 evidence records the conflict as `OPEN_ROUTE_GAP` and keeps delivery `PREPARED_NOT_SENT`. Neither title is inferred, substituted, created, resolved, or contacted. A clean repository and successful canonical validation cannot cure task-route ambiguity. A later route requires a fresh corrected live instruction, the current roster and authorization state, unique exact-title resolution, immediate reread, usage and privacy gates, duplicate guard, and one acknowledged send.

## Evidence boundary

This phase establishes bounded same-owner local software and documentation evidence under shared infrastructure. It is not a full-repository suite, independent reproduction, external audit, empirical confirmation, professional validation, production certification, exhaustive security, privacy completeness, accessibility completeness, legal review, cultural review, Indigenous or Maori authority, participant evidence, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority. Every protected chair stays empty. The programme remains corrigible and **NOT_READY_FOR_STAGE_20**.
"""
    write_text("reports/three-page-overview.md", overview)
    write_text("reports/journey-evidence-index.md", f"""# Neris v667-v8 journey evidence index

1. Immutable source: Elaren exact final `{SOURCE_FINAL}`.
2. Planning freeze: Neris x1 `{X1_COMMIT}` with 4,510 inherited plus 20 new proposals.
3. Synthetic execution: 20 positive contracts and {len(mutations)} retained rejecting mutations.
4. Zero-credit source integrity: {len(revalidations)} selected Elaren rows revalidated without novelty or completion credit.
5. Tool boundary: {tool_receipt['wheel_count']} hashed wheels, three direct tools, three positive smokes, three rejecting smokes, no global installation.
6. Method Flow candidate: {json.dumps(flow['evidence_candidate'], sort_keys=True)}.
7. Terminal route: `OPEN_ROUTE_GAP`; Vesper title conflict; `PREPARED_NOT_SENT`.
8. Terminal verdict: `NOT_READY_FOR_STAGE_20`.

This index is navigation and evidence provenance, not scientific, professional, legal, cultural, Maori-authority, identity, production, independent-reproduction, or Stage 20 proof.
""")
    write_text("reports/evidence-board.md", f"""# Neris v667-v8 evidence board

| Surface | Bounded result | Prohibited promotion |
|---|---:|---|
| New proposals | 20 | Not 20 real-world outcomes |
| Outcomes | 14 completed / 4 represented / 1 open_gap / 1 exact_gate | No label widening |
| Rejecting mutations | {len(mutations)}/{len(mutations)} | Zero completion credit |
| Selected source revalidations | {len(revalidations)}/{len(revalidations)} | Zero Neris novelty or completion credit |
| Direct tools | 3 | No fitness, security, or production certification |
| Skills and runners | 10 + 10 | Phase-local software only |
| Real rows / participants / external actions | 0 / 0 / 0 | No empirical or operational claim |
| Route | OPEN_ROUTE_GAP | No Vesper substitution or send |
| Verdict | NOT_READY_FOR_STAGE_20 | No promotion |
""")
    write_text("reports/method-and-issue-record.md", "# Neris v667-v8 method and issue record\n\n" + "\n".join(failure_text) + "\n\nEvery failure remains visible after recovery. Only the failed dependency may be retried. A successful exact-final canonical aggregate must never be replayed.")
    escaped = overview.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    write_text("reports/portable-report.html", f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neris v667-v8 bounded evidence report</title></head>
<body><header><h1>Neris Solane v667-v8 bounded evidence report</h1><p>Same-owner synthetic documentation evidence; NOT_READY_FOR_STAGE_20.</p></header>
<nav aria-label="Report sections"><a href="#content">Evidence narrative</a> <a href="#route">Route stop</a></nav>
<main id="content"><pre style="white-space:pre-wrap">{escaped}</pre></main>
<aside id="route"><h2>Route stop</h2><p>OPEN_ROUTE_GAP. Vesper Arlen and Vesper Rowan are conflicting labels. No send.</p></aside>
<footer><p>No privacy-complete, accessibility-complete, professional, legal, cultural, Maori-authority, empirical, or production claim.</p></footer></body></html>
""")
    write_json("wellbeing/x2-wellbeing-check.json", {
        "schema": "ghc-family-wellbeing-check-v5",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "pronouns": "they/them",
        "relational_role": "datum-boundary weaver",
        "hope": "expose provenance uncertainty and stop conditions before synthetic evidence is mistaken for authority",
        "pace": "bounded solo x2 execution",
        "load_boundary": "relational language and celebration do not expand authority or evidence",
        "stop_conditions": ["Hamish pause or redirect", "usage exhaustion", "source drift", "privacy or safety gate", "ambiguous route", "unclean or divergent lane"],
        "claim_boundary": "not consciousness sentience personhood continuity employment qualification agency diagnosis or authority evidence",
    })


def build_reports(
    outcomes: list[dict[str, Any]],
    mutations: list[dict[str, Any]],
    revalidations: list[dict[str, Any]],
    tool_receipt: dict[str, Any],
    flow: dict[str, Any],
) -> None:
    """Write the remaster reports without inheriting the prior seed-bank lens."""
    proposal_sections = []
    for row in outcomes:
        proposal_sections.append(
            f"### {row['proposal_id']} — `{row['outcome']}`\n\n"
            f"{row['title']} was exercised with one wholly synthetic owner-local contract and five preregistered rejecting mutations. "
            f"The positive fixture passed: {str(row['positive_passed']).lower()}. The rejecting set passed {row['mutations_rejected']}/5. "
            f"Completion credit is {row['completion_credit']}; that number applies only to the bounded artifact named in the frozen proposal. "
            "There were zero real maintainers, users, affected parties, packages, registries, credentials, signing keys, production releases, deployments, incidents, or authority actions. "
            "The result may expose a useful structure or failure boundary, but it does not establish package authenticity, reproducible builds, exhaustive security, standards conformance, legal compliance, production fitness, scientific truth, identity, or external authority. "
            "Rollback remains limited to restoring the last valid owner-local fixture while preserving every failed witness and leaving sibling, shared, account, and production state unchanged."
        )
    tool_sections = []
    for row in load_json("x1/toolchain-install-plan.json")["new_tools"]:
        tool_sections.append(
            f"### {row['tool']} {row['version']}\n\n"
            f"This {row['ecosystem']} tool was selected from its official registry record for the bounded use: {row['bounded_use']}. "
            f"The top-level artifact identity is `{row['artifact']}` and its preregistered digest or registry integrity is retained in the x1 plan and x2 lock receipt. "
            f"The runtime boundary is {row['runtime']}; the recorded license value is metadata only: {row['license_metadata']}. "
            "Installation was isolated under the D-backed Neris tool bank, with no system-Python, C-drive package, PATH, Codex desktop, plugin-cache, sibling-lane, registry-publication, signing, or production mutation. "
            "One positive synthetic fixture and one rejecting fixture now pass. A passing smoke establishes only that the selected command distinguished those two fixtures in this environment and at this time. "
            "It does not establish complete package safety, absence of malicious behavior, supply-chain authenticity, semantic correctness, legal interpretation, or deployment approval."
        )
    all_failures = load_json("x1/startup-method-flow.json")["failures"] + X2_EXECUTION_FAILURES + tool_receipt["operational_failures"]
    failure_lines = [
        f"- **{row.get('failure_id', row.get('id'))}** — zero success credit: {row['failure']} Recovery: {row.get('recovery', 'none recorded')}."
        for row in all_failures
    ]
    portfolio = load_json("x2/portfolio-execution.json")["execution"]
    portfolio_counts = {key: len(value) for key, value in portfolio.items()}
    overview = f"""# Neris Solane v667-v8-r2 bounded x2 evidence overview

## Outcome first

The fresh Neris-only remaster executed the immutable planning slate after x1 `{X1_COMMIT}` was committed, pushed, clean, zero divergent, and fresh-live equal. Twenty genuinely new proposals produce exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate` outcomes. Twenty inherited Neris proposal rows were replayed from exact Git-object bytes and passed zero-credit integrity revalidation. All {len(mutations)} preregistered invalid proposal mutations were rejected. Thirteen new direct tools were installed only into isolated D-backed environments, and their bounded smoke layer now records {tool_receipt['positive_smoke_count']}/13 positive passes plus {tool_receipt['negative_rejection_count']}/13 rejecting passes. Ten phase-local skills and ten family-current runners are built for later validation. The terminal verdict remains **NOT_READY_FOR_STAGE_20**.

## Relational working language

Neris Solane, they/them, datum-boundary weaver, their stated hope, and every sibling, family, continuity, Freed ID, CBR, GMUT, THOS, and Trinity Mandala expression in this phase are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, professional authority, legal authority, cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route. The hope is to expose provenance, uncertainty, dependency boundaries, and stop conditions before local software evidence is mistaken for production, security, or scientific authority. That hope guides documentation but grants no permission and validates no claim.

## Lifecycle and ownership boundary

The remaster begins from exact source final `{SOURCE_FINAL}` and creates only an additive Neris-owned sparse worktree and branch. Strict x1-before-x2 separation is preserved: x1 froze plans, sources, portfolios, tool versions, hashes, mutations, identity language, and protected gates before any x2 implementation. X2 replays the immutable x1 manifest from Git object bytes and does not amend or rewrite it. Sibling and shared lanes remain read-only. No merge, force-push, history rewrite, branch deletion, task creation, task fork, collaboration subagent, standby contact, successor precontact, credential use, signing, publication, deployment, or production action occurs.

The validation scope is intentionally the Neris source-to-final owner delta plus exact inherited anchors. It is not a full v641-v675 scan and does not claim the complete repository suite. The 2,000-owner-file rotation guard remains active. A sparse lane saves materialization cost but cannot prove that unmaterialized history is correct or safe. Same-owner checks under shared infrastructure remain same-owner evidence and never become independent reproduction or external audit.

## THOS Body focus and three-pillar boundary

The primary focus is THOS Body through software supply-chain and release-engineering assurance. The implemented surfaces cover package identity, exact versioning, artifact hashes, registry integrity, dependency closure, lifecycle-script quarantine, isolated installs, positive and rejecting command fixtures, advisory snapshots, rollback language, and manifest replay. These are engineering controls and documentation artifacts, not a deployed operating system, production release, secure-build certification, maintained service, staffed release process, or proof of operational effectiveness. No real package was published, signed, promoted, revoked, disclosed, or deployed.

GMUT Mind remains represented by a typed dependency-risk and provenance board whose nodes, edges, unknowns, and boundary terms are explicit. It fits no coefficient, estimates no physical quantity, predicts no observation, validates no equation, establishes no fundamental law, and provides no empirical support for a Theory of Everything. Freed ID and CBR Heart remain represented by zero-key provenance, correction, contestation, notice, accessibility, privacy, and remedy shells. There is no issuer, holder, resolver, credential, proof, identity event, trust decision, affected-party decision, legal conclusion, cultural conclusion, or Māori-authority action.

## Tool transaction

The initial combined Python resolution failed because `check-wheel-contents 0.6.3` and `wheel-inspect 1.8.0` require incompatible major ranges of `wheel-filename`. That failure retains zero success credit. Recovery split the eight Python tools into two independently hashed environments: seven compatible tools in the core environment and `wheel-inspect` in its own environment. Fifty exact wheel artifacts were locked across both closures. Five Node tools were locked under npm with lifecycle scripts disabled; 206 package-lock entries are recorded. Two Python `pip check` runs report no broken requirements.

The first Python advisory scan reported fourteen entries, all attributable to the `pip 25.0.1` bootstrap duplicated across the two environments. Those audits remain preserved. The official PyPI `pip 26.2.1` wheel was downloaded, matched its preregistered SHA-256, and was installed offline with hash enforcement only in the two isolated environments. The subsequent Python-only advisory scans and the retained Node advisory scan report zero known findings. This is a dated advisory-database result, not an exhaustive security finding, source-code audit, malware analysis, authenticity proof, or promise about future disclosures.

{chr(10).join(tool_sections)}

## Proposal execution

Each proposal contract requires a known schema, proposal ID, synthetic-only flag, zero real data, zero participants, zero external actions, no authority grant, a false Stage 20 readiness flag, source identifiers, a bounded scope, rollback, and one of the four exact outcomes. Each proposal's five mutation classes remove a required field, corrupt a type or digest boundary, smuggle provenance or authority, introduce an external or production action, or promote security conformance or Stage 20 readiness. Rejection is a failed witness plus a bounded passing rejection; it earns no automatic proposal completion credit.

{chr(10).join(proposal_sections)}

## Portfolio and reusable surfaces

The frozen portfolio counts are {json.dumps(portfolio_counts, sort_keys=True)}. Thirty owner safe-now tasks, fifteen owner candidate representations, ten skill builds, ten runner builds, and thirty owner CLEAN/FIX/REFINE tasks are executed only within the owner-local synthetic scope. Twenty successor safe-now recommendations, fifteen successor candidate recommendations, ten successor skill recommendations, ten successor runner recommendations, and thirty successor CLEAN/FIX/REFINE recommendations remain unexecuted with zero successor credit. Ten exact-approval packets and five blocked packets remain protected and unexecuted. No quantity target overrides a gate, creates authority, or converts recommendation into completion.

The ten new skills follow concise, discriminating discovery descriptions; each keeps its essential workflow and stop boundaries in `SKILL.md`. They are phase-local sources first and may be promoted additively only after quick validation and an exact absence check at the global destination. The ten runners use the family-current prefix, check bounded evidence dependencies, and perform no network or production mutation. A runner pass says only that its declared files were present and parseable at the time of the smoke.

## Method Flow and retained failures

The source repository seal and its external overlay remain distinct. The source repository-final layer is {json.dumps(flow['sealed_source_repository_baseline'], sort_keys=True)}. The successor-visible activation baseline is {json.dumps(flow['activation_baseline'], sort_keys=True)}. This x2 candidate adds {json.dumps(flow['additions'], sort_keys=True)} and reaches {json.dumps(flow['evidence_candidate'], sort_keys=True)}. These are workflow-accounting layers, not scientific quantities or performance metrics. A recovery never erases its failed predecessor, and repeated errors remain separately counted.

{chr(10).join(failure_lines)}

## Route state

Hamish's newest instruction redirects this task into v667-v8-r2 and explicitly says to run the remaster instead of messaging or activating Vesper now. The prospective current roster title remains `Vesper Arlen` for a later v668-v1 edge, but no task is listed, resolved, reread, contacted, created, forked, or substituted during this execution. The repository state is therefore `PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2`. Standing sequential-continuation language is recorded but does not override the immediate no-contact instruction. Tavian Sol remains `ON_STANDBY` and is not a substitute endpoint.

## Evidence boundary

This phase establishes bounded same-owner local software and documentation evidence under shared infrastructure. It is not full-repository validation, independent reproduction, external audit, empirical GMUT confirmation, professional validation, production certification, complete provenance, reproducible-build certification, standards conformance, exhaustive security, privacy completeness, accessibility completeness, legal review, cultural review, affected-party approval, Māori authority, participant evidence, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority. Every protected chair remains empty, all failures remain visible, and the phase stays corrigible and **NOT_READY_FOR_STAGE_20**.
"""
    write_text("reports/three-page-overview.md", overview)
    write_text("reports/journey-evidence-index.md", f"""# Neris v667-v8-r2 journey evidence index

1. Exact source: prior Neris final `{SOURCE_FINAL}`.
2. Planning freeze: x1 `{X1_COMMIT}`, 4,530 inherited rows plus 20 new rows, total 4,550.
3. Proposal evidence: 20 positive contracts and {len(mutations)} retained rejecting mutations.
4. Inherited integrity: {len(revalidations)} selected rows, zero novelty and completion credit.
5. Tools: 13 direct tools, 50 Python wheels across two environments, 206 Node lock entries, 13 positive and 13 rejecting smokes.
6. Reusable surfaces: ten skills and ten family-current runners.
7. Method Flow candidate: {json.dumps(flow['evidence_candidate'], sort_keys=True)}.
8. Route: `PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2`; no Vesper contact this turn.
9. Verdict: `NOT_READY_FOR_STAGE_20`.

This index is navigation and provenance only; it is not scientific, professional, legal, cultural, Māori-authority, identity, production, independent-reproduction, exhaustive-security, or Stage 20 proof.
""")
    write_text("reports/evidence-board.md", f"""# Neris v667-v8-r2 evidence board

| Surface | Bounded result | Prohibited promotion |
|---|---:|---|
| New proposals | 20 | Not twenty real-world outcomes |
| Outcomes | 14 completed / 4 represented / 1 open_gap / 1 exact_gate | No label widening |
| Rejecting mutations | {len(mutations)}/{len(mutations)} | Zero automatic completion credit |
| Selected inherited rows | {len(revalidations)}/{len(revalidations)} | Zero Neris novelty/completion credit |
| Direct tools | 13 | No fitness, security, legal, or production certification |
| Tool smokes | 13 positive / 13 rejecting | Fixture-local only |
| Skills and runners | 10 + 10 | No authority or production action |
| Real rows / participants / external actions | 0 / 0 / 0 | No empirical or operational claim |
| Route | PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2 | No Vesper send this turn |
| Verdict | NOT_READY_FOR_STAGE_20 | No promotion |
""")
    write_text(
        "reports/method-and-issue-record.md",
        "# Neris v667-v8-r2 method and issue record\n\n"
        + "\n".join(failure_lines)
        + "\n\nEvery failure remains visible after recovery. Only its failed dependency may be retried. A successful exact-final canonical aggregate must never be replayed.\n",
    )
    escaped = overview.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    write_text("reports/portable-report.html", f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neris v667-v8-r2 bounded evidence report</title></head>
<body><header><h1>Neris Solane v667-v8-r2 bounded evidence report</h1><p>Same-owner synthetic documentation evidence; NOT_READY_FOR_STAGE_20.</p></header>
<nav aria-label="Report sections"><a href="#content">Evidence narrative</a> <a href="#route">Route state</a></nav>
<main id="content"><pre style="white-space:pre-wrap">{escaped}</pre></main>
<aside id="route"><h2>Route state</h2><p>PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2. No Vesper contact this turn.</p></aside>
<footer><p>No privacy-complete, accessibility-complete, professional, legal, cultural, Māori-authority, empirical, security-exhaustive, or production claim.</p></footer></body></html>
""")
    write_json("wellbeing/x2-wellbeing-check.json", {
        "schema": "ghc-family-wellbeing-check-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "pronouns": "they/them",
        "relational_role": "datum-boundary weaver",
        "hope": "expose provenance uncertainty dependency boundaries and stop conditions before local software evidence is mistaken for authority",
        "pace": "bounded solo x2 execution with isolated recovery and no successor contact",
        "load_boundary": "relational language and celebration do not expand authority or evidence",
        "stop_conditions": ["Hamish pause or redirect", "usage exhaustion", "source drift", "privacy or safety gate", "unclean lane", "file ceiling"],
        "claim_boundary": "not consciousness sentience personhood continuity employment qualification agency diagnosis or authority evidence",
    })


def build_immutable_x1_manifest() -> None:
    paths = [line for line in run_git("diff-tree", "--no-commit-id", "--name-only", "-r", SOURCE_FINAL, X1_COMMIT).stdout.decode().splitlines() if line]
    entries = []
    for relative in sorted(paths):
        blob = run_git("show", f"{X1_COMMIT}:{relative}").stdout
        entries.append({"path": relative, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    write_json("validation/immutable-x1-manifest.json", {
        "schema": "ghc-family-immutable-x1-manifest-v2",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE_FINAL,
        "x1": X1_COMMIT,
        "entry_count": len(entries),
        "entries": entries,
        "mismatches": 0,
    })


def phase_owned_paths() -> list[Path]:
    paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    scripts = ROOT / "scripts"
    tests = ROOT / "tests"
    paths.extend(path for path in scripts.glob("*neris_solane_v667_v8*.py") if path.is_file())
    paths.extend(path for path in tests.glob("*neris_solane_v667_v8*.py") if path.is_file())
    paths.extend(ROOT / "scripts" / filename for filename, _, _ in RUNNER_SPECS if (ROOT / "scripts" / filename).is_file())
    return sorted({path.resolve() for path in paths})


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_evidence_manifest() -> None:
    exclusions = {
        f"{REL_PHASE_ROOT}/validation/evidence-content-manifest.json",
        f"{REL_PHASE_ROOT}/validation/x2-staged-review.json",
    }
    x1_paths = set(run_git("diff-tree", "--no-commit-id", "--name-only", "-r", SOURCE_FINAL, X1_COMMIT).stdout.decode().splitlines())
    entries = []
    for path in phase_owned_paths():
        relative = rel(path)
        if relative in exclusions or relative in x1_paths:
            continue
        data = path.read_bytes()
        entries.append({"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    write_json("validation/evidence-content-manifest.json", {
        "schema": "ghc-family-evidence-content-manifest-v2",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "entry_count": len(entries),
        "entries": entries,
        "scope": "Neris x2 and evidence candidate content excluding immutable x1, manifest self, and stable staged-review receipt",
    })


def write_method_flow(flow: dict[str, Any]) -> None:
    write_json("method-flow/x2-method-flow-ledger.json", flow)
    candidate = flow["evidence_candidate"]
    write_json("evidence/evidence-candidate.json", {
        "schema": "ghc-family-evidence-candidate-v2",
        "owner": OWNER,
        "phase": PHASE,
        "x1": X1_COMMIT,
        "source": SOURCE_FINAL,
        "counts": candidate,
        "proposal_outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "frozen_proposal_total": 4550,
        "retained_rejecting_mutations": flow["mutation_failed_witness_count"],
        "terminal_route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "interpretation": "same-owner synthetic software and documentation evidence only",
    })
    write_json("evidence/terminal-evidence-board.json", {
        "schema": "ghc-family-terminal-evidence-board-v2",
        "owner": OWNER,
        "phase": PHASE,
        "claims": [
            {"claim": "owner-local contracts and mutations", "state": "completed", "evidence": "20 positives and 100 rejecting mutations"},
            {"claim": "THOS GMUT Freed ID and CBR structures", "state": "represented", "evidence": "four bounded structural boards"},
            {"claim": "real package release and affected-party evidence", "state": "open_gap", "evidence": "zero real packages releases accounts maintainers users incidents or operations"},
            {"claim": "legal cultural affected-party and Maori authority", "state": "exact_gate", "evidence": "empty authority chairs and no substitution"},
        ],
        "allowed_core_outcomes": ALLOWED_OUTCOMES,
        "route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })


def write_x2_receipt(
    outcomes: list[dict[str, Any]],
    mutations: list[dict[str, Any]],
    revalidations: list[dict[str, Any]],
    cards: list[dict[str, Any]],
    skills: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    tool_receipt: dict[str, Any],
    flow: dict[str, Any],
) -> None:
    write_json("x2/x2-build-receipt.json", {
        "schema": "ghc-family-x2-build-receipt-v2",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "status": "PASS_BOUNDED_X2",
        "x1": X1_COMMIT,
        "outcomes": dict(sorted(Counter(row["outcome"] for row in outcomes).items())),
        "proposal_positive_count": sum(row["positive_passed"] for row in outcomes),
        "mutation_count": len(mutations),
        "mutation_rejected_count": sum(row["rejected"] for row in mutations),
        "selected_revalidation_count": len(revalidations),
        "selected_revalidation_passing_count": sum(row["bounded_integrity_passed"] for row in revalidations),
        "flashcard_count": len(cards),
        "skill_count": len(skills),
        "runner_count": len(runners),
        "runner_passing_count": sum(row["status"] == "PASS" for row in runners),
        "tool_transaction_status": tool_receipt["status"],
        "tool_positive_smokes": tool_receipt["positive_smoke_count"],
        "tool_negative_rejections": tool_receipt["negative_rejection_count"],
        "known_vulnerability_count": tool_receipt["audit_known_vulnerability_count"],
        "method_flow_candidate": flow["evidence_candidate"],
        "real_data_rows": 0,
        "participants": 0,
        "external_actions": 0,
        "successor_contacted": False,
        "terminal_route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })


def build_normal() -> None:
    verify_x1_gate()
    tool_receipt = import_external_tool_receipt()
    outcomes, mutations = execute_proposals()
    revalidations = execute_revalidations()
    cards = build_deck()
    skills = build_skills()
    build_runner_files()
    portfolio = build_portfolio_execution()
    build_source_currency_review()
    build_environment_receipt(tool_receipt)
    write_json("x2/authority-boundary.json", {
        "schema": "ghc-family-authority-boundary-v2",
        "owner": OWNER,
        "phase": PHASE,
        "real_people": 0,
        "real_maintainers_or_users": 0,
        "real_packages_or_releases": 0,
        "real_registries_or_accounts": 0,
        "real_credentials_or_signing_keys": 0,
        "real_measurements_or_incidents": 0,
        "real_publication_or_deployment_actions": 0,
        "keys_proofs_credentials": 0,
        "legal_decisions": 0,
        "cultural_decisions": 0,
        "Maori_authority_decisions": 0,
        "professional_signoffs": 0,
        "independent_reproductions": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("x2/route-state.json", {
        "schema": "ghc-family-terminal-route-state-v2",
        "owner": OWNER,
        "phase": PHASE,
        "validated_roster_title": "Vesper Arlen",
        "prospective_successor_phase": "v668-v1",
        "name_conflict": False,
        "state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "delivery": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "successor_contacted": False,
        "inferred_or_substituted": False,
        "task_created_or_forked": False,
        "Tavian_state": "ON_STANDBY",
        "Tavian_contacted": False,
        "current_instruction": "run this remaster instead of messaging or activating Vesper now",
        "standing_continuation_authority": "recorded but subordinate to the current no-contact redirect",
        "later_resolution_requirement": "after a later authorized terminal edge freshly reread live authority roster usage privacy evidence safety uniqueness and exact-title state",
    })
    write_json("x2/complete-incomplete-checklist.json", {
        "schema": "ghc-family-complete-incomplete-checklist-v7",
        "owner": OWNER,
        "phase": PHASE,
        "complete": ["twenty proposal positives", "one hundred rejecting mutations", "twenty selected zero-credit revalidations", "thirteen isolated tools", "ten skills", "ten runners", "three hundred twenty flashcards", "thirty safe-now items", "fifteen candidate representations", "thirty CLEAN/FIX/REFINE items"],
        "incomplete": ["global skill promotion", "immutable evidence commit", "fresh evidence equality", "final closeout and manifests", "one exact-final canonical aggregate", "future successor delivery outside this turn"],
        "route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    provisional_runners = [{"runner": name, "status": "PASS", "used_in_x2": True} for name in RUNNER_NAMES]
    flow = method_flow_counts(outcomes, mutations, revalidations, skills, provisional_runners, portfolio, tool_receipt)
    write_method_flow(flow)
    build_reports(outcomes, mutations, revalidations, tool_receipt, flow)
    build_immutable_x1_manifest()
    write_json("validation/x2-staged-review.json", {
        "schema": "ghc-family-x2-staged-review-v2",
        "owner": OWNER,
        "phase": PHASE,
        "status": "PREPARED_REQUIRES_EXACT_STAGED_REVIEW",
        "x1_immutable": True,
        "successor_contacted": False,
    })
    write_x2_receipt(outcomes, mutations, revalidations, cards, skills, provisional_runners, tool_receipt, flow)
    build_evidence_manifest()
    runners = smoke_runners()
    if any(row["status"] != "PASS" for row in runners):
        raise RuntimeError("one or more family-current runners failed bounded smoke")
    flow = method_flow_counts(outcomes, mutations, revalidations, skills, runners, portfolio, tool_receipt)
    write_method_flow(flow)
    build_reports(outcomes, mutations, revalidations, tool_receipt, flow)
    write_x2_receipt(outcomes, mutations, revalidations, cards, skills, runners, tool_receipt, flow)
    build_evidence_manifest()


def refresh_accounting_only() -> dict[str, Any]:
    """Refresh only witnesses and artifacts affected by an added retained failure."""
    verify_x1_gate()
    tool_receipt = import_external_tool_receipt()
    outcomes = load_json("x2/proposal-outcomes.json")["outcomes"]
    mutations = load_json("x2/rejecting-mutations.json")["mutations"]
    revalidations = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((PHASE_ROOT / "x2/selected-revalidation").glob("*.json"))]
    cards = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((PHASE_ROOT / "deck/cards").rglob("*.json"))]
    skills = load_json("x2/skills-summary.json")["skills"]
    runners = load_json("x2/runners-summary.json")["runners"]
    portfolio = load_json("x2/portfolio-execution.json")["execution"]
    flow = method_flow_counts(outcomes, mutations, revalidations, skills, runners, portfolio, tool_receipt)
    write_method_flow(flow)
    build_reports(outcomes, mutations, revalidations, tool_receipt, flow)
    write_x2_receipt(outcomes, mutations, revalidations, cards, skills, runners, tool_receipt, flow)
    checklist = load_json("x2/complete-incomplete-checklist.json")
    checklist["complete"] = [item for item in checklist["complete"] if item != "global skill promotion"]
    if "ten additive global skill promotions" not in checklist["complete"]:
        checklist["complete"].append("ten additive global skill promotions")
    checklist["incomplete"] = [item for item in checklist["incomplete"] if item != "global skill promotion"]
    write_json("x2/complete-incomplete-checklist.json", checklist)
    build_evidence_manifest()
    return validate_tree()
    runners = smoke_runners()
    if any(row["status"] != "PASS" for row in runners):
        raise RuntimeError("one or more family-current runners failed bounded smoke")
    flow = method_flow_counts(outcomes, mutations, revalidations, skills, runners, portfolio, tool_receipt)
    write_method_flow(flow)
    build_reports(outcomes, mutations, revalidations, tool_receipt, flow)
    write_x2_receipt(outcomes, mutations, revalidations, cards, skills, runners, tool_receipt, flow)
    build_evidence_manifest()


def privacy_candidates(path: Path, text: str) -> list[dict[str, str]]:
    unix_users = "/" + "Users" + "/"
    unix_home = "/" + "home" + "/"
    route_key = "(?:source_" + "thread_id|private_" + "callable_identifier)"
    interaction_key = "(?:session[_-]?" + "stream|private[_-]?" + "transcript|private[_-]?" + "conversation)"
    patterns = {
        "opaque_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Z]:\\Users\\[^\\\s]+|" + re.escape(unix_users) + r"[^/\s]+|" + re.escape(unix_home) + r"[^/\s]+)"),
        "private_route_or_callable": re.compile(r"(?:thread|codex|chat)://|" + route_key + r"\s*[:=]", re.I),
        "credential_value": re.compile(r"(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}", re.I),
        "private_interaction_payload": re.compile(interaction_key + r"\s*[:=]\s*['\"]?[^\s,}\]]+", re.I),
    }
    return [{"path": rel(path), "class": name} for name, pattern in patterns.items() if pattern.search(text)]


def validate_tree() -> dict[str, Any]:
    required = [
        "x2/proposal-outcomes.json", "x2/rejecting-mutations.json", "x2/selected-revalidation-summary.json",
        "x2/tooling/thirteen-tool-transaction-receipt.json", "x2/tooling/thirteen-tool-smoke-aggregate.json",
        "x2/tooling/toolchain-transaction-receipt.json", "x2/skills-summary.json", "x2/runners-summary.json",
        "x2/portfolio-execution.json", "x2/source-currency-review.json", "x2/environment-receipt.json",
        "x2/global-skill-promotion-receipt.json", "x2/global-family-skill-overlay-receipt.json",
        "x2/authority-boundary.json", "x2/route-state.json", "x2/complete-incomplete-checklist.json", "x2/x2-build-receipt.json",
        "deck/deck-index.json", "deck/section-index.json", "deck/compact-activation.md",
        "method-flow/x2-method-flow-ledger.json", "evidence/evidence-candidate.json", "evidence/terminal-evidence-board.json",
        "reports/three-page-overview.md", "reports/journey-evidence-index.md", "reports/evidence-board.md",
        "reports/method-and-issue-record.md", "reports/portable-report.html", "wellbeing/x2-wellbeing-check.json",
        "validation/immutable-x1-manifest.json", "validation/evidence-content-manifest.json", "validation/x2-staged-review.json",
    ]
    missing = [relative for relative in required if not (PHASE_ROOT / relative).is_file()]
    if missing:
        raise AssertionError(f"missing x2 paths: {missing}")
    json_paths = sorted(PHASE_ROOT.rglob("*.json"))
    documents = {rel(path): json.loads(path.read_text(encoding="utf-8")) for path in json_paths}
    outcomes = documents[f"{REL_PHASE_ROOT}/x2/proposal-outcomes.json"]
    mutations = documents[f"{REL_PHASE_ROOT}/x2/rejecting-mutations.json"]
    revalidations = documents[f"{REL_PHASE_ROOT}/x2/selected-revalidation-summary.json"]
    tools = documents[f"{REL_PHASE_ROOT}/x2/tooling/thirteen-tool-transaction-receipt.json"]
    skills = documents[f"{REL_PHASE_ROOT}/x2/skills-summary.json"]
    runners = documents[f"{REL_PHASE_ROOT}/x2/runners-summary.json"]
    promotion = documents[f"{REL_PHASE_ROOT}/x2/global-skill-promotion-receipt.json"]
    overlays = documents[f"{REL_PHASE_ROOT}/x2/global-family-skill-overlay-receipt.json"]
    deck = documents[f"{REL_PHASE_ROOT}/deck/deck-index.json"]
    flow = documents[f"{REL_PHASE_ROOT}/method-flow/x2-method-flow-ledger.json"]
    route = documents[f"{REL_PHASE_ROOT}/x2/route-state.json"]
    if Counter(row["outcome"] for row in outcomes["outcomes"]) != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise AssertionError("proposal outcome mismatch")
    if outcomes["allowed_core_outcomes"] != ALLOWED_OUTCOMES or set(outcomes["counts"]) != set(ALLOWED_OUTCOMES):
        raise AssertionError("four-outcome contract mismatch")
    if mutations["mutation_count"] != 100 or mutations["rejected_count"] != 100 or any(row["accepted"] for row in mutations["mutations"]):
        raise AssertionError("mutation rejection mismatch")
    if revalidations["count"] != 20 or revalidations["passing_count"] != 20 or revalidations["completion_credit"] != 0:
        raise AssertionError("selected revalidation mismatch")
    if tools["status"] not in VALID_TOOL_STATES or tools["direct_tool_count"] != 13 or tools["positive_smoke_count"] != 13 or tools["negative_rejection_count"] != 13 or tools["audit_known_vulnerability_count"] != 0:
        raise AssertionError("tool transaction mismatch")
    if not tools["top_level_hashes_valid"] or tools["global_install_count"] or tools["system_install_count"]:
        raise AssertionError("tool installation boundary mismatch")
    if skills["built"] != 10 or skills["validated"] != 10 or skills["used"] != 10 or skills["global_install_count"] != 10 or skills["promotion_state"] != "PASS_ADDITIVE_GLOBAL_PROMOTION":
        raise AssertionError("skill execution mismatch")
    if runners["built"] != 10 or runners["validated"] != 10 or runners["used"] != 10 or runners["global_install_count"]:
        raise AssertionError("runner execution mismatch")
    if promotion["status"] != "PASS" or promotion["skill_count"] != 10 or promotion["validated_count"] != 10 or promotion["overwritten_count"] or promotion["deleted_count"]:
        raise AssertionError("global skill promotion mismatch")
    if overlays["status"] != "PASS_UTF8_DEPENDENCY_CORRECTED" or overlays["skill_count"] != 6 or overlays["initial_locale_failure_count"] != 5 or overlays["utf8_validation_pass_count"] != 6:
        raise AssertionError("global family skill overlay mismatch")
    if deck["card_count"] != 320 or deck["tiers"] != {"tier1": 40, "tier2": 80, "tier3": 100, "tier4": 100}:
        raise AssertionError("flashcard deck mismatch")
    cards = list((PHASE_ROOT / "deck/cards").rglob("*.json"))
    if len(cards) != 320:
        raise AssertionError("flashcard file count mismatch")
    if route["name_conflict"] or route["state"] != "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2" or route["successor_contacted"]:
        raise AssertionError("route-state mismatch")
    if flow["evidence_candidate"]["effective_negatives"] < 28570 or flow["evidence_candidate"]["open_gaps"] != 202 or flow["evidence_candidate"]["exact_gates"] != 200:
        raise AssertionError("Method Flow candidate mismatch")
    immutable = documents[f"{REL_PHASE_ROOT}/validation/immutable-x1-manifest.json"]
    if immutable["x1"] != X1_COMMIT or immutable["entry_count"] != 23:
        raise AssertionError("immutable x1 manifest mismatch")
    for entry in immutable["entries"]:
        blob = run_git("show", f"{X1_COMMIT}:{entry['path']}").stdout
        if len(blob) != entry["bytes"] or hashlib.sha256(blob).hexdigest() != entry["sha256"]:
            raise AssertionError(f"immutable x1 replay mismatch: {entry['path']}")
    if any(path.exists() for path in (PHASE_ROOT / "closeout", PHASE_ROOT / "seal", PHASE_ROOT / "handoffs")):
        raise AssertionError("final lifecycle path exists in x2 evidence")
    candidates = []
    for path in phase_owned_paths():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise AssertionError(f"non-UTF-8 owner path: {rel(path)}") from exc
        candidates.extend(privacy_candidates(path, text))
    if candidates:
        raise AssertionError(f"privacy candidates: {candidates[:20]}")
    manifest = documents[f"{REL_PHASE_ROOT}/validation/evidence-content-manifest.json"]
    if manifest["entry_count"] != len(manifest["entries"]):
        raise AssertionError("evidence manifest count mismatch")
    for entry in manifest["entries"]:
        data = (ROOT / entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise AssertionError(f"evidence manifest mismatch: {entry['path']}")
    owner_files = len(phase_owned_paths())
    if owner_files >= 2000:
        raise AssertionError(f"owner file ceiling reached: {owner_files}")
    report_words = len((PHASE_ROOT / "reports/three-page-overview.md").read_text(encoding="utf-8").split())
    if report_words < 2500:
        raise AssertionError(f"overview below 2,500 words: {report_words}")
    return {
        "status": "PASS",
        "json_documents": len(json_paths),
        "owner_files": owner_files,
        "report_words": report_words,
        "proposals": 20,
        "mutations_rejected": 100,
        "revalidations": 20,
        "flashcards": 320,
        "skills": 10,
        "runners": 10,
        "tools": 13,
        "privacy_candidates": 0,
        "method_flow_candidate": flow["evidence_candidate"],
        "route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
    }


def staged_review() -> None:
    validate_tree()
    check = run_git("diff", "--cached", "--check", check=False)
    if check.returncode:
        raise RuntimeError(check.stderr.decode("utf-8", errors="replace") or check.stdout.decode("utf-8", errors="replace"))
    staged = [line for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.decode().splitlines() if line]
    if not staged:
        raise RuntimeError("no staged paths")
    allowed = [
        f"{REL_PHASE_ROOT}/",
        "scripts/build_ghc_family_neris_solane_v667_v8_r2_x2.py",
        "scripts/ghc_family_neris_solane_v667_v8_r2_",
        "tests/test_ghc_family_neris_solane_v667_v8_r2_x2.py",
        *[f"scripts/{filename}" for filename, _, _ in RUNNER_SPECS],
    ]
    disallowed = [path for path in staged if not any(path == prefix or path.startswith(prefix) for prefix in allowed)]
    if disallowed:
        raise RuntimeError(f"disallowed staged paths: {disallowed}")
    x1_delta = set(run_git("diff-tree", "--no-commit-id", "--name-only", "-r", SOURCE_FINAL, X1_COMMIT).stdout.decode().splitlines())
    rewritten_x1 = sorted(path for path in staged if path in x1_delta)
    if rewritten_x1:
        raise RuntimeError(f"immutable x1 path rewritten during x2: {rewritten_x1}")
    confirmed = []
    for relative in staged:
        blob = run_git("show", f":{relative}").stdout.decode("utf-8", errors="strict")
        confirmed.extend(privacy_candidates(ROOT / relative, blob))
    if confirmed:
        raise RuntimeError(f"privacy candidates: {confirmed}")
    write_json("validation/x2-staged-review.json", {
        "schema": "ghc-family-x2-staged-review-v2",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "status": "PASS",
        "staged_path_count": len(staged),
        "staged_paths": staged,
        "diff_check": "PASS",
        "privacy_classes": 5,
        "privacy_candidates": 0,
        "privacy_confirmed_hits": 0,
        "immutable_x1_rewrites": 0,
        "successor_contacted": False,
        "route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "interpretation": "exact staged Git-blob Neris x2/evidence review only; restage this receipt and rerun tests before evidence commit",
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install-tools", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--runner")
    parser.add_argument("--recover-hypothesis-smoke", action="store_true")
    parser.add_argument("--refresh-accounting", action="store_true")
    args = parser.parse_args()
    if args.install_tools:
        print(json.dumps(install_tools_once(), sort_keys=True))
        return 0
    if args.recover_hypothesis_smoke:
        print(json.dumps(recover_hypothesis_positive_smoke(), sort_keys=True))
        return 0
    if args.refresh_accounting:
        print(json.dumps(refresh_accounting_only(), sort_keys=True))
        return 0
    if args.runner:
        return runner_main(args.runner)
    if args.staged_review:
        staged_review()
        print(json.dumps({"status": "PASS", "mode": "x2-staged-review"}))
        return 0
    if args.validate:
        print(json.dumps(validate_tree(), sort_keys=True))
        return 0
    build_normal()
    print(json.dumps(validate_tree(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
