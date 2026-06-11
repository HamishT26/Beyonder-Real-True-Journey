#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const input = args.get("--input");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");
if (!input || !receiptJson || !receiptMd) {
  console.error("Usage: node ghc_route_state_validator.mjs --input <json> --receipt-json <json> --receipt-md <md>");
  process.exit(2);
}

const allowedStates = [
  "prepared",
  "sent",
  "generating",
  "complete",
  "blocker",
  "synthesized",
];
const requiredTransitions = [
  ["prepared", "sent"],
  ["sent", "generating"],
  ["generating", "complete"],
  ["generating", "blocker"],
  ["complete", "synthesized"],
  ["blocker", "synthesized"],
];

const manifest = JSON.parse(readFileSync(input, "utf8"));
const states = manifest?.route_state_contract?.states ?? [];
const transitions = manifest?.route_state_contract?.transitions ?? [];
const forbiddenFields = [
  "raw_lane_text",
  "raw_transcript_body",
  "raw_response_body",
  "credential_material",
  "browser_hidden_state",
  "screenshot_payload",
  "session_stream_payload",
];
const flatEntries = [];
function flatten(value, prefix = "") {
  if (Array.isArray(value)) {
    value.forEach((item, index) => flatten(item, `${prefix}[${index}]`));
    return;
  }
  if (value && typeof value === "object") {
    Object.entries(value).forEach(([key, item]) => flatten(item, prefix ? `${prefix}.${key}` : key));
    return;
  }
  flatEntries.push({ key: prefix, value });
}
flatten(manifest);
const forbidden = flatEntries.filter((entry) => {
  const key = entry.key.toLowerCase();
  if (forbiddenFields.includes(key.split(".").pop())) return true;
  return typeof entry.value === "boolean" && entry.value === true && /raw|credential|screenshot|session|hidden_browser/.test(key);
});

const missingStates = allowedStates.filter((state) => !states.includes(state));
const transitionKeys = new Set(transitions.map((transition) => `${transition.from}->${transition.to}`));
const missingTransitions = requiredTransitions
  .map(([from, to]) => ({ from, to, key: `${from}->${to}` }))
  .filter((transition) => !transitionKeys.has(transition.key));

const status = missingStates.length === 0 && missingTransitions.length === 0 && forbidden.length === 0
  ? "PASS_ROUTE_STATE_VALIDATOR"
  : "FAIL_ROUTE_STATE_VALIDATOR";

const receipt = {
  artifact_type: "ghc_route_state_validator_receipt",
  generated_utc: new Date().toISOString(),
  input,
  status,
  missing_states: missingStates,
  missing_transitions: missingTransitions,
  forbidden_publication_hits: forbidden,
  mutation_performed: false,
  raw_lane_text_published: false,
  credentials_published: false,
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
const md = [
  `# Route State Validator Receipt`,
  "",
  `Generated: ${receipt.generated_utc}`,
  "",
  `Status: ${status}`,
  "",
  `- Input: ${input}`,
  `- Missing states: ${missingStates.length}`,
  `- Missing transitions: ${missingTransitions.length}`,
  `- Forbidden publication hits: ${forbidden.length}`,
  "",
  "Mutation performed: `false`.",
  "Raw lane text and credentials published: `false`.",
  "",
].join("\n");
writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify(receipt, null, 2));

if (status !== "PASS_ROUTE_STATE_VALIDATOR") {
  process.exit(1);
}
