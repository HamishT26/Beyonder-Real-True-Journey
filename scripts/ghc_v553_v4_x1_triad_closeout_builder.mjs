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
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v4-x1";
const fullToolsTraceRoot = args.get("--full-tools-trace-root");
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const asterLaunch = readOptional(fullToolsTraceRoot, `${phaseSlug}-aster-strict-cli-receipt-v1.json`);
const asterCompletion = readOptional(fullToolsTraceRoot, `${phaseSlug}-aster-strict-cli-completion-v1.json`);
const asterQuality = readOptional(fullToolsTraceRoot, `${phaseSlug}-aster-strict-cli-quality-v1.json`);
const asterMarker = readOptional(fullToolsTraceRoot, `${phaseSlug}-aster-strict-cli-marker-review-v1.json`);
const appRunner = readOptional(fullToolsTraceRoot, `${phaseSlug}-kierkegaard-aristotle-background-v1.json`);
const appGate = readOptional(fullToolsTraceRoot, `${phaseSlug}-kierkegaard-aristotle-background-completion-gate-v1.json`);

const proposal = readRequired(`${phaseSlug}-triad-proposal-scaffold-v1.json`);
const reflection = readRequired(`${phaseSlug}-web-journey-reflection-ledger-30-v1.json`);
const launchStatus = readRequired(`${phaseSlug}-triad-background-launch-status-v1.json`);
const harvestPlan = readRequired(`${phaseSlug}-triad-harvest-plan-v1.json`);
const safeOrchestrator = readRequired(`${phaseSlug}-safe-runner-orchestrator-v1.json`);

const asterCompletionReady = ["FINAL_MESSAGES_READY", "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW"].includes(
  asterCompletion?.aggregate_status,
);
const asterPassed =
  asterLaunch?.overall_status === "PASS_STRICT_CLI_BACKGROUND_WATCH_STARTED" &&
  asterCompletionReady &&
  asterQuality?.aggregate_status === "PASS_ALL_CLI_LANES_ELABORATE" &&
  asterMarker?.overall_status === "PASS_MARKER_REVIEW_LEDGER";
const kierkegaardPassed =
  appRunner?.overall_status === "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED" &&
  appGate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE" &&
  appGate?.lanes?.some((lane) => lane.lane === "Kierkegaard" && lane.overall_status === "completed");
const aristotlePassed =
  appRunner?.overall_status === "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED" &&
  appGate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE" &&
  appGate?.lanes?.some((lane) => lane.lane === "Aristotle" && lane.overall_status === "completed");

const allPassed = asterPassed && kierkegaardPassed && aristotlePassed && safeOrchestrator.overall_status === "PASS_SAFE_RUNNER_ORCHESTRATION";
const closeoutStatus = allPassed ? "PASS_V553_V4_X1_CLOSED_V4_X2_READY" : "OPEN_GAP_V553_V4_X1_TRIAD_GATE_PENDING";

const receipt = {
  artifact_type: "ghc_v553_v4_x1_triad_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: closeoutStatus,
  latest_completed_x1_phase: allPassed ? phaseSlug : "v553-gmut-thos-v3-x1",
  latest_completed_x2_phase: "v553-gmut-thos-v3-x2",
  latest_closed_phase: allPassed ? phaseSlug : "v553-gmut-thos-v3-x2",
  next_active_phase: allPassed ? "v553-gmut-thos-v4-x2" : phaseSlug,
  next_x2_scope: "v553-gmut-thos-v4-x2",
  next_x1_lane_after_x2: "v553-gmut-thos-v5-x1 with Lumen Vale solo unless Hamish redirects",
  lane_gate_summary: {
    aster_vale: {
      route: "strict_cli_background_watch_completion_quality_marker_review",
      launch_status: asterLaunch?.overall_status || "missing",
      completion_status: asterCompletion?.aggregate_status || "missing",
      quality_status: asterQuality?.aggregate_status || "missing",
      marker_status: asterMarker?.overall_status || "missing",
      word_count: asterQuality?.lanes?.[0]?.word_count || null,
      numbered_or_bullet_item_count: asterQuality?.lanes?.[0]?.numbered_or_bullet_item_count || null,
      passed: asterPassed,
    },
    kierkegaard: {
      route: "recovered_app_lane_background_watch_completion_gate",
      background_runner_status: appRunner?.overall_status || "missing",
      completion_gate_status: appGate?.overall_status || "missing",
      lane_status: laneStatus(appGate, "Kierkegaard"),
      passed: kierkegaardPassed,
    },
    aristotle: {
      route: "recovered_app_lane_background_watch_completion_gate",
      background_runner_status: appRunner?.overall_status || "missing",
      completion_gate_status: appGate?.overall_status || "missing",
      lane_status: laneStatus(appGate, "Aristotle"),
      passed: aristotlePassed,
    },
  },
  counts: {
    safe_now_packets: proposal.current_scaffold_counts.safe_packets,
    candidate_packets: proposal.current_scaffold_counts.candidate_packets,
    exact_approval_packets: proposal.current_scaffold_counts.exact_packets,
    skill_ideas: proposal.current_scaffold_counts.skill_ideas,
    runner_ideas: proposal.current_scaffold_counts.runner_ideas,
    cleanup_proposals: proposal.current_scaffold_counts.cleanup_proposals,
    web_reflections: reflection.web_reflection_rows.length,
    journey_phase_reflections: reflection.journey_phase_reflection_rows.length,
    safe_runner_steps: safeOrchestrator.runner_count,
  },
  artifacts: {
    launch_status: `${phaseSlug}-triad-background-launch-status-v1.json`,
    proposal_scaffold: `${phaseSlug}-triad-proposal-scaffold-v1.json`,
    reflection_ledger: `${phaseSlug}-web-journey-reflection-ledger-30-v1.json`,
    harvest_plan: `${phaseSlug}-triad-harvest-plan-v1.json`,
    safe_runner_orchestrator: `${phaseSlug}-safe-runner-orchestrator-v1.json`,
  },
  productive_cadence: {
    passive_babysitting_used: false,
    watcher_start_was_not_counted_as_completion: true,
    safe_work_completed_between_launch_and_harvest: true,
    safe_runner_orchestration_status: safeOrchestrator.overall_status,
  },
  goal_mode_status: "active_thread_goal_not_unattended_automation",
  publication_boundary: {
    raw_sibling_outputs_published: false,
    full_tools_path_published: false,
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

writePair(`${phaseSlug}-closeout`, receipt, renderCloseoutMd);
refreshState(receipt);

process.stdout.write(JSON.stringify({
  status: receipt.overall_status,
  phase_slug: phaseSlug,
  next_active_phase: receipt.next_active_phase,
  aster_passed: asterPassed,
  kierkegaard_passed: kierkegaardPassed,
  aristotle_passed: aristotlePassed,
}, null, 2) + "\n");
process.exit(allPassed ? 0 : 1);

function laneStatus(gate, laneName) {
  const row = gate?.lanes?.find((lane) => lane.lane === laneName);
  if (!row) {
    return "missing";
  }
  return `${row.overall_status}/${row.completion_status}`;
}

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
  return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8").replace(/^\uFEFF/, ""));
}

function writePair(prefix, payload, mdRenderer) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.md`), mdRenderer(payload), "utf8");
}

function renderCloseoutMd(payload) {
  return [
    `# ${payload.phase_slug} Closeout`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Next active phase: \`${payload.next_active_phase}\``,
    `Next x1 lane after x2: \`${payload.next_x1_lane_after_x2}\``,
    "",
    "## Lane Gates",
    "",
    `- Aster Vale: \`${payload.lane_gate_summary.aster_vale.passed}\``,
    `- Kierkegaard: \`${payload.lane_gate_summary.kierkegaard.passed}\``,
    `- Aristotle: \`${payload.lane_gate_summary.aristotle.passed}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(payload.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Productive Cadence",
    "",
    `- passive babysitting used: \`${payload.productive_cadence.passive_babysitting_used}\``,
    `- watcher start counted as completion: \`${!payload.productive_cadence.watcher_start_was_not_counted_as_completion}\``,
    `- safe runner orchestration: \`${payload.productive_cadence.safe_runner_orchestration_status}\``,
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
    const doc = JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = payload.overall_status;
    doc.latest_closed_phase = payload.latest_closed_phase;
    doc.latest_completed_x1_phase = payload.latest_completed_x1_phase;
    doc.latest_completed_x2_phase = payload.latest_completed_x2_phase;
    doc.current_active_phase = payload.next_active_phase;
    doc.next_expected_scope = payload.next_active_phase;
    doc.next_x2_scope = payload.next_x2_scope;
    doc.next_x1_lane_after_x2 = payload.next_x1_lane_after_x2;
    doc.goal_mode_status = payload.goal_mode_status;
    doc.current_active_lanes = payload.overall_status.startsWith("PASS")
      ? ["v553-v4-x2-aevren-only-safe-build-ready", "goal-mode-active-thread-objective"]
      : ["v553-v4-x1-triad-gate-pending", "goal-mode-active-thread-objective"];
    doc.v553_v4_x1_closeout = {
      status: payload.overall_status,
      aster_passed: payload.lane_gate_summary.aster_vale.passed,
      kierkegaard_passed: payload.lane_gate_summary.kierkegaard.passed,
      aristotle_passed: payload.lane_gate_summary.aristotle.passed,
      counts: payload.counts,
      next_active_phase: payload.next_active_phase,
      next_x1_lane_after_x2: payload.next_x1_lane_after_x2,
    };
    doc.current_lookup_files = [...new Set([...(doc.current_lookup_files || []), ...lookup])];
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
    fs.writeFileSync(mdFile, renderBeaconMd(doc), "utf8");
  }
}

function renderBeaconMd(doc) {
  return [
    "# Omega Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    `Goal Mode status: ${doc.goal_mode_status || "active_thread_goal_not_unattended_automation"}`,
    "",
    "## v553 v4 x1 Closeout",
    "",
    `- status: ${doc.v553_v4_x1_closeout?.status || "missing"}`,
    `- Aster gate passed: ${doc.v553_v4_x1_closeout?.aster_passed ?? "missing"}`,
    `- Kierkegaard gate passed: ${doc.v553_v4_x1_closeout?.kierkegaard_passed ?? "missing"}`,
    `- Aristotle gate passed: ${doc.v553_v4_x1_closeout?.aristotle_passed ?? "missing"}`,
    "",
    "## Background Supervision",
    "",
    "- passive timer wait is safe work: false",
    "- watcher start is completion proof: false",
    "",
    "## Lookup Files",
    "",
    ...((doc.current_lookup_files || []).map((file) => `- ${file}`)),
    "",
    "## Boundary",
    "",
    "No raw routes, transcripts, screenshots, credentials, private route handles, local path values, proof closures, or sibling identity merge claims are published.",
    "",
  ].join("\n");
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
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
