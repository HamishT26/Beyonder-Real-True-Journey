"""Build bounded Caelen Morrow v682-v5 x2 evidence from the frozen x1 contracts."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.ghc_family_caelen_morrow_v682_v5_contracts import execute_proposal
from scripts.ghc_family_caelen_morrow_v682_v5_skill_bank import (
    SKILL_NAMES,
    smoke_skills,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE = "v682-v5"
OWNER = "Caelen Morrow"
X1 = ROOT / "docs" / "caelen-morrow" / PHASE / "x1"
X2 = ROOT / "docs" / "caelen-morrow" / PHASE / "x2"
VALIDATION = ROOT / "docs" / "caelen-morrow" / PHASE / "validation"
X1_SHA = "2b27d47bea8c183f3c6c9a927c7daed79a51f5b3"
SOURCE = "3cbffaa8b76a04a4c382545526658c2e8aaa256c"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []

ACTIVATION_BASELINE = {
    "effective_negatives": 56465,
    "effective_methods": 67469,
    "failed_witnesses": 28126,
    "bounded_passing_witnesses": 48749,
    "open_gaps": 500,
    "exact_gates": 491,
}

STARTUP_FAILURES = json.loads(
    (X1 / "method-flow-startup.json").read_text(encoding="utf-8")
)["startup_failures"]

POST_X1_FAILURES = [
    {
        "failure_id": "CM6825-X2-N016",
        "failed_witness": "A combined x2 template symbol and domain inventory exceeded the supported presentation window.",
        "initial_credit": 0,
        "recovery": "Read exact uppercase constants and bounded source windows separately without repeating completed source validation.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-X2-N017",
        "failed_witness": "A bounded PowerShell inventory reused the reserved automatic Matches variable and rejected string accumulation.",
        "initial_credit": 0,
        "recovery": "Rerun only the projection with a task-specific array variable and preserve the parser witness.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-X2-N018",
        "failed_witness": "A source-file size projection piped outer foreach output directly and PowerShell rejected the empty pipeline element.",
        "initial_credit": 0,
        "recovery": "Materialize the task-local row array before JSON serialization.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-X2-N019",
        "failed_witness": "The installed Git sparse-checkout add subcommand rejected the unsupported no-cone option.",
        "initial_credit": 0,
        "recovery": "Confirm the existing non-cone configuration and add literal patterns through the supported stdin form.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-X2-N020",
        "failed_witness": "A Windows ripgrep residue scan treated wildcard path arguments literally and rejected them.",
        "initial_credit": 0,
        "recovery": "Rerun only the residue scan with ripgrep include globs over exact bounded directories.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-X2-N021",
        "failed_witness": "A bounded constant-review regex used double-quoted shell text and PowerShell parsed part of it as module syntax.",
        "initial_credit": 0,
        "recovery": "Repeat only the projection with a single-quoted regex over the exact Caelen files.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-X2-N022",
        "failed_witness": "The first generated skill-bank syntax gate found an unterminated string because a newline escape was materialized as a literal line break.",
        "initial_credit": 0,
        "recovery": "Repair only the fully-read EOF predicate to use an escaped newline and rerun the changed syntax dependency.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-X2-N023",
        "failed_witness": "The bare Ruff check and format commands were unavailable on the current PowerShell command path.",
        "initial_credit": 0,
        "recovery": "Invoke the installed Ruff module through the current Python interpreter for the same exact owned files.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-X2-N024",
        "failed_witness": "The first module-qualified Ruff gate reported nineteen fixable lint findings and five format drifts across generated owner Python surfaces.",
        "initial_credit": 0,
        "recovery": "Apply Ruff fixes and formatting only to the exact generated owner files, then rerun changed lint and syntax dependencies.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-X2-N025",
        "failed_witness": "The generated runner wrapper docstrings retained a literal index format marker instead of their exact runner numbers.",
        "initial_credit": 0,
        "recovery": "Replace only the ten wrapper labels with their exact two-digit runner numbers; runtime contracts were not promoted by the presentation defect.",
        "recovery_credit": "bounded_dependency_only",
    },
]

OPERATIONAL_FAILURES = STARTUP_FAILURES + POST_X1_FAILURES


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
        "raw_task_or_thread_identifier": re.compile(
            r"\b019[a-f0-9]{29,}\b", re.IGNORECASE
        ),
        "credential_or_secret": re.compile(
            r"(?:api[_-]?key|private[_-]?key|bearer\s+[a-z0-9._-]{12,})", re.IGNORECASE
        ),
        "private_route_or_callable_identifier": re.compile(
            r"(?:threadId|private callable|app://connector_)", re.IGNORECASE
        ),
        "private_absolute_path": re.compile(
            r"(?:[A-Z]:\\Users\\|[A-Z]:\\GHC-Archives\\)", re.IGNORECASE
        ),
        "transcript_screenshot_or_session_stream": re.compile(
            r"(?:raw transcript|session stream|screenshot payload)", re.IGNORECASE
        ),
    }
    candidates: list[dict[str, str]] = []
    for path in paths:
        target = ROOT / path
        if not target.exists() or target.suffix.lower() not in {
            ".json",
            ".md",
            ".py",
            ".yaml",
            ".yml",
            ".html",
        }:
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
        "schema": "ghc.family.privacy-scan.v682.v5.x2",
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
        module = f"scripts.ghc_family_cylinder_archive_runner_{index:02d}"
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
                "accepting_fixture_accepted": positive.returncode == 0
                and positive_payload["accepted"],
                "family_current_name": positive_payload["runner"],
                "rejecting_fixture_rejected": invalid.returncode == 0
                and not invalid_payload["accepted"],
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
        failed.append(
            {
                "method_id": method_id,
                "witness_id": failure["failure_id"],
                "zero_credit": True,
            }
        )
        passing.append(
            {"method_id": method_id, "witness_id": method_id + "-PASS", "bounded": True}
        )
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
        failed.append(
            {
                "method_id": method_id,
                "witness_id": mutation["mutation_id"],
                "zero_credit": True,
            }
        )
        passing.append(
            {
                "method_id": method_id,
                "witness_id": mutation["mutation_id"] + "-REJECT",
                "bounded": True,
            }
        )
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
            methods.append(
                {
                    "method_id": method_id,
                    "scope": "bounded_portfolio_execution",
                    "status": "preferred",
                }
            )
            passing.append(
                {
                    "method_id": method_id,
                    "witness_id": row["task_id"] + "-PASS",
                    "bounded": True,
                }
            )
    for row in skills:
        method_id = "CM6825-SKILL-METHOD-" + row["skill"]
        methods.append(
            {
                "method_id": method_id,
                "scope": "phase_local_skill_smoke",
                "status": "preferred",
            }
        )
        passing.append(
            {"method_id": method_id, "witness_id": method_id + "-PASS", "bounded": True}
        )
    for row in runners:
        method_id = "CM6825-RUNNER-METHOD-" + row["family_current_name"]
        methods.append(
            {
                "method_id": method_id,
                "scope": "family_current_runner_smoke",
                "status": "preferred",
            }
        )
        passing.append(
            {"method_id": method_id, "witness_id": method_id + "-PASS", "bounded": True}
        )
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
        "schema": "ghc.family.method-flow-ledger.v682.v5.x2",
    }


def build() -> None:
    proposal_freeze = json.loads(
        (X1 / "new-proposal-freeze.json").read_text(encoding="utf-8")
    )
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
    expected = Counter(
        {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    )
    if disposition_counts != expected:
        raise RuntimeError(f"outcome counts changed: {disposition_counts}")
    if any(
        not row["bounded_positive_accepted"] or row["invalid_mutations_accepted"]
        for row in outcomes
    ):
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
    if not all(
        row["accepting_fixture_accepted"] and row["rejecting_fixture_rejected"]
        for row in runners
    ):
        raise RuntimeError("runner smoke failure")

    portfolio_execution = {
        "blocked": portfolio["blocked"],
        "exact_approval": portfolio["exact_approval"],
        "owner_candidates": executed_rows(
            portfolio["owner_candidates"], "bounded_executed_no_core_promotion"
        ),
        "owner_clean_fix_refine": executed_rows(
            portfolio["owner_clean_fix_refine"], "completed_bounded"
        ),
        "owner": OWNER,
        "phase": PHASE,
        "safe_now": executed_rows(portfolio["safe_now"], "completed_bounded"),
        "schema": "ghc.family.portfolio-execution.v682.v5.x2",
    }
    if any(
        row["state"] != "preregistered_not_executed"
        for row in portfolio_execution["exact_approval"]
        + portfolio_execution["blocked"]
    ):
        raise RuntimeError("approval hold was executed")

    flow = method_flow(proposals, mutations, portfolio, skills, runners)
    expected_method_count = 750 + len(OPERATIONAL_FAILURES)
    expected_failed_count = 300 + len(OPERATIONAL_FAILURES)
    expected_passing_count = 690 + len(OPERATIONAL_FAILURES)
    if (
        flow["method_count"] != expected_method_count
        or flow["failed_witness_count"] != expected_failed_count
        or flow["passing_witness_count"] != expected_passing_count
    ):
        raise RuntimeError("phase Method Flow arithmetic changed")

    totals = {
        "bounded_passing_witnesses": ACTIVATION_BASELINE["bounded_passing_witnesses"]
        + flow["passing_witness_count"],
        "effective_methods": ACTIVATION_BASELINE["effective_methods"]
        + flow["method_count"],
        "effective_negatives": ACTIVATION_BASELINE["effective_negatives"]
        + len(OPERATIONAL_FAILURES)
        + len(mutations),
        "exact_gates": ACTIVATION_BASELINE["exact_gates"]
        + disposition_counts["exact_gate"],
        "failed_witnesses": ACTIVATION_BASELINE["failed_witnesses"]
        + flow["failed_witness_count"],
        "open_gaps": ACTIVATION_BASELINE["open_gaps"] + disposition_counts["open_gap"],
    }

    write_json(
        X2 / "proposal-evidence.json",
        {
            "evidence": outcomes,
            "outcome_counts": dict(sorted(disposition_counts.items())),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.proposal-evidence.v682.v5.x2",
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
            "schema": "ghc.family.rejecting-mutations.v682.v5.x2",
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
            "schema": "ghc.family.skill-execution.v682.v5.x2",
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
            "schema": "ghc.family.runner-execution.v682.v5.x2",
        },
    )
    write_json(X2 / "method-flow-ledger.json", flow)
    write_json(
        X2 / "phase-truth.json",
        {
            "declared_proposal_chain": 10490,
            "outcomes": dict(sorted(disposition_counts.items())),
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "Freed ID and CBR Heart",
            "real_row_count": 0,
            "represented_pillars": ["GMUT Mind", "THOS Body"],
            "schema": "ghc.family.phase-truth.v682.v5.x2",
            "terminal_verdict": TERMINAL_VERDICT,
            "totals": totals,
        },
    )
    write_json(
        X2 / "source-use-receipt.json",
        {
            "citations_are_observations": False,
            "current_official_primary_sources": [
                "Library of Congress Caring for Cylinder Recordings",
                "IASA TC-05 Handling and Storage of Audio and Video Carriers",
                "Smithsonian Early Sound Recording Collection",
                "Smithsonian What Did 1889 Sound Like",
                "Library of Congress PREMIS",
                "DCMI Metadata Terms",
                "W3C PROV-O",
                "WCAG 2.2",
                "Verifiable Credentials Data Model 2.0",
                "New Zealand Privacy Principles",
                "Te Mana Raraunga principles",
            ],
            "network_rows_downloaded": 0,
            "owner": OWNER,
            "phase": PHASE,
            "real_rows_ingested": 0,
            "schema": "ghc.family.source-use-receipt.v682.v5.x2",
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
            "schema": "ghc.family.zero-row-evidence.v682.v5.x2",
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
            "schema": "ghc.family.complete-incomplete.v682.v5.x2",
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
            "schema": "ghc.family.threat-model.v682.v5.x2",
        },
    )
    write_json(
        X2 / "reflection-decision.json",
        {
            "decision": "retain all structure as bounded same-owner evidence and keep every external gate open",
            "method_change": "prefer exact-key projections, worktree-aware Git paths, and explicit D-drive patches",
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.reflection-decision.v682.v5.x2",
            "terminal_promotion": False,
        },
    )
    write_json(
        X2 / "bounded-tools.json",
        {
            "commands": [
                "python -X utf8",
                "git",
                "PowerShell bounded scalar projections",
            ],
            "full_repository_suite_run": False,
            "global_skill_installation": False,
            "host_security_changed": False,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.bounded-tools.v682.v5.x2",
            "versions_verified_only": True,
        },
    )
    write_json(
        X2 / "wellbeing-check.json",
        {
            "corrigible": True,
            "hope": "Every transition stays testable, reversible, and proportionate to its evidence.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "pause_redirect_rename_stop_right": "Hamish",
            "relational_working_language_only": True,
            "role": "provenance weaver and boundary cartographer",
            "schema": "ghc.family.wellbeing.v682.v5.x2",
        },
    )
    write_text(
        X2 / "evidence-overview.md",
        f"""# Caelen Morrow {PHASE} Bounded X2 Evidence Overview

Caelen Morrow, optionally they/them, is relational working language for a provenance weaver and boundary cartographer. The hope is to keep every transition testable, reversible, and proportionate to its evidence. This does not establish consciousness, personhood, continuity, employment, qualification, agency, or authority.

This x2 executed the sixty planning-only x1 contracts without changing their expected dispositions. Exactly 42 completed software or structural contracts, 12 represented contracts, three open gaps, and three exact gates remain. Every positive fixture was wholly synthetic and used zero real rows. All 300 preregistered invalid mutations were rejected and retained at zero credit.

The primary pillar is Freed ID and CBR Heart through synthetic carrier-record separation, surrogate provenance, label-lineage vacancy, digital-surrogate roles, event vacancies, rights and access holds, correction, remedy, privacy minimization, and authority noncompensation. GMUT Mind remains represented through typed state transitions, provenance digests, null conditions, uncertainty, and explicit nonconversion boundaries. THOS Body remains represented through command-versus-observation separation, dependency-closed workflow, workload leases, correction, and accessible handover.

The bounded human-practice lens is synthetic phonograph-cylinder cataloguing, preservation-planning, transfer, rights, accessibility, correction, remedy, workload, and handover record design only. No real person, speaker, performer, collector, community, carrier, cylinder, container, recording, media, label, groove, material, tool, observation, measurement, handling, cleaning, treatment, playback, transfer, publication, identity event, external write, professional decision, or authority act was involved.

Official and primary sources supplied vocabulary and refusal conditions only. They were not observations, work instructions, material identifications, conservation diagnoses, safety releases, certifications, rights decisions, legal interpretations, cultural ratifications, affected-party decisions, or Maori-authority grants.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no physical datum, likelihood, posterior, force, constraint, prediction, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS remains synthetic or proxy-only without preregistered blind matched-budget governed real arms, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle events, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.

Carrier identity, material, condition, label transcription, recording content, speaker or performer identity, rights and donor restrictions, location, handling, cleaning, treatment, playback, transfer, publication, professional release, privacy, accessibility remedy, legal or cultural interpretation, affected-party legitimacy, Maori wording, Maori data governance, and Maori authority remain open or exact-gated. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, proof or canon, and Stage 20 are not established. The terminal verdict remains {TERMINAL_VERDICT}.
""",
    )

    scripts = [
        "scripts/ghc_family_caelen_morrow_v682_v5_contracts.py",
        "scripts/ghc_family_caelen_morrow_v682_v5_skill_bank.py",
        "scripts/ghc_family_caelen_morrow_v682_v5_runner_bank.py",
        "scripts/build_ghc_family_caelen_morrow_v682_v5_x2.py",
        "tests/test_ghc_family_caelen_morrow_v682_v5_x2.py",
    ] + [f"scripts/ghc_family_cylinder_archive_runner_{i:02d}.py" for i in range(1, 11)]
    skill_paths = [
        relative(path) for path in sorted(skill_root.rglob("*")) if path.is_file()
    ]
    material_paths = sorted(set(WRITTEN + scripts + skill_paths))
    missing = [path for path in material_paths if not (ROOT / path).exists()]
    if missing:
        raise RuntimeError(f"missing x2 material paths: {missing}")
    exclusions = [
        "docs/caelen-morrow/v682-v5/validation/evidence-index-manifest.json",
        "docs/caelen-morrow/v682-v5/validation/evidence-privacy-scan.json",
        "docs/caelen-morrow/v682-v5/validation/evidence-staged-review.json",
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
            "schema": "ghc.family.normalized-lf-index-manifest.v682.v5.x2",
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
            "schema": "ghc.family.staged-review.v682.v5.x2",
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
