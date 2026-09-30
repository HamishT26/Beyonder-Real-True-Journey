import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
  buildModels,
  canonicalJson,
  nextPhase,
  privilegeMatrix,
  projectRoster,
  sha256Value,
  validateCapsule,
} from "../tools/nexus-core.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const x1 = path.resolve(here, "..");
const planning = path.resolve(x1, "..", "planning");
const read = (relative) =>
  JSON.parse(fs.readFileSync(path.join(x1, relative), "utf8"));
const valid = read("fixtures/capsule-valid.json");
const rosterInput = JSON.parse(
  fs.readFileSync(path.join(planning, "roster-cycle-input.json"), "utf8"),
);

test("canonical JSON ignores object key insertion order", () => {
  assert.equal(canonicalJson({ b: 2, a: 1 }), canonicalJson({ a: 1, b: 2 }));
});

test("canonical digest is stable", () => {
  assert.equal(sha256Value({ b: 2, a: 1 }), sha256Value({ a: 1, b: 2 }));
});

test("valid capsule passes", () =>
  assert.deepEqual(validateCapsule(valid), { ok: true, errors: [] }));

for (const [label, mutate, expected] of [
  ["wrong schema", (x) => (x.schema_version = "wrong"), "schema_version"],
  ["bad commit", (x) => (x.source_commit = "abc"), "source_commit"],
  [
    "bad manifest",
    (x) => (x.source_manifest_sha256 = "abc"),
    "source_manifest_sha256",
  ],
  [
    "bad classification",
    (x) => (x.classification = "private"),
    "classification",
  ],
  ["expired", (x) => (x.expires_at = x.created_at), "expires_at"],
  ["overspend", (x) => (x.max_cost_usd = 50.01), "max_cost_usd"],
  [
    "unknown operation",
    (x) => x.operations.push("deploy"),
    "operations_allowlist",
  ],
  [
    "absolute Windows path",
    (x) => (x.files[0].path = "C:\\private\\x"),
    "file_path",
  ],
  ["absolute Unix path", (x) => (x.files[0].path = "/private/x"), "file_path"],
  ["traversal", (x) => (x.files[0].path = "../x"), "file_path"],
  ["bad file digest", (x) => (x.files[0].sha256 = "bad"), "file_sha256"],
  [
    "authority promotion",
    (x) => (x.authority_claims.empirical = true),
    "authority_nonpromotion",
  ],
]) {
  test(`capsule rejects ${label}`, () => {
    const subject = structuredClone(valid);
    mutate(subject);
    assert.equal(validateCapsule(subject).ok, false);
    assert.ok(validateCapsule(subject).errors.includes(expected));
  });
}

test("capsule rejects secret-shaped key", () => {
  const subject = read("fixtures/capsule-invalid-secret-key.json");
  assert.match(validateCapsule(subject).errors.join("|"), /prohibited_keys/);
});

test("phase increments within version", () =>
  assert.deepEqual(nextPhase(708, 4), { version: 708, slot: 5 }));
test("phase increments version after v8", () =>
  assert.deepEqual(nextPhase(708, 8), { version: 709, slot: 1 }));

test("roster projection has exact range", () => {
  const projection = projectRoster(rosterInput);
  assert.equal(projection.row_count, 141);
  assert.equal(projection.start.owner, "Saelin Reed");
  assert.equal(projection.start.phase, "v708-v4");
  assert.equal(projection.rows[1].owner, "Elowen Cairn");
  assert.equal(projection.endpoint.phase, "v725-v8");
});

test("roster exposes endpoint conflict", () => {
  const projection = projectRoster(rosterInput);
  assert.equal(projection.endpoint.owner, "Ceryn Alder");
  assert.equal(projection.endpoint_conflict, true);
});

test("roster rejects uninstantiated Dot placeholder", () => {
  const subject = structuredClone(rosterInput);
  subject.cycle[0].owner = "New ChatGPT/Codex Dot sibling #1";
  assert.throws(() => projectRoster(subject), /placeholder/);
});

test("roster rejects duplicate positions", () => {
  const subject = structuredClone(rosterInput);
  subject.cycle[1].position = 1;
  assert.throws(() => projectRoster(subject), /duplicate/);
});

test("privilege matrix preserves non-equivalence", () => {
  const matrix = privilegeMatrix();
  assert.equal(matrix.all_equivalent, false);
  assert.equal(matrix.dimensions.length, 5);
});

test("fifteen models are finite and nonphysical", () => {
  const models = buildModels();
  assert.equal(models.length, 15);
  assert.ok(models.every((model) => model.physical_claim === false));
  assert.ok(models.every((model) => model.production_claim === false));
});
