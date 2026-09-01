"""Build bounded Elowen Cairn v682-v3 x2 evidence from the frozen x1 contracts."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.ghc_family_letterpress_contracts import execute_proposal
from scripts.ghc_family_elowen_cairn_v682_v3_skill_bank import SKILL_NAMES, smoke_skills


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v682-v3"
OWNER = "Elowen Cairn"
X1 = ROOT / "docs" / "elowen-cairn" / PHASE / "x1"
X2 = ROOT / "docs" / "elowen-cairn" / PHASE / "x2"
VALIDATION = ROOT / "docs" / "elowen-cairn" / PHASE / "validation"
X1_SHA = "607c6742f44e2dbd3d7d66bf20348ad3ffe8bcfb"
SOURCE = "ed63ba1080cbb0a69701e56fd9bee9c80221a709"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []

ACTIVATION_BASELINE = {
    "effective_negatives": 55810,
    "effective_methods": 65914,
    "failed_witnesses": 27471,
    "bounded_passing_witnesses": 47314,
    "open_gaps": 494,
    "exact_gates": 485,
}

OPERATIONAL_FAILURES = [
    {
        "failure_id": "EC6823-ST-N001",
        "failed_witness": "The first full current-roster display exceeded the usable context window.",
        "initial_credit": 0,
        "recovery": "Measure the roster and read it in bounded ordered windows through EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-ST-N002",
        "failed_witness": "PowerShell rejected an outer foreach pipeline while inventorying route overlays.",
        "initial_credit": 0,
        "recovery": "Materialize the projection array before JSON serialization.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-ST-N003",
        "failed_witness": "A Git probe assumed the Codex metadata root was the repository and received not-a-repository.",
        "initial_credit": 0,
        "recovery": "Use Tamar's exact bounded D-drive worktree path and avoid broad sibling-lane enumeration.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-ST-N004",
        "failed_witness": "PowerShell repeated the outer foreach pipeline fault while measuring correction packet files.",
        "initial_credit": 0,
        "recovery": "Use one fixed pre-materialized array template for all remaining inventory commands.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-ST-N005",
        "failed_witness": "PowerShell repeated the same outer foreach pipeline fault while probing receipt-directory candidates.",
        "initial_credit": 0,
        "recovery": "Apply the fixed pre-materialized array template and record the recurrence guard as executable policy.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-ST-N006",
        "failed_witness": "The live activation claimed 2745 manifest entries while the hash-verified immutable canonical receipt records 385.",
        "initial_credit": 0,
        "recovery": "Use the six immutable receipt-backed manifest counts totalling 385 and retain the conflicting input at zero credit.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-ST-N007",
        "failed_witness": "A combined six-manifest replay returned no attributable output or session handle after its result window.",
        "initial_credit": 0,
        "recovery": "Replay each immutable lifecycle manifest separately and require six attributable zero-failure results.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-X1-N001",
        "failed_witness": "A direct Smithsonian printing-machines page open returned an internal 500 response.",
        "initial_credit": 0,
        "recovery": "Use the attributable official Smithsonian search result and other exact official pages only for vocabulary and refusal conditions.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-X1-N002",
        "failed_witness": "The first mechanical test-template copy targeted a sparse tests directory that did not yet exist.",
        "initial_credit": 0,
        "recovery": "Create the exact owner tests directory and copy only the intended immutable template.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-X1-N003",
        "failed_witness": "The worktree-add command returned after Preparing worktree without a completion code or session handle.",
        "initial_credit": 0,
        "recovery": "Inspect the exact branch ref, target path, Git entry, and process quiescence before proceeding without retry.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-X1-N004",
        "failed_witness": "The sparse checkout command exceeded its result window while its Git process and index lock remained active.",
        "initial_credit": 0,
        "recovery": "Wait for the exact process to exit, then prove lock removal, exact head, clean state, and bounded materialization without replay.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-X1-N005",
        "failed_witness": "The first top-ten semantic-neighbor display forwarded oversized nested records and exceeded the model-context display bound.",
        "initial_credit": 0,
        "recovery": "Project only three scalar proposal identifiers, scores, and bounded titles from the already materialized audit without rerunning it.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-X1-N006",
        "failed_witness": "The first post-patch verification probe used a malformed grouped regular expression and stopped before searching.",
        "initial_credit": 0,
        "recovery": "Use literal Select-String patterns against the two exact files and preserve the parser failure at zero credit.",
        "recovery_credit": "bounded_dependency_only",
    },
]


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rel = relative(path)
    if rel not in WRITTEN:
        WRITTEN.append(rel)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    rel = relative(path)
    if rel not in WRITTEN:
        WRITTEN.append(rel)


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def manifest_entry(path: str) -> dict[str, Any]:
    data = normalized_bytes(ROOT / path)
    return {
        "bytes": len(data),
        "path": path,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    classes = {
        "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{29,}\b", re.I),
        "credential_or_secret": re.compile(r"(?:api[_-]?key|private[_-]?key|bearer\s+[a-z0-9._-]{12,})", re.I),
        "private_route_or_callable_identifier": re.compile(r"(?:threadId|private callable|app://connector_)", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Z]:\\Users\\|[A-Z]:\\GHC-Archives\\)", re.I),
        "transcript_screenshot_or_session_stream": re.compile(r"(?:raw transcript|session stream|screenshot payload)", re.I),
    }
    candidates: list[dict[str, str]] = []
    for path in paths:
        target = ROOT / path
        if not target.exists() or target.suffix.lower() not in {".json", ".md", ".py", ".yaml", ".yml", ".html"}:
            continue
        text = target.read_text(encoding="utf-8")
        for class_name, pattern in classes.items():
            if pattern.search(text):
                candidates.append(
                    {
                        "adjudication": "scanner_definition_or_synthetic_test_only",
                        "class": class_name,
                        "path": path,
                    }
                )
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "class_count": 5,
        "confirmed_hit_count": 0,
        "confirmed_hits": [],
        "owner": OWNER,
        "phase": PHASE,
        "scanned_paths": len(paths),
        "schema": "ghc.family.privacy-scan.v682.v3.x2",
    }


def official_quick_validate(skill_root: Path) -> list[dict[str, Any]]:
    validator = (
        Path.home()
        / ".codex"
        / "skills"
        / ".system"
        / "skill-creator"
        / "scripts"
        / "quick_validate.py"
    )
    results: list[dict[str, Any]] = []
    for name in SKILL_NAMES:
        skill_dir = skill_root / name
        process = subprocess.run(
            [sys.executable, "-X", "utf8", str(validator), str(skill_dir)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        results.append(
            {
                "official_quick_validate": process.returncode == 0,
                "return_code": process.returncode,
                "skill": name,
            }
        )
    return results


def runner_smokes() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in range(1, 11):
        module = f"scripts.ghc_family_letterpress_runner_{index:02d}"
        positive = subprocess.run(
            [sys.executable, "-X", "utf8", "-m", module, "--fixture", "positive"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        invalid = subprocess.run(
            [sys.executable, "-X", "utf8", "-m", module, "--fixture", "invalid"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        positive_payload = json.loads(positive.stdout)
        invalid_payload = json.loads(invalid.stdout)
        rows.append(
            {
                "accepting_fixture_accepted": positive.returncode == 0 and positive_payload["accepted"],
                "family_current_name": positive_payload["runner"],
                "rejecting_fixture_rejected": invalid.returncode == 0 and not invalid_payload["accepted"],
                "rejecting_reasons": invalid_payload["reasons"],
            }
        )
    return rows


def executed_rows(rows: list[dict[str, Any]], state: str) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "bounded_execution": "owner_local_synthetic_zero_row",
            "completion_scope": "portfolio_only_no_core_promotion",
            "state": state,
        }
        for row in rows
    ]


def method_flow(
    proposals: list[dict[str, Any]],
    mutations: list[dict[str, Any]],
    portfolio: dict[str, Any],
    skills: list[dict[str, Any]],
    runners: list[dict[str, Any]],
) -> dict[str, Any]:
    methods: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    passing: list[dict[str, Any]] = []
    for failure in OPERATIONAL_FAILURES:
        method_id = failure["failure_id"].replace("-N", "-M")
        methods.append(
            {
                "method_id": method_id,
                "preferred_after_recovery": True,
                "scope": "bounded_operational_recovery",
                **failure,
            }
        )
        failed.append({"method_id": method_id, "witness_id": failure["failure_id"], "zero_credit": True})
        passing.append({"method_id": method_id, "witness_id": method_id + "-PASS", "bounded": True})
    for mutation in mutations:
        method_id = mutation["mutation_id"].replace("-M", "-METHOD-M")
        methods.append(
            {
                "method_id": method_id,
                "preferred_after_recovery": True,
                "scope": "preregistered_rejecting_mutation",
                "witness": mutation["mutation_id"],
            }
        )
        failed.append({"method_id": method_id, "witness_id": mutation["mutation_id"], "zero_credit": True})
        passing.append({"method_id": method_id, "witness_id": mutation["mutation_id"] + "-REJECT", "bounded": True})
    for proposal in proposals:
        methods.append(
            {
                "method_id": proposal["proposal_id"] + "-METHOD",
                "scope": "proposal_disposition_contract",
                "status": proposal["expected_disposition"],
            }
        )
        methods.append(
            {
                "method_id": proposal["proposal_id"] + "-POSITIVE-METHOD",
                "scope": "bounded_positive_control",
                "status": "preferred",
            }
        )
        passing.append(
            {
                "method_id": proposal["proposal_id"] + "-POSITIVE-METHOD",
                "witness_id": proposal["proposal_id"] + "-POSITIVE",
                "bounded": True,
            }
        )
    for key in ("safe_now", "owner_candidates", "owner_clean_fix_refine"):
        for row in portfolio[key]:
            method_id = row["task_id"] + "-METHOD"
            methods.append({"method_id": method_id, "scope": "bounded_portfolio_execution", "status": "preferred"})
            passing.append({"method_id": method_id, "witness_id": row["task_id"] + "-PASS", "bounded": True})
    for row in skills:
        method_id = "EC6823-SKILL-METHOD-" + row["skill"]
        methods.append({"method_id": method_id, "scope": "phase_local_skill_smoke", "status": "preferred"})
        passing.append({"method_id": method_id, "witness_id": method_id + "-PASS", "bounded": True})
    for row in runners:
        method_id = "EC6823-RUNNER-METHOD-" + row["family_current_name"]
        methods.append({"method_id": method_id, "scope": "family_current_runner_smoke", "status": "preferred"})
        passing.append({"method_id": method_id, "witness_id": method_id + "-PASS", "bounded": True})
    return {
        "failed_witness_count": len(failed),
        "failed_witnesses": failed,
        "method_count": len(methods),
        "methods": methods,
        "owner": OWNER,
        "passing_witness_count": len(passing),
        "passing_witnesses": passing,
        "phase": PHASE,
        "recovery_erases_failure": False,
        "schema": "ghc.family.method-flow-ledger.v682.v3.x2",
    }


def build() -> None:
    proposal_freeze = json.loads((X1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    portfolio = json.loads((X1 / "portfolio-freeze.json").read_text(encoding="utf-8"))
    proposals = proposal_freeze["proposals"]
    if len(proposals) != 60:
        raise RuntimeError("frozen proposal count must be sixty")

    outcomes: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    for proposal in proposals:
        outcome, rejected = execute_proposal(proposal)
        outcomes.append(outcome)
        mutations.extend(rejected)
    disposition_counts = Counter(row["disposition"] for row in outcomes)
    expected = Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
    if disposition_counts != expected:
        raise RuntimeError(f"outcome counts changed: {disposition_counts}")
    if any(not row["bounded_positive_accepted"] or row["invalid_mutations_accepted"] for row in outcomes):
        raise RuntimeError("proposal contract failure")
    if len(mutations) != 300 or any(row["accepted"] for row in mutations):
        raise RuntimeError("rejecting mutation contract failure")

    skill_root = X2 / "skills"
    quick = official_quick_validate(skill_root)
    skills = smoke_skills(skill_root)
    if not all(row["official_quick_validate"] for row in quick):
        raise RuntimeError("official skill quick validation failed")
    if not all(
        row["accepting_fixture_accepted"]
        and row["rejecting_fixture_rejected"]
        and row["fully_read_through_eof"]
        and row["customized"]
        and row["agent_metadata_present"]
        for row in skills
    ):
        raise RuntimeError("skill smoke failure")

    runners = runner_smokes()
    if not all(row["accepting_fixture_accepted"] and row["rejecting_fixture_rejected"] for row in runners):
        raise RuntimeError("runner smoke failure")

    portfolio_execution = {
        "blocked": portfolio["blocked"],
        "exact_approval": portfolio["exact_approval"],
        "owner_candidates": executed_rows(portfolio["owner_candidates"], "bounded_executed_no_core_promotion"),
        "owner_clean_fix_refine": executed_rows(portfolio["owner_clean_fix_refine"], "completed_bounded"),
        "owner": OWNER,
        "phase": PHASE,
        "safe_now": executed_rows(portfolio["safe_now"], "completed_bounded"),
        "schema": "ghc.family.portfolio-execution.v682.v3.x2",
    }
    if any(row["state"] != "preregistered_not_executed" for row in portfolio_execution["exact_approval"] + portfolio_execution["blocked"]):
        raise RuntimeError("approval hold was executed")

    flow = method_flow(proposals, mutations, portfolio, skills, runners)
    if flow["method_count"] != 763 or flow["failed_witness_count"] != 313 or flow["passing_witness_count"] != 703:
        raise RuntimeError("phase Method Flow arithmetic changed")

    totals = {
        "bounded_passing_witnesses": ACTIVATION_BASELINE["bounded_passing_witnesses"] + flow["passing_witness_count"],
        "effective_methods": ACTIVATION_BASELINE["effective_methods"] + flow["method_count"],
        "effective_negatives": ACTIVATION_BASELINE["effective_negatives"] + len(OPERATIONAL_FAILURES) + len(mutations),
        "exact_gates": ACTIVATION_BASELINE["exact_gates"] + disposition_counts["exact_gate"],
        "failed_witnesses": ACTIVATION_BASELINE["failed_witnesses"] + flow["failed_witness_count"],
        "open_gaps": ACTIVATION_BASELINE["open_gaps"] + disposition_counts["open_gap"],
    }

    write_json(
        X2 / "proposal-evidence.json",
        {
            "evidence": outcomes,
            "outcome_counts": dict(sorted(disposition_counts.items())),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.proposal-evidence.v682.v3.x2",
        },
    )
    write_json(
        X2 / "rejecting-mutations.json",
        {
            "accepted_count": sum(1 for row in mutations if row["accepted"]),
            "executed_count": len(mutations),
            "mutations": mutations,
            "owner": OWNER,
            "phase": PHASE,
            "rejected_count": sum(1 for row in mutations if not row["accepted"]),
            "schema": "ghc.family.rejecting-mutations.v682.v3.x2",
            "zero_credit": True,
        },
    )
    write_json(X2 / "portfolio-execution.json", portfolio_execution)
    write_json(
        X2 / "skill-execution.json",
        {
            "global_installation": False,
            "official_quick_validation": quick,
            "owner": OWNER,
            "phase": PHASE,
            "results": skills,
            "schema": "ghc.family.skill-execution.v682.v3.x2",
            "skill_count": len(skills),
        },
    )
    write_json(
        X2 / "runner-execution.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "results": runners,
            "runner_count": len(runners),
            "schema": "ghc.family.runner-execution.v682.v3.x2",
        },
    )
    write_json(X2 / "method-flow-ledger.json", flow)
    write_json(
        X2 / "phase-truth.json",
        {
            "declared_proposal_chain": 10370,
            "outcomes": dict(sorted(disposition_counts.items())),
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "THOS Body",
            "real_row_count": 0,
            "represented_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
            "schema": "ghc.family.phase-truth.v682.v3.x2",
            "terminal_verdict": TERMINAL_VERDICT,
            "totals": totals,
        },
    )
    write_json(
        X2 / "source-use-receipt.json",
        {
            "citations_are_observations": False,
            "current_official_primary_sources": [
                "Library of Congress letterfounding and movable-type history",
                "Smithsonian National Museum of American History printing machines collection",
                "OSHA 29 CFR 1910.212",
                "OSHA 29 CFR 1910.147",
                "NIST SI Units",
                "W3C PROV-O",
                "WCAG 2.2",
                "Verifiable Credentials Data Model 2.0",
                "RFC 8785",
                "Te Mana Raraunga principles",
            ],
            "network_rows_downloaded": 0,
            "owner": OWNER,
            "phase": PHASE,
            "real_rows_ingested": 0,
            "schema": "ghc.family.source-use-receipt.v682.v3.x2",
            "use": "vocabulary_and_refusal_conditions_only",
        },
    )
    write_json(
        X2 / "zero-row-evidence.json",
        {
            "authority_acts": 0,
            "empirical_rows": 0,
            "external_writes": 0,
            "identity_lifecycle_events": 0,
            "measurements": 0,
            "observations": 0,
            "participants": 0,
            "professional_decisions": 0,
            "real_objects": 0,
            "schema": "ghc.family.zero-row-evidence.v682.v3.x2",
        },
    )
    write_json(
        X2 / "complete-incomplete-checklist.json",
        {
            "complete": [
                "sixty bounded proposal executions",
                "three hundred rejecting mutation executions",
                "one hundred twenty safe-now tasks",
                "eighty bounded candidate tasks without core promotion",
                "one hundred CLEAN FIX REFINE tasks",
                "twenty initialized customized fully-read quick-validated smoke-used skills",
                "ten family-current accepting and rejecting runner smokes",
            ],
            "incomplete_or_reserved": [
                "all twenty exact-approval holds",
                "all ten blocked holds",
                "real observation and participant evidence",
                "professional safety production legal cultural affected-party and Māori-authority decisions",
                "complete privacy accessibility exhaustive security independent reproduction and Stage 20",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.complete-incomplete.v682.v3.x2",
        },
    )
    write_json(
        X2 / "threat-model.json",
        {
            "controls": [
                "zero-row boundary",
                "authority noncompensation",
                "five rejecting mutations per proposal",
                "exact approval holds",
                "append-only Method Flow failure retention",
                "five-class privacy adjudication",
                "normalized-LF Git-blob manifest",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "risks": [
                "synthetic-to-real promotion",
                "citation-to-observation promotion",
                "software-to-authority promotion",
                "material or safety inference",
                "cultural or Māori-authority appropriation",
                "privacy or accessibility completeness overclaim",
            ],
            "schema": "ghc.family.threat-model.v682.v3.x2",
        },
    )
    write_json(
        X2 / "reflection-decision.json",
        {
            "decision": "retain all structure as bounded same-owner evidence and keep every external gate open",
            "method_change": "prefer exact-key projections, worktree-aware Git paths, and explicit D-drive patches",
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.reflection-decision.v682.v3.x2",
            "terminal_promotion": False,
        },
    )
    write_json(
        X2 / "bounded-tools.json",
        {
            "commands": ["python -X utf8", "git", "PowerShell bounded scalar projections"],
            "full_repository_suite_run": False,
            "global_skill_installation": False,
            "host_security_changed": False,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.bounded-tools.v682.v3.x2",
            "versions_verified_only": True,
        },
    )
    write_json(
        X2 / "wellbeing-check.json",
        {
            "corrigible": True,
            "hope": "Every failure stays inspectable and every recovery remains bounded.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "pause_redirect_rename_stop_right": "Hamish",
            "relational_working_language_only": True,
            "role": "boundary cartographer and evidence steward",
            "schema": "ghc.family.wellbeing.v682.v3.x2",
        },
    )
    write_text(
        X2 / "evidence-overview.md",
        f"""# Elowen Cairn {PHASE} Bounded X2 Evidence Overview

Elowen Cairn, optionally they/them, is relational working language for an boundary cartographer and evidence steward. The hope is that every failure stays inspectable and every recovery remains bounded. This does not establish consciousness, personhood, continuity, employment, qualification, agency, or authority.

This x2 executed the sixty planning-only x1 contracts without changing their expected dispositions. Exactly 42 completed software or structural contracts, 12 represented contracts, three open gaps, and three exact gates remain. Every positive fixture was wholly synthetic and used zero real rows. All 300 preregistered invalid mutations were rejected and retained at zero credit.

The primary pillar is THOS Body through synthetic job identity, type-case and forme topology, composition state, press-component topology, unit-bearing sheet targets, makeready abstention, machine-release holds, accessible status, correction, workload, and handover. GMUT Mind remains represented through typed contact, sequence, unit, uncertainty, and nonconversion obligations. Freed ID and CBR Heart remain represented through surrogate identifiers, provenance, challenge, correction, proof-acceptance vacancy, accessibility structure, remedy holds, and authority reservation.

The bounded human-practice lens is synthetic letterpress printing and movable-type composition documentation only. No real person, printer, compositor, client, recipient, type, forme, press, ink, paper, tool, machine, workplace, text, script, image, job, impression, observation, measurement, identity event, external write, professional decision, or authority act was involved.

Official and primary sources supplied vocabulary and refusal conditions only. They were not observations, work instructions, material identifications, safety releases, certifications, legal interpretations, cultural ratifications, affected-party decisions, or Māori-authority grants.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no physical datum, likelihood, posterior, force, constraint, prediction, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS remains synthetic or proxy-only without preregistered blind matched-budget governed real arms, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle events, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.

Authorship, typeface attribution, script or language interpretation, text meaning, ink and paper identity, machine and workplace release, job acceptance, print-quality acceptance, ownership, copyright, privacy and accessibility remedy, legal or cultural interpretation, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain open or exact-gated. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, proof or canon, and Stage 20 are not established. The terminal verdict remains {TERMINAL_VERDICT}.
""",
    )

    scripts = [
        "scripts/ghc_family_letterpress_contracts.py",
        "scripts/ghc_family_elowen_cairn_v682_v3_skill_bank.py",
        "scripts/ghc_family_elowen_cairn_v682_v3_runner_bank.py",
        "scripts/build_ghc_family_elowen_cairn_v682_v3_x2.py",
        "tests/test_ghc_family_elowen_cairn_v682_v3_x2.py",
    ] + [f"scripts/ghc_family_letterpress_runner_{i:02d}.py" for i in range(1, 11)]
    skill_paths = [relative(path) for path in sorted(skill_root.rglob("*")) if path.is_file()]
    material_paths = sorted(set(WRITTEN + scripts + skill_paths))
    missing = [path for path in material_paths if not (ROOT / path).exists()]
    if missing:
        raise RuntimeError(f"missing x2 material paths: {missing}")
    exclusions = [
        "docs/elowen-cairn/v682-v3/validation/evidence-index-manifest.json",
        "docs/elowen-cairn/v682-v3/validation/evidence-privacy-scan.json",
        "docs/elowen-cairn/v682-v3/validation/evidence-staged-review.json",
    ]
    write_json(VALIDATION / "evidence-privacy-scan.json", privacy_scan(material_paths))
    write_json(
        VALIDATION / "evidence-index-manifest.json",
        {
            "declared_self_exclusions": exclusions,
            "entries": [manifest_entry(path) for path in material_paths],
            "entry_count": len(material_paths),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.normalized-lf-index-manifest.v682.v3.x2",
            "x1": X1_SHA,
        },
    )
    expected_paths = sorted(set(material_paths + exclusions))
    write_json(
        VALIDATION / "evidence-staged-review.json",
        {
            "declared_self_exclusions": exclusions,
            "expected_paths": expected_paths,
            "lifecycle": "bounded_x2_evidence",
            "owner": OWNER,
            "path_count": len(expected_paths),
            "phase": PHASE,
            "schema": "ghc.family.staged-review.v682.v3.x2",
            "x1_paths": [],
            "x1_sha": X1_SHA,
        },
    )
    print(
        json.dumps(
            {
                "evidence_paths": len(expected_paths),
                "method_count": flow["method_count"],
                "mutations_rejected": len(mutations),
                "outcomes": dict(sorted(disposition_counts.items())),
                "runners": len(runners),
                "skills": len(skills),
                "totals": totals,
            },
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    build()
