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
const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v4-x1";
const appGateJson = args.get("--app-gate-json");
const asterCompletionJson = args.get("--aster-completion-json");
const asterQualityJson = args.get("--aster-quality-json");
const asterMarkerJson = args.get("--aster-marker-json");
const commit = args.get("--commit") || "unknown";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

if (!appGateJson || !asterCompletionJson || !asterQualityJson || !asterMarkerJson) {
  console.error("Usage: node ghc_v557_v4_x1_triad_closeout_builder.mjs --app-gate-json <file> --aster-completion-json <file> --aster-quality-json <file> --aster-marker-json <file>");
  process.exit(2);
}

const appGate = readJson(appGateJson);
const asterCompletion = readJson(asterCompletionJson);
const asterQuality = readJson(asterQualityJson);
const asterMarker = readJson(asterMarkerJson);
const asterMarkerStatus = asterMarker.status || asterMarker.overall_status;
const suite = readJson(path.join(tracesDir, `${phaseSlug}-lumen-prototype-suite-index-v1.json`));

const appLanesCompleted = Array.isArray(appGate.lanes)
  ? appGate.lanes.filter((lane) => lane.overall_status === "completed").length
  : 0;
const asterQualityLane = Array.isArray(asterQuality.lanes) ? asterQuality.lanes[0] || {} : {};
const asterCompletionLane = Array.isArray(asterCompletion.lanes) ? asterCompletion.lanes[0] || {} : {};

const closeoutPassed =
  appGate.overall_status === "PASS_APP_LANE_COMPLETION_GATE" &&
  appLanesCompleted === 2 &&
  asterCompletion.aggregate_status === "FINAL_MESSAGES_READY" &&
  asterQuality.aggregate_status === "PASS_ALL_CLI_LANES_ELABORATE" &&
  asterMarkerStatus === "PASS_MARKER_REVIEW_LEDGER";

const closeout = {
  artifact_type: "ghc_v557_v4_x1_triad_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: closeoutPassed ? "PASS_V557_V4_X1_CLOSED_V4_X2_READY" : "OPEN_GAP_V557_V4_X1_CLOSEOUT_NOT_PROVEN",
  sanitized_publication_commit_before_closeout: commit,
  latest_closed_phase: closeoutPassed ? phaseSlug : "v557-gmut-thos-v3-x2",
  next_active_phase: closeoutPassed ? "v557-gmut-thos-v4-x2" : phaseSlug,
  next_x2_scope: "v557-gmut-thos-v4-x2",
  next_x1_lane_after_x2: "v557-gmut-thos-v5-x1 with Lumen Vale solo unless Hamish redirects",
  lane_evidence: {
    aster_vale: {
      route: "strict_cli",
      completion_status: asterCompletion.aggregate_status,
      final_message_hash: asterCompletionLane.final_message_hash || null,
      final_message_bytes: asterCompletionLane.final_message_bytes || null,
      quality_status: asterQuality.aggregate_status,
      marker_status: asterMarkerStatus,
      word_count: asterQualityLane.word_count || null,
      numbered_or_bullet_item_count: asterQualityLane.numbered_or_bullet_item_count || null,
      category_item_counts: asterQualityLane.category_item_counts || {},
      raw_output_published: false,
    },
    kierkegaard: {
      route: "recovered_app_lane",
      completion_gate: appGate.overall_status,
      lane_status: laneStatus(appGate, "Kierkegaard"),
    },
    aristotle: {
      route: "recovered_app_lane",
      completion_gate: appGate.overall_status,
      lane_status: laneStatus(appGate, "Aristotle"),
    },
  },
  triad_profile_targets: {
    safe_packets: 20,
    candidate_packets: 12,
    exact_approval_packets: 12,
    skill_ideas: 20,
    runner_ideas: 8,
    cleanup_proposals: 40,
    web_reflections: 30,
    journey_phase_reflections: 30,
  },
  x2_carry_forward: {
    status: "READY_FOR_V557_V4_X2_BUILD_USE_SCOPE",
    lumen_prototype_suite_status: suite.overall_status,
    prototypes_ready: Array.isArray(suite.prototypes_run) ? suite.prototypes_run.length : 0,
    raw_proposal_bodies_published: false,
    next_action: "build/use x2 reducers and dashboards from sanitized hashes, lane counts, and open-gate policies",
  },
  full_goal_complete: false,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const refs = writePair("closeout", closeout);
refreshBeacons(refs, closeout);

process.stdout.write(JSON.stringify({
  status: closeout.overall_status,
  phase_slug: phaseSlug,
  app_lanes_completed: appLanesCompleted,
  aster_completion_status: asterCompletion.aggregate_status,
  aster_quality_status: asterQuality.aggregate_status,
  aster_marker_status: asterMarkerStatus,
  next_active_phase: closeout.next_active_phase,
  full_goal_complete: false,
  raw_private_material_published: false,
  artifact: refs.json,
}, null, 2) + "\n");

function laneStatus(gate, name) {
  const row = Array.isArray(gate.lanes) ? gate.lanes.find((lane) => lane.lane === name) : null;
  if (!row) return "missing";
  return row.overall_status || row.completion_status || "unknown";
}

function writePair(suffix, doc) {
  fs.mkdirSync(tracesDir, { recursive: true });
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, doc);
  fs.writeFileSync(`${base}.md`, renderMd(doc), "utf8");
  return {
    json: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    md: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  };
}

function refreshBeacons(ref, doc) {
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.status = doc.overall_status;
    data.current_active_phase = doc.next_active_phase;
    data.latest_closed_phase = doc.latest_closed_phase;
    data.latest_completed_x1_phase = closeoutPassed ? phaseSlug : data.latest_completed_x1_phase;
    data.next_expected_scope = doc.next_active_phase;
    data.next_x2_scope = doc.next_x2_scope;
    data.next_x1_lane_after_x2 = doc.next_x1_lane_after_x2;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.latest_active_open_handoff = null;
    data.v557_v4_x1_closeout = {
      status: doc.overall_status,
      aster_completion_status: doc.lane_evidence.aster_vale.completion_status,
      aster_quality_status: doc.lane_evidence.aster_vale.quality_status,
      aster_marker_status: doc.lane_evidence.aster_vale.marker_status,
      app_completion_gate_status: appGate.overall_status,
      app_lanes_completed: appLanesCompleted,
      full_goal_complete: false,
    };
    data[listKey] = unique([...(data[listKey] || []), ref.json, ref.md]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function renderMd(doc) {
  return [
    `# ${doc.phase_slug} Triad Closeout`,
    "",
    `Status: \`${doc.overall_status}\``,
    `Next active phase: \`${doc.next_active_phase}\``,
    "",
    "## Lane Evidence",
    "",
    `- Aster Vale completion: \`${doc.lane_evidence.aster_vale.completion_status}\``,
    `- Aster Vale quality: \`${doc.lane_evidence.aster_vale.quality_status}\``,
    `- Aster Vale marker review: \`${doc.lane_evidence.aster_vale.marker_status}\``,
    `- Kierkegaard completion gate: \`${doc.lane_evidence.kierkegaard.lane_status}\``,
    `- Aristotle completion gate: \`${doc.lane_evidence.aristotle.lane_status}\``,
    "",
    "## X2 Carry Forward",
    "",
    `- status: \`${doc.x2_carry_forward.status}\``,
    `- prototypes ready: \`${doc.x2_carry_forward.prototypes_ready}\``,
    "- raw proposal bodies remain unpublished.",
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
    `Next expected scope: ${doc.next_expected_scope}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## v557 v4 x1 Closeout",
    "",
    `Status: \`${doc.v557_v4_x1_closeout?.status || "not_recorded"}\``,
    `Aster quality: \`${doc.v557_v4_x1_closeout?.aster_quality_status || "not_recorded"}\``,
    `App completion gate: \`${doc.v557_v4_x1_closeout?.app_completion_gate_status || "not_recorded"}\``,
    `Full goal complete: \`${doc.v557_v4_x1_closeout?.full_goal_complete === true ? "true" : "false"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-240).map((entry) => `- ${entry}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
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

function claimBoundary() {
  return {
    phase_completion_scope: "v557_v4_x1_lane_evidence_only",
    full_goal_complete: false,
    v557_v4_x2_started: false,
    gmut_empirical_closure: "open",
    final_physics: "open",
    consciousness_proof: "open",
    legal_closure: "open",
    canon_promotion: "open",
    deployment: "open",
    purchase: "open",
    account_mutation: "open",
    api_key_creation: "open",
    private_material_proof: "open",
    raw_publication_proof: "open",
    sibling_identity_merge_or_replacement: "open",
  };
}

function boundarySentence() {
  return "No private message body content, private Browser routes, private URLs, screenshots, private callable IDs, credentials, runtime streams, local private paths, destructive cleanup, paid resources, deployments, account mutations, API keys, or sibling identity changes were published or performed.";
}

function parseArgs(argv) {
  const out = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      out.set(key, "true");
    } else {
      out.set(key, value);
      index += 1;
    }
  }
  return out;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "medium",
    timeStyle: "medium",
    hourCycle: "h23",
  }).format(date);
}
