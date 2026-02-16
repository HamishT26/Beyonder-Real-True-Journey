"""
freed_id_auditability_verifier.py
---------------------------------

Reproducible governance check for Heart-track GOV-003:
"Identity and governance actions must emit append-only audit records."

Checks:
1. registry actions create an audit ledger,
2. expected action sequence exists,
3. hash-chain integrity verifies end-to-end.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from Freed_id_registry import DIDDocument, FreedIDRegistry
from freed_id_audit_log import FreedIDAuditLedger


@dataclass
class CheckResult:
    check: str
    status: str
    detail: str


def _build_markdown(generated_utc: str, overall_status: str, ledger_path: str, checks: List[CheckResult]) -> str:
    lines = [
        "# Freed ID Auditability Verification Report",
        "",
        f"- generated_utc: `{generated_utc}`",
        f"- control: `GOV-003`",
        f"- ledger_path: `{ledger_path}`",
        f"- overall_status: **{overall_status}**",
        "",
        "## Checks",
        "| check | status | detail |",
        "|---|---|---|",
    ]
    for check in checks:
        lines.append(f"| {check.check} | {check.status} | {check.detail} |")
    return "\n".join(lines).strip() + "\n"


def _run_verification(ledger_file: Path) -> List[CheckResult]:
    checks: List[CheckResult] = []
    if ledger_file.exists():
        ledger_file.unlink()

    registry = FreedIDRegistry(audit_ledger_path=str(ledger_file))
    did = registry.register(
        DIDDocument(
            did="",
            controller="did:freed:controller",
            verification_methods=[{"id": "key-1", "type": "Ed25519", "publicKeyBase58": "GfH2..."}],
            services=[],
        )
    )
    checks.append(CheckResult("register_did", "PASS", f"registered {did}"))

    registry.issue_credential(did, {"claim": "baseline", "issuer": "did:freed:issuer"})
    checks.append(CheckResult("issue_credential", "PASS", "credential issued"))

    resolved = registry.resolve(did)
    if resolved is None:
        checks.append(CheckResult("resolve_for_update", "FAIL", "unable to resolve did for update"))
        return checks
    resolved.services.append({"id": f"{did}#svc-1", "type": "ExampleService", "serviceEndpoint": "https://example"})
    registry.update(did, resolved)
    checks.append(CheckResult("update_did", "PASS", "did update recorded"))

    registry.revoke(did)
    checks.append(CheckResult("revoke_did", "PASS", "did revoked"))

    if not ledger_file.exists():
        checks.append(CheckResult("ledger_exists", "FAIL", "audit ledger was not created"))
        return checks
    checks.append(CheckResult("ledger_exists", "PASS", f"ledger file present: {ledger_file}"))

    ledger = FreedIDAuditLedger(ledger_file)
    entries = list(ledger.iter_entries())
    if len(entries) < 4:
        checks.append(CheckResult("ledger_entry_count", "FAIL", f"expected >= 4 entries, found {len(entries)}"))
    else:
        checks.append(CheckResult("ledger_entry_count", "PASS", f"entries={len(entries)}"))

    expected_actions = ["register", "issue_credential", "update", "revoke"]
    observed_actions = [str(entry.get("action")) for entry in entries[:4]]
    if observed_actions == expected_actions:
        checks.append(CheckResult("action_sequence", "PASS", ",".join(observed_actions)))
    else:
        checks.append(
            CheckResult(
                "action_sequence",
                "FAIL",
                f"expected={expected_actions}; observed={observed_actions}",
            )
        )

    chain_ok, chain_detail = ledger.verify_integrity()
    checks.append(CheckResult("hash_chain_integrity", "PASS" if chain_ok else "FAIL", chain_detail))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Freed ID GOV-003 auditability verification.")
    parser.add_argument("--reports-dir", default="docs/heart-track-runs", help="Directory for timestamped artifacts.")
    parser.add_argument(
        "--ledger-file",
        default="docs/freed-id-audit-log.jsonl",
        help="Append-only audit ledger file written by the registry.",
    )
    parser.add_argument(
        "--latest-json",
        default="docs/heart-track-auditability-latest.json",
        help="Path for latest JSON result.",
    )
    parser.add_argument(
        "--latest-md",
        default="docs/heart-track-auditability-latest.md",
        help="Path for latest markdown result.",
    )
    args = parser.parse_args()

    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    ledger_path = Path(args.ledger_file)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    checks = _run_verification(ledger_path)
    overall_status = "PASS" if all(check.status == "PASS" for check in checks) else "FAIL"

    payload = {
        "generated_utc": generated_utc,
        "control_id": "GOV-003",
        "overall_status": overall_status,
        "ledger_file": str(ledger_path),
        "checks": [asdict(check) for check in checks],
    }
    markdown = _build_markdown(generated_utc, overall_status, str(ledger_path), checks)

    timestamped_json = reports_dir / f"{stamp}-freedid-auditability-check.json"
    timestamped_md = reports_dir / f"{stamp}-freedid-auditability-check.md"
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
    print(f"ledger_file={ledger_path}")
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
