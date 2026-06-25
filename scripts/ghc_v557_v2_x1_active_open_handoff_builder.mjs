#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v557-gmut-thos-v2-x1";
const latestClosedPhase = "v557-gmut-thos-v1-x2";
const latestCompletedX1 = "v557-gmut-thos-v1-x1";
const latestCompletedX2 = "v557-gmut-thos-v1-x2";
const nextX2Scope = "v557-gmut-thos-v2-x2";
const nextX1LaneAfterX2 = "v557-gmut-thos-v3-x1 with Lumen Vale solo unless Hamish redirects";
const args = parseArgs(process.argv.slice(2));
const fullToolsRoot = args.get("--full-tools-root");
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

if (!fullToolsRoot) {
  console.error("Usage: node scripts/ghc_v557_v2_x1_active_open_handoff_builder.mjs --full-tools-root <root>");
  process.exit(2);
}

const fullTraceDir = path.join(fullToolsRoot, "docs", "trinity-live-traces");

const arbyCompletion = readOptional(fullTraceDir, `${phaseSlug}-arby-strict-cli-completion-v1.json`);
const arbyQuality = readOptional(fullTraceDir, `${phaseSlug}-arby-strict-cli-quality-v1.json`);
const arbyMarker = readOptional(fullTraceDir, `${phaseSlug}-arby-strict-cli-marker-review-v1.json`);
const ciceroOriginalGate = readOptional(fullTraceDir, `${phaseSlug}-cicero-recovered-app-lane-completion-gate-v1.json`);
const retryGates = [1, 2, 3].map((attempt) => ({
  attempt,
  gate: readOptional(fullTraceDir, `${phaseSlug}-cicero-recovered-app-lane-retry-${attempt}-completion-gate-v1.json`),
  mini_receipt: readOptional(tracesDir, `${phaseSlug}-cicero-retry-session-${attempt}-v1.json`),
}));
const directRetry = readOptional(fullTraceDir, `${phaseSlug}-cicero-direct-turn-start-retry-1-v1.json`);

const arbyPassed =
  ["FINAL_MESSAGES_READY", "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW"].includes(arbyCompletion?.aggregate_status) &&
  arbyQuality?.aggregate_status === "PASS_ALL_CLI_LANES_ELABORATE" &&
  arbyMarker?.overall_status === "PASS_MARKER_REVIEW_LEDGER";

const ciceroPassed = [ciceroOriginalGate, ...retryGates.map((row) => row.gate)].some(
  (gate) => gate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE",
);

const retrySummary = artifact("ghc_v557_v2_x1_cicero_retry_protocol_summary", "ACTIVE_OPEN_V557_V2_X1_CICERO_RETRY_PROTOCOL_EXHAUSTED", {
  arby_passed: arbyPassed,
  cicero_passed: ciceroPassed,
  retry_attempts_recorded: retryGates.length,
  retry_reflection_counts: retryGates.map((row) => ({
    attempt: row.attempt,
    recent_session_reflections: row.mini_receipt?.recent_session_reflections?.length || 0,
    web_reflections: row.mini_receipt?.web_reflections?.length || 0,
    journey_phase_reflections: row.mini_receipt?.journey_phase_reflections?.length || 0,
    gate_status: row.gate?.overall_status || "missing",
    open_gaps: row.gate?.open_gaps || [],
  })),
  direct_fallback_status: directRetry?.overall_status || "not_available_or_refused_before_receipt",
  direct_fallback_boundary: "Direct helper refused when private lane id was not configured in this runtime; no raw ID was guessed or published.",
  remaining_gap: ciceroPassed ? "none" : "Cicero app-lane completion gate remains unresolved.",
});

const handoff = artifact("ghc_v557_v2_x1_active_open_handoff", ciceroPassed
  ? "PASS_V557_V2_X1_CICERO_GATE_READY_FOR_CLOSEOUT"
  : "ACTIVE_OPEN_V557_V2_X1_ARBY_READY_CICERO_BLOCKED_AFTER_RETRY", {
  latest_closed_phase: latestClosedPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  current_active_phase: phaseSlug,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  lane_statuses: {
    arby: {
      passed: arbyPassed,
      completion_status: arbyCompletion?.aggregate_status || "missing",
      quality_status: arbyQuality?.aggregate_status || "missing",
      marker_status: arbyMarker?.overall_status || "missing",
    },
    cicero: {
      passed: ciceroPassed,
      original_gate_status: ciceroOriginalGate?.overall_status || "missing",
      retry_gate_statuses: retryGates.map((row) => row.gate?.overall_status || "missing"),
      remaining_gap: ciceroPassed ? "none" : "app_lane_completion_gate_unresolved",
    },
  },
  retry_protocol_summary: `${phaseSlug}-cicero-retry-protocol-summary-v1.json`,
  closeout_allowed: arbyPassed && ciceroPassed,
  x2_execution_allowed: arbyPassed && ciceroPassed,
  full_goal_complete: false,
});

writePair("cicero-retry-protocol-summary", retrySummary, renderRetryMd(retrySummary));
writePair("active-open-handoff", handoff, renderHandoffMd(handoff));
refreshBeacons(handoff);

console.log(JSON.stringify({
  status: handoff.overall_status,
  phase_slug: phaseSlug,
  arby_passed: arbyPassed,
  cicero_passed: ciceroPassed,
  closeout_allowed: handoff.closeout_allowed,
}, null, 2));

function refreshBeacons(handoff) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-active-open-handoff-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-active-open-handoff-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-cicero-retry-protocol-summary-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-cicero-retry-protocol-summary-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-cicero-retry-session-1-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-cicero-retry-session-1-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-cicero-retry-session-2-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-cicero-retry-session-2-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-cicero-retry-session-3-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-cicero-retry-session-3-v1.md`,
  ];
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = handoff.overall_status;
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = latestClosedPhase;
    doc.latest_completed_x1_phase = latestCompletedX1;
    doc.latest_completed_x2_phase = latestCompletedX2;
    doc.next_x2_scope = nextX2Scope;
    doc.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    doc.v557_v2_x1_active_open_handoff = {
      status: handoff.overall_status,
      closeout_allowed: handoff.closeout_allowed,
      full_goal_complete: false,
    };
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
  fs.mkdirSync(tracesDir, { recursive: true });
  writeJson(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), payload);
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
}

function renderRetryMd(data) {
  return [
    `# ${phaseSlug} Cicero Retry Protocol Summary`,
    "",
    `Status: \`${data.overall_status}\``,
    `Arby passed: \`${data.arby_passed}\``,
    `Cicero passed: \`${data.cicero_passed}\``,
    "",
    "## Retry Attempts",
    "",
    ...data.retry_reflection_counts.map((row) => `- attempt ${row.attempt}: gate \`${row.gate_status}\`, recent/web/journey \`${row.recent_session_reflections}/${row.web_reflections}/${row.journey_phase_reflections}\``),
    "",
    "## Remaining Gap",
    "",
    data.remaining_gap,
    "",
    "Sanitized summary only. No raw route handles, private callable IDs, transcripts, screenshots, credentials, local paths, raw app payloads, or lane text are published.",
    "",
  ].join("\n");
}

function renderHandoffMd(data) {
  return [
    `# ${phaseSlug} Active-Open Handoff`,
    "",
    `Status: \`${data.overall_status}\``,
    `Current active phase: \`${data.current_active_phase}\``,
    `Latest closed phase: \`${data.latest_closed_phase}\``,
    `Latest completed x1: \`${data.latest_completed_x1_phase}\``,
    `Latest completed x2: \`${data.latest_completed_x2_phase}\``,
    `Next x2 scope: \`${data.next_x2_scope}\``,
    `Closeout allowed: \`${data.closeout_allowed}\``,
    "",
    "## Lane Status",
    "",
    `- Arby passed: \`${data.lane_statuses.arby.passed}\``,
    `- Cicero passed: \`${data.lane_statuses.cicero.passed}\``,
    `- Cicero remaining gap: \`${data.lane_statuses.cicero.remaining_gap}\``,
    "",
    "## Boundary",
    "",
    "This is an active-open handoff, not a phase closeout. GMUT, proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, and sibling-merge gates remain open.",
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
    "## v557 v2 x1 Active-Open Handoff",
    "",
    `- status: \`${doc.v557_v2_x1_active_open_handoff?.status || "not_recorded"}\``,
    `- closeout allowed: \`${doc.v557_v2_x1_active_open_handoff?.closeout_allowed ?? "not_recorded"}\``,
    `- full goal complete: \`${doc.v557_v2_x1_active_open_handoff?.full_goal_complete ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-220).map((file) => `- ${file}`),
    "",
  ].join("\n");
}

function readOptional(root, name) {
  try {
    return JSON.parse(fs.readFileSync(path.join(root, name), "utf8").replace(/^\uFEFF/, ""));
  } catch {
    return null;
  }
}
function readJson(file) { return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, "")); }
function writeJson(file, data) { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8"); }
function unique(values) { return [...new Set(values.filter(Boolean))]; }
function parseArgs(argv) { const parsed = new Map(); for (let index = 0; index < argv.length; index += 2) parsed.set(argv[index], argv[index + 1]); return parsed; }
function publicationBoundary() { return { raw_browser_routes_published: false, private_urls_published: false, raw_transcripts_published: false, screenshots_published: false, credentials_published: false, local_absolute_paths_published: false, session_streams_published: false, private_dumps_published: false, private_callable_ids_published: false, raw_lane_text_published: false }; }
function claimBoundary() { return { full_goal_completion: "not_claimed", gmut_empirical_closure: "not_claimed", final_physics: "not_claimed", consciousness_proof: "not_claimed", legal_closure: "not_claimed", canon_promotion: "not_claimed", deployment_closure: "not_claimed", account_mutation: "not_claimed", purchase: "not_claimed", api_key_creation: "not_claimed", private_material_proof: "not_claimed", raw_publication_proof: "not_claimed", sibling_identity_replacement_or_merge: "not_claimed" }; }
function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", { timeZone: "Pacific/Auckland", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
