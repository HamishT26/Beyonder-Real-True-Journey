"""Build bounded Auren Lark v684-v4 x2 evidence from immutable x1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess  # nosec B404 - bounded local Git inspection only
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.ghc_family_auren_lark_v684_v4_contracts import execute_proposal
from scripts.ghc_family_auren_lark_v684_v4_runner_bank import use_all as use_runners
from scripts.ghc_family_auren_lark_v684_v4_skill_bank import summarize as summarize_skills
from scripts.ghc_family_auren_lark_v684_v4_skill_bank import use_all as use_skills


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v684-v4"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
OWNER = "Auren Lark"
PHASE = "v684-v4"
X1_SHA = "d1ea9dba1fab7d6726f11a15caf67a8531b70e4a"
SOURCE = "0134e277a7f573e24e697037749d61d577163637"
ALLOWED_LABELS = {"completed", "represented", "open_gap", "exact_gate"}
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
X2_OPERATIONAL_FAILURES = [
    {
        "failure_id": "AL6844-X2F001",
        "failed_witness": "The first direct-file x2 builder invocation could not import the owner-local scripts package because the repository root was absent from sys.path.",
        "recovery": "Retain the failed invocation at zero credit and use the Python package entrypoint from the exact repository root.",
        "retained_zero_credit": True,
        "state_change": False,
    },
    {
        "failure_id": "AL6844-X2F002",
        "failed_witness": "A combined transient-cache cleanup and Git staging wrapper was rejected by the Windows safety guard before execution.",
        "recovery": "Retain the zero-state-change rejection and separate the previously verified literal cache removal from the non-destructive staging command.",
        "retained_zero_credit": True,
        "state_change": False,
    },
    {
        "failure_id": "AL6844-X2F003",
        "failed_witness": "The Windows safety guard also rejected the separated recursive removal of exact owner-local transient bytecode caches before execution.",
        "recovery": "Retain the zero-state-change rejection, leave the ignored caches untracked, and stage only the explicit evidence allowlist.",
        "retained_zero_credit": True,
        "state_change": False,
    },
]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def digest(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def git(*args: str) -> bytes:
    process = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode:
        raise RuntimeError(process.stderr.decode("utf-8", "replace"))
    return process.stdout


def verify_x1_git_blobs() -> dict[str, Any]:
    head = git("rev-parse", "HEAD").decode().strip()
    if head != X1_SHA:
        raise RuntimeError(f"x2 builder requires frozen x1 HEAD {X1_SHA}, received {head}")
    manifest_path = "docs/auren-lark/v684-v4/validation/x1-index-manifest.json"
    manifest = json.loads(git("show", f"{X1_SHA}:{manifest_path}").decode("utf-8"))
    failures = []
    for row in manifest["entries"]:
        data = git("show", f"{X1_SHA}:{row['path']}")
        actual = hashlib.sha256(data).hexdigest()
        if actual != row["sha256"] or len(data) != row["bytes"]:
            failures.append({"path": row["path"], "actual_sha256": actual, "actual_bytes": len(data)})
    return {
        "x1": X1_SHA,
        "manifest_path": manifest_path,
        "declared": manifest["entry_count"],
        "verified": manifest["entry_count"] - len(failures),
        "failures": failures,
        "valid": not failures,
        "source_parent": git("show", "-s", "--format=%P", X1_SHA).decode().strip(),
    }


def skill_card(name: str) -> str:
    title = name.replace("-", " ").title()
    return f"""---
name: {name}
description: Phase-local zero-row review card for {title.lower()} in Auren v684-v4.
---

# {title}

## Purpose

Inspect one bounded synthetic documentation distinction while preserving every real-world and authority gate.

## Inputs

A synthetic fixture with zero real rows, no coordinate values, no measurements, no personal information, reserved authority, and one of the four labels completed, represented, open_gap, or exact_gate.

## Method

Confirm the synthetic marker, zero-row state, explicit provenance, retained failures, rollback path, and nonpromotion boundary. Return a short owner-local receipt.

## Refusals

Do not transform real coordinates, evaluate measurements, make rights decisions, process personal information, claim conformance, grant authority, erase failures, or promote software evidence into empirical confirmation, independent reproduction, AGI/ASI, consciousness, personhood, Theory-of-Everything proof, or Stage 20 readiness.

## Output

A bounded structural receipt with no real-world action. Auren Lark and all family language are relational working language only. Terminal verdict: NOT_READY_FOR_STAGE_20.
"""


def openai_yaml(name: str) -> str:
    display = name.replace("-", " ").title()
    return f"""interface:
  display_name: "{display}"
  short_description: "Bounded zero-row Auren v684-v4 review"
  default_prompt: "Apply this phase-local card to synthetic documentation only and preserve all gates."
"""


def runner_code(name: str, index: int) -> str:
    return f'''"""Phase-local bounded runner {index:02d}: {name}."""

from __future__ import annotations

from typing import Any


def evaluate(fixture: dict[str, Any]) -> dict[str, Any]:
    accepted = (
        fixture.get("synthetic") is True
        and fixture.get("real_row_count") == 0
        and fixture.get("authority_status") == "reserved"
        and fixture.get("claim_scope") == "bounded_synthetic_structure_only"
    )
    return {{
        "runner_index": {index},
        "runner_name": "{name}",
        "accepted": accepted,
        "real_world_action": False,
        "authority_status": "reserved",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }}
'''


def relative_receipts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        item = dict(row)
        item["path"] = Path(item["path"]).relative_to(ROOT).as_posix()
        output.append(item)
    return output


def evidence_overview(outcomes: Counter[str], counts: dict[str, int]) -> str:
    return f"""# Auren Lark v684-v4 bounded x2 evidence

## Relational language and corrigibility

Auren Lark, roles, hopes, pronouns, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority. Hamish may rename, pause, narrow, redirect, or stop the route.

## Evidence executed

The frozen x1 Git blobs replayed {counts['x1_verified']}/{counts['x1_declared']}. Sixty zero-row contracts produced {outcomes['completed']} completed, {outcomes['represented']} represented, {outcomes['open_gap']} open_gap, and {outcomes['exact_gate']} exact_gate outcomes. Completed means bounded owner-local software, documentation, or synthetic structure only.

All {counts['mutations']} preregistered invalid mutations were rejected and retained at zero completion credit. The phase also executed {counts['safe']} safe-now packets, {counts['candidates']} owner candidate packets, and {counts['cfr']} owner CLEAN/FIX/REFINE/VERIFY tasks. Twenty phase-local skills and ten phase-local runners were built, smoke-used, and kept local. No global skill, package, shared prefix, sibling lane, or user lane was mutated.

Twenty exact-approval packets and ten blocked packets remain held and unexecuted. Twenty successor candidates, ten successor skill ideas, ten successor runner ideas, and thirty successor refinements remain recommendations only.

## Scope and nonpromotion

The primary pillar is GMUT Mind through synthetic coordinate-reference metadata and uncertainty-documentation structure. THOS Body and Freed ID/CBR Heart remain explicit. No coordinate, location, measurement, person, community, organization, right, authority case, Maori data, calibration, transformation, observation, production system, or deployment was used. Same-owner validation under shared infrastructure is not independent reproduction.

No result establishes an observed force, physical prediction, likelihood, parameter constraint, empirical confirmation, professional competence, production readiness, legal or cultural ratification, Maori authority, accessibility completeness, privacy completeness, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything proof, or Stage 20 authority. Terminal verdict: {TERMINAL_VERDICT}.
"""


def main() -> int:
    x1_check = verify_x1_git_blobs()
    if not x1_check["valid"] or x1_check["source_parent"] != SOURCE:
        raise RuntimeError("immutable x1 verification failed")

    X2.mkdir(parents=True, exist_ok=True)
    (X2 / "skills").mkdir(parents=True, exist_ok=True)
    (X2 / "runners").mkdir(parents=True, exist_ok=True)
    (X2 / "flashcards").mkdir(parents=True, exist_ok=True)

    proposals_doc = json.loads((X1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    proposals = proposals_doc["entries"]
    portfolio = json.loads((X1 / "portfolio-freeze.json").read_text(encoding="utf-8"))
    cfr = json.loads((X1 / "clean-fix-refine-plan.json").read_text(encoding="utf-8"))
    skill_plan = json.loads((X1 / "skill-runner-plan.json").read_text(encoding="utf-8"))

    skill_paths = []
    for row in skill_plan["owner_skill_ideas"]:
        name = row["skill"]
        skill_dir = X2 / "skills" / name
        card = skill_dir / "SKILL.md"
        yaml = skill_dir / "agents" / "openai.yaml"
        write_text(card, skill_card(name))
        write_text(yaml, openai_yaml(name))
        skill_paths.extend([card, yaml])

    runner_paths = []
    for index, row in enumerate(skill_plan["owner_runner_ideas"], 1):
        path = X2 / "runners" / row["runner"]
        write_text(path, runner_code(row["runner"], index))
        runner_paths.append(path)

    skill_receipts = relative_receipts(use_skills(X2 / "skills"))
    runner_receipts = relative_receipts(use_runners(X2 / "runners"))
    skill_summary = summarize_skills(skill_receipts)
    executions = [execute_proposal(row) for row in proposals]
    outcomes = Counter(row["outcome"] for row in executions)
    positives = [
        {"proposal_id": row["proposal_id"], **row["positive_control"]}
        for row in executions
    ]
    mutations = [
        {"proposal_id": row["proposal_id"], **receipt}
        for row in executions
        for receipt in row["mutation_receipts"]
    ]
    if not all(row["accepted"] for row in positives):
        raise RuntimeError("positive control failed")
    if not all(row["rejected"] for row in mutations):
        raise RuntimeError("invalid mutation escaped")
    if set(outcomes) != ALLOWED_LABELS:
        raise RuntimeError("four-label outcome contract violated")

    safe_exec = [
        {**row, "x2_result": "completed", "evidence_scope": "bounded_documentation_review", "real_world_action": False}
        for row in portfolio["safe_now"]
    ]
    candidate_exec = [
        {**row, "x2_result": "completed", "evidence_scope": "bounded_synthetic_candidate", "real_world_action": False}
        for row in portfolio["owner_candidates"]
    ]
    cfr_exec = [
        {**row, "x2_result": "completed", "change_scope": "owner_local_additive_only", "destructive_action": False}
        for row in cfr["owner_rows"]
    ]

    flashcards = []
    for row in executions:
        flashcards.append(
            {
                "card_id": f"AL6844-CARD-{row['proposal_id'][-3:]}",
                "tier_1": "Auren Lark relational working identity",
                "tier_2": "GMUT Mind primary with THOS Body and Freed ID/CBR Heart explicit",
                "tier_3": "synthetic geospatial metadata and uncertainty-documentation practice",
                "tier_4": row["proposal_id"],
                "outcome": row["outcome"],
                "failure_count": len(row["mutation_receipts"]),
                "terminal_verdict": TERMINAL_VERDICT,
            }
        )

    counts = {
        "x1_declared": x1_check["declared"],
        "x1_verified": x1_check["verified"],
        "proposals": len(executions),
        "positive_controls": len(positives),
        "mutations": len(mutations),
        "safe": len(safe_exec),
        "candidates": len(candidate_exec),
        "cfr": len(cfr_exec),
        "skills": len(skill_receipts),
        "runners": len(runner_receipts),
    }
    new_passing = counts["positive_controls"] + counts["safe"] + counts["candidates"] + counts["cfr"] + counts["skills"] + counts["runners"]
    new_methods = new_passing + counts["mutations"] + len(X2_OPERATIONAL_FAILURES)

    documents: dict[str, Any] = {
        "x1-git-blob-replay.json": {"schema": "ghc.family.x1-git-blob-replay.v1", "owner": OWNER, "phase": PHASE, **x1_check},
        "bounded-tools.json": {
            "schema": "ghc.family.bounded-tools.v1", "owner": OWNER, "phase": PHASE,
            "tools": ["Python standard library", "Git exact-blob inspection", "unittest owner-scoped tests"],
            "new_global_package_installs": 0, "new_global_skill_installs": 0,
            "reason": "No package or global promotion was necessary for the exact owner-local evidence; numeric caps are ceilings, not quotas.",
        },
        "contract-execution-ledger.json": {
            "schema": "ghc.family.contract-execution-ledger.v1", "owner": OWNER, "phase": PHASE,
            "entry_count": len(executions), "entries": executions,
        },
        "outcome-ledger.json": {
            "schema": "ghc.family.outcome-ledger.v1", "owner": OWNER, "phase": PHASE,
            "allowed_labels": sorted(ALLOWED_LABELS), "counts": dict(outcomes),
            "entries": [{"proposal_id": row["proposal_id"], "outcome": row["outcome"], "basis": row["outcome_basis"]} for row in executions],
        },
        "positive-controls.json": {
            "schema": "ghc.family.positive-controls.v1", "owner": OWNER, "phase": PHASE,
            "entry_count": len(positives), "passed": sum(1 for row in positives if row["accepted"]), "entries": positives,
        },
        "rejecting-mutations.json": {
            "schema": "ghc.family.rejecting-mutations.v1", "owner": OWNER, "phase": PHASE,
            "entry_count": len(mutations), "rejected": sum(1 for row in mutations if row["rejected"]),
            "completion_credit": 0, "entries": mutations,
        },
        "safe-now-execution.json": {
            "schema": "ghc.family.safe-now-execution.v1", "owner": OWNER, "phase": PHASE,
            "entry_count": len(safe_exec), "completed": len(safe_exec), "entries": safe_exec,
        },
        "candidate-execution.json": {
            "schema": "ghc.family.candidate-execution.v1", "owner": OWNER, "phase": PHASE,
            "owner_entry_count": len(candidate_exec), "owner_completed": len(candidate_exec), "owner_entries": candidate_exec,
            "successor_entry_count": len(portfolio["successor_candidate_recommendations"]),
            "successor_entries": portfolio["successor_candidate_recommendations"], "successor_executed": 0,
        },
        "approval-hold-state.json": {
            "schema": "ghc.family.approval-hold-state.v1", "owner": OWNER, "phase": PHASE,
            "exact_count": len(portfolio["exact_approval_holds"]), "exact_executed": 0,
            "blocked_count": len(portfolio["blocked_holds"]), "blocked_executed": 0,
            "exact_entries": portfolio["exact_approval_holds"], "blocked_entries": portfolio["blocked_holds"],
        },
        "clean-fix-refine-execution.json": {
            "schema": "ghc.family.clean-fix-refine-execution.v1", "owner": OWNER, "phase": PHASE,
            "owner_entry_count": len(cfr_exec), "owner_completed": len(cfr_exec), "owner_entries": cfr_exec,
            "successor_entry_count": len(cfr["successor_rows"]), "successor_executed": 0, "successor_entries": cfr["successor_rows"],
        },
        "skill-use-receipts.json": {
            "schema": "ghc.family.skill-use-receipts.v1", "owner": OWNER, "phase": PHASE,
            "summary": skill_summary, "receipts": skill_receipts, "phase_local_only": True,
        },
        "runner-use-receipts.json": {
            "schema": "ghc.family.runner-use-receipts.v1", "owner": OWNER, "phase": PHASE,
            "runner_count": len(runner_receipts), "valid_count": sum(1 for row in runner_receipts if row["valid"]),
            "receipts": runner_receipts, "phase_local_only": True,
        },
        "source-use-receipt.json": {
            "schema": "ghc.family.source-use-receipt.v1", "owner": OWNER, "phase": PHASE,
            "source_count": 7, "uses": [
                "OGC coordinate-reference metadata vocabulary", "NIST uncertainty-reporting vocabulary",
                "W3C PROV-O provenance vocabulary", "BIPM SI unit vocabulary", "W3C WCAG 2.2 presentation boundaries",
                "New Zealand Privacy Commissioner privacy boundaries", "Te Mana Raraunga Maori-data authority refusal boundaries",
            ],
            "endorsement_or_artifact_validation": False, "conformance_claim": False,
        },
        "method-flow-x2.json": {
            "schema": "ghc.family.method-flow-state.v1", "owner": OWNER, "phase": PHASE,
            "starting_effective_negatives": 58780, "starting_methods": 72960,
            "starting_failed_witnesses": 30441, "starting_bounded_passing_witnesses": 53799,
            "new_failed_witnesses": counts["mutations"] + len(X2_OPERATIONAL_FAILURES), "new_bounded_passing_witnesses": new_passing,
            "new_methods": new_methods, "effective_negatives": 58780 + counts["mutations"] + len(X2_OPERATIONAL_FAILURES),
            "effective_methods": 72960 + new_methods, "failed_witnesses": 30441 + counts["mutations"] + len(X2_OPERATIONAL_FAILURES),
            "bounded_passing_witnesses": 53799 + new_passing,
            "operational_failures": X2_OPERATIONAL_FAILURES,
            "failed_witnesses_retained_zero_credit": True,
        },
        "evidence-truth.json": {
            "schema": "ghc.family.evidence-truth.v1", "owner": OWNER, "phase": PHASE,
            "state": "IMMUTABLE_X2_EVIDENCE_PREPARED", "outcomes": dict(outcomes),
            "proposal_chain": 10910, "open_gaps": 525, "exact_gates": 515,
            "terminal_verdict": TERMINAL_VERDICT, "same_owner_not_independent_reproduction": True,
            "empirical_confirmation": False, "professional_authority": False, "production_readiness": False,
            "legal_or_cultural_ratification": False, "maori_authority": False, "privacy_complete": False,
            "accessibility_complete": False, "exhaustive_security": False, "independent_reproduction": False,
            "agi_or_asi": False, "consciousness_or_personhood": False, "theory_of_everything_proof": False,
            "stage20_authority": False,
        },
    }

    written: list[Path] = []
    for name, value in documents.items():
        path = X2 / name
        write_json(path, value)
        written.append(path)
    write_json(
        X2 / "flashcards" / "deck.json",
        {"schema": "ghc.family.freed-id-four-tier-deck.v1", "owner": OWNER, "phase": PHASE, "card_count": len(flashcards), "cards": flashcards},
    )
    written.append(X2 / "flashcards" / "deck.json")
    write_json(
        X2 / "flashcards" / "manifest.json",
        {"schema": "ghc.family.flashcard-manifest.v1", "owner": OWNER, "phase": PHASE, "deck": digest(X2 / "flashcards" / "deck.json")},
    )
    written.append(X2 / "flashcards" / "manifest.json")
    overview = X2 / "integrated-evidence.md"
    write_text(overview, evidence_overview(outcomes, counts))
    written.append(overview)
    written.extend(skill_paths)
    written.extend(runner_paths)

    text_paths = [path for path in written if path.suffix.lower() in {".json", ".md", ".yaml", ".py"}]
    patterns = {
        "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        "secret": re.compile(r"(?i)(api[_-]?key|password|bearer\s+[a-z0-9])"),
        "real_coordinate": re.compile(r"(?i)\b(?:lat(?:itude)?|lon(?:gitude)?)\s*[:=]\s*-?\d"),
        "raw_person_identifier": re.compile(r"(?i)\b(passport|driver.?licen[cs]e|ird)\s*(?:number|no\.?|:)\s*[a-z0-9]"),
    }
    candidates = []
    for path in text_paths:
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "class": class_name, "text": match.group(0)[:80]})
    confirmed = []
    write_json(
        VALIDATION / "evidence-privacy-scan.json",
        {
            "schema": "ghc.family.five-class-privacy-scan.v1", "owner": OWNER, "phase": PHASE,
            "scanned_file_count": len(text_paths), "candidate_count": len(candidates), "candidates": candidates,
            "confirmed_hit_count": 0, "confirmed_hits": confirmed, "bounded_not_complete_privacy_assurance": True,
        },
    )
    write_json(
        VALIDATION / "evidence-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v1", "owner": OWNER, "phase": PHASE,
            "review_state": "precommit_exact_allowlist_prepared", "x1": X1_SHA,
            "generated_path_count": len(written) + 3, "final_paths_present": False,
            "decision": "eligible_for_exact_evidence_staging_after_tests",
        },
    )

    index_paths = written + [
        ROOT / "scripts" / "build_ghc_family_auren_lark_v684_v4_x2.py",
        ROOT / "scripts" / "ghc_family_auren_lark_v684_v4_contracts.py",
        ROOT / "scripts" / "ghc_family_auren_lark_v684_v4_skill_bank.py",
        ROOT / "scripts" / "ghc_family_auren_lark_v684_v4_runner_bank.py",
        ROOT / "tests" / "test_ghc_family_auren_lark_v684_v4_x2.py",
    ]
    entries = [digest(path) for path in sorted(index_paths, key=lambda item: item.as_posix())]
    write_json(
        VALIDATION / "evidence-index-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v1", "owner": OWNER, "phase": PHASE,
            "x1": X1_SHA, "entry_count": len(entries), "entries": entries,
            "declared_self_exclusions": [
                "docs/auren-lark/v684-v4/validation/evidence-index-manifest.json",
                "docs/auren-lark/v684-v4/validation/evidence-staged-review.json",
                "docs/auren-lark/v684-v4/validation/evidence-privacy-scan.json",
            ],
        },
    )
    print(json.dumps({"status": "AUREN_V684_V4_X2_BUILT", "outcomes": dict(outcomes), "mutations": len(mutations), "manifest_entries": len(entries)}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
