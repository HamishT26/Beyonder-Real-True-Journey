#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v4-x2";
const sourcePhase = args.get("--source-phase") || "v553-gmut-thos-v4-x1";
const source = readJson(path.join(tracesDir, `${sourcePhase}-closeout-v1.json`));
const lanes = source?.lane_gate_summary || {};
const appLanes = ["kierkegaard", "aristotle"].map((key) => ({
  lane: key === "kierkegaard" ? "Kierkegaard" : "Aristotle",
  status: lanes[key]?.lane_status || "missing",
  gate: lanes[key]?.completion_gate_status || "missing",
  passed: lanes[key]?.passed === true,
}));
const allPassed = appLanes.every((lane) => lane.passed);
const receipt = {
  artifact_type: "ghc_app_lane_completion_reconciler",
  generated_utc: new Date().toISOString(),
  phase_slug: phaseSlug,
  source_phase: sourcePhase,
  overall_status: allPassed ? "PASS_APP_LANE_COMPLETION_RECONCILED" : "OPEN_GAP_APP_LANE_COMPLETION_RECONCILE",
  app_lanes: appLanes,
  source_boundary: {
    raw_app_state_read: false,
    raw_lane_text_read: false,
    private_callable_ids_read: false,
    sanitized_closeout_only: true,
  },
  publication_boundary: {
    raw_transcripts_published: false,
    private_route_handles_published: false,
    private_callable_ids_published: false,
    local_absolute_paths_published: false,
    credentials_published: false,
  },
};

writePair(`${phaseSlug}-app-lane-completion-reconciler-v1`, receipt);
process.stdout.write(JSON.stringify({ status: receipt.overall_status, app_lanes: appLanes.length }, null, 2) + "\n");
process.exit(allPassed ? 0 : 1);

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    return null;
  }
}

function writePair(baseName, payload) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${baseName}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(
    path.join(tracesDir, `${baseName}.md`),
    [
      `# ${phaseSlug} App-Lane Completion Reconciler`,
      "",
      `Status: \`${payload.overall_status}\``,
      "",
      ...payload.app_lanes.map((lane) => `- ${lane.lane}: \`${lane.status}\`, gate \`${lane.gate}\`, passed \`${lane.passed}\``),
      "",
      "Sanitized closeout facts only; no raw app state, private route handles, callable IDs, local paths, transcripts, or credentials are published.",
      "",
    ].join("\n"),
    "utf8",
  );
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
}
