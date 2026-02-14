"""
freed_id_control_verifier.py
----------------------------

Reproducible governance check for a Heart-track control:
GOV-005 (revoked identities cannot perform privileged credential actions).

Outputs:
1) timestamped JSON + markdown artifacts under docs/heart-track-runs/
2) latest JSON + markdown pointers for quick review
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from freed_id_registry import DIDDocument, FreedIDRegistry


@dataclass
class CheckResult:
    check: str
    status: str
    detail: str


def _build_markdown(generated_utc: str, overall_status: str, results: List[CheckResult]) -> str:
    lines = [
        "# Freed ID Governance Verification Report",
        "",
        f"- generated_utc: `{generated_utc}`",
        f"- control: `GOV-005`",
        f"- overall_status: **{overall_status}**",
        "",
        "## Checks",
        "| check | status | detail |",
        "|---|---|---|",
    ]
    for result in results:
        lines.append(f"| {result.check} | {result.status} | {result.detail} |")
    return "\n".join(lines).strip() + "\n"


def _run_verification() -> List[CheckResult]:
    results: List[CheckResult] = []
    registry = FreedIDRegistry()
    doc = DIDDocument(
        did="",
        controller="did:freed:controller",
        verification_methods=[
            {
                "id": "key-1",
                "type": "Ed25519VerificationKey2018",
                "publicKeyBase58": "GfH2...",
            }
        ],
        services=[],
    )
    did = registry.register(doc)
    results.append(CheckResult("register_did", "PASS", f"registered {did}"))

    try:
        registry.issue_credential(did, {"claim": "baseline", "issuer": "did:freed:issuer"})
        results.append(CheckResult("issue_credential_before_revoke", "PASS", "credential accepted"))
    except Exception as exc:  # pragma: no cover
        results.append(CheckResult("issue_credential_before_revoke", "FAIL", f"unexpected error: {exc}"))
        return results

    registry.revoke(did)
    results.append(CheckResult("revoke_did", "PASS", "did marked revoked"))

    blocked = False
    try:
        registry.issue_credential(did, {"claim": "should_fail", "issuer": "did:freed:issuer"})
    except KeyError:
        blocked = True

    if blocked:
        results.append(
            CheckResult("issue_credential_after_revoke", "PASS", "rejected as expected for revoked did")
        )
    else:
        results.append(CheckResult("issue_credential_after_revoke", "FAIL", "credential was not blocked"))

    # verify_credential must return False for revoked DIDs
    credential_id = f"{did}#cred-0"
    exists_for_revoked = registry.verify_credential(did, credential_id)
    if exists_for_revoked:
        results.append(CheckResult("verify_credential_after_revoke", "FAIL", "revoked did still verifies"))
    else:
        results.append(CheckResult("verify_credential_after_revoke", "PASS", "revoked did does not verify"))

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Freed ID governance control verification.")
    parser.add_argument("--reports-dir", default="docs/heart-track-runs", help="Directory for timestamped outputs.")
    parser.add_argument(
        "--latest-json",
        default="docs/heart-track-governance-latest.json",
        help="Path for latest JSON output.",
    )
    parser.add_argument(
        "--latest-md",
        default="docs/heart-track-governance-latest.md",
        help="Path for latest markdown output.",
    )
    args = parser.parse_args()

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    results = _run_verification()
    overall_status = "PASS" if all(result.status == "PASS" for result in results) else "FAIL"

    payload = {
        "generated_utc": generated_utc,
        "control_id": "GOV-005",
        "overall_status": overall_status,
        "checks": [asdict(result) for result in results],
    }
    markdown = _build_markdown(generated_utc, overall_status, results)

    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamped_json = reports_dir / f"{stamp}-freedid-gov-check.json"
    timestamped_md = reports_dir / f"{stamp}-freedid-gov-check.md"
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
