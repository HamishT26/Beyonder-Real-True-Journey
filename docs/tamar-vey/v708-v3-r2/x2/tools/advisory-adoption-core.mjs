import { canonicalJson, sha256Value } from "../../x1/tools/nexus-core.mjs";

export function expectationAwareVerdict(pkg, expectation, policyVersion) {
  const required = [
    "repository",
    "path",
    "source_commit",
    "origin",
    "purpose",
    "schema",
    "payload_sha256",
  ];
  const missing = required.filter(
    (field) =>
      !Object.hasOwn(pkg ?? {}, field) ||
      !Object.hasOwn(expectation ?? {}, field),
  );
  if (missing.length) return { verdict: "MISSING_SOURCE_EXPECTATION", missing };
  const mismatches = required.filter(
    (field) => canonicalJson(pkg[field]) !== canonicalJson(expectation[field]),
  );
  const packageDigest = sha256Value(pkg);
  const expectationDigest = sha256Value(expectation);
  return {
    verdict: mismatches.length ? "SOURCE_MISMATCH" : "MATCH",
    mismatches,
    receipt_key: sha256Value({
      packageDigest,
      expectationDigest,
      policyVersion,
    }),
    package_digest: packageDigest,
    expectation_digest: expectationDigest,
    policy_version: policyVersion,
  };
}

export function compareEnvironmentViews({ requested, configured, effective }) {
  if (
    !effective?.process_generation ||
    !Number.isInteger(effective?.observed_tick)
  ) {
    return { verdict: "UNBOUND_EFFECTIVE_OBSERVATION", fields: [] };
  }
  const profileFields = ["runtime", "dependencies", "cache", "listener"];
  const fields = profileFields.map((field) => ({
    field,
    requested: requested?.[field] ?? null,
    configured: configured?.[field] ?? null,
    effective: effective?.profile?.[field] ?? null,
    requested_matches_configured:
      canonicalJson(requested?.[field]) === canonicalJson(configured?.[field]),
    effective_matches_requested:
      canonicalJson(effective?.profile?.[field]) ===
      canonicalJson(requested?.[field]),
  }));
  return {
    verdict: fields.every((field) => field.effective_matches_requested)
      ? "EFFECTIVE_MATCH"
      : "RUNTIME_DRIFT",
    process_generation: effective.process_generation,
    observed_tick: effective.observed_tick,
    fields,
  };
}

export function permitFourGate({ application, host, sandbox, workflow }) {
  const gates = { application, host, sandbox, workflow };
  const missing = Object.entries(gates)
    .filter(([, value]) => value !== true)
    .map(([key]) => key);
  return {
    permit: missing.length === 0,
    missing,
    mock_effect_count: missing.length === 0 ? 1 : 0,
  };
}

export function reduceCorrelatedCompletion(expected, events) {
  const states = [];
  let submitted = false;
  let acknowledged = false;
  let completed = false;
  let acceptedCompletionIdentity = null;
  let submissions = 0;
  const failures = [];
  for (const event of events) {
    if (event.type === "submit") {
      if (!submitted) {
        submitted = true;
        submissions += 1;
      } else failures.push("duplicate_submission_blocked");
    } else if (event.type === "acknowledgement") {
      if (submitted && tupleMatches(expected, event.binding))
        acknowledged = true;
      else failures.push("acknowledgement_binding_mismatch");
    } else if (event.type === "completion") {
      const bindingMatch = tupleMatches(expected, event.binding);
      const digestMatch = event.result_digest === expected.result_digest;
      if (acknowledged && bindingMatch && digestMatch) {
        completed = true;
        acceptedCompletionIdentity ??= event.id;
      } else failures.push("completion_correlation_mismatch");
    } else if (event.type === "opaque_wait") {
      failures.push("opaque_wait_no_state_promotion");
    }
    states.push(completed);
  }
  return {
    completion_flags: states,
    submissions,
    acknowledged,
    completed,
    accepted_completion_identity: acceptedCompletionIdentity,
    failures,
  };
}

function tupleMatches(expected, binding) {
  const fields = ["edge", "capsule", "recipient", "purpose", "phase", "run"];
  return fields.every((field) => binding?.[field] === expected?.[field]);
}

export function reconcileDurableAttempt({ history, effectStore, resumeCount }) {
  const immutableHistory = structuredClone(history);
  const completed = new Set(
    history
      .filter((entry) => entry.status === "SUCCESS")
      .map((entry) => entry.step),
  );
  const started = history.find((entry) => entry.status === "STARTED");
  let cacheExecutions = 0;
  let readbackExecutions = 0;
  let recoveredReceipt = null;

  if (started) {
    const durable = effectStore.find(
      (entry) =>
        entry.step === started.step &&
        entry.attempt === started.attempt &&
        entry.input_digest === started.input_digest,
    );
    if (durable) {
      recoveredReceipt = durable.receipt;
      completed.add(started.step);
    } else {
      return {
        verdict: "RECOVERY_PROVENANCE_GAP",
        immutable_history: immutableHistory,
        cache_executions: 0,
        readback_executions: 0,
      };
    }
  }
  if (completed.has("cache") && !completed.has("readback") && resumeCount > 0) {
    readbackExecutions = 1;
    completed.add("readback");
  }
  return {
    verdict: "RECONCILED",
    immutable_history: immutableHistory,
    completed: [...completed].sort(),
    recovered_receipt: recoveredReceipt,
    environment_executions: 0,
    cache_executions: cacheExecutions,
    readback_executions: readbackExecutions,
    failed_records: immutableHistory.filter(
      (entry) => entry.status === "FAILED",
    ),
  };
}
