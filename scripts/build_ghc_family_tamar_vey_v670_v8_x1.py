"""Build Tamar Vey v670-v8's planning-only x1 freeze.

The builder is owner-delta scoped and fail-closed. It requires Liora Venn's
exact v670-v7 final, the exact Tamar branch, and an absent x2/closeout tree. It
does not stage, commit, push, route, contact a task, or perform an external
write.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "tamar-vey" / "v670-v8"
OWNER = "Tamar Vey"
PHASE = "v670-v8"
BRANCH = "codex/GHC-Family/tamar-vey-v670-v8-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v670-v7-full-tools"
SOURCE_START = "1879ce8f6158dafd4eade2f6bc39162ef9505b75"
SOURCE_X1 = "46ee8b0dbbd90d7ba6504c40b7d197a8582bf29b"
SOURCE_EVIDENCE = "fdb3b6e0f08c44163027fc5b8b2d7dbb2205c018"
SOURCE_FINAL = "65142e05e70b507d7f15247c4154d8d6013ca046"
ACTIVATION_PATH = "docs/liora-venn/v670-v7/handoffs/tamar-vey-v670-v8-activation-candidate.md"
ACTIVATION_SHA256 = "32f0521e61ddfbece93447fc9e1d391c357be6543e6d150586b165801fa96393"
SOURCE_CANONICAL_SHA256 = "43966d9b9252032212b02e228bf7df23a53bfe490a39618a17a00527e888f56a"
SOURCE_COMPOSITE_SHA256 = "4d6099ee99549709a3df421708d6fa2d8a5d1d656286b937f831e55a937d7855"
SOURCE_COMPONENT_PAYLOAD_SHA256 = "bf8d3ffcc8a2543d130c497149bf35aeff22ac4be13c5f37f08a30e1a5101107"
SOURCE_ALL_REF_CORPUS_SHA256 = "9b0fd79630a20c98c0967af24bc954d5bcc538aea264e34276370d4719dfcd7a"
EXPECTED_ANCESTRY_CORPUS_SHA256 = "097f96a8a83b26c4f93b397b16cb41e572f3889d820014fbcc9a0d7b96ee91b4"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Tamar Vey, she/they, relational evidence-and-recovery steward, "
    "is relational working language only. It is not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, or scientific, operational, legal, cultural, affected-party, "
    "or Māori authority."
)
HOPE = "keep every claim, abstention, correction, and handoff inspectable and safely retractable"
BOUNDARY = (
    "Software, symbolic, synthetic, same-owner, citation, inherited, or composite "
    "evidence is not empirical confirmation, participant evidence, professional or "
    "scientific authority, production readiness, legal or cultural ratification, "
    "Māori authority, affected-party approval, complete privacy or accessibility "
    "assurance, exhaustive security, independent reproduction, AGI/ASI, consciousness "
    "or personhood evidence, Theory-of-Everything proof, proof/canon, or Stage 20 authority."
)

REPOSITORY_SEAL = {
    "proposal_chain": 5510,
    "effective_negatives": 33129,
    "effective_methods": 19372,
    "failed_witnesses": 4950,
    "bounded_passing_witnesses": 6411,
    "open_gaps": 253,
    "exact_gates": 248,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}
ACTIVATION_OVERLAY = {
    **REPOSITORY_SEAL,
    "effective_negatives": 33131,
    "effective_methods": 19374,
    "failed_witnesses": 4952,
    "bounded_passing_witnesses": 6413,
    "external_zero_credit_failures": 2,
    "external_bounded_passing_witnesses": 2,
    "repository_seal_rewritten": False,
}

STARTUP_FAILURES = [
    (
        "TV6708-START-N001",
        "A combined PowerShell topology wrapper failed to parse before any Git command executed.",
        "Split each ancestry predicate into one scalar native command and capture its exit code separately.",
        "Source, x1, and evidence ancestry each returned exit code zero, with three direct single-parent phase commits and zero merges.",
        "Do not embed native commands and exit-code reads inside a parenthesized PowerShell property expression.",
    ),
    (
        "TV6708-START-N002",
        "The first all-ref semantic-audit wrapper crossed its result window while the exact read-only process continued, leaving no attributable payload.",
        "Inspect the exact process before retry and replace the overbroad scan with the sealed all-ref source audit plus a bounded exact-source-ancestry delta.",
        "The source seal retained the all-ref v670-v6 audit, and the bounded ancestry audit through v670-v7 recovered 1,295 titles with zero malformed blobs.",
        "Use the smallest proposal corpus that preserves the sealed prior audit and exact new-source delta.",
    ),
    (
        "TV6708-START-N003",
        "A PowerShell attempt to pipe a JSON value and Python program through the same pipeline failed to parse before Python started.",
        "Pass the JSON through an environment variable and the program through standard input as separate channels.",
        "The bounded recovery decoded the exact title collection and emitted attributable semantic scalars.",
        "Keep data and executable text on separate PowerShell transport surfaces.",
    ),
    (
        "TV6708-X1-N001",
        "The first typewriter-domain slate produced eighteen title collisions at or above the 0.72 threshold.",
        "Project only rejected title-neighbor pairs and rewrite the exact colliding obligations before reevaluation.",
        "A rewritten typewriter slate reached zero threshold collisions, but received no freeze or completion credit.",
        "Require zero threshold collisions before considering the stronger practice-level novelty test.",
    ),
    (
        "TV6708-X1-N002",
        "The collision-free typewriter rewrite still duplicated a well-represented inherited practice domain and was rejected before artifact freeze.",
        "Query practice-level terms across the recovered corpus and choose a zero-hit domain before drafting the final slate.",
        "Mechanical calculator had zero exact practice-term hits and the final forty titles remained below the 0.72 threshold.",
        "Token distance is necessary but not sufficient; also reject a slate whose human-practice lens is already materially represented.",
    ),
    (
        "TV6708-START-N004",
        "The first schema-aware cat-file replay wrote all requests before reading output and returned no receipt while its process pair remained blocked.",
        "Stop only the exact owner-started blocked process pair and use one communicate call that drains input and output together.",
        "The recovery replayed 20 x1, 196 evidence, 25 final-delta, and 247 final-owner Git blobs with zero mismatches under their actual schemas.",
        "Use communicate for bounded batch Git plumbing; never manually fill both pipes sequentially.",
    ),
    (
        "TV6708-START-N005",
        "A second overbroad all-ref audit outlived its result handle and left one Python and one Git process without attributable output.",
        "Verify the exact process tree, stop only those owner-started processes, and use the exact source ancestry as the delta audit domain.",
        "The bounded ancestry audit completed in one attributable call with 1,045 unique proposal blobs, zero malformed blobs, and zero candidate collisions.",
        "Do not repeat a known overbroad all-ref procedure after its sealed predecessor already covers prior refs.",
    ),
    (
        "TV6708-START-N006",
        "A compound branch-collision PowerShell expression failed to parse before any branch query ran.",
        "Run local and remote ref predicates sequentially and retain each exit code.",
        "Both exact branch predicates returned absent before worktree creation.",
        "Never place a native command and LASTEXITCODE expression inside one Boolean cast.",
    ),
    (
        "TV6708-START-N007",
        "A combined branch, path, sparse, and registry projection exceeded its output window without an attributable receipt.",
        "Partition the probe into exact branch refs, exact path registration, and sparse-list scalars.",
        "The partitioned recovery proved absent local and remote refs, absent path and registration, and captured the source sparse patterns.",
        "Split registry and sparse operations from ref collision checks.",
    ),
    (
        "TV6708-START-N008",
        "The first new-lane postflight embedded merge-base and LASTEXITCODE inside a property expression and failed to parse.",
        "Run merge-base separately, store its exit code, and only then build the receipt object.",
        "The new lane was clean at the exact source, with source ancestry exit zero and 240 materialized files.",
        "Keep native process attribution outside PowerShell object construction.",
    ),
    (
        "TV6708-START-N009",
        "The first activation-candidate Git-blob hash wrapper completed beyond its result window without an attributable payload.",
        "Resolve the exact blob object first and hash that bounded blob in a fresh call with an explicit result envelope.",
        "The exact 2,245-byte activation candidate hashed to the preregistered SHA-256 and contained 278 words.",
        "Hash exact Git blobs through a bounded object-id-first procedure.",
    ),
    (
        "TV6708-START-N010",
        "A source-range projection assumed Select-String returned one object and attempted subtraction on an object array.",
        "Select the first exact function-anchor match before reading its scalar line number.",
        "The bounded recovery projected the exact approval and blocked ranges without ambiguity.",
        "Normalize command output cardinality before scalar arithmetic.",
    ),
    (
        "TV6708-X1-N003",
        "The first monolithic x1 patch expected pre-rewrite template lines and failed verification without changing a byte.",
        "Read the exact current file surface and apply smaller section-anchored patches.",
        "The source constants, failures, proposal slate, portfolio, and boundary sections were updated through verified exact anchors.",
        "Patch against the current post-mechanical text and keep substantive edits section-bounded.",
    ),
    (
        "TV6708-X1-N004",
        "The first x1 materialization assumed Liora's final proposal ledger used an outcome key and stopped on KeyError before writing the packet.",
        "Inspect the exact source row keys and adapt only the inherited outcome projection to observed_outcome.",
        "The source ledger exposes proposal_id, title, expected_outcome, observed_outcome, positive control, and rejecting mutations.",
        "Inspect source-ledger row schemas before projecting inherited lifecycle fields.",
    ),
    (
        "TV6708-X1-N005",
        "Mechanical template preparation placed untracked future x2, final, and tool copies in Tamar's working tree before the x1 freeze, although none was staged or executed.",
        "Delete only those new untracked Tamar template copies, preserve the x1 builder and test, and rebuild the planning artifacts.",
        "The corrected pre-stage tree contains Tamar x1 planning files only, with no owner x2, final, validator, final test, or substantive tool implementation.",
        "Do not copy future lifecycle implementation templates until x1 is committed, pushed, clean, and fresh-live equal.",
    ),
]

NEW_TITLES = [
    "synthetic mechanical-calculator asset namespace frame keyboard carriage and component-identity vacancy register",
    "stepped-drum shaft selector gear register and crank topology consistency contract",
    "pinwheel tooth-setting rotor carriage and accumulator observation-vacancy ledger",
    "adding four-function direct-multiplication and automatic-machine class-uncertainty firewall",
    "numeral-key clearing-key decimal-marker counter and register-label transcription provenance board",
    "unopened calculator-case custody intake with reversible accession and examination holds",
    "reported jam slip and miscarry symptom separation from observation and diagnosis claims",
    "input-register result-register revolution-counter and decimal-alignment vacancy matrix",
    "crank-turn carriage-shift place-value and operation-sequence trace contract",
    "carry propagation borrow and repeated-addition analogy with arithmetic-proof nonconversion",
    "digit-wheel alignment register-zeroing and functional-test evidence-vacancy board",
    "selector-setting command versus observed mechanism-state distinction ledger",
    "clear add subtract multiply and divide response-test vacancy protocol",
    "motor mains stored-energy and energization abstention gate for calculator intake",
    "collection-housing environment snapshot with humidity temperature duration and calibration vacancies",
    "steel brass aluminium rubber and plastic material-source authenticity-and-fitness refusal matrix",
    "calculator image scan and media-pointer absence with rights and consent holds",
    "pseudonymous calculator-work role and capability record without credential or competence claims",
    "calculator free-text quarantine for addresses credentials private routes and raw identifiers",
    "two-source calculator docket reconciliation with unresolved disagreement quarantine",
    "crank pinch electrical sharp-edge and heavy-object signal taxonomy without safety release",
    "interruptible calculator documentation work-unit envelope with stop resume and rollback state",
    "keyboard-to-mechanism-to-accumulator kinematic graph with causal and accuracy refusal",
    "accessible calculator status surface with structure focus order text alternatives and supersession",
    "instruction-legend localization provenance with stale-translation and language-authority refusal",
    "operation-sequence change-control nonce and dual acknowledgement without a real operator",
    "work-in-progress cap pause token and fatigue-signal record without human-state inference",
    "append-only calculator service-and-calculation conjecture graph with correction lineage",
    "THOS calculator-service queue proxy with workload challenge and shift-handover controls",
    "THOS arithmetic-demonstration state-board proxy with zero participants and zero effectiveness credit",
    "Freed ID zero-key calculator-collection role status and revocation-vacancy profile",
    "calculator verification record isolated from accuracy condition authenticity and serviceability claims",
    "purpose-limited calculator notice contest correction and supersession contract",
    "CBR pseudonymous calculator-user privacy challenge explanation and redress representation",
    "GMUT discrete carry-state lattice analogy with field force and likelihood nonconversion",
    "GMUT coupled-gear impulse analogy with unit observation and physical-law firewall",
    "Smithsonian calculating-machine collection adapter with zero calls zero rows and provenance vacancies",
    "real authenticated calculator observations calibrated readings and blind evaluation evidence gap",
    "real conservator repairer operator and affected-user accessibility evaluation gap",
    "competent electrical release repair heritage access remedy and Māori-authority decision gate",
]

SKILLS = [
    "ghc-family-calculator-asset-identity",
    "ghc-family-calculator-stepped-drum-topology",
    "ghc-family-calculator-pinwheel-vacancy",
    "ghc-family-calculator-machine-class-firewall",
    "ghc-family-calculator-label-provenance",
    "ghc-family-calculator-custody-abstention",
    "ghc-family-calculator-symptom-diagnosis-firewall",
    "ghc-family-calculator-register-alignment-vacancy",
    "ghc-family-calculator-operation-trace",
    "ghc-family-calculator-carry-nonconversion",
    "ghc-family-calculator-digit-test-vacancy",
    "ghc-family-calculator-energization-abstention",
    "ghc-family-calculator-environment-freshness",
    "ghc-family-calculator-material-claim-firewall",
    "ghc-family-calculator-media-rights-vacancy",
    "ghc-family-calculator-role-capability-abstention",
    "ghc-family-calculator-privacy-quarantine",
    "ghc-family-calculator-docket-reconciliation",
    "ghc-family-calculator-accessible-status",
    "ghc-family-calculator-correction-handover",
]

RUNNERS = [
    "ghc_family_calculator_asset_identity.py",
    "ghc_family_calculator_stepped_drum_topology.py",
    "ghc_family_calculator_pinwheel_vacancy.py",
    "ghc_family_calculator_operation_trace.py",
    "ghc_family_calculator_carry_nonconversion.py",
    "ghc_family_calculator_energization_abstention.py",
    "ghc_family_calculator_privacy_quarantine.py",
    "ghc_family_calculator_accessible_status.py",
    "ghc_family_calculator_correction_readback.py",
    "ghc_family_calculator_workload_handover.py",
]

EXACT = [
    "real mechanical calculator component collection record service record or operator mutation",
    "real safety diagnosis repair treatment acceptance or return-to-service decision",
    "real dimension force electrical environmental performance or calibration measurement",
    "real conservator repairer operator curator participant practitioner or affected-user study",
    "real collection location access schedule account or personal-data processing",
    "real identity key proof credential issuance presentation status or revocation",
    "real heritage intervention demonstration access or collection-use decision",
    "real accessibility remedy service allocation complaint or appeal decision",
    "legal interpretation ownership liability privacy right remedy or public authority",
    "taonga tikanga mātauranga place-name data-governance or Māori-authority decision",
    "cultural ratification community mandate or affected-party acceptance",
    "production deployment external API write live feed publication or cloud mutation",
    "host elevation security weakening feature enablement Sandbox Hyper-V or reboot",
    "destructive cleanup history rewrite force push merge or sibling-lane mutation",
    "privacy-complete exhaustive-security or production-security certification",
    "complete accessibility-conformance or affected-user acceptance declaration",
    "independent-reproduction external-audit or professional-validation declaration",
    "empirical GMUT datum likelihood posterior parameter force or prediction claim",
    "AGI ASI consciousness personhood Theory-of-Everything proof or canon claim",
    "Stage 20 admission or protected-gate closure",
]

BLOCKED = [
    "raw task or thread identifiers private routes transcripts screenshots or session streams in artifacts",
    "sibling branch reset merge rewrite deletion reuse or force push",
    "successful canonical replay or failed-canonical success laundering",
    "synthetic fixture promotion into empirical professional legal or cultural evidence",
    "unapproved account secret payment deployment plugin install or third-party write",
    "real conservator repairer operator identity location access or service data ingestion",
    "real safety legal cultural Māori-authority affected-party or public-authority substitution",
    "unsafe elevation host-security weakening feature enablement or reboot",
    "unbounded full-repository unchanged-history or cross-lane scan",
    "Stage 20 proof canon personhood AGI ASI or Theory-of-Everything promotion",
]



def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(title: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9āēīōū]+", title.lower()) if len(token) > 2 and token not in {"and", "the", "with", "for", "from"}}


def json_blob(commit: str, path: str) -> Any:
    return json.loads(git("show", f"{commit}:{path}").stdout.decode("utf-8"))


def proposal_path_at_or_before_source(path: str) -> bool:
    match = re.search(r"(?:^|/)v(\d+)-v(\d+)(?:/|$)", path)
    return bool(match and (int(match.group(1)), int(match.group(2))) <= (670, 6))


def recover_proposal_corpus() -> tuple[dict[str, Any], list[str]]:
    object_rows = git_text("rev-list", "--objects", "--all").splitlines()
    candidates: dict[str, str] = {}
    for row in object_rows:
        parts = row.split(" ", 1)
        if len(parts) != 2:
            continue
        oid, path = parts
        lowered = path.lower()
        if lowered.endswith(".json") and "proposal" in lowered and proposal_path_at_or_before_source(path):
            candidates.setdefault(oid, path)
    proposal_ids: set[str] = set()
    titles: set[str] = set()
    occurrences = 0
    malformed = 0

    def walk(node: Any) -> None:
        nonlocal occurrences
        if isinstance(node, dict):
            proposal_id, title = node.get("proposal_id"), node.get("title")
            if isinstance(proposal_id, str) and isinstance(title, str) and proposal_id.strip() and title.strip():
                occurrences += 1
                proposal_ids.add(proposal_id.strip())
                titles.add(title.strip())
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    oids = sorted(candidates)
    for start in range(0, len(oids), 128):
        chunk = oids[start:start + 128]
        for oid, blob in zip(chunk, batch_blobs(chunk), strict=True):
            if blob is None:
                malformed += 1
                continue
            try:
                walk(json.loads(blob.decode("utf-8")))
            except (UnicodeDecodeError, json.JSONDecodeError):
                malformed += 1
    canonical = json.dumps(
        {"proposal_ids": sorted(proposal_ids), "titles": sorted(titles)},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    summary = {
        "scope": "all reachable local and remote refs, proposal-named JSON paths at or before v670-v6",
        "candidate_unique_git_blobs": len(oids),
        "malformed_or_missing_blobs": malformed,
        "semantic_occurrences": occurrences,
        "unique_proposal_ids": len(proposal_ids),
        "unique_titles": len(titles),
        "corpus_sha256": hashlib.sha256(canonical).hexdigest(),
        "declared_source_chain": 5470,
        "id_superset_covers_declared_chain": len(proposal_ids) >= 5470,
        "exact_canonical_row_mapping": False,
        "canonical_row_mapping_open_gap": True,
        "reason": "Reachable refs contain duplicate and variant proposal objects; recovered IDs exceed the seal while distinct titles do not define one exact canonical 5,470-row sequence.",
    }
    return summary, sorted(titles)


def batch_blobs(specs: list[str]) -> list[bytes | None]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"], cwd=ROOT,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    output, stderr = process.communicate(
        input=("\n".join(specs) + "\n").encode("utf-8"), timeout=30
    )
    if process.returncode != 0:
        raise SystemExit(f"git cat-file --batch failed: {stderr.decode('utf-8', errors='replace')}")
    stream = io.BytesIO(output)
    rows: list[bytes | None] = []
    for _ in specs:
        header = stream.readline().decode("utf-8", errors="strict").strip()
        if header.endswith(" missing"):
            rows.append(None)
            continue
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise SystemExit(f"unexpected git cat-file header: {header}")
        size = int(parts[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise SystemExit("git cat-file blob was not newline delimited")
        rows.append(data)
    if stream.read():
        raise SystemExit("git cat-file emitted undeclared trailing bytes")
    return rows


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(NEW_TITLES, start=1):
        outcome = "completed" if index <= 28 else "represented" if index <= 36 else "open_gap" if index <= 38 else "exact_gate"
        rows.append({
            "proposal_id": f"TV6708-N{index:03d}", "title": title,
            "hypothesis": f"A typed owner-local contract can expose proposal {index:02d}'s obligations without promoting its evidence class.",
            "null_or_failure_condition": "A missing field, accepted invalid mutation, real-world action, undeclared uncertainty or authority promotion rejects the hypothesis.",
            "approval_class": "safe_now" if outcome == "completed" else "bounded_candidate" if outcome == "represented" else outcome,
            "execution_lane": "owner_local_symbolic_or_synthetic_x2" if outcome in {"completed", "represented"} else "held_without_real_world_execution",
            "official_or_primary_source_needs": "Vocabulary and refusal boundaries only; citations are not observations, measurements, advice, validation, or authority.",
            "concrete_artifacts": ["typed JSON contract", "bounded accepting fixture", "four rejecting mutation receipts", "boundary card"],
            "falsifier_or_acceptance_gate": "The bounded fixture must pass, four preregistered invalid mutations must reject, and every protected boundary must remain explicit.",
            "rollback_or_recovery": "Retain the failed witness, correct only the isolated owner-local dependency, and never replay a successful canonical aggregate.",
            "protected_gates": ["empirical", "professional", "legal", "cultural", "Māori_authority", "independent_reproduction", "Stage_20"],
            "expected_disposition": outcome, "planned_outcome": outcome,
            "primary_pillar": "GMUT Mind", "real_people": 0, "real_records_or_objects": 0,
            "external_actions": 0, "x1_state": "frozen_not_executed",
        })
    return rows


def tasks(prefix: str, domains: list[str], controls: list[str], state: str) -> list[dict[str, Any]]:
    return [{"task_id": f"TV6708-{prefix}-{i:03d}", "title": f"{domain}: {control}", "owner": OWNER, "phase": PHASE, "x1_state": state, "external_actions": 0}
            for i, (domain, control) in enumerate(((d, c) for d in domains for c in controls), start=1)]


def named(prefix: str, values: list[str], state: str) -> list[dict[str, Any]]:
    return [{"task_id": f"TV6708-{prefix}-{i:03d}", "title": value, "owner": OWNER, "phase": PHASE, "x1_state": state, "external_actions": 0}
            for i, value in enumerate(values, start=1)]


def portfolio() -> dict[str, list[dict[str, Any]]]:
    domains = ["calculator asset identity", "stepped-drum and pinwheel topology", "mechanism-state vacancy", "register and alignment vacancy", "environment freshness", "operation-trace lineage", "diagnosis and treatment abstention", "docket privacy", "accessible calculator status", "workload handover"]
    safe = tasks("SAFE", domains, ["schema", "positive fixture", "negative fixture", "rollback", "manifest", "boundary"], "planned_for_x2")
    candidates = tasks("CAND", domains, ["mutation quarantine", "timeout and encoding quarantine", "ordering and authority quarantine"], "planned_for_x2")
    cfr = tasks("CFR", ["JSON order", "UTF-8 Māori text", "source status", "failure retention", "manifest closure", "privacy disposition", "accessibility structure", "route uniqueness", "sparse budget", "boundary vocabulary"], ["clean", "fix", "refine", "recheck", "document", "preserve"], "planned_for_x2")
    successor_skills = [f"ghc-family-successor-{i:02d}-review" for i in range(1, 11)]
    successor_runners = [f"ghc_family_successor_{i:02d}_review.py" for i in range(1, 11)]
    successor_cfr = tasks("NEXT-CFR", ["successor source", "successor manifests", "successor privacy", "successor route", "successor authority"], ["schema", "mutation", "rollback", "review", "receipt", "hold"], "recommendation_only")
    return {"safe_now": safe, "candidates": candidates, "exact_approval": named("EXACT", EXACT, "held_unexecuted"), "blocked": named("BLOCK", BLOCKED, "held_unexecuted"), "skills": named("SKILL", SKILLS, "planned_for_x2"), "runners": named("RUNNER", RUNNERS, "planned_for_x2"), "clean_fix_refine": cfr, "successor_skills": named("NEXT-SKILL", successor_skills, "recommendation_only"), "successor_runners": named("NEXT-RUNNER", successor_runners, "recommendation_only"), "successor_clean_fix_refine": successor_cfr}

def method_flow() -> dict[str, Any]:
    methods, witnesses, events, recommendations = [], [], [], []
    for index, (negative_id, failed, recovery, passed, guard) in enumerate(STARTUP_FAILURES, start=1):
        method_id = f"TV6708-M{index:03d}"
        fail_id, pass_id = f"TV6708-W{index:03d}-F", f"TV6708-W{index:03d}-P"
        methods.append({
            "method_id": method_id, "title": f"bounded recovery for {negative_id}", "failure_signature": failed,
            "trigger_preconditions": ["the exact bounded failure signature is observed"], "privacy_class": "sanitized_public",
            "approval_class": "safe_now", "candidate_workaround": recovery, "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": guard, "rollback": "Retain the failure, stop the affected wrapper, and change only the isolated owner-local procedure.",
            "recommendation_state": "preferred", "supersedes": [], "protected_gates": ["no_failure_laundering", "owner_delta_only", "no_authority_promotion"],
            "retained_negative_ids": [negative_id], "scope_boundary": "Bounded same-owner workflow evidence only.",
        })
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "procedure": failed, "scope": "startup or owner-local x1 construction", "expected": "attributable bounded evidence", "observed": failed, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
            {"witness_id": pass_id, "method_id": method_id, "procedure": recovery, "scope": "isolated startup or owner-local construction recovery", "expected": "bounded attributable recovery within the owner lane", "observed": passed, "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
        ])
        events.extend([
            {"event_index": len(events) + 1, "method_id": method_id, "before": None, "after": "candidate", "reason": "failure retained and bounded recovery proposed", "witness_id": fail_id},
            {"event_index": len(events) + 2, "method_id": method_id, "before": "candidate", "after": "validated", "reason": "isolated bounded recovery passed", "witness_id": pass_id},
            {"event_index": len(events) + 3, "method_id": method_id, "before": "validated", "after": "preferred", "reason": "recurrence guard retained for the exact trigger", "witness_id": pass_id},
        ])
        recommendations.append({"method_id": method_id, "state": "preferred", "recommendation": guard})
    return {"schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "owner": OWNER, "identity_boundary": IDENTITY_BOUNDARY, "execution_authority": "owner_self_scoped_delta", "methods": methods, "witnesses": witnesses, "state_events": events, "recommendations": recommendations, "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": len(events), "recommendations": len(recommendations), "states": {"candidate": 0, "deprecated": 0, "observed": 0, "preferred": len(methods), "superseded": 0, "validated": 0}, "witness_results": {"fail": len(methods), "pass": len(methods)}}, "boundary": BOUNDARY}


def verify_manifest(path: str, commit: str) -> tuple[int, int, set[str]]:
    manifest = json.loads(git("show", f"{SOURCE_FINAL}:{path}").stdout.decode("utf-8"))
    mismatches, digests = 0, set()
    blobs = batch_blobs([f"{commit}:{entry['path']}" for entry in manifest["entries"]])
    for entry, blob in zip(manifest["entries"], blobs, strict=True):
        digest = hashlib.sha256(blob).hexdigest() if blob is not None else None
        digests.add(entry["sha256"])
        if digest != entry["sha256"] or blob is None or len(blob) != entry["bytes"]:
            mismatches += 1
    return len(manifest["entries"]), mismatches, digests


def verify_source() -> dict[str, Any]:
    local = git_text("rev-parse", f"refs/heads/{SOURCE_BRANCH}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}")
    live_tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}").split()
    live = live_tokens[0] if live_tokens else None
    parents = {"x1_parent": git_text("rev-parse", f"{SOURCE_X1}^"), "evidence_parent": git_text("rev-parse", f"{SOURCE_EVIDENCE}^"), "final_parent": git_text("rev-parse", f"{SOURCE_FINAL}^")}
    exact_parent_chain = parents == {"x1_parent": SOURCE_START, "evidence_parent": SOURCE_X1, "final_parent": SOURCE_EVIDENCE}
    manifest_specs = [
        ("docs/liora-venn/v670-v7/validation/x1-manifest.json", SOURCE_X1),
        ("docs/liora-venn/v670-v7/validation/evidence-manifest.json", SOURCE_EVIDENCE),
        ("docs/liora-venn/v670-v7/validation/final-delta-manifest.json", SOURCE_FINAL),
        ("docs/liora-venn/v670-v7/validation/final-owner-manifest.json", SOURCE_FINAL),
    ]
    manifest_rows, all_digests = [], set()
    for manifest_path, commit in manifest_specs:
        count, mismatch, digests = verify_manifest(manifest_path, commit)
        manifest_rows.append({"path": manifest_path, "commit": commit, "entries": count, "mismatches": mismatch})
        all_digests |= digests
    packet = git("show", f"{SOURCE_FINAL}:{ACTIVATION_PATH}").stdout
    packet_text = packet.decode("utf-8")
    return {
        "source_branch": SOURCE_BRANCH, "local": local, "upstream": tracking, "tracking": tracking, "fresh_live": live,
        "all_equal": local == tracking == live == SOURCE_FINAL, "parent_chain": {**parents, "exact": exact_parent_chain},
        "phase_commits": int(git_text("rev-list", "--count", f"{SOURCE_START}..{SOURCE_FINAL}")),
        "merge_commits": int(git_text("rev-list", "--merges", "--count", f"{SOURCE_START}..{SOURCE_FINAL}")),
        "manifests": manifest_rows, "commit_local_manifest_entries_replayed": sum(row["entries"] for row in manifest_rows),
        "unique_declared_blob_digests": len(all_digests), "commit_local_manifest_mismatches": sum(row["mismatches"] for row in manifest_rows),
        "activation_packet": {"path": ACTIVATION_PATH, "bytes": len(packet), "words": len(packet_text.split()), "sha256": hashlib.sha256(packet).hexdigest(), "expected_sha256": ACTIVATION_SHA256, "integrity_valid": hashlib.sha256(packet).hexdigest() == ACTIVATION_SHA256, "prepared_labels_historical": True, "live_activation_authoritative": True},
        "source_canonical_receipt": {"sha256": SOURCE_CANONICAL_SHA256, "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "canonical_invocations": 1, "canonical_successes": 0, "replays": 0, "replay_forbidden": True, "failure": "KeyError('mode') on immutable x1 entries whose exact schema omits mode", "tamar_validation_credit": 0},
        "source_dependency_corrected_composite": {"sha256": SOURCE_COMPOSITE_SHA256, "component_payload_sha256": SOURCE_COMPONENT_PAYLOAD_SHA256, "status": "VALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT", "canonical_success_credit": 0, "tamar_validation_credit": 0},
    }

def overview(inherited: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> str:
    prose = [
        "# Tamar Vey v670-v8 x1 integrated planning overview", "", "## Lifecycle and evidence basis", "",
        "This packet is a planning-only x1 freeze. It contains no x2 implementation, executed proposal, completed portfolio claim, successor delivery, empirical result, production action, or authority act. Tamar's fresh additive sparse lane begins at Liora Venn's exact v670-v7 final. The activation Git blob, direct source-parent chain, three single-parent source commits, zero merges, four commit-local manifests, clean source state, typed zero divergence, and fresh local, upstream, tracking, and live-remote equality were verified before generation. Liora's sole canonical aggregate failed on an incorrect mode assumption and retains zero success credit. Her separately named dependency-corrected component composite is inherited source evidence only and gives Tamar no validation or completion credit.",
        "", "## Identity, hope, and corrigibility", "",
        IDENTITY_BOUNDARY,
        "",
        f"Tamar's relational hope is to {HOPE}. The role and hope are working vocabulary, not a credential or continuity proof. Hamish may rename, pause, redirect, or stop the route. Corrigibility means a contradiction, failed witness, unavailable evidence, ambiguous route, authority vacancy, or falsifier stops promotion. A recovery preserves the failed witness and changes only the narrow owner-local dependency that was actually shown to be wrong.",
        "", "## Primary pillar and bounded practice lenses", "",
        "The primary pillar is GMUT Mind. The first bounded practice lens is a wholly synthetic mechanical-calculator collection and service-intake packet covering asset identity, stepped-drum and pinwheel topology, reported symptoms, abstention, custody, correction, and handover. The second is a wholly synthetic arithmetic-trace packet covering input and result registers, crank and carriage sequences, carry-state analogies, provenance, observation vacancy, and accuracy refusal. The third is a wholly synthetic accessible status, privacy, workload, correction-readback, and shift-handover packet. None uses a real calculator, component, collection record, calculation result, operator, repairer, conservator, curator, visitor, measurement, service, treatment, identity event, or authority case.",
        "", "## Trinity Mandala protection", "",
        "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Carry-state lattices, coupled-gear impulse analogies, unit obligations, and zero-row adapters are software obligations only. They establish no real datum, likelihood, posterior, parameter constraint, force, prediction, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. THOS Body remains explicit through synthetic queue, correction-readback, workload, accessibility, and handover proxies, but there are no preregistered blind matched-budget real arms, real participants or operators, safety monitoring, suitable statistics, or independent review. Freed ID and CBR Heart remain explicit through zero-key role, custody-claim, contest, notice, restriction, reason, appeal, remedy, and authority-vacancy representations, never production identity or enacted rights.",
        "", "## Professional, legal, cultural, and Māori-authority firewall", "",
        "No artifact authenticates a calculator or component, diagnoses a fault, specifies repair or treatment, accepts a repair, establishes accuracy, serviceability, return-to-service or demonstration fitness, grants access, resolves ownership or heritage rights, or demonstrates conservation, repair, electrical, metrological, accessibility, or collection competence. Legal meaning, cultural legitimacy, affected-party acceptance, remedy, taonga status, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected authorities, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Official sources supply vocabulary and refusal conditions only; a citation is not an observation, professional opinion, legal conclusion, cultural mandate, or affected-party decision.",
        "", "## Semantic novelty and recovery honesty", "",
        "The source seal declares a 5,510-row frozen proposal chain. Liora's sealed all-ref audit supplies 5,374 unique titles through v670-v6; her forty exact v670-v7 proposal titles are then added as the new-source delta. Tamar compares every new title against that 5,414-title augmented corpus under the unchanged 0.72 token-Jaccard threshold. The recovered IDs form a conservative semantic superset of the earlier declared chain, but duplicate and variant proposal objects mean there is no proved one-to-one mapping to exactly 5,510 canonical rows. Tamar therefore records both the broad semantic comparison and the exact canonical-row mapping gap. Zero collisions and a maximum score of 0.545455 support bounded distinctness; they do not establish universal semantic novelty over unavailable compressed rows.",
        "", "## Preregistration and falsification", "",
        f"Forty Tamar proposals are frozen with exactly one expected disposition each: {OUTCOMES}. Every row includes a hypothesis, null or failure condition, approval class, execution lane, official or primary-source need, concrete artifacts, falsifier or acceptance gate, rollback or recovery, and protected gates. Each proposal freezes four rejecting mutations, for 160 planned rejections. A later completed label can mean only that its bounded owner-local software and structural gate passed. Represented means a synthetic proxy exists while real evidence or authority remains absent. Open gaps require data-bearing professional, participant, or independent evidence not present here. Exact gates remain with competent, affected, legal, cultural, and Māori authorities.",
        "", "## Retained failures and Method Flow", "",
        f"{len(STARTUP_FAILURES)} Tamar startup or owner-local construction failures are retained at zero initial-pass credit. Each receives one failed Method Flow witness, one bounded recovery witness, a recurrence guard, and an append-only state progression to preferred. The activation overlay is extended additively without rewriting Liora's seal. Silent stdout is never treated as success, a guessed JSON path never becomes evidence, and an elapsed worktree wrapper is inspected before any retry. Same-owner recovery is not independent reproduction.",
        "", "## Portfolio, skills, runners, and successor seeds", "",
        "The frozen portfolio contains sixty safe-now tasks, thirty bounded candidates, twenty exact-approval packets, ten blocked packets, twenty phase-local skill ideas, ten family-compatible runner ideas, sixty additive CLEAN/FIX/REFINE tasks, ten successor skill recommendations, ten successor runner recommendations, and thirty successor CLEAN/FIX/REFINE recommendations. Inherited work and successor recommendations earn zero Tamar novelty or completion credit. Three ordinary-phase substantive tools are planned. X2 may materialize only owner-local files below the 2,000-file guard and must preserve family-current ghc_family_* and build_ghc_family_* compatibility. No global install, unrelated software install, account or credential action, host elevation, security weakening, Windows feature change, Sandbox or Hyper-V activation, reboot, destructive cleanup, sibling mutation, or full-repository scan is authorized.",
        "", "## Sources, privacy, accessibility, and security", "",
        "The Smithsonian National Museum of American History calculating-machines collection page, Smithsonian Open Access developer-tools page, NIST SP 330, W3C PROV-O, and W3C WCAG 2.2 are official or primary vocabulary sources. The source lookup was read-only, made zero API calls, downloaded no dataset, and supplied no real row. Five privacy classes protect against raw task or thread identifiers, private routes or callable details, credentials and secrets, transcripts or session streams, and private absolute paths. Scanner definitions are candidates rather than payload hits and require exact-file adjudication. Structural headings, summaries, tables, labels, and navigation do not establish complete accessibility; manual keyboard, browser, assistive-technology, cognitive, language, security-usability, and affected-user evaluation remain reserved. Bounded changed-code checks are not exhaustive security.",
        "", "## x1-before-x2 and validation hold", "",
        "X1 must remain planning-only, be staged from an exact allowlist, pass owner-scoped tests, parse every phase JSON document, validate Method Flow, adjudicate five privacy classes, pass diff hygiene, and seal a normalized-LF exact staged Git-blob manifest. It must then be committed, pushed, clean, typed zero divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 begins. The later exact-final canonical aggregate has at most one invocation and one-success budget. A success is never replayed; a failure remains zero canonical-success credit and only a narrowly justified dependency may be tested in a separately named composite.",
        "", "## Route hold", "",
        "The current live activation anticipates Tamar Vey for v670-v8, but x1 deliberately records no prospective recipient because the edge remains terminally gated. No task has been created or forked, no collaboration subagent has been spawned, no standby task has been contacted, and no successor has been contacted. Only after Tamar's clean pushed exact final and terminal validation may the newest authority and roster be refreshed, one exact title uniquely resolved and immediately reread, a duplicate guard applied, and at most one sanitized message sent if every gate permits. Ambiguity, pause, redirect, rename, missing acknowledgement, usage exhaustion, or protected-gate failure stops the route.",
        "", "## Twenty inherited selections with zero Tamar credit", "",
    ]
    prose.extend(f"- {row['source_proposal_id']}: {row['source_title']} — inherited integrity evidence only." for row in inherited)
    prose.extend(["", "## Forty frozen Tamar proposals", ""])
    prose.extend(f"- {row['proposal_id']} [{row['planned_outcome']}]: {row['title']}." for row in proposals)
    prose.extend(["", "## Terminal truth", "", BOUNDARY, "", "NOT_READY_FOR_STAGE_20."])
    return "\n".join(prose)


def build() -> None:
    head, branch = git_text("rev-parse", "HEAD"), git_text("branch", "--show-current")
    if head != SOURCE_FINAL or branch != BRANCH:
        raise SystemExit(f"x1 requires {BRANCH} at {SOURCE_FINAL}; found {branch} at {head}")
    if any((OWNER_ROOT / name).exists() for name in ("x2", "closeout", "final", "seal")):
        raise SystemExit("x1 refuses a lane containing x2 or closeout material")
    source_rows = json_blob(SOURCE_FINAL, "docs/liora-venn/v670-v7/closeout/proposal-ledger-final.json")["rows"]
    if len(source_rows) != 40:
        raise SystemExit("source proposal ledger must contain forty Liora rows")
    inherited = [
        {
            "selection_id": f"TV6708-I{i:03d}", "source_owner": "Liora Venn", "source_phase": "v670-v7",
            "source_proposal_id": row["proposal_id"], "source_title": row["title"], "source_outcome": row["observed_outcome"],
            "source_row_sha256": hashlib.sha256(json.dumps(row, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "integrity_revalidated": True, "tamar_novelty_credit": 0, "tamar_completion_credit": 0,
            "state": "inherited_evidence_only",
        }
        for i, row in enumerate(source_rows[:20], start=1)
    ]
    proposals = proposal_rows()
    if len(proposals) != 40 or len({row["title"] for row in proposals}) != 40 or Counter(row["planned_outcome"] for row in proposals) != Counter(OUTCOMES):
        raise SystemExit("proposal count, uniqueness, or distribution drifted")
    corpus_summary, source_titles = recover_proposal_corpus()
    if not corpus_summary["id_superset_covers_declared_chain"] or corpus_summary["malformed_or_missing_blobs"] or corpus_summary["corpus_sha256"] != SOURCE_ALL_REF_CORPUS_SHA256:
        raise SystemExit("proposal corpus recovery did not cover the declared chain or contained malformed blobs")
    source_titles = sorted(set(source_titles) | {row["title"] for row in source_rows})
    if len(source_titles) != 5414:
        raise SystemExit(f"augmented source title count drifted: {len(source_titles)}")
    neighbors, max_score = [], 0.0
    for row in proposals:
        left, best_title, best_score = normalize(row["title"]), None, 0.0
        for source_title in source_titles:
            right = normalize(source_title)
            score = len(left & right) / max(1, len(left | right))
            if score > best_score:
                best_title, best_score = source_title, score
        max_score = max(max_score, best_score)
        neighbors.append({"proposal_id": row["proposal_id"], "source_title": best_title, "jaccard": round(best_score, 6), "collision": best_score >= 0.72})
    if any(row["collision"] for row in neighbors):
        raise SystemExit("semantic neighbor collision requires proposal rewrite")
    frozen_portfolio = portfolio()
    counts = {key: len(value) for key, value in frozen_portfolio.items()}
    expected = {"safe_now": 60, "candidates": 30, "exact_approval": 20, "blocked": 10, "skills": 20, "runners": 10, "clean_fix_refine": 60, "successor_skills": 10, "successor_runners": 10, "successor_clean_fix_refine": 30}
    if counts != expected:
        raise SystemExit(f"portfolio count drift: {counts}")
    source = verify_source()
    if not source["all_equal"] or not source["parent_chain"]["exact"] or source["phase_commits"] != 3 or source["merge_commits"] != 0 or source["commit_local_manifest_mismatches"] != 0 or not source["activation_packet"]["integrity_valid"]:
        raise SystemExit("immutable source verification failed")
    x1_overlay = {
        **ACTIVATION_OVERLAY,
        "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + len(STARTUP_FAILURES),
        "effective_methods": ACTIVATION_OVERLAY["effective_methods"] + len(STARTUP_FAILURES),
        "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + len(STARTUP_FAILURES),
        "bounded_passing_witnesses": ACTIVATION_OVERLAY["bounded_passing_witnesses"] + len(STARTUP_FAILURES),
        "tamar_startup_failures": len(STARTUP_FAILURES),
        "repository_seal_rewritten": False,
    }
    write_json("x1/activation-intake.json", {"schema": "ghc.family.activation-intake.v5", "owner": OWNER, "phase": PHASE, "source_verification": source, "task_creation_count": 0, "fork_count": 0, "subagent_count": 0, "standby_contact_count": 0})
    write_json("x1/identity-and-boundary.json", {"schema": "ghc.family.identity-boundary.v4", "owner": OWNER, "phase": PHASE, "pronouns": "she/they", "relational_role": "relational evidence-and-recovery steward", "relational_hope": HOPE, "identity_boundary": IDENTITY_BOUNDARY, "corrigibility": "Hamish may rename, pause, redirect, or stop the route."})
    write_json("x1/source-count-overlay.json", {"schema": "ghc.family.source-count-overlay.v5", "repository_sealed": REPOSITORY_SEAL, "live_activation_overlay": ACTIVATION_OVERLAY, "tamar_x1_overlay": x1_overlay})
    write_json("x1/inherited-proposal-revalidation.json", {"schema": "ghc.family.inherited-proposal-revalidation.v5", "owner": OWNER, "phase": PHASE, "selected": 20, "novelty_credit": 0, "completion_credit": 0, "rows": inherited})
    write_json("x1/semantic-neighbor-audit.json", {"schema": "ghc.family.semantic-neighbor-audit.v5", "owner": OWNER, "phase": PHASE, "sealed_all_ref_corpus": corpus_summary, "source_liora_titles_added": 40, "augmented_unique_titles": len(source_titles), "source_chain": 5510, "new_titles": 40, "max_jaccard": round(max_score, 6), "collision_threshold": 0.72, "collisions": 0, "rows": neighbors, "universal_novelty_claim": False, "canonical_row_mapping_open_gap": True})
    write_json("x1/new-proposal-freeze.json", {"schema": "ghc.family.new-proposal-freeze.v5", "owner": OWNER, "phase": PHASE, "proposal_chain_before": 5510, "proposal_chain_after_if_evidence_frozen": 5550, "outcomes": OUTCOMES, "planned_invalid_mutations_per_proposal": 4, "planned_invalid_mutations": 160, "rows": proposals})
    write_json("x1/portfolio-freeze.json", {"schema": "ghc.family.remastered-portfolio-freeze.v5", "owner": OWNER, "phase": PHASE, "rows": frozen_portfolio, "counts": counts, "ordinary_phase_new_tool_target": 3, "bounded_practice_lenses": ["synthetic mechanical-calculator collection and service intake with asset and mechanism topology vacancies", "synthetic arithmetic trace carry-state and accumulator documentation with accuracy refusal", "synthetic calculator status correction accessibility workload and shift handover"], "successor_practice_recommendation": "synthetic community hand-bookbinding intake, sewing-structure vacancy, correction, accessibility, and handover; recommendation only for the terminally authorized successor", "successor_practice_recommendation_count": 1, "inherited_portfolio_completion_credit": 0, "successor_recommendation_completion_credit": 0, "filler_prohibited": True})
    write_json("x1/source-ledger.json", {"schema": "ghc.family.public-source-ledger.v5", "owner": OWNER, "phase": PHASE, "retrieved_nz_date": "2026-08-26", "sources": [
        {"title": "Calculating Machines", "publisher": "Smithsonian National Museum of American History", "url": "https://americanhistory.si.edu/collections/object-groups/calculating-machines", "status": "current_page_checked_2026-08-26", "use": "stepped-drum, pinwheel, direct-multiplication, and adding-machine vocabulary only; not object evidence"},
        {"title": "Smithsonian Open Access Developer Tools", "publisher": "Smithsonian Institution", "url": "https://www.si.edu/openaccess/devtools", "status": "current_page_checked_2026-08-26", "use": "API-key and provenance requirements for a zero-call, zero-row adapter only"},
        {"title": "The International System of Units (SI), 2019 Edition, NIST SP 330", "publisher": "National Institute of Standards and Technology", "url": "https://www.nist.gov/pml/special-publication-330", "status": "current_2019_edition_page_checked_2026-08-26", "use": "unit and dimensional vocabulary with measurement-vacancy boundaries only"},
        {"title": "PROV-O: The PROV Ontology", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/prov-o/", "status": "stable", "use": "provenance vocabulary and responsibility-vacancy boundaries only"},
        {"title": "Web Content Accessibility Guidelines 2.2", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/WCAG22/", "status": "current", "use": "structural accessibility vocabulary and manual-evaluation reservation only"},
    ], "read_only_query_attempts": 5, "failed_projection_attempts": 0, "api_calls": 0, "downloads": 0, "real_rows": 0, "external_writes": 0, "boundary": "Sources supply vocabulary and refusal conditions only; they are not observations, measurements, professional advice, validation, legal interpretation, cultural legitimacy, Māori authority, or Stage 20 evidence."})
    write_json("x1/threat-model.json", {"schema": "ghc.family.threat-model.v5", "owner": OWNER, "phase": PHASE, "assets": ["immutable source lineage", "x1-before-x2 separation", "four truth labels", "retained failures", "synthetic-only fixtures", "authority vacancies", "route uniqueness"], "risks": [
        {"risk": "source or manifest drift", "control": "exact commits, Git-blob replay, and fresh live equality"},
        {"risk": "universal novelty overclaim", "control": "all-ref proposal-title comparison plus explicit exact-canonical-row mapping gap"},
        {"risk": "calculator condition, accuracy, service, treatment, or performance-state promotion", "control": "zero-object fixtures and observation, measurement, quality, and professional firewalls"},
        {"risk": "collection, mechanism, unit, or provenance vocabulary promoted into real service or safety evidence", "control": "typed vacancy fields and likelihood refusal"},
        {"risk": "failure laundering", "control": "append-only Method Flow with failed and passing witnesses"},
        {"risk": "private route or identifier leak", "control": "five-class owner-delta candidate adjudication"},
        {"risk": "accessibility overclaim", "control": "structural-only checks with manual and affected-user evaluation reserved"},
        {"risk": "duplicate successor send", "control": "terminal live authority, exact-title reread, duplicate guard, acknowledgement, and no-resend"},
    ], "not_exhaustive_security": True})
    write_json("x1/method-flow-startup.json", method_flow())
    write_json("x1/workflow-plan.json", {"schema": "ghc.family.workflow-plan.v5", "owner": OWNER, "phase": PHASE, "steps": [{"step": "activation guidance and source verification", "state": "completed_read_only"}, {"step": "planning-only x1 freeze", "state": "in_progress_until_pushed_equal"}, {"step": "bounded x2 execution", "state": "blocked_by_x1_terminal_gate"}, {"step": "combined closeout and seal", "state": "pending"}, {"step": "one owner-scoped canonical aggregate", "state": "pending_not_invoked"}, {"step": "successor route", "state": "unresolved_until_terminal_live_authority"}], "commit_ceiling": 8, "planned_phase_commits": 3, "x1_commit_ceiling": 5, "x2_commit_ceiling": 5, "materialized_file_guard": 2000, "canonical_invocation_budget": 1, "canonical_success_budget": 1, "post_success_replay": False})
    write_json("x1/phase-truth.json", {"schema": "ghc.family.phase-truth.x1.v5", "owner": OWNER, "phase": PHASE, "primary_pillar": "GMUT Mind", "protected_pillars": ["THOS Body", "Freed ID and CBR Heart"], "proposal_rows": {"inherited_zero_credit": 20, "new": 40}, "expected_outcomes": OUTCOMES, "core_truth_labels": CORE_LABELS, "proposal_chain": {"before": 5510, "after_if_frozen": 5550}, "universal_novelty_claim": False, "canonical_row_mapping_open_gap": True, "startup_operational_failures": len(STARTUP_FAILURES), "x1_completion_credit": 0, "x2_execution_started": False, "real_world_actions": 0, "external_writes": 0, "identity_boundary": IDENTITY_BOUNDARY, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x1/route-plan.json", {"schema": "ghc.family.route-plan.v5", "owner": OWNER, "phase": PHASE, "prospective_recipient_exact_title": None, "prospective_phase": None, "delivery_state": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH", "successor_contact_count": 0, "task_creation_count": 0, "substitute_endpoint_count": 0, "standby_contact_count": 0, "required_gate": "clean pushed exact final, attributable terminal validation, newest live authority and roster, unique exact-title reread, duplicate guard, and acknowledged one-send"})
    text = overview(inherited, proposals)
    write_text("x1/integrated-overview.md", text)
    write_json("x1/build-receipt.json", {"schema": "ghc.family.x1-build-receipt.v5", "owner": OWNER, "phase": PHASE, "source_head": head, "branch": branch, "inherited_rows": 20, "new_rows": 40, "portfolio_counts": counts, "overview_words": len(text.split()), "read_only_external_queries": 5, "external_writes": 0, "x2_materialized": False})
    print(json.dumps({"owner": OWNER, "phase": PHASE, "new": 40, "outcomes": OUTCOMES, "portfolio": counts, "startup_failures": len(STARTUP_FAILURES), "overview_words": len(text.split()), "corpus": corpus_summary}, sort_keys=True))


def staged_paths() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_review() -> None:
    paths = staged_paths()
    exact = {
        "scripts/build_ghc_family_tamar_vey_v670_v8_x1.py",
        "tests/test_ghc_family_tamar_vey_v670_v8_x1.py",
        "docs/tamar-vey/v670-v8/validation/x1-method-flow-validation.json",
        "docs/tamar-vey/v670-v8/validation/x1-validation-receipt.json",
        "docs/tamar-vey/v670-v8/validation/x1-staged-privacy.json",
        "docs/tamar-vey/v670-v8/validation/x1-staged-review.json",
        "docs/tamar-vey/v670-v8/validation/x1-manifest.json",
    }
    out = [path for path in paths if not (path.startswith("docs/tamar-vey/v670-v8/x1/") or path in exact)]
    mixed = [path for path in paths if any(part in path for part in ("/x2/", "/closeout/", "/final/", "/seal/")) or path.endswith(("_x2.py", "_final.py"))]
    payload = {"schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "x1", "staged_before_self": paths, "staged_count_before_self": len(paths), "out_of_scope": out, "mixed_lifecycle": mixed, "valid": not out and not mixed}
    write_json("validation/x1-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index() -> None:
    exclusions = ["docs/tamar-vey/v670-v8/validation/x1-manifest.json", "docs/tamar-vey/v670-v8/validation/x1-staged-review.json"]
    entries = []
    for path in staged_paths():
        if path in exclusions:
            continue
        blob = git("show", f":{path}").stdout
        entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    entries.sort(key=lambda row: row["path"])
    write_json("validation/x1-manifest.json", {"schema": "ghc.family.git-blob-manifest.v5", "domain": "x1 exact staged Git blobs before two declared self files", "hash_domain": "normalized_lf_exact_git_blob", "owner": OWNER, "phase": PHASE, "source_final": SOURCE_FINAL, "entry_count": len(entries), "entries": entries, "self_exclusions": exclusions})


def validation_receipt() -> None:
    json_paths = sorted((OWNER_ROOT / "x1").rglob("*.json"))
    text_paths = sorted(path for path in (OWNER_ROOT / "x1").rglob("*") if path.is_file())
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": type(exc).__name__})
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates = []
    for path in text_paths:
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "pattern_class": label})
    python_paths = [ROOT / "scripts" / "build_ghc_family_tamar_vey_v670_v8_x1.py", ROOT / "tests" / "test_ghc_family_tamar_vey_v670_v8_x1.py"]
    compile_issues = []
    for path in python_paths:
        try:
            compile(path.read_text(encoding="utf-8"), path.name, "exec")
        except SyntaxError as exc:
            compile_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": str(exc)})
    diff = git("diff", "--cached", "--check", check=False)
    materialized_files = len([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts])
    payload = {
        "schema": "ghc.family.x1-validation-receipt.v1", "owner": OWNER, "phase": PHASE,
        "json_documents": len(json_paths), "json_issues": json_issues,
        "text_files": len(text_paths), "privacy_pattern_classes": sorted(patterns),
        "privacy_candidates": candidates, "confirmed_privacy_hits": 0 if not candidates else None,
        "python_compiles": len(python_paths), "python_compile_issues": compile_issues,
        "staged_paths_before_receipt": len(staged_paths()), "diff_hygiene_exit": diff.returncode,
        "diff_hygiene_output": diff.stdout.decode("utf-8", errors="replace"),
        "materialized_files": materialized_files, "file_guard": 2000,
        "x2_absent": not (OWNER_ROOT / "x2").exists(),
        "valid": not json_issues and not candidates and not compile_issues and diff.returncode == 0 and materialized_files < 2000 and not (OWNER_ROOT / "x2").exists(),
        "boundary": BOUNDARY,
    }
    write_json("validation/x1-validation-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_privacy() -> None:
    self_path = "docs/tamar-vey/v670-v8/validation/x1-staged-privacy.json"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates = []
    scanned = 0
    for path in staged_paths():
        if path == self_path or Path(path).suffix.lower() not in {".py", ".json", ".md", ".txt", ".html"}:
            continue
        blob = git("show", f":{path}").stdout
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append({"path": path, "pattern_class": "non_utf8_text", "disposition": "confirmed_payload_hit"})
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                scanner_surface = path in {
                    "scripts/build_ghc_family_tamar_vey_v670_v8_x1.py",
                    "tests/test_ghc_family_tamar_vey_v670_v8_x1.py",
                }
                candidates.append({"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if scanner_surface else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {"schema": "ghc.family.staged-privacy-scan.v2", "owner": OWNER, "phase": PHASE, "lifecycle": "x1", "hash_domain": "exact_staged_git_blob", "pattern_classes": sorted(patterns), "scanned_text_files": scanned, "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed), "self_exclusions": [self_path], "valid": not confirmed, "boundary": "Scanner definitions and unit-test strings are candidates, never payload hits; every other match fails closed."}
    write_json("validation/x1-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    parser.add_argument("--validation-receipt", action="store_true")
    parser.add_argument("--staged-privacy", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
    elif args.manifest_from_index:
        manifest_from_index()
    elif args.validation_receipt:
        validation_receipt()
    elif args.staged_privacy:
        staged_privacy()
    else:
        build()


if __name__ == "__main__":
    main()
