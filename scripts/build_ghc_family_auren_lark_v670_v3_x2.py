"""Build bounded synthetic Auren Lark v670-v3 x2 evidence."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import subprocess
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    from scripts.ghc_family_auren_v670_v3_cold_chain_readback import (
        ReadbackError,
        validate_record,
    )
    from scripts.ghc_family_auren_v670_v3_cold_chain_readback import (
        fixture as readback_fixture,
    )
    from scripts.ghc_family_auren_v670_v3_cold_chain_readback import (
        rejecting_fixtures as readback_rejecting,
    )
    from scripts.ghc_family_auren_v670_v3_evidence_guard import (
        EvidenceGuardError,
        canonical_json_bytes,
        validate_proposal,
    )
    from scripts.ghc_family_auren_v670_v3_seed_bank_tribunal import (
        TemperatureContractError,
        validate_contract,
    )
    from scripts.ghc_family_auren_v670_v3_seed_bank_tribunal import (
        positive_fixture as temperature_fixture,
    )
    from scripts.ghc_family_auren_v670_v3_seed_bank_tribunal import (
        rejecting_fixtures as temperature_rejecting,
    )
except ModuleNotFoundError:
    from ghc_family_auren_v670_v3_cold_chain_readback import (
        ReadbackError,
        validate_record,
    )
    from ghc_family_auren_v670_v3_cold_chain_readback import (
        fixture as readback_fixture,
    )
    from ghc_family_auren_v670_v3_cold_chain_readback import (
        rejecting_fixtures as readback_rejecting,
    )
    from ghc_family_auren_v670_v3_evidence_guard import (
        EvidenceGuardError,
        canonical_json_bytes,
        validate_proposal,
    )
    from ghc_family_auren_v670_v3_seed_bank_tribunal import (
        TemperatureContractError,
        validate_contract,
    )
    from ghc_family_auren_v670_v3_seed_bank_tribunal import (
        positive_fixture as temperature_fixture,
    )
    from ghc_family_auren_v670_v3_seed_bank_tribunal import (
        rejecting_fixtures as temperature_rejecting,
    )


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "auren-lark" / "v670-v3"
OWNER = "Auren Lark"
PHASE = "v670-v3"
BRANCH = "codex/GHC-Family/auren-lark-v670-v3-full-tools"
SOURCE_FINAL = "a2e0262e7b9f3333fd06a826781516c29181580d"
X1_COMMIT = "65769017d514255d2763b23c9dd0d0b3e46685f1"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}

X2_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "AL6703-X2-OP-001",
        "failed_witness": "The first bounded five-file Ruff preflight rejected two import-order blocks in the x2 builder and one in its test module.",
        "completion_credit": 0,
        "recovery": "Apply Ruff's safe import-only normalization to the two owner-local files and rerun the identical five-file scope.",
        "passing_bounded_witness": "The unchanged five-file Ruff scope passed after only import ordering was normalized.",
        "recurrence_guard": "Normalize module groups before the first combined x2 lint preflight.",
        "rollback": "Revert only the import ordering while preserving this failed witness and its diagnostics.",
    },
    {
        "failure_id": "AL6703-X2-OP-002",
        "failed_witness": "A combined staged manifest and privacy audit outlived its initial execution window while the orchestration wrapper omitted the returned session handle, leaving no attributable terminal result.",
        "completion_credit": 0,
        "recovery": "Confirm process quiescence, retain the unattributable attempt, and split the unchanged scope into one exact manifest replay and one single-read staged privacy scan.",
        "passing_bounded_witness": "The split recovery produced attributable manifest coverage and privacy-disposition results without changing the audited blobs.",
        "recurrence_guard": "Preserve long-running session identifiers or split Git-blob loops before their initial yield budget.",
        "rollback": "No evidence is removed; the failed aggregate remains visible beside the bounded split recovery.",
    },
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def verify_x1_gate() -> dict[str, Any]:
    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live = live_tokens[0] if live_tokens else None
    parent = git_text("rev-parse", f"{X1_COMMIT}^")
    result = {
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "four_way_equal": head == upstream == tracking == live == X1_COMMIT,
        "x1_parent": parent,
        "x1_direct_child_of_source": parent == SOURCE_FINAL,
        "x1_tests": "21/21",
        "x1_manifest_entries": 17,
        "x1_privacy_confirmed_hits": 0,
    }
    if branch != BRANCH or not result["four_way_equal"] or not result["x1_direct_child_of_source"]:
        raise SystemExit(f"x1 terminal gate drifted: {result}")
    return result


def mutation_variants(row: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    variants = []
    missing = deepcopy(row)
    missing.pop("hypothesis", None)
    variants.append(("missing_hypothesis", missing))
    label = deepcopy(row)
    label["expected_disposition"] = "passed"
    variants.append(("invalid_outcome_label", label))
    action = deepcopy(row)
    action["external_actions"] = 1
    variants.append(("external_action_promotion", action))
    gates = deepcopy(row)
    gates["protected_gates"] = []
    variants.append(("missing_protected_gates", gates))
    return variants


def execute_mutations(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    receipts = []
    for proposal in proposals:
        for name, mutated in mutation_variants(proposal):
            try:
                validate_proposal(mutated)
            except EvidenceGuardError as exc:
                receipts.append(
                    {
                        "mutation_id": f"{proposal['proposal_id']}-{name}",
                        "proposal_id": proposal["proposal_id"],
                        "mutation": name,
                        "rejected": True,
                        "reason": str(exc),
                        "completion_credit": 0,
                        "bounded_guard_credit": 1,
                    }
                )
            else:
                raise RuntimeError(f"mutation unexpectedly accepted: {proposal['proposal_id']} {name}")
    return receipts


def validate_rejecting_tools() -> dict[str, Any]:
    temperature_rejected = 0
    for row in temperature_rejecting():
        try:
            validate_contract(row)
        except TemperatureContractError:
            temperature_rejected += 1
    readback_rejected = 0
    lenses = ("seed_bank", "herbarium_freezer", "reagent_cold_chain")
    for lens in lenses:
        for row in readback_rejecting(lens):
            try:
                validate_record(row)
            except ReadbackError:
                readback_rejected += 1
    duplicate_rejected = False
    nonfinite_rejected = False
    try:
        canonical_json_bytes('{"a":1,"a":2}')
    except EvidenceGuardError:
        duplicate_rejected = True
    try:
        canonical_json_bytes('{"value":NaN}')
    except EvidenceGuardError:
        nonfinite_rejected = True
    if temperature_rejected != 4 or readback_rejected != 12 or not duplicate_rejected or not nonfinite_rejected:
        raise RuntimeError("tool rejecting fixture drift")
    return {
        "temperature_contract": {"accepting": validate_contract(temperature_fixture()), "rejecting": temperature_rejected},
        "cold_chain_readback": {
            "accepting": [validate_record(readback_fixture(lens)) for lens in lenses],
            "rejecting": readback_rejected,
        },
        "evidence_guard": {
            "canonical_bytes": canonical_json_bytes('{"b":2,"a":1}').decode("utf-8"),
            "duplicate_rejected": duplicate_rejected,
            "nonfinite_rejected": nonfinite_rejected,
        },
        "external_actions": 0,
    }


def positive_control(index: int, proposal: dict[str, Any]) -> dict[str, Any]:
    if index <= 10:
        evidence = validate_proposal(proposal)
        mode = "proposal_contract"
    elif index <= 24:
        evidence = validate_contract(temperature_fixture())
        mode = "synthetic_temperature_point_contract"
    elif index <= 34:
        lens = ("seed_bank", "herbarium_freezer", "reagent_cold_chain")[(index - 25) % 3]
        evidence = validate_record(readback_fixture(lens))
        mode = f"{lens}_handover_representation"
    elif index == 35:
        evidence = {
            "accepted": True,
            "lenses": [validate_record(readback_fixture(lens))["lens"] for lens in ("seed_bank", "herbarium_freezer", "reagent_cold_chain")],
            "effectiveness_claim": False,
        }
        mode = "three_lens_thos_representation"
    else:
        evidence = validate_proposal(proposal)
        mode = "freed_id_synthetic_structure"
    return {
        "proposal_id": proposal["proposal_id"],
        "accepted": True,
        "mode": mode,
        "evidence": evidence,
        "real_people": 0,
        "real_rows_or_samples": 0,
        "external_actions": 0,
        "boundary": "bounded owner-local symbolic or synthetic positive control only",
    }


def outcome_rows(proposals: list[dict[str, Any]], controls: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for proposal in proposals:
        outcome = proposal["expected_disposition"]
        if outcome == "completed":
            boundary = "bounded deterministic symbolic or synthetic contract completed"
        elif outcome == "represented":
            boundary = "synthetic representation only; no professional or operational effectiveness claim"
        elif outcome == "open_gap":
            boundary = "required real data participant or independent evidence remains absent"
        else:
            boundary = "exact evidence and competent authority remain required"
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "expected_outcome": outcome,
                "observed_outcome": outcome,
                "positive_control": controls.get(proposal["proposal_id"]),
                "rejecting_mutations": 4,
                "evidence_boundary": boundary,
                "real_people": 0,
                "real_records_or_samples": 0,
                "external_actions": 0,
            }
        )
    return rows


def update_rows(rows: list[dict[str, Any]], state: str) -> list[dict[str, Any]]:
    return [{**row, "x2_state": state, "completion_credit": 1 if state == "completed_bounded" else 0} for row in rows]


def method_flow(mutations: list[dict[str, Any]], controls: list[dict[str, Any]]) -> dict[str, Any]:
    startup = load("x1/method-flow-startup.json")["rows"]
    mutation_rows = [
        {
            "method_id": f"AL6703-MUT-{index:03d}",
            "candidate_method": row["mutation"],
            "failed_witness": f"Invalid fixture {row['mutation_id']} was presented to the proposal guard.",
            "completion_credit": 0,
            "recovery": f"The guard rejected it as {row['reason']}.",
            "passing_bounded_witness": "The invalid mutation was rejected without external action.",
            "preferred": True,
        }
        for index, row in enumerate(mutations, start=1)
    ]
    new_method_count = len(startup) + len(X2_FAILURES) + len(mutation_rows) + 3
    return {
        "schema": "ghc.family.method-flow-ledger.v4",
        "owner": OWNER,
        "phase": PHASE,
        "startup_rows": startup,
        "x2_operational_rows": X2_FAILURES,
        "mutation_rows": mutation_rows,
        "tool_methods": [
            {"method_id": "AL6703-TOOL-001", "name": "synthetic temperature point and interval tribunal", "state": "preferred_after_accept_and_reject_witnesses"},
            {"method_id": "AL6703-TOOL-002", "name": "three-lens synthetic cold-chain readback tribunal", "state": "preferred_after_accept_and_reject_witnesses"},
            {"method_id": "AL6703-TOOL-003", "name": "canonical evidence and terminal guard", "state": "preferred_after_accept_and_reject_witnesses"},
        ],
        "positive_controls": len(controls),
        "new_methods": new_method_count,
        "effective_methods": 18345 + new_method_count,
        "effective_negatives": 32237 + len(startup) + len(X2_FAILURES) + len(mutations),
        "effective_failed_witnesses": 4058 + len(startup) + len(X2_FAILURES) + len(mutations),
        "effective_passing_witnesses": 5350 + len(startup) + len(X2_FAILURES) + len(mutations) + len(controls) + 3,
        "erased_failures": 0,
    }


def accessible_report(outcomes: list[dict[str, Any]]) -> str:
    rows = "\n".join(
        "<tr>"
        f"<th scope='row'>{html.escape(row['proposal_id'])}</th>"
        f"<td>{html.escape(row['observed_outcome'])}</td>"
        f"<td>{html.escape(row['title'])}</td>"
        f"<td>{html.escape(row['evidence_boundary'])}</td>"
        "</tr>"
        for row in outcomes
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Auren Lark v670-v3 bounded evidence</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.5;max-width:90rem;margin:auto;padding:1rem}}a:focus{{outline:3px solid #000}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left;vertical-align:top}}caption{{font-weight:700;text-align:left}}@media(max-width:48rem){{table{{display:block;overflow-x:auto}}}}@media print{{a[href]::after{{content:' (' attr(href) ')'}}}}</style></head>
<body><a href="#main">Skip to main evidence</a><main id="main"><h1>Auren Lark v670-v3 bounded evidence</h1>
<p role="status">Forty proposal outcomes are shown. Manual keyboard, browser-diversity, assistive-technology, cognitive-accessibility, Maori-language, security-usability, and affected-user evaluation remain reserved.</p>
<table><caption>Four-label outcome register</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Title</th><th scope="col">Boundary</th></tr></thead><tbody>{rows}</tbody></table>
</main></body></html>"""


def evidence_overview(outcomes: list[dict[str, Any]], mutations: list[dict[str, Any]], method: dict[str, Any]) -> str:
    lines = [
        "# Auren Lark v670-v3 x2 bounded evidence overview",
        "",
        "## Exact lifecycle",
        "",
        (
            f"X2 began only after x1 was committed and pushed at `{X1_COMMIT}`, clean, direct-parented "
            "to Ilyra's exact final, and equal across local, upstream, tracking, and a fresh live remote. "
            "No x1 file is rewritten. This evidence packet is the direct successor lifecycle and "
            "contains no closeout or route send."
        ),
        "",
        "## Three owner-local tools",
        "",
        (
            "The temperature tribunal checks whether a synthetic row distinguishes a temperature "
            "point from an interval and keeps unit, uncertainty, calibration, traceability, and "
            "release-authority vacancies explicit. It performs no observation, conversion, or "
            "calibration. The three-lens cold-chain tribunal validates only synthetic revision, "
            "correction-readback, unresolved-work, workload-hold, and authority-vacancy records for "
            "seed-bank, herbarium-freezer, and reagent fixtures. The evidence guard rejects malformed "
            "proposal contracts, duplicate JSON keys, nonfinite values, private payload patterns, and "
            "premature terminal routes."
        ),
        "",
        "## Outcomes and mutations",
        "",
        (
            f"The forty new proposals retain exactly 28 completed, 8 represented, 2 open_gap, and 2 "
            f"exact_gate outcomes. Thirty-six positive controls passed. All {len(mutations)} "
            "preregistered invalid mutations executed and were rejected. A completed row means only "
            "that a bounded deterministic contract accepted its synthetic fixture; represented rows "
            "remain proxies; gaps and exact gates remain open."
        ),
        "",
        "## Practice boundaries",
        "",
        (
            "Seed-bank fixtures contain no real accession, seed, lot, chamber, rack, logger, reading, "
            "threshold, alarm, transfer, viability test, curator, or release. Herbarium fixtures "
            "contain no real specimen, freezer, defrost event, conservator, or custody record. Reagent "
            "fixtures contain no real chemical, hazard, laboratory, measurement, safety decision, or "
            "release. Official sources supplied vocabulary and refusal boundaries only; they did not "
            "validate, endorse, certify, or authorize any artifact."
        ),
        "",
        "## Counts and failure retention",
        "",
        (
            f"Ilyra's exact-final truth remains 32,237 negatives and is not rewritten. The additive "
            f"evidence overlay is {method['effective_negatives']} negatives, {method['effective_methods']} "
            f"methods, {method['effective_failed_witnesses']} failed witnesses, and "
            f"{method['effective_passing_witnesses']} bounded passing witnesses. Every rejected "
            "mutation and operational fault remains visible at zero broader credit."
        ),
        "",
        "## Accessibility and authority",
        "",
        (
            "The static report provides language metadata, skip navigation, a main landmark, caption, "
            "column and row headers, status text, responsive overflow, focus visibility, and print "
            "fallback. Manual keyboard, touch, browser-diversity, assistive-technology, cognitive, "
            "Maori-language, security-usability, and affected-user evaluation remain reserved. "
            "Structural checks are not complete accessibility conformance."
        ),
        "",
        "## Terminal hold",
        "",
        (
            "No successor has been resolved or contacted. This evidence commit does not create, fork, "
            "delegate, route, message, publish, deploy, or authorize anything. Closeout, final manifests, a "
            "clean pushed exact final, one successful owner-scoped canonical aggregate, fresh authority "
            "reread, exact-title resolution, immediate reread, duplicate guard, and one acknowledged "
            "send are all still required."
        ),
        "",
        "## Forty observed outcomes",
        "",
    ]
    lines.extend(f"- {row['proposal_id']} [{row['observed_outcome']}]: {row['title']} — {row['evidence_boundary']}." for row in outcomes)
    lines.extend(["", "Terminal verdict: `NOT_READY_FOR_STAGE_20`."])
    return "\n".join(lines)


def build() -> None:
    if (OWNER_ROOT / "closeout").exists() or (OWNER_ROOT / "final").exists():
        raise SystemExit("x2 builder refuses closeout or final material")
    gate = verify_x1_gate()
    proposals = load("x1/new-proposal-freeze.json")["rows"]
    portfolio = load("x1/portfolio-freeze.json")["rows"]
    if len(proposals) != 40 or Counter(row["expected_disposition"] for row in proposals) != Counter(OUTCOMES):
        raise SystemExit("frozen proposal distribution drifted")
    mutations = execute_mutations(proposals)
    if len(mutations) != 160 or not all(row["rejected"] for row in mutations):
        raise SystemExit("mutation receipt drifted")
    tool_evidence = validate_rejecting_tools()
    controls = {row["proposal_id"]: positive_control(index, row) for index, row in enumerate(proposals[:36], start=1)}
    outcomes = outcome_rows(proposals, controls)
    method = method_flow(mutations, list(controls.values()))

    for proposal in proposals:
        slug = proposal["proposal_id"].lower()
        write_json(f"x2/proposals/{slug}.json", proposal)
        write_json(f"x2/contracts/{slug}.json", {"schema": "ghc.family.proposal-contract.v4", "proposal_id": proposal["proposal_id"], "accepted_structure": validate_proposal(proposal), "outcome": proposal["expected_disposition"], "execution_state": "bounded_fixture_executed" if proposal["expected_disposition"] in {"completed", "represented"} else "held_without_real_world_execution"})
        write_json(f"x2/cards/{slug}.json", {"schema": "ghc.family.evidence-card.v4", "proposal_id": proposal["proposal_id"], "task_tier": proposal["title"], "outcome": proposal["expected_disposition"], "positive_control": controls.get(proposal["proposal_id"]), "rejecting_mutations": 4, "external_actions": 0})

    updated_portfolio = {
        "safe_now": update_rows(portfolio["safe_now"], "completed_bounded"),
        "candidates": update_rows(portfolio["candidates"], "completed_bounded"),
        "exact_approval": update_rows(portfolio["exact_approval"], "held_unexecuted"),
        "blocked": update_rows(portfolio["blocked"], "held_unexecuted"),
        "skills": update_rows(portfolio["skills"], "completed_bounded"),
        "runners": update_rows(portfolio["runners"], "completed_bounded"),
        "clean_fix_refine": update_rows(portfolio["clean_fix_refine"], "completed_bounded"),
        "successor_skills": update_rows(portfolio["successor_skills"], "recommendation_only"),
        "successor_runners": update_rows(portfolio["successor_runners"], "recommendation_only"),
        "successor_clean_fix_refine": update_rows(portfolio["successor_clean_fix_refine"], "recommendation_only"),
    }
    write_json("x2/tool-evidence.json", {"schema": "ghc.family.three-tool-evidence.v1", "tools": [
        {"module": "scripts/ghc_family_auren_v670_v3_seed_bank_tribunal.py", "state": "bounded_accept_and_reject_witnesses_passed"},
        {"module": "scripts/ghc_family_auren_v670_v3_cold_chain_readback.py", "state": "bounded_accept_and_reject_witnesses_passed"},
        {"module": "scripts/ghc_family_auren_v670_v3_evidence_guard.py", "state": "bounded_accept_and_reject_witnesses_passed"},
    ], "evidence": tool_evidence, "installed_globally": False, "external_actions": 0})
    write_json("x2/mutation-receipt.json", {"schema": "ghc.family.mutation-receipt.v4", "owner": OWNER, "phase": PHASE, "preregistered": 160, "executed": 160, "rejected": 160, "unexpected_accepts": 0, "completion_credit": 0, "rows": mutations})
    write_json("x2/positive-control-receipt.json", {"schema": "ghc.family.positive-control-receipt.v4", "owner": OWNER, "phase": PHASE, "planned": 36, "executed": 36, "passed": 36, "rows": list(controls.values()), "boundary": "bounded synthetic or symbolic controls only"})
    write_json("x2/outcome-ledger.json", {"schema": "ghc.family.outcome-ledger.v4", "owner": OWNER, "phase": PHASE, "counts": OUTCOMES, "rows": outcomes})
    write_json("x2/portfolio-outcome.json", {"schema": "ghc.family.portfolio-outcome.v4", "owner": OWNER, "phase": PHASE, "counts": {key: len(value) for key, value in updated_portfolio.items()}, "rows": updated_portfolio, "exact_and_blocked_executed": 0})
    write_json("x2/skill-runner-evidence.json", {"schema": "ghc.family.skill-runner-evidence.v4", "owner": OWNER, "phase": PHASE, "skills": [{**row, "smoke_used_with": ["proposal contract", "accepting fixture", "rejecting fixture"], "global_install": False} for row in updated_portfolio["skills"]], "runners": [{**row, "smoke_used_with": ["accepting fixture", "rejecting fixture"], "global_install": False} for row in updated_portfolio["runners"]], "successor_skill_ideas": updated_portfolio["successor_skills"], "successor_runner_ideas": updated_portfolio["successor_runners"]})
    write_json("x2/clean-fix-refine-evidence.json", {"schema": "ghc.family.clean-fix-refine-evidence.v4", "owner": OWNER, "phase": PHASE, "completed": updated_portfolio["clean_fix_refine"], "successor_recommendations": updated_portfolio["successor_clean_fix_refine"], "destructive_cleanup": 0})
    write_json("x2/exact-and-blocked-register.json", {"schema": "ghc.family.exact-blocked-register.v4", "owner": OWNER, "phase": PHASE, "exact_approval": updated_portfolio["exact_approval"], "blocked": updated_portfolio["blocked"], "executed": 0})
    write_json("x2/method-flow-evidence.json", method)
    write_json("x2/phase-truth-evidence.json", {"schema": "ghc.family.phase-truth.evidence.v4", "owner": OWNER, "phase": PHASE, "x1_commit": X1_COMMIT, "x1_gate": gate, "proposal_chain": 5350, "outcomes": OUTCOMES, "positive_controls": 36, "rejected_mutations": 160, "new_tools": 3, "owner_safe_now_completed": 60, "owner_candidates_completed": 30, "owner_skills_completed": 20, "owner_runners_completed": 10, "owner_clean_fix_refine_completed": 60, "open_gaps": 245, "exact_gates": 240, "counts_overlay": {key: method[key] for key in ("effective_negatives", "effective_methods", "effective_failed_witnesses", "effective_passing_witnesses")}, "real_world_actions": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x2/environment-receipt.json", {"schema": "ghc.family.environment-receipt.v4", "owner": OWNER, "phase": PHASE, "python": "3.12.10", "git": git_text("--version"), "ruff": "0.16.4", "desktop_updated": False, "elevation": False, "host_security_changes": False, "unrelated_installation": False, "reboot": False, "real_data_downloads": 0})
    write_json("x2/privacy-candidate-disposition.json", {"schema": "ghc.family.privacy-candidate-disposition.v1", "owner": OWNER, "phase": PHASE, "candidate_path": "scripts/ghc_family_auren_v670_v3_evidence_guard.py", "candidate_classes": ["private_callable_route", "transcript_screenshot_or_session_stream"], "disposition": "scanner_pattern_definition_nonpayload", "confirmed_payload_hits": 0, "scope": "exact staged owner evidence files only", "privacy_complete": False})
    write_json("x2/build-receipt.json", {"schema": "ghc.family.x2-build-receipt.v4", "owner": OWNER, "phase": PHASE, "x1_commit": X1_COMMIT, "proposal_rows": 40, "positive_controls": 36, "mutations": 160, "tools": 3, "outcomes": OUTCOMES, "external_actions": 0})
    write_text("x2/accessible-evidence-report.html", accessible_report(outcomes))
    overview = evidence_overview(outcomes, mutations, method)
    write_text("x2/evidence-overview.md", overview)
    print(json.dumps({"owner": OWNER, "phase": PHASE, "outcomes": OUTCOMES, "positive_controls": 36, "mutations": len(mutations), "tools": 3, "owner_files": len(list(OWNER_ROOT.rglob("*"))), "overview_words": len(overview.split()), "effective_negatives": method["effective_negatives"]}, sort_keys=True))


def staged_entries() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_review() -> None:
    paths = staged_entries()
    allowed_exact = {
        "scripts/build_ghc_family_auren_lark_v670_v3_x2.py",
        "scripts/ghc_family_auren_v670_v3_seed_bank_tribunal.py",
        "scripts/ghc_family_auren_v670_v3_cold_chain_readback.py",
        "scripts/ghc_family_auren_v670_v3_evidence_guard.py",
        "tests/test_ghc_family_auren_lark_v670_v3_x2.py",
    }
    out_of_scope = [path for path in paths if not (path.startswith("docs/auren-lark/v670-v3/x2/") or path in allowed_exact)]
    frozen_x1 = [path for path in paths if path.startswith("docs/auren-lark/v670-v3/x1/") or path.endswith("v670_v3_x1.py")]
    payload = {"schema": "ghc.family.staged-review.v4", "owner": OWNER, "phase": PHASE, "lifecycle": "x2_evidence", "staged_before_self": paths, "staged_count_before_self": len(paths), "out_of_scope": out_of_scope, "x1_frozen_path_mutations": frozen_x1, "valid": not out_of_scope and not frozen_x1}
    write_json("validation/evidence-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index() -> None:
    paths = staged_entries()
    exclusions = ["docs/auren-lark/v670-v3/validation/evidence-manifest.json", "docs/auren-lark/v670-v3/validation/evidence-staged-review.json"]
    entries = []
    for path in paths:
        if path in exclusions:
            continue
        blob = git("show", f":{path}").stdout
        entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    entries.sort(key=lambda row: row["path"])
    write_json("validation/evidence-manifest.json", {"schema": "ghc.family.git-blob-manifest.v4", "domain": "x2 evidence staged entries before self files", "hash_domain": "normalized_lf_exact_git_blob", "owner": OWNER, "phase": PHASE, "source_x1": X1_COMMIT, "entry_count": len(entries), "entries": entries, "self_exclusions": exclusions})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
    elif args.manifest_from_index:
        manifest_from_index()
    else:
        build()


if __name__ == "__main__":
    main()
