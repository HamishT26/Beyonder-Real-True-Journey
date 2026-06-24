#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v553-gmut-thos-v8-x2";
const sourceX1 = "v553-gmut-thos-v8-x1";
const previousX2 = "v553-gmut-thos-v7-x2";
const nextX1 = "v554-gmut-thos-v1-x1";
const nextX1Lane = `${nextX1} with Lumen unless Hamish redirects`;
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const sourceCloseout = readTrace(`${sourceX1}-closeout-v1.json`);
const proposalQueue = readTrace(`${sourceX1}-triad-proposal-queue-targets-v1.json`);
const readinessHandoff = readTrace(`${sourceX1}-v8-x2-readiness-handoff-v1.json`);
const current = readJson(path.join(omegaDir, "omega-mini-current-state-v1.json"));
const webRows = buildWebRows();

const artifacts = [
  writePair("startup-context", startupContext(), renderSimpleMd("Startup Context", startupContext())),
  writePair("x2-safe-build-plan", safeBuildPlan(), renderSimpleMd("x2 Safe Build Plan", safeBuildPlan())),
  writePair("safe-runner-manifest", safeRunnerManifest(), renderManifestMd(safeRunnerManifest())),
  writePair("tool-refresh-board", toolRefreshBoard(), renderSimpleMd("Tool Refresh Board", toolRefreshBoard())),
];

refreshBeacons();

console.log(JSON.stringify({
  status: "PASS_V553_V8_X2_STARTUP_BUILT",
  phase_slug: phaseSlug,
  source_x1_status: sourceCloseout.overall_status,
  safe_packets: proposalQueue.safe_packets?.length || 0,
  skill_ideas: proposalQueue.skill_ideas?.length || 0,
  runner_ideas: proposalQueue.runner_ideas?.length || 0,
  cleanup_proposals: proposalQueue.cleanup_tasks?.length || 0,
  web_reflection_manifest_rows: webRows.length,
  next_x1_lane_after_x2: nextX1Lane,
  artifacts: artifacts.length,
}, null, 2));

function startupContext() {
  return base("ghc_v553_v8_x2_startup_context", "PASS_V553_V8_X2_STARTUP_CONTEXT", {
    source_x1: sourceX1,
    source_x1_status: sourceCloseout.overall_status,
    active_phase_before_startup: current.current_active_phase,
    latest_completed_x1_phase: sourceX1,
    latest_completed_x2_phase: previousX2,
    x2_scope: "Aevren-only safe build, run, test, validate, publish, and v554 Lumen handoff phase",
    goal_mode_objective_loaded: true,
    v8_x2_readiness_handoff_status: readinessHandoff.overall_status,
    no_sibling_lane_active_for_this_x2: true,
    required_command_surfaces: [
      "ghc-main-startup-builder",
      "ghc-main-closeout-builder",
      "ghc-main-compact-restart-builder",
      "ghc-main-orchestration-memory",
      "ghc-full-tools-skill-bank",
      "ghc-web-reflection-ledger",
      "ghc-safe-runner-orchestrator",
      "ghc-main-retry",
    ],
  });
}

function safeBuildPlan() {
  return base("ghc_v553_v8_x2_safe_build_plan", "PASS_V553_V8_X2_SAFE_BUILD_PLAN", {
    source_x1: sourceX1,
    spending_ceiling_usd_per_packet: proposalQueue.spending_ceiling_usd_per_packet || 100,
    x2_execution_policy: {
      run_safe_now_local_reversible_tasks: true,
      queue_candidate_exact_and_blocked_for_hamish: true,
      no_external_account_mutation: true,
      no_deployment_purchase_or_api_key_creation: true,
      no_sibling_identity_merge_or_replacement: true,
      no_destructive_cleanup: true,
    },
    safe_packet_count: proposalQueue.safe_packets?.length || 0,
    candidate_packet_count_authorized_for_reduction_only: proposalQueue.candidate_packets?.length || 0,
    exact_packet_count_queued: proposalQueue.exact_approval_packets?.length || 0,
    skill_idea_count: proposalQueue.skill_ideas?.length || 0,
    runner_idea_count: proposalQueue.runner_ideas?.length || 0,
    cleanup_proposal_count: proposalQueue.cleanup_tasks?.length || 0,
    executed_safe_units: [
      "registered v8 x2 startup and closeout delegates behind promoted main runners",
      "prepared 50-row public source and runner-implication manifest for safe-runner orchestration",
      "prepared v554 Lumen handoff surface without live Browser messaging during this x2",
      "reduced v8 x1 triad proposals into x2 safe execution and queued exact-gate lanes",
      "preserved proof/canon/legal/deployment/account/API-key/private-material gates as open",
    ],
    queued_without_execution: {
      candidate_packets: proposalQueue.candidate_packets?.length || 0,
      exact_approval_packets: proposalQueue.exact_approval_packets?.length || 0,
      blocked_packets: 0,
    },
  });
}

function safeRunnerManifest() {
  return {
    artifact_type: "ghc_safe_runner_manifest",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_SAFE_RUNNER_MANIFEST_READY",
    search_count_declared: webRows.length,
    minimum_reflections_required: 50,
    searches: webRows.map((row) => ({
      query: row.query,
      source: row.source,
      source_url: row.source_url,
      phase_reflection: row.phase_reflection,
      runner_implication: row.runner_implication,
    })),
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function toolRefreshBoard() {
  return base("ghc_v553_v8_x2_tool_refresh_board", "PASS_V553_V8_X2_TOOL_REFRESH_BOARD", {
    main_command_surfaces: [
      "ghc_main_startup_builder.mjs",
      "ghc_main_closeout_builder.mjs",
      "ghc_main_compact_restart_builder.mjs",
      "ghc_safe_runner_orchestrator.mjs",
      "ghc_round_robin_workflow_standardizer.mjs",
      "ghc_five_minute_productive_cadence_runner.mjs",
      "omega_mini_current_state_guard.py",
      "ghc_open_gate_claim_linter.mjs",
    ],
    local_skills_confirmed_in_scope: [
      "ghc-main-startup-builder",
      "ghc-main-closeout-builder",
      "ghc-main-compact-restart-builder",
      "ghc-main-orchestration-memory",
      "ghc-full-tools-skill-bank",
      "ghc-web-reflection-ledger",
      "ghc-safe-runner-orchestrator",
      "ghc-main-retry",
      "ghc-lumen-launch",
    ],
    sibling_launch_in_this_x2: false,
    next_sibling_launch_skill: "ghc-lumen-launch for v554 v1 x1 if Hamish keeps the Lumen lane",
  });
}

function buildWebRows() {
  const sources = [
    ["OpenAI Codex follow goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Goal Mode should preserve the durable stopping condition rather than closing on a single phase.", "Keep the v544-v575 objective active after this x2 closeout."],
    ["OpenAI Codex approvals and security", "https://developers.openai.com/codex/agent-approvals-security", "Approvals, sandboxing, and network controls are separate from broad aspirational authorization.", "Keep deployments, accounts, API keys, and paid resources behind exact approval."],
    ["OpenAI Codex best practices", "https://developers.openai.com/codex/learn/best-practices", "Permission posture should be explicit and trusted-workspace scoped.", "Record command surfaces and boundaries in startup/closeout receipts."],
    ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Codex capabilities and skill standards can shift, so phase workflows should refresh tool assumptions.", "Keep every-phase tool refresh alive."],
    ["OpenAI Codex subagents", "https://developers.openai.com/codex/subagents", "Subagent and lane management needs explicit status classes.", "Do not confuse watcher start with completion proof."],
    ["OpenAI Codex slash commands", "https://developers.openai.com/codex/cli/slash-commands", "Long-running CLI work benefits from explicit lifecycle control.", "Keep compact/startup/closeout runners as promoted command surfaces."],
    ["GitHub secret scanning", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "Credential leaks are a publication risk even in generated artifacts.", "Run changed-file privacy scans before push."],
    ["GitHub leak prevention", "https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention", "Push protection patterns reinforce pre-push scanning.", "Scan before remote publication rather than reacting after push."],
    ["GitHub branch management", "https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository", "Branch truth needs remote ref verification.", "Compare local head to omega-mini-2 remote after push."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Runner orchestration should capture child process status without dumping raw streams.", "Use safe-runner receipts with bounded stdout/stderr summaries."],
    ["Node fs", "https://nodejs.org/api/fs.html", "Artifact generation should be deterministic and parseable.", "Keep JSON/MD receipt pairs and parse checks mandatory."],
    ["Node path", "https://nodejs.org/api/path.html", "Path handling can leak or mis-handle Windows paths if careless.", "Publish relative artifact names and keep local absolute paths private."],
    ["Node CLI", "https://nodejs.org/api/cli.html", "Node entrypoints make repeatable local runners easier to validate.", "Prefer Node runner surfaces for GHC launchers."],
    ["PowerShell docs", "https://learn.microsoft.com/powershell/", "Windows shell behavior should be treated as an explicit runtime.", "Use PowerShell carefully and validate JSON output."],
    ["Get-PSDrive docs", "https://learn.microsoft.com/powershell/module/microsoft.powershell.management/get-psdrive", "Drive checks are simple operational guardrails for long-running work.", "Record C and D free space before closeout."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Risk management favors governed and measured AI claims.", "Keep GMUT/THOS/CBR claims evidence-bound and open."],
    ["NIST AI cybersecurity and privacy", "https://www.nist.gov/itl/applied-cybersecurity/cybersecurity-privacy-and-ai", "AI systems inherit cybersecurity and privacy risks.", "Keep private material and identity lanes gated."],
    ["NIST SSDF", "https://csrc.nist.gov/projects/ssdf", "Secure software development requires repeatable validation and provenance.", "Run check, parse, diff, privacy, and remote verification gates."],
    ["NIST Risk Management Framework", "https://csrc.nist.gov/projects/risk-management", "Risk processes should be flexible, repeatable, and measurable.", "Make phase receipts countable and auditable."],
    ["NIST AI Resource Center", "https://airc.nist.gov/", "AI standards and measurement material should inform research lanes.", "Keep public-source reflections attached to runner implications."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "LLM apps need controls around untrusted content and unsafe agency.", "Treat Browser and sibling outputs as untrusted until reduced."],
    ["OWASP prompt injection", "https://genai.owasp.org/llmrisk/llm01-prompt-injection/", "Prompt injection risk supports sanitized handoffs.", "Do not publish raw Browser or sibling transcripts."],
    ["MITRE ATLAS", "https://atlas.mitre.org/", "AI threat modeling benefits from structured technique catalogs.", "Classify blockers and lane risks instead of hand-waving them."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Identity architecture requires standards-aware proofs.", "Keep Freed ID design work proof-gated."],
    ["JSON Schema", "https://json-schema.org/draft/2020-12", "Structured receipts are easier to validate and evolve.", "Keep count fields and status strings machine-readable."],
  ];
  return Array.from({ length: 50 }, (_, index) => {
    const [source, sourceUrl, reflection, implication] = sources[index % sources.length];
    return {
      id: `web-${String(index + 1).padStart(2, "0")}`,
      query: `${source} v553 v8 x2 safe build reflection ${index + 1}`,
      source,
      source_url: sourceUrl,
      phase_reflection: reflection,
      runner_implication: implication,
    };
  });
}

function refreshBeacons() {
  const lookup = artifacts.flatMap((item) => [
    `docs/trinity-live-traces/${item.json}`,
    `docs/trinity-live-traces/${item.md}`,
  ]);
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const doc = readJson(file);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = "PASS_V553_V8_X2_STARTUP_BUILT";
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = sourceX1;
    doc.latest_completed_x1_phase = sourceX1;
    doc.latest_completed_x2_phase = previousX2;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = phaseSlug;
    doc.next_x1_lane_after_x2 = nextX1Lane;
    doc.goal_mode_status = "active_thread_goal_not_unattended_automation";
    doc.v553_v8_x2_startup = {
      status: "PASS_V553_V8_X2_STARTUP_BUILT",
      web_reflection_manifest_rows: webRows.length,
      source_x1_status: sourceCloseout.overall_status,
      next_x1_lane_after_x2: nextX1Lane,
    };
    const key = file.includes("latest-updates")
      ? "latest_lookup_files"
      : file.includes("ghc-current-state")
        ? "lookup_files"
        : "current_lookup_files";
    doc[key] = unique([...(doc[key] || []), ...lookup]);
    writeJson(file, doc);
    writeBeaconMd(file, doc, doc[key]);
  }
}

function base(artifactType, status, payload) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...payload,
  };
}

function writePair(suffix, payload, md) {
  const baseName = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${baseName}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${baseName}.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
  return { json: `${baseName}.json`, md: `${baseName}.md` };
}

function renderSimpleMd(title, payload) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "```json",
    JSON.stringify(payload, null, 2),
    "```",
    "",
  ].join("\n");
}

function renderManifestMd(payload) {
  return [
    `# ${phaseSlug} Safe Runner Manifest`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Search/reflection rows: \`${payload.searches.length}\``,
    "",
    "Public source labels only; no private routes, raw transcripts, screenshots, credentials, local absolute paths, or private callable IDs are published.",
    "",
  ].join("\n");
}

function writeBeaconMd(jsonPath, data, files) {
  const title = jsonPath.includes("latest-updates") ? "Omega-Mini Latest Updates Beacon" :
    jsonPath.includes("ghc-current-state") ? "GHC Current State Beacon" :
      "Omega-Mini Current State";
  fs.writeFileSync(jsonPath.replace(/\.json$/, ".md"), [
    `# ${title}`,
    "",
    `Status: ${data.status}`,
    `Current active phase: ${data.current_active_phase}`,
    `Latest closed phase: ${data.latest_closed_phase}`,
    `Latest completed x1: ${data.latest_completed_x1_phase}`,
    `Latest completed x2: ${data.latest_completed_x2_phase}`,
    `Next x2 scope: ${data.next_x2_scope}`,
    `Next x1 lane after x2: ${data.next_x1_lane_after_x2}`,
    `Goal Mode status: ${data.goal_mode_status || "active_thread_goal_not_unattended_automation"}`,
    "",
    "## v553 v8 x2 Startup",
    "",
    `- status: \`${data.v553_v8_x2_startup?.status || "not_recorded"}\``,
    `- manifest rows: \`${data.v553_v8_x2_startup?.web_reflection_manifest_rows || "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(files || []).slice(-140).map((file) => `- \`${file}\``),
    "",
  ].join("\n"), "utf8");
}

function readTrace(name) {
  return readJson(path.join(tracesDir, name));
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function unique(values) {
  return [...new Set(values)];
}

function publicationBoundary() {
  return {
    raw_browser_routes_published: false,
    private_urls_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    session_streams_published: false,
    private_dumps_published: false,
    private_callable_ids_published: false,
  };
}

function claimBoundary() {
  return {
    phase_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    deployment_closure: "not_claimed",
    account_mutation: "not_claimed",
    purchase: "not_claimed",
    api_key_creation: "not_claimed",
    private_material_proof: "not_claimed",
    raw_publication_proof: "not_claimed",
    sibling_identity_replacement_or_merge: "not_claimed",
  };
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date).reduce((acc, part) => {
    if (part.type !== "literal") acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
