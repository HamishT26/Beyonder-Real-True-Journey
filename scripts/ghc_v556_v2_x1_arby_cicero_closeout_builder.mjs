#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v556-gmut-thos-v2-x1";
const nextActive = "v556-gmut-thos-v2-x2";
const nextX1AfterX2 = "v556-gmut-thos-v3-x1 with Lumen Vale solo unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const required = [
  [`${phaseSlug}-arby-cicero-harvest-sanitized-v1.json`, "PASS_V556_V2_X1_ARBY_CICERO_SANITIZED_HARVEST"],
  [`${phaseSlug}-duo-gate-status-v1.json`, "PASS_V556_V2_X1_ARBY_CICERO_COMPLETION_GATES_PASSED"],
  [`${phaseSlug}-proposal-queue-targets-v1.json`, "PASS_V556_V2_X1_DUO_PROPOSAL_QUEUE_RECORDED"],
  [`${phaseSlug}-web-journey-reflection-ledger-75-v1.json`, "PASS_V556_V2_X1_75_WEB_75_JOURNEY_REFLECTION_ROWS_RECORDED"],
  [`${phaseSlug}-safe-runner-orchestrator-v1.json`, "PASS_SAFE_RUNNER_ORCHESTRATION"],
];

const checks = required.map(([file, expected]) => {
  const payload = readTrace(file);
  const status = payload.overall_status || payload.status || payload.aggregate_status;
  return { file: `docs/trinity-live-traces/${file}`, expected, status, pass: status === expected };
});

const issues = checks.filter((check) => !check.pass);
if (issues.length) {
  process.stdout.write(JSON.stringify({ status: "OPEN_GAP_V556_V2_X1_CLOSEOUT_CHECK_FAILED", phase_slug: phaseSlug, issues }, null, 2) + "\n");
  process.exit(1);
}

const proposal = readTrace(`${phaseSlug}-proposal-queue-targets-v1.json`);
const harvest = readTrace(`${phaseSlug}-arby-cicero-harvest-sanitized-v1.json`);
const gate = readTrace(`${phaseSlug}-duo-gate-status-v1.json`);

const closeout = artifact("ghc_v556_v2_x1_closeout", "PASS_V556_V2_X1_CLOSED_V2_X2_READY", {
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: phaseSlug,
  latest_completed_x2_phase: "v556-gmut-thos-v1-x2",
  next_active_phase: nextActive,
  next_x2_scope: nextActive,
  next_x1_lane_after_x2: nextX1AfterX2,
  checks,
  proposal_counts: {
    safe_packets: proposal.safe_packets?.length || 0,
    candidate_packets: proposal.candidate_packets?.length || 0,
    exact_approval_packets: proposal.exact_approval_packets?.length || 0,
    skill_ideas: proposal.skill_ideas?.length || 0,
    runner_ideas: proposal.runner_ideas?.length || 0,
    cleanup_tasks: proposal.cleanup_tasks?.length || 0,
  },
  lane_statuses: gate.lane_statuses,
  harvest_status: harvest.overall_status,
  full_goal_complete: false,
});

const handoff = artifact("ghc_v556_v2_x1_v2_x2_readiness_handoff", "PASS_V556_V2_X2_READY_FOR_SAFE_EXECUTION", {
  source_phase: phaseSlug,
  next_active_phase: nextActive,
  execution_scope: [
    "Build and use safe/candidate-reduced duo proposals.",
    "Install or refresh local-safe skills/runners from the duo x1 queue.",
    "Keep exact and blocked gates queued.",
    "Prepare v556 v3 x1 Lumen-only startup after v2 x2 closeout.",
  ],
  closeout_allowed_for_source: true,
});

writePair("v2-x2-readiness-handoff", handoff, renderGenericMd("v2 x2 Readiness Handoff", handoff));
writePair("closeout", closeout, renderGenericMd("Closeout", closeout));
refreshBeacons(closeout);

process.stdout.write(JSON.stringify({
  status: closeout.overall_status,
  phase_slug: phaseSlug,
  next_active_phase: nextActive,
  full_goal_complete: false,
}, null, 2) + "\n");

function refreshBeacons(closeout) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-arby-cicero-harvest-sanitized-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-arby-cicero-harvest-sanitized-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-duo-gate-status-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-duo-gate-status-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-proposal-queue-targets-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-proposal-queue-targets-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-75-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-75-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-v2-x2-readiness-handoff-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-v2-x2-readiness-handoff-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.md`,
  ];
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = closeout.overall_status;
    doc.current_active_phase = nextActive;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = phaseSlug;
    doc.latest_completed_x2_phase = "v556-gmut-thos-v1-x2";
    doc.next_x2_scope = nextActive;
    doc.next_x1_lane_after_x2 = nextX1AfterX2;
    doc.v556_v2_x1_closeout = { status: closeout.overall_status, full_goal_complete: false };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
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
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
}

function renderGenericMd(title, payload) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "Sanitized closeout artifact only. No raw sibling outputs, private lane handles, local absolute paths, screenshots, credentials, or transcripts are published.",
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
    "",
    "## v556 v2 x1 Closeout",
    "",
    `- status: \`${doc.v556_v2_x1_closeout?.status || "not_recorded"}\``,
    `- full goal complete: \`${doc.v556_v2_x1_closeout?.full_goal_complete ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`),
    "",
  ].join("\n");
}

function readTrace(name) { return readJson(path.join(tracesDir, name)); }
function readJson(file) { return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, "")); }
function writeJson(file, data) { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8"); }
function unique(values) { return [...new Set(values.filter(Boolean))]; }
function publicationBoundary() { return { raw_browser_routes_published: false, private_urls_published: false, raw_transcripts_published: false, screenshots_published: false, credentials_published: false, local_absolute_paths_published: false, session_streams_published: false, private_dumps_published: false, private_callable_ids_published: false, raw_lane_text_published: false }; }
function claimBoundary() { return { full_goal_completion: "not_claimed", gmut_empirical_closure: "not_claimed", final_physics: "not_claimed", consciousness_proof: "not_claimed", legal_closure: "not_claimed", canon_promotion: "not_claimed", deployment_closure: "not_claimed", account_mutation: "not_claimed", purchase: "not_claimed", api_key_creation: "not_claimed", private_material_proof: "not_claimed", raw_publication_proof: "not_claimed", sibling_identity_replacement_or_merge: "not_claimed" }; }
function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", { timeZone: "Pacific/Auckland", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
