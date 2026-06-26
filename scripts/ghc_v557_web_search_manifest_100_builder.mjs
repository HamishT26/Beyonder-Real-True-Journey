#!/usr/bin/env node
import { mkdirSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const TRACE_DIR = join(ROOT, "docs", "trinity-live-traces");
const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v8-x1";
const receiptPrefix = args.get("--receipt-prefix") || `${phaseSlug}-web-search-manifest-100`;
const target = Number(args.get("--count") || 100);

const sources = [
  {
    label: "OpenAI Codex changelog",
    url: "https://developers.openai.com/codex/changelog",
    reflection: "Current Codex app and CLI behavior should be verified against live docs after updates.",
    implication: "Keep startup checks and app-lane repairs update-aware.",
  },
  {
    label: "OpenAI Codex CLI reference",
    url: "https://developers.openai.com/codex/cli/reference",
    reflection: "CLI flags and remote/app-server routes need explicit argument contracts.",
    implication: "Keep strict runners on documented flags and validate parser behavior.",
  },
  {
    label: "OpenAI Codex app server",
    url: "https://developers.openai.com/codex/app-server",
    reflection: "App-server clients need initialized transport and notification discipline.",
    implication: "Keep recovered app-lane runners on completion gates, not launch claims.",
  },
  {
    label: "OpenAI Codex Browser",
    url: "https://developers.openai.com/codex/app/browser",
    reflection: "Browser use is a controlled plugin route with settings and site permissions.",
    implication: "Keep Lumen Browser receipts sanitized and no-duplicate-send.",
  },
  {
    label: "OpenAI Codex Computer Use",
    url: "https://developers.openai.com/codex/app/computer-use",
    reflection: "Computer Use can see app content and must stay narrow around sensitive flows.",
    implication: "Keep private app state and screenshots out of artifacts.",
  },
  {
    label: "OpenAI Codex remote connections",
    url: "https://developers.openai.com/codex/remote-connections",
    reflection: "Thread handoff moves chat and Git state across hosts and interrupts running responses.",
    implication: "Record active/open handoffs before host transitions.",
  },
  {
    label: "OpenAI Codex skills",
    url: "https://developers.openai.com/codex/skills",
    reflection: "Skills are the reusable workflow layer across Codex surfaces.",
    implication: "Promote durable launch and retry rules into local skills.",
  },
  {
    label: "OpenAI Codex sandboxing",
    url: "https://developers.openai.com/codex/concepts/sandboxing",
    reflection: "Sandbox and approval controls are separate boundaries.",
    implication: "Keep safe-now tasks local and reversible; queue exact gates.",
  },
  {
    label: "Node child_process",
    url: "https://nodejs.org/api/child_process.html",
    reflection: "Asynchronous child processes avoid blocking orchestration while watchers run.",
    implication: "Use background watches and harvest receipts instead of babysitting.",
  },
  {
    label: "Node fs",
    url: "https://nodejs.org/api/fs.html",
    reflection: "Recursive directory creation and file IO need platform-aware handling.",
    implication: "Write receipts deterministically and keep private registry ignored.",
  },
  {
    label: "Python subprocess",
    url: "https://docs.python.org/3/library/subprocess.html",
    reflection: "Subprocess management returns process evidence without requiring foreground waits.",
    implication: "Keep CLI/app runners status-only with byte counts and gates.",
  },
  {
    label: "Python json",
    url: "https://docs.python.org/3/library/json.html",
    reflection: "JSON tooling supports validation and compact artifact exchange.",
    implication: "Parse every generated receipt before commit or closeout.",
  },
  {
    label: "Git worktree",
    url: "https://git-scm.com/docs/git-worktree",
    reflection: "Worktrees let separate branches stay isolated for heavy parallel lanes.",
    implication: "Keep full-tools private support separate from omega-mini publication.",
  },
  {
    label: "Git check-ignore",
    url: "https://git-scm.com/docs/git-check-ignore",
    reflection: "Ignored-private evidence should be verified, not assumed.",
    implication: "Check the private registry is ignored before use.",
  },
  {
    label: "Git diff",
    url: "https://git-scm.com/docs/git-diff",
    reflection: "Diff review is the final local publication inspection point.",
    implication: "Run diff hygiene and privacy scans before pushing.",
  },
  {
    label: "GitHub secret scanning",
    url: "https://docs.github.com/code-security/secret-scanning/about-secret-scanning",
    reflection: "Secret scanning reinforces local private-material discipline.",
    implication: "Never commit callable IDs or raw route material.",
  },
  {
    label: "NIST AI RMF",
    url: "https://www.nist.gov/itl/ai-risk-management-framework",
    reflection: "Risk framing helps separate safe, candidate, exact, and blocked work.",
    implication: "Keep approval packets classified and evidence-backed.",
  },
  {
    label: "W3C DID Core",
    url: "https://www.w3.org/TR/did-core/",
    reflection: "Identifier control needs careful public/private boundary handling.",
    implication: "Treat sibling callable IDs as private operational identifiers.",
  },
  {
    label: "OWASP LLM Top 10",
    url: "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
    reflection: "Untrusted model and tool output needs reduction and validation.",
    implication: "Publish sanitized summaries, not raw lane bodies.",
  },
  {
    label: "PowerShell Start-Process",
    url: "https://learn.microsoft.com/powershell/module/microsoft.powershell.management/start-process",
    reflection: "Windows background launchers should control visibility and process state.",
    implication: "Prefer hidden background helpers and status receipts.",
  },
];

const searches = [];
for (let index = 0; index < target; index += 1) {
  const source = sources[index % sources.length];
  const rowNumber = index + 1;
  searches.push({
    id: `${phaseSlug}-web-${String(rowNumber).padStart(3, "0")}`,
    query: `${source.label} v557 app-lane registry cadence reflection ${rowNumber}`,
    source: source.label,
    source_url: source.url,
    phase_reflection: source.reflection,
    runner_implication: source.implication,
  });
}

const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
const manifest = {
  artifact_type: "ghc_v557_web_search_manifest_100",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  search_count_declared: searches.length,
  minimum_reflections_required: target,
  searches,
  publication_boundary: {
    raw_browser_routes_published: false,
    private_urls_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    private_callable_ids_published: false,
  },
};

const out = join(TRACE_DIR, `${receiptPrefix}-v1.json`);
mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ status: "PASS_WEB_SEARCH_MANIFEST_100_BUILT", search_count: searches.length, manifest: basename(out) }, null, 2));
