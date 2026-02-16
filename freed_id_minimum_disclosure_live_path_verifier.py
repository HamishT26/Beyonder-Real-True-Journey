"""
freed_id_minimum_disclosure_live_path_verifier.py
-------------------------------------------------

Live-path verifier for GOV-002 using the FreedIDRegistry presentation API:
`FreedIDRegistry.build_credential_presentation(...)`.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from Freed_id_registry import DIDDocument, FreedIDRegistry
from freed_id_minimum_disclosure import MinimumDisclosurePolicy


@dataclass
class CheckResult:
    check: str
    status: str
    detail: str


def _build_markdown(generated_utc: str, overall_status: str, checks: List[CheckResult]) -> str:
    lines = [
        "# Freed ID Minimum-Disclosure Live-Path Verification Report",
        "",
        f"- generated_utc: `{generated_utc}`",
        "- control: `GOV-002`",
        f"- overall_status: **{overall_status}**",
        "",
        "## Checks",
        "| check | status | detail |",
        "|---|---|---|",
    ]
    for check in checks:
        lines.append(f"| {check.check} | {check.status} | {check.detail} |")
    return "\n".join(lines).strip() + "\n"


def _run(audit_ledger: Path) -> List[CheckResult]:
    checks: List[CheckResult] = []
    if audit_ledger.exists():
        audit_ledger.unlink()

    registry = FreedIDRegistry(audit_ledger_path=str(audit_ledger))
    did = registry.register(
        DIDDocument(
            did="",
            controller="did:freed:controller:live",
            verification_methods=[{"id": "key-1", "type": "Ed25519", "publicKeyBase58": "GfH2..."}],
            services=[],
        )
    )
    checks.append(CheckResult("register_did", "PASS", f"did={did}"))

    claims = {
        "age_over_18": True,
        "residency_country": "NZ",
        "government_id": "NZ-EXAMPLE-987",
        "email": "holder@example.org",
    }
    registry.issue_credential(did, claims)
    cred_id = f"{did}#cred-0"
    checks.append(CheckResult("issue_credential", "PASS", f"credential_id={cred_id}"))

    requested = ["age_over_18", "residency_country", "government_id"]

    default_presentation = registry.build_credential_presentation(
        did=did,
        credential_id=cred_id,
        requested_fields=requested,
        policy=MinimumDisclosurePolicy(),
    )
    disclosed_default = set(default_presentation.get("disclosed_claims", {}).keys())
    denied_default = set(default_presentation.get("denied_sensitive_fields", []))
    if disclosed_default == {"age_over_18", "residency_country"}:
        checks.append(CheckResult("default_policy_block", "PASS", "government_id withheld by default policy"))
    else:
        checks.append(CheckResult("default_policy_block", "FAIL", f"disclosed={sorted(disclosed_default)}"))

    if "government_id" in denied_default:
        checks.append(CheckResult("default_denied_tracking", "PASS", "government_id recorded as denied"))
    else:
        checks.append(CheckResult("default_denied_tracking", "FAIL", f"denied={sorted(denied_default)}"))

    allow_policy = MinimumDisclosurePolicy(allowed_sensitive_fields={"government_id"})
    allow_presentation = registry.build_credential_presentation(
        did=did,
        credential_id=cred_id,
        requested_fields=requested,
        policy=allow_policy,
    )
    disclosed_allow = set(allow_presentation.get("disclosed_claims", {}).keys())
    if "government_id" in disclosed_allow and "email" not in disclosed_allow:
        checks.append(CheckResult("allowlisted_sensitive_disclosure", "PASS", "allowlisted sensitive field disclosed"))
    else:
        checks.append(
            CheckResult("allowlisted_sensitive_disclosure", "FAIL", f"disclosed={sorted(disclosed_allow)}")
        )

    if not audit_ledger.exists():
        checks.append(CheckResult("audit_ledger_exists", "FAIL", f"missing={audit_ledger}"))
        return checks

    entries = []
    with audit_ledger.open("r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if line:
                entries.append(json.loads(line))
    action_names = [str(entry.get("action")) for entry in entries]
    build_count = action_names.count("build_presentation")
    if build_count >= 2:
        checks.append(CheckResult("audit_build_presentation_events", "PASS", f"count={build_count}"))
    else:
        checks.append(CheckResult("audit_build_presentation_events", "FAIL", f"count={build_count}"))

    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Run GOV-002 live-path minimum-disclosure verification.")
    parser.add_argument("--audit-ledger", default="docs/freed-id-live-path-audit-log.jsonl")
    parser.add_argument("--reports-dir", default="docs/heart-track-runs")
    parser.add_argument("--latest-json", default="docs/heart-track-min-disclosure-live-latest.json")
    parser.add_argument("--latest-md", default="docs/heart-track-min-disclosure-live-latest.md")
    args = parser.parse_args()

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    checks = _run(Path(args.audit_ledger))
    overall_status = "PASS" if all(check.status == "PASS" for check in checks) else "FAIL"

    payload = {
        "generated_utc": generated_utc,
        "control_id": "GOV-002",
        "mode": "live_path",
        "overall_status": overall_status,
        "checks": [asdict(check) for check in checks],
    }
    markdown = _build_markdown(generated_utc, overall_status, checks)

    timestamped_json = reports_dir / f"{stamp}-freedid-min-disclosure-live-check.json"
    timestamped_md = reports_dir / f"{stamp}-freedid-min-disclosure-live-check.md"
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
    print(f"audit_ledger={args.audit_ledger}")
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
