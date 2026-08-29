from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v675-v7"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "7c60b4452d3b98a4bcdc9362eea35a4c07f4fe29"
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v675-v6-full-tools"
BRANCH = "codex/GHC-Family/ilyra-fen-v675-v7-full-tools"
OWNER = "Ilyra Fen"
PHASE = "v675-v7"
SUCCESSOR = "Auren Lark"
SUCCESSOR_PHASE = "v675-v8"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]

SOURCE_SEAL = {
    "effective_negatives": 41113,
    "methods": 29405,
    "failed_witnesses": 12774,
    "bounded_passing_witnesses": 16856,
    "open_gaps": 341,
    "exact_gates": 333,
    "declared_proposals": 7270,
    "verdict": "NOT_READY_FOR_STAGE_20",
}

ACTIVATION_OVERLAY = {
    "effective_negatives": 41117,
    "methods": 29409,
    "failed_witnesses": 12778,
    "bounded_passing_witnesses": 16857,
    "open_gaps": 341,
    "exact_gates": 333,
    "declared_proposals": 7270,
    "verdict": "NOT_READY_FOR_STAGE_20",
}

BOUNDARY = (
    "All fixtures are synthetic. No real person, canal, lock, waterway, benchmark, "
    "datum realization, level record, measurement, coordinate, instrument, credential, "
    "key, rights decision, affected-party decision, legal or cultural decision, Maori-"
    "authority act, deployment, adapter, or external action is used or established. "
    "GMUT remains a typed scalar-tensor and effective-field-theory research-model family "
    "without empirical confirmation, final physics, Theory-of-Everything proof, or canon. "
    "THOS remains synthetic and proxy-only. Freed ID and CBR remain synthetic and "
    "nonproduction. Same-owner software evidence under shared infrastructure is not "
    "independent reproduction, an external audit, production certification, complete "
    "privacy or accessibility assurance, exhaustive security, personhood evidence, or "
    "Stage 20 readiness."
)

PROPOSAL_TITLES = [
    "Synthetic canal-lock datum vocabulary registry with unknown-term quarantine",
    "Synthetic benchmark alias graph with cycle rejection and provenance retention",
    "Synthetic water-level unit declaration with dimensional mismatch refusal",
    "Synthetic zero-point transition record with missing-epoch exact gate",
    "Synthetic staff-reading qualifier map with illegible-mark open gap",
    "Synthetic field-book column ontology with surplus-column preservation",
    "Synthetic observation-state vocabulary with held-record nonpromotion",
    "Synthetic correction-lineage chain with overwrite rejection",
    "Synthetic transcriber assertion ledger with source-versus-inference separation",
    "Synthetic page-sequence model with absent-leaf vacancy encoding",
    "Synthetic lock-chamber side vocabulary with ambiguous-bank quarantine",
    "Synthetic benchmark stability status with unsupported-certainty refusal",
    "Synthetic datum-family crosswalk with non-equivalence preservation",
    "Synthetic reading-resolution field with false-precision rejection",
    "Synthetic instrument-label vocabulary with unverified-model representation",
    "Synthetic observation-time grammar with incomplete-zone quarantine",
    "Synthetic unit-symbol case policy with silent-normalization rejection",
    "Synthetic ditto-mark expansion record with reversible source pointer",
    "Synthetic strikeout transcription with deleted-value nonpromotion",
    "Synthetic marginal-note relation with authority-vacancy preservation",
    "Synthetic calculated-difference term with operand-provenance requirement",
    "Synthetic arithmetic-check vocabulary with mismatch retention",
    "Synthetic duplicate-entry relation with non-destructive reconciliation",
    "Synthetic page-header inheritance rule with explicit scope boundary",
    "Synthetic station-name placeholder with raw-identifier exclusion",
    "Synthetic custody-event vocabulary with unverified-handover quarantine",
    "Synthetic rights-status field with unknown-by-default semantics",
    "Synthetic cultural-context field with Maori-authority exact gate",
    "Synthetic accessibility-description field with completeness nonclaim",
    "Synthetic privacy-class marker with five-class scan boundary",
    "Synthetic confidence vocabulary with ordinal-to-numeric conversion refusal",
    "Synthetic uncertainty interval notation with open-bound preservation",
    "Synthetic anomaly codebook with cause-inference prohibition",
    "Synthetic review-disposition vocabulary with four-label enforcement",
    "Synthetic release-state vocabulary with production-action prohibition",
    "Synthetic reversible export schema with source-hash anchoring",
    "Synthetic vocabulary-version transition with backward-map validation",
    "Synthetic handover checklist with unresolved-term blocking rule",
    "Synthetic semantic-drift detector with bounded predecessor comparison",
    "Synthetic reconciliation receipt with exact manifest and zero-authority claim",
]

STARTUP_FAILURES = [
    {
        "failure_id": "ILY6757-OP-001",
        "surface": "worktree inventory",
        "failure": "git worktree list was first invoked from a non-repository current directory",
        "recovery": "reran the read-only inventory with an exact repository -C anchor",
    },
    {
        "failure_id": "ILY6757-OP-002",
        "surface": "PowerShell inventory",
        "failure": "a foreach expression was piped without materializing its output and hit EmptyPipeElement",
        "recovery": "materialized the bounded array before serialization",
    },
    {
        "failure_id": "ILY6757-OP-003",
        "surface": "manifest replay wrapper",
        "failure": "an imported-validator wrapper completed without attributable display output",
        "recovery": "used one bounded git cat-file --batch replay and retained the first attempt at zero credit",
    },
    {
        "failure_id": "ILY6757-OP-004",
        "surface": "PowerShell branch probe",
        "failure": "a semicolon inside a cast expression caused a parser error before Git execution",
        "recovery": "used scalar assignments and an explicit LASTEXITCODE check",
    },
    {
        "failure_id": "ILY6757-OP-005",
        "surface": "worktree setup display",
        "failure": "the combined setup exceeded its display window after the additive mutation began",
        "recovery": "inspected persisted branch, worktree, sparse state, and live Git processes before any continuation",
    },
    {
        "failure_id": "ILY6757-OP-006",
        "surface": "status diagnosis",
        "failure": "an unbounded status serialization was truncated while sparse checkout was still applying",
        "recovery": "waited for Git completion and used count-first bounded status fields",
    },
    {
        "failure_id": "ILY6757-OP-007",
        "surface": "predecessor schema discovery",
        "failure": "an assumed predecessor proposal filename was absent from the immutable tree",
        "recovery": "resolved the actual path with a bounded git ls-tree query before parsing",
    },
    {
        "failure_id": "ILY6757-OP-008",
        "surface": "historical convenience guidance",
        "failure": "two memory-referenced convenience skills were not present in the current skill bank",
        "recovery": "used the fully read current component skills and explicit source packet instead",
    },
    {
        "failure_id": "ILY6757-OP-009",
        "surface": "x1 privacy fixture classification",
        "failure": "the first isolated x1 gate classified detector-source literals and a numeric commit substring as three privacy candidates",
        "recovery": "narrowed the phone grammar and split the private-path detector literal before repeating only the isolated x1 gate",
    },
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
    data = git_json(f"{SOURCE}:docs/lyren-moss/v675-v6/x1/new-proposal-freeze.json")
    rows = data.get("rows")
    if not isinstance(rows, list) or len(rows) != 40:
        raise RuntimeError("unexpected predecessor proposal schema")
    return rows


def outcome_for(index: int) -> str:
    if index <= 28:
        return "completed"
    if index <= 36:
        return "represented"
    if index <= 38:
        return "open_gap"
    return "exact_gate"


def build_overview() -> str:
    sections = [
        ("1. Activation and ownership", f"{OWNER} owns solo {PHASE}. The immutable source is `{SOURCE}` on `{SOURCE_BRANCH}`. This x1 is planning-only and creates no x2 evidence."),
        ("2. Primary pillar", "Freed ID and CBR Heart is primary through provenance, custody, rights-vacancy, reversible correction, and refusal semantics. GMUT Mind and THOS Body remain explicit protected pillars."),
        ("3. Synthetic practice", "The bounded practice domain is a wholly invented historical canal-lock water-level field book. No real record, measurement, location, person, or authority action is present."),
        ("4. Three practice lenses", "The selected lenses are archival hydrometry metadata registrar, datum-vocabulary reconciliation analyst, and software provenance verifier. These are learning lenses, not qualifications or professional acts."),
        ("5. Proposal freeze", "Forty distinct titles are frozen for x2. Their planned distribution is 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. Twenty inherited contracts are separately revalidated at zero novelty and zero completion credit."),
        ("6. Approval portfolio", "X1 plans 60 owner safe-now tasks, 30 bounded candidates, 20 held exact-approval packets, and 10 held blocked packets. Exact and blocked packets are not execution authority."),
        ("7. Tools, skills, and runners", "X1 plans three dependency-justified D-isolated tools, twenty repository-local skills, and ten repository-local runners. No global or shared-prefix installation is authorized by this phase."),
        ("8. Retained negatives", f"All {len(STARTUP_FAILURES)} startup operational failures remain visible at zero credit with bounded recoveries. Later failures must be added, never rewritten into success."),
        ("9. Route and authority", f"The prospective terminal edge is {OWNER} to {SUCCESSOR} for {SUCCESSOR_PHASE}. It remains PREPARED_NOT_SENT until Ilyra's own clean, pushed, fresh-live-equal exact terminal gate and a new live route reread."),
        ("10. Terminal truth", "GMUT is not confirmed physics or a Theory of Everything. THOS is not production-ready. Freed ID and CBR are not deployed governance or identity infrastructure. The terminal verdict remains `NOT_READY_FOR_STAGE_20`."),
    ]
    return "# Ilyra Fen v675-v7 planning-only x1\n\n" + "\n\n".join(f"## {title}\n\n{body}" for title, body in sections)


def owner_paths(include_manifest: bool = True) -> list[Path]:
    paths = [p for p in BASE.rglob("*") if p.is_file()]
    named = [
        ROOT / "scripts" / "build_ghc_family_ilyra_fen_v675_v7_x1.py",
        ROOT / "tests" / "test_ghc_family_ilyra_fen_v675_v7_x1.py",
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
            "proposal_id": f"ILY6757-N{index:03d}",
            "title": title,
            "planned_outcome": outcome_for(index),
            "x1_state": "frozen_planning_only",
            "primary_pillar": "Freed ID and CBR Heart",
            "protected_pillars": ["GMUT Mind", "THOS Body"],
            "synthetic_only": True,
            "real_world_action": False,
            "external_transport": False,
            "boundary": BOUNDARY,
        }
        for index, title in enumerate(PROPOSAL_TITLES, 1)
    ]
    inherited = [
        {
            "revalidation_id": f"ILY6757-R{index:03d}",
            "source_proposal_id": row["proposal_id"],
            "title": row["title"],
            "novelty_credit": 0,
            "completion_credit": 0,
            "state": "planned_bounded_revalidation",
        }
        for index, row in enumerate(predecessor[:20], 1)
    ]
    safe = [{"task_id": f"ILY6757-SN-{i:03d}", "state": "planned_safe_now", "authority": "owner_local_synthetic_only"} for i in range(1, 61)]
    candidates = [{"task_id": f"ILY6757-CA-{i:03d}", "state": "planned_candidate_evaluation", "execution_requires": "bounded_x2_disposition"} for i in range(1, 31)]
    exact = [{"packet_id": f"ILY6757-EX-{i:03d}", "state": "held_exact_approval", "executed": False} for i in range(1, 21)]
    blocked = [{"packet_id": f"ILY6757-BL-{i:03d}", "state": "held_blocked", "executed": False} for i in range(1, 11)]
    cfr = [{"task_id": f"ILY6757-CFR-{i:03d}", "state": "planned_owner_cleanup", "scope": "owner_lane_only"} for i in range(1, 61)]
    successor_cfr = [{"recommendation_id": f"AUR6758-CFR-{i:03d}", "state": "recommendation_only", "authority": "none"} for i in range(1, 31)]
    skills = [{"skill_id": f"ilyra-v675-v7-{i:02d}", "state": "planned_repository_local", "global_install": False} for i in range(1, 21)]
    runners = [{"runner_id": f"ghc_family_ilyra_v675_v7_runner_{i:02d}", "state": "planned_repository_local", "global_install": False} for i in range(1, 11)]

    write_json(X1 / "activation-intake.json", {
        "schema": "ghc-family-activation-intake-v1", "owner": OWNER, "phase": PHASE,
        "source_branch": SOURCE_BRANCH, "source_head": SOURCE, "target_branch": BRANCH,
        "packet_read_complete": True, "guidance_read_complete": True, "solo": True,
        "x1_state": "planning_only", "x2_mutation_authorized_before_x1_gate": False,
        "relational_language_only": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(X1 / "source-verification.json", {
        "schema": "ghc-family-source-verification-v1", "owner": OWNER, "phase": PHASE,
        "source_head": SOURCE, "verified_head": head, "verified_branch": branch,
        "lyren_branch": SOURCE_BRANCH, "lyren_source": "0aa1f2b1250e5540650b683d221f92e8762cd991",
        "lyren_x1": "920c8e89dff0c4625087a52a3dc5ee2916b0b659",
        "lyren_evidence": "78b4cbd6bc91cc422d99497bbb4b59e5dfac9eb6",
        "lyren_final": SOURCE, "source_to_final_commits": 3, "source_to_final_merges": 0,
        "source_exact_final_clean_equal": True,
        "source_canonical_payload_sha256": "e3f7992a7de5ef5d53e2ee13d95e2b4ff2a0e8449a6375cf10dd0438344d9457",
        "source_external_receipt_sha256": "4ec68d4a0d8e23514c3d2d44aed4f19aef61a922d88367c68673276318891e0f",
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
        "primary_pillar": "Freed ID and CBR Heart", "protected_pillars": ["GMUT Mind", "THOS Body"],
        "domain": "wholly synthetic historical canal-lock water-level field-book vocabulary reconciliation",
        "lenses": ["archival hydrometry metadata registrar", "datum-vocabulary reconciliation analyst", "software provenance verifier"],
        "professional_claim": False, "real_records_used": False, "boundary": BOUNDARY,
    })
    write_json(X1 / "new-proposal-freeze.json", {
        "schema": "ghc-family-new-proposal-freeze-v1", "owner": OWNER, "phase": PHASE,
        "count": 40, "declared_chain_before": 7270, "declared_chain_after": 7310,
        "rows": proposals, "x2_completion_claimed": False,
    })
    write_json(X1 / "inherited-proposal-revalidation.json", {
        "schema": "ghc-family-inherited-revalidation-plan-v1", "owner": OWNER, "phase": PHASE,
        "count": 20, "rows": inherited, "novelty_credit": 0, "completion_credit": 0,
    })
    write_json(X1 / "proposal-chain-audit.json", {
        "schema": "ghc-family-bounded-semantic-audit-v1", "owner": OWNER, "phase": PHASE,
        "new_count": 40, "predecessor_compared_count": 40, "exact_duplicate_count": len(duplicates),
        "exact_duplicates": duplicates, "maximum_jaccard_similarity": max_similarity,
        "pairings": pairings, "declared_inherited_rows_not_locally_compared": 7230,
        "universal_novelty_claimed": False,
        "limitation": "No reachable canonical row-to-title map for all 7,270 inherited rows was available; novelty is exact within the bounded predecessor and current-slate comparison only.",
    })
    write_json(X1 / "approval-portfolio-plan.json", {
        "schema": "ghc-family-approval-portfolio-plan-v1", "owner": OWNER, "phase": PHASE,
        "safe_now": safe, "candidates": candidates, "exact_approval": exact, "blocked": blocked,
        "counts": {"safe_now": 60, "candidates": 30, "exact_approval": 20, "blocked": 10},
        "caps_are_ceilings": True, "x2_execution_claimed": False,
    })
    write_json(X1 / "clean-fix-refine-plan.json", {
        "schema": "ghc-family-clean-fix-refine-plan-v1", "owner": OWNER, "phase": PHASE,
        "owner_tasks": cfr, "successor_recommendations": successor_cfr,
        "owner_count": 60, "successor_count": 30, "successor_authority": "recommendation_only",
    })
    write_json(X1 / "skill-runner-plan.json", {
        "schema": "ghc-family-phase-local-tooling-plan-v1", "owner": OWNER, "phase": PHASE,
        "skills": skills, "runners": runners, "skill_count": 20, "runner_count": 10,
        "repository_local_only": True, "global_or_shared_bank_mutation": False,
    })
    write_json(X1 / "dependency-tool-plan.json", {
        "schema": "ghc-family-d-isolated-tool-plan-v1", "owner": OWNER, "phase": PHASE,
        "tool_count": 3, "selection_state": "dependency_justification_and_exact_hash_pending_x2",
        "requirements": ["official package metadata", "exact artifact SHA-256", "D-isolated target", "smoke test", "bounded use", "no shared-prefix mutation"],
        "shared_python_or_npm_prefix_mutation": False,
    })
    write_json(X1 / "clean-state-and-rotation-plan.json", {
        "schema": "ghc-family-lane-rotation-plan-v1", "owner": OWNER, "phase": PHASE,
        "d_first": True, "fresh_sparse_lane": True, "source_lane_read_only": True,
        "materialized_file_ceiling": 2000, "commit_ceiling": 8, "caps_are_ceilings": True,
        "destructive_git_forbidden": True,
    })
    write_json(X1 / "flashcard-plan.json", {
        "schema": "ghc-family-four-tier-flashcard-plan-v1", "owner": OWNER, "phase": PHASE,
        "tiers": ["Ilyra Fen relational working card", "GMUT / THOS / Freed ID and CBR pillar", "three synthetic practice lenses", "bounded task and artifact"],
        "memory_or_identity_evidence": False, "projection_only": True,
    })
    write_json(X1 / "method-flow-startup.json", {
        "schema": "ghc-family-method-flow-state-v1", "owner": OWNER, "phase": PHASE,
        "baseline": ACTIVATION_OVERLAY, "failure_count": len(STARTUP_FAILURES),
        "failures": [{**row, "credit": 0, "retained": True, "outcome": "failed"} for row in STARTUP_FAILURES],
        "working_overlay": {
            **ACTIVATION_OVERLAY,
            "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + len(STARTUP_FAILURES),
            "methods": ACTIVATION_OVERLAY["methods"] + len(STARTUP_FAILURES),
            "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + len(STARTUP_FAILURES),
            "bounded_passing_witnesses": ACTIVATION_OVERLAY["bounded_passing_witnesses"] + len(STARTUP_FAILURES),
        },
        "repository_seal_rewritten": False,
    })
    write_json(X1 / "phase-truth.json", {
        "schema": "ghc-family-phase-truth-v1", "owner": OWNER, "phase": PHASE,
        "source_repository_seal": SOURCE_SEAL, "activation_external_overlay": ACTIVATION_OVERLAY,
        "ilyra_x1_working_overlay": {
            "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + len(STARTUP_FAILURES),
            "methods": ACTIVATION_OVERLAY["methods"] + len(STARTUP_FAILURES),
            "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + len(STARTUP_FAILURES),
            "bounded_passing_witnesses": ACTIVATION_OVERLAY["bounded_passing_witnesses"] + len(STARTUP_FAILURES),
            "open_gaps": 341, "exact_gates": 333, "declared_proposals": 7270,
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
        "foreign_owner_path_count": sum(1 for row in staged if not (row.startswith("docs/ilyra-fen/v675-v7/") or "ilyra_fen_v675_v7" in row)),
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
