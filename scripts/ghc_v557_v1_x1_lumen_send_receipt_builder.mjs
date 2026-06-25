#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const phaseSlug = "v557-gmut-thos-v1-x1";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const handoff = readJson(path.join(tracesDir, `${phaseSlug}-lumen-handoff-message-v1.json`));
handoff.overall_status = "PASS_V557_V1_X1_LUMEN_HANDOFF_SUBMITTED_RESPONSE_ACTIVE";
handoff.browser_send_status = "browser_send_submitted_response_active";
handoff.live_send_status = "browser_send_submitted_response_active";
handoff.browser_send_verification = {
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  verification: "composer_cleared_and_response_control_visible",
  composer_cleared: true,
  response_control_visible_after_send: true,
  duplicate_send_performed: false,
  raw_browser_route_published: false,
};
writeJson(path.join(tracesDir, `${phaseSlug}-lumen-handoff-message-v1.json`), handoff);
fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-lumen-handoff-message-v1.md`), renderHandoffMd(handoff), "utf8");

const receipt = {
  artifact_type: "ghc_lumen_browser_send_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_LUMEN_BROWSER_HANDOFF_SUBMITTED",
  intended_recipient: "Lumen Vale",
  route: "in_app_browser_current_lumen_thread",
  send_status: "browser_send_submitted_response_active",
  verification: {
    composer_cleared: true,
    response_control_visible_after_send: true,
    verification: "composer_cleared_and_response_control_visible",
    duplicate_send_performed: false,
  },
  publication_boundary: {
    private_route_handles_published: false,
    private_lane_body_content_published: false,
    verbatim_conversation_logs_published: false,
    browser_routes_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    screenshots_published: false,
    raw_browser_route_published: false,
    private_urls_published: false,
    raw_transcripts_published: false,
    private_callable_ids_published: false,
  },
};
writeJson(path.join(tracesDir, `${phaseSlug}-lumen-browser-send-receipt-v1.json`), receipt);
fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-lumen-browser-send-receipt-v1.md`), renderReceiptMd(receipt), "utf8");
refreshBeacons(receipt);

process.stdout.write(JSON.stringify({
  status: receipt.overall_status,
  phase_slug: phaseSlug,
  send_status: receipt.send_status,
  composer_cleared: true,
  response_control_visible_after_send: true,
}, null, 2) + "\n");

function refreshBeacons(receipt) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-lumen-browser-send-receipt-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-lumen-browser-send-receipt-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-lumen-handoff-message-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-lumen-handoff-message-v1.md`,
  ];
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = receipt.overall_status;
    doc.current_active_phase = phaseSlug;
    doc.next_expected_scope = phaseSlug;
    doc.v557_v1_x1_lumen_handoff = {
      status: receipt.overall_status,
      browser_send_status: receipt.send_status,
      duplicate_send_allowed: false,
      composer_cleared: true,
      response_control_visible_after_send: true,
      raw_browser_route_published: false,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function renderHandoffMd(data) {
  return [
    `# ${phaseSlug} Lumen Handoff Message`,
    "",
    `Status: \`${data.overall_status}\``,
    `Browser send status: \`${data.browser_send_status}\``,
    `Message characters: \`${data.message_character_count}\``,
    "",
    "## Message",
    "",
    "```text",
    data.message_text,
    "```",
    "",
    "## Send Verification",
    "",
    "- composer cleared: `true`",
    "- response control visible after send: `true`",
    "- duplicate send performed: `false`",
    "- raw browser route published: `false`",
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function renderReceiptMd(data) {
  return [
    `# ${phaseSlug} Lumen Browser Send Receipt`,
    "",
    `Status: \`${data.overall_status}\``,
    `Send status: \`${data.send_status}\``,
    "",
    "## Verification",
    "",
    "- composer cleared: `true`",
    "- response control visible after send: `true`",
    "- duplicate send performed: `false`",
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
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## v557 v1 x1 Lumen Handoff",
    "",
    `- status: \`${doc.v557_v1_x1_lumen_handoff?.status || "not_recorded"}\``,
    `- browser send status: \`${doc.v557_v1_x1_lumen_handoff?.browser_send_status || "not_recorded"}\``,
    `- duplicate send allowed: \`${doc.v557_v1_x1_lumen_handoff?.duplicate_send_allowed ?? "not_recorded"}\``,
    `- composer cleared: \`${doc.v557_v1_x1_lumen_handoff?.composer_cleared ?? "not_recorded"}\``,
    `- response control visible after send: \`${doc.v557_v1_x1_lumen_handoff?.response_control_visible_after_send ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`),
    "",
  ].join("\n");
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function boundarySentence() {
  return "Sanitized receipt only. No raw Browser route, private URL, raw transcript, screenshot, credential, local absolute path, private callable ID, raw lane text, hidden reasoning, proof closure, or sibling merge claim is published.";
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
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
