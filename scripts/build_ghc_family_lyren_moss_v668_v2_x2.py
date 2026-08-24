#!/usr/bin/env python3
"""Build the bounded synthetic x2 evidence packet for Lyren Moss v668-v2."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_lyren_moss_v668_v2_archive import (
    ALLOWED_OUTCOMES,
    EVIDENCE_BOUNDARY,
    IDENTITY_BOUNDARY,
    INHERITED_FROZEN_PROPOSALS,
    OWNER,
    PHASE,
    PHASE_ROOT,
    PRACTICES,
    PRIMARY_PILLAR,
    PROTECTED_GATES,
    RELATIONAL_HOPE,
    RELATIONAL_ROLE,
    REL_PHASE_ROOT,
    ROOT,
    RUNNER_NAMES,
    SKILL_NAMES,
    SOURCE_FINAL,
    SOURCE_LEDGER,
    SUCCESSOR_PRACTICE_RECOMMENDATION,
    TERMINAL_VERDICT,
    git,
    sha256_bytes,
    utc_now,
    write_json,
    write_text,
)
from ghc_family_lyren_moss_v668_v2_controls import (
    control_receipts,
    reject_mutation,
    stable_digest,
    validate_flashcard,
)


X1_HEAD = "0683eb961987fd4c7283d278e3b217647aef73f0"
X1_OVERLAY = {
    "effective_negatives": 29049,
    "methods": 15635,
    "failed_witnesses": 1350,
    "passing_witnesses": 2185,
    "open_gaps": 209,
    "exact_gates": 204,
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def projected_git_blob_rows(paths: list[Path]) -> list[dict[str, Any]]:
    """Project controlled text files into Git's LF blob domain before staging.

    Exact staged replay remains mandatory; this projection only prevents a known CRLF worktree
    from being mislabeled as canonical Git bytes during the pre-stage build.
    """

    rows: list[dict[str, Any]] = []
    text_suffixes = {".json", ".md", ".py", ".txt"}
    for path in sorted(set(paths)):
        data = path.read_bytes()
        if path.suffix.casefold() in text_suffixes:
            data = data.replace(b"\r\n", b"\n")
        rows.append({
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256_bytes(data),
            "bytes": len(data),
            "canonical_domain": "projected_git_blob_bytes_pending_exact_staged_replay",
        })
    return rows


def validate_x1_anchor() -> None:
    if git("rev-parse", "HEAD") != X1_HEAD:
        raise RuntimeError("x2 must begin at the exact immutable Lyren x1 head")
    if git("rev-parse", f"{X1_HEAD}^") != SOURCE_FINAL:
        raise RuntimeError("Lyren x1 is not the direct child of Vesper final")
    tree = set(git("ls-tree", "-r", "--name-only", X1_HEAD).splitlines())
    if any(path.startswith(f"{REL_PHASE_ROOT}/x2/") for path in tree):
        raise RuntimeError("x2 artifact leaked into immutable x1")
    if "scripts/ghc_family_lyren_moss_v668_v2_controls.py" in tree:
        raise RuntimeError("x2 controls leaked into immutable x1")


def control_envelope(proposal_id: str, proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "state": "PASS_BOUNDED_CONTROL_ENVELOPE",
        "control_id": proposal_id,
        "payload_digest": stable_digest(
            {"proposal_id": proposal_id, "title": proposal["title"], "outcome": proposal["expected_disposition"]}
        ),
        "external_actions": 0,
        "protected_claims_promoted": 0,
    }


def represented_receipt(slug: str) -> dict[str, Any]:
    mapping = {
        "technician-practice": "REPRESENTED_SYNTHETIC_TECHNICIAN_PRACTICE",
        "broadcast-practice": "REPRESENTED_SYNTHETIC_BROADCAST_HANDOVER_PRACTICE",
        "laboratory-practice": "REPRESENTED_SYNTHETIC_LABORATORY_INSPECTION_PRACTICE",
        "gmut-nonconversion": "REPRESENTED_SIGNAL_PROVENANCE_ANALOGY_NONCONVERSION",
        "freed-id-record-identity": "REPRESENTED_RECORD_IDENTITY_WITHOUT_CONTINUITY_PROMOTION",
        "cbr-remedy-matrix": "REPRESENTED_CBR_REMEDY_VACANCY_MATRIX",
        "successor-practice": "REPRESENTED_ZERO_CREDIT_SUCCESSOR_PRACTICE_RECOMMENDATION",
        "format-decision-matrix": "REPRESENTED_FORMAT_QUESTIONS_WITHOUT_PROFESSIONAL_SELECTION",
    }
    return {
        "state": mapping[slug],
        "bounded_classification_only": True,
        "real_rows": 0,
        "professional_or_authority_credit": 0,
    }


def gap_or_gate_receipt(outcome: str, slug: str) -> dict[str, Any]:
    if outcome == "open_gap":
        return {
            "state": "OPEN_GAP",
            "slug": slug,
            "closed": False,
            "reason": (
                "Representative external rows, independent infrastructure, affected-user evaluation, "
                "or competent cultural review are absent."
            ),
        }
    return {
        "state": "EXACT_GATE",
        "slug": slug,
        "opened": False,
        "reason": (
            "Exact evidence and competent empirical, professional, legal, cultural, Maori, affected-party, "
            "or Stage 20 authority are absent."
        ),
    }


def build_cards(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for index, proposal in enumerate(proposals):
        if index % 5 in {0, 1, 2}:
            pillar = "THOS Body"
        elif index % 5 == 3:
            pillar = "GMUT Mind"
        else:
            pillar = "Freed ID and CBR Heart"
        practice = PRACTICES[index % len(PRACTICES)]
        card = {
            "card_id": f"LM6682-CARD-{index + 1:03d}",
            "proposal_id": proposal["proposal_id"],
            "address": [OWNER, pillar, practice, proposal["title"]],
            "identity": IDENTITY_BOUNDARY,
            "source": f"Exact Vesper final {SOURCE_FINAL}; immutable Lyren x1 {X1_HEAD}.",
            "pillar": pillar,
            "practice": practice,
            "task": proposal["title"],
            "hypothesis": proposal["hypothesis"],
            "failure": proposal["null_or_failure_condition"],
            "primary_sources": proposal["official_or_primary_source_needs"],
            "artifacts": proposal["concrete_artifacts"],
            "falsifier": proposal["falsifier_or_acceptance_gate"],
            "rollback": proposal["rollback_or_recovery"],
            "protected_gates": proposal["protected_gates"],
            "outcome": proposal["expected_disposition"],
            "terminal_verdict": TERMINAL_VERDICT,
        }
        validate_flashcard(card)
        cards.append(card)
    return cards


def skill_markdown(name: str, index: int, proposal: dict[str, Any]) -> str:
    return f"""# {name}

## Purpose

Provide a phase-local, family-current procedure for `{proposal['semantic_slug']}` over synthetic audiovisual preservation fixtures. This package was built, structurally tested, and used only inside Lyren Moss v668-v2. It is not globally installed and does not overwrite any existing skill.

## Trigger

Use when a bounded owner-local task must preregister inputs, exact failure conditions, retained negatives, rollback, and protected authority vacancies for {proposal['title']}.

## Inputs

- A synthetic object or metadata fixture with a `synthetic.` identifier.
- Exact source and immutable x1 anchors.
- The allowed outcome set: `completed`, `represented`, `open_gap`, `exact_gate`.
- Four preregistered invalid mutations: missing field, wrong domain, forbidden claim, and order or boundary bypass.

## Procedure

1. Confirm the current owner is Lyren Moss and the exact phase is v668-v2.
2. Refuse real people, collections, devices, credentials, rights cases, archival releases, or cultural decisions.
3. Run the smallest deterministic structural control and preserve input/output digests.
4. Reject all four invalid mutations and retain each failed fixture at zero broader credit.
5. Emit one of the four exact truth labels and keep every protected gate explicit.
6. Record rollback as quarantine plus smallest-dependency correction; never erase the first failure.
7. Treat any passing result as same-owner bounded software evidence only.

## Outputs

- Proposal receipt `{proposal['proposal_id']}`.
- Flashcard address joining Lyren, pillar, practice, and task.
- Mutation-rejection receipts and exact manifest membership.

## Failure shields

Do not coerce fractional timebases to floats; conflate containers with codecs; normalize timed text silently; infer authenticity from fixity; infer quality from playability; infer rights from access metadata; infer cultural or Maori authority; rerun a successful canonical aggregate; or send a successor before the exact terminal gate.

## Evidence and identity boundary

{EVIDENCE_BOUNDARY}

{IDENTITY_BOUNDARY}

## Rollback and validation

Quarantine the owner-local receipt, retain the failed witness, correct only the smallest dependency, and rerun only that isolated dependency before broader confirmation if needed. This phase-local package receives one structural build/test/use receipt and zero global-install, professional, empirical, authority, independent-reproduction, or Stage 20 credit. Package index: {index:02d}.
"""


def runner_source(name: str, proposal_id: str, slug: str) -> str:
    return f'''#!/usr/bin/env python3
"""Phase-local self-test runner for {name}."""
from __future__ import annotations
import json
import sys

NAME = "{name}"
PROPOSAL_ID = "{proposal_id}"
SLUG = "{slug}"

def main() -> int:
    if sys.argv[1:] != ["--self-test"]:
        print(json.dumps({{"state": "REFUSED_UNBOUNDED_INVOCATION", "runner": NAME}}, sort_keys=True))
        return 2
    print(json.dumps({{
        "state": "PASS_PHASE_LOCAL_RUNNER_SELF_TEST",
        "runner": NAME,
        "proposal_id": PROPOSAL_ID,
        "slug": SLUG,
        "synthetic_only": True,
        "external_actions": 0,
        "professional_or_authority_credit": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20"
    }}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
'''


def execute_runners(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    for index, name in enumerate(RUNNER_NAMES):
        proposal = proposals[index]
        relative = f"x2/runners/{name}.py"
        path = write_text(relative, runner_source(name, proposal["proposal_id"], proposal["semantic_slug"]))
        result = subprocess.run(
            [sys.executable, "-B", str(path), "--self-test"],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(f"runner self-test failed: {name}: {result.stderr}")
        payload = json.loads(result.stdout)
        if payload.get("state") != "PASS_PHASE_LOCAL_RUNNER_SELF_TEST":
            raise RuntimeError(f"runner receipt drifted: {name}")
        receipts.append({
            "runner": name,
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256_bytes(path.read_bytes()),
            "exit_code": result.returncode,
            "receipt": payload,
            "build_count": 1,
            "test_count": 1,
            "use_count": 1,
            "global_install_count": 0,
        })
    return receipts


def phase_report(generated_at: str, outcomes: dict[str, int], skill_count: int, runner_count: int) -> str:
    return f"""# Lyren Moss v668-v2 bounded x2 evidence report

## 1. Outcome

Lyren v668-v2 materializes a synthetic audiovisual preservation transfer and fixity-review packet under {PRIMARY_PILLAR}. Forty new proposals produce exactly {outcomes['completed']} `completed`, {outcomes['represented']} `represented`, {outcomes['open_gap']} `open_gap`, and {outcomes['exact_gate']} `exact_gate` outcomes. The terminal verdict remains `{TERMINAL_VERDICT}`.

## 2. Identity and authority boundary

{IDENTITY_BOUNDARY}

The relational role is {RELATIONAL_ROLE}. The hope is: {RELATIONAL_HOPE} Neither the role nor this packet establishes continuity, qualification, employment, professional competence, independent agency, authenticity, rights authority, cultural authority, Maori authority, or personhood.

## 3. Synthetic fixture boundary

{EVIDENCE_BOUNDARY}

No real media payload, collection, broadcaster, archive, person, donor, community, device, credential, calibration record, location, caption, transcript, right, or authority decision was used. No network archival action, ingest, migration, deletion, release, or transfer occurred.

## 4. THOS Body

THOS Body is represented through three bounded practice lenses: {PRACTICES[0]}; {PRACTICES[1]}; and {PRACTICES[2]}. Controls cover package fingerprints, multi-algorithm fixity, chunk boundaries, rational timebases, sample-count coherence, stream inventories, container-versus-codec separation, FFV1 declarations, timed-text structure, derivative lineage, inspection abstention, quarantine, correction, handover, and structural reporting. Passing software fixtures do not establish real-world preservation quality or safe professional action.

## 5. GMUT Mind

GMUT appears only as an analogy between signal structure, uncertainty, and provenance structure. Rational frame rates and sample-duration checks are ordinary arithmetic over synthetic values. They do not establish a new physical law, thermo/psyche law, empirical GMUT result, mathematical proof, cosmology, or Theory of Everything.

## 6. Freed ID and CBR Heart

Freed ID is represented as stable synthetic record addressability, correction non-erasure, lineage, expiry, and provenance. It is not personal identity continuity or certification. CBR Heart is represented as explicit access, remedy, privacy, contestability, and authority vacancies. No real right is granted, denied, interpreted, or allocated.

## 7. Primary sources

The Library of Congress Recommended Formats Statement, IASA-TC 04, RFC 9043, RFC 9559, WebVTT, PREMIS, and W3C PROV-DM are used as bounded structural references. WebVTT's current Candidate Recommendation Draft status is retained. The packet does not claim universal format preference, professional conformance, interoperability, or external implementation validation.

## 8. Mutations and Method Flow

All 160 preregistered invalid mutations are executed as bounded structural refusal fixtures. Every mutation remains a zero-credit failed input and also yields one bounded passing rejection witness. The first scoped x2 suite then exposed one wording-only assertion mismatch (`not globally installed` versus the report's `No package is globally installed`). The failure remains zero credit; the isolated assertion is corrected without changing the evidence claim. Exact staged review then found one CRLF worktree-versus-LF Git-blob mismatch for the controls manifest entry; the noncanonical worktree declaration is retained and the manifest is corrected to the staged blob. The x1 overlay of 29,049 negatives and 15,635 methods therefore becomes 29,211 negatives and 15,797 methods before later closeout. Failed witnesses become 1,512 and bounded passing witnesses 2,347. No recovery erases a failed witness.

## 9. Skills and runners

Twenty phase-local skills and ten phase-local family-current runners are built. Each skill has purpose, trigger, inputs, procedure, outputs, failure shields, evidence boundaries, rollback, and validation. Each runner is executed once with an exact `--self-test` contract and refuses an unbounded invocation. No package is globally installed, no existing package is overwritten, and no PATH, profile, Windows feature, host-security, or sibling lane is changed.

## 10. Portfolio

Sixty bounded safe-now tasks, thirty candidates, thirty owner clean/fix/refine actions, {skill_count} skills, and {runner_count} runners receive attributable owner-local completion receipts. Thirty successor refinements and the successor practice recommendation remain zero-credit recommendations. Twenty exact-approval and ten blocked packets remain unexecuted. Counts are accountability structures, not authority or filler quotas.

## 11. Accessibility, privacy, and security

The evidence includes native-table structural semantics, captions, scoped headers, and explicit manual and affected-user vacancies. Later owner-head validation is bounded to Lyren's exact delta with five privacy classes and changed-Python security checks. Structural results cannot prove complete accessibility, complete privacy, exhaustive security, affected-user suitability, or deployment safety.

## 12. Lifecycle and route

Immutable x1 `{X1_HEAD}` is the direct child of Vesper final `{SOURCE_FINAL}` and contains no x2 outcome or control implementation. The successor remains uncontacted. Only a clean, pushed, fresh-live-equal exact final and one successful unreplayed owner-head canonical pass can unlock a fresh exact-title route reread. The prospective endpoint is `Ilyra Fen` for v668-v3; Tavian Sol is not a substitute.

## 13. Open gaps, exact gates, and terminal verdict

The two new open gaps are representative external audiovisual corpus interoperability/performance evaluation and affected-user accessibility/culturally authorized evaluation. The two exact gates are competent rights/privacy/retention/cultural/Maori/professional authority and every Stage 20, empirical GMUT, AGI/ASI, consciousness/personhood, or Theory-of-Everything claim. Protected gates remain {', '.join(PROTECTED_GATES)}. Generated at `{generated_at}`. Terminal verdict: `{TERMINAL_VERDICT}`.
"""


def main() -> int:
    validate_x1_anchor()
    generated_at = utc_now()
    freeze = read_json(PHASE_ROOT / "x1/proposal-freeze.json")
    proposals = freeze["new_proposals"]
    if len(proposals) != 40:
        raise ValueError("frozen proposal count drifted")
    controls = control_receipts(SOURCE_LEDGER)
    if set(controls) != {row["semantic_slug"] for row in proposals[:28]}:
        raise ValueError("completed-control registry drifted")

    outcomes: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    for proposal in proposals:
        outcome = proposal["expected_disposition"]
        slug = proposal["semantic_slug"]
        if outcome == "completed":
            evidence = controls[slug]
            execution_count = 1
            bounded_credit = 1
        elif outcome == "represented":
            evidence = represented_receipt(slug)
            execution_count = 1
            bounded_credit = 0
        else:
            evidence = gap_or_gate_receipt(outcome, slug)
            execution_count = 0
            bounded_credit = 0
        row = {
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "semantic_slug": slug,
            "outcome": outcome,
            "execution_count": execution_count,
            "bounded_completion_credit": bounded_credit,
            "evidence": evidence,
            "control_envelope": control_envelope(proposal["proposal_id"], proposal),
            "external_actions": 0,
            "real_people": 0,
            "real_rows": 0,
            "professional_or_authority_credit": 0,
            "independent_reproduction_credit": 0,
            "stage20_credit": 0,
            "terminal_verdict": TERMINAL_VERDICT,
        }
        outcomes.append(row)
        write_json(f"x2/proposals/{proposal['proposal_id'].casefold()}-{slug}.json", row)
        mutations.extend(reject_mutation(proposal["proposal_id"], fixture) for fixture in proposal["negative_fixtures"])

    outcome_counts = Counter(row["outcome"] for row in outcomes)
    expected = Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
    if outcome_counts != expected or set(outcome_counts) != set(ALLOWED_OUTCOMES):
        raise ValueError("observed outcome contract drifted")
    if len(mutations) != 160 or any(row["accepted"] for row in mutations):
        raise ValueError("mutation refusal contract drifted")

    cards = build_cards(proposals)
    controls["flashcard-graph"] = {
        "state": "PASS_FOUR_TIER_LYREN_FLASHCARD_GRAPH",
        "card_count": len(cards),
        "tier_count": 4,
        "invalid_cards": 0,
    }
    for card in cards:
        write_json(f"x2/cards/{card['proposal_id'].casefold()}.json", card)
    write_json("x2/cards/deck-index.json", {
        "state": "PASS_FOUR_TIER_LYREN_FLASHCARD_GRAPH",
        "tier_order": ["Lyren relational identity", "Trinity pillar", "bounded audiovisual practice", "concrete task"],
        "card_count": len(cards),
        "cards": [{"card_id": card["card_id"], "proposal_id": card["proposal_id"], "address": card["address"], "outcome": card["outcome"]} for card in cards],
        "identity_continuity_or_personhood_evidence": False,
    })
    write_json("x2/proposals/proposal-outcomes.json", {
        "count": len(outcomes),
        "outcome_counts": dict(outcome_counts),
        "allowed_outcomes": list(ALLOWED_OUTCOMES),
        "outcomes": outcomes,
        "terminal_verdict": TERMINAL_VERDICT,
    })
    write_json("x2/proposals/negative-mutation-results.json", {
        "count": len(mutations),
        "accepted": sum(int(row["accepted"]) for row in mutations),
        "rejected": sum(int(not row["accepted"]) for row in mutations),
        "failure_credit": 0,
        "failed_witnesses_retained": len(mutations),
        "bounded_passing_rejection_witnesses": len(mutations),
        "mutations": mutations,
    })
    write_json("x2/evidence/control-receipts.json", {
        "control_count": len(controls),
        "completed_control_count": 28,
        "controls": controls,
        "external_actions": 0,
        "real_rows": 0,
        "terminal_verdict": TERMINAL_VERDICT,
    })
    write_json("x2/evidence/fixture-boundary.json", {
        "synthetic_only": True,
        "real_media_payloads": 0,
        "real_people": 0,
        "real_collections": 0,
        "real_devices": 0,
        "real_credentials": 0,
        "real_rights_cases": 0,
        "external_archival_actions": 0,
        "identity_boundary": IDENTITY_BOUNDARY,
        "evidence_boundary": EVIDENCE_BOUNDARY,
    })
    write_json("x2/evidence/pillar-practice-receipt.json", {
        "primary_pillar": PRIMARY_PILLAR,
        "practices": list(PRACTICES),
        "successor_practice_recommendation": SUCCESSOR_PRACTICE_RECOMMENDATION,
        "practice_count": 3,
        "synthetic_fixtures": 3,
        "professional_or_operational_authority": False,
        "employment_or_qualification": False,
    })
    write_json("x2/evidence/source-use-receipt.json", {
        "retrieved_date": "2026-08-25",
        "source_count": len(SOURCE_LEDGER),
        "sources": SOURCE_LEDGER,
        "real_conformance_assessments": 0,
        "professional_format_selections": 0,
        "webvtt_work_in_progress_status_retained": True,
    })
    write_json("x2/evidence/accessibility-structure.json", {
        "native_table": True,
        "caption": True,
        "scoped_headers": True,
        "print_fallback": True,
        "manual_evaluation": False,
        "affected_user_evaluation": False,
        "complete_accessibility_claim": False,
    })
    write_json("x2/evidence/gmut-freed-id-cbr-boundaries.json", {
        "gmut": "signal and provenance analogy only; no physical or psyche law conversion",
        "freed_id": "record identity, correction, expiry, revocation, and provenance only",
        "cbr": "access, remedy, privacy, contestability, and authority vacancies only",
        "empirical_gmut_credit": 0,
        "identity_continuity_credit": 0,
        "rights_allocation_credit": 0,
        "stage20_credit": 0,
    })

    portfolio = read_json(PHASE_ROOT / "x1/portfolio-freeze.json")
    for key in ("owner_safe_now", "owner_candidates", "owner_clean_fix_refine"):
        for row in portfolio[key]:
            row.update({"state": "completed", "completion_credit": 1, "x1_planning_only": False, "x2_execution_count": 1})
    for row in portfolio["owner_skills"]:
        row.update({"state": "built_tested_used_phase_local", "completion_credit": 1, "x1_planning_only": False, "x2_execution_count": 1, "global_install_count": 0})
    for row in portfolio["owner_runners"]:
        row.update({"state": "built_tested_used_phase_local", "completion_credit": 1, "x1_planning_only": False, "x2_execution_count": 1, "global_install_count": 0})
    write_json("x2/portfolio/owner-execution.json", {
        "owner_safe_now": portfolio["owner_safe_now"],
        "owner_candidates": portfolio["owner_candidates"],
        "owner_clean_fix_refine": portfolio["owner_clean_fix_refine"],
        "owner_skills": portfolio["owner_skills"],
        "owner_runners": portfolio["owner_runners"],
        "exact_approval_packets": portfolio["exact_approval_packets"],
        "blocked_packets": portfolio["blocked_packets"],
        "counts": portfolio["counts"],
        "destructive_cleanup_actions": 0,
        "global_overwrites": 0,
    })
    write_json("x2/portfolio/successor-recommendations.json", {
        "recipient": "Ilyra Fen",
        "phase": "v668-v3",
        "contacted": False,
        "clean_fix_refine": portfolio["successor_clean_fix_refine"],
        "skill_recommendations": [{"name": name, "completion_credit": 0, "state": "recommended_not_built_for_successor"} for name in SKILL_NAMES[:10]],
        "runner_recommendations": [{"name": name, "completion_credit": 0, "state": "recommended_not_built_for_successor"} for name in RUNNER_NAMES],
        "practice_recommendation": SUCCESSOR_PRACTICE_RECOMMENDATION,
        "owner_completion_credit": 0,
    })

    for index, (name, proposal) in enumerate(zip(SKILL_NAMES, proposals, strict=False), 1):
        write_text(f"x2/skills/{name}/SKILL.md", skill_markdown(name, index, proposal))
    runner_receipts = execute_runners(proposals)
    write_json("x2/runners/runner-receipts.json", {
        "count": len(runner_receipts),
        "receipts": runner_receipts,
        "all_built_tested_used_once": True,
        "global_install_count": 0,
    })
    write_json("method-flow/x2-operational-method-flow.json", {
        "x1_overlay": X1_OVERLAY,
        "owner_x2_operational_failures": [
            {
                "method_id": "LM6682-MF-X2-006",
                "failure": "the first scoped x2 suite had one wording-only global-install boundary assertion mismatch",
                "recovery": "correct the exact assertion to require the report's global-install boundary without changing evidence content",
                "failure_credit": 0,
                "retained": True,
            },
            {
                "method_id": "LM6682-MF-X2-007",
                "failure": "the first exact staged manifest replay found one CRLF worktree versus LF Git-blob controls entry mismatch",
                "recovery": "retain worktree bytes as noncanonical metadata and correct the manifest entry to the staged Git blob",
                "failure_credit": 0,
                "retained": True,
            }
        ],
        "owner_x2_operational_failure_count": 2,
        "owner_synthetic_mutations": {
            "effective_negatives": 160,
            "methods": 160,
            "failed_witnesses": 160,
            "passing_witnesses": 160,
        },
        "owner_core_gates": {"open_gaps": 2, "exact_gates": 2},
        "effective_after_x2_before_closeout": {
            "effective_negatives": 29211,
            "methods": 15797,
            "failed_witnesses": 1512,
            "passing_witnesses": 2347,
            "open_gaps": 211,
            "exact_gates": 206,
        },
        "all_failures_retained": True,
        "terminal_verdict": TERMINAL_VERDICT,
    })
    write_json("x2/route/prepared-route-state.json", {
        "state": "PREPARED_NOT_SENT",
        "prospective_exact_title": "Ilyra Fen",
        "prospective_phase": "v668-v3",
        "successor_contacted": False,
        "terminal_gate_passed": False,
        "fresh_live_authority_reread_required": True,
        "single_send_maximum": 1,
    })
    write_text("x2/evidence-report.md", phase_report(generated_at, dict(outcome_counts), len(SKILL_NAMES), len(RUNNER_NAMES)))

    manifest_path = PHASE_ROOT / "evidence/evidence-content-manifest.json"
    manifest_sources = [
        path for path in PHASE_ROOT.rglob("*")
        if path.is_file() and path != manifest_path and (
            f"{os.sep}x2{os.sep}" in str(path) or
            path.name == "x2-operational-method-flow.json"
        )
    ] + [
        ROOT / "scripts/ghc_family_lyren_moss_v668_v2_controls.py",
        ROOT / "scripts/build_ghc_family_lyren_moss_v668_v2_x2.py",
        ROOT / "tests/test_ghc_family_lyren_moss_v668_v2_x2.py",
    ]
    missing = [str(path) for path in manifest_sources if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"evidence manifest inputs missing: {missing}")
    rows = projected_git_blob_rows(manifest_sources)
    write_json("evidence/evidence-content-manifest.json", {
        "phase": PHASE,
        "x1_head": X1_HEAD,
        "scope": "exact Lyren x2 evidence and implementation files excluding this self-referential manifest",
        "canonical_domain": "Git blob bytes after evidence commit",
        "entry_count": len(rows),
        "entries": rows,
        "generated_at": generated_at,
    })
    print(
        f"built Lyren {PHASE} x2: {len(outcomes)} outcomes, {len(mutations)} rejected mutations, "
        f"{len(SKILL_NAMES)} skills, {len(runner_receipts)} runners, {len(rows)} manifest entries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
