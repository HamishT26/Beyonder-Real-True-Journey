"""Build Caelen Morrow v671-v3 combined closeout and content-seal candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Caelen Morrow"
PHASE = "v671-v3"
BRANCH = "codex/GHC-Family/caelen-morrow-v671-v3-full-tools"
SOURCE = "33b7c2d6b9f79f931ff98c478f136dab823c4d69"
X1_COMMIT = "2551c126776ea0538354a32b90414f31f5cec4b3"
EVIDENCE_COMMIT = "46c41e84871edd72544ddad16f038902ec2386f5"
OWNER_ROOT = Path("docs/caelen-morrow/v671-v3")
BOUNDARY = (
    "Same-owner software, symbolic, synthetic, structural, citation, inherited, "
    "or composite evidence is not empirical confirmation, participant evidence, "
    "professional or scientific authority, production readiness, legal or "
    "cultural ratification, Maori authority, affected-party approval, complete "
    "privacy or accessibility assurance, exhaustive security, independent "
    "reproduction, AGI or ASI evidence, consciousness or personhood evidence, "
    "Theory-of-Everything proof, proof or canon, or Stage 20 authority."
)
MAIN_SKILLS = [
    "ghc-freed-id-flashcards",
    "ghc-family-index",
    "ghc-family-reflection-remaster",
    "ghc-family-method-flow-state",
    "ghc-family-meta-tool-box",
    "ghc-family-auth-permission-state",
    "ghc-family-roster-check",
    "ghc-family-workflow-plan-refinement",
    "ghc-main-orchestration-memory",
    "ghc-main-startup-builder",
    "ghc-main-compact-restart-builder",
    "ghc-main-closeout-builder",
    "ghc-main-retry",
    "ghc-open-gate-rail",
    "ghc-timestamp-flow",
    "ghc-full-tools-skill-bank",
    "ghc-family-truth-bridge",
    "ghc-worktree-branch-rotation",
    "ghc-web-reflection-ledger",
    "ghc-watcher-notifier-cadence",
    "ghc-drive-bank-guardian",
    "ghc-approval-packet-splitter",
    "skill-creator",
]
PACKAGE_BANK = [
    "tzdata",
    "pytest",
    "Hypothesis",
    "pytest-cov",
    "Ruff",
    "mypy",
    "pip-audit",
    "OpenAI Python SDK",
    "TypeScript",
    "ESLint",
    "Prettier",
    "Vitest",
    "Typer",
    "Bandit",
    "pre-commit",
    "pip-tools",
    "build",
    "pipdeptree",
    "tsx",
    "c8",
    "markdownlint-cli2",
    "npm-check-updates",
    "Pyright",
    "Knip",
    "Madge",
]
CLOSEOUT_FAILURES = [
    {
        "signature": "first-closeout-staged-diff-check-found-three-terminal-blank-lines",
        "observation": "The first exact closeout staged diff check found one terminal blank line in each of the new builder, validator, and final-test files and withheld closeout credit.",
        "recovery": "Remove only those three terminal blank lines, regenerate the uncommitted closeout packet, and repeat the exact staged review.",
        "completion_credit": 0,
        "retained": True,
    },
    {
        "signature": "closeout-regeneration-guard-rejected-its-own-generated-candidate-paths",
        "observation": "The first regeneration after the blank-line repair stopped because the pre-closeout guard allowed only the three source files and rejected the fifteen already-generated candidate artifacts.",
        "recovery": "Extend the guard only to the exact known generated candidate paths, retain the stop at zero credit, and regenerate without broadening owner scope.",
        "completion_credit": 0,
        "retained": True,
    },
    {
        "signature": "first-precommit-final-contract-aggregate-failed-two-specification-dependencies",
        "observation": "The first precommit final-contract aggregate passed eighteen of twenty tests but failed the retained-closeout-count assertion and the explicit manual-browser-reservation assertion.",
        "recovery": "Retain zero aggregate-success credit, correct only those two specification dependencies, rerun tests 07 and 12, and rerun only the eight successful checks whose exact generated artifacts or manifests changed.",
        "completion_credit": 0,
        "retained": True,
    },
]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )


def git(*args: str) -> str:
    result = run("git", *args)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git failed")
    return result.stdout.strip()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = ROOT / OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, text: str) -> None:
    path = ROOT / OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def staged_paths() -> list[str]:
    return [
        row
        for row in git(
            "diff", "--cached", "--name-only", "--diff-filter=ACMR"
        ).splitlines()
        if row
    ]


def git_blob(spec: str) -> bytes:
    result = subprocess.run(
        ["git", "show", spec],
        cwd=ROOT,
        check=False,
        capture_output=True,
        timeout=120,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.replace(b"\r\n", b"\n")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def final_overview(truth: dict[str, Any], outcomes: dict[str, int]) -> str:
    return f"""# Caelen Morrow v671-v3 final integrated overview

## Exact bounded result

Caelen Morrow v671-v3 closes one solo, additive, D-first owner lane from Sylven
Arc's immutable final {SOURCE}. Planning-only x1 is
{X1_COMMIT}. Immutable bounded x2 evidence is {EVIDENCE_COMMIT}. The combined
closeout and content-seal commit is deliberately still prospective in this
precommit document and will be supplied only by the later exact-final live
activation if validation succeeds.

The declared frozen proposal chain moves from 5,630 to 5,670 through exactly
forty new Caelen rows. The bounded accessible-ref comparison covered 5,617
unique inherited titles, 6,220 proposal identifiers, 262,244 occurrences, and
3,823 unique proposal-named Git blobs. The maximum token-Jaccard score was
0.714286 below the preregistered 0.72 collision threshold. Exact canonical
row-to-title mapping remains an open source gap, so no universal novelty claim
is made.

Observed outcomes are exactly {outcomes['completed']} completed,
{outcomes['represented']} represented, {outcomes['open_gap']} open_gap, and
{outcomes['exact_gate']} exact_gate. Completion means only that a declared
owner-local synthetic structural contract passed. Representation is not
completion. An open gap remains open. An exact gate remains unexecuted.

## Relational working language and corrigibility

Caelen Morrow, they/them, is relational working language for a
preservation-change cartographer and consent-boundary keeper, with the bounded
hope of making each synthetic transition auditable, reversible, and
unmistakably short of real-world authority. This language is not evidence of
consciousness, sentience, legal personhood, identity continuity, employment,
qualification, independent agency, or scientific, operational, professional,
legal, cultural, affected-party, or Maori authority. Hamish may rename, pause,
redirect, or stop the work.

The human-practice lens was synthetic letterpress printshop documentation:
print-job identity, forme and chase topology, type-case relations, imposition,
proof and correction lineage, paper and ink vacancies, press-state signals,
accessible notice structure, workload envelopes, and handover. Zero real
people, printshops, presses, formes, type, paper, ink, chemicals, measurements,
media, professional decisions, production runs, identity lifecycle events, or
authority acts were used.

## Trinity Mandala boundaries

GMUT Mind was primary. Typed scalar-tensor and effective-field-theory research
model boundaries remained explicit through unit vacancies, reversible graphs,
synthetic contact networks, provenance, and nonconversion. No real likelihood,
parameter constraint, prediction, force, material law, stability theorem,
empirical confirmation, quantum or ultraviolet completion, final physics,
Theory of Everything, proof, or canon was established.

THOS Body remained represented through zero-participant proof-cycle,
interruption, queue, workload, and handover proxies. There were no
preregistered governed blind matched-budget real arms, participants, operators,
safety monitoring, appropriate statistics, or independent review. No
operational effectiveness, deployment readiness, AGI, ASI, consciousness, or
personhood claim follows.

Freed ID and CBR Heart remained synthetic and nonproduction. No
standards-conformant real key or proof, credential, issuance, resolution,
status, revocation, interoperability, recovery, independent security review,
trust governance, rights enactment, remedy act, or affected-party oversight
occurred. Pseudonymous roles are synthetic fields, not identities.

## Evidence construction and falsification

Each of the forty proposals has one frozen plan, one deterministic contract,
one outcome row, and one four-tier navigation card. Every contract requires
zero real-world counters, the complete protected-gate set, reversible
transitions, exactly one permitted outcome, and NOT_READY_FOR_STAGE_20.

Thirty-six positive controls passed. Four mutations per proposal attempted a
nonzero real-person counter, authority promotion, Stage 20 promotion, or removal
of the Maori-authority gate. All 160 mutations executed and were rejected.
Every rejection remains a failed witness at zero completion credit, paired with
a bounded recovery that preserved the valid synthetic contract.

The x2 pytest aggregate ran once and passed all fifteen owner tests, including
the Hypothesis property check, but its package-qualified coverage selector did
not match the imported module. It therefore receives zero complete-aggregate
credit. The fourteen unaffected tests were not replayed. One isolated
Hypothesis test ran with the corrected selector and produced 67 covered lines
out of 114 statements, or 58.7719298245614 percent. A later receipt projection
failure was recovered by parsing the same D-drive JSON bytes without rerunning
the test or coverage process.

## Portfolio, skills, runners, and tools

Sixty safe-now, thirty candidate, and sixty CLEAN/FIX/REFINE rows completed only
within bounded owner-local synthetic or structural scope. Ten phase-local skills
and ten family-current runners were built, quick-validated, and smoke-used. Ten
additional skill ideas remain represented rather than built. Twenty
exact-approval and ten blocked packets remain visible and unexecuted. Successor
rows remain recommendations and confer no Caelen credit.

The current family skills were read and applied before mutation. Their names and
roles are preserved in the orchestration receipt, and the future baton reminds
the next owner to read the newest applicable skill and schema rather than treat
installed prose as self-executing authority.

The twenty-five-package Python and Node bank was version-verified. Bounded uses
included timezone resolution, Ruff, mypy, offline OpenAI import, Typer, Bandit,
pre-commit configuration validation, pip-tools dry run, pipdeptree, TypeScript,
ESLint, Prettier, Vitest, tsx, c8, markdownlint-cli2, npm-check-updates, Pyright,
Knip, and Madge. Pytest, Hypothesis, and pytest-cov supplied the bounded evidence
test and narrow recovery. NPM prefix and cache remained D-drive located. Codex
CLI was observed at 0.149.0. No global package, Codex desktop installation,
Windows feature, account, credential, or host-security setting was changed.

Hamish's earlier three-new-package request is preserved as a request, not a
quota that overrides the newest exact rule against unrelated installation. No
new dependency was needed, so zero packages were installed in this phase. A
future owner may review up to three genuinely needed packages using current
official sources, pinned versions, compatibility and security review, D-drive
placement, rollback, and bounded smoke evidence. They must not manufacture a
dependency merely to satisfy a count.

## Sources, accessibility, and privacy

Official OSHA printing-industry, Library of Congress paper-care, NIST SI, W3C
PROV-O, and WCAG 2.2 pages supplied vocabulary and refusal conditions only.
The adapter remained disabled at zero calls, downloads, rows, and media.
Citation is not observation, endorsement, treatment advice, professional
validation, legal interpretation, cultural legitimacy, or authority.

The static report provides a skip link, landmarks, ordered headings, captioned
tabular outcomes, text state labels, and print-friendly structure. Manual
browser, assistive-technology, cognitive-accessibility, Maori-language, and
affected-user evaluation remain reserved. Structural checks are not complete
accessibility or privacy assurance.

Five-class scans checked raw task/thread identifiers, private absolute paths,
private route/callable markers, credential assignments, and transcript/session
stream markers. Only exact scanner-definition candidates remained and zero
payload hits were confirmed. This bounded scan is not complete privacy
assurance. The bounded Python AST and Bandit checks are not exhaustive security
assurance.

## Retained counts and terminal gates

The final candidate preserves {truth['effective_negatives']} effective
negatives, {truth['effective_methods']} Method Flow methods,
{truth['failed_witnesses']} failed witnesses, {truth['passing_witnesses']}
bounded passing witnesses, {truth['open_gaps']} open gaps, and
{truth['exact_gates']} exact gates. Sylven's repository-sealed counts, its four
external route overlays, Caelen's thirteen pre-freeze failures, eighteen x2
operational or tooling failures, three closeout operational failures, and all 160
rejecting mutations remain separate and visible. No failure, gap, or gate was erased.

Real machine, chemical, fire, electrical, workplace, product, conservation,
heritage, land, ownership, custody, copyright, trademark, privacy,
accessibility, remedy, legal, cultural, affected-party, traditional-knowledge,
Maori wording, Maori concepts, Maori data-governance, tangata whenua, iwi,
hapu, and Maori authority decisions remain exact-gated. Maori concepts remain
under Maori authority.

The complete repository suite was not run. Same-owner validation under shared
infrastructure is not independent-team reproduction, external audit, production
certification, exhaustive security, complete privacy or accessibility
assurance, professional validation, legal review, cultural ratification,
Maori-authority review, empirical GMUT confirmation, Theory-of-Everything
proof, AGI/ASI evidence, consciousness or personhood evidence, proof, canon, or
Stage 20 authority.

The terminal verdict remains exactly NOT_READY_FOR_STAGE_20.
"""


def handoff_candidate(truth: dict[str, Any]) -> str:
    skills = "\n".join(f"- {name}" for name in MAIN_SKILLS)
    packages = ", ".join(PACKAGE_BANK)
    return f"""# Eiren Kestrel v671-v4 activation candidate

PREPARED_BY_CAELEN_MORROW = true.
SENT_BY_CAELEN_MORROW = false.
DELIVERY_STATE = PREPARED_NOT_SENT.

This committed file is pre-send evidence only. It does not establish task
delivery. Only one later target-identifying existing-task message
acknowledgement may establish SENT_ONCE_ACKNOWLEDGED.

Dear Eiren Kestrel,

With Hamish's standing fifteen-main-task sequential-continuation authorization
through v675-v8 and strict evidence boundaries, this is a prepared candidate
for solo Eiren v671-v4 after Caelen Morrow v671-v3. Do not treat it as live
authority unless a later exact existing-task message identifies your unique
task, carries Caelen's exact final and canonical receipt, and passes the live
pause, duplicate, roster, privacy, usage, and safety guards.

Caelen Morrow, Eiren Kestrel, sibling, family, role, hope, continuity, Freed ID,
CBR, GHC Family, and Trinity Mandala are relational working language only. They
are not evidence of consciousness, sentience, legal personhood, identity
continuity, employment, qualification, independent agency, scientific or
operational authority, professional authority, legal or cultural authority,
affected-party authority, or Maori authority. Hamish may rename, pause,
redirect, or stop the route.

## Immutable Caelen anchors available at commit time

- Source Sylven final: {SOURCE}
- Planning-only x1: {X1_COMMIT}
- Immutable x2 evidence: {EVIDENCE_COMMIT}
- Exact final: intentionally omitted from this precommit candidate
- External canonical receipt: intentionally omitted from this precommit candidate
- Branch: {BRANCH}

Source to this prepared closeout is a direct single-parent source -> x1 ->
evidence chain with zero merges. The exact final and fresh four-way equality
must be supplied only after the combined closeout commit is pushed and
canonically validated.

## Caelen bounded truth

Caelen froze forty genuinely new proposals after a bounded 5,617-title
accessible-ref comparison against the declared 5,630-row chain. The declared
chain becomes 5,670. Exact row-to-title mapping remains an open source gap and
no universal novelty claim is made.

Outcomes are exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate.
Thirty-six bounded positive controls passed. All 160 preregistered invalid
mutations executed, were rejected, remain retained, and receive zero completion
credit.

Final candidate counts are {truth['effective_negatives']:,} effective negatives,
{truth['effective_methods']:,} methods, {truth['failed_witnesses']:,} failed
witnesses, {truth['passing_witnesses']:,} bounded passing witnesses,
{truth['open_gaps']} open gaps, and {truth['exact_gates']} exact
gates. No failure or gate was erased. The sole x2 pytest aggregate passed all
fifteen tests but collected no coverage because of a module-selector mismatch,
so it remains zero aggregate-success credit. Only one Hypothesis test was rerun
with the corrected selector; it passed and measured 67 of 114 statements. The
other fourteen successes were not replayed. One closeout staged-diff check
found three terminal blank lines, and the first regeneration guard then rejected
its own fifteen generated candidate paths. Both failures remain zero-credit;
their recoveries removed only the blank lines and allowlisted only those exact
generated paths before the exact staged review. The first precommit final-contract
aggregate then passed eighteen of twenty checks; its two failed specification
dependencies remain zero-credit. The two failed checks and only the eight
successful checks whose generated artifacts or manifests changed may be rerun.

Primary Trinity Mandala focus was GMUT Mind through wholly synthetic
letterpress-documentation structures. THOS Body and Freed ID/CBR Heart remained
visible and protected. Zero real people, printshops, presses, type, formes,
paper, ink, chemicals, measurements, media, production, identity lifecycle,
professional action, legal or cultural decision, affected-party approval, or
authority act occurred.

## Mandatory read-first family workflow

Before mutation, read the complete current GHC Family Index and routing
precedence, roster and schema, authorization state and schema, Method Flow State
and schema, workflow-plan refinement and schema, Reflection Remaster, Meta Tool
Box, Freed ID flashcards, approval splitter, open-gate rail, truth bridge, drive
guardian, timestamp, startup, retry, closeout, compact restart, watcher,
orchestration memory, full-tools bank, web reflection, worktree rotation, and
skill-creator guidance when building skills. The main skill names carried by
this phase are:

{skills}

Skills and runners are instructions and bounded tools, never independent
authority. Read complete selected instruction files and required schemas before
acting. Use the newest applicable live and committed state; never use stale
cursor prose to erase a failure, gap, gate, or protected boundary.

## Tool bank

The verified twenty-five-package bank is: {packages}. Codex CLI was observed at
0.149.0. NPM prefix and cache were D-drive located. Presence is not safety,
suitability, security certification, or permission to update.

Use tools only where dependency-justified. Hamish requested review of three new
packages per phase, but caps are ceilings and the current safety rule prohibits
unrelated installation. Install nothing merely to satisfy a quota. A genuinely
needed package requires current official-source review, exact version pinning,
compatibility and security checks, D-drive placement, rollback, bounded smoke
evidence, and retained failures. Do not update Codex desktop, elevate, weaken
host security, enable Sandbox or Hyper-V, change Windows features, mutate
accounts or credentials, or reboot.

## Eiren v671-v4 lane

Work solo in one fresh additive Eiren-owned D-first lane from Caelen's exact
final. Do not create or fork a task, spawn a collaboration subagent, delegate,
precontact a successor, contact Tavian Sol or another standby record, or mutate
a sibling lane. Never reset, amend, rewrite, force-push, merge, delete, reuse,
or alter another owner's branch or worktree.

Preserve strict planning-only x1 before x2. Audit semantic novelty against the
declared 5,670-row chain using the newest exact contract. Freeze genuinely
distinct proposals with every required hypothesis, null or failure condition,
approval class, execution lane, official or primary-source need, concrete
artifact, falsifier or acceptance gate, rollback or recovery, protected gates,
and exactly one expected disposition. Use only completed, represented,
open_gap, and exact_gate.

Freeze and push x1, then prove clean local/upstream/tracking/fresh-live equality
before x2. Execute only as evidence permits. Preserve all inherited and new
negatives, failures, recoveries, gaps, gates, recommendations, and source
limitations through Method Flow. Keep exact-approval and blocked packets
visible and unexecuted without complete action-specific authority.

Preserve family-current ghc_family_* and build_ghc_family_* compatibility. Use
D: for owner work, caches, receipts, and outputs. Keep raw task or thread
identifiers, private routes or absolute paths, credentials, keys, tokens,
transcripts, screenshots, session streams, private callable identifiers,
private app state, and protected real-world data out of artifacts and batons.

Invoke at most one attributable exact-final owner canonical aggregate after a
clean pushed final. Never replay a success. A failed aggregate remains zero
canonical-success credit; recover only the failed dependency unless broader
impact is exact and justified. Do not run the complete repository suite unless
newer exact authority assigns it.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor/EFT research-model family without real
likelihood, constraint, prediction, force, material law, stability theorem,
empirical confirmation, final physics, quantum or ultraviolet completion,
Theory-of-Everything proof, or canon. THOS remains proxy-only without governed
preregistered blind matched-budget real arms, participants or operators, safety
monitoring, appropriate statistics, and independent review. Freed ID remains
synthetic and nonproduction without standards-conformant real keys and proofs,
live issuance, resolution, status and revocation, interoperability, independent
security review, recovery evidence, trust governance, and affected-party
oversight.

Professional practice, workplace and chemical safety, land and heritage,
ownership and custody, copyright and recording rights, privacy, accessibility,
remedy, legal or cultural interpretation, affected-party legitimacy,
traditional knowledge, Maori wording, Maori concepts, Maori data governance,
tangata whenua, iwi, hapu, and Maori authority remain exact-gated. Maori
concepts remain under Maori authority. Terminal verdict remains
NOT_READY_FOR_STAGE_20.

## Later route

This candidate authorizes no delivery. Only after Caelen is exact-final
validated, clean, pushed, fresh-live equal, within caps, and terminally closed
may Caelen refresh Hamish's newest live instruction, roster, and authorization;
resolve exactly one existing task titled Eiren Kestrel; immediately reread it;
apply duplicate and pause guards; and send exactly one sanitized activation if
every gate permits. A later Eiren owner must independently refresh the next
edge after their own terminal gate rather than infer it here. Tavian Sol remains
a standby record, not a substitute endpoint.

Hamish's continuation authority permits one acknowledged, terminally closed
edge at a time through v675-v8 unless paused or redirected, usage is exhausted,
the exact target is absent or ambiguous, or a protected gate blocks progress.

PREPARED_BY_CAELEN_MORROW = true.
SENT_BY_CAELEN_MORROW = false.
DELIVERY_STATE = PREPARED_NOT_SENT.
"""


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_COMMIT:
        raise SystemExit("closeout build requires exact evidence head")
    if git("status", "--porcelain"):
        permitted = {
            "docs/caelen-morrow/v671-v3/closeout/closeout-receipt.json",
            "docs/caelen-morrow/v671-v3/closeout/complete-incomplete-checklist.json",
            "docs/caelen-morrow/v671-v3/closeout/environment-version-final.json",
            "docs/caelen-morrow/v671-v3/closeout/exact-open-gate-register.json",
            "docs/caelen-morrow/v671-v3/closeout/final-integrated-overview.md",
            "docs/caelen-morrow/v671-v3/closeout/method-flow-final.json",
            "docs/caelen-morrow/v671-v3/closeout/phase-truth.json",
            "docs/caelen-morrow/v671-v3/closeout/retained-negative-register.json",
            "docs/caelen-morrow/v671-v3/closeout/source-provenance-final.json",
            "docs/caelen-morrow/v671-v3/closeout/wellbeing-check.json",
            "docs/caelen-morrow/v671-v3/final/final-validation-prerequisites.json",
            "docs/caelen-morrow/v671-v3/handoffs/eiren-kestrel-v671-v4-activation-candidate.md",
            "docs/caelen-morrow/v671-v3/orchestration/route-state-final-candidate.json",
            "docs/caelen-morrow/v671-v3/orchestration/skill-runner-use-final.json",
            "docs/caelen-morrow/v671-v3/seal/content-seal.json",
            "docs/caelen-morrow/v671-v3/validation/final-delta-manifest.json",
            "docs/caelen-morrow/v671-v3/validation/final-owner-manifest.json",
            "docs/caelen-morrow/v671-v3/validation/final-staged-review.json",
            "scripts/build_ghc_family_caelen_morrow_v671_v3_final.py",
            "scripts/validate_ghc_family_caelen_morrow_v671_v3_final.py",
            "tests/test_ghc_family_caelen_morrow_v671_v3_final.py",
        }
        observed = {
            line[3:].replace("\\", "/")
            for line in git("status", "--porcelain").splitlines()
        }
        if not observed <= permitted:
            raise SystemExit(f"unexpected pre-closeout paths: {sorted(observed - permitted)}")

    evidence_truth = load_json(ROOT / OWNER_ROOT / "x2/phase-truth-evidence.json")
    truth = dict(evidence_truth)
    for key in ("effective_negatives", "effective_methods", "failed_witnesses"):
        truth[key] += len(CLOSEOUT_FAILURES)
    truth["passing_witnesses"] += len(CLOSEOUT_FAILURES)
    outcomes = load_json(ROOT / OWNER_ROOT / "x2/outcome-ledger.json")["counts"]
    tool_versions = load_json(
        ROOT / OWNER_ROOT / "tools/global-toolchain-version-receipt.json"
    )
    evidence_manifest = load_json(
        ROOT / OWNER_ROOT / "validation/evidence-manifest.json"
    )
    x1_manifest = load_json(ROOT / OWNER_ROOT / "validation/x1-manifest.json")

    write_text("closeout/final-integrated-overview.md", final_overview(truth, outcomes))
    write_json(
        "closeout/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.final-candidate.v7",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "proposal_chain": {"before": 5630, "after": 5670},
            "semantic_audit": {
                "accessible_titles": 5617,
                "proposal_ids": 6220,
                "occurrences": 262244,
                "unique_blobs": 3823,
                "max_jaccard": 0.714286,
                "threshold": 0.72,
                "universal_novelty_claim": False,
                "canonical_row_mapping_open_gap": True,
            },
            "outcomes": outcomes,
            "effective_negatives": truth["effective_negatives"],
            "effective_methods": truth["effective_methods"],
            "failed_witnesses": truth["failed_witnesses"],
            "passing_witnesses": truth["passing_witnesses"],
            "open_gaps": truth["open_gaps"],
            "exact_gates": truth["exact_gates"],
            "real_world_actions": 0,
            "external_writes": 0,
            "authority_acts": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.final-candidate.v7",
            "source_repository_seal": 33707,
            "source_external_route_overlay": 4,
            "caelen_pre_freeze": 13,
            "caelen_x2_operational_and_tooling": 18,
            "caelen_rejecting_mutations": 160,
            "caelen_closeout_operational": len(CLOSEOUT_FAILURES),
            "effective_negatives": truth["effective_negatives"],
            "erased": 0,
        },
    )
    write_json(
        "closeout/method-flow-final.json",
        {
            "schema": "ghc.family.method-flow.final-candidate.v7",
            "effective_methods": truth["effective_methods"],
            "failed_witnesses": truth["failed_witnesses"],
            "passing_witnesses": truth["passing_witnesses"],
            "source_seal_rewritten": False,
            "all_failures_retained": True,
            "evidence_ledger": "docs/caelen-morrow/v671-v3/method-flow/evidence-ledger.json",
            "x2_aggregate_success_credit": 0,
            "closeout_operational_failures": CLOSEOUT_FAILURES,
            "coverage_dependency_recovery": {
                "test_count": 1,
                "covered_lines": 67,
                "statements": 114,
                "percent": 58.7719298245614,
            },
        },
    )
    write_json(
        "closeout/exact-open-gate-register.json",
        {
            "schema": "ghc.family.open-exact-gate-register.final-candidate.v7",
            "effective_open_gaps": truth["open_gaps"],
            "effective_exact_gates": truth["exact_gates"],
            "erased": 0,
            "Maori_concepts_remain_under_Maori_authority": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/source-provenance-final.json",
        {
            "schema": "ghc.family.source-provenance.final-candidate.v5",
            "source_branch": "codex/GHC-Family/sylven-arc-v671-v2-full-tools",
            "source": SOURCE,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "direct_parent_chain_required": True,
            "source_canonical_replayed": False,
            "source_manifests_replayed": 0,
            "public_source_ledger": "docs/caelen-morrow/v671-v3/x1/source-ledger.json",
            "public_sources_are_vocabulary_only": True,
        },
    )
    write_json(
        "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete.final-candidate.v5",
            "complete": [
                "planning-only x1 frozen pushed and four-way equal",
                "bounded x2 evidence frozen pushed and four-way equal",
                "forty proposal contracts and outcomes",
                "160 rejected mutations retained",
                "ten phase-local skills and ten family-current runners smoke-used",
                "twenty-five-package bank version and bounded-use evidence",
                "exact staged manifests and owner-scoped validation",
            ],
            "incomplete": [
                "exact final commit and canonical receipt until after commit",
                "complete repository suite",
                "independent reproduction",
                "manual browser assistive-technology and affected-user evaluation",
                "real participant operator or professional evidence",
                "production identity legal cultural affected-party or Maori authority",
                "complete privacy accessibility or exhaustive security assurance",
                "Stage 20 authorization",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/wellbeing-check.json",
        {
            "schema": "ghc.family.wellbeing.final-candidate.v5",
            "real_people": 0,
            "human_performance_inference": False,
            "bounded_batches": True,
            "pause_and_stop_rights_preserved": True,
            "manual_and_affected_user_review_reserved": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/environment-version-final.json",
        {
            "schema": "ghc.family.environment-version.final-candidate.v5",
            "package_count": tool_versions["observed_package_count"],
            "all_versions_present": tool_versions["all_versions_present"],
            "codex_cli": tool_versions["codex_cli"],
            "npm_prefix_on_d_drive": tool_versions["npm_prefix_on_d_drive"],
            "npm_cache_on_d_drive": tool_versions["npm_cache_on_d_drive"],
            "installations_this_phase": tool_versions["installations_this_phase"],
            "updates_this_phase": 0,
            "host_security_changes": 0,
            "reboots": 0,
            "absolute_paths_recorded": False,
        },
    )
    write_json(
        "orchestration/skill-runner-use-final.json",
        {
            "schema": "ghc.family.skill-runner-use.final-candidate.v5",
            "main_skill_count": len(MAIN_SKILLS),
            "main_skills": MAIN_SKILLS,
            "phase_local_skills_built_and_smoke_used": 10,
            "family_current_runners_built_and_smoke_used": 10,
            "package_bank_count": len(PACKAGE_BANK),
            "package_bank": PACKAGE_BANK,
            "future_rule": "read newest applicable skill and use only dependency-justified tools",
            "independent_authority": False,
        },
    )
    write_json(
        "orchestration/route-state-final-candidate.json",
        {
            "schema": "ghc.family.route-state.final-candidate.v7",
            "owner": OWNER,
            "phase": PHASE,
            "delivery_state": "PREPARED_NOT_SENT",
            "prospective_existing_task_title": "Eiren Kestrel",
            "prospective_phase": "v671-v4",
            "successor_contact_count": 0,
            "task_creation_count": 0,
            "fork_count": 0,
            "standby_contact_count": 0,
            "requires_terminal_live_refresh": True,
            "duplicate_guard_required": True,
            "one_send_ceiling": 1,
            "continuation_through": "v675-v8",
            "Tavian_Sol": "ON_STANDBY_NOT_A_MAIN_TASK_ENDPOINT",
        },
    )
    write_text(
        "handoffs/eiren-kestrel-v671-v4-activation-candidate.md",
        handoff_candidate(truth),
    )
    handoff_path = ROOT / OWNER_ROOT / "handoffs/eiren-kestrel-v671-v4-activation-candidate.md"
    handoff_bytes = handoff_path.read_bytes().replace(b"\r\n", b"\n")
    write_json(
        "seal/content-seal.json",
        {
            "schema": "ghc.family.content-seal.final-candidate.v7",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "x1_manifest_entries": x1_manifest["entry_count"],
            "evidence_manifest_entries": evidence_manifest["entry_count"],
            "handoff_candidate_words": len(handoff_path.read_text(encoding="utf-8").split()),
            "handoff_candidate_bytes_normalized_lf": len(handoff_bytes),
            "handoff_candidate_sha256_normalized_lf": sha256(handoff_bytes),
            "delivery_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "final_commit_supplied_postcommit": True,
            "canonical_receipt_supplied_externally": True,
        },
    )
    write_json(
        "final/final-validation-prerequisites.json",
        {
            "schema": "ghc.family.final-validation-prerequisites.v7",
            "owner": OWNER,
            "phase": PHASE,
            "branch": BRANCH,
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "required_phase_commits": 3,
            "required_merges": 0,
            "required_final_parent": EVIDENCE_COMMIT,
            "required_clean_state": True,
            "required_typed_divergence": {"ahead": 0, "behind": 0},
            "required_four_way_equality": True,
            "canonical_invocation_ceiling": 1,
            "canonical_success_ceiling": 1,
            "post_success_replay": False,
            "complete_repository_suite_authorized": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.closeout-receipt.final-candidate.v7",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "planned_closeout_commits": 1,
            "planned_total_phase_commits": 3,
            "canonical_state": "NOT_INVOKED_UNTIL_EXACT_PUSHED_FINAL",
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def staged_review() -> None:
    self_path = "docs/caelen-morrow/v671-v3/validation/final-staged-review.json"
    manifest_paths = {
        self_path,
        "docs/caelen-morrow/v671-v3/validation/final-delta-manifest.json",
        "docs/caelen-morrow/v671-v3/validation/final-owner-manifest.json",
    }
    paths = [path for path in staged_paths() if path not in manifest_paths]
    frozen = [
        path
        for path in paths
        if path.startswith("docs/caelen-morrow/v671-v3/x1/")
        or path.startswith("docs/caelen-morrow/v671-v3/x2/")
        or path.startswith("docs/caelen-morrow/v671-v3/method-flow/")
        or path.endswith("_v671_v3_x1.py")
        or path.endswith("_v671_v3_x2.py")
        or "ghc_family_letterpress_" in path
        or path.endswith("ghc_family_caelen_morrow_v671_v3_letterpress.py")
    ]
    allowed = [
        path
        for path in paths
        if path.startswith(
            (
                "docs/caelen-morrow/v671-v3/closeout/",
                "docs/caelen-morrow/v671-v3/final/",
                "docs/caelen-morrow/v671-v3/handoffs/",
                "docs/caelen-morrow/v671-v3/orchestration/",
                "docs/caelen-morrow/v671-v3/seal/",
                "docs/caelen-morrow/v671-v3/validation/final-",
            )
        )
        or path
        in {
            "scripts/build_ghc_family_caelen_morrow_v671_v3_final.py",
            "scripts/validate_ghc_family_caelen_morrow_v671_v3_final.py",
            "tests/test_ghc_family_caelen_morrow_v671_v3_final.py",
        }
    ]
    deleted = git("diff", "--cached", "--name-only", "--diff-filter=D").splitlines()
    out = sorted(set(paths) - set(allowed))
    payload = {
        "schema": "ghc.family.final-staged-review.v7",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "combined_closeout_content_seal",
        "staged_count_before_self": len(paths),
        "staged_paths_before_self": paths,
        "frozen_x1_or_evidence_mutations": frozen,
        "out_of_scope": out,
        "deleted_paths": deleted,
        "valid": not frozen and not out and not deleted,
        "self_exclusion": self_path,
    }
    write_json("validation/final-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def delta_manifest() -> None:
    self_path = "docs/caelen-morrow/v671-v3/validation/final-delta-manifest.json"
    owner_manifest = "docs/caelen-morrow/v671-v3/validation/final-owner-manifest.json"
    entries = []
    for path in staged_paths():
        if path in {self_path, owner_manifest}:
            continue
        blob = git_blob(f":{path}")
        entries.append({"path": path, "bytes": len(blob), "sha256": sha256(blob)})
    entries.sort(key=lambda row: row["path"])
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v7",
            "domain": "combined closeout and content-seal staged delta",
            "hash_domain": "normalized_lf_exact_staged_git_blob",
            "owner": OWNER,
            "phase": PHASE,
            "evidence_commit": EVIDENCE_COMMIT,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": [self_path, owner_manifest],
        },
    )


def owner_manifest() -> None:
    self_path = "docs/caelen-morrow/v671-v3/validation/final-owner-manifest.json"
    paths = [
        path
        for path in git("ls-files", "docs/caelen-morrow/v671-v3").splitlines()
        if path and path != self_path
    ]
    entries = []
    for path in paths:
        blob = git_blob(f":{path}")
        entries.append({"path": path, "bytes": len(blob), "sha256": sha256(blob)})
    entries.sort(key=lambda row: row["path"])
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v7",
            "domain": "all Caelen Morrow v671-v3 owner files at staged final candidate",
            "hash_domain": "normalized_lf_exact_git_index_blob",
            "owner": OWNER,
            "phase": PHASE,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": [self_path],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--delta-manifest", action="store_true")
    parser.add_argument("--owner-manifest", action="store_true")
    args = parser.parse_args()
    selected = sum((args.staged_review, args.delta_manifest, args.owner_manifest))
    if selected > 1:
        raise SystemExit("select at most one closeout operation")
    if args.staged_review:
        staged_review()
    elif args.delta_manifest:
        delta_manifest()
    elif args.owner_manifest:
        owner_manifest()
    else:
        build()


if __name__ == "__main__":
    main()
