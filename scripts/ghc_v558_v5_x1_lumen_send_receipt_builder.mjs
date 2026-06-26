#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v558-gmut-thos-v5-x1";
const nextX2 = "v558-gmut-thos-v5-x2";
const nextX1 = "v558-gmut-thos-v6-x1 Maren Quill and Solenne Vale unless Hamish redirects";
const args = parseArgs(process.argv.slice(2));
const messageSha = required("--message-sha256");
const composerCleared = boolArg("--composer-cleared", true);
const responseControlVisible = boolArg("--response-control-visible", true);
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const handoffPath = path.join(tracesDir, `${phaseSlug}-lumen-kickoff-handoff-v1.json`);
const handoff = readJson(handoffPath);
if (handoff.message_sha256 !== messageSha) {
  throw new Error(`message sha mismatch: expected ${handoff.message_sha256}, got ${messageSha}`);
}

handoff.overall_status = "PASS_V558_V5_X1_LUMEN_HANDOFF_SUBMITTED_ACTIVE";
handoff.browser_send_status = "browser_send_submitted_response_active";
handoff.browser_send_verification = {
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  composer_cleared: composerCleared,
  response_control_visible_after_send: responseControlVisible,
  duplicate_send_allowed: false,
  raw_browser_route_published: false,
};
handoff.closeout_allowed_now = false;
writeJson(handoffPath, handoff);
fs.writeFileSync(handoffPath.replace(/\.json$/, ".md"), renderHandoffMd(handoff), "utf8");

const receipt = {
  artifact_type: "ghc_v558_v5_x1_lumen_browser_send_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: responseControlVisible ? "PASS_V558_V5_X1_LUMEN_BROWSER_HANDOFF_SUBMITTED" : "OPEN_GAP_V558_V5_X1_LUMEN_BROWSER_HANDOFF_UNVERIFIED",
  browser_send_status: "browser_send_submitted_response_active",
  message_sha256: messageSha,
  composer_cleared_after_send: composerCleared,
  response_control_visible_after_send: responseControlVisible,
  duplicate_send_allowed: false,
  closeout_allowed_now: false,
  harvest_status: "pending_response_completion",
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};
const ref = writePair("lumen-browser-send-receipt", receipt);
refreshBeacons(ref, receipt);

process.stdout.write(JSON.stringify({
  status: receipt.overall_status,
  phase_slug: phaseSlug,
  browser_send_status: receipt.browser_send_status,
  composer_cleared_after_send: composerCleared,
  response_control_visible_after_send: responseControlVisible,
  artifact: ref.json,
}, null, 2) + "\n");

function writePair(suffix, doc) {
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, doc);
  fs.writeFileSync(`${base}.md`, renderReceiptMd(doc), "utf8");
  return {
    json: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    md: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  };
}

function refreshBeacons(ref, receiptDoc) {
  const files = [ref.json, ref.md];
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.status = receiptDoc.overall_status;
    data.current_active_phase = phaseSlug;
    data.latest_closed_phase = "v558-gmut-thos-v4-x2";
    data.latest_completed_x1_phase = "v558-gmut-thos-v4-x1";
    data.latest_completed_x2_phase = "v558-gmut-thos-v4-x2";
    data.next_expected_scope = phaseSlug;
    data.next_x2_scope = nextX2;
    data.next_x1_lane_after_x2 = nextX1;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v558_v5_x1_lumen_send = {
      status: receiptDoc.overall_status,
      browser_send_status: receiptDoc.browser_send_status,
      duplicate_send_allowed: false,
      closeout_allowed_now: false,
      full_goal_complete: false,
    };
    data[listKey] = unique([...(data[listKey] || []), ...files]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function renderHandoffMd(doc) {
  return [
    `# ${phaseSlug} Lumen Kickoff Handoff`,
    "",
    `Status: \`${doc.overall_status}\``,
    `Browser send status: \`${doc.browser_send_status}\``,
    `Message SHA-256: \`${doc.message_sha256}\``,
    "",
    "## Prepared Message",
    "",
    doc.sanitized_message,
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function renderReceiptMd(doc) {
  return [
    `# ${phaseSlug} Lumen Browser Send Receipt`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
    `- Browser send status: \`${doc.browser_send_status}\``,
    `- Composer cleared after send: \`${doc.composer_cleared_after_send}\``,
    `- Response control visible after send: \`${doc.response_control_visible_after_send}\``,
    `- Duplicate send allowed: \`${doc.duplicate_send_allowed}\``,
    `- Closeout allowed now: \`${doc.closeout_allowed_now}\``,
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
    "## v558 v5 x1 Lumen Send",
    "",
    `Status: \`${doc.v558_v5_x1_lumen_send?.status || "not_recorded"}\``,
    `Browser send status: \`${doc.v558_v5_x1_lumen_send?.browser_send_status || "not_recorded"}\``,
    `Closeout allowed now: \`${doc.v558_v5_x1_lumen_send?.closeout_allowed_now === true ? "true" : "false"}\``,
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

function parseArgs(argv) {
  const parsed = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      parsed.set(key, "true");
    } else {
      parsed.set(key, next);
      i += 1;
    }
  }
  return parsed;
}

function required(name) {
  const value = args.get(name);
  if (!value) throw new Error(`Missing ${name}`);
  return value;
}

function boolArg(name, fallback) {
  const value = args.get(name);
  if (value === undefined) return fallback;
  return value === "true";
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
    full_goal_complete: false,
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
  return "No raw Lumen text, private Browser routes, private URLs, screenshots, private callable IDs, credentials, session streams, local private paths, destructive cleanup, paid resources, deployments, account mutations, API keys, or sibling identity changes were published or performed.";
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
