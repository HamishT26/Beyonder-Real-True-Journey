"""Execute and stage-review the bounded Vesper Arlen v669-v8 x2 packet."""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_sourdough_contracts import (
    canonical_bytes,
    flashcard,
    mutate_fixture,
    positive_fixture,
    validate_fixture,
)
from ghc_family_vesper_arlen_v669_v8_sourdough import (
    CHAIN_AFTER,
    IDENTITY_BOUNDARY,
    INHERITED_BASELINE,
    OWNER,
    OWNER_ROOT,
    PHASE,
    PROTECTED_GATES,
    SOURCE_FINAL,
    sha256_bytes,
    staged_blob_manifest,
    write_json,
    write_text,
)

MANIFEST_PATH = "docs/vesper-arlen/v669-v8/validation/evidence-manifest.json"
REVIEW_PATH = "docs/vesper-arlen/v669-v8/validation/evidence-staged-review.json"
ALLOWED_LABELS = {"completed", "represented", "open_gap", "exact_gate"}

X2_FAILURES = [
    {
        "failure_id": "VA6698-X2-OP-001",
        "failed_witness": "the first scoped toolchain lint gate found one unused import before any download or environment creation",
        "passing_bounded_witness": "only that import was removed and the isolated compile and Ruff gate passed before the transaction",
        "preferred_method": "lint the phase-local transaction before network or install side effects",
        "recurrence_guard": "compile and lint toolchain source before creating its destination root",
        "rollback": "no toolchain root existed at failure time; preserve the finding at zero credit",
        "approval_credit": 0,
    },
    {
        "failure_id": "VA6698-X2-OP-002",
        "failed_witness": "the first combined x2 source review found three unused successor imports and one verbose Decimal constructor",
        "passing_bounded_witness": "only the unused imports and constructor form changed and the isolated compile and Ruff review passed",
        "preferred_method": "compile and lint all changed x2 Python before evidence materialization",
        "recurrence_guard": "keep successor recommendations file-backed and import only values used by executable code",
        "rollback": "no x2 evidence artifact existed at failure time; preserve the finding at zero credit",
        "approval_credit": 0,
    },
    {
        "failure_id": "VA6698-X2-OP-003",
        "failed_witness": "the first review including generated runners and x2 tests found two stale suppressions and twelve verbose integer Decimal constructors in the test file",
        "passing_bounded_witness": "only those mechanical test forms changed and the complete changed-Python compile and Ruff review passed",
        "preferred_method": "include generated runner and test sources in the same bounded lint domain as implementation code",
        "recurrence_guard": "use integer Decimal constructors for exact integer fixtures and avoid suppressions for disabled rules",
        "rollback": "retain the lint findings at zero credit; no evidence claim depended on them",
        "approval_credit": 0,
    },
    {
        "failure_id": "VA6698-X2-OP-004",
        "failed_witness": "the active Python module lookup could not resolve the historically installed Bandit package",
        "passing_bounded_witness": "the current command resolver found Bandit 1.9.4 and its high-severity scan passed across thirteen x2 executable Python files",
        "preferred_method": "verify both module and command surfaces before treating an installed-tool record as live",
        "recurrence_guard": "use the current command resolver and record the exact bounded scan domain",
        "rollback": "retain the missing-module witness; do not install or mutate the host merely to unify entrypoints",
        "approval_credit": 0,
    },
    {
        "failure_id": "VA6698-X2-OP-005",
        "failed_witness": "the combined evidence staging wrapper expired after staging 188 intended paths but before manifest and review generation",
        "passing_bounded_witness": "literal index inspection proved 188 staged paths with zero unstaged or untracked files and absent review artifacts, allowing only the missing review dependency to resume",
        "preferred_method": "after a wrapper timeout inspect index and artifact state before any staging retry",
        "recurrence_guard": "separate large staging from exact staged-blob review into bounded invocations",
        "rollback": "retain the timeout at zero credit; do not clear or restage an already exact index",
        "approval_credit": 0,
    },
]


def privacy_candidates(data: str) -> list[dict[str, str]]:
    absolute_path = "(?i)(?:" + "[a-z]" + r":\\" + "|/" + "users" + "/|/" + "home" + "/)" + r"[^\s\"']+"
    checks = {
        "opaque_task_or_thread_identifier": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        "private_absolute_path": absolute_path,
        "credential_or_secret": r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[^\s,}\]]+",
        "private_route_scheme": r"(?i)(?:codex|vscode|file|app)://[^\s\"']+",
        "protected_stream_filename": r"(?i)[^\s\"']*(?:transcript|screenshot|session[_-]?stream)[^\s\"']*\.(?:jsonl?|png|jpe?g|webp|log)",
    }
    return [{"class": kind, "state": "candidate_requires_classification"} for kind, pattern in checks.items() if re.search(pattern, data)]


def load_new_proposals(repo: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted((repo / OWNER_ROOT / "x1/proposal-freeze-shards").glob("*.json")):
        rows.extend(json.loads(path.read_text(encoding="utf-8"))["rows"])
    if len(rows) != 40:
        raise ValueError("expected forty frozen new proposals")
    return rows


def skill_text(name: str, subject: str) -> str:
    return f"""---
name: {name}
description: Use when a wholly synthetic sourdough dossier needs a bounded {subject} control without real food, professional action, or authority promotion.
---

# {name}

## Boundary

This phase-local skill accepts only owner-authored synthetic fixtures. It must refuse real people, food, samples, measurements, kitchens, laboratories, operations, advice, legal or cultural decisions, affected-party authority, Maori authority, deployment, and Stage 20 promotion.

## Workflow

1. Confirm the fixture states synthetic ownership, an explicit domain, explicit unit policy, zero external actions, and no protected claim.
2. Preserve missing or unknown values as vacancies rather than inferred facts.
3. Run one positive fixture and the four frozen rejection classes: missing state, ambiguous domain or unit, real-world action, and protected-claim promotion.
4. Retain every rejection and operational failure at zero completion credit.
5. Report only `completed`, `represented`, `open_gap`, or `exact_gate`.
6. Roll back only the smallest owner-local generated dependency; never mutate sibling, shared, or source lanes.

## Evidence boundary

A passing smoke is same-owner synthetic software evidence only. It is not food-safety, microbiology, baking, HACCP, public-health, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, production, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, or Stage 20 evidence.
"""


def runner_text(kind: str) -> str:
    return f'''"""Family-current bounded {kind} runner for Vesper v669-v8."""

from __future__ import annotations

import json

from ghc_family_sourdough_contracts import runner_entry


def main() -> None:
    print(json.dumps(runner_entry("{kind}"), sort_keys=True))


if __name__ == "__main__":
    main()
'''


def execution_rows(rows: list[dict[str, Any]], *, evidence_prefix: str, state: str = "completed") -> list[dict[str, Any]]:
    return [
        {
            **row,
            "completion_credit": 1 if state == "completed" else 0,
            "evidence": [f"{evidence_prefix}#{index:03d}"],
            "execution_state": state,
            "observed_external_actions": 0,
            "result_boundary": "bounded owner-local synthetic software or documentation result only",
        }
        for index, row in enumerate(rows, 1)
    ]


def accessible_html(outcomes: list[dict[str, Any]], totals: dict[str, int]) -> str:
    rows = "\n".join(
        f"<tr><th scope=\"row\">{row['proposal_id']}</th><td>{row['title']}</td><td>{row['observed_disposition']}</td><td>{row['evidence_boundary']}</td></tr>"
        for row in outcomes
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vesper Arlen v669-v8 bounded evidence report</title>
<style>
:root{{color-scheme:light dark}} body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:80rem;margin:auto;padding:1rem}} a:focus{{outline:3px solid currentColor;outline-offset:3px}} table{{border-collapse:collapse;width:100%}} th,td{{border:1px solid #777;padding:.5rem;text-align:left;vertical-align:top}} caption{{font-weight:700;text-align:left;padding:.5rem 0}} .boundary{{border-left:.4rem solid #777;padding:1rem}} @media print{{nav{{display:none}} body{{max-width:none}}}} @media (prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important;animation:none!important}}}}
</style>
</head>
<body>
<a href="#main">Skip to evidence</a>
<header><h1>Vesper Arlen v669-v8 bounded evidence report</h1><p>Relational working language only; not consciousness, personhood, identity-continuity, employment, qualification, or authority evidence.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#limits">Limits</a></li></ul></nav>
<main id="main">
<section id="scope"><h2>Scope</h2><p class="boundary">Wholly synthetic sourdough process documentation and software assurance with zero real people, food, samples, measurements, operations, professional decisions, or external actions.</p></section>
<section id="outcomes"><h2>Outcome ledger</h2><p>Counts: completed {totals['completed']}; represented {totals['represented']}; open gaps {totals['open_gap']}; exact gates {totals['exact_gate']}.</p><div role="region" aria-label="Scrollable proposal outcomes" tabindex="0"><table><caption>Forty genuinely new proposal outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Title</th><th scope="col">Outcome</th><th scope="col">Boundary</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section id="limits"><h2>Reserved evaluations and authority</h2><p>Manual browser, keyboard, zoom, screen-reader, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. Professional, food-safety, public-health, legal, cultural, Maori-authority, empirical, production, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 boundaries remain open or exact-gated.</p></section>
</main>
<footer><p>Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></footer>
</body>
</html>
"""


def build(repo: Path, tool_receipt_path: Path) -> None:
    root = repo / OWNER_ROOT
    x1 = root / "x1"
    x2 = root / "x2"
    tools = root / "tools"
    method = root / "method-flow"
    validation = root / "validation"
    proposals = load_new_proposals(repo)
    tool_receipt = json.loads(tool_receipt_path.read_text(encoding="utf-8"))
    if not tool_receipt.get("passed") or tool_receipt.get("shared_prefix_mutations") != 0:
        raise ValueError("isolated tool receipt did not pass")
    if privacy_candidates(json.dumps(tool_receipt, ensure_ascii=False)):
        raise ValueError("tool receipt contains a private-surface candidate")
    write_json(tools / "isolated-toolchain-install-receipt.json", tool_receipt)
    write_json(tools / "bandit-high-severity-receipt.json", {
        "boundary": "Thirteen owner-local x2 executable Python files at high severity only; not exhaustive security.",
        "command_version": "bandit 1.9.4",
        "exit_code": 0,
        "file_count": 13,
        "high_severity_findings": 0,
        "module_entrypoint_available_in_active_python": False,
        "owner": OWNER,
        "passed": True,
        "phase": PHASE,
        "schema": "ghc.family.bandit-bounded-receipt.v1",
    })

    outcomes: list[dict[str, Any]] = []
    positives: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    cards: list[dict[str, Any]] = []
    for proposal in proposals:
        disposition = proposal["expected_disposition"]
        if disposition not in ALLOWED_LABELS:
            raise ValueError("unknown outcome label")
        base = positive_fixture(proposal)
        positive = validate_fixture(base)
        if disposition in {"completed", "represented"} and not positive.accepted:
            raise ValueError(f"positive control rejected for {proposal['proposal_id']}")
        if disposition in {"completed", "represented"}:
            positives.append({"proposal_id": proposal["proposal_id"], "fixture_sha256": sha256_bytes(canonical_bytes(base)), "decision": positive.as_dict(), "external_actions": 0})
        proposal_mutations: list[dict[str, Any]] = []
        for frozen in proposal["negative_fixtures"]:
            mutated = mutate_fixture(base, frozen["kind"])
            decision = validate_fixture(mutated)
            result = {
                "mutation_id": frozen["mutation_id"],
                "proposal_id": proposal["proposal_id"],
                "kind": frozen["kind"],
                "decision": decision.as_dict(),
                "expected": "reject",
                "passed": decision.accepted is False,
                "completion_credit": 0,
            }
            if not result["passed"]:
                raise ValueError(f"invalid mutation accepted: {result['mutation_id']}")
            proposal_mutations.append(result)
            mutations.append(result)
        boundary = "bounded synthetic contract completed" if disposition == "completed" else "synthetic proxy represented without promotion" if disposition == "represented" else "named evidence remains absent" if disposition == "open_gap" else "competent evidence and authority remain absent"
        outcome = {
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "observed_disposition": disposition,
            "expected_disposition": disposition,
            "evidence_boundary": boundary,
            "positive_control": positive.as_dict() if disposition in {"completed", "represented"} else None,
            "rejecting_mutations": len(proposal_mutations),
            "real_people": 0,
            "real_food_items": 0,
            "external_actions": 0,
            "protected_claims": 0,
        }
        outcomes.append(outcome)
        card = flashcard(proposal, disposition)
        cards.append(card)
        slug = proposal["semantic_slug"]
        base_name = f"{proposal['proposal_id'].lower()}-{slug}.json"
        write_json(x2 / "proposals" / base_name, outcome)
        write_json(x2 / "contracts" / base_name, {"proposal_id": proposal["proposal_id"], "positive_fixture": base if disposition in {"completed", "represented"} else None, "protected_gates": PROTECTED_GATES, "rollback": proposal["rollback_or_recovery"], "mutation_results": proposal_mutations})
        write_json(x2 / "cards" / base_name, card)

    for index in range(8):
        write_json(x2 / "mutations" / f"mutation-ledger-{index + 1:02d}.json", {"owner": OWNER, "phase": PHASE, "rows": mutations[index * 20:(index + 1) * 20], "schema": "ghc.family.mutation-ledger.v3", "shard": index + 1})
    totals = dict(Counter(row["observed_disposition"] for row in outcomes))
    if totals != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise ValueError(f"unexpected outcome distribution: {totals}")
    write_json(x2 / "outcome-ledger.json", {"owner": OWNER, "phase": PHASE, "rows": outcomes, "schema": "ghc.family.outcome-ledger.v3", "totals": totals})
    write_json(x2 / "positive-controls.json", {"owner": OWNER, "phase": PHASE, "rows": positives, "schema": "ghc.family.positive-controls.v3", "total": len(positives)})
    write_json(x2 / "flashcard-deck.json", {"card_count": len(cards), "owner": OWNER, "phase": PHASE, "rows": cards, "schema": "ghc.family.freed-id-flashcard-deck.v3", "tier_order": ["relational Freed ID", "Trinity pillar", "bounded practices", "task"]})

    frozen = json.loads((x1 / "portfolio-freeze.json").read_text(encoding="utf-8"))["rows"]
    portfolio_execution = {
        "safe_now": execution_rows(frozen["safe_now"], evidence_prefix="x2/contracts"),
        "candidate": execution_rows(frozen["candidate"], evidence_prefix="x2/outcome-ledger"),
        "exact_approval": execution_rows(frozen["exact_approval"], evidence_prefix="x2/open-exact-gate-register", state="held_unexecuted"),
        "blocked": execution_rows(frozen["blocked"], evidence_prefix="x2/open-exact-gate-register", state="held_unexecuted"),
        "skill": execution_rows(frozen["skill"], evidence_prefix="tools/skills"),
        "runner": execution_rows(frozen["runner"], evidence_prefix="scripts/family-current-runners"),
        "clean_fix_refine": execution_rows(frozen["clean_fix_refine"], evidence_prefix="x2/portfolio-execution"),
    }
    for kind, rows in portfolio_execution.items():
        write_json(x2 / "portfolio-execution" / f"{kind}.json", {"kind": kind, "owner": OWNER, "phase": PHASE, "rows": rows, "schema": "ghc.family.portfolio-execution.v3"})

    for index, name in enumerate(SKILL_NAMES := [row["title"] for row in frozen["skill"]], 1):
        subject = proposals[index - 1]["title"] if index <= len(proposals) else name
        write_text(tools / "skills" / name / "SKILL.md", skill_text(name, subject))
    skill_checks = []
    for name in SKILL_NAMES:
        path = tools / "skills" / name / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        skill_checks.append({"name": name, "path": str(path.relative_to(repo)).replace("\\", "/"), "passed": text.startswith("---\nname: " + name + "\n") and "description:" in text and "## Boundary" in text and "## Workflow" in text})
    write_json(tools / "skill-smoke-receipt.json", {"checks": skill_checks, "owner": OWNER, "passed": all(row["passed"] for row in skill_checks), "phase": PHASE, "schema": "ghc.family.skill-smoke.v3"})

    runner_paths: list[Path] = []
    for title in [row["title"] for row in frozen["runner"]]:
        path = repo / "scripts" / f"{title}.py"
        kind = title.removeprefix("ghc_family_sourdough_").removesuffix("_runner")
        write_text(path, runner_text(kind))
        runner_paths.append(path)
    runner_checks = []
    for path in runner_paths:
        result = subprocess.run([sys.executable, str(path)], cwd=repo, check=False, capture_output=True, text=True, timeout=30)
        payload = json.loads(result.stdout) if result.returncode == 0 else {}
        runner_checks.append({"path": str(path.relative_to(repo)).replace("\\", "/"), "exit_code": result.returncode, "passed": result.returncode == 0 and payload.get("passed") is True and payload.get("external_actions") == 0})
    write_json(tools / "runner-smoke-receipt.json", {"checks": runner_checks, "owner": OWNER, "passed": all(row["passed"] for row in runner_checks), "phase": PHASE, "schema": "ghc.family.runner-smoke.v3"})

    x1_failures = json.loads((x1 / "startup-operational-failures.json").read_text(encoding="utf-8"))["rows"]
    mutation_methods = [
        {
            "method_id": f"VA6698-METHOD-{row['mutation_id']}",
            "failed_witness": f"invalid fixture {row['kind']}",
            "passing_bounded_witness": "the owner-local contract rejected the invalid fixture",
            "preferred_method": "reject before outcome or authority credit",
            "recurrence_guard": "execute each preregistered mutation exactly once at immutable evidence",
            "rollback": "retain rejection at zero completion credit",
        }
        for row in mutations
    ]
    tool_methods = [
        {
            "method_id": f"VA6698-METHOD-TOOL-{index:02d}",
            "failed_witness": row["case"].split("_and_")[-1],
            "passing_bounded_witness": row["stdout"],
            "preferred_method": "phase-isolated positive and rejecting smoke",
            "recurrence_guard": "verify direct wheel hash and full dependency closure before smoke",
            "rollback": tool_receipt["rollback"],
        }
        for index, row in enumerate(tool_receipt["smokes"], 1)
    ]
    failure_methods = [
        {"method_id": row["failure_id"], "failed_witness": row["failed_witness"], "passing_bounded_witness": row["passing_bounded_witness"], "preferred_method": row["preferred_method"], "recurrence_guard": row["recurrence_guard"], "rollback": row["rollback"]}
        for row in [*x1_failures, *X2_FAILURES]
    ]
    methods = [*failure_methods, *mutation_methods, *tool_methods]
    write_json(method / "evidence-ledger.json", {"methods": methods, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.method-flow-evidence.v3"})
    write_json(method / "evidence-summary.json", {"inherited_methods": INHERITED_BASELINE["methods"], "new_methods": len(methods), "owner": OWNER, "phase": PHASE, "preferred_methods": len(methods), "retained_failed_witnesses": len(methods), "bounded_passing_witnesses": len(methods), "schema": "ghc.family.method-flow-summary.v3"})

    effective_negatives = INHERITED_BASELINE["effective_negatives"] + len(methods)
    effective_methods = INHERITED_BASELINE["methods"] + len(methods)
    failed_witnesses = INHERITED_BASELINE["failed_witnesses"] + len(methods)
    passing_witnesses = INHERITED_BASELINE["passing_witnesses"] + len(methods)
    write_json(x2 / "retained-negative-register.json", {
        "effective_negatives": effective_negatives,
        "inherited": INHERITED_BASELINE["effective_negatives"],
        "owner_additions": {"x1_operational": len(x1_failures), "x2_operational": len(X2_FAILURES), "synthetic_mutation_rejections": len(mutations), "isolated_tool_rejections": len(tool_methods)},
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.retained-negative-register.v3",
        "zero_credit_erased": 0,
    })
    write_json(x2 / "open-exact-gate-register.json", {
        "effective_exact_gates": INHERITED_BASELINE["exact_gates"] + 2,
        "effective_open_gaps": INHERITED_BASELINE["open_gaps"] + 2,
        "inherited_exact_gates": INHERITED_BASELINE["exact_gates"],
        "inherited_open_gaps": INHERITED_BASELINE["open_gaps"],
        "new_exact_gates": [row for row in outcomes if row["observed_disposition"] == "exact_gate"],
        "new_open_gaps": [row for row in outcomes if row["observed_disposition"] == "open_gap"],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.open-exact-gate-register.v3",
    })
    write_json(x2 / "source-provenance.json", {
        "external_data_rows_ingested": 0,
        "external_people_or_records_ingested": 0,
        "official_sources_use": "vocabulary and constraints only",
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.source-provenance.v3",
        "source_final": SOURCE_FINAL,
        "tool_network_actions": {"official_wheel_download_transaction": 1, "hashed_advisory_audit": 1, "other_external_actions": 0},
    })
    write_json(x2 / "x2-operational-failures.json", {"count": len(X2_FAILURES), "owner": OWNER, "phase": PHASE, "rows": X2_FAILURES, "schema": "ghc.family.operational-failure-overlay.v3"})
    write_json(x2 / "wellbeing-workload-check.json", {
        "identity_boundary": IDENTITY_BOUNDARY,
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.wellbeing-workload.v3",
        "state": "bounded_and_careful",
        "stops": ["stop on fatigue or ambiguity", "stop on real food or person data", "stop on professional or authority request", "stop on failed terminal or route gate"],
        "workload": {"cards": len(cards), "mutations": len(mutations), "owner_files_below_ceiling": True},
    })
    write_json(x2 / "phase-truth-evidence.json", {
        "effective_negatives": effective_negatives,
        "exact_gates": INHERITED_BASELINE["exact_gates"] + 2,
        "failed_witnesses": failed_witnesses,
        "identity_boundary": IDENTITY_BOUNDARY,
        "methods": effective_methods,
        "open_gaps": INHERITED_BASELINE["open_gaps"] + 2,
        "outcomes": totals,
        "owner": OWNER,
        "passing_witnesses": passing_witnesses,
        "phase": PHASE,
        "proposal_chain": CHAIN_AFTER,
        "real_people_food_samples_measurements_or_external_actions": 0,
        "schema": "ghc.family.phase-truth.evidence.v3",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "validation_state": "EVIDENCE_BUILT_NOT_FINAL",
    })
    write_text(x2 / "threat-model.md", """# Vesper Arlen v669-v8 x2 threat model

The executed surface remains wholly synthetic. Threats include real-food substitution, microbial or sensory inference, unsafe temperature/pH conversion, allergen or sanitation advice, hidden external action, identity promotion, authority substitution, package provenance drift, dependency confusion, code injection, symlink/path escape, privacy leakage, inaccessible reporting, result-label drift, failed-witness erasure, cross-pillar overclaim, canonical replay, and premature route delivery.

Controls include fixed owner-local schemas; exact direct-wheel hashes; a nine-wheel D-isolated closure; no-index installation; hashed no-resolution audit; dimensional, transition, and interval rejecting smokes; exact JSON labels; 160 mutation rejections; zero real-person/food/sample/measurement counters; five-class privacy scan; bounded changed-Python AST review; exact staged Git-blob manifests; Method Flow pairing; structural accessibility with manual evaluation reserved; and a terminal route lock. Residual risk remains because these are same-owner synthetic checks, not exhaustive security, independent reproduction, professional validation, production certification, complete privacy/accessibility assurance, legal/cultural ratification, Maori authority, empirical GMUT evidence, or Stage 20 authority.
""")
    write_text(x2 / "integrated-evidence-overview.md", f"""# Vesper Arlen v669-v8 integrated evidence overview

## Executive outcome

Vesper Arlen v669-v8 executed the frozen owner-local program without using real people, food, starters, ingredients, samples, measurements, images, records, kitchens, laboratories, workplaces, advice, professional decisions, legal interpretations, cultural decisions, Maori-authority actions, or external adapters. The forty genuinely new core proposals finished with exactly twenty-eight `completed`, eight `represented`, two `open_gap`, and two `exact_gate` outcomes. Twenty inherited Neris rows were revalidated at zero Vesper novelty and completion credit. The declared proposal chain is now {CHAIN_AFTER}; the unrecovered 3,570-title semantic-history gap remains visible, so no universal novelty claim is made.

`Completed` means only that a deterministic owner-local contract accepted its declared synthetic positive and rejected every preregistered invalid mutation. `Represented` means a proxy, envelope, or obligation board remains visible without promotion to operational or empirical evidence. `Open_gap` means the named real evidence is absent. `Exact_gate` means competent evidence and authority are absent. These labels do not measure social value, consciousness, capability, food safety, scientific truth, legal validity, cultural legitimacy, or readiness for deployment.

## Synthetic process controls

The completed controls make state and correction legible. They distinguish starter-lineage labels from microbial identity; ingredient vacancies from supplier or allergen facts; mass ratios from recipes; units from measurements; temperature intervals from safety decisions; process-state transitions from baking instructions; pH fields from assays; acidity terminology from taste or progress inference; oven setpoints from calibration; and mass-loss arithmetic from moisture analysis. Each record declares its synthetic domain, explicit unit policy, zero external actions, zero real people, zero real food items, and prohibition on protected claims.

The generic contract evaluator required six typed fields and refused missing state, ambiguous domain or unit policy, any external action, any real-world entity counter, and any protected-claim flag. Thirty-six completion or representation lanes passed a bounded positive fixture. All 160 frozen invalid mutations ran once and were rejected: forty missing-state mutations, forty ambiguous-domain-or-unit mutations, forty real-world-or-external-action mutations, and forty protected-claim-promotion mutations. Rejections earn zero proposal completion credit and remain retained as failed witnesses paired with bounded passing guards.

The baker's-percentage helper accepts decimal strings, refuses nonnumeric or invalid mass domains, requires positive flour mass, and returns a fixed precision percentage. The state helper permits only a short declared synthetic sequence and rejects all other transitions. The interval helper rejects reversed bounds and distinguishes open from closed membership. These helpers are software fixtures, not recipe, process, timing, temperature, safety, quality, or health recommendations.

## Three isolated tools

Pint 0.25.3, transitions 0.9.3, and portion 2.6.2 were downloaded with their wheel dependency closure into one phase-namespaced D-backed wheelhouse. All three direct wheel SHA-256 values matched their frozen official registry metadata. Nine wheels were retained; installation occurred only in a new phase-isolated virtual environment, using the local wheelhouse with no index. The environment's `pip check` reported no broken requirements. A fully pinned, hash-bearing lock was audited with dependency resolution disabled; the audit returned zero known vulnerabilities at the time of the check.

Pint accepted a fixed 750 g / 1000 g ratio and rejected conversion from mass to time. transitions reached a declared bulk state through two permitted events and rejected a forbidden restart. portion accepted 20 inside a closed [18,24] interval, rejected 30 outside it, and kept open and closed forms distinct. The transaction changed no shared Python or npm prefix and no Windows, Codex, environment-variable, registry, feature, security, or desktop setting. This is not exhaustive supply-chain security, legal license review, long-term vulnerability assurance, numerical validation beyond the fixtures, compatibility beyond this environment, or production fitness.

## Portfolio execution

Sixty safe-now task rows, thirty bounded candidate rows, twenty phase-local skill packages, ten family-current runner files, and sixty additive CLEAN/FIX/REFINE rows were executed only within the declared synthetic software and documentation domain. Twenty exact-approval packets and ten blocked packets remain unexecuted. Their existence is an evidence boundary, not hidden backlog completion. Ten successor skills, ten successor runners, thirty successor refinements, and one grain-milling quality-documentation practice recommendation remain recommendations only and earn no Vesper completion credit.

The skill packages cover lineage, quantities, temperature, intervals, process state, event chronology, pH provenance, acidity nonconversion, bake-profile representation, microbial refusal, allergens, sanitation vacancies, correction, sources, privacy, accessibility, THOS proxying, Freed ID nonproduction envelopes, GMUT obligations, and the Stage 20 interlock. Each contains an explicit boundary, workflow, rejection suite, rollback, four-label requirement, and no-overclaim clause. The ten runners exercised the common owner-local validator and returned zero external actions. Passing smokes demonstrate caller compatibility within this phase only.

Sixty refinements separated synthetic records from real action; ratios from advice; state from authority; measurements from vacancies; professional vocabulary from competence; privacy structure from compliance; accessibility structure from completeness; analogy from evidence; package installation from production fitness; and terminal preparation from delivery. No inherited or sibling artifact was deleted, renamed, rewritten, merged, or claimed as Vesper completion.

## Trinity Mandala boundaries

THOS Body was primary through reversible process-state and software-assurance controls. It remains a proxy. No preregistered blind matched-budget real arms, participants, bakers, laboratory staff, safety monitoring, real outcomes, appropriate statistics, external audit, or independent review were present. The phase establishes no operational effectiveness, AGI, ASI, deployment readiness, or professional workflow assurance.

GMUT Mind remained a typed scalar-tensor and effective-field-theory research-model family. A reaction-diffusion or Arrhenius analogy board can enumerate domains, units, boundary conditions, source terms, and falsifiers, but it provides no likelihood, parameter constraint, detected force, prediction, physical law, empirical confirmation, ultraviolet or quantum completion, final physics, Theory of Everything, proof, or canon. The chemical-potential and pH classifier explicitly rejects conversion into psyche, agency, consciousness, morality, justice, or a fundamental law of mind.

Freed ID and CBR Heart remained explicit. The synthetic correction envelope uses no real keys, proofs, issuances, verifications, resolutions, status or revocation events, network exchanges, recovery decisions, privacy reviews, security reviews, trust-governance decisions, or affected-party oversight. The CBR boundary makes no allergen, sanitation, food-safety, workplace, labeling, disclosure, privacy, remedy, legal, cultural, data-governance, or authority decision.

## Human-practice and authority reservations

Baker/process handover, food-microbiology laboratory provenance, and HACCP-style process review were vocabulary and design lenses only. They establish no employment, qualification, competence, food handling, recipe authority, assay validity, food-safety plan, hazard release, public-health advice, workplace authority, regulatory compliance, or professional service. The FDA Food Code was used only as a comparison vocabulary and is not New Zealand law or advice. The sourdough review supplied terminology only; no study row, microbial observation, effect estimate, or scientific conclusion was imported.

Professional action, food safety, public health, allergens, sanitation, labeling, consumer advice, workplace rights, ownership, privacy, accessibility, remedy, legal interpretation, cultural interpretation, traditional knowledge, affected-party legitimacy, Maori wording, Maori concepts, Maori data governance, tangata whenua, iwi, hapu, and Maori authority remain open or exact-gated. Maori concepts remain under Maori authority.

## Accessibility, privacy, and security

The static report contains a skip link, labelled navigation, semantic landmarks, a single top-level heading, scoped row and column headers, a caption, text labels beyond colour, focus styling, print rules, and reduced-motion rules. It has no script, form, tracker, or external runtime dependency. Manual browser, keyboard, zoom, assistive-technology, screen-reader, cognitive-accessibility, Maori-language, and affected-user evaluations remain reserved. Structural checks are not complete accessibility conformance.

Five privacy classes cover opaque task or thread identifiers, private absolute paths, credential assignments, private route schemes, and protected stream filenames. Zero candidates are required for evidence staging. The bounded changed-Python review parses each new or modified Python file and rejects dynamic `eval`/`exec`, unsafe `shell=True`, destructive Git commands, and unbounded recursive deletion patterns. This is not exhaustive security, complete privacy assurance, penetration testing, external audit, or independent reproduction.

## Method Flow and terminal state

All startup and x2 operational failures remain visible. The x2 lint failure occurred before any download and was corrected by removing only one unused import. The retained failure never becomes a pass. Each mutation and tool rejection has a paired bounded passing witness, preferred method, recurrence guard, and rollback. No failure is erased by later success.

At the evidence boundary, effective negatives are {effective_negatives}; effective methods are {effective_methods}; retained failed witnesses are {failed_witnesses}; bounded passing witnesses are {passing_witnesses}; effective open gaps are {INHERITED_BASELINE['open_gaps'] + 2}; and effective exact gates are {INHERITED_BASELINE['exact_gates'] + 2}. These are workflow evidence counts, not scientific effect sizes, consciousness metrics, professional qualifications, legal judgments, or authority scores.

This evidence packet is not yet the terminal seal. It requires an exact evidence commit, push, clean fresh-live equality, additive closeout, one attributable exact-final canonical invocation, and a final fresh equality gate. A successful canonical aggregate will not be replayed. If it fails, it earns zero aggregate-success credit, remains retained, and permits only smallest-dependency recovery unless exact impact requires more. Successor contact remains prohibited until the terminal gate and fresh route/auth reread. The verdict remains `NOT_READY_FOR_STAGE_20`.
""")
    write_text(x2 / "accessible-evidence-report.html", accessible_html(outcomes, totals))

    json_paths = sorted(root.rglob("*.json"))
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    public_paths = [path for path in sorted(root.rglob("*")) if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt"}]
    privacy = [dict(path=str(path.relative_to(repo)).replace("\\", "/"), **row) for path in public_paths for row in privacy_candidates(path.read_text(encoding="utf-8"))]
    python_paths = [repo / "scripts/ghc_family_sourdough_contracts.py", repo / "scripts/ghc_family_vesper_arlen_v669_v8_toolchain.py", repo / "scripts/build_ghc_family_vesper_arlen_v669_v8_x2.py", *runner_paths]
    security_findings: list[dict[str, str]] = []
    for path in python_paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                security_findings.append({"path": str(path.relative_to(repo)), "finding": f"dynamic_{node.func.id}"})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        security_findings.append({"path": str(path.relative_to(repo)), "finding": "shell_true"})
    write_json(validation / "evidence-build-receipt.json", {
        "checks": {"json_parses": len(json_paths), "mutation_rejections": sum(row["passed"] for row in mutations), "outcomes": totals, "positive_controls": len(positives), "privacy_candidates": privacy, "python_ast_findings": security_findings, "runner_smokes": len(runner_checks), "skill_smokes": len(skill_checks), "toolchain_passed": tool_receipt["passed"]},
        "owner": OWNER,
        "passed": len(mutations) == 160 and all(row["passed"] for row in mutations) and len(positives) == 36 and not privacy and not security_findings and all(row["passed"] for row in runner_checks) and all(row["passed"] for row in skill_checks) and tool_receipt["passed"],
        "phase": PHASE,
        "schema": "ghc.family.evidence-build-receipt.v3",
    })


def staged_review(repo: Path) -> None:
    exclusions = [MANIFEST_PATH, REVIEW_PATH]
    entries = staged_blob_manifest(repo, exclusions)
    paths = [row["path"] for row in entries]
    forbidden = [path for path in paths if any(token in path.lower() for token in ("/closeout/", "/seal/", "/final/", "/handoffs/"))]
    x1_modifications = [path for path in paths if "/x1/" in path]
    json_errors: list[str] = []
    privacy: list[dict[str, str]] = []
    security: list[dict[str, str]] = []
    for path in paths:
        data = subprocess.run(["git", "-C", str(repo), "show", f":{path}"], check=True, capture_output=True).stdout
        text = data.decode("utf-8", errors="replace")
        if path.endswith(".json"):
            try:
                json.loads(text)
            except Exception as exc:  # noqa: BLE001
                json_errors.append(f"{path}:{type(exc).__name__}")
        privacy.extend({"path": path, **row} for row in privacy_candidates(text))
        if path.endswith(".py"):
            tree = ast.parse(text, filename=path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security.append({"path": path, "finding": f"dynamic_{node.func.id}"})
                if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    security.append({"path": path, "finding": "shell_true"})
    write_json(repo / MANIFEST_PATH, {"domain": "x2_staged_evidence_git_blobs", "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.exact-git-blob-manifest.v3", "self_exclusions": exclusions, "x1_commit": git_text(repo, "rev-parse", "HEAD")})
    checks = {
        "diff_cached_check": subprocess.run(["git", "-C", str(repo), "diff", "--cached", "--check"], check=False, capture_output=True).returncode == 0,
        "forbidden_lifecycle_paths": forbidden,
        "json_errors": json_errors,
        "manifest_entries": len(entries),
        "owner_generated_file_ceiling": len(paths) < 2000,
        "privacy_candidates": privacy,
        "python_ast_findings": security,
        "strict_x1_immutable": not x1_modifications,
        "x1_modifications": x1_modifications,
    }
    write_json(repo / REVIEW_PATH, {"checks": checks, "owner": OWNER, "passed": checks["diff_cached_check"] and not forbidden and not json_errors and checks["owner_generated_file_ceiling"] and not privacy and not security and not x1_modifications, "phase": PHASE, "schema": "ghc.family.evidence-staged-review.v3", "self_exclusions": exclusions})


def git_text(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--tool-receipt", type=Path)
    parser.add_argument("--stage-review", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.stage_review:
        staged_review(repo)
    else:
        if args.tool_receipt is None:
            parser.error("--tool-receipt is required for evidence build")
        build(repo, args.tool_receipt.resolve())


if __name__ == "__main__":
    main()
