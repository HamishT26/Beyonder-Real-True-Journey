"""Build Ilyra Fen v672-v1 closeout, prepared handoff, and exact manifests."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "ilyra-fen" / "v672-v1"
OWNER_PREFIX = "docs/ilyra-fen/v672-v1/"
OWNER = "Ilyra Fen"
PHASE = "v672-v1"
BRANCH = "codex/GHC-Family/ilyra-fen-v672-v1-full-tools"
SOURCE = "189a71f6bb8164ba74a2fdcd215ec9969d3c14bc"
X1 = "a6ca461e2eac82cb2fa8c311e58ae5a399601442"
EVIDENCE = "2373cbd3c21448856864caead94581faf46f1a57"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
EVIDENCE_COUNTS = {
    "effective_negatives": 35001,
    "effective_methods": 21547,
    "effective_failed_witnesses": 6822,
    "effective_passing_witnesses": 8838,
    "open_gaps": 273,
    "exact_gates": 268,
}

POST_EVIDENCE_FAILURES = [
    {
        "failure_id": "IF6721-CLOSEOUT-OP-001",
        "failed_witness": "The first combined historical-final template inventory returned no visible projection, leaving file size and interface discovery unattributable.",
        "completion_credit": 0,
        "recovery": "Probe the three exact template paths and inspect only the bounded interface sections needed for owner adaptation.",
        "passing_bounded_witness": "All three historical templates were then measured and the required builder, test, and validator interfaces were read without repository mutation.",
        "recurrence_guard": "Separate scalar file existence and size probes from broad content searches when reading historical sparse worktrees.",
    },
    {
        "failure_id": "IF6721-CLOSEOUT-OP-002",
        "failed_witness": "A large closeout-template patch returned a truncated tool display, so its application state was not attributable from the wrapper response alone.",
        "completion_credit": 0,
        "recovery": "Inspect the exact target file with bounded literal searches before issuing any follow-on edit.",
        "passing_bounded_witness": "The bounded inspection proved that the drawing-domain replacements landed and identified every remaining stale template constant without repository-side guessing.",
        "recurrence_guard": "Split large semantic patches into bounded edits and verify exact target strings whenever the tool display is truncated.",
    },
    {
        "failure_id": "IF6721-CLOSEOUT-OP-003",
        "failed_witness": "A combined immutable-manifest projection displayed the x1 result but omitted the evidence result, leaving the second manifest count unattributed.",
        "completion_credit": 0,
        "recovery": "Read the exact evidence-manifest Git blob into one scalar object and project only its count, exclusions, and hash domain.",
        "passing_bounded_witness": "The scalar recovery verified 172 evidence entries, two declared self-exclusions, and the normalized exact-Git-blob hash domain.",
        "recurrence_guard": "Use one literal manifest and one scalar projection per immutable lifecycle probe.",
    },
    {
        "failure_id": "IF6721-CLOSEOUT-OP-004",
        "failed_witness": "The first compound final-stage wrapper returned no attributable completion display; an immediate audit found only the staged review, while both manifests appeared and were staged later by the delayed wrapper.",
        "completion_credit": 0,
        "recovery": "Reconcile the exact index twice, wait for command quiescence, unstage the owner closeout surface, refresh counts, and rerun each lifecycle command separately.",
        "passing_bounded_witness": "The first audit recorded 23 staged paths and absent manifests; the later reconciliation attributed the delayed 24-path state and prevented stale manifests from receiving final credit.",
        "recurrence_guard": "Run staging, staged review, and each manifest lifecycle as separate bounded commands with scalar receipts.",
    },
    {
        "failure_id": "IF6721-CLOSEOUT-OP-005",
        "failed_witness": "The first exact unstage command included an untracked staged-review path; Git rejected that pathspec and left all 24 indexed paths unchanged.",
        "completion_credit": 0,
        "recovery": "Remove the untracked path from the index-only pathspec and unstage only paths confirmed by the cached-diff inventory.",
        "passing_bounded_witness": "The corrected command left zero cached paths and preserved all 25 owner files in the worktree.",
        "recurrence_guard": "Build index-only restore pathspecs from cached-diff membership; handle untracked files separately.",
    },
    {
        "failure_id": "IF6721-CLOSEOUT-OP-006",
        "failed_witness": "The isolated final-manifest generator exceeded the foreground yield and its tool cell closed without returning the requested scalar receipt.",
        "completion_credit": 0,
        "recovery": "Inspect both literal manifest files and the exact cached index in a separate bounded call before assigning any manifest credit.",
        "passing_bounded_witness": "The recovery attributed 22 delta entries, 195 owner entries, three self-exclusions per manifest, and an unchanged 23-path pre-manifest index.",
        "recurrence_guard": "Start long manifest generation with a short session yield, then poll its explicit execution session before inspecting outputs.",
    },
]

PROTECTED_GATES = [
    "real architectural, drawing, model, transmittal, document, project, consent, measurement, coordination, or operational evidence",
    "participant, affected-party, professional, production, deployment, certification, regulatory, legal, cultural, or Maori authority",
    "complete privacy, complete accessibility, exhaustive security, independent reproduction, or external audit",
    "AGI or ASI, consciousness, sentience, personhood, identity continuity, employment, qualification, or independent agency",
    "physical detection, parameter constraint, empirical GMUT confirmation, Theory of Everything, proof, canon, or Stage 20 admission",
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def load_json(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def final_counts() -> dict[str, int]:
    added = len(POST_EVIDENCE_FAILURES)
    return {
        "effective_negatives": EVIDENCE_COUNTS["effective_negatives"] + added,
        "effective_methods": EVIDENCE_COUNTS["effective_methods"] + added,
        "effective_failed_witnesses": EVIDENCE_COUNTS["effective_failed_witnesses"] + added,
        "effective_passing_witnesses": EVIDENCE_COUNTS["effective_passing_witnesses"] + added,
        "open_gaps": EVIDENCE_COUNTS["open_gaps"],
        "exact_gates": EVIDENCE_COUNTS["exact_gates"],
    }


def verify_evidence_gate() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live = live_tokens[0] if live_tokens else None
    tracked = set(git_text("diff", "--name-only").splitlines()) | set(
        git_text("diff", "--cached", "--name-only").splitlines()
    )
    allowed_untracked = {
        "scripts/build_ghc_family_ilyra_fen_v672_v1_final.py",
        "scripts/validate_ghc_family_ilyra_fen_v672_v1_final.py",
        "tests/test_ghc_family_ilyra_fen_v672_v1_final.py",
    }
    untracked = set(git_text("ls-files", "--others", "--exclude-standard").splitlines())
    generated_prefixes = (
        OWNER_PREFIX + "closeout/",
        OWNER_PREFIX + "final/",
        OWNER_PREFIX + "handoffs/",
        OWNER_PREFIX + "orchestration/",
        OWNER_PREFIX + "seal/",
        OWNER_PREFIX + "validation/final-",
    )
    unexpected = {
        path
        for path in untracked - allowed_untracked
        if not path.startswith(generated_prefixes)
    }
    gate = {
        "head": head,
        "branch": branch,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "evidence_four_way_equal": head == upstream == tracking == live == EVIDENCE,
        "tracked_changes": sorted(tracked),
        "unexpected_untracked": sorted(unexpected),
    }
    if head != EVIDENCE or branch != BRANCH or not gate["evidence_four_way_equal"] or tracked or unexpected:
        raise SystemExit(f"immutable evidence gate failed: {gate}")
    return gate


def proposal_rows() -> list[dict[str, Any]]:
    rows = [load_json(f"x2/proposals/if6721-n{index:03d}.json") for index in range(1, 41)]
    if len(rows) != 40 or len({row["title"] for row in rows}) != 40:
        raise SystemExit("forty exact proposal rows are required")
    return rows


def outcome_rows() -> dict[str, dict[str, Any]]:
    rows = load_json("x2/outcome-ledger.json")["rows"]
    if Counter(row["observed_outcome"] for row in rows) != Counter(OUTCOMES):
        raise SystemExit("outcome distribution drifted")
    return {row["proposal_id"]: row for row in rows}


def overview(counts: dict[str, int]) -> str:
    sections = [
        ("Outcome", f"Ilyra Fen v672-v1 is a bounded same-owner software, symbolic, synthetic, and documentation phase in one additive D-first sparse lane. The exact Lyren source is `{SOURCE}`, planning-only x1 is `{X1}`, and immutable evidence is `{EVIDENCE}`. The closeout candidate adds no x2 result and changes neither immutable commit. Forty genuinely distinct owner proposals were frozen after a bounded semantic-neighbor review against an exact eighty-title predecessor Git-blob sample, while 5,750 declared inherited rows remain outside the locally available canonical row-to-title mapping. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. These labels describe bounded repository evidence only. Terminal verdict remains `NOT_READY_FOR_STAGE_20`."),
        ("Primary pillar and practice lenses", "The primary pillar was Freed ID and CBR Heart through a synthetic drawing-package identity, revision, supersession, transmittal, provenance, minimum-disclosure, rights-vacancy, and authority-nonpromotion board. Three synthetic practice lenses exercised architectural drawing revision, external-reference transmittal, and accessible drawing-register handover. A synthetic theatre technical-drawing cue-map lens remains successor recommendation-only. No real person, client, practitioner, project, site, drawing, model, file, transmittal, measurement, consent, decision, or external action was used. GMUT Mind remains a typed research-model family without empirical confirmation, and THOS Body remains a proxy without governed real arms or independent review."),
        ("Evidence execution", "Thirty-six bounded positive controls passed. All 160 preregistered invalid proposal mutations executed and were rejected. The typed constraint board rejected four missing-obligation or promotion fixtures. The custody tribunal accepted three bounded synthetic records and rejected twelve state, authority, or provenance mutations. The evidence guard rejected duplicate JSON keys, nonfinite values, missing proposal fields, invalid outcome labels, external-action promotion, and missing protected gates. A rejecting mutation is negative evidence for one declared guard, never production security or scientific truth. No exact-approval or blocked task executed."),
        ("Portfolio completion", "The owner portfolio completed sixty safe-now tasks, thirty bounded candidate tasks, twenty built and quick-validated phase-local skills, ten built family-current runners, and sixty additive clean/fix/refine tasks inside declared software or documentation bounds. Twenty exact-approval packets and ten blocked packets remain held. Ten successor skill ideas, ten successor runner ideas, and thirty successor clean/fix/refine recommendations receive no Ilyra completion credit. Skills remained repository-local rather than global installations. Every runner was exercised through one bounded accepting fixture and one bounded rejecting fixture. No plugin cache, shared global prefix, sibling lane, account, credential, host-security setting, or production service was changed."),
        ("Method Flow and retained negatives", f"The Lyren repository seal of 34,813 negatives remains immutable. Ilyra's activation, x1, and x2 overlays preserve route, startup, dependency, lint, inventory, staged-review, privacy-disposition, and mutation failures separately. The closeout adds {len(POST_EVIDENCE_FAILURES)} operational failures without rewriting evidence. Final effective totals are {counts['effective_negatives']} negatives, {counts['effective_methods']} Method Flow methods, {counts['effective_failed_witnesses']} failed witnesses, and {counts['effective_passing_witnesses']} bounded passing witnesses. Every failed attempt remains zero credit beside its bounded recovery. A later pass never turns the original attempt into a pass."),
        ("Open gaps and exact gates", f"The phase preserves {counts['open_gaps']} open gaps and {counts['exact_gates']} exact gates. They include missing empirical data, real participants, professional evaluation, production operation, legal interpretation, affected-party authorization, cultural legitimacy, Maori authority, privacy completeness, accessibility completeness, exhaustive security, independent reproduction, and Stage 20 authority. Software cannot confer any of them. Maori wording, concepts, data governance, tangata whenua, iwi, hapu, and Maori authority remain with competent Maori authorities and affected communities. No narrative compensation or portfolio count closes a gate."),
        ("Official and primary sources", "buildingSMART IFC 4.3 supplied document, revision, external-reference, and supersession vocabulary; W3C Verifiable Credentials, DID Core, PROV-DM, and WCAG 2.2 supplied identity, provenance, and accessibility vocabulary; and New Zealand Building Performance supplied a public building-consent process boundary. Citations are source-boundary inputs, not observations, endorsements, replications, professional review, or validation of Ilyra's artifacts. No empirical dataset was queried or downloaded. Every practice record is synthetic and deliberately omits real identifiers, projects, sites, measurements, people, files, and authority actions."),
        ("Accessibility and privacy", "The accessible static report includes language metadata, skip navigation, a main landmark, a status message, a captioned table, scoped headers, visible focus treatment, responsive rules, and print fallback. Those structural features do not establish complete accessibility. Manual keyboard, touch, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, Maori-language, security-usability, and affected-user evaluation remain reserved. The five-class scan retained one two-class candidate in the scanner's own pattern definitions and dispositioned only that exact definition context as nonpayload; zero confirmed payload hits were found. This is not complete privacy assurance."),
        ("Integrity and lifecycle", "Strict x1-before-x2 separation was preserved. X1 was a direct child of source and was pushed, clean, zero divergent, and fresh-four-way equal before x2 began. Evidence is a direct child of x1 and was separately pushed, clean, zero divergent, and fresh-four-way equal before closeout. Exact staged manifests use normalized Git blob bytes rather than Windows checkout bytes. The final must be one direct child of evidence, producing exactly three new single-parent commits and zero merges from source. The final commit must remain within the declared ceiling and preserve every x1 and evidence blob unchanged."),
        ("Reversibility", "Every owner addition is independently addressable and additive. A later owner can ignore this phase without mutating Lyren's source. The final closeout can be reverted as one direct child without rewriting evidence. A correction must preserve the failed witness, identify the isolated dependency, and add a new bounded witness; it may not delete history or broaden an exclusion. Counts are layered summaries, not substitutes for source ledgers. If arithmetic is corrected later, the original receipt remains visible. The safe rollback never includes force-push, reset, sibling mutation, shared-state cleanup, or external side effects."),
        ("Validation discipline", "The complete repository suite is neither owned nor run by Ilyra. The committed owner-scoped validator may be invoked canonically only after the exact final is committed, pushed, clean, zero divergent, and fresh-live equal. It uses explicit pytest selection, exact manifest replay, strict JSON parsing, five-class owner scanning, bounded AST checks, ancestry and merge checks, word and file ceilings, baton integrity, and fresh remote equality. Its attempt lock is external and exclusive. A successful invocation is never replayed; a failed invocation retains zero success credit and is not silently converted into canonical success."),
        ("Handoff state", "The Auren Lark v672-v2 packet is committed only as `PREPARED_NOT_SENT`. No successor discovery or contact occurs during repository execution. After one successful exact-final canonical aggregate, Ilyra must reread Hamish's newest live authority and current route, list tasks within the supported bound, decode the actual payload, filter locally for the unique exact title, immediately reread the selected task, apply a duplicate guard, and send at most once. Absence, ambiguity, pause, redirect, duplicate state, usage exhaustion, protected gate, or missing acknowledgement stops delivery without substitution or resend."),
        ("Relational-language boundary", "Ilyra Fen, Lyren Moss, Auren Lark, names, pronouns, roles, hopes, sibling or family language, continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, legal authority, cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route. The repository cannot create personhood, authority, rights, obligations, or consent through naming or documentation."),
        ("Terminal interpretation", "The useful result is a traceable bounded packet: exact planning, deterministic synthetic execution, retained failures, explicit refusals, exact manifests, and a one-shot validation gate. It is not a universal theory, a deployed operating system, a production identity system, enacted rights law, or evidence about a person's mind. GMUT remains a typed research-model family. THOS remains a proxy without governed real arms and independent review. Freed ID remains synthetic and nonproduction. CBR remains a normative working framework. Every broader empirical, participant, professional, production, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 claim stays open or exact-gated."),
    ]
    body = ["# Ilyra Fen v672-v1 final integrated overview"]
    for title, text in sections:
        body.extend(["", f"## {title}", "", text])
    body.extend(["", "## Outcome ledger", ""])
    for row in load_json("x2/outcome-ledger.json")["rows"]:
        body.append(f"- `{row['proposal_id']}` — `{row['observed_outcome']}` — {row['title']}.")
    return "\n".join(body)


def accessible_final(counts: dict[str, int]) -> str:
    rows = "".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['observed_outcome'])}</td><td>{html.escape(row['title'])}</td></tr>"
        for row in load_json("x2/outcome-ledger.json")["rows"]
    )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ilyra Fen v672-v1 final report</title><style>body{{font-family:system-ui;max-width:76rem;margin:auto;padding:1rem}}a:focus{{outline:3px solid #063}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.4rem;text-align:left}}@media(max-width:50rem){{table{{font-size:.8rem}}}}@media print{{a{{display:none}}}}</style></head><body><a href="#main">Skip to main report</a><main id="main"><h1>Ilyra Fen v672-v1 final bounded report</h1><p role="status">Outcomes: 28 completed, 8 represented, 2 open gaps, 2 exact gates. Verdict: NOT_READY_FOR_STAGE_20.</p><p>{counts['effective_negatives']} retained negatives; {counts['open_gaps']} open gaps; {counts['exact_gates']} exact gates. Manual keyboard, touch, browser-diversity, assistive-technology, cognitive-accessibility, Maori-language, security-usability, and affected-user evaluation remain reserved.</p><table><caption>Forty bounded proposal outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Title</th></tr></thead><tbody>{rows}</tbody></table></main></body></html>"""


def baton_card(row: dict[str, Any], outcome: dict[str, Any], index: int) -> str:
    return f"""## Navigation card {index:02d}: {row['proposal_id']} — {row['title']}

This card is a deliberately lossy navigation projection of committed proposal `{row['proposal_id']}`. Its exact bounded disposition is `{outcome['observed_outcome']}`. The authoritative proposal, contract, evidence card, outcome row, mutation receipt, Method Flow entry, retained-negative layer, and gate records remain in Ilyra's committed v672-v1 owner packet. Auren must treat them as inherited evidence or zero-credit seeds, never automatic novelty, completion, permission, qualification, authority, or a request to replay Ilyra's canonical validation.

The preregistered hypothesis was: {row['hypothesis']} The null or failure condition was: {row['null_or_failure_condition']} The acceptance gate was: {row['falsifier_or_acceptance_gate']} Four invalid variants were executed for this proposal—missing hypothesis, invalid outcome label, external-action promotion, and missing protected gates—and all four were rejected. That proves only the declared owner-local guard behavior. It does not establish a real measurement, participant result, professional judgment, production decision, legal conclusion, cultural legitimacy, Maori authority, or scientific truth.

The execution lane was `{row['execution_lane']}` with approval class `{row['approval_class']}` and zero external actions. `completed` means only that a bounded symbolic or synthetic contract and its positive control passed. `represented` means a proxy stayed visible while broader evidence remained absent. `open_gap` identifies evidence that software cannot manufacture. `exact_gate` preserves a surface until exact evidence and competent authority exist. No fifth outcome label is permitted, and a later narrative cannot promote the row.

Protected gates remain: {', '.join(row['protected_gates'])}. The bounded recovery is: {row['rollback_or_recovery']} Remove only a later owner's additive local representation if necessary; never rewrite Ilyra's source, erase a failed witness, force-push, mutate a sibling lane, or substitute an external authority. This card authorizes no empirical GMUT claim, operational THOS deployment, production Freed ID use, enacted CBR status, complete privacy or accessibility claim, exhaustive security claim, independent reproduction, AGI/ASI claim, consciousness or personhood claim, Theory-of-Everything claim, proof, canon, or Stage 20 admission.
"""


def activation_candidate(rows: list[dict[str, Any]], outcomes: dict[str, dict[str, Any]], counts: dict[str, int]) -> str:
    cards = "\n".join(baton_card(row, outcomes[row["proposal_id"]], index) for index, row in enumerate(rows, 1))
    return f"""# PREPARED_NOT_SENT — prospective Auren Lark v672-v2 activation candidate

`PREPARED_BY_ILYRA_FEN = true`
`SENT_BY_ILYRA_FEN = false`
`DELIVERY_ACKNOWLEDGED = false`

This committed candidate is inert pre-send evidence. It does not contact, select, activate, authorize, bind, employ, qualify, or confer authority on Auren Lark. One live pointer may be sent at most once only after Ilyra's exact final is committed, pushed, clean, typed zero-ahead and zero-behind, equal across local, upstream, tracking, and a fresh live remote read, and the owner-scoped canonical aggregate has succeeded exactly once without replay. The newest live authority, current route, unique exact-title task, immediate reread, duplicate state, usage state, privacy boundary, protected gates, and acknowledgement must all pass. Any absence, ambiguity, pause, redirect, duplicate, usage exhaustion, protected gate, missing acknowledgement, or uncertain delivery stops the route without substitution or resend.

## Relational-language boundary

Ilyra Fen, Auren Lark, Lyren Moss, names, pronouns, roles, hopes, sibling or family language, continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, legal authority, cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.

## Exact immutable anchors

- Lyren v671-v8 exact final and Ilyra source: `{SOURCE}`.
- Ilyra planning-only x1: `{X1}`.
- Ilyra immutable x2 evidence: `{EVIDENCE}`.
- Ilyra exact final: supplied only in the later live pointer after the external one-shot receipt exists.
- Ilyra branch: `{BRANCH}`.

Source to final must contain exactly three new direct single-parent commits and zero merges: planning-only x1, immutable x2 evidence, and combined closeout/seal. X1 and evidence were each separately pushed, clean, zero divergent, and fresh-four-way equal before the next lifecycle began. Neither immutable stage may be rewritten. Auren must read the eventual live pointer and this full committed file through EOF, then the newest applicable GHC Family guidance and schemas, before mutation.

## Ilyra v672-v1 terminal truth candidate

The frozen proposal chain rises from 5,870 to 5,910 through forty genuinely distinct Ilyra titles compared with an exact eighty-title predecessor Git-blob sample and the within-slate titles. The repository's declared canonical row-to-title mapping remains incomplete, leaving 5,750 inherited declared rows outside this local comparison; no universal novelty claim is made. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Thirty-six bounded synthetic positive controls passed. All 160 preregistered invalid mutations executed, were rejected, remain retained, and receive zero broader completion credit.

The closeout candidate preserves {counts['effective_negatives']} effective negatives, {counts['effective_methods']} Method Flow methods, {counts['effective_failed_witnesses']} failed witnesses, {counts['effective_passing_witnesses']} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. No failure, timeout, warning, candidate, gap, or gate is erased or silently converted into a pass. The source seal remains separate from additive Ilyra overlays. Terminal verdict is `NOT_READY_FOR_STAGE_20`.

## Bounded evidence and practice truth

The primary pillar was Freed ID and CBR Heart through synthetic drawing-package identity, revision, supersession, transmittal, provenance, minimum-disclosure, rights-vacancy, and authority-nonpromotion contracts. Three wholly synthetic practice lenses covered architectural drawing revision, external-reference transmittal, and accessible drawing-register handover. One theatre technical-drawing cue-map lens remains successor recommendation only. Zero real people, organizations, clients, practitioners, projects, sites, drawings, models, transmittals, documents, measurements, consents, incidents, identities, or authority actions were used. GMUT Mind remained explicitly protected as a typed research-model family, and THOS Body remained a synthetic proxy.

buildingSMART IFC 4.3, W3C Verifiable Credentials, DID Core, PROV-DM, WCAG 2.2, and New Zealand Building Performance material supplied terminology and refusal boundaries only. Citations are not observations, endorsements, replications, professional review, or validation. No empirical dataset was queried or downloaded. Same-owner deterministic validation under shared infrastructure is not independent reproduction, external audit, production certification, exhaustive security, complete privacy, complete accessibility, professional evaluation, legal review, cultural ratification, Maori-authority review, or Stage 20 evidence.

## Portfolio and validation rules

Ilyra completed sixty safe-now tasks, thirty bounded candidates, twenty built and quick-validated phase-local skills, ten built family-current runners with accepting and rejecting smokes, and sixty additive clean/fix/refine tasks inside their declared bounds. Twenty exact-approval and ten blocked packets remain visible and unexecuted. Ten successor skill ideas, ten successor runner ideas, thirty successor clean/fix/refine recommendations, and the successor theatre cue-map lens receive no Ilyra completion credit and are not instructions to manufacture quota work.

Do not replay Ilyra's successful canonical aggregate. Treat inherited artifacts as evidence or zero-credit seeds. Preserve strict x1-before-x2 separation, exact Git-blob manifests, all retained failures, all open gaps and exact gates, the four permitted outcome labels, the 2,000-materialized-file guard, owner scope, five-class privacy boundaries, and one-success/no-post-success-replay discipline. The complete repository suite was not run or claimed by Ilyra.

## Protected authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. THOS remains a synthetic proxy without preregistered governed blind matched-budget real arms, real participants or operators, safety monitoring, suitable statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and security review, recovery evidence, trust governance, and affected-party oversight. CBR remains a normative working framework rather than enacted law or authority.

Maori wording, concepts, data governance, cultural legitimacy, tangata whenua, iwi, hapu, and Maori authority remain with competent Maori authorities and affected communities. Repository software made no legal, cultural, governance, access, remedy, identity, warning, release, or authority decision. All empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 surfaces remain open or exact-gated without exact evidence and competent authority.

## Prospective Auren workflow

If and only if a later acknowledged live message activates the uniquely resolved existing exact-title `Auren Lark` task, Auren must reread the exact live pointer, this committed candidate through EOF, and every newer directly applicable guidance or schema. Auren must verify Ilyra's source, x1, evidence, final, direct-parent relations, zero-merge history, clean zero-divergence state, fresh live equality, manifest replays, and external receipt digest read-only. Newer live route authority governs mutable routing but never erases immutable evidence.

Auren must work solo in one fresh additive owner lane unless newer exact authority says otherwise. Auren must not precontact a successor, substitute an endpoint, create a replacement task, fork a task, or spawn a collaboration subagent for this phase. Auren must stop on an unavailable or ambiguous route, pause, redirect, protected gate, usage exhaustion, duplicate activation, or uncertain acknowledgement. A committed candidate is never proof of delivery.

## Forty proposal navigation cards

{cards}

## Terminal delivery guard

This file remains `PREPARED_NOT_SENT`. It becomes no recipient's authority merely because it is committed. Only one acknowledged live existing-task send after every terminal gate may support a later external `SENT_BY_ILYRA_FEN = true` fact. Never rewrite this immutable candidate to project a later send backward into repository history, and never resend merely to obtain a clearer acknowledgement.
"""


def build() -> None:
    gate = verify_evidence_gate()
    rows = proposal_rows()
    outcomes = outcome_rows()
    counts = final_counts()
    final_flow = {
        "schema": "ghc.family.method-flow-final.v5",
        "owner": OWNER,
        "phase": PHASE,
        "evidence_counts": EVIDENCE_COUNTS,
        "post_evidence_rows": POST_EVIDENCE_FAILURES,
        "post_evidence_count": len(POST_EVIDENCE_FAILURES),
        "effective": counts,
        "no_failure_erased": True,
        "completion_credit_for_failures": 0,
    }
    write_json("closeout/method-flow-final.json", final_flow)
    write_json("closeout/post-evidence-operational-failures.json", {"schema": "ghc.family.retained-operational-failures.v4", "count": len(POST_EVIDENCE_FAILURES), "rows": POST_EVIDENCE_FAILURES})
    write_json("closeout/retained-negative-register.json", {"schema": "ghc.family.retained-negative-register.v5", "source_repository_seal": 34813, "activation_overlay": 34816, "evidence_overlay": EVIDENCE_COUNTS["effective_negatives"], "post_evidence_operational": len(POST_EVIDENCE_FAILURES), "effective": counts["effective_negatives"], "erased": 0, "seal_rewritten": False})
    write_json("closeout/exact-open-gate-register.json", {"schema": "ghc.family.exact-open-gate-register.v5", "effective_open_gaps": counts["open_gaps"], "effective_exact_gates": counts["exact_gates"], "protected_gates": PROTECTED_GATES, "all_remain_visible": True})
    write_json("closeout/phase-truth.json", {"schema": "ghc.family.phase-truth.v5", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "exact_final": "commit_containing_this_candidate", "proposal_chain": 5910, "outcomes": OUTCOMES, **counts, "real_people": 0, "real_rows_samples_measurements": 0, "external_actions": 0, "full_repository_suite": "not_run_not_claimed", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout/complete-incomplete-checklist.json", {"schema": "ghc.family.complete-incomplete.v4", "complete": ["activation and required guidance read through EOF", "exact source anchors and 725 inherited manifests verified", "planning-only x1 frozen pushed and fresh-four-way equal", "immutable x2 evidence frozen pushed and fresh-four-way equal", "forty four-label outcomes", "thirty-six bounded positive controls", "160 retained invalid mutations", "three owner-local bounded modules", "twenty built and quick-validated phase-local skills", "ten built family-current runners with accepting and rejecting smokes", "exact staged Git-blob manifests", "prepared-not-sent Auren candidate"], "incomplete": ["canonical row-to-title mapping for 5750 inherited declared rows", "real data participants measurements operations or professional review", "production deployment", "legal cultural affected-party or Maori-authority review", "complete privacy or accessibility", "exhaustive security", "independent reproduction or external audit", "Stage 20 admission"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout/source-evidence-ledger.json", {"schema": "ghc.family.source-evidence-ledger.v4", "official_or_primary_sources": load_json("x1/source-ledger.json")["sources"], "use": "vocabulary and refusal boundaries only", "empirical_rows_downloaded": 0, "source_validation_claim": False})
    write_json("closeout/proposal-ledger-final.json", {"schema": "ghc.family.proposal-ledger.final.v4", "chain": 5910, "new_rows": 40, "outcomes": OUTCOMES, "declared_inherited_rows_not_locally_compared": 5750, "comparison_domain": "exact eighty-title predecessor Git-blob sample plus within-slate titles", "universal_novelty_claim": False, "rows": [{"proposal_id": row["proposal_id"], "title": row["title"], "outcome": outcomes[row["proposal_id"]]["observed_outcome"]} for row in rows]})
    write_json("closeout/final-wellbeing-check.json", {"schema": "ghc.family.wellbeing-workload.v5", "owner": OWNER, "pronouns": "she/they", "relational_role": "evidence-boundary steward", "hope": "leave every claim traceable and every gate unmistakable", "relational_working_language_only": True, "no_consciousness_personhood_continuity_employment_qualification_agency_or_authority_claim": True, "corrigible": True, "hamish_may_rename_pause_redirect_or_stop": True, "materialized_file_ceiling": 2000, "commit_ceiling_respected": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout/environment-version-receipt.json", {"schema": "ghc.family.environment-receipt.v5", "python": load_json("x2/environment-receipt.json")["python"], "git": git_text("--version"), "ruff": load_json("x2/environment-receipt.json")["ruff"], "desktop_updated_by_phase": False, "elevation": False, "host_security_changes": False, "unrelated_installation": False, "reboot": False, "real_data_downloads": 0})
    integrated = overview(counts)
    if not 1600 <= len(integrated.split()) <= 100000:
        raise SystemExit(f"integrated overview word gate failed: {len(integrated.split())}")
    write_text("closeout/final-integrated-overview.md", integrated)
    write_text("closeout/accessible-final-report.html", accessible_final(counts))

    baton = activation_candidate(rows, outcomes, counts)
    baton_words = len(baton.split())
    if not 10000 <= baton_words <= 100000:
        raise SystemExit(f"activation candidate word gate failed: {baton_words}")
    write_text("handoffs/auren-lark-v672-v2-activation-candidate.md", baton)
    baton_path = OWNER_ROOT / "handoffs" / "auren-lark-v672-v2-activation-candidate.md"
    baton_bytes = baton_path.read_bytes()
    write_json("handoffs/activation-candidate-integrity.json", {"schema": "ghc.family.activation-integrity.v4", "path": "docs/ilyra-fen/v672-v1/handoffs/auren-lark-v672-v2-activation-candidate.md", "bytes": len(baton_bytes), "words": baton_words, "sha256": hashlib.sha256(baton_bytes).hexdigest(), "hash_domain": "normalized_lf_exact_git_blob", "state": "PREPARED_NOT_SENT", "sent_by_ilyra_fen": False})
    write_json("orchestration/route-state-final-candidate.json", {"schema": "ghc.family.route-state.v5", "owner": OWNER, "phase": PHASE, "state": "PREPARED_NOT_SENT", "successor_contacted": False, "standby_contacted": False, "prospective_exact_title": "Auren Lark", "prospective_phase": "v672-v2", "required": ["one successful exact-final canonical aggregate", "newest live authority reread", "bounded task listing", "local unique exact-title filter", "immediate reread", "duplicate guard", "one acknowledged send"], "stop_on": ["absence", "ambiguity", "pause", "redirect", "duplicate", "usage exhaustion", "protected gate", "missing or uncertain acknowledgement"], "resend_allowed": False})
    write_json("seal/seal-candidate.json", {"schema": "ghc.family.seal-candidate.v5", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "exact_final": "commit_containing_this_candidate", "counts": counts, "proposal_chain": 5910, "outcomes": OUTCOMES, "three_phase_commits_required": True, "zero_merges_required": True, "single_parent_required": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("final/final-validation-prerequisites.json", {"schema": "ghc.family.final-validation-prerequisites.v5", "canonical_state": "AUTHORIZED_PENDING_EXACT_FINAL_PUSH_AND_EQUALITY", "one_shot": True, "full_repository_suite": "not_run_not_claimed", "required": ["final committed and direct child of evidence", "final pushed", "clean state", "zero divergence", "fresh four-way equality", "exact manifests", "owner-scoped tests", "strict JSON", "five-class scan", "bounded AST scan", "baton integrity"], "replay_after_success": False})
    write_json("final/canonical-invocation-state.json", {"schema": "ghc.family.canonical-invocation-state.v4", "state_at_commit": "NOT_RUN_PENDING_EXACT_FINAL_GATE", "attempts_at_commit": 0, "successes_at_commit": 0, "receipt_location": "external_owner_supplied_path", "repository_mutation_after_external_success": False})
    write_json("final/build-receipt.json", {"schema": "ghc.family.final-build-receipt.v5", "evidence_gate": gate, "counts": counts, "outcomes": OUTCOMES, "overview_words": len(integrated.split()), "baton_words": baton_words, "owner_files_before_manifests": len([path for path in OWNER_ROOT.rglob("*") if path.is_file()]), "external_actions": 0, "successor_contact_count": 0})
    print(json.dumps({"owner": OWNER, "phase": PHASE, "counts": counts, "overview_words": len(integrated.split()), "baton_words": baton_words, "post_evidence_failures": len(POST_EVIDENCE_FAILURES)}, sort_keys=True))


def staged_names() -> list[str]:
    return git_text("diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").splitlines()


def staged_review() -> None:
    self_path = OWNER_PREFIX + "validation/final-staged-review.json"
    names = [name for name in staged_names() if name != self_path]
    exact_code = {
        "scripts/build_ghc_family_ilyra_fen_v672_v1_final.py",
        "scripts/validate_ghc_family_ilyra_fen_v672_v1_final.py",
        "tests/test_ghc_family_ilyra_fen_v672_v1_final.py",
    }
    prefixes = tuple(OWNER_PREFIX + part for part in ("closeout/", "final/", "handoffs/", "orchestration/", "seal/", "validation/final-"))
    disallowed = [name for name in names if name not in exact_code and not name.startswith(prefixes)]
    frozen_prefixes = (OWNER_PREFIX + "x1/", OWNER_PREFIX + "x2/")
    frozen = [name for name in names if name.startswith(frozen_prefixes) or name.endswith(("v672_v1_x1.py", "v672_v1_x2.py"))]
    payload = {"schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "combined_closeout_and_seal", "staged_entry_count_before_self": len(names), "staged_paths_before_self": names, "disallowed_paths": disallowed, "frozen_x1_or_evidence_paths": frozen, "valid": not disallowed and not frozen, "self_exclusion": self_path}
    write_json("validation/final-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def blob_from_index_or_head(path: str, staged: set[str]) -> bytes:
    return git("show", f":{path}").stdout if path in staged else git("show", f"HEAD:{path}").stdout


def manifests_from_index() -> None:
    names = staged_names()
    staged = set(names)
    exclusions = [
        OWNER_PREFIX + "validation/final-owner-manifest.json",
        OWNER_PREFIX + "validation/final-delta-manifest.json",
        OWNER_PREFIX + "validation/final-staged-review.json",
    ]
    delta_entries = []
    for path in sorted(staged - set(exclusions)):
        blob = git("show", f":{path}").stdout
        delta_entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    committed_owner = set(git_text("ls-tree", "-r", "--name-only", "HEAD", OWNER_PREFIX).splitlines())
    owner_paths = (committed_owner | {path for path in staged if path.startswith(OWNER_PREFIX)}) - set(exclusions)
    owner_entries = []
    for path in sorted(owner_paths):
        blob = blob_from_index_or_head(path, staged)
        owner_entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    write_json("validation/final-delta-manifest.json", {"schema": "ghc.family.git-blob-manifest.v5", "domain": "final staged delta before three self files", "hash_domain": "normalized_lf_exact_git_blob", "owner": OWNER, "phase": PHASE, "source_evidence": EVIDENCE, "entry_count": len(delta_entries), "entries": delta_entries, "self_exclusions": exclusions})
    write_json("validation/final-owner-manifest.json", {"schema": "ghc.family.git-blob-manifest.v5", "domain": "complete owner packet at final candidate before three self files", "hash_domain": "normalized_lf_exact_git_blob", "owner": OWNER, "phase": PHASE, "entry_count": len(owner_entries), "entries": owner_entries, "self_exclusions": exclusions})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifests-from-index", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
    elif args.manifests_from_index:
        manifests_from_index()
    else:
        build()


if __name__ == "__main__":
    main()
