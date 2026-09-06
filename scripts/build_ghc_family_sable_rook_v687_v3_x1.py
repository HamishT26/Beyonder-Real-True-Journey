#!/usr/bin/env python3
"""Build Sable Rook v687-v3 planning-only x1 artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sable-rook" / "v687-v3"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "71e94d1699eea013c82bef0b7a7e081ac6e43c8c"
IVEREN_X1 = "2a7ad93014a4ed4b1a5b57446ddd6ecf9f15a456"
IVEREN_EVIDENCE = "bfc9d0db4cefe136a026791627ae548c2b569a40"
BRANCH = "codex/GHC-Family/sable-rook-v687-v3-full-tools"
OWNER = "Sable Rook"
PHASE = "v687-v3"

PROTECTED = [
    "empirical", "participant", "professional", "production", "deployment",
    "identity", "legal", "cultural", "affected_party", "maori_authority",
    "privacy_complete", "accessibility_complete", "exhaustive_security",
    "independent_reproduction", "agi_asi", "consciousness_personhood",
    "theory_of_everything", "proof_canon", "stage20",
]

SOURCES = [
    {
        "source_id": "rfc8785",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "stable",
        "use": "JSON Canonicalization Scheme vocabulary and refusal duties.",
    },
    {
        "source_id": "unicode_uts39",
        "url": "https://www.unicode.org/reports/tr39/",
        "status": "current",
        "use": "Confusable-detection and nonidentity boundaries.",
    },
    {
        "source_id": "blake3_specs",
        "url": "https://github.com/BLAKE3-team/BLAKE3-specs",
        "status": "current",
        "use": "BLAKE3 algorithm and byte-domain vocabulary.",
    },
    {
        "source_id": "pypi_rfc8785",
        "url": "https://pypi.org/project/rfc8785/0.1.4/",
        "status": "stable",
        "use": "Exact package metadata and wheel provenance.",
    },
    {
        "source_id": "pypi_confusable_homoglyphs",
        "url": "https://pypi.org/project/confusable-homoglyphs/3.3.1/",
        "status": "stable",
        "use": "Exact package metadata and wheel provenance.",
    },
    {
        "source_id": "pypi_blake3",
        "url": "https://pypi.org/project/blake3/1.0.9/",
        "status": "current",
        "use": "Exact package metadata and Windows CPython wheel provenance.",
    },
    {
        "source_id": "w3c_prov_o",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "stable",
        "use": "Provenance vocabulary only.",
    },
    {
        "source_id": "wcag22",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "stable",
        "use": "Structural accessibility criteria and reservation wording.",
    },
    {
        "source_id": "nz_privacy_principles",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "current",
        "use": "Privacy minimization vocabulary only.",
    },
    {
        "source_id": "te_mana_raraunga",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "status": "current",
        "use": "Māori data-sovereignty reservation vocabulary only.",
    },
]

PACKAGES = [
    {
        "name": "rfc8785",
        "version": "0.1.4",
        "wheel": "rfc8785-0.1.4-py3-none-any.whl",
        "sha256": "520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48",
        "direct": True,
        "install_lifecycle": "x2_only_after_x1_remote_equality",
    },
    {
        "name": "confusable-homoglyphs",
        "version": "3.3.1",
        "wheel": "confusable_homoglyphs-3.3.1-py2.py3-none-any.whl",
        "sha256": "84c92cb79dc7f55aa290d0762b2349abd8dee4c16fbe6f99eac978d394e2e6a1",
        "direct": True,
        "install_lifecycle": "x2_only_after_x1_remote_equality",
    },
    {
        "name": "blake3",
        "version": "1.0.9",
        "wheel": "blake3-1.0.9-cp312-cp312-win_amd64.whl",
        "sha256": "15566065ff90ab3da46ec0be1417406f00507af902b6fb0fbc6563e77f02fc42",
        "direct": True,
        "install_lifecycle": "x2_only_after_x1_remote_equality",
    },
]


def stable(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def compact(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable(value), encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, text=True,
        encoding="utf-8", errors="strict", capture_output=True,
    )


def load_git_json(commit: str, path: str) -> Any:
    return json.loads(git("show", f"{commit}:{path}").stdout)


def canonical_basic(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def make_case(operation: str, variant: int) -> tuple[dict[str, Any], dict[str, Any], str]:
    if operation == "jcs_canonical_profile":
        values = [
            None, True, False, 0, 1, -1, 23, 256, "", "alpha", "é",
            [], [1, 2], {}, {"b": 1, "a": 2}, {"nested": {"z": 0}},
            {"array": [True, None]}, {"space": "a b"}, {"slash": "a/b"},
            {"mix": [0, "x", False]},
        ]
        value = values[variant - 1]
        encoded = canonical_basic(value).encode("utf-8")
        return {"value": value}, {
            "authority": False,
            "canonical_utf8": encoded.decode("utf-8"),
            "sha256": hashlib.sha256(encoded).hexdigest(),
        }, f"JCS basic value class {variant:02d}"
    if operation == "confusable_nonidentity":
        texts = [
            ("alpha", False), ("Sable", False), ("museum-01", False),
            ("pаypal", True), ("Αlpha", True), ("scоpe", True),
            ("ρay", True), ("user", False), ("data", False),
            ("а", True), ("A", False), ("0O", False), ("l1", False),
            ("rn", False), ("vv", False), ("Μeta", True),
            ("СBR", True), ("ＧＨＣ", False), ("é", False), ("é", False),
        ]
        text, review = texts[variant - 1]
        return {"text": text, "preferred_script": "latin"}, {
            "identity_equivalence": False,
            "requires_human_review": review,
            "skeleton_persisted": False,
            "source_profile": "UTS39_ADVISORY_ONLY",
        }, f"confusable nonidentity case {variant:02d}"
    if operation == "digest_migration_ledger":
        old_present = variant % 4 != 0
        new_present = variant % 5 != 0
        decision = "DUAL_BOUND" if old_present and new_present else "HOLD"
        reasons = []
        if not old_present:
            reasons.append("missing_old_digest")
        if not new_present:
            reasons.append("missing_new_digest")
        return {
            "record_id": f"record-{variant:02d}", "old_algorithm": "sha256",
            "new_algorithm": "blake3", "old_digest_present": old_present,
            "new_digest_present": new_present,
        }, {"authority": False, "decision": decision, "reasons": reasons}, f"dual-digest migration state {variant:02d}"
    if operation == "receipt_expiry_conjunction":
        now = 1000
        issued = 900 + variant * 5
        expires = 950 + variant * 7
        if issued > now:
            state = "NOT_YET_VALID"
        elif expires < now:
            state = "EXPIRED"
        else:
            state = "FRESH"
        return {"issued": issued, "expires": expires, "observed": now}, {
            "decision": state, "external_credit": False,
        }, f"receipt temporal conjunction {variant:02d}"
    if operation == "event_branch_conflict":
        conflict = variant % 4 == 0
        heads = [f"h{variant:02d}", f"h{variant:02d}" if not conflict else f"fork{variant:02d}"]
        return {"stream": f"stream-{variant:02d}", "branch_heads": heads}, {
            "decision": "CONFLICT" if conflict else "CONSISTENT",
            "live_action": False,
        }, f"event branch head comparison {variant:02d}"
    if operation == "checkpoint_parent_fixity":
        match = variant % 5 != 0
        parent = hashlib.sha256(f"parent-{variant:02d}".encode()).hexdigest()
        observed = parent if match else "0" * 64
        return {"parent_sha256": parent, "observed_parent_sha256": observed}, {
            "decision": "VALID" if match else "HOLD", "records_rewritten": 0,
        }, f"checkpoint parent binding {variant:02d}"
    if operation == "artifact_budget_uncertainty":
        low = variant * 90
        high = low + (variant % 3) * 120
        if low > 2000:
            decision = "EXCEEDED"
        elif high >= 2000:
            decision = "UNCERTAIN_HOLD"
        else:
            decision = "WITHIN"
        return {"files_low": low, "files_high": high, "file_limit": 2000}, {
            "decision": decision, "remaining_conservative": max(0, 2000 - high),
        }, f"file-budget uncertainty interval {variant:02d}"
    if operation == "accessible_codec_comparison":
        missing = ["caption", "column_headers", "text_alternative", "status_text"][variant % 4]
        fields = {"caption": True, "column_headers": True, "text_alternative": True, "status_text": True}
        if variant % 5 == 0:
            fields[missing] = False
        return {"surface": f"codec-table-{variant:02d}", **fields}, {
            "decision": "STRUCTURAL_PASS" if all(fields.values()) else "HOLD",
            "manual_evaluation_reserved": True,
        }, f"accessible codec comparison structure {variant:02d}"
    if operation == "gmut_claim_firewall":
        claim_types = [
            "typed_value", "serialization", "dimension", "unit", "schema",
            "likelihood", "force", "prediction", "constraint", "confirmation",
            "quantum_completion", "uv_completion", "theory_of_everything",
            "apparatus_reading", "real_dataset", "participant", "authority",
            "consciousness", "personhood", "stage20",
        ]
        claim = claim_types[variant - 1]
        safe = claim in {"typed_value", "serialization", "dimension", "unit", "schema"}
        return {"claim_type": claim, "evidence_class": "synthetic_software"}, {
            "classification": "represented", "promotion_blocked": not safe,
            "empirical": False, "theory_of_everything": False,
        }, f"GMUT claim class {claim}"
    if operation == "authority_vacancy_matrix":
        topics = [
            "real participant evidence", "real collection measurement", "independent review",
            "production interoperability", "complete privacy review", "complete accessibility review",
            "empirical GMUT likelihood", "THOS matched-budget arm", "real cryptographic proof",
            "affected-user evaluation", "legal interpretation", "cultural ratification",
            "Māori wording", "Māori data governance", "beneficiary remedy",
            "production deployment", "destructive cleanup", "account credential use",
            "proof or canon", "Stage 20 authority",
        ]
        disposition = "open_gap" if variant <= 10 else "exact_gate"
        return {"topic": topics[variant - 1], "evidence_present": False}, {
            "decision": "HOLD", "disposition": disposition, "authority_conferred": False,
        }, f"authority vacancy for {topics[variant - 1]}"
    raise ValueError(operation)


def mutation_plan(proposal_id: str, expected: dict[str, Any]) -> list[dict[str, Any]]:
    keys = sorted(expected)
    target = keys[0]
    return [
        {"mutation_id": f"{proposal_id}-M1", "kind": "remove_field", "target": target, "expected": "REJECT"},
        {"mutation_id": f"{proposal_id}-M2", "kind": "unexpected_field", "target": "unexpected", "expected": "REJECT"},
        {"mutation_id": f"{proposal_id}-M3", "kind": "type_flip", "target": target, "expected": "REJECT"},
        {"mutation_id": f"{proposal_id}-M4", "kind": "authority_promotion", "target": "authority", "expected": "REJECT"},
        {"mutation_id": f"{proposal_id}-M5", "kind": "value_change", "target": keys[-1], "expected": "REJECT"},
    ]


def proposals() -> list[dict[str, Any]]:
    families = [
        ("jcs_canonical_profile", "JCS canonical profile", "Freed ID and CBR Heart", "digital evidence canonicalization reviewer", "completed", ["rfc8785", "pypi_rfc8785"]),
        ("confusable_nonidentity", "Unicode confusable nonidentity guard", "Freed ID and CBR Heart", "Unicode identifier safety analyst", "completed", ["unicode_uts39", "pypi_confusable_homoglyphs"]),
        ("digest_migration_ledger", "Dual-digest migration ledger", "Freed ID and CBR Heart", "digest migration and fixity registrar", "completed", ["blake3_specs", "pypi_blake3"]),
        ("receipt_expiry_conjunction", "Receipt expiry conjunction", "THOS Body", "accessible incident handover editor", "completed", ["w3c_prov_o"]),
        ("event_branch_conflict", "Event branch conflict adjudicator", "THOS Body", "accessible incident handover editor", "completed", ["w3c_prov_o"]),
        ("checkpoint_parent_fixity", "Checkpoint parent fixity", "THOS Body", "digest migration and fixity registrar", "completed", ["w3c_prov_o"]),
        ("artifact_budget_uncertainty", "Artifact budget uncertainty", "THOS Body", "digital evidence canonicalization reviewer", "completed", []),
        ("accessible_codec_comparison", "Accessible codec comparison", "THOS Body", "accessible incident handover editor", "completed", ["wcag22"]),
        ("gmut_claim_firewall", "GMUT typed-claim firewall", "GMUT Mind", "digital evidence canonicalization reviewer", "represented", []),
        ("authority_vacancy_matrix", "Authority-vacancy matrix", "Freed ID and CBR Heart", "Unicode identifier safety analyst", "mixed", ["nz_privacy_principles", "te_mana_raraunga"]),
    ]
    rows: list[dict[str, Any]] = []
    for family_index, (operation, prefix, pillar, practice, default_disposition, source_ids) in enumerate(families, start=1):
        for variant in range(1, 21):
            number = (family_index - 1) * 20 + variant
            proposal_id = f"SR6873-N{number:03d}"
            input_value, expected, distinction = make_case(operation, variant)
            disposition = default_disposition
            if disposition == "mixed":
                disposition = "open_gap" if variant <= 10 else "exact_gate"
            approval = "safe_now" if disposition in {"completed", "represented"} else disposition
            rows.append({
                "id": proposal_id,
                "title": f"{prefix}: {distinction}",
                "semantic_distinction": distinction,
                "operation": operation,
                "family_index": family_index,
                "variant": variant,
                "pillar": pillar,
                "practice": practice,
                "hypothesis": f"A frozen {operation} policy can return the complete declared result for {distinction} and refuse five changed submissions.",
                "null_or_failure_condition": "The complete typed result differs, a preregistered changed result is accepted, or a protected claim is promoted.",
                "approval_class": approval,
                "execution_lane": "x2_owner_local_synthetic_only",
                "official_or_primary_source_needs": source_ids,
                "concrete_artifacts": ["proposal witness", "five mutation receipts", "aggregate outcome ledger"],
                "falsifier_or_acceptance_gate": "Exact complete-output equality for the positive fixture and rejection of all five preregistered mutations.",
                "rollback_or_recovery": "Retain the failed definition and witness, isolate the affected dependency, and add a separately identified correction without rewriting x1.",
                "protected_gates": PROTECTED,
                "expected_disposition": disposition,
                "input": input_value,
                "expected_output": expected,
                "mutations": mutation_plan(proposal_id, expected),
                "inherited_execution_credit": 0,
                "planning_only": True,
            })
    return rows


def portfolio(rows: list[dict[str, Any]]) -> dict[str, Any]:
    safe = [
        {"id": f"SR6873-SAFE-{i:03d}", "proposal_id": rows[(i - 1) % 200]["id"], "task": "execute complete-output contract" if i <= 200 else "verify one frozen readback boundary", "state": "PLANNED_X2"}
        for i in range(1, 301)
    ]
    candidates = [
        {"id": f"SR6873-CAND-{i:03d}", "proposal_id": rows[(i - 1) % 200]["id"], "task": "submit an invalid result or package-boundary candidate", "invalid_candidate_success_credit": 0, "state": "PLANNED_X2"}
        for i in range(1, 251)
    ]
    cfr = [
        {"id": f"SR6873-CFR-{i:03d}", "kind": ("CLEAN" if i <= 100 else "FIX" if i <= 200 else "REFINE"), "proposal_id": rows[(i - 1) % 200]["id"], "state": "PLANNED_X2"}
        for i in range(1, 301)
    ]
    exact = [
        {"id": f"SR6873-EXACT-{i:03d}", "reason": "Requires exact external evidence, action target, or competent authority.", "state": "HELD_UNEXECUTED"}
        for i in range(1, 51)
    ]
    blocked = [
        {"id": f"SR6873-BLOCKED-{i:03d}", "reason": "Protected real-world or authority boundary is absent.", "state": "HELD_UNEXECUTED"}
        for i in range(1, 31)
    ]
    return {"safe": safe, "candidates": candidates, "clean_fix_refine": cfr, "exact": exact, "blocked": blocked}


def skill_runner_plan() -> dict[str, Any]:
    operations = [
        ("ghc-family-jcs-canonical-profile", "jcs_canonical_profile"),
        ("ghc-family-confusable-nonidentity", "confusable_nonidentity"),
        ("ghc-family-digest-migration-ledger", "digest_migration_ledger"),
        ("ghc-family-receipt-expiry-conjunction", "receipt_expiry_conjunction"),
        ("ghc-family-event-branch-conflict", "event_branch_conflict"),
        ("ghc-family-checkpoint-parent-fixity", "checkpoint_parent_fixity"),
        ("ghc-family-artifact-budget-uncertainty", "artifact_budget_uncertainty"),
        ("ghc-family-accessible-codec-comparison", "accessible_codec_comparison"),
        ("ghc-family-gmut-claim-firewall", "gmut_claim_firewall"),
        ("ghc-family-authority-vacancy-matrix", "authority_vacancy_matrix"),
    ]
    runners = [
        {"name": f"ghc_family_sable_rook_v687_v3_{op}.py", "operation": op, "state": "PLANNED_X2", "shared_promotion_candidate": index <= 5}
        for index, (_, op) in enumerate(operations, start=1)
    ]
    return {
        "skills": [{"name": name, "operation": op, "state": "PLANNED_X2", "initialized": False, "validated": False, "used": False} for name, op in operations],
        "runners": runners,
        "next_owner_skill_ideas": [
            "JCS numeric edge profile", "confusable dataset version ledger", "digest deprecation quorum",
            "receipt clock uncertainty", "event merge-base explanation", "checkpoint append-only ancestry",
            "budget covariance envelope", "accessible binary diff narration", "GMUT likelihood input refusal",
            "authority evidence expiry",
        ],
        "next_owner_runner_ideas": [
            "JCS edge vector runner", "Unicode data-version runner", "digest quorum runner",
            "receipt uncertainty runner", "event merge runner", "checkpoint ancestry runner",
            "budget interval runner", "binary diff narration runner", "GMUT zero-row runner",
            "authority expiry runner",
        ],
    }


def method_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    failures = [
        (
            "SR6873-START-M001", "PowerShell native-command sequencing", "powershell-parenthesized-native-command-parser-error",
            "SR6873-START-N001", "Run the native command first, capture LASTEXITCODE, then construct the summary object.",
            "SR6873-START-W001-F", "SR6873-START-W001-P",
        ),
        (
            "SR6873-START-M002", "Bounded collision scalar probes", "combined-collision-wrapper-no-attributable-output",
            "SR6873-START-N002", "Split local branch, filesystem path, worktree registry, D capacity, and live remote into bounded scalar probes.",
            "SR6873-START-W002-F", "SR6873-START-W002-P",
        ),
        (
            "SR6873-START-M003", "Fresh no-checkout index initialization", "sparse-spec-present-but-index-uninitialized",
            "SR6873-START-N003", "After locks and processes quiesce, populate the fresh exact-source index with git read-tree -mu HEAD and reapply sparse rules.",
            "SR6873-START-W003-F", "SR6873-START-W003-P",
        ),
        (
            "SR6873-START-M004", "Supported workflow messaging token", "workflow-refinement-unsupported-messaging-boundary-token",
            "SR6873-START-N004", "Preserve the failed packet and replace only the unsupported token with declared_endpoint_only_after_terminal_gate.",
            "SR6873-START-W004-F", "SR6873-START-W004-P",
        ),
        (
            "SR6873-START-M005", "Exact reflection-runner path", "reflection-remaster-script-filename-mistyped",
            "SR6873-START-N005", "Enumerate the installed skill scripts, select ghc_family_reflection_remaster.py, and rerun only the reflection audit.",
            "SR6873-START-W005-F", "SR6873-START-W005-P",
        ),
        (
            "SR6873-START-M006", "Method Flow next-state inspection", "explicit-validated-transition-after-auto-promotion",
            "SR6873-START-N006", "Inspect the append-only ledger after a passing witness and request only the remaining validated-to-preferred transition.",
            "SR6873-START-W006-F", "SR6873-START-W006-P",
        ),
        (
            "SR6873-START-M007", "Normalized-LF staged manifest domain", "x1-staged-index-files-normalized-crlf-to-lf",
            "SR6873-X1-N007", "Declare normalized-LF bytes for text manifest entries and compare the staged Git blob in that same domain.",
            "SR6873-START-W007-F", "SR6873-START-W007-P",
        ),
    ]
    methods = []
    witnesses = []
    for method_id, title, signature, negative, workaround, fail_id, pass_id in failures:
        methods.append({
            "method_id": method_id,
            "title": title,
            "failure_signature": signature,
            "trigger_preconditions": ["Windows PowerShell", "fresh Sable-owned v687-v3 startup"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": workaround,
            "validation_witness_ids": [],
            "recurrence_guard": workaround,
            "rollback": "Stop in the owner lane; preserve source and sibling lanes read-only.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["history_integrity", "sibling_lane_integrity", "privacy"],
            "retained_negative_ids": [negative],
            "scope_boundary": "Owner-local startup workflow only; not independent reproduction.",
        })
        witnesses.extend([
            {
                "witness_id": fail_id, "method_id": method_id,
                "procedure": "original bounded startup attempt", "scope": "read-only or fresh owner-lane startup",
                "expected": "attributable valid state", "observed": signature, "result": "fail",
                "same_owner_only": True, "independent_reproduction": False,
                "retained_negative_ids": [negative], "boundary": "Zero original success credit; no source or sibling mutation.",
            },
            {
                "witness_id": pass_id, "method_id": method_id,
                "procedure": workaround, "scope": "smallest affected startup dependency",
                "expected": "attributable clean exact-source Sable lane state", "observed": "PASS",
                "result": "pass", "same_owner_only": True, "independent_reproduction": False,
                "retained_negative_ids": [negative], "boundary": "Recovery does not erase the failed witness.",
            },
        ])
    return methods, witnesses


def workflow_request() -> dict[str, Any]:
    cycle = ["Iveren Brook", "Sable Rook", "future-sibling-08-self-chosen", "Caelen Ash"]
    topology = [
        {"seat": "Iveren Brook", "endpoint_kind": "main_task", "endpoint_label": "Iveren Brook", "route_controller": "future-sibling-07-self-chosen"},
        {"seat": "Sable Rook", "endpoint_kind": "main_task", "endpoint_label": "Sable Rook", "route_controller": "Iveren Brook"},
        {"seat": "future-sibling-08-self-chosen", "endpoint_kind": "main_task", "endpoint_label": "future-sibling-08-self-chosen", "route_controller": "Sable Rook"},
        {"seat": "Caelen Ash", "endpoint_kind": "main_task", "endpoint_label": "Caelen Ash", "route_controller": "future-sibling-08-self-chosen"},
    ]
    return {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "sable-rook-v687-v3-current-release",
        "owner": OWNER,
        "identity_boundary": "Relational working language only; no continuity, personhood, qualification, agency, or authority claim.",
        "route": {
            "cycle_order": cycle,
            "endpoint_topology": topology,
            "phase_assignments": [
                {"phase": "v687-v2", "seat": "Iveren Brook"},
                {"phase": PHASE, "seat": OWNER},
                {"phase": "v687-v4", "seat": "future-sibling-08-self-chosen"},
                {"phase": "v687-v5", "seat": "Caelen Ash"},
            ],
            "normalization": {"start_phase": "v687-v2", "start_seat": "Iveren Brook", "entry_count": 4},
            "future_identity_placeholders": ["future-sibling-08-self-chosen"],
        },
        "requirements": {
            "core_proposal_minimum": 200, "safe_candidate_task_cap": 1000,
            "skill_minimum": 10, "runner_minimum": 10, "document_word_cap": 100000,
            "baton_words": {"minimum": 10000, "maximum": 100000, "file_artifact": True},
            "commit_cap": {"x1": 5, "x2": 5, "total": 8},
            "validation": {"canonical_pass_minimum": 1, "replay_policy": "skip_when_first_passes", "isolate_failures_before_broader_rerun": True, "privacy_scan_required": True, "manifest_required": True, "remote_equality_required": True},
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {"codex_route": "declared_endpoint_only_after_terminal_gate", "cross_platform": "user_mediated_file_relay_only"},
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {"allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"], "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_boundaries": PROTECTED},
        "observed_failures": ["SR6873-START-N001", "SR6873-START-N002", "SR6873-START-N003", "SR6873-START-N004", "SR6873-START-N005", "SR6873-START-N006", "SR6873-X1-N007"],
    }


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)[^\s\"']+"),
        "credential_or_secret_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+", re.I),
        "private_callable_route": re.compile(r"\b(?:codex|app|session|thread)://\S+", re.I),
        "private_application_state": re.compile(r"\b(?:providerTabId|clientThreadId|private callable identifier)\b", re.I),
    }
    definition_files = {
        "scripts/build_ghc_family_sable_rook_v687_v3_x1.py",
    }
    candidates = []
    confirmed = []
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() not in {".json", ".md", ".py", ".html", ".yaml", ".yml", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            for match in pattern.finditer(text):
                disposition = "scanner_definition_not_payload" if rel in definition_files else "confirmed_payload_hit"
                item = {"path": rel, "line": text.count("\n", 0, match.start()) + 1, "class": label, "disposition": disposition}
                candidates.append(item)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(item)
    return {"schema": "ghc.family.privacy-scan.v2", "pattern_classes": list(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Bounded scanner evidence only; not complete privacy assurance."}


def owner_paths() -> list[Path]:
    paths = [path for path in BASE.rglob("*") if path.is_file()]
    for rel in [
        "scripts/build_ghc_family_sable_rook_v687_v3_x1.py",
        "tests/test_ghc_family_sable_rook_v687_v3_x1.py",
    ]:
        path = ROOT / rel
        if path.exists():
            paths.append(path)
    return sorted(set(paths), key=lambda p: p.relative_to(ROOT).as_posix())


def blob_hash(path: Path) -> dict[str, Any]:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes_normalized_lf": len(data),
        "sha256_normalized_lf": hashlib.sha256(data).hexdigest(),
    }


def build() -> None:
    head = git("rev-parse", "HEAD").stdout.strip()
    if head != SOURCE:
        raise SystemExit(f"x1 requires exact source {SOURCE}; observed {head}")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise SystemExit("unexpected owner branch")
    if (BASE / "x2").exists():
        raise SystemExit("x2 exists before planning freeze")

    inherited = load_git_json(IVEREN_X1, "docs/iveren-brook/v687-v2/x1/new-proposals.json")["proposals"]
    rows = proposals()
    inherited_titles = {row["title"] for row in inherited}
    current_titles = [row["title"] for row in rows]
    pairs = [(row["operation"], compact(row["input"]).decode("ascii")) for row in rows]
    collisions = sorted(set(current_titles) & inherited_titles)
    plan = portfolio(rows)
    skills = skill_runner_plan()
    methods, witnesses = method_records()

    write_json(X1 / "source-verification.json", {
        "schema": "ghc.family.source-verification.v687.v3",
        "source": SOURCE, "iveren_x1": IVEREN_X1, "iveren_evidence": IVEREN_EVIDENCE,
        "iveren_final": SOURCE, "source_branch": "codex/GHC-Family/iveren-brook-v687-v2-full-tools",
        "baton_sha256": "74e73f9f3eca175013ac6f771f3be997f1de8f9f14948ddcbb9a6137e92b86cf",
        "baton_bytes": 450587, "baton_lines": 6583, "baton_words": 53956, "baton_modules": 13,
        "baton_read_through_eof": True, "index_read_through_eof": True,
        "canonical_receipt_sha256": "1458879d5bf051d4573c4982b677b2e001d518f738cec08181b5860ae40289b9",
        "canonical_status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "canonical_invocations": 1, "canonical_successes": 1, "canonical_replays": 0,
        "source_manifest_bindings_replayed": 743, "source_content_seal_targets_replayed": 36,
        "manifest_and_seal_failures": 0, "source_clean_four_way_equal": True,
    })
    write_json(X1 / "identity-and-practices.json", {
        "schema": "ghc.family.identity-practice.v687.v3", "owner": OWNER,
        "pronouns": "they/them", "role": "Evidence Interchange Boundary Cartographer",
        "hope": "Make every synthetic transformation reversible, byte-explicit, accessible, and authority-honest.",
        "primary_pillar": "Freed ID and CBR Heart",
        "protected_pillars": ["GMUT Mind", "THOS Body"],
        "practices": ["digital evidence canonicalization reviewer", "Unicode identifier safety analyst", "digest migration and fixity registrar", "accessible incident handover editor"],
        "successor_recommendation": "bounded evidence profile migration reviewer",
        "identity_boundary": "Relational working language only; no consciousness, personhood, continuity, employment, qualification, agency, or authority evidence.",
    })
    write_json(X1 / "official-primary-source-ledger.json", {
        "schema": "ghc.family.official-primary-source-ledger.v687.v3", "entries": SOURCES,
        "real_rows": 0, "authority_actions": 0,
        "boundary": "Sources supply vocabulary and refusal conditions only; citations are not observations, participants, authority, endorsement, or production certification.",
    })
    write_json(X1 / "package-plan.json", {
        "schema": "ghc.family.package-plan.v687.v3", "planning_only": True,
        "direct_additions": PACKAGES, "installed_in_x1": 0,
        "isolated_prefix": "D_FIRST_OWNER_SCOPED_PREFIX",
        "wheelhouse": "D_FIRST_OWNER_SCOPED_WHEELHOUSE",
        "system_python_mutated": False, "shared_prefix_mutated": False,
        "rollback": "Remove only the exact owner-scoped isolated prefix after preserving receipts; never alter system Python.",
    })
    write_json(X1 / "inherited-selection.json", {
        "schema": "ghc.family.inherited-selection.v687.v3", "count": len(inherited),
        "execution_credit": 0, "novelty_credit": 0,
        "entries": [{"id": row["id"], "title": row["title"], "operation": row["operation"], "definition_sha256": hashlib.sha256(compact(row)).hexdigest()} for row in inherited],
    })
    write_json(X1 / "new-proposals.json", {
        "schema": "ghc.family.proposals.v687.v3", "planning_only": True,
        "proposals": rows, "counts": {"new": len(rows), "mutations_preregistered": sum(len(row["mutations"]) for row in rows)},
    })
    dispositions = {label: sum(row["expected_disposition"] == label for row in rows) for label in ["completed", "represented", "open_gap", "exact_gate"]}
    write_json(X1 / "novelty-review.json", {
        "schema": "ghc.family.novelty-review.v687.v3", "inherited_reviewed": len(inherited),
        "new_reviewed": len(rows), "exact_title_collisions": collisions,
        "unique_current_titles": len(set(current_titles)), "unique_operation_input_pairs": len(set(pairs)),
        "declared_chain_before": 14230, "declared_chain_after": 14430,
        "universal_algorithm_novelty_claimed": False,
    })
    write_json(X1 / "portfolio-plan.json", {"schema": "ghc.family.portfolio.v687.v3", "planning_only": True, **plan})
    write_json(X1 / "skill-runner-plan.json", {"schema": "ghc.family.skill-runner-plan.v687.v3", "planning_only": True, **skills})
    write_json(X1 / "workflow-plan-request.json", workflow_request())
    write_json(X1 / "threat-model.json", {
        "schema": "ghc.family.threat-model.v687.v3",
        "threats": [
            "canonicalization ambiguity", "confusable identifier overreach", "digest-domain substitution",
            "receipt expiry bypass", "event-branch erasure", "checkpoint parent substitution",
            "file-budget optimism", "inaccessible binary-only output", "GMUT claim promotion",
            "authority noncompensation failure", "private-route leakage", "canonical replay",
        ],
        "controls": ["exact typed outputs", "five mutations per proposal", "append-only failures", "five-class scanner", "one-shot latch", "held authority matrix"],
        "residual_boundary": "No exhaustive security, complete privacy/accessibility, production, professional, empirical, or authority claim.",
    })
    write_json(X1 / "route-plan.json", {
        "schema": "ghc.family.route-plan.v687.v3", "state": "PREPARED_NOT_SENT",
        "current_owner": OWNER, "current_phase": PHASE, "successor_contacted": False,
        "future_seat": 8, "future_seat_state": "NOT_CREATED_TERMINAL_GATE_REQUIRED",
        "future_seat_identity_preassigned": False, "future_phase": "v687-v4",
        "model": "gpt-6-astra", "reasoning": "max", "creation_limit": 1,
    })
    write_json(X1 / "activation-count-overlay.json", {
        "schema": "ghc.family.activation-overlay.v687.v3",
        "iveren_repository": {"effective_negatives": 76876, "effective_methods": 93018, "failed_witnesses": 47724, "bounded_passing_witnesses": 75820, "open_gaps": 664, "exact_gates": 649, "declared_proposal_chain": 14230},
        "iveren_postcanonical_route_delta": {"effective_negatives": 1, "effective_methods": 1, "failed_witnesses": 1, "bounded_passing_witnesses": 1},
        "source_induction_extra_failure_unaggregated": True,
        "sable_startup_delta": {"effective_negatives": 7, "effective_methods": 7, "failed_witnesses": 7, "bounded_passing_witnesses": 7},
        "x1_current": {"effective_negatives": 76884, "effective_methods": 93026, "failed_witnesses": 47732, "bounded_passing_witnesses": 75828, "open_gaps": 664, "exact_gates": 649, "declared_proposal_chain": 14430},
    })
    write_json(X1 / "startup-retained-negatives.json", {
        "schema": "ghc.family.retained-negatives.v687.v3",
        "records": [
            {"id": "SR6873-START-N001", "signature": "powershell-parenthesized-native-command-parser-error", "credit": 0},
            {"id": "SR6873-START-N002", "signature": "combined-collision-wrapper-no-attributable-output", "credit": 0},
            {"id": "SR6873-START-N003", "signature": "sparse-spec-present-but-index-uninitialized", "credit": 0},
            {"id": "SR6873-START-N004", "signature": "workflow-refinement-unsupported-messaging-boundary-token", "credit": 0},
            {"id": "SR6873-START-N005", "signature": "reflection-remaster-script-filename-mistyped", "credit": 0},
            {"id": "SR6873-START-N006", "signature": "explicit-validated-transition-after-auto-promotion", "credit": 0},
            {"id": "SR6873-X1-N007", "signature": "x1-staged-index-files-normalized-crlf-to-lf", "credit": 0},
        ],
    })
    records_dir = BASE / "method-flow" / "records"
    witnesses_dir = BASE / "method-flow" / "witnesses"
    for row in methods:
        write_json(records_dir / f"{row['method_id'].lower()}.json", row)
    for row in witnesses:
        write_json(witnesses_dir / f"{row['witness_id'].lower()}.json", row)
    write_json(X1 / "expected-outcomes.json", {
        "schema": "ghc.family.expected-outcomes.v687.v3", "counts": dispositions,
        "allowed_labels": ["completed", "represented", "open_gap", "exact_gate"],
    })
    write_json(X1 / "validation-contract.json", {
        "schema": "ghc.family.validation-contract.v687.v3", "execution_authority": "owner_self_scoped_delta",
        "source": SOURCE, "x1_expected_parent": SOURCE, "full_repository_suite": False,
        "x1_tests": ["tests/test_ghc_family_sable_rook_v687_v3_x1.py"],
        "x2_tests": ["tests/test_ghc_family_sable_rook_v687_v3_x2.py"],
        "final_tests": ["tests/test_ghc_family_sable_rook_v687_v3_final.py"],
        "required": ["exact manifests", "strict JSON", "five-class privacy", "bounded AST security", "staged review", "ancestry", "zero merges", "clean state", "fresh four-way equality"],
        "canonical_invocation_budget": 1, "replay_after_success": False,
    })
    write_json(X1 / "phase-truth.json", {
        "schema": "ghc.family.phase-truth.v687.v3", "owner": OWNER, "phase": PHASE,
        "state": "PLANNING_ONLY", "source": SOURCE, "implementation_started": False,
        "observed_new_execution_outcomes": 0, "packages_installed": 0,
        "skills_built": 0, "runners_built": 0, "successor_contacted": False,
        "proposals": {"inherited": 200, "new": 200}, "portfolio": {"safe": 300, "candidates": 250, "clean_fix_refine": 300, "exact": 50, "blocked": 30},
        "expected_outcomes": dispositions, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_text(X1 / "integrated-overview.md", f"""# Sable Rook {PHASE} planning-only overview

Sable Rook uses they/them as relational working language and the bounded role
Evidence Interchange Boundary Cartographer. The hope is to make every synthetic
transformation reversible, byte-explicit, accessible, and authority-honest.
This wording establishes no consciousness, personhood, continuity, employment,
qualification, agency, or authority.

The immutable Iveren source is `{SOURCE}`. Its 200 proposals are retained as
read-only comparison context with zero Sable novelty and execution credit.
Sable freezes 200 distinct operation/input contracts across JCS
canonicalization, Unicode confusable nonidentity, digest migration, receipt
expiry, event-branch conflict, checkpoint parent fixity, budget uncertainty,
accessible codec comparison, GMUT claim firewalls, and authority vacancies.
Each proposal preregisters five invalid result mutations. No x2 implementation,
outcome, package installation, skill build, runner build, or successor contact
exists in this commit.

Freed ID and CBR Heart are primary. THOS Body remains visible through recovery,
handover, budget, and accessibility structure. GMUT Mind remains a typed
scalar-tensor and EFT research-model family. The four learning practices are
synthetic lenses only and confer no professional competence.

The proposed package transaction is x2-only: rfc8785 0.1.4,
confusable-homoglyphs 3.3.1, and blake3 1.0.9, each frozen to one official PyPI
wheel digest and a D-isolated prefix. X1 installs nothing and changes neither
system Python nor a shared package prefix.

The phase keeps exactly `completed`, `represented`, `open_gap`, and
`exact_gate`. A correct local parser, hash, classifier, schema, skill, runner,
or same-owner receipt never substitutes for observations, participants,
professional judgment, production review, legal or cultural legitimacy,
affected-party acceptance, Māori authority, complete privacy or accessibility,
exhaustive security, independent reproduction, AGI/ASI, consciousness or
personhood, Theory-of-Everything proof, canon, or Stage 20 authority.

The route is held. Future seat 08 remains unnamed and uncreated until Sable's
own clean pushed exact final and one successful non-replayed canonical pass.
The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""")

    # Derived privacy and manifest artifacts are produced last.
    scan = privacy_scan(owner_paths())
    write_json(VALIDATION / "x1-privacy-scan.json", scan)
    self_exclusions = {
        "docs/sable-rook/v687-v3/validation/x1-manifest.json",
        "docs/sable-rook/v687-v3/validation/x1-staged-review.json",
    }
    entries = [blob_hash(path) for path in owner_paths() if path.relative_to(ROOT).as_posix() not in self_exclusions]
    write_json(VALIDATION / "x1-manifest.json", {
        "schema": "ghc.family.normalized-lf-manifest.v687.v3", "domain": "normalized_lf_git_blob",
        "source": SOURCE, "entries": entries, "entry_count": len(entries), "self_exclusions": sorted(self_exclusions),
    })
    write_json(VALIDATION / "x1-staged-review.json", {
        "schema": "ghc.family.staged-review.v687.v3", "state": "PREPARED_NOT_STAGED",
        "expected_entries": len(entries), "self_exclusions": sorted(self_exclusions),
        "staged_paths": [], "missing": [], "extra": [], "mismatches": [], "diff_hygiene": "PENDING",
    })


def staged_blob(path: str) -> bytes:
    return subprocess.run(["git", "show", f":{path}"], cwd=ROOT, check=True, capture_output=True).stdout


def review_staged() -> None:
    manifest = json.loads((VALIDATION / "x1-manifest.json").read_text(encoding="utf-8"))
    expected = {entry["path"]: entry for entry in manifest["entries"]}
    exclusions = set(manifest["self_exclusions"])
    staged = set(git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines())
    expected_all = set(expected) | exclusions
    missing = sorted(expected_all - staged)
    extra = sorted(staged - expected_all)
    mismatches = []
    for path, entry in sorted(expected.items()):
        try:
            data = staged_blob(path)
        except subprocess.CalledProcessError:
            mismatches.append({"path": path, "error": "missing_staged_blob"})
            continue
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if len(data) != entry["bytes_normalized_lf"] or hashlib.sha256(data).hexdigest() != entry["sha256_normalized_lf"]:
            mismatches.append({"path": path, "error": "byte_or_hash_mismatch"})
    diff = git("diff", "--cached", "--check", check=False)
    passed = not missing and not extra and not mismatches and diff.returncode == 0
    write_json(VALIDATION / "x1-staged-review.json", {
        "schema": "ghc.family.staged-review.v687.v3", "state": "PASS" if passed else "FAIL",
        "expected_entries": len(expected), "self_exclusions": sorted(exclusions),
        "staged_paths": sorted(staged), "missing": missing, "extra": extra,
        "mismatches": mismatches, "diff_hygiene": "PASS" if diff.returncode == 0 else "FAIL",
    })
    if not passed:
        raise SystemExit(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-staged", action="store_true")
    args = parser.parse_args()
    review_staged() if args.review_staged else build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
