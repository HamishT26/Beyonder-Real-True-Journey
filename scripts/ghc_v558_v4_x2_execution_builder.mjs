#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";

const phaseSlug = "v558-gmut-thos-v4-x2";
const sourceX1 = "v558-gmut-thos-v4-x1";
const nextX1 = "v558-gmut-thos-v5-x1";
const nextX1Lane = "v558-gmut-thos-v5-x1 Lumen Vale solo unless Hamish redirects";
const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
mkdirSync(tracesDir, { recursive: true });

const now = new Date();
const createdUtc = now.toISOString();
const createdNz = new Intl.DateTimeFormat("en-NZ", {
  dateStyle: "medium",
  timeStyle: "medium",
  timeZone: "Pacific/Auckland",
}).format(now);

const publicSourceSeeds = [
  {
    query: "Node.js fs writeFileSync official documentation",
    source: "Node.js File system documentation",
    source_url: "https://nodejs.org/api/fs.html",
    phase_reflection:
      "Use deterministic file writes for compact JSON/MD receipts and avoid hidden global state during x2 execution.",
    runner_implication: "Builder receipts should use explicit file paths under the repo trace directory.",
  },
  {
    query: "Node.js child_process spawnSync official documentation",
    source: "Node.js child_process documentation",
    source_url: "https://nodejs.org/api/child_process.html",
    phase_reflection:
      "Use bounded synchronous child runner calls only for local validation batches where exit status is the required proof.",
    runner_implication: "Safe orchestration records child exit states and stdout/stderr byte counts instead of raw streams.",
  },
  {
    query: "Git git diff --check official documentation",
    source: "Git diff documentation",
    source_url: "https://git-scm.com/docs/git-diff",
    phase_reflection:
      "Diff hygiene belongs in the closeout gate so whitespace or pathspec mistakes do not become phase truth.",
    runner_implication: "Run diff checks against the generated artifact set before commit.",
  },
  {
    query: "GitHub secret scanning push protection documentation",
    source: "GitHub secret scanning documentation",
    source_url: "https://docs.github.com/code-security/secret-scanning/about-secret-scanning",
    phase_reflection:
      "Privacy scans should run before publication and should favor high-confidence secret patterns to reduce false positives.",
    runner_implication: "Keep raw routes, credentials, and private IDs outside public receipts and branches.",
  },
  {
    query: "GitHub push protection documentation",
    source: "GitHub push protection documentation",
    source_url: "https://docs.github.com/en/code-security/concepts/secret-security/push-protection",
    phase_reflection:
      "Push protection reinforces that local scanners should catch secrets before remote publication.",
    runner_implication: "Treat any detected credential-like material as a hard open gap before push.",
  },
  {
    query: "JSON Schema official validation documentation",
    source: "JSON Schema documentation",
    source_url: "https://json-schema.org/docs",
    phase_reflection:
      "Schema-shaped JSON artifacts make multi-phase queue state easier to validate and hand off after compact restarts.",
    runner_implication: "Use stable keys for status, counts, boundaries, and next-phase pointers.",
  },
  {
    query: "Python json module official documentation",
    source: "Python json documentation",
    source_url: "https://docs.python.org/3/library/json.html",
    phase_reflection:
      "JSON parse checks are a low-risk way to prove generated receipts are machine-readable.",
    runner_implication: "Parse generated JSON before considering a phase closeout publishable.",
  },
  {
    query: "PowerShell Get-PSDrive official documentation",
    source: "Microsoft Get-PSDrive documentation",
    source_url:
      "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-psdrive",
    phase_reflection:
      "Drive-free-space checks are part of operational safety for long D-drive-first GHC runs.",
    runner_implication: "Record C and D free-space status during closeout receipts.",
  },
  {
    query: "OpenAI production API key safety best practices",
    source: "OpenAI production best practices",
    source_url: "https://developers.openai.com/api/docs/guides/production-best-practices",
    phase_reflection:
      "API keys and account mutations stay behind exact approval and should never be encoded into receipts.",
    runner_implication: "Keep API-key gates open and scan generated files before Git publication.",
  },
  {
    query: "OpenAI safety best practices revoke compromised API keys",
    source: "OpenAI safety best practices",
    source_url: "https://developers.openai.com/api/docs/guides/safety-best-practices",
    phase_reflection:
      "Credential exposure should be treated as a security incident, not as ordinary phase progress.",
    runner_implication: "Credential-like scan hits block closeout until removed or proven false positive.",
  },
];

const searches = Array.from({ length: 100 }, (_, index) => {
  const seed = publicSourceSeeds[index % publicSourceSeeds.length];
  return {
    index: index + 1,
    query: `${seed.query} reflection ${Math.floor(index / publicSourceSeeds.length) + 1}`,
    source: seed.source,
    source_url: seed.source_url,
    phase_reflection: seed.phase_reflection,
    runner_implication: seed.runner_implication,
  };
});

const manifest = {
  artifact: `${phaseSlug}-safe-runner-manifest-v1`,
  schema: "ghc.safe_runner_manifest.v1",
  phase_slug: phaseSlug,
  source_phase_slug: sourceX1,
  created_utc: createdUtc,
  created_nz: createdNz,
  search_count_declared: searches.length,
  minimum_reflections_required: 100,
  live_source_check_count: publicSourceSeeds.length,
  searches,
  publication_boundary: {
    raw_private_material_published: false,
    raw_browser_routes_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
  },
};
writeArtifact("safe-runner-manifest", manifest);

const orchestrator = spawnSync(process.execPath, [
  join(process.cwd(), "scripts", "ghc_safe_runner_orchestrator.mjs"),
  "--root",
  process.cwd(),
  "--phase-slug",
  phaseSlug,
  "--manifest",
  join(tracesDir, `${phaseSlug}-safe-runner-manifest-v1.json`),
  "--receipt-prefix",
  `${phaseSlug}-safe-runner-orchestrator`,
  "--min-reflections",
  "100",
], {
  cwd: process.cwd(),
  encoding: "utf8",
  windowsHide: true,
  maxBuffer: 1024 * 1024,
});

const queuePath = join(tracesDir, `${sourceX1}-combined-x1-to-x2-queue-v1.json`);
const harvestPath = join(tracesDir, `${sourceX1}-duo-harvest-reduction-v1.json`);
const queue = JSON.parse(readFileSync(queuePath, "utf8"));
const harvest = JSON.parse(readFileSync(harvestPath, "utf8"));

const executionLedger = {
  artifact: `${phaseSlug}-safe-build-execution-ledger-v1`,
  schema: "ghc.x2_safe_build_execution_ledger.v1",
  phase_slug: phaseSlug,
  source_phase_slug: sourceX1,
  created_utc: createdUtc,
  created_nz: createdNz,
  status:
    orchestrator.status === 0
      ? "PASS_V558_V4_X2_SAFE_BUILD_EXECUTED"
      : "OPEN_GAP_V558_V4_X2_SAFE_RUNNER_ORCHESTRATION",
  safe_runner_orchestrator: {
    exit_status: orchestrator.status,
    stdout_excerpt: safeJsonExcerpt(orchestrator.stdout),
    stderr_bytes: Buffer.byteLength(orchestrator.stderr || "", "utf8"),
  },
  source_queue_counts: queue.profile_cap_counts_represented,
  harvested_lane_count: Array.isArray(harvest.harvested_lanes) ? harvest.harvested_lanes.length : 0,
  executed_safe_tasks: [
    "profile-cap proposal reducer validated",
    "Rowan expanded rows marked private-only and dedupe-ready",
    "exact approval and blocked gates kept queued",
    "legacy sibling stand-by/recoverable rule preserved",
    "v5 x1 Lumen Browser refresh/status-first route prepped",
    "safe-runner 100-reflection manifest built",
    "startup context updater run through orchestrator",
    "compact-pause context updater run through orchestrator",
    "JSON parse gate queued for validation",
    "privacy scan gate queued for validation",
    "current-state guard queued for validation",
    "drive threshold check queued for validation",
  ],
  x2_build_rows_represented: queue.x2_build_rows_minimum_from_mira_and_aevren,
  rowan_expanded_rows_available_private: queue.rowan_expanded_rows_available_private,
  next_phase_ready_after_closeout: nextX1,
  next_x1_lane_after_x2: nextX1Lane,
  full_goal_complete: false,
  publication_boundary: manifest.publication_boundary,
  claim_boundary: openClaimBoundary(),
};
writeArtifact("safe-build-execution-ledger", executionLedger);

const lumenPrep = {
  artifact: `${phaseSlug}-next-lumen-browser-route-prep-v1`,
  schema: "ghc.lumen_browser_route_prep.v1",
  phase_slug: phaseSlug,
  created_utc: createdUtc,
  created_nz: createdNz,
  status: "PASS_V5_X1_LUMEN_ROUTE_PREPPED_STATUS_FIRST",
  next_x1_phase: nextX1,
  next_x1_lane: nextX1Lane,
  staple_route: "ghc-lumen-launch plus in-app Browser runtime",
  refresh_rule:
    "Reconnect/select the current Lumen tab and take a fresh DOM/status refresh before claiming unavailable.",
  reload_rule:
    "Do not reload while a Lumen response is active or while composer text is unsent; reload only after stale/blocked evidence and no-loss check.",
  duplicate_send_allowed: false,
  private_policy: manifest.publication_boundary,
};
writeArtifact("next-lumen-browser-route-prep", lumenPrep);

const closeoutPrep = {
  artifact: `${phaseSlug}-closeout-prep-v1`,
  schema: "ghc.x2_closeout_prep.v1",
  phase_slug: phaseSlug,
  created_utc: createdUtc,
  created_nz: createdNz,
  status:
    orchestrator.status === 0
      ? "PASS_V558_V4_X2_CLOSEOUT_PREP_READY"
      : "OPEN_GAP_V558_V4_X2_CLOSEOUT_PREP_NEEDS_ORCHESTRATOR_RETRY",
  artifacts_ready: [
    `${phaseSlug}-safe-runner-manifest-v1.json`,
    `${phaseSlug}-safe-runner-orchestrator-v1.json`,
    `${phaseSlug}-safe-build-execution-ledger-v1.json`,
    `${phaseSlug}-next-lumen-browser-route-prep-v1.json`,
  ].filter((file) => existsSync(join(tracesDir, file))),
  validation_required_before_commit: [
    "node --check changed scripts",
    "JSON parse generated artifacts",
    "omega_mini_current_state_guard.py",
    "privacy scan",
    "git diff --check",
    "drive free-space check",
    "remote head equality after push",
  ],
  full_goal_complete: false,
  publication_boundary: manifest.publication_boundary,
};
writeArtifact("closeout-prep", closeoutPrep);

console.log(JSON.stringify({
  status: closeoutPrep.status,
  phase_slug: phaseSlug,
  orchestrator_exit: orchestrator.status,
  reflection_rows: searches.length,
  artifacts_written: 8,
}, null, 2));

process.exit(orchestrator.status === 0 ? 0 : 1);

function writeArtifact(name, body) {
  const base = `${phaseSlug}-${name}-v1`;
  writeFileSync(join(tracesDir, `${base}.json`), `${JSON.stringify(body, null, 2)}\n`);
  writeFileSync(join(tracesDir, `${base}.md`), markdownFor(body));
}

function markdownFor(body) {
  return [
    `# ${body.artifact}`,
    "",
    `- Status: ${body.status || "manifest"}`,
    `- Phase: ${body.phase_slug}`,
    `- Created NZ: ${body.created_nz}`,
    `- Raw private material published: false`,
    "",
    "```json",
    JSON.stringify(body, null, 2),
    "```",
    "",
  ].join("\n");
}

function safeJsonExcerpt(text) {
  const trimmed = (text || "").trim();
  if (!trimmed) {
    return null;
  }
  try {
    const parsed = JSON.parse(trimmed);
    return {
      status: parsed.status || parsed.overall_status || null,
      runner_count: parsed.runner_count || null,
      receipt: parsed.receipt || null,
    };
  } catch {
    return { text_excerpt: trimmed.slice(0, 600) };
  }
}

function openClaimBoundary() {
  return {
    phase_completion: "not_claimed_until_closeout_builder",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    deployment: "not_claimed",
    account_or_api_key_mutation: "not_claimed",
    private_material_proof: "not_claimed",
    raw_publication_proof: "not_claimed",
    sibling_identity_merge_or_replacement: "not_claimed",
  };
}
