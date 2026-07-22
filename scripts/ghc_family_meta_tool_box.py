#!/usr/bin/env python3
"""Build and query a bounded, repository-relative GHC Family tool catalogue."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath


SCHEMA = "ghc.family.meta-tool-box.catalogue.v1"
KINDS = {"skill", "runner", "command", "method", "workflow"}
STATUSES = {"current", "compatibility", "historical", "candidate"}
EVIDENCE = {"observed", "validated", "preferred", "exact_gate"}
PROTECTED = ["failure_retention", "no_blind_execution", "no_destructive_delete", "no_independent_reproduction"]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def relative(repo: Path, path: Path) -> str:
    resolved_repo = repo.resolve()
    resolved = path.resolve()
    try:
        value = resolved.relative_to(resolved_repo).as_posix()
    except ValueError as exc:
        raise ValueError(f"path is outside repository scope: {path.name}") from exc
    return value


def tokens(value: str) -> list[str]:
    return sorted({word for word in re.findall(r"[a-z0-9]+", value.casefold()) if len(word) > 2 and word not in {"and", "the", "for", "with", "from"}})


def frontmatter(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    name_match = re.search(r"(?m)^name:\s*(.+?)\s*$", text)
    description_match = re.search(r"(?m)^description:\s*(.+?)\s*$", text)
    return (name_match.group(1).strip() if name_match else path.parent.name, description_match.group(1).strip() if description_match else "")


def status_for(name: str, path: str) -> str:
    lowered = f"{name} {path}".casefold()
    if any(label in lowered for label in ("historical", "v575", "v553", "aevren-")):
        return "historical"
    if any(label in lowered for label in ("compatibility", "legacy")):
        return "compatibility"
    if name.startswith("ghc-family-") or name.startswith("ghc_family_") or name.startswith("build_ghc_family_"):
        return "current"
    return "candidate"


def caller_documents(repo: Path, phase_root: Path) -> list[tuple[str, str]]:
    documents = []
    roots = [repo / "tests", phase_root]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.casefold() not in {".py", ".md", ".json", ".mjs", ".cjs"}:
                continue
            try:
                documents.append((relative(repo, path), path.read_text(encoding="utf-8", errors="ignore")))
            except OSError:
                continue
    return documents


def callers(documents: list[tuple[str, str]], needle: str) -> list[str]:
    return sorted({path for path, text in documents if needle in text})[:12]


def build(repo: Path, phase_root: Path) -> dict:
    repo = repo.resolve()
    phase_root = phase_root.resolve()
    cards = []
    documents = caller_documents(repo, phase_root)
    skill_root = phase_root / "skills"
    for path in sorted(skill_root.glob("*/SKILL.md")):
        name, description = frontmatter(path)
        rel = relative(repo, path)
        cards.append(
            {
                "card_id": f"skill:{name}",
                "name": name,
                "kind": "skill",
                "source_path": rel,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "status": status_for(name, rel),
                "evidence_state": "observed",
                "owner_scope": "Eiren v651-v5-2 remaster phase-local",
                "triggers": tokens(f"{name} {description}"),
                "caller_paths": callers(documents, name),
                "rollback": "Remove only the additive candidate from selection and retain its validation receipt and failed witnesses.",
                "protected_gates": PROTECTED,
            }
        )
    runner_names = {
        "ghc_family_meta_tool_box.py",
        "ghc_family_tool_trigger_collision_auditor.py",
        "ghc_family_runner_caller_map.py",
        "ghc_family_global_promotion_readiness.py",
        "ghc_family_tool_staleness_scorecard.py",
        "ghc_family_method_recommendation_index.py",
        "ghc_family_d_first_rotation_receipt.py",
        "ghc_family_commit_budget_guard.py",
        "ghc_family_single_pass_validation_planner.py",
        "ghc_family_tool_provenance_chain.py",
    }
    for name in sorted(runner_names):
        path = repo / "scripts" / name
        if not path.exists():
            continue
        rel = relative(repo, path)
        cards.append(
            {
                "card_id": f"runner:{name}",
                "name": name,
                "kind": "runner",
                "source_path": rel,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "status": "current",
                "evidence_state": "observed",
                "owner_scope": "family-compatible repository runner",
                "triggers": tokens(name),
                "caller_paths": callers(documents, name),
                "rollback": "Stop selecting the additive runner, retain callers and receipts, and preserve predecessor compatibility.",
                "protected_gates": PROTECTED,
            }
        )
    return {
        "schema": SCHEMA,
        "owner": "Eiren Kestrel",
        "phase": "v651-v5-2-remaster",
        "card_count": len(cards),
        "cards": sorted(cards, key=lambda row: row["card_id"]),
        "boundary": "Inventory and same-owner workflow evidence only; no execution, production, independent-reproduction, legal, cultural, identity, or Stage 20 authority.",
    }


def validate(catalogue: dict) -> dict:
    issues = []
    if catalogue.get("schema") != SCHEMA:
        issues.append("schema")
    cards = catalogue.get("cards", [])
    ids = [row.get("card_id") for row in cards]
    if len(ids) != len(set(ids)):
        issues.append("duplicate_card_id")
    for index, row in enumerate(cards):
        prefix = f"card[{index}]"
        if row.get("kind") not in KINDS:
            issues.append(f"{prefix}.kind")
        if row.get("status") not in STATUSES:
            issues.append(f"{prefix}.status")
        if row.get("evidence_state") not in EVIDENCE:
            issues.append(f"{prefix}.evidence_state")
        source = str(row.get("source_path", ""))
        if not source or PurePosixPath(source).is_absolute() or re.match(r"^[A-Za-z]:", source):
            issues.append(f"{prefix}.source_path")
        if not row.get("rollback"):
            issues.append(f"{prefix}.rollback")
        if not row.get("protected_gates"):
            issues.append(f"{prefix}.protected_gates")
    return {"schema": "ghc.family.meta-tool-box.validation.v1", "card_count": len(cards), "issues": issues, "valid": not issues, "boundary": "Structural validation only; not complete security, privacy, accessibility, or independent review."}


def query(catalogue: dict, args) -> dict:
    rows = catalogue.get("cards", [])
    for field, value in (("kind", args.kind), ("status", args.status), ("evidence_state", args.evidence_state), ("owner_scope", args.owner_scope)):
        if value:
            rows = [row for row in rows if row.get(field) == value]
    if args.trigger:
        wanted = set(tokens(args.trigger))
        rows = [row for row in rows if wanted <= set(row.get("triggers", []))]
    return {"schema": "ghc.family.meta-tool-box.query.v1", "filters": {"kind": args.kind, "status": args.status, "evidence_state": args.evidence_state, "owner_scope": args.owner_scope, "trigger": args.trigger}, "result_count": len(rows), "results": rows, "zero_result_is_refusal": len(rows) == 0}


def collisions(catalogue: dict) -> dict:
    rows = catalogue.get("cards", [])
    findings = []
    for left_index, left in enumerate(rows):
        left_tokens = set(left.get("triggers", []))
        for right in rows[left_index + 1 :]:
            right_tokens = set(right.get("triggers", []))
            union = left_tokens | right_tokens
            score = len(left_tokens & right_tokens) / len(union) if union else 0.0
            if score >= 0.45:
                findings.append({"left": left["card_id"], "right": right["card_id"], "token_jaccard": round(score, 6), "state": "review_required_no_silent_winner"})
    return {"schema": "ghc.family.meta-tool-box.collisions.v1", "finding_count": len(findings), "findings": findings, "selection_performed": False}


def promotion(catalogue: dict, card_id: str) -> dict:
    card = next((row for row in catalogue.get("cards", []) if row.get("card_id") == card_id), None)
    checks = {
        "card_found": card is not None,
        "catalogue_valid": validate(catalogue)["valid"],
        "validated_evidence": bool(card and card.get("evidence_state") in {"validated", "preferred"}),
        "caller_or_smoke_witness": bool(card and card.get("caller_paths")),
        "rollback_present": bool(card and card.get("rollback")),
        "additive_plan": True,
    }
    return {"schema": "ghc.family.meta-tool-box.promotion.v1", "card_id": card_id, "checks": checks, "state": "ready" if all(checks.values()) else "candidate", "destructive_action_authorized": False}


def attest(catalogue: dict, card_id: str, witness_path: Path) -> dict:
    witness = read_json(witness_path)
    if not witness.get("valid"):
        raise ValueError("validation witness is not valid")
    card = next((row for row in catalogue.get("cards", []) if row.get("card_id") == card_id), None)
    if card is None:
        raise ValueError("catalogue card not found")
    witness_value = witness_path.as_posix()
    if PurePosixPath(witness_value).is_absolute() or re.match(r"^[A-Za-z]:", witness_value):
        raise ValueError("witness path must be repository-relative")
    card["evidence_state"] = "validated"
    card["caller_paths"] = sorted(set([*card.get("caller_paths", []), witness_value]))
    card["validation_witness"] = witness_value
    return catalogue


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    commands = root.add_subparsers(dest="command", required=True)
    build_parser = commands.add_parser("build")
    build_parser.add_argument("--repo", required=True)
    build_parser.add_argument("--phase-root", required=True)
    build_parser.add_argument("--output", required=True)
    for name in ("validate", "collisions"):
        item = commands.add_parser(name)
        item.add_argument("--catalogue", required=True)
        item.add_argument("--output", required=True)
    query_parser = commands.add_parser("query")
    query_parser.add_argument("--catalogue", required=True)
    query_parser.add_argument("--output", required=True)
    query_parser.add_argument("--kind", choices=sorted(KINDS))
    query_parser.add_argument("--status", choices=sorted(STATUSES))
    query_parser.add_argument("--evidence-state", choices=sorted(EVIDENCE))
    query_parser.add_argument("--owner-scope")
    query_parser.add_argument("--trigger")
    promotion_parser = commands.add_parser("promotion")
    promotion_parser.add_argument("--catalogue", required=True)
    promotion_parser.add_argument("--card-id", required=True)
    promotion_parser.add_argument("--output", required=True)
    attest_parser = commands.add_parser("attest")
    attest_parser.add_argument("--catalogue", required=True)
    attest_parser.add_argument("--card-id", required=True)
    attest_parser.add_argument("--witness", required=True)
    attest_parser.add_argument("--output", required=True)
    return root


def main() -> None:
    args = parser().parse_args()
    output = Path(args.output)
    if args.command == "build":
        payload = build(Path(args.repo), Path(args.phase_root))
    else:
        catalogue = read_json(Path(args.catalogue))
        if args.command == "validate":
            payload = validate(catalogue)
        elif args.command == "collisions":
            payload = collisions(catalogue)
        elif args.command == "query":
            payload = query(catalogue, args)
        elif args.command == "promotion":
            payload = promotion(catalogue, args.card_id)
        else:
            payload = attest(catalogue, args.card_id, Path(args.witness))
    write_json(output, payload)
    print(json.dumps({"command": args.command, "output": output.as_posix(), "valid": payload.get("valid", True), "count": payload.get("card_count", payload.get("result_count", payload.get("finding_count")))}, sort_keys=True))


if __name__ == "__main__":
    main()
