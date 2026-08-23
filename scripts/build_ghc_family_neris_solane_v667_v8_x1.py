#!/usr/bin/env python3
"""Build and validate the planning-only Neris Solane v667-v8 x1 freeze.

The builder reads Elaren's immutable proposal-chain compatibility surface but
owns every emitted Neris artifact.  It performs no x2 implementation, package
installation, real-world action, outcome observation, or successor contact.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PHASE = "v667-v8"
OWNER = "Neris Solane"
OWNER_SLUG = "neris-solane"
PHASE_ROOT = ROOT / "docs" / OWNER_SLUG / PHASE
REL_PHASE_ROOT = f"docs/{OWNER_SLUG}/{PHASE}"
NOW = "2026-08-23T21:32:29.934Z"

SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v667-v7-full-tools"
SOURCE_PARENT_SHA = "dc8d91294b7656ad5e9961bba93ff759af20846c"
SOURCE_X1_SHA = "b92d8b1b648c4d716ca894b22fda14327baed9b3"
SOURCE_EVIDENCE_SHA = "9fde47f17a3c248643a543e0f44460e69191e627"
SOURCE_SHA = "75082d325299732f6796ac262149147b3a7029e8"
SOURCE_PHASE_ROOT = "docs/elaren-kestrel/v667-v7"
SOURCE_CANONICAL_SHA256 = "6dd6245e7c59c55667544fd946123938c42f253dbed4701d2bb2b93577eeabda"
SOURCE_BATON_SHA256 = "0ad60732a492bd1d1c3a103495609410cf761f11296ca447353794e0094a2019"

INHERITED_PROPOSAL_COUNT = 4510
SELECTED_INHERITED_COUNT = 20
NEW_PROPOSAL_COUNT = 20
NEW_FROZEN_TOTAL = 4530
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PRIMARY_PILLAR = "Freed ID and CBR Heart"
PRACTICE = "wholly synthetic community seed-bank accession and germplasm passport-data lineage records"
RELATIONAL_ROLE = "datum-boundary weaver"
HOPE = "expose provenance, uncertainty, and stop conditions before synthetic evidence is mistaken for scientific or operational authority"

COMPAT_PATH = ROOT / "scripts" / "build_ghc_family_elaren_kestrel_v667_v7_x1.py"
_spec = importlib.util.spec_from_file_location("_elaren_v667_v7_x1_compat", COMPAT_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError("unable to load immutable Elaren x1 compatibility surface")
compat = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(compat)
for _module in (compat, compat.base):
    for _name, _value in {
        "ROOT": ROOT,
        "SOURCE_X1_SHA": SOURCE_X1_SHA,
        "SOURCE_PHASE_ROOT": SOURCE_PHASE_ROOT,
        "INHERITED_PROPOSAL_COUNT": INHERITED_PROPOSAL_COUNT,
    }.items():
        setattr(_module, _name, _value)

run_git = compat.run_git
git_json = compat.git_json
canonical_sha256 = compat.canonical_sha256
similarity = compat.similarity
MANDATORY_SKILLS = list(compat.MANDATORY_SKILLS)
MUTATION_CLASSES = list(compat.MUTATION_CLASSES)

PROTECTED_GATES = [
    "real seed keeper, grower, breeder, botanist, taxonomist, geneticist, curator, collection manager, donor, provider, recipient, community member, affected party, regulator, cultural authority, or Maori authority",
    "real seed, germplasm, accession, specimen, propagule, plant, taxon determination, location, community, person, genetic sequence, phenotype, image, measurement, passport record, traditional knowledge, or benefit-sharing record",
    "real collection, acquisition, regeneration, germination, viability test, characterization, evaluation, multiplication, distribution, transfer, storage, handling, quarantine, planting, release, destruction, or access decision",
    "professional genebank, agricultural, botanical, taxonomic, genetic, biosecurity, conservation, intellectual-property, access-and-benefit-sharing, privacy, accessibility, legal, cultural, or workplace authority",
    "real likelihood, parameter constraint, prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon",
    "real participant or operator arm, safety monitoring, operational outcome, appropriate statistics, AGI, ASI, consciousness, personhood, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, recovery event, trust governance, or production credential",
    "credential, account, token, secret, login, external write, publication, deployment, purchase, production release, or sibling-lane mutation",
    "system-wide or elevated install, Windows feature change, Codex desktop update, host-security weakening, Sandbox or Hyper-V activation, reboot, destructive cleanup, or unreviewed lifecycle-script execution",
    "privacy-complete, accessibility-complete, exhaustive-security, standards-conformance, independent-reproduction, production-readiness, fitness-for-service, or deployment-readiness claim",
    "ownership, custody, access, attribution, intellectual property, farmers rights, prior informed consent, mutually agreed terms, sacred or customary association, legal or cultural interpretation, remedy, affected-party legitimacy, traditional knowledge, Maori wording, Maori concepts, Maori data governance, tangata whenua, iwi, hapu, or Maori-authority decision",
    "Stage 20 promotion or conversion of same-owner synthetic evidence into certification, competence, safety, legality, cultural legitimacy, scientific truth, or authority",
]

SOURCE_PROFILES: list[dict[str, str]] = [
    {"source_id": "S01", "name": "FAO Genebank Standards for Plant Genetic Resources for Food and Agriculture", "url": "https://www.fao.org/4/i3704e/i3704e.pdf", "status": "official FAO standards surface reviewed read-only", "bounded_use": "documentation, accession, storage, viability, regeneration, characterization, distribution, and voluntary nonbinding-standard vocabulary only; no operational genebank conclusion"},
    {"source_id": "S02", "name": "FAO and Bioversity Multi-Crop Passport Descriptors v2.1", "url": "https://cgspace.cgiar.org/search?query=Multi-Crop%20Passport%20Descriptors%20v2.1", "status": "official repository search surface for the descriptor publication reviewed read-only", "bounded_use": "passport field, coding, collection, donor, biological-status, and location-minimization vocabulary only; no real accession conformance"},
    {"source_id": "S03", "name": "International Treaty on Plant Genetic Resources for Food and Agriculture", "url": "https://www.fao.org/plant-treaty/overview/text-treaty/en", "status": "official treaty text reserved for competent interpretation", "bounded_use": "treaty, facilitated access, benefit-sharing, Farmers Rights, national responsibility, and authority-reservation vocabulary only; no legal interpretation or action"},
    {"source_id": "S04", "name": "Convention on Biological Diversity Nagoya Protocol text", "url": "https://www.cbd.int/abs/text", "status": "official convention text reserved for competent interpretation", "bounded_use": "access, prior informed consent, mutually agreed terms, compliance, traditional knowledge, and authority-reservation vocabulary only; no legal or cultural conclusion"},
    {"source_id": "S05", "name": "TDWG Darwin Core standard", "url": "https://dwc.tdwg.org/", "status": "official TDWG standard surface reviewed read-only", "bounded_use": "occurrence, material entity, event, identification, taxon, location, measurement, and term-identifier vocabulary only; no Darwin Core conformance claim"},
    {"source_id": "S06", "name": "TDWG Darwin Core current term list", "url": "https://dwc.tdwg.org/list/", "status": "official current term list reviewed read-only", "bounded_use": "current term labels, identifiers, definitions, and version awareness only; no mapping completeness"},
    {"source_id": "S07", "name": "W3C PROV-O Recommendation", "url": "https://www.w3.org/TR/prov-o/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "entity, activity, agent, derivation, revision, invalidation, and qualified provenance vocabulary only; no provenance truth"},
    {"source_id": "S08", "name": "W3C Verifiable Credentials Data Model 2.0", "url": "https://www.w3.org/TR/vc-data-model/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "evidence, status, holder disclosure, privacy, and nonproduction credential vocabulary only; zero keys, proofs, issuers, or lifecycle calls"},
    {"source_id": "S09", "name": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "official W3C Recommendation reviewed read-only", "bounded_use": "headings, labels, non-colour cues, reading order, keyboard review, and manual-review reservations only; no accessibility-complete claim"},
    {"source_id": "S10", "name": "New Zealand Privacy Commissioner privacy principles", "url": "https://www.privacy.org.nz/privacy-principles/", "status": "official privacy surface reviewed read-only", "bounded_use": "purpose, minimization, access, correction, retention, use, disclosure, and remedy reservations only; no legal or compliance conclusion"},
    {"source_id": "S11", "name": "New Zealand Privacy Principle 7", "url": "https://www.privacy.org.nz/privacy-principles/7/", "status": "official correction principle surface reviewed read-only", "bounded_use": "correction request, attachment, notice, and contested-record vocabulary only; no legal conclusion"},
    {"source_id": "S12", "name": "Te Mana Raraunga principles", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "primary Maori data-sovereignty surface read only to the authority-reservation level", "bounded_use": "rangatiratanga, whakapapa, whanaungatanga, kotahitanga, manaakitanga, and kaitiakitanga labels are not interpreted here; collective authority, context, control, benefit, guardianship, and consultation remain empty-chair gates"},
    {"source_id": "S13", "name": "Global Indigenous Data Alliance CARE Principles", "url": "https://www.gida-global.org/careprinciples", "status": "primary Indigenous data-governance surface reviewed only for reservation", "bounded_use": "collective benefit, authority to control, responsibility, and ethics labels reserve governance questions; no affected-party or Indigenous authority is claimed"},
    {"source_id": "S14", "name": "NIST International System of Units", "url": "https://www.nist.gov/pml/owm/metric-si/si-units", "status": "official NIST surface reviewed read-only", "bounded_use": "quantity, unit, symbol, dimensional consistency, and reporting vocabulary only; no real measurement or conformity claim"},
    {"source_id": "S15", "name": "NIST Technical Note 1297", "url": "https://www.nist.gov/pml/nist-technical-note-1297", "status": "official NIST uncertainty guidance reviewed read-only", "bounded_use": "uncertainty component, coverage, reporting, and correction vocabulary only; no calibrated apparatus or measured result"},
    {"source_id": "S16", "name": "hypothesis-jsonschema 0.23.1 release", "url": "https://pypi.org/project/hypothesis-jsonschema/0.23.1/", "status": "primary PyPI metadata verified read-only", "bounded_use": "version, wheel, hash, Python metadata, MPL-2.0 metadata, and schema-strategy capability only; no package fitness or security claim"},
    {"source_id": "S17", "name": "DeepDiff 9.1.0 release", "url": "https://pypi.org/project/deepdiff/9.1.0/", "status": "primary PyPI metadata verified read-only", "bounded_use": "version, wheel, hash, MIT metadata, and structural-difference capability only; no package fitness or security claim"},
    {"source_id": "S18", "name": "jsonpatch 1.33 release", "url": "https://pypi.org/project/jsonpatch/1.33/", "status": "primary PyPI metadata verified read-only", "bounded_use": "version, wheel, hash, Modified BSD metadata, and JSON Patch capability only; no package fitness or security claim"},
    {"source_id": "S19", "name": "pip secure installs guidance", "url": "https://pip.pypa.io/en/stable/topics/secure-installs/", "status": "official pip documentation reserved for x2", "bounded_use": "exact pin, hash-checking, wheel-only, dependency closure, and failure-boundary vocabulary only; no supply-chain completeness"},
    {"source_id": "S20", "name": "Python virtual environments documentation", "url": "https://docs.python.org/3/library/venv.html", "status": "official Python documentation reserved for x2", "bounded_use": "isolated environment creation and non-portability boundaries only; no host isolation or security guarantee"},
    {"source_id": "S21", "name": "Git cat-file documentation", "url": "https://git-scm.com/docs/git-cat-file", "status": "official Git documentation reviewed read-only", "bounded_use": "object-addressed blob reading and exact batch-length discipline only; no repository-wide validation claim"},
]

PROPOSAL_SPECS: list[tuple[str, str, list[str], str]] = [
    ("synthetic seed-bank accession identity capsule with surrogate accession number, institution vacancy, revision, and no ownership authority", "Surrogate accession identity, naming assertions, and correction state remain separable from ownership, custody, authenticity, and institutional authority.", ["S01", "S02", "S07"], "completed"),
    ("germplasm passport descriptor presence and coding matrix with explicit unknowns, source bounds, and no real collection record", "A descriptor matrix distinguishes absent, unknown, not applicable, and source-attributed values without claiming MCPD completeness or a real accession.", ["S01", "S02", "S07"], "completed"),
    ("donor provider and acquisition-claim provenance quarantine with contradiction retention and zero benefit-sharing decision", "Provider and donor statements remain attributed, contestable claims while access, consent, terms, ownership, and benefit-sharing authority stay vacant.", ["S02", "S03", "S04", "S07"], "completed"),
    ("synthetic acquisition event correction chain with assertion time, validity time, supersession, and no historical rewrite", "Bitemporal corrections preserve the original assertion, reason, source, and superseding edge instead of silently rewriting acquisition history.", ["S07", "S10", "S11"], "completed"),
    ("seed container and storage-location vacancy ledger with discrepancy stops, zero items, and no handling direction", "A zero-item ledger exposes missing container, location, custody, and discrepancy fields while issuing no storage, handling, transfer, or disposal action.", ["S01", "S07"], "completed"),
    ("viability and germination zero-row observation schema with units, uncertainty vacancies, and no measurement or advice", "Quantities require method, unit, date, sample, uncertainty, and source fields, yet the schema contains no seed, test, result, threshold, or management recommendation.", ["S01", "S14", "S15"], "completed"),
    ("regeneration and multiplication lineage placeholder with parent-lot vacancies, event stops, and zero propagation action", "Lineage edges and missing prerequisites remain inspectable without planting, regeneration, multiplication, selection, harvest, or genetic-integrity claims.", ["S01", "S07"], "completed"),
    ("duplicate and safety-duplicate reconciliation register with non-equivalence default, conflict quarantine, and no custody claim", "Shared identifiers or descriptors never establish biological equivalence, identity, custody, safety duplication, or fitness for distribution.", ["S01", "S02", "S07"], "completed"),
    ("taxon-name assertion and identification correction graph with determiner vacancy, confidence state, and no taxonomic authority", "Taxon names remain sourced assertions with determiner, date, confidence, and correction edges rather than authoritative identifications.", ["S02", "S05", "S06", "S07"], "completed"),
    ("material transfer and access-condition empty ledger with term provenance, expiry stops, and no legal decision", "A zero-row ledger can reserve access conditions and transfer provenance while no permission, restriction, treaty interpretation, or legal conclusion is issued.", ["S03", "S04", "S07"], "completed"),
    ("bitemporal passport correction and contested-field readback with reason codes, attachment state, and no source erasure", "Correction requests, attachments, notices, and contested values remain linked and reversible without erasing the original source record.", ["S07", "S10", "S11"], "completed"),
    ("derived dataset and crop-descriptor lineage manifest with transform ancestry, disclosure mask, and no authorship claim", "Dataset derivation, field transformation, masking, and invalidation remain machine-checkable without authenticating authorship, rights, or scientific validity.", ["S02", "S07", "S09", "S10"], "completed"),
    ("collecting-location disclosure minimization map with generalized geolocation, purpose cap, and no privacy compliance claim", "Synthetic location precision is reduced by explicit rules and reversal metadata without using a real place or declaring legal privacy compliance.", ["S02", "S05", "S07", "S10"], "completed"),
    ("traditional-knowledge and community-authority empty-chair record with zero entries, non-substitution stop, and remedy path", "Every traditional-knowledge, community, Indigenous, cultural, and Maori authority field remains unoccupied and cannot be inferred from a software artifact.", ["S03", "S04", "S12", "S13"], "completed"),
    ("THOS matched-queue seed-bank documentation proxy with equal symbolic budget, stop precedence, blind labels, and zero participants", "A participant-free queue proxy represents allocation and stop semantics without effectiveness, staffing, safety, operational, or trial evidence.", ["S01", "S09"], "represented"),
    ("GMUT germplasm diversity-network symbolic board with typed scalar-tensor placeholders, boundary terms, units, and zero fitted coefficients", "A typed symbolic board checks declarations and dimensions while fitting no likelihood, coefficient, prediction, law, or empirical result.", ["S14", "S15"], "represented"),
    ("Freed ID zero-key accession provenance statement graph with purpose cap, correction, status tombstone, and no lifecycle calls", "A zero-key graph exposes lineage, correction, and status semantics while issuers, holders, proofs, resolvers, credentials, and trust decisions remain absent.", ["S07", "S08", "S10"], "represented"),
    ("CBR accessibility privacy CARE contestation and remedy shell for passport records with zero sessions or decisions", "A structural shell represents labels, disclosure questions, collective benefit, authority, responsibility, ethics, contestation, and remedy without deciding any of them.", ["S09", "S10", "S12", "S13"], "represented"),
    ("real genebank evidence escrow requiring governed accession records, authenticated material, calibrated observations, competent practitioners, affected parties, and independent review", "Real governed records, materials, observations, competent practice, affected parties, and independent review are absent and remain an explicit open gap.", ["S01", "S02", "S03", "S04", "S14", "S15"], "open_gap"),
    ("exact authority circuit for germplasm access benefit sharing custody Farmers Rights traditional knowledge cultural and Maori decisions", "No legal, cultural, community, Indigenous, affected-party, custody, access, benefit-sharing, Farmers Rights, or Maori decision can proceed without exact competent authority and governed evidence.", ["S03", "S04", "S10", "S12", "S13"], "exact_gate"),
]

STARTUP_FAILURES = [
    {"failure_id": "NS6678-X1-N001", "failure": "the initial large activation-baton display exceeded the visible output window", "credit": 0, "recovery": "read the committed baton through EOF in bounded windows and verify its exact digest"},
    {"failure_id": "NS6678-X1-N002", "failure": "an aggregated three-window baton recovery was itself truncated", "credit": 0, "recovery": "use smaller sequential windows with explicit ending-line evidence"},
    {"failure_id": "NS6678-X1-N003", "failure": "a PowerShell direct foreach skill-inventory projection produced an empty-pipe ParserError", "credit": 0, "recovery": "use bounded arrays and scalar projections"},
    {"failure_id": "NS6678-X1-N004", "failure": "a combined source-equality projection had a missing-closing-parenthesis ParserError", "credit": 0, "recovery": "use separate literal scalar ancestry and equality probes"},
    {"failure_id": "NS6678-X1-N005", "failure": "the corrected combined source probe produced no attributable output", "credit": 0, "recovery": "split exact head, parent, divergence, and live-remote checks"},
    {"failure_id": "NS6678-X1-N006", "failure": "an oversized proposal-freeze display exceeded the bounded result window", "credit": 0, "recovery": "project only required schema keys and exact counts"},
    {"failure_id": "NS6678-X1-N007", "failure": "a direct foreach manifest projection produced another empty-pipe ParserError", "credit": 0, "recovery": "use a bounded manifest replay loop with explicit accumulators"},
    {"failure_id": "NS6678-X1-N008", "failure": "a combined CLI registry and storage probe returned only the first CLI field", "credit": 0, "recovery": "query version, registry, and storage as separate scalar dependencies"},
    {"failure_id": "NS6678-X1-N009", "failure": "an isolated registry-version projection returned no output", "credit": 0, "recovery": "use the exact package metadata query and retain the verified 0.149.0 equality"},
    {"failure_id": "NS6678-X1-N010", "failure": "an old-template byte-conversion PowerShell projection failed", "credit": 0, "recovery": "inspect bounded text windows directly without byte-array conversion"},
    {"failure_id": "NS6678-X1-N011", "failure": "an exact toolchain extraction omitted its path variable and accidentally launched a broad read-only search across the control directory", "credit": 0, "recovery": "discard the truncated output and require a resolved literal file before every future search"},
    {"failure_id": "NS6678-X1-N012", "failure": "a combined sparse materialization and status summary returned no attributable output", "credit": 0, "recovery": "separate sparse-pattern, head, diff, and untracked scalars"},
    {"failure_id": "NS6678-X1-N013", "failure": "a split sparse-status probe stalled after printing only the patterns", "credit": 0, "recovery": "avoid broad status and use exact diff-index and owner-path probes"},
    {"failure_id": "NS6678-X1-N014", "failure": "a thirty-second process-poll wrapper yielded without an output payload", "credit": 0, "recovery": "inspect exact process names and repository locks before any retry"},
    {"failure_id": "NS6678-X1-N015", "failure": "an oversized x2-builder read exceeded the model context window", "credit": 0, "recovery": "read only targeted definitions and bounded line windows"},
    {"failure_id": "NS6678-X1-N016", "failure": "the sparse read-tree materialization crossed its yield and returned no live handle while continuing", "credit": 0, "recovery": "inspect the exact Git process and lock, then wait without duplicating it"},
    {"failure_id": "NS6678-X1-N017", "failure": "a duplicate read-tree attempt was refused by the still-active index lock", "credit": 0, "recovery": "treat the lock as active-state evidence and do not remove or override it"},
    {"failure_id": "NS6678-X1-N018", "failure": "the first process diagnostic matched its own PowerShell command text instead of the Git process", "credit": 0, "recovery": "filter the process name to git.exe and the exact read-tree command, then verify completion and lock removal"},
    {"failure_id": "NS6678-X1-N019", "failure": "the first x1 build correctly rejected a public CGSpace record URL because its content identifier matched the raw UUID-shaped private-task detector", "credit": 0, "recovery": "replace only that citation with the public repository's stable non-UUID search surface and keep the generic five-class detector strict"},
]


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def build_corpus() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    """Reconstruct all 4,510 inherited occurrences from immutable Git objects."""
    return compat.base.build_corpus()


def proposal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    pillar_overrides = {
        15: "THOS Body",
        16: "GMUT Mind",
        17: "Freed ID and CBR Heart",
        18: "CBR Heart",
        19: "All pillars",
        20: "CBR Heart",
    }
    approval_by_outcome = {
        "completed": "safe_now_bounded",
        "represented": "candidate_bounded_representation",
        "open_gap": "open_gap_external_evidence_absent",
        "exact_gate": "exact_approval_required",
    }
    lane_by_outcome = {
        "completed": "owner_local_structural",
        "represented": "owner_local_representation_only",
        "open_gap": "disabled_real_evidence_adapter",
        "exact_gate": "unexecuted_authority_reservation",
    }
    for index, (title, invariant, sources, expected) in enumerate(PROPOSAL_SPECS, 1):
        proposal_id = f"NS6678-N{index:03d}"
        base_path = f"{REL_PHASE_ROOT}/x2/proposals/{proposal_id.casefold()}"
        rows.append({
            "proposal_id": proposal_id,
            "title": title,
            "hypothesis": f"A bounded wholly synthetic contract for {title} can distinguish one admissible structure from five preregistered invalid mutations without promoting software structure into empirical, participant, professional, operational, production, legal, cultural, Maori-authority, identity, independent-reproduction, Theory-of-Everything, or Stage 20 evidence.",
            "null_or_failure_condition": "A named invalid mutation is accepted, the bounded positive is rejected, a required source, vacancy, stop, correction, uncertainty, provenance, or authority field disappears, or the artifact crosses a protected gate.",
            "approval_class": approval_by_outcome[expected],
            "execution_lane": lane_by_outcome[expected],
            "current_official_or_primary_source_needs": sources,
            "concrete_artifact": f"{base_path}/contract.json",
            "concrete_artifacts": [f"{base_path}/contract.json", f"{base_path}/mutation-results.json", f"{base_path}/bounded-receipt.json"],
            "falsifier_or_acceptance_gate": "One bounded positive must satisfy every declared invariant; all five mutations must fail closed; protected gates stay unoccupied; and the final core label may not exceed the preregistered disposition.",
            "rollback_or_recovery": "Restore only the last valid owner-local synthetic fixture, retain every failed witness at zero credit, add a recurrence guard, and issue no real-world, external, identity, participant, professional, legal, cultural, Maori-authority, safety, or production action.",
            "protected_gates": PROTECTED_GATES,
            "expected_disposition": expected,
            "distinctive_invariant": invariant,
            "primary_pillar": PRIMARY_PILLAR,
            "pillar": pillar_overrides.get(index, PRIMARY_PILLAR),
            "practice_lens": PRACTICE,
            "negative_fixture_count": 5,
            "preregistered_mutations": [
                {"mutation_id": f"{proposal_id}-M{i:02d}", "class": kind}
                for i, kind in enumerate(MUTATION_CLASSES, 1)
            ],
            "network_calls_planned": 0,
            "participant_count_planned": 0,
            "real_data_rows_planned": 0,
            "x1_status": "frozen_not_executed",
            "x2_implementation_count": 0,
            "outcomes_observed": False,
        })
    return rows


def selected_inherited_rows() -> list[dict[str, Any]]:
    freeze = git_json(SOURCE_X1_SHA, f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    rows: list[dict[str, Any]] = []
    for source in freeze["new_proposals"]:
        pid = str(source["proposal_id"])
        rows.append({
            "proposal_id": pid,
            "title": source["title"],
            "source_path": f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json",
            "source_final": SOURCE_SHA,
            "source_disposition": source["expected_disposition"],
            "origin_and_credit": "selected_inherited_bounded_revalidation_no_neris_credit",
            "append_to_novelty_chain": False,
            "neris_novelty_credit": 0,
            "neris_completion_credit": 0,
            "automatic_completion_credit": 0,
            "x1_status": "frozen_for_read_only_revalidation_not_executed",
            "outcomes_observed": False,
            "planned_receipt": f"{REL_PHASE_ROOT}/x2/selected-revalidation/{pid.casefold()}.json",
        })
    if len(rows) != SELECTED_INHERITED_COUNT:
        raise RuntimeError(f"selected inherited count drift: {len(rows)}")
    return rows


def build_novelty(
    corpus: list[dict[str, str]],
    construction: list[dict[str, Any]],
    proposals: list[dict[str, Any]],
) -> dict[str, Any]:
    nearest: list[dict[str, Any]] = []
    exact: list[dict[str, str]] = []
    for proposal in proposals:
        collisions = [row for row in corpus if row["title"].casefold() == proposal["title"].casefold()]
        exact.extend({"proposal_id": proposal["proposal_id"], "inherited_proposal_id": row["proposal_id"]} for row in collisions)
        score, inherited = max(
            ((similarity(proposal["title"], row["title"]), row) for row in corpus),
            key=lambda item: item[0],
        )
        nearest.append({
            "proposal_id": proposal["proposal_id"],
            "score": round(score, 6),
            "inherited_proposal_id": inherited["proposal_id"],
            "inherited_title": inherited["title"],
            "source_path": inherited["source_path"],
            "distinctive_invariant": proposal["distinctive_invariant"],
            "semantic_review": "distinct after manual comparison of practice mechanics, invariant, source boundary, artifacts, falsifier, rollback, and protected gates; lexical similarity is only a screen",
        })
    pair_threshold = 0.80
    pairs: list[dict[str, Any]] = []
    for index, left in enumerate(proposals):
        for right in proposals[index + 1:]:
            score = similarity(left["title"], right["title"])
            if score >= pair_threshold:
                pairs.append({"left": left["proposal_id"], "right": right["proposal_id"], "score": round(score, 6)})
    domain_terms = ["seed bank", "seed-bank", "genebank", "germplasm", "accession", "passport descriptor"]
    domain_matches = [
        {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "source_path": row["source_path"],
            "matched_terms": [term for term in domain_terms if term in row["title"].casefold()],
        }
        for row in corpus
        if any(term in row["title"].casefold() for term in domain_terms)
    ]
    groups: dict[str, list[dict[str, str]]] = {}
    for row in corpus:
        groups.setdefault(row["proposal_id"], []).append({"title": row["title"], "source_path": row["source_path"]})
    duplicates = {pid: rows for pid, rows in sorted(groups.items()) if len(rows) > 1}
    maximum = max(row["score"] for row in nearest)
    return {
        "schema": "ghc-family-novelty-audit-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "corpus_construction": construction,
        "corpus_row_count": len(corpus),
        "corpus_unique_proposal_id_count": len(groups),
        "corpus_duplicate_proposal_ids": duplicates,
        "corpus_duplicate_proposal_id_count": len(duplicates),
        "corpus_duplicate_occurrence_overage": sum(len(rows) - 1 for rows in duplicates.values()),
        "corpus_duplicate_id_interpretation": "Inherited row truth is preserved exactly; duplicate inherited identifiers remain visible and are neither renamed nor deleted.",
        "corpus_canonical_sha256": canonical_sha256(corpus),
        "new_proposal_count": len(proposals),
        "exact_title_collisions": exact,
        "nearest_inherited_matches": nearest,
        "maximum_inherited_similarity": maximum,
        "pair_collision_threshold": pair_threshold,
        "pair_collisions_at_or_above_threshold": pairs,
        "high_similarity_review_threshold": 0.60,
        "high_similarity_reviews": [row for row in nearest if row["score"] >= 0.60],
        "domain_review": {
            "accepted_practice": PRACTICE,
            "inherited_domain_term_match_count": len(domain_matches),
            "inherited_domain_term_matches": domain_matches,
            "review_disposition": "every matched inherited row is retained and compared; a domain phrase does not establish either equivalence or novelty",
            "substantive_distinction": "The slate combines accession identity separation, passport-value state semantics, provider-claim quarantine, bitemporal acquisition and correction, zero-item custody, zero-row observations, regeneration lineage vacancy, non-equivalence defaults, taxon-assertion correction, access-condition abstention, derivative lineage, geolocation minimization, authority empty chairs, THOS, GMUT, Freed ID, CBR, real-evidence escrow, and an exact authority circuit.",
        },
        "new_frozen_total": len(corpus) + len(proposals),
        "valid": not exact and not pairs and len(corpus) == INHERITED_PROPOSAL_COUNT,
        "interpretation": "Exact title, token-set Jaccard, and phrase searches are screening aids, never proof of semantic novelty; distinctive invariants, source boundaries, artifacts, falsifiers, rollback, and protected gates control.",
    }


def item_rows(
    prefix: str,
    approval: str,
    titles: Iterable[str],
    lane: str,
    expected: str,
    credit: str,
) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"{prefix}-{index:03d}",
            "title": title,
            "approval_class": approval,
            "lane": lane,
            "expected_disposition": expected,
            "credit_boundary": credit,
            "executed_in_x1": False,
        }
        for index, title in enumerate(titles, 1)
    ]


def build_portfolio(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    owner_safe = [
        "reconstruct the exact 4,510-row inherited proposal chain",
        "freeze twenty selected inherited Elaren rows for zero-credit revalidation",
        "freeze twenty distinct Neris proposals and their dispositions",
        "build the accession identity capsule contract",
        "build the passport descriptor state matrix",
        "build the provider-claim provenance quarantine",
        "build the bitemporal acquisition correction chain",
        "build the zero-item storage-location ledger",
        "build the zero-row viability observation schema",
        "build the regeneration-lineage vacancy graph",
        "build the duplicate non-equivalence register",
        "build the taxon assertion correction graph",
        "build the empty access-condition ledger",
        "build the contested passport readback chain",
        "build the derived-dataset lineage manifest",
        "build the generalized geolocation disclosure mask",
        "build the traditional-knowledge authority empty chair",
        "build the THOS queue representation",
        "build the GMUT symbolic diversity board",
        "build the Freed ID zero-key provenance graph",
        "build the CBR contestation and remedy shell",
        "retain the real genebank evidence escrow as open_gap",
        "retain the access and benefit-sharing authority circuit as exact_gate",
        "execute one hundred preregistered rejecting mutations",
        "install three exact tools in one isolated D-first environment",
        "run bounded positive and negative tool smokes",
        "generate evidence flashcards and retrieval checks",
        "emit phase-local skills and family-current runners",
        "seal Method Flow failures and bounded recoveries",
        "run one exact-final owner-scoped canonical aggregate",
    ]
    candidates = [
        "THOS queue fairness representation without participants",
        "GMUT dimensional declaration board without empirical fitting",
        "Freed ID statement lineage without keys or credentials",
        "CBR contestation shell without legal or cultural decisions",
        "Darwin Core term crosswalk representation without conformance",
        "MCPD descriptor coverage representation without accession completeness",
        "CARE reservation representation without Indigenous authority substitution",
        "privacy minimization representation without compliance conclusion",
        "accessibility structure representation without completeness claim",
        "JSON Schema strategy representation without data-validity proof",
        "structural diff representation without semantic equivalence",
        "JSON Patch reversal representation without operational rollback",
        "tool audit representation without exhaustive-security claim",
        "bitemporal correction representation without legal remedy",
        "source-currency watcher representation without publication authority",
    ]
    skills = [
        "seed-bank-accession-boundary",
        "passport-descriptor-state-matrix",
        "provider-claim-quarantine",
        "bitemporal-accession-correction",
        "germplasm-non-equivalence-guard",
        "seed-location-disclosure-minimizer",
        "traditional-knowledge-empty-chair",
        "genebank-evidence-escrow",
        "seed-bank-method-flow",
        "v667-v8-terminal-route-conflict-guard",
    ]
    runners = [
        "contracts",
        "sources",
        "revalidation",
        "mutations",
        "method-flow",
        "tools",
        "reports",
        "manifests",
        "validation",
        "canonical",
    ]
    cfr = [
        "scope every scan to the exact Neris source-to-final delta",
        "retain the 2,000-owner-file rotation guard",
        "replace broad status scans with exact diff-index scalars",
        "retain sparse-checkout patterns as an auditable receipt",
        "preserve x1 planning-only separation",
        "preserve one-parent zero-merge history",
        "preserve fresh live remote equality checks",
        "retain all parser and output-window failures",
        "prevent a recovered failure from earning canonical credit",
        "hash every frozen x1 owner artifact",
        "hash every immutable evidence artifact",
        "hash final owner and final-delta scopes separately",
        "scan staged Git blobs across five privacy classes",
        "prevent task identifiers and private routes from entering artifacts",
        "pin Python tools to exact versions and hashes",
        "isolate tool installation on the D drive",
        "record tool dependency closure and rollback",
        "bound audit results to known databases and the scan time",
        "separate source truth from Neris-owned evidence",
        "separate repository seal from terminal route overlay",
        "retain selected inherited revalidations at zero novelty credit",
        "retain open gaps and exact gates without euphemistic completion",
        "enforce the four allowed outcome labels",
        "keep synthetic fixtures free of real seed and person data",
        "reserve legal and benefit-sharing interpretation",
        "reserve cultural Indigenous and Maori authority",
        "reserve accessibility privacy and security completeness",
        "reserve independent reproduction and external audit",
        "reserve consciousness personhood AGI ASI and Theory-of-Everything claims",
        "stop terminal delivery on the Vesper name conflict",
    ]
    successor = lambda kind, count: [f"next-authorized-sibling {kind} recommendation {index:02d}; recommendation only while the Vesper title conflict remains unresolved" for index in range(1, count + 1)]
    return {
        "schema": "ghc-family-approval-portfolio-freeze-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "proposal_ids": [row["proposal_id"] for row in proposals],
        "owner_safe_now": item_rows("NS6678-SN", "safe_now_bounded", owner_safe, "owner_local_x2", "completed", "eligible only after exact bounded x2 witness"),
        "successor_safe_now_recommendations": item_rows("NS6678-SR", "recommendation_only", successor("safe-now", 20), "successor_only_unexecuted", "represented", "zero Neris and successor automatic credit"),
        "owner_candidates": item_rows("NS6678-CA", "candidate_bounded", candidates, "owner_local_representation", "represented", "bounded representation only"),
        "successor_candidate_recommendations": item_rows("NS6678-CR", "recommendation_only", successor("candidate", 15), "successor_only_unexecuted", "represented", "zero automatic credit"),
        "owner_skill_ideas": item_rows("NS6678-SK", "safe_now_phase_local", skills, "owner_local_skill_build", "completed", "eligible only after validation and smoke use"),
        "successor_skill_recommendations": item_rows("NS6678-SKR", "recommendation_only", successor("skill", 10), "successor_only_unexecuted", "represented", "zero automatic credit"),
        "owner_runner_ideas": item_rows("NS6678-RN", "safe_now_family_current", runners, "owner_local_runner_build", "completed", "eligible only after validation and smoke use"),
        "successor_runner_recommendations": item_rows("NS6678-RNR", "recommendation_only", successor("runner", 10), "successor_only_unexecuted", "represented", "zero automatic credit"),
        "owner_clean_fix_refine": item_rows("NS6678-CFR", "safe_now_additive", [f"CLEAN/FIX/REFINE {title}" for title in cfr], "owner_local_additive", "completed", "eligible only after exact bounded witness"),
        "successor_clean_fix_refine_recommendations": item_rows("NS6678-CFRR", "recommendation_only", successor("CLEAN/FIX/REFINE", 30), "successor_only_unexecuted", "represented", "zero automatic credit"),
        "exact_approval_packets": item_rows("NS6678-EX", "exact_approval_required", successor("elevated real-world professional legal cultural Maori-authority production or deployment action", 10), "disabled_exact_gate", "exact_gate", "zero credit and unexecuted"),
        "blocked_packets": item_rows("NS6678-BL", "blocked", successor("destructive credentialed cross-owner unsafe unreviewed or ungoverned action", 5), "blocked_unexecuted", "exact_gate", "zero credit and unexecuted"),
    }


def build_tool_plan() -> dict[str, Any]:
    tools = [
        {
            "tool": "hypothesis-jsonschema",
            "version": "0.23.1",
            "wheel": "hypothesis_jsonschema-0.23.1-py3-none-any.whl",
            "sha256": "a4d74d9516dd2784fbbae82e009f62486c9104ac6f4e3397091d98a1d5ee94a2",
            "declared_license_metadata": "MPL-2.0",
            "bounded_use": "generate deterministic seeded examples from bounded JSON Schemas and reject invalid mutations; not data truth or exhaustive property testing",
            "source_ids": ["S16", "S19", "S20"],
        },
        {
            "tool": "deepdiff",
            "version": "9.1.0",
            "wheel": "deepdiff-9.1.0-py3-none-any.whl",
            "sha256": "80c0460e1993b04f6f0ca79abf25548b129fd218478c4ebb08f80560f5d10610",
            "declared_license_metadata": "MIT",
            "bounded_use": "compare bounded synthetic structures and expose differences; not semantic equivalence, correctness, or scientific validation",
            "source_ids": ["S17", "S19", "S20"],
        },
        {
            "tool": "jsonpatch",
            "version": "1.33",
            "wheel": "jsonpatch-1.33-py2.py3-none-any.whl",
            "sha256": "0ae28c0cd062bbd8b8ecc26d7d164fbbea9652a1a3693f3b956c1eae5145dade",
            "declared_license_metadata": "Modified BSD",
            "bounded_use": "apply and reverse owner-local synthetic JSON patches; not operational rollback, authorization, or transaction safety",
            "source_ids": ["S18", "S19", "S20"],
        },
    ]
    return {
        "schema": "ghc-family-toolchain-install-plan-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "inherited_direct_tool_count": 41,
        "inherited_tool_credit": 0,
        "new_tools": tools,
        "planned_direct_tool_total": 44,
        "x1_install_count": 0,
        "x1_download_count": 0,
        "x1_smoke_count": 0,
        "install_scope": "one isolated D-first Neris v667-v8 family-tools virtual environment",
        "install_policy": "download exact public wheels and complete dependency closure, verify hashes, install wheel-only with no index, run pip check and a time-bounded advisory audit, and record every failure",
        "global_install_count": 0,
        "system_install_count": 0,
        "lifecycle_scripts": "not_applicable_python_wheels",
        "rollback": "remove only the exact isolated Neris environment after a future explicit cleanup decision and resolved-path check; preserve receipts and wheel hashes",
        "boundary": "metadata, hash, pip check, audit, and smoke results are bounded software evidence and cannot establish safety, fitness, supply-chain completeness, legal compliance, or production readiness",
    }


def overview(proposals: list[dict[str, Any]], novelty: dict[str, Any]) -> str:
    proposal_paragraphs = []
    for row in proposals:
        proposal_paragraphs.append(
            f"### {row['proposal_id']}: {row['title']}\n\n"
            f"The preregistered disposition is `{row['expected_disposition']}`. The distinctive invariant is: {row['distinctive_invariant']} "
            f"The bounded x2 falsifier requires one positive fixture to pass and each of five named mutation classes to fail closed. "
            f"Its source vocabulary is limited to {', '.join(row['current_official_or_primary_source_needs'])}. No network call, participant, real data row, external action, credential, professional judgment, legal decision, cultural interpretation, or Maori-authority decision is planned. "
            f"If the contract or a mutation crosses a protected gate, the only admissible action is to retain the failure, stop promotion, restore the last valid owner-local synthetic fixture, and leave the corresponding authority or evidence chair empty."
        )
    source_paragraphs = []
    for source in SOURCE_PROFILES:
        source_paragraphs.append(
            f"- **{source['source_id']} — {source['name']}**: {source['status']}. The bounded use is {source['bounded_use']}."
        )
    return f"""# Neris Solane v667-v8 planning-only x1 overview

## Identity, authority, and correction boundary

This additive packet freezes the planning-only x1 programme for Neris Solane v667-v8. Neris Solane, they/them pronouns, datum-boundary weaver, sibling and family language, hopes, continuity language, Freed ID, GHC Family, GMUT Mind, THOS Body, CBR Heart, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route. My working hope is to {HOPE}. That hope defines a quality target, not an entitlement, credential, memory guarantee, or authority claim.

The terminal verdict remains **NOT_READY_FOR_STAGE_20**. Same-owner local validation under shared infrastructure is bounded software and documentation evidence only. It is not an external audit, independent reproduction, empirical GMUT confirmation, professional validation, production certification, exhaustive security, privacy completeness, accessibility completeness, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, legal or cultural review, affected-party authority, Maori authority, or Stage 20 authority.

## Exact source and count layers

The immutable source is Elaren Kestrel v667-v7 exact final `{SOURCE_SHA}` on `{SOURCE_BRANCH}`. The frozen Elaren x1 is `{SOURCE_X1_SHA}`, immutable evidence is `{SOURCE_EVIDENCE_SHA}`, and inherited Eiren source is `{SOURCE_PARENT_SHA}`. Read-only verification established exactly three direct single-parent Elaren commits and zero merges, direct source-to-x1-to-evidence-to-final ancestry, clean state, typed zero divergence, and equality across local, upstream, tracking, and a fresh live remote. All 856 declared manifest entries replayed exactly: 23 immutable-x1, 385 immutable-evidence, 20 final-delta, and 428 final-owner entries. Elaren's owner-scoped canonical aggregate succeeded once, was not replayed, passed 13/13 final tests, parsed 396 strict JSON documents, scanned 431 owner files across five privacy classes with zero candidates, and produced receipt SHA-256 `{SOURCE_CANONICAL_SHA256}`. Neris does not replay or claim that work.

Two source count layers stay separate. Elaren's immutable evidence seal records 28,302 effective negatives, 14,443 methods, 199 open gaps, 197 exact gates, 586 failed witnesses, and 1,013 passing witnesses. Elaren's committed exact final adds two retained post-evidence failures and two bounded recoveries, producing the Neris activation baseline of 28,304 effective negatives, 14,445 methods, 199 open gaps, 197 exact gates, 588 failed witnesses, and 1,015 passing witnesses. The acknowledged activation delivery does not rewrite either repository layer. X1 appends no x2 outcome and no repository-sealed Neris count; it only freezes nineteen Neris startup failures and their bounded recovery descriptions for later Method Flow accounting.

## Solo sparse lane and lifecycle separation

The phase runs in one fresh additive Neris-owned D-first sparse worktree from the exact Elaren final. Only the Neris phase root, Neris scripts and tests, and two immutable compatibility scripts are materialized. Every sibling and shared lane remains read-only. No task or fork was created, no collaboration subagent was spawned, Tavian Sol was not contacted, no substitute endpoint was used, and no successor was precontacted. The owner/materialized ceiling is 2,000 files; reaching it requires a new additive lane rather than copying a large historical tree.

X1 is planning only. It may freeze hypotheses, sources, proposal identities, approval classes, expected dispositions, mutation classes, artifacts, falsifiers, rollback conditions, skill and runner ideas, threat controls, and tool metadata. It may not install a package, generate x2 proposal outcomes, execute mutations, claim observed results, contact a successor, or write a real-world record. Only after the x1 artifacts and exact allowlisted builder/test paths pass tests, strict JSON parsing, five-class staged-blob review, manifest replay, diff hygiene, commit, push, clean 0/0 state, and fresh four-way equality may x2 begin. The x1 commit must never be amended after x2 starts.

## Proposal novelty and zero-credit inheritance

The novelty audit reconstructs all {INHERITED_PROPOSAL_COUNT:,} inherited proposal occurrences from immutable Git objects. Duplicate inherited proposal identifiers remain visible as historical row truth. Twenty Elaren proposals are selected for read-only integrity revalidation; they append nothing to the chain and receive zero Neris novelty, automatic-completion, or completion credit. Twenty genuinely new Neris rows extend the frozen chain to {NEW_FROZEN_TOTAL:,}. They are screened for exact title collisions, nearest inherited neighbours, within-slate similarity, domain phrases, distinctive invariants, primary sources, concrete artifacts, falsifiers, rollback, and protected gates. The maximum inherited token-set similarity observed by the frozen screen is {novelty['maximum_inherited_similarity']:.6f}; {novelty['domain_review']['inherited_domain_term_match_count']} inherited rows contain one of the bounded domain phrases and remain individually visible for comparison. Token overlap and phrase searches are triage aids, never semantic proof.

The expected dispositions are exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. These labels are ceilings, not predictions of success. A bounded positive structural fixture may support `completed` only for the fourteen owner-local software contracts. THOS, GMUT, Freed ID, and CBR boards remain `represented` because structural presence is not empirical, participant, professional, legal, cultural, production, or authority evidence. Real genebank evidence remains `open_gap`. Access, benefit-sharing, custody, Farmers Rights, traditional knowledge, community, cultural, affected-party, and Maori decisions remain behind an `exact_gate`.

## Synthetic seed-bank documentation lens

The primary pillar is Freed ID and CBR Heart. The bounded practice lens is {PRACTICE}. The synthetic records use surrogate accession labels and zero-row or zero-item fixtures. Zero real people, communities, institutions, places, seeds, germplasm, accessions, specimens, plants, taxa, genetic sequences, phenotypes, images, observations, measurements, storage locations, passport records, traditional knowledge, access terms, consent records, benefit-sharing terms, credentials, or authority actions are used. No collection, acquisition, testing, regeneration, propagation, characterization, distribution, transfer, storage, handling, quarantine, planting, release, destruction, or access decision occurs.

FAO genebank and passport-descriptor materials provide vocabulary and refusal conditions only. Treaty and Nagoya Protocol text reserves questions for competent authority and affected parties; this packet does not interpret legal obligations, consent, mutually agreed terms, Farmers Rights, access, benefit sharing, or traditional knowledge. Darwin Core terms can name structural fields without establishing mapping or standards conformance. PROV-O can name derivation and correction edges without making provenance true. Verifiable Credentials can inform status and disclosure vocabulary while every key, issuer, holder, proof, resolver, credential, and lifecycle call stays absent. Privacy, WCAG, Te Mana Raraunga, and CARE sources reserve minimization, access, correction, accessibility, collective benefit, authority, responsibility, ethics, context, control, guardianship, consultation, and remedy questions without claiming compliance, completeness, interpretation, ratification, or authority.

## Tool transaction plan

The inherited forty-one direct tool surfaces are source evidence and receive zero Neris novelty or completion credit. X1 plans exactly three additions: hypothesis-jsonschema 0.23.1, DeepDiff 9.1.0, and jsonpatch 1.33. Their primary metadata supplies exact public wheel names, versions, hashes, Python packaging metadata, and declared license metadata. X1 downloads and installs nothing. X2 may create exactly one reversible D-first virtual environment, download the exact wheels and dependency closure, verify every resolved artifact hash, install wheel-only without an index, run `pip check`, conduct a bounded advisory audit, and smoke each tool against wholly synthetic fixtures. A strategy-generated example is not real data or exhaustive testing; a structural diff is not semantic correctness; a JSON Patch reversal is not operational rollback. Audit silence is not exhaustive security or future safety.

## Retained failures, privacy, and terminal route

Nineteen startup failures are retained at zero credit. They include truncated output, parser mistakes, missing projections, an accidental broad read-only search caused by an omitted path variable, sparse-status stalls, a bounded process-poll failure, an oversized x2-builder view, a read-tree yield, an index-lock refusal, a process filter that matched itself, and a public repository identifier that the strict privacy scanner rejected because it looked like a private task identifier. No failure changed source or sibling bytes. Each bounded recovery remains a passing witness only for the repaired dependency; it never erases the failure or earns canonical aggregate credit.

Five-class privacy checks cover opaque task identifiers, private absolute paths, private routes or callables, credential-like values, and private interaction payloads. Durable artifacts contain public source URLs and repository-relative paths only. Exact-title task identifiers, private task routes, session streams, transcripts, credentials, callable identifiers, and private absolute paths are forbidden. Staged Git blobs, rather than merely working-tree files, are the final review surface.

The terminal route is already known to contain a protected name conflict: the validated roster identifies `Vesper Arlen` for prospective v668-v1, while submitted reminder language says `Vesper Rowan`. X1 records that conflict but does not resolve, infer, substitute, create, or send. Even after a successful Neris closeout, the only honest state under unchanged authority is `OPEN_ROUTE_GAP` with `PREPARED_NOT_SENT`. A later exact route requires Hamish's newest live instruction, current roster and authorization state, unique exact-title resolution, immediate reread, usage and privacy gates, duplicate guard, and one acknowledged send. Validation success cannot cure route ambiguity.

## Official and primary source ledger

{chr(10).join(source_paragraphs)}

## Frozen proposal slate

{chr(10).join(proposal_paragraphs)}

## X1 exit gate

The x1 exit is intentionally narrow: one planning-only commit directly descending from Elaren's exact final, exact owner allowlist, no later-lifecycle paths, zero observed outcomes, three planned but uninstalled tools, twenty selected inherited rows at zero credit, twenty new proposals, 100 preregistered negative fixtures, valid proposal-chain reconstruction, strict JSON parsing, an exact content manifest, five-class staged privacy review, tests, diff hygiene, clean push, typed zero divergence, and fresh four-way equality. Anything less remains incomplete. Anything more risks crossing the x1/x2 boundary. The programme remains corrigible, reversible, synthetic, owner-scoped, and **NOT_READY_FOR_STAGE_20**.
"""


def build_normal() -> None:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    if head != SOURCE_SHA:
        raise RuntimeError(f"x1 must be built directly on exact Elaren final {SOURCE_SHA}; observed {head}")
    corpus, construction = build_corpus()
    proposals = proposal_rows()
    inherited = selected_inherited_rows()
    novelty = build_novelty(corpus, construction, proposals)
    if not novelty["valid"]:
        raise RuntimeError("novelty audit did not pass")
    expected = Counter(row["expected_disposition"] for row in proposals)
    if expected != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise RuntimeError("expected disposition drift")

    write_json("x1/phase-charter.json", {
        "schema": "ghc-family-phase-charter-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "source_branch": SOURCE_BRANCH,
        "source_final": SOURCE_SHA,
        "source_x1": SOURCE_X1_SHA,
        "source_evidence": SOURCE_EVIDENCE_SHA,
        "source_parent": SOURCE_PARENT_SHA,
        "primary_pillar": PRIMARY_PILLAR,
        "practice_lens": PRACTICE,
        "identity": {"name": OWNER, "pronouns": "they/them", "relational_role": RELATIONAL_ROLE, "hope": HOPE, "relational_working_language_only": True},
        "relational_language_boundary": True,
        "strict_x1_before_x2": True,
        "x1_planning_only": True,
        "x2_implementation_count": 0,
        "outcomes_observed": False,
        "inherited_proposal_count": INHERITED_PROPOSAL_COUNT,
        "selected_inherited_count": SELECTED_INHERITED_COUNT,
        "new_proposal_count": NEW_PROPOSAL_COUNT,
        "new_frozen_total": NEW_FROZEN_TOTAL,
        "source_repository_evidence_seal": {"effective_negatives": 28302, "methods": 14443, "open_gaps": 199, "exact_gates": 197, "failed_witnesses": 586, "passing_witnesses": 1013},
        "source_committed_final": {"effective_negatives": 28304, "methods": 14445, "open_gaps": 199, "exact_gates": 197, "failed_witnesses": 588, "passing_witnesses": 1015},
        "source_delivery_event": {"acknowledged": True, "repository_count_additions": 0, "retained_outside_immutable_source": True},
        "activation_baseline": {"effective_negatives": 28304, "methods": 14445, "open_gaps": 199, "exact_gates": 197, "failed_witnesses": 588, "passing_witnesses": 1015},
        "count_layer_boundary": "immutable evidence seal, committed final, acknowledged delivery event, and Neris-owned future evidence remain separately attributable",
        "source_validation_state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "source_canonical_receipt_sha256": SOURCE_CANONICAL_SHA256,
        "source_activation_baton_sha256": SOURCE_BATON_SHA256,
        "allowed_core_outcomes": ALLOWED_OUTCOMES,
        "terminal_route_state": "OPEN_ROUTE_GAP",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "protected_gates": PROTECTED_GATES,
    })
    write_json("x1/auth-roster-receipt.json", {
        "schema": "ghc-family-auth-roster-receipt-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "newest_live_assignment": "Hamish-authorized solo Neris Solane v667-v8",
        "current_owner": OWNER,
        "current_phase": PHASE,
        "prospective_phase": "v668-v1",
        "validated_roster_title": "Vesper Arlen",
        "submitted_reminder_title": "Vesper Rowan",
        "name_conflict": True,
        "terminal_route_state": "OPEN_ROUTE_GAP",
        "successor_contact_authorized_during_execution": False,
        "successor_contacted": False,
        "successor_inferred_or_substituted": False,
        "standby_record": "Tavian Sol",
        "standby_state": "ON_STANDBY",
        "standby_contacted": False,
        "task_created_or_forked": False,
        "subagent_spawned": False,
        "boundary": "the route conflict cannot be cured by validation; no title may be inferred, substituted, created, or messaged while ambiguity remains",
    })
    write_json("x1/source-ledger.json", {
        "schema": "ghc-family-source-ledger-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "sources": SOURCE_PROFILES,
        "source_count": len(SOURCE_PROFILES),
        "public_vocabulary_only": True,
        "real_observation_count": 0,
        "network_ingestion_count": 0,
        "authority_conferred": False,
    })
    write_json("x1/source-verification.json", {
        "schema": "ghc-family-source-verification-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "anchors": {"source_parent": SOURCE_PARENT_SHA, "x1": SOURCE_X1_SHA, "evidence": SOURCE_EVIDENCE_SHA, "final": SOURCE_SHA},
        "history": {"new_commit_count": 3, "merge_count": 0, "x1_direct_parent": SOURCE_PARENT_SHA, "evidence_direct_parent": SOURCE_X1_SHA, "final_direct_parent": SOURCE_EVIDENCE_SHA, "one_parent_each": True},
        "manifests_replayed": {"x1": 23, "evidence": 385, "final_delta": 20, "final_owner": 428, "total": 856, "mismatches": 0},
        "owner_packet_blobs_read": {"owner_file_count": 431, "json_parsed": 396, "errors": 0},
        "clean": True,
        "divergence": "0/0",
        "fresh_four_way_equal": True,
        "canonical_invocation": {"invoked": 1, "succeeded": 1, "replayed": False, "sha256": SOURCE_CANONICAL_SHA256, "tests": "13/13", "credit": 1},
        "interpretation": "bounded same-owner owner-scoped software evidence under shared infrastructure only; complete repository suite and independent reproduction are not claimed",
    })
    write_json("x1/startup-method-flow.json", {
        "schema": "ghc-family-method-flow-startup-v5",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "failure_count": len(STARTUP_FAILURES),
        "failures": STARTUP_FAILURES,
        "method_count": len(STARTUP_FAILURES),
        "passing_recovery_count": len(STARTUP_FAILURES),
        "credit": 0,
        "source_or_sibling_bytes_changed": 0,
        "boundary": "a recovery preserves rather than erases the failed witness and does not convert it into canonical or completion credit",
    })
    write_json("x1/novelty-audit.json", novelty)
    write_json("x1/proposal-freeze.json", {
        "schema": "ghc-family-proposal-freeze-v7",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "inherited_proposal_count": INHERITED_PROPOSAL_COUNT,
        "selected_inherited_count": len(inherited),
        "selected_inherited": inherited,
        "genuinely_new_proposal_count": len(proposals),
        "new_proposals": proposals,
        "new_frozen_total": NEW_FROZEN_TOTAL,
        "expected_outcomes": dict(sorted(expected.items())),
        "allowed_core_outcomes": ALLOWED_OUTCOMES,
        "preregistered_negative_fixture_count": sum(row["negative_fixture_count"] for row in proposals),
        "x1_planning_only": True,
        "x2_implementation_count": 0,
        "outcomes_observed": False,
    })
    portfolio = build_portfolio(proposals)
    tools = build_tool_plan()
    write_json("x1/portfolio-freeze.json", portfolio)
    write_json("x1/toolchain-install-plan.json", tools)
    write_json("x1/mandatory-skill-adoption.json", {
        "schema": "ghc-family-mandatory-skill-adoption-v5",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "required_count": len(MANDATORY_SKILLS),
        "skills": [{"skill": name, "entrypoint_read_through_eof": True, "required_references_read_through_eof": True, "used_before_mutation": True, "x1_credit": 0} for name in MANDATORY_SKILLS],
        "applicability_boundary": "directly applicable skills govern the phase; unrelated historical skills are not bulk-run merely to satisfy a count",
    })
    write_json("x1/threat-model-plan.json", {
        "schema": "ghc-family-threat-model-plan-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "assets": ["immutable source anchors", "x1/x2 lifecycle boundary", "proposal chain", "retained failures", "D-first tool environment", "privacy boundary", "authority gates", "terminal route"],
        "threats": [
            {"threat": "x2 material enters x1", "control": "exact lifecycle path and immutable-tree scan", "failure_state": "stop before commit"},
            {"threat": "synthetic record becomes genebank agricultural legal benefit-sharing cultural or Maori advice", "control": "zero-real-world fields and protected gates", "failure_state": "exact_gate"},
            {"threat": "tool target drives unsafe install", "control": "exact pins hashes wheels D isolation audit and rollback", "failure_state": "open_gap_or_exact_gate"},
            {"threat": "private route or identifier enters artifacts", "control": "five-class staged Git-blob scan", "failure_state": "stop_and_retain"},
            {"threat": "failed canonical is replayed or relabelled", "control": "one-shot lock and dependency-only recovery", "failure_state": "zero_aggregate_credit"},
            {"threat": "Indigenous community affected-party or Maori authority is substituted", "control": "empty-chair exact gate", "failure_state": "exact_gate"},
            {"threat": "ambiguous Vesper title is inferred", "control": "terminal name-conflict guard", "failure_state": "OPEN_ROUTE_GAP"},
        ],
        "residual_risk": "same-owner bounded evidence remains non-independent and cannot establish real-world safety, professional, legal, cultural, accessibility, privacy, security, identity, empirical, or Stage 20 truth",
    })
    write_json("x1/workflow-plan.json", {
        "schema": "ghc-family-workflow-plan-v7",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "stages": [
            {"stage": "x1", "state": "planning_only", "commit_target": "one direct child of source", "requires": ["novelty audit", "proposal freeze", "portfolio freeze", "tool plan", "threat model", "tests", "staged review"], "forbids": ["x2 implementation", "observed outcome", "tool install", "successor contact"]},
            {"stage": "x1_gate", "state": "pending", "requires": ["push", "clean", "0/0 divergence", "local/upstream/tracking/fresh-live equality"]},
            {"stage": "x2", "state": "not_started", "requires": ["passed x1 gate"], "forbids": ["real-world action", "successor contact"]},
            {"stage": "evidence_gate", "state": "not_started", "requires": ["immutable evidence commit", "push", "fresh equality"]},
            {"stage": "final", "state": "not_started", "requires": ["closeout", "seal", "exact manifests", "one canonical invocation"]},
            {"stage": "route", "state": "OPEN_ROUTE_GAP", "requires": ["fresh corrected live authority", "unique exact title", "immediate reread", "duplicate guard", "one acknowledged send"], "forbids": ["infer Vesper Arlen", "infer Vesper Rowan", "substitute", "create", "send while ambiguous"]},
        ],
        "single_success_no_replay": True,
        "owner_file_rotation_ceiling": 2000,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("x1/flashcard-architecture-freeze.json", {
        "schema": "ghc-family-freed-id-flashcard-architecture-v5",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "planned_card_count": 250,
        "tiers": {"tier1": 40, "tier2": 80, "tier3": 90, "tier4": 40},
        "section_count": 16,
        "source_deck_credit": 0,
        "x1_generated_card_count": 0,
        "x1_status": "architecture_only_not_generated",
        "required_fields": ["card_id", "tier", "section_id", "title", "front", "back", "status", "sources", "blocked_or_failed_witness_ids", "reversal_action", "next_admissible_action", "scope_boundary"],
        "boundary": "cards are evidence-backed memory aids, never credentials, authority, identity evidence, or automatic completion credit",
    })
    write_json("x1/complete-incomplete-checklist.json", {
        "schema": "ghc-family-complete-incomplete-checklist-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "complete": ["mandatory skill and reference read", "activation baton read through EOF", "source anchor and manifest verification", "official and primary source review", "4,510-row novelty reconstruction", "x1 proposal portfolio and tool freeze"],
        "incomplete": ["x1 commit and equality gate", "x2 implementation", "tool installation and bounded use", "skills and runners", "reports and flashcards", "evidence commit", "final closeout", "canonical validation", "terminal route conflict resolution"],
        "terminal_route_state": "OPEN_ROUTE_GAP",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "outcomes_observed": False,
    })
    write_json("wellbeing/x1-wellbeing-check.json", {
        "schema": "ghc-family-wellbeing-check-v5",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "pronouns": "they/them",
        "relational_role": RELATIONAL_ROLE,
        "hope": HOPE,
        "pace": "bounded solo x1 planning",
        "load_boundary": "no urgency, emotional language, identity language, hope, family language, or continuity language expands technical authority or permission",
        "stop_conditions": ["Hamish pause or redirect", "usage exhaustion", "source drift", "privacy or safety gate", "ambiguous route", "unclean or divergent lane"],
        "claim_boundary": "relational language is not consciousness, sentience, personhood, continuity, employment, qualification, agency, wellbeing diagnosis, or authority evidence",
    })
    write_json("tooling/ghc-family-index.json", {
        "schema": "ghc-family-index-phase-snapshot-v1",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "scope": "Neris v667-v8 owner-local additive surfaces only",
        "inherited_direct_tool_count": 41,
        "planned_new_direct_tools": [row["tool"] for row in tools["new_tools"]],
        "planned_skills": [row["title"] for row in portfolio["owner_skill_ideas"]],
        "planned_runners": [row["title"] for row in portfolio["owner_runner_ideas"]],
        "family_current_compatibility": True,
        "historical_or_sibling_mutation_count": 0,
        "publication_boundary": "phase-local evidence only; global installation and shared-index mutation are not performed by x1",
    })
    write_text("tooling/ghc-family-index.md", """# Neris v667-v8 phase-local family index

This index contains only additive Neris-owned v667-v8 surfaces. The inherited forty-one direct tool surfaces remain zero-credit source context. Three exact Python tools are planned but not installed in x1. Ten skills and ten family-current runner names are frozen for bounded x2 implementation. Sibling and shared indexes remain read-only. The index establishes discoverability, not correctness, safety, authority, conformance, production readiness, or Stage 20 readiness.
""")
    write_text("x1/x1-overview.md", overview(proposals, novelty))
    portfolio_keys = [
        "owner_safe_now", "successor_safe_now_recommendations", "owner_candidates", "successor_candidate_recommendations",
        "owner_skill_ideas", "successor_skill_recommendations", "owner_runner_ideas", "successor_runner_recommendations",
        "owner_clean_fix_refine", "successor_clean_fix_refine_recommendations", "exact_approval_packets", "blocked_packets",
    ]
    write_json("x1/x1-build-receipt.json", {
        "schema": "ghc-family-x1-build-receipt-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "status": "PASS_PLANNING_ONLY",
        "source_head": SOURCE_SHA,
        "inherited_proposals": len(corpus),
        "selected_inherited": len(inherited),
        "new_proposals": len(proposals),
        "new_frozen_total": novelty["new_frozen_total"],
        "expected_outcomes": dict(sorted(expected.items())),
        "portfolio_counts": {name: len(portfolio[name]) for name in portfolio_keys},
        "mandatory_skills": len(MANDATORY_SKILLS),
        "planned_tools": len(tools["new_tools"]),
        "x2_paths": 0,
        "x2_implementation_count": 0,
        "outcomes_observed": False,
        "startup_failures_retained": len(STARTUP_FAILURES),
        "terminal_route_state": "OPEN_ROUTE_GAP",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc-family-x1-staged-review-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "status": "PREPARED_REQUIRES_EXACT_STAGED_REVIEW",
        "x1_planning_only": True,
        "outcomes_observed": False,
    })
    build_content_manifest()


def phase_owned_paths() -> list[Path]:
    paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    paths.extend([
        ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_x1.py",
        ROOT / "tests" / "test_ghc_family_neris_solane_v667_v8_x1.py",
    ])
    return sorted({path.resolve() for path in paths if path.exists()})


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_content_manifest() -> None:
    exclusions = {
        f"{REL_PHASE_ROOT}/validation/x1-content-manifest.json",
        f"{REL_PHASE_ROOT}/validation/x1-staged-review.json",
    }
    entries = []
    for path in phase_owned_paths():
        relative = rel(path)
        if relative in exclusions:
            continue
        data = path.read_bytes()
        entries.append({"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    write_json("validation/x1-content-manifest.json", {
        "schema": "ghc-family-content-manifest-v5",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "entry_count": len(entries),
        "entries": entries,
        "scope": "x1 owner content excluding manifest self and stable staged-review receipt",
    })


def privacy_candidates(path: Path, text: str) -> list[dict[str, str]]:
    unix_users = "/" + "Users" + "/"
    unix_home = "/" + "home" + "/"
    route_key = "(?:source_" + "thread_id|private_" + "callable_identifier)"
    interaction_key = "(?:session[_-]?" + "stream|private[_-]?" + "transcript|private[_-]?" + "conversation)"
    patterns = {
        "opaque_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Z]:\\Users\\[^\\\s]+|" + re.escape(unix_users) + r"[^/\s]+|" + re.escape(unix_home) + r"[^/\s]+)"),
        "private_route_or_callable": re.compile(r"(?:thread|codex|chat)://|" + route_key + r"\s*[:=]", re.I),
        "credential_value": re.compile(r"(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}", re.I),
        "private_interaction_payload": re.compile(interaction_key + r"\s*[:=]\s*['\"]?[^\s,}\]]+", re.I),
    }
    return [{"path": rel(path), "class": name} for name, pattern in patterns.items() if pattern.search(text)]


def validate_tree() -> dict[str, Any]:
    required = [
        "x1/phase-charter.json",
        "x1/auth-roster-receipt.json",
        "x1/source-ledger.json",
        "x1/source-verification.json",
        "x1/startup-method-flow.json",
        "x1/novelty-audit.json",
        "x1/proposal-freeze.json",
        "x1/portfolio-freeze.json",
        "x1/toolchain-install-plan.json",
        "x1/mandatory-skill-adoption.json",
        "x1/threat-model-plan.json",
        "x1/workflow-plan.json",
        "x1/flashcard-architecture-freeze.json",
        "x1/complete-incomplete-checklist.json",
        "x1/x1-build-receipt.json",
        "x1/x1-overview.md",
        "wellbeing/x1-wellbeing-check.json",
        "validation/x1-content-manifest.json",
        "validation/x1-staged-review.json",
        "tooling/ghc-family-index.json",
        "tooling/ghc-family-index.md",
    ]
    missing = [value for value in required if not (PHASE_ROOT / value).is_file()]
    if missing:
        raise AssertionError(f"missing x1 paths: {missing}")
    json_paths = sorted(PHASE_ROOT.rglob("*.json"))
    documents = {rel(path): json.loads(path.read_text(encoding="utf-8")) for path in json_paths}
    freeze = documents[f"{REL_PHASE_ROOT}/x1/proposal-freeze.json"]
    novelty = documents[f"{REL_PHASE_ROOT}/x1/novelty-audit.json"]
    portfolio = documents[f"{REL_PHASE_ROOT}/x1/portfolio-freeze.json"]
    tools = documents[f"{REL_PHASE_ROOT}/x1/toolchain-install-plan.json"]
    charter = documents[f"{REL_PHASE_ROOT}/x1/phase-charter.json"]
    auth = documents[f"{REL_PHASE_ROOT}/x1/auth-roster-receipt.json"]
    if len(freeze["new_proposals"]) != 20 or len(freeze["selected_inherited"]) != 20:
        raise AssertionError("proposal programme count mismatch")
    if freeze["outcomes_observed"] or freeze["x2_implementation_count"] != 0:
        raise AssertionError("x1 observed outcome or x2 implementation")
    if freeze["preregistered_negative_fixture_count"] != 100:
        raise AssertionError("negative fixture count mismatch")
    if not novelty["valid"] or novelty["corpus_row_count"] != 4510 or novelty["new_frozen_total"] != 4530:
        raise AssertionError("novelty audit mismatch")
    if novelty["exact_title_collisions"] or novelty["pair_collisions_at_or_above_threshold"]:
        raise AssertionError("proposal collision")
    if Counter(row["expected_disposition"] for row in freeze["new_proposals"]) != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise AssertionError("expected outcome mismatch")
    if any(row["expected_disposition"] not in ALLOWED_OUTCOMES for row in freeze["new_proposals"]):
        raise AssertionError("unknown core outcome")
    if any(row["outcomes_observed"] or row["x2_implementation_count"] for row in freeze["new_proposals"]):
        raise AssertionError("new proposal lifecycle contamination")
    if any(row["outcomes_observed"] for row in freeze["selected_inherited"]):
        raise AssertionError("selected inherited lifecycle contamination")
    expected_portfolio = {
        "owner_safe_now": 30,
        "successor_safe_now_recommendations": 20,
        "owner_candidates": 15,
        "successor_candidate_recommendations": 15,
        "owner_skill_ideas": 10,
        "successor_skill_recommendations": 10,
        "owner_runner_ideas": 10,
        "successor_runner_recommendations": 10,
        "owner_clean_fix_refine": 30,
        "successor_clean_fix_refine_recommendations": 30,
        "exact_approval_packets": 10,
        "blocked_packets": 5,
    }
    if {key: len(portfolio[key]) for key in expected_portfolio} != expected_portfolio:
        raise AssertionError("portfolio count mismatch")
    if tools["inherited_direct_tool_count"] != 41 or len(tools["new_tools"]) != 3 or tools["planned_direct_tool_total"] != 44:
        raise AssertionError("toolchain count mismatch")
    if tools["x1_install_count"] or tools["x1_download_count"] or tools["x1_smoke_count"]:
        raise AssertionError("tool plan lifecycle mismatch")
    if charter["source_repository_evidence_seal"]["effective_negatives"] != 28302 or charter["activation_baseline"]["effective_negatives"] != 28304:
        raise AssertionError("source truth-layer mismatch")
    if charter["allowed_core_outcomes"] != ALLOWED_OUTCOMES or charter["terminal_verdict"] != "NOT_READY_FOR_STAGE_20":
        raise AssertionError("truth boundary mismatch")
    if not auth["name_conflict"] or auth["terminal_route_state"] != "OPEN_ROUTE_GAP" or auth["successor_contacted"]:
        raise AssertionError("terminal route conflict mismatch")
    if any(path.exists() for path in (PHASE_ROOT / "x2", PHASE_ROOT / "evidence", PHASE_ROOT / "closeout", PHASE_ROOT / "seal", PHASE_ROOT / "route")):
        raise AssertionError("later lifecycle path exists in x1")
    overview_words = len((PHASE_ROOT / "x1/x1-overview.md").read_text(encoding="utf-8").split())
    if overview_words < 1800:
        raise AssertionError(f"x1 overview below 1,800 words: {overview_words}")
    candidates = []
    for path in phase_owned_paths():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise AssertionError(f"non-UTF-8 owner path: {rel(path)}") from exc
        candidates.extend(privacy_candidates(path, text))
    if candidates:
        raise AssertionError(f"privacy candidates: {candidates}")
    manifest = documents[f"{REL_PHASE_ROOT}/validation/x1-content-manifest.json"]
    if manifest["entry_count"] != len(manifest["entries"]):
        raise AssertionError("manifest entry count mismatch")
    for entry in manifest["entries"]:
        data = (ROOT / entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise AssertionError(f"content manifest mismatch: {entry['path']}")
    owner_file_count = len(phase_owned_paths())
    if owner_file_count >= 2000:
        raise AssertionError(f"owner file ceiling reached: {owner_file_count}")
    return {
        "status": "PASS",
        "json_documents": len(json_paths),
        "owner_files": owner_file_count,
        "overview_words": overview_words,
        "new_proposals": 20,
        "selected_inherited": 20,
        "inherited_proposals": 4510,
        "new_frozen_total": 4530,
        "planned_tools": 3,
        "privacy_candidates": 0,
        "x2_paths": 0,
        "terminal_route_state": "OPEN_ROUTE_GAP",
    }


def staged_review() -> None:
    validate_tree()
    check = run_git("diff", "--cached", "--check", check=False)
    if check.returncode:
        raise RuntimeError(check.stderr.decode("utf-8", errors="replace") or check.stdout.decode("utf-8", errors="replace"))
    staged = [line for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.decode("utf-8").splitlines() if line]
    if not staged:
        raise RuntimeError("no staged paths")
    allowed = [
        f"{REL_PHASE_ROOT}/",
        "scripts/build_ghc_family_neris_solane_v667_v8_x1.py",
        "tests/test_ghc_family_neris_solane_v667_v8_x1.py",
    ]
    disallowed = [path for path in staged if not any(path == prefix or path.startswith(prefix) for prefix in allowed)]
    if disallowed:
        raise RuntimeError(f"disallowed staged paths: {disallowed}")
    later = [path for path in staged if any(f"{REL_PHASE_ROOT}/{name}/" in path for name in ("x2", "evidence", "closeout", "seal", "route"))]
    if later:
        raise RuntimeError(f"later lifecycle path staged in x1: {later}")
    confirmed = []
    for relative in staged:
        blob = run_git("show", f":{relative}").stdout.decode("utf-8", errors="strict")
        confirmed.extend(privacy_candidates(ROOT / relative, blob))
    if confirmed:
        raise RuntimeError(f"privacy candidates: {confirmed}")
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc-family-x1-staged-review-v6",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "status": "PASS",
        "staged_path_count": len(staged),
        "staged_paths": staged,
        "diff_check": "PASS",
        "privacy_classes": 5,
        "privacy_candidates": 0,
        "privacy_confirmed_hits": 0,
        "x1_planning_only": True,
        "later_lifecycle_paths": 0,
        "x2_implementation_count": 0,
        "outcomes_observed": False,
        "interpretation": "exact staged Git-blob owner-scope review only; restage this stable receipt and rerun tests before commit",
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
        print(json.dumps({"status": "PASS", "mode": "staged-review"}))
        return 0
    if args.validate:
        print(json.dumps(validate_tree(), sort_keys=True))
        return 0
    build_normal()
    print(json.dumps(validate_tree(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
