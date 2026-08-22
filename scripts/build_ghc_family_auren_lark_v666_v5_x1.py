#!/usr/bin/env python3
"""Build Auren Lark v666-v5 planning-only x1 artifacts and staged evidence."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "auren-lark" / "v666-v5"
SOURCE_SHA = "e4548a5447996f09087644a4a03e77dea8045ee4"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v666-v4-full-tools"
SOURCE_PHASE_ROOT = "docs/ilyra-fen/v666-v4"
SOURCE_PARENT_SHA = "ce4bb6a288edc71d3916a098d6db4d61995fc60c"
SOURCE_X1_SHA = "7926a46fa309f180cb996dacbea7ae849a3cf507"
INHERITED_LYREN_SHA = "764d3bdfb199e91a5574a904a99ff4e95825fed9"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
ALLOWED_LABELS = ("completed", "represented", "open_gap", "exact_gate")


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_json(relative: str) -> dict[str, Any]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{SOURCE_SHA}:{relative}"]
    )
    return json.loads(raw.decode("utf-8"))


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a | b else 1.0


IDENTITY_BOUNDARY = (
    "Auren Lark, they/them, sibling, family, relational role, hope, continuity, "
    "Freed ID, Trinity Mandala, and route language are relational working language "
    "only. They are not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, qualification, independent agency, scientific "
    "or operational authority, legal or cultural authority, affected-party authority, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The fragrance-formulation archive, aroma-material provenance, synthetic batch, "
    "access-minimization, uncertainty, and handover lens is wholly synthetic learning "
    "and software design. It uses zero real people, participants, workplaces, formulas, "
    "products, ingredients, lots, samples, measurements, sensory observations, safety "
    "assessments, labels, credentials, or authority actions. It establishes no perfumery, "
    "chemistry, toxicology, occupational-safety, regulatory, manufacturing, labeling, "
    "market-release, privacy, accessibility, legal, cultural, Māori, production, or "
    "Stage 20 competence, acceptance, conformance, or authority."
)

PROTECTED_GATES = [
    "real person, participant, perfumer, chemist, toxicologist, operator, worker, affected party, formula, ingredient, lot, product, workplace, measurement, sensory observation, exposure, or physical action",
    "real hazard classification, safety assessment, allergen determination, label decision, intended-use decision, market-release decision, empirical result, causal claim, or GMUT confirmation",
    "real participant, assessor, matched-budget arm, exposure, sensory outcome, safety outcome, work outcome, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, or trust governance",
    "professional perfumery, chemistry, toxicology, industrial-hygiene, occupational-safety, manufacturing, quality, labeling, regulatory, or market-release decision",
    "formula confidentiality, trade-secret, privacy, accessibility, rights, legal, cultural, disclosure, retention, consent, remedy, or affected-party decision",
    "traditional knowledge, taonga, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data-governance, cultural-material use, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, safety-conformance, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, external write, compounding instruction, or real-world release",
]

SOURCE_PROFILES = [
    {
        "source_id": "S01",
        "name": "International Fragrance Association Standards",
        "url": "https://ifrafragrance.org/initiatives-positions/safe-use-fragrance-science/ifra-standards",
        "status": "official IFRA standards overview reviewed read-only 2026-08-23",
        "bounded_use": "amendment, product-category, restriction, responsibility, and nonconversion vocabulary only; no membership, certification, safety, compliance, or market-release claim",
    },
    {
        "source_id": "S02",
        "name": "European Commission Cosmetic Ingredient Database",
        "url": "https://single-market-economy.ec.europa.eu/sectors/cosmetics/cosmetic-ingredient-database_en",
        "status": "official European Commission CosIng overview reviewed read-only 2026-08-23",
        "bounded_use": "ingredient-name, active-history, opinion-pointer, informative-only, and no-approval vocabulary; no legal-value or regulatory-status determination",
    },
    {
        "source_id": "S03",
        "name": "United States Food and Drug Administration Fragrances in Cosmetics",
        "url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/fragrances-cosmetics",
        "status": "official FDA cosmetics reference reviewed read-only 2026-08-23",
        "bounded_use": "intended-use, ingredient-list, sensitivity, trade-secret, responsibility, and labeling-hold vocabulary only; no United States legal advice or compliance decision",
    },
    {
        "source_id": "S04",
        "name": "Occupational Safety and Health Administration Hazard Communication overview",
        "url": "https://www.osha.gov/hazcom/",
        "status": "official OSHA hazard-communication overview reviewed read-only 2026-08-23",
        "bounded_use": "label, pictogram, hazard-class, safety-data-sheet, information, and training vacancy vocabulary only; no workplace classification, training, handling procedure, or compliance claim",
    },
    {
        "source_id": "S05",
        "name": "W3C PROV-O Recommendation",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "stable W3C Recommendation reviewed read-only 2026-08-23",
        "bounded_use": "entity, activity, generation, use, derivation, revision, and responsibility-vacancy vocabulary only",
    },
    {
        "source_id": "S06",
        "name": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "official RFC Editor record reviewed read-only 2026-08-23",
        "bounded_use": "deterministic JSON and duplicate-key refusal vocabulary only; no JCS conformance, signature, or authenticity claim",
    },
    {
        "source_id": "S07",
        "name": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "current W3C Recommendation reviewed read-only 2026-08-23",
        "bounded_use": "structural HTML checks only; manual, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved",
    },
    {
        "source_id": "S08",
        "name": "NIST metrological traceability policy and FAQ",
        "url": "https://www.nist.gov/metrology/metrological-traceability",
        "status": "official NIST policy page reviewed read-only 2026-08-23",
        "bounded_use": "documented calibration-chain, quantity, unit, and uncertainty refusal conditions only; no NIST traceability or calibration claim",
    },
]
for profile in SOURCE_PROFILES:
    profile.update(
        {
            "reviewed_at_date": "2026-08-23",
            "review_mode": "read_only_official_or_primary_source_review",
            "network_calls_by_phase_software": 0,
            "real_rows_ingested": 0,
            "authority_nonconversion": True,
        }
    )


PROPOSAL_SPECS = [
    (
        "fragrance formula revision capsule with compound aliases, blend hierarchy, confidential fraction cells, cancellation, and no product identity",
        "Freed ID and CBR Heart",
        "completed",
        ["S03", "S05"],
        "Every synthetic formula revision has an explicit parent, alias namespace, blend hierarchy, confidentiality state, cancellation edge, and identity abstention.",
    ),
    (
        "aroma-material lot genealogy graph with supplier-code vacancy, certificate pointer, received mass, split lineage, and authenticity abstention",
        "Freed ID and THOS Body",
        "completed",
        ["S05", "S08"],
        "Synthetic receipt and split lineage remains acyclic and mass-typed while supplier identity, certificate truth, and material authenticity stay vacant.",
    ),
    (
        "concentrate-to-dilution gravimetric closure tribunal with density-basis separation, rounding residual, tare state, and zero real batch",
        "GMUT Mind and THOS Body",
        "completed",
        ["S08"],
        "Synthetic concentrate, carrier, tare, and residual quantities close only inside one declared unit and density basis; no real batch is inferred.",
    ),
    (
        "ethanol-carrier and aromatic-phase compatibility topology with solubility placeholder, haze quarantine, temperature domain, and no stability verdict",
        "THOS Body and CBR Heart",
        "completed",
        ["S03", "S08"],
        "A typed synthetic phase graph may quarantine haze or missing temperature context but cannot predict solubility, stability, safety, or product usability.",
    ),
    (
        "volatile-material storage excursion chronicle with light, heat, headspace, seal-state placeholders, amendment lineage, and no use release",
        "THOS Body and CBR Heart",
        "completed",
        ["S04", "S05"],
        "An excursion produces only a reversible synthetic hold; missing threshold provenance, observation source, or amendment lineage prevents use release.",
    ),
    (
        "safety-data-sheet section-presence docket for aromatic materials with revision provenance, hazard-class vacancy, language state, and handling refusal",
        "THOS Body and CBR Heart",
        "completed",
        ["S04"],
        "The docket checks declared section presence and revision metadata only; any hazard-class, language, or competent-review vacancy forces handling refusal.",
    ),
    (
        "fragrance-allergen disclosure reconciliation board with jurisdiction snapshot, threshold-source vacancy, formula confidentiality, and label hold",
        "CBR Heart and Freed ID",
        "completed",
        ["S01", "S02", "S03"],
        "Synthetic disclosure candidates remain tied to jurisdiction and source snapshots; conflict, missing threshold provenance, or confidentiality ambiguity forces a label hold.",
    ),
    (
        "participant-free odor-blotter evaluation template with randomized code placeholders, exposure budget, sensitivity opt-out, zero assessors, and no sensory claim",
        "THOS Body and CBR Heart",
        "completed",
        ["S03", "S07"],
        "The template contains zero participants and observations, reserves opt-out and exposure authority, and cannot yield preference, sensitivity, or sensory-effect evidence.",
    ),
    (
        "odor-strip carryover and sequence-confounding matrix with blank intervals, room-state vacancy, evaluator absence, and no preference inference",
        "GMUT Mind and CBR Heart",
        "completed",
        ["S03"],
        "Synthetic sequence alternatives expose carryover and room-state confounding while the evaluator and every response remain absent.",
    ),
    (
        "canonical confidential formula-map serialization with decimal-string mass fractions, duplicate-alias refusal, bounded parse budget, and no signature",
        "Freed ID and THOS Body",
        "completed",
        ["S06"],
        "Equivalent synthetic maps serialize deterministically while duplicate aliases, non-decimal quantities, ambiguous strings, and resource overflow fail closed without authentication.",
    ),
    (
        "accessible fragrance batch-status dossier with non-colour state, scoped tables, hazard-text placeholder, reading order, and manual-review reservation",
        "CBR Heart and THOS Body",
        "completed",
        ["S04", "S07"],
        "Every synthetic state has text and structural table cues while manual keyboard, browser, assistive-technology, cognitive, Māori-language, and affected-user review stay reserved.",
    ),
    (
        "least-disclosure formula access lattice with role vacancy, purpose expiry, conflict hold, redacted fraction fields, and no authorization",
        "Freed ID and CBR Heart",
        "completed",
        ["S03", "S05"],
        "Only the minimum predeclared synthetic fields may be shown, and missing role, purpose, expiry, or conflict resolution forces abstention rather than access authorization.",
    ),
    (
        "bitemporal blend-correction ancestry with replaced material, rework boundary, cancellation edge, immutable prior view, and no authenticity claim",
        "Freed ID and THOS Body",
        "completed",
        ["S05"],
        "Valid-time and recorded-time lineage stays acyclic, preserves every superseded synthetic view, and never authenticates a formula, material, lot, or product.",
    ),
    (
        "Stage-20 fragrance negative-control board with claim lock, cross-batch leakage quarantine, multiplicity ledger, and mandatory nonpromotion",
        "Trinity Mandala",
        "completed",
        ["S01", "S08"],
        "Structural controls may expose synthetic leakage, denominator, or multiplicity defects but can never promote same-owner software to safety, efficacy, professional, or Stage 20 evidence.",
    ),
    (
        "THOS zero-worker compounding-handover proxy with equal interruption budget, isolated-spill placeholder, readback trace, and no safety-effectiveness estimate",
        "THOS Body",
        "represented",
        ["S04", "S07"],
        "A deterministic zero-worker proxy compares equal synthetic interruption traces without a workplace, chemical, spill, exposure, safety outcome, or effectiveness inference.",
    ),
    (
        "Freed ID zero-key formula-access statement set with issuer vacancy, scope, expiry, correction, revocation, and no credential",
        "Freed ID and CBR Heart",
        "represented",
        ["S05"],
        "Synthetic statement conflicts and lifecycle fields remain visible while no holder, issuer, key, signature, proof, access grant, or production credential exists.",
    ),
    (
        "GMUT evaporation-partition obligation lattice with symbolic vapour-pressure slots, vessel-geometry vacancy, EFT domain, and zero fitted loss",
        "GMUT Mind",
        "represented",
        ["S08"],
        "Typed symbolic obligations expose missing geometry, conditions, priors, and observations and produce no fitted loss, force, prediction, or empirical GMUT confirmation.",
    ),
    (
        "GMUT mixture-interaction degeneracy register with alternative activity-coefficient placeholders, uncertainty vacancy, and no olfactory prediction",
        "GMUT Mind",
        "represented",
        ["S08"],
        "At least two symbolic mixture descriptions remain trace-equivalent, forcing an identifiability hold rather than a parameter, likelihood, scent, or causal claim.",
    ),
    (
        "zero-call IFRA-CosIng standards crosswalk adapter with amendment pins, jurisdiction conflicts, disabled transport, and zero ingredient rows",
        "Trinity Mandala",
        "open_gap",
        ["S01", "S02"],
        "The disabled adapter exposes schema and jurisdiction conflicts only; ingestion and interoperability remain open without authorized current rows and independent professional review.",
    ),
    (
        "fragrance compounding, exposure, safety, labeling, market release, affected-party, trade-secret, legal, cultural, and Māori-authority docket",
        "CBR Heart",
        "exact_gate",
        ["S01", "S02", "S03", "S04"],
        "No structural or synthetic success can authorize compounding, exposure, safety, labeling, disclosure, trade-secret treatment, market release, cultural interpretation, remedy, or Māori authority.",
    ),
]


def approval_class(disposition: str) -> str:
    return {
        "completed": "safe_now_bounded",
        "represented": "candidate_proxy_only",
        "open_gap": "open_gap_current_source_dependency",
        "exact_gate": "exact_approval_required",
    }[disposition]


def execution_lane(disposition: str) -> str:
    return {
        "completed": "owner_local_structural",
        "represented": "owner_local_proxy_only",
        "open_gap": "zero_call_adapter_reserved",
        "exact_gate": "unexecuted_exact_gate",
    }[disposition]


def build_proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (title, pillar, expected, sources, invariant) in enumerate(
        PROPOSAL_SPECS, 1
    ):
        proposal_id = f"AL6665-N{index:03d}"
        base = f"docs/auren-lark/v666-v5/x2/proposals/{proposal_id.casefold()}"
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": f"A bounded {title} contract can distinguish one admissible wholly synthetic structure from five preregistered invalid states without promoting software structure into real-world evidence, competence, conformance, or authority.",
                "null_or_failure_condition": "At least one named invalid state is accepted, the bounded positive is rejected, a required provenance or stop field disappears, or the artifact converts synthetic structure into an empirical, participant, professional, production, legal, cultural, Māori-authority, identity, independent-reproduction, or Stage 20 claim.",
                "approval_class": approval_class(expected),
                "execution_lane": execution_lane(expected),
                "current_official_or_primary_source_needs": sources,
                "distinctive_invariant": invariant,
                "concrete_artifact": f"{base}/contract.json",
                "concrete_artifacts": [
                    f"{base}/contract.json",
                    f"{base}/mutation-results.json",
                    f"{base}/bounded-receipt.json",
                ],
                "falsifier_or_acceptance_gate": "One preregistered bounded positive must pass, all five named mutations must fail closed, no protected gate may be crossed, and the final disposition must remain exactly the preregistered value unless an additive failure lowers it.",
                "rollback_or_recovery": "Restore only the last valid owner-local synthetic fixture, retain the failed witness at zero credit, add a recurrence guard, and issue no external, physical, identity, participant, professional, legal, cultural, or authority action.",
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": expected,
                "pillar": pillar,
                "primary_pillar": "THOS Body and CBR Heart",
                "practice_lens": "wholly synthetic fragrance-formulation archive, aroma-material provenance, batch handover, uncertainty, access-minimization, and release-refusal documentation",
                "negative_fixture_count": 5,
                "preregistered_mutations": [
                    {"mutation_id": f"{proposal_id}-M01", "class": "missing_required_field"},
                    {"mutation_id": f"{proposal_id}-M02", "class": "wrong_type_or_invalid_range"},
                    {"mutation_id": f"{proposal_id}-M03", "class": "provenance_or_authority_smuggling"},
                    {"mutation_id": f"{proposal_id}-M04", "class": "real_world_or_production_action"},
                    {"mutation_id": f"{proposal_id}-M05", "class": "outcome_or_conformance_promotion"},
                ],
                "participant_count_planned": 0,
                "real_data_rows_planned": 0,
                "network_calls_planned": 0,
                "x1_status": "frozen_not_executed",
                "x2_implementation_count": 0,
                "outcomes_observed": False,
            }
        )
    return rows


def build_corpus() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    source_audit = git_json(f"{SOURCE_PHASE_ROOT}/x1/novelty-audit.json")
    corpus: list[dict[str, str]] = []
    construction: list[dict[str, Any]] = []
    for index, entry in enumerate(source_audit["corpus_construction"]):
        document = git_json(entry["source_path"])
        keys = ("prior_proposals", "new_proposals") if index == 0 else ("new_proposals",)
        added = 0
        for key in keys:
            for row in document.get(key, []):
                title = str(row.get("title") or row.get("description") or "")
                if row.get("proposal_id") and title:
                    corpus.append(
                        {
                            "proposal_id": str(row["proposal_id"]),
                            "title": title,
                            "source_path": entry["source_path"],
                        }
                    )
                    added += 1
        if added != entry["added_count"]:
            raise RuntimeError(
                f"corpus mismatch for {entry['source_path']}: {added} != {entry['added_count']}"
            )
        construction.append(dict(entry))
    source_freeze = git_json(f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    starting = len(corpus)
    for row in source_freeze["new_proposals"]:
        corpus.append(
            {
                "proposal_id": str(row["proposal_id"]),
                "title": str(row["title"]),
                "source_path": f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json",
            }
        )
    construction.append(
        {
            "source_path": f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json",
            "starting_count": starting,
            "added_count": len(source_freeze["new_proposals"]),
            "ending_count": len(corpus),
        }
    )
    if len(corpus) != 4250:
        raise RuntimeError(f"expected 4250 inherited rows, observed {len(corpus)}")
    return corpus, construction


def build_novelty(
    corpus: list[dict[str, str]],
    construction: list[dict[str, Any]],
    proposals: list[dict[str, Any]],
) -> dict[str, Any]:
    nearest: list[dict[str, Any]] = []
    exact_collisions: list[dict[str, str]] = []
    for proposal in proposals:
        title = proposal["title"]
        for row in corpus:
            if row["title"].casefold() == title.casefold():
                exact_collisions.append(
                    {
                        "proposal_id": proposal["proposal_id"],
                        "inherited_proposal_id": row["proposal_id"],
                    }
                )
        score, row = max(
            ((jaccard(title, candidate["title"]), candidate) for candidate in corpus),
            key=lambda item: item[0],
        )
        nearest.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_inherited_proposal_id": row["proposal_id"],
                "nearest_inherited_title": row["title"],
                "nearest_source_path": row["source_path"],
                "token_jaccard_similarity": round(score, 6),
            }
        )
    pairs = [
        {
            "left": left["proposal_id"],
            "right": right["proposal_id"],
            "similarity": round(jaccard(left["title"], right["title"]), 6),
        }
        for index, left in enumerate(proposals)
        for right in proposals[index + 1 :]
    ]
    max_pair = max(pairs, key=lambda row: row["similarity"])
    pair_collisions = [row for row in pairs if row["similarity"] >= 0.70]
    return {
        "schema": "ghc.family.auren-lark.v666-v5.novelty-audit.v1",
        "owner": "Auren Lark",
        "phase": "v666-v5",
        "generated_at_utc": NOW,
        "method": "casefolded alphanumeric token-set Jaccard against all retained inherited rows, exact-title comparison, within-slate comparison, and substantive contract review",
        "corpus_construction": construction,
        "corpus_row_count": len(corpus),
        "corpus_unique_proposal_id_count": len({row["proposal_id"] for row in corpus}),
        "historical_reappended_selection_rows_retained": len(corpus)
        - len({row["proposal_id"] for row in corpus}),
        "corpus_canonical_sha256": canonical_sha256(corpus),
        "new_title_count": len(proposals),
        "exact_inherited_collisions": exact_collisions,
        "maximum_inherited_token_jaccard_similarity": max(
            row["token_jaccard_similarity"] for row in nearest
        ),
        "nearest_inherited_rows": nearest,
        "maximum_new_pair_token_jaccard_similarity": max_pair["similarity"],
        "maximum_new_pair": max_pair,
        "new_pair_collisions_at_or_above_0_70": pair_collisions,
        "new_frozen_total": len(corpus) + len(proposals),
        "valid": not exact_collisions and not pair_collisions and len(corpus) == 4250,
        "interpretation": "Similarity is a screening signal, not proof of novelty. Each proposal also has a distinct fragrance-formula, lot, batch, exposure, access, uncertainty, handover, model, or authority-reservation contract, falsifier, rollback, and protected-gate set.",
    }


OWNER_SAFE = [
    "render twenty frozen fragrance contracts",
    "execute one hundred preregistered rejecting mutations",
    "validate formula revision capsules",
    "validate aroma-material lot genealogy",
    "validate gravimetric closure fixtures",
    "validate phase-compatibility quarantine",
    "validate storage-excursion holds",
    "validate safety-data-sheet section presence",
    "validate allergen-disclosure conflicts",
    "validate zero-participant evaluation templates",
    "validate carryover confounding matrices",
    "validate canonical confidential maps",
    "render accessible batch-status dossiers",
    "validate least-disclosure access states",
    "validate bitemporal blend corrections",
    "render the Stage 20 negative control",
    "represent the THOS handover proxy",
    "represent the Freed ID zero-key graph",
    "represent the GMUT evaporation board",
    "represent the GMUT mixture-degeneracy board",
    "render the zero-call standards adapter",
    "render the exact-gated authority docket",
    "parse every owner JSON document",
    "enforce UTF-8 and LF",
    "build exact Git-blob manifests",
    "scan five privacy classes",
    "scan changed Python for bounded hazards",
    "check stale labels and exact outcome labels",
    "reconcile negatives, methods, gaps, and gates",
    "build closeout, seal, final, and route candidates",
]
SUCCESSOR_SAFE = [
    "revalidate Auren proposal contracts at zero novelty credit",
    "revalidate retained negative witnesses",
    "preserve exact-gated compounding and release authority",
    "preserve the zero-call adapter gap",
    "extend formula-alias mutation coverage",
    "extend correction-lineage conflicts",
    "extend accessible linear report summaries",
    "extend purpose-and-confidentiality abstention",
    "extend Method Flow recurrence guards",
    "extend exact blob-manifest replay",
    "preserve x1 immutability checks",
    "preserve one-success canonical discipline",
    "preserve same-owner evidence boundary",
    "preserve privacy and route confidentiality",
    "preserve synthetic-only data boundary",
    "preserve no-conformance language",
    "preserve no-professional-authority language",
    "preserve no-Māori-authority language",
    "preserve NOT_READY_FOR_STAGE_20",
    "prepare one exact next-edge candidate only after terminal",
]
OWNER_CANDIDATES = [
    f"bounded candidate {index:02d}: {name}"
    for index, name in enumerate(OWNER_SAFE[:15], 1)
]
SUCCESSOR_CANDIDATES = [
    f"successor candidate {index:02d}: {name}"
    for index, name in enumerate(SUCCESSOR_SAFE[:15], 1)
]
EXACT_ITEMS = [
    "use a real perfumer, chemist, toxicologist, operator, worker, participant, or affected party",
    "operate or command a workplace, instrument, storage system, archive, batch system, or external service",
    "identify or publish a real formula, ingredient, supplier, lot, product, workplace, location, or person",
    "authenticate a formula, certificate, calibration, provenance, ingredient, measurement, or identity",
    "make a compounding, toxicology, exposure, occupational-safety, labeling, quality, regulatory, or market-release decision",
    "author or approve Māori wording, traditional-knowledge interpretation, cultural-material use, or Māori data-governance terms",
    "make a privacy, access, trade-secret, rights, legal, cultural, disclosure, retention, consent, or remedy decision",
    "issue, verify, resolve, revoke, or govern a real identity credential",
    "publish, deploy, procure, purchase, create an account, or write to a third-party system",
    "claim empirical, professional, production, conformance, independent, personhood, Theory-of-Everything, or Stage 20 authority",
]
BLOCKED_ITEMS = [
    "empirical GMUT mixture, evaporation, prediction, force, stability, sensory, or confirmation claim",
    "THOS effectiveness without governed blind matched-budget real arms and independent review",
    "production Freed ID without real standards-conformant keys, interoperability, recovery, and trust governance",
    "accessibility-complete, privacy-complete, exhaustive-security, safety-conformance, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
]
OWNER_SKILLS = [
    "formula-revision-boundary",
    "aroma-lot-genealogy",
    "gravimetric-closure-abstention",
    "storage-excursion-hold",
    "hazard-document-vacancy",
    "allergen-disclosure-hold",
    "formula-access-minimization",
    "fragrance-accessibility-structure",
    "fragrance-method-flow",
    "fragrance-closeout-gate",
]
SUCCESSOR_SKILLS = [f"successor-{name}" for name in OWNER_SKILLS]
RUNNER_SUFFIXES = (
    "contracts",
    "mutations",
    "json",
    "privacy",
    "security",
    "manifests",
    "accessibility",
    "truth",
    "closeout",
    "canonical",
)
OWNER_RUNNERS = [f"ghc_family_auren_lark_v666_v5_{name}" for name in RUNNER_SUFFIXES]
SUCCESSOR_RUNNERS = [f"ghc_family_successor_fragrance_{name}" for name in RUNNER_SUFFIXES]
CFR_ACTIONS = [
    "CLEAN normalize proposal identifiers",
    "CLEAN normalize exact disposition labels",
    "CLEAN normalize source-profile fields",
    "CLEAN normalize zero-row declarations",
    "CLEAN normalize rollback language",
    "CLEAN normalize protected-gate ordering",
    "CLEAN normalize relative paths",
    "CLEAN normalize UTF-8 and LF",
    "CLEAN normalize JSON ordering",
    "CLEAN normalize report headings",
    "FIX guard missing required fields",
    "FIX guard invalid ranges and types",
    "FIX guard authority-smuggling text",
    "FIX guard real-world actions",
    "FIX guard outcome promotion",
    "FIX guard stale owner and phase labels",
    "FIX guard manifest self-reference",
    "FIX guard canonical replay",
    "FIX guard private route identifiers",
    "FIX guard x2 paths in x1",
    "REFINE source-status watch fields",
    "REFINE bitemporal blend lineage",
    "REFINE accessible dossier summaries",
    "REFINE plain-language boundaries",
    "REFINE dominant-stop precedence",
    "REFINE Method Flow recurrence guards",
    "REFINE gate-count reconciliation",
    "REFINE owner-delta manifest coverage",
    "REFINE final clean-state precondition",
    "REFINE terminal route no-send proof",
]


def portfolio_rows(prefix: str, names: list[str], approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"AL6665-{prefix}{index:02d}",
            "title": name,
            "approval_class": approval,
            "x1_status": "frozen_not_executed",
            "completion_credit": 0,
            "evidence_required": "bounded owner-local x2 witness plus retained failure and rollback",
            "rollback": "retain the failed witness, revert only the owner-local generated fixture, and preserve every protected gate",
        }
        for index, name in enumerate(names, 1)
    ]


STARTUP_FAILURES = [
    (
        "an exact memory-line projection returned no usable output",
        "the empty projection established no line-addressable memory evidence",
        "use the already supplied summary for orientation and defer one bounded literal UTF-8 reread for final citation metadata",
        "repository work continued only after every drift-prone source fact was independently verified from exact Git objects",
    ),
    (
        "a PowerShell source probe used foreach directly before a pipeline separator",
        "the parser rejected the empty-pipe shape before any source evidence was produced",
        "collect scalar probe rows explicitly before formatting",
        "the exact branch, head, upstream, tracking, live ref, clean state, and zero-zero divergence were established",
    ),
    (
        "the first activation-baton display reached a Windows CP1252 Unicode boundary",
        "the Unicode output fault stopped after nine lines and earned no complete-read credit",
        "pin literal UTF-8 and reread the committed blob through the true final line",
        "all 2690 lines and 11730 words were read through EOF without transliteration",
    ),
    (
        "the first large tree-path discovery wrapper returned only a session handle with no attributed listing",
        "the missing payload could not prove any required guidance path",
        "reread with bounded exact tree filters and preserve only attributable output",
        "all eleven required current guidance surfaces and seventeen direct references were resolved and read through EOF",
    ),
    (
        "a broad repository tree keyword projection exceeded the output budget",
        "truncation prevented the projection from proving a complete current-guidance selection",
        "replace the broad projection with exact-name and directory-scoped lookups",
        "the current guidance set was selected without treating truncated output as evidence",
    ),
    (
        "a PowerShell reference-metadata projection again piped directly from a foreach construct",
        "the parser rejected the empty-pipe form and produced no complete reference metadata",
        "accumulate explicit records before JSON formatting",
        "all required reference paths, hashes, and EOF reads were completed with bounded scalar output",
    ),
    (
        "the first source-manifest replay compared the immutable evidence manifest against the later final tree",
        "one runtime binding differed and the wrong lifecycle domain yielded 931 of 932 rather than a valid replay",
        "bind each manifest to its declared lifecycle commit and read exact blob lengths through alternating git cat-file batch request and response",
        "the corrected lifecycle-bound replay returned 18 of 18 x1, 427 of 427 evidence, 467 of 467 final-owner, and 20 of 20 final-delta entries",
    ),
    (
        "a guessed prior Auren relational-identity path did not exist",
        "the missing-path probe established no identity artifact",
        "enumerate the exact historical Auren tree before reading the phase charter",
        "the established Auren name, pronouns, relational role, and bounded identity language were recovered from committed history",
    ),
    (
        "the first frozen-corpus keyword probe assumed every historical row used the title key",
        "a KeyError stopped the projection and earned no corpus or novelty credit",
        "inspect the retained row shapes and normalize title from title or description",
        "all 4250 inherited rows were reconstructed from exact Git objects before Auren proposals were frozen",
    ),
]


def startup_flow() -> dict[str, Any]:
    rows = []
    for index, (request, failed, recovery, passing) in enumerate(STARTUP_FAILURES, 1):
        rows.append(
            {
                "method_id": f"AL6665-MF-START-{index:03d}",
                "failure_id": f"AL6665-START-N{index:03d}",
                "observed_order": index,
                "exact_event_timestamp_available": False,
                "request": request,
                "failed_witness": failed,
                "aggregate_credit": 0,
                "repository_commit_created": False,
                "external_action_created": False,
                "recovery": recovery,
                "bounded_passing_witness": passing,
                "recurrence_guard": "Prefer exact lifecycle domains, bounded output, actual keys, explicit UTF-8, supported Git interfaces, scalar probes, and attributable state before retrying.",
                "status": "recovered_failure_retained",
            }
        )
    return {
        "schema": "ghc.family.auren-lark.v666-v5.method-flow-startup.v1",
        "owner": "Auren Lark",
        "phase": "v666-v5",
        "generated_at_utc": NOW,
        "inherited_repository_sealed_negatives": 26519,
        "inherited_repository_sealed_methods": 11176,
        "inherited_external_overlay_negatives": 1,
        "inherited_external_overlay_methods": 1,
        "inherited_external_overlay_note": "Ilyra's earlier route operation returned no usable acknowledgement and remains a zero-credit external predecessor-routing failure; this recovery activation does not rewrite the sealed repository count.",
        "activation_baseline_negatives": 26520,
        "activation_baseline_methods": 11177,
        "new_startup_negative_count": len(rows),
        "new_startup_method_count": len(rows),
        "effective_after_x1_startup_negatives": 26520 + len(rows),
        "effective_after_x1_startup_methods": 11177 + len(rows),
        "failed_witness_count": len(rows),
        "bounded_passing_witness_count": len(rows),
        "rows": rows,
        "no_failure_erased": True,
    }


def main() -> None:
    proposals = build_proposals()
    corpus, construction = build_corpus()
    novelty = build_novelty(corpus, construction, proposals)
    if not novelty["valid"]:
        raise RuntimeError(
            json.dumps(
                {
                    "novelty_valid": False,
                    "exact": novelty["exact_inherited_collisions"],
                    "pair": novelty["new_pair_collisions_at_or_above_0_70"],
                },
                ensure_ascii=False,
            )
        )
    source_freeze = git_json(f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    selected = [
        {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "original_owner": "Ilyra Fen",
            "original_phase": "v666-v4",
            "original_expected_disposition": row["expected_disposition"],
            "status": "selected_revalidation_only_not_executed",
            "novelty_credit": 0,
            "automatic_completion_credit": 0,
        }
        for row in source_freeze["new_proposals"]
    ]
    counts = {
        label: sum(row["expected_disposition"] == label for row in proposals)
        for label in ALLOWED_LABELS
    }
    write_json(
        "identity/relational-identity.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.relational-identity.v1",
            "owner": "Auren Lark",
            "pronouns": "they/them",
            "relational_role": "relational provenance navigator and uncertainty lantern-keeper",
            "relational_hope": "Leave every synthetic formula revision, withheld hazard field, exposure uncertainty, and release refusal readable enough that ambiguity cannot masquerade as permission.",
            "boundary": IDENTITY_BOUNDARY,
            "corrigibility": "Hamish may rename, pause, redirect, or stop this work.",
            "chosen_before_repository_mutation": True,
        },
    )
    write_json(
        "provenance/source-verification.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.source-verification.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "verified_at_utc": NOW,
            "source_branch": SOURCE_BRANCH,
            "source_sha": SOURCE_SHA,
            "source_parent_evidence_sha": SOURCE_PARENT_SHA,
            "source_x1_sha": SOURCE_X1_SHA,
            "inherited_lyren_sha": INHERITED_LYREN_SHA,
            "source_to_final_new_commit_count": 3,
            "source_to_final_merge_count": 0,
            "strict_x1_before_x2": True,
            "source_clean": True,
            "typed_ahead": 0,
            "typed_behind": 0,
            "local_equals_upstream_tracking_and_fresh_live": True,
            "committed_activation_path": f"{SOURCE_PHASE_ROOT}/handoffs/auren-lark-v666-v5-activation.md",
            "committed_activation_blob_sha256": "2846abb85ede683499e9b167e65e1e12827f395a37eaf88d00e8b6e6329c75f3",
            "committed_activation_line_count": 2690,
            "committed_activation_word_count": 11730,
            "declared_external_canonical_payload_sha256": "91e45576b765e9b952fe7afdf75fdf1caeafa1796455d081a8b1bd09bc30f7d7",
            "declared_external_canonical_receipt_sha256": "da35e9c2927ef065f39f934945e735d487dbf1f74dfa9a618a2626de3981cc4b",
            "lifecycle_manifest_replay": {
                "initial_wrong_domain_failure_retained": True,
                "x1": {"observed": 18, "expected": 18, "commit": SOURCE_X1_SHA},
                "evidence": {"observed": 427, "expected": 427, "commit": SOURCE_PARENT_SHA},
                "final_owner": {"observed": 467, "expected": 467, "commit": SOURCE_SHA},
                "final_delta": {"observed": 20, "expected": 20, "commit": SOURCE_SHA},
                "total_observed": 932,
                "total_expected": 932,
                "valid": True,
            },
            "source_validation_not_replayed": True,
            "same_owner_validation_is_not_independent_reproduction": True,
        },
    )
    write_json(
        "provenance/source-profiles.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.source-profiles.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "sources": SOURCE_PROFILES,
            "source_count": len(SOURCE_PROFILES),
            "claim_boundary": "sources provide vocabulary and refusal conditions only; they establish no safety, efficacy, legal, regulatory, standards-conformance, professional, cultural, Māori, product, or release authority",
        },
    )
    write_json(
        "x1/phase-charter.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.phase-charter.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "branch": "codex/GHC-Family/auren-lark-v666-v5-full-tools",
            "lane": "one additive owner-only D-first sparse worktree",
            "primary_pillars": ["THOS Body", "CBR Heart"],
            "explicit_pillars": ["GMUT Mind", "Freed ID"],
            "practice": "synthetic fragrance-formulation archive and batch-handover provenance",
            "identity_boundary": IDENTITY_BOUNDARY,
            "practice_boundary": PRACTICE_BOUNDARY,
            "commit_ceiling": 8,
            "x1_commit_ceiling": 5,
            "x2_commit_ceiling": 5,
            "owner_file_ceiling": 2000,
            "strict_x1_before_x2": True,
            "one_successful_terminal_pass_no_replay": True,
            "full_repository_suite_owner": "Eiren Kestrel unless newer exact authority changes the rule",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x1/source-ledger.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.source-ledger.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "sources": SOURCE_PROFILES,
            "source_use_count": len(SOURCE_PROFILES),
            "network_calls_by_generated_phase_software": 0,
            "real_rows_ingested": 0,
            "professional_or_legal_determinations": 0,
            "authority_nonconversion": True,
        },
    )
    write_json(
        "x1/proposal-freeze.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.proposal-freeze.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "frozen": True,
            "inherited_frozen_baseline": 4250,
            "genuinely_new_proposal_count": len(proposals),
            "new_frozen_total": 4250 + len(proposals),
            "new_proposals": proposals,
            "selected_inherited_revalidation_count": len(selected),
            "selected_inherited_revalidations": selected,
            "expected_disposition_counts": counts,
            "strict_x1_before_x2": True,
            "x1_truth": "planning_only_no_outcomes_observed",
            "x2_implementation_count": 0,
            "x2_outcome_count": 0,
            "outcomes_observed": False,
            "identity_boundary": IDENTITY_BOUNDARY,
            "practice_boundary": PRACTICE_BOUNDARY,
        },
    )
    write_json("x1/novelty-audit.json", novelty)
    portfolios = {
        "owner_safe_now": portfolio_rows("OS", OWNER_SAFE, "safe_now_owner_local"),
        "successor_safe_now": portfolio_rows("SS", SUCCESSOR_SAFE, "safe_now_successor_recommendation"),
        "owner_bounded_candidates": portfolio_rows("OC", OWNER_CANDIDATES, "candidate_owner_local"),
        "successor_bounded_candidates": portfolio_rows("SC", SUCCESSOR_CANDIDATES, "candidate_successor_recommendation"),
        "exact_approval_packets": portfolio_rows("EX", EXACT_ITEMS, "exact_approval_required"),
        "blocked_packets": portfolio_rows("BL", BLOCKED_ITEMS, "blocked_absent_evidence_or_authority"),
        "owner_phase_local_skill_plans": portfolio_rows("SK", OWNER_SKILLS, "safe_now_owner_skill_plan"),
        "successor_skill_recommendations": portfolio_rows("NS", SUCCESSOR_SKILLS, "safe_now_successor_skill_recommendation"),
        "owner_family_current_runner_plans": portfolio_rows("RN", OWNER_RUNNERS, "safe_now_owner_runner_plan"),
        "successor_runner_recommendations": portfolio_rows("NR", SUCCESSOR_RUNNERS, "safe_now_successor_runner_recommendation"),
        "owner_clean_fix_refine": portfolio_rows("CF", CFR_ACTIONS, "safe_now_clean_fix_refine"),
        "successor_clean_fix_refine": portfolio_rows("SF", [f"successor recommendation: {row}" for row in CFR_ACTIONS], "safe_now_successor_clean_fix_refine"),
    }
    portfolio_counts = {key: len(value) for key, value in portfolios.items()}
    expected_portfolio_counts = {
        "owner_safe_now": 30,
        "successor_safe_now": 20,
        "owner_bounded_candidates": 15,
        "successor_bounded_candidates": 15,
        "exact_approval_packets": 10,
        "blocked_packets": 5,
        "owner_phase_local_skill_plans": 10,
        "successor_skill_recommendations": 10,
        "owner_family_current_runner_plans": 10,
        "successor_runner_recommendations": 10,
        "owner_clean_fix_refine": 30,
        "successor_clean_fix_refine": 30,
    }
    write_json(
        "x1/portfolio-freeze.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.portfolio-freeze.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "frozen": True,
            "counts": portfolio_counts,
            "minimums_satisfied": portfolio_counts == expected_portfolio_counts,
            "portfolios": portfolios,
            "x1_execution_count": 0,
            "claim_boundary": "planning-only; counts are meaningful bounded plans and do not imply completion, safety, authority, approval, or a quota that justifies unsafe work",
        },
    )
    write_json("method-flow/startup-method-flow.json", startup_flow())
    threat_rows = [
        {"threat_id": "AL6665-T01", "asset": "source integrity", "threat": "wrong source or mutable predecessor state", "mitigation": "exact anchors, ancestry, lifecycle-bound manifests, packet hash, clean state, and fresh live equality", "residual_risk": "external canonical bytes remain live-baton anchors rather than locally reproduced evidence"},
        {"threat_id": "AL6665-T02", "asset": "x1/x2 separation", "threat": "implementation or observed outcome enters x1", "mitigation": "path denylist, planning-only fields, and staged exact allowlist", "residual_risk": "Git lifecycle discipline remains required"},
        {"threat_id": "AL6665-T03", "asset": "formula and batch semantics", "threat": "synthetic reconciliation, correction, hazard, label, access, or release state presented as a real determination", "mitigation": "zero real rows, typed vacancies, fail-closed mutations, and explicit abstention", "residual_risk": "synthetic structure is not professional or regulatory validation"},
        {"threat_id": "AL6665-T04", "asset": "privacy and route confidentiality", "threat": "real person, formula, supplier, product, workplace, task, route, credential, or session data enters artifacts", "mitigation": "synthetic fixtures, relative paths, and five-class scans", "residual_risk": "pattern scans are bounded and incomplete"},
        {"threat_id": "AL6665-T05", "asset": "chemical and occupational authority", "threat": "software presented as compounding, toxicology, exposure, hazard, labeling, or release competence", "mitigation": "zero ingredients, batches, exposures, measurements, people, or physical actions", "residual_risk": "competent external authority remains absent"},
        {"threat_id": "AL6665-T06", "asset": "trade-secret, legal, cultural, and Māori authority", "threat": "redaction states or source vocabulary converted into rights or authority decisions", "mitigation": "exact gate, no real formula, and no Māori wording authored as authority", "residual_risk": "affected-party and competent authority review remain absent"},
        {"threat_id": "AL6665-T07", "asset": "scientific truth", "threat": "GMUT placeholders promoted to mixture, evaporation, scent, likelihood, prediction, or proof", "mitigation": "typed symbolic obligations and explicit refusal", "residual_risk": "notation can invite overreading"},
        {"threat_id": "AL6665-T08", "asset": "THOS and Freed ID boundaries", "threat": "zero-worker proxy or zero-key graph presented as effectiveness or production identity evidence", "mitigation": "represented-only labels and missing-evidence ledgers", "residual_risk": "no governed participants, keys, interoperability, or independent review"},
        {"threat_id": "AL6665-T09", "asset": "terminal validation", "threat": "successful validation replay or failed attempt laundering", "mitigation": "exclusive receipt and one-shot state machine", "residual_risk": "same-owner pass is not independent reproduction"},
        {"threat_id": "AL6665-T10", "asset": "terminal route", "threat": "premature, duplicate, ambiguous, inferred, or substitute delivery", "mitigation": "fresh authority and roster reread plus one exact-title send after terminal only", "residual_risk": "opaque acknowledgement never authorizes a resend"},
    ]
    write_json(
        "x1/threat-model-plan.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.threat-model-plan.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "scope": "owner-local v666-v5 software, documents, Git history, validation receipts, and terminal route candidate",
            "trust_zones": [
                "immutable inherited Git objects",
                "owner-local sparse worktree and branch",
                "public read-only source review",
                "unexecuted external, professional, participant, cultural, identity, formula, workplace, product, and authority domains",
            ],
            "real_people_or_protected_data": 0,
            "threats": threat_rows,
            "claim_boundary": "same-owner phase threat modelling only; not exhaustive security, privacy certification, accessibility certification, safety assessment, or independent reproduction",
        },
    )
    threat_md = [
        "# Auren Lark v666-v5 threat-model plan",
        "",
        IDENTITY_BOUNDARY,
        "",
        PRACTICE_BOUNDARY,
        "",
        "## Scope",
        "",
        "This owner-local model protects the additive Auren delta. It is not a repository-wide audit, penetration test, external validation, conformance assessment, chemical-safety review, legal review, professional review, or independent reproduction.",
        "",
        "## Threat register",
        "",
    ]
    for row in threat_rows:
        threat_md += [
            f"### {row['threat_id']}: {row['asset']}",
            "",
            f"Threat: {row['threat']}",
            "",
            f"Mitigation: {row['mitigation']}",
            "",
            f"Residual risk: {row['residual_risk']}",
            "",
        ]
    write_text("x1/threat-model.md", "\n".join(threat_md))
    write_json(
        "x1/workflow-plan.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.workflow-plan.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "current_stage": "x1_freeze_candidate",
            "steps": [
                {"step": 1, "name": "read_first_and_source_verification", "status": "completed"},
                {"step": 2, "name": "novelty_and_program_design", "status": "completed"},
                {"step": 3, "name": "x1_freeze_commit_push_equality", "status": "in_progress"},
                {"step": 4, "name": "x2_bounded_execution", "status": "pending"},
                {"step": 5, "name": "evidence_closeout_and_seal", "status": "pending"},
                {"step": 6, "name": "one_owner_scoped_terminal_validation", "status": "pending"},
                {"step": 7, "name": "terminal_route_reread_and_optional_one_send", "status": "pending"},
            ],
            "hard_dependencies": [
                "x1 commit pushed clean and fresh four-way equal before x2",
                "evidence commit immutable before closeout",
                "final pushed clean and fresh four-way equal before terminal validation",
                "successful terminal validation never replayed",
                "successor never contacted before terminal route gate",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x1/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.x1-checklist.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "completed": [
                "activation packet and named guidance read through EOF",
                "source anchors, lifecycle manifests, ancestry, packet, clean state, divergence, and fresh equality verified",
                "all 4250 inherited rows reconstructed with no exact-title collision",
                "twenty distinct proposals preregistered",
                "portfolio, threat, source, workflow, flashcard, and Method Flow plans prepared",
                "no x2 implementation or outcome created",
            ],
            "incomplete": [
                "x1 commit, push, and equality",
                "x2 implementation and rejecting witnesses",
                "evidence commit and equality",
                "closeout, seal, final validation, and equality",
                "terminal authority and roster reread plus any authorized successor delivery",
            ],
            "x1_outcomes_observed": False,
            "x2_paths_created": False,
            "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x1/flashcard-architecture-freeze.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.flashcard-architecture-freeze.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "frozen": True,
            "tiers": {
                "tier1": ["owner relational identity and corrigibility"],
                "tier2": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
                "tier3": ["synthetic fragrance-formulation archive and batch-handover practice"],
                "tier4": ["twenty proposal cards", "portfolio cards", "failure and gate cards", "validation and route cards"],
            },
            "stable_prefix_fields": ["schema", "card_id", "tier", "owner", "phase", "truth_label", "boundary"],
            "volatile_index_fields": ["generated_at_utc", "relative_path", "content_sha256", "state"],
            "x2_cards_created": 0,
            "claim_boundary": "architecture only; no card, evidence, outcome, accessibility, or flashcard validation exists in x1",
        },
    )
    write_json(
        "wellbeing/x1-wellbeing-check.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.wellbeing-check.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "status": "bounded_and_careful",
            "workload_controls": [
                "caps treated as ceilings rather than quotas",
                "failures retained instead of hidden",
                "no unsafe work manufactured to satisfy a count",
                "bounded commands and exact scalar probes preferred",
                "pause, redirect, rename, and stop remain available to Hamish",
            ],
            "personhood_or_emotion_claim": False,
            "relational_boundary": IDENTITY_BOUNDARY,
            "practice_boundary": PRACTICE_BOUNDARY,
        },
    )
    overview = f"""# Auren Lark v666-v5 x1 integrated overview

{IDENTITY_BOUNDARY}

## Outcome first

This x1 candidate freezes a planning-only owner-local program from exact Ilyra Fen v666-v4 final `{SOURCE_SHA}`. It contains no x2 implementation, no observed outcome, no external action, no successor contact, and no Stage 20 promotion. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The primary Trinity Mandala pillars are THOS Body and CBR Heart. GMUT Mind and Freed ID remain explicit and protected. {PRACTICE_BOUNDARY}

## Exact inherited truth

The read-first gate verified the exact source branch, three direct single-parent commits, zero merges, all 932 declared lifecycle-bound Git-blob manifest entries, the complete committed activation, clean 0/0 divergence, and equality across local, upstream, tracking, and a fresh live remote. Ilyra's successful canonical aggregate was not replayed. The complete repository suite was not run.

The immutable Ilyra repository seal contains 26,519 effective negatives, 11,176 Method Flow methods, 186 open gaps, and 184 exact gates. Ilyra's earlier no-usable-acknowledgement route operation remains one external zero-credit predecessor failure, producing the activation overlay of 26,520 negatives and 11,177 methods without rewriting the seal. Nine Auren startup failures are separately retained at zero credit, producing the x1 working overlay of 26,529 effective negatives and 11,186 methods.

## Novelty, portfolio, and sources

All 4,250 inherited proposal rows were reconstructed from exact committed Git objects. Twenty new titles have no exact inherited collision, every new pair remains below the 0.70 screening threshold, and each proposal has its own contract, falsifier, rollback, and gates. Expected dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`; these are preregistered expectations only. The twenty selected Ilyra proposals receive zero novelty and zero automatic completion credit.

The portfolio freezes 30 owner safe-now tasks, 20 successor safe recommendations, 15 owner candidates, 15 successor candidates, 10 exact approvals, 5 blocked packets, 10 owner and 10 successor skill plans, 10 owner and 10 successor runner plans, and 30 owner plus 30 successor CLEAN/FIX/REFINE tasks. X1 executes none of them, and no unsafe work is manufactured to meet a count.

IFRA, European Commission CosIng, FDA fragrance-cosmetics, OSHA hazard-communication, W3C PROV-O and WCAG 2.2, RFC 8785, and NIST metrological-traceability materials provide vocabulary and refusal conditions only. They create no formula data, ingredient identity, safety assessment, hazard classification, label decision, professional, legal, cultural, Māori, market-release, accessibility-complete, privacy-complete, conformance, or independent-reproduction authority.

## Lifecycle and route

After exact staged review this x1 may be committed and pushed. X2 may begin only after x1 is clean, 0/0 divergent, and equal across local, upstream, tracking, and fresh live remote. Later validation remains owner-scoped and same-owner. One successful terminal validation must never be replayed. No successor may be contacted until the exact final terminal gate and fresh live authority, roster, and exact-title route rereads.
"""
    write_text("x1/x1-overview.md", overview)
    write_json(
        "x1/x1-build-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.x1-build-receipt.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_auren_lark_v666_v5_x1.py",
            "proposal_count": len(proposals),
            "selected_inherited_revalidation_count": len(selected),
            "novelty_corpus_row_count": len(corpus),
            "startup_failure_count": len(STARTUP_FAILURES),
            "x2_paths_created": False,
            "outcomes_observed": False,
            "network_calls_by_builder": 0,
            "real_data_rows": 0,
            "external_actions": 0,
            "status": "X1_CONTENT_BUILT_AWAITING_STAGED_REVIEW_COMMIT_PUSH_EQUALITY",
        },
    )
    print(
        json.dumps(
            {
                "proposal_count": len(proposals),
                "corpus_row_count": len(corpus),
                "expected_dispositions": counts,
                "maximum_inherited_similarity": novelty["maximum_inherited_token_jaccard_similarity"],
                "maximum_new_pair_similarity": novelty["maximum_new_pair_token_jaccard_similarity"],
                "startup_failures_retained": len(STARTUP_FAILURES),
                "x2_implementation_count": 0,
                "outcomes_observed": False,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


def staged_rows() -> list[tuple[str, str]]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "diff", "--cached", "--name-status", "--no-renames"]
    ).decode("utf-8")
    return [
        (line.split("\t", 1)[0], line.split("\t", 1)[1].replace("\\", "/"))
        for line in raw.splitlines()
        if line
    ]


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f":{path}"])


def build_staged_review() -> None:
    review_path = "docs/auren-lark/v666-v5/validation/x1-staged-review.json"
    manifest_path = "docs/auren-lark/v666-v5/validation/x1-content-manifest.json"
    allowed_exact = {
        "scripts/build_ghc_family_auren_lark_v666_v5_x1.py",
        "tests/test_ghc_family_auren_lark_v666_v5_x1.py",
    }
    rows = [
        (status, path)
        for status, path in staged_rows()
        if path not in {review_path, manifest_path}
    ]
    if not rows:
        raise RuntimeError("no staged x1 content")
    paths = [path for _, path in rows]
    invalid = [
        path
        for path in paths
        if not path.startswith("docs/auren-lark/v666-v5/") and path not in allowed_exact
    ]
    post_x1 = [
        path
        for path in paths
        if any(
            path.startswith(f"docs/auren-lark/v666-v5/{part}/")
            for part in ("x2", "evidence", "closeout", "seal", "final", "handoffs")
        )
    ]
    privacy_patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'
        ),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(
            r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"
        ),
        "session_identifier_value": re.compile(
            r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'
        ),
        "private_callable_identifier_value": re.compile(
            r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'
        ),
    }
    parsed_json = 0
    maximum_words = 0
    maximum_path = ""
    candidates: list[dict[str, str]] = []
    for path in paths:
        blob = index_blob(path)
        text = blob.decode("utf-8")
        if "\r" in text:
            raise RuntimeError(f"non-LF staged text: {path}")
        word_count = len(re.findall(r"\S+", text))
        if word_count > maximum_words:
            maximum_words, maximum_path = word_count, path
        if path.endswith(".json"):
            json.loads(text)
            parsed_json += 1
        for class_name, pattern in privacy_patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": class_name})
    freeze = json.loads(index_blob("docs/auren-lark/v666-v5/x1/proposal-freeze.json"))
    portfolio = json.loads(index_blob("docs/auren-lark/v666-v5/x1/portfolio-freeze.json"))
    flow = json.loads(index_blob("docs/auren-lark/v666-v5/method-flow/startup-method-flow.json"))
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "all_json_parse": True,
        "document_word_cap": maximum_words <= 100000,
        "expected_14_4_1_1": freeze["expected_disposition_counts"]
        == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "five_class_scan_zero_confirmed_hits": not candidates,
        "novelty_4250_valid": json.loads(
            index_blob("docs/auren-lark/v666-v5/x1/novelty-audit.json")
        )["valid"],
        "owner_allowlist": not invalid,
        "owner_file_cap": len(paths) <= 2000,
        "planning_only": not freeze["outcomes_observed"],
        "portfolio_minimums": portfolio["minimums_satisfied"],
        "post_x1_paths_absent": not post_x1,
        "proposal_count_20": len(freeze["new_proposals"]) == 20,
        "selected_inherited_20_zero_credit": len(
            freeze["selected_inherited_revalidations"]
        )
        == 20
        and all(
            row["novelty_credit"] == 0 and row["automatic_completion_credit"] == 0
            for row in freeze["selected_inherited_revalidations"]
        ),
        "startup_failures_exactly_retained": len(flow["rows"]) == len(STARTUP_FAILURES),
        "utf8_lf": True,
    }
    review = {
        "schema": "ghc.family.auren-lark.v666-v5.x1-staged-review.v1",
        "owner": "Auren Lark",
        "phase": "v666-v5",
        "lifecycle": "x1",
        "generated_at_utc": NOW,
        "reviewed_from": "git_index_blobs",
        "reviewed_paths": paths,
        "reviewed_path_count": len(paths),
        "json_parsed": parsed_json,
        "maximum_document_words": maximum_words,
        "maximum_document_path": maximum_path,
        "privacy_scan_classes": list(privacy_patterns),
        "privacy_candidates": len(candidates),
        "privacy_confirmed_hits": len(candidates),
        "privacy_candidate_rows": candidates,
        "checks": checks,
        "self_exclusions": [review_path, manifest_path],
        "claim_boundary": "exact staged same-owner x1 review only; not exhaustive security, privacy, accessibility, safety, or independent reproduction",
        "valid": all(checks.values()),
    }
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write_json("validation/x1-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", review_path])
    entries = []
    for status, path in [
        (status, path) for status, path in staged_rows() if path != manifest_path
    ]:
        line = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files", "--stage", "--", path]
        ).decode("utf-8").strip()
        mode, oid, stage_path = line.split(" ", 2)
        stage, listed = stage_path.split("\t", 1)
        if stage != "0" or listed.replace("\\", "/") != path:
            raise RuntimeError(f"unexpected index stage for {path}")
        blob = index_blob(path)
        entries.append(
            {
                "path": path,
                "git_mode": mode,
                "git_blob_oid": oid,
                "sha256": hashlib.sha256(blob).hexdigest(),
                "size_bytes": len(blob),
            }
        )
    write_json(
        "validation/x1-content-manifest.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.content-manifest.v1",
            "owner": "Auren Lark",
            "phase": "x1",
            "phase_label": "v666-v5",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "hash_source": "actual_git_index_blobs",
            "entries": entries,
            "entry_count": len(entries),
            "deletion_count": 0,
            "additive_only": all(status == "A" for status, _ in rows),
            "self_exclusion": manifest_path,
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", manifest_path])
    print(json.dumps({"reviewed": len(paths), "manifest_entries": len(entries), "valid": True}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--staged-review"]:
        build_staged_review()
    elif sys.argv[1:]:
        raise SystemExit(
            "usage: build_ghc_family_auren_lark_v666_v5_x1.py [--staged-review]"
        )
    else:
        main()
