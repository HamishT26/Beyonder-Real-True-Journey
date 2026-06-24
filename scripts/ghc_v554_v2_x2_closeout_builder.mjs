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
const phaseSlug = args.get("--phase-slug") || "v554-gmut-thos-v2-x2";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const execution = readRequired(`${phaseSlug}-execution-index-v1.json`);
const safe = readRequired(`${phaseSlug}-safe-execution-reducer-v1.json`);
const skillPack = readRequired(`${phaseSlug}-skill-runner-pack-install-v1.json`);
const reflection = readRequired(`${phaseSlug}-web-journey-reflection-ledger-50-v1.json`);
const goalMode = readRequired(`${phaseSlug}-v3-lumen-goal-mode-readiness-v1.json`);
const safeRunner = readOptional(`${phaseSlug}-safe-runner-orchestrator-v1.json`);

const checks = {
  execution_status: execution.overall_status,
  safe_execution_status: safe.overall_status,
  skill_pack_status: skillPack.overall_status,
  reflection_status: reflection.overall_status,
  goal_mode_readiness_status: goalMode.overall_status,
  safe_runner_status: safeRunner?.overall_status || safeRunner?.status || "missing",
  web_reflections: reflection.web_reflection_count,
  journey_phase_reflections: reflection.journey_phase_reflection_count,
};
const passed =
  checks.execution_status === "PASS_V554_V2_X2_EXECUTION_BUILT_PENDING_CLOSEOUT" &&
  checks.safe_execution_status === "PASS_V554_V2_X2_SAFE_AND_CANDIDATE_EXECUTION_REDUCED" &&
  checks.skill_pack_status === "PASS_V554_V2_X2_SKILL_RUNNER_PACK_INSTALLED" &&
  checks.reflection_status === "PASS_V554_V2_X2_50_WEB_50_JOURNEY_REFLECTIONS_RECORDED" &&
  checks.goal_mode_readiness_status === "PASS_V554_V3_X1_LUMEN_GOAL_MODE_STARTUP_READY" &&
  checks.web_reflections >= 50 &&
  checks.journey_phase_reflections >= 50;

const receipt = {
  artifact_type: "ghc_v554_v2_x2_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: passed ? "PASS_V554_V2_X2_CLOSED_V3_X1_READY" : "OPEN_GAP_V554_V2_X2_CLOSEOUT_CHECKS_PENDING",
  latest_completed_x1_phase: "v554-gmut-thos-v2-x1",
  latest_completed_x2_phase: passed ? phaseSlug : "v554-gmut-thos-v1-x2",
  next_active_phase: passed ? "v554-gmut-thos-v3-x1" : phaseSlug,
  next_x2_scope: passed ? "v554-gmut-thos-v3-x2" : phaseSlug,
  next_x1_lane_after_x2: passed
    ? "v554-gmut-thos-v4-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects"
    : "v554-gmut-thos-v3-x1 with Lumen Vale solo unless Hamish redirects",
  checks,
  counts: {
    safe_now_packets_executed_or_represented: safe.executed_or_represented.safe_now_packets,
    candidate_packets_authorized_and_reduced: safe.executed_or_represented.candidate_packets_authorized_and_reduced,
    exact_packets_queued: safe.held_open.exact_approval_packets_queued,
    cleanup_inventory_only: safe.executed_or_represented.cleanup_proposals_inventory_only,
    skills_created_or_refreshed: skillPack.skill_count,
    runners_created_or_refreshed: skillPack.runner_count,
    web_reflections: reflection.web_reflection_count,
    journey_phase_reflections: reflection.journey_phase_reflection_count,
  },
  goal_mode_status: "active_thread_goal_not_unattended_automation",
  full_goal_complete: false,
  publication_boundary: boundary(),
  claim_boundary: claimBoundary(passed),
};

writePair(`${phaseSlug}-closeout`, receipt, renderMd);
if (passed) refreshState(receipt);

console.log(JSON.stringify({ status: receipt.overall_status, next_active_phase: receipt.next_active_phase, full_goal_complete: false }, null, 2) + "\n");
process.exit(passed ? 0 : 1);

function readRequired(name) {
  return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8").replace(/^\uFEFF/, ""));
}

function readOptional(name) {
  try {
    return readRequired(name);
  } catch {
    return null;
  }
}

function writePair(prefix, payload, mdRenderer) {
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.md`), mdRenderer(payload), "utf8");
}

function renderMd(payload) {
  return [`# ${payload.phase_slug} Closeout`, "", `Status: \`${payload.overall_status}\``, `Next active phase: \`${payload.next_active_phase}\``, `Full goal complete: \`${payload.full_goal_complete}\``, "", "## Counts", "", ...Object.entries(payload.counts).map(([key, value]) => `- ${key}: \`${value}\``), "", "## Boundary", "", "Exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, and sibling-merge gates remain open.", ""].join("\n");
}

function refreshState(payload) {
  const lookup = [`docs/trinity-live-traces/${phaseSlug}-closeout-v1.json`, `docs/trinity-live-traces/${phaseSlug}-closeout-v1.md`];
  for (const file of [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.json")]) {
    const doc = JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = payload.overall_status;
    doc.current_active_phase = payload.next_active_phase;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = payload.latest_completed_x1_phase;
    doc.latest_completed_x2_phase = phaseSlug;
    doc.next_expected_scope = payload.next_active_phase;
    doc.next_x2_scope = payload.next_x2_scope;
    doc.next_x1_lane_after_x2 = payload.next_x1_lane_after_x2;
    doc.goal_mode_status = payload.goal_mode_status;
    doc.v554_v2_x2_closeout = { status: payload.overall_status, counts: payload.counts, full_goal_complete: false };
    doc.current_lookup_files = [...new Set([...(doc.current_lookup_files || []), ...lookup])];
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
    const mdFile = file.replace(/\.json$/, ".md");
    if (fs.existsSync(mdFile)) fs.writeFileSync(mdFile, renderBeaconMd(doc), "utf8");
  }
}

function renderBeaconMd(doc) {
  return ["# Omega Mini Current State", "", `Status: ${doc.status}`, `Current active phase: ${doc.current_active_phase}`, `Latest closed phase: ${doc.latest_closed_phase}`, `Latest completed x1: ${doc.latest_completed_x1_phase}`, `Latest completed x2: ${doc.latest_completed_x2_phase}`, `Next x2 scope: ${doc.next_x2_scope}`, `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`, "", "## Boundary", "", "Sanitized current-state beacon only; private routes and proof/canon/legal/deployment gates remain open.", ""].join("\n");
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) parsed.set(argv[index], argv[index + 1]);
  return parsed;
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", { timeZone: "Pacific/Auckland", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }).formatToParts(date);
  const map = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return `${map.year}-${map.month}-${map.day}T${map.hour}:${map.minute}:${map.second}+12:00`;
}

function boundary() {
  return { raw_browser_routes_published: false, private_urls_published: false, raw_transcripts_published: false, screenshots_published: false, credentials_published: false, local_absolute_paths_published: false, session_streams_published: false, private_dumps_published: false, private_callable_ids_published: false, raw_lane_text_published: false };
}

function claimBoundary(passed) {
  return { phase_completion: passed ? phaseSlug : "not_claimed", full_goal_completion: "not_claimed", gmut_empirical_closure: "not_claimed", final_physics: "not_claimed", consciousness_proof: "not_claimed", legal_closure: "not_claimed", canon_promotion: "not_claimed", deployment_closure: "not_claimed", account_mutation: "not_claimed", purchase: "not_claimed", api_key_creation: "not_claimed", private_material_proof: "not_claimed", raw_publication_proof: "not_claimed", sibling_identity_replacement_or_merge: "not_claimed" };
}
