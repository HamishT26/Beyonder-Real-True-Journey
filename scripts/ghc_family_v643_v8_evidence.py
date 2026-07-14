#!/usr/bin/env python3
"""Build bounded Ilyra Fen v643-v8 evidence from the frozen x1 model."""

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


PHASE = "v643-gmut-thos-v8-x1-x2"
OWNER = "Ilyra Fen"
SOURCE_COMMIT = "428e2da33b504e45d7d4863b2d68e3ec48bcf6d5"
SOURCE_SEAL = "f20303c33bf4d8ba4e7dc0c34c614a3f0038f61b"
X1_COMMIT = "3d36e88ae05b1b41654518b9bedf34adefb338ba"
TRUTH_LABELS = ("completed", "represented", "open_gap", "exact_gate")
PHASE_REL = "docs/ilyra-fen/v643-v8"

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
    path = repo / "scripts/ghc_family_v643_v8_model.py"
    spec = importlib.util.spec_from_file_location("ghc_family_v643_v8_model_runtime", path)
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


# Add only actual v643-v8 x2 operational failures. Rejected preregistered
# mutations are assembled separately and never hidden by later success.
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6438-X2-N01",
        "origin": "v643-v8-x2-operational",
        "observed": (
            "An independent staged-name hash check attempted to use Convert.ToHexString, but the available "
            "Windows PowerShell/.NET surface did not provide that method, so the command returned a null hash."
        ),
        "recovery": (
            "Retain the failed check, compute the SHA-256 with the portable BitConverter byte-to-hex path, "
            "and compare it with the frozen staged-name receipt."
        ),
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6438-X2-N02",
        "origin": "v643-v8-x2-operational",
        "observed": (
            "A combined evidence-script inspection returned exit code one because an optional ripgrep term had "
            "no match, even though the requested source excerpt was read successfully."
        ),
        "recovery": (
            "Retain the wrapper failure, separate required reads from optional searches, and treat a bounded "
            "no-match search as an inspected absence rather than allowing it to mask successful output."
        ),
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6438-X2-N03",
        "origin": "v643-v8-x2-operational",
        "observed": (
            "A broad recursive search for privacy and raw-ID scanner names exceeded its bounded command timeout "
            "without returning a tool path."
        ),
        "recovery": (
            "Retain the timeout, narrow discovery to known phase tooling and direct script-directory metadata, "
            "then run the located scanner with an explicit bounded scope."
        ),
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6438-X2-N04",
        "origin": "v643-v8-x2-operational",
        "observed": (
            "The wrapper that added both fresh evidence worktrees exceeded its 120-second command timeout while "
            "the detached checkouts were materializing; both worktrees later proved complete, clean, and exact."
        ),
        "recovery": (
            "Retain the timeout, inspect each new path directly, verify its exact detached head and clean state, "
            "and validate the two snapshots separately without deleting or reusing either worktree."
        ),
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6438-X2-N05",
        "origin": "v643-v8-x2-operational",
        "observed": (
            "The first post-timeout worktree-registry query also exceeded its short timeout before returning "
            "registry output."
        ),
        "recovery": (
            "Retain the failed registry query, use direct bounded path-state checks first, then verify HEAD and "
            "clean status from inside each detached snapshot with a longer timeout."
        ),
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6438-X2-N06",
        "origin": "v643-v8-x2-operational",
        "observed": (
            "The first closeout repository-suite run passed 497 of 500 tests; the three failures all identified "
            "the closeout receipt hash as stale after its detailed-validation total was corrected."
        ),
        "recovery": (
            "Retain the failed run, write the known closeout counts before rebuilding the normalized manifest, "
            "then rerun the complete repository suite and validators."
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
        "schema": "ghc.family.v643-v8.x1-content-seal.v1", "phase": PHASE, "owner": OWNER,
        "x1_commit": X1_COMMIT, "entry_count": len(rows), "entries": rows,
        "all_unchanged": all(row["unchanged"] for row in rows),
        "boundary": "This seal proves frozen x1 bytes remained unchanged; it does not turn expected dispositions into evidence.",
    }


def open_and_exact_gates() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    open_gaps = [
        {"gate_id": "OPEN-01", "domain": "GMUT empirical joint likelihood", "state": "open", "requires": ["model-specific observable derivation", "licensed real background and growth rows", "joint covariance and nuisance plan", "frozen external baselines", "blind holdout", "independent review"]},
        {"gate_id": "OPEN-02", "domain": "THOS real-arm evidence", "state": "open", "requires": ["ethics", "consent", "preregistered blind matched-budget arms", "real participants and raters", "harms monitoring", "independent review"]},
        {"gate_id": "OPEN-03", "domain": "Freed ID production completion", "state": "open", "requires": ["standards-conformant real keys and proofs", "live resolution", "status and revocation", "interoperability", "privacy and security review", "trust governance"]},
        {"gate_id": "OPEN-04", "domain": "qualified accessibility evaluation", "state": "open", "requires": ["manual evaluation", "assistive-technology coverage", "affected-user evaluation"]},
        {"gate_id": "OPEN-05", "domain": "independent-team scientific reproduction", "state": "open", "requires": ["independent team", "independently owned protocol", "independent infrastructure", "returned evidence"]},
    ]
    exact_gates = [
        {"gate_id": "EXACT-01", "domain": "affected-party harm and remedy acceptance", "state": "pending_exact_authority"},
        {"gate_id": "EXACT-02", "domain": "Māori wording, authority, and data governance", "state": "pending_exact_authority"},
        {"gate_id": "EXACT-03", "domain": "cultural ratification and community-defined residual risk", "state": "pending_exact_authority"},
        {"gate_id": "EXACT-04", "domain": "legal interpretation and enacted-law status", "state": "pending_exact_authority"},
        {"gate_id": "EXACT-05", "domain": "destructive, account, credential, API-key, or sibling-merge action", "state": "pending_exact_authority"},
        {"gate_id": "EXACT-06", "domain": "Stage 20 external decision authority", "state": "pending_exact_authority"},
    ]
    return open_gaps, exact_gates


def overview_text(distribution: dict[str, int], negative_count: int) -> str:
    return f"""# Ilyra Fen v643-v8 final integrated overview

## 1. Executive boundary and disposition

v643-v8 is a bounded GMUT/THOS evidence-engineering phase owned in the existing Ilyra Fen lane. Its primary focus is GMUT Mind, while THOS Body and Freed ID/CBR Heart remain explicit. Exactly ten x1 proposals were frozen before x2. The observed distribution is {distribution['completed']} completed, {distribution['represented']} represented or proxy, {distribution['open_gap']} open gap, and {distribution['exact_gate']} exact gate. Those four labels are the entire phase truth vocabulary. “Completed” means a local deterministic artifact and its falsifiers behaved as preregistered. It does not mean a scientific, participant, production, legal, cultural, accessibility-complete, security-complete, or deployment result.

The phase inherits Eiren Kestrel v643-v7 at exact head `{SOURCE_COMMIT}` and exact seal `{SOURCE_SEAL}`. The dedicated x1 freeze is `{X1_COMMIT}`. Before x2, x1 was pushed and proved equal across local, upstream, tracking, and a fresh live-remote read. The source-to-x1 path was single-parent and zero-merge. No sibling lane was reset, merged, rewritten, deleted, or force-pushed. D-drive storage remained the primary work and validation bank. Identity language—“Ilyra Fen”, she/they, evidence-boundary steward—is relational working language only and is not evidence of consciousness, sentience, legal personhood, identity continuity, or independent authority.

The terminal verdict is **NOT_READY_FOR_STAGE_20**. No local score can compensate for a missing real-data, participant, production, affected-party, Māori-authority, cultural, legal, accessibility, security, or independent-reproduction requirement. The repository records what was built, what was represented, what stayed open, and what could only be reserved for exact authority.

## 2. Frozen design and evidence discipline

x1 audited 220 earlier frozen proposals and added ten mechanism-level distinctions, yielding 230 effective records. Exact identifiers and titles were unique. Token overlap was used only as a screen; novelty depended on the proposed evidence object, falsifier, recovery rule, and protected gate. Six non-duplicate official or primary sources were added to 147 inherited sources, producing 153 effective entries while preserving the source status vocabulary current, stable, draft, and watch.

The x2 engine converts each proposal into one accepted bounded canonical case and seven deliberately rejected mutations. Eighty deterministic cases therefore exercise ten proposal surfaces and retain seventy synthetic negative witnesses. A mutation that later becomes understood or locally recoverable is not erased. Operational failures are separately preserved. The retained-negative register contains {negative_count} entries and begins with the inherited v643-v7 list byte-for-byte. Same-owner clean snapshots can establish repeatability of these repository mechanics; they cannot establish independent-team scientific reproduction.

The local rule engine is standard-library only. It checks explicit required fields, exact zero-row or pending-state values, and forbidden promotions. It does not infer truth from absence, convert a protocol into participant data, create cryptographic keys, decide community authority, or treat an automated static check as a complete review. Each rejected row records concrete reasons. Recovery always returns to the narrowest evidenced state and keeps the witness visible.

## 3. GMUT Mind primary focus

Proposal P02 builds a Noether-current, boundary-flux, and charge-balance tribunal. It requires a declared continuous variation, tracked Euler–Lagrange residual, computed current divergence, oriented boundary flux, explicit improvement term, and checked bulk-boundary balance. The accepted row is a formal synthetic contract only. Mutations remove those obligations or attempt to promote the formal identity to physical conservation, GMUT confirmation, or a Theory of Everything; all are rejected. This is distinct from earlier generic conservation, gauge, and well-posedness surfaces because boundary orientation and improvement-term ambiguity are first-class evidence fields.

P03 binds a declared background equation to perturbation order. A background residual must be checked, the expansion order labeled, first-order tadpole cancellation tested, operator provenance bound, gauge labels explicit, and order separation preserved. A formal expansion cannot become a cosmological prediction. No real observation rows are present. The artifact is therefore completed as a local order-consistency tool, not as a solved physical background or empirical result.

P10 is deliberately open. A GMUT background-plus-growth likelihood would require a model-specific observable map, licensed real data, joint covariance, nuisance handling, named external baselines, blind holdout, sensitivity analysis, and independent review. This phase downloaded and fitted no real data and executed no likelihood. Synthetic rows are explicitly forbidden as substitutes. The open-gap receipt is the truthful result and prevents formal machinery from being described as a force, prediction, likelihood advantage, or empirical confirmation.

## 4. THOS Body representation

P04 freezes an eligibility and screening-flow protocol. It requires a versioned eligibility rule, a bound screening denominator, complete exclusion reasons, consent before allocation, conserved flow counts, visible missing screening rows, and a proxy label. There are zero real participants and zero real arms. The represented artifact helps detect denominator drift and post-hoc eligibility changes, but it does not resolve selection bias in an actual population.

THOS remains proxy because no ethics approval, consent process, preregistered blind matched-budget arms, real participants, raters, harms returns, or independent analysis exists here. The phase makes no effectiveness, safety, superiority, causal, or deployment claim. The screening protocol is useful preparation: it exposes what would need to be frozen and what discrepancies would have to be retained in a future authorized study. It is not participant evidence and cannot authorize recruitment.

## 5. Freed ID and CBR Heart boundaries

P05 represents a proof-purpose, verifier-domain, challenge, and transaction-binding profile. It rejects a transcript whose purpose is missing, domain broadened, challenge reused, transaction digest unbound, holder relation implicit, or verification relationship unchecked. The canonical profile contains zero real keys and zero live proofs. Production completion still requires standards-conformant keys and proofs, live resolution, live status and revocation, cross-vendor interoperability, independent privacy and security review, and trust governance. The fixture cannot prove replay resistance or production cryptographic assurance.

P06 remains an exact gate. The repository may preserve neutral questions about harm, remedy, and residual risk, but it may not identify the affected community, define the harms, rank or accept remedies, set a residual-risk threshold, declare closure, interpret tikanga or law, or ratify cultural wording. Those determinations require authorized affected parties and the relevant Māori, cultural, and legal authorities. A technically coherent questionnaire is not consent, legitimacy, governance, redress, ratification, or enacted law.

This distinction matters because authority is not a software property. A deterministic validator can ensure that required authority fields remain pending and that repository-authored conclusions are rejected. It cannot supply the people, mandates, relationships, accountability, language authority, or legal competence that the decision requires. The exact-gate outcome is therefore evidence of correct refusal, not evidence that the underlying issue has been resolved.

## 6. Provenance, security, accessibility, and thermo-psyche

P01 controls significant digits and uncertainty rounding. It preserves interval endpoints, coverage information, covariance labels, and a frozen rounding mode, rejecting narrowed intervals and unsupported precision. With zero real measurement rows, it is a reporting contract rather than measurement validation. P07 scans the static report for active elements, event handlers, unsafe URL schemes, and remote embeds while keeping the current W3C CSP status visibly draft. The host remains unchanged. Passing the bounded scan is not browser, product, deployment, independent-review, or exhaustive-security assurance.

P08 checks data-table structure: captions, unique header identifiers, cell-to-header resolution, consistent scope, and meaningful nonvisual linearization. It reserves manual, assistive-technology, and affected-user evaluation. Automated structure cannot establish complete accessibility or screen-reader equivalence. The HTML report is deliberately static, uses semantic headings and tables, and contains no script or remote embed, but qualified human evaluation remains open.

P09 separates negative thermodynamic temperature under bounded-spectrum and population-inversion prerequisites from fitted effective temperature and metaphorical psyche language. Physical units, entropy convention, equilibrium class, and temperature kind remain explicit. The classifier rejects any transfer into a psyche law or cross-pillar identity. It is a domain-separation tool, not a physical measurement, participant finding, GMUT law, or Theory of Everything.

## 7. Validation, repeatability, and retained negatives

The evidence commit is designed for two fresh detached D-drive validations at the exact same revision. Each snapshot must start and end clean, run the complete repository suite through the inherited semantic-preserving checkout adapter when required, run detailed and minimal validators, parse every phase JSON file, perform the privacy and raw-ID scan, and verify normalized manifest parity. Later closeout, seal, and final heads receive separate fresh detached checks rather than reusing evidence worktrees.

Every inherited negative is preserved first and unchanged. Five x1 operational failures remain visible: console encoding, legacy schema traversal, unavailable Sandbox query, the unadapted CRLF-sensitive suite, and an overbroad supplemental privacy regex. Seventy preregistered mutations add falsifying witnesses. Any x2 operational failure is appended rather than overwritten by recovery. A successful rerun proves only the corrected local path; it does not retroactively turn the failed command into success.

Repeatability language stays narrow. Two snapshots owned by the same phase and using the same repository, fixtures, validator logic, operating context, and infrastructure can show deterministic same-owner replay. They do not supply an independent team, independently owned protocol, separate infrastructure, or an external returned result. The independent-reproduction gate remains open even if every local hash matches.

## 8. Privacy, environment, and non-action receipts

Repository artifacts use repository-relative paths and sanitized public identifiers. Raw task or thread identifiers, private routes, transcripts, screenshots, session streams, credentials, private callable identifiers, private app state, and private local paths are excluded. Privacy scans are bounded pattern checks and are paired with staged-file review; they do not establish exhaustive privacy assurance. The source ledger links only to public official or primary materials.

Codex CLI, the installed Codex desktop package, Git, Python, Node, D-drive capacity, and Windows Sandbox availability were inspected read-only. Codex desktop was not updated. No elevation, host-security weakening, Windows-feature change, or reboot occurred. Windows Sandbox was unavailable, so the route uses ordinary fresh detached D-drive snapshots and makes no Sandbox-isolation claim. No account, API key, live identity service, production resolver, participant system, or deployment was accessed.

## 9. Closeout and terminal route

Closeout requires the complete/incomplete checklist, retained-negative register, exact/open-gate register, threat model, source ledger, environment receipts, static report, overview, evidence ledger, x1 content seal, and manifest to remain mutually consistent. The seal must be a new single-parent commit whose parent is the validated closeout. The exact final head must be a further single-parent commit, clean, pushed, four-way remote-equal, ancestral from every named anchor, and independently checked in a fresh detached snapshot.

Only after those conditions pass may exactly one sanitized activation baton be sent to the existing task titled Sable Rook for v644-v1. No task may be created, forked, delegated, or spawned, and no extra confirmation follows a successful send. Until the messaging tool acknowledges that one send, repository route truth remains PREPARED_NOT_SENT. None of the validation results changes the substantive scientific and authority boundaries above.
"""


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
        "scripts/ghc_family_v643_v8_model.py",
        "scripts/ghc_family_v643_v8_evidence.py",
        "scripts/ghc_family_v643_v8_validator.py",
        "scripts/ghc_family_v643_v8_minimal.py",
        "scripts/build_ghc_family_v643_v8_report.py",
        "tests/test_ghc_family_v643_v8.py",
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
            "schema": "ghc.family.v643-v8.proposal-contract.v1", "phase": PHASE, "owner": OWNER,
            "proposal_id": pid, "title": proposal["title"], "outcome": outcome,
            "canonical_input": canonical, "accepted": accepted, "reasons": reasons, "details": details,
            "required_fields": RULES[pid]["required"], "exact_fields": RULES[pid]["exact"],
            "forbidden_promotions": RULES[pid]["forbidden"], "external_claims_established": [], "boundary": BOUNDARY,
        })
        write_json(vector_path, {
            "schema": "ghc.family.v643-v8.mutation-vectors.v1", "phase": PHASE, "owner": OWNER,
            "proposal_id": pid, "case_count": len(cases), "accepted_count": sum(row["accepted"] for row in cases),
            "rejected_count": sum(not row["accepted"] for row in cases), "all_matched_expectation": all(row["matched_expectation"] for row in cases),
            "cases": cases, "retention_rule": "Every rejected case is copied into the retained-negative register.", "boundary": BOUNDARY,
        })
        write_json(boundary_path, {
            "schema": "ghc.family.v643-v8.nonpromotion-boundary.v1", "phase": PHASE, "owner": OWNER,
            "proposal_id": pid, "outcome": outcome, "protected_gates": proposal["protected_gates"],
            "rollback_or_recovery": proposal["rollback_or_recovery"], "external_claims_established": [],
            "real_data_rows": 0, "real_participants": 0, "real_arms": 0, "real_keys_or_proofs": 0,
            "authority_substitution_permitted": False, "boundary": BOUNDARY,
        })

    write_json(phase / "x2-proposal-ledger.json", {
        "schema": "ghc.family.v643-v8.x2-proposal-ledger.v1", "phase": PHASE, "owner": OWNER,
        "x1_commit": X1_COMMIT, "proposal_count": 10, "distribution": distribution,
        "case_count": 80, "rejected_mutation_count": 70, "proposals": ledger_rows,
        "outcome_classes": list(TRUTH_LABELS), "boundary": BOUNDARY,
    })
    write_json(phase / "evidence/evidence-ledger.json", {
        "schema": "ghc.family.v643-v8.evidence-ledger.v1", "phase": PHASE, "owner": OWNER,
        "evidence_class": "bounded deterministic repository fixtures", "rows": ledger_rows,
        "proposal_count": 10, "case_count": 80, "accepted_canonical_count": 10,
        "retained_rejection_count": 70, "distribution": distribution, "external_claims_established": [], "boundary": BOUNDARY,
    })

    inherited_path = repo / "docs/eiren-kestrel/v643-v7/retained-negative-register.json"
    inherited = json.loads(inherited_path.read_text(encoding="utf-8"))
    negatives = copy.deepcopy(inherited["negatives"])
    x1_audit = json.loads((phase / "validation/x1-operational-negatives.json").read_text(encoding="utf-8"))
    x1_negatives = [{
        "negative_id": item["negative_id"], "origin": "v643-v8-x1-operational",
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
                "negative_id": f"V6438-SYN-N{synthetic_index:03d}", "origin": "v643-v8-preregistered-synthetic",
                "proposal_id": pid, "case_id": row["case_id"], "observed": row["reasons"],
                "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False,
            })
    negatives.extend(copy.deepcopy(X2_OPERATIONAL_NEGATIVES))
    write_json(phase / "retained-negative-register.json", {
        "schema": "ghc.family.v643-v8.retained-negative-register.v1", "phase": PHASE, "owner": OWNER,
        "inherited_from": "docs/eiren-kestrel/v643-v7/retained-negative-register.json",
        "inherited_sha256_lf_normalized": normalized_sha256(inherited_path), "inherited_count": len(inherited["negatives"]),
        "x1_operational_count": len(x1_negatives), "new_synthetic_count": synthetic_index,
        "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES), "new_count": len(x1_negatives) + synthetic_index + len(X2_OPERATIONAL_NEGATIVES),
        "negative_count": len(negatives), "all_retained": True, "erasure_permitted": False,
        "negatives": negatives, "boundary": BOUNDARY,
    })
    write_json(phase / "validation/execution-negative-log.json", {
        "schema": "ghc.family.v643-v8.execution-negative-log.v1", "phase": PHASE, "owner": OWNER,
        "negative_count": len(X2_OPERATIONAL_NEGATIVES),
        "negatives": copy.deepcopy(X2_OPERATIONAL_NEGATIVES),
        "all_retained": True,
        "boundary": "Operational failures are retained as execution evidence and do not close any external gate.",
    })

    open_gaps, exact_gates = open_and_exact_gates()
    write_json(phase / "exact-open-gate-register.json", {
        "schema": "ghc.family.v643-v8.exact-open-gate-register.v1", "phase": PHASE, "owner": OWNER,
        "open_gap_count": len(open_gaps), "exact_gate_count": len(exact_gates), "open_gaps": open_gaps, "exact_gates": exact_gates,
        "all_visible": True, "none_silently_closed": True, "boundary": BOUNDARY,
    })

    threats = [
        {"id": "T01", "threat": "reported digits or rounding imply unsupported precision", "control": "bound intervals, coverage, covariance labels, frozen rounding, and nonpromotion"},
        {"id": "T02", "threat": "Noether bulk identity ignores oriented boundary flux or improvement terms", "control": "explicit current, divergence, orientation, flux, and charge-balance fields"},
        {"id": "T03", "threat": "perturbations are expanded around a non-solution or uncancelled tadpole", "control": "background residual, order labels, tadpole, provenance, and gauge checks"},
        {"id": "T04", "threat": "THOS screening exclusions or denominators drift after observation", "control": "versioned eligibility, conserved flow, reasoned exclusions, and zero-row proxy boundary"},
        {"id": "T05", "threat": "a proof transcript is rebound across purpose, domain, challenge, or transaction", "control": "explicit proof-purpose and transaction-binding profile"},
        {"id": "T06", "threat": "synthetic proof fields are called production cryptography", "control": "zero real keys and proofs plus resolution, interoperability, review, and governance gates"},
        {"id": "T07", "threat": "repository output defines community harm or accepts a remedy", "control": "neutral questions and exact affected-party, Māori, cultural, and legal authority gates"},
        {"id": "T08", "threat": "the static report contains active content or unsafe schemes", "control": "element, attribute, scheme, embed, and CSP-status audit"},
        {"id": "T09", "threat": "table cells lose header context when linearized", "control": "caption, ID, headers, scope, and linearization obligations"},
        {"id": "T10", "threat": "automated structure is called complete accessibility", "control": "manual, assistive-technology, and affected-user reservations"},
        {"id": "T11", "threat": "effective or negative temperature language becomes a psyche law", "control": "spectrum, inversion, equilibrium, entropy, units, and cross-pillar separation"},
        {"id": "T12", "threat": "synthetic likelihood scaffolding is called GMUT empirical confirmation", "control": "open real-data joint-likelihood gate with named baseline and independent review"},
        {"id": "T13", "threat": "same-owner snapshots are called independent evidence", "control": "owner, protocol, infrastructure, and return provenance"},
        {"id": "T14", "threat": "bounded privacy or security scans are called exhaustive", "control": "declared pattern and mutation scope plus independent-review boundary"},
    ]
    write_json(phase / "threat-model.json", {
        "schema": "ghc.family.v643-v8.threat-model.v1", "phase": PHASE, "owner": OWNER,
        "threat_count": len(threats), "threats": threats, "exhaustive_security": False,
        "independent_security_review": False, "resource_ceilings": {"owner_generated_files": 15000, "scope": "v643-v8 only"},
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
        "schema": "ghc.family.v643-v8.phase-truth.v1", "phase": PHASE, "owner": OWNER,
        "state": lifecycle_states[lifecycle], "source_commit": SOURCE_COMMIT, "source_seal": SOURCE_SEAL, "x1_commit": X1_COMMIT,
        "proposal_count": 10, "distribution": distribution, "case_count": 80, "synthetic_rejection_count": 70,
        "retained_negative_count": len(negatives), "open_gap_count": len(open_gaps), "exact_gate_count": len(exact_gates),
        "primary_focus": "GMUT Mind", "all_three_pillars_preserved": True,
        "same_owner_repeatability": verified, "independent_team_reproduction": False,
        "protected_claims": protected_claims, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT", "outbound_message_count": 0, "successor_task_count": 0, "subagent_count": 0,
        "boundary": BOUNDARY,
    })
    write_json(phase / "complete-incomplete-checklist.json", {
        "schema": "ghc.family.v643-v8.complete-incomplete-checklist.v1", "phase": PHASE, "owner": OWNER,
        "complete": [
            "exact Eiren v643-v7 source, seal ancestry, clean state, and fresh live-remote equality verified",
            "existing clean Ilyra lane advanced by fast-forward only",
            "dedicated x1 freeze pushed, clean, and four-way equal before x2",
            "ten semantically distinct proposals executed only within frozen approval classes",
            "eighty deterministic fixtures with seventy retained rejecting mutations",
            "all inherited and new negatives retained without erasure",
            "GMUT Mind, THOS Body, and Freed ID/CBR Heart preserved",
            "current official or primary source constraints and status classes recorded",
        ],
        "incomplete": [
            "GMUT model-specific physical derivation, real-data joint likelihood, prediction, force, or empirical confirmation",
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
        "schema": "ghc.family.v643-v8.x2-execution-receipt.v1", "phase": PHASE, "owner": OWNER,
        "x1_commit": X1_COMMIT, "x1_remote_equal_before_x2": True,
        "real_data_downloaded": False, "real_participants_or_raters": 0, "real_arms": 0,
        "real_keys_or_proofs": 0, "live_services_or_deployments": 0, "accounts_or_api_keys_changed": 0,
        "desktop_updated": False, "elevation_used": False, "host_security_changed": False,
        "windows_feature_changed": False, "rebooted": False, "boundary": BOUNDARY,
    })
    write_json(phase / "reproduction/independent-team-gap.json", {
        "schema": "ghc.family.v643-v8.independent-team-gap.v1", "phase": PHASE, "owner": OWNER,
        "same_owner_evidence_snapshots_verified": verified, "shared_repository_protocol_and_infrastructure": True,
        "different_architecture_return_received": False, "independent_team_protocol_owned": False,
        "independent_team_return_received": False, "independent_team_reproduction_established": False, "boundary": BOUNDARY,
    })
    write_json(phase / "reproduction/evidence-snapshot-plan.json", {
        "schema": "ghc.family.v643-v8.evidence-snapshot-plan.v1", "phase": PHASE, "owner": OWNER,
        "snapshot_count": 2, "location_class": "fresh detached D-drive worktrees", "required_same_commit": True,
        "required_clean_before_and_after": True,
        "required_checks": ["complete repository suite", "detailed validator", "minimal validator", "all JSON parsing", "privacy and raw-ID scan", "manifest parity"],
        "claim_scope": "same-owner repeatability only", "independent_team_reproduction": False, "boundary": BOUNDARY,
    })
    write_json(phase / "reproduction/x1-content-seal.json", x1_content_seal(repo, phase))
    write_json(phase / "tooling/executed-toolchain.json", {
        "schema": "ghc.family.v643-v8.executed-toolchain.v1", "phase": PHASE, "owner": OWNER,
        "tools": [
            {"name": "scripts/ghc_family_v643_v8_model.py", "role": "frozen rule and seventy-mutation model"},
            {"name": "scripts/ghc_family_v643_v8_evidence.py", "role": "eighty-case evidence and retained-negative assembler"},
            {"name": "scripts/ghc_family_v643_v8_validator.py", "role": "detailed evidence, manifest, report, privacy, and boundary validator"},
            {"name": "scripts/ghc_family_v643_v8_minimal.py", "role": "small standard-library validation floor"},
            {"name": "scripts/build_ghc_family_v643_v8_report.py", "role": "accessible static HTML report builder"},
            {"name": "tests/test_ghc_family_v643_v8.py", "role": "decision, mutation, retention, manifest, and validator regression suite"},
        ],
        "caller_compatibility_preserved": True, "inherited_tools_mutated": False,
        "mass_deletion_performed": False, "boundary": BOUNDARY,
    })
    vetoes = [
        {"domain": "GMUT Mind", "decision": "veto", "reason": "no model-specific real-data likelihood, physical prediction, force, or empirical confirmation"},
        {"domain": "THOS Body", "decision": "veto", "reason": "no preregistered blind matched-budget real arms, participants, raters, harms returns, or independent review"},
        {"domain": "Freed ID", "decision": "veto", "reason": "no real keys and proofs, live resolution and status, interoperability, reviews, or trust governance"},
        {"domain": "CBR and Māori authority", "decision": "veto", "reason": "harm, remedy, affected-party, Māori, cultural, and legal authority cannot be substituted"},
        {"domain": "reproduction", "decision": "veto", "reason": "shared owner, protocol, repository, and infrastructure; no independent return"},
        {"domain": "accessibility and security", "decision": "veto", "reason": "manual, affected-user, and independent review remain missing"},
    ]
    write_json(phase / "stage20/domain-veto-evidence-board.json", {
        "schema": "ghc.family.v643-v8.stage20-board.v1", "phase": PHASE, "owner": OWNER,
        "vetoes": vetoes, "compensation_across_domains_allowed": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY,
    })
    write_text(phase / "deliverables/v643-v8-final-integrated-overview.md", overview_text(distribution, len(negatives)))

    manifest_rows = []
    for relative in manifest_candidates(repo, phase):
        target = repo / relative
        data = normalized_bytes(target)
        manifest_rows.append({"repo_path": relative, "sha256_lf_normalized": hashlib.sha256(data).hexdigest(), "bytes_lf_normalized": len(data)})
    write_json(phase / "reproduction/manifest.json", {
        "schema": "ghc.family.v643-v8.manifest.v1", "phase": PHASE, "owner": OWNER,
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
