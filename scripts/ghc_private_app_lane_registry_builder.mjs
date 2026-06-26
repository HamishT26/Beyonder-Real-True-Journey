#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const DEFAULT_OUTPUT = join(ROOT, ".ghc-private", "ghc-app-lane-ids.local.json");
const SUPPORTED_LANES = ["Cicero", "Kierkegaard", "Aristotle"];

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const source = args.get("--source");
const output = args.get("--output") || DEFAULT_OUTPUT;

if (!source) {
  console.error("Usage: node ghc_private_app_lane_registry_builder.mjs --source <private-source> [--output <private-json>]");
  process.exit(2);
}

function extractIds(text) {
  const map = {};
  const missing = [];
  for (const lane of SUPPORTED_LANES) {
    const escapedLane = lane.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const pattern = new RegExp(`${escapedLane}: ` + "`" + "(019[0-9a-f-]+)" + "`");
    const match = text.match(pattern);
    if (match?.[1]) {
      map[lane] = match[1];
    } else {
      missing.push(lane);
    }
  }
  return { map, missing };
}

const text = readFileSync(source, "utf8");
const { map, missing } = extractIds(text);
const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
const payload = {
  artifact_type: "ghc_private_app_lane_registry",
  generated_utc: generatedUtc,
  source_artifact: basename(source),
  lanes: map,
  lane_count: Object.keys(map).length,
  missing_lanes: missing,
  private_boundary: {
    local_only: true,
    ignored_by_git: true,
    publish_raw_ids: false,
  },
};

mkdirSync(dirname(output), { recursive: true });
writeFileSync(output, `${JSON.stringify(payload, null, 2)}\n`, "utf8");

console.log(
  JSON.stringify(
    {
      status: missing.length === 0 ? "PASS_PRIVATE_APP_LANE_REGISTRY_BUILT" : "OPEN_GAP_PRIVATE_APP_LANE_REGISTRY_PARTIAL",
      source_artifact: basename(source),
      lane_count: Object.keys(map).length,
      missing_lanes: missing,
      output_artifact: basename(output),
    },
    null,
    2,
  ),
);
