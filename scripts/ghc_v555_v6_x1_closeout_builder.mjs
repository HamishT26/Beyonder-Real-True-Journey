#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v555-gmut-thos-v6-x1";
const fullToolsTraceRoot = args.get("--full-tools-trace-root");
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const proposal = readRequired(`${phaseSlug}-arby-cicero-duo-proposals-v1.json`);
const reflection = readRequired(`${phaseSlug}-web-journey-reflection-ledger-v1.json`);
const background = readRequired(`${phaseSlug}-background-sibling-supervision-standard-v1.json`);
const cadence = readRequired(`${phaseSlug}-five-minute-productive-cadence-v1.json`);
const phaseIndex = readRequired(`${phaseSlug}-phase-status-index-v1.json`);

const arbyReceipt = readOptional(fullToolsTraceRoot, `${phaseSlug}-arby-strict-cli-receipt-v1.json`);
const arbyCompletion = readOptional(fullToolsTraceRoot, `${phaseSlug}-arby-strict-cli-completion-v1.json`);
const arbyQuality = readOptional(fullToolsTraceRoot, `${phaseSlug}-arby-strict-cli-quality-v1.json`);
const arbyMarker = readOptional(fullToolsTraceRoot, `${phaseSlug}-arby-strict-cli-marker-review-v1.json`);
const ciceroRunner = readOptional(fullToolsTraceRoot, `${phaseSlug}-cicero-recovered-app-lane-v1.json`);
const ciceroGate = readOptional(fullToolsTraceRoot, `${phaseSlug}-cicero-recovered-app-lane-completion-gate-v1.json`);

const arbyPassed =
  ["PASS_STRICT_CLI_BACKGROUND_WATCH_STARTED", "PASS_STRICT_CLI_CYCLE_READY"].includes(arbyReceipt?.overall_status) &&
  ["FINAL_MESSAGES_READY", "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW"].includes(arbyCompletion?.aggregate_status) &&
  arbyQuality?.aggregate_status === "PASS_ALL_CLI_LANES_ELABORATE" &&
  arbyMarker?.overall_status === "PASS_MARKER_REVIEW_LEDGER";
const ciceroPassed =
  ciceroRunner?.overall_status === "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED" &&
  ciceroGate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE";
const passed = arbyPassed && ciceroPassed;

const receipt = {
  artifact_type: "ghc_v555_v6_x1_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: passed ? "PASS_V555_V6_X1_CLOSED_V6_X2_READY" : "OPEN_GAP_V555_V6_X1_LANE_GATE_PENDING",
  latest_completed_x1_phase: passed ? phaseSlug : "v555-gmut-thos-v5-x1",
  latest_completed_x2_phase: "v555-gmut-thos-v5-x2",
  next_active_phase: passed ? "v555-gmut-thos-v6-x2" : phaseSlug,
  next_x2_scope: "v555-gmut-thos-v6-x2",
  next_x1_lane_after_x2: "v555-gmut-thos-v7-x1 with Lumen Vale solo unless Hamish redirects",
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
  counts: {
    safe_now_packets: proposal.counts.safe_now_packets,
    candidate_packets: proposal.counts.candidate_packets,
    exact_approval_packets: proposal.counts.exact_approval_packets,
    skill_ideas: proposal.counts.skill_ideas,
    runner_ideas: proposal.counts.runner_ideas,
    cleanup_proposals: proposal.counts.cleanup_proposals,
    web_reflections: reflection.web_reflection_count,
    journey_phase_reflections: reflection.journey_phase_reflection_count,
    live_search_sweep_count: reflection.live_search_sweep_count,
    background_route_profiles: background.route_profiles.length,
    cadence_wait_work_queues: cadence.wait_work_queues.length,
  },
  source_workbench_status: phaseIndex.overall_status,
  goal_mode_status: "active_thread_goal_not_unattended_automation",
  full_goal_complete: false,
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(passed),
  open_gates: openGates(),
};

writePair("closeout", receipt, renderMd(receipt));
if (passed) refreshState(receipt);

console.log(JSON.stringify({
  status: receipt.overall_status,
  phase_slug: phaseSlug,
  next_active_phase: receipt.next_active_phase,
  arby_passed: arbyPassed,
  cicero_passed: ciceroPassed,
  full_goal_complete: false,
}, null, 2));
process.exit(passed ? 0 : 1);

function readOptional(root, name) {
  if (!root) return null;
  try {
    return JSON.parse(fs.readFileSync(path.join(root, name), "utf8").replace(/^\uFEFF/, ""));
  } catch {
    return null;
  }
}

function readRequired(name) {
  return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8").replace(/^\uFEFF/, ""));
}

function writePair(suffix, payload, md) {
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
}

function renderMd(payload) {
  return [`# ${payload.phase_slug} Closeout`, "", `Status: \`${payload.overall_status}\``, `Next active phase: \`${payload.next_active_phase}\``, `Full goal complete: \`${payload.full_goal_complete}\``, "", "## Lane Gates", "", `- Arby: \`${payload.lane_gate_summary.arby.passed}\``, `- Cicero: \`${payload.lane_gate_summary.cicero.passed}\``, "", "## Boundary", "", "No raw sibling outputs, private route handles, local path values, screenshots, credentials, proof closures, deployment/account/API-key mutations, or identity merge claims are published.", ""].join("\n");
}

function refreshState(payload) {
  const lookup = [`docs/trinity-live-traces/${phaseSlug}-closeout-v1.json`, `docs/trinity-live-traces/${phaseSlug}-closeout-v1.md`];
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = JSON.parse(fs.readFileSync(jsonFile, "utf8").replace(/^\uFEFF/, ""));
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = payload.overall_status;
    doc.current_active_phase = payload.next_active_phase;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = phaseSlug;
    doc.latest_completed_x2_phase = payload.latest_completed_x2_phase;
    doc.next_expected_scope = payload.next_active_phase;
    doc.next_x2_scope = payload.next_x2_scope;
    doc.next_x1_lane_after_x2 = payload.next_x1_lane_after_x2;
    doc.goal_mode_status = payload.goal_mode_status;
    doc.v555_v6_x1_closeout = { status: payload.overall_status, arby_passed: payload.lane_gate_summary.arby.passed, cicero_passed: payload.lane_gate_summary.cicero.passed, counts: payload.counts, full_goal_complete: false };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    fs.writeFileSync(jsonFile, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function renderBeaconMd(doc, listKey) {
  return ["# Omega-Mini Current State", "", `Status: ${doc.status}`, `Current active phase: ${doc.current_active_phase}`, `Latest closed phase: ${doc.latest_closed_phase}`, `Latest completed x1: ${doc.latest_completed_x1_phase}`, `Latest completed x2: ${doc.latest_completed_x2_phase}`, `Next x2 scope: ${doc.next_x2_scope}`, `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`, "", "## Lookup Files", "", ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`), ""].join("\n");
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) parsed.set(argv[index], argv[index + 1]);
  return parsed;
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", { timeZone: "Pacific/Auckland", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }).formatToParts(date);
  const map = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return `${map.year}-${map.month}-${map.day}T${map.hour}:${map.minute}:${map.second}+12:00`;
}

function boundary() {
  return { raw_browser_routes_published: false, private_urls_published: false, raw_transcripts_published: false, screenshots_published: false, credentials_published: false, local_absolute_paths_published: false, session_streams_published: false, private_dumps_published: false, private_callable_ids_published: false, raw_lane_text_published: false };
}

function claimBoundary(passed) {
  return { phase_completion: passed ? phaseSlug : "not_claimed", full_goal_completion: "not_claimed", gmut_empirical_closure: "not_claimed", final_physics: "not_claimed", consciousness_proof: "not_claimed", legal_closure: "not_claimed", canon_promotion: "not_claimed", deployment_closure: "not_claimed", account_mutation: "not_claimed", purchase: "not_claimed", api_key_creation: "not_claimed", private_material_proof: "not_claimed", raw_publication_proof: "not_claimed", sibling_identity_replacement_or_merge: "not_claimed" };
}

function openGates() {
  return ["GMUT empirical closure", "final physics", "consciousness proof", "legal closure", "canon promotion", "deployment closure", "account, purchase, and API-key mutation", "private-material proof", "raw-publication proof", "sibling identity replacement, merging, or erasure"];
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}
