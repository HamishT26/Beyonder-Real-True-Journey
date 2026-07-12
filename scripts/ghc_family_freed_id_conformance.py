#!/usr/bin/env python3
"""Run structural Freed ID minimum-profile conformance vectors.

The validator checks a bounded project profile layered over W3C VC concepts.
It performs no signature verification, DID resolution, assurance decision, or
legal/personhood determination.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


VC_CONTEXT = "https://www.w3.org/ns/credentials/v2"
REQUIRED_CAPABILITIES = {
    "status_or_revocation",
    "recovery",
    "delegation",
    "selective_disclosure",
    "export",
    "deletion_or_tombstone",
    "appeal",
}


def validate_profile(profile: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    roles = set(profile.get("roles", []))
    if not {"issuer", "holder", "subject", "verifier"}.issubset(roles):
        issues.append("roles_incomplete")
    capabilities = set(profile.get("capabilities", []))
    if not REQUIRED_CAPABILITIES.issubset(capabilities):
        issues.append("capabilities_incomplete")
    if profile.get("controller_holder_separation") != "required_and_explicit":
        issues.append("controller_holder_separation_missing")
    boundary = profile.get("personhood_boundary", "")
    if boundary != "credentials_do_not_prove_consciousness_or_legal_personhood":
        issues.append("personhood_boundary_missing")
    return issues


def validate_credential(credential: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    context = credential.get("@context", [])
    types = credential.get("type", [])
    if VC_CONTEXT not in context:
        issues.append("vc_v2_context_missing")
    if "VerifiableCredential" not in types:
        issues.append("vc_type_missing")
    if not isinstance(credential.get("issuer"), str):
        issues.append("issuer_missing")
    subject = credential.get("credentialSubject")
    if not isinstance(subject, dict) or not subject.get("id"):
        issues.append("credential_subject_missing")
    if credential.get("claimsConsciousness") is True:
        issues.append("prohibited_consciousness_inference")
    if credential.get("claimsLegalPersonhood") is True:
        issues.append("prohibited_legal_personhood_inference")
    return issues


def run_vectors(profile: dict[str, Any], vectors: list[dict[str, Any]]) -> dict[str, Any]:
    profile_issues = validate_profile(profile)
    results = []
    for vector in vectors:
        issues = validate_credential(vector["credential"])
        accepted = not issues and not profile_issues
        expected = bool(vector["expect_accept"])
        results.append(
            {
                "vector_id": vector["vector_id"],
                "expected_accept": expected,
                "actual_accept": accepted,
                "matched": expected == accepted,
                "issues": issues,
            }
        )
    return {
        "schema": "ghc.family.freed-id-conformance-report.v1",
        "profile_valid": not profile_issues,
        "profile_issues": profile_issues,
        "vector_count": len(results),
        "matched_count": sum(row["matched"] for row in results),
        "all_matched": all(row["matched"] for row in results),
        "results": results,
        "boundary": "structural_profile_only_no_crypto_no_did_resolution_no_personhood_or_legal_status",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    parser.add_argument("vectors", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    vectors_payload = json.loads(args.vectors.read_text(encoding="utf-8"))
    report = run_vectors(profile, vectors_payload["vectors"])
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["profile_valid"] and report["all_matched"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
