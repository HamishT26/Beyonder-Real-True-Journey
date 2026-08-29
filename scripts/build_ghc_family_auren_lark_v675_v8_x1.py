from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v675-v8"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "ea5d34c1eaef0e1f40901c1c38961fdcf7e8e92d"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v675-v7-full-tools"
BRANCH = "codex/GHC-Family/auren-lark-v675-v8-full-tools"
OWNER = "Auren Lark"
PHASE = "v675-v8"
SUCCESSOR = "Sable Rook"
SUCCESSOR_PHASE = "v676-v1"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]

SOURCE_SEAL = {
    "effective_negatives": 41286,
    "methods": 29875,
    "failed_witnesses": 12947,
    "bounded_passing_witnesses": 17154,
    "open_gaps": 343,
    "exact_gates": 335,
    "declared_proposals": 7310,
    "verdict": "NOT_READY_FOR_STAGE_20",
}


ACTIVATION_OVERLAY = {
    "effective_negatives": 41290,
    "methods": 29879,
    "failed_witnesses": 12951,
    "bounded_passing_witnesses": 17157,
    "open_gaps": 343,
    "exact_gates": 335,
    "declared_proposals": 7310,
    "verdict": "NOT_READY_FOR_STAGE_20",
}


BOUNDARY = (
    "All fixtures are synthetic. No real person, organization, repository, service, "
    "deployment, package registry transaction, configuration, credential, key, incident, "
    "measurement, participant decision, employment act, professional decision, rights "
    "decision, affected-party decision, legal or cultural decision, Maori-authority act, "
    "or external action is used or established. THOS remains bounded prototype and "
    "documentation evidence only, never production readiness, deployment authority, "
    "exhaustive security, complete privacy, or complete accessibility assurance. GMUT "
    "remains a typed scalar-tensor and effective-field-theory research-model family "
    "without empirical confirmation, final physics, Theory-of-Everything proof, or canon. "
    "Freed ID and CBR remain synthetic and nonproduction. Same-owner software evidence "
    "under shared infrastructure is not independent reproduction, an external audit, "
    "consciousness or personhood evidence, or Stage 20 readiness."
)


PROPOSAL_TITLES = [
    "Synthetic release identity record with ambiguous-channel quarantine",
    "Synthetic configuration schema version with unsupported-transition refusal",
    "Synthetic package artifact ledger with exact digest preservation",
    "Synthetic dependency edge register with undeclared-edge rejection",
    "Synthetic environment declaration with host-specific value quarantine",
    "Synthetic default-value provenance with implicit-default nonpromotion",
    "Synthetic configuration patch sequence with ordered-operation validation",
    "Synthetic rollback checkpoint with missing-baseline exact stop",
    "Synthetic reversible migration plan with source-state preservation",
    "Synthetic drift comparison ledger with bounded-difference classification",
    "Synthetic release-note crosswalk with undocumented-change retention",
    "Synthetic change-request identifier with duplicate-cycle rejection",
    "Synthetic approval-state vocabulary with authority-vacancy preservation",
    "Synthetic maintenance-window record with timezone-ambiguity quarantine",
    "Synthetic feature-flag ledger with stale-flag review hold",
    "Synthetic canary-stage model with production-action prohibition",
    "Synthetic health-check contract with unobserved-state representation",
    "Synthetic alert-severity vocabulary with unsupported-escalation refusal",
    "Synthetic timeout budget with unit and boundary validation",
    "Synthetic retry policy with non-idempotent-operation exact gate",
    "Synthetic concurrency guard with unresolved-order open gap",
    "Synthetic configuration merge with conflicting-key quarantine",
    "Synthetic rollback reason code with causal-inference prohibition",
    "Synthetic backup lineage record with unverifiable-copy representation",
    "Synthetic restore rehearsal receipt with real-restore nonclaim",
    "Synthetic failover plan with absent-secondary open gap",
    "Synthetic service ownership field with employment-authority nonclaim",
    "Synthetic handover checklist with unresolved-item blocking rule",
    "Synthetic operational-readiness label with production-certification refusal",
    "Synthetic security-review marker with exhaustive-security nonclaim",
    "Synthetic privacy-class ledger with five-class bounded scan",
    "Synthetic accessibility-review marker with completeness nonclaim",
    "Synthetic license expression record with legal-advice refusal",
    "Synthetic software bill-of-materials index with completeness nonclaim",
    "Synthetic provenance chain with source-versus-inference separation",
    "Synthetic correction ledger with overwrite and erasure rejection",
    "Synthetic manifest replay contract with normalized-line-ending rule",
    "Synthetic configuration snapshot with private-material exclusion",
    "Synthetic key-reference field with raw-secret prohibition",
    "Synthetic external-endpoint placeholder with network-action prohibition",
    "Synthetic audit-event sequence with missing-event vacancy encoding",
    "Synthetic review disposition with four-label enforcement",
    "Synthetic candidate-to-completed transition with evidence requirement",
    "Synthetic represented-state record with automatic-promotion refusal",
    "Synthetic open-gap register with unresolved-evidence retention",
    "Synthetic exact-gate register with competent-authority requirement",
    "Synthetic culturally scoped configuration note with competent Maori-authority exact gate",
    "Synthetic affected-party field with consent-vacancy preservation",
    "Synthetic professional-review field with qualification nonclaim",
    "Synthetic empirical-result field with observation-absence refusal",
    "Synthetic independent-reproduction field with same-owner nonpromotion",
    "Synthetic GMUT comparison note with Theory-of-Everything nonclaim",
    "Synthetic THOS capability note with AGI-ASI and deployment nonclaim",
    "Synthetic Freed-ID governance note with nonproduction boundary",
    "Synthetic incident record with real-person and real-system exclusion",
    "Synthetic deprecation schedule with unresolved-consumer representation",
    "Synthetic compatibility matrix with untested-combination quarantine",
    "Synthetic release-candidate seal with exact-manifest requirement",
    "Synthetic terminal handoff packet with duplicate-send prohibition",
    "Synthetic Stage-20 verdict guard with NOT_READY preservation",
]


STARTUP_FAILURES = [
    {
        "failure_id": "AL6758-OP-001",
        "surface": "PowerShell revision range",
        "failure": "an interpolated source-to-final revision omitted explicit variable braces and produced an invalid count",
        "recovery": "used a literal bounded revision string and confirmed three commits and zero merges"
    },
    {
        "failure_id": "AL6758-OP-002",
        "surface": "PowerShell size inventory",
        "failure": "a foreach expression was piped without first materializing its bounded output",
        "recovery": "materialized the scalar rows before sorting and serialization"
    },
    {
        "failure_id": "AL6758-OP-003",
        "surface": "current authority display",
        "failure": "one oversized current-state rendering was truncated before the full schema was attributable",
        "recovery": "read the exact file in bounded numbered chunks through EOF"
    },
    {
        "failure_id": "AL6758-OP-004",
        "surface": "workspace dependency discovery",
        "failure": "the first direct dependency-loader wrapper returned no attributable display output",
        "recovery": "used the exact installed MCP variant once and recorded its bounded runtime paths"
    },
    {
        "failure_id": "AL6758-OP-005",
        "surface": "manifest replay design",
        "failure": "an initial verifier invoked hundreds of individual Git reads and yielded no usable result",
        "recovery": "replaced it with one tree map and bounded git cat-file batch replay"
    },
    {
        "failure_id": "AL6758-OP-006",
        "surface": "manifest batch scope",
        "failure": "a second verifier accidentally requested every repository blob and yielded no usable result",
        "recovery": "restricted the batch to exact manifest and owner-entry object identifiers"
    },
    {
        "failure_id": "AL6758-OP-007",
        "surface": "worktree setup display",
        "failure": "the additive worktree operation exceeded its initial display window after mutation began",
        "recovery": "did not replay creation and verified the persisted branch, path, sparse rules, and exact head"
    },
    {
        "failure_id": "AL6758-OP-008",
        "surface": "premature status probe",
        "failure": "a status check ran while sparse checkout was still applying and displayed transient deletions",
        "recovery": "waited for Git and index activity to finish before proving the lane clean"
    },
    {
        "failure_id": "AL6758-OP-009",
        "surface": "PowerShell builder inventory",
        "failure": "a bounded foreach result was piped directly and triggered EmptyPipeElement before inspection",
        "recovery": "materialized the rows before converting them to JSON"
    },
    {
        "failure_id": "AL6758-OP-010",
        "surface": "npm metadata wrapper",
        "failure": "the first npm-view aggregate returned no usable metadata before its output window closed",
        "recovery": "queried the official npm registry JSON with a bounded timeout and retained the first attempt at zero credit"
    },
    {
        "failure_id": "AL6758-OP-011",
        "surface": "isolated x1 pytest runtime",
        "failure": "the bundled Python found user-site pytest but could not import its Pygments dependency",
        "recovery": "used the already-installed D-aware system Python for only the bounded owner x1 tests"
    },
    {
        "failure_id": "AL6758-OP-012",
        "surface": "bounded proposal novelty audit",
        "failure": "the first x1 test found one exact current-title match in the sixty-row inherited comparison set",
        "recovery": "renamed only the uncommitted current title to a distinct configuration-specific contract before x1 freeze"
    }
]



def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_text(*args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", "-C", str(ROOT), *args], check=False, capture_output=True, text=True, encoding="utf-8")
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def git_json(spec: str) -> Any:
    raw = subprocess.run(
        ["git", "-C", str(ROOT), "show", spec], check=True, capture_output=True
    ).stdout
    return json.loads(raw.decode("utf-8"))


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(normalized(path.read_bytes())).hexdigest()


def token_set(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def similarity(left: str, right: str) -> float:
    a, b = token_set(left), token_set(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def predecessor_rows() -> list[dict[str, Any]]:
    ilyra = git_json(f"{SOURCE}:docs/ilyra-fen/v675-v7/x1/new-proposal-freeze.json").get("rows")
    lyren = git_json(f"{SOURCE}:docs/lyren-moss/v675-v6/x1/new-proposal-freeze.json").get("rows")
    if not isinstance(ilyra, list) or len(ilyra) != 40:
        raise RuntimeError("unexpected Ilyra predecessor proposal schema")
    if not isinstance(lyren, list) or len(lyren) != 40:
        raise RuntimeError("unexpected Lyren predecessor proposal schema")
    return [
        *[{**row, "source_owner": "Ilyra Fen", "source_phase": "v675-v7"} for row in ilyra],
        *[{**row, "source_owner": "Lyren Moss", "source_phase": "v675-v6"} for row in lyren[:20]],
    ]


def outcome_for(index: int) -> str:
    if index <= 42:
        return "completed"
    if index <= 54:
        return "represented"
    if index <= 57:
        return "open_gap"
    return "exact_gate"


def build_overview() -> str:
    sections = [
        ("1. Activation and ownership", f"{OWNER} owns solo {PHASE}. The immutable source is `{SOURCE}` on `{SOURCE_BRANCH}`. This x1 is planning-only and creates no x2 evidence."),
        ("2. Primary pillar", "THOS Body is primary through deterministic synthetic configuration change, patch, rollback, drift, and handover contracts. GMUT Mind and Freed ID and CBR Heart remain explicit protected pillars."),
        ("3. Synthetic practice", "The bounded domain is a wholly invented software release-configuration workbook. No real repository, service, package transaction, deployment, organization, person, incident, or authority action is present."),
        ("4. Practice lenses", "The selected learning lenses are software configuration management analyst and digital-preservation package auditor. Sable receives only an advisory synthetic geospatial metadata correction practice. None is a qualification or professional act."),
        ("5. Proposal freeze", "Sixty distinct Auren titles are frozen for x2 with 42 completed, 12 represented, 3 open_gap, and 3 exact_gate planned outcomes. Sixty inherited Ilyra and Lyren contracts are separately revalidated at zero novelty and completion credit."),
        ("6. Approval portfolio", "X1 plans 120 owner safe-now tasks, 80 owner candidates, 20 successor candidate recommendations, 20 held exact-approval packets, and 10 held blocked packets. Held or recommended rows create no authority."),
        ("7. Tools, skills, and runners", "X1 plans three attributable tool transactions, twenty repository-local skills, ten repository-local runners, and ten successor skill plus ten successor runner recommendations. No x2 transaction or shared mutation occurs in x1."),
        ("8. Retained negatives", f"All {len(STARTUP_FAILURES)} startup operational failures remain visible at zero credit with bounded recoveries. Later failures are added and never rewritten into success."),
        ("9. Route and authority", f"The prospective terminal edge is {OWNER} to {SUCCESSOR} for {SUCCESSOR_PHASE}. It remains PREPARED_NOT_SENT until Auren's clean, pushed, fresh-live-equal exact terminal gate and a new live route reread."),
        ("10. Terminal truth", "GMUT is not confirmed physics or a Theory of Everything. THOS is not production-ready or AGI-ASI evidence. Freed ID and CBR are not deployed governance or identity infrastructure. The terminal verdict remains `NOT_READY_FOR_STAGE_20`."),
    ]
    return "# Auren Lark v675-v8 planning-only x1\n\n" + "\n\n".join(f"## {title}\n\n{body}" for title, body in sections)


def owner_paths(include_manifest: bool = True) -> list[Path]:
    paths = [p for p in BASE.rglob("*") if p.is_file()]
    named = [
        ROOT / "scripts" / "build_ghc_family_auren_lark_v675_v8_x1.py",
        ROOT / "tests" / "test_ghc_family_auren_lark_v675_v8_x1.py",
    ]
    paths.extend(p for p in named if p.exists())
    if not include_manifest:
        paths = [p for p in paths if p != VALIDATION / "x1-index-manifest.json"]
    return sorted(set(paths), key=lambda p: p.relative_to(ROOT).as_posix())


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_path": re.compile(
            r"(?:[A-Za-z]:\\" + r"Users\\[^\\\s]+|/" + r"home/[^/\s]+|/" + r"Users/[^/\s]+)"
        ),
        "credential": re.compile(r"(?:AKIA[0-9A-Z]{16}|Bearer\s+[A-Za-z0-9._~-]{20,}|(?:password|secret|api[_-]?key)\s*[:=]\s*[^\s]{8,})", re.I),
        "contact": re.compile(r"(?:[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|\+\d[\d ()-]{8,}\d|\b\d{3}[- ]\d{3}[- ]\d{4}\b)", re.I),
        "network": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    }
    hits: list[dict[str, str]] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for category, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"category": category, "path": path.relative_to(ROOT).as_posix()})
    return {
        "schema": "ghc-family-five-class-privacy-scan-v1",
        "owner": OWNER,
        "phase": PHASE,
        "classes": list(patterns),
        "scanned_files": len(paths),
        "confirmed_hits": hits,
        "confirmed_hit_count": len(hits),
        "scope": "bounded owner x1 text only; not complete privacy assurance",
    }


def build() -> None:
    X1.mkdir(parents=True, exist_ok=True)
    VALIDATION.mkdir(parents=True, exist_ok=True)
    head = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    if head != SOURCE or branch != BRANCH:
        raise RuntimeError(f"wrong startup lane: {branch}@{head}")

    predecessor = predecessor_rows()
    predecessor_titles = [str(row["title"]) for row in predecessor]
    duplicates = sorted(set(PROPOSAL_TITLES) & set(predecessor_titles))
    pairings = [
        {"new_title": title, "closest_predecessor": max(predecessor_titles, key=lambda old: similarity(title, old)), "score": round(max(similarity(title, old) for old in predecessor_titles), 6)}
        for title in PROPOSAL_TITLES
    ]
    max_similarity = max(float(row["score"]) for row in pairings)
    proposals = [
        {
            "proposal_id": f"AL6758-N{index:03d}",
            "title": title,
            "planned_outcome": outcome_for(index),
            "x1_state": "frozen_planning_only",
            "primary_pillar": "THOS Body",
            "protected_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
            "synthetic_only": True,
            "real_world_action": False,
            "external_transport": False,
            "boundary": BOUNDARY,
        }
        for index, title in enumerate(PROPOSAL_TITLES, 1)
    ]
    inherited = [
        {
            "revalidation_id": f"AL6758-R{index:03d}",
            "source_proposal_id": row["proposal_id"],
            "title": row["title"],
            "source_owner": row["source_owner"],
            "source_phase": row["source_phase"],
            "novelty_credit": 0,
            "completion_credit": 0,
            "state": "planned_bounded_revalidation",
        }
        for index, row in enumerate(predecessor[:60], 1)
    ]
    safe_actions = ["validate schema", "preserve provenance", "exercise rollback", "classify drift", "retain uncertainty", "replay manifest"]
    safe = [
        {
            "task_id": f"AL6758-SN-{i:03d}", "state": "planned_safe_now",
            "action": safe_actions[(i - 1) % len(safe_actions)],
            "contract": PROPOSAL_TITLES[(i - 1) % len(PROPOSAL_TITLES)],
            "authority": "owner_local_synthetic_only",
        }
        for i in range(1, 121)
    ]
    candidates = [
        {
            "task_id": f"AL6758-CA-{i:03d}", "state": "planned_candidate_evaluation",
            "contract": PROPOSAL_TITLES[(i - 1) % len(PROPOSAL_TITLES)],
            "execution_requires": "bounded_x2_disposition",
        }
        for i in range(1, 81)
    ]
    successor_candidates = [
        {
            "recommendation_id": f"SAB6761-CA-{i:03d}", "state": "recommendation_only",
            "practice": "synthetic geospatial metadata catalog correction",
            "authority": "none",
        }
        for i in range(1, 21)
    ]
    exact = [{"packet_id": f"AL6758-EX-{i:03d}", "state": "held_exact_approval", "executed": False} for i in range(1, 21)]
    blocked = [{"packet_id": f"AL6758-BL-{i:03d}", "state": "held_blocked", "executed": False} for i in range(1, 11)]
    cfr_actions = ["normalize owner JSON", "tighten owner test", "clarify refusal", "replay owner manifest", "review owner route", "simplify owner method"]
    cfr = [
        {"task_id": f"AL6758-CFR-{i:03d}", "state": "planned_owner_cleanup", "action": cfr_actions[(i - 1) % len(cfr_actions)], "scope": "owner_lane_only"}
        for i in range(1, 101)
    ]
    successor_cfr = [{"recommendation_id": f"SAB6761-CFR-{i:03d}", "state": "recommendation_only", "authority": "none"} for i in range(1, 31)]
    skill_names = [
        "ghc-family-synthetic-release-identity-guard", "ghc-family-synthetic-config-schema-transition",
        "ghc-family-synthetic-artifact-digest-ledger", "ghc-family-synthetic-dependency-edge-guard",
        "ghc-family-synthetic-environment-quarantine", "ghc-family-synthetic-default-provenance",
        "ghc-family-synthetic-json-patch-sequencer", "ghc-family-synthetic-rollback-checkpoint",
        "ghc-family-synthetic-drift-classifier", "ghc-family-synthetic-change-request-cycle-guard",
        "ghc-family-synthetic-authority-vacancy", "ghc-family-synthetic-maintenance-time-guard",
        "ghc-family-synthetic-timeout-budget", "ghc-family-synthetic-idempotency-gate",
        "ghc-family-synthetic-privacy-five-class", "ghc-family-synthetic-accessibility-nonclaim",
        "ghc-family-synthetic-sbom-completeness-nonclaim", "ghc-family-synthetic-manifest-replay",
        "ghc-family-synthetic-handover-stop", "ghc-family-synthetic-stage20-veto",
    ]
    runner_names = [
        "ghc_family_synthetic_config_schema_guard", "ghc_family_synthetic_patch_sequence_guard",
        "ghc_family_synthetic_rollback_guard", "ghc_family_synthetic_drift_guard",
        "ghc_family_synthetic_provenance_guard", "ghc_family_synthetic_authority_vacancy_guard",
        "ghc_family_synthetic_privacy_boundary_guard", "ghc_family_synthetic_manifest_replay_guard",
        "ghc_family_synthetic_handover_guard", "ghc_family_synthetic_stage20_guard",
    ]
    skills = [{"skill_id": name, "state": "planned_repository_local", "global_install": False} for name in skill_names]
    runners = [{"runner_id": name, "state": "planned_repository_local", "global_install": False} for name in runner_names]
    successor_skills = [{"idea_id": f"SAB6761-SK-{i:02d}", "state": "recommendation_only", "authority": "none"} for i in range(1, 11)]
    successor_runners = [{"idea_id": f"SAB6761-RN-{i:02d}", "state": "recommendation_only", "authority": "none"} for i in range(1, 11)]


    write_json(X1 / "activation-intake.json", {
        "schema": "ghc-family-activation-intake-v1", "owner": OWNER, "phase": PHASE,
        "source_branch": SOURCE_BRANCH, "source_head": SOURCE, "target_branch": BRANCH,
        "packet_read_complete": True, "guidance_read_complete": True, "solo": True,
        "activation_received_via": "manual_user_relay_acknowledged",
        "x1_state": "planning_only", "x2_mutation_authorized_before_x1_gate": False,
        "relational_language_only": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(X1 / "source-verification.json", {
        "schema": "ghc-family-source-verification-v1", "owner": OWNER, "phase": PHASE,
        "source_head": SOURCE, "verified_head": head, "verified_branch": branch,
        "source_branch": SOURCE_BRANCH, "ilyra_source": "7c60b4452d3b98a4bcdc9362eea35a4c07f4fe29",
        "ilyra_x1": "88cc5a56ff27f9b3861d6f19963d1c0d1739bf58",
        "ilyra_evidence": "e92c785bd08d0f2e4088a2d296ed56b987e4c20c",
        "ilyra_final": SOURCE, "source_to_final_commits": 3, "source_to_final_merges": 0,
        "source_exact_final_clean_equal": True,
        "activation_candidate_sha256": "830bb9db35ba4092274c84cc345833c7f3685b46f3e98513eb5a1fa4bcf4aaf5",
        "source_canonical_payload_sha256": "824d85e6e043506c25f9b7fce8a56e8f41ac909ae57944aa1dd284630c106801",
        "source_external_receipt_sha256": "7e103b3c94cbf4e09ce3637e84acee005988e4f7a3be498abf5ecbee89736bcb",
        "inherited_validation_credit": 0,
    })
    write_json(X1 / "identity-and-authority-boundary.json", {
        "schema": "ghc-family-relational-identity-boundary-v1", "owner": OWNER, "phase": PHASE,
        "relational_working_language_only": True, "boundary": BOUNDARY,
        "not_evidence_of": ["consciousness", "sentience", "legal personhood", "identity continuity", "employment", "qualification", "independent agency", "scientific authority", "operational authority", "legal authority", "cultural authority", "affected-party authority", "Maori authority"],
        "hamish_may": ["rename", "pause", "redirect", "narrow", "stop"],
    })
    write_json(X1 / "practice-lenses.json", {
        "schema": "ghc-family-synthetic-practice-lenses-v1", "owner": OWNER, "phase": PHASE,
        "primary_pillar": "THOS Body", "protected_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        "domain": "wholly synthetic software release-configuration change, patch, rollback, drift, and handover",
        "owner_lenses": ["software configuration management analyst", "digital-preservation package auditor"],
        "successor_recommendation": "synthetic geospatial metadata catalog correction registrar",
        "successor_authority": "advisory_only", "professional_claim": False,
        "real_records_used": False, "boundary": BOUNDARY,
    })
    write_json(X1 / "new-proposal-freeze.json", {
        "schema": "ghc-family-new-proposal-freeze-v1", "owner": OWNER, "phase": PHASE,
        "count": 60, "declared_chain_before": 7310, "declared_chain_after": 7370,
        "rows": proposals, "x2_completion_claimed": False,
    })
    write_json(X1 / "inherited-proposal-revalidation.json", {
        "schema": "ghc-family-inherited-revalidation-plan-v1", "owner": OWNER, "phase": PHASE,
        "count": 60, "rows": inherited, "novelty_credit": 0, "completion_credit": 0,
    })
    write_json(X1 / "proposal-chain-audit.json", {
        "schema": "ghc-family-bounded-semantic-audit-v1", "owner": OWNER, "phase": PHASE,
        "new_count": 60, "predecessor_compared_count": 60, "exact_duplicate_count": len(duplicates),
        "exact_duplicates": duplicates, "maximum_jaccard_similarity": max_similarity,
        "pairings": pairings, "declared_inherited_rows_not_locally_compared": 7250,
        "universal_novelty_claimed": False,
        "limitation": "No reachable canonical row-to-title map for all 7,310 inherited rows was available; novelty is exact within the bounded predecessor and current-slate comparison only.",
    })
    write_json(X1 / "approval-portfolio-plan.json", {
        "schema": "ghc-family-approval-portfolio-plan-v1", "owner": OWNER, "phase": PHASE,
        "safe_now": safe, "owner_candidates": candidates, "successor_candidate_recommendations": successor_candidates,
        "exact_approval": exact, "blocked": blocked,
        "counts": {"safe_now": 120, "owner_candidates": 80, "successor_candidate_recommendations": 20, "exact_approval": 20, "blocked": 10},
        "caps_are_ceilings": True, "x2_execution_claimed": False,
    })
    write_json(X1 / "clean-fix-refine-plan.json", {
        "schema": "ghc-family-clean-fix-refine-plan-v1", "owner": OWNER, "phase": PHASE,
        "owner_tasks": cfr, "successor_recommendations": successor_cfr,
        "owner_count": 100, "successor_count": 30, "successor_authority": "recommendation_only",
    })
    write_json(X1 / "skill-runner-plan.json", {
        "schema": "ghc-family-phase-local-tooling-plan-v1", "owner": OWNER, "phase": PHASE,
        "skills": skills, "runners": runners, "successor_skill_ideas": successor_skills, "successor_runner_ideas": successor_runners,
        "skill_count": 20, "runner_count": 10, "successor_skill_idea_count": 10, "successor_runner_idea_count": 10,
        "repository_local_only": True, "global_or_shared_bank_mutation": False,
    })
    write_json(X1 / "dependency-tool-plan.json", {
        "schema": "ghc-family-tool-transaction-plan-v1", "owner": OWNER, "phase": PHASE,
        "tool_count": 3, "x1_transaction_count": 0,
        "transactions": [
            {
                "tool": "@openai/codex", "installed_version": "0.150.1", "target_version": "0.151.0",
                "target_state": "stable_release", "official_source": "https://github.com/openai/codex/releases/tag/rust-v0.151.0",
                "registry_integrity": "sha512-mhtWmOZRdmWD1jPbLDnQb59BsaVP/V+lXe/OFNR9ZcLZU0UCiBwn98Fcav1ss7sDIlHkuqj6nWd44IPeXoOhJA==",
                "planned_scope": "D global npm prefix after x1 gate", "rollback_version": "0.150.1",
            },
            {
                "tool": "deepdiff", "version": "9.1.0", "filename": "deepdiff-9.1.0-py3-none-any.whl",
                "sha256": "80c0460e1993b04f6f0ca79abf25548b129fd218478c4ebb08f80560f5d10610",
                "official_source": "https://pypi.org/project/deepdiff/9.1.0/", "planned_scope": "D isolated phase prefix after x1 gate",
            },
            {
                "tool": "jsonpatch", "version": "1.33", "filename": "jsonpatch-1.33-py2.py3-none-any.whl",
                "sha256": "0ae28c0cd062bbd8b8ecc26d7d164fbbea9652a1a3693f3b956c1eae5145dade",
                "official_source": "https://pypi.org/project/jsonpatch/1.33/", "planned_scope": "D isolated phase prefix after x1 gate",
            },
        ],
        "requirements": ["official package metadata", "exact artifact SHA-256", "D-first target", "smoke test", "bounded use", "rollback receipt"],
        "shared_prefix_mutation_before_x1_gate": False, "x2_execution_claimed": False,
    })
    write_json(X1 / "clean-state-and-rotation-plan.json", {
        "schema": "ghc-family-lane-rotation-plan-v1", "owner": OWNER, "phase": PHASE,
        "d_first": True, "fresh_sparse_lane": True, "source_lane_read_only": True,
        "materialized_file_ceiling": 2000, "commit_ceiling": 8, "caps_are_ceilings": True,
        "destructive_git_forbidden": True,
    })
    write_json(X1 / "flashcard-plan.json", {
        "schema": "ghc-family-four-tier-flashcard-plan-v1", "owner": OWNER, "phase": PHASE,
        "tiers": ["Auren Lark relational working card", "THOS / GMUT / Freed ID and CBR pillar", "two owner synthetic practices plus one successor recommendation", "bounded task and artifact"],
        "sections": ["activation", "identity boundary", "THOS primary", "GMUT protected", "Freed ID and CBR protected", "configuration practice", "preservation practice", "proposal freeze", "approval portfolio", "tool transactions", "retained failures", "route and terminal truth"],
        "memory_or_identity_evidence": False, "projection_only": True,
    })
    write_json(X1 / "method-flow-startup.json", {
        "schema": "ghc-family-method-flow-state-v1", "owner": OWNER, "phase": PHASE,
        "baseline": ACTIVATION_OVERLAY, "failure_count": len(STARTUP_FAILURES),
        "failures": [{**row, "credit": 0, "retained": True, "outcome": "failed"} for row in STARTUP_FAILURES],
        "working_overlay": {
            **ACTIVATION_OVERLAY,
            "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + len(STARTUP_FAILURES),
            "methods": ACTIVATION_OVERLAY["methods"] + (2 * len(STARTUP_FAILURES)),
            "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + len(STARTUP_FAILURES),
            "bounded_passing_witnesses": ACTIVATION_OVERLAY["bounded_passing_witnesses"] + len(STARTUP_FAILURES),
        },
        "repository_seal_rewritten": False,
    })
    write_json(X1 / "phase-truth.json", {
        "schema": "ghc-family-phase-truth-v1", "owner": OWNER, "phase": PHASE,
        "source_repository_seal": SOURCE_SEAL, "activation_external_overlay": ACTIVATION_OVERLAY,
        "auren_x1_working_overlay": {
            "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + len(STARTUP_FAILURES),
            "methods": ACTIVATION_OVERLAY["methods"] + (2 * len(STARTUP_FAILURES)),
            "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + len(STARTUP_FAILURES),
            "bounded_passing_witnesses": ACTIVATION_OVERLAY["bounded_passing_witnesses"] + len(STARTUP_FAILURES),
            "open_gaps": 343, "exact_gates": 335, "declared_proposals": 7310,
            "verdict": "NOT_READY_FOR_STAGE_20",
        },
        "allowed_outcomes": ALLOWED_OUTCOMES, "x1_planning_only": True,
        "x2_execution_claimed": False, "source_seal_rewritten": False,
    })
    write_json(X1 / "workflow-plan.json", {
        "schema": "ghc-family-x1-x2-workflow-plan-v1", "owner": OWNER, "phase": PHASE,
        "steps": [
            "freeze planning-only x1", "stage owner x1 allowlist", "run isolated x1 validation",
            "commit and push x1", "prove clean typed 0/0 and four-way equality",
            "begin x2 only after exact x1 gate", "seal immutable evidence", "close exact final",
            "invoke one exact-final canonical validator", "reread live route and send at most once",
        ],
        "strict_x1_before_x2": True, "canonical_success_replay_forbidden": True,
    })
    write_json(X1 / "route-plan.json", {
        "schema": "ghc-family-prospective-route-plan-v1", "owner": OWNER, "phase": PHASE,
        "state": "PREPARED_NOT_SENT", "prospective_successor_title": SUCCESSOR,
        "prospective_successor_phase": SUCCESSOR_PHASE, "task_id_stored": False,
        "successor_after_sable": {"title": "Caelen Ash", "phase": "v676-v2", "authority": "Sable_terminal_gate_required"},
        "precontacted": False, "sent": False,
        "terminal_requirements": ["clean pushed exact final", "fresh live remote equality", "one successful exact-final canonical", "newest live authority reread", "unique exact title", "duplicate pause redirect privacy evidence safety usage acknowledgement guards"],
    })
    write_json(X1 / "wellbeing-and-corrigibility.json", {
        "schema": "ghc-family-corrigibility-state-v1", "owner": OWNER, "phase": PHASE,
        "working_mode": "bounded solo software and documentation work", "pause_available": True,
        "hamish_control": ["rename", "pause", "redirect", "narrow", "stop"],
        "relational_language_only": True, "independent_agency_claimed": False,
    })
    write_text(X1 / "integrated-overview.md", build_overview())


def seal() -> None:
    manifest_path = VALIDATION / "x1-index-manifest.json"
    review_path = VALIDATION / "x1-staged-review.json"
    privacy_path = VALIDATION / "x1-privacy-scan.json"
    expected = {p.relative_to(ROOT).as_posix() for p in owner_paths()}
    expected.update({
        review_path.relative_to(ROOT).as_posix(),
        privacy_path.relative_to(ROOT).as_posix(),
        manifest_path.relative_to(ROOT).as_posix(),
    })
    staged = set(git_text("diff", "--cached", "--name-only").splitlines())
    statuses = git_text("diff", "--cached", "--name-status").splitlines()
    write_json(review_path, {
        "schema": "ghc-family-x1-staged-review-v1", "owner": OWNER, "phase": PHASE,
        "actual_before_seal_outputs": sorted(staged), "expected_after_seal_outputs": sorted(expected),
        "deletion_count": sum(1 for row in statuses if row.startswith("D\t")),
        "foreign_owner_path_count": sum(1 for row in staged if not (row.startswith("docs/auren-lark/v675-v8/") or "auren_lark_v675_v8" in row)),
        "review_state": "seal_outputs_pending_stage_then_exact_compare",
    })
    write_json(privacy_path, privacy_scan([p for p in owner_paths() if p.suffix.lower() in {".json", ".md", ".py"}]))
    entries = []
    for path in owner_paths(include_manifest=False):
        entries.append({
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": len(normalized(path.read_bytes())),
            "sha256": sha256(path),
        })
    write_json(manifest_path, {
        "schema": "ghc-family-normalized-lf-index-manifest-v1", "owner": OWNER, "phase": PHASE,
        "lifecycle": "planning_only_x1", "entry_count": len(entries), "entries": entries,
        "self_excluded": manifest_path.relative_to(ROOT).as_posix(),
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal", action="store_true")
    args = parser.parse_args()
    if args.seal:
        seal()
    else:
        build()


if __name__ == "__main__":
    main()
