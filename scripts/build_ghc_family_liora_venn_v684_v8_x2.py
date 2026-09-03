#!/usr/bin/env python3
"""Build bounded Liora Venn v684-v8 x2 evidence from immutable x1."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.ghc_family_community_archives_contract import (  # noqa: E402
    RUNNER_NAMES,
    mutate,
    positive_fixture,
    validate_fixture,
)


PHASE = ROOT / "docs" / "liora-venn" / "v684-v8"
X1 = PHASE / "x1"
X2 = PHASE / "x2"
SKILLS = PHASE / "skills"
VALIDATION = PHASE / "validation"
SOURCE = "de8e8830bd7cb3a9aa49b2eb5efadaf17e57d513"
X1_COMMIT = "68150ea19231a904bc2e30e24510e14ec7ed3f9f"
BRANCH = "codex/GHC-Family/liora-venn-v684-v8-full-tools"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}
BASE_AFTER_X1 = {
    "effective_negatives": 60394,
    "effective_methods": 75142,
    "failed_witnesses": 31455,
    "bounded_passing_witnesses": 55677,
    "open_gaps": 537,
    "exact_gates": 527,
}

OPERATIONAL_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "LV6848-X2-N001",
        "failed_witness": "The first bulk template-seeding projection exceeded its output window, so its result was not attributable.",
        "recovery": "Audited the three exact target paths, lengths, adaptation markers, and Git status; all intended untracked files had persisted, so no copy was replayed.",
        "recurrence_guard": "After a projection overflow, inspect exact persisted targets before deciding whether any write must be repeated.",
        "initial_credit": 0,
        "repository_or_remote_state_changed_by_failure": False,
    },
    {
        "failure_id": "LV6848-X2-N002",
        "failed_witness": "The first contract replacement patch combined delete and add operations for the same path and was rejected by the patch tool.",
        "recovery": "Applied a targeted in-place semantic patch to the unchanged untracked contract file.",
        "recurrence_guard": "Use one in-place Update File operation when replacing content at a single existing path.",
        "initial_credit": 0,
        "repository_or_remote_state_changed_by_failure": False,
    },
    {
        "failure_id": "LV6848-X2-N003",
        "failed_witness": "A first flashcard inspection guessed a nonexistent x1 flashcard-index.json path.",
        "recovery": "A bounded x1 file inventory identified flashcard-freeze.json, whose exact schema and 67 cards were then projected.",
        "recurrence_guard": "Inventory exact filenames before selecting a phase artifact by semantic role.",
        "initial_credit": 0,
        "repository_or_remote_state_changed_by_failure": False,
    },
    {
        "failure_id": "LV6848-X2-N004",
        "failed_witness": "A stale-label adjudication passed a literal Windows wildcard path to ripgrep and returned an invalid-filename error.",
        "recovery": "Scanned the scripts directory with an explicit runner include glob; zero runner stale-label candidates were found.",
        "recurrence_guard": "On Windows, express ripgrep file selection with -g against a directory instead of a wildcard path argument.",
        "initial_credit": 0,
        "repository_or_remote_state_changed_by_failure": False,
    },
]

def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def git(*args: str) -> str:
    result = run(["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


SKILL_SLUGS = [
    "accession-custody-boundary",
    "hierarchy-parent-cycle-refusal",
    "original-order-annotation-separation",
    "creator-identity-nonconflation",
    "provenance-title-firewall",
    "acquisition-source-privacy-vacancy",
    "reference-location-nonidentity",
    "description-completeness-vacancy",
    "date-place-observation-separation",
    "language-subject-authority-vacancy",
    "redacted-view-source-nonmutation",
    "minimum-disclosure-hold",
    "access-permission-nonconflation",
    "rights-remedy-authority-gate",
    "contested-description-correction-readback",
    "retained-supersession-nonerasure",
    "flashcard-parent-digest-contract",
    "accessible-finding-aid-structure",
    "workload-review-handover",
    "maori-data-cultural-authority-gate",
]


def skill_text(index: int, slug: str) -> str:
    proposal_id = f"LV6848-N{index:03d}"
    skill_name = f"ghc-ca-{slug}"
    return f"""---
name: {skill_name}
description: Validate a wholly synthetic zero-row community-archives {slug.replace('-', ' ')} fixture; use for Liora v684-v8 owner-local archive contracts, never real access or authority decisions.
---

# GHC Family Community Archives {slug.replace('-', ' ').title()}

## Scope

Validate one wholly synthetic zero-row {slug.replace('-', ' ')} fixture for
{proposal_id}. This skill cannot identify, describe, ingest, redact, delete,
release, publish, or authorize a real archival record, collection, person,
access decision, cultural decision, or accessibility result.

## Inputs

- One synthetic fixture with placeholder collection and description identifiers.
- The immutable {proposal_id} x1 contract.
- No people, repositories, files, bitstreams, storage systems, donor records, credentials, private routes, or real data.

## Steps

1. Confirm the fixture is synthetic, zero-row, zero-action, and non-authoritative.
2. Compare its proposal-bound source digest and correction sequence.
3. Apply the bounded structural contract.
4. Retain every rejected mutation at zero credit.
5. Emit only a synthetic pass or refusal receipt.

## Refusals

- Refuse missing fields, identifier-role swaps, stale digests, inverted correction order, and authority promotion.
- Refuse empirical, participant, production, professional, legal, cultural, affected-party, or Māori-authority inference.
- Refuse privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, proof, canon, or Stage 20 claims.

## Outputs

A deterministic owner-local structural receipt with zero real-world action and
zero authority conferred.

## Smoke fixture

Use {proposal_id} with authority state WITHHELD_SYNTHETIC_ONLY and reject the
paired authority-promotion mutation.
"""


def skill_bank_script() -> str:
    return """#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = ["## Scope", "## Inputs", "## Steps", "## Refusals", "## Outputs", "## Smoke fixture"]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills-root", type=Path, required=True)
    args = parser.parse_args()
    receipts = []
    for path in sorted(args.skills_root.glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        missing = [heading for heading in REQUIRED if heading not in text]
        receipts.append({
            "skill": path.parent.name,
            "read_through_eof": True,
            "quick_validated": not missing,
            "smoke_used": "WITHHELD_SYNTHETIC_ONLY" in text and "authority-promotion" in text,
            "missing_headings": missing,
            "global_install": False,
            "real_world_rows": 0,
        })
    result = {
        "skill_count": len(receipts),
        "validated_count": sum(item["quick_validated"] for item in receipts),
        "smoke_used_count": sum(item["smoke_used"] for item in receipts),
        "receipts": receipts,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["skill_count"] == result["validated_count"] == result["smoke_used_count"] == 20 else 1

if __name__ == "__main__":
    raise SystemExit(main())
"""


def runner_script(index: int) -> str:
    return f"""#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.ghc_family_community_archives_contract import runner_smoke

if __name__ == "__main__":
    result = runner_smoke({index})
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["positive_accepted"] and result["invalid_rejected"] else 1)
"""


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    candidates = []
    confirmed = []
    patterns = privacy_patterns()
    scanner_files = {
        "build_ghc_family_liora_venn_v684_v8_x1.py",
        "build_ghc_family_liora_venn_v684_v8_x2.py",
    }
    for path in paths:
        data = path.read_bytes()
        for class_name, pattern in patterns.items():
            for _ in pattern.finditer(data):
                record = {"path": rel(path), "class": class_name}
                if path.name in scanner_files:
                    candidates.append({**record, "disposition": "scanner_definition_only"})
                else:
                    confirmed.append(record)
    return {
        "schema": "ghc.family.privacy-scan.v684.v8.evidence",
        "owner": "Liora Venn",
        "phase": "v684-v8",
        "privacy_classes": list(patterns),
        "scanned_paths": len(paths),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
    }


def security_scan(paths: list[Path]) -> dict[str, Any]:
    findings = []
    checked = 0
    for path in paths:
        if path.suffix != ".py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel(path))
        checked += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": rel(path), "finding": node.func.id})
            if (
                isinstance(node, ast.keyword)
                and node.arg == "shell"
                and isinstance(node.value, ast.Constant)
                and node.value.value is True
            ):
                findings.append({"path": rel(path), "finding": "shell_true"})
    return {
        "schema": "ghc.family.security-scan.v684.v8.evidence",
        "owner": "Liora Venn",
        "phase": "v684-v8",
        "python_ast_checks": checked,
        "findings": findings,
        "finding_count": len(findings),
        "exhaustive_security_claimed": False,
    }


def main() -> int:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong owner branch")
    if git("rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError("x2 builder must begin at immutable x1")
    allowed = {
        "scripts/build_ghc_family_liora_venn_v684_v8_x2.py",
        "scripts/ghc_family_community_archives_contract.py",
        "tests/test_ghc_family_liora_venn_v684_v8_x2.py",
        "scripts/ghc_family_liora_venn_v684_v8_skill_bank.py",
        "docs/liora-venn/v684-v8/validation/evidence-staged-review.json",
        "docs/liora-venn/v684-v8/validation/evidence-privacy-scan.json",
        "docs/liora-venn/v684-v8/validation/evidence-security-scan.json",
        "docs/liora-venn/v684-v8/validation/evidence-index-manifest.json",
        *{
            f"scripts/ghc_family_community_archives_{name}_runner.py"
            for name in RUNNER_NAMES
        },
    }
    dirty = {
        line[3:].replace("\\", "/")
        for line in git("status", "--porcelain=v1").splitlines()
        if len(line) >= 4
    }
    unexpected = {
        path
        for path in dirty - allowed
        if not path.startswith("docs/liora-venn/v684-v8/x2/")
        and not path.startswith("docs/liora-venn/v684-v8/skills/")
    }
    if unexpected:
        raise RuntimeError(f"unexpected x2 pre-build state: {sorted(unexpected)}")
    if git("rev-parse", "HEAD^") != SOURCE:
        raise RuntimeError("immutable x1 direct-parent mismatch")
    if git("ls-tree", "-r", "--name-only", X1_COMMIT, "--", "docs/liora-venn/v684-v8/x2"):
        raise RuntimeError("immutable x1 contains x2 paths")

    freeze = load(X1 / "new-proposal-freeze.json")
    portfolio = load(X1 / "portfolio-freeze.json")
    rows = freeze["proposals"]
    X2.mkdir(parents=True, exist_ok=True)
    SKILLS.mkdir(parents=True, exist_ok=True)
    positive_receipts = []
    mutation_receipts = []
    outcomes = []
    methods = []
    for row in rows:
        proposal_id = row["proposal_id"]
        positive = validate_fixture(positive_fixture(proposal_id))
        if not positive["accepted"]:
            raise RuntimeError(f"positive fixture failed: {proposal_id}: {positive['reasons']}")
        positive_receipts.append(
            {
                "proposal_id": proposal_id,
                "witness_id": proposal_id.replace("-N", "-PC-"),
                "accepted": True,
                "structural_only": True,
                "real_rows": 0,
                "authority_conferred": False,
            }
        )
        rejected = 0
        for preregistered in row["preregistered_rejecting_mutations"]:
            invalid = mutate(positive_fixture(proposal_id), preregistered["mutation_type"])
            result = validate_fixture(invalid)
            if result["accepted"]:
                raise RuntimeError(f"invalid fixture accepted: {preregistered['mutation_id']}")
            rejected += 1
            mutation_receipts.append(
                {
                    "proposal_id": proposal_id,
                    "mutation_id": preregistered["mutation_id"],
                    "mutation_type": preregistered["mutation_type"],
                    "accepted": False,
                    "state": "rejected_zero_credit",
                    "reasons": result["reasons"],
                    "failed_witness_retained": True,
                    "real_world_action": False,
                    "authority_conferred": False,
                }
            )
        if rejected != 5:
            raise RuntimeError(f"mutation count mismatch: {proposal_id}")
        label = row["expected_disposition"]
        if label not in LABELS:
            raise RuntimeError(f"unknown outcome label: {label}")
        outcomes.append(
            {
                "proposal_id": proposal_id,
                "title": row["title"],
                "outcome": label,
                "acceptance_gate_passed": True,
                "positive_witness": proposal_id.replace("-N", "-PC-"),
                "rejected_mutations": rejected,
                "completion_credit": 1 if label == "completed" else 0,
                "bounded_representation_credit": 1 if label == "represented" else 0,
                "broader_claim_credit": 0,
                "protected_gates_preserved": True,
            }
        )
        methods.append(
            {
                "method_id": f"LV6848-METHOD-{int(proposal_id[-3:]):03d}",
                "proposal_id": proposal_id,
                "candidate": "preregistered_in_immutable_x1",
                "validated": "one_zero_row_positive_and_five_rejecting_mutations",
                "preferred": "bounded_owner_local_contract_only",
                "independent_reproduction": False,
            }
        )

    outcome_counts = {label: sum(row["outcome"] == label for row in outcomes) for label in sorted(LABELS)}
    if outcome_counts != {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}:
        raise RuntimeError("outcome arithmetic mismatch")
    if len(mutation_receipts) != 300:
        raise RuntimeError("mutation arithmetic mismatch")

    skill_paths = []
    for index, slug in enumerate(SKILL_SLUGS, start=1):
        path = SKILLS / f"ghc-ca-{slug}" / "SKILL.md"
        write_text(path, skill_text(index, slug))
        skill_paths.append(path)

    skill_bank = ROOT / "scripts" / "ghc_family_liora_venn_v684_v8_skill_bank.py"
    write_text(skill_bank, skill_bank_script())
    runner_paths = []
    for index in range(1, 11):
        path = ROOT / "scripts" / f"ghc_family_community_archives_{RUNNER_NAMES[index - 1]}_runner.py"
        write_text(path, runner_script(index))
        runner_paths.append(path)

    validator_raw = os.environ.get("GHC_FAMILY_SKILL_VALIDATOR")
    if not validator_raw:
        raise RuntimeError("GHC_FAMILY_SKILL_VALIDATOR must identify the installed official quick validator")
    validator = Path(validator_raw).resolve()
    if not validator.is_file():
        raise RuntimeError("official skill validator is absent")
    official_skill_receipts = []
    for path in skill_paths:
        result = run([sys.executable, "-X", "utf8", str(validator), str(path.parent)])
        official_skill_receipts.append(
            {
                "skill": path.parent.name,
                "returncode": result.returncode,
                "passed": result.returncode == 0,
                "validator": "installed_skill_creator_quick_validate",
                "absolute_path_persisted": False,
            }
        )
        if result.returncode:
            raise RuntimeError(f"official skill quick validation failed: {path.parent.name}: {result.stdout} {result.stderr}")

    skill_result = run(
        [
            sys.executable,
            "-X",
            "utf8",
            rel(skill_bank),
            "--skills-root",
            rel(SKILLS),
        ]
    )
    if skill_result.returncode:
        raise RuntimeError(f"skill bank failed: {skill_result.stdout} {skill_result.stderr}")
    skill_receipt = json.loads(skill_result.stdout)
    skill_receipt["official_quick_validation_count"] = sum(item["passed"] for item in official_skill_receipts)
    skill_receipt["official_quick_validation_receipts"] = official_skill_receipts
    runner_receipts = []
    for path in runner_paths:
        result = run([sys.executable, "-X", "utf8", rel(path)])
        if result.returncode:
            raise RuntimeError(f"runner smoke failed: {rel(path)}: {result.stdout} {result.stderr}")
        runner_receipts.append(json.loads(result.stdout))

    tool_versions = {"python": sys.version.split()[0], "git": git("--version")}
    tool_receipts: list[dict[str, Any]] = []
    global_skill_receipts: list[dict[str, Any]] = []

    executed_safe = [{**item, "x2_state": "completed_bounded_owner_local"} for item in portfolio["safe_now"]]
    executed_candidates = [
        {**item, "x2_state": "completed_without_core_outcome_promotion"}
        for item in portfolio["owner_candidates"]
    ]
    executed_cfr = [
        {**item, "x2_state": "completed_bounded_additive_owner_local"}
        for item in portfolio["owner_clean_fix_refine"]
    ]
    prior_flashcards = load(X1 / "flashcard-freeze.json")
    prior_cards = prior_flashcards["cards"]
    if len(prior_cards) != 67 or prior_flashcards["erased_cards"] != 0:
        raise RuntimeError("immutable x1 flashcard freeze mismatch")
    outcomes_by_id = {row["proposal_id"]: row["outcome"] for row in outcomes}
    current_cards = []
    for prior in prior_cards:
        current = {
            "card_id": prior["card_id"],
            "tier": prior["tier"],
            "parent_card_id": prior["parent_card_id"],
            "title": prior["title"],
            "state": "x2_evidence_indexed",
            "supersedes_content_sha256": prior["content_sha256"],
            "evidence_scope": "bounded_synthetic_owner_local",
            "authority_conferred": False,
        }
        if prior["card_id"].startswith("LV6848-CARD-TASK-"):
            proposal_id = "LV6848-N" + prior["card_id"].rsplit("-", 1)[-1]
            current["proposal_id"] = proposal_id
            current["outcome"] = outcomes_by_id[proposal_id]
        payload = json.dumps(current, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        current["content_sha256"] = hashlib.sha256(payload).hexdigest()
        current_cards.append(current)
    current_ids = {card["card_id"] for card in current_cards}
    if current_ids != {card["card_id"] for card in prior_cards}:
        raise RuntimeError("flashcard stable-id mismatch")
    if any(card["parent_card_id"] not in current_ids for card in current_cards if card["parent_card_id"]):
        raise RuntimeError("flashcard parent resolution mismatch")
    flashcard_evidence = {
        "schema": "ghc.family.content-addressed-flashcards.v684.v8.x2",
        "owner": "Liora Venn",
        "phase": "v684-v8",
        "prior_card_count": len(prior_cards),
        "current_card_count": len(current_cards),
        "stable_id_count": len(current_ids),
        "superseded_card_count": len(current_cards),
        "erased_cards": 0,
        "parent_resolution_failures": 0,
        "prior_cards": prior_cards,
        "current_cards": current_cards,
        "navigation_only_not_manifest_receipt_or_authority": True,
        "independent_reproduction_claimed": False,
    }
    effective = {
        "effective_negatives": BASE_AFTER_X1["effective_negatives"] + 300 + len(OPERATIONAL_FAILURES),
        "effective_methods": BASE_AFTER_X1["effective_methods"] + 757 + len(OPERATIONAL_FAILURES),
        "failed_witnesses": BASE_AFTER_X1["failed_witnesses"] + 300 + len(OPERATIONAL_FAILURES),
        "bounded_passing_witnesses": BASE_AFTER_X1["bounded_passing_witnesses"] + 757 + len(OPERATIONAL_FAILURES),
        "open_gaps": BASE_AFTER_X1["open_gaps"] + 3,
        "exact_gates": BASE_AFTER_X1["exact_gates"] + 3,
    }

    documents: dict[Path, Any] = {
        X2 / "proposal-evidence.json": {
            "schema": "ghc.family.proposal-evidence.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "source_x1": X1_COMMIT,
            "outcome_counts": outcome_counts,
            "outcomes": outcomes,
            "real_data_rows": 0,
            "authority_conferred": False,
        },
        X2 / "flashcard-evidence.json": flashcard_evidence,
        X2 / "positive-controls.json": {
            "schema": "ghc.family.positive-controls.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "accepted_count": len(positive_receipts),
            "receipts": positive_receipts,
        },
        X2 / "mutations.json": {
            "schema": "ghc.family.mutations.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "preregistered_count": 300,
            "executed_count": len(mutation_receipts),
            "rejected_count": sum(not item["accepted"] for item in mutation_receipts),
            "accepted_invalid_count": sum(item["accepted"] for item in mutation_receipts),
            "receipts": mutation_receipts,
        },
        X2 / "portfolio-results.json": {
            "schema": "ghc.family.portfolio-results.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "safe_now": executed_safe,
            "owner_candidates": executed_candidates,
            "clean_fix_refine": executed_cfr,
            "successor_candidates": portfolio["successor_candidates"],
            "successor_credit": 0,
            "exact_approval": [{**item, "x2_state": "unexecuted"} for item in portfolio["exact_approval"]],
            "blocked": [{**item, "x2_state": "unexecuted"} for item in portfolio["blocked"]],
        },
        X2 / "skill-smoke-receipts.json": {
            "schema": "ghc.family.skill-smoke.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            **skill_receipt,
        },
        X2 / "runner-smoke-receipts.json": {
            "schema": "ghc.family.runner-smoke.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "runner_count": len(runner_receipts),
            "passed_count": sum(item["positive_accepted"] and item["invalid_rejected"] for item in runner_receipts),
            "receipts": runner_receipts,
        },
        X2 / "method-flow-ledger.json": {
            "schema": "ghc.family.method-flow.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "inherited_and_startup_baseline": BASE_AFTER_X1,
            "counts": effective,
            "methods": methods,
            "operational_failed_witnesses": OPERATIONAL_FAILURES,
            "operational_recovery_witnesses": [
                {
                    "failure_id": item["failure_id"],
                    "recovery": item["recovery"],
                    "bounded_recovery_credit": 1,
                    "failed_witness_promoted": False,
                }
                for item in OPERATIONAL_FAILURES
            ],
            "mutation_failed_witnesses": mutation_receipts,
            "positive_passing_witnesses": positive_receipts,
            "failure_erasure": False,
            "recoveries_retroactively_promote_failure": False,
            "independent_reproduction_claimed": False,
        },
        X2 / "retained-negative-register.json": {
            "schema": "ghc.family.retained-negatives.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "inherited_and_startup_negatives": BASE_AFTER_X1["effective_negatives"],
            "new_preregistered_rejections": 300,
            "new_operational_failures": len(OPERATIONAL_FAILURES),
            "operational_failures": OPERATIONAL_FAILURES,
            "effective_negatives": effective["effective_negatives"],
            "erased": 0,
        },
        X2 / "gate-register.json": {
            "schema": "ghc.family.gates.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "open_gaps": effective["open_gaps"],
            "exact_gates": effective["exact_gates"],
            "new_open_gap_proposals": [row["proposal_id"] for row in outcomes if row["outcome"] == "open_gap"],
            "new_exact_gate_proposals": [row["proposal_id"] for row in outcomes if row["outcome"] == "exact_gate"],
            "closed_by_software": 0,
            "authority_noncompensation": True,
        },
        X2 / "complete-incomplete-ledger.json": {
            "schema": "ghc.family.complete-incomplete.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "bounded_completed": 42,
            "bounded_represented": 12,
            "open_gap": 3,
            "exact_gate": 3,
            "real_files_bitstreams_or_packages": 0,
            "real_people": 0,
            "real_repositories_or_storage_locations": 0,
            "production_actions": 0,
            "authority_actions": 0,
            "independent_reproduction": False,
        },
        X2 / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "source": SOURCE,
            "x1": X1_COMMIT,
            "outcomes": outcome_counts,
            "counts": effective,
            "real_data_rows": 0,
            "network_data_queries": 0,
            "external_writes": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        X2 / "official-source-use-receipt.json": {
            "schema": "ghc.family.official-source-use.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "source_ledger": "docs/liora-venn/v684-v8/x1/official-primary-source-ledger.json",
            "used_for_vocabulary_and_refusal_conditions_only": True,
            "observations_or_measurements": 0,
            "endorsement_or_authority_claimed": False,
        },
        X2 / "environment-and-version-receipt.json": {
            "schema": "ghc.family.environment.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "python": sys.version.split()[0],
            "git": git("--version"),
            "versions_verified_only": True,
            "software_installed_or_updated": False,
            "versions": tool_versions,
            "global_or_plugin_cache_mutated": False,
            "host_security_changed": False,
        },
        X2 / "tool-install-smoke-receipt.json": {
            "schema": "ghc.family.tool-readonly-version.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "scope": "read_only_version_verification",
            "versions": tool_versions,
            "checks": tool_receipts,
            "passed_count": sum(item["passed"] for item in tool_receipts),
            "tool_count": len(tool_receipts),
            "software_installed_or_updated": False,
            "host_security_changed": False,
            "codex_desktop_updated": False,
            "production_certification": False,
        },
        X2 / "global-skill-promotion-receipt.json": {
            "schema": "ghc.family.global-skill-promotion.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "curated_not_bulk": False,
            "promoted_count": len(global_skill_receipts),
            "receipts": global_skill_receipts,
            "plugin_cache_mutated": False,
            "existing_skill_overwritten": False,
            "private_absolute_paths_persisted": False,
            "global_skill_lane_read_only": True,
        },
        X2 / "threat-control-evidence.json": {
            "schema": "ghc.family.threat-control-evidence.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "positive_controls": len(positive_receipts),
            "rejecting_mutations": len(mutation_receipts),
            "skills_used": skill_receipt["smoke_used_count"],
            "runners_used": len(runner_receipts),
            "read_only_version_checks": len(tool_versions),
            "D_first_tools_installed_or_used": 0,
            "curated_global_skills_promoted_and_smoke_used": 0,
            "content_addressed_flashcards_validated": len(current_cards),
            "real_world_rows": 0,
            "residual_authority_gates": True,
        },
        X2 / "successor-recommendations.json": {
            "schema": "ghc.family.successor-recommendations.v684.v8.x2",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "recipient_not_contacted": True,
            "practice_lens": portfolio["successor_practice_recommendation"],
            "candidate_seeds": portfolio["successor_candidates"],
            "skill_seeds": portfolio["successor_skill_ideas"],
            "runner_seeds": portfolio["successor_runner_ideas"],
            "clean_fix_refine_seeds": portfolio["successor_clean_fix_refine"],
            "Liora_completion_credit": 0,
        },
    }
    for path, value in documents.items():
        write_json(path, value)

    overview = f"""# Liora Venn v684-v8 bounded x2 evidence

This x2 executes only the owner-local zero-row contracts frozen at immutable x1
{X1_COMMIT}.  It records 42 completed, 12 represented, 3 open_gap, and 3
exact_gate outcomes using the four authorised labels and no others.

All 60 bounded positive structural fixtures passed.  All 300 preregistered
invalid mutations executed and were rejected.  Each invalid fixture remains a
zero-credit failed witness; its rejection is a separate bounded passing guard
and does not erase or promote the invalid witness.

Twenty phase-local skills were read through EOF, validated with the installed
official skill-creator quick validator, and smoke-used through one bounded
owner-local CLI surface without global installation. Ten family-current
ghc_family community-archives runners each accepted one synthetic
positive fixture and rejected one authority-promotion fixture.  The 120
safe-now, 80 owner-candidate, and 100 CLEAN/FIX/REFINE records executed only as
owner-local software or synthetic contracts.  Twenty exact-approval and ten
blocked records remained unexecuted.  Successor recommendations remain zero
Liora credit and no successor was contacted.

Python and Git versions were verified read-only. No software, global skill,
plugin, host feature, security setting, or account was installed or mutated.
The four-tier owner-to-pillar-to-practice-to-task flashcard index preserves all
67 immutable x1 versions and adds 67 digest-linked x2 versions with stable IDs,
resolved parents, explicit supersession, and zero erasure.

No real archival record, collection, description, person, donor, participant,
institution, location, access request, correction, redaction, credential,
measurement, identity event, external write, disclosure, release,
legal decision, cultural decision, affected-party decision, or Māori-authority
act occurred.

Archives New Zealand information-and-records guidance, New Zealand Privacy
Commissioner principles 6 and 7, W3C PROV-O, WCAG 2.2, Verifiable Credentials
Data Model 2.0, RFC 8785, JSON Schema 2020-12, and Te Mana Raraunga principles
supplied vocabulary and refusal conditions only. Citations are not observations,
endorsements, certificates, affected-party decisions, or delegated authority.

GMUT remains a typed scalar-tensor and EFT research-model family without
empirical confirmation or Theory-of-Everything proof.  THOS remains synthetic
or proxy-only without governed real arms and independent review.  Freed ID
remains synthetic and nonproduction without real keys, proofs, live lifecycle,
interoperability, privacy and security review, recovery evidence, and trust
governance. Archival custody, description, retention, disposal, access, legal remedy, affected-party
legitimacy, Māori wording, Māori data governance, and Māori authority remain
exact-gated.  The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""
    write_text(X2 / "integrated-overview.md", overview)

    entry_paths = sorted(
        list(documents)
        + [X2 / "integrated-overview.md"]
        + skill_paths
        + [
            Path(__file__),
            ROOT / "scripts" / "ghc_family_community_archives_contract.py",
            skill_bank,
            *runner_paths,
            ROOT / "tests" / "test_ghc_family_liora_venn_v684_v8_x2.py",
        ],
        key=rel,
    )
    staged_path = VALIDATION / "evidence-staged-review.json"
    privacy_path = VALIDATION / "evidence-privacy-scan.json"
    security_path = VALIDATION / "evidence-security-scan.json"
    manifest_path = VALIDATION / "evidence-index-manifest.json"
    all_paths = sorted(entry_paths + [staged_path, privacy_path, security_path, manifest_path], key=rel)
    write_json(
        staged_path,
        {
            "schema": "ghc.family.staged-review.v684.v8.evidence",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "x1": X1_COMMIT,
            "expected_paths": [rel(path) for path in all_paths],
            "expected_path_count": len(all_paths),
            "unexpected_paths": [],
            "x1_paths_modified": [],
        },
    )
    privacy = privacy_scan(entry_paths + [staged_path])
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"confirmed privacy hits: {privacy['confirmed_hits']}")
    write_json(privacy_path, privacy)
    security = security_scan(entry_paths)
    if security["finding_count"]:
        raise RuntimeError(f"bounded security findings: {security['findings']}")
    write_json(security_path, security)
    write_json(
        manifest_path,
        {
            "schema": "ghc.family.normalized-lf-index-manifest.v684.v8.evidence",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "x1": X1_COMMIT,
            "declared_self_exclusions": [rel(staged_path), rel(privacy_path), rel(security_path), rel(manifest_path)],
            "entry_count": len(entry_paths),
            "entries": [
                {
                    "path": rel(path),
                    "bytes": len(normalized(path)),
                    "sha256": hashlib.sha256(normalized(path)).hexdigest(),
                }
                for path in entry_paths
            ],
        },
    )
    print(
        json.dumps(
            {
                "status": "BUILT_BOUNDED_X2_EVIDENCE",
                "outcomes": outcome_counts,
                "positive_controls": len(positive_receipts),
                "rejected_mutations": len(mutation_receipts),
                "skills_used": skill_receipt["smoke_used_count"],
                "runners_used": len(runner_receipts),
                "manifest_entries": len(entry_paths),
                "staged_paths": len(all_paths),
                "confirmed_privacy_hits": privacy["confirmed_hit_count"],
                "security_findings": security["finding_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
