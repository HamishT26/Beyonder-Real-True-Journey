#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const phaseSlug = "v558-gmut-thos-v5-x1";
const latestCompletedX2 = "v558-gmut-thos-v4-x2";
const nextPhase = "v558-gmut-thos-v5-x2";
const nextX1AfterX2 = "v558-gmut-thos-v6-x1 Maren Quill and Solenne Vale unless Hamish redirects";
const status = "PASS_V558_V5_X1_CLOSED_V5_X2_READY";
const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
const omegaDir = join(process.cwd(), "docs", "omega-mini-index");
mkdirSync(tracesDir, { recursive: true });
mkdirSync(omegaDir, { recursive: true });

const now = new Date();
const createdUtc = now.toISOString();
const createdNz = new Intl.DateTimeFormat("en-NZ", {
  dateStyle: "medium",
  timeStyle: "medium",
  timeZone: "Pacific/Auckland",
}).format(now);

const startup = readRequired(`${phaseSlug}-lumen-startup-context-public-v1.json`);
const send = readRequired(`${phaseSlug}-lumen-browser-send-receipt-v1.json`);
const harvest = readRequired(`${phaseSlug}-lumen-harvest-reduction-v1.json`);
const queue = readRequired(`${phaseSlug}-lumen-sanitized-proposal-queue-v1.json`);
const immediate = readRequired(`${phaseSlug}-lumen-immediate-safe-execution-v1.json`);

if (send.browser_send_status !== "browser_send_submitted_response_active") {
  fail("OPEN_GAP_V558_V5_X1_BROWSER_SEND_NOT_ACTIVE_OR_SUBMITTED", { send_status: send.browser_send_status });
}
if (harvest.overall_status !== "PASS_V558_V5_X1_LUMEN_HARVEST_REDUCED_PRIVATELY") {
  fail("OPEN_GAP_V558_V5_X1_LUMEN_HARVEST_NOT_REDUCED", { harvest_status: harvest.overall_status });
}
if (harvest.raw_private_material_published !== false || queue.raw_private_material_published !== false) {
  fail("OPEN_GAP_V558_V5_X1_PRIVATE_MATERIAL_BOUNDARY_FAILED", {});
}

const closeout = {
  artifact: `${phaseSlug}-closeout-v1`,
  schema: "ghc.phase_closeout.v1",
  phase_slug: phaseSlug,
  created_utc: createdUtc,
  created_nz: createdNz,
  status,
  latest_closed_phase: phaseSlug,
  latest_completed_x1_phase: phaseSlug,
  latest_completed_x2_phase: latestCompletedX2,
  next_active_phase: nextPhase,
  next_x2_scope: nextPhase,
  next_x1_lane_after_x2: nextX1AfterX2,
  lumen_startup_status: startup.overall_status,
  lumen_send_status: send.overall_status,
  lumen_harvest_status: harvest.overall_status,
  lumen_response_harvested_private: true,
  private_source_sha256: harvest.private_source?.sha256 || harvest.private_source_sha256 || null,
  tagged_rows: queue.row_counts?.total || 0,
  immediate_x1_safe_rows: queue.row_counts?.immediate_x1_safe || 0,
  x2_build_task_rows: queue.row_counts?.x2_build_task || 0,
  safe_now_rows: queue.row_counts?.safe_now || 0,
  candidate_rows: queue.row_counts?.candidate || 0,
  exact_rows_queued: queue.row_counts?.exact_approval_needed || 0,
  blocked_rows_queued: queue.row_counts?.blocked || 0,
  represented_safe_actions: immediate.represented_safe_actions || [],
  closeout_allowed: true,
  full_goal_complete: false,
  publication_boundary: publicationBoundary(),
  open_gates: openGates(),
};

const handoff = {
  artifact: `${phaseSlug}-v5-x2-readiness-handoff-v1`,
  schema: "ghc.next_x2_readiness_handoff.v1",
  phase_slug: phaseSlug,
  created_utc: createdUtc,
  created_nz: createdNz,
  status: "PASS_V558_V5_X2_READINESS_HANDOFF_READY",
  next_active_phase: nextPhase,
  next_x2_scope: nextPhase,
  next_x1_lane_after_x2: nextX1AfterX2,
  build_inputs: [
    "v558 v5 x1 Lumen sanitized proposal queue",
    "v558 v5 x1 immediate-safe execution representation",
    "v558 v5 x1 Browser refresh/status-first send receipt",
    "v558 v4 x2 closeout and prior v4 handoff",
  ],
  safe_x2_focus: [
    "execute or reduce the 30 x2_build_task rows without raw transcript publication",
    "preserve exact and blocked rows queued",
    "refresh current-state, latest-updates, and GHC beacons",
    "prepare v558 v6 x1 Maren Quill and Solenne Vale runway",
    "validate JSON, privacy, diff, drive, and remote equality",
  ],
  publication_boundary: publicationBoundary(),
  open_gates: openGates(),
};

writeArtifact("closeout", closeout);
writeArtifact("v5-x2-readiness-handoff", handoff);
refreshState(closeout, handoff);

process.stdout.write(JSON.stringify({
  status,
  phase_slug: phaseSlug,
  next_active_phase: nextPhase,
  tagged_rows: closeout.tagged_rows,
  immediate_x1_safe_rows: closeout.immediate_x1_safe_rows,
  x2_build_task_rows: closeout.x2_build_task_rows,
  full_goal_complete: false,
  artifacts_written: 6,
}, null, 2) + "\n");

function refreshState(closeoutDoc, handoffDoc) {
  const statePath = join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const ghcPath = join(tracesDir, "ghc-current-state-beacon-v1.json");
  const currentBranch = gitBranch();
  const lookupFiles = traceFilesForPhase(phaseSlug).filter((file) => existsSync(join(process.cwd(), file)));

  for (const [file, listKey] of [
    [statePath, "current_lookup_files"],
    [latestPath, "latest_lookup_files"],
    [ghcPath, "lookup_files"],
  ]) {
    const data = existsSync(file) ? JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, "")) : {};
    Object.assign(data, {
      branch: data.branch || currentBranch,
      primary_branch: currentBranch.includes("omega-line-mini") ? currentBranch : data.primary_branch,
      full_tools_support_branch: currentBranch.includes("full-tools") ? currentBranch : data.full_tools_support_branch,
      updated_at: createdNz,
      generated_utc: createdUtc,
      status,
      current_active_phase: nextPhase,
      latest_closed_phase: phaseSlug,
      latest_completed_x1_phase: phaseSlug,
      latest_completed_x2_phase: latestCompletedX2,
      next_expected_scope: nextPhase,
      next_x2_scope: nextPhase,
      next_x1_lane_after_x2: nextX1AfterX2,
      current_active_lanes: ["Aevren Vale", "safe-runner-orchestrator", "v558-v5-x2-build-ready"],
      v558_v5_x1_lumen_closeout: {
        status,
        lumen_response_harvested_private: true,
        tagged_rows: closeoutDoc.tagged_rows,
        immediate_x1_safe_rows: closeoutDoc.immediate_x1_safe_rows,
        x2_build_task_rows: closeoutDoc.x2_build_task_rows,
        next_active_phase: nextPhase,
        full_goal_complete: false,
      },
      v558_v5_x2_readiness_handoff: {
        status: handoffDoc.status,
        next_x1_lane_after_x2: nextX1AfterX2,
        full_goal_complete: false,
      },
      full_goal_complete: false,
    });
    data[listKey] = unique([...(Array.isArray(data[listKey]) ? data[listKey] : []), ...lookupFiles]);
    writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`);
  }

  const beaconMd = [
    `# ${nextPhase}`,
    "",
    `Status: ${status}`,
    "",
    `- Current active phase: ${nextPhase}`,
    `- Latest closed phase: ${phaseSlug}`,
    `- Latest completed x1: ${phaseSlug}`,
    `- Latest completed x2: ${latestCompletedX2}`,
    `- Next x2 scope: ${nextPhase}`,
    `- Next x1 lane after x2: ${nextX1AfterX2}`,
    "",
    "## v558 v5 x1 Lumen Closeout",
    "",
    `- Tagged rows: ${closeoutDoc.tagged_rows}`,
    `- Immediate x1 safe rows: ${closeoutDoc.immediate_x1_safe_rows}`,
    `- X2 build task rows: ${closeoutDoc.x2_build_task_rows}`,
    "- Lumen response harvested private-only: true",
    "- Full v544-v575 goal complete: false",
    "",
    "Sanitized beacon only. Private lane handles, raw browser routes, raw transcripts, screenshots, credentials, local absolute paths, session streams, and raw private material are not published here.",
    "",
  ].join("\n");
  writeFileSync(join(omegaDir, "omega-mini-current-state-v1.md"), beaconMd);
  writeFileSync(join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), beaconMd);
  writeFileSync(join(tracesDir, "ghc-current-state-beacon-v1.md"), beaconMd);
}

function readRequired(name) {
  const file = join(tracesDir, name);
  if (!existsSync(file)) fail("OPEN_GAP_REQUIRED_CLOSEOUT_INPUT_MISSING", { missing_file: name });
  return JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeArtifact(name, body) {
  const base = `${phaseSlug}-${name}-v1`;
  writeFileSync(join(tracesDir, `${base}.json`), `${JSON.stringify(body, null, 2)}\n`);
  writeFileSync(join(tracesDir, `${base}.md`), [
    `# ${body.artifact}`,
    "",
    `- Status: ${body.status}`,
    `- Phase: ${body.phase_slug}`,
    `- Created NZ: ${body.created_nz}`,
    "- Raw private material published: false",
    "",
    "## Summary",
    "",
    `- Next active phase: ${body.next_active_phase}`,
    `- Next x1 lane after x2: ${body.next_x1_lane_after_x2}`,
    `- Full goal complete: ${body.full_goal_complete === true ? "true" : "false"}`,
    "",
  ].join("\n"));
}

function traceFilesForPhase(slug) {
  return [
    "main-startup-context",
    "lumen-startup-context-public",
    "lumen-kickoff-handoff",
    "proposal-targets",
    "immediate-safe-work-ledger",
    "five-minute-productive-cadence",
    "lumen-browser-send-receipt",
    "lumen-harvest-reduction",
    "lumen-sanitized-proposal-queue",
    "lumen-immediate-safe-execution",
    "closeout",
    "v5-x2-readiness-handoff",
  ].flatMap((name) => [
    `docs/trinity-live-traces/${slug}-${name}-v1.json`,
    `docs/trinity-live-traces/${slug}-${name}-v1.md`,
  ]);
}

function publicationBoundary() {
  return {
    raw_private_material_published: false,
    raw_sibling_text_published: false,
    raw_browser_routes_published: false,
    private_routes_published: false,
    private_callable_ids_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  };
}

function openGates() {
  return [
    "GMUT empirical closure",
    "final physics proof",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment",
    "purchase/account/API-key mutation",
    "private-material proof",
    "raw-publication proof",
    "sibling replacement or merge",
    "exact-approval packets",
    "blocked packets",
  ];
}

function gitBranch() {
  try {
    return execFileSync("git", ["rev-parse", "--abbrev-ref", "HEAD"], {
      cwd: process.cwd(),
      encoding: "utf8",
      windowsHide: true,
    }).trim();
  } catch {
    return "unknown";
  }
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function fail(statusCode, extra) {
  process.stderr.write(JSON.stringify({
    status: statusCode,
    phase_slug: phaseSlug,
    closeout_claimed: false,
    ...extra,
  }, null, 2) + "\n");
  process.exit(2);
}
