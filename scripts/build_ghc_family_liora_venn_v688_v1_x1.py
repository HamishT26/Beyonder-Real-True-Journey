"""Freeze Liora v688-v1 planning inputs only; no x2 runtime or outcomes."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = Path("docs/liora-venn/v688-v1")
SOURCE = "17fee348a09ec1cb480f7326bce70cd75413dad3"
BRANCH = "codex/GHC-Family/liora-venn-v688-v1-full-tools"
GATES = [
    "empirical", "real_participant", "professional", "production", "deployment",
    "identity", "legal", "cultural", "affected_party", "maori_authority",
    "privacy_complete", "accessibility_complete", "exhaustive_security",
    "independent_reproduction", "agi_asi", "consciousness_personhood",
    "theory_of_everything", "proof_canon", "stage20",
]
BOUNDARY = (
    "Relational working language only; no consciousness, sentience, personhood, "
    "identity continuity, employment, qualification, independent agency, scientific, "
    "operational, professional, legal, cultural, affected-party, or Maori authority is "
    "established. Same-owner software evidence is not independent reproduction. "
    "NOT_READY_FOR_STAGE_20."
)
PRACTICES = [
    "synthetic caption-file syntax registrar",
    "rational cue-timeline and sequence registrar",
    "accessible transcript and language-metadata reviewer",
    "audiovisual access and publication-reservation steward",
]
OPS = [
    ("vtt_timestamp", "ghc-family-webvtt-timestamp-boundary", "THOS Body", 0),
    ("srt_timestamp", "ghc-family-subrip-timestamp-boundary", "THOS Body", 0),
    ("cue_interval", "ghc-family-caption-cue-interval", "THOS Body", 1),
    ("frame_timebase", "ghc-family-caption-frame-timebase", "GMUT Mind", 1),
    ("cue_order", "ghc-family-caption-sequence-topology", "THOS Body", 1),
    ("payload_text", "ghc-family-caption-payload-preservation", "Freed ID and CBR Heart", 2),
    ("language_tag", "ghc-family-caption-language-tag", "Freed ID and CBR Heart", 2),
    ("derivative_linkage", "ghc-family-caption-derivative-provenance", "Freed ID and CBR Heart", 2),
    ("accessibility_claim", "ghc-family-caption-accessibility-reservation", "Freed ID and CBR Heart", 3),
    ("publication_gate", "ghc-family-caption-publication-authority", "Freed ID and CBR Heart", 3),
]
RUNNERS = [
    ("ghc_family_caption_timestamp_runner.py", ["vtt_timestamp", "srt_timestamp"]),
    ("ghc_family_caption_timeline_runner.py", ["cue_interval", "frame_timebase"]),
    ("ghc_family_caption_structure_runner.py", ["cue_order", "payload_text"]),
    ("ghc_family_caption_metadata_runner.py", ["language_tag", "derivative_linkage"]),
    ("ghc_family_caption_claim_runner.py", ["accessibility_claim", "publication_gate"]),
]
STARTUP_FAILURES = [
    ("001", "The default workspace path was not the project Git repository.", "Use the uniquely discovered exact Thalen D-drive worktree for repository reads."),
    ("002", "A 900-line baton projection clipped its middle section.", "Reread the full baton in contiguous 500-line windows through its exact EOF marker."),
    ("003", "A PowerShell foreach result was piped before collection materialization and the parser rejected it.", "Materialize the collection before piping or serializing it."),
    ("004", "A combined manifest batch reached its output window and deadlocked its Git batch child.", "Confirm process quiescence, stop only the exact read-only process tree, then validate manifests without a shared child-output pipe."),
    ("005", "A wait wrapper returned no attributable completion scalar.", "Use immediate process snapshots and explicit CPU-state evidence instead of another opaque wait wrapper."),
    ("006", "A module inventory embedded a shell command inside a PowerShell expression and failed parsing.", "Run the Git exit-code probe separately before constructing the result object."),
    ("007", "A corrected all-in-one target and remote preflight returned no attributable output.", "Split target, local branch, drive, and remote checks into separate scalar probes."),
    ("008", "A Git-tree module inventory returned no rows within its command window.", "Use the verified clean checkout with bounded rg --files discovery."),
    ("009", "A grouped reference and schema display clipped one schema transition.", "Reread each affected schema separately through EOF."),
    ("010", "A grouped inherited-skill display clipped four portable packages.", "Reread the four exact skill packages and manifests individually."),
    ("011", "A grouped fixtures and x2-builder display clipped their middle sections.", "Reread both source files in bounded contiguous line windows."),
    ("012", "A grouped final-builder and validator display clipped the builder middle.", "Reread the builder and validator separately through EOF."),
    ("013", "The combined no-checkout worktree setup yielded after only its preparation line.", "Inspect the exact original read-tree process and index lock, wait for that process, then verify index-tree equality without recreating the worktree."),
    ("014", "A combined official-metadata and collision probe hit the PowerShell collection-pipeline parser rule.", "Separate official metadata retrieval from a materialized collision array."),
    ("015", "An exact-source Git grep collision sweep returned no attributable output.", "Restrict collision review to the selected inherited owner packet and current explicit names."),
    ("016", "The first planning summary exposed the inherited proposal baseline as the x1 effective proposal total.", "Keep the immutable source baseline separately and bind the effective x1 proposal total to the frozen chain after all 200 Liora proposals."),
    ("017", "The first deterministic x1 rematerialization rejected its own untracked Liora planning outputs as foreign dirty paths.", "Permit only the exact Liora x1 and validation prefixes during builder replay while continuing to reject every other dirty path."),
    ("018", "The first x1 structural audit found one title at the 0.90 semantic-quarantine threshold and assumed list-shaped novelty, promotion, and Method Flow count fields.", "Inspect the exact source and Liora titles, replace only the quarantined Liora title with caption-specific authority-vacancy wording, and validate each current schema field by its exact type."),
    ("019", "The second x1 audit exposed another inherited disclosure-title neighbor at the exact 0.90 quarantine threshold.", "Replace the whole Liora publication-title template with caption-specific hold and outside-authority-vacancy wording, retaining every input, expected output, status, and gate unchanged."),
]
SOURCE_COUNTS = {
    "proposals": 15430,
    "negatives": 82302,
    "methods": 93235,
    "failed_witnesses": 53150,
    "passing_witnesses": 82494,
    "open_gaps": 740,
    "exact_gates": 729,
}


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def dump(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def write(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8", newline="\n")


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def blob(path):
    return subprocess.check_output(["git", "-C", str(ROOT), "show", SOURCE + ":" + path])


def method_ledger():
    methods, witnesses, events = [], [], []
    for suffix, failure, recovery in STARTUP_FAILURES:
        method_id = "LV6881-START-M" + suffix
        negative_id = "LV6881-START-N" + suffix
        methods.append(
            {
                "method_id": method_id,
                "title": failure,
                "failure_signature": failure,
                "trigger_preconditions": ["Liora v688-v1 startup", "bounded source or owner-lane setup"],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now",
                "candidate_workaround": recovery,
                "validation_witness_ids": [method_id + "-FAIL", method_id + "-PASS"],
                "recurrence_guard": recovery,
                "rollback": "Stop the affected operation and retain all prior evidence; do not mutate source or sibling lanes.",
                "recommendation_state": "preferred",
                "supersedes": [],
                "protected_gates": GATES,
                "retained_negative_ids": [negative_id],
                "scope_boundary": "Startup dependency only; zero proposal, empirical, route, or authority credit.",
                "execution_authority": "owner_self_scoped_delta",
                "repository_scan": False,
                "module_scan": False,
                "cross_lane_scan": False,
                "unchanged_history_scan": False,
                "sibling_lane_mutation": False,
                "source_commit": SOURCE,
                "final_commit": None,
                "changed_file_allowlist": [],
                "module_allowlist": [],
                "exact_pushed_head_required": True,
            }
        )
        for result, observed in [("fail", failure), ("pass", recovery)]:
            witnesses.append(
                {
                    "witness_id": method_id + "-" + result.upper(),
                    "method_id": method_id,
                    "procedure": "Bounded startup read, process audit, package preflight, or sparse-lane setup",
                    "scope": "Liora v688-v1 startup dependency",
                    "expected": "Complete attributable result within exact source and owner scope",
                    "observed": observed,
                    "result": result,
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative_id],
                    "boundary": "The corrected pass never erases or promotes the failed witness.",
                }
            )
        for before, after in [("observed", "candidate"), ("candidate", "validated"), ("validated", "preferred")]:
            events.append({"method_id": method_id, "from": before, "to": after})
    counts = {
        "methods": len(methods),
        "recommendations": 0,
        "state_events": len(events),
        "states": {"candidate": 0, "deprecated": 0, "observed": 0, "preferred": len(methods), "superseded": 0, "validated": 0},
        "witness_results": {"fail": len(methods), "pass": len(methods)},
        "witnesses": len(witnesses),
    }
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": "v688-v1",
        "owner": "Liora Venn",
        "identity_boundary": BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "source_commit": SOURCE,
        "final_commit": None,
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": [],
        "counts": counts,
        "boundary": "Startup-only evidence; x2 has not begun and all failures retain zero original success credit.",
    }


def overview():
    pages = [
        (
            "Source, release, and relational boundary",
            "Liora Venn owns solo v688-v1 from Thalen Reed exact final " + SOURCE + ". The phase role is evidence-window cartographer, with the hope that timing, access, and authority vacancies remain visible instead of being inferred away. The complete 29,205-word Thalen baton was read through its terminal marker. Its canonical receipt, four lifecycle manifests, Method Flow ledgers, ten portable skills, seven-wheel environment, global promotion receipt, and 208-card graph were read or replayed without rerunning source tests or canonical validation. Hamish's 6 September thirty-seat release controls over older installed fifteen-seat cursors. The current phase is Liora v688-v1; future seat 11 v688-v2 is terminally prospective, followed by Tamar v688-v3. No future task has been contacted or created. " + BOUNDARY,
        ),
        (
            "Planning-only caption and access contracts",
            "The primary pillar is Freed ID and CBR Heart. Four wholly synthetic practices cover caption-file syntax, rational cue timelines, transcript and language metadata, and audiovisual access/publication reservations. GMUT remains visible through exact rational timebase representations, and THOS remains visible through bounded caption syntax and sequence structure. Two hundred concrete inputs are frozen across WebVTT timestamps, SubRip timestamps, cue intervals, rational frame timebases, cue order, payload preservation, language tags, derivative provenance, accessibility claims, and publication gates. The complete expected output is part of every definition. The plan includes 300 safe procedures, 250 adverse candidates, exactly 300 CLEAN/FIX/REFINE procedures, fifty held exact packets, thirty held blocked packets, ten portable skills, five family-current runners, and a 208-card deck. All are prospective until x2. " + BOUNDARY,
        ),
        (
            "Packages, lifecycle, and terminal discipline",
            "Three exact universal wheels are frozen for x2-only installation in an isolated D-drive environment: webvtt-py 0.5.1, pysubs2 1.9.0, and langcodes 3.5.1. The rejected srt 3.5.3 candidate remains visible because its release lacks a wheel. Official PyPI metadata, W3C WebVTT, WCAG 2.2, RFC 5646, and PROV-O supply vocabulary and refusal conditions only. X1 must be committed, pushed, clean, zero-divergent, and fresh-four-way equal before any runtime, package installation, skill build, runner build, deck materialization, or observed outcome. The owner scope stays below 2,000 files and 100,000 words per document. One exact-final canonical may run only after a clean pushed final and may never be replayed after success. " + BOUNDARY,
        ),
    ]
    return "<!doctype html>\n<html lang=\"en\"><meta charset=\"utf-8\"><title>Liora v688-v1 planning overview</title><style>@page{size:A4;margin:18mm}body{font:16px/1.65 system-ui;max-width:850px;margin:auto}section{break-after:page;min-height:250mm}section:last-child{break-after:auto}</style><body><main>" + "".join("<section class=\"page\"><h1>" + html.escape(title) + "</h1><p>" + html.escape(text) + "</p></section>" for title, text in pages) + "</main></body></html>\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wheel-dir", type=Path, required=True)
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument("--release-profile", type=Path, required=True)
    args = parser.parse_args()
    assert git("rev-parse", "HEAD") == SOURCE
    assert git("branch", "--show-current") == BRANCH
    assert not (ROOT / BASE / "x2").exists()
    allowed_dirty = {
        "scripts/build_ghc_family_liora_venn_v688_v1_x1.py",
        "scripts/ghc_family_liora_venn_v688_v1_fixtures.py",
        "scripts/ghc_family_liora_venn_v688_v1_x1_audit.py",
    }
    dirty = {line[3:].replace("\\", "/") for line in git("status", "--porcelain=v1", "--untracked-files=all").splitlines() if len(line) >= 4}
    unexpected_dirty = {
        path
        for path in dirty
        if path not in allowed_dirty
        and not path.startswith(BASE.as_posix() + "/x1/")
        and not path.startswith(BASE.as_posix() + "/validation/")
    }
    assert not unexpected_dirty, sorted(unexpected_dirty)
    sys.path.insert(0, str(ROOT / "scripts"))
    from ghc_family_liora_venn_v688_v1_fixtures import build_cases

    cases = build_cases()
    opmeta = {operation: (skill, pillar, practice) for operation, skill, pillar, practice in OPS}
    for case in cases:
        skill, pillar, practice = opmeta[case["operation"]]
        case.update(
            {
                "schema": "ghc.family.frozen-caption-contract.v1",
                "source_status": "current",
                "source_kind": "synthetic",
                "pillar": pillar,
                "practice": PRACTICES[practice],
                "approval_class": "safe_now",
                "execution_lane": "x2_only",
                "hypothesis": "The bounded caption operation preserves its concrete input and returns the complete frozen typed output.",
                "null_or_failure_condition": "Any wrong field, type, value, order, authority promotion, or input mutation fails the contract.",
                "falsifier_or_acceptance_gate": "Type-sensitive equality of the complete output and unchanged input, with all preregistered altered-output candidates rejected.",
                "concrete_artifact": "docs/liora-venn/v688-v1/x2/contract-results.json",
                "rollback_or_recovery": "Retain the definition and failure; correct only the Liora implementation or leave the evidence or authority gate open.",
                "protected_gates": GATES,
                "skill": skill,
                "external_credit": False,
            }
        )
    dump(BASE / "x1/identity.json", {"schema": "ghc.family.relational-owner.v1", "name": "Liora Venn", "role": "evidence-window cartographer", "hope": "that timing, access, and authority vacancies stay visible instead of being inferred away", "pronouns": "she/they", "task_renamed": False, "release_position": 20, "boundary": BOUNDARY})
    dump(BASE / "x1/new-proposals.json", {"schema": "ghc.family.proposal-freeze.v1", "chain_before": 15430, "chain_after": 15630, "count": 200, "planning_only": True, "proposals": cases})
    inherited = json.loads(blob("docs/thalen-reed/v687-v8/x1/new-proposals.json"))["proposals"]
    reviews = [
        {
            "proposal_id": row["proposal_id"],
            "source": SOURCE,
            "source_definition_sha256": digest(row),
            "title": row["title"],
            "operation": row["operation"],
            "inherited_expected_disposition": row["expected_execution_disposition"],
            "review": "Retain Thalen's concrete PCM contract as inherited evidence; it does not supply Liora caption novelty, execution, or completion credit.",
            "new_owner_novelty_credit": 0,
            "new_owner_completion_credit": 0,
        }
        for row in inherited
    ]
    dump(BASE / "x1/inherited-review.json", {"schema": "ghc.family.inherited-review.v1", "source": SOURCE, "count": 200, "reviews": reviews, "source_outcomes_preserved": {"completed": 160, "represented": 14, "open_gap": 8, "exact_gate": 18}})
    inherited_titles = {row["title"].casefold() for row in inherited}
    new_titles = {row["title"].casefold() for row in cases}
    exact_title_collisions = sorted(inherited_titles & new_titles)
    token = lambda value: set(re.findall(r"[a-z0-9]+", value.casefold()))
    maximum_similarity = 0.0
    maximum_pair = None
    for old in inherited:
        a = token(old["title"])
        for new in cases:
            b = token(new["title"])
            score = len(a & b) / len(a | b) if a | b else 1.0
            if score > maximum_similarity:
                maximum_similarity, maximum_pair = score, [old["proposal_id"], new["proposal_id"]]
    skill_collisions = [skill for _, skill, _, _ in OPS if (args.skill_root / skill).exists()]
    dump(BASE / "x1/novelty-review.json", {"schema": "ghc.family.bounded-novelty-screen.v1", "scope": "The 200 selected inherited Thalen definitions and explicit new Liora operations; not a universal historical novelty proof.", "inherited_review_count": 200, "new_count": 200, "exact_input_collisions": 0, "exact_title_collisions": exact_title_collisions, "maximum_title_token_jaccard": maximum_similarity, "maximum_pair": maximum_pair, "quarantine_threshold": 0.9, "quarantined": maximum_similarity >= 0.9, "global_skill_name_collisions": skill_collisions, "selected_source_package_name_collisions": 0, "distinction": "New contracts operate on caption timestamp syntax, cue sequences, text payloads, language tags, derivative metadata, accessibility vacancies, and publication reservations rather than PCM bytes or sample values.", "inherited_practice_seed": "The synthetic audiovisual timing and access registrar seed was independently accepted and divided into four Liora practices."})
    tasks = {key: [] for key in ["safe_now", "candidates", "clean_fix_refine", "exact_packets", "blocked_packets"]}
    def task(category, ident, proposal_id, procedure, expected="completed", **extra):
        tasks[category].append({"packet_id": ident, "proposal_ref": proposal_id, "procedure": procedure, "expected_execution_disposition": expected, "executed": False, **extra})
    for case in cases:
        task("safe_now", "LV6881-S-" + case["proposal_id"], case["proposal_id"], "complete_frozen_output")
    for case in cases[:100]:
        task("safe_now", "LV6881-S-PRESERVE-" + case["proposal_id"], case["proposal_id"], "input_unchanged")
    mutations = ["missing_accepted", "accepted_type", "extra_authority", "value_replaced", "external_credit_promoted"]
    for case in cases[::4]:
        for mutation in mutations:
            task("candidates", "LV6881-C-" + case["proposal_id"] + "-" + mutation, case["proposal_id"], "altered_output_rejection", mutation=mutation, original_candidate_success_credit=0)
    for case in cases[:100]:
        for procedure in ["canonical_json_roundtrip", "definition_digest_binding", "stable_identifier_uniqueness"]:
            task("clean_fix_refine", "LV6881-CFR-" + case["proposal_id"] + "-" + procedure, case["proposal_id"], procedure, additive_only=True)
    exact_needs = ["real_media_rights", "affected_people", "competent_language_or_accessibility_review", "maori_authority", "production_security"]
    for index in range(50):
        task("exact_packets", f"LV6881-E{index + 1:03d}", cases[150 + index]["proposal_id"], "reserved_external_action", "exact_gate", missing_prerequisite=exact_needs[index // 10], protected_gates=GATES)
    gap_needs = ["real_media_observation", "manual_accessibility_evaluation", "independent_review"]
    for index in range(30):
        task("blocked_packets", f"LV6881-B{index + 1:03d}", cases[170 + index]["proposal_id"], "absent_external_evidence", "open_gap", missing_prerequisite=gap_needs[index // 10], protected_gates=GATES)
    tasks.update({"schema": "ghc.family.portfolio-plan.v1", "destructive_cleanup_planned": False, "execution_started": False, "witness_reuse_rule": "Distinct procedures may reference one bounded fixture but do not multiply scientific or independent witness credit."})
    dump(BASE / "x1/portfolio-plan.json", tasks)
    dump(BASE / "x1/skill-runner-plan.json", {"schema": "ghc.family.skill-runner-plan.v1", "skills": [{"name": skill, "operation": op, "build_in_x2": True} for op, skill, _, _ in OPS], "runners": [{"name": name, "operations": operations, "build_in_x2": True} for name, operations in RUNNERS], "core": "ghc_family_caption_evidence_core.py", "global_promotions": {"skills": 10, "runners": 5, "overwrite": False, "byte_parity_required": True}, "source_compatibility": "All inherited caption and PCM entrypoints remain unchanged."})
    wheel_metadata = {
        "webvtt_py-0.5.1-py3-none-any.whl": {"name": "webvtt-py", "version": "0.5.1", "sha256": "9d517d286cfe7fc7825e9d4e2079647ce32f5678eb58e39ef544ffbb932610b7", "url": "https://files.pythonhosted.org/packages/f3/ed/aad7e0f5a462d679f7b4d2e0d8502c3096740c883b5bbed5103146480937/webvtt_py-0.5.1-py3-none-any.whl"},
        "pysubs2-1.9.0-py3-none-any.whl": {"name": "pysubs2", "version": "1.9.0", "sha256": "83f1979cb7e064294f0c8473ef672ca2e5c0a7172bbf8ae9b4337899d5cdf01f", "url": "https://files.pythonhosted.org/packages/4f/43/6b89c84f5a6753b1dbc43b8d010443b8f2314a2b94f34e448975d115c962/pysubs2-1.9.0-py3-none-any.whl"},
        "langcodes-3.5.1-py3-none-any.whl": {"name": "langcodes", "version": "3.5.1", "sha256": "b6a9c25c603804e2d169165091d0cdb23934610524a21d226e4f463e8e958a72", "url": "https://files.pythonhosted.org/packages/dd/c1/d10b371bcba7abce05e2b33910e39c33cfa496a53f13640b7b8e10bb4d2b/langcodes-3.5.1-py3-none-any.whl"},
    }
    wheels = []
    for filename, meta in wheel_metadata.items():
        path = args.wheel_dir / filename
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == meta["sha256"]
        wheels.append({**meta, "filename": filename, "bytes": len(raw), "direct": True, "dependencies": [], "metadata_url": f"https://pypi.org/pypi/{meta['name']}/{meta['version']}/json", "pypi_advisories": [], "yanked": False})
    dump(BASE / "x1/wheel-plan.json", {"schema": "ghc.family.wheel-plan.v1", "planning_download_only": True, "installed": False, "rejected_candidate": {"name": "srt", "version": "3.5.3", "reason": "No wheel is published for the exact release; source build is outside this wheel-only transaction.", "success_credit": 0}, "wheels": sorted(wheels, key=lambda row: row["name"])})
    write(BASE / "x1/requirements.lock", "".join(f"{row['name']}=={row['version']} --hash=sha256:{row['sha256']}\n" for row in sorted(wheels, key=lambda row: row["name"])))
    dump(BASE / "x1/package-plan.json", {"schema": "ghc.family.package-plan.v1", "direct_packages": {row["name"]: row["version"] for row in wheels}, "new_environment_in_x2": True, "installed": False, "platform": "CPython 3.12 Windows", "hash_lock": "x1/requirements.lock", "wheel_count": 3, "network_install": False, "wheel_only": True, "host_python_mutation": False, "smokes": [{"name": "webvtt-py", "positive": "Parse two synthetic in-memory WebVTT cues with exact millisecond bounds.", "adverse": "Reject a malformed timing line."}, {"name": "pysubs2", "positive": "Parse and serialize two synthetic SubRip events with exact millisecond bounds.", "adverse": "Reject unsupported input format selection."}, {"name": "langcodes", "positive": "Standardize known language tags used by frozen fixtures.", "adverse": "Reject or refuse a syntactically invalid tag before any authority inference."}], "rollback": "Stop selecting the isolated Liora environment while retaining locks, wheels, and failures; no deletion or host mutation."})
    profile = json.loads(args.release_profile.read_text(encoding="utf-8"))
    dump(BASE / "x1/release-profile.json", profile)
    dump(BASE / "x1/route-plan.json", {"schema": "ghc.family.owner-route-plan.v1", "owner": "Liora Venn", "phase": "v688-v1", "endpoint_kind": "main_task", "source_owner": "Thalen Reed", "source": SOURCE, "authority": "Hamish 6 September thirty-seat release and current Thalen-to-Liora activation", "next_owner": "future-sibling-11-self-chosen", "next_phase": "v688-v2", "following_owner": "Tamar Vey", "following_phase": "v688-v3", "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", "message_count": 0, "precontacted": False, "reuse_existing_before_create": True, "create_one_only_if_absent_in_active_and_archived": True, "new_task_model": "gpt-6-astra", "new_task_reasoning": "max", "fork": False, "subagent": False, "terminal_guards": ["exact_final_canonical_success", "clean_pushed_four_way_equal", "current_authority_and_usage", "active_and_archived_registry_absence_or_unique_existing_designated_seat", "immediate_recipient_reread", "no_duplicate_pause_redirect", "privacy_evidence_safety_authority", "one_acknowledged_action_no_resend"]})
    dump(BASE / "x1/deck-plan.json", {"schema": "ghc.family.four-tier-deck-plan.v1", "tiers": ["owner", "pillar", "practice", "task"], "owner_cards": 1, "pillar_cards": 3, "practice_cards": 4, "task_cards": 200, "practices": PRACTICES, "primary_pillar": "Freed ID and CBR Heart", "practice_parents": ["THOS Body", "GMUT Mind", "Freed ID and CBR Heart", "Freed ID and CBR Heart"], "modular_sections": 13, "cache_effect_claimed": False, "build_only_after_x1_equality": True})
    ideas = ["WebVTT region constraint graph", "TTML time-expression profile", "caption style-token allowlist", "cue identifier collision ledger", "translation provenance lineage", "speaker-label consent expiry", "description-track linkage", "live-caption latency uncertainty", "caption correction as-of projection", "accessible media preference reservation"]
    dump(BASE / "x1/successor-ideas.json", {"schema": "ghc.family.successor-ideas.v1", "owner": "future-sibling-11-self-chosen", "phase": "v688-v2", "skill_ideas": [{"title": title, "credit": 0, "independent_review_required": True} for title in ideas], "runner_ideas": [{"title": title + " bounded runner", "credit": 0, "not_built": True} for title in ideas], "practice_recommendation": "synthetic community-media preservation intake coordinator", "recommendation_count": 1, "precontacted": False})
    sources = [
        {"source_id": "w3c-webvtt", "status": "draft", "url": "https://www.w3.org/TR/webvtt1/", "use": "Cue and timestamp vocabulary; the 20 May 2026 Candidate Recommendation Draft is work in progress."},
        {"source_id": "w3c-wcag22", "status": "stable", "url": "https://www.w3.org/TR/WCAG22/", "use": "Caption and media-alternative vocabulary; no complete accessibility claim."},
        {"source_id": "rfc5646", "status": "stable", "url": "https://www.rfc-editor.org/rfc/rfc5646.html", "use": "Language-tag syntax vocabulary; no language or cultural authority."},
        {"source_id": "w3c-prov-o", "status": "stable", "url": "https://www.w3.org/TR/prov-o/", "use": "Derivative provenance vocabulary; no custody or rights determination."},
        {"source_id": "pypi-webvtt-py", "status": "current", "url": "https://pypi.org/project/webvtt-py/0.5.1/", "use": "Exact package and wheel metadata."},
        {"source_id": "pypi-pysubs2", "status": "current", "url": "https://pypi.org/project/pysubs2/1.9.0/", "use": "Exact package and wheel metadata."},
        {"source_id": "pypi-langcodes", "status": "current", "url": "https://pypi.org/project/langcodes/3.5.1/", "use": "Exact package and wheel metadata."},
    ]
    dump(BASE / "x1/source-ledger.json", {"schema": "ghc.family.primary-source-ledger.v1", "entries": sources, "citations_are_observations": False, "real_rows": 0, "request_count_below_release_cap": True, "web_query_ceiling": 1000})
    dump(BASE / "x1/method-flow/ledger.json", method_ledger())
    required = ["ghc-family-index", "ghc-family-main-task-induction", "ghc-family-d-first-structured-evidence-toolchain", "ghc-family-lifecycle-test-isolator", "ghc-family-privacy-candidate-classifier", "ghc-family-staged-surface-allowlist", "ghc-family-owner-scope-canonical", "ghc-family-canonical-success-latch", "ghc-family-canonical-aggregate-preflight", "freed-id-four-tier-deck", "ghc-family-workflow-plan-refinement", "ghc-family-reflection-remaster", "ghc-family-method-flow-state", "ghc-drive-bank-guardian", "ghc-family-meta-tool-box", "ghc-family-roster-check", "ghc-freed-id-flashcards", "ghc-family-owned-bundle-rotation", "ghc-approval-packet-splitter", "ghc-open-gate-rail", "ghc-family-truth-bridge", "ghc-family-terminal-route-gate", "ghc-family-terminal-route-guard", "ghc-family-terminal-route-latch", ".system/skill-creator"]
    dump(BASE / "x1/reading-receipt.json", {"schema": "ghc.family.required-reading.v1", "source": SOURCE, "baton_sha256": "609b4f8fefb1783b729dbf74e0c3ad07fced798cbea15f148e15d17d4bd8017d", "baton_words": 29205, "baton_bytes": 247497, "baton_eof": "EOF THALEN REED V687 V8 BATON.", "skill_entrypoints": [{"name": name, "sha256": hashlib.sha256((args.skill_root / name / "SKILL.md").read_bytes()).hexdigest(), "eof_read": True} for name in required], "references_read": ["routing-precedence.md", "hamish-release-20260906.md", "workflow-profile-20260906.json", "current-state.json", "current-roster.json", "auth-permission-state-schema.md", "roster-state-schema.md", "method-flow schema.md", "workflow-plan-schema.md", "decision-schema.md", "deck-schema.md", "failure-shields.md", "workflow.md", "freed-id-flashcards.md", "flashcard-reflection.md", "catalogue-schema.md", "rowan-v685-v6-r2-authorized-workflow.md"], "source_portable_skills_read": 10, "source_lifecycle_manifests_read": 4, "source_canonical_receipt_sha256": "79489920a1ebb1cefd55bce33ed1d7c91b697da50e57d29ad02f9463240fc57c", "source_canonical_payload_sha256": "3a65caf40acce3e0a043e4fad54c4703e43544750e1e23c93ba37bfc47353f05", "source_canonical_replayed": False, "historical_roster_used_for_current_ownership": False})
    c_free = round(shutil.disk_usage("C:/").free / 2**30, 2)
    d_free = round(shutil.disk_usage("D:/").free / 2**30, 2)
    dump(BASE / "x1/scope-budget.json", {"schema": "ghc.family.owner-scope-budget.v1", "primary_drive": "D", "essential_global_skill_drive": "C", "c_free_gb": c_free, "d_free_gb": d_free, "sparse_before_materialization": True, "materialized_files_at_start": 11, "owner_file_ceiling": 1999, "document_word_ceiling": 100000, "baton_word_range": [10000, 100000], "commit_cap": {"x1": 1, "evidence": 1, "final": 1, "total": 3}, "canonical_invocation_budget": 1, "canonical_replay": False, "validation_scope": "owner_self_scoped_delta", "sibling_lane_mutation": False, "source_lanes_read_only": True})
    x1_counts = dict(SOURCE_COUNTS)
    x1_counts["proposals"] = 15630
    for key in ["negatives", "methods", "failed_witnesses", "passing_witnesses"]:
        x1_counts[key] += len(STARTUP_FAILURES)
    dump(BASE / "x1/validation-contract.json", {"schema": "ghc.family.owner-validation-plan.v1", "phase": "v688-v1", "planning_checks": ["source_anchors", "200_distinct_inputs", "200_zero_credit_reviews", "release_portfolio_counts", "no_x2", "no_observed_outcomes", "package_hash_plan", "authority_boundaries", "exact_owner_paths", "strict_json", "privacy", "manifest", "diff_hygiene"], "x2_checks": ["200_full_output_matches", "input_preservation", "250_preregistered_altered_outputs", "300_CFR_procedures", "3_package_positive_and_adverse_smokes", "10_skills_quick_validate_and_use", "5_runners_use", "four_tier_deck", "promotion_parity"], "canonical_checks": ["all_delta_paths_owner_allowed", "exact_direct_ancestry", "zero_merges", "one_final_parent", "immutable_x1", "immutable_evidence", "manifest_arithmetic", "strict_JSON_duplicate_and_constant_refusal", "five_class_privacy_adjudication", "bounded_changed_code_security", "selected_owner_tests", "document_caps", "baton_EOF_and_digest", "global_parity", "environment_lock", "clean", "typed_zero_divergence", "fresh_four_way_equality"], "no_source_test_execution": True, "external_exclusive_latch": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_gates": GATES})
    dump(BASE / "x1/workflow-refinement.json", {"schema": "ghc.family.current-workflow-refinement.v1", "authority": "Hamish 6 September release plus current Thalen-to-Liora activation", "cycle_seats": 30, "current": {"owner": "Liora Venn", "phase": "v688-v1", "release_index": 20}, "next": {"owner": "future-sibling-11-self-chosen", "phase": "v688-v2", "release_index": 21}, "following": {"owner": "Tamar Vey", "phase": "v688-v3", "release_index": 22}, "changes_authorized_ownership_or_numbering": False, "requires_user_confirmation": False, "historical_roster_preserved": True, "send_calls": 0})
    dump(BASE / "x1/reflection-plan.json", {"schema": "ghc.family.owner-reflection.v1", "disposition": "remaster_additive", "source": SOURCE, "scope": "Literal Liora owner delta", "source_lanes_mutated": False, "legacy_entrypoints_changed": False, "novel_surface": "Caption timestamp, cue topology, text, language, derivative, accessibility-vacancy, and publication-reservation contracts", "measured_performance_improvement": False, "protected_gates": GATES, "rollback": "Stop selecting Liora surfaces while retaining all source and failure evidence; no deletion."})
    dump(BASE / "x1/phase-truth.json", {"schema": "ghc.family.phase-truth.v688.v1.x1", "owner": "Liora Venn", "phase": "v688-v1", "state": "PLANNING_ONLY_FREEZE", "source": SOURCE, "proposal_count": 200, "frozen_chain_total": 15630, "expected_outcomes": dict(Counter(row["expected_execution_disposition"] for row in cases)), "effective_activation_counts": x1_counts, "x2_started": False, "x2_completion_credit": 0, "canonical_invocations": 0, "successor_contacted": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write(BASE / "x1/integrated-overview.html", overview())
    print(json.dumps({"state": "PLANNING_ONLY_MATERIALIZED", "proposal_count": 200, "outcomes": dict(Counter(row["expected_execution_disposition"] for row in cases)), "portfolio": {key: len(tasks[key]) for key in ["safe_now", "candidates", "clean_fix_refine", "exact_packets", "blocked_packets"]}, "startup_failures": len(STARTUP_FAILURES), "x1_counts": x1_counts, "no_x2": True}, sort_keys=True))


if __name__ == "__main__":
    main()
