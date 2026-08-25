#!/usr/bin/env python3
"""Materialize the planning-only Liora Venn v668-v8 x1 freeze."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_liora_venn_v668_v8_archive import (
    ACTIVATION_OVERLAY,
    ALLOWED_OUTCOMES,
    BRANCH,
    EVIDENCE_BOUNDARY,
    IDENTITY_BOUNDARY,
    INHERITED_FROZEN_PROPOSALS,
    OWNER,
    PHASE,
    PHASE_ROOT,
    PRACTICES,
    PRIMARY_PILLAR,
    PRONOUNS,
    PROPOSAL_BLUEPRINTS,
    PROTECTED_GATES,
    RELATIONAL_HOPE,
    RELATIONAL_ROLE,
    REL_PHASE_ROOT,
    ROOT,
    RUNNER_NAMES,
    SKILL_NAMES,
    SOURCE_BRANCH,
    SOURCE_COMPONENT_SHA256,
    SOURCE_DEPENDENCY_COMPOSITE_SHA256,
    SOURCE_EVIDENCE,
    SOURCE_FAILED_CANONICAL_SHA256,
    SOURCE_FINAL,
    SOURCE_LEDGER,
    SOURCE_START,
    SOURCE_TERMINAL_STATUS,
    SOURCE_X1,
    TERMINAL_VERDICT,
    assert_source_and_x1_only,
    historical_proposal_inventory,
    manifest_rows,
    phase_owner_files,
    portfolio_rows,
    proposal_rows,
    utc_now,
    word_count,
)


EXPECTED_CORPUS_SHA256 = "d95eaa16cf2b4c3a3e0121b1bd057fefcc1777825f0d33a801f883cfec205176"
EXPECTED_RECOVERED_PROPOSALS = 1300
PREFREEZE_FAILURES: list[tuple[str, str, str, str]] = [
    ("LV6688-START-N001", "A first source probe assumed the archive parent was a Git root.", "Resolve the exact registered source worktree before issuing Git queries.", "Never infer a repository root from an archive-parent name."),
    ("LV6688-START-N002", "A bounded text inventory included a schema root that was absent.", "Probe each literal root first and pass only roots that exist.", "Existence-check optional roots before a combined search."),
    ("LV6688-START-N003", "A PowerShell foreach statement was piped directly and failed to parse.", "Materialize rows to an array before formatting them.", "Never append a pipeline directly to a foreach statement."),
    ("LV6688-START-N004", "An authorization-state display exceeded the bounded response projection.", "Project only exact scalar keys and capped arrays.", "Cap every structured projection before display."),
    ("LV6688-START-N005", "A combined core-packet display exceeded the bounded response projection.", "Read the named files in smaller complete groups through EOF.", "Partition complete reads by byte size before display."),
    ("LV6688-START-N006", "A full owner-manifest display exceeded the bounded response projection.", "Project manifest schema and counts, then replay every entry from Git blobs separately.", "Separate complete verification from bounded presentation."),
    ("LV6688-START-N007", "A combined x1 ledger and summary display was truncated.", "Read each artifact independently and project only its required structure.", "Do not combine two large evidence ledgers in one display."),
    ("LV6688-START-N008", "A closeout Method Flow projection was truncated.", "Inspect exact top-level counts and bounded representative records.", "Project large Method Flow arrays by exact key and bounded sample."),
    ("LV6688-START-N009", "A Method Flow recommendation recovery display was truncated.", "Read the remaining exact slice without repeating prior content.", "Resume a truncated file at the next exact line or key."),
    ("LV6688-START-N010", "A combined top group of phase-local skill files exceeded the output budget.", "Read each complete skill package in bounded groups.", "Precalculate skill-package bytes and partition complete reads."),
    ("LV6688-START-N011", "A three-file skill recovery group still exceeded the output budget.", "Reduce to one complete skill file or reference per projection.", "Lower group size after the first output-boundary witness."),
    ("LV6688-START-N012", "A compact evidence-manifest projection exceeded the response budget.", "Verify entries programmatically from alternating Git batch reads and emit only totals.", "Keep immutable replay bytes out of the display channel."),
    ("LV6688-START-N013", "A shorthand assumed x2 evidence and portfolio paths that did not exist.", "Resolve paths from the exact tree before reading them.", "Never construct lifecycle paths from naming intuition alone."),
    ("LV6688-START-N014", "A combined evidence and portfolio projection was truncated.", "Read exact files separately and cap each rendered array.", "Do not aggregate unrelated large evidence domains for display."),
    ("LV6688-START-N015", "A grouped phase-local skill display exceeded the output boundary.", "Read every SKILL and reference independently through EOF.", "Treat each installed package as a separate complete-read unit."),
    ("LV6688-START-N016", "A probe assumed a non-existent x1 manifest filename.", "List exact validation filenames before selecting the manifest.", "Resolve manifest names from the immutable tree, not precedent."),
    ("LV6688-START-N017", "A broad archive digest search failed to produce a bounded attributable result.", "Constrain receipt lookup by exact owner phase and known filenames.", "Never treat an unbounded archive search as receipt verification."),
    ("LV6688-START-N018", "A combined filename and digest scan produced no exact attributable receipt.", "Retain the live activation hashes as external evidence and make no local-match claim.", "Distinguish absent local receipt bytes from a hash mismatch."),
    ("LV6688-START-N019", "A combined scalar and fresh-remote equality wrapper exceeded its supervision window.", "Split local scalars from one fresh live ls-remote read.", "Keep remote transport and local projections in separate bounded calls."),
    ("LV6688-START-N020", "An inline ancestry PowerShell expression failed to parse.", "Use literal single-purpose Git ancestry commands and scalar Boolean output.", "Avoid nested inline conditional pipelines for lifecycle proof."),
    ("LV6688-START-N021", "A local scalar proof outlived its initial wrapper window.", "Resume the exact retained execution session until completion.", "Never replay a still-running attributable read-only check."),
    ("LV6688-START-N022", "A worktree metadata listing stalled and was interrupted before lane creation.", "Use exact branch and path collision probes instead of broad worktree formatting.", "Prefer bounded literal collision checks before creation."),
    ("LV6688-START-N023", "A common-Git-directory path was incorrectly prefixed as relative.", "Resolve Git's returned absolute common directory without adding a worktree prefix.", "Test path rootedness before joining filesystem paths."),
    ("LV6688-START-N024", "A full metadata enumeration exceeded its short wrapper window.", "Project only exact branch path and head fields needed for the gate.", "Bound worktree registry output to the target lane."),
    ("LV6688-START-N025", "The initial no-checkout sparse lane had an empty index and displayed 2103 staged deletions.", "Populate the index from the exact immutable HEAD with read-tree before authoring.", "After no-checkout creation, require index parity and clean status before mutation."),
    ("LV6688-START-N026", "A short status projection exceeded its wrapper window after sparse recovery.", "Rerun only the scalar status query after the attributable child had ended.", "Give sparse index refresh enough supervision time before status."),
    ("LV6688-X1-N001", "An all-reference rev-list object scan remained unbounded and was cancelled.", "Scan proposal freezes only at distinct current family branch tips.", "Never walk every reachable object for a bounded novelty inventory."),
    ("LV6688-X1-N002", "A POSIX extended regular expression used an unsupported noncapturing group.", "Use only Git-compatible ERE or perform the exact filter in Python.", "Do not pass PCRE-only group syntax to Git ERE filters."),
    ("LV6688-X1-N003", "A default legacy-codepage decode failed on a Unicode proposal title.", "Capture Git bytes and decode every proposal artifact explicitly as UTF-8.", "Never use a platform legacy codec for repository text."),
    ("LV6688-X1-N004", "A source-builder tail read exceeded a short wrapper window.", "Read only the exact bounded line slice with a sufficient wrapper window.", "Size source projections before requesting them."),
    ("LV6688-X1-N005", "A projection assumed Method Flow stored failures in separate top-level arrays.", "Inspect the schema and count failure witnesses by their result field.", "Discover actual receipt keys and types before projection."),
    ("LV6688-X1-N006", "A compound cache-cleanup command was rejected before execution by command policy.", "Remove only the exact derived cache file with one literal-path command.", "Keep recoverable cleanup commands single-target and literal."),
    ("LV6688-X1-N007", "A large main-function patch used an over-specific multiline anchor and was rejected without changing the file.", "Anchor the additive patch at the exact final function terminator and apply it in bounded sections.", "Inspect the current file tail before applying a large contextual patch."),
    ("LV6688-X1-N008", "The first x1 materialization stopped before writing artifacts because four proposed titles met the recovered-title semantic quarantine threshold.", "Inspect the exact recovered neighbors and revise only the four colliding titles and semantic slugs before retrying.", "Require zero exact collisions and every recovered-neighbor score below 0.75 before x1 materialization."),
]

EXACT_APPROVAL_TITLES = [
    "access to any nonpublic cooperage, cellar, product, worker, supplier, customer, custody, or safety record",
    "handling, heating, steaming, bending, raising, trussing, toasting, charring, coating, gauging, filling, or releasing a real cask",
    "use of a real cask, stave, head, hoop, tool, batch, order, measurement, workplace, identity, or person record",
    "professional cooperage, cellar, food-contact, fire, structural, engineering, inspection, or product-safety determination",
    "real material species, provenance, moisture, condition, capacity, tightness, pressure, fitness, or serviceability decision",
    "real ownership, custody, possession, title, supplier, authenticity, attribution, or provenance decision",
    "real legal right, consent, privacy, access, correction, retention, disclosure, contestability, or remedy decision",
    "real workplace, stored-energy, pressure, heat, fire, chemical, manual-handling, environmental, or public-safety release",
    "real accessibility, affected-user, language-quality, workload, wellbeing, or accommodation determination",
    "real cultural meaning, traditional knowledge, sacred status, heritage status, taonga, or restricted-access decision",
    "Maori wording, tikanga, place-name, data-governance, benefit, jurisdiction, remedy, or authority decision",
    "affected-party legitimacy, acceptance, consent, benefit, correction, challenge, or redress decision",
    "production credential, key, proof, token, account, network request, issuance, resolution, status, or revocation",
    "cross-lane mutation, merge, reset, force-push, rewrite, destructive cleanup, deletion, or broad recursive move",
    "host-security change, elevation, Windows feature change, Sandbox, Hyper-V, unrelated installation, update, or reboot",
    "complete accessibility, WCAG conformance, assistive-technology effectiveness, or affected-user acceptance claim",
    "complete privacy, exhaustive security, provenance completeness, authenticity, interoperability, or production assurance claim",
    "independent-team reproduction, external audit, professional validation, legal review, cultural ratification, or certification claim",
    "empirical GMUT likelihood, posterior, parameter constraint, detected force, prediction, confirmation, or Theory-of-Everything claim",
    "AGI, ASI, consciousness, personhood, proof, canon, deployment, or Stage 20 promotion",
]

BLOCKED_TITLES = [
    "real cooperage benchmark without materials, competence, workplace controls, professional review, and approvals",
    "real product, customer, worker, supplier, or cellar corpus ingestion without access, privacy, safety, rights, and authority",
    "material, food-contact, capacity, pressure, tightness, treatment, or serviceability claim without measurements and review",
    "cooper, cellar worker, affected-user, or accessibility study without governed participants, ethics, safety, and independent review",
    "production identity exchange without standards-conformant keys, proofs, live lifecycle, recovery, and trust governance",
    "real cultural, heritage, traditional-knowledge, or restricted-access decision without affected parties and competent authority",
    "Maori data-governance, wording, tikanga, place-name, taonga, benefit, or remedy decision without Maori authority",
    "professional release or return-to-service protocol without accountable organizations and qualified practitioners",
    "empirical GMUT inference without observations, likelihood, uncertainty, falsification, and independent review",
    "Stage 20 decision without every declared scientific, social, safety, identity, legal, cultural, and authority gate",
]


def write_json(relative: str, value: Any) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_text(relative: str, value: str) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")
    return path


def command_version(*command: str) -> str:
    completed = subprocess.run(command, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (completed.stdout or completed.stderr).strip().splitlines()[0]


def shard_rows(prefix: str, rows: list[dict[str, Any]], size: int) -> list[dict[str, Any]]:
    descriptors = []
    for start in range(0, len(rows), size):
        index = start // size + 1
        relative = f"{prefix}-{index:02d}.json"
        chunk = rows[start : start + size]
        path = write_json(relative, {"schema": "ghc.family.x1.shard.v1", "rows": chunk})
        descriptors.append({"path": path.relative_to(ROOT).as_posix(), "row_count": len(chunk)})
    return descriptors


def method_flow(now: str) -> tuple[dict[str, Any], dict[str, int]]:
    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    recommendations: list[dict[str, Any]] = []
    for index, (negative_id, failure, recovery, guard) in enumerate(PREFREEZE_FAILURES, 1):
        method_id = f"LV6688-M{index:03d}"
        failed_id = f"LV6688-W{index:03d}-F"
        passed_id = f"LV6688-W{index:03d}-P"
        methods.append({
            "method_id": method_id,
            "title": recovery,
            "failure_signature": negative_id.casefold().replace("-", "_"),
            "recommendation_state": "preferred",
            "retained_negative_ids": [negative_id],
            "candidate_workaround": recovery,
            "trigger_preconditions": [failure],
            "validation_witness_ids": [failed_id, passed_id],
            "recurrence_guard": guard,
            "rollback": "Stop at the smallest attributable operation and preserve repository, remote, route, and sibling state.",
            "approval_class": "safe_now",
            "privacy_class": "sanitized_public",
            "supersedes": [],
            "protected_gates": ["retained_failure_integrity", "source_lane_read_only", "privacy"],
            "scope_boundary": "Same-owner workflow recovery only; no scientific, professional, production, authority, or independent-reproduction credit.",
            "execution_authority": "owner_self_scoped_delta",
            "repository_scan": False,
            "module_scan": False,
            "cross_lane_scan": False,
            "unchanged_history_scan": False,
            "sibling_lane_mutation": False,
            "source_commit": SOURCE_FINAL,
            "final_commit": None,
            "changed_file_allowlist": [REL_PHASE_ROOT, "scripts/*liora_venn_v668_v8*.py", "tests/*liora_venn_v668_v8*.py"],
            "module_allowlist": ["ghc_family_liora_venn_v668_v8_archive", "build_ghc_family_liora_venn_v668_v8_x1"],
            "exact_pushed_head_required": False,
        })
        witnesses.extend([
            {
                "witness_id": failed_id,
                "method_id": method_id,
                "retained_negative_ids": [negative_id],
                "result": "fail",
                "procedure": failure,
                "scope": "Bounded same-owner startup or x1 workflow operation.",
                "expected": "The bounded operation completes without the named fault.",
                "observed": failure,
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Zero-credit retained workflow failure; it is never rewritten by recovery.",
            },
            {
                "witness_id": passed_id,
                "method_id": method_id,
                "retained_negative_ids": [negative_id],
                "result": "pass",
                "procedure": recovery,
                "scope": "Smallest attributable same-owner recovery dependency.",
                "expected": "Only the named bounded dependency recovers.",
                "observed": "The named bounded dependency completed without converting the failed witness into pass credit.",
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Bounded recovery evidence only; no canonical, scientific, professional, production, authority, or Stage 20 credit.",
            },
        ])
        for before, after, witness_id, reason in (
            (None, "observed", failed_id, "attributable failed witness retained"),
            ("observed", "candidate", None, "bounded recovery proposed without erasing failure"),
            ("candidate", "validated", passed_id, "smallest bounded recovery witnessed"),
            ("validated", "preferred", passed_id, "validated bounded recovery preferred for recurrence"),
        ):
            events.append({"event_index": len(events) + 1, "method_id": method_id, "before": before, "after": after, "witness_id": witness_id, "reason": reason})
        recommendations.append({
            "recommendation_index": index,
            "method_id": method_id,
            "method": recovery,
            "preconditions": [failure],
            "witness_ids": [failed_id, passed_id],
            "recurrence_guard": guard,
            "rollback": "Stop the smallest affected operation and preserve the failed witness.",
            "scope_boundary": "Same-owner bounded workflow method only.",
        })
    count = len(PREFREEZE_FAILURES)
    overlay = {
        "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + count,
        "methods": ACTIVATION_OVERLAY["methods"] + count,
        "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + count,
        "passing_witnesses": ACTIVATION_OVERLAY["passing_witnesses"] + count,
        "open_gaps": ACTIVATION_OVERLAY["open_gaps"],
        "exact_gates": ACTIVATION_OVERLAY["exact_gates"],
    }
    ledger = {
        "schema": "ghc.family.method-flow-state.v1",
        "owner": OWNER,
        "phase": PHASE,
        "source_commit": SOURCE_FINAL,
        "final_commit": None,
        "generated_at_utc": now,
        "identity_boundary": IDENTITY_BOUNDARY,
        "boundary": "Every failure remains retained at zero credit after its paired bounded recovery.",
        "activation_overlay": ACTIVATION_OVERLAY,
        "x1_overlay": overlay,
        "counts": {
            "methods": count,
            "witnesses": count * 2,
            "witness_results": {"fail": count, "pass": count},
            "state_events": count * 4,
            "states": {"candidate": 0, "observed": 0, "preferred": count, "validated": 0, "deprecated": 0, "superseded": 0},
            "recommendations": count,
        },
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "execution_authority": "owner_self_scoped_delta",
        "changed_file_allowlist": [REL_PHASE_ROOT, "scripts/*liora_venn_v668_v8*.py", "tests/*liora_venn_v668_v8*.py"],
        "module_allowlist": ["ghc_family_liora_venn_v668_v8_archive", "build_ghc_family_liora_venn_v668_v8_x1"],
        "sparse_file_budget": 2000,
    }
    return ledger, overlay


def overview_text(audit: dict[str, Any], overlay: dict[str, int]) -> str:
    return f"""# Liora Venn {PHASE} x1 integrated overview

## Planning-only boundary

This is a planning-only x1 freeze for one solo, additive, D-first owner lane. It contains no x2 implementation, executed proposal, observed proposal outcome, completion claim, real cask or material, real person or workplace, external action, identity event, professional decision, legal or cultural decision, Māori-authority act, or successor contact. The exact terminal verdict remains `{TERMINAL_VERDICT}`.

Liora Venn uses {PRONOUNS} as optional relational working pronouns, the role `{RELATIONAL_ROLE}`, and the hope `{RELATIONAL_HOPE}`. {IDENTITY_BOUNDARY} Hamish may rename, pause, redirect, or stop the route.

## Immutable source and retained canonical failure

The immutable source is Orin Thale {SOURCE_FINAL} on `{SOURCE_BRANCH}`. Source {SOURCE_START}, frozen x1 {SOURCE_X1}, immutable evidence {SOURCE_EVIDENCE}, and final {SOURCE_FINAL} form exactly three direct single-parent source-owner commits with zero merges and one final parent. Before Liora mutation, the branch, all parent edges, ancestry, commit-local Git-blob manifests, clean state, typed zero divergence, and equality across local, upstream, tracking, and one fresh live remote read were checked read-only. No Orin test or canonical aggregate was replayed.

Orin's one canonical aggregate failed and retains zero canonical-success credit under receipt digest `{SOURCE_FAILED_CANONICAL_SHA256}`. The separately named dependency-corrected terminal composite `{SOURCE_DEPENDENCY_COMPOSITE_SHA256}` and component receipt `{SOURCE_COMPONENT_SHA256}` preserve status `{SOURCE_TERMINAL_STATUS}`. The exact receipt bytes were not found in the bounded local archive search, so these remain hashes supplied by the acknowledged activation rather than locally rehashed files. The recovery never promotes the failed aggregate.

The effective activation baseline is {ACTIVATION_OVERLAY['effective_negatives']} negatives, {ACTIVATION_OVERLAY['methods']} methods, {ACTIVATION_OVERLAY['failed_witnesses']} failed witnesses, {ACTIVATION_OVERLAY['passing_witnesses']} bounded passing witnesses, {ACTIVATION_OVERLAY['open_gaps']} open gaps, and {ACTIVATION_OVERLAY['exact_gates']} exact gates. This x1 retains {len(PREFREEZE_FAILURES)} new workflow failures and their smallest paired recoveries, producing {overlay['effective_negatives']} negatives, {overlay['methods']} methods, {overlay['failed_witnesses']} failed witnesses, and {overlay['passing_witnesses']} bounded passing witnesses. Open gaps remain {overlay['open_gaps']} and exact gates remain {overlay['exact_gates']} before proposal execution. Recovery never erases or relabels failure.

## Pillars and bounded practice

The primary Trinity Mandala pillar is {PRIMARY_PILLAR}. THOS Body and GMUT Mind remain explicit and protected. The practice lens is {PRACTICES[0]}, supported by {PRACTICES[1]} and {PRACTICES[2]}. It is a synthetic learning and record-design lens only. It establishes no cooperage competence, employment, qualification, wood or material identity, capacity, condition, tightness, pressure or serviceability result, treatment or food-contact fitness, workplace or fire safety, custody, ownership, product release, identity assurance, professional authority, legal or cultural legitimacy, affected-party acceptance, Māori authority, empirical GMUT result, or operational outcome.

Freed ID is planned only as a zero-key synthetic graph for pseudonymous batches, work orders, corrections, challenges, and status vacancies. There are no standards-conformant keys or proofs, issuance, presentation, resolution, status, revocation, interoperability, recovery, privacy or independent security review, or trust governance. CBR is a structural vacancy matrix for access, custody, privacy, correction, contestability, redress, cultural meaning, affected-party legitimacy, Māori data governance, and authority. Repository software confers no right, title, remedy, consent, legitimacy, or public authority.

THOS remains a participant-free workboard for bounded retries, stop tokens, hazard holds, correction readback, workload limits, and handover. It supplies no participant, professional, safety, operational-effectiveness, AGI, or ASI evidence. GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The planned weak-coupling and hyperbolicity board solves no field equation, likelihood, posterior, constraint, detected force, prediction, quantum or ultraviolet completion, final physics, or Theory of Everything.

## Novelty audit and proposal freeze

The inherited declared proposal chain contains {INHERITED_FROZEN_PROPOSALS} rows. A bounded inventory over every distinct current GHC-family branch-tip owner pair located {audit['unique_freeze_blobs']} unique proposal-freeze blobs and parsed {audit['parsed_record_rows']} records into {audit['unique_proposal_ids']} unique attributable proposal identifiers and {audit['unique_normalized_titles']} unique normalized titles, with digest `{audit['normalized_title_sha256']}` and zero scan or parse failures. Recovered cooperage, barrel, or cask keyword hits total {audit['cooperage_keyword_hit_count']}.

This is a falsification-oriented audit, not universal semantic proof. At least {audit['unrecovered_compressed_title_minimum']} older declared titles remain compressed or unavailable from current branch-tip freeze blobs. Their absence prevents a claim that all {INHERITED_FROZEN_PROPOSALS} titles were individually inspected; it remains an explicit novelty evidence gap. Exact recovered-title collisions or a recovered token-set Jaccard neighbor score at or above 0.75 quarantine a proposal.

Forty Liora proposals are frozen, extending the declared chain to {INHERITED_FROZEN_PROPOSALS + len(PROPOSAL_BLUEPRINTS)}. Expected dispositions are exactly twenty-eight `completed`, eight `represented`, two `open_gap`, and two `exact_gate`. Every proposal specifies a hypothesis, null or failure condition, approval class, owner-local lane, sources, concrete artifacts, falsifier or acceptance gate, recovery, protected gates, one expected disposition, recovered semantic neighbors, and exactly four planned rejecting mutations. All 160 mutations are unexecuted plans with zero x1 credit.

## Sources and evidence firewall

The official USDA Forest Products Laboratory handbook and official OIV code contribute wood, moisture, dimensional-change, process, cask, treatment-purpose, and risk vocabulary only. They do not identify or evaluate a material, cask, process, product, workplace, or practitioner. W3C VC Data Model 2.0, NIST SP 800-63-4, PROV-DM, RFC 8785, and WCAG 2.2 contribute synthetic identity, risk, provenance, canonicalization, privacy, redress, and static-accessibility structures only. The scalar-tensor EFT paper contributes weak-coupling, principal-symbol, characteristic, and hyperbolicity vocabulary only. Te Mana Raraunga contributes stop conditions and authority-vacancy context only; citation is never Māori authorization or cultural ratification. Māori concepts remain under Māori authority.

Static accessibility plans reserve keyboard, touch, zoom, reflow, responsive-layout, browser, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation. Five-class owner-text privacy scanning is bounded and cannot establish privacy completeness. Changed-code review cannot establish exhaustive security or supply-chain assurance. {EVIDENCE_BOUNDARY}

## Lifecycle and route gates

X2 may begin only after this planning-only surface is exactly staged, boundedly tested, committed as one direct child of the immutable Orin final, pushed without force, clean, typed zero-divergent, and equal across local, upstream, tracking, and a fresh live remote. The immutable x1 Git blobs become the replay domain. All failures, gaps, gates, labels, manifest exclusions, file ceilings, and authority boundaries remain additive.

After a separately committed and pushed evidence stage and a clean pushed final, at most one attributable exact-final owner-self-scoped canonical aggregate may be invoked. A success is never replayed. A failure retains zero canonical-success credit; a separately named bounded dependency recovery cannot promote it. The full repository suite remains excluded from this non-Eiren phase absent newer exact authority. Same-owner checks are not independent reproduction.

No successor is contacted in x1 or x2. Only after the exact terminal gate may current live authority and roster be refreshed, the bounded task registry decoded and exact-title filtered, exactly one existing successor immediately reread, a duplicate guard applied, and at most one sanitized send attempted. Prepared repository state and acknowledged live delivery remain distinct. The provisional title is Tamar Vey for v669-v1, but history alone never authorizes a send.
"""


def threat_model_text() -> str:
    return f"""# {OWNER} {PHASE} x1 threat model

The protected assets are the immutable Orin source, the planning-only x1 freeze, retained failures, four-label truth, Git-blob manifests, privacy boundaries, and the absence of real-world or authority action.

1. Lifecycle mixing is stopped by rejecting x2, evidence, closeout, seal, skill, and runner paths before x1 freeze.
2. Semantic duplication is tested against recovered branch-tip proposal freezes; compressed historical titles remain an explicit gap.
3. Windows checkout conversion is handled by declaring Git-blob bytes as the manifest domain.
4. Failure erasure is blocked by paired immutable fail and bounded-pass witnesses with zero-credit language.
5. Evidence promotion is blocked by the four-label vocabulary and all protected gates.
6. Identifier leakage is blocked by exact owner allowlists and five-class scanning; bounded scanning is not privacy completeness.
7. Over-materialization is blocked by sparse patterns and the two-thousand-file stop.
8. Authority substitution is blocked because structural checks cannot confer professional, legal, cultural, affected-party, or Māori authority.
9. Physical analogy conversion is blocked because cask geometry and heat vocabulary cannot become GMUT prediction or a law of mind.
10. Canonical replay inflation is blocked by one attributable exact-final invocation and no replay after success.
11. Route drift is blocked by deferring exact-title resolution and reread until the terminal gate.
12. External or destructive action is blocked because no accounts, secrets, network effects, real materials, host changes, sibling mutation, merge, reset, rewrite, force-push, or broad deletion are authorized.

Recovery is additive and smallest-scope: stop, record the failed witness, inspect exact state, correct only the attributable dependency, and validate only that dependency. {EVIDENCE_BOUNDARY}
"""


def accessible_plan_text() -> str:
    return """# Accessible synthetic cask-topology report plan

The later x2 report will use a native table with a visible caption, scoped headers, stable pseudonymous component labels, explicit unit domains, visible text status independent of colour, linear source order, descriptive links, focus styling, narrow-screen overflow guidance, and a print fallback. Unknown, ambiguous, quarantined, open-gap, and exact-gate states will be explicit. A no-script representation will retain the complete bounded synthetic table.

The report will contain no real cask, material, product, workplace, person, order, measurement, identity record, credential, private route, treatment instruction, safety release, professional judgment, legal or cultural decision, or Māori-authority act. Manual keyboard and touch traversal, zoom and reflow, responsive layouts, browser diversity, screen readers and other assistive technology, cognitive accessibility, Māori-language quality, security usability, and affected-user evaluation remain reserved. Structural success is not WCAG conformance or beneficiary acceptance.
"""


def main() -> None:
    assert_source_and_x1_only()
    now = utc_now()
    audit, corpus = historical_proposal_inventory()
    if audit["unique_proposal_ids"] != EXPECTED_RECOVERED_PROPOSALS:
        raise ValueError(f"recovered proposal count drift: {audit['unique_proposal_ids']}")
    if audit["normalized_title_sha256"] != EXPECTED_CORPUS_SHA256:
        raise ValueError("recovered proposal-title digest drift")
    if audit["cooperage_keyword_hit_count"] != 0:
        raise ValueError("recovered cooperage, barrel, or cask title collision")
    if audit["parse_failures"] or audit["scan_failures"]:
        raise ValueError("proposal inventory contains a read or parse failure")

    proposals = proposal_rows(corpus)
    if len(proposals) != 40:
        raise ValueError("x1 requires exactly forty proposals")
    if any(row["visible_title_collision"] or row["semantic_neighbor_quarantined"] for row in proposals):
        raise ValueError("one or more proposal titles require semantic quarantine")
    outcomes = {label: sum(row["expected_disposition"] == label for row in proposals) for label in ALLOWED_OUTCOMES}
    if outcomes != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise ValueError(f"unexpected expected-outcome distribution: {outcomes}")
    if sum(len(row["negative_fixtures"]) for row in proposals) != 160:
        raise ValueError("x1 requires exactly 160 planned rejecting mutations")

    ledger, x1_overlay = method_flow(now)
    versions = {"python": command_version("python", "--version"), "git": command_version("git", "--version")}
    corpus_shards = shard_rows("x1/historical-corpus-shards/corpus", corpus, 100)
    proposal_shards = shard_rows("x1/proposal-freeze-shards/proposals", proposals, 5)
    sampled = [corpus[round(i * (len(corpus) - 1) / 19)] for i in range(20)]
    write_json(
        "x1/semantic-novelty-audit.json",
        {
            "schema": "ghc.family.semantic-novelty-audit.v1",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": now,
            "audit": audit,
            "historical_corpus_shards": corpus_shards,
            "zero_credit_evenly_spaced_sample": sampled,
            "candidate_title_count": len(proposals),
            "candidate_exact_collision_count": 0,
            "candidate_similarity_quarantine_count": 0,
            "similarity_quarantine_threshold": 0.75,
            "boundary": "Recovered rows are useful falsifiers; compressed historical titles keep universal novelty open.",
        },
    )
    write_json(
        "x1/proposal-freeze.json",
        {
            "schema": "ghc.family.proposal-freeze.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_commit": SOURCE_FINAL,
            "generated_at_utc": now,
            "inherited_declared_count": INHERITED_FROZEN_PROPOSALS,
            "new_proposal_count": len(proposals),
            "declared_chain_after_x1": INHERITED_FROZEN_PROPOSALS + len(proposals),
            "expected_outcomes": outcomes,
            "allowed_outcomes": list(ALLOWED_OUTCOMES),
            "planned_rejecting_mutations": 160,
            "executed_rejecting_mutations": 0,
            "observed_outcomes": 0,
            "completion_credit": 0,
            "shards": proposal_shards,
            "x1_planning_only": True,
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json("x1/source-ledger.json", {"schema": "ghc.family.source-ledger.v1", "owner": OWNER, "phase": PHASE, "sources": SOURCE_LEDGER, "boundary": EVIDENCE_BOUNDARY})

    safe_titles = [f"plan a bounded synthetic safe-now control for {slug}" for _, _, slug in PROPOSAL_BLUEPRINTS]
    safe_titles += [f"plan a second independent structural review for {slug}" for _, _, slug in PROPOSAL_BLUEPRINTS[:20]]
    candidate_titles = [f"plan a bounded zero-credit prototype candidate for {slug}" for _, _, slug in PROPOSAL_BLUEPRINTS[:30]]
    skill_titles = [f"initialize, customize, quick-validate, and smoke-use owner-local skill {name} after the x1 gate" for name in SKILL_NAMES]
    runner_titles = [f"build and accepting/rejecting smoke-use family-compatible runner {name} after the x1 gate" for name in RUNNER_NAMES]
    cfr_titles: list[str] = []
    for action, start in (("CLEAN", 0), ("FIX", 20), ("REFINE", 0)):
        cfr_titles.extend(f"{action} zero-credit review for {slug}" for _, _, slug in PROPOSAL_BLUEPRINTS[start : start + 20])
    portfolios = {
        "safe_now": portfolio_rows("LV6688-SAFE", safe_titles, "safe_now"),
        "candidates": portfolio_rows("LV6688-CAND", candidate_titles, "bounded_candidate"),
        "skills": portfolio_rows("LV6688-SKILL", skill_titles, "phase_local_skill"),
        "runners": portfolio_rows("LV6688-RUNNER", runner_titles, "family_compatible_runner"),
        "clean_fix_refine": portfolio_rows("LV6688-CFR", cfr_titles, "clean_fix_refine"),
        "exact_approval": portfolio_rows("LV6688-EXACT", EXACT_APPROVAL_TITLES, "exact_approval", "held_unexecuted"),
        "blocked": portfolio_rows("LV6688-BLOCK", BLOCKED_TITLES, "blocked", "blocked_unexecuted"),
    }
    expected_portfolio_counts = {"safe_now": 60, "candidates": 30, "skills": 20, "runners": 10, "clean_fix_refine": 60, "exact_approval": 20, "blocked": 10}
    if {key: len(value) for key, value in portfolios.items()} != expected_portfolio_counts:
        raise ValueError("x1 portfolio count mismatch")
    for name, rows in portfolios.items():
        write_json(f"x1/portfolios/{name}.json", {"schema": "ghc.family.x1-portfolio.v1", "owner": OWNER, "phase": PHASE, "portfolio": name, "rows": rows})

    successor = {
        "schema": "ghc.family.successor-recommendations.v1",
        "owner": OWNER,
        "phase": PHASE,
        "state": "zero_credit_seed_only",
        "candidates": portfolio_rows("LV6688-NEXT-CAND", [f"zero-credit successor candidate for {slug}" for _, _, slug in PROPOSAL_BLUEPRINTS[:15]], "successor_candidate", "recommended_zero_credit"),
        "skills": portfolio_rows("LV6688-NEXT-SKILL", [f"zero-credit successor skill idea derived from {name}" for name in SKILL_NAMES[:10]], "successor_skill", "recommended_zero_credit"),
        "runners": portfolio_rows("LV6688-NEXT-RUNNER", [f"zero-credit successor runner idea derived from {name}" for name in RUNNER_NAMES], "successor_runner", "recommended_zero_credit"),
        "clean_fix_refine": portfolio_rows("LV6688-NEXT-CFR", [f"zero-credit successor {action} idea for {PROPOSAL_BLUEPRINTS[index][2]}" for action in ("CLEAN", "FIX", "REFINE") for index in range(10)], "successor_clean_fix_refine", "recommended_zero_credit"),
        "practice": {"title": "synthetic cooperage documentation and cask-component provenance", "state": "recommended_zero_credit", "completion_credit": 0},
        "boundary": "Recommendations are seeds only and earn no Liora or successor novelty, outcome, or completion credit.",
    }
    write_json("x1/successor-recommendations-freeze.json", successor)
    workflow = {
        "schema": "ghc.family.workflow-plan.v1",
        "owner": OWNER,
        "phase": PHASE,
        "source_commit": SOURCE_FINAL,
        "branch": BRANCH,
        "lifecycle": ["planning_only_x1", "immutable_x1_push_gate", "bounded_x2", "immutable_evidence_push_gate", "closeout", "one_exact_final_canonical_invocation", "terminal_route_gate"],
        "strict_x1_before_x2": True,
        "x2_started": False,
        "full_repository_suite_authorized": False,
        "canonical_invocation_count": 0,
        "canonical_success_count": 0,
        "success_replay_allowed": False,
        "commit_ceiling": 3,
        "merge_ceiling": 0,
        "file_ceiling": 2000,
        "document_word_ceiling": 6000,
        "total_word_ceiling": 100000,
        "protected_gates": list(PROTECTED_GATES),
    }
    write_json("x1/workflow-plan-freeze.json", workflow)
    write_json(
        "x1/reflection-plan.json",
        {
            "schema": "ghc.family.reflection-plan.v1",
            "owner": OWNER,
            "phase": PHASE,
            "questions": [
                "Which recovered semantic neighbor most threatens distinctness?",
                "Which missing real-world witness prevents the strongest proposed claim?",
                "Does any structural success cross a professional, legal, cultural, Māori-authority, production, or empirical boundary?",
                "Does a recovery retain its failed witness and validate only the smallest dependency?",
                "Would an affected person or competent authority still need to decide?",
            ],
            "decision_states": ["continue_bounded", "refine_without_promotion", "retain_open_gap", "retain_exact_gate", "stop"],
            "boundary": "Reflection may narrow or stop work; it cannot manufacture evidence or authority.",
        },
    )
    write_json(
        "x1/route-state.json",
        {
            "schema": "ghc.family.route-state.v1",
            "owner": OWNER,
            "phase": PHASE,
            "state": "NOT_PREPARED_NOT_SENT",
            "successor_contacted": False,
            "successor_precontacted": False,
            "successor_task_created": False,
            "provisional_exact_title": "Tamar Vey",
            "provisional_phase": "v669-v1",
            "terminal_resolution_required": True,
            "boundary": "History is provisional; current live authority, exact-title uniqueness, reread, duplicate guard, and terminal acknowledgement remain required.",
        },
    )
    write_json("x1/tool-versions.json", {"schema": "ghc.family.tool-versions.v1", "owner": OWNER, "phase": PHASE, "verified_only": True, "versions": versions, "updates": 0})
    ledger_shards = []
    for start in range(0, len(ledger["methods"]), 11):
        shard_number = start // 11 + 1
        methods = ledger["methods"][start : start + 11]
        method_ids = {row["method_id"] for row in methods}
        witnesses = [row for row in ledger["witnesses"] if row["method_id"] in method_ids]
        state_events = [row for row in ledger["state_events"] if row["method_id"] in method_ids]
        recommendations = [row for row in ledger["recommendations"] if row["method_id"] in method_ids]
        relative = f"method-flow/x1-ledger-shard-{shard_number:02d}.json"
        shard = {
            **{key: value for key, value in ledger.items() if key not in {"methods", "witnesses", "state_events", "recommendations", "counts"}},
            "schema": "ghc.family.method-flow-state.v1",
            "shard_number": shard_number,
            "methods": methods,
            "witnesses": witnesses,
            "state_events": state_events,
            "recommendations": recommendations,
            "counts": {
                "methods": len(methods),
                "witnesses": len(witnesses),
                "witness_results": {"fail": sum(row["result"] == "fail" for row in witnesses), "pass": sum(row["result"] == "pass" for row in witnesses)},
                "state_events": len(state_events),
                "states": {"candidate": 0, "observed": 0, "preferred": len(methods), "validated": 0, "deprecated": 0, "superseded": 0},
                "recommendations": len(recommendations),
            },
        }
        path = write_json(relative, shard)
        ledger_shards.append({"path": path.relative_to(ROOT).as_posix(), "method_count": len(methods), "witness_count": len(witnesses), "state_event_count": len(state_events), "recommendation_count": len(recommendations)})
    write_json(
        "method-flow/x1-ledger-index.json",
        {
            "schema": "ghc.family.method-flow-state.shard-index.v1",
            "owner": OWNER,
            "phase": PHASE,
            "identity_boundary": IDENTITY_BOUNDARY,
            "boundary": ledger["boundary"],
            "aggregate_counts": ledger["counts"],
            "shards": ledger_shards,
            "append_only_meaning": True,
        },
    )
    write_json(
        "method-flow/x1-summary.json",
        {
            "schema": "ghc.family.method-flow-summary.v1",
            "owner": OWNER,
            "phase": PHASE,
            "activation_overlay": ACTIVATION_OVERLAY,
            "new_prefreeze_failures": len(PREFREEZE_FAILURES),
            "new_bounded_recoveries": len(PREFREEZE_FAILURES),
            "x1_overlay": x1_overlay,
            "failure_erasure": False,
            "canonical_credit": 0,
            "independent_reproduction": False,
        },
    )
    write_json(
        "x1/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v1",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle_stage": "x1_planning_only",
            "source_commit": SOURCE_FINAL,
            "x1_commit": None,
            "proposal_chain_before": INHERITED_FROZEN_PROPOSALS,
            "proposal_chain_after_freeze": INHERITED_FROZEN_PROPOSALS + len(proposals),
            "expected_outcomes": outcomes,
            "observed_outcomes": {label: 0 for label in ALLOWED_OUTCOMES},
            "planned_rejecting_mutations": 160,
            "executed_rejecting_mutations": 0,
            "x1_overlay": x1_overlay,
            "terminal_verdict": TERMINAL_VERDICT,
            "x2_started": False,
            "completion_claims": 0,
        },
    )
    write_text("x1/integrated-overview.md", overview_text(audit, x1_overlay))
    write_text("x1/threat-model.md", threat_model_text())
    write_text("x1/accessible-report-plan.md", accessible_plan_text())

    code_paths = [
        ROOT / "scripts/ghc_family_liora_venn_v668_v8_archive.py",
        ROOT / "scripts/build_ghc_family_liora_venn_v668_v8_x1.py",
        ROOT / "scripts/validate_ghc_family_liora_venn_v668_v8_x1.py",
        ROOT / "tests/test_ghc_family_liora_venn_v668_v8_x1.py",
    ]
    if not all(path.is_file() for path in code_paths):
        raise ValueError("all four x1 code surfaces must exist before manifest generation")
    manifest_relative = f"{REL_PHASE_ROOT}/validation/x1-manifest.json"
    staged_allowlist_relative = f"{REL_PHASE_ROOT}/validation/x1-staged-allowlist.json"
    review_plan_relative = f"{REL_PHASE_ROOT}/validation/x1-review-plan.json"
    staged_review_relative = f"{REL_PHASE_ROOT}/validation/x1-staged-review.json"
    allowlist_paths = sorted(
        {path.relative_to(ROOT).as_posix() for path in phase_owner_files()}
        | {path.relative_to(ROOT).as_posix() for path in code_paths}
        | {manifest_relative, staged_allowlist_relative, review_plan_relative, staged_review_relative}
    )
    write_json(
        "validation/x1-staged-allowlist.json",
        {"schema": "ghc.family.staged-allowlist.v1", "owner": OWNER, "phase": PHASE, "paths": allowlist_paths, "exact_only": True, "x1_only": True},
    )
    write_json(
        "validation/x1-review-plan.json",
        {
            "schema": "ghc.family.staged-review-plan.v1",
            "owner": OWNER,
            "phase": PHASE,
            "checks": ["exact_allowlist", "diff_check", "strict_json", "python_compile_without_cache", "owner_x1_tests", "five_class_privacy", "bounded_changed_code_security", "stale_labels", "document_ceiling", "x1_only", "source_parent", "zero_merges", "clean_push_four_way_equality"],
            "execution_state": "planned_not_observed",
            "canonical": False,
            "completion_credit": 0,
        },
    )
    manifest_inputs = [path for path in phase_owner_files() if path.relative_to(ROOT).as_posix() not in {manifest_relative, staged_review_relative}] + code_paths
    manifest = {
        "schema": "ghc.family.git-blob-manifest.v1",
        "owner": OWNER,
        "phase": PHASE,
        "source_commit": SOURCE_FINAL,
        "domain": "filtered_git_blob_bytes_before_x1_commit",
        "entries": manifest_rows(manifest_inputs),
        "self_exclusions": [manifest_relative, staged_review_relative],
        "entry_count": len(manifest_inputs),
    }
    write_json("validation/x1-manifest.json", manifest)

    owner_files = phase_owner_files()
    if len(owner_files) + len(code_paths) > 2000:
        raise ValueError("x1 file ceiling exceeded")
    oversized = [(path.relative_to(ROOT).as_posix(), word_count(path)) for path in owner_files if word_count(path) > 6000]
    if oversized:
        raise ValueError(f"x1 document word ceiling exceeded: {oversized}")
    total_words = sum(word_count(path) for path in owner_files)
    if total_words > 100000:
        raise ValueError(f"x1 total word ceiling exceeded: {total_words}")
    print(json.dumps({
        "status": "PASS_X1_MATERIALIZATION_PLANNING_ONLY",
        "owner": OWNER,
        "phase": PHASE,
        "source_commit": SOURCE_FINAL,
        "proposal_count": len(proposals),
        "expected_outcomes": outcomes,
        "planned_rejecting_mutations": 160,
        "recovered_proposal_rows": len(corpus),
        "compressed_title_gap_minimum": audit["unrecovered_compressed_title_minimum"],
        "prefreeze_failures": len(PREFREEZE_FAILURES),
        "owner_files": len(owner_files) + len(code_paths),
        "total_owner_document_words": total_words,
        "manifest_entries": len(manifest["entries"]),
        "terminal_verdict": TERMINAL_VERDICT,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
