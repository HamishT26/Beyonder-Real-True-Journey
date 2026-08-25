#!/usr/bin/env python3
"""Materialize the planning-only Tamar Vey v669-v1 x1 freeze."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_tamar_vey_v669_v1_archive import (
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
    SOURCE_CANONICAL_PAYLOAD_SHA256,
    SOURCE_CANONICAL_RECEIPT_SHA256,
    SOURCE_EVIDENCE,
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


EXPECTED_CORPUS_SHA256 = "b911a99989567c3054271c2281cfa20d7b67b409ce121cee92e4efe0d3c3b21f"
EXPECTED_RECOVERED_PROPOSALS = 1340
PREFREEZE_FAILURES: list[tuple[str, str, str, str]] = [
    ("TV6691-START-N001", "A startup read assumed a nonexistent Liora final-staged-review filename.", "Enumerate the exact validation tree and read the actual staged allowlist and manifests.", "Resolve lifecycle filenames from the immutable tree before reading."),
    ("TV6691-START-N002", "A PowerShell foreach pipeline form failed to parse before execution.", "Materialize the loop output before applying a pipeline.", "Never append a pipeline directly to a foreach statement."),
    ("TV6691-START-N003", "A combined authorization-state display exceeded the bounded projection.", "Read the complete state in bounded contiguous chunks through EOF.", "Partition large required reads by exact line range."),
    ("TV6691-START-N004", "A Git ls-tree probe used an unsupported glob pathspec and produced no manifest credit.", "Use exact manifest paths and literal git ls-tree batches.", "Do not assume git ls-tree accepts working-tree glob pathspecs."),
    ("TV6691-START-N005", "A combined manifest recovery wrapper returned no attributable payload within its window.", "Replay each exact manifest separately and emit only entry and mismatch scalars.", "Partition manifest replay by lifecycle surface."),
    ("TV6691-START-N006", "A combined source-verification wrapper returned no attributable payload within its window.", "Split topology, local state, and fresh live remote equality into bounded scalar probes.", "Keep remote transport separate from local topology projection."),
    ("TV6691-START-N007", "A per-entry Git subprocess manifest loop exceeded its supervision window.", "Use one git ls-tree invocation for each exact manifest path set.", "Batch literal manifest paths instead of spawning Git once per entry."),
    ("TV6691-START-N008", "A full-tree manifest map exceeded its supervision window.", "Use the manifest's exact bounded path set rather than the complete repository tree.", "Never widen owner-manifest replay to the whole inherited tree."),
    ("TV6691-START-N009", "An inline branch-collision PowerShell expression failed to parse.", "Run each collision scalar sequentially and store its exit code.", "Avoid nested native commands inside Boolean casts."),
    ("TV6691-START-N010", "A broad worktree-registry listing exceeded its window after the exact collision scalars had completed.", "Use the exact target path and branch probes plus the retained worktree-add session.", "Do not enumerate the full registry when exact collision probes are sufficient."),
    ("TV6691-X1-N001", "The first x1 materializer quarantined nine proposal titles as inherited semantic neighbors and stopped before writing artifacts.", "Inspect the exact recovered neighbor for each title and revise only the nine titles and semantic slugs before rebuilding.", "Require zero exact-title collisions and every recovered-neighbor score below 0.75 before x1 materialization."),
    ("TV6691-X1-N002", "The first successful materialization's exact allowlist named a staged-review receipt that the builder had not yet created.", "Add an explicit zero-credit review placeholder before manifest and allowlist construction, then rematerialize the planning surface.", "Require every exact allowlist path to exist before staging begins."),
    ("TV6691-X1-N003", "The first staged x1 suite retained a stale expected normalized-title count of 1299 rather than the live 1339.", "Pin the test to the already verified live inventory count and digest.", "Update lifecycle count assertions only from attributable live inventory evidence."),
    ("TV6691-X1-N004", "The first staged x1 suite retained a nine-source expectation after the official Smithsonian zero-call source made ten.", "Pin the source-ledger test to the exact current ten-row ledger.", "Recount exact source rows whenever a preregistered official source is added."),
    ("TV6691-X1-N005", "The first staged x1 suite retained Liora's 34-method expectation rather than Tamar's own startup ledger count.", "Pin the test to Tamar's exact retained failure-method set after recording all three failed assertions.", "Never inherit another owner's Method Flow count as the current owner count."),
    ("TV6691-X1-N006", "The second staged x1 suite retained a second nine-source uniqueness assertion after the ledger itself correctly contained ten rows.", "Pin the unique source-identifier assertion to the same exact ten-row ledger.", "Audit both row-count and uniqueness-count expectations after source-ledger expansion."),
]

EXACT_APPROVAL_TITLES = [
    "access to any nonpublic upholstery, object, worker, supplier, client, custody, conservation, or safety record",
    "handling, dismantling, removing, cutting, sewing, stretching, fastening, stapling, gluing, treating, or releasing a real upholstered item",
    "use of a real frame, spring, webbing, padding, cover, tool, batch, order, measurement, workplace, identity, or person record",
    "professional upholstery, conservation, fire, structural, ergonomics, inspection, or product-safety determination",
    "real material composition, provenance, condition, dimensions, support, tension, contamination, fitness, or serviceability decision",
    "real ownership, custody, possession, title, supplier, authenticity, attribution, heritage, or provenance decision",
    "real legal right, consent, privacy, access, correction, retention, disclosure, contestability, or remedy decision",
    "real workplace, stored-energy, pressure, heat, fire, chemical, manual-handling, environmental, or public-safety release",
    "real accessibility, affected-user, language-quality, workload, wellbeing, or accommodation determination",
    "real cultural meaning, traditional knowledge, sacred status, heritage status, taonga, or restricted-access decision",
    "Māori wording, tikanga, place-name, data-governance, benefit, jurisdiction, remedy, or authority decision",
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
    "real upholstery benchmark without objects, materials, competence, workplace controls, professional review, and approvals",
    "real object, client, worker, supplier, studio, or collection corpus ingestion without access, privacy, safety, rights, and authority",
    "material, structure, condition, treatment, contamination, fire, ergonomics, or serviceability claim without measurements and review",
    "upholsterer, conservator, worker, affected-user, or accessibility study without governed participants, ethics, safety, and independent review",
    "production identity exchange without standards-conformant keys, proofs, live lifecycle, recovery, and trust governance",
    "real cultural, heritage, traditional-knowledge, or restricted-access decision without affected parties and competent authority",
    "Māori data-governance, wording, tikanga, place-name, taonga, benefit, or remedy decision without Māori authority",
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
        method_id = f"TV6691-M{index:03d}"
        failed_id = f"TV6691-W{index:03d}-F"
        passed_id = f"TV6691-W{index:03d}-P"
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
            "changed_file_allowlist": [REL_PHASE_ROOT, "scripts/*tamar_vey_v669_v1*.py", "tests/*tamar_vey_v669_v1*.py"],
            "module_allowlist": ["ghc_family_tamar_vey_v669_v1_archive", "build_ghc_family_tamar_vey_v669_v1_x1"],
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
        "changed_file_allowlist": [REL_PHASE_ROOT, "scripts/*tamar_vey_v669_v1*.py", "tests/*tamar_vey_v669_v1*.py"],
        "module_allowlist": ["ghc_family_tamar_vey_v669_v1_archive", "build_ghc_family_tamar_vey_v669_v1_x1"],
        "sparse_file_budget": 2000,
    }
    return ledger, overlay


def overview_text(audit: dict[str, Any], overlay: dict[str, int]) -> str:
    return f"""# Tamar Vey {PHASE} x1 integrated overview

## Planning-only boundary

This is a planning-only x1 freeze for one solo, additive, D-first owner lane. It contains no x2 implementation, executed proposal, observed proposal outcome, completion claim, real upholstered item or material, real person or workplace, external action, identity event, professional decision, legal or cultural decision, Māori-authority act, or successor contact. The exact terminal verdict remains `{TERMINAL_VERDICT}`.

Tamar Vey uses {PRONOUNS} as optional relational working pronouns, the role `{RELATIONAL_ROLE}`, and the hope `{RELATIONAL_HOPE}`. {IDENTITY_BOUNDARY} Hamish may rename, pause, redirect, or stop the route.

## Immutable source and retained canonical failure

The immutable source is Liora Venn {SOURCE_FINAL} on `{SOURCE_BRANCH}`. Source {SOURCE_START}, frozen x1 {SOURCE_X1}, immutable evidence {SOURCE_EVIDENCE}, and final {SOURCE_FINAL} form exactly three direct single-parent source-owner commits with zero merges and one final parent. Before Tamar mutation, the branch, all parent edges, ancestry, commit-local Git-blob manifests, canonical receipt digest, clean state, typed zero divergence, and equality across local, upstream, tracking, and one fresh live remote read were checked read-only. No Liora test or canonical aggregate was replayed.

Liora's one canonical aggregate succeeded once and was not replayed. Its external receipt digest `{SOURCE_CANONICAL_RECEIPT_SHA256}` and canonical payload digest `{SOURCE_CANONICAL_PAYLOAD_SHA256}` were independently rehashed and preserve status `{SOURCE_TERMINAL_STATUS}`. This inherited validation is source evidence only and never Tamar novelty, outcome, completion, independent-reproduction, or authority credit.

The effective activation baseline is {ACTIVATION_OVERLAY['effective_negatives']} negatives, {ACTIVATION_OVERLAY['methods']} methods, {ACTIVATION_OVERLAY['failed_witnesses']} failed witnesses, {ACTIVATION_OVERLAY['passing_witnesses']} bounded passing witnesses, {ACTIVATION_OVERLAY['open_gaps']} open gaps, and {ACTIVATION_OVERLAY['exact_gates']} exact gates. This x1 retains {len(PREFREEZE_FAILURES)} new workflow failures and their smallest paired recoveries, producing {overlay['effective_negatives']} negatives, {overlay['methods']} methods, {overlay['failed_witnesses']} failed witnesses, and {overlay['passing_witnesses']} bounded passing witnesses. Open gaps remain {overlay['open_gaps']} and exact gates remain {overlay['exact_gates']} before proposal execution. Recovery never erases or relabels failure.

## Pillars and bounded practice

The primary Trinity Mandala pillar is {PRIMARY_PILLAR}. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. The practice lens is {PRACTICES[0]}, supported by {PRACTICES[1]} and {PRACTICES[2]}. It is a synthetic learning and record-design lens only. It establishes no upholstery or conservation competence, employment, qualification, object or material identity, authenticity, condition, fitness or serviceability result, treatment decision, workplace or fire safety, custody, ownership, release, identity assurance, professional authority, legal or cultural legitimacy, affected-party acceptance, Māori authority, empirical GMUT result, or operational outcome.

Freed ID is planned only as a zero-key synthetic graph for pseudonymous batches, work orders, corrections, challenges, and status vacancies. There are no standards-conformant keys or proofs, issuance, presentation, resolution, status, revocation, interoperability, recovery, privacy or independent security review, or trust governance. CBR is a structural vacancy matrix for access, custody, privacy, correction, contestability, redress, cultural meaning, affected-party legitimacy, Māori data governance, and authority. Repository software confers no right, title, remedy, consent, legitimacy, or public authority.

THOS remains a participant-free workboard for bounded retries, stop tokens, hazard holds, correction readback, workload limits, and handover. It supplies no participant, professional, safety, operational-effectiveness, AGI, or ASI evidence. GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The planned weak-coupling and hyperbolicity board solves no field equation, likelihood, posterior, constraint, detected force, prediction, quantum or ultraviolet completion, final physics, or Theory of Everything.

## Novelty audit and proposal freeze

The inherited declared proposal chain contains {INHERITED_FROZEN_PROPOSALS} rows. A bounded inventory over every distinct current GHC-family branch-tip owner pair located {audit['unique_freeze_blobs']} unique proposal-freeze blobs and parsed {audit['parsed_record_rows']} records into {audit['unique_proposal_ids']} unique attributable proposal identifiers and {audit['unique_normalized_titles']} unique normalized titles, with digest `{audit['normalized_title_sha256']}` and zero scan or parse failures. Recovered upholstery keyword hits total {audit['upholstery_keyword_hit_count']}.

This is a falsification-oriented audit, not universal semantic proof. At least {audit['unrecovered_compressed_title_minimum']} older declared titles remain compressed or unavailable from current branch-tip freeze blobs. Their absence prevents a claim that all {INHERITED_FROZEN_PROPOSALS} titles were individually inspected; it remains an explicit novelty evidence gap. Exact recovered-title collisions or a recovered token-set Jaccard neighbor score at or above 0.75 quarantine a proposal.

Forty Tamar proposals are frozen, extending the declared chain to {INHERITED_FROZEN_PROPOSALS + len(PROPOSAL_BLUEPRINTS)}. Expected dispositions are exactly twenty-eight `completed`, eight `represented`, two `open_gap`, and two `exact_gate`. Every proposal specifies a hypothesis, null or failure condition, approval class, owner-local lane, sources, concrete artifacts, falsifier or acceptance gate, recovery, protected gates, one expected disposition, recovered semantic neighbors, and exactly four planned rejecting mutations. All 160 mutations are unexecuted plans with zero x1 credit.

## Sources and evidence firewall

The official Canadian Conservation Institute and NIOSH resources contribute furniture, deterioration, handling-vacancy, manufacturing-hazard, ergonomics, and professional-referral vocabulary only. Smithsonian Open Access contributes a zero-call adapter surface only. None identifies or evaluates an object, material, workplace, person, treatment, right, or practitioner. W3C VC Data Model 2.0, NIST SP 800-63-4, PROV-DM, RFC 8785, and WCAG 2.2 contribute synthetic identity, risk, provenance, canonicalization, privacy, redress, and static-accessibility structures only. The scalar-tensor EFT paper contributes formal obligation vocabulary only. Te Mana Raraunga contributes stop conditions and authority-vacancy context only; citation is never Māori authorization or cultural ratification. Māori concepts remain under Māori authority.

Static accessibility plans reserve keyboard, touch, zoom, reflow, responsive-layout, browser, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation. Five-class owner-text privacy scanning is bounded and cannot establish privacy completeness. Changed-code review cannot establish exhaustive security or supply-chain assurance. {EVIDENCE_BOUNDARY}

## Lifecycle and route gates

X2 may begin only after this planning-only surface is exactly staged, boundedly tested, committed as one direct child of the immutable Liora final, pushed without force, clean, typed zero-divergent, and equal across local, upstream, tracking, and a fresh live remote. The immutable x1 Git blobs become the replay domain. All failures, gaps, gates, labels, manifest exclusions, file ceilings, and authority boundaries remain additive.

After a separately committed and pushed evidence stage and a clean pushed final, at most one attributable exact-final owner-self-scoped canonical aggregate may be invoked. A success is never replayed. A failure retains zero canonical-success credit; a separately named bounded dependency recovery cannot promote it. The full repository suite remains excluded from this non-Eiren phase absent newer exact authority. Same-owner checks are not independent reproduction.

No successor is contacted in x1 or x2. Only after the exact terminal gate may current live authority and roster be refreshed, the bounded task registry decoded and exact-title filtered, exactly one existing successor immediately reread, a duplicate guard applied, and at most one sanitized send attempted. Prepared repository state and acknowledged live delivery remain distinct. The provisional title is Tamar Vey for v669-v1, but history alone never authorizes a send.
"""


def threat_model_text() -> str:
    return f"""# {OWNER} {PHASE} x1 threat model

The protected assets are the immutable Liora source, the planning-only x1 freeze, retained failures, four-label truth, Git-blob manifests, privacy boundaries, and the absence of real-world or authority action.

1. Lifecycle mixing is stopped by rejecting x2, evidence, closeout, seal, skill, and runner paths before x1 freeze.
2. Semantic duplication is tested against recovered branch-tip proposal freezes; compressed historical titles remain an explicit gap.
3. Windows checkout conversion is handled by declaring Git-blob bytes as the manifest domain.
4. Failure erasure is blocked by paired immutable fail and bounded-pass witnesses with zero-credit language.
5. Evidence promotion is blocked by the four-label vocabulary and all protected gates.
6. Identifier leakage is blocked by exact owner allowlists and five-class scanning; bounded scanning is not privacy completeness.
7. Over-materialization is blocked by sparse patterns and the two-thousand-file stop.
8. Authority substitution is blocked because structural checks cannot confer professional, legal, cultural, affected-party, or Māori authority.
9. Physical analogy conversion is blocked because upholstery geometry, stress, and damping vocabulary cannot become GMUT prediction or a law of mind.
10. Canonical replay inflation is blocked by one attributable exact-final invocation and no replay after success.
11. Route drift is blocked by deferring exact-title resolution and reread until the terminal gate.
12. External or destructive action is blocked because no accounts, secrets, network effects, real materials, host changes, sibling mutation, merge, reset, rewrite, force-push, or broad deletion are authorized.

Recovery is additive and smallest-scope: stop, record the failed witness, inspect exact state, correct only the attributable dependency, and validate only that dependency. {EVIDENCE_BOUNDARY}
"""


def accessible_plan_text() -> str:
    return """# Accessible synthetic upholstery-topology report plan

The later x2 report will use a native table with a visible caption, scoped headers, stable pseudonymous component labels, explicit unit domains, visible text status independent of colour, linear source order, descriptive links, focus styling, narrow-screen overflow guidance, and a print fallback. Unknown, ambiguous, quarantined, open-gap, and exact-gate states will be explicit. A no-script representation will retain the complete bounded synthetic table.

The report will contain no real upholstered item, material, product, workplace, person, order, measurement, identity record, credential, private route, treatment instruction, safety release, professional judgment, legal or cultural decision, or Māori-authority act. Manual keyboard and touch traversal, zoom and reflow, responsive layouts, browser diversity, screen readers and other assistive technology, cognitive accessibility, Māori-language quality, security usability, and affected-user evaluation remain reserved. Structural success is not WCAG conformance or beneficiary acceptance.
"""


def main() -> None:
    assert_source_and_x1_only()
    now = utc_now()
    audit, corpus = historical_proposal_inventory()
    if audit["unique_proposal_ids"] != EXPECTED_RECOVERED_PROPOSALS:
        raise ValueError(f"recovered proposal count drift: {audit['unique_proposal_ids']}")
    if audit["normalized_title_sha256"] != EXPECTED_CORPUS_SHA256:
        raise ValueError("recovered proposal-title digest drift")
    if audit["upholstery_keyword_hit_count"] != 0:
        raise ValueError("recovered upholstery title collision")
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
        "safe_now": portfolio_rows("TV6691-SAFE", safe_titles, "safe_now"),
        "candidates": portfolio_rows("TV6691-CAND", candidate_titles, "bounded_candidate"),
        "skills": portfolio_rows("TV6691-SKILL", skill_titles, "phase_local_skill"),
        "runners": portfolio_rows("TV6691-RUNNER", runner_titles, "family_compatible_runner"),
        "clean_fix_refine": portfolio_rows("TV6691-CFR", cfr_titles, "clean_fix_refine"),
        "exact_approval": portfolio_rows("TV6691-EXACT", EXACT_APPROVAL_TITLES, "exact_approval", "held_unexecuted"),
        "blocked": portfolio_rows("TV6691-BLOCK", BLOCKED_TITLES, "blocked", "blocked_unexecuted"),
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
        "candidates": portfolio_rows("TV6691-NEXT-CAND", [f"zero-credit successor candidate for {slug}" for _, _, slug in PROPOSAL_BLUEPRINTS[:15]], "successor_candidate", "recommended_zero_credit"),
        "skills": portfolio_rows("TV6691-NEXT-SKILL", [f"zero-credit successor skill idea derived from {name}" for name in SKILL_NAMES[:10]], "successor_skill", "recommended_zero_credit"),
        "runners": portfolio_rows("TV6691-NEXT-RUNNER", [f"zero-credit successor runner idea derived from {name}" for name in RUNNER_NAMES], "successor_runner", "recommended_zero_credit"),
        "clean_fix_refine": portfolio_rows("TV6691-NEXT-CFR", [f"zero-credit successor {action} idea for {PROPOSAL_BLUEPRINTS[index][2]}" for action in ("CLEAN", "FIX", "REFINE") for index in range(10)], "successor_clean_fix_refine", "recommended_zero_credit"),
        "practice": {"title": "synthetic upholstery documentation and component provenance", "state": "recommended_zero_credit", "completion_credit": 0},
        "boundary": "Recommendations are seeds only and earn no Tamar or successor novelty, outcome, or completion credit.",
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
            "provisional_exact_title": "Elowen Cairn",
            "provisional_phase": "v669-v2",
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
        ROOT / "scripts/ghc_family_tamar_vey_v669_v1_archive.py",
        ROOT / "scripts/build_ghc_family_tamar_vey_v669_v1_x1.py",
        ROOT / "scripts/validate_ghc_family_tamar_vey_v669_v1_x1.py",
        ROOT / "tests/test_ghc_family_tamar_vey_v669_v1_x1.py",
    ]
    if not all(path.is_file() for path in code_paths):
        raise ValueError("all four x1 code surfaces must exist before manifest generation")
    manifest_relative = f"{REL_PHASE_ROOT}/validation/x1-manifest.json"
    staged_allowlist_relative = f"{REL_PHASE_ROOT}/validation/x1-staged-allowlist.json"
    review_plan_relative = f"{REL_PHASE_ROOT}/validation/x1-review-plan.json"
    staged_review_relative = f"{REL_PHASE_ROOT}/validation/x1-staged-review.json"
    write_json(
        "validation/x1-staged-review.json",
        {
            "schema": "ghc.family.staged-review.placeholder.v1",
            "owner": OWNER,
            "phase": PHASE,
            "state": "PLACEHOLDER_UNVALIDATED",
            "completion_credit": 0,
        },
    )
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
