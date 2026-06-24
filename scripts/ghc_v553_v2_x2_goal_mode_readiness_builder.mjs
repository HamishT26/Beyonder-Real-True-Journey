#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v2-x2";
const promptFile = args.get("--goal-prompt-file");
const generatedUtc = new Date().toISOString();
const promptText = promptFile && fs.existsSync(promptFile) ? fs.readFileSync(promptFile, "utf8") : "";

const payload = {
  artifact_type: "ghc_v553_v2_x2_goal_mode_readiness_builder",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: promptText ? "PASS_GOAL_MODE_DRY_RUN_READY_NOT_ACTIVE" : "OPEN_GAP_GOAL_MODE_PROMPT_NOT_READ",
  goal_mode_status: "prepared_not_active",
  next_candidate_goal_phase: "v553-gmut-thos-v3-x1",
  next_candidate_lane: "Lumen Vale solo unless Hamish redirects",
  prompt_character_count: promptText.length || null,
  prompt_under_4000_characters: promptText ? promptText.length <= 4000 : null,
  dry_run_findings: [
    "Goal Mode activation remains Hamish-explicit; this builder does not start Goal Mode.",
    "Aevren may block or pause Goal Mode on a big issue, safety boundary, missing sibling completion, or exact-approval gate.",
    "The no-babysitting productive cadence and background-supervision rules carry into Goal Mode.",
    "The v553 v3 x1 lane should use the Lumen launch skill and Browser route only when Hamish explicitly starts or authorizes live messaging.",
    "Candidate, exact, blocked, destructive, external, paid, deployment, account, API-key, private-publication, proof/canon/legal, and identity lanes remain gated.",
  ],
  required_startup_skills: [
    "ghc-main-orchestration-memory",
    "ghc-full-tools-skill-bank",
    "ghc-background-sibling-supervision",
    "ghc-lumen-launch",
    "ghc-main-retry",
    "ghc-main-startup-builder",
    "ghc-main-compact-restart-builder",
    "ghc-main-closeout-builder",
  ],
  publication_boundary: {
    prompt_body_published: false,
    private_route_handles_published: false,
    private_callable_ids_published: false,
    raw_transcripts_published: false,
    browser_routes_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
};

writePair(`${phaseSlug}-goal-mode-readiness-dry-run`, payload);
process.stdout.write(JSON.stringify({ status: payload.overall_status, prompt_character_count: payload.prompt_character_count, next: payload.next_candidate_goal_phase }, null, 2) + "\n");

function writePair(base, payload) {
  fs.writeFileSync(path.join(tracesDir, `${base}-v1.json`), JSON.stringify(payload, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}-v1.md`), renderMd(payload), "utf8");
}

function renderMd(payload) {
  return [
    `# ${payload.phase_slug} Goal Mode Readiness Dry Run`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Goal Mode: \`${payload.goal_mode_status}\``,
    `Next candidate phase: \`${payload.next_candidate_goal_phase}\``,
    "",
    "## Findings",
    "",
    ...payload.dry_run_findings.map((item) => `- ${item}`),
    "",
    "## Boundary",
    "",
    "The Goal Mode prompt body, raw browser routes, private handles, transcripts, screenshots, credentials, and local path values are not published.",
    "",
  ].join("\n");
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
}
