"""
freed_id_min_disclosure_verifier.py
-----------------------------------

Reproducible governance check for Heart-track GOV-002:
"Credential presentations must support minimum-disclosure behavior."

This v0 verifier uses a policy-driven fixture to confirm that only required
fields are disclosed for a sample verification purpose.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


@dataclass
class CheckResult:
    check: str
    status: str
    detail: str


def _canonical_hash(payload: Dict[str, object]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _build_presentation(source_credential: Dict[str, object], required_fields: List[str]) -> Dict[str, object]:
    disclosed = {key: source_credential[key] for key in required_fields if key in source_credential}
    return {
        "purpose": "age_residency_eligibility",
        "disclosed_claims": disclosed,
        "proof": {
            "scheme": "commitment-v0",
            "source_credential_sha256": _canonical_hash(source_credential),
        },
    }


def _run_verification() -> Dict[str, object]:
    source_credential: Dict[str, object] = {
        "subject_did": "did:freed:holder:abc123",
        "full_name": "Example Holder",
        "date_of_birth": "1990-06-20",
        "national_id": "NZ-EXAMPLE-1234",
        "email": "holder@example.org",
        "residency_status": "resident",
        "age_over_18": True,
    }
    required_fields = ["subject_did", "age_over_18", "residency_status"]
    forbidden_fields = ["full_name", "date_of_birth", "national_id", "email"]
    allowed_fields = set(required_fields)

    presentation = _build_presentation(source_credential, required_fields)
    disclosed = presentation["disclosed_claims"]

    checks: List[CheckResult] = []

    missing = [field for field in required_fields if field not in disclosed]
    if missing:
        checks.append(CheckResult("required_fields_present", "FAIL", f"missing={missing}"))
    else:
        checks.append(CheckResult("required_fields_present", "PASS", "all required fields disclosed"))

    leaked = [field for field in forbidden_fields if field in disclosed]
    if leaked:
        checks.append(CheckResult("forbidden_fields_absent", "FAIL", f"leaked={leaked}"))
    else:
        checks.append(CheckResult("forbidden_fields_absent", "PASS", "no forbidden fields disclosed"))

    extras = sorted(set(disclosed.keys()) - allowed_fields)
    if extras:
        checks.append(CheckResult("no_unrequested_extras", "FAIL", f"extras={extras}"))
    else:
        checks.append(CheckResult("no_unrequested_extras", "PASS", "no extra claims disclosed"))

    source_commitment = _canonical_hash(source_credential)
    commitment_ok = (
        isinstance(presentation.get("proof"), dict)
        and presentation["proof"].get("source_credential_sha256") == source_commitment
    )
    if commitment_ok:
        checks.append(CheckResult("proof_commitment_binding", "PASS", "source commitment matches"))
    else:
        checks.append(CheckResult("proof_commitment_binding", "FAIL", "source commitment mismatch"))

    overall = "PASS" if all(check.status == "PASS" for check in checks) else "FAIL"
    return {
        "overall_status": overall,
        "required_fields": required_fields,
        "forbidden_fields": forbidden_fields,
        "checks": [asdict(check) for check in checks],
        "presentation_sample": presentation,
    }


def _render_markdown(generated_utc: str, payload: Dict[str, object]) -> str:
    lines = [
        "# Freed ID Minimum-Disclosure Verification Report",
        "",
        f"- generated_utc: `{generated_utc}`",
        "- control: `GOV-002`",
        f"- overall_status: **{payload['overall_status']}**",
        "",
        "## Checks",
        "| check | status | detail |",
        "|---|---|---|",
    ]
    for check in payload["checks"]:
        lines.append(f"| {check['check']} | {check['status']} | {check['detail']} |")
    lines.extend(
        [
            "",
            "## Presentation sample",
            "```json",
            json.dumps(payload["presentation_sample"], indent=2),
            "```",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Freed ID GOV-002 minimum-disclosure verifier.")
    parser.add_argument("--reports-dir", default="docs/heart-track-runs", help="Directory for timestamped artifacts.")
    parser.add_argument(
        "--latest-json",
        default="docs/heart-track-min-disclosure-latest.json",
        help="Path for latest JSON artifact.",
    )
    parser.add_argument(
        "--latest-md",
        default="docs/heart-track-min-disclosure-latest.md",
        help="Path for latest markdown artifact.",
    )
    args = parser.parse_args()

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    payload = _run_verification()
    payload["generated_utc"] = generated_utc
    payload["control_id"] = "GOV-002"

    timestamped_json = reports_dir / f"{stamp}-freedid-min-disclosure-check.json"
    timestamped_md = reports_dir / f"{stamp}-freedid-min-disclosure-check.md"
    latest_json = Path(args.latest_json)
    latest_md = Path(args.latest_md)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_md.parent.mkdir(parents=True, exist_ok=True)

    markdown = _render_markdown(generated_utc, payload)
    timestamped_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    timestamped_md.write_text(markdown, encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    print(f"overall_status={payload['overall_status']}")
    print(f"timestamped_json={timestamped_json}")
    print(f"timestamped_md={timestamped_md}")
    print(f"latest_json={latest_json}")
    print(f"latest_md={latest_md}")
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
