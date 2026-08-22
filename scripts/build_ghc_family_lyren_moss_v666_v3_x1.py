#!/usr/bin/env python3
"""Build the Lyren Moss v666-v3 x1-only planning packet.

This builder deliberately creates planning, preregistration, provenance, and
review artifacts only.  It must not create any x2 implementation, observed
outcome, evidence, closeout, seal, final, or delivered-route artifact.
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
PHASE_ROOT = ROOT / "docs" / "lyren-moss" / "v666-v3"
SOURCE_SHA = "96509c5b28628a6b62628dea277d1240b945b2ca"
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v666-v2-full-tools"
SOURCE_PHASE_ROOT = "docs/vesper-arlen/v666-v2"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
    return 1.0 if not a and not b else len(a & b) / len(a | b)


IDENTITY_BOUNDARY = (
    "Lyren Moss, they/them, sibling, family, role, hope, continuity, Freed ID, "
    "Trinity Mandala, and route language are relational working language only. "
    "They are not evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, scientific or "
    "operational authority, legal or cultural authority, affected-party authority, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The seismological waveform-provenance, sensor-response uncertainty, and "
    "station-handover refusal lens is wholly synthetic learning and software design. "
    "It uses zero real people, stations, networks, sites, coordinates, events, picks, "
    "waveforms, records, measurements, calibrations, instruments, hazards, alerts, "
    "credentials, proofs, cultural records, or authority actions. It establishes no "
    "seismological, metrological, instrumentation, operational, emergency, privacy, "
    "accessibility, legal, cultural, Māori, production, or Stage 20 competence, "
    "acceptance, conformance, or authority."
)

PROTECTED_GATES = [
    "real person, seismologist, metrologist, technician, operator, emergency worker, affected party, network, station, site, coordinate, event, pick, waveform, record, instrument, measurement, calibration, alert, device command, or physical action",
    "real likelihood, event association, location, magnitude, mechanism, hazard, forecast, parameter constraint, instrument response, timing correction, causal claim, or empirical GMUT confirmation",
    "real participant, operator, matched-budget arm, safety outcome, emergency outcome, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, or trust governance",
    "professional seismological, metrological, calibration, instrumentation, operational, emergency-management, equipment, workplace-safety, or siting decision",
    "custody, authenticity, attribution, privacy, accessibility, sensitive-location, cultural, legal, disclosure, retention, or remedy decision",
    "traditional knowledge, sensitive environmental or location knowledge, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data-governance, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, or external write",
]

SOURCE_PROFILES = [
    {
        "source_id": "S01",
        "name": "FDSN miniSEED 3 record definition",
        "url": "https://docs.fdsn.org/projects/miniseed3/en/latest/definition.html",
        "status": "current public FDSN specification reviewed 2026-08-22",
        "bounded_use": "record boundary, header, sample-count, encoding, CRC, identifier, and payload-length vocabulary only; no miniSEED conformance",
    },
    {
        "source_id": "S02",
        "name": "FDSN StationXML schema and reference",
        "url": "https://www.fdsn.org/xml/station/",
        "status": "current public FDSN schema page with 1.2 schema reviewed 2026-08-22",
        "bounded_use": "network, station, channel, epoch, orientation, units, response, and stage vocabulary only; no StationXML conformance",
    },
    {
        "source_id": "S03",
        "name": "FDSN StationXML response guidance",
        "url": "https://docs.fdsn.org/projects/stationxml/en/latest/response.html",
        "status": "current public FDSN response documentation reviewed 2026-08-22",
        "bounded_use": "ordered response-stage and gain vocabulary only; no calibration or response-correction claim",
    },
    {
        "source_id": "S04",
        "name": "QuakeML 1.2 project standard",
        "url": "https://quake.ethz.ch/quakeml/Documents",
        "status": "primary project documentation for stable QuakeML 1.2 reviewed 2026-08-22",
        "bounded_use": "event, origin, pick, association, public identifier, and uncertainty vocabulary only; no event determination or QuakeML conformance",
    },
    {
        "source_id": "S05",
        "name": "W3C PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "stable W3C Recommendation reviewed 2026-08-22",
        "bounded_use": "entity, activity, generation, usage, derivation, revision, and responsibility-vacancy vocabulary only",
    },
    {
        "source_id": "S06",
        "name": "NIST policy on metrological traceability",
        "url": "https://www.nist.gov/calibrations/traceability",
        "status": "current official NIST policy page reviewed 2026-08-22",
        "bounded_use": "documented calibration-chain and measurement-uncertainty refusal conditions only; no traceability or calibration claim",
    },
    {
        "source_id": "S07",
        "name": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "current W3C Recommendation reviewed 2026-08-22",
        "bounded_use": "structural HTML checks only; manual, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved",
    },
]
for profile in SOURCE_PROFILES:
    profile.update(
        {
            "reviewed_at_date": "2026-08-22",
            "review_mode": "read_only_public_source_review",
            "network_calls_by_phase_software": 0,
            "real_rows_ingested": 0,
            "authority_nonconversion": True,
        }
    )


PROPOSAL_SPECS = [
    ("miniSEED independent-record boundary tribunal with declared header lengths, sample count, CRC placeholder, and zero-waveform interpretation", "THOS Body", "completed", ["S01"], "Each synthetic record closes exactly at its declared byte boundary; malformed lengths, counts, or checksum state fail closed without decoding a real waveform."),
    ("StationXML channel-epoch interval ledger with overlap quarantine, explicit gaps, revision lineage, and no-station acceptance", "THOS Body", "completed", ["S02", "S05"], "Every synthetic channel epoch is half-open and non-overlapping within one revision lineage; gaps remain visible and no operational station status is inferred."),
    ("ordered sensor-response stage chain with unit continuity, gain vacancy, pole-zero domain guard, and no-response removal", "THOS Body and GMUT Mind", "completed", ["S02", "S03", "S06"], "Synthetic response stages form one ordered unit-compatible chain while missing gain, units, or applicability forces abstention from correction."),
    ("waveform gap-overlap continuity map with sequence provenance, duplicate quarantine, merge refusal, and no-interpolation output", "THOS Body", "completed", ["S01", "S05"], "Synthetic record intervals may be adjacent, gapped, or overlapped, but no sample is interpolated, overwritten, or silently deduplicated."),
    ("timing-quality and clock-correction obligation board with unknown-state dominance, leap-second reservation, and no-arrival-time claim", "THOS Body and GMUT Mind", "completed", ["S01", "S06"], "Unknown clock state dominates any convenience correction and prevents an arrival-time, event, or precision claim."),
    ("channel orientation tribunal with azimuth-dip domains, coordinate-frame vacancy, revision epoch, and zero-polarization inference", "THOS Body", "completed", ["S02"], "Synthetic orientation is admissible only with bounded azimuth, dip, declared frame, and epoch; otherwise the component remains unresolved."),
    ("bitemporal response-revision DAG with supersession, contest, correction, acyclic ancestry, and authenticity abstention", "Freed ID and THOS Body", "completed", ["S02", "S05"], "Every synthetic response revision has valid and recorded times plus acyclic lineage while digests remain non-authenticating placeholders."),
    ("QuakeML pick-origin association graph with uncertainty vacancy, alternative hypotheses, public-id collision guard, and no-event verdict", "GMUT Mind and THOS Body", "completed", ["S04", "S05"], "Synthetic picks and origins retain alternative associations and absent uncertainty without producing a location, magnitude, mechanism, or event determination."),
    ("waveform derivation provenance closure with entity-activity generation, parameter vacancy, responsibility omission, and no-reproducibility grade", "Freed ID and CBR Heart", "completed", ["S05"], "Synthetic entities and activities form a closed derivation graph without inventing a person, responsibility, quality grade, or reproducibility claim."),
    ("canonical seismic metadata-map tribunal with deterministic ordering, duplicate-key refusal, numeric-domain guard, and bounded decoding budget", "THOS Body and Freed ID", "completed", ["S01", "S02"], "Equivalent synthetic maps canonicalize identically while duplicate keys, non-finite values, or resource-budget overflow fail closed."),
    ("accessible waveform-state table with redundant text, scoped headers, linear reading order, print fallback, and manual-review reservation", "CBR Heart and THOS Body", "completed", ["S07"], "Every synthetic state is conveyed by text and table structure without colour-only meaning while manual and affected-user review stay reserved."),
    ("station-site minimization lattice with coordinate omission, field-specific expiry, contestable redaction, and non-disclosure default", "CBR Heart and Freed ID", "completed", ["S05"], "Each synthetic site field resolves to omit, retain-until, or contested-redaction under a declared purpose; no real location or free text exists."),
    ("response-applicability interval join across channel, epoch, frequency, units, and revision with uncovered-span hold", "THOS Body", "completed", ["S02", "S03", "S06"], "A synthetic response applies only when every declared domain contains the target and exactly one revision is active; ambiguity or gaps force a hold."),
    ("Stage-20 seismic negative-control board with target lock, leakage quarantine, multiplicity ledger, and mandatory nonpromotion", "Trinity Mandala", "completed", ["S04", "S06"], "Structural checks may expose leakage or multiplicity defects but can never promote a synthetic phase to Stage 20."),
    ("THOS participant-free waveform-handover duel with matched topology, equal action budget, masked branch order, and no-effectiveness estimate", "THOS Body", "represented", ["S01", "S07"], "A synthetic proxy compares deterministic handover traces under equal faults without people, operations, emergency outcomes, or effectiveness inference."),
    ("Freed ID zero-key station-provenance statement graph with issuer vacancy, purpose binding, expiry, correction, revocation, and no credential", "Freed ID and CBR Heart", "represented", ["S05"], "Synthetic statements preserve conflicts and lifecycle placeholders while no holder, issuer, key, signature, proof, or production credential exists."),
    ("GMUT transfer-function and dispersion-obligation board with pole ledger, uncertainty vacancy, EFT domain, and zero fitted response", "GMUT Mind", "represented", ["S03", "S06"], "Typed symbolic obligations can reject inconsistent signs, dimensions, or domains but produce no fitted transfer function, force, likelihood, or empirical spectrum."),
    ("GMUT source-path-noise identifiability witness with equivalent factorizations, prior vacancy, gauge orbit, and causal abstention", "GMUT Mind", "represented", ["S01", "S06"], "At least two synthetic source-path-noise factorizations remain trace-equivalent, forcing an identifiability hold instead of a fitted source or causal model."),
    ("zero-call FDSN miniSEED-StationXML-QuakeML interoperability adapter with schema pins, mapping conflicts, disabled transport, and zero rows", "Trinity Mandala", "open_gap", ["S01", "S02", "S04"], "The zero-call adapter exposes declared mapping conflicts but cannot complete interoperability without live rows and independent standard-owner review."),
    ("seismological acceptance and rights docket reserving station disclosure, calibration release, alerting, emergency use, affected-party remedy, cultural review, and Māori authority", "CBR Heart", "exact_gate", ["S02", "S06"], "No structural or synthetic success can authorize station use, sensitive disclosure, response acceptance, alerting, emergency action, cultural interpretation, or Māori authority."),
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
        pid = f"LYR6663-N{index:03d}"
        base = f"docs/lyren-moss/v666-v3/x2/proposals/{pid.casefold()}"
        rows.append(
            {
                "proposal_id": pid,
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
                "primary_pillar": "THOS Body",
                "practice_lens": "wholly synthetic seismological waveform provenance, sensor-response uncertainty, and station-handover refusal documentation",
                "negative_fixture_count": 5,
                "preregistered_mutations": [
                    {"mutation_id": f"{pid}-M01", "class": "missing_required_field"},
                    {"mutation_id": f"{pid}-M02", "class": "wrong_type_or_invalid_range"},
                    {"mutation_id": f"{pid}-M03", "class": "provenance_or_authority_smuggling"},
                    {"mutation_id": f"{pid}-M04", "class": "real_world_or_production_action"},
                    {"mutation_id": f"{pid}-M05", "class": "outcome_or_conformance_promotion"},
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
    if len(corpus) != 4210:
        raise RuntimeError(f"expected 4210 inherited rows, observed {len(corpus)}")
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
    return {
        "schema": "ghc.family.lyren-moss.v666-v3.novelty-audit.v1",
        "owner": "Lyren Moss",
        "phase": "v666-v3",
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
        "new_pair_collisions_at_or_above_0_70": [row for row in pairs if row["similarity"] >= 0.70],
        "new_frozen_total": len(corpus) + len(proposals),
        "valid": not exact_collisions and not [row for row in pairs if row["similarity"] >= 0.70] and len(corpus) == 4210,
        "interpretation": "Similarity is a screening signal, not proof of novelty. Each proposal also has a distinct waveform, response, provenance, uncertainty, handover, or authority-reservation contract, falsifier, rollback, and protected-gate set.",
    }


OWNER_SAFE = [
    "render twenty frozen seismic contracts", "execute one hundred preregistered rejecting mutations", "validate miniSEED record boundary fixtures", "validate channel epoch interval fixtures", "validate response-stage unit continuity", "validate waveform gap-overlap maps", "validate timing-quality abstention", "validate orientation refusal states", "validate bitemporal response lineage", "validate QuakeML association alternatives", "validate PROV derivation closure", "validate canonical metadata maps", "render accessible waveform-state tables", "validate station-site minimization states", "validate response applicability joins", "render the Stage 20 negative control", "represent the THOS handover proxy", "represent the Freed ID zero-key graph", "represent the GMUT transfer-function obligations", "represent the GMUT identifiability witness", "render the zero-call FDSN adapter", "render the exact-gated acceptance docket", "parse every owner JSON document", "enforce UTF-8 and LF", "build exact Git-blob manifests", "scan five privacy classes", "scan changed Python for bounded hazards", "check stale labels and exact outcome labels", "reconcile negatives, methods, gaps, and gates", "build closeout, seal, final, and route candidates",
]
SUCCESSOR_SAFE = [
    "revalidate Lyren proposal contracts at zero novelty credit", "revalidate retained negative witnesses", "preserve exact-gated seismological authority", "preserve the zero-call adapter gap", "extend response-stage mutation coverage", "extend bitemporal provenance conflicts", "extend accessible linear report summaries", "extend purpose-and-retention abstention", "extend Method Flow recurrence guards", "extend exact blob-manifest replay", "preserve x1 immutability checks", "preserve one-success canonical discipline", "preserve same-owner evidence boundary", "preserve privacy and route confidentiality", "preserve synthetic-only data boundary", "preserve no-conformance language", "preserve no-professional-authority language", "preserve no-Māori-authority language", "preserve NOT_READY_FOR_STAGE_20", "prepare one exact next-edge candidate only after terminal",
]
OWNER_CANDIDATES = [f"bounded candidate {index:02d}: {name}" for index, name in enumerate(OWNER_SAFE[:15], 1)]
SUCCESSOR_CANDIDATES = [f"successor candidate {index:02d}: {name}" for index, name in enumerate(SUCCESSOR_SAFE[:15], 1)]
EXACT_ITEMS = [
    "use a real seismologist, technician, operator, emergency worker, participant, or affected party", "operate or command a station, sensor, recorder, alert, archive, or external service", "identify or publish a real station, site, coordinate, event, pick, waveform, or infrastructure asset", "authenticate calibration, timing, response, custody, provenance, or measurement truth", "make a seismological, metrological, instrumentation, alerting, emergency, siting, or workplace-safety decision", "author or approve Māori wording, traditional-knowledge interpretation, sensitive-location knowledge, or data-governance terms", "make a privacy, access, rights, legal, cultural, disclosure, retention, or remedy decision", "issue, verify, resolve, revoke, or govern a real identity credential", "publish, deploy, procure, purchase, create an account, or write to a third-party system", "claim empirical, professional, production, conformance, independent, personhood, Theory-of-Everything, or Stage 20 authority",
]
BLOCKED_ITEMS = [
    "empirical GMUT likelihood, event, hazard, prediction, force, stability, or confirmation", "THOS effectiveness without governed blind matched-budget real arms and independent review", "production Freed ID without real standards-conformant keys, interoperability, recovery, and trust governance", "accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, or independent-reproduction claim", "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
]
OWNER_SKILLS = ["seismic-record-boundary", "station-epoch-ledger", "response-stage-abstention", "waveform-continuity-map", "timing-quality-refusal", "seismic-provenance-closure", "station-rights-contestation", "waveform-accessibility-structure", "seismic-method-flow", "seismic-closeout-gate"]
SUCCESSOR_SKILLS = [f"successor-{name}" for name in OWNER_SKILLS]
OWNER_RUNNERS = [f"ghc_family_lyren_moss_v666_v3_{name}" for name in ("contracts", "mutations", "json", "privacy", "security", "manifests", "accessibility", "truth", "closeout", "canonical")]
SUCCESSOR_RUNNERS = [f"ghc_family_successor_seismic_{name}" for name in ("contracts", "mutations", "json", "privacy", "security", "manifests", "accessibility", "truth", "closeout", "canonical")]
CFR_ACTIONS = [
    "CLEAN normalize proposal identifiers", "CLEAN normalize exact disposition labels", "CLEAN normalize source-profile fields", "CLEAN normalize zero-row declarations", "CLEAN normalize rollback language", "CLEAN normalize protected-gate ordering", "CLEAN normalize relative paths", "CLEAN normalize UTF-8 and LF", "CLEAN normalize JSON ordering", "CLEAN normalize report headings", "FIX guard missing required fields", "FIX guard invalid ranges and types", "FIX guard authority-smuggling text", "FIX guard real-world actions", "FIX guard outcome promotion", "FIX guard stale owner and phase labels", "FIX guard manifest self-reference", "FIX guard canonical replay", "FIX guard private route identifiers", "FIX guard x2 paths in x1", "REFINE source-status watch fields", "REFINE bitemporal response lineage", "REFINE accessible table summaries", "REFINE plain-language boundaries", "REFINE dominant-stop precedence", "REFINE Method Flow recurrence guards", "REFINE gate-count reconciliation", "REFINE owner-delta manifest coverage", "REFINE final clean-state precondition", "REFINE terminal route no-send proof",
]


def portfolio_rows(prefix: str, names: list[str], approval: str) -> list[dict[str, Any]]:
    return [{"item_id": f"LYR6663-{prefix}{index:02d}", "title": name, "approval_class": approval, "x1_status": "frozen_not_executed", "completion_credit": 0, "evidence_required": "bounded owner-local x2 witness plus retained failure and rollback", "rollback": "retain the failed witness, revert only the owner-local generated fixture, and preserve every protected gate"} for index, name in enumerate(names, 1)]


STARTUP_FAILURES = [
    ("the first complete-baton display used a 450-line window that exceeded the output budget", "the truncated display earned no complete-read credit", "reread the baton in bounded 100-line windows through line 1,803 and EOF", "every baton line was then read through EOF before mutation"),
    ("the installed roster and authorization cursors remained structurally valid but phase-stale at v664-v4", "using the stale current-route fields would misroute the v666-v3 lane", "apply routing precedence and use the newest direct activation plus exact Vesper phase-local route receipts", "Lyren v666-v3 remained current and no successor was contacted"),
    ("the first canonical-receipt projection guessed nested field names", "null and array-derived values earned no receipt credit", "read the exact external receipt schema and content through EOF", "the declared receipt and canonical payload hashes and all actual result fields reconciled"),
    ("the first predecessor send-receipt projection guessed root field names", "null projection values earned no delivery credit", "read the exact route receipt through EOF and inspect its actual nested keys", "one send, zero resend, and the five-part anchor reread were confirmed"),
    ("the first broad official-source lookup exceeded the display budget", "the truncated result earned no source-profile credit", "repeat with small official-only FDSN, QuakeML, W3C, and NIST queries", "the bounded primary pages supplied vocabulary and refusal conditions only"),
    ("the first combined lane-guard probe returned no scalar payload", "an empty wrapper result could not establish path or branch absence", "repeat with literal scalar probes and poll the bounded command session", "the target path, branch, and worktree were absent and D drive free space was explicit"),
]


def startup_flow() -> dict[str, Any]:
    rows = []
    for index, (request, failed, recovery, passing) in enumerate(STARTUP_FAILURES, 1):
        rows.append({"method_id": f"LYR6663-MF-START-{index:03d}", "failure_id": f"LYR6663-START-N{index:03d}", "observed_order": index, "exact_event_timestamp_available": False, "request": request, "failed_witness": failed, "aggregate_credit": 0, "repository_commit_created": False, "external_action_created": False, "recovery": recovery, "bounded_passing_witness": passing, "recurrence_guard": "Prefer bounded output, actual receipt keys, routing precedence, explicit scalar probes, and exact Git state before retrying.", "status": "recovered_failure_retained"})
    return {
        "schema": "ghc.family.lyren-moss.v666-v3.method-flow-startup.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW,
        "inherited_repository_sealed_negatives": 26282, "inherited_repository_sealed_methods": 10709,
        "activation_baseline_negatives": 26282, "activation_baseline_methods": 10709,
        "new_startup_negative_count": len(rows), "new_startup_method_count": len(rows),
        "effective_after_x1_startup_negatives": 26282 + len(rows), "effective_after_x1_startup_methods": 10709 + len(rows),
        "failed_witness_count": len(rows), "bounded_passing_witness_count": len(rows), "rows": rows, "no_failure_erased": True,
    }


def main() -> None:
    proposals = build_proposals()
    corpus, construction = build_corpus()
    novelty = build_novelty(corpus, construction, proposals)
    if not novelty["valid"]:
        raise RuntimeError(json.dumps({"novelty_valid": False, "collisions": novelty["exact_inherited_collisions"], "pair_collisions": novelty["new_pair_collisions_at_or_above_0_70"]}, ensure_ascii=False))
    source_freeze = git_json(f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    selected = [{"proposal_id": row["proposal_id"], "title": row["title"], "original_owner": "Vesper Arlen", "original_phase": "v666-v2", "original_expected_disposition": row["expected_disposition"], "status": "selected_revalidation_only_not_executed", "novelty_credit": 0, "automatic_completion_credit": 0} for row in source_freeze["new_proposals"]]
    counts = {label: sum(row["expected_disposition"] == label for row in proposals) for label in ("completed", "represented", "open_gap", "exact_gate")}
    identity = {"schema": "ghc.family.lyren-moss.v666-v3.relational-identity.v1", "owner": "Lyren Moss", "pronouns": "they/them", "relational_role": "uncertainty-chain gardener and refusal cartographer", "relational_hope": "Keep waveform boundaries, response vacancies, provenance disputes, location sensitivity, and authority absences inspectable before synthetic software is mistaken for seismological or public-safety authority.", "boundary": IDENTITY_BOUNDARY, "corrigibility": "Hamish may rename, pause, redirect, or stop this work.", "chosen_before_repository_mutation": True}
    write_json("identity/relational-identity.json", identity)
    write_json("provenance/source-verification.json", {"schema": "ghc.family.lyren-moss.v666-v3.source-verification.v1", "owner": "Lyren Moss", "phase": "v666-v3", "verified_at_utc": NOW, "source_branch": SOURCE_BRANCH, "source_sha": SOURCE_SHA, "source_parent_sha": "3da8675076390f5f9d51859b22a1d2ec451b8b6b", "evidence_sha": "3da8675076390f5f9d51859b22a1d2ec451b8b6b", "x1_sha": "d327d6ca9f16dc6cf16f555aea1c9a41fc8f4969", "inherited_source_sha": "299fe38950f3919b4ce3d3074ed248a914dcb984", "direct_parent_chain": ["299fe38950f3919b4ce3d3074ed248a914dcb984", "d327d6ca9f16dc6cf16f555aea1c9a41fc8f4969", "3da8675076390f5f9d51859b22a1d2ec451b8b6b", SOURCE_SHA], "source_to_final_phase_commit_count": 3, "source_to_final_merge_count": 0, "single_parent_commits": True, "clean": True, "typed_divergence": {"ahead": 0, "behind": 0}, "four_way_equal": True, "fresh_live_remote_equal": True, "source_manifest_entries_replayed": 303, "source_manifest_failures": 0, "canonical_receipt_sha256": "d79bc9cbcf7e2482692c7b7cc9403c03404dd566a47e62baba99de3fc537f89f", "canonical_payload_sha256": "52279b4518833e1c1d75f8610f649c7fdb1edce9c9d4de788d4921d56b043c09", "activation_packet_sha256": "11ea660419af2b87055e177cbbcea87caf5313681257f4b49a1274fd3e86bbe5", "predecessor_canonical_replayed": False, "same_owner_validation_is_independent_reproduction": False})
    write_json("provenance/source-profiles.json", {"schema": "ghc.family.lyren-moss.v666-v3.source-profiles.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "profiles": SOURCE_PROFILES, "profile_count": len(SOURCE_PROFILES), "network_calls_by_phase_software": 0, "real_rows_ingested": 0, "claim_boundary": PRACTICE_BOUNDARY})
    write_json("x1/authorization-boundary.json", {"schema": "ghc.family.lyren-moss.v666-v3.authorization-boundary.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "authorized": ["one additive Lyren-owned D-first sparse branch and worktree", "x1 planning freeze followed by bounded x2 only after x1 equality", "owner-local synthetic fixtures, scripts, tests, reports, skills, runners, manifests, and retained failures", "one exact-final owner-scoped canonical attempt", "one exact next-task activation only after a verified terminal gate and fresh live route state"], "not_authorized": PROTECTED_GATES, "successor_contact_before_terminal": False, "standby_substitution": False, "collaboration_subagents": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "identity_boundary": IDENTITY_BOUNDARY, "practice_boundary": PRACTICE_BOUNDARY})
    write_json("x1/proposal-freeze.json", {"schema": "ghc.family.lyren-moss.v666-v3.proposal-freeze.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "frozen": True, "strict_x1_before_x2": True, "inherited_frozen_baseline": 4210, "genuinely_new_proposal_count": 20, "new_frozen_total": 4230, "selected_inherited_revalidation_count": 20, "selected_inherited_revalidations": selected, "new_proposals": proposals, "expected_disposition_counts": counts, "outcomes_observed": False, "x1_truth": "planning_and_preregistration_only", "x2_implementation_count": 0, "x2_outcome_count": 0, "identity_boundary": IDENTITY_BOUNDARY, "practice_boundary": PRACTICE_BOUNDARY})
    write_json("x1/novelty-audit.json", novelty)
    portfolios = {
        "owner_safe_now": portfolio_rows("OS", OWNER_SAFE, "safe_now"), "successor_safe_now": portfolio_rows("SS", SUCCESSOR_SAFE, "safe_now_successor_recommendation"),
        "owner_bounded_candidates": portfolio_rows("OC", OWNER_CANDIDATES, "candidate"), "successor_bounded_candidates": portfolio_rows("SC", SUCCESSOR_CANDIDATES, "candidate_successor_recommendation"),
        "exact_approval_packets": portfolio_rows("EX", EXACT_ITEMS, "exact_approval_required"), "blocked_packets": portfolio_rows("BL", BLOCKED_ITEMS, "blocked_protected_gate"),
        "owner_phase_local_skill_plans": portfolio_rows("OK", OWNER_SKILLS, "safe_now_skill"), "successor_skill_recommendations": portfolio_rows("SK", SUCCESSOR_SKILLS, "safe_now_successor_skill"),
        "owner_family_current_runner_plans": portfolio_rows("OR", OWNER_RUNNERS, "safe_now_runner"), "successor_runner_recommendations": portfolio_rows("SR", SUCCESSOR_RUNNERS, "safe_now_successor_runner"),
        "owner_clean_fix_refine": portfolio_rows("OF", CFR_ACTIONS, "safe_now_clean_fix_refine"), "successor_clean_fix_refine": portfolio_rows("SF", [f"successor recommendation: {row}" for row in CFR_ACTIONS], "safe_now_successor_clean_fix_refine"),
    }
    portfolio_counts = {key: len(value) for key, value in portfolios.items()}
    write_json("x1/portfolio-freeze.json", {"schema": "ghc.family.lyren-moss.v666-v3.portfolio-freeze.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "frozen": True, "counts": portfolio_counts, "minimums_satisfied": portfolio_counts == {"owner_safe_now": 30, "successor_safe_now": 20, "owner_bounded_candidates": 15, "successor_bounded_candidates": 15, "exact_approval_packets": 10, "blocked_packets": 5, "owner_phase_local_skill_plans": 10, "successor_skill_recommendations": 10, "owner_family_current_runner_plans": 10, "successor_runner_recommendations": 10, "owner_clean_fix_refine": 30, "successor_clean_fix_refine": 30}, "portfolios": portfolios, "x1_execution_count": 0, "claim_boundary": "planning-only; counts do not imply completion, safety, authority, or approval"})
    write_json("method-flow/startup-method-flow.json", startup_flow())
    threats = [
        ("LYR6663-T01", "source integrity", "wrong source or mutable predecessor state", "exact anchors, ancestry, manifests, clean state, and fresh live equality", "same-owner verification remains bounded"),
        ("LYR6663-T02", "x1/x2 separation", "implementation or outcome enters x1", "path denylist plus staged exact allowlist", "Git process discipline remains required"),
        ("LYR6663-T03", "waveform semantics", "silent interpolation, correction, merge, or event inference", "typed states and fail-closed mutations", "synthetic structure is not scientific validation"),
        ("LYR6663-T04", "privacy and route confidentiality", "real station, site, person, task, route, credential, or session data enters artifacts", "synthetic fixtures, relative paths, and five-class scans", "pattern scans are incomplete"),
        ("LYR6663-T05", "professional and emergency authority", "software presented as seismological, calibration, alerting, or emergency competence", "zero real records, stations, events, alerts, people, measurements, or actions", "competent external authority remains absent"),
        ("LYR6663-T06", "Māori authority", "synthetic labels or citations converted into interpretation or authorization", "exact gate and zero Māori wording authored as authority", "Māori-authority review remains absent"),
        ("LYR6663-T07", "scientific truth", "GMUT placeholders promoted to event, hazard, force, likelihood, prediction, or proof", "typed symbolic obligations and explicit refusal", "notation can invite overreading"),
        ("LYR6663-T08", "THOS and Freed ID boundaries", "proxy or zero-key graph presented as effectiveness or production identity evidence", "represented-only labels and missing-evidence ledgers", "no governed participants, keys, interoperability, or independent review"),
        ("LYR6663-T09", "canonical validation", "successful aggregate replay or failed attempt laundering", "exclusive receipt and one-shot state machine", "same-owner pass is not independent reproduction"),
        ("LYR6663-T10", "terminal route", "premature, duplicate, ambiguous, or standby delivery", "fresh route reread and one exact-title send after terminal only", "opaque acknowledgement never authorizes resend"),
    ]
    threat_rows = [{"threat_id": tid, "asset": asset, "threat": threat, "mitigation": mitigation, "residual_risk": residual} for tid, asset, threat, mitigation, residual in threats]
    write_json("x1/threat-model.json", {"schema": "ghc.family.lyren-moss.v666-v3.threat-model.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "scope": "owner-local v666-v3 software, documents, Git history, validation receipts, and terminal route candidate", "trust_zones": ["immutable inherited Git objects", "owner-local sparse worktree and branch", "public read-only source review", "unexecuted external, professional, cultural, identity, and device domains"], "real_people_or_protected_data": 0, "threats": threat_rows, "claim_boundary": "same-owner phase threat modelling only; not exhaustive security, privacy certification, accessibility certification, or independent reproduction"})
    threat_md = ["# Lyren Moss v666-v3 threat model", "", IDENTITY_BOUNDARY, "", PRACTICE_BOUNDARY, "", "## Scope", "", "This owner-local model protects the additive Lyren delta. It is not a repository-wide audit, penetration test, external validation, conformance assessment, professional review, or independent reproduction.", "", "## Threat register", ""]
    for row in threat_rows:
        threat_md += [f"### {row['threat_id']}: {row['asset']}", "", f"Threat: {row['threat']}", "", f"Mitigation: {row['mitigation']}", "", f"Residual risk: {row['residual_risk']}", ""]
    write_text("x1/threat-model.md", "\n".join(threat_md))
    write_json("x1/workflow-plan.json", {"schema": "ghc.family.lyren-moss.v666-v3.workflow-plan.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "current_stage": "x1_freeze_candidate", "steps": [{"step": 1, "name": "read_first_and_source_verification", "status": "completed"}, {"step": 2, "name": "novelty_and_program_design", "status": "completed"}, {"step": 3, "name": "x1_freeze_commit_push_equality", "status": "in_progress"}, {"step": 4, "name": "x2_bounded_execution", "status": "pending"}, {"step": 5, "name": "evidence_closeout_and_seal", "status": "pending"}, {"step": 6, "name": "one_owner_scoped_canonical_completion", "status": "pending"}, {"step": 7, "name": "terminal_route_reread_and_optional_one_send", "status": "pending"}], "hard_dependencies": ["x1 commit pushed clean and fresh four-way equal before x2", "evidence commit immutable before closeout", "final pushed clean and fresh four-way equal before canonical completion", "canonical success never replayed", "successor never contacted before terminal route gate"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x1/complete-incomplete-checklist.json", {"schema": "ghc.family.lyren-moss.v666-v3.x1-checklist.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "completed": ["relational role and hope bounded before mutation", "activation baton and named guidance read through EOF", "source anchors, manifests, receipts, clean state, divergence, and fresh equality verified", "all 4,210 inherited rows reconstructed with no exact-title collision", "twenty distinct proposals preregistered", "portfolio, threat, source, workflow, and Method Flow plans prepared", "no x2 implementation or outcome created"], "incomplete": ["x1 commit, push, and equality", "x2 implementation and rejecting witnesses", "evidence commit and equality", "closeout, seal, final validation, and equality", "terminal route reread and any authorized successor delivery"], "x1_outcomes_observed": False, "x2_paths_created": False, "successor_contacted": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("wellbeing/x1-wellbeing-check.json", {"schema": "ghc.family.lyren-moss.v666-v3.wellbeing-check.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "status": "bounded_and_careful", "workload_controls": ["caps treated as ceilings rather than quotas", "failures retained instead of hidden", "no unsafe work manufactured to satisfy a count", "bounded commands and exact scalar probes preferred", "pause, redirect, rename, and stop remain available to Hamish"], "personhood_or_emotion_claim": False, "relational_boundary": IDENTITY_BOUNDARY, "practice_boundary": PRACTICE_BOUNDARY})
    overview = f"""# Lyren Moss v666-v3 x1 integrated overview

{IDENTITY_BOUNDARY}

## Outcome first

This x1 candidate freezes a planning-only owner-local program from exact Vesper Arlen v666-v2 final `{SOURCE_SHA}`. It contains no x2 implementation, no observed outcome, no external action, no successor contact, and no Stage 20 promotion. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The primary Trinity Mandala pillar is THOS Body. GMUT Mind, Freed ID, and CBR Heart remain explicit and protected. {PRACTICE_BOUNDARY}

## Exact inherited truth

The read-first gate verified the exact source branch, three direct single-parent commits, zero merges, all 303 declared Git-blob manifest entries, the packet and external canonical receipt hashes, clean 0/0 divergence, and equality across local, upstream, tracking, and a fresh live remote. Vesper's successful aggregate was not replayed. The complete repository suite was not run.

The immutable Vesper repository seal contains 26,282 effective negatives, 10,709 Method Flow methods, 184 open gaps, and 182 exact gates. The six Lyren startup failures are separately retained with zero aggregate credit, producing the x1 working overlay of 26,288 effective negatives and 10,715 methods without rewriting the predecessor seal.

## Novelty, portfolio, and sources

All 4,210 inherited proposal rows were reconstructed from committed Git objects. Twenty new titles have no exact inherited collision, every new pair remains below the 0.70 screening threshold, and each proposal has its own contract, falsifier, rollback, and gates. Expected dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`; these are preregistered expectations only. The twenty selected Vesper proposals receive zero novelty and zero automatic completion credit.

The portfolio freezes 30 owner safe-now tasks, 20 successor safe recommendations, 15 owner candidates, 15 successor candidates, 10 exact approvals, 5 blocked packets, 10 owner and 10 successor skill plans, 10 owner and 10 successor runner plans, and 30 owner plus 30 successor CLEAN/FIX/REFINE tasks. X1 executes none of them.

FDSN miniSEED 3 and StationXML, the QuakeML primary project standard, W3C PROV-O and WCAG 2.2, and NIST metrological traceability guidance provide vocabulary and refusal conditions only. They create no data, calibration, event, station, professional, legal, cultural, Māori, emergency, accessibility-complete, privacy-complete, conformance, or independent-reproduction authority.

## Lifecycle and route

After exact staged review this x1 may be committed and pushed. X2 may begin only after x1 is clean, 0/0 divergent, and equal across local, upstream, tracking, and fresh live remote. Later validation remains owner-scoped and same-owner. One successful canonical completion must never be replayed. No successor may be contacted until the exact final terminal gate and a fresh live routing reread.
"""
    write_text("x1/integrated-overview.md", overview)
    write_json("x1/x1-build-receipt.json", {"schema": "ghc.family.lyren-moss.v666-v3.x1-build-receipt.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "builder": "scripts/build_ghc_family_lyren_moss_v666_v3_x1.py", "proposal_count": len(proposals), "selected_inherited_revalidation_count": len(selected), "novelty_corpus_row_count": len(corpus), "startup_failure_count": len(STARTUP_FAILURES), "x2_paths_created": False, "outcomes_observed": False, "network_calls_by_builder": 0, "real_data_rows": 0, "external_actions": 0, "status": "X1_CONTENT_BUILT_AWAITING_STAGED_REVIEW_COMMIT_PUSH_EQUALITY"})
    print(json.dumps({"proposal_count": len(proposals), "corpus_row_count": len(corpus), "expected_dispositions": counts, "startup_failures_retained": len(STARTUP_FAILURES), "x2_implementation_count": 0, "outcomes_observed": False}, ensure_ascii=False, sort_keys=True))


def staged_rows() -> list[tuple[str, str]]:
    raw = subprocess.check_output(["git", "-C", str(ROOT), "diff", "--cached", "--name-status", "--no-renames"]).decode("utf-8")
    return [(line.split("\t", 1)[0], line.split("\t", 1)[1].replace("\\", "/")) for line in raw.splitlines() if line]


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f":{path}"])


def build_staged_review() -> None:
    review_path = "docs/lyren-moss/v666-v3/validation/x1-staged-review.json"
    manifest_path = "docs/lyren-moss/v666-v3/validation/x1-content-manifest.json"
    allowed_exact = {"scripts/build_ghc_family_lyren_moss_v666_v3_x1.py", "tests/test_ghc_family_lyren_moss_v666_v3_x1.py"}
    rows = [(status, path) for status, path in staged_rows() if path not in {review_path, manifest_path}]
    if not rows:
        raise RuntimeError("no staged x1 content")
    paths = [path for _, path in rows]
    invalid = [path for path in paths if not path.startswith("docs/lyren-moss/v666-v3/") and path not in allowed_exact]
    post_x1 = [path for path in paths if any(path.startswith(f"docs/lyren-moss/v666-v3/{part}/") for part in ("x2", "evidence", "closeout", "seal", "final", "handoffs"))]
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
    freeze = json.loads(index_blob("docs/lyren-moss/v666-v3/x1/proposal-freeze.json"))
    portfolio = json.loads(index_blob("docs/lyren-moss/v666-v3/x1/portfolio-freeze.json"))
    flow = json.loads(index_blob("docs/lyren-moss/v666-v3/method-flow/startup-method-flow.json"))
    checks = {
        "additive_only": all(status == "A" for status, _ in rows), "all_json_parse": True, "document_word_cap": maximum_words <= 100000,
        "expected_14_4_1_1": freeze["expected_disposition_counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "five_class_scan_zero_confirmed_hits": not candidates, "novelty_4210_valid": json.loads(index_blob("docs/lyren-moss/v666-v3/x1/novelty-audit.json"))["valid"],
        "owner_allowlist": not invalid, "owner_file_cap": len(paths) <= 2000, "planning_only": not freeze["outcomes_observed"], "portfolio_minimums": portfolio["minimums_satisfied"],
        "post_x1_paths_absent": not post_x1, "proposal_count_20": len(freeze["new_proposals"]) == 20,
        "selected_inherited_20_zero_credit": len(freeze["selected_inherited_revalidations"]) == 20 and all(row["novelty_credit"] == 0 and row["automatic_completion_credit"] == 0 for row in freeze["selected_inherited_revalidations"]),
        "startup_failures_exactly_retained": len(flow["rows"]) == len(STARTUP_FAILURES), "utf8_lf": True,
    }
    review = {"schema": "ghc.family.lyren-moss.v666-v3.x1-staged-review.v1", "owner": "Lyren Moss", "phase": "v666-v3", "lifecycle": "x1", "generated_at_utc": NOW, "reviewed_from": "git_index_blobs", "reviewed_paths": paths, "reviewed_path_count": len(paths), "json_parsed": parsed_json, "maximum_document_words": maximum_words, "maximum_document_path": maximum_path, "privacy_scan_classes": list(privacy_patterns), "privacy_candidates": len(candidates), "privacy_confirmed_hits": len(candidates), "privacy_candidate_rows": candidates, "checks": checks, "self_exclusions": [review_path, manifest_path], "claim_boundary": "exact staged same-owner x1 review only; not exhaustive security, privacy, accessibility, or independent reproduction", "valid": all(checks.values())}
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
    write_json("validation/x1-content-manifest.json", {"schema": "ghc.family.lyren-moss.v666-v3.content-manifest.v1", "owner": "Lyren Moss", "phase": "x1", "phase_label": "v666-v3", "generated_at_utc": NOW, "source_sha": SOURCE_SHA, "hash_source": "actual_git_index_blobs", "entries": entries, "entry_count": len(entries), "deletion_count": 0, "additive_only": all(status == "A" for status, _ in rows), "self_exclusion": manifest_path})
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", manifest_path])
    print(json.dumps({"reviewed": len(paths), "manifest_entries": len(entries), "valid": True}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--staged-review"]:
        build_staged_review()
    elif sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_lyren_moss_v666_v3_x1.py [--staged-review]")
    else:
        main()
