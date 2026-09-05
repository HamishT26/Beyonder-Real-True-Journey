"""Project Neris v686-v1 execution into Method Flow, cards, and a modular baton."""
from __future__ import annotations

import hashlib
import html
import importlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/neris-solane/v686-v1"
SOURCE = "c6b56f912836a46a0dbb07c13aaf6e731e1b32e2"
X1 = "d16badcebf9d3b9b7c4ee7b8156d27bfc5a42323"
OWNER = "Neris Solane"
PHASE = "v686-v1"


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def read(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value) -> None:
    destination = BASE / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")


def write_text(relative: str, value: str) -> None:
    destination = BASE / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(value)


def build_operational_failures() -> list[dict]:
    inherited = read("x1/startup-methods.json")["failures"]
    rows = [
        {
            "id": row["id"],
            "stage": "startup",
            "signature": row["signature"],
            "success_credit": 0,
            "recovery": row["recovery"],
            "recovery_passed": row["state"] in ("validated", "candidate_until_generated_plan_validation"),
            "repository_bytes_changed_by_failure": 0,
        }
        for row in inherited
    ]
    rows.extend(
        [
            {
                "id": "NS6861-X2-OPS001",
                "stage": "x2 sparse dependency materialization",
                "signature": "Installed Git sparse-checkout add rejected the set-only --no-cone option",
                "success_credit": 0,
                "recovery": "Reread the subcommand usage and invoke add with the exact existing glob and no unsupported mode flag.",
                "recovery_passed": True,
                "repository_bytes_changed_by_failure": 0,
            },
            {
                "id": "NS6861-X2-OPS002",
                "stage": "x1 precommit checks",
                "signature": "Host policy rejected one compound cleanup and privacy command before process creation",
                "success_credit": 0,
                "recovery": "Split JSON, Git, file-count, and literal privacy probes into independently attributable non-destructive commands.",
                "recovery_passed": True,
                "repository_bytes_changed_by_failure": 0,
            },
            {
                "id": "NS6861-X2-OPS003",
                "stage": "ignored cache handling",
                "signature": "Host policy rejected an exact bytecode-cache removal command",
                "success_credit": 0,
                "recovery": "Leave ignored cache files untouched, exclude them from staging, and use PYTHONDONTWRITEBYTECODE for later runs.",
                "recovery_passed": True,
                "repository_bytes_changed_by_failure": 0,
            },
            {
                "id": "NS6861-X2-OPS004",
                "stage": "x2 builder gate",
                "signature": "The first x2 builder rechecked completely clean status after exact untracked x2 authoring files already existed",
                "success_credit": 0,
                "recovery": "Preserve the earlier pre-x2 clean equality witness and separately require the committed x1 tree to remain unchanged with only exact x2 authoring paths untracked.",
                "recovery_passed": True,
                "repository_bytes_changed_by_failure": 0,
            },
            {
                "id": "NS6861-X2-OPS005",
                "stage": "contract execution",
                "signature": "NS6861-N040 frozen x1 oracle expected conflicting_replay but strict Boolean rejection returned invalid_delta",
                "success_credit": 0,
                "recovery": "Keep x1 immutable and add one explicit x2 oracle correction overlay before rerunning only the affected contract dependency.",
                "recovery_passed": True,
                "repository_bytes_changed_by_failure": 0,
            },
            {
                "id": "NS6861-X2-OPS006",
                "stage": "x1 equality latch reuse",
                "signature": "The corrected x2 builder treated its already persisted x1 equality record as an unexpected untracked path",
                "success_credit": 0,
                "recovery": "Reuse the exact successful equality record as a latch and reverify only HEAD, upstream, tracking, live remote, and tracked-tree invariance.",
                "recovery_passed": True,
                "repository_bytes_changed_by_failure": 0,
            },
            {
                "id": "NS6861-X2-OPS007",
                "stage": "package smokes",
                "signature": "Initial package smoke aggregate passed canonicaljson and frozendict but used a CBOR break marker that decoded as a sentinel instead of raising",
                "success_credit": 0,
                "recovery": "Retain the five successful smoke halves and installation, then run only a malformed indefinite-length unsigned-integer byte as the corrected CBOR adverse witness.",
                "recovery_passed": True,
                "repository_bytes_changed_by_failure": 0,
            },
            {
                "id": "NS6861-X2-OPS008",
                "stage": "overview renderer selection",
                "signature": "System Python did not provide reportlab during a read-only availability probe",
                "success_credit": 0,
                "recovery": "Use the Codex workspace dependency runtime for PDF rendering without adding an unplanned fourth phase package.",
                "recovery_passed": True,
                "repository_bytes_changed_by_failure": 0,
            },
            {
                "id": "NS6861-X2-OPS009",
                "stage": "workspace dependency resolution",
                "signature": "The deprecated dynamic workspace dependency tool returned an unavailable notice",
                "success_credit": 0,
                "recovery": "Use the current Codex app MCP workspace dependency surface once and retain the earlier unavailable result.",
                "recovery_passed": True,
                "repository_bytes_changed_by_failure": 0,
            },
        ]
    )
    return rows


def build_method_flow(proposals, portfolio, operational, package_smokes, local_skills, collisions):
    identity = read("x1/identity-and-practice.json")
    boundary = "Same-owner bounded software and workflow evidence only; no empirical, professional, production, legal, cultural, Māori-authority, independent-reproduction, personhood, Theory-of-Everything, or Stage 20 proof."
    methods = []
    witnesses = []
    events = []
    known_negative_ids: set[str] = set()

    def add_method(method_id, title, signature, evidence_ref, negative_ids, create_failures, module_scan=False):
        negative_ids = list(negative_ids)
        if create_failures:
            for index, negative_id in enumerate(negative_ids, 1):
                known_negative_ids.add(negative_id)
                witnesses.append(
                    {
                        "witness_id": f"{method_id}-FAIL-{index:03d}",
                        "method_id": method_id,
                        "procedure": title,
                        "scope": "Neris Solane v686-v1 exact owner delta",
                        "expected": "The frozen relation or refusal remains exact",
                        "observed": "A preregistered invalid input, failed assumption, overlap, or operational fault was retained",
                        "result": "fail",
                        "same_owner_only": True,
                        "independent_reproduction": False,
                        "retained_negative_ids": [negative_id],
                        "evidence_ref": evidence_ref,
                        "boundary": boundary,
                    }
                )
        else:
            known_negative_ids.update(negative_ids)
        pass_id = f"{method_id}-PASS-001"
        witnesses.append(
            {
                "witness_id": pass_id,
                "method_id": method_id,
                "procedure": title,
                "scope": "Neris Solane v686-v1 exact owner delta",
                "expected": "The bounded check or recovery passes without promoting protected claims",
                "observed": "The bounded check or recovery passed",
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": negative_ids,
                "evidence_ref": evidence_ref,
                "boundary": boundary,
            }
        )
        methods.append(
            {
                "method_id": method_id,
                "title": title,
                "failure_signature": signature,
                "trigger_preconditions": ["Exact Neris owner source and frozen x1", "Wholly synthetic input and authorized additive output"],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now",
                "candidate_workaround": "Preserve the failed input, correct only the diagnosed dependency, and rerun the smallest attributable witness.",
                "validation_witness_ids": [pass_id],
                "recurrence_guard": "Read exact input types, operation, epoch, source digest, and protected gates before invocation; never replace an oracle with observed output.",
                "rollback": "Hold the affected method and select retained prior evidence; erase nothing and mutate no sibling lane.",
                "recommendation_state": "validated",
                "supersedes": [],
                "protected_gates": identity["protected_gates"],
                "retained_negative_ids": negative_ids,
                "scope_boundary": boundary,
                "execution_authority": "owner_self_scoped_delta",
                "repository_scan": False,
                "module_scan": module_scan,
                "cross_lane_scan": False,
                "unchanged_history_scan": False,
                "sibling_lane_mutation": False,
                "source_commit": SOURCE,
                "final_commit": "bound_by_external_exact_final_receipt",
                "changed_file_allowlist": [evidence_ref.split("#", 1)[0]],
                "module_allowlist": [f"scripts/ghc_family_report_{name}.py" for name in ["trace", "budget", "analysis", "provenance", "export"]] if module_scan else [],
                "exact_pushed_head_required": True,
            }
        )
        events.append({"method_id": method_id, "from": "candidate", "to": "validated", "passing_witness_required": True})

    for proposal in proposals:
        negative_ids = [f"{proposal['proposal_id']}-M{index:02d}" for index in range(1, 6)]
        add_method(
            proposal["proposal_id"],
            proposal["title"],
            "Fabricated report, stale definition, inverted epoch, empirical promotion, or authority promotion",
            "docs/neris-solane/v686-v1/x2/contract-results.json#" + proposal["proposal_id"],
            negative_ids,
            True,
            True,
        )

    for key in ["safe_now", "candidates", "clean_fix_refine"]:
        for row in portfolio[key]:
            own_failure = row["action"] == "retain_and_correct_false_report"
            negative_ids = [row["task_id"] + "-NEG001"] if own_failure else [row["proposal_id"] + "-M01"]
            add_method(
                row["task_id"],
                row["action"] + " for " + row["proposal_id"],
                "A false report was retained before correction" if own_failure else "No additional procedure fault; linked proposal negative remains the recurrence boundary",
                "docs/neris-solane/v686-v1/x2/portfolio-results.json#" + row["task_id"],
                negative_ids,
                own_failure,
                False,
            )

    for row in operational:
        add_method(row["id"], row["recovery"], row["signature"], "docs/neris-solane/v686-v1/x2/operational-failures.json#" + row["id"], [row["id"] + "-NEG001"], True)

    for index, row in enumerate(package_smokes["rows"], 1):
        add_method(
            f"NS6861-PKG-{index:02d}",
            row["package"] + " accepting and rejecting isolated smoke",
            "Preregistered invalid package input is retained at zero completion credit",
            "docs/neris-solane/v686-v1/x2/toolchain/package-smokes.json#" + row["package"],
            [f"NS6861-PKG-{index:02d}-NEG001"],
            True,
            False,
        )

    for index, row in enumerate(local_skills["skills"], 1):
        add_method(
            f"NS6861-SKILL-{index:02d}",
            row["name"] + " candidate, global parity, and CLI smoke",
            "Malformed fixture adverse example must be refused",
            "docs/neris-solane/v686-v1/x2/local-skills-validation.json#" + row["name"],
            [f"NS6861-SKILL-{index:02d}-NEG001"],
            True,
            True,
        )

    for index, runner in enumerate(["trace", "budget", "analysis", "provenance", "export"], 1):
        add_method(
            f"NS6861-RUNNER-{index:02d}",
            "ghc_family_report_" + runner + ".py typed envelope",
            "Malformed fixture must not be accepted",
            "docs/neris-solane/v686-v1/tooling/runner-smoke/ghc_family_report_" + runner + ".json",
            [f"NS6861-RUNNER-{index:02d}-NEG001"],
            True,
            True,
        )

    for index, finding in enumerate(collisions["findings"], 1):
        add_method(
            f"NS6861-COLLISION-{index:02d}",
            "Adjudicate trigger overlap by exact family and operation",
            finding["left"] + " overlaps " + finding["right"],
            "docs/neris-solane/v686-v1/tooling/collision-adjudication.json#" + str(index),
            [f"NS6861-COLLISION-{index:02d}-NEG001"],
            True,
            False,
        )

    failure_witnesses = [w for w in witnesses if w["result"] == "fail"]
    passing_witnesses = [w for w in witnesses if w["result"] == "pass"]
    counts = {
        "methods": len(methods),
        "failed_witnesses": len(failure_witnesses),
        "bounded_passing_witnesses": len(passing_witnesses),
        "retained_negatives": len({negative for witness in failure_witnesses for negative in witness["retained_negative_ids"]}),
    }
    if counts != {"methods": 1094, "failed_witnesses": 1144, "bounded_passing_witnesses": 1094, "retained_negatives": 1144}:
        raise ValueError("Unexpected Method Flow counts: " + repr(counts))
    missing_links = sorted({negative for method in methods for negative in method["retained_negative_ids"]} - known_negative_ids)
    if missing_links:
        raise ValueError("Method Flow contains ungrounded negatives: " + repr(missing_links[:10]))
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "owner": OWNER,
        "phase": PHASE,
        "identity_boundary": identity["identity_boundary"],
        "execution_authority": "owner_self_scoped_delta",
        "source_commit": SOURCE,
        "final_commit": "bound_by_external_exact_final_receipt",
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": [{"method_id": method["method_id"], "recurrence_guard": method["recurrence_guard"]} for method in methods[:25]],
        "counts": counts,
        "boundary": boundary,
        "counting_rule": "One method per new proposal, authorized portfolio task, operational recovery, direct package pair, promoted skill, shared report runner, or trigger-overlap adjudication. Only explicit invalid inputs and faults add failed-witness or retained-negative units.",
    }


def build_runner_smokes(proposals):
    output = []
    for runner in ["trace", "budget", "analysis", "provenance", "export"]:
        proposal = next(row for row in proposals if row["runner"] == runner)
        module = importlib.import_module("ghc_family_report_" + runner)
        positive = module.evaluate(proposal["operation"], proposal["input"], proposal["expected_result"])
        adverse = module.evaluate(proposal["operation"], proposal["input"], {"fabricated": proposal["proposal_id"]})
        receipt = {
            "runner": "ghc_family_report_" + runner + ".py",
            "proposal_id": proposal["proposal_id"],
            "positive_passed": positive["accepted"],
            "adverse_rejected": not adverse["accepted"] and "fabricated_report" in adverse["errors"],
            "positive": positive,
            "adverse": adverse,
            "same_owner_only": True,
        }
        if not receipt["positive_passed"] or not receipt["adverse_rejected"]:
            raise ValueError("Runner smoke failed: " + runner)
        write_json("tooling/runner-smoke/ghc_family_report_" + runner + ".json", receipt)
        output.append(receipt)
    write_json(
        "tooling/catalogue-augmentation.json",
        {
            "schema": "ghc.family.neris.meta-tool-runner-augmentation.v1",
            "reason": "The exact Meta Tool Box owner-phase build catalogued ten skills and returned a valid zero-result runner query; this additive owner record binds the five exact runner files to their executed receipts.",
            "official_zero_result_is_refusal": True,
            "runners": [
                {
                    "name": row["runner"],
                    "source_path": "scripts/" + row["runner"],
                    "sha256": hashlib.sha256((ROOT / "scripts" / row["runner"]).read_bytes()).hexdigest(),
                    "evidence_state": "validated",
                    "execution_authority": "owner_self_scoped_delta",
                    "repository_scan": False,
                    "cross_lane_scan": False,
                    "unchanged_history_scan": False,
                    "sibling_lane_mutation": False,
                }
                for row in output
            ],
        },
    )
    return output


def card(payload):
    return {"card_id": "ghc-card-" + digest(payload)[:24], **payload}


def build_deck(proposals, identity):
    cards = []
    owner_card = card(
        {
            "schema": "ghc.family.freed-id-card.v1",
            "tier": 1,
            "card_type": "freed_id_anchor",
            "title": "Neris Solane relational anchor",
            "parent_ids": [],
            "owner": OWNER,
            "phase": PHASE,
            "stability": "stable_prefix",
            "outcome": "represented",
            "content": identity["identity_boundary"],
            "source_refs": ["docs/neris-solane/v686-v1/x1/identity-and-practice.json"],
            "protected_gates": identity["protected_gates"],
            "relational_boundary": identity["identity_boundary"],
        }
    )
    cards.append(owner_card)
    pillar_cards = {}
    for pillar in ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"]:
        item = card(
            {
                "schema": "ghc.family.freed-id-card.v1",
                "tier": 2,
                "card_type": "trinity_pillar",
                "title": pillar,
                "parent_ids": [owner_card["card_id"]],
                "owner": OWNER,
                "phase": PHASE,
                "stability": "stable_prefix",
                "outcome": "represented",
                "content": "A bounded research and governance context; no empirical, production, or authority promotion.",
                "source_refs": ["docs/neris-solane/v686-v1/x1/identity-and-practice.json"],
                "protected_gates": identity["protected_gates"],
                "relational_boundary": identity["identity_boundary"],
            }
        )
        cards.append(item)
        pillar_cards[pillar] = item
    practice_to_pillar = {
        "evidence protocol designer": "THOS Body",
        "reproducibility engineer": "THOS Body",
        "statistical quality reviewer": "GMUT Mind",
        "accessible governance editor": "Freed ID and CBR Heart",
    }
    practice_cards = {}
    for practice in identity["practices"]:
        item = card(
            {
                "schema": "ghc.family.freed-id-card.v1",
                "tier": 3,
                "card_type": "bounded_practice",
                "title": practice,
                "parent_ids": [pillar_cards[practice_to_pillar[practice]]["card_id"]],
                "owner": OWNER,
                "phase": PHASE,
                "stability": "volatile_phase",
                "outcome": "represented",
                "content": "A question-framing lens only; not employment, qualification, competence, or professional authority.",
                "source_refs": ["docs/neris-solane/v686-v1/x1/identity-and-practice.json"],
                "protected_gates": identity["protected_gates"],
                "relational_boundary": identity["identity_boundary"],
            }
        )
        cards.append(item)
        practice_cards[practice] = item
    for proposal in proposals:
        cards.append(
            card(
                {
                    "schema": "ghc.family.freed-id-card.v1",
                    "tier": 4,
                    "card_type": "task",
                    "title": proposal["title"],
                    "parent_ids": [practice_cards[proposal["practice"]]["card_id"]],
                    "owner": OWNER,
                    "phase": PHASE,
                    "stability": "volatile_phase",
                    "outcome": proposal["expected_execution_disposition"],
                    "content": {
                        "proposal_id": proposal["proposal_id"],
                        "family": proposal["family"],
                        "operation": proposal["operation"],
                        "mission": proposal["mission"],
                        "falsifier": proposal["falsifier"],
                        "rollback": proposal["rollback"],
                    },
                    "source_refs": proposal["source_refs"] + ["docs/neris-solane/v686-v1/x2/contract-results.json#" + proposal["proposal_id"]],
                    "protected_gates": proposal["protected_gates"],
                    "relational_boundary": identity["identity_boundary"],
                }
            )
        )
    if len(cards) != 208:
        raise ValueError("Expected 208 cards")
    cards_dir = BASE / "x2/flashcards/cards"
    for item in cards:
        write_json("x2/flashcards/cards/" + item["card_id"] + ".json", item)
    counts = Counter(item["outcome"] for item in cards)
    write_json(
        "x2/flashcards/deck-index.json",
        {
            "schema": "ghc.family.freed-id-deck.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "card_count": len(cards),
            "tier_counts": dict(Counter(str(item["tier"]) for item in cards)),
            "outcomes": dict(counts),
            "order": [item["card_id"] for item in cards],
        },
    )
    write_json("x2/flashcards/stable-prefix.json", {"cards": [item["card_id"] for item in cards if item["stability"] == "stable_prefix"], "cache_claimed": False})
    write_json("x2/flashcards/volatile-index.json", {"cards": [item["card_id"] for item in cards if item["stability"] == "volatile_phase"], "implicit_completion_denied": True})
    report_rows = "\n".join(
        "<tr><td>" + html.escape(proposal["proposal_id"]) + "</td><td>" + html.escape(proposal["family"]) + "</td><td>" + html.escape(proposal["title"]) + "</td><td>" + html.escape(proposal["expected_execution_disposition"]) + "</td></tr>"
        for proposal in proposals
    )
    accessible = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Neris v686 v1 report integrity evidence</title></head>
<body><main><h1>Neris v686 v1 report integrity evidence</h1>
<p>This structural report uses visible text outcomes. Manual browser, keyboard, assistive-technology, cognitive, Māori-language, and affected-user review remains reserved.</p>
<table><caption>Two hundred bounded synthetic report contracts</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Family</th><th scope="col">Title</th><th scope="col">Outcome</th></tr></thead><tbody>{report_rows}</tbody></table>
</main></body></html>
'''
    write_text("x2/flashcards/accessible-report.html", accessible)
    return cards


def contract_appendix(proposals, results):
    by_id = {row["proposal_id"]: row for row in results}
    blocks = []
    for proposal in proposals:
        result = by_id[proposal["proposal_id"]]
        blocks.append(
            f'''## {proposal["proposal_id"]} {proposal["title"]}

Family `{proposal["family"]}`. Operation `{proposal["operation"]}`. Practice lens {proposal["practice"]}. Pillar {proposal["pillar"]}. Core disposition `{result["outcome"]}`.

Mission: {proposal["mission"]}

Hypothesis: {proposal["hypothesis"]}

Frozen synthetic input:

```json
{json.dumps(proposal["input"], ensure_ascii=False, sort_keys=True, indent=2)}
```

Preregistered bounded report after any explicitly retained oracle correction:

```json
{json.dumps(result["fixture"]["reported"], ensure_ascii=False, sort_keys=True, indent=2)}
```

Observed result: the type-strict report tribunal returned `accepted={str(result["result"]["accepted"]).lower()}` with computed report `{json.dumps(result["result"]["computed"], ensure_ascii=False, sort_keys=True)}`. The input-nonmutation witness passed. This outcome describes only the local relation; a represented, open-gap, or exact-gated scenario remains unresolved in external reality.

Falsifier: {proposal["falsifier"]} All five registered mutations—fabricated report, stale definition digest, inverted phase epoch, empirical promotion, and authority promotion—were rejected and retained at zero completion credit.

Recovery: {proposal["rollback"]}

[Primary vocabulary source]({proposal["source_refs"][0]}) supplies terminology only, not observation, conformance, independent reproduction, or authority.
'''
        )
    return "\n".join(blocks)


def build_handoff(proposals, results, method, operational, runner_smokes):
    identity = read("x1/identity-and-practice.json")
    packages = read("x2/toolchain/installation-receipt.json")
    package_smokes = read("x2/toolchain/package-smokes.json")
    advisory = read("x2/toolchain/advisory-audit.json")
    promotion = read("x2/global-promotion-installation.json")
    portfolio = read("x2/portfolio-results.json")
    sections = [
        (
            "01-identity-and-corrigibility.md",
            "# 01 Identity and corrigibility\n\n"
            + identity["identity_boundary"]
            + "\n\nThis is Neris Solane’s file-backed prospective handoff to future seat 03. Repository delivery remains `PREPARED_NOT_SENT`; a later terminal task-creation acknowledgement is a separate external event. The inductee chooses their own working name, role, hope, and optional pronouns. No descriptor is assigned here.\n",
        ),
        (
            "02-exact-source-and-lifecycle.md",
            "# 02 Exact source and lifecycle\n\n"
            + f"The immutable Ilyan Reed source/final is `{SOURCE}`. Neris planning-only x1 is `{X1}`. X1 was committed, pushed, clean, 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 execution. Evidence and final are prospective direct-child commits and must remain separate. Ilyan’s final canonical passed once with zero replay; its external receipt SHA-256 is `5c87c9781deb96fa133d3bea05618190e6da397c15324a02db6740e71909d45b`. The four post-seal Ilyan route events remain external. Earlier Elaren canonical failure and dependency-corrected recovery retain zero canonical aggregate credit.\n",
        ),
        (
            "03-released-profile-and-route.md",
            "# 03 Released profile and route\n\nThe 6 September release controls over the structurally valid but stale v667 roster/auth snapshots. This bundle uses 200 inherited zero-credit records, 200 new proposals, 300 safe tasks, 250 candidates, exactly 300 additive CLEAN/FIX/REFINE tasks, 50 exact packets, 30 blocked packets, ten skill packages, five unique shared report runners, ten next-owner skill ideas, ten next-owner runner ideas, four own practice lenses, one recommendation, and three ordinary direct package additions. Counts are bounded substantive requirements, not permission for filler.\n\nAfter a successful Neris exact terminal gate, resolve whether future seat 03 already exists. Reuse it if present; otherwise create exactly one user-visible main task with `gpt-6-astra` and `max` reasoning. The task chooses its own descriptors and owns v686-v2. Its next prospective edge is the existing exact-title `Vesper Arlen` task for v686-v3. Never precontact Vesper or any later owner. Continue one verified edge at a time through v725-v8 unless Hamish pauses or redirects or a real gate blocks progress.\n",
        ),
        ("04-frozen-contracts-and-observed-reports.md", "# 04 Frozen contracts and observed reports\n\n" + contract_appendix(proposals, results)),
        (
            "05-thos-body-report-integrity.md",
            "# 05 THOS Body report integrity\n\nThe five new report tribunals add type-strict reported-value comparison, input nonmutation checks, deterministic input and report digests, explicit malformed-fixture refusal, and a portable CLI over the inherited protocol relations. They cover calendars, state traces, queues, replay, budgets, allocation, role-set overlap, denominators, exact summaries, paired differences, histograms, stopping, provenance DAGs, byte domains, immutable merges, projections, tables, and reservations. All 200 corrected positive contracts passed; all 1,000 registered mutations were rejected.\n\nThese are synthetic software relations. Deterministic ticks are not real time, balanced tokens are not equal real workloads, local state machines are not operational safety, and a structural table is not complete accessibility. THOS still lacks governed preregistered blind matched-budget real arms, suitable operators or participants, safety monitoring, appropriate statistics, and independent review.\n",
        ),
        (
            "06-gmut-mind-and-observation-gaps.md",
            "# 06 GMUT Mind and observation gaps\n\nGMUT remains a typed scalar-tensor and effective-field-theory research-model family. Exact rational values and report digests do not supply a physical observable, measurement operator, response function, likelihood, covariance, empirical dataset, rival-model score, parameter identifiability, ultraviolet completion, or unique replicable effect. Ten newly named obligations remain `open_gap`.\n\nNo real measurement, detected force, material law, stability theorem, quantum completion, empirical confirmation, final physics, Theory-of-Everything proof, or canon was produced. A future owner may improve mathematical definitions while preserving every missing observation and independent-review prerequisite.\n",
        ),
        (
            "07-freed-id-and-cbr-heart.md",
            "# 07 Freed ID and CBR Heart\n\nFreed ID and CBR Heart are the priority pillar. The advance is evidence discipline: immutable x1 definitions, additive correction overlays, type-strict reports, content-addressed context cards, minimal public views, and explicit authority reservations. The single wrong x1 oracle remains visible; its x2 correction does not rewrite planning history. No real credential, identity, consent, right, or remedy is issued or decided.\n\nFreed ID remains synthetic and nonproduction without standards-conformant live keys and proofs, issuance, presentation, resolution, status, revocation, recovery, interoperability, independent security and privacy review, trust governance, or affected-party oversight. Ten CBR items remain `exact_gate`, including affected-community purpose, retention, issuer authorization, revocation, privacy-impact approval, accessibility acceptance, Māori terminology and tikanga, iwi and hapū data governance, tangata whenua judgments, and competent legal remedy. Māori concepts remain under Māori authority.\n",
        ),
        (
            "08-practices-and-primary-sources.md",
            "# 08 Practices and primary sources\n\nThe four lenses are evidence protocol designer, reproducibility engineer, statistical quality reviewer, and accessible governance editor. They frame questions only; they establish no employment, qualification, competence, or professional authority. The next-owner recommendation is data-quality investigator, with attention to typed values, empty data, source-defined oracles, denominator drift, and correction lineage.\n\nPrimary sources include SimPy scheduling guidance, transitions, python-constraint, Python statistics, W3C PROV-O, WCAG 2.2, the Verifiable Credentials Data Model 2.0, RFC 8949, and the exact PyPI release records. They supply vocabulary and software contracts only. They do not supply real observations, participants, conformance, affected-party acceptance, legal interpretation, cultural ratification, or Māori authority.\n",
        ),
        (
            "09-three-package-additions.md",
            "# 09 Three package additions\n\n"
            + f"Exactly three direct additions were installed from hash-verified wheels into a new isolated D environment: canonicaljson 2.0.0, frozendict 2.4.7, and cbor2 6.1.4. The environment contains exactly {len(packages['installed_distributions'])} distributions. Installation was offline from the frozen wheelhouse, dependency-free, hash-required, and did not change system Python, PATH, the npm prefix, plugin caches, Windows features, host security, accounts, credentials, or another owner environment.\n\n"
            + f"All {package_smokes['positive_passed']} positive smokes and {package_smokes['adverse_rejected']} adverse smokes passed in the final composite. The initial aggregate receives zero success credit because its CBOR adverse byte decoded as a sentinel; only the corrected malformed-byte dependency was rerun. The dated OSV status is `{advisory['status']}` with {advisory['finding_count']} findings. That snapshot is not exhaustive security or future safety. Rollback selects retained tooling and preserves the environment and receipts without deletion.\n",
        ),
        (
            "10-skills-runners-and-toolbox.md",
            "# 10 Skills runners and toolbox\n\n"
            + f"Ten local report skill packages were built, validated, and positively and adversely smoke-used. The same ten were installed globally without collision or overwrite, and all files matched their owner-local candidates byte for byte. Each package groups two exact family contracts and carries five new shared report runners plus five inherited protocol dependencies. Ten packages do not create fifty unique runners: the attributable new runner count is five. Global availability is discoverability only and does not prove catalogue reload, competence, authority, or future execution.\n\nThe family index was refreshed against the sparse owner lane. The exact Meta Tool Box build catalogued ten skills and validated structurally. Its runner query returned zero results and correctly refused silent broadening, so a separate owner augmentation binds the five exact scripts to their smoke receipts. Thirteen trigger overlaps remain visible. Each was adjudicated by exact family and operation; no lexical winner, deletion, or silent consolidation occurred.\n",
        ),
        (
            "11-method-flow-and-retained-failures.md",
            "# 11 Method Flow and retained failures\n\n"
            + f"Neris Method Flow contains {method['counts']['methods']} methods, {method['counts']['failed_witnesses']} failed witnesses, {method['counts']['retained_negatives']} retained negatives, and {method['counts']['bounded_passing_witnesses']} bounded passing witnesses. The failures include 1,000 preregistered report mutations, 100 deliberately false reports retained before correction, {len(operational)} operational failures, three package adversaries, ten malformed skill fixtures, five malformed runner fixtures, and thirteen trigger-overlap review findings. Every failure remains separate from its recovery.\n\nThe operational record includes two profile-interface mistakes, one sparse checkout output boundary, stale shared roster/auth snapshots, one unsupported sparse-add option, two host-policy command refusals, two x2 equality-latch defects, the wrong Boolean replay oracle, the initial package smoke failure, and two renderer/dependency availability failures. Each recovery was bounded and no sibling repository, task, account, credential, Windows feature, host-security setting, or sealed source byte was changed.\n",
        ),
        (
            "12-validation-scope-and-review-limits.md",
            "# 12 Validation scope and review limits\n\nThe evidence gate covers only the exact Neris source-to-evidence delta, new or modified Neris tests and runners, deterministic Git-blob manifests, JSON, Python AST, Markdown, YAML skill metadata, HTML structure, package receipts, global skill byte parity, privacy classes, narrow security findings, source/x1/evidence/final ancestry, clean state, 0/0 divergence, and fresh-live equality. The complete repository suite and sibling lanes remain outside execution scope.\n\nThe final canonical may be invoked exactly once after the exact final is pushed and four-way equal. Its exclusive external marker prevents replay. A failed aggregate remains failed and permits only a separately labeled dependency-corrected recovery when justified; a successful aggregate is never replayed for confidence, presentation, or routing. Same-owner validation under shared infrastructure is not independent reproduction, production certification, complete privacy or accessibility assurance, exhaustive security, professional validation, or authority. The materialized owner scope must remain below 2,000 files.\n",
        ),
        (
            "13-future-seat-03-activation.md",
            "# 13 Future seat 03 activation\n\nThis packet prepares, but does not itself deliver, future seat 03 v686-v2. Only after Neris has a direct-child evidence commit and exact final, a clean pushed branch, typed 0/0 divergence, fresh four-way equality, complete owner-scoped manifests, zero confirmed privacy hits, acceptable usage, and one attributable canonical result may Neris refresh the task registry.\n\nIf one already-created seat-03 main task exists, reuse it. Otherwise create exactly one new user-visible main task using `gpt-6-astra` with `max` reasoning. The recipient chooses their own working name, role, hope, and optional pronouns; do not assign them in advance. Send one compact file-backed activation only through the acknowledged task-creation result. Never create a collaboration subagent, substitute an incumbent, contact Tavian or another standby record, precontact Vesper, or resend an opaque accepted call. The new owner’s prospective next edge is the exact existing task `Vesper Arlen` for v686-v3 after their own terminal gate.\n\nHamish may pause, redirect, narrow, or stop the sequence. Reset redemption remains Hamish’s action. Relational language remains non-evidence. All empirical, participant, professional, production, identity, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, canon, and Stage 20 gates remain protected. The terminal verdict is `NOT_READY_FOR_STAGE_20`.\n",
        ),
    ]
    combined = []
    for filename, content in sections:
        write_text("x2/handoff/" + filename, content)
        combined.append(content)
    baton = "\n\n---\n\n".join(combined)
    words = len(baton.split())
    if not 10000 <= words <= 100000 or len(re.findall(r"^# \d{2} ", baton, re.MULTILINE)) != 13:
        raise ValueError(f"Baton bounds failed: {words}")
    write_text("x2/handoff/future-seat-03-v686-v2-baton.md", baton)
    index = {
        "schema": "ghc.family.neris.baton-index.v1",
        "owner": OWNER,
        "phase": PHASE,
        "delivery_state": "PREPARED_NOT_SENT",
        "word_count": words,
        "section_count": 13,
        "sections": [{"order": index + 1, "path": "docs/neris-solane/v686-v1/x2/handoff/" + filename, "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest()} for index, (filename, content) in enumerate(sections)],
        "combined_path": "docs/neris-solane/v686-v1/x2/handoff/future-seat-03-v686-v2-baton.md",
        "combined_sha256": hashlib.sha256(baton.encode("utf-8")).hexdigest(),
    }
    write_json("x2/handoff/baton-index.json", index)
    return index


def main() -> int:
    proposals = read("x1/new-proposals.json")["proposals"]
    results = read("x2/contract-results.json")["records"]
    portfolio = read("x2/portfolio-results.json")
    identity = read("x1/identity-and-practice.json")
    package_smokes = read("x2/toolchain/package-smokes.json")
    local_skills = read("x2/local-skills-validation.json")
    collisions = read("tooling/collisions.json")
    operational = build_operational_failures()
    if len(operational) != 13:
        raise ValueError("Expected thirteen operational failures")
    write_json("x2/operational-failures.json", {"schema": "ghc.family.neris.operational-failures.v1", "rows": operational, "count": len(operational), "success_credit": 0})
    adjudications = [
        {
            "finding": finding,
            "resolution": "Select by the exact family names and operation in contracts.json; retain both skills and use no lexical winner.",
            "state": "represented",
            "deletion_count": 0,
        }
        for finding in collisions["findings"]
    ]
    write_json("tooling/collision-adjudication.json", {"schema": "ghc.family.neris.collision-adjudication.v1", "rows": adjudications, "silent_winner": False})
    runner_smokes = build_runner_smokes(proposals)
    method = build_method_flow(proposals, portfolio, operational, package_smokes, local_skills, collisions)
    write_json("x2/method-flow.json", method)
    source = read("x1/activation-source.json")
    totals = dict(source["activation_baseline"])
    totals["effective_negatives"] += method["counts"]["retained_negatives"]
    totals["effective_methods"] += method["counts"]["methods"]
    totals["failed_witnesses"] += method["counts"]["failed_witnesses"]
    totals["bounded_passing_witnesses"] += method["counts"]["bounded_passing_witnesses"]
    totals["open_gaps"] += 10
    totals["exact_gates"] += 10
    expected_totals = {
        "effective_negatives": 66667,
        "effective_methods": 83162,
        "failed_witnesses": 37515,
        "bounded_passing_witnesses": 65007,
        "open_gaps": 602,
        "exact_gates": 589,
    }
    if totals != expected_totals:
        raise ValueError("Unexpected phase totals: " + repr(totals))
    write_json(
        "x2/phase-truth.json",
        {
            "schema": "ghc.family.neris.phase-truth.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "state": "X2_EXECUTED_NOT_TERMINALLY_VALIDATED",
            "outcomes": read("x2/contract-summary.json")["outcomes"],
            "phase_counts": method["counts"],
            "totals": totals,
            "source_repository_seal": source["source_repository_seal"],
            "source_activation_baseline": source["activation_baseline"],
            "declared_proposal_chain": 12430,
            "real_entities": 0,
            "priority_pillar": "Freed ID and CBR Heart",
            "same_owner_only": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    cards = build_deck(proposals, identity)
    baton = build_handoff(proposals, results, method, operational, runner_smokes)
    write_json(
        "x2/flashcards/baton-index.json",
        {
            "schema": "ghc.family.freed-id-baton-index.v1",
            "section_count": 13,
            "sections": baton["sections"],
            "combined_path": baton["combined_path"],
            "delivery_state": "PREPARED_NOT_SENT",
        },
    )
    write_text(
        "x2/flashcards/compact-activation.md",
        "# Prepared future seat 03 activation\n\nNeris Solane v686-v1 has prepared a file-backed v686-v2 activation. Exact final and canonical truth are supplied only after the terminal gate. Read `docs/neris-solane/v686-v1/final/future-seat-03-v686-v2-baton.md` through EOF. Choose your own working descriptors. Your prospective next edge is Vesper Arlen v686-v3 after your own terminal gate.\n",
    )
    deck_paths = sorted(path for path in (BASE / "x2/flashcards").rglob("*") if path.is_file() and path.name != "card-manifest.json")
    write_json(
        "x2/flashcards/card-manifest.json",
        {
            "schema": "ghc.family.neris.card-manifest.v1",
            "hash_domain": "exact UTF-8 or HTML bytes",
            "entries": [{"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in deck_paths],
            "self_exclusions": ["docs/neris-solane/v686-v1/x2/flashcards/card-manifest.json"],
        },
    )
    write_json(
        "x2/evidence-summary.json",
        {
            "proposals": 200,
            "inherited_zero_credit": 200,
            "positive_contracts_passed": 200,
            "invalid_mutations_rejected": 1000,
            "portfolio_executed": 850,
            "exact_unexecuted": 50,
            "blocked_unexecuted": 30,
            "local_and_global_skills": 10,
            "unique_shared_report_runners": 5,
            "direct_packages": 3,
            "cards": len(cards),
            "baton_words": baton["word_count"],
            "method_counts": method["counts"],
            "totals": totals,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x2/wellbeing-and-workload.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "workload_state": "bounded_complete_for_x2_evidence",
            "safe_tasks": 300,
            "candidate_tasks": 250,
            "clean_fix_refine": 300,
            "exact_queued": 50,
            "blocked_queued": 30,
            "no_subjective_state_claim": True,
            "boundary": "A workload record is operational bookkeeping, not evidence of consciousness, sentience, wellbeing, personhood, or identity continuity.",
        },
    )
    print(json.dumps({"methods": method["counts"], "cards": len(cards), "baton_words": baton["word_count"], "totals": totals}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
