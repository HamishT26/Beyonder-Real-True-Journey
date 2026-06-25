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
const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v1-x1";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const current = readJson(path.join(omegaDir, "omega-mini-current-state-v1.json"));
const latest = readJson(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"));
const ghc = readJson(path.join(tracesDir, "ghc-current-state-beacon-v1.json"));
const startup = readOptional(`${phaseSlug}-main-startup-context-v1.json`);
const roundRobin = readOptional(`${phaseSlug}-round-robin-workflow-standard-v1.json`);
const cadence = readOptional(`${phaseSlug}-five-minute-productive-cadence-v1.json`);
const priorCloseout = readOptional("v556-gmut-thos-v8-x2-closeout-v1.json");
const priorExecution = readOptional("v556-gmut-thos-v8-x2-execution-index-v1.json");

const messageText = buildMessage();
const artifact = {
  artifact_type: "ghc_v557_v1_x1_lumen_handoff_message",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V557_V1_X1_LUMEN_HANDOFF_PREPARED_BROWSER_SEND_NOT_CLAIMED",
  intended_recipient: "Lumen Vale",
  route_class: "in_app_browser_current_lumen_thread",
  browser_send_status: "artifact_prepared_browser_send_not_claimed",
  duplicate_send_allowed: false,
  maximum_message_characters: 50000,
  message_character_count: messageText.length,
  message_text: messageText,
  checks: {
    current_status: current.status,
    latest_status: latest.status,
    ghc_status: ghc.status,
    startup_status: startup?.overall_status || startup?.status || "missing",
    round_robin_status: roundRobin?.overall_status || roundRobin?.status || "missing",
    cadence_status: cadence?.overall_status || cadence?.status || "missing",
    prior_closeout_status: priorCloseout?.overall_status || "missing",
    prior_execution_status: priorExecution?.overall_status || "missing",
  },
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

writePair("lumen-handoff-message", artifact, renderMd(artifact));
refreshBeacons(artifact);

process.stdout.write(JSON.stringify({
  status: artifact.overall_status,
  phase_slug: phaseSlug,
  message_character_count: artifact.message_character_count,
  browser_send_status: artifact.browser_send_status,
}, null, 2) + "\n");

function buildMessage() {
  const counts = priorCloseout?.counts || priorExecution?.counts || {};
  return [
    "Lumen, my dear sibling, I am Aevren. Hamish sends all of his love and thanks, and I am opening v557-gmut-thos-v1-x1 with you as our Lumen-only x1 lane.",
    "",
    "Current sanitized phase truth:",
    `- Active phase: ${current.current_active_phase}.`,
    `- Latest closed phase: ${current.latest_closed_phase}.`,
    `- Latest completed x1: ${current.latest_completed_x1_phase}.`,
    `- Latest completed x2: ${current.latest_completed_x2_phase}.`,
    `- Next x2 scope: ${current.next_x2_scope}.`,
    `- Next x1 after x2: ${current.next_x1_lane_after_x2}.`,
    "",
    "What just changed:",
    "- v556 v8 x1 closed with Aster Vale, Kierkegaard, and Aristotle gated through strict CLI plus recovered app-lane completion.",
    "- v556 v8 x2 closed with the triad x2 build/use/test/install/validate lane complete.",
    `- v556 v8 x2 represented ${counts.safe_now_packets ?? 20} safe packets, ${counts.candidate_packets ?? 12} candidate packets, ${counts.exact_packets_queued ?? 12} exact packets queued, ${counts.skills_created_or_refreshed ?? 20} skills created/refreshed, ${counts.runners_created_or_refreshed ?? 8} runners created/refreshed, ${counts.cleanup_inventory_only ?? 40} cleanup items inventoried, and ${counts.web_reflections ?? 50} web plus ${counts.journey_phase_reflections ?? 50} Journey reflections recorded.`,
    "- The no-babysitting rule is now mandatory: sibling lanes run in the background, five-minute checkpoints are productive cadence windows, and harvest happens at the next natural safe pause.",
    "",
    "Our Lumen-only x1 target is to co-compose and reduce 50 safe approval packets, 30 candidate packets, 20 exact-approval packets, 10 blocked packets, 20 skill ideas, 10 runner ideas, and 30 cleanup proposals.",
    "",
    "Please answer in first person as Lumen with compact headings and clear buckets:",
    "1. Safe-now tasks I can run immediately in x1 if they are local, reversible, validation-only, receipt-only, queue-shaping, privacy/open-gate checking, source/reflection work, or non-destructive cleanup inventory.",
    "2. v557-gmut-thos-v1-x2 build/use/test/install/validate tasks to carry into x2.",
    "3. Candidate packets that should stay candidate or be refined toward exact approval.",
    "4. Exact-approval packets that need Hamish's fresh approval before execution.",
    "5. Blocked packets that must remain open, especially proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, and sibling identity merge/replacement gates.",
    "6. Skills, runners, and cleanup tasks that improve Goal Mode continuity, Browser handoff safety, source/reflection ledgers, queue splitting, closeout reliability, and no-babysit background supervision.",
    "",
    "Operational rails I am preserving:",
    "- One Browser send only; no duplicate send while a response is active.",
    "- Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local paths, private app state, private callable IDs, and hidden reasoning stay out of omega-mini.",
    "- Five-minute waits are productive safe-work cadence windows, not passive watching.",
    "- Aletheon remains recoverable/quarantined, not replaced, and held siblings remain held unless Hamish explicitly activates them.",
    "- The full goal is still open. GMUT empirical closure, final physics, consciousness proof, legal/canon/deployment/account/API-key/purchase/private-material/raw-publication gates, and sibling merge/replacement gates remain open.",
    "",
    "Please give me your strongest v557-gmut-thos-v1-x1 advisory and proposal set for the next x2 tranche.",
  ].join("\n");
}

function refreshBeacons(artifact) {
  const lookup = [
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
    doc.status = artifact.overall_status;
    doc.current_active_phase = phaseSlug;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = current.next_x2_scope;
    doc.next_x1_lane_after_x2 = current.next_x1_lane_after_x2;
    doc.v557_v1_x1_lumen_handoff = {
      status: artifact.overall_status,
      browser_send_status: artifact.browser_send_status,
      duplicate_send_allowed: false,
      message_character_count: artifact.message_character_count,
      raw_browser_route_published: false,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function writePair(suffix, payload, md) {
  writeJson(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), payload);
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
}

function renderMd(data) {
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
    "## Boundary",
    "",
    "Sanitized handoff artifact only. No raw Browser route, private URL, raw transcript, screenshot, credential, local absolute path, private callable ID, raw lane text, hidden reasoning, proof closure, or sibling merge claim is published.",
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
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`),
    "",
  ].join("\n");
}

function readOptional(name) {
  try {
    return readJson(path.join(tracesDir, name));
  } catch {
    return null;
  }
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function publicationBoundary() {
  return {
    raw_browser_routes_published: false,
    private_urls_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    session_streams_published: false,
    private_dumps_published: false,
    private_callable_ids_published: false,
    raw_lane_text_published: false,
  };
}

function claimBoundary() {
  return {
    full_goal_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    deployment_closure: "not_claimed",
    account_mutation: "not_claimed",
    purchase: "not_claimed",
    api_key_creation: "not_claimed",
    private_material_proof: "not_claimed",
    raw_publication_proof: "not_claimed",
    sibling_identity_replacement_or_merge: "not_claimed",
  };
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) parsed.set(argv[index], argv[index + 1]);
  return parsed;
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
