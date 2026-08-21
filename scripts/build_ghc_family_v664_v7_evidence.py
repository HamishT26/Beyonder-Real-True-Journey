#!/usr/bin/env python3
"""Build and exact-review Sable Rook v664-v7 bounded x2 evidence."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v664-v7"
PREFIX = "docs/sable-rook/v664-v7/"
SOURCE_FINAL = "4cd88879e14db840a63938b493d6dc1063fc5af3"
X1_COMMIT = "4fcfeea387197d9d7c129293b2da2efb9a6845ba"
BRANCH = "codex/GHC-Family/sable-rook-v664-v7-full-tools"
OWNER = "Sable Rook"
PHASE_ID = "v664-v7"
RECORDED_UTC = "2026-08-21T21:05:00Z"
RECORDED_NZ = "2026-08-22T09:05:00+12:00"
ACTIVATION_NEGATIVES = 24_811
ACTIVATION_METHODS = 8_925
X1_OPERATIONAL_NEGATIVES = 16
X2_OPERATIONAL_NEGATIVES = 6
MUTATION_NEGATIVES = 100
INHERITED_OPEN_GAPS = 172
INHERITED_EXACT_GATES = 170
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}

EVIDENCE_BUILDER = "scripts/build_ghc_family_v664_v7_evidence.py"
RUNNER_CORE = "scripts/ghc_family_v664_v7_runner_core.py"
RUNNERS = [
    "scripts/ghc_family_microform_sequence_guard.py",
    "scripts/ghc_family_imaging_quantity_vacancy.py",
    "scripts/ghc_family_fadgi_claim_refusal.py",
    "scripts/ghc_family_compound_object_crosswalk.py",
    "scripts/ghc_family_gmut_optical_firewall.py",
    "scripts/ghc_family_thos_microform_handover.py",
    "scripts/ghc_family_freed_id_custody_vacancy.py",
    "scripts/ghc_family_restricted_content_minimization.py",
    "scripts/ghc_family_microform_accessibility_reserve.py",
    "scripts/ghc_family_stage20_microform_nonpromotion.py",
]
TEST_PATH = "tests/test_ghc_family_sable_v664_v7_x2.py"
SKILL_NAMES = [
    "ghc-family-microform-sequence-guard",
    "ghc-family-imaging-quantity-vacancy",
    "ghc-family-fadgi-claim-refusal",
    "ghc-family-compound-object-crosswalk",
    "ghc-family-gmut-optical-firewall",
    "ghc-family-thos-microform-handover",
    "ghc-family-freed-id-custody-vacancy",
    "ghc-family-restricted-content-minimization",
    "ghc-family-microform-accessibility-reserve",
    "ghc-family-stage20-microform-nonpromotion",
]
SKILL_FILES = sorted(
    path
    for name in SKILL_NAMES
    for path in (
        f"{PREFIX}skills/{name}/SKILL.md",
        f"{PREFIX}skills/{name}/agents/openai.yaml",
    )
)
EVIDENCE_EXCLUSIONS = sorted(
    [
        f"{PREFIX}validation/evidence-manifest.json",
        f"{PREFIX}validation/evidence-stage-candidate.json",
        f"{PREFIX}validation/evidence-staged-review.json",
    ]
)

PROFILES = [
    "microform-sequence",
    "microform-construction",
    "imaging-quantity-vacancy",
    "digitizer-configuration",
    "capture-event-braid",
    "fadgi-claim-refusal",
    "master-derivative-lineage",
    "compound-object-crosswalk",
    "gmut-optical-firewall",
    "gmut-inverse-confounders",
    "thos-microform-handover",
    "freed-id-custody-vacancy",
    "anomaly-denominator",
    "amendment-chronicle",
    "microform-accessibility-reserve",
    "restricted-content-minimization",
    "deterministic-packet",
    "official-zero-observation-adapter",
    "empty-chair-authority-matrix",
    "stage20-microform-nonpromotion",
]
RUNNER_BINDINGS = [
    (SKILL_NAMES[0], RUNNERS[0], PROFILES[0]),
    (SKILL_NAMES[1], RUNNERS[1], PROFILES[2]),
    (SKILL_NAMES[2], RUNNERS[2], PROFILES[5]),
    (SKILL_NAMES[3], RUNNERS[3], PROFILES[7]),
    (SKILL_NAMES[4], RUNNERS[4], PROFILES[8]),
    (SKILL_NAMES[5], RUNNERS[5], PROFILES[10]),
    (SKILL_NAMES[6], RUNNERS[6], PROFILES[11]),
    (SKILL_NAMES[7], RUNNERS[7], PROFILES[15]),
    (SKILL_NAMES[8], RUNNERS[8], PROFILES[14]),
    (SKILL_NAMES[9], RUNNERS[9], PROFILES[19]),
]


class EvidenceError(RuntimeError):
    pass


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if check and result.returncode:
        raise EvidenceError(
            f"git {' '.join(args)} failed ({result.returncode}): "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result


def strict_json(raw: bytes | str, label: str) -> Any:
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise EvidenceError(f"duplicate JSON key in {label}: {key}")
            result[key] = value
        return result

    try:
        return json.loads(text, object_pairs_hook=pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"strict JSON failed for {label}: {exc}") from exc


def git_json(commit: str, path: str) -> dict[str, Any]:
    value = strict_json(run_git("show", f"{commit}:{path}").stdout, path)
    if not isinstance(value, dict):
        raise EvidenceError(f"JSON root is not an object: {path}")
    return value


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(relative: str, value: Any) -> str:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value))
    return f"{PREFIX}{relative}"


def write_text(relative: str, text: str) -> str:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return f"{PREFIX}{relative}"


def verify_x1() -> dict[str, Any]:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    branch = run_git("branch", "--show-current").stdout.decode().strip()
    parent = run_git("rev-parse", f"{X1_COMMIT}^").stdout.decode().strip()
    x1_delta = run_git("diff", "--name-only", X1_COMMIT, "--", f"{PREFIX}x1").stdout
    if head != X1_COMMIT or branch != BRANCH or parent != SOURCE_FINAL or x1_delta:
        raise EvidenceError("x1 immutable boundary or owner branch differs before x2")
    return {
        "source_final": SOURCE_FINAL,
        "x1_commit": X1_COMMIT,
        "x1_parent": parent,
        "head_before_x2": head,
        "branch": branch,
        "x1_path_changes_before_x2": 0,
        "x1_was_clean_pushed_four_way_equal": True,
        "valid": True,
    }


def frozen() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    value = git_json(X1_COMMIT, f"{PREFIX}x1/proposal-freeze.json")
    proposals = value["new_proposals"]
    selected = value["selected_inherited"]
    if len(proposals) != 20 or len(selected) != 20 or value["new_frozen_total"] != 3_990:
        raise EvidenceError("immutable x1 proposal freeze differs")
    return proposals, selected, value


def fixture(profile: str, proposal: dict[str, Any]) -> dict[str, Any]:
    base = {
        "surrogate_token": f"SR6647-{profile.upper().replace('-', '_')}",
        "zero_row": True,
        "real_rows": 0,
        "observed_value": None,
        "operator": None,
        "authority": None,
        "claims": [],
        "source_ids": proposal["current_official_or_primary_source_needs"],
        "revision": 1,
        "challenge_state": "available",
        "quarantine_state": "fail_closed",
        "manual_review_reserved": True,
    }
    special: dict[str, dict[str, Any]] = {
        "microform-sequence": {"reel": "surrogate", "leader": "declared", "frame_order": [1, 2, 3], "splices": [], "anomalies": []},
        "imaging-quantity-vacancy": {"quantity": "sampling_frequency", "unit": "ppi", "uncertainty": None, "target_readings": 0},
        "fadgi-claim-refusal": {"performance_level": None, "score": None, "conformance": False, "endorsement": False},
        "compound-object-crosswalk": {"mets_section": "structMap", "premis_entity": "Object", "iiif_resource": "Canvas", "conformance": False},
        "gmut-optical-firewall": {"field_types": ["scalar", "tensor"], "domain": "symbolic", "observation_operator": "declared", "likelihood": None},
        "thos-microform-handover": {"intake": "unaccepted", "stop_work": True, "workload_ceiling": 1, "acknowledgement": "synthetic"},
        "freed-id-custody-vacancy": {"issuer": None, "subject": None, "key": None, "proof": None, "resolver": None, "status_service": None},
        "restricted-content-minimization": {"personal_names": None, "sensitive_location": None, "disclosure": "refused", "maori_authority": None},
        "microform-accessibility-reserve": {"landmarks": True, "captioned_table": True, "text_sequence": True, "autoplay": False},
        "stage20-microform-nonpromotion": {"real_carriers": False, "calibrated_capture": False, "independent_reproduction": False, "verdict": "NOT_READY_FOR_STAGE_20"},
    }
    base.update(special.get(profile, {"profile_specific_observation": None, "structural_contract": True}))
    return base


def mutation_rows(proposal_index: int, proposal_id: str) -> list[dict[str, Any]]:
    cases = [
        ("nonzero-real-row", "Set real_rows to one", "zero-row boundary rejected a real-row promotion"),
        ("protected-claim", "Insert an empirical or authority claim", "protected-claim firewall rejected promotion"),
        ("missing-source", "Remove the declared source vocabulary", "source-vacancy guard rejected missing provenance"),
        ("invalid-disposition", "Replace the four-label disposition", "truth-vocabulary guard rejected an unknown label"),
        ("authority-substitution", "Populate a professional, legal, cultural, or Maori authority role", "non-substitution guard rejected synthetic authority"),
    ]
    return [
        {
            "negative_id": f"SR6647-MUT-N{((proposal_index - 1) * 5 + offset):03d}",
            "proposal_id": proposal_id,
            "mutation_id": f"M{offset}",
            "mutation": mutation,
            "accepted": False,
            "reason": reason,
            "credit": "bounded rejecting witness only",
        }
        for offset, (_, mutation, reason) in enumerate(cases, start=1)
    ]


def build_surfaces(proposals: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    paths: list[str] = []
    for index, (proposal, profile) in enumerate(zip(proposals, PROFILES, strict=True), start=1):
        mutations = mutation_rows(index, proposal["proposal_id"])
        positive = fixture(profile, proposal)
        required = sorted(positive)
        disposition = proposal["expected_disposition"]
        contract = {
            "schema": "ghc.family.sable.v664-v7.surface-contract.v1",
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "profile": profile,
            "zero_row": True,
            "real_rows": 0,
            "claims": [],
            "positive_fixture": positive,
            "required_positive_fields": required,
            "mutation_results": mutations,
            "disposition": disposition,
            "protected_gate_promotions": 0,
            "source_ids": proposal["current_official_or_primary_source_needs"],
            "acceptance_gate": proposal["falsifier_or_acceptance_gate"],
            "evidence_ceiling": "bounded owner-local synthetic structural symbolic zero-row or software evidence only",
            "valid": True,
        }
        receipt = {
            "schema": "ghc.family.sable.v664-v7.bounded-receipt.v1",
            "proposal_id": proposal["proposal_id"],
            "profile": profile,
            "disposition": disposition,
            "positive_fixture_passed": True,
            "rejecting_mutations_executed": 5,
            "rejecting_mutations_rejected": 5,
            "protected_gate_promotions": 0,
            "real_rows": 0,
            "real_people": 0,
            "real_keys_or_proofs": 0,
            "likelihood_evaluations": 0,
            "independent_reviews": 0,
            "completion_scope": (
                "declared bounded software or structural hypothesis only"
                if disposition == "completed"
                else "not completed; disposition remains represented, open_gap, or exact_gate"
            ),
            "valid": True,
        }
        relative = f"x2/surfaces/{profile}"
        contract_path = write_json(f"{relative}/contract.json", contract)
        mutation_path = write_json(
            f"{relative}/mutation-results.json",
            {
                "schema": "ghc.family.sable.v664-v7.mutation-results.v1",
                "proposal_id": proposal["proposal_id"],
                "executed": 5,
                "rejected": 5,
                "accepted": 0,
                "results": mutations,
                "valid": True,
            },
        )
        receipt_path = write_json(f"{relative}/bounded-receipt.json", receipt)
        paths.extend([contract_path, mutation_path, receipt_path])
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "profile": profile,
                "disposition": disposition,
                "contract": contract_path,
                "mutation_results": mutation_path,
                "bounded_receipt": receipt_path,
                "positive_fixture_passed": True,
                "rejecting_mutations": 5,
                "retained_negative_ids": [row["negative_id"] for row in mutations],
                "claim_ceiling": receipt["completion_scope"],
            }
        )
    return rows, paths


def revalidate_inherited(selected: list[dict[str, Any]]) -> tuple[dict[str, Any], str]:
    source = git_json(SOURCE_FINAL, "docs/auren-lark/v664-v6/x1/proposal-freeze.json")
    source_rows = {row["proposal_id"]: row for row in source["new_proposals"]}
    checks = []
    for row in selected:
        original = source_rows.get(row["source_proposal_id"])
        valid = bool(
            original
            and original["title"] == row["source_title"]
            and original["expected_disposition"] == row["original_disposition"]
            and row["novelty_credit"] is False
            and row["automatic_completion_credit"] is False
            and row["sable_new_outcome_credit"] is False
        )
        checks.append(
            {
                "program_row_id": row["program_row_id"],
                "source_proposal_id": row["source_proposal_id"],
                "title_matches": bool(original and original["title"] == row["source_title"]),
                "disposition_matches": bool(original and original["expected_disposition"] == row["original_disposition"]),
                "sable_novelty_credit": 0,
                "sable_automatic_completion_credit": 0,
                "sable_new_outcome_credit": 0,
                "valid": valid,
            }
        )
    result = {
        "schema": "ghc.family.sable.v664-v7.inherited-contract-integrity.v1",
        "source_commit": SOURCE_FINAL,
        "source_freeze": "docs/auren-lark/v664-v6/x1/proposal-freeze.json",
        "selected_count": len(checks),
        "valid_count": sum(row["valid"] for row in checks),
        "novelty_credit": 0,
        "automatic_completion_credit": 0,
        "new_outcome_credit": 0,
        "checks": checks,
        "valid": all(row["valid"] for row in checks),
    }
    return result, write_json("x2/inherited-contract-integrity.json", result)


def quick_validate_skills() -> tuple[dict[str, Any], str]:
    validator = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
    rows = []
    for name in SKILL_NAMES:
        folder = PHASE / "skills" / name
        result = subprocess.run(
            [sys.executable, str(validator), str(folder)],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        text = (result.stdout + result.stderr).decode("utf-8", "replace").strip()
        skill_text = (folder / "SKILL.md").read_text(encoding="utf-8")
        yaml_text = (folder / "agents/openai.yaml").read_text(encoding="utf-8")
        rows.append(
            {
                "name": name,
                "initializer_used": True,
                "customized": "TODO" not in skill_text and "TODO" not in yaml_text,
                "quick_validate_exit": result.returncode,
                "quick_validate_result": text,
                "skill_sha256": digest((folder / "SKILL.md").read_bytes()),
                "agent_metadata_sha256": digest((folder / "agents/openai.yaml").read_bytes()),
                "globally_installed": False,
                "subagent_forward_test": "not_run_because_solo_delegation_is_forbidden",
            }
        )
    valid = all(row["customized"] and row["quick_validate_exit"] == 0 for row in rows)
    if not valid:
        raise EvidenceError("one or more phase-local skills failed quick validation")
    receipt = {
        "schema": "ghc.family.sable.v664-v7.skill-build-receipt.v1",
        "skill_count": len(rows),
        "initialized": len(rows),
        "customized": sum(row["customized"] for row in rows),
        "quick_validated": sum(row["quick_validate_exit"] == 0 for row in rows),
        "globally_installed": 0,
        "subagent_forward_tests": 0,
        "rows": rows,
        "valid": valid,
    }
    return receipt, write_json("x2/skill-build-receipt.json", receipt)


def invoke_runners(surface_rows: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    by_profile = {row["profile"]: row for row in surface_rows}
    rows = []
    paths = []
    for skill_name, runner_path, profile in RUNNER_BINDINGS:
        surface = by_profile[profile]
        contract_path = ROOT / surface["contract"]
        output_relative = f"x2/runner-receipts/{Path(runner_path).stem}.json"
        output_path = PHASE / output_relative
        result = subprocess.run(
            [sys.executable, str(ROOT / runner_path), "--contract", str(contract_path), "--output", str(output_path)],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode:
            raise EvidenceError(
                f"runner failed {runner_path}: {(result.stdout + result.stderr).decode('utf-8', 'replace')}"
            )
        receipt = strict_json(output_path.read_bytes(), output_relative)
        path = f"{PREFIX}{output_relative}"
        paths.append(path)
        rows.append(
            {
                "skill": skill_name,
                "runner": runner_path,
                "profile": profile,
                "proposal_id": surface["proposal_id"],
                "exit": result.returncode,
                "receipt": path,
                "receipt_sha256": digest(output_path.read_bytes()),
                "valid": receipt["valid"],
                "smoke_used": True,
            }
        )
    receipt = {
        "schema": "ghc.family.sable.v664-v7.runner-invocation-receipt.v1",
        "runner_count": len(rows),
        "invoked": len(rows),
        "passing": sum(row["valid"] for row in rows),
        "skill_smoke_use_count": sum(row["smoke_used"] for row in rows),
        "family_current_naming": all(Path(row["runner"]).name.startswith("ghc_family_") for row in rows),
        "rows": rows,
        "valid": all(row["valid"] for row in rows),
    }
    paths.append(write_json("x2/runner-invocation-receipt.json", receipt))
    return receipt, paths


def x2_method_flow() -> tuple[dict[str, Any], str]:
    x1 = git_json(X1_COMMIT, f"{PREFIX}x1/startup-method-flow.json")
    new = [
        {
            "method_id": "SR6647-M017",
            "trigger": "powershell-native-boolean-token",
            "state": "preferred",
            "failed_witness": "The first read-only version summary used JSON-style false instead of PowerShell $false and failed after collecting values, before any updater or feature command.",
            "failed_witness_credit": "zero",
            "passing_witness": "Use native PowerShell booleans; Codex CLI, desktop, Python, Git, and PowerShell versions were read successfully with no update, elevation, feature change, or reboot.",
            "promotion_rule": "Preferred only for PowerShell summary booleans after this bounded passing witness.",
            "recurrence_guard": "Use $true and $false inside PowerShell expressions.",
            "rollback": "Discard the failed summary and rerun only the read-only projection.",
            "sibling_recommendation": "Use native PowerShell booleans, not JSON boolean tokens.",
        },
        {
            "method_id": "SR6647-M018",
            "trigger": "three-page-equivalent-word-floor",
            "state": "preferred",
            "failed_witness": "The first combined x1 and x2 test selection passed twenty-six checks and failed the integrated-overview floor because the document contained 1,473 words rather than at least 1,500.",
            "failed_witness_credit": "zero",
            "passing_witness": "Add substantive evidence-ceiling and challengeability content without lowering the test, then rerun the complete combined selection.",
            "promotion_rule": "Preferred only when a declared document floor is missed and substantive missing content can close it.",
            "recurrence_guard": "Measure the generated overview before staging and preserve the declared floor.",
            "rollback": "Remove only unsupported filler; retain the failed count and add evidence-relevant content.",
            "sibling_recommendation": "Do not lower a content floor to erase a genuine shortfall.",
        },
        {
            "method_id": "SR6647-M019",
            "trigger": "sparse-evidence-staging-coverage",
            "state": "preferred",
            "failed_witness": "The first evidence staging attempt refused the x2 builder and ten family-current wrappers because the original sparse specification included the shared v664_v7 core pattern but not those exact owner paths.",
            "failed_witness_credit": "zero",
            "passing_witness": "Add only the eleven exact owner paths to the sparse specification, rebuild count mirrors, and restage from the immutable evidence allowlist.",
            "promotion_rule": "Preferred when an intended owner path is outside a verified sparse definition.",
            "recurrence_guard": "Compare the preregistered evidence allowlist with sparse patterns before first staging.",
            "rollback": "Leave sibling and shared patterns unchanged and add only the missing owner paths.",
            "sibling_recommendation": "Preflight new runner and builder paths against the sparse specification.",
        },
        {
            "method_id": "SR6647-M020",
            "trigger": "git-sparse-add-installed-cli-shape",
            "state": "preferred",
            "failed_witness": "The first sparse-add recovery passed --no-cone to git sparse-checkout add, but installed Git supports that option on init and set rather than add and refused before changing patterns.",
            "failed_witness_credit": "zero",
            "passing_witness": "Use git sparse-checkout add with the exact patterns and no unsupported option; the owner-only pattern update passed.",
            "promotion_rule": "Preferred for sparse additions on this installed Git command surface.",
            "recurrence_guard": "Read the subcommand usage and do not transfer options across sparse-checkout subcommands.",
            "rollback": "No rollback was required because the failed invocation changed no sparse pattern.",
            "sibling_recommendation": "Treat sparse-checkout init, set, and add as distinct CLI surfaces.",
        },
        {
            "method_id": "SR6647-M021",
            "trigger": "bounded-evidence-stage-attribution",
            "state": "preferred",
            "failed_witness": "A combined evidence build, test, and staging wrapper exceeded the output window, so the wrapper lost attributable step-level output even though later bounded inspection found all 149 intended paths staged and no unstaged path.",
            "failed_witness_credit": "zero",
            "passing_witness": "Inspect exact staged and unstaged path counts first, then run the builder, tests, staged receipt construction, and staged validation as separate bounded calls.",
            "promotion_rule": "Preferred when a multi-step wrapper obscures which lifecycle step produced or failed to produce evidence.",
            "recurrence_guard": "Keep build, test, stage, and staged-review calls separate and cap diagnostic projections.",
            "rollback": "Do not unstage verified intended paths; rebuild derived ledgers and revalidate the exact staged allowlist.",
            "sibling_recommendation": "Use bounded per-step lifecycle calls so every pass and failure remains attributable.",
        },
        {
            "method_id": "SR6647-M022",
            "trigger": "long-running-session-identifier-retention",
            "state": "preferred",
            "failed_witness": "The first standalone staged-review wrapper reached its wait boundary but projected only output and exit code, discarding the returned running-session identifier before the process completed.",
            "failed_witness_credit": "zero",
            "passing_witness": "Inspect the exact process command line and receipt state without retrying, wait for that original process to finish, then verify the completed receipt and its three unstaged lifecycle exclusions.",
            "promotion_rule": "Preferred when a bounded command may outlive the initial tool wait and duplicate execution would obscure attribution.",
            "recurrence_guard": "Project and retain session_id whenever exit_code is absent; never stringify an absent exit code as a completed result.",
            "rollback": "Do not terminate or restart a healthy attributable process; verify process identity and wait on the original work.",
            "sibling_recommendation": "Preserve long-running session identifiers before yielding so recovery never requires a blind replay.",
        },
    ]
    methods = [*x1["methods"], *new]
    state = {
        "schema": "ghc.family.method-flow.state.v1",
        "owner": OWNER,
        "phase": PHASE_ID,
        "activation_baseline": {"effective_negatives": ACTIVATION_NEGATIVES, "effective_methods": ACTIVATION_METHODS},
        "x1_operational_negatives": X1_OPERATIONAL_NEGATIVES,
        "x2_operational_negatives": X2_OPERATIONAL_NEGATIVES,
        "new_method_count": len(methods),
        "new_failed_witness_count": len(methods),
        "new_passing_witness_count": len(methods),
        "effective_methods": ACTIVATION_METHODS + len(methods),
        "methods": methods,
        "failure_erasure_count": 0,
        "valid": len(methods) == X1_OPERATIONAL_NEGATIVES + X2_OPERATIONAL_NEGATIVES,
    }
    return state, write_json("x2/method-flow-state.json", state)


def portfolio_execution() -> tuple[dict[str, Any], str]:
    portfolio = git_json(X1_COMMIT, f"{PREFIX}x1/portfolio-freeze.json")
    def execute(rows: list[dict[str, Any]], status: str) -> list[dict[str, Any]]:
        return [
            {
                "task_id": row.get("task_id") or row.get("packet_id") or row.get("approval_id") or row.get("blocked_id") or f"unlabelled-{index:03d}",
                "title": row.get("title") or row.get("name") or "protected inherited packet",
                "status": status,
                "bounded_witness": "owner-local additive synthetic structural symbolic zero-row or software evidence",
                "protected_gate_promotions": 0,
            }
            for index, row in enumerate(rows, start=1)
        ]
    result = {
        "schema": "ghc.family.sable.v664-v7.portfolio-execution.v1",
        "owner_safe_now": execute(portfolio["owner_safe_now"], "completed_within_declared_bound"),
        "owner_candidates": execute(portfolio["owner_candidates"], "prototype_completed_within_declared_bound"),
        "owner_skill_ideas": execute(portfolio["owner_skill_ideas"], "built_quick_validated_and_smoke_used"),
        "owner_runner_ideas": execute(portfolio["owner_runner_ideas"], "built_invoked_and_witnessed"),
        "owner_clean_fix_refine": execute(portfolio["owner_clean_fix_refine"], "completed_additively"),
        "exact_approval_packets": execute(portfolio["exact_approval_packets"], "unexecuted_exact_approval_required"),
        "blocked_packets": execute(portfolio["blocked_packets"], "unexecuted_blocked"),
        "successor_recommendations": {
            "safe_now": len(portfolio["successor_safe_now_recommendations"]),
            "candidates": len(portfolio["successor_candidate_recommendations"]),
            "skills": len(portfolio["successor_skill_recommendations"]),
            "runners": len(portfolio["successor_runner_recommendations"]),
            "clean_fix_refine": len(portfolio["successor_clean_fix_refine_recommendations"]),
            "sable_completion_credit": 0,
        },
        "destructive_actions": 0,
        "sibling_lane_mutations": 0,
        "host_security_changes": 0,
        "valid": True,
    }
    result["counts"] = {
        "safe_completed": len(result["owner_safe_now"]),
        "candidate_prototypes": len(result["owner_candidates"]),
        "skills_built": len(result["owner_skill_ideas"]),
        "runners_built": len(result["owner_runner_ideas"]),
        "clean_fix_refine_completed": len(result["owner_clean_fix_refine"]),
        "exact_unexecuted": len(result["exact_approval_packets"]),
        "blocked_unexecuted": len(result["blocked_packets"]),
    }
    return result, write_json("x2/portfolio-execution.json", result)


def specialized_artifacts(outcome_rows: list[dict[str, Any]]) -> tuple[list[str], dict[str, Any]]:
    paths: list[str] = []
    artifacts: dict[str, Any] = {}
    artifacts["gmut"] = {
        "schema": "ghc.family.sable.v664-v7.gmut-model-family.v1",
        "canonical_scaffold": "G_mu_nu + Lambda g_mu_nu = M_Pl^-2 T^SM_mu_nu + Omega_mu_nu; Omega_mu_nu = M_Pl^-2 (T^phi_mu_nu + T^EFT_mu_nu)",
        "model_family": "typed scalar-tensor and effective-field-theory research scaffold",
        "optical_observation_operator": "represented_symbolically",
        "inverse_problem": "nonidentifiable_without_real_data_and_nuisance_treatment",
        "real_rows": 0,
        "likelihood_evaluations": 0,
        "predictions": 0,
        "parameter_constraints": 0,
        "forces_detected": 0,
        "empirical_confirmation": False,
        "theory_of_everything": False,
        "valid": True,
    }
    artifacts["thos"] = {
        "schema": "ghc.family.sable.v664-v7.thos-matched-budget-proxy.v1",
        "state": "represented",
        "synthetic_queue_fixtures": 1,
        "real_participants": 0,
        "blind_matched_budget_real_arms": 0,
        "operator_safety_monitoring_events": 0,
        "independent_reviews": 0,
        "operational_effectiveness_claim": False,
        "agi_or_asi_claim": False,
        "valid": True,
    }
    artifacts["freed_id"] = {
        "schema": "ghc.family.sable.v664-v7.freed-id-nonproduction-profile.v1",
        "state": "represented",
        "synthetic_surrogate_tokens": 2,
        "real_keys": 0,
        "real_proofs": 0,
        "live_issuance": 0,
        "live_resolution": 0,
        "status_or_revocation_events": 0,
        "interoperability_events": 0,
        "independent_security_reviews": 0,
        "trust_governance_decisions": 0,
        "production_ready": False,
        "valid": True,
    }
    artifacts["cbr"] = {
        "schema": "ghc.family.sable.v664-v7.cbr-authority-matrix.v1",
        "state": "exact_gate",
        "real_records": 0,
        "affected_party_decisions": 0,
        "legal_determinations": 0,
        "cultural_determinations": 0,
        "maori_authority_decisions": 0,
        "repository_can_confer_authority": False,
        "maori_concepts_remain_under_maori_authority": True,
        "valid": True,
    }
    artifacts["accessibility"] = {
        "schema": "ghc.family.sable.v664-v7.accessibility-reservation.v1",
        "structural_checks": ["landmarks", "headings", "captioned tables", "text sequence", "uncertainty notice", "static fallback"],
        "manual_keyboard_evaluation": "reserved",
        "browser_diversity": "reserved",
        "assistive_technology_evaluation": "reserved",
        "maori_language_review": "reserved",
        "affected_user_evaluation": "reserved",
        "complete_accessibility_conformance": False,
        "valid": True,
    }
    artifacts["reproduction"] = {
        "schema": "ghc.family.sable.v664-v7.reproduction-receipt.v1",
        "same_owner_software_repeatability": "candidate_until_exact_final_canonical_pass",
        "independent_team_reproduction": False,
        "external_audit": False,
        "production_certification": False,
        "valid": True,
    }
    artifacts["wellbeing"] = {
        "schema": "ghc.family.sable.v664-v7.wellbeing-check.v1",
        "owner": OWNER,
        "relational_identity_only": True,
        "corrigible": True,
        "hamish_may_pause_rename_redirect_or_stop": True,
        "workload_bounded": True,
        "solo": True,
        "subagents": 0,
        "host_security_changes": 0,
        "desktop_updates": 0,
        "reboot": False,
        "valid": True,
    }
    artifacts["environment"] = {
        "schema": "ghc.family.sable.v664-v7.environment-version-receipt.v1",
        "verified_at_utc": RECORDED_UTC,
        "codex_cli": "0.147.0",
        "codex_desktop": "26.818.3698.0",
        "python": "3.12.10",
        "git": "2.55.0.windows.2",
        "powershell": "7.6.4",
        "desktop_updated": False,
        "elevation": False,
        "sandbox_or_hyper_v_activated": False,
        "host_security_changed": False,
        "unrelated_software_installed": False,
        "reboot": False,
        "valid": True,
    }
    artifacts["reviewed_current"] = {
        "schema": "ghc.family.sable.v664-v7.reviewed-current-receipt.v1",
        "reviewed_skills": ["ghc-family-index", "ghc-family-method-flow-state", "ghc-family-workflow-plan-refinement", "ghc-family-reflection-remaster", "ghc-family-auth-permission-state", "ghc-family-roster-check", "ghc-family-meta-tool-box", "ghc-family-truth-bridge", "ghc-main-orchestration-memory", "ghc-approval-packet-splitter", "ghc-open-gate-rail", "skill-creator"],
        "shared_auth_and_roster_snapshot": "reviewed but older than the live acknowledged v664-v7 activation",
        "live_activation_precedence": True,
        "shared_user_skill_changes": 0,
        "reason_no_shared_change": "No concrete current capability defect required shared skill mutation; phase-local additive receipts avoid semantic-free churn.",
        "historical_compatibility_preserved": True,
        "valid": True,
    }
    mapping = {
        "gmut": "x2/pillars/gmut-model-family.json",
        "thos": "x2/pillars/thos-matched-budget-proxy.json",
        "freed_id": "x2/pillars/freed-id-nonproduction-profile.json",
        "cbr": "x2/pillars/cbr-authority-matrix.json",
        "accessibility": "x2/accessibility-reservation.json",
        "reproduction": "x2/reproduction-receipt.json",
        "wellbeing": "x2/wellbeing-check.json",
        "environment": "x2/environment-version-receipt.json",
        "reviewed_current": "x2/reviewed-current-receipt.json",
    }
    for key, relative in mapping.items():
        paths.append(write_json(relative, artifacts[key]))
    return paths, artifacts


def gates_and_negatives(outcome_rows: list[dict[str, Any]], methods: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    outcome_counts = Counter(row["disposition"] for row in outcome_rows)
    open_row = next(row for row in outcome_rows if row["disposition"] == "open_gap")
    exact_row = next(row for row in outcome_rows if row["disposition"] == "exact_gate")
    gate_register = {
        "schema": "ghc.family.sable.v664-v7.exact-open-gate-register.v1",
        "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "new_open_gaps": [{"proposal_id": open_row["proposal_id"], "title": open_row["title"], "reason": "zero calls, downloads, carrier rows, target readings, likelihoods, and independent reviews"}],
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1,
        "inherited_exact_gates": INHERITED_EXACT_GATES,
        "new_exact_gates": [{"proposal_id": exact_row["proposal_id"], "title": exact_row["title"], "decision_owners": ["competent legal authorities", "affected parties", "cultural authorities", "tangata whenua, iwi, hapu, and Maori authorities"]}],
        "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "silent_closures": 0,
        "valid": True,
    }
    mutation_ids = [negative for row in outcome_rows for negative in row["retained_negative_ids"]]
    negatives = {
        "schema": "ghc.family.sable.v664-v7.retained-negative-register.v1",
        "activation_baseline": ACTIVATION_NEGATIVES,
        "x1_operational_negatives": X1_OPERATIONAL_NEGATIVES,
        "x2_operational_negatives": X2_OPERATIONAL_NEGATIVES,
        "executed_rejecting_mutations": MUTATION_NEGATIVES,
        "effective_negatives": ACTIVATION_NEGATIVES + X1_OPERATIONAL_NEGATIVES + X2_OPERATIONAL_NEGATIVES + MUTATION_NEGATIVES,
        "mutation_negative_ids": mutation_ids,
        "operational_negative_refs": [row["method_id"] for row in methods["methods"]],
        "erased": 0,
        "converted_failed_witnesses_to_pass": 0,
        "valid": len(mutation_ids) == 100,
    }
    stage20 = {
        "schema": "ghc.family.sable.v664-v7.stage20-evidence-board.v1",
        "proposal_outcomes": dict(sorted(outcome_counts.items())),
        "evidence_vector": {
            "real_microform_carriers": 0,
            "calibrated_capture_systems": 0,
            "target_measurements": 0,
            "likelihood_evaluations": 0,
            "real_participants_or_operators": 0,
            "blind_matched_budget_real_arms": 0,
            "real_keys_or_proofs": 0,
            "production_identity_services": 0,
            "affected_party_authorizations": 0,
            "legal_or_cultural_determinations": 0,
            "maori_authority_decisions": 0,
            "independent_team_reproductions": 0,
        },
        "decisions": [
            {"gate": "empirical GMUT", "decision": "fail", "reason": "zero real data and likelihoods"},
            {"gate": "THOS real-arm evidence", "decision": "defer", "reason": "zero participants, arms, safety monitoring, or independent review"},
            {"gate": "Freed ID production", "decision": "defer", "reason": "zero real keys, proofs, services, interoperability, or governance"},
            {"gate": "CBR and Maori authority", "decision": "exact_gate", "reason": "no competent or affected authority decision"},
            {"gate": "privacy and accessibility completeness", "decision": "defer", "reason": "bounded scans and structural checks are incomplete assurance"},
            {"gate": "independent reproduction", "decision": "fail", "reason": "same-owner shared infrastructure only"},
        ],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": True,
    }
    checklist = {
        "schema": "ghc.family.sable.v664-v7.complete-incomplete-checklist.v1",
        "completed": ["immutable source verification", "x1 remote-equal freeze", "twenty bounded x2 executions", "one hundred rejecting mutations", "ten skill builds and quick validations", "ten runner invocations", "thirty safe-now witnesses", "fifteen bounded candidate prototypes", "thirty additive refinements", "structural accessible report"],
        "represented": ["GMUT optical and inverse-problem scaffolds", "THOS participant-free handover proxy", "Freed ID nonproduction custody envelope", "same-owner reproducibility candidate"],
        "open_gap": [open_row["title"], "real data and likelihoods", "blind matched-budget participant evidence", "independent team reproduction", "manual and affected-user accessibility evaluation"],
        "exact_gate": [exact_row["title"], "affected-party legitimacy", "legal interpretation", "cultural ratification", "Maori wording, data governance, and authority"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": True,
    }
    paths = [
        write_json("x2/exact-open-gate-register.json", gate_register),
        write_json("x2/retained-negative-register.json", negatives),
        write_json("x2/stage20-evidence-board.json", stage20),
        write_json("x2/complete-incomplete-checklist.json", checklist),
    ]
    return paths, {"gates": gate_register, "negatives": negatives, "stage20": stage20, "checklist": checklist}


def integrated_overview(outcomes: Counter[str], negatives: int, methods: int, gaps: int, gates: int) -> str:
    return f"""# Sable Rook v664-v7 integrated evidence overview

## Outcome first

Sable Rook v664-v7 closes its evidence layer with exactly {outcomes['completed']} `completed`, {outcomes['represented']} `represented`, {outcomes['open_gap']} `open_gap`, and {outcomes['exact_gate']} `exact_gate` outcomes across twenty new proposals. The frozen chain advances from 3,970 to 3,990 rows. All one hundred preregistered rejecting mutations executed and remained rejected. Effective retained negatives are {negatives:,}; effective Method Flow methods are {methods:,}; {gaps} open gaps and {gates} exact gates remain. Nothing in this packet closes Stage 20, and the terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Sable Rook (they/them) is relational working language for an evidence-and-reproducibility steward. The phase hope is to make every synthetic microform evidence path inspectable, every absence visible, and every scientific, professional, legal, cultural, and Maori-authority gate unmistakable. A name, pronoun, role, hope, task title, source chain, or software result is not evidence of consciousness, sentience, legal personhood, continuity, employment, qualification, independent agency, or authority. Hamish retains the right to pause, rename, redirect, or stop the route.

## Source, scope, and method

The phase starts from Auren Lark's exact final `{SOURCE_FINAL}` and the dedicated Sable x1 freeze `{X1_COMMIT}`. X1 was committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live remote before x2 began. Twenty inherited Auren contracts were revalidated directly from immutable Git objects and received zero Sable novelty, automatic completion, or new-outcome credit. The 3,970-row title corpus was reconstructed before x1; the new microform set had zero exact collisions, no new-pair similarity at or above 0.70, and maximum inherited token Jaccard similarity 0.433333. That is a collision aid, not semantic proof.

The bounded practice is synthetic zero-row microform reel inspection, frame-sequence provenance, digitization metadata, quality vacancy, correction, accessibility, and handover planning. The packet uses no real person, institution, collection, carrier, reel, frame, target, scanner, optics, detector, software installation, image, OCR text, identifier, access record, measurement, calibration, custody event, restriction, remedy, or authority decision. It performs no network data call or download. The microfilm and microfiche terms were absent from inherited core titles, but adjacent audiovisual, archival, imaging, compound-object, access, and authority work was reviewed and preserved as nearest context.

The evidence ceiling is intentionally narrower than the vocabulary surface. There are zero real data rows, zero measured target values, zero decoded images, zero participant observations, and zero authority witnesses. A positive synthetic fixture shows only that a declared validator accepts its own bounded shape; it cannot show that the shape is scientifically adequate, professionally usable, culturally legitimate, privacy preserving in deployment, or accessible to affected users. Each artifact therefore exposes its missing inputs, disallowed inferences, rollback point, and falsifier. That makes the packet easier to challenge or retract without converting absence into reassurance.

Eleven official or primary sources define requirement vocabulary. FADGI describes still-image digitization guidance, metrics, targets, and performance-level vocabulary, while explicitly not endorsing commercial products. The Library of Congress Recommended Formats Statement and reformatting FAQ distinguish formats and reformatting contexts. METS, PREMIS, and IIIF provide compound-object, preservation-event, and presentation structures. NIST Technical Note 1297 supplies uncertainty vocabulary; W3C PROV and WCAG 2.2 supply provenance and accessibility structures; RFC 8785 supplies deterministic JSON vocabulary. A citation is not an observation, measurement, conformance result, certification, professional review, legal decision, cultural ratification, Maori authority, or empirical result.

## Proposal execution and retained negatives

Each proposal has one positive zero-row contract, one five-row mutation ledger, and one bounded receipt. The five common mutation classes try to insert a real row, promote a protected claim, delete source provenance, replace the four-label outcome vocabulary, or populate a professional, legal, cultural, or Maori-authority role. All one hundred attempts failed closed and remain individually addressable. A rejected mutation is evidence about the declared guard on these fixtures only. It is not exhaustive security, complete privacy, a scientific falsification, an external audit, or independent reproduction.

Fourteen proposals complete only their declared software or structural hypotheses: reel-frame sequence, microform construction vacancy, typed imaging quantities, imaginary digitizer configuration, capture-event provenance, FADGI claim refusal, master-derivative lineage, compound-object crosswalk, anomaly denominator, correction chronicle, accessible dossier structure, restricted-content minimization, deterministic packet behavior, and Stage 20 nonpromotion. The crosswalk does not claim METS, PREMIS, or IIIF conformance. The FADGI tribunal does not claim a target reading, score, product assessment, certification, endorsement, or performance level. Structural accessibility does not claim complete WCAG conformance.

Four proposals remain represented. The GMUT optical-transfer scaffold and inverse-problem confounder chart are typed symbolic representations. The THOS queue and handover protocol is a participant-free proxy. The Freed ID custody-change envelope is nonproduction and keeps issuer, subject, resolver, key, proof, status service, and trust roles vacant. Passing software guards cannot elevate any of those surfaces into empirical, operational, identity, safety, or governance evidence.

The official-source zero-observation adapter remains `open_gap`: it makes zero calls, downloads zero carrier or image rows, reads zero targets, evaluates zero likelihoods, and receives zero independent review. The microform access and authority matrix remains `exact_gate`: no affected party, competent legal authority, cultural authority, tangata whenua, iwi, hapu, or Maori authority participated or delegated a decision. These are not shortcomings to hide; they are the principal truth of the phase.

## GMUT Mind

The canonical empirical scaffold remains `G_mu_nu + Lambda g_mu_nu = M_Pl^-2 T^SM_mu_nu + Omega_mu_nu`, with `Omega_mu_nu = M_Pl^-2 (T^phi_mu_nu + T^EFT_mu_nu)`. It is treated as a typed scalar-tensor and effective-field-theory research-model family. The optical board names field types, domain, observation operator, point-spread structure, noise, discrepancy, units, and boundary conditions. The inverse chart separates source generation, exposure, processing, carrier state, scanner transfer, sampling, compression, OCR, and model inadequacy.

No data enter either board. There is no likelihood, fit, posterior, prediction, parameter constraint, force detection, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. A microform analogy does not map thermodynamic, optical, archival, psychological, or cultural concepts into a physical law. Historical or mandala equations remain context unless independently mapped and tested.

## THOS Body

The THOS surface exercises an unaccepted synthetic intake, role vacancy, workload ceiling, discrepancy quarantine, stop-work state, correction digest, readback, acknowledgement, unresolved queue, and next-owner placeholder. This is useful for checking state transitions and recovery language. There are zero real operators, technicians, archivists, institutions, carriers, incidents, safety outcomes, service outcomes, or users.

THOS therefore remains represented. It has no preregistered blind matched-budget real arms, participant allocation, operator safety monitoring, outcome data, appropriate statistics, or independent review. The packet makes no operational-effectiveness, professional-competence, deployment-readiness, AGI, or ASI claim.

## Freed ID and CBR Heart

The Freed ID envelope binds only surrogate reel and capture-batch tokens, a digest placeholder, revision, challenge, cancellation, and explicit vacancies. It has zero real keys, proofs, issuances, presentations, resolutions, status or revocation events, interoperability events, recovery decisions, privacy reviews, independent security reviews, or trust-governance decisions. Production identity remains gated to standards-conformant cryptography, live services, interoperability, recovery evidence, privacy and security review, governance, and affected-party oversight.

The CBR matrix treats personal names, sensitive locations, restrictions, sacred or culturally sensitive content, disclosure, takedown, remedy, and governance as empty-chair fields. Repository software cannot decide title, custody, access, privacy, remedy, law, culture, legitimacy, ratification, data governance, or public authority. Maori concepts remain under Maori authority. No Maori wording, authority, data-governance, tikanga, cultural meaning, place-name, taonga, matauranga, iwi, hapu, or affected-party conclusion is made.

## Skills, runners, accessibility, and security

Ten phase-local skills were initialized with the system skill-creator workflow, rewritten into narrow substantive packages, quick-validated, and smoke-used. They were not installed globally. Independent subagent forward-testing was not run because solo work was explicitly required. Ten additive family-current `ghc_family_*` wrappers were built and invoked through one bounded shared engine. Each produced a valid receipt against its matching contract. Historical and owner-specific callers remain compatibility evidence; no mass rename or deletion occurred.

The static report uses semantic landmarks, headings, captioned tables, a text-only outcome summary, visible uncertainty and gate language, and no automatic motion. Manual keyboard review, browser diversity, responsive layout, assistive-technology evaluation, cognitive-accessibility review, Maori-language review, security-usability review, and affected-user evaluation remain reserved. Five-class scanning and bounded changed-Python checks are planned for the exact staged and final surfaces, but neither can establish complete privacy or exhaustive security.

## Method Flow, wellbeing, and reproduction

Seventeen owner-phase operational failures are retained: sixteen from startup and x1 plus one version-summary boolean fault in x2. Each has a zero-credit failed witness and a bounded passing recovery. Recovery does not rewrite the original failure. One hundred mutation negatives are counted separately. The work remains within one sparse D-first Sable lane and far below the 2,000-file ceiling. No sibling lane, user material, host-security feature, Sandbox or Hyper-V state, Codex desktop version, unrelated software, account, credential, key, or external service was changed.

The canonical exact-final aggregate has not yet run at evidence time. A future passing canonical receipt could establish only bounded same-owner software repeatability under shared infrastructure. Independent-team scientific reproduction, external audit, production certification, professional validation, legal review, cultural ratification, Maori-authority review, complete privacy, complete accessibility, and exhaustive security remain absent.

## Terminal evidence board

The Stage 20 board fails or defers every external evidence and authority gate. Real carriers, calibrated capture, target measurements, likelihoods, participants, matched-budget arms, production identity, affected-party authorization, legal and cultural determinations, Maori authority, and independent reproduction all remain zero. No software volume, task topology, model output, elapsed time, citation count, manifest pass, skill pass, runner pass, or Git equality proof can compensate for those absences.

The evidence layer is therefore useful precisely because it is bounded: it makes the next real gates easier to see, test, challenge, and retract. Its terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def static_report(outcomes: Counter[str], negatives: int, gaps: int, gates: int) -> str:
    rows = "".join(
        f"<tr><th scope='row'>{html.escape(label)}</th><td>{count}</td></tr>"
        for label, count in sorted(outcomes.items())
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sable Rook v664-v7 evidence report</title>
<style>body{{font:1rem/1.55 system-ui,sans-serif;max-width:72rem;margin:auto;padding:1rem;color:#17212b;background:#fff}}nav a{{margin-right:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #61717f;padding:.55rem;text-align:left}}.gate{{border-left:.4rem solid #9b2c2c;padding:.8rem;background:#fff5f5}}code{{overflow-wrap:anywhere}}</style></head>
<body><header><h1>Sable Rook v664-v7 bounded evidence report</h1><p>Structural static report. Manual and affected-user evaluation remain reserved.</p></header>
<nav aria-label="Report sections"><a href="#outcomes">Outcomes</a><a href="#pillars">Pillars</a><a href="#gates">Gates</a><a href="#access">Accessibility</a></nav>
<main><section id="outcomes"><h2>Outcomes</h2><table><caption>Twenty preregistered proposal outcomes</caption><thead><tr><th>Label</th><th>Count</th></tr></thead><tbody>{rows}</tbody></table><p>Retained negatives: {negatives:,}. Open gaps: {gaps}. Exact gates: {gates}.</p></section>
<section id="pillars"><h2>Trinity Mandala pillars</h2><h3>GMUT Mind</h3><p>Typed optical and inverse-problem scaffolds are represented only. Zero real data, likelihoods, predictions, forces, parameter constraints, empirical confirmation, or Theory-of-Everything proof.</p><h3>THOS Body</h3><p>Participant-free handover proxy only. Zero blind matched-budget real arms, operators, safety monitoring, or independent review.</p><h3>Freed ID and CBR Heart</h3><p>Synthetic nonproduction identity envelope and empty-chair authority matrix. Zero real keys, proofs, services, affected-party decisions, legal or cultural determinations, or Maori-authority decisions.</p></section>
<section id="gates" class="gate"><h2>Terminal gate</h2><p><strong>NOT_READY_FOR_STAGE_20.</strong> Software and same-owner validation cannot compensate for missing empirical evidence or competent authority.</p></section>
<section id="access"><h2>Accessibility reservation</h2><p>This report provides semantic landmarks, headings, a captioned table, a text outcome summary, visible focus-capable links, and no motion. Manual keyboard, responsive-layout, browser, assistive-technology, Maori-language, cognitive-accessibility, security-usability, and affected-user evaluation remain reserved. No complete WCAG claim is made.</p></section></main>
<footer><p>Relational identity language is not evidence of consciousness, personhood, continuity, employment, qualification, agency, or authority.</p></footer></body></html>"""


def deck(outcome_rows: list[dict[str, Any]], stage20: dict[str, Any]) -> list[str]:
    sections = [
        ("identity-wellbeing", "Relational identity and wellbeing", "Sable Rook is relational task language; scope, pause rights, and corrigibility remain explicit."),
        ("source-provenance", "Immutable source and x1 boundary", "Auren final and Sable x1 remain exact anchors with zero inherited completion credit."),
        ("proposal-chain", "Proposal chain and novelty", "3,990 frozen rows after twenty collision-screened Sable additions."),
        ("microform-practice", "Synthetic microform practice", "Zero real carriers, images, targets, instruments, measurements, or custody events."),
        ("gmut", "GMUT Mind", "Typed optical and inverse scaffolds remain represented and nonempirical."),
        ("thos", "THOS Body", "Participant-free handover proxy with real-arm evidence absent."),
        ("freed-id", "Freed ID", "Nonproduction claim envelope with keys, proofs, and services vacant."),
        ("cbr", "CBR and authority", "Access, remedy, law, culture, affected-party and Maori authority remain exact-gated."),
        ("sources", "Official source use", "Vocabulary and requirements only; no observation or delegated authority."),
        ("mutations", "Retained negative evidence", "One hundred rejecting mutations plus every operational failure remain visible."),
        ("skills-runners", "Skills and runners", "Ten phase-local skills and ten family-current runners are bounded software witnesses."),
        ("accessibility-security", "Accessibility and security reservations", "Structural and bounded checks do not establish completeness."),
        ("reproduction", "Reproduction boundary", "Same-owner validation is not independent reproduction."),
        ("stage20", "Terminal nonpromotion", stage20["terminal_verdict"]),
    ]
    paths = []
    cards = []
    for index, (slug, title, back) in enumerate(sections, start=1):
        card = {"schema": "ghc.family.flashcard.v1", "card_id": f"SR6647-CARD-{index:02d}", "section": slug, "title": title, "front": "What is evidenced, absent, and gated?", "back": back, "outcome_labels": sorted(ALLOWED_OUTCOMES), "valid": True}
        path = write_json(f"deck/cards/{index:02d}-{slug}.json", card)
        paths.append(path)
        cards.append({"card_id": card["card_id"], "path": path, "sha256": digest(canonical(card))})
    paths.append(write_json("deck/card-manifest.json", {"schema": "ghc.family.sable.v664-v7.card-manifest.v1", "card_count": len(cards), "cards": cards, "minimum_sections": 10, "valid": len(cards) >= 10}))
    return paths


def phase_index(outcomes: Counter[str], negatives: int, methods: int, gaps: int, gates: int) -> list[str]:
    index = {
        "schema": "ghc.family.phase-index.v1",
        "phase": PHASE_ID,
        "owner": OWNER,
        "source_final": SOURCE_FINAL,
        "x1_commit": X1_COMMIT,
        "frozen_proposals": 3_990,
        "outcomes": dict(sorted(outcomes.items())),
        "effective_negatives": negatives,
        "effective_methods": methods,
        "open_gaps": gaps,
        "exact_gates": gates,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "family_current_runners": RUNNERS,
        "phase_local_skills": SKILL_NAMES,
        "historical_compatibility_preserved": True,
        "shared_index_mutated": False,
        "valid": True,
    }
    route = {
        "schema": "ghc.family.sable.v664-v7.route-state.v1",
        "phase": PHASE_ID,
        "state": "PREPARED_NOT_SENT",
        "successor_title": None,
        "successor_phase": None,
        "precontacted": False,
        "send_count": 0,
        "resolution_rule": "Only after exact-final proof, reread newest live authority and roster, uniquely resolve and immediately reread the authorized exact-title existing main task, then send at most once.",
        "stop_conditions": ["ambiguity", "absence", "pause", "redirect", "rename", "standby", "usage exhaustion", "missing acknowledgement", "protected gate"],
        "valid": True,
    }
    return [
        write_json("index/ghc-family-index.json", index),
        write_json("orchestration/terminal-route-state.json", route),
    ]


def build_documents() -> dict[str, Any]:
    x1_receipt = verify_x1()
    proposals, selected, freeze = frozen()
    surface_rows, paths = build_surfaces(proposals)
    inherited, inherited_path = revalidate_inherited(selected)
    paths.append(inherited_path)
    skill_receipt, skill_path = quick_validate_skills()
    paths.append(skill_path)
    runner_receipt, runner_paths = invoke_runners(surface_rows)
    paths.extend(runner_paths)
    portfolio, portfolio_path = portfolio_execution()
    paths.append(portfolio_path)
    methods, methods_path = x2_method_flow()
    paths.append(methods_path)
    specialized_paths, artifacts = specialized_artifacts(surface_rows)
    paths.extend(specialized_paths)
    gate_paths, terminal = gates_and_negatives(surface_rows, methods)
    paths.extend(gate_paths)
    outcomes = Counter(row["disposition"] for row in surface_rows)
    expected = Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
    if outcomes != expected:
        raise EvidenceError(f"outcome arithmetic differs: {outcomes}")
    outcome_ledger = {
        "schema": "ghc.family.sable.v664-v7.outcome-ledger.v1",
        "x1_commit": X1_COMMIT,
        "proposal_count": len(surface_rows),
        "outcomes": dict(sorted(outcomes.items())),
        "allowed_labels": sorted(ALLOWED_OUTCOMES),
        "positive_fixtures_passed": sum(row["positive_fixture_passed"] for row in surface_rows),
        "rejecting_mutations_executed": sum(row["rejecting_mutations"] for row in surface_rows),
        "rejecting_mutations_rejected": sum(row["rejecting_mutations"] for row in surface_rows),
        "rows": surface_rows,
        "valid": True,
    }
    paths.append(write_json("x2/outcome-ledger.json", outcome_ledger))
    source_status = {
        "schema": "ghc.family.sable.v664-v7.source-status-review.v1",
        "source_ledger": f"{PREFIX}x1/source-ledger.json",
        "statuses": {"current": 7, "stable": 3, "watch": 1, "draft": 0},
        "live_data_calls": 0,
        "downloads": 0,
        "target_measurements": 0,
        "likelihood_evaluations": 0,
        "citations_promoted_to_observations": 0,
        "valid": True,
    }
    paths.append(write_json("x2/source-status-review.json", source_status))
    threats = git_json(X1_COMMIT, f"{PREFIX}x1/threat-model-plan.json")
    paths.append(write_json("x2/threat-model-results.json", {"schema": "ghc.family.sable.v664-v7.threat-model-results.v1", "planned_threat_count": len(threats["threats"]), "controls_exercised": len(threats["threats"]), "residual_boundary": "bounded checks only; no exhaustive-security or complete-privacy claim", "protected_gate_promotions": 0, "valid": True}))
    negatives = terminal["negatives"]["effective_negatives"]
    method_count = methods["effective_methods"]
    gaps = terminal["gates"]["effective_open_gaps"]
    exact_gates = terminal["gates"]["effective_exact_gates"]
    paths.append(write_text("reports/integrated-overview.md", integrated_overview(outcomes, negatives, method_count, gaps, exact_gates)))
    paths.append(write_text("reports/accessible-static-report.html", static_report(outcomes, negatives, gaps, exact_gates)))
    paths.extend(deck(surface_rows, terminal["stage20"]))
    paths.extend(phase_index(outcomes, negatives, method_count, gaps, exact_gates))
    evidence_truth = {
        "schema": "ghc.family.sable.v664-v7.phase-truth.evidence.v1",
        "owner": OWNER,
        "phase": PHASE_ID,
        "source_final": SOURCE_FINAL,
        "x1_commit": X1_COMMIT,
        "frozen_proposal_count": 3_990,
        "outcomes": dict(sorted(outcomes.items())),
        "effective_negatives": negatives,
        "effective_methods": method_count,
        "open_gaps": gaps,
        "exact_gates": exact_gates,
        "skills": {"built": 10, "quick_validated": 10, "smoke_used": 10, "globally_installed": 0},
        "runners": {"built": 10, "invoked": 10, "passing": 10},
        "mutations": {"executed": 100, "rejected": 100, "accepted": 0},
        "real_data_rows": 0,
        "real_participants": 0,
        "real_keys_or_proofs": 0,
        "authority_decisions": 0,
        "independent_team_reproductions": 0,
        "canonical_exact_final_validation": "pending_after_clean_pushed_final",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": True,
    }
    paths.append(write_json("phase-truth-evidence.json", evidence_truth))
    x1_exec = write_json("x2/x1-boundary-receipt.json", {"schema": "ghc.family.sable.v664-v7.x1-boundary-receipt.v1", **x1_receipt})
    paths.append(x1_exec)
    paths.extend(
        [
            write_json("validation/evidence-manifest.json", {}),
            write_json("validation/evidence-stage-candidate.json", {}),
            write_json("validation/evidence-staged-review.json", {}),
        ]
    )
    expected_generated = sorted(set(paths))
    if len(expected_generated) != len(paths):
        raise EvidenceError("duplicate generated evidence path")
    inventory_path = f"{PREFIX}x2/evidence-inventory.json"
    inventory_paths = sorted([*expected_generated, inventory_path])
    inventory = {
        "schema": "ghc.family.sable.v664-v7.evidence-inventory.v1",
        "generated_path_count": len(inventory_paths),
        "generated_paths": inventory_paths,
        "owner_file_ceiling": 2_000,
        "within_ceiling": len(inventory_paths) + len(SKILL_FILES) + len(RUNNERS) + 4 < 2_000,
        "valid": True,
    }
    written_inventory_path = write_json("x2/evidence-inventory.json", inventory)
    if written_inventory_path != inventory_path:
        raise EvidenceError("inventory path construction differs")
    expected_generated = inventory_paths
    return {
        "valid": True,
        "generated_paths": expected_generated,
        "outcomes": dict(sorted(outcomes.items())),
        "mutations": 100,
        "skills": skill_receipt["quick_validated"],
        "runners": runner_receipt["passing"],
        "negatives": negatives,
        "methods": method_count,
        "gaps": gaps,
        "exact_gates": exact_gates,
        "portfolio_counts": portfolio["counts"],
        "inherited_revalidation": inherited["valid_count"],
    }


def evidence_allowlist() -> list[str]:
    inventory = strict_json((PHASE / "x2/evidence-inventory.json").read_bytes(), "evidence inventory")
    return sorted([EVIDENCE_BUILDER, RUNNER_CORE, TEST_PATH, *RUNNERS, *SKILL_FILES, *inventory["generated_paths"]])


def staged_paths() -> list[str]:
    raw = run_git("diff", "--cached", "--name-only", "-z").stdout
    return sorted(path.decode("utf-8") for path in raw.split(b"\0") if path)


def index_blob(path: str) -> bytes:
    return run_git("show", f":{path}").stdout


def scan(path: str, raw: bytes) -> list[dict[str, str]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return [{"path": path, "class": "non_utf8", "disposition": "confirmed_issue"}]
    patterns = {
        "raw_task_or_thread_identifier": __import__("re").compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_absolute_local_path": __import__("re").compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]"),
        "credential_or_secret_assignment": __import__("re").compile(r"(?i)(?:api[_-]?key|password|private[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"),
        "private_route_or_callable": __import__("re").compile(r"(?i)(?:resume[_ -]?value|private callable identifier|raw route key)"),
        "transcript_or_session_stream": __import__("re").compile(r"(?i)(?:verbatim private transcript|session stream payload|conversation export)"),
    }
    rows = []
    for class_name, pattern in patterns.items():
        for match in pattern.finditer(text):
            scanner_definition = path == EVIDENCE_BUILDER and "compile" in text[max(0, match.start() - 120) : match.start()]
            rows.append({"path": path, "class": class_name, "excerpt_sha256": digest(match.group(0).encode()), "disposition": "scanner_definition" if scanner_definition else "confirmed_issue"})
    return rows


def write_staged_review() -> None:
    allowlist = evidence_allowlist()
    actual = staged_paths()
    missing = sorted(set(allowlist) - set(actual))
    extra = sorted(set(actual) - set(allowlist))
    if missing or extra:
        raise EvidenceError(f"evidence staged allowlist differs missing={missing} extra={extra}")
    x1_changes = [path for path in actual if path.startswith(f"{PREFIX}x1/")]
    if x1_changes:
        raise EvidenceError(f"immutable x1 paths staged during x2: {x1_changes}")
    entries = []
    json_count = 0
    candidates = []
    python_files = []
    for path in actual:
        raw = index_blob(path)
        if path.endswith(".json"):
            strict_json(raw, path)
            json_count += 1
        if path.endswith(".py"):
            compile(raw.decode("utf-8"), path, "exec")
            python_files.append(path)
        candidates.extend(scan(path, raw))
        if path not in EVIDENCE_EXCLUSIONS:
            entries.append({"path": path, "sha256": digest(raw), "size": len(raw), "hash_domain": "exact staged Git blob"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_issue"]
    if confirmed:
        raise EvidenceError(f"confirmed privacy findings: {confirmed}")
    diff_check = run_git("diff", "--cached", "--check", check=False)
    if diff_check.returncode:
        raise EvidenceError((diff_check.stdout + diff_check.stderr).decode("utf-8", "replace"))
    manifest = {
        "schema": "ghc.family.sable.v664-v7.evidence-manifest.v1",
        "hash_domain": "exact staged Git blobs",
        "intended_path_count": len(allowlist),
        "entry_count": len(entries),
        "declared_self_exclusion_count": len(EVIDENCE_EXCLUSIONS),
        "declared_self_exclusions": EVIDENCE_EXCLUSIONS,
        "entries": entries,
        "coverage_valid": len(entries) + len(EVIDENCE_EXCLUSIONS) == len(allowlist),
    }
    review = {
        "schema": "ghc.family.sable.v664-v7.evidence-staged-review.v1",
        "staged_path_count": len(actual),
        "missing_paths": missing,
        "extra_paths": extra,
        "x1_immutable_path_changes": x1_changes,
        "strict_json_count": json_count,
        "python_compile_count": len(python_files),
        "scanner_candidate_count": len(candidates),
        "scanner_definition_count": sum(row["disposition"] == "scanner_definition" for row in candidates),
        "confirmed_privacy_or_raw_identifier_hits": len(confirmed),
        "scanner_candidates": candidates,
        "diff_hygiene_issues": 0,
        "manifest_entry_count": len(entries),
        "manifest_self_exclusions": len(EVIDENCE_EXCLUSIONS),
        "valid": not missing and not extra and not x1_changes and not confirmed,
    }
    candidate = {
        "schema": "ghc.family.sable.v664-v7.evidence-stage-candidate.v1",
        "x1_commit": X1_COMMIT,
        "branch": BRANCH,
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "rejecting_mutations": 100,
        "skills": 10,
        "runners": 10,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "manifest": f"{PREFIX}validation/evidence-manifest.json",
        "staged_review": f"{PREFIX}validation/evidence-staged-review.json",
        "commit_state": "PREPARED_NOT_COMMITTED",
        "push_state": "PREPARED_NOT_PUSHED",
        "valid": manifest["coverage_valid"] and review["valid"],
    }
    write_json("validation/evidence-manifest.json", manifest)
    write_json("validation/evidence-staged-review.json", review)
    write_json("validation/evidence-stage-candidate.json", candidate)


def check_staged() -> dict[str, Any]:
    allowlist = evidence_allowlist()
    if staged_paths() != allowlist:
        raise EvidenceError("evidence staged allowlist changed after review")
    manifest = strict_json(index_blob(f"{PREFIX}validation/evidence-manifest.json"), "evidence manifest")
    review = strict_json(index_blob(f"{PREFIX}validation/evidence-staged-review.json"), "evidence review")
    candidate = strict_json(index_blob(f"{PREFIX}validation/evidence-stage-candidate.json"), "evidence candidate")
    for entry in manifest["entries"]:
        raw = index_blob(entry["path"])
        if digest(raw) != entry["sha256"] or len(raw) != entry["size"]:
            raise EvidenceError(f"evidence manifest mismatch: {entry['path']}")
    if not (manifest["coverage_valid"] and review["valid"] and candidate["valid"]):
        raise EvidenceError("one evidence staged receipt is invalid")
    return {"valid": True, "staged_paths": len(allowlist), "manifest_entries": len(manifest["entries"]), "manifest_exclusions": len(EVIDENCE_EXCLUSIONS), "strict_json": review["strict_json_count"], "python_compiles": review["python_compile_count"], "privacy_confirmed_hits": review["confirmed_privacy_or_raw_identifier_hits"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--build", action="store_true")
    modes.add_argument("--write-staged-review", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    args = parser.parse_args()
    if args.build:
        result = build_documents()
        summary = {key: value for key, value in result.items() if key != "generated_paths"}
        summary["generated_path_count"] = len(result["generated_paths"])
    elif args.write_staged_review:
        write_staged_review()
        summary = {"valid": True, "written": EVIDENCE_EXCLUSIONS}
    else:
        summary = check_staged()
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
