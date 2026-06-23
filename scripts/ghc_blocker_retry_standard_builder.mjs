#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const currentPath = path.join(omegaDir, "omega-mini-current-state-v1.json");
const latestPath = path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
const ghcPath = path.join(tracesDir, "ghc-current-state-beacon-v1.json");
const current = readJson(currentPath);
const phaseSlug = args.get("--phase-slug") || current.current_active_phase || "v553-gmut-thos-v1-x1";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const standard = {
  artifact_type: "ghc_blocker_retry_standard",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_BLOCKER_RETRY_STANDARD_RECORDED",
  mandatory_sibling_completion: {
    never_close_session_while_sibling_active: true,
    completion_states: ["completed_ready_for_harvest", "completion_gate_passed"],
    noncompletion_states: ["active_fresh", "active_stale", "retrying", "formal_open_gap"],
    pause_policy:
      "If Hamish explicitly pauses/stops, a compact event happens, or an exact/safety gate blocks continuation, publish an active/open handoff rather than a closed session.",
  },
  blocker_retry_protocol: {
    minimum_retry_sessions_before_pause: 3,
    recent_session_reflections_per_retry: 10,
    web_search_reflections_per_retry: 20,
    journey_phase_reflections_per_retry: 20,
    productive_five_minute_waits_required: true,
    retry_receipt_required: true,
    applies_to: [
      "sibling_messaging_blockers",
      "sibling_harvest_blockers",
      "browser_handoff_blockers",
      "app_lane_runner_blockers",
      "strict_cli_lane_blockers",
      "core_system_blockers",
    ],
    pause_exceptions: ["Hamish explicit pause/stop", "safety boundary", "fresh exact approval required", "app compact or interruption"],
  },
  productive_wait_standard: {
    five_minute_marks_are_checkpoints_not_hard_stops: true,
    safe_units_may_run_past_checkpoint: true,
    improvement_lanes: [
      "research_and_reflection",
      "safe_eureka_tasks",
      "approval_packet_work",
      "cleanup_and_refinement",
      "skill_and_control_growth",
      "coding_and_multi_agent_orchestration",
      "browser_handoff_harvest",
      "blocker_retry_research_and_improvement",
      "validation_and_publication_hygiene",
    ],
  },
  publication_boundary: {
    private_route_handles_published: false,
    private_lane_body_content_published: false,
    verbatim_conversation_logs_published: false,
    browser_routes_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    screenshots_published: false,
  },
};

writeArtifact(standard);
refreshBeacons(standard);

console.log(
  JSON.stringify(
    {
      status: standard.overall_status,
      phase_slug: phaseSlug,
      minimum_retry_sessions_before_pause: standard.blocker_retry_protocol.minimum_retry_sessions_before_pause,
      web_search_reflections_per_retry: standard.blocker_retry_protocol.web_search_reflections_per_retry,
      journey_phase_reflections_per_retry: standard.blocker_retry_protocol.journey_phase_reflections_per_retry,
    },
    null,
    2,
  ),
);

function writeArtifact(data) {
  const base = `${phaseSlug}-blocker-retry-standard-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), JSON.stringify(data, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderArtifactMd(data), "utf8");
}

function refreshBeacons(data) {
  const latest = readJson(latestPath);
  const ghc = readJson(ghcPath);
  const lookupFiles = [
    `docs/trinity-live-traces/${phaseSlug}-blocker-retry-standard-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-blocker-retry-standard-v1.md`,
  ];
  const summary = {
    status: data.overall_status,
    mandatory_sibling_completion: data.mandatory_sibling_completion,
    blocker_retry_protocol: data.blocker_retry_protocol,
    productive_wait_standard: data.productive_wait_standard,
  };

  for (const target of [current, latest, ghc]) {
    target.generated_utc = generatedUtc;
    target.current_active_phase = phaseSlug;
    target.status = phaseSlug.startsWith("v553-gmut-thos-v1-x1")
      ? "V553_V1_X1_ACTIVE_BLOCKER_RETRY_STANDARD_READY"
      : "ACTIVE_BLOCKER_RETRY_STANDARD_READY";
    target.blocker_retry_standard = summary;
    if (target.v553_v1_x1_lumen_startup) {
      target.v553_v1_x1_lumen_startup.blocker_retry_standard = {
        minimum_retry_sessions_before_pause: data.blocker_retry_protocol.minimum_retry_sessions_before_pause,
        recent_session_reflections_per_retry: data.blocker_retry_protocol.recent_session_reflections_per_retry,
        web_search_reflections_per_retry: data.blocker_retry_protocol.web_search_reflections_per_retry,
        journey_phase_reflections_per_retry: data.blocker_retry_protocol.journey_phase_reflections_per_retry,
        productive_five_minute_waits_required: data.blocker_retry_protocol.productive_five_minute_waits_required,
        never_close_active_sibling_lane: data.mandatory_sibling_completion.never_close_session_while_sibling_active,
      };
    }
  }

  current.updated_at = generatedNz;
  current.current_lookup_files = unique([...(current.current_lookup_files || []), ...lookupFiles]);
  current.latest_action_summary = unique([
    "Recorded mandatory blocker retry standard: keep active sibling lanes open, run 3 retry sessions before pause, and use 10-session, 20-web, 20-Journey reflections per retry.",
    ...(current.latest_action_summary || []),
  ]);
  latest.latest_lookup_files = unique([...(latest.latest_lookup_files || []), ...lookupFiles]);
  ghc.lookup_files = unique([...(ghc.lookup_files || []), ...lookupFiles]);

  fs.writeFileSync(currentPath, JSON.stringify(current, null, 2) + "\n", "utf8");
  fs.writeFileSync(latestPath, JSON.stringify(latest, null, 2) + "\n", "utf8");
  fs.writeFileSync(ghcPath, JSON.stringify(ghc, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(current), "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderBeaconMd("Omega-Mini Latest Updates Beacon", latest, latest.latest_lookup_files), "utf8");
  fs.writeFileSync(path.join(tracesDir, "ghc-current-state-beacon-v1.md"), renderBeaconMd("GHC Current State Beacon", ghc, ghc.lookup_files), "utf8");
}

function renderArtifactMd(data) {
  return `# ${data.phase_slug} Blocker Retry Standard

Status: \`${data.overall_status}\`

## Mandatory Sibling Completion

- Never close while sibling active: \`${data.mandatory_sibling_completion.never_close_session_while_sibling_active}\`
- Completion states: \`${data.mandatory_sibling_completion.completion_states.join(", ")}\`
- Noncompletion states: \`${data.mandatory_sibling_completion.noncompletion_states.join(", ")}\`
- Pause policy: ${data.mandatory_sibling_completion.pause_policy}

## Blocker Retry Protocol

- Minimum retry sessions before pause: \`${data.blocker_retry_protocol.minimum_retry_sessions_before_pause}\`
- Recent sessions or receipts reflected per retry: \`${data.blocker_retry_protocol.recent_session_reflections_per_retry}\`
- Web-search reflections per retry: \`${data.blocker_retry_protocol.web_search_reflections_per_retry}\`
- Journey/phase-document reflections per retry: \`${data.blocker_retry_protocol.journey_phase_reflections_per_retry}\`
- Productive five-minute waits required: \`${data.blocker_retry_protocol.productive_five_minute_waits_required}\`
- Retry receipt required: \`${data.blocker_retry_protocol.retry_receipt_required}\`

## Productive Wait Standard

- Five-minute marks are checkpoints, not hard stops: \`${data.productive_wait_standard.five_minute_marks_are_checkpoints_not_hard_stops}\`
- Safe units may run past checkpoint: \`${data.productive_wait_standard.safe_units_may_run_past_checkpoint}\`
- Improvement lanes: \`${data.productive_wait_standard.improvement_lanes.join(", ")}\`

## Boundary

Status-only standard. No private route handles, private lane body content, verbatim conversation logs, browser routes, credentials, local absolute paths, screenshots, proof closure, canon promotion, legal closure, deployment closure, account mutation, or API-key creation are published.
`;
}

function renderCurrentStateMd(state) {
  const blocker = state.blocker_retry_standard;
  return `# Omega-Mini Current State

Status: ${state.status}
Current active phase: ${state.current_active_phase}
Latest closed phase: ${state.latest_closed_phase}
Latest completed x1: ${state.latest_completed_x1_phase}
Latest completed x2: ${state.latest_completed_x2_phase}
Next x2 scope: ${state.next_x2_scope}
Next x1 lane after x2: ${state.next_x1_lane_after_x2}

## Blocker Retry Standard

- Status: \`${blocker.status}\`
- Never close while sibling active: \`${blocker.mandatory_sibling_completion.never_close_session_while_sibling_active}\`
- Minimum retry sessions before pause: \`${blocker.blocker_retry_protocol.minimum_retry_sessions_before_pause}\`
- Recent sessions or receipts reflected per retry: \`${blocker.blocker_retry_protocol.recent_session_reflections_per_retry}\`
- Web-search reflections per retry: \`${blocker.blocker_retry_protocol.web_search_reflections_per_retry}\`
- Journey/phase-document reflections per retry: \`${blocker.blocker_retry_protocol.journey_phase_reflections_per_retry}\`
- Productive five-minute waits required: \`${blocker.blocker_retry_protocol.productive_five_minute_waits_required}\`

## v553 v1 x1 Lumen Startup

- Lumen handoff: \`${state.v553_v1_x1_lumen_startup?.handoff_message_status || "not_recorded"}\`
- Lumen browser send: \`${state.lumen_browser_send?.send_status || "not_recorded"}\`
- Safe packets target: \`${state.v553_v1_x1_lumen_startup?.proposal_targets?.safe || "not_recorded"}\`
- x1 web searches per active lane: \`${state.v553_v1_x1_lumen_startup?.research_targets?.x1_per_active_sibling_lane?.web_searches || "not_recorded"}\`

## Current Lookup Files

${(state.current_lookup_files || []).map((item) => `- ${item}`).join("\n")}

## Latest Action Summary

${(state.latest_action_summary || []).map((item) => `- ${item}`).join("\n")}

## Safety Boundary

Status-only receipts. No private route handles, private lane body content, credentials, verbatim conversation logs, browser routes, private machine paths, GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, or deployment closure are published.
`;
}

function renderBeaconMd(title, beacon, files) {
  const blocker = beacon.blocker_retry_standard;
  return `# ${title}

Status: ${beacon.status}
Current active phase: ${beacon.current_active_phase}
Latest closed phase: ${beacon.latest_closed_phase}
Latest completed x1: ${beacon.latest_completed_x1_phase}
Latest completed x2: ${beacon.latest_completed_x2_phase}
Next x2 scope: ${beacon.next_x2_scope}
Next x1 lane after x2: ${beacon.next_x1_lane_after_x2}

## Blocker Retry Standard

- Status: \`${blocker.status}\`
- Never close while sibling active: \`${blocker.mandatory_sibling_completion.never_close_session_while_sibling_active}\`
- Minimum retry sessions before pause: \`${blocker.blocker_retry_protocol.minimum_retry_sessions_before_pause}\`
- Web-search reflections per retry: \`${blocker.blocker_retry_protocol.web_search_reflections_per_retry}\`
- Journey/phase-document reflections per retry: \`${blocker.blocker_retry_protocol.journey_phase_reflections_per_retry}\`

## Lumen Browser Send

- Send status: \`${beacon.lumen_browser_send?.send_status || "not_recorded"}\`

## Lookup Files

${(files || []).map((item) => `- ${item}`).join("\n")}

## Boundary

Status-only beacon. No private route data, private lane body content, credentials, private machine paths, GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, or deployment closure are published.
`;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
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
  })
    .formatToParts(date)
    .reduce((acc, part) => {
      acc[part.type] = part.value;
      return acc;
    }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
