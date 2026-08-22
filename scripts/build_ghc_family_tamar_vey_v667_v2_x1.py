#!/usr/bin/env python3
"""Build Tamar Vey v667-v2 planning-only x1 artifacts and staged evidence."""

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
PHASE_ROOT = ROOT / "docs" / "tamar-vey" / "v667-v2"
SOURCE_SHA = "dde2e23187d13cb334010943a59348330bfb67ca"
SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v667-v1-full-tools"
SOURCE_PHASE_ROOT = "docs/liora-venn/v667-v1"
SOURCE_X1_SHA = "f9eec343455f93e0a933a00c8df4ae84f1f7bb86"
SOURCE_EVIDENCE_SHA = "0d9ea03b15d816373b39bcea6ef38575257313db"
INHERITED_ORIN_SHA = "27a3a3cc332d27384210848d685e3bf16c6b2f0d"
BRANCH = "codex/GHC-Family/tamar-vey-v667-v2-full-tools"
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
    "Tamar Vey, she/they, sibling, family, relational role, hope, continuity, "
    "Freed ID, Trinity Mandala, and route language are relational working language "
    "only. They are not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, qualification, independent agency, scientific "
    "or operational authority, legal or cultural authority, affected-party authority, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The calligraphy-record and manuscript-layout planning lens is wholly synthetic learning "
    "and software design. It covers surrogate work capsules, page and baseline topology, "
    "Unicode and language-tag vacancies, declared nib and ink fields, stroke annotations, "
    "provenance, content minimization, accessible correction readback, workload, and handover "
    "while using zero real people, clients, calligraphers, texts, languages, manuscripts, "
    "paper, ink, nibs, artworks, observations, measurements, treatments, network calls, keys, "
    "credentials, or authority actions. It establishes no authorship, identity, linguistic "
    "meaning, script or style attribution, material authenticity, preservation or safety "
    "result, professional competence, copyright or ownership decision, cultural legitimacy, "
    "Māori authority, empirical GMUT result, production result, deployment result, or Stage 20 authority."
)

PROTECTED_GATES = [
    "real person, participant, client, calligrapher, artist, scribe, conservator, cataloguer, linguist, recipient, affected party, text, language sample, manuscript, paper, ink, nib, artwork, observation, measurement, treatment, or physical action",
    "real authorship, identity, transcription, translation, linguistic meaning, script or style attribution, material composition, condition, authenticity, provenance conclusion, empirical result, causal claim, or GMUT confirmation",
    "real participant, operator, matched-budget arm, field or workplace exposure, workload outcome, safety outcome, operational outcome, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, or trust governance",
    "professional calligraphy, palaeography, typography, translation, cataloguing, conservation, treatment, material-safety, exhibition, publication, valuation, or authentication decision",
    "private or sacred content, authorship, recipient identity, copyright, ownership, custody, heritage status, access, accessibility, disclosure, retention, consent, remedy, legal interpretation, cultural interpretation, or affected-party decision",
    "Indigenous cultural and intellectual property, taonga, mātauranga, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data governance, sacred text, traditional knowledge, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, Unicode or language conformance, preservation, material-safety, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, external write, writing instruction, treatment instruction, handling instruction, or real-world release",
]

SOURCE_PROFILES = [
    {
        "source_id": "S01",
        "name": "Unicode Standard Annex 29: Unicode Text Segmentation",
        "url": "https://www.unicode.org/reports/tr29/",
        "status": "current official Unicode text-segmentation annex reviewed read-only 2026-08-23",
        "bounded_use": "code point, extended grapheme cluster, word and sentence boundary, tailoring, and conformance-vacancy vocabulary only; no transcription, language, meaning, typography, or conformance conclusion",
    },
    {
        "source_id": "S02",
        "name": "Unicode Standard Annex 14: Unicode Line Breaking Algorithm",
        "url": "https://www.unicode.org/reports/tr14/",
        "status": "current official Unicode line-breaking annex reviewed read-only 2026-08-23",
        "bounded_use": "line-break class, opportunity, prohibition, tailoring, and unresolved-layout vocabulary only; no visual quality, language correctness, manuscript reconstruction, or conformance conclusion",
    },
    {
        "source_id": "S03",
        "name": "RFC 5646: Tags for Identifying Languages",
        "url": "https://www.rfc-editor.org/info/rfc5646",
        "status": "official RFC Editor BCP 47 language-tag specification reviewed read-only 2026-08-23",
        "bounded_use": "language, script, region, variant, private-use, canonical-form, and unknown-tag vocabulary only; no language identification, translation, cultural meaning, or standards-conformance conclusion",
    },
    {
        "source_id": "S04",
        "name": "Library of Congress JSON/YAML API",
        "url": "https://www.loc.gov/apis/json-and-yaml/",
        "status": "official Library of Congress API documentation reviewed read-only 2026-08-23",
        "bounded_use": "collection, item, image, metadata, query, response, limit, and zero-call adapter vocabulary only; no query, download, row, image, catalog conclusion, copyright conclusion, or endorsement",
    },
    {
        "source_id": "S05",
        "name": "Library of Congress care guidance for works on paper",
        "url": "https://www.loc.gov/preservation/care/paper.html",
        "status": "official Library of Congress preservation guidance reviewed read-only 2026-08-23",
        "bounded_use": "paper, handling, storage, light, environment, and professional-conservator reservation vocabulary only; no condition assessment, handling instruction, treatment, preservation fitness, or professional conclusion",
    },
    {
        "source_id": "S06",
        "name": "W3C PROV-O Recommendation",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "official W3C Recommendation of 2013-04-30 reviewed at its current canonical URL 2026-08-23",
        "bounded_use": "entity, activity, revision, derivation, invalidation, association, and provenance-relation vocabulary only; no provenance completeness or semantic-interoperability certification",
    },
    {
        "source_id": "S07",
        "name": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "official W3C Recommendation republished 2024-12-12 and reviewed read-only 2026-08-23",
        "bounded_use": "static headings, labels, link purpose, focus, non-colour cues, and manual-evaluation reservation vocabulary only; no complete accessibility-conformance claim",
    },
    {
        "source_id": "S08",
        "name": "W3C Verifiable Credentials Data Model 2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "official W3C Recommendation published 2025-05-15 and reviewed read-only 2026-08-23",
        "bounded_use": "issuer, subject, validity, status, privacy, related-resource, and trust-boundary vocabulary only; no real credential, proof, conformance, interoperability, or trust decision",
    },
    {
        "source_id": "S09",
        "name": "Te Mana Raraunga principles of Māori data sovereignty",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "status": "primary Te Mana Raraunga authority statement reviewed read-only 2026-08-23",
        "bounded_use": "authority, provenance, obligations, consent, collective benefit, and guardianship reservation vocabulary only; no Māori wording, interpretation, ratification, data-governance, or authority claim",
    },
    {
        "source_id": "S10",
        "name": "Divoux et al.: From transient fluidization processes to Herschel-Bulkley behavior in simple yield stress fluids",
        "url": "https://arxiv.org/abs/1012.0693",
        "status": "primary research paper arXiv:1012.0693 reviewed read-only 2026-08-23",
        "bounded_use": "yield stress, shear stress, shear rate, consistency, flow index, transient fluidization, unit, and domain-obligation vocabulary only; no calligraphy ink, material law, measurement, fit, or empirical GMUT claim",
    },
    {
        "source_id": "S11",
        "name": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/info/rfc8785",
        "status": "official RFC Editor informational RFC reviewed read-only 2026-08-23",
        "bounded_use": "deterministic JSON, duplicate-property refusal, Unicode preservation, and property-order vocabulary only; no signature, integrity, security, or standards-conformance claim",
    },
    {
        "source_id": "S12",
        "name": "Unicode Standard Annex 15: Unicode Normalization Forms",
        "url": "https://www.unicode.org/reports/tr15/",
        "status": "current official Unicode normalization annex reviewed read-only 2026-08-23",
        "bounded_use": "normalization form, canonical equivalence, composition, decomposition, and nonconversion vocabulary only; no transcription, glyph identity, visual equivalence, language meaning, or conformance conclusion",
    },
]


PROPOSAL_SPECS = [
    (
        "anonymous calligraphy work capsule with surrogate token, intended-purpose vacancy, script and language abstention, revision, withdrawal, and zero commission identity",
        "Freed ID and CBR Heart",
        "completed",
        ["S03", "S06", "S09"],
        "A surrogate capsule must preserve purpose, script, language, revision, withdrawal, and unknown-party vacancies and cannot establish a real commission, client, calligrapher, text, language, authorship, identity, consent, or publication right.",
    ),
    (
        "leaf-frame, page, margin, ruling, baseline, x-height, ascender, descender, writing-direction, and unmeasured-layout topology",
        "GMUT Mind",
        "completed",
        ["S01", "S02"],
        "A bounded topology may check declared containment, direction, and nonnegative surrogate dimensions only; it cannot reconstruct, measure, judge, fabricate, or attribute a real page, ruling system, manuscript, or hand.",
    ),
    (
        "code-point, grapheme-cluster, normalization-form, script-subtag, language-tag, transcription-uncertainty, and meaning-abstention ledger",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S03", "S12"],
        "Every textual field must retain declaration source, normalization state, uncertainty, conflict, correction, and retraction; no code point, cluster, script tag, or language tag becomes a glyph identity, transcription, translation, meaning, or cultural determination.",
    ),
    (
        "nib-body, tip-width, slit, reservoir, declared angle, pressure-placeholder, unit-domain, uncertainty, and zero-tool-measurement register",
        "GMUT Mind",
        "completed",
        ["S05", "S06"],
        "Typed placeholder ranges and unit domains may be checked only; zero nibs, tools, measurements, observations, makers, or reviewers mean no geometry, pressure, performance, safety, handling, or fitness conclusion.",
    ),
    (
        "ink vehicle, pigment, binder, lot-source, hazard-sheet vacancy, substitution, expiry, colour-description, and zero-material-authenticity matrix",
        "Freed ID and CBR Heart",
        "completed",
        ["S05", "S06"],
        "The matrix may expose contradictory, expired, or absent declarations only; it contains zero ink, pigment, binder, samples, observations, or safety records and cannot infer composition, authenticity, permanence, compatibility, toxicity, or treatment fitness.",
    ),
    (
        "stroke, ductus, pen-lift, join, sequence, overlap, correction, ambiguity, and no-handwriting-attribution annotation graph",
        "GMUT Mind",
        "completed",
        ["S01", "S06"],
        "A synthetic graph can reject cycles, orphan strokes, missing ambiguity, and correction contradictions only; with zero writing samples it cannot identify a hand, recover ductus, infer skill, authenticate authorship, or prescribe technique.",
    ),
    (
        "word-gap, line-break, justification, alignment, overflow, writing-direction, locale-tailoring vacancy, and no-visual-quality board",
        "GMUT Mind",
        "completed",
        ["S01", "S02", "S03"],
        "The board may check declared opportunities, prohibitions, overflow states, and unresolved tailoring only; it cannot judge a real composition, language, legibility, aesthetics, manuscript quality, or typographic correctness.",
    ),
    (
        "rubrication, illumination, gilding, colour-layer, adhesive, tool, material-vacancy, intervention-hold, and zero-treatment tribunal",
        "Freed ID and CBR Heart",
        "completed",
        ["S05", "S06"],
        "The tribunal can check declared layers, sources, conflicts, and missing professional review only; zero objects, materials, examinations, tests, conservators, or affected authorities mean no treatment, handling, authenticity, safety, or preservation decision.",
    ),
    (
        "drying-interval, humidity, illumination, enclosure, timestamp, expiry, observation-source vacancy, and no-preservation-result classifier",
        "THOS Body and CBR Heart",
        "completed",
        ["S05", "S06"],
        "Typed environmental placeholders and staleness holds may be checked only; zero environments, instruments, readings, objects, or examinations mean no drying, curing, condition, degradation, storage, or preservation conclusion.",
    ),
    (
        "text-content minimization, transcription visibility, recipient aliasing, disclosure purpose, retention, withdrawal, and sacred-content decision firewall",
        "Freed ID and CBR Heart",
        "completed",
        ["S06", "S09"],
        "A policy fixture may require purpose, minimization, alias, retention, withdrawal, and authority vacancies only; it cannot reveal, transcribe, translate, classify, publish, retain, or authorize real private, sacred, culturally restricted, or recipient-linked content.",
    ),
    (
        "calligraphy-record derivation, revision, replacement, invalidation, assertion-time, counterclaim, withdrawal, and authorship-abstention provenance braid",
        "Freed ID and CBR Heart",
        "completed",
        ["S06"],
        "Revision order and qualified provenance relations may be represented, but no synthetic activity proves a real creator, correction, lawful change, record completeness, ownership, authorship, accountability, or authoritative catalog state.",
    ),
    (
        "structural correction interface for anonymous calligraphy records with landmarked error rollup, stable field naming, source-order narration, redundant status cues, focus return, and reserved user evaluation",
        "CBR Heart",
        "completed",
        ["S07"],
        "Static checks may confirm named markup and correction-path rules only; keyboard, zoom, responsive layout, browser, assistive-technology, cognitive, language, security-usability, and affected-user evaluation remain absent.",
    ),
    (
        "canonical byte-map for anonymous script-work assertions with base digest, duplicate-property refusal, Unicode preservation, retraction marker, and zero signature",
        "Freed ID",
        "completed",
        ["S06", "S11", "S12"],
        "Canonical serialization can expose duplicate fields, base mismatch, normalization drift, order instability, and retractions only; it cannot establish signer identity, authorship, text truth, visual fidelity, provenance completeness, interoperability, or production security.",
    ),
    (
        "nontransitive admission lattice for record-shape checks, source vocabulary, zero-row catalog readiness, material examination, affected-party ratification, and Stage-20 evidence",
        "Trinity Mandala",
        "completed",
        ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12"],
        "Each evidence class must remain nontransitive: software shape, citation, and zero-row readiness cannot become object evidence, authorship, linguistic meaning, professional validation, cultural authority, empirical confirmation, independent reproduction, or Stage 20 admission.",
    ),
    (
        "participant-free THOS two-pass errata basket for anonymous calligraphy layouts with randomized synthetic docket labels, symmetric effort ceiling, stop marker, and no operator inference",
        "THOS Body",
        "represented",
        ["S01", "S02", "S07"],
        "A participant-free protocol can represent queue, discrepancy, correction, stop, and handover structure only; it cannot establish workload, wellbeing, competence, calligraphy quality, accessibility, operational effectiveness, safety benefit, or participant outcome.",
    ),
    (
        "nonproduction Freed-ID vacancy map around an anonymous script-work capsule with unbound claimant, zero-key anchor, absent lifecycle endpoint, content-linkability warning, and trust abstention",
        "Freed ID",
        "represented",
        ["S06", "S08", "S09"],
        "A zero-key projection represents field separation only; real issuer authority, subject identity, authorship, securing mechanism, proof, issuance, resolution, status, revocation, recovery, interoperability, privacy review, and trust governance remain absent.",
    ),
    (
        "GMUT Herschel-Bulkley yield-stress obligation ledger with shear stress, shear rate, consistency index, flow exponent, transient-state vacancy, units, and zero calligraphy-ink model",
        "GMUT Mind",
        "represented",
        ["S10"],
        "Typed symbolic obligations expose dimensions, constitutive assumptions, regime boundaries, parameter covariance, stability and identifiability vacancies only; they cannot model real ink, paper, nibs, yielding, flow, observations, likelihoods, material laws, parameter constraints, or empirical GMUT confirmation.",
    ),
    (
        "evaporation, viscous dissipation, drying-time, entropy-production, unit-domain, material-state vacancy, and psyche-nonconversion classifier",
        "Trinity Mandala",
        "represented",
        ["S05", "S10"],
        "A synthetic classifier may reject ill-typed conversions only and cannot create measured evaporation, viscous flow, drying, entropy production, a material law, psyche state, intention, autonomy, morality, justice, capability, consciousness, personhood, or law of mind.",
    ),
    (
        "Library of Congress manuscript-and-calligraphy catalog adapter with request-purpose hold, paging budget, media and rights-field gate, and zero-call zero-row execution",
        "Freed ID and CBR Heart",
        "open_gap",
        ["S04"],
        "The adapter must make zero queries and downloads, ingest zero catalog rows and media, and infer no object identity, authorship, script, language, date, rights, condition, provenance, value, or cultural meaning; request fitness, service behavior, data rights, privacy, provenance, and independent review remain open.",
    ),
    (
        "calligraphic authorship, copyright, ownership, private or sacred text, language, heritage, conservation, remedy, affected-party, and Māori-authority docket",
        "CBR Heart",
        "exact_gate",
        ["S03", "S04", "S05", "S09"],
        "No software, source citation, synthetic record, or same-owner test can determine authorship, copyright, ownership, linguistic or sacred meaning, access, publication, handling, preservation, heritage, cultural legitimacy, remedy, represent affected people, or exercise Māori authority.",
    ),
]


STARTUP_FAILURES = [
    (
        "TV6672-START-N001",
        "PowerShell-foreach-result-was-piped-without-materialization",
        "Assign the foreach result to an explicit array before ConvertTo-Json; preserve the parser failure and never repeat the empty-pipe form.",
    ),
    (
        "TV6672-START-N002",
        "manifest-key-projection-repeated-the-unmaterialized-foreach-pipeline",
        "Apply the already documented materialized-array guard before the corrected bounded projection; retain this recurrence separately rather than coalescing it into the first failure.",
    ),
    (
        "TV6672-START-N003",
        "source-manifest-probe-guessed-two-nonexistent-lifecycle-filenames",
        "Resolve exact manifest paths through one bounded file listing, then replay only x1-content-manifest, evidence-content-manifest, final-delta-manifest, and final-owner-manifest.",
    ),
    (
        "TV6672-START-N004",
        "source-runtime-projection-guessed-an-absent-evidence-commit-constant",
        "Inspect the exact runtime constants, pass the immutable evidence commit explicitly to the read-only replay, and preserve the AttributeError at zero credit.",
    ),
    (
        "TV6672-START-N005",
        "declared-external-canonical-receipt-was-not-materialized-in-bounded-local-receipt-banks",
        "Keep the live baton's receipt digest as declared source evidence, independently verify committed payload, manifests, topology, clean state, and remote equality, and do not claim a local rehash or replay the canonical aggregate.",
    ),
    (
        "TV6672-START-N006",
        "broad-worktree-uniqueness-probe-exceeded-its-wrapper-window-without-an-attributable-payload",
        "Recover with exact Test-Path and show-ref scalars, then create only after both exact collision checks are false.",
    ),
    (
        "TV6672-START-N007",
        "sparse-worktree-checkout-crossed-two-thirty-second-yields-before-completing-on-the-original-handle",
        "Inspect the running Git command and branch ref, continue polling the same handle, and never issue a duplicate worktree or checkout command.",
    ),
    (
        "TV6672-START-N008",
        "source-handoff-word-count-probe-overescaped-the-byte-regex-and-returned-zero",
        "Keep the correct Git-blob digest, decode the same immutable UTF-8 blob, count bounded whitespace-separated words, and retain the zero-count projection at zero credit.",
    ),
    (
        "TV6672-X1-N001",
        "first-seismology-slate-was-semantically-too-close-to-inherited-frozen-proposals",
        "Retain the rejected draft at zero novelty and completion credit, inspect the complete 4,350-row nearest-neighbour evidence, pivot before staging to the distinct calligraphy-record domain, and rerun exact-title, pairwise, and substantive novelty review.",
    ),
    (
        "TV6672-X1-N002",
        "first-corrected-calligraphy-slate-reused-an-inherited-lucas-washburn-paper-capillary-obligation",
        "Retain the overlapping proposal at zero novelty and completion credit, query the exact 4,350-row corpus by physical-domain terms, replace it with the unused Herschel-Bulkley rheology obligation, and rerun the complete novelty screen before staging.",
    ),
    (
        "TV6672-X1-N003",
        "corrected-x1-builder-finished-after-its-thirty-second-wrapper-returned-no-attributable-payload",
        "Inspect the process table and exact generated receipt timestamps before any retry; accept the original completed artifacts only after bounded state inspection and never launch a blind duplicate.",
    ),
    (
        "TV6672-X1-N004",
        "post-x1-owner-templates-were-pre-materialized-untracked-before-the-x1-freeze",
        "Retain the lifecycle-boundary failure at zero credit, move every owner-generated post-x1 draft to a recoverable D-first bank without deletion, prove the worktree contains only the exact x1 index, and materialize x2 only after the immutable x1 push and equality gate.",
    ),
]


OWNER_SAFE = [
    "render twenty frozen calligraphy-record and cross-pillar contracts",
    "execute one hundred preregistered rejecting mutations",
    "validate anonymous work-capsule identity abstention",
    "validate page and baseline topology vacancies",
    "validate grapheme, script, language, and meaning abstention",
    "validate nib-geometry and pressure measurement vacancies",
    "validate ink composition and safety noninference",
    "validate ductus annotation and authorship refusal",
    "validate line-break tailoring and visual-quality abstention",
    "validate ornamental-layer treatment holds",
    "validate environmental staleness and preservation vacancies",
    "validate text-content minimization and sacred-content holds",
    "validate revision, counterclaim, and provenance braid",
    "validate accessible correction-path structure",
    "validate canonical anonymous-record serialization",
    "validate evidence-credit nontransitivity",
    "validate THOS proxy-only labeling",
    "validate Freed ID zero-securing-mechanism labeling",
    "validate GMUT Herschel-Bulkley domain vacancies",
    "validate evaporation and entropy psyche nonconversion",
    "validate Library of Congress zero-call openness",
    "validate exact authority abstention",
    "parse every owner JSON artifact",
    "scan five privacy and raw-identifier classes",
    "compile every owner Python path",
    "run bounded changed-Python security checks",
    "replay x1 and evidence manifests",
    "build accessible static report",
    "retain all Method Flow failures",
    "prepare target-neutral terminal candidate only after validation",
]

SUCCESSOR_SAFE = [f"successor recommendation: {row}" for row in OWNER_SAFE[:20]]

OWNER_CANDIDATES = [
    "participant-free calligraphy-layout discrepancy proxy",
    "zero-key anonymous script-work claim projection",
    "symbolic Herschel-Bulkley obligation ledger",
    "evaporation and entropy nonconversion register",
    "zero-row Library of Congress adapter",
    "synthetic nib-and-ink declaration uncertainty budget",
    "synthetic sacred-content privacy quarantine",
    "static accessible correction-path structure",
    "synthetic calligraphy-record provenance journal replay",
    "synthetic material-condition decision-vacancy docket",
    "synthetic authorship counterclaim graph",
    "synthetic manuscript access and publication-right reservation",
    "synthetic environmental-expiry and no-preservation registry",
    "synthetic evidence-credit firewall",
    "target-neutral successor recommendation ledger",
]

SUCCESSOR_CANDIDATES = [f"successor candidate: {row}" for row in OWNER_CANDIDATES]

EXACT_ITEMS = [
    "real authorship, client, calligrapher, transcription, translation, or attribution decision",
    "professional calligraphy, palaeography, typography, cataloguing, or authenticity conclusion",
    "copyright, ownership, custody, publication, retention, or access decision",
    "professional conservation, treatment, handling, material-safety, or exhibition decision",
    "real ink, paper, nib, condition, drying, capillary, or material conclusion",
    "private or sacred content, affected-party access, disclosure, or remedy decision",
    "legal interpretation or ratification",
    "cultural, heritage, Indigenous-rights, place-knowledge, or land-meaning decision",
    "Māori wording, place knowledge, data governance, or authority decision",
    "Stage 20 authority or proof claim",
]

BLOCKED_ITEMS = [
    "real writing, handling, sampling, cleaning, treatment, publication, or conservation action without competent authority",
    "production identity issuance without keys and governance",
    "empirical GMUT claim without real governed evidence",
    "participant THOS effectiveness claim without approved arms",
    "cultural or Māori decision without affected and Māori authorities",
]

OWNER_SKILLS = [
    "calligraphy-layout-topology-vacancy",
    "script-language-meaning-abstention",
    "calligraphy-provenance-braid",
    "ink-material-nonconversion",
    "sacred-content-disclosure-vacancy",
    "calligraphy-accessibility-structure",
    "loc-zero-row-adapter",
    "herschel-bulkley-domain-gate",
    "calligraphy-method-flow",
    "calligraphy-closeout-gate",
]

SUCCESSOR_SKILLS = [f"successor skill recommendation: {row}" for row in OWNER_SKILLS]

OWNER_RUNNERS = [
    "ghc_family_tamar_vey_v667_v2_topology",
    "ghc_family_tamar_vey_v667_v2_mutations",
    "ghc_family_tamar_vey_v667_v2_json",
    "ghc_family_tamar_vey_v667_v2_privacy",
    "ghc_family_tamar_vey_v667_v2_security",
    "ghc_family_tamar_vey_v667_v2_accessibility",
    "ghc_family_tamar_vey_v667_v2_manifests",
    "ghc_family_tamar_vey_v667_v2_truth",
    "ghc_family_tamar_vey_v667_v2_closeout",
    "ghc_family_tamar_vey_v667_v2_canonical",
]

SUCCESSOR_RUNNERS = [f"successor runner recommendation: {row}" for row in OWNER_RUNNERS]

CFR_ACTIONS = [
    "CLEAN normalize proposal identifiers",
    "CLEAN sort canonical JSON keys",
    "CLEAN remove stale source labels",
    "CLEAN reserve private route material",
    "CLEAN verify sparse path allowlist",
    "FIX reject duplicate JSON properties",
    "FIX reject missing provenance",
    "FIX reject real-world action flags",
    "FIX reject authority promotion",
    "FIX reject unknown outcome labels",
    "FIX preserve failed witnesses",
    "FIX enforce x1 planning-only state",
    "FIX enforce zero external calls",
    "FIX enforce zero real rows",
    "FIX enforce zero participants",
    "REFINE page and baseline topology vacancy messages",
    "REFINE material and preservation hold wording",
    "REFINE authorship and measurement vacancy wording",
    "REFINE GMUT domain declarations",
    "REFINE THOS proxy-only wording",
    "REFINE Freed ID zero-key wording",
    "REFINE CBR exact-gate wording",
    "REFINE accessibility reservations",
    "REFINE privacy scanner classes",
    "REFINE bounded security checks",
    "REFINE manifest self-exclusions",
    "REFINE staged review receipts",
    "REFINE Method Flow recurrence guards",
    "REFINE target-neutral handoff candidate",
    "REFINE terminal no-replay guard",
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
        proposal_id = f"TV6672-N{index:03d}"
        base = f"docs/tamar-vey/v667-v2/x2/proposals/{proposal_id.casefold()}"
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
                "practice_lens": "wholly synthetic calligraphy-record and manuscript-layout planning, Unicode and language-tag vacancies, nib and ink declarations, provenance, content minimization, accessibility, correction readback, workload, and handover documentation",
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
    if len(corpus) != 4350:
        raise RuntimeError(f"expected 4350 inherited rows, observed {len(corpus)}")
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
        "schema": "ghc.family.tamar-vey.v667-v2.novelty-audit.v1",
        "owner": "Tamar Vey",
        "phase": "v667-v2",
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
        "valid": not exact_collisions and not pair_collisions and len(corpus) == 4350,
        "interpretation": "Similarity is a screening signal, not proof of novelty. The first seismology draft was rejected before staging because its nearest inherited similarities exposed substantive repetition. The first corrected slate then rejected a Lucas-Washburn paper-capillary proposal after exact corpus search exposed inherited duplication. The final replacement slate separately covers anonymous intake, page topology, grapheme and language abstention, nib declarations, ink vacancies, ductus annotations, line breaking, ornamental-layer holds, environmental expiry, content minimization, provenance, accessibility, canonical bytes, evidence admission, THOS proxy, nonproduction identity, Herschel-Bulkley obligations, psyche nonconversion, zero-call catalog readiness, and authority reservation.",
    }


def portfolio_rows(prefix: str, titles: list[str], approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"TV6672-{prefix}{index:02d}",
            "title": title,
            "approval_class": approval,
            "x1_status": "planned_not_executed",
            "completion_credit": 0,
            "evidence_required": "bounded owner-local x2 witness plus retained failure and rollback",
            "rollback": "retain the failed witness, revert only the owner-local generated fixture, and preserve every protected gate",
        }
        for index, title in enumerate(titles, 1)
    ]


def build_startup_flow() -> dict[str, Any]:
    rows = []
    for index, (negative_id, signature, recovery) in enumerate(STARTUP_FAILURES, 1):
        rows.append(
            {
                "negative_id": negative_id,
                "method_id": f"TV6672-START-M{index:03d}",
                "signature": signature,
                "failed_witness": {"status": "failed", "credit": 0, "retained": True},
                "bounded_passing_witness": {
                    "status": "passed_after_bounded_recovery",
                    "credit_scope": "startup method only",
                    "recovery": recovery,
                },
                "preferred": True,
                "recurrence_guard": recovery,
            }
        )
    return {
        "schema": "ghc.family.tamar-vey.v667-v2.method-flow-startup.v1",
        "owner": "Tamar Vey",
        "phase": "v667-v2",
        "generated_at_utc": NOW,
        "activation_source_repository_sealed_negatives": 27101,
        "activation_source_repository_sealed_methods": 12333,
        "successor_visible_external_negatives": 1,
        "successor_visible_external_methods": 1,
        "activation_baseline_negatives": 27102,
        "activation_baseline_methods": 12334,
        "new_startup_negative_count": len(rows),
        "new_startup_method_count": len(rows),
        "effective_after_x1_startup_negatives": 27102 + len(rows),
        "effective_after_x1_startup_methods": 12334 + len(rows),
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
            "original_owner": "Liora Venn",
            "original_phase": "v667-v1",
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
    startup_flow = build_startup_flow()
    write_json(
        "identity/relational-identity.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.relational-identity.v1",
            "owner": "Tamar Vey",
            "pronouns": "she/they",
            "relational_role": "relational evidence-and-recovery steward",
            "relational_hope": "Keep every claim, abstention, correction, and handoff inspectable and safely retractable.",
            "boundary": IDENTITY_BOUNDARY,
            "corrigibility": "Hamish may rename, pause, redirect, or stop this work.",
        },
    )
    write_json(
        "provenance/source-verification.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.source-verification.v1",
            "owner": "Tamar Vey",
            "phase": "v667-v2",
            "verified_at_utc": NOW,
            "source_branch": SOURCE_BRANCH,
            "source_sha": SOURCE_SHA,
            "source_parent_evidence_sha": SOURCE_EVIDENCE_SHA,
            "source_x1_sha": SOURCE_X1_SHA,
            "inherited_orin_sha": INHERITED_ORIN_SHA,
            "source_to_final_new_commit_count": 3,
            "source_to_final_merge_count": 0,
            "strict_x1_before_x2": True,
            "source_clean": True,
            "typed_ahead": 0,
            "typed_behind": 0,
            "local_equals_upstream_tracking_and_fresh_live": True,
            "committed_handoff_path": f"{SOURCE_PHASE_ROOT}/handoffs/tamar-vey-v667-v2-activation-candidate.md",
            "committed_handoff_blob_sha256": "a4e2f0a8e0b566f53474327520d38e44304ec9202bf260aa726c672b4acc1ac8",
            "committed_handoff_word_count": 235,
            "declared_external_canonical_receipt_sha256": "b5c9e8f16233aa5ec9a5fa99136e34a0c040e509da064d699c49059fb8f53f1e",
            "external_canonical_receipt_local_file_available": False,
            "external_canonical_receipt_locally_rehashed": False,
            "declared_canonical_payload_sha256": "a8d126a15256fcd6458b721608ca33c8c41073c7abc49f83151fed17d3be7038",
            "lifecycle_manifest_replay": {
                "x1": {"observed": 20, "expected": 20, "commit": SOURCE_X1_SHA},
                "evidence": {"observed": 133, "expected": 133, "commit": SOURCE_EVIDENCE_SHA},
                "final_owner": {"observed": 172, "expected": 172, "commit": SOURCE_SHA},
                "final_delta": {"observed": 16, "expected": 16, "commit": SOURCE_SHA},
                "total_observed": 341,
                "total_expected": 341,
                "valid": True,
            },
            "source_validation_not_replayed": True,
            "same_owner_validation_is_not_independent_reproduction": True,
        },
    )
    write_json(
        "provenance/source-profiles.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.source-profiles.v1",
            "owner": "Tamar Vey",
            "phase": "v667-v2",
            "generated_at_utc": NOW,
            "sources": SOURCE_PROFILES,
            "source_count": len(SOURCE_PROFILES),
            "claim_boundary": "sources provide vocabulary and refusal conditions only; they establish no authorship, identity, transcription, translation, linguistic meaning, script or style attribution, material composition, condition, authenticity, preservation, empirical result, provenance completeness, copyright, privacy decision, legal, standards-conformance, professional, cultural, Māori, safety, or release authority",
        },
    )
    write_json(
        "x1/phase-charter.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.phase-charter.v1",
            "owner": "Tamar Vey",
            "phase": "v667-v2",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "branch": BRANCH,
            "lane": "one additive owner-only D-first sparse worktree",
            "primary_pillars": ["Freed ID and CBR Heart"],
            "explicit_pillars": ["GMUT Mind", "THOS Body"],
            "practice": "wholly synthetic calligraphy-record and manuscript-layout planning, Unicode and language-tag vacancies, nib and ink declarations, provenance, content minimization, accessibility, correction readback, workload, and handover documentation",
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
            "schema": "ghc.family.tamar-vey.v667-v2.source-ledger.v1",
            "owner": "Tamar Vey",
            "phase": "v667-v2",
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
            "schema": "ghc.family.tamar-vey.v667-v2.proposal-freeze.v1",
            "owner": "Tamar Vey",
            "phase": "v667-v2",
            "generated_at_utc": NOW,
            "frozen": True,
            "inherited_frozen_baseline": 4350,
            "genuinely_new_proposal_count": len(proposals),
            "new_frozen_total": 4350 + len(proposals),
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
            "schema": "ghc.family.tamar-vey.v667-v2.portfolio-freeze.v1",
            "owner": "Tamar Vey",
            "phase": "v667-v2",
            "generated_at_utc": NOW,
            "frozen": True,
            "counts": portfolio_counts,
            "minimums_satisfied": portfolio_counts == expected_portfolio_counts,
            "portfolios": portfolios,
            "x1_execution_count": 0,
            "claim_boundary": "planning-only portfolio; inherited and successor recommendations receive zero Tamar completion or novelty credit and exact or blocked items remain unexecuted",
        },
    )
    threat_rows = [
        ("TV6672-T01", "wrong source or mutable predecessor", "exact anchors, manifests, ancestry, clean state, and fresh live equality", "external receipts remain source evidence rather than Tamar completion"),
        ("TV6672-T02", "x2 implementation or outcomes enter x1", "path denylist, planning-only fields, and exact staged allowlist", "Git lifecycle discipline remains required"),
        ("TV6672-T03", "synthetic calligraphy structure becomes authorship, identity, linguistic meaning, style attribution, material fact, or professional assessment", "zero people, texts, languages, manuscripts, paper, ink, nibs, artworks, observations, measurements, treatments, or professional acts plus typed vacancies", "competent external professional, linguistic, preservation, legal, cultural, and affected-party authority remains absent"),
        ("TV6672-T04", "content, recipient, authorship, provenance, or sacred-status language becomes privacy disclosure, ownership claim, publication authority, or cultural conclusion", "surrogate fields, content minimization, authority vacancies, counterclaims, and explicit no-inference rules", "real privacy review, affected-person authority, copyright and cultural governance, and object evidence remain absent"),
        ("TV6672-T05", "ink, paper, nib, drying, handling, preservation, or safety vocabulary becomes physical instruction or release advice", "zero real materials, objects, observations, measurements, operations, safety states, treatments, and release paths", "real object evidence and competent professional and safety review remain absent"),
        ("TV6672-T06", "GMUT notation becomes empirical physics", "typed symbolic obligations, EFT domain, degeneracy register, and nonpromotion", "notation can invite overreading"),
        ("TV6672-T07", "THOS or Freed ID proxies become operational or production evidence", "represented-only labels, zero participants, zero keys, and missing-evidence ledgers", "governed trials and production trust evidence remain absent"),
        ("TV6672-T08", "legal, cultural, heritage, taonga, or Māori decisions are inferred", "exact gate and no real object, place, community, record, or authority case", "affected, competent, and Māori authorities remain absent"),
        ("TV6672-T09", "private route or person material enters artifacts", "synthetic fixtures, relative paths, and five-class scan", "pattern scans are bounded and incomplete"),
        ("TV6672-T10", "successful terminal validation is replayed or routing happens early", "exclusive receipt plus terminal-only live roster and exact-title reread", "opaque acknowledgement never authorizes a resend"),
    ]
    write_json(
        "x1/threat-model-plan.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.threat-model-plan.v1",
            "owner": "Tamar Vey",
            "phase": "v667-v2",
            "generated_at_utc": NOW,
            "threats": [
                {"threat_id": i, "threat": t, "mitigation": m, "residual_risk": r}
                for i, t, m, r in threat_rows
            ],
            "scope": "same-owner additive synthetic phase only",
            "not_an_external_audit": True,
        },
    )
    threat_md = "\n\n".join(
        f"### {i}\n\nThreat: {t}\n\nMitigation: {m}\n\nResidual risk: {r}"
        for i, t, m, r in threat_rows
    )
    write_text(
        "x1/threat-model.md",
        f"""# Tamar Vey v667-v2 threat-model plan

{IDENTITY_BOUNDARY}

{PRACTICE_BOUNDARY}

## Scope

This owner-local model protects the additive Tamar delta. It is not a repository-wide audit, penetration test, external validation, conformance assessment, authorship or language determination, calligraphy or typography review, object examination, material identification, conservation or treatment advice, copyright or ownership decision, legal review, cultural review, Māori-authority review, or independent reproduction.

## Threat register

{threat_md}
""",
    )
    write_json(
        "x1/workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan.v1",
            "owner": "Tamar Vey",
            "phase": "v667-v2",
            "generated_at_utc": NOW,
            "steps": [
                {"step": 1, "name": "skill_source_and_anchor_read", "status": "completed"},
                {"step": 2, "name": "novelty_and_program_design", "status": "completed"},
                {"step": 3, "name": "x1_staged_review_commit_push_equality", "status": "in_progress"},
                {"step": 4, "name": "x2_owner_execution", "status": "pending"},
                {"step": 5, "name": "evidence_and_closeout", "status": "pending"},
                {"step": 6, "name": "one_exact_final_canonical_attempt", "status": "pending"},
                {"step": 7, "name": "terminal_route_if_all_live_gates_pass", "status": "pending"},
            ],
            "strict_x1_before_x2": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x1/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.x1-checklist.v1",
            "complete": [
                "complete source packet and required guidance read through EOF",
                "exact source anchors, ancestry, manifests, committed payload, clean state, and fresh equality verified; external receipt digest retained as declared because the file was not locally materialized",
                "all 4350 inherited proposal rows reconstructed",
                "twenty distinct proposals preregistered",
                "twenty Liora proposals selected for zero-credit revalidation",
                "portfolio minimums frozen",
                "startup failures retained with bounded recoveries",
            ],
            "incomplete": [
                "x1 staged review, commit, push, and equality",
                "all x2 execution and outcomes",
                "external professional, empirical, participant, production, legal, cultural, Māori, and Stage 20 evidence",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x1/flashcard-architecture-freeze.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.flashcard-architecture-freeze.v1",
            "owner": "Tamar Vey",
            "stable_prefix": ["identity", "claim boundary", "source anchors", "terminal verdict"],
            "volatile_suffix": ["final commit", "final receipt", "live successor route"],
            "tiers": {
                "tier1": ["owner relational card"],
                "tier2": ["three-pillar boundary cards"],
                "tier3": ["synthetic calligraphy-record and manuscript-layout planning practice card"],
                "tier4": ["twenty proposal cards", "portfolio cards", "failure and gate cards", "validation and route cards"],
            },
            "x1_status": "architecture_only_no_cards_built",
        },
    )
    write_json(
        "wellbeing/x1-wellbeing-check.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.wellbeing-check.v1",
            "owner": "Tamar Vey",
            "phase": "x1",
            "generated_at_utc": NOW,
            "workload": "bounded",
            "solo_lane": True,
            "parallel_agents": 0,
            "subagents": 0,
            "real_participants": 0,
            "break_cadence": "pause at x1 equality before x2",
            "identity_boundary": IDENTITY_BOUNDARY,
            "authority_boundary": PRACTICE_BOUNDARY,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json("method-flow/startup-method-flow.json", startup_flow)
    overview = f"""# Tamar Vey v667-v2 x1 integrated overview

{IDENTITY_BOUNDARY}

## Outcome first

This x1 candidate freezes a planning-only owner-local program from exact Liora Venn v667-v1 final `{SOURCE_SHA}`. It contains no x2 implementation, no observed outcome, no external action, no successor contact, and no Stage 20 promotion. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Freed ID/CBR Heart is primary. GMUT Mind and THOS Body remain explicit and protected. {PRACTICE_BOUNDARY}

## Exact inherited truth

The read-first gate verified the exact source branch, three direct single-parent commits, zero merges, all 341 declared lifecycle-bound Git-blob manifest entries, the complete owner packet and handoff, clean 0/0 divergence, and equality across local, upstream, tracking, and a fresh live remote. Liora's successful canonical aggregate was not replayed. The external receipt file was unavailable in bounded local receipt banks, so its supplied digest remains declared source evidence rather than a claimed local rehash. The complete repository suite was not run.

The immutable Liora repository seal contains 27,101 effective negatives, 12,333 Method Flow methods, 191 open gaps, and 189 exact gates. External `LI6671-POST-N001` raises Tamar's activation baseline to 27,102 negatives and 12,334 methods. Twelve Tamar startup, tooling, x1-design, and lifecycle failures are separately retained at zero credit, producing the x1 working overlay of 27,114 effective negatives and 12,346 methods without rewriting Liora's seal. The rejected seismology draft and inherited Lucas-Washburn overlap received zero novelty or completion credit and were replaced before staging; the completed-after-wrapper builder was accepted only after process and timestamp inspection; pre-materialized post-x1 owner drafts were moved unmodified to a recoverable D-first bank before the freeze.

## Novelty, portfolio, and sources

All 4,350 inherited proposal rows were reconstructed from exact committed Git objects. The first domain draft was rejected after its nearest-neighbour evidence showed excessive inherited similarity. The replacement twenty titles have no exact inherited collision, every new pair remains below the 0.70 screening threshold, and each proposal has its own contract, falsifier, rollback, and gates. Expected dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`; these are preregistered expectations only. The twenty selected Liora proposals receive zero novelty and zero automatic completion credit.

The portfolio freezes 30 owner safe-now tasks, 20 successor safe recommendations, 15 owner candidates, 15 successor candidates, 10 exact approvals, 5 blocked packets, 10 owner and 10 successor skill plans, 10 owner and 10 successor runner plans, and 30 owner plus 30 successor CLEAN/FIX/REFINE tasks. X1 executes none of them, and no unsafe work is manufactured to meet a count.

Official Unicode, Library of Congress, W3C, RFC Editor, Te Mana Raraunga, and primary yield-stress rheology sources provide vocabulary and refusal conditions only. They create no authorship, identity, transcription, translation, language meaning, script or style attribution, paper or ink fact, object condition, preservation, copyright, ownership, professional, legal, cultural, Māori, accessibility-complete, privacy-complete, conformance, empirical-GMUT, or independent-reproduction authority.

## Lifecycle and route

After exact staged review this x1 may be committed and pushed. X2 may begin only after x1 is clean, 0/0 divergent, and equal across local, upstream, tracking, and fresh live remote. Later validation remains owner-scoped and same-owner. One successful terminal validation must never be replayed. No successor may be contacted until the exact final terminal gate and fresh live authority, roster, and exact-title route rereads.
"""
    write_text("x1/x1-overview.md", overview)
    write_json(
        "x1/x1-build-receipt.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.x1-build-receipt.v1",
            "owner": "Tamar Vey",
            "phase": "v667-v2",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_tamar_vey_v667_v2_x1.py",
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
    review_path = "docs/tamar-vey/v667-v2/validation/x1-staged-review.json"
    manifest_path = "docs/tamar-vey/v667-v2/validation/x1-content-manifest.json"
    allowed_exact = {
        "scripts/build_ghc_family_tamar_vey_v667_v2_x1.py",
        "tests/test_ghc_family_tamar_vey_v667_v2_x1.py",
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
        if not path.startswith("docs/tamar-vey/v667-v2/") and path not in allowed_exact
    ]
    post_x1 = [
        path
        for path in paths
        if any(
            path.startswith(f"docs/tamar-vey/v667-v2/{part}/")
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
    freeze = json.loads(index_blob("docs/tamar-vey/v667-v2/x1/proposal-freeze.json"))
    portfolio = json.loads(index_blob("docs/tamar-vey/v667-v2/x1/portfolio-freeze.json"))
    flow = json.loads(index_blob("docs/tamar-vey/v667-v2/method-flow/startup-method-flow.json"))
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "all_json_parse": True,
        "document_word_cap": maximum_words <= 100000,
        "expected_14_4_1_1": freeze["expected_disposition_counts"]
        == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "five_class_scan_zero_confirmed_hits": not candidates,
        "novelty_4350_valid": json.loads(
            index_blob("docs/tamar-vey/v667-v2/x1/novelty-audit.json")
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
        "schema": "ghc.family.tamar-vey.v667-v2.x1-staged-review.v1",
        "owner": "Tamar Vey",
        "phase": "v667-v2",
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
            "schema": "ghc.family.tamar-vey.v667-v2.content-manifest.v1",
            "owner": "Tamar Vey",
            "phase": "x1",
            "phase_label": "v667-v2",
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
            "usage: build_ghc_family_tamar_vey_v667_v2_x1.py [--staged-review]"
        )
    else:
        main()
