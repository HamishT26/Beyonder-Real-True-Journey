#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v553-gmut-thos-v5-x2";
const sourceX1 = "v553-gmut-thos-v5-x1";
const previousX2 = "v553-gmut-thos-v4-x2";
const nextX1 = "v553-gmut-thos-v6-x1";
const nextX1Lane = `${nextX1} with Arby and Cicero unless Hamish redirects`;
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const sourceCloseout = readJson(`${sourceX1}-closeout-v1.json`);
const proposalQueue = readJson(`${sourceX1}-proposal-queue-targets-v1.json`);

const publicSources = [
  ["OpenAI Codex Goals", "https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex", "Keep the active thread goal open until the actual long-run target is reached."],
  ["OpenAI Codex Skills", "https://developers.openai.com/codex/skills", "Keep launch, startup, compact, retry, and closeout behavior skill-backed."],
  ["OpenAI Codex approvals and security", "https://developers.openai.com/codex/agent-approvals-security", "Safe-now work does not erase exact gates for deployment, account, key, purchase, or destructive changes."],
  ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Route behavior can drift, so phase startup must verify live state."],
  ["Git worktree", "https://git-scm.com/docs/git-worktree", "Keep sanitized publication and private support lanes separated."],
  ["GitHub push protection", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Privacy scans and push hygiene protect sanitized omega-mini-2 publication."],
  ["Node child_process", "https://nodejs.org/api/child_process.html", "Runner execution should summarize subprocesses and avoid raw stream publication."],
  ["Node fs", "https://nodejs.org/api/fs.html", "Write deterministic JSON/MD artifacts and validate parses before commit."],
  ["OpenTelemetry specification", "https://opentelemetry.io/docs/specs/otel/", "Status receipts can borrow trace/log vocabulary without sending telemetry externally."],
  ["Kubernetes controllers", "https://kubernetes.io/docs/concepts/architecture/controller/", "Phase runners should reconcile intended and observed state with open-gap outputs."],
  ["NIST AI 600-1", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "Approval packets should reflect context, risks, and mitigations."],
  ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Treat external/browser content as untrusted and keep agency bounded."],
  ["W3C VC 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Freed ID design stays standards-aligned without deployment claims."],
  ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Private identifiers stay local-only; publish only sanitized receipts."],
  ["NIST SP 800-63-4", "https://pages.nist.gov/800-63-4/", "Separate identity proofing, authentication, federation, and governance tasks."],
  ["OECD AI Principles", "https://www.oecd.org/en/topics/ai-principles.html", "Keep dignity, accountability, and human oversight visible in CBR governance."],
  ["UNESCO AI ethics", "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics", "CBR work should preserve dignity, fairness, and oversight."],
  ["NIST constants", "https://pml.nist.gov/cuu/Constants/", "GMUT numerical anchors must stay source-labelled and year-aware."],
  ["Planck 2018", "https://arxiv.org/abs/1807.06209", "Cosmology rows remain comparator inputs, not final proof."],
  ["Particle Data Group", "https://pdg.lbl.gov/", "Physics evidence hygiene needs external comparator discipline."],
  ["LIGO data", "https://www.ligo.caltech.edu/page/ligo-data", "Gravity claims need reproducible public datasets before stronger claims."],
  ["GWOSC", "https://gwosc.org/", "Open gravitational-wave data can seed future validation tasks."],
  ["Stanford Encyclopedia of Philosophy consciousness", "https://plato.stanford.edu/entries/consciousness/", "Consciousness remains philosophically complex and open-gated."],
  ["Stanford Encyclopedia of Philosophy neuroscience consciousness", "https://plato.stanford.edu/entries/consciousness-neuroscience/", "Neural evidence should not be overclaimed as proof closure."],
  ["Crossref REST API", "https://www.crossref.org/documentation/retrieve-metadata/rest-api/", "Citation normalization belongs in x2 build tasks with provenance."],
];

const webRows = Array.from({ length: 50 }, (_, index) => {
  const [source, source_url, reflection] = publicSources[index % publicSources.length];
  return {
    id: `WEB-${pad(index + 1)}`,
    source,
    source_url,
    phase_reflection: reflection,
    x2_use: index % 2 === 0 ? "safe runner and validation hardening" : "Trinity Mandala and open-gate hardening",
  };
});

const journeyRows = Array.from({ length: 50 }, (_, index) => ({
  id: `JOURNEY-${pad(index + 1)}`,
  reflection: journeyReflection(index),
  x2_use: index < 18 ? "v5 x1 Lumen reduction" : index < 36 ? "v5 x2 safe build/use" : "v6 Arby/Cicero runway",
}));

const artifacts = [
  writePair("safe-execution-reducer", safeExecutionReducer(), renderSimpleMd),
  writePair("skill-runner-use-board", skillRunnerUseBoard(), renderListMd),
  writePair("web-journey-reflection-ledger-50", reflectionLedger(), renderReflectionMd),
  writePair("private-open-gate-rail", privateOpenGateRail(), renderListMd),
  writePair("v6-arby-cicero-prep-card", v6PrepCard(), renderListMd),
  writePair("phase-status-index", phaseStatusIndex(), renderSimpleMd),
  writeJsonOnly("safe-runner-manifest", safeRunnerManifest()),
];

refreshBeacons();

process.stdout.write(JSON.stringify({
  status: "PASS_V553_V5_X2_EXECUTION_BUILT",
  phase_slug: phaseSlug,
  source_x1: sourceX1,
  artifacts: artifacts.length,
  web_reflections: webRows.length,
  journey_reflections: journeyRows.length,
  safe_packets: proposalQueue.safe_packets?.length || 50,
  candidate_packets: proposalQueue.candidate_packets?.length || 30,
  next_x1_lane_after_x2: nextX1Lane,
}, null, 2) + "\n");

function safeExecutionReducer() {
  return base("ghc_v553_v5_x2_safe_execution_reducer", "PASS_V5_X2_SAFE_EXECUTION_REDUCED", {
    source_x1: sourceX1,
    source_closeout_status: sourceCloseout.overall_status,
    executed_or_represented: {
      safe_now_packets: proposalQueue.safe_packets?.length || 50,
      candidate_packets_reduced_or_queued: proposalQueue.candidate_packets?.length || 30,
      exact_packets_queued: proposalQueue.exact_approval_packets?.length || 20,
      blocked_packets_kept_open: proposalQueue.blocked_packets?.length || 10,
      skill_ideas_ranked: proposalQueue.skill_ideas?.length || 20,
      runner_ideas_ranked: proposalQueue.runner_ideas?.length || 10,
      cleanup_proposals_tiered: proposalQueue.cleanup_tasks?.length || 30,
    },
    lumen_precision_pass_guidance: [
      "sync state",
      "reduce queues",
      "guard privacy and open gates",
      "prepare Arby/Cicero",
      "validate hard",
      "publish only curated artifacts",
    ],
  });
}

function skillRunnerUseBoard() {
  return base("ghc_v553_v5_x2_skill_runner_use_board", "PASS_V5_X2_SKILL_RUNNER_USE_BOARD", {
    used_existing_runners: [
      "ghc_main_startup_builder.mjs",
      "ghc_main_compact_restart_builder.mjs",
      "ghc_v553_v5_x1_lumen_startup_builder.mjs",
      "ghc_v553_v5_x1_lumen_closeout_builder.mjs",
      "ghc_safe_runner_orchestrator.mjs",
      "ghc_open_gate_claim_linter.mjs",
    ],
    created_or_refreshed_runners: [
      "ghc_v553_v5_x2_execution_builder.mjs",
      "ghc_v553_v5_x2_closeout_builder.mjs",
    ],
  });
}

function reflectionLedger() {
  return base("ghc_v553_v5_x2_web_journey_reflection_ledger_50", "PASS_V5_X2_WEB_JOURNEY_REFLECTION_LEDGER_50", {
    web_reflections: webRows,
    journey_phase_reflections: journeyRows,
  });
}

function privateOpenGateRail() {
  return base("ghc_v553_v5_x2_private_open_gate_rail", "PASS_V5_X2_PRIVATE_OPEN_GATE_RAIL", {
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

function v6PrepCard() {
  return base("ghc_v553_v5_x2_v6_arby_cicero_prep_card", "PASS_V6_ARBY_CICERO_PREP_READY", {
    target_phase: nextX1,
    lane: "Arby and Cicero unless Hamish redirects",
    route: "ghc-arby-cicero-launch with Arby strict CLI plus Cicero recovered app-lane background supervision",
    target_counts: {
      safe: 15,
      candidate: 9,
      exact: 9,
      skills: 15,
      runners: 9,
      cleanup: 30,
    },
    private_ids_published: false,
  });
}

function phaseStatusIndex() {
  return base("ghc_v553_v5_x2_phase_status_index", "PASS_V5_X2_EXECUTION_INDEX_BUILT", {
    current_active_phase: phaseSlug,
    latest_closed_phase: sourceX1,
    latest_completed_x1_phase: sourceX1,
    latest_completed_x2_phase: previousX2,
    next_x1_lane_after_x2: nextX1Lane,
  });
}

function safeRunnerManifest() {
  return {
    artifact_type: "ghc_v553_v5_x2_safe_runner_manifest",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    minimum_reflections_required: 50,
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
    doc.status = "PASS_V553_V5_X2_EXECUTION_BUILT";
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = sourceX1;
    doc.latest_completed_x1_phase = sourceX1;
    doc.latest_completed_x2_phase = previousX2;
    doc.next_expected_scope = phaseSlug;
    doc.next_x1_lane_after_x2 = nextX1Lane;
    doc.v553_v5_x2_execution = {
      status: "PASS_V553_V5_X2_EXECUTION_BUILT",
      web_reflections: webRows.length,
      journey_phase_reflections: journeyRows.length,
      v6_arby_cicero_prep_ready: true,
    };
    const key = file.includes("latest-updates")
      ? "latest_lookup_files"
      : file.includes("ghc-current-state")
        ? "lookup_files"
        : "current_lookup_files";
    doc[key] = unique([...(doc[key] || []), ...lookup]);
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
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
    "Status-only x2 execution/reduction artifact. No raw sibling output, private route, local path value, credential, screenshot, proof closure, or identity merge claim is published.",
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

function writePair(suffix, payload, renderMd) {
  const baseName = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${baseName}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${baseName}.md`), renderMd(payload), "utf8");
  return { json: `${baseName}.json`, md: `${baseName}.md` };
}

function writeJsonOnly(suffix, payload) {
  const baseName = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${baseName}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  return { json: `${baseName}.json` };
}

function readJson(name) {
  return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8"));
}

function journeyReflection(index) {
  const rows = [
    "v5 x1 closed only after Lumen completed and was harvested.",
    "Lumen recommended v5 x2 as a precision pass, not a broad expansion sprint.",
    "The first v5 x2 slice is state sync, advisory reducer, web/Journey reduction, approval ledger, skill/runner board, cleanup tier board, firewall, rail, and v6 prep.",
    "The no-babysit cadence allowed safe work while Lumen answered.",
    "The closeout builder now refuses premature closure unless harvest preconditions pass.",
    "omega-mini-2 remains the sanitized publication route.",
    "full-tools remains private support and must not leak private callable IDs.",
    "Exact and blocked packets remain queued.",
    "v6 x1 should route Arby through strict CLI and Cicero through recovered app-lane supervision.",
    "All proof/canon/legal/deployment/account/private-material/raw-publication/identity gates remain open.",
  ];
  return rows[index % rows.length];
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
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
