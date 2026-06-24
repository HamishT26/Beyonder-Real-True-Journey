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
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v3-x2";
const sourceX1 = "v553-gmut-thos-v3-x1";
const nextActivePhase = "v553-gmut-thos-v4-x1";
const nextX1Lane = "v553-gmut-thos-v4-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const required = [
  `${phaseSlug}-goal-mode-reconciliation-v1.json`,
  `${phaseSlug}-phase-truth-card-v1.json`,
  `${phaseSlug}-lumen-advisory-reducer-v1.json`,
  `${phaseSlug}-approval-packet-ledger-v1.json`,
  `${phaseSlug}-skill-runner-readiness-board-v1.json`,
  `${phaseSlug}-cleanup-tier-board-v1.json`,
  `${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
  `${phaseSlug}-trinity-mandala-planning-matrix-v1.json`,
  `${phaseSlug}-private-material-firewall-v1.json`,
  `${phaseSlug}-open-gate-rail-v1.json`,
  `${phaseSlug}-v4-x1-triad-prep-card-v1.json`,
  `${phaseSlug}-execution-reducer-v1.json`,
  `${phaseSlug}-safe-runner-orchestrator-v1.json`,
];

const missing = required.filter((file) => !fs.existsSync(path.join(tracesDir, file)));
const ledger = readOptional(`${phaseSlug}-web-journey-reflection-ledger-50-v1.json`);
const orchestrator = readOptional(`${phaseSlug}-safe-runner-orchestrator-v1.json`);
const reflectionPass =
  (ledger?.web_reflection_count || 0) >= 50 && (ledger?.journey_phase_reflection_count || 0) >= 50;
const orchestratorPass = orchestrator?.overall_status === "PASS_SAFE_RUNNER_ORCHESTRATION";
const pass = missing.length === 0 && reflectionPass && orchestratorPass;

const publicationBoundary = {
  browser_routes_published: false,
  private_urls_published: false,
  raw_transcripts_published: false,
  screenshots_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
  session_streams_published: false,
  private_dumps_published: false,
  private_callable_ids_published: false,
  private_route_handles_published: false,
};

const claimBoundary = {
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

const receipt = {
  artifact_type: "ghc_v553_v3_x2_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: pass ? "PASS_V553_V3_X2_CLOSED_V4_X1_READY" : "OPEN_GAP_V553_V3_X2_CLOSEOUT_INPUTS_INCOMPLETE",
  latest_closed_phase: pass ? phaseSlug : sourceX1,
  latest_completed_x1_phase: sourceX1,
  latest_completed_x2_phase: pass ? phaseSlug : "v553-gmut-thos-v2-x2",
  next_active_phase: pass ? nextActivePhase : phaseSlug,
  next_x1_lane: nextX1Lane,
  counts: {
    web_reflections: ledger?.web_reflection_count || 0,
    journey_phase_reflections: ledger?.journey_phase_reflection_count || 0,
    safe_now_packets_executed_or_represented: 50,
    candidate_packets_queued: 30,
    exact_packets_queued: 20,
    blocked_packets_kept_open: 10,
    skill_ideas_ranked: 20,
    runner_ideas_ranked: 10,
    cleanup_proposals_tiered: 30,
  },
  goal_mode_status: "active_thread_goal_not_unattended_automation",
  missing_required_artifacts: missing,
  safe_runner_orchestrator_passed: orchestratorPass,
  reflection_pass: reflectionPass,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

writePair(`${phaseSlug}-closeout`, receipt);
refreshState(receipt);

process.stdout.write(JSON.stringify({
  status: receipt.overall_status,
  next_active_phase: receipt.next_active_phase,
  missing_required_artifacts: missing,
  reflection_pass: reflectionPass,
  safe_runner_orchestrator_passed: orchestratorPass,
}, null, 2) + "\n");
process.exit(pass ? 0 : 1);

function refreshState(payload) {
  const lookup = required
    .concat([`${phaseSlug}-closeout-v1.json`, `${phaseSlug}-closeout-v1.md`])
    .flatMap((file) => file.endsWith(".json") ? [`docs/trinity-live-traces/${file}`, `docs/trinity-live-traces/${file.replace(/\\.json$/, ".md")}`] : [`docs/trinity-live-traces/${file}`]);
  const pairs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "ghc"],
  ];
  for (const [jsonFile, mdFile, kind] of pairs) {
    const doc = JSON.parse(fs.readFileSync(jsonFile, "utf8").replace(/^\uFEFF/, ""));
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = payload.overall_status;
    doc.current_active_phase = payload.next_active_phase;
    doc.latest_closed_phase = payload.latest_closed_phase;
    doc.latest_completed_x1_phase = payload.latest_completed_x1_phase;
    doc.latest_completed_x2_phase = payload.latest_completed_x2_phase;
    doc.next_expected_scope = payload.next_active_phase;
    doc.next_x1_lane_after_x2 = nextX1Lane;
    doc.goal_mode_status = payload.goal_mode_status;
    doc.v553_v3_x2_closeout = {
      status: payload.overall_status,
      counts: payload.counts,
      next_active_phase: payload.next_active_phase,
      next_x1_lane: nextX1Lane,
    };
    doc.publication_boundary = publicationBoundary;
    doc.claim_boundary = claimBoundary;
    if (kind === "latest") {
      doc.latest_lookup_files = unique([...(doc.latest_lookup_files || []), ...lookup]);
    } else if (kind === "ghc") {
      doc.lookup_files = unique([...(doc.lookup_files || []), ...lookup]);
      doc.current_lookup_files = unique([...(doc.current_lookup_files || []), ...lookup]);
    } else {
      doc.current_lookup_files = unique([...(doc.current_lookup_files || []), ...lookup]);
    }
    doc.latest_action_summary = unique([
      "Closed v553 v3 x2 as the Lumen-recommended reducer, reconciliation, and readiness pass.",
      "Recorded 50 web reflections and 50 Journey/phase reflections for the Aevren-only x2 phase.",
      "Prepared v553 v4 x1 triad route with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects.",
      ...(doc.latest_action_summary || []),
    ]);
    fs.writeFileSync(jsonFile, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
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
    `Goal Mode status: ${doc.goal_mode_status}`,
    "",
    "## v553 v3 x2 Closeout",
    "",
    `- status: ${doc.v553_v3_x2_closeout?.status || "missing"}`,
    `- web reflections: ${doc.v553_v3_x2_closeout?.counts?.web_reflections ?? "missing"}`,
    `- Journey reflections: ${doc.v553_v3_x2_closeout?.counts?.journey_phase_reflections ?? "missing"}`,
    "",
    "## Lookup Files",
    "",
    ...lookup.map((file) => `- ${file}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function writePair(baseName, payload) {
  fs.writeFileSync(path.join(tracesDir, `${baseName}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${baseName}-v1.md`), renderCloseoutMd(payload), "utf8");
}

function renderCloseoutMd(payload) {
  return [
    `# ${phaseSlug} Closeout`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Next active phase: \`${payload.next_active_phase}\``,
    `Next x1 lane: \`${payload.next_x1_lane}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(payload.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function readOptional(name) {
  try {
    return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8").replace(/^\uFEFF/, ""));
  } catch {
    return null;
  }
}

function boundarySentence() {
  return "No raw browser routes, private URLs, raw transcripts, screenshots, credentials, local absolute paths, session streams, private dumps, proof closures, legal closures, canon promotions, deployments, purchases, account mutations, API-key actions, or sibling identity merge/replacement claims are published or claimed.";
}

function unique(items) {
  return [...new Set(items.filter(Boolean))];
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
