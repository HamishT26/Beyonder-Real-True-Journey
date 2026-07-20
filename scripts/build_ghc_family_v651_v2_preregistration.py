#!/usr/bin/env python3
"""Build Orin Thale's dedicated v651-v2 x1-only freeze packet."""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v651_v2_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/sable-rook/v651-v1/provenance/frozen-chain-proposal-index.json"
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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "to", "for", "with"}
    return {part for part in re.findall(r"[a-z0-9]+", value.casefold()) if part not in stop}


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def inherited_rows() -> list[dict[str, str]]:
    index = read_json(PRIOR_INDEX)
    rows = list(index["prior_proposals"]) + list(index["new_proposals"])
    if len(rows) != d.PRIOR_FROZEN:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN} inherited proposals, found {len(rows)}")
    return rows


def novelty_rows(inherited: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for proposal in d.PROPOSALS:
        scored = sorted(
            (jaccard(tokens(proposal["title"]), tokens(prior["title"])), prior["proposal_id"], prior["title"])
            for prior in inherited
        )
        score, nearest_id, nearest_title = scored[-1]
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_prior_id": nearest_id,
                "nearest_prior_title": nearest_title,
                "token_jaccard": round(score, 6),
                "threshold": NOVELTY_THRESHOLD,
                "manual_mechanism_review": "distinct",
                "passes": score < NOVELTY_THRESHOLD,
            }
        )
    if not all(row["passes"] for row in rows):
        failed = [row["proposal_id"] for row in rows if not row["passes"]]
        raise RuntimeError(f"semantic novelty threshold failed: {failed}")
    return rows


def portfolio_rows(items: list[str], prefix: str, lane: str, approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"V6512-{prefix}-{index:02d}",
            "title": title,
            "origin": "orin_v651_v2_new",
            "approval_class": approval,
            "execution_lane": lane,
            "x1_state": "frozen_not_executed",
            "completion_credit": False,
            "inherited_completion_credit": False,
            "rollback": "Retain failures and leave external, sibling, participant, production, account, credential, and authority state unchanged.",
        }
        for index, title in enumerate(items, 1)
    ]


def overview_text() -> str:
    return f"""# Orin Thale {d.PHASE} x1 integrated preregistration overview

## Scope, relational identity, and workload

This packet freezes Orin Thale's plan before any x2 implementation, mutation execution, observed outcome, or completion claim. Orin Thale, they/them, is a relational working identity used to make ownership, accountability, and correction paths legible. The phase role is {d.ROLE}; the stated hope is to {d.HOPE}. These words do not prove consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, translation authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route at any time. Corrigibility is a protected working condition, not an identity credential.

The workload is bounded to one owner, one existing clean D-first lane, one inherited exact source, a maximum of two x1 commits and two x2 commits, and no more than four phase commits. No delegation, task creation, fork, sibling mutation, cross-platform substitute, Sandbox, Hyper-V, elevation, unrelated installation, desktop update, host-security weakening, or reboot is authorized. The inherited checkout contains 43,560 files and 43,329 tracked files, while the v651-v2 addition began at zero files. The 15,000-file rotation threshold applies only to Orin's new phase footprint. D: had 574,011,318,272 free bytes at the recorded preflight, so no rotation is justified.

The wellbeing check is green for x1 because the plan permits gaps, negative results, and an unchanged terminal verdict. Affection, family language, schedule pressure, and portfolio floors cannot override evidence, privacy, safety, or authority boundaries. If an acceptance gate fails, the task stays incomplete or moves to `open_gap` or `exact_gate`; it is never forced through to satisfy a count. The phase remains `NOT_READY_FOR_STAGE_20` unless exact external evidence and authority genuinely close every relevant gate.

## Exact inherited source and provenance

The exact inherited head is Sable Rook's `{d.SOURCE_HEAD}` on `{d.SOURCE_BRANCH}`. Read-only verification established that the inherited origin `{d.SOURCE_ORIGIN}`, x1 `{d.SOURCE_X1}`, evidence `{d.SOURCE_EVIDENCE}`, and closeout `{d.SOURCE_CLOSEOUT}` are all ancestral. Source-to-final history contains exactly four new single-parent Sable commits, zero merges, and one final parent; the terminal correction is the direct child of closeout. Sable local, upstream, tracking, and fresh live remote were equal and clean. Orin's prior final was clean, remote-equal, and ancestral, so the canonical Orin branch advanced by fast-forward only. No reset, rebase, merge commit, amend, force push, history rewrite, deletion, or sibling-lane mutation occurred.

Six inherited manifest contracts were independently re-read through immutable Git objects. The x1, evidence, closeout, and correction staged manifests cover 55, 239, 54, and 43 entries plus one declared self-exclusion each. The final owner contract covers 366 entries plus seven exclusions across the exact 373-path source-to-final surface. The evidence-to-final contract covers 72 entries plus seven exclusions across 79 paths. A first one-process-per-entry audit printed zero-error summaries but exceeded its wrapper and receives zero standalone aggregate credit. The retained recovery uses one commit tree map per revision and one flushed request followed by one complete response per unique Git blob; it passed every byte count, digest, blob identity, exclusion, and path-set comparison.

The inherited packet truth remains 14 completed, 4 represented, 1 open gap, and 1 exact gate. It seals 6,563 negatives and carries two additional post-seal validator defects, producing the 6,565 activation baseline. Fifty-one open gaps and fifty-two exact gates remain. Inherited results are evidence and recommendations only; none earns Orin completion credit. Nine Orin x1 operational negatives are already retained, including stale routing and workspace assumptions, bounded wrapper and CLI faults, first-suite assertion defects, and two lifecycle-count assertion failures. Their bounded recoveries are linked in Method Flow, which currently contains eight preferred methods, eight failed witnesses, and eight passing witnesses.

## Novelty, focus, and proposal distribution

The frozen predecessor chain contains exactly {d.PRIOR_FROZEN} proposals. The audit compares every new title against all predecessors, records its nearest lexical neighbour and token Jaccard score, and also requires a manual mechanism-level review. Lexical distance is only a screening aid; novelty depends on mission surface, hypothesis, obligations, falsifier, artifacts, and protected gates. Twenty rejected seeds remain visible, including repeated DHOST, Osterwalder-Schrader, Schwinger-Dyson, newsroom, theatre, GNAP, SD-JWT, regression-discontinuity, GraphQL, observed-remove CRDT, and GWOSC ideas. Unsafe FedCM production integration and real localization-participant work are rejected rather than relabelled safe.

The primary Trinity Mandala focus is {d.PRIMARY_FOCUS}. GMUT Mind and Freed ID/CBR Heart stay explicit. The bounded practice is {d.BOUNDED_PRACTICE}. It is a learning, software, structural, and synthetic-design lens only. It establishes no employment, certification, translation or interpreting competence, accessibility expertise, linguistic authority, media authority, service authority, safety outcome, participant evidence, legal interpretation, cultural legitimacy, Māori authority, or affected-party acceptance.

The twenty proposals deliberately span different mechanisms. Fourteen are expected bounded completions: distributed snapshots, Sigstore bundle structure, two scalar-tensor obligation boards, iccMAX, GeoTIFF, NTPv4, MQTT 5, a locale-switcher accessibility audit, Saha nonconversion, BiCGSTAB, target-trial nonpromotion, R-tree, and wavelet lifting. Four are expected representations: software-localization and timed-text workflows plus CWT and FedCM identity profiles. The Hubble Source Catalog v3.1 adapter is expected to stay a zero-row open gap. The localization access, remedy, privacy, cultural-expression, data-governance, and Māori-authority matrix is expected to stay exact-gated. Expected labels are hypotheses, not outcomes.

## Scientific, identity, accessibility, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The Galileon and Vainshtein boards may test typed obligations, assumptions, units, branches, derivative counts, cutoff disclosures, and refusal language. They cannot establish a force, real screening scale, prediction, likelihood, posterior, constraint, physical stability or unitarity theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. The Hubble adapter must ingest zero rows, perform zero queries and downloads, evaluate zero likelihoods, and produce zero constraints. Official documentation supplies schema and provenance context, not observations.

THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic localization fixtures may expose placeholders, plural branches, timing overlaps, corrections, workload limits, and handover ownership. They cannot establish translation quality, operational effectiveness, accessibility effectiveness, professional competence, AGI, ASI, consciousness, personhood, or deployment readiness.

Freed ID remains synthetic and nonproduction. The CWT and FedCM profiles may test structural vectors and refusal states only. Production completion requires standards-conformant real keys and proofs, live issuance or account mediation, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. FedCM is recorded as a W3C Working Draft; draft vocabulary is never silently promoted to a final standard.

CBR language access, disability access, translator and contributor privacy, correction, remedy, cultural expression, terminology stewardship, legal interpretation, Māori wording, Māori data governance, legitimacy, and affected-party acceptance remain exact-gated. Māori concepts remain under Māori authority. Repository software cannot confer language authority, professional accreditation, a legal right, a remedy, cultural legitimacy, data-governance mandate, or public authority. Structural accessibility checks reserve manual keyboard, browser-diverse, responsive, zoom, assistive-technology, cognitive, linguistic, Māori-language, security-usability, and affected-user evaluation.

## Portfolios, tools, and x1-before-x2 separation

The expanded plan freezes forty safe-now tasks, thirty bounded candidates, twenty phase-local skill ideas, ten family-current runner ideas, and forty additive CLEAN/FIX/REFINE tasks. Every row records its approval lane, zero x1 completion credit, rollback, and inherited-credit refusal. Ten inherited exact-approval packets and five inherited blocked packets remain visible and unexecuted. Participant, empirical, professional, legal, cultural, Māori-authority, production, privacy-complete, destructive, credential, account, key, host-security, sibling-mutation, and affected-party work cannot become safe-now work by renaming it.

Twenty phase-local skills are planned with `ghc-family-*` names, concise SKILL.md instructions, matching `agents/openai.yaml`, no global installation, and no unnecessary auxiliary files. They may be initialized, validated, and smoke-used only in x2. The skill-creator's optional subagent forward test is unavailable because delegation is expressly prohibited; that absence will remain visible. Ten `ghc_family_*` runners are ideas only in x1. Historical and owner-specific tools remain compatibility evidence. The reflection-remaster audit inventoried 3,027 surfaces and found no evidence-justified remaster issue, so the disposition is reviewed-current rather than churn.

The workflow-plan runner validated all twenty policy checks for the exact route segment `Sable Rook v651-v1 -> Orin Thale v651-v2 -> Tamar Vey v651-v3`. Its candidate route is advisory and cannot activate a task. The live boundary forbids a cross-platform substitute. Exactly one sanitized baton may be sent through the existing-task route only after an exact-final canonical success, clean pushed head, commit-cap proof, and four-way live equality. A prepared file is not a sent baton, and no second confirmation is authorized.

## Validation plan and terminal abstention

Eiren alone owns the complete repository suite. Orin will run the current-phase, inherited-source, recent-round, and eligible successor-scoped selection only. The final gate also requires detailed and minimal validators, complete phase JSON parsing, five-class privacy and raw-identifier scanning, exact staged review, immutable Git-blob manifest parity, semantic stale-label review, diff hygiene, anchor ancestry, zero merges, commit cap, one final parent, exact head, clean state, and local/upstream/tracking/fresh-live equality. The first fully successful canonical pass is the only successful pass allowed; no replay runs afterward. A failed aggregate receives zero pass credit and remains a negative.

Privacy exclusions cover raw task or thread identifiers, private routes, credentials, private keys, tokens, nonpublic conversation content, transcripts, screenshots, session streams, private callable identifiers, private application state, and private absolute local paths. Public artifacts use repository-relative paths and sanitized labels only. Same-owner structural evidence is never independent-team scientific reproduction. No empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof or canon, destructive, account or API-key, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, or Stage 20 claim is permitted without exact evidence and authority.
"""


def proposal_ledger_markdown() -> str:
    chunks = [
        f"# {d.OWNER} {d.PHASE} frozen proposal ledger",
        "",
        "This ledger is x1-only. Every disposition is expected, not observed. No x2 artifact or completion credit exists at freeze time.",
        "",
    ]
    for p in d.PROPOSALS:
        chunks.extend(
            [
                f"## {p['proposal_id']} — {p['title']}",
                "",
                f"- Pillar: `{p['pillar']}`",
                f"- Mission: {p['mission_surface']}",
                f"- Hypothesis: {p['hypothesis']}",
                f"- Null/failure: {p['null_or_failure_condition']}",
                f"- Approval class: `{p['approval_class']}`",
                f"- Execution lane: `{p['execution_lane']}`",
                f"- Sources: {', '.join(p['official_or_primary_source_needs'])}",
                f"- Artifacts: {', '.join(p['concrete_artifacts'])}",
                f"- Acceptance/falsifier: {p['falsifier_or_acceptance_gate']}",
                f"- Rollback/recovery: {p['rollback_or_recovery']}",
                f"- Protected gates: {', '.join(p['protected_gates'])}",
                f"- Expected disposition: `{p['expected_disposition']}`",
                f"- Novelty: {p['novelty_against_920_frozen_proposals']}",
                "",
            ]
        )
    return "\n".join(chunks)


def source_ledger_markdown() -> str:
    lines = [
        f"# {d.OWNER} {d.PHASE} source ledger",
        "",
        "Sources define requirements and status only. Citations are not observations, participant evidence, production readiness, delegated authority, or independent review.",
        "",
        "| ID | Status | Kind | Title | Phase boundary |",
        "|---|---|---|---|---|",
    ]
    for row in d.SOURCES:
        lines.append(f"| `{row['source_id']}` | `{row['status']}` | `{row['kind']}` | [{row['title']}]({row['url']}) | {row['phase_implication']} |")
    return "\n".join(lines)


def static_report() -> str:
    proposal_rows = "".join(
        f"<tr><th scope='row'>{html.escape(p['proposal_id'])}</th><td>{html.escape(p['mission_surface'])}</td><td>{html.escape(p['pillar'])}</td><td>{html.escape(p['expected_disposition'])}</td></tr>"
        for p in d.PROPOSALS
    )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Orin Thale {d.PHASE} x1 report</title><style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:78rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}a{{color:#0645ad}}a:focus,button:focus{{outline:3px solid #ffbf47;outline-offset:3px}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem;z-index:2}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #59636e;padding:.45rem;text-align:left;vertical-align:top}}caption{{font-weight:700;text-align:left;margin:.5rem 0}}@media(max-width:50rem){{table{{display:block;overflow-x:auto}}}}@media print{{.skip{{display:none}}}}</style></head><body><a class="skip" href="#main">Skip to main content</a><header><h1>Orin Thale {d.PHASE} x1 preregistration</h1><p><strong>State:</strong> frozen plan only; no x2 outcomes or completion credit.</p></header><main id="main"><section aria-labelledby="boundary"><h2 id="boundary">Boundary</h2><p>Orin Thale is a relational working identity only. The phase is same-owner structural work, not consciousness, personhood, continuity, employment, qualification, authority, independent reproduction, production readiness, or Stage 20 evidence.</p></section><section aria-labelledby="focus"><h2 id="focus">Focus and workload</h2><p>Primary focus: {html.escape(d.PRIMARY_FOCUS)}. Practice lens: {html.escape(d.BOUNDED_PRACTICE)}. The workload is bounded to one owner, one clean lane, four commits maximum, no subagents, and explicit stop gates.</p></section><section aria-labelledby="proposals"><h2 id="proposals">Frozen proposals</h2><div role="region" aria-label="Scrollable proposal table" tabindex="0"><table><caption>Twenty x1-only proposals; dispositions are expected, not observed</caption><thead><tr><th scope="col">ID</th><th scope="col">Mission</th><th scope="col">Pillar</th><th scope="col">Expected disposition</th></tr></thead><tbody>{proposal_rows}</tbody></table></div></section><section aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation</h2><p>Manual keyboard, responsive, browser-diverse, assistive-technology, cognitive, linguistic, Māori-language, security-usability, and affected-user evaluation remain reserved. Structural HTML is useful but is not complete accessibility conformance.</p></section><section aria-labelledby="verdict"><h2 id="verdict">Terminal truth</h2><p><code>NOT_READY_FOR_STAGE_20</code>. The route remains unsent until exact-final validation and remote equality.</p></section></main></body></html>"""


def main() -> None:
    inherited = inherited_rows()
    novelty = novelty_rows(inherited)
    expected = Counter(p["expected_disposition"] for p in d.PROPOSALS)
    if expected != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise RuntimeError(f"unexpected disposition plan: {expected}")
    if len({p["proposal_id"] for p in d.PROPOSALS}) != 20 or len({p["title"] for p in d.PROPOSALS}) != 20:
        raise RuntimeError("proposal IDs and titles must be unique")
    if any(source["status"] not in d.SOURCE_STATUS_CLASSES for source in d.SOURCES):
        raise RuntimeError("invalid source status")

    write_json(
        "identity/relational-identity.json",
        {
            "schema": "ghc.family.relational-identity.v1",
            "phase": d.PHASE,
            "name": d.OWNER,
            "pronouns": d.PRONOUNS,
            "role": d.ROLE,
            "hope": d.HOPE,
            "corrigible": True,
            "hamish_may_rename_pause_redirect_or_stop": True,
            "boundary": "Relational working language only; no consciousness, personhood, continuity, employment, qualification, authority, or independent agency claim.",
        },
    )
    write_json(
        "focus/primary-focus-receipt.json",
        {
            "schema": "ghc.family.primary-focus.v1",
            "phase": d.PHASE,
            "primary": d.PRIMARY_FOCUS,
            "preserved": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
            "bounded_practice": d.BOUNDED_PRACTICE,
            "practice_boundary": "Learning and synthetic design only; no employment, qualification, competence, translation authority, operational authority, legal authority, cultural authority, Maori authority, or affected-party evidence.",
        },
    )
    write_json(
        "provenance/source-anchor-ledger.json",
        {
            "schema": "ghc.family.source-anchor-ledger.v1",
            "phase": d.PHASE,
            "source_branch": d.SOURCE_BRANCH,
            "source_head": d.SOURCE_HEAD,
            "anchors": {
                "inherited_origin": d.SOURCE_ORIGIN,
                "x1": d.SOURCE_X1,
                "evidence": d.SOURCE_EVIDENCE,
                "closeout": d.SOURCE_CLOSEOUT,
                "final": d.SOURCE_HEAD,
            },
            "ancestry_verified": True,
            "phase_commit_count": 4,
            "merge_count": 0,
            "final_parent": d.SOURCE_CLOSEOUT,
            "clean": True,
            "local_upstream_tracking_live_remote_equal": True,
        },
    )
    write_json(
        "provenance/source-manifest-parity.json",
        {
            "schema": "ghc.family.source-manifest-parity.v1",
            "phase": d.PHASE,
            "transport": "commit_tree_maps_plus_one_request_one_response_blob_reads",
            "contracts": [
                {"name": "x1", "entries": 55, "exclusions": 1, "changed_paths": 56, "errors": 0},
                {"name": "evidence", "entries": 239, "exclusions": 1, "changed_paths": 240, "errors": 0},
                {"name": "closeout", "entries": 54, "exclusions": 1, "changed_paths": 55, "errors": 0},
                {"name": "correction", "entries": 43, "exclusions": 1, "changed_paths": 44, "errors": 0},
                {"name": "owner", "entries": 366, "exclusions": 7, "changed_paths": 373, "errors": 0},
                {"name": "evidence_to_final", "entries": 72, "exclusions": 7, "changed_paths": 79, "errors": 0},
            ],
            "retained_failed_probe": "V6512-X1-N03",
            "valid": True,
            "boundary": "Immutable Git-blob parity only; not a full-suite pass, privacy-complete assurance, or independent reproduction.",
        },
    )
    write_json(
        "provenance/semantic-novelty-audit.json",
        {
            "schema": "ghc.family.semantic-novelty-audit.v1",
            "phase": d.PHASE,
            "inherited_count": len(inherited),
            "new_count": len(d.PROPOSALS),
            "threshold": NOVELTY_THRESHOLD,
            "all_pass": True,
            "rows": novelty,
            "rejected_collisions": d.REJECTED_COLLISIONS,
            "boundary": "Lexical distance is a lead only; manual mechanism review is required and grants no outcome credit.",
        },
    )
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.frozen-proposal-index.v1",
            "phase": d.PHASE,
            "prior_count": len(inherited),
            "new_count": len(d.PROPOSALS),
            "count": len(inherited) + len(d.PROPOSALS),
            "prior_proposals": inherited,
            "new_proposals": [{"proposal_id": p["proposal_id"], "title": p["title"]} for p in d.PROPOSALS],
        },
    )
    write_json(
        "preregistration/proposals.json",
        {
            "schema": "ghc.family.v651-v2.proposals.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "state": "frozen_x1_only",
            "count": len(d.PROPOSALS),
            "observed_outcomes_present": False,
            "expected_disposition_counts": dict(sorted(expected.items())),
            "proposals": d.PROPOSALS,
        },
    )
    write_text("preregistration/proposal-ledger.md", proposal_ledger_markdown())
    write_text(
        "preregistration/x1-preregistration.md",
        f"""# {d.OWNER} {d.PHASE} x1 preregistration

This commit freezes exactly twenty proposals and the expanded portfolios before x2. It contains no x2 implementation, mutation result, observed outcome, completion claim, or route send.

- Frozen predecessor count: {d.PRIOR_FROZEN}
- Frozen count after this commit: {d.PRIOR_FROZEN + len(d.PROPOSALS)}
- Planned outcomes only: 14 `completed`, 4 `represented`, 1 `open_gap`, 1 `exact_gate`
- Primary focus: {d.PRIMARY_FOCUS}
- Bounded practice: {d.BOUNDED_PRACTICE}
- Inherited activation negatives: {d.INHERITED_NEGATIVES}
- New x1 operational negatives retained so far: {d.STARTUP_NEGATIVES}
- Current effective negative count: {d.INHERITED_NEGATIVES + d.STARTUP_NEGATIVES}
- Terminal verdict: `NOT_READY_FOR_STAGE_20`

X2 may begin only after this dedicated freeze is committed, pushed, clean, and local/upstream/tracking/fresh-live equal.
""",
    )
    status_counts = Counter(source["status"] for source in d.SOURCES)
    write_json(
        "sources/source-ledger.json",
        {
            "schema": "ghc.family.source-ledger.v1",
            "phase": d.PHASE,
            "count": len(d.SOURCES),
            "status_counts": dict(sorted(status_counts.items())),
            "real_data_rows": 0,
            "participants_or_operators": 0,
            "production_identity_events": 0,
            "authority_decisions": 0,
            "sources": d.SOURCES,
            "boundary": "Sources define requirements and status; citations are not observations, participant evidence, production readiness, authority, or independent review.",
        },
    )
    write_text("sources/source-ledger.md", source_ledger_markdown())

    portfolios = {
        "safe_now": portfolio_rows(d.SAFE_NOW, "SAFE", "x2_bounded_safe_now", "safe_now"),
        "candidate": portfolio_rows(d.CANDIDATES, "CAND", "x2_bounded_candidate", "candidate"),
        "skills": portfolio_rows(d.SKILLS, "SKILL", "x2_phase_local_skill", "candidate_skill_build"),
        "runners": portfolio_rows(d.RUNNERS, "RUN", "x2_family_current_runner", "candidate_runner_build"),
        "clean_fix_refine": portfolio_rows(d.CLEAN_FIX_REFINE, "CFR", "x2_additive_cleanup", "safe_now_additive_cleanup"),
    }
    portfolio_counts = {key: len(value) for key, value in portfolios.items()}
    required_counts = {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40}
    if portfolio_counts != required_counts:
        raise RuntimeError(f"portfolio floors not met exactly: {portfolio_counts}")
    write_json(
        "portfolios/expanded-portfolio-plan.json",
        {
            "schema": "ghc.family.v651-v2.expanded-portfolio-plan.v1",
            "phase": d.PHASE,
            "state": "frozen_not_executed",
            "counts": portfolio_counts,
            "inherited_completion_credit": False,
            "portfolios": portfolios,
            "boundary": "X1 contains ideas and plans only. Unsafe or authority-dependent work cannot earn safe-now credit.",
        },
    )
    write_json(
        "truth/held-approval-packets.json",
        {
            "schema": "ghc.family.v651-v2.held-approvals.v1",
            "state": "inherited_visible_unexecuted",
            "exact_approval_count": 10,
            "blocked_count": 5,
            "executed_count": 0,
            "safe_now_credit": 0,
            "source": "docs/sable-rook/v651-v1/truth/held-approval-packets.json",
        },
    )
    mutation_types = ["missing_required_obligation", "wrong_type_or_domain", "unexpected_promotion_phrase", "resource_budget_overrun", "state_or_order_violation"]
    mutations = []
    for proposal in d.PROPOSALS:
        for number, mutation_type in enumerate(mutation_types, 1):
            mutations.append(
                {
                    "mutation_id": f"{proposal['proposal_id']}-MUT-{number}",
                    "proposal_id": proposal["proposal_id"],
                    "target_slug": proposal["slug"],
                    "mutation_type": mutation_type,
                    "expected_result": "rejected_or_quarantined",
                    "x1_state": "preregistered_not_executed",
                    "credit_boundary": "A future rejection is bounded guard evidence only, never complete security, scientific truth, accessibility conformance, production readiness, or authority.",
                }
            )
    write_json(
        "validation/preregistered-mutation-plan.json",
        {
            "schema": "ghc.family.v651-v2.mutation-plan.v1",
            "phase": d.PHASE,
            "count": len(mutations),
            "executed_count": 0,
            "state": "frozen_x1_only",
            "mutations": mutations,
        },
    )

    write_json(
        "environment/environment-version-receipt.json",
        {
            "schema": "ghc.family.environment-version.v1",
            "phase": d.PHASE,
            "observed_date": "2026-07-21",
            "codex_cli": "0.144.5",
            "codex_desktop": "26.715.4045.0",
            "chatgpt_desktop": "1.2026.190.0",
            "python": "3.12.10",
            "git": "2.55.0.windows.2",
            "windows_powershell": "5.1.26100.8894",
            "windows_sandbox_executable_present": False,
            "versions_verified_only": True,
            "desktop_updated": False,
            "elevated": False,
            "host_security_changed": False,
            "windows_feature_changed": False,
            "unrelated_software_installed": False,
            "rebooted": False,
        },
    )
    write_json(
        "environment/file-footprint-receipt.json",
        {
            "schema": "ghc.family.file-footprint.v1",
            "phase": d.PHASE,
            "inherited_full_checkout_files": 43560,
            "inherited_tracked_files": 43329,
            "owner_phase_files_at_activation": 0,
            "owner_rotation_threshold": 15000,
            "rotation_triggered": False,
            "d_free_bytes_at_activation": 574011318272,
            "boundary": "The inherited checkout baseline does not trigger rotation; only new Orin-generated phase files count.",
        },
    )
    write_json(
        "wellbeing/wellbeing-check.json",
        {
            "schema": "ghc.family.wellbeing-check.v1",
            "phase": d.PHASE,
            "state": "green_bounded_x1",
            "single_owner": True,
            "delegation_forbidden_and_unused": True,
            "failure_and_gap_tolerance": True,
            "stop_conditions_visible": True,
            "no_affective_pressure_override": True,
            "boundary": "A green workload receipt is not consciousness, personhood, employment, wellness diagnosis, or authority evidence.",
        },
    )
    write_json(
        "threat-model/x1-threat-model.json",
        {
            "schema": "ghc.family.threat-model.v1",
            "phase": d.PHASE,
            "assets": ["x1 freeze integrity", "negative retention", "source ancestry", "privacy exclusions", "authority reservations", "terminal route"],
            "threats": [
                {"id": "T1", "threat": "x2 work contaminates x1", "control": "dedicated freeze, exact staged review, x1-only tests"},
                {"id": "T2", "threat": "lexical novelty substitutes for mechanism review", "control": "all-920 comparison plus manual mechanism field"},
                {"id": "T3", "threat": "citation becomes observation", "control": "zero-row and source-ledger boundaries"},
                {"id": "T4", "threat": "synthetic localization becomes competence or affected-user evidence", "control": "represented class and professional/participant gates"},
                {"id": "T5", "threat": "identity fixture becomes production claim", "control": "zero keys, accounts, network events, and interoperability"},
                {"id": "T6", "threat": "structural audit becomes accessibility-complete", "control": "manual, assistive-technology, linguistic, and affected-user reservations"},
                {"id": "T7", "threat": "software matrix substitutes for legal, cultural, or Maori authority", "control": "exact gate and noncompensation assertions"},
                {"id": "T8", "threat": "failed attempt disappears after recovery", "control": "append-only Method Flow fail and pass witnesses"},
                {"id": "T9", "threat": "private routing or local paths enter public artifacts", "control": "five-class staged and final scanning"},
                {"id": "T10", "threat": "prepared baton is mistaken for sent", "control": "route remains prepared_not_sent until one acknowledged exact-title send"},
            ],
            "residual_boundary": "This is a bounded threat model, not exhaustive security, privacy completeness, production certification, legal review, or independent audit.",
        },
    )
    write_json(
        "tooling/phase-tool-selection.json",
        {
            "schema": "ghc.family.phase-tool-selection.v1",
            "phase": d.PHASE,
            "selected": [
                {"skill": "ghc-family-index", "purpose": "phase-scoped family-current inventory and routing precedence"},
                {"skill": "ghc-family-method-flow-state", "purpose": "append-only failure, workaround, witness, and recommendation ledger"},
                {"skill": "ghc-family-workflow-plan-refinement", "purpose": "sanitized route and budget normalization without activation"},
                {"skill": "ghc-family-reflection-remaster", "purpose": "read-only overlap and compatibility audit"},
                {"skill": "skill-creator", "purpose": "x2 phase-local skill packaging and validation"},
            ],
            "reflection_inventory_count": 3027,
            "reflection_scoped_issues": 0,
            "disposition": "reviewed_current_no_semantic_free_churn",
            "caller_compatibility_preserved": True,
        },
    )
    write_json(
        "orchestration/x1-phase-state.json",
        {
            "schema": "ghc.family.phase-state.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "state": "x1_frozen_candidate",
            "source_head": d.SOURCE_HEAD,
            "x2_started": False,
            "terminal_route": "prepared_not_sent",
            "successor": "Tamar Vey",
            "successor_phase": "v651-v3",
            "boundary": "This state file is not activation, delivery, identity continuity, or delegated authority.",
        },
    )
    write_json(
        "truth/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v1",
            "phase": d.PHASE,
            "sealed_inherited": 6563,
            "external_inherited": 2,
            "v651_v2_x1_operational": d.STARTUP_NEGATIVES,
            "preregistered_mutations_executed": 0,
            "effective_count": d.INHERITED_NEGATIVES + d.STARTUP_NEGATIVES,
            "erasures": 0,
            "new_operational_negatives": [
                {"negative_id": "V6512-X1-N01", "summary": "Stale memory registry filename; recovered with one unique suffix match."},
                {"negative_id": "V6512-X1-N02", "summary": "Grouped parallel source audit timed out; recovered with isolated no-profile probes."},
                {"negative_id": "V6512-X1-N03", "summary": "One-process-per-blob manifest replay exceeded its wrapper; recovered with tree maps and framed blob reads."},
                {"negative_id": "V6512-X1-N04", "summary": "First x1 suite expected a nonexistent top-level workflow key and an outdated reflection count key."},
                {"negative_id": "V6512-X1-N05", "summary": "First x1 suite compared an equivalent same-owner boundary phrase case-sensitively."},
                {"negative_id": "V6512-X1-N06", "summary": "A resumed shell started in the .codex project root rather than the owned Git worktree; no repository command or mutation ran before recovery."},
                {"negative_id": "V6512-X1-N07", "summary": "The Method Flow validator was first given an unsupported --json-output flag after M05 state changes had already succeeded; recovery uses the documented --receipt flag."},
                {"negative_id": "V6512-X1-N08", "summary": "A rebuilt x1 suite retained an obsolete exact Method Flow count and failed after legitimate later x1 recoveries expanded the append-only ledger."},
                {"negative_id": "V6512-X1-N09", "summary": "The first lifecycle-safe correction still required M07's passing-witness count before that witness could be appended, creating a circular acceptance threshold."},
            ],
        },
    )
    write_json(
        "truth/open-gap-register.json",
        {
            "schema": "ghc.family.open-gap-register.v1",
            "phase": d.PHASE,
            "inherited_effective_count": d.INHERITED_OPEN_GAPS,
            "current_effective_count": d.INHERITED_OPEN_GAPS,
            "planned_new_open_gap": "V6512-P05",
            "planned_not_observed": True,
            "silently_closed": 0,
        },
    )
    write_json(
        "truth/exact-gate-register.json",
        {
            "schema": "ghc.family.exact-gate-register.v1",
            "phase": d.PHASE,
            "inherited_effective_count": d.INHERITED_EXACT_GATES,
            "current_effective_count": d.INHERITED_EXACT_GATES,
            "planned_new_exact_gate": "V6512-P10",
            "planned_not_observed": True,
            "silently_closed": 0,
        },
    )
    write_json(
        "truth/x1-phase-truth.json",
        {
            "schema": "ghc.family.v651-v2.x1-truth.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_head": d.SOURCE_HEAD,
            "frozen_proposals_before": d.PRIOR_FROZEN,
            "frozen_proposals_after": d.PRIOR_FROZEN + len(d.PROPOSALS),
            "proposal_count": len(d.PROPOSALS),
            "observed_outcomes": None,
            "x2_started": False,
            "effective_negatives": d.INHERITED_NEGATIVES + d.STARTUP_NEGATIVES,
            "open_gaps": d.INHERITED_OPEN_GAPS,
            "exact_gates": d.INHERITED_EXACT_GATES,
            "full_repository_suite_run": False,
            "independent_reproduction_claimed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "terminal_route": "prepared_not_sent",
        },
    )
    write_text("overview/integrated-overview.md", overview_text())
    write_text("reports/x1-accessible-static-report.html", static_report())

    documents = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.casefold() not in {".md", ".html"}:
            continue
        words = len(re.findall(r"\b[\w'-]+\b", path.read_text(encoding="utf-8")))
        documents.append({"path": path.relative_to(REPO).as_posix(), "words": words, "cap": 6000, "within_cap": words <= 6000})
    if not all(row["within_cap"] for row in documents):
        raise RuntimeError("x1 document cap exceeded")
    write_json(
        "validation/x1-document-cap-receipt.json",
        {
            "schema": "ghc.family.document-cap.v1",
            "phase": d.PHASE,
            "documents": documents,
            "all_within_cap": True,
            "baton_exception_used": False,
        },
    )
    owned_files = sum(1 for path in ROOT.rglob("*") if path.is_file())
    write_json(
        "validation/x1-owner-file-threshold.json",
        {
            "schema": "ghc.family.owner-file-threshold.v1",
            "phase": d.PHASE,
            "owner_generated_files": owned_files + 1,
            "threshold": 15000,
            "within_threshold": owned_files + 1 < 15000,
            "inherited_baseline_excluded": True,
        },
    )
    write_json(
        "validation/x1-build-receipt.json",
        {
            "schema": "ghc.family.v651-v2.x1-build.v1",
            "phase": d.PHASE,
            "proposal_count": len(d.PROPOSALS),
            "prior_count": len(inherited),
            "frozen_after": len(inherited) + len(d.PROPOSALS),
            "source_count": len(d.SOURCES),
            "portfolio_counts": portfolio_counts,
            "mutation_plan_count": len(mutations),
            "novelty_passed": True,
            "x2_artifacts_written": False,
            "observed_outcomes_written": False,
            "valid": True,
        },
    )
    print(json.dumps({"phase": d.PHASE, "proposals": 20, "frozen_after": 940, "sources": len(d.SOURCES), "mutations": len(mutations), "x2_started": False, "valid": True}))


if __name__ == "__main__":
    main()
