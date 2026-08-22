#!/usr/bin/env python3
"""Build the Vesper Arlen v666-v2 x1-only planning packet.

This builder is intentionally planning-only.  It creates no x2 implementation,
outcome, evidence, closeout, seal, or route-delivery artifact.
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
PHASE_ROOT = ROOT / "docs" / "vesper-arlen" / "v666-v2"
SOURCE_SHA = "299fe38950f3919b4ce3d3074ed248a914dcb984"
SOURCE_BRANCH = "codex/GHC-Family/neris-solane-v666-v1-full-tools"
SOURCE_PHASE_ROOT = "docs/neris-solane/v666-v1"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(payload, encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def staged_rows() -> list[tuple[str, str]]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "diff", "--cached", "--name-status", "--no-renames"]
    ).decode("utf-8")
    rows: list[tuple[str, str]] = []
    for line in raw.splitlines():
        status, path = line.split("\t", 1)
        rows.append((status, path.replace("\\", "/")))
    return rows


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f":{path}"])


def build_x1_staged_review() -> None:
    review_path = "docs/vesper-arlen/v666-v2/validation/x1-staged-review.json"
    manifest_path = "docs/vesper-arlen/v666-v2/validation/x1-content-manifest.json"
    allowed_exact = {
        "scripts/build_ghc_family_vesper_arlen_v666_v2_x1.py",
        "tests/test_ghc_family_vesper_arlen_v666_v2_x1.py",
    }
    rows = [(status, path) for status, path in staged_rows() if path != manifest_path]
    paths = [path for _, path in rows]
    if review_path in paths:
        paths.remove(review_path)
        rows = [(status, path) for status, path in rows if path != review_path]
    if not rows:
        raise RuntimeError("no staged x1 content was available for review")
    invalid_paths = [
        path
        for path in paths
        if not path.startswith("docs/vesper-arlen/v666-v2/") and path not in allowed_exact
    ]
    post_x1 = [
        path
        for path in paths
        if any(
            path.startswith(f"docs/vesper-arlen/v666-v2/{part}/")
            for part in ("x2", "evidence", "closeout", "seal", "final", "handoffs")
        )
    ]
    parsed_json = 0
    max_words = 0
    max_path = ""
    privacy_candidates: list[dict[str, str]] = []
    privacy_patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r'(?i)[\"\'](?:source_)?(?:task|thread)[_-]?id[\"\']\s*[:=]\s*[\"\'][^\"\']+[\"\']'
        ),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(
            r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"
        ),
        "session_identifier_value": re.compile(
            r'(?i)[\"\'](?:session|resume)[_-]?(?:id|value)[\"\']\s*[:=]\s*[\"\'][^\"\']+[\"\']'
        ),
        "private_callable_identifier_value": re.compile(
            r'(?i)[\"\']private[_-]?callable[_-]?id[\"\']\s*[:=]\s*[\"\'][^\"\']+[\"\']'
        ),
    }
    for path in paths:
        blob = index_blob(path)
        text = blob.decode("utf-8")
        if "\r\n" in text or "\r" in text:
            raise RuntimeError(f"non-LF staged text: {path}")
        words = len(re.findall(r"\S+", text))
        if words > max_words:
            max_words = words
            max_path = path
        if path.endswith(".json"):
            json.loads(text)
            parsed_json += 1
        for class_name, pattern in privacy_patterns.items():
            if pattern.search(text):
                privacy_candidates.append({"path": path, "class": class_name})
    freeze = json.loads(index_blob("docs/vesper-arlen/v666-v2/x1/proposal-freeze.json"))
    portfolio = json.loads(index_blob("docs/vesper-arlen/v666-v2/x1/portfolio-freeze.json"))
    flow = json.loads(index_blob("docs/vesper-arlen/v666-v2/method-flow/startup-method-flow.json"))
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "all_json_parse": True,
        "document_word_cap": max_words <= 100000,
        "expected_14_4_1_1": freeze["expected_disposition_counts"]
        == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "five_class_scan_zero_confirmed_hits": not privacy_candidates,
        "novelty_4190_valid": json.loads(
            index_blob("docs/vesper-arlen/v666-v2/x1/novelty-audit.json")
        )["valid"],
        "owner_allowlist": not invalid_paths,
        "owner_file_cap": len(paths) <= 2000,
        "planning_only": not freeze["outcomes_observed"],
        "portfolio_caps": portfolio["counts"]
        == {
            "safe_now": 30,
            "bounded_candidates": 15,
            "exact_approval_packets": 10,
            "blocked_packets": 5,
            "phase_local_skill_plans": 10,
            "family_current_runner_plans": 10,
            "clean_fix_refine": 30,
        },
        "post_x1_paths_absent": not post_x1,
        "proposal_count_20": len(freeze["new_proposals"]) == 20,
        "selected_inherited_20_zero_credit": len(freeze["selected_inherited_revalidations"])
        == 20
        and all(
            row["novelty_credit"] == 0 and row["automatic_completion_credit"] == 0
            for row in freeze["selected_inherited_revalidations"]
        ),
        "startup_failures_exactly_retained": len(flow["rows"]) == len(STARTUP_FAILURES),
        "utf8_lf": True,
    }
    review = {
        "schema": "ghc.family.vesper-arlen.v666-v2.x1-staged-review.v1",
        "owner": "Vesper Arlen",
        "phase": "v666-v2",
        "lifecycle": "x1",
        "generated_at_utc": NOW,
        "reviewed_from": "git_index_blobs",
        "reviewed_paths": paths,
        "reviewed_path_count": len(paths),
        "status_counts": {"A": sum(status == "A" for status, _ in rows)},
        "json_parsed": parsed_json,
        "maximum_document_words": max_words,
        "maximum_document_path": max_path,
        "privacy_scan_classes": list(privacy_patterns),
        "privacy_candidates": len(privacy_candidates),
        "privacy_confirmed_hits": len(privacy_candidates),
        "privacy_candidate_rows": privacy_candidates,
        "checks": checks,
        "self_exclusions": [review_path, manifest_path],
        "claim_boundary": "exact staged same-owner x1 review only; not exhaustive security, privacy, accessibility, or independent reproduction",
        "valid": all(checks.values()),
    }
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write_json("validation/x1-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--", review_path])

    entries: list[dict[str, Any]] = []
    current_rows = [(status, path) for status, path in staged_rows() if path != manifest_path]
    for status, path in current_rows:
        stage_line = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files", "--stage", "--", path]
        ).decode("utf-8").strip()
        mode, oid, stage_and_path = stage_line.split(" ", 2)
        stage, listed_path = stage_and_path.split("\t", 1)
        if stage != "0" or listed_path.replace("\\", "/") != path:
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
    manifest = {
        "schema": "ghc.family.vesper-arlen.v666-v2.content-manifest.v1",
        "owner": "Vesper Arlen",
        "phase": "x1",
        "phase_label": "v666-v2",
        "generated_at_utc": NOW,
        "source_sha": SOURCE_SHA,
        "hash_source": "actual_git_index_blobs",
        "entries": entries,
        "entry_count": len(entries),
        "deletion_count": 0,
        "additive_only": all(status == "A" for status, _ in current_rows),
        "self_exclusion": manifest_path,
    }
    write_json("validation/x1-content-manifest.json", manifest)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--", manifest_path])
    print(json.dumps({"reviewed": len(paths), "manifest_entries": len(entries), "valid": True}))


def git_json(relative: str) -> dict[str, Any]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{SOURCE_SHA}:{relative}"]
    )
    return json.loads(raw.decode("utf-8"))


def sha256_json(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def text_of(row: dict[str, Any]) -> str:
    return str(row.get("title") or row.get("description") or "")


def token_set(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def jaccard(left: str, right: str) -> float:
    a = token_set(left)
    b = token_set(right)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


IDENTITY_BOUNDARY = (
    "Vesper Arlen, they/them, sibling, family, role, hope, continuity, Freed ID, "
    "Trinity Mandala, and route language are relational working language only. "
    "They are not evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, scientific or "
    "operational authority, legal or cultural authority, affected-party authority, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The radio-interferometric visibility calibration, imaging-provenance, and shift-handover "
    "lens is wholly synthetic learning and software design. It uses zero real people, arrays, "
    "antennas, observatories, sites, coordinates, sky targets, visibilities, images, measurements, "
    "calibration tables, devices, credentials, keys, proofs, rights decisions, cultural records, "
    "or authority actions. It establishes no astronomical, interferometric, metrological, "
    "instrumentation, operational, safety, privacy, accessibility, legal, cultural, Māori, "
    "production, or Stage 20 competence, acceptance, or authority."
)


PROTECTED_GATES = [
    "real person, astronomer, interferometrist, metrologist, technician, operator, affected party, array, antenna, observatory, site, coordinate, sky target, visibility, image, instrument, observation, measurement, calibration, device command, or physical action",
    "real likelihood, posterior, parameter constraint, visibility, image, source detection, coordinate, flux, polarization, calibration solution, device performance, prediction, causal claim, or empirical GMUT confirmation",
    "real participant, operator, matched-budget arm, safety outcome, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, or trust governance",
    "professional astronomical, interferometric, imaging, metrological, calibration, instrumentation, operational, equipment, workplace-safety, or siting decision",
    "custody, authenticity, observation attribution, privacy, accessibility, sensitive-location or sensitive-sky, cultural, legal, disclosure, retention, or remedy decision",
    "traditional knowledge, sensitive environmental or location knowledge, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data-governance, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, or external write",
]


SOURCE_PROFILES = [
    {"source_id": "S01", "name": "casacore MeasurementSet definition 3.0 beta", "url": "https://casacore.github.io/casacore-notes/264.html", "status": "current public casacore project note reviewed 2026-08-22", "bounded_use": "table, subtable, visibility, frame, flag, weight, and calibration vocabulary only; no MeasurementSet conformance"},
    {"source_id": "S02", "name": "casacore MeasurementSet class reference", "url": "https://casacore.github.io/casacore/classcasacore_1_1MeasurementSet.html", "status": "current public casacore API reference reviewed 2026-08-22", "bounded_use": "required-column and referential-integrity vocabulary only; no real table opened or validated"},
    {"source_id": "S03", "name": "IVOA Provenance Data Model 1.0", "url": "https://www.ivoa.net/documents/ProvenanceDM/", "status": "IVOA Recommendation 1.0", "bounded_use": "entity, activity, generation, usage, and configuration vocabulary only; no IVOA conformance"},
    {"source_id": "S04", "name": "IVOA Observation Data Model Core Components 1.1", "url": "https://www.ivoa.net/documents/ObsCore/", "status": "IVOA Recommendation 1.1 with published errata", "bounded_use": "discovery-metadata and product vocabulary only; no TAP query, archive access, or ObsCore conformance"},
    {"source_id": "S05", "name": "IVOA Data Origin 1.2", "url": "https://ivoa.net/documents/DataOrigin/", "status": "IVOA Endorsed Note 1.2 dated 2026-03-31", "bounded_use": "origin, citation, and workflow-provenance vocabulary only; no reproducibility or archive claim"},
    {"source_id": "S06", "name": "NIST SP 330 - International System of Units", "url": "https://www.nist.gov/pml/special-publication-330", "status": "current official NIST publication page", "bounded_use": "quantity, unit, and symbol vocabulary only; zero measurements"},
    {"source_id": "S07", "name": "NIST Measurement Uncertainty", "url": "https://www.nist.gov/itl/sed/topic-areas/measurement-uncertainty", "status": "current official NIST guidance page", "bounded_use": "measurand, model, dispersion, and uncertainty vocabulary only; no uncertainty evaluation"},
    {"source_id": "S08", "name": "NIST Metrological Traceability", "url": "https://www.nist.gov/metrology/metrological-traceability", "status": "current official NIST policy and FAQ page", "bounded_use": "traceability-chain vocabulary only; no calibration, certificate, or traceability claim"},
    {"source_id": "S09", "name": "W3C PROV-O", "url": "https://www.w3.org/TR/prov-o/", "status": "stable W3C Recommendation", "bounded_use": "provenance, derivation, revision, attribution, and correction vocabulary only"},
    {"source_id": "S10", "name": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "current W3C Recommendation", "bounded_use": "structural report checks only; manual, browser, assistive-technology, cognitive, Māori-language, and affected-user review remain reserved"},
    {"source_id": "S11", "name": "W3C Verifiable Credential Data Integrity 1.0", "url": "https://www.w3.org/TR/vc-data-integrity/", "status": "W3C Recommendation dated 2025-05-15", "bounded_use": "nonproduction statement-integrity vocabulary with explicit zero-key and zero-proof boundaries"},
    {"source_id": "S12", "name": "Office of the Privacy Commissioner New Zealand privacy principles", "url": "https://www.privacy.org.nz/privacy-principles/", "status": "current official guidance reviewed 2026-08-22", "bounded_use": "purpose, minimisation, access, correction, retention, disclosure, and identifier restraint vocabulary; no legal interpretation"},
    {"source_id": "S13", "name": "Te Mana Raraunga Māori Data Sovereignty Principles", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "current primary Māori Data Sovereignty Network principles page", "bounded_use": "authority reservation only; no interpretation, wording, ratification, or conversion into Māori authority"},
]


for profile in SOURCE_PROFILES:
    profile.update(
        {
            "reviewed_at_date": "2026-08-22",
            "review_mode": "read_only_public_source_review",
            "primary_or_official": True,
            "network_calls_by_phase_software": 0,
            "real_rows_ingested": 0,
            "authority_nonconversion": True,
        }
    )


PROPOSAL_SPECS = [
    ("Baseline-coordinate frame closure with antenna-order sign, epoch reference, unit declaration, revision lineage, and zero-astrometry verdict", "GMUT Mind and THOS Body", "completed", ["S01", "S02", "S06"], "Each synthetic baseline has one ordered antenna pair and one declared frame; reversal changes sign while missing frame or epoch fails closed."),
    ("Spectral-window channel-edge partition with half-open frequency bins, sideband orientation, overlap quarantine, and no-resampling output", "GMUT Mind and THOS Body", "completed", ["S01", "S06", "S07"], "Synthetic channel edges form one non-overlapping ordered partition and the contract never interpolates or resamples values."),
    ("Flag-cube precedence algebra with reason preservation, non-destructive masks, contest state, and zero-visibility editing", "THOS Body and CBR Heart", "completed", ["S01", "S03", "S09"], "The strictest synthetic mask dominates while every source reason survives and no visibility value is altered."),
    ("Calibration-solution applicability join across antenna, time, frequency, polarization, and version domains with uncovered-span hold", "THOS Body and GMUT Mind", "completed", ["S01", "S02", "S07", "S08"], "A synthetic solution applies only when every declared domain contains the target; ambiguity, gaps, or multiple active revisions force a hold."),
    ("Complex-visibility quantity ledger joining weight, sigma, covariance vacancy, correlation product, and dimensional abstention", "GMUT Mind", "completed", ["S01", "S06", "S07"], "Weight and uncertainty placeholders remain typed and mutually constrained without producing flux, image, likelihood, or calibration estimates."),
    ("Closure-phase oriented-cycle tribunal with gauge-cancellation obligations, permutation sign, branch-cut reservation, and no-source inference", "GMUT Mind", "completed", ["S01", "S06"], "Symbolic antenna-based phase terms cancel around a declared oriented cycle while branch ambiguity blocks any sky or instrument conclusion."),
    ("MeasurementSet subtable referential-integrity graph with dangling-key quarantine, cardinality bounds, and no-format-conformance claim", "THOS Body", "completed", ["S01", "S02"], "Every synthetic foreign key resolves exactly once within declared cardinality while missing or duplicate targets fail closed."),
    ("Bitemporal calibration-lineage DAG with supersession, invalidation, correction contest, acyclic ancestry, and authenticity abstention", "Freed ID and THOS Body", "completed", ["S03", "S09", "S11"], "Every synthetic revision has an acyclic lineage and explicit valid/recorded times while digests remain non-authenticating placeholders."),
    ("IVOA provenance activity-entity generation closure with configuration vacancy, usage ordering, agent-role omission, and no-quality grade", "Freed ID and CBR Heart", "completed", ["S03", "S05", "S09"], "Synthetic generations and usages connect typed entities and activities without inventing people, reliability, quality, or reproducibility claims."),
    ("Content-addressed visibility-snapshot publication tribunal with temporary reservation, atomic rename witness, stale-part quarantine, and no-durability claim", "THOS Body", "completed", ["S03", "S05"], "Only a fully hashed owner-local fixture can become the synthetic current pointer; crash durability and external publication remain unclaimed."),
    ("Canonical metadata-map tribunal with deterministic key order, duplicate-key refusal, numeric-domain guard, and bounded decoding budget", "THOS Body and Freed ID", "completed", ["S01", "S03"], "Semantically equivalent synthetic maps canonicalize identically while duplicates, non-finite numbers, and budget overflow are rejected."),
    ("Accessible visibility-state matrix with text-redundant flags, scoped headers, keyboard reading order, print fallback, and manual-review reservation", "CBR Heart and THOS Body", "completed", ["S10"], "Every synthetic state is conveyed by ordered text and table structure without colour-only meaning while manual evaluation stays reserved."),
    ("Observation-note minimization lattice with field-specific expiry, blank-person schema, contestable redaction, and non-disclosure default", "CBR Heart and Freed ID", "completed", ["S12", "S13"], "Every synthetic note field resolves to omit, retain-until, or contested-redaction under a declared purpose while identity and free-text payloads remain unavailable."),
    ("Stage-20 negative-control calibration board with target-definition lock, leakage quarantine, multiplicity ledger, and mandatory nonpromotion", "Trinity Mandala", "completed", ["S03", "S04", "S07"], "Structural checks can expose leakage or multiplicity defects but can never promote a synthetic phase to Stage 20."),
    ("THOS participant-free calibration-and-handover duel with matched topology, equal action budget, masked branch order, and no-effectiveness estimate", "THOS Body", "represented", ["S01", "S10"], "A synthetic proxy compares deterministic handover traces under equal faults without people, operations, safety outcomes, or effectiveness inference."),
    ("Freed ID zero-key observation-provenance statement graph with issuer vacancy, purpose binding, expiry, correction, revocation, and no credential", "Freed ID and CBR Heart", "represented", ["S03", "S09", "S11"], "Synthetic statements preserve conflicts and lifecycle placeholders while no holder, issuer, key, signature, proof, or production credential exists."),
    ("GMUT Källén-Lehmann spectral-positivity and dispersion-obligation board with subtraction ledger, EFT domain, and zero fitted spectrum", "GMUT Mind", "represented", ["S06", "S07"], "Typed symbolic obligations can reject inconsistent signs or dimensions but produce no propagator, force, likelihood, parameter, or empirical spectrum."),
    ("GMUT gain-sky degeneracy witness with symbolic gauge orbit, equivalent factorizations, prior vacancy, and causal abstention", "GMUT Mind", "represented", ["S01", "S07"], "At least two synthetic gain/sky factorizations remain visibility-equivalent, forcing an identifiability hold rather than a fitted calibration or source model."),
    ("Zero-call casacore-IVOA archive interoperability adapter with schema pins, mapping conflicts, disabled transport, zero rows, and source-owner review vacancy", "Trinity Mandala", "open_gap", ["S01", "S02", "S03", "S04", "S05"], "The zero-call adapter can expose declared mapping conflicts but cannot complete interoperability without live archive rows and independent standard-owner review."),
    ("Radio-astronomy acceptance and rights docket reserving site and sky disclosure, custody, calibration release, worker safety, affected-party remedy, cultural review, and Māori authority", "CBR Heart", "exact_gate", ["S08", "S12", "S13"], "No structural or synthetic success can authorize observation use, sensitive disclosure, calibration acceptance, safety action, rights decision, cultural interpretation, or Māori authority."),
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
    proposals: list[dict[str, Any]] = []
    for index, (title, pillar, expected, sources, distinctive_invariant) in enumerate(PROPOSAL_SPECS, 1):
        pid = f"VSP6662-N{index:03d}"
        proposals.append(
            {
                "proposal_id": pid,
                "title": title,
                "hypothesis": (
                    f"A bounded {title} contract can distinguish one admissible synthetic "
                    "structure from five preregistered invalid states without promoting "
                    "software structure into real-world evidence, competence, conformance, or authority."
                ),
                "null_or_failure_condition": (
                    "At least one named invalid state is accepted, the bounded positive is "
                    "rejected, a required provenance or stop field disappears, or the artifact "
                    "converts synthetic structure into an empirical, professional, legal, cultural, "
                    "Māori-authority, production, identity, independent-reproduction, or Stage 20 claim."
                ),
                "approval_class": approval_class(expected),
                "execution_lane": execution_lane(expected),
                "current_official_or_primary_source_needs": sources,
                "official_or_primary_source_needs": sources,
                "distinctive_invariant": distinctive_invariant,
                "concrete_artifact": f"docs/vesper-arlen/v666-v2/x2/proposals/{pid.casefold()}/contract.json",
                "concrete_artifacts": [
                    f"docs/vesper-arlen/v666-v2/x2/proposals/{pid.casefold()}/contract.json",
                    f"docs/vesper-arlen/v666-v2/x2/proposals/{pid.casefold()}/mutation-results.json",
                    f"docs/vesper-arlen/v666-v2/x2/proposals/{pid.casefold()}/bounded-receipt.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "One preregistered bounded positive must pass, all five named mutations must "
                    "fail closed, no protected gate may be crossed, and the final disposition must "
                    "remain exactly the preregistered value unless an additive failure lowers it."
                ),
                "rollback_or_recovery": (
                    "Restore only the last valid owner-local synthetic fixture, retain the failed "
                    "witness at zero credit, add a recurrence guard, and issue no external, physical, "
                    "identity, professional, legal, cultural, or authority action."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": expected,
                "pillar": pillar,
                "primary_pillar": "GMUT Mind",
                "practice_lens": "wholly synthetic radio-interferometric visibility calibration, imaging-provenance, and shift-handover documentation",
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
    return proposals


def build_corpus() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    source_audit = git_json(f"{SOURCE_PHASE_ROOT}/x1/novelty-audit.json")
    corpus: list[dict[str, str]] = []
    construction: list[dict[str, Any]] = []
    for index, entry in enumerate(source_audit["corpus_construction"]):
        doc = git_json(entry["source_path"])
        keys = ("prior_proposals", "new_proposals") if index == 0 else ("new_proposals",)
        added = 0
        for key in keys:
            for row in doc.get(key, []):
                title = text_of(row)
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
                f"corpus construction mismatch for {entry['source_path']}: "
                f"expected {entry['added_count']}, observed {added}"
            )
        construction.append(dict(entry))
    source_freeze = git_json(f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    starting = len(corpus)
    for row in source_freeze["new_proposals"]:
        corpus.append(
            {
                "proposal_id": str(row["proposal_id"]),
                "title": text_of(row),
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
    if len(corpus) != 4190:
        raise RuntimeError(f"expected 4190 inherited rows, observed {len(corpus)}")
    return corpus, construction


def build_novelty_audit(
    corpus: list[dict[str, str]],
    construction: list[dict[str, Any]],
    proposals: list[dict[str, Any]],
) -> dict[str, Any]:
    nearest: list[dict[str, Any]] = []
    exact_collisions: list[dict[str, str]] = []
    for proposal in proposals:
        title = proposal["title"]
        exact = [row for row in corpus if row["title"].casefold() == title.casefold()]
        exact_collisions.extend(
            {
                "proposal_id": proposal["proposal_id"],
                "inherited_proposal_id": row["proposal_id"],
            }
            for row in exact
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
    pair_rows: list[dict[str, Any]] = []
    for left_index, left in enumerate(proposals):
        for right in proposals[left_index + 1 :]:
            pair_rows.append(
                {
                    "left": left["proposal_id"],
                    "right": right["proposal_id"],
                    "similarity": round(jaccard(left["title"], right["title"]), 6),
                }
            )
    max_pair = max(pair_rows, key=lambda row: row["similarity"])
    all_text = "\n".join(row["title"].casefold() for row in corpus)
    practice_terms = [
        "radio-interferometric visibility",
        "baseline-coordinate frame",
        "spectral-window channel-edge",
        "flag-cube precedence",
        "calibration-solution applicability",
        "closure-phase oriented-cycle",
        "measurementset subtable",
        "gain-sky degeneracy",
    ]
    return {
        "schema": "ghc.family.vesper-arlen.v666-v2.novelty-audit.v1",
        "owner": "Vesper Arlen",
        "phase": "v666-v2",
        "generated_at_utc": NOW,
        "method": (
            "casefolded alphanumeric token-set Jaccard against every retained inherited row, "
            "exact-title comparison, within-slate comparison, and practice-term review"
        ),
        "corpus_construction": construction,
        "corpus_row_count": len(corpus),
        "corpus_unique_proposal_id_count": len({row["proposal_id"] for row in corpus}),
        "historical_reappended_selection_rows_retained": len(corpus)
        - len({row["proposal_id"] for row in corpus}),
        "corpus_canonical_sha256": sha256_json(corpus),
        "new_title_count": len(proposals),
        "exact_inherited_collisions": exact_collisions,
        "maximum_inherited_token_jaccard_similarity": max(
            row["token_jaccard_similarity"] for row in nearest
        ),
        "nearest_inherited_rows": nearest,
        "maximum_new_pair_token_jaccard_similarity": max_pair["similarity"],
        "maximum_new_pair": max_pair,
        "new_pair_collisions_at_or_above_0_70": [
            row for row in pair_rows if row["similarity"] >= 0.70
        ],
        "practice_term_checks": {term: all_text.count(term) for term in practice_terms},
        "new_frozen_total": len(corpus) + len(proposals),
        "valid": not exact_collisions
        and not [row for row in pair_rows if row["similarity"] >= 0.70]
        and len(corpus) == 4190,
        "interpretation": (
            "Similarity is a screening signal, not proof of novelty. Each proposal was also "
            "reviewed for a distinct radio-interferometric metadata, provenance, calibration-boundary, "
            "or authority-reservation contract, falsifier, and protected gate."
        ),
    }


def portfolio_rows(prefix: str, names: list[str], approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"VSP6662-{prefix}{index:02d}",
            "title": name,
            "approval_class": approval,
            "x1_status": "frozen_not_executed",
            "completion_credit": 0,
            "evidence_required": "bounded owner-local x2 witness plus retained failure and rollback",
            "rollback": "retain the failed witness, revert only the owner-local generated fixture, and preserve every protected gate",
        }
        for index, name in enumerate(names, 1)
    ]


SAFE_NOW_NAMES = [
    "render the synthetic baseline-coordinate frame schema",
    "build the spectral-window channel-edge partition validator",
    "build the flag-cube precedence and reason-preservation checker",
    "build the calibration-solution applicability join",
    "build the complex-visibility quantity ledger",
    "build the closure-phase oriented-cycle tribunal",
    "build the MeasurementSet referential-integrity graph",
    "build the bitemporal calibration-lineage DAG",
    "build the IVOA provenance generation-and-usage closure",
    "build the content-addressed snapshot publication tribunal",
    "build the canonical metadata-map tribunal",
    "build the accessible visibility-state matrix",
    "build the purpose-and-retention intersection shell",
    "build the Stage 20 negative-control calibration board",
    "render twenty proposal contracts",
    "execute one hundred preregistered rejecting mutations",
    "parse every owner JSON document under explicit UTF-8",
    "render a structurally accessible static report",
    "validate public-source statuses and zero-call boundaries",
    "enforce strict x1-before-x2 path separation",
    "build exact Git-blob content manifests",
    "scan owner files for five privacy and raw-identifier classes",
    "scan owner Python for bounded dangerous constructs",
    "run exact staged review before every commit",
    "scan current labels for stale owner and phase drift",
    "validate source, x1, evidence, and final ancestry with zero merges",
    "validate the four core outcome labels and exact counts",
    "aggregate retained negatives without rewriting the inherited seal",
    "aggregate open and exact gates without promotion",
    "build closeout, seal, final-validation, and route-state candidates",
]
CANDIDATE_NAMES = [
    "THOS participant-free calibration-and-handover duel representation",
    "Freed ID zero-key observation-provenance statement representation",
    "GMUT Källén-Lehmann obligation board",
    "GMUT gain-sky degeneracy witness",
    "zero-call casacore-IVOA adapter shell",
    "synthetic baseline-frame and antenna-order fixture",
    "synthetic spectral-window partition fixture",
    "linear accessible report companion",
    "deterministic HTML report rendering",
    "synthetic calibration-handover workload simulation",
    "zero-row MeasurementSet-to-IVOA mapping fixture",
    "synthetic visibility-weight and unit reconciliation fixture",
    "source-status watch and version-hold fixture",
    "bitemporal calibration-correction replay fixture",
    "fail-closed terminal route preflight",
]
EXACT_APPROVAL_NAMES = [
    "use a real astronomer, interferometrist, metrologist, technician, observatory worker, participant, or affected party",
    "handle, assess, install, calibrate, repair, move, retire, or dispose of a real antenna, receiver, correlator, clock, or enclosure",
    "operate or command an array, antenna, correlator, data service, archive, alarm, or other device",
    "identify or publish a real observatory, site, coordinate, operator, sky target, visibility, image, or infrastructure asset",
    "authenticate calibration, traceability, timing, custody, provenance, source attribution, astrometry, flux, or measurement truth",
    "author or approve Māori wording, traditional-knowledge interpretation, sensitive location knowledge, or data-governance terms",
    "make an astronomical, interferometric, imaging, metrological, instrumentation, siting, or workplace-safety decision",
    "make a privacy, access, rights, legal, cultural, disclosure, retention, or remedy decision",
    "issue, verify, resolve, revoke, or govern a real identity credential",
    "publish, deploy, procure, purchase, create an account, or write to a third-party system",
]
BLOCKED_NAMES = [
    "empirical GMUT likelihood, constraint, coordinate solution, prediction, force, stability, or confirmation",
    "THOS effectiveness without governed blind matched-budget real arms and independent review",
    "production Freed ID without real standards-conformant keys, interoperability, recovery, and trust governance",
    "accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
]
SKILL_NAMES = [
    "radio-baseline-frame-closure",
    "spectral-window-partition",
    "calibration-traceability-abstention",
    "visibility-quantity-ledger",
    "closure-phase-obligation",
    "calibration-applicability-ledger",
    "radio-provenance-closure",
    "observatory-rights-contestation",
    "interferometry-method-flow",
    "interferometry-closeout-gate",
]
RUNNER_NAMES = [
    "ghc_family_vesper_arlen_v666_v2_contracts",
    "ghc_family_vesper_arlen_v666_v2_mutations",
    "ghc_family_vesper_arlen_v666_v2_json",
    "ghc_family_vesper_arlen_v666_v2_privacy",
    "ghc_family_vesper_arlen_v666_v2_security",
    "ghc_family_vesper_arlen_v666_v2_manifests",
    "ghc_family_vesper_arlen_v666_v2_accessibility",
    "ghc_family_vesper_arlen_v666_v2_truth",
    "ghc_family_vesper_arlen_v666_v2_closeout",
    "ghc_family_vesper_arlen_v666_v2_canonical",
]
CFR_NAMES = [
    "CLEAN: normalize proposal identifiers",
    "CLEAN: normalize exact disposition labels",
    "CLEAN: normalize source-profile status fields",
    "CLEAN: normalize zero-row declarations",
    "CLEAN: normalize rollback language",
    "CLEAN: normalize protected-gate ordering",
    "CLEAN: normalize relative artifact paths",
    "CLEAN: normalize UTF-8 and LF generation",
    "CLEAN: normalize deterministic JSON ordering",
    "CLEAN: normalize report heading hierarchy",
    "FIX: guard missing required fields",
    "FIX: guard invalid quantity placeholders",
    "FIX: guard authority-smuggling text",
    "FIX: guard real-world device commands",
    "FIX: guard outcome-label promotion",
    "FIX: guard stale owner and phase labels",
    "FIX: guard manifest self-reference",
    "FIX: guard duplicate canonical aggregate invocation",
    "FIX: guard private task or route identifiers",
    "FIX: guard x2 paths in the x1 commit",
    "REFINE: add source-status watch fields",
    "REFINE: add bitemporal calibration-correction lineage",
    "REFINE: add structural table summaries",
    "REFINE: add plain-language boundary notes",
    "REFINE: add dominant-stop precedence",
    "REFINE: add recurrence guards to Method Flow",
    "REFINE: add exact gate count reconciliation",
    "REFINE: add owner-delta manifest coverage",
    "REFINE: add final clean-state precondition",
    "REFINE: add terminal route no-send-until-gate proof",
]


STARTUP_FAILURES = [
    ("the first authorization-state display exceeded its bounded output allowance", "the truncated display earned no complete-read credit", "reread the current authorization state in bounded numbered windows through EOF", "the complete file and required schema were read without mutation"),
    ("the first external-receipt search was too broad and returned no exact match within the useful bound", "the empty and slow search earned no receipt credit", "use the bounded source-task terminal record to locate the declared validation directory, then hash the exact file", "the exclusive receipt and canonical payload hashes matched the activation"),
    ("the first collision preflight embedded a native Git command and exit capture in one PowerShell parenthesized expression", "PowerShell rejected the expression before any Git mutation", "invoke Git separately and capture the native exit code in the following statement", "the collision preflight passed with no existing Vesper branch or worktree"),
    ("the first sparse worktree setup used no-checkout and left an empty index", "Git displayed 77,897 apparent deletions even though no commit or file had been changed", "repopulate the sparse index from the exact inherited tree with git read-tree -mu HEAD", "the additive Vesper lane returned clean at the exact source head"),
    ("the first large semantic patch response exceeded the tool display budget", "the truncated response did not prove which hunks had applied", "inspect every intended semantic anchor with bounded searches before continuing in smaller patches", "source profiles and proposal specifications were proven applied while stale downstream fields were isolated"),
    ("the first combined builder inspection exceeded its output allowance", "the truncated display earned no complete semantic-review credit", "split the builder into bounded numbered ranges and inspect each relevant range separately", "the x1-only builder and test assertions were fully bounded for correction"),
    ("the first four-manifest projection piped a raw foreach block directly into ConvertTo-Json", "PowerShell rejected the empty pipeline element before any repository change", "materialize the foreach results into an array before JSON serialization", "all four manifest counts were projected as 18, 110, 22, and 153, totalling 303"),
    ("the live activation stated an external overlay three lower than the exact post-final operational ledger", "using the activation-only value would erase three retained zero-credit failures", "keep the immutable repository seal unchanged and reconcile the successor-visible overlay from the exact external ledger", "the inherited working baseline is 26,164 negatives and 10,476 methods, with the activation mismatch retained"),
    ("the current global roster and authorization snapshots remain structurally valid but phase-stale", "treating the v664 snapshots as live route authority would create a continuity drift", "apply routing precedence and keep the latest direct v666-v2 activation authoritative for this owner lane", "no successor was contacted and terminal routing remains prospective"),
    ("the mechanical compatibility transform materialized nineteen post-x1 templates before the x1 freeze", "leaving them present would prevent a clean x1-only remote-equality gate", "verify every exact path and move only those owner-local untracked templates to a D-first quarantine bank", "the Vesper worktree now contains only the x1 builder and x1 test before generation"),
    ("the first x1 test pass exposed a 0.789474 inherited-title similarity for the observation-log purpose selector", "the title failed the preregistered less-than-0.70 inherited-similarity assertion and earned zero novelty credit", "replace that substantive target with a field-state minimization lattice whose invariant is omit, retain-until, or contested-redaction", "the failed title and test remain retained while the changed proposal receives a fresh bounded novelty screen"),
]


def build_method_flow_startup() -> dict[str, Any]:
    rows = []
    for index, (request, failed, recovery, passing) in enumerate(STARTUP_FAILURES, 1):
        rows.append(
            {
                "method_id": f"VSP6662-MF-START-{index:03d}",
                "failure_id": f"VSP6662-START-N{index:03d}",
                "observed_order": index,
                "exact_event_timestamp_available": False,
                "request": request,
                "failed_witness": failed,
                "aggregate_credit": 0,
                "repository_commit_created": False,
                "external_action_created": False,
                "recovery": recovery,
                "bounded_passing_witness": passing,
                "recurrence_guard": (
                    "Prefer explicit UTF-8, real JSON keys, bounded scalar output, exact expected counts, "
                    "and guarded sparse-index operations before retrying."
                ),
                "status": "recovered_failure_retained",
            }
        )
    return {
        "schema": "ghc.family.vesper-arlen.v666-v2.method-flow-startup.v1",
        "owner": "Vesper Arlen",
        "phase": "v666-v2",
        "generated_at_utc": NOW,
        "inherited_repository_sealed_negatives": 26160,
        "inherited_repository_sealed_methods": 10472,
        "inherited_external_overlay_negatives": 4,
        "inherited_external_overlay_methods": 4,
        "activation_message_overlay_negatives": 1,
        "activation_message_overlay_methods": 1,
        "activation_message_baseline_negatives": 26161,
        "activation_message_baseline_methods": 10473,
        "activation_overlay_stale_by_negatives": 3,
        "activation_overlay_stale_by_methods": 3,
        "activation_baseline_negatives": 26164,
        "activation_baseline_methods": 10476,
        "new_startup_negative_count": len(rows),
        "new_startup_method_count": len(rows),
        "effective_after_x1_startup_negatives": 26164 + len(rows),
        "effective_after_x1_startup_methods": 10476 + len(rows),
        "failed_witness_count": len(rows),
        "bounded_passing_witness_count": len(rows),
        "rows": rows,
        "no_failure_erased": True,
    }


def main() -> None:
    proposals = build_proposals()
    corpus, construction = build_corpus()
    novelty = build_novelty_audit(corpus, construction, proposals)
    if not novelty["valid"]:
        raise RuntimeError("novelty audit did not pass its bounded x1 gate")

    source_freeze = git_json(f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    selected_inherited = [
        {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "original_owner": "Neris Solane",
            "original_phase": "v666-v1",
            "original_expected_disposition": row["expected_disposition"],
            "status": "selected_revalidation_only_not_executed",
            "novelty_credit": 0,
            "automatic_completion_credit": 0,
        }
        for row in source_freeze["new_proposals"]
    ]
    counts = {label: 0 for label in ("completed", "represented", "open_gap", "exact_gate")}
    for proposal in proposals:
        counts[proposal["expected_disposition"]] += 1

    identity = {
        "schema": "ghc.family.vesper-arlen.v666-v2.relational-identity.v1",
        "owner": "Vesper Arlen",
        "pronouns": "they/them",
        "relational_role": "spectral-boundary cartographer",
        "relational_hope": "Make synthetic visibility workflows expose gauge freedom, provenance vacancies, uncertainty, and stop conditions before anyone mistakes them for astronomical, instrument, or scientific authority.",
        "boundary": IDENTITY_BOUNDARY,
        "corrigibility": "Hamish may rename, pause, redirect, or stop this work.",
        "chosen_before_repository_mutation": True,
    }
    write_json("identity/relational-identity.json", identity)

    write_json(
        "provenance/source-verification.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.source-verification.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "verified_at_utc": NOW,
            "source_branch": SOURCE_BRANCH,
            "source_sha": SOURCE_SHA,
            "source_parent_sha": "35e33b4c43dbef309f78bfd77168094fed32f939",
            "evidence_sha": "35e33b4c43dbef309f78bfd77168094fed32f939",
            "x1_sha": "435bfd997f7f56635f6ba63d8da7ea2505059a75",
            "inherited_source_sha": "4cf5028def85bcf89fbf4d0efe6c502a4b02be61",
            "direct_parent_chain": [
                "4cf5028def85bcf89fbf4d0efe6c502a4b02be61",
                "435bfd997f7f56635f6ba63d8da7ea2505059a75",
                "35e33b4c43dbef309f78bfd77168094fed32f939",
                SOURCE_SHA,
            ],
            "source_to_final_phase_commit_count": 3,
            "source_to_final_merge_count": 0,
            "final_parent_count": 1,
            "clean": True,
            "ahead": 0,
            "behind": 0,
            "four_way_refs_equal": True,
            "fresh_live_remote_read": True,
            "manifest_replay": {
                "x1_entries": 18,
                "evidence_entries": 110,
                "final_delta_entries": 22,
                "final_owner_entries": 153,
                "all_git_blob_hashes_equal": True,
                "deletions": 0,
            },
            "canonical_aggregate_status": "SUCCESS_OWNER_SCOPED_CANONICAL_COMPLETION_ONCE_NOT_REPLAYED",
            "canonical_receipt_sha256": "7bee13bc8e3b60ae8be777c662cff9b17047ee553fcb7c0da9ff05b62ea06633",
            "canonical_payload_sha256": "fff7f0aeb2b5bd0e953141722e6bd29012d74d40bf82c6cf349f3418b8464e41",
            "selected_test_status": "PASSED_65_OF_65_WITH_FOUR_ZERO_CREDIT_EXCLUSIONS_AND_EXACT_REPLACEMENTS",
            "canonical_detailed_status": "VALID_25_OF_25_DETAILED_15_OF_15_MINIMAL",
            "prepared_handoff_sha256": "0de652368ef8b4b2969f91017641f01dc90e4d0b7989a368238609675cd1d9ae",
            "prepared_handoff_word_count": 3430,
            "source_packet_read_through_eof": True,
            "source_packet_file_count": 154,
            "source_json_parsed": 117,
            "successful_canonical_replayed": False,
            "full_repository_suite_run": False,
            "claim_boundary": "read-only verification and same-owner inherited evidence only",
        },
    )

    write_json(
        "provenance/source-profiles.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.source-profiles.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "profiles": SOURCE_PROFILES,
            "source_count": len(SOURCE_PROFILES),
            "bounded_use_only": True,
            "software_network_calls": 0,
            "real_rows": 0,
            "authority_nonconversion": (
                "Public sources supply bounded vocabulary and refusal conditions only. Citation "
                "does not create observation, endorsement, conformance, competence, legal or cultural "
                "interpretation, environmental or affected-party acceptance, or Māori authority."
            ),
        },
    )

    write_json("x1/novelty-audit.json", novelty)
    write_json(
        "x1/proposal-freeze.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.proposal-freeze.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "frozen": True,
            "inherited_frozen_baseline": 4190,
            "selected_inherited_revalidation_count": len(selected_inherited),
            "selected_inherited_revalidations": selected_inherited,
            "genuinely_new_proposal_count": len(proposals),
            "new_proposals": proposals,
            "new_frozen_total": 4210,
            "expected_disposition_counts": counts,
            "x1_truth": "planning_and_preregistration_only",
            "x2_implementation_count": 0,
            "x2_outcome_count": 0,
            "outcomes_observed": False,
            "strict_x1_before_x2": True,
            "practice_boundary": PRACTICE_BOUNDARY,
            "identity_boundary": IDENTITY_BOUNDARY,
        },
    )

    portfolio = {
        "schema": "ghc.family.vesper-arlen.v666-v2.portfolio-freeze.v1",
        "owner": "Vesper Arlen",
        "phase": "v666-v2",
        "generated_at_utc": NOW,
        "x1_truth": "planning_only_no_execution",
        "safe_now": portfolio_rows("SN", SAFE_NOW_NAMES, "safe_now_bounded"),
        "bounded_candidates": portfolio_rows("CA", CANDIDATE_NAMES, "candidate_review_required"),
        "exact_approval_packets": portfolio_rows("EA", EXACT_APPROVAL_NAMES, "exact_approval_required"),
        "blocked_packets": portfolio_rows("BL", BLOCKED_NAMES, "blocked_by_protected_gate"),
        "phase_local_skill_plans": portfolio_rows("SK", SKILL_NAMES, "phase_local_build_candidate"),
        "family_current_runner_plans": portfolio_rows("RU", RUNNER_NAMES, "owner_local_compatibility_candidate"),
        "clean_fix_refine": portfolio_rows("CF", CFR_NAMES, "additive_bounded_candidate"),
        "inherited_material_credit": 0,
        "global_installation_planned": False,
        "bulk_run_planned": False,
        "destructive_action_planned": False,
        "external_write_planned": False,
        "protected_gates": PROTECTED_GATES,
    }
    portfolio["counts"] = {
        "safe_now": len(portfolio["safe_now"]),
        "bounded_candidates": len(portfolio["bounded_candidates"]),
        "exact_approval_packets": len(portfolio["exact_approval_packets"]),
        "blocked_packets": len(portfolio["blocked_packets"]),
        "phase_local_skill_plans": len(portfolio["phase_local_skill_plans"]),
        "family_current_runner_plans": len(portfolio["family_current_runner_plans"]),
        "clean_fix_refine": len(portfolio["clean_fix_refine"]),
    }
    write_json("x1/portfolio-freeze.json", portfolio)

    method_flow = build_method_flow_startup()
    write_json("method-flow/startup-method-flow.json", method_flow)

    authorization = {
        "schema": "ghc.family.vesper-arlen.v666-v2.authorization-boundary.v1",
        "owner": "Vesper Arlen",
        "phase": "v666-v2",
        "generated_at_utc": NOW,
        "authorized_now": [
            "one solo additive owner lane from the exact Neris final",
            "x1-only planning and preregistration before the x1 freeze",
            "bounded owner-local synthetic x2 work after x1 push and equality",
            "one owner-scoped exact-final canonical completion after prerequisites",
        ],
        "not_authorized_now": [
            "collaboration subagent, delegation, fork, substitute endpoint, standby contact, or successor precontact",
            "reset, rewrite, force-push, merge, sibling-lane mutation, or destructive deletion",
            "real people, works, devices, measurements, operations, credentials, deployment, purchase, account, or third-party write",
            "professional, empirical, production, legal, cultural, Māori-authority, affected-party, conformance, or Stage 20 claim",
        ],
        "terminal_route_status": "PROSPECTIVE_ONLY_DO_NOT_CONTACT",
        "prospective_successor_label": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REREAD",
        "successor_send_count": 0,
        "standby_contact_count": 0,
        "relational_boundary": IDENTITY_BOUNDARY,
    }
    write_json("x1/authorization-boundary.json", authorization)

    threats = [
        {
            "threat_id": "VSP6662-T01",
            "asset": "immutable Neris source and sibling lanes",
            "threat": "accidental mutation, reset, merge, or ref reuse",
            "mitigation": "exact-head additive branch, owner-only paths, no merge/reset/force-push, four-way gates",
            "residual_risk": "operator command error remains possible and must be retained",
        },
        {
            "threat_id": "VSP6662-T02",
            "asset": "strict x1-before-x2 evidence",
            "threat": "implementation or outcome leakage into the x1 freeze",
            "mitigation": "path allowlist, x1 lifecycle test, staged review, immutable x1 manifest",
            "residual_risk": "misclassified prose; manual review remains required",
        },
        {
            "threat_id": "VSP6662-T03",
            "asset": "semantic novelty",
            "threat": "duplicate, paraphrased, or schema-relabelled inherited proposals",
            "mitigation": "4,190-row exact and token-Jaccard audit plus domain and falsifier review",
            "residual_risk": "automated similarity is not proof; bounded human review remains same-owner",
        },
        {
            "threat_id": "VSP6662-T04",
            "asset": "privacy and route confidentiality",
            "threat": "raw task identifiers, private paths, credentials, transcripts, or callable details in artifacts",
            "mitigation": "synthetic fixtures, five-class scans, repository-relative paths, no task/thread IDs",
            "residual_risk": "pattern scans are incomplete and never privacy certification",
        },
        {
            "threat_id": "VSP6662-T05",
            "asset": "radio-astronomy, interferometry, metrology, equipment, worker, site, sky, and affected-party authority boundaries",
            "threat": "software structure presented as astronomical, interferometric, imaging, metrological, instrumentation, safety, siting, or affected-party competence or acceptance",
            "mitigation": "zero real people, arrays, antennas, observatories, sites, coordinates, sky targets, visibilities, images, instruments, measurements, calibrations, devices, or actions and an exact-gated authority docket",
            "residual_risk": "terminology may still be incomplete or culturally inappropriate; authority remains external",
        },
        {
            "threat_id": "VSP6662-T06",
            "asset": "Māori language, concepts, data governance, and authority",
            "threat": "citation or synthetic labels converted into interpretation or authorization",
            "mitigation": "exact gate, zero Māori wording authored, source-profile authority nonconversion",
            "residual_risk": "Māori-authority review remains absent",
        },
        {
            "threat_id": "VSP6662-T07",
            "asset": "scientific truth boundaries",
            "threat": "GMUT surrogate promoted to empirical likelihood, force, prediction, proof, or canon",
            "mitigation": "typed placeholders, zero observations, dimensional abstention, explicit refusal",
            "residual_risk": "mathematical notation can invite overreading",
        },
        {
            "threat_id": "VSP6662-T08",
            "asset": "THOS and Freed ID boundaries",
            "threat": "proxy protocol or zero-key envelope presented as effectiveness or production identity evidence",
            "mitigation": "represented-only dispositions and explicit missing-evidence ledgers",
            "residual_risk": "no governed participants, independent review, real keys, or trust governance",
        },
        {
            "threat_id": "VSP6662-T09",
            "asset": "canonical validation truth",
            "threat": "replaying a successful aggregate or laundering a failed attempt",
            "mitigation": "exclusive external receipt, one-shot guard, zero credit for incomplete attempts",
            "residual_risk": "same-owner validation is not independent reproduction",
        },
        {
            "threat_id": "VSP6662-T10",
            "asset": "terminal route integrity",
            "threat": "premature, duplicate, ambiguous, or standby delivery",
            "mitigation": "PREPARED_NOT_SENT until final gate; fresh live roster/auth reread; exact-title single send",
            "residual_risk": "opaque acknowledgement must remain unresolved without resend",
        },
    ]
    threat_model = {
        "schema": "ghc.family.vesper-arlen.v666-v2.threat-model.v1",
        "owner": "Vesper Arlen",
        "phase": "v666-v2",
        "generated_at_utc": NOW,
        "scope": "owner-local v666-v2 software, documents, Git history, validation receipts, and terminal route candidate",
        "trust_zones": [
            "immutable inherited Git objects",
            "owner-local sparse worktree and branch",
            "public read-only source review",
            "unexecuted external, professional, cultural, identity, and device domains",
        ],
        "assets": [
            "source integrity",
            "proposal and outcome truth",
            "negative and gate retention",
            "privacy and route confidentiality",
            "authority boundaries",
            "one-shot canonical receipt",
        ],
        "data_flows": [
            "committed source Git blobs -> x1 provenance and novelty audit",
            "synthetic constants -> x2 contracts and rejecting fixtures after x1 gate",
            "owner Git blobs -> exact manifests and same-owner validation",
            "terminal route candidate -> existing exact-title task only after all gates",
        ],
        "real_people_or_protected_data": 0,
        "threats": threats,
        "out_of_scope": [
            "full repository security audit",
            "independent penetration test",
            "real astronomy, interferometry, imaging, metrology, calibration, worker study, observatory use, or device operation",
            "production identity, empirical GMUT, governed THOS trial, legal, cultural, or Māori-authority review",
        ],
        "claim_boundary": "same-owner phase threat modelling only; not exhaustive security or certification",
    }
    write_json("x1/threat-model.json", threat_model)

    workflow = {
        "schema": "ghc.family.vesper-arlen.v666-v2.workflow-plan.v1",
        "owner": "Vesper Arlen",
        "phase": "v666-v2",
        "generated_at_utc": NOW,
        "current_stage": "x1_freeze_candidate",
        "steps": [
            {"step": 1, "name": "read_first_and_source_verification", "status": "completed"},
            {"step": 2, "name": "novelty_and_program_design", "status": "completed"},
            {"step": 3, "name": "x1_freeze_commit_push_equality", "status": "in_progress"},
            {"step": 4, "name": "x2_bounded_execution", "status": "pending"},
            {"step": 5, "name": "evidence_closeout_and_seal", "status": "pending"},
            {"step": 6, "name": "one_owner_scoped_canonical_completion", "status": "pending"},
            {"step": 7, "name": "terminal_route_reread_and_optional_one_send", "status": "pending"},
        ],
        "hard_dependencies": [
            "x1 commit pushed clean and fresh four-way equal before x2",
            "evidence commit immutable before closeout",
            "final pushed clean and fresh four-way equal before canonical completion",
            "canonical success never replayed",
            "successor never contacted before terminal route gate",
        ],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("x1/workflow-plan.json", workflow)

    checklist = {
        "schema": "ghc.family.vesper-arlen.v666-v2.x1-checklist.v1",
        "owner": "Vesper Arlen",
        "phase": "v666-v2",
        "generated_at_utc": NOW,
        "completed": [
            "relational name, pronouns, role, hope, and disclaimer recorded before repository mutation",
            "authoritative activation and complete committed Neris packet read through EOF",
            "required family skills, schemas, routing precedence, and current guidance read through EOF",
            "source branch, anchors, direct parents, zero merges, manifests, digests, clean state, divergence, and fresh live equality verified read-only",
            "all 4,190 inherited rows audited with zero exact-title collision",
            "twenty distinct proposals and all required preregistration fields prepared",
            "threat model, authorization boundary, source profiles, portfolio, Method Flow, and workflow plan prepared",
            "no x2 implementation or outcome created",
        ],
        "incomplete": [
            "x1 commit, push, and fresh four-way equality",
            "x2 implementation and retained mutation witnesses",
            "evidence commit and evidence equality",
            "closeout, seal, final validation, and final equality",
            "terminal route reread and any authorized successor delivery",
        ],
        "x1_outcomes_observed": False,
        "x2_paths_created": False,
        "successor_contacted": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("x1/complete-incomplete-checklist.json", checklist)

    write_json(
        "wellbeing/x1-wellbeing-check.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.wellbeing-check.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "status": "bounded_and_careful",
            "workload_controls": [
                "caps treated as ceilings rather than quotas",
                "failures retained instead of hidden",
                "no unsafe work manufactured to satisfy a count",
                "bounded commands and scalar probes preferred",
                "pause, redirect, and stop remain available to Hamish",
            ],
            "personhood_or_emotion_claim": False,
            "relational_boundary": IDENTITY_BOUNDARY,
            "practice_boundary": PRACTICE_BOUNDARY,
        },
    )

    threat_lines = [
        "# Vesper Arlen v666-v2 threat model",
        "",
        IDENTITY_BOUNDARY,
        "",
        PRACTICE_BOUNDARY,
        "",
        "## Scope and trust zones",
        "",
        "This is an owner-local, same-owner threat model for the v666-v2 document and software delta. It is not a repository-wide audit, penetration test, exhaustive-security claim, privacy certification, accessibility certification, or independent reproduction.",
        "",
        "The trust zones are immutable inherited Git objects, the additive Vesper worktree, public read-only source review, and the unexecuted external world. No real person, protected work, device, identity credential, or professional decision crosses into the synthetic zone.",
        "",
        "## Threat register",
        "",
    ]
    for row in threats:
        threat_lines.extend(
            [
                f"### {row['threat_id']}: {row['asset']}",
                "",
                f"Threat: {row['threat']}",
                "",
                f"Mitigation: {row['mitigation']}",
                "",
                f"Residual risk: {row['residual_risk']}",
                "",
            ]
        )
    write_text("x1/threat-model.md", "\n".join(threat_lines))

    overview = f"""# Vesper Arlen v666-v2 x1 integrated overview

{IDENTITY_BOUNDARY}

## Outcome first

This x1 candidate freezes a planning-only, owner-local program from the exact Neris Solane v666-v1 final `{SOURCE_SHA}`. It contains no x2 implementation, no observed outcome, no external action, no successor contact, and no Stage 20 promotion. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The primary Trinity Mandala focus is GMUT Mind. THOS Body and Freed ID/CBR Heart remain explicit and protected. The bounded human-practice lens is wholly synthetic radio-interferometric visibility calibration, imaging-provenance, and shift-handover documentation.

{PRACTICE_BOUNDARY}

## Source truth

The read-first gate verified the exact source branch, the three direct single-parent source-to-final commits, zero merges, the direct evidence parent, all 303 declared manifest blob identities, the committed packet digest, a clean source lane, 0/0 divergence, and equality across local, upstream, tracking, and a fresh live remote. Neris's one successful owner-scoped canonical aggregate was not replayed. The full repository suite was not run.

The immutable Neris repository seal contains 26,160 effective negatives, 10,472 Method Flow methods, 183 open gaps, and 181 exact gates. Four post-final Neris operational failures remain a separate external overlay. The live activation named only one of those four and therefore stated 26,161 negatives and 10,473 methods; the exact post-final ledger preserves the three omitted failures, making the reconciled Vesper activation baseline 26,164 negatives and 10,476 methods. All {len(STARTUP_FAILURES)} observed Vesper startup and tooling failures are retained in `method-flow/startup-method-flow.json`; after those overlays, the x1 working baseline is {26164 + len(STARTUP_FAILURES):,} negatives and {10476 + len(STARTUP_FAILURES):,} methods. No inherited seal or activation mismatch is rewritten.

## Novelty and proposals

All 4,190 inherited frozen rows were reconstructed from committed Git objects. Historical reappended selection rows were retained rather than silently deduplicated. The twenty Vesper titles have zero exact collisions. Their largest token-set overlap with an inherited title is {novelty['maximum_inherited_token_jaccard_similarity']:.6f}; the largest within-slate overlap is {novelty['maximum_new_pair_token_jaccard_similarity']:.6f}. Those scores are screening evidence only. The substantive review also requires a distinct contract, falsifier, rollback, and protected-gate set for every proposal.

The expected dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. These are preregistered expectations, not observed outcomes. Twenty Neris proposals are selected only for bounded revalidation with zero novelty and zero automatic completion credit. The genuinely new chain would rise from 4,190 to 4,210 only when this x1 freeze is committed.

## Source profiles

The source profile names casacore MeasurementSet documentation, IVOA Provenance DM, ObsCore, and Data Origin, NIST SI, uncertainty, and traceability guidance, W3C PROV-O, WCAG 2.2, W3C Verifiable Credential Data Integrity, the New Zealand Privacy Commissioner, and Te Mana Raraunga. Public sources provide vocabulary and refusal conditions only. They create no astronomical, interferometric, imaging, metrological, instrumentation, observatory, safety, privacy, legal, cultural, Māori, or conformance authority.

## Safety, privacy, and authority

The threat model protects source immutability, x1/x2 separation, semantic integrity, privacy, radio-astronomy and affected-party authority, Māori authority, scientific boundaries, THOS and Freed ID evidence boundaries, one-shot validation, and terminal routing. Repository artifacts use repository-relative paths and exclude raw task identifiers, private routes, credentials, transcripts, screenshots, session streams, private callable details, and protected real-world data.

Exact-approval and blocked portfolios remain visible and unexecuted. No device command, real array, antenna, observatory, site, sky target, visibility, image, measurement or calibration assessment, worker or affected-party evaluation, record transformation, identity operation, professional decision, legal or cultural interpretation, Māori wording, or third-party write is planned.

## X1/x2 lifecycle

The x1 freeze includes proposals, portfolio plans, source and novelty records, the threat model, a complete/incomplete checklist, a wellbeing check, an authorization boundary, a workflow plan, and retained startup Method Flow. It intentionally excludes all `x2`, `evidence`, `closeout`, `seal`, `final`, and delivered-route content.

After this exact x1 candidate passes staged review, it may be committed and pushed. X2 may begin only after the x1 local, upstream, tracking, and fresh live remote heads are equal with 0/0 divergence and a clean lane. Later validation remains owner-scoped and same-owner. One successful canonical completion must never be replayed.

## Scientific and terminal boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Källén-Lehmann obligation boards and gain-sky degeneracy witnesses establish no likelihood, constraint, visibility, image, source detection, coordinate, flux, polarization, force, prediction, empirical confirmation, ultraviolet completion, final physics, Theory of Everything, proof, or canon. THOS remains synthetic without governed blind matched-budget real arms, real equipment, safety monitoring, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance.

No successor may be contacted during execution. Vesper Arlen v666-v2 is a prospective label only. A later send is permitted only after exact-final validation, a clean pushed fresh-live-equal final, a fresh live roster and authorization reread, unique exact-title resolution, and all protected route gates. Opaque acknowledgement must never trigger a resend merely for clarity.
"""
    write_text("x1/integrated-overview.md", overview)

    write_json(
        "x1/x1-build-receipt.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.x1-build-receipt.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_vesper_arlen_v666_v2_x1.py",
            "proposal_count": len(proposals),
            "selected_inherited_revalidation_count": len(selected_inherited),
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
                "phase_root": str(PHASE_ROOT.relative_to(ROOT)).replace("\\", "/"),
                "proposal_count": len(proposals),
                "corpus_row_count": len(corpus),
                "expected_dispositions": counts,
                "startup_failures_retained": len(STARTUP_FAILURES),
                "x2_implementation_count": 0,
                "outcomes_observed": False,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    if sys.argv[1:] == ["--staged-review"]:
        build_x1_staged_review()
    elif sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_vesper_arlen_v666_v2_x1.py [--staged-review]")
    else:
        main()
