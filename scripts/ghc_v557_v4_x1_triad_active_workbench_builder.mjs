#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const phaseSlug = "v557-gmut-thos-v4-x1";
const nextX2Scope = "v557-gmut-thos-v4-x2";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const startup = readOptional(`${phaseSlug}-main-startup-context-v1.json`);

const artifact = {
  artifact_type: "ghc_v557_v4_x1_triad_active_workbench",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "ACTIVE_OPEN_V557_V4_X1_TRIAD_BACKGROUND_RUNNING_SAFE_WORK_READY",
  startup_status: startup?.overall_status || startup?.status || "missing",
  lanes: {
    aster_vale: "strict_cli_background_watch_started_pending_completion_quality_marker_gates",
    kierkegaard: "recovered_app_lane_background_watch_started_pending_completion_gate",
    aristotle: "recovered_app_lane_background_watch_started_pending_completion_gate",
  },
  watcher_start_is_completion_proof: false,
  closeout_allowed_now: false,
  proposal_targets: {
    safe_packets: 20,
    candidate_packets: 12,
    exact_approval_packets: 12,
    skill_ideas: 20,
    runner_ideas: 8,
    cleanup_proposals: 40,
    web_reflections: 30,
    journey_phase_reflections: 30,
  },
  immediate_x1_safe_work: [
    "triad phase truth card",
    "strict CLI and recovered app-lane receipt index",
    "triad proposal scaffold",
    "ethics/governance/taxonomy boundary board",
    "privacy/open-gate rail",
    "v4 x2 build queue seed",
    "completion-gate harvest checklist",
    "compact-pause active-lane card",
  ],
  x2_build_queue_seed: [
    "reduce Aster evidence/source proposal set",
    "reduce Kierkegaard governance/ethics proposal set",
    "reduce Aristotle taxonomy/schema proposal set",
    "build v4 x2 safe execution reducer",
    "validate and publish sanitized triad closeout artifacts",
  ],
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

writePair("triad-active-workbench", artifact);
refreshBeacons(artifact);

process.stdout.write(JSON.stringify({
  status: artifact.overall_status,
  phase_slug: phaseSlug,
  lanes_active: 3,
  closeout_allowed_now: false,
  safe_work_items: artifact.immediate_x1_safe_work.length,
}, null, 2) + "\n");

function writePair(suffix, payload) {
  const base = `${phaseSlug}-${suffix}-v1`;
  writeJson(path.join(tracesDir, `${base}.json`), payload);
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderMd(payload), "utf8");
}

function refreshBeacons(payload) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-triad-active-workbench-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-triad-active-workbench-v1.md`,
  ];
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = payload.overall_status;
    doc.current_active_phase = phaseSlug;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = nextX2Scope;
    doc.v557_v4_x1_triad_workbench = {
      status: payload.overall_status,
      lanes_active: 3,
      watcher_start_is_completion_proof: false,
      closeout_allowed_now: false,
      proposal_targets: payload.proposal_targets,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function renderMd(data) {
  return [
    `# ${phaseSlug} Triad Active Workbench`,
    "",
    `Status: \`${data.overall_status}\``,
    `Closeout allowed now: \`${data.closeout_allowed_now}\``,
    `Watcher start is completion proof: \`${data.watcher_start_is_completion_proof}\``,
    "",
    "## Lanes",
    "",
    ...Object.entries(data.lanes).map(([lane, status]) => `- ${lane}: \`${status}\``),
    "",
    "## Immediate x1 Safe Work",
    "",
    ...data.immediate_x1_safe_work.map((item) => `- ${item}`),
    "",
    "## Boundary",
    "",
    "Active/open handoff only. No raw private route, callable ID, transcript, screenshot, credential, local absolute path, app state, proof closure, or sibling merge claim is published.",
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
    "",
    "## v557 v4 x1 Triad Workbench",
    "",
    `- status: \`${doc.v557_v4_x1_triad_workbench?.status || "not_recorded"}\``,
    `- lanes active: \`${doc.v557_v4_x1_triad_workbench?.lanes_active ?? "not_recorded"}\``,
    `- closeout allowed now: \`${doc.v557_v4_x1_triad_workbench?.closeout_allowed_now ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`),
    "",
  ].join("\n");
}

function readOptional(name) {
  try { return readJson(path.join(tracesDir, name)); } catch { return null; }
}
function readJson(file) { return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, "")); }
function writeJson(file, data) { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8"); }
function unique(values) { return [...new Set(values.filter(Boolean))]; }
function publicationBoundary() { return { raw_browser_routes_published: false, private_urls_published: false, raw_transcripts_published: false, screenshots_published: false, credentials_published: false, local_absolute_paths_published: false, session_streams_published: false, private_dumps_published: false, private_callable_ids_published: false, raw_lane_text_published: false, private_app_state_published: false }; }
function claimBoundary() { return { full_goal_completion: "not_claimed", gmut_empirical_closure: "not_claimed", final_physics: "not_claimed", consciousness_proof: "not_claimed", legal_closure: "not_claimed", canon_promotion: "not_claimed", deployment_closure: "not_claimed", account_mutation: "not_claimed", purchase: "not_claimed", api_key_creation: "not_claimed", private_material_proof: "not_claimed", raw_publication_proof: "not_claimed", sibling_identity_replacement_or_merge: "not_claimed" }; }
function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", { timeZone: "Pacific/Auckland", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
