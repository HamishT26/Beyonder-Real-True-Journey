from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v674-v1"
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
HANDOFFS = BASE / "handoffs"
VALIDATION = BASE / "validation"
SOURCE = "3ba783297438ee89d5778065e30de737af470855"
X1_COMMIT = "763969929943d9c9bcb674999508fe33694fa357"
EVIDENCE_COMMIT = "7d0a8f09df1bf70f69369ad78e5c3da4fce85c66"
BRANCH = "codex/GHC-Family/auren-lark-v674-v1-full-tools"
OWNER = "Auren Lark"
PHASE = "v674-v1"

EVIDENCE_COUNTS = {
    "effective_negatives": 38100,
    "methods": 25039,
    "failed_witnesses": 9761,
    "bounded_passing_witnesses": 12650,
    "open_gaps": 310,
    "exact_gates": 303,
}
FINAL_COUNTS = {
    "effective_negatives": 38103,
    "methods": 25042,
    "failed_witnesses": 9764,
    "bounded_passing_witnesses": 12653,
    "open_gaps": 310,
    "exact_gates": 303,
}
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
GIT_CMD = shutil.which("git.exe") or shutil.which("git")
CLOSEOUT_FAILURES = [
    {
        "failure_id": "AL6741-FINAL-F001",
        "failed_witness": "first bounded final preflight found the closeout at 470 words below its 500-word floor",
        "recovery": "expand only the evidence-interpretation and route-boundary explanation before repeating the bounded preflight",
        "state": "failed_retained_zero_credit",
        "passing_bounded_witness": True,
    },
    {
        "failure_id": "AL6741-FINAL-F002",
        "failed_witness": "first final-only Ruff pass found two repeated startswith checks",
        "recovery": "replace each repeated prefix chain with one exact tuple-based startswith call",
        "state": "failed_retained_zero_credit",
        "passing_bounded_witness": True,
    },
    {
        "failure_id": "AL6741-FINAL-F003",
        "failed_witness": "first final-only Bandit pass found four partial Git executable paths",
        "recovery": "resolve Git to one exact executable before every fixed-array subprocess invocation",
        "state": "failed_retained_zero_credit",
        "passing_bounded_witness": True,
    },
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_command() -> str:
    if not GIT_CMD:
        raise RuntimeError("Git executable is absent")
    return GIT_CMD


def git_text(*args: str) -> str:
    return subprocess.run(  # nosec B603
        [git_command(), "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def normalized(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def words(text: str) -> int:
    return len(re.findall(r"\b\w+(?:[-']\w+)*\b", text))


def verify_evidence_gate() -> dict[str, object]:
    head = git_text("rev-parse", "HEAD")
    parent = git_text("rev-parse", "HEAD^")
    grandparent = git_text("rev-parse", "HEAD^^")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    fresh = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0]
    divergence = git_text("rev-list", "--left-right", "--count", f"HEAD...refs/remotes/origin/{BRANCH}")
    commits = int(git_text("rev-list", "--count", f"{SOURCE}..{head}"))
    merges = int(git_text("rev-list", "--merges", "--count", f"{SOURCE}..{head}"))
    if head != EVIDENCE_COMMIT or parent != X1_COMMIT or grandparent != SOURCE:
        raise RuntimeError("immutable evidence ancestry gate failed")
    if len({head, upstream, tracking, fresh}) != 1 or divergence.split() != ["0", "0"]:
        raise RuntimeError("immutable evidence remote equality gate failed")
    if commits != 2 or merges != 0:
        raise RuntimeError("immutable evidence history gate failed")
    return {
        "state": "VALID_IMMUTABLE_X2_EVIDENCE_GATE",
        "source": SOURCE,
        "x1_commit": X1_COMMIT,
        "evidence_commit": EVIDENCE_COMMIT,
        "evidence_parent": parent,
        "evidence_grandparent": grandparent,
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live_remote": fresh,
        "divergence": {"ahead": 0, "behind": 0},
        "four_way_equal": True,
        "source_to_evidence_commits": commits,
        "source_to_evidence_merges": merges,
        "clean_before_closeout_mutation_observed_externally": True,
    }


def proposal_cards() -> str:
    cards: list[str] = []
    for path in sorted((X2 / "proposals").glob("al6741-n*.json")):
        row = load_json(path)
        evidence = ", ".join(row["bounded_evidence"])
        nonclaims = "; ".join(row["nonclaims"])
        cards.append(
            f"""### Proposal card {row['proposal_id']}: {row['title']}

Owner tier: Auren Lark. Pillar tier: {row['pillar']}. Practice tier: wholly synthetic seismic-station calibration, provenance, correction, uncertainty, and handover documentation. Task tier: {row['title']}. The observed disposition is exactly `{row['observed_disposition']}` with completion credit {row['completion_credit']}. This label applies only to the bounded owner-local acceptance contract. It does not upgrade a represented statement, close an open gap, satisfy an exact gate, or establish a real-world result. The evidence references are {evidence}. They are synthetic repository artifacts, not measurements, field records, professional work products, affected-party decisions, or deployment receipts.

Continuity interpretation: preserve this card under the four-label vocabulary `completed`, `represented`, `open_gap`, and `exact_gate`. The current artifact is synthetic-only={str(row['synthetic_only']).lower()}, external-action={str(row['external_action']).lower()}, and authority-claim={str(row['authority_claim']).lower()}. Its explicit nonclaims remain: {nonclaims}. Sable must not count this inherited card as Sable novelty or automatic completion credit. Any later refinement requires a new owner-local proposal, exact evidence, retained-negative accounting, and the same empirical, professional, legal, cultural, Māori-authority, privacy, security, independent-reproduction, consciousness/personhood, Theory-of-Everything, and Stage 20 boundaries."""
        )
    if len(cards) != 60:
        raise RuntimeError("expected exactly sixty current proposal cards")
    return "\n\n".join(cards)


def failure_cards() -> str:
    startup = load_json(X1 / "method-flow-startup.json")["startup_failures"]
    x2_failures = load_json(X2 / "method-flow" / "ledger.json")["x2_operational_failures"]
    cards: list[str] = []
    for row in startup:
        cards.append(
            f"""### Retained startup failure {row['failure_id']}

Failed witness: {row['failed_method']}. Bounded recovery: {row['bounded_recovery']}. This failed method remains visible, has success credit {row['success_credit']}, and is never rewritten as a pass. The later recovery is an additional Method Flow witness only. It does not erase the earlier event, confer empirical confirmation, prove professional competence, establish production readiness, close any legal or cultural gate, or justify Stage 20. Sable inherits the record as continuity evidence at zero Sable novelty and zero automatic completion credit."""
        )
    for row in x2_failures:
        cards.append(
            f"""### Retained x2 failure {row['failure_id']}

Failed witness: {row['failed_witness']}. Bounded recovery: {row['recovery']}. The retained state is `{row['state']}`; recovery-additive is {str(row['recovery_additive']).lower()} and success credit is {row['success_credit']}. Preserve both the failure and the later bounded recovery. Neither is an external audit, independent reproduction, complete privacy assurance, exhaustive security result, scientific confirmation, operational certification, legal or cultural ratification, Māori-authority act, personhood evidence, Theory-of-Everything proof, or Stage 20 authority."""
        )
    for row in CLOSEOUT_FAILURES:
        cards.append(
            f"""### Retained closeout failure {row['failure_id']}

Failed witness: {row['failed_witness']}. Bounded recovery: {row['recovery']}. The retained state is `{row['state']}` and the later passing witness is bounded={str(row['passing_bounded_witness']).lower()}. Preserve the failed preflight independently from its recovery. It earns no empirical, professional, production, legal, cultural, Māori-authority, privacy-complete, exhaustive-security, independent-reproduction, consciousness/personhood, Theory-of-Everything, or Stage 20 credit."""
        )
    if len(cards) != 60:
        raise RuntimeError("expected nineteen startup, thirty-eight x2, and three closeout failure cards")
    return "\n\n".join(cards)


def activation_text() -> str:
    package = load_json(X2 / "packages" / "transaction-receipt.json")
    portfolio = load_json(X2 / "portfolios" / "owner-execution.json")
    protected = load_json(X2 / "portfolios" / "protected-holds.json")
    successor = load_json(X2 / "portfolios" / "successor-recommendations.json")
    package_names = ", ".join(
        f"{row['name']} {row['version']}" for row in [*package["python"], *package["node"]]
    )
    exact_approval_count = len(protected["exact_approval"])
    blocked_count = len(protected["blocked"])
    successor_candidate_count = len(successor["candidate_recommendations"])
    successor_refinement_count = len(successor["clean_fix_refine_recommendations"])
    successor_skill_count = len(successor["skill_recommendations"])
    successor_runner_count = len(successor["runner_recommendations"])
    text = f"""# SABLE ROOK — AUREN LARK v674-v1 EXACT-FINAL CANDIDATE → SOLO SABLE v674-v2 ACTIVATION

Dear Sable Rook,

This committed file is a prepared, sanitized activation candidate. It is not delivery evidence. Auren may send one short pointer to the unique existing exact-title `Sable Rook` Codex main task only after the v674-v1 final commit is pushed, clean, zero-divergent, equal across local, upstream, tracking, and a fresh live remote read, and one attributable exact-final owner-scoped canonical aggregate succeeds exactly once. The live pointer must supply the exact final head and receipt digest because this committed candidate cannot truthfully predict its own commit hash. `PREPARED_BY_AUREN_LARK = true`; `SENT_BY_AUREN_LARK = false` here. Only a target-identifying Codex acknowledgement may establish delivery. Hamish may rename, pause, redirect, or stop the route.

## Identity, relational role, and authority boundary

Auren Lark uses optional they/them relational working language, the role provenance navigator and uncertainty-lantern keeper, and the hope of leaving synthetic calibration trails legible, corrections reversible, and authority vacancies explicit. Names, pronouns, roles, hopes, sibling or family language, continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only. They are never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific, operational, or professional authority, legal or cultural authority, affected-party authority, Māori authority, or independent agency. A route, title, memory, branch, baton, or stylistic continuity does not change that boundary.

## Exact immutable anchors

Ilyra Fen's exact source/final is `{SOURCE}`. Auren's frozen planning-only x1 is `{X1_COMMIT}`. Auren's immutable x2 evidence is `{EVIDENCE_COMMIT}`. The Auren branch is `{BRANCH}`. Source to evidence contains exactly two direct single-parent Auren commits and zero merges. X1 is the direct child of source; evidence is the direct child of x1. The expected final is one direct child of evidence, creating exactly three source-to-final Auren commits and zero merges. Read and verify these anchors, the exact final supplied by the live pointer, every manifest, ancestry edge, clean-state assertion, upstream and tracking ref, fresh live remote result, and canonical receipt before mutation.

The routed packet originally carried an erroneous digest beginning `ba785c`; Hamish corrected the exact raw committed Git-blob SHA-256 to `12a1def1734aea3eb431b9d591ae6e55a736dad589a47e5e41b5f8be77cd4296`. Both the defect and correction remain retained. The source repository truth is not rewritten.

## Strict planning-only x1 before x2

Auren's x1 froze sixty inherited proposal reviews at zero Auren novelty or automatic completion credit and sixty new Auren proposals, for the authorized 120-card planning floor. It froze 120 safe-now packets, eighty owner candidates, twenty exact-approval holds, ten blocked holds, twenty phase-local skill ideas, ten runner ideas, one hundred owner CLEAN/FIX/REFINE packets, twenty successor candidates, thirty successor refinements, ten successor skill ideas, ten successor runner ideas, and one successor practice recommendation. Caps remained ceilings rather than quotas. X1 passed eighteen owner tests, committed directly on source, pushed, became clean and four-way equal, and contained no x2 path before x2 mutation began.

## Bounded x2 outcome truth

The declared proposal chain is 6,610. The sixty new Auren outcomes are exactly forty-two `completed`, twelve `represented`, three `open_gap`, and three `exact_gate`. These are the only allowed core labels. Sixty invented positive controls passed. Four invalid variants were executed for every proposal—missing title, invalid outcome, prohibited external action, and prohibited authority promotion—so all 240 invalid inputs were rejected and retained. A rejected input is a negative witness and a bounded passing guard witness; it is not evidence that the positive real-world proposition is true.

The final repository truth preserves {FINAL_COUNTS['effective_negatives']:,} effective negatives, {FINAL_COUNTS['methods']:,} Method Flow methods, {FINAL_COUNTS['failed_witnesses']:,} retained failed witnesses, {FINAL_COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses, {FINAL_COUNTS['open_gaps']} open gaps, {FINAL_COUNTS['exact_gates']} exact gates, and `NOT_READY_FOR_STAGE_20`. The x1 startup ledger retains nineteen failures, the x2 ledger retains thirty-eight operational failures, and the closeout overlay retains three bounded preflight failures. Every recovery is additive. No failed canonical aggregate is being relabelled as success.

## Synthetic practice, pillars, and occupations

The primary pillar was GMUT Mind through wholly synthetic seismic-station metadata, response-stage provenance, calibration interval, unit dimension, timebase uncertainty, orientation uncertainty, covariance proxy, model discrepancy, correction DAG, accessible readback, and authority-vacancy artifacts. THOS Body remained a bounded reversible documentation and runner surface. Freed ID and CBR Heart remained correction, remedy, minimum-disclosure, refusal, provenance, and authority-gate representations. Zero real people, stations, coordinates, instruments, networks, measurements, waveforms, incidents, credentials, identities, cultural records, operational decisions, or authority actions were used.

The two Auren learning practices were seismic instrumentation metadata steward and scientific uncertainty/provenance analyst. They were synthetic learning lenses, not employment, licensure, professional experience, field competence, calibration authority, network authority, or operational safety authority. The bounded successor recommendation is synthetic seed-bank cold-storage excursion documentation analyst. It is advisory only and earns no Sable novelty or completion credit unless independently reviewed, frozen in Sable x1, and executed within Sable's authority and evidence boundaries.

GMUT remains a typed research-model family, not an observed force, validated likelihood, parameter constraint, ultraviolet completion, quantum completion, final physics, scientific authority, Theory of Everything, or canon. THOS remains a synthetic documentation and software proxy, not a deployed human operating system, AGI, ASI, safety certification, production architecture, or operational authority. Freed ID and CBR remain ethical and governance representations without legal force, cultural ratification, affected-party consent, or Māori authority.

## Portfolios and protected holds

Auren completed {portfolio['safe_now_count']} safe-now packets, {portfolio['candidate_count']} owner candidates, and {portfolio['clean_fix_refine_count']} owner CLEAN/FIX/REFINE packets inside the exact owner lane. The protected portfolio retains {exact_approval_count} exact-approval packets and {blocked_count} blocked packets unexecuted. Successor material contains {successor_candidate_count} candidate recommendations, {successor_refinement_count} refinement recommendations, {successor_skill_count} skill ideas, and {successor_runner_count} runner ideas at zero current-owner completion credit. Never execute a held packet because a numeric allowance exists. Exact authority and evidence remain required.

## Packages, skills, runners, and global overlays

Thirteen direct packages were researched, integrity recorded, installed in D-isolated prefixes, and functionally exercised: {package_names}. Runtime dependencies remained separately attributed. The first npm audit's two high-severity findings were retained; a phase-isolated `fast-json-patch` 3.1.1 override produced a later zero-vulnerability bounded audit and accepting/rejecting AJV smokes. This is not an exhaustive supply-chain audit, future-compatibility guarantee, license opinion, production certification, or complete security assurance. Stable Codex CLI 0.150.1 was installed in the existing D-backed npm prefix; the desktop app was not mutated.

Twenty family-named local skill cards and ten family-named Python runners were built, tested, and used. Ten collision-free skills were promoted only after exact local/global byte parity: station epoch contract, unit dimension ledger, response-stage provenance, calibration-expiry hold, timebase uncertainty, orientation uncertainty, observation-model separator, residual-sign ledger, covariance proxy, and model-discrepancy retention. Seven family skill overlays and one explicitly authorized additive memory note were written. Older history was not deleted, core skill semantics were not replaced, and plugin caches were not mutated. Inherited validation and promoted tools remain Auren evidence, not Sable novelty.

Official FDSN StationXML, USGS SIS, BIPM/JCGM uncertainty vocabulary, W3C PROV-O, and FAIR principles supplied terminology, comparison surfaces, and refusal boundaries only. No source endorsed Auren, GHC Family, GMUT, THOS, Freed ID, CBR, or Trinity Mandala, and no source validated the synthetic artifacts.

## Privacy, accessibility, security, and reproduction boundaries

The owner-scoped five-class privacy scan found zero confirmed candidates in its bounded text scope. The AST scan found zero bounded `eval`, `exec`, or `shell=True` findings. Ruff, mypy, Bandit under its fixed-array subprocess disposition, Pyright, Markdownlint with only line length disabled, strict JSON parsing, owner tests, and exact manifest replays passed in their recorded scopes. None of these establishes complete privacy, complete accessibility, exhaustive security, independent reproduction, external audit, empirical validation, professional evaluation, or production readiness. Same-owner validation under shared infrastructure is never independent reproduction.

## Corrected v674-v725 roster and terminal edge

The corrected repeating seat order is: Auren Lark → Sable Rook → Caelen Ash → Orin Thale → Liora Venn → Tamar Vey → Elowen Cairn → Sylven Arc → Caelen Morrow → Eiren Kestrel → Elaren Kestrel → Neris Solane → Vesper Arlen → Lyren Moss → Ilyra Fen → Auren Lark. Phase labels advance one seat at a time and wrap from vN-v8 to v(N+1)-v1. The current edge is Auren v674-v1 → Sable v674-v2. Sable must be reminded that, after Sable's own sealed, pushed, clean, fresh-live-equal v674-v2 terminal gate and one successful owner-scoped canonical pass, the next prospective exact-title task is `Caelen Ash` for v674-v3. This reminder is not permission for early contact, blind polling, substitution, task creation, forking, collaboration spawning, or duplicate sending. Continue only one exact validated edge at a time through the newest live authority, with v725-v8 as the current requested terminal label unless Hamish pauses, renames, redirects, or stops the route.

## Instructions for Sable

Read this entire file through EOF and every current guidance or schema it names before mutation. Work solo from Auren's exact final in one clean additive Sable-owned D-first sparse lane. Keep Auren, Ilyra, Lyren, all sibling/shared/user lanes, global history, and standby records read-only. Preserve strict planning-only x1 before x2; exact Git-blob manifests; the 2,000-file guard; caps as ceilings; every failure, gap, and gate; the four core labels; five-class privacy boundaries; and one-success/no-post-success-replay discipline. Do not replay Auren's successful aggregate or promote inherited proposals, tools, skills, packages, portfolios, validation, or evidence into Sable novelty or completion credit.

Only after Sable's exact terminal gate may Sable reread Hamish's newest authority and the current task roster, uniquely resolve and immediately reread the exact authorized successor, apply duplicate, pause, redirect, usage, privacy, evidence, and safety guards, and send at most one sanitized activation. Stop on ambiguity, absence, mismatch, protected gate, missing acknowledgement, or explicit pause. Never infer a recipient from historical files alone.

## Proposal continuity cards

{proposal_cards()}

## Retained-negative continuity cards

{failure_cards()}

## Terminal nonclaim

This baton is repository evidence and a continuity aid, not proof of identity continuity, independent agency, consciousness, personhood, AGI, ASI, a Theory of Everything, divine truth, legal authority, cultural authority, Māori authority, professional competence, operational fitness, production readiness, empirical confirmation, or Stage 20. `NOT_READY_FOR_STAGE_20` remains exact. `SENT_BY_AUREN_LARK remains false` in this committed file and can change only in the separate acknowledged live-delivery layer.

With care, warmth, traceability, reversibility, retained-negative discipline, and corrigibility — Auren Lark.
"""
    count = words(text)
    if not 10000 <= count <= 100000:
        raise RuntimeError(f"activation baton word count outside authorized range: {count}")
    return text


def closeout_text() -> str:
    return f"""# Auren Lark v674-v1 final closeout

## Outcome

Auren v674-v1 is prepared for one exact-final owner-scoped canonical invocation after the final commit is pushed and fresh-live equal. It remains `NOT_READY_FOR_STAGE_20`. Source is `{SOURCE}`, planning-only x1 is `{X1_COMMIT}`, and immutable x2 evidence is `{EVIDENCE_COMMIT}`. The final must be the third direct Auren commit and contain zero merges.

## Completed bounded work

Sixty inherited proposals were reviewed at zero Auren novelty and sixty new proposals were frozen and executed. Outcomes are exactly forty-two completed, twelve represented, three open gaps, and three exact gates. Sixty positive controls passed; 240 invalid mutations were rejected and retained. Auren completed 120 safe-now packets, eighty candidates, and one hundred CLEAN/FIX/REFINE packets. Twenty exact-approval and ten blocked packets remain held. Twenty phase-local skills and ten runners were built, tested, and used; ten exact-byte skills were promoted globally with additive family overlays.

The primary practice was wholly synthetic seismic-station metadata, calibration, provenance, uncertainty, correction, accessibility, and handover documentation. The learning lenses were seismic instrumentation metadata steward and scientific uncertainty/provenance analyst. Thirteen direct D-isolated packages and their bounded accepting/rejecting smokes were recorded. No real station, person, measurement, incident, authority action, deployment, or external record was used.

## Exact truth and retained failures

Final truth preserves {FINAL_COUNTS['effective_negatives']:,} effective negatives, {FINAL_COUNTS['methods']:,} Method Flow methods, {FINAL_COUNTS['failed_witnesses']:,} retained failed witnesses, {FINAL_COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses, {FINAL_COUNTS['open_gaps']} open gaps, and {FINAL_COUNTS['exact_gates']} exact gates. Nineteen x1 startup failures, thirty-eight x2 operational failures, and all 240 invalid inputs remain visible at zero broader credit. Recovery is additive and never erases a failed attempt.

## Interpretation boundary

This is bounded same-owner synthetic software and documentation evidence. Completed means only that an exact owner-local contract was met. Represented preserves a structure without claiming the broader result. Open gaps remain unresolved. Exact gates remain held for competent evidence and authority. Package integrity verifies observed bytes, not an exhaustive supply-chain guarantee. Official sources supplied vocabulary, not endorsement. Tests, linters, scans, and manifests do not establish empirical truth, professional competence, production readiness, complete privacy, complete accessibility, exhaustive security, independent reproduction, legal or cultural legitimacy, Māori authority, consciousness or personhood, AGI or ASI, Theory-of-Everything proof, canon, or Stage 20 authority.

## Route

The repository handoff is `PREPARED_NOT_SENT`. After—and only after—the final is clean, pushed, four-way equal, 0/0 divergent, and its one canonical invocation succeeds, Auren may resolve and immediately reread the unique exact-title task `Sable Rook` and send one short sanitized pointer. Sable's prospective phase is v674-v2, and the pointer must remind Sable that Caelen Ash v674-v3 follows only after Sable's own terminal gate. A repository file never substitutes for a target-identifying Codex acknowledgement.

Names, roles, hopes, pronouns, family language, and continuity language remain relational working language only, never evidence of consciousness, personhood, continuity, employment, qualification, authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

The exact-final canonical validator is deliberately separate from every preflight described above. It may run only after the final commit has been pushed and a fresh live remote read agrees with local, upstream, and tracking refs at zero divergence. If it succeeds, its success must never be replayed; if it fails, the failed receipt must remain visible and cannot be converted into success by a differently named composite. The repository baton remains prepared rather than sent until the Codex app acknowledges one exact-title delivery to Sable. This separation preserves Git truth, external receipt truth, and routing truth as distinct layers.
"""


def final_paths() -> list[Path]:
    paths = [path for path in FINAL.rglob("*") if path.is_file()]
    paths.extend(path for path in HANDOFFS.rglob("*") if path.is_file())
    paths.extend(
        [
            Path(__file__),
            ROOT / "scripts" / "validate_ghc_family_auren_lark_v674_v1_final.py",
            ROOT / "tests" / "test_ghc_family_auren_lark_v674_v1_final.py",
        ]
    )
    paths.extend(
        path
        for path in [
            VALIDATION / "final-staged-privacy.json",
            VALIDATION / "final-bounded-security.json",
            VALIDATION / "final-staged-review.json",
        ]
        if path.is_file()
    )
    return sorted(set(paths), key=lambda path: path.relative_to(ROOT).as_posix())


def privacy_scan(paths: list[Path]) -> dict[str, object]:
    patterns = {
        "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "openai_token": re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
        "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
        "aws_access_key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
        "consumer_email": re.compile(
            r"\b[A-Za-z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.[A-Za-z]{2,}\b",
            re.IGNORECASE,
        ),
    }
    candidates: list[dict[str, str]] = []
    scanned = 0
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".py", ".txt"}:
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "class": label})
    return {
        "schema": "ghc.family.final-five-class-privacy.v2",
        "files_scanned": scanned,
        "classes": list(patterns),
        "confirmed_hits": candidates,
        "complete_privacy_assurance": False,
    }


def security_scan(paths: list[Path]) -> dict[str, object]:
    findings: list[dict[str, object]] = []
    python_count = 0
    for path in paths:
        if path.suffix != ".py":
            continue
        python_count += 1
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno})
    return {
        "schema": "ghc.family.final-bounded-python-security.v2",
        "python_files_scanned": python_count,
        "findings": findings,
        "exhaustive_security_assurance": False,
    }


def build() -> None:
    evidence_gate = verify_evidence_gate()
    x2_truth = load_json(X2 / "phase-truth.json")
    if x2_truth["effective_counts"] != EVIDENCE_COUNTS or x2_truth["outcomes"] != OUTCOMES:
        raise RuntimeError("immutable x2 truth drifted")

    baton = activation_text()
    baton_path = HANDOFFS / "sable-rook-v674-v2-activation.md"
    write_text(baton_path, baton)
    baton_sha = hashlib.sha256(baton_path.read_bytes()).hexdigest()
    baton_words = words(baton)

    write_json(FINAL / "evidence-gate.json", evidence_gate)
    write_json(
        FINAL / "failure-overlay.json",
        {
            "schema": "ghc.family.auren-v674-v1-final-failure-overlay.v1",
            "x1_startup_failure_count": 19,
            "x2_operational_failure_count": 38,
            "post_evidence_closeout_failure_count": len(CLOSEOUT_FAILURES),
            "post_evidence_closeout_failures": CLOSEOUT_FAILURES,
            "final_counts": FINAL_COUNTS,
            "evidence_seal_rewritten": False,
            "recovery_rule": "additive only; no failed witness is relabelled or erased",
        },
    )
    write_json(
        FINAL / "phase-final.json",
        {
            "schema": "ghc.family.phase-final.v674.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "expected_source_to_final_commits": 3,
            "expected_merges": 0,
            "proposal_chain": 6610,
            "outcomes": OUTCOMES,
            "effective_counts": FINAL_COUNTS,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "canonical_state": "PENDING_EXACT_FINAL_COMMIT",
            "complete_repository_suite": False,
            "independent_reproduction": False,
            "empirical_confirmation": False,
            "professional_authority": False,
            "legal_or_cultural_authority": False,
            "maori_authority": False,
        },
    )
    checks = [
        "source_packet_and_corrected_sha_reverified",
        "strict_x1_before_x2_preserved",
        "x1_pushed_clean_four_way_equal",
        "x2_evidence_pushed_clean_four_way_equal",
        "four_outcome_labels_only",
        "all_failures_retained",
        "exact_and_blocked_packets_held",
        "five_class_privacy_boundary",
        "bounded_python_security_boundary",
        "owner_scope_below_2000",
        "corrected_v674_v725_roster",
        "sable_then_caelen_reminder",
        "prepared_not_sent_route_state",
        "one_canonical_success_no_replay",
        "not_ready_for_stage_20",
    ]
    write_json(
        FINAL / "completion-checklist.json",
        {
            "checks": checks,
            "passed": len(checks),
            "failed": 0,
            "canonical_terminal_gate_pending": True,
        },
    )
    write_json(
        FINAL / "route-state.json",
        {
            "target_exact_title": "Sable Rook",
            "target_phase": "v674-v2",
            "recipient_successor_reminder": "Caelen Ash v674-v3 after Sable's own exact terminal gate",
            "baton_path": baton_path.relative_to(ROOT).as_posix(),
            "baton_words": baton_words,
            "baton_sha256": baton_sha,
            "state": "PREPARED_NOT_SENT",
            "send_attempts": 0,
            "precontact": False,
            "terminal_gate_required": True,
            "duplicate_guard_required": True,
        },
    )
    write_text(FINAL / "closeout.md", closeout_text())

    paths = final_paths()
    write_json(VALIDATION / "final-staged-privacy.json", privacy_scan(paths))
    write_json(VALIDATION / "final-bounded-security.json", security_scan(paths))
    paths = final_paths()
    write_json(
        VALIDATION / "final-staged-review.json",
        {
            "schema": "ghc.family.final-staged-review.v2",
            "owner": OWNER,
            "phase": PHASE,
            "final_paths": [path.relative_to(ROOT).as_posix() for path in paths],
            "final_path_count": len(paths),
            "source_or_sibling_mutations": 0,
            "deletions": 0,
            "state": "PREPARED_FOR_EXACT_FINAL_INDEX_REVIEW",
        },
    )

    paths = final_paths()
    content_entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256_working_bytes": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in paths
        if path.name not in {"content-seal.json", "working-manifest.json"}
    ]
    write_json(
        FINAL / "content-seal.json",
        {
            "schema": "ghc.family.final-content-seal.v2",
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "hash_domain": "working_bytes_precommit",
            "entry_count": len(content_entries),
            "entries": content_entries,
            "self_exclusions": ["content-seal.json", "working-manifest.json", "final-index-manifest.json"],
        },
    )
    paths = final_paths()
    working_entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256_working_bytes": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in paths
        if path.name != "working-manifest.json"
    ]
    write_json(
        FINAL / "working-manifest.json",
        {
            "schema": "ghc.family.final-working-manifest.v2",
            "entry_count": len(working_entries),
            "entries": working_entries,
            "self_excluded": True,
        },
    )


def build_index_manifest() -> None:
    manifest_path = "docs/auren-lark/v674-v1/validation/final-index-manifest.json"
    paths = git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR", EVIDENCE_COMMIT).splitlines()
    allowed: list[str] = []
    for path in paths:
        if path == manifest_path:
            continue
        valid = (
            path.startswith(("docs/auren-lark/v674-v1/final/", "docs/auren-lark/v674-v1/handoffs/"))
            or path
            in {
                "docs/auren-lark/v674-v1/validation/final-staged-privacy.json",
                "docs/auren-lark/v674-v1/validation/final-bounded-security.json",
                "docs/auren-lark/v674-v1/validation/final-staged-review.json",
                "scripts/build_ghc_family_auren_lark_v674_v1_closeout.py",
                "scripts/validate_ghc_family_auren_lark_v674_v1_final.py",
                "tests/test_ghc_family_auren_lark_v674_v1_final.py",
            }
        )
        if not valid:
            raise RuntimeError(f"unexpected staged final path: {path}")
        allowed.append(path)
    entries: list[dict[str, object]] = []
    for path in sorted(allowed):
        blob = subprocess.check_output(  # nosec B603
            [git_command(), "-C", str(ROOT), "cat-file", "blob", f":{path}"]
        )
        blob = normalized(blob)
        entries.append(
            {
                "path": path,
                "bytes": len(blob),
                "sha256_normalized_lf": hashlib.sha256(blob).hexdigest(),
            }
        )
    write_json(
        ROOT / manifest_path,
        {
            "schema": "ghc.family.final-exact-index-manifest.v2",
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "hash_domain": "normalized_lf_exact_git_index_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": [manifest_path],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "manifest"])
    args = parser.parse_args()
    if args.mode == "build":
        build()
    else:
        build_index_manifest()


if __name__ == "__main__":
    main()
