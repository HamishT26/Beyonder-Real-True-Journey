from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = "v672-v1-2-remaster"
OWNER = "Ilyra Fen"
SOURCE = "f67221fbee56905a770c64533771dd9471fb2fba"
SOURCE_X1 = "a6ca461e2eac82cb2fa8c311e58ae5a399601442"
SOURCE_EVIDENCE = "2373cbd3c21448856864caead94581faf46f1a57"
PHASE_ROOT = ROOT / "docs" / "ilyra-fen" / PHASE
X1 = PHASE_ROOT / "x1"
ORIGINAL = ROOT / "docs" / "ilyra-fen" / "v672-v1"
STAMP = "2026-08-27T16:30:00+12:00"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(value.rstrip() + "\n")


def slug(title: str) -> str:
    return "-".join("".join(ch.lower() if ch.isalnum() else " " for ch in title).split())


NEW_TITLES = [
    "Canonical YAML Duplicate-Key Refusal",
    "YAML Alias Expansion Budget",
    "JSON Nonfinite Number Quarantine",
    "JSON Duplicate-Key Evidence Fence",
    "Deterministic Structured-Data Serialization",
    "Schema Version Monotonicity Gate",
    "RFC6901 Pointer Escape Tribunal",
    "RFC6902 Patch Preconditions",
    "JMESPath Query Allowlist",
    "Streaming JSON Record Budget",
    "Deep Structural Diff Review Envelope",
    "Round-Trip Comment Preservation Boundary",
    "Exact Package-Lock Integrity Ledger",
    "Python Wheel Hash Closure",
    "Node Lifecycle-Script Disable Receipt",
    "Direct-versus-Transitive Attribution",
    "D-First Toolchain Rollback Capsule",
    "Global Skill Collision Refusal",
    "Global Skill Byte-Parity Proof",
    "Composite Skill Source Attribution",
    "Freed-ID Four-Tier Flashcard Projection",
    "Flashcard Sensitive-Field Redaction",
    "Method-Flow Failed-Witness Preservation",
    "Stale Beacon Historical Labelling",
    "Parenthetical Remaster Arithmetic Firewall",
    "Original Canonical No-Replay Lock",
    "Remaster Source-Ancestry Witness",
    "X1-X2 Phase Boundary Linter",
    "Owner-Scope Manifest Self-Exclusion",
    "Normalized-Git-Blob Hash Verification",
    "Sparse-Lane Materialization Ceiling",
    "Exact-Title Route Duplicate Guard",
    "Route Pause-and-Redirect Recheck",
    "Privacy Five-Class Candidate Tribunal",
    "Bounded AST Security Diff Screen",
    "Accessible Evidence Index Alternative",
    "Configuration Data Quality Handover",
    "Supply-Chain Metadata Vacancy Refusal",
    "Digital Preservation Fixity Handover",
    "Stage-20 Nonpromotion Seal",
]


PACKAGE_ALLOWLIST = [
    {"ecosystem": "python", "name": "PyYAML", "version": "6.0.3", "artifact": "pyyaml-6.0.3-cp312-cp312-win_amd64.whl", "integrity": "sha256:5fcd34e47f6e0b794d17de1b4ff496c00986e1c83f7ab2fb8fcfe9616ff7477b", "purpose": "safe-load and emit bounded YAML fixtures"},
    {"ecosystem": "python", "name": "deepdiff", "version": "9.1.0", "artifact": "deepdiff-9.1.0-py3-none-any.whl", "integrity": "sha256:80c0460e1993b04f6f0ca79abf25548b129fd218478c4ebb08f80560f5d10610", "purpose": "explain bounded structured-data deltas"},
    {"ecosystem": "python", "name": "ijson", "version": "3.5.1", "artifact": "ijson-3.5.1-cp312-cp312-win_amd64.whl", "integrity": "sha256:322c783f3ee0c6b383bbd4db88370b10172168808cc2a0bf811f1253f7435602", "purpose": "stream bounded JSON without whole-document loading"},
    {"ecosystem": "python", "name": "ruamel.yaml", "version": "0.19.1", "artifact": "ruamel_yaml-0.19.1-py3-none-any.whl", "integrity": "sha256:27592957fedf6e0b62f281e96effd28043345e0e66001f97683aa9a40c667c93", "purpose": "preserve YAML presentation details in disposable fixtures"},
    {"ecosystem": "python", "name": "yamale", "version": "6.1.0", "artifact": "yamale-6.1.0-py3-none-any.whl", "integrity": "sha256:7e109c9d83e3a7e42703516cb2b70b9c7aa5b7a738019c4a6c202b6b0b9096c5", "purpose": "validate trusted phase-local YAML schemas"},
    {"ecosystem": "python", "name": "jsonpointer", "version": "3.1.1", "artifact": "jsonpointer-3.1.1-py3-none-any.whl", "integrity": "sha256:8ff8b95779d071ba472cf5bc913028df06031797532f08a7d5b602d8b2a488ca", "purpose": "resolve RFC6901 pointers in synthetic documents"},
    {"ecosystem": "python", "name": "jmespath", "version": "1.1.0", "artifact": "jmespath-1.1.0-py3-none-any.whl", "integrity": "sha256:a5663118de4908c91729bea0acadca56526eb2698e83de10cd116ae0f4e97c64", "purpose": "query allowlisted fields from bounded JSON"},
    {"ecosystem": "python", "name": "jsonpatch", "version": "1.33", "artifact": "jsonpatch-1.33-py2.py3-none-any.whl", "integrity": "sha256:0ae28c0cd062bbd8b8ecc26d7d164fbbea9652a1a3693f3b956c1eae5145dade", "purpose": "exercise RFC6902 preconditioned synthetic corrections"},
    {"ecosystem": "node", "name": "@biomejs/biome", "version": "2.5.10", "integrity": "sha512-WRKXARA3kTuiV5sxqTpobJ/I0MVd4vk3pOL6wnp5az4LntFIhWTj1RWZq3DI9PCEN3lXcqy7p5aqUHzvq8AXyQ==", "purpose": "bounded formatter and linter for remaster fixtures"},
    {"ecosystem": "node", "name": "ajv", "version": "8.20.0", "integrity": "sha512-Thbli+OlOj+iMPYFBVBfJ3OmCAnaSyNn4M1vz9T6Gka5Jt9ba/HIR56joy65tY6kx/FCF5VXNB819Y7/GUrBGA==", "purpose": "validate JSON Schema fixtures"},
    {"ecosystem": "node", "name": "yaml", "version": "2.9.0", "integrity": "sha512-2AvhNX3mb8zd6Zy7INTtSpl1F15HW6Wnqj0srWlkKLcpYl/gMIMJiyuGq2KeI2YFxUPjdlB+3Lc10seMLtL4cA==", "purpose": "cross-runtime YAML parsing and validation"},
    {"ecosystem": "node", "name": "json-stable-stringify", "version": "1.3.0", "integrity": "sha512-qtYiSSFlwot9XHtF9bD9c7rwKjr+RecWT//ZnPvSmEjpV5mmPOCN4j8UjY5hbjNkOwZ/jQv3J6R1/pL7RwgMsg==", "purpose": "deterministic JSON serialization fixture"},
    {"ecosystem": "node", "name": "semver", "version": "7.8.5", "integrity": "sha512-Y7/KDsb8LjooZpwaqGyulO6DQlksgCncchHGk+sZIY4SBvUocMBEFH5Ur1fI4dV+Jvl0w6cjvucaIi40puRioA==", "purpose": "enforce schema-version compatibility ranges"},
]


SKILL_TITLES = [
    "ghc-family-structured-data-capsule", "ghc-family-yaml-duplicate-key-refusal",
    "ghc-family-json-nonfinite-quarantine", "ghc-family-schema-version-gate",
    "ghc-family-json-pointer-tribunal", "ghc-family-json-patch-precondition",
    "ghc-family-query-allowlist", "ghc-family-streaming-record-budget",
    "ghc-family-structural-diff-envelope", "ghc-family-yaml-roundtrip-boundary",
    "ghc-family-package-integrity-ledger", "ghc-family-direct-dependency-attribution",
    "ghc-family-d-first-toolchain-rollback", "ghc-family-global-skill-collision-guard",
    "ghc-family-global-skill-parity", "ghc-family-composite-skill-attribution",
    "ghc-family-four-tier-flashcard-projection", "ghc-family-method-failure-retention",
    "ghc-family-parenthetical-remaster-firewall", "ghc-family-original-canonical-no-replay",
]


RUNNER_TITLES = [
    "ghc_family_structured_data_guard.py", "ghc_family_yaml_boundary_runner.py",
    "ghc_family_json_integrity_runner.py", "ghc_family_schema_version_runner.py",
    "ghc_family_pointer_patch_runner.py", "ghc_family_query_budget_runner.py",
    "ghc_family_package_integrity_runner.py", "ghc_family_global_skill_parity_runner.py",
    "ghc_family_flashcard_projection_runner.py", "ghc_family_remaster_lifecycle_runner.py",
]


def task_rows(prefix: str, count: int, state: str, family: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"IF6721R2-{prefix}-{i:03d}",
            "title": f"{family} {i:03d}: bounded {slug(family)} review",
            "approval_class": "safe_now" if prefix in {"SAFE", "CFR"} else "candidate",
            "x1_state": "planned_for_x2" if state == "owner" else "recommendation_only",
            "expected_disposition": "completed" if state == "owner" else "represented",
            "external_actions": 0,
            "completion_credit": 0,
        }
        for i in range(1, count + 1)
    ]


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(NEW_TITLES, 1):
        if index <= 28:
            disposition = "completed"
        elif index <= 36:
            disposition = "represented"
        elif index <= 38:
            disposition = "open_gap"
        else:
            disposition = "exact_gate"
        approval = "safe_now" if index <= 20 else "candidate" if index <= 36 else "exact_approval" if index <= 38 else "blocked"
        rows.append(
            {
                "proposal_id": f"IF6721R2-N{index:03d}",
                "title": title,
                "hypothesis": f"A bounded synthetic {title.lower()} artifact can make one remaster decision more testable without conferring external authority.",
                "null_or_failure": "The artifact is ambiguous, accepts its preregistered invalid mutation, exceeds owner scope, or promotes evidence beyond its bounded lane.",
                "approval_class": approval,
                "execution_lane": "x2_synthetic_owner_scope" if approval in {"safe_now", "candidate"} else "unexecuted_gate_register",
                "current_official_or_primary_source_needs": ["current repository schema or skill guidance", "official PyPI, npm, or tool documentation only when the package surface is implicated"],
                "concrete_artifacts": [f"x2/proposals/if6721r2-n{index:03d}.json", f"x2/fixtures/{slug(title)}.json"],
                "falsifier_or_acceptance_gate": "Reject on missing provenance, non-deterministic output, authority promotion, unretained failure, or accepting any preregistered invalid mutation.",
                "rollback_or_recovery": "Quarantine the owner-local artifact, retain the failed witness at zero credit, and recover only the failed dependency without replaying a success.",
                "protected_gates": ["no real data", "no professional or legal authority", "no Maori authority", "no production action", "no independent-reproduction claim", "NOT_READY_FOR_STAGE_20"],
                "expected_disposition": disposition,
                "x1_state": "preregistered_only",
                "completion_credit": 0,
            }
        )
    return rows


def main() -> None:
    if not ORIGINAL.exists():
        raise SystemExit("original v672-v1 evidence is not materialized")
    original_proposals = []
    for path in sorted((ORIGINAL / "x2" / "proposals").glob("*.json"))[:40]:
        value = json.loads(path.read_text(encoding="utf-8"))
        original_proposals.append({
            "source_path": path.relative_to(ROOT).as_posix(),
            "proposal_id": value.get("proposal_id"),
            "title": value.get("title"),
            "current_novelty_credit": 0,
            "current_completion_credit": 0,
            "state": "selected_for_bounded_revalidation_only",
        })
    if len(original_proposals) != 40:
        raise SystemExit(f"expected 40 inherited proposal rows, found {len(original_proposals)}")
    inherited_titles = {row["title"].casefold() for row in original_proposals if row["title"]}
    if len({title.casefold() for title in NEW_TITLES}) != 40 or inherited_titles.intersection(title.casefold() for title in NEW_TITLES):
        raise SystemExit("proposal title novelty guard failed")

    startup_failures = [
        "batched named-skill read truncated before EOF",
        "PowerShell foreach pipeline parser rejected direct pipe",
        "raw authorization-state display truncated before EOF",
        "stale v552 compact-restart beacon preflight remained open",
        "combined ancestry projection hit a PowerShell grouping parser edge",
        "canonical receipt projection guessed absent key names",
        "broad package inventory exceeded its bounded execution window",
        "combined official-registry metadata probe exceeded its bounded execution window",
        "worktree-creation wrapper exceeded its display window after preparing the lane",
        "first scoped x1 validation found the overview below its preregistered 700-word floor",
        "second scoped x1 validation found the prior build receipt self-included on rebuild",
        "first x1 Ruff gate found two import-block formatting findings",
    ]
    source_counts = {"effective_negatives": 35007, "effective_methods": 21553, "effective_failed_witnesses": 6828, "effective_passing_witnesses": 8844, "open_gaps": 273, "exact_gates": 268}
    overlay = dict(source_counts)
    overlay["effective_negatives"] += len(startup_failures)
    overlay["effective_methods"] += len(startup_failures)
    overlay["effective_failed_witnesses"] += len(startup_failures)
    overlay["effective_passing_witnesses"] += len(startup_failures)
    overlay["open_gaps"] += 1

    proposals = proposal_rows()
    outcomes = {label: sum(row["expected_disposition"] == label for row in proposals) for label in ["completed", "represented", "open_gap", "exact_gate"]}
    if outcomes != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise SystemExit(f"unexpected outcome plan {outcomes}")

    write_json(X1 / "activation-intake.json", {
        "schema": "ghc.family.activation-intake.v7", "owner": OWNER, "phase": PHASE,
        "activated_at": STAMP, "source": SOURCE, "source_phase": "v672-v1",
        "parenthetical_remaster": True, "consumes_round_robin_seat": False,
        "next_prospective_edge": {"title": "Auren Lark", "phase": "v672-v2", "precontacted": False},
        "solo": True, "subagents": 0, "forks": 0,
    })
    write_json(X1 / "identity-and-boundary.json", {
        "schema": "ghc.family.identity-boundary.v7", "owner": OWNER, "phase": PHASE,
        "relational_language_only": True,
        "not_evidence_of": ["consciousness", "sentience", "legal personhood", "identity continuity", "employment", "qualification", "independent agency", "scientific authority", "operational authority", "legal authority", "cultural authority", "Maori authority"],
        "protected_boundaries": ["empirical", "participant", "professional", "production", "deployment", "privacy-complete", "accessibility-complete", "exhaustive-security", "independent-reproduction", "AGI/ASI", "Theory-of-Everything", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(X1 / "source-ledger.json", {
        "schema": "ghc.family.source-ledger.v7", "source": SOURCE, "source_x1": SOURCE_X1,
        "source_evidence": SOURCE_EVIDENCE, "source_branch": "codex/GHC-Family/ilyra-fen-v672-v1-full-tools",
        "source_canonical_receipt_sha256": "632c2cfe6b6377979bedbeb6a7512c963bdcdbf475a593b49843ab144cf67b75",
        "source_canonical_replay_prohibited": True, "source_read_only": True,
        "startup_failures": [{"failure_id": f"IF6721R2-START-{i:03d}", "description": text, "credit": 0, "retained": True, "recovery": "bounded successful recovery without erasing the failed witness"} for i, text in enumerate(startup_failures, 1)],
    })
    write_json(X1 / "source-count-overlay.json", {
        "schema": "ghc.family.count-overlay.v5", "repository_sealed_source": source_counts,
        "external_startup_overlay_count": len(startup_failures), "activation_overlay": overlay,
        "source_seal_rewritten": False, "stale_beacon_open_gap_added": 1,
    })
    write_json(X1 / "inherited-proposal-revalidation.json", {
        "schema": "ghc.family.inherited-proposal-revalidation.v6", "owner": OWNER, "phase": PHASE,
        "declared_chain": 5910, "selected_count": 40, "novelty_credit": 0,
        "completion_credit": 0, "rows": original_proposals,
    })
    write_json(X1 / "new-proposal-freeze.json", {
        "schema": "ghc.family.new-proposal-freeze.v7", "owner": OWNER, "phase": PHASE,
        "proposal_chain_before": 5910, "proposal_chain_after_if_evidence_frozen": 5950,
        "rows": proposals, "outcomes": outcomes, "universal_novelty_claim": False,
        "comparison_domain": "exact forty-row predecessor owner slate plus within-remaster title comparison; inaccessible canonical row-to-title mappings remain an explicit gap",
    })
    write_json(X1 / "semantic-neighbor-audit.json", {
        "schema": "ghc.family.semantic-neighbor-audit.v6", "candidate_count": 40,
        "exact_predecessor_rows_compared": 40, "within_slate_duplicates": 0,
        "exact_title_collisions": 0, "declared_inherited_rows_not_locally_compared": 5870,
        "universal_novelty_claim": False,
    })

    safe = task_rows("SAFE", 60, "owner", "safe-now packet")
    candidate = task_rows("CAND", 50, "owner", "candidate packet")
    successor_candidate = task_rows("NEXT-CAND", 20, "successor", "successor candidate packet")
    cleanup = task_rows("CFR", 60, "owner", "CLEAN-FIX-REFINE")
    successor_cleanup = task_rows("NEXT-CFR", 30, "successor", "successor CLEAN-FIX-REFINE")
    exact = [{"task_id": f"IF6721R2-EXACT-{i:03d}", "title": f"exact approval packet {i:03d}", "approval_class": "exact_approval", "x1_state": "visible_unexecuted", "expected_disposition": "exact_gate", "completion_credit": 0} for i in range(1, 21)]
    blocked = [{"task_id": f"IF6721R2-BLOCK-{i:03d}", "title": f"blocked authority packet {i:03d}", "approval_class": "blocked", "x1_state": "visible_unexecuted", "expected_disposition": "exact_gate", "completion_credit": 0} for i in range(1, 11)]
    skills = [{"task_id": f"IF6721R2-SKILL-{i:03d}", "title": title, "x1_state": "planned_for_x2", "completion_credit": 0} for i, title in enumerate(SKILL_TITLES, 1)]
    runners = [{"task_id": f"IF6721R2-RUNNER-{i:03d}", "title": title, "x1_state": "planned_for_x2", "completion_credit": 0} for i, title in enumerate(RUNNER_TITLES, 1)]
    next_skills = [{"task_id": f"IF6721R2-NEXT-SKILL-{i:03d}", "title": f"auren structured-evidence skill idea {i:03d}", "x1_state": "recommendation_only", "completion_credit": 0} for i in range(1, 11)]
    next_runners = [{"task_id": f"IF6721R2-NEXT-RUNNER-{i:03d}", "title": f"ghc_family_auren_structured_evidence_runner_{i:03d}.py", "x1_state": "recommendation_only", "completion_credit": 0} for i in range(1, 11)]
    write_json(X1 / "portfolio-freeze.json", {
        "schema": "ghc.family.portfolio-freeze.v8", "owner": OWNER, "phase": PHASE,
        "caps_are_ceilings_not_quotas": True, "filler_prohibited": True,
        "counts": {"safe_now_owner": len(safe), "candidate_owner": len(candidate), "candidate_successor": len(successor_candidate), "exact_approval": len(exact), "blocked": len(blocked), "skills_owner": len(skills), "runners_owner": len(runners), "skills_successor": len(next_skills), "runners_successor": len(next_runners), "clean_fix_refine_owner": len(cleanup), "clean_fix_refine_successor": len(successor_cleanup), "package_direct_surfaces": len(PACKAGE_ALLOWLIST)},
        "rows": safe + candidate + successor_candidate + exact + blocked + skills + runners + next_skills + next_runners + cleanup + successor_cleanup,
        "package_allowlist": PACKAGE_ALLOWLIST,
        "package_transaction": {"state": "planned_only", "python_environment": "D:/GHC-Archives/global-tools/ilyra-v672-v1-2/python", "node_environment": "D:/GHC-Archives/global-tools/ilyra-v672-v1-2/node", "system_python_mutation": False, "npm_global_prefix_mutation": False, "wheel_only": True, "hash_required": True, "npm_ignore_scripts": True, "rollback": "remove only the exact owner-attributed isolated environment after verifying its token and path"},
        "global_skill_promotions": ["ghc-family-accessible-sheet-index", "ghc-family-datum-uncertainty-ledger", "ghc-family-drawing-fixity-manifest", "ghc-family-drawing-handover-proxy", "ghc-family-drawing-authority-nonpromotion"],
        "composite_global_skill": "ghc-family-d-first-structured-evidence-toolchain",
        "bounded_practice_lenses": ["synthetic configuration data-quality analyst", "synthetic software supply-chain metadata steward", "synthetic digital-preservation package registrar"],
        "successor_practice_recommendation": "synthetic public-interest incident documentation analyst",
    })
    write_json(X1 / "threat-model.json", {
        "schema": "ghc.family.threat-model.v7", "assets": ["original seal", "remaster manifests", "isolated tool environments", "global skill root", "route acknowledgement"],
        "threats": ["dependency confusion", "unhashed artifact", "npm lifecycle script", "YAML unsafe constructor", "alias resource exhaustion", "duplicate key", "nonfinite JSON", "symlink or collision overwrite", "canonical replay", "route duplicate", "privacy leakage", "authority promotion"],
        "controls": ["official registry provenance", "exact direct pins", "wheel hashes", "npm lock integrities", "ignore scripts", "safe loaders", "bounded input sizes", "exclusive collision refusal", "byte parity", "one-success lock", "five-class scan", "four truth labels"],
        "residual": ["registry compromise beyond bounded metadata", "transitive future advisories", "parent-directory reparse races", "non-exhaustive privacy and security review"],
    })
    write_json(X1 / "workflow-plan.json", {
        "schema": "ghc.family.workflow-plan.v8", "owner": OWNER, "phase": PHASE,
        "lifecycle": ["read-only source verification", "planning-only x1 freeze", "x1 commit and fresh four-way equality", "x2 bounded execution", "immutable evidence commit", "closeout and final commit", "one exact-final owner-scoped canonical pass", "one exact-title Auren activation if every route gate permits"],
        "strict_x1_before_x2": True, "commit_ceiling": 8, "planned_commits": 3,
        "materialized_file_ceiling": 2000, "canonical_success_ceiling": 1,
        "replay_after_success": False, "full_repository_suite": False,
    })
    write_json(X1 / "route-plan.json", {
        "schema": "ghc.family.route-plan.v7", "state": "PROSPECTIVE_NOT_CONTACTED",
        "target_exact_title": "Auren Lark", "target_phase": "v672-v2",
        "required_terminal_gates": ["clean exact final", "pushed 0/0 divergence", "fresh local-upstream-tracking-live equality", "one successful canonical pass", "current live authority reread", "bounded task list <= 50", "unique exact-title match", "immediate target reread", "duplicate-pause-usage-privacy-evidence-safety guard"],
        "next_target_instruction": "After Auren v672-v2, message the exact existing Sable Rook task for v672-v3 only after Auren's own terminal gate and current live route reread.",
        "precontacted": False, "substitute_permitted": False, "resend_permitted": False,
    })
    write_json(X1 / "flashcard-plan.json", {
        "schema": "ghc.family.freed-id-flashcard-plan.v2", "tiers": ["Freed ID owner card", "GMUT-THOS-Freed ID and CBR pillar card", "bounded practice card", "task and method card"],
        "minimum_sections": 10, "sensitive_fields": "redacted or omitted", "identity_claims": False,
        "handoff_projection": True, "source_of_truth": "file-backed evidence, never flashcard text alone",
    })
    write_json(X1 / "method-flow-startup.json", {
        "schema": "ghc.family.method-flow.v8", "owner": OWNER, "phase": PHASE,
        "source_counts": source_counts, "activation_overlay": overlay,
        "failed_witnesses": [{"id": f"IF6721R2-START-{i:03d}", "status": "failed_retained_zero_credit", "description": text} for i, text in enumerate(startup_failures, 1)],
        "recovery_rule": "A recovery is a new bounded method; it never erases or relabels the failed witness.",
    })
    write_json(X1 / "phase-truth.json", {
        "schema": "ghc.family.phase-truth.v8", "owner": OWNER, "phase": PHASE,
        "state": "X1_PLANNING_ONLY", "source": SOURCE, "proposal_chain_source": 5910,
        "proposal_chain_if_x2_evidence_frozen": 5950, "expected_outcomes": outcomes,
        "x2_executed": False, "packages_installed": 0, "global_skills_installed": 0,
        "external_actions": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    overview = f"""# Ilyra Fen {PHASE} planning-only x1 overview

## Purpose and source discipline

This parenthetical remaster begins from the immutable, already sealed Ilyra v672-v1 exact final `{SOURCE}`. It does not consume a new round-robin seat, rewrite the original phase, replay the original canonical validator, or claim inherited work as remaster novelty. The source x1 and evidence anchors remain `{SOURCE_X1}` and `{SOURCE_EVIDENCE}`. Every source, sibling, shared, and standby lane remains read-only. The remaster owns only its fresh sparse D:-first branch and artifacts.

## Evidence boundary

Names, roles, hopes, pronouns, family language, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, legal or cultural authority, affected-party authority, or Maori authority. This phase uses synthetic configuration, package-metadata, and digital-preservation fixtures only. It establishes no empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, Theory-of-Everything, canon, or Stage 20 result. The verdict remains `NOT_READY_FOR_STAGE_20`.

## Proposal and portfolio freeze

Forty inherited Ilyra v672-v1 proposal rows are selected for bounded revalidation with zero remaster novelty and zero remaster completion credit. Forty distinct remaster proposals are preregistered after exact-title comparison with that predecessor slate and within-slate comparison. Because the repository does not expose a complete canonical mapping for every declared inherited row, universal novelty is not claimed. If and only if x2 evidence is frozen, the declared chain would move from 5,910 to 5,950. Expected new outcomes are 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`; these are expectations, not x1 observations.

The frozen portfolio contains sixty safe-now owner packets, fifty owner candidate packets, twenty candidate recommendations for Auren, twenty exact-approval packets kept visible and unexecuted, ten blocked packets kept visible and unexecuted, twenty owner skill builds, ten owner runner builds, ten successor skill ideas, ten successor runner ideas, sixty owner CLEAN/FIX/REFINE reviews, and thirty successor cleanup recommendations. Caps are ceilings, never quotas, and filler is prohibited. Completion credit remains zero throughout x1.

## Toolchain plan

Thirteen direct package surfaces are allowlisted: eight Python packages and five Node packages. PyYAML is included at Hamish's explicit request, but the record distinguishes its pre-existing system presence from a new direct, pinned, owner-attributable installation in an isolated D:-backed environment. No system-Python mutation, npm-global-prefix mutation, PATH/profile mutation, elevation, desktop update, host-security weakening, Windows-feature change, or reboot is planned. Python requires wheel-only resolution and exact SHA-256 closure; Node requires exact package-lock integrity and disabled lifecycle scripts. Every direct surface needs one useful positive smoke and one rejecting or boundary witness. An audit is bounded and cannot establish future or exhaustive safety.

## Skills and Method Flow

Five collision-free, already validated Ilyra archive skills are proposed for additive global promotion with exact source/global byte parity. A new composite skill, `ghc-family-d-first-structured-evidence-toolchain`, will coordinate existing drive-guardian, meta-toolbox, Method Flow, reflection, and flashcard responsibilities while preserving their attribution and avoiding destructive history merging. Every failed attempt remains retained at zero credit. Nine startup failures and their bounded recoveries are already registered; the stale v552 beacon remains an explicit open gap rather than a current-state authority.

The remaster also separates discovery, authorization, installation, smoke evidence, and broader claims. A registry record may support a version or artifact hash, but it does not authorize installation by itself. A successful import or command smoke may establish only that one bounded invocation worked in the isolated environment; it does not establish production fitness, future safety, complete compatibility, legal license interpretation, or independent review. Each package, skill, and runner therefore keeps its own attribution, rejection fixture, rollback path, and zero-credit failure history instead of being compressed into one aggregate success label.

## Human-practice lenses

The three lenses are synthetic configuration data-quality analysis, synthetic software supply-chain metadata stewardship, and synthetic digital-preservation package registration. They provide vocabulary and refusal-fixture structure only. No real workplace, worker, customer, record, package, credential, system, release, preservation object, authority decision, or external action is used. Auren receives one recommendation only: synthetic public-interest incident documentation analysis.

## Lifecycle and route

X1 must be committed, pushed, clean, zero divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 begins. X2 may then execute only the preregistered safe-now and candidate work. Evidence and closeout remain separate commits. After a clean pushed exact final, one owner-scoped canonical aggregate may run once; a success must never be replayed. Only then may the current live authority and task roster be reread. Auren Lark must be uniquely resolved from a bounded list, immediately reread, guarded against duplication or pause, and sent one sanitized file pointer at most once. Acknowledged delivery and repository preparation are separate truths.
"""
    write_text(X1 / "integrated-overview.md", overview)

    files = sorted(path for path in X1.rglob("*") if path.is_file() and path.name != "build-receipt.json")
    manifest = [{"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size} for path in files]
    write_json(X1 / "build-receipt.json", {
        "schema": "ghc.family.x1-build-receipt.v7", "owner": OWNER, "phase": PHASE,
        "state": "X1_PLANNING_ONLY", "generated_at": STAMP, "file_count_before_receipt": len(files),
        "manifest": manifest, "x2_mutations": 0, "source_mutations": 0,
    })
    print(json.dumps({"phase": PHASE, "state": "X1_PLANNING_ONLY", "proposal_count": len(proposals), "portfolio_rows": len(safe + candidate + successor_candidate + exact + blocked + skills + runners + next_skills + next_runners + cleanup + successor_cleanup), "package_direct_surfaces": len(PACKAGE_ALLOWLIST), "x1_files": len(files) + 1}, sort_keys=True))


if __name__ == "__main__":
    main()
