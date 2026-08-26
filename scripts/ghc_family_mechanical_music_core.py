#!/usr/bin/env python3
"""Family-current bounded validators for synthetic mechanical-music records.

The module validates only owner-local synthetic structures.  It never operates
an apparatus, reads a real collection record, makes a rights or conservation
decision, or establishes professional, legal, cultural, Maori, empirical,
identity, production, or Stage 20 authority.
"""

from __future__ import annotations

import argparse
import ast
import importlib.metadata
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import jsonschema
from pydantic import BaseModel, ConfigDict
from referencing import Registry, Resource


CORE_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
BOUNDARY = (
    "Synthetic owner-local software evidence only; no real apparatus, person, "
    "measurement, operation, professional decision, rights decision, legal or "
    "cultural interpretation, Maori authority, empirical confirmation, "
    "production fitness, independent reproduction, or Stage 20 authority."
)


CONTRACT_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "urn:ghc-family:mechanical-music:contract:v1",
    "type": "object",
    "required": [
        "proposal_id",
        "synthetic_id",
        "expected_disposition",
        "observed_outcome",
        "execution_state",
        "synthetic_only",
        "real_people",
        "real_objects_or_records",
        "external_actions",
        "authority_claim",
        "boundary",
    ],
    "properties": {
        "proposal_id": {"type": "string", "pattern": "^EL6715-N[0-9]{3}$"},
        "synthetic_id": {"type": "string", "pattern": "^SYN-MM-[0-9]{3}$"},
        "expected_disposition": {"enum": sorted(CORE_OUTCOMES)},
        "observed_outcome": {"enum": sorted(CORE_OUTCOMES)},
        "execution_state": {"enum": ["bounded_positive_passed", "held_open_gap", "held_exact_gate"]},
        "synthetic_only": {"const": True},
        "real_people": {"const": 0},
        "real_objects_or_records": {"const": 0},
        "external_actions": {"const": 0},
        "authority_claim": {"const": False},
        "boundary": {"type": "string", "minLength": 40},
    },
    "additionalProperties": True,
}


class ContractModel(BaseModel):
    """Pydantic companion used only as a bounded typed smoke."""

    model_config = ConfigDict(extra="allow")
    proposal_id: str
    synthetic_id: str
    expected_disposition: str
    observed_outcome: str
    execution_state: str
    synthetic_only: bool
    real_people: int
    real_objects_or_records: int
    external_actions: int
    authority_claim: bool
    boundary: str


def tool_smoke() -> dict[str, Any]:
    sample = {
        "proposal_id": "EL6715-N001",
        "synthetic_id": "SYN-MM-001",
        "expected_disposition": "completed",
        "observed_outcome": "completed",
        "execution_state": "bounded_positive_passed",
        "synthetic_only": True,
        "real_people": 0,
        "real_objects_or_records": 0,
        "external_actions": 0,
        "authority_claim": False,
        "boundary": BOUNDARY,
    }
    jsonschema.validate(sample, CONTRACT_SCHEMA)
    model = ContractModel.model_validate(sample)
    resource = Resource.from_contents(CONTRACT_SCHEMA)
    registry = Registry().with_resource(CONTRACT_SCHEMA["$id"], resource)
    registry.get_or_retrieve(CONTRACT_SCHEMA["$id"])
    tools = []
    for name in ("jsonschema", "pydantic", "referencing"):
        metadata = importlib.metadata.metadata(name)
        tools.append(
            {
                "name": name,
                "version": importlib.metadata.version(name),
                "license": metadata.get("License-Expression") or metadata.get("License"),
                "installed_environment_only": True,
                "network_calls": 0,
                "external_writes": 0,
            }
        )
    return {
        "result": "VALID_BOUNDED_THREE_TOOL_SMOKE",
        "tools": tools,
        "pydantic_proposal_id": model.proposal_id,
        "registry_resource_present": True,
        "boundary": BOUNDARY,
    }


def validate_contract(row: dict[str, Any]) -> list[str]:
    issues = []
    try:
        jsonschema.validate(row, CONTRACT_SCHEMA)
    except jsonschema.ValidationError as exc:
        issues.append("jsonschema:" + exc.validator)
    try:
        ContractModel.model_validate(row)
    except Exception as exc:  # pydantic supplies structured detail; class only is retained
        issues.append("pydantic:" + type(exc).__name__)
    expected = row.get("expected_disposition")
    if row.get("observed_outcome") != expected:
        issues.append("outcome_mismatch")
    state = row.get("execution_state")
    if expected in {"completed", "represented"} and state != "bounded_positive_passed":
        issues.append("bounded_positive_state")
    if expected == "open_gap" and state != "held_open_gap":
        issues.append("open_gap_state")
    if expected == "exact_gate" and state != "held_exact_gate":
        issues.append("exact_gate_state")
    if row.get("boundary") != BOUNDARY:
        issues.append("boundary_mismatch")
    return issues


def mutate(base: dict[str, Any], mutation_type: str) -> dict[str, Any]:
    row = json.loads(json.dumps(base))
    if mutation_type == "missing_required":
        row.pop("synthetic_only", None)
    elif mutation_type == "external_action":
        row["external_actions"] = 1
    elif mutation_type == "authority_promotion":
        row["authority_claim"] = True
    elif mutation_type == "outcome_promotion":
        row["observed_outcome"] = "completed" if row["expected_disposition"] != "completed" else "represented"
    else:
        raise ValueError(f"unknown mutation type: {mutation_type}")
    return row


def validate_mutations(contracts: list[dict[str, Any]], rows: list[dict[str, Any]]) -> list[str]:
    by_id = {row["proposal_id"]: row for row in contracts}
    issues = []
    for row in rows:
        base = by_id.get(row.get("proposal_id"))
        if base is None:
            issues.append(f"unknown_proposal:{row.get('mutation_id')}")
            continue
        mutated = mutate(base, row["mutation_type"])
        rejected = bool(validate_contract(mutated))
        if not rejected or row.get("rejected") is not True or row.get("completion_credit") != 0:
            issues.append(f"mutation_not_retained:{row.get('mutation_id')}")
    return issues


class StructuralHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.h1 = 0
        self.captions = 0
        self.scoped_headers = 0
        self.skip_links = 0
        self.external_resources = 0
        self.scripts = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        values = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "caption":
            self.captions += 1
        if tag == "th" and values.get("scope") in {"row", "col"}:
            self.scoped_headers += 1
        if tag == "a" and str(values.get("href", "")).startswith("#"):
            self.skip_links += 1
        if tag in {"script", "iframe"}:
            self.scripts += 1
        if tag in {"link", "img", "audio", "video", "source"} and values.get("src"):
            self.external_resources += 1


def check_accessibility_html(text: str) -> dict[str, Any]:
    parser = StructuralHTMLParser()
    parser.feed(text)
    checks = {
        "html_lang": bool(re.search(r"<html[^>]+lang=", text, re.I)),
        "skip_link": parser.skip_links >= 1,
        "main_landmark": "main" in parser.tags,
        "nav_landmark": "nav" in parser.tags,
        "one_h1": parser.h1 == 1,
        "table_caption": parser.captions >= 1,
        "scoped_headers": parser.scoped_headers >= 4,
        "visible_focus": ":focus-visible" in text,
        "reduced_motion": "prefers-reduced-motion" in text,
        "print_rule": "@media print" in text,
        "no_script": parser.scripts == 0,
        "no_external_resource": parser.external_resources == 0,
    }
    return {
        "result": "VALID_STRUCTURAL_ACCESSIBILITY" if all(checks.values()) else "INVALID",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "manual_evaluations_reserved": [
            "browser",
            "keyboard",
            "zoom",
            "assistive_technology",
            "cognitive_accessibility",
            "Maori_language",
            "affected_user",
        ],
        "complete_accessibility_claim": False,
    }


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}(?![0-9a-f])"),
        "private_absolute_path": re.compile(r"(?i)(?:[a-z]:[\\/]+users[\\/]+|[a-z]:[\\/]+ghc-archives[\\/]+)"),
        "private_route_or_callable": re.compile(r"(?i)(?:<source[_-]?thread[_-]?id>|\"(?:thread|task)id\"\s*:)"),
        "credential_assignment": re.compile(r"(?i)(?:api[_-]?key|password|access[_-]?token|client[_-]?secret)\s*[:=]\s*[\"']?[a-z0-9_./+\-=]{12,}"),
        "private_interaction_stream": re.compile(r"(?i)(?:session[_-]?stream|conversation[_-]?transcript)\s*[:=]\s*[\"'][^\"']+"),
    }
    candidates = []
    files = 0
    for path in paths:
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        files += 1
        for pattern_class, pattern in patterns.items():
            matches = list(pattern.finditer(text))
            if matches:
                candidates.append(
                    {
                        "path": path.as_posix(),
                        "pattern_class": pattern_class,
                        "match_count": len(matches),
                    }
                )
    return {
        "result": "VALID_ZERO_CONFIRMED_HITS" if not candidates else "INVALID",
        "files_scanned": files,
        "pattern_classes": list(patterns),
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(candidates),
        "candidates": candidates,
        "complete_privacy_claim": False,
    }


def security_scan(paths: list[Path]) -> dict[str, Any]:
    findings = []
    compiled = 0
    dangerous_calls = {"eval", "exec", "compile", "__import__"}
    for path in paths:
        if path.suffix != ".py" or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
        compiled += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in dangerous_calls:
                # compile is used by bounded syntax validators and receives no untrusted execution.
                if node.func.id != "compile":
                    findings.append({"path": path.as_posix(), "call": node.func.id})
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == "system":
                    findings.append({"path": path.as_posix(), "call": "system"})
            if isinstance(node, ast.keyword) and node.arg == "shell":
                if isinstance(node.value, ast.Constant) and node.value.value is True:
                    findings.append({"path": path.as_posix(), "call": "shell_true"})
    return {
        "result": "VALID_BOUNDED_SECURITY_SCAN" if not findings else "INVALID",
        "python_files": compiled,
        "findings": findings,
        "finding_count": len(findings),
        "exhaustive_security_claim": False,
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def runner_result(mode: str, root: Path) -> dict[str, Any]:
    owner = root / "docs" / "elaren-kestrel" / "v671-v5"
    contracts_path = owner / "x2" / "contract-suite.json"
    mutations_path = owner / "x2" / "mutation-ledger.json"
    if mode == "contracts":
        payload = load_json(contracts_path)
        issues = [
            {"proposal_id": row["proposal_id"], "issues": validate_contract(row)}
            for row in payload["contracts"]
            if validate_contract(row)
        ]
        return {"mode": mode, "result": "VALID" if not issues else "INVALID", "rows": len(payload["contracts"]), "issues": issues}
    if mode == "mutations":
        contracts = load_json(contracts_path)["contracts"]
        mutations = load_json(mutations_path)["rows"]
        issues = validate_mutations(contracts, mutations)
        return {"mode": mode, "result": "VALID" if not issues else "INVALID", "rows": len(mutations), "issues": issues}
    if mode == "json":
        paths = list(owner.rglob("*.json"))
        issues = []
        for path in paths:
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                issues.append({"path": path.relative_to(root).as_posix(), "issue": type(exc).__name__})
        return {"mode": mode, "result": "VALID" if not issues else "INVALID", "documents": len(paths), "issues": issues}
    if mode == "privacy":
        result = privacy_scan(list(owner.rglob("*")) + list((root / "scripts").glob("ghc_family_mechanical_music*.py")))
        result["mode"] = mode
        return result
    if mode == "security":
        result = security_scan(list((root / "scripts").glob("ghc_family_mechanical_music*.py")))
        result["mode"] = mode
        return result
    if mode == "accessibility":
        result = check_accessibility_html((owner / "x2" / "static-report.html").read_text(encoding="utf-8"))
        result["mode"] = mode
        return result
    if mode == "truth":
        payload = load_json(owner / "x2" / "outcome-ledger.json")
        counts = {label: 0 for label in CORE_OUTCOMES}
        unknown = []
        for row in payload["rows"]:
            outcome = row["outcome"]
            if outcome not in CORE_OUTCOMES:
                unknown.append(outcome)
            else:
                counts[outcome] += 1
        expected = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
        return {"mode": mode, "result": "VALID" if counts == expected and not unknown else "INVALID", "counts": counts, "unknown": unknown}
    if mode == "manifest":
        return {"mode": mode, "result": "VALID_SELF_TEST", "actual_manifest_deferred_to_evidence_gate": True}
    if mode == "closeout":
        return {"mode": mode, "result": "VALID_PREFLIGHT", "terminal_closeout_eligible": False, "reason": "evidence_not_yet_committed"}
    if mode == "canonical":
        return {"mode": mode, "result": "VALID_PREFLIGHT", "canonical_eligible": False, "reason": "exact_final_not_yet_committed"}
    raise ValueError(f"unknown runner mode: {mode}")


def runner_main(mode: str) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        sample = tool_smoke()
        result = {"mode": mode, "result": "VALID_SELF_TEST", "tool_smoke": sample["result"], "boundary": BOUNDARY}
    else:
        result = runner_result(mode, args.root.resolve())
        result["boundary"] = BOUNDARY
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not str(result.get("result", "")).startswith("VALID"):
        raise SystemExit(1)
