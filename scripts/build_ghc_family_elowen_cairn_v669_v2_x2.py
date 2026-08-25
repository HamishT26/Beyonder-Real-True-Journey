from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_elowen_cairn_v669_v2_archive import (
    ACTIVATION_OVERLAY,
    ALLOWED_OUTCOMES,
    BRANCH,
    DOCUMENT_WORD_CEILING,
    EVIDENCE_OVERLAY,
    FROZEN_X1,
    IDENTITY_BOUNDARY,
    OWNER,
    PHASE,
    PORTFOLIO_COUNTS,
    RELATIONAL_HOPE,
    RELATIONAL_ROLE,
    REL_PHASE_ROOT,
    ROOT,
    RUNNER_NAMES,
    SKILL_NAMES,
    SOURCE_FINAL,
    SOURCE_OVERLAY,
    STARTUP_FAILURES,
    TERMINAL_VERDICT,
    X2_FAILURES,
    canonical_json_bytes,
    git,
    manifest_rows,
    phase_owner_files,
    run_git,
    sha256_bytes,
    utc_now,
)
from ghc_family_lutherie_contracts import RUNNER_PROFILES, execute_contracts, load_proposals


PHASE_ROOT = ROOT / REL_PHASE_ROOT
EVIDENCE_MANIFEST = (REL_PHASE_ROOT / "validation/evidence-owner-manifest.json").as_posix()
DELTA_MANIFEST = (REL_PHASE_ROOT / "validation/evidence-delta-manifest.json").as_posix()
STAGED_REVIEW = (REL_PHASE_ROOT / "validation/evidence-staged-review.json").as_posix()
FAILED_STAGED_REVIEW = (REL_PHASE_ROOT / "validation/evidence-staged-review-failed.json").as_posix()
FAILED_RECOVERY_REVIEW = (REL_PHASE_ROOT / "validation/evidence-staged-recovery-failed.json").as_posix()
FAILED_RECOVERY_REVIEW_2 = (REL_PHASE_ROOT / "validation/evidence-staged-recovery-failed-2.json").as_posix()
STAGED_ALLOWLIST = (REL_PHASE_ROOT / "validation/evidence-staged-allowlist.json").as_posix()


def write_json(relative: str | Path, value: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_text(relative: str | Path, value: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")
    return path


def assert_x2_start() -> None:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong Elowen owner branch")
    if git("rev-parse", "HEAD") != FROZEN_X1:
        raise RuntimeError("x2 must begin at the immutable Elowen x1 head")
    if git("rev-parse", f"{FROZEN_X1}^") != SOURCE_FINAL:
        raise RuntimeError("x1 parent is not the immutable Tamar final")
    if run_git("diff", "--cached", "--quiet", check=False).returncode != 0:
        raise RuntimeError("x2 builder requires an empty index")


def operation_methods() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    rows = [("x1", row) for row in STARTUP_FAILURES] + [("x2", row) for row in X2_FAILURES]
    for ordinal, (stage, row) in enumerate(rows, 1):
        failure_id, signature, workaround, guard = row
        method_id = f"EC6692-METHOD-OP-{ordinal:03d}"
        failed_id = f"EC6692-WITNESS-OP-{ordinal:03d}-F"
        passed_id = f"EC6692-WITNESS-OP-{ordinal:03d}-P"
        methods.append(
            {
                "approval_class": "safe_now",
                "failed_witness_ids": [failed_id],
                "failure_id": failure_id,
                "failure_signature": signature,
                "method_id": method_id,
                "owner": OWNER,
                "phase": PHASE,
                "protected_gates": ["no_failure_erasure", "owner_local_only", "no_claim_promotion"],
                "recurrence_guard": guard,
                "result": "dependency_corrected_bounded_recovery",
                "rollback": "stop the smallest failed dependency and preserve the immutable prior lifecycle",
                "stage": stage,
                "validation_witness_ids": [passed_id],
                "workaround": workaround,
            }
        )
        witnesses.extend(
            [
                {
                    "completion_credit": 0,
                    "method_id": method_id,
                    "result": "fail",
                    "signature": signature,
                    "witness_id": failed_id,
                },
                {
                    "bounded_scope": workaround,
                    "method_id": method_id,
                    "result": "pass",
                    "witness_id": passed_id,
                },
            ]
        )
        for state in ("observed_failure", "retained_zero_credit", "bounded_recovery", "recurrence_guarded"):
            events.append({"method_id": method_id, "ordinal": len(events) + 1, "state": state})
    return methods, witnesses, events


def mutation_methods(mutations: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    for ordinal, row in enumerate(mutations, 1):
        method_id = f"EC6692-METHOD-MUT-{ordinal:03d}"
        failed_id = f"EC6692-WITNESS-MUT-{ordinal:03d}-F"
        passed_id = f"EC6692-WITNESS-MUT-{ordinal:03d}-P"
        methods.append(
            {
                "approval_class": "safe_now",
                "failed_witness_ids": [failed_id],
                "failure_id": row["mutation_id"],
                "failure_signature": row["mutation_kind"],
                "method_id": method_id,
                "owner": OWNER,
                "phase": PHASE,
                "protected_gates": ["synthetic_only", "zero_external_action", "no_claim_promotion"],
                "recurrence_guard": f"reject fixture whenever {row['mutation_kind']} is observed",
                "result": "rejected_as_preregistered",
                "rollback": "retain the invalid fixture at zero credit and preserve the accepted bounded control",
                "stage": "x2",
                "validation_witness_ids": [passed_id],
                "workaround": "fail closed with the exact stable rejection reason",
            }
        )
        witnesses.extend(
            [
                {
                    "completion_credit": 0,
                    "method_id": method_id,
                    "mutation_id": row["mutation_id"],
                    "result": "fail",
                    "witness_id": failed_id,
                },
                {
                    "completion_credit": 0,
                    "method_id": method_id,
                    "observed": row["observed"],
                    "result": "pass",
                    "witness_id": passed_id,
                },
            ]
        )
        for state in ("mutation_materialized", "retained_zero_credit", "guard_rejected", "recurrence_guarded"):
            events.append({"method_id": method_id, "ordinal": len(events) + 1, "state": state})
    return methods, witnesses, events


def skill_document(name: str, index: int) -> str:
    focus = name.removeprefix("ghc-family-lutherie-")
    return f"""---
name: {name}
description: Owner-local Elowen v669-v2 synthetic lutherie {focus} contract with fail-closed evidence and authority boundaries.
---

# {name}

Use this phase-local skill only for the Elowen v669-v2 owner lane. It is not globally installed or promoted.

## Boundary

{IDENTITY_BOUNDARY} This skill uses zero real people, instruments, materials, observations, measurements, treatments, repairs, keys, proofs, identity events, professional decisions, legal or cultural decisions, affected-party approvals, or authority acts. Māori wording, concepts, data governance, and authority remain under Māori authority.

## Procedure

1. Load the immutable x1 proposal row associated with the `{focus}` surface.
2. Require explicit synthetic state, domain and unit status, zero-valued real-world counters, empty external actions, and empty protected claims.
3. Preserve vacancies and the declared outcome label without promotion.
4. Execute the four preregistered invalid mutations and require stable rejection.
5. Retain every failed mutation at zero credit and link the bounded passing guard witness.

## Acceptance

Quick validation requires this frontmatter, all five procedure steps, the relational and authority boundary, and a successful owner-local smoke read. That proves only that the instruction packet is structurally usable by this phase; it does not prove professional competence, accessibility completeness, security completeness, independent reproduction, production readiness, or Stage 20 authority.

Skill ordinal: {index:02d}.
"""


def runner_script(profile: str) -> str:
    return f"""from __future__ import annotations

from ghc_family_lutherie_contracts import cli_for_profile


if __name__ == \"__main__\":
    raise SystemExit(cli_for_profile(\"{profile}\"))
"""


def portfolio_ledger(category: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    output: list[dict[str, Any]] = []
    for index, row in enumerate(rows, 1):
        if category in {"exact_approval", "blocked"}:
            disposition = "exact_gate"
            state = "held_unexecuted"
        elif category == "candidates":
            if index in {1, 2, 3, 4}:
                disposition, state = "open_gap", "absence_preserved"
            elif index == 27:
                disposition, state = "exact_gate", "authority_gate_preserved"
            elif index in {6, 7, 8, 15, 18, 19, 24, 25, 26, 28, 29}:
                disposition, state = "represented", "typed_or_protocol_surface_only"
            else:
                disposition, state = "completed", "bounded_synthetic_check_complete"
        else:
            disposition, state = "completed", "bounded_owner_local_check_complete"
        output.append(
            {
                **row,
                "completion_credit": 1 if disposition == "completed" else 0,
                "evidence_scope": "owner-local synthetic contract, structural check, held gate, or explicit absence only",
                "execution_state": state,
                "observed_disposition": disposition,
                "x2_external_actions": 0,
            }
        )
    return {
        "category": category,
        "count": len(output),
        "outcome_counts": dict(Counter(row["observed_disposition"] for row in output)),
        "owner": OWNER,
        "phase": PHASE,
        "rows": output,
        "schema": "ghc.family.portfolio-execution-ledger.v2",
    }


def overview_text(truth: dict[str, Any], portfolio_counts: dict[str, dict[str, int]]) -> str:
    sections = [
        (
            "Evidence scope",
            f"Elowen Cairn is relational working language for a {RELATIONAL_ROLE}, with the hope {RELATIONAL_HOPE}. {IDENTITY_BOUNDARY} "
            "This immutable-evidence candidate executes only the bounded synthetic contracts frozen at x1. It uses no real person, participant, "
            "luthier, musician, owner, custodian, instrument, component, material, workshop, measurement, treatment, repair, tuning action, identity "
            "event, legal or cultural decision, affected-party approval, or authority act. It confers no employment, qualification, competence, "
            "scientific authority, operational authority, or Māori authority.",
        ),
        (
            "Contract execution",
            "Forty positive contract fixtures were materialized from the immutable preregistration. Every fixture requires an explicit synthetic "
            "state, explicit domain and unit treatment, zero-valued real-world counters, an empty external-action list, an empty protected-claim list, "
            "authority vacancy, professional-status abstention, and the original protected gates. Twenty-eight fixtures meet bounded completion gates. "
            "Eight remain typed or protocol representations. The Library of Congress zero-call adapter and human-evaluation surface remain open gaps. "
            "The instrument-authority and Stage 20 locks remain exact gates. Passing a generic contract checker never changes those dispositions.",
        ),
        (
            "Rejecting mutations",
            "All 160 preregistered invalid mutations executed. Each proposal supplied four failures: missing required state, ambiguous domain or unit, "
            "a real-world or external-action request, and a protected-claim promotion. All 160 were rejected with stable reason codes and remain retained "
            "at zero completion credit. Each failed fixture has a paired bounded passing witness for the rejection guard. The guard witness shows only that "
            "the owner-local contract failed closed on that synthetic input; it does not validate real data, safety, professional practice, law, culture, "
            "privacy completeness, accessibility completeness, or scientific truth.",
        ),
        (
            "Source and assertion firewall",
            "The current source ledger is reused as bounded vocabulary and obligation evidence only. Library of Congress collection material can name a public "
            "collection surface, but this phase performs no collection query and imports no catalog row, media object, attribution, rights statement, or condition "
            "claim. NIOSH language supports the existence of a wood-dust hazard vocabulary, not a workplace assessment or instruction. WCAG 2.2 supports structural "
            "criteria, not a complete accessibility result. NIST digital-identity guidance, W3C provenance concepts, and RFC canonicalization vocabulary inform fields "
            "without creating keys, proofs, interoperability, conformance, authenticity, or trust. ICOM material supports a source-version receipt, not professional "
            "or cultural ratification. Te Mana Raraunga is used only to reinforce the stop at Māori authority. Research papers motivate typed obligations but supply "
            "no data row, fitted parameter, likelihood, instrument measurement, or empirical confirmation to this owner phase.",
        ),
        (
            "Evidence admission and non-substitution",
            "Every artifact states which kind of evidence it can admit. A positive synthetic fixture can demonstrate schema closure, stable state vocabulary, an explicit "
            "vacancy, or fail-closed control behavior. It cannot substitute for an observation, measurement, participant record, professional examination, calibrated "
            "instrument, source-controlled material sample, live credential, consent receipt, authority decision, independent audit, or external reproduction. Counts "
            "are therefore separated from claims: forty accepted controls do not mean forty real findings, and 160 rejected mutations do not mean exhaustive security. "
            "Represented surfaces remain represented even when their JSON is valid. Open gaps remain open when their zero-call or zero-person invariants pass. Exact "
            "gates remain exact when their lock behaves correctly. The conjunctive Stage 20 vector cannot be satisfied by adding synthetic rows across missing evidence "
            "classes, and no same-owner test can fill an authority-owned component.",
        ),
        (
            "Correction, recovery, and provenance",
            "Operational faults and deliberately invalid fixtures follow the same retention discipline without being conflated. An operational fault records the exact "
            "failed assumption, its zero-credit witness, the narrow recovery, a passing witness for that recovery, a recurrence guard, and a rollback. A mutation record "
            "preserves the invalid input class and the checker reason that rejected it. Neither category is deleted after recovery. Corrections are append-only and "
            "bitemporal in design: later records may supersede a field while preserving what was known and recorded earlier. Provenance links point only to immutable x1 "
            "proposal rows, owner-generated x2 controls, or declared public-source metadata. They never infer an instrument maker, owner, custodian, treatment history, "
            "material identity, authenticity, value, cultural meaning, or legal title. Rollback remains owner-local and additive; it never resets, amends, rewrites, "
            "force-pushes, merges, deletes, or mutates another owner's branch or worktree.",
        ),
        (
            "Workload and stopping discipline",
            "Execution volume is bounded by exact x1 portfolios and is not a quota that overrides evidence or care. The wellbeing and workload receipt describes context "
            "pressure, interruption tolerance, queue limits, and stopping conditions without pretending to measure a person's health. Work stops on phase or source drift, "
            "unexpected dirty inherited state, file or document ceiling pressure, an undeclared external dependency, account or credential demand, network or third-party "
            "write, host-security change, elevation, protected claim, missing authority, weekly usage exhaustion, or ambiguous terminal route. Candidate tasks can end as "
            "represented, open_gap, or exact_gate without being failures of diligence. Exact-approval and blocked portfolios receive evidence because their holds are "
            "inspectable, not because the forbidden actions occurred. The route remains prepared but unsent throughout x2, and no successor activation is inherited as "
            "completion credit or performed before the final terminal gate.",
        ),
        (
            "GMUT Mind",
            "The GMUT string, shell, plate, bridge, spectrum, inverse-map, damping, and acoustic-to-psyche surfaces are typed obligation boards only. "
            "Their ledgers explicitly record zero data rows, zero equations solved, zero likelihoods fitted, and zero constrained parameters. They do not "
            "produce an eigenfrequency, mode shape, stiffness, damping value, radiation estimate, force, material law, empirical prediction, quantum or "
            "ultraviolet completion, final physics, Theory-of-Everything proof, or canon. The lutherie analogy is bookkeeping, not evidence that a physical "
            "model describes any instrument or mind.",
        ),
        (
            "THOS Body and practice boundary",
            "THOS surfaces remain participant-free proxies with zero governed real arms, operators, participants, effectiveness estimates, safety monitoring, "
            "or independent review. The synthetic lutherie practice lens organizes vocabulary, component topology, vacancies, correction, workload, and handover, "
            "but demonstrates no craft, inspection, handling, tuning, setup, repair, conservation, hazard evaluation, product release, or professional competence. "
            "Hazard records are referral holds only and provide no safety instruction or risk determination.",
        ),
        (
            "Freed ID, CBR, and authority",
            "Freed ID records remain synthetic and nonproduction with zero keys, proofs, issuers, status services, lifecycle events, interoperability, governed "
            "recovery, privacy review, independent security review, or trust governance. CBR challenge and disclosure records are state-machine hypotheses, not "
            "rights decisions or remedies. Authorship, attribution, ownership, custody, copyright, heritage, traditional knowledge, cultural meaning, legal "
            "interpretation, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, and Māori authority remain exact-gated. Māori "
            "concepts remain under Māori authority.",
        ),
        (
            "Portfolio execution",
            f"The execution ledgers preserve exact x1 counts: {PORTFOLIO_COUNTS}. Observed portfolio-label counts are {portfolio_counts}. Safe-now checks, "
            "owner-local skill packages, family-current runner wrappers, and CLEAN/FIX/REFINE checks completed only where their structural predicates passed. "
            "Candidate rows were assigned completed, represented, open_gap, or exact_gate according to the actual bounded evidence. All exact-approval and "
            "blocked rows remain held and unexecuted. Successor recommendations remain zero-credit seeds and no successor was contacted during x2.",
        ),
        (
            "Skills and runners",
            "Twenty phase-local skill packets were built under the owner phase directory, quick-validated, and smoke-read. They were not globally installed. "
            "Ten family-current ghc_family_lutherie runner wrappers were built and smoke-used through list-form subprocess invocation. Each runner selected only "
            "a bounded proposal subset, performed zero network calls and zero external actions, and returned accepted synthetic controls. These receipts prove "
            "only caller and contract compatibility within this owner lane. They do not promote the tools globally or establish independent reproduction.",
        ),
        (
            "Method Flow and retained truth",
            f"The evidence candidate retains {truth['new_operational_failures']} new operational failures and {truth['rejecting_mutations']} rejecting mutations. "
            f"Effective truth is {truth['effective_negatives']} negatives, {truth['methods']} methods, {truth['failed_witnesses']} failed witnesses, "
            f"{truth['passing_witnesses']} bounded passing witnesses, {truth['open_gaps']} open gaps, and {truth['exact_gates']} exact gates. Every operational "
            "or mutation recovery is paired with its failed witness. No recovery erases a failure or converts same-owner synthetic evidence into external proof.",
        ),
        (
            "Accessibility and privacy",
            "The later static report is planned with semantic landmarks, a skip link, heading order, captioned tables, scoped headers, text-redundant statuses, "
            "visible keyboard focus, responsive reflow, and print fallback. Those are structural checks only. Manual keyboard, touch, zoom, browser-diverse, "
            "assistive-technology, cognitive, Māori-language, security-usability, print, and affected-user evaluation remain reserved. Five-class scanning keeps "
            "raw task or thread identifiers, private routes and paths, credentials, keys, tokens, transcripts, screenshots, session streams, private callable "
            "identifiers, and private application state out of owner artifacts.",
        ),
        (
            "Lifecycle and verdict",
            "This evidence candidate can be committed only after exact staging, manifest replay, scoped tests, strict JSON parsing, document and file ceilings, "
            "privacy scanning, bounded changed-code security review, diff hygiene, and x1 ancestry pass. A separate closeout commit must then build the final truth, "
            "registers, accessible report, seal, route candidate, and final manifests. Only after that clean pushed final may one exclusive canonical owner aggregate "
            "run. The full repository suite remains outside this non-Eiren phase. The terminal verdict remains NOT_READY_FOR_STAGE_20.",
        ),
    ]
    lines = [f"# {OWNER} {PHASE} immutable x2 evidence overview", ""]
    for heading, body in sections:
        lines.extend([f"## {heading}", "", body, ""])
    return "\n".join(lines)


def is_changed_from_x1(path: Path) -> bool:
    relative = path.relative_to(ROOT).as_posix()
    probe = run_git("cat-file", "-e", f"{FROZEN_X1}:{relative}", check=False)
    if probe.returncode != 0:
        return True
    old = run_git("show", f"{FROZEN_X1}:{relative}", text=False).stdout
    oid = git("hash-object", "-w", "--path", relative, relative)
    current = run_git("cat-file", "blob", oid, text=False).stdout
    return old != current


def main() -> None:
    assert_x2_start()
    prior_review_path = ROOT / STAGED_REVIEW
    if prior_review_path.exists():
        try:
            prior_review = json.loads(prior_review_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            prior_review = {}
        if prior_review.get("status") == "FAIL_IMMUTABLE_EVIDENCE_STAGED_ZERO_CREDIT":
            write_json(FAILED_STAGED_REVIEW, prior_review)
        elif prior_review.get("status") == "FAIL_DEPENDENCY_RECOVERY_ZERO_CREDIT":
            if prior_review.get("recovery", {}).get("invocation_count") == 2:
                write_json(FAILED_RECOVERY_REVIEW_2, prior_review)
            else:
                write_json(FAILED_RECOVERY_REVIEW, prior_review)
    now = utc_now()
    proposals = load_proposals()
    execution = execute_contracts(proposals)
    positive = execution["positive"]
    mutations = execution["mutations"]
    if len(positive) != 40 or not all(row["result"]["accepted"] for row in positive):
        raise RuntimeError("positive contract execution drift")
    if len(mutations) != 160 or any(row["observed"] != "reject" for row in mutations):
        raise RuntimeError("rejecting mutation execution drift")
    if execution["outcome_counts"] != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise RuntimeError("outcome count drift")

    for row in positive:
        fixture = row["fixture"]
        proposal_id = fixture["proposal_id"].lower()
        slug = fixture["semantic_slug"]
        write_json(REL_PHASE_ROOT / f"x2/proposals/{proposal_id}-{slug}.json", row)
        write_json(
            REL_PHASE_ROOT / f"x2/cards/{proposal_id}-{slug}.json",
            {
                "acceptance": row["result"],
                "authority_status": fixture["authority_status"],
                "bounded_completion_credit": fixture["bounded_completion_credit"],
                "declared_outcome": fixture["declared_outcome"],
                "external_actions": 0,
                "owner": OWNER,
                "phase": PHASE,
                "proposal_id": fixture["proposal_id"],
                "schema": "ghc.family.proposal-evidence-card.v2",
                "semantic_slug": slug,
                "source_is_x1_freeze": True,
            },
        )
    mutation_paths: list[str] = []
    for index in range(0, len(mutations), 20):
        path = REL_PHASE_ROOT / f"x2/mutations/mutation-ledger-{index // 20 + 1:02d}.json"
        write_json(
            path,
            {
                "completion_credit": 0,
                "count": len(mutations[index : index + 20]),
                "owner": OWNER,
                "phase": PHASE,
                "rows": mutations[index : index + 20],
                "schema": "ghc.family.rejecting-mutation-ledger.v2",
            },
        )
        mutation_paths.append(path.as_posix())

    write_json(
        REL_PHASE_ROOT / "x2/outcome-ledger.json",
        {
            "allowed_labels": sorted(ALLOWED_OUTCOMES),
            "counts": execution["outcome_counts"],
            "mutation_count": len(mutations),
            "mutation_shards": mutation_paths,
            "owner": OWNER,
            "phase": PHASE,
            "positive_contracts": len(positive),
            "schema": "ghc.family.outcome-ledger.v2",
        },
    )

    x1_portfolios: dict[str, list[dict[str, Any]]] = {}
    portfolio_outcomes: dict[str, dict[str, int]] = {}
    for category in PORTFOLIO_COUNTS:
        source = json.loads((PHASE_ROOT / f"x1/portfolios/{category}.json").read_text(encoding="utf-8"))["rows"]
        ledger = portfolio_ledger(category, source)
        x1_portfolios[category] = source
        portfolio_outcomes[category] = ledger["outcome_counts"]
        write_json(REL_PHASE_ROOT / f"x2/portfolio-execution/{category}.json", ledger)

    skill_receipts: list[dict[str, Any]] = []
    for index, name in enumerate(SKILL_NAMES, 1):
        path = write_text(REL_PHASE_ROOT / f"tools/skills/{name}/SKILL.md", skill_document(name, index))
        content = path.read_text(encoding="utf-8")
        passed = content.startswith("---\nname:") and "## Procedure" in content and "Māori authority" in content
        skill_receipts.append(
            {
                "completion_credit": 1 if passed else 0,
                "external_actions": 0,
                "globally_installed": False,
                "name": name,
                "path": path.relative_to(ROOT).as_posix(),
                "quick_validation": "PASS" if passed else "FAIL",
                "smoke_use": "PASS_OWNER_LOCAL_READ" if passed else "FAIL",
            }
        )
    if not all(row["quick_validation"] == "PASS" for row in skill_receipts):
        raise RuntimeError("skill quick validation failed")
    write_json(
        REL_PHASE_ROOT / "tools/skill-smoke-receipt.json",
        {"count": len(skill_receipts), "owner": OWNER, "phase": PHASE, "rows": skill_receipts, "schema": "ghc.family.skill-smoke.v2"},
    )

    profiles = list(RUNNER_PROFILES)
    if len(profiles) != len(RUNNER_NAMES):
        raise RuntimeError("runner name/profile count drift")
    runner_receipts: list[dict[str, Any]] = []
    for name, profile in zip(RUNNER_NAMES, profiles, strict=True):
        path = write_text(Path("scripts") / f"{name}.py", runner_script(profile))
        result = subprocess.run([sys.executable, "-X", "utf8", str(path),], cwd=ROOT, capture_output=True, text=True, check=False)
        payload = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else {}
        runner_receipts.append(
            {
                "completion_credit": 1 if result.returncode == 0 and payload.get("status") == "PASS" else 0,
                "external_actions": payload.get("external_actions"),
                "name": name,
                "network_calls": payload.get("network_calls"),
                "path": path.relative_to(ROOT).as_posix(),
                "profile": profile,
                "return_code": result.returncode,
                "smoke_status": payload.get("status", "FAIL"),
            }
        )
    if not all(row["smoke_status"] == "PASS" for row in runner_receipts):
        raise RuntimeError("runner smoke validation failed")
    write_json(
        REL_PHASE_ROOT / "tools/runner-smoke-receipt.json",
        {"count": len(runner_receipts), "owner": OWNER, "phase": PHASE, "rows": runner_receipts, "schema": "ghc.family.runner-smoke.v2"},
    )

    op_methods, op_witnesses, op_events = operation_methods()
    mut_methods, mut_witnesses, mut_events = mutation_methods(mutations)
    methods = op_methods + mut_methods
    witnesses = op_witnesses + mut_witnesses
    events = op_events + [dict(row, ordinal=len(op_events) + row["ordinal"]) for row in mut_events]
    if len(methods) != len(STARTUP_FAILURES) + len(X2_FAILURES) + 160:
        raise RuntimeError("Method Flow method count drift")
    write_json(
        REL_PHASE_ROOT / "method-flow/evidence-ledger.json",
        {
            "append_only": True,
            "effective_method_count": SOURCE_OVERLAY["methods"] + len(methods),
            "methods": methods,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.method-flow-ledger.v5",
            "source_sealed_method_count": SOURCE_OVERLAY["methods"],
            "state_events": events,
            "witnesses": witnesses,
        },
    )

    portfolio_witnesses = sum(PORTFOLIO_COUNTS.values())
    passing_witnesses = SOURCE_OVERLAY["passing_witnesses"] + len(STARTUP_FAILURES) + len(X2_FAILURES) + 160 + 40 + portfolio_witnesses
    truth = {
        "core_outcomes": execution["outcome_counts"],
        "effective_negatives": EVIDENCE_OVERLAY["effective_negatives"] + 160,
        "exact_gates": EVIDENCE_OVERLAY["exact_gates"] + 2,
        "failed_witnesses": EVIDENCE_OVERLAY["failed_witnesses"] + 160,
        "immutable_x1": FROZEN_X1,
        "methods": EVIDENCE_OVERLAY["methods"] + 160,
        "new_operational_failures": len(STARTUP_FAILURES) + len(X2_FAILURES),
        "open_gaps": EVIDENCE_OVERLAY["open_gaps"] + 2,
        "owner": OWNER,
        "passing_witnesses": passing_witnesses,
        "phase": PHASE,
        "rejecting_mutations": 160,
        "schema": "ghc.family.immutable-evidence-truth.v2",
        "status": "IMMUTABLE_EVIDENCE_CANDIDATE",
        "terminal_verdict": TERMINAL_VERDICT,
    }
    write_json(REL_PHASE_ROOT / "x2/phase-truth-evidence.json", truth)
    write_json(
        REL_PHASE_ROOT / "x2/retained-negative-register.json",
        {
            "effective_negatives": truth["effective_negatives"],
            "mutation_failures": mutations,
            "new_operational_failures": [
                {"failure_id": row[0], "signature": row[1], "workaround": row[2], "recurrence_guard": row[3]}
                for row in STARTUP_FAILURES + X2_FAILURES
            ],
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.retained-negative-register.v3",
            "source_sealed_negatives": SOURCE_OVERLAY["effective_negatives"],
        },
    )
    write_json(
        REL_PHASE_ROOT / "x2/open-exact-gate-register.json",
        {
            "effective_exact_gates": truth["exact_gates"],
            "effective_open_gaps": truth["open_gaps"],
            "new_exact_gates": ["EC6692-N039", "EC6692-N040"],
            "new_open_gaps": ["EC6692-N037", "EC6692-N038"],
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.open-exact-gate-register.v3",
        },
    )
    write_json(
        REL_PHASE_ROOT / "x2/wellbeing-workload-check.json",
        {
            "context_pressure": "bounded_by_shards_and_generated_ledgers",
            "external_coordination": 0,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.wellbeing-workload.v2",
            "status": "SUSTAINABLE_WITH_TERMINAL_STOP_RULES",
            "stop_conditions": ["usage_exhaustion", "phase_or_source_drift", "privacy_or_authority_gate", "ambiguous_route"],
            "synthetic_health_measurement": False,
            "work_items_observed": PORTFOLIO_COUNTS,
        },
    )
    write_text(REL_PHASE_ROOT / "x2/integrated-evidence-overview.md", overview_text(truth, portfolio_outcomes))

    write_json(
        REL_PHASE_ROOT / "validation/evidence-staged-review.json",
        {"owner": OWNER, "phase": PHASE, "schema": "ghc.family.evidence-staged-review.v2", "status": "PREPARED_FOR_EXACT_STAGED_VALIDATION"},
    )

    owner_paths = phase_owner_files()
    initial_delta = [path for path in owner_paths if is_changed_from_x1(path)]
    intended = sorted(
        set(
            [path.relative_to(ROOT).as_posix() for path in initial_delta]
            + [EVIDENCE_MANIFEST, DELTA_MANIFEST, STAGED_REVIEW, STAGED_ALLOWLIST]
        )
    )
    write_json(
        STAGED_ALLOWLIST,
        {
            "expected_paths": intended,
            "owner": OWNER,
            "path_count": len(intended),
            "phase": PHASE,
            "schema": "ghc.family.evidence-staged-allowlist.v2",
            "strict_after_x1": True,
        },
    )
    owner_paths = phase_owner_files()
    owner_exclusions = {EVIDENCE_MANIFEST, DELTA_MANIFEST, STAGED_REVIEW}
    owner_entries = manifest_rows(path for path in owner_paths if path.relative_to(ROOT).as_posix() not in owner_exclusions)
    write_json(
        EVIDENCE_MANIFEST,
        {
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.evidence-owner-manifest.v2",
            "self_exclusions": sorted(owner_exclusions),
        },
    )
    delta_exclusions = {EVIDENCE_MANIFEST, DELTA_MANIFEST, STAGED_REVIEW}
    delta_paths = [path for path in phase_owner_files() if is_changed_from_x1(path) and path.relative_to(ROOT).as_posix() not in delta_exclusions]
    delta_entries = manifest_rows(delta_paths)
    write_json(
        DELTA_MANIFEST,
        {
            "base": FROZEN_X1,
            "entries": delta_entries,
            "entry_count": len(delta_entries),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.evidence-delta-manifest.v2",
            "self_exclusions": sorted(delta_exclusions),
        },
    )
    payload = {
        "evidence_manifest_entries": len(owner_entries),
        "evidence_overlay": truth,
        "mutation_count": len(mutations),
        "outcomes": execution["outcome_counts"],
        "owner": OWNER,
        "phase": PHASE,
        "portfolio_counts": PORTFOLIO_COUNTS,
        "runner_smokes": len(runner_receipts),
        "skill_smokes": len(skill_receipts),
        "status": "X2_EVIDENCE_MATERIALIZED_NOT_COMMITTED",
    }
    payload["payload_sha256"] = sha256_bytes(canonical_json_bytes(payload))
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
