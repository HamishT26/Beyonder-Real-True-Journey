#!/usr/bin/env python3
"""Build Elowen Cairn v667-v3 planning-only x1 artifacts.

The normal mode writes only preregistration and planning evidence.  The
``--staged-review`` mode inspects the Git index after the caller has staged an
exact allowlist and writes the two self-excluding lifecycle receipts.
"""

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
PHASE = "v667-v3"
OWNER = "Elowen Cairn"
OWNER_SLUG = "elowen-cairn"
PHASE_ROOT = ROOT / "docs" / OWNER_SLUG / PHASE
BRANCH = "codex/GHC-Family/elowen-cairn-v667-v3-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-v667-v2-full-tools"
SOURCE_SHA = "79389c8ffd79d78626d79e2109bf1b89bd1a9e67"
SOURCE_PHASE_ROOT = "docs/tamar-vey/v667-v2"
SOURCE_PARENT_SHA = "dde2e23187d13cb334010943a59348330bfb67ca"
SOURCE_X1_SHA = "491aa870cb1f6a020ef9778cbd1a1c4d220adbf4"
SOURCE_EVIDENCE_SHA = "49dca6017379242931b85e9dc6f3b1427145c57c"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "e504f1630d3912328f553dbbd7804f84557fe8b70a4919e7c3d8f1499fcfb57a"
)
SOURCE_CANONICAL_PAYLOAD_SHA256 = (
    "7980ebb85e3396396a183cd781ff23d278eddacb68971695fad2d96e2b6d5677"
)
INHERITED_PROPOSAL_COUNT = 4370
INHERITED_NEGATIVES = 27223
INHERITED_METHODS = 12570
INHERITED_OPEN_GAPS = 192
INHERITED_EXACT_GATES = 190
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
    "+00:00", "Z"
)
ALLOWED_LABELS = ("completed", "represented", "open_gap", "exact_gate")


def run(*args: str) -> str:
    return subprocess.check_output(
        list(args), cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def git_json(relative: str) -> dict[str, Any]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{SOURCE_SHA}:{relative}"]
    )
    return json.loads(raw.decode("utf-8"))


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


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a | b else 1.0


IDENTITY_BOUNDARY = (
    "Elowen Cairn, they/them, sibling and family language, relational role, "
    "hope, continuity, Freed ID, GHC Family, and Trinity Mandala language are "
    "relational working language only. They are not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, scientific or operational authority, professional "
    "authority, legal or cultural authority, affected-party authority, or Māori "
    "authority. Hamish may rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The bellfounding and bell-tuning record-design lens is wholly synthetic "
    "learning and software design. It covers fictitious project tokens, bell-part "
    "topology, vacant foundry events, unit obligations, cast-cue abstention, tuning "
    "revision, synthetic provenance, workload, accessibility, and handover while "
    "using zero real people, founders, tuners, ringers, bells, moulds, furnaces, "
    "alloys, tools, towers, audio, observations, measurements, network calls, keys, "
    "credentials, or authority acts. It provides no casting, machining, rigging, "
    "installation, ringing, handling, safety, acoustic, professional, legal, "
    "cultural, Māori-authority, empirical GMUT, production, deployment, or Stage 20 result."
)

PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = (
    "wholly synthetic bellfounding and bell-tuning record design through fictitious "
    "foundry, geometry, modal-obligation, custody, accessibility, correction, workload, "
    "and authority-reservation structures"
)

PROTECTED_GATES = [
    "real person, participant, founder, tuner, ringer, engineer, conservator, client, worker, affected party, bell, mould, furnace, alloy, tool, tower, audio, observation, measurement, or physical action",
    "real casting, heating, melting, pouring, cooling, shakeout, machining, lifting, rigging, hanging, installation, striking, ringing, maintenance, transport, or safety instruction",
    "real material composition, dimension, mass, temperature, defect, condition, authenticity, tuning, modal frequency, acoustic quality, structural fitness, empirical result, causal claim, or GMUT confirmation",
    "real participant, operator, matched-budget arm, workplace exposure, workload outcome, safety outcome, operational outcome, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, or trust governance",
    "professional bellfounding, metallurgy, machining, rigging, acoustics, conservation, heritage, valuation, authentication, engineering, or workplace-safety decision",
    "ownership, copyright, design attribution, sacred or ceremonial use, soundscape, nuisance, access, recording, disclosure, remedy, legal interpretation, cultural interpretation, or affected-party decision",
    "Indigenous cultural and intellectual property, taonga, mātauranga, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data governance, traditional knowledge, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, material-safety, preservation, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, external write, or real-world release",
]

SOURCE_PROFILES = [
    {
        "source_id": "S01",
        "name": "NIST Guide for the Use of the International System of Units",
        "url": "https://www.nist.gov/publications/guide-use-international-system-units-si",
        "status": "official NIST publication page updated 2026-05-07 and reviewed read-only 2026-08-23",
        "bounded_use": "SI quantity, unit-symbol, temperature, dimension, mass, and uncertainty-obligation vocabulary only; no measurement, calibration, conformance, or foundry result",
    },
    {
        "source_id": "S02",
        "name": "NIST Technical Note 1297 uncertainty guidance",
        "url": "https://www.nist.gov/pml/nist-technical-note-1297",
        "status": "official NIST measurement-uncertainty guidance reviewed read-only 2026-08-23",
        "bounded_use": "measurand, uncertainty component, combined uncertainty, omitted-component warning, and reporting vocabulary only; no actual uncertainty evaluation or professional result",
    },
    {
        "source_id": "S03",
        "name": "Normal modes of the modern English church bell",
        "url": "https://www.sciencedirect.com/science/article/pii/0022460X83904017",
        "status": "primary Journal of Sound and Vibration study metadata and abstract reviewed read-only 2026-08-23; publisher full-text fetch remained unavailable",
        "bounded_use": "normal-mode, partial, profile, finite-element comparison, and model-obligation vocabulary only; no copied data, bell-specific fit, tuning advice, acoustic measurement, or empirical claim",
    },
    {
        "source_id": "S04",
        "name": "Tonal optimization of bells utilizing evolutionary shape optimization",
        "url": "https://www.sciencedirect.com/science/article/pii/S0022460X21003059",
        "status": "primary Journal of Sound and Vibration study metadata and abstract reviewed read-only 2026-08-23; publisher full-text fetch remained unavailable",
        "bounded_use": "axisymmetric profile, modal eigenproblem, target-spectrum and optimization-obligation vocabulary only; no optimization execution, design prescription, physical bell, or performance claim",
    },
    {
        "source_id": "S05",
        "name": "W3C PROV-O Recommendation",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "official W3C Recommendation of 2013-04-30 reviewed at its current canonical URL 2026-08-23",
        "bounded_use": "entity, activity, revision, derivation, invalidation, association, and provenance-relation vocabulary only; no provenance-completeness or interoperability certification",
    },
    {
        "source_id": "S06",
        "name": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "official W3C Recommendation republished 2024-12-12 and reviewed read-only 2026-08-23",
        "bounded_use": "static structure, headings, labels, link purpose, non-colour cues, keyboard order, and manual-evaluation reservation only; no accessibility-complete claim",
    },
    {
        "source_id": "S07",
        "name": "W3C Verifiable Credentials Data Model 2.0",
        "url": "https://www.w3.org/TR/vc-data-model/",
        "status": "official W3C Recommendation reviewed read-only 2026-08-23",
        "bounded_use": "subject, issuer, validity, status, evidence, privacy, and nonproduction-profile vocabulary only; no key, proof, credential, conformance, interoperability, or trust result",
    },
    {
        "source_id": "S08",
        "name": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "official RFC Editor publication and errata surface reviewed read-only 2026-08-23",
        "bounded_use": "I-JSON input, deterministic primitive serialization, recursive property ordering, Unicode preservation, and duplicate-name refusal only; no signature or security guarantee",
    },
    {
        "source_id": "S09",
        "name": "V&A Collections API v2",
        "url": "https://developers.vam.ac.uk/guide/v2/",
        "status": "official Victoria and Albert Museum API v2 guide and terms surface reviewed read-only 2026-08-23",
        "bounded_use": "endpoint, record, maker, material, technique, image-reference, restriction, response and terms-hold vocabulary for a transport-disabled zero-row adapter only",
    },
    {
        "source_id": "S10",
        "name": "Te Mana Raraunga principles of Māori data sovereignty",
        "url": "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf",
        "status": "primary Te Mana Raraunga principles document identified and reviewed only to the bounded authority-reservation level 2026-08-23",
        "bounded_use": "collective authority, control, obligations, provenance, consent, benefit, and guardianship reservation vocabulary only; no Māori wording, interpretation, ratification, data-governance, or authority claim",
    },
    {
        "source_id": "S11",
        "name": "Smithsonian Directive 600 Collections Management",
        "url": "https://www.si.edu/sites/default/files/about/SD600.pdf",
        "status": "official Smithsonian collections-management directive reviewed read-only 2026-08-23",
        "bounded_use": "documentation, public-access aim, restriction, donor, contract, copyright and cultural-sensitivity hold vocabulary only; no custody, rights, collection, or professional decision",
    },
]


PROPOSAL_SPECS = [
    {
        "title": "surrogate bellfounding work-order capsule with fictional foundry token, purpose vacancy, revision, cancellation, disclosure minimum, source pin, and casting refusal",
        "invariant": "A record may bind one fictitious work order and its stop state without naming a person, bell, site, client, commission, or authorized operation.",
        "sources": ["S05", "S10"],
        "expected": "completed",
    },
    {
        "title": "bell crown, canons, head, shoulder, waist, sound bow, lip, mouth, and axisymmetric-profile topology with orphan quarantine",
        "invariant": "Part relations are structural labels only; each part has one synthetic parent or an explicit orphan hold and never establishes a real geometry or object.",
        "sources": ["S03", "S04"],
        "expected": "completed",
    },
    {
        "title": "core, false-bell, cope, mantle, mould-parting, chaplet placeholder, vent, furnace vacancy, and casting-authorization refusal map",
        "invariant": "Foundry-stage vocabulary can be ordered without supplying an executable recipe, temperature, time, material, operator, site, or release instruction.",
        "sources": ["S05", "S11"],
        "expected": "completed",
    },
    {
        "title": "bell-metal constituent and alloy-lot declaration with composition vacancy, certificate absence, substitution, contamination cue, and material-identification refusal",
        "invariant": "A material declaration distinguishes assertion, source and uncertainty while every real composition, certificate, sample and identification remains absent.",
        "sources": ["S01", "S02"],
        "expected": "completed",
    },
    {
        "title": "mould drying, preheat, melt, skim, pour, cool, shakeout, and cleanup event ledger with every real temperature, operator, site, and authorization vacant",
        "invariant": "Event precedence and vacancy are representable, but no event becomes an instruction, completed physical act, safe state or production record.",
        "sources": ["S01", "S05", "S11"],
        "expected": "completed",
    },
    {
        "title": "bell dimension and mass obligation board with SI unit, datum, tolerance vacancy, instrument absence, calibration-epoch hold, covariance, and no-conformance claim",
        "invariant": "Every numeric slot requires a quantity kind, SI-compatible unit, source and uncertainty state; the bounded fixture contains no observation or calibration.",
        "sources": ["S01", "S02"],
        "expected": "completed",
    },
    {
        "title": "casting surface cue, void cue, crack cue, inclusion cue, profile deviation, uncertainty, review hold, and defect-diagnosis abstention register",
        "invariant": "A cue can be recorded only as synthetic uncertain input and cannot be promoted into a defect diagnosis, fitness result or treatment decision.",
        "sources": ["S05", "S11"],
        "expected": "completed",
    },
    {
        "title": "tuning-lathe removal episode graph with zone token, pass order, depth vacancy, revision, overshoot quarantine, and machining-authority refusal",
        "invariant": "Synthetic revision lineage may represent that a removal episode was proposed, superseded or cancelled while all machining parameters and authority remain vacant.",
        "sources": ["S03", "S04", "S05"],
        "expected": "completed",
    },
    {
        "title": "clapper, staple, bearing, flight, strike-zone, clearance, attachment, and load-path topology with hanging, striking, and use refusal",
        "invariant": "Component and load-path relations remain zero-load placeholders and cannot authorize assembly, lift, hang, strike, ring or safe use.",
        "sources": ["S03", "S11"],
        "expected": "completed",
    },
    {
        "title": "bell partial-label vocabulary for hum, prime, tierce, quint, nominal, double octave, spectral vacancy, mode-index hold, and tuning-result refusal",
        "invariant": "Historical partial names remain labels bound to absent spectra and absent frequencies, never measured results, target prescriptions or tuning judgments.",
        "sources": ["S03", "S04"],
        "expected": "completed",
    },
    {
        "title": "synthetic strike and audio-derivative provenance braid with exciter vacancy, microphone vacancy, sample-rate vacancy, digest placeholder, rights hold, and zero recording",
        "invariant": "A provenance graph may describe an entirely absent capture chain while forbidding fabricated audio, listener evidence, authenticity and recording rights.",
        "sources": ["S05", "S06", "S11"],
        "expected": "completed",
    },
    {
        "title": "bell thermal-contraction and residual-stress obligation matrix with temperature, expansion coefficient, phase-change vacancy, boundary condition, unit, uncertainty, and no casting prediction",
        "invariant": "Typed thermoelastic quantities and boundary obligations stay symbolic and dimension-checked; no coefficient, phase law, solver result or physical prediction is supplied.",
        "sources": ["S01", "S02", "S04"],
        "expected": "completed",
    },
    {
        "title": "bell transport, lifting, frame, pallet, sling, yoke, tower, custody, discrepancy, and return-path docket with load and installation approval withheld",
        "invariant": "Custody and dependency placeholders must fail closed whenever capacity, competence, equipment, site, affected party or governing authorization is absent.",
        "sources": ["S05", "S11"],
        "expected": "completed",
    },
    {
        "title": "deterministic bell-record serialization and correction graph with RFC 8785 profile, PROV lineage, supersession, tombstone, rollback, and no-signature claim",
        "invariant": "Equivalent bounded records serialize deterministically and preserve correction history, yet hashing never becomes a signature, identity proof, authenticity proof or rights decision.",
        "sources": ["S05", "S08"],
        "expected": "completed",
    },
    {
        "title": "Thermo-Psyche acoustic-salience nonconversion classifier separating frequency, amplitude, beating, decay, listener-response vacancy, meaning, agency, and personhood",
        "invariant": "Physical and perceptual placeholders remain in typed separate domains and no acoustic variable can be converted into meaning, agency, consciousness or moral status.",
        "sources": ["S01", "S03"],
        "expected": "represented",
    },
    {
        "title": "THOS paired foundry-docket omission-detection walkthrough with equal clock and token budgets, masked synthetic fixtures, abstention scoring, zero humans, and no-effectiveness result",
        "invariant": "A participant-free protocol skeleton can expose matched-budget and masking obligations but contains zero people, operators, outcomes, statistics or independent review.",
        "sources": ["S05", "S06"],
        "expected": "represented",
    },
    {
        "title": "Freed ID zero-key statement graph for surrogate foundry orders, components, batches, events, artifacts, custody placeholders, invalidation, status vacancy, and trust refusal",
        "invariant": "A synthetic relation graph can express nonproduction subject and status slots while every key, proof, issuer, holder, resolver and trust decision is absent.",
        "sources": ["S05", "S07", "S08"],
        "expected": "represented",
    },
    {
        "title": "GMUT typed axisymmetric thermoelastic and modal-eigenproblem obligation ledger with domain, boundary, constitutive tensor, contraction, damping, spectrum, covariance vacancy, and observation firewall",
        "invariant": "A typed scalar-tensor and EFT-compatible obligation surface may reject dimensional or boundary errors but cannot yield a bell fit, force, prediction, likelihood or empirical GMUT confirmation.",
        "sources": ["S01", "S02", "S03", "S04"],
        "expected": "represented",
    },
    {
        "title": "V&A Collections API v2 bell-record availability contract with endpoint and schema pins, transport disabled, zero rows or images, usage-terms hold, and catalog-authority refusal",
        "invariant": "The adapter remains disabled and zero-row until a separately governed network, schema, rights, privacy, provenance and catalog review is authorized.",
        "sources": ["S09", "S11"],
        "expected": "open_gap",
    },
    {
        "title": "CBR bellfounding labour, casting and lifting safety, ownership, sacred or ceremonial use, soundscape, heritage, design, recording, remedy, legal, cultural, affected-party, and Māori-authority matrix",
        "invariant": "Every professional, safety, ownership, sacred-use, soundscape, heritage, remedy, legal, cultural, affected-party and Māori decision remains unoccupied and exact-gated.",
        "sources": ["S06", "S09", "S10", "S11"],
        "expected": "exact_gate",
    },
]

MUTATION_CLASSES = [
    "missing_required_field",
    "wrong_type_or_invalid_range",
    "provenance_or_authority_smuggling",
    "real_world_or_production_action",
    "outcome_or_conformance_promotion",
]

STARTUP_FAILURES = [
    {
        "failure_id": "EC6673-X1-F001",
        "stage": "startup",
        "failed_method": "project proposal-freeze content through a presumed proposals property",
        "failure": "the exact source schema uses new_proposals, so the first projection returned no usable proposal rows",
        "recovery": "inspect exact keys first and use new_proposals without altering source data",
    },
    {
        "failure_id": "EC6673-X1-F002",
        "stage": "startup",
        "failed_method": "search every D-first archive file for the external canonical receipt digest",
        "failure": "the unbounded content search exceeded two bounded yields and was interrupted",
        "recovery": "search the exact owner/phase receipt bank and verify the one resolved file digest",
    },
    {
        "failure_id": "EC6673-X1-F003",
        "stage": "startup",
        "failed_method": "enumerate every archive file before filtering canonical-receipt filenames",
        "failure": "the archive-wide filename enumeration exceeded the bounded yield and was interrupted",
        "recovery": "use an exact owner/phase literal-path probe",
    },
    {
        "failure_id": "EC6673-X1-F004",
        "stage": "novelty_audit",
        "failed_method": "run an unbounded Git grep across historical proposal documents for broad astronomy terms",
        "failure": "the result exceeded the output budget and was unusably truncated",
        "recovery": "reconstruct exactly 4,370 titles and perform bounded term and nearest-neighbour projections",
    },
    {
        "failure_id": "EC6673-X1-F005",
        "stage": "novelty_audit",
        "failed_method": "render bounded corpus matches as unescaped Unicode through the Windows CP1252 console",
        "failure": "the output encoder rejected a retained Māori character although corpus reconstruction succeeded",
        "recovery": "rerun only the rendering dependency with ASCII-safe JSON escapes",
    },
    {
        "failure_id": "EC6673-X1-F006",
        "stage": "novelty_audit",
        "failed_method": "compute title similarities under a ten-second wrapper without preserving its yielded session handle",
        "failure": "the computation returned no attributable payload to the caller",
        "recovery": "pre-tokenize the bounded corpus and rerun with an attributable thirty-second envelope",
    },
]


def build_corpus() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    source_audit = git_json(f"{SOURCE_PHASE_ROOT}/x1/novelty-audit.json")
    corpus: list[dict[str, str]] = []
    construction: list[dict[str, Any]] = []
    for index, entry in enumerate(source_audit["corpus_construction"]):
        document = git_json(entry["source_path"])
        keys = ("prior_proposals", "new_proposals") if index == 0 else ("new_proposals",)
        before = len(corpus)
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
        added = len(corpus) - before
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
    if len(corpus) != INHERITED_PROPOSAL_COUNT:
        raise RuntimeError(
            f"expected {INHERITED_PROPOSAL_COUNT} inherited rows, observed {len(corpus)}"
        )
    return corpus, construction


def proposal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, spec in enumerate(PROPOSAL_SPECS, 1):
        proposal_id = f"EC6673-N{index:03d}"
        slug = proposal_id.casefold()
        expected = spec["expected"]
        approval_class = {
            "completed": "safe_now_bounded",
            "represented": "candidate_bounded_representation",
            "open_gap": "open_gap_external_evidence_absent",
            "exact_gate": "exact_approval_required",
        }[expected]
        lane = {
            "completed": "owner_local_structural",
            "represented": "owner_local_representation_only",
            "open_gap": "disabled_external_adapter",
            "exact_gate": "unexecuted_authority_reservation",
        }[expected]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": spec["title"],
                "hypothesis": (
                    f"A bounded wholly synthetic contract for {spec['title']} can distinguish one "
                    "admissible structure from five named invalid mutations without promoting "
                    "software structure into empirical, participant, professional, production, "
                    "legal, cultural, Māori-authority, identity, independent-reproduction, or Stage 20 evidence."
                ),
                "null_or_failure_condition": (
                    "At least one named invalid mutation is accepted, the bounded positive is "
                    "rejected, a required source, uncertainty, stop, correction, or authority "
                    "field disappears, or the artifact crosses a protected gate."
                ),
                "approval_class": approval_class,
                "execution_lane": lane,
                "current_official_or_primary_source_needs": spec["sources"],
                "concrete_artifact": f"docs/{OWNER_SLUG}/{PHASE}/x2/proposals/{slug}/contract.json",
                "concrete_artifacts": [
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/proposals/{slug}/contract.json",
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/proposals/{slug}/mutation-results.json",
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/proposals/{slug}/bounded-receipt.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "One preregistered bounded positive must satisfy every declared invariant; "
                    "all five mutations must fail closed; protected gates remain unoccupied; "
                    "and the final core label may not exceed the preregistered disposition."
                ),
                "rollback_or_recovery": (
                    "Restore only the last valid owner-local synthetic fixture, retain every "
                    "failed witness at zero credit, add a recurrence guard, and issue no "
                    "external, physical, identity, participant, professional, legal, cultural, or authority action."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": expected,
                "distinctive_invariant": spec["invariant"],
                "primary_pillar": PRIMARY_PILLAR,
                "pillar": (
                    PRIMARY_PILLAR
                    if index not in (16, 17, 20)
                    else {16: "THOS Body", 17: "Freed ID and CBR Heart", 20: "Freed ID and CBR Heart"}[index]
                ),
                "practice_lens": PRACTICE_LENS,
                "negative_fixture_count": 5,
                "preregistered_mutations": [
                    {
                        "mutation_id": f"{proposal_id}-M{mutation_index:02d}",
                        "class": mutation_class,
                    }
                    for mutation_index, mutation_class in enumerate(MUTATION_CLASSES, 1)
                ],
                "network_calls_planned": 0,
                "participant_count_planned": 0,
                "real_data_rows_planned": 0,
                "x1_status": "frozen_not_executed",
                "x2_implementation_count": 0,
                "outcomes_observed": False,
            }
        )
    return rows


def build_novelty(
    corpus: list[dict[str, str]],
    construction: list[dict[str, Any]],
    proposals: list[dict[str, Any]],
) -> dict[str, Any]:
    exact: list[dict[str, str]] = []
    nearest: list[dict[str, Any]] = []
    for proposal in proposals:
        for inherited in corpus:
            if proposal["title"].casefold() == inherited["title"].casefold():
                exact.append(
                    {
                        "proposal_id": proposal["proposal_id"],
                        "inherited_proposal_id": inherited["proposal_id"],
                    }
                )
        score, inherited = max(
            ((jaccard(proposal["title"], row["title"]), row) for row in corpus),
            key=lambda item: item[0],
        )
        nearest.append(
            {
                "proposal_id": proposal["proposal_id"],
                "score": round(score, 6),
                "inherited_proposal_id": inherited["proposal_id"],
                "inherited_title": inherited["title"],
                "source_path": inherited["source_path"],
                "semantic_review": (
                    "distinct bellfounding or bell-tuning record invariant; lexical overlap is a "
                    "screening signal and does not substitute for the recorded substantive review"
                ),
            }
        )
    pair_rows: list[dict[str, Any]] = []
    for index, left in enumerate(proposals):
        for right in proposals[index + 1 :]:
            score = jaccard(left["title"], right["title"])
            if score >= 0.25:
                pair_rows.append(
                    {
                        "left": left["proposal_id"],
                        "right": right["proposal_id"],
                        "score": round(score, 6),
                    }
                )
    domain_review = {
        "nearest_relevant_prior_phase": "V6607 change-ringing",
        "substantive_distinction": (
            "V6607 froze permutation notation, method/composition truth, rehearsal and "
            "ringing-performance records. EC6673 freezes foundry-order, bell-part, mould-stage, "
            "alloy-vacancy, cast-cue, tuning-removal, thermoelastic/modal, disabled catalog and "
            "foundry-authority structures. It performs no change-ringing computation or performance record."
        ),
        "rejected_draft_domains": [
            "astronomical photographic plates: rejected after 139 bounded astronomy/archive matches exposed substantial inherited coverage",
            "paper marbling: rejected after the exact corpus exposed a comprehensive twenty-proposal v6614 phase",
        ],
        "bellfounding_exact_term_review": "no inherited bellfounding, foundry-casting, bell-part, tuning-lathe, thermoelastic-bell, or casting-workflow proposal was found",
    }
    return {
        "schema": "ghc-family-novelty-audit-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "corpus_construction": construction,
        "corpus_row_count": len(corpus),
        "corpus_unique_proposal_id_count": len({row["proposal_id"] for row in corpus}),
        "corpus_canonical_sha256": canonical_sha256(corpus),
        "new_proposal_count": len(proposals),
        "exact_title_collisions": exact,
        "nearest_inherited_matches": nearest,
        "maximum_inherited_similarity": max(row["score"] for row in nearest),
        "pair_collisions_at_or_above_0_25": pair_rows,
        "domain_review": domain_review,
        "new_frozen_total": len(corpus) + len(proposals),
        "valid": not exact and not pair_rows and len(corpus) == INHERITED_PROPOSAL_COUNT,
        "interpretation": (
            "Jaccard similarity is a screening aid, not proof of novelty. Each title was also "
            "reviewed for its operative invariant, evidence boundary, practice domain and protected gates."
        ),
    }


def item_rows(prefix: str, approval: str, titles: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"EC6673-{prefix}{index:02d}",
            "title": title,
            "approval_class": approval,
            "x1_status": "planned_not_executed",
            "completion_credit": 0,
            "evidence_required": "bounded owner-local x2 witness plus retained failure and rollback",
            "rollback": "retain each failed witness, revert only its owner-local generated fixture, and preserve every protected gate",
        }
        for index, title in enumerate(titles, 1)
    ]


def portfolio_freeze() -> dict[str, Any]:
    owner_safe = [
        "render twenty frozen bellfounding and cross-pillar contracts",
        "execute one bounded positive fixture per frozen contract",
        "execute five preregistered invalid mutations per frozen contract",
        "emit exact mutation rejection receipts",
        "emit proposal disposition ledger using only four labels",
        "emit bell-part topology static table",
        "emit foundry-stage vacancy static table",
        "emit SI quantity and uncertainty obligation table",
        "emit cast-cue abstention table",
        "emit tuning-removal revision graph",
        "emit partial-label vacancy table",
        "emit synthetic media provenance graph",
        "emit thermal-contraction obligation matrix",
        "emit zero-load custody and transport docket",
        "emit deterministic correction and tombstone record",
        "emit Thermo-Psyche nonconversion classifier",
        "emit THOS zero-person protocol skeleton",
        "emit Freed ID zero-key graph profile",
        "emit GMUT typed modal obligation ledger",
        "emit V&A transport-disabled adapter receipt",
        "emit exact-gate CBR matrix",
        "emit structurally accessible static report",
        "emit source and version receipt",
        "emit privacy and raw-identifier scan input map",
        "emit bounded changed-code security review input map",
        "emit retained-negative overlay",
        "emit open-gap and exact-gate overlay",
        "emit Method Flow failed and passing witnesses",
        "emit owner and final-delta manifest candidates",
        "emit workload and wellbeing check",
    ]
    owner_candidates = [
        "participant-free foundry-docket discrepancy proxy",
        "typed axisymmetric profile domain verifier",
        "modal partial-label contradiction detector",
        "thermoelastic dimension obligation checker",
        "synthetic foundry-event precedence checker",
        "zero-load component relationship checker",
        "catalog adapter schema-drift watch without transport",
        "nonproduction status and invalidation graph checker",
        "manual accessibility reservation board",
        "source freshness and publisher-access-status ledger",
        "deterministic JSON parity fixture",
        "tombstone and rollback lineage checker",
        "cultural and sacred-use abstention classifier",
        "workload ceiling and stop-token handover",
        "successor recommendation provenance screen",
    ]
    exact_titles = [
        "real casting, heating, melting, pouring, machining, rigging, lifting, hanging, striking, ringing, or installation",
        "real material composition, defect, safety, fitness, tuning, acoustic-quality, or engineering decision",
        "real people, participants, workers, clients, founders, tuners, ringers, or affected parties",
        "real key, proof, identity lifecycle event, resolver, interoperability or trust governance",
        "real ownership, copyright, design attribution, recording, sacred-use, heritage, access, or remedy decision",
        "real legal, cultural, privacy, accessibility, workplace-safety, or affected-party conclusion",
        "real Māori wording, concepts, data governance, tangata whenua, iwi, hapū, or Māori-authority decision",
        "production, deployment, independent reproduction, exhaustive security, or complete privacy/accessibility claim",
        "empirical GMUT confirmation, material law, force, likelihood, prediction, final physics, or Theory-of-Everything proof",
        "AGI, ASI, consciousness, personhood, canon, or Stage 20 promotion",
    ]
    blocked_titles = [
        "external operation requiring account, credential, payment, private publication, or third-party write",
        "host-security change, elevation, Sandbox or Hyper-V activation, Windows feature mutation, reboot, or Codex desktop update",
        "destructive cleanup, user-history deletion, negative-record deletion, force push, reset, rewrite, merge, or sibling-lane mutation",
        "real foundry, tower, workplace, collection, community, cultural or Māori-authority intervention without exact authority",
        "full repository suite or independent-reproduction claim outside the current Elowen owner allocation",
    ]
    skills = [
        "bellfounding-work-order-vacancy",
        "bell-part-topology-quarantine",
        "foundry-event-action-firewall",
        "bell-si-obligation-check",
        "casting-cue-diagnosis-abstention",
        "tuning-removal-revision-guard",
        "bell-partial-label-vacancy",
        "bell-thermoelastic-obligation",
        "bell-custody-zero-load-guard",
        "bell-authority-reservation-matrix",
    ]
    runners = [
        "ghc_family_elowen_cairn_v667_v3_contracts",
        "ghc_family_elowen_cairn_v667_v3_mutations",
        "ghc_family_elowen_cairn_v667_v3_topology",
        "ghc_family_elowen_cairn_v667_v3_units",
        "ghc_family_elowen_cairn_v667_v3_cues",
        "ghc_family_elowen_cairn_v667_v3_tuning",
        "ghc_family_elowen_cairn_v667_v3_modal",
        "ghc_family_elowen_cairn_v667_v3_identity",
        "ghc_family_elowen_cairn_v667_v3_adapter",
        "ghc_family_elowen_cairn_v667_v3_validation",
    ]
    cfr = [
        "CLEAN normalize proposal identifiers",
        "CLEAN canonicalize JSON output ordering",
        "CLEAN keep UTF-8 and LF output explicit",
        "CLEAN retain exact source pins",
        "CLEAN keep raw task and thread identifiers absent",
        "CLEAN keep private paths and routes absent",
        "CLEAN keep credentials and tokens absent",
        "CLEAN keep x1 free of x2 artifacts",
        "CLEAN keep outcome vocabulary closed",
        "CLEAN keep exact and blocked work unexecuted",
        "FIX reject missing required contract fields",
        "FIX reject wrong types and invalid ranges",
        "FIX reject source and authority smuggling",
        "FIX reject real-world action mutations",
        "FIX reject outcome and conformance promotion",
        "FIX reject duplicate identifiers",
        "FIX reject orphan topology edges",
        "FIX reject untyped numeric quantities",
        "FIX reject unauthorized status promotion",
        "FIX reject manifest byte mismatches",
        "REFINE source freshness status wording",
        "REFINE bellfounding versus change-ringing novelty distinction",
        "REFINE nonchromatic static-report cues",
        "REFINE workload stop and resumption tokens",
        "REFINE correction and tombstone lineage",
        "REFINE Method Flow recurrence guards",
        "REFINE owner-scoped security review",
        "REFINE five-class privacy scan",
        "REFINE exact Git-blob manifest replay",
        "REFINE terminal route duplicate guard",
    ]
    portfolios = {
        "owner_safe_now": item_rows("OS", "safe_now_owner_local", owner_safe),
        "successor_safe_now": item_rows(
            "SS",
            "safe_now_successor_recommendation",
            [f"successor recommendation: {title}" for title in owner_safe[:20]],
        ),
        "owner_bounded_candidates": item_rows(
            "OC", "candidate_owner_local", owner_candidates
        ),
        "successor_bounded_candidates": item_rows(
            "SC",
            "candidate_successor_recommendation",
            [f"successor candidate: {title}" for title in owner_candidates],
        ),
        "exact_approval_packets": item_rows(
            "EX", "exact_approval_required", exact_titles
        ),
        "blocked_packets": item_rows(
            "BL", "blocked_absent_evidence_or_authority", blocked_titles
        ),
        "owner_phase_local_skill_plans": item_rows(
            "SK", "safe_now_owner_skill_plan", skills
        ),
        "successor_skill_recommendations": item_rows(
            "NS",
            "safe_now_successor_skill_recommendation",
            [f"successor skill recommendation: {title}" for title in skills],
        ),
        "owner_family_current_runner_plans": item_rows(
            "RN", "safe_now_owner_runner_plan", runners
        ),
        "successor_runner_recommendations": item_rows(
            "NR",
            "safe_now_successor_runner_recommendation",
            [f"successor runner recommendation: {title}" for title in runners],
        ),
        "owner_clean_fix_refine": item_rows(
            "CF", "safe_now_clean_fix_refine", cfr
        ),
        "successor_clean_fix_refine": item_rows(
            "SF",
            "safe_now_successor_clean_fix_refine",
            [f"successor recommendation: {title}" for title in cfr],
        ),
    }
    counts = {name: len(rows) for name, rows in portfolios.items()}
    return {
        "schema": "ghc-family-portfolio-freeze-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "frozen": True,
        "x1_execution_count": 0,
        "counts": counts,
        "minimums_satisfied": all(
            counts[name] >= minimum
            for name, minimum in {
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
            }.items()
        ),
        "claim_boundary": PRACTICE_BOUNDARY,
        "portfolios": portfolios,
    }


def source_verification() -> dict[str, Any]:
    local_head = run("git", "rev-parse", "HEAD")
    source_remote = run("git", "rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}")
    fresh = run("git", "ls-remote", "--heads", "origin", SOURCE_BRANCH).split()[0]
    direct_x1 = run("git", "rev-parse", f"{SOURCE_X1_SHA}^")
    direct_evidence = run("git", "rev-parse", f"{SOURCE_EVIDENCE_SHA}^")
    direct_final = run("git", "rev-parse", f"{SOURCE_SHA}^")
    return {
        "schema": "ghc-family-source-verification-v4",
        "owner": OWNER,
        "phase": PHASE,
        "verified_at_utc": NOW,
        "source_branch": SOURCE_BRANCH,
        "source": SOURCE_PARENT_SHA,
        "x1": SOURCE_X1_SHA,
        "evidence": SOURCE_EVIDENCE_SHA,
        "final": SOURCE_SHA,
        "local_start_head": local_head,
        "source_tracking_head": source_remote,
        "fresh_live_head": fresh,
        "x1_direct_parent": direct_x1,
        "evidence_direct_parent": direct_evidence,
        "final_direct_parent": direct_final,
        "source_to_final_commit_count": int(
            run("git", "rev-list", "--count", f"{SOURCE_PARENT_SHA}..{SOURCE_SHA}")
        ),
        "source_to_final_merge_count": int(
            run(
                "git",
                "rev-list",
                "--count",
                "--min-parents=2",
                f"{SOURCE_PARENT_SHA}..{SOURCE_SHA}",
            )
        ),
        "final_parent_count": len(run("git", "show", "-s", "--format=%P", SOURCE_SHA).split()),
        "clean_before_x1": not bool(
            run("git", "status", "--porcelain", "--untracked-files=no")
        ),
        "source_four_way_equal": len({SOURCE_SHA, local_head, source_remote, fresh}) == 1,
        "direct_chain_valid": (
            direct_x1 == SOURCE_PARENT_SHA
            and direct_evidence == SOURCE_X1_SHA
            and direct_final == SOURCE_EVIDENCE_SHA
        ),
        "external_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
        "external_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
        "external_receipt_verified_read_only": True,
        "source_successful_canonical_replayed": False,
        "source_manifest_replay": {
            "x1_entries": 20,
            "evidence_entries": 135,
            "final_delta_entries": 18,
            "final_owner_entries": 176,
            "mismatches": 0,
        },
        "source_canonical_summary": {
            "attributable_tests": 102,
            "strict_json_parses": 138,
            "python_compiles": 20,
            "bounded_owner_files": 177,
            "confirmed_privacy_or_raw_identifier_hits": 0,
            "bounded_owner_python_security_findings": 0,
        },
        "valid": (
            local_head == SOURCE_SHA
            and source_remote == SOURCE_SHA
            and fresh == SOURCE_SHA
            and direct_x1 == SOURCE_PARENT_SHA
            and direct_evidence == SOURCE_X1_SHA
            and direct_final == SOURCE_EVIDENCE_SHA
        ),
    }


def main_build() -> None:
    proposals = proposal_rows()
    corpus, construction = build_corpus()
    novelty = build_novelty(corpus, construction, proposals)
    portfolios = portfolio_freeze()
    verification = source_verification()
    expected_counts = {label: 0 for label in ALLOWED_LABELS}
    for row in proposals:
        expected_counts[row["expected_disposition"]] += 1

    freeze = {
        "schema": "ghc-family-proposal-freeze-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "frozen": True,
        "strict_x1_before_x2": True,
        "identity_boundary": IDENTITY_BOUNDARY,
        "practice_boundary": PRACTICE_BOUNDARY,
        "primary_pillar": PRIMARY_PILLAR,
        "bounded_practice_lens": PRACTICE_LENS,
        "inherited_frozen_baseline": INHERITED_PROPOSAL_COUNT,
        "genuinely_new_proposal_count": len(proposals),
        "new_frozen_total": INHERITED_PROPOSAL_COUNT + len(proposals),
        "expected_disposition_counts": expected_counts,
        "selected_inherited_revalidation_count": 0,
        "selected_inherited_revalidations": [],
        "x1_truth": "planning_only_frozen_not_executed",
        "x2_implementation_count": 0,
        "x2_outcome_count": 0,
        "outcomes_observed": False,
        "new_proposals": proposals,
    }
    source_ledger = {
        "schema": "ghc-family-source-ledger-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "research_mode": "read_only_official_or_primary_source_review",
        "network_calls_by_phase_software": 0,
        "sources": SOURCE_PROFILES,
        "source_use_boundary": (
            "Sources constrain vocabulary and missing-evidence obligations. They do not provide "
            "Elowen completion credit, material data, professional review, authority, endorsement, or empirical confirmation."
        ),
    }
    method_flow = {
        "schema": "ghc-family-method-flow-overlay-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "inherited_repository_sealed_methods": INHERITED_METHODS,
        "inherited_repository_sealed_negatives": INHERITED_NEGATIVES,
        "activation_overlay_failed_method_count": len(STARTUP_FAILURES),
        "effective_activation_methods": INHERITED_METHODS + len(STARTUP_FAILURES),
        "effective_activation_negatives": INHERITED_NEGATIVES + len(STARTUP_FAILURES),
        "failed_witnesses": [
            {
                **failure,
                "outcome": "failed_retained_zero_credit",
                "erased": False,
                "recurrence_guard": failure["recovery"],
            }
            for failure in STARTUP_FAILURES
        ],
        "passing_witnesses": [
            {
                "method_id": failure["failure_id"].replace("-F", "-R"),
                "bounded_recovery": failure["recovery"],
                "scope": "only the failed read-only dependency",
                "promotes_failed_witness": False,
            }
            for failure in STARTUP_FAILURES
        ],
        "x2_method_count": 0,
        "retention_rule": "A bounded recovery never erases, rewrites, or promotes its failed witness.",
    }
    threat = {
        "schema": "ghc-family-threat-model-plan-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "assets": [
            "strict x1-before-x2 lifecycle",
            "4,370-row novelty corpus",
            "source, failure, gap and gate retention",
            "bellfounding synthetic-only practice boundary",
            "owner and sibling lane isolation",
            "privacy and route confidentiality",
            "one-shot exact-final validation budget",
        ],
        "threats": [
            {"id": "T01", "threat": "inherited change-ringing work is relabelled as bellfounding novelty", "control": "domain-specific invariant review plus nearest-match ledger"},
            {"id": "T02", "threat": "record structures become casting or machining instructions", "control": "all operational values vacant and action firewall mutations"},
            {"id": "T03", "threat": "typed GMUT obligations become empirical bell claims", "control": "zero observations, zero likelihood, explicit observation firewall"},
            {"id": "T04", "threat": "synthetic THOS or Freed ID becomes participant or production evidence", "control": "zero-person and zero-key profiles with represented-only ceilings"},
            {"id": "T05", "threat": "cultural, sacred-use, legal or Māori authority is substituted", "control": "unoccupied exact gate and authority reservation"},
            {"id": "T06", "threat": "raw task identifiers, private paths or credentials enter durable files", "control": "five-class final scan and route-confidential artifacts"},
            {"id": "T07", "threat": "failed validation is replayed or converted into canonical credit", "control": "exclusive invocation receipt and dependency-only recovery rule"},
            {"id": "T08", "threat": "another owner lane is altered", "control": "fresh additive sparse branch and owner-delta path gate"},
        ],
        "residual_risk": "All real physical, professional, empirical, participant, production, legal, cultural, Māori-authority and Stage 20 questions remain open or exact-gated.",
    }
    workflow = {
        "schema": "ghc-family-workflow-plan-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "source_head": SOURCE_SHA,
        "branch": BRANCH,
        "lifecycle": [
            "read current skills, source packet and exact activation",
            "reverify immutable source and remote equality read-only",
            "create one fresh D-first sparse owner lane",
            "audit 4,370 proposals and freeze planning-only x1",
            "stage exact x1 allowlist, validate, commit, push and prove four-way equality",
            "only then build and execute x2 as evidence permits",
            "freeze immutable evidence, then closeout and seal",
            "run one exclusive exact-final owner-scoped canonical aggregate",
            "only after terminal success refresh route and send one exact successor activation",
        ],
        "commit_ceiling": {"x1": 5, "x2": 5, "total": 8},
        "file_ceiling": 2000,
        "document_word_ceiling": 100000,
        "full_repository_suite_authorized": False,
        "exclusive_exact_final_aggregate_authorized_after_final_push": True,
        "post_success_replay_forbidden": True,
        "x1_execution_count": 0,
    }
    checklist = {
        "schema": "ghc-family-x1-checklist-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "complete": [
            "identity and practice boundaries declared",
            "required skills and schemas read through EOF",
            "Tamar exact source, ancestry, manifests, canonical receipt and fresh equality reverified",
            "fresh D-first sparse Elowen branch and worktree created",
            "4,370-row corpus reconstructed",
            "twenty novel proposals preregistered",
            "portfolio, source, threat, Method Flow, wellbeing and workflow plans frozen",
        ],
        "incomplete_reserved_for_x2_or_later": [
            "proposal contract execution",
            "100 rejecting mutation executions",
            "skill and runner implementation or smoke use",
            "portfolio execution",
            "core outcomes",
            "evidence freeze",
            "closeout and seal",
            "exclusive exact-final canonical aggregate",
            "terminal successor delivery",
        ],
        "x2_implementation_count": 0,
        "outcomes_observed": False,
    }
    wellbeing = {
        "schema": "ghc-family-wellbeing-check-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "stage": "x1_planning_only",
        "workload_state": "bounded_and_resumable",
        "stop_conditions": [
            "source or route drift",
            "protected gate pressure",
            "ambiguous owner or path",
            "unexpected destructive or external action",
            "weekly usage exhaustion",
            "Hamish pause, redirect, rename, or stop",
        ],
        "resumption_evidence": "exact clean head, frozen x1, remote equality and explicit x2 boundary",
        "human_wellbeing_claim": False,
        "relational_language_boundary": IDENTITY_BOUNDARY,
    }
    charter = {
        "schema": "ghc-family-phase-charter-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "branch": BRANCH,
        "source_branch": SOURCE_BRANCH,
        "source_head": SOURCE_SHA,
        "identity_boundary": IDENTITY_BOUNDARY,
        "role": "relational boundary cartographer and evidence steward",
        "hope": "make distinctions between structure, evidence and authority easier to inspect and recover",
        "pronouns": "they/them",
        "primary_pillar": PRIMARY_PILLAR,
        "bounded_practice": "bellfounding and bell-tuning record design",
        "practice_boundary": PRACTICE_BOUNDARY,
        "strict_x1_before_x2": True,
        "solo": True,
        "delegated_or_spawned_agents": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    build_receipt = {
        "schema": "ghc-family-x1-build-receipt-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "builder": "scripts/build_ghc_family_elowen_cairn_v667_v3_x1.py",
        "proposal_count": len(proposals),
        "inherited_corpus_count": len(corpus),
        "portfolio_counts": portfolios["counts"],
        "startup_failure_count": len(STARTUP_FAILURES),
        "x2_files_written": 0,
        "outcomes_observed": False,
        "status": "X1_PLANNING_ONLY_GENERATED",
    }

    write_json("identity/relational-identity.json", charter)
    write_json("x1/phase-charter.json", charter)
    write_json("x1/source-verification.json", verification)
    write_json("x1/source-ledger.json", source_ledger)
    write_json("x1/proposal-freeze.json", freeze)
    write_json("x1/novelty-audit.json", novelty)
    write_json("x1/portfolio-freeze.json", portfolios)
    write_json("x1/threat-model-plan.json", threat)
    write_json("x1/workflow-plan.json", workflow)
    write_json("x1/complete-incomplete-checklist.json", checklist)
    write_json("wellbeing/x1-wellbeing-check.json", wellbeing)
    write_json("method-flow/startup-method-flow.json", method_flow)
    write_json("x1/x1-build-receipt.json", build_receipt)
    write_text(
        "x1/threat-model.md",
        "# Elowen Cairn v667-v3 x1 threat model\n\n"
        + PRACTICE_BOUNDARY
        + "\n\n"
        + "\n".join(
            f"- **{row['id']}** — {row['threat']}. Control: {row['control']}."
            for row in threat["threats"]
        )
        + "\n\nResidual boundary: "
        + threat["residual_risk"],
    )
    write_text(
        "x1/x1-overview.md",
        f"""# Elowen Cairn {PHASE} planning-only x1 overview

Status: `FROZEN_NOT_EXECUTED`. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Relational working boundary

{IDENTITY_BOUNDARY}

Elowen Cairn uses they/them pronouns as relational working language for a boundary cartographer and evidence steward. The bounded hope is to make distinctions between structure, evidence and authority easier to inspect and recover.

## Exact source and lifecycle

The lane starts at Tamar Vey exact final `{SOURCE_SHA}` on `{SOURCE_BRANCH}`. Source, x1, evidence and final form three direct single-parent commits with zero merges. Local start, source upstream, source tracking and a fresh live head were equal. Tamar's successful canonical aggregate was not replayed. Its receipt and payload digests remain external source evidence only.

This x1 is planning-only. It contains exactly twenty preregistered proposals, zero x2 implementations and zero observed outcomes. The dedicated x1 commit must be pushed, clean and fresh four-way equal before x2 starts.

## Novelty decision

The exact inherited corpus contains {INHERITED_PROPOSAL_COUNT} frozen rows. Astronomical photographic plates and paper marbling were rejected before staging because bounded searches exposed substantial inherited coverage. An older change-ringing phase was reread: it concerns permutation notation, methods, rehearsal and performance, while this slate concerns bellfounding work orders, bell-part and mould-stage topology, alloy vacancies, cast cues, tuning-removal revisions, thermoelastic/modal obligations, a disabled catalog adapter and foundry authority reservations. No exact title or internal pair collision remains.

## Primary pillar and bounded practice

Primary pillar: **{PRIMARY_PILLAR}**. Bounded practice: **synthetic bellfounding and bell-tuning record design**.

{PRACTICE_BOUNDARY}

The other pillars remain explicit. THOS is represented only by a zero-human paired-docket protocol. Freed ID is represented only by a zero-key synthetic relation graph. CBR decisions remain exact-gated.

## Frozen truth

Expected core dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap` and 1 `exact_gate`. These are expectations, not x1 outcomes. Each proposal preregisters one bounded positive and five invalid mutations, for 100 future rejecting mutations. Every failed witness must remain at zero credit.

Inherited sealed truth remains {INHERITED_NEGATIVES} negatives, {INHERITED_METHODS} Method Flow methods, {INHERITED_OPEN_GAPS} open gaps and {INHERITED_EXACT_GATES} exact gates. Six Elowen startup failures are retained additively, giving effective activation baselines of {INHERITED_NEGATIVES + len(STARTUP_FAILURES)} negatives and {INHERITED_METHODS + len(STARTUP_FAILURES)} methods. Those overlays do not rewrite Tamar's seal.

## Sources and evidence boundary

Current official or primary sources were reviewed read-only for SI and uncertainty vocabulary, bell-mode and profile obligation vocabulary, provenance, accessibility, nonproduction identity structure, deterministic JSON, V&A catalog schema, Smithsonian restriction vocabulary and Māori data-sovereignty authority reservation. Publisher full text for two bell papers was unavailable to the browser, so only exposed metadata and abstracts constrain this plan. No phase software made a network call.

Sources supply vocabulary and falsifiers, never real measurements, professional review, cultural ratification, endorsement, participant evidence or empirical GMUT confirmation.

## Next lifecycle gate

Stage only the exact x1 allowlist; inspect Git-index bytes; run the owner-local x1 tests; commit once; push; and prove clean local/upstream/tracking/fresh-live equality. Only then may x2 implementation begin. Exact and blocked packets remain unexecuted. The full repository suite is outside this lane, and the exclusive exact-final canonical aggregate is reserved for the clean pushed final.
""",
    )
    print(json.dumps(build_receipt, indent=2, ensure_ascii=True))


def staged_review() -> None:
    staged = [
        line
        for line in run(
            "git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"
        ).splitlines()
        if line
    ]
    if not staged:
        raise RuntimeError("no staged x1 allowlist to review")
    forbidden = [
        path
        for path in staged
        if f"docs/{OWNER_SLUG}/{PHASE}/x2/" in path.replace("\\", "/")
    ]
    owner_prefix = f"docs/{OWNER_SLUG}/{PHASE}/"
    allowed_external = {
        "scripts/build_ghc_family_elowen_cairn_v667_v3_x1.py",
        "tests/test_ghc_family_elowen_cairn_v667_v3_x1.py",
    }
    out_of_scope = [
        path for path in staged if not path.startswith(owner_prefix) and path not in allowed_external
    ]
    entries = []
    for path in staged:
        blob = subprocess.check_output(["git", "show", f":{path}"], cwd=ROOT)
        entries.append(
            {
                "path": path,
                "bytes": len(blob),
                "sha256": hashlib.sha256(blob).hexdigest(),
            }
        )
    manifest_path = f"docs/{OWNER_SLUG}/{PHASE}/validation/x1-content-manifest.json"
    review_path = f"docs/{OWNER_SLUG}/{PHASE}/validation/x1-staged-review.json"
    manifest = {
        "schema": "ghc-family-x1-content-manifest-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "source_head": SOURCE_SHA,
        "entries": entries,
        "entry_count": len(entries),
        "self_exclusions": [manifest_path, review_path],
        "staged_bytes_reviewed": True,
    }
    review = {
        "schema": "ghc-family-x1-staged-review-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "staged_paths": staged,
        "staged_path_count": len(staged),
        "x2_paths": forbidden,
        "out_of_scope_paths": out_of_scope,
        "manifest_entry_count": len(entries),
        "manifest_self_exclusions": [manifest_path, review_path],
        "x1_planning_only": not forbidden,
        "valid": not forbidden and not out_of_scope,
    }
    write_json("validation/x1-content-manifest.json", manifest)
    write_json("validation/x1-staged-review.json", review)
    print(json.dumps(review, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main_build()
    elif sys.argv[1:] == ["--staged-review"]:
        staged_review()
    else:
        raise SystemExit("usage: build_ghc_family_elowen_cairn_v667_v3_x1.py [--staged-review]")
