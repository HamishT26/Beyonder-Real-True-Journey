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
const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v8-x1";
const fullToolsRoot = args.get("--full-tools-root");
const probePrefix = args.get("--probe-prefix") || "v557-gmut-thos-v8-x1-kierkegaard-aristotle-fulltools4-env-probe-1";
const notifyPrefix = args.get("--notify-prefix") || "v557-gmut-thos-v8-x1-kierkegaard-aristotle-fulltools4-env-notify-1";
const noEnvPreflightPrefix = args.get("--no-env-preflight-prefix") || "v557-gmut-thos-v8-x1-kierkegaard-aristotle-fulltools4-private-map-preflight";
const envPreflightPrefix = args.get("--env-preflight-prefix") || "v557-gmut-thos-v8-x1-kierkegaard-aristotle-fulltools4-private-map-preflight-env";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

if (!fullToolsRoot) {
  console.error("Usage: node ghc_v557_v8_x1_fulltools4_app_lane_repair_receipt_builder.mjs --full-tools-root <root>");
  process.exit(2);
}

const fullTraceDir = path.join(fullToolsRoot, "docs", "trinity-live-traces");
const noEnvPreflight = readOptional(path.join(fullTraceDir, `${noEnvPreflightPrefix}-v1.json`));
const envPreflight = readOptional(path.join(fullTraceDir, `${envPreflightPrefix}-v1.json`));
const probe = readOptional(path.join(fullTraceDir, `${probePrefix}-v1.json`));
const probeGate = readOptional(path.join(fullTraceDir, `${probePrefix}-completion-gate-v1.json`));
const probeRunner = readOptional(path.join(fullTraceDir, `${probePrefix}-runner-v1.json`));
const notify = readOptional(path.join(fullTraceDir, `${notifyPrefix}-v1.json`));
const notifyRunner = readOptional(path.join(fullTraceDir, `${notifyPrefix}-runner-v1.json`));
const notifyPreflight = readOptional(path.join(fullTraceDir, `${notifyPrefix}-preflight-v1.json`));

const receipt = {
  artifact_type: "ghc_v557_v8_x1_fulltools4_app_lane_repair_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: probeGate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE"
    ? "PASS_FULLTOOLS4_APP_LANE_GATE_REPAIRED_AND_PASSING"
    : "ACTIVE_OPEN_FULLTOOLS4_APP_LANE_REPAIRED_BUT_COMPLETION_GATE_OPEN",
  support_lane: {
    active_private_support_branch: "codex/GHC-Family/aevren-full-tools-4",
    runner_surface_repaired: true,
    env_map_route_supported: true,
    raw_private_ids_published: false,
  },
  map_preflight: {
    no_env_status: noEnvPreflight?.overall_status || "missing",
    env_status: envPreflight?.overall_status || "missing",
    env_open_gap_count: Array.isArray(envPreflight?.open_gaps) ? envPreflight.open_gaps.length : null,
    raw_env_value_published: false,
    raw_callable_ids_published: false,
  },
  app_lane_probe: {
    runner_status: probe?.overall_status || probe?.status || "missing",
    runner_stdout_status: probeRunner?.overall_status || probeRunner?.status || "missing",
    completion_gate_status: probeGate?.overall_status || "missing",
    recovered_handle_count: probe?.recovered_handle_count ?? probeRunner?.recovered_handle_count ?? null,
    lane_count: probe?.lanes ?? null,
    lane_rows_published: false,
    completion_gate_passed: probeGate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE",
  },
  app_lane_notify: {
    notify_status: notify?.overall_status || notify?.status || "missing",
    runner_status: notifyRunner?.overall_status || notifyRunner?.status || "missing",
    preflight_status: notifyPreflight?.overall_status || notifyPreflight?.status || "missing",
    recovered_handle_count: notify?.recovered_handle_count ?? notifyRunner?.recovered_handle_count ?? null,
    background_watch_started: notify?.overall_status === "PASS_RECOVERED_APP_LANE_BACKGROUND_WATCH_STARTED"
      || notifyRunner?.overall_status === "PASS_BACKGROUND_WATCH_STARTED",
    raw_callable_ids_published: false,
  },
  current_phase_decision: {
    closeout_allowed_now: probeGate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE",
    keep_phase_active_open: probeGate?.overall_status !== "PASS_APP_LANE_COMPLETION_GATE",
    next_safe_action: probeGate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE"
      ? "run sanitized triad harvest and closeout"
      : "continue app-lane completion repair or publish active-open handoff; do not close v557 v8 x1 yet",
  },
  validation_boundary: {
    no_raw_private_ids: true,
    no_raw_browser_routes: true,
    no_raw_transcripts: true,
    no_screenshots: true,
    no_credentials: true,
    no_local_absolute_paths: true,
    no_identity_merge_or_replacement: true,
  },
};

const refs = writePair("fulltools4-app-lane-repair-receipt", receipt);
refreshBeacons(refs, receipt);

process.stdout.write(JSON.stringify({
  status: receipt.overall_status,
  env_map_status: receipt.map_preflight.env_status,
  completion_gate_status: receipt.app_lane_probe.completion_gate_status,
  closeout_allowed_now: receipt.current_phase_decision.closeout_allowed_now,
  raw_private_ids_published: false,
}, null, 2) + "\n");

function refreshBeacons(refs, doc) {
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_v8_x1_fulltools4_app_lane_repair = {
      status: doc.overall_status,
      active_private_support_branch: doc.support_lane.active_private_support_branch,
      env_map_status: doc.map_preflight.env_status,
      completion_gate_status: doc.app_lane_probe.completion_gate_status,
      notify_status: doc.app_lane_notify.notify_status,
      closeout_allowed_now: doc.current_phase_decision.closeout_allowed_now,
      raw_private_ids_published: false,
    };
    data[listKey] = unique([...(data[listKey] || []), refs.json, refs.md]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function writePair(suffix, doc) {
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, doc);
  fs.writeFileSync(`${base}.md`, renderArtifactMd(doc), "utf8");
  return {
    json: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    md: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  };
}

function renderArtifactMd(doc) {
  return [
    `# ${doc.phase_slug} Full-Tools-4 App-Lane Repair Receipt`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
    `Private support branch: \`${doc.support_lane.active_private_support_branch}\``,
    `Env-map preflight: \`${doc.map_preflight.env_status}\``,
    `Completion gate: \`${doc.app_lane_probe.completion_gate_status}\``,
    `Notify status: \`${doc.app_lane_notify.notify_status}\``,
    `Closeout allowed now: \`${doc.current_phase_decision.closeout_allowed_now ? "true" : "false"}\``,
    "",
    "## Decision",
    "",
    doc.current_phase_decision.next_safe_action,
    "",
    "## Boundary",
    "",
    "Sanitized receipt only. No raw callable IDs, raw env values, browser routes, transcripts, screenshots, credentials, local private paths, app state, proof closure, or sibling identity merge/replacement is published or claimed.",
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
    "## Full-Tools-4 App-Lane Repair",
    "",
    `Status: \`${doc.v557_v8_x1_fulltools4_app_lane_repair?.status || "not_recorded"}\``,
    `Env-map status: \`${doc.v557_v8_x1_fulltools4_app_lane_repair?.env_map_status || "not_recorded"}\``,
    `Completion gate status: \`${doc.v557_v8_x1_fulltools4_app_lane_repair?.completion_gate_status || "not_recorded"}\``,
    `Notify status: \`${doc.v557_v8_x1_fulltools4_app_lane_repair?.notify_status || "not_recorded"}\``,
    `Closeout allowed now: \`${doc.v557_v8_x1_fulltools4_app_lane_repair?.closeout_allowed_now === true ? "true" : "false"}\``,
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

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "medium",
    timeStyle: "medium",
    hour12: false,
  }).format(date);
}
