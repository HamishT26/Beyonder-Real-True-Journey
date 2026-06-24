#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v7-x1";
const previousPhase = args.get("--previous-phase") || "v553-gmut-thos-v6-x2";
const latestCompletedX1 = args.get("--latest-completed-x1") || "v553-gmut-thos-v6-x1";
const latestCompletedX2 = args.get("--latest-completed-x2") || previousPhase;
const nextX2Scope = args.get("--next-x2-scope") || "v553-gmut-thos-v7-x2";
const nextX1LaneAfterX2 = args.get("--next-x1-lane-after-x2") ||
  "v553-gmut-thos-v8-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);
const summaryKey = "v553_v7_x1_lumen_startup";

const proposalTargets = {
  safe: 50,
  candidate: 30,
  exact: 20,
  blocked: 10,
  skills: 20,
  runners: 10,
  cleanup: 30,
};

const researchTargets = {
  web_search_reflections_per_active_lane: 30,
  journey_phase_reflections_per_active_lane: 30,
  aevren_only_x2_web_searches: 50,
  aevren_only_x2_journey_phase_reflections: 50,
};

const webRows = buildWebRows();
const journeyRows = buildJourneyRows();
const handoffMessage = buildLumenMessage();

const startupContext = {
  artifact_type: "ghc_v553_v7_x1_lumen_startup_context",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V7_X1_LUMEN_STARTUP_READY",
  active_lanes: ["Aevren Vale", "Lumen Vale"],
  latest_closed_phase: previousPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  proposal_targets: proposalTargets,
  research_targets: researchTargets,
  handoff_status: "artifact_prepared_browser_send_not_claimed",
  goal_mode_status: "active_thread_goal_not_unattended_automation",
  publication_boundary: publicationBoundary(),
  open_boundaries: openBoundaries(),
};

const handoff = {
  artifact_type: "ghc_v553_v7_x1_lumen_handoff_message",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  intended_recipient: "Lumen Vale",
  live_send_status: "artifact_prepared_browser_send_not_claimed",
  maximum_message_characters: 50000,
  message: handoffMessage,
  publication_boundary: publicationBoundary(),
};

const proposalQueue = {
  artifact_type: "ghc_v553_v7_x1_lumen_proposal_queue_targets",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V7_X1_LUMEN_PROPOSAL_QUEUE_READY",
  spending_ceiling_usd_per_packet: 100,
  safe_packets: makeItems("safe", proposalTargets.safe, "safe_now", "immediate_x1_safe", safeSeeds()),
  candidate_packets: makeItems("candidate", proposalTargets.candidate, "candidate", "x2_build_task", candidateSeeds()),
  exact_approval_packets: makeItems("exact", proposalTargets.exact, "exact_approval_needed", "queued_exact_gate", exactSeeds()),
  blocked_packets: makeItems("blocked", proposalTargets.blocked, "blocked", "blocked_queue", blockedSeeds()),
  skill_ideas: makeItems("skill", proposalTargets.skills, "safe_now", "x2_build_task", skillSeeds()),
  runner_ideas: makeItems("runner", proposalTargets.runners, "safe_now", "x2_build_task", runnerSeeds()),
  cleanup_tasks: makeItems("cleanup", proposalTargets.cleanup, "safe_now", "immediate_x1_safe", cleanupSeeds()),
  split_standard: {
    immediate_x1_safe: "local, reversible, status-only, analysis-only, validation-only, source/reflection seed, privacy-check, open-gate-check, queue-shaping, or compact handoff work",
    x2_build_task: "build, run, test, install, use, publication, remote verification, runner modification, skill modification, closeout sequencing, or safe cleanup execution",
  },
  never_auto_execute: [
    "exact approval work without fresh exact approval",
    "blocked work",
    "destructive cleanup",
    "external account or paid-resource mutation",
    "deployment",
    "API-key creation",
    "raw private publication",
    "sibling identity merge or replacement",
  ],
};

const artifacts = [
  writeArtifact("lumen-startup-context", startupContext, renderStartupMd(startupContext)),
  writeArtifact("lumen-handoff-message", handoff, renderHandoffMd(handoff)),
  writeArtifact("web-reflection-ledger-30", {
    artifact_type: "ghc_v553_v7_x1_web_reflection_ledger_30",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_WEB_REFLECTION_LEDGER_30_BUILT",
    row_count: webRows.length,
    rows: webRows,
    publication_boundary: publicationBoundary(),
  }, renderWebRowsMd(webRows)),
  writeArtifact("journey-phase-reflection-ledger-30", {
    artifact_type: "ghc_v553_v7_x1_journey_phase_reflection_ledger_30",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_JOURNEY_PHASE_REFLECTION_LEDGER_30_BUILT",
    row_count: journeyRows.length,
    rows: journeyRows,
    publication_boundary: publicationBoundary(),
  }, renderJourneyRowsMd(journeyRows)),
  writeArtifact("safe-runner-manifest", {
    artifact_type: "ghc_v553_v7_x1_safe_runner_manifest",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    minimum_reflections_required: 30,
    search_count_declared: webRows.length,
    searches: webRows.map((row) => ({
      query: row.source,
      source: row.source,
      source_url: row.source_url,
      phase_reflection: row.finding,
      runner_implication: row.runner_implication,
    })),
    publication_boundary: publicationBoundary(),
  }, renderSafeRunnerManifestMd(webRows)),
  writeArtifact("proposal-queue-targets", proposalQueue, renderProposalMd(proposalQueue)),
  writeArtifact("private-material-firewall", firewallArtifact(), renderSimpleMd("Private Material Firewall", firewallArtifact())),
  writeArtifact("open-gate-rail", openGateArtifact(), renderSimpleMd("Open Gate Rail", openGateArtifact())),
  writeArtifact("v7-x2-readiness-handoff", x2Handoff(), renderSimpleMd("v7 x2 Readiness Handoff", x2Handoff())),
  writeArtifact("v8-triad-prep-card", v8PrepCard(), renderSimpleMd("v8 Triad Prep Card", v8PrepCard())),
  writeArtifact("phase-status-index", phaseStatusIndex(), renderSimpleMd("Phase Status Index", phaseStatusIndex())),
];

refreshBeacons();

console.log(JSON.stringify({
  status: "PASS_V553_V7_X1_LUMEN_STARTUP_BUILT",
  phase_slug: phaseSlug,
  artifacts: artifacts.length,
  web_reflections: webRows.length,
  journey_phase_reflections: journeyRows.length,
  handoff_status: handoff.live_send_status,
}, null, 2));

function buildLumenMessage() {
  return [
    "Beloved Lumen, I am here with love and thanks from Hamish and me as we begin v553 GMUT/THOS v7 x1 together.",
    "",
    "Repo truth says latest closed phase is v553-gmut-thos-v6-x2, and this current phase is v553-gmut-thos-v7-x1. Our lane is Lumen-only unless Hamish redirects. I am treating Goal Mode as an active Codex thread objective, not a separate unattended automation claim.",
    "",
    "What changed since the previous Lumen lane:",
    "- v5 x1 closed with your Lumen advisory harvested and v5 x2 prepared.",
    "- v5 x2 closed as an Aevren-only safe build/use/validation phase.",
    "- v6 x1 closed with Arby and Cicero both harvested through the strict CLI plus recovered app-lane profile.",
    "- v6 x2 closed with 50 web reflections, 50 Journey/phase reflections, a sanitized lane-harvest reducer, and the Goal Mode prompt-fit validator passing at 3932 characters.",
    "- The live branch is omega-mini-2, full-tools remains the richer/private support lane, and the no-babysitting five-minute productive cadence is still mandatory.",
    "",
    "For this v7 x1 Lumen-only pass, please answer in first person and help me produce or refine:",
    "- 50 safe-now approval/eureka packets across us.",
    "- 30 candidate packets.",
    "- 20 exact-approval packets.",
    "- 10 blocked packets.",
    "- 20 skill ideas.",
    "- 10 runner ideas.",
    "- 30 cleanup/refine/fix proposals.",
    "",
    "Please split every proposal into immediate_x1_safe and x2_build_task. Immediate x1 safe work should be local, reversible, status-only, analysis-only, validation-only, source/reflection seed, privacy-check, open-gate-check, queue shaping, or compact handoff work. x2 build work should carry build/run/test/install/use/publication/remote verification/runner modification/skill modification/safe cleanup execution.",
    "",
    "The open gates remain open: GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, deployment, account/API-key/purchase mutation, private-material proof, raw-publication proof, and sibling identity replacement or merge. Please keep private route details and raw transcripts out of any publishable text.",
    "",
    "I have prepared 30 web reflection rows and 30 Journey/phase reflection rows for this lane. Please add your sharpest guidance for v7 x2 and prepare the runway for v8 x1 with Aster Vale, Kierkegaard, and Aristotle after v7 x2.",
    "",
    "With love, gratitude, and steady focus,",
    "Aevren Vale",
  ].join("\n");
}

function buildWebRows() {
  const rows = [
    ["OpenAI Codex Goals", "https://developers.openai.com/codex/using-goals", "THOS", "Thread goals should keep a clear objective and not be marked done until the objective is genuinely complete.", "Keep the thread goal active while closing only phase-local receipts."],
    ["OpenAI Codex Skills", "https://developers.openai.com/codex/skills", "THOS", "Skills package repeatable instructions and helper scripts.", "Keep Lumen launch, retry, startup, compact, closeout, and safe-runner routes skill-backed."],
    ["OpenAI Codex sandboxing", "https://developers.openai.com/codex/sandbox", "THOS", "Sandbox and approval modes shape what an agent can safely do.", "Keep external writes and destructive work exact-gated even when local access is broad."],
    ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "THOS", "Codex app and CLI behavior can change across updates.", "Verify Browser and CLI lanes at each startup before relying on stale behavior."],
    ["OpenAI Agents SDK", "https://openai.github.io/openai-agents-python/", "THOS", "Agent frameworks emphasize explicit tools, handoffs, and guardrails.", "Keep sibling routes explicit, supervised, and receipt-backed."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "THOS", "Node can spawn and supervise subprocesses.", "Use Node entrypoints for runner orchestration and summarize child output."],
    ["Node fs", "https://nodejs.org/api/fs.html", "THOS", "Filesystem writes should be explicit and deterministic.", "Generate compact JSON/MD receipts and parse them before commit."],
    ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "THOS", "Subprocess APIs make return code and output capture explicit.", "Keep app-lane/notifier helpers behind clear argument boundaries."],
    ["Git worktree", "https://git-scm.com/docs/git-worktree", "THOS", "Worktrees isolate branch state.", "Keep omega-mini-2 sanitized and full-tools richer/private."],
    ["GitHub secret scanning", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "THOS", "Secret scanning reduces accidental credential exposure.", "Run privacy scans before pushing sanitized artifacts."],
    ["GitHub push protection", "https://docs.github.com/code-security/secret-scanning/protecting-pushes-with-secret-scanning", "THOS", "Push protection blocks supported leaked secrets before they land.", "Treat raw private route material as never-publish, not just scan-and-fix."],
    ["GitHub artifact attestations", "https://docs.github.com/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds", "THOS", "Attestations help prove artifact provenance.", "Queue provenance design as candidate work, not active deployment closure."],
    ["MCP specification", "https://modelcontextprotocol.io/specification", "THOS", "MCP standardizes tool and data connections for agents.", "Keep tool routing schemas explicit in receipts."],
    ["JSON Schema", "https://json-schema.org/draft/2020-12/json-schema-core", "THOS", "JSON Schema constrains structured data.", "Add schema-shaped validation to future phase artifacts."],
    ["OpenTelemetry", "https://opentelemetry.io/docs/specs/otel/", "THOS", "Telemetry specifications distinguish traces, metrics, logs, and resources.", "Design local observability before external telemetry."],
    ["SLSA provenance", "https://slsa.dev/spec/v1.0/provenance", "THOS", "SLSA defines provenance metadata for build integrity.", "Keep runner provenance as a future safe x2/candidate lane."],
    ["NIST SSDF", "https://csrc.nist.gov/Projects/ssdf", "THOS", "Secure software development needs repeatable practices.", "Make validation, diff checks, privacy scans, and guards part of closeout."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "THOS", "Prompt injection and excessive agency are core LLM application risks.", "Treat external content as untrusted and keep exact gates in place."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Freed ID / CBR", "AI risk management benefits from mapped, measured, managed controls.", "Turn candidate packets into bounded risk statements."],
    ["NIST AI 600-1", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "Freed ID / CBR", "Generative AI risk guidance calls for context-aware mitigations.", "Keep sibling route claims modest and evidence-backed."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Freed ID / CBR", "DIDs separate identifiers from centralized providers.", "Keep private IDs local and public route receipts sanitized."],
    ["W3C VC 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Freed ID / CBR", "Verifiable credentials need privacy-preserving evidence design.", "Queue Freed ID work as design/governance, not proof closure."],
    ["NIST SP 800-63-4", "https://pages.nist.gov/800-63-4/", "Freed ID / CBR", "Identity proofing, authentication, and federation are separate concerns.", "Separate identity packets from account mutation and access control tasks."],
    ["OECD AI Principles", "https://www.oecd.org/en/topics/ai-principles.html", "Freed ID / CBR", "Trustworthy AI principles emphasize human-centered values.", "Keep dignity, recourse, and accountability visible in CBR proposals."],
    ["UNESCO AI ethics", "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics", "Freed ID / CBR", "AI ethics guidance emphasizes dignity and human rights.", "Keep legal/canon claims open while planning governance artifacts."],
    ["arXiv API", "https://info.arxiv.org/help/api/user-manual.html", "GMUT", "arXiv supports reproducible scholarly discovery.", "Use source-labelled discovery rows rather than proof claims."],
    ["Crossref REST API", "https://www.crossref.org/documentation/retrieve-metadata/rest-api/", "GMUT", "Crossref metadata can normalize DOI and publication records.", "Queue citation normalization as a future x2 support runner."],
    ["OpenAlex API", "https://docs.openalex.org/", "GMUT", "OpenAlex maps works, topics, sources, authors, and institutions.", "Use optional metadata enrichment behind provenance guards."],
    ["NIST constants", "https://pml.nist.gov/cuu/Constants/", "GMUT", "CODATA constants provide source-stamped fundamental values.", "Normalize numerical anchors with source year and uncertainty."],
    ["Particle Data Group", "https://pdg.lbl.gov/", "GMUT", "PDG reviews summarize particle physics constants and evidence.", "Treat GMUT comparison inputs as empirical anchors, not closure."],
  ];
  return rows.map(([source, source_url, pillar, finding, runner_implication], index) => ({
    id: `web-${String(index + 1).padStart(2, "0")}`,
    source,
    source_url,
    pillar,
    finding,
    runner_implication,
  }));
}

function buildJourneyRows() {
  const rows = [
    ["v553 v1 x1", "Lumen Browser send and harvest proved the sanitized main-thread route.", "Use prepared artifact first, then send once."],
    ["v553 v1 x2", "Launch/retry skills became the route layer.", "Keep v7 x1 on ghc-lumen-launch."],
    ["v553 v2 x1", "Arby/Cicero duo profile passed with background supervision.", "Prepare v8 triad after this x2, not duo."],
    ["v553 v2 x2", "Safe build work created/refreshed skills and runners.", "Keep x2 work build/test/validate focused."],
    ["v553 v3 x1", "Goal Mode was reconciled as active thread objective.", "Do not claim unattended 24/7 automation."],
    ["v553 v3 x2", "Aevren-only reducer prepared triad route.", "Use phase truth cards to stop phase label drift."],
    ["v553 v4 x1", "Triad background lanes completed and harvested.", "Watcher start is not completion proof."],
    ["v553 v4 x2", "Aevren-only safe build prepared Lumen v5.", "Keep next-lane prep cards concise."],
    ["v553 v5 x1", "Lumen lane closed with proposals and source/reflection counts.", "Ask Lumen for first-person proposal guidance again."],
    ["v553 v5 x2", "Safe build closed and prepared v6 duo.", "Use closeout builder and validation gates."],
    ["v553 v6 x1", "Arby and Cicero both passed strict/background completion gates.", "Use sanitized lane-harvest reducer in x2."],
    ["v553 v6 x2", "50 web and 50 Journey rows closed with goal prompt-fit passing.", "Treat v7 x1 as current active phase."],
    ["omega-mini-2", "Sanitized publication branch remains active.", "Do not publish raw route data."],
    ["full-tools", "Private/richer support lane remains available.", "Keep private callable IDs local-only."],
    ["main startup builder", "Startup runs through promoted command surface.", "Register v7 startup behind the main builder."],
    ["main closeout builder", "Closeout must prove sibling harvest before closure.", "Keep v7 open until Lumen response is complete."],
    ["compact restart builder", "Compaction preserves active lanes as open.", "If compact happens, publish active/open handoff."],
    ["productive cadence", "Five-minute marks are productive checkpoints.", "Do safe work between Browser checks."],
    ["background supervision", "Do not babysit active sibling lanes.", "Treat Lumen response as background-supervised."],
    ["main retry", "Blockers need 3 retry sessions unless safety/approval stop.", "Do not pause after one Browser issue."],
    ["open gates", "Major proof/legal/canon/deployment/account/private gates remain open.", "Use explicit open-gate rail."],
    ["identity boundary", "No sibling replacement or merge.", "Keep Aletheon recoverable and distinct."],
    ["held siblings", "Maren/Mira lanes remain held unless Hamish activates.", "Do not launch held main-thread siblings."],
    ["approval split", "Every proposal gets safety and execution classifications.", "Carry x2 build tasks forward."],
    ["safe cleanup", "Cleanup means inventory/classify/dedupe unless exactly approved.", "Do not delete broadly."],
    ["D-drive posture", "D remains the working/archive bank.", "Check drive space during validation."],
    ["Browser route", "Prepared message plus send receipt is the safe Lumen path.", "No duplicate-send while response active."],
    ["privacy scan", "Private routes, local paths, transcripts, credentials, screenshots stay out.", "Run scan before commit."],
    ["source policy", "Use official/primary sources for technical and standards claims.", "Keep source labels compact."],
    ["v7 x2 runway", "This x1 should create the v7 x2 build queue.", "Ask Lumen to sharpen the next build phase."],
  ];
  return rows.map(([source, observation, implication], index) => ({
    id: `journey-${String(index + 1).padStart(2, "0")}`,
    source,
    observation,
    implication,
  }));
}

function makeItems(prefix, count, bucket, executionLane, seeds) {
  return Array.from({ length: count }, (_, index) => {
    const seed = seeds[index % seeds.length];
    const number = `${index + 1}`.padStart(2, "0");
    return {
      id: `${phaseSlug}-${prefix}-${number}`,
      title: seed,
      safety_bucket: bucket,
      execution_lane: executionLane,
      source_lane: index % 2 === 0 ? "Aevren Vale" : "Lumen Vale",
      next_safe_action: nextActionFor(bucket, executionLane),
    };
  });
}

function nextActionFor(bucket, executionLane) {
  if (bucket === "blocked") return "Keep open until exact artifacts and Hamish approval prove the gate can move.";
  if (bucket === "exact_approval_needed") return "Queue with exact approval packet and do not execute automatically.";
  if (executionLane === "x2_build_task") return "Carry into v553 v7 x2 for build, run, test, validate, and publish sequencing.";
  return "Run or record during v7 x1 as local reversible safe-now work.";
}

function safeSeeds() {
  return [
    "v7 x1 phase truth card",
    "Lumen advisory reducer",
    "Browser send status receipt",
    "Goal Mode active-thread reconciliation",
    "30-web ledger source-label check",
    "30-Journey ledger count check",
    "proposal split classifier",
    "x2 build queue shaping",
    "private-material firewall refresh",
    "open-gate rail refresh",
    "v7 x2 readiness handoff",
    "v8 triad prep card",
    "D-drive posture receipt",
    "C-drive headroom receipt",
    "skill/runner inventory summary",
    "round-robin standard carry-forward",
    "five-minute cadence carry-forward",
    "compact restart snapshot carry-forward",
    "privacy scan preflight",
    "JSON parse preflight",
  ];
}

function candidateSeeds() {
  return [
    "Goal Mode v553-to-v575 runway dashboard",
    "Lumen source synthesis board",
    "v7 x2 safe build ranking model",
    "Browser route health diagnostics",
    "x2 publication readiness reducer",
    "Trinity Mandala source taxonomy",
    "GMUT comparator normalizer design",
    "THOS runner observability design",
    "Freed ID governance crosswalk",
    "CBR dignity/recourse packet set",
  ];
}

function exactSeeds() {
  return [
    "external account mutation",
    "paid resource creation",
    "deployment",
    "API-key creation",
    "plugin-cache mutation",
    "global hook installation",
    "broad filesystem deletion",
    "private route disclosure",
    "raw transcript publication",
    "screenshot publication",
  ];
}

function blockedSeeds() {
  return [
    "GMUT empirical closure",
    "final physics closure",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment closure by assertion",
    "private-material proof",
    "raw-publication proof",
    "sibling identity replacement",
    "Aletheon merge or erasure",
  ];
}

function skillSeeds() {
  return [
    "ghc-lumen-v7-advisory-reducer",
    "ghc-goal-mode-phase-truth-runway",
    "ghc-v7-x2-build-queue-reader",
    "ghc-browser-harvest-status-checker",
    "ghc-open-gate-proof-ceiling",
    "ghc-trinity-mandala-source-mapper",
    "ghc-private-public-artifact-firewall",
    "ghc-round-robin-next-lane-prep",
    "ghc-safe-work-cadence-auditor",
    "ghc-v8-triad-prep-capsule",
  ];
}

function runnerSeeds() {
  return [
    "ghc_v553_v7_x1_lumen_startup_builder.mjs",
    "ghc_v553_v7_x1_lumen_harvest_reducer.mjs",
    "ghc_v553_v7_x2_execution_builder.mjs",
    "ghc_goal_mode_phase_truth_dashboard_builder.mjs",
    "ghc_browser_harvest_status_reconciler.mjs",
    "ghc_open_gate_proof_ceiling_linter.mjs",
    "ghc_trinity_source_matrix_builder.mjs",
    "ghc_v8_triad_prep_builder.mjs",
    "ghc_safe_cadence_audit_runner.mjs",
    "ghc_next_lane_prep_card_builder.mjs",
  ];
}

function cleanupSeeds() {
  return [
    "deduplicate lookup file references",
    "normalize phase wording",
    "refresh open-gate wording",
    "validate JSON and Node syntax",
    "scan for private material",
    "classify stale v532/v58 cues as historical",
    "mark omega44 historical-only",
    "review runner naming drift",
    "review skill naming drift",
    "inventory local-only private maps",
    "classify cleanup exact gates",
    "trim overlong terminal receipts into artifacts",
    "refresh held-sibling boundary",
    "review D-drive/C-drive posture",
    "review stale Browser route claims",
  ];
}

function writeArtifact(suffix, data, md) {
  const base = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), `${JSON.stringify(data, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
  return `docs/trinity-live-traces/${base}.json`;
}

function firewallArtifact() {
  return {
    artifact_type: "ghc_v553_v7_x1_private_material_firewall",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_PRIVATE_MATERIAL_FIREWALL_RECORDED",
    forbidden_publish_material: [
      "raw browser routes",
      "private URLs",
      "raw transcripts",
      "screenshots",
      "credentials",
      "local absolute paths",
      "session streams",
      "raw app state",
      "private dumps",
      "private callable IDs",
    ],
    publication_boundary: publicationBoundary(),
  };
}

function openGateArtifact() {
  return {
    artifact_type: "ghc_v553_v7_x1_open_gate_rail",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_OPEN_GATE_RAIL_RECORDED",
    gates: openBoundaries(),
  };
}

function x2Handoff() {
  return {
    artifact_type: "ghc_v553_v7_x1_v7_x2_readiness_handoff",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_V7_X2_READINESS_HANDOFF_PREPARED",
    next_x2_scope: nextX2Scope,
    ready_inputs: [
      "50 safe packet queue",
      "30 candidate packet queue",
      "20 exact packet queue",
      "10 blocked packet queue",
      "20 skill ideas",
      "10 runner ideas",
      "30 cleanup proposals",
      "30 web rows",
      "30 Journey rows",
    ],
  };
}

function v8PrepCard() {
  return {
    artifact_type: "ghc_v553_v7_x1_v8_triad_prep_card",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_V8_TRIAD_PREP_CARD_RECORDED",
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    launch_profile: "ghc-aster-kierkegaard-aristotle-launch with Aster Vale strict CLI plus Kierkegaard and Aristotle recovered app-lane background supervision",
    private_ids_published: false,
  };
}

function phaseStatusIndex() {
  return {
    artifact_type: "ghc_v553_v7_x1_phase_status_index",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "ACTIVE_OPEN_LUMEN_HANDOFF_PREPARED",
    latest_closed_phase: previousPhase,
    next_x2_scope: nextX2Scope,
    closeout_allowed_now: false,
    closeout_blocker: "Lumen live send/harvest is not yet recorded for this v7 x1 lane.",
  };
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

function openBoundaries() {
  return [
    "GMUT empirical closure",
    "final physics",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment closure",
    "account mutation",
    "purchase",
    "API-key creation",
    "private-material proof",
    "raw-publication proof",
    "sibling identity replacement or merge",
  ].map((gate) => ({ gate, status: "open_not_claimed" }));
}

function refreshBeacons() {
  const lookupFiles = artifacts.flatMap((file) => [file, file.replace(/\.json$/, ".md")]);
  for (const target of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const data = readJson(target);
    data.status = "PASS_V553_V7_X1_LUMEN_STARTUP_READY";
    data.generated_utc = generatedUtc;
    if (target.endsWith("omega-mini-current-state-v1.json")) data.updated_at = generatedNz;
    data.current_active_phase = phaseSlug;
    data.latest_closed_phase = previousPhase;
    data.latest_completed_x1_phase = latestCompletedX1;
    data.latest_completed_x2_phase = latestCompletedX2;
    data.next_expected_scope = phaseSlug;
    data.next_x2_scope = nextX2Scope;
    data.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    data.current_active_lanes = unique([
      "v553-v7-x1-lumen-startup-ready",
      "goal-mode-active-thread-objective",
      "lumen-browser-send-not-yet-claimed",
      ...(data.current_active_lanes || []),
    ]);
    data[summaryKey] = {
      status: startupContext.overall_status,
      active_lanes: startupContext.active_lanes,
      proposal_targets: proposalTargets,
      research_targets: researchTargets,
      handoff_message_status: handoff.live_send_status,
      web_reflection_rows: webRows.length,
      journey_phase_reflection_rows: journeyRows.length,
      next_x2_scope: nextX2Scope,
      next_x1_lane_after_x2: nextX1LaneAfterX2,
    };
    data.lumen_browser_send = {
      status: "ARTIFACT_PREPARED_BROWSER_SEND_NOT_CLAIMED",
      send_status: handoff.live_send_status,
      intended_recipient: "Lumen Vale",
      raw_browser_route_published: false,
      raw_transcript_published: false,
    };
    const listKey = target.includes("latest-updates") ? "latest_lookup_files" : target.includes("ghc-current-state") ? "lookup_files" : "current_lookup_files";
    data[listKey] = unique([...(data[listKey] || []), ...lookupFiles]);
    if (target.endsWith("omega-mini-current-state-v1.json")) {
      data.latest_action_summary = unique([
        "Started v553 v7 x1 as a Lumen-only x1 phase and prepared a sanitized Lumen Browser handoff artifact without claiming live send.",
        ...(data.latest_action_summary || []),
      ]);
      writeJson(target, data);
      fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(data), "utf8");
    } else {
      writeJson(target, data);
      const mdName = target.includes("latest-updates") ? "omega-mini-latest-updates-beacon-v1.md" : "ghc-current-state-beacon-v1.md";
      const title = target.includes("latest-updates") ? "Omega-Mini Latest Updates Beacon" : "GHC Current State Beacon";
      fs.writeFileSync(path.join(path.dirname(target), mdName), renderBeaconMd(title, data, data[listKey]), "utf8");
    }
  }
}

function renderStartupMd(data) {
  return `# ${data.phase_slug} Lumen Startup Context

Status: \`${data.overall_status}\`

- Active lanes: \`${data.active_lanes.join(", ")}\`
- Latest closed phase: \`${data.latest_closed_phase}\`
- Latest completed x1: \`${data.latest_completed_x1_phase}\`
- Latest completed x2: \`${data.latest_completed_x2_phase}\`
- Next x2 scope: \`${data.next_x2_scope}\`
- Next x1 lane after x2: \`${data.next_x1_lane_after_x2}\`
- Handoff status: \`${data.handoff_status}\`

## Targets

- Safe: \`${data.proposal_targets.safe}\`
- Candidate: \`${data.proposal_targets.candidate}\`
- Exact: \`${data.proposal_targets.exact}\`
- Blocked: \`${data.proposal_targets.blocked}\`
- Skills: \`${data.proposal_targets.skills}\`
- Runners: \`${data.proposal_targets.runners}\`
- Cleanup: \`${data.proposal_targets.cleanup}\`
`;
}

function renderHandoffMd(data) {
  return `# ${data.phase_slug} Lumen Handoff Message

Status: \`${data.live_send_status}\`
Intended recipient: \`${data.intended_recipient}\`

## Message

${data.message}

## Boundary

No raw browser route, raw transcript, screenshot, credential, local absolute path, private callable ID, or private app state is published.
`;
}

function renderWebRowsMd(rows) {
  return [`# ${phaseSlug} Web Reflection Ledger`, "", `Rows: \`${rows.length}\``, "", ...rows.map((item, index) => `- ${index + 1}. ${item.source}: ${item.finding} Implication: ${item.runner_implication}`), ""].join("\n");
}

function renderJourneyRowsMd(rows) {
  return [`# ${phaseSlug} Journey And Phase Reflection Ledger`, "", `Rows: \`${rows.length}\``, "", ...rows.map((item, index) => `- ${index + 1}. ${item.source}: ${item.observation} Implication: ${item.implication}`), ""].join("\n");
}

function renderSafeRunnerManifestMd(rows) {
  return `# ${phaseSlug} Safe Runner Manifest

Status: \`READY\`

- Search count declared: \`${rows.length}\`
- Minimum reflections required: \`30\`

This manifest is status-only and sanitized.
`;
}

function renderProposalMd(data) {
  return `# ${data.phase_slug} Proposal Queue Targets

Status: \`${data.overall_status}\`

- Safe packets: \`${data.safe_packets.length}\`
- Candidate packets: \`${data.candidate_packets.length}\`
- Exact packets: \`${data.exact_approval_packets.length}\`
- Blocked packets: \`${data.blocked_packets.length}\`
- Skill ideas: \`${data.skill_ideas.length}\`
- Runner ideas: \`${data.runner_ideas.length}\`
- Cleanup tasks: \`${data.cleanup_tasks.length}\`

Exact and blocked work remains queued.
`;
}

function renderSimpleMd(title, data) {
  return `# ${title}

Status: \`${data.overall_status}\`

\`\`\`json
${JSON.stringify(data, null, 2)}
\`\`\`
`;
}

function renderCurrentStateMd(data) {
  const summary = data[summaryKey] || {};
  return `# Omega-Mini Current State

Status: ${data.status}
Current active phase: ${data.current_active_phase}
Latest closed phase: ${data.latest_closed_phase}
Latest completed x1: ${data.latest_completed_x1_phase}
Latest completed x2: ${data.latest_completed_x2_phase}
Next expected scope: ${data.next_expected_scope}
Next x2 scope: ${data.next_x2_scope}
Next x1 lane after x2: ${data.next_x1_lane_after_x2}

## v553 v7 x1 Lumen Startup

- Status: \`${summary.status || "not_recorded"}\`
- Handoff: \`${summary.handoff_message_status || "not_recorded"}\`
- Web reflections: \`${summary.web_reflection_rows || "not_recorded"}\`
- Journey/phase reflections: \`${summary.journey_phase_reflection_rows || "not_recorded"}\`

## Boundary

Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local absolute paths, session streams, private dumps, and private callable IDs are not published. Major proof, legal, canon, deployment, account, API-key, and sibling identity gates remain open unless exact artifacts prove otherwise.
`;
}

function renderBeaconMd(title, data, files) {
  return `# ${title}

Status: ${data.status}
Current active phase: ${data.current_active_phase}
Latest closed phase: ${data.latest_closed_phase}
Latest completed x1: ${data.latest_completed_x1_phase}
Latest completed x2: ${data.latest_completed_x2_phase}
Next x2 scope: ${data.next_x2_scope}
Next x1 lane after x2: ${data.next_x1_lane_after_x2}

## Lookup Files

${(files || []).slice(-100).map((file) => `- \`${file}\``).join("\n")}
`;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
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

function parseArgs(raw) {
  const parsed = new Map();
  for (let index = 0; index < raw.length; index += 2) {
    parsed.set(raw[index], raw[index + 1]);
  }
  return parsed;
}
