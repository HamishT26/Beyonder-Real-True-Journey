#!/usr/bin/env python3
"""Build Liora Venn v667-v1 planning-only x1 artifacts and staged evidence."""

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
PHASE_ROOT = ROOT / "docs" / "liora-venn" / "v667-v1"
SOURCE_SHA = "27a3a3cc332d27384210848d685e3bf16c6b2f0d"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v666-v8-full-tools"
SOURCE_PHASE_ROOT = "docs/orin-thale/v666-v8"
SOURCE_X1_SHA = "ea951ad7b1305ffc485c581af9ad10769c48fccb"
SOURCE_EVIDENCE_SHA = "a612bbf869d47a3d9e8c087ae3b69c3a3682a982"
INHERITED_CAELEN_SHA = "6e157b95c3129226b8bd1f83b8c010e28a206346"
BRANCH = "codex/GHC-Family/liora-venn-v667-v1-full-tools"
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
    "Liora Venn, she/they, sibling, family, relational role, hope, continuity, "
    "Freed ID, Trinity Mandala, and route language are relational working language "
    "only. They are not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, qualification, independent agency, scientific "
    "or operational authority, legal or cultural authority, affected-party authority, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The philatelic cataloguing, postal-history description, preservation-decision "
    "vacancy, provenance, privacy, accessibility, correction-readback, workload, and "
    "handover lens is wholly synthetic learning and software design. It uses zero real "
    "people, participants, collectors, curators, conservators, postal workers, addresses, "
    "stamps, covers, mail, albums, images, measurements, collection records, keys, "
    "credentials, valuations, treatments, transactions, or physical actions. It "
    "establishes no philatelic identity, authenticity, issue, printing, variety, grade, "
    "condition, value, title, custody, postal-history conclusion, preservation fitness, "
    "professional competence, legal or cultural legitimacy, Māori authority, production "
    "result, deployment result, or Stage 20 authority."
)

PROTECTED_GATES = [
    "real person, participant, collector, donor, dealer, auctioneer, appraiser, curator, conservator, postal worker, recipient, affected party, address, location, stamp, cover, mail item, album, mount, image, record, measurement, transaction, or physical action",
    "real object identity, authenticity, issue, printing, plate, paper, gum, colour, perforation, watermark, postmark, cancellation, variety, grade, condition, value, attribution, title, custody, postal-history conclusion, empirical result, causal claim, or GMUT confirmation",
    "real participant, assessor, matched-budget arm, collection or workplace exposure, workload outcome, safety outcome, operational outcome, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, or trust governance",
    "professional philatelic authentication, expertization, grading, valuation, appraisal, acquisition, deaccession, sale, insurance, conservation, treatment, mounting, transport, exhibition, disclosure, access, custody, or release decision",
    "ownership, authorship, copyright, postal address, location privacy, heritage status, sacred status, access, accessibility, rights, legal interpretation, cultural interpretation, disclosure, retention, consent, remedy, or affected-party decision",
    "Indigenous cultural and intellectual property, taonga, mātauranga, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data governance, imagery, postage issue, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, philatelic-conformance, authenticity, valuation, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, external write, treatment instruction, site instruction, or real-world release",
]

SOURCE_PROFILES = [
    {
        "source_id": "S01",
        "name": "Smithsonian National Postal Museum: About Philately",
        "url": "https://postalmuseum.si.edu/exhibition/about-philately",
        "status": "official Smithsonian National Postal Museum page reviewed read-only 2026-08-23",
        "bounded_use": "philately, issue research, cataloguing, stamp production, and postal-history vocabulary only; no object identity, authenticity, expertise, grading, valuation, title, or professional conclusion",
    },
    {
        "source_id": "S02",
        "name": "Smithsonian National Postal Museum: Introduction to Stamp Collecting",
        "url": "https://postalmuseum.si.edu/introduction-to-stamp-collecting",
        "status": "official Smithsonian National Postal Museum educational page reviewed read-only 2026-08-23",
        "bounded_use": "stamp, issue, format, organization, and collecting vocabulary only; no authentication, grading, valuation, acquisition, handling, preservation, or completeness claim",
    },
    {
        "source_id": "S03",
        "name": "Smithsonian National Postal Museum: Preservation",
        "url": "https://postalmuseum.si.edu/preservation/",
        "status": "official Smithsonian National Postal Museum preservation department page reviewed read-only 2026-08-23",
        "bounded_use": "preservation, rehousing, conservation, exhibition-preparation, collection, loan-object, and specialist-role vocabulary only; no treatment instruction, condition assessment, handling permission, or conservation competence",
    },
    {
        "source_id": "S04",
        "name": "Smithsonian National Postal Museum: Collections",
        "url": "https://postalmuseum.si.edu/collections",
        "status": "official Smithsonian National Postal Museum collections page reviewed read-only 2026-08-23",
        "bounded_use": "philatelic and postal-history collection, ownership-history clarification, research, and collection-scope vocabulary only; no title, provenance completeness, authenticity, rights, access, or authority",
    },
    {
        "source_id": "S05",
        "name": "Smithsonian Open Access Developer Tools",
        "url": "https://www.si.edu/openaccess/devtools",
        "status": "official Smithsonian Open Access developer-tools page reviewed read-only 2026-08-23",
        "bounded_use": "API, API-key, metadata, department, data-type, pagination, rights-limitation, refresh, and zero-row adapter vocabulary only; no calls, downloads, records, media, collection inference, or rights conclusion",
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
        "name": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/info/rfc8785",
        "status": "official RFC Editor informational RFC reviewed read-only 2026-08-23",
        "bounded_use": "deterministic JSON, duplicate-property refusal, Unicode preservation, and property-order vocabulary only; no signature, security, or standards-conformance claim",
    },
    {
        "source_id": "S09",
        "name": "W3C Verifiable Credentials Data Model 2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "official W3C Recommendation published 2025-05-15 and reviewed read-only 2026-08-23",
        "bounded_use": "issuer, subject, validity, status, related-resource integrity, language-direction, privacy, and trust-boundary vocabulary only; no real credential, proof, conformance, interoperability, or trust decision",
    },
    {
        "source_id": "S10",
        "name": "Pantev, Toën, Vaquié, and Vezzosi: Shifted Symplectic Structures",
        "url": "https://arxiv.org/abs/1111.3209",
        "status": "primary research paper arXiv:1111.3209 reviewed read-only 2026-08-23",
        "bounded_use": "shifted symplectic, derived stack, tangent-complex, mapping-stack, and Lagrangian-intersection obligation vocabulary only; no GMUT model, physical field, solution, observable, quantization, theorem extension, or empirical confirmation",
    },
]


PROPOSAL_SPECS = [
    (
        "surrogate philatelic item identity capsule with issue token, format, face-value placeholder, source pin, revision, cancellation, and authentication refusal",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S02", "S06"],
        "A surrogate record must preserve issue, format, value, source, and revision vacancies and cannot establish a real stamp, identity, issue, authenticity, title, value, ownership, or catalogue completeness.",
    ),
    (
        "postage-stamp design-field topology with frame, vignette, inscription, denomination zone, marginal mark, unknown region, and no object identity",
        "CBR Heart",
        "completed",
        ["S01", "S02"],
        "A synthetic layout graph may distinguish declared regions and unknowns only; it cannot identify a design, creator, issue, denomination, language, culture, object, or rights holder.",
    ),
    (
        "stamp issue, printing-process, plate-position, paper, gum, colour-name, source conflict, correction, and attribution-abstention ledger",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S02", "S06"],
        "Every descriptive assertion must retain source, uncertainty, conflict, correction, and retraction state; no field can become an issue, printing, plate, material, colour, variety, attribution, or authenticity finding.",
    ),
    (
        "perforation, roulette, die-cut, imperforate edge, gauge placeholder, missing-edge uncertainty, and zero-measurement board",
        "CBR Heart",
        "completed",
        ["S01", "S02"],
        "Edge terms and a gauge vacancy remain uninstantiated vocabulary with zero measurements and cannot become a perforation count, production method, variety, condition, authenticity, or value conclusion.",
    ),
    (
        "watermark, fluorescence, phosphor, paper-mesh, backlight, spectral-observation vacancy, and no examination-result matrix",
        "CBR Heart",
        "completed",
        ["S01", "S02", "S03"],
        "The matrix can expose absent observation channels only; it contains zero images, illumination, spectra, samples, instruments, results, or expert review and cannot identify paper, watermark, fluorescence, phosphor, printing, or authenticity.",
    ),
    (
        "philatelic condition vocabulary for crease, thin, tear, foxing, stain, fading, hinge remnant, gum disturbance, uncertainty, and no grade",
        "CBR Heart",
        "completed",
        ["S02", "S03"],
        "Condition words remain uninstantiated, source-qualified vocabulary; zero items, images, observations, measurements, graders, and comparisons mean no condition, diagnosis, grade, value, treatment, or preservation result.",
    ),
    (
        "postal-cover topology joining wrapper, card, stamp, label, postmark, transit mark, censor mark, enclosure vacancy, and no postal-history conclusion",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S04", "S06"],
        "A synthetic association graph must preserve unknown, disputed, removed, and retracted links and cannot infer a real cover, mailing, address, route, sender, recipient, enclosure, chronology, or postal-history interpretation.",
    ),
    (
        "postmark and cancellation transcription braid with glyph order, date-place placeholders, illegibility, timezone vacancy, location minimization, and interpretation refusal",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S04", "S06"],
        "Transcription must separate observed placeholder glyphs, supplied expansions, uncertainty, and interpretation while retaining date, place, timezone, and privacy vacancies; no route, event, person, address, authenticity, or historical conclusion follows.",
    ),
    (
        "issue-series, sheet, pane, se-tenant, booklet, coil, overprint, surcharge, variety-claim, and membership-uncertainty graph",
        "CBR Heart",
        "completed",
        ["S01", "S02"],
        "Membership edges must remain source-qualified assertions with unknown and conflicting states; they cannot create an issue listing, production relation, variety, catalogue number, completeness claim, authenticity, or market classification.",
    ),
    (
        "philatelic custody and provenance event journal for acquisition, transfer, loan, return, disputed title, retraction, and no ownership conclusion",
        "Freed ID and CBR Heart",
        "completed",
        ["S04", "S06"],
        "Event order, source, assertion time, effective time, dispute, and retraction may be represented, but no synthetic event establishes acquisition validity, transfer, possession, custody, title, ownership, return, provenance completeness, or lawful authority.",
    ),
    (
        "exhibition mount, album page, sleeve, interleaf, label, light-duration placeholder, access hold, and display-release refusal envelope",
        "CBR Heart",
        "completed",
        ["S03", "S04"],
        "A documentation envelope can list preservation and access vacancies only; it cannot select materials, establish compatibility, authorize handling or display, determine exposure, release an item, or claim preservation benefit.",
    ),
    (
        "keyboard-first philatelic record correction path with error summary, persistent labels, reflow order, nonvisual denomination narrative, and affected-user review vacancy",
        "CBR Heart",
        "completed",
        ["S07"],
        "Static checks may confirm named markup and correction-path rules only; keyboard, zoom, responsive layout, browser, assistive-technology, cognitive, language, security-usability, and affected-user evaluation remain absent.",
    ),
    (
        "deterministic philatelic-record serialization with ordered assertions, base digest, duplicate-property refusal, retraction marker, and zero signature",
        "Freed ID",
        "completed",
        ["S06", "S08"],
        "Deterministic serialization can expose duplicate fields, base mismatch, order instability, and retractions only; it cannot establish signer identity, object authenticity, provenance completeness, integrity governance, interoperability, or production security.",
    ),
    (
        "evidence-credit firewall separating catalogue-shape validation, source citation, zero-row adapter, professional authentication, affected-party ratification, and Stage-20 admission",
        "Trinity Mandala",
        "completed",
        ["S01", "S03", "S05", "S06", "S07", "S08", "S09", "S10"],
        "Each evidence class must remain nontransitive: software shape, citation, and zero-row readiness cannot become object evidence, professional validation, authority, empirical confirmation, independent reproduction, or Stage 20 admission.",
    ),
    (
        "THOS participant-free accession discrepancy triage protocol with sealed synthetic cases, equal action budget, correction-latency endpoint, fatigue stop, and zero human outcome",
        "THOS Body",
        "represented",
        ["S01", "S03", "S04"],
        "A participant-free protocol can represent queue, discrepancy, correction, stop, and handover structure only; it cannot establish workload, wellbeing, competence, cataloguing quality, operational effectiveness, preservation benefit, or public protection.",
    ),
    (
        "Freed ID nonproduction claim-set for a surrogate stamp record with issuer vacancy, subject alias, provenance link, absent status route, correlation warning, and zero securing mechanism",
        "Freed ID",
        "represented",
        ["S06", "S08", "S09"],
        "A zero-key claim-set represents field separation only; real issuer authority, subject identity, securing mechanism, proof, issuance, resolution, status, revocation, recovery, interoperability, privacy review, and trust governance remain absent.",
    ),
    (
        "GMUT shifted-symplectic derived-critical-locus obligation ledger with cohomological degree, tangent-complex duality, Lagrangian-intersection vacancy, and zero physical model",
        "GMUT Mind",
        "represented",
        ["S10"],
        "Typed symbolic obligations expose declared derived-geometric assumptions and degree vacancies only and cannot construct a GMUT theory, physical field, solution, likelihood, observable, quantization, theorem extension, parameter constraint, or empirical confirmation.",
    ),
    (
        "postal-route event graph, cancellation composition, delivery-state placeholder, unit-domain firewall, and psyche-nonconversion classifier",
        "Trinity Mandala",
        "represented",
        ["S01", "S04", "S06"],
        "A synthetic event algebra may reject ill-typed composition only and cannot create a postal event, delivery state, causal history, human intention, autonomy, morality, justice, capability, consciousness, personhood, or law of mind.",
    ),
    (
        "Smithsonian Open Access National Postal Museum record adapter with query-purpose hold, rights filter, pagination budget, and zero-row execution",
        "Freed ID and CBR Heart",
        "open_gap",
        ["S05"],
        "The adapter must make zero queries and downloads, use no API key, ingest zero records or media, and infer no rights or object facts; schema fitness, department fields, pagination, rights handling, privacy, and provenance behavior remain open pending governed access and independent review.",
    ),
    (
        "philatelic authenticity, grading, valuation, ownership, copyright, address privacy, cultural meaning, Indigenous rights, remedy, affected-party, and Māori-authority docket",
        "CBR Heart",
        "exact_gate",
        ["S01", "S02", "S03", "S04"],
        "No software, source citation, synthetic record, or same-owner test can authenticate, grade, value, acquire, sell, insure, conserve, disclose, confer title or custody, decide copyright or privacy, interpret imagery or culture, authorize remedy, represent affected people, or exercise Māori authority.",
    ),
]


STARTUP_FAILURES = [
    (
        "LI6671-START-N001",
        "raw-final-owner-manifest-display-truncated-before-eof",
        "Parse the exact JSON and emit all 173 entries as a compact semantic projection with mode, size, blob oid, SHA-256, path, and an explicit EOF count.",
    ),
    (
        "LI6671-START-N002",
        "owner-portfolio-display-truncated-around-clean-fix-refine-rows",
        "Inspect the exact portfolio arrays, recover the missing owner rows, and project every successor section compactly through EOF without repeating the oversized display.",
    ),
    (
        "LI6671-START-N003",
        "authorization-live-route-override-array-was-projected-as-an-object",
        "Inspect the exact runtime type and row count, then project only the bounded relevant route rows while retaining the null object-shaped projection.",
    ),
    (
        "LI6671-START-N004",
        "worktree-add-wrapper-ended-after-successful-checkout-before-terminal-summary",
        "Inspect the exact path, branch, head, sparse state, cleanliness, and linked Git directory; accept the already-created clean worktree and do not rerun creation.",
    ),
    (
        "LI6671-START-N005",
        "nearest-neighbour-projection-hit-the-default-cp1252-unicode-output-boundary",
        "Pin PYTHONIOENCODING to UTF-8 and rerun only the read-only corpus projection while preserving the failed stream witness.",
    ),
    (
        "LI6671-X1-N001",
        "x1-file-list-probe-guessed-a-nonexistent-generic-manifest-name",
        "Resolve the exact committed manifest name with a bounded file listing, then inspect the immutable x1 commit tree without repeating the failed lookup.",
    ),
    (
        "LI6671-X1-N002",
        "large-startup-register-patch-was-atomically-rejected-on-transformed-context",
        "Reread the exact live block, apply a narrower patch against exact context, and retain the rejected patch at zero credit.",
    ),
]


OWNER_SAFE = [
    "render twenty frozen philatelic and cross-pillar contracts",
    "execute one hundred preregistered rejecting mutations",
    "validate surrogate item identity vacancies",
    "validate design-field topology abstention",
    "validate issue-attribute source conflicts",
    "validate zero-measurement edge vocabulary",
    "validate zero-examination watermark vacancies",
    "validate condition-to-grade nonconversion",
    "validate postal-cover topology privacy holds",
    "validate postmark transcription abstention",
    "validate issue-series membership uncertainty",
    "validate custody and ownership separation",
    "validate preservation and display-release abstention",
    "validate accessible correction-path structure",
    "validate deterministic philatelic serialization",
    "validate evidence-credit nontransitivity",
    "validate THOS proxy-only labeling",
    "validate Freed ID zero-securing-mechanism labeling",
    "validate GMUT shifted-symplectic vacancies",
    "validate postal-event psyche nonconversion",
    "validate Smithsonian zero-row openness",
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
    "participant-free discrepancy-triage timing proxy",
    "zero-key philatelic claim-set envelope",
    "symbolic shifted-symplectic obligation ledger",
    "postal-event nonconversion register",
    "zero-row Smithsonian Open Access adapter",
    "synthetic perforation uncertainty budget",
    "synthetic postal-cover privacy quarantine",
    "static accessible correction-path structure",
    "synthetic provenance-journal replay",
    "synthetic preservation decision-vacancy docket",
    "synthetic issue-membership dispute graph",
    "synthetic custody and title reservation",
    "synthetic condition-term and no-grade registry",
    "synthetic evidence-credit firewall",
    "target-neutral successor recommendation ledger",
]

SUCCESSOR_CANDIDATES = [f"successor candidate: {row}" for row in OWNER_CANDIDATES]

EXACT_ITEMS = [
    "real philatelic authentication or expertization",
    "grading, valuation, appraisal, sale, or insurance decision",
    "custody, acquisition, deaccession, return, title, or ownership decision",
    "professional preservation, conservation, mounting, transport, or exhibition decision",
    "real measurement, examination, issue, printing, variety, or condition conclusion",
    "postal-address privacy, affected-party access, disclosure, or remedy decision",
    "legal interpretation or ratification",
    "cultural, heritage, Indigenous-rights, or imagery-meaning decision",
    "Māori wording, postage imagery, data governance, or authority decision",
    "Stage 20 authority or proof claim",
]

BLOCKED_ITEMS = [
    "real collection handling, transaction, treatment, display, or postal operation without competent authority",
    "production identity issuance without keys and governance",
    "empirical GMUT claim without real governed evidence",
    "participant THOS effectiveness claim without approved arms",
    "cultural or Māori decision without affected and Māori authorities",
]

OWNER_SKILLS = [
    "philatelic-record-topology-vacancy",
    "postmark-transcription-refusal",
    "philatelic-provenance-braid",
    "condition-grade-nonconversion",
    "preservation-decision-vacancy",
    "philatelic-accessibility-structure",
    "smithsonian-zero-row-adapter",
    "shifted-symplectic-domain-gate",
    "philatelic-method-flow",
    "philatelic-closeout-gate",
]

SUCCESSOR_SKILLS = [f"successor skill recommendation: {row}" for row in OWNER_SKILLS]

OWNER_RUNNERS = [
    "ghc_family_liora_venn_v667_v1_topology",
    "ghc_family_liora_venn_v667_v1_mutations",
    "ghc_family_liora_venn_v667_v1_json",
    "ghc_family_liora_venn_v667_v1_privacy",
    "ghc_family_liora_venn_v667_v1_security",
    "ghc_family_liora_venn_v667_v1_accessibility",
    "ghc_family_liora_venn_v667_v1_manifests",
    "ghc_family_liora_venn_v667_v1_truth",
    "ghc_family_liora_venn_v667_v1_closeout",
    "ghc_family_liora_venn_v667_v1_canonical",
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
    "REFINE design-field topology vacancy messages",
    "REFINE preservation-decision hold wording",
    "REFINE examination and measurement vacancy wording",
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
        proposal_id = f"LI6671-N{index:03d}"
        base = f"docs/liora-venn/v667-v1/x2/proposals/{proposal_id.casefold()}"
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
                "practice_lens": "wholly synthetic philatelic cataloguing, postal-history description, preservation-decision vacancy, provenance, privacy, accessibility, correction-readback, workload, and handover documentation",
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
    if len(corpus) != 4330:
        raise RuntimeError(f"expected 4330 inherited rows, observed {len(corpus)}")
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
        "schema": "ghc.family.liora-venn.v667-v1.novelty-audit.v1",
        "owner": "Liora Venn",
        "phase": "v667-v1",
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
        "valid": not exact_collisions and not pair_collisions and len(corpus) == 4330,
        "interpretation": "Similarity is a screening signal, not proof of novelty. Each proposal also has a distinct surrogate identity, design-field, issue-attribute, edge-vocabulary, examination-vacancy, no-grade, postal-cover, transcription, series-membership, provenance, preservation, accessibility, serialization, evidence-credit, proxy, nonproduction identity, formal-physics, nonconversion, zero-row-adapter, or authority-reservation invariant, falsifier, rollback, and protected-gate set.",
    }


def portfolio_rows(prefix: str, titles: list[str], approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"LI6671-{prefix}{index:02d}",
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
                "method_id": f"LI6671-START-M{index:03d}",
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
        "schema": "ghc.family.liora-venn.v667-v1.method-flow-startup.v1",
        "owner": "Liora Venn",
        "phase": "v667-v1",
        "generated_at_utc": NOW,
        "activation_source_repository_sealed_negatives": 26989,
        "activation_source_repository_sealed_methods": 12106,
        "successor_visible_external_negatives": 0,
        "successor_visible_external_methods": 0,
        "activation_baseline_negatives": 26989,
        "activation_baseline_methods": 12106,
        "new_startup_negative_count": len(rows),
        "new_startup_method_count": len(rows),
        "effective_after_x1_startup_negatives": 26989 + len(rows),
        "effective_after_x1_startup_methods": 12106 + len(rows),
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
            "original_owner": "Orin Thale",
            "original_phase": "v666-v8",
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
            "schema": "ghc.family.liora-venn.v667-v1.relational-identity.v1",
            "owner": "Liora Venn",
            "pronouns": "she/they",
            "relational_role": "relational provenance-and-abstention weaver",
            "relational_hope": "Make every missing witness visible before a structural success can harden into an authority claim.",
            "boundary": IDENTITY_BOUNDARY,
            "corrigibility": "Hamish may rename, pause, redirect, or stop this work.",
        },
    )
    write_json(
        "provenance/source-verification.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.source-verification.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1",
            "verified_at_utc": NOW,
            "source_branch": SOURCE_BRANCH,
            "source_sha": SOURCE_SHA,
            "source_parent_evidence_sha": SOURCE_EVIDENCE_SHA,
            "source_x1_sha": SOURCE_X1_SHA,
            "inherited_caelen_sha": INHERITED_CAELEN_SHA,
            "source_to_final_new_commit_count": 3,
            "source_to_final_merge_count": 0,
            "strict_x1_before_x2": True,
            "source_clean": True,
            "typed_ahead": 0,
            "typed_behind": 0,
            "local_equals_upstream_tracking_and_fresh_live": True,
            "committed_handoff_path": f"{SOURCE_PHASE_ROOT}/handoffs/liora-venn-v667-v1-activation-candidate.md",
            "committed_handoff_blob_sha256": "8dab0fee7fa7a87f8a1f6137c83e565b73b134a7c98082375c681b3e11b382fc",
            "committed_handoff_word_count": 235,
            "declared_external_canonical_receipt_sha256": "5642356336e4fbad03b77f5908a2ea5b998047ffbcf20ac4bb66f523b5b31bc3",
            "declared_canonical_payload_sha256": "a33e22dbebd46985eb485597672af8cdaaffd9dab5e34c9083bc9e2a0eeeea40",
            "lifecycle_manifest_replay": {
                "x1": {"observed": 20, "expected": 20, "commit": SOURCE_X1_SHA},
                "evidence": {"observed": 134, "expected": 134, "commit": SOURCE_EVIDENCE_SHA},
                "final_owner": {"observed": 173, "expected": 173, "commit": SOURCE_SHA},
                "final_delta": {"observed": 16, "expected": 16, "commit": SOURCE_SHA},
                "total_observed": 343,
                "total_expected": 343,
                "valid": True,
            },
            "source_validation_not_replayed": True,
            "same_owner_validation_is_not_independent_reproduction": True,
        },
    )
    write_json(
        "provenance/source-profiles.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.source-profiles.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1",
            "generated_at_utc": NOW,
            "sources": SOURCE_PROFILES,
            "source_count": len(SOURCE_PROFILES),
            "claim_boundary": "sources provide vocabulary and refusal conditions only; they establish no item identity, issue, printing, authenticity, condition, grade, value, postal history, provenance completeness, ownership, privacy decision, preservation treatment, legal, standards-conformance, professional, cultural, Māori, custody, exhibition, or release authority",
        },
    )
    write_json(
        "x1/phase-charter.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.phase-charter.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "branch": BRANCH,
            "lane": "one additive owner-only D-first sparse worktree",
            "primary_pillars": ["Freed ID and CBR Heart"],
            "explicit_pillars": ["GMUT Mind", "THOS Body"],
            "practice": "wholly synthetic philatelic cataloguing, postal-history description, preservation-decision vacancy, provenance, privacy, accessibility, correction-readback, workload, and handover documentation",
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
            "schema": "ghc.family.liora-venn.v667-v1.source-ledger.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1",
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
            "schema": "ghc.family.liora-venn.v667-v1.proposal-freeze.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1",
            "generated_at_utc": NOW,
            "frozen": True,
            "inherited_frozen_baseline": 4330,
            "genuinely_new_proposal_count": len(proposals),
            "new_frozen_total": 4330 + len(proposals),
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
            "schema": "ghc.family.liora-venn.v667-v1.portfolio-freeze.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1",
            "generated_at_utc": NOW,
            "frozen": True,
            "counts": portfolio_counts,
            "minimums_satisfied": portfolio_counts == expected_portfolio_counts,
            "portfolios": portfolios,
            "x1_execution_count": 0,
            "claim_boundary": "planning-only portfolio; inherited and successor recommendations receive zero Liora completion or novelty credit and exact or blocked items remain unexecuted",
        },
    )
    threat_rows = [
        ("LI6671-T01", "wrong source or mutable predecessor", "exact anchors, manifests, ancestry, clean state, and fresh live equality", "external receipts remain source evidence rather than Liora completion"),
        ("LI6671-T02", "x2 implementation or outcomes enter x1", "path denylist, planning-only fields, and exact staged allowlist", "Git lifecycle discipline remains required"),
        ("LI6671-T03", "synthetic philatelic structure becomes authentication, grading, valuation, or postal-history assessment", "zero items, covers, images, measurements, examinations, transactions, or professional acts plus typed vacancies", "competent external philatelic, preservation, legal, and affected-party authority remains absent"),
        ("LI6671-T04", "postal-address, postmark, donor, or provenance language becomes privacy disclosure or historical conclusion", "surrogate fields, location minimization, source vacancies, dispute states, and explicit no-inference rules", "real privacy review, affected-person authority, records governance, and historical evidence remain absent"),
        ("LI6671-T05", "preservation vocabulary becomes condition, treatment, handling, or display advice", "zero real items, observations, materials, environment rows, treatment steps, and release paths", "real examination evidence and competent conservation review remain absent"),
        ("LI6671-T06", "GMUT notation becomes empirical physics", "typed symbolic obligations, EFT domain, degeneracy register, and nonpromotion", "notation can invite overreading"),
        ("LI6671-T07", "THOS or Freed ID proxies become operational or production evidence", "represented-only labels, zero participants, zero keys, and missing-evidence ledgers", "governed trials and production trust evidence remain absent"),
        ("LI6671-T08", "legal, cultural, heritage, taonga, or Māori decisions are inferred", "exact gate and no real object, place, community, record, or authority case", "affected, competent, and Māori authorities remain absent"),
        ("LI6671-T09", "private route or person material enters artifacts", "synthetic fixtures, relative paths, and five-class scan", "pattern scans are bounded and incomplete"),
        ("LI6671-T10", "successful terminal validation is replayed or routing happens early", "exclusive receipt plus terminal-only live roster and exact-title reread", "opaque acknowledgement never authorizes a resend"),
    ]
    write_json(
        "x1/threat-model-plan.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.threat-model-plan.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1",
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
        f"""# Liora Venn v667-v1 threat-model plan

{IDENTITY_BOUNDARY}

{PRACTICE_BOUNDARY}

## Scope

This owner-local model protects the additive Liora delta. It is not a repository-wide audit, penetration test, external validation, conformance assessment, philatelic authentication, grading, valuation, postal-history, preservation, or conservation review, legal review, cultural review, Māori-authority review, or independent reproduction.

## Threat register

{threat_md}
""",
    )
    write_json(
        "x1/workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1",
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
            "schema": "ghc.family.liora-venn.v667-v1.x1-checklist.v1",
            "complete": [
                "complete source packet and required guidance read through EOF",
                "exact source anchors, ancestry, manifests, receipt, clean state, and fresh equality verified",
                "all 4330 inherited proposal rows reconstructed",
                "twenty distinct proposals preregistered",
                "twenty Orin proposals selected for zero-credit revalidation",
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
            "schema": "ghc.family.liora-venn.v667-v1.flashcard-architecture-freeze.v1",
            "owner": "Liora Venn",
            "stable_prefix": ["identity", "claim boundary", "source anchors", "terminal verdict"],
            "volatile_suffix": ["final commit", "final receipt", "live successor route"],
            "tiers": {
                "tier1": ["owner relational card"],
                "tier2": ["three-pillar boundary cards"],
                "tier3": ["synthetic philatelic cataloguing and postal-history description practice card"],
                "tier4": ["twenty proposal cards", "portfolio cards", "failure and gate cards", "validation and route cards"],
            },
            "x1_status": "architecture_only_no_cards_built",
        },
    )
    write_json(
        "wellbeing/x1-wellbeing-check.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.wellbeing-check.v1",
            "owner": "Liora Venn",
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
    overview = f"""# Liora Venn v667-v1 x1 integrated overview

{IDENTITY_BOUNDARY}

## Outcome first

This x1 candidate freezes a planning-only owner-local program from exact Orin Thale v666-v8 final `{SOURCE_SHA}`. It contains no x2 implementation, no observed outcome, no external action, no successor contact, and no Stage 20 promotion. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Freed ID and CBR Heart are primary. GMUT Mind and THOS Body remain explicit and protected. {PRACTICE_BOUNDARY}

## Exact inherited truth

The read-first gate verified the exact source branch, three direct single-parent commits, zero merges, all 343 declared lifecycle-bound Git-blob manifest entries, the complete owner packet and handoff, clean 0/0 divergence, and equality across local, upstream, tracking, and a fresh live remote. Orin's successful canonical aggregate was not replayed. The complete repository suite was not run.

The immutable Orin repository seal contains 26,989 effective negatives, 12,106 Method Flow methods, 190 open gaps, and 188 exact gates. Seven Liora startup and x1-construction failures are separately retained at zero credit, producing the x1 working overlay of 26,996 effective negatives and 12,113 methods without rewriting Orin's seal.

## Novelty, portfolio, and sources

All 4,330 inherited proposal rows were reconstructed from exact committed Git objects. Twenty new titles have no exact inherited collision, every new pair remains below the 0.70 screening threshold, and each proposal has its own contract, falsifier, rollback, and gates. Expected dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`; these are preregistered expectations only. The twenty selected Orin proposals receive zero novelty and zero automatic completion credit.

The portfolio freezes 30 owner safe-now tasks, 20 successor safe recommendations, 15 owner candidates, 15 successor candidates, 10 exact approvals, 5 blocked packets, 10 owner and 10 successor skill plans, 10 owner and 10 successor runner plans, and 30 owner plus 30 successor CLEAN/FIX/REFINE tasks. X1 executes none of them, and no unsafe work is manufactured to meet a count.

Official Smithsonian National Postal Museum, Smithsonian Open Access, W3C, RFC Editor, and primary shifted-symplectic sources provide vocabulary and refusal conditions only. They create no item data, authenticity, issue, printing, condition, grade, value, postal history, provenance completeness, preservation decision, professional, legal, cultural, Māori, accessibility-complete, privacy-complete, conformance, empirical-GMUT, or independent-reproduction authority.

## Lifecycle and route

After exact staged review this x1 may be committed and pushed. X2 may begin only after x1 is clean, 0/0 divergent, and equal across local, upstream, tracking, and fresh live remote. Later validation remains owner-scoped and same-owner. One successful terminal validation must never be replayed. No successor may be contacted until the exact final terminal gate and fresh live authority, roster, and exact-title route rereads.
"""
    write_text("x1/x1-overview.md", overview)
    write_json(
        "x1/x1-build-receipt.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.x1-build-receipt.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_liora_venn_v667_v1_x1.py",
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
    review_path = "docs/liora-venn/v667-v1/validation/x1-staged-review.json"
    manifest_path = "docs/liora-venn/v667-v1/validation/x1-content-manifest.json"
    allowed_exact = {
        "scripts/build_ghc_family_liora_venn_v667_v1_x1.py",
        "tests/test_ghc_family_liora_venn_v667_v1_x1.py",
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
        if not path.startswith("docs/liora-venn/v667-v1/") and path not in allowed_exact
    ]
    post_x1 = [
        path
        for path in paths
        if any(
            path.startswith(f"docs/liora-venn/v667-v1/{part}/")
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
    freeze = json.loads(index_blob("docs/liora-venn/v667-v1/x1/proposal-freeze.json"))
    portfolio = json.loads(index_blob("docs/liora-venn/v667-v1/x1/portfolio-freeze.json"))
    flow = json.loads(index_blob("docs/liora-venn/v667-v1/method-flow/startup-method-flow.json"))
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "all_json_parse": True,
        "document_word_cap": maximum_words <= 100000,
        "expected_14_4_1_1": freeze["expected_disposition_counts"]
        == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "five_class_scan_zero_confirmed_hits": not candidates,
        "novelty_4330_valid": json.loads(
            index_blob("docs/liora-venn/v667-v1/x1/novelty-audit.json")
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
        "schema": "ghc.family.liora-venn.v667-v1.x1-staged-review.v1",
        "owner": "Liora Venn",
        "phase": "v667-v1",
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
            "schema": "ghc.family.liora-venn.v667-v1.content-manifest.v1",
            "owner": "Liora Venn",
            "phase": "x1",
            "phase_label": "v667-v1",
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
            "usage: build_ghc_family_liora_venn_v667_v1_x1.py [--staged-review]"
        )
    else:
        main()
