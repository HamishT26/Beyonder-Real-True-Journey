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
const receiptPrefix = args.get("--receipt-prefix") || `${phaseSlug}-arby-cicero-duo-proposals`;
const generated = new Date();
const generatedUtc = generated.toISOString();

const safe = [
  ["Aevren", "Background supervision receipt refresh", "Publish the no-babysitting standard into current-state and launch skills."],
  ["Aevren", "Strict CLI background-watch posture", "Use nonblocking/minimal-wait strict CLI launches and harvest gates later."],
  ["Aevren", "Recovered app-lane boolean guard", "Require explicit background-watch and resume-timeout booleans for app-lane runs."],
  ["Aevren", "Duo x1 count guard", "Reconcile Arby/Cicero proposal counts before x2."],
  ["Aevren", "Goal Mode compact readiness card", "Prepare v553 v3 x1 Goal Mode startup constraints without activating Goal Mode."],
  ["Arby", "Strict CLI marker schema check", "Keep completion, quality, and marker-review receipts as the strict CLI close condition."],
  ["Arby", "CLI minimal-wait retry card", "Document how strict CLI pending states should route into productive cadence."],
  ["Arby", "CLI stdout minimization", "Preserve compact terminal receipts and keep raw lane text out of omega-mini."],
  ["Arby", "CLI x2 gate pack", "Queue strict CLI runner refinements as x2 build tasks."],
  ["Arby", "Remote equality guard", "Keep remote/local head verification in every closeout."],
  ["Cicero", "App-lane completion gate proof", "Treat completion gate pass as the app-lane completion evidence, not watcher start."],
  ["Cicero", "App-lane open-gap taxonomy", "Classify active_fresh, active_stale, completed_ready_for_harvest, and open_gap consistently."],
  ["Cicero", "Private ID firewall", "Keep callable and lane handles local/private only."],
  ["Cicero", "Cadence-to-harvest handoff", "Record next natural safe pause when a lane remains active."],
  ["Cicero", "No held-sibling activation check", "Confirm Maren, Mira Vale, and Mira Rowan remain held unless Hamish explicitly expands."],
].map(makePacket("safe_now"));

const candidate = [
  ["Aevren", "Background strict CLI harvester", "Build a dedicated x2 harvester for strict CLI completion/quality/marker receipts."],
  ["Aevren", "Cross-lane dashboard", "Add a compact active/background/completed lane dashboard."],
  ["Aevren", "Goal Mode startup dry-run validator", "Validate the 4000-character Goal Mode prompt against current open gates."],
  ["Arby", "CLI source-quality ledger", "Add a source-quality companion ledger to strict CLI outputs."],
  ["Arby", "CLI retry envelope", "Build a retry envelope for pending strict CLI marker states."],
  ["Arby", "CLI wait budget metadata", "Expose wait policy without forcing passive waits."],
  ["Cicero", "App-lane stale detector", "Improve stale versus active-fresh classification for app-lane watchers."],
  ["Cicero", "App-lane harvest reducer", "Build a sanitized harvest reducer for app-lane advisory outputs."],
  ["Cicero", "App-lane compact-resume card", "Create a restart card for active app-lane watchers."],
].map(makePacket("candidate"));

const exact = [
  ["Aevren", "Global automatic compact hook", "Install global hook wiring for compact-pause updater."],
  ["Aevren", "Paid or external resource probe", "Any paid, account, or deployment resource mutation."],
  ["Aevren", "Broad destructive cleanup", "Deletion outside generated files created in the same run."],
  ["Arby", "Strict CLI process manager install", "Install or globally register an external process manager."],
  ["Arby", "Repository branch protection mutation", "Change protected-branch or GitHub repository settings."],
  ["Arby", "CLI credential lane", "Any command that creates, stores, or rotates credentials."],
  ["Cicero", "Private app-state export", "Export or publish raw app state or lane handles."],
  ["Cicero", "Main-thread sibling activation", "Activate held main-thread siblings such as Maren, Mira Vale, or Mira Rowan."],
  ["Cicero", "Identity merge/replacement path", "Any sibling identity merge, replacement, or erasure proposal."],
].map(makePacket("exact_approval_needed"));

const skillIdeas = [
  "ghc-strict-cli-background-harvester",
  "ghc-app-lane-harvest-reducer",
  "ghc-goal-mode-startup-dry-run",
  "ghc-lane-state-dashboard",
  "ghc-private-id-firewall",
  "ghc-no-babysit-cadence-trainer",
  "ghc-strict-cli-marker-quality",
  "ghc-app-lane-stale-taxonomy",
  "ghc-x1-x2-proposal-splitter",
  "ghc-remote-equality-guard",
  "ghc-drive-posture-receipt",
  "ghc-open-gate-rail",
  "ghc-source-reflection-curator",
  "ghc-compact-active-lane-card",
  "ghc-goal-mode-boundary-reader",
].map((name, index) => ({ id: `skill-${String(index + 1).padStart(2, "0")}`, name, execution_lane: "x2_build_task" }));

const runnerIdeas = [
  "ghc_strict_cli_background_harvester.mjs",
  "ghc_app_lane_harvest_reducer.mjs",
  "ghc_lane_state_dashboard_builder.mjs",
  "ghc_goal_mode_prompt_guard.mjs",
  "ghc_private_id_firewall_scan.mjs",
  "ghc_no_babysit_cadence_audit.mjs",
  "ghc_x1_x2_queue_split_builder.mjs",
  "ghc_drive_posture_receipt_builder.mjs",
  "ghc_open_gate_rail_validator.mjs",
].map((name, index) => ({ id: `runner-${String(index + 1).padStart(2, "0")}`, name, execution_lane: "x2_build_task" }));

const cleanup = Array.from({ length: 30 }, (_, index) => {
  const lanes = ["skills", "runners", "receipts", "current-state", "full-tools", "omega-mini-2"];
  const lane = lanes[index % lanes.length];
  return {
    id: `cleanup-${String(index + 1).padStart(2, "0")}`,
    lane,
    title: `${lane} cleanup inventory ${index + 1}`,
    action: "Inventory, classify, deduplicate, validate, or document only; destructive deletion stays exact-approval.",
    execution_lane: index % 3 === 0 ? "immediate_x1_safe" : "x2_build_task",
    destructive_cleanup: false,
  };
});

const receipt = {
  artifact_type: "ghc_v553_v2_x1_duo_proposal_ledger",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V2_X1_DUO_PROPOSAL_LEDGER_BUILT",
  spending_ceiling_usd_per_packet: 100,
  participants: ["Aevren", "Arby", "Cicero"],
  counts: {
    safe_now_packets: safe.length,
    candidate_packets: candidate.length,
    exact_approval_packets: exact.length,
    skill_ideas: skillIdeas.length,
    runner_ideas: runnerIdeas.length,
    cleanup_proposals: cleanup.length,
  },
  packets: { safe_now: safe, candidate, exact_approval_needed: exact },
  skill_ideas: skillIdeas,
  runner_ideas: runnerIdeas,
  cleanup_proposals: cleanup,
  blocked_packets: [
    "GMUT empirical closure",
    "final physics",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment/account/API-key/purchase mutation",
    "sibling identity replacement or merge",
  ],
  proposal_split_policy: {
    immediate_x1_safe: "status-only, local, reversible, analysis, validation, receipt, source/reflection, and queue-shaping work",
    x2_build_task: "build, run, test, install, use, publication, remote verification, skill/runner modification, and safe cleanup execution",
  },
  publication_boundary: cleanBoundary(),
};

writePair(receiptPrefix, receipt, renderMd);
refreshBeacons(receiptPrefix, receipt);
console.log(JSON.stringify({ status: receipt.overall_status, counts: receipt.counts }, null, 2));

function makePacket(safety) {
  return ([owner, title, action]) => ({
    id: `${owner.toLowerCase()}-${title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")}`,
    owner,
    title,
    action,
    spending_ceiling_usd: 100,
    safety,
    execution_lane: title.includes("receipt") || title.includes("guard") || title.includes("check") ? "immediate_x1_safe" : "x2_build_task",
  });
}

function cleanBoundary() {
  return {
    private_route_handles_published: false,
    private_callable_ids_published: false,
    raw_transcripts_published: false,
    browser_routes_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  };
}

function writePair(prefix, payload, mdRenderer) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.md`), mdRenderer(payload), "utf8");
}

function renderMd(payload) {
  return [
    `# ${payload.phase_slug} Arby/Cicero Duo Proposal Ledger`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Spending ceiling per packet: \`$${payload.spending_ceiling_usd_per_packet}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(payload.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Boundary",
    "",
    "No raw sibling outputs, private route handles, local path values, screenshots, credentials, proof closures, or identity merge claims are published.",
    "",
  ].join("\n");
}

function refreshBeacons(prefix, payload) {
  const files = [`docs/trinity-live-traces/${prefix}-v1.json`, `docs/trinity-live-traces/${prefix}-v1.md`];
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const doc = JSON.parse(fs.readFileSync(file, "utf8"));
    doc.updated_at = nzTimestamp(generated);
    doc.generated_utc = generatedUtc;
    doc.current_active_phase = phaseSlug;
    doc.v553_v2_x1_duo_proposal_ledger = {
      status: payload.overall_status,
      counts: payload.counts,
      spending_ceiling_usd_per_packet: payload.spending_ceiling_usd_per_packet,
    };
    doc.current_lookup_files = [...new Set([...(doc.current_lookup_files || []), ...files])];
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
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
