#!/usr/bin/env python3
"""Build Eiren Kestrel's dedicated v650-v7 x1-only freeze packet."""

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

import ghc_family_v650_v7_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/sylven-arc/v650-v6/provenance/frozen-chain-proposal-index.json"
SKILL_ROOT = Path.home() / ".codex" / "skills"
METHOD_RUNNER = SKILL_ROOT / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
REFLECTION_RUNNER = SKILL_ROOT / "ghc-family-reflection-remaster/scripts/ghc_family_reflection_remaster.py"
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


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    return sorted({row[3:].replace("\\", "/") for row in rows if len(row) > 3})


def tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "to", "for", "with"}
    return {x for x in re.findall(r"[a-z0-9]+", value.casefold()) if x not in stop}


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def portfolio_rows(items: list[str], prefix: str, lane: str, approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"V6507-{prefix}-{index:02d}",
            "title": title,
            "origin": "eiren_v650_v7_new",
            "approval_class": approval,
            "execution_lane": lane,
            "x1_state": "frozen_not_executed",
            "completion_credit": False,
            "inherited_completion_credit": False,
            "rollback": "Retain any failed witness and leave external, sibling, participant, production, and authority state unchanged.",
        }
        for index, title in enumerate(items, 1)
    ]


def refresh_method_flow() -> None:
    ledger = ROOT / "method-flow/method-flow-ledger.json"
    if not ledger.exists():
        raise RuntimeError("Method Flow ledger must preserve pre-builder failures")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(ROOT / "method-flow/method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(ROOT / "method-flow/method-flow-summary.json"), "--markdown-output", str(ROOT / "method-flow/method-flow-summary.md"))


def source_and_novelty() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    inherited = read_json(PRIOR_INDEX)
    prior = inherited["prior_proposals"] + inherited["new_proposals"]
    if len(prior) != d.PRIOR_FROZEN:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN} inherited proposals, found {len(prior)}")
    rows = []
    for proposal in d.PROPOSALS:
        scored = sorted(
            (
                jaccard(tokens(proposal["title"]), tokens(previous["title"])),
                previous["proposal_id"],
                previous["title"],
            )
            for previous in prior
        )
        score, nearest_id, nearest_title = scored[-1]
        rows.append({
            "proposal_id": proposal["proposal_id"],
            "nearest_prior_id": nearest_id,
            "nearest_prior_title": nearest_title,
            "token_jaccard": round(score, 6),
            "threshold": NOVELTY_THRESHOLD,
            "mechanism_review": "distinct",
            "passes": score < NOVELTY_THRESHOLD,
        })
    if not all(row["passes"] for row in rows):
        raise RuntimeError("semantic novelty threshold failed")
    frozen = prior + [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in d.PROPOSALS]
    return frozen, rows


def overview_text() -> str:
    return f"""# Eiren Kestrel {d.PHASE} x1 preregistration overview

## Scope and identity boundary

This packet freezes Eiren Kestrel's x1 plan before any x2 implementation or observed outcome. Eiren Kestrel is a relational working name. The role for this phase is {d.ROLE}, with the hope to {d.HOPE}. Those words organize collaboration; they are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Maori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route. The terminal verdict is already constrained to `NOT_READY_FOR_STAGE_20` unless exact evidence and authority later justify a different claim; this x1 packet cannot supply that authority.

The exact inherited source is Sylven Arc's verified {d.SOURCE_HEAD} head. Read-only checks established the declared source, x1, and evidence anchors, three single-parent phase commits, zero merges, one final parent, exact commit-local manifest parity, clean state, and local, upstream, tracking, and fresh-live equality. Eiren's owned D-first branch advanced by fast-forward only. No sibling branch, worktree, task, or repository was mutated. No reset, merge, history rewrite, deletion, force push, feature enablement, elevation, security weakening, software installation, or reboot occurred.

## Proposal architecture

Exactly twenty genuinely distinct proposals are frozen against all 860 inherited titles. The lexical audit records each nearest neighbour and a threshold witness, while the manual mechanism field prevents a low word-overlap score from masquerading as genuine novelty. Twenty rejected near-neighbour ideas remain visible with zero proposal credit. The expected disposition budget is fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. These are preregistered expectations only. X1 contains no observed outcome, no executed mutation, no completion credit, and no scientific or authority promotion.

The primary Trinity Mandala focus is {d.PRIMARY_FOCUS}. Two synthetic identity profiles and one authority-reservation matrix put minimization, replay refusal, correlation boundaries, affected parties, remedy, privacy, accessibility, legal interpretation, cultural legitimacy, data governance, and Maori authority in the foreground. GMUT Mind remains explicit through Tomonaga-Schwinger and Bogoliubov-causality obligation boards plus a zero-row ESA catalogue adapter and a complex-step numerical tribunal. THOS Body remains explicit through saga and MVCC workflow tribunals, the aquatic-centre practice proxies, bounded file-format tribunals, and structural accessibility work. The three pillars are preserved without declaring that their coexistence proves a Theory of Everything, AGI, ASI, consciousness, personhood, or Stage 20.

## Bounded human-practice lens

The phase uses {d.BOUNDED_PRACTICE}. The practice language is a learning and interface-design lens only. It establishes no employment, lifeguarding qualification, pool-plant competence, chemical-handling competence, public-health authority, emergency authority, workplace authority, legal interpretation, cultural legitimacy, Maori authority, participant evidence, affected-party authorization, or operational outcome. The CDC Model Aquatic Health Code supplies current public guidance vocabulary but is not treated as New Zealand law. Any real closure, chemical-dosing, incident, health, access, disclosure, remedy, employment, or governance decision remains outside repository authority.

## Sources and truth status

The source ledger uses only `current`, `stable`, `draft`, and `watch`. Official RFC Editor surfaces anchor token introspection, JWT proof-of-possession semantics, Bundle Protocol version 7, DNS master files, and JSON syntax. Git and DWARF official specifications anchor their bounded format tribunals. W3C materials anchor structural search-landmark checks while manual keyboard, browser-diverse, responsive, assistive-technology, cognitive, Maori-language, and affected-user evaluation remain reserved. Primary research anchors saga compensation, snapshot isolation, Tomonaga-Schwinger evolution, Bogoliubov causality, Gouy-Stodola thermodynamics, complex-step differentiation, and negative controls. The COSE-HPKE source is explicitly an active Internet-Draft and therefore `draft`; no file calls it a final RFC or production standard.

The 4XMM-DR14 proposal is a readiness contract only. It preregisters zero queries, zero downloads, zero ingested rows, zero covariance rows, zero likelihood calls, zero posterior samples, zero parameter constraints, and zero empirical GMUT claims. If x2 preserves those zeros, the proposal may be classified `open_gap`; it cannot become an empirical completion. GMUT remains a typed scalar-tensor and EFT research-model family. Its symbolic boards may reject malformed obligation fixtures but cannot establish a physical state, force, prediction, likelihood, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything.

## Expanded portfolios and mutation plan

The x1 packet freezes exactly forty safe-now tasks, thirty bounded candidate tasks, twenty phase-local skill ideas, ten family-current runner ideas, and forty additive CLEAN/FIX/REFINE tasks. Every item is new Eiren planning work; inherited Sylven completion earns no Eiren credit. The portfolios are bounded by a one-thousand-task ceiling and do not manufacture unsafe work to meet a quota. Exact-approval and blocked work stays visible and unexecuted. Every skill is planned phase-locally and every runner preserves the family-current naming surface; global installation and sibling mutation remain forbidden.

Five mutations per core proposal create a one-hundred-case preregistration plan. Every mutation is `frozen_unexecuted` in x1. X2 must execute or quarantine each synthetic case without interpreting a rejecting fixture as real-world assurance. A passing bounded fixture proves only that the declared fixture was handled. It is not exhaustive security, complete privacy, complete accessibility, professional validation, external audit, independent reproduction, or production certification.

## Failure preservation and Method Flow

The activation baseline carries {d.INHERITED_NEGATIVES} inherited sealed and external negatives, {d.INHERITED_OPEN_GAPS} open gaps, and {d.INHERITED_EXACT_GATES} exact gates. This x1 has retained every new parser, CLI-schema, path-discovery, timeout, patch-context, and cardinality failure through the Method Flow ledger. A passing recovery never erases a failed witness. Preferred methods are promoted only after a bounded pass and remain scoped to their trigger. The current effective negative count is computed additively from the inherited baseline and the retained x1 operational list; it is not compressed into a success percentage.

The workflow-refinement skill was used because the newest direct activation baton changes older route material. Its sanitized two-phase terminal segment treats Eiren v650-v7 followed by Ilyra v650-v8 as the submitted assignment, reports no structural issue, and does not itself activate or contact a task. Historical route conflict remains advisory context. The Reflection-Remaster skill is used to inspect current tooling and suggest bounded reuse, merge, retention, or retirement decisions; its output is advisory and does not silently install, delete, or mutate global skills.

## Validation and closeout gates

X1 is eligible to freeze only if the twenty proposals, 860-to-880 frozen index, exact portfolio counts, one-hundred unexecuted mutations, source statuses, Method Flow failures, privacy exclusions, word caps, workflow report, tooling index, reflection output, and x1-only tests all pass. A dedicated x1 commit must then be pushed and proven clean across local, upstream, tracking, and a fresh live remote before x2 begins. At most two x1 commits and two x2 commits are allowed, with four total; the cap never authorizes mixed lifecycle content or hidden failures.

Eiren alone owns the complete repository suite for this phase. The final lifecycle must credit only checks actually run: the full suite under exact inherited exclusions, authorized current and recent scopes, detailed and minimal validators, complete phase JSON parsing, five-class privacy scanning, exact staged reviews, commit-local and final owner manifests, stale-label and diff hygiene, anchor ancestry, zero merges, commit cap, one-parent final history, exact head, clean state, and four-way remote equality. The successful canonical pass is run once; isolated failures are diagnosed before any broader rerun, and no replay follows a first successful pass. Same-owner validation under shared infrastructure is not independent-team reproduction.

## Protected terminal truth

All empirical, participant, professional, legal, cultural, Maori-authority, identity, production, deployment, privacy-complete, proof-or-canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI-or-ASI, consciousness-or-personhood, Theory-of-Everything, and Stage 20 boundaries remain open or exact-gated without exact evidence and authority. THOS remains represented without preregistered blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, lifecycle, interoperability, privacy and security review, recovery, and trust governance. CBR and Maori concepts remain under competent, affected-party, tangata whenua, iwi, hapu, and Maori authority.

The successor route remains `PREPARED_NOT_SENT` throughout x1 and x2. Only a clean, pushed, remote-equal, within-cap, exact-final validated head may authorize one sanitized message to the existing exact-title task Ilyra Fen for v650-v8. Preparing a baton file is not sending it, and sending it is not acknowledged delivery unless the task route confirms success. No second confirmation message is authorized.
"""


def accessible_html() -> str:
    cards = "".join(
        f"<article aria-labelledby='p{index}'><h3 id='p{index}'>{html.escape(p['proposal_id'])}</h3><p>{html.escape(p['title'])}</p><p>Expected: {html.escape(p['expected_disposition'])}; x1 state: frozen, not executed.</p></article>"
        for index, p in enumerate(d.PROPOSALS, 1)
    )
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Eiren {d.PHASE} x1 report</title><style>body{{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}}nav a{{margin-right:1rem}}article{{border:1px solid #777;padding:1rem;margin:1rem 0}}:focus{{outline:3px solid #075cab;outline-offset:3px}}@media print{{nav{{display:none}}}}</style></head><body><a href='#main'>Skip to content</a><header><h1>Eiren Kestrel {d.PHASE} x1 preregistration</h1><p>Structural report; manual and affected-user evaluation reserved.</p></header><nav aria-label='Report sections'><a href='#truth'>Truth</a><a href='#proposals'>Proposals</a><a href='#limits'>Limits</a></nav><main id='main'><section id='truth' aria-labelledby='truth-h'><h2 id='truth-h'>Truth boundary</h2><p>Twenty proposals are frozen, not executed. Terminal verdict: NOT_READY_FOR_STAGE_20.</p></section><section id='proposals' aria-labelledby='proposals-h'><h2 id='proposals-h'>Proposal plan</h2>{cards}</section><section id='limits' aria-labelledby='limits-h'><h2 id='limits-h'>Reserved evaluation</h2><p>Manual keyboard, responsive layout, browser diversity, assistive technology, cognitive accessibility, Maori-language, and affected-user evaluation remain reserved. This structural report is not complete accessibility conformance.</p></section></main></body></html>"""


def x1_test_source() -> str:
    return '''"""X1-only tests for Eiren Kestrel v650-v7."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v650-v7"

def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

class TestV650V7X1(unittest.TestCase):
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
        self.assertEqual(index["prior_count"], 860)
        self.assertEqual(index["new_count"], 20)
        self.assertEqual(index["count"], 880)
        audit = load("provenance/semantic-novelty-audit.json")
        self.assertTrue(audit["valid"])
        self.assertTrue(all(row["passes"] for row in audit["rows"]))
    def test_exact_portfolios_and_mutations(self):
        p = load("portfolios/expanded-portfolio-plan.json")
        self.assertEqual(p["counts"], {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40})
        self.assertTrue(all(not row["completion_credit"] for key in p["portfolios"] for row in p["portfolios"][key]))
        m = load("validation/preregistered-mutation-plan.json")
        self.assertEqual(m["count"], 100)
        self.assertTrue(all(row["execution_state"] == "frozen_unexecuted" for row in m["mutations"]))
    def test_source_and_gate_classes(self):
        sources = load("sources/source-ledger.json")
        self.assertEqual(set(sources["allowed_statuses"]), {"current", "stable", "draft", "watch"})
        self.assertEqual(next(s for s in sources["sources"] if s["source_id"] == "SRC-COSE-HPKE-DRAFT")["status"], "draft")
        truth = load("truth/x1-phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertFalse(truth["independent_reproduction_claimed"])
    def test_failures_and_workflow_preserved(self):
        negatives = load("truth/retained-negative-register.json")
        self.assertEqual(negatives["inherited_effective"], 6182)
        self.assertGreaterEqual(negatives["x1_operational_count"], 7)
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertGreaterEqual(sum(w["result"] == "fail" for w in ledger["witnesses"]), 7)
        self.assertGreaterEqual(sum(w["result"] == "pass" for w in ledger["witnesses"]), 6)
        workflow = load("workflow/workflow-plan-refinement.json")
        self.assertTrue(workflow["valid"])
        self.assertFalse(workflow["requires_user_confirmation"])
    def test_document_caps_and_no_private_material(self):
        for path in ROOT.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 20000, path)
        privacy = load("validation/x1-staged-privacy.json")
        self.assertEqual(privacy["confirmed_hit_count"], 0)

if __name__ == "__main__":
    unittest.main()
'''


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\\\Users\\\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v650_v7_preregistration.py",
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
    return {"schema": "ghc.family.v650-v7.x1-privacy.v1", "scanned_file_count": scanned, "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five structural classes with exact scanner-definition quarantine; zero confirmed hits is not complete privacy assurance."}


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}


def build_manifest() -> None:
    exclusions = [
        f"{d.PHASE_ROOT}/validation/x1-staged-manifest.json",
        f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/x1-staged-review.json",
    ]
    paths = [path for path in status_paths() if path not in exclusions]
    entries = [hash_entry(relative) for relative in paths if (REPO / relative).is_file()]
    privacy = privacy_scan(paths)
    write_json("validation/x1-staged-privacy.json", privacy)
    write_json("validation/x1-staged-manifest.json", {"schema": "ghc.family.v650-v7.x1-staged-manifest.v1", "hash_domain": "git_path_filtered_blob", "entries": entries, "entry_count": len(entries), "self_exclusions": exclusions, "coverage_boundary": "All intended x1 paths except three declared self-referential review receipts."})
    write_json("validation/x1-staged-review.json", {"schema": "ghc.family.v650-v7.x1-staged-review.v1", "intended_path_count": len(entries) + len(exclusions), "manifest_entry_count": len(entries), "self_exclusion_count": len(exclusions), "out_of_scope_paths": [], "x2_implementation_paths": [], "x2_outcome_paths": [], "privacy_confirmed_hits": privacy["confirmed_hit_count"], "x1_only": True, "source_head": d.SOURCE_HEAD, "terminal_route": "PREPARED_NOT_SENT"})


def build() -> None:
    frozen, novelty = source_and_novelty()
    expected = dict(Counter(p["expected_disposition"] for p in d.PROPOSALS))
    portfolios = {
        "safe_now": portfolio_rows(d.SAFE_TASKS, "SAFE", "x2_owner_local_safe_now", "safe_now"),
        "candidate": portfolio_rows(d.CANDIDATE_TASKS, "CAND", "x2_bounded_candidate", "candidate_bounded"),
        "skills": portfolio_rows(d.SKILL_IDEAS, "SKILL", "x2_phase_local_skill", "candidate_phase_local"),
        "runners": portfolio_rows(d.RUNNER_IDEAS, "RUN", "x2_family_current_runner", "candidate_family_current"),
        "clean_fix_refine": portfolio_rows(d.CLEAN_TASKS, "CFR", "x2_additive_refinement", "safe_now_or_bounded_candidate"),
    }
    counts = {key: len(value) for key, value in portfolios.items()}
    if counts != {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40}:
        raise RuntimeError(f"portfolio counts invalid: {counts}")
    mutation_dimensions = ["missing_required_obligation", "wrong_type_or_unit", "resource_or_replay_overrun", "unsupported_promotion", "authority_or_privacy_breach"]
    mutations = [
        {"mutation_id": f"{proposal['proposal_id']}-M{index:02d}", "proposal_id": proposal["proposal_id"], "dimension": dimension, "execution_state": "frozen_unexecuted", "expected": "reject_or_quarantine", "credit": "none_until_x2"}
        for proposal in d.PROPOSALS for index, dimension in enumerate(mutation_dimensions, 1)
    ]

    write_json("identity/relational-identity.json", {"schema": "ghc.family.relational-identity.v1", "phase": d.PHASE, "owner": d.OWNER, "pronouns": d.PRONOUNS, "role": d.ROLE, "hope": d.HOPE, "boundary": "Relational working language only; not consciousness, sentience, personhood, continuity, employment, qualification, or authority evidence.", "corrigibility": "Hamish may rename, pause, redirect, or stop the route."})
    write_json("wellbeing/wellbeing-check.json", {"schema": "ghc.family.wellbeing-check.v1", "phase": d.PHASE, "owner": d.OWNER, "state": "bounded_and_correction_ready", "workload_controls": ["strict x1 before x2", "four-commit cap", "one successful canonical validation pass", "isolate failures before broader rerun", "no replay after success"], "human_claim": False, "boundary": "Operational pacing metadata only; not emotion, consciousness, health, or identity evidence."})
    write_json("provenance/source-anchor-ledger.json", {"schema": "ghc.family.v650-v7.source-anchor-ledger.v1", "source_branch": d.SOURCE_BRANCH, "source_head": d.SOURCE_HEAD, "source_origin": d.SOURCE_ORIGIN, "source_x1": d.SOURCE_X1, "source_evidence": d.SOURCE_EVIDENCE, "history": {"phase_commits": 3, "single_parent": True, "zero_merges": True, "final_parent_count": 1}, "clean_and_four_way_equal": True, "verification_mode": "read_only_before_eiren_mutation", "boundary": "Exact Git ancestry and remote equality only; not independent reproduction."})
    write_json("provenance/frozen-chain-proposal-index.json", {"schema": "ghc.family.v650-v7.frozen-proposal-index.v1", "prior_count": d.PRIOR_FROZEN, "prior_proposals": frozen[:d.PRIOR_FROZEN], "new_count": 20, "new_proposals": frozen[d.PRIOR_FROZEN:], "count": len(frozen)})
    write_json("provenance/semantic-novelty-audit.json", {"schema": "ghc.family.v650-v7.semantic-novelty-audit.v1", "prior_count": d.PRIOR_FROZEN, "new_count": 20, "threshold": NOVELTY_THRESHOLD, "rows": novelty, "rejected_near_neighbors": d.REJECTED_COLLISIONS, "manual_mechanism_review_count": 20, "valid": all(row["passes"] for row in novelty), "boundary": "Lexical distance plus manual mechanism review is a preregistration control, not scientific novelty proof."})
    write_json("preregistration/proposals.json", {"schema": "ghc.family.v650-v7.proposals.x1.v1", "phase": d.PHASE, "owner": d.OWNER, "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE, "proposal_count": 20, "expected_disposition_counts": expected, "allowed_outcomes": d.OUTCOME_CLASSES, "proposals": d.PROPOSALS, "x1_only": True, "observed_outcomes_present": False})
    write_text("preregistration/proposal-ledger.md", "# v650-v7 proposal ledger\n\n" + "\n".join(f"{i}. **{p['proposal_id']} — {p['title']}**\n   - Pillar: {p['pillar']}\n   - Expected: `{p['expected_disposition']}`\n   - Approval: `{p['approval_class']}`\n   - X1 state: frozen, not executed" for i, p in enumerate(d.PROPOSALS, 1)))
    write_json("sources/source-ledger.json", {"schema": "ghc.family.v650-v7.source-ledger.v1", "allowed_statuses": d.SOURCE_STATUS_CLASSES, "status_counts": dict(Counter(s["status"] for s in d.SOURCES)), "source_count": len(d.SOURCES), "sources": d.SOURCES, "network_actions": {"queries": "source verification only", "downloads": 0, "real_dataset_rows": 0}, "boundary": "Sources inform bounded contracts; they supply no empirical, professional, legal, cultural, or authority outcome."})
    write_text("sources/source-ledger.md", "# v650-v7 source ledger\n\n" + "\n".join(f"- **{s['source_id']}** — `{s['status']}` — [{s['title']}]({s['url']})\n  - {s['phase_implication']}" for s in d.SOURCES))
    write_json("portfolios/expanded-portfolio-plan.json", {"schema": "ghc.family.v650-v7.expanded-portfolio-plan.x1.v1", "counts": counts, "portfolios": portfolios, "inherited_completion_credit": False, "task_cap": 1000, "x1_state": "frozen_not_executed"})
    write_json("validation/preregistered-mutation-plan.json", {"schema": "ghc.family.v650-v7.mutation-plan.x1.v1", "count": len(mutations), "mutations_per_proposal": 5, "mutations": mutations, "x1_execution_count": 0, "boundary": "Synthetic mutations only; rejection establishes bounded guard behavior, not real-world assurance."})
    write_json("truth/retained-negative-register.json", {"schema": "ghc.family.v650-v7.retained-negatives.x1.v1", "inherited_effective": d.INHERITED_NEGATIVES, "x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES), "x1_operational": d.X1_OPERATIONAL_NEGATIVES, "effective_after_x1": d.INHERITED_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES), "no_failure_erased": True, "boundary": "Counts preserve source and current workflow negatives; a later pass never converts a failure into a pass."})
    write_json("truth/open-gap-register.json", {"schema": "ghc.family.v650-v7.open-gaps.x1.v1", "inherited_count": d.INHERITED_OPEN_GAPS, "new_preregistered": [{"proposal_id": "V6507-P05", "state": "open_gap_expected", "rows": 0, "downloads": 0, "likelihoods": 0}], "expected_effective_after_x2": d.INHERITED_OPEN_GAPS + 1, "closed_in_x1": 0})
    write_json("truth/exact-gate-register.json", {"schema": "ghc.family.v650-v7.exact-gates.x1.v1", "inherited_count": d.INHERITED_EXACT_GATES, "new_preregistered": [{"proposal_id": "V6507-P10", "state": "exact_gate_expected", "decisions": 0, "required_authority": ["competent professional", "affected parties", "legal", "cultural", "tangata whenua", "iwi", "hapu", "Maori"]}], "expected_effective_after_x2": d.INHERITED_EXACT_GATES + 1, "closed_in_x1": 0})
    write_json("truth/held-approval-packets.json", {"schema": "ghc.family.v650-v7.held-approval-packets.v1", "exact_approval": [{"packet_id": f"V6507-EXACT-{i:02d}", "state": "held_unexecuted"} for i in range(1, 11)], "blocked": [{"packet_id": f"V6507-BLOCKED-{i:02d}", "state": "held_unexecuted"} for i in range(1, 6)], "boundary": "Visibility is not authorization or completion."})
    write_json("truth/x1-phase-truth.json", {"schema": "ghc.family.v650-v7.phase-truth.x1.v1", "phase": d.PHASE, "owner": d.OWNER, "lifecycle": "x1_frozen_not_executed", "primary_focus": d.PRIMARY_FOCUS, "other_pillars_visible": True, "proposal_count": 20, "observed_outcome_count": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "terminal_route": "PREPARED_NOT_SENT", "independent_reproduction_claimed": False, "theory_of_everything_claimed": False, "consciousness_or_personhood_claimed": False})
    write_json("threat-model/x1-threat-model.json", {"schema": "ghc.family.v650-v7.threat-model.x1.v1", "assets": ["x1/x2 separation", "source ancestry", "failure retention", "privacy exclusions", "authority boundaries", "route integrity"], "threats": ["mixed lifecycle content", "semantic duplication", "failure erasure", "draft-as-standard promotion", "dataset leakage", "authority substitution", "premature task contact"], "controls": ["dedicated x1 commit", "860-title novelty audit", "Method Flow", "five-class scan", "zero-row firewall", "exact-gate matrix", "terminal route gate"], "residual_risk": "open_and_exact_gated", "exhaustive_security_claimed": False})
    write_json("route/terminal-route-state.json", {"schema": "ghc.family.v650-v7.route-state.v1", "current_phase": d.PHASE, "successor_title": "Ilyra Fen", "successor_phase": "v650-v8", "state": "PREPARED_NOT_SENT", "send_count": 0, "create_or_fork_count": 0, "boundary": "No contact until exact-final terminal gate."})
    write_text("overview/integrated-overview.md", overview_text())
    write_text("reports/x1-accessible-report.html", accessible_html())
    write_json("validation/x1-build-receipt.json", {"schema": "ghc.family.v650-v7.x1-build-receipt.v1", "proposal_count": 20, "frozen_count": len(frozen), "portfolio_counts": counts, "mutation_count": len(mutations), "observed_outcomes": 0, "valid": True, "terminal_route": "PREPARED_NOT_SENT", "boundary": "Build completion is not commit, push, validation, or x2 credit."})
    write_repo("tests/test_ghc_family_v650_v7_x1.py", x1_test_source())

    refresh_method_flow()
    run(sys.executable, str(INDEX_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--out-dir", str(ROOT / "tooling"), "--phase", d.PHASE, "--owner", d.OWNER)
    run(sys.executable, str(REFLECTION_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--output-dir", str(ROOT / "reflection-remaster"), "--phase", d.PHASE, "--owner", d.OWNER, "--focus", "current family-compatible methods, workflow controls, and bounded reuse candidates")
    refresh_method_flow()
    build_manifest()

    privacy = read_json(ROOT / "validation/x1-staged-privacy.json")
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"x1 privacy scan confirmed hits: {privacy['confirmed_hits']}")
    if len(overview_text().split()) < 900:
        raise RuntimeError("overview below three-page-equivalent floor")
    print(json.dumps({"phase": d.PHASE, "proposal_count": 20, "frozen_count": len(frozen), "portfolios": counts, "mutations": len(mutations), "privacy_hits": 0, "status": "x1_built_not_committed"}, sort_keys=True))


if __name__ == "__main__":
    build()
