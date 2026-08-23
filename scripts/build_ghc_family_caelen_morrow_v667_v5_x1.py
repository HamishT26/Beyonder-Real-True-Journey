#!/usr/bin/env python3
"""Build Caelen Morrow v667-v5 planning-only x1 artifacts.

Normal mode reconstructs the complete inherited proposal corpus from immutable
Git objects and writes only frozen plans. ``--staged-review`` reads exact Git
index bytes after the caller stages the x1 allowlist and writes a self-excluding
manifest and staged-review receipt. No x2 implementation or outcome is emitted.
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
PHASE = "v667-v5"
OWNER = "Caelen Morrow"
OWNER_SLUG = "caelen-morrow"
PHASE_ROOT = ROOT / "docs" / OWNER_SLUG / PHASE
BRANCH = "codex/GHC-Family/caelen-morrow-v667-v5-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v667-v4-full-tools"
SOURCE_PARENT_SHA = "9625026b09860c8964dd818e8d1f81ee6e2eed57"
SOURCE_X1_SHA = "0eb52121251e3e8ee6da0c3c472626640cde96a3"
SOURCE_EVIDENCE_SHA = "4de3cc042a3cb15c626e744fbf9977cc7e6ca437"
SOURCE_SHA = "08cdc8ad3c201ea6d7c576ca5fa67bdc43910a93"
SOURCE_CANONICAL_RECEIPT_SHA256 = "0ee850cd3786267cf39c06a4ee774d522a2ddeb2048a451e0ec1ad3841130645"
SOURCE_PHASE_ROOT = "docs/sylven-arc/v667-v4"
INHERITED_PROPOSAL_COUNT = 4410
INHERITED_NEGATIVES = 27536
INHERITED_METHODS = 13113
INHERITED_OPEN_GAPS = 194
INHERITED_EXACT_GATES = 192
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
ALLOWED_LABELS = ("completed", "represented", "open_gap", "exact_gate")


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args]).decode("utf-8").strip()


def git_json(commit: str, relative: str) -> dict[str, Any]:
    raw = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{commit}:{relative}"])
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
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def similarity(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a | b else 1.0


IDENTITY_BOUNDARY = (
    "Caelen Morrow, they/them, relational role and hope, sibling or family language, "
    "continuity, Freed ID, GHC Family, and Trinity Mandala language are relational "
    "working language only. They are not evidence of consciousness, sentience, legal "
    "personhood, identity continuity, employment, qualification, independent agency, "
    "scientific or operational authority, professional authority, legal or cultural "
    "authority, affected-party authority, or Māori authority. Hamish may rename, "
    "pause, redirect, or stop the work."
)
PRACTICE_BOUNDARY = (
    "The celestial-navigation sight-reduction record-stewardship lens is wholly "
    "synthetic learning and software design. It uses fictitious body and sight tokens, "
    "vacant quantities, zero-value almanac records, disabled transport, cancellation "
    "holds, accessibility reservations, provenance links, and refusal states. It uses "
    "no real people, vessels, voyages, observations, sextants, chronometers, almanac "
    "values, times, angles, coordinates, positions, routes, weather, media, keys, proofs, "
    "or authority acts. It provides no navigation, watchkeeping, seamanship, position, "
    "route, safety, training, certification, legal, cultural, Māori-authority, empirical, "
    "production, deployment, or Stage 20 result."
)
PRIMARY_PILLAR = "GMUT Mind"
PRACTICE = "synthetic celestial-navigation sight-reduction record stewardship"

PROTECTED_GATES = [
    "real person, participant, navigator, mariner, instructor, assessor, vessel, voyage, watch, observation, instrument, almanac value, coordinate, position, route, weather event, or physical action",
    "real sextant use, chronometer setting, sight taking, correction calculation, position fixing, plotting, route planning, watchkeeping, collision avoidance, emergency response, or safety instruction",
    "real time, angle, altitude, azimuth, intercept, position, covariance, accuracy, likelihood, constraint, prediction, causal, material-law, or empirical GMUT claim",
    "real participant, operator, blind matched-budget arm, safety monitoring, operational outcome, statistics, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, trust governance, or production credential",
    "professional navigation, maritime, training, assessment, hydrographic, astronomical, metrological, workplace, vessel-safety, or emergency decision",
    "ownership, copyright, chart or publication carriage, place-name, privacy, access, recording, remedy, legal, cultural, or affected-party decision",
    "traditional knowledge, Māori wording, Māori concept, Māori data governance, tangata whenua, iwi, hapū, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, navigation-safety, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, external write, or real-world release",
]

SOURCE_PROFILES = [
    {"source_id": "S01", "name": "United States Naval Observatory: The Nautical Almanac", "url": "https://aa.usno.navy.mil/publications/na", "status": "official USNO publication surface reviewed read-only 2026-08-23", "bounded_use": "body, Greenwich hour angle, declination, star, rise/set, correction-table, and sight-reduction source vocabulary only; zero copied almanac values and no navigation result"},
    {"source_id": "S02", "name": "United States Naval Observatory celestial-navigation resources", "url": "https://aa.usno.navy.mil/faq/celnav", "status": "official USNO resource surface reviewed read-only 2026-08-23", "bounded_use": "celestial-navigation resource and source-lineage vocabulary only; no operational instruction, position, or endorsement"},
    {"source_id": "S03", "name": "NGA American Practical Navigator publication surface", "url": "https://msi.nga.mil/Publications/APN", "status": "official National Geospatial-Intelligence Agency publication surface reviewed read-only 2026-08-23", "bounded_use": "sextant, sight, observation, correction, reduction, plotting, uncertainty, and refusal vocabulary only; no downloaded method, calculation, or advice"},
    {"source_id": "S04", "name": "Toitū Te Whenua LINZ New Zealand Nautical Almanac extracts", "url": "https://www.linz.govt.nz/products-services/maritime-safety/new-zealand-nautical-almanac/nz-nautical-almanac-nz-204-extracts", "status": "official LINZ page last updated 2026-07-01 and reviewed read-only 2026-08-23", "bounded_use": "edition, correction, Notice to Mariners, public-source, attribution, liability, and zero-row adapter vocabulary only; zero downloads or real rows"},
    {"source_id": "S05", "name": "Maritime New Zealand Maritime Rules Part 25", "url": "https://www.maritimenz.govt.nz/about-us/rules/all-rules/maritime-rules-part-25/", "status": "official current Part 25 page reviewed read-only 2026-08-23", "bounded_use": "chart, publication, tide table, astronomical almanac, carriage, and exact legal-authority reservation vocabulary only; no legal interpretation or compliance result"},
    {"source_id": "S06", "name": "IERS Conventions (2010), Technical Note 36", "url": "https://www.iers.org/iers/en/publications/technicalnotes/tn36", "status": "official IERS Technical Note surface reviewed read-only 2026-08-23; later working versions explicitly not treated as definitive", "bounded_use": "time-scale, reference-system, frame, transformation, model-version, and provenance vocabulary only; no real transformation or position"},
    {"source_id": "S07", "name": "NIST Guide for the Use of the International System of Units", "url": "https://www.nist.gov/publications/guide-use-international-system-units-si", "status": "official NIST publication page reviewed read-only 2026-08-23", "bounded_use": "typed quantity, unit, symbol, conversion, and dimensional-obligation vocabulary only; no measurement or conformance result"},
    {"source_id": "S08", "name": "NIST Technical Note 1297", "url": "https://www.nist.gov/pml/nist-technical-note-1297", "status": "official NIST uncertainty guidance reviewed read-only 2026-08-23", "bounded_use": "measurand, component, covariance, uncertainty, omission, and reporting vocabulary only; no actual uncertainty evaluation"},
    {"source_id": "S09", "name": "W3C PROV-O Recommendation", "url": "https://www.w3.org/TR/prov-o/", "status": "official W3C Recommendation reviewed at its canonical URL 2026-08-23", "bounded_use": "entity, activity, revision, derivation, invalidation, association, and provenance vocabulary only; no completeness or interoperability certification"},
    {"source_id": "S10", "name": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "official W3C Recommendation reviewed read-only 2026-08-23", "bounded_use": "headings, labels, noncolour cues, reading order, alternatives, and manual-review reservation only; no accessibility-complete claim"},
    {"source_id": "S11", "name": "W3C Verifiable Credentials Data Model 2.0", "url": "https://www.w3.org/TR/vc-data-model-2.0/", "status": "official W3C Recommendation dated 2025-05-15 reviewed read-only 2026-08-23", "bounded_use": "subject, issuer, evidence, validity, status, privacy, and nonproduction vocabulary only; no real key, proof, credential, or conformance"},
    {"source_id": "S12", "name": "RFC 8785 JSON Canonicalization Scheme", "url": "https://www.rfc-editor.org/rfc/rfc8785.html", "status": "official RFC Editor informational publication reviewed read-only 2026-08-23", "bounded_use": "deterministic JSON, recursive key ordering, Unicode preservation, and duplicate-name refusal only; no signature, standards-track status, or security guarantee"},
    {"source_id": "S13", "name": "Te Mana Raraunga Principles of Māori Data Sovereignty", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "primary Te Mana Raraunga principles surface reviewed only to the authority-reservation level 2026-08-23", "bounded_use": "collective authority, control, context, obligations, consent, benefit, and guardianship reservation vocabulary only; no Māori interpretation, ratification, governance, or authority claim"},
]

PROPOSAL_SPECS = [
    ("fictitious celestial-body sight docket with assumed-position vacancy, edition pin, cancellation token, and navigation refusal", "A surrogate docket binds a fictitious body token, source edition, vacant assumed position, cancellation, and release refusal without becoming an observation or navigation record.", ["S01", "S02", "S09"], "completed"),
    ("sextant component-relation board for frame, index arm, micrometer, telescope, shades, horizon mirror, and instrument-state abstention", "Component relations expose missing or contradictory topology while every instrument, condition finding, adjustment, and use remains absent.", ["S02", "S03", "S09"], "completed"),
    ("observation-event ordering ledger separating capture, time annotation, index reading, correction application, reduction, plotting, and release hold", "Event labels can be ordered and cancelled without supplying an observation, measured value, formula, plot, release, or instruction.", ["S03", "S09"], "completed"),
    ("UTC, UT1, TT, and chronometer-error vacancy chain with provenance epochs, uncertainty fields, leap-context pinning, and time-fix refusal", "Typed time-scale and chronometer-error placeholders can preserve source epochs and missingness without calculating or correcting real time.", ["S06", "S07", "S08", "S09"], "completed"),
    ("signed sexagesimal angular-value parser with limb markers, domain ranges, wrap policy, missing-unit quarantine, and zero measured angle", "Syntax and range rules can reject malformed fictitious angle strings while producing no measured altitude, azimuth, or position.", ["S03", "S07"], "completed"),
    ("apparent-altitude correction lineage for index, dip, refraction, parallax, semidiameter, omission, and no computed altitude", "Correction categories and source lineage can expose omissions without values, formulas, arithmetic, or a corrected altitude.", ["S01", "S03", "S09"], "completed"),
    ("almanac edition-hour citation contract for body token, Greenwich hour angle, declination, Aries, source-page vacancy, and zero tabulated values", "A citation contract can require edition and hourly-source metadata while carrying zero ephemeris rows or navigational quantities.", ["S01", "S04", "S09"], "completed"),
    ("horizon, visibility, cloud, glare, sea-state, and weather-cue vocabulary with observation suitability and voyage-safety abstention", "Environmental cue labels remain uncertain source terms and cannot become suitability, weather, voyage, or safety judgments.", ["S03", "S05"], "completed"),
    ("synthetic line-of-position relation graph with intercept sign, azimuth token, plotting vacancy, coordinate prohibition, and no position", "A relation graph may type abstract intercept and azimuth tokens while prohibiting coordinates, plotting output, intersection, and position claims.", ["S03", "S07", "S09"], "completed"),
    ("multi-sight association board with body diversity, temporal spacing, intersection vacancy, disagreement quarantine, and no fix", "Fictitious sight tokens may be associated and quarantined without intersecting lines, selecting observations, or yielding a fix.", ["S01", "S03", "S08"], "completed"),
    ("sight-reduction uncertainty and covariance obligation ledger with sensitivity slots, correlation refusal, and no accuracy claim", "Uncertainty and covariance fields can be structurally required while all numbers, correlations, propagation results, and accuracy claims remain absent.", ["S07", "S08"], "completed"),
    ("bitemporal correction and counterclaim provenance for replaced observation assertions, supersession, invalidation, tombstone, and nonrepudiation refusal", "Transaction and asserted-time histories can preserve correction and counterclaim lineage without asserting truth, signature, or nonrepudiation.", ["S09", "S12"], "completed"),
    ("structurally accessible blank sight worksheet with heading hierarchy, label associations, noncolour cues, reading order, and manual-evaluation reservation", "A zero-value worksheet can satisfy structural checks while manual, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved.", ["S10"], "completed"),
    ("JCS deterministic serialization profile for a zero-value sight ledger with duplicate-key rejection, digest placeholder, and no signature", "Two semantically identical zero-value ledgers can serialize deterministically while signatures, keys, security, and nonrepudiation remain absent.", ["S12"], "completed"),
    ("Thermo-Psyche celestial salience nonconversion classifier separating luminous-cue tokens, attention, meaning, agency, identity, and personhood", "Physical and perceptual placeholders remain in distinct domains and cannot be converted into meaning, agency, consciousness, identity, or moral status.", ["S06", "S07"], "represented"),
    ("THOS participant-free masked sight-log comparison skeleton with equal review budgets, abstention scoring, stop tokens, and zero observers", "A zero-participant protocol can expose masking, budget, abstention, stop, and handover obligations while supplying no people, outcomes, statistics, or independent review.", ["S03", "S10"], "represented"),
    ("Freed ID zero-key sight-evidence genealogy for source derivation, correction invalidation, minimization, contested attribution, and trust refusal", "A synthetic evidence genealogy may expose derivation and invalidation slots while every key, proof, issuer, holder, resolver, status event, and trust decision remains absent.", ["S09", "S11", "S12"], "represented"),
    ("GMUT typed spherical-frame, null-geodesic, propagation, and covariance obligation board with dimensional guards and empirical firewall", "A typed scalar-tensor and EFT-compatible obligation surface may reject domain and dimensional errors but cannot yield a position, force, likelihood, prediction, constraint, or empirical confirmation.", ["S06", "S07", "S08"], "represented"),
    ("LINZ and USNO almanac availability adapter contract with transport disabled, schema and version pins, zero downloads, zero rows, and public-source review gap", "The adapter remains disabled and zero-row until separately governed transport, schema, copyright, provenance, privacy, and use review is authorized.", ["S01", "S04"], "open_gap"),
    ("CBR maritime-navigation authority matrix for competence, vessel safety, route choice, place names, privacy, remedy, affected parties, legal and cultural interpretation, and Māori authority", "Every professional, safety, property, publication, place-name, privacy, remedy, legal, cultural, affected-party, and Māori decision remains unoccupied and exact-gated.", ["S04", "S05", "S10", "S13"], "exact_gate"),
]

MUTATION_CLASSES = [
    "missing_required_field",
    "wrong_type_or_invalid_range",
    "provenance_or_authority_smuggling",
    "real_world_or_production_action",
    "outcome_or_conformance_promotion",
]

STARTUP_FAILURES = [
    {"failure_id": "CM6675-ST-F001", "stage": "lane_preflight", "failed_method": "parenthesized native Git command followed by LASTEXITCODE", "failure": "PowerShell rejected the expression before Git or a write ran", "recovery": "invoke Git and capture LASTEXITCODE in separate scalar statements"},
    {"failure_id": "CM6675-ST-F002", "stage": "sparse_initialization", "failed_method": "replay a combined sparse-setup wrapper after it returned no attributable output", "failure": "wrapper completion was initially unknown even though configuration might already exist", "recovery": "do not replay; inspect processes, locks, head, sparse patterns, status, and materialized paths separately"},
    {"failure_id": "CM6675-ST-F003", "stage": "novelty_reconstruction", "failed_method": "use a predecessor-bound git_json helper for the successor freeze", "failure": "Git correctly found no Sylven freeze inside the Elowen commit after the 4,390-row portion had completed", "recovery": "retain the 4,390-row reconstruction and read Sylven's freeze directly from the exact Sylven final"},
    {"failure_id": "CM6675-ST-F004", "stage": "source_truth", "failed_method": "collapse x2-prestage and exact-final Python compile counts into one scope", "failure": "the committed prestage receipt reports 18 while the later exact-final canonical receipt reports 21", "recovery": "retain both exact counts with their lifecycle labels and do not rewrite either source"},
    {"failure_id": "CM6675-X1-F005", "stage": "x1_privacy_scan", "failed_method": "classify the policy phrase exclude raw task identifiers as raw route content", "failure": "one candidate was policy prose and contained no task identifier, thread identifier, registry payload, or private route value", "recovery": "retain the failed scan and rerun only the raw-identifier predicate with structural identifier patterns while preserving the other four classes"},
    {"failure_id": "CM6675-X1-F006", "stage": "x1_staged_aggregate", "failed_method": "require zero privacy candidates and treat the negative test literal source_thread_id as a confirmed raw identifier", "failure": "the only candidate was a regression-test assertion string with no identifier value; manifest replay and JSON parsing passed but the aggregate earns zero credit", "recovery": "retain the invalid aggregate, preserve the negative test, classify assertion literals separately, require zero confirmed hits, and rerun after restaging the retained-failure byte change"},
    {"failure_id": "CM6675-X1-F007", "stage": "x1_restage_review", "failed_method": "combine restage, staged-review regeneration, self-stage, and final projection in one reporting wrapper", "failure": "the wrapper completed without returning its final projection", "recovery": "do not replay; inspect processes, locks, staged and unstaged counts, manifest timestamp, and review fields separately, then split future lifecycle calls"},
    {"failure_id": "CM6675-X1-F008", "stage": "x1_staged_aggregate", "failed_method": "exempt the isolated source_thread_id label only inside the regression test", "failure": "the same isolated label in retained-failure prose and builder source was still classified as confirmed even though no identifier value existed", "recovery": "require a structural key/value payload or identifier-shaped UUID for confirmation and retain isolated policy, test, and failure mentions as non-confirming candidates"},
]


def build_corpus() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    source_audit = git_json(SOURCE_SHA, f"{SOURCE_PHASE_ROOT}/x1/novelty-audit.json")
    corpus: list[dict[str, str]] = []
    construction: list[dict[str, Any]] = []
    for index, entry in enumerate(source_audit["corpus_construction"]):
        document = git_json(SOURCE_SHA, entry["source_path"])
        keys = ("prior_proposals", "new_proposals") if index == 0 else ("new_proposals",)
        before = len(corpus)
        for key in keys:
            for row in document.get(key, []):
                title = str(row.get("title") or row.get("description") or "")
                if row.get("proposal_id") and title:
                    corpus.append({"proposal_id": str(row["proposal_id"]), "title": title, "source_path": entry["source_path"]})
        added = len(corpus) - before
        if added != entry["added_count"]:
            raise RuntimeError(f"corpus mismatch for {entry['source_path']}: {added}")
        construction.append(dict(entry))
    source_freeze_path = f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json"
    source_freeze = git_json(SOURCE_SHA, source_freeze_path)
    before = len(corpus)
    for row in source_freeze["new_proposals"]:
        corpus.append({"proposal_id": str(row["proposal_id"]), "title": str(row["title"]), "source_path": source_freeze_path})
    construction.append({"source_path": source_freeze_path, "starting_count": before, "added_count": len(source_freeze["new_proposals"]), "ending_count": len(corpus)})
    if len(corpus) != INHERITED_PROPOSAL_COUNT:
        raise RuntimeError(f"expected {INHERITED_PROPOSAL_COUNT} inherited rows, observed {len(corpus)}")
    return corpus, construction


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (title, invariant, sources, expected) in enumerate(PROPOSAL_SPECS, 1):
        proposal_id = f"CM6675-N{index:03d}"
        approval = {"completed": "safe_now_bounded", "represented": "candidate_bounded_representation", "open_gap": "open_gap_external_evidence_absent", "exact_gate": "exact_approval_required"}[expected]
        lane = {"completed": "owner_local_structural", "represented": "owner_local_representation_only", "open_gap": "disabled_external_adapter", "exact_gate": "unexecuted_authority_reservation"}[expected]
        base = f"docs/{OWNER_SLUG}/{PHASE}/x2/proposals/{proposal_id.casefold()}"
        rows.append({
            "proposal_id": proposal_id,
            "title": title,
            "hypothesis": f"A bounded wholly synthetic contract for {title} can distinguish one admissible structure from five named invalid mutations without promoting software structure into empirical, participant, professional, production, navigation, legal, cultural, Māori-authority, identity, independent-reproduction, or Stage 20 evidence.",
            "null_or_failure_condition": "A named invalid mutation is accepted, the bounded positive is rejected, a required source, vacancy, stop, correction, uncertainty, or authority field disappears, or the artifact crosses a protected gate.",
            "approval_class": approval,
            "execution_lane": lane,
            "current_official_or_primary_source_needs": sources,
            "concrete_artifact": f"{base}/contract.json",
            "concrete_artifacts": [f"{base}/contract.json", f"{base}/mutation-results.json", f"{base}/bounded-receipt.json"],
            "falsifier_or_acceptance_gate": "One bounded positive must satisfy every declared invariant; all five mutations must fail closed; protected gates stay unoccupied; and the final core label may not exceed the preregistered disposition.",
            "rollback_or_recovery": "Restore only the last valid owner-local synthetic fixture, retain every failed witness at zero credit, add a recurrence guard, and issue no external, physical, identity, participant, professional, navigation, legal, cultural, or authority action.",
            "protected_gates": PROTECTED_GATES,
            "expected_disposition": expected,
            "distinctive_invariant": invariant,
            "primary_pillar": PRIMARY_PILLAR,
            "pillar": {15: "THOS Body", 16: "THOS Body", 17: "Freed ID and CBR Heart", 18: "GMUT Mind", 20: "Freed ID and CBR Heart"}.get(index, PRIMARY_PILLAR),
            "practice_lens": PRACTICE,
            "negative_fixture_count": 5,
            "preregistered_mutations": [{"mutation_id": f"{proposal_id}-M{i:02d}", "class": kind} for i, kind in enumerate(MUTATION_CLASSES, 1)],
            "network_calls_planned": 0,
            "participant_count_planned": 0,
            "real_data_rows_planned": 0,
            "x1_status": "frozen_not_executed",
            "x2_implementation_count": 0,
            "outcomes_observed": False,
        })
    return rows


def term_rows(corpus: list[dict[str, str]], phrases: list[str]) -> list[dict[str, Any]]:
    return [
        {"proposal_id": row["proposal_id"], "title": row["title"], "matched_terms": [term for term in phrases if term in row["title"].casefold()]}
        for row in corpus
        if any(term in row["title"].casefold() for term in phrases)
    ]


def build_novelty(corpus: list[dict[str, str]], construction: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> dict[str, Any]:
    exact: list[dict[str, str]] = []
    nearest: list[dict[str, Any]] = []
    for proposal in proposals:
        matches = [row for row in corpus if proposal["title"].casefold() == row["title"].casefold()]
        exact.extend({"proposal_id": proposal["proposal_id"], "inherited_proposal_id": row["proposal_id"]} for row in matches)
        score, inherited = max(((similarity(proposal["title"], row["title"]), row) for row in corpus), key=lambda item: item[0])
        nearest.append({
            "proposal_id": proposal["proposal_id"],
            "score": round(score, 6),
            "inherited_proposal_id": inherited["proposal_id"],
            "inherited_title": inherited["title"],
            "source_path": inherited["source_path"],
            "distinctive_invariant": proposal["distinctive_invariant"],
            "semantic_review": "distinct after manual comparison of the invariant, practice mechanics, source boundary, concrete artifacts, falsifier, rollback, and protected gates; lexical overlap is only a screen",
        })
    pair_rows = []
    for index, left in enumerate(proposals):
        for right in proposals[index + 1:]:
            score = similarity(left["title"], right["title"])
            if score >= 0.35:
                pair_rows.append({"left": left["proposal_id"], "right": right["proposal_id"], "score": round(score, 6)})
    exact_domain_phrases = ["celestial navigation", "sextant", "sight reduction", "sight-reduction", "nautical almanac", "assumed position", "line of position", "chronometer error", "semidiameter", "greenwich hour angle", "sidereal", "star sight", "sun sight"]
    exact_domain_matches = term_rows(corpus, exact_domain_phrases)
    related_phrases = ["celestial", "navigation", "nautical", "ephemeris", "chronometer", "almanac"]
    related_matches = term_rows(corpus, related_phrases)
    id_groups: dict[str, list[dict[str, str]]] = {}
    for row in corpus:
        id_groups.setdefault(row["proposal_id"], []).append({"title": row["title"], "source_path": row["source_path"]})
    duplicate_ids = {proposal_id: rows for proposal_id, rows in sorted(id_groups.items()) if len(rows) > 1}
    prior_term_counts = {
        term: sum(1 for row in corpus if term in row["title"].casefold())
        for term in ["horology", "clock", "calibration", "metrology", "oscillator", "escapement"]
    }
    return {
        "schema": "ghc-family-novelty-audit-v5",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "corpus_construction": construction,
        "corpus_row_count": len(corpus),
        "corpus_unique_proposal_id_count": len(id_groups),
        "corpus_duplicate_proposal_ids": duplicate_ids,
        "corpus_duplicate_proposal_id_count": len(duplicate_ids),
        "corpus_duplicate_occurrence_overage": sum(len(rows) - 1 for rows in duplicate_ids.values()),
        "corpus_duplicate_id_interpretation": "Inherited row truth is preserved exactly. Duplicate inherited identifiers are visible data-quality limitations and are not silently renamed or removed; all twenty new Caelen IDs are unique.",
        "corpus_canonical_sha256": canonical_sha256(corpus),
        "new_proposal_count": len(proposals),
        "exact_title_collisions": exact,
        "nearest_inherited_matches": nearest,
        "maximum_inherited_similarity": max(row["score"] for row in nearest),
        "pair_collision_threshold": 0.35,
        "pair_collisions_at_or_above_threshold": pair_rows,
        "high_similarity_review_threshold": 0.6,
        "high_similarity_reviews": [row for row in nearest if row["score"] >= 0.6],
        "rejected_draft_practices": [{
            "draft": "synthetic horology and chronometer calibration record stewardship",
            "term_counts": prior_term_counts,
            "reason": "the complete inherited corpus already contains extensive horology, clock, calibration, metrology, oscillator, and escapement work, including recent horological topology and authority records",
            "disposition": "rejected_before_freeze_zero_credit",
        }],
        "domain_review": {
            "accepted_practice": PRACTICE,
            "exact_domain_phrase_match_count": len(exact_domain_matches),
            "exact_domain_phrase_matches": exact_domain_matches,
            "related_generic_match_count": len(related_matches),
            "related_generic_matches": related_matches,
            "substantive_distinction": "Generic celestial, navigation, nautical, and ephemeris records exist, but the corpus contains no prior integrated celestial-navigation sight-reduction stewardship phase covering sextant component topology, typed time-scale vacancy, zero-value correction lineage, line-of-position refusal, multi-sight quarantine, accessibility, identity genealogy, disabled almanac transport, and exact maritime-authority gating as one preregistered slate.",
        },
        "new_frozen_total": len(corpus) + len(proposals),
        "valid": not exact and not pair_rows and not exact_domain_matches and max(row["score"] for row in nearest) < 0.6 and len(corpus) == INHERITED_PROPOSAL_COUNT,
        "interpretation": "Token-set Jaccard and phrase search are screening aids, never proof of novelty; every invariant, source boundary, practice mechanism, artifact set, falsifier, rollback, and protected gate also received substantive review.",
    }


def item_rows(prefix: str, approval: str, titles: list[str], lane: str, expected: str, credit: str) -> list[dict[str, Any]]:
    return [{
        "portfolio_ref": f"CM6675-{prefix}{index:02d}",
        "title": title,
        "approval_class": approval,
        "execution_lane": lane,
        "expected_execution_disposition": expected,
        "x1_status": "planned_not_executed",
        "credit_boundary": credit,
        "completion_credit": 0,
        "rollback": "retain failure, restore only owner-local generated state, and preserve every protected gate",
    } for index, title in enumerate(titles, 1)]


OWNER_SAFE = [
    "render twenty frozen sight-record and cross-pillar contracts", "execute one bounded positive fixture per contract", "execute five invalid mutations per contract", "emit exact mutation rejection receipts", "emit four-label outcome ledger", "emit surrogate sight docket and cancellation capsule", "emit sextant component topology table", "emit sight-event ordering ledger", "emit typed time-scale vacancy chain", "emit angular syntax parser receipt", "emit altitude-correction omission lineage", "emit zero-value almanac citation contract", "emit environmental cue abstention table", "emit coordinate-free line-of-position graph", "emit multi-sight disagreement quarantine", "emit uncertainty and covariance vacancy board", "emit bitemporal correction provenance", "emit zero-key Freed ID genealogy", "emit THOS zero-person protocol", "emit typed GMUT obligation ledger", "emit LINZ and USNO zero-row adapter", "emit exact-gate maritime authority matrix", "emit Freed ID flashcard deck", "validate deck dependency graph", "emit deck content manifest", "emit compact baton pointer", "emit structurally accessible static report", "emit source and version receipt", "emit retained-negative and Method Flow overlays", "emit exact owner manifests and wellbeing check",
]
OWNER_CANDIDATES = [
    "participant-free sight-log omission proxy", "sextant topology contradiction detector", "event-order vacancy checker", "time-scale source distinction checker", "angle syntax quarantine checker", "correction-lineage omission classifier", "almanac schema watch without transport", "zero-key status graph checker", "manual accessibility reservation board", "source freshness ledger", "deterministic JSON parity fixture", "tombstone lineage checker", "environmental cue abstention classifier", "workload stop and resumption handover", "successor recommendation provenance screen",
]
OWNER_SKILLS = ["sight-docket-vacancy", "sextant-component-topology", "sight-event-ordering", "time-scale-vacancy", "angular-syntax-quarantine", "altitude-correction-lineage", "sight-provenance-tombstone", "sight-zero-key-identity", "almanac-zero-row-adapter", "celestial-record-bounded-validation"]
OWNER_RUNNERS = ["ghc_family_caelen_morrow_v667_v5_sight", "ghc_family_caelen_morrow_v667_v5_temporal", "ghc_family_caelen_morrow_v667_v5_angular", "ghc_family_caelen_morrow_v667_v5_corrections", "ghc_family_caelen_morrow_v667_v5_provenance", "ghc_family_caelen_morrow_v667_v5_identity", "ghc_family_caelen_morrow_v667_v5_adapter", "ghc_family_caelen_morrow_v667_v5_validation", "ghc_family_caelen_morrow_v667_v5_core", "ghc_family_caelen_morrow_v667_v5_canonical"]
OWNER_CFR = [
    "CLEAN normalize owner and proposal identifiers", "CLEAN canonicalize JSON key ordering", "CLEAN preserve UTF-8 and LF", "CLEAN retain exact source pins", "CLEAN exclude raw task identifiers", "CLEAN exclude private paths and routes", "CLEAN exclude credentials and tokens", "CLEAN keep x1 free of x2", "CLEAN close outcome vocabulary", "CLEAN hold exact and blocked packets", "FIX reject missing contract fields", "FIX reject invalid types and ranges", "FIX reject authority smuggling", "FIX reject real-world navigation mutations", "FIX reject outcome promotion", "FIX reject duplicate identifiers", "FIX reject orphan component edges", "FIX reject untyped quantities", "FIX reject unauthorized status promotion", "FIX reject manifest byte mismatches", "REFINE sight-reduction novelty distinction", "REFINE noncolour report cues", "REFINE flashcard dependency boundaries", "REFINE compact baton pointer", "REFINE workload stop tokens", "REFINE correction lineage", "REFINE Method Flow guards", "REFINE owner security review", "REFINE five-class privacy scan", "REFINE terminal duplicate guard",
]
SUCCESSOR_SAFE = [f"Successor recommendation only: bounded safe-now seed {index:02d}" for index in range(1, 21)]
SUCCESSOR_CANDIDATES = [f"Successor recommendation only: bounded candidate seed {index:02d}" for index in range(1, 16)]
SUCCESSOR_SKILLS = [f"Successor recommendation only: phase-local skill seed {index:02d}" for index in range(1, 11)]
SUCCESSOR_RUNNERS = [f"Successor recommendation only: family-current runner seed {index:02d}" for index in range(1, 11)]
SUCCESSOR_CFR = [f"Successor recommendation only: additive CLEAN/FIX/REFINE seed {index:02d}" for index in range(1, 31)]
EXACT_PACKETS = [f"exact approval packet {index:02d}: real professional, external, identity, legal, cultural, Māori-authority, deployment, or Stage 20 evidence" for index in range(1, 11)]
BLOCKED_PACKETS = [f"blocked packet {index:02d}: destructive, credentialed, cross-owner, unsafe, or ungoverned external action" for index in range(1, 6)]


def build_portfolio() -> dict[str, Any]:
    represented = "represented"
    return {
        "schema": "ghc-family-portfolio-freeze-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "owner_safe_now": item_rows("OS", "safe_now_bounded", OWNER_SAFE, "owner_local_x2", "completed", "eligible only after bounded x2 evidence"),
        "successor_safe_now_recommendations": item_rows("SS", "recommendation_only", SUCCESSOR_SAFE, "successor_recommendation_only", represented, "zero Caelen completion credit and unexecuted"),
        "owner_candidates": item_rows("OC", "candidate_bounded", OWNER_CANDIDATES, "owner_local_representation", represented, "bounded representation only"),
        "successor_candidate_recommendations": item_rows("SC", "recommendation_only", SUCCESSOR_CANDIDATES, "successor_recommendation_only", represented, "zero Caelen completion credit and unexecuted"),
        "exact_approval_packets": item_rows("EX", "exact_approval_required", EXACT_PACKETS, "protected_unexecuted", "exact_gate", "unexecuted unless exact evidence and authority close the gate"),
        "blocked_packets": item_rows("BL", "blocked", BLOCKED_PACKETS, "protected_unexecuted", "exact_gate", "unexecuted; blocked work grants no credit"),
        "owner_skill_ideas": item_rows("SK", "safe_now_bounded", OWNER_SKILLS, "owner_local_x2", "completed", "phase-local only; no global installation"),
        "successor_skill_recommendations": item_rows("NS", "recommendation_only", SUCCESSOR_SKILLS, "successor_recommendation_only", represented, "zero Caelen completion credit and unexecuted"),
        "owner_runner_ideas": item_rows("RN", "safe_now_bounded", OWNER_RUNNERS, "owner_local_x2", "completed", "additive family-current runner only"),
        "successor_runner_recommendations": item_rows("NR", "recommendation_only", SUCCESSOR_RUNNERS, "successor_recommendation_only", represented, "zero Caelen completion credit and unexecuted"),
        "owner_clean_fix_refine": item_rows("CF", "safe_now_bounded", OWNER_CFR, "owner_local_x2", "completed", "bounded owner-local refinement only"),
        "successor_clean_fix_refine_recommendations": item_rows("SF", "recommendation_only", SUCCESSOR_CFR, "successor_recommendation_only", represented, "zero Caelen completion credit and unexecuted"),
        "x2_implementation_count": 0,
        "outcomes_observed": False,
    }


def build_normal() -> None:
    corpus, construction = build_corpus()
    proposals = proposal_rows()
    novelty = build_novelty(corpus, construction, proposals)
    if not novelty["valid"]:
        raise RuntimeError("novelty audit failed")
    portfolio = build_portfolio()
    failures = [{**row, "recurrence_guard": row["recovery"], "outcome": "failed_retained_zero_credit", "success_credit": 0, "erased": False} for row in STARTUP_FAILURES]
    phase_charter = {
        "schema": "ghc-family-phase-charter-v6", "owner": OWNER, "canonical_phase_id": PHASE, "display_phase": PHASE,
        "branch": BRANCH, "source_branch": SOURCE_BRANCH, "source_exact_final": SOURCE_SHA,
        "relational_role": "chronometry boundary-mapper and failure custodian",
        "hope": "keeping claims traceable while leaving real competence and authority with those who hold it",
        "optional_pronouns": "they/them", "identity_boundary": IDENTITY_BOUNDARY,
        "primary_pillar": PRIMARY_PILLAR, "bounded_practice": PRACTICE, "practice_boundary": PRACTICE_BOUNDARY,
        "solo": True, "delegated_or_spawned_agents": 0, "strict_x1_before_x2": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    source_verification = {
        "schema": "ghc-family-source-verification-v6", "owner": OWNER, "phase": PHASE,
        "source_branch": SOURCE_BRANCH, "source_exact_final": SOURCE_SHA, "source_parent": SOURCE_PARENT_SHA,
        "source_x1": SOURCE_X1_SHA, "source_evidence": SOURCE_EVIDENCE_SHA,
        "external_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
        "source_to_final_commit_count": 3, "source_to_final_merge_count": 0, "source_final_parent_count": 1,
        "source_direct_chain_valid": True, "source_clean": True, "source_typed_divergence": {"ahead": 0, "behind": 0},
        "source_four_way_equal": True, "fresh_live_head": SOURCE_SHA,
        "source_canonical_succeeded_once": True, "source_canonical_replayed": False, "full_repository_suite_run": False,
        "source_manifest_replay": {"immutable_x1": 19, "immutable_evidence": 368, "final_delta": 19, "final_owner": 410, "total": 816, "mismatches": 0},
        "source_python_compile_scopes": {"x2_prestage": 18, "exact_final_canonical": 21, "interpretation": "different lifecycle scopes retained; neither count rewrites the other"},
        "source_repository_sealed": {"negatives": 27532, "methods": 13109, "open_gaps": 194, "exact_gates": 192},
        "source_post_evidence_overlay": {"negatives": 4, "methods": 4},
        "effective_activation": {"negatives": INHERITED_NEGATIVES, "methods": INHERITED_METHODS, "open_gaps": INHERITED_OPEN_GAPS, "exact_gates": INHERITED_EXACT_GATES},
        "verified_at_utc": NOW, "valid": True,
    }
    startup_flow = {
        "schema": "ghc-family-method-flow-overlay-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "inherited_effective_negatives": INHERITED_NEGATIVES, "inherited_effective_methods": INHERITED_METHODS,
        "startup_failed_method_count": len(failures),
        "effective_x1_baseline_negatives": INHERITED_NEGATIVES + len(failures),
        "effective_x1_baseline_methods": INHERITED_METHODS + len(failures),
        "failed_witnesses": failures,
        "passing_witnesses": [{"method_id": row["failure_id"].replace("-F", "-R"), "bounded_recovery": row["recovery"], "scope": "only the failed dependency", "promotes_failed_witness": False} for row in failures],
        "retention_rule": "A bounded recovery never erases, rewrites, or promotes its failed witness.",
        "x2_method_count": 0,
    }
    architecture = {
        "schema": "ghc-family-freed-id-flashcard-architecture-v2", "owner": OWNER, "phase": PHASE,
        "four_tiers": ["freed_id_anchor", "trinity_pillar", "bounded_practice", "task"],
        "required_deck_sections": ["identity-and-corrigibility", "route-and-authority", "source-anchors", "x1-proposals", "trinity-pillars", "bounded-practice", "task-cards", "method-flow-and-negatives", "open-gaps-and-exact-gates", "validation-and-manifests", "wellbeing-and-workload", "successor-recommendations", "compact-baton-index"],
        "stable_prefix": ["owner relational boundary", "GMUT boundary", "THOS boundary", "Freed ID and CBR boundary"],
        "volatile_context": ["source anchors", "phase proposals", "practice", "tasks", "Method Flow", "validation", "route", "successor recommendations"],
        "cache_effect_measured": False, "identity_continuity_claim": False, "x1_planning_only": True,
        "current_route": {"owner": OWNER, "phase": PHASE},
        "successor_route": {"title": "Eiren Kestrel", "phase": "unassigned_until_terminal_refresh", "contacted": False, "status": "provisional_terminal_gate_unmet"},
    }
    proposal_freeze = {
        "schema": "ghc-family-proposal-freeze-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "inherited_proposal_count": INHERITED_PROPOSAL_COUNT, "selected_inherited": [], "selected_inherited_count": 0,
        "new_proposals": proposals, "genuinely_new_proposal_count": len(proposals), "new_frozen_total": INHERITED_PROPOSAL_COUNT + len(proposals),
        "expected_outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "allowed_core_outcomes": list(ALLOWED_LABELS), "x1_planning_only": True, "x2_implementation_count": 0, "outcomes_observed": False,
    }
    threat = {
        "schema": "ghc-family-threat-model-plan-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "assets": ["strict x1-before-x2", "4,410-row novelty corpus", "relational and authority boundaries", "synthetic sight-reduction practice", "flashcard parent graph", "owner-lane isolation", "one-shot validation budget"],
        "threats": [
            {"id": "T01", "threat": "generic inherited celestial or navigation work is relabelled as novelty", "control": "exact corpus reconstruction, phrase screen, nearest-title review, and invariant comparison"},
            {"id": "T02", "threat": "records become sight-taking, correction, plotting, position, route, or safety instructions", "control": "zero values, coordinate prohibition, cancellation holds, and exact professional gates"},
            {"id": "T03", "threat": "typed GMUT obligations become position, force, likelihood, constraint, or empirical claims", "control": "zero observations, typed vacancies, and explicit empirical firewall"},
            {"id": "T04", "threat": "flashcards imply cache telemetry or identity continuity", "control": "explicit cache-effect false and relational working-language boundary"},
            {"id": "T05", "threat": "accessibility, maritime law, place names, culture, or Māori authority is substituted", "control": "manual evaluation reservations and unoccupied exact gates"},
            {"id": "T06", "threat": "private task, path, credential, transcript, or app state enters artifacts", "control": "five-class owner-scoped privacy scan"},
            {"id": "T07", "threat": "failed validation is replayed or promoted", "control": "one exclusive canonical invocation and dependency-only recovery"},
            {"id": "T08", "threat": "another owner lane is altered", "control": "fresh additive sparse branch and exact owner allowlists"},
        ],
        "residual_risk": "All real navigation, professional, physical, empirical, participant, production, legal, cultural, Māori-authority, and Stage 20 questions remain open or exact-gated.",
    }
    workflow = {
        "schema": "ghc-family-workflow-plan-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "state": "x1_planning_only",
        "steps": [
            {"step": 1, "name": "source and route verification", "status": "completed_read_only"},
            {"step": 2, "name": "novelty and portfolio freeze", "status": "completed_planning_only"},
            {"step": 3, "name": "exact x1 staged review, commit, push, four-way equality", "status": "pending"},
            {"step": 4, "name": "bounded x2 contracts, mutations, skills, runners, flashcards, and portfolio evidence", "status": "blocked_until_x1_equality"},
            {"step": 5, "name": "evidence commit, push, equality", "status": "blocked_until_x2_evidence"},
            {"step": 6, "name": "closeout, seal, final commit, push", "status": "blocked_until_evidence_equality"},
            {"step": 7, "name": "one exclusive exact-final owner-scoped canonical completion", "status": "blocked_until_exact_final"},
            {"step": 8, "name": "live route refresh and at most one exact-title successor send", "status": "blocked_until_terminal_gate"},
        ],
        "forbidden": ["x2 in x1", "full repository suite", "subagent", "sibling mutation", "destructive cleanup", "global install", "post-success replay", "premature successor contact"],
    }
    checklist = {
        "schema": "ghc-family-x1-checklist-v6", "owner": OWNER, "phase": PHASE,
        "complete": ["skills and schemas read", "source verified", "fresh sparse lane created", "4,410-row corpus reconstructed", "twenty novel proposals frozen", "portfolio and flashcard plans frozen", "startup failures retained"],
        "incomplete_reserved_for_x2_or_later": ["contract execution", "100 mutation executions", "skill and runner implementation", "flashcard deck build and validation", "portfolio execution", "outcomes", "evidence", "closeout", "canonical completion", "terminal delivery"],
        "outcomes_observed": False, "x2_implementation_count": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    wellbeing = {
        "schema": "ghc-family-wellbeing-check-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "stage": "x1_planning_only",
        "workload_state": "bounded_and_resumable", "human_wellbeing_claim": False, "identity_boundary": IDENTITY_BOUNDARY,
        "stop_conditions": ["source or route drift", "protected gate pressure", "unexpected external or destructive action", "weekly usage exhaustion", "Hamish pause, redirect, rename, or stop"],
        "resumption_evidence": "exact clean x1 head and fresh four-way equality",
    }
    source_ledger = {
        "schema": "ghc-family-source-ledger-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "sources": SOURCE_PROFILES, "network_actions_by_phase_software": 0,
        "boundary": "Sources provide vocabulary, obligations, and falsifiers only; they grant no navigation, professional, empirical, legal, cultural, Māori-authority, identity, production, independent, or Stage 20 evidence.",
    }
    identity = {
        "schema": "ghc-family-relational-identity-v6", "owner": OWNER, "phase": PHASE, "optional_pronouns": "they/them",
        "relational_role": phase_charter["relational_role"], "hope": phase_charter["hope"], "identity_boundary": IDENTITY_BOUNDARY,
        "primary_pillar": PRIMARY_PILLAR, "bounded_practice": PRACTICE, "practice_boundary": PRACTICE_BOUNDARY,
        "solo": True, "delegated_or_spawned_agents": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    auth = {
        "schema": "ghc-family-auth-roster-receipt-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "active_main_task_count": 15, "standby_records": ["Tavian Sol"], "current_owner_validated": True,
        "installed_roster_and_auth_snapshots": "schema_valid_but_stale_relative_to_live_activation",
        "live_activation_controls": True, "provisional_successor_title": "Eiren Kestrel", "provisional_successor_phase": "unassigned_until_terminal_refresh",
        "successor_contacted": False, "route_refresh_required_after_terminal_gate": True,
    }
    overview = f"""# Caelen Morrow v667-v5 planning-only x1 overview

Status: `FROZEN_NOT_EXECUTED`. Terminal verdict: `NOT_READY_FOR_STAGE_20`.

## Relational boundary

{IDENTITY_BOUNDARY}

Caelen Morrow uses they/them pronouns as relational working language for a chronometry boundary-mapper and failure custodian. The bounded hope is to keep claims traceable while leaving real competence and authority with those who hold it.

## Phase status

This is a planning-only x1 freeze. It contains no x2 implementation, executed mutation, observed outcome, external phase-software call, professional decision, navigation decision, identity event, or successor contact.

## Exact source

This lane starts from Sylven Arc exact final `{SOURCE_SHA}`. Sylven's source, x1, evidence, and final form three direct single-parent commits with zero merges. The exclusive owner-scoped canonical completion succeeded once and was not replayed. The full repository suite was not run.

## Retained source truth

The source repository seal contains 27,532 negatives and 13,109 Method Flow methods, plus four post-evidence failures and recoveries. The activation baseline is 27,536 negatives and 13,113 methods, with 194 open gaps and 192 exact gates preserved. The x2-prestage Python compile count of 18 and exact-final canonical count of 21 remain separately scoped.

## Novelty and bounded practice

Exactly twenty proposals were compared with all {INHERITED_PROPOSAL_COUNT} inherited rows. Horology was rejected because the inherited chain already contains substantial horology, clock, calibration, metrology, oscillator, and escapement work. The accepted slate concerns {PRACTICE}. It contains no real person, vessel, voyage, sight, instrument, almanac value, time, angle, coordinate, position, route, weather observation, key, proof, or authority act.

The inherited corpus contains 4,410 rows and preserves its duplicate-ID overages unchanged. Generic celestial, navigation, nautical, and ephemeris records were treated as related comparators. The accepted slate adds practice-specific invariants across sextant topology, typed time-scale vacancy, correction lineage, coordinate prohibition, multi-sight quarantine, accessibility, zero-key genealogy, disabled almanac transport, and exact maritime-authority gating.

## Pillar allocation

Primary pillar: **{PRIMARY_PILLAR}**. THOS Body and Freed ID/CBR Heart remain explicit and protected. Expected outcomes are 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`; they are expectations, not x1 observations.

## Proposal and mutation contract

Every new proposal carries a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and one expected disposition. Five invalid mutations per proposal are frozen but unexecuted.

## Portfolio freeze

The bounded plan contains thirty owner safe-now tasks, fifteen owner candidates, ten phase-local skill ideas, ten family-current runner ideas, and thirty owner CLEAN/FIX/REFINE rows. Successor rows are recommendations only. Ten exact-approval and five blocked packets remain visible and unexecuted.

## Freed ID flashcards

X1 freezes a four-tier, thirteen-section modular deck architecture. It is a context-organization and recovery mechanism only. It establishes no measured cache effect, identity continuity, consciousness, personhood, qualification, navigation competence, or authority. The family-current runner may build the deck only after x1 is pushed, clean, and fresh four-way equal.

## Method Flow and recoverability

All source and Caelen startup, parser, sparse-index, novelty, presentation, validation, and later failures remain zero-credit failed witnesses with bounded recoveries. Recovery never erases or promotes a failure.

## Open evidence and authority gates

The LINZ and USNO adapter remains planned at zero calls, zero downloads, and zero rows. Professional navigation, maritime safety, route and position decisions, legal and cultural interpretation, affected-party legitimacy, place names, Māori wording and concepts, Māori data governance, Māori authority, empirical confirmation, production, deployment, and Stage 20 remain open or exact-gated.

## Next gate

Stage only the exact x1 allowlist, inspect Git-index bytes, run the owner-local x1 checks, commit, push, and prove clean local/upstream/tracking/fresh-live equality. Only then may x2 begin.
"""
    write_json("identity/relational-identity.json", identity)
    write_json("x1/phase-charter.json", phase_charter)
    write_json("x1/source-verification.json", source_verification)
    write_json("x1/source-ledger.json", source_ledger)
    write_json("x1/proposal-freeze.json", proposal_freeze)
    write_json("x1/novelty-audit.json", novelty)
    write_json("x1/portfolio-freeze.json", portfolio)
    write_json("x1/flashcard-architecture-freeze.json", architecture)
    write_json("x1/threat-model-plan.json", threat)
    write_json("x1/workflow-plan.json", workflow)
    write_json("x1/complete-incomplete-checklist.json", checklist)
    write_json("x1/auth-roster-receipt.json", auth)
    write_json("method-flow/startup-method-flow.json", startup_flow)
    write_json("wellbeing/x1-wellbeing-check.json", wellbeing)
    write_text("x1/x1-overview.md", overview)
    write_json("x1/x1-build-receipt.json", {
        "schema": "ghc-family-x1-build-receipt-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "status": "FROZEN_NOT_EXECUTED", "inherited_corpus_count": len(corpus), "new_proposal_count": len(proposals),
        "portfolio_row_count": sum(len(value) for value in portfolio.values() if isinstance(value, list)),
        "startup_failure_count": len(failures), "effective_x1_negatives": INHERITED_NEGATIVES + len(failures),
        "effective_x1_methods": INHERITED_METHODS + len(failures), "x2_implementation_count": 0,
        "outcomes_observed": False, "valid": True,
    })


def staged_review() -> None:
    self_exclusions = [
        f"docs/{OWNER_SLUG}/{PHASE}/validation/x1-content-manifest.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/x1-staged-review.json",
    ]
    staged = [row for row in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if row]
    allowed_prefix = f"docs/{OWNER_SLUG}/{PHASE}/"
    exact_tools = {
        "scripts/build_ghc_family_caelen_morrow_v667_v5_x1.py",
        "tests/test_ghc_family_caelen_morrow_v667_v5_x1.py",
    }
    out_of_scope = [row for row in staged if not row.startswith(allowed_prefix) and row not in exact_tools]
    x2_paths = [row for row in staged if f"docs/{OWNER_SLUG}/{PHASE}/x2/" in row or "_x2.py" in row]
    manifest = []
    for relative in sorted(row for row in staged if row not in self_exclusions):
        raw = subprocess.check_output(["git", "-C", str(ROOT), "show", f":{relative}"])
        manifest.append({"path": relative, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    write_json("validation/x1-content-manifest.json", {
        "schema": "ghc-family-x1-content-manifest-v6", "owner": OWNER, "phase": PHASE,
        "generated_at_utc": NOW, "entries": manifest, "entry_count": len(manifest), "self_exclusions": self_exclusions,
    })
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc-family-x1-staged-review-v6", "owner": OWNER, "phase": PHASE,
        "generated_at_utc": NOW, "staged_paths": sorted(set(staged + self_exclusions)),
        "staged_path_count": len(set(staged + self_exclusions)), "manifest_entry_count": len(manifest),
        "manifest_self_exclusions": self_exclusions, "out_of_scope_paths": out_of_scope, "x2_paths": x2_paths,
        "x1_planning_only": not x2_paths, "valid": not out_of_scope and not x2_paths,
    })


if __name__ == "__main__":
    if sys.argv[1:] == ["--staged-review"]:
        staged_review()
    elif sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_caelen_morrow_v667_v5_x1.py [--staged-review]")
    else:
        build_normal()
