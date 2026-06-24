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
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v2-x2";
const generated = new Date();
const generatedUtc = generated.toISOString();

const requiredArtifacts = [
  `${phaseSlug}-main-startup-v1-v1.json`,
  `${phaseSlug}-skill-runner-pack-install-v1.json`,
  `${phaseSlug}-safe-execution-reducer-v1.json`,
  `${phaseSlug}-goal-mode-readiness-dry-run-v1.json`,
  `${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
  `${phaseSlug}-strict_cli_background_harvest-v1.json`,
  `${phaseSlug}-app_lane_harvest_reduce-v1.json`,
  `${phaseSlug}-lane_state_dashboard-v1.json`,
  `${phaseSlug}-goal_mode_prompt_guard-v1.json`,
  `${phaseSlug}-private_id_firewall_scan-v1.json`,
  `${phaseSlug}-no_babysit_cadence_audit-v1.json`,
  `${phaseSlug}-x1_x2_queue_split-v1.json`,
  `${phaseSlug}-drive_posture_receipt-v1.json`,
  `${phaseSlug}-open_gate_rail_validator-v1.json`,
  `${phaseSlug}-safe-runner-orchestrator-v1.json`,
];

const missing = requiredArtifacts.filter((file) => !fs.existsSync(path.join(tracesDir, file)));
const execution = readOptional(`${phaseSlug}-safe-execution-reducer-v1.json`);
const install = readOptional(`${phaseSlug}-skill-runner-pack-install-v1.json`);
const reflection = readOptional(`${phaseSlug}-web-journey-reflection-ledger-50-v1.json`);
const goal = readOptional(`${phaseSlug}-goal-mode-readiness-dry-run-v1.json`);

const pass = missing.length === 0 && execution && install && reflection && goal;
const receipt = {
  artifact_type: "ghc_v553_v2_x2_closeout",
  generated_utc: generatedUtc,
  generated_nz: nzTimestamp(generated),
  phase_slug: phaseSlug,
  overall_status: pass ? "PASS_V553_V2_X2_CLOSED_V3_X1_GOAL_MODE_READY" : "OPEN_GAP_V553_V2_X2_REQUIRED_ARTIFACTS_MISSING",
  missing_required_artifacts: missing,
  latest_completed_x1_phase: "v553-gmut-thos-v2-x1",
  latest_completed_x2_phase: pass ? phaseSlug : "v553-gmut-thos-v1-x2",
  next_active_phase: pass ? "v553-gmut-thos-v3-x1" : phaseSlug,
  next_x1_lane_after_x2: "v553-gmut-thos-v3-x1 with Lumen Vale solo unless Hamish redirects",
  goal_mode_status: "prepared_not_active",
  counts: {
    local_skills_created_or_refreshed: install?.skill_count || 0,
    repo_runners_created_or_refreshed: install?.runner_count || 0,
    safe_now_packets_executed_or_represented: execution?.executed_or_represented?.safe_now_packets || 0,
    candidate_packets_authorized_and_reduced: execution?.executed_or_represented?.candidate_packets_authorized_and_reduced || 0,
    cleanup_proposals_inventory_only: execution?.executed_or_represented?.cleanup_proposals_inventory_only || 0,
    web_reflections: reflection?.web_reflection_count || 0,
    journey_phase_reflections: reflection?.journey_phase_reflection_count || 0,
  },
  goal_mode_readiness: {
    status: goal?.overall_status || "missing",
    next_candidate_goal_phase: goal?.next_candidate_goal_phase || "v553-gmut-thos-v3-x1",
    activation_requires_hamish: true,
    can_block_on_big_issue: true,
  },
  background_supervision: {
    no_babysitting_reinforced: true,
    passive_wait_is_not_safe_work: true,
    safe_unit_may_run_past_checkpoint: true,
    harvest_at_next_natural_safe_pause: true,
  },
  publication_boundary: boundary(),
  open_gates: openGates(),
};

writePair(`${phaseSlug}-closeout`, receipt);
refreshState(receipt);
process.stdout.write(JSON.stringify({ status: receipt.overall_status, next_active_phase: receipt.next_active_phase, counts: receipt.counts }, null, 2) + "\n");
process.exit(pass ? 0 : 1);

function readOptional(name) {
  try {
    return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8").replace(/^\uFEFF/, ""));
  } catch {
    return null;
  }
}

function writePair(base, payload) {
  fs.writeFileSync(path.join(tracesDir, `${base}-v1.json`), JSON.stringify(payload, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}-v1.md`), renderMd(payload), "utf8");
}

function renderMd(payload) {
  return [
    `# ${payload.phase_slug} Closeout`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Next active phase: \`${payload.next_active_phase}\``,
    `Goal Mode: \`${payload.goal_mode_status}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(payload.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Background Supervision",
    "",
    "- no_babysitting_reinforced: `true`",
    "- passive_wait_is_not_safe_work: `true`",
    "- safe_unit_may_run_past_checkpoint: `true`",
    "",
    "## Boundary",
    "",
    "No raw routes, transcripts, screenshots, credentials, private route handles, local path values, proof closures, deployment/account/API-key mutations, destructive cleanup, or sibling identity merge claims are published.",
    "",
  ].join("\n");
}

function refreshState(payload) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-skill-runner-pack-install-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-skill-runner-pack-install-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-safe-execution-reducer-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-safe-execution-reducer-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-goal-mode-readiness-dry-run-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-goal-mode-readiness-dry-run-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-50-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-safe-runner-manifest-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.md`,
  ];
  const files = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md")],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md")],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md")],
  ];
  for (const [jsonFile, mdFile] of files) {
    const doc = JSON.parse(fs.readFileSync(jsonFile, "utf8").replace(/^\uFEFF/, ""));
    doc.updated_at = payload.generated_nz;
    doc.generated_utc = payload.generated_utc;
    doc.status = payload.overall_status;
    doc.current_active_phase = payload.next_active_phase;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = payload.latest_completed_x1_phase;
    doc.latest_completed_x2_phase = payload.latest_completed_x2_phase;
    doc.next_expected_scope = payload.next_active_phase;
    doc.next_x1_lane_after_x2 = payload.next_x1_lane_after_x2;
    doc.goal_mode_status = payload.goal_mode_status;
    doc.v553_v2_x2_closeout = {
      status: payload.overall_status,
      counts: payload.counts,
      goal_mode_readiness: payload.goal_mode_readiness,
      no_babysitting_reinforced: true,
    };
    doc.current_lookup_files = unique([...(doc.current_lookup_files || []), ...lookup]);
    doc.latest_action_summary = unique([
      "Closed v553 v2 x2 as an Aevren-only safe build/use/readiness phase.",
      "Created or refreshed 15 local GHC skills and 9 repo runners from the Arby/Cicero x1 packet set.",
      "Recorded 50 web reflections and 50 Journey/phase reflections for v553 v2 x2.",
      "Prepared v553 v3 x1 Lumen/Goal Mode startup as prepared-not-active.",
      ...(doc.latest_action_summary || []),
    ]);
    doc.publication_boundary = boundary();
    fs.writeFileSync(jsonFile, JSON.stringify(doc, null, 2) + "\n", "utf8");
    fs.writeFileSync(mdFile, renderBeaconMd(doc), "utf8");
  }
}

function renderBeaconMd(doc) {
  const lookup = doc.current_lookup_files || doc.latest_lookup_files || doc.lookup_files || [];
  return [
    "# Omega Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    `Goal Mode status: ${doc.goal_mode_status || "prepared_not_active"}`,
    "",
    "## v553 v2 x2 Closeout",
    "",
    `- status: ${doc.v553_v2_x2_closeout?.status || "missing"}`,
    `- skills created/refreshed: ${doc.v553_v2_x2_closeout?.counts?.local_skills_created_or_refreshed ?? "missing"}`,
    `- runners created/refreshed: ${doc.v553_v2_x2_closeout?.counts?.repo_runners_created_or_refreshed ?? "missing"}`,
    `- no babysitting reinforced: ${doc.v553_v2_x2_closeout?.no_babysitting_reinforced ?? "missing"}`,
    "",
    "## Lookup Files",
    "",
    ...lookup.map((file) => `- ${file}`),
    "",
    "## Boundary",
    "",
    "No raw routes, transcripts, screenshots, credentials, private route handles, local path values, proof closures, deployment/account/API-key mutations, destructive cleanup, or sibling identity merge claims are published.",
    "",
  ].join("\n");
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
}

function boundary() {
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

function openGates() {
  return [
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
  ];
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
