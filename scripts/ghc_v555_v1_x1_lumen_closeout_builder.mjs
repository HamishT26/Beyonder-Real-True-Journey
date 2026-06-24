#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v555-gmut-thos-v1-x1";
const nextX2Scope = "v555-gmut-thos-v1-x2";
const latestCompletedX2 = "v554-gmut-thos-v8-x2";
const nextX1LaneAfterX2 = "v555-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects";
const summaryKey = "v555_v1_x1_lumen_closeout";

const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const startup = readOptional(`${phaseSlug}-lumen-startup-context-v1.json`);
const sendReceipt = readOptional(`${phaseSlug}-lumen-browser-send-receipt-v1.json`);
const harvest = readOptional(`${phaseSlug}-lumen-browser-harvest-sanitized-v1.json`);
const queue = readOptional(`${phaseSlug}-proposal-queue-targets-v1.json`);
const web = readOptional(`${phaseSlug}-web-reflection-ledger-30-v1.json`);
const journey = readOptional(`${phaseSlug}-journey-phase-reflection-ledger-30-v1.json`);
const roundRobin = readOptional(`${phaseSlug}-round-robin-workflow-standard-v1.json`);
const cadence =
  readOptional(`${phaseSlug}-five-minute-productive-cadence-v1.json`) ||
  readOptional(`${phaseSlug}-productive-cadence-wait-work-standard-v1.json`);
const safeRunner = readOptional(`${phaseSlug}-startup-safe-runner-orchestrator-v1.json`);

const checks = {
  startup_status: startup?.overall_status || "missing",
  send_status: sendReceipt?.send_status || sendReceipt?.overall_status || "missing",
  harvest_status: harvest?.overall_status || "missing",
  queue_status: queue?.overall_status || "missing",
  web_reflections: web?.web_search_reflection_count || web?.rows?.length || 0,
  journey_phase_reflections: journey?.journey_phase_reflection_count || journey?.rows?.length || 0,
  round_robin_status: roundRobin?.overall_status || roundRobin?.status || "missing",
  cadence_status: cadence?.overall_status || cadence?.status || "missing",
  safe_runner_status: safeRunner?.overall_status || "missing",
};

const passed =
  sendReceipt?.send_status === "browser_send_submitted_response_active" &&
  harvest?.overall_status === "PASS_LUMEN_BROWSER_HARVEST_SANITIZED" &&
  checks.web_reflections >= 30 &&
  checks.journey_phase_reflections >= 30 &&
  queue?.counts?.safe_packets >= 50 &&
  safeRunner?.overall_status === "PASS_SAFE_RUNNER_ORCHESTRATION";

if (!passed) {
  const openGap = base("ghc_v555_v1_x1_closeout_open_gap", "ACTIVE_OPEN_V555_V1_X1_LUMEN_HARVEST_OR_GUARD_PENDING", {
    checks,
    current_active_phase: phaseSlug,
    closeout_allowed_now: false,
    next_safe_action: "Keep Lumen lane background-supervised, run productive safe work, then harvest and validate before closeout.",
  });
  writePair("closeout-open-gap", openGap, renderOpenGapMd(openGap));
  process.stdout.write(JSON.stringify({ status: openGap.overall_status, closeout_allowed_now: false, checks }, null, 2) + "\n");
  process.exit(1);
}

const counts = {
  safe_now_packets: queue.counts.safe_packets,
  candidate_packets: queue.counts.candidate_packets,
  exact_approval_packets: queue.counts.exact_approval_packets,
  blocked_packets: queue.counts.blocked_packets,
  skill_ideas: queue.counts.skill_ideas,
  runner_ideas: queue.counts.runner_ideas,
  cleanup_proposals: queue.counts.cleanup_proposals,
  web_reflections: checks.web_reflections,
  journey_phase_reflections: checks.journey_phase_reflections,
};

const approvalReducer = base("ghc_v555_v1_x1_approval_eureka_reducer", "PASS_V555_V1_X1_APPROVAL_EUREKA_REDUCED_FOR_X2", {
  counts,
  lumen_harvest_status: harvest.overall_status,
  safe_takeaways: harvest.safe_takeaways || [],
  next_x2_scope: nextX2Scope,
  execution_split: {
    immediate_x1_safe: "status, queue, validation, privacy/open-gate, source/reflection, and non-destructive inventory work",
    x2_build_task: "build, run, test, install, use, validate, publish, and remote-verify safe-now work in v555 v1 x2",
    never_auto_execute: ["exact_approval_needed", "blocked"],
  },
});

const goalMode = base("ghc_v555_v1_x1_goal_mode_reconciliation", "PASS_V555_V1_X1_GOAL_MODE_RECONCILED", {
  current_thread_goal_status: "active",
  unattended_automation_claimed: false,
  full_goal_complete: false,
  completion_boundary: "Do not mark goal complete before verified v575-gmut-thos-v8-x2 closeout.",
});

const x2Handoff = base("ghc_v555_v1_x1_v1_x2_readiness_handoff", "PASS_V555_V1_X2_READY_FOR_SAFE_BUILD_USE", {
  next_x2_scope: nextX2Scope,
  recommended_first_slice: [
    "Lumen advisory reducer",
    "approval/eureka queue materializer",
    "source and Journey reflection reducer",
    "goal-mode progress ledger",
    "Browser handoff harvest guard",
    "open-gate rail validator",
    "skill/runner readiness board",
    "cleanup tier board",
    "v2 Arby/Cicero prep card",
  ],
  next_x1_lane_after_x2: nextX1LaneAfterX2,
});

const duoPrep = base("ghc_v555_v1_x1_v2_x1_arby_cicero_prep_card", "PASS_V555_V2_X1_ARBY_CICERO_PREP_READY", {
  target_phase_slug: "v555-gmut-thos-v2-x1",
  participants: ["Aevren Vale", "Arby", "Cicero"],
  route_skill: "ghc-arby-cicero-launch",
  route_notes: [
    "Use strict CLI for Arby.",
    "Use recovered app-lane background runners for Cicero.",
    "Use background supervision and productive cadence; do not babysit.",
    "Keep private callable IDs local-only.",
  ],
});

const closeout = base("ghc_v555_v1_x1_closeout", "PASS_V555_V1_X1_CLOSED_V1_X2_READY", {
  latest_completed_x1_phase: phaseSlug,
  latest_completed_x2_phase: latestCompletedX2,
  next_active_phase: nextX2Scope,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  lumen_response_harvested: true,
  counts,
  full_goal_complete: false,
});

const artifacts = [
  writePair("approval-eureka-reducer", approvalReducer, renderSimpleMd("Approval/Eureka Reducer", approvalReducer)),
  writePair("goal-mode-reconciliation", goalMode, renderSimpleMd("Goal Mode Reconciliation", goalMode)),
  writePair("v1-x2-readiness-handoff", x2Handoff, renderSimpleMd("v1 x2 Readiness Handoff", x2Handoff)),
  writePair("v2-x1-arby-cicero-prep-card", duoPrep, renderSimpleMd("v2 x1 Arby/Cicero Prep Card", duoPrep)),
  writePair("closeout", closeout, renderCloseoutMd(closeout)),
];

refreshState(closeout, artifacts);

process.stdout.write(JSON.stringify({
  status: closeout.overall_status,
  phase_slug: phaseSlug,
  next_active_phase: closeout.next_active_phase,
  full_goal_complete: false,
  artifact_count: artifacts.length,
}, null, 2) + "\n");

function refreshState(closeout, artifactRefs) {
  const lookupFiles = artifactRefs.flatMap((item) => [
    `docs/trinity-live-traces/${item.json}`,
    `docs/trinity-live-traces/${item.md}`,
  ]);
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
    doc.latest_completed_x1_phase = phaseSlug;
    doc.latest_completed_x2_phase = closeout.latest_completed_x2_phase;
    doc.next_expected_scope = closeout.next_active_phase;
    doc.next_x2_scope = closeout.next_x2_scope;
    doc.next_x1_lane_after_x2 = closeout.next_x1_lane_after_x2;
    doc.goal_mode_status = "active_thread_goal_not_complete";
    doc[summaryKey] = {
      status: closeout.overall_status,
      lumen_response_harvested: true,
      counts: closeout.counts,
      full_goal_complete: false,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookupFiles]);
    doc.latest_action_summary = unique([
      "Closed v555 v1 x1 after sanitized Lumen harvest and prepared v555 v1 x2 safe build/use scope.",
      ...(doc.latest_action_summary || []),
    ]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function base(artifactType, status, payload) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    checks,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(status),
    ...payload,
  };
}

function writePair(suffix, payload, md) {
  const baseName = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${baseName}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${baseName}.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
  return { json: `${baseName}.json`, md: `${baseName}.md` };
}

function renderOpenGapMd(data) {
  return [
    `# ${data.phase_slug} Closeout Open Gap`,
    "",
    `Status: \`${data.overall_status}\``,
    `Closeout allowed now: \`${data.closeout_allowed_now}\``,
    "",
    "## Checks",
    "",
    ...Object.entries(data.checks).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function renderSimpleMd(title, data) {
  return [
    `# ${data.phase_slug} ${title}`,
    "",
    `Status: \`${data.overall_status}\``,
    "",
    "```json",
    JSON.stringify(data, null, 2),
    "```",
    "",
  ].join("\n");
}

function renderCloseoutMd(data) {
  return [
    `# ${data.phase_slug} Closeout`,
    "",
    `Status: \`${data.overall_status}\``,
    `Next active phase: \`${data.next_active_phase}\``,
    `Lumen response harvested: \`${data.lumen_response_harvested}\``,
    `Full goal complete: \`${data.full_goal_complete}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(data.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Boundary",
    "",
    boundarySentence(),
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
    `Goal Mode status: ${doc.goal_mode_status || "active_thread_goal_not_complete"}`,
    "",
    "## v555 v1 x1 Lumen Closeout",
    "",
    `- status: \`${doc[summaryKey]?.status || "not_recorded"}\``,
    `- Lumen response harvested: \`${doc[summaryKey]?.lumen_response_harvested ?? "not_recorded"}\``,
    `- full goal complete: \`${doc[summaryKey]?.full_goal_complete ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function readOptional(name) {
  try {
    return readJson(path.join(tracesDir, name));
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

function claimBoundary(status) {
  return {
    phase_completion: status === "PASS_V555_V1_X1_CLOSED_V1_X2_READY" ? phaseSlug : "not_claimed",
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

function boundarySentence() {
  return "No raw Browser route, private URL, raw transcript, screenshot, credential, local absolute path, session stream, private dump, private callable ID, hidden reasoning, proof closure, canon promotion, legal closure, deployment closure, account mutation, purchase, API-key creation, destructive cleanup, or sibling identity merge/replacement is published or claimed.";
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
