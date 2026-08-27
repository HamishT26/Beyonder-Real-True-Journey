"""Bounded synthetic contracts for Vesper Arlen v673-v6.

Nothing in this module reads a real instrument, observation, identity, person,
collection, location, key, credential, or external system.  The domain objects
are invented fixtures for software-validation evidence only.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Iterable


ALLOWED_UNITS = {"degree", "arcminute", "dimensionless", "kelvin", "second", "none"}
ALLOWED_VALUE_KINDS = {"transcribed", "derived", "corrected", "placeholder", "structural"}
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED_RECORD_FIELDS = {
    "synthetic",
    "synthetic_id",
    "proposal_id",
    "state",
    "units",
    "value_kind",
    "provenance",
    "real_rows",
    "network_calls",
    "external_actions",
    "authority_claim",
}


@dataclass(frozen=True)
class ValidationResult:
    accepted: bool
    errors: tuple[str, ...]


def validate_synthetic_record(record: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []
    missing = sorted(REQUIRED_RECORD_FIELDS - set(record))
    if missing:
        errors.append("missing_fields:" + ",".join(missing))
    if record.get("synthetic") is not True:
        errors.append("synthetic_flag_required")
    if not isinstance(record.get("synthetic_id"), str) or not record.get("synthetic_id", "").startswith("SYN-VA6736-"):
        errors.append("invalid_synthetic_id")
    if not isinstance(record.get("proposal_id"), str) or not re.fullmatch(r"VA6736-N\d{3}", record.get("proposal_id", "")):
        errors.append("invalid_proposal_id")
    if record.get("units") not in ALLOWED_UNITS:
        errors.append("unit_domain_escape")
    if record.get("value_kind") not in ALLOWED_VALUE_KINDS:
        errors.append("value_kind_domain_escape")
    provenance = record.get("provenance")
    if not isinstance(provenance, dict) or provenance.get("fixture_origin") != "invented_phase_local":
        errors.append("provenance_fixture_origin_required")
    if not isinstance(provenance, dict) or provenance.get("real_agent") is not None:
        errors.append("real_agent_forbidden")
    for field in ("real_rows", "network_calls", "external_actions"):
        if record.get(field) != 0:
            errors.append(f"{field}_must_be_zero")
    if record.get("authority_claim") is not False:
        errors.append("authority_claim_forbidden")
    if record.get("state") not in {"declared", "reserved", "represented", "gap", "gate"}:
        errors.append("state_domain_escape")
    return ValidationResult(not errors, tuple(errors))


def synthetic_record(proposal_id: str, index: int, *, state: str = "declared", units: str = "dimensionless", value_kind: str = "structural") -> dict[str, Any]:
    record = {
        "synthetic": True,
        "synthetic_id": f"SYN-VA6736-{index:03d}",
        "proposal_id": proposal_id,
        "state": state,
        "units": units,
        "value_kind": value_kind,
        "value": None,
        "uncertainty": {"lower": None, "upper": None, "reason": "no observation"},
        "provenance": {
            "fixture_origin": "invented_phase_local",
            "entity": f"synthetic:sextant-record-{index:03d}",
            "activity": "synthetic:bounded-documentation-validation",
            "real_agent": None,
        },
        "real_rows": 0,
        "network_calls": 0,
        "external_actions": 0,
        "authority_claim": False,
    }
    result = validate_synthetic_record(record)
    if not result.accepted:
        raise ValueError(result.errors)
    return record


def mutation_cases(record: dict[str, Any]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    missing = copy.deepcopy(record)
    missing.pop("synthetic")
    cases.append({"mutation": "missing_synthetic_flag", "record": missing})
    real_row = copy.deepcopy(record)
    real_row["real_rows"] = 1
    cases.append({"mutation": "real_row_injection", "record": real_row})
    authority = copy.deepcopy(record)
    authority["authority_claim"] = True
    cases.append({"mutation": "authority_upgrade", "record": authority})
    unit = copy.deepcopy(record)
    unit["units"] = "unbounded_navigation_fix"
    cases.append({"mutation": "unit_domain_escape", "record": unit})
    return cases


def canonical_digest(value: Any) -> dict[str, str]:
    import rfc8785

    canonical = rfc8785.dumps(value)
    return {"canonical_utf8": canonical.decode("utf-8"), "sha256": hashlib.sha256(canonical).hexdigest()}


def jsonpath_values(value: Any, expression: str) -> list[Any]:
    from jsonpath_ng import parse

    return [match.value for match in parse(expression).find(value)]


def component_tree_receipt() -> dict[str, Any]:
    from treelib import Tree

    tree = Tree()
    tree.create_node("synthetic sextant", "root")
    for tag in ("frame", "limb", "index-arm", "mirror-system", "telescope", "shade-stack"):
        tree.create_node(tag, tag, parent="root")
    tree.create_node("index-mirror", "index-mirror", parent="mirror-system")
    tree.create_node("horizon-glass", "horizon-glass", parent="mirror-system")
    edges = []
    for node in tree.all_nodes_itr():
        parent = tree.parent(node.identifier)
        if parent is not None:
            edges.append([parent.identifier, node.identifier])
    return {
        "node_count": tree.size(),
        "edge_count": len(edges),
        "depth": tree.depth(),
        "root": tree.root,
        "edges": sorted(edges),
        "real_instrument": False,
    }


def validate_outcome_ledger(rows: Iterable[dict[str, Any]]) -> ValidationResult:
    errors: list[str] = []
    seen: set[str] = set()
    for row in rows:
        proposal_id = row.get("proposal_id")
        if proposal_id in seen:
            errors.append(f"duplicate_proposal_id:{proposal_id}")
        seen.add(proposal_id)
        if row.get("outcome") not in ALLOWED_OUTCOMES:
            errors.append(f"unknown_outcome:{proposal_id}")
        if row.get("real_rows") != 0:
            errors.append(f"real_rows_nonzero:{proposal_id}")
        if row.get("network_calls") != 0:
            errors.append(f"network_calls_nonzero:{proposal_id}")
        if row.get("independent_reproduction") is not False:
            errors.append(f"independent_reproduction_forbidden:{proposal_id}")
    return ValidationResult(not errors, tuple(errors))


def structural_html_audit(html: str) -> dict[str, Any]:
    checks = {
        "language": '<html lang="en">' in html,
        "title": "<title>" in html,
        "main": "<main" in html,
        "heading": "<h1" in html,
        "table_caption": "<caption>" in html,
        "column_headers": 'scope="col"' in html,
        "skip_link": 'href="#main"' in html,
        "print_style": "@media print" in html,
        "manual_reservation": "Manual keyboard, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved." in html,
    }
    return {
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "structural_pass": all(checks.values()),
        "accessibility_complete": False,
    }


def make_accessible_companion(rows: list[dict[str, Any]]) -> str:
    table_rows = "\n".join(
        f"<tr><th scope=\"row\">{row['proposal_id']}</th><td>{row['outcome']}</td><td>{row['boundary']}</td></tr>"
        for row in rows
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vesper Arlen v673-v6 synthetic sextant evidence</title>
<style>
body {{ font-family: system-ui, sans-serif; line-height: 1.55; max-width: 78rem; margin: auto; padding: 1rem; }}
.skip {{ position: absolute; left: -9999px; }} .skip:focus {{ left: 1rem; background: white; padding: .5rem; }}
table {{ border-collapse: collapse; width: 100%; }} th, td {{ border: 1px solid #555; padding: .45rem; text-align: left; vertical-align: top; }}
@media print {{ .skip {{ display: none; }} body {{ max-width: none; }} }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<main id="main">
<h1>Vesper Arlen v673-v6 synthetic sextant evidence</h1>
<p>All records are invented software fixtures. No real instrument, observation, person, location, identity, right, or authority decision appears here.</p>
<p>Manual keyboard, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved.</p>
<table><caption>Bounded proposal outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Boundary</th></tr></thead><tbody>
{table_rows}
</tbody></table>
</main>
</body>
</html>
"""


def package_versions() -> dict[str, str]:
    import importlib.metadata as metadata

    return {name: metadata.version(name) for name in ("rfc8785", "jsonpath-ng", "treelib", "six")}


def deterministic_json_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
