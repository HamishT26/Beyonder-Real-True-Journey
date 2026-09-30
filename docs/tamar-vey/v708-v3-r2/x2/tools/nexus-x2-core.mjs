import { canonicalJson, sha256Value } from "../../x1/tools/nexus-core.mjs";

const HEX40 = /^[0-9a-f]{40}$/i;
const HEX64 = /^[0-9a-f]{64}$/i;

export function verifySourceBinding({ capsule, expected, payload }) {
  const errors = [];
  if (!capsule || typeof capsule !== "object") errors.push("capsule_missing");
  if (!expected || typeof expected !== "object")
    errors.push("expectation_missing");
  if (!payload || typeof payload !== "object") errors.push("payload_missing");
  if (errors.length) return { ok: false, errors };

  if (!HEX40.test(expected.source_commit ?? ""))
    errors.push("expected_commit_shape");
  if (!HEX64.test(expected.source_manifest_sha256 ?? "")) {
    errors.push("expected_manifest_shape");
  }
  if (!HEX64.test(expected.payload_sha256 ?? ""))
    errors.push("expected_payload_shape");
  if (capsule.source_commit !== expected.source_commit)
    errors.push("source_commit_mismatch");
  if (capsule.source_manifest_sha256 !== expected.source_manifest_sha256) {
    errors.push("source_manifest_mismatch");
  }
  if (sha256Value(payload) !== expected.payload_sha256)
    errors.push("payload_digest_mismatch");

  return {
    ok: errors.length === 0,
    errors,
    observed: {
      source_commit: capsule.source_commit ?? null,
      source_manifest_sha256: capsule.source_manifest_sha256 ?? null,
      payload_sha256: sha256Value(payload),
    },
  };
}

export function compareEnvironment(requested, observed) {
  const keys = [
    ...new Set([
      ...Object.keys(requested ?? {}),
      ...Object.keys(observed ?? {}),
    ]),
  ].sort();
  const fields = keys.map((key) => {
    const hasRequested = Object.hasOwn(requested ?? {}, key);
    const hasObserved = Object.hasOwn(observed ?? {}, key);
    const requestedValue = hasRequested ? requested[key] : null;
    const observedValue = hasObserved ? observed[key] : null;
    let status = "matched";
    if (!hasRequested) status = "unexpected_observation";
    else if (!hasObserved) status = "unknown";
    else if (canonicalJson(requestedValue) !== canonicalJson(observedValue))
      status = "drift";
    return { key, requested: requestedValue, observed: observedValue, status };
  });
  const counts = Object.fromEntries(
    ["matched", "drift", "unknown", "unexpected_observation"].map((status) => [
      status,
      fields.filter((field) => field.status === status).length,
    ]),
  );
  return {
    schema: "ghc.environment.drift-report.v1",
    fields,
    counts,
    exact_match: counts.drift === 0 && counts.unknown === 0,
  };
}

const ACTION_REQUIREMENTS = Object.freeze({
  inspect_repository: ["workspace_read"],
  write_owner_repository: ["workspace_write", "owner_scope"],
  publish_cloud_environment: ["cloud_publish", "human_authorization"],
  mutate_host_security: ["host_admin_token", "human_authorization"],
});

export function evaluatePrivilege(action, observation) {
  const required = ACTION_REQUIREMENTS[action];
  if (!required)
    return { allowed: false, reason: "unknown_action", required: [] };
  const observed = new Set(observation?.observed_grants ?? []);
  const missing = required.filter((grant) => !observed.has(grant));
  return {
    allowed: missing.length === 0,
    reason: missing.length
      ? "missing_observed_grant"
      : "all_observed_grants_present",
    required,
    missing,
    requested_labels_are_not_observed_grants: true,
  };
}

export function reduceRouteEvidence(events) {
  const result = {
    prepared: false,
    sent: false,
    acknowledged: false,
    recipient_completed: false,
    duplicate_count: 0,
    errors: [],
  };
  const seen = new Set();
  for (const event of events ?? []) {
    if (!event || typeof event !== "object") {
      result.errors.push("malformed_event");
      continue;
    }
    if (event.id && seen.has(event.id)) {
      result.duplicate_count += 1;
      continue;
    }
    if (event.id) seen.add(event.id);
    if (event.type === "prepared") result.prepared = true;
    else if (event.type === "send_accepted") result.sent = true;
    else if (event.type === "delivery_acknowledged") {
      if (!result.sent) result.errors.push("ack_without_send");
      else result.acknowledged = true;
    } else if (event.type === "recipient_completed") {
      if (!result.acknowledged)
        result.errors.push("completion_without_acknowledgement");
      else if (event.evidence_digest && HEX64.test(event.evidence_digest)) {
        result.recipient_completed = true;
      } else result.errors.push("completion_without_evidence_digest");
    } else result.errors.push("unknown_event_type");
  }
  result.ok = result.errors.length === 0;
  return result;
}

export function reconcileSetup(prior, plan) {
  const priorCompleted = new Set(prior?.completed ?? []);
  const priorFailures = Array.isArray(prior?.failures)
    ? structuredClone(prior.failures)
    : [];
  const actions = [];
  for (const step of plan ?? []) {
    if (!step || typeof step.id !== "string" || !step.id) {
      actions.push({ id: null, action: "reject", reason: "malformed_step" });
      continue;
    }
    if (priorCompleted.has(step.id)) {
      actions.push({
        id: step.id,
        action: "retain",
        reason: "already_completed",
      });
    } else if (
      step.dependencies?.some((dependency) => !priorCompleted.has(dependency))
    ) {
      actions.push({
        id: step.id,
        action: "hold",
        reason: "dependency_missing",
      });
    } else {
      actions.push({
        id: step.id,
        action: "execute_once",
        reason: "missing_current_step",
      });
      if (step.synthetic_result === "success") priorCompleted.add(step.id);
      else if (step.synthetic_result === "failure") {
        priorFailures.push({
          id: step.id,
          status: "retained_failure",
          credit: 0,
        });
      }
    }
  }
  return {
    schema: "ghc.setup.reconciliation.v1",
    completed: [...priorCompleted].sort(),
    failures: priorFailures,
    actions,
    restart_all: false,
  };
}

export function buildNexusEnvelope({
  source,
  payload,
  environment,
  route,
  reconciliation,
}) {
  const body = {
    schema: "ghc.local-cloud.nexus-envelope.v1",
    source,
    payload,
    environment,
    route,
    reconciliation,
    deployment_claim: false,
    authority_claim: false,
  };
  return { ...body, envelope_sha256: sha256Value(body) };
}
