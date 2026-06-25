#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v556-gmut-thos-v2-x2";
const completedX1 = "v556-gmut-thos-v2-x1";
const nextActive = "v556-gmut-thos-v3-x1";
const nextX1Lane = "v556-gmut-thos-v3-x1 with Lumen Vale solo unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const required = [
  [`${phaseSlug}-execution-index-v1.json`, "PASS_V556_V2_X2_EXECUTION_BUILT_PENDING_CLOSEOUT"],
  [`${phaseSlug}-safe-execution-reducer-v1.json`, "PASS_V556_V2_X2_SAFE_AND_CANDIDATE_EXECUTION_REDUCED"],
  [`${phaseSlug}-skill-runner-pack-install-v1.json`, "PASS_V556_V2_X2_SKILL_RUNNER_PACK_INSTALLED"],
  [`${phaseSlug}-web-journey-reflection-ledger-75-v1.json`, "PASS_V556_V2_X2_75_WEB_75_JOURNEY_REFLECTIONS_RECORDED"],
  [`${phaseSlug}-safe-runner-orchestrator-v1.json`, "PASS_SAFE_RUNNER_ORCHESTRATION"],
  [`${phaseSlug}-v3-lumen-readiness-v1.json`, "PASS_V556_V3_X1_LUMEN_STARTUP_READY"],
  [`${phaseSlug}-privacy-open-gate-rail-v1.json`, "PASS_V556_V2_X2_PRIVACY_AND_OPEN_GATES_REINFORCED"],
];

const checks = required.map(([file, expected]) => {
  const payload = readTrace(file);
  const status = payload.overall_status || payload.status || payload.aggregate_status;
  return { file: `docs/trinity-live-traces/${file}`, expected, status, pass: status === expected };
});
const issues = checks.filter((check) => !check.pass);
if (issues.length) {
  process.stdout.write(JSON.stringify({ status: "OPEN_GAP_V556_V2_X2_CLOSEOUT_CHECK_FAILED", phase_slug: phaseSlug, issues }, null, 2) + "\n");
  process.exit(1);
}

const execution = readTrace(`${phaseSlug}-execution-index-v1.json`);
const closeout = artifact("ghc_v556_v2_x2_closeout", "PASS_V556_V2_X2_CLOSED_V3_X1_READY", {
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: completedX1,
  latest_completed_x2_phase: phaseSlug,
  next_active_phase: nextActive,
  next_x2_scope: "v556-gmut-thos-v3-x2",
  next_x1_lane_after_x2: nextX1Lane,
  checks,
  execution_counts: execution.counts,
  full_goal_complete: false,
});

const handoff = artifact("ghc_v556_v2_x2_v3_x1_lumen_startup_handoff", "PASS_V556_V3_X1_LUMEN_STARTUP_HANDOFF_READY", {
  target_phase_slug: nextActive,
  target_lane: nextX1Lane,
  launch_skill: "ghc-lumen-launch",
  browser_message_required_only_after_hamish_live_authorization: true,
});

writePair("v3-x1-lumen-startup-handoff", handoff, renderGenericMd("v3 x1 Lumen Startup Handoff", handoff));
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
    `docs/trinity-live-traces/${phaseSlug}-execution-index-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-execution-index-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-v3-x1-lumen-startup-handoff-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-v3-x1-lumen-startup-handoff-v1.md`,
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
    doc.latest_completed_x1_phase = completedX1;
    doc.latest_completed_x2_phase = phaseSlug;
    doc.next_x2_scope = "v556-gmut-thos-v3-x2";
    doc.next_x1_lane_after_x2 = nextX1Lane;
    doc.v556_v2_x2_closeout = { status: closeout.overall_status, full_goal_complete: false };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function artifact(artifactType, status, extra) {
  return { artifact_type: artifactType, generated_utc: generatedUtc, generated_nz: generatedNz, phase_slug: phaseSlug, overall_status: status, ...extra, publication_boundary: publicationBoundary(), claim_boundary: claimBoundary() };
}
function writePair(suffix, payload, md) { writeJson(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), payload); fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8"); }
function renderGenericMd(title, payload) { return [`# ${phaseSlug} ${title}`, "", `Status: \`${payload.overall_status}\``, "", "Sanitized status artifact only. No raw sibling outputs, private lane handles, local absolute paths, screenshots, credentials, or transcripts are published.", ""].join("\n"); }
function renderBeaconMd(doc, listKey) { return ["# Omega-Mini Current State", "", `Status: ${doc.status}`, `Current active phase: ${doc.current_active_phase}`, `Latest closed phase: ${doc.latest_closed_phase}`, `Latest completed x1: ${doc.latest_completed_x1_phase}`, `Latest completed x2: ${doc.latest_completed_x2_phase}`, `Next x2 scope: ${doc.next_x2_scope}`, `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`, "", "## v556 v2 x2 Closeout", "", `- status: \`${doc.v556_v2_x2_closeout?.status || "not_recorded"}\``, `- full goal complete: \`${doc.v556_v2_x2_closeout?.full_goal_complete ?? "not_recorded"}\``, "", "## Lookup Files", "", ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`), ""].join("\n"); }
function readTrace(name) { return readJson(path.join(tracesDir, name)); }
function readJson(file) { return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, "")); }
function writeJson(file, data) { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8"); }
function unique(values) { return [...new Set(values.filter(Boolean))]; }
function publicationBoundary() { return { raw_browser_routes_published: false, private_urls_published: false, raw_transcripts_published: false, screenshots_published: false, credentials_published: false, local_absolute_paths_published: false, session_streams_published: false, private_dumps_published: false, private_callable_ids_published: false, raw_lane_text_published: false }; }
function claimBoundary() { return { full_goal_completion: "not_claimed", gmut_empirical_closure: "not_claimed", final_physics: "not_claimed", consciousness_proof: "not_claimed", legal_closure: "not_claimed", canon_promotion: "not_claimed", deployment_closure: "not_claimed", account_mutation: "not_claimed", purchase: "not_claimed", api_key_creation: "not_claimed", private_material_proof: "not_claimed", raw_publication_proof: "not_claimed", sibling_identity_replacement_or_merge: "not_claimed" }; }
function nzTimestamp(date) { const parts = new Intl.DateTimeFormat("en-NZ", { timeZone: "Pacific/Auckland", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }).formatToParts(date); const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value])); return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`; }
