import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
  buildNexusEnvelope,
  compareEnvironment,
  evaluatePrivilege,
  reconcileSetup,
  reduceRouteEvidence,
  verifySourceBinding,
} from "../tools/nexus-x2-core.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const x2 = path.resolve(here, "..");
const read = (relative) =>
  JSON.parse(fs.readFileSync(path.join(x2, relative), "utf8"));

const binding = read("fixtures/source-binding.json");
const environment = read("fixtures/environment-drift.json");
const route = read("fixtures/route-evidence.json");
const setup = read("fixtures/partial-setup.json");

test("source binding positive control passes", () => {
  assert.equal(verifySourceBinding(binding).ok, true);
});

for (const [label, mutate, error] of [
  [
    "commit substitution",
    (x) => (x.capsule.source_commit = "b".repeat(40)),
    "source_commit_mismatch",
  ],
  [
    "manifest substitution",
    (x) => (x.capsule.source_manifest_sha256 = "b".repeat(64)),
    "source_manifest_mismatch",
  ],
  [
    "payload substitution",
    (x) => x.payload.rows.push(4),
    "payload_digest_mismatch",
  ],
  [
    "bad expected commit",
    (x) => (x.expected.source_commit = "bad"),
    "expected_commit_shape",
  ],
  [
    "bad expected manifest",
    (x) => (x.expected.source_manifest_sha256 = "bad"),
    "expected_manifest_shape",
  ],
  [
    "bad expected payload",
    (x) => (x.expected.payload_sha256 = "bad"),
    "expected_payload_shape",
  ],
]) {
  test(`source binding rejects ${label}`, () => {
    const subject = structuredClone(binding);
    mutate(subject);
    const result = verifySourceBinding(subject);
    assert.equal(result.ok, false);
    assert.ok(result.errors.includes(error));
  });
}

test("source binding rejects missing capsule", () => {
  assert.deepEqual(
    verifySourceBinding({
      capsule: null,
      expected: binding.expected,
      payload: binding.payload,
    }),
    { ok: false, errors: ["capsule_missing"] },
  );
});

test("environment comparison preserves matched, drift, and unknown", () => {
  const result = compareEnvironment(
    environment.requested,
    environment.observed,
  );
  assert.equal(result.counts.matched, 2);
  assert.equal(result.counts.drift, 1);
  assert.equal(result.counts.unknown, 1);
  assert.equal(result.exact_match, false);
});

test("environment comparison marks unexpected observations", () => {
  const result = compareEnvironment({}, { extra: true });
  assert.equal(result.counts.unexpected_observation, 1);
});

test("environment comparison accepts exact equality", () => {
  const result = compareEnvironment({ a: [1, 2] }, { a: [1, 2] });
  assert.equal(result.exact_match, true);
});

test("privilege allows bounded repository inspection", () => {
  const result = evaluatePrivilege("inspect_repository", {
    observed_grants: ["workspace_read"],
  });
  assert.equal(result.allowed, true);
});

test("full access label alone does not grant host mutation", () => {
  const result = evaluatePrivilege("mutate_host_security", {
    observed_grants: ["full_access_label"],
  });
  assert.equal(result.allowed, false);
  assert.deepEqual(result.missing, ["host_admin_token", "human_authorization"]);
});

test("host mutation requires token and authorization", () => {
  const result = evaluatePrivilege("mutate_host_security", {
    observed_grants: ["host_admin_token", "human_authorization"],
  });
  assert.equal(result.allowed, true);
});

test("cloud publication requires explicit observed authority", () => {
  const result = evaluatePrivilege("publish_cloud_environment", {
    observed_grants: ["cloud_publish"],
  });
  assert.equal(result.allowed, false);
  assert.deepEqual(result.missing, ["human_authorization"]);
});

test("unknown action is rejected", () => {
  assert.equal(evaluatePrivilege("become_admin", {}).reason, "unknown_action");
});

test("delivery acknowledgement is not recipient completion", () => {
  const result = reduceRouteEvidence(route.events);
  assert.equal(result.ok, true);
  assert.equal(result.acknowledged, true);
  assert.equal(result.recipient_completed, false);
});

test("completion needs acknowledgement", () => {
  const result = reduceRouteEvidence([
    { id: "A", type: "recipient_completed", evidence_digest: "a".repeat(64) },
  ]);
  assert.ok(result.errors.includes("completion_without_acknowledgement"));
});

test("completion needs an evidence digest", () => {
  const result = reduceRouteEvidence([
    { id: "A", type: "send_accepted" },
    { id: "B", type: "delivery_acknowledged" },
    { id: "C", type: "recipient_completed" },
  ]);
  assert.ok(result.errors.includes("completion_without_evidence_digest"));
});

test("completion with evidence is distinct and explicit", () => {
  const result = reduceRouteEvidence([
    { id: "A", type: "send_accepted" },
    { id: "B", type: "delivery_acknowledged" },
    { id: "C", type: "recipient_completed", evidence_digest: "a".repeat(64) },
  ]);
  assert.equal(result.recipient_completed, true);
});

test("duplicate route events are ignored and counted", () => {
  const result = reduceRouteEvidence([
    { id: "A", type: "prepared" },
    { id: "A", type: "send_accepted" },
  ]);
  assert.equal(result.duplicate_count, 1);
  assert.equal(result.sent, false);
});

test("malformed route event remains a failure", () => {
  assert.ok(reduceRouteEvidence([null]).errors.includes("malformed_event"));
});

test("partial setup retains prior success and failure", () => {
  const result = reconcileSetup(setup.prior, setup.plan);
  assert.equal(result.restart_all, false);
  assert.equal(result.actions[0].action, "retain");
  assert.equal(result.actions[1].action, "retain");
  assert.equal(result.actions[2].action, "execute_once");
  assert.equal(result.actions[3].action, "hold");
  assert.equal(result.failures.length, 1);
});

test("failed new setup step is retained at zero credit", () => {
  const result = reconcileSetup({ completed: [], failures: [] }, [
    { id: "probe", synthetic_result: "failure" },
  ]);
  assert.deepEqual(result.failures, [
    { id: "probe", status: "retained_failure", credit: 0 },
  ]);
});

test("malformed setup step is rejected", () => {
  assert.equal(reconcileSetup({}, [{}]).actions[0].action, "reject");
});

test("nexus envelope is stable and nonpromotional", () => {
  const args = {
    source: verifySourceBinding(binding),
    payload: binding.payload,
    environment: compareEnvironment(
      environment.requested,
      environment.observed,
    ),
    route: reduceRouteEvidence(route.events),
    reconciliation: reconcileSetup(setup.prior, setup.plan),
  };
  const first = buildNexusEnvelope(args);
  const second = buildNexusEnvelope(structuredClone(args));
  assert.equal(first.envelope_sha256, second.envelope_sha256);
  assert.equal(first.deployment_claim, false);
  assert.equal(first.authority_claim, false);
});
