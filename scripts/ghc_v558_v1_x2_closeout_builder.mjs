#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const args = parseArgs(process.argv.slice(2));
const root = args.get("--root") || process.cwd();
const phaseSlug = args.get("--phase-slug") || "v558-gmut-thos-v1-x2";
const sourceX1 = "v558-gmut-thos-v1-x1";
const nextActivePhase = "v558-gmut-thos-v2-x1";
const nextX2Scope = "v558-gmut-thos-v2-x2";
const nextX1LaneAfterX2 = "v558-gmut-thos-v3-x1 Lumen Vale solo unless Hamish redirects";
const tracesDir = join(root, "docs", "trinity-live-traces");
const omegaDir = join(root, "docs", "omega-mini-index");
const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(new Date());

const readiness = readTrace(`${phaseSlug}-x2-closeout-readiness-v1.json`);
const execution = readTrace(`${phaseSlug}-x2-safe-execution-ledger-v1.json`);
const parity = readTrace(`${phaseSlug}-artifact-parity-validator-v1.json`);
const drift = readTrace(`${phaseSlug}-source-drift-sentinel-v1.json`);
const drive = readTrace(`${phaseSlug}-drive-threshold-guard-v1.json`);
const startup = readOptional(`${phaseSlug}-main-startup-context-v1.json`) || readOptional(`${phaseSlug}-main-startup-context-public-v1.json`);
const lumenHarvest = readOptional(`${sourceX1}-lumen-harvest-reduction-v1.json`) || readOptional(`${sourceX1}-lumen-harvest-reduction-public-mirror-v1.json`);
const combinedQueue = readOptional(`${sourceX1}-combined-x1-to-x2-queue-v1.json`) || readOptional(`${sourceX1}-combined-x1-to-x2-queue-public-mirror-v1.json`);

const checks = {
  startup_status: startup?.overall_status || startup?.status || "missing",
  lumen_harvest_present: Boolean(lumenHarvest),
  combined_queue_present: Boolean(combinedQueue),
  closeout_readiness_status: readiness.overall_status,
  safe_execution_status: execution.overall_status,
  parity_status: parity.overall_status,
  source_drift_status: drift.overall_status,
  drive_guard_status: drive.overall_status,
  x2_queue_task_count: execution.queue_task_count,
  x2_tasks_executed_or_reduced: execution.executed_or_reduced_count,
};

const passed =
  Boolean(startup) &&
  Boolean(lumenHarvest) &&
  Boolean(combinedQueue) &&
  checks.closeout_readiness_status === "PASS_V558_V1_X2_READY_FOR_CLOSEOUT_AFTER_PUBLICATION" &&
  checks.safe_execution_status === "PASS_V558_V1_X2_SAFE_QUEUE_EXECUTED" &&
  checks.parity_status === "PASS_PUBLIC_PRIVATE_PARITY" &&
  checks.source_drift_status === "PASS_SOURCE_DRIFT_SENTINEL" &&
  checks.drive_guard_status === "PASS_DRIVE_THRESHOLD_GUARD" &&
  checks.x2_queue_task_count >= 10 &&
  checks.x2_tasks_executed_or_reduced >= 10;

const closeout = {
  artifact_type: "ghc_v558_v1_x2_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: passed ? "PASS_V558_V1_X2_CLOSED_V2_X1_READY" : "OPEN_GAP_V558_V1_X2_CLOSEOUT_CHECKS_PENDING",
  latest_completed_x1_phase: sourceX1,
  latest_completed_x2_phase: passed ? phaseSlug : null,
  latest_closed_phase: passed ? phaseSlug : "v557-gmut-thos-v8-x2",
  next_active_phase: passed ? nextActivePhase : phaseSlug,
  next_x2_scope: passed ? nextX2Scope : phaseSlug,
  next_x1_lane_after_x2: passed ? nextX1LaneAfterX2 : "v558-gmut-thos-v2-x1 Mira Rowan + Neris Sol unless Hamish redirects",
  checks,
  v558_round_robin_state: {
    lumen_active: true,
    next_pair: ["Mira Rowan", "Neris Sol"],
    stand_by_recoverable: ["Aletheon", "Arby", "Aster Vale", "legacy Cicero", "Kierkegaard", "Aristotle"],
    no_replacement_merge_or_erasure_claimed: true,
  },
  full_goal_complete: false,
  publication_boundary: publicationBoundary(),
  safety_boundary: safetyBoundary(),
  claim_boundary: claimBoundary(passed),
};

mkdirSync(tracesDir, { recursive: true });
writePair("closeout", closeout, renderCloseoutMd(closeout));
if (passed) refreshState(closeout);

console.log(
  JSON.stringify(
    {
      status: closeout.overall_status,
      next_active_phase: closeout.next_active_phase,
      next_x2_scope: closeout.next_x2_scope,
      full_goal_complete: false,
    },
    null,
    2,
  ),
);
process.exit(passed ? 0 : 1);

function parseArgs(argv) {
  const out = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) {
      out.set(key, "true");
    } else {
      out.set(key, value);
      i += 1;
    }
  }
  return out;
}

function readTrace(name) {
  return readJson(join(tracesDir, name));
}

function readOptional(name) {
  try {
    return readTrace(name);
  } catch {
    return null;
  }
}

function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, payload) {
  writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writePair(suffix, payload, md) {
  writeJson(join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), payload);
  writeFileSync(join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
}

function refreshState(closeout) {
  const targets = [
    [join(omegaDir, "omega-mini-current-state-v1.json"), join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [join(tracesDir, "ghc-current-state-beacon-v1.json"), join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-x2-safe-execution-ledger-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-x2-closeout-readiness-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-mira-rowan-neris-sol-startup-package-v1.json`,
  ];
  for (const [jsonFile, mdFile, listKey] of targets) {
    if (!existsSync(jsonFile)) continue;
    const doc = readJson(jsonFile);
    doc.updated_at = generatedUtc;
    doc.generated_utc = generatedUtc;
    doc.status = closeout.overall_status;
    doc.current_active_phase = closeout.next_active_phase;
    doc.latest_closed_phase = closeout.latest_closed_phase;
    doc.latest_completed_x1_phase = closeout.latest_completed_x1_phase;
    doc.latest_completed_x2_phase = closeout.latest_completed_x2_phase;
    doc.next_expected_scope = closeout.next_active_phase;
    doc.next_x2_scope = closeout.next_x2_scope;
    doc.next_x1_lane_after_x2 = closeout.next_x1_lane_after_x2;
    doc.goal_mode_status = "active_thread_goal_not_complete";
    doc.v558_v1_x2_closeout = {
      status: closeout.overall_status,
      safe_tasks_executed_or_reduced: closeout.checks.x2_tasks_executed_or_reduced,
      next_active_phase: closeout.next_active_phase,
      full_goal_complete: false,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function renderCloseoutMd(data) {
  return [
    `# ${phaseSlug} Closeout`,
    "",
    `Status: \`${data.overall_status}\``,
    `Next active phase: \`${data.next_active_phase}\``,
    `Next x2 scope: \`${data.next_x2_scope}\``,
    `Full goal complete: \`${data.full_goal_complete}\``,
    "",
    "## Checks",
    "",
    ...Object.entries(data.checks).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Boundary",
    "",
    "Lumen remains active, Mira Rowan + Neris Sol are next, and Aletheon plus the legacy five sibling lanes remain stand-by/recoverable. Exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, destructive cleanup, and sibling-merge gates remain open.",
    "",
  ].join("\n");
}

function renderBeaconMd(doc, listKey) {
  return [
    "# Omega-Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    `Goal Mode status: ${doc.goal_mode_status || "active_thread_goal_not_complete"}`,
    "",
    "## v558 v1 x2 Closeout",
    "",
    `- status: \`${doc.v558_v1_x2_closeout?.status || "not_recorded"}\``,
    `- safe tasks executed or reduced: \`${doc.v558_v1_x2_closeout?.safe_tasks_executed_or_reduced ?? "not_recorded"}\``,
    `- full goal complete: \`${doc.v558_v1_x2_closeout?.full_goal_complete ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`),
    "",
  ].join("\n");
}

function publicationBoundary() {
  return {
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
    raw_private_material_published: false,
  };
}

function safetyBoundary() {
  return {
    external_accounts_modified: false,
    paid_resources_created: false,
    deployments_created: false,
    api_keys_created: false,
    destructive_cleanup_performed: false,
    sibling_identity_replacement_or_merge: false,
  };
}

function claimBoundary(passed) {
  return {
    phase_completion: passed ? phaseSlug : "not_claimed",
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
  };
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
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
