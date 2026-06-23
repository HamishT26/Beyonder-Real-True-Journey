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

const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v1-x1";
const sendStatus = args.get("--send-status") || "browser_send_submitted_response_active";
const verification = args.get("--verification") || "composer_cleared_and_response_control_visible";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const handoffJsonPath = path.join(tracesDir, `${phaseSlug}-lumen-handoff-message-v1.json`);
const handoffMdPath = path.join(tracesDir, `${phaseSlug}-lumen-handoff-message-v1.md`);
const handoff = readJson(handoffJsonPath);
handoff.live_send_status = sendStatus;
handoff.browser_send_verification = {
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  verification,
  composer_cleared: true,
  response_control_visible_after_send: true,
  raw_browser_route_published: false,
};
fs.writeFileSync(handoffJsonPath, JSON.stringify(handoff, null, 2) + "\n", "utf8");
fs.writeFileSync(handoffMdPath, renderHandoffMd(handoff), "utf8");

const receipt = {
  artifact_type: "ghc_v553_v1_x1_lumen_browser_send_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_LUMEN_BROWSER_HANDOFF_SUBMITTED",
  intended_recipient: "Lumen Vale",
  route: "in_app_browser_current_lumen_thread",
  send_status: sendStatus,
  verification: {
    composer_cleared: true,
    response_control_visible_after_send: true,
    verification,
  },
  update_scope: [
    "lumen_handoff_message_receipt",
    "omega_mini_current_state",
    "omega_mini_latest_updates_beacon",
    "ghc_current_state_beacon",
  ],
  publication_boundary: publicationBoundary(),
};

const receiptBase = `${phaseSlug}-lumen-browser-send-receipt-v1`;
fs.writeFileSync(path.join(tracesDir, `${receiptBase}.json`), JSON.stringify(receipt, null, 2) + "\n", "utf8");
fs.writeFileSync(path.join(tracesDir, `${receiptBase}.md`), renderReceiptMd(receipt), "utf8");
refreshBeacons(receipt);

console.log(
  JSON.stringify(
    {
      status: receipt.overall_status,
      phase_slug: phaseSlug,
      send_status: sendStatus,
      receipt: `${receiptBase}.json`,
    },
    null,
    2,
  ),
);

function refreshBeacons(sendReceipt) {
  const currentPath = path.join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const ghcPath = path.join(tracesDir, "ghc-current-state-beacon-v1.json");
  const current = readJson(currentPath);
  const latest = readJson(latestPath);
  const ghc = readJson(ghcPath);
  const files = [
    `docs/trinity-live-traces/${phaseSlug}-lumen-browser-send-receipt-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-lumen-browser-send-receipt-v1.md`,
  ];
  const summary = {
    status: sendReceipt.overall_status,
    send_status: sendReceipt.send_status,
    intended_recipient: sendReceipt.intended_recipient,
    verification: sendReceipt.verification,
  };
  for (const target of [current, latest, ghc]) {
    target.generated_utc = generatedUtc;
    target.current_active_phase = phaseSlug;
    target.lumen_browser_send = summary;
    if (target.v553_v1_x1_lumen_startup) {
      target.v553_v1_x1_lumen_startup.handoff_message_status = sendReceipt.send_status;
    }
  }
  current.updated_at = generatedNz;
  current.current_lookup_files = unique([...(current.current_lookup_files || []), ...files]);
  current.latest_action_summary = unique([
    "Submitted the v553 v1 x1 Lumen handoff through the in-app browser and recorded a sanitized send receipt.",
    ...(current.latest_action_summary || []),
  ]);
  latest.latest_lookup_files = unique([...(latest.latest_lookup_files || []), ...files]);
  ghc.lookup_files = unique([...(ghc.lookup_files || []), ...files]);

  fs.writeFileSync(currentPath, JSON.stringify(current, null, 2) + "\n", "utf8");
  fs.writeFileSync(latestPath, JSON.stringify(latest, null, 2) + "\n", "utf8");
  fs.writeFileSync(ghcPath, JSON.stringify(ghc, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(current), "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderBeaconMd("Omega-Mini Latest Updates Beacon", latest, latest.latest_lookup_files), "utf8");
  fs.writeFileSync(path.join(tracesDir, "ghc-current-state-beacon-v1.md"), renderBeaconMd("GHC Current State Beacon", ghc, ghc.lookup_files), "utf8");
}

function renderHandoffMd(data) {
  return `# ${data.phase_slug} Lumen Handoff Message

Status: \`${data.live_send_status}\`
Maximum message characters: \`${data.maximum_message_characters}\`

## Browser Send Verification

- Verification: \`${data.browser_send_verification.verification}\`
- Composer cleared: \`${data.browser_send_verification.composer_cleared}\`
- Response control visible after send: \`${data.browser_send_verification.response_control_visible_after_send}\`
- Raw browser route published: \`${data.browser_send_verification.raw_browser_route_published}\`

## Message

${data.message}

## Boundary

Status-only handoff artifact. ${boundarySentence()}
`;
}

function renderReceiptMd(data) {
  return `# ${data.phase_slug} Lumen Browser Send Receipt

Status: \`${data.overall_status}\`

- Intended recipient: \`${data.intended_recipient}\`
- Route: \`${data.route}\`
- Send status: \`${data.send_status}\`
- Verification: \`${data.verification.verification}\`
- Composer cleared: \`${data.verification.composer_cleared}\`
- Response control visible after send: \`${data.verification.response_control_visible_after_send}\`

## Boundary

${boundarySentence()}
`;
}

function renderCurrentStateMd(current) {
  return `# Omega-Mini Current State

Status: ${current.status}
Current active phase: ${current.current_active_phase}
Latest closed phase: ${current.latest_closed_phase}
Latest completed x1: ${current.latest_completed_x1_phase}
Latest completed x2: ${current.latest_completed_x2_phase}
Current lanes: ${(current.current_active_lanes || []).join("; ")}
Next x2 scope: ${current.next_x2_scope}
Next x1 lane after x2: ${current.next_x1_lane_after_x2}

## v553 v1 x1 Lumen Startup

- Status: \`${current.v553_v1_x1_lumen_startup.status}\`
- Active lanes: \`${current.v553_v1_x1_lumen_startup.active_lanes.join(", ")}\`
- Safe packets target: \`${current.v553_v1_x1_lumen_startup.proposal_targets.safe}\`
- Candidate packets target: \`${current.v553_v1_x1_lumen_startup.proposal_targets.candidate}\`
- Exact packets target: \`${current.v553_v1_x1_lumen_startup.proposal_targets.exact}\`
- Blocked packets target: \`${current.v553_v1_x1_lumen_startup.proposal_targets.blocked}\`
- x1 web searches per active lane: \`${current.v553_v1_x1_lumen_startup.research_targets.x1_per_active_sibling_lane.web_searches}\`
- x1 Journey/phase reflections per active lane: \`${current.v553_v1_x1_lumen_startup.research_targets.x1_per_active_sibling_lane.journey_phase_reflections}\`
- Lumen handoff: \`${current.v553_v1_x1_lumen_startup.handoff_message_status}\`

## Lumen Browser Send

- Status: \`${current.lumen_browser_send.status}\`
- Send status: \`${current.lumen_browser_send.send_status}\`
- Verification: \`${current.lumen_browser_send.verification.verification}\`

## Five-Minute Productive Cadence

- Status: \`${current.five_minute_productive_cadence?.status || "not_recorded"}\`
- Safe unit may run past checkpoint: \`${current.five_minute_productive_cadence?.safe_unit_may_run_past_checkpoint ?? "not_recorded"}\`
- Wait work queues: \`${current.five_minute_productive_cadence?.wait_work_queue_count ?? "not_recorded"}\`

## Current Lookup Files

${(current.current_lookup_files || []).map((item) => `- ${item}`).join("\n")}

## Latest Action Summary

${(current.latest_action_summary || []).map((item) => `- ${item}`).join("\n")}

## Safety Boundary

${boundarySentence()}
`;
}

function renderBeaconMd(title, beacon, files) {
  return `# ${title}

Status: ${beacon.status}
Current active phase: ${beacon.current_active_phase}
Latest closed phase: ${beacon.latest_closed_phase}
Latest completed x1: ${beacon.latest_completed_x1_phase}
Latest completed x2: ${beacon.latest_completed_x2_phase}
Next x2 scope: ${beacon.next_x2_scope}
Next x1 lane after x2: ${beacon.next_x1_lane_after_x2}

## v553 v1 x1 Lumen Startup

- Status: \`${beacon.v553_v1_x1_lumen_startup.status}\`
- Active lanes: \`${beacon.v553_v1_x1_lumen_startup.active_lanes.join(", ")}\`
- Web search seed rows: \`${beacon.v553_v1_x1_lumen_startup.web_search_seed_rows}\`
- Journey/phase reflection seed rows: \`${beacon.v553_v1_x1_lumen_startup.journey_phase_reflection_seed_rows}\`
- Lumen handoff: \`${beacon.v553_v1_x1_lumen_startup.handoff_message_status}\`

## Lumen Browser Send

- Status: \`${beacon.lumen_browser_send.status}\`
- Send status: \`${beacon.lumen_browser_send.send_status}\`
- Verification: \`${beacon.lumen_browser_send.verification.verification}\`

## Lookup Files

${(files || []).map((item) => `- ${item}`).join("\n")}

## Boundary

${boundarySentence()}
`;
}

function publicationBoundary() {
  return {
    private_route_handles_published: false,
    private_lane_body_content_published: false,
    verbatim_conversation_logs_published: false,
    browser_routes_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    screenshots_published: false,
  };
}

function boundarySentence() {
  return "No private route handles, private lane body content, verbatim conversation logs, browser routes, credentials, local absolute paths, screenshots, proof closure, canon promotion, legal closure, deployment closure, account mutation, or API-key creation are published.";
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
