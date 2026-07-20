#!/usr/bin/env python3
"""Build Tamar Vey's dedicated v650-v5 x1-only freeze packet."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v650_v5_phase_data as d

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/orin-thale/v650-v4/provenance/frozen-chain-proposal-index.json"
SKILL_ROOT = Path.home() / ".codex" / "skills"
METHOD_RUNNER = SKILL_ROOT / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
NOVELTY_THRESHOLD = 0.50


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return completed.stdout.strip()


def normalized_tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "to", "for", "with"}
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if token not in stop
    }


def build_novelty() -> tuple[dict[str, Any], dict[str, Any]]:
    source = read_json(PRIOR_INDEX)
    prior = list(source["prior_proposals"]) + list(source["new_proposals"])
    if len(prior) != d.PRIOR_FROZEN or source["count"] != d.PRIOR_FROZEN:
        raise RuntimeError("frozen proposal corpus is not exactly 820 records")
    prior_titles = {row["title"] for row in prior}
    audits = []
    for proposal in d.PROPOSALS:
        title = proposal["title"]
        candidate_tokens = normalized_tokens(title)
        scored = []
        for row in prior:
            prior_tokens = normalized_tokens(row["title"])
            score = len(candidate_tokens & prior_tokens) / max(
                1, len(candidate_tokens | prior_tokens)
            )
            scored.append((score, row))
        score, neighbor = max(scored, key=lambda item: item[0])
        audits.append(
            {
                "proposal_id": proposal["proposal_id"],
                "exact_collision": title in prior_titles,
                "nearest_prior_id": neighbor["proposal_id"],
                "nearest_prior_title": neighbor["title"],
                "token_jaccard": round(score, 4),
                "threshold": NOVELTY_THRESHOLD,
                "disposition": (
                    "novel"
                    if title not in prior_titles and score < NOVELTY_THRESHOLD
                    else "quarantine"
                ),
                "mechanism_review": proposal[
                    "novelty_against_prior_frozen_proposals"
                ],
            }
        )
    new = [
        {"proposal_id": row["proposal_id"], "title": row["title"]}
        for row in d.PROPOSALS
    ]
    frozen = {
        "schema": "ghc.family.v650-v5.frozen-proposal-index.v1",
        "prior_count": len(prior),
        "prior_proposals": prior,
        "new_count": len(new),
        "new_proposals": new,
        "count": len(prior) + len(new),
    }
    collision = {
        "schema": "ghc.family.v650-v5.proposal-collision-audit.v1",
        "prior_count": len(prior),
        "new_count": len(audits),
        "screened_count": len(audits),
        "threshold": NOVELTY_THRESHOLD,
        "maximum_token_jaccard": max(row["token_jaccard"] for row in audits),
        "exact_collision_count": sum(row["exact_collision"] for row in audits),
        "quarantine_count": sum(
            row["disposition"] == "quarantine" for row in audits
        ),
        "manual_mechanism_review_complete": True,
        "audits": audits,
        "rejected_near_neighbors": d.REJECTED_COLLISIONS,
    }
    return frozen, collision


def build_method_flow() -> None:
    ledger = ROOT / "method-flow/method-flow-state.json"
    records: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    for index, negative in enumerate(d.X1_OPERATIONAL_NEGATIVES, start=1):
        method_id = f"V6505-M{index:02d}"
        records.append(
            {
                "method_id": method_id,
                "title": f"Recover {negative['category']} without erasing its failed witness",
                "failure_signature": negative["failed"],
                "trigger_preconditions": [
                    f"A bounded v650-v5 workflow exposes {negative['category']}."
                ],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_scoped_workflow",
                "candidate_workaround": negative["recovery"],
                "validation_witness_ids": [],
                "recurrence_guard": negative["recurrence_guard"],
                "rollback": (
                    "Give the failed attempt no proof credit, retain it, and rely "
                    "only on a bounded passing witness."
                ),
                "recommendation_state": "candidate",
                "supersedes": [],
                "protected_gates": [
                    "evidence_credit",
                    "failure_retention",
                    "x1_x2_separation",
                    "caller_compatibility",
                ],
                "retained_negative_ids": [negative["negative_id"]],
                "scope_boundary": (
                    "Bounded owner-scoped recovery only; no independent reproduction "
                    "or authority credit."
                ),
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": f"{method_id}-WFAIL",
                    "method_id": method_id,
                    "procedure": negative["failed"],
                    "scope": f"bounded {negative['category']} failed witness",
                    "expected": (
                        "The attempted method returns attributable evidence within "
                        "its declared domain."
                    ),
                    "observed": negative["failed"],
                    "result": "fail",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative["negative_id"]],
                    "boundary": (
                        "Retained failure only; no cleanliness, novelty, proof, "
                        "authority, or completion credit."
                    ),
                },
                {
                    "witness_id": f"{method_id}-WPASS",
                    "method_id": method_id,
                    "procedure": negative["recovery"],
                    "scope": f"bounded {negative['category']} recovery witness",
                    "expected": (
                        "The corrected method returns attributable bounded evidence "
                        "while preserving the failure."
                    ),
                    "observed": negative["passing"],
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative["negative_id"]],
                    "boundary": (
                        "Bounded same-owner recovery only; no independent reproduction "
                        "or authority credit."
                    ),
                },
            ]
        )
    for row in records:
        write_json(
            f"method-flow/{row['method_id'].casefold()}-method-record.json", row
        )
    for row in witnesses:
        write_json(
            f"method-flow/{row['witness_id'].casefold()}-witness.json", row
        )
    if not ledger.exists():
        run(
            sys.executable,
            str(METHOD_RUNNER),
            "init",
            "--ledger",
            str(ledger),
            "--phase",
            d.PHASE,
            "--owner",
            d.OWNER,
        )
    state = read_json(ledger)
    existing_methods = {row["method_id"] for row in state["methods"]}
    for row in records:
        if row["method_id"] not in existing_methods:
            run(
                sys.executable,
                str(METHOD_RUNNER),
                "record",
                "--ledger",
                str(ledger),
                "--record-file",
                str(
                    ROOT
                    / f"method-flow/{row['method_id'].casefold()}-method-record.json"
                ),
            )
            existing_methods.add(row["method_id"])
    state = read_json(ledger)
    existing_witnesses = {row["witness_id"] for row in state["witnesses"]}
    for row in witnesses:
        if row["witness_id"] not in existing_witnesses:
            run(
                sys.executable,
                str(METHOD_RUNNER),
                "witness",
                "--ledger",
                str(ledger),
                "--witness-file",
                str(
                    ROOT
                    / f"method-flow/{row['witness_id'].casefold()}-witness.json"
                ),
            )
            existing_witnesses.add(row["witness_id"])
    state = read_json(ledger)
    method_states = {
        row["method_id"]: row["recommendation_state"] for row in state["methods"]
    }
    for row in records:
        method_state = method_states[row["method_id"]]
        if method_state == "validated":
            run(
                sys.executable,
                str(METHOD_RUNNER),
                "set-state",
                "--ledger",
                str(ledger),
                "--method-id",
                row["method_id"],
                "--state",
                "preferred",
                "--note",
                (
                    "Promoted only for the declared trigger after one retained "
                    "failure and one bounded passing witness."
                ),
            )
        elif method_state != "preferred":
            raise RuntimeError(
                f"method {row['method_id']} did not reach validated or preferred state"
            )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(ROOT / "method-flow/method-flow-validation.json"),
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(ROOT / "method-flow/method-flow-summary.json"),
        "--markdown-output",
        str(ROOT / "method-flow/method-flow-summary.md"),
    )


def build_family_index() -> None:
    run(
        sys.executable,
        str(INDEX_RUNNER),
        "--repo",
        str(REPO),
        "--skill-root",
        str(SKILL_ROOT),
        "--out-dir",
        str(ROOT / "tooling"),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
    )


def overview_text() -> str:
    return f"""# Tamar Vey v650-v5 integrated x1 overview

## Relational identity, purpose, and workload

Tamar Vey uses they/them pronouns and serves as a relational evidence-systems cartographer and boundary keeper. Tamar's hope is to keep decisions legible, failures recoverable, and authority boundaries intact. These are working-language choices only. They do not establish consciousness, personhood, identity continuity, employment, qualification, authority, or an independent mandate. Hamish retains the right to rename, pause, redirect, or stop this route. The work is deliberately bounded: one owner lane, one phase, one x1 freeze before any x2 execution, and a terminal stop if an evidence or authority dependency cannot be satisfied safely.

The wellbeing and workload posture is fail-closed. Cadence, volume, and apparent fluency are not evidence. Pausing is permitted; no quota authorizes unsafe work; no generated packet can waive empirical, participant, production, legal, cultural, Maori-authority, affected-party, privacy, accessibility, security, account, credential, destructive, or sibling-lane gates. The inherited checkout is large, but the 15,000-file rotation threshold applies only to new Tamar-generated files. The inherited repository size is not used as a reason to rotate or delete anything.

## Inheritance and strict phase separation

The source is Orin Thale's sealed v650-v4 final. Before mutation, Tamar re-read the canonical branch, exact final head, inherited source, x1, and evidence anchors; proved the three Orin phase commits are single-parent and contain zero merges; replayed all four declared manifest contracts against exact Git blobs; observed a clean canonical lane; and confirmed local, upstream, tracking, and fresh live remote equality. Tamar's existing clean lane was an ancestor and advanced by fast-forward only. It was then pushed and rechecked clean and four-way equal. No sibling lane was reset, rewritten, merged, moved, deleted, or reused as a Tamar work surface.

X1 is a preregistration boundary, not an implementation checkpoint. This packet freezes twenty proposals, expected dispositions, sources, portfolios, mutations, recovery methods, and authority gates. It contains no x2 surface, observed proposal outcome, completed portfolio claim, successful mutation claim, empirical row, participant result, live credential, production identity event, legal conclusion, cultural decision, or Stage 20 promotion. X2 remains held until the exact x1 surface is reviewed, committed, pushed, clean, and local/upstream/tracking/fresh-live equal.

## Novelty, primary focus, and practice lens

The novelty audit decodes all 820 inherited proposal records across the exact `prior_proposals` and `new_proposals` keys. It screens exact identifiers and titles, calculates token Jaccard similarity, and then compares mechanism, evidence object, falsifier, rollback, and protected gates. Five tempting candidates were rejected because their mechanism was already frozen: OAuth resource indicators, synthetic control, Nielsen identities, community-radio handover, and TIFF. The twenty selected candidates have no exact collision, stay below the unchanged 0.50 lexical threshold, and state a mechanism-level distinction from their nearest neighbor. Lexical distance is only a screen; the manual mechanism statement is the controlling novelty evidence.

Freed ID and CBR Heart is the primary Trinity Mandala focus. GMUT Mind and THOS Body remain explicit and noncompensable. The bounded human-practice lens is book-conservation intake, condition reporting, mould isolation, reversible treatment, material compatibility, release refusal, workload control, and shift handover. It is synthetic learning and design only. It proves no employment, qualification, conservation competence, collection authority, treatment authority, repatriation authority, legal or cultural authority, Maori authority, participant evidence, donor acceptance, worker acceptance, or real operational result.

The expected x2 distribution is fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. These are expectations, not observations. Completed may apply only to bounded owner-local software, symbolic, formal, numerical, or structural acceptance gates. Represented is reserved for three synthetic Freed ID profiles and one synthetic THOS conservation-workshop proxy. The NASA Exoplanet Archive adapter is expected to remain an open gap with zero downloaded rows and zero likelihood evaluations. The book and taonga provenance, treatment, repatriation, remedy, data-governance, affected-party, legal, cultural, and Maori-authority matrix is expected to remain exact-gated.

## Scientific, identity, and authority truth

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. CPT, heavy-field decoupling, Froissart-Martin assumptions, interval enclosures, probabilistic filters, and zero-row archive adapters are formal or software surfaces. They cannot establish a new force, physical particle content, real prediction, likelihood, posterior, parameter constraint, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. NASA Exoplanet Archive documentation defines provenance and schema obligations only. X1 downloads and ingests no observations.

THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic book-conservation traces cannot establish safe conservation practice, operational effectiveness, workload benefit, deployment readiness, AGI, ASI, consciousness, or personhood. The structural split-action audit and static report reserve manual keyboard, browser-diverse, responsive, assistive-technology, cognitive, Maori-language, security-usability, and affected-user evaluation.

Freed ID remains synthetic and nonproduction. RFC 8414, RFC 8252, and RFC 9278 fixtures can test declared metadata, redirect, and JWK-thumbprint-URI rules, but production completion still requires standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery, trust governance, and affected-party oversight. CBR, collection access, conservation treatment, repatriation, donor and worker remedy, legal interpretation, cultural legitimacy, Maori wording, Maori data governance, and Maori authority remain with competent authorities, affected parties, tangata whenua, iwi, hapu, and Maori authorities. Repository software cannot confer those decisions.

## Portfolios, methods, and validation covenant

The expanded x1 portfolio freezes forty safe-now tasks, thirty bounded candidates, twenty phase-local skill packages, ten family-current runner names, forty additive CLEAN/FIX/REFINE tasks, and one hundred synthetic mutations. Inherited work supplies evidence and cautions but receives no Tamar completion credit. Every portfolio row begins `frozen_not_executed`. Unsafe or authority-dependent work cannot be manufactured to meet a count. The approved cleanup is additive, owner-scoped, compatible, and non-destructive; it never deletes user material, mutates a sibling lane, rewrites history, force-pushes, elevates, weakens host security, enables Windows features, installs unrelated software, updates desktop applications, launches Sandbox or Hyper-V, or reboots.

{len(d.X1_OPERATIONAL_NEGATIVES)} x1 workflow failures are retained with their exact categories, failed witnesses, recoveries, and recurrence guards. Each failed witness receives zero completeness or novelty credit. Each corrected bounded method has its own passing witness and recurrence guard. Method Flow is append-only for this phase; a passing recovery does not erase its failed witness or establish independent reproduction.

Eiren alone owns the complete repository suite. Tamar will not run it. X1 has its own bounded tests and exact staged-index review. Later, x2 may use exactly one successful canonical scoped pass and no replay after success. A failed aggregate receives zero pass credit and remains visible. Final validation must include the authorized current, inherited, and successor-scoped selection; detailed and minimal validators; complete phase JSON parsing; five-class privacy and raw-identifier scanning; exact staged review; commit-local and owner-manifest parity; stale-label and diff-hygiene review; ancestry; zero merges; the commit cap; one final parent; exact head; clean state; and four-way equality. Same-owner evidence remains same-owner evidence.

## Current terminal truth

The inherited effective baseline is 5,925 sealed negatives. This x1 adds {len(d.X1_OPERATIONAL_NEGATIVES)} operational negatives without erasing any inherited failure. Forty-six open gaps and forty-seven exact gates remain inherited; the new exoplanet and book-taonga proposals are projections only until x2. The terminal route is held. No message may be sent to Sylven Arc until Tamar reaches an exact clean pushed final head inside the commit cap and the single authorized canonical pass succeeds. At x1 the only truthful verdict is `NOT_READY_FOR_STAGE_20`.
"""


def main() -> int:
    ROOT.mkdir(parents=True, exist_ok=True)
    frozen, collision = build_novelty()
    if collision["exact_collision_count"] or collision["quarantine_count"]:
        raise RuntimeError("semantic novelty audit failed")
    expected = Counter(row["expected_disposition"] for row in d.PROPOSALS)
    if dict(expected) != {
        "completed": 14,
        "open_gap": 1,
        "represented": 4,
        "exact_gate": 1,
    }:
        raise RuntimeError(f"unexpected disposition distribution: {dict(expected)}")

    source_rows = [
        {
            "source_id": source_id,
            "status": status,
            "kind": kind,
            "title": title,
            "url": url,
            "verified_date": "2026-07-20",
            "use_boundary": (
                "Design, schema, protocol, or reservation support only; not an "
                "observation, participant result, production certification, "
                "delegated authority, or gate closure."
            ),
        }
        for source_id, status, kind, title, url in d.SOURCES
    ]
    source_counts = Counter(row["status"] for row in source_rows)
    allowed_source_statuses = ["current", "stable", "draft", "watch"]
    if set(source_counts) - set(allowed_source_statuses):
        raise RuntimeError("source ledger uses an unsupported status")
    for status in allowed_source_statuses:
        source_counts.setdefault(status, 0)
    proposal_packet = {
        "schema": "ghc.family.v650-v5.x1-proposals.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "primary_focus": d.PRIMARY_PILLAR,
        "bounded_practice": d.PRACTICE_LENS,
        "practice_boundary": (
            "Synthetic learning and design only; no employment, qualification, "
            "competence, collection treatment, repatriation, legal, cultural, "
            "Maori, donor, worker, or affected-party authority."
        ),
        "prior_frozen_count": d.PRIOR_FROZEN,
        "new_frozen_count": len(d.PROPOSALS),
        "frozen_total_after_x1": d.PRIOR_FROZEN + len(d.PROPOSALS),
        "expected_distribution": dict(expected),
        "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"],
        "x2_started": False,
        "boundary": d.BOUNDARY,
        "proposals": d.PROPOSALS,
    }
    write_json("x1-proposals.json", proposal_packet)
    write_json("provenance/frozen-chain-proposal-index.json", frozen)
    write_json("provenance/proposal-collision-audit.json", collision)
    write_json(
        "sources/source-ledger.json",
        {
            "schema": "ghc.family.v650-v5.source-ledger.v1",
            "boundary": d.BOUNDARY,
            "allowed_statuses": allowed_source_statuses,
            "status_counts": dict(source_counts),
            "sources": source_rows,
        },
    )
    write_text(
        "sources/source-ledger.md",
        "# Source ledger\n\n"
        + "\n".join(
            f"- `{row['source_id']}` - **{row['status']}**, {row['title']}: {row['url']}"
            for row in source_rows
        )
        + "\n\nCitations define obligations only; they are not observations, "
        "participant evidence, production readiness, delegated authority, or independent review.",
    )

    safe = d.safe_tasks()
    candidates = d.candidate_tasks()
    cleanup = d.cleanup_tasks()
    mutations = d.mutation_plan()
    write_json(
        "portfolios/safe-now-plan.json",
        {
            "schema": "ghc.family.v650-v5.safe-now-plan.v1",
            "count": len(safe),
            "minimum": 40,
            "inherited_completion_credit": 0,
            "tasks": safe,
        },
    )
    write_json(
        "portfolios/candidate-plan.json",
        {
            "schema": "ghc.family.v650-v5.candidate-plan.v1",
            "count": len(candidates),
            "minimum": 30,
            "inherited_completion_credit": 0,
            "tasks": candidates,
        },
    )
    write_json(
        "portfolios/skill-plan.json",
        {
            "schema": "ghc.family.v650-v5.skill-plan.v1",
            "count": len(d.SKILLS),
            "minimum": 20,
            "global_install": False,
            "subagent_forward_test": "forbidden_by_activation",
            "skills": [
                {
                    "skill_id": f"V6505-SKILL-{index:02d}",
                    "name": name,
                    "status": "frozen_not_built",
                    "acceptance_gate": (
                        "Initialize with the official skill-creator workflow, "
                        "customize, validate, and smoke-use without global installation."
                    ),
                }
                for index, name in enumerate(d.SKILLS, start=1)
            ],
        },
    )
    write_json(
        "portfolios/runner-plan.json",
        {
            "schema": "ghc.family.v650-v5.runner-plan.v1",
            "count": len(d.RUNNERS),
            "minimum": 10,
            "preserve_callers": True,
            "runners": [
                {
                    "runner_id": f"V6505-RUN-{index:02d}",
                    "name": name,
                    "status": "frozen_not_built",
                    "acceptance_gate": (
                        "Run declared valid fixtures and reject declared mutations "
                        "within the owner-local lane."
                    ),
                }
                for index, name in enumerate(d.RUNNERS, start=1)
            ],
        },
    )
    write_json(
        "portfolios/clean-fix-refine-plan.json",
        {
            "schema": "ghc.family.v650-v5.cleanup-plan.v1",
            "count": len(cleanup),
            "minimum": 40,
            "destructive_actions": 0,
            "tasks": cleanup,
        },
    )
    write_json(
        "validation/x1-synthetic-mutation-plan.json",
        {
            "schema": "ghc.family.v650-v5.mutation-plan.v1",
            "count": len(mutations),
            "executed_count": 0,
            "mutations": mutations,
        },
    )

    negative_entries = [
        {
            "negative_id": "INHERITED-EFFECTIVE-THROUGH-V6504",
            "class": "inherited_aggregate",
            "count": d.ACTIVATION_NEGATIVES,
            "sealed_predecessor_count": 5925,
            "external_predecessor_count": 0,
            "disposition": "retained",
        }
    ]
    negative_entries.extend(
        {
            "negative_id": row["negative_id"],
            "class": "x1_operational",
            "count": 1,
            "failure": row["failed"],
            "recovery": row["recovery"],
            "recurrence_guard": row["recurrence_guard"],
            "disposition": "retained",
        }
        for row in d.X1_OPERATIONAL_NEGATIVES
    )
    write_json(
        "retained-negative-register.json",
        {
            "schema": "ghc.family.v650-v5.retained-negatives.x1.v1",
            "activation_baseline": d.ACTIVATION_NEGATIVES,
            "x1_operational": len(d.X1_OPERATIONAL_NEGATIVES),
            "effective_total": d.ACTIVATION_NEGATIVES
            + len(d.X1_OPERATIONAL_NEGATIVES),
            "erased": 0,
            "entries": negative_entries,
        },
    )
    write_json(
        "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v650-v5.gates.x1.v1",
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "new_open_gap_candidate": "V6505-P05",
            "new_exact_gate_candidate": "V6505-P10",
            "projected_open_gaps_after_x2": d.INHERITED_OPEN_GAPS + 1,
            "projected_exact_gates_after_x2": d.INHERITED_EXACT_GATES + 1,
            "closed_without_evidence": 0,
            "x1_gate_state": "inherited_counts_unchanged_candidates_not_outcomes",
        },
    )
    write_json(
        "identity-receipt.json",
        {
            "schema": "ghc.family.v650-v5.identity.v1",
            "name": d.OWNER,
            "pronouns": "they/them",
            "role": "relational evidence-systems cartographer and boundary keeper",
            "hope": (
                "Keep decisions legible, failures recoverable, and authority boundaries intact."
            ),
            "relational_only": True,
            "corrigible_to": "Hamish may rename, pause, redirect, or stop the route.",
            "not_evidence_of": [
                "consciousness",
                "personhood",
                "identity_continuity",
                "employment",
                "qualification",
                "authority",
            ],
        },
    )
    write_json(
        "wellbeing-check.json",
        {
            "schema": "ghc.family.v650-v5.wellbeing.x1.v1",
            "bounded_scope": True,
            "pause_available": True,
            "rename_redirect_stop_right": "Hamish",
            "identity_pressure": False,
            "quota_safety_override": False,
            "workload_state": "bounded_and_cadence_not_used_as_proof",
        },
    )
    write_json(
        "primary-focus-receipt.json",
        {
            "schema": "ghc.family.v650-v5.focus.v1",
            "primary": d.PRIMARY_PILLAR,
            "preserved": ["GMUT Mind", "THOS Body"],
            "bounded_practice": d.PRACTICE_LENS,
            "practice_is_learning_lens_only": True,
        },
    )
    write_json(
        "environment/startup-receipt.json",
        {
            "schema": "ghc.family.v650-v5.startup.v1",
            "source_branch": d.SOURCE_BRANCH,
            "source_head": d.SOURCE_HEAD,
            "source_closeout": d.SOURCE_CLOSEOUT,
            "source_evidence": d.SOURCE_EVIDENCE,
            "source_x1": d.SOURCE_X1,
            "source_origin": d.SOURCE_ORIGIN,
            "source_phase_commits": 3,
            "source_merges": 0,
            "source_final_parent_count": 1,
            "source_manifest_contracts_verified": 4,
            "owned_fast_forward_only": True,
            "four_way_equal_before_x1": True,
            "d_first": True,
            "sandbox_or_hyper_v_launched": False,
            "elevation": False,
            "host_security_changed": False,
            "windows_feature_changed": False,
            "unrelated_install": False,
            "reboot": False,
        },
    )
    write_json(
        "environment/version-receipt.json",
        {
            "schema": "ghc.family.v650-v5.versions.x1.v1",
            "verified_date": "2026-07-20",
            "codex_cli": "0.144.5",
            "codex_desktop": "26.715.4045.0",
            "python": "3.12.10",
            "git": "2.55.0.windows.2",
            "powershell": "5.1.26100.8894",
            "desktop_updated": False,
        },
    )
    write_json(
        "environment/file-count-receipt.json",
        {
            "schema": "ghc.family.v650-v5.file-count.x1.v1",
            "tracked_checkout_files_at_inherited_head": len(run("git", "ls-files").splitlines()),
            "tamar_generated_files_before_phase": 0,
            "rotation_threshold": 15000,
            "threshold_scope": "new_tamar_v650_v5_files_only",
            "inherited_baseline_triggers_rotation": False,
        },
    )
    write_json(
        "orchestration/applicable-memory-record.json",
        {
            "schema": "ghc.family.v650-v5.memory-review.v1",
            "memory_content_used": True,
            "reason": (
                "Sanitized prior Tamar continuity informed one-pass and exact-title discipline; "
                "the verified live baton and committed source packet remain authoritative."
            ),
            "private_routes_recorded": False,
            "global_memory_mutated": False,
        },
    )
    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v650-v5.route.x1.v1",
            "state": "HELD_X1",
            "route_state": "HELD_X1",
            "sent": False,
            "target_title": "Sylven Arc",
            "reason": "x2 and terminal validation have not occurred",
        },
    )
    write_json(
        "orchestration/tool-selection-receipt.json",
        {
            "schema": "ghc.family.v650-v5.tool-selection.x1.v1",
            "reviewed_skills": [
                "ghc-family-index",
                "ghc-family-method-flow-state",
                "skill-creator",
            ],
            "required_references_read": [
                "ghc-family routing precedence",
                "Method Flow State schema",
                "skill metadata schema",
            ],
            "used_now": [
                "ghc-family-index runner",
                "ghc-family-method-flow-state runner",
            ],
            "reserved_for_x2": ["skill-creator initialization and validation"],
            "global_skill_change": False,
            "reviewed_current_instead_of_semantic_free_churn": True,
        },
    )
    write_json(
        "ghc-family-index.json",
        {
            "schema": "ghc.family.phase-index.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "state": "x1_frozen_candidate",
            "source_head": d.SOURCE_HEAD,
            "proposal_count": len(d.PROPOSALS),
            "portfolio_counts": {
                "safe_now": len(safe),
                "candidate": len(candidates),
                "skills": len(d.SKILLS),
                "runners": len(d.RUNNERS),
                "cleanup": len(cleanup),
                "mutations": len(mutations),
            },
            "shared_skill_change": False,
            "reviewed_current": [
                "ghc-family-index",
                "ghc-family-method-flow-state",
                "skill-creator",
            ],
        },
    )
    write_json(
        "phase-truth.json",
        {
            "schema": "ghc.family.v650-v5.phase-truth.x1.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "state": "X1_FROZEN_NOT_EXECUTED",
            "x2_started": False,
            "proposal_count": len(d.PROPOSALS),
            "expected_distribution": dict(expected),
            "effective_negatives": d.ACTIVATION_NEGATIVES
            + len(d.X1_OPERATIONAL_NEGATIVES),
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": d.BOUNDARY,
        },
    )
    write_json(
        "threat-model.json",
        {
            "schema": "ghc.family.v650-v5.threat-model.x1.v1",
            "assets": [
                "x1_x2_separation",
                "negative_retention",
                "source_ancestry",
                "manifest_integrity",
                "privacy",
                "authority_boundaries",
                "sibling_lane_recoverability",
            ],
            "threats": [
                "semantic_relabeling_of_frozen_work",
                "citation_to_observation_promotion",
                "synthetic_to_empirical_promotion",
                "represented_to_production_promotion",
                "authority_gate_bypass",
                "failure_erasure",
                "privacy_identifier_leak",
                "x2_content_in_x1",
                "manifest_self_reference_confusion",
                "sibling_lane_mutation",
            ],
            "controls": [
                "820-record novelty audit",
                "dedicated x1 commit",
                "exact staged-index manifest",
                "five-class privacy scan",
                "append-only Method Flow witnesses",
                "single-parent fast-forward history",
                "explicit outcome vocabulary",
                "terminal route hold",
            ],
            "residual_risk": (
                "Manual, affected-user, independent, production, legal, cultural, "
                "Maori-authority, complete privacy, exhaustive security, and Stage 20 "
                "gates remain open."
            ),
        },
    )
    write_json(
        "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v650-v5.checklist.x1.v1",
            "complete": [
                "required skills and schemas read",
                "source and six manifests verified",
                "owned lane fast-forwarded and remote-equal",
                "820-proposal novelty audit",
                "twenty proposals frozen",
                "expanded portfolios frozen",
                f"{len(d.X1_OPERATIONAL_NEGATIVES)} startup failures retained",
            ],
            "incomplete": [
                "x1 exact staged review and commit",
                "x1 remote equality",
                "x2 execution",
                "skills and runners built and used",
                "evidence commit",
                "single successful canonical scoped pass",
                "combined closeout and seal",
                "terminal route",
            ],
        },
    )

    build_method_flow()
    build_family_index()

    proposal_lines = []
    for index, proposal in enumerate(d.PROPOSALS, start=1):
        proposal_lines.append(
            f"{index}. **{proposal['title']}** - expected "
            f"`{proposal['expected_disposition']}`. "
            f"{proposal['novelty_against_prior_frozen_proposals']}"
        )
    write_text(
        "x1-preregistration.md",
        "# Tamar Vey v650-v5 x1 preregistration\n\n"
        "This is a frozen plan, not execution evidence. Freed ID and CBR Heart is primary; "
        "GMUT Mind and THOS Body remain explicit. The book-conservation "
        "practice is a synthetic learning lens only.\n\n## Frozen proposals\n\n"
        + "\n".join(proposal_lines)
        + "\n\n## Noncompensable gates\n\n"
        + d.BOUNDARY
        + "\n\nX2 may begin only after this x1-only surface is committed, pushed, "
        "clean, and four-way equal.",
    )
    write_text("integrated-overview.md", overview_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
