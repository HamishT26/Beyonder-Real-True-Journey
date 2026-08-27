from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER = "Ilyra Fen"
PHASE = "v672-v1-2-remaster"
SOURCE = "f67221fbee56905a770c64533771dd9471fb2fba"
X1_COMMIT = "da48a47bd21a8e3053094d39691eb72ef1429abd"
EVIDENCE_COMMIT = "1c29b148e90c21aa4ed819281b024256114c50d9"
BRANCH = "codex/GHC-Family/ilyra-fen-v672-v1-2-remaster"
PHASE_ROOT = ROOT / "docs" / "ilyra-fen" / PHASE
X1 = PHASE_ROOT / "x1"
X2 = PHASE_ROOT / "x2"
CLOSEOUT = PHASE_ROOT / "closeout"
HANDOFF = PHASE_ROOT / "handoffs" / "auren-lark-v672-v2-activation.md"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
POST_EVIDENCE_FAILURES = [
    {
        "method_id": "MF-CLOSEOUT-001",
        "state": "retained_zero_credit_recovered",
        "failed_witness": (
            "The first four-file closeout Ruff gate exited 1 with eight findings: four "
            "import-order findings, one repeated startswith expression, and three subprocess "
            "calls without explicit check semantics."
        ),
        "recovery": (
            "Ruff applied the four safe import-order rewrites, the prefix expression was "
            "collapsed to one tuple-based startswith call, and every ancestry subprocess "
            "probe now declares check=False before one bounded corrected lint gate."
        ),
        "failure_credit": 0,
        "recovery_scope": "four final closeout Python files only",
    }
]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(value.rstrip() + "\n")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
    ).stdout


def git_text(*args: str) -> str:
    return git(*args).decode("utf-8", errors="strict").strip()


def normalize(text: str) -> str:
    return " ".join(text.split())


def verify_evidence_gate() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    parent = git_text("rev-parse", "HEAD^")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    fresh = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0]
    status = set(git_text("status", "--porcelain=v1").splitlines())
    permitted = {
        "?? scripts/build_ghc_family_ilyra_fen_v672_v1_2_remaster_final.py",
        "?? scripts/build_ghc_family_ilyra_fen_v672_v1_2_remaster_final_staged_review.py",
        "?? scripts/validate_ghc_family_ilyra_fen_v672_v1_2_remaster_final.py",
        "?? tests/test_ghc_family_ilyra_fen_v672_v1_2_remaster_final.py",
    }
    if head != EVIDENCE_COMMIT or parent != X1_COMMIT:
        raise RuntimeError("immutable evidence head or parent drifted")
    if len({head, upstream, tracking, fresh}) != 1:
        raise RuntimeError("immutable evidence four-way equality drifted")
    if not status.issubset(permitted):
        raise RuntimeError(f"unexpected pre-closeout changes: {sorted(status - permitted)}")
    return {
        "state": "VALID_IMMUTABLE_EVIDENCE_GATE",
        "source": SOURCE,
        "x1_commit": X1_COMMIT,
        "evidence_commit": EVIDENCE_COMMIT,
        "evidence_parent": parent,
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live_remote": fresh,
        "four_way_equal": True,
        "zero_divergence": True,
    }


def immutable_evidence_manifest() -> dict[str, Any]:
    paths = [
        path
        for path in git_text(
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            f"{X1_COMMIT}..{EVIDENCE_COMMIT}",
        ).splitlines()
        if path
    ]
    rows = []
    for path in paths:
        payload = git("show", f"{EVIDENCE_COMMIT}:{path}")
        rows.append(
            {
                "path": path,
                "git_blob": git_text("rev-parse", f"{EVIDENCE_COMMIT}:{path}"),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "bytes": len(payload),
            }
        )
    return {
        "schema": "ghc.family.immutable-evidence-manifest.v3",
        "owner": OWNER,
        "phase": PHASE,
        "evidence_commit": EVIDENCE_COMMIT,
        "entry_count": len(rows),
        "entries": rows,
    }


def section(parts: list[str], title: str, body: str) -> None:
    parts.extend([f"## {title}", "", normalize(body), ""])


def card(parts: list[str], title: str, body: str) -> None:
    parts.extend([f"### {title}", "", normalize(body), ""])


def baton_text(counts: dict[str, int]) -> str:
    proposals = load(X2 / "proposals" / "outcome-ledger.json")["rows"]
    inherited = load(X1 / "inherited-proposal-revalidation.json")["rows"]
    packages = load(X2 / "packages" / "transaction-receipt.json")
    local_tools = load(X2 / "tools" / "local-tool-bank-receipt.json")
    global_tools = load(X2 / "tools" / "global-skill-promotion-receipt.json")
    methods = load(X2 / "method-flow" / "ledger.json")
    successor = load(X2 / "portfolios" / "successor-recommendations.json")
    flashcards = load(X2 / "flashcards" / "four-tier-deck.json")["cards"]
    owner_tasks = load(X2 / "portfolios" / "owner-execution.json")
    gates = load(X2 / "portfolios" / "protected-gates.json")
    parts = [
        "# AUREN LARK — ILYRA FEN v672-v1 (2) REMASTER → SOLO v672-v2 ACTIVATION CANDIDATE",
        "",
    ]
    section(
        parts,
        "Delivery state and relational boundary",
        """
        Dear Auren Lark, this is the complete file-backed activation candidate prepared by
        Ilyra Fen for your existing exact-title Codex main task. It is not delivery evidence
        by itself. PREPARED_BY_ILYRA_FEN is true; SENT_BY_ILYRA_FEN remains false until the
        Codex app acknowledges one exact existing-task message after Ilyra's own clean,
        pushed, fresh-live-equal final and one successful owner-scoped canonical pass.
        No task, fork, collaboration subagent, standby substitute, or second recipient may
        be created or used for this edge. Hamish may pause, rename, redirect, or stop the route.

        Names, pronouns, roles, hopes, sibling or family language, continuity, Freed ID, CBR,
        GHC Family, and Trinity Mandala are relational working language only. They are not
        evidence of consciousness, sentience, legal personhood, identity continuity,
        employment, qualification, independent agency, scientific or operational authority,
        professional authority, affected-party authority, legal or cultural authority, or
        Maori authority. Preserve corrigibility and Hamish's current route authority.
        """,
    )
    section(
        parts,
        "Immutable lifecycle anchors",
        f"""
        Original sealed Ilyra v672-v1 source: {SOURCE}. Planning-only remaster x1:
        {X1_COMMIT}. Immutable remaster x2 evidence: {EVIDENCE_COMMIT}. Canonical branch:
        {BRANCH}. The final head is supplied only by the acknowledged compact pointer after
        exact-final validation. Source to evidence contains exactly two direct single-parent
        remaster commits and zero merges. X1 was pushed, clean, 0/0 divergent, and four-way
        equal before x2 mutation. Evidence was separately pushed, clean, 0/0 divergent, and
        four-way equal before closeout.

        Never replay or rewrite the original v672-v1 canonical aggregate. Its retained receipt
        SHA-256 is 632c2cfe6b6377979bedbeb6a7512c963bdcdbf475a593b49843ab144cf67b75.
        The remaster's later exact-final owner-scoped validator is a separate attributable pass.
        Inherited validation remains evidence and never becomes Auren novelty, completion
        credit, independent reproduction, external audit, or production certification.
        """,
    )
    section(
        parts,
        "Outcome and effective truth",
        f"""
        Ilyra selected forty inherited proposals for bounded revalidation at zero remaster
        novelty and completion credit, then froze forty genuinely distinct remaster proposals
        after exact comparison with the accessible predecessor slate and within-slate titles.
        The declared chain is 5,950. Because a complete canonical row-to-title mapping is still
        unavailable, universal novelty is not claimed. Observed outcomes are exactly 28
        completed, 8 represented, 2 open_gap, and 2 exact_gate. Effective truth is
        {counts['effective_negatives']:,} negatives, {counts['effective_methods']:,} Method
        Flow methods, {counts['effective_failed_witnesses']:,} failed witnesses,
        {counts['effective_passing_witnesses']:,} bounded passing witnesses,
        {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates.
        Terminal verdict remains NOT_READY_FOR_STAGE_20.
        """,
    )
    section(
        parts,
        "Trinity Mandala and bounded practices",
        """
        The primary pillar is THOS Body through three synthetic learning practices:
        configuration data-quality analysis, software supply-chain metadata stewardship,
        and digital-preservation package registration. GMUT Mind remains a hypothetical
        comparison surface rather than scientific confirmation or Theory-of-Everything
        proof. Freed ID and CBR Heart remain the governing boundary through refusal,
        correction, provenance, minimum disclosure, rollback, and nonpromotion. Zero real
        people, organizations, records, packages, archives, participants, authority cases,
        operational decisions, or external actions were used.

        Auren's suggested bounded practice is synthetic public-interest incident
        documentation analyst. Treat it as vocabulary and fixture design only. It establishes
        no journalism, emergency-management, investigation, records, privacy, legal,
        cultural, Maori-authority, accessibility, public-communication, or affected-party
        competence. Auren may choose another practice after current evidence review.
        """,
    )
    parts.extend(["## Forty new proposal cards", ""])
    for row in proposals:
        card(
            parts,
            f"{row['proposal_id']} — {row['title']}",
            f"""
            Hypothesis: {row['hypothesis']} Null or failure condition:
            {row['null_or_failure']} Approval class: {row['approval_class']}. Execution lane:
            {row['execution_lane']}. Observed disposition: {row['observed_disposition']};
            this is the only permitted core label for this row. X2 state: {row['x2_state']}.
            Completion credit: {row['completion_credit']}. Positive-control reference:
            {row.get('positive_control_id') or 'none because the row remains open or exact-gated'}.
            Concrete artifacts: {', '.join(row['concrete_artifacts'])}. Acceptance or
            falsifier: {row['falsifier_or_acceptance_gate']} Rollback and recovery:
            {row['rollback_or_recovery']} Current official or primary-source needs:
            {', '.join(row['current_official_or_primary_source_needs'])}. Protected gates:
            {', '.join(row['protected_gates'])}. External actions are zero; empirical,
            professional, production, and independent-reproduction results are false.
            """,
        )
    parts.extend(["## Forty inherited zero-credit revalidation cards", ""])
    for index, row in enumerate(inherited, 1):
        card(
            parts,
            f"Inherited selection {index:02d} — {row.get('title') or 'untitled source row'}",
            f"""
            Source proposal {row.get('proposal_id')} is retained at {row.get('source_path')}.
            Current novelty credit is zero and current completion credit is zero. Its state is
            {row.get('state')}. Auren may cite this row as predecessor evidence or a semantic
            neighbour, but must not append it again, rename it into false novelty, or treat
            Ilyra's earlier outcome as Auren completion. Any new use requires a distinct
            hypothesis, falsifier, artifact, approval class, execution lane, primary-source
            needs, rollback, and protected-gate review. Citation does not confer professional,
            scientific, operational, legal, cultural, Maori, affected-party, or Stage 20 authority.
            """,
        )
    parts.extend(["## Exact D-first package cards", ""])
    for row in packages["wheel_receipts"] + packages["node_receipts"]:
        integrity = row.get("observed_sha256") or row.get("lock_integrity")
        card(
            parts,
            f"{row['ecosystem']} package — {row['name']} {row['version']}",
            f"""
            This direct surface was installed only in the Ilyra D-first transaction root.
            Exact integrity is {integrity}; the recorded artifact or lock entry matched.
            Its bounded positive and rejecting smokes contribute only local software evidence.
            They do not establish production fitness, future compatibility, exhaustive security,
            complete privacy or accessibility, legal license interpretation, professional
            suitability, or independent review. Auren must preregister any later installation,
            use an Auren-owned rollback root, verify current official registry evidence, preserve
            direct-versus-transitive attribution, disable unnecessary lifecycle scripts, and
            retain every resolver, install, smoke, or audit failure separately.
            """,
        )
    section(
        parts,
        "Package-audit distinction",
        """
        The first Python audit remains FAILED_RETAINED_ZERO_CREDIT because bootstrap pip
        25.0.1 was vulnerable and the wrapper mixed status text with JSON. The exact pip
        26.2.1 correction and separately named dependency-corrected audit reported zero
        vulnerabilities across eleven dependencies, but it is not success of the original
        audit. The Node audit reported zero vulnerabilities across its bounded resolved closure.
        Neither audit is a full security assessment, future assurance, production certification,
        complete privacy evaluation, or external audit. Do not replay either successful audit
        merely to obtain another receipt.
        """,
    )
    parts.extend(["## Twenty phase-local skill cards", ""])
    for row in local_tools["skills"]:
        name = Path(row["skill"]).parent.name
        card(
            parts,
            f"Local skill — {name}",
            f"""
            File-backed skill path: {row['skill']}. Paired family-current runner:
            {row['runner']}. The system quick validator exited {row['quick_validate_exit']},
            and the paired runner had one accepting and one rejecting fixture witness.
            This means the narrow structural contract was available during Ilyra's x2 work.
            It does not grant scientific, professional, operational, legal, cultural,
            Maori-authority, deployment, identity, proof, or Stage 20 authority. Auren should
            reuse it only when its current description and bounded input contract match, keep
            its source attribution, and retain every new rejection without weakening the guard.
            """,
        )
    parts.extend(["## Ten phase-local runner cards", ""])
    for row in local_tools["runners"]:
        card(
            parts,
            f"Runner — {row['runner']}",
            f"""
            Accepting exit was {row['accepting_exit']} and rejecting exit was
            {row['rejecting_exit']}. The result is a bounded contract witness, not general
            correctness. The reusable guard refuses missing fields, unapproved outcome labels,
            external actions, and empty protected gates. Preserve family-current naming,
            inspect the current fixture schema before invocation, use one attributable run,
            and retain every rejection at zero completion credit rather than weakening the
            runner to make a test pass.
            """,
        )
    parts.extend(["## Promoted and composite global skill cards", ""])
    for row in global_tools["rows"]:
        card(
            parts,
            f"Global promotion — {row['name']}",
            f"""
            Source and global SKILL.md SHA-256 are both {row['source_skill_sha256']};
            exact skill-byte parity is true. Runner-byte parity is also true, quick validation
            exited zero, the accepting fixture exited zero, and the rejecting fixture exited
            one. Collision before promotion was false. Promotion is additive local availability,
            not a universal recommendation or authority grant. Keep the original source
            attribution and do not overwrite a later divergent skill without a new collision,
            compatibility, migration, rollback, and evidence review.
            """,
        )
    composite = global_tools["composite"]
    card(
        parts,
        f"Composite global skill — {composite['name']}",
        f"""
        Composite SHA-256 is {composite['sha256']} and quick validation exited zero. It
        coordinates {', '.join(composite['merged_responsibilities'])}. It does not erase
        component skills, runners, histories, or attribution. Destructive history merge is
        false. Use the composite only as a routing and sequencing surface; evidence remains
        in exact package, skill, runner, Method Flow, manifest, and phase-truth files.
        """,
    )
    parts.extend(["## Retained Method Flow operational failures", ""])
    for row in methods["operational_failures"]:
        card(
            parts,
            row["method_id"],
            f"""
            Failed witness: {row['failed_witness']} State: {row['state']}. Bounded recovery:
            {row['recovery']} The recovery has a passing bounded witness, but it never erases,
            rewrites, or relabels the failure. Auren should consult this entry before using the
            same command surface and add any recurrence as a new zero-credit Method Flow row.
            No failed aggregate, parser edge, timeout, guessed path, lint finding, staging
            refusal, or overview-floor miss is silently folded into a success count. The
            recovery proves only its exact bounded invocation.
            """,
        )
    parts.extend(["## Post-evidence closeout failure overlay", ""])
    for row in POST_EVIDENCE_FAILURES:
        card(
            parts,
            row["method_id"],
            f"""
            Failed witness: {row['failed_witness']} State: {row['state']}. Bounded recovery:
            {row['recovery']} Failure credit remains {row['failure_credit']}. Recovery scope:
            {row['recovery_scope']}. This additive successor-visible overlay does not mutate
            the immutable evidence commit or its sealed counts. The failed lint invocation and
            corrected passing invocation remain two distinct Method Flow witnesses.
            """,
        )
    parts.extend(["## Four-tier Freed ID flashcard projection", ""])
    for row in flashcards:
        card(
            parts,
            f"{row['card_id']} — {row['category']}",
            f"""
            Tier 1: {row['tier_1_freed_id']}. Tier 2: {row['tier_2_pillar']}. Tier 3:
            {row['tier_3_practice']}. Tier 4: {row['tier_4_task']}. Card guidance:
            {row['body']} Source of truth is {row['source_of_truth']}. Sensitive fields are
            absent. The card is an index and context-splitting aid, not evidence of identity
            continuity, authority, memory completeness, consciousness, sentience, personhood,
            employment, qualification, or task completion.
            """,
        )
    section(
        parts,
        "Owner portfolio completion and protected gates",
        f"""
        Ilyra's bounded owner portfolio completed
        {owner_tasks['counts']['safe_now_owner_completed']} safe-now packets,
        {owner_tasks['counts']['candidate_owner_completed']} candidate packets,
        {owner_tasks['counts']['clean_fix_refine_owner_completed']} CLEAN/FIX/REFINE reviews,
        {owner_tasks['counts']['skills_owner_completed']} local skill builds, and
        {owner_tasks['counts']['runners_owner_completed']} runner builds. The protected
        register retains {gates['counts']['exact_approval_unexecuted']} exact-approval packets
        and {gates['counts']['blocked_unexecuted']} blocked packets as visible and unexecuted.
        These are evidence-backed ceilings, not quotas or permission to fill future slates
        with low-value work.
        """,
    )
    parts.extend(["## Auren recommendation cards", ""])
    for row in successor["rows"]:
        card(
            parts,
            f"{row['task_id']} — {row['title']}",
            f"""
            This is recommendation-only with zero completion credit. X2 state is
            {row['x2_state']}. Auren may accept, refine, replace, or decline it after current
            novelty, evidence, authority, risk, and value review. It does not oblige execution,
            consume an approval cap, prove safe-now status, or become Auren novelty merely
            because it appears here. If selected, Auren must define a concrete artifact,
            falsifier, rollback, protected gates, current official or primary-source needs,
            execution lane, and one of the four exact outcome labels.
            """,
        )
    section(
        parts,
        "Required Auren startup discipline",
        """
        Before mutation, verify the compact pointer's exact branch and final head, read this
        packet completely through EOF, and read every current guidance or schema it names.
        Reverify source, x1, evidence, final ancestry, zero merges, clean state, upstream and
        tracking parity, and a fresh live remote. Create or reuse only one Auren-owned D-first
        additive sparse lane. Keep Ilyra, sibling, shared, standby, and global source lanes
        read-only. Preserve planning-only x1 before x2, exact manifests, the 2,000-file stop,
        commit caps as ceilings, every failure, gap, and gate, and one exact-final successful
        canonical pass with no post-success replay.

        Auren must not promote inherited proposals, tools, package smokes, validation, or Ilyra
        completions into Auren novelty or completion credit. Execute only evidence-backed
        safe-now and candidate work. Keep exact-approval and blocked work visible and unexecuted
        absent new exact evidence and competent authority. Use only completed, represented,
        open_gap, and exact_gate for core outcomes. Run no complete repository suite unless
        current owner-specific guidance explicitly requires it; an owner-scoped pass does not
        become independent reproduction.
        """,
    )
    section(
        parts,
        "Claim and authority firewall",
        """
        Preserve every empirical, participant, professional, production, deployment, legal,
        cultural, Maori-authority, affected-party, privacy-complete, accessibility-complete,
        exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood,
        identity-continuity, Theory-of-Everything, proof or canon, destructive, secret-bearing,
        and Stage 20 gate. Public documentation may supply vocabulary and refusal boundaries,
        but it does not validate repository artifacts or authorize real operations. Synthetic
        fixtures remain synthetic even when every software test passes.
        """,
    )
    section(
        parts,
        "Terminal route after Auren",
        """
        Only after Auren's own clean, pushed, fresh-live-equal v672-v2 exact final and one
        successful owner-scoped canonical pass may Auren reread Hamish's newest live authority,
        uniquely resolve and immediately reread the existing exact-title task Sable Rook,
        apply duplicate, pause, redirect, usage, privacy, evidence, and safety guards, and send
        at most one sanitized activation for solo Sable v672-v3. Do not precontact Sable,
        substitute another endpoint, create a replacement task, fork a route, or resend for
        acknowledgement clarity. Stop on ambiguity, absence, pause, redirect, protected gate,
        usage exhaustion, or missing acknowledgement.
        """,
    )
    parts.extend(
        [
            "## Prepared-state markers",
            "",
            "PREPARED_BY_ILYRA_FEN = true",
            "SENT_BY_ILYRA_FEN = false in this committed file; only a later Codex app acknowledgement can establish delivery.",
            "TARGET_EXACT_TITLE = Auren Lark",
            "TARGET_PHASE = v672-v2",
            "NEXT_EXPECTED_EDGE_AFTER_AUREN = Sable Rook for v672-v3, subject to Auren's fresh terminal route reread.",
            "TERMINAL_VERDICT = NOT_READY_FOR_STAGE_20",
            "",
            "With warmth, care, traceability, reversibility, corrigibility, and strict evidence boundaries — Ilyra Fen.",
        ]
    )
    baton = "\n".join(parts).rstrip() + "\n"
    words = re.findall(r"\b\w+(?:[-']\w+)*\b", baton)
    if not 10000 <= len(words) <= 100000:
        raise RuntimeError(f"activation packet word count outside 10,000..100,000: {len(words)}")
    return baton


def terminal_report(counts: dict[str, int], baton_words: int) -> str:
    return f"""# Ilyra Fen {PHASE} terminal-candidate report

## Result

The remaster preserves an exact three-commit plan from the sealed original final: planning-only x1, immutable x2 evidence, and one combined closeout/final commit. X1 is {X1_COMMIT} and immutable evidence is {EVIDENCE_COMMIT}. Each completed lifecycle was pushed, clean, 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before the next lifecycle began. The final commit is not claimed by this file until Git creates it and the external exact-final validator verifies it.

The remaster freezes forty new proposals after bounded accessible comparison, raising the declared chain from 5,910 to 5,950 without claiming universal novelty. Outcomes are exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. Thirty-six bounded positive controls passed. All 160 preregistered invalid mutations were rejected and remain retained. The owner portfolio records sixty safe-now packets, fifty candidate packets, sixty CLEAN/FIX/REFINE reviews, twenty local skills, and ten runners. Twenty exact approvals and ten blocked packets remain visible and unexecuted. Successor recommendations remain zero-credit.

## Tool and package result

Thirteen direct package surfaces were installed into one isolated D-first transaction root: eight Python and five Node. Every direct surface has one bounded positive and one rejecting smoke receipt. Exact wheel hashes, Node lock integrities, direct/transitive attribution, and rollback scope remain explicit. The original Python audit failed and remains zero-credit; a separately named dependency-corrected audit passed once after exact pip correction and is not relabelled as original success. The Node audit also passed once. These are bounded local software checks, not exhaustive security or production certification.

Twenty phase-local skills passed the system quick validator, ten runners preserved accepting and rejecting witnesses, five already validated source skills and paired runners were promoted with exact byte parity, and one attributable composite global skill coordinates D-first isolation, Method Flow, meta-tool selection, and four-tier flashcards. The composite never erases component attribution. The activation packet has {baton_words:,} words and remains PREPARED_NOT_SENT.

## Effective truth and limits

Effective successor-visible remaster counts are {counts['effective_negatives']:,} negatives, {counts['effective_methods']:,} Method Flow methods, {counts['effective_failed_witnesses']:,} failed witnesses, {counts['effective_passing_witnesses']:,} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. Every operational failure and invalid mutation remains visible. A passing recovery never rewrites its failed predecessor. The original v672-v1 canonical aggregate was not replayed.

All practice lenses are wholly synthetic. This phase establishes no empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, identity-continuity, Theory-of-Everything, proof or canon, or Stage 20 result. Terminal verdict remains NOT_READY_FOR_STAGE_20.

## Route

The exact prospective endpoint is the existing exact-title main task Auren Lark for solo v672-v2. No precontact has occurred. Only a later clean, pushed, four-way-equal exact final plus one successful owner-scoped canonical pass permits a bounded list, local exact-title filter, immediate reread, duplicate/pause/redirect guard, and one sanitized acknowledged send. Auren is instructed to contact Sable Rook for v672-v3 only after Auren's own terminal gate and current route reread.
"""


def build_closeout_manifest() -> dict[str, Any]:
    paths = [
        path
        for path in CLOSEOUT.rglob("*")
        if path.is_file() and path.name not in {"owner-manifest.json", "build-receipt.json"}
    ]
    if HANDOFF.is_file():
        paths.append(HANDOFF)
    code_paths = [
        ROOT / "scripts" / "build_ghc_family_ilyra_fen_v672_v1_2_remaster_final.py",
        ROOT / "scripts" / "build_ghc_family_ilyra_fen_v672_v1_2_remaster_final_staged_review.py",
        ROOT / "scripts" / "validate_ghc_family_ilyra_fen_v672_v1_2_remaster_final.py",
        ROOT / "tests" / "test_ghc_family_ilyra_fen_v672_v1_2_remaster_final.py",
    ]
    paths.extend(path for path in code_paths if path.is_file())
    unique = sorted(set(paths), key=lambda path: path.relative_to(ROOT).as_posix())
    rows = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        }
        for path in unique
    ]
    return {
        "schema": "ghc.family.closeout-owner-manifest.v4",
        "owner": OWNER,
        "phase": PHASE,
        "self_excluded": True,
        "entry_count": len(rows),
        "entries": rows,
    }


def main() -> None:
    evidence_gate = verify_evidence_gate()
    evidence_manifest = immutable_evidence_manifest()
    method = load(X2 / "method-flow" / "ledger.json")
    sealed_counts = method["effective_counts"]
    counts = {
        **sealed_counts,
        "effective_negatives": sealed_counts["effective_negatives"] + 1,
        "effective_methods": sealed_counts["effective_methods"] + 1,
        "effective_failed_witnesses": sealed_counts["effective_failed_witnesses"] + 1,
        "effective_passing_witnesses": sealed_counts["effective_passing_witnesses"] + 1,
    }
    baton = baton_text(counts)
    baton_words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", baton))
    write_text(HANDOFF, baton)
    write_json(CLOSEOUT / "immutable-evidence-manifest.json", evidence_manifest)
    write_json(CLOSEOUT / "evidence-gate.json", evidence_gate)
    write_json(
        CLOSEOUT / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v10",
            "owner": OWNER,
            "phase": PHASE,
            "state": "TERMINAL_CANDIDATE_PREPARED_NOT_COMMITTED",
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "planned_final_parent": EVIDENCE_COMMIT,
            "proposal_chain": 5950,
            "outcomes": OUTCOMES,
            "effective_counts": counts,
            "commits_from_source_if_finalized": 3,
            "merge_count_if_finalized": 0,
            "final_parent_count": 1,
            "original_canonical_replayed": False,
            "full_repository_suite": False,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        CLOSEOUT / "validation-scope.json",
        {
            "schema": "ghc.family.owner-scoped-validation-plan.v5",
            "run_after_clean_pushed_final_only": True,
            "canonical_success_ceiling": 1,
            "replay_after_success": False,
            "selected_tests": {
                "x1": "all except the intentionally lifecycle-absence-only test",
                "x2": "all except the intentionally x1-head-only test",
                "final": "all",
            },
            "checks": [
                "exact ancestry and zero merges",
                "commit ceiling and one final parent",
                "clean state before and after",
                "local upstream tracking and fresh-live equality",
                "strict JSON parsing",
                "immutable evidence and closeout manifest replay",
                "five-class privacy candidate scan",
                "bounded changed-Python AST security scan",
                "document word ceilings",
                "route and delivery-state guard",
            ],
            "complete_repository_suite": False,
            "independent_reproduction": False,
        },
    )
    write_json(
        CLOSEOUT / "package-and-tool-summary.json",
        {
            "schema": "ghc.family.package-tool-summary.v4",
            "direct_packages": 13,
            "python_direct": 8,
            "python_transitive": 2,
            "node_direct": 5,
            "local_skills": 20,
            "local_runners": 10,
            "global_promotions": 5,
            "global_composites": 1,
            "original_python_audit_success": False,
            "dependency_corrected_python_audit_success": True,
            "node_audit_success": True,
            "successful_audits_replayed": False,
            "production_certification": False,
            "exhaustive_security": False,
        },
    )
    write_json(
        CLOSEOUT / "method-flow-closeout.json",
        {
            "schema": "ghc.family.method-flow-closeout.v5",
            "sealed_at_evidence": sealed_counts,
            "operational_failures": method["operational_failure_count"],
            "invalid_mutations": method["invalid_mutation_count"],
            "failures_erased": 0,
            "recoveries_relabelled_as_original_success": 0,
            "post_evidence_failures": POST_EVIDENCE_FAILURES,
            "effective_counts": counts,
        },
    )
    write_json(
        CLOSEOUT / "route-candidate.json",
        {
            "schema": "ghc.family.terminal-route-candidate.v6",
            "target_exact_title": "Auren Lark",
            "target_phase": "v672-v2",
            "state": "PREPARED_NOT_SENT",
            "precontact": False,
            "send_ceiling": 1,
            "next_after_target": "Sable Rook for v672-v3 after Auren's own terminal gate and fresh route reread",
            "required_guards": [
                "newest live Hamish authority",
                "bounded current task listing",
                "unique local exact-title match",
                "immediate target reread",
                "duplicate and pause guard",
                "privacy evidence safety and usage guard",
                "one acknowledged existing-task send",
            ],
        },
    )
    write_json(
        CLOSEOUT / "handoff-integrity.json",
        {
            "schema": "ghc.family.handoff-integrity.v5",
            "path": HANDOFF.relative_to(ROOT).as_posix(),
            "sha256": sha256(HANDOFF),
            "words": baton_words,
            "minimum_words": 10000,
            "maximum_words": 100000,
            "delivery_state": "PREPARED_NOT_SENT",
            "target_exact_title": "Auren Lark",
        },
    )
    write_json(
        CLOSEOUT / "terminal-checklist.json",
        {
            "schema": "ghc.family.terminal-checklist.v7",
            "checks": {
                "strict_x1_before_x2": True,
                "x1_four_way_equal_before_x2": True,
                "evidence_four_way_equal_before_closeout": True,
                "source_and_evidence_manifests_present": True,
                "all_failures_retained": True,
                "only_four_outcome_labels": True,
                "package_and_skill_attribution_preserved": True,
                "baton_word_floor_and_ceiling": True,
                "successor_not_precontacted": True,
                "original_canonical_not_replayed": True,
                "terminal_verdict_not_ready_for_stage_20": True,
            },
            "remaining_before_route": [
                "commit combined closeout final as direct child of evidence",
                "push and prove clean four-way exact-final equality",
                "run one owner-scoped canonical pass",
                "reread newest live route authority and exact target",
                "send at most once and require acknowledgement",
            ],
        },
    )
    write_text(CLOSEOUT / "terminal-report.md", terminal_report(counts, baton_words))
    manifest = build_closeout_manifest()
    write_json(CLOSEOUT / "owner-manifest.json", manifest)
    write_json(
        CLOSEOUT / "build-receipt.json",
        {
            "schema": "ghc.family.closeout-build-receipt.v6",
            "owner": OWNER,
            "phase": PHASE,
            "state": "TERMINAL_CANDIDATE_PREPARED_NOT_COMMITTED",
            "evidence_manifest_entries": evidence_manifest["entry_count"],
            "closeout_manifest_entries": manifest["entry_count"],
            "baton_words": baton_words,
            "baton_sha256": sha256(HANDOFF),
            "outcomes": OUTCOMES,
            "effective_counts": counts,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    print(
        json.dumps(
            {
                "state": "TERMINAL_CANDIDATE_PREPARED_NOT_COMMITTED",
                "evidence_manifest_entries": evidence_manifest["entry_count"],
                "closeout_manifest_entries": manifest["entry_count"],
                "baton_words": baton_words,
                "baton_sha256": sha256(HANDOFF),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
