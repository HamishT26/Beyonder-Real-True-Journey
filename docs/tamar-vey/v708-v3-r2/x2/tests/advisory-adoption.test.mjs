import assert from "node:assert/strict";
import test from "node:test";
import {
  compareEnvironmentViews,
  expectationAwareVerdict,
  permitFourGate,
  reconcileDurableAttempt,
  reduceCorrelatedCompletion,
} from "../tools/advisory-adoption-core.mjs";

const basePackage = {
  repository: "fixture-repo",
  path: "result.json",
  source_commit: "1".repeat(40),
  origin: "cloud",
  purpose: "review",
  schema: 1,
  payload_sha256: "a".repeat(64),
};

test("A1 matches identical package and expectation", () => {
  assert.equal(
    expectationAwareVerdict(basePackage, basePackage, "p1").verdict,
    "MATCH",
  );
});

test("A1 rejects same payload under different source expectation", () => {
  const expectation = { ...basePackage, source_commit: "2".repeat(40) };
  const result = expectationAwareVerdict(basePackage, expectation, "p1");
  assert.equal(result.verdict, "SOURCE_MISMATCH");
  assert.deepEqual(result.mismatches, ["source_commit"]);
});

test("A1 cache key binds package, expectation, and policy", () => {
  const same = expectationAwareVerdict(
    basePackage,
    basePackage,
    "p1",
  ).receipt_key;
  const otherExpectation = expectationAwareVerdict(
    basePackage,
    { ...basePackage, source_commit: "2".repeat(40) },
    "p1",
  ).receipt_key;
  const otherPolicy = expectationAwareVerdict(
    basePackage,
    basePackage,
    "p2",
  ).receipt_key;
  assert.notEqual(same, otherExpectation);
  assert.notEqual(same, otherPolicy);
});

test("A1 classifies missing expectation separately", () => {
  const expectation = { ...basePackage };
  delete expectation.source_commit;
  assert.equal(
    expectationAwareVerdict(basePackage, expectation, "p1").verdict,
    "MISSING_SOURCE_EXPECTATION",
  );
});

const profileB = {
  runtime: "py-B",
  dependencies: "deps-B",
  cache: "writable",
  listener: "loopback",
};

test("A2 detects effective process drift", () => {
  const result = compareEnvironmentViews({
    requested: profileB,
    configured: profileB,
    effective: {
      process_generation: "g0",
      observed_tick: 10,
      profile: { ...profileB, runtime: "py-A", dependencies: "deps-A" },
    },
  });
  assert.equal(result.verdict, "RUNTIME_DRIFT");
  assert.equal(
    result.fields.filter((field) => !field.effective_matches_requested).length,
    2,
  );
});

test("A2 accepts a bound effective match", () => {
  const result = compareEnvironmentViews({
    requested: profileB,
    configured: profileB,
    effective: {
      process_generation: "g1",
      observed_tick: 11,
      profile: profileB,
    },
  });
  assert.equal(result.verdict, "EFFECTIVE_MATCH");
});

test("A2 refuses unbound effective observation", () => {
  assert.equal(
    compareEnvironmentViews({
      requested: profileB,
      configured: profileB,
      effective: { profile: profileB },
    }).verdict,
    "UNBOUND_EFFECTIVE_OBSERVATION",
  );
});

test("A3 enumerates one permit among sixteen Boolean combinations", () => {
  const rows = [];
  for (const application of [false, true])
    for (const host of [false, true])
      for (const sandbox of [false, true])
        for (const workflow of [false, true])
          rows.push(permitFourGate({ application, host, sandbox, workflow }));
  assert.equal(rows.filter((row) => row.permit).length, 1);
  assert.equal(
    rows.reduce((sum, row) => sum + row.mock_effect_count, 0),
    1,
  );
});

test("A3 blocks the dropped-host-gate counterexample", () => {
  assert.equal(
    permitFourGate({
      application: true,
      host: false,
      sandbox: true,
      workflow: true,
    }).permit,
    false,
  );
});

const expectedRoute = {
  edge: "e0",
  capsule: "p0",
  recipient: "slot0",
  purpose: "review-startup",
  phase: "X2",
  run: "r0",
  result_digest: "d".repeat(64),
};

test("A4 keeps acknowledgement distinct from completion", () => {
  const result = reduceCorrelatedCompletion(expectedRoute, [
    { type: "submit" },
    { type: "acknowledgement", binding: expectedRoute },
  ]);
  assert.deepEqual(result.completion_flags, [false, false]);
  assert.equal(result.acknowledged, true);
});

test("A4 matches the six-tick completion oracle", () => {
  const result = reduceCorrelatedCompletion(expectedRoute, [
    { type: "submit" },
    { type: "acknowledgement", binding: expectedRoute },
    {
      id: "wrong",
      type: "completion",
      binding: { ...expectedRoute, capsule: "p1" },
      result_digest: expectedRoute.result_digest,
    },
    { type: "opaque_wait" },
    {
      id: "right",
      type: "completion",
      binding: expectedRoute,
      result_digest: expectedRoute.result_digest,
    },
    {
      id: "right",
      type: "completion",
      binding: expectedRoute,
      result_digest: expectedRoute.result_digest,
    },
  ]);
  assert.deepEqual(result.completion_flags, [
    false,
    false,
    false,
    false,
    true,
    true,
  ]);
  assert.equal(result.submissions, 1);
  assert.equal(result.accepted_completion_identity, "right");
});

test("A4 blocks duplicate submission", () => {
  const result = reduceCorrelatedCompletion(expectedRoute, [
    { type: "submit" },
    { type: "submit" },
  ]);
  assert.equal(result.submissions, 1);
  assert.ok(result.failures.includes("duplicate_submission_blocked"));
});

const history = [
  { id: "sA", step: "environment", attempt: 1, status: "SUCCESS" },
  { id: "fB", step: "cache", attempt: 1, status: "FAILED", credit: 0 },
  {
    id: "b2",
    step: "cache",
    attempt: 2,
    status: "STARTED",
    input_digest: "i2",
  },
];
const effectStore = [
  {
    step: "cache",
    attempt: 2,
    input_digest: "i2",
    receipt: "rB",
    completed_tick: 2,
  },
];

test("A5 reconciles durable success without rerunning prior effects", () => {
  const result = reconcileDurableAttempt({
    history,
    effectStore,
    resumeCount: 2,
  });
  assert.equal(result.verdict, "RECONCILED");
  assert.equal(result.environment_executions, 0);
  assert.equal(result.cache_executions, 0);
  assert.equal(result.readback_executions, 1);
  assert.equal(result.recovered_receipt, "rB");
});

test("A5 retains the failed first attempt at zero credit", () => {
  const result = reconcileDurableAttempt({
    history,
    effectStore,
    resumeCount: 2,
  });
  assert.deepEqual(result.failed_records, [
    { id: "fB", step: "cache", attempt: 1, status: "FAILED", credit: 0 },
  ]);
});

test("A5 refuses recovery without exact durable binding", () => {
  const result = reconcileDurableAttempt({
    history,
    effectStore: [],
    resumeCount: 2,
  });
  assert.equal(result.verdict, "RECOVERY_PROVENANCE_GAP");
  assert.equal(result.cache_executions, 0);
});
