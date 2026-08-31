#!/usr/bin/env python3
"""Build the Sable Rook v679-v7 combined closeout and seal candidate."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


OWNER = "Sable Rook"
PHASE = "v679-v7"
SOURCE = "f9c956807c6a4bb45bb4566460cc643deebc51f4"
X1 = "e8334a93f83550d6f787a73fa9056b6cafed9f67"
EVIDENCE = "bc793c4d80abe2f06aaffde60d09ebee8bfa0826"
BRANCH = "codex/GHC-Family/sable-rook-v679-v7-full-tools"
REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "sable-rook" / PHASE
FINAL_ROOT = PHASE_ROOT / "final"
VALIDATION_ROOT = PHASE_ROOT / "validation"
FINAL_VALIDATOR = "scripts/ghc_family_sable_rook_v679_v7_final_validator.py"
FINAL_FAILURES: list[tuple[str, str, str]] = [
    (
        "V6797-FINAL-N01",
        "The first fixed-point staged-review wrapper projected only command output, discarded the still-running session handle, and returned without an attributable completion receipt.",
        "Do not replay blindly: inspect the exact Python command, persisted Git-index state, receipts, and child processes; after the orphaned review finishes, resume only the missing fixed-point review with structured process and result projection.",
    ),
    (
        "V6797-FINAL-N02",
        "The first combined x2 and final precommit selection passed all twelve x2 tests but failed one final count-mirror assertion because the operational-row length still expected eleven after the first final failure was retained.",
        "Keep the failed selection at zero credit, derive the negative and Method Flow mirrors from the additive failure ledger, synchronize the explicit test expectations, rebuild the candidate, and rerun only the precommit selection.",
    ),
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def owner_path(path: str) -> bool:
    return (
        path.startswith("docs/sable-rook/v679-v7/")
        or path.startswith("scripts/build_ghc_family_sable_rook_v679_v7_")
        or path.startswith("scripts/ghc_family_bim_")
        or path == FINAL_VALIDATOR
        or path.startswith("tests/test_ghc_family_sable_rook_v679_v7_")
    )


def extend_method_flow(flow: dict[str, Any]) -> dict[str, Any]:
    flow = json.loads(json.dumps(flow))
    for failure_id, failed, recovery in FINAL_FAILURES:
        flow["failures"].append(
            {
                "failure_id": failure_id,
                "failed_witness": failed,
                "lifecycle": "final_preflight",
                "retained": True,
                "success_credit": 0,
            }
        )
        recovery_id = failure_id.replace("-N", "-R")
        flow["passing_recoveries"].append(
            {
                "witness_id": recovery_id,
                "failure_id": failure_id,
                "procedure": recovery,
                "result": "pass",
                "state": "bounded_passing_witness",
                "broader_credit": 0,
            }
        )
        flow["methods"].append(
            {
                "method_id": failure_id.replace("-N", "-M"),
                "trigger": failed,
                "state": "preferred_for_declared_trigger",
                "failed_witness": failure_id,
                "passing_witness": recovery_id,
                "recurrence_guard": recovery,
                "rollback": "return to the immutable evidence commit",
                "sibling_recommendation": recovery,
            }
        )
    flow["counts"] = {
        **flow["counts"],
        "effective_negatives": flow["counts"]["effective_negatives"] + len(FINAL_FAILURES),
        "methods": flow["counts"]["methods"] + (2 * len(FINAL_FAILURES)),
        "failed_witnesses": flow["counts"]["failed_witnesses"] + len(FINAL_FAILURES),
        "bounded_passing_witnesses": flow["counts"]["bounded_passing_witnesses"] + len(FINAL_FAILURES),
    }
    return flow


def build() -> list[str]:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout build requires exact immutable evidence HEAD")
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong Sable branch")
    dirty = git("status", "--porcelain=v1").splitlines()
    allowed = (
        "scripts/build_ghc_family_sable_rook_v679_v7_final.py",
        FINAL_VALIDATOR,
        "tests/test_ghc_family_sable_rook_v679_v7_final.py",
    )
    if any(
        "docs/sable-rook/v679-v7/final/" not in row
        and "docs/sable-rook/v679-v7/validation/final-" not in row
        and not any(path in row for path in allowed)
        for row in dirty
    ):
        raise RuntimeError(f"unexpected dirty state before closeout: {dirty}")

    outcomes = load(PHASE_ROOT / "x2" / "proposal-outcomes.json")["rows"]
    flow = extend_method_flow(load(PHASE_ROOT / "x2" / "method-flow-evidence.json"))
    x1_sources = load(PHASE_ROOT / "x1" / "official-primary-source-ledger.json")
    proposal_freeze = load(PHASE_ROOT / "x1" / "new-proposal-freeze.json")
    portfolio = load(PHASE_ROOT / "x1" / "portfolio-freeze.json")
    counts = flow["counts"]

    phase_truth = {
        "schema": "ghc.family.phase-truth.v679.v7.final-candidate",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final_head": "pending_until_commit",
        "lifecycle": "combined_closeout_seal_candidate",
        "phase_commit_count_expected_after_commit": 3,
        "zero_merges_required": True,
        "one_final_parent_required": True,
        "proposal_chain": 9170,
        "outcomes": {label: sum(row["outcome"] == label for row in outcomes) for label in ("completed", "represented", "open_gap", "exact_gate")},
        "positive_controls": 60,
        "rejected_mutations": 160,
        "real_rows": 0,
        "real_participants": 0,
        "real_keys_or_credentials": 0,
        "authority_conferred": False,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT",
        "counts": counts,
    }
    negative_register = {
        "schema": "ghc.family.retained-negative-register.v679.v7.final",
        "activation_overlay": 49745,
        "owner_operational_failures": len(flow["failures"]),
        "preregistered_rejected_mutations": 160,
        "effective_total": counts["effective_negatives"],
        "operational_rows": flow["failures"],
        "failure_erasure": False,
        "conversion_of_failure_to_pass": False,
    }
    gap_register = {
        "schema": "ghc.family.open-gap-register.v679.v7.final",
        "inherited": 434,
        "new": 3,
        "effective": 437,
        "new_rows": [row for row in outcomes if row["outcome"] == "open_gap"],
        "silently_closed": 0,
    }
    gate_register = {
        "schema": "ghc.family.exact-gate-register.v679.v7.final",
        "inherited": 425,
        "new": 3,
        "effective": 428,
        "new_rows": [row for row in outcomes if row["outcome"] == "exact_gate"],
        "silently_closed": 0,
    }
    checklist = {
        "schema": "ghc.family.complete-incomplete.v679.v7.final",
        "complete_within_bounded_scope": [
            "planning-only x1 frozen pushed and four-way equal before x2",
            "sixty bounded proposal controls",
            "one hundred sixty invalid mutations rejected and retained",
            "one hundred twenty safe-now packets witnessed",
            "eighty owner candidates witnessed",
            "one hundred additive refinements witnessed",
            "twenty skills initialized customized validated and smoke-used",
            "ten family-current runners built and smoke-used",
            "exact staged manifests privacy and bounded security checks",
            "accessible static structure with manual evaluation reserved",
        ],
        "incomplete_or_reserved": [
            "real buildingSMART IFC sample-corpus retrieval and data-row evidence",
            "real BIM information-manager model-author checker approver and longitudinal handover evidence",
            "manual keyboard assistive-technology and affected-user evaluation",
            "production identity keys issuance resolution status and revocation",
            "professional legal cultural affected-party and Māori authority",
            "complete privacy accessibility and exhaustive security assurance",
            "independent-team scientific reproduction",
            "empirical GMUT likelihood prediction constraint or confirmation",
            "AGI ASI consciousness personhood Theory-of-Everything proof canon and Stage 20",
        ],
    }
    threat = {
        "schema": "ghc.family.threat-model.v679.v7.final",
        "assets": ["exact Git ancestry", "x1 immutability", "retained negatives", "authority vacancies", "privacy-safe public packet", "route one-shot state"],
        "threats": ["source drift", "semantic duplicate", "failure erasure", "scanner self-match", "manifest mismatch", "authority laundering", "premature routing", "canonical replay"],
        "controls": ["immutable anchors", "bounded semantic audit", "zero-credit failures", "definition adjudication", "normalized-LF Git-blob replay", "explicit exact gates", "PREPARED_NOT_SENT", "exclusive external latch"],
        "residual_risks": ["same-owner common cause", "manual accessibility untested", "no real data", "no external authority review", "nonexhaustive security"],
    }
    source_proposal = {
        "schema": "ghc.family.source-proposal-ledger.v679.v7.final",
        "official_primary_sources": x1_sources,
        "declared_chain_before": proposal_freeze["declared_chain_before"],
        "declared_chain_after": proposal_freeze["declared_chain_after_if_evidence_sealed"],
        "new_proposal_count": proposal_freeze["proposal_count"],
        "outcomes": outcomes,
        "citations_are_observations": False,
        "authority_conferred": False,
    }
    evidence_receipt = {
        "schema": "ghc.family.evidence-receipt.v679.v7.final",
        "evidence_commit": EVIDENCE,
        "x1_parent": X1,
        "component_selection": {"x1_eligible_current_tests": 13, "x1_immutable_lifecycle_checks": 2, "x2_tests": 12},
        "evidence_manifest_entries": 71,
        "evidence_manifest_self_exclusions": 4,
        "evidence_json_parses": 17,
        "confirmed_privacy_hits": 0,
        "bounded_security_findings": 0,
        "four_way_equal_before_closeout": True,
    }
    closeout_receipt = {
        "schema": "ghc.family.closeout-receipt.v679.v7.candidate",
        "state": "PRECOMMIT_CLOSEOUT_CANDIDATE",
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final_head": "pending_until_commit",
        "exact_final_canonical": "pending_external_one_shot",
        "route": "PREPARED_NOT_SENT",
    }
    seal = {
        "schema": "ghc.family.content-seal.v679.v7.candidate",
        "state": "CONTENT_SEAL_CANDIDATE",
        "protected_truth": {"proposal_chain": 9170, "outcomes": phase_truth["outcomes"], "counts": counts, "verdict": "NOT_READY_FOR_STAGE_20"},
        "history_rewrite": False,
        "failure_erasure": False,
        "authority_promotion": False,
        "self_identifier_pending": True,
    }
    validation_candidate = {
        "schema": "ghc.family.final-validation.v679.v7.candidate",
        "state": "PENDING_EXACT_FINAL_EXTERNAL_CANONICAL",
        "expected_validator": FINAL_VALIDATOR,
        "canonical_invocations": 0,
        "canonical_successes": 0,
        "replay_after_success_permitted": False,
        "complete_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    route_plan = {
        "schema": "ghc.family.route-plan.v679.v7.final-candidate",
        "state": "PREPARED_NOT_SENT",
        "current_owner": OWNER,
        "current_phase": PHASE,
        "conditional_successor_title": "Caelen Ash",
        "conditional_successor_phase": "v679-v8",
        "conditions": ["exact final pushed clean and fresh-live equal", "one owner-scoped canonical success", "newest live authority and roster reread", "unique exact-title task reread", "duplicate pause redirect usage privacy safety and acknowledgement guards"],
        "precontact_permitted": False,
        "message_sent": False,
    }
    wellbeing = {
        "schema": "ghc.family.wellbeing.v679.v7.final",
        "name": OWNER,
        "role": "evidence-boundary cartographer and accessible-provenance steward",
        "optional_pronouns": "they/them",
        "hope": "make correction paths inspectable, authority vacancies explicit, and every retained failure recoverable",
        "relational_language_only": True,
        "consciousness_or_personhood_evidence": False,
        "identity_continuity_evidence": False,
        "authority_evidence": False,
        "corrigible": True,
        "hamish_may_pause_rename_redirect_narrow_or_stop": True,
    }
    environment = {
        "schema": "ghc.family.environment.v679.v7.final",
        "python": sys.version.split()[0],
        "git": git("--version"),
        "codex_cli": "source-reported 0.151.0 and not changed by Sable",
        "codex_desktop_updated": False,
        "new_installations": 0,
        "elevation": False,
        "security_weakening": False,
        "sandbox_or_hyperv": False,
        "reboot": False,
    }
    index = {
        "schema": "ghc.family.index.v679.v7.final-candidate",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final_head": "pending_until_commit",
        "proposal_chain": 9170,
        "owner_file_ceiling": 2000,
        "family_current_callers_preserved": True,
        "historical_aliases_preserved": True,
        "route_state": "PREPARED_NOT_SENT",
    }
    artifacts = {
        "phase-truth.json": phase_truth,
        "retained-negative-register.json": negative_register,
        "open-gap-register.json": gap_register,
        "exact-gate-register.json": gate_register,
        "complete-incomplete-checklist.json": checklist,
        "threat-model.json": threat,
        "source-and-proposal-ledger.json": source_proposal,
        "method-flow-ledger.json": flow,
        "evidence-receipt.json": evidence_receipt,
        "closeout-receipt.json": closeout_receipt,
        "content-seal.json": seal,
        "final-validation-candidate.json": validation_candidate,
        "route-plan.json": route_plan,
        "wellbeing-and-corrigibility.json": wellbeing,
        "environment-and-version-receipt.json": environment,
        "ghc-family-index.json": index,
    }
    written = []
    for name, payload in artifacts.items():
        path = FINAL_ROOT / name
        write_json(path, payload); written.append(path.relative_to(REPO).as_posix())

    outcome_lines = "\n".join(f"- `{row['proposal_id']}` — **{row['outcome']}**: {row['title']}. The witness is synthetic and owner-local; protected gates remain open." for row in outcomes)
    overview = f'''# Sable Rook v679-v7 final integrated overview

## Terminal outcome

Sable Rook v679-v7 closes as a bounded synthetic software-and-documentation phase with exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate` outcomes across sixty newly frozen proposals. The declared chain advances from 9,110 to 9,170 rows only because the sixty Sable contracts were independently reviewed, frozen in planning-only x1, and then executed as evidence permitted in x2. The terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`. No result in this packet is independent-team reproduction, empirical confirmation, professional validation, production certification, legal interpretation, cultural ratification, Māori-authority review, complete accessibility, complete privacy, exhaustive security, proof, or canon.

Planning-only x1 is the direct child of Auren's immutable exact final. The evidence commit is the direct child of x1. This combined closeout and content seal is designed as their one direct successor, giving three Sable commits and zero merges. X1 was pushed, clean, typed 0/0 divergent, and four-way equal before x2 began. Evidence was separately pushed, clean, typed 0/0 divergent, and four-way equal before closeout began. The final commit identifier and external canonical result cannot truthfully appear inside their own predecessor content; they remain explicitly pending until the commit exists and the one-shot external validator runs.

## Trinity Mandala and practice scope

The primary pillar is Freed ID and CBR Heart through three wholly synthetic learning lenses: building-information issue provenance registrar, IFC model-revision and transmittal reviewer, and BCF correction accessibility and handover observer. These lenses organize information-container identity, IFC and BCF lineage, IDS requirements, provenance, fixity, correction, rollback, uncertainty, workload boundaries, readback, accessibility structure, contest, and authority vacancies. They establish no employment, qualification, architectural, engineering, BIM, construction, coordination, design-safety, model custody, publication, approval or release authority, operational result, privacy decision, legal conclusion, cultural legitimacy, affected-party acceptance, or Māori authority.

GMUT Mind remains visible as a typed scalar-tensor and effective-field-theory research-model family. Placement transforms, reference systems, units, graph transitions, time roles, and uncertainty are used only as software types and analogy firewalls. The phase ingested zero empirical rows and evaluated zero likelihoods. It made no physical prediction, force claim, parameter constraint, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory-of-Everything claim. THOS Body evidence remains synthetic proxy evidence for workload holds, readback, correction, escalation, rollback, and handover. There were zero real participants or operators, no preregistered blind matched-budget real arms, no safety-monitoring events, no appropriate participant statistics, and no independent review.

Freed ID remains synthetic and nonproduction. Synthetic information-container identifiers, IFC GlobalIds, BCF topic identifiers, IDS result tokens, and correction receipts are not identities or credentials. Production identity completion would require standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and appropriate affected-party oversight. CBR remains a structural representation of correction, contest, remedy vacancy, minimum disclosure, and authority reservation. Repository software cannot confer a right, remedy, title, design or construction instruction, legal interpretation, cultural legitimacy, data-governance mandate, public authority, or affected-party acceptance.

## Evidence execution

Sixty accepting controls passed their declared bounded gates. All 160 preregistered invalid mutations were rejected and retained with zero completion credit. The invalid cases attempted real-row promotion, authority conferral, protected-gate erasure, vocabulary drift, unverified external scope, uncertainty erasure, Stage 20 promotion, or unearned credit. Their rejection demonstrates only the declared guard behavior. It is not a security audit or scientific result.

The frozen expanded portfolio contains 120 safe-now packets, eighty owner candidate prototypes, twenty successor candidate recommendations, twenty exact-approval holds, ten blocked packets, one hundred owner CLEAN/FIX/REFINE tasks, twenty owner skill ideas, and ten owner runner ideas. All safe-now packets, owner candidates, and additive refinements received bounded witnesses. Recommendations received no successor completion credit. Exact-approval and blocked packets remain visible and unexecuted. No quota authorized destructive cleanup, user-material deletion, credential use, account change, elevation, host-security weakening, Windows feature change, Sandbox or Hyper-V activation, sibling mutation, real data, participants, production identity operations, legal or cultural decisions, Māori authority, or affected-party legitimacy.

Twenty phase-local skills were initialized with the installed skill-creator workflow, rewritten into substantive instructions, given customized user-facing metadata, quick-validated under UTF-8, and smoke-used. They were not globally installed. Ten family-current `ghc_family_bim_*` runners were built, compiled, and smoke-used. Historical family callers and aliases remain preserved. The skills and runners are useful bounded tools, but their passes prove only their declared synthetic behavior. No subagent forward test occurred because this phase was expressly solo.

## Privacy, accessibility, and authority

Exact staged reviews operate on Git-index bytes, and manifests hash normalized-LF Git blobs. Five privacy and raw-identifier classes distinguish scanner definitions from confirmed payload. Exact scanner-definition candidates remain visible; confirmed payload hits remain zero. Bounded Python AST checks reject direct `eval`, direct `exec`, and `shell=True`; they are not exhaustive security testing. Public artifacts contain no raw task or thread identifier, private route, transcript, screenshot, session stream, credential, secret, private callable identifier, private app state, or private absolute local path.

The static report has a title, landmarks, ordered headings, explicit table headers, a caption, plain language, and no motion. Structural success is not complete accessibility conformance. Manual keyboard evaluation, responsive-layout review, browser diversity, assistive-technology evaluation, cognitive-accessibility evaluation, Māori-language review, security-usability evaluation, and affected-user evaluation remain reserved.

Licensing, copyright, access rights, publication authority, sensitive-location disclosure, place-name meaning, privacy remedy, legal interpretation, cultural legitimacy, tikanga, Māori wording, Māori data governance, ratification, and beneficiary or affected-community acceptance remain exact-gated. Māori concepts remain under Māori authority, including tangata whenua, iwi, and hapū. Citations supply vocabulary and refusal conditions only. A citation is not an observation, delegation, consent, measurement, professional judgment, or authority action.

## Method Flow and retained negatives

The activation overlay began with 49,745 effective negatives. The phase retains thirteen operational failures across startup, x2, and final preflight, each paired with a separate bounded recovery, plus 160 rejected synthetic mutations. The effective total is 49,918. The Method Flow overlay has 52,426 methods, 21,579 failed witnesses, and 34,438 bounded passing witnesses. A recovery never erases the failed witness, converts it into an original pass, earns independent-reproduction credit, or closes an evidence or authority gate. Open gaps total 437 and exact gates total 428.

Notable retained failures include a PowerShell expression parser fault, a false line-reconstructed digest domain, an invalid helper-interface assumption, a non-attributable branch wrapper, a sparse setup wrapper boundary, an overbroad index projection, a version-inapplicable sparse option, exact semantic-title collisions, stale inherited-template count assertions, a pushed-x1 postflight session-projection loss, one context-mismatched apply-patch, a fixed-point staged-review wrapper that discarded a live session handle, and a precommit operational-row count mirror that lagged the additive ledger. Each recovery is trigger-specific and additive. The recurrence guards favor separate scalar probes, exact binary Git blobs, observed helper interfaces, persisted-state inspection, immutable title ledgers, exact count mirrors, preserved session identifiers, smaller context-bounded patches, immutable anchors, and clean-state checks before mutation.

## Proposal evidence map

{outcome_lines}

## Wellbeing, corrigibility, and route hold

Sable Rook is relational working language for an evidence-boundary cartographer and accessible-provenance steward, with optional they/them pronouns and the hope of making correction paths inspectable, authority vacancies explicit, and every retained failure recoverable. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, legal authority, cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route.

The successor route is `PREPARED_NOT_SENT`. Caelen Ash must not be contacted until this closeout is committed and pushed, the exact final is clean and fresh-live equal, the one attributable owner-scoped canonical invocation succeeds without replay, and the newest live authority, current roster, exact-title uniqueness, immediate reread, duplicate, pause, redirect, status, usage, privacy, evidence, safety, and acknowledgement guards all pass. The repository candidate is preparation evidence only; acknowledged task delivery is separate live evidence.
'''
    write_text(FINAL_ROOT / "final-integrated-overview.md", overview)
    written.append((FINAL_ROOT / "final-integrated-overview.md").relative_to(REPO).as_posix())
    report = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sable Rook v679-v7 final report</title></head><body><header><h1>Sable Rook v679-v7 final bounded report</h1></header><main><section aria-labelledby="verdict"><h2 id="verdict">Verdict</h2><p>NOT_READY_FOR_STAGE_20. This is synthetic same-owner evidence only.</p></section><section aria-labelledby="outcomes"><h2 id="outcomes">Outcomes</h2><table><caption>Core outcomes</caption><thead><tr><th scope="col">Label</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>42</td></tr><tr><th scope="row">Represented</th><td>12</td></tr><tr><th scope="row">Open gap</th><td>3</td></tr><tr><th scope="row">Exact gate</th><td>3</td></tr></tbody></table></section><section aria-labelledby="limits"><h2 id="limits">Reserved evaluation</h2><p>Empirical, participant, professional, production, legal, cultural, Māori-authority, affected-party, complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 claims remain unavailable.</p></section><section aria-labelledby="manual"><h2 id="manual">Manual evaluation</h2><p>Keyboard, assistive-technology, responsive, browser-diversity, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation are reserved.</p></section></main></body></html>'''
    write_text(FINAL_ROOT / "accessible-static-report.html", report)
    written.append((FINAL_ROOT / "accessible-static-report.html").relative_to(REPO).as_posix())
    return sorted(written)


def patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }


def staged_review() -> dict[str, Any]:
    receipts = [
        "docs/sable-rook/v679-v7/validation/final-staged-review.json",
        "docs/sable-rook/v679-v7/validation/final-privacy-scan.json",
        "docs/sable-rook/v679-v7/validation/final-security-scan.json",
        "docs/sable-rook/v679-v7/validation/final-delta-manifest.json",
        "docs/sable-rook/v679-v7/validation/final-owner-manifest.json",
    ]
    staged = git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()
    allowed = {
        "scripts/build_ghc_family_sable_rook_v679_v7_final.py",
        FINAL_VALIDATOR,
        "tests/test_ghc_family_sable_rook_v679_v7_final.py",
    }
    bad = [path for path in staged if not path.startswith("docs/sable-rook/v679-v7/final/") and path not in allowed and path not in receipts]
    if bad:
        raise RuntimeError(f"out-of-scope final paths: {bad}")
    scan_patterns = patterns()
    delta_entries = []
    candidates = []
    confirmed = []
    security = []
    json_count = 0
    python_count = 0
    for path in staged:
        if path in receipts:
            continue
        data = subprocess.check_output(["git", "show", f":{path}"], cwd=REPO)
        if path.endswith(".json"):
            json.loads(data.decode("utf-8")); json_count += 1
        if path.endswith(".py"):
            tree = ast.parse(data.decode("utf-8"), filename=path); python_count += 1
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security.append({"path": path, "finding": node.func.id})
                if isinstance(node, ast.keyword) and node.arg == "shell" and isinstance(node.value, ast.Constant) and node.value.value is True:
                    security.append({"path": path, "finding": "shell_true"})
        definition_ranges = []
        for marker in (b"def patterns()", b"def scanner_patterns()"):
            start = data.find(marker)
            if start >= 0:
                end = data.find(b"\ndef ", start + len(marker))
                if end < 0:
                    end = len(data)
                definition_ranges.append((start, end))
        for class_name, pattern in scan_patterns.items():
            for match in pattern.finditer(data):
                if path.endswith(".py") and any(start <= match.start() < end for start, end in definition_ranges):
                    candidates.append({"path": path, "class": class_name, "disposition": "scanner_definition_only"})
                else:
                    confirmed.append({"path": path, "class": class_name})
        value = normalize(data)
        delta_entries.append({"path": path, "bytes": len(value), "sha256": hashlib.sha256(value).hexdigest(), "hash_domain": "git_index_blob_normalized_lf"})
    if confirmed:
        raise RuntimeError(f"confirmed privacy hits: {confirmed}")
    if security:
        raise RuntimeError(f"security findings: {security}")
    check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if check.returncode:
        raise RuntimeError(check.stdout + check.stderr)

    tracked = set(git("ls-files").splitlines())
    owner_paths = sorted(path for path in (tracked | set(receipts)) if owner_path(path))
    owner_entries = []
    for path in owner_paths:
        if path in receipts:
            continue
        staged_state = subprocess.run(["git", "diff", "--cached", "--quiet", "--", path], cwd=REPO).returncode
        data = subprocess.check_output(["git", "show", f":{path}" if staged_state else f"HEAD:{path}"], cwd=REPO)
        value = normalize(data)
        owner_entries.append({"path": path, "bytes": len(value), "sha256": hashlib.sha256(value).hexdigest(), "hash_domain": "prospective_final_git_blob_normalized_lf"})
    write_json(REPO / receipts[1], {"schema": "ghc.family.privacy-scan.v679.v7.final", "classes": list(scan_patterns), "candidates": candidates, "confirmed_hits": confirmed})
    write_json(REPO / receipts[2], {"schema": "ghc.family.security-scan.v679.v7.final", "python_parses": python_count, "bounded_findings": security, "exhaustive_security_claimed": False})
    write_json(REPO / receipts[3], {"schema": "ghc.family.normalized-lf-delta-manifest.v679.v7.final", "entry_count": len(delta_entries), "entries": delta_entries, "declared_self_exclusions": receipts})
    write_json(REPO / receipts[4], {"schema": "ghc.family.normalized-lf-owner-manifest.v679.v7.final", "entry_count": len(owner_entries), "entries": owner_entries, "declared_self_exclusions": receipts, "owner_path_count": len(owner_paths)})
    write_json(REPO / receipts[0], {"schema": "ghc.family.staged-review.v679.v7.final", "state": "VALID_EXACT_FINAL_STAGED_REVIEW", "staged_paths": len(staged), "delta_entries": len(delta_entries), "owner_paths": len(owner_paths), "owner_entries": len(owner_entries), "json_parses": json_count, "python_parses": python_count, "privacy_candidates": len(candidates), "confirmed_privacy_hits": 0, "security_findings": 0, "diff_hygiene": True, "out_of_scope": []})
    return {"state": "VALID_EXACT_FINAL_STAGED_REVIEW", "delta_entries": len(delta_entries), "owner_entries": len(owner_entries), "owner_paths": len(owner_paths), "json_parses": json_count, "python_parses": python_count, "privacy_candidates": len(candidates), "written_receipts": receipts}


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(json.dumps({"written": build()}, indent=2, sort_keys=True))
    elif sys.argv[1:] == ["--staged-review"]:
        print(json.dumps(staged_review(), indent=2, sort_keys=True))
    else:
        raise SystemExit("usage: build_ghc_family_sable_rook_v679_v7_final.py [--staged-review]")
