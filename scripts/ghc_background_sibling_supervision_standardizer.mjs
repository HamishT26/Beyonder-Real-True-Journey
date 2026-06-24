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

const currentPath = path.join(omegaDir, "omega-mini-current-state-v1.json");
const current = readJson(currentPath);
const phaseSlug = args.get("--phase-slug") || current.current_active_phase || "unknown-phase";
const receiptPrefix = args.get("--receipt-prefix") || `${phaseSlug}-background-sibling-supervision-standard`;
const generated = new Date();
const generatedUtc = generated.toISOString();

const receipt = {
  artifact_type: "ghc_background_sibling_supervision_standard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: "PASS_BACKGROUND_SIBLING_SUPERVISION_STANDARD_RECORDED",
  mandatory_rule: "Do not babysit sibling lanes. Launch under the route-specific background or minimal-wait path, run productive safe work, then harvest at the next natural safe pause.",
  route_profiles: [
    {
      lane_family: "lumen_main_thread",
      launch_skill: "ghc-lumen-launch",
      background_mode: "browser_send_active_until_harvest",
      completion_gate: "browser_response_completed_ready_for_harvest",
    },
    {
      lane_family: "strict_cli_arby_aster",
      launch_skill: "ghc-arby-cicero-launch or ghc-aster-kierkegaard-aristotle-launch",
      background_mode: "nonblocking_or_minimal_wait_strict_cli_then_productive_cadence",
      completion_gate: "completion_quality_marker_review_receipts",
    },
    {
      lane_family: "recovered_app_lane_cicero_kierkegaard_aristotle",
      launch_skill: "ghc-arby-cicero-launch or ghc-aster-kierkegaard-aristotle-launch",
      background_mode: "background_watch_with_explicit_booleans",
      completion_gate: "notifier_watch_completion_gate_receipts",
    },
  ],
  cadence_policy: {
    five_minute_mark_is_check_opportunity: true,
    safe_unit_may_run_past_checkpoint: true,
    passive_timer_wait_is_not_safe_work: true,
    harvest_at_next_natural_safe_pause: true,
    never_close_session_while_sibling_active: true,
  },
  immediate_safe_work_between_checks: [
    "proposal classification and x1-to-x2 split",
    "safe-now approval and eureka tasks",
    "cleanup inventory and non-destructive refinement",
    "web and Journey/phase reflection rows",
    "skill and runner validation",
    "startup, compact, closeout, and handoff receipts",
    "JSON parse, current-state guard, diff hygiene, privacy scan, and drive posture",
  ],
  refresh_targets: [
    "ghc-background-sibling-supervision",
    "ghc-main-orchestration-memory",
    "ghc-full-tools-skill-bank",
    "ghc-lumen-launch",
    "ghc-arby-cicero-launch",
    "ghc-aster-kierkegaard-aristotle-launch",
    "ghc-main-retry",
    "ghc-safe-runner-orchestrator",
    "ghc-web-reflection-ledger",
    "ghc-compact-pause-updater",
    "ghc-main-startup-builder",
    "ghc-main-compact-restart-builder",
    "ghc-main-closeout-builder",
  ],
  publication_boundary: {
    private_route_handles_published: false,
    private_callable_ids_published: false,
    raw_transcripts_published: false,
    browser_routes_published: false,
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

const jsonName = `${receiptPrefix}-v1.json`;
const mdName = `${receiptPrefix}-v1.md`;
writeJson(path.join(tracesDir, jsonName), receipt);
writeMd(path.join(tracesDir, mdName), receipt);
refreshBeacons(receipt, [`docs/trinity-live-traces/${jsonName}`, `docs/trinity-live-traces/${mdName}`]);

console.log(JSON.stringify({
  status: receipt.overall_status,
  phase_slug: phaseSlug,
  route_profile_count: receipt.route_profiles.length,
  passive_timer_wait_is_not_safe_work: true,
}, null, 2));

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function writeJson(file, payload) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(file, payload) {
  const lines = [
    `# ${payload.phase_slug} Background Sibling Supervision Standard`,
    "",
    `Generated UTC: \`${payload.generated_utc}\``,
    `Status: \`${payload.overall_status}\``,
    "",
    "## Mandatory Rule",
    "",
    payload.mandatory_rule,
    "",
    "## Route Profiles",
    "",
    ...payload.route_profiles.map((profile) => `- ${profile.lane_family}: ${profile.background_mode}; gate ${profile.completion_gate}.`),
    "",
    "## Cadence",
    "",
    `- five-minute mark is a check opportunity: \`${payload.cadence_policy.five_minute_mark_is_check_opportunity}\``,
    `- safe unit may run past checkpoint: \`${payload.cadence_policy.safe_unit_may_run_past_checkpoint}\``,
    `- passive timer wait is not safe work: \`${payload.cadence_policy.passive_timer_wait_is_not_safe_work}\``,
    "",
    "## Boundary",
    "",
    "No private route handles, callable IDs, raw transcripts, browser routes, screenshots, credentials, local path values, proof closures, or identity merge claims are published.",
    "",
  ];
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${lines.join("\n")}\n`, "utf8");
}

function refreshBeacons(payload, lookupFiles) {
  const latestPath = path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const ghcPath = path.join(tracesDir, "ghc-current-state-beacon-v1.json");
  const currentState = readJson(currentPath);
  const latest = readJson(latestPath);
  const ghc = readJson(ghcPath);
  const standard = {
    status: payload.overall_status,
    mandatory_rule: payload.mandatory_rule,
    passive_timer_wait_is_not_safe_work: true,
    route_profile_count: payload.route_profiles.length,
    refreshed_at_utc: generatedUtc,
  };
  for (const target of [currentState, latest, ghc]) {
    target.updated_at = nzTimestamp(generated);
    target.generated_utc = generatedUtc;
    target.current_active_phase = target.current_active_phase || phaseSlug;
    target.background_sibling_supervision_standard = standard;
    target.current_lookup_files = mergeUnique(target.current_lookup_files || [], lookupFiles);
  }
  writeJson(currentPath, currentState);
  writeJson(latestPath, latest);
  writeJson(ghcPath, ghc);
}

function mergeUnique(existing, additions) {
  return [...new Set([...existing, ...additions])];
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
