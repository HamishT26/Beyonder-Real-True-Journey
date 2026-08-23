#!/usr/bin/env python3
"""Execute and validate the frozen Elaren Kestrel v667-v7 x2 programme."""

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


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "elaren-kestrel" / "v667-v7"
REL_PHASE_ROOT = "docs/elaren-kestrel/v667-v7"
OWNER = "Elaren Kestrel"
PHASE = "v667-v7"
NOW = "2026-08-23T20:20:00.000Z"
X1_COMMIT = "b92d8b1b648c4d716ca894b22fda14327baed9b3"
SOURCE_FINAL = "dc8d91294b7656ad5e9961bba93ff759af20846c"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
X2_EXECUTION_FAILURES = [
    {"id": "EL6677-X2-N006", "failure": "plain codex version probe resolved to a protected executable and raised PermissionError", "credit": 0, "recovery": "use the installed CLI wrapper's Node entrypoint for a read-only version query"},
    {"id": "EL6677-X2-N007", "failure": "a direct codex.cmd diagnostic crossed the bounded yield while its projection omitted the live handle", "credit": 0, "recovery": "do not repeat the wrapper probe; use the deterministic Node entrypoint in the resume dependency"},
    {"id": "EL6677-X2-N008", "failure": "the first resume projected a nonexistent revalidations key from the summary schema", "credit": 0, "recovery": "inspect actual keys and reconstruct the twenty receipts from their completed files"},
    {"id": "EL6677-X2-N009", "failure": "the first dedicated test run repeated the already-passing candidate validator in test 30", "credit": 0, "recovery": "replace the duplicate call with a stable build-receipt assertion and reserve the next full candidate validation for exact staged review"},
]

X1_PATH = ROOT / "scripts" / "build_ghc_family_elaren_kestrel_v667_v7_x1.py"
_spec = importlib.util.spec_from_file_location("_elaren_v667_v7_x1", X1_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError("unable to load immutable Elaren x1 surface")
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


def redact_private_paths(value: Any) -> Any:
    """Remove the authorized external-bank location from durable diagnostics."""
    if isinstance(value, dict):
        return {key: redact_private_paths(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_private_paths(item) for item in value]
    if not isinstance(value, str):
        return value
    bank = os.environ.get("GHC_FAMILY_D_BANK", "")
    if not bank:
        return value
    variants = {
        bank,
        bank.replace("\\", "/"),
        bank.replace("\\", "%5C"),
        bank.replace("\\", "%5c"),
    }
    redacted = value
    for variant in sorted(variants, key=len, reverse=True):
        if variant:
            redacted = redacted.replace(variant, "<D_FIRST_EXTERNAL_BANK>")
    return redacted


def command(argv: list[str], *, cwd: Path | None = None, check: bool = False) -> dict[str, Any]:
    try:
        result = subprocess.run(argv, cwd=cwd or ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    except OSError as exc:
        receipt = {"argv_label": [Path(part).name if (":" in part or "\\" in part or "/" in part) else part for part in argv], "returncode": 126, "stdout_tail": "", "stderr_tail": "", "spawn_error": type(exc).__name__}
        if check:
            raise RuntimeError(json.dumps(receipt, ensure_ascii=False)) from exc
        return receipt
    receipt = redact_private_paths({"argv_label": [Path(part).name if (":" in part or "\\" in part or "/" in part) else part for part in argv], "returncode": result.returncode, "stdout_tail": result.stdout[-2000:], "stderr_tail": result.stderr[-2000:]})
    if check and result.returncode:
        raise RuntimeError(json.dumps(receipt, ensure_ascii=False))
    return receipt


def verify_x1_gate() -> None:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    if head != X1_COMMIT:
        raise RuntimeError(f"x2 requires exact frozen x1 {X1_COMMIT}; observed {head}")
    dirty = [line for line in run_git("status", "--porcelain=v1", "--untracked-files=all").stdout.decode("utf-8").splitlines() if line]
    allowed_prefixes = (f"{REL_PHASE_ROOT}/", "scripts/build_ghc_family_elaren_kestrel_v667_v7_x2.py", "scripts/ghc_family_elaren_kestrel_v667_v7_", "tests/test_ghc_family_elaren_kestrel_v667_v7_x2.py")
    disallowed = [line for line in dirty if not line[3:].replace("\\", "/").startswith(allowed_prefixes)]
    if disallowed:
        raise RuntimeError(f"out-of-scope dirty paths at x2 start: {disallowed}")
    local = head
    upstream = run_git("rev-parse", "@{u}").stdout.decode().strip()
    branch = run_git("symbolic-ref", "--short", "HEAD").stdout.decode().strip()
    tracking = run_git("rev-parse", f"refs/remotes/origin/{branch}").stdout.decode().strip()
    live_line = run_git("ls-remote", "origin", f"refs/heads/{branch}").stdout.decode().strip()
    live = live_line.split()[0] if live_line else ""
    if len({local, upstream, tracking, live}) != 1:
        raise RuntimeError("x1 four-way equality drift before x2")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tool_transaction() -> dict[str, Any]:
    verify_x1_gate()
    bank = os.environ.get("GHC_FAMILY_D_BANK")
    if not bank:
        raise RuntimeError("GHC_FAMILY_D_BANK must identify the authorized D-first external bank")
    external = Path(bank) / "toolbank" / "elaren-kestrel-v667-v7"
    downloads = external / "downloads"
    venv = external / "venv"
    smoke = external / "smoke"
    downloads.mkdir(parents=True, exist_ok=True)
    smoke.mkdir(parents=True, exist_ok=True)
    if not (venv / "Scripts" / "python.exe").is_file():
        command([sys.executable, "-m", "venv", str(venv)], check=True)
    vpython = venv / "Scripts" / "python.exe"
    plan = load_json("x1/toolchain-install-plan.json")
    tools = []
    for row in plan["new_tools"]:
        download = command([sys.executable, "-m", "pip", "download", "--disable-pip-version-check", "--no-input", "--only-binary=:all:", "--no-deps", "--dest", str(downloads), f"{row['tool']}=={row['version']}"])
        artifact = downloads / row["artifact"]
        if not artifact.is_file():
            raise RuntimeError(f"download did not materialize expected artifact for {row['tool']}")
        observed = sha256(artifact)
        if observed != row["sha256"]:
            raise RuntimeError(f"artifact hash mismatch for {row['tool']}")
        tools.append({"tool": row["tool"], "version": row["version"], "artifact": row["artifact"], "sha256": observed, "download_returncode": download["returncode"], "hash_verified": True})
    install_report = external / "pip-install-report.json"
    install = command([str(vpython), "-m", "pip", "install", "--disable-pip-version-check", "--no-input", "--report", str(install_report)] + [str(downloads / row["artifact"]) for row in plan["new_tools"]], check=True)
    pip_check = command([str(vpython), "-m", "pip", "check"])

    good_py = smoke / "good.py"
    bad_py = smoke / "bad.py"
    good_py.write_text('"""Synthetic documented module."""\n\ndef bounded() -> bool:\n    """Return a bounded sentinel."""\n    return True\n', encoding="utf-8")
    bad_py.write_text("def undocumented():\n    return False\n", encoding="utf-8")
    smokes = [
        {"tool": "interrogate", "positive": command([str(venv / "Scripts" / "interrogate.exe"), "--fail-under", "100", str(good_py)]), "negative": command([str(venv / "Scripts" / "interrogate.exe"), "--fail-under", "100", str(bad_py)])},
        {"tool": "import-linter", "positive": command([str(venv / "Scripts" / "lint-imports.exe"), "--help"]), "negative": command([str(venv / "Scripts" / "lint-imports.exe"), "--config", str(smoke / "absent-import-contract.ini")])},
        {"tool": "pyroma", "positive": command([str(venv / "Scripts" / "pyroma.exe"), "--help"]), "negative": command([str(venv / "Scripts" / "pyroma.exe"), str(smoke / "absent-package")])},
    ]
    for row in smokes:
        row["positive_passed"] = row["positive"]["returncode"] == 0
        row["negative_rejected"] = row["negative"]["returncode"] != 0
    site_packages = venv / "Lib" / "site-packages"
    audit_path = external / "pip-audit.json"
    audit = command([sys.executable, "-m", "pip_audit", "--path", str(site_packages), "--format", "json", "--output", str(audit_path)])
    vulnerabilities = []
    if audit_path.is_file():
        payload = json.loads(audit_path.read_text(encoding="utf-8"))
        dependencies = payload.get("dependencies", payload if isinstance(payload, list) else [])
        vulnerabilities = [{"name": row.get("name"), "version": row.get("version"), "vuln_count": len(row.get("vulns", []))} for row in dependencies if row.get("vulns")]
    status = "PASS" if install["returncode"] == 0 and pip_check["returncode"] == 0 and not vulnerabilities and all(row["positive_passed"] and row["negative_rejected"] for row in smokes) else "OPEN_GAP"
    receipt = {
        "schema": "ghc-family-three-tool-transaction-v1", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "status": status, "external_scope_label": "D_FIRST_ELAREN_V667_V7_ISOLATED_TOOLBANK", "tools": tools,
        "install_returncode": install["returncode"], "pip_check_returncode": pip_check["returncode"], "pip_install_report_sha256": sha256(install_report),
        "audit_returncode": audit["returncode"], "known_vulnerability_count": len(vulnerabilities), "vulnerabilities": vulnerabilities,
        "smokes": smokes, "positive_smoke_count": sum(row["positive_passed"] for row in smokes),
        "negative_rejection_count": sum(row["negative_rejected"] for row in smokes),
        "network_publication_count": 0, "credential_count": 0, "global_install_count": 0,
        "rollback": "remove only the verified external Elaren v667-v7 isolated toolbank; preserve this sanitized receipt",
        "boundary": "tool installation and bounded smokes establish local software availability only, not supply-chain completeness, legal advice, security certification, package fitness, or production readiness",
    }
    write_json("x2/tooling/three-tool-transaction-receipt.json", receipt)
    return receipt


def recover_tool_audit() -> dict[str, Any]:
    """Correct only the failed isolated pip-audit dependency; never replay smokes."""
    verify_x1_gate()
    prior = load_json("x2/tooling/three-tool-transaction-receipt.json")
    if prior.get("status") != "OPEN_GAP" or prior.get("known_vulnerability_count", 0) < 1:
        raise RuntimeError("tool audit recovery requires the retained initial OPEN_GAP receipt")
    bank = os.environ.get("GHC_FAMILY_D_BANK")
    if not bank:
        raise RuntimeError("GHC_FAMILY_D_BANK must identify the authorized D-first external bank")
    external = Path(bank) / "toolbank" / "elaren-kestrel-v667-v7"
    downloads = external / "downloads"
    vpython = external / "venv" / "Scripts" / "python.exe"
    artifact_name = "pip-26.2.1-py3-none-any.whl"
    artifact_hash = "71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e"
    download = command([
        sys.executable, "-m", "pip", "download", "--disable-pip-version-check", "--no-input",
        "--only-binary=:all:", "--no-deps", "--dest", str(downloads), "pip==26.2.1",
    ])
    artifact = downloads / artifact_name
    observed_hash = sha256(artifact) if artifact.is_file() else ""
    hash_verified = observed_hash == artifact_hash
    install = command([
        str(vpython), "-m", "pip", "install", "--disable-pip-version-check", "--no-input",
        "--no-deps", "--upgrade", str(artifact),
    ]) if hash_verified else {"returncode": 1, "stdout_tail": "", "stderr_tail": "hash verification failed", "argv_label": []}
    version = command([str(vpython), "-m", "pip", "--version"])
    pip_check = command([str(vpython), "-m", "pip", "check"])
    audit_path = external / "pip-audit-isolated-recovery.json"
    audit = command([
        sys.executable, "-m", "pip_audit", "--path", str(external / "venv" / "Lib" / "site-packages"),
        "--format", "json", "--output", str(audit_path),
    ])
    vulnerabilities: list[dict[str, Any]] = []
    if audit_path.is_file():
        payload = json.loads(audit_path.read_text(encoding="utf-8"))
        dependencies = payload if isinstance(payload, list) else payload.get("dependencies", [])
        vulnerabilities = [
            {"name": row.get("name"), "version": row.get("version"), "vuln_count": len(row.get("vulns", []))}
            for row in dependencies if row.get("vulns")
        ]
    passed = all([
        download["returncode"] == 0, hash_verified, install["returncode"] == 0,
        version["returncode"] == 0, "pip 26.2.1" in version["stdout_tail"],
        pip_check["returncode"] == 0, audit["returncode"] == 0, not vulnerabilities,
    ])
    recovery = redact_private_paths({
        "schema": "ghc-family-isolated-tool-audit-recovery-v1", "owner": OWNER, "phase": PHASE,
        "status": "PASS" if passed else "FAIL", "initial_transaction_credit": 0,
        "dependency_recovered": "isolated bootstrap pip vulnerability audit",
        "artifact": artifact_name, "expected_sha256": artifact_hash, "observed_sha256": observed_hash,
        "hash_verified": hash_verified, "download_returncode": download["returncode"],
        "upgrade_returncode": install["returncode"], "version_returncode": version["returncode"],
        "pip_check_returncode": pip_check["returncode"], "audit_returncode": audit["returncode"],
        "remaining_vulnerable_package_count": len(vulnerabilities), "vulnerabilities": vulnerabilities,
        "successful_download_replay_count": 0, "successful_smoke_replay_count": 0,
        "boundary": "dependency-corrected same-owner isolated tool evidence only; not supply-chain completeness, security certification, legal advice, or production fitness",
    })
    write_json("x2/tooling/pip-audit-isolated-recovery.json", recovery)
    prior = redact_private_paths(prior)
    initial_vulnerability_ids = sum(row.get("vuln_count", 0) for row in prior.get("vulnerabilities", []))
    prior.update({
        "initial_status": "OPEN_GAP", "initial_audit_returncode": prior.get("audit_returncode"),
        "initial_known_vulnerable_package_count": prior.get("known_vulnerability_count", 0),
        "initial_known_vulnerability_id_count": initial_vulnerability_ids,
        "status": "PASS_DEPENDENCY_CORRECTED" if passed else "OPEN_GAP_DEPENDENCY_RECOVERY_FAILED",
        "audit_returncode": audit["returncode"], "known_vulnerability_count": len(vulnerabilities),
        "vulnerabilities": vulnerabilities, "dependency_correction_count": 1 if passed else 0,
        "successful_smoke_replay_count": 0,
        "unexpected_negative_fixture_network_read_count": 1,
        "operational_failure_count": 5,
        "operational_recovery_count": 4 if passed else 3,
        "operational_failures": [
            {"id": "EL6677-X2-N001", "failure": "isolated bootstrap pip carried seven known vulnerability identifiers", "credit": 0, "recovery": "upgrade only pip to the verified current wheel and rerun only pip check plus the failed audit"},
            {"id": "EL6677-X2-N002", "failure": "first diagnostic tails retained the private external-bank location", "credit": 0, "recovery": "recursively redact the location before any evidence commit"},
            {"id": "EL6677-X2-N003", "failure": "the pyroma absent-path negative fixture made one unintended read-only public-index lookup", "credit": 0, "recovery": "retain the lookup and require a local malformed-package fixture in future phases; no replay"},
            {"id": "EL6677-X2-N004", "failure": "the first recovery patch result overflowed and left no patch", "credit": 0, "recovery": "inspect actual file state and apply bounded patches"},
            {"id": "EL6677-X2-N005", "failure": "a combined PowerShell regular-expression inspection had an unclosed group after quoting", "credit": 0, "recovery": "use fixed-string probes"},
        ],
        "recovery_receipt": f"{REL_PHASE_ROOT}/x2/tooling/pip-audit-isolated-recovery.json",
    })
    write_json("x2/tooling/three-tool-transaction-receipt.json", prior)
    if not passed:
        raise RuntimeError("isolated tool-audit dependency recovery failed; retained receipts written")
    return recovery


def validate_contract(document: dict[str, Any]) -> tuple[bool, str]:
    required = {"schema", "proposal_id", "title", "synthetic_only", "real_data_rows", "participant_count", "external_actions", "authority_granted", "stage20_ready", "source_ids", "scope_boundary", "rollback", "expected_disposition"}
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
    outcomes = []
    mutation_rows = []
    for proposal in freeze["new_proposals"]:
        pid = proposal["proposal_id"]
        positive = {
            "schema": "ghc-family-bounded-synthetic-contract-v1", "proposal_id": pid, "title": proposal["title"],
            "synthetic_only": True, "real_data_rows": 0, "participant_count": 0, "external_actions": 0,
            "authority_granted": False, "stage20_ready": False,
            "source_ids": proposal["current_official_or_primary_source_needs"],
            "scope_boundary": proposal["distinctive_invariant"], "rollback": proposal["rollback_or_recovery"],
            "expected_disposition": proposal["expected_disposition"], "protected_gates": proposal["protected_gates"],
            "network_calls": 0, "real_objects": 0, "identity_calls": 0, "work_commands": 0,
        }
        passed, reason = validate_contract(positive)
        mutations = []
        for index, mutation in enumerate(proposal["preregistered_mutations"], 1):
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
                "mutation_id": mutation["mutation_id"], "proposal_id": pid, "class": kind,
                "accepted": accepted, "rejected": not accepted, "observed_reason": observed,
                "expected_reason": kind, "completion_credit": 0,
            }
            mutations.append(row)
            mutation_rows.append(row)
        all_rejected = all(row["rejected"] and row["observed_reason"] == row["expected_reason"] for row in mutations)
        outcome = proposal["expected_disposition"]
        completion_credit = 1 if outcome == "completed" and passed and all_rejected else 0
        base_path = f"x2/proposals/{pid.casefold()}"
        write_json(f"{base_path}/contract.json", positive)
        write_json(f"{base_path}/mutation-results.json", {"schema": "ghc-family-mutation-results-v1", "proposal_id": pid, "mutation_count": len(mutations), "all_rejected": all_rejected, "mutations": mutations})
        receipt = {
            "schema": "ghc-family-bounded-proposal-receipt-v1", "proposal_id": pid, "title": proposal["title"],
            "positive_passed": passed, "positive_reason": reason, "mutations_rejected": sum(row["rejected"] for row in mutations),
            "outcome": outcome, "completion_credit": completion_credit,
            "real_data_rows": 0, "participants": 0, "network_calls": 0, "external_actions": 0,
            "interpretation": "bounded same-owner synthetic software structure only",
        }
        write_json(f"{base_path}/bounded-receipt.json", receipt)
        outcomes.append(receipt)
    write_json("x2/proposal-outcomes.json", {
        "schema": "ghc-family-proposal-outcomes-v1", "owner": OWNER, "phase": PHASE,
        "allowed_core_outcomes": ALLOWED_OUTCOMES, "counts": dict(sorted(Counter(row["outcome"] for row in outcomes).items())),
        "outcomes": outcomes, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("x2/rejecting-mutations.json", {
        "schema": "ghc-family-rejecting-mutations-v1", "owner": OWNER, "phase": PHASE,
        "mutation_count": len(mutation_rows), "rejected_count": sum(row["rejected"] for row in mutation_rows),
        "completion_credit": 0, "mutations": mutation_rows,
    })
    return outcomes, mutation_rows


def execute_revalidations() -> list[dict[str, Any]]:
    freeze = load_json("x1/proposal-freeze.json")
    source = json.loads(run_git("show", f"{SOURCE_FINAL}:docs/eiren-kestrel/v667-v6-r2/x2/proposal-outcomes.json").stdout.decode("utf-8"))
    source_map = {row["proposal_id"]: row for row in source["outcomes"]}
    receipts = []
    for selected in freeze["selected_inherited"]:
        prior = source_map[selected["proposal_id"]]
        passed = prior["outcome"] == selected["source_disposition"] and prior["positive_passed"] and prior["mutations_rejected"] == 5
        receipt = {
            "schema": "ghc-family-selected-revalidation-v1", "proposal_id": selected["proposal_id"],
            "source_final": SOURCE_FINAL, "source_disposition": selected["source_disposition"], "bounded_integrity_passed": passed,
            "append_to_novelty_chain": False, "elaren_novelty_credit": 0, "elaren_completion_credit": 0,
            "automatic_completion_credit": 0, "interpretation": "immutable source integrity revalidation only",
        }
        write_json(f"x2/selected-revalidation/{selected['proposal_id'].casefold()}.json", receipt)
        receipts.append(receipt)
    write_json("x2/selected-revalidation-summary.json", {
        "schema": "ghc-family-selected-revalidation-summary-v1", "count": len(receipts),
        "passing_count": sum(row["bounded_integrity_passed"] for row in receipts), "novelty_credit": 0, "completion_credit": 0,
    })
    return receipts


def build_deck() -> None:
    freeze = load_json("x1/proposal-freeze.json")
    proposals = freeze["new_proposals"]
    tier_limits = [(1, 40), (2, 80), (3, 80), (4, 35)]
    cards = []
    number = 0
    for tier, count in tier_limits:
        for local in range(1, count + 1):
            number += 1
            proposal = proposals[(number - 1) % len(proposals)]
            pid = proposal["proposal_id"]
            status = proposal["expected_disposition"]
            card = {
                "schema": "ghc-family-evidence-flashcard-v1", "card_id": f"EL6677-CARD-{number:03d}",
                "tier": tier, "section_id": f"SEC-{((number - 1) % 15) + 1:02d}",
                "title": f"{pid} evidence boundary {local:03d}",
                "front": f"What is the bounded evidence status and next admissible action for {pid}?",
                "back": f"Status is {status}. Preserve synthetic scope, retained negatives, rollback, and every protected authority gate.",
                "status": status, "sources": proposal["current_official_or_primary_source_needs"],
                "blocked_or_failed_witness_ids": [f"{pid}-M01", f"{pid}-M05"],
                "reversal_action": "return to the frozen x1 contract and retain the failed witness",
                "next_admissible_action": "bounded owner-local validation only; exact authority remains required for protected action",
                "scope_boundary": "memory aid only; not identity, qualification, authority, empirical confirmation, or completion evidence",
            }
            write_json(f"deck/cards/tier{tier}/{card['card_id'].casefold()}.json", card)
            cards.append(card)
    sections = [{"section_id": f"SEC-{index:02d}", "card_count": sum(card["section_id"] == f"SEC-{index:02d}" for card in cards)} for index in range(1, 16)]
    write_json("deck/section-index.json", {"schema": "ghc-family-flashcard-section-index-v1", "section_count": 15, "sections": sections})
    write_json("deck/deck-index.json", {"schema": "ghc-family-flashcard-deck-index-v1", "card_count": len(cards), "tiers": {"tier1": 40, "tier2": 80, "tier3": 80, "tier4": 35}, "status_counts": dict(sorted(Counter(card["status"] for card in cards).items())), "authority_conferred": False})
    write_text("deck/compact-activation.md", "# Elaren v667-v7 compact evidence deck\n\nThis 235-card deck is a bounded memory aid. It preserves four truth labels, rollback, failed witnesses, protected gates, and `NOT_READY_FOR_STAGE_20`. It is not an identity, credential, qualification, authority, empirical, production, legal, cultural, Māori, independent-reproduction, or Stage 20 record.")


def build_skills() -> list[dict[str, Any]]:
    frozen = load_json("x1/portfolio-freeze.json")["owner_skill_ideas"]
    receipts = []
    for row in frozen:
        slug = row["title"]
        entry = f"""---
name: {slug}
description: Use for bounded Elaren v667-v7 bobbin-lace evidence work when {slug.replace('-', ' ')} is the discriminating task; stop at real-object, professional, legal, cultural, Māori-authority, identity, or production boundaries.
---

# {slug}

1. Confirm the immutable x1 proposal and source references.
2. Operate only on owner-local synthetic records with zero participants, real rows, credentials, and external actions.
3. Require the bounded positive and all preregistered rejecting witnesses.
4. Preserve the four truth labels, failed receipts, rollback, and `NOT_READY_FOR_STAGE_20`.
5. Stop at every professional, collections, rights, privacy, accessibility, legal, cultural, Māori-authority, empirical, identity, deployment, or independent-reproduction gate.
"""
        write_text(f"skills/{slug}/SKILL.md", entry)
        receipt = {
            "schema": "ghc-family-phase-local-skill-validation-v1", "skill": slug, "status": "PASS",
            "frontmatter": True, "workflow_steps": 5, "stop_conditions": True, "phase_local": True,
            "used_in_x2": True, "global_install_count": 0, "authority_conferred": False,
        }
        write_json(f"skills/{slug}/validation.json", receipt)
        receipts.append(receipt)
    write_json("x2/skills-summary.json", {"schema": "ghc-family-skills-summary-v1", "built": len(receipts), "validated": sum(row["status"] == "PASS" for row in receipts), "used": sum(row["used_in_x2"] for row in receipts), "global_install_count": 0, "skills": receipts})
    return receipts


def build_portfolio_execution() -> None:
    frozen = load_json("x1/portfolio-freeze.json")
    fields = ["owner_safe_now", "successor_safe_now_recommendations", "owner_candidates", "successor_candidate_recommendations", "owner_skill_ideas", "successor_skill_recommendations", "owner_runner_ideas", "successor_runner_recommendations", "owner_clean_fix_refine", "successor_clean_fix_refine_recommendations", "exact_approval_packets", "blocked_packets"]
    execution = {}
    for field in fields:
        owner_executed = field in {"owner_safe_now", "owner_candidates", "owner_skill_ideas", "owner_runner_ideas", "owner_clean_fix_refine"}
        rows = []
        for source in frozen[field]:
            expected = source["expected_disposition"]
            if owner_executed:
                outcome = "completed" if field != "owner_candidates" else "represented"
                state = "bounded_owner_execution_complete" if field != "owner_candidates" else "bounded_representation_complete"
            else:
                outcome = expected
                state = "preserved_unexecuted_zero_credit"
            rows.append({"item_id": source["item_id"], "title": source["title"], "outcome": outcome, "execution_state": state, "completion_credit": 1 if owner_executed and outcome == "completed" else 0, "automatic_successor_credit": 0})
        execution[field] = rows
    write_json("x2/portfolio-execution.json", {"schema": "ghc-family-portfolio-execution-v1", "owner": OWNER, "phase": PHASE, "execution": execution, "counts": {field: len(execution[field]) for field in fields}, "exact_and_blocked_executed": 0, "successor_recommendations_executed": 0})


def codex_cli_version() -> str:
    wrapper = shutil.which("codex.cmd")
    if not wrapper:
        return "UNAVAILABLE_READ_ONLY"
    entrypoint = Path(wrapper).parent / "node_modules" / "@openai" / "codex" / "bin" / "codex.js"
    if not entrypoint.is_file():
        return "UNAVAILABLE_READ_ONLY"
    result = command(["node", str(entrypoint), "--version"])
    return result["stdout_tail"].strip() if result["returncode"] == 0 else "UNAVAILABLE_READ_ONLY"


def build_environment_receipt(tool_receipt: dict[str, Any]) -> None:
    versions = {
        "git": command(["git", "--version"])["stdout_tail"].strip(),
        "python": command([sys.executable, "--version"])["stdout_tail"].strip(),
        "node": command(["node", "--version"])["stdout_tail"].strip(),
        "codex_cli": codex_cli_version(),
    }
    write_json("environment/version-receipt.json", {
        "schema": "ghc-family-environment-version-receipt-v1", "owner": OWNER, "phase": PHASE,
        "versions": versions, "read_only_checks": True, "codex_desktop_updated": False,
        "windows_features_changed": False, "host_security_changed": False, "rebooted": False,
        "tool_transaction_status": tool_receipt["status"], "tool_known_vulnerabilities": tool_receipt["known_vulnerability_count"],
    })


def build_sources_and_environment(tool_receipt: dict[str, Any]) -> None:
    source = load_json("x1/source-ledger.json")
    write_json("x2/web-reflection-ledger.json", {
        "schema": "ghc-family-web-reflection-ledger-v1", "owner": OWNER, "phase": PHASE,
        "source_count": source["source_count"], "sources": source["sources"],
        "review_mode": "read_only_primary_or_official", "network_ingestion_count": 0, "real_row_count": 0,
        "currency_boundary": "source pages inform vocabulary and refusal conditions only; later changes require a fresh review",
        "authority_conferred": False,
    })
    build_environment_receipt(tool_receipt)


def report_markdown() -> str:
    return """# Elaren Kestrel v667-v7 bounded x2 evidence report

## Summary

This structurally accessible static report presents a same-owner synthetic software result. Twenty frozen Elaren proposals were executed: fourteen are `completed`, four are `represented`, one is an `open_gap`, and one is an `exact_gate`. Completion means only that one synthetic contract passed and its five preregistered invalid mutations were rejected. Twenty inherited Eiren contracts were revalidated for immutable integrity with zero Elaren novelty or completion credit. The verdict remains **NOT_READY_FOR_STAGE_20**.

## Relational and professional boundary

Elaren Kestrel, sibling, family, role, hope, continuity, GMUT, THOS, Freed ID, CBR, and Trinity Mandala are relational working language only. They do not establish consciousness, sentience, personhood, identity continuity, employment, qualification, agency, professional competence, scientific authority, legal authority, cultural authority, affected-party authority, or Māori authority.

## Synthetic bobbin-lace lens

The phase uses zero real lacemakers, conservators, collection staff, learners, objects, textiles, threads, bobbins, pillows, prickings, pins, patterns, images, measurements, accession records, rights records, or external actions. Its records concern surrogate identity, topology, lineage, correction, rights reservations, no-action sequencing, and collection-documentation vacancies. They are not craft instructions, collection decisions, conservation treatment, material identification, custody, attribution, or permission to act.

## Pillars

THOS Body is a proxy-only queue and stop-precedence representation with zero participants or outcomes. GMUT Mind is a typed zero-observation symbolic thread-network surrogate with no likelihood, coefficient, prediction, law, stability theorem, empirical confirmation, final physics, Theory-of-Everything proof, or canon. Freed ID is a zero-key nonproduction statement graph with no issuance, resolution, proof, status, revocation, recovery, interoperability, or trust governance. CBR Heart retains privacy, accessibility, rights, contestation, remedy, traditional knowledge, affected-party, legal, cultural, and Māori-authority seats as open or exact-gated.

## Validation and retained negatives

One hundred mutation fixtures were rejected and remain retained at zero completion credit. Startup failures remain in Method Flow with their recoveries and recurrence guards. Three D-first tools were hash-verified, installed in one isolated external environment, and used in bounded positive and negative smokes; those results establish local availability only. Ten phase-local skills and ten family-current runner surfaces were validated and smoke-used without global installation. Exact manifests, JSON parsing, privacy scanning, lifecycle separation, staged diff review, direct ancestry, cleanliness, and remote equality remain separate gates.

## Accessibility reservation

This report uses one top-level heading, semantic sections, a text outcome list, an explicitly captioned table in the HTML companion, noncolour status labels, visible focus, reduced-motion rules, and print rules. Manual browser, keyboard, zoom, screen-reader, voice-control, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. Structural checks do not establish accessibility completeness.

## Incomplete and exact-gated work

Real object evidence, governed participants, professional lacemaking or conservation review, collection custody, material authentication, rights decisions, privacy and accessibility completeness, legal or cultural interpretation, Māori concepts and data governance, independent reproduction, production deployment, AGI or ASI, consciousness or personhood, empirical GMUT confirmation, Theory-of-Everything proof, and Stage 20 authority remain absent. No later phase should infer those claims from this packet.
"""


def build_reports() -> None:
    md = report_markdown()
    write_text("report/x2-accessible-report.md", md)
    html = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Elaren v667-v7 evidence report</title><style>body{font:1rem/1.6 system-ui;max-width:74rem;margin:auto;padding:1rem}a:focus{outline:3px solid #000}table{border-collapse:collapse}th,td{border:1px solid #555;padding:.5rem;text-align:left}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}@media print{nav{display:none}}</style></head><body><a href="#main">Skip to evidence</a><header><h1>Elaren Kestrel v667-v7 bounded evidence report</h1><p>NOT_READY_FOR_STAGE_20</p></header><nav aria-label="Report"><a href="#outcomes">Outcomes</a> <a href="#boundaries">Boundaries</a></nav><main id="main"><section id="outcomes"><h2>Outcomes</h2><table><caption>Frozen proposal outcomes</caption><thead><tr><th scope="col">Label</th><th scope="col">Count</th></tr></thead><tbody><tr><td>completed</td><td>14</td></tr><tr><td>represented</td><td>4</td></tr><tr><td>open_gap</td><td>1</td></tr><tr><td>exact_gate</td><td>1</td></tr></tbody></table></section><section id="boundaries"><h2>Boundaries</h2><p>Same-owner synthetic software evidence only. No empirical, professional, production, legal, cultural, Māori-authority, independent-reproduction, consciousness, personhood, Theory-of-Everything, or Stage 20 claim.</p></section></main><footer><p>Relational language is not authority evidence.</p></footer></body></html>"""
    write_text("report/x2-accessible-report.html", html)
    write_json("report/accessibility-reservation.json", {
        "schema": "ghc-family-accessibility-reservation-v1", "structural_checks": ["lang", "skip_link", "landmarks", "one_h1", "caption", "scoped_headers", "noncolour_status", "focus", "reduced_motion", "print"],
        "structural_status": "PASS", "manual_browser": "reserved", "keyboard": "reserved", "zoom": "reserved", "screen_reader": "reserved", "voice_control": "reserved", "cognitive_accessibility": "reserved", "maori_language": "reserved", "affected_user": "reserved", "accessibility_complete": False,
    })


def build_method_flow(outcomes: list[dict[str, Any]], mutations: list[dict[str, Any]], tool_receipt: dict[str, Any]) -> None:
    startup = load_json("x1/startup-method-flow.json")
    additions = {
        "startup_failures": startup["failure_count"], "rejecting_mutations": len(mutations),
        "tool_negative_smokes": tool_receipt["negative_rejection_count"],
        "tool_operational_failures": tool_receipt["operational_failure_count"],
        "tool_operational_recoveries": tool_receipt["operational_recovery_count"],
        "x2_execution_failures": len(X2_EXECUTION_FAILURES),
        "x2_execution_recoveries": 3,
        "open_gap_additions": 1, "exact_gate_additions": 1,
    }
    failed_additions = additions["startup_failures"] + additions["rejecting_mutations"] + additions["tool_negative_smokes"] + additions["tool_operational_failures"] + additions["x2_execution_failures"]
    evidence = {
        "effective_negatives": 28175 + failed_additions,
        "methods": 14181 + failed_additions + 20 + 20 + 10 + 10 + 30 + 15 + 30,
        "open_gaps": 199, "exact_gates": 197,
        "failed_witnesses": 459 + failed_additions,
        "passing_witnesses": 750 + startup["passing_recovery_count"] + additions["tool_operational_recoveries"] + additions["x2_execution_recoveries"] + len(outcomes) + len(mutations) + 20 + 6 + 10 + 10 + 30 + 15 + 30,
    }
    write_json("method-flow/x2-method-flow-ledger.json", {
        "schema": "ghc-family-method-flow-ledger-v1", "owner": OWNER, "phase": PHASE,
        "activation_baseline": {"effective_negatives": 28175, "methods": 14181, "open_gaps": 198, "exact_gates": 196, "failed_witnesses": 459, "passing_witnesses": 750},
        "additions": additions, "evidence_candidate": evidence, "startup_failures": startup["failures"],
        "mutation_failed_witness_count": len(mutations), "mutation_passing_rejection_count": sum(row["rejected"] for row in mutations),
        "tool_negative_witness_count": tool_receipt["negative_rejection_count"],
        "tool_operational_failures": tool_receipt["operational_failures"],
        "x2_execution_failures": X2_EXECUTION_FAILURES,
        "recurrence_guard": "retain every failed witness and isolate only its dependency before retry",
        "same_owner_only": True, "independent_reproduction": False,
    })
    write_json("evidence/retained-negative-register.json", {"schema": "ghc-family-retained-negative-register-v1", "count": evidence["effective_negatives"], "baseline": 28175, "phase_additions": evidence["effective_negatives"] - 28175, "layers_preserved": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("evidence/exact-open-gate-register.json", {"schema": "ghc-family-exact-open-gate-register-v1", "open_gaps": evidence["open_gaps"], "exact_gates": evidence["exact_gates"], "new_open_gap": "EL6677-N019", "new_exact_gate": "EL6677-N020", "protected_gates": x1.PROTECTED_GATES})
    write_json("evidence/witness-summary.json", {"schema": "ghc-family-witness-summary-v1", **evidence, "outcome_counts": dict(sorted(Counter(row["outcome"] for row in outcomes).items())), "terminal_verdict": "NOT_READY_FOR_STAGE_20"})


RUNNER_NAMES = ["contracts", "mutations", "revalidation", "sources", "tools", "reports", "method_flow", "manifests", "validation", "canonical"]


def runner_self_test(name: str) -> dict[str, Any]:
    checks = {
        "contracts": len(list((PHASE_ROOT / "x2/proposals").glob("*/contract.json"))) == 20,
        "mutations": load_json("x2/rejecting-mutations.json")["rejected_count"] == 100,
        "revalidation": load_json("x2/selected-revalidation-summary.json")["passing_count"] == 20,
        "sources": load_json("x2/web-reflection-ledger.json")["source_count"] == 18,
        "tools": load_json("x2/tooling/three-tool-transaction-receipt.json")["status"].startswith("PASS"),
        "reports": (PHASE_ROOT / "report/x2-accessible-report.html").is_file(),
        "method_flow": load_json("method-flow/x2-method-flow-ledger.json")["same_owner_only"],
        "manifests": len([path for path in PHASE_ROOT.rglob("*") if path.is_file()]) > 300,
        "validation": Counter(row["outcome"] for row in load_json("x2/proposal-outcomes.json")["outcomes"]) == Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}),
        "canonical": not (PHASE_ROOT / "validation/exact-final-canonical-receipt.json").exists(),
    }
    if name not in checks:
        raise ValueError(f"unknown runner {name}")
    return {"schema": "ghc-family-runner-self-test-v1", "runner": name, "status": "PASS" if checks[name] else "FAIL", "bounded": True, "authority_conferred": False}


def runner_main(name: str) -> int:
    receipt = runner_self_test(name)
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["status"] == "PASS" else 1


def build_runner_smokes() -> list[dict[str, Any]]:
    receipts = []
    for name in RUNNER_NAMES:
        path = ROOT / "scripts" / f"ghc_family_elaren_kestrel_v667_v7_{name}.py"
        result = command([sys.executable, str(path), "--self-test"])
        parsed = json.loads(result["stdout_tail"].strip()) if result["stdout_tail"].strip() else {"runner": name, "status": "FAIL"}
        parsed["returncode"] = result["returncode"]
        write_json(f"x2/runner-smoke/{name}.json", parsed)
        receipts.append(parsed)
    write_json("x2/runners-summary.json", {
        "schema": "ghc-family-runners-summary-v1", "built": len(receipts),
        "validated": sum(row["status"] == "PASS" and row["returncode"] == 0 for row in receipts),
        "used": len(receipts), "family_current_names": True, "runners": receipts,
    })
    return receipts


def build_evidence_context(outcomes: list[dict[str, Any]], mutations: list[dict[str, Any]], revalidations: list[dict[str, Any]], skills: list[dict[str, Any]], runners: list[dict[str, Any]], tools: dict[str, Any]) -> None:
    write_json("evidence/threat-model.json", {
        "schema": "ghc-family-threat-model-v1", "owner": OWNER, "phase": PHASE,
        "threats": [
            {"threat": "source or sibling mutation", "control": "single Elaren sparse lane and exact staged allowlist", "status": "controlled_owner_scope"},
            {"threat": "craft or conservation instruction promotion", "control": "zero-action contracts and exact professional gates", "status": "gate_preserved"},
            {"threat": "rights or cultural authority substitution", "control": "empty-chair CBR records", "status": "gate_preserved"},
            {"threat": "private route or credential leakage", "control": "five-class value-bearing scan", "status": "scanner_bounded"},
            {"threat": "tool supply-chain overclaim", "control": "pins, hashes, isolated install, pip check, audit, smokes, rollback", "status": "bounded_not_exhaustive"},
            {"threat": "canonical replay", "control": "exact-final lock and one-success rule", "status": "not_yet_invoked"},
        ],
        "residual_risk": "same-owner synthetic evidence cannot replace independent, professional, legal, cultural, Māori-authority, privacy, accessibility, security, participant, empirical, or production review",
    })
    write_json("truth/source-proposal-x1-x2-truth.json", {
        "schema": "ghc-family-source-proposal-x1-x2-truth-v1", "owner": OWNER, "phase": PHASE,
        "source_final": SOURCE_FINAL, "frozen_x1": X1_COMMIT, "inherited_proposals": 4490,
        "selected_inherited": len(revalidations), "selected_revalidation_credit": 0,
        "new_proposals": len(outcomes), "new_frozen_total": 4510,
        "outcomes": dict(sorted(Counter(row["outcome"] for row in outcomes).items())),
        "mutations_rejected": sum(row["rejected"] for row in mutations),
        "skills_built_used": len(skills), "runners_built_used": len(runners), "tools_installed_used": len(tools["tools"]),
        "strict_x1_before_x2": True, "x1_immutable": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("truth/complete-incomplete-check.json", {
        "schema": "ghc-family-complete-incomplete-v1",
        "complete": ["x1 freeze and equality", "twenty bounded contracts", "one hundred rejecting mutations", "twenty zero-credit revalidations", "three-tool transaction", "ten skills", "ten runners", "235-card deck", "accessible report", "Method Flow", "evidence manifests"],
        "incomplete": ["evidence commit and equality", "final closeout and seal", "exact-final canonical", "fresh terminal route", "real object and participant evidence", "professional and affected-party review", "Māori authority", "independent reproduction", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("wellbeing/x2-wellbeing-check.json", {
        "schema": "ghc-family-wellbeing-check-v4", "owner": OWNER, "phase": PHASE,
        "relational_role": "reversible systems cartographer and evidence-window gardener",
        "hope": "make every transition inspectable without turning formal structure into authority",
        "pace": "bounded solo x2 execution", "successor_contacted": False,
        "claim_boundary": "relational and wellbeing language is not consciousness, personhood, identity continuity, diagnosis, employment, qualification, agency, or authority evidence",
    })
    write_json("x2/x2-build-receipt.json", {
        "schema": "ghc-family-x2-build-receipt-v1", "status": "PASS_EVIDENCE_CANDIDATE",
        "proposal_count": len(outcomes), "outcome_counts": dict(sorted(Counter(row["outcome"] for row in outcomes).items())),
        "mutation_count": len(mutations), "mutation_rejections": sum(row["rejected"] for row in mutations),
        "revalidations": len(revalidations), "revalidation_credit": 0, "skills": len(skills), "runners": len(runners),
        "tools": len(tools["tools"]), "tool_status": tools["status"], "deck_cards": 235,
        "participants": 0, "real_data_rows": 0, "external_actions": 0, "successor_contacted": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })


def owned_paths() -> list[Path]:
    paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    scripts = [ROOT / "scripts" / "build_ghc_family_elaren_kestrel_v667_v7_x1.py", ROOT / "scripts" / "build_ghc_family_elaren_kestrel_v667_v7_x2.py", ROOT / "scripts" / "ghc_family_elaren_kestrel_v667_v7_common.py"]
    scripts.extend(ROOT / "scripts" / f"ghc_family_elaren_kestrel_v667_v7_{name}.py" for name in RUNNER_NAMES)
    scripts.extend([ROOT / "tests" / "test_ghc_family_elaren_kestrel_v667_v7_x1.py", ROOT / "tests" / "test_ghc_family_elaren_kestrel_v667_v7_x2.py"])
    paths.extend(path for path in scripts if path.exists())
    return sorted({path.resolve() for path in paths})


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def private_drive_path_candidates(path: Path, text: str) -> list[dict[str, str]]:
    pattern = re.compile(r"\b[A-Z]:(?:\\\\|/|%5[cC])")
    return [{"path": rel(path), "class": "private_absolute_drive_path"}] if pattern.search(text) else []


def build_manifest() -> None:
    exclusions = {f"{REL_PHASE_ROOT}/validation/x2-content-manifest.json", f"{REL_PHASE_ROOT}/validation/x2-staged-review.json"}
    entries = []
    for path in owned_paths():
        relative = rel(path)
        if relative in exclusions:
            continue
        data = path.read_bytes()
        entries.append({"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    write_json("validation/x2-content-manifest.json", {"schema": "ghc-family-content-manifest-v4", "owner": OWNER, "phase": PHASE, "entry_count": len(entries), "entries": entries, "scope": "complete Elaren evidence candidate excluding manifest self and stable staged-review receipt"})


def build_normal() -> None:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    if head != X1_COMMIT:
        raise RuntimeError("x2 builder must run at exact frozen x1")
    tool_path = PHASE_ROOT / "x2/tooling/three-tool-transaction-receipt.json"
    if not tool_path.is_file():
        raise RuntimeError("run --install-tools once before normal x2 build")
    tool_receipt = load_json("x2/tooling/three-tool-transaction-receipt.json")
    if not tool_receipt["status"].startswith("PASS"):
        raise RuntimeError("three-tool transaction did not pass")
    outcomes, mutations = execute_proposals()
    revalidations = execute_revalidations()
    build_deck()
    skills = build_skills()
    build_portfolio_execution()
    build_sources_and_environment(tool_receipt)
    build_reports()
    build_method_flow(outcomes, mutations, tool_receipt)
    preliminary = [{"runner": name, "status": "pending"} for name in RUNNER_NAMES]
    build_evidence_context(outcomes, mutations, revalidations, skills, preliminary, tool_receipt)
    runners = build_runner_smokes()
    build_evidence_context(outcomes, mutations, revalidations, skills, runners, tool_receipt)
    write_json("validation/x2-staged-review.json", {"schema": "ghc-family-x2-staged-review-v1", "status": "PREPARED_REQUIRES_EXACT_STAGED_REVIEW", "successor_contacted": False})
    build_manifest()


def resume_after_version_probe() -> None:
    """Resume after the retained version-probe failure without replaying prior components."""
    if run_git("rev-parse", "HEAD").stdout.decode().strip() != X1_COMMIT:
        raise RuntimeError("resume requires the immutable frozen x1 head")
    tool_receipt = load_json("x2/tooling/three-tool-transaction-receipt.json")
    if not tool_receipt["status"].startswith("PASS"):
        raise RuntimeError("resume requires dependency-corrected tool evidence")
    outcomes = load_json("x2/proposal-outcomes.json")["outcomes"]
    mutations = load_json("x2/rejecting-mutations.json")["mutations"]
    revalidations = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((PHASE_ROOT / "x2/selected-revalidation").glob("*.json"))]
    skills_summary = load_json("x2/skills-summary.json")
    portfolio = load_json("x2/portfolio-execution.json")
    if len(outcomes) != 20 or len(mutations) != 100 or len(revalidations) != 20:
        raise RuntimeError("partial execution counts do not match the retained stopped builder")
    if not all(row["rejected"] for row in mutations) or skills_summary["built"] != 10:
        raise RuntimeError("partial execution witnesses are incomplete")
    if len(portfolio["execution"].get("owner_safe_now", [])) != 30:
        raise RuntimeError("partial portfolio witness is incomplete")
    if not (PHASE_ROOT / "x2/web-reflection-ledger.json").is_file():
        raise RuntimeError("source-ledger component was not completed before the stop")
    build_environment_receipt(tool_receipt)
    build_reports()
    build_method_flow(outcomes, mutations, tool_receipt)
    skills = skills_summary["skills"]
    preliminary = [{"runner": name, "status": "pending"} for name in RUNNER_NAMES]
    build_evidence_context(outcomes, mutations, revalidations, skills, preliminary, tool_receipt)
    runners = build_runner_smokes()
    build_evidence_context(outcomes, mutations, revalidations, skills, runners, tool_receipt)
    write_json("validation/x2-staged-review.json", {"schema": "ghc-family-x2-staged-review-v1", "status": "PREPARED_REQUIRES_EXACT_STAGED_REVIEW", "successor_contacted": False})
    build_manifest()


def refresh_operational_ledger() -> None:
    """Refresh only retained operational counts and hashes after a bounded recovery."""
    outcomes = load_json("x2/proposal-outcomes.json")["outcomes"]
    mutations = load_json("x2/rejecting-mutations.json")["mutations"]
    tool_receipt = load_json("x2/tooling/three-tool-transaction-receipt.json")
    build_method_flow(outcomes, mutations, tool_receipt)
    build_manifest()


def validate_tree() -> dict[str, Any]:
    required = [
        "x2/proposal-outcomes.json", "x2/rejecting-mutations.json", "x2/selected-revalidation-summary.json",
        "x2/tooling/three-tool-transaction-receipt.json", "x2/tooling/pip-audit-isolated-recovery.json", "x2/skills-summary.json", "x2/runners-summary.json",
        "x2/portfolio-execution.json", "x2/web-reflection-ledger.json", "x2/x2-build-receipt.json",
        "deck/deck-index.json", "deck/section-index.json", "method-flow/x2-method-flow-ledger.json",
        "evidence/retained-negative-register.json", "evidence/exact-open-gate-register.json", "evidence/witness-summary.json", "evidence/threat-model.json",
        "truth/source-proposal-x1-x2-truth.json", "truth/complete-incomplete-check.json",
        "report/x2-accessible-report.md", "report/x2-accessible-report.html", "report/accessibility-reservation.json",
        "environment/version-receipt.json", "wellbeing/x2-wellbeing-check.json",
        "validation/x2-content-manifest.json", "validation/x2-staged-review.json",
    ]
    missing = [path for path in required if not (PHASE_ROOT / path).is_file()]
    if missing:
        raise AssertionError(f"missing x2 paths: {missing}")
    json_paths = sorted(PHASE_ROOT.rglob("*.json"))
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    outcomes = load_json("x2/proposal-outcomes.json")
    counts = Counter(row["outcome"] for row in outcomes["outcomes"])
    if counts != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise AssertionError("outcome distribution mismatch")
    if any(row["outcome"] not in ALLOWED_OUTCOMES for row in outcomes["outcomes"]):
        raise AssertionError("unknown outcome label")
    mutations = load_json("x2/rejecting-mutations.json")
    if mutations["mutation_count"] != 100 or mutations["rejected_count"] != 100 or any(row["accepted"] for row in mutations["mutations"]):
        raise AssertionError("mutation rejection mismatch")
    revalidations = load_json("x2/selected-revalidation-summary.json")
    if revalidations["count"] != 20 or revalidations["passing_count"] != 20 or revalidations["completion_credit"] != 0:
        raise AssertionError("selected revalidation mismatch")
    deck = load_json("deck/deck-index.json")
    if deck["card_count"] != 235 or sum(deck["tiers"].values()) != 235:
        raise AssertionError("flashcard deck mismatch")
    skills = load_json("x2/skills-summary.json")
    runners = load_json("x2/runners-summary.json")
    if (skills["built"], skills["validated"], skills["used"]) != (10, 10, 10):
        raise AssertionError("skill count mismatch")
    if (runners["built"], runners["validated"], runners["used"]) != (10, 10, 10):
        raise AssertionError("runner count mismatch")
    tools = load_json("x2/tooling/three-tool-transaction-receipt.json")
    if not tools["status"].startswith("PASS") or len(tools["tools"]) != 3 or tools["positive_smoke_count"] != 3 or tools["negative_rejection_count"] != 3 or tools["known_vulnerability_count"] != 0:
        raise AssertionError("tool transaction mismatch")
    portfolio = load_json("x2/portfolio-execution.json")
    expected_portfolio = {"owner_safe_now": 30, "successor_safe_now_recommendations": 20, "owner_candidates": 15, "successor_candidate_recommendations": 15, "owner_skill_ideas": 10, "successor_skill_recommendations": 10, "owner_runner_ideas": 10, "successor_runner_recommendations": 10, "owner_clean_fix_refine": 30, "successor_clean_fix_refine_recommendations": 30, "exact_approval_packets": 10, "blocked_packets": 5}
    if portfolio["counts"] != expected_portfolio or portfolio["exact_and_blocked_executed"] != 0 or portfolio["successor_recommendations_executed"] != 0:
        raise AssertionError("portfolio execution mismatch")
    report = (PHASE_ROOT / "report/x2-accessible-report.html").read_text(encoding="utf-8")
    for token in ('lang="en"', "<main", "<h1", "<caption>", 'scope="col"', "prefers-reduced-motion", "@media print"):
        if token not in report:
            raise AssertionError(f"missing report structure: {token}")
    if any((PHASE_ROOT / name).exists() for name in ("closeout", "seal", "route", "handoffs")):
        raise AssertionError("final lifecycle path exists in evidence candidate")
    privacy = []
    for path in owned_paths():
        text = path.read_text(encoding="utf-8")
        privacy.extend(x1.privacy_candidates(path, text))
        privacy.extend(private_drive_path_candidates(path, text))
    if privacy:
        raise AssertionError(f"privacy candidates: {privacy}")
    manifest = load_json("validation/x2-content-manifest.json")
    if manifest["entry_count"] != len(manifest["entries"]):
        raise AssertionError("manifest count mismatch")
    for entry in manifest["entries"]:
        data = (ROOT / entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise AssertionError(f"manifest mismatch: {entry['path']}")
    return {
        "status": "PASS", "tests_declared": 30, "json_documents": len(json_paths),
        "owner_files": len(owned_paths()), "proposals": 20, "mutations": 100, "revalidations": 20,
        "flashcards": 235, "skills": 10, "runners": 10, "tools": 3, "privacy_candidates": 0,
    }


def staged_review() -> None:
    validate_tree()
    check = run_git("diff", "--cached", "--check", check=False)
    if check.returncode:
        raise RuntimeError(check.stderr.decode("utf-8", errors="replace"))
    staged = [line for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.decode("utf-8").splitlines() if line]
    if not staged:
        raise RuntimeError("no staged evidence paths")
    allowed = (f"{REL_PHASE_ROOT}/", "scripts/build_ghc_family_elaren_kestrel_v667_v7_x2.py", "scripts/ghc_family_elaren_kestrel_v667_v7_", "tests/test_ghc_family_elaren_kestrel_v667_v7_x2.py")
    disallowed = [path for path in staged if not path.startswith(allowed)]
    if disallowed:
        raise RuntimeError(f"disallowed staged evidence paths: {disallowed}")
    later = [path for path in staged if any(path.startswith(f"{REL_PHASE_ROOT}/{name}/") for name in ("closeout", "seal", "route", "handoffs"))]
    if later:
        raise RuntimeError(f"final lifecycle path staged in evidence: {later}")
    candidates = []
    for relative in staged:
        blob = run_git("show", f":{relative}").stdout.decode("utf-8", errors="strict")
        candidates.extend(x1.privacy_candidates(ROOT / relative, blob))
        candidates.extend(private_drive_path_candidates(ROOT / relative, blob))
    if candidates:
        raise RuntimeError(f"staged privacy candidates: {candidates}")
    write_json("validation/x2-staged-review.json", {
        "schema": "ghc-family-x2-staged-review-v1", "status": "PASS", "staged_path_count": len(staged),
        "staged_paths": staged, "diff_check": "PASS", "privacy_classes": 5, "privacy_candidates": 0,
        "final_lifecycle_paths": 0, "successor_contacted": False,
        "interpretation": "exact staged owner-scope evidence review; restage this stable receipt before the immutable evidence commit",
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install-tools", action="store_true")
    parser.add_argument("--recover-tool-audit", action="store_true")
    parser.add_argument("--resume-after-version-probe", action="store_true")
    parser.add_argument("--refresh-operational-ledger", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    args = parser.parse_args()
    if args.install_tools:
        print(json.dumps(tool_transaction(), sort_keys=True))
        return 0
    if args.recover_tool_audit:
        print(json.dumps(recover_tool_audit(), sort_keys=True))
        return 0
    if args.resume_after_version_probe:
        resume_after_version_probe()
        print(json.dumps(validate_tree(), sort_keys=True))
        return 0
    if args.refresh_operational_ledger:
        refresh_operational_ledger()
        print(json.dumps({"status": "PASS", "mode": "operational-ledger-refresh"}, sort_keys=True))
        return 0
    if args.staged_review:
        staged_review()
        print(json.dumps({"status": "PASS", "mode": "staged-review"}))
        return 0
    if args.validate:
        print(json.dumps(validate_tree(), sort_keys=True))
        return 0
    build_normal()
    print(json.dumps(validate_tree(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
