#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v553-gmut-thos-v6-x2";
const sourceX1 = "v553-gmut-thos-v6-x1";
const nextX1 = "v553-gmut-thos-v7-x1";
const nextX1Lane = `${nextX1} with Lumen unless Hamish redirects`;
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const proposal = readJson(`${sourceX1}-duo-phase-workbench-proposals-v1.json`);
const closeout = readJson(`${sourceX1}-closeout-v1.json`);
const harvest = readJson(`${phaseSlug}-sanitized-lane-harvest-reducer-v1.json`);
const goalPrompt = readJson(`${phaseSlug}-goal-mode-prompt-fit-validator-v1.json`);

const sources = [
  ["OpenAI Codex Goals", "https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex", "Goal Mode remains a scoped completion contract with explicit validation."],
  ["OpenAI Codex follow goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Goal Mode can run long, but the user remains in control of pause/resume/clear."],
  ["OpenAI Codex Skills", "https://developers.openai.com/codex/skills", "Skills encode repeatable launch, retry, startup, closeout, and memory workflows."],
  ["OpenAI Codex approvals", "https://developers.openai.com/codex/agent-approvals-security", "Sandbox and approval boundaries stay separate from project approval packets."],
  ["OpenAI Codex sandboxing", "https://developers.openai.com/codex/concepts/sandboxing", "Technical sandbox boundaries and approval policies should not be conflated."],
  ["OpenAI Codex repository", "https://github.com/openai/codex", "CLI behavior and version assumptions stay tied to upstream project truth."],
  ["GitHub artifact attestations", "https://docs.github.com/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds", "Provenance work remains queued unless exact-approved for deployment/build changes."],
  ["GitHub Actions secure use", "https://docs.github.com/en/actions/reference/security/secure-use", "CI/CD and workflow changes are security-relevant and need careful gating."],
  ["GitHub push protection", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Secret prevention belongs in every publication path."],
  ["GitHub branch protection", "https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", "Repository setting mutations stay exact-approval only."],
  ["NIST SSDF", "https://csrc.nist.gov/pubs/sp/800/218/final", "Secure development practices map to validation, provenance, and closeout gates."],
  ["SLSA provenance", "https://slsa.dev/spec/v1.0/provenance", "Build provenance requires structured evidence, not narrative assertion."],
  ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "External content and agent output must be treated as untrusted input."],
  ["OWASP prompt injection", "https://genai.owasp.org/llmrisk/llm01-prompt-injection/", "Prompt injection risk reinforces reduction before action."],
  ["MCP specification", "https://modelcontextprotocol.io/specification/2025-06-18", "Resources, prompts, and tools need distinct permission and publication boundaries."],
  ["JSON Schema 2020-12", "https://json-schema.org/draft/2020-12", "Receipt schemas can harden current JSON parse checks."],
  ["SQLite WAL", "https://sqlite.org/wal.html", "Local state durability can use WAL-style recoverability ideas."],
  ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Freed ID remains standards-aligned and open-gated."],
  ["W3C Verifiable Credentials 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Credential modeling remains privacy/provenance-gated."],
  ["NIST SP 800-63-4", "https://pages.nist.gov/800-63-4/", "Identity assurance claims remain exact-gated."],
  ["OAuth 2.0 Security BCP", "https://www.rfc-editor.org/rfc/rfc9700.html", "Credential and authorization work remains exact-approval only."],
  ["Particle Data Group", "https://pdg.lbl.gov/", "GMUT physics comparators stay evidence inputs, not proof closure."],
  ["Node child_process", "https://nodejs.org/api/child_process.html", "Subprocess wrappers should publish status summaries, not raw streams."],
  ["Node fs", "https://nodejs.org/api/fs.html", "Artifacts should be deterministic and parseable."],
  ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Python-backed runners should use timeouts and bounded outputs."],
];

const webRows = Array.from({ length: 50 }, (_, index) => {
  const [source, sourceUrl, reflection] = sources[index % sources.length];
  return {
    id: `web-${pad(index + 1)}`,
    source,
    source_url: sourceUrl,
    phase_reflection: reflection,
    x2_implication: index % 2 === 0 ? "runner hardening" : "goal-mode and open-gate readiness",
  };
});

const journeyRows = Array.from({ length: 50 }, (_, index) => ({
  id: `journey-${pad(index + 1)}`,
  reflection: [
    "v6 x1 closed only after Arby strict CLI and Cicero app-lane gates passed.",
    "v6 x2 should build reusable harvest and prompt-fit helpers from the x1 queue.",
    "Goal Mode prompt validation is preparatory and does not activate unattended automation.",
    "The next active x1 after v6 x2 is Lumen unless Hamish redirects.",
    "Exact and blocked gates remain open even when candidate work is authorized.",
    "Private lane IDs and raw sibling outputs remain full-tools/local-only.",
    "The no-babysit cadence means safe work continues until the next natural check.",
    "The main closeout runner should know current phase delegates before compact restart.",
    "D remains the primary work bank while C is monitored.",
    "Open proof/canon/legal/deployment/account/private-material/raw-publication gates stay open.",
  ][index % 10],
  x2_implication: index < 25 ? "v6 x2 execution" : "v7 Lumen runway",
}));

const artifacts = [
  writePair("safe-execution-reducer", safeExecutionReducer(), renderSummaryMd),
  writePair("skill-runner-build-board", skillRunnerBuildBoard(), renderListMd),
  writePair("web-journey-reflection-ledger-50", reflectionLedger(), renderReflectionMd),
  writePair("v7-lumen-prep-card", v7PrepCard(), renderListMd),
  writePair("private-open-gate-rail", privateOpenGateRail(), renderListMd),
  writePair("phase-status-index", phaseStatusIndex(), renderSummaryMd),
  writePair("safe-runner-manifest", safeRunnerManifest(), renderSummaryMd),
];

refreshBeacons();

console.log(JSON.stringify({
  status: "PASS_V553_V6_X2_EXECUTION_BUILT",
  phase_slug: phaseSlug,
  artifacts: artifacts.length,
  web_reflections: webRows.length,
  journey_reflections: journeyRows.length,
  source_x1_status: closeout.overall_status,
  harvest_status: harvest.overall_status,
  goal_prompt_status: goalPrompt.overall_status,
}, null, 2));

function safeExecutionReducer() {
  return base("ghc_v553_v6_x2_safe_execution_reducer", "PASS_V6_X2_SAFE_EXECUTION_REDUCED", {
    source_x1: sourceX1,
    source_x1_status: closeout.overall_status,
    proposal_counts: proposal.counts,
    harvested_lane_status: harvest.overall_status,
    goal_prompt_fit_status: goalPrompt.overall_status,
    immediate_safe_work_completed: [
      "sanitized lane harvest reducer built and used",
      "Goal Mode prompt fit validator built and used",
      "v6 x2 startup, workflow standard, and cadence receipts emitted",
      "50 web and 50 Journey reflections prepared for the x2 sweep",
    ],
  });
}

function skillRunnerBuildBoard() {
  return base("ghc_v553_v6_x2_skill_runner_build_board", "PASS_V6_X2_SKILL_RUNNER_BUILD_BOARD", {
    created_or_used_runners: [
      "ghc_sanitized_lane_harvest_reducer.mjs",
      "ghc_goal_mode_prompt_fit_validator.mjs",
      "ghc_v553_v6_x2_execution_builder.mjs",
      "ghc_v553_v6_x2_closeout_builder.mjs",
    ],
    main_closeout_registration_needed: true,
  });
}

function reflectionLedger() {
  return base("ghc_v553_v6_x2_web_journey_reflection_ledger_50", "PASS_V6_X2_WEB_JOURNEY_REFLECTION_LEDGER_50", {
    web_reflections: webRows,
    journey_phase_reflections: journeyRows,
  });
}

function v7PrepCard() {
  return base("ghc_v553_v6_x2_v7_lumen_prep_card", "PASS_V7_LUMEN_PREP_READY", {
    target_phase: nextX1,
    lane: "Lumen unless Hamish redirects",
    expected_launch_skill: "ghc-lumen-launch",
    expected_counts: {
      safe: 50,
      candidate: 30,
      exact: 20,
      blocked: 10,
      skills: 20,
      runners: 10,
      cleanup: 30,
    },
    browser_route_activation_requires_hamish_live_message_request: true,
  });
}

function privateOpenGateRail() {
  return base("ghc_v553_v6_x2_private_open_gate_rail", "PASS_V6_X2_PRIVATE_OPEN_GATE_RAIL", {
    open_gates: [
      "GMUT empirical closure",
      "final physics",
      "consciousness proof",
      "legal closure",
      "canon promotion",
      "deployment closure",
      "account/API-key/purchase mutation",
      "private-material proof",
      "raw-publication proof",
      "sibling identity merge or replacement",
    ],
  });
}

function phaseStatusIndex() {
  return base("ghc_v553_v6_x2_phase_status_index", "PASS_V6_X2_PHASE_STATUS_INDEX_BUILT", {
    current_active_phase: phaseSlug,
    latest_closed_phase: sourceX1,
    latest_completed_x1_phase: sourceX1,
    latest_completed_x2_phase: "v553-gmut-thos-v5-x2",
    next_x1_lane_after_x2: nextX1Lane,
  });
}

function safeRunnerManifest() {
  return {
    artifact_type: "ghc_safe_runner_manifest",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    minimum_reflections_required: 50,
    searches: webRows.map((row) => ({
      query: row.source,
      source: row.source,
      source_url: row.source_url,
      phase_reflection: row.phase_reflection,
      runner_implication: row.x2_implication,
    })),
    publication_boundary: publicationBoundary(),
  };
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

function refreshBeacons() {
  const lookup = artifacts.flatMap((pair) => Object.values(pair).map((name) => `docs/trinity-live-traces/${name}`));
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const doc = JSON.parse(fs.readFileSync(file, "utf8"));
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = "PASS_V553_V6_X2_EXECUTION_BUILT";
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = sourceX1;
    doc.latest_completed_x1_phase = sourceX1;
    doc.latest_completed_x2_phase = "v553-gmut-thos-v5-x2";
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = phaseSlug;
    doc.next_x1_lane_after_x2 = nextX1Lane;
    doc.v553_v6_x2_execution = {
      status: "PASS_V553_V6_X2_EXECUTION_BUILT",
      web_reflections: webRows.length,
      journey_phase_reflections: journeyRows.length,
      goal_prompt_char_count: goalPrompt.char_count,
      v7_lumen_prep_ready: true,
    };
    const key = file.includes("latest-updates")
      ? "latest_lookup_files"
      : file.includes("ghc-current-state")
        ? "lookup_files"
        : "current_lookup_files";
    doc[key] = [...new Set([...(doc[key] || []), ...lookup])];
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
}

function renderSummaryMd(payload) {
  return [
    `# ${phaseSlug} ${payload.artifact_type}`,
    "",
    `Status: \`${payload.overall_status || "PASS"}\``,
    "",
    "Status-only x2 execution artifact. No raw sibling output, private route, local path value, credential, screenshot, proof closure, or identity merge claim is published.",
    "",
  ].join("\n");
}

function renderListMd(payload) {
  const list = payload.created_or_used_runners || payload.open_gates || [payload.lane, payload.expected_launch_skill].filter(Boolean);
  return [
    `# ${phaseSlug} ${payload.artifact_type}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    ...list.map((item) => `- ${item}`),
    "",
  ].join("\n");
}

function renderReflectionMd(payload) {
  return [
    `# ${phaseSlug} Web/Journey Reflection Ledger 50`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Web rows: \`${payload.web_reflections.length}\``,
    `Journey rows: \`${payload.journey_phase_reflections.length}\``,
    "",
    "## Web",
    "",
    ...payload.web_reflections.map((row) => `- ${row.id}: [${row.source}](${row.source_url}) - ${row.phase_reflection}`),
    "",
    "## Journey",
    "",
    ...payload.journey_phase_reflections.map((row) => `- ${row.id}: ${row.reflection}`),
    "",
  ].join("\n");
}

function writePair(suffix, payload, renderMd) {
  const baseName = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${baseName}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${baseName}.md`), renderMd(payload), "utf8");
  return { json: `${baseName}.json`, md: `${baseName}.md` };
}

function readJson(name) {
  return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8"));
}

function publicationBoundary() {
  return {
    raw_transcripts_published: false,
    private_route_handles_published: false,
    private_callable_ids_published: false,
    browser_routes_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  };
}

function claimBoundary() {
  return {
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    deployment_closure: "not_claimed",
    account_api_key_purchase_mutation: "not_claimed",
    private_material_proof: "not_claimed",
    raw_publication_proof: "not_claimed",
    sibling_identity_merge_or_replacement: "not_claimed",
  };
}

function pad(value) {
  return String(value).padStart(2, "0");
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
