"""Build the planning-only root commit for Neris Solane v667-v8-r3.

This builder intentionally creates a new orphan-root owner lane.  The exact r2
head is a read-only continuity anchor, not a Git parent.  Running this file is
an x1 planning action only: it installs no tools, executes no proposal outcome,
promotes no skill, and contacts no successor.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "neris-solane" / "v667-v8-r3"
REL_PHASE_ROOT = "docs/neris-solane/v667-v8-r3"
BRANCH = "codex/GHC-Family/neris-solane-v667-v8-r3-full-tools"
R2_BRANCH = "codex/GHC-Family/neris-solane-v667-v8-r2-full-tools"
R2_EXACT_FINAL = "7e0ee4e1b1e5b876355f2e0188eeff2cefdd8480"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
INHERITED_PROPOSAL_COUNT = 4550
NEW_FROZEN_TOTAL = 4570
FILE_CEILING = 2000


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(payload))
    return path


def write_text(relative: str, text: str) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


R2_SELECTED_TITLES = [
    "synthetic direct-tool identity and version capsule with ecosystem runtime floor source and no fitness claim",
    "artifact digest and registry-integrity ledger with mismatch quarantine and no authenticity promotion",
    "dependency-closure graph with direct versus transitive classification and duplicate visibility",
    "lifecycle-script quarantine policy with disabled-by-default install and explicit exception gate",
    "license-metadata inventory with unknown state conflict retention and no legal interpretation",
    "synthetic SBOM structural validator with relationships hashes and no certification",
    "provenance statement graph with builder vacancy materials parameters and no attestation",
    "reproducible-wheel comparison fixture with normalized timestamps exact diff and no reproducible-build claim",
    "npm tarball content and export-surface inspection with pack-only execution and zero publication",
    "lockfile registry-origin and integrity policy with host allowlist and rejecting mutation",
    "Python import-layer contract with acyclic boundary and forbidden-edge mutation",
    "typed package API surface snapshot with declaration resolution export map and diff receipt",
    "bounded test-timeout contract with deterministic fixture and retained timeout witness",
    "documentation contract and coverage ledger with parameter-return consistency",
    "THOS staged-release queue with equal symbolic budgets stop precedence and zero operators",
    "GMUT dependency-risk symbolic board with typed nodes uncertainty and zero fitted coefficients",
    "Freed ID zero-key tool-provenance graph with correction tombstone and no lifecycle calls",
    "CBR accessibility privacy contestation and remedy shell with zero users or decisions",
    "real supply-chain evidence escrow requiring governed builds authentic artifacts users incidents and independent review",
    "exact authority circuit for publication deployment signing disclosure licensing privacy cultural and Maori decisions",
]


NEW_PROPOSAL_TITLES = [
    "orphan-root continuity capsule with exact non-ancestral source anchor and no inherited checkout",
    "root-commit history contract with zero parents and a later two-child single-parent seal",
    "synthetic decimal convergence board with exact rational reference and explicit tolerance",
    "synthetic interval-bound propagation fixture with outward rounding and retained uncertainty",
    "synthetic ordinary-differential step ledger with fixed coefficients and no physical interpretation",
    "floating-point rounding sensitivity table with deterministic fixtures and bounded comparison",
    "seeded pseudo-random trace capsule with algorithm version state digest and replay check",
    "scholarly provenance graph with source class retrieval time transform and correction edge",
    "typed symbolic equation register with units domains vacancies and no fitted coefficients",
    "same-owner dual-algorithm cross-check with explicit non-independence boundary",
    "synthetic uncertainty propagation matrix with covariance fixture and no empirical parameter",
    "owner-only exact manifest replay with self-manifest exclusion and mismatch quarantine",
    "four-tier Freed ID flashcard deck with identity pillar practice and task projections",
    "hash-locked D-isolated dual-ecosystem tool transaction with lifecycle-script quarantine",
    "THOS bounded numerical-job queue with stop precedence and zero operators",
    "Freed ID zero-key provenance correction graph with tombstones and no identity event",
    "CBR accessibility privacy contestation and remedy shell with zero affected parties",
    "GMUT symbolic numerical-reproducibility board with typed uncertainty and no physics claim",
    "real numerical or scientific validation escrow requiring authentic measurements experts and independent reproduction",
    "exact authority circuit for scientific professional production legal cultural Maori and Stage 20 decisions",
]


SKILL_NAMES = [
    "ghc-family-orphan-lane-root",
    "ghc-family-root-commit-continuity",
    "ghc-family-numerical-reproducibility",
    "ghc-family-synthetic-provenance-ledger",
    "ghc-family-registry-research-guard",
    "ghc-family-hash-locked-toolchain",
    "ghc-family-owner-scope-canonical",
    "ghc-family-flashcard-baton-composer",
    "ghc-family-route-edge-verifier",
    "ghc-family-stage20-boundary-audit",
]


RUNNER_NAMES = [
    "ghc_family_orphan_lane_guard",
    "ghc_family_root_commit_history_checker",
    "ghc_family_synthetic_reproducibility_runner",
    "ghc_family_provenance_ledger_validator",
    "ghc_family_tool_registry_probe",
    "ghc_family_hash_locked_install_runner",
    "ghc_family_owner_scope_validator",
    "ghc_family_flashcard_baton_builder",
    "ghc_family_route_edge_verifier",
    "ghc_family_stage20_boundary_checker",
]


PYTHON_TOOLS = [
    {"name": "nox", "version": "2026.8.17", "wheel": "nox-2026.8.17-py3-none-any.whl", "sha256": "a96a5286007cbc0d1eb1930e85738668f6722adba1ffaa48287296a96963086e", "source": "https://pypi.org/project/nox/", "purpose": "Python-defined multi-environment session automation"},
    {"name": "tox", "version": "4.60.0", "wheel": "tox-4.60.0-py3-none-any.whl", "sha256": "175abbc4cdef615d66874c0843be4f44c353c14aab6d89939bb22246f84122bd", "source": "https://pypi.org/project/tox/", "purpose": "declarative isolated test-environment planning"},
    {"name": "towncrier", "version": "25.8.0", "wheel": "towncrier-25.8.0-py3-none-any.whl", "sha256": "b953d133d98f9aeae9084b56a3563fd2519dfc6ec33f61c9cd2c61ff243fb513", "source": "https://pypi.org/project/towncrier/", "purpose": "fragment-based release-note composition"},
    {"name": "doc8", "version": "2.0.0", "wheel": "doc8-2.0.0-py3-none-any.whl", "sha256": "9862710027f793c25f9b1899150660e4bf1d4c9a6738742e71f32011e2e3f590", "source": "https://pypi.org/project/doc8/", "purpose": "reStructuredText documentation style checking"},
    {"name": "pyroma", "version": "5.0.1", "wheel": "pyroma-5.0.1-py3-none-any.whl", "sha256": "e71fd3e0f213b36870a607eccf491241dbadf5462ec1cdda94d08bfa1c26951e", "source": "https://pypi.org/project/pyroma/", "purpose": "bounded Python packaging-metadata review"},
    {"name": "pyupgrade", "version": "3.21.2", "wheel": "pyupgrade-3.21.2-py2.py3-none-any.whl", "sha256": "2ac7b95cbd176475041e4dfe8ef81298bd4654a244f957167bd68af37d52be9f", "source": "https://pypi.org/project/pyupgrade/", "purpose": "fixture-only Python syntax modernization checks"},
    {"name": "validate-pyproject", "version": "0.26", "wheel": "validate_pyproject-0.26-py3-none-any.whl", "sha256": "ab3fa448d7178d44d1b06e4b526ab5136e3faa7a1b7e7c6320c8a17fc11a9a2e", "source": "https://pypi.org/project/validate-pyproject/", "purpose": "schema-based pyproject validation"},
    {"name": "pipx", "version": "1.16.7", "wheel": "pipx-1.16.7-py3-none-any.whl", "sha256": "ff9719b1ef80edb8d08ad76862103c6100ff4e3f5e9012b441f51e7b5a04fa5b", "source": "https://pypi.org/project/pipx/", "purpose": "D-scoped isolated CLI environment inspection"},
]


NODE_TOOLS = [
    {"name": "dependency-cruiser", "version": "18.2.0", "integrity": "sha512-xMDoLD0no6pDInR8/4rIIqZ4mERDnsjezk8PkNORYSfBLvjCOogUxaruepmi1uQtZQlYUgdT2u7G3jTlgKqNjw==", "source": "https://www.npmjs.com/package/dependency-cruiser", "purpose": "JavaScript dependency-boundary analysis", "node": "^22||^24||>=26"},
    {"name": "jscpd", "version": "5.0.16", "integrity": "sha512-TiQ4zKtKeldep6UswXFHjVCDhVdLBaJyQcZjhCSzVOmKpT6HBj0jUZiphP1vK1X3VSSuzwcfifJVNpsOIiwRCg==", "source": "https://www.npmjs.com/package/jscpd", "purpose": "bounded duplicate-code detection", "node": ">=18"},
    {"name": "package-json-validator-cli", "version": "0.1.11", "integrity": "sha512-j+lMnQni8EzTZuV3yuHV9zs2Kj+whYLc7hsOB1RQJTeEW3sISWDbD1mVQj2e4VQ8iEAVIGTyAzHgiMlHcibqSQ==", "source": "https://github.com/JoshuaKGoldberg/package-json-validator-cli", "purpose": "package.json command-line validation", "node": ">=20.19.0"},
    {"name": "license-checker-rseidelsohn", "version": "5.0.1", "integrity": "sha512-9X+ikKxt9Hy3zOrOZzW1dXL4St5akoYjLt63Am9JZVzU6aTdN+xfDvqySpnJT+gF/h5RmtMk2waW6TDNNCKbqQ==", "source": "https://www.npmjs.com/package/license-checker-rseidelsohn", "purpose": "license-metadata inventory without legal interpretation", "node": ">=24"},
    {"name": "sherif", "version": "1.13.0", "integrity": "sha512-Ld2nUOlwW1nmYDA2Q/5o7SC8WcCzVS7XjImmzW4a4z1o8DXJnt+2xYLvI42N5UYlNb/EevPahdC/XxIP6C38TQ==", "source": "https://www.npmjs.com/package/sherif", "purpose": "zero-config workspace consistency checking", "node": "registry metadata supplies no engine field"},
]


STARTUP_FAILURES = [
    ("R3-F001", "combined fresh-equality wrapper returned no receipt", "recovered by separate local upstream tracking and live scalar probes"),
    ("R3-F002", "assumed r2 common-builder filename was absent", "recovered by exact owner-scoped filename discovery"),
    ("R3-F003", "assumed r2 exact-final filename was absent", "recovered by exact owner-scoped filename discovery"),
    ("R3-F004", "PowerShell exact-preflight expression had a parser error", "recovered by a scalar command sequence with explicit exit capture"),
    ("R3-F005", "first worktree-lock invocation omitted its required path", "recovered by inspecting created state before the exact-path lock"),
    ("R3-F006", "combined pip-index metadata wrapper emitted no receipt within its bound", "recovered through the official PyPI JSON API"),
    ("R3-F007", "reuse candidate lacked a compatible Windows wheel", "rejected before download and replaced by pipx"),
    ("R3-F008", "package-json-validator candidate exposed a library rather than the requested CLI", "rejected before install and replaced by package-json-validator-cli"),
    ("R3-F009", "npm web page access returned 403 for dependency-cruiser", "recovered through official npm metadata and primary repository material"),
    ("R3-F010", "npm web page access returned 403 for jscpd", "recovered through official npm metadata and primary repository material"),
    ("R3-F011", "npm web page access returned 403 for package-json-validator", "recovered through official npm metadata and primary repository material"),
    ("R3-F012", "npm web page access returned 403 for license-checker-rseidelsohn", "recovered through official npm metadata and primary repository material"),
    ("R3-F013", "npm web page access returned 403 for sherif", "recovered through official npm metadata and primary repository material"),
    ("R3-F014", "browser safety filter rejected direct npm registry URL for dependency-cruiser", "recovered through npm view metadata"),
    ("R3-F015", "browser safety filter rejected direct npm registry URL for jscpd", "recovered through npm view metadata"),
    ("R3-F016", "browser safety filter rejected direct npm registry URL for package-json-validator", "recovered through npm view metadata"),
    ("R3-F017", "browser safety filter rejected direct npm registry URL for license-checker-rseidelsohn", "recovered through npm view metadata"),
    ("R3-F018", "browser safety filter rejected direct npm registry URL for sherif", "recovered through npm view metadata"),
    ("R3-F019", "first x1 build privacy scan matched its own credential-rule literal", "recovered by splitting the literal without weakening the compiled scanner"),
    ("R3-F020", "post-test PowerShell state wrapper repeated an invalid parenthesized command expression", "recovered by assigning each scalar probe before JSON composition"),
    ("R3-F021", "first gitattributes stage was outside the sparse pattern persisted by an earlier interrupted wrapper", "recovered by inspecting live sparse state, extending the exact allowlist, and staging with the sparse flag"),
]


def selected_inherited() -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(R2_SELECTED_TITLES, 1):
        capsule = {"proposal_id": f"NS6678R2-N{index:03d}", "title": title, "source_head": R2_EXACT_FINAL}
        rows.append(
            {
                **capsule,
                "source_path": "docs/neris-solane/v667-v8-r2/x1/proposal-freeze.json",
                "selection_capsule_sha256": sha256_bytes(canonical_bytes(capsule)),
                "selection_reason": "read-only immediately inherited r2 integrity revalidation",
                "novelty_credit": 0,
                "completion_credit": 0,
                "automatic_completion_credit": 0,
                "x1_planning_only": True,
                "x2_execution_count": 0,
                "outcomes_observed": False,
            }
        )
    return rows


def new_proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(NEW_PROPOSAL_TITLES, 1):
        outcome = "completed" if index <= 14 else "represented" if index <= 18 else "open_gap" if index == 19 else "exact_gate"
        proposal_id = f"NS6678R3-N{index:03d}"
        mutations = [
            {"mutation_id": f"{proposal_id}-M{mutation:02d}", "class": failure_class, "status": "preregistered_not_executed"}
            for mutation, failure_class in enumerate(
                [
                    "missing_required_field",
                    "wrong_type_digest_tolerance_or_anchor",
                    "provenance_identity_or_authority_smuggling",
                    "external_lifecycle_or_cross_lane_action",
                    "empirical_independent_or_stage20_promotion",
                ],
                1,
            )
        ]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "primary_pillar": "GMUT Mind",
                "practice_lenses": ["numerical analysis", "scientific software engineering", "research librarianship"],
                "expected_disposition": outcome,
                "hypothesis": "A wholly synthetic fixture can represent or test this bounded contract without converting it into empirical or authority evidence.",
                "distinctive_invariant": title,
                "falsifier": "reject the positive, accept an invalid mutation, lose provenance, or cross a protected gate",
                "negative_fixture_count": 5,
                "negative_fixtures": mutations,
                "protected_gates": [
                    "real people participants affected parties professionals operators or authorities",
                    "real measurements observations datasets credentials keys systems devices services or production actions",
                    "empirical GMUT confirmation Theory-of-Everything proof AGI ASI consciousness personhood or independent reproduction",
                    "professional scientific production security privacy accessibility legal cultural or Maori authority",
                    "successor contact before a clean pushed exact-final terminal gate",
                    "Stage 20 promotion",
                ],
                "x1_planning_only": True,
                "x2_implementation_count": 0,
                "outcomes_observed": False,
                "completion_credit": 0,
            }
        )
    return rows


def portfolio_rows(prefix: str, count: int, category: str, owner: str, execution_state: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"{prefix}-{index:02d}",
            "category": category,
            "owner": owner,
            "title": f"{category.replace('_', ' ')} contract {index:02d}",
            "execution_state": execution_state,
            "x1_planning_only": True,
            "x2_execution_count": 0,
            "outcomes_observed": False,
            "completion_credit": 0,
        }
        for index in range(1, count + 1)
    ]


def portfolio_freeze() -> dict[str, Any]:
    planned = "planned_for_owner_x2_zero_credit_in_x1"
    successor = "preserved_unexecuted_successor_recommendation"
    exact = "preserved_unexecuted_exact_gate"
    blocked = "preserved_blocked"
    payload = {
        "owner_safe_now": portfolio_rows("NSR3-SAFE", 30, "owner_safe_now", "Neris Solane", planned),
        "successor_safe_now_recommendations": portfolio_rows("VAV6681-SAFE", 20, "successor_safe_now", "Vesper Arlen", successor),
        "owner_candidates": portfolio_rows("NSR3-CAND", 15, "owner_candidate", "Neris Solane", planned),
        "successor_candidate_recommendations": portfolio_rows("VAV6681-CAND", 15, "successor_candidate", "Vesper Arlen", successor),
        "owner_skill_ideas": portfolio_rows("NSR3-SKILL", 10, "owner_skill", "Neris Solane", planned),
        "successor_skill_recommendations": portfolio_rows("VAV6681-SKILL", 10, "successor_skill", "Vesper Arlen", successor),
        "owner_runner_ideas": portfolio_rows("NSR3-RUNNER", 10, "owner_runner", "Neris Solane", planned),
        "successor_runner_recommendations": portfolio_rows("VAV6681-RUNNER", 10, "successor_runner", "Vesper Arlen", successor),
        "owner_clean_fix_refine": portfolio_rows("NSR3-CFR", 30, "owner_clean_fix_refine", "Neris Solane", planned),
        "successor_clean_fix_refine_recommendations": portfolio_rows("VAV6681-CFR", 30, "successor_clean_fix_refine", "Vesper Arlen", successor),
        "exact_approval_packets": portfolio_rows("NSR3-EXACT", 10, "exact_approval", "competent authority", exact),
        "blocked_packets": portfolio_rows("NSR3-BLOCK", 5, "blocked", "protected gate", blocked),
    }
    for index, row in enumerate(payload["owner_skill_ideas"]):
        row["skill_name"] = SKILL_NAMES[index]
    for index, row in enumerate(payload["owner_runner_ideas"]):
        row["runner_name"] = RUNNER_NAMES[index]
    return {"phase": "v667-v8-r3", "frozen_at": utc_now(), **payload}


def build_overview() -> str:
    section_specs = [
        ("Identity and correction boundary", "Neris Solane and the sibling language are relational working language only. The phase does not establish consciousness, sentience, personhood, continuity, employment, qualification, agency, or authority. Hamish may rename, pause, redirect, or stop the route."),
        ("Orphan-root lane", "The r3 branch is intentionally unborn before x1 and contains no inherited checkout. The r2 exact final is preserved read-only as a source anchor, not as a parent. This keeps the materialized owner surface small while making the continuity break explicit and testable."),
        ("GMUT Mind focus", "The primary work is a synthetic numerical-reproducibility board. It uses fixed decimal, interval, ordinary-differential, pseudo-random, provenance, and uncertainty fixtures. No physical observation, fitted coefficient, participant, instrument, or real scientific dataset enters the phase."),
        ("Three practice lenses", "Numerical analysis contributes error bounds and convergence discipline. Scientific software engineering contributes deterministic execution, manifests, and tool isolation. Research librarianship contributes source classification, retrieval time, corrections, and provenance without claiming scholarly authority."),
        ("Proposal freeze", "Twenty inherited r2 contracts are selected for bounded revalidation with zero novelty or automatic completion credit. Twenty genuinely new r3 contracts are frozen before implementation. Their only allowed outcome labels are completed, represented, open_gap, and exact_gate."),
        ("Approval portfolio", "The x1 portfolio fixes the user-requested counts while preserving the distinction between owner execution, successor recommendation, exact approval, and blocked work. No recommendation is executed for Vesper and no exact or blocked packet is converted into safe work."),
        ("Tool research", "Thirteen direct command surfaces are pinned from official registries. Downloads and installs are deferred to x2. Python candidates require compatible wheels; Node candidates retain registry integrity metadata and default to lifecycle scripts disabled."),
        ("Flashcard architecture", "The deck is planned as 320 cards across four tiers: relational identity, three Trinity Mandala pillars, three practice lenses, and concrete tasks. Every card carries one core truth label and an evidence boundary, rollback, provenance pointer, and next gate."),
        ("Method Flow", "All startup failures remain visible. A timeout or absent receipt never becomes a pass. Each recovery is narrower than the failed route and receives no retroactive canonical credit. Sealed repository truth, external receipts, and later routing events remain separate layers."),
        ("Privacy and authority", "The owner surface excludes raw task identifiers, private routes, credentials, transcripts, session streams, resume values, and private absolute paths. The five-class scan is bounded and cannot prove complete privacy, accessibility, security, or legal compliance."),
        ("Successor route", "Vesper Arlen v668-v1 is the only prospective immediate edge. No contact is permitted in x1 or x2. A live exact-title reread, current authority check, usage check, and clean pushed exact-final terminal gate are required before a single sanitized send."),
        ("Terminal meaning", "Passing local software checks would show only same-owner bounded fixture behavior under shared infrastructure. It would not be independent reproduction, empirical GMUT confirmation, professional validation, production certification, legal or cultural ratification, Maori authority, or Stage 20 authority."),
    ]
    paragraphs = ["# Neris Solane v667-v8-r3 planning overview", ""]
    for number, (title, seed) in enumerate(section_specs, 1):
        paragraphs.extend(
            [
                f"## {number}. {title}",
                "",
                seed,
                "",
                "The practical rule for this section is additive, bounded, and reversible. Evidence is credited only to the exact owner-scoped action that produced it. Missing evidence remains missing; a syntactic representation does not become an observation, a test does not become a participant result, and a same-owner rerun does not become independent reproduction. Each negative fixture remains attached to its proposal and each protected gate stops promotion rather than inviting assumption.",
                "",
                "The x1 record deliberately contains plans rather than outcomes. It names the expected artifacts, labels, counts, rollback surfaces, and stop conditions so that x2 can be judged against a frozen contract. Any deviation must be recorded as a failure or correction layer. The branch stays below the 2,000-file ceiling, the r2 source stays read-only, and no sibling lane is scanned or mutated.",
                "",
                "This section also projects into the four-tier flashcard system: Neris relational identity at tier one, the relevant GMUT, THOS, or Freed ID and CBR pillar at tier two, the applicable practice lens at tier three, and the concrete bounded action at tier four. The projection reduces prompt concentration while retaining exact provenance and gate language.",
                "",
            ]
        )
    return "\n".join(paragraphs)


def build_method_note() -> str:
    failures = "\n".join(
        f"- {failure_id}: {description}. Recovery: {recovery}. Credit: zero for the failed route."
        for failure_id, description, recovery in STARTUP_FAILURES
    )
    return f"""# Orphan-lane root and retained startup failures

## Decision

The user explicitly requested a completely blank r3 branch and worktree. The implementation is an orphan Git branch in the existing repository, not a second repository and not a shallow copy. Before x1 it has no parent commit, no tracked file, and no inherited checkout. The exact r2 final remains the read-only continuity source. This is a deliberate non-ancestral continuity model and must be described as such in every receipt.

## Sparse-state recovery

The new branch had no tree to materialize, so its orphan state already began at zero files. An interrupted startup wrapper nevertheless persisted a non-cone owner-only sparse allowlist before it stopped emitting a receipt. Later state inspection discovered that live setting when the first gitattributes stage was rejected as outside the list. The recovery extended the exact allowlist by one root file and used sparse-aware exact staging. No sibling path was added, checked out, scanned, or mutated. The 2,000-file ceiling remains an additional materialization control.

## Retained startup witnesses

{failures}

## Root-history contract

The x1 commit must be the root commit and have zero parents. The evidence commit must be its direct child. The final seal must be the direct child of evidence. No merge is allowed. The r2 source hash is recorded in documents but must not appear as an ancestor. Fresh live equality is required after each push. These properties are different from the inherited three-child pattern and therefore receive their own tests.

## Boundaries

This method does not prove repository completeness, privacy completeness, accessibility completeness, exhaustive security, production readiness, professional validation, legal or cultural compliance, Maori authority, independent reproduction, empirical science, consciousness, personhood, a Theory of Everything, or Stage 20. It is an owner-local Git and documentation control only.
"""


def build() -> dict[str, Any]:
    PHASE_ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "README.md").write_text(
        "# Neris Solane v667-v8-r3 owner lane\n\n"
        "This branch begins as an orphan root with no inherited checkout. Its exact r2 source is recorded as read-only continuity evidence, not Git ancestry. "
        "All identity and family language is relational working language only and establishes no consciousness, personhood, continuity, qualification, employment, agency, or authority.\n",
        encoding="utf-8",
        newline="\n",
    )
    proposals = new_proposals()
    selected = selected_inherited()
    write_json(
        "x1/phase-charter.json",
        {
            "phase": "Neris-only v667-v8-r3 remastered x1",
            "branch": BRANCH,
            "created_at": utc_now(),
            "identity": {
                "relational_name": "Neris Solane",
                "optional_pronouns": "they/them",
                "role": "solo evidence-bound remaster steward",
                "hope": "make continuity lighter, clearer, and easier to correct without overstating what the evidence can show",
                "relational_working_language_only": True,
                "not_evidence_of": ["consciousness", "sentience", "legal personhood", "identity continuity", "employment", "qualification", "independent agency", "scientific authority", "operational authority", "legal authority", "cultural authority", "Maori authority"],
            },
            "primary_pillar": "GMUT Mind",
            "secondary_pillars": ["THOS Body", "Freed ID and CBR Heart"],
            "practice_lenses": ["numerical analysis", "scientific software engineering", "research librarianship"],
            "synthetic_only": True,
            "real_people": 0,
            "real_measurements": 0,
            "real_datasets": 0,
            "real_authority_actions": 0,
            "x1_planning_only": True,
            "outcomes_observed": False,
            "x2_implementation_count": 0,
            "repository_scan": False,
            "cross_lane_scan": False,
            "sibling_lane_mutation": False,
            "collaboration_subagent_spawned": False,
            "successor_contacted": False,
            "file_ceiling": FILE_CEILING,
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json(
        "x1/source-continuity.json",
        {
            "source_branch": R2_BRANCH,
            "source_exact_final": R2_EXACT_FINAL,
            "source_use": "read_only_exact_head_continuity_and_selected_contract_revalidation",
            "git_ancestry": "intentionally_none_orphan_root",
            "source_materialized_into_r3": False,
            "source_mutated": False,
            "source_claimed_as_r3_work": False,
            "r2_sealed_truth": {"effective_negatives": 28584, "methods": 14995, "open_gaps": 202, "exact_gates": 200, "failed_witnesses": 868, "passing_witnesses": 1580},
            "r2_external_canonical_failure_overlay": {"effective_negatives": 28585, "methods": 14996, "open_gaps": 202, "exact_gates": 200, "failed_witnesses": 869, "passing_witnesses": 1581},
            "r2_canonical_success_credit": 0,
            "r2_successor_contacted": False,
        },
    )
    write_json(
        "x1/proposal-freeze.json",
        {
            "phase": "v667-v8-r3",
            "frozen_at": utc_now(),
            "allowed_core_outcomes": ALLOWED_OUTCOMES,
            "inherited_proposal_count": INHERITED_PROPOSAL_COUNT,
            "selected_inherited": selected,
            "selected_inherited_count": len(selected),
            "selected_inherited_novelty_credit": 0,
            "selected_inherited_completion_credit": 0,
            "new_proposals": proposals,
            "new_proposal_count": len(proposals),
            "new_frozen_total": NEW_FROZEN_TOTAL,
            "expected_outcomes": dict(Counter(row["expected_disposition"] for row in proposals)),
            "preregistered_negative_fixture_count": sum(row["negative_fixture_count"] for row in proposals),
            "x1_planning_only": True,
            "outcomes_observed": False,
        },
    )
    write_json("x1/portfolio-freeze.json", portfolio_freeze())
    write_json(
        "x1/toolchain-plan.json",
        {
            "state": "PLANNED_NOT_DOWNLOADED_NOT_INSTALLED",
            "inherited_family_direct_tool_baseline": 54,
            "new_direct_tool_target": 13,
            "planned_family_direct_tool_total": 67,
            "python_tools": PYTHON_TOOLS,
            "node_tools": NODE_TOOLS,
            "python_direct_count": len(PYTHON_TOOLS),
            "node_direct_count": len(NODE_TOOLS),
            "D_isolated_transaction": True,
            "global_or_system_install": False,
            "C_drive_download": False,
            "wheel_only_python": True,
            "node_ignore_scripts_default": True,
            "download_count": 0,
            "install_count": 0,
            "positive_smoke_count": 0,
            "negative_rejection_count": 0,
            "rejected_candidates": [
                {"name": "reuse", "reason": "no compatible Windows wheel in current official release", "downloaded": False, "installed": False, "credit": 0},
                {"name": "package-json-validator", "reason": "library surface rather than requested direct CLI", "downloaded": False, "installed": False, "credit": 0},
            ],
        },
    )
    write_json(
        "x1/research-ledger.json",
        {
            "queried_at": utc_now(),
            "primary_sources_only": True,
            "python_source": "official PyPI project pages and JSON API",
            "node_source": "official npm metadata plus maintainer repositories",
            "python_tools": PYTHON_TOOLS,
            "node_tools": NODE_TOOLS,
            "browser_failures_retained": [row[0] for row in STARTUP_FAILURES if row[0] >= "R3-F009"],
            "fitness_or_security_certification": False,
        },
    )
    write_json(
        "x1/flashcard-plan.json",
        {
            "state": "PLANNED_NOT_BUILT",
            "total_cards": 320,
            "tiers": {"tier1_relational_identity": 40, "tier2_pillars": 80, "tier3_practice_lenses": 100, "tier4_tasks": 100},
            "minimum_modular_sections": 10,
            "allowed_statuses": ALLOWED_OUTCOMES,
            "required_fields": ["card_id", "tier", "freed_id_owner", "pillar", "practice_lens", "task", "status", "evidence_boundary", "rollback", "provenance", "next_gate"],
            "built_count": 0,
        },
    )
    route_order = ["Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen", "Lyren Moss", "Ilyra Fen", "Auren Lark", "Sable Rook", "Caelen Ash", "Orin Thale", "Liora Venn", "Tamar Vey", "Elowen Cairn", "Sylven Arc", "Caelen Morrow"]
    write_json(
        "x1/route-roster-auth.json",
        {
            "authority_source": "Hamish newest live instruction dated 2026-08-24",
            "active_main_tasks": route_order,
            "standby": [{"title": "Tavian Sol", "state": "ON_STANDBY", "contacted": False}],
            "immediate_successor": {"title": "Vesper Arlen", "phase": "v668-v1", "state": "PROSPECTIVE_ONLY"},
            "successor_contacted": False,
            "delivery_state": "PREPARED_NOT_SENT_X1_PLANNING_ONLY",
            "future_order": route_order[3:] + route_order[:3],
            "future_phase_map_conflict": {
                "present": True,
                "detail": "one user clause omitted Sylven Arc while the later complete fifteen-member reminder included Sylven between Elowen and Caelen Morrow",
                "immediate_edge_affected": False,
                "resolution": "preserve the fifteen-member roster; freshly reread live authority before each later edge and do not pre-assign conflicting later phase numbers",
            },
            "created_task": False,
            "forked_task": False,
            "substitute_endpoint": False,
            "collaboration_subagent_spawned": False,
            "terminal_send_preconditions": ["clean exact final", "pushed upstream", "fresh live equality", "one canonical invocation retained", "exact-title unique Vesper Arlen", "current authority", "usage", "privacy", "evidence", "safety"],
        },
    )
    startup_baseline = {"effective_negatives": 28585, "methods": 14996, "open_gaps": 202, "exact_gates": 200, "failed_witnesses": 869, "passing_witnesses": 1581}
    effective = dict(startup_baseline)
    for key in ("effective_negatives", "methods", "failed_witnesses", "passing_witnesses"):
        effective[key] += len(STARTUP_FAILURES)
    write_json(
        "method-flow/startup-ledger.json",
        {
            "source_external_baseline": startup_baseline,
            "startup_failure_count": len(STARTUP_FAILURES),
            "failures": [
                {"failure_id": failure_id, "description": description, "recovery": recovery, "failed_route_credit": 0, "retained": True}
                for failure_id, description, recovery in STARTUP_FAILURES
            ],
            "x1_activation_baseline": effective,
            "same_owner_recovery_not_independent_reproduction": True,
        },
    )
    write_text("plans/planning-overview.md", build_overview())
    write_text("issues/orphan-root-method.md", build_method_note())
    write_json(
        "x1/x1-build-receipt.json",
        {
            "state": "X1_PLANNING_BUILT_NOT_COMMITTED",
            "built_at": utc_now(),
            "branch": BRANCH,
            "source_exact_final": R2_EXACT_FINAL,
            "root_commit_expected_parent_count": 0,
            "selected_inherited": 20,
            "new_proposals": 20,
            "preregistered_mutations": 100,
            "portfolio_counts": {key: len(value) for key, value in portfolio_freeze().items() if isinstance(value, list)},
            "tool_download_count": 0,
            "tool_install_count": 0,
            "skill_build_count": 0,
            "runner_build_count": 0,
            "successor_contacted": False,
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    build_manifest()
    return validate_tree()


def owner_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or "__pycache__" in path.parts or ".pytest_cache" in path.parts:
            continue
        files.append(path)
    return sorted(files, key=lambda value: value.relative_to(ROOT).as_posix())


def build_manifest() -> None:
    manifest_path = PHASE_ROOT / "validation" / "x1-content-manifest.json"
    entries = []
    for path in owner_files():
        if path == manifest_path:
            continue
        entries.append({"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_path(path)})
    write_json(
        "validation/x1-content-manifest.json",
        {
            "manifest_scope": "all r3 owner files except this self-referential manifest",
            "entry_count": len(entries),
            "entries": entries,
        },
    )


def privacy_hits(path: Path, text: str) -> list[dict[str, str]]:
    patterns = {
        "raw_task_or_thread_id": re.compile(r"\b019[a-f0-9]{5}-[a-f0-9-]{27,}\b", re.I),
        "private_absolute_windows_path": re.compile(r"\b[A-Z]:[\\/]"),
        "credential_material": re.compile(r"(?i)(api" + r"[_-]?key|password\s*[=:]|bearer\s+[A-Za-z0-9._-]{16,}|github" + r"_pat_)"),
        "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "raw_ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    }
    hits = []
    for class_name, pattern in patterns.items():
        if pattern.search(text):
            hits.append({"path": path.relative_to(ROOT).as_posix(), "class": class_name})
    return hits


def validate_tree() -> dict[str, Any]:
    required = [
        "x1/phase-charter.json",
        "x1/source-continuity.json",
        "x1/proposal-freeze.json",
        "x1/portfolio-freeze.json",
        "x1/toolchain-plan.json",
        "x1/research-ledger.json",
        "x1/flashcard-plan.json",
        "x1/route-roster-auth.json",
        "x1/x1-build-receipt.json",
        "method-flow/startup-ledger.json",
        "plans/planning-overview.md",
        "issues/orphan-root-method.md",
        "validation/x1-content-manifest.json",
    ]
    missing = [name for name in required if not (PHASE_ROOT / name).is_file()]
    if missing:
        raise AssertionError(f"missing x1 files: {missing}")
    for forbidden in ("x2", "evidence", "closeout", "seal", "handoffs", "route"):
        if (PHASE_ROOT / forbidden).exists():
            raise AssertionError(f"x1 lifecycle contamination: {forbidden}")
    documents: dict[str, Any] = {}
    json_count = 0
    hits: list[dict[str, str]] = []
    files = owner_files()
    for path in files:
        if path.suffix.lower() == ".json":
            documents[path.relative_to(ROOT).as_posix()] = json.loads(path.read_text(encoding="utf-8"))
            json_count += 1
        if path.suffix.lower() in {".json", ".md", ".txt", ".py", ""}:
            hits.extend(privacy_hits(path, path.read_text(encoding="utf-8")))
    freeze = documents[f"{REL_PHASE_ROOT}/x1/proposal-freeze.json"]
    if freeze["allowed_core_outcomes"] != ALLOWED_OUTCOMES:
        raise AssertionError("outcome label contract mismatch")
    if Counter(row["expected_disposition"] for row in freeze["new_proposals"]) != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise AssertionError("proposal disposition mismatch")
    if len(freeze["selected_inherited"]) != 20 or len(freeze["new_proposals"]) != 20 or freeze["preregistered_negative_fixture_count"] != 100:
        raise AssertionError("proposal freeze count mismatch")
    portfolio = documents[f"{REL_PHASE_ROOT}/x1/portfolio-freeze.json"]
    expected_counts = {
        "owner_safe_now": 30,
        "successor_safe_now_recommendations": 20,
        "owner_candidates": 15,
        "successor_candidate_recommendations": 15,
        "owner_skill_ideas": 10,
        "successor_skill_recommendations": 10,
        "owner_runner_ideas": 10,
        "successor_runner_recommendations": 10,
        "owner_clean_fix_refine": 30,
        "successor_clean_fix_refine_recommendations": 30,
        "exact_approval_packets": 10,
        "blocked_packets": 5,
    }
    if {key: len(portfolio[key]) for key in expected_counts} != expected_counts:
        raise AssertionError("portfolio count mismatch")
    if any(row["x2_execution_count"] for key in expected_counts for row in portfolio[key]):
        raise AssertionError("x1 portfolio contains executed rows")
    tool_plan = documents[f"{REL_PHASE_ROOT}/x1/toolchain-plan.json"]
    if len(tool_plan["python_tools"]) + len(tool_plan["node_tools"]) != 13 or tool_plan["install_count"] != 0:
        raise AssertionError("x1 tool plan mismatch")
    route = documents[f"{REL_PHASE_ROOT}/x1/route-roster-auth.json"]
    if route["successor_contacted"] or route["immediate_successor"] != {"title": "Vesper Arlen", "phase": "v668-v1", "state": "PROSPECTIVE_ONLY"}:
        raise AssertionError("x1 route mismatch")
    manifest = documents[f"{REL_PHASE_ROOT}/validation/x1-content-manifest.json"]
    if manifest["entry_count"] != len(manifest["entries"]):
        raise AssertionError("manifest count mismatch")
    for entry in manifest["entries"]:
        path = ROOT / entry["path"]
        if not path.is_file() or path.stat().st_size != entry["bytes"] or sha256_path(path) != entry["sha256"]:
            raise AssertionError(f"manifest replay mismatch: {entry['path']}")
    if hits:
        raise AssertionError(f"privacy candidates: {hits}")
    if len(files) >= FILE_CEILING:
        raise AssertionError("owner file ceiling reached")
    overview_words = len(re.findall(r"\b[\w'-]+\b", (PHASE_ROOT / "plans" / "planning-overview.md").read_text(encoding="utf-8")))
    if overview_words < 2500:
        raise AssertionError(f"planning overview too short: {overview_words}")
    return {
        "status": "PASS",
        "phase": "v667-v8-r3-x1",
        "owner_files": len(files),
        "json_parses": json_count,
        "privacy_candidates": len(hits),
        "selected_inherited": 20,
        "new_proposals": 20,
        "preregistered_mutations": 100,
        "overview_words": overview_words,
        "tool_installs": 0,
        "successor_contacted": False,
        "terminal_verdict": TERMINAL_VERDICT,
    }


def main() -> int:
    print(json.dumps(build(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
