#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const promptFile = args.get("--prompt-file");
const maxChars = Number(args.get("--max-chars") || 4000);
const receiptPrefix = args.get("--receipt-prefix") || `${phaseSlug}-goal-mode-prompt-fit-validator`;

if (!phaseSlug || !promptFile) {
  console.error("Usage: node scripts/ghc_goal_mode_prompt_fit_validator.mjs --phase-slug <slug> --prompt-file <path> [--max-chars 4000]");
  process.exit(2);
}

const text = fs.readFileSync(promptFile, "utf8");
const findings = [];
const checks = [
  ["drive_path", /\b[A-Za-z]:\\/],
  ["chatgpt_conversation_url", /https?:\/\/chatgpt\.com\/c\//i],
  ["openai_secret_key", /\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b/],
  ["private_key_block", /BEGIN [A-Z ]*PRIVATE KEY/],
  ["raw_app_state_dump", /raw app state dump/i],
  ["session_stream_dump", /session stream dump/i],
];
for (const [label, pattern] of checks) {
  if (pattern.test(text)) findings.push(label);
}

const receipt = {
  artifact_type: "ghc_goal_mode_prompt_fit_validator",
  generated_utc: new Date().toISOString(),
  phase_slug: phaseSlug,
  overall_status: text.length <= maxChars && findings.length === 0 ? "PASS_GOAL_MODE_PROMPT_FIT_VALIDATOR" : "OPEN_GAP_GOAL_MODE_PROMPT_FIT_VALIDATOR",
  max_chars: maxChars,
  char_count: text.length,
  line_count: text.split(/\r?\n/).length,
  within_limit: text.length <= maxChars,
  private_pattern_findings: findings,
  prompt_body_published: false,
  prompt_path_published: false,
  publication_boundary: {
    prompt_body_published: false,
    prompt_path_published: false,
    raw_browser_routes_published: false,
    local_absolute_paths_published: false,
    credentials_published: false,
  },
};

writePair(receiptPrefix, receipt);
console.log(JSON.stringify({ status: receipt.overall_status, char_count: receipt.char_count, max_chars: maxChars, findings: findings.length }, null, 2));
process.exit(receipt.overall_status.startsWith("PASS") ? 0 : 1);

function writePair(prefix, payload) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.md`), renderMd(payload), "utf8");
}

function renderMd(payload) {
  return [
    `# ${payload.phase_slug} Goal Mode Prompt Fit Validator`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Character count: \`${payload.char_count}\` / \`${payload.max_chars}\``,
    `Within limit: \`${payload.within_limit}\``,
    `Private pattern findings: \`${payload.private_pattern_findings.length}\``,
    "",
    "Prompt body and local prompt path are not published.",
    "",
  ].join("\n");
}
