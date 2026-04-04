#!/usr/bin/env python3
"""Bootstrap V32 GCP auth, service checks, and bounded foundation resources."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from trinity_v32_runtime_common import (
    ARTIFACT_REPOSITORY,
    DEFAULT_GCP_KEY_BUNDLE,
    DEFAULT_SECRET_IDS,
    PRIMARY_REGION,
    PROJECT_ID,
    google_request,
    load_gcp_service_accounts,
    mask_email,
    mint_access_token,
    now_iso,
    windows_kubectl,
    write_json,
    write_text,
    wsl_probe,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_JSON = ROOT / "docs" / "trinity-live-traces" / "v32-gcp-bootstrap-proof-v1.json"
OUTPUT_MD = ROOT / "docs" / "trinity-live-traces" / "v32-gcp-bootstrap-proof-v1.md"
SERVICE_NAMES = [
    "container.googleapis.com",
    "artifactregistry.googleapis.com",
    "secretmanager.googleapis.com",
    "storage.googleapis.com",
]
CUSTOM_PARITY_ROLES = [
    "roles/browser",
    "roles/storage.admin",
    "roles/container.admin",
    "roles/artifactregistry.admin",
    "roles/secretmanager.admin",
    "roles/serviceusage.serviceUsageAdmin",
]


def service_url(project_id: str, service_name: str) -> str:
    return f"https://serviceusage.googleapis.com/v1/projects/{project_id}/services/{service_name}"


def ensure_service_enabled(project_id: str, token: str, service_name: str, enable: bool) -> dict[str, Any]:
    initial = google_request("GET", service_url(project_id, service_name), token)
    initial_state = str(initial.get("parsed", {}).get("state", "UNKNOWN"))
    enable_attempted = False
    enable_status = None
    final = initial
    if enable and initial_state != "ENABLED":
        enable_attempted = True
        enabled = google_request(
            "POST",
            f"{service_url(project_id, service_name)}:enable",
            token,
            body={},
        )
        enable_status = enabled["status"]
        final = google_request("GET", service_url(project_id, service_name), token)
    return {
        "service_name": service_name,
        "initial_status": initial["status"],
        "initial_state": initial_state,
        "enable_attempted": enable_attempted,
        "enable_status": enable_status,
        "final_status": final["status"],
        "final_state": str(final.get("parsed", {}).get("state", "UNKNOWN")),
    }


def get_project(project_id: str, token: str) -> dict[str, Any]:
    return google_request(
        "GET",
        f"https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}",
        token,
    )


def get_gke_inventory(project_id: str, token: str) -> dict[str, Any]:
    return google_request(
        "GET",
        f"https://container.googleapis.com/v1/projects/{project_id}/locations/-/clusters",
        token,
    )


def get_server_config(project_id: str, token: str, region: str) -> dict[str, Any]:
    return google_request(
        "GET",
        f"https://container.googleapis.com/v1/projects/{project_id}/locations/{region}/serverConfig",
        token,
    )


def get_iam_policy(project_id: str, token: str) -> dict[str, Any]:
    return google_request(
        "POST",
        f"https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}:getIamPolicy",
        token,
        body={},
    )


def set_iam_policy(project_id: str, token: str, policy: dict[str, Any]) -> dict[str, Any]:
    return google_request(
        "POST",
        f"https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}:setIamPolicy",
        token,
        body={"policy": policy},
    )


def add_member_to_roles(policy: dict[str, Any], member: str, roles: list[str]) -> list[str]:
    bindings = policy.setdefault("bindings", [])
    changed: list[str] = []
    for role in roles:
        binding = next((row for row in bindings if row.get("role") == role), None)
        if binding is None:
            binding = {"role": role, "members": [member]}
            bindings.append(binding)
            changed.append(role)
            continue
        members = binding.setdefault("members", [])
        if member not in members:
            members.append(member)
            changed.append(role)
    return changed


def ensure_secret(project_id: str, token: str, secret_id: str) -> dict[str, Any]:
    url = f"https://secretmanager.googleapis.com/v1/projects/{project_id}/secrets/{secret_id}"
    probe = google_request("GET", url, token)
    if probe["status"] == 200:
        return {"secret_id": secret_id, "status": "exists", "http_status": 200}
    create = google_request(
        "POST",
        f"https://secretmanager.googleapis.com/v1/projects/{project_id}/secrets?secretId={secret_id}",
        token,
        body={
            "replication": {"automatic": {}},
            "labels": {"phase": "v32omega", "managed_by": "codex"},
        },
    )
    created = create["status"] in {200, 201}
    return {
        "secret_id": secret_id,
        "status": "created" if created else "blocked",
        "http_status": create["status"],
        "error": create.get("parsed", {}),
    }


def ensure_artifact_repository(project_id: str, token: str, region: str, repository_id: str) -> dict[str, Any]:
    url = (
        "https://artifactregistry.googleapis.com/v1/"
        f"projects/{project_id}/locations/{region}/repositories/{repository_id}"
    )
    probe = google_request("GET", url, token)
    if probe["status"] == 200:
        return {"repository_id": repository_id, "status": "exists", "http_status": 200}
    create = google_request(
        "POST",
        "https://artifactregistry.googleapis.com/v1/"
        f"projects/{project_id}/locations/{region}/repositories?repositoryId={repository_id}",
        token,
        body={
            "format": "DOCKER",
            "description": "V32 Omega bounded container lane.",
            "labels": {"phase": "v32omega", "managed_by": "codex"},
        },
    )
    created = create["status"] in {200, 201}
    return {
        "repository_id": repository_id,
        "status": "created" if created else "blocked",
        "http_status": create["status"],
        "error": create.get("parsed", {}),
    }


def write_outputs(payload: dict[str, Any]) -> None:
    write_json(OUTPUT_JSON, payload)
    lines = [
        "# V32 GCP Bootstrap Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- Proof state: `{payload['proof_state']}`",
        f"- Project: `{payload['project_id']}`",
        f"- Primary identity: `{payload.get('gcp_primary_identity', 'unknown')}`",
        f"- Custom identity state: `{payload.get('gcp_custom_identity_state', 'unknown')}`",
        f"- Gcloud CLI state: `{payload.get('gcloud_cli_state', 'unknown')}`",
        f"- Kubectl fallback: `{payload.get('kubectl_client_path', '') or 'missing'}`",
        "",
        "## Completed Steps",
        "",
    ]
    for step in payload.get("completed_steps", []):
        lines.append(f"- `{step}`")
    if payload.get("pending_steps"):
        lines.extend(["", "## Pending Steps", ""])
        for step in payload["pending_steps"]:
            lines.append(f"- `{step}`")
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        for blocker in payload["blockers"]:
            lines.append(f"- {blocker}")
    write_text(OUTPUT_MD, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap V32 GCP auth and foundation resources.")
    parser.add_argument("--bundle", default=str(DEFAULT_GCP_KEY_BUNDLE))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--region", default=PRIMARY_REGION)
    parser.add_argument("--create-foundation", action="store_true")
    parser.add_argument("--repair-custom-identity", action="store_true")
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v32_omega",
        "overall_status": "WARN",
        "proof_state": "pending",
        "project_id": args.project_id,
        "region": args.region,
        "attempted_steps": [
            "parse_service_account_bundle",
            "mint_tokens",
            "project_resolution",
            "service_enablement_checks",
            "gke_inventory",
            "region_server_config",
            "wsl_operator_probe",
            "custom_identity_parity",
            "secret_manager_bootstrap",
            "artifact_registry_bootstrap",
        ],
        "completed_steps": [],
        "pending_steps": [
            "parse_service_account_bundle",
            "mint_tokens",
            "project_resolution",
            "service_enablement_checks",
            "gke_inventory",
            "region_server_config",
            "wsl_operator_probe",
            "custom_identity_parity",
            "secret_manager_bootstrap",
            "artifact_registry_bootstrap",
        ],
        "blockers": [],
        "identities": [],
        "service_checks": [],
        "secret_manager_results": [],
        "artifact_registry_result": {},
    }

    bundle = load_gcp_service_accounts(Path(args.bundle))
    records = bundle["records"]
    payload["bundle_path"] = bundle["bundle_path"]
    payload["runtime_dir"] = bundle["runtime_dir"]
    if not records:
        payload["proof_state"] = "missing_gcp_service_accounts"
        payload["blockers"].append("No service-account JSON objects were parsed from the external GCP key bundle.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("parse_service_account_bundle")
    payload["pending_steps"].remove("parse_service_account_bundle")

    alias_map = {row["alias"]: row for row in records}
    token_map: dict[str, dict[str, Any]] = {}
    for row in records:
        try:
            minted = mint_access_token(row["info"])
            token_map[row["alias"]] = minted
            payload["identities"].append(
                {
                    "alias": row["alias"],
                    "client_email_masked": mask_email(row["client_email"]),
                    "project_id": row["project_id"],
                    "token_minted": True,
                    "expiry_utc": minted["expiry_utc"],
                }
            )
        except Exception as exc:  # pragma: no cover - network/auth handling
            payload["identities"].append(
                {
                    "alias": row["alias"],
                    "client_email_masked": mask_email(row["client_email"]),
                    "project_id": row["project_id"],
                    "token_minted": False,
                    "error": str(exc),
                }
            )
    if not token_map:
        payload["proof_state"] = "token_mint_failed"
        payload["blockers"].append("None of the parsed service accounts minted a usable cloud-platform token.")
        write_outputs(payload)
        return 1
    payload["completed_steps"].append("mint_tokens")
    payload["pending_steps"].remove("mint_tokens")

    primary_alias = "compute_default" if "compute_default" in token_map else "app_engine_default"
    if primary_alias not in token_map:
        primary_alias = sorted(token_map.keys())[0]
    primary_token = token_map[primary_alias]["token"]
    payload["gcp_primary_identity"] = primary_alias

    project = get_project(args.project_id, primary_token)
    payload["project_resolution"] = {
        "status": project["status"],
        "project_name": project.get("parsed", {}).get("name", ""),
        "lifecycle_state": project.get("parsed", {}).get("lifecycleState", ""),
    }
    if project["status"] == 200:
        payload["completed_steps"].append("project_resolution")
        payload["pending_steps"].remove("project_resolution")
        payload["gcp_project_state"] = "resolved"
    else:
        payload["gcp_project_state"] = "blocked"
        payload["blockers"].append(f"Primary identity failed project resolution with HTTP {project['status']}.")

    for service_name in SERVICE_NAMES:
        check = ensure_service_enabled(args.project_id, primary_token, service_name, args.create_foundation)
        payload["service_checks"].append(check)
    if all(row["final_status"] == 200 for row in payload["service_checks"]):
        payload["completed_steps"].append("service_enablement_checks")
        payload["pending_steps"].remove("service_enablement_checks")

    inventory = get_gke_inventory(args.project_id, primary_token)
    clusters = inventory.get("parsed", {}).get("clusters", []) if inventory["status"] == 200 else []
    payload["gke_inventory"] = {
        "status": inventory["status"],
        "cluster_names": [row.get("name", "") for row in clusters if isinstance(row, dict)],
        "cluster_count": len(clusters),
    }
    if inventory["status"] == 200:
        payload["completed_steps"].append("gke_inventory")
        payload["pending_steps"].remove("gke_inventory")
        payload["gke_api_state"] = "inventory_readable"
    else:
        payload["gke_api_state"] = "inventory_blocked"
        payload["blockers"].append(f"GKE inventory probe failed with HTTP {inventory['status']}.")

    server_config = get_server_config(args.project_id, primary_token, args.region)
    payload["server_config"] = {
        "status": server_config["status"],
        "valid_master_versions": server_config.get("parsed", {}).get("validMasterVersions", []),
        "default_cluster_version": server_config.get("parsed", {}).get("defaultClusterVersion", ""),
    }
    if server_config["status"] == 200:
        payload["completed_steps"].append("region_server_config")
        payload["pending_steps"].remove("region_server_config")

    wsl = wsl_probe()
    payload["wsl_probe"] = wsl
    payload["kubectl_client_path"] = windows_kubectl()
    if wsl["readiness"] == "ubuntu_shell_ready":
        payload["gcloud_cli_state"] = "wsl_shell_reachable_gcloud_not_yet_installed"
    elif wsl["readiness"] == "ubuntu_launch_timeout":
        payload["gcloud_cli_state"] = "blocked_wsl_launch_timeout"
        payload["blockers"].append("WSL Ubuntu launch is timing out, so the preferred gcloud install lane is not yet healthy.")
    else:
        payload["gcloud_cli_state"] = "blocked_wsl_launch_failed"
        payload["blockers"].append("WSL Ubuntu did not provide a clean shell for the preferred gcloud install lane.")
    payload["completed_steps"].append("wsl_operator_probe")
    payload["pending_steps"].remove("wsl_operator_probe")

    custom_alias = "beyonder_real_journey_1"
    custom_state = "not_present"
    if custom_alias in token_map:
        custom_token = token_map[custom_alias]["token"]
        custom_project = get_project(args.project_id, custom_token)
        custom_gke = get_gke_inventory(args.project_id, custom_token)
        custom_state = "parity_confirmed" if custom_project["status"] == 200 and custom_gke["status"] == 200 else "blocked"
        repair_attempt = {
            "project_status": custom_project["status"],
            "gke_inventory_status": custom_gke["status"],
            "roles_added": [],
            "set_policy_status": None,
        }
        if custom_state == "blocked" and args.repair_custom_identity:
            iam = get_iam_policy(args.project_id, primary_token)
            if iam["status"] == 200:
                member = f"serviceAccount:{alias_map[custom_alias]['client_email']}"
                policy = iam.get("parsed", {}).get("bindings") and iam["parsed"] or {}
                roles_added = add_member_to_roles(policy, member, CUSTOM_PARITY_ROLES)
                repair_attempt["roles_added"] = roles_added
                if roles_added:
                    set_policy = set_iam_policy(args.project_id, primary_token, policy)
                    repair_attempt["set_policy_status"] = set_policy["status"]
                    if set_policy["status"] == 200:
                        custom_project = get_project(args.project_id, custom_token)
                        custom_gke = get_gke_inventory(args.project_id, custom_token)
                        custom_state = "parity_confirmed" if custom_project["status"] == 200 and custom_gke["status"] == 200 else "blocked_after_repair"
                    else:
                        custom_state = "repair_failed"
                else:
                    custom_state = "blocked_no_role_delta"
            else:
                custom_state = "repair_policy_read_blocked"
                repair_attempt["set_policy_status"] = iam["status"]
        payload["custom_identity_probe"] = repair_attempt
        if custom_state.startswith("blocked"):
            payload["blockers"].append(
                "Custom service account beyonder-real-journey-1 remains below parity for project/GKE reads."
            )
    payload["gcp_custom_identity_state"] = custom_state
    payload["completed_steps"].append("custom_identity_parity")
    payload["pending_steps"].remove("custom_identity_parity")

    if args.create_foundation and payload.get("gcp_project_state") == "resolved":
        for secret_id in DEFAULT_SECRET_IDS:
            payload["secret_manager_results"].append(ensure_secret(args.project_id, primary_token, secret_id))
        payload["artifact_registry_result"] = ensure_artifact_repository(
            args.project_id,
            primary_token,
            args.region,
            ARTIFACT_REPOSITORY,
        )
    else:
        payload["secret_manager_results"] = [
            {"secret_id": secret_id, "status": "skipped"} for secret_id in DEFAULT_SECRET_IDS
        ]
        payload["artifact_registry_result"] = {"repository_id": ARTIFACT_REPOSITORY, "status": "skipped"}
    payload["secret_manager_state"] = (
        "ready"
        if all(row.get("status") in {"created", "exists"} for row in payload["secret_manager_results"])
        else "blocked"
    )
    payload["artifact_registry_state"] = (
        "ready" if payload["artifact_registry_result"].get("status") in {"created", "exists"} else "blocked"
    )
    payload["completed_steps"].append("secret_manager_bootstrap")
    payload["completed_steps"].append("artifact_registry_bootstrap")
    payload["pending_steps"].remove("secret_manager_bootstrap")
    payload["pending_steps"].remove("artifact_registry_bootstrap")

    blocking_states = {
        payload.get("gcp_project_state"),
        payload.get("gke_api_state"),
        payload.get("secret_manager_state"),
        payload.get("artifact_registry_state"),
    }
    if "resolved" in blocking_states or "inventory_readable" in blocking_states:
        pass
    if (
        payload.get("gcp_project_state") == "resolved"
        and payload.get("gke_api_state") == "inventory_readable"
        and payload.get("secret_manager_state") == "ready"
        and payload.get("artifact_registry_state") == "ready"
    ):
        payload["overall_status"] = "PASS"
        payload["proof_state"] = "foundation_ready"
    elif payload.get("gcp_project_state") == "resolved" and payload.get("gke_api_state") == "inventory_readable":
        payload["overall_status"] = "WARN"
        payload["proof_state"] = "bootstrap_ready_with_foundation_blockers"
    else:
        payload["overall_status"] = "WARN"
        payload["proof_state"] = "bootstrap_blocked"

    write_outputs(payload)
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
