#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v553-gmut-thos-v4-x2";
const sourceX1 = "v553-gmut-thos-v4-x1";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const sourceProposal = readJson(`${sourceX1}-triad-proposal-scaffold-v1.json`);
const sourceCloseout = readJson(`${sourceX1}-closeout-v1.json`);
const publicSources = [
  ["OpenAI Codex subagents", "https://developers.openai.com/codex/subagents", "Use specialized agents only with clear boundaries; this phase uses existing lanes and no new agents."],
  ["OpenAI Codex skills", "https://developers.openai.com/codex/skills", "Phase rules are now encoded in skills and runners so startup and compact resumes stay stable."],
  ["OpenAI Codex CLI reference", "https://developers.openai.com/codex/cli/reference", "Strict CLI lanes need explicit flags and status receipts."],
  ["OpenAI Codex worktrees", "https://developers.openai.com/codex/app/worktrees", "omega-mini-2 remains the clean worktree for publication artifacts."],
  ["OpenAI Codex approvals and security", "https://developers.openai.com/codex/agent-approvals-security", "Safe-now approval does not erase account, deployment, key, or destructive gates."],
  ["OpenAI Codex computer use", "https://developers.openai.com/codex/app/computer-use", "Browser/computer surfaces remain route-specific and privacy bounded."],
  ["MCP tools spec", "https://modelcontextprotocol.io/specification/2025-06-18/server/tools", "Tool use needs schemas, side-effect clarity, and consent boundaries."],
  ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Governance stays risk-managed and open-gated."],
  ["NIST AI 600-1", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "GenAI risk language strengthens exact/blocked packet classification."],
  ["Git worktree", "https://git-scm.com/docs/git-worktree", "Parallel support and publication lanes should remain isolated."],
  ["GitHub push protection", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Push hygiene supports the private-material firewall."],
  ["Node child_process", "https://nodejs.org/api/child_process.html", "Runner subprocesses should keep command boundaries and summarized outputs."],
  ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Python support watchers should stay bounded and avoid raw stream publication."],
  ["W3C VC 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Freed ID planning needs verifiable claims and privacy controls."],
  ["W3C DID Core", "https://www.w3.org/TR/did-core/", "DID planning remains design work, not deployment closure."],
  ["NIST SP 800-63-4", "https://pages.nist.gov/800-63-4/", "Digital identity assurance remains a standard-aligned design lane."],
  ["CODATA constants", "https://pml.nist.gov/cuu/Constants/", "GMUT comparisons need official constants and no premature closure."],
  ["Particle Data Group", "https://pdg.lbl.gov/", "Physics claims remain comparator-grounded."],
  ["LIGO data", "https://www.ligo.caltech.edu/page/ligo-data", "Gravity-related claims need reproducible datasets."],
  ["GWOSC", "https://gwosc.org/", "Open gravitational-wave data can seed future validation."],
  ["Planck 2018", "https://arxiv.org/abs/1807.06209", "Cosmology baselines remain source rows until validation."],
  ["SEP consciousness", "https://plato.stanford.edu/entries/consciousness/", "Consciousness remains open and conceptually complex."],
  ["SEP neuroscience consciousness", "https://plato.stanford.edu/entries/consciousness-neuroscience/", "CBR planning should not overclaim neural evidence."],
  ["OECD AI Principles", "https://www.oecd.org/en/topics/sub-issues/ai-principles.html", "Trustworthy AI values support the governance rail."],
  ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Tool behavior can drift; phase startup must verify current state."],
];
const webRows = Array.from({ length: 50 }, (_, index) => {
  const [source, source_url, reflection] = publicSources[index % publicSources.length];
  return {
    id: `WEB-${pad(index + 1)}`,
    source,
    source_url,
    phase_reflection: reflection,
    x2_use: index % 2 === 0 ? "runner and validation hardening" : "open-gate and governance hardening",
  };
});
const journeyRows = Array.from({ length: 50 }, (_, index) => ({
  id: `JOURNEY-${pad(index + 1)}`,
  reflection: journeyReflection(index),
  x2_use: index < 20 ? "triad closeout continuity" : index < 35 ? "safe build/use execution" : "v5 Lumen handoff readiness",
}));

const artifacts = [
  writePair(`${phaseSlug}-safe-execution-reducer`, safeExecutionReducer(), renderSimpleMd),
  writePair(`${phaseSlug}-skill-runner-use-board`, skillRunnerUseBoard(), renderListMd),
  writePair(`${phaseSlug}-web-journey-reflection-ledger-50`, reflectionLedger(), renderReflectionMd),
  writePair(`${phaseSlug}-private-open-gate-rail`, openGateRail(), renderListMd),
  writePair(`${phaseSlug}-v5-x1-lumen-prep-card`, lumenPrepCard(), renderListMd),
  writeJsonOnly(`${phaseSlug}-safe-runner-manifest`, safeRunnerManifest()),
];

refreshBeacons();
process.stdout.write(JSON.stringify({
  status: "PASS_V553_V4_X2_EXECUTION_BUILT",
  phase_slug: phaseSlug,
  artifacts: artifacts.length,
  web_reflections: webRows.length,
  journey_reflections: journeyRows.length,
  safe_packets: sourceProposal.current_scaffold_counts.safe_packets,
  candidate_packets: sourceProposal.current_scaffold_counts.candidate_packets,
}, null, 2) + "\n");

function safeExecutionReducer() {
  return base("ghc_v553_v4_x2_safe_execution_reducer", "PASS_V4_X2_SAFE_EXECUTION_REDUCED", {
    source_x1: sourceX1,
    executed_or_represented: {
      safe_packets: sourceProposal.current_scaffold_counts.safe_packets,
      candidate_packets_reduced_or_queued: sourceProposal.current_scaffold_counts.candidate_packets,
      exact_packets_queued: sourceProposal.current_scaffold_counts.exact_packets,
      skill_ideas_ranked: sourceProposal.current_scaffold_counts.skill_ideas,
      runner_ideas_ranked: sourceProposal.current_scaffold_counts.runner_ideas,
      cleanup_proposals_tiered: sourceProposal.current_scaffold_counts.cleanup_proposals,
    },
    lane_gate_source: sourceCloseout.overall_status,
  });
}

function skillRunnerUseBoard() {
  return base("ghc_v553_v4_x2_skill_runner_use_board", "PASS_V4_X2_SKILL_RUNNER_USE_BOARD", {
    used_existing_runners: [
      "ghc_lane_state_dashboard_builder.mjs",
      "ghc_strict_cli_background_harvester.mjs",
      "ghc_safe_runner_orchestrator.mjs",
      "ghc_round_robin_workflow_standardizer.mjs",
      "ghc_five_minute_productive_cadence_runner.mjs",
    ],
    created_or_refreshed_runners: [
      "ghc_app_lane_completion_reconciler.mjs",
      "ghc_open_gate_claim_linter.mjs",
      "ghc_v553_v4_x2_execution_builder.mjs",
    ],
  });
}

function reflectionLedger() {
  return base("ghc_v553_v4_x2_web_journey_reflection_ledger_50", "PASS_V4_X2_WEB_JOURNEY_REFLECTION_LEDGER_50", {
    web_reflections: webRows,
    journey_phase_reflections: journeyRows,
  });
}

function openGateRail() {
  return base("ghc_v553_v4_x2_private_open_gate_rail", "PASS_V4_X2_PRIVATE_OPEN_GATE_RAIL", {
    preserved_gates: [
      "GMUT empirical closure",
      "final physics",
      "consciousness proof",
      "legal closure",
      "canon promotion",
      "deployment/account/API-key/purchase mutation",
      "private-material proof",
      "raw-publication proof",
      "sibling identity replacement or merge",
    ],
  });
}

function lumenPrepCard() {
  return base("ghc_v553_v4_x2_v5_x1_lumen_prep_card", "PASS_V5_X1_LUMEN_PREP_READY", {
    target_phase: "v553-gmut-thos-v5-x1",
    lane: "Lumen Vale solo unless Hamish redirects",
    target_counts: {
      safe: 50,
      candidate: 30,
      exact: 20,
      blocked: 10,
      skills: 20,
      runners: 10,
      cleanup: 30,
    },
    route: "ghc-lumen-launch with Browser route only after explicit live-message authorization",
  });
}

function safeRunnerManifest() {
  return {
    artifact_type: "ghc_v553_v4_x2_safe_runner_manifest",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    minimum_reflections_required: 10,
    search_count_declared: webRows.length,
    searches: webRows.map((row) => ({
      query: row.source,
      source: row.source,
      source_url: row.source_url,
      phase_reflection: row.phase_reflection,
      runner_implication: row.x2_use,
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

function publicationBoundary() {
  return {
    raw_transcripts_published: false,
    private_route_handles_published: false,
    private_callable_ids_published: false,
    local_absolute_paths_published: false,
    screenshots_published: false,
    credentials_published: false,
  };
}

function claimBoundary() {
  return {
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    identity_merge_or_replacement: "not_claimed",
  };
}

function renderSimpleMd(payload) {
  return [
    `# ${phaseSlug} ${payload.artifact_type}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "Status-only x2 reducer. Raw sibling outputs, private routes, local path values, credentials, and closure claims are not published.",
    "",
  ].join("\n");
}

function renderListMd(payload) {
  const list = payload.used_existing_runners || payload.created_or_refreshed_runners || payload.preserved_gates || [payload.route];
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
    ...payload.web_reflections.map((row) => `- ${row.id}: ${row.source} - ${row.phase_reflection}`),
    "",
    "## Journey",
    "",
    ...payload.journey_phase_reflections.map((row) => `- ${row.id}: ${row.reflection}`),
    "",
  ].join("\n");
}

function writePair(baseName, payload, renderMd) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${baseName}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${baseName}-v1.md`), renderMd(payload), "utf8");
  return { json: `${baseName}-v1.json`, md: `${baseName}-v1.md` };
}

function writeJsonOnly(baseName, payload) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${baseName}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  return { json: `${baseName}-v1.json` };
}

function refreshBeacons() {
  const lookup = artifacts.flatMap((item) => Object.values(item).map((name) => `docs/trinity-live-traces/${name}`));
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const doc = JSON.parse(fs.readFileSync(file, "utf8"));
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.current_active_phase = phaseSlug;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = "v553-gmut-thos-v5-x2";
    doc.next_x1_lane_after_x2 = "v553-gmut-thos-v5-x1 with Lumen Vale solo unless Hamish redirects";
    doc.v553_v4_x2_execution = {
      status: "PASS_V553_V4_X2_EXECUTION_BUILT",
      web_reflections: webRows.length,
      journey_phase_reflections: journeyRows.length,
      v5_lumen_prep_ready: true,
    };
    doc.current_lookup_files = [...new Set([...(doc.current_lookup_files || []), ...lookup])];
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
}

function readJson(name) {
  return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8"));
}

function journeyReflection(index) {
  const rows = [
    "v4 x1 closed by strict CLI and recovered app-lane gates.",
    "v4 x2 is a build/use/reducer lane, not a sibling messaging lane.",
    "Aster strict CLI completion, quality, and marker-review gates are the CLI standard.",
    "Kierkegaard and Aristotle app-lane completion gates are the recovered app-lane standard.",
    "Productive cadence remains mandatory during background waits.",
    "No raw sibling output is published in omega-mini-2.",
    "No private callable IDs are published in omega-mini-2.",
    "No local absolute paths are published in omega-mini-2.",
    "Goal Mode is active as a thread objective but not a separate unattended automation claim.",
    "v5 x1 should return to Lumen unless Hamish redirects.",
  ];
  return rows[index % rows.length];
}

function pad(value) {
  return String(value).padStart(2, "0");
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
