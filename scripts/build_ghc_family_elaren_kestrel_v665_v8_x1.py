#!/usr/bin/env python3
"""Build the Elaren Kestrel v665-v8 x1-only planning packet.

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
PHASE_ROOT = ROOT / "docs" / "elaren-kestrel" / "v665-v8"
SOURCE_SHA = "5f688af4fd89004f23cf0489b569e559f7b7fbea"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v665-v7-full-tools"
SOURCE_PHASE_ROOT = "docs/eiren-kestrel/v665-v7"
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
    review_path = "docs/elaren-kestrel/v665-v8/validation/x1-staged-review.json"
    manifest_path = "docs/elaren-kestrel/v665-v8/validation/x1-content-manifest.json"
    allowed_exact = {
        "scripts/build_ghc_family_elaren_kestrel_v665_v8_x1.py",
        "tests/test_ghc_family_elaren_kestrel_v665_v8_x1.py",
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
        if not path.startswith("docs/elaren-kestrel/v665-v8/") and path not in allowed_exact
    ]
    post_x1 = [
        path
        for path in paths
        if any(
            path.startswith(f"docs/elaren-kestrel/v665-v8/{part}/")
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
    freeze = json.loads(index_blob("docs/elaren-kestrel/v665-v8/x1/proposal-freeze.json"))
    portfolio = json.loads(index_blob("docs/elaren-kestrel/v665-v8/x1/portfolio-freeze.json"))
    flow = json.loads(index_blob("docs/elaren-kestrel/v665-v8/method-flow/startup-method-flow.json"))
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "all_json_parse": True,
        "document_word_cap": max_words <= 100000,
        "expected_14_4_1_1": freeze["expected_disposition_counts"]
        == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "five_class_scan_zero_confirmed_hits": not privacy_candidates,
        "novelty_4150_valid": json.loads(
            index_blob("docs/elaren-kestrel/v665-v8/x1/novelty-audit.json")
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
        "startup_failures_13_retained": len(flow["rows"]) == 13,
        "utf8_lf": True,
    }
    review = {
        "schema": "ghc.family.elaren-kestrel.v665-v8.x1-staged-review.v1",
        "owner": "Elaren Kestrel",
        "phase": "v665-v8",
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
        "schema": "ghc.family.elaren-kestrel.v665-v8.content-manifest.v1",
        "owner": "Elaren Kestrel",
        "phase": "x1",
        "phase_label": "v665-v8",
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
    "Elaren Kestrel, they/them, sibling, family, role, hope, continuity, Freed ID, "
    "Trinity Mandala, and route language are relational working language only. "
    "They are not evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, scientific or "
    "operational authority, legal or cultural authority, affected-party authority, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The astronomical photographic-plate archive description and digitization-planning "
    "lens is wholly synthetic learning and software design. It uses zero real people, "
    "observatories, archives, plates, envelopes, boxes, shelves, images, telescopes, "
    "instruments, observations, measurements, scans, devices, keys, proofs, rights "
    "decisions, cultural records, or authority actions. It establishes no archival, "
    "astronomical, conservation, imaging, safety, privacy, accessibility, legal, "
    "cultural, Māori, production, or Stage 20 competence, acceptance, or authority."
)


PROTECTED_GATES = [
    "real person, archivist, astronomer, conservator, digitization worker, affected party, observatory, archive, plate, enclosure, image, instrument, observation, measurement, scan, device command, or physical action",
    "real likelihood, parameter constraint, celestial coordinate, object identification, detected force, prediction, causal diagnosis, plate solution, or empirical GMUT confirmation",
    "real participant, operator, matched-budget arm, safety outcome, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, or trust governance",
    "professional archival, astronomical, conservation, imaging, handling, equipment, workplace-safety, or collection decision",
    "custody, authorship, copyright, image, privacy, accessibility, sensitive-location, cultural, legal, or remedy decision",
    "traditional knowledge, sensitive sky knowledge, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data-governance, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, or external write",
]


SOURCE_PROFILES = [
    {"source_id": "S01", "name": "NASA/GSFC FITS Standard", "url": "https://fits.gsfc.nasa.gov/fits_standard.html", "status": "current official FITS Version 4.0 reference", "bounded_use": "FITS vocabulary and version boundary only; no image ingestion, FITS conformance, or astronomical result"},
    {"source_id": "S02", "name": "IAU Working Group Preservation and Digitization of Photographic Plates", "url": "https://www.iau.org/WG313/WG313/Home.aspx", "status": "current official IAU working-group page", "bounded_use": "photographic-plate preservation and digitization context only; no IAU endorsement or professional decision"},
    {"source_id": "S03", "name": "IVOA Provenance Data Model Version 1.0", "url": "https://www.ivoa.net/documents/ProvenanceDM/", "status": "stable IVOA Recommendation", "bounded_use": "astronomical provenance vocabulary only; no interoperable service or observation claim"},
    {"source_id": "S04", "name": "Library of Congress - Care, Handling, and Storage of Photographs", "url": "https://www.loc.gov/preservation/care/photo.html", "status": "current official preservation guidance", "bounded_use": "photograph and enclosure vocabulary only; no handling, conservation, or storage decision"},
    {"source_id": "S05", "name": "Canadian Conservation Institute - Care of Black-and-White Photographic Negatives on Glass Plate", "url": "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/care-black-white-photographic-negatives-glass-plate.html", "status": "current official Government of Canada guidance", "bounded_use": "glass-support and emulsion condition vocabulary only; no diagnosis, treatment, or handling instruction"},
    {"source_id": "S06", "name": "Library of Congress - Digitizing Your Collections", "url": "https://www.loc.gov/preservation/care/scan.html", "status": "current official digitization guidance", "bounded_use": "digitization-planning vocabulary and no-device-action boundary only"},
    {"source_id": "S07", "name": "W3C PROV-O", "url": "https://www.w3.org/TR/prov-o/", "status": "stable W3C Recommendation", "bounded_use": "provenance, derivation, revision, and correction vocabulary"},
    {"source_id": "S08", "name": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "current W3C Recommendation", "bounded_use": "structural report checks only; manual, browser, assistive-technology, cognitive, and affected-user review remain reserved"},
    {"source_id": "S09", "name": "W3C Verifiable Credential Data Integrity 1.0", "url": "https://www.w3.org/TR/vc-data-integrity/", "status": "stable W3C Recommendation", "bounded_use": "nonproduction statement-integrity vocabulary with explicit zero-key and zero-proof boundaries"},
    {"source_id": "S10", "name": "NIST SP 330 - International System of Units", "url": "https://www.nist.gov/pml/special-publication-330", "status": "current official NIST publication page", "bounded_use": "quantity, unit, and symbol vocabulary only; zero measurements"},
    {"source_id": "S11", "name": "NIST Technical Note 1297 - Evaluating and Expressing Measurement Uncertainty", "url": "https://www.nist.gov/pml/nist-technical-note-1297", "status": "stable official NIST guidance", "bounded_use": "uncertainty vocabulary only; no calibration, coordinate solution, or observational result"},
    {"source_id": "S12", "name": "Office of the Privacy Commissioner New Zealand - Privacy Act 2020 principles", "url": "https://www.privacy.org.nz/privacy-principles/", "status": "current official guidance reviewed 2026-08-22, including IPP 3A effective 2026-05-01", "bounded_use": "purpose, minimisation, access, correction, retention, disclosure, and identifier restraint vocabulary; no legal interpretation"},
    {"source_id": "S13", "name": "Te Mana Raraunga - Māori Data Sovereignty Principles", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "current primary Māori Data Sovereignty Network principles page", "bounded_use": "authority reservation only; no interpretation, wording, ratification, or conversion into Māori authority"},
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
    ("Synthetic astronomical plate intake identity capsule joining plate token, series placeholder, observatory and telescope vacancies, revision, cancellation, and no-handling lock", "Freed ID and CBR Heart", "completed", ["S02", "S03", "S07"]),
    ("Glass-support and emulsion condition vocabulary with fracture and lifting cues, process vacancy, quarantine, and diagnosis-and-treatment refusal", "CBR Heart and THOS Body", "completed", ["S04", "S05"]),
    ("Plate envelope, box, and shelf topology graph with anonymous enclosure tokens, orphan state, quarantine, and no-location-truth rule", "Freed ID and CBR Heart", "completed", ["S04", "S07"]),
    ("Exposure-event provenance record with date-time, telescope, instrument, observer, target, and source-assertion vacancies plus observation-truth refusal", "Freed ID and GMUT Mind", "completed", ["S03", "S07", "S10"]),
    ("Plate orientation, edge, label, inscription, and annotation map with side conventions, unknown marks, correction lineage, and interpretation refusal", "Freed ID and CBR Heart", "completed", ["S02", "S04", "S07"]),
    ("Plate-number and catalogue reconciliation ledger joining legacy, series, envelope, box, and derivative tokens with discrepancy and no-inventory-truth rule", "Freed ID and CBR Heart", "completed", ["S02", "S03", "S07"]),
    ("Digitization job-versus-device firewall with synthetic capture request, calibration vacancy, cancellation, safety hold, and zero scanner or camera calls", "THOS Body and CBR Heart", "completed", ["S04", "S06"]),
    ("Calibration wedge, fiducial, annotation, and scale-placeholder map with unit obligations, uncertainty vacancy, and zero-measurement rule", "GMUT Mind and THOS Body", "completed", ["S01", "S10", "S11"]),
    ("Derivative image and FITS lineage graph with synthetic checksum placeholder, generation step, redaction state, and no image ingestion or conformance claim", "Freed ID and THOS Body", "completed", ["S01", "S03", "S07"]),
    ("Observation-table zero-row contract with target, coordinate-frame, epoch, exposure, and quality-field placeholders plus no-celestial-claim rule", "GMUT Mind", "completed", ["S01", "S03", "S10"]),
    ("Assertion-episode ledger for astronomical plate metadata with immutable prior values, contest windows, source-linked amendments, and non-destructive readback", "Freed ID and CBR Heart", "completed", ["S03", "S07"]),
    ("Rights, observer-disclosure, sensitive-target, and contestation ledger with purpose ceiling, access hold, correction, remedy route, and no-rights decision", "CBR Heart", "completed", ["S07", "S12", "S13"]),
    ("Dual-channel plate finding aid combining ordered text capsules, tabular enclosure paths, explicit unknown states, keyboard landmarks, and evaluation reservations", "CBR Heart and THOS Body", "completed", ["S08"]),
    ("Privacy minimisation, retention, disclosure, correction, and identifier-purpose ledger for synthetic plate metadata with no personal-data ingestion", "CBR Heart and Freed ID", "completed", ["S12"]),
    ("THOS participant-free metadata transformation duel using permuted plate packets, equal edit ceilings, masked provenance labels, dominant stop states, and no effectiveness inference", "THOS Body", "represented", ["S08"]),
    ("Freed ID zero-key astronomical-plate provenance statement graph with synthetic status, disclosure-purpose, expiry, correction, and revocation placeholders", "Freed ID and CBR Heart", "represented", ["S03", "S07", "S09"]),
    ("GMUT plate-coordinate transform surrogate with typed frame placeholders, basis convention, dimensional abstention, and zero observations", "GMUT Mind", "represented", ["S01", "S10", "S11"]),
    ("GMUT plate-distortion and covariance tensor placeholder with typed coefficients, identifiability hold, uncertainty vacancy, and prediction refusal", "GMUT Mind", "represented", ["S10", "S11"]),
    ("FITS, IVOA, IAU, preservation, W3C, NIST, privacy, and Māori-data-authority source adapter with zero calls, zero rows, version holds, and authority nonconversion", "Trinity Mandala", "open_gap", ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13"]),
    ("CBR astronomical-plate authority docket reserving custody, rights, cultural knowledge, sensitive sky knowledge, worker safety, affected-party remedy, and Māori authority", "CBR Heart", "exact_gate", ["S04", "S05", "S12", "S13"]),
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
    for index, (title, pillar, expected, sources) in enumerate(PROPOSAL_SPECS, 1):
        pid = f"ELK6658-N{index:03d}"
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
                "concrete_artifact": f"docs/elaren-kestrel/v665-v8/x2/proposals/{pid.casefold()}/contract.json",
                "concrete_artifacts": [
                    f"docs/elaren-kestrel/v665-v8/x2/proposals/{pid.casefold()}/contract.json",
                    f"docs/elaren-kestrel/v665-v8/x2/proposals/{pid.casefold()}/mutation-results.json",
                    f"docs/elaren-kestrel/v665-v8/x2/proposals/{pid.casefold()}/bounded-receipt.json",
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
                "primary_pillar": "Freed ID and CBR Heart",
                "practice_lens": "wholly synthetic astronomical photographic-plate archive description and digitization planning",
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
    if len(corpus) != 4150:
        raise RuntimeError(f"expected 4150 inherited rows, observed {len(corpus)}")
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
        "astronomical photographic plate",
        "photographic plate archive",
        "plate digitization",
        "glass plate",
        "exposure provenance",
        "plate series",
        "plate enclosure",
        "plate coordinate",
    ]
    return {
        "schema": "ghc.family.elaren-kestrel.v665-v8.novelty-audit.v1",
        "owner": "Elaren Kestrel",
        "phase": "v665-v8",
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
        and len(corpus) == 4150,
        "interpretation": (
            "Similarity is a screening signal, not proof of novelty. Each proposal was also "
            "reviewed for a distinct astronomical photographic-plate archive contract, falsifier, and protected gate."
        ),
    }


def portfolio_rows(prefix: str, names: list[str], approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"ELK6658-{prefix}{index:02d}",
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
    "render the synthetic plate-intake identity schema",
    "render the glass-support and emulsion vocabulary schema",
    "build the enclosure-topology validator",
    "build the exposure-provenance record checker",
    "build the orientation and annotation-map checker",
    "build the plate-number reconciliation checker",
    "build the digitization job-versus-device firewall",
    "build the fiducial and calibration-placeholder checker",
    "build the derivative and FITS-lineage checker",
    "build the zero-row observation-table checker",
    "build the bitemporal plate-correction checker",
    "build the rights and contestation-ledger checker",
    "build the accessible noncolour archive-map checker",
    "build the privacy-minimisation ledger checker",
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
    "THOS participant-free matched-queue protocol representation",
    "Freed ID zero-key plate-provenance statement representation",
    "GMUT plate-coordinate transform surrogate",
    "GMUT plate-distortion and covariance tensor placeholder",
    "zero-call current-source adapter shell",
    "synthetic enclosure-topology fixture",
    "synthetic annotation-orientation fixture",
    "linear accessible report companion",
    "deterministic HTML report rendering",
    "synthetic metadata-handover workload simulation",
    "zero-row FITS-header mapping fixture",
    "synthetic plate-series reconciliation fixture",
    "source-status watch and version-hold fixture",
    "bitemporal contestation replay fixture",
    "fail-closed terminal route preflight",
]
EXACT_APPROVAL_NAMES = [
    "use a real archivist, astronomer, conservator, digitization worker, participant, or affected party",
    "handle, assess, move, image, scan, conserve, or discard a real photographic plate or enclosure",
    "operate or command a scanner, camera, telescope, instrument, lift, or other device",
    "identify a real celestial target, observer, institution, location, plate, or collection",
    "authenticate custody, authorship, copyright, annotations, provenance, catalogue identity, or observational truth",
    "author or approve Māori wording, traditional-knowledge interpretation, sensitive sky knowledge, or data-governance terms",
    "make an archival, astronomical, conservation, imaging, material, workplace-safety, or collection decision",
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
    "astronomical-plate-intake-boundary",
    "plate-enclosure-topology",
    "exposure-provenance-abstention",
    "digitization-device-firewall",
    "plate-annotation-orientation",
    "plate-catalogue-reconciliation",
    "plate-rights-contestation",
    "plate-source-profile-watch",
    "plate-method-flow",
    "plate-closeout-gate",
]
RUNNER_NAMES = [
    "ghc_family_elaren_kestrel_v665_v8_contracts",
    "ghc_family_elaren_kestrel_v665_v8_mutations",
    "ghc_family_elaren_kestrel_v665_v8_json",
    "ghc_family_elaren_kestrel_v665_v8_privacy",
    "ghc_family_elaren_kestrel_v665_v8_security",
    "ghc_family_elaren_kestrel_v665_v8_manifests",
    "ghc_family_elaren_kestrel_v665_v8_accessibility",
    "ghc_family_elaren_kestrel_v665_v8_truth",
    "ghc_family_elaren_kestrel_v665_v8_closeout",
    "ghc_family_elaren_kestrel_v665_v8_canonical",
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
    "REFINE: add bitemporal plate-correction lineage",
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
    ("the first skill-inventory wrapper piped a direct PowerShell foreach block into JSON serialization", "PowerShell rejected the expression before any task action or repository mutation", "materialize rows in a variable before serialization and prefer bounded scalar probes", "the complete required skill and reference set was read through EOF"),
    ("a later current-state metadata wrapper repeated the direct foreach-pipeline parser shape", "the parser recurrence produced no valid current-state projection", "retain the recurrence and use literal-path scalar reads for current artifacts", "the roster, authorization, source packet, manifests, and receipts were read and validated"),
    ("the first Git source-gate wrapper embedded native-command status inside an expression", "PowerShell stopped at parse time and no Git state changed", "separate native commands from boolean projection and compare exact scalar hashes", "source ancestry, cleanliness, divergence, and four-way equality were verified read-only"),
    ("the first proposal-freeze projection guessed a proposals key instead of the actual new_proposals key", "the null-index projection earned no proposal or novelty credit", "inspect the real JSON schema and use the committed new_proposals array", "the exact twenty-row Eiren freeze and 4,170-row inherited chain were reconstructed"),
    ("a broad four-source web lookup exceeded the useful display budget", "the truncated display earned no combined-source review credit", "query only the missing official source and preserve each source status separately", "the Privacy Commissioner source was recovered narrowly and the official-source ledger was bounded"),
    ("the first lane-uniqueness wrapper placed native status syntax inside a parenthesized assignment", "PowerShell rejected the wrapper before creating or changing a lane", "use branch-name output rather than native command status inside an expression", "the branch, remote ref, path, and worktree registration were proven unused"),
    ("a combined equality and version wrapper returned no visible payload", "the silent wrapper earned no equality or version credit", "separate the immutable Git gate from optional version observations", "the exact Git gate and each read-only version value were recorded independently"),
    ("the first sparse-lane proof enumerated git ls-files and flooded the display with the complete index", "index cardinality was incorrectly presented as if it measured materialized owner files", "measure physical files and skip-worktree state without printing the whole index", "the new lane was exact, clean, and physically materialized only one tracked file before owner additions"),
    ("the first non-skip index filter included S-prefixed skip-worktree rows", "the projected non-skip count was invalid and earned zero materialization credit", "classify S as skipped and use the physical filesystem as the decisive bounded witness", "the sparse patterns, one physical tracked file, exact head, and clean state were verified"),
    ("Eiren's sealed roster projection retained three older surname labels that differ from the current validated roster", "the inherited projection cannot authorize current routing and receives zero live-route credit", "preserve Eiren's immutable record while using the complete current roster, schema, auth state, and live activation", "the current fifteen-main-task roster validates Elaren v665-v8 and prospectively maps Neris Solane v666-v1"),
    ("the first whole-file transformation patch asked the patch engine to delete and add the same path in one transaction", "the patch engine rejected the operation before changing the file", "retain the failed patch and apply the prepared transformation as two guarded sequential patch operations", "the Elaren x1 builder was replaced additively with recoverable transformed content"),
    ("the first x1 test pass found inherited-title token overlap above the stricter semantic-screen threshold", "the uncommitted candidate earned zero x1 validation credit despite having no exact collision", "rename the three structurally over-similar surfaces and retain their distinct astronomical-plate hypotheses and gates", "the revised slate passes the inherited and within-slate similarity thresholds"),
    ("a combined multi-file semantic-correction patch missed one exact staged-review context", "the patch engine rejected every hunk before changing either file", "split builder and test corrections into separate exact-context patches", "the proposal, staged-review, and test expectations were updated without partial drift"),
]


def build_method_flow_startup() -> dict[str, Any]:
    rows = []
    for index, (request, failed, recovery, passing) in enumerate(STARTUP_FAILURES, 1):
        rows.append(
            {
                "method_id": f"ELK6658-MF-START-{index:03d}",
                "failure_id": f"ELK6658-START-N{index:03d}",
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
        "schema": "ghc.family.elaren-kestrel.v665-v8.method-flow-startup.v1",
        "owner": "Elaren Kestrel",
        "phase": "v665-v8",
        "generated_at_utc": NOW,
        "inherited_repository_sealed_negatives": 25918,
        "inherited_repository_sealed_methods": 10000,
        "inherited_external_overlay_negatives": 3,
        "inherited_external_overlay_methods": 3,
        "activation_baseline_negatives": 25921,
        "activation_baseline_methods": 10003,
        "new_startup_negative_count": len(rows),
        "new_startup_method_count": len(rows),
        "effective_after_x1_startup_negatives": 25921 + len(rows),
        "effective_after_x1_startup_methods": 10003 + len(rows),
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
            "original_owner": "Eiren Kestrel",
            "original_phase": "v665-v7",
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
        "schema": "ghc.family.elaren-kestrel.v665-v8.relational-identity.v1",
        "owner": "Elaren Kestrel",
        "pronouns": "they/them",
        "relational_role": "privacy-boundary steward and evidence cartographer",
        "relational_hope": "Make identity and records systems easier to contest, minimize, recover, and govern without promoting prototypes into authority.",
        "boundary": IDENTITY_BOUNDARY,
        "corrigibility": "Hamish may rename, pause, redirect, or stop this work.",
        "chosen_before_repository_mutation": True,
    }
    write_json("identity/relational-identity.json", identity)

    write_json(
        "provenance/source-verification.json",
        {
            "schema": "ghc.family.elaren-kestrel.v665-v8.source-verification.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
            "verified_at_utc": NOW,
            "source_branch": SOURCE_BRANCH,
            "source_sha": SOURCE_SHA,
            "source_parent_sha": "d8fde58e01141b1013c09f7771d3ff1efb609166",
            "evidence_sha": "d8fde58e01141b1013c09f7771d3ff1efb609166",
            "x1_sha": "b506a51a5b22c6bab84bdd2748a0deb1e85d145b",
            "inherited_source_sha": "959c32796fb822dba0a670c162d9489a044d0554",
            "direct_parent_chain": [
                "959c32796fb822dba0a670c162d9489a044d0554",
                "b506a51a5b22c6bab84bdd2748a0deb1e85d145b",
                "d8fde58e01141b1013c09f7771d3ff1efb609166",
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
                "evidence_entries": 112,
                "final_delta_entries": 23,
                "final_owner_entries": 156,
                "all_git_blob_hashes_equal": True,
                "deletions": 0,
            },
            "canonical_aggregate_status": "FAILED_IMPORT_PATH_SELECTED_TEST_DEPENDENCY_ZERO_CREDIT_NOT_REPLAYED",
            "canonical_receipt_sha256": "fbc13876b2c8e8920f928004fed724d51f836c67069fa70fafc9ea11b7900a10",
            "isolated_selected_test_recovery_status": "PASSED_65_OF_65_ONCE_NOT_REPLAYED",
            "dependency_corrected_composite_status": "VALID_25_OF_25_DETAILED_15_OF_15_MINIMAL_AGGREGATE_STILL_ZERO_CREDIT",
            "dependency_corrected_composite_receipt_sha256": "3a9f2f672af04963123b1d56c79bdeac4aaae1bb63b7db244fe2dcfe152773d0",
            "prepared_handoff_sha256": "1cac5f9f8e2c31d81e9cc2c7dc14206accbe3ed13c24b496baca5242a52783ec",
            "prepared_handoff_word_count": 3233,
            "source_packet_read_through_eof": True,
            "source_packet_file_count": 157,
            "source_json_parsed": 120,
            "successful_isolated_recovery_replayed": False,
            "full_repository_suite_run": False,
            "claim_boundary": "read-only verification and same-owner inherited evidence only",
        },
    )

    write_json(
        "provenance/source-profiles.json",
        {
            "schema": "ghc.family.elaren-kestrel.v665-v8.source-profiles.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
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
            "schema": "ghc.family.elaren-kestrel.v665-v8.proposal-freeze.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
            "generated_at_utc": NOW,
            "frozen": True,
            "inherited_frozen_baseline": 4150,
            "selected_inherited_revalidation_count": len(selected_inherited),
            "selected_inherited_revalidations": selected_inherited,
            "genuinely_new_proposal_count": len(proposals),
            "new_proposals": proposals,
            "new_frozen_total": 4170,
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
        "schema": "ghc.family.elaren-kestrel.v665-v8.portfolio-freeze.v1",
        "owner": "Elaren Kestrel",
        "phase": "v665-v8",
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
        "schema": "ghc.family.elaren-kestrel.v665-v8.authorization-boundary.v1",
        "owner": "Elaren Kestrel",
        "phase": "v665-v8",
        "generated_at_utc": NOW,
        "authorized_now": [
            "one solo additive owner lane from the exact Eiren final",
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
        "prospective_successor_label": "Neris Solane v666-v1",
        "successor_send_count": 0,
        "standby_contact_count": 0,
        "relational_boundary": IDENTITY_BOUNDARY,
    }
    write_json("x1/authorization-boundary.json", authorization)

    threats = [
        {
            "threat_id": "ELK6658-T01",
            "asset": "immutable Eiren source and sibling lanes",
            "threat": "accidental mutation, reset, merge, or ref reuse",
            "mitigation": "exact-head additive branch, owner-only paths, no merge/reset/force-push, four-way gates",
            "residual_risk": "operator command error remains possible and must be retained",
        },
        {
            "threat_id": "ELK6658-T02",
            "asset": "strict x1-before-x2 evidence",
            "threat": "implementation or outcome leakage into the x1 freeze",
            "mitigation": "path allowlist, x1 lifecycle test, staged review, immutable x1 manifest",
            "residual_risk": "misclassified prose; manual review remains required",
        },
        {
            "threat_id": "ELK6658-T03",
            "asset": "semantic novelty",
            "threat": "duplicate, paraphrased, or schema-relabelled inherited proposals",
            "mitigation": "4,150-row exact and token-Jaccard audit plus domain and falsifier review",
            "residual_risk": "automated similarity is not proof; bounded human review remains same-owner",
        },
        {
            "threat_id": "ELK6658-T04",
            "asset": "privacy and route confidentiality",
            "threat": "raw task identifiers, private paths, credentials, transcripts, or callable details in artifacts",
            "mitigation": "synthetic fixtures, five-class scans, repository-relative paths, no task/thread IDs",
            "residual_risk": "pattern scans are incomplete and never privacy certification",
        },
        {
            "threat_id": "ELK6658-T05",
            "asset": "astronomical-plate archive, conservation, imaging, worker, and affected-party authority boundaries",
            "threat": "software structure presented as archival, astronomical, conservation, imaging, safety, or affected-party competence or acceptance",
            "mitigation": "zero real people, plates, images, observatories, instruments, observations, measurements, devices, or actions and an exact-gated authority docket",
            "residual_risk": "terminology may still be incomplete or culturally inappropriate; authority remains external",
        },
        {
            "threat_id": "ELK6658-T06",
            "asset": "Māori language, concepts, data governance, and authority",
            "threat": "citation or synthetic labels converted into interpretation or authorization",
            "mitigation": "exact gate, zero Māori wording authored, source-profile authority nonconversion",
            "residual_risk": "Māori-authority review remains absent",
        },
        {
            "threat_id": "ELK6658-T07",
            "asset": "scientific truth boundaries",
            "threat": "GMUT surrogate promoted to empirical likelihood, force, prediction, proof, or canon",
            "mitigation": "typed placeholders, zero observations, dimensional abstention, explicit refusal",
            "residual_risk": "mathematical notation can invite overreading",
        },
        {
            "threat_id": "ELK6658-T08",
            "asset": "THOS and Freed ID boundaries",
            "threat": "proxy protocol or zero-key envelope presented as effectiveness or production identity evidence",
            "mitigation": "represented-only dispositions and explicit missing-evidence ledgers",
            "residual_risk": "no governed participants, independent review, real keys, or trust governance",
        },
        {
            "threat_id": "ELK6658-T09",
            "asset": "canonical validation truth",
            "threat": "replaying a successful aggregate or laundering a failed attempt",
            "mitigation": "exclusive external receipt, one-shot guard, zero credit for incomplete attempts",
            "residual_risk": "same-owner validation is not independent reproduction",
        },
        {
            "threat_id": "ELK6658-T10",
            "asset": "terminal route integrity",
            "threat": "premature, duplicate, ambiguous, or standby delivery",
            "mitigation": "PREPARED_NOT_SENT until final gate; fresh live roster/auth reread; exact-title single send",
            "residual_risk": "opaque acknowledgement must remain unresolved without resend",
        },
    ]
    threat_model = {
        "schema": "ghc.family.elaren-kestrel.v665-v8.threat-model.v1",
        "owner": "Elaren Kestrel",
        "phase": "v665-v8",
        "generated_at_utc": NOW,
        "scope": "owner-local v665-v8 software, documents, Git history, validation receipts, and terminal route candidate",
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
            "real archival, astronomical, conservation, imaging, worker study, or device operation",
            "production identity, empirical GMUT, governed THOS trial, legal, cultural, or Māori-authority review",
        ],
        "claim_boundary": "same-owner phase threat modelling only; not exhaustive security or certification",
    }
    write_json("x1/threat-model.json", threat_model)

    workflow = {
        "schema": "ghc.family.elaren-kestrel.v665-v8.workflow-plan.v1",
        "owner": "Elaren Kestrel",
        "phase": "v665-v8",
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
        "schema": "ghc.family.elaren-kestrel.v665-v8.x1-checklist.v1",
        "owner": "Elaren Kestrel",
        "phase": "v665-v8",
        "generated_at_utc": NOW,
        "completed": [
            "relational name, pronouns, role, hope, and disclaimer recorded before repository mutation",
            "authoritative activation and complete committed Eiren packet read through EOF",
            "required family skills, schemas, routing precedence, and current guidance read through EOF",
            "source branch, anchors, direct parents, zero merges, manifests, digests, clean state, divergence, and fresh live equality verified read-only",
            "all 4,150 inherited rows audited with zero exact-title collision",
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
            "schema": "ghc.family.elaren-kestrel.v665-v8.wellbeing-check.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
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
        "# Elaren Kestrel v665-v8 threat model",
        "",
        IDENTITY_BOUNDARY,
        "",
        PRACTICE_BOUNDARY,
        "",
        "## Scope and trust zones",
        "",
        "This is an owner-local, same-owner threat model for the v665-v8 document and software delta. It is not a repository-wide audit, penetration test, exhaustive-security claim, privacy certification, accessibility certification, or independent reproduction.",
        "",
        "The trust zones are immutable inherited Git objects, the additive Elaren worktree, public read-only source review, and the unexecuted external world. No real person, protected work, device, identity credential, or professional decision crosses into the synthetic zone.",
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

    overview = f"""# Elaren Kestrel v665-v8 x1 integrated overview

{IDENTITY_BOUNDARY}

## Outcome first

This x1 candidate freezes a planning-only, owner-local program from the exact Eiren Kestrel v665-v7 final `{SOURCE_SHA}`. It contains no x2 implementation, no observed outcome, no external action, no successor contact, and no Stage 20 promotion. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The primary Trinity Mandala focus is Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit and protected. The bounded human-practice lens is wholly synthetic astronomical photographic-plate archive description and digitization planning.

{PRACTICE_BOUNDARY}

## Source truth

The read-first gate verified the exact source branch, the three direct single-parent source-to-final commits, zero merges, the direct evidence parent, all declared manifests and receipt digests, a clean source lane, 0/0 divergence, and equality across local, upstream, tracking, and a fresh live remote. Eiren's single failed import-path canonical aggregate was not replayed. The isolated selected-test dependency recovery succeeded once and was not replayed. The full repository suite was not run.

The immutable Eiren seal contains 25,918 effective negatives, 10,000 Method Flow methods, 181 open gaps, and 179 exact gates. Three external zero-credit failures—the import-path canonical dependency, the serialized registry extractor assumption, and the overbroad stop-word scan—make the activation baseline 25,921 negatives and 10,003 methods. Thirteen Elaren pre-freeze failures are retained in `method-flow/startup-method-flow.json`; after those overlays, the x1 working baseline is 25,934 negatives and 10,016 methods. No inherited seal is rewritten.

## Novelty and proposals

All 4,150 inherited frozen rows were reconstructed from committed Git objects. Historical reappended selection rows were retained rather than silently deduplicated. The twenty Elaren titles have zero exact collisions. Their largest token-set overlap with an inherited title is {novelty['maximum_inherited_token_jaccard_similarity']:.6f}; the largest within-slate overlap is {novelty['maximum_new_pair_token_jaccard_similarity']:.6f}. Those scores are screening evidence only. The substantive review also requires a distinct contract, falsifier, rollback, and protected-gate set for every proposal.

The expected dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. These are preregistered expectations, not observed outcomes. Twenty Eiren proposals are selected only for bounded revalidation with zero novelty and zero automatic completion credit. The genuinely new chain would rise from 4,150 to 4,170 only when this x1 freeze is committed.

## Source profiles

The source profile names NASA FITS, the IAU photographic-plate working group, IVOA Provenance, the Library of Congress, the Canadian Conservation Institute, W3C PROV-O, WCAG 2.2, W3C Verifiable Credential Data Integrity, NIST SI and uncertainty guidance, the New Zealand Privacy Commissioner, and Te Mana Raraunga. Public sources provide vocabulary and refusal conditions only. They create no archival, astronomical, conservation, imaging, professional, safety, privacy, legal, cultural, Māori, or conformance authority.

## Safety, privacy, and authority

The threat model protects source immutability, x1/x2 separation, semantic integrity, privacy, astronomical-plate archival and affected-party authority, Māori authority, scientific boundaries, THOS and Freed ID evidence boundaries, one-shot validation, and terminal routing. Repository artifacts use repository-relative paths and exclude raw task identifiers, private routes, credentials, transcripts, screenshots, session streams, private callable details, and protected real-world data.

Exact-approval and blocked portfolios remain visible and unexecuted. No device command, real plate handling, image or observation assessment, worker or affected-party evaluation, record transformation, identity operation, professional decision, legal or cultural interpretation, Māori wording, or third-party write is planned.

## X1/x2 lifecycle

The x1 freeze includes proposals, portfolio plans, source and novelty records, the threat model, a complete/incomplete checklist, a wellbeing check, an authorization boundary, a workflow plan, and retained startup Method Flow. It intentionally excludes all `x2`, `evidence`, `closeout`, `seal`, `final`, and delivered-route content.

After this exact x1 candidate passes staged review, it may be committed and pushed. X2 may begin only after the x1 local, upstream, tracking, and fresh live remote heads are equal with 0/0 divergence and a clean lane. Later validation remains owner-scoped and same-owner. One successful canonical completion must never be replayed.

## Scientific and terminal boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Plate-coordinate surrogates or plate-distortion and covariance tensors establish no likelihood, constraint, force, prediction, material law, empirical confirmation, ultraviolet completion, final physics, Theory of Everything, proof, or canon. THOS remains represented without governed blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance.

No successor may be contacted during execution. Neris Solane v666-v1 is a prospective label only. A later send is permitted only after exact-final validation, a clean pushed fresh-live-equal final, a fresh live roster and authorization reread, unique exact-title resolution, and all protected route gates. Opaque acknowledgement must never trigger a resend merely for clarity.
"""
    write_text("x1/integrated-overview.md", overview)

    write_json(
        "x1/x1-build-receipt.json",
        {
            "schema": "ghc.family.elaren-kestrel.v665-v8.x1-build-receipt.v1",
            "owner": "Elaren Kestrel",
            "phase": "v665-v8",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_elaren_kestrel_v665_v8_x1.py",
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
        raise SystemExit("usage: build_ghc_family_elaren_kestrel_v665_v8_x1.py [--staged-review]")
    else:
        main()
