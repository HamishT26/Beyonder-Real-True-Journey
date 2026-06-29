#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = parseArgs();
const phaseSlug = required("--phase-slug");
const summaryKey = args.get("--summary-key") || "v553_v3_x1_lumen_startup";
const sendStatus = args.get("--send-status") || "browser_send_submitted_response_active";
const verification = args.get("--verification") || "composer_cleared_and_response_control_visible";
const composerCleared = parseBool(args.get("--composer-cleared"), true);
const responseControlVisible = parseBool(args.get("--response-control-visible"), true);
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const handoffBase = args.get("--handoff-base") || firstExistingHandoffBase(phaseSlug);
const handoffJsonPath = path.join(tracesDir, `${handoffBase}.json`);
const handoffMdPath = path.join(tracesDir, `${handoffBase}.md`);
const handoff = readJson(handoffJsonPath);
handoff.live_send_status = sendStatus;
handoff.browser_send_verification = {
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  verification,
  composer_cleared: composerCleared,
  response_control_visible_after_send: responseControlVisible,
  raw_browser_route_published: false,
};
fs.writeFileSync(handoffJsonPath, `${JSON.stringify(handoff, null, 2)}\n`, "utf8");
fs.writeFileSync(handoffMdPath, renderHandoffMd(handoff), "utf8");

const receipt = {
  artifact_type: "ghc_lumen_browser_send_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: browserSendOverallStatus(sendStatus, responseControlVisible),
  intended_recipient: "Lumen Vale",
  route: "in_app_browser_current_lumen_thread",
  send_status: sendStatus,
  verification: {
    composer_cleared: composerCleared,
    response_control_visible_after_send: responseControlVisible,
    verification,
  },
  publication_boundary: publicationBoundary(),
};

const base = `${phaseSlug}-lumen-browser-send-receipt-v1`;
fs.writeFileSync(path.join(tracesDir, `${base}.json`), `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderReceiptMd(receipt), "utf8");
refreshBeacons(receipt);

console.log(
  JSON.stringify(
    {
      status: receipt.overall_status,
      phase_slug: phaseSlug,
      send_status: sendStatus,
      receipt: `${base}.json`,
    },
    null,
    2,
  ),
);

function parseArgs() {
  const parsed = new Map();
  for (let index = 2; index < process.argv.length; index += 2) {
    parsed.set(process.argv[index], process.argv[index + 1]);
  }
  return parsed;
}

function required(flag) {
  const value = args.get(flag);
  if (!value) {
    console.error(`Usage: node ghc_lumen_browser_send_receipt_builder.mjs ${flag} <value>`);
    process.exit(2);
  }
  return value;
}

function parseBool(value, fallback) {
  if (value === undefined) return fallback;
  return value === "true";
}

function refreshBeacons(receipt) {
  const currentPath = path.join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const ghcPath = path.join(tracesDir, "ghc-current-state-beacon-v1.json");
  const files = [
    `docs/trinity-live-traces/${phaseSlug}-lumen-browser-send-receipt-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-lumen-browser-send-receipt-v1.md`,
  ];
  for (const file of [currentPath, latestPath, ghcPath]) {
    const data = readJson(file);
    data.generated_utc = generatedUtc;
    if (file === currentPath) data.updated_at = generatedNz;
    data.current_active_phase = phaseSlug;
    data.lumen_browser_send = {
      status: receipt.overall_status,
      send_status: receipt.send_status,
      intended_recipient: receipt.intended_recipient,
      verification: receipt.verification,
      raw_browser_route_published: false,
      raw_transcript_published: false,
    };
    if (data[summaryKey]) {
      data[summaryKey].handoff_message_status = receipt.send_status;
    }
    const listKey = file === latestPath ? "latest_lookup_files" : file === ghcPath ? "lookup_files" : "current_lookup_files";
    data[listKey] = unique([...(data[listKey] || []), ...files]);
    if (file === currentPath) {
      data.latest_action_summary = unique([
        `Submitted ${phaseSlug} Lumen handoff through the in-app Browser and recorded a sanitized send receipt.`,
        ...(data.latest_action_summary || []),
      ]);
    }
    fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
    if (file === currentPath) {
      fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(data), "utf8");
    } else if (file === latestPath) {
      fs.writeFileSync(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderBeaconMd("Omega-Mini Latest Updates Beacon", data, data.latest_lookup_files), "utf8");
    } else {
      fs.writeFileSync(path.join(tracesDir, "ghc-current-state-beacon-v1.md"), renderBeaconMd("GHC Current State Beacon", data, data.lookup_files), "utf8");
    }
  }
}

function renderHandoffMd(data) {
  const message = data.message_text || data.message || "";
  const maximumCharacters = data.maximum_message_characters || data.message_character_count || message.length;
  return `# ${data.phase_slug} Lumen Handoff Message

Status: \`${data.live_send_status}\`
Message characters: \`${maximumCharacters}\`

## Browser Send Verification

- Verification: \`${data.browser_send_verification.verification}\`
- Composer cleared: \`${data.browser_send_verification.composer_cleared}\`
- Response control visible after send: \`${data.browser_send_verification.response_control_visible_after_send}\`
- Raw browser route published: \`${data.browser_send_verification.raw_browser_route_published}\`

## Message

${message}

## Boundary

${boundarySentence()}
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
  const summary = current[summaryKey] || {};
  return `# Omega-Mini Current State

Status: ${current.status}
Current active phase: ${current.current_active_phase}
Latest closed phase: ${current.latest_closed_phase}
Latest completed x1: ${current.latest_completed_x1_phase}
Latest completed x2: ${current.latest_completed_x2_phase}
Next expected scope: ${current.next_expected_scope}
Next x2 scope: ${current.next_x2_scope}
Next x1 lane after x2: ${current.next_x1_lane_after_x2}

## ${summaryKey.replaceAll("_", " ")}

- Status: \`${summary.status || "not_recorded"}\`
- Lumen handoff: \`${summary.handoff_message_status || "not_recorded"}\`
- Web reflections: \`${summary.web_reflection_rows || "not_recorded"}\`
- Journey/phase reflections: \`${summary.journey_phase_reflection_rows || "not_recorded"}\`

## Lumen Browser Send

- Status: \`${current.lumen_browser_send?.status || "not_recorded"}\`
- Send status: \`${current.lumen_browser_send?.send_status || "not_recorded"}\`
- Verification: \`${current.lumen_browser_send?.verification?.verification || "not_recorded"}\`

## Current Lookup Files

${(current.current_lookup_files || []).map((item) => `- ${item}`).join("\n")}

## Latest Action Summary

${(current.latest_action_summary || []).map((item) => `- ${item}`).join("\n")}

## Safety Boundary

${boundarySentence()}
`;
}

function renderBeaconMd(title, beacon, files) {
  const summary = beacon[summaryKey] || {};
  return `# ${title}

Status: ${beacon.status}
Current active phase: ${beacon.current_active_phase}
Latest closed phase: ${beacon.latest_closed_phase}
Latest completed x1: ${beacon.latest_completed_x1_phase}
Latest completed x2: ${beacon.latest_completed_x2_phase}
Next expected scope: ${beacon.next_expected_scope}
Next x2 scope: ${beacon.next_x2_scope}
Next x1 lane after x2: ${beacon.next_x1_lane_after_x2}

## ${summaryKey.replaceAll("_", " ")}

- Status: \`${summary.status || "not_recorded"}\`
- Lumen handoff: \`${summary.handoff_message_status || "not_recorded"}\`

## Lumen Browser Send

- Status: \`${beacon.lumen_browser_send?.status || "not_recorded"}\`
- Send status: \`${beacon.lumen_browser_send?.send_status || "not_recorded"}\`

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

function browserSendOverallStatus(status, controlVisible) {
  if (status === "browser_send_submitted_response_completed_ready_for_harvest") {
    return "PASS_LUMEN_BROWSER_HANDOFF_COMPLETED_READY_FOR_HARVEST";
  }
  if (status === "browser_send_submitted_response_active" && controlVisible) {
    return "PASS_LUMEN_BROWSER_HANDOFF_SUBMITTED_RESPONSE_ACTIVE";
  }
  return controlVisible ? "PASS_LUMEN_BROWSER_HANDOFF_SUBMITTED" : "OPEN_GAP_LUMEN_BROWSER_HANDOFF_SUBMISSION_UNVERIFIED";
}

function firstExistingHandoffBase(slug) {
  const candidates = [
    `${slug}-lumen-handoff-message-v1`,
    `${slug}-lumen-browser-handoff-v1`,
  ];
  for (const candidate of candidates) {
    if (fs.existsSync(path.join(tracesDir, `${candidate}.json`))) return candidate;
  }
  return candidates[0];
}

function boundarySentence() {
  return "No private route handles, private lane body content, verbatim conversation logs, browser routes, credentials, local absolute paths, screenshots, proof closure, canon promotion, legal closure, deployment closure, account mutation, purchase, API-key creation, or sibling identity replacement are published or claimed.";
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
