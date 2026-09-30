import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  buildModels,
  privilegeMatrix,
  projectRoster,
  sha256Value,
} from "./nexus-core.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const x1 = path.resolve(here, "..");
const phase = path.resolve(x1, "..");
const rosterInput = JSON.parse(
  fs.readFileSync(
    path.join(phase, "planning", "roster-cycle-input.json"),
    "utf8",
  ),
);

const projection = projectRoster(rosterInput);
const models = {
  schema: "ghc.local-cloud-nexus.models.v1",
  status: "finite_synthetic",
  coordinate_semantics: {
    locality: "1 local to 5 cloud",
    evidence: "1 absent to 5 exact bounded",
    reversibility: "1 difficult to 5 easy",
    authority_gap: "1 small to 5 exact-gated",
  },
  models: buildModels(),
};
const privilege = privilegeMatrix();

const outputs = [
  ["roster-projection.json", projection],
  ["nexus-models.json", models],
  ["privilege-matrix.json", privilege],
];

for (const [name, value] of outputs) {
  fs.writeFileSync(
    path.join(x1, name),
    `${JSON.stringify(value, null, 2)}\n`,
    "utf8",
  );
}

const receipt = {
  schema: "ghc.tamar.v708-v3-r2.x1-build.v1",
  generated: outputs.map(([name, value]) => ({
    name,
    sha256: sha256Value(value),
  })),
  roster_rows: projection.row_count,
  model_count: models.models.length,
  endpoint_conflict: projection.endpoint_conflict,
  status: "BUILT_NOT_VALIDATED",
};
fs.writeFileSync(
  path.join(x1, "build-receipt.json"),
  `${JSON.stringify(receipt, null, 2)}\n`,
  "utf8",
);
