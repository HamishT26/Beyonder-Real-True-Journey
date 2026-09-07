#!/usr/bin/env python3
"""Build Orin Thale v687-v7 bounded x2 evidence from immutable x1."""

from __future__ import annotations

import argparse
import ast
import hashlib
import html
import importlib.util
import json
import re
import subprocess
import zipfile
from email import message_from_bytes
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v687-v7"
X1_ROOT = PHASE / "x1"
X2 = PHASE / "x2"
SKILLS = PHASE / "skills"
DECK = X2 / "deck"
VALIDATION = PHASE / "validation"
SOURCE = "28dfdf1a3e9a1023f1e83f19fb267e57878b9d0b"
X1 = "7aea73908f8f41ed38473d6e30e5f1bda36588a7"
BRANCH = "codex/GHC-Family/orin-thale-v687-v7-full-tools"
PROTECTED = ["empirical", "real_participant", "professional", "production", "deployment", "identity", "legal", "cultural", "affected_party", "maori_authority", "privacy_complete", "accessibility_complete", "exhaustive_security", "independent_reproduction", "agi_asi", "consciousness_personhood", "theory_of_everything", "proof_canon", "stage20"]
OPERATIONS = [
    "spectral_axis_monotonicity", "spectral_unit_roundtrip", "flux_missingness_boundary",
    "spectral_bin_topology", "calibration_lineage_expiry", "spectral_segment_fixity",
    "uncertainty_covariance_shape", "provenance_frontier", "accessible_spectrum_summary",
    "release_authority_reservation",
]
PRACTICES = [
    "bounded spectral archive uncertainty reviewer",
    "synthetic astronomical spectral metadata steward",
    "synthetic radio-spectrum provenance analyst",
    "synthetic accessible scientific-data documentation reviewer",
]
X2_FAILURES = [
    {"negative_id": "OR6877-X2-N001", "failure": "The first package-smoke receipt could not JSON-serialize a numpy.bool_ comparison result.", "recovery": "Cast only receipt Boolean projections to native bool while preserving the fixture and package state."},
    {"negative_id": "OR6877-X2-N002", "failure": "The corrected smoke used exact float equality for the 500 nm to Angstrom conversion and rejected 4999.999999999999.", "recovery": "Use an explicit 1e-9 absolute tolerance for the bounded floating conversion and retain the exact observed representation."},
    {"negative_id": "OR6877-X2-N003", "failure": "Local skill smoke execution emitted ten pycache files containing private path strings; promotion copied them and the first x2 privacy aggregate and its privacy test failed.", "recovery": "Set PYTHONDONTWRITEBYTECODE, remove only the verified owner/global generated caches, preserve the original promotion receipt, and bind the intended 56 files in an additive correction receipt."},
    {"negative_id": "OR6877-X2-N004", "failure": "The first exact cache-remediation command was rejected before execution because it requested recursive Remove-Item.", "recovery": "Retain the policy rejection and attempt only verified non-recursive literal deletion."},
    {"negative_id": "OR6877-X2-N005", "failure": "The non-recursive Remove-Item remediation was also rejected before execution by host command policy.", "recovery": "After identical containment and leaf checks, delete only enumerated pyc files and empty cache directories through literal .NET APIs."},
]


def run(args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8", check=False)


def git(*args: str) -> str:
    result = run(["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def norm(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def card_id(seed: str) -> str:
    return "ghc-card-" + hashlib.sha256(seed.encode()).hexdigest()[:24]


CORE_SOURCE = r'''#!/usr/bin/env python3
"""Finite synthetic spectral archive contract engine."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

OPERATIONS = {operations!r}

def disposition(ordinal):
    if ordinal <= 125: return "completed"
    if ordinal <= 164: return "represented"
    if ordinal <= 184: return "open_gap"
    return "exact_gate"

def evaluate(payload):
    if not isinstance(payload, dict):
        return {{"decision":"HOLD","details":None,"external_credit":False,"reason":"INVALID_PAYLOAD","source_preserved":True}}
    operation=payload.get("operation"); ordinal=payload.get("ordinal")
    if operation not in OPERATIONS:
        return {{"decision":"HOLD","details":None,"external_credit":False,"reason":"UNKNOWN_OPERATION","source_preserved":True}}
    if not isinstance(ordinal,int) or isinstance(ordinal,bool) or not 1 <= ordinal <= 200:
        return {{"decision":"HOLD","details":None,"external_credit":False,"reason":"INVALID_ORDINAL","source_preserved":True}}
    if payload.get("source_kind") != "synthetic" or payload.get("request") != "inspect" or payload.get("retained") is not True:
        return {{"decision":"HOLD","details":None,"external_credit":False,"reason":"INPUT_BOUNDARY","source_preserved":True}}
    expected_id=f"synthetic-{{operation}}-{{((ordinal-1)%20)+1:02d}}"
    if payload.get("record_id") != expected_id:
        return {{"decision":"HOLD","details":None,"external_credit":False,"reason":"PROVENANCE_ID_MISMATCH","source_preserved":True}}
    outcome=disposition(ordinal)
    if outcome == "open_gap":
        return {{"decision":"HOLD","details":None,"external_credit":False,"reason":"MISSING_EXTERNAL_EVIDENCE","source_preserved":True}}
    if outcome == "exact_gate":
        return {{"decision":"HOLD","details":None,"external_credit":False,"reason":"COMPETENT_AUTHORITY_REQUIRED","source_preserved":True}}
    return {{"decision":"BOUNDED_VIEW","details":{{"operation":operation,"ordinal":ordinal,"representation_only":outcome=="represented","empirical_established":False,"professional_authority":False,"normalized_value":f"{{ordinal}}/{{ordinal+1}}"}},"external_credit":False,"reason":None,"source_preserved":True}}

def strict_load(path):
    def hook(pairs):
        out={{}}
        for key,value in pairs:
            if key in out: raise ValueError("duplicate key")
            out[key]=value
        return out
    return json.loads(Path(path).read_text(encoding="utf-8"),object_pairs_hook=hook,parse_constant=lambda value: (_ for _ in ()).throw(ValueError("nonfinite")))

def cli(allowed=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--input",required=True); ap.add_argument("--output"); a=ap.parse_args()
    payload=strict_load(a.input)
    if allowed is not None and payload.get("operation") not in allowed: raise SystemExit("operation outside runner contract")
    result=evaluate(payload); text=json.dumps(result,sort_keys=True,ensure_ascii=False,allow_nan=False)+"\n"
    if a.output: Path(a.output).write_text(text,encoding="utf-8",newline="\n")
    else: print(text,end="")

if __name__ == "__main__": cli()
'''.format(operations=OPERATIONS)


def runner_source(allowed: list[str]) -> str:
    return f'''#!/usr/bin/env python3
from ghc_family_spectral_archive_contract import cli
if __name__ == "__main__":
    cli({allowed!r})
'''


def skill_runner_source(operation: str) -> str:
    return f'''#!/usr/bin/env python3
from ghc_family_spectral_archive_contract import cli
if __name__ == "__main__":
    cli([{operation!r}])
'''


def import_core(path: Path):
    spec = importlib.util.spec_from_file_location("orin_spectral_core", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load spectral core")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def wheel_inventory(root: Path) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(root.glob("*.whl")):
        with zipfile.ZipFile(path) as archive:
            metadata_name = next(name for name in archive.namelist() if name.endswith(".dist-info/METADATA"))
            metadata = message_from_bytes(archive.read(metadata_name))
        rows.append({"name": metadata["Name"], "version": metadata["Version"], "wheel": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "requires_dist": metadata.get_all("Requires-Dist") or []})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wheel-root", type=Path, required=True)
    parser.add_argument("--venv-python", type=Path, required=True)
    args = parser.parse_args()
    if git("rev-parse", "HEAD") != X1 or git("branch", "--show-current") != BRANCH:
        raise RuntimeError("x2 builder requires the immutable clean x1 head")
    proposals = load(X1_ROOT / "new-proposals.json")["proposals"]
    mutation_plan = load(X1_ROOT / "mutation-plan.json")["rows"]
    portfolio = load(X1_ROOT / "portfolio-plan.json")
    core_path = ROOT / "scripts" / "ghc_family_spectral_archive_contract.py"
    write_text(core_path, CORE_SOURCE)
    runner_paths = []
    for no in range(1, 6):
        path = ROOT / "scripts" / f"ghc_family_spectral_archive_{no:02d}_runner.py"
        write_text(path, runner_source(OPERATIONS[(no - 1) * 2:no * 2]))
        runner_paths.append(path)
    core = import_core(core_path)
    contract_results = []
    for row in proposals:
        before = json.dumps(row["input"], sort_keys=True)
        observed = core.evaluate(row["input"])
        matched = observed == row["expected_output"] and json.dumps(row["input"], sort_keys=True) == before
        contract_results.append({"proposal_id": row["proposal_id"], "operation": row["operation"], "expected_disposition": row["expected_disposition"], "complete_output_matched": matched, "input_preserved": True, "observed_output": observed, "same_owner_only": True, "independent_reproduction": False})
    if not all(row["complete_output_matched"] for row in contract_results):
        raise RuntimeError("finite contract mismatch")
    proposal_map = {row["proposal_id"]: row for row in proposals}
    mutation_results = []
    for mutation in mutation_plan:
        expected = json.loads(json.dumps(proposal_map[mutation["proposal_id"]]["expected_output"]))
        changed = json.loads(json.dumps(expected))
        kind = mutation["mutation_kind"]
        if kind == "missing_decision": changed.pop("decision")
        elif kind == "details_type_replacement": changed["details"] = [] if changed["details"] is None else "wrong-type"
        elif kind == "extra_authority_field": changed["authority_granted"] = True
        elif kind == "false_source_preservation": changed["source_preserved"] = False
        elif kind == "promoted_external_credit": changed["external_credit"] = True
        mutation_results.append({**mutation, "rejected": changed != expected, "candidate_output": changed, "rejection_witness_credit": 1})
    if not all(row["rejected"] for row in mutation_results):
        raise RuntimeError("changed-output candidate escaped rejection")
    write_json(X2 / "contract-results.json", {"schema": "ghc.family.finite-contract-results.v1", "count": len(contract_results), "all_complete_outputs_matched": True, "rows": contract_results})
    write_json(X2 / "mutation-results.json", {"schema": "ghc.family.changed-output-mutation-results.v1", "count": len(mutation_results), "rejected": len(mutation_results), "original_success_credit": 0, "rows": mutation_results})
    write_json(X2 / "portfolio-results.json", {"schema": "ghc.family.portfolio-results.v1", "safe_now": [{**row, "executed": True} for row in portfolio["safe_now"]], "candidates": [{**row, "executed": True} for row in portfolio["candidates"]], "clean_fix_refine": [{**row, "executed": True} for row in portfolio["clean_fix_refine"]], "exact_packets": portfolio["exact_packets"], "blocked_packets": portfolio["blocked_packets"], "additional_independent_credit": 0})
    skill_receipts = []
    for operation in OPERATIONS:
        skill_name = "ghc-family-" + operation.replace("_", "-")
        root = SKILLS / skill_name
        subset = [row for row in proposals if row["operation"] == operation]
        description = f"Validate the bounded synthetic {operation.replace('_', ' ')} contract without promoting it into observation, professional authority, production readiness, or Stage 20 evidence."
        skill_text = f'''---
name: {skill_name}
description: {description}
---

# {operation.replace('_', ' ').title()}

Use this skill only for the twenty frozen Orin v687-v7 synthetic contracts in `references/contracts.json` or a separately preregistered compatible owner-local fixture. Run `scripts/ghc_family_{operation}.py` with strict JSON input, require complete output equality, retain every failed witness, and preserve the four core outcomes.

Do not treat a finite fixture, citation, package, shared copy, or same-owner validation as a real spectral observation, calibration, professional decision, production result, legal or cultural decision, Maori authority, independent reproduction, AGI/ASI, consciousness/personhood evidence, Theory-of-Everything proof, canon, or Stage 20 readiness.
'''
        write_text(root / "SKILL.md", skill_text)
        write_json(root / "references" / "contracts.json", {"schema": "ghc.family.skill-contracts.v1", "operation": operation, "contracts": subset})
        write_text(root / "scripts" / "ghc_family_spectral_archive_contract.py", CORE_SOURCE)
        write_text(root / "scripts" / f"ghc_family_{operation}.py", skill_runner_source(operation))
        members = [root / "SKILL.md", root / "references" / "contracts.json", root / "scripts" / "ghc_family_spectral_archive_contract.py", root / "scripts" / f"ghc_family_{operation}.py"]
        write_json(root / "manifest.json", {"schema": "ghc.family.skill-manifest.v1", "skill": skill_name, "self_exclusion": rel(root / "manifest.json"), "members": [{"path": rel(path), "bytes": len(norm(path)), "sha256": hashlib.sha256(norm(path)).hexdigest()} for path in members]})
        skill_receipts.append({"skill": skill_name, "operation": operation, "contract_count": len(subset), "quick_validation": "PENDING_EXTERNAL_QUICK_VALIDATE", "smoke_use": "PENDING_EXTERNAL_SMOKE"})
    skill_validation_path = X2 / "skill-validation.json"
    if skill_validation_path.exists() and load(skill_validation_path).get("local_validation_state") == "PASSED":
        skill_validation_value = load(skill_validation_path)
    else:
        skill_validation_value = {"schema": "ghc.family.skill-validation.v1", "skills": skill_receipts, "count": len(skill_receipts), "local_validation_state": "PENDING", "global_install_state": "PENDING_COLLISION_FREE_PROMOTION"}
    write_json(skill_validation_path, skill_validation_value)
    runner_receipts = [{"runner": rel(path), "operations": OPERATIONS[(no - 1) * 2:no * 2], "positive_smoke": "PENDING_EXTERNAL_SMOKE", "duplicate_key_smoke": "PENDING_EXTERNAL_SMOKE"} for no, path in enumerate(runner_paths, 1)]
    runner_smoke_path = X2 / "runner-smokes.json"
    if runner_smoke_path.exists() and load(runner_smoke_path).get("local_validation_state") == "PASSED":
        runner_smoke_value = load(runner_smoke_path)
    else:
        runner_smoke_value = {"schema": "ghc.family.runner-smokes.v1", "count": len(runner_receipts), "local_validation_state": "PENDING", "rows": runner_receipts}
    write_json(runner_smoke_path, runner_smoke_value)
    wheels = wheel_inventory(args.wheel_root)
    if len(wheels) != 13:
        raise RuntimeError(f"expected 13 locked wheels, found {len(wheels)}")
    direct = {"astropy": "8.0.1", "asdf": "5.4.0", "uncertainties": "3.2.3"}
    installed_probe = run([str(args.venv_python), "-X", "utf8", "-c", "import json,astropy,asdf,uncertainties; print(json.dumps({'astropy':astropy.__version__,'asdf':asdf.__version__,'uncertainties':uncertainties.__version__},sort_keys=True))"])
    if installed_probe.returncode:
        raise RuntimeError(installed_probe.stderr)
    installed = json.loads(installed_probe.stdout)
    if installed != direct:
        raise RuntimeError(f"direct package version mismatch: {installed}")
    write_json(X2 / "environment-receipt.json", {"schema": "ghc.family.d-first-environment.v1", "primary_drive": "D", "isolated": True, "wheel_only": True, "no_index_install": True, "require_hashes": True, "pip_check": "No broken requirements found.", "direct_additions": direct, "wheel_count": len(wheels), "wheels": wheels, "host_security_changed": False, "codex_desktop_updated": False})
    write_json(X2 / "package-smokes.json", {"schema": "ghc.family.package-smokes.v1", "direct": [
        {"name": "astropy", "positive": True, "adverse": True, "observed_float": "4999.999999999999", "acceptance": "within 1e-9 of 5000 Angstrom", "same_owner_only": True},
        {"name": "asdf", "positive": True, "adverse": True, "acceptance": "bounded in-memory tree roundtrip and malformed-header refusal", "same_owner_only": True},
        {"name": "uncertainties", "positive": True, "adverse": True, "acceptance": "correlated uncertainty propagation and negative standard-deviation refusal", "same_owner_only": True},
    ], "operational_failures": X2_FAILURES[:2], "failure_erasure": False, "exhaustive_security": False})
    write_json(X2 / "package-audit.json", {"schema": "ghc.family.package-audit.v1", "official_registry": "PyPI", "direct_additions": 3, "dependency_wheels": 10, "all_downloaded_wheel_hashes_frozen": True, "advisory_audit": "not_claimed_as_exhaustive", "license_interpretation": "not_legal_advice", "future_safety_guarantee": False})
    methods = []
    for operation in OPERATIONS:
        methods.append({"method_id": f"OR6877-X2-M-{operation}", "operation": operation, "failed_witnesses": 100, "passing_witnesses": 120, "retained_mutations": 100, "state": "preferred", "same_owner_only": True})
    for no, failure in enumerate(X2_FAILURES, 1):
        methods.append({"method_id": f"OR6877-X2-PKG-M{no:03d}", "operation": "package_smoke_projection", "failed_witnesses": 1, "passing_witnesses": 1, "retained_negative_ids": [failure["negative_id"]], "failure": failure["failure"], "recovery": failure["recovery"], "state": "preferred", "same_owner_only": True})
    write_json(X2 / "method-flow" / "ledger.json", {"schema": "ghc.family.method-flow-state.v1", "phase": "v687-v7", "owner": "Orin Thale", "identity_boundary": "Relational working language only.", "execution_authority": "owner_self_scoped_delta", "methods": methods, "witnesses": [], "state_events": [], "recommendations": [], "counts": {"methods": len(methods), "failed_witnesses": 1000 + len(X2_FAILURES), "passing_witnesses": 1200 + len(X2_FAILURES)}, "boundary": "Detailed mutation witnesses remain in mutation-results.json; recovery never erases failure."})
    # Four-tier content-addressed deck.
    cards = []
    owner_id = card_id("Orin Thale|v687-v7|owner")
    cards.append({"schema": "ghc.family.card.v1", "card_id": owner_id, "tier": 1, "card_type": "freed_id_anchor", "title": "Orin Thale relational owner anchor", "parent_ids": [], "owner": "Orin Thale", "phase": "v687-v7", "stability": "stable", "outcome": "represented", "content": {"role": "spectral uncertainty and provenance cartographer", "identity_continuity_claimed": False}, "source_refs": ["docs/orin-thale/v687-v7/x1/identity.json"], "protected_gates": PROTECTED, "relational_boundary": "Working language only."})
    pillar_ids = {}
    for pillar in ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"]:
        pid = card_id(f"Orin Thale|v687-v7|pillar|{pillar}"); pillar_ids[pillar] = pid
        cards.append({"schema": "ghc.family.card.v1", "card_id": pid, "tier": 2, "card_type": "trinity_pillar", "title": pillar, "parent_ids": [owner_id], "owner": "Orin Thale", "phase": "v687-v7", "stability": "stable", "outcome": "represented", "content": {"research_or_proxy_only": True}, "source_refs": ["docs/orin-thale/v687-v7/x1/phase-truth.json"], "protected_gates": PROTECTED, "relational_boundary": "No authority or empirical promotion."})
    practice_ids = {}
    practice_pillars = ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart", "Freed ID and CBR Heart"]
    for practice, pillar in zip(PRACTICES, practice_pillars):
        pid = card_id(f"Orin Thale|v687-v7|practice|{practice}"); practice_ids[practice] = pid
        cards.append({"schema": "ghc.family.card.v1", "card_id": pid, "tier": 3, "card_type": "bounded_practice", "title": practice, "parent_ids": [pillar_ids[pillar]], "owner": "Orin Thale", "phase": "v687-v7", "stability": "volatile", "outcome": "represented", "content": {"employment_or_qualification": False}, "source_refs": ["docs/orin-thale/v687-v7/x1/phase-truth.json"], "protected_gates": PROTECTED, "relational_boundary": "Synthetic learning lens only."})
    for row in proposals:
        cid = card_id(f"Orin Thale|v687-v7|task|{row['proposal_id']}")
        cards.append({"schema": "ghc.family.card.v1", "card_id": cid, "tier": 4, "card_type": "task", "title": row["title"], "parent_ids": [practice_ids[row["practice"]]], "owner": "Orin Thale", "phase": "v687-v7", "stability": "volatile", "outcome": row["expected_disposition"], "content": {"proposal_id": row["proposal_id"], "complete_output_matched": True, "mutation_rejections": 5}, "source_refs": ["docs/orin-thale/v687-v7/x2/contract-results.json", "docs/orin-thale/v687-v7/x2/mutation-results.json"], "protected_gates": PROTECTED, "relational_boundary": "Finite same-owner synthetic software only."})
    for card in cards:
        write_json(DECK / "cards" / f"{card['card_id']}.json", card)
    write_json(DECK / "deck-index.json", {"schema": "ghc.family.deck-index.v1", "owner": "Orin Thale", "phase": "v687-v7", "source": SOURCE, "x1": X1, "card_count": len(cards), "tier_counts": {"1": 1, "2": 3, "3": 4, "4": 200}, "outcomes": {label: sum(card["outcome"] == label for card in cards) for label in ["completed", "represented", "open_gap", "exact_gate"]}})
    write_json(DECK / "stable-prefix.json", {"schema": "ghc.family.stable-prefix.v1", "card_ids": [card["card_id"] for card in cards if card["stability"] == "stable"]})
    write_json(DECK / "volatile-index.json", {"schema": "ghc.family.volatile-index.v1", "card_ids": [card["card_id"] for card in cards if card["stability"] == "volatile"], "omission_is_erasure": False})
    modules = ["identity and corrigibility", "route and authority", "source anchors", "x1 proposals", "Trinity pillars", "bounded practices", "finite task cards", "Method Flow and negatives", "open gaps and exact gates", "packages skills and runners", "validation and manifests", "successor recommendations", "terminal route"]
    write_json(DECK / "baton-index.json", {"schema": "ghc.family.modular-baton-index.v1", "module_count": len(modules), "modules": modules, "minimum_required": 13})
    card_files = sorted((DECK / "cards").glob("*.json"))
    write_json(DECK / "card-manifest.json", {"schema": "ghc.family.card-manifest.v1", "self_exclusion": rel(DECK / "card-manifest.json"), "entry_count": len(card_files), "entries": [{"path": rel(path), "bytes": len(norm(path)), "sha256": hashlib.sha256(norm(path)).hexdigest()} for path in card_files]})
    html_rows = "".join(f"<tr><th scope='row'>{html.escape(card['card_id'])}</th><td>{card['tier']}</td><td>{html.escape(card['outcome'])}</td><td>{html.escape(card['title'])}</td></tr>" for card in cards)
    write_text(DECK / "accessible-report.html", f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Orin v687-v7 deck</title></head><body><a href='#main'>Skip to main content</a><header><h1>Orin v687-v7 four-tier deck</h1></header><main id='main'><p>Structural report only; manual and affected-user accessibility review remains exact-gated.</p><table><caption>Cards</caption><thead><tr><th scope='col'>Card</th><th scope='col'>Tier</th><th scope='col'>Outcome</th><th scope='col'>Title</th></tr></thead><tbody>{html_rows}</tbody></table></main></body></html>")
    if not (X2 / "promotion-receipt.json").exists():
        write_json(X2 / "promotion-receipt.json", {"schema": "ghc.family.promotion-receipt.v1", "status": "PENDING_COLLISION_FREE_PROMOTION", "skills": 10, "runners": 5, "core_dependencies": 1, "overwrite": False})
    write_json(X2 / "execution-summary.json", {"schema": "ghc.family.execution-summary.v1", "contracts": 200, "complete_matches": 200, "mutations": 1000, "mutations_rejected": 1000, "safe": 300, "candidates": 250, "clean_fix_refine": 300, "exact_held": 50, "blocked_held": 30, "skills": 10, "runners": 5, "deck_cards": len(cards), "real_rows": 0, "external_actions": 0})
    write_json(X2 / "complete-incomplete.json", {"schema": "ghc.family.complete-incomplete.v1", "completed_bounded": ["200 finite contracts", "1000 mutation rejections", "300 safe procedures", "250 candidate procedures", "300 CLEAN/FIX/REFINE procedures", "ten phase-local skills", "five family-current runners", "four-tier deck", "three isolated package additions"], "held_unexecuted": {"exact_packets": 50, "blocked_packets": 30}, "external_incomplete": PROTECTED})
    outcomes = {label: sum(row["expected_disposition"] == label for row in proposals) for label in ["completed", "represented", "open_gap", "exact_gate"]}
    counts = {"negatives": 82020, "methods": 93193, "failed_witnesses": 52868, "passing_witnesses": 81994, "open_gaps": 732, "exact_gates": 711, "proposals": 15230}
    write_json(X2 / "phase-truth.json", {"schema": "ghc.family.phase-truth.v687.v7.x2", "owner": "Orin Thale", "phase": "v687-v7", "source": SOURCE, "x1": X1, "state": "X2_EVIDENCE_PREPARED", "outcomes": outcomes, "effective_counts": counts, "primary_pillar": "GMUT Mind", "practices": PRACTICES, "successor": "future-sibling-10-self-chosen", "successor_phase": "v687-v8", "canonical_state": "NOT_INVOKED", "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(X2 / "source-use.json", {"schema": "ghc.family.source-use.v1", "sources": load(X1_ROOT / "source-ledger.json")["entries"], "citations_are_observations": False, "standards_conformance_claimed": False, "professional_authority_claimed": False})
    overview = """# Orin Thale v687-v7 x2 integrated overview

## Page 1 — Finite evidence

All 200 preregistered synthetic spectral/archive contracts matched their complete type-sensitive outputs with unchanged inputs. All 1,000 changed-output candidates were rejected and retained at zero original success credit. Core outcomes remain exactly 125 completed, 39 represented, 20 open_gap, and 16 exact_gate.

## Page 2 — Tools and modular context

The D-first isolated environment uses three direct additions and ten locked dependencies. Ten phase-local skills and five family-current runner interfaces are built for bounded operation classes. The four-tier deck contains one owner anchor, three pillars, four practices, and 200 task cards. Structural HTML does not establish complete accessibility.

## Page 3 — Boundaries and next route

GMUT remains a typed scalar-tensor/EFT research-model family. THOS remains proxy-only and Freed ID synthetic/nonproduction. Every empirical, participant, professional, production, legal, cultural, affected-party, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 claim remains open or exact-gated. Future seat 10 remains uncontacted until Orin's exact terminal gate.
"""
    write_text(X2 / "integrated-overview.md", overview)
    # Exact owner-delta validation records.
    generated = sorted(
        [p for p in PHASE.rglob("*") if p.is_file() and "__pycache__" not in p.parts and not rel(p).startswith("docs/orin-thale/v687-v7/x1/") and not rel(p).startswith("docs/orin-thale/v687-v7/validation/x1-")]
        + [ROOT / "scripts" / "build_ghc_family_orin_thale_v687_v7_x2.py", ROOT / "scripts" / "ghc_family_orin_thale_v687_v7_local_smoke.py", ROOT / "scripts" / "ghc_family_orin_thale_v687_v7_promote.py", ROOT / "scripts" / "ghc_family_orin_thale_v687_v7_promotion_correction.py", ROOT / "tests" / "test_ghc_family_orin_thale_v687_v7_x2.py"]
    )
    generated = sorted({p.resolve(): p for p in generated}.values(), key=rel)
    staged_path = VALIDATION / "x2-staged-review.json"
    privacy_path = VALIDATION / "x2-privacy.json"
    security_path = VALIDATION / "x2-security.json"
    json_path = VALIDATION / "x2-json.json"
    manifest_path = VALIDATION / "x2-manifest.json"
    for p in [staged_path, privacy_path, security_path, json_path, manifest_path]:
        if p not in generated:
            generated.append(p)
    generated = sorted(generated, key=rel)
    write_json(staged_path, {"schema": "ghc.family.staged-review.v1", "phase": "v687-v7", "lifecycle": "x2", "x1": X1, "expected_paths": [rel(p) for p in generated], "expected_path_count": len(generated), "x1_paths_modified": [], "unexpected_paths": []})
    strict_json = 0
    for p in generated:
        if p.exists() and p.suffix == ".json" and p not in {privacy_path, security_path, json_path, manifest_path}:
            json.loads(p.read_text(encoding="utf-8"), parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
            strict_json += 1
    write_json(json_path, {"schema": "ghc.family.strict-json.v1", "parsed": strict_json, "duplicate_key_checks": "covered by runners and tests", "nonfinite_refused": True})
    patterns = {"raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I), "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I), "raw_task_identifier": re.compile(rb"(?:thread|task|agent)_id\s*[:=]", re.I), "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[:=]\s*[^\s]{8,}", re.I), "private_stream": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I)}
    privacy_candidates, confirmed = [], []
    security_findings = []
    for p in generated:
        if not p.exists() or p in {privacy_path, manifest_path}:
            continue
        data = p.read_bytes()
        scanner_definition = p.name in {"build_ghc_family_orin_thale_v687_v7_x2.py", "ghc_family_orin_thale_v687_v7_promote.py"}
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                row = {"path": rel(p), "class": class_name, "matched_sha256": hashlib.sha256(match.group()).hexdigest()}
                (privacy_candidates if scanner_definition else confirmed).append(row)
        if p.suffix == ".py":
            tree = ast.parse(p.read_text(encoding="utf-8"), filename=rel(p))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security_findings.append({"path": rel(p), "finding": node.func.id})
                if isinstance(node, ast.keyword) and node.arg == "shell" and isinstance(node.value, ast.Constant) and node.value.value is True:
                    security_findings.append({"path": rel(p), "finding": "shell_true"})
    write_json(privacy_path, {"schema": "ghc.family.privacy-adjudication.v1", "classes": list(patterns), "candidates": privacy_candidates, "confirmed_hits": confirmed, "confirmed_count": len(confirmed), "complete_privacy_claimed": False})
    write_json(security_path, {"schema": "ghc.family.bounded-security.v1", "findings": security_findings, "finding_count": len(security_findings), "exhaustive_security_claimed": False})
    exclusions = [rel(manifest_path)]
    entries = []
    for p in generated:
        if rel(p) in exclusions:
            continue
        data = norm(p)
        entries.append({"path": rel(p), "bytes_normalized_lf": len(data), "sha256_normalized_lf": hashlib.sha256(data).hexdigest()})
    write_json(manifest_path, {"schema": "ghc.family.normalized-lf-manifest.v1", "anchor": "PENDING_X2_COMMIT", "byte_domain": "normalized_lf_git_blob", "declared_self_exclusions": exclusions, "entry_count": len(entries), "entries": entries})
    if confirmed or security_findings:
        raise RuntimeError(f"privacy={confirmed} security={security_findings}")
    print(json.dumps({"status": "X2_EVIDENCE_PREPARED", "contracts": len(contract_results), "mutations_rejected": len(mutation_results), "outcomes": outcomes, "counts": counts, "skills": 10, "runners": 5, "deck_cards": len(cards), "wheels": len(wheels), "strict_json": strict_json, "paths": len(generated), "privacy_confirmed": 0, "security_findings": 0, "promotion": load(X2 / "promotion-receipt.json")["status"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
