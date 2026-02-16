"""
freed_id_minimum_disclosure_verifier.py
---------------------------------------

Reproducible governance check for Heart-track GOV-002:
"Credential presentations must support minimum-disclosure behavior."
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from Freed_id_registry import DIDDocument, FreedIDRegistry
from freed_id_minimum_disclosure import (
    MinimumDisclosurePolicy,
    build_minimum_disclosure_presentation,
    validate_minimum_disclosure_presentation,
)


@dataclass
class CheckResult:
    check: str
    status: str
    detail: str


def _build_markdown(generated_utc: str, overall_status: str, checks: List[CheckResult]) -> str:
    lines = [
        "# Freed ID Minimum-Disclosure Verification Report",
        "",
        f"- generated_utc: `{generated_utc}`",
        f"- control: `GOV-002`",
        f"- overall_status: **{overall_status}**",
        "",
        "## Checks",
        "| check | status | detail |",
        "|---|---|---|",
    ]
    for check in checks:
        lines.append(f"| {check.check} | {check.status} | {check.detail} |")
    return "\n".join(lines).strip() + "\n"


def _run_verification(policy_doc: Path, schema_doc: Path) -> List[CheckResult]:
    checks: List[CheckResult] = []

    if policy_doc.exists():
        checks.append(CheckResult("policy_doc_exists", "PASS", str(policy_doc)))
    else:
        checks.append(CheckResult("policy_doc_exists", "FAIL", f"missing {policy_doc}"))

    if schema_doc.exists():
        checks.append(CheckResult("schema_doc_exists", "PASS", str(schema_doc)))
    else:
        checks.append(CheckResult("schema_doc_exists", "FAIL", f"missing {schema_doc}"))

    if not (policy_doc.exists() and schema_doc.exists()):
        return checks

    with schema_doc.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    required_fields = set(schema.get("required", []))
    if required_fields:
        checks.append(CheckResult("schema_required_fields_present", "PASS", f"count={len(required_fields)}"))
    else:
        checks.append(CheckResult("schema_required_fields_present", "FAIL", "required array missing/empty"))
        return checks

    sample_claims = {
        "age_over_18": True,
        "residency_country": "NZ",
        "government_id": "ABC12345",
        "email": "sample@example.org",
        "phone": "+6400000000",
    }
    requested_fields = ["age_over_18", "residency_country", "government_id"]
    policy = MinimumDisclosurePolicy()
    presentation = build_minimum_disclosure_presentation(
        subject_did="did:freed:example:subject-1",
        credential_id="did:freed:example:subject-1#cred-0",
        claims=sample_claims,
        requested_fields=requested_fields,
        policy=policy,
    )

    disclosed_keys = set(presentation["disclosed_claims"].keys())
    if disclosed_keys == {"age_over_18", "residency_country"}:
        checks.append(CheckResult("default_sensitive_block", "PASS", "government_id blocked by default"))
    else:
        checks.append(CheckResult("default_sensitive_block", "FAIL", f"disclosed_keys={sorted(disclosed_keys)}"))

    denied_sensitive = set(presentation["denied_sensitive_fields"])
    if "government_id" in denied_sensitive:
        checks.append(CheckResult("denied_sensitive_tracking", "PASS", "government_id listed"))
    else:
        checks.append(CheckResult("denied_sensitive_tracking", "FAIL", f"denied_sensitive={sorted(denied_sensitive)}"))

    valid, detail = validate_minimum_disclosure_presentation(presentation, policy)
    checks.append(CheckResult("presentation_validation_default", "PASS" if valid else "FAIL", detail))

    allowed_policy = MinimumDisclosurePolicy(allowed_sensitive_fields={"government_id"})
    allowed_presentation = build_minimum_disclosure_presentation(
        subject_did="did:freed:example:subject-1",
        credential_id="did:freed:example:subject-1#cred-0",
        claims=sample_claims,
        requested_fields=requested_fields,
        policy=allowed_policy,
    )
    allowed_disclosed = set(allowed_presentation["disclosed_claims"].keys())
    if "government_id" in allowed_disclosed and "email" not in allowed_disclosed:
        checks.append(CheckResult("allowlisted_sensitive_field", "PASS", "government_id disclosed, email withheld"))
    else:
        checks.append(
            CheckResult("allowlisted_sensitive_field", "FAIL", f"disclosed={sorted(allowed_disclosed)}")
        )

    valid_allowed, detail_allowed = validate_minimum_disclosure_presentation(allowed_presentation, allowed_policy)
    checks.append(CheckResult("presentation_validation_allowlisted", "PASS" if valid_allowed else "FAIL", detail_allowed))

    missing_from_schema = sorted(required_fields - set(presentation.keys()))
    if not missing_from_schema:
        checks.append(CheckResult("schema_alignment", "PASS", "presentation contains all required schema keys"))
    else:
        checks.append(CheckResult("schema_alignment", "FAIL", f"missing={missing_from_schema}"))

    # API-path integration check through the registry presentation method
    registry = FreedIDRegistry()
    did = registry.register(
        DIDDocument(
            did="",
            controller="did:freed:controller",
            verification_methods=[{"id": "key-1", "type": "Ed25519", "publicKeyBase58": "GfH2..."}],
            services=[],
        )
    )
    registry.issue_credential(
        did,
        {
            "age_over_18": True,
            "residency_country": "NZ",
            "government_id": "ABC12345",
            "email": "sample@example.org",
        },
    )
    cred_id = f"{did}#cred-0"
    api_presentation = registry.build_credential_presentation(
        did,
        cred_id,
        requested_fields=["age_over_18", "government_id", "email"],
        policy=MinimumDisclosurePolicy(),
    )
    api_disclosed = set(api_presentation.get("disclosed_claims", {}).keys())
    if api_disclosed == {"age_over_18"}:
        checks.append(CheckResult("registry_api_min_disclosure", "PASS", "sensitive fields filtered via API"))
    else:
        checks.append(
            CheckResult("registry_api_min_disclosure", "FAIL", f"api_disclosed={sorted(api_disclosed)}")
        )

    valid_api, detail_api = validate_minimum_disclosure_presentation(
        api_presentation, MinimumDisclosurePolicy()
    )
    checks.append(CheckResult("registry_api_presentation_validation", "PASS" if valid_api else "FAIL", detail_api))

    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Freed ID GOV-002 minimum-disclosure verification.")
    parser.add_argument("--reports-dir", default="docs/heart-track-runs", help="Directory for timestamped outputs.")
    parser.add_argument(
        "--policy-doc",
        default="docs/freed-id-minimum-disclosure-policy-v0.md",
        help="Policy markdown path.",
    )
    parser.add_argument(
        "--schema-doc",
        default="docs/freed-id-minimum-disclosure-schema-v0.json",
        help="Policy schema path.",
    )
    parser.add_argument(
        "--latest-json",
        default="docs/heart-track-min-disclosure-latest.json",
        help="Latest JSON output path.",
    )
    parser.add_argument(
        "--latest-md",
        default="docs/heart-track-min-disclosure-latest.md",
        help="Latest markdown output path.",
    )
    args = parser.parse_args()

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    checks = _run_verification(Path(args.policy_doc), Path(args.schema_doc))
    overall_status = "PASS" if all(check.status == "PASS" for check in checks) else "FAIL"

    payload = {
        "generated_utc": generated_utc,
        "control_id": "GOV-002",
        "overall_status": overall_status,
        "checks": [asdict(check) for check in checks],
    }
    markdown = _build_markdown(generated_utc, overall_status, checks)

    timestamped_json = reports_dir / f"{stamp}-freedid-min-disclosure-check.json"
    timestamped_md = reports_dir / f"{stamp}-freedid-min-disclosure-check.md"
    latest_json = Path(args.latest_json)
    latest_md = Path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)

    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={overall_status}")
    print(f"timestamped_json={timestamped_json}")
    print(f"timestamped_md={timestamped_md}")
    print(f"latest_json={latest_json}")
    print(f"latest_md={latest_md}")
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
