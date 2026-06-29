#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = required("--phase-slug");
const nextPhase = required("--next-phase");
const latestCompletedX2 = required("--latest-completed-x2");
const nextX1AfterX2 = required("--next-x1-after-x2");
const launchSkill = args.get("--launch-skill") || "not_recorded";
const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
const omegaDir = join(process.cwd(), "docs", "omega-mini-index");
mkdirSync(tracesDir, { recursive: true });
mkdirSync(omegaDir, { recursive: true });

const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);

const requiredFiles = [
  `${phaseSlug}-main-startup-context-v1.json`,
  `${phaseSlug}-five-minute-productive-cadence-v1.json`,
  `${phaseSlug}-duo-harvest-reduction-v1.json`,
  `${phaseSlug}-duo-sanitized-proposal-queue-v1.json`,
  `${phaseSlug}-closeout-prep-v1.json`,
];
const missing = requiredFiles.filter((file) => !existsSync(join(tracesDir, file)));
if (missing.length) {
  console.error(JSON.stringify({ status: "OPEN_GAP_DUO_X1_CLOSEOUT_REQUIRED_ARTIFACTS_MISSING", phase_slug: phaseSlug, missing, closeout_claimed: false }, null, 2));
  process.exit(2);
}

const reduction = readJson(join(tracesDir, `${phaseSlug}-duo-harvest-reduction-v1.json`));
const queue = readJson(join(tracesDir, `${phaseSlug}-duo-sanitized-proposal-queue-v1.json`));
const prep = readJson(join(tracesDir, `${phaseSlug}-closeout-prep-v1.json`));
const counts = queue.profile_cap_counts_represented || reduction.profile_cap_counts_represented || {};
const rows = Array.isArray(queue.rows) ? queue.rows : [];
const closeoutAllowed = reduction.status.startsWith("PASS") && prep.status.startsWith("PASS") && rows.length > 0;
const closeoutStatus = closeoutAllowed ? "PASS_DUO_X1_CLOSED_NEXT_X2_READY" : "OPEN_GAP_DUO_X1_CLOSEOUT_GATES_INCOMPLETE";
const immediateRows = rows.filter((row) => row.execution_lane === "immediate_x1_safe").length;
const x2Rows = rows.filter((row) => row.execution_lane === "x2_build_task").length;

const artifacts = [
  artifact("duo-closeout", "ghc.duo_x1_closeout.v2", closeoutStatus, {
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: phaseSlug,
    latest_completed_x2_phase: latestCompletedX2,
    next_active_phase: closeoutAllowed ? nextPhase : phaseSlug,
    next_x2_scope: nextPhase,
    next_x1_lane_after_x2: nextX1AfterX2,
    launch_skill: launchSkill,
    active_duo: reduction.active_duo || [],
    profile_counts_represented: counts,
    queue_rows: rows.length,
    immediate_x1_safe_rows_represented: immediateRows,
    x2_build_rows_represented: x2Rows,
    full_goal_complete: false,
    open_gates: openGates(),
  }),
  artifact("x2-safe-build-handoff", "ghc.x2_handoff.v2", closeoutAllowed
    ? "PASS_DUO_X2_SAFE_BUILD_HANDOFF_READY"
    : "OPEN_GAP_DUO_X2_HANDOFF_NOT_READY", {
    source_x1_phase: phaseSlug,
    next_active_phase: closeoutAllowed ? nextPhase : phaseSlug,
    next_x2_scope: nextPhase,
    next_x1_lane_after_x2: nextX1AfterX2,
    source_queue_basename: `${phaseSlug}-duo-sanitized-proposal-queue-v1.json`,
    profile_counts_represented: counts,
    queue_rows: rows.length,
    immediate_x1_safe_rows_represented: immediateRows,
    x2_build_rows_represented: x2Rows,
    exact_and_blocked_boundary: "exact approval and blocked gates remain queued/open unless freshly authorized",
  }),
];

for (const doc of artifacts) writePair(doc);
if (closeoutAllowed) refreshBeacons(artifacts);

console.log(JSON.stringify({
  status: closeoutStatus,
  phase_slug: phaseSlug,
  next_active_phase: closeoutAllowed ? nextPhase : phaseSlug,
  latest_completed_x1_phase: closeoutAllowed ? phaseSlug : null,
  safe_packets_represented: counts.safe_approval_packets || 0,
  candidate_packets_represented: counts.candidate_packets || 0,
  exact_packets_queued: counts.exact_approval_packets_queued || 0,
  skill_ideas_represented: counts.skill_ideas || 0,
  runner_ideas_represented: counts.runner_ideas || 0,
  cleanup_tasks_represented: counts.cleanup_refine_fix_tasks || 0,
  queue_rows: rows.length,
  immediate_x1_safe_rows: immediateRows,
  x2_build_task_rows: x2Rows,
  artifacts_written: artifacts.length * 2 + (closeoutAllowed ? 6 : 0),
}, null, 2));

process.exit(closeoutAllowed ? 0 : 1);

function parseArgs(argv) {
  const out = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) out.set(key, "true");
    else {
      out.set(key, value);
      index += 1;
    }
  }
  return out;
}

function required(flag) {
  const value = args.get(flag);
  if (!value) {
    console.error(`Usage: node scripts/ghc_duo_x1_closeout_builder.mjs ${flag} <value>`);
    process.exit(2);
  }
  return value;
}

function artifact(suffix, schema, status, body = {}) {
  return {
    artifact: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1`,
    schema,
    phase_slug: phaseSlug,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    status,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...body,
  };
}

function writePair(doc) {
  const base = join(process.cwd(), doc.artifact);
  mkdirSync(dirname(base), { recursive: true });
  writeFileSync(`${base}.json`, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  writeFileSync(`${base}.md`, `# ${phaseSlug} ${doc.artifact.split(`${phaseSlug}-`).pop().replace(/-v1$/, "")}

Status: ${doc.status}

Generated NZ: ${doc.generated_nz}

Boundary: sanitized artifact only. Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local private paths, session streams, private app state, private dumps, and hidden reasoning are not published.
`, "utf8");
}

function refreshBeacons(artifactDocs) {
  const lookup = artifactDocs.flatMap((doc) => [`${doc.artifact}.json`, `${doc.artifact}.md`]);
  const statePath = join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const beaconPath = join(tracesDir, "ghc-current-state-beacon-v1.json");
  const state = readJson(statePath);
  const latest = readJson(latestPath);
  const beacon = existsSync(beaconPath) ? readJson(beaconPath) : {};
  for (const [doc, lookupKey] of [[state, "current_lookup_files"], [latest, "latest_lookup_files"], [beacon, "lookup_files"]]) {
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = closeoutStatus;
    doc.current_active_phase = nextPhase;
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = phaseSlug;
    doc.latest_completed_x2_phase = latestCompletedX2;
    doc.next_expected_scope = nextPhase;
    doc.next_x2_scope = nextPhase;
    doc.next_x1_lane_after_x2 = nextX1AfterX2;
    doc.duo_x1_closeout = {
      status: closeoutStatus,
      launch_skill: launchSkill,
      profile_counts_represented: counts,
      queue_rows: rows.length,
      next_active_phase: nextPhase,
      full_goal_complete: false,
    };
    doc.full_goal_complete = false;
    doc[lookupKey] = unique([...(doc[lookupKey] || []), ...lookup]);
  }
  writeJson(statePath, state);
  writeJson(latestPath, latest);
  writeJson(beaconPath, beacon);
  writeFileSync(join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(state), "utf8");
  writeFileSync(join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderBeaconMd("Omega-Mini Latest Updates Beacon", latest, latest.latest_lookup_files), "utf8");
  writeFileSync(join(tracesDir, "ghc-current-state-beacon-v1.md"), renderBeaconMd("GHC Current State Beacon", beacon, beacon.lookup_files), "utf8");
}

function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function renderCurrentStateMd(current) {
  return `# Omega-Mini Current State

Status: ${current.status}
Current active phase: ${current.current_active_phase}
Latest closed phase: ${current.latest_closed_phase}
Latest completed x1: ${current.latest_completed_x1_phase}
Latest completed x2: ${current.latest_completed_x2_phase}
Next expected scope: ${current.next_expected_scope}
Next x2 scope: ${current.next_x2_scope}
Next x1 lane after x2: ${current.next_x1_lane_after_x2}

## Duo X1 Closeout

- Status: \`${current.duo_x1_closeout?.status || "not_recorded"}\`
- Launch skill: \`${current.duo_x1_closeout?.launch_skill || "not_recorded"}\`
- Queue rows: \`${current.duo_x1_closeout?.queue_rows || "not_recorded"}\`

## Safety Boundary

Sanitized state only. Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local private paths, session streams, private app state, private dumps, and hidden reasoning are not published.
`;
}

function renderBeaconMd(title, data, lookupFiles = []) {
  return `# ${title}

Status: ${data.status}
Current active phase: ${data.current_active_phase}
Latest closed phase: ${data.latest_closed_phase}
Latest completed x1: ${data.latest_completed_x1_phase}
Latest completed x2: ${data.latest_completed_x2_phase}
Next x1 lane after x2: ${data.next_x1_lane_after_x2}

## Lookup Files

${(lookupFiles || []).map((item) => `- ${item}`).join("\n")}

## Safety Boundary

Sanitized beacon only. Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local private paths, session streams, private app state, private dumps, and hidden reasoning are not published.
`;
}

function unique(items) {
  return [...new Set(items.filter(Boolean))];
}

function publicationBoundary() {
  return {
    raw_private_material_published: false,
    raw_browser_routes_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
  };
}

function claimBoundary() {
  return {
    full_goal_completion: "not_claimed",
    sibling_identity_replacement_or_merge: "not_claimed",
    proof_canon_legal_deployment_account_api_key_raw_publication_closure: "not_claimed",
  };
}

function openGates() {
  return [
    "GMUT empirical closure",
    "final physics",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment closure",
    "account mutation",
    "API-key creation",
    "purchase",
    "private-material proof/publication",
    "raw-publication proof",
    "sibling merge/replacement/erasure",
  ];
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
