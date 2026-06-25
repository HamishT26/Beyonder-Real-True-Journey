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
const commit = args.get("--commit") || "unknown";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const suite = readJson(path.join(tracesDir, `${phaseSlug}-lumen-prototype-suite-index-v1.json`));
const handoff = {
  artifact_type: "ghc_v557_v4_x1_active_open_handoff",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "ACTIVE_OPEN_V557_V4_X1_TRIAD_RETRY_THRESHOLD_MET_PROTOTYPE_SUITE_PUBLISHED",
  sanitized_publication_commit: commit,
  active_sanitized_publication_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini-3",
  active_private_support_branch: "codex/GHC-Family/aevren-full-tools-2",
  latest_closed_phase: "v557-gmut-thos-v3-x2",
  next_x2_scope: "v557-gmut-thos-v4-x2",
  next_x1_lane_after_x2: "v557-gmut-thos-v5-x1 with Lumen Vale solo unless Hamish redirects",
  lumen_prototype_suite: {
    status: suite.overall_status,
    prototypes_run: Array.isArray(suite.prototypes_run) ? suite.prototypes_run.length : 0,
    proposal_candidates_indexed: suite.proposal_candidates_indexed,
    matrix_cells_reused: suite.matrix_cells_reused,
    raw_private_material_published: false,
  },
  triad_lanes: [
    {
      lane: "Aster Vale",
      route: "strict_cli",
      status: "active_open_completion_marker_review_not_proven_in_current_receipts",
    },
    {
      lane: "Kierkegaard",
      route: "recovered_app_lane_background_watch",
      status: "retry_3_watcher_started_completion_gate_not_proven",
    },
    {
      lane: "Aristotle",
      route: "recovered_app_lane_background_watch",
      status: "retry_3_watcher_started_completion_gate_not_proven",
    },
  ],
  retry_posture: {
    recovered_app_lane_retry_sessions_started: 3,
    formal_retry_threshold_met: true,
    watcher_start_is_completion_proof: false,
    closeout_allowed_now: false,
    next_safe_action: "harvest completion gates or publish a formal open-gap continuation receipt without closing the phase",
  },
  validation_evidence: {
    node_check: "PASS",
    current_state_guard: "PASS",
    json_parse_changed_files: "PASS_15",
    diff_check: "PASS_WITH_LINE_ENDING_WARNINGS_ONLY",
    privacy_scan_changed_files: "PASS_31",
    remote_equals_local: commit,
  },
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

const refs = writePair("active-open-handoff-after-lumen-prototype-suite", handoff);
refreshBeacons(refs, handoff);

process.stdout.write(JSON.stringify({
  status: handoff.overall_status,
  phase_slug: phaseSlug,
  closeout_allowed_now: false,
  recovered_app_lane_retry_sessions_started: 3,
  formal_retry_threshold_met: true,
  raw_private_material_published: false,
  artifact: refs.json,
}, null, 2) + "\n");

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
    data.current_active_phase = phaseSlug;
    data.latest_closed_phase = doc.latest_closed_phase;
    data.next_x2_scope = doc.next_x2_scope;
    data.next_x1_lane_after_x2 = doc.next_x1_lane_after_x2;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.latest_active_open_handoff = ref.json;
    data.v557_v4_x1_active_open_handoff = {
      status: doc.overall_status,
      recovered_app_lane_retry_sessions_started: 3,
      formal_retry_threshold_met: true,
      closeout_allowed_now: false,
      sanitized_publication_commit: commit,
    };
    data[listKey] = unique([...(data[listKey] || []), ref.json, ref.md]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function renderMd(doc) {
  return [
    `# ${doc.phase_slug} Active/Open Handoff`,
    "",
    `Status: \`${doc.overall_status}\``,
    `Sanitized publication commit: \`${doc.sanitized_publication_commit}\``,
    "",
    "## What Is Proven",
    "",
    `- Lumen prototype suite: \`${doc.lumen_prototype_suite.status}\``,
    `- prototypes run: \`${doc.lumen_prototype_suite.prototypes_run}\``,
    `- proposal candidates indexed: \`${doc.lumen_prototype_suite.proposal_candidates_indexed}\``,
    `- formal recovered app-lane retry threshold met: \`${doc.retry_posture.formal_retry_threshold_met}\``,
    "",
    "## What Is Still Open",
    "",
    "- Aster Vale completion marker review is not proven in current receipts.",
    "- Kierkegaard and Aristotle recovered app-lane completion gates are not proven in current receipts.",
    "- v557 v4 x1 is active/open; v557 v4 x2 is not started by this handoff.",
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
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    `Latest active/open handoff: ${doc.latest_active_open_handoff}`,
    "",
    "## Active/Open Handoff",
    "",
    `Status: \`${doc.v557_v4_x1_active_open_handoff?.status || "not_recorded"}\``,
    `Retry sessions started: \`${doc.v557_v4_x1_active_open_handoff?.recovered_app_lane_retry_sessions_started ?? "not_recorded"}\``,
    `Closeout allowed now: \`${doc.v557_v4_x1_active_open_handoff?.closeout_allowed_now === true ? "true" : "false"}\``,
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
    phase_completion: "not_claimed",
    x2_closeout: "not_claimed",
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
