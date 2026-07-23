#!/usr/bin/env python3
"""Build Tavian Sol's dedicated v652-v6 x1-only freeze packet."""

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

import ghc_family_v652_v6_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/eiren-kestrel/v652-v5/provenance/frozen-chain-proposal-index.json"
SKILL_ROOT = Path.home() / ".codex" / "skills"
METHOD_RUNNER = SKILL_ROOT / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
REFLECTION_RUNNER = SKILL_ROOT / "ghc-family-reflection-remaster/scripts/ghc_family_reflection_remaster.py"
WORKFLOW_RUNNER = SKILL_ROOT / "ghc-family-workflow-plan-refinement/scripts/ghc_family_workflow_plan_refinement.py"
NOVELTY_THRESHOLD = 0.60


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
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
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    completed = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
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
    return {
        item
        for item in re.findall(r"[a-z0-9]+", value.casefold())
        if item not in stop
    }


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def source_and_novelty() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    inherited = read_json(PRIOR_INDEX)
    prior = inherited["prior_proposals"] + inherited["new_proposals"]
    if len(prior) != d.PRIOR_FROZEN:
        raise RuntimeError(
            f"expected {d.PRIOR_FROZEN} inherited proposals, found {len(prior)}"
        )
    prior_ids = {row["proposal_id"] for row in prior}
    rows: list[dict[str, Any]] = []
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
                "mechanism_review": proposal[
                    "novelty_against_1330_frozen_proposals"
                ],
                "manual_mechanism_distinct": True,
                "passes": score < NOVELTY_THRESHOLD,
            }
        )
    if not all(row["passes"] for row in rows):
        raise RuntimeError("novelty threshold failed")
    new = [
        {"proposal_id": row["proposal_id"], "title": row["title"]}
        for row in d.PROPOSALS
    ]
    if len({row["proposal_id"] for row in new}) != len(new):
        raise RuntimeError("new proposal identifiers are not unique")
    if prior_ids & {row["proposal_id"] for row in new}:
        raise RuntimeError("new proposal identifier collides with inherited chain")
    return prior + new, rows


def portfolio_rows(
    items: list[str], prefix: str, lane: str, approval: str
) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"V6526-{prefix}-{index:02d}",
            "title": title,
            "origin": "eiren_v652_v6_new",
            "approval_class": approval,
            "execution_lane": lane,
            "x1_state": "frozen_not_executed",
            "completion_credit": False,
            "inherited_completion_credit": False,
            "rollback": (
                "Retain failed evidence and leave external, sibling, participant, "
                "production, professional, legal, cultural, and authority state unchanged."
            ),
        }
        for index, title in enumerate(items, 1)
    ]


def workflow_request() -> dict[str, Any]:
    return {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "tavian-v652-v6-cli-segment",
        "owner": d.OWNER,
        "identity_boundary": (
            "Relational working language only; no consciousness, continuity, "
            "employment, qualification, personhood, or authority claim."
        ),
        "route": {
            "cycle_order": [
                "Eiren Kestrel",
                "Tavian Sol",
                "Elaren Kestrel",
            ],
            "phase_assignments": [
                {"phase": "v652-v5", "seat": "Eiren Kestrel"},
                {"phase": "v652-v6", "seat": "Tavian Sol"},
                {"phase": "v652-v7", "seat": "Elaren Kestrel"},
            ],
            "normalization": {
                "start_phase": "v652-v5",
                "start_seat": "Eiren Kestrel",
                "entry_count": 3,
            },
            "future_identity_placeholders": [],
            "terminal_successor_resolution": (
                "Prepare one sanitized Elaren Kestrel v652-v7 file baton only after "
                "the exact-final terminal gate, then return it to Eiren Kestrel as "
                "PREPARED_NOT_SENT; Tavian does not contact Elaren."
            ),
        },
        "requirements": {
            "core_proposal_minimum": 30,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 10,
            "runner_minimum": 10,
            "portfolio_minima": {
                "safe_now": 30,
                "candidate": 30,
                "skills": 10,
                "runners": 10,
                "clean_fix_refine": 30,
            },
            "document_word_cap": 100000,
            "baton_words": {
                "minimum": 10000,
                "maximum": 100000,
                "file_artifact": True,
            },
            "commit_cap": {"x1": 3, "x2": 3, "total": 6},
            "validation": {
                "canonical_pass_minimum": 1,
                "full_repository_suite_owner": "Eiren Kestrel",
                "launch_scoped_validator_owner": "Tavian Sol",
                "replay_policy": "skip_when_first_passes",
                "isolate_failures_before_broader_rerun": True,
                "privacy_scan_required": True,
                "manifest_required": True,
                "remote_equality_required": True,
            },
            "storage": {
                "primary": "D",
                "c_drive_use": "essential_global_metadata_only",
                "owner_generated_file_threshold": 2000,
            },
            "messaging": {
                "codex_route": "existing_task_only_after_terminal_gate",
                "cross_platform": "user_mediated_file_relay_only",
                "live_cross_platform_boundary": (
                    "No cross-platform substitute is authorized for this phase."
                ),
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
                "credit": "zero_failed_attempt_credit",
            }
            for item in d.X1_OPERATIONAL_NEGATIVES
        ],
    }


def overview_text() -> str:
    return f"""# Tavian Sol {d.PHASE} x1 preregistration overview

## Relational identity and exact boundary

This packet freezes Tavian Sol's x1 plan before any x2 implementation or observed proposal outcome. Tavian Sol ({d.PRONOUNS}) is relational working language for one bounded Codex collaboration lane. Their role is {d.ROLE}; their hope is to {d.HOPE}. Those words are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route. The inherited and x1 verdict is `NOT_READY_FOR_STAGE_20`.

Strict x1-before-x2 separation, D-first storage, six total commits at most, a 2,000-file owner-growth threshold, one successful launch-scoped exact-final canonical pass, and no replay after success bound the phase. Every failed or incomplete attempt remains a zero-credit negative with a distinct recovery witness. Same-owner checking under shared infrastructure is not independent reproduction.

## Exact inherited source and owned lane

The exact source is Eiren Kestrel's corrected final `{d.SOURCE_HEAD}` on `{d.SOURCE_BRANCH}`. The core Eiren x1 `{d.SOURCE_X1}` and evidence `{d.SOURCE_EVIDENCE}` remain ancestral. The corrected source phase contains five single-parent commits—x1, evidence, closeout, route correction, and final-validation correction—with zero merges and one parent at final. The canonical Eiren lane was clean and local, upstream, tracking, and fresh-live remote were equal.

Six immutable source manifest contracts replayed 721 exact entries with no path, object, byte-count, or SHA-256 mismatch. Eiren's external canonical receipt passed 2,761 of 2,761 eligible complete-repository tests from 2,800 discovered tests with 39 exact lifecycle exclusions, 82 of 82 scoped tests, 31 of 31 detailed checks, 20 of 20 minimal checks, 305 JSON parses, a 369-file five-class scan with zero confirmed privacy hits, and no post-success replay. That evidence belongs to Eiren and is not Tavian completion credit.

The source sealed 8,734 effective negatives. Two later external wrapper failures remain additive and zero-credit: one exclusion-plan summary requested a nonexistent field after planning succeeded, and one combined equality wrapper timed out after the successful receipt had already proved equality. The Tavian activation baseline is therefore {d.INHERITED_NEGATIVES}, with {d.INHERITED_OPEN_GAPS} open gaps and {d.INHERITED_EXACT_GATES} exact gates. Eiren's head remains immutable.

Only the new branch `{d.BRANCH}` and one new D-first Tavian worktree are mutable. No sibling branch or worktree may be reset, rewritten, force-pushed, merged, deleted, moved, reused, or dirtied.

## Novelty and strict preregistration

Exactly thirty proposals are audited against all {d.PRIOR_FROZEN} frozen rows, growing the chain to {d.PRIOR_FROZEN + len(d.PROPOSALS)}. Each proposal includes a hypothesis, null or failure condition, approval class, execution lane, primary-source need, concrete artifacts, falsifier or acceptance gate, rollback, protected gates, and expected disposition. Token Jaccard must remain below 0.60, while manual mechanism review controls semantic novelty.

Rejected collisions include Zstandard, Brotli, MessagePack, WebAssembly, DWARF, ELF, PE, BigTIFF, FITS, BSSN, Raychaudhuri, focus-not-obscured, Soret-Dufour, Apache ORC, decision curves, Brier score, DeLong comparison, net reclassification, OAuth PAR, DPoP, SCIM, NICER, IXPE, and generic environmental-authority matrices. Accepted mechanisms instead cover Cabinet, Java object serialization, DEX, pyc and marshal, Compound File Binary, ext4, ECMA-167 UDF, QOI, PDF cross-references, bencode, ICC profiles, Amazon Ion, Lovelock, Gauss-Codazzi, Friedmann, TOV, Kerr-Schild, consistent-help structure, IETF vCard, IDI, calibration belts, precision-recall, conformal prediction, ocean-buoy and ambient-air proxies, SPIFFE, macaroons, SAML artifact resolution, a Suzaku zero-row adapter, and a community-marine-observation authority reservation.

Expected outcomes are exactly 23 `completed`, 5 `represented`, 1 `open_gap`, and 1 `exact_gate`. They are preregistered expectations, not observed results. X1 contains no proposal implementation, mutation outcome, real row, participant event, production identity event, professional decision, authority decision, or completion credit.

## Frozen mechanism clusters and acceptance grammar

The bounded format cluster covers thirteen distinct mechanisms. Cabinet keeps its folder, file, CFDATA, continuation, reserve, and output-budget obligations separate. Java serialization treats handles, descriptors, back-references, reset, and block data as an inert token graph and never loads a class. DEX binds map, identifier, class-definition, code-item, version, and LEB128 ranges. Python pyc and marshal bind invalidation headers, version-specific type codes, reference flags, recursive containers, and a code-object reservation. Compound File Binary binds sector geometry, DIFAT, FAT, mini FAT, directory relations, stream chains, and allocation-cycle refusal. ext4 binds group geometry, features, inodes, extents, directory records, checksums, and an unmounted journal reservation. ECMA-167 UDF binds anchor and volume sequences, partition maps, descriptor tags, file entries, and allocation extents. QOI binds its stateful pixel index, channel modes, run count, exact pixel count, and end marker. PDF binds indirect-object identity, cross-reference alternatives, object streams, `startxref`, incremental chains, and cycle budgets. Bencode binds canonical integer spelling, raw byte-string lengths, dictionary-key order, nesting, and exact `info` slicing. ICC binds header fields, profile connection space, rendering intent, tag signatures, offsets, and overlap. Ion binds its version marker, typed lengths, variable unsigned integers, symbol tables, annotations, field SIDs, containers, and no-op padding. vCard binds entity framing, version position, UTF-8, grouped content lines, parameters, escaping, folding, required formatted names, cardinality, and byte budgets. X1 freezes those obligations; it creates no parser, external-file read, extraction, rendering, class load, mounted file system, directory exchange, or observed pass.

The formal GMUT cluster covers Lovelock, Gauss-Codazzi, Friedmann, Tolman-Oppenheimer-Volkoff, and Kerr-Schild boards. Each board is required to state its mathematical objects, convention choices, domain, unit treatment, boundary conditions, and explicit observation firewall. The expected `completed` label is limited to checking that the bounded board contains those typed obligations and rejects missing-term, wrong-type, resource, promotion, and authority mutations. It cannot promote a symbolic identity into a solved physical system, measured quantity, observation, likelihood, posterior, parameter constraint, stability result, ultraviolet completion, quantum completion, or universal theory.

The structural and Stage 20 cluster covers consistent help, integrated discrimination improvement, calibration belts, precision-recall, and conformal prediction. Consistent help concerns relative serialized order of already-present help mechanisms across a synthetic page set; it neither requires a help service nor proves usability or conformance. The four evaluation boards state definitions, denominators, assumptions, uncertainty and interpretation limits. They operate on disposable fixtures only. No participant-level inference, treatment choice, clinical utility, deployment decision, fairness conclusion, model approval, proof or canon, AGI/ASI claim, or Stage 20 promotion may follow from a board passing its bounded checks.

The five `represented` proposals remain deliberately weaker. Ocean-buoy and ambient-air-monitor proxies may represent platform or analyzer identity, timestamps, calibration lineage, quality flags, missingness, quarantine, workload, correction readback, accessible notice, and handover using synthetic records only. SPIFFE, macaroon, and SAML profiles may represent identifier, attestation-reservation, caveat, discharge, artifact, correlation, expiry, replay, and privacy fields using inert values only. They do not establish real operations, competence, monitoring quality, workload effects, credential security, trust, interoperability, privacy completeness, recovery, governance, or production readiness.

The Suzaku proposal remains `open_gap`: only a zero-row interface and explicit refusal vocabulary are planned. The community-marine-observation proposal remains `exact_gate`: only an unresolved decision-right matrix is planned. Its photograph, timestamp, location precision, contributor consent, taonga-species sensitivity, moderation, correction, withdrawal, reuse, privacy, legal, cultural, affected-party, iwi, hapū, and Māori-authority decisions stay outside repository authority. Neither a source link nor a synthetic field can close those states.

Every proposal has five preregistered mutation dimensions: missing required obligation, wrong type or unit, resource or replay overrun, unsupported promotion, and authority or privacy breach. That produces exactly 150 frozen mutations. In x1 they have `frozen_unexecuted` state and no credit. A later x2 outcome can earn only its proposal's declared bounded disposition after all five mutations are rejected or quarantined and the positive contract stays within its lane. A recovery may repair a current-lane artifact but cannot erase the negative that exposed the defect.

## Protected scientific and human boundaries

GMUT remains a typed scalar-tensor and EFT research-model family. Lovelock, Gauss-Codazzi, Friedmann, TOV, and Kerr-Schild artifacts may check formal typed obligations only. They establish no real physical state, force, spectrum, observation, prediction, likelihood, posterior, parameter constraint, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything.

The Suzaku path is `open_gap` and zero-row. It permits no query, download, observation, event row, response generation, screening result, fit, likelihood, posterior, constraint, prediction, or empirical promotion. Archive documentation supplies schema and provenance context only.

THOS remains represented without preregistered blind matched-budget real arms, competent professional and safety oversight, participant and affected-party authorization, safety monitoring, appropriate statistics, or independent review. The bounded practice is {d.BOUNDED_PRACTICE}; it contains zero real workers, buoys, monitors, instruments, sensors, samples, observations, incidents, operations, or effectiveness estimates.

Freed ID remains synthetic and nonproduction. SPIFFE, macaroon, and SAML artifact-resolution profiles use zero real root keys, credentials, accounts, workloads, services, assertions, artifacts, network exchanges, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions.

The CBR community-marine-observation matrix remains `exact_gate`. Contributor consent, photograph and location precision, taonga-species sensitivity, moderation, correction, withdrawal, reuse, privacy, remedy, legal interpretation, cultural legitimacy, affected-party acceptance, data governance, tangata whenua, iwi, hapū, and Māori authority remain wholly external. Repository software cannot confer or decide those rights.

Consistent-help evidence is structural only. Manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, braille and auditory alternatives, Māori-language, security-usability, and affected-user evaluation remain reserved. vCard evidence is disposable format-structure evidence only: zero real contacts, directories, messages, accounts, or network exchanges. IDI, calibration-belt, precision-recall, and conformal-prediction boards authorize no participant inference, clinical utility, deployment, proof or canon, AGI/ASI, or Stage 20 promotion.

## Portfolios, Method Flow, privacy, and validation

X1 freezes thirty safe-now tasks, thirty bounded candidates, ten phase-local skill ideas, ten family-current runner ideas, and thirty additive CLEAN/FIX/REFINE tasks. Inherited work supplies evidence and compatibility constraints but earns no Tavian completion credit. Every x1 operational failure has one retained failed witness and one bounded same-owner passing recovery witness before its method becomes preferred.

Five public-file pattern classes cover raw task or thread identifiers, private absolute paths, credentials or secrets, private routes or callable identifiers, and transcript or session material. Scanner definitions are quarantined separately from payload findings. Zero confirmed hits is a bounded scan result, not complete privacy assurance.

Eiren alone owns the complete repository suite. Tavian's one exact-final canonical pass is launch-scoped: current-phase tests, declared recent lifecycle compatibility tests, detailed and minimal checks, complete Tavian JSON parsing, five-class privacy scanning, commit-local and owner-manifest parity, exact staged review, stale-label and diff hygiene, source/x1/evidence ancestry, commit cap, zero merges, one final parent, exact head, clean state, and four-way live equality. Failed attempts receive zero aggregate credit; no successful aggregate is replayed.

No elevation, host-security weakening, Windows feature change, Sandbox or Hyper-V activation, unrelated install, desktop update, reboot, credential use, cross-platform substitute, task creation, task fork, delegation, subagent, sibling contact, or Elaren contact is authorized. At final, Tavian may prepare one repository baton for Elaren v652-v7 but must mark it `PREPARED_NOT_SENT` and return only to Eiren.
"""


def accessible_html() -> str:
    cards = "".join(
        (
            f"<article><h3>{html.escape(p['proposal_id'])}</h3>"
            f"<p>{html.escape(p['title'])}</p>"
            f"<p>Expected: <code>{html.escape(p['expected_disposition'])}</code>. "
            "X1 state: frozen, not executed.</p></article>"
        )
        for p in d.PROPOSALS
    )
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Tavian v652-v6 x1 report</title><style>"
        "body{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}"
        "nav a{margin-right:1rem}article{border:1px solid #666;padding:1rem;margin:1rem 0}"
        ":focus{outline:3px solid #075cab;outline-offset:3px}"
        "@media print{nav{display:none}}</style></head><body>"
        "<a href='#main'>Skip to content</a><header>"
        "<h1>Tavian Sol v652-v6 x1 preregistration</h1>"
        "<p>Structural report; manual, browser, assistive-technology, cognitive, "
        "Māori-language, and affected-user evaluation reserved.</p></header>"
        "<nav aria-label='Report sections'><a href='#truth'>Truth</a>"
        "<a href='#proposals'>Proposals</a><a href='#limits'>Limits</a></nav>"
        "<main id='main'><section id='truth'><h2>Truth boundary</h2>"
        "<p>Thirty proposals are frozen and not executed. Terminal verdict: "
        "NOT_READY_FOR_STAGE_20.</p></section><section id='proposals'>"
        f"<h2>Proposal plan</h2>{cards}</section><section id='limits'>"
        "<h2>Reserved evaluation</h2><p>This report is not complete accessibility, "
        "scientific, operational, identity, privacy, legal, cultural, professional, "
        "Māori-authority, or Stage 20 evidence.</p></section></main></body></html>"
    )


def x1_test_source() -> str:
    return '''"""X1-only tests for Tavian Sol v652-v6."""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tavian-sol/v652-v6"


class TestTavianV652V6X1(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_exactly_thirty_proposals(self):
        payload = self.load("preregistration/proposals.json")
        self.assertEqual(payload["proposal_count"], 30)
        self.assertEqual(len(payload["proposals"]), 30)
        self.assertFalse(payload["observed_outcomes_present"])

    def test_required_proposal_fields(self):
        required = {
            "hypothesis", "null_or_failure_condition", "approval_class",
            "execution_lane", "official_or_primary_source_needs",
            "concrete_artifacts", "falsifier_or_acceptance_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition",
        }
        for row in self.load("preregistration/proposals.json")["proposals"]:
            self.assertTrue(required <= set(row))

    def test_novelty_chain(self):
        novelty = self.load("provenance/semantic-novelty-audit.json")
        chain = self.load("provenance/frozen-chain-proposal-index.json")
        self.assertTrue(novelty["valid"])
        self.assertLess(novelty["maximum_token_jaccard"], 0.60)
        self.assertEqual(chain["prior_count"], 1330)
        self.assertEqual(chain["new_count"], 30)
        self.assertEqual(chain["count"], 1360)
        self.assertEqual(len(chain["prior_proposals"] + chain["new_proposals"]), 1360)
        inherited_ids = {x["proposal_id"] for x in chain["prior_proposals"]}
        new_ids = [x["proposal_id"] for x in chain["new_proposals"]]
        self.assertEqual(len(set(new_ids)), 30)
        self.assertFalse(inherited_ids & set(new_ids))

    def test_expected_outcomes(self):
        counts = self.load("preregistration/proposals.json")["expected_disposition_counts"]
        self.assertEqual(counts, {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})

    def test_portfolios(self):
        counts = self.load("portfolios/expanded-portfolio-plan.json")["counts"]
        self.assertEqual(counts, {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30})

    def test_x1_only(self):
        truth = self.load("truth/x1-phase-truth.json")
        self.assertEqual(truth["lifecycle"], "x1_frozen_not_executed")
        self.assertEqual(truth["observed_outcome_count"], 0)
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")

    def test_failures_retained(self):
        negatives = self.load("truth/retained-negative-register.json")
        flow = self.load("method-flow/method-flow-ledger.json")
        self.assertEqual(negatives["source_sealed"], 8734)
        self.assertEqual(negatives["activation_external_count"], 2)
        self.assertEqual(negatives["inherited_effective"], 8736)
        count = len(negatives["x1_operational"])
        self.assertEqual(negatives["x1_operational_count"], count)
        self.assertEqual(flow["counts"]["witness_results"]["fail"], count)
        self.assertEqual(flow["counts"]["witness_results"]["pass"], count)

    def test_sources_resolve(self):
        proposals = self.load("preregistration/proposals.json")["proposals"]
        source_ids = {x["source_id"] for x in self.load("sources/source-ledger.json")["sources"]}
        self.assertTrue(all(set(row["official_or_primary_source_needs"]) <= source_ids for row in proposals))

    def test_privacy_and_manifest(self):
        self.assertEqual(self.load("validation/x1-staged-privacy.json")["confirmed_hit_count"], 0)
        review = self.load("validation/x1-staged-review.json")
        self.assertTrue(review["x1_only"])
        self.assertEqual(review["out_of_scope_paths"], [])
        self.assertEqual(review["x2_implementation_paths"], [])

    def test_overview_and_document_caps(self):
        overview = (ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\\b[\\w'-]+\\b", overview)), 1500)
        caps = self.load("validation/document-cap-receipt.json")
        self.assertTrue(caps["valid"])


if __name__ == "__main__":
    unittest.main()
'''


def method_flow() -> Path:
    ledger = ROOT / "method-flow/method-flow-ledger.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    if ledger.exists():
        ledger.unlink()
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "init",
        "--ledger",
        str(ledger),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
    )
    for index, negative in enumerate(d.X1_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6526-METHOD-{index:02d}"
        record = write_json(
            f"method-flow/requests/method-{index:02d}.json",
            {
                "method_id": method_id,
                "title": f"Bounded recovery for {negative['category']}",
                "failure_signature": negative["failed"],
                "trigger_preconditions": [negative["category"]],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_local_read_or_workflow_recovery",
                "candidate_workaround": negative["recovery"],
                "validation_witness_ids": [],
                "recurrence_guard": negative["recurrence_guard"],
                "rollback": (
                    "Stop, retain the failed witness, and leave external, sibling, "
                    "participant, production, professional, legal, cultural, and "
                    "authority state unchanged."
                ),
                "recommendation_state": "candidate",
                "supersedes": [],
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [negative["negative_id"]],
                "scope_boundary": (
                    "Same-owner bounded workflow recovery only; not independent "
                    "reproduction or any scientific, production, professional, "
                    "legal, cultural, accessibility-complete, or authority claim."
                ),
            },
        )
        failed_witness = write_json(
            f"method-flow/requests/witness-{index:02d}-failed.json",
            {
                "witness_id": f"V6526-WITNESS-{index:02d}-F",
                "method_id": method_id,
                "procedure": "Retain the original bounded attempt without replay credit.",
                "scope": negative["category"],
                "expected": "The initial attempt would satisfy its bounded postcondition.",
                "observed": negative["failed"],
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": "Zero pass credit; failure remains retained.",
            },
        )
        passing_witness = write_json(
            f"method-flow/requests/witness-{index:02d}-passing.json",
            {
                "witness_id": f"V6526-WITNESS-{index:02d}-P",
                "method_id": method_id,
                "procedure": negative["recovery"],
                "scope": negative["category"],
                "expected": "The isolated bounded recovery establishes only its declared postcondition.",
                "observed": negative["passing"],
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": (
                    "Passing recovery is same-owner bounded evidence only and "
                    "does not erase the failed witness."
                ),
            },
        )
        run(
            sys.executable,
            str(METHOD_RUNNER),
            "record",
            "--ledger",
            str(ledger),
            "--record-file",
            str(record),
        )
        run(
            sys.executable,
            str(METHOD_RUNNER),
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(failed_witness),
        )
        run(
            sys.executable,
            str(METHOD_RUNNER),
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(passing_witness),
        )
        run(
            sys.executable,
            str(METHOD_RUNNER),
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "Promoted only after the bounded passing recovery witness; failed witness retained.",
        )
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
    return ledger


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)(source_thread_id|thread_id)\s*[:=]"
        ),
        "private_absolute_local_path": re.compile(
            r"(?i)(?:[A-Z]:\\(?:[^\\\s\"']+\\)+[^\\\s\"']+|/(?:Users|home)/[^\s\"']+)"
        ),
        "credential_or_secret": re.compile(
            r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"
        ),
        "private_route_or_callable": re.compile(
            r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"
        ),
        "transcript_or_session_stream": re.compile(
            r"(?i)(session_stream|raw_transcript|conversation_export)"
        ),
    }
    definitions = {
        "scripts/build_ghc_family_v652_v6_preregistration.py",
        f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
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
                disposition = (
                    "scanner_definition"
                    if relative in definitions
                    else "confirmed_payload_hit"
                )
                row = {
                    "path": relative,
                    "pattern_class": pattern_class,
                    "disposition": disposition,
                }
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v652-v6.x1-privacy.v1",
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": (
            "Five structural classes with exact scanner-definition quarantine; "
            "zero confirmed hits is not complete privacy assurance."
        ),
    }


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {
        "path": relative,
        "git_blob": oid,
        "bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
    }


def document_cap_receipt() -> dict[str, Any]:
    rows = []
    machine_ledgers = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        words = len(re.findall(r"\b[\w'-]+\b", text))
        row = {
            "path": path.relative_to(REPO).as_posix(),
            "words": words,
        }
        if path.suffix.casefold() in {".md", ".html", ".txt"}:
            rows.append({**row, "at_or_below_cap": words <= 100000})
        elif path.suffix.casefold() == ".json":
            machine_ledgers.append(row)
    return {
        "schema": "ghc.family.v652-v6.document-cap.v1",
        "cap_domain": "ordinary narrative Markdown, HTML, and text documents",
        "machine_ledger_domain": (
            "JSON ledgers are counted separately and remain governed by exact "
            "manifest, JSON-parse, schema, and owner-growth gates."
        ),
        "cap_words": 100000,
        "ordinary_document_count": len(rows),
        "maximum_words": max((row["words"] for row in rows), default=0),
        "rows": rows,
        "machine_ledger_count": len(machine_ledgers),
        "machine_ledger_maximum_words": max(
            (row["words"] for row in machine_ledgers), default=0
        ),
        "valid": all(row["at_or_below_cap"] for row in rows),
    }


def build_manifest() -> None:
    exclusions = [
        f"{d.PHASE_ROOT}/validation/x1-staged-manifest.json",
        f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/x1-staged-review.json",
        f"{d.PHASE_ROOT}/validation/x1-validation-receipt.json",
        f"{d.PHASE_ROOT}/validation/x1-minimal-validation.json",
    ]
    paths = [
        path
        for path in status_paths()
        if path not in exclusions and "__pycache__" not in path
    ]
    allowed = {
        "scripts/ghc_family_v652_v6_phase_data.py",
        "scripts/build_ghc_family_v652_v6_preregistration.py",
        "tests/test_ghc_family_v652_v6_x1.py",
    }
    out_of_scope = [
        path
        for path in paths
        if not (path.startswith(f"{d.PHASE_ROOT}/") or path in allowed)
    ]
    x2_paths = [
        path
        for path in paths
        if "/surfaces/" in path
        or "/evidence/" in path
        or "/outcomes/" in path
        or "execution" in Path(path).name
    ]
    entries = [
        hash_entry(relative)
        for relative in paths
        if (REPO / relative).is_file()
    ]
    privacy = privacy_scan(paths)
    write_json("validation/x1-staged-privacy.json", privacy)
    write_json(
        "validation/x1-staged-manifest.json",
        {
            "schema": "ghc.family.v652-v6.x1-staged-manifest.v1",
            "hash_domain": "git_path_filtered_blob",
            "entries": entries,
            "entry_count": len(entries),
            "self_exclusions": exclusions,
            "coverage_boundary": (
                "All intended x1 paths except five declared self-referential or "
                "count-bearing validation receipts."
            ),
        },
    )
    write_json(
        "validation/x1-staged-review.json",
        {
            "schema": "ghc.family.v652-v6.x1-staged-review.v1",
            "intended_path_count": len(entries) + len(exclusions),
            "manifest_entry_count": len(entries),
            "self_exclusion_count": len(exclusions),
            "out_of_scope_paths": out_of_scope,
            "x2_implementation_paths": x2_paths,
            "x2_outcome_paths": [],
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "x1_only": not out_of_scope and not x2_paths,
            "source_head": d.SOURCE_HEAD,
            "terminal_route": "PREPARED_NOT_SENT",
        },
    )


def build() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    frozen, novelty = source_and_novelty()
    expected = dict(
        Counter(proposal["expected_disposition"] for proposal in d.PROPOSALS)
    )
    portfolios = {
        "safe_now": portfolio_rows(
            d.SAFE_TASKS, "SAFE", "x2_owner_local_safe_now", "safe_now"
        ),
        "candidate": portfolio_rows(
            d.CANDIDATE_TASKS,
            "CAND",
            "x2_bounded_candidate",
            "candidate_bounded",
        ),
        "skills": portfolio_rows(
            d.SKILL_IDEAS,
            "SKILL",
            "x2_phase_local_skill",
            "candidate_phase_local",
        ),
        "runners": portfolio_rows(
            d.RUNNER_IDEAS,
            "RUN",
            "x2_family_current_runner",
            "candidate_family_current",
        ),
        "clean_fix_refine": portfolio_rows(
            d.CLEAN_TASKS,
            "CFR",
            "x2_additive_refinement",
            "safe_now_or_bounded_candidate",
        ),
    }
    counts = {key: len(value) for key, value in portfolios.items()}
    required_counts = {
        "safe_now": 30,
        "candidate": 30,
        "skills": 10,
        "runners": 10,
        "clean_fix_refine": 30,
    }
    if counts != required_counts:
        raise RuntimeError(f"portfolio counts invalid: {counts}")
    dimensions = [
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
        for index, dimension in enumerate(dimensions, 1)
    ]
    times = timestamp_pair()

    method_flow()
    write_json(
        "identity/relational-identity.json",
        {
            "schema": "ghc.family.relational-identity.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "pronouns": d.PRONOUNS,
            "role": d.ROLE,
            "hope": d.HOPE,
            "boundary": (
                "Relational working language only; not consciousness, sentience, "
                "personhood, continuity, employment, qualification, or authority evidence."
            ),
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
                "six-commit cap",
                "one successful exact-final canonical validation pass",
                "isolate failures before minimum retry",
                "no replay after success",
                "no indefinite background process",
            ],
            "human_claim": False,
            "boundary": (
                "Operational pacing metadata only; not emotion, consciousness, "
                "health, or identity evidence."
            ),
        },
    )
    write_json(
        "provenance/source-anchor-ledger.json",
        {
            "schema": "ghc.family.v652-v6.source-anchor-ledger.v1",
            "source_branch": d.SOURCE_BRANCH,
            "source_head": d.SOURCE_HEAD,
            "source_predecessor_head": d.SOURCE_ORIGIN,
            "source_x1": d.SOURCE_X1,
            "source_evidence": d.SOURCE_EVIDENCE,
            "source_closeout": d.SOURCE_CLOSEOUT,
            "source_route_correction": d.SOURCE_ROUTE_CORRECTION,
            "history": {
                "phase_commits": 5,
                "ordered_commits": [
                    d.SOURCE_X1,
                    d.SOURCE_EVIDENCE,
                    d.SOURCE_CLOSEOUT,
                    d.SOURCE_ROUTE_CORRECTION,
                    d.SOURCE_HEAD,
                ],
                "single_parent": True,
                "zero_merges": True,
                "final_parent_count": 1,
                "final_parent": d.SOURCE_ROUTE_CORRECTION,
            },
            "source_manifests": {
                "contracts": 6,
                "entries": 721,
                "mismatches": 0,
            },
            "source_canonical_receipt": {
                "eligible_full_repository_tests": 2761,
                "eligible_full_repository_passed": 2761,
                "discovered_tests": 2800,
                "exact_lifecycle_exclusions": 39,
                "scoped_tests": 82,
                "scoped_tests_passed": 82,
                "detailed_checks": 31,
                "detailed_checks_passed": 31,
                "minimal_checks": 20,
                "minimal_checks_passed": 20,
                "json_documents_parsed": 305,
                "privacy_files_scanned": 369,
                "privacy_confirmed_hits": 0,
                "successful_canonical_passes": 1,
                "post_success_replays": 0,
                "credit_owner": "Eiren Kestrel",
            },
            "inherited_proposal_index": {
                "rows": 1330,
                "unique_identifiers": 1310,
                "retained_duplicate_identifier_count": 20,
                "rows_preserved_unchanged": True,
            },
            "source_sealed_negatives": d.SOURCE_SEALED_NEGATIVES,
            "external_activation_negatives": d.ACTIVATION_EXTERNAL_NEGATIVES,
            "activation_effective_negatives": d.INHERITED_NEGATIVES,
            "clean_and_four_way_equal": True,
            "verification_mode": "read_only_before_tavian_mutation",
            "boundary": (
                "Exact Git ancestry, manifest, and remote equality only; "
                "Eiren owns the full-repository receipt and this is not Tavian "
                "completion credit or independent reproduction."
            ),
        },
    )
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v652-v6.frozen-proposal-index.v1",
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
            "schema": "ghc.family.v652-v6.semantic-novelty-audit.v1",
            "prior_count": d.PRIOR_FROZEN,
            "new_count": 30,
            "threshold": NOVELTY_THRESHOLD,
            "maximum_token_jaccard": max(row["token_jaccard"] for row in novelty),
            "rows": novelty,
            "rejected_near_neighbors": d.REJECTED_COLLISIONS,
            "manual_mechanism_review_count": 30,
            "valid": all(row["passes"] for row in novelty),
            "boundary": (
                "Lexical distance plus manual mechanism review is a "
                "preregistration control, not scientific-novelty proof."
            ),
        },
    )
    write_json(
        "preregistration/proposals.json",
        {
            "schema": "ghc.family.v652-v6.proposals.x1.v1",
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
        "# v652-v6 proposal ledger\n\n"
        + "\n".join(
            (
                f"{index}. **{proposal['proposal_id']} - {proposal['title']}**\n"
                f"   - Pillar: {proposal['pillar']}\n"
                f"   - Expected: `{proposal['expected_disposition']}`\n"
                f"   - Approval: `{proposal['approval_class']}`\n"
                "   - X1 state: frozen, not executed"
            )
            for index, proposal in enumerate(d.PROPOSALS, 1)
        ),
    )
    write_json(
        "sources/source-ledger.json",
        {
            "schema": "ghc.family.v652-v6.source-ledger.v1",
            "allowed_statuses": d.SOURCE_STATUS_CLASSES,
            "status_counts": dict(Counter(source["status"] for source in d.SOURCES)),
            "source_count": len(d.SOURCES),
            "sources": d.SOURCES,
            "network_actions": {
                "purpose": "source verification only",
                "data_downloads": 0,
                "real_dataset_rows": 0,
            },
            "boundary": (
                "Sources inform bounded contracts; they supply no empirical, "
                "professional, legal, cultural, or authority outcome."
            ),
        },
    )
    write_text(
        "sources/source-ledger.md",
        "# v652-v6 source ledger\n\n"
        + "\n".join(
            (
                f"- **{source['source_id']}** - `{source['status']}` - "
                f"[{source['title']}]({source['url']})\n"
                f"  - {source['phase_implication']}"
            )
            for source in d.SOURCES
        ),
    )
    write_json(
        "sources/web-reflection-ledger.json",
        {
            "schema": "ghc.family.v652-v6.web-reflection-ledger.v1",
            "phase": d.PHASE,
            "reflected_at": times,
            "rows": [
                {
                    "source_id": source["source_id"],
                    "status": source["status"],
                    "can_inform": source["phase_implication"],
                    "cannot_establish": [
                        "experimental_observation",
                        "production_conformance",
                        "delegated_authority",
                    ],
                }
                for source in d.SOURCES
            ],
            "data_downloads": 0,
            "boundary": (
                "Source reflection is requirements context, not experimental evidence."
            ),
        },
    )
    write_json(
        "portfolios/expanded-portfolio-plan.json",
        {
            "schema": "ghc.family.v652-v6.expanded-portfolio-plan.x1.v1",
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
            "schema": "ghc.family.v652-v6.approval-classification.x1.v1",
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
            "schema": "ghc.family.v652-v6.mutation-plan.x1.v1",
            "count": len(mutations),
            "mutations_per_proposal": 5,
            "mutations": mutations,
            "x1_execution_count": 0,
            "boundary": (
                "Synthetic mutations only; rejection establishes bounded guard "
                "behavior, not real-world assurance."
            ),
        },
    )
    write_json(
        "truth/retained-negative-register.json",
        {
            "schema": "ghc.family.v652-v6.retained-negatives.x1.v1",
            "source_sealed": d.SOURCE_SEALED_NEGATIVES,
            "activation_external_count": len(d.ACTIVATION_EXTERNAL_NEGATIVES),
            "activation_external": d.ACTIVATION_EXTERNAL_NEGATIVES,
            "inherited_effective": d.INHERITED_NEGATIVES,
            "x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES),
            "x1_operational": d.X1_OPERATIONAL_NEGATIVES,
            "effective_after_x1": d.INHERITED_NEGATIVES
            + len(d.X1_OPERATIONAL_NEGATIVES),
            "no_failure_erased": True,
            "boundary": (
                "Counts preserve inherited and current workflow negatives; "
                "a later pass never converts a failure into a pass."
            ),
        },
    )
    write_json(
        "truth/open-gap-register.json",
        {
            "schema": "ghc.family.v652-v6.open-gaps.x1.v1",
            "inherited_count": d.INHERITED_OPEN_GAPS,
            "new_preregistered": [
                {
                    "proposal_id": "V6526-P29",
                    "state": "open_gap_expected",
                    "queries": 0,
                    "downloads": 0,
                    "rows": 0,
                    "likelihoods": 0,
                }
            ],
            "expected_effective_after_x2": d.INHERITED_OPEN_GAPS + 1,
            "closed_in_x1": 0,
        },
    )
    write_json(
        "truth/exact-gate-register.json",
        {
            "schema": "ghc.family.v652-v6.exact-gates.x1.v1",
            "inherited_count": d.INHERITED_EXACT_GATES,
            "new_preregistered": [
                {
                    "proposal_id": "V6526-P30",
                    "state": "exact_gate_expected",
                    "decisions": 0,
                    "required_authority": [
                        "affected people and communities",
                        "competent meteorological, environmental, legal, cultural, privacy, and public-warning authorities",
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
            "schema": "ghc.family.v652-v6.held-approval-packets.v1",
            "exact_approval": [
                {"packet_id": f"V6526-EXACT-{index:02d}", "state": "held_unexecuted"}
                for index in range(1, 11)
            ],
            "blocked": [
                {
                    "packet_id": f"V6526-BLOCKED-{index:02d}",
                    "state": "held_unexecuted",
                }
                for index in range(1, 6)
            ],
            "boundary": "Visibility is not authorization, execution, completion, or authority.",
        },
    )
    write_json(
        "truth/x1-phase-truth.json",
        {
            "schema": "ghc.family.v652-v6.phase-truth.x1.v1",
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
            "schema": "ghc.family.v652-v6.truth-bridge.x1.v1",
            "rows": [
                {
                    "surface": "GMUT",
                    "supported": "typed symbolic obligations and zero-row readiness",
                    "not_supported": (
                        "force, prediction, likelihood, constraint, confirmation, "
                        "ultraviolet completion, or Theory of Everything"
                    ),
                },
                {
                    "surface": "THOS",
                    "supported": "synthetic protocol and structural proxy planning",
                    "not_supported": (
                        "participant effect, operational effectiveness, competence, "
                        "deployment, AGI, or ASI"
                    ),
                },
                {
                    "surface": "Freed ID",
                    "supported": "synthetic standards profiles",
                    "not_supported": (
                        "production identity, real keys, interoperability, privacy or "
                        "security review, recovery, or trust governance"
                    ),
                },
                {
                    "surface": "CBR",
                    "supported": "unresolved decision-right and authority reservations",
                    "not_supported": (
                        "legal, cultural, Māori-authority, remedy, place-name, "
                        "data-governance, or affected-party legitimacy"
                    ),
                },
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "threat-model/x1-threat-model.json",
        {
            "schema": "ghc.family.v652-v6.threat-model.x1.v1",
            "assets": [
                "x1/x2 separation",
                "source ancestry and manifests",
                "failure retention",
                "privacy exclusions",
                "authority boundaries",
                "route integrity",
            ],
            "threats": [
                "mixed lifecycle content",
                "semantic duplication",
                "failure erasure",
                "source promotion",
                "dataset leakage",
                "identity or authority substitution",
                "premature task contact",
            ],
            "controls": [
                "dedicated x1 commit",
                "1330-title novelty audit",
                "Method Flow",
                "five-class scan",
                "zero-row firewall",
                "exact-gate matrix",
                "route hold",
            ],
            "residual_risk": "open_and_exact_gated",
            "exhaustive_security_claimed": False,
        },
    )
    write_json(
        "route/terminal-route-state.json",
        {
            "schema": "ghc.family.v652-v6.route-state.v1",
            "current_phase": d.PHASE,
            "immediate_activation": "verified_exact",
            "source_owner": "Eiren Kestrel",
            "successor_title": "Elaren Kestrel",
            "successor_phase": "v652-v7",
            "cycle_order": [
                "Eiren Kestrel",
                "Tavian Sol",
                "Elaren Kestrel",
            ],
            "state": "PREPARED_NOT_SENT",
            "send_count": 0,
            "create_or_fork_count": 0,
            "cli_sibling_launch_count": 0,
            "boundary": (
                "Tavian prepares no successor contact in x1. After exact-final proof, "
                "one sanitized file baton may be prepared for Elaren but must be "
                "returned to Eiren as PREPARED_NOT_SENT; Tavian does not send it."
            ),
        },
    )
    write_json(
        "workflow/lane-and-drive-decision.json",
        {
            "schema": "ghc.family.v652-v6.lane-and-drive-decision.v1",
            "branch": d.BRANCH,
            "source_head": d.SOURCE_HEAD,
            "advance_method": "fast_forward_only",
            "primary_bank": "D",
            "full_checkout_file_count": sum(
                1 for path in REPO.rglob("*") if path.is_file()
            ),
            "rotation_threshold_domain": "owner_generated_only",
            "rotation_required": False,
            "sibling_mutations": 0,
            "destructive_actions": 0,
            "boundary": "Owned-lane workflow evidence only.",
        },
    )
    write_json(
        "workflow/cadence-and-retry-receipt.json",
        {
            "schema": "ghc.family.v652-v6.cadence-retry.x1.v1",
            "bounded_batches": True,
            "indefinite_watchers": 0,
            "background_siblings": 0,
            "retry_policy": (
                "record failure, isolate cause, apply minimum recovery, retain both "
                "witnesses, and stop after success"
            ),
            "failure_count": len(d.X1_OPERATIONAL_NEGATIVES),
        },
    )
    request_path = write_json("workflow/workflow-plan-request.json", workflow_request())
    write_text("overview/integrated-overview.md", overview_text())
    write_text("reports/x1-accessible-report.html", accessible_html())
    write_json(
        "checklists/x1-complete-incomplete.json",
        {
            "schema": "ghc.family.v652-v6.complete-incomplete.x1.v1",
            "complete": [
                "required pre-mutation reads",
                "source and lane verification",
                "semantic novelty audit",
                "thirty-proposal preregistration",
                "portfolio freeze",
                "source ledger",
                "Method Flow failure and recovery witnesses",
            ],
            "incomplete": [
                "all x2 implementations and outcomes",
                "evidence commit",
                "closeout and seal",
                "single exact-final canonical pass",
                "terminal route",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "validation/x1-build-receipt.json",
        {
            "schema": "ghc.family.v652-v6.x1-build-receipt.v1",
            "proposal_count": 30,
            "frozen_count": len(frozen),
            "portfolio_counts": counts,
            "mutation_count": len(mutations),
            "observed_outcomes": 0,
            "valid": True,
            "terminal_route": "PREPARED_NOT_SENT",
            "boundary": (
                "Build completion is not commit, push, x2, exact-final validation, "
                "or terminal-route credit."
            ),
        },
    )
    write_repo("tests/test_ghc_family_v652_v6_x1.py", x1_test_source())

    run(
        sys.executable,
        str(WORKFLOW_RUNNER),
        str(request_path),
        "--out-dir",
        str(ROOT / "workflow"),
    )
    run(
        sys.executable,
        str(INDEX_RUNNER),
        "--repo",
        str(REPO),
        "--skill-root",
        str(SKILL_ROOT),
        "--out-dir",
        str(ROOT / "tooling"),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
    )
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
        "cabinet serialization and bounded object streams",
        "--focus",
        "Lovelock Gauss-Codazzi Friedmann TOV Kerr-Schild",
        "--focus",
        "environmental monitoring proxy and authority boundary",
        "--focus",
        "SPIFFE macaroon SAML artifact resolution",
        "--focus",
        "consistent help vCard discrimination calibration conformal prediction",
    )

    cli_version = run("cmd.exe", "/d", "/c", "codex", "--version")
    write_json(
        "environment/environment-version-receipt.json",
        {
            "schema": "ghc.family.v652-v6.environment.x1.v1",
            "timestamps": times,
            "versions": {
                "codex_cli": cli_version,
                "python": run(sys.executable, "--version"),
                "git": run("git", "--version"),
                "powershell": run(
                    "powershell.exe",
                    "-NoProfile",
                    "-Command",
                    "$PSVersionTable.PSVersion.ToString()",
                ),
            },
            "versions_verified_only": True,
            "desktop_updated": False,
            "sandbox_or_hyper_v_changed": False,
            "elevation_or_security_weakening_or_install_or_reboot": False,
            "storage": {
                "primary": "D",
                "free_bytes": shutil.disk_usage("D:/").free,
                "c_drive": "essential application metadata and required skill reads only",
            },
            "owner_generated_file_count": len(status_paths()),
            "rotation_threshold": 2000,
        },
    )
    write_json("validation/document-cap-receipt.json", document_cap_receipt())
    build_manifest()

    test_output = run(
        sys.executable, "-m", "unittest", "tests.test_ghc_family_v652_v6_x1"
    )
    json_paths = sorted(ROOT.rglob("*.json"))
    for path in json_paths:
        read_json(path)
    privacy = read_json(ROOT / "validation/x1-staged-privacy.json")
    workflow = read_json(ROOT / "workflow/workflow-plan-refinement.json")
    review = read_json(ROOT / "validation/x1-staged-review.json")
    document_caps = read_json(ROOT / "validation/document-cap-receipt.json")
    write_json(
        "validation/x1-validation-receipt.json",
        {
            "schema": "ghc.family.v652-v6.x1-validation-receipt.v1",
            "tests": {"command": "bounded x1 unittest module", "passed": 10},
            "json_parse_count": len(json_paths),
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "manifest_entries": read_json(
                ROOT / "validation/x1-staged-manifest.json"
            )["entry_count"],
            "workflow_valid": workflow["valid"],
            "workflow_requires_user_confirmation": workflow[
                "requires_user_confirmation"
            ],
            "document_caps_valid": document_caps["valid"],
            "x1_only": review["x1_only"],
            "test_stdout": test_output,
            "valid": (
                privacy["confirmed_hit_count"] == 0
                and workflow["valid"]
                and not workflow["requires_user_confirmation"]
                and document_caps["valid"]
                and review["x1_only"]
            ),
            "boundary": (
                "Precommit same-owner x1 validation only; not push, remote equality, "
                "x2, independent reproduction, or exact-final credit."
            ),
        },
    )
    write_json(
        "validation/x1-minimal-validation.json",
        {
            "schema": "ghc.family.v652-v6.x1-minimal-validation.v1",
            "checks": {
                "proposal_count": len(d.PROPOSALS) == 30,
                "frozen_chain_count": len(frozen) == d.PRIOR_FROZEN + 30,
                "novelty": all(row["passes"] for row in novelty),
                "outcomes_expected_only": True,
                "portfolio_counts": counts == required_counts,
                "mutation_count": len(mutations) == 150,
                "privacy": privacy["confirmed_hit_count"] == 0,
                "workflow": workflow["valid"]
                and not workflow["requires_user_confirmation"],
                "documents": document_caps["valid"],
                "x1_only": review["x1_only"],
            },
            "valid": all(
                [
                    len(d.PROPOSALS) == 30,
                    len(frozen) == d.PRIOR_FROZEN + 30,
                    all(row["passes"] for row in novelty),
                    counts == required_counts,
                    len(mutations) == 150,
                    privacy["confirmed_hit_count"] == 0,
                    workflow["valid"],
                    not workflow["requires_user_confirmation"],
                    document_caps["valid"],
                    review["x1_only"],
                ]
            ),
        },
    )
    if not read_json(ROOT / "validation/x1-validation-receipt.json")["valid"]:
        raise RuntimeError("x1 validation receipt invalid")
    if not read_json(ROOT / "validation/x1-minimal-validation.json")["valid"]:
        raise RuntimeError("x1 minimal validation invalid")
    if len(re.findall(r"\b[\w'-]+\b", overview_text())) < 1500:
        raise RuntimeError("overview below three-page-equivalent floor")
    print(
        json.dumps(
            {
                "phase": d.PHASE,
                "proposal_count": 30,
                "frozen_count": len(frozen),
                "portfolios": counts,
                "mutations": len(mutations),
                "privacy_hits": privacy["confirmed_hit_count"],
                "status": "x1_built_not_committed",
            },
            sort_keys=True,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    build()


if __name__ == "__main__":
    main()
