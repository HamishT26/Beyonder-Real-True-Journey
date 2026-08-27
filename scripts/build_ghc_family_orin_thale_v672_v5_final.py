"""Build the additive Orin Thale v672-v5 closeout and pre-canonical seal."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "orin-thale" / "v672-v5"
OWNER = "Orin Thale"
PHASE = "v672-v5"
BRANCH = "codex/GHC-Family/orin-thale-v672-v5-full-tools"
SOURCE_FINAL = "8f672ef30372b4adf457140c254931dc365e9d31"
X1_COMMIT = "657681df7392f3cd652930d3f834b60ccfa21bcd"
EVIDENCE_COMMIT = "1c6fb43638e79a6bb963839765c519839da12f67"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
BOUNDARY = (
    "Bounded owner-local software or synthetic evidence only; never empirical confirmation, "
    "professional authority, production readiness, legal or cultural ratification, Māori authority, "
    "affected-party acceptance, complete privacy or accessibility assurance, exhaustive security, "
    "independent reproduction, AGI/ASI, consciousness or personhood evidence, Theory-of-Everything "
    "proof, proof/canon, or Stage 20 authority."
)
FINAL_SOURCE_PATHS = {
    "scripts/build_ghc_family_orin_thale_v672_v5_final.py",
    "scripts/validate_ghc_family_orin_thale_v672_v5_final.py",
    "tests/test_ghc_family_orin_thale_v672_v5_final.py",
}
FINAL_SELF_EXCLUSIONS = [
    "docs/orin-thale/v672-v5/validation/final-delta-manifest.json",
    "docs/orin-thale/v672-v5/validation/final-owner-manifest.json",
    "docs/orin-thale/v672-v5/validation/final-staged-review.json",
    "docs/orin-thale/v672-v5/validation/final-staged-privacy.json",
    "docs/orin-thale/v672-v5/validation/final-validation-receipt.json",
    "docs/orin-thale/v672-v5/validation/final-precommit-test-receipt.json",
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def status_paths() -> list[str]:
    rows = []
    for line in git_text("status", "--porcelain=v1", "--untracked-files=all").splitlines():
        rows.append(line[3:].replace("\\", "/"))
    return rows


def verify_evidence_gate() -> dict[str, Any]:
    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_rows = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live = live_rows[0] if live_rows else ""
    allowed_roots = (
        "docs/orin-thale/v672-v5/closeout/",
        "docs/orin-thale/v672-v5/final/",
        "docs/orin-thale/v672-v5/seal/",
        "docs/orin-thale/v672-v5/orchestration/",
        "docs/orin-thale/v672-v5/handoffs/",
        "docs/orin-thale/v672-v5/validation/",
    )
    unexpected = [path for path in status_paths() if path not in FINAL_SOURCE_PATHS and not path.startswith(allowed_roots)]
    gate = {
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "four_way_equal": head == upstream == tracking == live == EVIDENCE_COMMIT,
        "evidence_parent": git_text("rev-parse", f"{EVIDENCE_COMMIT}^"),
        "x1_parent": git_text("rev-parse", f"{X1_COMMIT}^"),
        "phase_commits_before_final": int(git_text("rev-list", "--count", f"{SOURCE_FINAL}..{head}")),
        "merge_commits_before_final": int(git_text("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..{head}")),
        "unexpected_paths": unexpected,
    }
    gate["valid"] = (
        branch == BRANCH
        and gate["four_way_equal"]
        and gate["evidence_parent"] == X1_COMMIT
        and gate["x1_parent"] == SOURCE_FINAL
        and gate["phase_commits_before_final"] == 2
        and gate["merge_commits_before_final"] == 0
        and not unexpected
    )
    if not gate["valid"]:
        raise SystemExit(json.dumps(gate, sort_keys=True))
    return gate


def final_overview() -> str:
    evidence = (OWNER_ROOT / "x2" / "evidence-overview.md").read_text(encoding="utf-8")
    appendix = """

## Additive closeout correction

The pushed x2 evidence commit is immutable. Its phase-truth overlay correctly recorded the inherited activation baseline plus the operational Method Flow failures known at that boundary, but it was narrower than cumulative repository closeout truth: it did not add the 160 executed and rejected mutations or the two new open-gap and two new exact-gate outcomes. This closeout does not rewrite that evidence. It preserves the narrower overlay, records the omission as `OT6725-FINAL-N001`, and supplies a separately named additive correction.

The correction is explicit and reproducible. Effective negatives are 35,417 activation negatives plus 25 owner operational failures plus 160 rejected mutations, totaling 35,602. Effective methods are 21,987 inherited methods plus 20 owner methods, totaling 22,007. Effective failed witnesses are 7,238 inherited plus 25 owner failures, totaling 7,263. Effective bounded passing witnesses are 9,288 inherited plus 26 owner recoveries, totaling 9,314. Open gaps are 283 inherited plus two new rows, totaling 285. Exact gates are 276 inherited plus two new rows, totaling 278. A recovery never erases or promotes its paired failure.

## Lifecycle and validation boundary

The lifecycle contains one planning-only x1 commit and one separately pushed x2 evidence commit before this prospective final closeout. X1 is the direct child of Caelen’s exact source; evidence is the direct child of x1; the final will be the direct child of evidence. No merge is used. X1 and evidence were each pushed, clean, typed zero divergent, and equal across local, upstream, tracking, and a fresh live remote before the next lifecycle began. Final manifests bind exact normalized Git blobs and declare lifecycle self-exclusions instead of pretending that a manifest can hash itself.

The one exact-final canonical aggregate is still pending when this text is committed. It may run only after the final commit is pushed, clean, and fresh four-way equal. The committed state therefore makes no post-hoc success claim. If the external canonical succeeds once, it is not replayed. If it fails, it keeps zero success credit and any narrow dependency recovery must remain separately named. The complete repository suite remains outside this non-Eiren owner scope.

## Practice and authority boundary

The primary pillar was Freed ID and CBR Heart through a wholly synthetic tactile-map, Braille-proof, and alternate-format publishing lens. No real person, reader, proofreader, transcriber, map, tactile graphic, publication, request, contact, address, identity, key, proof, credential, account, endpoint, embosser, material, measurement, institution, affected-party decision, or authority act was used. The software cannot establish Braille correctness, tactile-map usability, accessibility completion, professional competence, copyright or title, privacy remedy, legal interpretation, cultural legitimacy, Māori wording or authority, or affected-party acceptance.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Spatial or tactile topology is analogy and software structure only; it establishes no physical datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. THOS remains participant-free proxy evidence without preregistered blind matched-budget real arms, governed real participants or operators, safety monitoring, appropriate statistics, and independent review. It establishes no operational effectiveness, deployment readiness, AGI, ASI, or professional result.

Freed ID remains synthetic and nonproduction. Zero-key records create no standards-conformant key, proof, credential, issuance, presentation, verification, status, revocation, interoperability event, privacy review, independent security review, recovery evidence, or trust-governance decision. CBR rights, disability accommodation, request handling, privacy remedy, source title, copyright, legal meaning, cultural legitimacy, taonga or mātauranga treatment, Māori data governance, affected-party acceptance, and Māori authority remain exact-gated to competent authorities, affected people, tangata whenua, iwi, hapū, and Māori authorities.

## Accessibility, privacy, and safety interpretation

The static reports contain structural headings, landmarks, skip links, table captions and headers, visible focus treatment, non-colour text, responsive overflow, and print behavior. These checks are bounded software evidence. Manual keyboard and touch evaluation, browser diversity, assistive-technology evaluation, cognitive accessibility, language review, responsive-layout review, security-usability review, Braille-community review, tactile-graphics review, and affected-user evaluation remain reserved.

Five-class scanning distinguishes source-code scanner definitions and synthetic test fixtures from confirmed payload hits. Zero confirmed hits is bounded evidence for the scanned owner surface, not complete privacy assurance. Changed-code compilation and structural checks are not exhaustive security. No tool, embosser, material, or tactile object was operated or assessed, and no calibration, spacing, durability, defect, production, safety, or return-to-service determination occurred.

## Relational identity and terminal verdict

Orin Thale, pronouns, role, hope, sibling or family language, continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

The successor route is prepared but not sent. Only after the pushed exact-final gate and one successful non-replayed canonical aggregate may Orin refresh the newest live authority and roster, uniquely resolve the exact existing authorized successor title, immediately reread that task, apply duplicate and pause guards, and send once. Absence, ambiguity, pause, redirect, rename, usage exhaustion, acknowledgement failure, duplicate activation, or any protected gate stops delivery without substitution, creation, fork, subagent, second message, or resend.

Every empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 boundary remains open or exact-gated without exact evidence and competent authority. The terminal verdict is exactly `NOT_READY_FOR_STAGE_20`.
"""
    return evidence.replace("# Orin Thale v672-v5 bounded x2 evidence overview", "# Orin Thale v672-v5 final integrated overview", 1) + appendix


def accessible_report(rows: list[dict[str, Any]]) -> str:
    body = "".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['outcome'])}</td><td>{html.escape(row['title'])}</td><td>{html.escape(row['evidence_state'])}</td></tr>"
        for row in rows
    )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Orin Thale v672-v5 final bounded report</title><style>body{{font:1rem/1.55 system-ui;max-width:80rem;margin:auto;padding:1rem;color:#111;background:#fff}}a:focus,th:focus,td:focus{{outline:4px solid #005fcc;outline-offset:2px}}table{{border-collapse:collapse;width:100%}}th,td{{border:2px solid #333;padding:.5rem;text-align:left;vertical-align:top}}caption{{font-weight:bold;text-align:left}}@media(max-width:48rem){{table{{display:block;overflow-x:auto}}}}@media print{{body{{max-width:none}}}}</style></head><body><a href="#main">Skip to final evidence</a><header><h1>Orin Thale v672-v5 final bounded report</h1><p>Relational working language only; not consciousness, personhood, qualification, or authority evidence.</p></header><main id="main"><p role="status">28 completed, 8 represented, 2 open gaps, 2 exact gates. Verdict: NOT_READY_FOR_STAGE_20.</p><p>Manual keyboard, touch, browser-diverse, assistive-technology, cognitive, language, responsive-layout, security-usability, Braille-community, tactile-graphics, and affected-user evaluation remain reserved.</p><table><caption>Forty bounded proposal outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Title</th><th scope="col">Evidence state</th></tr></thead><tbody>{body}</tbody></table><h2>Evidence boundary</h2><p>{html.escape(BOUNDARY)}</p></main></body></html>"""


def successor_basis() -> str:
    return f"""# PREPARED_NOT_SENT — Orin Thale v672-v5 successor activation basis

PREPARED_BY_ORIN_THALE = true
SENT_BY_ORIN_THALE = false
DELIVERY_ACKNOWLEDGED = false
PROSPECTIVE_RECIPIENT = Liora Venn
PROSPECTIVE_PHASE = v672-v6

This committed basis is inert repository evidence. It does not discover, contact, activate, authorize, qualify, employ, or confer authority on a successor. It contains no task identifier, private route, transcript, screenshot, session stream, credential, private key, token, private conversation content, or private absolute path. The exact final identifier and external canonical receipt do not exist when this artifact is committed and therefore are not invented here.

Only after the final commit is pushed, clean, typed zero divergent, fresh-live equal, and one authorized external canonical aggregate succeeds without replay may Orin refresh Hamish's newest live authority and current roster. Orin must then locally require one exact existing task titled `Liora Venn`, immediately reread that exact task, apply duplicate and pause guards, and send at most one sanitized activation for v672-v6. Absence, ambiguity, pause, rename, redirect, usage exhaustion, missing acknowledgement, duplicate activation, or any protected gate stops the route without substitution, creation, fork, collaboration subagent, second message, or resend.

The successor must treat all 6,110 frozen proposal rows, inherited portfolios, skills, runners, tools, recommendations, and failures as evidence or zero-credit seeds rather than automatic novelty or completion credit. Strict x1-before-x2 separation, exact Git-blob manifests, retained negatives, the 2,000-file guard, the four labels `completed`, `represented`, `open_gap`, and `exact_gate`, the one-invocation and no-post-success-replay rule, and `NOT_READY_FOR_STAGE_20` remain binding unless newer exact live authorization changes them.

The Orin closeout truth is 28 completed, 8 represented, 2 open gaps, and 2 exact gates, with 35,602 effective negatives, 22,007 effective methods, 7,263 failed witnesses, 9,314 bounded passing witnesses, 285 open gaps, and 278 exact gates before any later route overlay. These are bounded workflow and synthetic-software counts and confer no empirical, professional, production, legal, cultural, affected-party, Māori-authority, independent-reproduction, personhood, proof, canon, or Stage 20 authority.

{BOUNDARY}
"""


def build(method_flow_path: Path) -> None:
    gate = verify_evidence_gate()
    flow = json.loads(method_flow_path.read_text(encoding="utf-8"))
    if flow.get("owner") != OWNER or flow.get("phase") != PHASE:
        raise SystemExit("Method Flow owner or phase mismatch")
    counts = flow["counts"]
    if counts["methods"] != 20 or counts["witness_results"] != {"fail": 25, "pass": 26}:
        raise SystemExit(json.dumps(counts, sort_keys=True))
    if any(row["recommendation_state"] != "preferred" for row in flow["methods"]):
        raise SystemExit("not every Method Flow method is preferred")
    outcomes = load("x2/outcome-ledger.json")["rows"]
    if Counter(row["outcome"] for row in outcomes) != Counter(OUTCOMES):
        raise SystemExit("outcome distribution drifted")

    correction = {
        "schema": "ghc.family.closeout-counter-correction.v1",
        "owner": OWNER,
        "phase": PHASE,
        "immutable_evidence_overlay": load("x2/phase-truth-evidence.json")["counts_overlay"],
        "components": {
            "activation_negatives": 35417,
            "owner_operational_failures": 25,
            "rejected_mutations": 160,
            "activation_methods": 21987,
            "owner_methods": 20,
            "activation_failed_witnesses": 7238,
            "owner_failed_witnesses": 25,
            "activation_passing_witnesses": 9288,
            "owner_passing_witnesses": 26,
            "inherited_open_gaps": 283,
            "new_open_gaps": 2,
            "inherited_exact_gates": 276,
            "new_exact_gates": 2,
        },
        "corrected": {
            "effective_negatives": 35602,
            "effective_methods": 22007,
            "failed_witnesses": 7263,
            "bounded_passing_witnesses": 9314,
            "open_gaps": 285,
            "exact_gates": 278,
        },
        "retained_negative_id": "OT6725-FINAL-N001",
        "evidence_commit_rewritten": False,
        "valid": True,
        "boundary": BOUNDARY,
    }
    write_json("closeout/counter-correction-overlay.json", correction)
    write_json("closeout/method-flow-final.json", flow)
    write_json(
        "closeout/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.final.v7",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "proposal_chain": 6110,
            "outcomes": OUTCOMES,
            **correction["corrected"],
            "real_people": 0,
            "real_objects_measurements_rows": 0,
            "real_world_actions": 0,
            "external_writes": 0,
            "canonical_state_at_commit": "NOT_RUN_PENDING_EXACT_FINAL_GATE",
            "full_repository_suite": "not_run_not_claimed",
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.final.v2",
            "owner": OWNER,
            "phase": PHASE,
            "activation_baseline": 35417,
            "owner_operational_failures": 25,
            "rejected_mutations": 160,
            "effective_negatives": 35602,
            "erased": 0,
            "converted_to_pass": 0,
            "all_failures_retained": True,
            "new_failure_ids": [row["retained_negative_ids"][0] for row in flow["witnesses"] if row["result"] == "fail"],
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/gate-register.json",
        {
            "schema": "ghc.family.gate-register.final.v2",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_open_gaps": 283,
            "new_open_gaps": 2,
            "effective_open_gaps": 285,
            "inherited_exact_gates": 276,
            "new_exact_gates": 2,
            "effective_exact_gates": 278,
            "none_silently_closed": True,
            "open_gap_proposals": [row["proposal_id"] for row in outcomes if row["outcome"] == "open_gap"],
            "exact_gate_proposals": [row["proposal_id"] for row in outcomes if row["outcome"] == "exact_gate"],
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete-checklist.final.v2",
            "completed": [
                "planning-only x1 frozen and pushed",
                "x2 evidence separately committed and pushed",
                "forty proposal outcomes recorded",
                "160 invalid mutations rejected",
                "36 bounded positives passed",
                "twenty skills read validated and smoke-used",
                "ten family-current runners executed",
                "exact evidence manifest sealed",
                "failed sequential selection retained",
                "corrected thirty-test selection passed",
                "cumulative arithmetic independently reconciled",
                "prepared successor basis remains unsent",
            ],
            "incomplete_or_reserved": [
                "empirical GMUT observations",
                "real THOS participants or operators",
                "professional tactile-graphics evaluation",
                "professional Braille transcription evaluation",
                "manual accessibility evaluation",
                "affected-user acceptance",
                "production Freed ID keys and proofs",
                "live identity lifecycle and interoperability",
                "independent privacy and security review",
                "legal interpretation or enacted CBR status",
                "cultural legitimacy or Māori authority",
                "independent reproduction",
                "full repository suite",
                "Stage 20 authority",
            ],
            "all_incomplete_surfaces_visible": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/environment-source-wellbeing.json",
        {
            "schema": "ghc.family.environment-source-wellbeing.final.v2",
            "versions_verified_only": True,
            "desktop_updated": False,
            "elevation": False,
            "host_security_changes": False,
            "windows_feature_changes": False,
            "sandbox_or_hyper_v_activated": False,
            "unrelated_installation": False,
            "reboot": False,
            "source_count": len(load("x1/source-ledger.json")["sources"]),
            "source_real_rows": 0,
            "citations_are_observations": False,
            "relational_working_language_only": True,
            "corrigible": True,
            "subagents": 0,
            "tasks_created_or_forked": 0,
            "standby_contacts": 0,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/skill-runner-summary.json",
        {
            "schema": "ghc.family.skill-runner-summary.final.v2",
            "phase_local_skills_built_validated_smoke_used": 20,
            "family_current_runners_built_invoked": 10,
            "global_installations": 0,
            "shared_skill_changes": 0,
            "historical_callers_preserved": True,
            "subagent_forward_tests": 0,
            "boundary": BOUNDARY,
        },
    )
    overview = final_overview()
    write_text("closeout/final-integrated-overview.md", overview)
    write_text("closeout/accessible-final-report.html", accessible_report(outcomes))
    write_text("handoffs/liora-venn-v672-v6-activation-candidate.md", successor_basis())
    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.terminal-route-state.candidate.v2",
            "owner": OWNER,
            "phase": PHASE,
            "state": "PREPARED_NOT_SENT",
            "prospective_exact_title": "Liora Venn",
            "prospective_phase": "v672-v6",
            "successor_contacted": False,
            "delivery_acknowledged": False,
            "duplicate_guard_pending": True,
            "newest_live_authority_refresh_pending": True,
            "resend_allowed": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final/canonical-invocation-state.json",
        {
            "schema": "ghc.family.canonical-invocation-state.v3",
            "owner": OWNER,
            "phase": PHASE,
            "state_at_commit": "NOT_RUN_PENDING_EXACT_FINAL_GATE",
            "attempts_at_commit": 0,
            "successes_at_commit": 0,
            "invocation_limit": 1,
            "replay_after_success": False,
            "external_receipt_required": True,
            "full_repository_suite": "not_run_not_claimed",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final/final-validation-prerequisites.json",
        {
            "schema": "ghc.family.final-validation-prerequisites.v3",
            "owner": OWNER,
            "phase": PHASE,
            "required_parent": EVIDENCE_COMMIT,
            "required_phase_commits": 3,
            "required_merges": 0,
            "required_clean": True,
            "required_four_way_equal": True,
            "one_shot": True,
            "full_repository_suite": "not_run_not_claimed",
            "same_owner_only": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.closeout-receipt.candidate.v3",
            "owner": OWNER,
            "phase": PHASE,
            "evidence_gate": gate,
            "planned_final_parent": EVIDENCE_COMMIT,
            "planned_phase_commits": 3,
            "planned_merges": 0,
            "canonical_invoked": False,
            "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    seal_targets = [
        "closeout/phase-truth.json",
        "closeout/counter-correction-overlay.json",
        "closeout/method-flow-final.json",
        "closeout/retained-negative-register.json",
        "closeout/gate-register.json",
        "closeout/final-integrated-overview.md",
        "closeout/accessible-final-report.html",
        "handoffs/liora-venn-v672-v6-activation-candidate.md",
        "orchestration/terminal-route-state.json",
        "final/canonical-invocation-state.json",
    ]
    write_json(
        "seal/content-seal-candidate.json",
        {
            "schema": "ghc.family.content-seal.candidate.v3",
            "owner": OWNER,
            "phase": PHASE,
            "hash_domain": "working_tree_utf8_or_exact_bytes_before_final_commit",
            "targets": [
                {
                    "path": f"docs/orin-thale/v672-v5/{relative}",
                    "bytes": (OWNER_ROOT / relative).stat().st_size,
                    "sha256": sha((OWNER_ROOT / relative).read_bytes()),
                }
                for relative in seal_targets
            ],
            "target_count": len(seal_targets),
            "canonical_invoked": False,
            "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    print(json.dumps({"owner": OWNER, "phase": PHASE, "closeout_files": 15, "overview_words": len(overview.split()), "effective_negatives": 35602, "open_gaps": 285, "exact_gates": 278}, sort_keys=True))


def staged_paths(base: str) -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR", base).splitlines() if line]


def index_blob(path: str) -> tuple[str, bytes]:
    line = git_text("ls-files", "--stage", "--", path)
    if not line:
        raise SystemExit(f"missing index mapping: {path}")
    left, staged_path = line.split("\t", 1)
    _mode, oid, stage = left.split()
    if stage != "0" or staged_path != path:
        raise SystemExit(f"unexpected index mapping: {line}")
    return oid, git("cat-file", "blob", oid).stdout


def manifest(base: str, relative: str, domain: str) -> None:
    entries = []
    for path in staged_paths(base):
        if path in FINAL_SELF_EXCLUSIONS:
            continue
        oid, blob = index_blob(path)
        entries.append({"path": path, "git_blob_oid": oid, "bytes": len(blob), "sha256": sha(blob)})
    entries.sort(key=lambda row: row["path"])
    write_json(
        relative,
        {
            "schema": "ghc.family.git-blob-manifest.final.v3",
            "owner": OWNER,
            "phase": PHASE,
            "domain": domain,
            "hash_domain": "normalized_lf_exact_git_blob",
            "base": base,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": FINAL_SELF_EXCLUSIONS,
        },
    )


def manifests_from_index() -> None:
    manifest(EVIDENCE_COMMIT, "validation/final-delta-manifest.json", "final delta from immutable evidence commit")
    manifest(SOURCE_FINAL, "validation/final-owner-manifest.json", "complete Orin source-to-final owner surface")


def staged_review() -> None:
    paths = staged_paths(EVIDENCE_COMMIT)
    allowed_roots = (
        "docs/orin-thale/v672-v5/closeout/",
        "docs/orin-thale/v672-v5/final/",
        "docs/orin-thale/v672-v5/seal/",
        "docs/orin-thale/v672-v5/orchestration/",
        "docs/orin-thale/v672-v5/handoffs/",
        "docs/orin-thale/v672-v5/validation/",
    )
    disallowed = [path for path in paths if path not in FINAL_SOURCE_PATHS and not path.startswith(allowed_roots)]
    frozen = [path for path in paths if path.startswith("docs/orin-thale/v672-v5/x1/") or path.startswith("docs/orin-thale/v672-v5/x2/")]
    payload = {
        "schema": "ghc.family.staged-review.final.v3",
        "owner": OWNER,
        "phase": PHASE,
        "staged_count_before_self": len(paths),
        "staged_paths_before_self": paths,
        "disallowed_paths": disallowed,
        "frozen_x1_or_x2_paths": frozen,
        "declared_lifecycle_self_exclusions": FINAL_SELF_EXCLUSIONS,
        "valid": not disallowed and not frozen,
    }
    write_json("validation/final-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_privacy() -> None:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    scanner_surfaces = FINAL_SOURCE_PATHS
    candidates = []
    scanned = 0
    for path in staged_paths(EVIDENCE_COMMIT):
        if path in FINAL_SELF_EXCLUSIONS or Path(path).suffix.lower() not in {".py", ".json", ".md", ".html", ".txt", ".yaml"}:
            continue
        _oid, blob = index_blob(path)
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append({"path": path, "pattern_class": "non_utf8_text", "disposition": "confirmed_payload_hit"})
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if path in scanner_surfaces else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {
        "schema": "ghc.family.staged-privacy.final.v3",
        "owner": OWNER,
        "phase": PHASE,
        "pattern_classes": sorted(patterns),
        "scanned_text_files": scanned,
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
        "self_exclusions": FINAL_SELF_EXCLUSIONS,
        "valid": not confirmed,
        "boundary": "Definitions and synthetic test fixtures are candidates rather than payload; every other match fails closed.",
    }
    write_json("validation/final-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def validation_receipt() -> None:
    json_paths = sorted(OWNER_ROOT.rglob("*.json"))
    issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": type(exc).__name__})
    docs = [path for path in OWNER_ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}]
    max_words = max((len(path.read_text(encoding="utf-8").split()) for path in docs), default=0)
    python_paths = [ROOT / path for path in staged_paths(SOURCE_FINAL) if path.endswith(".py")]
    compile_issues = []
    for path in python_paths:
        try:
            compile(path.read_text(encoding="utf-8"), path.name, "exec")
        except SyntaxError as exc:
            compile_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": str(exc)})
    frozen = git_text("diff", "--cached", "--name-only", EVIDENCE_COMMIT, "--", "docs/orin-thale/v672-v5/x1", "docs/orin-thale/v672-v5/x2", "scripts/build_ghc_family_orin_thale_v672_v5.py", "scripts/build_ghc_family_orin_thale_v672_v5_x2.py", "tests/test_ghc_family_orin_thale_v672_v5_x1.py", "tests/test_ghc_family_orin_thale_v672_v5_x2.py")
    diff = git("diff", "--cached", "--check", check=False)
    materialized = len([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts])
    payload = {
        "schema": "ghc.family.final-validation-prereceipt.v3",
        "owner": OWNER,
        "phase": PHASE,
        "json_documents": len(json_paths),
        "json_issues": issues,
        "documents": len(docs),
        "max_document_words": max_words,
        "python_compiles": len(python_paths),
        "python_compile_issues": compile_issues,
        "diff_hygiene_exit": diff.returncode,
        "frozen_x1_or_x2_changes": frozen.splitlines() if frozen else [],
        "materialized_files": materialized,
        "file_guard": 2000,
        "canonical_invoked": False,
        "full_repository_suite": "not_run_not_claimed",
        "valid": not issues and not compile_issues and diff.returncode == 0 and not frozen and max_words <= 100000 and materialized < 2000,
        "boundary": BOUNDARY,
    }
    write_json("validation/final-validation-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def precommit_test_receipt() -> None:
    result = subprocess.run([sys.executable, "-X", "utf8", "-m", "unittest", "tests.test_ghc_family_orin_thale_v672_v5_final", "-v"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=180)
    combined = result.stdout + result.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests", combined)
    count = int(match.group(1)) if match else 0
    payload = {
        "schema": "ghc.family.final-precommit-test-receipt.v3",
        "owner": OWNER,
        "phase": PHASE,
        "tests": count,
        "exit_code": result.returncode,
        "result": "passed" if result.returncode == 0 else "failed",
        "output_sha256": sha(combined.encode("utf-8")),
        "immutable_x1_tests": {"tests": 24, "result": "passed_before_x2", "rerun": False},
        "evidence_x2_tests": {"tests": 30, "result": "passed_before_final", "rerun": False},
        "full_repository_suite": "not_run_not_claimed",
        "canonical": False,
        "same_owner_only": True,
        "valid": result.returncode == 0 and count == 20,
    }
    write_json("validation/final-precommit-test-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps({**payload, "output_tail": combined[-3000:]}, ensure_ascii=False, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method-flow-ledger", type=Path)
    parser.add_argument("--manifests-from-index", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--staged-privacy", action="store_true")
    parser.add_argument("--validation-receipt", action="store_true")
    parser.add_argument("--precommit-test-receipt", action="store_true")
    args = parser.parse_args()
    if args.manifests_from_index:
        manifests_from_index()
    elif args.staged_review:
        staged_review()
    elif args.staged_privacy:
        staged_privacy()
    elif args.validation_receipt:
        validation_receipt()
    elif args.precommit_test_receipt:
        precommit_test_receipt()
    else:
        if args.method_flow_ledger is None:
            parser.error("default build requires --method-flow-ledger")
        build(args.method_flow_ledger)


if __name__ == "__main__":
    main()
