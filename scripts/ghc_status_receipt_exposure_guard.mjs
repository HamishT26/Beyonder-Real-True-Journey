#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 1) {
  const key = process.argv[index];
  if (!key.startsWith("--")) continue;
  const value = process.argv[index + 1];
  if (value && !value.startsWith("--")) {
    args.set(key, value);
    index += 1;
  } else {
    args.set(key, "true");
  }
}

function requireArg(name) {
  const value = args.get(name);
  if (!value) {
    console.error(`Missing required argument: ${name}`);
    process.exit(2);
  }
  return value;
}

const phaseSlug = requireArg("--phase-slug");
const files = requireArg("--files")
  .split(",")
  .map((file) => file.trim())
  .filter(Boolean);
const guardJson = requireArg("--guard-json");
const guardMd = requireArg("--guard-md");

const patterns = [
  ["windows_absolute_path", /[A-Z]:\\(?:Users\\hamis|GHC-Archives|Windows|ProgramData|Program Files)/iu],
  ["chatgpt_conversation_url", /https:\/\/chatgpt\.com\/c\/[A-Za-z0-9:_-]+/iu],
  ["openai_api_key", /\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b/u],
  ["named_api_key_assignment", /\b(?:OPENAI_API_KEY|GITHUB_TOKEN|GOOGLE_API_KEY|ANTHROPIC_API_KEY)\b\s*[:=]/iu],
  ["password_assignment", /\bpassword\b\s*[:=]\s*\S+/iu],
  ["session_jsonl_reference", /\bsessions?[\\/].+\.jsonl\b/iu],
  ["screenshot_file_reference", /\bScreenshot(?:[_\s-]?\d{4}|\s)/iu],
  ["conversation_turn_id", /\bconversation-turn-\d+\b/iu],
  ["raw_callable_uuid", /\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/iu],
];

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, lines) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${lines.join("\n")}\n`, "utf8");
}

const findings = [];
const missingFiles = [];

for (const file of files) {
  if (!existsSync(file)) {
    missingFiles.push(file);
    continue;
  }
  const text = readFileSync(file, "utf8");
  for (const [rule, pattern] of patterns) {
    if (pattern.test(text)) {
      findings.push({ file, rule });
    }
  }
}

const generatedUtc = utcNow();
const payload = {
  artifact_type: "status_receipt_exposure_guard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: findings.length === 0 && missingFiles.length === 0 ? "PASS_EXPOSURE_GUARD" : "FAIL_EXPOSURE_GUARD",
  files_scanned: files.length - missingFiles.length,
  files_requested: files.length,
  missing_files: missingFiles,
  findings_count: findings.length,
  findings,
  claim_boundary: {
    matched_text_published: false,
    raw_lane_text_published: false,
    raw_transport_published: false,
    raw_chatgpt_transcript_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
};

writeJson(guardJson, payload);
const findingLines =
  findings.length === 0
    ? ["- No publish-blocking exposure patterns found."]
    : findings.map((finding) => `- ${finding.file}: ${finding.rule}`);
writeMd(guardMd, [
  `# ${phaseSlug} Status Receipt Exposure Guard`,
  "",
  `- generated_utc: \`${generatedUtc}\``,
  `- overall_status: \`${payload.overall_status}\``,
  `- files_requested: \`${payload.files_requested}\``,
  `- files_scanned: \`${payload.files_scanned}\``,
  `- missing_files_count: \`${missingFiles.length}\``,
  `- findings_count: \`${findings.length}\``,
  "",
  "## Findings",
  ...findingLines,
  "",
  "This guard records filenames, rule identifiers, and counts only. It does not publish matched text.",
]);

console.log(
  JSON.stringify(
    {
      overall_status: payload.overall_status,
      files_scanned: payload.files_scanned,
      missing_files_count: missingFiles.length,
      findings_count: findings.length,
    },
    null,
    2,
  ),
);
