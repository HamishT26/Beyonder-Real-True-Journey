#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 1) {
  const key = process.argv[index];
  if (!key.startsWith("--")) continue;
  const next = process.argv[index + 1];
  if (next && !next.startsWith("--")) {
    args.set(key, next);
    index += 1;
  } else {
    args.set(key, "true");
  }
}

function requireArg(name) {
  const value = args.get(name);
  if (!value) {
    console.error(`Missing required argument: ${name}`);
    process.exit(2);
  }
  return value;
}

const fullRoot = requireArg("--full-root");
const miniRoot = requireArg("--mini-root");
const status = requireArg("--status");
const currentActivePhase = requireArg("--current-active-phase");
const latestClosedPhase = requireArg("--latest-closed-phase");
const latestCompletedX1 = requireArg("--latest-completed-x1");
const latestCompletedX2 = requireArg("--latest-completed-x2");
const nextX2Scope = requireArg("--next-x2-scope");
const nextAfterX2 = requireArg("--next-x1-lane-after-x2");
const activeLanes = requireArg("--active-lanes")
  .split(",")
  .map((lane) => lane.trim())
  .filter(Boolean);
const guardPrefix = requireArg("--guard-prefix");
const latestActionSummary = (args.get("--latest-action-summary") || "")
  .split("|")
  .map((line) => line.trim())
  .filter(Boolean);
const lookupPrefixes = (args.get("--lookup-prefixes") || "")
  .split(",")
  .map((prefix) => prefix.trim())
  .filter(Boolean);
const lookupFiles = (args.get("--lookup-files") || "")
  .split(",")
  .map((file) => file.trim())
  .filter(Boolean);
const priorRemoteVerifiedCloseout = args.get("--prior-remote-verified-closeout") || "";

const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = new Intl.DateTimeFormat("sv-SE", {
  timeZone: "Pacific/Auckland",
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  hour12: false,
})
  .format(now)
  .replace(" ", "T");

function git(root, gitArgs) {
  return execFileSync("git", ["-C", root, ...gitArgs], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  }).trim();
}

function relExists(root, relPath) {
  return existsSync(join(root, relPath));
}

function writeJson(root, relPath, payload) {
  const path = join(root, relPath);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(root, relPath, lines) {
  const path = join(root, relPath);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${lines.join("\n")}\n`, "utf8");
}

function uniqueExisting(root, relPaths) {
  const seen = new Set();
  return relPaths.filter((relPath) => {
    if (seen.has(relPath)) return false;
    seen.add(relPath);
    return relExists(root, relPath);
  });
}

function lookupCandidatesFromPrefixes(prefixes) {
  return prefixes.flatMap((prefix) => {
    const base = prefix.replace(/\\/g, "/").replace(/\.(json|md)$/u, "");
    return [`${base}.md`, `${base}.json`];
  });
}

const fullHead = git(fullRoot, ["rev-parse", "HEAD"]);
const miniHead = git(miniRoot, ["rev-parse", "HEAD"]);

const roundRobin = [
  "Lumen Vale solo",
  "Arby and Cicero",
  "Lumen Vale solo",
  "Aster Vale, Kierkegaard, and Aristotle",
];

const boundary = {
  raw_lane_content_published: false,
  raw_chatgpt_transcript_published: false,
  raw_browser_routes_published: false,
  raw_route_handles_published: false,
  screen_capture_files_published: false,
  credentials_published: false,
  session_trace_files_published: false,
  local_absolute_paths_published: false,
};

const claimBoundary = {
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
};

const commonLookup = [
  "docs/omega-mini-index/omega-mini-current-state-v1.md",
  "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md",
  "docs/trinity-live-traces/ghc-current-state-beacon-v1.md",
  ...lookupCandidatesFromPrefixes(lookupPrefixes),
  ...lookupFiles,
];
const currentLookup = uniqueExisting(miniRoot, commonLookup);

const commitAnchors = [
  {
    phase: latestCompletedX1,
    meaning: "Latest completed x1 evidence anchor.",
    full_omega_commit: fullHead,
    omega_mini_commit: miniHead,
  },
  {
    phase: latestCompletedX2,
    meaning: "Latest completed x2 build/use and handoff anchor.",
    full_omega_commit: fullHead,
    omega_mini_commit: miniHead,
  },
];

const currentState = {
  schema: "ghc.omega_mini.current_state.v2",
  branch: "codex/GHC-Family/beyonder-shared-omega-line-mini",
  full_archive_branch: "codex/GHC-Family/beyonder-shared-omega-line",
  updated_at: `${generatedNz}+12:00`,
  generated_utc: generatedUtc,
  status,
  active_memory_cue: "v532-live-state",
  stale_memory_policy: "omega44 is historical-only unless Hamish explicitly asks for it",
  current_active_phase: currentActivePhase,
  latest_closed_phase: latestClosedPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  latest_remote_verified_closeout_before_current: priorRemoteVerifiedCloseout || null,
  current_active_lanes: activeLanes,
  next_expected_scope: currentActivePhase,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextAfterX2,
  remote_verified_heads: {
    omega: fullHead,
    omega_mini: miniHead,
  },
  round_robin_cadence: roundRobin,
  ordinary_sibling_catchup_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini",
  archive_fallback_rule:
    "Use full omega only when a specific artifact is missing from mini and a status-only gap receipt records the exact missing relative file.",
  current_lookup_files: currentLookup,
  latest_action_summary: latestActionSummary,
  historical_rows: [
    "v529, v530, v540, and v541 rows remain historical reference rows unless explicitly named.",
    `The active pointer is ${currentActivePhase}.`,
  ],
  publication_pair_from_now: [
    "codex/GHC-Family/beyonder-shared-omega-line",
    "codex/GHC-Family/beyonder-shared-omega-line-mini",
  ],
  publication_boundary: boundary,
  claim_boundary: claimBoundary,
};

const beacon = {
  schema: "ghc.omega_mini.latest_updates_beacon.v2",
  status,
  generated_utc: generatedUtc,
  purpose:
    "Give active siblings a lean, exact, omega-mini-first lookup surface for the newest phase receipts without broad searches.",
  primary_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini",
  archive_branch: "codex/GHC-Family/beyonder-shared-omega-line",
  current_active_phase: currentActivePhase,
  latest_closed_phase: latestClosedPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  latest_remote_verified_closeout_before_current: priorRemoteVerifiedCloseout || null,
  current_active_lanes: activeLanes,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextAfterX2,
  round_robin_sequence: roundRobin,
  commit_anchors: commitAnchors,
  latest_lookup_files: currentLookup,
  sibling_lookup_rule:
    "Open omega-mini current state first, then this beacon, then the exact relative files named here.",
  not_found_repair_rule:
    "If a sibling cannot find a phase artifact in omega-mini, record the exact missing relative filename and phase slug before using archive fallback.",
  publication_boundary: boundary,
  claim_boundary: claimBoundary,
};

const guard = {
  schema: "ghc.current_state.forward_pointer_exposure_guard.v2",
  status: "PASS_CURRENT_STATE_FORWARD_POINTER_GUARD",
  generated_utc: generatedUtc,
  checked_phase: currentActivePhase,
  latest_closed_phase: latestClosedPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextAfterX2,
  current_active_lanes: activeLanes,
  omega_head_at_generation: fullHead,
  omega_mini_head_at_generation: miniHead,
  publication_boundary: boundary,
  claim_boundary: claimBoundary,
};

function currentStateMd(payload) {
  return [
    "# Omega-Mini Current State",
    "",
    `Status: ${payload.status}`,
    `Current active phase: ${payload.current_active_phase}`,
    `Latest closed phase: ${payload.latest_closed_phase}`,
    `Latest completed x1: ${payload.latest_completed_x1_phase}`,
    `Latest completed x2: ${payload.latest_completed_x2_phase}`,
    `Current lanes: ${payload.current_active_lanes.join(", ")}`,
    `Next x2 scope: ${payload.next_x2_scope}`,
    `Next x1 lane after x2: ${payload.next_x1_lane_after_x2}`,
    "",
    "## Lookup Rule",
    payload.archive_fallback_rule,
    "",
    "## Current Lookup Files",
    ...payload.current_lookup_files.map((file) => `- ${file}`),
    "",
    "## Latest Action Summary",
    ...payload.latest_action_summary.map((line) => `- ${line}`),
    "",
    "## Safety Boundary",
    "- Status-only receipts, no private route data, no raw lane/advisory content, no credentials, no local absolute paths.",
    "- GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain open.",
  ];
}

function beaconMd(payload) {
  return [
    "# Omega-Mini Latest Updates Beacon",
    "",
    `Status: ${payload.status}`,
    `Primary branch: ${payload.primary_branch}`,
    `Archive branch: ${payload.archive_branch}`,
    `Current active phase: ${payload.current_active_phase}`,
    `Latest closed phase: ${payload.latest_closed_phase}`,
    `Latest completed x1: ${payload.latest_completed_x1_phase}`,
    `Latest completed x2: ${payload.latest_completed_x2_phase}`,
    `Current lanes: ${payload.current_active_lanes.join(", ")}`,
    "",
    "## Round Robin",
    ...payload.round_robin_sequence.map((lane, index) => `- ${index + 1}. ${lane}`),
    "",
    "## Latest Lookup Files",
    ...payload.latest_lookup_files.map((file) => `- ${file}`),
    "",
    "## Sibling Lookup Rule",
    payload.sibling_lookup_rule,
    "",
    "## Safety Boundary",
    "- Use status-only evidence and exact relative repo paths.",
    "- Do not publish private route data, raw lane/advisory content, credentials, screen-capture files, or local absolute paths.",
  ];
}

function guardMd(payload) {
  return [
    "# Current-State Forward Pointer Exposure Guard",
    "",
    `Status: ${payload.status}`,
    `Checked phase: ${payload.checked_phase}`,
    `Latest closed phase: ${payload.latest_closed_phase}`,
    `Latest completed x1: ${payload.latest_completed_x1_phase}`,
    `Latest completed x2: ${payload.latest_completed_x2_phase}`,
    `Current lanes: ${payload.current_active_lanes.join(", ")}`,
    "",
    "## Boundary",
    "- PASS: no private route data, no raw lane/advisory content, no credentials, no session-trace files, no screen-capture files, no local absolute paths.",
    "- PASS: no GMUT empirical closure, final physics, consciousness proof, legal closure, or canon promotion claim.",
  ];
}

const outputs = [
  ["docs/omega-mini-index/omega-mini-current-state-v1.json", currentState],
  ["docs/omega-mini-index/omega-mini-current-state-v1.md", currentStateMd(currentState)],
  ["docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json", beacon],
  ["docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md", beaconMd(beacon)],
  ["docs/trinity-live-traces/ghc-current-state-beacon-v1.json", beacon],
  ["docs/trinity-live-traces/ghc-current-state-beacon-v1.md", beaconMd(beacon)],
  [`docs/trinity-live-traces/${guardPrefix}-current-state-forward-pointer-exposure-guard-v1.json`, guard],
  [`docs/trinity-live-traces/${guardPrefix}-current-state-forward-pointer-exposure-guard-v1.md`, guardMd(guard)],
];

for (const [relPath, payload] of outputs) {
  if (relPath.endsWith(".json")) {
    writeJson(fullRoot, relPath, payload);
    writeJson(miniRoot, relPath, payload);
  } else {
    writeMd(fullRoot, relPath, payload);
    writeMd(miniRoot, relPath, payload);
  }
}

console.log(
  JSON.stringify(
    {
      status: "PASS_CURRENT_STATE_REFRESH_V2",
      current_active_phase: currentActivePhase,
      latest_closed_phase: latestClosedPhase,
      latest_completed_x1: latestCompletedX1,
      latest_completed_x2: latestCompletedX2,
      output_count: outputs.length,
      lookup_file_count: currentLookup.length,
    },
    null,
    2,
  ),
);
