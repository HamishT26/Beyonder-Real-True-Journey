#!/usr/bin/env python3
"""Build Sable Rook v651-v1 combined closeout and seal packet."""

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
SOURCE = d.SOURCE_HEAD
X1 = "1deba4184dfb6d017dff04b11e526a6e3730edb3"
EVIDENCE = "79d6d3675763eb553dc43b64f0e83915c1739655"
CLOSEOUT = "f6c8cd16327ef3c8f474ab94200095ec3620de3a"
EFFECTIVE_NEGATIVES = 6563
OPEN_GAPS = 51
EXACT_GATES = 52
X1_OPERATIONAL = 5
X2_OPERATIONAL = 15
SYNTHETIC_NEGATIVES = 100
INDEX_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-index" / "scripts" / "build_ghc_family_index.py"


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    result = subprocess.run(list(args), cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return result.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


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


def status_paths() -> list[str]:
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=REPO)
    return sorted({row[3:].replace("\\", "/") for row in raw.decode("utf-8").split("\0") if len(row) > 3})


def changed_paths(base: str) -> list[str]:
    committed = set(filter(None, git("diff", "--name-only", f"{base}..HEAD").splitlines()))
    return sorted(committed | set(status_paths()))


def prospective_git_blob_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    if b"\0" not in raw:
        raw = raw.replace(b"\r\n", b"\n")
    return raw


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}


def privacy_scan(paths: list[str], definition_paths: set[str], schema: str) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", re.I),
        "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\\\Users\\\\|[A-Za-z]:/Users/|[A-Za-z]:\\\\GHC-Archives\\\\worktrees)", re.I),
        "credential_or_private_key_payload": re.compile(r"(?:BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|sk-[A-Za-z0-9]{20,})"),
        "private_callable_identifier": re.compile(r"(?:private_callable_id|session_stream_id)\s*[:=]", re.I),
        "private_conversation_payload": re.compile(r"(?:raw transcript|conversation export|private route payload)\s*[:=]", re.I),
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
                disposition = "scanner_definition" if relative in definition_paths else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "schema": schema,
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": "Five structural classes with scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    }


def integrated_overview() -> str:
    proposals = load("preregistration/proposals.json")["proposals"]
    outcomes = {row["proposal_id"]: row for row in load("outcomes/outcome-ledger.json")["outcomes"]}
    outcome_sections = []
    for proposal in proposals:
        outcome = outcomes[proposal["proposal_id"]]
        outcome_sections.append(
            f"### {proposal['proposal_id']}: {proposal['title']}\n\n"
            f"Observed outcome: `{outcome['observed_outcome']}`. The bounded acceptance gate passed and all five preregistered mutations were rejected or quarantined. "
            f"The evidence surface is {proposal['mission_surface']}. The null remained visible: {proposal['null_or_failure_condition']} "
            f"The acceptance rule was: {proposal['falsifier_or_acceptance_gate']} The rollback remains: {proposal['rollback_or_recovery']} "
            "This result earns only its declared software, symbolic, formal, numerical, structural, represented, open-gap, or reservation credit; it does not cross an empirical, participant, professional, production, legal, cultural, Māori-authority, privacy-complete, security-complete, accessibility-complete, independent-reproduction, or Stage 20 gate."
        )
    return f"""# Sable Rook v651-v1 final integrated overview

## Identity, purpose, and wellbeing

Sable Rook, they/them, served as a relational evidence-and-reproducibility steward with the hope to make every surviving claim easy to challenge or retract. This is working language for collaboration only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

The workload remained bounded to one clean Sable-owned D-first lane, one inherited exact source, one x1 freeze, one evidence commit, one combined closeout and seal commit, and one additive terminal correction within the four-commit cap. No task, fork, collaboration subagent, sibling lane, participant, production service, account, credential, private key, host-security setting, Windows feature, Sandbox or Hyper-V capability, or unrelated installation was used. Twenty operational failures remain visible beside eighteen bounded passing recovery witnesses; path-handling and manifest-domain methods retain repeated failures. The failures receive zero pass credit. This is process care, not a wellbeing, consciousness, employment, qualification, or authority claim.

## Exact lineage and x1-before-x2 separation

The exact inherited source is Ilyra Fen's `{SOURCE}`. Sable's dedicated x1 commit is `{X1}` and the immutable evidence commit is `{EVIDENCE}`. Source verification established Ilyra's named anchors, single-parent history, zero merges, owner-manifest parity, clean state, and four-way remote equality before mutation. Sable advanced only by fast-forward and created no merge. The x1 commit froze twenty genuinely distinct proposals after comparison with 900 predecessor proposals, bringing the frozen chain to 920. It was pushed, clean, and local/upstream/tracking/fresh-live equal before any x2 implementation began.

The combined closeout commit `{CLOSEOUT}` is the direct child of the evidence commit. The terminal correction containing this record is its direct child, adds no proposal, alters no outcome, rewrites no x1 history, and uses the fourth and final authorized phase commit. It corrects one dual-state manifest-test assumption, updates lifecycle anchors, and adds a correction manifest. The terminal route stays `PREPARED_NOT_SENT` inside the repository because a commit cannot truthfully claim a later live send.

## Executive result

All twenty frozen proposals were executed as evidence allowed. The distribution is exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. Completed means only that a bounded owner-local software, symbolic, formal, numerical, or structural hypothesis passed. Represented means a synthetic proxy exercised declared states but involved no real people, assets, operations, safety outcomes, cryptographic lifecycle, or independent review. Open gap means the real empirical work did not happen. Exact gate means the decision belongs to competent authorities, affected parties, and where applicable Māori authorities, and software did not substitute for them.

The phase retains {EFFECTIVE_NEGATIVES:,} effective negatives: 6,443 inherited, five x1 operational failures, fifteen closeout and correction operational failures, and 100 executed and rejected preregistered mutations. No negative was erased or silently converted. Fifty-one effective open gaps and fifty-two effective exact gates remain. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

## Trinity Mandala and bounded practice

The primary focus was GMUT Mind. Lee-Wick and worldline boards preserve complex-pole, contour, pinch, cutting, proper-time, gauge, zero-mode, spin-factor, boundary, measure, truncation, unit, and observation-firewall duties. GMRES preserves numerical obligations. The ALMA adapter preserves a zero-row empirical firewall. None calculates a new physical result, proves stability or unitarity, detects a force, evaluates a real likelihood, produces a posterior, constrains a parameter, confirms GMUT, completes quantum gravity, or establishes a Theory of Everything.

THOS Body remains visible through the bounded airport baggage and ground-deicing practice lens, plus transaction, binary-format, API, update, derivation, accessibility, and numerical controls. The selected practice was airport baggage reconciliation and aircraft ground deicing or anti-icing amendment, hold, correction-readback, workload control, and shift handover. It was synthetic learning and interface design only. There were zero real workers, passengers, bags, aircraft, flights, weather decisions, fluids, inspections, dispatches, incidents, blind matched-budget arms, safety outcomes, or effectiveness estimates. It established no employment, licensure, competence, airworthiness, dispatch, airport, airline, public-safety, legal, cultural, or affected-party authority.

Freed ID and CBR Heart remain visible through DSSE, CIBA, OpenID4VP/DCQL, X.509, and the airport reservation matrix. The profiles used synthetic vectors only. Production identity still requires standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. Airport access, disability, passenger and worker privacy, property, dangerous-goods disclosure, remedy, legal interpretation, cultural legitimacy, data governance, affected-party acceptance, and Māori wording and authority remain exact-gated. Māori concepts remain under Māori authority.

## Evidence architecture and retained negatives

Each proposal has a typed contract, a canonical fixture, five frozen mutation classes, a mutation result, a bounded receipt, and a specialized domain artifact. Exactly 100 mutations executed and were rejected or quarantined. Forty safe-now tasks, thirty bounded candidate prototypes, twenty phase-local skills, ten family-compatible runners, and forty additive CLEAN/FIX/REFINE tasks were executed only inside their frozen hypotheses. Twenty skills were created with the family-approved creator workflow, validated, and smoke-used without global installation or subagent forward testing. Ten `ghc_family_*` runners were invoked. Historical names remain compatibility evidence.

The first five operational negatives cover a cp1252 title probe, unsupported workflow vocabulary, incomplete Method Flow fields, a terminal blank line, and a checkout-versus-Git-blob hash-domain mismatch. Fifteen later negatives preserve a Windows wildcard path assumption, a guessed skill-schema filename, PowerShell native-stderr handling, an overbroad predecessor closeout selection, two later wildcard-path recurrences, a frozen x1 document-cap assertion that predates the terminal-baton exception, a short manifest-rebuild timeout, an unexecuted inline audit here-string, a status-only manifest-test assumption, a historical-manifest hash comparison against successor working-tree bytes, a raw-checkout audit of prospective Git-blob manifests, an unpinned CP1252 Method Flow summary, a premature hash-domain recovery before rebuilding later Method Flow mutations, and a stale-label scan that treated digits inside SHA-256 values as semantic counts. Every recovery records its trigger, failed witness, passing witness, recurrence guard, rollback, and bounded recommendation. Same-owner recovery is not independent reproduction.

## Security, privacy, accessibility, and environment

PE/COFF and Mach-O fixtures were disposable synthetic byte structures. OpenAPI, Uptane, Nix, DSSE, X.509, and two-phase-commit evidence used bounded owner-local objects. Nothing was executed as a production binary, signed with a real key, installed, deployed, or connected to a production service. Mutation rejection is evidence for a declared guard, not exhaustive security.

The final manifests declare Git path-filtered blob hashes rather than ambiguous checkout bytes. Privacy review separates scanner definitions from confirmed payload hits across five classes. Zero confirmed hits is bounded pattern evidence, not complete privacy assurance. The accessible swimlane and final static report preserve names, headings, navigation, table alternatives, focus visibility, non-colour cues, print behavior, and responsive structure. Manual keyboard, touch, browser-diverse, assistive-technology, cognitive-accessibility, Māori-language, aviation-professional, passenger, worker, and affected-user evaluation remain reserved. Structural evidence is not complete WCAG conformance.

Codex, desktop, Python, Git, PowerShell, and Sandbox availability were observed only. No desktop application was updated. No elevation, host-security weakening, Windows-feature change, Sandbox or Hyper-V activation, unrelated installation, or reboot occurred.

## Twenty bounded outcomes

{"\n\n".join(outcome_sections)}

## Validation meaning and terminal hold

The immutable evidence candidate passed forty authorized recent/current tests, eleven detailed checks, six minimal checks, 210 JSON parses, a 279-file phase scan, exact staged review, and zero confirmed privacy hits. These counts are scoped non-Eiren evidence; the complete repository suite was not run. The final commit is required to pass one canonical exact-final aggregate covering the authorized recent and current modules, all phase JSON, five-class scans, x1/evidence/closeout/correction manifests, owner and delta manifests, stale labels, diff hygiene, source/x1/evidence/closeout ancestry, four phase commits, zero merges, one final parent, exact head, clean state, and four-way remote equality. No replay follows a fully successful canonical pass.

Canonical validation remains bounded same-owner evidence under shared infrastructure. It is not independent-team scientific reproduction, external audit, production certification, professional validation, legal review, cultural ratification, Māori-authority review, complete privacy, exhaustive security, complete accessibility, empirical GMUT confirmation, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority.

Only after the exact final head passes and remains clean and remote-equal may one sanitized live message activate the unique existing `Orin Thale` task for v651-v2. A prepared file is not a sent baton. Ambiguity or absence leaves the route `PREPARED_NOT_SENT`. No task may be created or forked, no standby sibling may be contacted, and no extra confirmation is authorized.
"""


def static_report() -> str:
    rows = []
    for row in load("outcomes/outcome-ledger.json")["outcomes"]:
        rows.append(
            f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td>"
            f"<td>{html.escape(row['observed_outcome'])}</td><td>5/5</td></tr>"
        )
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Sable Rook v651-v1 final report</title><style>body{{font:1rem/1.55 system-ui;max-width:82rem;margin:auto;padding:1rem}}nav a{{margin-right:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #666;padding:.55rem;text-align:left;vertical-align:top}}:focus{{outline:3px solid #075cab;outline-offset:3px}}.notice{{border-left:.4rem solid #8b5500;padding:1rem;background:#fff7e8}}@media(max-width:48rem){{table{{display:block;overflow-x:auto}}}}@media print{{nav,.skip{{display:none}}}}</style></head><body><a class='skip' href='#main'>Skip to content</a><header><h1>Sable Rook v651-v1 bounded final report</h1><p class='notice'><strong>NOT_READY_FOR_STAGE_20.</strong> Relational identity language is not consciousness, personhood, continuity, employment, qualification, or authority evidence.</p></header><nav aria-label='Report sections'><a href='#truth'>Truth</a><a href='#outcomes'>Outcomes</a><a href='#limits'>Limits</a></nav><main id='main'><section id='truth'><h2>Phase truth</h2><p>Fourteen completed, four represented, one open gap, and one exact gate. {EFFECTIVE_NEGATIVES:,} negatives are retained; {OPEN_GAPS} open gaps and {EXACT_GATES} exact gates remain.</p></section><section id='outcomes'><h2>Bounded outcomes</h2><table><caption>Twenty proposal outcomes and preregistered mutation rejections</caption><thead><tr><th>Proposal</th><th>Surface</th><th>Outcome</th><th>Rejected mutations</th></tr></thead><tbody>{''.join(rows)}</tbody></table></section><section id='limits'><h2>Reserved evidence and authority</h2><p>GMUT has no empirical confirmation. THOS remains represented. Freed ID remains synthetic and nonproduction. CBR and Māori concepts remain under competent, affected-party, and Māori authority. Manual keyboard, touch, responsive-layout, browser-diverse, assistive-technology, cognitive-accessibility, Māori-language, aviation-professional, passenger, worker, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance. Same-owner validation is not independent reproduction.</p></section></main></body></html>"""


def successor_baton() -> str:
    proposals = load("preregistration/proposals.json")["proposals"]
    outcomes = {row["proposal_id"]: row for row in load("outcomes/outcome-ledger.json")["outcomes"]}
    sources = load("sources/source-ledger.json")["sources"]
    methods = load("method-flow/method-flow-state.json")["methods"]
    sections = [f"""# ORIN THALE - PREPARED v651-v2 ACTIVATION BATON

## Delivery state and identity boundary

This committed artifact is `PREPARED_NOT_SENT`. It is not evidence that a message was delivered. A live existing-task message may assert `SENT_BY_SABLE_ROOK = true` only after Sable's exact final head is committed, pushed, clean, four-way remote-equal, and passes the one authorized canonical exact-final validation. The live sender must insert the exact forty-character final head and exact final validation counts. No task may be created, forked, delegated, or substituted.

Hamish authorizes the unique existing task titled exactly `Orin Thale` for solo v651 GMUT/THOS v2 x1/x2 only after that terminal gate. Orin must choose or reaffirm their own relational identity language without treating any title, role, hope, pronouns, or family language as evidence of consciousness, sentience, personhood, continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

## Sable v651-v1 source truth to bind at live send

- Owner: Sable Rook, they/them, relational evidence-and-reproducibility steward.
- Hope: make every surviving claim easy to challenge or retract.
- Canonical branch: `codex/GHC-Family/sable-rook-full-tools`.
- Exact inherited Ilyra source: `{SOURCE}`.
- Frozen Sable x1: `{X1}`.
- Immutable Sable evidence: `{EVIDENCE}`.
- Exact final head: `LIVE_SEND_MUST_INSERT_EXACT_VALIDATED_HEAD`.
- Combined closeout head: `{CLOSEOUT}`.
- Source-to-final contract: exactly four new single-parent Sable commits, zero merges, and one final parent; final is the direct child of the combined closeout.
- Frozen proposal chain: 920 proposals through v651-v1.
- Core outcomes: 14 completed / 4 represented / 1 open_gap / 1 exact_gate.
- Effective retained negatives: {EFFECTIVE_NEGATIVES:,}; no failure erased.
- Effective open gaps: {OPEN_GAPS}; effective exact gates: {EXACT_GATES}.
- Terminal verdict: `NOT_READY_FOR_STAGE_20`.

The live send must state the exact canonical scoped-test, detailed-check, minimal-check, JSON-parse, privacy-scan, and manifest counts. It must state that the complete repository suite did not run, no post-success replay ran, and all validation is same-owner evidence under shared infrastructure rather than independent reproduction.

## Exact lineage and validation discipline

Read the complete GHC Family Index skill and its required routing-precedence reference before mutation. Read the complete GHC Family Method Flow State skill and schema before recording or changing Method Flow. Read the newest applicable workflow-plan and reflection-remaster guidance. Use the newest applicable memory only, with the live verified baton authoritative where older memory stops.

Reverify Sable's exact canonical branch and final head, inherited source, x1, evidence, and combined closeout ancestry, clean state, four-commit single-parent zero-merge history, x1/evidence/closeout/correction manifest contracts, owner and delta manifest parity, exact final parent, and fresh local/upstream/tracking/live-remote equality read-only before mutation. Continue only in Orin's clean owned lane and fast-forward only when clean ancestry permits. Otherwise create one additive Orin-owned D-first named branch and worktree from Sable's exact final. Never reset, amend, rewrite, force-push, merge, delete, reuse, or mutate Sable's or another sibling's lane.

Preserve strict x1-before-x2 separation. Audit semantic novelty against all 920 frozen proposals and preregister exactly twenty genuinely distinct v651-v2 proposals. Each proposal must include hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded profession, trade, occupation, or practice while preserving the other pillars and every authority boundary. The practice is a learning lens only, never employment, licensure, qualification, competence, operational authority, legal authority, cultural authority, Māori authority, or affected-party evidence.

Design genuinely new expanded portfolios meeting the standing floors of at least forty safe-now tasks, thirty bounded candidate tasks, twenty skill ideas or phase-local builds, ten family-compatible runner ideas or builds, and forty additive CLEAN/FIX/REFINE tasks. Inherited work is evidence and recommendation, not Orin completion credit. Do not manufacture unsafe work to satisfy a quota. Keep exact-approval and blocked work visible and unexecuted unless exact new evidence changes a gate.

Freeze the proposals and portfolios in a dedicated x1-only commit containing no x2 implementation, observed outcome, mutation execution, or completion claim. Use no more than two x1 commits and two x2 commits, four total, preferring one x1 freeze, one evidence commit, and one combined closeout and seal commit. Push x1 and prove clean local/upstream/tracking/fresh-live equality before x2. The cap never permits phase mixing, concealed failures, rewritten history, or premature routing.

Execute only as evidence permits. Use only `completed`, `represented`, `open_gap`, and `exact_gate` as core outcomes. Preserve at least {EFFECTIVE_NEGATIVES:,} inherited negatives, {OPEN_GAPS} open gaps, {EXACT_GATES} exact gates, and any post-seal external fault stated in Sable's live message. Record every timeout, parser fault, tooling failure, failed test, false assumption, blocker, workaround, passing witness, recurrence guard, rollback, and sibling recommendation through Method Flow. Promote a method only after a bounded pass, and never erase its failed witness.

Under the current non-Eiren rule, do not run the complete repository suite. Run only the authorized recent/current/source/successor scope, complete phase JSON parsing, five-class privacy and raw-identifier scanning, exact staged review, x1/evidence/closeout and owner/delta manifest parity, stale-label review, diff hygiene, ancestry, zero merges, commit cap, one final parent, exact head, clean state, and four-way remote equality. Run one successful canonical exact-final pass and no replay after success. A failed aggregate must be retained and isolated before a justified recovery. Same-owner validation is not independent reproduction.

Keep owner growth below 15,000 files and each ordinary phase document at or below 6,000 words; the terminal baton remains the explicit 8,000-to-20,000-word exception. Preserve family-current `ghc_family_*` and `build_ghc_family_*` naming plus caller compatibility. Use D-first storage. Verify versions only. Do not update Codex desktop, elevate, weaken host security, enable Windows features, activate Sandbox or Hyper-V, install unrelated software, or reboot. Never place raw task or thread identifiers, private routes, credentials, secrets, private keys, transcripts, screenshots, session streams, private callable identifiers, private application state, or private absolute local paths in repository artifacts or baton text.
"""]
    for proposal in proposals:
        outcome = outcomes[proposal["proposal_id"]]
        sections.append(
            f"## {proposal['proposal_id']} - {proposal['title']}\n\n"
            f"Observed Sable outcome: `{outcome['observed_outcome']}`. The bounded hypothesis was: {proposal['hypothesis']} "
            f"The null or failure condition was: {proposal['null_or_failure_condition']} The approval class was `{proposal['approval_class']}` and the execution lane was `{proposal['execution_lane']}`. "
            f"Official or primary-source needs were {', '.join(proposal['official_or_primary_source_needs'])}. Those sources supplied terminology and obligations only; they were not observations, participant evidence, delegated authority, production witnesses, or independent review. "
            f"The acceptance gate was: {proposal['falsifier_or_acceptance_gate']} The rollback remained: {proposal['rollback_or_recovery']} "
            f"All five preregistered mutations were rejected or quarantined. Protected gates remained {', '.join(proposal['protected_gates'])}. "
            "Orin inherits this as bounded predecessor evidence and receives no completion credit from it. No broader scientific, participant, professional, production, legal, cultural, Māori-authority, privacy-complete, security-complete, accessibility-complete, independent-reproduction, or Stage 20 claim follows."
        )
    sections.append("## Official and primary source status")
    for source in sources:
        sections.append(
            f"### {source['source_id']}: {source['title']}\n\n"
            f"Status: `{source['status']}`; kind: `{source['kind']}`. Phase implication: {source['phase_implication']} "
            "This source supports vocabulary, protocol shape, measurement duties, or authority reservations only. Its citation is not a real row, likelihood, participant result, production interoperability event, legal interpretation, cultural ratification, Māori authorization, or independent review. Orin must reverify current or watch-sensitive status where material and preserve stable historical sources without pretending stability is freshness."
        )
    sections.append("## Method Flow inheritance")
    for method in methods:
        sections.append(
            f"### {method['method_id']}: {method['title']}\n\n"
            f"Failure retained: {method['failure_signature']} Preferred bounded recovery: {method['candidate_workaround']} "
            f"Recurrence guard: {method['recurrence_guard']} Rollback: {method['rollback']} "
            f"This method is preferred only for its exact trigger and passing witness. Its failed witness remains retained. {method['scope_boundary']}"
        )
    sections.append(f"""## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Lee-Wick, worldline, GMRES, formal classifiers, and software adapters do not establish a force, physical state, real prediction, likelihood, posterior, parameter constraint, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. The ALMA adapter made zero queries and downloads, restored zero measurement sets, ingested zero real rows, evaluated zero likelihoods, and produced zero posteriors or constraints. It remains `open_gap`.

THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Airport baggage and ground-deicing fixtures establish no operational effectiveness, professional competence, dispatch or airworthiness authority, deployment readiness, AGI, or ASI.

Freed ID remains synthetic and nonproduction. DSSE, CIBA, OpenID4VP/DCQL, and X.509 fixtures used no real private keys, signatures, accounts, tokens, credentials, issuances, presentations, resolutions, status or revocation events, network interoperability, privacy review, independent security review, recovery decision, or trust-governance decision. Production completion requires exact standards-conformant and governance evidence.

CBR airport access, disability, privacy, property, dangerous-goods disclosure, remedy, legal interpretation, cultural legitimacy, data governance, affected-party acceptance, and Māori wording and authority remain exact-gated to competent authorities, affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Repository software cannot confer a remedy, title, right, legitimacy, governance mandate, or public authority.

No empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof or canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, or Stage 20 claim is permitted without exact evidence and authority. The terminal verdict remains `NOT_READY_FOR_STAGE_20` unless the declared external gates genuinely close.

## Terminal route after Orin

Only after Orin's v651-v2 work is clean, pushed, remote-equal, within its commit cap, and exact-final validated may Orin send exactly one sanitized live activation baton to the unique existing `Tamar Vey` task for v651-v3 using the existing-task route only. Do not create or fork a task, do not contact standby siblings, and send no extra confirmation. Preserve the six-seat order Eiren Kestrel to Ilyra Fen to Sable Rook to Orin Thale to Tamar Vey to Sylven Arc and repeat through v660-v8 unless Hamish stops or redirects the route, usage is exhausted, the required exact title is unavailable, or an exact safety or authority gate blocks progress.

This committed file remains `PREPARED_NOT_SENT`. Delivery becomes true only after an acknowledged live tool result. A prepared file, exact title, branch, clean commit, or route plan is not a send acknowledgement.
""")
    text = "\n\n".join(sections)
    count = len(re.findall(r"\b\w+\b", text, flags=re.UNICODE))
    if not 8000 <= count <= 20000:
        raise RuntimeError(f"successor baton word count outside 8000..20000: {count}")
    return text


def build_manifests() -> dict[str, int]:
    owner_exclusions = [
        f"{d.PHASE_ROOT}/validation/final-owner-manifest.json",
        f"{d.PHASE_ROOT}/validation/final-owner-privacy.json",
        f"{d.PHASE_ROOT}/validation/final-delta-manifest.json",
        f"{d.PHASE_ROOT}/validation/final-delta-privacy.json",
        f"{d.PHASE_ROOT}/validation/closeout-staged-review.json",
        f"{d.PHASE_ROOT}/validation/closeout-staged-manifest.json",
        f"{d.PHASE_ROOT}/validation/closeout-staged-privacy.json",
    ]
    definition_paths = {
        "scripts/build_ghc_family_v651_v1_preregistration.py",
        "scripts/build_ghc_family_v651_v1_evidence.py",
        "scripts/build_ghc_family_v651_v1_closeout.py",
        "scripts/validate_ghc_family_v651_v1_final.py",
        f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/evidence-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/final-owner-privacy.json",
        f"{d.PHASE_ROOT}/validation/final-delta-privacy.json",
        f"{d.PHASE_ROOT}/validation/closeout-staged-privacy.json",
    }

    owner_paths = changed_paths(SOURCE)
    owner_entries = [hash_entry(path) for path in owner_paths if path not in owner_exclusions and (REPO / path).is_file()]
    owner_privacy = privacy_scan(owner_paths, definition_paths, "ghc.family.v651-v1.final-owner-privacy.v1")
    write_json("validation/final-owner-privacy.json", owner_privacy)
    write_json("validation/final-owner-manifest.json", {
        "schema": "ghc.family.v651-v1.final-owner-manifest.v1",
        "hash_domain": "git_path_filtered_blob",
        "source_head": SOURCE,
        "entry_count": len(owner_entries),
        "entries": owner_entries,
        "self_exclusions": owner_exclusions,
        "coverage_contract": "source-to-commit-containing-this-record changed paths",
    })

    delta_paths = changed_paths(EVIDENCE)
    delta_entries = [hash_entry(path) for path in delta_paths if path not in owner_exclusions and (REPO / path).is_file()]
    delta_privacy = privacy_scan(delta_paths, definition_paths, "ghc.family.v651-v1.final-delta-privacy.v1")
    write_json("validation/final-delta-privacy.json", delta_privacy)
    write_json("validation/final-delta-manifest.json", {
        "schema": "ghc.family.v651-v1.final-delta-manifest.v1",
        "hash_domain": "git_path_filtered_blob",
        "evidence_head": EVIDENCE,
        "entry_count": len(delta_entries),
        "entries": delta_entries,
        "self_exclusions": owner_exclusions,
        "coverage_contract": "evidence-to-commit-containing-this-record changed paths",
    })

    closeout_paths = status_paths()
    closeout_privacy = privacy_scan(closeout_paths, definition_paths, "ghc.family.v651-v1.closeout-staged-privacy.v1")
    write_json("validation/closeout-staged-privacy.json", closeout_privacy)
    closeout_paths = status_paths()
    staged_manifest_rel = f"{d.PHASE_ROOT}/validation/closeout-staged-manifest.json"
    staged_review_rel = f"{d.PHASE_ROOT}/validation/closeout-staged-review.json"
    staged_privacy_rel = f"{d.PHASE_ROOT}/validation/closeout-staged-privacy.json"
    staged_entries = []
    for relative in closeout_paths:
        if relative in {staged_manifest_rel, staged_review_rel}:
            continue
        raw = prospective_git_blob_bytes(REPO / relative)
        staged_entries.append({"path": relative, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "hash_domain": "prospective_normalized_git_blob_bytes"})
    write_json("validation/closeout-staged-review.json", {
        "schema": "ghc.family.v651-v1.closeout-staged-review.v1",
        "lifecycle": "combined_closeout_and_seal",
        "intended_path_count": len(staged_entries) + 2,
        "content_entry_count_before_review": len(staged_entries),
        "self_exclusions": [staged_manifest_rel],
        "privacy_receipt": staged_privacy_rel,
        "privacy_confirmed_hits": closeout_privacy["confirmed_hit_count"],
        "x1_proposals_immutable": True,
        "evidence_outcomes_immutable": True,
        "diff_hygiene_expected": True,
        "terminal_route": "PREPARED_NOT_SENT",
    })
    review_raw = prospective_git_blob_bytes(ROOT / "validation/closeout-staged-review.json")
    staged_entries.append({"path": staged_review_rel, "sha256": hashlib.sha256(review_raw).hexdigest(), "bytes": len(review_raw), "hash_domain": "prospective_normalized_git_blob_bytes"})
    write_json("validation/closeout-staged-manifest.json", {
        "schema": "ghc.family.v651-v1.closeout-staged-manifest.v1",
        "evidence_head": EVIDENCE,
        "entries": sorted(staged_entries, key=lambda row: row["path"]),
        "entry_count": len(staged_entries),
        "self_exclusions": [staged_manifest_rel],
        "covered_path_count": len(staged_entries) + 1,
    })

    confirmed = owner_privacy["confirmed_hit_count"] + delta_privacy["confirmed_hit_count"] + closeout_privacy["confirmed_hit_count"]
    if confirmed:
        raise RuntimeError(f"final privacy scans found {confirmed} confirmed payload hits")
    return {
        "owner_paths": len(owner_paths),
        "owner_entries": len(owner_entries),
        "delta_paths": len(delta_paths),
        "delta_entries": len(delta_entries),
        "closeout_paths": len(closeout_paths),
        "closeout_entries": len(staged_entries),
    }


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout must begin at the immutable evidence commit")
    outcome_ledger = load("outcomes/outcome-ledger.json")
    expected_counts = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
    if outcome_ledger["outcome_counts"] != expected_counts:
        raise RuntimeError("outcome distribution drift")
    if git("show", f"{X1}:{d.PHASE_ROOT}/preregistration/proposals.json") != (ROOT / "preregistration/proposals.json").read_text(encoding="utf-8").rstrip("\n"):
        raise RuntimeError("frozen x1 proposals changed")
    if git("show", f"{EVIDENCE}:{d.PHASE_ROOT}/outcomes/outcome-ledger.json") != (ROOT / "outcomes/outcome-ledger.json").read_text(encoding="utf-8").rstrip("\n"):
        raise RuntimeError("immutable evidence outcomes changed")

    method_counts = load("method-flow/method-flow-state.json")["counts"]
    if method_counts["methods"] != 16 or method_counts["witness_results"] != {"fail": 20, "pass": 18}:
        raise RuntimeError("Method Flow closeout counts drift")

    write_text("deliverables/final-integrated-overview.md", integrated_overview())
    write_text("deliverables/final-static-report.html", static_report())
    write_text("wellbeing/final-wellbeing-check.md", """# Sable Rook v651-v1 final wellbeing and workload check

Work stayed inside one owner lane, four phase commits, the 15,000-owner-file threshold, and bounded software, symbolic, structural, synthetic, or reservation evidence. Twenty failures remain paired with eighteen bounded passing recoveries; none was erased. No participant recruitment, aviation operation, production identity operation, sibling mutation, elevation, host-security weakening, Sandbox or Hyper-V activation, unrelated installation, desktop update, or reboot occurred. The route remains pausable, corrigible, and held before proof. This is workflow care, not a consciousness, personhood, continuity, employment, qualification, health, or authority claim.
""")
    write_text("threat-model/final-threat-model.md", """# Sable Rook v651-v1 final threat model

Protected assets are x1 immutability, evidence lineage, negative retention, scientific and participant boundaries, aviation and public-safety authority, identity nonproduction, privacy, legal and cultural decision rights, Māori authority, sibling isolation, and terminal-route integrity. Threats include claim inflation, empirical substitution, authority laundering, privacy leakage, manifest drift, checkout-byte ambiguity, stale source status, mutation erasure, validation replay inflation, sibling-lane mutation, task substitution, and premature route send. Controls are typed outcomes, zero-row firewalls, represented and exact-gate reservations, Git-blob manifests, five-class scans, exact staged review, Method Flow witnesses, one canonical final pass with no replay after success, four-way equality, and send-after-proof. Residual risk remains nonzero; this is not exhaustive security, complete privacy, complete accessibility, aviation assurance, legal review, cultural ratification, Māori-authority review, or independent reproduction.
""")

    x1_entries = load("truth/retained-negative-register.json")["entries"]
    closeout_negatives = [
        {
            "negative_id": "V6511-X2-N06",
            "disposition": "retained",
            "failure": "A read-only ripgrep query passed literal Windows wildcard paths and stopped with a path-syntax error.",
            "recovery": "A directory-scoped recursive query returned the exact frozen baton range and ordinary-document cap; the failed probe keeps zero search credit.",
        },
        {
            "negative_id": "V6511-X2-N07",
            "disposition": "retained",
            "failure": "A read-only skill refresh guessed a nonexistent schema filename despite the skill naming its exact required reference.",
            "recovery": "The exact linked references/schema.md file was read completely and the runner was resolved; the guessed-path failure keeps zero schema credit.",
        },
        {
            "negative_id": "V6511-X2-N08",
            "disposition": "retained",
            "failure": "PowerShell terminating error handling converted unittest's normal stderr progress into a NativeCommandError before exit-code adjudication.",
            "recovery": "Non-terminating native-output capture exposed the explicit exit code and totals; the interrupted wrapper keeps zero aggregate credit.",
        },
        {
            "negative_id": "V6511-X2-N09",
            "disposition": "retained",
            "failure": "An overbroad inherited v650-v8 pattern included predecessor closeout self-state assertions and produced a 20-test two-failure aggregate.",
            "recovery": "An exact successor module allowlist passed its bounded evidence selection; the overbroad aggregate keeps zero selection credit.",
        },
        {
            "negative_id": "V6511-X2-N10",
            "disposition": "retained",
            "failure": "A diagnostic repeated the literal Windows wildcard-path mistake before reading inherited test source.",
            "recovery": "A directory-scoped ripgrep query with an exact file-name filter returned the required assertions; the recurrence remains visible.",
        },
        {
            "negative_id": "V6511-X2-N11",
            "disposition": "retained",
            "failure": "The frozen x1 document-cap assertion treated the later terminal baton as an ordinary document and produced a seven-test one-failure run.",
            "recovery": "The exact historical assertion was reserved while a closeout check enforced the 6,000-word ordinary cap and 8,000-to-20,000-word baton range.",
        },
        {
            "negative_id": "V6511-X2-N12",
            "disposition": "retained",
            "failure": "A targeted source-to-final manifest rebuild exceeded a generic 30-second command wrapper and returned no completion receipt.",
            "recovery": "The measured 120-second envelope completed the rebuild in 96.5 seconds and emitted structured counts; the timeout keeps zero manifest credit.",
        },
        {
            "negative_id": "V6511-X2-N13",
            "disposition": "retained",
            "failure": "An intended staged AST audit omitted its interpreter pipeline and printed unparsed source instead of executing it.",
            "recovery": "An explicitly piped minimal probe parsed all three closeout source files and emitted structured success; the unexecuted source keeps zero review credit.",
        },
        {
            "negative_id": "V6511-X2-N14",
            "disposition": "retained",
            "failure": "The committed closeout manifest test used working status as its only evidence domain and would falsely fail after the status became clean.",
            "recovery": "A dual-state assertion preserved staged status precommit and used the exact evidence-to-commit diff postcommit; the status-only assumption keeps zero terminal-test credit.",
        },
        {
            "negative_id": "V6511-X2-N15",
            "disposition": "retained",
            "failure": "The correction precommit selection ran 47 tests and failed one because historical closeout manifest hashes were compared with successor working-tree bytes.",
            "recovery": "The historical manifest test now resolves both coverage and content from the immutable closeout commit; the failed aggregate keeps zero validation credit.",
        },
        {
            "negative_id": "V6511-X2-N16",
            "disposition": "retained",
            "failure": "A precommit wrapper compared raw checkout bytes with prospective normalized Git-blob manifests and falsely reported hash mismatches after all other aggregate checks passed.",
            "recovery": "A bounded witness reproduced the declared CRLF-to-LF prospective hash domain and granted the failed aggregate zero precommit credit.",
        },
        {
            "negative_id": "V6511-X2-N17",
            "disposition": "retained",
            "failure": "A helper inspection appended a literal scripts/*.py path and returned a Windows path-syntax error after partial output.",
            "recovery": "Exact LiteralPath reads exposed the prospective-byte helpers without wildcard expansion; the recurrence keeps zero search credit.",
        },
        {
            "negative_id": "V6511-X2-N18",
            "disposition": "retained",
            "failure": "The Method Flow summary writer reached console output and then raised a CP1252 UnicodeEncodeError on Māori text.",
            "recovery": "The same summary command completed with UTF-8 standard streams pinned; the failed emission keeps zero summary credit.",
        },
        {
            "negative_id": "V6511-X2-N19",
            "disposition": "retained",
            "failure": "A narrow hash-domain recovery probe ran before rebuilding four later-mutated Method Flow files and therefore retained twelve manifest-entry mismatches.",
            "recovery": "The method witness separated 28 domain recoveries from the four known later mutations and reserved aggregate credit until a full rebuild.",
        },
        {
            "negative_id": "V6511-X2-N20",
            "disposition": "retained",
            "failure": "An exact staged stale-label probe used raw digit substrings and falsely flagged 6557 and 6558 inside SHA-256 values after all substantive index checks passed.",
            "recovery": "Field-aware and prose-boundary patterns found zero semantic stale labels while excluding opaque hashes by construction; the failed staged aggregate keeps zero review credit.",
        },
    ]
    write_json("final/phase-truth.json", {
        "schema": "ghc.family.v651-v1.phase-truth.final.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "pronouns": d.PRONOUNS,
        "role": d.ROLE,
        "hope": d.HOPE,
        "identity_boundary": "Relational working language only; not consciousness, personhood, continuity, employment, qualification, or authority evidence.",
        "source_head": SOURCE,
        "x1_head": X1,
        "evidence_head": EVIDENCE,
        "final_head_binding": "commit_containing_this_record",
        "primary_focus": d.PRIMARY_FOCUS,
        "bounded_practice": d.BOUNDED_PRACTICE,
        "frozen_proposals_before": d.PRIOR_FROZEN,
        "frozen_proposals_after": d.PRIOR_FROZEN + len(d.PROPOSALS),
        "outcome_counts": expected_counts,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "negative_breakdown": {"inherited": d.INHERITED_NEGATIVES, "x1_operational": X1_OPERATIONAL, "x2_operational": X2_OPERATIONAL, "executed_rejected_synthetic": SYNTHETIC_NEGATIVES},
        "negative_erasures": 0,
        "effective_open_gaps": OPEN_GAPS,
        "effective_exact_gates": EXACT_GATES,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "terminal_route": "PREPARED_NOT_SENT",
        "same_owner_only": True,
        "full_repository_suite_run": False,
        "post_success_replay_planned": False,
        "independent_reproduction_claimed": False,
        "empirical_gmut_claimed": False,
        "agi_or_asi_claimed": False,
        "consciousness_or_personhood_claimed": False,
        "production_identity_claimed": False,
        "legal_or_cultural_ratification_claimed": False,
    })
    write_json("final/retained-negative-register.json", {
        "schema": "ghc.family.v651-v1.final-retained-negative-register.v1",
        "effective": EFFECTIVE_NEGATIVES,
        "inherited": d.INHERITED_NEGATIVES,
        "x1_operational_count": X1_OPERATIONAL,
        "x2_operational_count": X2_OPERATIONAL,
        "executed_rejected_synthetic": SYNTHETIC_NEGATIVES,
        "owner_operational_entries": x1_entries + closeout_negatives,
        "method_failed_witnesses": 20,
        "method_passing_witnesses": 18,
        "no_failure_erased": True,
    })
    write_json("final/gate-register.json", {
        "schema": "ghc.family.v651-v1.final-gate-register.v1",
        "effective_open_gaps": OPEN_GAPS,
        "effective_exact_gates": EXACT_GATES,
        "new_open_gap": {"proposal_id": "V6511-P05", "state": "open_gap", "reason": "The ALMA adapter made zero queries or downloads, ingested zero real rows, and evaluated zero likelihoods."},
        "new_exact_gate": {"proposal_id": "V6511-P10", "state": "exact_gate", "reason": "Airport access, privacy, remedy, legal, cultural, data-governance, affected-party, and Māori authority cannot be conferred by repository software."},
        "protected_inherited_gates": True,
        "silently_closed": 0,
    })
    source_counts = dict(Counter(row["status"] for row in d.SOURCES))
    write_json("final/source-status-summary.json", {
        "schema": "ghc.family.v651-v1.final-source-status-summary.v1",
        "count": len(d.SOURCES),
        "status_counts": source_counts,
        "allowed_statuses": d.SOURCE_STATUS_CLASSES,
        "citations_are_observations": False,
        "sources": d.SOURCES,
    })
    write_json("final/complete-incomplete-checklist.json", {
        "schema": "ghc.family.v651-v1.complete-incomplete.final.v1",
        "complete": ["exact inherited source verification", "dedicated x1 freeze", "twenty evidence-permitted outcomes", "one hundred rejected mutations", "forty safe-now tasks", "thirty bounded candidates", "twenty phase-local skills", "ten family-compatible runners", "forty additive cleanup tasks", "Method Flow retention", "accessible structural report", "Git-blob manifests", "five-class privacy scan", "combined closeout and seal packet"],
        "incomplete": ["real-data GMUT likelihood", "blind matched-budget THOS real arms", "production Freed ID lifecycle", "airport affected-party and Māori authority", "manual and affected-user accessibility evaluation", "independent-team reproduction", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("final/environment-receipt.json", {
        "schema": "ghc.family.v651-v1.environment.final.v1",
        "checked_at": "2026-07-21",
        "codex_cli": "0.144.5",
        "codex_desktop": "26.715.4045.0",
        "chatgpt_desktop": "1.2026.190.0",
        "python": "3.12.10",
        "git": "2.55.0.windows.2",
        "windows_powershell": "5.1.26100.8894",
        "windows_sandbox_executable_present": False,
        "actions": {"desktop_updated": False, "elevated": False, "host_security_weakened": False, "windows_feature_changed": False, "sandbox_or_hyper_v_activated": False, "unrelated_software_installed": False, "rebooted": False},
        "boundary": "Version and availability observation only; not an update instruction or administrative-capability claim.",
    })
    write_json("final/evidence-receipt.json", {
        "schema": "ghc.family.v651-v1.evidence-receipt.v1",
        "evidence_head": EVIDENCE,
        "scoped_tests": {"passed": 40, "total": 40},
        "detailed_checks": {"passed": 11, "total": 11},
        "minimal_checks": {"passed": 6, "total": 6},
        "json_parses": 210,
        "public_phase_files_scanned": 279,
        "privacy_confirmed_hits": 0,
        "outcomes": expected_counts,
        "mutations_executed_and_rejected": 100,
        "full_repository_suite_run": False,
        "same_owner_only": True,
        "independent_reproduction": False,
    })
    write_json("final/closeout-receipt.json", {
        "schema": "ghc.family.v651-v1.closeout-receipt.v1",
        "source_head": SOURCE,
        "x1_head": X1,
        "evidence_head": EVIDENCE,
        "final_head_binding": "commit_containing_this_record",
        "expected_phase_commits": 3,
        "authorized_commit_ceiling": 4,
        "expected_merges": 0,
        "outcomes": expected_counts,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "open_gaps": OPEN_GAPS,
        "exact_gates": EXACT_GATES,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route": "PREPARED_NOT_SENT",
        "exact_final_validation": "required_after_commit_and_push",
    })
    write_json("final/seal-candidate-receipt.json", {
        "schema": "ghc.family.v651-v1.seal-candidate.v1",
        "sealed_surfaces": ["x1", "evidence", "combined_closeout", "negative_retention", "gates", "method_flow", "owner_manifest", "delta_manifest", "privacy", "terminal_route_hold"],
        "head_binding": "commit_containing_this_record",
        "direct_parent_required": EVIDENCE,
        "source_ancestry_required": SOURCE,
        "x1_ancestry_required": X1,
        "same_owner_only": True,
        "independent_reproduction": False,
        "external_exact_final_validation_required": True,
    })
    write_json("final/final-validation-contract.json", {
        "schema": "ghc.family.v651-v1.final-validation-contract.v1",
        "expected_head": "commit_containing_this_record",
        "expected_parent": EVIDENCE,
        "expected_source": SOURCE,
        "expected_x1": X1,
        "expected_phase_commits": 3,
        "authorized_commit_ceiling": 4,
        "expected_merges": 0,
        "expected_scoped_tests": 47,
        "expected_detailed_checks": 11,
        "expected_minimal_checks": 6,
        "full_suite_allowed": False,
        "canonical_successes_allowed": 1,
        "post_success_replay_allowed": False,
        "remote_equality_required": True,
        "clean_state_required": True,
        "terminal_route_before_success": "PREPARED_NOT_SENT",
    })
    write_json("route/final-phase-state.json", {
        "schema": "ghc.family.v651-v1.final-route-state.v1",
        "target_title": "Orin Thale",
        "target_phase": "v651-v2",
        "terminal_route": "PREPARED_NOT_SENT",
        "send_count": 0,
        "task_created": False,
        "task_forked": False,
        "standby_sibling_messaged": False,
        "send_gate": "exact final clean, pushed, four-way equal, and one canonical validation pass",
    })
    write_json("orchestration/terminal-route-plan.json", {
        "schema": "ghc.family.v651-v1.terminal-route-plan.v1",
        "current_owner": "Sable Rook",
        "next_exact_title": "Orin Thale",
        "next_phase": "v651-v2",
        "state": "PREPARED_NOT_SENT",
        "permitted_action_after_proof": "one_existing_task_message",
        "task_creation_allowed": False,
        "fork_allowed": False,
        "extra_confirmation_allowed": False,
        "standby_contact_allowed": False,
    })
    write_text("handoffs/orin-thale-v651-v2-activation.md", successor_baton())

    run(sys.executable, str(INDEX_RUNNER), "--repo", str(REPO), "--skill-root", str(Path.home() / ".codex" / "skills"), "--out-dir", str(ROOT / "tooling/closeout-index"), "--phase", d.PHASE, "--owner", d.OWNER)
    manifests = build_manifests()
    print(json.dumps({"phase": d.PHASE, "state": "closeout_built_not_committed", "effective_negatives": EFFECTIVE_NEGATIVES, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES, "method_failures": 20, "method_passes": 18, **manifests, "privacy_hits": 0}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    build()
