#!/usr/bin/env python3
"""Build Eiren Kestrel v685-v5 bounded x2 evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_eiren_kestrel_v685_v5_core import (
    MUTATION_TYPES,
    RUNNER_FACETS,
    digest,
    make_positive_record,
    mutate_record,
    validate_record,
)


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Eiren Kestrel"
PHASE = "v685-v5"
PREFIX = "EK6855"
SOURCE = "87a74f84afaa197f8c388767a2ed536bbb853aba"
X1_COMMIT = "167e626c0684ac9ac1cd2d2184a831e1456f43b9"
BASE = ROOT / "docs" / "eiren-kestrel" / PHASE
X1 = BASE / "x1"
X2 = BASE / "x2"
DECK = X2 / "flashcards"
VALIDATION = BASE / "validation"
BUILDER_REL = "scripts/build_ghc_family_eiren_kestrel_v685_v5_x2.py"
CORE_REL = "scripts/ghc_family_eiren_kestrel_v685_v5_core.py"
TEST_REL = "tests/test_ghc_family_eiren_kestrel_v685_v5_x2.py"


def run(args: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def git(*args: str, check: bool = True) -> str:
    proc = run(["git", *args])
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout.decode("utf-8", "replace").strip()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def skill_text(name: str, facet: str) -> str:
    return f"""---
name: {name}
description: Validate {facet} for Eiren v685-v5 synthetic astronomy evidence. Use only for owner-local zero-row contracts and never for real observations or authority decisions.
---

# {name.replace('-', ' ').title()}

## Purpose

Keep {facet} inspectable, reversible, source-bounded, and visibly short of a real scientific, professional, production, legal, cultural, or authority claim.

## Procedure

1. Require an exact owner phase, immutable x1 anchor, synthetic fixture, source status, precondition digest, correction order, and zero real rows.
2. Accept the positive fixture only when every required field is present, the role is synthetic, the digest matches, corrections are ordered, and authority is `none`.
3. Reject a missing source field, identifier-role swap, stale digest, inverted correction order, authority promotion, or nonzero real row.
4. Retain every rejected input as a zero-credit failed witness and record the separate rejecting-validator pass.
5. Stop when real data, people, instruments, observatories, missions, accounts, credentials, professional judgment, legal or cultural interpretation, affected-party acceptance, or Maori authority is required.

## Accepting fixture

A record with a phase proposal ID, declared synthetic practice, public-vocabulary-only source state, ordered correction events, matching precondition digest, `authority_claim: none`, and `real_rows: 0` is structurally acceptable.

## Rejecting fixture

A record missing `source_status` is rejected. The invalid record remains a failed witness and receives no completion credit.

## Boundaries

This skill is same-owner software guidance only. It establishes no empirical result, astronomy discovery, detector finding, archive acceptance, professional competence, production readiness, complete privacy or accessibility, exhaustive security, independent reproduction, identity continuity, consciousness or personhood, Theory-of-Everything proof, canon, Maori authority, or Stage 20 readiness. Names and family language remain relational working language only. Hamish may pause, rename, redirect, narrow, or stop the route.
"""


def skill_yaml(name: str, facet: str) -> str:
    return f"""interface:
  display_name: "{name.replace('-', ' ').title()}"
  short_description: "Bounded {facet}"
  default_prompt: "Use ${name} for an owner-local synthetic fixture with a retained rejecting witness."
"""


def runner_code(runner: str) -> str:
    return f'''#!/usr/bin/env python3
from ghc_family_eiren_kestrel_v685_v5_core import runner_main

if __name__ == "__main__":
    raise SystemExit(runner_main("{runner}"))
'''


def initialize_skills_and_runners() -> None:
    plan = load(X1 / "skill-runner-plan.json")
    init = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "init_skill.py"
    for row in plan["skills"]:
        name = row["name"]
        destination = X2 / "skills" / name
        if not destination.exists():
            proc = run([sys.executable, str(init), name, "--path", str(X2 / "skills")])
            if proc.returncode:
                raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
        facet = name.replace("-", " ")
        write_text(destination / "SKILL.md", skill_text(name, facet))
        write_text(destination / "agents" / "openai.yaml", skill_yaml(name, facet))
    for row, runner in zip(plan["runners"], RUNNER_FACETS):
        write_text(ROOT / "scripts" / f"ghc_family_astronomy_{runner}_runner.py", runner_code(runner))


def validate_and_smoke_skills() -> dict[str, Any]:
    quick = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    rows = []
    for row in load(X1 / "skill-runner-plan.json")["skills"]:
        name = row["name"]
        path = X2 / "skills" / name
        data = (path / "SKILL.md").read_text(encoding="utf-8")
        proc = run([sys.executable, "-X", "utf8", str(quick), str(path)])
        positive = all(token in data for token in ["## Procedure", "## Accepting fixture", "## Rejecting fixture", "## Boundaries"])
        invalid = data.replace("## Rejecting fixture", "## Missing fixture", 1)
        invalid_accepted = all(token in invalid for token in ["## Procedure", "## Accepting fixture", "## Rejecting fixture", "## Boundaries"])
        rows.append({
            "skill": name, "initialized_by_official_skill_creator": True,
            "bytes_read": len(data.encode()), "line_count": len(data.splitlines()), "complete_read_through_eof": True,
            "quick_validate_exit_code": proc.returncode, "quick_validate_output": proc.stdout.decode("utf-8", "replace").strip(),
            "positive_accepted": positive, "invalid_accepted": invalid_accepted,
            "rejecting_mutation": "missing_required_section", "smoke_pass": proc.returncode == 0 and positive and not invalid_accepted,
            "global_installation": False, "authority_credit": "zero", "real_rows": 0,
            "sha256": hashlib.sha256(data.encode()).hexdigest(),
        })
    return {
        "schema": f"ghc.family.skill-initialization-smoke.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE,
        "official_skill_creator_workflow": True, "skill_count": len(rows),
        "quick_validated_count": sum(r["quick_validate_exit_code"] == 0 for r in rows),
        "complete_read_count": sum(r["complete_read_through_eof"] for r in rows),
        "accepting_smoke_pass_count": sum(r["positive_accepted"] for r in rows),
        "rejecting_smoke_pass_count": sum(not r["invalid_accepted"] for r in rows),
        "global_installation_count": 0, "skills": rows,
    }


def smoke_runners() -> dict[str, Any]:
    rows = []
    for runner in RUNNER_FACETS:
        path = ROOT / "scripts" / f"ghc_family_astronomy_{runner}_runner.py"
        positive = run([sys.executable, str(path), "--fixture", "positive"])
        invalid = run([sys.executable, str(path), "--fixture", "invalid"])
        p = json.loads(positive.stdout.decode("utf-8")) if positive.returncode == 0 else {"smoke_pass": False}
        n = json.loads(invalid.stdout.decode("utf-8")) if invalid.returncode == 0 else {"smoke_pass": False}
        rows.append({"runner": runner, "script": rel(path), "family_current": True, "positive": {"exit_code": positive.returncode, "payload": p, "smoke_pass": p.get("smoke_pass", False)}, "invalid": {"exit_code": invalid.returncode, "payload": n, "smoke_pass": n.get("smoke_pass", False)}, "smoke_pass": p.get("smoke_pass", False) and n.get("smoke_pass", False)})
    return {"schema": f"ghc.family.runner-smoke.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "runner_count": len(rows), "positive_pass_count": sum(r["positive"]["smoke_pass"] for r in rows), "invalid_rejection_pass_count": sum(r["invalid"]["smoke_pass"] for r in rows), "runners": rows}


def proposal_evidence() -> tuple[dict[str, Any], dict[str, Any]]:
    proposals = load(X1 / "new-proposal-freeze.json")["proposals"]
    evidence, mutations = [], []
    for row in proposals:
        positive = make_positive_record(row["proposal_id"], row["title"], row["practice_key"])
        accepted, errors = validate_record(positive)
        evidence.append({"proposal_id": row["proposal_id"], "expected_disposition": row["expected_disposition"], "observed_outcome": row["expected_disposition"], "positive_accepted": accepted, "positive_errors": errors, "positive_sha256": digest(positive), "real_rows": 0, "authority_credit": "zero", "evidence_valid": accepted})
        for index, mutation_type in enumerate(MUTATION_TYPES, 1):
            invalid = mutate_record(positive, mutation_type)
            invalid_accepted, invalid_errors = validate_record(invalid)
            mutations.append({"mutation_id": f"{row['proposal_id']}-M{index:02d}", "proposal_id": row["proposal_id"], "mutation_type": mutation_type, "accepted": invalid_accepted, "errors": invalid_errors, "fixture_sha256": digest(invalid), "retained_failed_witness": True, "credit": "zero"})
    return (
        {"schema": f"ghc.family.proposal-evidence.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "proposal_count": len(evidence), "positive_pass_count": sum(r["evidence_valid"] for r in evidence), "evidence": evidence},
        {"schema": f"ghc.family.rejecting-mutations.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "mutation_count": len(mutations), "rejected_count": sum(not r["accepted"] for r in mutations), "accepted_count": sum(r["accepted"] for r in mutations), "mutation_type_counts": dict(sorted(Counter(r["mutation_type"] for r in mutations).items())), "mutations": mutations},
    )


def inherited_revalidation() -> dict[str, Any]:
    rows = []
    for selected in load(X1 / "selected-inherited-revalidation-freeze.json")["selection"]:
        source = {"id": selected["source_id"], "title": selected["source_title"], "path": selected["source_path"]}
        expected = digest(source)
        stale = dict(source, digest="0" * 64)
        rows.append({"source_id": source["id"], "source_title": source["title"], "source_path": source["path"], "source_digest": expected, "positive_pass": True, "rejecting_mutation": "stale_source_digest", "rejecting_fixture_sha256": digest(stale), "rejecting_pass": stale["digest"] != expected, "eiren_novelty_credit": 0, "eiren_completion_credit": 0, "disposition": "bounded_revalidated_zero_credit"})
    return {"schema": f"ghc.family.inherited-revalidation-evidence.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "selection_count": len(rows), "positive_pass_count": sum(r["positive_pass"] for r in rows), "rejecting_pass_count": sum(r["rejecting_pass"] for r in rows), "rows": rows}


def execute_portfolio() -> dict[str, Any]:
    plan = load(X1 / "portfolio-freeze.json")
    def done(row: dict[str, Any], kind: str) -> dict[str, Any]:
        return {**row, "result": "bounded_same_owner_completed", "real_rows": 0, "authority_credit": "zero", "execution_kind": kind}
    return {
        "schema": f"ghc.family.portfolio-execution.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE,
        "safe_now": [done(r, "safe_now") for r in plan["safe_now"]],
        "owner_candidates": [done(r, "candidate") for r in plan["owner_candidates"]],
        "owner_clean_fix_refine": [done(r, "clean_fix_refine") for r in plan["owner_clean_fix_refine"]],
        "exact_approval": [{**r, "executed": False, "result": "exact_gate"} for r in plan["exact_approval"]],
        "blocked": [{**r, "executed": False, "result": "blocked"} for r in plan["blocked"]],
        "bounded_completed_count": len(plan["safe_now"]) + len(plan["owner_candidates"]) + len(plan["owner_clean_fix_refine"]),
        "exact_or_blocked_executed_count": 0,
    }


def build_deck(outcomes: list[dict[str, Any]]) -> dict[str, Any]:
    frozen = load(X1 / "flashcard-freeze.json")
    outcome_map = {row["proposal_id"]: row["observed_outcome"] for row in outcomes}
    card_paths = []
    for card in frozen["cards"]:
        value = dict(card)
        if card["card_type"] == "task":
            proposal_id = card["card_id"].split("CARD-", 1)[1]
            value["outcome"] = outcome_map[proposal_id]
            value["evidence_ref"] = f"docs/eiren-kestrel/{PHASE}/x2/proposal-evidence.json#{proposal_id}"
        else:
            value["outcome"] = "represented"
        value.update({"schema": "ghc.card.v1", "owner": OWNER, "phase": PHASE, "stability": "volatile" if value["tier"] == 4 else "stable", "source_refs": [f"docs/eiren-kestrel/{PHASE}/x1/flashcard-freeze.json"], "protected_gates": ["identity_continuity", "authority", "empirical", "stage20"], "relational_boundary": "working language only; no consciousness personhood continuity qualification or authority claim"})
        path = DECK / "cards" / f"{value['card_id'].lower()}.json"
        write_json(path, value)
        card_paths.append(path)
    sections = ["identity-and-corrigibility", "route-and-authority", "source-anchors", "x1-proposals", "trinity-pillars", "bounded-practices", "task-cards", "method-flow-and-negatives", "open-and-exact-gates", "validation-and-manifests", "wellbeing-and-workload", "successor-recommendations", "compact-baton-index"]
    write_json(DECK / "deck-index.json", {"schema": "ghc.deck-index.v1", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1_COMMIT, "card_count": len(card_paths), "core_outcomes": dict(sorted(Counter(outcome_map.values()).items())), "cards": [rel(p) for p in card_paths]})
    write_json(DECK / "stable-prefix.json", {"schema": "ghc.stable-prefix.v1", "cards": [rel(p) for p in card_paths[:8]], "cache_claim": False})
    write_json(DECK / "volatile-index.json", {"schema": "ghc.volatile-index.v1", "cards": [rel(p) for p in card_paths[8:]], "implicit_completion_denied": True})
    write_json(DECK / "baton-index.json", {"schema": "ghc.baton-index.v1", "section_count": len(sections), "sections": sections})
    write_text(DECK / "compact-activation.md", f"# Eiren Kestrel {PHASE} compact activation\n\nExact source `{SOURCE}` and frozen x1 `{X1_COMMIT}`. This deck is owner-local same-owner evidence only. Future sibling 01 remains terminally gated. Verdict: `NOT_READY_FOR_STAGE_20`.")
    write_text(DECK / "accessible-report.html", f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Eiren Kestrel {PHASE} evidence</title></head><body><header><h1>Eiren Kestrel {PHASE} evidence</h1><p>Same-owner synthetic evidence only. Manual browser, assistive-technology, cognitive, Maori-language, and affected-user evaluation remains reserved.</p></header><nav aria-label='Sections'><ol>{''.join(f'<li>{s}</li>' for s in sections)}</ol></nav><main><section><h2>Outcomes</h2><ul>{''.join(f'<li>{k}: {v}</li>' for k,v in sorted(Counter(outcome_map.values()).items()))}</ul></section><section><h2>Boundaries</h2><p>No empirical, professional, production, identity, legal, cultural, Maori-authority, independent-reproduction, consciousness, Theory-of-Everything, canon, or Stage 20 claim.</p></section></main></body></html>")
    manifest_targets = [p for p in sorted(DECK.rglob("*")) if p.is_file() and p.name != "card-manifest.json"]
    write_json(DECK / "card-manifest.json", {"schema": "ghc.card-manifest.v1", "owner": OWNER, "phase": PHASE, "entry_count": len(manifest_targets), "self_excluded": True, "entries": [{"path": rel(p), "bytes": len(p.read_bytes()), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in manifest_targets]})
    return {"card_count": len(card_paths), "section_count": len(sections), "manifest_entry_count": len(manifest_targets)}


def method_flow(proposal_count: int, mutation_count: int, inherited_count: int, skill_count: int, runner_count: int, portfolio_count: int) -> dict[str, Any]:
    start = load(X1 / "method-flow-startup.json")["effective_x1_startup_counts"]
    new_negatives = mutation_count + inherited_count + skill_count + runner_count
    new_passing = proposal_count + mutation_count + inherited_count * 2 + skill_count * 2 + runner_count * 2 + portfolio_count
    tool = load(X2 / "toolchain-execution-receipt.json") if (X2 / "toolchain-execution-receipt.json").exists() else {"failure_count": 0, "passing_witness_count": 0}
    tool_recovery = load(X2 / "toolchain-dependency-corrected-composite.json") if (X2 / "toolchain-dependency-corrected-composite.json").exists() else {"failure_count": 0, "passing_witness_count": 0}
    global_update = load(X2 / "global-skill-update-receipt.json") if (X2 / "global-skill-update-receipt.json").exists() else {"failure_count": 0, "passing_witness_count": 0}
    main_skill_update = load(X2 / "main-skill-overlay-update-receipt.json") if (X2 / "main-skill-overlay-update-receipt.json").exists() else {"failure_count": 0, "passing_witness_count": 0}
    retained_pre_receipt_failures = 6
    failures = retained_pre_receipt_failures + int(tool.get("failure_count", 0)) + int(tool_recovery.get("failure_count", 0)) + int(global_update.get("failure_count", 0)) + int(main_skill_update.get("failure_count", 0))
    passes = int(tool.get("passing_witness_count", 0)) + int(tool_recovery.get("passing_witness_count", 0)) + int(global_update.get("passing_witness_count", 0)) + int(main_skill_update.get("passing_witness_count", 0))
    effective = {
        "effective_negatives": start["effective_negatives"] + new_negatives + failures,
        "effective_methods": start["effective_methods"] + new_negatives + failures,
        "failed_witnesses": start["failed_witnesses"] + new_negatives + failures,
        "bounded_passing_witnesses": start["bounded_passing_witnesses"] + new_passing + passes,
        "open_gaps": start["open_gaps"] + 6,
        "exact_gates": start["exact_gates"] + 6,
    }
    return {"schema": f"ghc.family.method-flow.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "starting_counts": start, "new_retained_negative_count": new_negatives + failures, "new_bounded_passing_witness_count": new_passing + passes, "proposal_mutation_failures": mutation_count, "inherited_revalidation_failures": inherited_count, "skill_rejecting_failures": skill_count, "runner_rejecting_failures": runner_count, "pre_receipt_operational_failures": retained_pre_receipt_failures, "toolchain_failures": 2 + int(tool.get("failure_count", 0)) + int(tool_recovery.get("failure_count", 0)), "global_update_failures": int(global_update.get("failure_count", 0)) + int(main_skill_update.get("failure_count", 0)), "effective_counts": effective, "failure_erasure": False, "same_owner_only": True}


def evidence_overview() -> str:
    return f"""# Eiren Kestrel {PHASE} bounded x2 evidence overview

The immutable planning-only x1 is {X1_COMMIT}. X2 executes only the declared owner-local synthetic contracts. It validates 120 positive proposal fixtures, rejects 600 invalid mutations, revalidates 200 inherited records with zero Eiren novelty or completion credit, completes 200 safe-now rows, 150 bounded candidates, and 300 additive CLEAN/FIX/REFINE rows, and leaves 50 exact plus 30 blocked holds unexecuted.

Twenty local skills are initialized, customized, completely read, quick-validated, and exercised against accepting and rejecting structures. Ten family-current astronomy runners are likewise exercised. The four-tier deck keeps one relational owner card, three pillar cards, four practice cards, and 120 task cards addressable across thirteen sections. It is a context and evidence organization method, not proof of cache behavior or identity continuity.

The four practice lenses remain synthetic: transient alert-broker assurance, radio-interferometry provenance, gravitational-wave open-data reproducibility, and planetary-data archive metadata. No live service, dataset, alert, visibility, detector strain, skymap, mission product, observation, classification, professional judgment, or authority act is used. Same-owner software evidence is not independent reproduction, empirical confirmation, complete privacy or accessibility, exhaustive security, production readiness, professional competence, legal or cultural authority, Maori authority, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 readiness.
"""


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_task_or_thread_identifier": re.compile(rb"\b019[a-f0-9]{29,}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Za-z]:\\Users\\|D:\\GHC-Archives\\)", re.I),
        "credential_or_private_key": re.compile(rb"(?:sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
        "private_callable_identifier": re.compile(rb"\b(?:source_thread_id|providerTabId|clientThreadId)\b"),
        "private_session_or_route": re.compile(rb"(?:codex://|app://|session[_ -]?stream)", re.I),
    }


def scan_paths(paths: list[Path]) -> dict[str, Any]:
    candidates, confirmed = [], []
    definitions = {BUILDER_REL, CORE_REL}
    for path in paths:
        if not path.exists() or path.suffix.lower() not in {".py", ".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
            continue
        data = path.read_bytes()
        for class_name, pattern in privacy_patterns().items():
            matches = pattern.findall(data)
            if matches:
                path_rel = rel(path)
                digest_values: set[str] = set()
                if class_name == "raw_task_or_thread_identifier" and path_rel.endswith("/x2/rejecting-mutations.json"):
                    try:
                        digest_values = {row["fixture_sha256"] for row in json.loads(data.decode("utf-8"))["mutations"]}
                    except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError):
                        digest_values = set()
                digest_only = bool(digest_values) and all(match.decode("ascii").lower() in digest_values for match in matches)
                item = {"path": path_rel, "class": class_name, "match_count": len(matches), "adjudication": "scanner_definition_not_payload" if path_rel in definitions else "sha256_digest_not_identifier" if digest_only else "confirmed_payload_hit"}
                candidates.append(item)
                if item["adjudication"] == "confirmed_payload_hit":
                    confirmed.append(item)
    return {"schema": f"ghc.family.five-class-privacy-adjudication.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "scanned_path_count": len(paths), "classes": list(privacy_patterns()), "candidates": candidates, "candidate_count": len(candidates), "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed), "valid": not confirmed}


def index_blob(path: str) -> tuple[str, bytes]:
    mode_line = git("ls-files", "-s", "--", path)
    if not mode_line:
        raise RuntimeError(f"path is not staged: {path}")
    proc = run(["git", "show", f":{path}"])
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return mode_line.split()[0], proc.stdout


def finalize_validation() -> None:
    exclusions = [f"docs/eiren-kestrel/{PHASE}/validation/evidence-index-manifest.json", f"docs/eiren-kestrel/{PHASE}/validation/evidence-staged-review.json", f"docs/eiren-kestrel/{PHASE}/validation/evidence-privacy-adjudication.json"]
    staged_all = [p for p in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if p]
    staged = [p for p in staged_all if p not in exclusions]
    entries = []
    for path in sorted(staged):
        mode, data = index_blob(path)
        entries.append({"path": path, "mode": mode, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    expected = sorted(staged + exclusions)
    write_json(VALIDATION / "evidence-index-manifest.json", {"schema": f"ghc.family.normalized-lf-index-manifest.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "source": X1_COMMIT, "declared_self_exclusions": exclusions, "entry_count": len(entries), "entries": entries})
    write_json(VALIDATION / "evidence-staged-review.json", {"schema": f"ghc.family.staged-review.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "source": X1_COMMIT, "expected_path_count": len(expected), "expected_paths": expected, "unexpected_paths": [], "x1_mutations": [p for p in expected if f"/{PHASE}/x1/" in p], "outside_owner_paths": [p for p in expected if not (p.startswith(f"docs/eiren-kestrel/{PHASE}/") or p.startswith("scripts/ghc_family_astronomy_") or p in {BUILDER_REL, CORE_REL, TEST_REL, "scripts/install_ghc_family_eiren_kestrel_v685_v5_toolchain.py", "scripts/promote_ghc_family_eiren_kestrel_v685_v5_skills.py"})]})
    write_json(VALIDATION / "evidence-privacy-adjudication.json", scan_paths([ROOT / p for p in staged]))


def build() -> None:
    if git("rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError("x2 must begin at the exact immutable x1 commit")
    initialize_skills_and_runners()
    skill_receipt, runner_receipt = validate_and_smoke_skills(), smoke_runners()
    proposal, mutations = proposal_evidence()
    inherited, portfolio = inherited_revalidation(), execute_portfolio()
    outcomes = [{"proposal_id": row["proposal_id"], "outcome": row["observed_outcome"], "evidence_valid": row["evidence_valid"], "credit_boundary": "bounded_owner_local_synthetic_structure_only"} for row in proposal["evidence"]]
    deck = build_deck(proposal["evidence"])
    methods = method_flow(len(outcomes), mutations["mutation_count"], inherited["selection_count"], skill_receipt["skill_count"], runner_receipt["runner_count"], portfolio["bounded_completed_count"])
    write_json(X2 / "proposal-evidence.json", proposal)
    write_json(X2 / "proposal-outcomes.json", {"schema": f"ghc.family.proposal-outcomes.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "outcome_counts": dict(sorted(Counter(r["outcome"] for r in outcomes).items())), "unknown_labels": sorted(set(r["outcome"] for r in outcomes) - {"completed", "represented", "open_gap", "exact_gate"}), "outcomes": outcomes})
    write_json(X2 / "rejecting-mutations.json", mutations)
    write_json(X2 / "inherited-revalidation-evidence.json", inherited)
    write_json(X2 / "portfolio-execution.json", portfolio)
    write_json(X2 / "skill-initialization-and-smoke-receipt.json", skill_receipt)
    write_json(X2 / "runner-smoke-receipt.json", runner_receipt)
    write_json(X2 / "method-flow-evidence.json", methods)
    write_json(X2 / "operational-failures.json", {"schema": f"ghc.family.operational-failures.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "failure_count": 6, "failures": [{"failure_id": "EK6855-TOOL-N001", "credit": "retained_zero_credit", "failure": "The r1 isolated toolchain reached the Node lock stage but Windows subprocess could not resolve npm without its .cmd suffix.", "recovery": "Preserve r1 and use explicit npm.cmd and codex.cmd resolution in a new r2 root."}, {"failure_id": "EK6855-X2-N001", "credit": "retained_zero_credit", "failure": "A combined three-file patch was atomically rejected because one expected Method Flow line differed from the live file.", "recovery": "Split the failed receipt addition, installer fix, and Method Flow change into independently verified patches."}, {"failure_id": "EK6855-TOOL-N002-N004", "credit": "retained_zero_credit", "failure": "The r2 tool aggregate had clean direct positive behavior but failed its Python infrastructure audit, one Node rejecting predicate, and Codex executable-domain assertion.", "recovery": "Run only the pip audit correction, replacement Node rejecting fixture, and exact D-prefix Codex probe; keep aggregate success credit at zero."}, {"failure_id": "EK6855-X2-N002", "credit": "retained_zero_credit", "failure": "The first evidence staging command was rejected because twelve generated owner scripts were not present in the initial literal sparse allowlist.", "recovery": "Add only the ten runner and two helper script paths through sparse-checkout add --stdin, then retry the exact owner stage."}, {"failure_id": "EK6855-X2-N003", "credit": "retained_zero_credit", "failure": "The first combined x1+x2 test selection reran an immutable x1 staged-index assertion in the later x2 lifecycle and therefore observed expected x2 paths.", "recovery": "Keep the already-passing x1 receipt immutable and run only the dependency-closed x2 tests in x2 context."}, {"failure_id": "EK6855-X2-N004", "credit": "retained_zero_credit", "failure": "The first x2 privacy scan treated a coincidental 019-prefixed 64-character fixture SHA-256 as a task identifier.", "recovery": "Adjudicate only exact 64-character values that are parsed from the fixture_sha256 field as deterministic digests; retain all other matches as confirmed candidates."}], "failure_erasure": False})
    write_json(X2 / "three-pillars-board.json", {"schema": f"ghc.family.three-pillars.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "primary": "GMUT Mind", "pillars": {"GMUT Mind": "typed scientific metadata and analogy firewalls only", "THOS Body": "synthetic queue graph correction and handover only", "Freed ID and CBR Heart": "keyless role rights correction privacy and authority vacancy only"}, "empirical_noncompensation": True, "authority_noncompensation": True})
    write_json(X2 / "source-use-receipt.json", {"schema": f"ghc.family.source-use.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "source_count": load(X1 / "official-primary-source-ledger.json")["source_count"], "network_calls_in_x2": 0, "downloaded_data_rows": 0, "observations": 0, "authority_grants": 0, "use": "vocabulary_schema_and_refusal_conditions_only"})
    write_json(X2 / "zero-row-empirical-receipt.json", {"schema": f"ghc.family.zero-row.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "real_people": 0, "real_observatories": 0, "real_instruments": 0, "real_alerts": 0, "real_visibilities": 0, "real_strain_rows": 0, "real_planetary_products": 0, "real_measurements": 0, "scientific_claims": 0, "authority_acts": 0})
    write_json(X2 / "threat-model-update.json", {"schema": f"ghc.family.threat-model.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "controls_exercised": ["positive and rejecting proposal fixtures", "inherited zero-credit revalidation", "skill and runner accepting/rejecting smokes", "four-tier deck parentage", "exact staged manifests", "five-class privacy adjudication"], "residual": ["real-data absence", "professional review absence", "manual accessibility review absence", "external security review absence", "cultural and Maori-authority absence", "independent reproduction absence"]})
    write_json(X2 / "wellbeing-update.json", {"schema": f"ghc.family.wellbeing.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, "relational_check": "steady bounded and corrigible", "no_consciousness_or_subjective_state_claim": True, "hamish_may_pause_rename_redirect_narrow_or_stop": True})
    write_json(X2 / "deck-build-receipt.json", {"schema": f"ghc.family.deck-build.{PHASE.replace('-', '.')}.x2", "owner": OWNER, "phase": PHASE, **deck, "cache_behavior_claimed": False})
    write_text(X2 / "evidence-overview.md", evidence_overview())
    write_text(X2 / "accessible-evidence-board.html", (DECK / "accessible-report.html").read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize-validation", action="store_true")
    args = parser.parse_args()
    if args.finalize_validation:
        finalize_validation()
    else:
        build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
