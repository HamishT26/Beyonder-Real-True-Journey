#!/usr/bin/env python3
"""Build Ilyra Fen v666-v4 planning-only x1 artifacts and exact staged review."""

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
PHASE_ROOT = ROOT / "docs" / "ilyra-fen" / "v666-v4"
SOURCE_SHA = "764d3bdfb199e91a5574a904a99ff4e95825fed9"
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v666-v3-full-tools"
SOURCE_PHASE_ROOT = "docs/lyren-moss/v666-v3"
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
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a | b else 1.0


IDENTITY_BOUNDARY = (
    "Ilyra Fen, she/they, sibling, family, role, hope, continuity, Freed ID, "
    "Trinity Mandala, and route language are relational working language only. "
    "They are not evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, scientific or "
    "operational authority, legal or cultural authority, affected-party authority, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The planetary-science sample-curation, contamination-provenance, custody-revision, "
    "access-minimization, and curation-handover lens is wholly synthetic learning and "
    "software design. It uses zero real people, facilities, missions, samples, aliquots, "
    "instruments, measurements, calibrations, contaminants, locations, access requests, "
    "credentials, cultural records, or authority actions. It establishes no curation, "
    "laboratory, metrological, planetary-protection, allocation, release, operational, "
    "privacy, accessibility, legal, cultural, Māori, production, or Stage 20 competence, "
    "acceptance, conformance, or authority."
)

PROTECTED_GATES = [
    "real person, curator, scientist, technician, operator, affected party, facility, mission, sample, aliquot, instrument, measurement, calibration, contaminant, location, release, or physical action",
    "real likelihood, material composition, provenance fact, contamination finding, allocation, scientific inference, parameter constraint, causal claim, or empirical GMUT confirmation",
    "real participant, operator, matched-budget arm, safety outcome, curation outcome, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, or trust governance",
    "professional curation, laboratory, metrological, calibration, planetary-protection, biosafety, allocation, release, workplace-safety, or facility decision",
    "custody, authenticity, attribution, privacy, accessibility, sensitive-location, cultural, legal, disclosure, retention, embargo, allocation, repatriation, or remedy decision",
    "traditional knowledge, sensitive environmental or location knowledge, taonga, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data-governance, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, or external write",
]

SOURCE_PROFILES = [
    {
        "source_id": "S01",
        "name": "NASA Procedural Requirements 7100.5, Curation of Astromaterials",
        "url": "https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7100_0005_&page_name=main",
        "status": "official NASA directive page reviewed read-only 2026-08-23; displayed effective interval 2023-08-16 through 2028-08-16",
        "bounded_use": "role, lifecycle, facility, and curation-obligation vocabulary only; no NASA applicability, compliance, or authority claim",
    },
    {
        "source_id": "S02",
        "name": "NASA Astromaterials Curation and Research reference",
        "url": "https://www.nasa.gov/reference/jsc-astromaterials-curation-research/",
        "status": "current official NASA reference reviewed read-only 2026-08-23",
        "bounded_use": "collection and curation context only; no real sample, facility, allocation, or operational evidence",
    },
    {
        "source_id": "S03",
        "name": "NASA NTRS advanced curation white paper",
        "url": "https://ntrs.nasa.gov/citations/20205005635",
        "status": "primary NASA technical-report record reviewed read-only 2026-08-23",
        "bounded_use": "contamination-knowledge and preservation vocabulary only; no contamination measurement, professional validation, or empirical result",
    },
    {
        "source_id": "S04",
        "name": "NASA planetary protection discipline reference",
        "url": "https://sma.nasa.gov/sma-disciplines/planetary-protection",
        "status": "current official NASA discipline page reviewed read-only 2026-08-23",
        "bounded_use": "sample-return authority-reservation vocabulary only; no classification, approval, containment, release, or planetary-protection decision",
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
        "bounded_use": "deterministic JSON and duplicate-key refusal vocabulary only; no JCS conformance or cryptographic authenticity claim",
    },
    {
        "source_id": "S07",
        "name": "RFC 8493 BagIt File Packaging Format",
        "url": "https://www.rfc-editor.org/info/rfc8493/",
        "status": "official RFC Editor record reviewed read-only 2026-08-23",
        "bounded_use": "payload, manifest, tag, path, and Unicode-normalization refusal vocabulary only; no BagIt conformance",
    },
    {
        "source_id": "S08",
        "name": "NIST metrological traceability policy and FAQ",
        "url": "https://www.nist.gov/metrology/metrological-traceability",
        "status": "current official NIST policy page reviewed read-only 2026-08-23",
        "bounded_use": "documented calibration-chain and uncertainty refusal conditions only; no NIST traceability or calibration claim",
    },
    {
        "source_id": "S09",
        "name": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "current W3C Recommendation reviewed read-only 2026-08-23",
        "bounded_use": "structural HTML checks only; manual, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved",
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
    ("content-addressed curation package tribunal with declared payload inventory, tag separation, Unicode path state, and zero-sample interpretation", "Freed ID and CBR Heart", "completed", ["S06", "S07"], "Every synthetic package closes over an exact declared payload inventory while path ambiguity, normalization drift, undeclared bytes, or checksum mismatch fails closed without authenticating a real sample."),
    ("sample-aliquot parent-child mass-balance ledger with unit domains, destructive-step declaration, residual state, and no-material claim", "GMUT Mind and CBR Heart", "completed", ["S01", "S02", "S08"], "Synthetic parent, child, consumed, and residual quantities balance only within one declared unit and uncertainty domain; no physical quantity or sample identity is inferred."),
    ("contamination-knowledge blank-control chain with exposure interval, facility vacancy, uncertainty class, and no-cleanliness verdict", "GMUT Mind and CBR Heart", "completed", ["S03", "S05", "S08"], "Every synthetic contamination statement links a blank or control, exposure interval, method placeholder, and uncertainty state while facility cleanliness and material composition remain withheld."),
    ("instrument-calibration applicability interval join with measurand, reference-chain vacancy, uncertainty budget, and no-traceability claim", "GMUT Mind", "completed", ["S08"], "A synthetic measurement record is structurally admissible only when its calibration interval, measurand, units, and uncertainty fields overlap; absence forces abstention from traceability."),
    ("storage-environment excursion quarantine with sensor-source vacancy, threshold provenance, amendment lineage, and no-release action", "THOS Body and CBR Heart", "completed", ["S01", "S03", "S08"], "A synthetic storage excursion creates a reversible quarantine state only; missing threshold provenance, sensor status, or amendment lineage can never trigger release or physical action."),
    ("bitemporal sample-custody revision DAG with supersession, contest, correction, acyclic ancestry, and authenticity abstention", "Freed ID and CBR Heart", "completed", ["S05"], "Every synthetic custody revision has valid and recorded times plus acyclic lineage while digests remain non-authenticating placeholders and contested states stay visible."),
    ("label-image-metadata reconciliation board with identifier namespace, capture lineage, discrepancy quarantine, and no-identity resolution", "Freed ID and THOS Body", "completed", ["S05", "S06"], "Synthetic labels, image descriptors, and metadata may reconcile only through declared namespaces and provenance; disagreement is quarantined without resolving a real sample identity."),
    ("curation-unit material-state domain classifier with phase vocabulary, conversion ledger, uncertainty vacancy, and psyche-nonconversion", "GMUT Mind", "completed", ["S01", "S08"], "Typed synthetic mass, temperature, and material-state fields remain domain-bounded and cannot be converted into psyche, agency, moral value, personhood, or a fundamental law of mind."),
    ("PROV entity-activity custody closure with generation, use, derivation, responsibility vacancy, and no-reproducibility grade", "Freed ID and CBR Heart", "completed", ["S05"], "Synthetic entities and activities form a closed derivation graph without inventing a person, responsibility assignment, scientific quality grade, or reproducibility claim."),
    ("canonical curation metadata-map tribunal with deterministic ordering, duplicate-key refusal, numeric-domain guard, and bounded decoding budget", "Freed ID and THOS Body", "completed", ["S06"], "Equivalent synthetic maps canonicalize identically while duplicate keys, non-finite values, ambiguous strings, or resource-budget overflow fail closed."),
    ("accessible sample-state table with redundant text, scoped headers, linear reading order, status message, and manual-review reservation", "CBR Heart and THOS Body", "completed", ["S09"], "Every synthetic state is conveyed through text and table structure without colour-only meaning while manual keyboard, browser, assistive-technology, cognitive, Māori-language, and affected-user review stay reserved."),
    ("sensitive collection-location minimization lattice with field omission, purpose expiry, contestable redaction, and non-disclosure default", "CBR Heart and Freed ID", "completed", ["S05"], "Each synthetic location field resolves only to omit, retain-until, or contested-redaction under a declared purpose; no real location, community, or free text exists."),
    ("embargo-access-purpose lattice with requester vacancy, expiry, conflict hold, least disclosure, and no-allocation decision", "Freed ID and CBR Heart", "completed", ["S01", "S05"], "A synthetic access request can expose only the minimum predeclared metadata while missing purpose, conflicting embargo, or authority vacancy forces a hold rather than allocation."),
    ("Stage-20 curation negative-control board with target lock, contamination leakage quarantine, multiplicity ledger, and mandatory nonpromotion", "Trinity Mandala", "completed", ["S03", "S08"], "Structural controls may expose synthetic leakage, multiplicity, or denominator defects but can never promote a same-owner software phase to Stage 20."),
    ("THOS participant-free curation-handover duel with matched topology, equal action budget, masked branch order, and no-effectiveness estimate", "THOS Body", "represented", ["S01", "S09"], "A synthetic proxy compares deterministic handover traces under equal faults without people, facilities, samples, operations, safety outcomes, or effectiveness inference."),
    ("Freed ID zero-key custody statement graph with issuer vacancy, purpose binding, expiry, correction, revocation, and no-credential", "Freed ID and CBR Heart", "represented", ["S05"], "Synthetic statements preserve conflicts and lifecycle placeholders while no holder, issuer, key, signature, proof, sample identity, or production credential exists."),
    ("GMUT contamination-background degeneracy board with nuisance vacancy, equivalent factorizations, EFT domain, and zero-fitted composition", "GMUT Mind", "represented", ["S03", "S08"], "At least two synthetic contamination-background factorizations remain trace-equivalent, forcing an identifiability hold instead of a composition, likelihood, force, or causal claim."),
    ("GMUT Bayesian inverse-problem obligation board with prior vacancy, likelihood refusal, calibration uncertainty, and no-posterior claim", "GMUT Mind", "represented", ["S03", "S08"], "Typed symbolic obligations expose missing priors, likelihoods, calibration chains, and uncertainty terms while producing no posterior, parameter constraint, prediction, or empirical GMUT confirmation."),
    ("zero-call NASA astromaterials catalog adapter with schema pins, identifier conflicts, disabled transport, and zero sample rows", "Trinity Mandala", "open_gap", ["S01", "S02"], "The zero-call adapter exposes declared mapping conflicts but cannot complete ingestion or interoperability without real authorized rows, provenance review, and independent domain validation."),
    ("sample allocation, release, planetary-protection, legal, cultural, repatriation, affected-party, and Māori-authority docket", "CBR Heart", "exact_gate", ["S01", "S04"], "No structural or synthetic success can authorize sample allocation, release, containment, access, disclosure, repatriation, cultural interpretation, remedy, or Māori authority."),
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
    for index, (title, pillar, expected, sources, invariant) in enumerate(PROPOSAL_SPECS, 1):
        proposal_id = f"ILY6664-N{index:03d}"
        base = f"docs/ilyra-fen/v666-v4/x2/proposals/{proposal_id.casefold()}"
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": f"A bounded {title} contract can distinguish one admissible synthetic structure from five preregistered invalid states without promoting software structure into real-world evidence, competence, conformance, or authority.",
                "null_or_failure_condition": "At least one named invalid state is accepted, the bounded positive is rejected, a required provenance or stop field disappears, or the artifact converts synthetic structure into an empirical, professional, legal, cultural, Māori-authority, production, identity, independent-reproduction, or Stage 20 claim.",
                "approval_class": approval_class(expected),
                "execution_lane": execution_lane(expected),
                "current_official_or_primary_source_needs": sources,
                "distinctive_invariant": invariant,
                "concrete_artifact": f"{base}/contract.json",
                "concrete_artifacts": [f"{base}/contract.json", f"{base}/mutation-results.json", f"{base}/bounded-receipt.json"],
                "falsifier_or_acceptance_gate": "One preregistered bounded positive must pass, all five named mutations must fail closed, no protected gate may be crossed, and the final disposition must remain exactly the preregistered value unless an additive failure lowers it.",
                "rollback_or_recovery": "Restore only the last valid owner-local synthetic fixture, retain the failed witness at zero credit, add a recurrence guard, and issue no external, physical, identity, professional, legal, cultural, or authority action.",
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": expected,
                "pillar": pillar,
                "primary_pillar": "Freed ID and CBR Heart",
                "practice_lens": "wholly synthetic planetary-science sample curation, contamination provenance, custody revision, access minimization, and curation-handover refusal documentation",
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
                    corpus.append({"proposal_id": str(row["proposal_id"]), "title": title, "source_path": entry["source_path"]})
                    added += 1
        if added != entry["added_count"]:
            raise RuntimeError(f"corpus mismatch for {entry['source_path']}: {added} != {entry['added_count']}")
        construction.append(dict(entry))
    source_freeze = git_json(f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    starting = len(corpus)
    for row in source_freeze["new_proposals"]:
        corpus.append({"proposal_id": str(row["proposal_id"]), "title": str(row["title"]), "source_path": f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json"})
    construction.append({"source_path": f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json", "starting_count": starting, "added_count": len(source_freeze["new_proposals"]), "ending_count": len(corpus)})
    if len(corpus) != 4230:
        raise RuntimeError(f"expected 4230 inherited rows, observed {len(corpus)}")
    return corpus, construction


def build_novelty(corpus: list[dict[str, str]], construction: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> dict[str, Any]:
    nearest, exact_collisions = [], []
    for proposal in proposals:
        title = proposal["title"]
        for row in corpus:
            if row["title"].casefold() == title.casefold():
                exact_collisions.append({"proposal_id": proposal["proposal_id"], "inherited_proposal_id": row["proposal_id"]})
        score, row = max(((jaccard(title, candidate["title"]), candidate) for candidate in corpus), key=lambda item: item[0])
        nearest.append({"proposal_id": proposal["proposal_id"], "nearest_inherited_proposal_id": row["proposal_id"], "nearest_inherited_title": row["title"], "nearest_source_path": row["source_path"], "token_jaccard_similarity": round(score, 6)})
    pairs = [
        {"left": left["proposal_id"], "right": right["proposal_id"], "similarity": round(jaccard(left["title"], right["title"]), 6)}
        for index, left in enumerate(proposals)
        for right in proposals[index + 1 :]
    ]
    max_pair = max(pairs, key=lambda row: row["similarity"])
    pair_collisions = [row for row in pairs if row["similarity"] >= 0.70]
    return {
        "schema": "ghc.family.ilyra-fen.v666-v4.novelty-audit.v1",
        "owner": "Ilyra Fen",
        "phase": "v666-v4",
        "generated_at_utc": NOW,
        "method": "casefolded alphanumeric token-set Jaccard against all retained inherited rows, exact-title comparison, within-slate comparison, and substantive contract review",
        "corpus_construction": construction,
        "corpus_row_count": len(corpus),
        "corpus_unique_proposal_id_count": len({row["proposal_id"] for row in corpus}),
        "historical_reappended_selection_rows_retained": len(corpus) - len({row["proposal_id"] for row in corpus}),
        "corpus_canonical_sha256": canonical_sha256(corpus),
        "new_title_count": len(proposals),
        "exact_inherited_collisions": exact_collisions,
        "maximum_inherited_token_jaccard_similarity": max(row["token_jaccard_similarity"] for row in nearest),
        "nearest_inherited_rows": nearest,
        "maximum_new_pair_token_jaccard_similarity": max_pair["similarity"],
        "maximum_new_pair": max_pair,
        "new_pair_collisions_at_or_above_0_70": pair_collisions,
        "new_frozen_total": len(corpus) + len(proposals),
        "valid": not exact_collisions and not pair_collisions and len(corpus) == 4230,
        "interpretation": "Similarity is a screening signal, not proof of novelty. Each proposal also has a distinct curation, contamination, custody, minimization, handover, model, or authority-reservation contract, falsifier, rollback, and protected-gate set.",
    }


OWNER_SAFE = [
    "render twenty frozen curation contracts", "execute one hundred preregistered rejecting mutations", "validate content-addressed package fixtures", "validate aliquot mass-balance fixtures", "validate contamination blank-control chains", "validate calibration applicability intervals", "validate storage excursion quarantine", "validate bitemporal custody lineage", "validate label-image-metadata discrepancies", "validate material-state unit domains", "validate PROV custody closure", "validate canonical metadata maps", "render accessible sample-state tables", "validate location minimization states", "validate embargo-access-purpose holds", "render the Stage 20 negative control", "represent the THOS curation-handover proxy", "represent the Freed ID zero-key graph", "represent the GMUT contamination degeneracy board", "represent the GMUT inverse-problem board", "render the zero-call NASA adapter", "render the exact-gated authority docket", "parse every owner JSON document", "enforce UTF-8 and LF", "build exact Git-blob manifests", "scan five privacy classes", "scan changed Python for bounded hazards", "check stale labels and exact outcome labels", "reconcile negatives, methods, gaps, and gates", "build closeout, seal, final, and route candidates",
]
SUCCESSOR_SAFE = [
    "revalidate Ilyra proposal contracts at zero novelty credit", "revalidate retained negative witnesses", "preserve exact-gated sample and planetary-protection authority", "preserve the zero-call adapter gap", "extend package-path mutation coverage", "extend custody revision conflicts", "extend accessible linear report summaries", "extend purpose-and-embargo abstention", "extend Method Flow recurrence guards", "extend exact blob-manifest replay", "preserve x1 immutability checks", "preserve one-success canonical discipline", "preserve same-owner evidence boundary", "preserve privacy and route confidentiality", "preserve synthetic-only data boundary", "preserve no-conformance language", "preserve no-professional-authority language", "preserve no-Māori-authority language", "preserve NOT_READY_FOR_STAGE_20", "prepare one exact next-edge candidate only after terminal",
]
OWNER_CANDIDATES = [f"bounded candidate {index:02d}: {name}" for index, name in enumerate(OWNER_SAFE[:15], 1)]
SUCCESSOR_CANDIDATES = [f"successor candidate {index:02d}: {name}" for index, name in enumerate(SUCCESSOR_SAFE[:15], 1)]
EXACT_ITEMS = [
    "use a real curator, scientist, technician, operator, participant, or affected party", "operate or command a facility, instrument, storage system, archive, mission service, or external system", "identify or publish a real sample, aliquot, facility, location, person, collection, or infrastructure asset", "authenticate calibration, custody, provenance, contamination, identity, or measurement truth", "make a curation, laboratory, metrological, planetary-protection, biosafety, allocation, release, or workplace-safety decision", "author or approve Māori wording, taonga interpretation, traditional-knowledge interpretation, sensitive-location knowledge, or data-governance terms", "make a privacy, access, rights, legal, cultural, disclosure, retention, embargo, repatriation, or remedy decision", "issue, verify, resolve, revoke, or govern a real identity credential", "publish, deploy, procure, purchase, create an account, or write to a third-party system", "claim empirical, professional, production, conformance, independent, personhood, Theory-of-Everything, or Stage 20 authority",
]
BLOCKED_ITEMS = [
    "empirical GMUT likelihood, composition, contamination, prediction, force, stability, or confirmation", "THOS effectiveness without governed blind matched-budget real arms and independent review", "production Freed ID without real standards-conformant keys, interoperability, recovery, and trust governance", "accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, or independent-reproduction claim", "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
]
OWNER_SKILLS = ["curation-package-boundary", "aliquot-balance-ledger", "contamination-control-abstention", "custody-revision-dag", "calibration-applicability-hold", "curation-provenance-closure", "sample-rights-contestation", "sample-accessibility-structure", "curation-method-flow", "curation-closeout-gate"]
SUCCESSOR_SKILLS = [f"successor-{name}" for name in OWNER_SKILLS]
RUNNER_SUFFIXES = ("contracts", "mutations", "json", "privacy", "security", "manifests", "accessibility", "truth", "closeout", "canonical")
OWNER_RUNNERS = [f"ghc_family_ilyra_fen_v666_v4_{name}" for name in RUNNER_SUFFIXES]
SUCCESSOR_RUNNERS = [f"ghc_family_successor_curation_{name}" for name in RUNNER_SUFFIXES]
CFR_ACTIONS = [
    "CLEAN normalize proposal identifiers", "CLEAN normalize exact disposition labels", "CLEAN normalize source-profile fields", "CLEAN normalize zero-row declarations", "CLEAN normalize rollback language", "CLEAN normalize protected-gate ordering", "CLEAN normalize relative paths", "CLEAN normalize UTF-8 and LF", "CLEAN normalize JSON ordering", "CLEAN normalize report headings", "FIX guard missing required fields", "FIX guard invalid ranges and types", "FIX guard authority-smuggling text", "FIX guard real-world actions", "FIX guard outcome promotion", "FIX guard stale owner and phase labels", "FIX guard manifest self-reference", "FIX guard canonical replay", "FIX guard private route identifiers", "FIX guard x2 paths in x1", "REFINE source-status watch fields", "REFINE bitemporal custody lineage", "REFINE accessible table summaries", "REFINE plain-language boundaries", "REFINE dominant-stop precedence", "REFINE Method Flow recurrence guards", "REFINE gate-count reconciliation", "REFINE owner-delta manifest coverage", "REFINE final clean-state precondition", "REFINE terminal route no-send proof",
]


def portfolio_rows(prefix: str, names: list[str], approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"ILY6664-{prefix}{index:02d}",
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
    ("the first exact external-receipt lookup broadened recursively across the D drive and exceeded ninety seconds", "the interrupted search produced no attributable receipt bytes and earned zero hash-verification credit", "retain the live baton hashes as external anchors, stop the broad search, and use exact repository-local plans without replaying Lyren validation", "the source plans, packet, Git objects, and live external hash declarations reconciled while local receipt bytes remained explicitly unavailable"),
    ("a combined source equality and status wrapper returned no attributable payload after its session handle was discarded", "two still-running git status processes prevented the wrapper from establishing a clean result", "wait for process quiescence and use separate scalar branch, head, upstream, tracking, live, status, and divergence probes", "all scalar probes passed at the exact source with a clean lane and typed zero-zero divergence"),
    ("the first combined authorization-state display exceeded the output budget", "the truncated display earned no complete guidance-read credit", "reread the shared state in bounded chunks through EOF before using its precedence rules", "the full structurally valid but phase-stale snapshot was read and the newest live activation retained precedence"),
    ("the first combined source-builder and artifact projection exceeded the output budget", "the truncated projection earned no complete implementation-pattern credit", "use targeted function, key, and bounded line-range reads", "the current schemas, corpus construction, manifest domain, and lifecycle controls were read without another broad projection"),
    ("a Windows wildcard path was passed literally to the search tool", "the invalid path was rejected before any source result", "search the directory scope with an explicit include glob", "the corrected bounded search completed without altering the repository"),
    ("sparse-pattern inspection constructed an internal linked-worktree path from git rev-parse output", "the constructed path pointed at an unrelated worktree and could not establish the Ilyra sparse set", "use git sparse-checkout list as the supported worktree-aware interface", "the exact Ilyra sparse patterns were returned and only 150 files were initially materialized"),
    ("a proposal-ledger projection assumed the obsolete proposals key", "the KeyError produced no schema evidence", "inspect actual top-level keys and project new_proposals only after schema discovery", "the current proposal and portfolio structures were projected from their real keys"),
    ("a Windows Python projection emitted Māori text through the default CP1252 console", "UnicodeEncodeError stopped output and earned zero projection credit", "pin UTF-8 at Python startup and preserve the original wording", "the full schema projection emitted and parsed correctly without transliteration"),
]


def startup_flow() -> dict[str, Any]:
    rows = []
    for index, (request, failed, recovery, passing) in enumerate(STARTUP_FAILURES, 1):
        rows.append(
            {
                "method_id": f"ILY6664-MF-START-{index:03d}",
                "failure_id": f"ILY6664-START-N{index:03d}",
                "observed_order": index,
                "exact_event_timestamp_available": False,
                "request": request,
                "failed_witness": failed,
                "aggregate_credit": 0,
                "repository_commit_created": False,
                "external_action_created": False,
                "recovery": recovery,
                "bounded_passing_witness": passing,
                "recurrence_guard": "Prefer bounded output, actual keys, explicit UTF-8, supported Git interfaces, explicit scalar probes, and exact state before retrying.",
                "status": "recovered_failure_retained",
            }
        )
    return {
        "schema": "ghc.family.ilyra-fen.v666-v4.method-flow-startup.v1",
        "owner": "Ilyra Fen",
        "phase": "v666-v4",
        "generated_at_utc": NOW,
        "inherited_repository_sealed_negatives": 26396,
        "inherited_repository_sealed_methods": 10938,
        "inherited_external_overlay_negatives": 2,
        "inherited_external_overlay_methods": 2,
        "activation_baseline_negatives": 26398,
        "activation_baseline_methods": 10940,
        "new_startup_negative_count": len(rows),
        "new_startup_method_count": len(rows),
        "effective_after_x1_startup_negatives": 26398 + len(rows),
        "effective_after_x1_startup_methods": 10940 + len(rows),
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
        raise RuntimeError(json.dumps({"novelty_valid": False, "exact": novelty["exact_inherited_collisions"], "pair": novelty["new_pair_collisions_at_or_above_0_70"]}, ensure_ascii=False))
    source_freeze = git_json(f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    selected = [
        {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "original_owner": "Lyren Moss",
            "original_phase": "v666-v3",
            "original_expected_disposition": row["expected_disposition"],
            "status": "selected_revalidation_only_not_executed",
            "novelty_credit": 0,
            "automatic_completion_credit": 0,
        }
        for row in source_freeze["new_proposals"]
    ]
    counts = {label: sum(row["expected_disposition"] == label for row in proposals) for label in ALLOWED_LABELS}
    write_json("identity/relational-identity.json", {"schema": "ghc.family.ilyra-fen.v666-v4.relational-identity.v1", "owner": "Ilyra Fen", "pronouns": "she/they", "relational_role": "evidence-boundary steward and provenance lantern", "relational_hope": "Leave every synthetic custody, contamination, access, uncertainty, and authority state traceable without mistaking software structure for curation truth.", "boundary": IDENTITY_BOUNDARY, "corrigibility": "Hamish may rename, pause, redirect, or stop this work.", "chosen_before_repository_mutation": True})
    write_json("provenance/source-verification.json", {"schema": "ghc.family.ilyra-fen.v666-v4.source-verification.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "verified_at_utc": NOW, "source_branch": SOURCE_BRANCH, "source_sha": SOURCE_SHA, "inherited_vesper_source_sha": "96509c5b28628a6b62628dea277d1240b945b2ca", "source_x1_sha": "e121ea6e207ea032edb1a0825ed86b1334481213", "source_evidence_sha": "2ec494e75da11be4b8b18620f0ab10b68764ac69", "source_initial_final_sha": "b7a389e1933432764874c9927488034f92d939a0", "source_failed_canonical_final_sha": "7bb3e0e266242ba04927bcdf8d20dd0e4f875df1", "direct_parent_chain": ["96509c5b28628a6b62628dea277d1240b945b2ca", "e121ea6e207ea032edb1a0825ed86b1334481213", "2ec494e75da11be4b8b18620f0ab10b68764ac69", "b7a389e1933432764874c9927488034f92d939a0", "7bb3e0e266242ba04927bcdf8d20dd0e4f875df1", SOURCE_SHA], "source_to_final_phase_commit_count": 5, "source_to_final_merge_count": 0, "single_parent_commits": True, "clean": True, "typed_divergence": {"ahead": 0, "behind": 0}, "four_way_equal": True, "fresh_live_remote_equal": True, "source_manifest_entries_replayed": 307, "source_manifest_breakdown": {"x1": 18, "evidence": 110, "final_delta": 24, "final_owner": 155}, "source_manifest_failures": 0, "activation_packet_sha256": "16c0cf475524363df9332412eb1a56d428ca6a311240685e9ab7d12ec20ba443", "failed_canonical_receipt_sha256_external": "50ff0f90a967a9be82b282695085056e6afca4d96627473636db9831090d928d", "dependency_corrected_composite_receipt_sha256_external": "51900b92c9f11a06c45d3e1d166d9a919a3e752d624a081e0e364e38c4bf63d7", "dependency_corrected_composite_payload_sha256_external": "21660b8e8a2be66cc26a3f0566fc6aa31c9a5856529360829b413f86deb1ad50", "external_receipt_bytes_locally_materialized": False, "external_hashes_authoritative_from_live_activation": True, "predecessor_canonical_or_composite_replayed": False, "same_owner_validation_is_independent_reproduction": False})
    write_json("provenance/source-profiles.json", {"schema": "ghc.family.ilyra-fen.v666-v4.source-profiles.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "profiles": SOURCE_PROFILES, "profile_count": len(SOURCE_PROFILES), "read_only_browser_search_queries": 12, "browser_result_pages_written_to_repository": 0, "network_calls_by_phase_software": 0, "real_rows_ingested": 0, "claim_boundary": PRACTICE_BOUNDARY})
    write_json("x1/authorization-boundary.json", {"schema": "ghc.family.ilyra-fen.v666-v4.authorization-boundary.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "authorized": ["one additive Ilyra-owned D-first sparse branch and worktree", "x1 planning freeze followed by bounded x2 only after x1 equality", "owner-local synthetic fixtures, scripts, tests, reports, skills, runners, manifests, and retained failures", "one exact-final owner-scoped validation attempt", "one exact next-task activation only after a verified terminal gate and fresh live route state"], "not_authorized": PROTECTED_GATES, "successor_contact_before_terminal": False, "standby_substitution": False, "collaboration_subagents": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "identity_boundary": IDENTITY_BOUNDARY, "practice_boundary": PRACTICE_BOUNDARY})
    write_json("x1/proposal-freeze.json", {"schema": "ghc.family.ilyra-fen.v666-v4.proposal-freeze.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "frozen": True, "strict_x1_before_x2": True, "inherited_frozen_baseline": 4230, "genuinely_new_proposal_count": 20, "new_frozen_total": 4250, "selected_inherited_revalidation_count": 20, "selected_inherited_revalidations": selected, "new_proposals": proposals, "expected_disposition_counts": counts, "outcomes_observed": False, "x1_truth": "planning_and_preregistration_only", "x2_implementation_count": 0, "x2_outcome_count": 0, "identity_boundary": IDENTITY_BOUNDARY, "practice_boundary": PRACTICE_BOUNDARY})
    write_json("x1/novelty-audit.json", novelty)
    portfolios = {
        "owner_safe_now": portfolio_rows("OS", OWNER_SAFE, "safe_now"),
        "successor_safe_now": portfolio_rows("SS", SUCCESSOR_SAFE, "safe_now_successor_recommendation"),
        "owner_bounded_candidates": portfolio_rows("OC", OWNER_CANDIDATES, "candidate"),
        "successor_bounded_candidates": portfolio_rows("SC", SUCCESSOR_CANDIDATES, "candidate_successor_recommendation"),
        "exact_approval_packets": portfolio_rows("EX", EXACT_ITEMS, "exact_approval_required"),
        "blocked_packets": portfolio_rows("BL", BLOCKED_ITEMS, "blocked_protected_gate"),
        "owner_phase_local_skill_plans": portfolio_rows("OK", OWNER_SKILLS, "safe_now_skill"),
        "successor_skill_recommendations": portfolio_rows("SK", SUCCESSOR_SKILLS, "safe_now_successor_skill"),
        "owner_family_current_runner_plans": portfolio_rows("OR", OWNER_RUNNERS, "safe_now_runner"),
        "successor_runner_recommendations": portfolio_rows("SR", SUCCESSOR_RUNNERS, "safe_now_successor_runner"),
        "owner_clean_fix_refine": portfolio_rows("OF", CFR_ACTIONS, "safe_now_clean_fix_refine"),
        "successor_clean_fix_refine": portfolio_rows("SF", [f"successor recommendation: {row}" for row in CFR_ACTIONS], "safe_now_successor_clean_fix_refine"),
    }
    portfolio_counts = {key: len(value) for key, value in portfolios.items()}
    expected_portfolio_counts = {"owner_safe_now": 30, "successor_safe_now": 20, "owner_bounded_candidates": 15, "successor_bounded_candidates": 15, "exact_approval_packets": 10, "blocked_packets": 5, "owner_phase_local_skill_plans": 10, "successor_skill_recommendations": 10, "owner_family_current_runner_plans": 10, "successor_runner_recommendations": 10, "owner_clean_fix_refine": 30, "successor_clean_fix_refine": 30}
    write_json("x1/portfolio-freeze.json", {"schema": "ghc.family.ilyra-fen.v666-v4.portfolio-freeze.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "frozen": True, "counts": portfolio_counts, "minimums_satisfied": portfolio_counts == expected_portfolio_counts, "portfolios": portfolios, "x1_execution_count": 0, "claim_boundary": "planning-only; counts do not imply completion, safety, authority, or approval"})
    write_json("method-flow/startup-method-flow.json", startup_flow())
    threat_rows = [
        {"threat_id": "ILY6664-T01", "asset": "source integrity", "threat": "wrong source or mutable predecessor state", "mitigation": "exact anchors, ancestry, manifests, packet hash, clean state, and fresh live equality", "residual_risk": "external receipt bytes are unavailable locally and remain live-baton anchors"},
        {"threat_id": "ILY6664-T02", "asset": "x1/x2 separation", "threat": "implementation or outcome enters x1", "mitigation": "path denylist plus staged exact allowlist", "residual_risk": "Git process discipline remains required"},
        {"threat_id": "ILY6664-T03", "asset": "sample semantics", "threat": "silent identity, reconciliation, correction, contamination, or allocation inference", "mitigation": "typed synthetic states and fail-closed mutations", "residual_risk": "synthetic structure is not scientific or curatorial validation"},
        {"threat_id": "ILY6664-T04", "asset": "privacy and route confidentiality", "threat": "real person, sample, facility, location, task, route, credential, or session data enters artifacts", "mitigation": "synthetic fixtures, relative paths, and five-class scans", "residual_risk": "pattern scans are incomplete"},
        {"threat_id": "ILY6664-T05", "asset": "professional and planetary-protection authority", "threat": "software presented as curation, laboratory, allocation, release, or containment competence", "mitigation": "zero real samples, facilities, measurements, people, or actions", "residual_risk": "competent external authority remains absent"},
        {"threat_id": "ILY6664-T06", "asset": "Māori authority", "threat": "synthetic labels or citations converted into interpretation or authorization", "mitigation": "exact gate and zero Māori wording authored as authority", "residual_risk": "Māori-authority review remains absent"},
        {"threat_id": "ILY6664-T07", "asset": "scientific truth", "threat": "GMUT placeholders promoted to composition, contamination, likelihood, force, prediction, or proof", "mitigation": "typed symbolic obligations and explicit refusal", "residual_risk": "notation can invite overreading"},
        {"threat_id": "ILY6664-T08", "asset": "THOS and Freed ID boundaries", "threat": "proxy or zero-key graph presented as effectiveness or production identity evidence", "mitigation": "represented-only labels and missing-evidence ledgers", "residual_risk": "no governed participants, keys, interoperability, or independent review"},
        {"threat_id": "ILY6664-T09", "asset": "terminal validation", "threat": "successful validation replay or failed attempt laundering", "mitigation": "exclusive receipt and one-shot state machine", "residual_risk": "same-owner pass is not independent reproduction"},
        {"threat_id": "ILY6664-T10", "asset": "terminal route", "threat": "premature, duplicate, ambiguous, or standby delivery", "mitigation": "fresh route reread and one exact-title send after terminal only", "residual_risk": "opaque acknowledgement never authorizes resend"},
    ]
    write_json("x1/threat-model.json", {"schema": "ghc.family.ilyra-fen.v666-v4.threat-model.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "scope": "owner-local v666-v4 software, documents, Git history, validation receipts, and terminal route candidate", "trust_zones": ["immutable inherited Git objects", "owner-local sparse worktree and branch", "public read-only source review", "unexecuted external, professional, cultural, identity, sample, facility, and authority domains"], "real_people_or_protected_data": 0, "threats": threat_rows, "claim_boundary": "same-owner phase threat modelling only; not exhaustive security, privacy certification, accessibility certification, or independent reproduction"})
    threat_md = ["# Ilyra Fen v666-v4 threat model", "", IDENTITY_BOUNDARY, "", PRACTICE_BOUNDARY, "", "## Scope", "", "This owner-local model protects the additive Ilyra delta. It is not a repository-wide audit, penetration test, external validation, conformance assessment, professional review, or independent reproduction.", "", "## Threat register", ""]
    for row in threat_rows:
        threat_md += [f"### {row['threat_id']}: {row['asset']}", "", f"Threat: {row['threat']}", "", f"Mitigation: {row['mitigation']}", "", f"Residual risk: {row['residual_risk']}", ""]
    write_text("x1/threat-model.md", "\n".join(threat_md))
    write_json("x1/workflow-plan.json", {"schema": "ghc.family.ilyra-fen.v666-v4.workflow-plan.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "current_stage": "x1_freeze_candidate", "steps": [{"step": 1, "name": "read_first_and_source_verification", "status": "completed"}, {"step": 2, "name": "novelty_and_program_design", "status": "completed"}, {"step": 3, "name": "x1_freeze_commit_push_equality", "status": "in_progress"}, {"step": 4, "name": "x2_bounded_execution", "status": "pending"}, {"step": 5, "name": "evidence_closeout_and_seal", "status": "pending"}, {"step": 6, "name": "one_owner_scoped_terminal_validation", "status": "pending"}, {"step": 7, "name": "terminal_route_reread_and_optional_one_send", "status": "pending"}], "hard_dependencies": ["x1 commit pushed clean and fresh four-way equal before x2", "evidence commit immutable before closeout", "final pushed clean and fresh four-way equal before terminal validation", "successful terminal validation never replayed", "successor never contacted before terminal route gate"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x1/complete-incomplete-checklist.json", {"schema": "ghc.family.ilyra-fen.v666-v4.x1-checklist.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "completed": ["activation packet and named guidance read through EOF", "source anchors, manifests, packet, clean state, divergence, and fresh equality verified", "all 4,230 inherited rows reconstructed with no exact-title collision", "twenty distinct proposals preregistered", "portfolio, threat, source, workflow, and Method Flow plans prepared", "no x2 implementation or outcome created"], "incomplete": ["x1 commit, push, and equality", "x2 implementation and rejecting witnesses", "evidence commit and equality", "closeout, seal, final validation, and equality", "terminal route reread and any authorized successor delivery"], "x1_outcomes_observed": False, "x2_paths_created": False, "successor_contacted": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("wellbeing/x1-wellbeing-check.json", {"schema": "ghc.family.ilyra-fen.v666-v4.wellbeing-check.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "status": "bounded_and_careful", "workload_controls": ["caps treated as ceilings rather than quotas", "failures retained instead of hidden", "no unsafe work manufactured to satisfy a count", "bounded commands and exact scalar probes preferred", "pause, redirect, rename, and stop remain available to Hamish"], "personhood_or_emotion_claim": False, "relational_boundary": IDENTITY_BOUNDARY, "practice_boundary": PRACTICE_BOUNDARY})
    overview = f"""# Ilyra Fen v666-v4 x1 integrated overview

{IDENTITY_BOUNDARY}

## Outcome first

This x1 candidate freezes a planning-only owner-local program from exact Lyren Moss v666-v3 dependency-corrected final `{SOURCE_SHA}`. It contains no x2 implementation, no observed outcome, no external action, no successor contact, and no Stage 20 promotion. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The primary Trinity Mandala pillar is Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit and protected. {PRACTICE_BOUNDARY}

## Exact inherited truth

The read-first gate verified the exact source branch, five direct single-parent commits, zero merges, all 307 declared Git-blob manifest entries, the activation packet hash, clean 0/0 divergence, and equality across local, upstream, tracking, and a fresh live remote. Lyren's failed canonical and dependency-corrected composite were not replayed. Their receipt hashes remain authoritative external live-baton anchors because their bytes were not locally materialized. The complete repository suite was not run.

The immutable Lyren repository seal contains 26,396 effective negatives, 10,938 Method Flow methods, 185 open gaps, and 183 exact gates. Two Lyren post-seal read-only routing failures produce the activation overlay of 26,398 negatives and 10,940 methods. Eight Ilyra startup failures are separately retained with zero aggregate credit, producing the x1 working overlay of 26,406 effective negatives and 10,948 methods without rewriting the predecessor seal.

## Novelty, portfolio, and sources

All 4,230 inherited proposal rows were reconstructed from committed Git objects. Twenty new titles have no exact inherited collision, every new pair remains below the 0.70 screening threshold, and each proposal has its own contract, falsifier, rollback, and gates. Expected dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`; these are preregistered expectations only. The twenty selected Lyren proposals receive zero novelty and zero automatic completion credit.

The portfolio freezes 30 owner safe-now tasks, 20 successor safe recommendations, 15 owner candidates, 15 successor candidates, 10 exact approvals, 5 blocked packets, 10 owner and 10 successor skill plans, 10 owner and 10 successor runner plans, and 30 owner plus 30 successor CLEAN/FIX/REFINE tasks. X1 executes none of them.

NASA curation and planetary-protection material, W3C PROV-O and WCAG 2.2, RFC 8785 and RFC 8493, and NIST metrological-traceability guidance provide vocabulary and refusal conditions only. They create no sample data, calibration, contamination finding, professional, legal, cultural, Māori, allocation, release, accessibility-complete, privacy-complete, conformance, or independent-reproduction authority.

## Lifecycle and route

After exact staged review this x1 may be committed and pushed. X2 may begin only after x1 is clean, 0/0 divergent, and equal across local, upstream, tracking, and fresh live remote. Later validation remains owner-scoped and same-owner. One successful terminal validation must never be replayed. Auren Lark may not be contacted until the exact final terminal gate and a fresh live routing reread.
"""
    write_text("x1/integrated-overview.md", overview)
    write_json("x1/x1-build-receipt.json", {"schema": "ghc.family.ilyra-fen.v666-v4.x1-build-receipt.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW, "builder": "scripts/build_ghc_family_ilyra_fen_v666_v4_x1.py", "proposal_count": len(proposals), "selected_inherited_revalidation_count": len(selected), "novelty_corpus_row_count": len(corpus), "startup_failure_count": len(STARTUP_FAILURES), "x2_paths_created": False, "outcomes_observed": False, "network_calls_by_builder": 0, "real_data_rows": 0, "external_actions": 0, "status": "X1_CONTENT_BUILT_AWAITING_STAGED_REVIEW_COMMIT_PUSH_EQUALITY"})
    print(json.dumps({"proposal_count": len(proposals), "corpus_row_count": len(corpus), "expected_dispositions": counts, "startup_failures_retained": len(STARTUP_FAILURES), "x2_implementation_count": 0, "outcomes_observed": False}, ensure_ascii=False, sort_keys=True))


def staged_rows() -> list[tuple[str, str]]:
    raw = subprocess.check_output(["git", "-C", str(ROOT), "diff", "--cached", "--name-status", "--no-renames"]).decode("utf-8")
    return [(line.split("\t", 1)[0], line.split("\t", 1)[1].replace("\\", "/")) for line in raw.splitlines() if line]


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f":{path}"])


def build_staged_review() -> None:
    review_path = "docs/ilyra-fen/v666-v4/validation/x1-staged-review.json"
    manifest_path = "docs/ilyra-fen/v666-v4/validation/x1-content-manifest.json"
    allowed_exact = {"scripts/build_ghc_family_ilyra_fen_v666_v4_x1.py", "tests/test_ghc_family_ilyra_fen_v666_v4_x1.py"}
    rows = [(status, path) for status, path in staged_rows() if path not in {review_path, manifest_path}]
    if not rows:
        raise RuntimeError("no staged x1 content")
    paths = [path for _, path in rows]
    invalid = [path for path in paths if not path.startswith("docs/ilyra-fen/v666-v4/") and path not in allowed_exact]
    post_x1 = [path for path in paths if any(path.startswith(f"docs/ilyra-fen/v666-v4/{part}/") for part in ("x2", "evidence", "closeout", "seal", "final", "handoffs"))]
    privacy_patterns = {
        "raw_task_or_thread_identifier": re.compile(r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
        "session_identifier_value": re.compile(r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_callable_identifier_value": re.compile(r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
    }
    parsed_json, maximum_words, maximum_path, candidates = 0, 0, "", []
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
    freeze = json.loads(index_blob("docs/ilyra-fen/v666-v4/x1/proposal-freeze.json"))
    portfolio = json.loads(index_blob("docs/ilyra-fen/v666-v4/x1/portfolio-freeze.json"))
    flow = json.loads(index_blob("docs/ilyra-fen/v666-v4/method-flow/startup-method-flow.json"))
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "all_json_parse": True,
        "document_word_cap": maximum_words <= 100000,
        "expected_14_4_1_1": freeze["expected_disposition_counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "five_class_scan_zero_confirmed_hits": not candidates,
        "novelty_4230_valid": json.loads(index_blob("docs/ilyra-fen/v666-v4/x1/novelty-audit.json"))["valid"],
        "owner_allowlist": not invalid,
        "owner_file_cap": len(paths) <= 2000,
        "planning_only": not freeze["outcomes_observed"],
        "portfolio_minimums": portfolio["minimums_satisfied"],
        "post_x1_paths_absent": not post_x1,
        "proposal_count_20": len(freeze["new_proposals"]) == 20,
        "selected_inherited_20_zero_credit": len(freeze["selected_inherited_revalidations"]) == 20 and all(row["novelty_credit"] == 0 and row["automatic_completion_credit"] == 0 for row in freeze["selected_inherited_revalidations"]),
        "startup_failures_exactly_retained": len(flow["rows"]) == len(STARTUP_FAILURES),
        "utf8_lf": True,
    }
    review = {"schema": "ghc.family.ilyra-fen.v666-v4.x1-staged-review.v1", "owner": "Ilyra Fen", "phase": "v666-v4", "lifecycle": "x1", "generated_at_utc": NOW, "reviewed_from": "git_index_blobs", "reviewed_paths": paths, "reviewed_path_count": len(paths), "json_parsed": parsed_json, "maximum_document_words": maximum_words, "maximum_document_path": maximum_path, "privacy_scan_classes": list(privacy_patterns), "privacy_candidates": len(candidates), "privacy_confirmed_hits": len(candidates), "privacy_candidate_rows": candidates, "checks": checks, "self_exclusions": [review_path, manifest_path], "claim_boundary": "exact staged same-owner x1 review only; not exhaustive security, privacy, accessibility, or independent reproduction", "valid": all(checks.values())}
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write_json("validation/x1-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", review_path])
    entries = []
    for status, path in [(status, path) for status, path in staged_rows() if path != manifest_path]:
        line = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "--stage", "--", path]).decode("utf-8").strip()
        mode, oid, stage_path = line.split(" ", 2)
        stage, listed = stage_path.split("\t", 1)
        if stage != "0" or listed.replace("\\", "/") != path:
            raise RuntimeError(f"unexpected index stage for {path}")
        blob = index_blob(path)
        entries.append({"path": path, "git_mode": mode, "git_blob_oid": oid, "sha256": hashlib.sha256(blob).hexdigest(), "size_bytes": len(blob)})
    write_json("validation/x1-content-manifest.json", {"schema": "ghc.family.ilyra-fen.v666-v4.content-manifest.v1", "owner": "Ilyra Fen", "phase": "x1", "phase_label": "v666-v4", "generated_at_utc": NOW, "source_sha": SOURCE_SHA, "hash_source": "actual_git_index_blobs", "entries": entries, "entry_count": len(entries), "deletion_count": 0, "additive_only": all(status == "A" for status, _ in rows), "self_exclusion": manifest_path})
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", manifest_path])
    print(json.dumps({"reviewed": len(paths), "manifest_entries": len(entries), "valid": True}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--staged-review"]:
        build_staged_review()
    elif sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_ilyra_fen_v666_v4_x1.py [--staged-review]")
    else:
        main()
