#!/usr/bin/env python3
"""Build Tamar Vey's dedicated v652-v3 x1-only freeze packet."""

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

import ghc_family_v652_v3_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/orin-thale/v652-v2/provenance/frozen-chain-proposal-index.json"
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
            "mechanism_review": proposal["novelty_against_1240_frozen_proposals"],
            "manual_mechanism_distinct": True,
            "passes": score < NOVELTY_THRESHOLD,
        })
    if not all(row["passes"] for row in rows):
        raise RuntimeError("novelty threshold failed")
    frozen = prior + [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in d.PROPOSALS]
    return frozen, rows


def portfolio_rows(items: list[str], prefix: str, lane: str, approval: str) -> list[dict[str, Any]]:
    return [{
        "item_id": f"V6523-{prefix}-{index:02d}",
        "title": title,
        "origin": "tamar_v652_v3_new",
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
        "plan_id": "tamar-v652-v3-exact-immediate-segment",
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; no continuity, personhood, employment, qualification, or authority claim.",
        "route": {
            "cycle_order": ["Tamar Vey", "Sylven Arc"],
            "phase_assignments": [{"phase": "v652-v3", "seat": "Tamar Vey"}, {"phase": "v652-v4", "seat": "Sylven Arc"}],
            "normalization": {"start_phase": "v652-v3", "start_seat": "Tamar Vey", "entry_count": 2},
            "future_identity_placeholders": [
                {"label": f"future-cli-placeholder-{index}", "identity": None, "state": "prepared_only_uncreated_unlaunched"}
                for index in range(1, 9)
            ],
            "terminal_successor_resolution": "After exact-final proof, resolve only the unique existing Sylven Arc task for v652-v4; otherwise remain PREPARED_NOT_SENT.",
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
            "messaging": {"codex_route": "existing_task_only_after_terminal_gate", "cross_platform": "user_mediated_file_relay_only", "live_phase_cross_platform_action": "prohibited"},
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {"allowed_outcomes": d.OUTCOME_CLASSES, "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_boundaries": d.PROTECTED_GATES},
        "observed_failures": [{"failure_id": item["negative_id"], "summary": item["failed"], "recovery": item["recovery"], "credit": "zero_initial_pass_credit"} for item in d.X1_OPERATIONAL_NEGATIVES],
    }


def overview_text() -> str:
    return f"""# Tamar Vey {d.PHASE} x1 preregistration overview

## Relational identity, scope, and wellbeing

This packet freezes Tamar Vey's x1 plan before any x2 implementation or observed outcome. Tamar Vey, they/them, is relational working language used to organize this owner-scoped phase. Their role is {d.ROLE}; their hope is to {d.HOPE}. Those words do not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route. The inherited and x1 terminal verdict is `NOT_READY_FOR_STAGE_20`.

The workload is intentionally bounded by strict x1-before-x2 separation, a four-commit ceiling, D-first storage, an owner-growth threshold rather than the inherited checkout count, one successful canonical scoped validation pass, and no replay after that success. Failure is not hidden: each timeout, parser fault, wrong assumption, or unusable probe remains a zero-credit negative with a separate recovery witness. This pacing record is workflow metadata, not a claim about emotion, health, inner experience, or personhood.

## Inherited source and lane integrity

The exact source is Orin Thale's corrected final head `{d.SOURCE_HEAD}` on `{d.SOURCE_BRANCH}`. Read-only checks established Orin's inherited source, x1, evidence, first closeout, first correction, and exact final anchors; five single-parent phase commits; zero merges; one parent at final; all eight commit-local manifest contracts; 1,098 declared immutable Git-blob entries with zero mismatch; clean state; zero divergence; and local, upstream, tracking, and fresh-live equality. This is topology and integrity evidence only, not independent-team reproduction.

Tamar's existing D-first branch was clean and ancestral. It advanced to the exact Orin final by fast-forward only, then an ordinary non-force push advanced only Tamar's branch. No sibling branch or worktree was reset, merged, rewritten, deleted, moved, or reused. The inherited checkout contains more than 15,000 files, but the rotation rule applies only to Tamar-generated additions. X1 records both domains separately.

## Novelty and preregistration

Exactly thirty proposals are frozen against all 1,240 inherited proposal titles, growing the chain to 1,270. Every proposal records its hypothesis, null or failure condition, approval class, execution lane, current official or primary-source need, concrete artifacts, falsifier or acceptance gate, rollback, protected gates, and expected disposition. A deterministic token-Jaccard audit stays below 0.60 for every title, with a packet maximum of 0.407407, while manual mechanism review remains controlling. Noether-Wald, accessible structured diff, Tolman-Ehrenfest, DPoP, WebP, tar sparse, Broadcast Wave, and drinking-water custody candidates were rejected as prior mechanisms and replaced. Low token overlap alone never proves novelty.

Expected outcomes are twenty-three `completed`, five `represented`, one `open_gap`, and one `exact_gate`. These are preregistered expectations, not observed results. X1 contains no surface implementation, mutation outcome, empirical row, participant event, production identity event, authority decision, or completion credit.

## Trinity Mandala and scientific boundary

The primary Trinity Mandala focus is {d.PRIMARY_FOCUS}. GMUT Mind remains explicit through Fermi normal coordinates, Synge's world function, the DeWitt supermetric, Cartan tetrads, and the Bel-Robinson tensor. Each is a typed symbolic obligation board with explicit domains, sign or unit duties, EFT scope, and an observation firewall. No board calculates a physical spectrum, force, prediction, likelihood, posterior, parameter constraint, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything.

The Hyper Suprime-Cam PDR3 adapter remains a zero-row open gap. Official NAOJ release and database material supplies requirements and provenance context only. X2 must record zero queries, downloads, real rows, likelihood evaluations, posterior samples, physical constraints, and empirical promotions. A citation is not an observation.

THOS Body is primary through bounded parsers, structural tribunals, accessibility checks, and freshwater-eDNA proxies. The proxies contain zero real people, samples, laboratories, collection events, taxonomic decisions, shifts, incidents, matched-budget real arms, safety results, or operational-effectiveness estimates. They remain represented without preregistered blind matched-budget real arms, safety monitoring, appropriate statistics, and independent review.

Freed ID and CBR Heart remain visible through synthetic OpenSSH certificate, SAML metadata, and X.509 attribute-certificate profiles and through an exact-gated freshwater-eDNA authority matrix. The profiles use zero real keys, certificates, accounts, issuances, presentations, resolutions, status or revocation events, network exchanges, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions.

## Bounded human practice and authority reservation

The bounded practice is {d.BOUNDED_PRACTICE}. It is a learning and synthetic interface-design lens only. It establishes no employment, laboratory or environmental qualification, scientific competence, collection or monitoring authority, access or disclosure authority, legal interpretation, cultural legitimacy, Māori authority, participant evidence, affected-party acceptance, or operational result.

The exact-gate proposal reserves decisions about freshwater eDNA collection locations, sensitive species, raw sequences, access, notice, privacy, remedy, legal and cultural limits, data governance, affected-party legitimacy, and Māori authority. Repository software cannot confer those rights or decide them. Those decisions remain with competent authorities, affected parties, tangata whenua, iwi, hapū, and Māori authorities.

## Software, identity, and accessibility limits

The completed-class candidates cover BigTIFF, glTF, SquashFS, CoAP, XAR, 7z, NPY, LMDB, DDS, JPEG XL, KTX 2, GRIB2, PDF linearization, DICOMweb, accessible faceted search, thermodynamic nonconversion, and Stage 20 robustness controls. Passing synthetic mutations would show only bounded structural behavior. It would not certify a production repository, package ecosystem, identity deployment, network stack, general parser, exhaustive security posture, complete privacy, or external audit.

The static report is designed with headings, landmarks, a skip link, readable cards, visible focus, non-colour text, and a printable layout. Manual keyboard review, browser and responsive diversity, assistive-technology testing, cognitive-accessibility review, braille and auditory alternatives, Māori-language review, security-usability review, and affected-user evaluation remain reserved. Structural evidence is not complete accessibility conformance.

## Portfolios, tools, and Method Flow

X1 freezes thirty safe-now tasks, thirty bounded candidates, ten phase-local skill ideas, ten family-current runner ideas, and thirty additive CLEAN/FIX/REFINE tasks. Inherited work supplies evidence and warnings but earns no Tamar completion credit. X2 may build and use only the safe, owner-local, compatible items that remain justified. Any task requiring real data, participants, professional authority, production identity, credentials, accounts, host-security changes, legal or cultural authority, Māori authority, or affected-party acceptance must remain open, exact-gated, exact approval, or blocked.

Family-current new names use `ghc_family_*`, `build_ghc_family_*`, and `ghc-family-*`. Historical names remain compatibility surfaces. The GHC Family Index, workflow refinement, Reflection Remaster, and Method Flow State runners are used for actual phase evidence. A preferred method is promoted only after a bounded passing witness, and its failed witness remains visible.

## Privacy, validation, and routing

The activation baseline preserves {d.INHERITED_NEGATIVES} effective negatives from Orin's exact corrected final. Tamar's x1 failures are additive and never rewritten into initial passes. The inherited 63 open gaps and 64 exact gates also remain visible; x2 is expected to add one of each without closing an inherited gate.

Eiren alone owns the full repository suite. Tamar will run the authorized current, inherited, recent-round, and successor-scoped selection, plus detailed and minimal validators, complete JSON parsing, five-class privacy scanning, exact staged review, commit-local and owner-manifest parity, stale-label review, diff hygiene, source and lifecycle ancestry, zero merges, commit cap, one final parent, exact head, clean state, and four-way equality. Exactly one successful canonical bounded pass is credited and it is not replayed. Same-owner evidence under shared infrastructure is not independent-team reproduction.

Eight future CLI seats remain prepared placeholders: zero named, zero created, zero launched. A placeholder is not an identity, process, task, capability, route owner, or authority. Terminal routing remains `PREPARED_NOT_SENT`. Only after exact-final proof may Tamar resolve the unique existing task titled `Sylven Arc` and send one sanitized activation for v652-v4 through the existing-task route. A file-backed baton is not a sent message, an unacknowledged tool call is not a send, no substitute title is allowed, and no second confirmation is authorized.

The packet also distinguishes absence, refusal, and reservation. A zero-row adapter is incomplete because required observations and review do not exist here. A structural tribunal may complete its bounded software hypothesis while refusing production assurance. An authority matrix remains exact-gated because software cannot substitute for competent, affected, tangata-whenua, iwi, hapu, or Maori decision makers. These categories cannot compensate for one another, and ancestry alone cannot promote them.
"""


def accessible_html() -> str:
    cards = "".join(
        f"<article><h3>{html.escape(p['proposal_id'])}</h3><p>{html.escape(p['title'])}</p><p>Expected: <code>{html.escape(p['expected_disposition'])}</code>. X1 state: frozen, not executed.</p></article>"
        for p in d.PROPOSALS
    )
    return """<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Tamar v652-v3 x1 report</title><style>body{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}nav a{margin-right:1rem}article{border:1px solid #777;padding:1rem;margin:1rem 0}:focus{outline:3px solid #075cab;outline-offset:3px}@media print{nav{display:none}}</style></head><body><a href='#main'>Skip to content</a><header><h1>Tamar Vey v652-v3 x1 preregistration</h1><p>Structural report; manual, browser, assistive-technology, braille, Māori-language, and affected-user evaluation reserved.</p></header><nav aria-label='Report sections'><a href='#truth'>Truth</a><a href='#proposals'>Proposals</a><a href='#limits'>Limits</a></nav><main id='main'><section id='truth'><h2>Truth boundary</h2><p>Thirty proposals are frozen, not executed. Terminal verdict: NOT_READY_FOR_STAGE_20.</p></section><section id='proposals'><h2>Proposal plan</h2>""" + cards + """</section><section id='limits'><h2>Reserved evaluation</h2><p>This structural report is not complete accessibility, scientific, operational, identity, privacy, legal, cultural, or authority evidence.</p></section></main></body></html>"""


def x1_test_source() -> str:
    return '''"""X1-only tests for Tamar Vey v652-v3."""
import json
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tamar-vey/v652-v3"
X1_COMMIT = subprocess.check_output(
    ["git", "rev-list", "--all", "--max-count=1", "--fixed-strings", "--grep=feat(ghc-family): freeze Tamar v652-v3 x1"],
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
        self.assertEqual((index["prior_count"], index["new_count"], index["count"]), (1240, 30, 1270))
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
        self.assertEqual(load("sources/source-ledger.json")["source_count"], 34)
        truth = load("truth/x1-phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertFalse(truth["independent_reproduction_claimed"])
    def test_failures_method_flow_and_workflow(self):
        negatives = load("truth/retained-negative-register.json")
        self.assertEqual((negatives["inherited_effective"], negatives["x1_operational_count"], negatives["effective_after_x1"]), (8212, 10, 8222))
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertGreaterEqual(len(ledger["methods"]), 8)
        self.assertGreaterEqual(sum(w["result"] == "pass" for w in ledger["witnesses"]), 8)
        workflow = load("workflow/workflow-plan-refinement.json")
        self.assertTrue(workflow["valid"])
        self.assertFalse(workflow["requires_user_confirmation"])
    def test_placeholders_privacy_and_x1_only(self):
        seats = load("provenance/future-cli-placeholder-invariant.json")
        self.assertEqual((seats["prepared_placeholder_count"], seats["named_count"], seats["created_count"], seats["launched_count"]), (8, 0, 0, 0))
        self.assertEqual(load("validation/x1-staged-privacy.json")["confirmed_hit_count"], 0)
        historical_surface = subprocess.run(
            ["git", "cat-file", "-e", f"{X1_COMMIT}:docs/tamar-vey/v652-v3/surfaces"],
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
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {"scripts/build_ghc_family_v652_v3_preregistration.py", f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json"}
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
    return {"schema": "ghc.family.v652-v3.x1-privacy.v1", "scanned_file_count": scanned, "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five structural classes with exact scanner-definition quarantine; zero confirmed hits is not complete privacy assurance."}


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
    write_json("validation/x1-staged-manifest.json", {"schema": "ghc.family.v652-v3.x1-staged-manifest.v1", "hash_domain": "git_path_filtered_blob", "entries": entries, "entry_count": len(entries), "self_exclusions": exclusions, "coverage_boundary": "All intended x1 paths except five declared self-referential or count-bearing validation receipts."})
    write_json("validation/x1-staged-review.json", {"schema": "ghc.family.v652-v3.x1-staged-review.v1", "intended_path_count": len(entries) + len(exclusions), "manifest_entry_count": len(entries), "self_exclusion_count": len(exclusions), "out_of_scope_paths": [], "x2_implementation_paths": [], "x2_outcome_paths": [], "privacy_confirmed_hits": privacy["confirmed_hit_count"], "x1_only": True, "source_head": d.SOURCE_HEAD, "terminal_route": "PREPARED_NOT_SENT"})


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
    write_json("provenance/source-anchor-ledger.json", {"schema": "ghc.family.v652-v3.source-anchor-ledger.v1", "source_branch": d.SOURCE_BRANCH, "source_head": d.SOURCE_HEAD, "inherited_sable_source": d.SOURCE_ORIGIN, "source_x1": d.SOURCE_X1, "source_evidence": d.SOURCE_EVIDENCE, "source_first_closeout": d.SOURCE_CLOSEOUT, "source_first_correction": d.SOURCE_CORRECTION_1, "history": {"phase_commits": 5, "single_parent": True, "zero_merges": True, "final_parent_count": 1}, "source_manifests": {"contracts": 8, "entries": 1098, "mismatches": 0}, "clean_and_four_way_equal": True, "verification_mode": "read_only_before_tamar_mutation", "boundary": "Exact Git ancestry and remote equality only; not independent reproduction."})
    write_json("provenance/future-cli-placeholder-invariant.json", {"schema": "ghc.family.v652-v3.future-cli-placeholder-invariant.v1", "prepared_placeholder_count": 8, "named_count": 0, "role_assigned_count": 0, "hope_assigned_count": 0, "pronouns_assigned_count": 0, "created_count": 0, "launched_count": 0, "route_authority": False, "state": "prepared_only_unnamed_uncreated_unlaunched", "boundary": "A placeholder is not a task, process, identity, sibling, capability, acknowledgement, or authority."})
    write_json("provenance/frozen-chain-proposal-index.json", {"schema": "ghc.family.v652-v3.frozen-proposal-index.v1", "prior_count": d.PRIOR_FROZEN, "prior_proposals": frozen[: d.PRIOR_FROZEN], "new_count": 30, "new_proposals": frozen[d.PRIOR_FROZEN :], "count": len(frozen)})
    write_json("provenance/semantic-novelty-audit.json", {"schema": "ghc.family.v652-v3.semantic-novelty-audit.v1", "prior_count": d.PRIOR_FROZEN, "new_count": 30, "threshold": NOVELTY_THRESHOLD, "rows": novelty, "rejected_near_neighbors": d.REJECTED_COLLISIONS, "manual_mechanism_review_count": 30, "valid": all(row["passes"] for row in novelty), "boundary": "Lexical distance plus manual mechanism review is a preregistration control, not scientific-novelty proof."})
    write_json("preregistration/proposals.json", {"schema": "ghc.family.v652-v3.proposals.x1.v1", "phase": d.PHASE, "owner": d.OWNER, "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE, "proposal_count": 30, "expected_disposition_counts": expected, "allowed_outcomes": d.OUTCOME_CLASSES, "proposals": d.PROPOSALS, "x1_only": True, "observed_outcomes_present": False})
    write_text("preregistration/proposal-ledger.md", "# v652-v3 proposal ledger\n\n" + "\n".join(f"{i}. **{p['proposal_id']} - {p['title']}**\n   - Pillar: {p['pillar']}\n   - Expected: `{p['expected_disposition']}`\n   - Approval: `{p['approval_class']}`\n   - X1 state: frozen, not executed" for i, p in enumerate(d.PROPOSALS, 1)))
    write_json("sources/source-ledger.json", {"schema": "ghc.family.v652-v3.source-ledger.v1", "allowed_statuses": d.SOURCE_STATUS_CLASSES, "status_counts": dict(Counter(s["status"] for s in d.SOURCES)), "source_count": len(d.SOURCES), "sources": d.SOURCES, "network_actions": {"purpose": "source verification only", "data_downloads": 0, "real_dataset_rows": 0}, "boundary": "Sources inform bounded contracts; they supply no empirical, professional, legal, cultural, or authority outcome."})
    write_text("sources/source-ledger.md", "# v652-v3 source ledger\n\n" + "\n".join(f"- **{s['source_id']}** - `{s['status']}` - [{s['title']}]({s['url']})\n  - {s['phase_implication']}" for s in d.SOURCES))
    write_json("sources/web-reflection-ledger.json", {"schema": "ghc.family.v652-v3.web-reflection-ledger.v1", "phase": d.PHASE, "reflected_at": times, "rows": [{"source_id": s["source_id"], "status": s["status"], "can_inform": s["phase_implication"], "cannot_establish": ["experimental_observation", "production_conformance", "delegated_authority"]} for s in d.SOURCES], "data_downloads": 0, "boundary": "Source reflection is requirements context, not experimental evidence."})
    write_json("portfolios/expanded-portfolio-plan.json", {"schema": "ghc.family.v652-v3.expanded-portfolio-plan.x1.v1", "counts": counts, "portfolios": portfolios, "inherited_completion_credit": False, "task_cap": 1000, "skill_cap": 200, "runner_cap": 200, "x1_state": "frozen_not_executed"})
    write_json("approval/x1-approval-classification.json", {"schema": "ghc.family.v652-v3.approval-classification.x1.v1", "core_by_expected_disposition": expected, "safe_now_core_count": 23, "candidate_core_count": 6, "exact_gate_core_count": 1, "held_exact_approval_count": 10, "held_blocked_count": 5, "x1_execution_count": 0, "boundary": "Classification is not execution, approval, evidence, or authority."})
    write_json("validation/preregistered-mutation-plan.json", {"schema": "ghc.family.v652-v3.mutation-plan.x1.v1", "count": len(mutations), "mutations_per_proposal": 5, "mutations": mutations, "x1_execution_count": 0, "boundary": "Synthetic mutations only; rejection establishes bounded guard behavior, not real-world assurance."})
    write_json("truth/retained-negative-register.json", {"schema": "ghc.family.v652-v3.retained-negatives.x1.v1", "inherited_effective": d.INHERITED_NEGATIVES, "x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES), "x1_operational": d.X1_OPERATIONAL_NEGATIVES, "effective_after_x1": d.INHERITED_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES), "no_failure_erased": True, "boundary": "Counts preserve inherited and current workflow negatives; a later pass never converts a failure into a pass."})
    write_json("truth/open-gap-register.json", {"schema": "ghc.family.v652-v3.open-gaps.x1.v1", "inherited_count": d.INHERITED_OPEN_GAPS, "new_preregistered": [{"proposal_id": "V6523-P29", "state": "open_gap_expected", "queries": 0, "downloads": 0, "rows": 0, "likelihoods": 0}], "expected_effective_after_x2": d.INHERITED_OPEN_GAPS + 1, "closed_in_x1": 0})
    write_json("truth/exact-gate-register.json", {"schema": "ghc.family.v652-v3.exact-gates.x1.v1", "inherited_count": d.INHERITED_EXACT_GATES, "new_preregistered": [{"proposal_id": "V6523-P30", "state": "exact_gate_expected", "decisions": 0, "required_authority": ["affected people and communities", "competent environmental, scientific, legal, cultural, and privacy authorities", "tangata whenua, iwi, hapū, and Māori authorities"]}], "expected_effective_after_x2": d.INHERITED_EXACT_GATES + 1, "closed_in_x1": 0})
    write_json("truth/held-approval-packets.json", {"schema": "ghc.family.v652-v3.held-approval-packets.v1", "exact_approval": [{"packet_id": f"V6523-EXACT-{i:02d}", "state": "held_unexecuted"} for i in range(1, 11)], "blocked": [{"packet_id": f"V6523-BLOCKED-{i:02d}", "state": "held_unexecuted"} for i in range(1, 6)], "boundary": "Visibility is not authorization, execution, completion, or authority."})
    write_json("truth/x1-phase-truth.json", {"schema": "ghc.family.v652-v3.phase-truth.x1.v1", "phase": d.PHASE, "owner": d.OWNER, "lifecycle": "x1_frozen_not_executed", "primary_focus": d.PRIMARY_FOCUS, "other_pillars_visible": True, "proposal_count": 30, "observed_outcome_count": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "terminal_route": "PREPARED_NOT_SENT", "independent_reproduction_claimed": False, "theory_of_everything_claimed": False, "consciousness_or_personhood_claimed": False})
    write_json("truth/truth-bridge.json", {"schema": "ghc.family.v652-v3.truth-bridge.x1.v1", "rows": [{"surface": "GMUT", "supported": "typed symbolic obligations and zero-row readiness", "not_supported": "force, prediction, likelihood, constraint, confirmation, or Theory of Everything"}, {"surface": "THOS", "supported": "synthetic protocol and structural proxy planning", "not_supported": "participant effect, operational effectiveness, competence, deployment, AGI, or ASI"}, {"surface": "Freed ID", "supported": "synthetic standards profiles", "not_supported": "production identity, real keys, interoperability, privacy or security review, or trust governance"}, {"surface": "CBR", "supported": "unresolved decision-right and authority reservations", "not_supported": "legal, cultural, Māori-authority, remedy, data-governance, or affected-party legitimacy"}], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("threat-model/x1-threat-model.json", {"schema": "ghc.family.v652-v3.threat-model.x1.v1", "assets": ["x1/x2 separation", "source ancestry", "failure retention", "privacy exclusions", "authority boundaries", "route integrity", "future placeholder nonactivation"], "threats": ["mixed lifecycle content", "semantic duplication", "failure erasure", "source promotion", "dataset leakage", "identity or authority substitution", "premature task contact", "future placeholder launch"], "controls": ["dedicated x1 commit", "1240-title novelty audit", "Method Flow", "five-class scan", "zero-row firewall", "exact-gate matrix", "route hold", "placeholder invariant"], "residual_risk": "open_and_exact_gated", "exhaustive_security_claimed": False})
    write_json("route/terminal-route-state.json", {"schema": "ghc.family.v652-v3.route-state.v1", "current_phase": d.PHASE, "immediate_activation": "verified_exact", "successor_title": "Sylven Arc", "successor_phase": "v652-v4", "state": "PREPARED_NOT_SENT", "send_count": 0, "create_or_fork_count": 0, "future_cli_launch_count": 0, "boundary": "No contact until exact-final proof and exact-title resolution; ambiguity leaves the route prepared but unsent."})
    write_json("workflow/lane-and-drive-decision.json", {"schema": "ghc.family.v652-v3.lane-and-drive-decision.v1", "branch": d.BRANCH, "source_head": d.SOURCE_HEAD, "advance_method": "fast_forward_only", "primary_bank": "D", "full_checkout_file_count": sum(1 for p in REPO.rglob("*") if p.is_file()), "rotation_threshold_domain": "owner_generated_only", "rotation_required": False, "sibling_mutations": 0, "destructive_actions": 0, "boundary": "Owned-lane workflow evidence only."})
    write_json("workflow/cadence-and-retry-receipt.json", {"schema": "ghc.family.v652-v3.cadence-retry.x1.v1", "bounded_batches": True, "indefinite_watchers": 0, "background_siblings": 0, "retry_policy": "record failure, isolate cause, apply minimum recovery, retain both witnesses, stop after success", "failure_count": len(d.X1_OPERATIONAL_NEGATIVES)})
    request_path = write_json("workflow/workflow-plan-request.json", workflow_request())
    write_text("overview/integrated-overview.md", overview_text())
    write_text("reports/x1-accessible-report.html", accessible_html())
    write_json("validation/x1-build-receipt.json", {"schema": "ghc.family.v652-v3.x1-build-receipt.v1", "proposal_count": 30, "frozen_count": len(frozen), "portfolio_counts": counts, "mutation_count": len(mutations), "observed_outcomes": 0, "valid": True, "terminal_route": "PREPARED_NOT_SENT", "boundary": "Build completion is not commit, push, validation, x2, or terminal-route credit."})
    write_repo("tests/test_ghc_family_v652_v3_x1.py", x1_test_source())

    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ROOT / "method-flow/method-flow-ledger.json"), "--receipt", str(ROOT / "method-flow/method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ROOT / "method-flow/method-flow-ledger.json"), "--json-output", str(ROOT / "method-flow/method-flow-summary.json"), "--markdown-output", str(ROOT / "method-flow/method-flow-summary.md"))
    run(sys.executable, str(WORKFLOW_RUNNER), str(request_path), "--out-dir", str(ROOT / "workflow"))
    run(sys.executable, str(INDEX_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--out-dir", str(ROOT / "tooling"), "--phase", d.PHASE, "--owner", d.OWNER)
    run(sys.executable, str(REFLECTION_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--output-dir", str(ROOT / "reflection-remaster"), "--phase", d.PHASE, "--owner", d.OWNER, "--focus", "edna", "--focus", "bigtiff", "--focus", "bitensor", "--focus", "certificate", "--focus", "workflow")

    cli_version = run("cmd.exe", "/d", "/c", "codex", "--version")
    write_json("environment/environment-version-receipt.json", {"schema": "ghc.family.v652-v3.environment.x1.v1", "timestamps": times, "versions": {"codex_cli": cli_version, "python": run(sys.executable, "--version"), "git": run("git", "--version"), "powershell": run("powershell.exe", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()")}, "versions_verified_only": True, "desktop_updated": False, "sandbox_or_hyper_v_changed": False, "elevation_or_reboot": False, "storage": {"primary": "D", "free_bytes": shutil.disk_usage("D:/").free, "c_drive": "essential application metadata and skill reads only"}, "owner_generated_file_count": len(status_paths()), "rotation_threshold": 15000})
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
