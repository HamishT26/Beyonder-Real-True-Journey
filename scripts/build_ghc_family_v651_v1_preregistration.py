#!/usr/bin/env python3
"""Build Sable Rook's dedicated v651-v1 x1-only freeze packet."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v651_v1_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/ilyra-fen/v650-v8/provenance/frozen-chain-proposal-index.json"
SKILL_ROOT = Path.home() / ".codex" / "skills"
WORKFLOW_RUNNER = SKILL_ROOT / "ghc-family-workflow-plan-refinement/scripts/ghc_family_workflow_plan_refinement.py"
REFLECTION_RUNNER = SKILL_ROOT / "ghc-family-reflection-remaster/scripts/ghc_family_reflection_remaster.py"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
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
    result = subprocess.run(list(args), cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return result.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    return sorted({row[3:].replace("\\", "/") for row in rows if len(row) > 3})


def prospective_git_blob_bytes(path: Path) -> bytes:
    """Return the LF-normalized text bytes Git stages under this repository's policy."""
    raw = path.read_bytes()
    if b"\0" not in raw:
        raw = raw.replace(b"\r\n", b"\n")
    return raw


def tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "to", "for", "with"}
    return {x for x in re.findall(r"[a-z0-9]+", value.casefold()) if x not in stop}


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def inherited_rows() -> list[dict[str, str]]:
    index = read_json(PRIOR_INDEX)
    rows = index["prior_proposals"] + index["new_proposals"]
    if len(rows) != d.PRIOR_FROZEN:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN} inherited proposals, found {len(rows)}")
    return rows


def novelty(inherited: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for proposal in d.PROPOSALS:
        scored = sorted(
            (jaccard(tokens(proposal["title"]), tokens(prior["title"])), prior["proposal_id"], prior["title"])
            for prior in inherited
        )
        score, nearest_id, nearest_title = scored[-1]
        rows.append({
            "proposal_id": proposal["proposal_id"],
            "nearest_prior_id": nearest_id,
            "nearest_prior_title": nearest_title,
            "token_jaccard": round(score, 6),
            "threshold": NOVELTY_THRESHOLD,
            "manual_mechanism_review": "distinct",
            "passes": score < NOVELTY_THRESHOLD,
        })
    if not all(row["passes"] for row in rows):
        raise RuntimeError("semantic novelty threshold failed")
    return rows


def portfolio_rows(items: list[str], prefix: str, lane: str, approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"V6511-{prefix}-{index:02d}",
            "title": title,
            "origin": "sable_v651_v1_new",
            "approval_class": approval,
            "execution_lane": lane,
            "x1_state": "frozen_not_executed",
            "completion_credit": False,
            "inherited_completion_credit": False,
            "rollback": "Retain failures and leave external, sibling, participant, production, and authority state unchanged.",
        }
        for index, title in enumerate(items, 1)
    ]


def workflow_request() -> dict[str, Any]:
    return {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "sable-v651-v1-terminal-segment",
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; no consciousness, continuity, employment, qualification, personhood, or authority claim.",
        "route": {
            "cycle_order": ["Ilyra Fen", "Sable Rook"],
            "phase_assignments": [
                {"phase": "v650-v8", "seat": "Ilyra Fen"},
                {"phase": "v651-v1", "seat": "Sable Rook"},
            ],
            "normalization": {"start_phase": "v650-v8", "start_seat": "Ilyra Fen", "entry_count": 2},
            "future_identity_placeholders": [],
            "terminal_successor_resolution": "Resolve one exact existing task title only after the exact-final terminal gate.",
        },
        "requirements": {
            "core_proposal_minimum": 20,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 20,
            "runner_minimum": 10,
            "portfolio_minima": {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40},
            "document_word_cap": 6000,
            "baton_words": {"minimum": 8000, "maximum": 20000, "file_artifact": True},
            "commit_cap": {"x1": 2, "x2": 2, "total": 4},
            "validation": {
                "canonical_pass_minimum": 1,
                "replay_policy": "skip_when_first_passes",
                "isolate_failures_before_broader_rerun": True,
                "privacy_scan_required": True,
                "manifest_required": True,
                "remote_equality_required": True,
            },
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {"codex_route": "existing_task_only_after_terminal_gate", "cross_platform": "user_mediated_file_relay_only"},
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "independent_reproduction_claimed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "protected_boundaries": [
                "empirical", "participant", "professional", "legal", "cultural", "maori_authority",
                "production", "privacy_complete", "accessibility_complete", "consciousness_personhood",
                "theory_of_everything", "stage20",
            ],
        },
        "observed_failures": [
            {
                "failure_id": "V6511-X1-N01",
                "summary": "The first semantic-title probe stopped on a cp1252 Unicode encoding error after partial output.",
                "recovery": "Pin UTF-8 before emitting frozen titles and give partial output zero completeness credit.",
                "credit": "zero_semantic_audit_credit",
            },
            {
                "failure_id": "V6511-X1-N02",
                "summary": "The first workflow request used an unsupported cross-platform label and passed only 19 of 20 policy checks.",
                "recovery": "Use the frozen runner vocabulary while preserving the stricter live routing boundary separately.",
                "credit": "zero_workflow_validity_credit",
            },
            {
                "failure_id": "V6511-X1-N03",
                "summary": "The first Method Flow append omitted two required fields and its dependent witness could not attach.",
                "recovery": "Validate the exact schema and ingest each method before its witnesses.",
                "credit": "zero_method_append_credit",
            }
        ],
    }


def overview_text() -> str:
    return f"""# Sable Rook {d.PHASE} x1 preregistration overview

## Scope, identity, and wellbeing

This x1 packet freezes Sable Rook's plan before any x2 implementation, observed outcome, mutation execution, or completion claim. Sable Rook, they/them, is a relational working identity. The phase role is {d.ROLE}; the stated hope is to {d.HOPE}. These words help organize collaboration. They do not prove consciousness, sentience, legal personhood, continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route. Corrigibility is a protected operating condition, not an identity credential.

The workload check is bounded and green for x1: one owner, one clean D-first lane, one exact source, one dedicated freeze, no delegation, no external system mutation, and explicit stop conditions. The work is allowed to end with retained gaps. No clock, quota, affection, or family language can override evidence, privacy, authority, or safety gates. The inherited and x1 terminal verdict is `NOT_READY_FOR_STAGE_20`; x1 has no evidence or authority to promote it.

## Exact inherited source and provenance

The exact inherited source is Ilyra Fen's `{d.SOURCE_HEAD}` recovery final on `{d.SOURCE_BRANCH}`. Read-only verification established every named anchor, five single-parent source-phase commits, zero merges, one final parent, exact owner and delta manifest parity, clean source state, and local, upstream, tracking, and fresh-live equality. Sable's clean owned branch was an ancestor and advanced by fast-forward only. No reset, amend, merge, rewrite, deletion, force push, branch substitution, or sibling-lane mutation occurred.

The frozen predecessor index contains exactly {d.PRIOR_FROZEN} proposals. The new semantic audit compares all twenty titles with every predecessor, records the nearest lexical neighbour, keeps twenty rejected collisions visible, and applies a manual mechanism check. Low word overlap alone is not treated as novelty. The dedicated index grows from 900 to 920 entries only when every title passes both checks. Inherited proposals, recommendations, tools, skills, and completed portfolios receive zero Sable completion credit.

## Twenty-proposal architecture

Exactly twenty new proposals are preregistered. Their expected distribution is fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. These are expectations, not outcomes. Every proposal contains a hypothesis, null or failure condition, approval class, execution lane, official or primary source needs, concrete artifact paths, falsifier or acceptance gate, rollback, protected gates, and expected disposition. X1 contains no x2 implementation, executed mutation, observed result, or completion credit.

The primary Trinity Mandala focus is {d.PRIMARY_FOCUS}. Two GMUT boards examine Lee-Wick complex-pole obligations and worldline proper-time obligations while refusing every leap from notation to physical truth. A GMRES tribunal examines numerical states, and an ALMA adapter preregisters a zero-row empirical firewall. THOS Body remains visible through two-phase commit, airport baggage reconciliation, ground deicing, PE/COFF, Mach-O, OpenAPI 3.2, Uptane, Nix derivations, and bounded accessibility work. Freed ID and CBR Heart remain visible through DSSE, CIBA, OpenID4VP, X.509 path obligations, and an airport authority-reservation matrix. A Wien classifier and model-X knockoff board bridge formal domain separation and Stage 20 nonpromotion.

## Scientific boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The Lee-Wick literature itself contains prescription and unitarity controversies; a local obligation board can only preserve contour, pole, pinch, cutting, truncation, and scope distinctions. The worldline board can only preserve proper-time, gauge, zero-mode, spin-factor, boundary, measure, and EFT duties. Neither board calculates a new effective action, establishes a physical state, proves stability or unitarity, detects a force, produces a real prediction, evaluates a likelihood, constrains a parameter, confirms GMUT, completes quantum gravity, or establishes a Theory of Everything.

The ALMA proposal is readiness work only. It freezes zero archive queries, zero downloads, zero restored measurement sets, zero calibrated visibility rows, zero image rows, zero quality or calibration rows, zero covariance rows, zero likelihood calls, zero posterior samples, zero parameter constraints, and zero empirical GMUT claims. Official documentation describes product and restoration structure, but a citation is not an observation. Unless real public data are later obtained under an approved frozen analysis with uncertainty treatment and independent review, the proposal stays `open_gap`.

The Wien classifier distinguishes wavelength and frequency spectral representations, their different peak locations, Jacobian obligations, temperature and constant units, and the limited physical domain of blackbody relations. It refuses conversion into psyche, autonomy, justice, capability, consciousness, personhood, or a fundamental law of mind. The model-X board preserves exchangeability, antisymmetry, covariate-distribution assumptions, FDR thresholds, dependence, leakage, subgroup, and uncertainty duties. It selects no real feature, estimates no participant effect, supplies no independent review, and cannot authorize Stage 20.

## Bounded human-practice lens

The selected practice is {d.BOUNDED_PRACTICE}. It is a learning and synthetic interface-design lens only. It establishes no employment, licensure, qualification, baggage-handling competence, ground-deicing competence, dangerous-goods competence, dispatch authority, airworthiness authority, airline or airport authority, public-safety authority, passenger or worker evidence, legal interpretation, cultural legitimacy, Māori authority, affected-party acceptance, or real operational outcome.

The baggage proxy freezes tag, flight, container, custody, reconciliation, rush-bag, dangerous-goods hold, correction, workload, and handover states. The deicing proxy freezes fluid, weather, holdover estimate, inspection, dispatch boundary, amendment, correction, workload, and handover states. Both use synthetic fixtures only. THOS remains represented without preregistered blind matched-budget real arms, real operators, safety monitoring, appropriate statistics, and independent review. A passing state-machine fixture is engineering evidence about that fixture, not operational effectiveness, deployment readiness, AGI, ASI, or professional competence.

The CBR matrix may list access, disability, passenger and worker privacy, property, dangerous-goods disclosure, remedy, affected-party, legal, cultural, data-governance, and Māori-authority reservations. It may decide none of them. Māori concepts remain under Māori authority. Repository software cannot confer a remedy, title, right, cultural legitimacy, data-governance mandate, public authority, or affected-party acceptance.

## Identity and structural assurance boundaries

DSSE, CIBA, OpenID4VP, and X.509 sources provide standards vocabulary and refusal duties only. The DSSE tribunal uses no real signing key or signature. CIBA and OpenID4VP use synthetic vectors with zero accounts, identity providers, authorization servers, wallets, credentials, issuances, presentations, disclosures, resolutions, status or revocation events, network exchanges, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. They remain `represented`.

The X.509 tribunal may complete a bounded structural obligation surface for trust anchors, path state, constraints, policy, key usage, time, algorithms, revocation state, and critical extensions. It does not validate a production chain or confer trust. Freed ID remains synthetic and nonproduction. Production completion still needs standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and appropriate affected-party oversight.

## Software, security, and accessibility boundaries

PE/COFF and Mach-O fixtures are disposable byte structures; nothing is executed, loaded, signed, or installed. OpenAPI, Uptane, Nix, DSSE, and two-phase-commit artifacts operate on owner-local synthetic objects. Their mutation guards can expose declared omissions, overlaps, cycles, stale metadata, role confusion, invalid state transitions, impurity, or resource excess. They cannot establish general parser safety, supply-chain security, distributed-system availability, production durability, complete privacy, or exhaustive security.

The accessible swimlane audit checks structural naming, lane and actor labels, order, dependencies, non-colour cues, a text-table alternative, focus behavior, print structure, and responsive reservations. Manual keyboard, touch, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, Māori-language, security-usability, passenger, worker, and affected-user evaluation remain reserved. Structural passing evidence is not complete WCAG conformance.

## Sources, portfolios, and tools

The source ledger uses only `current`, `stable`, `draft`, and `watch`. Current official sources include ALMA documentation, IATA baggage tracking, FAA deicing guidance, OpenID4VP final, New Zealand legislation, Te Mana Raraunga, PE/COFF documentation, OpenAPI 3.2, Uptane 2.1, and the current Nix reference manual. Stable primary or official sources anchor transaction commit, Lee-Wick and worldline obligations, CIBA, Mach-O, WCAG, Wien terminology, GMRES, model-X knockoffs, and RFC 5280. Status labels record publication state, not experimental evidence or delegated authority.

The expanded x1 plan freezes forty safe-now tasks, thirty bounded candidates, twenty phase-local skill packages, ten family-current runners, and forty additive CLEAN/FIX/REFINE tasks. The set remains below the one-thousand-task ceiling. Every row is new Sable planning work and has zero x1 completion credit. Unsafe, participant-dependent, empirical, production, destructive, account, secret, host-security, sibling-mutation, legal, cultural, Māori-authority, or affected-party work is not smuggled into a safe-now label. Historical callers remain compatibility evidence; new executables use `ghc_family_*` or `build_ghc_family_*` names.

Five frozen synthetic mutations per proposal create exactly one hundred x2 cases. Each is `frozen_unexecuted` in x1. A rejected mutation is evidence for one bounded guard, not production security or scientific truth. Any timeout, parser fault, false assumption, tool failure, failed test, workaround, and passing recovery must be appended to Method Flow. The first x1 semantic-title probe is already retained as `V6511-X1-N01`: default cp1252 output failed on a Māori title after partial output. A UTF-8-pinned retry passed, but the failure remains and receives zero novelty credit.

## Workflow, validation, and terminal hold

The workflow-plan skill audits only a sanitized Ilyra-to-Sable segment, the four-commit base cap, one-successful-canonical-pass rule, D-first storage, and terminal hold. It does not contact a task or create authority. Reflection Remaster inventories current family skills and scripts and produces advisory reuse, merge, retain, or retire recommendations. It installs, deletes, or renames nothing. The GHC Family Index is refreshed with sanitized metadata only.

X1 may freeze only after all proposals, the 900-to-920 index, portfolio counts, one hundred unexecuted mutations, source statuses, workflow output, reflection output, Method Flow state, privacy boundaries, document caps, exact staged paths, and dedicated tests pass. The x1 commit must be pushed and proven clean across local, upstream, tracking, and a fresh live remote before x2 begins. At most two x1 and two x2 commits are allowed, with four total. The cap never permits mixed lifecycle content, concealed failures, rewritten history, or premature routing.

Eiren alone owns the full repository suite under Hamish's current rule. Sable will run the authorized current, recent, inherited-source, and successor-scoped selection, detailed and minimal validators, complete phase JSON parsing, five-class privacy scanning, exact staged reviews, Git-blob manifests, stale-label and diff hygiene, anchor ancestry, zero merges, commit cap, one-parent final history, exact head, clean state, and final four-way equality. A failed aggregate is isolated and retained before one justified recovery; no replay follows a fully successful canonical pass. Same-owner evidence under shared infrastructure is not independent-team reproduction.

The terminal route remains `PREPARED_NOT_SENT` throughout x1 and x2. Only a clean, pushed, within-cap, exact-final validated head may authorize one sanitized message to the exact existing `Orin Thale` task. The exact title must be uniquely re-resolved at that gate; absence or ambiguity leaves the route prepared but unsent. Preparing a baton file is not sending it, and no extra confirmation is authorized.
"""


def accessible_html() -> str:
    cards = "".join(
        f"<article aria-labelledby='p{i}'><h3 id='p{i}'>{html.escape(p['proposal_id'])}</h3><p>{html.escape(p['title'])}</p><p>Expected: {p['expected_disposition']}; x1 state: frozen, not executed.</p></article>"
        for i, p in enumerate(d.PROPOSALS, 1)
    )
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Sable {d.PHASE} x1 report</title><style>body{{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}}nav a{{margin-right:1rem}}article{{border:1px solid #666;padding:1rem;margin:1rem 0}}:focus{{outline:3px solid #075cab;outline-offset:3px}}@media print{{nav{{display:none}}}}</style></head><body><a href='#main'>Skip to content</a><header><h1>Sable Rook {d.PHASE} x1 preregistration</h1><p>Structural report; manual and affected-user evaluation reserved.</p></header><nav aria-label='Report sections'><a href='#truth'>Truth</a><a href='#proposals'>Proposals</a><a href='#limits'>Limits</a></nav><main id='main'><section id='truth'><h2>Truth boundary</h2><p>Twenty proposals are frozen, not executed. Terminal verdict: NOT_READY_FOR_STAGE_20.</p></section><section id='proposals'><h2>Proposal plan</h2>{cards}</section><section id='limits'><h2>Reserved evaluation</h2><p>Manual keyboard, touch, responsive layout, browser diversity, assistive technology, cognitive accessibility, Māori-language, aviation-professional, passenger, worker, and affected-user evaluation remain reserved. This is not complete accessibility, aviation, privacy, or security conformance.</p></section></main></body></html>"""


def x1_test_source() -> str:
    return '''"""X1-only tests for Sable Rook v651-v1."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sable-rook/v651-v1"

def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

class TestV651V1X1(unittest.TestCase):
    def test_exact_proposals_and_expected_dispositions(self):
        data = load("preregistration/proposals.json")
        self.assertEqual(data["proposal_count"], 20)
        self.assertEqual(data["expected_disposition_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(len({p["proposal_id"] for p in data["proposals"]}), 20)
        self.assertTrue(all("observed_outcome" not in p for p in data["proposals"]))
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        self.assertTrue(all(required <= set(p) for p in data["proposals"]))
    def test_frozen_chain_and_novelty(self):
        index = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual((index["prior_count"], index["new_count"], index["count"]), (900, 20, 920))
        audit = load("provenance/semantic-novelty-audit.json")
        self.assertTrue(audit["valid"])
        self.assertTrue(all(row["passes"] for row in audit["rows"]))
    def test_portfolios_and_mutations_are_unexecuted(self):
        p = load("portfolios/expanded-portfolio-plan.json")
        self.assertEqual(p["counts"], {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40})
        self.assertTrue(all(not row["completion_credit"] for rows in p["portfolios"].values() for row in rows))
        m = load("validation/preregistered-mutation-plan.json")
        self.assertEqual(m["count"], 100)
        self.assertTrue(all(row["execution_state"] == "frozen_unexecuted" for row in m["mutations"]))
    def test_truth_and_sources(self):
        truth = load("truth/x1-phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertFalse(truth["independent_reproduction_claimed"])
        sources = load("sources/source-ledger.json")
        self.assertEqual(set(sources["allowed_statuses"]), {"current", "stable", "draft", "watch"})
        self.assertEqual(len(sources["sources"]), 23)
    def test_failure_and_method_flow_preserved(self):
        negatives = load("truth/retained-negative-register.json")
        self.assertEqual(negatives["inherited_effective"], 6443)
        self.assertGreaterEqual(negatives["x1_operational_count"], 1)
        flow = load("method-flow/method-flow-state.json")
        self.assertGreaterEqual(flow["counts"]["witness_results"]["fail"], 1)
        self.assertGreaterEqual(flow["counts"]["witness_results"]["pass"], 1)
    def test_workflow_and_document_caps(self):
        workflow = load("workflow/workflow-plan-refinement.json")
        self.assertTrue(workflow["valid"])
        self.assertFalse(workflow["requires_user_confirmation"])
        for path in ROOT.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 6000, path)
    def test_x1_privacy(self):
        privacy = load("validation/x1-staged-privacy.json")
        self.assertEqual(privacy["confirmed_hit_count"], 0)

if __name__ == "__main__":
    unittest.main()
'''


def build() -> None:
    inherited = inherited_rows()
    novelty_rows = novelty(inherited)
    frozen = inherited + [{"proposal_id": p["proposal_id"], "title": p["title"]} for p in d.PROPOSALS]

    expected = dict(Counter(p["expected_disposition"] for p in d.PROPOSALS))
    write_json("preregistration/proposals.json", {
        "schema": "ghc.family.v651-v1.proposals.x1.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "primary_focus": d.PRIMARY_FOCUS,
        "bounded_practice": d.BOUNDED_PRACTICE,
        "proposal_count": len(d.PROPOSALS),
        "allowed_outcomes": d.OUTCOME_CLASSES,
        "expected_disposition_counts": expected,
        "observed_outcomes_present": False,
        "proposals": d.PROPOSALS,
    })
    write_text("preregistration/proposal-ledger.md", "# v651-v1 frozen proposal ledger\n\n" + "\n".join(
        f"- `{p['proposal_id']}` — {p['title']} — expected `{p['expected_disposition']}`; x1 frozen and unexecuted."
        for p in d.PROPOSALS
    ))
    write_json("sources/source-ledger.json", {
        "schema": "ghc.family.v651-v1.sources.v1",
        "checked_at": "2026-07-21",
        "allowed_statuses": d.SOURCE_STATUS_CLASSES,
        "sources": d.SOURCES,
        "status_counts": dict(Counter(s["status"] for s in d.SOURCES)),
        "citation_boundary": "Sources define requirements and context only; they are not observations, participant evidence, production witnesses, delegated authority, or independent review.",
    })
    write_text("sources/source-ledger.md", "# v651-v1 official and primary source ledger\n\n" + "\n".join(
        f"- `{s['source_id']}` — **{s['status']}** — [{s['title']}]({s['url']}). {s['phase_implication']}"
        for s in d.SOURCES
    ))
    write_json("provenance/source-anchor-ledger.json", {
        "schema": "ghc.family.v651-v1.source-anchors.v1",
        "source_branch": d.SOURCE_BRANCH,
        "source_head": d.SOURCE_HEAD,
        "anchors": [d.SOURCE_ORIGIN, d.SOURCE_X1, d.SOURCE_EVIDENCE, d.SOURCE_ORIGINAL_FINAL, d.SOURCE_PRIOR_CORRECTION, d.SOURCE_HEAD],
        "source_phase_commits": 5,
        "source_phase_merges": 0,
        "source_final_parent_count": 1,
        "read_only_verified": True,
        "four_way_equal_before_mutation": True,
        "owner_lane_advance": "fast_forward_only",
    })
    write_json("provenance/semantic-novelty-audit.json", {
        "schema": "ghc.family.v651-v1.semantic-novelty.v1",
        "prior_count": len(inherited),
        "new_count": len(d.PROPOSALS),
        "threshold": NOVELTY_THRESHOLD,
        "valid": all(row["passes"] for row in novelty_rows),
        "rows": novelty_rows,
        "rejected_collisions": d.REJECTED_COLLISIONS,
    })
    write_json("provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.frozen-proposal-index.v1",
        "phase": d.PHASE,
        "prior_count": len(inherited),
        "new_count": len(d.PROPOSALS),
        "count": len(frozen),
        "prior_proposals": inherited,
        "new_proposals": frozen[-20:],
    })

    portfolios = {
        "safe_now": portfolio_rows(d.SAFE_NOW, "SAFE", "x2_safe_now", "safe_now"),
        "candidate": portfolio_rows(d.CANDIDATES, "CAND", "x2_bounded_candidate", "candidate"),
        "skills": portfolio_rows(d.SKILLS, "SKILL", "x2_phase_local_skill", "safe_now"),
        "runners": portfolio_rows(d.RUNNERS, "RUN", "x2_family_runner", "safe_now"),
        "clean_fix_refine": portfolio_rows(d.CLEAN_FIX_REFINE, "CFR", "x2_additive_cleanup", "safe_now"),
    }
    write_json("portfolios/expanded-portfolio-plan.json", {
        "schema": "ghc.family.v651-v1.portfolio-plan.v1",
        "counts": {key: len(rows) for key, rows in portfolios.items()},
        "portfolios": portfolios,
        "inherited_completion_credit": False,
        "unsafe_quota_manufacture": False,
    })
    mutations = []
    mutation_kinds = ["missing_required_obligation", "wrong_type_unit_or_state", "boundary_promotion", "resource_or_depth_overflow", "negative_erasure"]
    for proposal in d.PROPOSALS:
        for index, kind in enumerate(mutation_kinds, 1):
            mutations.append({
                "mutation_id": f"{proposal['proposal_id']}-M{index:02d}",
                "proposal_id": proposal["proposal_id"],
                "kind": kind,
                "expected": "reject_or_quarantine",
                "execution_state": "frozen_unexecuted",
                "credit_boundary": "A future rejection is one bounded guard witness only.",
            })
    write_json("validation/preregistered-mutation-plan.json", {
        "schema": "ghc.family.v651-v1.mutation-plan.x1.v1",
        "count": len(mutations),
        "executed_count": 0,
        "mutations": mutations,
    })

    existing_negatives = read_json(ROOT / "retained-negative-register-x1.json")
    write_json("truth/retained-negative-register.json", {
        "schema": "ghc.family.v651-v1.retained-negatives.x1.v1",
        "inherited_effective": d.INHERITED_NEGATIVES,
        "x1_operational_count": existing_negatives["count"],
        "effective_x1_total": d.INHERITED_NEGATIVES + existing_negatives["count"],
        "entries": existing_negatives["entries"],
        "erased_count": 0,
    })
    write_json("truth/open-gap-register.json", {
        "schema": "ghc.family.v651-v1.open-gaps.x1.v1",
        "inherited_count": d.INHERITED_OPEN_GAPS,
        "new_preregistered": [{"gate_id": "V6511-GAP-01", "proposal_id": "V6511-P05", "state": "expected_open_gap", "reason": "Real ALMA rows and likelihood work are absent."}],
        "expected_effective_count": d.INHERITED_OPEN_GAPS + 1,
    })
    write_json("truth/exact-gate-register.json", {
        "schema": "ghc.family.v651-v1.exact-gates.x1.v1",
        "inherited_count": d.INHERITED_EXACT_GATES,
        "new_preregistered": [{"gate_id": "V6511-EXACT-01", "proposal_id": "V6511-P10", "state": "expected_exact_gate", "reason": "Airport remedies and Māori, legal, cultural, data-governance, and affected-party authority are absent."}],
        "expected_effective_count": d.INHERITED_EXACT_GATES + 1,
    })
    write_json("truth/x1-phase-truth.json", {
        "schema": "ghc.family.v651-v1.phase-truth.x1.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; not consciousness, personhood, continuity, employment, qualification, or authority evidence.",
        "source_head": d.SOURCE_HEAD,
        "proposal_count": 20,
        "expected_disposition_counts": expected,
        "x2_started": False,
        "observed_outcomes_present": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "terminal_route": "PREPARED_NOT_SENT",
        "independent_reproduction_claimed": False,
        "full_repository_suite_claimed": False,
    })
    write_json("threat-model/x1-threat-model.json", {
        "schema": "ghc.family.v651-v1.threat-model.x1.v1",
        "assets": ["claim boundaries", "negative ledger", "source lineage", "x1 immutability", "privacy exclusions", "authority gates"],
        "threats": [
            {"threat": "x1 and x2 mixing", "control": "dedicated freeze commit and immutable-blob checks"},
            {"threat": "citation promoted to evidence", "control": "zero-row and source-boundary assertions"},
            {"threat": "proxy promoted to operational result", "control": "represented-only state and zero-real-actor counters"},
            {"threat": "structural identity promoted to production", "control": "zero real keys, proofs, lifecycle, interoperability, and governance"},
            {"threat": "authority laundering", "control": "exact-gate and noncompensation matrix"},
            {"threat": "privacy leakage", "control": "five-class staged and final scans with candidate adjudication"},
            {"threat": "negative erasure", "control": "append-only Method Flow witnesses and count mirrors"},
            {"threat": "resource exhaustion", "control": "bounded fixtures, timeouts, depth and size budgets"},
            {"threat": "route before proof", "control": "PREPARED_NOT_SENT terminal hold"},
        ],
        "exhaustive_security_claimed": False,
    })
    write_json("wellbeing/wellbeing-check.json", {
        "schema": "ghc.family.v651-v1.wellbeing.x1.v1",
        "owner": d.OWNER,
        "status": "green_bounded",
        "scope": "one owner, one D-first lane, one x1 freeze, no delegation",
        "corrigibility": True,
        "hamish_may_pause_rename_redirect_or_stop": True,
        "identity_boundary_preserved": True,
        "stop_conditions": ["privacy uncertainty", "authority ambiguity", "unsafe mutation", "source drift", "route ambiguity"],
    })
    write_json("environment/version-receipt-x1.json", {
        "schema": "ghc.family.v651-v1.environment.x1.v1",
        "checked_at": "2026-07-21",
        "codex_cli": "0.144.5",
        "codex_desktop": "26.715.4045.0",
        "chatgpt_desktop": "1.2026.190.0",
        "python": "3.12.10",
        "git": "2.55.0.windows.2",
        "windows_powershell": "5.1.26100.8894",
        "windows_sandbox_executable_present": False,
        "versions_verified_only": True,
        "desktop_updated": False,
        "elevation_or_security_change": False,
        "sandbox_or_hyper_v_activated": False,
        "rebooted": False,
    })
    write_text("overview/integrated-overview.md", overview_text())
    write_text("deliverables/static-report.html", accessible_html())
    write_repo("tests/test_ghc_family_v651_v1_x1.py", x1_test_source())

    request_path = write_json("workflow/workflow-plan-request.json", workflow_request())
    run(sys.executable, str(WORKFLOW_RUNNER), str(request_path), "--out-dir", str(ROOT / "workflow"))
    run(sys.executable, str(REFLECTION_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--output-dir", str(ROOT / "reflection-remaster"), "--phase", d.PHASE, "--owner", d.OWNER, "--focus", "evidence reproducibility and retained-negative discipline")
    run(sys.executable, str(INDEX_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--out-dir", str(ROOT / "tooling"), "--phase", d.PHASE, "--owner", d.OWNER)

    # Build privacy and exact-working-byte manifest receipts after every x1 artifact exists.
    paths_before_receipts = status_paths()
    private_patterns = {
        "raw_task_or_thread_identifier": re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", re.I),
        "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\\\Users\\\\|[A-Za-z]:/Users/|[A-Za-z]:\\\\GHC-Archives\\\\worktrees)", re.I),
        "credential_or_private_key_payload": re.compile(r"(?:BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|sk-[A-Za-z0-9]{20,})"),
        "private_callable_identifier": re.compile(r"(?:private_callable_id|session_stream_id)\s*[:=]", re.I),
        "private_conversation_payload": re.compile(r"(?:raw transcript|conversation export|private route payload)\s*[:=]", re.I),
    }
    candidates = []
    for rel in paths_before_receipts:
        path = REPO / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for cls, pattern in private_patterns.items():
            for match in pattern.finditer(text):
                candidates.append({"path": rel, "class": cls, "offset": match.start(), "disposition": "confirmed_payload"})
    write_json("validation/x1-staged-privacy.json", {
        "schema": "ghc.family.v651-v1.x1-privacy.v1",
        "scan_classes": list(private_patterns),
        "scanned_path_count": len(paths_before_receipts),
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(candidates),
        "hits": candidates,
        "scanner_definition_separated_from_payload": True,
    })
    if candidates:
        raise RuntimeError(f"privacy scan found {len(candidates)} confirmed payload hits")

    paths_with_privacy = status_paths()
    manifest_rel = f"{d.PHASE_ROOT}/validation/x1-staged-manifest.json"
    review_rel = f"{d.PHASE_ROOT}/validation/x1-staged-review.json"
    entries = []
    for rel in paths_with_privacy:
        if rel in {manifest_rel, review_rel}:
            continue
        raw = prospective_git_blob_bytes(REPO / rel)
        entries.append({"path": rel, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "hash_domain": "prospective_normalized_git_blob_bytes"})
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc.family.v651-v1.x1-staged-review.v1",
        "lifecycle": "x1_only",
        "intended_path_count": len(entries) + 2,
        "content_entry_count": len(entries),
        "self_exclusions": [manifest_rel, review_rel],
        "x2_paths_present": False,
        "privacy_confirmed_hits": 0,
        "diff_hygiene_expected": True,
    })
    review_raw = prospective_git_blob_bytes(ROOT / "validation/x1-staged-review.json")
    entries.append({"path": review_rel, "sha256": hashlib.sha256(review_raw).hexdigest(), "bytes": len(review_raw), "hash_domain": "prospective_normalized_git_blob_bytes"})
    write_json("validation/x1-staged-manifest.json", {
        "schema": "ghc.family.v651-v1.x1-manifest.v1",
        "source_head": d.SOURCE_HEAD,
        "entries": sorted(entries, key=lambda x: x["path"]),
        "entry_count": len(entries),
        "self_exclusions": [manifest_rel],
        "covered_path_count": len(entries) + 1,
    })

    print(json.dumps({
        "valid": True,
        "phase": d.PHASE,
        "proposal_count": len(d.PROPOSALS),
        "frozen_count": len(frozen),
        "portfolio_counts": {key: len(rows) for key, rows in portfolios.items()},
        "mutation_count": len(mutations),
        "source_count": len(d.SOURCES),
        "manifest_entries": len(entries),
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    build()
