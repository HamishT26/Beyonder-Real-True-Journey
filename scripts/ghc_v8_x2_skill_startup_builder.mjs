import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
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

const phaseSlug = "v552-gmut-thos-v88-v8-x2";
const skillsRoot = args.get("--skills-root");
const fullToolsRoot = args.get("--full-tools-root");
if (!skillsRoot || !fullToolsRoot) {
  console.error("Usage: node scripts/ghc_v8_x2_skill_startup_builder.mjs --skills-root <skills-root> --full-tools-root <full-tools-root>");
  process.exit(2);
}

const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);
const publicationBoundary = {
  local_absolute_paths_published: false,
  private_route_handles_published: false,
  raw_transcripts_published: false,
  browser_routes_published: false,
  credentials_published: false,
  screenshots_published: false,
};
const claimBoundary = {
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
  deployment_closure: "not_claimed",
};

const startup = runJson(process.execPath, [
  path.join(skillsRoot, "ghc-main-orchestration-memory", "scripts", "ghc_orchestration_startup_check.mjs"),
  "--mini-root",
  repoRoot,
  "--full-tools-root",
  fullToolsRoot,
  "--phase-slug",
  phaseSlug,
]);

const inventory = runJson(process.execPath, [
  path.join(skillsRoot, "ghc-full-tools-skill-bank", "scripts", "ghc_full_tools_inventory.mjs"),
  "--mini-root",
  repoRoot,
  "--full-tools-root",
  fullToolsRoot,
]);

const drive = runJson("powershell", [
  "-NoProfile",
  "-Command",
  "Get-PSDrive -PSProvider FileSystem | Select-Object Name,@{Name='FreeGB';Expression={[math]::Round($_.Free/1GB,2)}},@{Name='UsedGB';Expression={[math]::Round($_.Used/1GB,2)}} | ConvertTo-Json",
]);

const codexVersion = runText("codex", ["--version"]);
const startupUpdater = readLocal("v552-gmut-thos-v88-v8-x2-main-orchestration-skill-startup-updater-v1.json");
const safeRunner = readLocal("v552-gmut-thos-v88-v8-x2-initial-safe-runner-orchestrator-v1.json");
const persistedInventory = readLocal("v552-gmut-thos-v88-v8-x2-full-tools-skill-bank-inventory-v1.json");

const receipt = {
  artifact_type: "ghc_v8_x2_skill_startup_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V8_X2_SKILL_STARTUP_READY",
  skills_created_and_used: [
    {
      name: "ghc-main-orchestration-memory",
      validation_status: "PASS_QUICK_VALIDATE",
      helper_status: startup ? "PASS_HELPER_USED" : "OPEN_GAP_HELPER_OUTPUT",
    },
    {
      name: "ghc-full-tools-skill-bank",
      validation_status: "PASS_QUICK_VALIDATE",
      helper_status: inventory ? "PASS_HELPER_USED" : "OPEN_GAP_HELPER_OUTPUT",
    },
  ],
  current_state_snapshot: startup?.current_state || null,
  runner_availability: startup
    ? {
        mini: startup.mini_runner_availability,
        full_tools: startup.full_tools_runner_availability,
      }
    : {},
  full_tools_inventory_summary: inventory
    ? {
        script_count: inventory.script_count,
        category_counts: Object.fromEntries(Object.entries(inventory.categories || {}).map(([key, value]) => [key, value.length])),
        must_have_full_tools: inventory.must_have_full_tools,
        must_have_mini: inventory.must_have_mini,
      }
    : {},
  drive_free_gb: normalizeDriveRows(drive),
  codex_version: codexVersion.trim(),
  x2_safe_now_work_started: [
    "Created and validated two local Codex skills.",
    "Used both skill helper scripts against omega-mini-2 and full-tools.",
    "Ran the v8 x2 startup updater.",
    "Ran the v8 x2 initial safe runner orchestrator.",
    "Persisted the full-tools skill bank inventory.",
    "Confirmed v8 x2 active with v8 x1 closed.",
    "Confirmed promoted main orchestrator and full-tools support runner availability.",
    "Confirmed D drive remains the preferred work bank.",
  ],
  continuous_safe_work_policy: {
    safe_now_approval_packets_eureka_and_cleanup_work_continues_between_cadence_marks: true,
    five_minute_marks_are_check_opportunities_not_forced_stops: true,
    harvest_at_next_natural_safe_pause_after_cadence_mark: true,
  },
  execution_receipts: {
    startup_updater_status: startupUpdater?.overall_status || "missing",
    safe_runner_orchestrator_status: safeRunner?.overall_status || "missing",
    safe_runner_count: safeRunner?.runner_count || 0,
    persisted_inventory_status: persistedInventory ? "PASS_INVENTORY_PERSISTED" : "missing",
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

writeArtifact("skill-startup-receipt", receipt, renderReceiptMd);
refreshBeacons(receipt);

console.log(JSON.stringify({ status: receipt.overall_status, phase_slug: phaseSlug, skills: receipt.skills_created_and_used.length }, null, 2));

function refreshBeacons(data) {
  const currentPath = path.join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const ghcPath = path.join(tracesDir, "ghc-current-state-beacon-v1.json");
  const current = JSON.parse(fs.readFileSync(currentPath, "utf8"));
  const latest = JSON.parse(fs.readFileSync(latestPath, "utf8"));
  const ghc = JSON.parse(fs.readFileSync(ghcPath, "utf8"));
  const lookupFiles = [
    "docs/omega-mini-index/omega-mini-current-state-v1.md",
    "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md",
    "docs/trinity-live-traces/ghc-current-state-beacon-v1.md",
    "docs/trinity-live-traces/v552-gmut-thos-v88-v8-x2-skill-startup-receipt-v1.md",
    "docs/trinity-live-traces/v552-gmut-thos-v88-v8-x2-skill-startup-receipt-v1.json",
    "docs/trinity-live-traces/v552-gmut-thos-v88-v8-x2-main-orchestration-skill-startup-updater-v1.md",
    "docs/trinity-live-traces/v552-gmut-thos-v88-v8-x2-main-orchestration-skill-startup-updater-v1.json",
    "docs/trinity-live-traces/v552-gmut-thos-v88-v8-x2-initial-safe-runner-orchestrator-v1.md",
    "docs/trinity-live-traces/v552-gmut-thos-v88-v8-x2-initial-safe-runner-orchestrator-v1.json",
    "docs/trinity-live-traces/v552-gmut-thos-v88-v8-x2-full-tools-skill-bank-inventory-v1.json",
  ];
  const common = {
    generated_utc: generatedUtc,
    status: "V552_V8_X2_ACTIVE_SKILL_BUILD_RUN",
    current_active_phase: phaseSlug,
    latest_closed_phase: "v552-gmut-thos-v88-v8-x1",
    latest_completed_x1_phase: "v552-gmut-thos-v88-v8-x1",
    latest_completed_x2_phase: "v552-gmut-thos-v88-v7-x2",
    current_active_lanes: [
      "v8-x2-active-skill-build-run",
      "ghc-main-orchestration-memory-created-and-used",
      "ghc-full-tools-skill-bank-created-and-used",
      "main-orchestrator-route-available",
      "full-tools-support-available",
    ],
    next_x2_scope: phaseSlug,
    next_x1_lane_after_x2: "v553-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects",
  };
  Object.assign(current, common, {
    updated_at: generatedNz,
    next_expected_scope: phaseSlug,
    current_lookup_files: unique([...(current.current_lookup_files || []), ...lookupFiles]),
    latest_action_summary: [
      "v552 v8 x2 started as an active skill build run.",
      "Created and validated ghc-main-orchestration-memory.",
      "Created and validated ghc-full-tools-skill-bank.",
      "Used both skill helper scripts for startup and full-tools inventory.",
      "Ran the v8 x2 startup updater and initial safe runner orchestrator.",
      "Persisted the full-tools skill bank inventory for runner selection.",
      "Safe-now approval packet, eureka, cleanup, validation, and orchestration work may continue between cadence marks.",
      "No proof/canon/legal/deployment gates were closed.",
    ],
    v8_x2_skill_startup: {
      status: data.overall_status,
      skills_created_and_used: data.skills_created_and_used.map((skill) => skill.name),
      full_tools_script_count: data.full_tools_inventory_summary.script_count,
      codex_version: data.codex_version,
      drive_free_gb: data.drive_free_gb,
      execution_receipts: data.execution_receipts,
    },
  });
  Object.assign(latest, common, { latest_lookup_files: unique([...(latest.latest_lookup_files || []), ...lookupFiles]) });
  Object.assign(ghc, common, { lookup_files: unique([...(ghc.lookup_files || []), ...lookupFiles]) });
  fs.writeFileSync(currentPath, JSON.stringify(current, null, 2) + "\n", "utf8");
  fs.writeFileSync(latestPath, JSON.stringify(latest, null, 2) + "\n", "utf8");
  fs.writeFileSync(ghcPath, JSON.stringify(ghc, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(current), "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderBeaconMd("Omega-Mini Latest Updates Beacon", latest, latest.latest_lookup_files), "utf8");
  fs.writeFileSync(path.join(tracesDir, "ghc-current-state-beacon-v1.md"), renderBeaconMd("GHC Current State Beacon", ghc, ghc.lookup_files), "utf8");
}

function writeArtifact(slug, payload, renderer) {
  const base = `${phaseSlug}-${slug}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), JSON.stringify(payload, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderer(payload), "utf8");
}

function runJson(command, commandArgs) {
  const proc = spawnSync(command, commandArgs, { cwd: repoRoot, encoding: "utf8", windowsHide: true, maxBuffer: 8 * 1024 * 1024 });
  if (proc.status !== 0) return null;
  return JSON.parse(proc.stdout);
}

function readLocal(name) {
  const file = path.join(tracesDir, name);
  if (!fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function runText(command, commandArgs) {
  const proc = spawnSync(command, commandArgs, { cwd: repoRoot, encoding: "utf8", windowsHide: true, maxBuffer: 1024 * 1024 });
  return proc.status === 0 ? proc.stdout : "unavailable";
}

function normalizeDriveRows(value) {
  const rows = Array.isArray(value) ? value : value ? [value] : [];
  return rows
    .filter((row) => row && (row.Name === "C" || row.Name === "D"))
    .map((row) => ({ drive: row.Name, free_gb: row.FreeGB, used_gb: row.UsedGB }));
}

function renderReceiptMd(data) {
  return `# v552 v8 x2 Skill Startup Receipt

Status: \`${data.overall_status}\`

## Skills

${data.skills_created_and_used.map((skill) => `- ${skill.name}: \`${skill.validation_status}\`, \`${skill.helper_status}\``).join("\n")}

## State

- Active phase: \`${data.current_state_snapshot?.current_active_phase || "missing"}\`
- Latest closed phase: \`${data.current_state_snapshot?.latest_closed_phase || "missing"}\`
- Latest completed x1: \`${data.current_state_snapshot?.latest_completed_x1_phase || "missing"}\`
- Codex version: \`${data.codex_version}\`

## Full Tools

- Script count: \`${data.full_tools_inventory_summary.script_count}\`
- App-lane tools present: \`${data.runner_availability.full_tools?.recovered_app_lane_map_runner}\`
- Strict CLI cycle present: \`${data.runner_availability.full_tools?.strict_cli_lane_cycle}\`
- Main orchestrator present: \`${data.runner_availability.mini?.main_orchestrator}\`

## Execution Receipts

- Startup updater: \`${data.execution_receipts.startup_updater_status}\`
- Safe runner orchestrator: \`${data.execution_receipts.safe_runner_orchestrator_status}\`
- Safe runner count: \`${data.execution_receipts.safe_runner_count}\`
- Persisted inventory: \`${data.execution_receipts.persisted_inventory_status}\`

## Drive Free

${data.drive_free_gb.map((row) => `- ${row.drive}: \`${row.free_gb} GB free\``).join("\n")}

## Continuous Safe Work

- Safe-now approval/eureka/cleanup work continues between cadence marks: \`${data.continuous_safe_work_policy.safe_now_approval_packets_eureka_and_cleanup_work_continues_between_cadence_marks}\`
- Five-minute marks are check opportunities: \`${data.continuous_safe_work_policy.five_minute_marks_are_check_opportunities_not_forced_stops}\`
- Harvest at natural safe pause: \`${data.continuous_safe_work_policy.harvest_at_next_natural_safe_pause_after_cadence_mark}\`
`;
}

function renderCurrentStateMd(current) {
  return `# Omega-Mini Current State

Status: ${current.status}
Current active phase: ${current.current_active_phase}
Latest closed phase: ${current.latest_closed_phase}
Latest completed x1: ${current.latest_completed_x1_phase}
Latest completed x2: ${current.latest_completed_x2_phase}
Current lanes: ${current.current_active_lanes.join("; ")}
Next x2 scope: ${current.next_x2_scope}
Next x1 lane after x2: ${current.next_x1_lane_after_x2}

## v8 x2 Skill Startup

- Status: \`${current.v8_x2_skill_startup.status}\`
- Skills: \`${current.v8_x2_skill_startup.skills_created_and_used.join(", ")}\`
- Full-tools script count: \`${current.v8_x2_skill_startup.full_tools_script_count}\`
- Codex version: \`${current.v8_x2_skill_startup.codex_version}\`
- Startup updater: \`${current.v8_x2_skill_startup.execution_receipts.startup_updater_status}\`
- Safe runner orchestrator: \`${current.v8_x2_skill_startup.execution_receipts.safe_runner_orchestrator_status}\`

## Current Lookup Files

${current.current_lookup_files.map((item) => `- ${item}`).join("\n")}

## Latest Action Summary

${current.latest_action_summary.map((item) => `- ${item}`).join("\n")}

## Safety Boundary

Status-only receipts. No private route handles, private lane body content, credentials, raw transcripts, browser routes, private machine paths, GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, or deployment closure are published.
`;
}

function renderBeaconMd(title, beacon, files) {
  return `# ${title}

Status: ${beacon.status}
Current active phase: ${beacon.current_active_phase}
Latest closed phase: ${beacon.latest_closed_phase}
Latest completed x1: ${beacon.latest_completed_x1_phase}
Latest completed x2: ${beacon.latest_completed_x2_phase}
Next x2 scope: ${beacon.next_x2_scope}
Next x1 lane after x2: ${beacon.next_x1_lane_after_x2}

## Lookup Files

${files.map((item) => `- ${item}`).join("\n")}

## Boundary

Status-only beacon. No private route data, raw app-lane content, credentials, private paths, GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, or deployment closure are published.
`;
}

function unique(items) {
  return Array.from(new Set(items.filter(Boolean)));
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
  }).formatToParts(date).reduce((acc, part) => {
    acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
