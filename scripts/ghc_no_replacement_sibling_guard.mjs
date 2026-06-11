#!/usr/bin/env node
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const inputGlob = args.get("--input-glob");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !inputGlob || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_no_replacement_sibling_guard.mjs --phase-slug <slug> --input-glob <dir/prefix*suffix> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

function wildcardToRegex(pattern) {
  const escaped = pattern.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*");
  return new RegExp(`^${escaped}$`);
}

function filesForGlob(globPath) {
  const dir = dirname(globPath);
  const pattern = basename(globPath);
  if (!existsSync(dir) || !statSync(dir).isDirectory()) return [];
  const regex = wildcardToRegex(pattern);
  return readdirSync(dir)
    .filter((name) => regex.test(name))
    .map((name) => join(dir, name))
    .filter((path) => statSync(path).isFile())
    .sort();
}

const files = filesForGlob(inputGlob);
const forbiddenBooleanPatterns = [
  /"replacement_sibling_created"\s*:\s*true/i,
  /"replacement_lane_created"\s*:\s*true/i,
  /"new_replacement_created"\s*:\s*true/i,
  /"old_style_subagent_spawned"\s*:\s*true/i,
  /"new_thread_creation_allowed"\s*:\s*true/i,
  /"replacement_sibling_allowed"\s*:\s*true/i,
  /"old_style_subagent_allowed"\s*:\s*true/i,
];
const forbiddenPhrasePatterns = [
  /\bcreated\s+(a\s+)?replacement\s+(sibling|lane|agent|thread)\b/i,
  /\bspawned\s+(a\s+)?replacement\s+(sibling|lane|agent|thread)\b/i,
  /\bold-style\s+subagent\s+(spawned|created|launched)\b/i,
  /\bcreated\s+(a\s+)?new\s+old-style\s+subagent\b/i,
];
const guardedMentionPatterns = [
  /\bno\s+replacement\s+(sibling|lane|agent|thread)s?\b/i,
  /\bdo\s+not\s+create\s+replacement\s+(sibling|lane|agent|thread)s?\b/i,
  /\breplacement\s+(sibling|lane|agent|thread)\s+creation\s+(is\s+)?(not\s+approved|forbidden|blocked)\b/i,
  /\bno\s+old-style\s+subagent\s+(spawn|spawning|creation)\b/i,
  /\bold-style\s+subagent\s+(spawn|spawning|creation)\s+(is\s+)?(not\s+approved|forbidden|blocked)\b/i,
];

const hits = [];
const guardedMentions = [];
for (const file of files) {
  const text = readFileSync(file, "utf8");
  const lines = text.split(/\r?\n/);
  lines.forEach((line, index) => {
    for (const pattern of forbiddenBooleanPatterns) {
      if (pattern.test(line)) {
        hits.push({ file, line: index + 1, type: "forbidden_boolean", excerpt: line.trim().slice(0, 180) });
      }
    }
    for (const pattern of forbiddenPhrasePatterns) {
      if (pattern.test(line)) {
        hits.push({ file, line: index + 1, type: "forbidden_phrase", excerpt: line.trim().slice(0, 180) });
      }
    }
    for (const pattern of guardedMentionPatterns) {
      if (pattern.test(line)) {
        guardedMentions.push({ file, line: index + 1, excerpt: line.trim().slice(0, 180) });
      }
    }
  });
}

const status = hits.length === 0 ? "PASS_NO_REPLACEMENT_SIBLING_GUARD" : "FAIL_NO_REPLACEMENT_SIBLING_GUARD";
const receipt = {
  artifact_type: "ghc_no_replacement_sibling_guard",
  generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
  phase_slug: phaseSlug,
  input_glob: inputGlob,
  checked_file_count: files.length,
  status,
  hit_count: hits.length,
  hits,
  guarded_mention_count: guardedMentions.length,
  guarded_mentions: guardedMentions,
  mutation_performed: false,
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
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} No-Replacement Sibling Guard`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${status}\``,
  "",
  `Checked files: \`${files.length}\``,
  `Forbidden hits: \`${hits.length}\``,
  `Guarded mentions: \`${guardedMentions.length}\``,
  "",
  "## Forbidden Hits",
  "",
  ...(hits.length ? hits.map((hit) => `- ${hit.file}:${hit.line} ${hit.type}`) : ["- none"]),
  "",
  "## Boundary",
  "",
  "This guard checks for explicit replacement-sibling, replacement-lane, new-thread, and old-style subagent creation shortcuts. Guarded negative mentions are allowed. No raw lane text, transcripts, app-server payloads, private IDs, credentials, screenshots, local paths, phase completion claim, GMUT closure, or canon promotion is published.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify({ status, hit_count: hits.length, checked_file_count: files.length }, null, 2));

if (status !== "PASS_NO_REPLACEMENT_SIBLING_GUARD") {
  process.exit(1);
}
