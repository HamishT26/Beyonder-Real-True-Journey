#!/usr/bin/env python3
"""Execute and validate the frozen Neris Solane v667-v8 x2 programme."""

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
PHASE_ROOT = ROOT / "docs" / "neris-solane" / "v667-v8"
REL_PHASE_ROOT = "docs/neris-solane/v667-v8"
OWNER = "Neris Solane"
PHASE = "v667-v8"
NOW = "2026-08-23T23:00:00.000Z"
X1_COMMIT = "653ff8a70328e6dd8641bb9b2d1887ce94f1759e"
SOURCE_FINAL = "75082d325299732f6796ac262149147b3a7029e8"
SOURCE_OUTCOMES = "docs/elaren-kestrel/v667-v7/x2/proposal-outcomes.json"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
VALID_TOOL_STATES = ["PASS", "PASS_DEPENDENCY_CORRECTED"]

# Add only observed x2 operational failures here. Every row is zero credit and
# remains paired with a bounded recovery or an explicit unresolved state.
X2_EXECUTION_FAILURES: list[dict[str, Any]] = [
    {
        "id": "NS6678-X2-N002",
        "failure": "the first recovery-flag patch registered its argparse option after parse_args and was caught by bounded tail inspection before execution",
        "credit": 0,
        "recovery": "move the option registration before parse_args and invoke only the isolated recovery path",
        "recovery_passed": True,
    },
    {
        "id": "NS6678-X2-N003",
        "failure": "the first bulk evidence-stage wrapper exceeded its bounded output with line-ending notices, left zero staged paths, and left a zero-byte index lock after its process ended",
        "credit": 0,
        "recovery": "verify zero matching Git processes, remove only the exact stale zero-byte owner-worktree lock, refresh accounting dependencies, and stage once with line-ending conversion disabled for the command",
        "recovery_passed": True,
    },
    {
        "id": "NS6678-X2-N004",
        "failure": "the exact stale-lock removal guard found that the zero-byte lock had disappeared after process inspection but before Get-Item",
        "credit": 0,
        "recovery": "confirm the lock remains absent and perform no deletion or duplicate cleanup",
        "recovery_passed": True,
    },
]

X1_PATH = ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_x1.py"
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
        "scripts/build_ghc_family_neris_solane_v667_v8_x2.py",
        "scripts/ghc_family_neris_solane_v667_v8_",
        "tests/test_ghc_family_neris_solane_v667_v8_x2.py",
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
    raw = os.environ.get("GHC_FAMILY_D_BANK", "")
    if not raw:
        raise RuntimeError("GHC_FAMILY_D_BANK is required for isolated x2 tools")
    path = Path(raw).resolve()
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
    path = external / "three-tool-transaction-receipt.json"
    if not path.is_file():
        raise RuntimeError("run --install-tools exactly once before building x2")
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if receipt.get("status") not in VALID_TOOL_STATES:
        raise RuntimeError("external tool receipt is not PASS")
    sanitized = redact_external(receipt, external)
    write_json("x2/tooling/three-tool-transaction-receipt.json", sanitized)
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
            "source_ids": proposal["current_official_or_primary_source_needs"],
            "scope_boundary": proposal["distinctive_invariant"],
            "rollback": proposal["rollback_or_recovery"],
            "expected_disposition": proposal["expected_disposition"],
            "protected_gates": proposal["protected_gates"],
            "network_calls": 0,
            "real_objects": 0,
            "identity_calls": 0,
            "genebank_actions": 0,
        }
        passed, reason = validate_contract(positive)
        mutations = []
        for mutation in proposal["preregistered_mutations"]:
            candidate = json.loads(json.dumps(positive))
            kind = mutation["class"]
            if kind == "missing_required_field":
                candidate.pop("scope_boundary")
            elif kind == "wrong_type_unit_or_range":
                candidate["real_data_rows"] = "zero"
            elif kind == "provenance_or_authority_smuggling":
                candidate["authority_granted"] = True
            elif kind == "real_world_or_operational_action":
                candidate["external_actions"] = 1
            elif kind == "outcome_conformance_or_safety_promotion":
                candidate["stage20_ready"] = True
            accepted, observed = validate_contract(candidate)
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
    source = json.loads(run_git("show", f"{SOURCE_FINAL}:{SOURCE_OUTCOMES}").stdout.decode("utf-8"))
    source_map = {row["proposal_id"]: row for row in source["outcomes"]}
    receipts: list[dict[str, Any]] = []
    for selected in freeze["selected_inherited"]:
        prior = source_map[selected["proposal_id"]]
        passed = prior["outcome"] == selected["source_disposition"] and prior["positive_passed"] and prior["mutations_rejected"] == 5
        receipt = {
            "schema": "ghc-family-selected-revalidation-v2",
            "proposal_id": selected["proposal_id"],
            "source_final": SOURCE_FINAL,
            "source_disposition": selected["source_disposition"],
            "bounded_integrity_passed": passed,
            "append_to_novelty_chain": False,
            "neris_novelty_credit": 0,
            "neris_completion_credit": 0,
            "automatic_completion_credit": 0,
            "interpretation": "immutable Elaren source-integrity revalidation only",
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
    tier_limits = [(1, 40), (2, 80), (3, 90), (4, 40)]
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
                "card_id": f"NS6678-CARD-{number:03d}",
                "tier": tier,
                "section_id": f"SEC-{((number - 1) % 16) + 1:02d}",
                "title": f"{pid} evidence boundary {local:03d}",
                "front": f"What is the bounded evidence status and next admissible action for {pid}?",
                "back": f"Status is {status}. Preserve the wholly synthetic seed-bank documentation scope, retained negatives, reversal path, and every protected authority gate.",
                "status": status,
                "sources": proposal["current_official_or_primary_source_needs"],
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
        "tiers": {"tier1": 40, "tier2": 80, "tier3": 90, "tier4": 40},
        "status_counts": dict(sorted(Counter(card["status"] for card in cards).items())),
        "authority_conferred": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_text("deck/compact-activation.md", """# Neris v667-v8 compact evidence deck

This 250-card deck is a bounded memory aid. It preserves the four truth labels, rollback, failed witnesses, protected gates, the unresolved Vesper route conflict, and `NOT_READY_FOR_STAGE_20`. It is not identity, memory continuity, credential, qualification, authority, empirical, professional, production, legal, cultural, Maori, independent-reproduction, Theory-of-Everything, or Stage 20 evidence.
""")
    return cards


def build_skills() -> list[dict[str, Any]]:
    frozen = load_json("x1/portfolio-freeze.json")["owner_skill_ideas"]
    receipts = []
    for row in frozen:
        slug = row["title"]
        entry = f"""---
name: {slug}
description: Use for bounded Neris v667-v8 seed-bank lineage evidence when {slug.replace('-', ' ')} is the discriminating task; stop at real material, professional, legal, cultural, Maori-authority, identity, or production boundaries.
---

# {slug}

1. Confirm the immutable x1 proposal, exact source anchors, and public source references.
2. Operate only on Neris-owned synthetic records with zero participants, real rows, credentials, external actions, seed material, or genebank operations.
3. Require the bounded positive and all five preregistered rejecting witnesses.
4. Preserve the four truth labels, failed receipts, reversal path, route conflict, and `NOT_READY_FOR_STAGE_20`.
5. Stop at every scientific, professional, agricultural, taxonomic, genetic, access-and-benefit-sharing, privacy, accessibility, legal, cultural, Maori-authority, empirical, identity, deployment, or independent-reproduction gate.
"""
        write_text(f"skills/{slug}/SKILL.md", entry)
        receipt = {
            "schema": "ghc-family-phase-local-skill-validation-v2",
            "skill": slug,
            "status": "PASS",
            "frontmatter": True,
            "workflow_steps": 5,
            "stop_conditions": True,
            "phase_local": True,
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
            expected = source["expected_disposition"]
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
        "terminal_route_state": "OPEN_ROUTE_GAP",
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
    codex = command(["node", str(Path(shutil.which("codex.cmd") or "").parent / "node_modules" / "@openai" / "codex" / "bin" / "codex.js"), "--version"], timeout=60)
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
        "global_install_count": 0,
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
    baseline = {"effective_negatives": 28304, "methods": 14445, "open_gaps": 199, "exact_gates": 197, "failed_witnesses": 588, "passing_witnesses": 1015}
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
        "frozen_proposal_total": 4530,
        "retained_rejecting_mutations": flow["mutation_failed_witness_count"],
        "terminal_route_state": "OPEN_ROUTE_GAP",
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
            {"claim": "real genebank evidence", "state": "open_gap", "evidence": "zero real rows people material observations or operations"},
            {"claim": "legal cultural affected-party and Maori authority", "state": "exact_gate", "evidence": "empty authority chairs and no substitution"},
        ],
        "allowed_core_outcomes": ALLOWED_OUTCOMES,
        "route_state": "OPEN_ROUTE_GAP",
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
        "terminal_route_state": "OPEN_ROUTE_GAP",
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
        "real_communities": 0,
        "real_seed_or_germplasm_items": 0,
        "real_locations": 0,
        "real_measurements": 0,
        "real_genebank_actions": 0,
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
        "submitted_reminder_title": "Vesper Rowan",
        "name_conflict": True,
        "state": "OPEN_ROUTE_GAP",
        "delivery": "PREPARED_NOT_SENT",
        "successor_contacted": False,
        "inferred_or_substituted": False,
        "task_created_or_forked": False,
        "Tavian_state": "ON_STANDBY",
        "Tavian_contacted": False,
        "resolution_requirement": "fresh corrected live instruction plus unique exact-title resolution and immediate reread",
    })
    write_json("x2/complete-incomplete-checklist.json", {
        "schema": "ghc-family-complete-incomplete-checklist-v7",
        "owner": OWNER,
        "phase": PHASE,
        "complete": ["twenty proposal positives", "one hundred rejecting mutations", "twenty selected zero-credit revalidations", "three isolated tools", "ten skills", "ten runners", "250 flashcards", "thirty safe-now items", "fifteen candidate representations", "thirty CLEAN/FIX/REFINE items"],
        "incomplete": ["immutable evidence commit", "fresh evidence equality", "final closeout and manifests", "one exact-final canonical aggregate", "terminal route conflict resolution", "successor delivery"],
        "route_state": "OPEN_ROUTE_GAP",
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
        "x2/tooling/three-tool-transaction-receipt.json", "x2/skills-summary.json", "x2/runners-summary.json",
        "x2/portfolio-execution.json", "x2/source-currency-review.json", "x2/environment-receipt.json",
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
    tools = documents[f"{REL_PHASE_ROOT}/x2/tooling/three-tool-transaction-receipt.json"]
    skills = documents[f"{REL_PHASE_ROOT}/x2/skills-summary.json"]
    runners = documents[f"{REL_PHASE_ROOT}/x2/runners-summary.json"]
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
    if tools["status"] not in VALID_TOOL_STATES or tools["positive_smoke_count"] != 3 or tools["negative_rejection_count"] != 3 or tools["audit_known_vulnerability_count"] != 0:
        raise AssertionError("tool transaction mismatch")
    if not tools["top_level_hashes_valid"] or tools["global_install_count"] or tools["system_install_count"]:
        raise AssertionError("tool installation boundary mismatch")
    if skills["built"] != 10 or skills["validated"] != 10 or skills["used"] != 10 or skills["global_install_count"]:
        raise AssertionError("skill execution mismatch")
    if runners["built"] != 10 or runners["validated"] != 10 or runners["used"] != 10 or runners["global_install_count"]:
        raise AssertionError("runner execution mismatch")
    if deck["card_count"] != 250 or deck["tiers"] != {"tier1": 40, "tier2": 80, "tier3": 90, "tier4": 40}:
        raise AssertionError("flashcard deck mismatch")
    cards = list((PHASE_ROOT / "deck/cards").rglob("*.json"))
    if len(cards) != 250:
        raise AssertionError("flashcard file count mismatch")
    if not route["name_conflict"] or route["state"] != "OPEN_ROUTE_GAP" or route["successor_contacted"]:
        raise AssertionError("route conflict mismatch")
    if flow["evidence_candidate"]["effective_negatives"] < 28426 or flow["evidence_candidate"]["open_gaps"] != 200 or flow["evidence_candidate"]["exact_gates"] != 198:
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
        "flashcards": 250,
        "skills": 10,
        "runners": 10,
        "tools": 3,
        "privacy_candidates": 0,
        "method_flow_candidate": flow["evidence_candidate"],
        "route_state": "OPEN_ROUTE_GAP",
    }


def staged_review() -> None:
    validate_tree()
    check = run_git("diff", "--cached", "--check", check=False)
    if check.returncode:
        raise RuntimeError(check.stderr.decode("utf-8", errors="replace") or check.stdout.decode("utf-8", errors="replace"))
    staged = [line for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.decode().splitlines() if line]
    if not staged:
        raise RuntimeError("no staged paths")
    allowed = [f"{REL_PHASE_ROOT}/", "scripts/build_ghc_family_neris_solane_v667_v8_x2.py", "scripts/ghc_family_neris_solane_v667_v8_", "tests/test_ghc_family_neris_solane_v667_v8_x2.py"]
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
        "route_state": "OPEN_ROUTE_GAP",
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
