#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v2-x1";
const fullToolsTraceRoot = args.get("--full-tools-trace-root");
const generated = new Date();
const generatedUtc = generated.toISOString();

const arbyReceipt = readOptional(fullToolsTraceRoot, "v553-gmut-thos-v2-x1-arby-strict-cli-receipt-v1.json");
const arbyCompletion = readOptional(fullToolsTraceRoot, "v553-gmut-thos-v2-x1-arby-strict-cli-completion-v1.json");
const arbyQuality = readOptional(fullToolsTraceRoot, "v553-gmut-thos-v2-x1-arby-strict-cli-quality-v1.json");
const arbyMarker = readOptional(fullToolsTraceRoot, "v553-gmut-thos-v2-x1-arby-strict-cli-marker-review-v1.json");
const ciceroRunner = readOptional(fullToolsTraceRoot, "v553-gmut-thos-v2-x1-cicero-background-v1.json");
const ciceroGate = readOptional(fullToolsTraceRoot, "v553-gmut-thos-v2-x1-cicero-background-completion-gate-v1.json");

const arbyPassed =
  arbyReceipt?.overall_status === "PASS_STRICT_CLI_CYCLE_READY" &&
  arbyCompletion?.aggregate_status === "FINAL_MESSAGES_READY" &&
  arbyQuality?.aggregate_status === "PASS_ALL_CLI_LANES_ELABORATE" &&
  arbyMarker?.overall_status === "PASS_MARKER_REVIEW_LEDGER";
const ciceroPassed =
  ciceroRunner?.overall_status === "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED" &&
  ciceroGate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE";

const proposal = readRequired(`${phaseSlug}-arby-cicero-duo-proposals-v1.json`);
const reflection = readRequired(`${phaseSlug}-web-journey-reflection-ledger-v1.json`);
const background = readRequired(`${phaseSlug}-background-sibling-supervision-standard-v1.json`);
const cadence = readRequired(`${phaseSlug}-five-minute-productive-cadence-v1.json`);

const closeoutStatus = arbyPassed && ciceroPassed
  ? "PASS_V553_V2_X1_CLOSED_V2_X2_READY"
  : "OPEN_GAP_V553_V2_X1_LANE_GATE_PENDING";

const receipt = {
  artifact_type: "ghc_v553_v2_x1_closeout",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: closeoutStatus,
  latest_completed_x1_phase: closeoutStatus.startsWith("PASS") ? phaseSlug : "v553-gmut-thos-v1-x1",
  next_active_phase: closeoutStatus.startsWith("PASS") ? "v553-gmut-thos-v2-x2" : phaseSlug,
  next_x2_scope: "v553-gmut-thos-v2-x2",
  next_x1_lane_after_x2: "v553-gmut-thos-v3-x1 with Lumen Vale solo unless Hamish redirects",
  lane_gate_summary: {
    arby: {
      route: "strict_cli_completion_quality_marker_review",
      strict_cli_cycle_status: arbyReceipt?.overall_status || "missing",
      completion_status: arbyCompletion?.aggregate_status || "missing",
      quality_status: arbyQuality?.aggregate_status || "missing",
      marker_status: arbyMarker?.overall_status || "missing",
      passed: arbyPassed,
    },
    cicero: {
      route: "recovered_app_lane_background_watch_completion_gate",
      background_runner_status: ciceroRunner?.overall_status || "missing",
      completion_gate_status: ciceroGate?.overall_status || "missing",
      passed: ciceroPassed,
    },
  },
  artifacts: {
    proposal_ledger: `${phaseSlug}-arby-cicero-duo-proposals-v1.json`,
    reflection_ledger: `${phaseSlug}-web-journey-reflection-ledger-v1.json`,
    background_supervision_standard: `${phaseSlug}-background-sibling-supervision-standard-v1.json`,
    productive_cadence: `${phaseSlug}-five-minute-productive-cadence-v1.json`,
  },
  counts: {
    safe_now_packets: proposal.counts.safe_now_packets,
    candidate_packets: proposal.counts.candidate_packets,
    exact_approval_packets: proposal.counts.exact_approval_packets,
    skill_ideas: proposal.counts.skill_ideas,
    runner_ideas: proposal.counts.runner_ideas,
    cleanup_proposals: proposal.counts.cleanup_proposals,
    web_reflections: reflection.web_reflection_count,
    journey_phase_reflections: reflection.journey_phase_reflection_count,
    background_route_profiles: background.route_profiles.length,
    cadence_wait_work_queues: cadence.wait_work_queues.length,
  },
  goal_mode_readiness: {
    status: "prepared_not_active",
    next_candidate_start: "v553-gmut-thos-v3-x1",
    activation_requires_hamish_goal_mode_start: true,
  },
  publication_boundary: {
    full_tools_path_published: false,
    raw_sibling_outputs_published: false,
    private_route_handles_published: false,
    private_callable_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
  open_gates: [
    "GMUT empirical closure",
    "final physics",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment closure",
    "account/API-key/purchase mutation",
    "private-material proof",
    "raw-publication proof",
    "sibling identity replacement or merge",
  ],
};

writePair(`${phaseSlug}-closeout`, receipt, renderMd);
refreshState(receipt);
console.log(JSON.stringify({
  status: receipt.overall_status,
  phase_slug: phaseSlug,
  next_active_phase: receipt.next_active_phase,
  arby_passed: arbyPassed,
  cicero_passed: ciceroPassed,
}, null, 2));
process.exit(closeoutStatus.startsWith("PASS") ? 0 : 1);

function readOptional(root, name) {
  if (!root) {
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(path.join(root, name), "utf8"));
  } catch {
    return null;
  }
}

function readRequired(name) {
  return parseJsonFile(path.join(tracesDir, name));
}

function writePair(prefix, payload, mdRenderer) {
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.md`), mdRenderer(payload), "utf8");
}

function renderMd(payload) {
  return [
    `# ${payload.phase_slug} Closeout`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Next active phase: \`${payload.next_active_phase}\``,
    "",
    "## Lane Gates",
    "",
    `- Arby: \`${payload.lane_gate_summary.arby.passed}\``,
    `- Cicero: \`${payload.lane_gate_summary.cicero.passed}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(payload.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Goal Mode",
    "",
    `- status: \`${payload.goal_mode_readiness.status}\``,
    `- activation requires Hamish start: \`${payload.goal_mode_readiness.activation_requires_hamish_goal_mode_start}\``,
    "",
    "## Boundary",
    "",
    "No raw sibling outputs, private route handles, local path values, screenshots, credentials, proof closures, deployment/account/API-key mutations, or identity merge claims are published.",
    "",
  ].join("\n");
}

function refreshState(payload) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.md`,
  ];
  const beaconPairs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md")],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md")],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md")],
  ];
  for (const [file, mdFile] of beaconPairs) {
    const doc = parseJsonFile(file);
    doc.updated_at = nzTimestamp(generated);
    doc.generated_utc = generatedUtc;
    doc.status = payload.overall_status;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = payload.latest_completed_x1_phase;
    doc.current_active_phase = payload.next_active_phase;
    doc.next_expected_scope = payload.next_active_phase;
    doc.next_x2_scope = payload.next_x2_scope;
    doc.next_x1_lane_after_x2 = payload.next_x1_lane_after_x2;
    doc.goal_mode_status = payload.goal_mode_readiness.status;
    doc.v553_v2_x1_closeout = {
      status: payload.overall_status,
      arby_passed: payload.lane_gate_summary.arby.passed,
      cicero_passed: payload.lane_gate_summary.cicero.passed,
      counts: payload.counts,
    };
    doc.current_lookup_files = [...new Set([...(doc.current_lookup_files || []), ...lookup])];
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
    fs.writeFileSync(mdFile, renderBeaconMd(doc), "utf8");
  }
}

function renderBeaconMd(doc) {
  const lines = [
    "# Omega Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    `Goal Mode status: ${doc.goal_mode_status || "prepared_not_active"}`,
    "",
    "## v553 v2 x1 Closeout",
    "",
    `- status: ${doc.v553_v2_x1_closeout?.status || "missing"}`,
    `- Arby gate passed: ${doc.v553_v2_x1_closeout?.arby_passed ?? "missing"}`,
    `- Cicero gate passed: ${doc.v553_v2_x1_closeout?.cicero_passed ?? "missing"}`,
    "",
    "## Background Supervision",
    "",
    `- status: ${doc.background_sibling_supervision_standard?.status || "missing"}`,
    `- passive timer wait is safe work: false`,
    "",
    "## Lookup Files",
    "",
    ...((doc.current_lookup_files || []).map((file) => `- ${file}`)),
    "",
    "## Boundary",
    "",
    "No raw routes, transcripts, screenshots, credentials, private route handles, local path values, proof closures, or sibling identity merge claims are published.",
    "",
  ];
  return lines.join("\n");
}

function parseJsonFile(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
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
