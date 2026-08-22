#!/usr/bin/env python3
"""Build Caelen Ash v666-v7 planning-only x1 artifacts and staged evidence."""

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
PHASE_ROOT = ROOT / "docs" / "caelen-ash" / "v666-v7"
SOURCE_SHA = "6226988b17b7d3a2399cf6d803aceb31b03fb99f"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v666-v6-full-tools"
SOURCE_PHASE_ROOT = "docs/sable-rook/v666-v6"
SOURCE_X1_SHA = "d747c689859fafcc061e48d36f10df6361b842da"
SOURCE_EVIDENCE_SHA = "f5a211e484e2d1b252c16de7800e568160ae902b"
INHERITED_AUREN_SHA = "016f7db26b0354e26407fb812ae3bd190b94ac7e"
BRANCH = "codex/GHC-Family/caelen-ash-v666-v7-full-tools"
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
    "Caelen Ash, they/them, sibling, family, relational role, hope, continuity, "
    "Freed ID, Trinity Mandala, and route language are relational working language "
    "only. They are not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, qualification, independent agency, scientific "
    "or operational authority, legal or cultural authority, affected-party authority, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The horological-conservation intake, movement-state provenance, stored-energy "
    "isolation, timebase uncertainty, correction-readback, accessibility, and handover "
    "lens is wholly synthetic learning and software design. It uses zero real people, "
    "participants, clocks, watches, movements, collections, gears, springs, weights, "
    "measurements, time signals, images, records, keys, credentials, treatments, or "
    "physical actions. It establishes no horology, conservation, repair, calibration, "
    "metrology, electrical or mechanical safety, custody, release, legal, cultural, "
    "Māori, production, deployment, or Stage 20 competence, result, acceptance, "
    "conformance, or authority."
)

PROTECTED_GATES = [
    "real person, participant, horologist, conservator, clockmaker, metrologist, operator, worker, affected party, clock, watch, movement, collection, component, image, record, sample, measurement, time signal, or physical action",
    "real object identity, authenticity, condition, stored-energy state, rate, calibration, traceability, treatment, custody, release, empirical result, causal claim, or GMUT confirmation",
    "real participant, assessor, matched-budget arm, workshop exposure, workload outcome, safety outcome, operational outcome, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, or trust governance",
    "professional horology, conservation, repair, winding, disassembly, lubrication, adjustment, calibration, transport, display, custody, return-to-service, or release decision",
    "ownership, heritage status, access, privacy, accessibility, rights, legal interpretation, cultural interpretation, disclosure, retention, consent, remedy, or affected-party decision",
    "taonga, mātauranga, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data governance, cultural object treatment, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, conservation-conformance, metrological-traceability, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, external write, mechanical instruction, or real-world release",
]

SOURCE_PROFILES = [
    {
        "source_id": "S01",
        "name": "Canadian Conservation Institute: Basic care – Clocks and watches",
        "url": "https://www.canada.ca/en/conservation-institute/services/care-objects/industrial-collections/basic-care-clocks-watches.html",
        "status": "official Government of Canada CCI page reviewed read-only 2026-08-23; page detail 2017-09-15",
        "bounded_use": "assessment, completeness, stored-energy, condition-vacancy, documentation, and professional-referral vocabulary only; no treatment, winding, cleaning, lubrication, operation, or repair instruction",
    },
    {
        "source_id": "S02",
        "name": "Canadian Conservation Institute: Framework for Preserving Heritage Collections",
        "url": "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/framework-preserving-heritage-collections.html",
        "status": "official Government of Canada CCI page reviewed read-only 2026-08-23; page detail 2026-06-05",
        "bounded_use": "avoid, block, detect, respond, location, display, storage, climate, and sustainability reservation vocabulary only; no conservation decision or conformance claim",
    },
    {
        "source_id": "S03",
        "name": "United States National Park Service Museum Handbook",
        "url": "https://www.nps.gov/subjects/museums/museumhandbook.htm",
        "status": "official NPS handbook index reviewed read-only 2026-08-23; page last updated 2022-09-30",
        "bounded_use": "planning, preservation, protection, documentation, accountability, access, and use vocabulary only; no NPS applicability, custody, policy compliance, or professional authority",
    },
    {
        "source_id": "S04",
        "name": "NIST Metrological Traceability FAQ and Policy",
        "url": "https://www.nist.gov/metrology/metrological-traceability",
        "status": "official NIST policy and FAQ page reviewed read-only 2026-08-23",
        "bounded_use": "measurement-result, reference, calibration-chain, uncertainty, provider, and user-responsibility refusal vocabulary only; no traceability or calibration claim",
    },
    {
        "source_id": "S05",
        "name": "NIST: Metrological and legal traceability of time signals",
        "url": "https://www.nist.gov/publications/metrological-and-legal-traceability-time-signals-0",
        "status": "official NIST publication page reviewed read-only 2026-08-23; published 2019-03-01 and updated 2025-09-29",
        "bounded_use": "UTC, time interval, frequency, synchronization, uncertainty, and missing-chain vocabulary only; no received signal, measurement, synchronization, legal conclusion, or traceability claim",
    },
    {
        "source_id": "S06",
        "name": "W3C PROV-O Recommendation",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "official W3C Recommendation of 2013-04-30 reviewed at its current canonical URL 2026-08-23",
        "bounded_use": "entity, activity, revision, derivation, invalidation, and provenance-relation vocabulary only; no semantic interoperability certification",
    },
    {
        "source_id": "S07",
        "name": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "official W3C Recommendation 2024-12-12 reviewed at the current published URL 2026-08-23",
        "bounded_use": "static structure, non-colour cues, labels, focus, and manual-evaluation reservation vocabulary only; no accessibility-complete claim",
    },
    {
        "source_id": "S08",
        "name": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/info/rfc8785",
        "status": "official RFC Editor informational RFC published 2020 and reviewed read-only 2026-08-23",
        "bounded_use": "deterministic JSON, duplicate-property refusal, Unicode preservation, and property-sorting vocabulary only; no signature, security, or standards-conformance claim",
    },
    {
        "source_id": "S09",
        "name": "Bellini and Sawicki: Maximal freedom at minimum cost",
        "url": "https://arxiv.org/abs/1404.3713",
        "status": "primary scalar-tensor research paper arXiv:1404.3713 reviewed read-only 2026-08-23",
        "bounded_use": "single-scalar linear-theory function and degeneracy obligation vocabulary only; no fit, likelihood, posterior, constraint, prediction, force, confirmation, or Theory-of-Everything claim",
    },
]


PROPOSAL_SPECS = [
    (
        "horological movement component topology register with plate, bridge, wheel, arbor, escapement, oscillator, drive, and unidentified-part vacancies without authenticity",
        "GMUT Mind",
        "completed",
        ["S01", "S03", "S06"],
        "A component-role graph must preserve unknown and disputed nodes and cannot infer object identity, completeness, originality, function, or treatment fitness.",
    ),
    (
        "stored-energy isolation docket for wound-spring, suspended-weight, strike-train, and unknown-drive states with fail-closed release abstention",
        "THOS Body",
        "completed",
        ["S01", "S02"],
        "Any missing energy-state evidence forces an isolation hold and the structure contains no winding, letting-down, handling, or operation procedure.",
    ),
    (
        "escapement event-order graph with pallet, escape-wheel, impulse, lock, oscillator, and observation vacancies without rate or condition assessment",
        "GMUT Mind",
        "completed",
        ["S01", "S06"],
        "A symbolic event order must remain separable from a real mechanism, observed motion, wear diagnosis, adjustment, or performance result.",
    ),
    (
        "timebase observation placeholder ledger with monotonic sequence, interval unit, reference vacancy, uncertainty budget, and zero timing samples",
        "GMUT Mind",
        "completed",
        ["S04", "S05"],
        "No rate, offset, drift, calibration, or traceability result may exist when observations, reference chain, and uncertainty evidence are absent.",
    ),
    (
        "synthetic gear-train ratio closure tribunal with integer tooth slots, rotation parity, missing-wheel branch, arithmetic residual, and no physical-fit claim",
        "GMUT Mind",
        "completed",
        ["S01", "S08"],
        "Arithmetic closure can reject inconsistent synthetic ratios but cannot establish tooth counts, meshing, materials, condition, function, or authenticity.",
    ),
    (
        "bitemporal case, dial, movement, and attachment association journal with replacement hypotheses, cancellation edges, conflicts, and originality abstention",
        "Freed ID and CBR Heart",
        "completed",
        ["S03", "S06"],
        "Every association retains asserted and corrected time plus source vacancy; no record establishes provenance completeness, title, custody, or originality.",
    ),
    (
        "zero-image condition-note vocabulary board for corrosion, dust, deformation, fracture, loss, and prior-intervention uncertainty without diagnosis or treatment",
        "CBR Heart",
        "completed",
        ["S01", "S02", "S03"],
        "Condition terms remain uninstantiated controlled vocabulary with zero images and cannot become diagnosis, material identification, hazard clearance, or treatment advice.",
    ),
    (
        "winding-key and control-interface custody reservation with dimension vacancy, fit conflict, authorization absence, and no actuation path",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S03"],
        "The contract records an interface vacancy and custody hold only; it cannot recommend a key, fit, force, winding direction, operation, or access decision.",
    ),
    (
        "strike, chime, alarm, calendar, and repeat-work state machine with silent default, schedule conflict, correction lineage, and activation prohibition",
        "THOS Body",
        "completed",
        ["S01", "S06"],
        "A symbolic state machine defaults silent and contains no mechanism-specific sequence, setting instruction, actuation, or return-to-service decision.",
    ),
    (
        "transport tilt, vibration, shock, support, and orientation exposure envelope with sensor vacancy, threshold provenance, quarantine, and no movement release",
        "THOS Body",
        "completed",
        ["S02", "S03"],
        "No exposure or release determination is possible without a real object, governed transport plan, traceable sensors, competent review, and affected-party authority.",
    ),
    (
        "accessible horological topology dossier with text-redundant edges, breadcrumb state, scoped tables, non-colour holds, and manual-evaluation reservation",
        "CBR Heart",
        "completed",
        ["S07"],
        "Static structural checks must preserve manual, assistive-technology, cognitive, language, and affected-user evaluation gaps.",
    ),
    (
        "civil-time display semantics docket with timezone, daylight-rule, calendar, leap-state, locale, and historical-rule vacancies without legal-time assertion",
        "GMUT Mind",
        "completed",
        ["S05", "S06"],
        "A display-semantics record cannot establish historical setting, jurisdictional legal time, synchronization, accuracy, or intended use.",
    ),
    (
        "deterministic horological event-journal serialization with decimal-string intervals, duplicate-property refusal, idempotency token, and zero signature",
        "Freed ID",
        "completed",
        ["S06", "S08"],
        "Repeatable bytes may support bounded replay but cannot establish signer identity, authenticity, integrity governance, interoperability, or production security.",
    ),
    (
        "Stage-20 synthetic oscillator residual comparison board with blind-arm placeholders, matched budget, leakage quarantine, multiplicity ledger, and mandatory nonpromotion",
        "GMUT Mind",
        "completed",
        ["S04", "S05", "S09"],
        "The board must remain empty until preregistered governed real arms, calibrated references, appropriate statistics, safety monitoring, and independent review exist.",
    ),
    (
        "THOS zero-worker conservation-intake and stored-energy handover replay proxy with equal interruption budget, correction readback, and no safety-effectiveness estimate",
        "THOS Body",
        "represented",
        ["S01", "S02", "S03"],
        "A participant-free proxy can represent protocol structure only and cannot establish workload, safety, competence, operational effectiveness, or public protection.",
    ),
    (
        "Freed ID zero-key pseudonymous condition-note envelope with verifier-domain separation, scope, expiry, correction, revocation placeholders, and no credential",
        "Freed ID",
        "represented",
        ["S06", "S08"],
        "A zero-key envelope can represent claim separation only; issuance, proof, resolution, status, revocation, recovery, interoperability, and trust governance remain absent.",
    ),
    (
        "GMUT scalar-tensor clock-rate obligation lattice with conformal and disformal coupling slots, frame declaration, EFT domain, and zero predicted offset",
        "GMUT Mind",
        "represented",
        ["S09"],
        "Typed symbolic couplings must expose domain and frame vacancies and cannot yield a likelihood, posterior, constraint, force, rate shift, detection, or empirical confirmation.",
    ),
    (
        "GMUT oscillator-drift degeneracy register separating environmental covariates, reference instability, readout bias, and scalar-field placeholders without inference",
        "GMUT Mind",
        "represented",
        ["S04", "S05", "S09"],
        "Alternative explanations and missing observability must remain explicit; no synthetic residual can identify a field, mechanism, parameter, or Theory of Everything.",
    ),
    (
        "zero-call CCI, NPS, NIST, PROV-O, and WCAG crosswalk adapter with version pins, semantic conflicts, disabled transport, and zero object rows",
        "Trinity Mandala",
        "open_gap",
        ["S01", "S02", "S03", "S04", "S05", "S06", "S07"],
        "A disabled adapter exposes vocabulary conflicts only; ingestion, fitness, conformance, and interoperability remain open without authorized current rows and independent domain review.",
    ),
    (
        "horological treatment, stored-energy release, custody, ownership, heritage meaning, taonga, remedy, legal, cultural, affected-party, and Māori-authority docket",
        "CBR Heart",
        "exact_gate",
        ["S01", "S02", "S03"],
        "No software, source citation, or synthetic success can authorize treatment, actuation, release, custody, title, remedy, heritage interpretation, cultural legitimacy, or Māori authority.",
    ),
]


STARTUP_FAILURES = [
    (
        "CA6667-START-N001",
        "guessed-nonexistent-final-integrated-overview-path",
        "Enumerate the exact Sable owner paths and read reports/integrated-evidence-overview.md through EOF.",
    ),
    (
        "CA6667-START-N002",
        "archive-wide-canonical-receipt-digest-search-exceeded-bounded-time",
        "Stop the broad read-only search and use the phase-specific receipts directory named by the established archive convention.",
    ),
    (
        "CA6667-START-N003",
        "windows-rg-rejected-literal-wildcard-path-arguments",
        "Use exact literal files or rg --glob patterns rather than wildcard characters in Windows path arguments.",
    ),
    (
        "CA6667-START-N004",
        "canonical-receipt-projection-guessed-absent-invocation-state-keys",
        "Inspect the receipt root keys before projecting status, expected_final, post_success_replay_forbidden, and related actual fields.",
    ),
    (
        "CA6667-START-N005",
        "canonical-receipt-summary-guessed-json-python-and-valid-field-names",
        "Use json_parse_count, python_compile_count, and status after exact-key inspection; preserve the null projection at zero credit.",
    ),
    (
        "CA6667-START-N006",
        "proposal-and-successor-projection-guessed-row-identifier-and-category-fields",
        "Inspect row keys and use proposal_id, item_id, original_owner, original_phase, novelty_credit, and automatic_completion_credit.",
    ),
    (
        "CA6667-START-N007",
        "recursive-recent-receipt-enumeration-persisted-beyond-its-bound",
        "Stop only the verified read-only enumeration process and use the observed phase-specific receipt directory.",
    ),
    (
        "CA6667-START-N008",
        "first-web-result-wrapper-assumed-content-blocks-and-emitted-no-attributable-output",
        "Serialize the installed web tool result directly and retain only official or primary sources relevant to the bounded lens.",
    ),
]


OWNER_SAFE = [
    "render twenty frozen horological contracts",
    "execute one hundred preregistered rejecting mutations",
    "validate component topology vacancies",
    "validate stored-energy isolation holds",
    "validate escapement event-order placeholders",
    "validate zero-sample timebase ledgers",
    "validate synthetic gear arithmetic",
    "validate bitemporal association corrections",
    "validate zero-image condition vocabulary",
    "validate interface custody reservations",
    "validate silent strike-state defaults",
    "validate transport exposure abstention",
    "validate accessible topology structure",
    "validate civil-time rule vacancies",
    "validate deterministic event journals",
    "validate Stage-20 nonpromotion",
    "validate THOS proxy-only labeling",
    "validate Freed ID zero-key labeling",
    "validate GMUT coupling-domain vacancies",
    "validate GMUT degeneracy retention",
    "validate zero-call crosswalk openness",
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

SUCCESSOR_SAFE = [
    "revalidate Caelen horological contracts at zero novelty credit",
    "revalidate all retained negative witnesses",
    "preserve stored-energy and treatment authority holds",
    "preserve the zero-call crosswalk gap",
    "extend component-topology mutation coverage",
    "extend timebase uncertainty vacancies",
    "extend accessible topology summaries",
    "extend event-journal conflict fixtures",
    "extend Method Flow recurrence guards",
    "extend exact Git-blob manifest replay",
    "preserve x1 immutability checks",
    "preserve one-success canonical discipline",
    "preserve same-owner evidence boundaries",
    "preserve privacy and route confidentiality",
    "preserve synthetic-only data boundaries",
    "preserve no-conformance language",
    "preserve no-professional-authority language",
    "preserve no-Māori-authority language",
    "preserve NOT_READY_FOR_STAGE_20",
    "prepare one exact next edge only after terminal validation",
]

OWNER_CANDIDATES = [
    "participant-free handover timing proxy",
    "zero-key condition-note envelope",
    "symbolic scalar-tensor clock-rate lattice",
    "oscillator-drift degeneracy register",
    "zero-call standards crosswalk",
    "synthetic timebase uncertainty budget",
    "synthetic vibration quarantine model",
    "static accessibility structure",
    "synthetic event-journal replay",
    "synthetic civil-time semantics",
    "synthetic component dispute graph",
    "synthetic custody reservation",
    "synthetic condition-term registry",
    "synthetic matched-budget design board",
    "target-neutral successor recommendation ledger",
]

SUCCESSOR_CANDIDATES = [f"successor candidate: {row}" for row in OWNER_CANDIDATES]

EXACT_ITEMS = [
    "real object treatment approval",
    "stored-energy release approval",
    "custody or ownership decision",
    "professional conservation or repair decision",
    "real calibration or traceability claim",
    "affected-party access or remedy decision",
    "legal interpretation or ratification",
    "cultural or heritage meaning decision",
    "Māori wording, data governance, or authority decision",
    "Stage 20 authority or proof claim",
]

BLOCKED_ITEMS = [
    "real workshop operation without competent authority",
    "production identity issuance without keys and governance",
    "empirical GMUT claim without real governed evidence",
    "participant THOS effectiveness claim without approved arms",
    "cultural or Māori decision without affected and Māori authorities",
]

OWNER_SKILLS = [
    "horological-component-topology-vacancy",
    "stored-energy-isolation-abstention",
    "timebase-zero-sample-refusal",
    "gear-ratio-synthetic-closure",
    "movement-association-revision-boundary",
    "condition-vocabulary-zero-image",
    "horological-accessibility-structure",
    "clock-rate-gmut-domain-gate",
    "horological-method-flow",
    "horological-closeout-gate",
]

SUCCESSOR_SKILLS = [f"successor skill recommendation: {row}" for row in OWNER_SKILLS]

OWNER_RUNNERS = [
    "ghc_family_caelen_ash_v666_v7_contracts",
    "ghc_family_caelen_ash_v666_v7_mutations",
    "ghc_family_caelen_ash_v666_v7_json",
    "ghc_family_caelen_ash_v666_v7_privacy",
    "ghc_family_caelen_ash_v666_v7_security",
    "ghc_family_caelen_ash_v666_v7_accessibility",
    "ghc_family_caelen_ash_v666_v7_manifests",
    "ghc_family_caelen_ash_v666_v7_truth",
    "ghc_family_caelen_ash_v666_v7_closeout",
    "ghc_family_caelen_ash_v666_v7_canonical",
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
    "REFINE component vacancy messages",
    "REFINE stored-energy hold wording",
    "REFINE timebase uncertainty wording",
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
        proposal_id = f"CA6667-N{index:03d}"
        base = f"docs/caelen-ash/v666-v7/x2/proposals/{proposal_id.casefold()}"
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
                "primary_pillar": "GMUT Mind",
                "practice_lens": "wholly synthetic horological-conservation intake, movement-state provenance, stored-energy isolation, timebase uncertainty, correction-readback, accessibility, and handover documentation",
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
    if len(corpus) != 4290:
        raise RuntimeError(f"expected 4290 inherited rows, observed {len(corpus)}")
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
        "schema": "ghc.family.caelen-ash.v666-v7.novelty-audit.v1",
        "owner": "Caelen Ash",
        "phase": "v666-v7",
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
        "valid": not exact_collisions and not pair_collisions and len(corpus) == 4290,
        "interpretation": "Similarity is a screening signal, not proof of novelty. Each proposal also has a distinct movement, energy, escapement, timebase, ratio, association, condition, interface, strike, transport, accessibility, civil-time, serialization, model, proxy, identity, crosswalk, or authority-reservation invariant, falsifier, rollback, and protected-gate set.",
    }


def portfolio_rows(prefix: str, titles: list[str], approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"CA6667-{prefix}{index:02d}",
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
                "method_id": f"CA6667-START-M{index:03d}",
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
        "schema": "ghc.family.caelen-ash.v666-v7.method-flow-startup.v1",
        "owner": "Caelen Ash",
        "phase": "v666-v7",
        "generated_at_utc": NOW,
        "activation_source_repository_sealed_negatives": 26758,
        "activation_source_repository_sealed_methods": 11645,
        "successor_visible_external_negatives": 1,
        "successor_visible_external_methods": 1,
        "activation_baseline_negatives": 26759,
        "activation_baseline_methods": 11646,
        "new_startup_negative_count": len(rows),
        "new_startup_method_count": len(rows),
        "effective_after_x1_startup_negatives": 26759 + len(rows),
        "effective_after_x1_startup_methods": 11646 + len(rows),
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
            "original_owner": "Sable Rook",
            "original_phase": "v666-v6",
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
            "schema": "ghc.family.caelen-ash.v666-v7.relational-identity.v1",
            "owner": "Caelen Ash",
            "pronouns": "they/them",
            "relational_role": "relational uncertainty-and-handover cartographer",
            "relational_hope": "Make every boundary, missing witness, and reversible next step easier to see before structure is mistaken for authority.",
            "boundary": IDENTITY_BOUNDARY,
            "corrigibility": "Hamish may rename, pause, redirect, or stop this work.",
        },
    )
    write_json(
        "provenance/source-verification.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.source-verification.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7",
            "verified_at_utc": NOW,
            "source_branch": SOURCE_BRANCH,
            "source_sha": SOURCE_SHA,
            "source_parent_evidence_sha": SOURCE_EVIDENCE_SHA,
            "source_x1_sha": SOURCE_X1_SHA,
            "inherited_auren_sha": INHERITED_AUREN_SHA,
            "source_to_final_new_commit_count": 3,
            "source_to_final_merge_count": 0,
            "strict_x1_before_x2": True,
            "source_clean": True,
            "typed_ahead": 0,
            "typed_behind": 0,
            "local_equals_upstream_tracking_and_fresh_live": True,
            "committed_handoff_path": f"{SOURCE_PHASE_ROOT}/handoffs/next-owner-activation-candidate.md",
            "committed_handoff_blob_sha256": "41b0b1478d77bb178e9213945a5d6c0f7b94f32c05c4264813b8c00a1ae83c33",
            "committed_handoff_word_count": 528,
            "declared_external_canonical_receipt_sha256": "f5599700e622d2d44c8518124a52cf7d2896405385de7727152928c3879860e8",
            "lifecycle_manifest_replay": {
                "x1": {"observed": 20, "expected": 20, "commit": SOURCE_X1_SHA},
                "evidence": {"observed": 166, "expected": 166, "commit": SOURCE_EVIDENCE_SHA},
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
            "schema": "ghc.family.caelen-ash.v666-v7.source-profiles.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7",
            "generated_at_utc": NOW,
            "sources": SOURCE_PROFILES,
            "source_count": len(SOURCE_PROFILES),
            "claim_boundary": "sources provide vocabulary and refusal conditions only; they establish no object identity, condition, energy state, rate, calibration, conservation, repair, legal, standards-conformance, professional, cultural, Māori, custody, treatment, or release authority",
        },
    )
    write_json(
        "x1/phase-charter.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.phase-charter.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "branch": BRANCH,
            "lane": "one additive owner-only D-first sparse worktree",
            "primary_pillars": ["GMUT Mind"],
            "explicit_pillars": ["THOS Body", "Freed ID", "CBR Heart"],
            "practice": "wholly synthetic horological-conservation intake, movement-state provenance, stored-energy isolation, timebase uncertainty, correction-readback, accessibility, and handover documentation",
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
            "schema": "ghc.family.caelen-ash.v666-v7.source-ledger.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7",
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
            "schema": "ghc.family.caelen-ash.v666-v7.proposal-freeze.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7",
            "generated_at_utc": NOW,
            "frozen": True,
            "inherited_frozen_baseline": 4290,
            "genuinely_new_proposal_count": len(proposals),
            "new_frozen_total": 4290 + len(proposals),
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
            "schema": "ghc.family.caelen-ash.v666-v7.portfolio-freeze.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7",
            "generated_at_utc": NOW,
            "frozen": True,
            "counts": portfolio_counts,
            "minimums_satisfied": portfolio_counts == expected_portfolio_counts,
            "portfolios": portfolios,
            "x1_execution_count": 0,
            "claim_boundary": "planning-only portfolio; inherited and successor recommendations receive zero Caelen completion or novelty credit and exact or blocked items remain unexecuted",
        },
    )
    threat_rows = [
        ("CA6667-T01", "wrong source or mutable predecessor", "exact anchors, manifests, ancestry, clean state, and fresh live equality", "external receipts remain source evidence rather than Caelen completion"),
        ("CA6667-T02", "x2 implementation or outcomes enter x1", "path denylist, planning-only fields, and exact staged allowlist", "Git lifecycle discipline remains required"),
        ("CA6667-T03", "synthetic movement structure becomes professional assessment", "zero objects, measurements, images, operation, or treatment plus typed vacancies", "competent external horological and conservation authority remains absent"),
        ("CA6667-T04", "stored-energy language becomes mechanical instruction", "isolation-state labels only and explicit absence of winding, release, disassembly, or actuation steps", "real hazard assessment and control remain absent"),
        ("CA6667-T05", "timebase placeholders become calibration or traceability claims", "zero samples, missing reference chain, uncertainty vacancy, and explicit refusal", "real metrology evidence and responsibility remain absent"),
        ("CA6667-T06", "GMUT notation becomes empirical physics", "typed symbolic obligations, EFT domain, degeneracy register, and nonpromotion", "notation can invite overreading"),
        ("CA6667-T07", "THOS or Freed ID proxies become operational or production evidence", "represented-only labels, zero participants, zero keys, and missing-evidence ledgers", "governed trials and production trust evidence remain absent"),
        ("CA6667-T08", "legal, cultural, heritage, taonga, or Māori decisions are inferred", "exact gate and no real object, place, community, record, or authority case", "affected, competent, and Māori authorities remain absent"),
        ("CA6667-T09", "private route or person material enters artifacts", "synthetic fixtures, relative paths, and five-class scan", "pattern scans are bounded and incomplete"),
        ("CA6667-T10", "successful terminal validation is replayed or routing happens early", "exclusive receipt plus terminal-only live roster and exact-title reread", "opaque acknowledgement never authorizes a resend"),
    ]
    write_json(
        "x1/threat-model-plan.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.threat-model-plan.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7",
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
        f"""# Caelen Ash v666-v7 threat-model plan

{IDENTITY_BOUNDARY}

{PRACTICE_BOUNDARY}

## Scope

This owner-local model protects the additive Caelen delta. It is not a repository-wide audit, penetration test, external validation, conformance assessment, horological or conservation review, legal review, cultural review, Māori-authority review, or independent reproduction.

## Threat register

{threat_md}
""",
    )
    write_json(
        "x1/workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7",
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
            "schema": "ghc.family.caelen-ash.v666-v7.x1-checklist.v1",
            "complete": [
                "complete source packet and required guidance read through EOF",
                "exact source anchors, ancestry, manifests, receipt, clean state, and fresh equality verified",
                "all 4290 inherited proposal rows reconstructed",
                "twenty distinct proposals preregistered",
                "twenty Sable proposals selected for zero-credit revalidation",
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
            "schema": "ghc.family.caelen-ash.v666-v7.flashcard-architecture-freeze.v1",
            "owner": "Caelen Ash",
            "stable_prefix": ["identity", "claim boundary", "source anchors", "terminal verdict"],
            "volatile_suffix": ["final commit", "final receipt", "live successor route"],
            "tiers": {
                "tier1": ["owner relational card"],
                "tier2": ["three-pillar boundary cards"],
                "tier3": ["synthetic horological practice card"],
                "tier4": ["twenty proposal cards", "portfolio cards", "failure and gate cards", "validation and route cards"],
            },
            "x1_status": "architecture_only_no_cards_built",
        },
    )
    write_json(
        "wellbeing/x1-wellbeing-check.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.wellbeing-check.v1",
            "owner": "Caelen Ash",
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
    overview = f"""# Caelen Ash v666-v7 x1 integrated overview

{IDENTITY_BOUNDARY}

## Outcome first

This x1 candidate freezes a planning-only owner-local program from exact Sable Rook v666-v6 final `{SOURCE_SHA}`. It contains no x2 implementation, no observed outcome, no external action, no successor contact, and no Stage 20 promotion. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

GMUT Mind is primary. THOS Body and Freed ID/CBR Heart remain explicit and protected. {PRACTICE_BOUNDARY}

## Exact inherited truth

The read-first gate verified the exact source branch, three direct single-parent commits, zero merges, all 417 declared lifecycle-bound Git-blob manifest entries, the complete owner packet and handoff, clean 0/0 divergence, and equality across local, upstream, tracking, and a fresh live remote. Sable's successful canonical aggregate was not replayed. The complete repository suite was not run.

The immutable Sable repository seal contains 26,758 effective negatives, 11,645 Method Flow methods, 188 open gaps, and 186 exact gates. One later zero-credit routing discovery failure produces the activation baseline of 26,759 negatives and 11,646 methods without rewriting the seal. Eight Caelen startup and read-only projection failures are separately retained at zero credit, producing the x1 working overlay of 26,767 effective negatives and 11,654 methods.

## Novelty, portfolio, and sources

All 4,290 inherited proposal rows were reconstructed from exact committed Git objects. Twenty new titles have no exact inherited collision, every new pair remains below the 0.70 screening threshold, and each proposal has its own contract, falsifier, rollback, and gates. Expected dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`; these are preregistered expectations only. The twenty selected Sable proposals receive zero novelty and zero automatic completion credit.

The portfolio freezes 30 owner safe-now tasks, 20 successor safe recommendations, 15 owner candidates, 15 successor candidates, 10 exact approvals, 5 blocked packets, 10 owner and 10 successor skill plans, 10 owner and 10 successor runner plans, and 30 owner plus 30 successor CLEAN/FIX/REFINE tasks. X1 executes none of them, and no unsafe work is manufactured to meet a count.

Official CCI, NPS, NIST, W3C, RFC Editor, and primary scalar-tensor sources provide vocabulary and refusal conditions only. They create no object data, condition assessment, energy-state determination, rate measurement, calibration, traceability, treatment, professional, legal, cultural, Māori, accessibility-complete, privacy-complete, conformance, or independent-reproduction authority.

## Lifecycle and route

After exact staged review this x1 may be committed and pushed. X2 may begin only after x1 is clean, 0/0 divergent, and equal across local, upstream, tracking, and fresh live remote. Later validation remains owner-scoped and same-owner. One successful terminal validation must never be replayed. No successor may be contacted until the exact final terminal gate and fresh live authority, roster, and exact-title route rereads.
"""
    write_text("x1/x1-overview.md", overview)
    write_json(
        "x1/x1-build-receipt.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.x1-build-receipt.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_caelen_ash_v666_v7_x1.py",
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
    review_path = "docs/caelen-ash/v666-v7/validation/x1-staged-review.json"
    manifest_path = "docs/caelen-ash/v666-v7/validation/x1-content-manifest.json"
    allowed_exact = {
        "scripts/build_ghc_family_caelen_ash_v666_v7_x1.py",
        "tests/test_ghc_family_caelen_ash_v666_v7_x1.py",
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
        if not path.startswith("docs/caelen-ash/v666-v7/") and path not in allowed_exact
    ]
    post_x1 = [
        path
        for path in paths
        if any(
            path.startswith(f"docs/caelen-ash/v666-v7/{part}/")
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
    freeze = json.loads(index_blob("docs/caelen-ash/v666-v7/x1/proposal-freeze.json"))
    portfolio = json.loads(index_blob("docs/caelen-ash/v666-v7/x1/portfolio-freeze.json"))
    flow = json.loads(index_blob("docs/caelen-ash/v666-v7/method-flow/startup-method-flow.json"))
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "all_json_parse": True,
        "document_word_cap": maximum_words <= 100000,
        "expected_14_4_1_1": freeze["expected_disposition_counts"]
        == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "five_class_scan_zero_confirmed_hits": not candidates,
        "novelty_4290_valid": json.loads(
            index_blob("docs/caelen-ash/v666-v7/x1/novelty-audit.json")
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
        "schema": "ghc.family.caelen-ash.v666-v7.x1-staged-review.v1",
        "owner": "Caelen Ash",
        "phase": "v666-v7",
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
            "schema": "ghc.family.caelen-ash.v666-v7.content-manifest.v1",
            "owner": "Caelen Ash",
            "phase": "x1",
            "phase_label": "v666-v7",
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
            "usage: build_ghc_family_caelen_ash_v666_v7_x1.py [--staged-review]"
        )
    else:
        main()
