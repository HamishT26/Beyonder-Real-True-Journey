#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const fullRoot = args.get("--full-root");
const miniRoot = args.get("--mini-root");
if (!fullRoot || !miniRoot) {
  console.error("Usage: node scripts/ghc_v541_v7_x2_current_state_refresher.mjs --full-root <path> --mini-root <path>");
  process.exit(2);
}

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

function readJson(root, relPath) {
  return JSON.parse(readFileSync(join(root, relPath), "utf8"));
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

const fullHead = git(fullRoot, ["rev-parse", "HEAD"]);
const miniHead = git(miniRoot, ["rev-parse", "HEAD"]);

const status = "READY_FOR_V542_V1_X1_LUMEN";
const currentActivePhase = "v542-gmut-thos-v78-v1-x1";
const latestClosedPhase = "v541-gmut-thos-v77-v8-x2";
const latestCompletedX1 = "v541-gmut-thos-v77-v8-x1";
const latestCompletedX2 = "v541-gmut-thos-v77-v8-x2";
const nextX2Scope = "v542-gmut-thos-v78-v1-x2";
const nextAfterX2 = "Arby and Cicero";
const activeLanes = ["Lumen Vale"];
const roundRobin = [
  "Lumen Vale solo",
  "Arby and Cicero",
  "Lumen Vale solo",
  "Aster Vale, Kierkegaard, and Aristotle",
];

const boundary = {
  raw_lane_text_published: false,
  raw_chatgpt_transcript_published: false,
  raw_browser_routes_published: false,
  raw_route_handles_published: false,
  image_files_published: false,
  credentials_published: false,
  session_streams_published: false,
  local_absolute_paths_published: false,
};

const claimBoundary = {
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
};

const lookupCandidates = [
  "docs/omega-mini-index/omega-mini-current-state-v1.md",
  "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md",
  "docs/trinity-live-traces/ghc-current-state-beacon-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-lumen-browser-send-receipt-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-lumen-browser-send-exposure-guard-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-source-ledger-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-approval-continuity-pack-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-eureka-continuity-ledger-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-to-v7-x2-continuity-handoff-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-lumen-browser-five-minute-check-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-lumen-marker-receipt-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-lumen-response-hash-receipt-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-lumen-normalized-action-ledger-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-closeout-exposure-guard-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-grouped-lane-receipt-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-grouped-lane-guard-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x1-x2-grouped-handoff-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x2-lane-state-reducer-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x2-route-family-manifest-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x2-full-phase-guard-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x2-closeout-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x2-lumen-v7-x2-action-execution-ledger-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x2-lumen-action-completion-reconciliation-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v7-x2-final-exposure-guard-v1.md",
  "docs/omega-mini-index/v541-v7-lumen-omega-mini-catchup-brief-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-next-group-prep-card-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-source-ledger-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-approval-continuity-pack-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-eureka-continuity-ledger-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-to-v8-x2-continuity-handoff-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-arby-five-minute-check-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-strict-cli-lane-cycle-quality-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-strict-cli-lane-cycle-marker-review-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-cicero-recovered-notifier-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-cicero-app-redaction-guard-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-cicero-recovered-completion-gate-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-grouped-lane-receipt-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-grouped-lane-guard-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x1-x2-grouped-handoff-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x2-lane-state-reducer-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x2-route-family-manifest-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x2-full-phase-guard-v1.md",
  "docs/trinity-live-traces/v541-gmut-thos-v77-v8-x2-closeout-v1.md",
  "docs/trinity-live-traces/v542-gmut-thos-v78-v1-x1-next-group-prep-card-v1.md",
];

const currentLookup = uniqueExisting(miniRoot, lookupCandidates);

const commitAnchors = [
  {
    phase: "v541-gmut-thos-v77-v6-x2",
    meaning: "Prior Arby/Cicero completion and Lumen v7 prep anchor.",
    omega_mini_commit: "d2f5f0f31d865190d809e3b354ae2ffe0f47ac4e",
    full_omega_commit: "ae65c623a3366dd29ba545179d2d7ac94631bdd1",
  },
  {
    phase: "v541-gmut-thos-v77-v7-x1-lumen-send",
    meaning: "Lumen v7 x1 Browser prompt transmission and exposure guard.",
    omega_mini_commit: "5a1833c12d456a923f6d0f87dcebd1fadbdd8314",
    full_omega_commit: "762a6be5c2b65e0864cc4ae13e4a70b4ac487586",
  },
  {
    phase: "v541-gmut-thos-v77-v7-x1-wait-pack",
    meaning: "Source ledger, approval continuity, eureka continuity, and five-minute check while Lumen reasoned.",
    omega_mini_commit: "a05ed4d6079656dcb1ff5b0da0132b6e6a43a355",
    full_omega_commit: "26ab6ee6c26d1c21cdd3e6ff193f852224e9d505",
  },
  {
    phase: "v541-gmut-thos-v77-v7-x1-closeout",
    meaning: "Lumen v7 x1 completion, response hash receipt, and normalized action ledger.",
    omega_mini_commit: "da41e1eeedc00fc23b48d0916724a9695133868d",
    full_omega_commit: "35a96df7fc6afb05e6cead09b39eaf2670abdcc4",
  },
  {
    phase: latestCompletedX2,
    meaning: "Arby/Cicero v8 x1 status closeout, v8 x2 build/use closeout, and Lumen v542 v1 x1 prep.",
    omega_mini_commit: miniHead,
    full_omega_commit: fullHead,
  },
];

function currentStatePayload() {
  return {
    schema: "ghc.omega_mini.current_state.v1",
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
    latest_remote_verified_closeout_before_v540: "v539-gmut-thos-v75-v8-x2",
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
    latest_action_summary: [
      "Arby v8 x1 passed strict CLI quality and marker review with status-only evidence.",
      "Cicero v8 x1 completed through the recovered app lane and passed the direct completion gate.",
      "v8 x2 build/use closeout passed and prepared the next Lumen solo start.",
      "Next grouped x1 is Lumen Vale solo through the Browser live-adapter route.",
    ],
    historical_rows: [
      "v529, v530, and earlier v540/v541 rows remain historical reference rows only.",
      `The active pointer is ${currentActivePhase}, not v530 or v541 v8 x1.`,
    ],
    publication_pair_from_now: [
      "codex/GHC-Family/beyonder-shared-omega-line",
      "codex/GHC-Family/beyonder-shared-omega-line-mini",
    ],
    publication_boundary: boundary,
    claim_boundary: claimBoundary,
  };
}

function beaconPayload() {
  return {
    schema: "ghc.omega_mini.latest_updates_beacon.v1",
    status,
    generated_utc: generatedUtc,
    purpose:
      "Give every active sibling a lean, exact, omega-mini-first lookup surface for the latest v541 phase receipts without broad searches.",
    primary_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini",
    archive_branch: "codex/GHC-Family/beyonder-shared-omega-line",
    current_active_phase: currentActivePhase,
    latest_closed_phase: latestClosedPhase,
    latest_completed_x1_phase: latestCompletedX1,
    latest_completed_x2_phase: latestCompletedX2,
    latest_remote_verified_closeout_before_v540: "v539-gmut-thos-v75-v8-x2",
    current_active_lanes: activeLanes,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextAfterX2,
    round_robin_sequence: roundRobin,
    commit_anchors: commitAnchors,
    latest_lookup_files: currentLookup,
    sibling_lookup_rule:
      "Open omega-mini current state first, then this beacon, then the exact relative files named here. Do not run broad full-omega searches unless a named mini artifact is missing.",
    not_found_repair_rule:
      "If a sibling cannot find a phase artifact in omega-mini, record the exact missing relative filename and phase slug before using archive fallback.",
    publication_boundary: boundary,
    claim_boundary: claimBoundary,
  };
}

function ghcBeaconPayload() {
  return {
    schema: "ghc.current_state_beacon.v1",
    updated_at: `${generatedNz}+12:00`,
    generated_utc: generatedUtc,
    status: "ACTIVE_BEACON_READY_FOR_V542_V1_X1_LUMEN",
    active_memory_cue: "v532-live-state",
    stale_memory_policy: "omega44 is historical-only unless Hamish explicitly asks for it",
    primary_context_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini",
    archive_branch: "codex/GHC-Family/beyonder-shared-omega-line",
    remote_verified_heads: {
      omega: fullHead,
      omega_mini: miniHead,
    },
    latest_remote_verified_closeout: latestClosedPhase,
    latest_local_closeout_publication_anchor: latestClosedPhase,
    active_local_phase: currentActivePhase,
    next_prepared_phase: currentActivePhase,
    next_x2_scope: nextX2Scope,
    next_active_lanes: activeLanes,
    round_robin_pattern: roundRobin,
    current_v541_local_artifacts: currentLookup.filter((item) => item.includes("v541-gmut-thos-v77-v8")),
    next_phase_artifacts: currentLookup.filter((item) => item.includes("v542-gmut-thos-v78-v1")),
    browser_developer_mode_rule: {
      high_level_browser_actions_for_messaging: true,
      cdp_read_only_verification_and_profiling: true,
      direct_page_mutation_without_exact_future_approval: false,
    },
    storage_policy:
      "D-drive-first for workspaces, phase artifacts, and scratch outputs; C drive only for essential platform locations.",
    claim_boundary: claimBoundary,
    publication_boundary: boundary,
  };
}

function mdForCurrent(payload) {
  return [
    "# Omega Mini Current State",
    "",
    `Status: \`${payload.status}\``,
    "",
    `Generated UTC: \`${payload.generated_utc}\``,
    "",
    "## Active Routing",
    "",
    `- Active memory cue: \`${payload.active_memory_cue}\``,
    `- Stale memory policy: \`${payload.stale_memory_policy}\`.`,
    `- Primary branch: \`${payload.branch}\``,
    `- Archive branch: \`${payload.full_archive_branch}\``,
    `- Current active phase: \`${payload.current_active_phase}\``,
    `- Latest closed phase: \`${payload.latest_closed_phase}\``,
    `- Latest completed x1 phase: \`${payload.latest_completed_x1_phase}\``,
    `- Latest completed x2 phase: \`${payload.latest_completed_x2_phase}\``,
    `- Current active lanes: \`${payload.current_active_lanes.join(", ")}\``,
    `- Next expected scope: \`${payload.next_expected_scope}\``,
    `- Next x2 scope: \`${payload.next_x2_scope}\``,
    `- Next x1 lane after x2: \`${payload.next_x1_lane_after_x2}\``,
    "",
    "## Latest Remote-Verified Heads",
    "",
    `- Full omega: \`${payload.remote_verified_heads.omega}\``,
    `- Omega-mini: \`${payload.remote_verified_heads.omega_mini}\``,
    "",
    "## Round-Robin Cadence",
    "",
    ...payload.round_robin_cadence.map((item, index) => `${index + 1}. ${item}.`),
    `${payload.round_robin_cadence.length + 1}. Repeat.`,
    "",
    "## Latest Action Summary",
    "",
    ...payload.latest_action_summary.map((item) => `- ${item}`),
    "",
    "## Current Lookup Files",
    "",
    "Use these omega-mini files before broad searching:",
    ...payload.current_lookup_files.map((item) => `- \`${item}\``),
    "",
    "## Historical Rows",
    "",
    ...payload.historical_rows.map((item) => `- ${item}`),
    "",
    "## Sibling Catch-Up Rule",
    "",
    payload.archive_fallback_rule,
    "",
    "## Open Gates",
    "",
    "GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain open.",
  ];
}

function mdForBeacon(payload) {
  return [
    "# Omega-Mini Latest Updates Beacon v1",
    "",
    `Status: \`${payload.status}\``,
    "",
    `Generated UTC: \`${payload.generated_utc}\``,
    "",
    `Purpose: ${payload.purpose}`,
    "",
    `Primary branch: \`${payload.primary_branch}\``,
    "",
    `Archive branch: \`${payload.archive_branch}\``,
    "",
    "## Current State",
    "",
    `- Current active phase: \`${payload.current_active_phase}\``,
    `- Latest closed phase: \`${payload.latest_closed_phase}\``,
    `- Latest completed x1 phase: \`${payload.latest_completed_x1_phase}\``,
    `- Latest completed x2 phase: \`${payload.latest_completed_x2_phase}\``,
    `- Current active lane group: \`${payload.current_active_lanes.join(", ")}\``,
    `- Next x2 scope: \`${payload.next_x2_scope}\``,
    `- Next x1 lane after x2: \`${payload.next_x1_lane_after_x2}\``,
    "",
    "## Commit Anchors",
    "",
    ...payload.commit_anchors.map(
      (item) =>
        `- \`${item.phase}\`: ${item.meaning} (omega-mini: \`${item.omega_mini_commit}\`, full omega: \`${item.full_omega_commit}\`).`,
    ),
    "",
    "## Exact Lookup Files",
    "",
    "Open these in omega-mini before searching:",
    ...payload.latest_lookup_files.map((item) => `- \`${item}\``),
    "",
    "## Sibling Lookup Rule",
    "",
    payload.sibling_lookup_rule,
    "",
    "## Boundaries",
    "",
    "This beacon publishes status-only pointers and commit anchors. It does not publish private sibling replies, private browser transport details, image files, credentials, transcript streams, local absolute paths, or private transport material.",
    "",
    "GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain open.",
  ];
}

function mdForGhcBeacon(payload) {
  return [
    "# GHC Current State Beacon",
    "",
    `Status: \`${payload.status}\``,
    "",
    `Generated UTC: \`${payload.generated_utc}\``,
    "",
    "## Active Routing",
    "",
    `- Active memory cue: \`${payload.active_memory_cue}\``,
    `- Stale memory policy: \`${payload.stale_memory_policy}\`.`,
    `- Primary context branch: \`${payload.primary_context_branch}\``,
    `- Archive branch: \`${payload.archive_branch}\``,
    `- Latest remote-verified closeout: \`${payload.latest_remote_verified_closeout}\``,
    `- Active local phase: \`${payload.active_local_phase}\``,
    `- Next prepared phase: \`${payload.next_prepared_phase}\``,
    `- Next active lanes: \`${payload.next_active_lanes.join(", ")}\``,
    "",
    "## Remote-Verified Heads",
    "",
    `- Full omega: \`${payload.remote_verified_heads.omega}\``,
    `- Omega-mini: \`${payload.remote_verified_heads.omega_mini}\``,
    "",
    "## Round Robin Pattern",
    "",
    ...payload.round_robin_pattern.map((item) => `- \`${item}\``),
    "",
    "## Current v541 Local Artifacts",
    "",
    ...payload.current_v541_local_artifacts.map((item) => `- \`${item}\``),
    "",
    "## Next Phase Artifacts",
    "",
    ...payload.next_phase_artifacts.map((item) => `- \`${item}\``),
    "",
    "## Browser Developer Mode Rule",
    "",
    "Use high-level Browser actions for ordinary Lumen messaging. Use CDP for read-only route verification, readiness checks, event/log watching, asset inventory, and profiling. Do not use CDP for direct page mutation unless an exact future approval packet authorizes it.",
    "",
    "## Storage Rule",
    "",
    payload.storage_policy,
    "",
    "## Open Gates",
    "",
    "GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain open.",
  ];
}

function exposureScan(root, relPaths) {
  const patterns = [
    ["secret_like_token", /sk-[A-Za-z0-9_-]{20,}/],
    ["private_chatgpt_url", /https?:\/\/chatgpt\.com\/c\/[0-9A-Za-z:_-]+/],
    ["local_absolute_path", /[A-Z]:\\(?:Users\\hamis|GHC-Archives)\\/i],
    ["session_stream_extension", new RegExp("\\." + "jsonl\\b", "i")],
    ["raw_lane_text_phrase", /raw\s+lane\s+text/i],
  ];
  const hits = [];
  for (const relPath of relPaths) {
    const text = readFileSync(join(root, relPath), "utf8");
    for (const [label, pattern] of patterns) {
      if (pattern.test(text)) hits.push({ file: relPath, label });
    }
  }
  return hits;
}

function writeAll(root) {
  const current = currentStatePayload();
  const beacon = beaconPayload();
  const ghcBeacon = ghcBeaconPayload();
  writeJson(root, "docs/omega-mini-index/omega-mini-current-state-v1.json", current);
  writeMd(root, "docs/omega-mini-index/omega-mini-current-state-v1.md", mdForCurrent(current));
  writeJson(root, "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json", beacon);
  writeMd(root, "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md", mdForBeacon(beacon));
  writeJson(root, "docs/trinity-live-traces/ghc-current-state-beacon-v1.json", ghcBeacon);
  writeMd(root, "docs/trinity-live-traces/ghc-current-state-beacon-v1.md", mdForGhcBeacon(ghcBeacon));

  const written = [
    "docs/omega-mini-index/omega-mini-current-state-v1.json",
    "docs/omega-mini-index/omega-mini-current-state-v1.md",
    "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json",
    "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md",
    "docs/trinity-live-traces/ghc-current-state-beacon-v1.json",
    "docs/trinity-live-traces/ghc-current-state-beacon-v1.md",
  ];
  const exposureHits = exposureScan(root, written);
  const exposureLines = exposureHits.length
    ? exposureHits.map((hit) => `- \`${hit.file}\`: \`${hit.label}\``)
    : ["- None."];
  const guard = {
    schema: "ghc.current_state_forward_pointer_exposure_guard.v1",
    generated_utc: generatedUtc,
    status: exposureHits.length === 0 ? "PASS_CURRENT_STATE_FORWARD_POINTER_GUARD" : "FAIL_CURRENT_STATE_FORWARD_POINTER_GUARD",
    phase_slug: latestCompletedX2,
    next_phase: currentActivePhase,
    checked_files: written,
    exposure_hits: exposureHits,
    publication_boundary: boundary,
    claim_boundary: claimBoundary,
  };
  writeJson(root, "docs/omega-mini-index/v541-gmut-thos-v77-v8-x2-current-state-forward-pointer-exposure-guard-v1.json", guard);
  writeMd(root, "docs/omega-mini-index/v541-gmut-thos-v77-v8-x2-current-state-forward-pointer-exposure-guard-v1.md", [
    "# v541 v8 x2 Current-State Forward Pointer Exposure Guard",
    "",
    `Generated UTC: \`${generatedUtc}\``,
    "",
    `Status: \`${guard.status}\``,
    "",
    `Next phase: \`${currentActivePhase}\``,
    "",
    "## Checked Files",
    "",
    ...written.map((item) => `- \`${item}\``),
    "",
    "## Exposure Hits",
    "",
    ...exposureLines,
    "",
    "## Open Gates",
    "",
    "GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain open.",
  ]);
  return { current, beacon, ghcBeacon, guard };
}

const fullResult = writeAll(fullRoot);
const miniResult = writeAll(miniRoot);

const miniCurrent = readJson(miniRoot, "docs/omega-mini-index/omega-mini-current-state-v1.json");
const result = {
  schema: "ghc.v541_v7_x2_current_state_refresher.result.v1",
  generated_utc: generatedUtc,
  status:
    fullResult.guard.status === "PASS_CURRENT_STATE_FORWARD_POINTER_GUARD" &&
    miniResult.guard.status === "PASS_CURRENT_STATE_FORWARD_POINTER_GUARD"
      ? "PASS_REFRESHED_CURRENT_STATE_TO_V542_V1_X1"
      : "FAIL_REFRESHED_CURRENT_STATE_TO_V542_V1_X1",
  full_head: fullHead,
  mini_head: miniHead,
  next_phase: miniCurrent.current_active_phase,
  latest_closed_phase: miniCurrent.latest_closed_phase,
  lookup_file_count: miniCurrent.current_lookup_files.length,
};
console.log(JSON.stringify(result, null, 2));
