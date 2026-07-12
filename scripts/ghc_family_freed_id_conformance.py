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

V2_REQUIRED_PROFILE_FIELDS = {
    "pinned_vc_context",
    "pinned_vc_recommendation",
    "pinned_did_recommendation",
    "proof_boundary",
    "status_boundary",
    "synthetic_data_only",
}

V2_REQUIRED_PROOF_FIELDS = {
    "type",
    "cryptosuite",
    "created",
    "verificationMethod",
    "proofPurpose",
    "proofValue",
}

V2_REQUIRED_STATUS_FIELDS = {
    "id",
    "type",
    "statusPurpose",
    "statusListIndex",
    "statusListCredential",
}

V3_REQUIRED_PROFILE_FIELDS = {
    "allowed_contexts",
    "status_freshness_policy",
    "proof_verification_boundary",
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
    if profile.get("profile_version") == "2":
        missing = sorted(field for field in V2_REQUIRED_PROFILE_FIELDS if not profile.get(field))
        if missing:
            issues.append("v2_profile_fields_missing:" + ",".join(missing))
        if profile.get("pinned_vc_context") != VC_CONTEXT:
            issues.append("v2_vc_context_not_pinned")
        if profile.get("synthetic_data_only") is not True:
            issues.append("v2_real_data_boundary_missing")
    if profile.get("profile_revision") == "3":
        missing = sorted(field for field in V3_REQUIRED_PROFILE_FIELDS if not profile.get(field))
        if missing:
            issues.append("v3_profile_fields_missing:" + ",".join(missing))
        if VC_CONTEXT not in profile.get("allowed_contexts", []):
            issues.append("v3_vc_context_not_allowed")
        policy = profile.get("status_freshness_policy", {})
        if not isinstance(policy.get("maximum_age_seconds"), int) or policy.get(
            "maximum_age_seconds", 0
        ) <= 0:
            issues.append("v3_status_freshness_policy_invalid")
        if profile.get("proof_verification_boundary") != "shape_only_no_crypto_performed":
            issues.append("v3_proof_verification_boundary_missing")
    return issues


def validate_credential(
    credential: dict[str, Any], *, profile: dict[str, Any] | None = None
) -> list[str]:
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
    if profile and profile.get("profile_version") == "2":
        if not isinstance(credential.get("validFrom"), str):
            issues.append("valid_from_missing")
        if not isinstance(credential.get("validUntil"), str):
            issues.append("valid_until_missing")

        status = credential.get("credentialStatus")
        if not isinstance(status, dict):
            issues.append("credential_status_missing")
        else:
            missing_status = sorted(
                field for field in V2_REQUIRED_STATUS_FIELDS if not status.get(field)
            )
            if missing_status:
                issues.append("credential_status_fields_missing:" + ",".join(missing_status))
            if status.get("type") != "BitstringStatusListEntry":
                issues.append("credential_status_type_invalid")
            if status.get("statusPurpose") not in {"revocation", "suspension"}:
                issues.append("credential_status_purpose_invalid")

        proof = credential.get("proof")
        if not isinstance(proof, dict):
            issues.append("proof_shape_missing")
        else:
            missing_proof = sorted(
                field for field in V2_REQUIRED_PROOF_FIELDS if not proof.get(field)
            )
            if missing_proof:
                issues.append("proof_fields_missing:" + ",".join(missing_proof))

        holder = credential.get("holder")
        controller = credential.get("controller")
        if not isinstance(holder, str) or not isinstance(controller, str):
            issues.append("holder_controller_roles_missing")
        elif holder == controller:
            issues.append("holder_controller_separation_violated")
    if profile and profile.get("profile_revision") == "3":
        allowed_contexts = set(profile.get("allowed_contexts", []))
        if not isinstance(context, list) or any(item not in allowed_contexts for item in context):
            issues.append("unapproved_context")
        maximum_age = profile.get("status_freshness_policy", {}).get(
            "maximum_age_seconds"
        )
        age = credential.get("statusAgeSeconds")
        if not isinstance(age, (int, float)) or isinstance(age, bool) or age < 0:
            issues.append("status_age_missing_or_invalid")
        elif isinstance(maximum_age, int) and age > maximum_age:
            issues.append("status_stale")
        proof_status = credential.get("proofVerificationStatus")
        if proof_status != "not_performed":
            issues.append("unverified_proof_misrepresented")
    return issues


def run_vectors(profile: dict[str, Any], vectors: list[dict[str, Any]]) -> dict[str, Any]:
    profile_issues = validate_profile(profile)
    results = []
    for vector in vectors:
        issues = validate_credential(vector["credential"], profile=profile)
        accepted = not issues and not profile_issues
        expected = bool(vector["expect_accept"])
        expected_issue_codes = vector.get("expected_issue_codes")
        issue_codes_matched = (
            True
            if expected_issue_codes is None
            else set(expected_issue_codes) == set(issues)
        )
        results.append(
            {
                "vector_id": vector["vector_id"],
                "expected_accept": expected,
                "actual_accept": accepted,
                "matched": expected == accepted and issue_codes_matched,
                "issue_codes_matched": issue_codes_matched,
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
        "boundary": "structural_profile_only_no_signature_verification_no_did_resolution_no_trust_decision_no_deployment_no_personhood_or_legal_status",
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
