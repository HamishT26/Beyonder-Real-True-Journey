#!/usr/bin/env node
import { promises as fs } from "node:fs";
import path from "node:path";

function arg(name, fallback = undefined) {
  const index = process.argv.indexOf(`--${name}`);
  return index >= 0 && index + 1 < process.argv.length ? process.argv[index + 1] : fallback;
}

function count(text, pattern) {
  const matches = text.match(pattern);
  return matches ? matches.length : 0;
}

function isoNzFrom(date) {
  const parts = new Intl.DateTimeFormat("sv-SE", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false
  }).formatToParts(date).reduce((acc, part) => {
    acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}

const root = arg("root", process.cwd());
const phaseSlug = arg("phase-slug", "v557-gmut-thos-v8-x1");
const dropbox = arg("dropbox", ".ghc-private/v557-gmut-thos-v8-x1-sibling-response-dropbox");
const outDir = arg("out-dir", "docs/trinity-live-traces");
const artifactId = arg("artifact-id", `${phaseSlug}-recomposed-private-dropbox-sanitized-index-v1`);

const dropboxAbs = path.resolve(root, dropbox);
const outAbs = path.resolve(root, outDir);
const now = new Date();

let entries = [];
try {
  const names = await fs.readdir(dropboxAbs);
  for (const name of names.sort()) {
    if (!/\.md$|\.json$|\.txt$/i.test(name)) continue;
    const fileAbs = path.join(dropboxAbs, name);
    const stat = await fs.stat(fileAbs);
    if (!stat.isFile()) continue;
    const text = await fs.readFile(fileAbs, "utf8");
    entries.push({
      file: name,
      bytes: stat.size,
      lines: text.split(/\r?\n/).length,
      safe_mentions: count(text, /\bsafe\b/gi),
      candidate_mentions: count(text, /\bcandidate\b/gi),
      exact_mentions: count(text, /\bexact\b|exact-approval/gi),
      blocked_mentions: count(text, /\bblocked\b|\bblocker\b/gi),
      skill_mentions: count(text, /\bskill\b|\bskills\b/gi),
      runner_mentions: count(text, /\brunner\b|\brunners\b/gi),
      cleanup_mentions: count(text, /\bcleanup\b|\bclean-up\b|\brefine\b|\bfix\b/gi)
    });
  }
} catch (error) {
  entries = [];
}

const totals = entries.reduce((acc, entry) => {
  for (const key of [
    "bytes",
    "lines",
    "safe_mentions",
    "candidate_mentions",
    "exact_mentions",
    "blocked_mentions",
    "skill_mentions",
    "runner_mentions",
    "cleanup_mentions"
  ]) {
    acc[key] = (acc[key] || 0) + entry[key];
  }
  return acc;
}, { files: entries.length });

const payload = {
  schema: "ghc.private_dropbox_sanitized_index.v1",
  artifact_id: artifactId,
  phase_slug: phaseSlug,
  recorded_at_utc: now.toISOString(),
  recorded_at_nz: isoNzFrom(now),
  status: entries.length > 0 ? "SANITIZED_PRIVATE_DROPBOX_INDEX_READY" : "SANITIZED_PRIVATE_DROPBOX_EMPTY_OR_UNAVAILABLE",
  privacy: {
    raw_private_text_included: false,
    local_absolute_paths_included: false,
    private_ids_included: false,
    raw_routes_included: false,
    raw_transcripts_included: false
  },
  dropbox_repo_relative: dropbox,
  entries,
  totals
};

await fs.mkdir(outAbs, { recursive: true });
await fs.writeFile(path.join(outAbs, `${artifactId}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} Recomputed Private Dropbox Sanitized Index`,
  "",
  `Status: \`${payload.status}\``,
  "",
  `Recorded NZ: \`${payload.recorded_at_nz}\``,
  "",
  "This index records file-level counts from the private response dropbox without publishing raw private text, local absolute paths, private IDs, raw routes, or raw transcripts.",
  "",
  `Files indexed: ${entries.length}`,
  "",
  "| File | Bytes | Lines | Safe | Candidate | Exact | Blocked | Skills | Runners | Cleanup |",
  "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
  ...entries.map((entry) => `| ${entry.file} | ${entry.bytes} | ${entry.lines} | ${entry.safe_mentions} | ${entry.candidate_mentions} | ${entry.exact_mentions} | ${entry.blocked_mentions} | ${entry.skill_mentions} | ${entry.runner_mentions} | ${entry.cleanup_mentions} |`),
  "",
  "Totals:",
  "",
  `- Files: ${totals.files || 0}`,
  `- Bytes: ${totals.bytes || 0}`,
  `- Lines: ${totals.lines || 0}`,
  `- Safe mentions: ${totals.safe_mentions || 0}`,
  `- Candidate mentions: ${totals.candidate_mentions || 0}`,
  `- Exact mentions: ${totals.exact_mentions || 0}`,
  `- Blocked mentions: ${totals.blocked_mentions || 0}`,
  `- Skill mentions: ${totals.skill_mentions || 0}`,
  `- Runner mentions: ${totals.runner_mentions || 0}`,
  `- Cleanup mentions: ${totals.cleanup_mentions || 0}`,
  ""
].join("\n");

await fs.writeFile(path.join(outAbs, `${artifactId}.md`), md, "utf8");
console.log(JSON.stringify({ status: payload.status, artifact_id: artifactId, files: entries.length }, null, 2));
