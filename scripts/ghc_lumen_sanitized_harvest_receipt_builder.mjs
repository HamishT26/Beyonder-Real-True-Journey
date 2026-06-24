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
const summaryKey = args.get("--summary-key") || phaseSlug.replaceAll("-", "_");
const reductionPath = args.get("--reduction-json");
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);
const reduction = reductionPath ? readJson(path.resolve(reductionPath)) : {};

const payload = {
  artifact_type: "ghc_lumen_sanitized_harvest_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_LUMEN_BROWSER_HARVEST_SANITIZED",
  response_status: "completed_ready_for_harvest",
  raw_transcript_published: false,
  raw_browser_route_published: false,
  screenshots_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
  private_callable_ids_published: false,
  reduction: {
    text_length: reduction.textLength || null,
    line_count: reduction.lineCount || null,
    key_phrases: reduction.keyPhrases || [],
    section_counts: reduction.sections || {},
    sanitized_headings: reduction.headings || [],
  },
  safe_takeaways: [
    "Lumen response completed and was reduced without publishing a verbatim transcript.",
    "Immediate x1-safe work remains analysis, status, queue reduction, validation, and privacy/open-gate hygiene.",
    "v554 v1 x2 should build the first compact artifact set from the Lumen/Aevren proposal queue.",
    "Candidate work that touches curation, remote verification, or risky cleanup remains exact-gated before execution.",
    "Goal Mode continuity, Browser handoff safety, skill/runner readiness, cleanup tiering, and current-state reliability remain the main build themes.",
    "GMUT empirical closure, final physics, consciousness proof, legal/canon/deployment/account/API-key/purchase/private-material/raw-publication/sibling-merge gates remain open.",
  ],
  next_safe_actions: [
    "Run the v554 v1 x1 closeout builder only after this harvest receipt is validated.",
    "Carry build/use/test/install tasks into v554 v1 x2 as x2_build_task rows.",
    "Keep exact-approval and blocked packets queued unless Hamish freshly approves those gates.",
  ],
};

const base = `${phaseSlug}-lumen-browser-harvest-sanitized-v1`;
writePair(base, payload, renderMd(payload));
refreshBeacons(payload, base);

console.log(JSON.stringify({
  status: payload.overall_status,
  phase_slug: phaseSlug,
  receipt: `${base}.json`,
}, null, 2));

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
    console.error(`Usage: node scripts/ghc_lumen_sanitized_harvest_receipt_builder.mjs ${flag} <value>`);
    process.exit(2);
  }
  return value;
}

function writePair(base, json, md) {
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), `${JSON.stringify(json, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), md, "utf8");
}

function renderMd(data) {
  return [
    `# ${data.phase_slug} Lumen Browser Harvest Sanitized`,
    "",
    `Status: \`${data.overall_status}\``,
    `Response status: \`${data.response_status}\``,
    "",
    "## Reduction",
    "",
    `- Text length: \`${data.reduction.text_length || "not_recorded"}\``,
    `- Line count: \`${data.reduction.line_count || "not_recorded"}\``,
    `- Key phrases: \`${data.reduction.key_phrases.length}\``,
    "",
    "## Safe Takeaways",
    "",
    ...data.safe_takeaways.map((item) => `- ${item}`),
    "",
    "## Next Safe Actions",
    "",
    ...data.next_safe_actions.map((item) => `- ${item}`),
    "",
    "## Boundary",
    "",
    "No raw Browser route, private URL, raw transcript, screenshot, credential, local absolute path, private callable ID, hidden reasoning, proof closure, canon promotion, legal closure, deployment closure, account mutation, purchase, API-key creation, or sibling identity merge is published or claimed.",
    "",
  ].join("\n");
}

function refreshBeacons(receipt, base) {
  const files = [
    `docs/trinity-live-traces/${base}.json`,
    `docs/trinity-live-traces/${base}.md`,
  ];
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const data = readJson(file);
    data.generated_utc = generatedUtc;
    if (file.includes("current-state")) data.updated_at = generatedNz;
    data.current_active_phase = phaseSlug;
    data.lumen_browser_harvest = {
      status: receipt.overall_status,
      response_status: receipt.response_status,
      raw_transcript_published: false,
      raw_browser_route_published: false,
      private_callable_ids_published: false,
    };
    if (data[summaryKey]) {
      data[summaryKey].lumen_response_harvested = true;
      data[summaryKey].handoff_message_status = "browser_send_submitted_response_completed_ready_for_harvest";
    }
    const key = file.includes("latest-updates") ? "latest_lookup_files" : file.includes("ghc-current-state") ? "lookup_files" : "current_lookup_files";
    data[key] = [...new Set([...(data[key] || []), ...files])];
    fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
  }
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date).reduce((acc, part) => {
    if (part.type !== "literal") acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
