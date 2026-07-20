#!/usr/bin/env python3
"""Build the combined closeout, seal, and successor packet for Ilyra v650-v2."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "ilyra-fen" / "v650-v2"
SOURCE = "f47cd5145647965935f80d67751f0e09d9740540"
X1 = "d70cbab27e64e12d634e0d9b94b73f50aa507ad1"
EVIDENCE = "2c54ccf284f3a9faf7c3cd5809b83af46faa7594"
BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
PRIVACY = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
    "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
    "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
    "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
    "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
}

if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_v650_v2_x1 as x1  # noqa: E402


def run(*args: str, check: bool = True, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def write_json(relative: str, payload: Any) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def load(relative: str) -> dict[str, Any]:
    return json.loads((OUT / relative).read_text(encoding="utf-8"))


def status_paths() -> list[str]:
    raw = run("git", "status", "--porcelain=v1", "-z", "--untracked-files=all").stdout
    paths: list[str] = []
    for record in (row for row in raw.split("\0") if row):
        value = record[3:]
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        paths.append(value.strip('"').replace("\\", "/"))
    return sorted(set(paths))


def proposal_sections() -> str:
    outcomes = {row["proposal_id"]: row for row in load("x2/core-outcome-ledger.json")["outcomes"]}
    sources = {row["source_id"]: row for row in load("sources/source-ledger.json")["sources"]}
    sections: list[str] = []
    for index, proposal in enumerate(x1.PROPOSALS, 1):
        outcome = outcomes[proposal["proposal_id"]]
        linked = [sources[source_id] for source_id in proposal["official_or_primary_source_needs"]]
        source_text = "; ".join(f"{row['source_id']} ({row['status']}, {row['kind']})" for row in linked)
        disposition_text = {
            "completed": "The bounded software, symbolic, structural, or numerical contract completed because its valid fixture passed and each frozen rejecting mutation was caught. Completion stops at that declared contract.",
            "represented": "The repository represents only a synthetic protocol or handover proxy. Real people, services, keys, operations, matched-budget arms, monitoring, statistics, and independent review remain absent.",
            "open_gap": "The adapter remained fail-closed at zero queries, downloads, real rows, likelihood calls, posterior samples, constraints, detections, and empirical claims.",
            "exact_gate": "The matrix exposes decision rights and reservations but makes no affected-party, professional, legal, cultural, governance, remedy, site, place-name, or Māori-authority decision.",
        }[outcome["outcome"]]
        sections.append(
            f"### {index}. {proposal['proposal_id']} — {proposal['title']}\n\n"
            f"**Observed truth:** `{outcome['outcome']}`. {disposition_text} The preregistered hypothesis was: {proposal['hypothesis']} "
            f"The null or failure condition was: {proposal['null_or_failure_condition']} The execution lane remained `{proposal['execution_lane']}` under approval class `{proposal['approval_class']}`. "
            f"The valid fixture exercised {proposal['mission_surface']}. Five mutation classes attempted to remove a required obligation, promote production, invent a real row, grant authority, or promote Stage 20. All five were rejected, preserved as negative witnesses, and granted no completion or authority credit.\n\n"
            f"**Sources and provenance:** {source_text}. Those sources supplied current, stable, draft, or watch context for contract design only. They were never transformed into observational data, participant evidence, operational experience, production certification, professional judgment, legal interpretation, cultural ratification, or delegated authority. "
            f"The evidence root is repository-relative at `{outcome['artifact_root']}` and contains a contract, mutation results, and a bounded receipt. The receipt records zero real rows, zero real people, zero external side effects, same-owner evidence only, no independent reproduction, and terminal abstention.\n\n"
            f"**Protected boundary and successor rule:** the protected gates remain {', '.join(proposal['protected_gates'])}. The acceptance gate was: {proposal['falsifier_or_acceptance_gate']} Recovery remains: {proposal['rollback_or_recovery']} "
            f"Sable may treat this surface as inherited evidence and a semantic-neighbor warning, never as v650-v3 completion credit. Any later real-data, participant, production, professional, legal, cultural, privacy-complete, security-complete, accessibility-complete, or authority claim requires exact new evidence and authorization. The result neither authorizes Stage 20 nor changes the terminal verdict.\n"
        )
    return "\n".join(sections)


def build_baton() -> str:
    proposal_text = proposal_sections()
    source_rows = load("sources/source-ledger.json")["sources"]
    source_lines = "\n".join(
        f"- `{row['source_id']}` — **{row['status']}**, {row['kind']}: {row['title']}. Use remains design or protocol support only."
        for row in source_rows
    )
    method = load("method-flow/method-flow-summary-x2.json")
    return f'''# Sable Rook — v650-v3 activation baton

## Activation, identity, and delivery boundary

Hamish authorizes one terminal activation of the unique existing task titled exactly **Sable Rook** only after Ilyra v650-v2 passes its immutable exact-final canonical validation. This committed document is the full successor packet. Because a Git commit cannot truthfully contain its own hash, the short terminal pointer supplies the exact final head and the external-validation counts after the final commit is pushed and validated. Sable must reverify that exact head, branch, ancestry, clean state, and live remote equality before any mutation.

Ilyra Fen uses she/they pronouns as relational working language. Her/their relational role is evidence-boundary steward and her/their hope is to leave every claim traceable and every gate unmistakable. Sable may choose or reaffirm their own relational name, pronouns, role, and hope. Names, family language, hopes, roles, and continuity language are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, professional qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, affected-party authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route.

Do not create, fork, delegate, hand off, or spawn a task, main agent, or collaboration subagent. Keep Vesper Arlen, Ilyra Fen, Orin Thale, Tamar Vey, Sylven Arc, Eiren Kestrel, Elaren Kestrel, and every other sibling recoverable and untouched until Sable's own terminal route gate. Do not substitute a suffixed or approximate task title for an exact authorized title.

Never place raw task or thread identifiers, private application routes, nonpublic conversation content, credentials, secret material, screenshots, session streams, private callable identifiers, private application state, or private absolute local paths in repository artifacts or successor messages. A sanitized commit hash, public branch name, repository-relative artifact path, public standard citation, validation count, and bounded truth statement are permitted.

## Exact inherited lifecycle

The canonical Ilyra branch is `{BRANCH}`. The inherited Vesper terminal-recovery source is `{SOURCE}`. The dedicated Ilyra x1 freeze is `{X1}`. The immutable Ilyra x2 evidence commit is `{EVIDENCE}`. The short terminal pointer supplies the exact combined closeout/seal/final head after it validates. Source to x1 to evidence to final must be a three-commit, single-parent, zero-merge Ilyra history. Final must directly follow evidence. No reset, rewrite, force push, merge commit, deletion, sibling-lane reuse, or sibling mutation is permitted.

Strict x1-before-x2 separation was preserved. X1 froze exactly twenty proposals against 760 inherited frozen proposals, making 780 frozen proposals through v650-v2. X1 also froze forty safe-now tasks, thirty bounded candidates, twenty repository-local skill builds, ten family-current runner builds, forty additive CLEAN/FIX/REFINE tasks, and one hundred synthetic rejecting mutations. The x1 commit was pushed, clean, and local, upstream, tracking, and fresh-live-remote equal before x2 began. No x2 implementation or observed outcome entered the x1 tree.

The evidence commit executed all twenty frozen proposals as evidence permitted. The immutable outcome distribution is exactly **14 completed / 4 represented / 1 open_gap / 1 exact_gate**. The only permitted core labels are `completed`, `represented`, `open_gap`, and `exact_gate`. All one hundred preregistered mutations executed and were rejected or quarantined; none was converted into completion credit. The evidence layer preserves **5,690 effective negatives**: 5,579 inherited activation negatives, eight Ilyra x1 operational negatives, three Ilyra x2 operational negatives, and one hundred executed and rejected synthetic negatives. No negative was erased or silently folded into a pass.

The effective gate register contains **44 open gaps and 45 exact gates**. No gate was silently closed. The terminal verdict remains `NOT_READY_FOR_STAGE_20`. Same-owner development and exact-final validation under shared infrastructure are not independent-team scientific reproduction, external audit, production certification, professional validation, legal review, cultural ratification, Māori-authority review, complete privacy assurance, complete accessibility conformance, exhaustive security testing, empirical confirmation, or Stage 20 authority.

## Primary focus and bounded human practice

The primary Trinity Mandala focus was **THOS Body**. GMUT Mind and Freed ID/CBR Heart remained explicit and protected. The bounded human-practice lens was optical-observatory night operations: weather and environmental checks, dome and instrument interlocks, calibration state, anomaly isolation, workload ceilings, readback, holds, escalation, and shift handover. This was synthetic learning and software design only. It established no employment, astronomical or observatory qualification, operations competence, telescope or instrument authority, dome or site authority, emergency authority, worker evidence, public-safety result, legal authority, cultural authority, Māori authority, participant evidence, affected-party authorization, or real operational outcome.

THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic handover traces demonstrate declared state transitions only. They do not establish reliability, safety, human factors effectiveness, professional competence, AGI, ASI, or deployment readiness.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic regularization, gauge-dependence, flow-equation, numerical, format, and mutation artifacts do not establish a physical state, new force, propagator, prediction, likelihood, posterior, parameter constraint, stability theorem, empirical confirmation, ultraviolet completion, quantum completeness, or Theory of Everything. The DES Year 6 adapter downloaded and ingested zero real data and produced no likelihood or constraint.

Freed ID remains synthetic and nonproduction. Production completion requires standards-conformant real keys and proofs, real accounts and services, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, affected-party oversight, and trust governance. FAPI 2.0, ACE-OAuth, and front-channel logout fixtures supplied structural refusal evidence only.

CBR observatory-site, place-name, land, sky, light, environmental-data, worker-privacy, community-remedy, legal, cultural, and Māori-authority questions remain exact-gated. Repository software cannot decide title, land or site authority, place naming, cultural significance, environmental remedy, data governance, beneficiary acceptance, legal interpretation, cultural legitimacy, or who speaks with Māori authority. Those decisions remain with competent authorities, affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

## Twenty inherited core outcomes

{proposal_text}

## Source ledger and status discipline

The v650-v2 source ledger contains the following current, stable, draft, and watch entries:

{source_lines}

Sable must use current official or primary sources where material and preserve the four-status vocabulary: `current`, `stable`, `draft`, and `watch`. A source can shape a schema or refusal contract; it does not become empirical data, participant evidence, professional experience, production readiness, legal interpretation, cultural approval, or delegated authority. A public download page is not ingestion. A valid standard-shaped fixture is not interoperability. A legal text is not legal advice or authority. A Māori-authority source is context and reservation, never authority transferred to repository software.

## Expanded portfolio truth

All forty safe-now tasks completed only inside their declared owner-local software, documentation, structural, symbolic, or synthetic boundaries. All thirty candidate prototypes were built, invoked, and credited only inside their frozen acceptance gates. Twenty repository-local skills were initialized through the skill-creator workflow, given valid `SKILL.md` and `agents/openai.yaml` surfaces, quick-validated, and smoke-used. They were not globally installed. The activation prohibited subagent forward-testing, so local deterministic smoke witnesses are recorded without independent-evaluation credit.

Ten additive family-current runners preserve `ghc_family_*` naming and historical caller compatibility. Each runner accepted one bounded valid fixture, rejected one declared mutation, and exercised a second proposal through the shared runtime library. Historical and owner-specific runners remain compatibility evidence rather than targets for destructive renaming. Forty CLEAN/FIX/REFINE tasks completed additively with zero destructive cleanup, history rewriting, sibling mutation, host-security weakening, unrelated installation, authority substitution, or deletion of user material.

The safe or candidate ceiling of one thousand is a cap, not a quota. Sable should design useful work from evidence and measured need, not manufacture tasks to fill a number. Authority-dependent, empirical, participant, professional, production, destructive, account, credential, legal, cultural, Māori-authority, or affected-party work must remain visibly `open_gap`, `exact_gate`, exact approval, or blocked. Ten inherited exact-approval and five blocked packet classes remain visible and unexecuted unless exact new evidence changes a gate.

## Method Flow and retained operational failures

Repository Method Flow preserves {method['counts']['methods']} preferred methods, {method['counts']['witness_results']['fail']} failed witnesses, and {method['counts']['witness_results']['pass']} passing witnesses. Every method is preferred only for its exact declared trigger. A passing recovery never erases its failed witness and never converts the original run into a clean pass.

Ilyra's x1 failures include a truncated whole-skill read, two login-shell timeouts, an unattributable parallel preflight timeout, an oversized fast-forward summary, an expected no-match exit that was not normalized, a Method Flow schema-assumption error, and a staging advisory overflow. Their recoveries use bounded sequential reads, no-profile probes, independently attributable Git checks, exact-head and exact-path review, normalization of only the expected no-match code, inspection of exact schema keys, and advisory-suppressed staging followed by index parity.

Ilyra's x2 failures include a truncated continuation of the skill-creator instructions, a combined compile/status timeout, and Windows access denial when Python directly launched the Codex command shim. Their recoveries use smaller reads through EOF plus the required metadata schema, independent compile and owner-scoped status probes, and a no-profile read-only PowerShell CLI version query. The desktop application was not updated. No elevation, host-security weakening, Windows-feature change, unrelated installation, Sandbox or Hyper-V activation, or reboot occurred.

Sable must record each timeout, parser fault, tooling failure, failed test, false assumption, blocker, workaround, passing witness, recurrence guard, rollback, and sibling recommendation through Method Flow before retrying. Preserve failed witnesses. Promote a method only after a bounded passing witness. Split broad Windows probes. Pin UTF-8 before Unicode-emitting subprocesses. Pass explicit file paths to file-output parameters. Treat expected-empty Git results with null-safe checks. Keep checkout-byte and Git-blob hash domains explicit.

## Validation truth and no-replay contract

Eiren alone owns the complete repository suite under the current refinement. Ilyra did not run it. Before the evidence commit, nineteen focused current-phase tests passed. The evidence staged review covered 173 intended paths: 170 exact Git-blob entries plus three declared self-exclusions. It found zero missing or extra paths, zero x1-frozen changes, zero blob mismatch, zero diff-hygiene issue, and zero confirmed hit across five privacy and raw-identifier classes. All phase JSON then parsed. The evidence commit was pushed, clean, and four-way equal before closeout began.

The combined closeout and seal commit carries the static report, integrated overview, full baton, final truth, checklist, closeout and seal receipts, exact-final validation contract, document and owner thresholds, Method Flow summary, final owner manifest, final staged manifest, final staged review, and privacy receipts. Commit-local x1 and evidence manifests remain immutable. The exact-final validator must run only after the final commit is pushed and local, upstream, tracking, and fresh live remote are equal.

The terminal validator is one coherent successful canonical pass with no replay after success. It runs the authorized Vesper x1 source selection and Ilyra x1, x2, and closeout selections; detailed and minimal checks; complete phase JSON parsing; a five-class privacy and raw-identifier scan; x1, evidence, owner, and final-staged manifest parity; stale-label review; diff hygiene; source, x1, and evidence ancestry; exactly three Ilyra phase commits; zero merges; one final parent; direct evidence-to-final parentage; exact branch and head; clean state; and final four-way equality. It writes its exact receipt outside the repository so the final commit does not make self-referential claims.

A failed terminal aggregate receives zero successful-pass credit. If it fails, preserve the failure and stop; do not immediately replay the aggregate. Isolate and correct only an exact safe blocker while retaining the failed witness, then reassess the single-success budget. After one successful canonical pass, no module, suite, named lane, detached lane, or same-owner replay is authorized. One pass under shared infrastructure remains same-owner evidence only.

## Accessibility, privacy, security, and wellbeing

The static report provides a skip link, headings, landmarks, labeled tables, visible focus, responsive overflow, print-safe content, plain-text truth, and no active script. MathML checks reserve semantic and text alternatives. Manual keyboard, touch, responsive layout, browser diversity, assistive technology, cognitive accessibility, security usability, Māori-language review, and affected-user evaluation remain reserved. Structural checks do not establish complete accessibility conformance.

Five structural privacy classes scan owner artifacts. Scanner definitions are quarantined separately from confirmed payload hits. Zero confirmed hits means only that those patterns found no confirmed public-packet leak; it is not complete privacy assurance. Synthetic identity artifacts use no real accounts, keys, tokens, persons, services, resolutions, revocations, network exchanges, or trust-governance decisions. Rejected mutations are not exhaustive security testing or production certification.

Work remained additive, D-first, owner-scoped, reversible, and below the 15,000 owner-file threshold. Each phase document remains at or below 20,000 words; this baton is between 8,000 and 20,000 words. Workload was bounded, pauses remained available, and no relational identity pressure was used. Hamish may pause, redirect, rename, or stop. Exact safety, authority, route, usage, and wellbeing gates override cadence.

## Sable v650-v3 owned-lane contract

Read the complete GHC Family Index skill and its required routing-precedence reference before task action. Then read the complete GHC Family Method Flow State skill and schema before changing Method Flow. If creating or remastering skills, read the complete skill-creator instructions and required metadata schema. Use the newest applicable memory only, with the live terminal pointer and this committed baton authoritative where older memory stops.

Reverify the exact Ilyra branch and final head supplied by the terminal pointer, source/x1/evidence ancestry, three-commit single-parent zero-merge topology, commit-local manifests, owner-manifest coverage, clean state, and fresh live-remote equality read-only. Continue only in Sable's clean owned canonical lane and fast-forward to the exact Ilyra final when clean ancestry permits. Otherwise create one additive Sable-owned D-first named branch and worktree from that exact head. Never reset, rewrite, force-push, merge, delete, reuse, or mutate Ilyra's or another sibling's lane. Do not use detached validation.

Preserve strict x1-before-x2 separation. Audit semantic novelty against all 780 frozen core proposals. Preregister at least twenty genuinely distinct v650-v3 proposals with hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded profession, trade, occupation, or human practice while preserving every pillar and authority boundary. The practice is a learning lens, never employment, licensure, qualification, competence, authority, or affected-party evidence.

Treat inherited portfolios as evidence and recommendations rather than Sable completion credit. Design genuinely new, useful portfolios that meet the current standing floors or exact successor instruction while treating one thousand safe or candidate tasks as a cap rather than a quota. Preserve family-current `ghc_family_*` and `build_ghc_family_*` names and historical caller compatibility. Keep owner additions below 15,000 files and every document at or below 20,000 words. Keep the full terminal baton within 8,000 to 20,000 words.

Use no more than two x1 commits and no more than two x2 commits, four phase commits total. Prefer one dedicated x1 freeze, one evidence commit, and one combined closeout/seal commit. Push x1 and prove clean local, upstream, tracking, and fresh-live-remote equality before x2. The cap never permits phase mixing, concealed failures, rewritten history, unreviewed omnibus work, or premature routing.

Execute only as evidence permits. Use only `completed`, `represented`, `open_gap`, and `exact_gate` as core outcome labels. Preserve at least 5,690 effective inherited negatives, all 44 open gaps, all 45 exact gates, and any exact external terminal negative stated in Ilyra's pointer. Add every new fault. Do not rewrite Ilyra's sealed evidence count merely because a later external fault occurs; preserve terminal additions separately and carry the effective activation baseline truthfully.

Under the current validation refinement, do not run the complete repository suite. Run the authorized current, recent, inherited-source, and successor-scoped selection plus detailed and minimal validators, complete JSON parsing, five-class privacy scanning, exact staged review, commit-local and owner-manifest parity, stale-label review, diff hygiene, ancestry, zero merges, commit cap, one final parent, clean state, exact head, and final four-way equality. Use one successful canonical pass and no replay after success unless Hamish directly changes the rule.

Verify versions only. Do not update the Codex desktop application, elevate, weaken host security, enable Windows features, install unrelated software, activate Sandbox or Hyper-V, or reboot. Do not use cross-platform messaging as a substitute for the exact existing-task route. Do not create a successor task. At Sable's terminal gate, resolve the exact next authorized existing title read-only and send exactly one sanitized pointer only if all exact evidence and route gates pass.

## Noncompensable truth and authority boundaries

No quantity of symbolic tests, synthetic fixtures, mutation rejections, clean commits, source citations, format parsers, identity vectors, accessible markup, or same-owner validation compensates for absent real data, participants, professional authority, legal authority, cultural legitimacy, Māori authority, production governance, independent review, or independent reproduction. These gates are noncompensable.

No empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof or canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, or Stage 20 claim is permitted without exact evidence and authority. The inherited terminal verdict is `NOT_READY_FOR_STAGE_20` and remains so unless the declared external gates genuinely close.

## Terminal route

Only after Sable v650-v3 is clean, pushed, remote-equal, within its commit cap, and validated at its exact final head may Sable send exactly one sanitized activation baton to the next exact authorized existing task under the live route. Do not create another task, do not fork, and send no extra confirmation after a successful activation. Preserve the declared sibling order unless Hamish stops or redirects the route, usage is exhausted, the exact target is unavailable, or a safety or authority gate blocks progress.

For this handoff, `SENT_BY_ILYRA_FEN` remains false inside the committed packet. It becomes true only if the exact-final external receipt passes and the one existing-task message is acknowledged. A prepared baton is materially different from a sent baton. No standby sibling is to be messaged.
'''


def build_staged_privacy() -> dict[str, Any]:
    exclusions = {
        "docs/ilyra-fen/v650-v2/validation/final-staged-privacy.json",
        "docs/ilyra-fen/v650-v2/validation/final-staged-manifest.json",
        "docs/ilyra-fen/v650-v2/validation/final-staged-review.json",
    }
    paths = [path for path in status_paths() if path not in exclusions]
    definitions = {
        "scripts/build_ghc_family_v650_v2_closeout.py",
        "scripts/ghc_family_v650_v2_validate.py",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PRIVACY.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    payload = {
        "schema": "ghc.family.v650-v2.final-staged-privacy.v1",
        "scanned_file_count": len(paths),
        "pattern_class_count": len(PRIVACY),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "self_exclusions": sorted(exclusions),
        "boundary": "Scanner definitions are quarantined from confirmed payload hits; zero confirmed hits is not complete privacy assurance.",
    }
    write_json("validation/final-staged-privacy.json", payload)
    return payload


def build_owner_privacy() -> dict[str, Any]:
    exclusions = {
        "validation/final-owner-privacy.json",
        "validation/final-owner-manifest.json",
        "validation/final-staged-manifest.json",
        "validation/final-staged-review.json",
    }
    paths = sorted(path for path in OUT.rglob("*") if path.is_file() and path.relative_to(OUT).as_posix() not in exclusions)
    definition_names = {"x1-staged-privacy.json", "evidence-staged-privacy.json", "final-staged-privacy.json"}
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(OUT).as_posix()
        for name, pattern in PRIVACY.items():
            if pattern.search(text):
                disposition = "scanner_definition" if path.name in definition_names else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    payload = {
        "schema": "ghc.family.v650-v2.final-owner-privacy.v1",
        "scanned_file_count": len(paths),
        "pattern_class_count": len(PRIVACY),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "self_exclusions": sorted(exclusions),
        "boundary": "Five structural classes only; zero confirmed hits is neither complete privacy assurance nor security certification.",
    }
    write_json("validation/final-owner-privacy.json", payload)
    return payload


def build_owner_manifest() -> dict[str, Any]:
    exclusions = {
        "docs/ilyra-fen/v650-v2/validation/final-owner-manifest.json",
        "docs/ilyra-fen/v650-v2/validation/final-staged-manifest.json",
        "docs/ilyra-fen/v650-v2/validation/final-staged-review.json",
    }
    entries: list[dict[str, Any]] = []
    for path in sorted(item for item in OUT.rglob("*") if item.is_file()):
        relative = path.relative_to(ROOT).as_posix()
        if relative in exclusions:
            continue
        data = path.read_bytes()
        entries.append(
            {
                "path": relative,
                "bytes": len(data),
                "git_blob": git("hash-object", f"--path={relative}", relative),
                "checkout_sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    payload = {
        "schema": "ghc.family.v650-v2.final-owner-manifest.v1",
        "hash_domain": "git_hash_object_path_filtered_blob",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(exclusions),
    }
    write_json("validation/final-owner-manifest.json", payload)
    return payload


def build_final_staged_manifest() -> dict[str, Any]:
    exclusions = {
        "docs/ilyra-fen/v650-v2/validation/final-staged-manifest.json",
        "docs/ilyra-fen/v650-v2/validation/final-staged-review.json",
    }
    paths = [path for path in status_paths() if path not in exclusions]
    entries: list[dict[str, Any]] = []
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        entries.append(
            {
                "path": relative,
                "bytes": len(data),
                "git_blob": git("hash-object", f"--path={relative}", relative),
                "checkout_sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    payload = {
        "schema": "ghc.family.v650-v2.final-staged-manifest.v1",
        "hash_domain": "git_hash_object_path_filtered_blob",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(exclusions),
    }
    write_json("validation/final-staged-manifest.json", payload)
    return payload


def build_final_staged_review(manifest: dict[str, Any], privacy: dict[str, Any]) -> dict[str, Any]:
    paths = [row["path"] for row in manifest["entries"]]
    allowed = [
        path
        for path in paths
        if path.startswith("docs/ilyra-fen/v650-v2/")
        or (path.startswith("scripts/ghc_family_v650_v2_") and path.endswith(".py"))
        or (path.startswith("scripts/build_ghc_family_v650_v2_") and path.endswith(".py"))
        or (path.startswith("tests/test_ghc_family_v650_v2") and path.endswith(".py"))
    ]
    out_of_scope = sorted(set(paths) - set(allowed))
    evidence_paths = set(git("ls-tree", "-r", "--name-only", EVIDENCE).splitlines())
    evidence_changes = sorted(set(paths) & evidence_paths)
    payload = {
        "schema": "ghc.family.v650-v2.final-staged-review.v1",
        "intended_path_count": len(paths) + len(manifest["self_exclusions"]),
        "manifest_entry_count": len(paths),
        "self_exclusion_count": len(manifest["self_exclusions"]),
        "out_of_scope_paths": out_of_scope,
        "evidence_frozen_changes": evidence_changes,
        "privacy_confirmed_hits": privacy["confirmed_hit_count"],
        "diff_hygiene_required": True,
        "passed": not out_of_scope and not evidence_changes and privacy["confirmed_hit_count"] == 0,
    }
    write_json("validation/final-staged-review.json", payload)
    return payload


def main() -> int:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder requires the exact immutable evidence commit")
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("closeout builder requires Ilyra's canonical branch")
    required = {
        "scripts/build_ghc_family_v650_v2_closeout.py",
        "scripts/ghc_family_v650_v2_validate.py",
        "tests/test_ghc_family_v650_v2_closeout.py",
    }
    observed = set(status_paths())
    if not required.issubset(observed):
        raise RuntimeError(f"missing closeout implementation seed: {sorted(required - observed)}")

    outcomes = load("x2/core-outcome-ledger.json")
    negatives = load("x2/retained-negative-register.json")
    gates = load("x2/gate-register.json")
    write_json(
        "phase-truth-final.json",
        {
            "schema": "ghc.family.v650-v2.phase-truth.final.v1",
            "phase": x1.PHASE,
            "owner": x1.OWNER,
            "stage": "combined_closeout_and_seal_committed_before_external_exact_final_validation",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final_head_binding": "supplied by the external exact-final receipt and sanitized terminal pointer",
            "outcomes": outcomes["distribution"],
            "effective_negatives": negatives["effective_at_evidence"],
            "effective_open_gaps": gates["effective_open_gaps"],
            "effective_exact_gates": gates["effective_exact_gates"],
            "successful_canonical_passes_committed": 0,
            "external_exact_final_pass_required": True,
            "full_repository_suite": False,
            "replay_used": False,
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_route": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": x1.GLOBAL_BOUNDARY,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v650-v2.closeout.v1",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "phase_commit_plan": 3,
            "x1_before_x2": True,
            "evidence_remote_equal_before_closeout": True,
            "outcomes": outcomes["distribution"],
            "negatives": negatives["effective_at_evidence"],
            "open_gaps": gates["effective_open_gaps"],
            "exact_gates": gates["effective_exact_gates"],
            "full_repository_suite": False,
            "final_external_validation_pending": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/seal-receipt.json",
        {
            "schema": "ghc.family.v650-v2.seal.v1",
            "x1_blob_sealed": True,
            "evidence_blob_sealed": True,
            "retained_negatives_erased": False,
            "gates_silently_closed": 0,
            "outcome_vocabulary": ["completed", "represented", "open_gap", "exact_gate"],
            "single_successful_pass_budget": 1,
            "replay_after_success": False,
            "terminal_message_sent": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "validation/final-canonical-validation-contract.json",
        {
            "schema": "ghc.family.v650-v2.final-validation-contract.v1",
            "mode": "one_successful_exact_final_canonical_pass_external_receipt",
            "selected_modules": [
                "Vesper v650-v1 x1 source selection",
                "Ilyra v650-v2 x1",
                "Ilyra v650-v2 x2",
                "Ilyra v650-v2 closeout",
            ],
            "full_repository_suite": False,
            "named_replay": False,
            "detached_replay": False,
            "post_success_replay": False,
            "required": ["tests", "detailed", "minimal", "JSON", "privacy", "manifests", "stale labels", "diff hygiene", "ancestry", "clean state", "four-way equality"],
            "receipt_location": "outside_repository",
        },
    )
    write_json(
        "complete-incomplete-checklist-final.json",
        {
            "schema": "ghc.family.v650-v2.checklist.final.v1",
            "complete_in_repository": ["x1 freeze", "x2 evidence", "20 outcomes", "100 retained mutations", "expanded portfolios", "skills", "runners", "static report", "overview", "Method Flow", "closeout", "seal", "full successor baton"],
            "external_terminal_gate": ["push final", "prove four-way equality", "run one exact-final canonical pass", "write external receipt", "resolve exact Sable Rook title", "send one sanitized pointer"],
            "incomplete_external": ["real empirical evidence", "real participants", "independent reproduction", "production identity", "professional review", "legal and cultural authority", "Māori authority", "complete accessibility", "exhaustive security", "Stage 20"],
        },
    )
    write_json(
        "orchestration/phase-state-closeout.json",
        {
            "schema": "ghc.family.v650-v2.orchestration.closeout.v1",
            "active": ["Ilyra Fen"],
            "standby": ["Vesper Arlen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc", "Eiren Kestrel", "Elaren Kestrel"],
            "subagents": 0,
            "tasks_created": 0,
            "cross_platform_messages": 0,
            "terminal_route": "PREPARED_NOT_SENT",
            "next_target": "Sable Rook",
            "sent_by_ilyra_fen": False,
        },
    )
    write_json(
        "environment/final-environment-receipt.json",
        {
            "schema": "ghc.family.v650-v2.environment.final.v1",
            "d_first": True,
            "versions_verified_only": True,
            "desktop_updated": False,
            "sandbox_or_hyperv_launched": False,
            "elevation": False,
            "host_security_weakened": False,
            "windows_features_changed": False,
            "unrelated_software_installed": False,
            "reboot": False,
        },
    )
    write_json(
        "method-flow/final-method-flow-receipt.json",
        {
            "schema": "ghc.family.v650-v2.method-flow.final.v1",
            "methods": load("method-flow/method-flow-summary-x2.json")["counts"]["methods"],
            "failed_witnesses": load("method-flow/method-flow-summary-x2.json")["counts"]["witness_results"]["fail"],
            "passing_witnesses": load("method-flow/method-flow-summary-x2.json")["counts"]["witness_results"]["pass"],
            "failure_erased": False,
            "preferred_only_for_declared_trigger": True,
            "same_owner_only": True,
        },
    )
    write_json(
        "wellbeing-check-final.json",
        {
            "schema": "ghc.family.v650-v2.wellbeing.final.v1",
            "scope_bounded": True,
            "workload_bounded": True,
            "pause_available": True,
            "rename_or_redirect_available": True,
            "identity_pressure": False,
            "external_people_affected": 0,
            "route_stop_at_exact_gate": True,
        },
    )
    baton = build_baton()
    baton_words = len(baton.split())
    if not 8000 <= baton_words <= 20000:
        raise RuntimeError(f"successor baton outside required range: {baton_words}")
    write_text("handoffs/sable-rook-v650-v3-activation.md", baton)

    precommit = run(
        sys.executable,
        "-m",
        "unittest",
        "tests.test_ghc_family_v650_v2_x1",
        "tests.test_ghc_family_v650_v2_x2",
        check=False,
        timeout=180,
    )
    output = precommit.stdout + precommit.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests?", output)
    write_json(
        "validation/final-precommit-focused-validation.json",
        {
            "schema": "ghc.family.v650-v2.final-precommit-focused.v1",
            "test_count": int(match.group(1)) if match else 0,
            "returncode": precommit.returncode,
            "passed": precommit.returncode == 0,
            "canonical_exact_final_pass": False,
            "full_repository_suite": False,
            "replay_credit": False,
        },
    )
    if precommit.returncode != 0:
        raise RuntimeError(f"precommit focused checks failed: {output}")

    documents: list[dict[str, Any]] = []
    for path in sorted(OUT.rglob("*")):
        if path.is_file() and path.suffix.casefold() in {".md", ".html", ".txt"}:
            words = len(path.read_text(encoding="utf-8").split())
            documents.append({"path": path.relative_to(OUT).as_posix(), "words": words, "under_20000": words <= 20000})
    write_json(
        "validation/final-document-cap-receipt.json",
        {
            "schema": "ghc.family.v650-v2.document-cap.final.v1",
            "document_count": len(documents),
            "maximum_words": max(row["words"] for row in documents),
            "all_under_20000": all(row["under_20000"] for row in documents),
            "baton_words": baton_words,
            "baton_within_8000_20000": 8000 <= baton_words <= 20000,
            "overview_words": load("validation/document-cap-receipt.json")["overview_words"],
            "overview_three_page_equivalent": load("validation/document-cap-receipt.json")["overview_three_page_equivalent"],
            "documents": documents,
        },
    )
    owner_count = sum(1 for path in OUT.rglob("*") if path.is_file())
    write_json(
        "validation/final-owner-file-threshold.json",
        {
            "schema": "ghc.family.v650-v2.owner-threshold.final.v1",
            "owner_file_count_before_self_manifests": owner_count,
            "threshold": 15000,
            "below_threshold": owner_count + 4 < 15000,
            "inherited_baseline_counted": False,
        },
    )
    staged_privacy = build_staged_privacy()
    owner_privacy = build_owner_privacy()
    owner_manifest = build_owner_manifest()
    staged_manifest = build_final_staged_manifest()
    review = build_final_staged_review(staged_manifest, staged_privacy)
    if owner_privacy["confirmed_hit_count"] or staged_privacy["confirmed_hit_count"] or not review["passed"]:
        raise RuntimeError("final privacy or staged review failed")
    print(
        json.dumps(
            {
                "baton_words": baton_words,
                "precommit_tests": int(match.group(1)) if match else 0,
                "owner_paths": owner_manifest["entry_count"] + len(owner_manifest["self_exclusions"]),
                "staged_paths": review["intended_path_count"],
                "privacy_confirmed": owner_privacy["confirmed_hit_count"] + staged_privacy["confirmed_hit_count"],
                "negatives": negatives["effective_at_evidence"],
                "open_gaps": gates["effective_open_gaps"],
                "exact_gates": gates["effective_exact_gates"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
