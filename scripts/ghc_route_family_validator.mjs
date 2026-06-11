#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const input = args.get("--input");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!input || !receiptJson || !receiptMd) {
  console.error("Usage: node ghc_route_family_validator.mjs --input <registry-json> --receipt-json <json> --receipt-md <md>");
  process.exit(2);
}

const registry = JSON.parse(readFileSync(input, "utf8"));
const families = Array.isArray(registry.route_families) ? registry.route_families : [];
const policy = registry.chatgpt_sibling_policy || {};
const publication = registry.publication_boundary || registry.phase_rules || {};

const requiredFamilies = [
  "Browser in-app live adapter",
  "Codex app local callable lanes",
  "Codex CLI read-only lanes",
];
const optionalStandbyFamilies = ["Chrome extension live adapter"];

function hasFamily(name) {
  return families.some((family) => family.family === name);
}

function rulesFor(name) {
  const family = families.find((item) => item.family === name);
  return Array.isArray(family?.rules) ? family.rules.join(" ").toLowerCase() : "";
}

const missingFamilies = requiredFamilies.filter((name) => !hasFamily(name));
const missingStandbyFamilies = optionalStandbyFamilies.filter((name) => !hasFamily(name));
const activeChatgpt = Array.isArray(policy.active) ? policy.active : [];
const standbyChatgpt = Array.isArray(policy.standby) ? policy.standby : [];

const checks = [
  {
    name: "browser_family_present",
    passed: hasFamily("Browser in-app live adapter"),
  },
  {
    name: "codex_app_family_present",
    passed: hasFamily("Codex app local callable lanes"),
  },
  {
    name: "codex_cli_family_present",
    passed: hasFamily("Codex CLI read-only lanes"),
  },
  {
    name: "lumen_only_active_chatgpt_lane",
    passed: activeChatgpt.length === 1 && activeChatgpt[0] === "Lumen Vale",
  },
  {
    name: "solas_and_unnamed_standby",
    passed: standbyChatgpt.includes("Solas Veridion") && standbyChatgpt.includes("Unnamed ChatGPT 5.5 Thinking Sibling"),
  },
  {
    name: "browser_rules_status_only",
    passed: /status-only|status only/.test(rulesFor("Browser in-app live adapter")),
  },
  {
    name: "cli_rules_read_only",
    passed: /read-only|read only/.test(rulesFor("Codex CLI read-only lanes")),
  },
  {
    name: "app_rules_existing_lanes",
    passed: /existing/.test(rulesFor("Codex app local callable lanes")),
  },
  {
    name: "raw_publication_forbidden",
    passed:
      publication.raw_lane_text_published === false ||
      publication.raw_lane_text_publication_allowed === false ||
      registry.phase_rules?.raw_lane_text_publication_allowed === false,
  },
];

const openGaps = checks.filter((check) => !check.passed).map((check) => check.name);
const status = openGaps.length === 0 ? "PASS_ROUTE_FAMILY_VALIDATOR" : "OPEN_GAP_ROUTE_FAMILY_VALIDATOR";

const receipt = {
  artifact_type: "ghc_route_family_validator_receipt",
  generated_utc: new Date().toISOString(),
  input,
  status,
  required_families: requiredFamilies,
  optional_standby_families: optionalStandbyFamilies,
  missing_families: missingFamilies,
  missing_standby_families: missingStandbyFamilies,
  checks,
  open_gaps: openGaps,
  mutation_performed: false,
  publication_boundary: {
    raw_lane_text_published: false,
    raw_chatgpt_transcript_published: false,
    raw_browser_error_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    gmut_gate_state: "open",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const lines = [
  "# GHC Route Family Validator",
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${status}\``,
  "",
  "## Checks",
  ...checks.map((check) => `- ${check.name}: \`${check.passed}\``),
  "",
  "## Open Gaps",
  ...(openGaps.length ? openGaps.map((gap) => `- \`${gap}\``) : ["- none"]),
  "",
  "## Boundary",
  "",
  "No raw lane text, raw ChatGPT transcript, raw browser error dump, credentials, screenshots, local absolute paths, or closure claims are published.",
  "",
];

writeFileSync(receiptMd, lines.join("\n"), "utf8");
console.log(JSON.stringify(receipt, null, 2));

if (status !== "PASS_ROUTE_FAMILY_VALIDATOR") {
  process.exit(1);
}
