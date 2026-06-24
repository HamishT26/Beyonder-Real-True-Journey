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

const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v6-x1";
const fullToolsTraceRoot = args.get("--full-tools-trace-root");
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const proposal = readRequired(`${phaseSlug}-duo-phase-workbench-proposals-v1.json`);
const reflections = readRequired(`${phaseSlug}-duo-phase-workbench-web-journey-reflections-v1.json`);
const cadence = readRequired(`${phaseSlug}-duo-phase-workbench-safe-cadence-v1.json`);
const launchStatus = readRequired(`${phaseSlug}-duo-phase-workbench-lane-launch-status-v1.json`);
const safeOrchestrator = readRequired(`${phaseSlug}-safe-runner-orchestrator-v1.json`);
const openGateLinter = readRequired(`${phaseSlug}-open-gate-claim-linter-v1.json`);

const arbyCycle = readOptional(fullToolsTraceRoot, `${phaseSlug}-arby-strict-cli-receipt-v1.json`);
const arbyCompletion = readOptional(fullToolsTraceRoot, `${phaseSlug}-arby-strict-cli-completion-v1.json`);
const arbyQuality = readOptional(fullToolsTraceRoot, `${phaseSlug}-arby-strict-cli-quality-v1.json`);
const arbyMarker = readOptional(fullToolsTraceRoot, `${phaseSlug}-arby-strict-cli-marker-review-v1.json`);
const ciceroRunner = readOptional(fullToolsTraceRoot, `${phaseSlug}-cicero-background-v1.json`);
const ciceroGate = readOptional(fullToolsTraceRoot, `${phaseSlug}-cicero-background-completion-gate-v1.json`);

const arbyCompletionReady = ["FINAL_MESSAGES_READY", "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW"].includes(arbyCompletion?.aggregate_status);
const arbyPassed =
  arbyCycle?.overall_status === "PASS_STRICT_CLI_BACKGROUND_WATCH_STARTED" &&
  arbyCompletionReady &&
  arbyQuality?.aggregate_status === "PASS_ALL_CLI_LANES_ELABORATE" &&
  arbyMarker?.overall_status === "PASS_MARKER_REVIEW_LEDGER";
const ciceroPassed =
  ciceroRunner?.overall_status === "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED" &&
  ciceroGate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE";
const safePassed =
  safeOrchestrator?.overall_status === "PASS_SAFE_RUNNER_ORCHESTRATION" &&
  openGateLinter?.overall_status === "PASS_OPEN_GATE_CLAIM_LINTER";
const proposalPassed = proposal?.overall_status === "PASS_V553_V6_X1_DUO_PROPOSAL_LEDGER_BUILT";
const reflectionPassed = reflections?.overall_status === "PASS_V553_V6_X1_REFLECTION_LEDGER_BUILT";
const cadencePassed = cadence?.overall_status === "PASS_V553_V6_X1_SAFE_CADENCE_WORKBENCH_BUILT";
const pass = arbyPassed && ciceroPassed && safePassed && proposalPassed && reflectionPassed && cadencePassed;

const receipt = {
  artifact_type: "ghc_v553_v6_x1_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: pass ? "PASS_V553_V6_X1_CLOSED_V6_X2_READY" : "OPEN_GAP_V553_V6_X1_CLOSEOUT",
  latest_closed_phase: pass ? phaseSlug : "v553-gmut-thos-v5-x2",
  latest_completed_x1_phase: pass ? phaseSlug : "v553-gmut-thos-v5-x1",
  latest_completed_x2_phase: "v553-gmut-thos-v5-x2",
  next_active_phase: pass ? "v553-gmut-thos-v6-x2" : phaseSlug,
  next_x2_scope: "v553-gmut-thos-v6-x2",
  next_x1_lane_after_x2: "v553-gmut-thos-v7-x1 with Lumen unless Hamish redirects",
  goal_mode_readiness: {
    status: "prepared_not_unattended",
    next_candidate_phase: "v553-gmut-thos-v7-x1 or Hamish-directed goal-mode test phase",
    activation_requires_hamish_prompt: true,
  },
  lane_gate_summary: {
    arby: {
      route: "strict_cli_background_watch_then_completion_quality_marker_review",
      background_cycle_status: arbyCycle?.overall_status || "missing",
      completion_status: arbyCompletion?.aggregate_status || "missing",
      quality_status: arbyQuality?.aggregate_status || "missing",
      marker_status: arbyMarker?.overall_status || "missing",
      word_count: arbyQuality?.lanes?.[0]?.word_count || null,
      category_item_counts: arbyQuality?.lanes?.[0]?.category_item_counts || null,
      passed: arbyPassed,
    },
    cicero: {
      route: "recovered_app_lane_background_watch_then_completion_gate",
      background_runner_status: ciceroRunner?.overall_status || "missing",
      completion_gate_status: ciceroGate?.overall_status || "missing",
      passed: ciceroPassed,
    },
  },
  safe_work_summary: {
    proposal_counts: proposal.counts,
    web_reflections: reflections.web_reflection_count,
    journey_phase_reflections: reflections.journey_phase_reflection_count,
    safe_orchestrator_status: safeOrchestrator.overall_status,
    open_gate_linter_status: openGateLinter.overall_status,
    no_babysit_applied: cadence.no_babysit === true,
    completion_claimed_at_launch: launchStatus.completion_claimed === true,
  },
  x2_queue_headlines: [
    "strict CLI background harvester",
    "recovered app-lane harvest reducer",
    "goal-mode prompt fit validator",
    "private ID firewall scan",
    "v6 state correction and closeout validation pack",
  ],
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

writePair(`${phaseSlug}-closeout`, receipt, renderCloseoutMd);
refreshBeacons(receipt);

console.log(JSON.stringify({
  status: receipt.overall_status,
  phase_slug: phaseSlug,
  next_active_phase: receipt.next_active_phase,
  arby_passed: arbyPassed,
  cicero_passed: ciceroPassed,
  safe_passed: safePassed,
}, null, 2));
process.exit(pass ? 0 : 1);

function readRequired(name) {
  return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8"));
}

function readOptional(root, name) {
  if (!root) return null;
  try {
    return JSON.parse(fs.readFileSync(path.join(root, name), "utf8"));
  } catch {
    return null;
  }
}

function writePair(prefix, payload, renderMd) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.md`), renderMd(payload), "utf8");
}

function refreshBeacons(payload) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.md`,
  ];
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const doc = JSON.parse(fs.readFileSync(file, "utf8"));
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = payload.overall_status;
    doc.current_active_phase = payload.next_active_phase;
    doc.latest_closed_phase = payload.latest_closed_phase;
    doc.latest_completed_x1_phase = payload.latest_completed_x1_phase;
    doc.latest_completed_x2_phase = payload.latest_completed_x2_phase;
    doc.next_expected_scope = payload.next_active_phase;
    doc.next_x2_scope = payload.next_x2_scope;
    doc.next_x1_lane_after_x2 = payload.next_x1_lane_after_x2;
    doc.goal_mode_status = "active_thread_goal_not_unattended_automation";
    doc.v553_v6_x1_closeout = {
      status: payload.overall_status,
      arby_passed: payload.lane_gate_summary.arby.passed,
      cicero_passed: payload.lane_gate_summary.cicero.passed,
      counts: payload.safe_work_summary.proposal_counts,
      web_reflections: payload.safe_work_summary.web_reflections,
      journey_phase_reflections: payload.safe_work_summary.journey_phase_reflections,
      next_active_phase: payload.next_active_phase,
    };
    const key = file.includes("latest-updates")
      ? "latest_lookup_files"
      : file.includes("ghc-current-state")
        ? "lookup_files"
        : "current_lookup_files";
    doc[key] = [...new Set([...(doc[key] || []), ...lookup])];
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
    fs.writeFileSync(file.replace(/\.json$/, ".md"), renderBeaconMd(path.basename(file, ".json"), doc, doc[key]), "utf8");
  }
}

function renderCloseoutMd(payload) {
  return [
    `# ${payload.phase_slug} Closeout`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Next active phase: \`${payload.next_active_phase}\``,
    `Next x2 scope: \`${payload.next_x2_scope}\``,
    "",
    "## Lane Gates",
    "",
    `- Arby: \`${payload.lane_gate_summary.arby.passed}\``,
    `- Cicero: \`${payload.lane_gate_summary.cicero.passed}\``,
    "",
    "## Safe Work",
    "",
    ...Object.entries(payload.safe_work_summary.proposal_counts).map(([key, value]) => `- ${key}: \`${value}\``),
    `- web reflections: \`${payload.safe_work_summary.web_reflections}\``,
    `- Journey/phase reflections: \`${payload.safe_work_summary.journey_phase_reflections}\``,
    "",
    "## v6 x2 Queue",
    "",
    ...payload.x2_queue_headlines.map((item) => `- ${item}`),
    "",
    "## Boundary",
    "",
    "No raw sibling output, private route handle, callable ID, local path value, screenshot, credential, proof closure, deployment/account/API-key mutation, private-material proof, raw-publication proof, or identity merge claim is published.",
    "",
  ].join("\n");
}

function renderBeaconMd(title, doc, files) {
  return [
    `# ${title}`,
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next expected scope: ${doc.next_expected_scope}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## v553 v6 x1 Closeout",
    "",
    `- status: \`${doc.v553_v6_x1_closeout?.status || "not_recorded"}\``,
    `- Arby gate passed: \`${doc.v553_v6_x1_closeout?.arby_passed ?? "not_recorded"}\``,
    `- Cicero gate passed: \`${doc.v553_v6_x1_closeout?.cicero_passed ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(files || []).slice(-120).map((item) => `- \`${item}\``),
    "",
    "## Boundary",
    "",
    "No raw routes, transcripts, screenshots, credentials, private route handles, local path values, proof closures, legal/canon/deployment/account/API-key closures, private-material proof, raw-publication proof, or identity merge claims are published.",
    "",
  ].join("\n");
}

function publicationBoundary() {
  return {
    raw_transcripts_published: false,
    private_route_handles_published: false,
    private_callable_ids_published: false,
    browser_routes_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  };
}

function claimBoundary() {
  return {
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    deployment_closure: "not_claimed",
    account_api_key_purchase_mutation: "not_claimed",
    private_material_proof: "not_claimed",
    raw_publication_proof: "not_claimed",
    sibling_identity_merge_or_replacement: "not_claimed",
  };
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date).reduce((acc, part) => {
    if (part.type !== "literal") acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
