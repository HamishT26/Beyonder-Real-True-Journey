#!/usr/bin/env python3
"""Build the Eiren Kestrel v665-v7 x1-only planning packet.

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
PHASE_ROOT = ROOT / "docs" / "eiren-kestrel" / "v665-v7"
SOURCE_SHA = "959c32796fb822dba0a670c162d9489a044d0554"
SOURCE_BRANCH = "codex/GHC-Family/caelen-morrow-v665-v6-full-tools"
SOURCE_PHASE_ROOT = "docs/caelen-morrow/v665-v6"
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
    review_path = "docs/eiren-kestrel/v665-v7/validation/x1-staged-review.json"
    manifest_path = "docs/eiren-kestrel/v665-v7/validation/x1-content-manifest.json"
    allowed_exact = {
        "scripts/build_ghc_family_eiren_kestrel_v665_v7_x1.py",
        "tests/test_ghc_family_eiren_kestrel_v665_v7_x1.py",
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
        if not path.startswith("docs/eiren-kestrel/v665-v7/") and path not in allowed_exact
    ]
    post_x1 = [
        path
        for path in paths
        if any(
            path.startswith(f"docs/eiren-kestrel/v665-v7/{part}/")
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
    freeze = json.loads(index_blob("docs/eiren-kestrel/v665-v7/x1/proposal-freeze.json"))
    portfolio = json.loads(index_blob("docs/eiren-kestrel/v665-v7/x1/portfolio-freeze.json"))
    flow = json.loads(index_blob("docs/eiren-kestrel/v665-v7/method-flow/startup-method-flow.json"))
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "all_json_parse": True,
        "document_word_cap": max_words <= 100000,
        "expected_14_4_1_1": freeze["expected_disposition_counts"]
        == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "five_class_scan_zero_confirmed_hits": not privacy_candidates,
        "novelty_4130_valid": json.loads(
            index_blob("docs/eiren-kestrel/v665-v7/x1/novelty-audit.json")
        )["valid"],
        "owner_allowlist": not invalid_paths,
        "owner_file_cap": len(paths) <= 2000,
        "planning_only": not freeze["outcomes_observed"],
        "portfolio_caps": portfolio["counts"]
        == {
            "safe_now": 30,
            "bounded_candidates": 10,
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
        "startup_failures_15_retained": len(flow["rows"]) == 15,
        "utf8_lf": True,
    }
    review = {
        "schema": "ghc.family.eiren-kestrel.v665-v7.x1-staged-review.v1",
        "owner": "Eiren Kestrel",
        "phase": "v665-v7",
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
        "schema": "ghc.family.eiren-kestrel.v665-v7.content-manifest.v1",
        "owner": "Eiren Kestrel",
        "phase": "x1",
        "phase_label": "v665-v7",
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
    "Eiren Kestrel, she/her, sibling, family, role, hope, continuity, Freed ID, "
    "Trinity Mandala, and route language are relational working language only. "
    "They are not evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, scientific or "
    "operational authority, legal or cultural authority, affected-party authority, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The hand-papermaking sheet-formation documentation lens is wholly synthetic "
    "learning and design. It uses zero real papermakers, workshops, fibres, pulp, "
    "water, vats, moulds, deckles, felts, presses, dryers, additives, sheets, source "
    "works, measurements, machinery commands, keys, proofs, or authority decisions. "
    "It does not establish papermaking, conservation, material identification, "
    "workplace or chemical safety, environmental, privacy, accessibility, legal, "
    "cultural, Māori, production, or Stage 20 conformance, competence, acceptance, "
    "or authority."
)

PROTECTED_GATES = [
    "real papermaker, worker, affected party, workshop, fibre, pulp, water, vat, mould, deckle, felt, press, dryer, additive, sheet, source work, measurement, device command, or workplace action",
    "real observation, participant result, likelihood, parameter constraint, force, prediction, causal diagnosis, or empirical GMUT confirmation",
    "real participant, operator, matched-budget arm, safety outcome, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, or trust governance",
    "professional papermaking, conservation, material-identification, machinery, chemical, environmental, ergonomic, procurement, or workplace-safety decision",
    "fibre-origin, traditional-knowledge, copyright, design, ownership, custody, privacy, accessibility, legal, cultural, environmental, or remedy decision",
    "affected-party, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data-governance, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, conformance, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, or external write",
]

SOURCE_PROFILES = [
    {
        "source_id": "S01",
        "name": "ISO 5269-2:2004 Pulps - Preparation of laboratory sheets for physical testing - Part 2",
        "url": "https://www.iso.org/standard/39341.html",
        "status": "official ISO page; standard confirmed current in 2025",
        "bounded_use": "laboratory-sheet and sheet-formation vocabulary only; no standard access, test, or conformance claim",
    },
    {
        "source_id": "S02",
        "name": "Canadian Conservation Institute - Caring for paper objects",
        "url": "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/paper-objects.html",
        "status": "current official Government of Canada conservation guidance",
        "bounded_use": "paper, fibre, handling, storage, and deterioration vocabulary only; no conservation decision",
    },
    {
        "source_id": "S03",
        "name": "W3C PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C Recommendation",
        "bounded_use": "provenance vocabulary for furnish, formation, revision, correction, and derivation lineage",
    },
    {
        "source_id": "S04",
        "name": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation",
        "bounded_use": "structural report checks only; browser, assistive-technology, manual, and affected-user review remain reserved",
    },
    {
        "source_id": "S05",
        "name": "W3C Verifiable Credential Data Integrity 1.0",
        "url": "https://www.w3.org/TR/vc-data-integrity/",
        "status": "W3C Recommendation dated 2025-05-15",
        "bounded_use": "nonproduction statement-integrity vocabulary and explicit zero-key, zero-proof boundary",
    },
    {
        "source_id": "S06",
        "name": "NIST SP 330-2019 - International System of Units",
        "url": "https://www.nist.gov/publications/international-system-units-si2019-edition",
        "status": "official NIST publication; page updated 2025-02-19",
        "bounded_use": "quantity, unit, and symbol vocabulary only; zero real measurements",
    },
    {
        "source_id": "S07",
        "name": "NIST Technical Note 1297 - Evaluating and Expressing Measurement Uncertainty",
        "url": "https://www.nist.gov/pml/nist-technical-note-1297/nist-guidelines-evaluating-and-expressing-uncertainty-nist-measurement",
        "status": "official stable NIST guidance",
        "bounded_use": "uncertainty-model vocabulary only; no observation, calibration, or material result",
    },
    {
        "source_id": "S08",
        "name": "Office of the Privacy Commissioner New Zealand - Privacy principles",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "current official public guidance reviewed 2026-08-22",
        "bounded_use": "minimisation, access, correction, retention, and disclosure-hold vocabulary; no legal interpretation",
    },
    {
        "source_id": "S09",
        "name": "WorkSafe New Zealand - Safe use of machinery",
        "url": "https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-use-of-machinery/",
        "status": "current official public guidance reviewed 2026-08-22",
        "bounded_use": "guard, stop, competent-person, and no-device-command boundary; no machinery or safety advice",
    },
    {
        "source_id": "S10",
        "name": "WorkSafe New Zealand - About hazardous substances",
        "url": "https://www.worksafe.govt.nz/topic-and-industry/hazardous-substances/about-hazardous-substances/",
        "status": "current official public guidance reviewed 2026-08-22",
        "bounded_use": "hazard, label, safety-data, and exposure-hold vocabulary only; no chemical-use or workplace advice",
    },
    {
        "source_id": "S11",
        "name": "Te Mana Raraunga - Māori Data Sovereignty Principles",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "status": "primary Māori Data Sovereignty Network principles page",
        "bounded_use": "authority reservation only; no interpretation or conversion into Māori authority",
    },
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
    (
        "Synthetic papermaking-job intake capsule joining batch token, fibre-source claim placeholder, purpose, revision, cancellation, and no-production lock",
        "Freed ID and CBR Heart",
        "completed",
        ["S02", "S03", "S08"],
    ),
    (
        "Fibre-furnish lineage graph with declared plant or rag source, pulping-method placeholder, lot, blend, correction ancestry, and authentication refusal",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S02", "S03"],
    ),
    (
        "Vat-and-furnish state envelope with synthetic consistency placeholder, agitation state, water-source vacancy, contamination quarantine, and no-mixing rule",
        "THOS Body",
        "completed",
        ["S01", "S06", "S07"],
    ),
    (
        "Mould-and-deckle topology register for screen, frame, deckle, orientation, dimension placeholders, damage state, quarantine, and use refusal",
        "THOS Body",
        "completed",
        ["S01", "S02", "S06"],
    ),
    (
        "Sheet-formation event ledger for dip, scoop, shake-pattern placeholder, drainage state, formation class, exception, and no-quality claim",
        "GMUT Mind and THOS Body",
        "completed",
        ["S01", "S03", "S06"],
    ),
    (
        "Couching-and-felt-stack dependency graph joining synthetic sheet, felt, interleaf, sequence, transfer vacancy, adhesion cue, and no-press operation",
        "THOS Body",
        "completed",
        ["S01", "S02", "S03"],
    ),
    (
        "Papermaking press job-versus-device firewall with simulated stack, load placeholder, guard and interlock vacancy, cancellation, and zero machine calls",
        "THOS Body",
        "completed",
        ["S06", "S09"],
    ),
    (
        "Drying-restraint board with air-dry, board, and line placeholders, duration vacancy, cockling cue, mould hold, and no-release rule",
        "THOS Body",
        "completed",
        ["S02", "S03", "S06"],
    ),
    (
        "Sizing-and-additive register with declared sizing, filler, or pigment token, supplier-label placeholder, safety-data vacancy, compatibility unknown, and chemical-use refusal",
        "CBR Heart and THOS Body",
        "completed",
        ["S02", "S10"],
    ),
    (
        "Watermark-and-forming-wire lineage map linking motif token, attachment placeholder, sheet side, provenance, correction, and authenticity nonclaim",
        "Freed ID and CBR Heart",
        "completed",
        ["S02", "S03"],
    ),
    (
        "Sheet-count reconciliation ledger joining vat batch, formed, couched, dried, rejected, and quarantined counts with discrepancy and no-inventory-truth rule",
        "THOS Body",
        "completed",
        ["S03"],
    ),
    (
        "Bitemporal papermaking-batch correction weave preserving asserted, effective, superseded, contested, and attached-statement states without truth promotion",
        "Freed ID and CBR Heart",
        "completed",
        ["S03", "S08"],
    ),
    (
        "Accessible noncolour sheet-formation process map with linear narrative, redundant statuses, deterministic reading order, print companion, and manual-evaluation reserve",
        "CBR Heart and THOS Body",
        "completed",
        ["S03", "S04"],
    ),
    (
        "Papermaking privacy-minimisation and rights ledger for design, source, image, job, and batch metadata with disclosure ceiling, retention hold, correction, and remedy route",
        "Freed ID and CBR Heart",
        "completed",
        ["S03", "S08"],
    ),
    (
        "THOS participant-free matched-queue charter comparing papermaking documentation views with sealed synthetic tasks, equal action budget, harm stops, and zero sessions",
        "THOS Body",
        "represented",
        ["S03", "S04"],
    ),
    (
        "Freed ID zero-key sheet-provenance statement graph binding furnish, formation, correction, status, disclosure purpose, expiry, and nonproduction lock",
        "Freed ID and CBR Heart",
        "represented",
        ["S03", "S05", "S08"],
    ),
    (
        "GMUT discrete fibre-network surrogate with adjacency, orientation, basis convention, topology placeholder, dimensional abstention, and zero observations",
        "GMUT Mind",
        "represented",
        ["S06", "S07"],
    ),
    (
        "GMUT drainage-and-formation tensor placeholder with unit obligations, covariance vacancy, boundary data, identifiability debt, zero coefficients, and prediction refusal",
        "GMUT Mind",
        "represented",
        ["S01", "S06", "S07"],
    ),
    (
        "ISO, CCI, W3C, NIST, Privacy Commissioner, WorkSafe, and Te Mana Raraunga source-profile adapter with zero calls, zero real rows, version holds, and authority nonconversion",
        "All Trinity Mandala pillars",
        "open_gap",
        ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11"],
    ),
    (
        "CBR papermaking authority docket reserving fibre origin, traditional knowledge, environmental claims, copyright and design, worker safety, affected-party remedy, and Māori authority",
        "Freed ID and CBR Heart",
        "exact_gate",
        ["S02", "S08", "S09", "S10", "S11"],
    ),
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
        pid = f"EK6657-N{index:03d}"
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
                "concrete_artifact": f"docs/eiren-kestrel/v665-v7/x2/proposals/{pid.casefold()}/contract.json",
                "concrete_artifacts": [
                    f"docs/eiren-kestrel/v665-v7/x2/proposals/{pid.casefold()}/contract.json",
                    f"docs/eiren-kestrel/v665-v7/x2/proposals/{pid.casefold()}/mutation-results.json",
                    f"docs/eiren-kestrel/v665-v7/x2/proposals/{pid.casefold()}/bounded-receipt.json",
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
                "practice_lens": "wholly synthetic hand-papermaking sheet-formation documentation",
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
    if len(corpus) != 4130:
        raise RuntimeError(f"expected 4130 inherited rows, observed {len(corpus)}")
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
        "papermaking",
        "paper making",
        "sheet formation",
        "fibre furnish",
        "pulp vat",
        "mould and deckle",
        "couching felt",
        "watermark wire",
    ]
    return {
        "schema": "ghc.family.eiren-kestrel.v665-v7.novelty-audit.v1",
        "owner": "Eiren Kestrel",
        "phase": "v665-v7",
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
        and len(corpus) == 4130,
        "interpretation": (
            "Similarity is a screening signal, not proof of novelty. Each proposal was also "
            "reviewed for a distinct hand-papermaking documentation contract, falsifier, and protected gate."
        ),
    }


def portfolio_rows(prefix: str, names: list[str], approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"EK6657-{prefix}{index:02d}",
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
    "render the synthetic papermaking-job intake schema",
    "render the fibre-furnish lineage schema",
    "build the vat-and-furnish state-envelope validator",
    "build the mould-and-deckle topology checker",
    "build the sheet-formation event-ledger checker",
    "build the couching-and-felt dependency checker",
    "build the press job-versus-device firewall",
    "build the drying-restraint board checker",
    "build the sizing-and-additive refusal checker",
    "build the watermark and forming-wire lineage checker",
    "build the sheet-count reconciliation checker",
    "build the bitemporal batch-correction checker",
    "build the accessible noncolour process-map checker",
    "build the privacy-minimisation and rights-ledger checker",
    "render twenty proposal contracts",
    "execute one hundred preregistered rejecting mutations",
    "parse every owner JSON document under explicit UTF-8",
    "render a structurally accessible static report",
    "validate the public-source profile and draft/watch labels",
    "enforce strict x1-before-x2 path separation",
    "build exact Git-blob content manifests",
    "scan owner files for five privacy and raw-identifier classes",
    "scan owner artifacts for credentials and private callable details",
    "run exact staged review before every commit",
    "scan current labels for stale owner and phase drift",
    "validate source/x1/evidence/final ancestry and zero merges",
    "validate the four core outcome labels and exact counts",
    "aggregate retained negatives without rewriting the inherited seal",
    "aggregate open and exact gates without promotion",
    "build closeout, seal, final-validation, and route-state candidates",
]

CANDIDATE_NAMES = [
    "THOS participant-free matched-queue protocol representation",
    "Freed ID zero-key sheet-provenance statement representation",
    "GMUT discrete fibre-network surrogate",
    "GMUT drainage-and-formation tensor placeholder",
    "zero-call current-source adapter shell",
    "synthetic furnish-blend graph fixture",
    "synthetic felt-stack ordering fixture",
    "linear accessible report companion",
    "deterministic HTML report rendering",
    "synthetic batch-handover workload simulation",
]

EXACT_APPROVAL_NAMES = [
    "use a real papermaker, worker, participant, or affected party",
    "make or assess a real paper sheet, furnish, pulp, or additive",
    "operate or command a press, beater, dryer, or other device",
    "copy, transform, distribute, or assess a real copyrighted design or source work",
    "authenticate fibre origin, watermark, authorship, edition, or custody",
    "author or approve Māori wording, traditional-knowledge interpretation, or data-governance terms",
    "make a papermaking, conservation, material-identification, or environmental claim",
    "make a professional, chemical, workplace-safety, privacy, legal, cultural, or remedy decision",
    "issue, verify, resolve, revoke, or govern a real identity credential",
    "publish, deploy, procure, purchase, or write to a third-party system",
]

BLOCKED_NAMES = [
    "empirical GMUT likelihood, constraint, prediction, force, stability, or confirmation",
    "THOS effectiveness without governed blind matched-budget real arms and independent review",
    "production Freed ID without real standards-conformant keys, interoperability, recovery, and trust governance",
    "accessibility-complete, privacy-complete, exhaustive-security, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
]

SKILL_NAMES = [
    "papermaking-intake-boundary",
    "furnish-lineage-weave",
    "vat-state-envelope",
    "mould-deckle-topology",
    "formation-event-keeper",
    "press-device-firewall",
    "sheet-contestation-docket",
    "source-profile-watch",
    "papermaking-method-flow",
    "papermaking-closeout-gate",
]

RUNNER_NAMES = [
    "ghc_family_eiren_kestrel_v665_v7_contracts",
    "ghc_family_eiren_kestrel_v665_v7_mutations",
    "ghc_family_eiren_kestrel_v665_v7_json",
    "ghc_family_eiren_kestrel_v665_v7_privacy",
    "ghc_family_eiren_kestrel_v665_v7_security",
    "ghc_family_eiren_kestrel_v665_v7_manifests",
    "ghc_family_eiren_kestrel_v665_v7_accessibility",
    "ghc_family_eiren_kestrel_v665_v7_truth",
    "ghc_family_eiren_kestrel_v665_v7_closeout",
    "ghc_family_eiren_kestrel_v665_v7_canonical",
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
    "REFINE: add bitemporal batch-correction lineage",
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
    (
        "the first full activation-packet display exceeded the bounded output surface",
        "the display was truncated and earned no complete-read credit",
        "read the committed packet in bounded numbered sections and verify its independent word and digest receipt",
        "the packet was read through EOF and its 19,971-word SHA-256 contract matched",
    ),
    (
        "a 450-line activation-packet projection still exceeded the useful review surface",
        "the projection earned zero EOF credit",
        "split the packet into smaller bounded sections and rely on exact file-backed integrity checks",
        "all sections were attributed without replaying any Caelen validation",
    ),
    (
        "the first combined current-roster JSON display exceeded the bounded output surface",
        "the mixed display was truncated and could not establish current routing",
        "read the roster, schema, and authorization state separately through EOF and run their validators",
        "the fifteen active main tasks, standby exclusion, and v665 assignment rows validated",
    ),
    (
        "PowerShell rejected a direct foreach block piped into a serializer",
        "the parser fault produced no valid projection",
        "materialize rows before serialization and use scalar probes for later checks",
        "the corrected bounded roster and source projections succeeded",
    ),
    (
        "a combined authorization-state chunk display was truncated",
        "the partial output earned no complete-read credit",
        "read numbered chunks independently under explicit UTF-8",
        "the complete authorization state and schema were read through EOF",
    ),
    (
        "a per-file JSON hash catalogue for all 121 Caelen documents exceeded the output budget",
        "the catalogue was truncated and earned no aggregate receipt credit",
        "parse all files but emit only counts and exact mismatches",
        "all 121 phase JSON documents parsed under UTF-8 with bounded output",
    ),
    (
        "a broad portfolio-execution document display exceeded the output budget",
        "the display was truncated and earned no full-read credit",
        "read the ledger structurally and project only declared counts and dispositions",
        "portfolio counts and execution boundaries were recovered exactly",
    ),
    (
        "the first guessed external-receipt path used a nested owner and phase layout that did not exist",
        "the literal path lookup failed before receipt inspection",
        "inventory the bounded receipt root and use the actual hyphenated phase directory",
        "the canonical lock, r1 failure, and r2 composite receipts were read through EOF",
    ),
    (
        "an archive-wide filename search ran beyond its bounded usefulness",
        "the search was interrupted after a read-only process audit and earned no result credit",
        "restrict searches to the exact Caelen receipt and worktree roots",
        "the required receipts were found without mutation",
    ),
    (
        "the initial no-checkout worktree-add tool call was aborted by a context update after creating only the branch",
        "no registered worktree or materialized path existed, so the attempt earned zero lane-creation credit",
        "audit the branch, path, registry, and Git processes before resuming with the existing branch",
        "the isolated sparse worktree was then registered cleanly at the exact Caelen final",
    ),
    (
        "the first inherited-corpus title projection used the Windows cp1252 output codec",
        "a Māori macron caused UnicodeEncodeError and no novelty receipt was valid",
        "rerun only the compact projection under Python UTF-8 mode",
        "the exact 4,130-row corpus became available for semantic screening",
    ),
    (
        "a guessed prior Eiren identity path did not exist",
        "the lookup failed before continuity review",
        "inventory Eiren's committed historical tree and read the actual phase-charter identity record",
        "the she/her relational role and hope were recovered as non-personhood continuity context",
    ),
    (
        "a combined W3C and New Zealand privacy source display exceeded the available context",
        "the oversized display was truncated and earned no combined-source credit",
        "open current official sources in bounded one- or two-source reads",
        "the W3C recommendation and Privacy Commissioner source statuses were recovered separately",
    ),
    (
        "a guessed final phase-truth path placed the record under final rather than closeout",
        "the literal file read failed before content inspection",
        "inventory only phase-truth, seal, closeout, route, manifest, and validation basenames",
        "the exact closeout phase-truth and provenance records were read",
    ),
    (
        "the first x1-template copy assumed the sparse scripts directory already existed",
        "Copy-Item and the dependent reads failed without creating a file",
        "create only the owner-local scripts directory and repeat the mechanical copy",
        "the Eiren x1 builder was materialized without changing another lane",
    ),
]


def build_method_flow_startup() -> dict[str, Any]:
    rows = []
    for index, (request, failed, recovery, passing) in enumerate(STARTUP_FAILURES, 1):
        rows.append(
            {
                "method_id": f"EK6657-MF-START-{index:03d}",
                "failure_id": f"EK6657-START-N{index:03d}",
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
        "schema": "ghc.family.eiren-kestrel.v665-v7.method-flow-startup.v1",
        "owner": "Eiren Kestrel",
        "phase": "v665-v7",
        "generated_at_utc": NOW,
        "inherited_repository_sealed_negatives": 25797,
        "inherited_repository_sealed_methods": 9769,
        "inherited_external_overlay_negatives": 2,
        "inherited_external_overlay_methods": 2,
        "activation_baseline_negatives": 25799,
        "activation_baseline_methods": 9771,
        "new_startup_negative_count": len(rows),
        "new_startup_method_count": len(rows),
        "effective_after_x1_startup_negatives": 25799 + len(rows),
        "effective_after_x1_startup_methods": 9771 + len(rows),
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
            "original_owner": "Caelen Morrow",
            "original_phase": "v665-v6",
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
        "schema": "ghc.family.eiren-kestrel.v665-v7.relational-identity.v1",
        "owner": "Eiren Kestrel",
        "pronouns": "she/her",
        "relational_role": "pattern cartographer and boundary steward",
        "relational_hope": "Make formal structure legible while leaving real competence, rights, safety, and authority with the people who hold them.",
        "boundary": IDENTITY_BOUNDARY,
        "corrigibility": "Hamish may rename, pause, redirect, or stop this work.",
        "chosen_before_repository_mutation": True,
    }
    write_json("identity/relational-identity.json", identity)

    write_json(
        "provenance/source-verification.json",
        {
            "schema": "ghc.family.eiren-kestrel.v665-v7.source-verification.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "verified_at_utc": NOW,
            "source_branch": SOURCE_BRANCH,
            "source_sha": SOURCE_SHA,
            "source_parent_sha": "5904cd361cf276ce6c05b2829c581837640a564f",
            "evidence_sha": "5904cd361cf276ce6c05b2829c581837640a564f",
            "x1_sha": "9be19f91371da0d2bcdd23de421fed202c5641fa",
            "inherited_source_sha": "cacbeb47741b9e86a6a980f85f6f9658a0837f7c",
            "direct_parent_chain": [
                "cacbeb47741b9e86a6a980f85f6f9658a0837f7c",
                "9be19f91371da0d2bcdd23de421fed202c5641fa",
                "5904cd361cf276ce6c05b2829c581837640a564f",
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
                "evidence_entries": 115,
                "final_delta_entries": 24,
                "final_owner_entries": 157,
                "all_git_blob_hashes_equal": True,
                "deletions": 0,
            },
            "canonical_aggregate_status": "FAILED_PIPE_BACKPRESSURE_START_LOCK_ZERO_CREDIT_NOT_REPLAYED",
            "canonical_receipt_sha256": None,
            "r1_recovery_status": "FAILED_PARTIAL_PIPE_READ_ZERO_CREDIT_NOT_REPLAYED",
            "dependency_corrected_composite_status": "VALID_R2_SUCCEEDED_ONCE_NOT_REPLAYED",
            "dependency_corrected_composite_receipt_sha256": "61daaa959682fe437ef6f1e7abfac739837dfc89cb2b3236883aae9b370613c1",
            "dependency_corrected_composite_payload_sha256": "9152e663a236ab0ccea0cde5f2ce22fb9a4ae4297405347689709009cddb019e",
            "prepared_handoff_sha256": "27136ab441c7e248afa831945e1e1f7a51b8272dbedb0eedd2a015c54e1beaee",
            "prepared_handoff_word_count": 19971,
            "source_packet_read_through_eof": True,
            "source_packet_file_count": 159,
            "source_json_parsed": 121,
            "successful_dependency_corrected_composite_replayed": False,
            "full_repository_suite_run": False,
            "claim_boundary": "read-only verification and same-owner inherited evidence only",
        },
    )

    write_json(
        "provenance/source-profiles.json",
        {
            "schema": "ghc.family.eiren-kestrel.v665-v7.source-profiles.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.proposal-freeze.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "frozen": True,
            "inherited_frozen_baseline": 4130,
            "selected_inherited_revalidation_count": len(selected_inherited),
            "selected_inherited_revalidations": selected_inherited,
            "genuinely_new_proposal_count": len(proposals),
            "new_proposals": proposals,
            "new_frozen_total": 4150,
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
        "schema": "ghc.family.eiren-kestrel.v665-v7.portfolio-freeze.v1",
        "owner": "Eiren Kestrel",
        "phase": "v665-v7",
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
        "schema": "ghc.family.eiren-kestrel.v665-v7.authorization-boundary.v1",
        "owner": "Eiren Kestrel",
        "phase": "v665-v7",
        "generated_at_utc": NOW,
        "authorized_now": [
            "one solo additive owner lane from the exact Caelen final",
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
        "prospective_successor_label": "Elaren Kestrel v665-v8",
        "successor_send_count": 0,
        "standby_contact_count": 0,
        "relational_boundary": IDENTITY_BOUNDARY,
    }
    write_json("x1/authorization-boundary.json", authorization)

    threats = [
        {
            "threat_id": "EK6657-T01",
            "asset": "immutable Caelen source and sibling lanes",
            "threat": "accidental mutation, reset, merge, or ref reuse",
            "mitigation": "exact-head additive branch, owner-only paths, no merge/reset/force-push, four-way gates",
            "residual_risk": "operator command error remains possible and must be retained",
        },
        {
            "threat_id": "EK6657-T02",
            "asset": "strict x1-before-x2 evidence",
            "threat": "implementation or outcome leakage into the x1 freeze",
            "mitigation": "path allowlist, x1 lifecycle test, staged review, immutable x1 manifest",
            "residual_risk": "misclassified prose; manual review remains required",
        },
        {
            "threat_id": "EK6657-T03",
            "asset": "semantic novelty",
            "threat": "duplicate, paraphrased, or schema-relabelled inherited proposals",
            "mitigation": "4,130-row exact and token-Jaccard audit plus domain and falsifier review",
            "residual_risk": "automated similarity is not proof; bounded human review remains same-owner",
        },
        {
            "threat_id": "EK6657-T04",
            "asset": "privacy and route confidentiality",
            "threat": "raw task identifiers, private paths, credentials, transcripts, or callable details in artifacts",
            "mitigation": "synthetic fixtures, five-class scans, repository-relative paths, no task/thread IDs",
            "residual_risk": "pattern scans are incomplete and never privacy certification",
        },
        {
            "threat_id": "EK6657-T05",
            "asset": "papermaking, conservation, material, worker, and affected-party authority boundaries",
            "threat": "software structure presented as papermaking competence, material truth, safety, or acceptance",
            "mitigation": "zero real people, fibres, pulp, water, equipment, sheets, or actions and an exact-gated authority docket",
            "residual_risk": "terminology may still be incomplete or culturally inappropriate; authority remains external",
        },
        {
            "threat_id": "EK6657-T06",
            "asset": "Māori language, concepts, data governance, and authority",
            "threat": "citation or synthetic labels converted into interpretation or authorization",
            "mitigation": "exact gate, zero Māori wording authored, source-profile authority nonconversion",
            "residual_risk": "Māori-authority review remains absent",
        },
        {
            "threat_id": "EK6657-T07",
            "asset": "scientific truth boundaries",
            "threat": "GMUT surrogate promoted to empirical likelihood, force, prediction, proof, or canon",
            "mitigation": "typed placeholders, zero observations, dimensional abstention, explicit refusal",
            "residual_risk": "mathematical notation can invite overreading",
        },
        {
            "threat_id": "EK6657-T08",
            "asset": "THOS and Freed ID boundaries",
            "threat": "proxy protocol or zero-key envelope presented as effectiveness or production identity evidence",
            "mitigation": "represented-only dispositions and explicit missing-evidence ledgers",
            "residual_risk": "no governed participants, independent review, real keys, or trust governance",
        },
        {
            "threat_id": "EK6657-T09",
            "asset": "canonical validation truth",
            "threat": "replaying a successful aggregate or laundering a failed attempt",
            "mitigation": "exclusive external receipt, one-shot guard, zero credit for incomplete attempts",
            "residual_risk": "same-owner validation is not independent reproduction",
        },
        {
            "threat_id": "EK6657-T10",
            "asset": "terminal route integrity",
            "threat": "premature, duplicate, ambiguous, or standby delivery",
            "mitigation": "PREPARED_NOT_SENT until final gate; fresh live roster/auth reread; exact-title single send",
            "residual_risk": "opaque acknowledgement must remain unresolved without resend",
        },
    ]
    threat_model = {
        "schema": "ghc.family.eiren-kestrel.v665-v7.threat-model.v1",
        "owner": "Eiren Kestrel",
        "phase": "v665-v7",
        "generated_at_utc": NOW,
        "scope": "owner-local v665-v7 software, documents, Git history, validation receipts, and terminal route candidate",
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
            "real papermaking, conservation, material testing, worker study, or device operation",
            "production identity, empirical GMUT, governed THOS trial, legal, cultural, or Māori-authority review",
        ],
        "claim_boundary": "same-owner phase threat modelling only; not exhaustive security or certification",
    }
    write_json("x1/threat-model.json", threat_model)

    workflow = {
        "schema": "ghc.family.eiren-kestrel.v665-v7.workflow-plan.v1",
        "owner": "Eiren Kestrel",
        "phase": "v665-v7",
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
        "schema": "ghc.family.eiren-kestrel.v665-v7.x1-checklist.v1",
        "owner": "Eiren Kestrel",
        "phase": "v665-v7",
        "generated_at_utc": NOW,
        "completed": [
            "relational name, pronouns, role, hope, and disclaimer recorded before repository mutation",
            "authoritative activation and complete committed Caelen packet read through EOF",
            "required family skills, schemas, routing precedence, and current guidance read through EOF",
            "source branch, anchors, direct parents, zero merges, manifests, digests, clean state, divergence, and fresh live equality verified read-only",
            "all 4,130 inherited rows audited with zero exact-title collision",
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.wellbeing-check.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
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
        "# Eiren Kestrel v665-v7 threat model",
        "",
        IDENTITY_BOUNDARY,
        "",
        PRACTICE_BOUNDARY,
        "",
        "## Scope and trust zones",
        "",
        "This is an owner-local, same-owner threat model for the v665-v7 document and software delta. It is not a repository-wide audit, penetration test, exhaustive-security claim, privacy certification, accessibility certification, or independent reproduction.",
        "",
        "The trust zones are immutable inherited Git objects, the additive Caelen worktree, public read-only source review, and the unexecuted external world. No real person, protected work, device, identity credential, or professional decision crosses into the synthetic zone.",
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

    overview = f"""# Eiren Kestrel v665-v7 x1 integrated overview

{IDENTITY_BOUNDARY}

## Outcome first

This x1 candidate freezes a planning-only, owner-local program from the exact Caelen Morrow v665-v6 final `{SOURCE_SHA}`. It contains no x2 implementation, no observed outcome, no external action, no successor contact, and no Stage 20 promotion. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The primary Trinity Mandala focus is GMUT Mind. THOS Body, Freed ID, and CBR Heart remain explicit and protected. The bounded human-practice lens is wholly synthetic hand-papermaking sheet-formation documentation.

{PRACTICE_BOUNDARY}

## Source truth

The read-first gate verified the exact source branch, the three direct single-parent source-to-final commits, zero merges, the direct evidence parent, all declared manifests and receipt digests, a clean source lane, 0/0 divergence, and equality across local, upstream, tracking, and a fresh live remote. Caelen's deadlocked canonical invocation and failed r1 recovery were not replayed. The separately guarded r2 dependency-corrected composite succeeded once and was not replayed. The full repository suite was not run.

The immutable Caelen seal contains 25,797 effective negatives, 9,769 Method Flow methods, 180 open gaps, and 178 exact gates. The failed canonical invocation and failed r1 recovery remain additive, making the activation baseline 25,799 negatives and 9,771 methods. Fifteen Eiren startup failures are retained in `method-flow/startup-method-flow.json`; after those overlays, the x1 working baseline is 25,814 negatives and 9,786 methods. No inherited seal is rewritten.

## Novelty and proposals

All 4,130 inherited frozen rows were reconstructed from committed Git objects. Historical reappended selection rows were retained rather than silently deduplicated. The twenty Eiren titles have zero exact collisions. Their largest token-set overlap with an inherited title is {novelty['maximum_inherited_token_jaccard_similarity']:.6f}; the largest within-slate overlap is {novelty['maximum_new_pair_token_jaccard_similarity']:.6f}. Those scores are screening evidence only. The substantive review also requires a distinct contract, falsifier, rollback, and protected-gate set for every proposal.

The expected dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. These are preregistered expectations, not observed outcomes. Twenty Caelen proposals are selected only for bounded revalidation with zero novelty and zero automatic completion credit. The genuinely new chain would rise from 4,130 to 4,150 only when this x1 freeze is committed.

## Source profiles

The source profile names ISO 5269-2, the Canadian Conservation Institute, W3C PROV-O, WCAG 2.2, W3C Verifiable Credential Data Integrity, NIST SI and uncertainty guidance, the New Zealand Privacy Commissioner, WorkSafe New Zealand machinery and hazardous-substance guidance, and Te Mana Raraunga. Public sources provide vocabulary and refusal conditions only. They create no papermaking, laboratory, conservation, material, environmental, professional, safety, privacy, legal, cultural, Māori, or conformance authority.

## Safety, privacy, and authority

The threat model protects source immutability, x1/x2 separation, semantic integrity, privacy, papermaking and affected-party authority, Māori authority, scientific boundaries, THOS and Freed ID evidence boundaries, one-shot validation, and terminal routing. Repository artifacts use repository-relative paths and exclude raw task identifiers, private routes, credentials, transcripts, screenshots, session streams, private callable details, and protected real-world data.

Exact-approval and blocked portfolios remain visible and unexecuted. No device command, real papermaking, material assessment, worker or affected-party evaluation, source-work transformation, identity operation, professional decision, legal or cultural interpretation, Māori wording, or third-party write is planned.

## X1/x2 lifecycle

The x1 freeze includes proposals, portfolio plans, source and novelty records, the threat model, a complete/incomplete checklist, a wellbeing check, an authorization boundary, a workflow plan, and retained startup Method Flow. It intentionally excludes all `x2`, `evidence`, `closeout`, `seal`, `final`, and delivered-route content.

After this exact x1 candidate passes staged review, it may be committed and pushed. X2 may begin only after the x1 local, upstream, tracking, and fresh live remote heads are equal with 0/0 divergence and a clean lane. Later validation remains owner-scoped and same-owner. One successful canonical completion must never be replayed.

## Scientific and terminal boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Fibre-network surrogates or drainage-and-formation tensors establish no likelihood, constraint, force, prediction, material law, empirical confirmation, ultraviolet completion, final physics, Theory of Everything, proof, or canon. THOS remains represented without governed blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance.

No successor may be contacted during execution. Elaren Kestrel v665-v8 is a prospective label only. A later send is permitted only after exact-final validation, a clean pushed fresh-live-equal final, a fresh live roster and authorization reread, unique exact-title resolution, and all protected route gates. Opaque acknowledgement must never trigger a resend merely for clarity.
"""
    write_text("x1/integrated-overview.md", overview)

    write_json(
        "x1/x1-build-receipt.json",
        {
            "schema": "ghc.family.eiren-kestrel.v665-v7.x1-build-receipt.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_eiren_kestrel_v665_v7_x1.py",
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
        raise SystemExit("usage: build_ghc_family_eiren_kestrel_v665_v7_x1.py [--staged-review]")
    else:
        main()
