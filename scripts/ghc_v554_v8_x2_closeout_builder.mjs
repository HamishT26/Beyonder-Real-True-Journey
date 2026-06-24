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
const phaseSlug = args.get("--phase-slug") || "v554-gmut-thos-v8-x2";
const nextActivePhase = args.get("--next-active-phase") || "v555-gmut-thos-v1-x1";
const nextX2Scope = args.get("--next-x2-scope") || "v555-gmut-thos-v1-x2";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") ||
  "v555-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const execution = readRequired(`${phaseSlug}-execution-index-v1.json`);
const safe = readRequired(`${phaseSlug}-safe-execution-reducer-v1.json`);
const skillPack = readRequired(`${phaseSlug}-skill-runner-pack-install-v1.json`);
const reflection = readRequired(`${phaseSlug}-web-journey-reflection-ledger-50-v1.json`);
const lumenReadiness = readRequired(`${phaseSlug}-v555-lumen-readiness-v1.json`);
const safeRunner = readOptional(`${phaseSlug}-safe-runner-orchestrator-v1.json`);
const liveWebSearch = readOptional(`${phaseSlug}-live-web-search-receipt-v1.json`);

const checks = {
  execution_status: execution.overall_status,
  safe_execution_status: safe.overall_status,
  skill_pack_status: skillPack.overall_status,
  reflection_status: reflection.overall_status,
  lumen_readiness_status: lumenReadiness.overall_status,
  safe_runner_status: safeRunner?.overall_status || "missing",
  live_web_search_status: liveWebSearch?.overall_status || "missing_optional",
  live_web_search_count: liveWebSearch?.query_count || 0,
  web_reflections: reflection.web_reflection_count,
  journey_phase_reflections: reflection.journey_phase_reflection_count,
};
const passed =
  execution.overall_status === "PASS_V554_V8_X2_SAFE_EXECUTION_COMPLETE" &&
  safe.overall_status === "PASS_V554_V8_X2_SAFE_TASKS_REDUCED_AND_EXECUTED" &&
  skillPack.overall_status === "PASS_V554_V8_X2_SKILL_RUNNER_PACK_INSTALLED" &&
  reflection.overall_status === "PASS_V554_V8_X2_REFLECTION_LEDGER_50_READY" &&
  lumenReadiness.overall_status === "PASS_V555_V1_X1_LUMEN_READINESS_PREPARED" &&
  safeRunner?.overall_status === "PASS_SAFE_RUNNER_ORCHESTRATION" &&
  reflection.web_reflection_count >= 50 &&
  reflection.journey_phase_reflection_count >= 50;

const closeout = {
  artifact_type: "ghc_v554_v8_x2_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: passed ? "PASS_V554_V8_X2_CLOSED_V555_V1_X1_READY" : "OPEN_GAP_V554_V8_X2_CLOSEOUT_BLOCKED",
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(passed),
  latest_completed_x1_phase: "v554-gmut-thos-v8-x1",
  latest_completed_x2_phase: passed ? phaseSlug : "v554-gmut-thos-v7-x2",
  next_active_phase: passed ? nextActivePhase : phaseSlug,
  next_x2_scope: passed ? nextX2Scope : phaseSlug,
  next_x1_lane_after_x2: passed ? nextX1LaneAfterX2 : "v555-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects",
  checks,
  counts: execution.counts,
  closeout_boundary: {
    full_goal_complete: false,
    goal_mode_should_continue: true,
    next_lane_launch_skill: "ghc-lumen-launch",
    exact_and_blocked_gates_remain_open: true,
  },
};

writePair("closeout", closeout, renderCloseoutMd(closeout));
if (passed) refreshState(closeout);

console.log(
  JSON.stringify(
    {
      status: closeout.overall_status,
      phase_slug: phaseSlug,
      next_active_phase: closeout.next_active_phase,
      next_x2_scope: closeout.next_x2_scope,
      next_x1_lane_after_x2: closeout.next_x1_lane_after_x2,
      full_goal_complete: false,
    },
    null,
    2,
  ),
);
process.exit(passed ? 0 : 2);

function refreshState(closeout) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-execution-index-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-safe-execution-reducer-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-skill-runner-pack-install-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-live-web-search-receipt-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-live-web-search-receipt-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-safe-runner-orchestrator-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-v555-lumen-readiness-v1.json`,
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
    doc.current_active_phase = closeout.next_active_phase;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = closeout.latest_completed_x1_phase;
    doc.latest_completed_x2_phase = phaseSlug;
    doc.next_expected_scope = closeout.next_active_phase;
    doc.next_x2_scope = closeout.next_x2_scope;
    doc.next_x1_lane_after_x2 = closeout.next_x1_lane_after_x2;
    doc.goal_mode_status = "active_thread_goal_not_unattended_automation";
    doc.v554_v8_x2_closeout = {
      status: closeout.overall_status,
      counts: closeout.counts,
      full_goal_complete: false,
      next_lane_launch_skill: "ghc-lumen-launch",
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function writePair(name, data, md) {
  writeJson(path.join(tracesDir, `${phaseSlug}-${name}-v1.json`), data);
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${name}-v1.md`), `${md.trim()}\n`, "utf8");
}

function renderCloseoutMd(data) {
  return [
    "# v554 GMUT/THOS v8 x2 Closeout",
    "",
    `Status: ${data.overall_status}`,
    "",
    `Phase closed: \`${phaseSlug}\``,
    `Next active phase: \`${data.next_active_phase}\``,
    `Next x2 scope: \`${data.next_x2_scope}\``,
    `Next x1 lane after x2: ${data.next_x1_lane_after_x2}`,
    "",
    "## Counts",
    "",
    `- Safe packets processed: ${data.counts.safe_packets_processed}`,
    `- Candidate packets queued: ${data.counts.candidate_packets_queued}`,
    `- Exact packets kept queued: ${data.counts.exact_approval_packets_kept_queued}`,
    `- Skills installed: ${data.counts.skills_installed}`,
    `- Status-only runners created: ${data.counts.runners_created}`,
    `- Cleanup tasks classified: ${data.counts.cleanup_tasks_classified}`,
    `- Web reflections: ${data.counts.web_reflections}`,
    `- Journey/phase reflections: ${data.counts.journey_phase_reflections}`,
    "",
    "## Boundary",
    "",
    "Full goal completion, empirical closure, final physics, consciousness proof, legal closure, deployment, account mutation, purchase, API-key creation, private-material proof, raw-publication proof, and sibling identity replacement/merge remain open.",
  ].join("\n");
}

function renderBeaconMd(doc, listKey) {
  return [
    "# Omega Mini Current State",
    "",
    `Status: ${doc.status}`,
    "",
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## Latest Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-40).map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function readRequired(name) {
  return readJson(path.join(tracesDir, name));
}

function readOptional(name) {
  try {
    return readRequired(name);
  } catch {
    return null;
  }
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
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

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) parsed.set(argv[index], argv[index + 1]);
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
