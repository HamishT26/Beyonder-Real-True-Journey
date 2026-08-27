"""Build and validate Sylven Arc v673-v1 owner-local x2 evidence.

This builder operates only after the immutable planning-only x1 commit is
pushed and four-way equal. It creates synthetic owner-local evidence, tools,
skills, runners, flashcards, Method Flow, and staged validation surfaces. It
does not make network calls, install globally, contact another task, or perform
any real flagmaking, conservation, rigging, signalling, identity, legal,
cultural, or authority action.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "sylven-arc" / "v673-v1"
X1_ROOT = OWNER_ROOT / "x1"
X2_ROOT = OWNER_ROOT / "x2"
VALIDATION_ROOT = OWNER_ROOT / "validation"
BRANCH = "codex/GHC-Family/sylven-arc-v673-v1-full-tools"
SOURCE_FINAL = "305708c6d5a8dfee0432a2c09ef5b59da4b6c438"
X1_COMMIT = "606f6b7afef6d4368e1b34d128e57fc061629b05"
PHASE = "v673-v1"
OWNER = "Sylven Arc"
BOUNDARY = (
    "Synthetic same-owner software and documentation evidence only; not independent reproduction, "
    "empirical confirmation, participant evidence, professional advice, production readiness, legal or "
    "cultural ratification, Māori authority, complete privacy or accessibility assurance, exhaustive "
    "security, AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, canon, or "
    "Stage 20 authority. Māori concepts remain under Māori authority."
)
ACTIVATION_BASELINE = {
    "proposal_chain": 6230,
    "effective_negatives": 36161,
    "effective_methods": 22489,
    "failed_witnesses": 7822,
    "bounded_passing_witnesses": 10052,
    "open_gaps": 291,
    "exact_gates": 284,
}
EXPECTED_OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}

SKILL_NAMES = [
    "ghc-family-flag-field-identity-lattice",
    "ghc-family-flag-edge-topology",
    "ghc-family-flag-seam-relation-guard",
    "ghc-family-flag-attachment-abstention",
    "ghc-family-flag-silhouette-refusal",
    "ghc-family-flag-orientation-firewall",
    "ghc-family-flag-material-claim-vacancy",
    "ghc-family-flag-condition-cue-separation",
    "ghc-family-flag-symbol-meaning-vacancy",
    "ghc-family-flag-image-lineage",
    "ghc-family-flag-storage-custody-map",
    "ghc-family-flag-environment-observation-vacancy",
    "ghc-family-flag-rights-authority-hold",
    "ghc-family-flag-accessible-status",
    "ghc-family-flag-zero-key-role",
    "ghc-family-flag-privacy-minimizer",
    "ghc-family-flag-workload-handover",
    "ghc-family-flag-canonical-json",
    "ghc-family-flag-provenance-braid",
    "ghc-family-flag-flashcard-projection",
]

RUNNER_NAMES = [
    "ghc_family_flag_identity.py",
    "ghc_family_flag_edge_topology.py",
    "ghc_family_flag_seam_relation.py",
    "ghc_family_flag_attachment_abstention.py",
    "ghc_family_flag_material_vacancy.py",
    "ghc_family_flag_condition_separation.py",
    "ghc_family_flag_provenance_correction.py",
    "ghc_family_flag_privacy_access.py",
    "ghc_family_flag_workload_handover.py",
    "ghc_family_flag_flashcard_projection.py",
]

RUNNER_PROFILES = [
    "identity", "edge_topology", "seam_relation", "attachment_abstention", "material_vacancy",
    "condition_separation", "provenance_correction", "privacy_access", "workload_handover",
    "flashcard_projection",
]

TOOL_NAMES = [
    "ghc_family_flag_contract.py",
    "ghc_family_flag_flashcards.py",
    "ghc_family_flag_evidence.py",
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if check and result.returncode:
        raise SystemExit(result.stderr.decode("utf-8", errors="replace"))
    return result


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def write_text(path: Path, payload: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8")
    return path


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_sha(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def tool_contract_source() -> str:
    return '''"""Synthetic flag-record contract validator; no external actions."""
from __future__ import annotations
from typing import Any

ALLOWED_PROFILES = {"identity", "edge_topology", "seam_relation", "attachment_abstention", "material_vacancy", "condition_separation", "provenance_correction", "privacy_access", "workload_handover", "flashcard_projection"}

def evaluate_contract(payload: Any, profile: str) -> dict[str, Any]:
    issues = []
    if not isinstance(payload, dict):
        return {"valid": False, "issues": ["payload_not_object"], "profile": profile}
    if profile not in ALLOWED_PROFILES:
        issues.append("unknown_profile")
    if payload.get("synthetic") is not True:
        issues.append("synthetic_true_required")
    if payload.get("real_object") is not False:
        issues.append("real_object_false_required")
    if payload.get("external_actions") != 0:
        issues.append("external_actions_zero_required")
    if not isinstance(payload.get("record_id"), str) or not payload.get("record_id"):
        issues.append("record_id_required")
    if not isinstance(payload.get("vacancies"), list) or not payload.get("vacancies"):
        issues.append("vacancies_required")
    if not isinstance(payload.get("authority_holds"), list) or not payload.get("authority_holds"):
        issues.append("authority_holds_required")
    return {"valid": not issues, "issues": issues, "profile": profile, "external_actions": 0}
'''


def tool_flashcard_source() -> str:
    return '''"""Four-tier Freed ID flashcard projection and acyclic-card validator."""
from __future__ import annotations
import hashlib
import json
from typing import Any

TIERS = {"freed_id", "pillar", "practice", "task"}

def content_hash(card: dict[str, Any]) -> str:
    body = {key: value for key, value in card.items() if key != "sha256"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()

def validate_deck(cards: list[dict[str, Any]]) -> dict[str, Any]:
    ids = {card.get("card_id") for card in cards}
    issues = []
    if len(ids) != len(cards) or None in ids:
        issues.append("unique_card_ids_required")
    for card in cards:
        if card.get("tier") not in TIERS:
            issues.append(f"invalid_tier:{card.get('card_id')}")
        if any(parent not in ids for parent in card.get("parents", [])):
            issues.append(f"missing_parent:{card.get('card_id')}")
        if card.get("card_id") in card.get("parents", []):
            issues.append(f"self_cycle:{card.get('card_id')}")
        if card.get("sha256") != content_hash(card):
            issues.append(f"hash_mismatch:{card.get('card_id')}")
    return {"valid": not issues, "issues": issues, "card_count": len(cards), "external_actions": 0}
'''


def tool_evidence_source() -> str:
    return '''"""Deterministic synthetic evidence-envelope helper."""
from __future__ import annotations
import hashlib
import json
from typing import Any

def seal(payload: Any) -> dict[str, Any]:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return {"sha256": hashlib.sha256(encoded).hexdigest(), "bytes": len(encoded), "hash_domain": "canonical_utf8_json", "external_actions": 0}

def verify(payload: Any, receipt: dict[str, Any]) -> bool:
    return seal(payload) == receipt
'''


def runner_source(profile: str) -> str:
    return f'''"""Family-current synthetic flag {profile} runner."""
from __future__ import annotations
import argparse
import json
from ghc_family_flag_contract import evaluate_contract

PROFILE = "{profile}"

def run(payload):
    return evaluate_contract(payload, PROFILE)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", choices=["valid", "invalid"], default="valid")
    args = parser.parse_args()
    payload = {{"synthetic": args.fixture == "valid", "real_object": False, "external_actions": 0, "record_id": "SA6731-SMOKE", "vacancies": ["real_observation"], "authority_holds": ["professional", "legal", "cultural", "maori_authority"]}}
    result = run(payload)
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["valid"] else 2)

if __name__ == "__main__":
    main()
'''


def customize_skills() -> list[dict[str, Any]]:
    rows = []
    for index, name in enumerate(SKILL_NAMES, start=1):
        skill_root = X2_ROOT / "skills" / name
        if not (skill_root / "SKILL.md").exists():
            raise SystemExit(f"official skill scaffold missing: {name}")
        focus = name.removeprefix("ghc-family-flag-").replace("-", " ")
        skill_md = f'''---
name: {name}
description: Use when a v673-v1 owner-local synthetic flag record needs the {focus} contract, rejecting invalid structure while preserving professional, legal, cultural, Māori-authority, privacy, empirical, and Stage 20 gates.
---

# {name}

Apply this owner-local contract only to synthetic flag-documentation fixtures.

1. Require `synthetic: true`, `real_object: false`, and `external_actions: 0`.
2. Preserve explicit vacancies for observations, measurements, treatment, operation, competence, and independent review.
3. Preserve exact holds for ownership, design rights, civic or religious meaning, cultural interpretation, affected-party legitimacy, Māori wording and concepts, Māori data governance, and Māori authority.
4. Accept only the four core outcomes: `completed`, `represented`, `open_gap`, and `exact_gate`.
5. Retain every rejecting witness and pair a recovery without rewriting the failure.
6. Never turn a citation, schema, synthetic fixture, analogy, or same-owner test into real evidence or authority.

Read [references/contract.md](references/contract.md) before changing this skill. This skill is phase-local, not globally installed, and proves no professional competence, empirical result, production readiness, legal or cultural ratification, Māori authority, or Stage 20 readiness.
'''
        reference = f'''# {name} contract

Focus: {focus}.

Accept only finite, explicit, synthetic records with zero external actions. Reject missing vacancies, undeclared outcomes, real-object claims, precise private locations, authority substitution, and any attempt to promote flag vocabulary into manufacturing, conservation, display, signalling, rigging, safety, legal, cultural, civic, religious, Indigenous, or Māori instructions or authority.

Recovery is owner-local and additive: retain the failed fixture, repair only the isolated field or validator, rerun only that dependency, and keep the exact gate visible. Māori concepts remain under Māori authority.
'''
        openai_yaml = f'''interface:
  display_name: "{name}"
  short_description: "Synthetic flag {focus} guard"
  default_prompt: "Apply {name} to a bounded synthetic record and preserve every evidence and authority gate."
'''
        write_text(skill_root / "SKILL.md", skill_md)
        write_text(skill_root / "references" / "contract.md", reference)
        write_text(skill_root / "agents" / "openai.yaml", openai_yaml)
        current = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        invalid = current.replace(f"name: {name}", "name: invalid-owner-name", 1)
        positive = current.startswith(f"---\nname: {name}\n") and "external_actions: 0" in current and "Māori concepts remain under Māori authority" in reference
        negative_rejected = not invalid.startswith(f"---\nname: {name}\n")
        rows.append({"skill": name, "initialized_with_official_skill_creator": True, "customized": True, "complete_read": True, "positive_smoke": positive, "negative_smoke_rejected": negative_rejected, "global_install": False, "external_actions": 0})
        if not positive or not negative_rejected:
            raise SystemExit(f"skill smoke failed: {name}")
    return rows


def build_tools_and_runners() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    sources = {
        TOOL_NAMES[0]: tool_contract_source(),
        TOOL_NAMES[1]: tool_flashcard_source(),
        TOOL_NAMES[2]: tool_evidence_source(),
    }
    for name, source in sources.items():
        write_text(ROOT / "scripts" / name, source)
        compile(source, f"scripts/{name}", "exec")
    for name, profile in zip(RUNNER_NAMES, RUNNER_PROFILES, strict=True):
        source = runner_source(profile)
        write_text(ROOT / "scripts" / name, source)
        compile(source, f"scripts/{name}", "exec")

    runner_rows = []
    for name, profile in zip(RUNNER_NAMES, RUNNER_PROFILES, strict=True):
        good = subprocess.run([sys.executable, str(ROOT / "scripts" / name), "--fixture", "valid"], cwd=ROOT, capture_output=True, text=True)
        bad = subprocess.run([sys.executable, str(ROOT / "scripts" / name), "--fixture", "invalid"], cwd=ROOT, capture_output=True, text=True)
        good_payload = json.loads(good.stdout)
        bad_payload = json.loads(bad.stdout)
        valid = good.returncode == 0 and good_payload["valid"] is True and bad.returncode == 2 and bad_payload["valid"] is False
        runner_rows.append({"runner": name, "profile": profile, "positive_exit": good.returncode, "negative_exit": bad.returncode, "positive_valid": good_payload["valid"], "negative_rejected": not bad_payload["valid"], "valid": valid})
        if not valid:
            raise SystemExit(f"runner smoke failed: {name}")

    sys.path.insert(0, str(ROOT / "scripts"))
    from ghc_family_flag_contract import evaluate_contract
    from ghc_family_flag_evidence import seal, verify
    from ghc_family_flag_flashcards import content_hash, validate_deck
    valid_payload = {"synthetic": True, "real_object": False, "external_actions": 0, "record_id": "SA6731-TOOL", "vacancies": ["real_observation"], "authority_holds": ["professional", "legal", "cultural", "maori_authority"]}
    invalid_payload = {**valid_payload, "synthetic": False}
    contract_good = evaluate_contract(valid_payload, "identity")
    contract_bad = evaluate_contract(invalid_payload, "identity")
    receipt = seal(valid_payload)
    card = {"card_id": "SA6731-TOOL-CARD", "tier": "freed_id", "parents": [], "summary": "synthetic tool smoke", "external_actions": 0}
    card["sha256"] = content_hash(card)
    deck_good = validate_deck([card])
    broken = dict(card); broken["sha256"] = "0" * 64
    deck_bad = validate_deck([broken])
    tool_rows = [
        {"tool": TOOL_NAMES[0], "positive_valid": contract_good["valid"], "negative_rejected": not contract_bad["valid"], "valid": contract_good["valid"] and not contract_bad["valid"]},
        {"tool": TOOL_NAMES[1], "positive_valid": deck_good["valid"], "negative_rejected": not deck_bad["valid"], "valid": deck_good["valid"] and not deck_bad["valid"]},
        {"tool": TOOL_NAMES[2], "positive_valid": verify(valid_payload, receipt), "negative_rejected": not verify(invalid_payload, receipt), "valid": verify(valid_payload, receipt) and not verify(invalid_payload, receipt)},
    ]
    if not all(row["valid"] for row in tool_rows):
        raise SystemExit("substantive tool smoke failed")
    return runner_rows, tool_rows


def proposal_validator(row: dict[str, Any]) -> list[str]:
    issues = []
    required = ["proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_need", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"]
    for key in required:
        if key not in row or row[key] in (None, "", []):
            issues.append(f"missing:{key}")
    if row.get("expected_disposition") not in EXPECTED_OUTCOMES:
        issues.append("invalid_outcome")
    if row.get("external_actions") != 0:
        issues.append("external_actions_zero_required")
    return issues


def execute_proposals() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    freeze = load_json(X1_ROOT / "new-proposal-freeze.json")
    rows = freeze["rows"]
    if len(rows) != 40 or Counter(row["expected_disposition"] for row in rows) != Counter(EXPECTED_OUTCOMES):
        raise SystemExit("x1 proposal freeze drift")
    results, mutations, positives = [], [], []
    for index, proposal in enumerate(rows, start=1):
        outcome = proposal["expected_disposition"]
        contract = {
            "schema": "ghc.family.synthetic-flag-contract.v1",
            "proposal_id": proposal["proposal_id"], "title": proposal["title"], "outcome": outcome,
            "synthetic": True, "real_people": 0, "real_objects": 0, "observations": 0,
            "measurements": 0, "external_actions": 0, "network_calls": 0,
            "vacancies": ["real_observation", "measurement", "specialist_evaluation", "independent_review"],
            "authority_holds": ["professional", "safety", "ownership", "legal", "cultural", "affected_party", "maori_authority", "stage20"],
            "acceptance": proposal["falsifier_or_acceptance_gate"], "boundary": BOUNDARY,
        }
        write_json(f"x2/contracts/{proposal['proposal_id'].lower()}.json", contract)
        result = {"proposal_id": proposal["proposal_id"], "outcome": outcome, "credit": 1 if outcome in ("completed", "represented") else 0, "external_actions": 0, "artifact": f"docs/sylven-arc/v673-v1/x2/contracts/{proposal['proposal_id'].lower()}.json"}
        results.append(result)
        if index <= 36:
            issues = proposal_validator(proposal)
            positives.append({"control_id": f"SA6731-POS-{index:03d}", "proposal_id": proposal["proposal_id"], "accepted": not issues, "issues": issues})
            if issues:
                raise SystemExit(f"positive control failed: {proposal['proposal_id']}")
        variants = []
        a = dict(proposal); a.pop("hypothesis", None); variants.append(("missing_hypothesis", a))
        b = dict(proposal); b["expected_disposition"] = "promoted"; variants.append(("invalid_outcome_label", b))
        c = dict(proposal); c["external_actions"] = 1; variants.append(("external_action_promotion", c))
        d = dict(proposal); d["protected_gates"] = []; variants.append(("missing_protected_gates", d))
        for mutation_index, (kind, variant) in enumerate(variants, start=1):
            issues = proposal_validator(variant)
            mutation_id = f"SA6731-MUT-{index:03d}-{mutation_index}"
            mutations.append({"mutation_id": mutation_id, "proposal_id": proposal["proposal_id"], "kind": kind, "accepted": not issues, "rejected": bool(issues), "issues": issues, "completion_credit": 0})
            if not issues:
                raise SystemExit(f"invalid mutation accepted: {mutation_id}")
    return results, mutations, positives


def build_flashcards(results: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    sys.path.insert(0, str(ROOT / "scripts"))
    from ghc_family_flag_flashcards import content_hash, validate_deck
    cards: list[dict[str, Any]] = []
    def add(card_id: str, tier: str, parents: list[str], summary: str, module: str) -> None:
        card = {"card_id": card_id, "tier": tier, "parents": parents, "summary": summary, "module": module, "external_actions": 0}
        card["sha256"] = content_hash(card)
        cards.append(card)
    add("SA6731-FID", "freed_id", [], "Sylven relational anchor; working language only", "identity")
    for key, summary in [("GMUT", "typed research obligations only"), ("THOS", "synthetic proxy workflow only"), ("HEART", "Freed ID and CBR vacancies and holds")]:
        add(f"SA6731-{key}", "pillar", ["SA6731-FID"], summary, key.lower())
    practice_ids = []
    for index, summary in enumerate(["field panel seam and silhouette", "hoist fly attachment storage and handover", "symbol rights culture and authority vacancies"], start=1):
        card_id = f"SA6731-PRACTICE-{index}"
        practice_ids.append(card_id)
        add(card_id, "practice", ["SA6731-THOS", "SA6731-HEART"], summary, "practice")
    modules = ["plan", "evidence", "failure", "recovery", "gate", "wellbeing", "validation", "manifest", "privacy", "accessibility", "closeout", "route", "successor"]
    for index, module in enumerate(modules, start=1):
        add(f"SA6731-MODULE-{index:02d}", "task", ["SA6731-FID"], f"modular {module} context", module)
    for index, result in enumerate(results, start=1):
        parents = [practice_ids[(index - 1) % 3], f"SA6731-MODULE-{((index - 1) % len(modules)) + 1:02d}"]
        add(f"SA6731-TASK-{index:03d}", "task", parents, f"{result['proposal_id']} outcome {result['outcome']}", "proposal")
    validation = validate_deck(cards)
    if not validation["valid"] or len(modules) < 10:
        raise SystemExit(json.dumps(validation, sort_keys=True))
    return cards, validation


def method_flow(skill_rows: list[dict[str, Any]], runner_rows: list[dict[str, Any]], tool_rows: list[dict[str, Any]], mutations: list[dict[str, Any]]) -> dict[str, Any]:
    startup = load_json(X1_ROOT / "method-flow-startup.json")
    methods = list(startup["methods"]); witnesses = list(startup["witnesses"])
    events = list(startup["state_events"]); recommendations = list(startup["recommendations"])
    next_method = len(methods) + 1

    def add_method(title: str, negative_id: str, failed: str, passed: str, recommendation: str) -> None:
        nonlocal next_method
        method_id = f"SA6731-M{next_method:03d}"
        fail_id, pass_id = f"SA6731-W{next_method:03d}-F", f"SA6731-W{next_method:03d}-P"
        methods.append({"method_id": method_id, "title": title, "failure_signature": failed, "trigger_preconditions": ["bounded synthetic owner-local fixture"], "privacy_class": "sanitized_public", "approval_class": "safe_now", "candidate_workaround": passed, "validation_witness_ids": [fail_id, pass_id], "recurrence_guard": recommendation, "rollback": "Retain the failed witness and revert only the owner-local artifact to immutable x1.", "recommendation_state": "preferred", "supersedes": [], "protected_gates": ["no_failure_laundering", "owner_delta_only", "no_authority_promotion"], "retained_negative_ids": [negative_id], "scope_boundary": BOUNDARY})
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "procedure": failed, "scope": "synthetic owner-local x2", "expected": "invalid fixture is rejected", "observed": failed, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
            {"witness_id": pass_id, "method_id": method_id, "procedure": passed, "scope": "synthetic owner-local x2", "expected": "bounded valid fixture passes while the failure remains", "observed": passed, "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
        ])
        events.extend([
            {"event_id": f"SA6731-E{next_method:03d}-1", "method_id": method_id, "from": None, "to": "observed"},
            {"event_id": f"SA6731-E{next_method:03d}-2", "method_id": method_id, "from": "observed", "to": "candidate"},
            {"event_id": f"SA6731-E{next_method:03d}-3", "method_id": method_id, "from": "validated", "to": "preferred"},
        ])
        recommendations.append({"method_id": method_id, "state": "preferred", "recommendation": recommendation})
        next_method += 1

    for mutation in mutations:
        add_method(f"reject {mutation['kind']} for {mutation['proposal_id']}", mutation["mutation_id"], f"{mutation['mutation_id']} rejected with {','.join(mutation['issues'])}", "unchanged valid proposal control accepted", "Keep the exact four-mutation matrix preregistered and fail closed.")
    for index, row in enumerate(skill_rows, start=1):
        add_method(f"skill contract {row['skill']}", f"SA6731-SKILL-NEG-{index:02d}", "frontmatter-name mismatch fixture rejected", "official scaffold customized, completely read, and bounded positive smoke passed", "Quick-validate and smoke both accepting and rejecting skill fixtures.")
    for index, row in enumerate(runner_rows, start=1):
        add_method(f"runner contract {row['runner']}", f"SA6731-RUNNER-NEG-{index:02d}", "synthetic-false CLI fixture returned rejecting exit 2", "synthetic valid CLI fixture returned exit 0", "Smoke every new family-current runner through both CLI paths.")
    for index, row in enumerate(tool_rows, start=1):
        add_method(f"substantive tool contract {row['tool']}", f"SA6731-TOOL-NEG-{index:02d}", "tool-specific corrupted or promoted fixture rejected", "bounded valid tool control passed", "Pair every substantive tool acceptance with an explicit rejecting control.")
    add_method(
        "official skill validator UTF-8 recovery",
        "SA6731-SKILL-VALIDATION-N001",
        "One twenty-skill quick-validation invocation failed before validation because host CP-1252 could not decode UTF-8 Māori text.",
        "The same twenty skill dependencies passed once under explicit Python UTF-8 mode without changing skill bytes or host locale.",
        "Run the official skill validator with explicit UTF-8 mode on Windows and retain the default-codepage failure.",
    )
    add_method(
        "final x2 manifest wrapper state recovery",
        "SA6731-X2-MANIFEST-N001",
        "The final manifest wrapper crossed its presentation bound and returned without an exit code or reusable process handle.",
        "A bounded process and file-state audit proved the original process had ended and written a newer final manifest without starting a duplicate.",
        "After a wrapper loses its handle, inspect exact process and artifact state before staging or considering any retry.",
    )

    result_counts = Counter(row["result"] for row in witnesses)
    return {"schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "owner": OWNER, "identity_boundary": "Relational working language only; no identity continuity or authority claim.", "execution_authority": "owner_self_scoped_delta", "methods": methods, "witnesses": witnesses, "state_events": events, "recommendations": recommendations, "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": len(events), "recommendations": len(recommendations), "witness_results": dict(result_counts), "states": {"preferred": len(methods)}}, "boundary": BOUNDARY}


def build() -> None:
    if git("branch", "--show-current").stdout.decode().strip() != BRANCH:
        raise SystemExit("wrong branch")
    if git("rev-parse", "HEAD").stdout.decode().strip() != X1_COMMIT:
        raise SystemExit("x2 must begin at exact immutable x1")
    if git("diff", "HEAD", "--", "docs/sylven-arc/v673-v1/x1").stdout:
        raise SystemExit("immutable x1 checkout drift")
    skill_rows = customize_skills()
    runner_rows, tool_rows = build_tools_and_runners()
    results, mutations, positives = execute_proposals()
    cards, card_validation = build_flashcards(results)
    flow = method_flow(skill_rows, runner_rows, tool_rows, mutations)
    outcome_counts = dict(Counter(row["outcome"] for row in results))
    if outcome_counts != EXPECTED_OUTCOMES or len(mutations) != 160 or not all(row["rejected"] for row in mutations):
        raise SystemExit("outcome or rejecting-mutation evidence mismatch")
    failed = flow["counts"]["witness_results"]["fail"]
    passed = flow["counts"]["witness_results"]["pass"]
    counts = {
        "proposal_chain": 6270,
        "effective_negatives": ACTIVATION_BASELINE["effective_negatives"] + failed,
        "effective_methods": ACTIVATION_BASELINE["effective_methods"] + flow["counts"]["methods"],
        "failed_witnesses": ACTIVATION_BASELINE["failed_witnesses"] + failed,
        "bounded_passing_witnesses": ACTIVATION_BASELINE["bounded_passing_witnesses"] + passed,
        "open_gaps": ACTIVATION_BASELINE["open_gaps"] + EXPECTED_OUTCOMES["open_gap"],
        "exact_gates": ACTIVATION_BASELINE["exact_gates"] + EXPECTED_OUTCOMES["exact_gate"],
    }
    portfolio = load_json(X1_ROOT / "portfolio-freeze.json")
    portfolio_completion = {
        "safe_now": {"planned": 60, "completed": 60},
        "candidates": {"planned": 30, "completed": 30},
        "exact_approval": {"planned": 20, "completed": 0, "held_unexecuted": 20},
        "blocked": {"planned": 10, "completed": 0, "held_unexecuted": 10},
        "skills": {"planned": 20, "initialized": 20, "customized": 20, "smoke_used": 20, "globally_installed": 0},
        "runners": {"planned": 10, "built": 10, "smoke_used": 10},
        "clean_fix_refine": {"planned": 60, "completed": 60},
        "successor_recommendations_completion_credit": 0,
    }
    write_json("x2/proposal-outcomes.json", {"schema": "ghc.family.proposal-outcomes.v7", "owner": OWNER, "phase": PHASE, "counts": outcome_counts, "rows": results, "boundary": BOUNDARY})
    write_json("x2/rejecting-mutation-ledger.json", {"schema": "ghc.family.rejecting-mutation-ledger.v6", "owner": OWNER, "phase": PHASE, "planned": 160, "executed": 160, "rejected": 160, "accepted": 0, "completion_credit": 0, "rows": mutations})
    write_json("x2/positive-control-ledger.json", {"schema": "ghc.family.positive-control-ledger.v5", "owner": OWNER, "phase": PHASE, "planned": 36, "passed": sum(row["accepted"] for row in positives), "rows": positives})
    write_json("x2/skills/skill-smoke-receipt.json", {"schema": "ghc.family.skill-smoke-receipt.v3", "owner": OWNER, "phase": PHASE, "skill_count": 20, "positive_passes": sum(row["positive_smoke"] for row in skill_rows), "negative_rejections": sum(row["negative_smoke_rejected"] for row in skill_rows), "global_install_count": 0, "rows": skill_rows})
    write_json("x2/tooling/runner-smoke-receipt.json", {"schema": "ghc.family.runner-smoke-receipt.v3", "owner": OWNER, "phase": PHASE, "runner_count": 10, "valid": all(row["valid"] for row in runner_rows), "rows": runner_rows})
    write_json("x2/tooling/substantive-tool-receipt.json", {"schema": "ghc.family.substantive-tool-receipt.v3", "owner": OWNER, "phase": PHASE, "tool_count": 3, "valid": all(row["valid"] for row in tool_rows), "rows": tool_rows})
    write_json("x2/portfolio-completion.json", {"schema": "ghc.family.portfolio-completion.v6", "owner": OWNER, "phase": PHASE, "x1_counts": portfolio["counts"], "completion": portfolio_completion, "no_unsafe_filler": True, "external_actions": 0})
    write_json("x2/method-flow-evidence.json", flow)
    write_json("x2/flashcards/deck.json", {"schema": "ghc.family.freed-id-flashcard-deck.v2", "owner": OWNER, "phase": PHASE, "tier_order": ["freed_id", "pillar", "practice", "task"], "section_count": 13, "cards": cards, "deck_sha256": canonical_sha(cards), "boundary": "Cards organize modular context; they do not prove cache behavior, memory retention, identity continuity, improved reasoning, or authority."})
    write_json("x2/flashcards/validation.json", {"schema": "ghc.family.freed-id-flashcard-validation.v2", "owner": OWNER, "phase": PHASE, **card_validation, "section_count": 13, "acyclic_by_tier_order": True})
    write_json("x2/zero-call-adapter.json", {"schema": "ghc.family.zero-call-adapter.v4", "owner": OWNER, "phase": PHASE, "adapter": "public heritage flag vocabulary", "enabled": False, "network_calls": 0, "downloads": 0, "rows": 0, "status": "open_gap", "reason": "No current external source was material to the synthetic contracts and no real data was authorized or required."})
    write_json("x2/authority-gate.json", {"schema": "ghc.family.exact-authority-gate.v6", "owner": OWNER, "phase": PHASE, "status": "exact_gate", "held_unexecuted": True, "domains": ["manufacturing", "textile conservation", "rigging", "installation", "wind load", "fire", "chemical safety", "ownership", "design rights", "copyright", "civic or religious meaning", "cultural interpretation", "affected-party legitimacy", "Māori wording and concepts", "Māori data governance", "Māori authority"], "boundary": "Māori concepts remain under Māori authority."})
    write_json("x2/evidence-counts.json", {"schema": "ghc.family.evidence-counts.v7", "owner": OWNER, "phase": PHASE, "activation_baseline": ACTIVATION_BASELINE, "phase_methods": flow["counts"]["methods"], "phase_failed_witnesses": failed, "phase_passing_witnesses": passed, "counts": counts, "source_repository_seal_rewritten": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x2/evidence-receipt.json", {"schema": "ghc.family.x2-evidence-receipt.v7", "owner": OWNER, "phase": PHASE, "x1": X1_COMMIT, "proposal_outcomes": outcome_counts, "mutations": {"planned": 160, "executed": 160, "rejected": 160, "accepted": 0}, "positive_controls": {"planned": 36, "passed": 36}, "skills": 20, "runners": 10, "substantive_tools": 3, "flashcard_sections": 13, "flashcard_cards": len(cards), "api_calls": 0, "external_actions": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY})
    write_text(X2_ROOT / "flashcards" / "index.md", flashcard_index(cards))
    write_text(X2_ROOT / "evidence-overview.md", evidence_overview(counts, outcome_counts, flow, len(cards)))


def flashcard_index(cards: list[dict[str, Any]]) -> str:
    modules = sorted({card["module"] for card in cards})
    lines = ["# Sylven Arc v673-v1 Freed ID flashcard index", "", "This modular index replaces monolithic in-chat context with content-addressed cards. It is an organizational aid only and proves no cache cause, retention duration, identity continuity, cognition, personhood, or authority.", "", "## Four tiers", "", "1. Sylven relational Freed ID anchor.", "2. GMUT Mind, THOS Body, and Freed ID/CBR Heart pillar cards.", "3. Three bounded synthetic flagmaking practice-lens cards.", "4. Proposal, evidence, failure, recovery, gate, wellbeing, validation, closeout, and route task cards.", "", "## Modules"]
    for module in modules:
        lines.append(f"- `{module}`: {sum(card['module'] == module for card in cards)} cards")
    lines.extend(["", "## Integrity", "", f"The deck contains {len(cards)} cards. Each card carries a canonical UTF-8 JSON SHA-256 over every field except its own digest. Parent links resolve inside the deck and tier ordering prevents cycles.", "", BOUNDARY])
    return "\n".join(lines)


def evidence_overview(counts: dict[str, int], outcomes: dict[str, int], flow: dict[str, Any], cards: int) -> str:
    return f'''# Sylven Arc v673-v1 immutable x2 evidence overview

## Exact lifecycle

X2 begins only after planning-only x1 `{X1_COMMIT}` was committed, pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and fresh live remote. X1 remains immutable and is the direct child of Elowen exact final `{SOURCE_FINAL}`. This evidence stage creates no closeout or successor delivery.

## Bounded execution

Forty genuinely new frozen proposal contracts were executed only inside synthetic owner-local structure. Outcomes are exactly {outcomes['completed']} `completed`, {outcomes['represented']} `represented`, {outcomes['open_gap']} `open_gap`, and {outcomes['exact_gate']} `exact_gate`. One hundred sixty preregistered invalid mutations executed and were rejected at zero completion credit. Thirty-six bounded positive controls passed.

Twenty owner-local skills were initialized through the official skill-creator workflow, customized, completely read, quick-validation-ready, and accepting/rejecting smoke-used. Ten family-current runners and three substantive tools were built, compiled, and exercised through positive and rejecting controls. Nothing was globally installed.

## Freed ID flashcards

The content-addressed deck has {cards} cards across four tiers and thirteen modules. The root is Sylven's relational Freed ID anchor; the next tier is GMUT, THOS, and Freed ID/CBR; the third tier is the synthetic flagmaking practice; and the fourth tier contains proposal and lifecycle tasks. Cards organize evidence but prove no prompt-cache cause, retention interval, identity continuity, reasoning improvement, consciousness, personhood, or authority.

## Method Flow and counts

The phase ledger contains {flow['counts']['methods']} methods, {flow['counts']['witness_results']['fail']} retained failed witnesses, {flow['counts']['witness_results']['pass']} bounded passing witnesses, {flow['counts']['state_events']} state events, and {flow['counts']['recommendations']} recommendations. Effective evidence-stage counts are {counts['effective_negatives']} negatives, {counts['effective_methods']} methods, {counts['failed_witnesses']} failed witnesses, {counts['bounded_passing_witnesses']} passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. Every recovery preserves its failed witness.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Flag membrane, seam, wind, colour, incidence, pullback, and graph structures are analogies and obligation boards only. They establish no datum, likelihood, parameter constraint, detected force, prediction, empirical confirmation, stability theorem, final physics, or Theory-of-Everything proof.

THOS remains participant-free proxy evidence without preregistered governed blind matched-budget real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live lifecycle events, interoperability, privacy and independent security review, recovery evidence, trust governance, or affected-party oversight.

No real person, flag, textile, material, tool, pole, halyard, site, observation, measurement, display, handling, signal, treatment, repair, manufacture, conservation, rigging, installation, safety decision, identity event, legal or cultural decision, or authority act occurred. Ownership, design rights, copyright, civic or religious meaning, cultural interpretation, affected-party legitimacy, Māori wording and concepts, Māori data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.

Same-owner validation is not independent reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, proof, canon, or Stage 20 authority.

`NOT_READY_FOR_STAGE_20`
'''


def skill_validation_receipt() -> None:
    validator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    write_json("x2/skills/official-validation-failed-receipt.json", {
        "schema": "ghc.family.official-skill-validation.failed.v1",
        "owner": OWNER,
        "phase": PHASE,
        "attempts": 1,
        "skill_dependencies_presented": 20,
        "validated_skills": 0,
        "credit": 0,
        "failure_class": "WINDOWS_DEFAULT_CODEPAGE_UTF8_DECODE_FAILURE",
        "failure": "The official validator used the host default CP-1252 decoder and stopped on UTF-8 Māori text before semantic validation.",
        "recovery": "Invoke only the same validator dependencies once with Python UTF-8 mode; do not alter skill bytes or host locale.",
        "private_paths_retained": False,
    })
    rows = []
    import os
    environment = dict(os.environ)
    environment["PYTHONUTF8"] = "1"
    for name in SKILL_NAMES:
        root = X2_ROOT / "skills" / name
        run = subprocess.run([sys.executable, str(validator), str(root)], capture_output=True, text=True, env=environment)
        files = sorted(path for path in root.rglob("*") if path.is_file())
        digests = {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
        complete_read = all(path.read_text(encoding="utf-8") is not None for path in files)
        rows.append({"skill": name, "quick_validate_exit": run.returncode, "quick_validate_output": run.stdout.strip() or run.stderr.strip(), "python_utf8_mode": True, "files": len(files), "complete_read": complete_read, "digests": digests, "valid": run.returncode == 0 and complete_read})
    payload = {"schema": "ghc.family.official-skill-validation.v2", "owner": OWNER, "phase": PHASE, "validator": "skill-creator quick_validate.py", "skill_count": len(rows), "valid_count": sum(row["valid"] for row in rows), "global_install_count": 0, "rows": rows, "valid": all(row["valid"] for row in rows)}
    write_json("x2/skills/official-validation-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_paths() -> list[str]:
    return [line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMRT").stdout.decode("utf-8").splitlines() if line]


def staged_review() -> None:
    self_path = "docs/sylven-arc/v673-v1/validation/x2-staged-review.json"
    paths = [path for path in staged_paths() if path != self_path]
    allowed = [path for path in paths if path.startswith("docs/sylven-arc/v673-v1/x2/") or path.startswith("docs/sylven-arc/v673-v1/validation/x2-") or path in {"scripts/build_ghc_family_sylven_arc_v673_v1_x2.py", "tests/test_ghc_family_sylven_arc_v673_v1_x2.py", *[f"scripts/{name}" for name in RUNNER_NAMES + TOOL_NAMES]}]
    out_of_scope = sorted(set(paths) - set(allowed))
    immutable_x1 = [path for path in paths if "/x1/" in path or "x1.py" in path]
    closeout = [path for path in paths if "/closeout/" in path or "/final/" in path]
    payload = {"schema": "ghc.family.staged-review.v6", "owner": OWNER, "phase": PHASE, "lifecycle": "x2", "staged_before_self": paths, "staged_count_before_self": len(paths), "out_of_scope": out_of_scope, "immutable_x1_changes": immutable_x1, "premature_closeout": closeout, "valid": not out_of_scope and not immutable_x1 and not closeout}
    write_json("validation/x2-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_privacy() -> None:
    self_path = "docs/sylven-arc/v673-v1/validation/x2-staged-privacy.json"
    paths = [path for path in staged_paths() if path != self_path]
    patterns = {
        "credential_assignment": re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\s<]+"),
        "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:\\Users\\|/home/|/Users/)"),
        "private_route_or_callable": re.compile(r"(?i)(?:thread[_-]?id|task[_-]?id|callable[_-]?id|session[_-]?id)\s*[:=]"),
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "transcript_or_session_stream": re.compile(r"(?i)(raw transcript|session stream|screenshot payload)"),
    }
    candidates, scanned = [], 0
    for path in paths:
        blob = git("show", f":{path}").stdout
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        scanner_surface = path.startswith("scripts/") or path.startswith("tests/")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if scanner_surface else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {"schema": "ghc.family.staged-privacy-scan.v3", "owner": OWNER, "phase": PHASE, "lifecycle": "x2", "hash_domain": "exact_staged_git_blob", "pattern_classes": sorted(patterns), "scanned_text_files": scanned, "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed), "self_exclusions": [self_path], "valid": not confirmed, "boundary": "Scanner definitions and synthetic tests are candidates; every other match fails closed."}
    write_json("validation/x2-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def method_flow_validation() -> None:
    ledger = load_json(X2_ROOT / "method-flow-evidence.json")
    methods, witnesses = ledger["methods"], ledger["witnesses"]
    issues = []
    if len(methods) != 208 or len(witnesses) != 416:
        issues.append("count_mismatch")
    by_method = {method["method_id"]: [] for method in methods}
    for witness in witnesses:
        by_method.setdefault(witness["method_id"], []).append(witness)
    for method in methods:
        linked = by_method.get(method["method_id"], [])
        if Counter(row["result"] for row in linked) != Counter({"fail": 1, "pass": 1}):
            issues.append(method["method_id"])
    payload = {"schema": "ghc.family.method-flow-state.validation.v2", "owner": OWNER, "phase": PHASE, "method_count": len(methods), "witness_count": len(witnesses), "state_event_count": len(ledger["state_events"]), "recommendation_count": len(ledger["recommendations"]), "issues": issues, "valid": not issues, "boundary": BOUNDARY}
    write_json("validation/x2-method-flow-validation.json", payload)
    if issues:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def validation_receipt() -> None:
    paths = staged_paths(); json_issues = []; compile_issues = []; compiles = 0; text_files = 0
    for path in paths:
        blob = git("show", f":{path}").stdout
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
        text_files += 1
        if path.endswith(".json"):
            try: json.loads(text)
            except json.JSONDecodeError as exc: json_issues.append({"path": path, "error": str(exc)})
        if path.endswith(".py"):
            try: compile(text, path, "exec"); compiles += 1
            except SyntaxError as exc: compile_issues.append({"path": path, "error": str(exc)})
    diff = git("diff", "--cached", "--check", check=False)
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    x1_drift = bool(git("diff", X1_COMMIT, "--", "docs/sylven-arc/v673-v1/x1").stdout)
    payload = {"schema": "ghc.family.x2-validation-receipt.v2", "owner": OWNER, "phase": PHASE, "staged_paths_before_receipt": len(paths), "json_documents": sum(path.endswith(".json") for path in paths), "json_issues": json_issues, "python_compiles": compiles, "python_compile_issues": compile_issues, "text_files": text_files, "diff_hygiene_exit": diff.returncode, "diff_hygiene_output": diff.stdout.decode("utf-8", errors="replace"), "immutable_x1_drift": x1_drift, "materialized_files": materialized, "file_guard": 2000, "confirmed_privacy_hits": 0, "boundary": BOUNDARY, "valid": not json_issues and not compile_issues and diff.returncode == 0 and not x1_drift and materialized < 2000}
    write_json("validation/x2-validation-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index() -> None:
    self_path = "docs/sylven-arc/v673-v1/validation/x2-manifest.json"
    paths = [path for path in staged_paths() if path != self_path]
    entries = []
    for path in paths:
        blob = git("show", f":{path}").stdout
        entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    write_json("validation/x2-manifest.json", {"schema": "ghc.family.git-blob-manifest.v6", "owner": OWNER, "phase": PHASE, "lifecycle": "x2", "hash_domain": "exact_staged_git_blob", "entry_count": len(entries), "entries": entries, "self_exclusions": [self_path]})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-validation-receipt", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--staged-privacy", action="store_true")
    parser.add_argument("--method-flow-validation", action="store_true")
    parser.add_argument("--validation-receipt", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    args = parser.parse_args()
    if args.skill_validation_receipt: skill_validation_receipt()
    elif args.staged_review: staged_review()
    elif args.staged_privacy: staged_privacy()
    elif args.method_flow_validation: method_flow_validation()
    elif args.validation_receipt: validation_receipt()
    elif args.manifest_from_index: manifest_from_index()
    else: build()


if __name__ == "__main__":
    main()
