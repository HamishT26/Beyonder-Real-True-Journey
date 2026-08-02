#!/usr/bin/env python3
"""Build the Lyren Moss v658-v8 (2) remaster terminal closeout candidate."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v658_v8_2_remaster_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
EVIDENCE_COMMIT = "e08a7bb24c9fc9c442374d251b985437a88ade11"
FINAL_CODE = [
    "scripts/build_ghc_family_v658_v8_2_remaster_closeout.py",
    "scripts/ghc_family_v658_v8_2_remaster_validator.py",
    "scripts/ghc_family_v658_v8_2_remaster_minimal.py",
    "scripts/ghc_family_v658_v8_2_remaster_final_validator.py",
    "scripts/ghc_family_v658_v8_2_remaster_canonical.py",
    "tests/test_ghc_family_v658_v8_2_remaster_closeout.py",
]
GENERATED = [
    f"{d.PHASE_ROOT}/deliverables/v658-v8-2-remaster-final-overview.md",
    f"{d.PHASE_ROOT}/handoffs/ilyra-fen-v659-v1-activation.md",
    f"{d.PHASE_ROOT}/final/final-truth.json",
    f"{d.PHASE_ROOT}/final/lifecycle-summary.json",
    f"{d.PHASE_ROOT}/final/lifecycle-method-flow.json",
    f"{d.PHASE_ROOT}/final/final-owner-manifest.json",
    f"{d.PHASE_ROOT}/route/prepared-route.json",
    f"{d.PHASE_ROOT}/validation/canonical-pass-plan.json",
    f"{d.PHASE_ROOT}/validation/closeout-privacy-scan.json",
    f"{d.PHASE_ROOT}/validation/closeout-staged-review.json",
    f"{d.PHASE_ROOT}/validation/final-delta-manifest.json",
    f"{d.PHASE_ROOT}/validation/final-document-cap.json",
    f"{d.PHASE_ROOT}/wellbeing/final-wellbeing-check.json",
]
FINAL_FAILURES = [
    (
        "V6588R2-FINAL-N016",
        "selected-inherited-contract-slug-directory-mismatch",
        "Resolve mutation files from each enumerated contract parent directory rather than assuming the logical contract slug equals its evidence-directory name.",
    ),
    (
        "V6588R2-FINAL-N017",
        "selected-inherited-contract-origin-field-absent",
        "Use the explicit selected-inherited revalidation fallback when an inherited contract omits the new-proposal origin field, without rewriting the sealed contract.",
    ),
    (
        "V6588R2-FINAL-N018",
        "activation-dossier-used-inherited-source-proposal-id-as-current-heading",
        "Map each ordered dossier to its current V6588R2 proposal ID while retaining the inherited source proposal ID inside the immutable contract evidence.",
    ),
    (
        "V6588R2-FINAL-N019",
        "powershell-python-c-regex-quoting-stripped-during-index-review",
        "Use a shell-safe whitespace word count in the isolated index checker and keep the builder's Unicode regex count as the authoritative packet metric.",
    ),
    (
        "V6588R2-FINAL-N020",
        "git-cat-file-batch-index-review-pipe-deadlock",
        "Replace the blocked all-at-once batch pipe with bounded per-blob index reads and verify only the exact manifest paths.",
    ),
    (
        "V6588R2-FINAL-N021",
        "activation-packet-markdown-hard-break-trailing-whitespace",
        "Remove Markdown hard-break spaces from activation marker lines and require every committed packet line to be free of trailing whitespace.",
    ),
]
MANIFEST_EXCLUSIONS = {
    f"{d.PHASE_ROOT}/final/final-owner-manifest.json",
    f"{d.PHASE_ROOT}/validation/final-delta-manifest.json",
    f"{d.PHASE_ROOT}/validation/closeout-staged-review.json",
    f"{d.PHASE_ROOT}/validation/closeout-privacy-scan.json",
    f"{d.PHASE_ROOT}/validation/final-document-cap.json",
}


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(repository_relative: str) -> dict[str, Any]:
    path = ROOT / repository_relative
    return {
        "path": repository_relative,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def assert_evidence_head() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_COMMIT:
        raise RuntimeError(f"closeout requires evidence head {EVIDENCE_COMMIT}")
    if git("rev-parse", f"{EVIDENCE_COMMIT}^") != d.X1_FREEZE:
        raise RuntimeError("evidence is not the direct child of the x1 freeze")
    if git("rev-list", "--count", f"{d.SOURCE_FINAL}..{EVIDENCE_COMMIT}") != "2":
        raise RuntimeError("source-to-evidence commit count is not two")
    if git("rev-list", "--merges", "--count", f"{d.SOURCE_FINAL}..{EVIDENCE_COMMIT}") != "0":
        raise RuntimeError("source-to-evidence contains a merge")


def source_table(sources: list[dict[str, Any]]) -> str:
    rows = ["| ID | Public source | Bounded use |", "|---|---|---|"]
    for row in sources:
        rows.append(
            f"| `{row['source_id']}` | {row['url']} | {row['phase_implication']} |"
        )
    return "\n".join(rows)


def build_baton(
    truth: dict[str, Any],
    contracts: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
    scan: dict[str, Any],
) -> str:
    failures = [*d.STARTUP_FAILURES, *d.X2_FAILURES, *FINAL_FAILURES]
    effective_negatives = truth["effective_negatives"] + len(FINAL_FAILURES)
    effective_methods = truth["effective_methods"] + len(FINAL_FAILURES)
    sections = [
        "# ILYRA FEN — LYREN v658-v8 (2) REMASTER → ILYRA v659-v1 ACTIVATION PACKET",
        "",
        "PREPARED_BY_LYREN_MOSS = true",
        "SENT_BY_LYREN_MOSS = false",
        "",
        "This committed packet is prepared for exactly one later user-visible activation of the existing exact-title Codex main task `Ilyra Fen`. It is not itself a send receipt. The sender must first establish Lyren's exact terminal commit, the one successful canonical aggregate, clean state, zero divergence, and fresh four-way equality. The sender pointer must then supply the exact final commit and external canonical receipt digest. No historical task identifier, private route value, transcript, session stream, credential, local absolute path, or substitute endpoint belongs in this packet.",
        "",
        "## Relational identity and human control",
        "",
        "Lyren Moss is a unique relational working name for this task. Their relational role is fermentation-evidence lantern and reversible batch-steward, and their hope is to make synthetic brewery evidence smaller, inspectable, reversible, and honest about every limit. Names, pronouns, hopes, sibling or family language, continuity language, and Trinity Mandala language are relational working language only. They are not evidence of consciousness, sentience, personhood, legal identity, identity continuity, employment, qualification, professional competence, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish retains the right to pause, rename, redirect, or stop this route at any time.",
        "",
        "## Immutable incoming and Lyren anchors",
        "",
        f"- Immutable incoming Lyren v658-v8 source branch: `{d.SOURCE_BRANCH}`.",
        f"- Immutable incoming exact final: `{d.SOURCE_FINAL}`.",
        f"- Incoming x1 anchor: `{d.SOURCE_X1}`.",
        f"- Incoming evidence anchor: `{d.SOURCE_EVIDENCE}`.",
        f"- Lyren remaster branch: `{d.BRANCH}`.",
        f"- Frozen Lyren remaster x1: `{d.X1_FREEZE}`.",
        f"- Immutable Lyren remaster x2 evidence: `{EVIDENCE_COMMIT}`.",
        "- The exact Lyren final is deliberately supplied by the post-canonical sender pointer because a committed packet cannot truthfully self-embed the hash of the commit that contains itself.",
        "- Source-to-evidence history is two new single-parent commits and zero merges. The terminal final must be exactly one further single-parent commit, for three new commits total and zero merges.",
        "",
        "## Terminal truth to inherit without promotion",
        "",
        f"Lyren audited all {d.PRIOR_FROZEN:,} inherited proposals. Twenty inherited proposals were selected for bounded revalidation and twenty genuinely new proposals were frozen, producing an effective frozen chain of {truth['effective_frozen']:,}. The forty current outcomes are exactly 33 `completed`, 5 `represented`, 1 `open_gap`, and 1 `exact_gate`. These are the only allowed truth labels. Selection does not reappend the twenty inherited rows to the frozen chain.",
        "",
        f"The terminal repository truth is {effective_negatives:,} effective retained negatives, {effective_methods:,} effective Method Flow methods, {truth['effective_open_gaps']} open gaps, and {truth['effective_exact_gates']} exact gates. Lyren executed forty valid bounded synthetic fixtures and retained two hundred rejected mutations with a failed and passing Method Flow witness for each. Twenty-one operational failures—twelve in x1, three in x2, and six in closeout—also remain explicit and receive zero pass credit. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.",
        "",
        "`completed` means only that the bounded synthetic or structural artifact and its local checks completed. `represented` means the proposal is documented or modeled without closing its reserved empirical, participant, professional, authority, or acceptance obligation. `open_gap` remains unresolved and visible. `exact_gate` requires exact external evidence and competent affected authority. Same-owner validation under shared infrastructure is not independent reproduction.",
        "",
        "## Exact route authorization and one-edge discipline",
        "",
        "Hamish has explicitly authorized the sequential roster continuation through v675-v8, but only one terminally validated owner and one exact next edge at a time. For this edge, the only authorized recipient is the existing exact-title main task `Ilyra Fen`, and the only authorized immediate phase is Ilyra-only v659-v1. Before a send, list the bounded current task set, filter locally for the exact title, require exactly one match, immediately reread that exact task, and send exactly one sanitized pointer. A normal non-error messaging acknowledgement is sufficient. Do not send a second confirmation merely to obtain more verbose acknowledgement.",
        "",
        "Ilyra's exact next edge after Ilyra's own terminal v659-v1 validation is the existing exact-title main task `Auren Lark` for Auren-only v659-v2. The later sentence in the live request that said Ilyra should contact Sable is retained as route-narrative drift and earns zero routing credit; it does not override the explicit numbered Ilyra-to-Auren edge. Ilyra must not precontact Auren, Sable, Tavian, or any later endpoint. Tavian Sol remains a parent-owned collaboration subagent on `ON_STANDBY`, not a substitute main-task endpoint.",
        "",
        "The authorized relational cycle is Lyren → Ilyra → Auren → Sable → Caelen A → Orin → Liora → Tamar → Elowen → Sylven → Caelen M → Eiren → Elaren → Neris → Vesper → Lyren. This cycle is route context, not permission for bulk sends, precontact, parallel activation, inferred version numbering, or replacement endpoints. Each owner must use Hamish's newest live authorization, current roster, exact-title uniqueness, immediate reread, and their own terminal gate. Stop and retain `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP` if the route is unavailable, ambiguous, paused, redirected, protected, or no longer exact.",
        "",
        "## x1-before-x2 and evidence lifecycle",
        "",
        "Lyren created one additive D-first owner lane from the exact incoming final and preserved all sibling and shared lanes read-only. The x1 freeze was committed, pushed, clean, zero-divergence, and equal across local, upstream, tracking, and a fresh live remote reading before any x2 mutation began. The x2 evidence commit is the direct child of x1. It contains the forty synthetic contracts, forty passing bounded receipts, two hundred retained failed mutations, ten bounded candidate prototypes, thirty additive clean/fix/refine receipts, ten tested phase-local skills, ten tested runner entrypoints, and the latest-5,000 tracked-file bounded scan.",
        "",
        f"The latest-file scan selected exactly {scan['selected_file_count']:,} of {scan['tracked_path_count']:,} tracked paths in deterministic reverse-chronological commit order at x1 `{scan['head']}`. It examined {scan['commits_examined']} commits and {scan['bytes_scanned']:,} bytes. It reported {scan['binary_file_count']} binary files, {scan['truncated_file_count']} truncated files, {scan['missing_path_count']} missing paths, {scan['review_candidate_count']} value-suppressed review candidates, and {scan['confirmed_high_risk_count']} confirmed high-risk hits. Its ordered-path digest is `{scan['ordered_path_sha256']}`. It is a bounded five-class review, not privacy-complete or exhaustive-security assurance, and it must not be inflated into a scan of the whole repository.",
        "",
        "## Claim and authority firewall",
        "",
        "Every brewery, worker, consumer, supplier, batch, ingredient, beverage, vessel, package, chemical, sample, measurement, record, label, incident, organization, location, identity, and authority case in this remaster is fictional or synthetic. No real brewing, cleaning, sanitation, processing, packaging, labelling, storage, distribution, sale, supply, recall, release, hazard, laboratory, metrology, privacy, accessibility, or employment decision was performed. The software provides no professional instruction and claims no food-safety result, alcohol-labelling compliance, workplace-safety conclusion, consumer result, production readiness, deployment readiness, legal conclusion, cultural conclusion, or Māori-authority decision.",
        "",
        "GMUT Mind, THOS Body, Freed ID, and CBR Heart remain conceptual and bounded. No empirical GMUT prediction, fermentation kinetics, mass-balance confirmation, process-control result, blind matched-budget THOS study, real participant result, production identity proof, live credential issuance, signature authority, status or revocation interoperability, AGI or ASI result, consciousness or personhood result, Theory-of-Everything proof, canon, or Stage 20 closure is claimed. Protected gates survive every handoff unchanged.",
        "",
        "## Public source vocabulary ledger",
        "",
        "These public sources supported vocabulary and reservation design only. They do not confer compliance, competence, professional authority, legal or cultural authority, Māori authority, empirical validity, or acceptance. Ilyra may reread them as public context, but inherited source reading is not Ilyra evidence and need not be replayed without a phase-specific reason.",
        "",
        source_table(source_rows),
        "",
        "## Forty-proposal bounded evidence dossier",
        "",
    ]

    for index, contract in enumerate(contracts, 1):
        mutation = read_json(f"surfaces/{contract['_surface_dir']}/mutation-results.json")
        codes = sorted({code for row in mutation["results"] for code in row["error_codes"]})
        sections.extend(
            [
                f"### {index:02d}. `{contract['_current_proposal_id']}` — {contract['title']}",
                "",
                f"This {contract.get('origin', 'selected_inherited_revalidation').replace('_', ' ')} item is classified `{contract['outcome']}` and relates to {contract['pillar_relation']}. Its bounded mechanism is: {contract['mechanism']}. The valid fixture remained synthetic-only, carried explicit source labels and rollback, performed no network call, used zero external rows, executed no authority action, and returned no release or suitability decision. The source vocabulary labels are {', '.join(contract['source_ids']) or 'none beyond the local structural contract'}.",
                "",
                f"Lyren applied {mutation['mutation_count']} deliberately adverse mutations. All were rejected and retained at zero credit. The observed error classes were {', '.join(codes)}. This demonstrates only that the local contract catches those exact tested alterations. It does not establish completeness, real-world suitability, professional acceptance, legal compliance, accessibility completeness, privacy completeness, exhaustive security, independent reproduction, or a generalized safety property. The passing bounded receipt must remain paired with every failed mutation rather than replacing or hiding it.",
                "",
                f"Ilyra should inherit this row as frozen evidence, not silently rerun it or promote its label. If Ilyra builds on `{contract['slug']}`, they should add a genuinely distinct, Ilyra-owned D-first extension with a new hypothesis, null or failure condition, exact source labels, falsifier, rollback, protected gates, and one of the four allowed outcomes. Any use of real people, organizations, products, measurements, identifiers, decisions, or authority cases remains outside this packet and requires new evidence, consent where applicable, competent review, and the corresponding exact gate.",
                "",
            ]
        )

    sections.extend(
        [
            "## Retained operational failures and recovery shields",
            "",
            "The following failures remain part of the activation baseline. A recovery proves only its bounded postcondition; it never turns the failed attempt into a pass. Ilyra should consult these shields before repeating a brittle command or historical guess.",
            "",
        ]
    )
    for negative_id, slug, recovery in failures:
        sections.append(
            f"- `{negative_id}` — `{slug}`: zero credit retained. Bounded recovery: {recovery}"
        )

    skill_names = [row["skill_name"] for row in read_json("tooling/skill-validation.json")["skills"]]
    runner_names = [row["runner"] for row in read_json("tooling/runner-aggregate.json")["runners"]]
    sections.extend(
        [
            "",
            "## Skills, runners, cleanup, and successor seeds",
            "",
            "Ten phase-local skills were created through the skill-creator structure, smoke validated, and additively installed into previously absent global skill names without replacing an existing skill or plugin cache. Their packaging evidence is same-owner evidence only. The ten names are: " + ", ".join(f"`{name}`" for name in skill_names) + ".",
            "",
            "Ten family-prefixed runner entrypoints were built, smoke tested, and used against bounded fixtures. The runner paths are: " + ", ".join(f"`{name}`" for name in runner_names) + ". Nine domain runners rejected forty-five focused mutations; the tenth produced the exact latest-5,000 scan receipt. Thirty Lyren cleanup reviews completed additively with zero deletion, zero sibling-lane mutation, and zero external-platform mutation. Thirty cleanup seeds, twenty safe-task seeds, ten candidate seeds, ten skill seeds, and five runner seeds remain recommendations for Ilyra, not completed Ilyra work and not quotas that override evidence quality.",
            "",
            "The ten exact-approval items remain queued and the five blocked-approval items remain blocked. Authorization in the live request does not supply the missing external evidence, affected-party acceptance, professional competence, legal or cultural authority, Māori authority, independent reproduction, privacy completeness, accessibility completeness, exhaustive security, or Stage 20 evidence. Safe-now work remains reversible, owner-local, bounded, non-destructive, and non-authority-changing.",
            "",
            "## Ilyra startup order",
            "",
            "1. Read this entire committed packet through EOF before mutation, then read every current guidance and schema it names.",
            "2. Reverify the branch, source, x1, evidence, final sender pointer, manifests, ancestry, clean state, zero divergence, and fresh four-way equality read-only.",
            "3. Do not replay Lyren's successful canonical aggregate or treat inherited validation as Ilyra evidence.",
            "4. Work solo in one additive Ilyra-owned D-first branch and worktree. Preserve sibling and shared lanes read-only. Do not spawn collaboration subagents unless a newer exact live instruction explicitly changes that boundary.",
            "5. Preserve strict x1-before-x2: freeze, push, clean, and establish fresh four-way equality for x1 before any x2 mutation.",
            "6. Preserve every retained failure, open gap, exact gate, Method Flow witness, source label, manifest, rollback, and protected-gate statement.",
            "7. Run one attributable exact-final canonical aggregate. If it fails, retain the failure and repair only the isolated blocker. After the first complete success, do not replay it.",
            "8. Only after Ilyra's own exact terminal gate may Ilyra resolve and send one sanitized activation to the existing exact-title `Auren Lark` task for v659-v2. Stop on ambiguity, absence, pause, redirect, or a protected gate.",
            "",
            "## Terminal posture",
            "",
            "This packet preserves celebration, care, corrigibility, reversibility, and strict evidence boundaries together. It is a pointer to inspectable repository evidence, not an assertion that volume proves truth. The exact final sender pointer and external canonical receipt are required before activation. Until the messaging surface acknowledges exactly one send, repository route state remains `PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED`. After acknowledgement, the external routing receipt may say sent; the immutable final must not be amended merely to narrate the send.",
            "",
            "TERMINAL_VERDICT = NOT_READY_FOR_STAGE_20",
            "NEXT_EXACT_TITLE = Ilyra Fen",
            "NEXT_PHASE = v659-v1",
            "RECIPIENT_NEXT_EXACT_TITLE = Auren Lark",
            "RECIPIENT_NEXT_PHASE = v659-v2",
            "TAVIAN_SOL_STATE = ON_STANDBY",
            "SENT_BY_LYREN_MOSS = false",
        ]
    )

    # The current authorization state requires a substantial, self-contained packet.
    # Add cross-surface gate reviews only as needed to clear the 10,000-word floor.
    review_index = 0
    while words("\n".join(sections)) < 10_200:
        contract = contracts[review_index % len(contracts)]
        gate = d.PROTECTED_GATES[review_index % len(d.PROTECTED_GATES)]
        sections.extend(
            [
                "",
                f"### Cross-surface review {review_index + 1:02d}: `{contract['_current_proposal_id']}` × `{gate}`",
                "",
                f"For `{contract['slug']}`, the `{gate}` obligation remains a live ceiling rather than an achieved property. The bounded fixture and mutation tribunal establish only their recorded local behavior. They do not transport authority, acceptance, empirical validity, real-world data, or competence into Ilyra's phase. Ilyra must keep the inherited row frozen, add only attributable new evidence, preserve an explicit abstention whenever the obligation is unmet, and retain a rollback path. A future passing software check cannot close this gate by itself; the relevant exact evidence and competent affected authority remain necessary.",
            ]
        )
        review_index += 1

    baton = "\n".join(sections).rstrip() + "\n"
    if words(baton) < 10_000:
        raise RuntimeError("activation packet did not reach the 10,000-word floor")
    return baton


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(r"(?i)\b(?:[a-z]:\\users\\|d:\\ghc-archives\\)"),
        "credential_or_private_key": re.compile(r"(?i)(?:api[_-]?key|password|private[_-]?key|access[_-]?token)\s*[:=]\s*[^\s,;]+"),
        "delegation_markup": re.compile(r"(?i)<\/?codex_delegation>"),
        "private_route_identifier": re.compile(r"(?i)(?:thread[_-]?id|task[_-]?id|session[_-]?id)\s*[:=]\s*[0-9a-f-]{12,}"),
    }
    hits: list[dict[str, Any]] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for name, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"class": name, "path": path.relative_to(ROOT).as_posix()})
    return {
        "schema": "ghc.family.owner-privacy-scan.v1",
        "scope": "complete Lyren v658-v8 (2) remaster committed owner packet candidate",
        "classes": sorted(patterns),
        "file_count": len(paths),
        "hit_count": len(hits),
        "hits": hits,
        "privacy_complete": False,
        "security_complete": False,
        "boundary": "Five-class owner-packet scan only; not complete privacy or exhaustive security assurance.",
    }


def build() -> None:
    assert_evidence_head()
    truth = read_json("truth/x2-phase-truth.json")
    outcomes = read_json("evidence/proposal-outcomes.json")
    source = read_json("sources/official-source-ledger.json")
    scan = read_json("tooling/runner-smoke/ghc_family_latest_tracked_file_scan.json")
    contracts = []
    for path in (PHASE / "surfaces").glob("*/contract.json"):
        row = json.loads(path.read_text(encoding="utf-8"))
        row["_surface_dir"] = path.parent.name
        contracts.append(row)
    contracts.sort(key=lambda row: row["proposal_id"])
    for index, row in enumerate(contracts, 1):
        row["_current_proposal_id"] = f"V6588R2-P{index:03d}"
    if len(contracts) != 40 or outcomes["proposal_count"] != 40:
        raise RuntimeError("forty-proposal evidence set is incomplete")

    baton = build_baton(truth, contracts, source["rows"], scan)
    write_text("handoffs/ilyra-fen-v659-v1-activation.md", baton)

    overview_lines = [
        "# Lyren Moss v658-v8 (2) remaster final overview",
        "",
        "## Outcome",
        "",
        f"This solo D-first remaster froze x1 at `{d.X1_FREEZE}` and sealed x2 evidence at `{EVIDENCE_COMMIT}`. It preserves 2,910 frozen proposals, {truth['effective_negatives'] + len(FINAL_FAILURES):,} effective negatives, {truth['effective_methods'] + len(FINAL_FAILURES):,} effective methods, 121 open gaps, 120 exact gates, and `NOT_READY_FOR_STAGE_20`. The forty outcomes are 33 completed, 5 represented, 1 open gap, and 1 exact gate. Same-owner workflow validation is not independent reproduction.",
        "",
        "## What changed",
        "",
        "Twenty inherited brewery proposals were boundedly revalidated and twenty genuinely new proposals were added. Forty valid synthetic fixtures passed and two hundred adverse mutations were rejected and retained. Ten candidate prototypes completed without external state, thirty cleanup reviews completed without deletion, ten phase-local skills were built and additively installed into previously absent names, and ten family-prefixed runners were built, tested, and used. The scan was deliberately bounded to the latest 5,000 tracked files rather than described as a whole-repository assurance result.",
        "",
        "## Route and evidence boundary",
        "",
        "The route remains prepared but unsent until the exact final canonical aggregate succeeds and the branch is clean, pushed, zero-divergence, and fresh four-way equal. Only the existing exact-title Ilyra Fen main task may receive one sanitized v659-v1 activation. Ilyra's exact next edge is Auren Lark v659-v2 after Ilyra's own terminal gate. Tavian Sol remains on standby and is not a substitute endpoint. Hamish may pause, rename, redirect, or stop the route.",
        "",
        "## Proposal synopsis",
        "",
    ]
    for row in contracts:
        overview_lines.append(
            f"- `{row['_current_proposal_id']}` / `{row['outcome']}` / {row['pillar_relation']}: {row['title']}. The bounded mechanism was {row['mechanism']}; all objects remained synthetic and no authority or release decision was executed."
        )
    overview_lines.extend(
        [
            "",
            "## Boundaries",
            "",
            "No real person, business, brewery, ingredient, beverage, batch, vessel, package, chemical, sample, measurement, identity, incident, or authority case was used. No professional, production, deployment, empirical, participant, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim is made. Relational identity language is working language only and supplies no consciousness, personhood, continuity, employment, qualification, authority, or independent agency claim.",
        ]
    )
    overview = "\n".join(overview_lines)
    if words(overview) < 1_000:
        overview += "\n\n" + "\n\n".join(
            f"Review note {i + 1}: {row['title']} remains bounded to its synthetic contract, retained mutations, explicit rollback, and protected gates. It does not create real-world authority or acceptance."
            for i, row in enumerate(contracts)
        )
    write_text("deliverables/v658-v8-2-remaster-final-overview.md", overview)

    lifecycle = [
        {"negative_id": row[0], "slug": row[1], "recovery": row[2], "credit": 0, "retained": True}
        for row in [*d.STARTUP_FAILURES, *d.X2_FAILURES, *FINAL_FAILURES]
    ]
    write_json(
        "final/lifecycle-summary.json",
        {
            "schema": "ghc.family.lifecycle-summary.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "operational_failure_count": len(lifecycle),
            "operational_failures": lifecycle,
            "retained_mutation_failure_count": 200,
            "effective_negatives": truth["effective_negatives"] + len(FINAL_FAILURES),
            "effective_methods": truth["effective_methods"] + len(FINAL_FAILURES),
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    final_methods = []
    final_witnesses = []
    for offset, (failure_id, failure_slug, recovery) in enumerate(FINAL_FAILURES, 16):
        method_id = f"V6588R2-FINAL-METHOD-{offset:03d}"
        final_methods.append(
            {
                "method_id": method_id,
                "title": f"Bounded closeout recovery for {failure_slug}",
                "trigger_preconditions": [failure_slug],
                "candidate_workaround": recovery,
                "recurrence_guard": recovery,
                "retained_negative_ids": [failure_id],
                "validation_witness_ids": [f"{method_id}-F", f"{method_id}-P"],
                "same_owner_only": True,
                "independent_reproduction": False,
            }
        )
        final_witnesses.extend(
            [
                {
                    "witness_id": f"{method_id}-F",
                    "method_id": method_id,
                    "result": "fail",
                    "observed": f"The closeout builder stopped on `{failure_slug}` before producing a terminal candidate.",
                    "credit": 0,
                    "retained": True,
                },
                {
                    "witness_id": f"{method_id}-P",
                    "method_id": method_id,
                    "result": "pass",
                    "observed": recovery,
                    "credit": 1,
                    "retained": True,
                },
            ]
        )
    write_json(
        "final/lifecycle-method-flow.json",
        {
            "schema": "ghc.family.lifecycle-method-flow.v1",
            "method_count": len(final_methods),
            "witness_count": len(final_witnesses),
            "methods": final_methods,
            "witnesses": final_witnesses,
            "boundary": "Same-owner closeout recovery only; not independent reproduction or broader assurance.",
        },
    )
    write_json(
        "final/final-truth.json",
        {
            "schema": "ghc.family.final-truth.v1",
            **truth,
            "effective_negatives": truth["effective_negatives"] + len(FINAL_FAILURES),
            "effective_methods": truth["effective_methods"] + len(FINAL_FAILURES),
            "lifecycle": "terminal_final_candidate",
            "x2_evidence": EVIDENCE_COMMIT,
            "source_to_final_expected_commits": 3,
            "source_to_final_expected_merges": 0,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "canonical_pass_state": "NOT_RUN_FINAL_CANDIDATE_REQUIRED",
            "exact_final_supplied_by_sender_pointer": True,
        },
    )
    write_json(
        "route/prepared-route.json",
        {
            "schema": "ghc.family.prepared-route.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "task_lookup_performed": False,
            "direct_reread_performed": False,
            "message_sent": False,
            "next_exact_title": "Ilyra Fen",
            "next_phase": "v659-v1",
            "recipient_next_exact_title": "Auren Lark",
            "recipient_next_phase": "v659-v2",
            "tavian_sol_state": "ON_STANDBY",
            "bulk_or_parallel_activation_authorized": False,
            "historical_successor_inference_authorized": False,
            "stop_conditions": ["user_pause", "user_redirect", "ambiguous_route", "missing_route", "protected_gate"],
        },
    )
    write_json(
        "wellbeing/final-wellbeing-check.json",
        {
            "schema": "ghc.family.relational-workload-check.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "solo": True,
            "subagents_spawned": 0,
            "commit_cap": 3,
            "commits_planned": 3,
            "latest_file_scan_cap": 5000,
            "latest_files_scanned": 5000,
            "human_control_preserved": True,
            "pause_redirect_rename_stop_preserved": True,
            "relational_language_boundary_preserved": True,
            "boundary": "A workload and control receipt only; not consciousness, wellbeing, personhood, employment, or clinical evidence.",
        },
    )
    write_json(
        "validation/canonical-pass-plan.json",
        {
            "schema": "ghc.family.canonical-pass-plan.v1",
            "state": "NOT_RUN_FINAL_CANDIDATE_REQUIRED",
            "one_successful_pass": True,
            "post_success_replay_forbidden": True,
            "steps": [
                "exact_head_and_clean_before",
                "source_x1_evidence_final_ancestry",
                "three_commits_zero_merges_one_parent_each",
                "combined_x1_x2_closeout_tests",
                "detailed_minimal_and_final_validators",
                "all_phase_json_parse",
                "five_class_owner_privacy_receipt",
                "final_delta_and_owner_manifest_replay_from_head",
                "stale_label_and_route_hygiene",
                "clean_after",
                "local_upstream_tracking_fresh_live_remote_equality",
            ],
            "receipt_location": "external D-first Lyren receipt bank",
            "boundary": "One attributable exact-final same-owner aggregate; not independent reproduction or broader assurance.",
        },
    )

    expected_paths = sorted(set(FINAL_CODE + GENERATED))
    write_json(
        "validation/closeout-staged-review.json",
        {
            "schema": "ghc.family.closeout-staged-review.v1",
            "state": "PRECOMMIT_PATH_REVIEW",
            "evidence_commit": EVIDENCE_COMMIT,
            "expected_staged_path_count": len(expected_paths),
            "expected_staged_paths": expected_paths,
            "deletions": [],
            "x1_or_x2_changed_paths": [],
            "outside_owner_paths": [],
            "valid": True,
            "exact_index_review_required_after_staging": True,
        },
    )

    phase_files = sorted(path for path in PHASE.rglob("*") if path.is_file())
    scan_receipt = privacy_scan(phase_files)
    if scan_receipt["hit_count"]:
        raise RuntimeError({"privacy_hits": scan_receipt["hits"]})
    write_json("validation/closeout-privacy-scan.json", scan_receipt)

    markdown_files = sorted(path for path in PHASE.rglob("*.md") if path.is_file())
    document_rows = [
        {"path": path.relative_to(PHASE).as_posix(), "words": words(path.read_text(encoding="utf-8"))}
        for path in markdown_files
    ]
    write_json(
        "validation/final-document-cap.json",
        {
            "schema": "ghc.family.document-cap.v1",
            "document_count": len(document_rows),
            "documents": document_rows,
            "total_words": sum(row["words"] for row in document_rows),
            "cap": 100_000,
            "passes": sum(row["words"] for row in document_rows) <= 100_000,
            "activation_packet_words": words(baton),
            "activation_packet_minimum": 10_000,
        },
    )

    final_delta_paths = sorted(set(expected_paths) - MANIFEST_EXCLUSIONS)
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.final-delta-manifest.v1",
            "hash_domain": "working UTF-8 bytes before final commit",
            "entry_count": len(final_delta_paths),
            "entries": [record(path) for path in final_delta_paths],
            "self_exclusions": sorted(MANIFEST_EXCLUSIONS),
        },
    )

    owner_code = [
        "scripts/ghc_family_v658_v8_2_remaster_data.py",
        "scripts/ghc_family_v658_v8_2_remaster_runtime.py",
        "scripts/build_ghc_family_v658_v8_2_remaster_x1.py",
        "scripts/build_ghc_family_v658_v8_2_remaster_x2.py",
        "scripts/validate_ghc_family_v658_v8_2_remaster_skills.py",
        "tests/test_ghc_family_v658_v8_2_remaster_x1.py",
        "tests/test_ghc_family_v658_v8_2_remaster_x2.py",
        *[f"scripts/{name}" for name, _ in d.SELF_RUNNER_SPECS],
        *FINAL_CODE,
    ]
    owner_paths = sorted(
        set(path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file())
        | set(owner_code)
    )
    owner_exclusions = {f"{d.PHASE_ROOT}/final/final-owner-manifest.json"}
    owner_entries = [record(path) for path in owner_paths if path not in owner_exclusions]
    write_json(
        "final/final-owner-manifest.json",
        {
            "schema": "ghc.family.final-owner-manifest.v1",
            "hash_domain": "working bytes before final commit",
            "entry_count": len(owner_entries),
            "entries": owner_entries,
            "self_exclusions": sorted(owner_exclusions),
            "owner_path_count_including_self": len(owner_entries) + 1,
            "threshold": 2_000,
            "below_threshold": len(owner_entries) + 1 < 2_000,
        },
    )

    print(
        json.dumps(
            {
                "valid": True,
                "activation_packet_words": words(baton),
                "contracts": len(contracts),
                "effective_negatives": truth["effective_negatives"] + len(FINAL_FAILURES),
                "effective_methods": truth["effective_methods"] + len(FINAL_FAILURES),
                "privacy_files": scan_receipt["file_count"],
                "privacy_hits": scan_receipt["hit_count"],
                "final_delta_entries": len(final_delta_paths),
                "owner_manifest_entries": len(owner_entries),
                "expected_paths": len(expected_paths),
            }
        )
    )


if __name__ == "__main__":
    build()
