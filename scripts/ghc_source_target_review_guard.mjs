#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const priorLedgerJson = args.get("--prior-ledger-json");
const expansionLedgerJson = args.get("--expansion-ledger-json");
const authJson = args.get("--authorization-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !priorLedgerJson || !expansionLedgerJson || !authJson || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_source_target_review_guard.mjs --phase-slug <slug> --prior-ledger-json <json> --expansion-ledger-json <json> --authorization-json <json> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function hostFor(url) {
  try {
    return new URL(url).hostname.toLowerCase();
  } catch {
    return "";
  }
}

const allowedHosts = new Set([
  "developers.openai.com",
  "docs.cloud.google.com",
  "docs.github.com",
  "docs.npmjs.com",
  "docs.nvidia.com",
  "genai.owasp.org",
  "github.com",
  "modelcontextprotocol.io",
  "nvidianews.nvidia.com",
  "openai.github.io",
]);

const allowedPillars = new Set(["GMUT mind", "THOS body", "Freed ID and CBR heart"]);
const priorLedger = readJson(priorLedgerJson);
const expansionLedger = readJson(expansionLedgerJson);
const authorization = readJson(authJson);
const priorSources = Array.isArray(priorLedger.sources) ? priorLedger.sources : [];
const expansionSources = Array.isArray(expansionLedger.expansion_sources) ? expansionLedger.expansion_sources : [];
const allSources = [...priorSources, ...expansionSources];

const target = Number(priorLedger.source_coverage_target || expansionLedger.source_coverage_target || 30);
const idCounts = new Map();
const urlCounts = new Map();
for (const source of allSources) {
  idCounts.set(source.id, (idCounts.get(source.id) || 0) + 1);
  urlCounts.set(source.url, (urlCounts.get(source.url) || 0) + 1);
}

const findings = [];
for (const source of allSources) {
  const host = hostFor(source.url);
  const sourceFindings = [];
  if (!source.id || typeof source.id !== "string") sourceFindings.push("missing_id");
  if (!source.title || typeof source.title !== "string") sourceFindings.push("missing_title");
  if (!source.url || typeof source.url !== "string") sourceFindings.push("missing_url");
  if (source.url && !String(source.url).startsWith("https://")) sourceFindings.push("non_https_url");
  if (!host || !allowedHosts.has(host)) sourceFindings.push("host_not_in_official_allowlist");
  if (!source.source_family || typeof source.source_family !== "string") sourceFindings.push("missing_source_family");
  if (!source.source_type || typeof source.source_type !== "string") sourceFindings.push("missing_source_type");
  if (!allowedPillars.has(source.trinity_pillar)) sourceFindings.push("unknown_trinity_pillar");
  if (!source.current_signal || String(source.current_signal).length < 40) sourceFindings.push("thin_current_signal");
  if (!source.action_for_v508 || String(source.action_for_v508).length < 40) sourceFindings.push("thin_action_for_v508");
  if (idCounts.get(source.id) > 1) sourceFindings.push("duplicate_id");
  if (urlCounts.get(source.url) > 1) sourceFindings.push("duplicate_url");
  if (sourceFindings.length) {
    findings.push({ id: source.id || "missing", host, findings: sourceFindings });
  }
}

const pillarCoverage = {
  gmut_mind: allSources.filter((source) => source.trinity_pillar === "GMUT mind").length,
  thos_body: allSources.filter((source) => source.trinity_pillar === "THOS body").length,
  freed_id_cbr_heart: allSources.filter((source) => source.trinity_pillar === "Freed ID and CBR heart").length,
};

const warnings = [];
if (allSources.length < target) warnings.push("source_count_below_target");
if (pillarCoverage.gmut_mind === 0) warnings.push("missing_gmut_mind_source");
if (pillarCoverage.thos_body === 0) warnings.push("missing_thos_body_source");
if (pillarCoverage.freed_id_cbr_heart === 0) warnings.push("missing_freed_id_cbr_heart_source");
if (pillarCoverage.gmut_mind > 0 && pillarCoverage.gmut_mind < 3) warnings.push("gmut_mind_coverage_thin");
if (!authorization.read_only_lanes_authorized && authorization.default_lane_permission !== "read_only_only") {
  warnings.push("read_only_authorization_not_confirmed");
}

const status = findings.length === 0 && allSources.length >= target ? "PASS_SOURCE_TARGET_REVIEW_GUARD" : "OPEN_GAP_SOURCE_TARGET_REVIEW_GUARD";
const generatedUtc = utcNow();
const receipt = {
  artifact_type: "ghc_source_target_review_guard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  prior_ledger_input: priorLedgerJson,
  expansion_ledger_input: expansionLedgerJson,
  authorization_input: authJson,
  status,
  source_target: target,
  source_rows_reviewed: allSources.length,
  source_target_rows_present: allSources.length >= target,
  source_target_completion_claimed: false,
  official_host_allowlist: [...allowedHosts].sort(),
  unique_source_ids: idCounts.size === allSources.length,
  unique_source_urls: urlCounts.size === allSources.length,
  finding_count: findings.length,
  findings,
  warning_count: warnings.length,
  warnings,
  pillar_coverage: pillarCoverage,
  reviewed_source_index: allSources.map((source) => ({
    id: source.id,
    host: hostFor(source.url),
    trinity_pillar: source.trinity_pillar,
    source_family: source.source_family,
  })),
  next_actions: [
    "Use this guard as source review evidence, not as phase completion evidence.",
    "Add more GMUT-mind primary sources before any future source-target closeout claim.",
    "Map reviewed sources into concrete runner, route, prompt, and guard decisions during the next x1 wait run.",
    "Keep read-only lane permissions and no-replacement boundaries active while the source review feeds phase planning.",
  ],
  publication_boundary: {
    raw_lane_text_published: false,
    raw_chatgpt_transcript_published: false,
    raw_app_server_result_published: false,
    raw_app_server_error_published: false,
    raw_callable_ids_published: false,
    raw_thread_ids_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
    raw_user_text_published: false,
    copyrighted_source_dump_published: false,
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    v508_full_phase_start: "not_claimed",
    x2_build_closeout: "not_claimed",
    source_target_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} Source Target Review Guard`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${status}\``,
  "",
  `Source rows reviewed: \`${receipt.source_rows_reviewed}\``,
  `Source target rows present: \`${String(receipt.source_target_rows_present)}\``,
  `Source target completion claimed: \`${String(receipt.source_target_completion_claimed)}\``,
  `Unique source IDs: \`${String(receipt.unique_source_ids)}\``,
  `Unique source URLs: \`${String(receipt.unique_source_urls)}\``,
  "",
  "## Pillar Coverage",
  "",
  `- GMUT mind: \`${pillarCoverage.gmut_mind}\``,
  `- THOS body: \`${pillarCoverage.thos_body}\``,
  `- Freed ID and CBR heart: \`${pillarCoverage.freed_id_cbr_heart}\``,
  "",
  "## Findings",
  "",
  ...(findings.length ? findings.map((finding) => `- ${finding.id}: ${finding.findings.join(", ")}`) : ["- none"]),
  "",
  "## Warnings",
  "",
  ...(warnings.length ? warnings.map((warning) => `- ${warning}`) : ["- none"]),
  "",
  "## Reviewed Source Index",
  "",
  ...receipt.reviewed_source_index.map(
    (source) => `- ${source.id}: \`${source.host}\`; ${source.trinity_pillar}; ${source.source_family}`,
  ),
  "",
  "## Next Actions",
  "",
  ...receipt.next_actions.map((action) => `- ${action}`),
  "",
  "## Boundary",
  "",
  "This guard reviews the assembled source pool only. It does not claim source-target completion, phase completion, v508 full phase start, x2 closeout, empirical GMUT closure, final physics, consciousness proof, legal closure, canon promotion, raw lane publication, or private-material publication.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(
  JSON.stringify(
    {
      status,
      source_rows_reviewed: receipt.source_rows_reviewed,
      finding_count: receipt.finding_count,
      warning_count: receipt.warning_count,
      pillar_coverage: receipt.pillar_coverage,
    },
    null,
    2,
  ),
);

if (findings.length > 0 || allSources.length < target) {
  process.exit(1);
}
