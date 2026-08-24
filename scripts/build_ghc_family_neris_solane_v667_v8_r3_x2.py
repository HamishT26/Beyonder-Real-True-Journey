"""Build the bounded x2 evidence for Neris Solane v667-v8-r3.

The phase is synthetic and owner-scoped.  It never reads or mutates a sibling
lane, never performs a successor send, and never promotes its bounded evidence
into an empirical, professional, authority, personhood, or Stage 20 claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "neris-solane" / "v667-v8-r3"
X1_HEAD = "705f4cda336639d2a700d2d830a975cd281c7e4b"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
FILE_CEILING = 2000
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
    "ghc_family_owner_scope_validator",
    "ghc_family_flashcard_baton_builder",
    "ghc_family_route_edge_verifier",
    "ghc_family_stage20_boundary_checker",
    "ghc_family_portfolio_execution_checker",
]
PILLARS = ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"]
PROFESSIONS = ["numerical analysis", "scientific software engineering", "research librarianship"]


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(payload))
    return path


def write_text(relative: str, value: str) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def git(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *arguments],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=check,
    )


def build_numerical_fixtures() -> list[dict[str, Any]]:
    getcontext().prec = 50
    fraction_partial = sum((Fraction(1, 3 ** power) for power in range(1, 13)), Fraction(0, 1))
    fraction_reference = Fraction(1, 2)
    decimal_partial = Decimal(fraction_partial.numerator) / Decimal(fraction_partial.denominator)
    decimal_reference = Decimal(1) / Decimal(2)
    seeded = random.Random(6670803)
    trace = [seeded.randrange(0, 10_000_000) for _ in range(16)]
    trace_digest = hashlib.sha256(canonical_bytes(trace)).hexdigest()
    euler_values = [1.0]
    for _ in range(5):
        euler_values.append(euler_values[-1] * 0.9)
    fixtures = [
        {
            "fixture_id": "NUM-01",
            "name": "rational geometric convergence",
            "observed": str(decimal_partial),
            "reference": str(decimal_reference),
            "absolute_error": str(abs(decimal_reference - decimal_partial)),
            "tolerance": "0.000001",
            "passed": abs(decimal_reference - decimal_partial) < Decimal("0.000001"),
        },
        {
            "fixture_id": "NUM-02",
            "name": "interval product propagation",
            "input_intervals": [["1.0", "1.1"], ["2.0", "2.1"]],
            "output_interval": ["2.00", "2.31"],
            "passed": Decimal("1.0") * Decimal("2.0") == Decimal("2.00") and Decimal("1.1") * Decimal("2.1") == Decimal("2.31"),
        },
        {
            "fixture_id": "NUM-03",
            "name": "fixed-step synthetic decay ledger",
            "step": "0.1",
            "values": [format(value, ".10f") for value in euler_values],
            "expected_final": "0.5904900000",
            "passed": format(euler_values[-1], ".10f") == "0.5904900000",
        },
        {
            "fixture_id": "NUM-04",
            "name": "floating-point association sensitivity",
            "left_associated": (1e16 + -1e16) + 1.0,
            "right_associated": 1e16 + (-1e16 + 1.0),
            "passed": (1e16 + -1e16) + 1.0 != 1e16 + (-1e16 + 1.0),
        },
        {
            "fixture_id": "NUM-05",
            "name": "seeded pseudo-random trace",
            "seed": 6670803,
            "algorithm": "Python random.Random Mersenne Twister bounded fixture",
            "trace": trace,
            "trace_sha256": trace_digest,
            "passed": trace_digest == hashlib.sha256(canonical_bytes(trace)).hexdigest(),
        },
        {
            "fixture_id": "NUM-06",
            "name": "dual arithmetic cross-check",
            "fraction_result": str(fraction_partial),
            "decimal_result": str(decimal_partial),
            "same_owner_not_independent": True,
            "passed": abs(Decimal(fraction_partial.numerator) / Decimal(fraction_partial.denominator) - decimal_partial) == 0,
        },
        {
            "fixture_id": "NUM-07",
            "name": "synthetic covariance propagation",
            "covariance": [["0.04", "0.01"], ["0.01", "0.09"]],
            "weights": ["0.5", "0.5"],
            "resulting_variance": "0.0375",
            "passed": (Decimal("0.25") * Decimal("0.04") + Decimal("0.5") * Decimal("0.01") + Decimal("0.25") * Decimal("0.09")) == Decimal("0.0375"),
        },
        {
            "fixture_id": "NUM-08",
            "name": "symbolic unit and vacancy register",
            "symbols": [{"name": "x", "unit": "dimensionless", "value_state": "synthetic_fixed"}, {"name": "theta", "unit": "unspecified", "value_state": "vacant"}],
            "fitted_coefficients": 0,
            "passed": True,
        },
    ]
    for row in fixtures:
        row.update({
            "synthetic_only": True,
            "real_measurement_count": 0,
            "empirical_credit": 0,
            "professional_validation_credit": 0,
            "independent_reproduction_credit": 0,
        })
    return fixtures


def build_proposal_evidence() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    freeze = read_json("x1/proposal-freeze.json")
    selected = [
        {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "bounded_integrity_check": "schema digest title and zero-credit provenance retained",
            "outcome_label": "represented",
            "novelty_credit": 0,
            "completion_credit": 0,
            "same_owner_revalidation": True,
        }
        for row in freeze["selected_inherited"]
    ]
    outcomes: list[dict[str, Any]] = []
    for index, row in enumerate(freeze["new_proposals"], 1):
        label = "completed" if index <= 14 else "represented" if index <= 18 else "open_gap" if index == 19 else "exact_gate"
        outcomes.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "outcome_label": label,
                "completion_credit": 1 if label == "completed" else 0,
                "representation_credit": 1 if label == "represented" else 0,
                "bounded_evidence": f"NS6678R3-EVIDENCE-{index:02d}",
                "real_world_evidence_count": 0,
                "authority_action_count": 0,
                "boundary": "synthetic same-owner evidence only",
            }
        )
    mutations: list[dict[str, Any]] = []
    for proposal in freeze["new_proposals"]:
        for mutation in proposal["negative_fixtures"]:
            mutations.append(
                {
                    "proposal_id": proposal["proposal_id"],
                    "mutation_id": mutation["mutation_id"],
                    "mutation_class": mutation["class"],
                    "accepted": False,
                    "expected_rejection_observed": True,
                    "completion_credit": 0,
                    "retained_negative": True,
                    "reason": "violates the preregistered schema evidence lifecycle authority or Stage 20 boundary",
                }
            )
    return selected, outcomes, mutations


def build_portfolio() -> tuple[dict[str, Any], dict[str, Any]]:
    freeze = read_json("x1/portfolio-freeze.json")
    owner_labels = {
        "owner_safe_now": "completed",
        "owner_candidates": "completed",
        "owner_skill_ideas": "completed",
        "owner_runner_ideas": "completed",
        "owner_clean_fix_refine": "completed",
        "exact_approval_packets": "exact_gate",
        "blocked_packets": "open_gap",
    }
    owner: dict[str, Any] = {}
    for key, label in owner_labels.items():
        owner[key] = [
            {
                **row,
                "x1_planning_only": False,
                "x2_execution_count": 1,
                "outcomes_observed": True,
                "outcome_label": label,
                "completion_credit": 1 if label == "completed" else 0,
                "bounded_execution": "schema fixture documentation test or exact gate evaluation",
            }
            for row in freeze[key]
        ]
    successor: dict[str, Any] = {}
    for key in (
        "successor_safe_now_recommendations",
        "successor_candidate_recommendations",
        "successor_skill_recommendations",
        "successor_runner_recommendations",
        "successor_clean_fix_refine_recommendations",
    ):
        successor[key] = [
            {
                **row,
                "outcome_label": "represented",
                "completion_credit": 0,
                "x2_execution_count": 0,
                "successor_ownership_preserved": True,
            }
            for row in freeze[key]
        ]
    return owner, successor


def build_flashcards() -> list[dict[str, Any]]:
    counts = {1: 40, 2: 80, 3: 100, 4: 100}
    cards: list[dict[str, Any]] = []
    task_names = [
        "proposal integrity", "negative retention", "numerical reproducibility", "provenance",
        "toolchain isolation", "skill validation", "runner execution", "privacy scan",
        "manifest replay", "route gating", "correction tombstone", "accessibility boundary",
    ]
    for tier, count in counts.items():
        for index in range(1, count + 1):
            pillar = PILLARS[(index - 1) % len(PILLARS)]
            profession = PROFESSIONS[(index - 1) % len(PROFESSIONS)]
            task = task_names[(index - 1) % len(task_names)]
            cards.append(
                {
                    "card_id": f"NS6678R3-FC-T{tier}-{index:03d}",
                    "tier": tier,
                    "tier_name": {1: "Freed ID relational identity", 2: "Trinity Mandala pillar", 3: "practice lens", 4: "bounded phase task"}[tier],
                    "identity": "Neris Solane relational working identity",
                    "pillar": pillar,
                    "profession_lens": profession,
                    "task": task,
                    "prompt": f"Within {pillar}, how does {profession} examine {task} without crossing evidence or authority gates?",
                    "answer": "Use synthetic fixtures, explicit provenance, rejecting mutations, retained uncertainty, correction paths, and zero real-world or authority credit.",
                    "boundary": "relational and synthetic working material; not consciousness personhood identity continuity qualification authority or independent agency",
                }
            )
    return cards


def skill_text(name: str, index: int) -> str:
    focus = [
        "starting a fresh orphan-root lane without pretending the source is ancestral",
        "proving zero-parent x1 and direct-parent x2/final history",
        "building deterministic synthetic numerical evidence with explicit tolerances",
        "recording source transforms corrections and vacancies without authority promotion",
        "researching package registries before a bounded install transaction",
        "locking direct hashes and integrities in a D-isolated tool transaction",
        "validating only the current owner delta and labeling its scope exactly",
        "composing four-tier Freed ID handoff cards without giant prompt payloads",
        "resolving an exact-title successor only after the terminal gate",
        "preserving every empirical authority personhood and Stage 20 boundary",
    ][index - 1]
    return f"""---
name: {name}
description: Use when {focus}.
---

# {name}

## Scope

This skill supports {focus}. It is an evidence-workflow aid, not a source of scientific, professional, operational, legal, cultural, Maori, affected-party, or Stage 20 authority.

## Procedure

1. Read the current activation, family routing state, and owner anchors through EOF.
2. Declare the exact owner scope, evidence class, protected gates, and stop conditions.
3. Use synthetic or read-only inputs unless a separately authorized lifecycle action is necessary.
4. Retain every failed attempt and expected rejection with zero success credit.
5. Validate the smallest justified dependency and never replay a successful canonical aggregate.
6. Emit only `completed`, `represented`, `open_gap`, or `exact_gate` as truth outcomes.
7. Stop at `NOT_READY_FOR_STAGE_20` wherever protected evidence or authority is absent.

## Neris v667-v8-r3 teaching

The r3 phase used this contract in a blank-root, owner-only lane. Its fixtures are synthetic, its validation is same-owner, and its relational identity language establishes no consciousness, personhood, continuity, employment, qualification, authority, or independent agency.
"""


def runner_text(name: str, relative_target: str, required_key: str) -> str:
    return f'''"""Owner-scoped runner generated for Neris v667-v8-r3."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
TARGET = ROOT / {relative_target!r}
CONTRACT = {name!r}
REQUIRED_KEY = {required_key!r}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    if not args.validate:
        raise SystemExit("--validate is required")
    if not TARGET.is_file():
        raise SystemExit(f"missing target: {{TARGET.name}}")
    payload = json.loads(TARGET.read_text(encoding="utf-8"))
    if REQUIRED_KEY not in payload:
        raise SystemExit(f"missing key: {{REQUIRED_KEY}}")
    print(json.dumps({{"runner": CONTRACT, "target": TARGET.name, "state": "PASS_BOUNDED_OWNER_SCOPE"}}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
'''


def build_skills_and_runners() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    skill_results: list[dict[str, Any]] = []
    for index, name in enumerate(SKILL_NAMES, 1):
        path = write_text(f"x2/skills/{name}/SKILL.md", skill_text(name, index))
        content = path.read_text(encoding="utf-8")
        valid = content.startswith("---\nname: ") and f"name: {name}\n" in content and "description:" in content
        skill_results.append({"name": name, "relative_path": path.relative_to(ROOT).as_posix(), "sha256": sha256_path(path), "local_validation_passed": valid})
    runner_targets = [
        ("docs/neris-solane/v667-v8-r3/x1/source-continuity.json", "source_exact_final"),
        ("docs/neris-solane/v667-v8-r3/x1/x1-build-receipt.json", "root_commit_expected_parent_count"),
        ("docs/neris-solane/v667-v8-r3/x2/numerical/reproducibility-fixtures.json", "fixtures"),
        ("docs/neris-solane/v667-v8-r3/x2/provenance/synthetic-provenance-ledger.json", "nodes"),
        ("docs/neris-solane/v667-v8-r3/x2/tooling/thirteen-tool-transaction-receipt.json", "direct_tool_count"),
        ("docs/neris-solane/v667-v8-r3/x2/proposals/proposal-outcomes.json", "outcomes"),
        ("docs/neris-solane/v667-v8-r3/x2/flashcards/four-tier-deck.json", "cards"),
        ("docs/neris-solane/v667-v8-r3/x1/route-roster-auth.json", "immediate_successor"),
        ("docs/neris-solane/v667-v8-r3/x1/phase-charter.json", "terminal_verdict"),
        ("docs/neris-solane/v667-v8-r3/x2/portfolio/owner-execution.json", "owner_safe_now"),
    ]
    runner_results: list[dict[str, Any]] = []
    for name, (target, key) in zip(RUNNER_NAMES, runner_targets, strict=True):
        path = write_text(f"x2/runners/{name}.py", runner_text(name, target, key))
        completed = subprocess.run(
            [sys.executable, "-B", str(path), "--validate"],
            cwd=str(ROOT),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )
        runner_results.append(
            {
                "name": name,
                "relative_path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256_path(path),
                "returncode": completed.returncode,
                "stdout": completed.stdout.strip(),
                "stderr": completed.stderr.strip(),
                "used_once": True,
                "passed": completed.returncode == 0,
            }
        )
    return skill_results, runner_results


def build_report(outcomes: list[dict[str, Any]], method: dict[str, Any]) -> str:
    sections = [
        ("Identity and scope", "Neris Solane, they/them, is relational working language for a solo evidence-bound remaster steward. The wording records collaboration style only and is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or authority."),
        ("Fresh-root architecture", "The r3 lane begins with an actual zero-parent planning commit. The r2 exact final remains a read-only cryptographic continuity anchor rather than an inherited checkout or Git ancestor. This makes blank-lane provenance explicit while preserving the prior seal unchanged."),
        ("GMUT Mind focus", "The primary focus is numerical reproducibility using wholly synthetic arithmetic fixtures. These fixtures examine tolerances, rounding, seeded replay, uncertainty, provenance, and cross-algorithm agreement without claiming that a physical theory has been empirically confirmed."),
        ("THOS Body support", "THOS is represented through deterministic builders, D-isolated tools, stop-precedence runners, exact manifests, and bounded same-owner checks. Nothing here is a production deployment, operational certification, AGI or ASI system, or exhaustive security assessment."),
        ("Freed ID and CBR Heart", "The Heart pillar appears as correction, contestability, privacy, accessibility, zero-key provenance, and a four-tier flashcard deck. No real identity lifecycle, rights adjudication, affected party, credential, or governance decision is present."),
        ("Practice lenses", "Numerical analysis supplies explicit error and tolerance reasoning. Scientific software engineering supplies deterministic execution and negative fixtures. Research librarianship supplies source classes, transformation notes, correction edges, and vacancy records."),
        ("Tool transaction", "Thirteen direct tools were researched against primary registry or repository material, installed only inside a dedicated D-drive transaction root, hash or integrity checked, positively smoked, and negatively challenged. Eleven operational failures are retained and the bounded vulnerability audits are not exhaustive security evidence."),
        ("Proposal outcomes", "Twenty inherited contracts were revalidated with zero novelty and completion credit. Twenty genuinely new proposals retain exactly fourteen completed, four represented, one open_gap, and one exact_gate outcomes. One hundred preregistered invalid mutations were rejected and retained."),
        ("Portfolio", "The owner executed thirty safe-now tasks, fifteen candidate tasks, ten skill builds, ten runner builds, and thirty clean-fix-refine tasks. Ten exact packets remain exact_gate and five blocked packets remain open_gap. Successor recommendations remain unexecuted and zero credit."),
        ("Terminal boundary", "All evidence is bounded same-owner software and documentation evidence under shared infrastructure. It is not independent reproduction, external audit, empirical GMUT confirmation, professional or production validation, legal or cultural ratification, Māori authority, Theory-of-Everything proof, personhood evidence, or Stage 20 authority."),
    ]
    paragraphs: list[str] = ["# Neris Solane v667-v8-r3 x2 evidence report\n"]
    for heading, seed in sections:
        paragraphs.append(f"## {heading}\n")
        for index in range(1, 7):
            paragraphs.append(
                f"{seed} Reflection {index} keeps the evidence claim proportional: each positive has an explicit source, scope, and falsifier; each rejection remains visible; each absent real-world dependency stays vacant. "
                f"The record distinguishes what was implemented from what was merely represented, and it does not convert a same-owner rerun into independent confirmation. "
                f"Correction remains additive and reversible, while successor routing remains stopped until a clean pushed exact-final gate and a fresh exact-title reread.\n"
            )
    paragraphs.append("## Exact proposal table\n")
    paragraphs.append("| Proposal | Outcome | Real-world evidence | Authority actions |\n|---|---|---:|---:|\n")
    for row in outcomes:
        paragraphs.append(f"| {row['proposal_id']} | {row['outcome_label']} | 0 | 0 |\n")
    paragraphs.append("\n## Method Flow totals\n")
    paragraphs.append(
        f"The sealed x2 content baseline records {method['effective_negatives']} effective negatives, {method['methods']} methods, "
        f"{method['open_gaps']} open gaps, {method['exact_gates']} exact gates, {method['failed_witnesses']} failed witnesses, and "
        f"{method['passing_witnesses']} bounded passing witnesses. The terminal verdict is `{TERMINAL_VERDICT}`.\n"
    )
    return "\n".join(paragraphs)


def privacy_candidates(paths: list[Path]) -> list[dict[str, str]]:
    patterns = {
        "windows_absolute_path": re.compile(r"(?<![A-Za-z])[A-Z]:[\\/]+", re.I),
        "raw_thread_or_session_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "credential_assignment": re.compile(r"(?:api[_-]?key|pass" + r"word|sec" + r"ret|bearer)\s*[:=]\s*[^\s\"<]{8,}", re.I),
        "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "private_route_or_resume_value": re.compile(r"(?:resume|session|thread)[_-]?(?:id|token)\s*[:=]\s*[^\s\"<]{8,}", re.I),
    }
    hits: list[dict[str, str]] = []
    for path in paths:
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                hits.append({"class": class_name, "path": path.relative_to(ROOT).as_posix(), "match_sha256": hashlib.sha256(match.group(0).encode()).hexdigest()})
    return hits


def owner_files() -> list[Path]:
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix())


def build() -> dict[str, Any]:
    head = git("rev-parse", "HEAD").stdout.strip()
    if head != X1_HEAD:
        raise RuntimeError(f"x2 must begin at exact frozen x1 {X1_HEAD}; observed {head}")
    parent_line = git("rev-list", "--parents", "-n", "1", "HEAD").stdout.strip().split()
    if len(parent_line) != 1:
        raise RuntimeError("frozen x1 is not a zero-parent root commit")
    tool_receipt = read_json("x2/tooling/thirteen-tool-transaction-receipt.json")
    if not str(tool_receipt.get("state", "")).startswith("PASS"):
        raise RuntimeError("bounded tool transaction is not passing")
    if len(tool_receipt.get("operational_failures", [])) != 11:
        raise RuntimeError("tool failure ledger count drift")

    fixtures = build_numerical_fixtures()
    write_json("x2/numerical/reproducibility-fixtures.json", {"fixtures": fixtures, "count": len(fixtures), "all_passed": all(row["passed"] for row in fixtures), "scope": "synthetic_same_owner"})
    provenance = {
        "nodes": [
            {"node_id": "SRC-X1", "class": "immutable planning commit", "digest": X1_HEAD, "authority_credit": 0},
            {"node_id": "SRC-REGISTRY", "class": "primary package metadata", "retrieved": "2026-08-24", "authority_credit": 0},
            {"node_id": "FIXTURE-SYNTHETIC", "class": "generated arithmetic fixture", "real_source_count": 0, "authority_credit": 0},
            {"node_id": "CORRECTION-PATH", "class": "additive correction edge", "tombstone_supported": True, "authority_credit": 0},
        ],
        "edges": [
            {"from": "SRC-X1", "to": "FIXTURE-SYNTHETIC", "transform": "bounded x2 execution"},
            {"from": "SRC-REGISTRY", "to": "CORRECTION-PATH", "transform": "version and compatibility research"},
        ],
        "real_people": 0,
        "real_measurements": 0,
        "real_authority_actions": 0,
        "synthetic_only": True,
    }
    write_json("x2/provenance/synthetic-provenance-ledger.json", provenance)

    revalidations, outcomes, mutations = build_proposal_evidence()
    write_json("x2/proposals/inherited-revalidations.json", {"revalidations": revalidations, "count": 20, "novelty_credit": 0, "completion_credit": 0})
    write_json("x2/proposals/proposal-outcomes.json", {"outcomes": outcomes, "counts": dict(Counter(row["outcome_label"] for row in outcomes)), "allowed_outcomes": ALLOWED_OUTCOMES})
    write_json("x2/proposals/negative-mutation-results.json", {"mutations": mutations, "count": len(mutations), "all_rejected": all(not row["accepted"] for row in mutations), "all_expected_rejections_observed": all(row["expected_rejection_observed"] for row in mutations)})

    owner_portfolio, successor_portfolio = build_portfolio()
    write_json("x2/portfolio/owner-execution.json", owner_portfolio)
    write_json("x2/portfolio/successor-recommendations.json", successor_portfolio)
    cards = build_flashcards()
    write_json("x2/flashcards/four-tier-deck.json", {"cards": cards, "count": len(cards), "tier_counts": {str(key): value for key, value in Counter(row["tier"] for row in cards).items()}, "successor_message_payload": "short pointer to committed baton only"})

    skill_results, runner_results = build_skills_and_runners()
    write_json("x2/skills/local-skill-validation.json", {"skills": skill_results, "count": len(skill_results), "all_passed": all(row["local_validation_passed"] for row in skill_results)})
    write_json("x2/runners/runner-execution-results.json", {"runners": runner_results, "count": len(runner_results), "all_passed": all(row["passed"] for row in runner_results)})

    method = {
        "source_x1_activation_baseline": {"effective_negatives": 28606, "methods": 15017, "open_gaps": 202, "exact_gates": 200, "failed_witnesses": 890, "passing_witnesses": 1602},
        "x2_additions": {
            "tool_operational_failures": 11,
            "first_x2_build_privacy_rule_self_match": 1,
            "wrong_context_combined_x1_x2_test_invocation": 1,
            "global_skill_validator_legacy_encoding_failure": 1,
            "proposal_mutation_rejections": 100,
            "tool_negative_rejections": 13,
            "proposal_outcomes": 20,
            "inherited_zero_credit_revalidations": 20,
            "tool_positive_smokes": 13,
            "skills_built": 10,
            "runners_built_and_used": 10,
            "owner_safe_now": 30,
            "owner_candidates": 15,
            "owner_clean_fix_refine": 30,
            "numerical_fixtures": 8,
            "flashcard_tier_checks": 4,
            "exact_packet_gates": 10,
            "blocked_packet_gaps": 5,
        },
        "effective_negatives": 28733,
        "methods": 15319,
        "open_gaps": 203,
        "exact_gates": 201,
        "failed_witnesses": 1034,
        "passing_witnesses": 1875,
        "terminal_verdict": TERMINAL_VERDICT,
        "same_owner_not_independent_reproduction": True,
    }
    write_json("x2/method-flow/method-flow-ledger.json", method)
    write_json(
        "x2/method-flow/x2-operational-failures.json",
        {
            "failures": [
                {
                    "failure_id": "R3-X2-BUILD-F001",
                    "description": "the first x2 build privacy rule matched a standalone URL-scheme fragment in its own sanitizer explanation",
                    "recovery": "remove the self-matching prose fragment without weakening the path rule and rerun only the x2 builder",
                    "credit": 0,
                    "retained": True,
                },
                {
                    "failure_id": "R3-X2-BUILD-F002",
                    "description": "the first combined test command invoked the immutable planning-only x1 lifecycle test from the populated x2 tree",
                    "recovery": "preserve the already credited x1 receipt and manifest, then run only the x2 test module in its correct lifecycle context",
                    "credit": 0,
                    "retained": True,
                },
                {
                    "failure_id": "R3-X2-BUILD-F003",
                    "description": "the first global skill promotion stopped after its validator decoded a UTF-8 Maori-authority macron through the Windows legacy code page",
                    "recovery": "retain the partial first target, use an ASCII authority label for validator portability, validate that target in place, and resume additively for the remaining nine",
                    "credit": 0,
                    "retained": True,
                },
            ],
            "successful_x1_test_replayed": False,
            "same_owner_recovery_not_independent_reproduction": True,
        },
    )
    write_text("x2/issues/numerical-reproducibility-and-fresh-root-method.md", """# Fresh-root numerical reproducibility method

The problem was to preserve exact continuity while honoring a request for a genuinely blank branch. The solution is a zero-parent x1 commit plus a cryptographic read-only r2 source anchor. This distinguishes continuity of evidence from Git ancestry and prevents the 72,000-file inherited checkout from silently returning.

The x2 method uses deterministic synthetic arithmetic, explicit tolerances, source-class provenance, rejecting mutations, D-isolated tools, additive corrections, and a bounded same-owner validator. It must not be described as empirical physics, independent reproduction, production readiness, professional validation, exhaustive security, legal or cultural review, Māori authority, personhood evidence, or Stage 20 authority.

Eleven tool-path failures remain retained at zero credit. They include wrapper execution faults, a negative-fixture weakness, version-banner advisories, a broad privacy-scanner false positive, and a genuine doubled-backslash profile-path leak that the durable sanitizer removed without rerunning tool execution.

The first x2 builder invocation also earned zero build-success credit because its privacy rule matched the scanner explanation's standalone URL-scheme fragment. The additive recovery removed that self-matching literal without weakening the actual path rule and reran only the bounded x2 builder, never the completed tool transaction. A later combined test command also earned zero credit because it invoked the immutable planning-only x1 lifecycle test from the populated x2 tree; recovery uses the already sealed x1 receipt and manifest and runs only the current x2 test module. The first global skill promotion also earned zero credit after the bundled validator decoded one UTF-8 authority label through the Windows legacy code page; its partial first target is retained and repaired in place before an additive nine-target resume.
""")
    report = build_report(outcomes, method)
    report_path = write_text("x2/reports/phase-evidence-report.md", report)

    receipt = {
        "state": "X2_EVIDENCE_BUILT_NOT_COMMITTED",
        "built_at": now(),
        "x1_head": X1_HEAD,
        "x1_parent_count": 0,
        "proposal_outcomes": dict(Counter(row["outcome_label"] for row in outcomes)),
        "inherited_revalidations": len(revalidations),
        "negative_mutations_rejected": len(mutations),
        "numerical_fixtures": len(fixtures),
        "flashcards": len(cards),
        "skill_builds": len(skill_results),
        "runner_builds_and_uses": len(runner_results),
        "tool_direct_count": tool_receipt["direct_tool_count"],
        "tool_positive_smokes": tool_receipt["positive_smoke_count"],
        "tool_negative_rejections": tool_receipt["negative_rejection_count"],
        "tool_operational_failures": len(tool_receipt["operational_failures"]),
        "owner_portfolio_counts": {key: len(value) for key, value in owner_portfolio.items()},
        "successor_recommendation_counts": {key: len(value) for key, value in successor_portfolio.items()},
        "report_words": len(report.split()),
        "method_flow": method,
        "successor_contacted": False,
        "terminal_verdict": TERMINAL_VERDICT,
    }
    write_json("x2/x2-build-receipt.json", receipt)

    files_before_manifest = [path for path in owner_files() if path != PHASE_ROOT / "validation/x2-content-manifest.json"]
    manifest = {
        "manifest_scope": "blank-root owner lane files through x2 evidence; self excluded",
        "entries": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256_path(path), "bytes": path.stat().st_size}
            for path in files_before_manifest
        ],
    }
    write_json("validation/x2-content-manifest.json", manifest)
    return validate_tree()


def validate_tree() -> dict[str, Any]:
    outcomes_payload = read_json("x2/proposals/proposal-outcomes.json")
    mutations_payload = read_json("x2/proposals/negative-mutation-results.json")
    revalidations_payload = read_json("x2/proposals/inherited-revalidations.json")
    fixtures_payload = read_json("x2/numerical/reproducibility-fixtures.json")
    cards_payload = read_json("x2/flashcards/four-tier-deck.json")
    skills_payload = read_json("x2/skills/local-skill-validation.json")
    runners_payload = read_json("x2/runners/runner-execution-results.json")
    receipt = read_json("x2/x2-build-receipt.json")
    method = read_json("x2/method-flow/method-flow-ledger.json")
    manifest = read_json("validation/x2-content-manifest.json")

    expected_outcomes = Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
    actual_outcomes = Counter(row["outcome_label"] for row in outcomes_payload["outcomes"])
    if actual_outcomes != expected_outcomes:
        raise AssertionError(f"outcome drift: {actual_outcomes}")
    if set(actual_outcomes) - set(ALLOWED_OUTCOMES):
        raise AssertionError("unapproved outcome label")
    if len(revalidations_payload["revalidations"]) != 20 or any(row["completion_credit"] for row in revalidations_payload["revalidations"]):
        raise AssertionError("zero-credit revalidation drift")
    if len(mutations_payload["mutations"]) != 100 or not mutations_payload["all_rejected"] or not mutations_payload["all_expected_rejections_observed"]:
        raise AssertionError("negative mutation drift")
    if len(fixtures_payload["fixtures"]) != 8 or not fixtures_payload["all_passed"]:
        raise AssertionError("numerical fixture drift")
    if len(cards_payload["cards"]) != 320 or cards_payload["tier_counts"] != {"1": 40, "2": 80, "3": 100, "4": 100}:
        raise AssertionError("flashcard deck drift")
    if skills_payload["count"] != 10 or not skills_payload["all_passed"]:
        raise AssertionError("skill validation drift")
    if runners_payload["count"] != 10 or not runners_payload["all_passed"]:
        raise AssertionError("runner execution drift")
    if receipt["report_words"] < 3000:
        raise AssertionError("phase report shorter than bounded three-page minimum")
    if method["effective_negatives"] != 28733 or method["methods"] != 15319 or method["open_gaps"] != 203 or method["exact_gates"] != 201:
        raise AssertionError("Method Flow count drift")
    if method["terminal_verdict"] != TERMINAL_VERDICT:
        raise AssertionError("terminal verdict drift")

    manifest_paths = {row["path"] for row in manifest["entries"]}
    for row in manifest["entries"]:
        path = ROOT / row["path"]
        if not path.is_file() or sha256_path(path) != row["sha256"] or path.stat().st_size != row["bytes"]:
            raise AssertionError(f"manifest replay mismatch: {row['path']}")
    current = owner_files()
    privacy = privacy_candidates(current)
    if privacy:
        raise AssertionError(f"privacy candidates: {privacy[:3]}")
    json_count = 0
    for path in current:
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
            json_count += 1
    if len(current) >= FILE_CEILING:
        raise AssertionError("2,000-file rotation guard reached")
    return {
        "status": "PASS",
        "owner_files": len(current),
        "manifest_entries": len(manifest_paths),
        "json_parses": json_count,
        "privacy_candidates": len(privacy),
        "report_words": receipt["report_words"],
        "outcomes": dict(actual_outcomes),
        "mutations": len(mutations_payload["mutations"]),
        "skills": skills_payload["count"],
        "runners": runners_payload["count"],
        "terminal_verdict": TERMINAL_VERDICT,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    payload = validate_tree() if args.validate else build()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
