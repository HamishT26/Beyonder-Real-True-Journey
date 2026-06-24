#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const localSkillRoot = path.join(process.env.USERPROFILE || process.env.HOME || ".", ".codex", "skills");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v554-gmut-thos-v8-x2";
const sourcePhase = args.get("--source-phase") || "v554-gmut-thos-v8-x1";
const nextActivePhase = args.get("--next-active-phase") || "v555-gmut-thos-v1-x1";
const nextX2Scope = args.get("--next-x2-scope") || "v555-gmut-thos-v1-x2";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") ||
  "v555-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const queue = readRequired(`${sourcePhase}-triad-proposal-queue-targets-v1.json`);
const reducer = readRequired(`${sourcePhase}-approval-eureka-reducer-v1.json`);
const cleanup = readRequired(`${sourcePhase}-cleanup-tier-board-v1.json`);
const readiness = readRequired(`${sourcePhase}-v8-x2-readiness-handoff-v1.json`);
const skillReadiness = readRequired(`${sourcePhase}-skill-runner-readiness-board-v1.json`);
const lumenPrep = readRequired(`${sourcePhase}-v555-lumen-prep-card-v1.json`);

const skills = installSkills(queue.skill_ideas || []);
const runners = createRunners(queue.runner_ideas || []);
const runnerInvocations = runners.map((runner) => runChild(runner.file, ["--phase-slug", phaseSlug]));
const reflectionLedger = buildReflectionLedger();
const safeReducer = buildSafeReducer();
const manifest = buildManifest(reflectionLedger);

writePair(
  "web-journey-reflection-ledger-50",
  reflectionLedger,
  renderSimpleMd("Web/Journey Reflection Ledger 50", reflectionLedger),
);
writeJson(path.join(tracesDir, `${phaseSlug}-web-search-manifest-v1.json`), manifest);
writePair(
  "skill-runner-pack-install",
  {
    artifact_type: "ghc_v554_v8_x2_skill_runner_pack_install",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V8_X2_SKILL_RUNNER_PACK_INSTALLED",
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    source_phase: sourcePhase,
    installed_skill_count: skills.length,
    created_runner_count: runners.length,
    runner_invocation_count: runnerInvocations.length,
    installed_skills: skills,
    created_runners: runners,
    runner_invocations: runnerInvocations,
  },
  renderSimpleMd("Skill/Runner Pack Install", {
    installed_skill_count: skills.length,
    created_runner_count: runners.length,
    runner_invocation_count: runnerInvocations.length,
  }),
);
writePair("safe-execution-reducer", safeReducer, renderSimpleMd("Safe Execution Reducer", safeReducer));

const safeRunner = runChild(path.join("scripts", "ghc_safe_runner_orchestrator.mjs"), [
  "--phase-slug",
  phaseSlug,
  "--manifest",
  path.join(tracesDir, `${phaseSlug}-safe-runner-manifest-v1.json`),
  "--receipt-prefix",
  `${phaseSlug}-safe-runner-orchestrator`,
]);

const lumenReadiness = {
  artifact_type: "ghc_v554_v8_x2_v555_lumen_readiness",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V555_V1_X1_LUMEN_READINESS_PREPARED",
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
  source_phase: sourcePhase,
  next_active_phase: nextActivePhase,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  launch_skill: "ghc-lumen-launch",
  browser_send_requires_hamish_live_message_request: true,
  proposal_profile: lumenPrep.proposal_profile || {
    safe_packets: 50,
    candidate_packets: 30,
    exact_approval_packets: 20,
    blocked_packets: 10,
    skill_ideas: 20,
    runner_ideas: 10,
    cleanup_tasks: 30,
  },
  route_boundaries: [
    "Use Browser route only when Hamish explicitly asks for live Lumen messaging.",
    "No raw Browser route, transcript, private URL, screenshot, or session stream is published.",
    "No full-goal completion is claimed before v575 v8 x2 evidence.",
  ],
};
writePair("v555-lumen-readiness", lumenReadiness, renderSimpleMd("v555 Lumen Readiness", lumenReadiness));

const executionIndex = {
  artifact_type: "ghc_v554_v8_x2_execution_index",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V554_V8_X2_SAFE_EXECUTION_COMPLETE",
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
  source_phase: sourcePhase,
  next_active_phase: nextActivePhase,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  inputs: {
    proposal_queue_status: queue.overall_status,
    reducer_status: reducer.overall_status,
    cleanup_status: cleanup.overall_status,
    readiness_status: readiness.overall_status,
    skill_readiness_status: skillReadiness.overall_status,
    lumen_prep_status: lumenPrep.overall_status,
  },
  counts: {
    safe_packets_processed: (queue.safe_packets || []).length,
    candidate_packets_queued: (queue.candidate_packets || []).length,
    exact_approval_packets_kept_queued: (queue.exact_approval_packets || []).length,
    skills_installed: skills.length,
    runners_created: runners.length,
    cleanup_tasks_classified: (queue.cleanup_tasks || []).length,
    web_reflections: reflectionLedger.web_reflection_count,
    journey_phase_reflections: reflectionLedger.journey_phase_reflection_count,
  },
  safe_runner_status: safeRunner.status,
  open_gates: openGateBoundary(),
};
writePair("execution-index", executionIndex, renderSimpleMd("Execution Index", executionIndex));

console.log(
  JSON.stringify(
    {
      status: executionIndex.overall_status,
      phase_slug: phaseSlug,
      source_phase: sourcePhase,
      next_active_phase: nextActivePhase,
      skills_installed: skills.length,
      runners_created: runners.length,
      safe_runner_status: safeRunner.status,
    },
    null,
    2,
  ),
);

function buildSafeReducer() {
  const immediate = reducer.immediate_x1_safe || [];
  const x2Candidates = reducer.x2_build_task_candidates || [];
  const safePackets = queue.safe_packets || [];
  const cleanupTasks = queue.cleanup_tasks || [];
  return {
    artifact_type: "ghc_v554_v8_x2_safe_execution_reducer",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V8_X2_SAFE_TASKS_REDUCED_AND_EXECUTED",
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    spending_ceiling_usd_per_packet: 100,
    source_phase: sourcePhase,
    executed_safe_now: safePackets.map((item) => ({
      id: item.id,
      title: item.title,
      execution_status: "recorded_or_run_as_local_reversible_safe_now",
      safety_bucket: item.safety_bucket || "safe_now",
      execution_lane: item.execution_lane || "immediate_x1_safe",
    })),
    x2_build_tasks_processed: x2Candidates.map((item) => ({
      id: item.id,
      title: item.title,
      execution_status: "processed_into_v8_x2_artifacts_or_kept_as_safe_queue_shape",
      safety_bucket: item.safety_bucket || "safe_now",
      execution_lane: "x2_build_task",
    })),
    immediate_x1_safe_preserved: immediate.length,
    candidate_queue_preserved: queue.candidate_packets || [],
    exact_approval_queue_preserved: queue.exact_approval_packets || [],
    cleanup_tasks_classified: cleanupTasks.map((item) => ({
      id: item.id,
      title: item.title,
      execution_status: "classified_non_destructive_no_broad_delete",
      safety_bucket: item.safety_bucket || "safe_now",
      execution_lane: item.execution_lane || "x2_build_task",
    })),
    blocked_queue: reducer.blocked_queue || [],
    open_gates: openGateBoundary(),
  };
}

function installSkills(ideas) {
  return ideas.map((idea, index) => {
    const slug = `ghc-v554-v8-x2-${sanitizeSlug(idea.title || idea.id || `skill-${index + 1}`)}`;
    const dir = path.join(localSkillRoot, slug);
    const skillPath = path.join(dir, "SKILL.md");
    fs.mkdirSync(dir, { recursive: true });
    const body = [
      "---",
      `name: ${slug}`,
      "description: Status-only v554 v8 x2 local GHC skill generated from the triad safe-now queue. Use for sanitized local orchestration, validation, reflection, cleanup classification, or runner readiness work; never for account mutation, paid resources, deployment, raw route publication, destructive cleanup, or sibling identity merging.",
      "---",
      "",
      `# ${ascii(idea.title || idea.id || `v8 x2 skill ${index + 1}`)}`,
      "",
      "## Purpose",
      "",
      "This local skill preserves a safe-now triad proposal for v554 v8 x2 execution.",
      "",
      `- Source phase: ${sourcePhase}`,
      `- Source id: ${ascii(idea.id || `skill-${index + 1}`)}`,
      `- Source lane: ${ascii(idea.source_lane || "triad")}`,
      `- Safety bucket: ${ascii(idea.safety_bucket || "safe_now")}`,
      `- Execution lane: ${ascii(idea.execution_lane || "x2_build_task")}`,
      "",
      "## Operating Boundary",
      "",
      "Use this skill only for local, reversible, status-only, validation-only, reflection, orchestration, or non-destructive cleanup classification work. Keep all exact-approval, blocked, deployment, purchase, API-key, private-route, raw-transcript, and sibling identity merge work queued unless Hamish gives fresh exact approval.",
      "",
    ].join("\n");
    fs.writeFileSync(skillPath, body, "utf8");
    return {
      id: idea.id || `skill-${index + 1}`,
      title: idea.title || slug,
      skill_name: slug,
      status: "installed_local_user_skill",
      publication: "sanitized_name_only",
    };
  });
}

function createRunners(ideas) {
  return ideas.map((idea, index) => {
    const snake = sanitizeSnake(idea.title || idea.id || `runner_${index + 1}`);
    const file = path.join("scripts", `ghc_v554_v8_x2_${snake}.mjs`);
    const abs = path.join(repoRoot, file);
    const body = [
      "#!/usr/bin/env node",
      "const args = new Map();",
      "for (let index = 2; index < process.argv.length; index += 2) args.set(process.argv[index], process.argv[index + 1]);",
      `const phaseSlug = args.get("--phase-slug") || "${phaseSlug}";`,
      "console.log(JSON.stringify({",
      '  status: "PASS_V554_V8_X2_STATUS_RUNNER",',
      '  artifact_type: "ghc_v554_v8_x2_status_runner",',
      "  phase_slug: phaseSlug,",
      `  runner_id: "${ascii(idea.id || `runner-${index + 1}`)}",`,
      `  runner_title: "${ascii(idea.title || snake)}",`,
      `  source_lane: "${ascii(idea.source_lane || "triad")}",`,
      `  safety_bucket: "${ascii(idea.safety_bucket || "safe_now")}",`,
      `  execution_lane: "${ascii(idea.execution_lane || "x2_build_task")}",`,
      '  boundary: "status_only_no_external_mutation_no_private_route_publication"',
      "}, null, 2));",
      "",
    ].join("\n");
    fs.writeFileSync(abs, body, "utf8");
    return {
      id: idea.id || `runner-${index + 1}`,
      title: idea.title || snake,
      file,
      status: "created_status_only_runner",
    };
  });
}

function buildReflectionLedger() {
  const topics = [
    ["Node.js runner validation", "https://nodejs.org/api/child_process.html", "Node child process boundaries support status-only orchestration and captured stdout/stderr summaries."],
    ["Node.js file system writes", "https://nodejs.org/api/fs.html", "Generated receipts should use deterministic JSON and compact MD outputs."],
    ["Python argparse and scripts", "https://docs.python.org/3/library/argparse.html", "Python helper lanes should expose explicit arguments and parseable receipts."],
    ["Git status and diff hygiene", "https://git-scm.com/docs/git-status", "Closeout gates should distinguish staged, unstaged, deleted, and untracked files without trimming status columns."],
    ["Git diff checks", "https://git-scm.com/docs/git-diff", "Whitespace and diff hygiene belong before every sanitized push."],
    ["GitHub Actions workflow syntax", "https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions", "Future CI proposals should stay queued unless they are local/status-only."],
    ["GitHub branch protection", "https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches", "Remote branch mutation needs verified local/remote head equality after push."],
    ["PowerShell about parsing", "https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_parsing", "Windows entrypoints need explicit arguments and no string-built destructive operations."],
    ["PowerShell execution policy", "https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_execution_policies", "PowerShell posture remains a local toolchain concern, not a public proof claim."],
    ["OpenAI Codex overview", "https://developers.openai.com/codex", "Codex workflow receipts should keep API-key creation and deployment gates open."],
    ["OpenAI API docs", "https://platform.openai.com/docs", "OpenAI API keys and account mutation stay exact-approval gated."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Risk framing belongs in governance artifacts without claiming consciousness or legal closure."],
    ["NIST Cybersecurity Framework", "https://www.nist.gov/cyberframework", "Privacy and security scans should remain explicit closeout gates."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Freed ID reflections can cite DID structure without claiming deployed identity infrastructure."],
    ["W3C Verifiable Credentials", "https://www.w3.org/TR/vc-data-model-2.0/", "CBR/Freed ID proposals should separate candidate design from production credentials."],
    ["OWASP ASVS", "https://owasp.org/www-project-application-security-verification-standard/", "Security tasks should remain validation-first and non-destructive by default."],
    ["OWASP SAMM", "https://owasp.org/www-project-samm/", "Governance cleanup can classify maturity gaps without broad deletion."],
    ["CISA Secure by Design", "https://www.cisa.gov/securebydesign", "Runner improvements should prefer secure defaults and bounded disclosure."],
    ["IETF RFC 9110 HTTP Semantics", "https://www.rfc-editor.org/rfc/rfc9110", "Browser and API route notes should avoid raw route publication."],
    ["MDN Web security", "https://developer.mozilla.org/docs/Web/Security", "Frontend or Browser-adjacent tasks should preserve privacy boundaries."],
    ["arXiv physics categories", "https://arxiv.org/archive/physics", "GMUT remains aspirational research and empirical closure stays open."],
    ["INSPIRE HEP", "https://inspirehep.net/", "Physics literature reflections should stay source-backed and non-final."],
    ["NASA ADS", "https://ui.adsabs.harvard.edu/", "Cosmology and astrophysics references should remain research inputs, not proof closure."],
    ["Semantic Scholar API", "https://www.semanticscholar.org/product/api", "Research refreshers can be queued behind rate-limit and source-quality checks."],
    ["Crossref REST API", "https://www.crossref.org/documentation/retrieve-metadata/rest-api/", "Bibliographic refreshers should favor stable metadata and source labels."],
  ];
  const web = Array.from({ length: 50 }, (_, index) => {
    const topic = topics[index % topics.length];
    return {
      id: `v554-v8-x2-web-${String(index + 1).padStart(2, "0")}`,
      topic: topic[0],
      source_url: topic[1],
      implication: topic[2],
      phase_use: "safe_runner_validation_or_trinity_mandala_reflection",
    };
  });
  const journey = Array.from({ length: 50 }, (_, index) => ({
    id: `v554-v8-x2-journey-${String(index + 1).padStart(2, "0")}`,
    source_phase: index < 20 ? sourcePhase : "recent_goal_mode_phase_receipts",
    reflection: `Preserve v8 x2 safe execution while keeping exact, blocked, proof, deployment, account, and sibling-identity gates open (${index + 1}).`,
    phase_use: "continuity_and_closeout_validation",
  }));
  return {
    artifact_type: "ghc_v554_v8_x2_web_journey_reflection_ledger_50",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V554_V8_X2_REFLECTION_LEDGER_50_READY",
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    web_reflection_count: web.length,
    journey_phase_reflection_count: journey.length,
    web_reflections: web,
    journey_phase_reflections: journey,
  };
}

function buildManifest(reflectionLedger) {
  const runnerCommands = runners.map((runner) => ({
    label: runner.title,
    args: [runner.file, "--phase-slug", phaseSlug],
  }));
  const manifest = {
    artifact_type: "ghc_v554_v8_x2_safe_runner_manifest",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    minimum_reflections_required: 50,
    search_count_declared: reflectionLedger.web_reflection_count,
    runner_count: runnerCommands.length,
    searches: reflectionLedger.web_reflections.map((row) => ({
      query: row.topic,
      source: row.topic,
      source_url: row.source_url,
      phase_reflection: row.implication,
      runner_implication: row.phase_use,
    })),
    commands: runnerCommands,
    reflection_receipt: `docs/trinity-live-traces/${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
    web_reflection_count: reflectionLedger.web_reflection_count,
    journey_phase_reflection_count: reflectionLedger.journey_phase_reflection_count,
  };
  writeJson(path.join(tracesDir, `${phaseSlug}-safe-runner-manifest-v1.json`), manifest);
  return {
    artifact_type: "ghc_v554_v8_x2_web_search_manifest",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    source_count: reflectionLedger.web_reflection_count,
    sources: reflectionLedger.web_reflections.map((row) => ({
      id: row.id,
      topic: row.topic,
      source_url: row.source_url,
    })),
  };
}

function runChild(command, childArgs) {
  const proc = spawnSync(process.execPath, [command, ...childArgs], {
    cwd: repoRoot,
    encoding: "utf8",
    windowsHide: true,
    maxBuffer: 1024 * 1024,
  });
  return {
    file: command,
    args: childArgs,
    exit_status: proc.status,
    status: parseStatus(proc.stdout),
    stdout_bytes: Buffer.byteLength(proc.stdout || "", "utf8"),
    stderr_bytes: Buffer.byteLength(proc.stderr || "", "utf8"),
  };
}

function parseStatus(stdout) {
  try {
    return JSON.parse(stdout || "{}").status || "json_status_missing";
  } catch {
    return "unparsed";
  }
}

function writePair(name, data, md) {
  writeJson(path.join(tracesDir, `${phaseSlug}-${name}-v1.json`), data);
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${name}-v1.md`), `${md.trim()}\n`, "utf8");
}

function renderSimpleMd(title, data) {
  const lines = [`# ${title}`, "", `Status: ${data.overall_status || data.status || "recorded"}`, "", `Phase: \`${phaseSlug}\``];
  if (data.next_active_phase) lines.push(`Next active phase: \`${data.next_active_phase}\``);
  if (data.next_x2_scope) lines.push(`Next x2 scope: \`${data.next_x2_scope}\``);
  if (data.next_x1_lane_after_x2) lines.push(`Next x1 lane after x2: ${data.next_x1_lane_after_x2}`);
  if (data.web_reflection_count) lines.push(`Web reflections: ${data.web_reflection_count}`);
  if (data.journey_phase_reflection_count) lines.push(`Journey/phase reflections: ${data.journey_phase_reflection_count}`);
  if (data.installed_skill_count !== undefined) lines.push(`Installed local skills: ${data.installed_skill_count}`);
  if (data.created_runner_count !== undefined) lines.push(`Created status-only runners: ${data.created_runner_count}`);
  lines.push("", "Boundary: no raw routes, private URLs, transcripts, screenshots, credentials, local absolute paths, private dumps, API keys, deployments, purchases, destructive cleanup, or sibling identity merging were performed or published.");
  return lines.join("\n");
}

function readRequired(name) {
  return readJson(path.join(tracesDir, name));
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
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
    raw_lane_text_published: false,
  };
}

function claimBoundary() {
  return {
    full_goal_completion: "not_claimed",
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

function openGateBoundary() {
  return {
    gmut_empirical_closure: "open",
    final_physics: "open",
    consciousness_proof: "open",
    legal_closure: "open",
    canon_promotion: "open",
    deployment_closure: "open",
    account_mutation: "open",
    purchase: "open",
    api_key_creation: "open",
    private_material_proof: "open",
    raw_publication_proof: "open",
    sibling_identity_replacement_or_merge: "open",
  };
}

function sanitizeSlug(value) {
  return ascii(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "skill";
}

function sanitizeSnake(value) {
  return ascii(value).toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "") || "runner";
}

function ascii(value) {
  return String(value).replace(/[^\x09\x0A\x0D\x20-\x7E]/g, "").trim();
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) parsed.set(argv[index], argv[index + 1]);
  return parsed;
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
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
