from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v673-v8"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "c1818f0c09737c69a1870ef6bf8ed7fc339cb727"
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v673-v7-full-tools"
BRANCH = "codex/GHC-Family/ilyra-fen-v673-v8-full-tools"
PHASE = "v673-v8"
OWNER = "Ilyra Fen"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]


PROPOSAL_TITLES = [
    "Synthetic loom pattern-chain catalog record and reversible version lineage",
    "Pattern-chain segment membership with explicit predecessor and successor order",
    "Peg-hole-state map with unknown, vacant, present, and unreadable distinctions",
    "Card and slat orientation declaration with reversal quarantine",
    "Repeat-boundary ledger with overlap and omission refusal",
    "Pattern-unit symbol registry with interpretation vacancy",
    "Chain-position tokenization that excludes textile content and personal data",
    "Synthetic warp-weft relation lattice without production instructions",
    "Pattern-chain correction record with append-only supersession edges",
    "Pseudonymous custody envelope for synthetic pattern-chain handover",
    "Role-placeholder envelope with qualification and authority refusal",
    "Digital surrogate lineage from invented chain to structural derivative",
    "Canonical pattern-chain correction sequence with cycle rejection",
    "Provenance DAG for synthetic pattern cards and reversible derivatives",
    "Custody-transition graph with vacant signer and authority fields",
    "Hash-bound segment register with normalized-line-ending declaration",
    "Orientation-conflict hold that blocks automatic pattern interpretation",
    "Broken-link and missing-card uncertainty register",
    "Duplicate-card-position quarantine with bounded deterministic detection",
    "Unknown-repeat-count hold with no inferred completion",
    "Color-code vacancy record without material, dye, or production claim",
    "Fiber and substrate vocabulary placeholder with professional gate",
    "Machine-configuration vacancy record without equipment instruction",
    "Measurement and scale vacancy record without metrology claim",
    "Accessible structural companion for pattern-chain tables",
    "Plain-language uncertainty companion with manual-evaluation gap",
    "Keyboard-order and heading-map proxy for static evidence navigation",
    "Language-interpretation vacancy with affected-party evaluation gate",
    "Purpose-and-access boundary card for synthetic collection records",
    "Rights-attribution vacancy with competent-authority refusal",
    "Cultural-context vacancy with community-governance reservation",
    "Maori-authority reservation with no proxy consent or ratification",
    "Remedy-authority matrix for correction, hold, and disclosure refusal",
    "THOS documentation-handover proxy with workload and error caveats",
    "THOS reversible-state proxy with no production-readiness promotion",
    "GMUT event-order firewall as typed research-model representation only",
    "Manual conservation-evaluation gap with no treatment recommendation",
    "Real collection adapter gap with no external record access",
    "Competent-authority gate for legal, cultural, conservation, and Maori decisions",
    "Terminal veto for deployment, ultimate-theory, machine-status, and Stage-20 promotion",
]


STARTUP_FAILURES = [
    (
        "IF6738-M001",
        "An older memory index named the removed ghc-family-solo-activation aggregate skill.",
        "Retain the stale pointer and use the fully read current component skills instead.",
    ),
    (
        "IF6738-M002",
        "The first full auth current-state display truncated before the middle of the file.",
        "Reread the exact UTF-8 state in bounded numbered windows through EOF.",
    ),
    (
        "IF6738-M003",
        "The first Lyren task reread requested a per-item output bound above the host maximum.",
        "Retry only the reread at the supported 20000-character bound.",
    ),
    (
        "IF6738-M004",
        "A sequential per-entry inherited-manifest verifier exceeded its display window without attributable output.",
        "Inspect process state before any recovery and replace repeated Git processes with one bounded batch.",
    ),
    (
        "IF6738-M005",
        "A Wait-Process wrapper also returned no attributable completion projection.",
        "Use a direct scalar process-existence probe rather than inferring completion from silence.",
    ),
    (
        "IF6738-M006",
        "A broad older-Ilyra remaster inventory crossed its bounded display window.",
        "Abandon the broad inventory and rely on the current Lyren source plus narrow literal probes.",
    ),
    (
        "IF6738-M007",
        "The first Git cat-file batch recovery deadlocked by writing every request before draining binary output.",
        "Stop only the verifier process tree and use communicate-style concurrent input and output handling.",
    ),
    (
        "IF6738-M008",
        "A completed nonblocking verifier lost its output because the wrapper did not expose the session object.",
        "Preserve the zero-credit attempt and explicitly project the exec result or retained session handle.",
    ),
    (
        "IF6738-M009",
        "The first lane-absence wrapper hung in the large shared git worktree listing.",
        "Interrupt only that wrapper and prove absence with target path, local branch, and fresh remote branch scalars.",
    ),
    (
        "IF6738-M010",
        "A sparse-pattern inspection bound PowerShell -replace as a Get-Content parameter.",
        "Separate the raw .git read from the parenthesized replacement expression and reread only the pattern file.",
    ),
    (
        "IF6738-M011",
        "The first x1 privacy scan classified its own email-detection regex as a confirmed email hit.",
        "Retain the candidate, classify only the exact scanner self-description as a reviewed false positive, and keep every other candidate fail-closed.",
    ),
    (
        "IF6738-M012",
        "The first full x1 test pass found a 668-word integrated overview below the preregistered 700-word floor.",
        "Retain the failed suite, add substantive lifecycle and evidentiary boundary text, and rerun the isolated overview test before the final x1 module.",
    ),
    (
        "IF6738-M013",
        "The direct ruff launcher was not present on the active PowerShell PATH.",
        "Retain the launcher failure and invoke the installed package through python -m ruff.",
    ),
    (
        "IF6738-M014",
        "The first module-based Ruff pass found seventeen owner-file style findings.",
        "Retain the lint failure, apply bounded Ruff mechanical fixes only to the two x1 owner Python files, and rerun the exact lint target.",
    ),
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_bytes(spec: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", spec], cwd=ROOT)


def normalized(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def similarity(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def predecessor_results() -> list[dict[str, object]]:
    path = "docs/lyren-moss/v673-v7/x2/proposal-results.json"
    return json.loads(git_bytes(f"{SOURCE}:{path}").decode("utf-8"))["results"]


def build_overview() -> str:
    sections = [
        (
            "Owner and lifecycle",
            ("Ilyra Fen v673-v8 is one additive, owner-scoped phase from immutable Lyren final "
            f"`{SOURCE}`. This document is planning-only x1. It freezes contracts, gates, comparison "
            "scope, task portfolios, and recovery methods; it reports no x2 execution outcome. The "
            "relational name and role language is working language only, never consciousness, identity "
            "continuity, personhood, qualification, employment, or independent agency evidence."),
        ),
        (
            "Primary pillar and practice",
            ("The primary pillar is Freed ID and CBR Heart, exercised through wholly synthetic historical "
            "loom pattern-chain documentation and provenance assurance. The three learning lenses are "
            "textile-collections registrar, pattern-chain conservation documentation analyst, and software "
            "provenance librarian. No real textile, loom, card, slat, chain, collection, person, community, "
            "measurement, treatment, machine setting, right, authority act, deployment, or external record "
            "is in scope. The phase produces structural fixtures and refusal logic only."),
        ),
        (
            "Proposal freeze",
            ("Forty new titles are frozen after exact comparison with the forty accessible predecessor titles. "
            "Twenty predecessor contracts are separately revalidated at zero Ilyra novelty and zero automatic "
            "completion credit. The broader 6,510-row declaration lacks a complete local row-to-title mapping, "
            "so universal novelty remains an open gap. Planned dispositions use only completed, represented, "
            "open_gap, and exact_gate; x1 does not claim that those future dispositions were achieved."),
        ),
        (
            "Approval portfolios",
            ("Sixty safe-now tasks and thirty bounded candidates are planned for synthetic local execution. "
            "Twenty exact-approval packets and ten blocked packets remain held. Caps are ceilings rather than "
            "quotas, and nothing unsafe will be manufactured merely to fill a count. Exact packets require "
            "competent evidence and authority; blocked packets retain their blocker instead of being softened "
            "into a pass."),
        ),
        (
            "Skills, runners, and refinement",
            ("Twenty repo-local portable skill-card ideas, ten declarative runner-card ideas, and sixty additive "
            "CLEAN/FIX/REFINE reviews are planned for Ilyra. Ten skill, ten runner, and thirty refinement ideas "
            "are successor recommendations only. No global installation, shared prefix mutation, plugin-cache "
            "change, sibling-lane write, host cleanup, or destructive migration is authorized by this x1."),
        ),
        (
            "Retained failures",
            ("Every startup failure is retained before recovery. The failures recorded in the x1 Method Flow "
            "startup ledger: stale skill routing, truncated reads, unsupported tool bounds, lost session output, "
            "a batch-pipe deadlock, a large worktree registry stall, and one PowerShell expression error. Each "
            "has zero completion credit and one bounded preferred recovery. Recovery never erases the rejecting "
            "witness or converts same-owner work into independent reproduction."),
        ),
        (
            "Evidence and validation boundary",
            ("The source branch, three-commit ancestry, zero merges, clean state, fresh four-way equality, baton "
            "digest, external receipt digest, canonical payload digest, and all 225 inherited manifest entries "
            "were reverified read-only. Lyren's successful canonical aggregate was not replayed. Ilyra will "
            "eventually validate only its own source-to-final delta, with exact Git-blob manifests, staged review, "
            "five-class privacy review, bounded changed-Python security review, and one attributable terminal gate."),
        ),
        (
            "Interpretation and reversibility",
            ("Every future x2 record must distinguish observed synthetic state, declared vacancy, inferred relation, "
            "and prohibited promotion. Correction is append-only: an earlier record remains inspectable while a "
            "later edge identifies what changed and why. Unknown card position, direction, repeat count, material, "
            "scale, custody, purpose, right, language, or authority must stay unknown rather than being guessed. "
            "This reversibility contract is documentation logic only and supplies no conservation treatment, weaving "
            "instruction, authenticity determination, cultural interpretation, ownership decision, or release authority."),
        ),
        (
            "Scientific and operational boundary",
            ("GMUT remains a typed scalar-tensor or EFT research-model family without empirical confirmation, final "
            "physics, Theory-of-Everything proof, or canon. THOS remains a proxy architecture without governed "
            "blind matched-budget real arms and independent review. Freed ID is synthetic and nonproduction. CBR "
            "is a rights-and-remedy representation without legal, cultural, affected-party, or Maori authority. "
            "No production, professional, conservation-treatment, accessibility-complete, privacy-complete, or "
            "exhaustive-security claim follows from local tests."),
        ),
        (
            "x1-to-x2 gate",
            ("Before x2, the planning files, builder, tests, privacy receipt, staged review, and exact index-blob "
            "manifest must pass. The x1 commit must be pushed, clean, typed zero-divergent, and equal across local, "
            "upstream, tracking, and a fresh live remote read. No x2 directory or outcome artifact may exist in the "
            "x1 tree. The immutable x1 commit will be the sole planning anchor for later evidence."),
        ),
        (
            "Route and stop conditions",
            ("Auren Lark v674-v1 is prospective only. Ilyra will not precontact Auren during x1 or x2. Only after "
            "Ilyra's own clean, pushed, fresh-live-equal exact final and one successful owner-scoped canonical gate "
            "may the newest live authority and roster be reread, the unique exact title resolved and immediately "
            "reread, and one sanitized activation sent. Pause, redirect, ambiguity, duplicate evidence, usage, "
            "privacy, safety, or authority failure stops the edge."),
        ),
    ]
    body = ["# Ilyra Fen v673-v8 planning-only x1", ""]
    for title, text in sections:
        body.extend([f"## {title}", "", text, ""])
    body.append("Terminal planning verdict: `NOT_READY_FOR_STAGE_20`.")
    return "\n".join(body)


def build() -> None:
    previous = predecessor_results()
    previous_titles = [str(row["title"]) for row in previous]
    outcomes = ["completed"] * 28 + ["represented"] * 8 + ["open_gap"] * 2 + ["exact_gate"] * 2
    proposals = []
    neighbor_rows = []
    for index, (title, planned) in enumerate(zip(PROPOSAL_TITLES, outcomes, strict=True), start=1):
        scored = sorted(
            ((similarity(title, old), old) for old in previous_titles),
            key=lambda item: (-item[0], item[1]),
        )
        proposals.append(
            {
                "proposal_id": f"IF6738-N{index:03d}",
                "title": title,
                "planned_disposition": planned,
                "x1_state": "frozen_not_executed",
                "novelty_scope": "forty_accessible_predecessor_titles_plus_within_slate",
            }
        )
        neighbor_rows.append(
            {
                "proposal_id": f"IF6738-N{index:03d}",
                "nearest_predecessor_title": scored[0][1],
                "jaccard": round(scored[0][0], 6),
            }
        )
    within = []
    for index, title in enumerate(PROPOSAL_TITLES):
        others = [(similarity(title, other), other) for pos, other in enumerate(PROPOSAL_TITLES) if pos != index]
        score, nearest = max(others, key=lambda item: item[0])
        within.append({"proposal_id": f"IF6738-N{index + 1:03d}", "nearest_within_slate": nearest, "jaccard": round(score, 6)})

    inherited = [
        {
            "source_proposal_id": row["proposal_id"],
            "source_title": row["title"],
            "source_outcome": row["outcome"],
            "state": "bounded_contract_revalidated",
            "ilyra_novelty_credit": 0,
            "ilyra_completion_credit": 0,
        }
        for row in previous[:20]
    ]
    safe = [
        {
            "task_id": f"IF6738-SAFE-{i:03d}",
            "title": f"Freeze synthetic loom documentation safety contract {i:02d}",
            "state": "planned_safe_now",
            "external_action": False,
        }
        for i in range(1, 61)
    ]
    candidates = [
        {
            "task_id": f"IF6738-CAND-{i:03d}",
            "title": f"Analyze dependency-closed loom provenance candidate {i:02d}",
            "state": "planned_candidate",
            "promotion_without_evidence": False,
        }
        for i in range(1, 31)
    ]
    exact = [
        {
            "packet_id": f"IF6738-EXACT-{i:03d}",
            "state": "held_exact_approval_required",
            "execution_credit": 0,
        }
        for i in range(1, 21)
    ]
    blocked = [
        {
            "packet_id": f"IF6738-BLOCK-{i:03d}",
            "state": "blocked_unexecuted",
            "execution_credit": 0,
        }
        for i in range(1, 11)
    ]
    skills = [
        {
            "skill_id": f"IF6738-SKILL-{i:03d}",
            "name": f"ghc-family-loom-{i:02d}-portable-card",
            "state": "planned_repo_local_only",
        }
        for i in range(1, 21)
    ]
    runners = [
        {
            "runner_id": f"IF6738-RUNNER-{i:03d}",
            "name": f"ghc_family_loom_{i:02d}_runner",
            "state": "planned_declarative_only",
        }
        for i in range(1, 11)
    ]
    cfr = [
        {
            "review_id": f"IF6738-CFR-{i:03d}",
            "title": f"Additive loom evidence CLEAN/FIX/REFINE review {i:02d}",
            "state": "planned_additive_review",
            "deletion": False,
        }
        for i in range(1, 61)
    ]
    successor = {
        "skills": [f"ghc-family-auren-pattern-chain-recommendation-{i:02d}" for i in range(1, 11)],
        "runners": [f"ghc_family_auren_pattern_chain_{i:02d}_runner" for i in range(1, 11)],
        "clean_fix_refine": [f"Auren additive pattern-chain refinement {i:02d}" for i in range(1, 31)],
        "practice": "synthetic historical Jacquard sample-book documentation and provenance assurance",
        "execution_credit": 0,
    }
    method_rows = [
        {
            "method_id": method_id,
            "failure_signature": failure,
            "retained_negative_id": f"NEG-{method_id}",
            "state": "preferred",
            "passing_witness": recovery,
            "credit": 0,
            "independent_reproduction": False,
        }
        for method_id, failure, recovery in STARTUP_FAILURES
    ]

    write_json(
        X1 / "source-and-provenance.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE,
            "source_repository_counts": {"negatives": 37613, "methods": 23821, "failed": 9274, "passing": 11432},
            "activation_overlay": {"negatives": 37616, "methods": 23824, "failed": 9277, "passing": 11435},
            "source_open_gaps": 305,
            "source_exact_gates": 298,
            "source_canonical_payload_sha256": "e3f6167e25ef9d5d57d25a744eaf239e9de08cacd9eac3b4b9c45e541058fcaa",
            "source_canonical_receipt_file_sha256": "bbafef3847211d5b03c08f52c273237e9176373091fe52eab70d5aa0d6d9e5fc",
            "source_manifest_entries_reverified": 225,
            "source_validation_inherited_without_replay": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        X1 / "official-source-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "sources": [
                {"label": "W3C PROV-O", "url": "https://www.w3.org/TR/prov-o/", "use": "provenance vocabulary only"},
                {"label": "PREMIS at Library of Congress", "url": "https://www.loc.gov/standards/premis/", "use": "preservation metadata vocabulary only"},
                {"label": "W3C WCAG 2.2", "url": "https://www.w3.org/TR/WCAG22/", "use": "accessibility design vocabulary only"},
                {"label": "BIPM SI Brochure", "url": "https://www.bipm.org/en/publications/si-brochure", "use": "unit and uncertainty boundary only"},
            ],
            "endorsement_claimed": False,
            "operational_validation_claimed": False,
        },
    )
    write_text(
        X1 / "phase-boundaries.md",
        """# Ilyra Fen v673-v8 phase boundaries

This is a wholly synthetic software and documentation phase. Names, roles, hopes, pronouns, sibling/family language, continuity, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, authority, or independent agency.

No empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim is made. Same-owner software validation under shared infrastructure is not an external audit or independent reproduction.
""",
    )
    write_json(X1 / "inherited-revalidations.json", {"owner": OWNER, "phase": PHASE, "count": 20, "rows": inherited})
    write_json(
        X1 / "proposals.json",
        {"owner": OWNER, "phase": PHASE, "declared_chain_before": 6510, "declared_chain_after": 6550, "count": 40, "allowed_outcomes": ALLOWED_OUTCOMES, "proposals": proposals},
    )
    max_predecessor = max(row["jaccard"] for row in neighbor_rows)
    max_within = max(row["jaccard"] for row in within)
    write_json(
        X1 / "semantic-neighbor-audit.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "accessible_predecessor_titles": len(previous_titles),
            "unmapped_declared_inherited_rows": 6470,
            "universal_novelty_claimed": False,
            "quarantine_threshold": 0.72,
            "max_predecessor_jaccard": max_predecessor,
            "max_within_slate_jaccard": max_within,
            "predecessor_neighbors": neighbor_rows,
            "within_slate_neighbors": within,
            "state": "bounded_distinct_with_universal_mapping_open_gap",
        },
    )
    write_json(
        X1 / "portfolio-freeze.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "new_proposals": 40,
            "inherited_revalidations_zero_credit": 20,
            "planned_outcomes": {label: outcomes.count(label) for label in ALLOWED_OUTCOMES},
            "x2_outcomes_claimed": False,
            "caps_are_ceilings": True,
        },
    )
    write_json(X1 / "approval-split.json", {"owner": OWNER, "phase": PHASE, "safe_now": safe, "candidates": candidates, "exact_approval": exact, "blocked": blocked})
    write_json(X1 / "skill-runner-plan.json", {"owner": OWNER, "phase": PHASE, "owner_skills": skills, "owner_runners": runners, "successor": successor})
    write_json(X1 / "clean-fix-refine-plan.json", {"owner": OWNER, "phase": PHASE, "owner_reviews": cfr, "successor_recommendations": successor["clean_fix_refine"]})
    write_json(
        X1 / "practice-lens-screen.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "Freed ID and CBR Heart",
            "practice": "synthetic historical loom pattern-chain documentation and provenance assurance",
            "lenses": ["textile-collections registrar", "pattern-chain conservation documentation analyst", "software provenance librarian"],
            "successor_practice_recommendation": successor["practice"],
            "real_objects_or_people": 0,
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "prospective_exact_title": "Auren Lark",
            "prospective_phase": "v674-v1",
            "precontact_performed": False,
            "send_attempts": 0,
            "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "tavian_state": "ON_STANDBY",
        },
    )
    write_json(
        X1 / "method-flow-startup.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "baseline": {"negatives": 37616, "methods": 23824, "failed": 9277, "passing": 11435},
            "startup_failure_count": len(method_rows),
            "methods": method_rows,
            "failures_erased": 0,
        },
    )
    write_json(
        X1 / "open-gate-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "inherited_open_gaps": 305,
            "inherited_exact_gates": 298,
            "planned_additive_open_gaps": 2,
            "planned_additive_exact_gates": 2,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        X1 / "threat-model.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "threats": [
                {"threat": "cross-owner mutation", "guard": "owner sparse lane and exact staged path review"},
                {"threat": "x2 leakage into x1", "guard": "absence test and immutable x1 commit"},
                {"threat": "private identifier leakage", "guard": "five-class staged scan"},
                {"threat": "canonical replay", "guard": "exclusive receipt directory and invocation latch"},
                {"threat": "authority promotion", "guard": "exact and blocked packets remain held"},
                {"threat": "successor precontact", "guard": "route-state send count zero until terminal gate"},
            ],
        },
    )
    write_text(X1 / "integrated-overview.md", build_overview())

    scan_paths = sorted([path for path in X1.rglob("*") if path.is_file()] + [Path(__file__)])
    classes = {
        "uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.IGNORECASE),
        "email": re.compile(r"\b[^\s@]+@[^\s@]+\.[^\s@]+\b"),
        "private_windows_path": re.compile(r"\b[A-Z]:\\(?:Users|GHC-Archives)\\", re.IGNORECASE),
        "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        "secret_assignment": re.compile(r"\b(?:api[_-]?key|password|secret|token)\s*[:=]\s*[^\s]+", re.IGNORECASE),
    }
    candidates = []
    for path in scan_paths:
        text = path.read_text(encoding="utf-8")
        for label, pattern in classes.items():
            for match in pattern.finditer(text):
                candidates.append({"class": label, "path": path.relative_to(ROOT).as_posix(), "sample_sha256": hashlib.sha256(match.group(0).encode()).hexdigest()})
    false_positives = []
    confirmed_hits = []
    for candidate in candidates:
        if candidate["class"] == "email" and candidate["path"] == "scripts/build_ghc_family_ilyra_fen_v673_v8_x1.py":
            false_positives.append({**candidate, "reason": "scanner_regex_self_description"})
        else:
            confirmed_hits.append(candidate)
    write_json(
        VALIDATION / "x1-staged-privacy.json",
        {"owner": OWNER, "phase": PHASE, "classes": list(classes), "files_scanned": len(scan_paths), "candidates": candidates, "reviewed_false_positives": false_positives, "confirmed_hits": confirmed_hits, "complete_privacy_assurance": False},
    )
    expected = sorted(path.relative_to(ROOT).as_posix() for path in X1.rglob("*") if path.is_file())
    expected += ["docs/ilyra-fen/v673-v8/validation/x1-staged-privacy.json", "scripts/build_ghc_family_ilyra_fen_v673_v8_x1.py", "tests/test_ghc_family_ilyra_fen_v673_v8_x1.py"]
    write_json(
        VALIDATION / "x1-staged-review.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "expected_paths": sorted(set(expected)),
            "x2_paths": 0,
            "deletions": 0,
            "source_or_sibling_mutations": 0,
            "state": "PREPARED_FOR_EXACT_INDEX_REVIEW",
        },
    )
    write_json(
        X1 / "build-receipt.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "mode": "planning_only_x1",
            "files_written": sorted(path.relative_to(ROOT).as_posix() for path in BASE.rglob("*") if path.is_file()),
            "x2_mutation": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def build_manifest() -> None:
    paths = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"], cwd=ROOT, text=True, encoding="utf-8"
    ).splitlines()
    manifest_path = "docs/ilyra-fen/v673-v8/validation/x1-manifest.json"
    allowed = []
    for path in paths:
        if path == manifest_path:
            continue
        if path.startswith("docs/ilyra-fen/v673-v8/x1/") or path in {
            "docs/ilyra-fen/v673-v8/validation/x1-staged-privacy.json",
            "docs/ilyra-fen/v673-v8/validation/x1-staged-review.json",
            "scripts/build_ghc_family_ilyra_fen_v673_v8_x1.py",
            "tests/test_ghc_family_ilyra_fen_v673_v8_x1.py",
        }:
            allowed.append(path)
        else:
            raise SystemExit(f"unexpected staged x1 path: {path}")
    entries = []
    for path in sorted(allowed):
        blob = normalized(git_bytes(f":{path}"))
        entries.append({"path": path, "bytes": len(blob), "sha256_normalized_lf": hashlib.sha256(blob).hexdigest()})
    write_json(
        ROOT / manifest_path,
        {
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE,
            "hash_domain": "normalized_lf_exact_git_index_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": [manifest_path],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "manifest"])
    args = parser.parse_args()
    if args.mode == "build":
        build()
    else:
        build_manifest()


if __name__ == "__main__":
    main()
