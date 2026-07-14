#!/usr/bin/env python3
"""Build bounded Sable Rook v644-v1 evidence from the frozen x1 model."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Callable


PHASE = "v644-gmut-thos-v1-x1-x2"
OWNER = "Sable Rook"
SOURCE_COMMIT = "96ca5acffa5e0eb9c5ee95a42f94f38602bb6be5"
SOURCE_SEAL = "e4fc8480ccaccf5816cf9ef744f454fcb6c927cc"
X1_COMMIT = "248af65fb976f1bb356cdaa3d12894320d91fd6c"
TRUTH_LABELS = ("completed", "represented", "open_gap", "exact_gate")
PHASE_REL = "docs/sable-rook/v644-v1"

BOUNDARY = (
    "Bounded repository engineering evidence only. GMUT remains a typed scalar-tensor/EFT research-model "
    "family, not an established force, unique prediction, likelihood result, empirical confirmation, proof, "
    "final physics, or Theory of Everything. THOS remains proxy without preregistered blind matched-budget "
    "real arms, real participants and raters, and independent review. No production Freed ID, CBR legitimacy, "
    "affected-party acceptance, Māori wording or authority, Māori data governance, cultural ratification, "
    "legal interpretation, enacted-law status, deployment, exhaustive security, complete accessibility, "
    "independent-team reproduction, AGI/ASI, consciousness, sentience, personhood, proof/canon, sibling merge, "
    "or Stage 20 readiness is established."
)


def _load_model(repo: Path):
    path = repo / "scripts/ghc_family_v644_v1_model.py"
    spec = importlib.util.spec_from_file_location("ghc_family_v644_v1_model_runtime", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def normalize_data(data: bytes) -> bytes:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def normalized_bytes(path: Path) -> bytes:
    return normalize_data(path.read_bytes())


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def decision(reasons: list[str], details: dict[str, Any] | None = None) -> tuple[bool, list[str], dict[str, Any]]:
    return not reasons, reasons, details or {}


def rule_decision(proposal_id: str, row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    rules = RULES[proposal_id]
    reasons: list[str] = []
    for field in rules["required"]:
        if row.get(field) is not True:
            reasons.append(f"{field}_required")
    for field, expected in rules["exact"].items():
        if row.get(field) != expected:
            reasons.append(f"{field}_expected_{expected}")
    for field in rules["forbidden"]:
        if row.get(field) is not False:
            reasons.append(f"{field}_forbidden")
    return decision(reasons, copy.deepcopy(DETAILS[proposal_id]))


_ROOT = Path(__file__).resolve().parents[1]
_MODEL = _load_model(_ROOT)
OBSERVED = _MODEL.OBSERVED
RULES = _MODEL.RULES
DETAILS = _MODEL.DETAILS
MUTATIONS = _MODEL.MUTATIONS
DECISIONS: dict[str, Callable[[dict[str, Any]], tuple[bool, list[str], dict[str, Any]]]] = {
    proposal_id: (lambda row, pid=proposal_id: rule_decision(pid, row)) for proposal_id in RULES
}


def canonical_inputs() -> dict[str, dict[str, Any]]:
    canonical: dict[str, dict[str, Any]] = {}
    for proposal_id, rules in RULES.items():
        row: dict[str, Any] = {field: True for field in rules["required"]}
        row.update(copy.deepcopy(rules["exact"]))
        row.update({field: False for field in rules["forbidden"]})
        canonical[proposal_id] = row
    return canonical


def fixture_catalog() -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for proposal_id, canonical in canonical_inputs().items():
        rows = [{"case_id": f"{proposal_id}-C00", "name": "bounded-canonical", "expect_accept": True, "input": canonical}]
        for index, (name, patch) in enumerate(MUTATIONS[proposal_id], 1):
            row = copy.deepcopy(canonical)
            row.update(copy.deepcopy(patch))
            rows.append({"case_id": f"{proposal_id}-C{index:02d}", "name": name, "expect_accept": False, "input": row})
        groups[proposal_id] = rows
    return groups


def evaluate_catalog() -> dict[str, list[dict[str, Any]]]:
    evaluated: dict[str, list[dict[str, Any]]] = {}
    for proposal_id, rows in fixture_catalog().items():
        evaluated[proposal_id] = []
        for row in rows:
            accepted, reasons, details = DECISIONS[proposal_id](row["input"])
            evaluated[proposal_id].append({
                "case_id": row["case_id"], "name": row["name"], "expect_accept": row["expect_accept"],
                "accepted": accepted, "matched_expectation": accepted == row["expect_accept"],
                "reasons": reasons, "details": details,
            })
    return evaluated


# Add only actual v644-v1 x2 operational failures. Rejected preregistered
# mutations are assembled separately and never hidden by later success.
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6441-X2-N01",
        "origin": "v644-v1-x2-operational",
        "observed": (
            "A combined parallel inspection wrapper exceeded its bounded command timeout before returning the "
            "requested status, search, and source excerpts."
        ),
        "recovery": (
            "Retain the timeout, split status and semantic searches into bounded commands, and inspect the "
            "required source ranges directly."
        ),
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6441-X2-N02",
        "origin": "v644-v1-x2-operational",
        "observed": (
            "The first v644-v1 unit run passed 24 of 25 tests but one Freed ID test mutated an obsolete "
            "production_cryptography_claim field, so the bounded rule correctly did not reject that unrelated key."
        ),
        "recovery": (
            "Retain the failed run, align the test with the frozen production_issuance_claim prohibition, and "
            "rerun the unchanged rule model and complete phase suite."
        ),
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6441-X2-N03",
        "origin": "v644-v1-x2-operational",
        "observed": (
            "The unadapted x2 complete repository suite passed 524 of 525 tests and reproduced the inherited "
            "CRLF-sensitive legacy constraint-hash alias failure."
        ),
        "recovery": (
            "Retain the 524-of-525 run, invoke the inherited semantic-hash-verified materializer through a new "
            "byte-restoring family wrapper, rerun all 525 tests, and require exact raw-byte restoration."
        ),
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6441-X2-N04",
        "origin": "v644-v1-x2-operational",
        "observed": (
            "The first byte-restoring complete-suite wrapper run restored both inherited files exactly but "
            "failed four of 525 tests because the generated negative register and manifest predated the newly "
            "retained N03 record and wrapper source."
        ),
        "recovery": (
            "Retain the stale-packet run, regenerate evidence and the normalized manifest after all current "
            "negative and tooling changes, then rerun the same byte-restoring wrapper without relaxing checks."
        ),
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
]


def git_blob(repo: Path, commit: str, relative: str) -> bytes:
    result = subprocess.run(["git", "show", f"{commit}:{relative}"], cwd=repo, check=True, stdout=subprocess.PIPE)
    return result.stdout


def x1_content_seal(repo: Path, phase: Path) -> dict[str, Any]:
    exact = json.loads(git_blob(repo, X1_COMMIT, f"{PHASE_REL}/validation/x1-exact-file-set.json").decode("utf-8"))
    rows = []
    for relative in exact["files"]:
        frozen = normalize_data(git_blob(repo, X1_COMMIT, relative))
        current = normalized_bytes(repo / relative)
        rows.append({
            "repo_path": relative,
            "x1_sha256_lf_normalized": hashlib.sha256(frozen).hexdigest(),
            "current_sha256_lf_normalized": hashlib.sha256(current).hexdigest(),
            "unchanged": frozen == current,
        })
    return {
        "schema": "ghc.family.v644-v1.x1-content-seal.v1", "phase": PHASE, "owner": OWNER,
        "x1_commit": X1_COMMIT, "entry_count": len(rows), "entries": rows,
        "all_unchanged": all(row["unchanged"] for row in rows),
        "boundary": "This seal proves frozen x1 bytes remained unchanged; it does not turn expected dispositions into evidence.",
    }


def open_and_exact_gates() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    open_gaps = [
        {"gate_id": "OPEN-01", "domain": "GMUT multi-messenger propagation likelihood", "state": "open", "requires": ["model-specific propagation observable derivation", "licensed gravitational-wave and counterpart rows", "calibration and selection functions", "frozen waveform and nuisance plan", "blind GR baseline", "identifiability analysis", "independent review"]},
        {"gate_id": "OPEN-02", "domain": "THOS real-arm evidence", "state": "open", "requires": ["ethics", "consent", "preregistered blind matched-budget arms", "real participants and raters", "harms monitoring", "independent review"]},
        {"gate_id": "OPEN-03", "domain": "Freed ID production completion", "state": "open", "requires": ["standards-conformant real keys and proofs", "live issuance", "live resolution", "status and revocation", "cross-vendor interoperability", "privacy and security review", "trust governance"]},
        {"gate_id": "OPEN-04", "domain": "qualified accessibility evaluation", "state": "open", "requires": ["manual evaluation", "assistive-technology coverage", "fluent-speaker review", "affected-user evaluation"]},
        {"gate_id": "OPEN-05", "domain": "independent-team scientific reproduction", "state": "open", "requires": ["independent team", "independently owned protocol", "independent infrastructure", "returned evidence"]},
    ]
    exact_gates = [
        {"gate_id": "EXACT-01", "domain": "affected-party data return and stewardship acceptance", "state": "pending_exact_authority"},
        {"gate_id": "EXACT-02", "domain": "Māori wording, authority, and data governance", "state": "pending_exact_authority"},
        {"gate_id": "EXACT-03", "domain": "cultural ratification, repatriation, and stewardship transfer", "state": "pending_exact_authority"},
        {"gate_id": "EXACT-04", "domain": "legal interpretation and enacted-law status", "state": "pending_exact_authority"},
        {"gate_id": "EXACT-05", "domain": "destructive, account, credential, API-key, or sibling-merge action", "state": "pending_exact_authority"},
        {"gate_id": "EXACT-06", "domain": "Stage 20 external decision authority", "state": "pending_exact_authority"},
    ]
    return open_gaps, exact_gates


def overview_text(distribution: dict[str, int], negative_count: int) -> str:
    from ghc_family_v644_v1_overview import render_overview

    return render_overview(distribution, negative_count, SOURCE_COMMIT, SOURCE_SEAL, X1_COMMIT)

def manifest_candidates(repo: Path, phase: Path) -> list[str]:
    paths: set[str] = set()
    for path in phase.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(repo).as_posix()
        if "/validation/" in relative or relative.endswith("/reproduction/manifest.json"):
            continue
        paths.add(relative)
    paths.update({
        "scripts/ghc_family_v644_v1_model.py",
        "scripts/ghc_family_v644_v1_overview.py",
        "scripts/ghc_family_v644_v1_evidence.py",
        "scripts/ghc_family_v644_v1_validator.py",
        "scripts/ghc_family_v644_v1_minimal.py",
        "scripts/ghc_family_v644_v1_complete_suite.py",
        "scripts/ghc_family_v644_v1_staged_review.py",
        "scripts/build_ghc_family_v644_v1_report.py",
        "tests/test_ghc_family_v644_v1.py",
    })
    return sorted(relative for relative in paths if (repo / relative).is_file())


def build(repo: Path, snapshot_state: str = "pending", lifecycle: str = "evidence") -> dict[str, Any]:
    repo = repo.resolve()
    phase = repo / PHASE_REL
    proposals_packet = json.loads((phase / "x1-proposals.json").read_text(encoding="utf-8"))
    proposals = proposals_packet["proposals"]
    evaluated = evaluate_catalog()
    if not all(row["matched_expectation"] for rows in evaluated.values() for row in rows):
        raise ValueError("fixture expectation mismatch")
    distribution = dict(Counter(OBSERVED.values()))
    if distribution != {"completed": 6, "represented": 2, "exact_gate": 1, "open_gap": 1}:
        raise ValueError(f"unexpected distribution: {distribution}")

    ledger_rows = []
    for proposal in proposals:
        pid = proposal["proposal_id"]
        cases = evaluated[pid]
        outcome = OBSERVED[pid]
        ledger_rows.append({
            "proposal_id": pid, "title": proposal["title"], "outcome": outcome,
            "truth_label": outcome, "canonical_case_accepted": cases[0]["accepted"],
            "mutation_count": len(cases) - 1, "rejected_mutation_count": sum(not row["accepted"] for row in cases[1:]),
            "deliverables": proposal["deliverables"], "protected_gates": proposal["protected_gates"],
            "external_claims_established": [], "boundary": BOUNDARY,
        })
        canonical = canonical_inputs()[pid]
        accepted, reasons, details = DECISIONS[pid](canonical)
        contract_path, vector_path, boundary_path = (phase / relative for relative in proposal["deliverables"])
        write_json(contract_path, {
            "schema": "ghc.family.v644-v1.proposal-contract.v1", "phase": PHASE, "owner": OWNER,
            "proposal_id": pid, "title": proposal["title"], "outcome": outcome,
            "canonical_input": canonical, "accepted": accepted, "reasons": reasons, "details": details,
            "required_fields": RULES[pid]["required"], "exact_fields": RULES[pid]["exact"],
            "forbidden_promotions": RULES[pid]["forbidden"], "external_claims_established": [], "boundary": BOUNDARY,
        })
        write_json(vector_path, {
            "schema": "ghc.family.v644-v1.mutation-vectors.v1", "phase": PHASE, "owner": OWNER,
            "proposal_id": pid, "case_count": len(cases), "accepted_count": sum(row["accepted"] for row in cases),
            "rejected_count": sum(not row["accepted"] for row in cases), "all_matched_expectation": all(row["matched_expectation"] for row in cases),
            "cases": cases, "retention_rule": "Every rejected case is copied into the retained-negative register.", "boundary": BOUNDARY,
        })
        write_json(boundary_path, {
            "schema": "ghc.family.v644-v1.nonpromotion-boundary.v1", "phase": PHASE, "owner": OWNER,
            "proposal_id": pid, "outcome": outcome, "protected_gates": proposal["protected_gates"],
            "rollback_or_recovery": proposal["rollback_or_recovery"], "external_claims_established": [],
            "real_data_rows": 0, "real_participants": 0, "real_arms": 0, "real_keys_or_proofs": 0,
            "authority_substitution_permitted": False, "boundary": BOUNDARY,
        })

    write_json(phase / "x2-proposal-ledger.json", {
        "schema": "ghc.family.v644-v1.x2-proposal-ledger.v1", "phase": PHASE, "owner": OWNER,
        "x1_commit": X1_COMMIT, "proposal_count": 10, "distribution": distribution,
        "case_count": 80, "rejected_mutation_count": 70, "proposals": ledger_rows,
        "outcome_classes": list(TRUTH_LABELS), "boundary": BOUNDARY,
    })
    write_json(phase / "evidence/evidence-ledger.json", {
        "schema": "ghc.family.v644-v1.evidence-ledger.v1", "phase": PHASE, "owner": OWNER,
        "evidence_class": "bounded deterministic repository fixtures", "rows": ledger_rows,
        "proposal_count": 10, "case_count": 80, "accepted_canonical_count": 10,
        "retained_rejection_count": 70, "distribution": distribution, "external_claims_established": [], "boundary": BOUNDARY,
    })

    inherited_path = repo / "docs/ilyra-fen/v643-v8/retained-negative-register.json"
    inherited = json.loads(inherited_path.read_text(encoding="utf-8"))
    negatives = copy.deepcopy(inherited["negatives"])
    x1_audit = json.loads((phase / "validation/x1-operational-negatives.json").read_text(encoding="utf-8"))
    x1_negatives = [{
        "negative_id": item["negative_id"], "origin": "v644-v1-x1-operational",
        "observed": item["observed_failure"], "recovery": item["recovery"], "retained": True,
        "resolved_for_current_local_scope": True, "external_gate_closed": False,
    } for item in x1_audit["negatives"]]
    negatives.extend(x1_negatives)
    synthetic_index = 0
    for pid, rows in evaluated.items():
        for row in rows:
            if row["accepted"]:
                continue
            synthetic_index += 1
            negatives.append({
                "negative_id": f"V6441-SYN-N{synthetic_index:03d}", "origin": "v644-v1-preregistered-synthetic",
                "proposal_id": pid, "case_id": row["case_id"], "observed": row["reasons"],
                "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False,
            })
    negatives.extend(copy.deepcopy(X2_OPERATIONAL_NEGATIVES))
    write_json(phase / "retained-negative-register.json", {
        "schema": "ghc.family.v644-v1.retained-negative-register.v1", "phase": PHASE, "owner": OWNER,
        "inherited_from": "docs/ilyra-fen/v643-v8/retained-negative-register.json",
        "inherited_sha256_lf_normalized": normalized_sha256(inherited_path), "inherited_count": len(inherited["negatives"]),
        "x1_operational_count": len(x1_negatives), "new_synthetic_count": synthetic_index,
        "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES), "new_count": len(x1_negatives) + synthetic_index + len(X2_OPERATIONAL_NEGATIVES),
        "negative_count": len(negatives), "all_retained": True, "erasure_permitted": False,
        "negatives": negatives, "boundary": BOUNDARY,
    })
    write_json(phase / "validation/execution-negative-log.json", {
        "schema": "ghc.family.v644-v1.execution-negative-log.v1", "phase": PHASE, "owner": OWNER,
        "negative_count": len(X2_OPERATIONAL_NEGATIVES),
        "negatives": copy.deepcopy(X2_OPERATIONAL_NEGATIVES),
        "all_retained": True,
        "boundary": "Operational failures are retained as execution evidence and do not close any external gate.",
    })

    open_gaps, exact_gates = open_and_exact_gates()
    write_json(phase / "exact-open-gate-register.json", {
        "schema": "ghc.family.v644-v1.exact-open-gate-register.v1", "phase": PHASE, "owner": OWNER,
        "open_gap_count": len(open_gaps), "exact_gate_count": len(exact_gates), "open_gaps": open_gaps, "exact_gates": exact_gates,
        "all_visible": True, "none_silently_closed": True, "boundary": BOUNDARY,
    })

    threats = [
        {"id": "T01", "threat": "shared authorship, dataset, code, or protocol lineage is counted as independent corroboration", "control": "collapse version relations and shared lineage before any independence count"},
        {"id": "T02", "threat": "GMUT source sectors overlap or exchange and improvement terms are hidden", "control": "typed sector split, explicit exchange currents, total-balance check, and improvement declaration"},
        {"id": "T03", "threat": "synthetic propagation rows are substituted for licensed gravitational-wave and electromagnetic-counterpart evidence", "control": "open real-row gate with calibration, selection, waveform, nuisance, blind-baseline, and identifiability requirements"},
        {"id": "T04", "threat": "THOS follow-up windows, decay model, durability threshold, or intercurrent-event handling drift after observation", "control": "frozen time origin, windows, schedule, estimand, decay model, attrition, and zero-real-arm proxy boundary"},
        {"id": "T05", "threat": "an authorization code, nonce, or wallet session is rebound across issuance transactions", "control": "single-use code and nonce plus issuer, offer, authorization, PKCE, wallet, and deferred-session binding"},
        {"id": "T06", "threat": "synthetic proof fields are called production cryptography", "control": "zero real keys and proofs plus resolution, interoperability, review, and governance gates"},
        {"id": "T07", "threat": "repository output decides rightful stewardship, return, deletion, repatriation, or cultural and legal ratification", "control": "neutral questions and exact affected-party, Māori, custodian, cultural, and legal authority gates"},
        {"id": "T08", "threat": "Git clean or smudge filters, hooks, textconv, or external diff execute during an inspection", "control": "inventory attribute and configuration sources with execution disabled and no host mutation"},
        {"id": "T09", "threat": "document language, language-of-parts inheritance, or directionality metadata mislabels content", "control": "bounded static language and direction checks with narrow exceptions"},
        {"id": "T10", "threat": "automated structure is called complete accessibility", "control": "manual, assistive-technology, and affected-user reservations"},
        {"id": "T11", "threat": "a fluctuation correlation is equated with causal response or converted into a psyche law", "control": "equilibrium class, conjugate perturbation, causal response, transform convention, physical units, and cross-pillar nonconversion"},
        {"id": "T12", "threat": "withdrawn evidence leaves a Stage 20 pass unchanged or dissent and negatives disappear", "control": "hash-bound domain decisions, necessary-evidence map, withdrawal replay, reversal reasons, dissent retention, and noncompensation"},
        {"id": "T13", "threat": "same-owner snapshots are called independent evidence", "control": "owner, protocol, infrastructure, and return provenance"},
        {"id": "T14", "threat": "bounded privacy or security scans are called exhaustive", "control": "declared pattern and mutation scope plus independent-review boundary"},
    ]
    write_json(phase / "threat-model.json", {
        "schema": "ghc.family.v644-v1.threat-model.v1", "phase": PHASE, "owner": OWNER,
        "threat_count": len(threats), "threats": threats, "exhaustive_security": False,
        "independent_security_review": False, "resource_ceilings": {"owner_generated_files": 15000, "scope": "v644-v1 only"},
        "boundary": BOUNDARY,
    })

    verified = snapshot_state == "verified"
    lifecycle_states = {"evidence": "EVIDENCE_VERIFIED" if verified else "EVIDENCE_CANDIDATE", "closeout": "CLOSEOUT_CANDIDATE", "seal": "SEALED_CANDIDATE", "final": "FINAL_HEAD_CANDIDATE"}
    protected_claims = {
        "empirical_gmut": False, "gmut_likelihood_or_unique_prediction": False,
        "thos_effectiveness_safety_or_superiority": False, "production_freed_id": False,
        "cbr_legitimacy_or_affected_party_acceptance": False, "maori_authority_or_data_governance": False,
        "legal_or_cultural_ratification": False, "deployment_or_production_readiness": False,
        "complete_accessibility": False, "exhaustive_security": False, "independent_team_reproduction": False,
        "proof_or_canon": False, "consciousness_personhood_agi_asi": False, "stage20_readiness": False,
    }
    write_json(phase / "phase-truth.json", {
        "schema": "ghc.family.v644-v1.phase-truth.v1", "phase": PHASE, "owner": OWNER,
        "state": lifecycle_states[lifecycle], "source_commit": SOURCE_COMMIT, "source_seal": SOURCE_SEAL, "x1_commit": X1_COMMIT,
        "proposal_count": 10, "distribution": distribution, "case_count": 80, "synthetic_rejection_count": 70,
        "retained_negative_count": len(negatives), "open_gap_count": len(open_gaps), "exact_gate_count": len(exact_gates),
        "primary_focus": "Freed ID/CBR Heart", "all_three_pillars_preserved": True,
        "same_owner_repeatability": verified, "independent_team_reproduction": False,
        "protected_claims": protected_claims, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT", "outbound_message_count": 0, "successor_task_count": 0, "subagent_count": 0,
        "boundary": BOUNDARY,
    })
    write_json(phase / "complete-incomplete-checklist.json", {
        "schema": "ghc.family.v644-v1.complete-incomplete-checklist.v1", "phase": PHASE, "owner": OWNER,
        "complete": [
            "exact Ilyra v643-v8 source, seal ancestry, clean state, and fresh live-remote equality verified",
            "existing clean Sable lane advanced by fast-forward only",
            "dedicated x1 freeze pushed, clean, and four-way equal before x2",
            "ten semantically distinct proposals executed only within frozen approval classes",
            "eighty deterministic fixtures with seventy retained rejecting mutations",
            "all inherited and new negatives retained without erasure",
            "GMUT Mind, THOS Body, and Freed ID/CBR Heart preserved",
            "current official or primary source constraints and status classes recorded",
        ],
        "incomplete": [
            "GMUT model-specific multi-messenger propagation derivation, licensed real rows, calibrated blind likelihood, prediction, force, or empirical confirmation",
            "preregistered blind matched-budget THOS arms, participants, raters, harms evidence, safety, effectiveness, or superiority",
            "production Freed ID real keys and proofs, live resolution and status, interoperability, privacy/security review, and trust governance",
            "CBR harm or remedy acceptance, Māori wording and authority, Māori data governance, cultural ratification, legal interpretation, or enacted-law status",
            "qualified manual, assistive-technology, and affected-user accessibility evaluation",
            "independent product or host security review and exhaustive security",
            "independent-team scientific reproduction and Stage 20 external decision",
        ],
        "lifecycle": lifecycle, "same_owner_evidence_snapshots_verified": verified,
        "closeout_ready": verified, "boundary": BOUNDARY,
    })
    write_json(phase / "environment/x2-execution-receipt.json", {
        "schema": "ghc.family.v644-v1.x2-execution-receipt.v1", "phase": PHASE, "owner": OWNER,
        "x1_commit": X1_COMMIT, "x1_remote_equal_before_x2": True,
        "real_data_downloaded": False, "real_participants_or_raters": 0, "real_arms": 0,
        "real_keys_or_proofs": 0, "live_services_or_deployments": 0, "accounts_or_api_keys_changed": 0,
        "desktop_updated": False, "elevation_used": False, "host_security_changed": False,
        "windows_feature_changed": False, "rebooted": False, "boundary": BOUNDARY,
    })
    write_json(phase / "reproduction/independent-team-gap.json", {
        "schema": "ghc.family.v644-v1.independent-team-gap.v1", "phase": PHASE, "owner": OWNER,
        "same_owner_evidence_snapshots_verified": verified, "shared_repository_protocol_and_infrastructure": True,
        "different_architecture_return_received": False, "independent_team_protocol_owned": False,
        "independent_team_return_received": False, "independent_team_reproduction_established": False, "boundary": BOUNDARY,
    })
    write_json(phase / "reproduction/evidence-snapshot-plan.json", {
        "schema": "ghc.family.v644-v1.evidence-snapshot-plan.v1", "phase": PHASE, "owner": OWNER,
        "snapshot_count": 2, "location_class": "fresh detached D-drive worktrees", "required_same_commit": True,
        "required_clean_before_and_after": True,
        "required_checks": ["complete repository suite", "detailed validator", "minimal validator", "all JSON parsing", "privacy and raw-ID scan", "manifest parity"],
        "claim_scope": "same-owner repeatability only", "independent_team_reproduction": False, "boundary": BOUNDARY,
    })
    write_json(phase / "reproduction/x1-content-seal.json", x1_content_seal(repo, phase))
    write_json(phase / "tooling/executed-toolchain.json", {
        "schema": "ghc.family.v644-v1.executed-toolchain.v1", "phase": PHASE, "owner": OWNER,
        "tools": [
            {"name": "scripts/ghc_family_v644_v1_model.py", "role": "frozen rule and seventy-mutation model"},
            {"name": "scripts/ghc_family_v644_v1_overview.py", "role": "three-page-equivalent boundary overview renderer"},
            {"name": "scripts/ghc_family_v644_v1_evidence.py", "role": "eighty-case evidence and retained-negative assembler"},
            {"name": "scripts/ghc_family_v644_v1_validator.py", "role": "detailed evidence, manifest, report, privacy, and boundary validator"},
            {"name": "scripts/ghc_family_v644_v1_minimal.py", "role": "small standard-library validation floor"},
            {"name": "scripts/ghc_family_v644_v1_complete_suite.py", "role": "semantic-hash-verified complete-suite adapter with exact byte restoration"},
            {"name": "scripts/ghc_family_v644_v1_staged_review.py", "role": "exact staged-blob, scope, deletion, x1-freeze, and diff-hygiene review"},
            {"name": "scripts/build_ghc_family_v644_v1_report.py", "role": "accessible static HTML report builder"},
            {"name": "tests/test_ghc_family_v644_v1.py", "role": "decision, mutation, retention, manifest, and validator regression suite"},
        ],
        "caller_compatibility_preserved": True, "inherited_tools_mutated": False,
        "mass_deletion_performed": False, "boundary": BOUNDARY,
    })
    vetoes = [
        {"domain": "GMUT Mind", "decision": "veto", "reason": "no model-specific multi-messenger derivation, licensed real rows, calibrated blind likelihood, physical prediction, force, or empirical confirmation"},
        {"domain": "THOS Body", "decision": "veto", "reason": "no preregistered blind matched-budget real arms, participants, raters, harms returns, or independent review"},
        {"domain": "Freed ID", "decision": "veto", "reason": "no real keys and proofs, live resolution and status, interoperability, reviews, or trust governance"},
        {"domain": "CBR and Māori authority", "decision": "veto", "reason": "harm, remedy, affected-party, Māori, cultural, and legal authority cannot be substituted"},
        {"domain": "reproduction", "decision": "veto", "reason": "shared owner, protocol, repository, and infrastructure; no independent return"},
        {"domain": "accessibility and security", "decision": "veto", "reason": "manual, affected-user, and independent review remain missing"},
    ]
    write_json(phase / "stage20/domain-veto-evidence-board.json", {
        "schema": "ghc.family.v644-v1.stage20-board.v1", "phase": PHASE, "owner": OWNER,
        "vetoes": vetoes, "compensation_across_domains_allowed": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY,
    })
    write_text(phase / "deliverables/v644-v1-final-integrated-overview.md", overview_text(distribution, len(negatives)))

    manifest_rows = []
    for relative in manifest_candidates(repo, phase):
        target = repo / relative
        data = normalized_bytes(target)
        manifest_rows.append({"repo_path": relative, "sha256_lf_normalized": hashlib.sha256(data).hexdigest(), "bytes_lf_normalized": len(data)})
    write_json(phase / "reproduction/manifest.json", {
        "schema": "ghc.family.v644-v1.manifest.v1", "phase": PHASE, "owner": OWNER,
        "hash_algorithm": "sha256", "text_normalization": "CRLF and CR normalized to LF before hashing",
        "entry_count": len(manifest_rows), "entries": manifest_rows, "snapshot_state": snapshot_state,
        "same_owner_repeatability_only": True, "independent_team_reproduction": False, "boundary": BOUNDARY,
    })
    return {
        "phase": PHASE, "proposal_count": 10, "case_count": 80, "rejections": 70,
        "distribution": distribution, "retained_negatives": len(negatives),
        "x1_operational_negatives": len(x1_negatives), "x2_operational_negatives": len(X2_OPERATIONAL_NEGATIVES),
        "manifest_entries": len(manifest_rows), "snapshot_state": snapshot_state, "lifecycle": lifecycle,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--snapshot-state", choices=("pending", "verified"), default="pending")
    parser.add_argument("--lifecycle", choices=("evidence", "closeout", "seal", "final"), default="evidence")
    args = parser.parse_args()
    print(json.dumps(build(args.repo, args.snapshot_state, args.lifecycle), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
