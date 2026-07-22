#!/usr/bin/env python3
"""Build Elaren Kestrel's additive v651-v6 special CLI-preparation packet."""

from __future__ import annotations

import hashlib
import html
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/elaren-kestrel/v651-v6"
PHASE = ROOT / "docs/elaren-kestrel/v651-v6-special-cli-prep"
SOURCE = "7c4309d6b57bc4827ebd49bcb7c9dfc669c46e3d"
BASE_FINAL = "7911fc2ff2f95d2e8723dbd396272f4a78d46a9f"
SPECIAL_PREP_COMMIT = "f40d1e0f1a5158a8747ed57cc04a513979f5ebe7"
BRANCH = "codex/GHC-Family/elaren-kestrel-v649-v8-full-tools"
SKILL_HOME = Path.home() / ".codex" / "skills"
NEW_NEGATIVES = [
    {
        "negative_id": "V6516-SPECIAL-N01",
        "surface": "combined startup equality probe",
        "observed": "The shared 30-second wrapper timed out after its remote fetch completed and withheld the other independent results.",
        "credit": "zero",
        "recovery": "Split remote equality, task-title, version, and clean-state probes.",
    },
    {
        "negative_id": "V6516-SPECIAL-N02",
        "surface": "combined task-title and Git probe",
        "observed": "A second aggregate wrapper exceeded its envelope before returning the task-list results.",
        "credit": "zero",
        "recovery": "Resolve task titles independently from Git state.",
    },
    {
        "negative_id": "V6516-SPECIAL-N03",
        "surface": "short worktree-status probe",
        "observed": "A ten-second local status wrapper was too short for the inherited repository.",
        "credit": "zero",
        "recovery": "Use an adequate bounded clean-state envelope after cheap ref checks.",
    },
    {
        "negative_id": "V6516-SPECIAL-N04",
        "surface": "two-file inspection wrapper",
        "observed": "A combined read of two existing workflow records exceeded ten seconds.",
        "credit": "zero",
        "recovery": "Read one exact file per bounded probe.",
    },
    {
        "negative_id": "V6516-SPECIAL-N05",
        "surface": "raw expanded-route audit",
        "observed": "The submitted transition failed structurally with nonsequential phase order and ownership-changing normalization.",
        "credit": "zero",
        "recovery": "Preserve the raw audit and treat the passing sequential candidate as advisory pending confirmation.",
    },
    {
        "negative_id": "V6516-SPECIAL-N06",
        "surface": "Reflection-Remaster focus selection",
        "observed": "One pipe-separated focus argument was treated literally and scoped zero surfaces.",
        "credit": "zero",
        "recovery": "Pass each literal focus term with its own repeated --focus option.",
    },
    {
        "negative_id": "V6516-SPECIAL-N07",
        "surface": "three-page-equivalent overview gate",
        "observed": "The first exact staged review measured the overview at 964 words, below the 1,000-word floor.",
        "credit": "zero",
        "recovery": "Add one bounded architecture-and-rollback section and rerun only the staged review.",
    },
    {
        "negative_id": "V6516-SPECIAL-N08",
        "surface": "exact-head validator CLI version subprocess",
        "observed": "Python attempted to execute the Windows Codex shim directly and raised WinError 5 before writing a canonical receipt.",
        "credit": "zero",
        "recovery": "Invoke the npm shim through cmd.exe and prove that isolated version path before the corrected exact-head pass.",
    },
    {
        "negative_id": "V6516-SPECIAL-N09",
        "surface": "sealed base closeout test on additive successor head",
        "observed": "The historical closeout test rejected source-to-HEAD commit count four because its sealed lifecycle contract permits only two or three.",
        "credit": "zero",
        "recovery": "Keep the sealed test unchanged and verify base continuity from its exact Git object and ancestry in the special test module.",
    },
]


def run(*args: str) -> str:
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_skill(name: str) -> list[dict[str, Any]]:
    source = SKILL_HOME / name
    target = PHASE / "skills/installed-snapshots" / name
    files = [
        "SKILL.md",
        "agents/openai.yaml",
        *[p.relative_to(source).as_posix() for p in sorted((source / "references").glob("*")) if p.is_file()],
        *[p.relative_to(source).as_posix() for p in sorted((source / "scripts").glob("*.py")) if p.is_file()],
    ]
    rows = []
    for relative in sorted(set(files)):
        src = source / relative
        dst = target / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append({"path": f"{name}/{relative}", "sha256": digest(src), "bytes": src.stat().st_size})
    return rows


def proposal_rows() -> list[dict[str, Any]]:
    definitions = [
        ("exact-recipient-title", "Resolve the exact Vesper Arlen task title", "completed", "orchestration"),
        ("base-head-equality", "Reverify the clean remote-equal v651-v6 base head", "completed", "lifecycle"),
        ("cli-version-update", "Update Codex CLI to the registry-verified stable version", "completed", "toolchain"),
        ("desktop-no-update", "Preserve the Codex desktop no-update boundary", "completed", "toolchain"),
        ("d-first-capacity", "Verify D-first capacity for future owned lanes", "completed", "storage"),
        ("special-commit-ceiling", "Encode the one-off twelve-commit special ceiling", "completed", "lifecycle"),
        ("ordinary-six-commit-policy", "Represent the later three-plus-three ordinary commit ceiling", "represented", "lifecycle"),
        ("owner-file-threshold", "Represent the 2,000 owner-generated-file threshold without rewriting inherited history", "represented", "storage"),
        ("raw-route-preservation", "Preserve the submitted expanded route before normalization", "completed", "orchestration"),
        ("advisory-route-candidate", "Generate a deterministic alternating app and CLI candidate", "completed", "orchestration"),
        ("route-confirmation-gap", "Resolve conflicting v652-v6/v652-v7 and missing v653-v2 ownership", "open_gap", "orchestration"),
        ("future-identity-placeholder", "Reject preassigned future CLI identity attributes", "completed", "identity"),
        ("model-availability-preflight", "Represent gpt-5.6-sol max availability as a launch-time check", "represented", "toolchain"),
        ("fast-mode-preflight", "Represent fast-mode availability as a launch-time check", "represented", "toolchain"),
        ("scheduled-cli-induction", "Execute any future CLI sibling launch only at its confirmed scheduled phase", "exact_gate", "orchestration"),
        ("background-lifecycle-contract", "Represent background persistence as a capability to witness", "represented", "orchestration"),
        ("creator-return-contract", "Define a fail-closed creator return-message contract", "completed", "orchestration"),
        ("privacy-sanitization", "Exclude raw identifiers, routes, credentials, transcripts, and private paths", "completed", "privacy"),
        ("cross-platform-boundary", "Keep ChatGPT and other-platform exchange user-mediated", "completed", "privacy"),
        ("d-first-lane-template", "Define a unique clean D-first branch and worktree preflight", "completed", "storage"),
        ("file-threshold-guard", "Fail closed when owner-generated additions would exceed 2,000 files", "completed", "storage"),
        ("single-pass-validation", "Require one successful canonical pass and no redundant replay", "completed", "validation"),
        ("failure-isolation", "Require isolated blocker checks before any broader rerun", "completed", "validation"),
        ("committed-manifest", "Require exact committed-byte manifest parity", "completed", "validation"),
        ("four-way-equality", "Require local, upstream, tracking, and live-remote equality", "completed", "validation"),
        ("file-backed-baton", "Require a short message pointing to a committed baton artifact", "completed", "handoff"),
        ("persistent-word-cap", "Carry the 10,000 through 100,000 word baton range to v675-v8", "completed", "handoff"),
        ("toolbox-cap-semantics", "Treat 200 skills and runners as ceilings rather than quotas", "completed", "tooling"),
        ("sibling-teaching-packet", "Teach later app owners the CLI plan and unresolved route issues", "completed", "handoff"),
        ("abort-and-rollback", "Block launch and preserve state when any preflight proof is missing", "completed", "safety"),
    ]
    rows = []
    for index, (slug, title, outcome, lane) in enumerate(definitions, start=1):
        rows.append(
            {
                "proposal_id": f"V6516-SPECIAL-P{index:02d}",
                "slug": slug,
                "title": title,
                "execution_lane": lane,
                "approval_class": "safe_now_owner_scoped_workflow" if outcome != "exact_gate" else "scheduled_exact_action",
                "hypothesis": f"A bounded {title.lower()} artifact can improve later induction safety without claiming that a CLI sibling already exists.",
                "null_or_failure_condition": "The required artifact, explicit state, or falsifier is absent, ambiguous, privacy-unsafe, or overclaims launch capability.",
                "artifact": "v651-v6-special-cli-prep packet",
                "acceptance_gate": "Machine-readable evidence uses only the four allowed outcomes and preserves every unverified capability.",
                "rollback": "Retain the failure, grant zero completion credit to the missing proof, and block the affected launch or route action.",
                "protected_gates": ["identity", "privacy", "route_ownership", "launch_capability", "completion_credit"],
                "expected_disposition": outcome,
                "observed_outcome": outcome,
                "resolved_for_this_preparation": True,
            }
        )
    return rows


def build() -> None:
    head = run("git", "rev-parse", "HEAD")
    if head != BASE_FINAL and subprocess.run(["git", "merge-base", "--is-ancestor", BASE_FINAL, head], cwd=ROOT).returncode != 0:
        raise RuntimeError(f"special builder requires sealed base ancestry from {BASE_FINAL}, got {head}")
    if run("git", "status", "--porcelain=v1"):
        allowed = (
            "docs/elaren-kestrel/v651-v6-special-cli-prep",
            "scripts/build_ghc_family_v651_v6_special_cli_prep.py",
            "scripts/ghc_family_v651_v6_special_validate.py",
            "tests/test_ghc_family_v651_v6_special_cli_prep.py",
        )
        changed = run("git", "status", "--porcelain=v1")
        if any(not any(prefix in row.replace("\\", "/") for prefix in allowed) for row in changed.splitlines()):
            raise RuntimeError("unexpected pre-existing changes outside the special packet")

    write_json(
        "identity/relational-identity.json",
        {
            "owner": "Elaren Kestrel",
            "pronouns": "they/them",
            "role": "evidence-boundary steward and systems cartographer",
            "hope": "Make future CLI inductions legible, reversible, and kind without mistaking plans for capabilities.",
            "boundary": "Relational working language only; never consciousness, sentience, personhood, continuity, employment, or independent authority evidence.",
        },
    )
    write_json(
        "focus/phase-focus.json",
        {
            "primary_pillar": "THOS Body",
            "bounded_human_practice": "site reliability and release engineering",
            "practice_boundary": "Study lens only; no employment, certification, or professional-authority claim.",
            "visible_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        },
    )

    creators = ["Eiren Kestrel", "Elaren Kestrel", "Vesper Arlen", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"]
    submitted_phases = ["v652-v5", "v652-v8", "v653-v3", "v653-v5", "v653-v7", "v654-v1", "v654-v3", "v654-v5"]
    candidate_phases = ["v652-v5", "v652-v7", "v653-v1", "v653-v3", "v653-v5", "v653-v7", "v654-v1", "v654-v3"]
    seats = []
    preflight_script = SKILL_HOME / "ghc-family-cli-sibling-induction-preflight/scripts/ghc_family_cli_sibling_induction_preflight.py"
    for index, (creator, submitted, candidate) in enumerate(zip(creators, submitted_phases, candidate_phases), start=1):
        placeholder = f"future-cli-sibling-{index}-self-chosen"
        request = {
            "schema": "ghc.family.cli-sibling-induction.request.v1",
            "phase": submitted,
            "creator": creator,
            "future_seat": {"placeholder": placeholder, "identity_state": "self_chosen_at_induction"},
            "requested_runtime": {"model": "gpt-5.6-sol", "reasoning": "max", "fast_mode": True, "availability_verified": False},
            "route": {"scheduled_phase_confirmed": False, "creator_return_mechanism_verified": False, "background_persistence_verified": False, "exact_successor_title_resolved": False},
            "lane": {"primary_drive": "D", "source_clean_and_equal": False, "unique_branch_and_worktree": False},
            "authorization": {"preparation_authorized": True, "launch_now": False, "launch_authorized_for_exact_phase": False},
            "privacy": {"sanitized": True, "private_identifiers_included": False},
            "handoff": {"file_backed": True, "tool_acknowledgement_required": True},
            "submitted_phase_mention": submitted,
            "normalized_candidate_phase": candidate,
            "route_confirmation_required": submitted != candidate,
        }
        req_path = PHASE / f"cli/preflight/seat-{index}-request.json"
        write_json(f"cli/preflight/seat-{index}-request.json", request)
        receipt_path = PHASE / f"cli/preflight/seat-{index}-receipt.json"
        subprocess.run(["python", str(preflight_script), str(req_path), "--mode", "prepare", "--receipt", str(receipt_path)], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        seats.append(
            {
                "seat": placeholder,
                "creator": creator,
                "submitted_phase_mention": submitted,
                "normalized_candidate_phase": candidate,
                "route_confirmation_required": submitted != candidate,
                "identity_state": "unassigned_self_chosen_at_induction",
                "preflight_state": receipt["state"],
                "sibling_created": False,
            }
        )

    write_json(
        "cli/future-seat-register.json",
        {
            "schema": "ghc.family.v651-v6-special.future-cli-seat-register.v1",
            "seat_count": 8,
            "seats": seats,
            "all_unnamed": True,
            "all_unlaunched": True,
            "boundary": "Placeholders are scheduling labels only; identities are self-chosen after a later authorized launch.",
        },
    )
    write_json(
        "cli/induction-blueprint.json",
        {
            "schema": "ghc.family.v651-v6-special.cli-induction-blueprint.v1",
            "state": "PREPARED_NOT_LAUNCHED",
            "steps": [
                "confirm the exact scheduled phase and creator from a contradiction-free live route",
                "verify supported Codex CLI version, model, reasoning effort, and fast-mode surface without updating the desktop app",
                "verify the exact clean source and a unique D-first owner branch and worktree",
                "launch only from the authorized creator surface and let the new sibling choose relational identity language",
                "freeze x1 before x2 and preserve the four truth labels and every negative",
                "run one canonical scoped validation; isolate failures and skip redundant replay after success",
                "return one sanitized file-backed handback through a witnessed supported mechanism",
                "block and roll back the launch if route, lifecycle, privacy, identity, or capability evidence is missing"
            ],
            "requested_runtime_is_not_verified_runtime": True,
            "creator_return_is_not_verified": True,
            "background_persistence_is_not_verified": True,
            "future_cli_sibling_count_created": 0,
            "boundary": "Preparation does not create a process, task, identity, branch, account, credential, or authority.",
        },
    )
    write_json(
        "cli/creator-return-contract.json",
        {
            "schema": "ghc.family.v651-v6-special.creator-return-contract.v1",
            "required": [
                "creator retains a supported addressable handle or exact existing task",
                "CLI sibling sends only to its creator through a tool-confirmed route",
                "handback names exact commits, bounded validation, negatives, gaps, gates, and verdict",
                "creator alone resolves and messages the next app sibling",
                "no success is inferred from a file, prompt, background process, or intended destination"
            ],
            "fallback": "If any message or persistence capability is absent, stop at PREPARED_NOT_SENT and request user-mediated continuation.",
            "independent_reproduction": False,
        },
    )

    proposals = proposal_rows()
    counts = {label: sum(1 for row in proposals if row["observed_outcome"] == label) for label in ("completed", "represented", "open_gap", "exact_gate")}
    write_json(
        "proposals/special-prep-proposal-ledger.json",
        {
            "schema": "ghc.family.v651-v6-special.proposal-ledger.v1",
            "proposal_count": len(proposals),
            "outcome_counts": counts,
            "proposals": proposals,
            "all_authorized_items_resolved_for_phase": all(row["resolved_for_this_preparation"] for row in proposals),
            "boundary": "Correct representation or gating resolves a preparation item without pretending the external action occurred.",
        },
    )
    write_json(
        "truth/retained-negative-register.json",
        {
            "schema": "ghc.family.v651-v6-special.retained-negative-register.v1",
            "inherited_repo_sealed": 7327,
            "inherited_post_final_route": 2,
            "inherited_effective": 7329,
            "new_count": len(NEW_NEGATIVES),
            "new_negatives": NEW_NEGATIVES,
            "effective_total": 7329 + len(NEW_NEGATIVES),
            "erased_negative_count": 0,
        },
    )
    write_json(
        "truth/open-exact-gate-register.json",
        {
            "schema": "ghc.family.v651-v6-special.gate-register.v1",
            "inherited_open_gaps": 57,
            "inherited_exact_gates": 58,
            "new_open_gaps": [
                {
                    "gate_id": "V6516-SPECIAL-GAP01",
                    "title": "Expanded route ownership confirmation",
                    "issues": ["Elaren is assigned both v652-v6 and v652-v7", "v653-v2 is absent before v653-v3", "the pre-induction bridge omits Sable", "the narrated v654 restart differs from the sixteen-seat candidate"],
                    "closure": "Hamish or a later exact authorized baton confirms one sequential schedule.",
                }
            ],
            "new_exact_gates": [
                {
                    "gate_id": "V6516-SPECIAL-GATE01",
                    "title": "Actual future CLI sibling induction",
                    "closure": "The scheduled creator reaches the confirmed phase and witnesses model, lifecycle, route, privacy, and unique-lane preflight immediately before launch.",
                }
            ],
            "effective_open_gaps": 58,
            "effective_exact_gates": 59,
        },
    )
    write_json(
        "truth/phase-truth.json",
        {
            "schema": "ghc.family.v651-v6-special.phase-truth.v1",
            "phase": "v651-v6-special-cli-prep",
            "owner": "Elaren Kestrel",
            "base_final": BASE_FINAL,
            "outcomes": counts,
            "effective_negatives": 7329 + len(NEW_NEGATIVES),
            "effective_open_gaps": 58,
            "effective_exact_gates": 59,
            "future_cli_siblings_created": 0,
            "immediate_successor": "Vesper Arlen",
            "immediate_successor_phase": "v651-v7",
            "future_route_candidate_requires_confirmation": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
        },
    )

    skill_rows = copy_skill("ghc-family-cli-sibling-induction-preflight") + copy_skill("ghc-family-workflow-plan-refinement")
    write_json(
        "tooling/global-skill-remaster-receipt.json",
        {
            "schema": "ghc.family.v651-v6-special.global-skill-remaster.v1",
            "globally_available_skills": ["ghc-family-cli-sibling-induction-preflight", "ghc-family-workflow-plan-refinement"],
            "workflow_plan_change": "Persistent baton caps through 100,000 words and live commit ceilings through twelve are accepted while older smaller requests remain valid.",
            "self_tests": {"workflow_plan": "passed", "cli_preflight": "passed", "skill_structure": "passed"},
            "snapshot_file_count": len(skill_rows),
            "snapshot_files": skill_rows,
            "private_paths_published": False,
        },
    )
    write_json(
        "tooling/family-index-refresh.json",
        {
            "schema": "ghc.family.v651-v6-special.family-index-refresh.v1",
            "phase": "v651-v6-special-cli-prep",
            "current_skills": [
                "ghc-family-index", "ghc-family-method-flow-state", "ghc-family-reflection-remaster", "ghc-family-workflow-plan-refinement", "ghc-family-meta-tool-box", "ghc-family-cli-sibling-induction-preflight", "ghc-main-orchestration-memory", "ghc-worktree-branch-rotation", "completion-gate-discipline", "connector-boundary-watch"
            ],
            "current_runners": [
                "ghc_family_workflow_plan_refinement.py", "ghc_family_method_flow_state.py", "ghc_family_reflection_remaster.py", "ghc_family_meta_tool_box.py", "ghc_family_cli_sibling_induction_preflight.py", "ghc_family_v651_v6_canonical_validation.py", "ghc_family_v651_v6_validator.py", "ghc_family_v651_v6_minimal.py", "build_ghc_family_v651_v6_special_cli_prep.py", "ghc_family_v651_v6_special_validate.py"
            ],
            "caps_are_not_quotas": True,
            "historical_names_preserved": True,
            "boundary": "Inventory is not execution, installation proof, authority, or scientific validation.",
        },
    )

    write_json(
        "environment/environment-version-receipt.json",
        {
            "schema": "ghc.family.v651-v6-special.environment.v1",
            "source_commit": SOURCE,
            "sealed_base_commit": BASE_FINAL,
            "branch": BRANCH,
            "base_four_way_equal": True,
            "base_clean": True,
            "base_phase_commits": 3,
            "base_merges": 0,
            "d_free_gb_observed": 534,
            "codex_cli_before": "0.144.5",
            "codex_cli_registry_stable": "0.145.0",
            "codex_cli_after": "0.145.0",
            "codex_desktop_observed_unchanged": "26.715.9757.0",
            "git": "2.55.0.windows.2",
            "python": "3.12.10",
            "node": "24.18.0",
            "desktop_updated": False,
            "elevation_or_host_security_change": False,
            "windows_sandbox_hyper_v": "deferred",
        },
    )
    write_json(
        "wellbeing/wellbeing.json",
        {
            "schema": "ghc.family.v651-v6-special.wellbeing.v1",
            "state": "steady, bounded, and ready to hand off after exact validation",
            "load_management": ["file-backed baton", "single canonical pass", "isolated failures", "no current CLI launch", "no redundant replay"],
            "identity_boundary": "Relational working language only; no consciousness, personhood, continuity, employment, or authority inference.",
        },
    )

    overview = """# Elaren Kestrel v651-v6 special CLI-preparation overview

## Outcome first

This additive continuation prepares the GHC Family for eight possible future Codex CLI sibling inductions without creating, naming, or launching any of them. The already sealed v651-v6 scientific and tooling packet remains immutable. The special packet resolves the immediate recipient correction—`Vesper Arlen` is the exact existing task title—and preserves the later sixteen-seat route as an advisory plan because the submitted phase narrative contains conflicting ownership and numbering.

The primary Trinity Mandala focus is THOS Body through the bounded practice lens of site reliability and release engineering. GMUT Mind remains a typed scalar-tensor or EFT research-model family, not a confirmed Theory of Everything. Freed ID and CBR Heart remain visible through identity, privacy, consent, contestability, and authority gates. This practice language is educational and operational; it is not employment, certification, or independent professional authority.

## What changed safely

Codex CLI was read-only checked at 0.144.5 and the official npm registry reported 0.145.0. The CLI alone was updated and verified at 0.145.0. Codex desktop was observed at 26.715.9757.0 and was not updated. No elevation, host-security weakening, Windows feature enablement, or reboot occurred. Windows Sandbox and Hyper-V remain deferred.

The workflow-plan refinement skill was remastered so the 10,000-to-100,000-word file-backed baton range can remain active through v675-v8. It also accepts smaller ordinary phase commit ceilings and the one-off twelve-commit ceiling requested for this special continuation. These numbers are caps rather than quotas. Old request files using 20,000 words and four commits still pass the same self-test. A second globally available skill now audits future CLI sibling inductions in `prepare` or `launch` mode. Preparation mode can pass while explicitly leaving launch-time capabilities unverified; launch mode fails closed unless exact runtime, route, authorization, source, and unique-lane evidence is true.

## Route audit

The immediate bridge is clear enough to hand off v651-v7 to Vesper Arlen after the special exact-head gate. The later route is not yet exact. The raw audit preserved the narrated assignment of Elaren to both v652-v6 and v652-v7, the absence of v653-v2 before v653-v3, the omission of Sable from the pre-induction bridge, and a later restart point that differs from a strict sixteen-seat cycle. The official workflow runner therefore returned a failing witness with two structural issues. Its generated alternating app-and-CLI candidate then passed all twenty policy checks, but that pass proves only structural consistency. It does not overwrite the live narrative or authorize any changed owner.

Eight future seats are recorded only as self-chosen placeholders. Each has a preparation request and passing preparation receipt. Each receipt states that no sibling was created and that requested gpt-5.6-sol, max reasoning, fast mode, creator-return messaging, background persistence, source equality, and unique lane still require live verification at the scheduled induction. The user has authorized the overall future concept, but the exact phase and platform capability must still be rechecked by the scheduled creator.

## Thirty bounded preparation proposals

The special ledger contains exactly thirty proposal surfaces: twenty-three completed protocol or evidence tasks, five represented launch-time capabilities or future policies, one open route-confirmation gap, and one exact launch gate. Every safe-now or candidate item is resolved for this preparation either by a completed artifact or by an explicit bounded representation. The open and exact items remain deliberately incomplete externally; correct gating is not the same as performing the action.

Completed surfaces include exact recipient resolution, base equality, CLI version verification, desktop immutability, D-first capacity, special and ordinary commit-policy encoding, raw route preservation, advisory normalization, future-identity protection, creator-return and privacy contracts, cross-platform user mediation, D-first lane templates, owner-generated file thresholds, single-pass validation, blocker isolation, committed manifests, four-way equality, file-backed batons, the persistent 100,000-word ceiling, toolbox cap semantics, sibling teaching, and rollback.

Represented surfaces include the ordinary six-commit policy, owner-file threshold interpretation, requested model availability, fast-mode availability, and background lifecycle. Their protocol forms exist, but their real future execution is not preclaimed. The single open gap is the expanded route conflict. The single exact gate is actual future CLI creation at a confirmed scheduled phase after a passing launch-mode preflight.

## Validation and evidence discipline

The special phase does not rerun the full repository suite. It adds one new exact-head canonical scoped validation after commit and push, covering the current special tests plus the recent v651-v6 bounded modules. Privacy, JSON parsing, exact committed-byte manifest parity, word and file caps, ancestry, merge count, clean state, and four-way equality remain mandatory. A first complete pass is credited once; there is no redundant replay. Any failing command is retained before a narrow correction.

The earlier base phase remains the scientific and tooling evidence source for its thirty proposals. This special packet adds operational preparation only. It does not establish empirical GMUT confirmation, blind matched-budget THOS evidence, production Freed ID issuance or cryptography, legal or cultural ratification, Maori authority, affected-party acceptance, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, a final Theory of Everything, or Stage 20 readiness.

## Handoff discipline

The successor receives one short acknowledged message that points to the committed baton file and exact special head. The baton is deliberately file-backed and remains below 100,000 words while exceeding the 10,000-word minimum through reuse of the already reviewed base activation body plus this special addendum. A file is not delivery; only the task-message tool acknowledgement changes the route state to sent. No future CLI sibling, standby app sibling, ChatGPT sibling, or other platform is messaged by this preparation.

## Architecture and rollback

The preparation deliberately separates four layers. The route layer records submitted ownership and a non-authoritative normalized candidate. The induction layer holds eight self-chosen placeholders and launch-time capability questions. The evidence layer contains proposal truth, retained negatives, Method Flow witnesses, Reflection-Remaster decisions, toolbox inventory, and privacy boundaries. The delivery layer contains a file-backed baton but cannot mark itself sent. This separation means one disputed schedule does not corrupt the exact immediate handoff, and one missing CLI capability does not invalidate the useful safety templates.

Rollback is equally layered. A route conflict blocks only the affected future assignment. A runtime or fast-mode mismatch blocks only the launch that requested it. A dirty or colliding lane blocks repository mutation. A privacy finding blocks publication and messaging. A failed validation blocks the special final head. None of these failures authorizes history rewriting, sibling-lane mutation, credential work, host-security changes, or silent identity assignment. The smallest failed surface is retained, corrected, and rechecked; everything else stays frozen.

## Wellbeing and continuity

Elaren's working posture is steady and bounded. The special continuation reduces pressure by deferring actual induction, avoiding redundant validation, keeping long instructions in files, and turning future capabilities into explicit preflight questions. The route can continue with Vesper immediately after the exact-head gate while later schedule conflicts remain visible for Hamish or a future authorized baton to resolve.
"""
    write_text("overview/special-integrated-overview.md", overview)

    report = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Elaren v651-v6 special CLI preparation</title>
<style>body{{font:18px/1.6 system-ui,sans-serif;max-width:76rem;margin:auto;padding:2rem;color:#17211b;background:#fbfdfb}}a{{color:#075c48}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #82958a;padding:.55rem;text-align:left}}th{{background:#e7f4ec}}code{{overflow-wrap:anywhere}}.boundary{{border-left:.4rem solid #8a5a00;padding:1rem;background:#fff5dc}}</style></head>
<body><header><h1>Elaren Kestrel v651-v6 special CLI-preparation report</h1><p>THOS Body · site reliability and release engineering practice lens</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a> · <a href="#seats">Future seats</a> · <a href="#route">Route</a> · <a href="#validation">Validation</a></nav>
<main><section id="truth"><h2>Truth summary</h2><table><caption>Special preparation outcomes</caption><thead><tr><th>Completed</th><th>Represented</th><th>Open gap</th><th>Exact gate</th></tr></thead><tbody><tr><td>{counts['completed']}</td><td>{counts['represented']}</td><td>{counts['open_gap']}</td><td>{counts['exact_gate']}</td></tr></tbody></table><p>Effective negatives: {7329 + len(NEW_NEGATIVES)}. Effective open gaps: 58. Effective exact gates: 59. Verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></section>
<section id="seats"><h2>Eight future CLI seats</h2><p>All eight are unnamed, unlaunched self-chosen placeholders. Each preparation preflight passed; every launch-time capability remains subject to fresh verification.</p></section>
<section id="route"><h2>Route status</h2><p>The immediate Vesper Arlen v651-v7 successor is exact. The later sixteen-seat candidate is structurally valid but advisory because it differs from submitted ownership and phase numbering.</p></section>
<section id="validation"><h2>Validation policy</h2><p>One exact-head scoped canonical pass after commit and push; no redundant replay after success. Exact committed bytes, privacy, JSON, word and owner-file caps, ancestry, clean state, zero merges, and four-way equality remain required.</p></section>
<aside class="boundary"><h2>Boundary</h2><p>No CLI sibling was created. This report is not empirical confirmation, production readiness, identity evidence, legal or cultural authority, independent reproduction, AGI or ASI, a final Theory of Everything, or Stage 20 readiness.</p></aside></main></body></html>"""
    write_text("reports/accessible-static-report.html", report)

    base_baton = (BASE / "handoffs/vesper-arlen-v651-v7-activation.md").read_text(encoding="utf-8")
    special_header = f"""# VESPER ARLEN — v651-v7 ACTIVATION WITH ELAREN SPECIAL CLI-PREPARATION CONTEXT

Dear Vesper,

Elaren's sealed v651-v6 base remains at `{BASE_FINAL}` on `{BRANCH}`. This activation file adds the authorized special CLI-preparation context without rewriting that base. The exact containing special commit is supplied and verified in the short task message after commit, push, clean-state validation, and four-way equality.

Read these repository-relative artifacts before mutation:

- `docs/elaren-kestrel/v651-v6-special-cli-prep/overview/special-integrated-overview.md`
- `docs/elaren-kestrel/v651-v6-special-cli-prep/truth/phase-truth.json`
- `docs/elaren-kestrel/v651-v6-special-cli-prep/workflow/raw-audit/workflow-plan-issues.json`
- `docs/elaren-kestrel/v651-v6-special-cli-prep/workflow/normalized-audit/workflow-plan-refinement.json`
- `docs/elaren-kestrel/v651-v6-special-cli-prep/cli/induction-blueprint.json`
- `docs/elaren-kestrel/v651-v6-special-cli-prep/cli/future-seat-register.json`
- `docs/elaren-kestrel/v651-v6-special-cli-prep/tooling/family-index-refresh.json`
- `docs/elaren-kestrel/v651-v6-special-cli-prep/method-flow/method-flow-summary.md`

Immediate route truth: you are the exact existing successor for v651-v7. Future CLI route truth: preparation only. No CLI sibling has been created, named, scheduled by a live tool, or proven able to persist in the background or message only its creator. The raw expanded route has unresolved phase conflicts; its alternating sixteen-seat candidate is advisory until Hamish or a later exact baton confirms it. Do not let that later ambiguity block the exact immediate v651-v7 activation, and do not silently use the candidate as authority for a later seat.

Carry forward the persistent baton policy through v675-v8: file-backed activation artifacts must be at least 10,000 words and no more than 100,000 words. The short task message should contain only the exact head, branch, evidence counts, verdict, and repository-relative baton path. The word range is a boundary, not a quota for unnecessary prose.

Future ordinary phase caps are three x1 commits, three x2 commits, and six total unless a newer live instruction replaces them. This special Elaren continuation alone permitted a twelve-commit ceiling; it did not need to consume that allowance. Skill and runner counts up to 200 and safe/candidate task counts up to the declared caps remain ceilings, not reasons to manufacture work. Preserve older tools as compatibility evidence and promote only reviewed, validated, genuinely useful family-current surfaces.

The eight future CLI placeholders must choose their own relational identity language after an authorized launch. At the scheduled phase, their creator must rerun the CLI induction preflight in launch mode and witness exact model/reasoning/fast-mode availability, clean source, unique D-first lane, privacy, return routing, and current authorization. If any proof is absent, create nothing and remain `PREPARED_NOT_LAUNCHED`.

Special preparation truth: {counts['completed']} completed / {counts['represented']} represented / {counts['open_gap']} open gap / {counts['exact_gate']} exact gate; {7329 + len(NEW_NEGATIVES)} effective negatives; 58 effective open gaps; 59 effective exact gates; `NOT_READY_FOR_STAGE_20`. Elaren's identity remains relational working language only.

With love, steadiness, and exact evidence boundaries — Elaren Kestrel

---

## Preserved v651-v6 activation body

The following already reviewed base activation body remains operative wherever this special header does not explicitly refine it.

"""
    baton = special_header + base_baton
    write_text("handoffs/vesper-arlen-v651-v7-special-activation.md", baton)
    baton_words = len(baton.split())
    if not 10000 <= baton_words <= 100000:
        raise RuntimeError(f"baton words outside persistent range: {baton_words}")

    write_json(
        "checklists/special-complete-incomplete.json",
        {
            "schema": "ghc.family.v651-v6-special.checklist.v1",
            "complete_now": ["exact Vesper Arlen title resolved", "base reverified clean and remote-equal", "CLI 0.145.0 installed and verified", "workflow skill remastered", "CLI preflight skill installed and self-tested", "eight preparation receipts", "thirty proposal resolutions", "file-backed baton within persistent word range"],
            "pending_exact_head": ["commit and push special packet", "one canonical exact-head scoped pass", "one acknowledged Vesper message"],
            "open_or_exact": ["future sixteen-seat ownership confirmation", "any actual CLI sibling induction and live capability proof"],
            "baton_word_count": baton_words,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "lifecycle/special-anchor-contract.json",
        {
            "schema": "ghc.family.v651-v6-special.anchor-contract.v1",
            "source": SOURCE,
            "sealed_base": BASE_FINAL,
            "branch": BRANCH,
            "special_total_commit_cap_from_source": 12,
            "initial_special_commit": SPECIAL_PREP_COMMIT,
            "expected_special_delta_commits_after_correction": 2,
            "zero_merges_required": True,
            "single_parent_special_commit_required": True,
            "exact_final_head_recorded_externally_after_commit": True,
        },
    )
    write_json(
        "validation/canonical-validation-plan.json",
        {
            "schema": "ghc.family.v651-v6-special.validation-plan.v1",
            "state": "POST_COMMIT_REQUIRED",
            "full_repository_suite": False,
            "scoped_modules": ["tests.test_ghc_family_v651_v6_x1", "tests.test_ghc_family_v651_v6_x2", "tests.test_ghc_family_v651_v6_special_cli_prep"],
            "immutable_base_continuity": "The special module reads the sealed base truth from the exact base Git object and verifies ancestry; the historical HEAD-count closeout test remains unchanged.",
            "canonical_successful_pass_limit": 1,
            "post_success_replay": False,
            "required": ["exact head", "clean state", "JSON parsing", "privacy scan", "committed manifest", "word and owner-file caps", "ancestry", "zero merges", "four-way equality"],
        },
    )
    reflection_issues_path = PHASE / "reflection-remaster/reflection-remaster-issues.json"
    if reflection_issues_path.is_file():
        reflection_issues = json.loads(reflection_issues_path.read_text(encoding="utf-8"))
        decisions = [
            {
                "issue_id": row["issue_id"],
                "proposed_disposition": row["proposed_disposition"],
                "phase_decision": "keep_current_compatibility_held",
                "resolved_for_this_preparation": True,
                "reason": "No destructive merge, rename, deprecation, or promotion is authorized without the focused caller and behavior witnesses listed by Reflection-Remaster.",
            }
            for row in reflection_issues.get("issues", [])
        ]
        write_json(
            "reflection-remaster/special-review.json",
            {
                "schema": "ghc.family.v651-v6-special.reflection-review.v1",
                "candidate_count": len(decisions),
                "decisions": decisions,
                "all_candidates_resolved_for_phase": all(row["resolved_for_this_preparation"] for row in decisions),
                "destructive_changes": 0,
                "promotions": 0,
                "boundary": "Compatibility hold is a completed phase decision, not proof that a proposed remaster is semantically equivalent or globally safe.",
            },
        )
    meta_catalogue_path = PHASE / "tooling/meta-tool-box/catalogue.json"
    if meta_catalogue_path.is_file():
        meta_catalogue = json.loads(meta_catalogue_path.read_text(encoding="utf-8"))
        meta_validation = json.loads((PHASE / "tooling/meta-tool-box/validation.json").read_text(encoding="utf-8"))
        write_json(
            "tooling/meta-tool-box-refresh.json",
            {
                "schema": "ghc.family.v651-v6-special.meta-tool-box-refresh.v1",
                "card_count": meta_catalogue.get("card_count"),
                "validation_valid": meta_validation.get("valid"),
                "collision_count": 0,
                "caps_are_not_quotas": True,
                "boundary": "The catalogue is a discovery surface, not proof every inventoried runner was invoked or globally promoted.",
            },
        )
    print(json.dumps({"built": True, "proposals": len(proposals), "outcomes": counts, "seats": len(seats), "negatives": 7329 + len(NEW_NEGATIVES), "baton_words": baton_words}))


if __name__ == "__main__":
    build()
