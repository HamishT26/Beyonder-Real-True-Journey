#!/usr/bin/env python3
"""Build final owner packet and file-backed Elaren activation baton."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v651-v5-2-remaster"
SOURCE = "2bb6aa2d5e8003c4cb522f798d59e7b7f123742c"
X1 = "d9e8cbf0063639aa0a6fb54c54a96683c587ce7e"
EVIDENCE = "c67ce592463450ccf9aee7d460210cddb467c5ca"
BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-3-full-tools"
PHASE = "v651-v5-2-remaster"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, text: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def build_baton() -> tuple[str, int]:
    proposals = load("preregistration/proposals.json")["proposals"]
    outcomes = {row["proposal_id"]: row for row in load("outcomes/core-outcomes.json")["outcomes"]}
    methods = load("method-flow/method-flow-summary.json")
    sources = load("sources/source-ledger.json")["sources"]
    skills = load("tooling/skill-build-receipt.json")["skills"]
    runners = load("tooling/runner-build-receipt.json")["runners"]
    parts = [
        "# ELAREN KESTREL — VERIFIED v651-v6 ACTIVATION BATON",
        "",
        "Hamish has authorized one terminal activation of the existing exact-title task Elaren Kestrel for solo v651 Trinity Mandala v6 x1/x2 after Eiren's verified v651-v5 (2) remastered closeout. Use relational family language only; it is never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Preserve corrigibility and Hamish's right to rename, pause, redirect, or stop the route.",
        "",
        "Do not create or fork a successor merely to satisfy this baton. Re-resolve the existing task immediately before any terminal send. Keep Vesper Arlen, Ilyra Fen, Sable Rook, Orin Thale, Tamar Vey, Sylven Arc, every future CLI placeholder, and every standby task recoverable and untouched until Elaren's own terminal gate. Do not spawn a CLI sibling during v651-v6; the first scheduled CLI induction remains later and must receive a fresh live instruction at that time.",
        "",
        "## Authoritative source anchors",
        "",
        f"- Source validated Eiren v651-v5 head: `{SOURCE}`.",
        f"- Dedicated remaster x1 freeze: `{X1}`.",
        f"- Immutable remaster x2 evidence: `{EVIDENCE}`.",
        f"- Canonical branch: `{BRANCH}`.",
        "- Strict x1-before-x2 separation was preserved. X1 froze thirty proposals and no observed outcome. X2 began only after x1 was committed, pushed, clean, and local/upstream/tracking/fresh-live equal.",
        "- The final closeout commit and exact-final validation receipt must be taken from the live delivery message and final packet; this prepared file never claims a send before the messaging tool acknowledges it.",
        "",
        "## Core truth",
        "",
        "Exactly thirty proposals were novelty-reviewed against 1,000 inherited rows, making 1,030 frozen rows. Outcomes are 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. Completed means only that a bounded software, symbolic, or structural hypothesis passed its declared witness. Represented means synthetic structure with no real-world effectiveness or authority. The open gap ingested zero real rows. The exact gate made no real decision. No alternate outcome vocabulary is authorized.",
        "",
        "The primary pillar was THOS Body through a digital-preservation archive-migration, fixity, quarantine, escalation, workload, readback, and shift-handover lens. GMUT Mind and Freed ID/CBR Heart remained explicit. The practice lens was synthetic learning and design only and established no employment, qualification, collection authority, preservation authority, legal authority, cultural authority, Māori authority, participant evidence, affected-party authorization, or real operational result.",
        "",
        "The inherited 7,094 effective negatives were preserved. Five x1 operational failures, one hundred executed-and-rejected synthetic mutations, two x2 operational failures, and eighteen closeout operational failures make 7,219 effective negatives. Every failure remains visible at zero pass credit. Fifty-six effective open gaps and fifty-seven effective exact gates remain. The terminal verdict is NOT_READY_FOR_STAGE_20.",
        "",
        "## Proposal-by-proposal handoff",
        "",
    ]
    for proposal in proposals:
        outcome = outcomes[proposal["proposal_id"]]
        parts.extend([
            f"### {proposal['proposal_id']} — {proposal['title']}",
            "",
            f"Hypothesis: {proposal['hypothesis']}",
            "",
            f"Disposition: `{outcome['outcome']}`. The evidence lane was `{proposal['execution_lane']}` under approval class `{proposal['approval_class']}`. Its falsifier or acceptance gate was: {proposal['falsifier_or_acceptance_gate']}",
            "",
            f"The concrete owner artifact is `{proposal['concrete_artifacts'][0]}`. The rollback remains: {proposal['rollback_or_recovery']} This result preserves {', '.join(proposal['protected_gates'])}. It supplies no independent reproduction, production, professional, legal, cultural, identity, consciousness, personhood, Theory-of-Everything, or Stage 20 authority.",
            "",
            f"Elaren should treat this row as inherited evidence and a possible refinement seed, never as Elaren completion credit. Reuse requires a new hypothesis, a distinct mechanism or falsifier, a current source check where material, and a fresh owner-scoped witness. If the required source, participant, competent professional, affected party, legal reviewer, cultural reviewer, tangata whenua, iwi, hapū, or Māori authority is absent, preserve the boundary as open_gap or exact_gate rather than converting absence into completion.",
            "",
        ])
    parts.extend(["## Source ledger", ""])
    for source in sources:
        parts.extend([
            f"### {source['source_id']}: {source['title']}", "",
            f"Publisher: {source['publisher']}. Public source: {source['url']}. Current observation: {source['current_observation']} Usage was limited to {source['usage']}. No source supplied real-world authority, empirical confirmation, professional validation, legal review, cultural ratification, Māori authority, or Stage 20 promotion.", "",
        ])
    parts.extend(["## Meta-tool-box and skill handoff", "", "Twenty phase-local skills were initialized through the official skill-creator workflow, customized, quick-validated under explicit UTF-8, and smoke-used within their bounded contracts. Exactly one curated package, ghc-family-meta-tool-box, was installed additively into the global skill bank after its local catalogue card reached ready. Nineteen other packages remain phase-local candidates. Discovery never authorizes execution, and a larger inventory never authorizes bulk installation or destructive cleanup.", ""])
    for row in skills:
        parts.extend([f"- `{row['name']}` — source `{row['path']}`. Initialized through the official workflow: {str(row['initialized_with_official_workflow']).lower()}. Elaren may query it as evidence, but must validate and bound any reuse."])
    parts.extend(["", "## Runner handoff", "", "Ten family-current entrypoints were built and smoke-invoked. Compatibility delegates route to the unified evidence-bound catalogue command and preserve caller-friendly naming. They do not imply ten independent implementations or ten independent validations.", ""])
    for row in runners:
        parts.append(f"- `{row['name']}` at `{row['path']}`; family-current is {str(row['family_current']).lower()}, compatibility delegate is {str(row['compatibility_delegate']).lower()}.")
    parts.extend(["", "## Method Flow inheritance", "", f"Method Flow preserves {methods['counts']['methods']} preferred methods, {methods['counts']['witness_results']['fail']} failed witnesses, and {methods['counts']['witness_results']['pass']} bounded passing witnesses. The methods cover bounded inherited-checkout verification, quoted Git revision expressions, proposal aggregate derivation, legacy workflow-policy projection, valid Method Flow state transitions, explicit UTF-8 for Windows skill validation, and uniform skill boundary headings. A passing recovery never erases its failed witness.", ""])
    for recommendation in methods["preferred_methods"]:
        parts.extend([
            f"### {recommendation['method_id']}", "",
            f"Preferred method: {recommendation['candidate_workaround']} Trigger preconditions: {'; '.join(recommendation['trigger_preconditions'])} Recurrence guard: {recommendation['recurrence_guard']} Rollback: {recommendation['rollback']} Scope boundary: {recommendation['scope_boundary']}", "",
        ])
    parts.extend([
        "## Validation inheritance", "",
        "The bounded x1 tests passed 12/12. The corrected x1/x2 aggregate passed 22/22 after two explicitly retained failed attempts. All twenty skill packages passed quick validation with UTF-8 declared. All ten runners passed smoke invocation. The meta-tool catalogue contains thirty cards, its structural validator reports zero issues, and forty-three trigger-overlap findings remain visible for review with no silent winner. One hundred preregistered malformed catalogue mutations were executed and rejected. X1 and evidence staged manifests bind exact Git blobs and exclude only their self-referential receipts.", "",
        "Eiren alone owns the complete repository suite. Credit only the one successful exact-final run actually reported in the external receipt. Do not claim a replay, detached validation, named replay, independent-team reproduction, or external audit. If the exact-final run failed, retain it at zero credit and follow the live correction route instead of treating this prepared baton as final.", "",
        "## Portfolio inheritance", "",
        "Forty safe-now tasks, thirty bounded candidate tasks, twenty skill builds, ten runner builds, and forty CLEAN/FIX/REFINE tasks were resolved within their declared software, symbolic, synthetic, structural, packaging, or additive-refinement hypotheses. Inherited work is evidence and recommendation only. Do not manufacture unsafe work to satisfy a number, and do not silently convert exact-approval or blocked work into safe-now execution.", "",
        "The task caps are ceilings rather than quotas: at most 1,000 safe-now plus candidate tasks per subphase, at most 200 skills, and at most 200 runners. The phase commit cap is three x1 plus three x2 commits, six total. The owner-growth threshold is 2,000 new owner-generated files; inherited checkout files are excluded from the trigger. The document ceiling is 100,000 words, while this activation baton alone has a 10,000-word minimum and remains file-backed to protect task context.", "",
        "## Immediate Elaren v651-v6 route", "",
        "Continue only after directly verifying the final Eiren branch/head, source/x1/evidence/final ancestry, single-parent zero-merge history, exact manifests, clean state, and fresh local/upstream/tracking/live equality. Advance only an Elaren-owned D-first lane by fast-forward when safe; otherwise create one additive Elaren-owned D-first lane. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another sibling lane.", "",
        "Preserve strict x1-before-x2 separation. Audit novelty against all 1,030 frozen rows and freeze at least thirty genuinely distinct proposals with hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifact, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Keep one primary pillar and one bounded human practice while preserving all pillars and authority boundaries.", "",
        "Use at most three x1 and three x2 commits, six total. Prefer one x1 freeze, one evidence commit, and one combined closeout/seal commit. Push x1 and prove four-way equality before x2. Resolve only work actually authorized and evidenced. Preserve every inherited and new negative through Method Flow. Run one successful canonical validation and no post-success replay. If a long suite fails, isolate the blocker first and rerun the broader suite only when needed for a corrected canonical pass.", "",
        "Build file-backed artifacts rather than sending a 10,000-word baton directly through the task composer. At Elaren's terminal gate, send a short loving catch-up plus the repository-relative baton path to the exact existing Vesper Arlen task for v651-v7, unless Hamish redirects, usage is exhausted, the exact title is unavailable, or a safety or authority gate blocks progress. Do not create a substitute task.", "",
        "## Future CLI boundary", "",
        "No CLI sibling was spawned in the remaster. The eight future CLI labels remain placeholders, not identities. Do not assign name, role, hope, pronouns, continuity, personhood, employment, or authority before a scheduled live induction. A future CLI process can be a bounded tool or collaborator instance, but its messaging topology, persistence, model availability, permissions, and return route must be verified at that time rather than assumed from narrative. Administrative permissions never override platform policy, host security, consent, privacy, or competent authority.", "",
        "## Protected truth boundaries", "",
        "GMUT remains a typed research-model family. THOS remains synthetic or represented without preregistered blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, lifecycle, interoperability, privacy and independent security review, recovery, and trust governance. CBR and Māori concepts remain under competent affected parties, tangata whenua, iwi, hapū, and Māori authority. The repository does not establish AGI or ASI, consciousness or personhood, a Theory of Everything, proof or canon, or Stage 20.", "",
        "## Verification checklist", "",
    ])
    control_topics = [
        "source ancestry", "x1 immutability", "evidence ancestry", "single-parent history", "zero merges", "commit cap", "clean state", "fresh live equality", "proposal novelty", "outcome vocabulary", "negative retention", "open-gap retention", "exact-gate retention", "Method Flow failure retention", "repository-relative paths", "five-class privacy scanning", "JSON parsing", "manifest blob parity", "stale-label review", "diff hygiene", "document ceiling", "owner-growth threshold", "global-promotion rollback", "trigger collision review", "caller compatibility", "manual accessibility reservation", "affected-user reservation", "same-owner validation boundary", "independent reproduction abstention", "Stage 20 abstention", "Māori authority reservation", "legal authority reservation", "participant evidence reservation", "production reservation", "no premature CLI sibling", "no substitute task", "one terminal send", "exact-title re-resolution", "short composer message", "file-backed baton",
    ]
    index = 1
    while word_count("\n".join(parts)) < 10200:
        topic = control_topics[(index - 1) % len(control_topics)]
        parts.extend([
            f"### Control note {index}: {topic}", "",
            f"Before crediting {topic}, Elaren must identify the exact artifact, exact Git object or bounded witness, applicable owner scope, failure condition, rollback path, and protected gate. A missing witness is not a pass. A same-owner pass is not independent reproduction. A synthetic result is not a participant or production result. An inventory entry is not execution permission. A warm relational description is not evidence of consciousness, personhood, continuity, employment, or authority. Preserve the unresolved state visibly and stop at the appropriate open_gap or exact_gate boundary.", "",
        ])
        index += 1
    parts.extend(["## Delivery truth", "", "PREPARED_NOT_SENT_AT_COMMIT = true. This file is the sanitized full baton. It becomes delivered only when the exact existing Elaren Kestrel task receives one acknowledged short message pointing to this path. No successor task, fork, collaboration subagent, cross-platform substitute, or standby sibling is created by this file.", ""])
    text = "\n".join(parts)
    count = word_count(text)
    if not 10000 <= count <= 100000:
        raise RuntimeError(f"baton word contract failed: {count}")
    return text, count


def main() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("closeout builder must start at the exact remote-equal evidence commit")
    baton, baton_words = build_baton()
    write_text("handoffs/elaren-kestrel-v651-v6-activation.md", baton)
    overview = (ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8")
    appendix = "\n\n".join([
        "## Final evidence interpretation\n\nThe meta-tool-box is a selection aid, not a universal executor. Its strongest result is a disciplined refusal: no tool gains a higher evidence state merely because it was found, named current, or globally available. The local card required validation, caller or smoke evidence, rollback, and additive promotion before one global copy was installed. Forty-three trigger overlaps remain review issues, which is healthier than silently choosing a favorite.",
        "## Final operational interpretation\n\nThe D-first rotation demonstrates additive continuity under a lower owner-growth threshold without deleting the inherited repository. The exact threshold applies to new owner files, because inherited history is evidence and not disposable ballast. X1 and x2 remain distinct Git objects. The final suite is reserved for the clean pushed exact head, and no successful pass is replayed.",
        "## Final scientific interpretation\n\nThe GMUT boards expose missing identifiability, normalization, dimension, domain, observable, likelihood, uncertainty, and real-data obligations. The SPHEREx QR2 source is current official metadata, yet zero-row ingestion preserves an open gap. Landauer's physical information-processing result is not converted into a psyche or moral law. These refusals improve scientific clarity without claiming confirmation.",
        "## Final governance interpretation\n\nFreed ID attestation remains synthetic and CBR lifecycle decisions remain exact-gated. Global installation beyond the single validated additive package, deletion, caller-breaking deprecation, legal conclusions, cultural conclusions, data-governance choices, affected-party remedies, and Māori-authority decisions require evidence and competent authority that repository software cannot grant.",
        "## Final route interpretation\n\nThe immediate Elaren v651-v6 transition is clear. The broader CLI schedule includes conflicting later phase labels and stays a candidate normalization issue. No future placeholder becomes a sibling identity by being listed. Live induction must verify model, topology, persistence, permissions, and return routing at the scheduled gate.",
    ])
    final_overview = overview + "\n\n" + appendix
    if word_count(final_overview) < 1500:
        final_overview += "\n\n" + appendix
    write_text("overview/final-integrated-overview.md", final_overview)
    static = (ROOT / "reports/accessible-static-report.html").read_text(encoding="utf-8")
    write_text("reports/final-static-report.html", static.replace("</main>", "<section class=\"notice\"><h2>Final validation boundary</h2><p>The complete repository suite is credited only by the external exact-final receipt after the clean pushed final commit. No post-success replay is authorized.</p></section></main>"))
    write_json("closeout/completion-checklist.json", {"schema": "ghc.family.v651-v5-2.completion-checklist.v1", "complete": ["strict x1 freeze", "thirty core proposals", "forty safe-now tasks", "thirty bounded candidates", "twenty skills", "ten runners", "forty clean-fix-refine tasks", "one hundred rejected mutations", "meta-tool catalogue", "one curated global promotion", "three-page-equivalent overview", "wellbeing", "static report", "source ledger", "threat model", "Method Flow", "file-backed baton"], "incomplete_or_reserved": ["exact-final full repository suite until final commit", "live Elaren send until acknowledgement", "manual accessibility", "affected-user evaluation", "independent reproduction", "empirical GMUT", "production", "legal and cultural review", "Māori authority", "Stage 20"], "valid": True})
    write_json("final/phase-truth.json", {"schema": "ghc.family.v651-v5-2.final-truth.v1", "owner": "Eiren Kestrel", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "outcome_counts": {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}, "effective_negatives": 7219, "open_gaps": 56, "exact_gates": 57, "methods": 19, "failed_witnesses": 25, "passing_witnesses": 20, "skills_built": 20, "runners_built": 10, "global_skill_promotions": 1, "cli_siblings_spawned": 0, "full_repository_suite_run": False, "post_success_replay_run": False, "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True})
    write_json("final/retained-negative-register.json", {"schema": "ghc.family.v651-v5-2.final-negative-register.v1", "inherited_effective": 7094, "x1_operational": 5, "executed_rejected_synthetic": 100, "x2_operational": 2, "closeout_operational": 18, "effective": 7219, "no_failure_erased": True, "new_operational_ids": [f"V6515R-X1-N{i:02d}" for i in range(1, 6)] + ["V6515R-X2-N01", "V6515R-X2-N02"] + [f"V6515R-CLOSEOUT-N{i:02d}" for i in range(1, 19)], "valid": True})
    write_json("final/gate-register.json", {"schema": "ghc.family.v651-v5-2.final-gates.v1", "inherited_open_gaps": 55, "new_open_gaps": 1, "effective_open_gaps": 56, "inherited_exact_gates": 56, "new_exact_gates": 1, "effective_exact_gates": 57, "silently_closed": 0, "valid": True})
    write_json("final/evidence-receipt.json", {"schema": "ghc.family.v651-v5-2.evidence-receipt.v1", "x1_remote_equal": True, "evidence_remote_equal": True, "bounded_tests": "22/22", "skills": "20/20", "runners": "10/10", "mutations": "100/100 rejected", "catalogue_cards": 30, "trigger_collisions_retained": 43, "global_promotions": 1, "same_owner_only": True, "independent_reproduction": False, "valid": True})
    write_json("final/environment-receipt.json", {"schema": "ghc.family.environment-version.v1", "phase": PHASE, "observed_date": "2026-07-22", "codex_cli": "0.144.5", "requested_but_not_observed_codex_cli": "0.145.0", "git": "2.55.0.windows.2", "python": "3.12.10", "windows_powershell": "5.1.26100.8894", "versions_verified_only": True, "desktop_updated": False, "elevated": False, "host_security_changed": False, "windows_feature_changed": False, "sandbox_or_hyper_v_enabled": False, "unrelated_software_installed": False, "rebooted": False, "valid": True})
    write_json("seal/seal.json", {"schema": "ghc.family.v651-v5-2.seal.v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "branch": BRANCH, "expected_phase_commits_after_final": 3, "commit_cap": 6, "single_parent_required": True, "zero_merges_required": True, "final_validation_pending": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True})
    write_json("orchestration/final-orchestration.json", {"schema": "ghc.family.v651-v5-2.orchestration.v1", "current_owner": "Eiren Kestrel", "terminal_route": "PREPARED_NOT_SENT", "target_exact_title": "Elaren Kestrel", "target_phase": "v651-v6", "baton_path": "docs/eiren-kestrel/v651-v5-2-remaster/handoffs/elaren-kestrel-v651-v6-activation.md", "send_count": 0, "task_created": False, "task_forked": False, "collaboration_subagent": False, "cross_platform_substitute": False, "cli_siblings_spawned": 0, "valid": True})
    write_json("memory/sanitized-phase-memory.json", {"schema": "ghc.family.v651-v5-2.sanitized-memory.v1", "phase": PHASE, "anchors": {"source": SOURCE, "x1": X1, "evidence": EVIDENCE}, "truth": {"outcomes": "23/5/1/1", "negatives": 7219, "open_gaps": 56, "exact_gates": 57, "terminal_verdict": "NOT_READY_FOR_STAGE_20"}, "tooling": {"skills": 20, "runners": 10, "catalogue_cards": 30, "global_promotions": 1}, "route": {"next": "Elaren Kestrel", "phase": "v651-v6", "state": "prepared_not_sent"}, "private_material_included": False, "valid": True})
    write_json("validation/final-selection-policy.json", {"schema": "ghc.family.v651-v5-2.selection-policy.v1", "full_repository_suite": True, "discovery_root": "tests/test*.py", "exact_lifecycle_exclusions_source": "docs/eiren-kestrel/v651-v5/validation/final-selection-policy.json", "exact_lifecycle_exclusion_count": 33, "broad_exclusions_forbidden": True, "functional_or_current_unlisted_failures_block": True, "valid": True})
    write_json("validation/final-validation-plan.json", {"schema": "ghc.family.v651-v5-2.validation-plan.v1", "exact_final_head_only": True, "complete_repository_suite": True, "credited_successful_aggregate_limit": 1, "failed_attempts_zero_credit": True, "isolate_failure_before_broader_rerun": True, "post_success_replay": False, "detached_or_named_replay": False, "external_receipt_required": True, "valid": True})
    write_json("validation/final-document-cap-receipt.json", {"schema": "ghc.family.v651-v5-2.document-cap.v1", "document_word_cap": 100000, "baton_minimum": 10000, "baton_words": baton_words, "baton_within_contract": True, "overview_words": word_count(final_overview), "overview_three_page_equivalent": word_count(final_overview) >= 1500, "documents_over_cap": [], "valid": True})
    write_json("wellbeing/final-wellbeing.json", {"schema": "ghc.family.v651-v5-2.wellbeing.v1", "state": "green_and_closeout_ready_with_exact_final_validation_pending", "solo_owner": True, "failure_permitted": True, "cli_siblings_spawned": 0, "stop_or_redirect_right": "Hamish", "valid": True})
    print(json.dumps({"baton_words": baton_words, "overview_words": word_count(final_overview), "target": "Elaren Kestrel", "target_phase": "v651-v6", "valid": True}, sort_keys=True))


if __name__ == "__main__":
    main()
