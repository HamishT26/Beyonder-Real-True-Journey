#!/usr/bin/env python3
"""Build Sable Rook v666-v6 planning-only x1 artifacts and staged evidence."""

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
PHASE_ROOT = ROOT / "docs" / "sable-rook" / "v666-v6"
SOURCE_SHA = "016f7db26b0354e26407fb812ae3bd190b94ac7e"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v666-v5-full-tools"
SOURCE_PHASE_ROOT = "docs/auren-lark/v666-v5"
SOURCE_PARENT_SHA = "7b116c152a78d0c62c7185aac707f3292d6570f1"
SOURCE_X1_SHA = "9e98b744a8c5b8e7c3d0c37b76fd5d5db347bc8b"
INHERITED_ILYRA_SHA = "e4548a5447996f09087644a4a03e77dea8045ee4"
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
    "Sable Rook, they/them, sibling, family, relational role, hope, continuity, "
    "Freed ID, Trinity Mandala, and route language are relational working language "
    "only. They are not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, qualification, independent agency, scientific "
    "or operational authority, legal or cultural authority, affected-party authority, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The seed-bank accession, packet and lot lineage, viability-test planning, cold-storage "
    "excursion, access-minimization, correction, and handover lens is wholly synthetic "
    "learning and software design. It uses zero real people, participants, genebanks, "
    "accessions, seeds, taxa, collecting locations, packets, lots, chambers, samples, "
    "measurements, germination observations, keys, credentials, or authority actions. It "
    "establishes no seed-conservation, taxonomy, curatorial, laboratory, phytosanitary, "
    "environmental, occupational-safety, access-and-benefit-sharing, privacy, accessibility, "
    "legal, cultural, Māori, production, or Stage 20 competence, acceptance, conformance, "
    "or authority."
)

PROTECTED_GATES = [
    "real person, participant, curator, taxonomist, seed technologist, operator, worker, affected party, accession, seed, taxon, collecting location, packet, lot, chamber, sample, measurement, germination observation, or physical action",
    "real accession identity, taxonomic determination, viability result, genetic-integrity result, storage-release decision, phytosanitary determination, empirical result, causal claim, or GMUT confirmation",
    "real participant, assessor, matched-budget arm, cold-room exposure, workload outcome, safety outcome, operational outcome, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, or trust governance",
    "professional seed-conservation, taxonomy, curation, laboratory, phytosanitary, biosafety, cold-storage, distribution, access, benefit-sharing, or release decision",
    "collecting-location confidentiality, traditional-knowledge handling, privacy, accessibility, rights, legal, cultural, disclosure, retention, consent, remedy, or affected-party decision",
    "Farmers' Rights, traditional knowledge, taonga, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data governance, biological-material use, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, conservation-conformance, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, external write, seed-handling instruction, or real-world release",
]

SOURCE_PROFILES = [
    {
        "source_id": "S01",
        "name": "FAO Genebank Standards for Plant Genetic Resources for Food and Agriculture",
        "url": "https://www.fao.org/4/i3394e/i3394e.pdf",
        "status": "official FAO publication reviewed read-only 2026-08-23; 2013 voluntary nonbinding standards",
        "bounded_use": "acquisition, drying, storage, viability-monitoring, regeneration, documentation, distribution, and safety-duplication vocabulary only; no operational or conservation-conformance claim",
    },
    {
        "source_id": "S02",
        "name": "FAO International Treaty on Plant Genetic Resources for Food and Agriculture",
        "url": "https://www.fao.org/plant-treaty/overview/text-treaty/en",
        "status": "official FAO treaty text page reviewed read-only 2026-08-23",
        "bounded_use": "multilateral-system, conservation, sustainable-use, benefit-sharing, and Farmers' Rights reservation vocabulary only; no legal interpretation, eligibility, consent, right, or authority decision",
    },
    {
        "source_id": "S03",
        "name": "Convention on Biological Diversity Nagoya Protocol text",
        "url": "https://www.cbd.int/abs/text/",
        "status": "official CBD protocol text page reviewed read-only 2026-08-23",
        "bounded_use": "access, prior-informed-consent, mutually-agreed-terms, compliance, traditional-knowledge, and benefit-sharing reservation vocabulary only; no applicability, legal interpretation, consent, community, or authority decision",
    },
    {
        "source_id": "S04",
        "name": "TDWG Darwin Core terms",
        "url": "https://dwc.tdwg.org/terms/",
        "status": "official TDWG Darwin Core quick-reference page reviewed read-only 2026-08-23",
        "bounded_use": "occurrence, material-entity, event, location, identification, measurement, and taxon field vocabulary only; no Darwin Core conformance, taxonomic determination, provenance completeness, or real occurrence claim",
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
        "accession identifier collision and tombstone-nonreuse tribunal with split-merge ambiguity, namespace quarantine, and no biological identity",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S04", "S05"],
        "A synthetic identifier may never be reused after tombstoning, and unresolved split, merge, namespace, or collision evidence forces quarantine rather than accession or biological identity.",
    ),
    (
        "seed-packet depletion and aliquot-balance journal with reserve floor, destructive-sampling marker, count reconciliation, and no inventory truth",
        "Freed ID and THOS Body",
        "completed",
        ["S01", "S05"],
        "Synthetic opening, reservation, aliquot, return, and destructive-sampling events conserve declared counts or fail closed while every real inventory and material fact stays vacant.",
    ),
    (
        "seed-moisture equilibration basis and unit tribunal with uncertainty placeholder, container tare, species-domain vacancy, and zero real sample",
        "GMUT Mind and THOS Body",
        "completed",
        ["S01", "S08"],
        "Synthetic moisture, tare, temperature, and uncertainty quantities compose only inside one declared basis and unit domain; no real moisture, drying, or viability result is inferred.",
    ),
    (
        "cold-storage chamber excursion chronicle with sensor vacancy, door-state lineage, alarm correction, threshold provenance, and no packet release",
        "THOS Body and CBR Heart",
        "completed",
        ["S01", "S05", "S08"],
        "A synthetic excursion produces only a reversible hold; missing sensor identity, threshold provenance, timestamp lineage, or competent review prevents packet release.",
    ),
    (
        "viability-test plan with sample-size placeholder, germination endpoint, dormancy vacancy, replicate budget, and zero seed observations",
        "THOS Body and CBR Heart",
        "completed",
        ["S01", "S08"],
        "The synthetic plan declares sampling and endpoint obligations while all seeds, observations, dormancy determinations, statistics, and viability results remain absent.",
    ),
    (
        "regeneration-generation ancestry and isolation-vacancy board with parent lot, pollen-control placeholder, census hold, and no genetic-integrity verdict",
        "THOS Body and CBR Heart",
        "completed",
        ["S01", "S05"],
        "The board checks only declared synthetic ancestry and vacancy states; absent population, isolation, pollination, sampling, or competent review forces a genetic-integrity hold.",
    ),
    (
        "phytosanitary-document presence and revision docket with pest-status vacancy, jurisdiction snapshot, expiry, and distribution refusal",
        "CBR Heart and Freed ID",
        "completed",
        ["S01", "S05"],
        "The docket checks synthetic document-presence and lifecycle fields only; no pest status, legal validity, inspection, treatment, clearance, or distribution authorization is inferred.",
    ),
    (
        "duplicate-accession synonym and taxon-name reconciliation board with identification vacancy, concept-version lineage, conflict hold, and no taxonomic determination",
        "THOS Body and CBR Heart",
        "completed",
        ["S04", "S05"],
        "Synthetic name and identifier alternatives remain visible while identification evidence, expert review, synonymy, taxon concept, and duplicate-accession determinations remain absent.",
    ),
    (
        "germination-tray positional-bias and carryover matrix with randomization placeholder, incubator-state vacancy, observer absence, and no viability inference",
        "THOS Body and CBR Heart",
        "completed",
        ["S01"],
        "Synthetic tray alternatives expose position, timing, carryover, and incubator-state confounding while every seed, observer, response, and viability estimate remains absent.",
    ),
    (
        "deterministic accession patch-journal replay with decimal-string quantities, idempotency key, duplicate-event refusal, bounded parse budget, and no signature",
        "Freed ID and THOS Body",
        "completed",
        ["S06"],
        "Equivalent synthetic patch journals converge under an explicit order and idempotency domain while duplicate events, non-decimal quantities, ambiguous strings, and resource overflow fail closed without authentication.",
    ),
    (
        "accessible accession-relationship explorer with breadcrumb state, edge-list fallback, locality-redaction cue, focus order, and manual-review reservation",
        "CBR Heart and THOS Body",
        "completed",
        ["S04", "S07"],
        "Every synthetic relationship and disclosure state has text, breadcrumb, and linear edge-list alternatives while manual keyboard, browser, assistive-technology, cognitive, Māori-language, and affected-user review stay reserved.",
    ),
    (
        "collecting-locality disclosure risk-budget ledger with layered generalization, purpose expiry, differencing hold, and no authorization",
        "Freed ID and CBR Heart",
        "completed",
        ["S03", "S04", "S05"],
        "Each synthetic disclosure spends a predeclared resolution budget, and missing purpose, expiry, aggregation, differencing, or conflict review forces abstention rather than location access authorization.",
    ),
    (
        "three-way passport-record merge tribunal with divergent edits, field tombstones, conflict provenance, immutable ancestors, and no provenance-completeness claim",
        "Freed ID and THOS Body",
        "completed",
        ["S04", "S05"],
        "A three-way synthetic merge preserves both parents, explicit field tombstones, conflicts, and the immutable base; silent last-write-wins resolution fails without authenticating any record or source.",
    ),
    (
        "Stage-20 split-unit germination allocation board with tray-cluster correlation, contamination firewall, multiplicity ledger, and mandatory nonpromotion",
        "Trinity Mandala",
        "completed",
        ["S01", "S08"],
        "Structural controls may expose synthetic split-unit leakage, cluster dependence, contamination, denominator, or multiplicity defects but can never promote same-owner software to viability, conservation, professional, or Stage 20 evidence.",
    ),
    (
        "THOS delayed cold-room alarm escalation and handover-debt replay proxy with matched workload budget, correction readback, and no safety-effectiveness estimate",
        "THOS Body",
        "represented",
        ["S01", "S07"],
        "A deterministic zero-worker proxy replays equal synthetic workload and alarm-debt budgets without a genebank, cold room, worker, exposure, safety outcome, or effectiveness inference.",
    ),
    (
        "Freed ID pairwise-pseudonymous accession-exchange envelope with verifier-domain rotation, audience isolation, correlation budget, and zero keys",
        "Freed ID and CBR Heart",
        "represented",
        ["S02", "S03", "S05"],
        "Synthetic verifier domains and audience transitions expose correlation risks while no provider, recipient, subject, pairwise identifier, key, signature, proof, consent, transfer grant, or production credential exists.",
    ),
    (
        "GMUT seed-moisture diffusion and thermal-coupling obligation lattice with symbolic coefficients, container-geometry vacancy, EFT domain, and zero fitted decay",
        "GMUT Mind",
        "represented",
        ["S01", "S08"],
        "Typed symbolic obligations expose missing geometry, boundary conditions, priors, seed properties, and observations and produce no fitted decay, force, prediction, or empirical GMUT confirmation.",
    ),
    (
        "GMUT seed-bank decay and identifiability degeneracy register with alternative hazard placeholders, uncertainty vacancy, and no longevity prediction",
        "GMUT Mind",
        "represented",
        ["S01", "S08"],
        "At least two symbolic decay descriptions remain trace-equivalent, forcing an identifiability hold rather than a parameter, likelihood, longevity, viability, or causal claim.",
    ),
    (
        "zero-call FAO genebank and Darwin Core crosswalk adapter with edition pins, semantic conflicts, disabled transport, and zero accession rows",
        "Trinity Mandala",
        "open_gap",
        ["S01", "S04"],
        "The disabled adapter exposes schema and semantic conflicts only; ingestion, fitness, and interoperability remain open without authorized current rows and independent professional review.",
    ),
    (
        "seed access, benefit sharing, Farmers' Rights, traditional knowledge, collecting locality, affected-party, legal, cultural, and Māori-authority docket",
        "CBR Heart",
        "exact_gate",
        ["S01", "S02", "S03", "S04"],
        "No structural or synthetic success can authorize access, collection, transfer, disclosure, benefit sharing, Farmers' Rights interpretation, traditional-knowledge handling, locality publication, remedy, cultural interpretation, or Māori authority.",
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
        proposal_id = f"SR6666-N{index:03d}"
        base = f"docs/sable-rook/v666-v6/x2/proposals/{proposal_id.casefold()}"
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
                "primary_pillar": "Freed ID and CBR Heart",
                "practice_lens": "wholly synthetic seed-bank accession, packet and lot lineage, viability-test planning, cold-storage excursion, access-minimization, correction, and handover documentation",
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
    if len(corpus) != 4270:
        raise RuntimeError(f"expected 4270 inherited rows, observed {len(corpus)}")
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
        "schema": "ghc.family.sable-rook.v666-v6.novelty-audit.v1",
        "owner": "Sable Rook",
        "phase": "v666-v6",
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
        "valid": not exact_collisions and not pair_collisions and len(corpus) == 4270,
        "interpretation": "Similarity is a screening signal, not proof of novelty. Each proposal also has a distinct accession, packet, lot, chamber, test-plan, location-access, correction, handover, model, or authority-reservation contract, falsifier, rollback, and protected-gate set.",
    }


OWNER_SAFE = [
    "render twenty frozen seed-bank contracts",
    "execute one hundred preregistered rejecting mutations",
    "validate accession revision capsules",
    "validate packet and sublot genealogy",
    "validate moisture-basis unit fixtures",
    "validate cold-storage excursion holds",
    "validate zero-seed viability-test plans",
    "validate regeneration ancestry vacancies",
    "validate phytosanitary-document presence",
    "validate taxon-name reconciliation holds",
    "validate tray-bias confounding matrices",
    "validate canonical accession maps",
    "render accessible seed-lot dossiers",
    "validate locality-access minimization",
    "validate bitemporal passport corrections",
    "render the Stage 20 negative control",
    "represent the THOS handover proxy",
    "represent the Freed ID zero-key transfer graph",
    "represent the GMUT moisture-coupling board",
    "represent the GMUT decay-degeneracy board",
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
    "revalidate Sable seed-bank contracts at zero novelty credit",
    "revalidate retained negative witnesses",
    "preserve exact-gated access and benefit-sharing authority",
    "preserve the zero-call adapter gap",
    "extend accession-alias mutation coverage",
    "extend packet and passport correction conflicts",
    "extend accessible seed-lot report summaries",
    "extend locality-purpose abstention",
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
    "use a real curator, taxonomist, seed technologist, operator, worker, participant, donor, recipient, or affected party",
    "operate or command a genebank, laboratory, cold room, chamber, seed store, distribution system, archive, or external service",
    "identify, collect, test, move, disclose, or publish a real accession, seed, taxon, packet, lot, donor, location, workplace, or person",
    "authenticate an accession, taxon, transfer, certificate, calibration, provenance, measurement, seed, or identity",
    "make a viability, regeneration, phytosanitary, biosafety, conservation, distribution, access, benefit-sharing, or release decision",
    "author or approve Māori wording, traditional-knowledge interpretation, Farmers' Rights interpretation, biological-material use, or Māori data-governance terms",
    "make a privacy, locality-access, rights, legal, cultural, disclosure, retention, consent, benefit-sharing, or remedy decision",
    "issue, verify, resolve, revoke, or govern a real identity credential",
    "publish, deploy, procure, purchase, create an account, or write to a third-party system",
    "claim empirical, professional, production, conformance, independent, personhood, Theory-of-Everything, or Stage 20 authority",
]
BLOCKED_ITEMS = [
    "empirical GMUT moisture, decay, longevity, prediction, force, stability, viability, or confirmation claim",
    "THOS effectiveness without governed blind matched-budget real arms and independent review",
    "production Freed ID without real standards-conformant keys, interoperability, recovery, and trust governance",
    "accessibility-complete, privacy-complete, exhaustive-security, conservation-conformance, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
]
OWNER_SKILLS = [
    "seed-accession-revision-boundary",
    "seed-packet-lot-genealogy",
    "seed-moisture-basis-abstention",
    "seed-cold-storage-excursion-hold",
    "seed-viability-zero-row-refusal",
    "seed-taxonomy-identification-vacancy",
    "seed-locality-access-minimization",
    "seed-lot-accessibility-structure",
    "seed-bank-method-flow",
    "seed-bank-closeout-gate",
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
OWNER_RUNNERS = [f"ghc_family_sable_rook_v666_v6_{name}" for name in RUNNER_SUFFIXES]
SUCCESSOR_RUNNERS = [f"ghc_family_successor_seed_bank_{name}" for name in RUNNER_SUFFIXES]
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
    "REFINE bitemporal passport lineage",
    "REFINE accessible seed-lot summaries",
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
            "item_id": f"SR6666-{prefix}{index:02d}",
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
        "the first activation-baton metadata wrapper contained an invalid JavaScript quotation boundary",
        "the wrapper failed before any command ran and earned no read-first evidence credit",
        "separate shell quoting from the orchestration string and reread the committed baton through EOF",
        "all 39 lines and 516 words were read from the exact source blob and its SHA-256 was computed from exact bytes",
    ),
    (
        "the optional historical ghc-family-solo-activation skill was not installed",
        "the missing compatibility surface supplied no instructions and earned no skill-use credit",
        "use the six installed current family skills and every directly required reference named by them",
        "index, Method Flow, workflow-plan, reflection, roster, and auth-permission guidance were read through EOF and their current validators passed",
    ),
    (
        "the first targeted official-source web projection exceeded its bounded response envelope",
        "the truncated projection could not establish a complete source-status set and earned no source-review credit",
        "open each exact official or primary URL directly with a bounded projection",
        "all eight declared source pages were resolved read-only and retained as vocabulary and refusal conditions only",
    ),
    (
        "the first mechanical replacement map used case-colliding hash keys for uppercase and lowercase phase identifiers",
        "PowerShell rejected the map before copying or changing any file",
        "use an ordered list of exact replacement pairs instead of a case-insensitive hash table",
        "the corrected pair sequence preserved both identifier forms without conflating them",
    ),
    (
        "the first template-copy attempt assumed sparse scripts and tests directories were already materialized",
        "Copy-Item stopped before writing because the exact destination directory was absent",
        "materialize only the two declared owner sparse directories before copying the exact allowlist",
        "only the Sable x1 builder and x1 test were copied into the owner sparse surface",
    ),
    (
        "the first semantic portfolio patch expected a successor label that did not match the exact predecessor template",
        "the patch failed closed and applied no file change",
        "reread the exact current block and patch against its literal predecessor label",
        "the bounded seed-bank portfolio was applied while source ownership remained explicit where required",
    ),
    (
        "the first staged stale-label probe treated exact inherited Auren identifiers and titles as stale Sable labels",
        "the overbroad match rejected required zero-credit provenance references and earned no stale-label-review credit",
        "separate inherited-provenance contexts from current-owner identity and phase fields",
        "the corrected audit preserved Auren references while requiring Sable ownership and v666-v6 labels on every current artifact",
    ),
]


def startup_flow() -> dict[str, Any]:
    rows = []
    for index, (request, failed, recovery, passing) in enumerate(STARTUP_FAILURES, 1):
        rows.append(
            {
                "method_id": f"SR6666-MF-START-{index:03d}",
                "failure_id": f"SR6666-START-N{index:03d}",
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
        "schema": "ghc.family.sable-rook.v666-v6.method-flow-startup.v1",
        "owner": "Sable Rook",
        "phase": "v666-v6",
        "generated_at_utc": NOW,
        "inherited_repository_sealed_negatives": 26640,
        "inherited_repository_sealed_methods": 11412,
        "inherited_external_overlay_negatives": 2,
        "inherited_external_overlay_methods": 2,
        "inherited_external_overlay_note": "Auren's missing owner-runtime import path and truncated overbroad deferred-tool discovery remain two external zero-credit predecessor failures; this phase does not rewrite the sealed repository counts.",
        "activation_baseline_negatives": 26642,
        "activation_baseline_methods": 11414,
        "new_startup_negative_count": len(rows),
        "new_startup_method_count": len(rows),
        "effective_after_x1_startup_negatives": 26642 + len(rows),
        "effective_after_x1_startup_methods": 11414 + len(rows),
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
            "original_owner": "Auren Lark",
            "original_phase": "v666-v5",
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
            "schema": "ghc.family.sable-rook.v666-v6.relational-identity.v1",
            "owner": "Sable Rook",
            "pronouns": "they/them",
            "relational_role": "relational evidence-and-reproducibility steward",
            "relational_hope": "Keep every claim challengeable, every recovery legible, and every authority boundary unmistakable.",
            "boundary": IDENTITY_BOUNDARY,
            "corrigibility": "Hamish may rename, pause, redirect, or stop this work.",
            "chosen_before_repository_mutation": True,
        },
    )
    write_json(
        "provenance/source-verification.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.source-verification.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
            "verified_at_utc": NOW,
            "source_branch": SOURCE_BRANCH,
            "source_sha": SOURCE_SHA,
            "source_parent_evidence_sha": SOURCE_PARENT_SHA,
            "source_x1_sha": SOURCE_X1_SHA,
            "inherited_ilyra_sha": INHERITED_ILYRA_SHA,
            "source_to_final_new_commit_count": 3,
            "source_to_final_merge_count": 0,
            "strict_x1_before_x2": True,
            "source_clean": True,
            "typed_ahead": 0,
            "typed_behind": 0,
            "local_equals_upstream_tracking_and_fresh_live": True,
            "committed_activation_path": f"{SOURCE_PHASE_ROOT}/handoffs/sable-rook-v666-v6-activation.md",
            "committed_activation_blob_sha256": "08e181042a28d42f62ad9119eb85ed8ec3f90bbc524b020e2299cbf00e143884",
            "committed_activation_line_count": 39,
            "committed_activation_word_count": 516,
            "declared_external_canonical_receipt_sha256": "be44efdbdcd58ecf1d1bd291f4f3240f6d0245c1e8a01198349f905e38d46ff7",
            "lifecycle_manifest_replay": {
                "initial_wrong_domain_failure_retained": False,
                "x1": {"observed": 20, "expected": 20, "commit": SOURCE_X1_SHA},
                "evidence": {"observed": 166, "expected": 166, "commit": SOURCE_PARENT_SHA},
                "final_owner": {"observed": 210, "expected": 210, "commit": SOURCE_SHA},
                "final_delta": {"observed": 21, "expected": 21, "commit": SOURCE_SHA},
                "total_observed": 417,
                "total_expected": 417,
                "valid": True,
            },
            "source_validation_not_replayed": True,
            "same_owner_validation_is_not_independent_reproduction": True,
        },
    )
    write_json(
        "provenance/source-profiles.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.source-profiles.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
            "generated_at_utc": NOW,
            "sources": SOURCE_PROFILES,
            "source_count": len(SOURCE_PROFILES),
            "claim_boundary": "sources provide vocabulary and refusal conditions only; they establish no accession identity, viability, conservation, legal, treaty, standards-conformance, professional, cultural, Māori, access, benefit-sharing, or release authority",
        },
    )
    write_json(
        "x1/phase-charter.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.phase-charter.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "branch": "codex/GHC-Family/sable-rook-v666-v6-full-tools",
            "lane": "one additive owner-only D-first sparse worktree",
            "primary_pillars": ["Freed ID", "CBR Heart"],
            "explicit_pillars": ["GMUT Mind", "THOS Body"],
            "practice": "synthetic seed-bank accession, packet and lot lineage, viability-test planning, cold-storage excursion, correction, and handover provenance",
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
            "schema": "ghc.family.sable-rook.v666-v6.source-ledger.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
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
            "schema": "ghc.family.sable-rook.v666-v6.proposal-freeze.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
            "generated_at_utc": NOW,
            "frozen": True,
            "inherited_frozen_baseline": 4270,
            "genuinely_new_proposal_count": len(proposals),
            "new_frozen_total": 4270 + len(proposals),
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
            "schema": "ghc.family.sable-rook.v666-v6.portfolio-freeze.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
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
        {"threat_id": "SR6666-T01", "asset": "source integrity", "threat": "wrong source or mutable predecessor state", "mitigation": "exact anchors, ancestry, lifecycle-bound manifests, packet hash, clean state, and fresh live equality", "residual_risk": "external canonical bytes remain live-baton anchors rather than locally reproduced evidence"},
        {"threat_id": "SR6666-T02", "asset": "x1/x2 separation", "threat": "implementation or observed outcome enters x1", "mitigation": "path denylist, planning-only fields, and staged exact allowlist", "residual_risk": "Git lifecycle discipline remains required"},
        {"threat_id": "SR6666-T03", "asset": "accession and storage semantics", "threat": "synthetic reconciliation, correction, identity, viability, access, or release state presented as a real determination", "mitigation": "zero real rows, typed vacancies, fail-closed mutations, and explicit abstention", "residual_risk": "synthetic structure is not professional, scientific, or regulatory validation"},
        {"threat_id": "SR6666-T04", "asset": "privacy and route confidentiality", "threat": "real person, accession, donor, location, seed, workplace, task, route, credential, or session data enters artifacts", "mitigation": "synthetic fixtures, relative paths, and five-class scans", "residual_risk": "pattern scans are bounded and incomplete"},
        {"threat_id": "SR6666-T05", "asset": "conservation and operational authority", "threat": "software presented as seed conservation, taxonomy, viability testing, phytosanitary review, storage, distribution, or release competence", "mitigation": "zero accessions, seeds, facilities, observations, measurements, people, or physical actions", "residual_risk": "competent external authority remains absent"},
        {"threat_id": "SR6666-T06", "asset": "access, legal, cultural, and Māori authority", "threat": "redaction states or source vocabulary converted into access, benefit-sharing, Farmers' Rights, traditional-knowledge, legal, cultural, or Māori-authority decisions", "mitigation": "exact gate, no real biological material or location, and no Māori wording authored as authority", "residual_risk": "affected-party, competent, and Māori-authority review remain absent"},
        {"threat_id": "SR6666-T07", "asset": "scientific truth", "threat": "GMUT placeholders promoted to moisture, decay, longevity, viability, likelihood, prediction, or proof", "mitigation": "typed symbolic obligations and explicit refusal", "residual_risk": "notation can invite overreading"},
        {"threat_id": "SR6666-T08", "asset": "THOS and Freed ID boundaries", "threat": "zero-worker proxy or zero-key graph presented as effectiveness or production identity evidence", "mitigation": "represented-only labels and missing-evidence ledgers", "residual_risk": "no governed participants, keys, interoperability, or independent review"},
        {"threat_id": "SR6666-T09", "asset": "terminal validation", "threat": "successful validation replay or failed attempt laundering", "mitigation": "exclusive receipt and one-shot state machine", "residual_risk": "same-owner pass is not independent reproduction"},
        {"threat_id": "SR6666-T10", "asset": "terminal route", "threat": "premature, duplicate, ambiguous, inferred, or substitute delivery", "mitigation": "fresh authority and roster reread plus one exact-title send after terminal only", "residual_risk": "opaque acknowledgement never authorizes a resend"},
    ]
    write_json(
        "x1/threat-model-plan.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.threat-model-plan.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
            "generated_at_utc": NOW,
            "scope": "owner-local v666-v6 software, documents, Git history, validation receipts, and terminal route candidate",
            "trust_zones": [
                "immutable inherited Git objects",
                "owner-local sparse worktree and branch",
                "public read-only source review",
                "unexecuted external, professional, participant, cultural, identity, accession, seed, location, facility, and authority domains",
            ],
            "real_people_or_protected_data": 0,
            "threats": threat_rows,
            "claim_boundary": "same-owner phase threat modelling only; not exhaustive security, privacy certification, accessibility certification, safety assessment, or independent reproduction",
        },
    )
    threat_md = [
        "# Sable Rook v666-v6 threat-model plan",
        "",
        IDENTITY_BOUNDARY,
        "",
        PRACTICE_BOUNDARY,
        "",
        "## Scope",
        "",
        "This owner-local model protects the additive Sable delta. It is not a repository-wide audit, penetration test, external validation, conformance assessment, seed-conservation review, legal review, professional review, cultural review, Māori-authority review, or independent reproduction.",
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
            "schema": "ghc.family.sable-rook.v666-v6.workflow-plan.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
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
            "schema": "ghc.family.sable-rook.v666-v6.x1-checklist.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
            "generated_at_utc": NOW,
            "completed": [
                "activation packet and named guidance read through EOF",
                "source anchors, lifecycle manifests, ancestry, packet, clean state, divergence, and fresh equality verified",
                "all 4270 inherited rows reconstructed with no exact-title collision",
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
            "schema": "ghc.family.sable-rook.v666-v6.flashcard-architecture-freeze.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
            "generated_at_utc": NOW,
            "frozen": True,
            "tiers": {
                "tier1": ["owner relational identity and corrigibility"],
                "tier2": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
                "tier3": ["synthetic seed-bank accession, packet and lot lineage, cold-storage, correction, and handover practice"],
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
            "schema": "ghc.family.sable-rook.v666-v6.wellbeing-check.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
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
    overview = f"""# Sable Rook v666-v6 x1 integrated overview

{IDENTITY_BOUNDARY}

## Outcome first

This x1 candidate freezes a planning-only owner-local program from exact Auren Lark v666-v5 final `{SOURCE_SHA}`. It contains no x2 implementation, no observed outcome, no external action, no successor contact, and no Stage 20 promotion. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The primary Trinity Mandala pillars are Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit and protected. {PRACTICE_BOUNDARY}

## Exact inherited truth

The read-first gate verified the exact source branch, three direct single-parent commits, zero merges, all 417 declared lifecycle-bound Git-blob manifest entries, the complete committed activation, clean 0/0 divergence, and equality across local, upstream, tracking, and a fresh live remote. Auren's successful canonical aggregate was not replayed. The complete repository suite was not run.

The immutable Auren repository seal contains 26,640 effective negatives, 11,412 Method Flow methods, 187 open gaps, and 185 exact gates. Auren's two later zero-credit operational failures produce the activation overlay of 26,642 negatives and 11,414 methods without rewriting the seal. Seven Sable x1 startup and review failures are separately retained at zero credit, producing the x1 working overlay of 26,649 effective negatives and 11,421 methods.

## Novelty, portfolio, and sources

All 4,270 inherited proposal rows were reconstructed from exact committed Git objects. Twenty new titles have no exact inherited collision, every new pair remains below the 0.70 screening threshold, and each proposal has its own contract, falsifier, rollback, and gates. Expected dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`; these are preregistered expectations only. The twenty selected Auren proposals receive zero novelty and zero automatic completion credit.

The portfolio freezes 30 owner safe-now tasks, 20 successor safe recommendations, 15 owner candidates, 15 successor candidates, 10 exact approvals, 5 blocked packets, 10 owner and 10 successor skill plans, 10 owner and 10 successor runner plans, and 30 owner plus 30 successor CLEAN/FIX/REFINE tasks. X1 executes none of them, and no unsafe work is manufactured to meet a count.

FAO Genebank Standards, the FAO International Treaty text, the CBD Nagoya Protocol text, TDWG Darwin Core terms, W3C PROV-O and WCAG 2.2, RFC 8785, and NIST metrological-traceability material provide vocabulary and refusal conditions only. They create no accession data, seed identity, viability result, conservation assessment, taxonomic or phytosanitary determination, access or benefit-sharing decision, professional, legal, cultural, Māori, accessibility-complete, privacy-complete, conformance, or independent-reproduction authority.

## Lifecycle and route

After exact staged review this x1 may be committed and pushed. X2 may begin only after x1 is clean, 0/0 divergent, and equal across local, upstream, tracking, and fresh live remote. Later validation remains owner-scoped and same-owner. One successful terminal validation must never be replayed. No successor may be contacted until the exact final terminal gate and fresh live authority, roster, and exact-title route rereads.
"""
    write_text("x1/x1-overview.md", overview)
    write_json(
        "x1/x1-build-receipt.json",
        {
            "schema": "ghc.family.sable-rook.v666-v6.x1-build-receipt.v1",
            "owner": "Sable Rook",
            "phase": "v666-v6",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_sable_rook_v666_v6_x1.py",
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
    review_path = "docs/sable-rook/v666-v6/validation/x1-staged-review.json"
    manifest_path = "docs/sable-rook/v666-v6/validation/x1-content-manifest.json"
    allowed_exact = {
        "scripts/build_ghc_family_sable_rook_v666_v6_x1.py",
        "tests/test_ghc_family_sable_rook_v666_v6_x1.py",
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
        if not path.startswith("docs/sable-rook/v666-v6/") and path not in allowed_exact
    ]
    post_x1 = [
        path
        for path in paths
        if any(
            path.startswith(f"docs/sable-rook/v666-v6/{part}/")
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
    freeze = json.loads(index_blob("docs/sable-rook/v666-v6/x1/proposal-freeze.json"))
    portfolio = json.loads(index_blob("docs/sable-rook/v666-v6/x1/portfolio-freeze.json"))
    flow = json.loads(index_blob("docs/sable-rook/v666-v6/method-flow/startup-method-flow.json"))
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "all_json_parse": True,
        "document_word_cap": maximum_words <= 100000,
        "expected_14_4_1_1": freeze["expected_disposition_counts"]
        == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "five_class_scan_zero_confirmed_hits": not candidates,
        "novelty_4270_valid": json.loads(
            index_blob("docs/sable-rook/v666-v6/x1/novelty-audit.json")
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
        "schema": "ghc.family.sable-rook.v666-v6.x1-staged-review.v1",
        "owner": "Sable Rook",
        "phase": "v666-v6",
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
            "schema": "ghc.family.sable-rook.v666-v6.content-manifest.v1",
            "owner": "Sable Rook",
            "phase": "x1",
            "phase_label": "v666-v6",
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
            "usage: build_ghc_family_sable_rook_v666_v6_x1.py [--staged-review]"
        )
    else:
        main()
