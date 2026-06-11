#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const completionJson = args.get("--completion-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !completionJson || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_marker_source_validator.mjs --phase-slug <slug> --completion-json <json> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

if (!existsSync(completionJson)) {
  throw new Error(`completion json not found: ${completionJson}`);
}

const completion = JSON.parse(readFileSync(completionJson, "utf8"));
const evidence = completion.verified_evidence || {};
const marker = evidence.required_marker || completion.required_marker || "unknown marker";
const assistantMarkerVisible = evidence.assistant_marker_visible === true;
const userPromptMarkerVisible = evidence.user_prompt_marker_visible === true;
const rawPublished =
  completion.publication_boundary?.raw_chatgpt_transcript_published === true ||
  completion.publication_boundary?.raw_browser_error_published === true ||
  completion.publication_boundary?.screenshots_published === true ||
  completion.publication_boundary?.credentials_published === true ||
  completion.publication_boundary?.local_absolute_paths_published === true;

const status = assistantMarkerVisible && !rawPublished
  ? "PASS_ASSISTANT_MARKER_SOURCE_VERIFIED"
  : "FAIL_ASSISTANT_MARKER_SOURCE_UNVERIFIED";

const receipt = {
  artifact_type: "ghc_marker_source_validator",
  generated_utc: new Date().toISOString(),
  phase_slug: phaseSlug,
  status,
  completion_json: completionJson,
  required_marker: marker,
  marker_source: {
    assistant_marker_visible: assistantMarkerVisible,
    user_prompt_marker_visible: userPromptMarkerVisible,
    user_prompt_marker_alone_unlocks_phase: false,
    assistant_marker_required_for_phase_advance: true,
  },
  publication_boundary: {
    raw_response_published: evidence.raw_response_published === true,
    raw_private_material_published: rawPublished,
  },
  route_rules: {
    duration_is_completion_proof: false,
    prompt_echo_is_completion_proof: false,
    assistant_marker_is_completion_proof: assistantMarkerVisible,
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  "# GHC Marker Source Validator",
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${status}\``,
  "",
  `Phase: \`${phaseSlug}\``,
  `Required marker: \`${marker}\``,
  "",
  "## Source Decision",
  "",
  `- Assistant marker visible: \`${assistantMarkerVisible}\``,
  `- User prompt marker visible: \`${userPromptMarkerVisible}\``,
  "- User prompt marker alone unlocks phase: `false`",
  "- Assistant marker required for phase advance: `true`",
  "- Duration is completion proof: `false`",
  "- Prompt echo is completion proof: `false`",
  "",
  "## Boundary",
  "",
  "This validator publishes no raw ChatGPT transcript, raw browser errors, screenshots, credentials, local absolute paths, or closure claims.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify(receipt, null, 2));

if (status !== "PASS_ASSISTANT_MARKER_SOURCE_VERIFIED") {
  process.exit(1);
}
