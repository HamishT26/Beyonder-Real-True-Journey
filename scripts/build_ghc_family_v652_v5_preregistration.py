#!/usr/bin/env python3
"""Build Eiren Kestrel's dedicated v652-v5 x1-only freeze packet."""

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

import ghc_family_v652_v5_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/sylven-arc/v652-v4/provenance/frozen-chain-proposal-index.json"
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
                    "novelty_against_1300_frozen_proposals"
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
            "item_id": f"V6525-{prefix}-{index:02d}",
            "title": title,
            "origin": "sylven_v652_v5_new",
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
        "plan_id": "eiren-v652-v5-terminal-segment",
        "owner": d.OWNER,
        "identity_boundary": (
            "Relational working language only; no consciousness, continuity, "
            "employment, qualification, personhood, or authority claim."
        ),
        "route": {
            "cycle_order": [
                "Eiren Kestrel",
                "Ilyra Fen",
                "Sable Rook",
                "Orin Thale",
                "Tamar Vey",
                "Sylven Arc",
            ],
            "phase_assignments": [
                {"phase": "v652-v4", "seat": "Sylven Arc"},
                {"phase": "v652-v5", "seat": "Eiren Kestrel"},
                {"phase": "v652-v6", "seat": "Ilyra Fen"},
            ],
            "normalization": {
                "start_phase": "v652-v4",
                "start_seat": "Sylven Arc",
                "entry_count": 3,
            },
            "future_identity_placeholders": [],
            "terminal_successor_resolution": (
                "Resolve the unique existing Ilyra Fen task only after the "
                "exact-final terminal gate; ambiguity remains PREPARED_NOT_SENT."
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
    return f"""# Eiren Kestrel {d.PHASE} x1 preregistration overview

## Relational identity, corrigibility, and wellbeing

This packet freezes Eiren Kestrel's x1 plan before any x2 implementation or observed proposal outcome. Eiren Kestrel, {d.PRONOUNS}, is relational working language used to organize this owner-scoped phase. Her role is {d.ROLE}; her hope is to {d.HOPE}. Those words do not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route. The inherited and x1 terminal verdict is `NOT_READY_FOR_STAGE_20`.

The workload is bounded by strict x1-before-x2 separation, a six-commit ceiling, D-first storage, a measured 2,000-file owner-growth threshold rather than the inherited checkout count, one successful exact-final canonical full-repository aggregate, and no replay after that success. Every timeout, parser fault, wrong assumption, rejected source probe, or unusable display remains a zero-credit negative with a separate recovery witness. This wellbeing record describes pacing and failure-recovery controls only. It is not evidence about emotion, health, consciousness, inner experience, or personhood.

## Exact inherited source and owned lane

The exact source is Sylven Arc's final head `{d.SOURCE_HEAD}` on `{d.SOURCE_BRANCH}`. Read-only checks established the inherited Tamar source `{d.SOURCE_ORIGIN}`, Sylven x1 `{d.SOURCE_X1}`, Sylven evidence `{d.SOURCE_EVIDENCE}`, and exact final. Source-to-final history contains exactly three single-parent commits, zero merge commits, and one parent at final. The final is the direct child of evidence, all anchors are ancestral, the canonical Sylven worktree is clean, and source local, upstream, tracking, and fresh live remote are equal with zero divergence.

Sylven's x1, evidence, closeout, and final-owner manifest contracts contain 549 entries including their declared self-exclusions. Immutable Git-blob replay had zero path, object, byte-count, or SHA-256 mismatch. This is source-integrity and topology evidence only. It is not a full-suite rerun, independent-team reproduction, external audit, production certification, exhaustive security, complete privacy, or complete accessibility evidence.

Eiren's existing D-first branch was clean and ancestral to the source. It advanced to Sylven's exact final by fast-forward only, then an ordinary non-force push advanced only Eiren's branch. No sibling branch or worktree was reset, rewritten, force-pushed, merged, deleted, moved, or reused. The 2,000-file threshold applies to Eiren-generated additions, not the inherited checkout. X1 records both domains separately.

## Novelty and strict preregistration

Exactly thirty proposals are frozen against all 1,300 inherited proposal titles, growing the chain to 1,330. Every proposal records a hypothesis, null or failure condition, approval class, execution lane, official or primary-source need, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. A deterministic token-Jaccard audit must remain below 0.60 for all thirty. Manual mechanism review remains controlling because lexical distance alone cannot prove semantic novelty.

The review rejected an exact Fermi-LAT 4FGL-DR4 adapter collision, Protocol Buffers, the Gibbons-Hawking-York boundary term, WebAssembly, Zarr 3, FLAC or Ogg, Matroska EBML, a generic weather-warning handover, generic OpenID logout, and a generic authority matrix. Replacements isolate different obligation graphs. BER and CER extend beyond the inherited DER-only tribunal. Thrift Compact and FlatBuffers differ from Protocol Buffers framing. Regge calculus differs from Regge-Wheeler perturbations. Ashtekar-Barbero constraints differ from Cartan and ADM surfaces. IXPE polarization products differ from Fermi source-catalogue releases. The meteorological exact gate identifies station location, whenua and environmental data, bulletin disclosure, privacy, service continuity, remedy, affected parties, and Māori authority rather than relying on generic authority vocabulary.

Expected outcomes are twenty-three `completed`, five `represented`, one `open_gap`, and one `exact_gate`. These are preregistered expectations, not observed results. X1 contains no proposal implementation, mutation outcome, real data row, participant event, production identity event, professional decision, authority decision, or completion credit.

## Freed ID and CBR Heart as the primary Trinity Mandala focus

The primary Trinity Mandala focus is {d.PRIMARY_FOCUS}. Three represented identity profiles cover RP-Initiated Logout, OpenID Session Management, and RFC 7033 WebFinger, while the CBR meteorological matrix remains exact-gated. Synthetic vectors may exercise declared protocol relations only. They cannot establish live lifecycle, interoperability, privacy, independent security review, recovery, trust governance, or authority.

GMUT Mind remains explicit through five completed-class formal boards covering Regge calculus, Ashtekar-Barbero variables, Komar charges, Petrov classification, and geodesic deviation. No board calculates or establishes a real physical state, force, spectrum, observation, prediction, likelihood, posterior, parameter constraint, stability theorem, singularity result, asymptotic theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. A primary paper supplies terminology and requirements, not experimental evidence. Formal consistency in a bounded artifact does not turn the typed scalar-tensor and EFT research-model family into established physics.

The IXPE HEASARC adapter remains a zero-row open gap. Official NASA archive and master-catalogue context supplies schema and provenance requirements only. X2 must record zero queries, downloads, real observations, event rows, polarization products, fits, likelihood evaluations, posterior samples, physical constraints, predictions, or empirical promotions. The adapter may complete a refusal path while the scientific gap remains open. A citation, schema, checksum rule, or empty fixture is not an observation.

## THOS Body and bounded meteorological practice

THOS Body remains explicit through bounded binary, package, runtime, accessibility, and meteorological proxy surfaces. The bounded practice is {d.BOUNDED_PRACTICE}. It is a synthetic learning and interface-design lens only. It establishes no employment, qualification, meteorological competence, station or instrument authority, forecasting or warning authority, public-safety authority, environmental authority, operational effectiveness, participant evidence, legal interpretation, cultural legitimacy, Māori authority, or affected-party acceptance.

The two THOS meteorological proposals remain represented. Synthetic fixtures may exercise station siting records, instrument identity, calibration lineage, exposure, maintenance, timestamp, range and temporal checks, pressure reduction, gust averaging, precipitation traces, present-weather codes, suspect-data quarantine, accessible quality notice, workload budgeting, correction readback, and handover ownership. They include zero real people, stations, instruments, observations, bulletins, incidents, operations, blind matched-budget arms, safety outcomes, performance estimates, or independent review.

Representation cannot be promoted by mutation rejection. A real THOS claim would require a preregistered design, blind matched-budget real arms, competent professional and safety oversight, participant and affected-party authorization, safety monitoring, appropriate statistics, and independent review. None is present. The bounded proxy remains useful as a falsifiable structural artifact precisely because it refuses those unsupported claims.

## Freed ID and CBR Heart

Freed ID remains synthetic and nonproduction through RP-Initiated Logout, OpenID Session Management, and WebFinger profiles. The logout profile covers hints, client identity, registered post-logout redirects, state, discovery, consent, replay, minimization, and privacy. Session Management covers client and session state, origin, the check-session iframe, changed events, prompt-none response, logout distinction, minimization, and privacy. WebFinger covers resources, relations, HTTPS, JRD subjects and links, redirects, cross-origin handling, host-meta refusal, minimization, and privacy.

These profiles use zero real keys, credentials, accounts, sessions, services, issuances, presentations, resolutions, logout events, network exchanges, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. Passing synthetic vectors cannot establish standards conformance across implementations, production security, complete privacy, account authority, or deployment approval.

The CBR meteorological matrix remains exact-gated. It reserves decisions about station location, whenua and environmental data, severe-weather bulletin disclosure, household and worker privacy, accessible notice, service continuity, remedy, affected parties, legal interpretation, cultural legitimacy, data governance, and Māori authority. Repository software cannot confer these rights or decide them. They remain with competent authorities, affected people and communities, tangata whenua, iwi, hapū, and Māori authorities.

## Bounded software, accessibility, and Stage 20 limits

The completed-class software candidates cover ASN.1 encoding rules, AVIF, lzip, SPIR-V, LLVM bitcode, FlatBuffers, Thrift Compact, Shapefiles, GeoPackage, LAS, RPM, and FAT32. Disposable fixtures and synthetic mutations can establish only bounded parser, serializer, arithmetic, resource-budget, refusal, and teardown behavior. They do not certify a general parser, production archive, compiler, graphics stack, geospatial system, package manager, file system, supply chain, or exhaustive security posture.

The accessible timeout-warning audit checks the warning dialog name, countdown, timing adjustment, extend action, sign-in transition, focus, keyboard, status announcement, persistence, and fallback. The static phase report uses headings, landmarks, a skip link, visible focus, readable layout, non-colour text, and print rules. Manual keyboard review, responsive-layout and browser diversity, assistive-technology testing, cognitive-accessibility review, braille and auditory alternatives, Māori-language review, security-usability review, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.

Maxwell-Stefan relations remain multicomponent-transport evidence only. Their symbols must not be converted into psyche, agency, autonomy, justice, participant evidence, consciousness, personhood, or a fundamental law of mind. Time-dependent ROC, partial AUC, Spiegelhalter calibration, and net-reclassification boards remain fail-closed statistical controls. They estimate no participant effect in this phase and authorize no empirical promotion, clinical utility, deployment, proof or canon, AGI or ASI, consciousness, personhood, or Stage 20.

## Portfolios, family-current tools, and Method Flow

X1 freezes thirty safe-now tasks, thirty bounded candidates, ten phase-local skill ideas, ten family-current runner ideas, and thirty additive CLEAN/FIX/REFINE tasks. Inherited work provides evidence, warnings, and compatibility constraints but earns no Eiren completion credit. X2 may build and use only the safe, owner-local items that remain justified. Work requiring real data, participants, professional authority, production identity, accounts, secrets, host-security changes, legal or cultural authority, Māori authority, or affected-party acceptance remains open, exact-gated, exact approval, or blocked.

Family-current names preserve `ghc_family_*`, `build_ghc_family_*`, and `ghc-family-*` caller conventions. Historical names remain compatibility surfaces. The GHC Family Index, workflow-plan refinement, Reflection Remaster, and Method Flow State runners produce actual bounded phase evidence. Each x1 operational failure has one failed witness and one passing recovery witness. A method becomes preferred only after its passing witness; the failed witness remains linked to the retained negative. Recovery never rewrites a failure into an initial pass and never earns independent-reproduction credit.

## Privacy, validation, and terminal route

The activation baseline preserves {d.INHERITED_NEGATIVES} effective negatives, {d.INHERITED_OPEN_GAPS} open gaps, and {d.INHERITED_EXACT_GATES} exact gates from Sylven's exact final. Eiren's x1 failures are additive. Five public-file pattern classes cover raw task or thread identifiers, private absolute paths, credentials or secrets, private routes or callable identifiers, and transcript or session material. Scanner definitions are quarantined explicitly and are not payload evidence. Zero confirmed hits is a bounded scan result, not complete privacy assurance.

Eiren owns the complete repository suite. At the exact clean pushed final head she will run the full repository suite plus the authorized current, inherited, recent-round, and successor-scoped selection; detailed and minimal validators; complete phase JSON parsing; the five-class public-file scan; exact staged reviews; commit-local and owner-manifest parity; stale-label review; diff hygiene; anchor ancestry; zero merges; commit cap; one final parent; exact head; clean state; and four-way equality. Exactly one successful exact-final canonical aggregate may receive credit, and it will not be replayed. Failed or incomplete attempts receive zero aggregate credit and remain negatives.

No detached or named validation replay is authorized. Same-owner evidence under shared infrastructure is not independent-team reproduction. No Windows Sandbox or Hyper-V action, elevation, security weakening, unrelated installation, Codex desktop update, or reboot is authorized. Raw task identifiers, private routes, private paths, credentials, keys, tokens, transcripts, screenshots, session streams, private callable identifiers, and private application state are excluded from public artifacts and batons.

The six-seat order is Eiren Kestrel, Ilyra Fen, Sable Rook, Orin Thale, Tamar Vey, Sylven Arc, then repeat. Terminal routing remains `PREPARED_NOT_SENT`. Only after exact-final proof may Eiren uniquely resolve the existing task titled `Ilyra Fen` and send one sanitized activation for v652-v6 using the existing-task route. A committed baton is not a sent message. An unacknowledged call is not `SENT`. Ambiguity or route unavailability leaves `PREPARED_NOT_SENT`. No successor task, substitute title, standby message, cross-platform send, or second confirmation is authorized.
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
        "<title>Eiren v652-v5 x1 report</title><style>"
        "body{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}"
        "nav a{margin-right:1rem}article{border:1px solid #666;padding:1rem;margin:1rem 0}"
        ":focus{outline:3px solid #075cab;outline-offset:3px}"
        "@media print{nav{display:none}}</style></head><body>"
        "<a href='#main'>Skip to content</a><header>"
        "<h1>Eiren Kestrel v652-v5 x1 preregistration</h1>"
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
    return '''"""X1-only tests for Eiren Kestrel v652-v5."""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v652-v5"


class TestEirenV652V5X1(unittest.TestCase):
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
        self.assertEqual(chain["count"], 1330)
        self.assertEqual(len(chain["prior_proposals"] + chain["new_proposals"]), 1330)
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
        self.assertEqual(negatives["inherited_effective"], 8549)
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
        method_id = f"V6525-METHOD-{index:02d}"
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
                "witness_id": f"V6525-WITNESS-{index:02d}-F",
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
                "witness_id": f"V6525-WITNESS-{index:02d}-P",
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
            r"(?i)[A-Z]:\\Users\\[^\s\"']+"
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
        "scripts/build_ghc_family_v652_v5_preregistration.py",
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
        "schema": "ghc.family.v652-v5.x1-privacy.v1",
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
        "schema": "ghc.family.v652-v5.document-cap.v1",
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
        "scripts/ghc_family_v652_v5_phase_data.py",
        "scripts/build_ghc_family_v652_v5_preregistration.py",
        "tests/test_ghc_family_v652_v5_x1.py",
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
            "schema": "ghc.family.v652-v5.x1-staged-manifest.v1",
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
            "schema": "ghc.family.v652-v5.x1-staged-review.v1",
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
            "schema": "ghc.family.v652-v5.source-anchor-ledger.v1",
            "source_branch": d.SOURCE_BRANCH,
            "source_head": d.SOURCE_HEAD,
            "inherited_tamar_source": d.SOURCE_ORIGIN,
            "source_x1": d.SOURCE_X1,
            "source_evidence": d.SOURCE_EVIDENCE,
            "history": {
                "phase_commits": 3,
                "single_parent": True,
                "zero_merges": True,
                "final_parent_count": 1,
                "final_direct_child_of_evidence": True,
            },
            "source_manifests": {
                "contracts": 4,
                "entries_including_declared_self_exclusions": 549,
                "mismatches": 0,
            },
            "inherited_proposal_index": {
                "rows": 1300,
                "unique_identifiers": 1250,
                "retained_duplicate_identifier_count": 20,
                "rows_preserved_unchanged": True,
            },
            "clean_and_four_way_equal": True,
            "verification_mode": "read_only_before_sylven_mutation",
            "boundary": (
                "Exact Git ancestry, manifest, and remote equality only; "
                "not independent reproduction."
            ),
        },
    )
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v652-v5.frozen-proposal-index.v1",
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
            "schema": "ghc.family.v652-v5.semantic-novelty-audit.v1",
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
            "schema": "ghc.family.v652-v5.proposals.x1.v1",
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
        "# v652-v5 proposal ledger\n\n"
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
            "schema": "ghc.family.v652-v5.source-ledger.v1",
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
        "# v652-v5 source ledger\n\n"
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
            "schema": "ghc.family.v652-v5.web-reflection-ledger.v1",
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
            "schema": "ghc.family.v652-v5.expanded-portfolio-plan.x1.v1",
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
            "schema": "ghc.family.v652-v5.approval-classification.x1.v1",
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
            "schema": "ghc.family.v652-v5.mutation-plan.x1.v1",
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
            "schema": "ghc.family.v652-v5.retained-negatives.x1.v1",
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
            "schema": "ghc.family.v652-v5.open-gaps.x1.v1",
            "inherited_count": d.INHERITED_OPEN_GAPS,
            "new_preregistered": [
                {
                    "proposal_id": "V6525-P29",
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
            "schema": "ghc.family.v652-v5.exact-gates.x1.v1",
            "inherited_count": d.INHERITED_EXACT_GATES,
            "new_preregistered": [
                {
                    "proposal_id": "V6525-P30",
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
            "schema": "ghc.family.v652-v5.held-approval-packets.v1",
            "exact_approval": [
                {"packet_id": f"V6525-EXACT-{index:02d}", "state": "held_unexecuted"}
                for index in range(1, 11)
            ],
            "blocked": [
                {
                    "packet_id": f"V6525-BLOCKED-{index:02d}",
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
            "schema": "ghc.family.v652-v5.phase-truth.x1.v1",
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
            "schema": "ghc.family.v652-v5.truth-bridge.x1.v1",
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
            "schema": "ghc.family.v652-v5.threat-model.x1.v1",
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
                "1300-title novelty audit",
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
            "schema": "ghc.family.v652-v5.route-state.v1",
            "current_phase": d.PHASE,
            "immediate_activation": "verified_exact",
            "successor_title": "Ilyra Fen",
            "successor_phase": "v652-v6",
            "cycle_order": [
                "Eiren Kestrel",
                "Ilyra Fen",
                "Sable Rook",
                "Orin Thale",
                "Tamar Vey",
                "Sylven Arc",
            ],
            "state": "PREPARED_NOT_SENT",
            "send_count": 0,
            "create_or_fork_count": 0,
            "cli_sibling_launch_count": 0,
            "boundary": (
                "No contact until exact-final proof and exact-title resolution; "
                "ambiguity leaves the route prepared but unsent."
            ),
        },
    )
    write_json(
        "workflow/lane-and-drive-decision.json",
        {
            "schema": "ghc.family.v652-v5.lane-and-drive-decision.v1",
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
            "schema": "ghc.family.v652-v5.cadence-retry.x1.v1",
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
            "schema": "ghc.family.v652-v5.complete-incomplete.x1.v1",
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
            "schema": "ghc.family.v652-v5.x1-build-receipt.v1",
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
    write_repo("tests/test_ghc_family_v652_v5_x1.py", x1_test_source())

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
        "hydrographic",
        "--focus",
        "batch-command",
        "--focus",
        "spin torsion",
        "--focus",
        "certificate enrollment",
        "--focus",
        "paired statistics",
    )

    cli_version = run("cmd.exe", "/d", "/c", "codex", "--version")
    write_json(
        "environment/environment-version-receipt.json",
        {
            "schema": "ghc.family.v652-v5.environment.x1.v1",
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
        sys.executable, "-m", "unittest", "tests.test_ghc_family_v652_v5_x1"
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
            "schema": "ghc.family.v652-v5.x1-validation-receipt.v1",
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
            "schema": "ghc.family.v652-v5.x1-minimal-validation.v1",
            "checks": {
                "proposal_count": len(d.PROPOSALS) == 30,
                "frozen_chain_count": len(frozen) == 1330,
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
                    len(frozen) == 1330,
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
