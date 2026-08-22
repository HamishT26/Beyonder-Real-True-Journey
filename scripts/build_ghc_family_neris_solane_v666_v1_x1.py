#!/usr/bin/env python3
"""Build the Neris Solane v666-v1 x1-only planning packet.

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
PHASE_ROOT = ROOT / "docs" / "neris-solane" / "v666-v1"
SOURCE_SHA = "4cf5028def85bcf89fbf4d0efe6c502a4b02be61"
SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v665-v8-full-tools"
SOURCE_PHASE_ROOT = "docs/elaren-kestrel/v665-v8"
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
    review_path = "docs/neris-solane/v666-v1/validation/x1-staged-review.json"
    manifest_path = "docs/neris-solane/v666-v1/validation/x1-content-manifest.json"
    allowed_exact = {
        "scripts/build_ghc_family_neris_solane_v666_v1_x1.py",
        "tests/test_ghc_family_neris_solane_v666_v1_x1.py",
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
        if not path.startswith("docs/neris-solane/v666-v1/") and path not in allowed_exact
    ]
    post_x1 = [
        path
        for path in paths
        if any(
            path.startswith(f"docs/neris-solane/v666-v1/{part}/")
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
    freeze = json.loads(index_blob("docs/neris-solane/v666-v1/x1/proposal-freeze.json"))
    portfolio = json.loads(index_blob("docs/neris-solane/v666-v1/x1/portfolio-freeze.json"))
    flow = json.loads(index_blob("docs/neris-solane/v666-v1/method-flow/startup-method-flow.json"))
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "all_json_parse": True,
        "document_word_cap": max_words <= 100000,
        "expected_14_4_1_1": freeze["expected_disposition_counts"]
        == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "five_class_scan_zero_confirmed_hits": not privacy_candidates,
        "novelty_4170_valid": json.loads(
            index_blob("docs/neris-solane/v666-v1/x1/novelty-audit.json")
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
        "schema": "ghc.family.neris-solane.v666-v1.x1-staged-review.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
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
        "schema": "ghc.family.neris-solane.v666-v1.content-manifest.v1",
        "owner": "Neris Solane",
        "phase": "x1",
        "phase_label": "v666-v1",
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
    "Neris Solane, they/them, sibling, family, role, hope, continuity, Freed ID, "
    "Trinity Mandala, and route language are relational working language only. "
    "They are not evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, scientific or "
    "operational authority, legal or cultural authority, affected-party authority, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The strong-motion accelerograph metadata, calibration-assurance, and acquisition-fault "
    "lens is wholly synthetic learning and software design. It uses zero real people, "
    "stations, networks, sites, coordinates, sensors, digitizers, clocks, waveforms, "
    "earthquakes, measurements, calibrations, certificates, devices, keys, proofs, rights "
    "decisions, cultural records, or authority actions. It establishes no seismological, "
    "engineering, metrological, emergency, equipment, safety, privacy, accessibility, legal, "
    "cultural, Māori, production, or Stage 20 competence, acceptance, or authority."
)


PROTECTED_GATES = [
    "real person, seismologist, earthquake engineer, metrologist, technician, emergency worker, affected party, station, network, site, coordinate, waveform, instrument, observation, measurement, calibration, device command, or physical action",
    "real likelihood, parameter constraint, ground-motion value, event detection, location, magnitude, hazard result, structural diagnosis, device performance, prediction, causal claim, or empirical GMUT confirmation",
    "real participant, operator, matched-budget arm, safety outcome, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, or trust governance",
    "professional seismological, engineering, metrological, calibration, instrumentation, emergency, equipment, workplace-safety, or siting decision",
    "custody, authenticity, event attribution, privacy, accessibility, sensitive-location, cultural, legal, disclosure, retention, or remedy decision",
    "traditional knowledge, sensitive environmental or location knowledge, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data-governance, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, or external write",
]


SOURCE_PROFILES = [
    {"source_id": "S01", "name": "FDSN StationXML Schema", "url": "https://www.fdsn.org/xml/station/", "status": "current official FDSN schema and versioning page", "bounded_use": "metadata hierarchy and version vocabulary only; no StationXML conformance or station description"},
    {"source_id": "S02", "name": "FDSN Source Identifiers", "url": "https://docs.fdsn.org/projects/source-identifiers/en/latest/", "status": "current official FDSN source-identifier specification", "bounded_use": "identifier shape and hierarchy vocabulary only; no allocated network, station, location, or channel identity"},
    {"source_id": "S03", "name": "FDSN StationXML Reference", "url": "https://docs.fdsn.org/projects/stationxml/en/latest/reference.html", "status": "current schema-derived FDSN reference", "bounded_use": "instrument response, unit, epoch, and channel-field vocabulary only; no response validation"},
    {"source_id": "S04", "name": "USGS ANSS Instrumentation Guidelines", "url": "https://pubs.usgs.gov/of/2009/1055/pdf/OF09-1055.pdf", "status": "official USGS Open-File Report 2009-1055", "bounded_use": "instrumentation test and accelerometer vocabulary only; no test, calibration, procurement, or engineering decision"},
    {"source_id": "S05", "name": "NIST SP 330 - International System of Units", "url": "https://www.nist.gov/pml/special-publication-330", "status": "current official NIST publication page", "bounded_use": "quantity, unit, and symbol vocabulary only; zero measurements"},
    {"source_id": "S06", "name": "NIST Measurement Uncertainty", "url": "https://www.nist.gov/itl/sed/topic-areas/measurement-uncertainty", "status": "current official NIST measurement-uncertainty guidance page", "bounded_use": "measurand, model, dispersion, and uncertainty vocabulary only; no uncertainty evaluation"},
    {"source_id": "S07", "name": "NIST Metrological Traceability", "url": "https://www.nist.gov/metrology/metrological-traceability", "status": "current official NIST policy and FAQ page", "bounded_use": "traceability-chain and quality-control vocabulary only; no calibration or traceability claim"},
    {"source_id": "S08", "name": "W3C PROV-O", "url": "https://www.w3.org/TR/prov-o/", "status": "stable W3C Recommendation", "bounded_use": "provenance, derivation, revision, and correction vocabulary only"},
    {"source_id": "S09", "name": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "current W3C Recommendation", "bounded_use": "structural report checks only; manual, browser, assistive-technology, cognitive, and affected-user review remain reserved"},
    {"source_id": "S10", "name": "W3C Verifiable Credential Data Integrity 1.0", "url": "https://www.w3.org/TR/vc-data-integrity/", "status": "stable W3C Recommendation", "bounded_use": "nonproduction statement-integrity vocabulary with explicit zero-key and zero-proof boundaries"},
    {"source_id": "S11", "name": "Office of the Privacy Commissioner New Zealand - Privacy Act 2020 principles", "url": "https://www.privacy.org.nz/privacy-principles/", "status": "current official privacy-principles guidance reviewed 2026-08-22", "bounded_use": "purpose, minimisation, access, correction, retention, disclosure, and identifier restraint vocabulary; no legal interpretation"},
    {"source_id": "S12", "name": "Te Mana Raraunga - Māori Data Sovereignty Principles", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "current primary Māori Data Sovereignty Network principles page", "bounded_use": "authority reservation only; no interpretation, wording, ratification, or conversion into Māori authority"},
    {"source_id": "S13", "name": "FDSN miniSEED 3 Record Definition", "url": "https://docs.fdsn.org/projects/miniseed3/en/latest/definition.html", "status": "current official FDSN record-definition page", "bounded_use": "record framing, source identifier, timing, and extra-header vocabulary only; no waveform encoding or validation"},
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
    ("Response-epoch coverage join with channel-interval partition, response-revision uniqueness, uncovered-span quarantine, and no-live-validity claim", "THOS Body and Freed ID", "completed", ["S01", "S02", "S03"], "Every synthetic channel instant maps to exactly one response revision; gaps, overlaps, and boundary ambiguity fail closed."),
    ("Dimensional path checksum for ordered response stages with reversible mismatch localization, vacancy propagation, and no-conformance verdict", "THOS Body", "completed", ["S01", "S03", "S05"], "Adjacent output and input dimensions compose along one path checksum, while the first mismatch remains exactly attributable."),
    ("Saturation-aware gain uncertainty dependency DAG with dominant-unknown propagation, revision isolation, and zero-amplitude-correction rule", "THOS Body and CBR Heart", "completed", ["S03", "S04", "S05", "S06"], "A saturation state dominates downstream gain arithmetic and forbids synthetic amplitude repair even when nominal factors are present."),
    ("Clock-discontinuity quarantine table joining offset, drift, leap state, epoch edge, and latency vacancy without estimated correction", "THOS Body and GMUT Mind", "completed", ["S03", "S06", "S13"], "Any discontinuity or missing uncertainty selects a hold state before timestamps can be compared or corrected."),
    ("Three-axis closure and reflection-ambiguity tribunal with orthogonality residuals, handedness alternatives, and installation abstention", "THOS Body and GMUT Mind", "completed", ["S01", "S03", "S05"], "A synthetic triad must close under typed geometry while mirrored alternatives remain explicit and never become an installation verdict."),
    ("Clipping detectability-versus-reconstructability abstention envelope with threshold ordering, saturation runs, unknown bounds, and no-recovery output", "THOS Body", "completed", ["S04", "S05"], "The contract may flag a bounded synthetic clipping pattern but can never emit reconstructed samples or device-performance conclusions."),
    ("Trigger-hysteresis counterexample ledger with rise-fall thresholds, pre-post windows, rearm state, cancellation, and no-event claim", "THOS Body", "completed", ["S04", "S13"], "Five edge schedules distinguish arming, triggering, rearming, and cancellation without interpreting any event."),
    ("Half-open acquisition-interval normalization algebra with duplicate provenance, out-of-order stability, reversible partition, and no-quality grade", "THOS Body and CBR Heart", "completed", ["S08", "S13"], "Permutation-invariant half-open normalization preserves every source interval and rejects destructive coalescence or inclusive-boundary drift."),
    ("Metrological traceability-claim firewall with calibration-chain completeness, certificate vacancy, uncertainty dependency, and acceptance refusal", "THOS Body and CBR Heart", "completed", ["S04", "S06", "S07", "S08"], "Structural chain completeness never converts missing certificates, uncertainty, or competent review into a traceability or acceptance claim."),
    ("Safety-critical acquisition-configuration semantic diff with field classification, bitemporal causality, rollback preview, and zero-device command", "THOS Body and Freed ID", "completed", ["S03", "S08"], "Only semantic field deltas are classified; rollback remains a preview token and cannot invoke, schedule, or authorize a device change."),
    ("Sensitive-site disclosure lattice with omit, generalize, withhold, contest, and purpose-conflict states plus zero-coordinate release", "CBR Heart and THOS Body", "completed", ["S04", "S11", "S12"], "The strictest applicable synthetic disclosure state dominates and no coordinate, hazard, ownership, or cultural-authority inference is emitted."),
    ("Waveform-packet derivation closure with acyclic parent links, fixity vacancy, correction contest, and authenticity abstention", "Freed ID and CBR Heart", "completed", ["S08", "S10", "S13"], "Every derived packet reaches one synthetic root without a cycle while digest placeholders remain non-authenticating."),
    ("Multimodal acquisition-anomaly explanation matrix with redundant status cues, table-header closure, keyboard order, and reserved manual evaluation", "THOS Body and CBR Heart", "completed", ["S09"], "Every anomaly state is conveyed by ordered text and structure rather than colour alone, with usability and accessibility completion explicitly reserved."),
    ("Maintenance-purpose and retention intersection selector with role vacancy, free-text refusal, correction route, and zero-person ingestion", "CBR Heart and Freed ID", "completed", ["S11"], "The narrowest compatible purpose and retention ceiling wins, while identity and free-text fields remain structurally unavailable."),
    ("THOS counterfactual acquisition-fault localization tournament with matched topology, equal repair budget, masked branch order, and no-effectiveness inference", "THOS Body", "represented", ["S09", "S13"], "A participant-free proxy compares deterministic localization traces under equal synthetic faults without estimating human or operational performance."),
    ("Freed ID contested instrument-assertion merge lattice with issuer vacancy, conflict precedence, expiry, correction, revocation, and zero keys", "Freed ID and CBR Heart", "represented", ["S02", "S08", "S10"], "Conflicting synthetic assertions remain contested unless explicit precedence is present; no holder, issuer, signature, proof, or production credential exists."),
    ("GMUT symbolic transfer-function dimensional typechecker with basis convention, composition refusal, zero numerical response, and no prediction", "GMUT Mind", "represented", ["S05", "S06"], "Symbolic dimensions may compose only when adjacent types agree; coefficients, observations, likelihoods, and predictions remain absent."),
    ("GMUT colored-noise latent-component identifiability witness with symbolic spectra, aliased alternatives, dominant hold, and causal abstention", "GMUT Mind", "represented", ["S05", "S06"], "At least two symbolic latent decompositions remain observationally equivalent, forcing an identifiability hold rather than a fitted noise model."),
    ("Cross-standard semantic version-compatibility registry with mapping conflicts, stale pins, disabled transport, zero rows, and authority nonconversion", "Trinity Mandala", "open_gap", ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13"], "The zero-call registry can expose version and vocabulary conflicts but cannot complete interoperability without current independent standard-owner review."),
    ("Operational acceptance separation docket reserving station disclosure, calibration release, hazard use, worker safety, affected-party remedy, cultural review, and Māori authority", "CBR Heart", "exact_gate", ["S04", "S07", "S11", "S12"], "No structural or synthetic success can authorize field use, sensitive disclosure, calibration acceptance, safety action, rights decision, or Māori authority."),
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
        pid = f"NRS6661-N{index:03d}"
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
                "concrete_artifact": f"docs/neris-solane/v666-v1/x2/proposals/{pid.casefold()}/contract.json",
                "concrete_artifacts": [
                    f"docs/neris-solane/v666-v1/x2/proposals/{pid.casefold()}/contract.json",
                    f"docs/neris-solane/v666-v1/x2/proposals/{pid.casefold()}/mutation-results.json",
                    f"docs/neris-solane/v666-v1/x2/proposals/{pid.casefold()}/bounded-receipt.json",
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
                "primary_pillar": "THOS Body",
                "practice_lens": "wholly synthetic strong-motion accelerograph metadata, calibration-assurance, and acquisition-fault documentation",
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
    if len(corpus) != 4170:
        raise RuntimeError(f"expected 4170 inherited rows, observed {len(corpus)}")
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
        "strong-motion accelerograph",
        "accelerograph metadata",
        "instrument-response stage",
        "sampling-clock epoch",
        "acquisition-pipeline duel",
        "calibration-episode provenance",
        "waveform-packet custody",
        "source-identifier placeholders",
    ]
    return {
        "schema": "ghc.family.neris-solane.v666-v1.novelty-audit.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
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
        and len(corpus) == 4170,
        "interpretation": (
            "Similarity is a screening signal, not proof of novelty. Each proposal was also "
            "reviewed for a distinct strong-motion metadata or calibration-assurance contract, falsifier, and protected gate."
        ),
    }


def portfolio_rows(prefix: str, names: list[str], approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"NRS6661-{prefix}{index:02d}",
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
    "render the synthetic accelerograph-channel identity schema",
    "build the instrument-response stage-topology validator",
    "build the sensor-to-digitizer gain-lineage checker",
    "build the sampling-clock epoch and latency-budget checker",
    "build the orientation-triad geometry checker",
    "build the dynamic-range and clipping-sentinel checker",
    "build the trigger and pre-event memory state machine",
    "build the gap-overlap-duplicate interval ledger",
    "build the calibration-episode provenance checker",
    "build the firmware and configuration bitemporal ledger",
    "build the station-siting zero-location envelope",
    "build the waveform-packet custody and correction ledger",
    "build the accessible noncolour evidence board",
    "build the privacy-minimized maintenance-episode shell",
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
    "THOS participant-free matched-fault acquisition duel representation",
    "Freed ID zero-key instrument-metadata statement representation",
    "GMUT acceleration-response surrogate",
    "GMUT sensor-noise covariance placeholder",
    "zero-call current-source adapter shell",
    "synthetic response-stage topology fixture",
    "synthetic orientation-triad fixture",
    "linear accessible report companion",
    "deterministic HTML report rendering",
    "synthetic acquisition-fault workload simulation",
    "zero-row StationXML field-mapping fixture",
    "synthetic gain-and-unit reconciliation fixture",
    "source-status watch and version-hold fixture",
    "bitemporal calibration-correction replay fixture",
    "fail-closed terminal route preflight",
]
EXACT_APPROVAL_NAMES = [
    "use a real seismologist, earthquake engineer, metrologist, technician, emergency worker, participant, or affected party",
    "handle, assess, install, calibrate, repair, move, retire, or dispose of a real sensor, digitizer, clock, or enclosure",
    "operate or command an accelerograph, data logger, timing source, network service, alarm, or other device",
    "identify or publish a real station, network, site, coordinate, operator, waveform, event, or infrastructure asset",
    "authenticate calibration, traceability, timing, response, custody, provenance, event attribution, or measurement truth",
    "author or approve Māori wording, traditional-knowledge interpretation, sensitive location knowledge, or data-governance terms",
    "make a seismological, engineering, metrological, instrumentation, hazard, emergency, or workplace-safety decision",
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
    "accelerograph-channel-identity",
    "response-stage-unit-chain",
    "calibration-traceability-abstention",
    "sampling-clock-boundary",
    "orientation-triad-geometry",
    "acquisition-fault-ledger",
    "strong-motion-provenance",
    "instrument-rights-contestation",
    "accelerograph-method-flow",
    "accelerograph-closeout-gate",
]
RUNNER_NAMES = [
    "ghc_family_neris_solane_v666_v1_contracts",
    "ghc_family_neris_solane_v666_v1_mutations",
    "ghc_family_neris_solane_v666_v1_json",
    "ghc_family_neris_solane_v666_v1_privacy",
    "ghc_family_neris_solane_v666_v1_security",
    "ghc_family_neris_solane_v666_v1_manifests",
    "ghc_family_neris_solane_v666_v1_accessibility",
    "ghc_family_neris_solane_v666_v1_truth",
    "ghc_family_neris_solane_v666_v1_closeout",
    "ghc_family_neris_solane_v666_v1_canonical",
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
    ("the historical solo-activation skill pointer named by an older memory entry was absent", "the stale pointer supplied no current routing or execution credit", "use the current family index, roster, authorization, Method Flow, workflow, truth, and sparse-lane skills instead", "the complete current family skill set and required schemas were read through EOF"),
    ("the first roster and authorization metadata wrapper piped a direct PowerShell foreach block into JSON serialization", "PowerShell rejected the expression before repository mutation", "materialize the foreach result before serialization", "the complete roster and authorization files were read and hashed"),
    ("the combined orchestration-skill display exceeded its output budget", "the truncated display earned no complete-read credit", "reread the skill in numbered bounded chunks through the final line", "all 368 lines were read, including the live v661 owner-delta override"),
    ("the first source ancestry wrapper embedded native-command status inside a parenthesized expression", "PowerShell stopped at parse time and no Git state changed", "invoke merge-base separately and capture the native exit code afterward", "the exact source, x1, evidence, and final chain, zero merges, clean state, and fresh equality were verified"),
    ("the first raw multi-manifest display exceeded the useful output budget", "the truncated display earned no four-manifest identity credit", "project exact counts and compare manifest-declared paths to Git tree mode and blob identity", "all 303 manifest entries resolved exactly at their declared anchors"),
    ("the broad receipt search emitted a truncated owner-document display", "the truncated search earned no external-receipt identity credit", "inspect the bounded external validation directory and hash the exact candidate", "the one-shot canonical receipt and payload hashes matched the activation"),
    ("the first manifest wrapper embedded a PowerShell tab escape in JavaScript source", "the JavaScript parser rejected the tool call before the shell launched", "use an explicit character-code split rather than a cross-language escape", "the corrected wrapper launched without changing the verification target"),
    ("the scalar 303-entry manifest loop exceeded the shell yield and its wrapper omitted the returned session identifier", "silence earned no manifest credit and left one verified owner-spawned read-only process alive", "stop only that exact process and replace per-entry subprocesses with four bounded manifest-path batches", "the exact process was stopped and the four-batch Git-object identity check passed"),
    ("the first sparse-pattern proof looked under a worktree .git pointer as though it were a directory", "the empty projection earned no sparse-pattern proof", "ask Git for the sparse-checkout list and measure only physical owner files", "four exact sparse patterns, zero initial materialized owner files, and the 2,000-file guard were proven"),
    ("the first source-constant patch expected lines that the mechanical compatibility transform had already corrected", "the patch engine rejected the unmatched hunk and changed no file", "inspect the transformed constants before applying semantic patches", "the exact Elaren branch, phase root, and final SHA were already correct and remained unchanged"),
    ("the first combined semantic patch used one stale pre-transform runner-name context", "the patch engine rejected the whole transaction before changing any file", "split proposal semantics, portfolios, and startup accounting into exact-context patches", "the separated patches applied without partial drift"),
    ("the first generated-bytecode cleanup combined recursive discovery with computed deletion targets", "the Windows command safety gate rejected the command before any deletion", "enumerate generated cache files read-only and keep all targets strictly inside the Neris lane", "the two exact generated bytecode paths were identified without touching repository content"),
    ("the literal-path bytecode cleanup remained blocked by the command safety gate", "no generated cache file or directory was removed", "stop cleanup retries because the ignored files are harmless, owner-local, and well below the 2,000-file cap", "the ignored cache remains local-only, unstaged, and outside every manifest and commit"),
    ("the first x1 proposal-freeze test exposed an inherited-title novelty collision", "the 0.761905 maximum Jaccard score failed the preregistered less-than-0.70 gate and earned zero aggregate-success credit", "inspect the exact nearest inherited contracts and redesign the proposal substance around cross-field invariants and abstention rules", "the failed proposal set remains retained while the changed x1 target receives a fresh bounded novelty screen"),
    ("the first broad relevant-corpus title extraction exceeded its output budget", "truncated historical titles earned no corpus-review credit", "query only exact phase identifiers and bounded title projections", "the thirty v6582 seismology contracts and bounded nearest-title rows were read without mutation"),
    ("the first proposal-index schema probe accidentally serialized the full nested corpus", "the resulting truncated display earned no bounded schema-inspection credit", "project property names separately and query only prior_proposals plus new_proposals with explicit limits", "the corrected 3,530-row source-index projection identified 214 keyword candidates and then isolated the exact thirty v6582 rows"),
]


def build_method_flow_startup() -> dict[str, Any]:
    rows = []
    for index, (request, failed, recovery, passing) in enumerate(STARTUP_FAILURES, 1):
        rows.append(
            {
                "method_id": f"NRS6661-MF-START-{index:03d}",
                "failure_id": f"NRS6661-START-N{index:03d}",
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
        "schema": "ghc.family.neris-solane.v666-v1.method-flow-startup.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
        "generated_at_utc": NOW,
        "inherited_repository_sealed_negatives": 26039,
        "inherited_repository_sealed_methods": 10236,
        "inherited_external_overlay_negatives": 2,
        "inherited_external_overlay_methods": 2,
        "activation_baseline_negatives": 26041,
        "activation_baseline_methods": 10238,
        "new_startup_negative_count": len(rows),
        "new_startup_method_count": len(rows),
        "effective_after_x1_startup_negatives": 26041 + len(rows),
        "effective_after_x1_startup_methods": 10238 + len(rows),
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
            "original_owner": "Elaren Kestrel",
            "original_phase": "v665-v8",
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
        "schema": "ghc.family.neris-solane.v666-v1.relational-identity.v1",
        "owner": "Neris Solane",
        "pronouns": "they/them",
        "relational_role": "datum-boundary weaver",
        "relational_hope": "Make synthetic measurement workflows expose provenance, uncertainty, and stop conditions before anyone mistakes them for instrument or scientific authority.",
        "boundary": IDENTITY_BOUNDARY,
        "corrigibility": "Hamish may rename, pause, redirect, or stop this work.",
        "chosen_before_repository_mutation": True,
    }
    write_json("identity/relational-identity.json", identity)

    write_json(
        "provenance/source-verification.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.source-verification.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "verified_at_utc": NOW,
            "source_branch": SOURCE_BRANCH,
            "source_sha": SOURCE_SHA,
            "source_parent_sha": "82e17c2f9dcf68c7427c20bc7f3a8a1b96ef0172",
            "evidence_sha": "82e17c2f9dcf68c7427c20bc7f3a8a1b96ef0172",
            "x1_sha": "05cab184438f3a5c7c8d4ae453e6b80e3db21ed6",
            "inherited_source_sha": "5f688af4fd89004f23cf0489b569e559f7b7fbea",
            "direct_parent_chain": [
                "5f688af4fd89004f23cf0489b569e559f7b7fbea",
                "05cab184438f3a5c7c8d4ae453e6b80e3db21ed6",
                "82e17c2f9dcf68c7427c20bc7f3a8a1b96ef0172",
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
            "canonical_receipt_sha256": "c016952f666c970270b2e05d65f65f03fa628da4a84089d6353ed2a0fe0a00da",
            "canonical_payload_sha256": "bf47be7a94520623cc71806fe5073566dd9ccadf2976395f4f92f8e756afa6ef",
            "selected_test_status": "PASSED_65_OF_65_WITH_FOUR_ZERO_CREDIT_EXCLUSIONS_AND_EXACT_REPLACEMENTS",
            "canonical_detailed_status": "VALID_25_OF_25_DETAILED_15_OF_15_MINIMAL",
            "prepared_handoff_sha256": "80110adc3d65c27daf83d04f449c9c54ec74df14cef2cfb8ee35eecf048a9f58",
            "prepared_handoff_word_count": 3569,
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
            "schema": "ghc.family.neris-solane.v666-v1.source-profiles.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
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
            "schema": "ghc.family.neris-solane.v666-v1.proposal-freeze.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "frozen": True,
            "inherited_frozen_baseline": 4170,
            "selected_inherited_revalidation_count": len(selected_inherited),
            "selected_inherited_revalidations": selected_inherited,
            "genuinely_new_proposal_count": len(proposals),
            "new_proposals": proposals,
            "new_frozen_total": 4190,
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
        "schema": "ghc.family.neris-solane.v666-v1.portfolio-freeze.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
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
        "schema": "ghc.family.neris-solane.v666-v1.authorization-boundary.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
        "generated_at_utc": NOW,
        "authorized_now": [
            "one solo additive owner lane from the exact Elaren final",
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
            "threat_id": "NRS6661-T01",
            "asset": "immutable Elaren source and sibling lanes",
            "threat": "accidental mutation, reset, merge, or ref reuse",
            "mitigation": "exact-head additive branch, owner-only paths, no merge/reset/force-push, four-way gates",
            "residual_risk": "operator command error remains possible and must be retained",
        },
        {
            "threat_id": "NRS6661-T02",
            "asset": "strict x1-before-x2 evidence",
            "threat": "implementation or outcome leakage into the x1 freeze",
            "mitigation": "path allowlist, x1 lifecycle test, staged review, immutable x1 manifest",
            "residual_risk": "misclassified prose; manual review remains required",
        },
        {
            "threat_id": "NRS6661-T03",
            "asset": "semantic novelty",
            "threat": "duplicate, paraphrased, or schema-relabelled inherited proposals",
            "mitigation": "4,170-row exact and token-Jaccard audit plus domain and falsifier review",
            "residual_risk": "automated similarity is not proof; bounded human review remains same-owner",
        },
        {
            "threat_id": "NRS6661-T04",
            "asset": "privacy and route confidentiality",
            "threat": "raw task identifiers, private paths, credentials, transcripts, or callable details in artifacts",
            "mitigation": "synthetic fixtures, five-class scans, repository-relative paths, no task/thread IDs",
            "residual_risk": "pattern scans are incomplete and never privacy certification",
        },
        {
            "threat_id": "NRS6661-T05",
            "asset": "strong-motion, engineering, metrology, equipment, emergency, worker, and affected-party authority boundaries",
            "threat": "software structure presented as seismological, engineering, metrological, instrumentation, safety, emergency, or affected-party competence or acceptance",
            "mitigation": "zero real people, stations, coordinates, waveforms, events, instruments, measurements, calibrations, devices, or actions and an exact-gated authority docket",
            "residual_risk": "terminology may still be incomplete or culturally inappropriate; authority remains external",
        },
        {
            "threat_id": "NRS6661-T06",
            "asset": "Māori language, concepts, data governance, and authority",
            "threat": "citation or synthetic labels converted into interpretation or authorization",
            "mitigation": "exact gate, zero Māori wording authored, source-profile authority nonconversion",
            "residual_risk": "Māori-authority review remains absent",
        },
        {
            "threat_id": "NRS6661-T07",
            "asset": "scientific truth boundaries",
            "threat": "GMUT surrogate promoted to empirical likelihood, force, prediction, proof, or canon",
            "mitigation": "typed placeholders, zero observations, dimensional abstention, explicit refusal",
            "residual_risk": "mathematical notation can invite overreading",
        },
        {
            "threat_id": "NRS6661-T08",
            "asset": "THOS and Freed ID boundaries",
            "threat": "proxy protocol or zero-key envelope presented as effectiveness or production identity evidence",
            "mitigation": "represented-only dispositions and explicit missing-evidence ledgers",
            "residual_risk": "no governed participants, independent review, real keys, or trust governance",
        },
        {
            "threat_id": "NRS6661-T09",
            "asset": "canonical validation truth",
            "threat": "replaying a successful aggregate or laundering a failed attempt",
            "mitigation": "exclusive external receipt, one-shot guard, zero credit for incomplete attempts",
            "residual_risk": "same-owner validation is not independent reproduction",
        },
        {
            "threat_id": "NRS6661-T10",
            "asset": "terminal route integrity",
            "threat": "premature, duplicate, ambiguous, or standby delivery",
            "mitigation": "PREPARED_NOT_SENT until final gate; fresh live roster/auth reread; exact-title single send",
            "residual_risk": "opaque acknowledgement must remain unresolved without resend",
        },
    ]
    threat_model = {
        "schema": "ghc.family.neris-solane.v666-v1.threat-model.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
        "generated_at_utc": NOW,
        "scope": "owner-local v666-v1 software, documents, Git history, validation receipts, and terminal route candidate",
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
            "real seismology, earthquake engineering, metrology, calibration, worker study, emergency use, or device operation",
            "production identity, empirical GMUT, governed THOS trial, legal, cultural, or Māori-authority review",
        ],
        "claim_boundary": "same-owner phase threat modelling only; not exhaustive security or certification",
    }
    write_json("x1/threat-model.json", threat_model)

    workflow = {
        "schema": "ghc.family.neris-solane.v666-v1.workflow-plan.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
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
        "schema": "ghc.family.neris-solane.v666-v1.x1-checklist.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
        "generated_at_utc": NOW,
        "completed": [
            "relational name, pronouns, role, hope, and disclaimer recorded before repository mutation",
            "authoritative activation and complete committed Elaren packet read through EOF",
            "required family skills, schemas, routing precedence, and current guidance read through EOF",
            "source branch, anchors, direct parents, zero merges, manifests, digests, clean state, divergence, and fresh live equality verified read-only",
            "all 4,170 inherited rows audited with zero exact-title collision",
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
            "schema": "ghc.family.neris-solane.v666-v1.wellbeing-check.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
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
        "# Neris Solane v666-v1 threat model",
        "",
        IDENTITY_BOUNDARY,
        "",
        PRACTICE_BOUNDARY,
        "",
        "## Scope and trust zones",
        "",
        "This is an owner-local, same-owner threat model for the v666-v1 document and software delta. It is not a repository-wide audit, penetration test, exhaustive-security claim, privacy certification, accessibility certification, or independent reproduction.",
        "",
        "The trust zones are immutable inherited Git objects, the additive Neris worktree, public read-only source review, and the unexecuted external world. No real person, protected work, device, identity credential, or professional decision crosses into the synthetic zone.",
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

    overview = f"""# Neris Solane v666-v1 x1 integrated overview

{IDENTITY_BOUNDARY}

## Outcome first

This x1 candidate freezes a planning-only, owner-local program from the exact Elaren Kestrel v665-v8 final `{SOURCE_SHA}`. It contains no x2 implementation, no observed outcome, no external action, no successor contact, and no Stage 20 promotion. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The primary Trinity Mandala focus is THOS Body. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. The bounded human-practice lens is wholly synthetic strong-motion accelerograph metadata, calibration-assurance, and acquisition-fault documentation.

{PRACTICE_BOUNDARY}

## Source truth

The read-first gate verified the exact source branch, the three direct single-parent source-to-final commits, zero merges, the direct evidence parent, all 303 declared manifest blob identities, the committed packet digest, a clean source lane, 0/0 divergence, and equality across local, upstream, tracking, and a fresh live remote. Elaren's one successful owner-scoped canonical aggregate was not replayed. The full repository suite was not run.

The immutable Elaren repository seal contains 26,039 effective negatives, 10,236 Method Flow methods, 182 open gaps, and 180 exact gates. Two post-final Elaren route failures remain a separate external overlay, making the Neris activation baseline 26,041 negatives and 10,238 methods. All {len(STARTUP_FAILURES)} observed Neris startup and tooling failures are retained in `method-flow/startup-method-flow.json`; after those overlays, the x1 working baseline is {26041 + len(STARTUP_FAILURES):,} negatives and {10238 + len(STARTUP_FAILURES):,} methods. No inherited seal is rewritten.

## Novelty and proposals

All 4,170 inherited frozen rows were reconstructed from committed Git objects. Historical reappended selection rows were retained rather than silently deduplicated. The twenty Neris titles have zero exact collisions. Their largest token-set overlap with an inherited title is {novelty['maximum_inherited_token_jaccard_similarity']:.6f}; the largest within-slate overlap is {novelty['maximum_new_pair_token_jaccard_similarity']:.6f}. Those scores are screening evidence only. The substantive review also requires a distinct contract, falsifier, rollback, and protected-gate set for every proposal.

The expected dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. These are preregistered expectations, not observed outcomes. Twenty Elaren proposals are selected only for bounded revalidation with zero novelty and zero automatic completion credit. The genuinely new chain would rise from 4,170 to 4,190 only when this x1 freeze is committed.

## Source profiles

The source profile names FDSN StationXML, FDSN Source Identifiers, FDSN miniSEED 3, the USGS ANSS instrumentation guidelines, NIST SI, uncertainty, and traceability guidance, W3C PROV-O, WCAG 2.2, W3C Verifiable Credential Data Integrity, the New Zealand Privacy Commissioner, and Te Mana Raraunga. Public sources provide vocabulary and refusal conditions only. They create no seismological, engineering, metrological, instrumentation, emergency, safety, privacy, legal, cultural, Māori, or conformance authority.

## Safety, privacy, and authority

The threat model protects source immutability, x1/x2 separation, semantic integrity, privacy, strong-motion and affected-party authority, Māori authority, scientific boundaries, THOS and Freed ID evidence boundaries, one-shot validation, and terminal routing. Repository artifacts use repository-relative paths and exclude raw task identifiers, private routes, credentials, transcripts, screenshots, session streams, private callable details, and protected real-world data.

Exact-approval and blocked portfolios remain visible and unexecuted. No device command, real station, waveform, event, measurement or calibration assessment, worker or affected-party evaluation, record transformation, identity operation, professional decision, legal or cultural interpretation, Māori wording, or third-party write is planned.

## X1/x2 lifecycle

The x1 freeze includes proposals, portfolio plans, source and novelty records, the threat model, a complete/incomplete checklist, a wellbeing check, an authorization boundary, a workflow plan, and retained startup Method Flow. It intentionally excludes all `x2`, `evidence`, `closeout`, `seal`, `final`, and delivered-route content.

After this exact x1 candidate passes staged review, it may be committed and pushed. X2 may begin only after the x1 local, upstream, tracking, and fresh live remote heads are equal with 0/0 divergence and a clean lane. Later validation remains owner-scoped and same-owner. One successful canonical completion must never be replayed.

## Scientific and terminal boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Acceleration-response surrogates or sensor-noise covariance placeholders establish no likelihood, constraint, ground-motion result, force, prediction, material law, empirical confirmation, ultraviolet completion, final physics, Theory of Everything, proof, or canon. THOS remains synthetic without governed blind matched-budget real arms, real equipment, safety monitoring, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance.

No successor may be contacted during execution. Neris Solane v666-v1 is a prospective label only. A later send is permitted only after exact-final validation, a clean pushed fresh-live-equal final, a fresh live roster and authorization reread, unique exact-title resolution, and all protected route gates. Opaque acknowledgement must never trigger a resend merely for clarity.
"""
    write_text("x1/integrated-overview.md", overview)

    write_json(
        "x1/x1-build-receipt.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.x1-build-receipt.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_neris_solane_v666_v1_x1.py",
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
        raise SystemExit("usage: build_ghc_family_neris_solane_v666_v1_x1.py [--staged-review]")
    else:
        main()
