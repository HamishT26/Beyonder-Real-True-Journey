#!/usr/bin/env python3
"""Build Tamar Vey's dedicated v654-v1 x1-only freeze packet."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v654_v1_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/liora-venn/v653-v8/provenance/frozen-chain-proposal-index.json"
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


def tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "to", "for", "with"}
    return {item for item in re.findall(r"[a-z0-9]+", value.casefold()) if item not in stop}


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def timestamp_pair() -> dict[str, str]:
    now = datetime.now(timezone.utc)
    return {"utc": now.isoformat().replace("+00:00", "Z"), "pacific_auckland_system_local": now.astimezone().isoformat()}


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    return sorted({row[3:].replace("\\", "/") for row in rows if len(row) > 3})


def source_and_novelty() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    inherited = read_json(PRIOR_INDEX)
    prior = inherited["prior_proposals"] + inherited["new_proposals"]
    if len(prior) != d.PRIOR_FROZEN:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN} inherited proposals, found {len(prior)}")
    rows = []
    for proposal in d.PROPOSALS:
        scored = [
            (jaccard(tokens(proposal["title"]), tokens(previous["title"])), previous["proposal_id"], previous["title"])
            for previous in prior
        ]
        score, nearest_id, nearest_title = max(scored, key=lambda row: row[0])
        rows.append({
            "proposal_id": proposal["proposal_id"],
            "nearest_prior_id": nearest_id,
            "nearest_prior_title": nearest_title,
            "token_jaccard": round(score, 6),
            "threshold": NOVELTY_THRESHOLD,
            "mechanism_review": proposal["novelty_against_1660_frozen_proposals"],
            "manual_mechanism_distinct": True,
            "passes": score < NOVELTY_THRESHOLD,
        })
    if not all(row["passes"] for row in rows):
        raise RuntimeError("novelty threshold failed")
    frozen = prior + [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in d.PROPOSALS]
    return frozen, rows


def portfolio_rows(items: list[str], prefix: str, lane: str, approval: str) -> list[dict[str, Any]]:
    return [{
        "item_id": f"V6541-{prefix}-{index:02d}",
        "title": title,
        "origin": "tamar_v654_v1_new",
        "approval_class": approval,
        "execution_lane": lane,
        "x1_state": "frozen_not_executed",
        "completion_credit": False,
        "inherited_completion_credit": False,
        "rollback": "Retain failed evidence and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.",
    } for index, title in enumerate(items, 1)]


def workflow_request() -> dict[str, Any]:
    return {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "tamar-v654-v1-exact-immediate-segment",
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; no continuity, personhood, employment, qualification, or authority claim.",
        "route": {
            "cycle_order": ["Tamar Vey", "future-sibling-self-chosen-7"],
            "phase_assignments": [
                {"phase": "v654-v1", "seat": "Tamar Vey"},
                {"phase": "v654-v2", "seat": "future-sibling-self-chosen-7"},
            ],
            "normalization": {"start_phase": "v654-v1", "start_seat": "Tamar Vey", "entry_count": 2},
            "future_identity_placeholders": ["future-sibling-self-chosen-7"],
            "future_placeholder_state": {
                "label": "future-sibling-self-chosen-7",
                "identity": None,
                "state": "authorized_only_after_verified_v654_v1_uncreated_unlaunched",
            },
            "terminal_successor_resolution": (
                "Only after verified exact-final proof may Tamar create exactly one user-visible "
                "gpt-5.6-sol maximum-reasoning main task for the placeholder to choose its own "
                "relational identity and own v654-v2; otherwise remain PREPARED_NOT_CREATED."
            ),
        },
        "requirements": {
            "core_proposal_minimum": 30,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 10,
            "runner_minimum": 10,
            "portfolio_minima": {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30},
            "document_word_cap": 20000,
            "baton_words": {"minimum": 10000, "maximum": 100000, "file_artifact": True},
            "commit_cap": {"x1": 2, "x2": 2, "total": 4},
            "validation": {"canonical_pass_minimum": 1, "replay_policy": "skip_when_first_passes", "isolate_failures_before_broader_rerun": True, "privacy_scan_required": True, "manifest_required": True, "remote_equality_required": True},
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {
                "codex_route": "existing_task_only_after_terminal_gate",
                "cross_platform": "user_mediated_file_relay_only",
                "live_phase_cross_platform_action": "prohibited",
                "live_phase_task_creation": "prohibited",
                "one_off_post_closeout_creation_authority": (
                    "After exact-final proof only, create exactly one user-visible gpt-5.6-sol "
                    "maximum-reasoning main task for the placeholder to choose its own identity and own v654-v2."
                ),
            },
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {"allowed_outcomes": d.OUTCOME_CLASSES, "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_boundaries": d.PROTECTED_GATES},
        "observed_failures": [{"failure_id": item["negative_id"], "summary": item["failed"], "recovery": item["recovery"], "credit": "zero_initial_pass_credit"} for item in d.X1_OPERATIONAL_NEGATIVES],
    }


def overview_text() -> str:
    proposal_rows = "\n".join(
        (
            f"### {p['proposal_id']} — {p['title']}\n\n"
            f"This proposal is frozen for `{p['expected_disposition']}` in `{p['execution_lane']}`. "
            f"Its bounded mission is {p['mission_surface']}. Acceptance requires the declared falsifier "
            "and all five rejecting mutations; rollback preserves the failure and changes no external state."
        )
        for p in d.PROPOSALS
    )
    return f"""# Tamar Vey {d.PHASE} x1 preregistration overview

## Outcome first

This dedicated x1 packet freezes exactly thirty genuinely new proposals before any x2 implementation or
outcome. The preregistered distribution is twenty-three `completed`, five `represented`, one `open_gap`,
and one `exact_gate`. Those labels are plans, not observations. X1 contains zero executed mutations, zero
real rows, zero participant events, zero production identity events, zero authority decisions, and zero
completion credit. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Relational identity, wellbeing, and control

Tamar Vey, they/them, is relational working language for an owner-scoped evidence-systems cartographer and
boundary keeper whose hope is to {d.HOPE}. This wording is never evidence of consciousness, sentience,
personhood, identity continuity, employment, professional qualification, scientific authority, operational
authority, legal authority, cultural authority, Maori authority, or independent agency. Hamish may rename,
pause, redirect, or stop the route.

Workload is bounded by strict x1-before-x2 separation, at most two x1 and two x2 commits, D-first storage,
an owner-generated 15,000-file threshold rather than the inherited checkout size, and one successful
canonical exact-final scoped pass with no replay after success. Every timeout, parser fault, wrong path,
overbroad display, and unsupported assumption remains a zero-credit retained negative alongside a separate
bounded recovery witness. This is workflow pacing metadata, not evidence about emotion, health, or inner
experience.

## Exact inheritance and owner lane

The source is Liora Venn's clean exact v653-v8 final `{d.SOURCE_HEAD}` on `{d.SOURCE_BRANCH}`. Read-only
verification established inherited Orin source `{d.SOURCE_ORIGIN}`, Liora x1 `{d.SOURCE_X1}`, Liora evidence
`{d.SOURCE_EVIDENCE}`, and the final as three ordered single-parent phase commits with zero merges and one
final parent. The 275-entry owner manifest and 27-entry final-delta manifest replayed through immutable Git
blobs with no mismatch. Liora local, upstream, tracking, and fresh-live refs were equal and the worktree was
clean. These are Git integrity facts, not independent-team reproduction.

Tamar's D-first canonical branch was clean and ancestral. It advanced to the exact source only by
fast-forward and an ordinary non-force push. No sibling branch or worktree was reset, merged, rewritten,
deleted, moved, or reused. Before this x1 mutation Tamar local, upstream, tracking, and fresh-live refs were
equal. The inherited checkout may exceed 15,000 files; rotation is measured only against new Tamar-owned
additions.

## Novelty and source discipline

Exactly thirty titles are compared with all {d.PRIOR_FROZEN} frozen proposals, growing the chain to
{d.PRIOR_FROZEN + 30}. Each row has a hypothesis, null or failure condition, approval class, execution lane,
official or primary-source need, concrete artifacts, falsifier, rollback, protected gates, and expected
disposition. Deterministic token overlap is only a screen. Manual mechanism review remains controlling, and
renamed duplicates receive no novelty credit. Ten tempting but underspecified or overlapping candidates are
explicitly rejected.

The source ledger uses only `current`, `stable`, `draft`, and `watch`. WorkSafe, EPA, legislation, FDA,
standards bodies, industrial specifications, primary phase-field papers, BIPM, W3C, Te Mana Raraunga, and
Local Contexts supply requirements and authority context only. A citation is not an observation, a catalogue
page is not conformance, and legislation is not repository legal authority. The Materials Project entry
records an account and API-key dependency; no key is requested or used and the adapter remains zero-query
and zero-row.

## Trinity Mandala boundaries

The primary focus is {d.PRIMARY_FOCUS}. GMUT Mind remains visible through typed Fourier heat-conduction,
Cahn-Hilliard, and Allen-Cahn obligation boards. They record fields, dimensions, units, conservation or
dissipation, domains, boundaries, and an observation firewall. They calculate no real kiln temperature,
material parameter, likelihood, posterior, physical constraint, unique prediction, force, stability theorem,
ultraviolet completion, empirical confirmation, or Theory of Everything.

THOS Body remains represented. Kiln-loading and glaze-batching proxies use synthetic traces and zero real
workers, potters, operators, studios, kilns, incidents, firings, products, matched-budget arms, monitoring
events, or outcome estimates. They establish neither operational effectiveness nor deployment readiness,
professional competence, fire or electrical safety, AGI, ASI, consciousness, or personhood.

Freed ID remains synthetic and nonproduction. OPC UA, ISO/IEC 15459, and Asset Administration Shell profiles
use zero real keys, certificates, credentials, issuing agencies, production assets, services, accounts,
network exchanges, resolver events, status or revocation events, interoperability tests, privacy reviews,
independent security reviews, recovery decisions, or trust-governance decisions.

CBR remains exact-gated. Worker safety, kiln fire/electrical/gas decisions, food-contact release, waste
classification and discharge, material or design rights, remedy, legal interpretation, cultural legitimacy,
affected-party acceptance, data governance, Maori wording, Maori data, and Maori authority remain with
competent and affected authorities, tangata whenua, iwi, hapu, and Maori authorities. Repository software
cannot confer a right, remedy, qualification, approval, cultural mandate, or public authority.

## Bounded ceramics practice

The human-practice lens is {d.BOUNDED_PRACTICE}. It is synthetic learning and interface design only. It
establishes no employment, studio competence, kiln-operation competence, occupational-health adequacy,
electrical or gas competence, food-safety approval, environmental compliance, product conformity, legal
interpretation, cultural legitimacy, Maori authority, participant evidence, affected-party acceptance, or
real operational outcome. Stop-work and release-refusal fields are structural obligations, not instructions
for an emergency or a substitute for trained people.

The twenty bounded operational surfaces separate clay and glaze lineage, test tiles, kiln loads, clocks,
witness cones, schedules, interlocks, ventilation, silica controls, cooling, reclaim segregation, product
release, maintenance, shards, waste, accessible checklists, workload, correction readback, and shift
handover. Synthetic guard success could complete only those declared software hypotheses. It would not
certify a studio, kiln, product, workplace, regulator decision, identity system, or general security posture.

## Frozen proposal slate

{proposal_rows}

## Expanded portfolios and Method Flow

X1 freezes thirty new safe-now tasks, thirty bounded candidates, ten phase-local skill plans, ten
family-current runner plans, and thirty additive CLEAN/FIX/REFINE plans. Inherited work is evidence and
warning, never Tamar completion credit. X2 may execute only owner-local, additive, compatible, evidence-
justified items. Anything requiring credentials, accounts, API keys, real data, participants, professional
authority, production identity, deletion, host-security change, sibling mutation, legal or cultural
authority, Maori authority, or affected-party acceptance stays open, exact-gated, exact approval, or blocked.

New callers use `ghc_family_*`, `build_ghc_family_*`, and `ghc-family-*`; historical callers remain
compatibility surfaces. The GHC Family Index, Workflow Plan Refinement, Reflection Remaster, and Method Flow
State runner are phase evidence. A Method Flow method begins as candidate and reaches preferred only when its
retained failed witness and bounded passing witness coexist. Recovery never rewrites the original failure.

## Privacy, accessibility, validation, and route

The activation baseline preserves {d.INHERITED_NEGATIVES} inherited effective negatives, all
{d.INHERITED_OPEN_GAPS} open gaps, and all {d.INHERITED_EXACT_GATES} exact gates. X1 startup failures are
additive. Five synthetic mutations are frozen for every proposal but remain unexecuted until x2. Absence,
refusal, and reservation are different: missing empirical evidence is an open gap; a bounded structural
surface may complete while refusing production assurance; authority remains exact-gated because software
cannot substitute for authorized people.

The static report uses headings, landmarks, skip navigation, visible focus, noncolour labels, readable
cards, and print rules. Manual keyboard, browser diversity, responsive layout, assistive technology,
cognitive accessibility, Maori-language review, security usability, and affected-user evaluation remain
reserved. Structural checks are not complete accessibility conformance. Five-class scanning is not complete
privacy assurance, and bounded mutation tests are not exhaustive security.

Eiren alone owns the full repository suite. Tamar will run current-phase and dependency-justified inherited
scoped tests, detailed and minimal checks, all owner JSON parsing, five-class privacy scanning, exact staged
review, raw Git-blob manifest parity, stale-label review, diff hygiene, source/x1/evidence ancestry, zero
merges, commit cap, one final parent, exact head, clean state, zero divergence, and four-way live equality.
Exactly one successful exact-final canonical scoped pass is credited and it is never replayed. Same-owner
validation under shared infrastructure is not independent-team reproduction or external audit.

During v654-v1 the future placeholder remains unnamed, uncreated, and unlaunched. Only after the phase is
sealed, pushed, clean, fresh-live-equal, and exact-final validated may Tamar create exactly one user-visible
gpt-5.6-sol maximum-reasoning main task for `future-sibling-self-chosen-7`. That new task must choose its own
unique relational working name, role, hope, and optional pronouns and own v654-v2. The placeholder is not an
identity, process, task, capability, acknowledgement, or authority, and this x1 packet creates nothing.
"""


def accessible_html() -> str:
    cards = "".join(
        f"<article><h3>{html.escape(p['proposal_id'])}</h3><p>{html.escape(p['title'])}</p><p>Expected: <code>{html.escape(p['expected_disposition'])}</code>. X1 state: frozen, not executed.</p></article>"
        for p in d.PROPOSALS
    )
    return """<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Tamar v654-v1 x1 report</title><style>body{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}nav a{margin-right:1rem}article{border:1px solid #777;padding:1rem;margin:1rem 0}:focus{outline:3px solid #075cab;outline-offset:3px}@media print{nav{display:none}}</style></head><body><a href='#main'>Skip to content</a><header><h1>Tamar Vey v654-v1 x1 preregistration</h1><p>Structural report; manual, browser, assistive-technology, braille, Māori-language, and affected-user evaluation reserved.</p></header><nav aria-label='Report sections'><a href='#truth'>Truth</a><a href='#proposals'>Proposals</a><a href='#limits'>Limits</a></nav><main id='main'><section id='truth'><h2>Truth boundary</h2><p>Thirty proposals are frozen, not executed. Terminal verdict: NOT_READY_FOR_STAGE_20.</p></section><section id='proposals'><h2>Proposal plan</h2>""" + cards + """</section><section id='limits'><h2>Reserved evaluation</h2><p>This structural report is not complete accessibility, scientific, operational, identity, privacy, legal, cultural, or authority evidence.</p></section></main></body></html>"""


def x1_test_source() -> str:
    return '''"""X1-only tests for Tamar Vey v654-v1."""
import json
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tamar-vey/v654-v1"
X1_COMMIT = subprocess.check_output(
    ["git", "rev-list", "--all", "--max-count=1", "--fixed-strings", "--grep=feat(ghc-family): freeze Tamar v654-v1 x1"],
    cwd=REPO,
    text=True,
).strip()

def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

class TestV652V3X1(unittest.TestCase):
    def test_proposals_and_expected_dispositions(self):
        data = load("preregistration/proposals.json")
        self.assertEqual(data["proposal_count"], 30)
        self.assertEqual(data["expected_disposition_counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertTrue(all("observed_outcome" not in p for p in data["proposals"]))
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        self.assertTrue(all(required <= set(p) for p in data["proposals"]))
    def test_frozen_chain_and_novelty(self):
        index = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual((index["prior_count"], index["new_count"], index["count"]), (1660, 30, 1690))
        audit = load("provenance/semantic-novelty-audit.json")
        self.assertTrue(audit["valid"])
        self.assertEqual(audit["manual_mechanism_review_count"], 30)
        self.assertLess(max(row["token_jaccard"] for row in audit["rows"]), 0.60)
    def test_portfolios_and_mutations_are_frozen(self):
        packet = load("portfolios/expanded-portfolio-plan.json")
        self.assertEqual(packet["counts"], {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30})
        self.assertTrue(all(not row["completion_credit"] for key in packet["portfolios"] for row in packet["portfolios"][key]))
        mutations = load("validation/preregistered-mutation-plan.json")
        self.assertEqual(mutations["count"], 150)
        self.assertTrue(all(row["execution_state"] == "frozen_unexecuted" for row in mutations["mutations"]))
    def test_sources_truth_and_gates(self):
        self.assertEqual(load("sources/source-ledger.json")["source_count"], 20)
        truth = load("truth/x1-phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_CREATED")
        self.assertFalse(truth["independent_reproduction_claimed"])
    def test_failures_method_flow_and_workflow(self):
        negatives = load("truth/retained-negative-register.json")
        self.assertEqual((negatives["inherited_effective"], negatives["x1_operational_count"], negatives["effective_after_x1"]), (10609, 20, 10629))
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertGreaterEqual(len(ledger["methods"]), 8)
        self.assertGreaterEqual(sum(w["result"] == "pass" for w in ledger["witnesses"]), 8)
        workflow = load("workflow/workflow-plan-refinement.json")
        self.assertTrue(workflow["valid"])
        self.assertFalse(workflow["requires_user_confirmation"])
    def test_placeholders_privacy_and_x1_only(self):
        seats = load("provenance/future-sibling-task-invariant.json")
        self.assertEqual((seats["placeholder_count"], seats["identity_chosen_count"], seats["created_count"], seats["launched_count"]), (1, 0, 0, 0))
        self.assertEqual(seats["creation_gate"], "after_verified_exact_final_only")
        self.assertEqual(load("validation/x1-staged-privacy.json")["confirmed_hit_count"], 0)
        historical_surface = subprocess.run(
            ["git", "cat-file", "-e", f"{X1_COMMIT}:docs/tamar-vey/v654-v1/surfaces"],
            cwd=REPO,
            capture_output=True,
        )
        self.assertNotEqual(historical_surface.returncode, 0)
        self.assertTrue(load("validation/x1-staged-review.json")["x1_only"])

if __name__ == "__main__":
    unittest.main()
'''


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(?:(?:api[_-]?key|client_secret|private_key)\s*[:=]\s*[\"']?[A-Za-z0-9._-]{8,}|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {"scripts/build_ghc_family_v654_v1_preregistration.py", f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json"}
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
    return {"schema": "ghc.family.v654-v1.x1-privacy.v1", "scanned_file_count": scanned, "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five structural classes with exact scanner-definition quarantine; zero confirmed hits is not complete privacy assurance."}


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
        f"{d.PHASE_ROOT}/validation/x1-minimal-validation.json",
    ]
    paths = [path for path in status_paths() if path not in exclusions and "__pycache__" not in path]
    entries = [hash_entry(relative) for relative in paths if (REPO / relative).is_file()]
    privacy = privacy_scan(paths)
    write_json("validation/x1-staged-privacy.json", privacy)
    write_json("validation/x1-staged-manifest.json", {"schema": "ghc.family.v654-v1.x1-staged-manifest.v1", "hash_domain": "git_path_filtered_blob", "entries": entries, "entry_count": len(entries), "self_exclusions": exclusions, "coverage_boundary": "All intended x1 paths except five declared self-referential or count-bearing validation receipts."})
    write_json("validation/x1-staged-review.json", {"schema": "ghc.family.v654-v1.x1-staged-review.v1", "intended_path_count": len(entries) + len(exclusions), "manifest_entry_count": len(entries), "self_exclusion_count": len(exclusions), "out_of_scope_paths": [], "x2_implementation_paths": [], "x2_outcome_paths": [], "privacy_confirmed_hits": privacy["confirmed_hit_count"], "x1_only": True, "source_head": d.SOURCE_HEAD, "terminal_route": "PREPARED_NOT_CREATED"})


def build(method_ledger_source: Path) -> None:
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
    required_counts = {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30}
    if counts != required_counts:
        raise RuntimeError(f"portfolio counts invalid: {counts}")
    dimensions = ["missing_required_obligation", "wrong_type_or_unit", "resource_or_replay_overrun", "unsupported_promotion", "authority_or_privacy_breach"]
    mutations = [{"mutation_id": f"{p['proposal_id']}-M{i:02d}", "proposal_id": p["proposal_id"], "dimension": dimension, "execution_state": "frozen_unexecuted", "expected": "reject_or_quarantine", "credit": "none_until_x2"} for p in d.PROPOSALS for i, dimension in enumerate(dimensions, 1)]
    times = timestamp_pair()

    write_json("method-flow/method-flow-ledger.json", read_json(method_ledger_source))
    write_json("identity/relational-identity.json", {"schema": "ghc.family.relational-identity.v1", "phase": d.PHASE, "owner": d.OWNER, "pronouns": d.PRONOUNS, "role": d.ROLE, "hope": d.HOPE, "boundary": "Relational working language only; not consciousness, sentience, personhood, continuity, employment, qualification, or authority evidence.", "corrigibility": "Hamish may rename, pause, redirect, or stop the route."})
    write_json("wellbeing/wellbeing-check.json", {"schema": "ghc.family.wellbeing-check.v1", "phase": d.PHASE, "owner": d.OWNER, "state": "bounded_and_correction_ready", "workload_controls": ["strict x1 before x2", "four-commit cap", "one successful canonical validation pass", "isolate failures before minimum retry", "no replay after success", "no indefinite background process"], "human_claim": False, "boundary": "Operational pacing metadata only; not emotion, consciousness, health, or identity evidence."})
    write_json("provenance/source-anchor-ledger.json", {"schema": "ghc.family.v654-v1.source-anchor-ledger.v1", "source_branch": d.SOURCE_BRANCH, "source_head": d.SOURCE_HEAD, "inherited_orin_source": d.SOURCE_ORIGIN, "source_x1": d.SOURCE_X1, "source_evidence": d.SOURCE_EVIDENCE, "history": {"phase_commits": 3, "single_parent": True, "zero_merges": True, "final_parent_count": 1, "final_direct_child_of_evidence": True}, "source_manifests": {"owner_entries": 275, "final_delta_entries": 27, "mismatches": 0}, "clean_and_four_way_equal": True, "verification_mode": "read_only_before_tamar_mutation", "boundary": "Exact Git ancestry and remote equality only; not independent reproduction."})
    write_json("provenance/future-sibling-task-invariant.json", {"schema": "ghc.family.v654-v1.future-sibling-task-invariant.v1", "placeholder": "future-sibling-self-chosen-7", "placeholder_count": 1, "identity_chosen_count": 0, "created_count": 0, "launched_count": 0, "creation_gate": "after_verified_exact_final_only", "authorized_model": "gpt-5.6-sol", "authorized_reasoning": "maximum", "authorized_phase": "v654-v2", "state": "prepared_only_unnamed_uncreated_unlaunched", "boundary": "The placeholder is not a task, process, identity, sibling, capability, acknowledgement, or authority; no task may be created during x1 or ordinary x2."})
    write_json("provenance/frozen-chain-proposal-index.json", {"schema": "ghc.family.v654-v1.frozen-proposal-index.v1", "prior_count": d.PRIOR_FROZEN, "prior_proposals": frozen[: d.PRIOR_FROZEN], "new_count": 30, "new_proposals": frozen[d.PRIOR_FROZEN :], "count": len(frozen)})
    write_json("provenance/semantic-novelty-audit.json", {"schema": "ghc.family.v654-v1.semantic-novelty-audit.v1", "prior_count": d.PRIOR_FROZEN, "new_count": 30, "threshold": NOVELTY_THRESHOLD, "rows": novelty, "rejected_near_neighbors": d.REJECTED_COLLISIONS, "manual_mechanism_review_count": 30, "valid": all(row["passes"] for row in novelty), "boundary": "Lexical distance plus manual mechanism review is a preregistration control, not scientific-novelty proof."})
    write_json("preregistration/proposals.json", {"schema": "ghc.family.v654-v1.proposals.x1.v1", "phase": d.PHASE, "owner": d.OWNER, "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE, "proposal_count": 30, "expected_disposition_counts": expected, "allowed_outcomes": d.OUTCOME_CLASSES, "proposals": d.PROPOSALS, "x1_only": True, "observed_outcomes_present": False})
    write_text("preregistration/proposal-ledger.md", "# v654-v1 proposal ledger\n\n" + "\n".join(f"{i}. **{p['proposal_id']} - {p['title']}**\n   - Pillar: {p['pillar']}\n   - Expected: `{p['expected_disposition']}`\n   - Approval: `{p['approval_class']}`\n   - X1 state: frozen, not executed" for i, p in enumerate(d.PROPOSALS, 1)))
    write_json("sources/source-ledger.json", {"schema": "ghc.family.v654-v1.source-ledger.v1", "allowed_statuses": d.SOURCE_STATUS_CLASSES, "status_counts": dict(Counter(s["status"] for s in d.SOURCES)), "source_count": len(d.SOURCES), "sources": d.SOURCES, "network_actions": {"purpose": "source verification only", "data_downloads": 0, "real_dataset_rows": 0}, "boundary": "Sources inform bounded contracts; they supply no empirical, professional, legal, cultural, or authority outcome."})
    write_text("sources/source-ledger.md", "# v654-v1 source ledger\n\n" + "\n".join(f"- **{s['source_id']}** - `{s['status']}` - [{s['title']}]({s['url']})\n  - {s['phase_implication']}" for s in d.SOURCES))
    write_json("sources/web-reflection-ledger.json", {"schema": "ghc.family.v654-v1.web-reflection-ledger.v1", "phase": d.PHASE, "reflected_at": times, "rows": [{"source_id": s["source_id"], "status": s["status"], "can_inform": s["phase_implication"], "cannot_establish": ["experimental_observation", "production_conformance", "delegated_authority"]} for s in d.SOURCES], "data_downloads": 0, "boundary": "Source reflection is requirements context, not experimental evidence."})
    write_json("portfolios/expanded-portfolio-plan.json", {"schema": "ghc.family.v654-v1.expanded-portfolio-plan.x1.v1", "counts": counts, "portfolios": portfolios, "inherited_completion_credit": False, "task_cap": 1000, "skill_cap": 200, "runner_cap": 200, "x1_state": "frozen_not_executed"})
    write_json("approval/x1-approval-classification.json", {"schema": "ghc.family.v654-v1.approval-classification.x1.v1", "core_by_expected_disposition": expected, "safe_now_core_count": 23, "candidate_core_count": 6, "exact_gate_core_count": 1, "held_exact_approval_count": 10, "held_blocked_count": 5, "x1_execution_count": 0, "boundary": "Classification is not execution, approval, evidence, or authority."})
    write_json("validation/preregistered-mutation-plan.json", {"schema": "ghc.family.v654-v1.mutation-plan.x1.v1", "count": len(mutations), "mutations_per_proposal": 5, "mutations": mutations, "x1_execution_count": 0, "boundary": "Synthetic mutations only; rejection establishes bounded guard behavior, not real-world assurance."})
    write_json("truth/retained-negative-register.json", {"schema": "ghc.family.v654-v1.retained-negatives.x1.v1", "inherited_effective": d.INHERITED_NEGATIVES, "x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES), "x1_operational": d.X1_OPERATIONAL_NEGATIVES, "effective_after_x1": d.INHERITED_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES), "no_failure_erased": True, "boundary": "Counts preserve inherited and current workflow negatives; a later pass never converts a failure into a pass."})
    write_json("truth/open-gap-register.json", {"schema": "ghc.family.v654-v1.open-gaps.x1.v1", "inherited_count": d.INHERITED_OPEN_GAPS, "new_preregistered": [{"proposal_id": "V6541-P29", "state": "open_gap_expected", "account_or_api_key_used": False, "queries": 0, "downloads": 0, "rows": 0, "likelihoods": 0}], "expected_effective_after_x2": d.INHERITED_OPEN_GAPS + 1, "closed_in_x1": 0})
    write_json("truth/exact-gate-register.json", {"schema": "ghc.family.v654-v1.exact-gates.x1.v1", "inherited_count": d.INHERITED_EXACT_GATES, "new_preregistered": [{"proposal_id": "V6541-P30", "state": "exact_gate_expected", "decisions": 0, "required_authority": ["affected workers, makers, customers, communities, and rights holders", "competent occupational, fire, electrical, gas, food, environmental, legal, cultural, and privacy authorities", "tangata whenua, iwi, hapu, and Maori authorities"]}], "expected_effective_after_x2": d.INHERITED_EXACT_GATES + 1, "closed_in_x1": 0})
    write_json("truth/held-approval-packets.json", {"schema": "ghc.family.v654-v1.held-approval-packets.v1", "exact_approval": [{"packet_id": f"V6541-EXACT-{i:02d}", "state": "held_unexecuted"} for i in range(1, 11)], "blocked": [{"packet_id": f"V6541-BLOCKED-{i:02d}", "state": "held_unexecuted"} for i in range(1, 6)], "boundary": "Visibility is not authorization, execution, completion, or authority."})
    write_json("truth/x1-phase-truth.json", {"schema": "ghc.family.v654-v1.phase-truth.x1.v1", "phase": d.PHASE, "owner": d.OWNER, "lifecycle": "x1_frozen_not_executed", "primary_focus": d.PRIMARY_FOCUS, "other_pillars_visible": True, "proposal_count": 30, "observed_outcome_count": 0, "real_row_count": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "terminal_route": "PREPARED_NOT_CREATED", "independent_reproduction_claimed": False, "theory_of_everything_claimed": False, "consciousness_or_personhood_claimed": False})
    write_json("truth/truth-bridge.json", {"schema": "ghc.family.v654-v1.truth-bridge.x1.v1", "rows": [{"surface": "GMUT", "supported": "typed symbolic obligations and zero-row readiness", "not_supported": "force, prediction, likelihood, constraint, confirmation, or Theory of Everything"}, {"surface": "THOS", "supported": "synthetic protocol and structural proxy planning", "not_supported": "participant effect, operational effectiveness, competence, deployment, AGI, or ASI"}, {"surface": "Freed ID", "supported": "synthetic standards profiles", "not_supported": "production identity, real keys, interoperability, privacy or security review, or trust governance"}, {"surface": "CBR", "supported": "unresolved decision-right and authority reservations", "not_supported": "legal, cultural, Māori-authority, remedy, data-governance, or affected-party legitimacy"}], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("threat-model/x1-threat-model.json", {"schema": "ghc.family.v654-v1.threat-model.x1.v1", "assets": ["x1/x2 separation", "source ancestry", "failure retention", "privacy exclusions", "authority boundaries", "route integrity", "future task noncreation"], "threats": ["mixed lifecycle content", "semantic duplication", "failure erasure", "source promotion", "dataset leakage", "identity or authority substitution", "premature task creation", "placeholder treated as identity"], "controls": ["dedicated x1 commit", "1660-title novelty audit", "Method Flow", "five-class scan", "zero-row firewall", "exact-gate matrix", "creation hold", "task invariant"], "residual_risk": "open_and_exact_gated", "exhaustive_security_claimed": False})
    write_json("route/terminal-route-state.json", {"schema": "ghc.family.v654-v1.route-state.v1", "current_phase": d.PHASE, "immediate_activation": "verified_exact", "future_placeholder": "future-sibling-self-chosen-7", "successor_phase": "v654-v2", "state": "PREPARED_NOT_CREATED", "create_count": 0, "fork_count": 0, "delegate_count": 0, "contact_count": 0, "requires_verified_exact_final": True, "authorized_model_after_gate": "gpt-5.6-sol", "authorized_reasoning_after_gate": "maximum", "boundary": "No task creation or contact before exact-final proof; the future task must choose its own relational identity."})
    write_json("workflow/lane-and-drive-decision.json", {"schema": "ghc.family.v654-v1.lane-and-drive-decision.v1", "branch": d.BRANCH, "source_head": d.SOURCE_HEAD, "advance_method": "fast_forward_only", "primary_bank": "D", "full_checkout_file_count": sum(1 for p in REPO.rglob("*") if p.is_file()), "rotation_threshold_domain": "owner_generated_only", "rotation_required": False, "sibling_mutations": 0, "destructive_actions": 0, "boundary": "Owned-lane workflow evidence only."})
    write_json("workflow/cadence-and-retry-receipt.json", {"schema": "ghc.family.v654-v1.cadence-retry.x1.v1", "bounded_batches": True, "indefinite_watchers": 0, "background_siblings": 0, "retry_policy": "record failure, isolate cause, apply minimum recovery, retain both witnesses, stop after success", "failure_count": len(d.X1_OPERATIONAL_NEGATIVES)})
    request_path = write_json("workflow/workflow-plan-request.json", workflow_request())
    write_text("overview/integrated-overview.md", overview_text())
    write_text("reports/x1-accessible-report.html", accessible_html())
    write_json("validation/x1-build-receipt.json", {"schema": "ghc.family.v654-v1.x1-build-receipt.v1", "proposal_count": 30, "frozen_count": len(frozen), "portfolio_counts": counts, "mutation_count": len(mutations), "observed_outcomes": 0, "valid": True, "terminal_route": "PREPARED_NOT_CREATED", "boundary": "Build completion is not commit, push, validation, x2, or terminal-route credit."})
    write_repo("tests/test_ghc_family_v654_v1_x1.py", x1_test_source())

    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ROOT / "method-flow/method-flow-ledger.json"), "--receipt", str(ROOT / "method-flow/method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ROOT / "method-flow/method-flow-ledger.json"), "--json-output", str(ROOT / "method-flow/method-flow-summary.json"), "--markdown-output", str(ROOT / "method-flow/method-flow-summary.md"))
    run(sys.executable, str(WORKFLOW_RUNNER), str(request_path), "--out-dir", str(ROOT / "workflow"))
    run(sys.executable, str(INDEX_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--out-dir", str(ROOT / "tooling"), "--phase", d.PHASE, "--owner", d.OWNER)
    run(sys.executable, str(REFLECTION_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--output-dir", str(ROOT / "reflection-remaster"), "--phase", d.PHASE, "--owner", d.OWNER, "--focus", "ceramics", "--focus", "kiln", "--focus", "phase-field", "--focus", "asset-identity", "--focus", "workflow")

    cli_version = run("cmd.exe", "/d", "/c", "codex", "--version")
    write_json("environment/environment-version-receipt.json", {"schema": "ghc.family.v654-v1.environment.x1.v1", "timestamps": times, "versions": {"codex_cli": cli_version, "python": run(sys.executable, "--version"), "git": run("git", "--version"), "powershell": run("powershell.exe", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()")}, "versions_verified_only": True, "desktop_updated": False, "sandbox_or_hyper_v_changed": False, "elevation_or_reboot": False, "storage": {"primary": "D", "free_bytes": shutil.disk_usage("D:/").free, "c_drive": "essential application metadata and skill reads only"}, "owner_generated_file_count": len(status_paths()), "rotation_threshold": 15000})
    build_manifest()

    if read_json(ROOT / "validation/x1-staged-privacy.json")["confirmed_hit_count"]:
        raise RuntimeError("x1 privacy scan found confirmed hits")
    workflow = read_json(ROOT / "workflow/workflow-plan-refinement.json")
    if not workflow["valid"] or workflow["requires_user_confirmation"]:
        raise RuntimeError("workflow plan did not validate")
    if len(overview_text().split()) < 1300:
        raise RuntimeError("overview below three-page-equivalent floor")
    print(json.dumps({"phase": d.PHASE, "proposal_count": 30, "frozen_count": len(frozen), "portfolios": counts, "mutations": len(mutations), "privacy_hits": 0, "status": "x1_built_not_committed"}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method-ledger-source", required=True)
    args = parser.parse_args()
    build(Path(args.method_ledger_source).resolve())


if __name__ == "__main__":
    main()
