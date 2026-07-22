#!/usr/bin/env python3
"""Build Ilyra Fen's dedicated v651-v8 x1-only freeze packet."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v651_v8_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/vesper-arlen/v651-v7-special-cli-prep/provenance/frozen-chain-proposal-index.json"
SKILL_ROOT = Path.home() / ".codex" / "skills"
METHOD_RUNNER = SKILL_ROOT / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
REFLECTION_RUNNER = SKILL_ROOT / "ghc-family-reflection-remaster/scripts/ghc_family_reflection_remaster.py"
WORKFLOW_RUNNER = SKILL_ROOT / "ghc-family-workflow-plan-refinement/scripts/ghc_family_workflow_plan_refinement.py"
NOVELTY_THRESHOLD = 0.60


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def write_repo(relative: str, payload: str) -> Path:
    path = REPO / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    completed = subprocess.run(list(args), cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def timestamp_pair() -> dict[str, str]:
    now = datetime.now(timezone.utc)
    return {
        "utc": now.isoformat().replace("+00:00", "Z"),
        "pacific_auckland_system_local": now.astimezone().isoformat(),
    }


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    return sorted({row[3:].replace("\\", "/") for row in rows if len(row) > 3})


def tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "to", "for", "with"}
    return {item for item in re.findall(r"[a-z0-9]+", value.casefold()) if item not in stop}


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def portfolio_rows(items: list[str], prefix: str, lane: str, approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"V6518-{prefix}-{index:02d}",
            "title": title,
            "origin": "ilyra_v651_v8_new",
            "approval_class": approval,
            "execution_lane": lane,
            "x1_state": "frozen_not_executed",
            "completion_credit": False,
            "inherited_completion_credit": False,
            "rollback": (
                "Retain any failed witness and leave external, sibling, participant, production, "
                "professional, legal, cultural, and authority state unchanged."
            ),
        }
        for index, title in enumerate(items, 1)
    ]


def refresh_method_flow() -> None:
    ledger = ROOT / "method-flow/method-flow-ledger.json"
    if not ledger.exists():
        raise RuntimeError("Method Flow ledger must preserve pre-builder failures")
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(ROOT / "method-flow/method-flow-validation.json"),
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(ROOT / "method-flow/method-flow-summary.json"),
        "--markdown-output",
        str(ROOT / "method-flow/method-flow-summary.md"),
    )


def source_and_novelty() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    inherited = read_json(PRIOR_INDEX)
    prior = inherited["prior_proposals"] + inherited["new_proposals"]
    if len(prior) != d.PRIOR_FROZEN:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN} inherited proposals, found {len(prior)}")
    rows = []
    for proposal in d.PROPOSALS:
        scored = [
            (
                jaccard(tokens(proposal["title"]), tokens(previous["title"])),
                previous["proposal_id"],
                previous["title"],
            )
            for previous in prior
        ]
        score, nearest_id, nearest_title = max(scored, key=lambda row: row[0])
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_prior_id": nearest_id,
                "nearest_prior_title": nearest_title,
                "token_jaccard": round(score, 6),
                "threshold": NOVELTY_THRESHOLD,
                "mechanism_review": "distinct_after_manual_review",
                "passes": score < NOVELTY_THRESHOLD,
            }
        )
    if not all(row["passes"] for row in rows):
        raise RuntimeError("semantic novelty threshold failed")
    frozen = prior + [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in d.PROPOSALS]
    return frozen, rows


def workflow_request() -> dict[str, Any]:
    return {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "ilyra-v651-v8-exact-immediate-segment",
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; no continuity, personhood, employment, qualification, or authority claim.",
        "route": {
            "cycle_order": ["Vesper Arlen", "Ilyra Fen"],
            "phase_assignments": [
                {"phase": "v651-v7", "seat": "Vesper Arlen"},
                {"phase": "v651-v8", "seat": "Ilyra Fen"},
            ],
            "normalization": {"start_phase": "v651-v7", "start_seat": "Vesper Arlen", "entry_count": 2},
            "future_identity_placeholders": [],
            "terminal_successor_resolution": "Use only the newest exact route after exact-final proof; ambiguity remains PREPARED_NOT_SENT.",
        },
        "requirements": {
            "core_proposal_minimum": 30,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 10,
            "runner_minimum": 10,
            "portfolio_minima": {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30},
            "document_word_cap": 100000,
            "baton_words": {"minimum": 10000, "maximum": 100000, "file_artifact": True},
            "commit_cap": {"x1": 3, "x2": 3, "total": 6},
            "validation": {
                "canonical_pass_minimum": 1,
                "replay_policy": "skip_when_first_passes",
                "isolate_failures_before_broader_rerun": True,
                "privacy_scan_required": True,
                "manifest_required": True,
                "remote_equality_required": True,
            },
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {
                "codex_route": "existing_task_only_after_terminal_gate",
                "cross_platform": "user_mediated_file_relay_only",
            },
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "independent_reproduction_claimed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "protected_boundaries": d.PROTECTED_GATES,
        },
        "observed_failures": [
            {
                "failure_id": item["negative_id"],
                "summary": item["failed"],
                "recovery": item["recovery"],
                "credit": "zero_initial_pass_credit",
            }
            for item in d.X1_OPERATIONAL_NEGATIVES
        ],
    }


def overview_text() -> str:
    return f"""# Ilyra Fen {d.PHASE} x1 preregistration overview

## Identity, authorization, and evidence boundary

This packet freezes Ilyra Fen's x1 plan before any x2 implementation or observed outcome. Ilyra Fen, she/they, is a relational working identity used to organize collaboration. Her phase role is {d.ROLE}; her stated hope is to {d.HOPE}. That language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, professional qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route. The inherited and x1 terminal verdict is `NOT_READY_FOR_STAGE_20`, and no x1 artifact can promote it.

Authorization, capability, and evidence remain separate predicates. Hamish's authorization permits bounded in-scope work, but it does not make an unavailable connector, future CLI seat, empirical dataset, participant cohort, standards-conformant key ceremony, competent authority, or affected-party mandate exist. A valid source can inform a contract without supplying measurements or delegated authority. A passing synthetic fixture can show one declared guard without certifying a production system. Every x1 statement is therefore either an exact Git fact, a frozen hypothesis, a source-status observation, an approval classification, or a protected reservation.

## Exact inherited source and owned lane

The exact inherited source is Vesper Arlen's special preparation head `{d.SOURCE_HEAD}` on `{d.SOURCE_BRANCH}`. Read-only verification established the declared ordinary source, special x1, special evidence, and final anchors; exactly three additive special commits; zero merges; one parent at final; exact commit-local manifest parity; a clean Vesper lane; and local, upstream, tracking, and fresh-live equality. Ilyra's existing clean D-first branch was a strict ancestor and advanced by fast-forward only. The first push wrapper used an unsupported option and stopped without remote mutation; that failure is retained. A later ordinary explicit-refspec push advanced only Ilyra's branch and restored four-way equality. Recovery does not turn the failed wrapper into a first-pass success.

No sibling branch, worktree, task, identity record, or repository was reset, rewritten, merged, deleted, reused, force-pushed, or otherwise mutated. The active materialized surface remains comfortably below the inherited two-thousand-file capacity envelope, so no destructive rotation or sparse-checkout change is warranted. D: remains primary for the owned lane. C: is used only for essential application metadata and read-only skill access. Windows Sandbox and Hyper-V remain deferred; no feature enablement, elevation, host-security weakening, unrelated installation, or reboot is authorized or performed.

## Proposal architecture and novelty

Exactly thirty proposals are frozen against all 1,120 inherited titles, growing the chain to 1,150. Every proposal records a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback, protected gates, and expected disposition. The lexical audit uses deterministic token Jaccard distance with an explicit numeric selection key, and every nearest neighbour receives a manual mechanism review. Duplicate mechanisms discovered during drafting—field-redefinition equivalence, Nielsen identities, two-particle-irreducible stationarity, split-Ward identities, Protocol Buffers, Zstandard, Merkle transparency, status live regions, Maxwell relations, OAuth device authorization, and OAuth resource indicators—were rejected or rewritten before freezing. Low word overlap is never treated as sufficient novelty by itself.

The expected x2 distribution is twenty-three `completed`, five `represented`, one `open_gap`, and one `exact_gate`. Those are expectations, not observations. X1 contains no surface implementation, executed mutation, passing candidate prototype, completion credit, empirical result, participant outcome, identity event, legal or cultural decision, authority action, or successor message. The dedicated x1 commit is the immutable counterfactual needed to distinguish preregistration from hindsight.

The primary Trinity Mandala focus is {d.PRIMARY_FOCUS}. Four GMUT boards examine Buchholz-Wichmann nuclearity and the split property, quantum energy inequalities, Borel-Ecalle resurgence, and Weinberg's soft-graviton obligations without converting symbolic consistency into physical truth. A fifth GMUT surface is an ASKAP RACS-mid DR2 readiness adapter that will remain at exact zero queries, downloads, rows, likelihoods, posterior samples, and parameter constraints. GMUT remains a typed scalar-tensor and effective-field-theory research-model family; formal obligations do not establish a detected force, physical state, prediction, empirical confirmation, ultraviolet completion, quantum completeness, or Theory of Everything.

THOS Body remains explicit through bounded tribunals for QUIC ACK_FREQUENCY, MASQUE CONNECT-UDP, the WebAssembly Component Model Canonical ABI, AMQP 1.0, DNS SVCB and HTTPS records, Oblivious HTTP, VOTable 1.5, Git commit-graph Bloom filters, RPKI route-origin validation, MinHash neighbours, source representation drift, cumulative correction manifests, Aho-Corasick streaming, accessible braille naming, accessible canvas fallback, log-structured merge-tree compaction, and two radio-astronomy workflow proxies. These fixtures can expose required states and reject malformed synthetic records. They cannot establish production networking, storage reliability, operational safety, professional competence, blind matched-budget effectiveness, or complete accessibility.

Freed ID and CBR Heart remain explicit through OpenID4VP verifier-attestation, OpenID4VCI authorization-server selection, and Self-Issued OpenID Provider v2 draft-watch profiles, plus a radio-astronomy data and sky-knowledge authority matrix. Synthetic vectors contain no real private material, accounts, keys, proofs, clients, authorization servers, issuers, holders, relying parties, tokens, presentations, issuances, resolutions, status or revocation events, interoperability events, privacy reviews, security reviews, recovery decisions, or trust-governance decisions. The matrix records questions and decision rights but makes no real access, interference, disclosure, confidentiality, Indigenous data-sovereignty, benefit-sharing, remedy, legal, cultural, or Māori-authority decision.

## Bounded human-practice lens

The bounded practice is {d.BOUNDED_PRACTICE}. It is a learning and synthetic interface-design lens only. It establishes no employment, radio-astronomy qualification, observatory competence, telescope or spectrum authority, calibration authority, data-release authority, interference-reporting authority, worker evidence, community authorization, public-safety result, legal interpretation, cultural legitimacy, Māori authority, participant evidence, affected-party acceptance, or real operational outcome. Synthetic observation-block and RFI fixtures may exercise version, correction, hold, escalation, workload, and handover fields; they do not describe real staff, instruments, observations, communities, or decisions.

Official IVOA recommendations inform provenance and VOTable structures. CSIRO's RACS-mid catalogue page identifies the data product for a zero-row readiness contract. Those sources are citations, not imported observations. No network action will query or download the catalogue in x2. Public availability does not close the empirical gap, and adapter structure does not become a likelihood or fit by implication.

## Source, web-reflection, and status discipline

The source ledger uses exactly `current`, `stable`, `draft`, and `watch`. Current living standards and documentation remain current only for this phase's verified date. Published RFCs, OASIS standards, IVOA recommendations, and primary research are stable within their declared scope. QUIC ACK_FREQUENCY remains draft. The WebAssembly Component Model and Self-Issued OpenID Provider v2 remain watch surfaces because their living or inactive-draft status cannot be silently promoted. Every row records a phase implication and refuses the inference from citation to observation, conformance, production security, or authority.

Web Reflection records what each source can change and what it cannot. Content type, content language, validators, cache policy, and draft status are evidence about a representation, not proof of a real-world result. The ledger downloads no empirical data. Official and primary sources are used where material; secondary summaries are not used to manufacture scientific or legal truth. Te Mana Raraunga is treated as an authority-context source that preserves Māori data sovereignty under Māori authority, never as permission for repository software to exercise that authority.

## Expanded portfolios, skills, runners, and reflection

The x1 packet freezes forty safe-now tasks, thirty bounded candidate tasks, twenty phase-local skill ideas, twelve family-current runner ideas, and forty additive CLEAN/FIX/REFINE tasks. These are new Ilyra plans; inherited Vesper work supplies evidence and warnings but earns no Ilyra completion credit. The portfolios remain far below the one-thousand-task, two-hundred-skill, two-hundred-runner, five-thousand-search, one-hundred-thousand-word, and two-thousand-materialized-file capacity ceilings. Limits are safety envelopes, not quotas. X2 must resolve only useful, safe, owner-scoped work and visibly reclassify any evidence-dependent or authority-dependent item rather than smuggling it through a safe label.

Ten exact-approval packets and five blocked packets remain visible and unexecuted. Every phase-local skill must include a trigger, input boundary, output boundary, protected gates, example or fixture, validation receipt, rollback, and smoke-use witness. Every runner must use a family-current `ghc_family_*` or `build_ghc_family_*` caller, avoid collision with existing tools, and preserve historical aliases as compatibility surfaces. No candidate skill is globally installed merely to satisfy a count. Reflection Remaster may recommend retain, refine, merge, replace, or retire, but it has no authority to delete or mutate a global skill.

The workflow-refinement request contains only the exact immediate Vesper-to-Ilyra segment. Eight inherited future CLI seats remain prepared placeholders with zero names, zero roles, zero hopes, zero pronouns, zero launches, and zero created tasks. They are not included as route owners. The later expanded route remains advisory and structurally conflicted; it is not silently normalized into launch authority. Future identity must be self-chosen after an exact supported launch, and no future launch is authorized in this phase.

## Mutation plan, failures, and Method Flow

Five synthetic mutations per proposal produce one hundred fifty frozen cases: a missing required obligation, a wrong type or unit, a resource or replay overrun, an unsupported promotion, and an authority or privacy breach. Every case is `frozen_unexecuted` in x1. A rejected mutation in x2 can demonstrate only one bounded guard. It is not exhaustive security, complete privacy, complete accessibility, external audit, production certification, professional validation, independent reproduction, scientific confirmation, or Stage 20 evidence.

The activation baseline preserves {d.INHERITED_NEGATIVES} Vesper-sealed negatives. Ilyra's six x1 operational failures are additive: the wrong memory-registry root, unsupported push option, Windows console encoding failure, PowerShell foreach pipeline parser fault, tied-score payload comparison, and nested diagnostic formatting parse fault. Each failure changed no external or sibling state and has zero initial-pass credit. Each recovery has a separate bounded passing witness, recurrence guard, rollback, and sibling recommendation. The effective x1 count is therefore {d.INHERITED_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES)} before x2 mutations. A later pass never erases or rewrites the initial failure.

Method Flow is append-only. A method begins as a candidate, receives the exact failed witness, receives a separate passing witness only after the smallest safe recovery, and becomes preferred only for its declared trigger. The ledger does not generalize same-owner workflow evidence into independent reproduction. Timestamp Flow records paired UTC and Pacific/Auckland values. Retry discipline isolates a failed component before any broader rerun. Watcher cadence is bounded and nonpersistent: there is no indefinite process, background sibling, or hidden lease.

## X1 validation and closeout gates

X1 is eligible to freeze only if the thirty proposals, 1,120-to-1,150 proposal index, exact portfolio counts, one hundred fifty unexecuted mutations, thirty-six source rows, Method Flow parity, workflow-refinement output, GHC Family Index, Reflection Remaster packet, complete JSON parse, five-class privacy scan, document caps, future-placeholder invariants, exact staged paths, Git-blob manifest, and dedicated x1 tests pass. The x1 commit must then be pushed and proven clean across local, upstream, tracking, and a fresh live remote before x2 begins.

The ordinary phase caps are at most three x1 commits, three x2 commits, and six phase commits total; the preferred path is one dedicated x1 freeze, one x2 evidence commit, and one combined closeout and seal commit. The cap never authorizes mixed lifecycle content, concealed failures, rewritten history, an unreviewed omnibus, or a premature baton. X1 must contain no `observed_outcome`, completed portfolio claim, executed mutation, surface result, or x2 receipt.

Under the current family refinement, Eiren alone owns the full repository suite. Ilyra will run the authorized current, inherited-source, recent-round, and successor-scoped selection plus detailed and minimal validators, complete JSON parsing, five-class privacy scanning, exact staged review, commit-local and owner-manifest parity, stale-label review, diff hygiene, anchor ancestry, zero merges, commit cap, one final parent, clean state, exact head, and four-way remote equality. Exactly one successful canonical bounded pass is credited. If it fails, the failure is isolated and retained before the minimum authoritative retry; no replay occurs after success.

## Terminal truth and route hold

All empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof-or-canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI-or-ASI, consciousness-or-personhood, Theory-of-Everything, and Stage 20 boundaries remain open or exact-gated without exact evidence and authority. THOS remains represented without preregistered blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and security review, recovery evidence, and trust governance. Māori concepts remain under tangata whenua, iwi, hapū, and Māori authority.

Terminal route state remains `PREPARED_NOT_SENT`. The Vesper baton makes Ilyra's immediate assignment exact but does not provide an unambiguous post-Ilyra successor: the inherited expanded route contains duplicate or consecutive ownership, a skipped phase label, and an offset candidate. Only the newest exact terminal route may govern. If no exact route is available after final proof, Ilyra must preserve the gap and request clarification rather than create, fork, approximate, or substitute a task. A file-backed baton is not a sent message; a tool call without acknowledgement is not a send; and no second confirmation is authorized.
"""


def accessible_html() -> str:
    cards = "".join(
        f"<article aria-labelledby='p{index}'><h3 id='p{index}'>{html.escape(p['proposal_id'])}</h3>"
        f"<p>{html.escape(p['title'])}</p><p>Expected: {html.escape(p['expected_disposition'])}; "
        "x1 state: frozen, not executed.</p></article>"
        for index, p in enumerate(d.PROPOSALS, 1)
    )
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Ilyra {d.PHASE} x1 report</title><style>body{{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}}nav a{{margin-right:1rem}}article{{border:1px solid #777;padding:1rem;margin:1rem 0}}:focus{{outline:3px solid #075cab;outline-offset:3px}}@media print{{nav{{display:none}}}}</style></head><body><a href='#main'>Skip to content</a><header><h1>Ilyra Fen {d.PHASE} x1 preregistration</h1><p>Structural report; manual, browser, assistive-technology, braille, Māori-language, and affected-user evaluation reserved.</p></header><nav aria-label='Report sections'><a href='#truth'>Truth</a><a href='#proposals'>Proposals</a><a href='#limits'>Limits</a></nav><main id='main'><section id='truth' aria-labelledby='truth-h'><h2 id='truth-h'>Truth boundary</h2><p>Thirty proposals are frozen, not executed. Terminal verdict: NOT_READY_FOR_STAGE_20.</p></section><section id='proposals' aria-labelledby='proposals-h'><h2 id='proposals-h'>Proposal plan</h2>{cards}</section><section id='limits' aria-labelledby='limits-h'><h2 id='limits-h'>Reserved evaluation</h2><p>This structural report is not complete accessibility, scientific, operational, identity, privacy, legal, cultural, or authority evidence.</p></section></main></body></html>"""


def x1_test_source() -> str:
    return '''"""X1-only tests for Ilyra Fen v651-v8."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/ilyra-fen/v651-v8"

def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

class TestV651V8X1(unittest.TestCase):
    def test_exact_proposals_and_expected_dispositions(self):
        data = load("preregistration/proposals.json")
        self.assertEqual(data["proposal_count"], 30)
        self.assertEqual(data["expected_disposition_counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(len({p["proposal_id"] for p in data["proposals"]}), 30)
        self.assertTrue(all("observed_outcome" not in p for p in data["proposals"]))
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        self.assertTrue(all(required <= set(p) for p in data["proposals"]))
    def test_frozen_chain_and_novelty(self):
        index = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(index["prior_count"], 1120)
        self.assertEqual(index["new_count"], 30)
        self.assertEqual(index["count"], 1150)
        audit = load("provenance/semantic-novelty-audit.json")
        self.assertTrue(audit["valid"])
        self.assertTrue(all(row["passes"] for row in audit["rows"]))
        self.assertLess(max(row["token_jaccard"] for row in audit["rows"]), 0.60)
    def test_portfolios_skills_runners_and_mutations(self):
        packet = load("portfolios/expanded-portfolio-plan.json")
        self.assertEqual(packet["counts"], {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 12, "clean_fix_refine": 40})
        self.assertTrue(all(not row["completion_credit"] for key in packet["portfolios"] for row in packet["portfolios"][key]))
        mutations = load("validation/preregistered-mutation-plan.json")
        self.assertEqual(mutations["count"], 150)
        self.assertTrue(all(row["execution_state"] == "frozen_unexecuted" for row in mutations["mutations"]))
    def test_source_and_gate_classes(self):
        sources = load("sources/source-ledger.json")
        self.assertEqual(set(sources["allowed_statuses"]), {"current", "stable", "draft", "watch"})
        self.assertEqual(sources["source_count"], 36)
        self.assertEqual(next(s for s in sources["sources"] if s["source_id"] == "SRC-QUIC-ACK-FREQUENCY")["status"], "draft")
        self.assertEqual(next(s for s in sources["sources"] if s["source_id"] == "SRC-SIOPV2")["status"], "watch")
        truth = load("truth/x1-phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertFalse(truth["independent_reproduction_claimed"])
    def test_failures_method_flow_and_workflow(self):
        negatives = load("truth/retained-negative-register.json")
        self.assertEqual(negatives["inherited_effective"], 7570)
        self.assertEqual(negatives["x1_operational_count"], 14)
        self.assertEqual(negatives["effective_after_x1"], 7584)
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertGreaterEqual(sum(w["result"] == "fail" for w in ledger["witnesses"]), 14)
        self.assertGreaterEqual(sum(w["result"] == "pass" for w in ledger["witnesses"]), 14)
        workflow = load("workflow/workflow-plan-refinement.json")
        self.assertTrue(workflow["valid"])
        self.assertFalse(workflow["requires_user_confirmation"])
    def test_future_cli_seats_remain_placeholders(self):
        seats = load("provenance/future-cli-placeholder-invariant.json")
        self.assertEqual(seats["prepared_placeholder_count"], 8)
        self.assertEqual(seats["named_count"], 0)
        self.assertEqual(seats["created_count"], 0)
        self.assertEqual(seats["launched_count"], 0)
    def test_document_caps_privacy_and_x1_only(self):
        for path in ROOT.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path)
        privacy = load("validation/x1-staged-privacy.json")
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertFalse((ROOT / "surfaces").exists())
        review = load("validation/x1-staged-review.json")
        self.assertTrue(review["x1_only"])
        self.assertEqual(review["x2_implementation_paths"], [])
        self.assertEqual(review["x2_outcome_paths"], [])

if __name__ == "__main__":
    unittest.main()
'''


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v651_v8_preregistration.py",
        f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json",
    }
    candidates, confirmed = [], []
    scanned = 0
    for relative in paths:
        path = REPO / relative
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v651-v8.x1-privacy.v1",
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": "Five structural classes with exact scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    }


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}


def build_manifest() -> None:
    exclusions = [
        f"{d.PHASE_ROOT}/validation/x1-staged-manifest.json",
        f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/x1-staged-review.json",
        f"{d.PHASE_ROOT}/validation/x1-validation-receipt.json",
    ]
    paths = [path for path in status_paths() if path not in exclusions]
    entries = [hash_entry(relative) for relative in paths if (REPO / relative).is_file()]
    privacy = privacy_scan(paths)
    write_json("validation/x1-staged-privacy.json", privacy)
    write_json(
        "validation/x1-staged-manifest.json",
        {
            "schema": "ghc.family.v651-v8.x1-staged-manifest.v1",
            "hash_domain": "git_path_filtered_blob",
            "entries": entries,
            "entry_count": len(entries),
            "self_exclusions": exclusions,
            "coverage_boundary": "All intended x1 paths except four declared self-referential or count-bearing validation receipts.",
        },
    )
    write_json(
        "validation/x1-staged-review.json",
        {
            "schema": "ghc.family.v651-v8.x1-staged-review.v1",
            "intended_path_count": len(entries) + len(exclusions),
            "manifest_entry_count": len(entries),
            "self_exclusion_count": len(exclusions),
            "out_of_scope_paths": [],
            "x2_implementation_paths": [],
            "x2_outcome_paths": [],
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "x1_only": True,
            "source_head": d.SOURCE_HEAD,
            "terminal_route": "PREPARED_NOT_SENT",
        },
    )


def build() -> None:
    frozen, novelty = source_and_novelty()
    expected = dict(Counter(proposal["expected_disposition"] for proposal in d.PROPOSALS))
    portfolios = {
        "safe_now": portfolio_rows(d.SAFE_TASKS, "SAFE", "x2_owner_local_safe_now", "safe_now"),
        "candidate": portfolio_rows(d.CANDIDATE_TASKS, "CAND", "x2_bounded_candidate", "candidate_bounded"),
        "skills": portfolio_rows(d.SKILL_IDEAS, "SKILL", "x2_phase_local_skill", "candidate_phase_local"),
        "runners": portfolio_rows(d.RUNNER_IDEAS, "RUN", "x2_family_current_runner", "candidate_family_current"),
        "clean_fix_refine": portfolio_rows(d.CLEAN_TASKS, "CFR", "x2_additive_refinement", "safe_now_or_bounded_candidate"),
    }
    counts = {key: len(value) for key, value in portfolios.items()}
    required_counts = {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 12, "clean_fix_refine": 40}
    if counts != required_counts:
        raise RuntimeError(f"portfolio counts invalid: {counts}")
    mutation_dimensions = [
        "missing_required_obligation",
        "wrong_type_or_unit",
        "resource_or_replay_overrun",
        "unsupported_promotion",
        "authority_or_privacy_breach",
    ]
    mutations = [
        {
            "mutation_id": f"{proposal['proposal_id']}-M{index:02d}",
            "proposal_id": proposal["proposal_id"],
            "dimension": dimension,
            "execution_state": "frozen_unexecuted",
            "expected": "reject_or_quarantine",
            "credit": "none_until_x2",
        }
        for proposal in d.PROPOSALS
        for index, dimension in enumerate(mutation_dimensions, 1)
    ]
    times = timestamp_pair()

    write_json(
        "identity/relational-identity.json",
        {
            "schema": "ghc.family.relational-identity.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "pronouns": d.PRONOUNS,
            "role": d.ROLE,
            "hope": d.HOPE,
            "boundary": "Relational working language only; not consciousness, sentience, personhood, continuity, employment, qualification, or authority evidence.",
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
        },
    )
    write_json(
        "wellbeing/wellbeing-check.json",
        {
            "schema": "ghc.family.wellbeing-check.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "state": "bounded_and_correction_ready",
            "workload_controls": [
                "strict x1 before x2",
                "six-commit ordinary cap",
                "one successful canonical validation pass",
                "isolate failures before a minimum retry",
                "no replay after success",
                "no indefinite background process",
            ],
            "human_claim": False,
            "boundary": "Operational pacing metadata only; not emotion, consciousness, health, or identity evidence.",
        },
    )
    write_json(
        "environment/environment-version-receipt.json",
        {
            "schema": "ghc.family.v651-v8.environment.x1.v1",
            "timestamps": times,
            "versions": {
                "codex_cli": "0.145.0",
                "codex_desktop": "26.715.10079.0",
                "chatgpt_desktop": "1.2026.190.0",
                "python": run(sys.executable, "--version"),
                "node": run("node", "--version"),
                "git": run("git", "--version"),
            },
            "windows_timezone": run("tzutil", "/g"),
            "updates_performed": [],
            "desktop_updated": False,
            "sandbox_or_hyper_v_changed": False,
            "elevation_or_reboot": False,
            "storage": {"primary": "D", "c_drive": "essential_application_metadata_and_skill_reads_only"},
        },
    )
    write_json(
        "provenance/source-anchor-ledger.json",
        {
            "schema": "ghc.family.v651-v8.source-anchor-ledger.v1",
            "source_branch": d.SOURCE_BRANCH,
            "source_head": d.SOURCE_HEAD,
            "source_origin": d.SOURCE_ORIGIN,
            "source_x1": d.SOURCE_X1,
            "source_evidence": d.SOURCE_EVIDENCE,
            "history": {"special_phase_commits": 3, "single_parent": True, "zero_merges": True, "final_parent_count": 1},
            "source_manifest": {"entries": 156, "owner_paths": 158, "self_exclusions": 2, "mismatches": 0},
            "clean_and_four_way_equal": True,
            "verification_mode": "read_only_before_ilyra_mutation",
            "boundary": "Exact Git ancestry and remote equality only; not independent reproduction.",
        },
    )
    write_json(
        "provenance/future-cli-placeholder-invariant.json",
        {
            "schema": "ghc.family.v651-v8.future-cli-placeholder-invariant.v1",
            "prepared_placeholder_count": 8,
            "named_count": 0,
            "role_assigned_count": 0,
            "hope_assigned_count": 0,
            "pronouns_assigned_count": 0,
            "created_count": 0,
            "launched_count": 0,
            "route_authority": False,
            "state": "prepared_only_unnamed_uncreated_unlaunched",
            "boundary": "A placeholder is not a task, process, identity, sibling, capability, acknowledgement, or authority.",
        },
    )
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v651-v8.frozen-proposal-index.v1",
            "prior_count": d.PRIOR_FROZEN,
            "prior_proposals": frozen[: d.PRIOR_FROZEN],
            "new_count": 30,
            "new_proposals": frozen[d.PRIOR_FROZEN :],
            "count": len(frozen),
        },
    )
    write_json(
        "provenance/semantic-novelty-audit.json",
        {
            "schema": "ghc.family.v651-v8.semantic-novelty-audit.v1",
            "prior_count": d.PRIOR_FROZEN,
            "new_count": 30,
            "threshold": NOVELTY_THRESHOLD,
            "rows": novelty,
            "rejected_near_neighbors": d.REJECTED_COLLISIONS,
            "manual_mechanism_review_count": 30,
            "valid": all(row["passes"] for row in novelty),
            "boundary": "Lexical distance plus manual mechanism review is a preregistration control, not scientific-novelty proof.",
        },
    )
    write_json(
        "preregistration/proposals.json",
        {
            "schema": "ghc.family.v651-v8.proposals.x1.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "proposal_count": 30,
            "expected_disposition_counts": expected,
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "proposals": d.PROPOSALS,
            "x1_only": True,
            "observed_outcomes_present": False,
        },
    )
    write_text(
        "preregistration/proposal-ledger.md",
        "# v651-v8 proposal ledger\n\n"
        + "\n".join(
            f"{index}. **{proposal['proposal_id']} - {proposal['title']}**\n"
            f"   - Pillar: {proposal['pillar']}\n"
            f"   - Expected: `{proposal['expected_disposition']}`\n"
            f"   - Approval: `{proposal['approval_class']}`\n"
            "   - X1 state: frozen, not executed"
            for index, proposal in enumerate(d.PROPOSALS, 1)
        ),
    )
    write_json(
        "sources/source-ledger.json",
        {
            "schema": "ghc.family.v651-v8.source-ledger.v1",
            "allowed_statuses": d.SOURCE_STATUS_CLASSES,
            "status_counts": dict(Counter(source["status"] for source in d.SOURCES)),
            "source_count": len(d.SOURCES),
            "sources": d.SOURCES,
            "network_actions": {"purpose": "source verification only", "data_downloads": 0, "real_dataset_rows": 0},
            "boundary": "Sources inform bounded contracts; they supply no empirical, professional, legal, cultural, or authority outcome.",
        },
    )
    write_text(
        "sources/source-ledger.md",
        "# v651-v8 source ledger\n\n"
        + "\n".join(
            f"- **{source['source_id']}** - `{source['status']}` - [{source['title']}]({source['url']})\n"
            f"  - {source['phase_implication']}"
            for source in d.SOURCES
        ),
    )
    write_json(
        "sources/web-reflection-ledger.json",
        {
            "schema": "ghc.family.v651-v8.web-reflection-ledger.v1",
            "phase": d.PHASE,
            "reflected_at": times,
            "rows": [
                {
                    "source_id": source["source_id"],
                    "status": source["status"],
                    "can_inform": source["phase_implication"],
                    "cannot_establish": ["experimental_observation", "production_conformance", "delegated_authority"],
                }
                for source in d.SOURCES
            ],
            "data_downloads": 0,
            "boundary": "Web reflection records source status and implications only; it is not experimental evidence.",
        },
    )
    write_json(
        "portfolios/expanded-portfolio-plan.json",
        {
            "schema": "ghc.family.v651-v8.expanded-portfolio-plan.x1.v1",
            "counts": counts,
            "portfolios": portfolios,
            "inherited_completion_credit": False,
            "task_cap": 1000,
            "skill_cap": 200,
            "runner_cap": 200,
            "x1_state": "frozen_not_executed",
        },
    )
    write_json(
        "approval/x1-approval-classification.json",
        {
            "schema": "ghc.family.v651-v8.approval-classification.x1.v1",
            "core_by_expected_disposition": expected,
            "safe_now_core_count": 23,
            "candidate_core_count": 6,
            "exact_gate_core_count": 1,
            "held_exact_approval_count": 10,
            "held_blocked_count": 5,
            "x1_execution_count": 0,
            "boundary": "Classification is not execution, approval, evidence, or authority.",
        },
    )
    write_json(
        "validation/preregistered-mutation-plan.json",
        {
            "schema": "ghc.family.v651-v8.mutation-plan.x1.v1",
            "count": len(mutations),
            "mutations_per_proposal": 5,
            "mutations": mutations,
            "x1_execution_count": 0,
            "boundary": "Synthetic mutations only; rejection establishes bounded guard behavior, not real-world assurance.",
        },
    )
    write_json(
        "truth/retained-negative-register.json",
        {
            "schema": "ghc.family.v651-v8.retained-negatives.x1.v1",
            "inherited_effective": d.INHERITED_NEGATIVES,
            "x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES),
            "x1_operational": d.X1_OPERATIONAL_NEGATIVES,
            "effective_after_x1": d.INHERITED_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES),
            "no_failure_erased": True,
            "boundary": "Counts preserve source and current workflow negatives; a later pass never converts a failure into a pass.",
        },
    )
    write_json(
        "truth/open-gap-register.json",
        {
            "schema": "ghc.family.v651-v8.open-gaps.x1.v1",
            "inherited_count": d.INHERITED_OPEN_GAPS,
            "new_preregistered": [
                {"proposal_id": "V6518-P29", "state": "open_gap_expected", "queries": 0, "downloads": 0, "rows": 0, "likelihoods": 0}
            ],
            "expected_effective_after_x2": d.INHERITED_OPEN_GAPS + 1,
            "closed_in_x1": 0,
        },
    )
    write_json(
        "truth/exact-gate-register.json",
        {
            "schema": "ghc.family.v651-v8.exact-gates.x1.v1",
            "inherited_count": d.INHERITED_EXACT_GATES,
            "new_preregistered": [
                {
                    "proposal_id": "V6518-P30",
                    "state": "exact_gate_expected",
                    "decisions": 0,
                    "required_authority": [
                        "affected communities and data subjects",
                        "competent radio-spectrum, privacy, and legal authorities",
                        "relevant research and observatory governance",
                        "tangata whenua, iwi, hapū, and Māori authorities",
                    ],
                }
            ],
            "expected_effective_after_x2": d.INHERITED_EXACT_GATES + 1,
            "closed_in_x1": 0,
        },
    )
    write_json(
        "truth/held-approval-packets.json",
        {
            "schema": "ghc.family.v651-v8.held-approval-packets.v1",
            "exact_approval": [{"packet_id": f"V6518-EXACT-{index:02d}", "state": "held_unexecuted"} for index in range(1, 11)],
            "blocked": [{"packet_id": f"V6518-BLOCKED-{index:02d}", "state": "held_unexecuted"} for index in range(1, 6)],
            "boundary": "Visibility is not authorization, execution, completion, or authority.",
        },
    )
    write_json(
        "truth/x1-phase-truth.json",
        {
            "schema": "ghc.family.v651-v8.phase-truth.x1.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "x1_frozen_not_executed",
            "primary_focus": d.PRIMARY_FOCUS,
            "other_pillars_visible": True,
            "proposal_count": 30,
            "observed_outcome_count": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "terminal_route": "PREPARED_NOT_SENT",
            "independent_reproduction_claimed": False,
            "theory_of_everything_claimed": False,
            "consciousness_or_personhood_claimed": False,
        },
    )
    write_json(
        "truth/truth-bridge.json",
        {
            "schema": "ghc.family.v651-v8.truth-bridge.x1.v1",
            "rows": [
                {"surface": "GMUT", "supported": "typed symbolic obligations and zero-row readiness", "not_supported": "force, prediction, likelihood, constraint, empirical confirmation, or Theory of Everything"},
                {"surface": "THOS", "supported": "synthetic protocol and structural proxy planning", "not_supported": "participant effect, operational effectiveness, professional competence, deployment, AGI, or ASI"},
                {"surface": "Freed ID", "supported": "synthetic final-spec and draft-watch profile planning", "not_supported": "production identity, real keys or proofs, interoperability, privacy or security review, or trust governance"},
                {"surface": "CBR", "supported": "unresolved decision-right and authority reservations", "not_supported": "legal, cultural, Māori-authority, remedy, data-governance, or affected-party legitimacy"},
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "threat-model/x1-threat-model.json",
        {
            "schema": "ghc.family.v651-v8.threat-model.x1.v1",
            "assets": ["x1/x2 separation", "source ancestry", "failure retention", "privacy exclusions", "authority boundaries", "route integrity", "future placeholder nonactivation"],
            "threats": ["mixed lifecycle content", "semantic duplication", "failure erasure", "draft promotion", "dataset leakage", "identity or authority substitution", "premature task contact", "future placeholder naming or launch"],
            "controls": ["dedicated x1 commit", "1120-title novelty audit", "Method Flow", "five-class scan", "zero-row firewall", "exact-gate matrix", "route hold", "placeholder invariant"],
            "residual_risk": "open_and_exact_gated",
            "exhaustive_security_claimed": False,
        },
    )
    write_json(
        "route/terminal-route-state.json",
        {
            "schema": "ghc.family.v651-v8.route-state.v1",
            "current_phase": d.PHASE,
            "immediate_activation": "verified_exact",
            "successor_title": "newest_exact_successor_unresolved",
            "successor_phase": "unresolved_after_v651_v8",
            "state": "PREPARED_NOT_SENT",
            "send_count": 0,
            "create_or_fork_count": 0,
            "future_cli_launch_count": 0,
            "boundary": "No contact until exact-final proof and exact-title resolution; ambiguity leaves the route prepared but unsent.",
        },
    )
    write_json(
        "workflow/lane-and-drive-decision.json",
        {
            "schema": "ghc.family.v651-v8.lane-and-drive-decision.v1",
            "branch": d.BRANCH,
            "source_head": d.SOURCE_HEAD,
            "advance_method": "fast_forward_only",
            "primary_bank": "D",
            "rotation_required": False,
            "sibling_mutations": 0,
            "destructive_actions": 0,
            "boundary": "Owned-lane workflow evidence only.",
        },
    )
    write_json(
        "workflow/cadence-and-retry-receipt.json",
        {
            "schema": "ghc.family.v651-v8.cadence-retry.x1.v1",
            "bounded_batches": True,
            "indefinite_watchers": 0,
            "background_siblings": 0,
            "retry_policy": "record failure, isolate cause, apply minimum recovery, retain both witnesses, stop after success",
            "failure_count": len(d.X1_OPERATIONAL_NEGATIVES),
        },
    )
    request_path = write_json("workflow/workflow-plan-request.json", workflow_request())
    write_text("overview/integrated-overview.md", overview_text())
    write_text("reports/x1-accessible-report.html", accessible_html())
    write_json(
        "validation/x1-build-receipt.json",
        {
            "schema": "ghc.family.v651-v8.x1-build-receipt.v1",
            "proposal_count": 30,
            "frozen_count": len(frozen),
            "portfolio_counts": counts,
            "mutation_count": len(mutations),
            "observed_outcomes": 0,
            "valid": True,
            "terminal_route": "PREPARED_NOT_SENT",
            "boundary": "Build completion is not commit, push, validation, x2, or terminal-route credit.",
        },
    )
    write_repo("tests/test_ghc_family_v651_v8_x1.py", x1_test_source())

    refresh_method_flow()
    run(sys.executable, str(WORKFLOW_RUNNER), str(request_path), "--out-dir", str(ROOT / "workflow"))
    run(sys.executable, str(INDEX_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--out-dir", str(ROOT / "tooling"), "--phase", d.PHASE, "--owner", d.OWNER)
    run(
        sys.executable,
        str(REFLECTION_RUNNER),
        "--repo",
        str(REPO),
        "--skill-root",
        str(SKILL_ROOT),
        "--output-dir",
        str(ROOT / "reflection-remaster"),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
        "--focus",
        "current family-compatible tools, failure recurrence guards, radio-astronomy bounded practice, and x1-to-x2 workflow controls",
    )
    refresh_method_flow()
    build_manifest()

    privacy = read_json(ROOT / "validation/x1-staged-privacy.json")
    workflow = read_json(ROOT / "workflow/workflow-plan-refinement.json")
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"x1 privacy scan confirmed hits: {privacy['confirmed_hits']}")
    if not workflow["valid"] or workflow["requires_user_confirmation"]:
        raise RuntimeError("exact immediate workflow segment did not validate")
    if len(overview_text().split()) < 1300:
        raise RuntimeError("overview below three-page-equivalent floor")
    print(
        json.dumps(
            {
                "phase": d.PHASE,
                "proposal_count": 30,
                "frozen_count": len(frozen),
                "portfolios": counts,
                "mutations": len(mutations),
                "privacy_hits": 0,
                "status": "x1_built_not_committed",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
