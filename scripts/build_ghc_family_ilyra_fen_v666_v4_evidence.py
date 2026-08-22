#!/usr/bin/env python3
"""Build and exact-stage-review the immutable Ilyra Fen v666-v4 evidence candidate."""

from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_ilyra_fen_v666_v4_runtime import PHASE_ROOT, ROOT, X1_SHA, load_json, replay_manifest


NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
OUTCOMES = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def scalar(command: list[str]) -> str:
    return subprocess.check_output(command, cwd=ROOT, text=True, encoding="utf-8").strip()


def build() -> None:
    x1_replay = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
    proposal = load_json(PHASE_ROOT / "x2" / "proposal-ledger.json")
    smoke = load_json(PHASE_ROOT / "x2" / "tooling-smoke-receipt.json")
    portfolio = load_json(PHASE_ROOT / "x2" / "portfolio-execution.json")
    x2_flow = load_json(PHASE_ROOT / "method-flow" / "x2-method-flow.json")
    operations = load_json(PHASE_ROOT / "method-flow" / "x2-operational-overlay.json")
    deck_validation = json.loads(subprocess.check_output(
        [sys.executable, "-X", "utf8", str(ROOT / "scripts" / "ghc_family_ilyra_fen_v666_v4_flashcards.py"), "validate"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    ))
    if not x1_replay["valid"]:
        raise RuntimeError("immutable x1 manifest replay failed")
    if proposal["outcome_counts"] != OUTCOMES:
        raise RuntimeError("outcome counts drifted")
    if smoke["passed_count"] != 10 or smoke["canonical_aggregate_invoked"]:
        raise RuntimeError("tooling smoke state invalid")
    if x2_flow["new_method_count"] != 215 or x2_flow["new_negative_count"] != 100:
        raise RuntimeError("x2 Method Flow counts drifted")
    if operations["new_negative_count"] != 10 or operations["new_method_count"] != 10:
        raise RuntimeError("x2 operational overlay drifted")
    if not deck_validation["valid"]:
        raise RuntimeError("phase-local flashcard deck invalid")

    write_json("evidence/environment-version-receipt.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.environment-version-receipt.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "python": platform.python_version(), "python_implementation": platform.python_implementation(),
        "operating_system": platform.system(), "operating_system_release": platform.release(),
        "machine": platform.machine(), "git": scalar(["git", "--version"]),
        "node": scalar(["node", "--version"]), "codex_cli": scalar(["codex.cmd", "--version"]),
        "versions_verified_only": True, "software_updated": False, "elevation_used": False,
        "host_security_changed": False, "unrelated_software_installed": False, "rebooted": False,
        "private_absolute_paths_recorded": False, "environment_equivalence_claim": False,
        "independent_reproduction_claim": False,
    })
    write_json("evidence/source-use-ledger.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.source-use-ledger.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "reviewed_at_date": "2026-08-23", "network_calls_by_phase_software": 0,
        "real_data_rows": 0, "citations_are_not_observations": True,
        "sources": [
            {"authority": "NASA", "title": "NASA Procedural Requirements 7100.5", "url": "https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7100_0005_&page_name=main", "use": "curation responsibilities and procedural-boundary review"},
            {"authority": "NASA", "title": "JSC Astromaterials Curation and Research", "url": "https://www.nasa.gov/reference/jsc-astromaterials-curation-research/", "use": "official curation-program context"},
            {"authority": "NASA NTRS", "title": "Advanced Curation of Astromaterials", "url": "https://ntrs.nasa.gov/citations/20205005635", "use": "primary technical curation context"},
            {"authority": "NASA", "title": "Planetary Protection", "url": "https://sma.nasa.gov/sma-disciplines/planetary-protection", "use": "reserved planetary-protection authority boundary"},
            {"authority": "W3C", "title": "PROV-O", "url": "https://www.w3.org/TR/prov-o/", "use": "provenance vocabulary obligations"},
            {"authority": "IETF", "title": "RFC 8785 JSON Canonicalization Scheme", "url": "https://www.rfc-editor.org/rfc/rfc8785.html", "use": "deterministic JSON representation comparison"},
            {"authority": "IETF", "title": "RFC 8493 The BagIt File Packaging Format", "url": "https://www.rfc-editor.org/info/rfc8493/", "use": "content inventory and package-boundary comparison"},
            {"authority": "NIST", "title": "Metrological Traceability", "url": "https://www.nist.gov/metrology/metrological-traceability", "use": "traceability and uncertainty reservation"},
            {"authority": "W3C", "title": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "use": "structural accessible-report obligations"}
        ],
        "claim_boundary": "Current public sources informed synthetic schema design only. They do not establish ingestion, calibration, professional competence, legal or cultural authority, Maori authority, or empirical findings."
    })
    write_json("evidence/portfolio-evidence-receipt.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.portfolio-evidence-receipt.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "executed_owner_safe_now": 30, "represented_owner_candidates": 15,
        "built_tested_used_phase_local_skills": 10, "built_smoke_tested_family_current_runners": 10,
        "completed_owner_clean_fix_refine": 30, "prepared_successor_safe_now": 20,
        "prepared_successor_candidates": 15, "prepared_successor_skills": 10,
        "prepared_successor_runners": 10, "prepared_successor_clean_fix_refine": 30,
        "exact_approval_packets_unexecuted": 10, "blocked_packets_unexecuted": 5,
        "owner_method_count": portfolio["method_count"], "external_actions": 0,
        "protected_items_executed": 0,
        "claim_boundary": "bounded owner-local execution and successor preparation only; no external approval or authority"
    })
    write_json("evidence/authority-and-evidence-gaps.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.authority-and-evidence-gaps.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "inherited_open_gaps": 185, "new_open_gaps": 1, "effective_open_gaps": 186,
        "inherited_exact_gates": 183, "new_exact_gates": 1, "effective_exact_gates": 184,
        "new_open_gap_rows": [{"gap_id": "ILY6664-GAP-186", "proposal_id": "ILY6664-N019", "status": "open_gap", "missing": ["authorized live catalog interaction", "real astromaterials rows", "independent schema-owner review", "external interoperability evidence"], "network_calls": 0, "real_rows": 0, "completion_credit": 0}],
        "new_exact_gate_rows": [{"gate_id": "ILY6664-GATE-184", "proposal_id": "ILY6664-N020", "status": "exact_gate", "reserved_for": ["sample allocation or release", "planetary-protection decision", "legal or cultural decision", "repatriation or remedy", "affected-party authorization", "Maori authority"], "executed": False, "completion_credit": 0}],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20"
    })
    write_json("evidence/threat-model-review.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.threat-model-review.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "reviewed_threat_count": 12,
        "retained_phase_failures": 18,
        "new_threats_observed": [
            {"threat": "historical tool schema drift", "status": "mitigated_bounded", "retained_failure_count": 3, "residual": "inspect exact consumer inputs before use"},
            {"threat": "filesystem order substituted for declared semantic order", "status": "mitigated_bounded", "retained_failure_count": 1, "residual": "load by canonical index"},
            {"threat": "destructive cleanup pressure after a failed generation", "status": "mitigated_bounded", "retained_failure_count": 1, "residual": "preserve owner-local failure artifacts additively"}
        ],
        "unmitigated_external_domains": ["real samples and catalog evidence", "professional curation review", "affected-user accessibility evaluation", "privacy-complete review", "independent security review", "legal and cultural review", "Maori authority", "independent reproduction"],
        "exhaustive_security_claim": False, "privacy_complete_claim": False, "accessibility_complete_claim": False
    })
    write_json("evidence/wellbeing-workload-check.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.wellbeing-workload-check.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "status": "bounded_and_careful",
        "observations": ["x1 froze and became four-way equal before x2", "failed tooling and validation attempts remain visible", "no unsafe or external work was manufactured to satisfy counts", "work stayed in one owner-local sparse lane", "Hamish may rename, pause, redirect, or stop the route"],
        "personhood_or_emotion_claim": False, "workload_is_evidence_of_consciousness": False
    })
    write_json("evidence/flashcard-evidence-receipt.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.flashcard-evidence-receipt.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "builder": "scripts/ghc_family_ilyra_fen_v666_v4_flashcards.py",
        "validation": deck_validation, "legacy_partial_preserved": True,
        "legacy_tool_completion_credit": 0, "phase_local_deck_credit": "bounded_same_owner_structural_only",
        "identity_or_authority_claim": False
    })
    write_json("evidence/family-index-update.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.family-index-update.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "new_family_current_runners": 10, "new_phase_local_skills": 10,
        "historical_aliases_removed": 0, "shared_skill_files_modified": 0,
        "compatibility_surfaces_preserved": True,
        "recommended_tools": ["ghc_family_ilyra_fen_v666_v4_contracts.py", "ghc_family_ilyra_fen_v666_v4_manifests.py", "ghc_family_ilyra_fen_v666_v4_privacy.py", "ghc_family_ilyra_fen_v666_v4_flashcards.py"],
        "claim_boundary": "phase-scoped discovery update only; not a global install or universal endorsement"
    })
    write_json("evidence/method-flow-recommendations.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.method-flow-recommendations.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "preferred_methods": [
            {"trigger": "historical family tool on current phase", "method": "inspect exact input paths and keys before first invocation", "bounded_passing_witness": "phase-local current-schema deck validates"},
            {"trigger": "semantic ordering contract", "method": "read the canonical order index rather than filesystem lexical order", "bounded_passing_witness": "25-card graph validates"},
            {"trigger": "failed generated tree blocks canonical path", "method": "move the verified owner-generated tree into retained failures", "bounded_passing_witness": "258 files preserved and canonical path restored without deletion"},
            {"trigger": "Windows shell patterns contain brackets or quotes", "method": "use one bounded literal expression per probe", "bounded_passing_witness": "exact key accesses recovered"}
        ],
        "failed_witness_count": 18, "bounded_passing_witness_count": 18,
        "no_failure_erased": True, "universal_applicability_claim": False
    })
    write_json("evidence/reflection-remaster-receipt.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.reflection-remaster-receipt.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "reflected_surfaces": ["inherited flashcard builder", "privacy scanner", "manifest replay", "family-current runner wrappers", "Method Flow ledgers"],
        "remastered": ["current-schema phase-local four-tier flashcard builder", "semantic-order validator", "additive retained-failure relocation"],
        "deactivated_or_deleted": [], "shared_surfaces_mutated": [],
        "reason": "historical compatibility remained evidence; current-schema mismatches required a bounded additive implementation"
    })
    write_json("evidence/meta-toolbox-receipt.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.meta-toolbox-receipt.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "selected_phase_tools": 20, "runner_count": 10, "skill_count": 10,
        "globally_installed": 0, "smoke_used": 20,
        "selection_basis": ["current schema", "bounded fixture", "explicit failure mode", "family-current naming", "no external action"],
        "claim_boundary": "owner-phase toolbox receipt only; no production assurance or global installation claim"
    })
    write_json("evidence/evidence-summary.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.evidence-summary.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "x1_sha": X1_SHA, "x1_manifest_entries_replayed": x1_replay["entry_count"], "x1_manifest_failures": x1_replay["failure_count"],
        "proposal_chain_inherited": 4230, "proposal_count": 20, "proposal_chain_frozen_total": 4250,
        "outcome_counts": proposal["outcome_counts"], "positive_fixture_valid_count": 20,
        "synthetic_mutation_count": 100, "synthetic_mutation_rejected_count": 100,
        "x2_method_count": 215, "startup_failure_count": 8, "x2_operational_failure_count": 10,
        "effective_negatives": 26516, "effective_methods": 11173, "open_gaps": 186, "exact_gates": 184,
        "runner_smoke_passed": smoke["passed_count"], "skill_smoke_passed": smoke["skill_passed_count"],
        "canonical_aggregate_invoked": False, "real_data_rows": 0,
        "network_calls_by_phase_software": 0, "external_actions": 0,
        "complete_repository_suite_run": False, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20"
    })
    write_json("evidence/complete-incomplete-checklist.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.evidence-checklist.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "completed": ["strict x1-before-x2 gate", "twenty bounded proposal fixtures", "one hundred retained rejecting mutations", "exact 14/4/1/1 outcomes", "ten phase-local skills", "ten family-current runner interfaces", "owner and successor portfolio accounting", "phase-local four-tier flashcard deck", "ten x2 operational failures retained"],
        "incomplete": ["evidence commit, push, and four-way equality", "closeout, seal, and exact final", "one exact-final canonical attempt", "fresh terminal route reread and any one authorized delivery", "every external, empirical, professional, legal, cultural, Maori-authority, and independent-reproduction gate"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20"
    })
    write_json("evidence/evidence-build-receipt.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.evidence-build-receipt.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "builder": "scripts/build_ghc_family_ilyra_fen_v666_v4_evidence.py",
        "x1_manifest_replay": x1_replay, "x2_tooling_smoke_valid": smoke["valid"],
        "flashcard_deck_valid": deck_validation["valid"],
        "effective_negatives": 26516, "effective_methods": 11173,
        "open_gaps": 186, "exact_gates": 184,
        "canonical_aggregate_invoked": False, "closeout_paths_created": False,
        "status": "EVIDENCE_CONTENT_BUILT_AWAITING_STAGED_REVIEW_COMMIT_PUSH_EQUALITY"
    })
    write_json("method-flow/evidence-operational-overlay.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.method-flow-evidence-operational-overlay.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "generated_at_utc": NOW,
        "starting_effective_negatives": 26516, "starting_effective_methods": 11173,
        "new_negative_count": 0, "new_method_count": 0,
        "effective_after_evidence_negatives": 26516, "effective_after_evidence_methods": 11173,
        "rows": [], "no_failure_erased": True
    })
    print(json.dumps({"x1_manifest_entries": x1_replay["entry_count"], "outcomes": proposal["outcome_counts"], "mutations": 100, "deck_cards": deck_validation["card_count"], "effective_negatives": 26516, "effective_methods": 11173}, sort_keys=True))


def staged_rows() -> list[tuple[str, str]]:
    raw = subprocess.check_output(["git", "-C", str(ROOT), "diff", "--cached", "--name-status", "--no-renames"]).decode("utf-8")
    return [(line.split("\t", 1)[0], line.split("\t", 1)[1].replace("\\", "/")) for line in raw.splitlines() if line]


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f":{path}"])


def staged_review() -> None:
    review_path = "docs/ilyra-fen/v666-v4/validation/evidence-staged-review.json"
    manifest_path = "docs/ilyra-fen/v666-v4/validation/evidence-content-manifest.json"
    allowed_scripts = {path.relative_to(ROOT).as_posix() for path in (ROOT / "scripts").glob("*ilyra_fen_v666_v4*.py")}
    allowed_tests = {"tests/test_ghc_family_ilyra_fen_v666_v4_x2.py", "tests/test_ghc_family_ilyra_fen_v666_v4_evidence.py"}
    rows = [(status, path) for status, path in staged_rows() if path not in {review_path, manifest_path}]
    paths = [path for _, path in rows]
    if not rows:
        raise RuntimeError("no staged evidence content")
    invalid = [path for path in paths if not path.startswith("docs/ilyra-fen/v666-v4/") and path not in allowed_scripts and path not in allowed_tests]
    forbidden_lifecycle = [path for path in paths if any(path.startswith(f"docs/ilyra-fen/v666-v4/{part}/") for part in ("closeout", "seal", "final", "handoffs", "orchestration"))]
    changed_x1 = [path for path in paths if path.startswith("docs/ilyra-fen/v666-v4/x1/") or path in {"scripts/build_ghc_family_ilyra_fen_v666_v4_x1.py", "tests/test_ghc_family_ilyra_fen_v666_v4_x1.py"}]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
        "session_identifier_value": re.compile(r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_callable_identifier_value": re.compile(r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
    }
    parsed, candidates, maximum_words, maximum_path = 0, [], 0, ""
    for path in paths:
        blob = index_blob(path)
        text = blob.decode("utf-8")
        if "\r" in text:
            raise RuntimeError(f"non-LF staged text: {path}")
        words = len(re.findall(r"\S+", text))
        if words > maximum_words:
            maximum_words, maximum_path = words, path
        if path.endswith(".json"):
            json.loads(text)
            parsed += 1
        for class_name, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": class_name})
    x1_replay = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
    proposal = json.loads(index_blob("docs/ilyra-fen/v666-v4/x2/proposal-ledger.json"))
    flow = json.loads(index_blob("docs/ilyra-fen/v666-v4/method-flow/x2-method-flow.json"))
    operations = json.loads(index_blob("docs/ilyra-fen/v666-v4/method-flow/x2-operational-overlay.json"))
    smoke = json.loads(index_blob("docs/ilyra-fen/v666-v4/x2/tooling-smoke-receipt.json"))
    deck = json.loads(subprocess.check_output([sys.executable, "-X", "utf8", str(ROOT / "scripts" / "ghc_family_ilyra_fen_v666_v4_flashcards.py"), "validate"], cwd=ROOT, text=True, encoding="utf-8"))
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "owner_allowlist": not invalid,
        "closeout_final_paths_absent": not forbidden_lifecycle,
        "x1_paths_unchanged": not changed_x1 and x1_replay["valid"],
        "owner_file_cap": len(paths) <= 2000,
        "all_json_parse": True,
        "utf8_lf": True,
        "five_class_scan_zero_confirmed_hits": not candidates,
        "document_word_cap": maximum_words <= 100000,
        "proposal_outcomes_exact": proposal["outcome_counts"] == OUTCOMES,
        "x2_method_count_exact": flow["new_method_count"] == 215 and len(flow["rows"]) == 215,
        "all_100_mutations_retained": flow["new_negative_count"] == 100 and flow["failed_witness_count"] == 100,
        "ten_operational_failures_retained": operations["new_negative_count"] == 10 and len(operations["rows"]) == 10,
        "ten_runner_smoke_passed": smoke["passed_count"] == 10 and not smoke["canonical_aggregate_invoked"],
        "phase_local_flashcards_valid": deck["valid"] and deck["card_count"] == 25,
    }
    review = {
        "schema": "ghc.family.ilyra-fen.v666-v4.evidence-staged-review.v1",
        "owner": "Ilyra Fen", "phase": "v666-v4", "lifecycle": "evidence", "generated_at_utc": NOW,
        "reviewed_from": "git_index_blobs", "reviewed_paths": paths, "reviewed_path_count": len(paths),
        "json_parsed": parsed, "maximum_document_words": maximum_words, "maximum_document_path": maximum_path,
        "privacy_scan_classes": list(patterns), "privacy_candidates": len(candidates), "privacy_confirmed_hits": len(candidates),
        "privacy_candidate_rows": candidates, "checks": checks, "self_exclusions": [review_path, manifest_path],
        "claim_boundary": "exact staged same-owner evidence review only; not full repository suite, exhaustive security, privacy-complete, accessibility-complete, or independent reproduction",
        "valid": all(checks.values())
    }
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write_json("validation/evidence-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", review_path])
    entries = []
    for status, path in [(status, path) for status, path in staged_rows() if path != manifest_path]:
        line = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "--stage", "--", path]).decode("utf-8").strip()
        mode, oid, stage_path = line.split(" ", 2)
        stage, listed = stage_path.split("\t", 1)
        if stage != "0" or listed.replace("\\", "/") != path:
            raise RuntimeError(f"unexpected index stage for {path}")
        blob = index_blob(path)
        entries.append({"path": path, "git_mode": mode, "git_blob_oid": oid, "sha256": hashlib.sha256(blob).hexdigest(), "size_bytes": len(blob), "status": status})
    write_json("validation/evidence-content-manifest.json", {
        "schema": "ghc.family.ilyra-fen.v666-v4.content-manifest.v1",
        "owner": "Ilyra Fen", "phase": "evidence", "phase_label": "v666-v4", "generated_at_utc": NOW,
        "x1_sha": X1_SHA, "hash_source": "actual_git_index_blobs", "entries": entries,
        "entry_count": len(entries), "deletion_count": sum(status == "D" for status, _ in rows),
        "additive_only": all(status == "A" for status, _ in rows), "self_exclusion": manifest_path
    })
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", manifest_path])
    print(json.dumps({"reviewed": len(paths), "manifest_entries": len(entries), "json": parsed, "valid": True}, sort_keys=True))


if __name__ == "__main__":
    if not sys.argv[1:]:
        build()
    elif sys.argv[1:] == ["--staged-review"]:
        staged_review()
    else:
        raise SystemExit("usage: build_ghc_family_ilyra_fen_v666_v4_evidence.py [--staged-review]")
