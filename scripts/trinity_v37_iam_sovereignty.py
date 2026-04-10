#!/usr/bin/env python3
"""Inventory and apply the bounded V37 project-scoped IAM/API sovereignty wave."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from trinity_v32_gcp_bootstrap import add_member_to_roles
from trinity_v32_runtime_common import google_request, PROJECT_ID
from trinity_v36_cloud_common import ensure_service_enabled, load_primary_service_account, now_iso, write_json, write_text

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON = ROOT / "docs" / "trinity-live-traces" / "v37-iam-sovereignty-proof-v1.json"
DEFAULT_MD = ROOT / "docs" / "trinity-live-traces" / "v37-iam-sovereignty-proof-v1.md"
FALLBACK_PROPOSAL_DIGEST = ROOT / "docs" / "trinity-live-traces" / "v37-proposal-digest-v1.json"
DEFAULT_PRINCIPALS = [
    "649817769181-compute@developer.gserviceaccount.com",
    "Hamisht26@gmail.com",
    "gen-lang-client-0020882673@appspot.gserviceaccount.com",
    "beyonder-real-journey-1@gen-lang-client-0020882673.iam.gserviceaccount.com",
]
SEEDED_SERVICE_NAMES = {
    "aiplatform.googleapis.com",
    "admin.googleapis.com",
    "apikeys.googleapis.com",
    "artifactregistry.googleapis.com",
    "automl.googleapis.com",
    "bigtable.googleapis.com",
    "bigtableadmin.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "compute.googleapis.com",
    "container.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "run.googleapis.com",
    "secretmanager.googleapis.com",
    "servicemanagement.googleapis.com",
    "serviceusage.googleapis.com",
    "sqladmin.googleapis.com",
    "storage.googleapis.com",
}
SERVICE_KEYWORDS = (
    "ai",
    "agent",
    "apikey",
    "api key",
    "api",
    "artifact",
    "automl",
    "bigquery",
    "bigtable",
    "cloud sql",
    "compute",
    "container",
    "dialogflow",
    "discovery",
    "iam",
    "language",
    "resource manager",
    "run",
    "security",
    "service",
    "speech",
    "sql",
    "storage",
    "translate",
    "vertex",
    "vision",
)


def write_outputs(payload: dict[str, Any], output_json: Path, output_md: Path) -> None:
    write_json(output_json, payload)
    lines = [
        "# V37 IAM Sovereignty Proof",
        "",
        f"- Generated UTC: `{payload['generated_utc']}`",
        f"- Apply mode: `{payload['apply_mode']}`",
        f"- Overall status: `{payload['overall_status']}`",
        f"- IAM state: `{payload.get('iam_state', 'unknown')}`",
        f"- API state: `{payload.get('api_state', 'unknown')}`",
        f"- Requested grantable roles: `{payload.get('requested_grantable_role_count', 0)}`",
        f"- Eligible roles: `{payload.get('eligible_role_count', 0)}`",
        f"- Applied role bindings: `{payload.get('applied_role_binding_count', 0)}`",
        f"- Candidate services: `{payload.get('candidate_service_count', 0)}`",
        f"- Enabled services: `{payload.get('enabled_service_count', 0)}`",
        "",
        "## Principals",
        "",
    ]
    lines.extend([f"- `{row}`" for row in payload.get("principals", [])])
    if payload.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        lines.extend([f"- {row}" for row in payload["blockers"]])
    write_text(output_md, "\n".join(lines) + "\n")


def parse_principals(values: list[str] | None) -> list[str]:
    raw = values or []
    parsed: list[str] = []
    for value in raw:
        for part in str(value or "").split(","):
            item = part.strip()
            if item and item not in parsed:
                parsed.append(item)
    return parsed or list(DEFAULT_PRINCIPALS)


def member_for_principal(principal: str) -> str:
    principal = str(principal or "").strip()
    if principal.endswith(".gserviceaccount.com"):
        return f"serviceAccount:{principal}"
    return f"user:{principal}"


def deep_copy_policy(policy: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(policy))


def project_info(project_id: str, token: str) -> dict[str, Any]:
    return google_request("GET", f"https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}", token, timeout=120)


def get_iam_policy(project_id: str, token: str) -> dict[str, Any]:
    return google_request(
        "POST",
        f"https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}:getIamPolicy",
        token,
        body={},
        timeout=120,
    )


def set_iam_policy(project_id: str, token: str, policy: dict[str, Any]) -> dict[str, Any]:
    return google_request(
        "POST",
        f"https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}:setIamPolicy",
        token,
        body={"policy": policy},
        timeout=240,
    )


def query_grantable_roles(project_number: str, token: str) -> dict[str, Any]:
    roles: list[dict[str, Any]] = []
    page_token = ""
    raw_pages: list[dict[str, Any]] = []
    while True:
        body: dict[str, Any] = {
            "fullResourceName": f"//cloudresourcemanager.googleapis.com/projects/{project_number}",
            "pageSize": 1000,
            "view": "FULL",
        }
        if page_token:
            body["pageToken"] = page_token
        response = google_request("POST", "https://iam.googleapis.com/v1/roles:queryGrantableRoles", token, body=body, timeout=240)
        raw_pages.append({"status": response["status"], "body_excerpt": response.get("body_text", "")[:1200]})
        if response["status"] != 200:
            return {"status": response["status"], "roles": [], "raw_pages": raw_pages}
        parsed = response.get("parsed", {})
        page_roles = parsed.get("roles", []) if isinstance(parsed, dict) else []
        if isinstance(page_roles, list):
            roles.extend([row for row in page_roles if isinstance(row, dict)])
        page_token = str(parsed.get("nextPageToken") or "") if isinstance(parsed, dict) else ""
        if not page_token:
            break
    return {"status": 200, "roles": roles, "raw_pages": raw_pages}


def list_public_roles(token: str) -> dict[str, Any]:
    roles: list[dict[str, Any]] = []
    page_token = ""
    raw_pages: list[dict[str, Any]] = []
    while True:
        suffix = f"&pageToken={page_token}" if page_token else ""
        response = google_request(
            "GET",
            f"https://iam.googleapis.com/v1/roles?pageSize=1000&view=FULL{suffix}",
            token,
            timeout=240,
        )
        raw_pages.append({"status": response["status"], "body_excerpt": response.get("body_text", "")[:1200]})
        if response["status"] != 200:
            return {"status": response["status"], "roles": [], "raw_pages": raw_pages}
        parsed = response.get("parsed", {})
        page_roles = parsed.get("roles", []) if isinstance(parsed, dict) else []
        if isinstance(page_roles, list):
            roles.extend([row for row in page_roles if isinstance(row, dict)])
        page_token = str(parsed.get("nextPageToken") or "") if isinstance(parsed, dict) else ""
        if not page_token:
            break
    return {"status": 200, "roles": roles, "raw_pages": raw_pages}


def load_proposal_titles() -> list[str]:
    if not FALLBACK_PROPOSAL_DIGEST.exists():
        return []
    try:
        payload = json.loads(FALLBACK_PROPOSAL_DIGEST.read_text(encoding="utf-8-sig"))
    except Exception:
        return []
    rows = payload.get("parsed_role_titles", []) if isinstance(payload, dict) else []
    titles: list[str] = []
    for row in rows if isinstance(rows, list) else []:
        title = str(row or "").strip()
        if title.startswith("- "):
            title = title[2:].strip()
        if title and title not in titles:
            titles.append(title)
    return titles


def service_inventory(project_id: str, token: str) -> dict[str, Any]:
    enabled: list[str] = []
    page_token = ""
    enabled_pages: list[dict[str, Any]] = []
    while True:
        suffix = f"&pageToken={page_token}" if page_token else ""
        response = google_request(
            "GET",
            f"https://serviceusage.googleapis.com/v1/projects/{project_id}/services?pageSize=200&filter=state:ENABLED{suffix}",
            token,
            timeout=240,
        )
        enabled_pages.append({"status": response["status"], "body_excerpt": response.get("body_text", "")[:1200]})
        if response["status"] != 200:
            return {"enabled_status": response["status"], "enabled": [], "available": [], "raw_pages": enabled_pages}
        parsed = response.get("parsed", {})
        for row in parsed.get("services", []) if isinstance(parsed, dict) else []:
            if not isinstance(row, dict):
                continue
            config = row.get("config", {}) if isinstance(row.get("config"), dict) else {}
            name = str(config.get("name") or row.get("name") or "")
            if name:
                enabled.append(name)
        page_token = str(parsed.get("nextPageToken") or "") if isinstance(parsed, dict) else ""
        if not page_token:
            break

    available: list[dict[str, str]] = []
    page_token = ""
    available_pages: list[dict[str, Any]] = []
    while True:
        suffix = f"&pageToken={page_token}" if page_token else ""
        response = google_request(
            "GET",
            f"https://servicemanagement.googleapis.com/v1/services?pageSize=200{suffix}",
            token,
            timeout=240,
        )
        available_pages.append({"status": response["status"], "body_excerpt": response.get("body_text", "")[:1200]})
        if response["status"] != 200:
            return {
                "enabled_status": 200,
                "enabled": sorted(set(enabled)),
                "available_status": response["status"],
                "available": [],
                "raw_pages": {"enabled": enabled_pages, "available": available_pages},
            }
        parsed = response.get("parsed", {})
        for row in parsed.get("services", []) if isinstance(parsed, dict) else []:
            if not isinstance(row, dict):
                continue
            name = str(row.get("serviceName") or row.get("name") or "")
            title = str(row.get("title") or "")
            if name.endswith(".googleapis.com"):
                available.append({"name": name, "title": title})
        page_token = str(parsed.get("nextPageToken") or "") if isinstance(parsed, dict) else ""
        if not page_token:
            break
    return {
        "enabled_status": 200,
        "available_status": 200,
        "enabled": sorted(set(enabled)),
        "available": available,
        "raw_pages": {"enabled": enabled_pages, "available": available_pages},
    }


def role_skip_reason(role: dict[str, Any]) -> str:
    name = str(role.get("name") or "")
    title = str(role.get("title") or "")
    description = str(role.get("description") or "")
    stage = str(role.get("stage") or role.get("launchStage") or "").upper()
    haystack = " ".join([name, title, description]).lower()
    if not name.startswith("roles/"):
        return "unsupported_name"
    if "service agent" in haystack or ".serviceagent" in name.lower() or name.lower().endswith("serviceagent"):
        return "service_agent_role_excluded"
    if stage in {"DEPRECATED", "DISABLED"}:
        return "deprecated_or_disabled"
    return ""


def candidate_services(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    selected: dict[str, dict[str, str]] = {}
    for row in rows:
        name = str(row.get("name") or "")
        title = str(row.get("title") or "")
        haystack = f"{name} {title}".lower()
        if name in SEEDED_SERVICE_NAMES or any(keyword in haystack for keyword in SERVICE_KEYWORDS):
            selected[name] = {"name": name, "title": title}
    for name in SEEDED_SERVICE_NAMES:
        selected.setdefault(name, {"name": name, "title": ""})
    return [selected[key] for key in sorted(selected)]


def resolve_fallback_roles(payload: dict[str, Any], token: str) -> list[dict[str, Any]]:
    public_inventory = list_public_roles(token)
    payload["public_role_inventory"] = {
        "status": public_inventory.get("status"),
        "page_count": len(public_inventory.get("raw_pages", [])),
    }
    if public_inventory.get("status") != 200:
        payload["blockers"].append("Public predefined-role inventory failed after grantable-role inventory was denied.")
        return []

    titles = load_proposal_titles()
    payload["fallback_requested_title_count"] = len(titles)
    payload["fallback_source"] = str(FALLBACK_PROPOSAL_DIGEST)
    by_title: dict[str, list[dict[str, Any]]] = {}
    for row in public_inventory.get("roles", []):
        title = str(row.get("title") or "").strip()
        if not title:
            continue
        by_title.setdefault(title.lower(), []).append(row)

    matched: list[dict[str, Any]] = []
    for title in titles:
        title_key = title.lower()
        matches = by_title.get(title_key, [])
        if not matches:
            payload["skipped_grants"].append(
                {
                    "role": "",
                    "reason": "requested_title_not_found_in_public_roles",
                    "title": title,
                    "stage": "",
                }
            )
            continue
        for row in matches:
            matched.append(row)
    return matched


def apply_role_batch(
    project_id: str,
    token: str,
    base_policy: dict[str, Any],
    principals: list[str],
    roles: list[str],
) -> dict[str, Any]:
    candidate_policy = deep_copy_policy(base_policy)
    changed_roles: set[str] = set()
    for principal in principals:
        member = member_for_principal(principal)
        changed_roles.update(add_member_to_roles(candidate_policy, member, roles))
    changed_list = sorted(changed_roles)
    if not changed_list:
        return {
            "ok": True,
            "status": 200,
            "changed_roles": [],
            "policy": candidate_policy,
            "body_excerpt": "",
        }
    response = set_iam_policy(project_id, token, candidate_policy)
    parsed = response.get("parsed", {}) if isinstance(response.get("parsed", {}), dict) else {}
    return {
        "ok": response["status"] == 200,
        "status": response["status"],
        "changed_roles": changed_list,
        "policy": parsed if parsed else candidate_policy,
        "body_excerpt": response.get("body_text", "")[:2000],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the bounded V37 project-scoped IAM/API sovereignty sweep.")
    parser.add_argument("--bundle", default=str(Path.home() / "GCP service account keys.txt"))
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--principal", action="append")
    parser.add_argument("--scope", default="project")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD))
    args = parser.parse_args()

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    principals = parse_principals(args.principal)
    payload: dict[str, Any] = {
        "generated_utc": now_iso(),
        "phase": "v37_omega",
        "apply_mode": "apply" if args.apply else "dry_run",
        "scope": args.scope,
        "project_id": args.project_id,
        "principals": principals,
        "overall_status": "WARN",
        "iam_state": "pending",
        "api_state": "pending",
        "blockers": [],
        "requested_grants": [],
        "applied_grants": [],
        "skipped_grants": [],
        "enabled_services": [],
        "rejected_services": [],
    }

    try:
        _records, primary, minted = load_primary_service_account(Path(args.bundle))
    except Exception as exc:
        payload["overall_status"] = "FAIL"
        payload["iam_state"] = "blocked_missing_identity"
        payload["api_state"] = "blocked_missing_identity"
        payload["blockers"].append(str(exc))
        write_outputs(payload, output_json, output_md)
        return 1

    token = minted["token"]
    payload["primary_identity"] = str(primary["client_email"])
    payload["service_account_path"] = str(primary["runtime_path"])

    project = project_info(args.project_id, token)
    payload["project_probe"] = {
        "status": project["status"],
        "body_excerpt": project.get("body_text", "")[:1200],
    }
    if project["status"] != 200:
        payload["overall_status"] = "FAIL"
        payload["iam_state"] = "blocked_project_resolution"
        payload["api_state"] = "blocked_project_resolution"
        payload["blockers"].append(f"Project resolution failed with HTTP {project['status']}.")
        write_outputs(payload, output_json, output_md)
        return 1

    project_parsed = project.get("parsed", {}) if isinstance(project.get("parsed", {}), dict) else {}
    project_number = str(project_parsed.get("projectNumber") or "")
    payload["project_number"] = project_number
    payload["completed_project_resolution"] = True

    role_inventory = query_grantable_roles(project_number, token)
    payload["grantable_role_inventory"] = {
        "status": role_inventory.get("status"),
        "page_count": len(role_inventory.get("raw_pages", [])),
    }
    payload["grantable_role_inventory"]["fallback_used"] = False
    if role_inventory.get("status") == 200:
        raw_roles = role_inventory.get("roles", [])
    else:
        payload["grantable_role_inventory"]["fallback_used"] = True
        payload["grantable_role_inventory"]["failure_body_excerpt"] = (
            role_inventory.get("raw_pages", [{}])[0].get("body_excerpt", "") if role_inventory.get("raw_pages") else ""
        )
        raw_roles = resolve_fallback_roles(payload, token)
        if not raw_roles:
            payload["overall_status"] = "FAIL"
            payload["iam_state"] = "blocked_grantable_role_inventory"
            payload["api_state"] = "unreached"
            payload["blockers"].append("Grantable-role inventory failed for the project scope.")
            write_outputs(payload, output_json, output_md)
            return 1

    payload["requested_grantable_role_count"] = len(raw_roles)
    eligible_roles: list[str] = []
    for row in raw_roles:
        name = str(row.get("name") or "")
        reason = role_skip_reason(row)
        if reason:
            payload["skipped_grants"].append(
                {
                    "role": name,
                    "reason": reason,
                    "title": str(row.get("title") or ""),
                    "stage": str(row.get("stage") or row.get("launchStage") or ""),
                }
            )
            continue
        eligible_roles.append(name)
    eligible_roles = sorted(set(eligible_roles))
    payload["eligible_role_count"] = len(eligible_roles)
    payload["requested_grants"] = [{"role": role, "principals": principals} for role in eligible_roles]

    policy_response = get_iam_policy(args.project_id, token)
    payload["policy_read_status"] = policy_response["status"]
    if policy_response["status"] != 200:
        payload["overall_status"] = "FAIL"
        payload["iam_state"] = "blocked_policy_read"
        payload["api_state"] = "unreached"
        payload["blockers"].append(f"Project IAM policy read failed with HTTP {policy_response['status']}.")
        write_outputs(payload, output_json, output_md)
        return 1

    current_policy = policy_response.get("parsed", {}) if isinstance(policy_response.get("parsed", {}), dict) else {}
    policy_copy = json.loads(json.dumps(current_policy))
    bindings_before = len(policy_copy.get("bindings", [])) if isinstance(policy_copy.get("bindings", []), list) else 0
    payload["policy_binding_count_before"] = bindings_before

    applied_roles: set[str] = set()
    for principal in principals:
        member = member_for_principal(principal)
        changed_roles = add_member_to_roles(policy_copy, member, eligible_roles)
        applied_roles.update(changed_roles)

    payload["planned_role_binding_count"] = len(applied_roles)
    payload["applied_role_binding_count"] = len(applied_roles) if args.apply else 0

    if args.apply and applied_roles:
        batch_result = apply_role_batch(args.project_id, token, current_policy, principals, eligible_roles)
        payload["policy_set_status"] = batch_result["status"]
        payload["policy_set_body_excerpt"] = batch_result.get("body_excerpt", "")
        if batch_result["ok"]:
            payload["iam_state"] = "maximal_project_scope_bindings_applied"
            payload["applied_grants"] = [{"role": role, "principals": principals} for role in sorted(batch_result["changed_roles"])]
            payload["applied_role_binding_count"] = len(batch_result["changed_roles"])
        else:
            payload["batch_apply_mode"] = "fallback_single_role_apply"
            working_policy = current_policy
            applied_bindings: list[str] = []
            for role in eligible_roles:
                single_result = apply_role_batch(args.project_id, token, working_policy, principals, [role])
                if single_result["ok"]:
                    if single_result["changed_roles"]:
                        applied_bindings.extend(single_result["changed_roles"])
                        working_policy = single_result["policy"]
                    continue
                payload["skipped_grants"].append(
                    {
                        "role": role,
                        "reason": "policy_update_failed",
                        "http_status": single_result["status"],
                        "title": "",
                        "stage": "",
                        "body_excerpt": single_result.get("body_excerpt", ""),
                    }
                )
            if applied_bindings:
                payload["iam_state"] = "partial_project_scope_bindings_applied"
                payload["applied_grants"] = [{"role": role, "principals": principals} for role in sorted(set(applied_bindings))]
                payload["applied_role_binding_count"] = len(sorted(set(applied_bindings)))
            else:
                payload["overall_status"] = "FAIL"
                payload["iam_state"] = "apply_failed"
                payload["api_state"] = "pending"
                payload["blockers"].append(
                    f"Project IAM policy update failed with HTTP {batch_result['status']} and no single-role fallback binding succeeded."
                )
    else:
        payload["iam_state"] = "grant_plan_generated"

    services = service_inventory(args.project_id, token)
    payload["service_inventory"] = {
        "enabled_status": services.get("enabled_status"),
        "available_status": services.get("available_status"),
    }
    available_services = candidate_services(services.get("available", []))
    payload["candidate_service_count"] = len(available_services)
    payload["candidate_services"] = available_services

    if args.apply:
        for row in available_services:
            state = ensure_service_enabled(args.project_id, token, row["name"])
            entry = {
                "service_name": row["name"],
                "title": row.get("title", ""),
                "initial_state": state.get("initial_state"),
                "final_state": state.get("final_state"),
                "final_status": state.get("final_status"),
                "enable_attempted": state.get("enable_attempted"),
            }
            if state.get("final_status") == 200 and state.get("final_state") == "ENABLED":
                payload["enabled_services"].append(entry)
            else:
                entry["reason"] = "enable_failed_or_unavailable"
                payload["rejected_services"].append(entry)
        payload["enabled_service_count"] = len(payload["enabled_services"])
        payload["rejected_service_count"] = len(payload["rejected_services"])
        if payload["rejected_services"]:
            payload["api_state"] = "partially_enabled_with_rejections"
        else:
            payload["api_state"] = "maximal_project_scope_enablement_applied"
    else:
        payload["enabled_service_count"] = 0
        payload["rejected_service_count"] = 0
        payload["api_state"] = "service_plan_generated"

    post_policy = get_iam_policy(args.project_id, token)
    payload["post_policy_status"] = post_policy["status"]
    if post_policy["status"] == 200:
        post_bindings = post_policy.get("parsed", {}).get("bindings", []) if isinstance(post_policy.get("parsed", {}), dict) else []
        payload["policy_binding_count_after"] = len(post_bindings) if isinstance(post_bindings, list) else 0
        member_roles: dict[str, list[str]] = {}
        for principal in principals:
            member = member_for_principal(principal)
            roles: list[str] = []
            for binding in post_bindings if isinstance(post_bindings, list) else []:
                if not isinstance(binding, dict):
                    continue
                members = binding.get("members", [])
                role = str(binding.get("role") or "")
                if isinstance(members, list) and member in members and role:
                    roles.append(role)
            member_roles[principal] = sorted(roles)
        payload["post_apply_principal_roles"] = member_roles

    if payload["overall_status"] != "FAIL":
        payload["overall_status"] = "PASS" if args.apply else "WARN"
    write_outputs(payload, output_json, output_md)
    return 0 if payload["overall_status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
