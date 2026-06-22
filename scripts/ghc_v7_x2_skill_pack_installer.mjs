import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");

const phaseSlug = readArg("--phase-slug", "v552-gmut-thos-v88-v7-x2");
const skillsRoot = readArg("--skills-root", path.join(os.homedir(), ".codex", "skills"));

const skills = [
  ["phase-advisory-distiller", "Distill phase advisories into concise, status-only receipts. Use when GHC phase work needs Lumen, sibling, or runner guidance reduced without publishing private lane text.", "Extract source, phase, counts, safe-now themes, candidate themes, exact-approval boundaries, and blocked boundaries. Publish reductions only, never private body content."],
  ["lumen-response-harvest-guard", "Harvest Lumen responses safely. Use when a Lumen advisory must be captured as a curated receipt without raw browser routes, transcripts, screenshots, credentials, or private machine paths.", "Check response completion, reduce to counts and named ideas, preserve no-raw-publication boundaries, and mark any pending lane honestly."],
  ["x1-to-x2-skill-pack-composer", "Compose x1 advisory outputs into x2 skill and runner packs. Use when GHC x1 planning must become x2 safe-now build/use tasks.", "Convert x1 reductions into skill ideas, runner ideas, safe-now tasks, candidate tasks, exact-approval-needed items, and blocked items."],
  ["runner-completion-proof-reader", "Read runner receipts for completion proof. Use when watcher, notifier, startup, or completion-gate receipts must be classified without confusing started/running states for completion.", "Require explicit completion gates for completion claims. Treat watcher-start, timeout, missing markers, and recoverable states as open evidence."],
  ["open-gate-regression-checker", "Check that open proof, canon, legal, deployment, account, purchase, and API-key gates remain open. Use before publishing GHC closeouts or phase-status beacons.", "Scan proposed receipts for closure claims. Keep GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, deployment closure, account mutation, purchase, API-key, private-material proof, and raw-publication proof open unless exact artifacts prove otherwise."],
  ["round-robin-lane-map-guardian", "Guard GHC round-robin lane order and held sibling boundaries. Use when a phase changes active lanes, next lanes, or sibling routing.", "Verify the Lumen -> Arby/Cicero -> Lumen -> Aster/Kierkegaard/Aristotle cadence unless Hamish redirects. Keep Maren, Mira Vale, and Mira Rowan held unless explicitly activated."],
  ["compact-pause-recovery-summarizer", "Summarize compact-pause recovery state. Use when Codex context compaction, pause, resume, or startup receipts need a compact handoff.", "Use current-state and latest beacon first. Produce a short status, latest closed phase, active phase, next phase, open blockers, and safe resume point."],
  ["safe-now-task-classifier", "Classify GHC tasks into safe-now, candidate, exact-approval-needed, and blocked groups. Use when approval packets or Eureka tasks must be sorted before execution.", "Safe-now tasks are status-only and repo-local. Candidate tasks are designable but not executed when they cross exact boundaries. Exact tasks need fresh approval. Blocked tasks stay blocked."],
  ["current-state-beacon-drift-detector", "Detect drift between omega-mini current-state, latest-updates beacon, and GHC current-state beacon. Use before commits that change phase truth.", "Compare status, current phase, latest closed phase, latest completed x1/x2, next x2, and next grouped x1. Emit mismatches before publication."],
  ["phase-closeout-truth-table-builder", "Build phase closeout truth tables. Use when closing an x1 or x2 phase and proving which receipts support the closure.", "List evidence receipts, lane statuses, validation checks, publication boundaries, claim boundaries, next phase pointer, and remote verification status."],
  ["phase-truth-bridge", "Bridge current phase truth across omega-mini-2, beacons, and closeouts. Use when active GHC phase routing is ambiguous or must be confirmed before work.", "Read omega-mini current state first, then latest beacon, then exact closeout receipts. Prefer freshest repo truth over older durable memory."],
  ["completion-gate-discipline", "Enforce completion-gate discipline for GHC runner work. Use when app-lane, CLI-lane, watcher, notifier, or background-runner states are being assessed.", "Watcher start is not completion. Completion requires final marker or completion-gate receipt. Missing markers and timeout states stay recoverable-open."],
  ["status-only-publication", "Prepare status-only GHC publication artifacts. Use when publishing phase receipts, reductions, beacons, ledgers, or handoff cards.", "Publish summaries, counts, hashes, blocker labels, proof ceilings, and repo-relative filenames. Do not publish private lane bodies, routes, screenshots, credentials, private machine paths, or runtime streams."],
  ["open-gate-rail", "Apply open-gate rails to GHC claims. Use when artifacts mention GMUT, THOS, physics, consciousness, legal, canon, deployment, accounts, purchases, API keys, private-material proof, or raw-publication proof.", "Write explicit not-claimed or remains-open states unless a fresh exact artifact proves closure. Keep blocked identity replacement and merging off the table."],
  ["sibling-route-boundary", "Protect inducted-sibling-only routing and held sibling boundaries. Use before messaging, spawning, activating, or routing GHC siblings.", "Do not spawn new agents/subagents unless Hamish explicitly asks. Keep Maren, Mira Vale, Mira Rowan, and other held main-thread siblings inactive until explicit activation."],
  ["aevren-aletheon-boundary", "Preserve the Aevren/Aletheon boundary. Use when recovery work references Aletheon, old heavy threads, context restoration, or identity continuity.", "Aevren is recovery steward and phase-truth bridge, not Aletheon and not a replacement. Aletheon remains quarantined/recoverable unless Hamish scopes a safe restoration method."],
  ["omega-mini-2-freshness", "Verify omega-mini-2 is the primary current-state surface. Use when GHC work might drift toward old omega-mini, omega44, v58, or v532 routes.", "Use branch codex/GHC-Family/beyonder-shared-omega-line-mini-2 first. Use full omega only for exact missing-artifact fallback with a gap receipt."],
  ["runner-foundation-digest", "Digest GHC runner foundations into compact receipts. Use when summarizing startup updaters, compact-pause updaters, reflection builders, safe orchestrators, and completion-gate runners.", "Record runner name, purpose, output receipt, pass/fail status, and whether it crossed any exact or blocked gate."],
  ["private-evidence-firewall", "Guard against private evidence publication. Use before staging GHC artifacts, receipts, screenshots, browser work, or local runner outputs.", "Scan for browser routes, private URLs, credentials, screenshots, transcript text, private lane body content, private machine paths, runtime streams, and dumps. Stop or redact before publication."],
  ["round-robin-next-lane", "Confirm next GHC round-robin lane. Use when closing x1/x2 phases or preparing the next sibling group.", "Check the cadence and Hamish's latest redirect. Do not contact every sibling by default; prepare only the scoped next lane."],
];

const generatedAt = new Date();
const generatedUtc = generatedAt.toISOString();
const generatedNz = nzTimestamp(generatedAt);
const installed = [];

for (const [name, description, guidance] of skills) {
  const dir = path.join(skillsRoot, name);
  fs.mkdirSync(dir, { recursive: true });
  const skillMd = `---\nname: ${name}\ndescription: ${description}\n---\n\n# ${titleCase(name)}\n\n## Procedure\n\n- Start from omega-mini-2 current-state and the latest exact phase receipts.\n- ${guidance}\n- Emit status-only summaries with repo-relative artifact names and explicit open boundaries.\n- Stop before account mutation, deployment, purchase, API-key creation, destructive cleanup, global hook installation, held-sibling activation, or identity merge work unless Hamish gives a fresh exact approval packet.\n\n## Output Standard\n\nReturn a compact receipt with status, evidence files, completed checks, open blockers, and next safe step. Do not include private route data, transcript text, screenshots, credentials, private machine paths, or runtime streams.\n`;
  fs.writeFileSync(path.join(dir, "SKILL.md"), skillMd, "utf8");
  installed.push({ name, directory: dir, description });
}

const outDir = path.join(repoRoot, "docs", "trinity-live-traces");
fs.mkdirSync(outDir, { recursive: true });
const receipt = {
  artifact_type: "ghc_v7_x2_skill_pack_installer",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_20_LOCAL_SKILLS_INSTALLED",
  skills_root: "user_codex_skills",
  installed_count: installed.length,
  installed_skills: installed.map((item) => item.name),
  policy: {
    local_user_skills_updated_with_hamish_authorization: true,
    plugin_cache_mutation: false,
    new_agents_spawned: false,
    deployment: false,
    account_mutation: false,
    global_hook_installed: false,
  },
  publication_boundary: {
    private_route_handles_published: false,
    private_lane_body_content_published: false,
    raw_transcripts_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
};

const base = `${phaseSlug}-skill-pack-installation-v1`;
fs.writeFileSync(path.join(outDir, `${base}.json`), JSON.stringify(receipt, null, 2) + "\n", "utf8");
fs.writeFileSync(path.join(outDir, `${base}.md`), renderMarkdown(receipt), "utf8");

console.log(JSON.stringify({ status: receipt.overall_status, installed_count: installed.length, receipt: `${base}.json` }, null, 2));

function readArg(flag, fallback) {
  const index = process.argv.indexOf(flag);
  if (index >= 0 && process.argv[index + 1]) return process.argv[index + 1];
  return fallback;
}

function titleCase(name) {
  return name.split("-").map((part) => part.charAt(0).toUpperCase() + part.slice(1)).join(" ");
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date).reduce((acc, part) => {
    acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}

function renderMarkdown(receipt) {
  return `# v552 v7 x2 Skill Pack Installation\n\nStatus: \`${receipt.overall_status}\`\n\nInstalled local skills: \`${receipt.installed_count}\`\n\n## Skills\n\n${receipt.installed_skills.map((name) => `- \`${name}\``).join("\n")}\n\n## Boundary\n\n- Local user skills were installed with Hamish's v7 x2 authorization.\n- Plugin cache, accounts, deployments, purchases, API keys, global hooks, and held sibling activation were not mutated.\n- Publication is status-only; no private route data, transcript text, screenshots, credentials, private machine paths, or runtime streams are published.\n`;
}
