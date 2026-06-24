#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const fullToolsTraceRoot = args.get("--full-tools-trace-root");
const receiptPrefix = args.get("--receipt-prefix") || `${phaseSlug}-sanitized-lane-harvest-reducer`;

if (!phaseSlug || !fullToolsTraceRoot) {
  console.error("Usage: node scripts/ghc_sanitized_lane_harvest_reducer.mjs --phase-slug <slug> --full-tools-trace-root <path>");
  process.exit(2);
}

const arbyCycle = readOptional(`${phaseSlug}-arby-strict-cli-receipt-v1.json`);
const arbyCompletion = readOptional(`${phaseSlug}-arby-strict-cli-completion-v1.json`);
const arbyQuality = readOptional(`${phaseSlug}-arby-strict-cli-quality-v1.json`);
const arbyMarker = readOptional(`${phaseSlug}-arby-strict-cli-marker-review-v1.json`);
const ciceroRunner = readOptional(`${phaseSlug}-cicero-background-v1.json`);
const ciceroGate = readOptional(`${phaseSlug}-cicero-background-completion-gate-v1.json`);

const arbyCompletionReady = ["FINAL_MESSAGES_READY", "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW"].includes(arbyCompletion?.aggregate_status);
const arbyPassed =
  arbyCycle?.overall_status === "PASS_STRICT_CLI_BACKGROUND_WATCH_STARTED" &&
  arbyCompletionReady &&
  arbyQuality?.aggregate_status === "PASS_ALL_CLI_LANES_ELABORATE" &&
  arbyMarker?.overall_status === "PASS_MARKER_REVIEW_LEDGER";
const ciceroPassed =
  ciceroRunner?.overall_status === "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED" &&
  ciceroGate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE";

const receipt = {
  artifact_type: "ghc_sanitized_lane_harvest_reducer",
  generated_utc: new Date().toISOString(),
  phase_slug: phaseSlug,
  overall_status: arbyPassed && ciceroPassed ? "PASS_SANITIZED_LANE_HARVEST_REDUCED" : "OPEN_GAP_SANITIZED_LANE_HARVEST_REDUCER",
  lanes: {
    arby: {
      route: "strict_cli_background_watch_then_completion_quality_marker_review",
      background_status: arbyCycle?.overall_status || "missing",
      completion_status: arbyCompletion?.aggregate_status || "missing",
      quality_status: arbyQuality?.aggregate_status || "missing",
      marker_status: arbyMarker?.overall_status || "missing",
      word_count: arbyQuality?.lanes?.[0]?.word_count || null,
      item_count: arbyQuality?.lanes?.[0]?.numbered_or_bullet_item_count || null,
      passed: arbyPassed,
    },
    cicero: {
      route: "recovered_app_lane_background_watch_then_completion_gate",
      background_status: ciceroRunner?.overall_status || "missing",
      completion_gate_status: ciceroGate?.overall_status || "missing",
      passed: ciceroPassed,
    },
  },
  publication_boundary: {
    full_tools_path_published: false,
    raw_sibling_output_published: false,
    private_route_handles_published: false,
    private_callable_ids_published: false,
    local_absolute_paths_published: false,
    credentials_published: false,
  },
};

writePair(receiptPrefix, receipt);
console.log(JSON.stringify({ status: receipt.overall_status, phase_slug: phaseSlug, arby_passed: arbyPassed, cicero_passed: ciceroPassed }, null, 2));
process.exit(receipt.overall_status.startsWith("PASS") ? 0 : 1);

function readOptional(name) {
  try {
    return JSON.parse(fs.readFileSync(path.join(fullToolsTraceRoot, name), "utf8"));
  } catch {
    return null;
  }
}

function writePair(prefix, payload) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.md`), renderMd(payload), "utf8");
}

function renderMd(payload) {
  return [
    `# ${payload.phase_slug} Sanitized Lane Harvest Reducer`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    `- Arby passed: \`${payload.lanes.arby.passed}\``,
    `- Cicero passed: \`${payload.lanes.cicero.passed}\``,
    `- Arby words: \`${payload.lanes.arby.word_count || "not_recorded"}\``,
    `- Arby items: \`${payload.lanes.arby.item_count || "not_recorded"}\``,
    "",
    "No raw sibling output, private route handle, callable ID, local path value, credential, screenshot, proof closure, or identity merge claim is published.",
    "",
  ].join("\n");
}
