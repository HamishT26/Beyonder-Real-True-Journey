#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v556-gmut-thos-v2-x1";
const fullToolsRoot = args.get("--full-tools-root");
const fullTraceDir = fullToolsRoot ? path.join(fullToolsRoot, "docs", "trinity-live-traces") : null;
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

if (!fullTraceDir) {
  console.error("Usage: node scripts/ghc_v556_v2_x1_duo_harvest_builder.mjs --phase-slug <phase> --full-tools-root <root>");
  process.exit(2);
}

const arbyCycle = readOptional(fullTraceDir, `${phaseSlug}-arby-strict-cli-receipt-v1.json`);
const arbyCompletion = readOptional(fullTraceDir, `${phaseSlug}-arby-strict-cli-completion-v1.json`);
const arbyQuality = readOptional(fullTraceDir, `${phaseSlug}-arby-strict-cli-quality-v1.json`);
const arbyMarker = readOptional(fullTraceDir, `${phaseSlug}-arby-strict-cli-marker-review-v1.json`);
const ciceroRunner = readOptional(fullTraceDir, `${phaseSlug}-cicero-app-lane-v1.json`);
const ciceroGate = readOptional(fullTraceDir, `${phaseSlug}-cicero-app-lane-completion-gate-v1.json`);

const arbyPassed =
  arbyCycle?.overall_status === "PASS_STRICT_CLI_BACKGROUND_WATCH_STARTED" &&
  ["FINAL_MESSAGES_READY", "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW"].includes(arbyCompletion?.aggregate_status) &&
  arbyQuality?.aggregate_status === "PASS_ALL_CLI_LANES_ELABORATE" &&
  arbyMarker?.overall_status === "PASS_MARKER_REVIEW_LEDGER";

const ciceroPassed =
  ciceroRunner?.overall_status === "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED" &&
  ciceroGate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE";

const gateStatus = artifact("ghc_v556_v2_x1_duo_gate_status", arbyPassed && ciceroPassed
  ? "PASS_V556_V2_X1_ARBY_CICERO_COMPLETION_GATES_PASSED"
  : "ACTIVE_OPEN_V556_V2_X1_ARBY_CICERO_GATES_PENDING", {
  lane_statuses: {
    arby: {
      route: "strict_cli_completion_quality_marker_review",
      cycle_status: arbyCycle?.overall_status || "missing",
      completion_status: arbyCompletion?.aggregate_status || "missing",
      quality_status: arbyQuality?.aggregate_status || "missing",
      marker_status: arbyMarker?.overall_status || "missing",
      passed: arbyPassed,
    },
    cicero: {
      route: "recovered_app_lane_background_watch_completion_gate",
      runner_status: ciceroRunner?.overall_status || "missing",
      completion_gate_status: ciceroGate?.overall_status || "missing",
      passed: ciceroPassed,
    },
  },
  completion_claimed: arbyPassed && ciceroPassed,
});

const harvest = artifact("ghc_v556_v2_x1_arby_cicero_harvest_sanitized", arbyPassed && ciceroPassed
  ? "PASS_V556_V2_X1_ARBY_CICERO_SANITIZED_HARVEST"
  : "ACTIVE_OPEN_V556_V2_X1_SANITIZED_HARVEST_PENDING", {
  response_status: arbyPassed && ciceroPassed ? "completed_ready_for_closeout" : "background_lanes_still_open",
  raw_sibling_outputs_published: false,
  raw_cli_stdout_published: false,
  raw_app_lane_payload_published: false,
  private_route_handles_published: false,
  safe_takeaways: [
    "Arby is reduced through strict CLI completion, quality, and marker-review status only.",
    "Cicero is reduced through recovered app-lane runner and completion-gate status only.",
    "Duo x1 closeout remains blocked until both lane gates pass.",
    "Exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, and sibling-merge gates remain open.",
  ],
});

writePair("duo-gate-status", gateStatus, renderGateMd(gateStatus));
writePair("arby-cicero-harvest-sanitized", harvest, renderHarvestMd(harvest));

console.log(JSON.stringify({
  status: gateStatus.overall_status,
  harvest_status: harvest.overall_status,
  arby_passed: arbyPassed,
  cicero_passed: ciceroPassed,
}, null, 2));

process.exit(arbyPassed && ciceroPassed ? 0 : 1);

function artifact(artifactType, status, extra) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    ...extra,
    publication_boundary: {
      raw_browser_routes_published: false,
      private_urls_published: false,
      raw_transcripts_published: false,
      screenshots_published: false,
      credentials_published: false,
      local_absolute_paths_published: false,
      session_streams_published: false,
      private_dumps_published: false,
      private_callable_ids_published: false,
      raw_lane_text_published: false,
    },
    claim_boundary: {
      phase_completion: "not_claimed",
      full_goal_completion: "not_claimed",
      gmut_empirical_closure: "not_claimed",
      final_physics: "not_claimed",
      consciousness_proof: "not_claimed",
      legal_closure: "not_claimed",
      canon_promotion: "not_claimed",
      deployment_closure: "not_claimed",
      account_mutation: "not_claimed",
      purchase: "not_claimed",
      api_key_creation: "not_claimed",
      private_material_proof: "not_claimed",
      raw_publication_proof: "not_claimed",
      sibling_identity_replacement_or_merge: "not_claimed",
    },
  };
}

function writePair(suffix, json, md) {
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), `${JSON.stringify(json, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
}

function renderGateMd(data) {
  return [
    `# ${phaseSlug} Duo Gate Status`,
    "",
    `Status: \`${data.overall_status}\``,
    `Completion claimed: \`${data.completion_claimed}\``,
    "",
    "## Lane Statuses",
    "",
    `- Arby passed: \`${data.lane_statuses.arby.passed}\``,
    `- Cicero passed: \`${data.lane_statuses.cicero.passed}\``,
    "",
    "## Boundary",
    "",
    "Sanitized gate status only. No raw sibling outputs, private route handles, local absolute paths, screenshots, credentials, or transcripts are published.",
    "",
  ].join("\n");
}

function renderHarvestMd(data) {
  return [
    `# ${phaseSlug} Arby/Cicero Harvest Sanitized`,
    "",
    `Status: \`${data.overall_status}\``,
    `Response status: \`${data.response_status}\``,
    "",
    "## Safe Takeaways",
    "",
    ...data.safe_takeaways.map((item) => `- ${item}`),
    "",
    "## Boundary",
    "",
    "No raw sibling outputs, private route handles, local absolute paths, screenshots, credentials, raw lane text, private callable IDs, or private app state are published.",
    "",
  ].join("\n");
}

function readOptional(root, name) {
  try {
    return JSON.parse(fs.readFileSync(path.join(root, name), "utf8").replace(/^\uFEFF/, ""));
  } catch {
    return null;
  }
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) parsed.set(argv[index], argv[index + 1]);
  return parsed;
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
