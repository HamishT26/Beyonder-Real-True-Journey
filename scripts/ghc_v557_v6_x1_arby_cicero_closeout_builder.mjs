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

const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v6-x1";
const fullToolsRoot = args.get("--full-tools-root");
if (!fullToolsRoot) {
  console.error("Usage: node ghc_v557_v6_x1_arby_cicero_closeout_builder.mjs --full-tools-root <path>");
  process.exit(2);
}

const supportTraceDir = path.join(fullToolsRoot, "docs", "trinity-live-traces");
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);
const nextActivePhase = "v557-gmut-thos-v6-x2";
const nextX1AfterX2 = "v557-gmut-thos-v7-x1 with Lumen Vale solo unless Hamish redirects";

const arbyCompletion = readSupport(`${phaseSlug}-arby-strict-cli-completion-v1.json`);
const arbyQuality = readSupport(`${phaseSlug}-arby-strict-cli-quality-v1.json`);
const arbyMarker = readSupport(`${phaseSlug}-arby-strict-cli-marker-review-v1.json`);
const ciceroGate = readSupport(`${phaseSlug}-cicero-recovered-app-lane-completion-gate-v1.json`);
const proposal = readLocal(`${phaseSlug}-duo-proposal-targets-v1.json`);
const safeRunner = readLocal(`${phaseSlug}-safe-runner-orchestrator-v1.json`);

const arbyQualityLane = Array.isArray(arbyQuality.lanes) ? arbyQuality.lanes.find((lane) => lane.lane === "Arby") || {} : {};
const ciceroLane = Array.isArray(ciceroGate.lanes) ? ciceroGate.lanes.find((lane) => lane.lane === "Cicero") || {} : {};

const checks = [
  ["arby_completion", arbyCompletion.aggregate_status, "FINAL_MESSAGES_READY"],
  ["arby_quality", arbyQuality.aggregate_status, "PASS_ALL_CLI_LANES_ELABORATE"],
  ["arby_marker_review", arbyMarker.status || arbyMarker.overall_status, "PASS_MARKER_REVIEW_LEDGER"],
  ["cicero_completion_gate", ciceroGate.overall_status, "PASS_APP_LANE_COMPLETION_GATE"],
  ["safe_runner_orchestrator", safeRunner.overall_status, "PASS_SAFE_RUNNER_ORCHESTRATION"],
  ["proposal_targets", proposal.overall_status, "PASS_V557_V6_X1_DUO_PROPOSAL_TARGETS_RECORDED"],
];
const failed = checks.filter(([, actual, expected]) => actual !== expected);
if (failed.length) {
  process.stdout.write(JSON.stringify({
    status: "OPEN_GAP_V557_V6_X1_CLOSEOUT_CHECK_FAILED",
    phase_slug: phaseSlug,
    failed: failed.map(([name, actual, expected]) => ({ name, actual: actual || "missing", expected })),
  }, null, 2) + "\n");
  process.exit(1);
}

const harvest = artifact("ghc_v557_v6_x1_arby_cicero_harvest_sanitized", "PASS_V557_V6_X1_ARBY_CICERO_SANITIZED_HARVEST", {
  lanes: [
    {
      lane: "Arby",
      route: "strict_cli",
      completion_status: arbyCompletion.aggregate_status,
      quality_status: arbyQuality.aggregate_status,
      marker_review_status: arbyMarker.status || arbyMarker.overall_status,
      word_count: arbyQualityLane.word_count || null,
      required_headings_missing: arbyQualityLane.missing_required_headings || [],
      shallow_required_categories: arbyQualityLane.shallow_required_categories || [],
      category_item_counts: arbyQualityLane.category_item_counts || {},
      raw_output_published: false,
      private_output_hash_published: false,
    },
    {
      lane: "Cicero",
      route: "recovered_app_lane",
      completion_gate_status: ciceroGate.overall_status,
      completion_status: ciceroLane.completion_status || null,
      read_status: ciceroLane.read_status || null,
      resume_status: ciceroLane.resume_status || null,
      turn_status: ciceroLane.turn_status || null,
      open_gaps: ciceroGate.open_gaps || [],
      raw_output_published: false,
      private_callable_ids_published: false,
    },
  ],
  watcher_start_is_completion_proof: false,
  completion_gate_passed: true,
});

const gateStatus = artifact("ghc_v557_v6_x1_duo_gate_status", "PASS_V557_V6_X1_ARBY_CICERO_COMPLETION_GATES_PASSED", {
  checks: checks.map(([name, actual, expected]) => ({ name, actual, expected, pass: actual === expected })),
  phase_advance_allowed: true,
  source_receipts_private_support_only: true,
});

const closeout = artifact("ghc_v557_v6_x1_closeout", "PASS_V557_V6_X1_CLOSED_V6_X2_READY", {
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: phaseSlug,
  latest_completed_x2_phase: "v557-gmut-thos-v5-x2",
  next_active_phase: nextActivePhase,
  next_x2_scope: nextActivePhase,
  next_x1_lane_after_x2: nextX1AfterX2,
  full_goal_complete: false,
  proposal_counts: {
    safe_packets: proposal.safe_packets?.length || 0,
    candidate_packets: proposal.candidate_packets?.length || 0,
    exact_approval_packets: proposal.exact_approval_packets?.length || 0,
    skill_ideas: proposal.skill_ideas?.length || 0,
    runner_ideas: proposal.runner_ideas?.length || 0,
    cleanup_proposals: proposal.cleanup_proposals?.length || 0,
  },
  safe_runner_status: safeRunner.overall_status,
  branch_rotation_next_pattern: "omega-mini-4/full-tools-3 when mini-3 or full-tools-2 gets heavy",
});

const handoff = artifact("ghc_v557_v6_x1_v6_x2_handoff", "PASS_V557_V6_X2_READY_FOR_DUO_SAFE_EXECUTION", {
  source_phase: phaseSlug,
  next_active_phase: nextActivePhase,
  execution_scope: [
    "Build, run, test, and validate safe/candidate duo proposals.",
    "Refresh/install local-safe skills and runners from the duo queue.",
    "Keep exact and blocked gates queued unless Hamish explicitly redirects.",
    "Prepare v557 v7 x1 Lumen-only startup after v6 x2 closeout.",
    "Continue branch rotation watch for omega-mini-4 and full-tools-3 readiness.",
  ],
});

writePair("arby-cicero-harvest-sanitized", harvest, renderGenericMd("Arby/Cicero Sanitized Harvest", harvest));
writePair("duo-gate-status", gateStatus, renderGenericMd("Duo Gate Status", gateStatus));
writePair("v6-x2-handoff", handoff, renderGenericMd("v6 x2 Handoff", handoff));
writePair("closeout", closeout, renderGenericMd("Closeout", closeout));
refreshBeacons(closeout);

process.stdout.write(JSON.stringify({
  status: closeout.overall_status,
  phase_slug: phaseSlug,
  next_active_phase: nextActivePhase,
  arby_passed: true,
  cicero_passed: true,
  full_goal_complete: false,
}, null, 2) + "\n");

function readSupport(name) {
  return JSON.parse(fs.readFileSync(path.join(supportTraceDir, name), "utf8").replace(/^\uFEFF/, ""));
}

function readLocal(name) {
  return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8").replace(/^\uFEFF/, ""));
}

function artifact(artifactType, status, extra) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    ...extra,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function writePair(suffix, payload, md) {
  writeJson(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), payload);
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md, "utf8");
}

function writeJson(file, payload) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function renderGenericMd(title, payload) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "Sanitized phase artifact only. No raw sibling output, private callable IDs, raw routes, transcripts, screenshots, credentials, private dumps, local path values, or private material proof claims are published.",
    "",
  ].join("\n");
}

function refreshBeacons(closeout) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-arby-cicero-harvest-sanitized-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-arby-cicero-harvest-sanitized-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-duo-gate-status-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-duo-gate-status-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-v6-x2-handoff-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-v6-x2-handoff-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.md`,
  ];
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = JSON.parse(fs.readFileSync(jsonFile, "utf8").replace(/^\uFEFF/, ""));
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = closeout.overall_status;
    doc.current_active_phase = nextActivePhase;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = phaseSlug;
    doc.latest_completed_x2_phase = "v557-gmut-thos-v5-x2";
    doc.next_x2_scope = nextActivePhase;
    doc.next_x1_lane_after_x2 = nextX1AfterX2;
    doc.v557_v6_x1_closeout = {
      status: closeout.overall_status,
      arby_passed: true,
      cicero_passed: true,
      full_goal_complete: false,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
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
    "",
    "## v557 v6 x1 Closeout",
    "",
    `- status: \`${doc.v557_v6_x1_closeout?.status || "not_recorded"}\``,
    `- full goal complete: \`${doc.v557_v6_x1_closeout?.full_goal_complete ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-240).map((file) => `- ${file}`),
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
    private_output_hash_published: false,
  };
}

function claimBoundary() {
  return {
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
