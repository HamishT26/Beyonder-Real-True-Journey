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
const phaseSlug = requireArg("--phase-slug");
const fullToolsRoot = requireArg("--full-tools-root");
const supportLaneLabel = requireArg("--support-lane-label");
const supportBranch = requireArg("--support-branch");
const supportHead = args.get("--support-head") || "unknown";
const probePrefix = requireArg("--probe-prefix");
const strictPrefix = args.get("--strict-prefix") || null;
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const fullTraceDir = path.join(fullToolsRoot, "docs", "trinity-live-traces");
const preflight = readOptional(path.join(fullTraceDir, `${probePrefix}-preflight-v1.json`));
const runner = readOptional(path.join(fullTraceDir, `${probePrefix}-runner-v1.json`));
const probe = readOptional(path.join(fullTraceDir, `${probePrefix}-v1.json`));
const completionGate = readOptional(path.join(fullTraceDir, `${probePrefix}-completion-gate-v1.json`));

const completionStatus = completionGate?.overall_status || completionGate?.status || "missing";
const probeStatus = probe?.overall_status || probe?.status || "missing";
const preflightStatus = preflight?.overall_status || preflight?.status || "missing";
const runnerStatus = runner?.overall_status || runner?.status || "missing";
const completionPassed = completionStatus === "PASS_APP_LANE_COMPLETION_GATE";
const strictCycle = strictPrefix ? readOptional(path.join(fullTraceDir, `${strictPrefix}-receipt-v1.json`)) : null;
const strictLauncher = strictPrefix ? readOptional(path.join(fullTraceDir, `${strictPrefix}-launcher-v1.json`)) : null;
const strictStatus = strictCycle?.overall_status || strictCycle?.status || "not_in_scope";
const strictLauncherStatus = strictLauncher?.overall_status || strictLauncher?.status || "not_in_scope";
const strictStarted = strictStatus === "PASS_STRICT_CLI_BACKGROUND_WATCH_STARTED" || strictStatus === "PASS_STRICT_CLI_CYCLE_READY";
const appStarted = probeStatus === "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED";

const receipt = {
  artifact_type: "ghc_support_app_lane_probe_mirror",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: completionPassed
    ? "PASS_SUPPORT_APP_LANE_PROBE_COMPLETION_GATE"
    : "ACTIVE_OPEN_SUPPORT_APP_LANE_PROBE_COMPLETION_GATE_OPEN",
  timestamp_workflow: {
    mirror_time_utc: generatedUtc,
    last_checkpoint_time_utc: generatedUtc,
    next_checkpoint_due_utc: new Date(Date.parse(generatedUtc) + 5 * 60 * 1000).toISOString(),
    checkpoint_interval_minutes: 5,
    checkpoint_overrun_allowed: true,
    continue_retry_refresh_repair_until_gate_or_formal_open_gap: true,
  },
  support_lane: {
    label: supportLaneLabel,
    branch: supportBranch,
    head: supportHead,
    raw_private_material_published: false,
  },
  probe_summary: {
    preflight_status: preflightStatus,
    runner_status: runnerStatus,
    probe_status: probeStatus,
    completion_gate_status: completionStatus,
    recovered_handle_count: probe?.recovered_handle_count ?? runner?.recovered_handle_count ?? null,
    lane_count: Array.isArray(probe?.lanes) ? probe.lanes.length : probe?.lanes ?? null,
    completion_gate_passed: completionPassed,
  },
  strict_cli_summary: {
    strict_prefix: strictPrefix,
    cycle_status: strictStatus,
    launcher_status: strictLauncherStatus,
    lanes: strictCycle?.lanes || strictLauncher?.lanes?.map((row) => row.lane) || [],
    background_watch_started: strictStarted,
    completion_gate_passed: strictStatus === "PASS_STRICT_CLI_CYCLE_READY",
    raw_private_material_published: false,
  },
  five_lane_summary: {
    strict_cli_lanes: strictCycle?.lanes || ["Arby", "Aster Vale"],
    recovered_app_lanes: Array.isArray(probe?.lanes) ? probe.lanes : ["Cicero", "Kierkegaard", "Aristotle"],
    strict_cli_background_started: strictStarted,
    recovered_app_background_started: appStarted,
    all_five_background_started: strictStarted && appStarted,
    all_five_completion_gates_passed: completionPassed && strictStatus === "PASS_STRICT_CLI_CYCLE_READY",
    closeout_allowed_now: completionPassed && strictStatus === "PASS_STRICT_CLI_CYCLE_READY",
  },
  phase_decision: {
    closeout_allowed_now: completionPassed && strictStatus === "PASS_STRICT_CLI_CYCLE_READY",
    keep_phase_active_open: !(completionPassed && strictStatus === "PASS_STRICT_CLI_CYCLE_READY"),
    next_safe_action: completionPassed && strictStatus === "PASS_STRICT_CLI_CYCLE_READY"
      ? "run sanitized triad harvest and closeout validation"
      : "keep v557 v8 x1 active/open; active round-robin group watchers are running or open, and completion gates are still required before closeout",
  },
  publication_boundary: {
    raw_private_ids_published: false,
    raw_env_values_published: false,
    raw_browser_routes_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
};

const refs = writePair(`${supportLaneLabel}-app-lane-probe-mirror`, receipt);
refreshBeacons(refs, receipt);

process.stdout.write(JSON.stringify({
  status: receipt.overall_status,
  support_lane_label: supportLaneLabel,
  preflight_status: preflightStatus,
  probe_status: probeStatus,
  completion_gate_status: completionStatus,
  recovered_handle_count: receipt.probe_summary.recovered_handle_count,
  closeout_allowed_now: receipt.phase_decision.closeout_allowed_now,
  raw_private_material_published: false,
}, null, 2) + "\n");

function writePair(suffix, doc) {
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, doc);
  fs.writeFileSync(`${base}.md`, renderMd(doc), "utf8");
  return {
    json: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    md: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  };
}

function refreshBeacons(refs, doc) {
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.full_tools_support_branch = supportBranch;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_support_app_lane_probe_mirror = {
      status: doc.overall_status,
      support_lane_label: doc.support_lane.label,
      support_branch: doc.support_lane.branch,
      support_head: doc.support_lane.head,
      preflight_status: doc.probe_summary.preflight_status,
      probe_status: doc.probe_summary.probe_status,
      completion_gate_status: doc.probe_summary.completion_gate_status,
      strict_cli_status: doc.strict_cli_summary.cycle_status,
      five_lane_background_started: doc.five_lane_summary.all_five_background_started,
      closeout_allowed_now: doc.phase_decision.closeout_allowed_now,
      raw_private_material_published: false,
    };
    data[listKey] = unique([...(data[listKey] || []), refs.json, refs.md]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function renderMd(doc) {
  return [
    `# ${doc.phase_slug} ${doc.support_lane.label} App-Lane Probe Mirror`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
    `Support branch: \`${doc.support_lane.branch}\``,
    `Support head: \`${doc.support_lane.head}\``,
    `Preflight: \`${doc.probe_summary.preflight_status}\``,
    `Probe: \`${doc.probe_summary.probe_status}\``,
    `Completion gate: \`${doc.probe_summary.completion_gate_status}\``,
    `Recovered handle count: \`${doc.probe_summary.recovered_handle_count ?? "unknown"}\``,
    `Strict CLI: \`${doc.strict_cli_summary.cycle_status}\``,
    `Five-lane background started: \`${doc.five_lane_summary.all_five_background_started ? "true" : "false"}\``,
    `Closeout allowed now: \`${doc.phase_decision.closeout_allowed_now ? "true" : "false"}\``,
    "",
    "## Decision",
    "",
    doc.phase_decision.next_safe_action,
    "",
    "## Boundary",
    "",
    "Sanitized mirror only. No raw callable IDs, raw env values, browser routes, transcripts, screenshots, credentials, local private paths, app state, proof closure, or sibling identity merge/replacement is published or claimed.",
    "",
  ].join("\n");
}

function renderBeaconMd(doc, listKey) {
  return [
    "# Omega-Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Branch: ${doc.branch}`,
    `Full-tools support branch: ${doc.full_tools_support_branch}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## Support App-Lane Probe Mirror",
    "",
    `Status: \`${doc.v557_support_app_lane_probe_mirror?.status || "not_recorded"}\``,
    `Support lane: \`${doc.v557_support_app_lane_probe_mirror?.support_lane_label || "not_recorded"}\``,
    `Probe status: \`${doc.v557_support_app_lane_probe_mirror?.probe_status || "not_recorded"}\``,
    `Completion gate status: \`${doc.v557_support_app_lane_probe_mirror?.completion_gate_status || "not_recorded"}\``,
    `Strict CLI status: \`${doc.v557_support_app_lane_probe_mirror?.strict_cli_status || "not_recorded"}\``,
    `Five-lane background started: \`${doc.v557_support_app_lane_probe_mirror?.five_lane_background_started === true ? "true" : "false"}\``,
    `Closeout allowed now: \`${doc.v557_support_app_lane_probe_mirror?.closeout_allowed_now === true ? "true" : "false"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-240).map((ref) => `- ${ref}`),
    "",
  ].join("\n");
}

function readOptional(file) {
  try {
    return readJson(file);
  } catch {
    return null;
  }
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function parseArgs(argv) {
  const out = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      out.set(key, "true");
    } else {
      out.set(key, value);
      index += 1;
    }
  }
  return out;
}

function requireArg(name) {
  const value = args.get(name);
  if (!value) {
    console.error(`Missing required argument ${name}`);
    process.exit(2);
  }
  return value;
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "medium",
    timeStyle: "medium",
    hourCycle: "h23",
  }).format(date);
}
