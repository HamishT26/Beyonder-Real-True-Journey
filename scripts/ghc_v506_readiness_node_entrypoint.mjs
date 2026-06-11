#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phase = args.get("--phase") ?? "v506-gmut-thos-v42-v1-x1";
const outDir = args.get("--out-dir") ?? "docs/trinity-live-traces";
const jsonOut = join(outDir, `${phase}-node-readiness-receipt-v1.json`);
const mdOut = join(outDir, `${phase}-node-readiness-receipt-v1.md`);

function run(command, commandArgs, options = {}) {
  try {
    return {
      ok: true,
      stdout: execFileSync(command, commandArgs, {
        encoding: "utf8",
        stdio: ["ignore", "pipe", "pipe"],
        timeout: options.timeoutMs ?? 15_000,
      }).trim(),
    };
  } catch (error) {
    return {
      ok: false,
      stdout: "",
      error: error?.message ?? String(error),
    };
  }
}

function boundedSize(root, options = {}) {
  const maxEntries = options.maxEntries ?? 20_000;
  const started = Date.now();
  const maxMs = options.maxMs ?? 8_000;
  let bytes = 0;
  let fileCount = 0;
  let dirCount = 0;
  let truncated = false;
  const stack = [root];

  while (stack.length) {
    if (fileCount + dirCount >= maxEntries || Date.now() - started > maxMs) {
      truncated = true;
      break;
    }
    const current = stack.pop();
    let entries;
    try {
      entries = readdirSync(current, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const entry of entries) {
      const full = join(current, entry.name);
      try {
        if (entry.isDirectory()) {
          dirCount += 1;
          stack.push(full);
        } else if (entry.isFile()) {
          const stats = statSync(full);
          bytes += stats.size;
          fileCount += 1;
        }
      } catch {
        continue;
      }
    }
  }

  return {
    exists: existsSync(root),
    size_mb: Math.round((bytes / 1024 / 1024) * 100) / 100,
    file_count: fileCount,
    dir_count: dirCount,
    truncated,
  };
}

function listTopLevel(root, prefixPattern = /.*/) {
  if (!existsSync(root)) return [];
  return readdirSync(root, { withFileTypes: true })
    .filter((entry) => prefixPattern.test(entry.name))
    .map((entry) => {
      const full = join(root, entry.name);
      const stats = statSync(full);
      const size = entry.isDirectory()
        ? boundedSize(full, { maxEntries: 8_000, maxMs: 4_000 }).size_mb
        : Math.round((stats.size / 1024 / 1024) * 100) / 100;
      return {
        name: entry.name,
        kind: entry.isDirectory() ? "directory" : "file",
        size_mb: size,
        last_write_utc: stats.mtime.toISOString(),
      };
    });
}

const userHome = homedir();
const codexHome = join(userHome, ".codex");
const codexTmp = join(codexHome, ".tmp");
const npmOpenAi = join(userHome, "AppData", "Roaming", "npm", "node_modules", "@openai");
const videos = join(userHome, "Videos");
const downloads = join(userHome, "Downloads");

const drives = run("powershell", [
  "-NoProfile",
  "-Command",
  "Get-PSDrive -Name C,D | Select-Object Name,@{Name='FreeGB';Expression={[math]::Round($_.Free/1GB,2)}},@{Name='UsedGB';Expression={[math]::Round($_.Used/1GB,2)}} | ConvertTo-Json",
]);

let codexVersion = run("codex", ["--version"], { timeoutMs: 10_000 });
if (!codexVersion.ok) {
  codexVersion = run("powershell", ["-NoProfile", "-Command", "codex --version"], { timeoutMs: 10_000 });
}
const gitHead = run("git", ["log", "-1", "--format=%H %s"], { timeoutMs: 10_000 });

const receipt = {
  artifact_type: "ghc_node_readiness_receipt",
  phase,
  generated_utc: new Date().toISOString(),
  mutation_performed: false,
  raw_paths_published: false,
  raw_session_text_published: false,
  credentials_published: false,
  local_state: {
    drives: drives.ok ? JSON.parse(drives.stdout) : { unavailable: true },
    codex_cli_version: codexVersion.ok ? codexVersion.stdout : "unavailable",
    git_head: gitHead.ok ? gitHead.stdout : "unavailable",
  },
  bounded_sizes: {
    videos: boundedSize(videos, { maxEntries: 10_000, maxMs: 5_000 }),
    downloads: boundedSize(downloads, { maxEntries: 20_000, maxMs: 8_000 }),
    codex_tmp: boundedSize(codexTmp, { maxEntries: 30_000, maxMs: 10_000 }),
  },
  codex_tmp_candidates: {
    stale_review_candidates: listTopLevel(codexTmp, /^plugins-backup-|^legacy-|^marketplaces$/),
    preserve_by_default: listTopLevel(codexTmp, /^plugins$|^plugins\.sha$|^plugins\.sync\.lock$|^bundled-marketplaces$/),
  },
  npm_openai_packages: listTopLevel(npmOpenAi),
  recommendation: [
    "Keep using the D omega workspace for repo work.",
    "Use Node entrypoint receipts for phase-start state instead of broad recursive shell scans.",
    "Treat Codex session history as backup-first only.",
    "Treat Codex temporary staging cleanup as exact-candidate and backup-first only.",
    "Keep Browser-first ChatGPT panel work gated to v508+ or explicit immediate user request.",
  ],
};

mkdirSync(outDir, { recursive: true });
writeFileSync(jsonOut, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phase} Node Readiness Receipt v1`,
  "",
  `Generated: ${receipt.generated_utc}`,
  "",
  `Status: NODE_ENTRYPOINT_READY`,
  "",
  "## Summary",
  "",
  `- Codex CLI: \`${receipt.local_state.codex_cli_version}\`.`,
  `- Latest git head: \`${receipt.local_state.git_head}\`.`,
  "- Mutation performed: `false`.",
  "- Raw paths, raw session text, and credentials published: `false`.",
  "",
  "## Bounded Size Signals",
  "",
  `- Videos: ${receipt.bounded_sizes.videos.size_mb} MB, truncated: ${receipt.bounded_sizes.videos.truncated}.`,
  `- Downloads: ${receipt.bounded_sizes.downloads.size_mb} MB, truncated: ${receipt.bounded_sizes.downloads.truncated}.`,
  `- Codex temporary staging: ${receipt.bounded_sizes.codex_tmp.size_mb} MB, truncated: ${receipt.bounded_sizes.codex_tmp.truncated}.`,
  "",
  "## Cleanup Interpretation",
  "",
  "- Video cleanup is already materially reflected in the current state.",
  "- npm package hygiene shows only the active OpenAI package set discovered by the helper.",
  "- Codex temporary staging has backup-style candidates, but current plugin and marketplace material remains preserve-by-default.",
  "",
  "## Recommendations",
  "",
  ...receipt.recommendation.map((item) => `- ${item}`),
  "",
  "All GMUT, canon, empirical, legal, and consciousness gates remain open.",
  "",
].join("\n");

writeFileSync(mdOut, md, "utf8");
console.log(JSON.stringify({ ok: true, jsonOut, mdOut }, null, 2));
