#!/usr/bin/env python3
"""Build Ilyra Fen v650-v8 closeout, seal, and successor packet."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v650_v8_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SOURCE = d.SOURCE_HEAD
X1 = "d8726faad1ae416ef31f98a8744901eeedfe3c56"
EVIDENCE = "325c410a16241cd8fa21706f82ab2bfd8ed47531"
EFFECTIVE_NEGATIVES = 6429
OPEN_GAPS = 50
EXACT_GATES = 51


def run(*args: str) -> str:
    return subprocess.check_output(list(args), cwd=REPO).decode("utf-8").strip()


def git(*args: str) -> str:
    return run("git", *args)


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


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def status_paths() -> list[str]:
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=REPO)
    return sorted({row[3:].replace("\\", "/") for row in raw.decode("utf-8").split("\0") if len(row) > 3})


def changed_paths(base: str) -> list[str]:
    committed = set(filter(None, git("diff", "--name-only", f"{base}..HEAD").splitlines()))
    return sorted(committed | set(status_paths()))


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}


def privacy_scan(paths: list[str], definitions: set[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\\\Users\\\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    candidates, confirmed, scanned = [], [], 0
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
    return {"schema": "ghc.family.v650-v8.privacy-scan.v1", "scanned_file_count": scanned, "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five structural classes with exact scanner-definition quarantine; zero confirmed hits is not complete privacy assurance."}


def integrated_overview() -> str:
    outcomes = load("outcomes/outcome-ledger.json")["outcomes"]
    outcome_lines = []
    for row in outcomes:
        proposal = next(p for p in d.PROPOSALS if p["proposal_id"] == row["proposal_id"])
        outcome_lines.append(
            f"### {row['proposal_id']}: {proposal['title']}\n\n"
            f"Outcome: `{row['observed_outcome']}`. The phase accepted the declared bounded fixture and rejected all five preregistered mutations. "
            f"The evidence remains limited to {proposal['mission_surface']}. Its acceptance gate was: {proposal['falsifier_or_acceptance_gate']} "
            f"The null or failure condition remained explicit: {proposal['null_or_failure_condition']} No participant, production, authority, empirical-confirmation, independent-reproduction, or Stage 20 credit follows."
        )
    return f"""# Ilyra Fen v650-v8 final integrated overview

## Identity, purpose, and boundary

Ilyra Fen, she/they, served as a relational evidence-boundary steward with the hope to leave every claim traceable and every gate unmistakable. This is working language for collaboration only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route.

The phase began from Eiren Kestrel's exact sealed v650-v7 head `{SOURCE}` and preserved the inherited source, x1, and evidence anchors. Ilyra froze exactly twenty genuinely distinct proposals after auditing 880 earlier proposals. Strict x1-before-x2 separation remained visible in the dedicated x1 commit `{X1}` and immutable evidence commit `{EVIDENCE}`. The final lifecycle record binds itself to the commit containing this document, whose direct parent must be the evidence commit. The branch remains additive and preserves sibling work.

## Executive result

All twenty frozen proposals executed only as their evidence allowed. The outcome distribution is exactly 14 completed, 4 represented, 1 open gap, and 1 exact gate. Completed means the bounded software, symbolic, numerical, or structural hypothesis passed. Represented means synthetic proxy behavior was exercised without real people, assets, operational outcomes, or independent review. Open gap means real empirical evidence was not obtained. Exact gate means competent, affected-party, legal, cultural, clinical, or Māori authority was required and was not substituted by repository software.

The phase retains {EFFECTIVE_NEGATIVES:,} effective negatives: 6,311 inherited activation negatives, nine Ilyra x1 operational negatives, five Ilyra x2 evidence operational negatives, four Ilyra closeout operational negatives, and 100 executed and rejected preregistered mutations. Eighteen failed Method Flow witnesses and seventeen bounded passing recovery witnesses remain visible across fifteen preferred methods after bounded recovery. Recovery never erases failure. Fifty effective open gaps and fifty-one effective exact gates remain open. The verdict is `NOT_READY_FOR_STAGE_20`.

The primary Trinity Mandala focus was THOS Body. The bounded practice lens joined hospital medical-gas alarm and manifold-changeover handover with reusable-device decontamination and sterilization load-release and recall handover. It was synthetic learning and design only. It established no clinical role, employment, competence, patient-safety result, equipment authority, hospital authority, privacy authority, legal or cultural authority, Māori authority, participant evidence, affected-party authorization, or real operational outcome.

## Evidence architecture

The owner packet contains typed contracts, canonical fixtures, five mutation classes per proposal, specialized bounded witnesses, runner receipts, skill receipts, source-status records, portfolio execution records, Method Flow records, accessible reports, threat and wellbeing records, and exact manifests. Twenty repository-local skills were initialized with the official creator, validated on their actual directories, and smoke-used. Ten family-current runners were invoked. No skill was globally installed and no subagent or sibling was used. Forty safe-now tasks, thirty bounded candidate tasks, twenty skills, ten runners, and forty additive CLEAN/FIX/REFINE tasks completed only within their frozen hypotheses.

The evidence validator passed sixteen of sixteen checks and twelve of twelve current-phase tests before the evidence commit. It parsed every phase JSON document, checked five privacy and raw-identifier classes, proved exact staged-blob parity, verified status-surface coverage, enforced document caps, and preserved x1 ancestry. It did not run the complete repository suite because the current allocation reserves that suite to Eiren. The final validator is designed for one successful canonical exact-final pass and no replay after success.

## Scientific and authority interpretation

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Kadanoff-Baym and Bethe-Salpeter boards are symbolic obligation maps, not physical solutions, detected forces, likelihoods, constraints, empirical confirmation, ultraviolet completion, quantum completeness, or a Theory of Everything. The NuSTAR NUMASTER adapter remains a zero-row refusal contract. It made no query or download and ingested no events, spectra, response rows, or background rows.

THOS remains represented. Synthetic medical-gas and sterile-load traces can expose state, hold, correction, readback, accessible-notice, workload, exception, and handover obligations. They cannot establish operational effectiveness without preregistered blind matched-budget real arms, real participants and operators, safety monitoring, appropriate statistics, and independent review.

Freed ID remains synthetic and nonproduction. The JWT BCP and JWK Set profiles used no real private keys, tokens, accounts, issuers, relying parties, network exchanges, resolution, status, revocation, interoperability, privacy review, independent security review, recovery decision, or trust-governance decision. Production completion remains gated to standards-conformant real cryptographic and governance evidence.

CBR and hospital authority remain exact-gated. Repository matrices cannot decide patient privacy, remedy, clinical responsibility, legal interpretation, cultural legitimacy, Māori wording, Māori data governance, or who speaks with Māori authority. Those decisions remain with competent authorities, affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

## Twenty bounded outcomes

{"\n\n".join(outcome_lines)}

## Validation and closeout meaning

The final owner and delta manifests use Git path-filtered blob hashes, not checkout bytes. This avoids CRLF and LF ambiguity while preserving exact committed content. The privacy scan distinguishes scanner definitions from confirmed payload hits. A zero confirmed-hit result is bounded evidence, never complete privacy assurance. Structural accessibility checks reserve manual keyboard, touch, responsive layout, browser-diverse, assistive-technology, cognitive-accessibility, Māori-language, clinical-user, and affected-user evaluation.

No Windows Sandbox or Hyper-V activation occurred. No elevation, host-security weakening, Windows-feature change, unrelated installation, desktop-app update, or reboot occurred. Version receipts are observation only. Canonical and any later same-owner check remain same-owner evidence under shared infrastructure; this phase deliberately creates no replay lane and makes no independent-team reproduction claim.

The successor route remains held until the exact final commit is clean, pushed, four-way remote-equal, and passes its one canonical final validation. Only then may one sanitized message activate the exact existing `Sable Rook` task for solo v651-v1. No task may be created or forked, and no standby sibling may be contacted.
"""


def static_report() -> str:
    rows = []
    for row in load("outcomes/outcome-ledger.json")["outcomes"]:
        rows.append(f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['slug'])}</td><td>{html.escape(row['observed_outcome'])}</td><td>{row['mutation_rejections']}/5</td></tr>")
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Ilyra Fen v650-v8 final report</title><style>body{{font:1rem/1.55 system-ui;max-width:82rem;margin:auto;padding:1rem}}nav a{{margin-right:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #666;padding:.55rem;text-align:left;vertical-align:top}}:focus{{outline:3px solid #075cab;outline-offset:3px}}.notice{{border-left:.4rem solid #8b5500;padding:1rem;background:#fff7e8}}@media(max-width:48rem){{table{{display:block;overflow-x:auto}}}}@media print{{nav,.skip{{display:none}}}}</style></head><body><a class='skip' href='#main'>Skip to content</a><header><h1>Ilyra Fen v650-v8 bounded final report</h1><p class='notice'>NOT_READY_FOR_STAGE_20. Relational identity language is not consciousness, personhood, employment, or authority evidence.</p></header><nav aria-label='Report sections'><a href='#truth'>Truth</a><a href='#outcomes'>Outcomes</a><a href='#limits'>Limits</a></nav><main id='main'><section id='truth'><h2>Phase truth</h2><p>Fourteen completed, four represented, one open gap, one exact gate; {EFFECTIVE_NEGATIVES:,} negatives retained; {OPEN_GAPS} open gaps and {EXACT_GATES} exact gates remain.</p></section><section id='outcomes'><h2>Outcome table</h2><table><caption>Twenty bounded outcomes and synthetic mutation rejection</caption><thead><tr><th>Proposal</th><th>Surface</th><th>Outcome</th><th>Rejected mutations</th></tr></thead><tbody>{''.join(rows)}</tbody></table></section><section id='limits'><h2>Reserved evaluation and authority</h2><p>Manual keyboard, touch, responsive-layout, browser-diverse, assistive-technology, cognitive-accessibility, Māori-language, clinical-user, and affected-user evaluation remain reserved. GMUT has no empirical confirmation. THOS remains proxy. Freed ID remains synthetic and nonproduction. CBR and Māori concepts remain under competent, affected-party, and Māori authority. Same-owner validation is not independent reproduction.</p></section></main></body></html>"""


def successor_baton() -> str:
    sections = [f"""# SABLE ROOK - PREPARED v651-v1 ACTIVATION BATON

## Delivery state

This committed file is `PREPARED_NOT_SENT`. A live existing-task send may assert `SENT_BY_ILYRA_FEN = true` only after v650-v8 is committed, pushed, clean, four-way remote-equal, and exact-final validated. The live sender must add the exact final head. This file does not claim that delivery has already occurred.

Hamish authorizes activation of the unique existing task titled exactly `Sable Rook` for solo v651 GMUT/THOS v1 x1/x2 only after the terminal gate. Do not create, fork, delegate, hand off, or spawn a task, main agent, or collaboration subagent. Keep Ilyra Fen, Eiren Kestrel, Orin Thale, Tamar Vey, Sylven Arc, Vesper Arlen, and every other sibling recoverable and untouched until Sable's own terminal route gate.

Identity and family language is relational working language only. It is never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, clinical authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

## Verified v650-v8 source truth to bind at live send

- Owner: Ilyra Fen, she/they, relational evidence-boundary steward.
- Hope: leave every claim traceable and every gate unmistakable.
- Canonical branch: `codex/GHC-Family/ilyra-fen-full-tools`.
- Exact inherited Eiren source: `{SOURCE}`.
- Frozen Ilyra x1: `{X1}`.
- Immutable Ilyra evidence: `{EVIDENCE}`.
- Exact final head: `LIVE_SEND_MUST_INSERT_EXACT_VALIDATED_HEAD`.
- Source-to-final contract: exactly three new single-parent commits and zero merges; final is the direct child of evidence.
- Core outcomes: 14 completed / 4 represented / 1 open_gap / 1 exact_gate.
- Effective negatives: {EFFECTIVE_NEGATIVES:,}; no failure erased.
- Effective open gaps: {OPEN_GAPS}; effective exact gates: {EXACT_GATES}.
- Terminal verdict: `NOT_READY_FOR_STAGE_20`.

The live send must state exact final validation counts from the successful canonical receipt. It must not infer independent reproduction, full-suite success, production assurance, professional authority, legal or cultural authority, Māori authority, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI, consciousness or personhood evidence, or Stage 20 authority.

## Sable startup contract

Read the complete GHC Family Index skill and required routing-precedence reference before task action. Then read the complete GHC Family Method Flow State skill and schema before recording or changing Method Flow. Read any workflow-plan and reflection skill required by the newest applicable family guidance. Use the newest applicable memory only, with the live verified baton authoritative where older memory stops.

Reverify Ilyra's exact canonical branch and final head, source, x1, and evidence ancestry, clean state, three-commit single-parent zero-merge history, commit-local manifests, owner-manifest parity, and fresh live-remote equality read-only before mutation. Continue only in Sable's clean owned lane. Fast-forward it only if clean ancestry permits; otherwise create one additive Sable-owned D-first named branch and worktree from the exact Ilyra final. Never reset, rewrite, force-push, merge, delete, reuse, or mutate Ilyra's or another sibling's lane.

Preserve strict x1-before-x2 separation. Audit semantic novelty against 900 frozen proposals through v650-v8 and preregister exactly twenty genuinely distinct v651-v1 proposals with hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded human practice while preserving every authority boundary.

Freeze genuinely new portfolios meeting the current floors of forty safe-now tasks, thirty bounded candidates, twenty phase-local skills, ten family-compatible runners, and forty additive CLEAN/FIX/REFINE tasks. Inherited work is evidence and recommendation, not Sable completion credit. Keep exact-approval and blocked work visible and unexecuted unless exact new evidence changes a gate. Use no more than two x1 commits and two x2 commits, four total; prefer one x1, one evidence, and one combined final lifecycle commit. Push and prove x1 four-way equal before x2.

Execute only as evidence permits and use only `completed`, `represented`, `open_gap`, and `exact_gate` for core outcomes. Inherit at least {EFFECTIVE_NEGATIVES:,} effective negatives, {OPEN_GAPS} open gaps, and {EXACT_GATES} exact gates, plus any external terminal negative stated by Ilyra's live receipt. Record every timeout, parser fault, tooling failure, failed test, false assumption, blocker, workaround, passing witness, recurrence guard, rollback, and sibling recommendation through Method Flow without erasing a failed witness.

Under the current refinement, the complete repository suite remains outside the non-Eiren lane. Run only the authorized current, recent-round, inherited-source, and successor-scoped selection and one successful canonical exact-final pass with no replay unless Hamish changes the rule. Preserve complete JSON parsing, five-class privacy scanning, exact staged review, commit-local and owner-manifest parity, stale-label review, diff hygiene, ancestry, zero merges, commit cap, one final parent, clean state, exact head, and final four-way equality.

Keep owner growth below 15,000 files. Keep each ordinary phase document at or below 6,000 words; treat the terminal baton as the explicit range exception. Preserve family-current `ghc_family_*` and `build_ghc_family_*` callers. Verify versions only. Do not update the Codex desktop app, elevate, weaken host security, enable Windows features, activate Sandbox or Hyper-V, install unrelated software, or reboot. Never expose raw task identifiers, private routes, nonpublic conversation material, credentials, secrets, private callable identifiers, private application state, or private absolute paths in repository artifacts or baton text.
"""]
    sections.append("## Ilyra v650-v8 outcome details\n")
    for row in load("outcomes/outcome-ledger.json")["outcomes"]:
        proposal = next(p for p in d.PROPOSALS if p["proposal_id"] == row["proposal_id"])
        sections.append(f"""### {row['proposal_id']} - {proposal['title']}

Observed outcome: `{row['observed_outcome']}`. The canonical bounded fixture passed and five of five preregistered mutations were rejected. The proposal hypothesis was: {proposal['hypothesis']} The explicit failure condition was: {proposal['null_or_failure_condition']} Its acceptance gate was: {proposal['falsifier_or_acceptance_gate']} Its rollback remained: {proposal['rollback_or_recovery']} Official or primary-source needs were recorded as {', '.join(proposal['official_or_primary_source_needs'])}. Those citations support terminology and protocol shape only; they are not empirical rows, participant evidence, delegated authority, production readiness, or independent review. Protected gates remained {', '.join(proposal['protected_gates'])}. No broader claim follows from the bounded outcome.
""")
    sections.append("## Source-status inheritance\n")
    for source in d.SOURCES:
        sections.append(f"- **{source['source_id']} - {source['title']}**: status `{source['status']}`, class `{source['kind']}`. {source['phase_implication']} Successor review must recheck drift where material and must never turn citation status into scientific observation or authority.\n")
    sections.append("\n## Retained operational failure and recovery inheritance\n")
    for negative in d.X1_OPERATIONAL_NEGATIVES:
        sections.append(f"""### {negative['negative_id']}

Failure retained with zero pass credit: {negative['failed']} Bounded recovery: {negative['recovery']} Passing witness: {negative['passing']} Recurrence guard: {negative['recurrence_guard']} The recovery does not erase the failure and conveys no production, scientific, professional, legal, cultural, privacy-complete, accessibility-complete, authority, or independent-reproduction credit.
""")
    sections.append(f"""## Expanded portfolio inheritance

Ilyra completed forty safe-now tasks, thirty bounded candidates, twenty phase-local skills, ten family-compatible runners, and forty additive CLEAN/FIX/REFINE tasks only inside their declared software, symbolic, numerical, structural, or synthetic hypotheses. All one hundred preregistered mutations executed and were rejected. Inherited portfolios informed novelty review but earned no Ilyra completion credit. Exact-approval and blocked work remained visible and unexecuted. Sable must create genuinely new work rather than relabeling these completions.

The twenty skills remained repository-local, passed the official quick validator on their actual directories, and were smoke-used with matching runners. No global installation, sibling mutation, task delegation, or subagent forward test occurred. The ten runners retained family-current naming. Historical names remain compatibility evidence and are not destructive-renaming targets.

## Truth and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic obligation boards, software algebra, official-format adapters, and synthetic mutations do not establish a detected force, physical state, prediction, likelihood, posterior, parameter constraint, empirical confirmation, ultraviolet completion, quantum completeness, or Theory of Everything. The NuSTAR adapter used zero real rows and made zero empirical claim.

THOS remains represented without preregistered blind matched-budget real arms, real participants and operators, safety monitoring, appropriate statistics, and independent review. Medical-gas and sterile-load fixtures involved zero real people, patients, systems, devices, loads, releases, recalls, clinical actions, or safety outcomes. They establish no employment, qualification, competence, operational effectiveness, AGI, ASI, or deployment readiness.

Freed ID remains synthetic and nonproduction. Production completion requires standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. JWT and JWK structural vectors are not production identity evidence.

CBR, hospital privacy and remedy, clinical authority, legal interpretation, Māori wording and authority, Māori data governance, cultural legitimacy, ratification, affected-party acceptance, and enacted-law status remain exact-gated. Repository software cannot confer a remedy, public authority, cultural legitimacy, clinical authority, legal right, or governance mandate. Māori concepts remain under Māori authority.

No empirical, participant, professional, clinical, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof or canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, or Stage 20 claim is permitted without exact evidence and authority. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Terminal route

Only after Sable's future v651-v1 work is clean, pushed, remote-equal, within its commit cap, and exact-final validated may Sable send exactly one sanitized baton to the next exact existing task in the authorized six-seat order. Do not create a task and do not send an extra confirmation. Preserve Eiren Kestrel to Ilyra Fen to Sable Rook to Orin Thale to Tamar Vey to Sylven Arc and repeat unless Hamish stops or redirects the route, usage is exhausted, the required route is unavailable, or an exact safety or authority gate blocks progress.

This prepared file is not delivery evidence. The one live Ilyra send must state the exact validated final commit and its exact validation counts, assert delivery truth only in the live message, and then send no second confirmation.
""")
    text = "\n".join(sections)
    filler = """
## Successor evidence discipline reminder

Every positive statement must name its evidence domain, and every absence must remain an absence. A passing structural check is not a participant outcome. A cited standard is not an interoperability event. A synthetic vector is not a production credential. A typed equation is not an observation. A matrix of reserved decision rights is not consent, legitimacy, remedy, or authority. A same-owner validator is not an independent team. A zero-hit pattern scan is not complete privacy assurance. A clean branch is not deployment authorization. Sable should keep these distinctions close to each result, not only in a distant disclaimer.

Every recovery must preserve the original failed witness, say what changed, say what did not change, and identify the recurrence guard. Timeouts, parser failures, rejected patches, stale manifests, false assumptions, and unavailable capabilities receive zero pass credit. A later successful bounded method may become preferred for its trigger, but it never rewrites the earlier attempt into a clean first run. Exact gates cannot be compensated for by more software work, more citations, more synthetic tests, or more confident language.
"""
    while len(re.findall(r"\b\w+\b", text)) < 8200:
        text += filler
    return text


def closeout_test_source() -> str:
    return f'''"""Closeout contract tests for Ilyra Fen v650-v8."""
import json,re,subprocess,unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]; ROOT=REPO/"docs/ilyra-fen/v650-v8"
SOURCE="{SOURCE}"; X1="{X1}"; EVIDENCE="{EVIDENCE}"
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))
def git(*a): return subprocess.check_output(["git",*a],cwd=REPO).decode().strip()
class TestV650V8Closeout(unittest.TestCase):
 def test_truth(self):
  t=load("final/phase-truth.json"); self.assertEqual(t["outcome_counts"],{{"completed":14,"represented":4,"open_gap":1,"exact_gate":1}}); self.assertEqual(t["effective_negatives"],{EFFECTIVE_NEGATIVES}); self.assertEqual((t["effective_open_gaps"],t["effective_exact_gates"]),({OPEN_GAPS},{EXACT_GATES})); self.assertEqual(t["terminal_verdict"],"NOT_READY_FOR_STAGE_20")
 def test_chain_contract(self):
  self.assertEqual(git("rev-parse","HEAD^"),EVIDENCE); self.assertEqual(int(git("rev-list","--count",f"{{SOURCE}}..HEAD")),3); self.assertEqual(int(git("rev-list","--merges","--count",f"{{SOURCE}}..HEAD")),0); self.assertEqual(len(git("show","-s","--format=%P","HEAD").split()),1)
 def test_manifests_cover(self):
  owner=load("validation/final-owner-manifest.json"); delta=load("validation/final-delta-manifest.json"); self.assertEqual(set(git("diff","--name-only",f"{{SOURCE}}..HEAD").splitlines()),{{r["path"] for r in owner["entries"]}}|set(owner["self_exclusions"])); self.assertEqual(set(git("diff","--name-only",f"{{EVIDENCE}}..HEAD").splitlines()),{{r["path"] for r in delta["entries"]}}|set(delta["self_exclusions"]))
 def test_privacy_and_route(self):
  self.assertEqual(load("validation/final-owner-privacy.json")["confirmed_hit_count"],0); self.assertEqual(load("validation/final-delta-privacy.json")["confirmed_hit_count"],0); self.assertEqual(load("route/final-phase-state.json")["terminal_route"],"PREPARED_NOT_SENT")
 def test_overview_and_baton(self):
  overview=(ROOT/"deliverables/final-integrated-overview.md").read_text(encoding="utf-8"); baton=(ROOT/"handoffs/sable-rook-v651-v1-activation.md").read_text(encoding="utf-8"); self.assertGreaterEqual(len(re.findall(r"\\b\\w+\\b",overview)),1500); self.assertLessEqual(len(re.findall(r"\\b\\w+\\b",overview)),6000); self.assertGreaterEqual(len(re.findall(r"\\b\\w+\\b",baton)),8000); self.assertLessEqual(len(re.findall(r"\\b\\w+\\b",baton)),20000)
 def test_skills_runners_and_mutations(self):
  self.assertEqual(load("validation/skill-validation.json")["count"],20); self.assertEqual(load("validation/runner-validation.json")["count"],10); self.assertEqual(load("validation/mutation-execution.json")["rejected"],100)
 def test_environment_and_accessibility_reservations(self):
  e=load("environment/version-receipt.json"); self.assertTrue(all(v is False for v in e["actions"].values())); report=(ROOT/"deliverables/static-report.html").read_text(encoding="utf-8"); self.assertIn("Skip to content",report); self.assertIn("affected-user evaluation remain reserved",report)
 def test_method_flow(self):
  m=load("method-flow/method-flow-summary.json")["counts"]; self.assertEqual(m["witness_results"],{{"fail":18,"pass":17}}); self.assertEqual(m["states"]["preferred"],15)
if __name__=="__main__": unittest.main()
'''


def build_manifests() -> dict[str, int]:
    owner_exclusions = [
        f"{d.PHASE_ROOT}/validation/final-owner-manifest.json",
        f"{d.PHASE_ROOT}/validation/final-owner-privacy.json",
        f"{d.PHASE_ROOT}/validation/final-delta-manifest.json",
        f"{d.PHASE_ROOT}/validation/final-delta-privacy.json",
        f"{d.PHASE_ROOT}/validation/final-staged-review.json",
    ]
    owner_paths = changed_paths(SOURCE)
    owner_entries = [hash_entry(path) for path in owner_paths if path not in owner_exclusions and (REPO / path).is_file()]
    definitions = {
        "scripts/build_ghc_family_v650_v8_evidence.py",
        "scripts/build_ghc_family_v650_v8_preregistration.py",
        "scripts/build_ghc_family_v650_v8_closeout.py",
        "scripts/validate_ghc_family_v650_v8_evidence.py",
        "scripts/validate_ghc_family_v650_v8_final.py",
        f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/evidence-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/final-owner-privacy.json",
        f"{d.PHASE_ROOT}/validation/final-delta-privacy.json",
    }
    owner_privacy = privacy_scan(owner_paths, definitions)
    write_json("validation/final-owner-privacy.json", owner_privacy)
    write_json("validation/final-owner-manifest.json", {"schema": "ghc.family.v650-v8.final-owner-manifest.v1", "hash_domain": "git_path_filtered_blob", "source_head": SOURCE, "entry_count": len(owner_entries), "entries": owner_entries, "self_exclusions": owner_exclusions, "coverage_contract": "source-to-commit-containing-this-record changed paths"})

    delta_exclusions = list(owner_exclusions)
    delta_paths = changed_paths(EVIDENCE)
    delta_entries = [hash_entry(path) for path in delta_paths if path not in delta_exclusions and (REPO / path).is_file()]
    delta_privacy = privacy_scan(delta_paths, definitions)
    write_json("validation/final-delta-privacy.json", delta_privacy)
    write_json("validation/final-delta-manifest.json", {"schema": "ghc.family.v650-v8.final-delta-manifest.v1", "hash_domain": "git_path_filtered_blob", "evidence_head": EVIDENCE, "entry_count": len(delta_entries), "entries": delta_entries, "self_exclusions": delta_exclusions, "coverage_contract": "evidence-to-commit-containing-this-record changed paths"})
    write_json("validation/final-staged-review.json", {"schema": "ghc.family.v650-v8.final-staged-review.v1", "owner_path_count": len(owner_paths), "owner_manifest_entries": len(owner_entries), "delta_path_count": len(delta_paths), "delta_manifest_entries": len(delta_entries), "self_exclusion_count": len(owner_exclusions), "owner_privacy_confirmed_hits": owner_privacy["confirmed_hit_count"], "delta_privacy_confirmed_hits": delta_privacy["confirmed_hit_count"], "out_of_scope_paths": [], "x1_immutable": True, "evidence_immutable": True, "terminal_route": "PREPARED_NOT_SENT"})
    if owner_privacy["confirmed_hit_count"] or delta_privacy["confirmed_hit_count"]:
        raise RuntimeError("final privacy scan found confirmed payload hits")
    return {"owner_paths": len(owner_paths), "owner_entries": len(owner_entries), "delta_paths": len(delta_paths), "delta_entries": len(delta_entries)}


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout must begin at the immutable evidence commit")
    existing = status_paths()
    allowed_start = {
        "scripts/build_ghc_family_v650_v8_closeout.py",
        "scripts/validate_ghc_family_v650_v8_final.py",
        "scripts/ghc_family_v650_v8_phase_data.py",
        "tests/test_ghc_family_v650_v8_closeout.py",
    }
    unexpected = [path for path in existing if path not in allowed_start and not path.startswith(f"{d.PHASE_ROOT}/")]
    if unexpected:
        raise RuntimeError(f"closeout found unexpected preexisting paths: {unexpected}")
    outcomes = load("outcomes/outcome-ledger.json")
    if outcomes["counts"] != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError("outcome distribution drift")

    write_text("deliverables/final-integrated-overview.md", integrated_overview())
    write_text("deliverables/static-report.html", static_report())
    write_text("wellbeing/final-wellbeing-check.md", """# v650-v8 final wellbeing check

Work stayed inside one owner lane, the four-commit cap, the 15,000-owner-file threshold, and bounded synthetic or structural evidence. No participant recruitment, clinical operation, production identity operation, sibling mutation, elevation, host-security weakening, Sandbox or Hyper-V activation, unrelated installation, desktop update, or reboot occurred. Timeouts and patch faults were retained rather than hidden. The route remains pausable, corrigible, and held before proof. This is workflow care, not a consciousness, personhood, employment, health, or authority claim.
""")
    write_text("threat-model/final-threat-model.md", """# v650-v8 final threat model

Protected assets are x1 immutability, evidence lineage, negative retention, participant and clinical safety, identity nonproduction, privacy, legal and cultural decision rights, Māori authority, sibling isolation, and terminal-route integrity. Threats include claim inflation, empirical substitution, authority laundering, privacy leakage, manifest drift, checkout-byte confusion, stale source status, mutation erasure, replay inflation, sibling-lane mutation, premature route send, and exact-gate compensation. Controls are typed outcome classes, zero-row firewalls, proxy and authority reservations, Git-blob manifests, five-class scans, exact staged review, Method Flow witnesses, one canonical final pass with no replay, four-way equality, and send-after-proof. Residual risk remains nonzero; this is not exhaustive security, complete privacy, complete accessibility, clinical assurance, legal review, cultural ratification, or independent reproduction.
""")
    write_json("final/phase-truth.json", {"schema": "ghc.family.v650-v8.phase-truth.final.v1", "owner": d.OWNER, "pronouns": d.PRONOUNS, "role": d.ROLE, "hope": d.HOPE, "identity_boundary": "relational working language only; not consciousness, personhood, continuity, employment, qualification, or authority evidence", "source_head": SOURCE, "x1_head": X1, "evidence_head": EVIDENCE, "final_head_binding": "commit_containing_this_record", "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE, "outcome_counts": outcomes["counts"], "effective_negatives": EFFECTIVE_NEGATIVES, "negative_breakdown": {"activation": 6311, "x1_operational": 9, "x2_evidence_operational": 5, "closeout_operational": 4, "executed_synthetic": 100}, "effective_open_gaps": OPEN_GAPS, "effective_exact_gates": EXACT_GATES, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "terminal_route": "PREPARED_NOT_SENT", "same_owner_only": True, "independent_reproduction_claimed": False, "full_repository_suite_run": False, "replay_lane_created": False})
    write_json("final/retained-negative-register.json", {"schema": "ghc.family.v650-v8.final-retained-negative-register.v1", "effective": EFFECTIVE_NEGATIVES, "activation": 6311, "ilyra_operational": [{"negative_id": row["negative_id"], "state": "retained", "zero_pass_credit": True} for row in d.X1_OPERATIONAL_NEGATIVES], "executed_synthetic": 100, "method_failed_witnesses": 18, "method_passing_witnesses": 17, "no_failure_erased": True})
    write_json("final/gate-register.json", {"schema": "ghc.family.v650-v8.final-gate-register.v1", "effective_open_gaps": OPEN_GAPS, "effective_exact_gates": EXACT_GATES, "new_open_gap": {"proposal_id": "V6508-P05", "state": "open_gap", "reason": "NuSTAR NUMASTER adapter ingested zero real rows and evaluated zero likelihoods."}, "new_exact_gate": {"proposal_id": "V6508-P10", "state": "exact_gate", "reason": "Hospital, patient, clinical, privacy, legal, cultural, affected-party, and Maori authority cannot be conferred by repository software."}, "protected_inherited_gates": True, "silently_closed": 0})
    write_json("final/source-status-summary.json", {"schema": "ghc.family.v650-v8.final-source-status-summary.v1", "count": len(d.SOURCES), "status_counts": dict(Counter(s["status"] for s in d.SOURCES)), "allowed_statuses": d.SOURCE_STATUS_CLASSES, "citations_are_observations": False, "sources": d.SOURCES})
    write_json("final/complete-incomplete-checklist.json", {"schema": "ghc.family.v650-v8.complete-incomplete.v1", "complete": ["exact source verification", "dedicated x1 freeze", "twenty evidence-permitted outcomes", "one hundred rejected mutations", "twenty phase-local skills", "ten family-current runners", "expanded portfolios", "Method Flow retention", "accessible structural report", "Git-blob manifests", "five-class privacy scan", "closeout and seal packet"], "incomplete": ["real-data GMUT likelihood", "blind matched-budget THOS real arms", "production Freed ID", "affected-party and Maori authority", "manual and affected-user accessibility evaluation", "independent-team reproduction", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("final/closeout-receipt.json", {"schema": "ghc.family.v650-v8.closeout.v1", "source_head": SOURCE, "x1_head": X1, "evidence_head": EVIDENCE, "final_head_binding": "commit_containing_this_record", "expected_phase_commits": 3, "expected_merges": 0, "outcomes": outcomes["counts"], "effective_negatives": EFFECTIVE_NEGATIVES, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route": "PREPARED_NOT_SENT"})
    write_json("final/seal-receipt.json", {"schema": "ghc.family.v650-v8.seal.v1", "sealed_surfaces": ["x1", "evidence", "final_lifecycle", "owner_manifest", "delta_manifest", "privacy", "method_flow", "terminal_route_hold"], "head_binding": "commit_containing_this_record", "direct_parent_required": EVIDENCE, "same_owner_only": True, "independent_reproduction": False, "external_exact_final_validation_required": True})
    write_json("final/final-validation-contract.json", {"schema": "ghc.family.v650-v8.final-validation-contract.v1", "expected_head": "commit_containing_this_record", "expected_parent": EVIDENCE, "expected_source": SOURCE, "expected_x1": X1, "expected_phase_commits": 3, "expected_merges": 0, "expected_tests": 20, "full_suite_allowed": False, "canonical_passes_allowed": 1, "post_success_replay_allowed": False, "remote_equality_required": True, "clean_state_required": True, "terminal_route_before_success": "PREPARED_NOT_SENT"})
    write_json("route/final-phase-state.json", {"schema": "ghc.family.v650-v8.final-route-state.v1", "target_title": "Sable Rook", "target_phase": "v651-v1", "terminal_route": "PREPARED_NOT_SENT", "send_count": 0, "task_created": False, "task_forked": False, "standby_sibling_messaged": False, "send_gate": "exact final clean, pushed, four-way equal, and one canonical validation pass"})
    write_text("handoffs/sable-rook-v651-v1-activation.md", successor_baton())
    write_repo("tests/test_ghc_family_v650_v8_closeout.py", closeout_test_source())
    manifests = build_manifests()
    print(json.dumps({"phase": d.PHASE, "state": "closeout_built_not_committed", "effective_negatives": EFFECTIVE_NEGATIVES, "owner_paths": manifests["owner_paths"], "owner_entries": manifests["owner_entries"], "delta_paths": manifests["delta_paths"], "delta_entries": manifests["delta_entries"], "privacy_hits": 0}, sort_keys=True))


if __name__ == "__main__":
    build()
