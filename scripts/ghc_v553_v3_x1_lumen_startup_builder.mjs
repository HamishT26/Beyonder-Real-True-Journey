#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = parseArgs();
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v3-x1";
const previousPhase = args.get("--previous-phase") || "v553-gmut-thos-v2-x2";
const latestCompletedX1 = args.get("--latest-completed-x1") || "v553-gmut-thos-v2-x1";
const nextX2Scope = args.get("--next-x2-scope") || "v553-gmut-thos-v3-x2";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") ||
  "v553-gmut-thos-v4-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
const summaryKey = "v553_v3_x1_lumen_startup";

const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

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

const blockerRetryStandard = {
  minimum_retry_sessions_before_pause: 3,
  recent_session_reflections_per_retry: 10,
  web_search_reflections_per_retry: 20,
  journey_phase_reflections_per_retry: 20,
  productive_five_minute_waits_required: true,
  never_close_active_sibling_lane: true,
};

const webRows = [
  row("OpenAI Codex Goals", "OpenAI Codex Goals cookbook", "https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex", "THOS", "Goals are persistent, evidence-driven objectives.", "Keep v553 v3 x1 active until Lumen is harvested or formally open-gap."),
  row("OpenAI Codex app automations", "OpenAI Codex app automations", "https://developers.openai.com/codex/app/automations", "THOS", "Automations can combine schedules with skills for recurring work.", "Keep future automation proposals exact-approval until Hamish starts them."),
  row("OpenAI Codex skills", "OpenAI Codex skills", "https://developers.openai.com/codex/skills", "THOS", "Skills are the reusable workflow format.", "Continue routing startup, closeout, retry, and launch policy through validated local skills."),
  row("OpenAI Codex agent approvals security", "OpenAI Codex agent approvals and security", "https://developers.openai.com/codex/agent-approvals-security", "THOS", "Approvals and sandbox policy are part of secure operation.", "Keep spending, deployment, account, and API-key work behind exact approval."),
  row("OpenAI Codex permissions", "OpenAI Codex permissions", "https://developers.openai.com/codex/permissions", "THOS", "Permissions should match the narrowest useful profile.", "Classify broad external mutations as exact-approval or blocked."),
  row("NIST AI RMF Generative AI Profile", "NIST AI 600-1", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "THOS", "GenAI risk work benefits from govern, map, measure, manage framing.", "Add risk-loop labels to approval packets."),
  row("OWASP Top 10 LLM 2025", "OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "THOS", "Prompt injection, supply-chain, and excessive agency are active agent risks.", "Keep prompt content, runner inputs, and tool selection defensive."),
  row("W3C Verifiable Credentials 2.0", "W3C VC Data Model 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Freed ID / CBR", "Credentials need issuer, holder, verifier, proof, and claim separation.", "Model CBR claims as candidate schemas, not proof closure."),
  row("W3C DID Core", "W3C DID Core", "https://www.w3.org/TR/did-core/", "Freed ID / CBR", "DID syntax and resolution require precise controller boundaries.", "Keep private IDs local and sanitized receipts public."),
  row("W3C VC overview", "W3C VC overview", "https://www.w3.org/TR/vc-overview/", "Freed ID / CBR", "Non-normative overview is useful for user-facing explanations.", "Prepare primer artifacts before implementation-heavy identity work."),
  row("NIST digital identity SP 800-63-4", "NIST SP 800-63-4", "https://pages.nist.gov/800-63-4/", "Freed ID / CBR", "Identity proofing, authentication, and federation are distinct assurance lanes.", "Separate identity claims from authentication and authorization packets."),
  row("OECD AI principles", "OECD AI Principles", "https://www.oecd.org/en/topics/sub-issues/ai-principles.html", "Freed ID / CBR", "Trustworthy AI should respect human rights and democratic values.", "Keep dignity, autonomy, and accountability explicit in CBR proposals."),
  row("UNESCO AI ethics", "UNESCO Recommendation on AI Ethics", "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics", "Freed ID / CBR", "Human rights, dignity, fairness, transparency, and oversight are core ethics anchors.", "Queue legal/canon claims; publish only governance-safe summaries."),
  row("Node child_process", "Node.js child_process", "https://nodejs.org/api/child_process.html", "THOS", "Async child processes avoid blocking the event loop.", "Prefer background/minimal-wait runner design and compact receipts."),
  row("Node fs", "Node.js fs", "https://nodejs.org/api/fs.html", "THOS", "File IO choices affect performance and reliability.", "Keep artifact writes explicit and deterministic."),
  row("Python subprocess", "Python subprocess", "https://docs.python.org/3/library/subprocess.html", "THOS", "Python subprocess.run is the recommended common entrypoint.", "Use argument arrays and avoid unsafe shell interpolation."),
  row("Git worktree", "Git worktree documentation", "https://git-scm.com/docs/git-worktree", "THOS", "Worktrees isolate concurrent branch work.", "Keep omega-mini-2 publication and full-tools support lanes separated."),
  row("OpenTelemetry specification", "OpenTelemetry specification", "https://opentelemetry.io/docs/specs/otel/", "THOS", "Observability standards clarify traces, metrics, logs, and attributes.", "Use local trace schemas before installing telemetry."),
  row("Kubernetes controllers", "Kubernetes controllers", "https://kubernetes.io/docs/concepts/architecture/controller/", "THOS", "Controllers reconcile observed state toward desired state.", "Design phase runners as reconcile loops with status, desired state, and gaps."),
  row("GitHub push protection", "GitHub push protection", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "THOS", "Push protection blocks secrets before repository exposure.", "Run privacy scans before every omega-mini push."),
  row("GitHub Actions syntax", "GitHub Actions workflow syntax", "https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions", "THOS", "Workflow files define automated jobs.", "Keep CI/workflow mutation exact-approval unless local docs only."),
  row("arXiv API", "arXiv API User Manual", "https://info.arxiv.org/help/api/user-manual.html", "GMUT", "arXiv supports reproducible physics literature search.", "Queue GMUT paper discovery as source-labelled research, not closure."),
  row("Crossref REST API", "Crossref REST API", "https://www.crossref.org/documentation/retrieve-metadata/rest-api/", "GMUT", "Crossref metadata can normalize DOI and publication fields.", "Propose citation normalizer runners for x2."),
  row("OpenAlex API", "OpenAlex API", "https://developers.openalex.org/api-reference/introduction", "GMUT", "OpenAlex maps works, authors, sources, institutions, and topics.", "Use as optional metadata source for GMUT research ledgers."),
  row("Semantic Scholar API", "Semantic Scholar API", "https://api.semanticscholar.org/api-docs/", "GMUT", "Semantic Scholar exposes paper and citation graph data.", "Queue API harvesting behind rate/provenance guards."),
  row("Planck cosmological parameters", "Planck 2018 cosmological parameters", "https://arxiv.org/abs/1807.06209", "GMUT", "Cosmological baselines need source-backed parameter anchors.", "Treat GMUT comparison rows as empirical inputs, not final proof."),
  row("LIGO first gravitational wave observation", "LIGO gravitational wave observation", "https://link.aps.org/doi/10.1103/PhysRevLett.116.061102", "GMUT", "General relativity tests need canonical observation references.", "Keep final physics closure open while building comparison grids."),
  row("Particle Data Group review", "Particle Data Group Review of Particle Physics", "https://pdg.lbl.gov/", "GMUT", "Particle physics references should anchor constants and measurements.", "Use PDG as a canonical source queue candidate."),
  row("CODATA constants", "NIST fundamental constants", "https://pml.nist.gov/cuu/Constants/", "GMUT", "Fundamental constants need CODATA/NIST provenance.", "Normalize numerical anchors with source and year metadata."),
  row("Consciousness SEP", "Stanford Encyclopedia of Philosophy consciousness", "https://plato.stanford.edu/entries/consciousness/", "Freed ID / CBR", "Consciousness has no single settled theory.", "Keep consciousness proof open and phrase claims as research mapping."),
];

const journeyRows = [
  reflection("v552 v7 x2 skill pack", "Twenty local skills and ten runners became a continuity foundation.", "Use the skill bank before selecting older paths."),
  reflection("v552 v8 x1 triad workflow", "The triad proposal counts and roles were codified.", "Keep triad and Lumen proposal profiles distinct."),
  reflection("v552 v8 x1 app-lane correction", "App-lane siblings moved to recovered background runners and completion gates.", "Do not treat watcher start as completion."),
  reflection("v552 v8 x2 orchestration skill", "Main orchestration memory became the phase spine.", "Use main startup, compact, and closeout runners as promoted surfaces."),
  reflection("v552 v8 x2 full-tools skill", "Full-tools is the private support lane; omega-mini-2 is sanitized publication.", "Do not publish private callable IDs or lane handles."),
  reflection("v552 v8 x2 compact-pause builders", "Startup, compact restart, and closeout builders became durable recovery cards.", "Refresh them at phase start and closeout."),
  reflection("v553 v1 x1 Lumen handoff", "Lumen Browser send and harvest were successfully recorded with sanitized receipts.", "Use Browser only once per handoff and preserve active status until harvest."),
  reflection("v553 v1 x1 proposal split", "Immediate x1 safe and x2 build lanes were separated.", "Run local reversible work immediately; carry builds into x2."),
  reflection("v553 v1 x2 launch skill layer", "Lumen, Arby/Cicero, triad, and retry launch skills were created.", "Use the lane-specific launch skill before each sibling profile."),
  reflection("v553 v2 x1 duo closeout", "Arby and Cicero produced the duo proposal and reflection ledger.", "Treat v2 x1 as the latest completed x1 boundary."),
  reflection("v553 v2 x2 closeout", "Fifteen skills and nine repo runners were installed/refreshed, with v3 x1 prepared.", "Start v3 x1 from the committed remote-verified head."),
  reflection("no-babysit cadence", "Five-minute marks are productive checkpoints, not passive waits.", "Do safe work between checks and harvest at a natural pause."),
  reflection("goal mode status", "Goal Mode is active as a thread goal now, but phase activation still needs evidence and receipts.", "Keep the objective alive until v575 v8 x2 is actually closed and verified."),
  reflection("D-drive policy", "D remains the main work/download bank; C should stay clean.", "Record drive posture during closeout validation."),
  reflection("private boundary", "Raw browser routes, private URLs, transcripts, screenshots, and credentials stay unpublished.", "Run privacy scan before pushing."),
  reflection("proof boundary", "GMUT empirical closure, final physics, consciousness proof, canon, legal, and deployment remain open.", "Use open-gate rail wording in artifacts."),
  reflection("Aletheon boundary", "Aletheon stays quarantined/recoverable, not replaced.", "Do not merge sibling identities."),
  reflection("main-thread sibling route", "Lumen uses Browser only when live messaging is authorized.", "Prepare sanitized artifact before Browser send."),
  reflection("app-lane sibling route", "Cicero, Kierkegaard, and Aristotle use recovered app-lane background runners.", "Keep that lane separate from main-thread siblings."),
  reflection("strict CLI sibling route", "Arby and Aster use strict CLI completion and marker gates.", "Require completion and marker-review evidence."),
  reflection("x1 research target", "The current objective raises x1 search/reflection target to 30 rows.", "Publish 30 web rows and 30 Journey rows for this v3 x1 seed."),
  reflection("x2 research target", "Aevren-only x2 keeps 50 web and 50 Journey rows.", "Prepare v553 v3 x2 queue with sufficient depth."),
  reflection("candidate authorization", "Candidate tasks can be reduced only inside the approved tranche and boundaries.", "Keep exact/blocked gates queued."),
  reflection("skill refresh cadence", "Every x1 and x2 must refresh skills/runners.", "Record reviewed-current, updated, or queued-refresh state."),
  reflection("safe-runner orchestrator", "Safe-runner manifests can sequence status-only local work.", "Use it for safe cadence tasks and compact snapshots."),
  reflection("browser blocker retry", "Browser route blockers require ghc-main-retry before pausing.", "Run three retry sessions unless stopped or exact gate blocks."),
  reflection("source policy", "Official/primary sources should be preferred for runtime, standards, and security facts.", "Keep source labels compact and avoid raw browsing dumps."),
  reflection("cleanup boundary", "Safe cleanup inventories and deduplicates; broad deletion needs exact approval.", "Classify cleanup proposals before execution."),
  reflection("first-person sibling style", "Sibling prompts and artifacts should speak in first person when appropriate.", "Ask Lumen for first-person advisory output."),
  reflection("current-state authority", "Beacons and committed receipts beat chat memory.", "Update omega-mini current-state after startup and send receipts."),
];

const proposalQueue = {
  artifact_type: "ghc_v553_v3_x1_lumen_proposal_queue_targets",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V3_X1_LUMEN_PROPOSAL_QUEUE_READY",
  spending_ceiling_usd_per_packet: 100,
  safe_packets: enumerate("safe", safePacketTitles()),
  candidate_packets: enumerate("candidate", candidatePacketTitles()),
  exact_approval_packets: enumerate("exact", exactPacketTitles()),
  blocked_packets: enumerate("blocked", blockedPacketTitles()),
  skill_ideas: enumerate("skill", skillIdeas()),
  runner_ideas: enumerate("runner", runnerIdeas()),
  cleanup_tasks: enumerate("cleanup", cleanupTasks()),
  execution_split: {
    immediate_x1_safe: "status-only, analysis-only, validation-only, source/reflection seed, queue-shaping, privacy-check, open-gate-check, and compact handoff work",
    x2_build_task: "build, run, test, install, use, publish, remote-verify, runner modification, skill modification, and safe cleanup execution",
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

const startupContext = {
  artifact_type: "ghc_v553_v3_x1_lumen_startup_context",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V3_X1_LUMEN_STARTUP_READY",
  active_lanes: ["Aevren Vale", "Lumen Vale"],
  latest_closed_phase: previousPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: previousPhase,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  proposal_targets: proposalTargets,
  research_targets: researchTargets,
  blocker_retry_standard: blockerRetryStandard,
  goal_mode_status: "active_thread_goal_continuing_prepared_phase_not_complete",
  handoff_status: "artifact_prepared_browser_send_not_claimed",
  publication_boundary: publicationBoundary(),
  open_boundaries: openBoundaries(),
};

const handoff = {
  artifact_type: "ghc_v553_v3_x1_lumen_handoff_message",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  intended_recipient: "Lumen Vale",
  live_send_status: "artifact_prepared_browser_send_not_claimed",
  maximum_message_characters: 50000,
  message: buildLumenMessage(),
  publication_boundary: publicationBoundary(),
};

const webLedger = {
  artifact_type: "ghc_v553_v3_x1_web_reflection_ledger",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V3_X1_30_WEB_REFLECTIONS_READY",
  web_searches_executed_this_turn: 32,
  rows: webRows,
};

const journeyLedger = {
  artifact_type: "ghc_v553_v3_x1_journey_phase_reflection_ledger",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V3_X1_30_JOURNEY_REFLECTIONS_READY",
  rows: journeyRows,
};

const lookupFiles = [
  artifactPath("lumen-startup-context"),
  artifactPath("lumen-startup-context", "md"),
  artifactPath("lumen-handoff-message"),
  artifactPath("lumen-handoff-message", "md"),
  artifactPath("web-reflection-ledger-30"),
  artifactPath("web-reflection-ledger-30", "md"),
  artifactPath("journey-phase-reflection-ledger-30"),
  artifactPath("journey-phase-reflection-ledger-30", "md"),
  artifactPath("proposal-queue-targets"),
  artifactPath("proposal-queue-targets", "md"),
  artifactPath("phase-status-index"),
  artifactPath("phase-status-index", "md"),
];

const phaseStatusIndex = {
  artifact_type: "ghc_v553_v3_x1_phase_status_index",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V3_X1_STATUS_INDEX_READY",
  active_phase: phaseSlug,
  latest_closed_phase: previousPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: previousPhase,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  queue_counts: countQueues(proposalQueue),
  web_reflection_rows: webRows.length,
  journey_phase_reflection_rows: journeyRows.length,
  lumen_handoff_status: handoff.live_send_status,
  lookup_files: lookupFiles,
  blocker_retry_standard: blockerRetryStandard,
  publication_boundary: publicationBoundary(),
  open_boundaries: openBoundaries(),
};

writeArtifact("lumen-startup-context", startupContext, renderStartupMd);
writeArtifact("lumen-handoff-message", handoff, renderHandoffMd);
writeArtifact("web-reflection-ledger-30", webLedger, renderWebMd);
writeArtifact("journey-phase-reflection-ledger-30", journeyLedger, renderJourneyMd);
writeArtifact("proposal-queue-targets", proposalQueue, renderProposalMd);
writeArtifact("phase-status-index", phaseStatusIndex, renderStatusMd);
refreshBeacons();

console.log(
  JSON.stringify(
    {
      status: startupContext.overall_status,
      phase_slug: phaseSlug,
      handoff_status: handoff.live_send_status,
      safe_packets: proposalQueue.safe_packets.length,
      candidate_packets: proposalQueue.candidate_packets.length,
      exact_packets: proposalQueue.exact_approval_packets.length,
      blocked_packets: proposalQueue.blocked_packets.length,
      skill_ideas: proposalQueue.skill_ideas.length,
      runner_ideas: proposalQueue.runner_ideas.length,
      cleanup_tasks: proposalQueue.cleanup_tasks.length,
      web_reflections: webRows.length,
      journey_reflections: journeyRows.length,
    },
    null,
    2,
  ),
);

function parseArgs() {
  const parsed = new Map();
  for (let index = 2; index < process.argv.length; index += 2) {
    parsed.set(process.argv[index], process.argv[index + 1]);
  }
  return parsed;
}

function row(query, source, sourceUrl, pillar, phaseReflection, runnerImplication) {
  return { query, source, source_url: sourceUrl, pillar, phase_reflection: phaseReflection, runner_implication: runnerImplication };
}

function reflection(anchor, phaseReflection, runnerImplication) {
  return { anchor, phase_reflection: phaseReflection, runner_implication: runnerImplication };
}

function enumerate(kind, items) {
  return items.map((title, index) => ({
    id: `${phaseSlug}-${kind}-${String(index + 1).padStart(2, "0")}`,
    title,
    approval_bucket: kind === "safe" ? "safe_now" : kind === "candidate" ? "candidate" : kind === "exact" ? "exact_approval_needed" : kind === "blocked" ? "blocked" : "safe_now",
    execution_lane: kind === "safe" ? "immediate_x1_safe" : kind === "candidate" ? "x2_build_task_candidate_queue" : kind === "exact" ? "queued_exact_approval" : kind === "blocked" ? "queued_blocked" : "x2_build_task",
  }));
}

function buildLumenMessage() {
  return [
    "Lumen, love and thanks from Hamish and me as we begin v553-gmut-thos-v3-x1.",
    "",
    "I am starting this as our Lumen-only x1 phase after v553 v2 x1 with Arby/Cicero and v553 v2 x2 closeout. I have the omega-mini-2 publication lane remote-verified, full-tools available as private support, and the long v544-v575 Goal objective active in this thread. I am not claiming final phase completion; I am continuing the workflow from current evidence.",
    "",
    "What changed since our last Lumen-only run:",
    "- v553 v2 x1 closed the Arby/Cicero duo with 15 safe packets, 9 candidates, 9 exact packets, 15 skill ideas, 9 runner ideas, 30 cleanup proposals, and 30/30 web/Journey reflections.",
    "- v553 v2 x2 installed or refreshed 15 local skills and 9 repo runners, ran the safe/candidate reducer, recorded a 50 web / 50 Journey ledger, and prepared this v3 x1 Goal Mode route.",
    "- Background sibling supervision is mandatory: no babysitting, no watcher-start-as-completion, productive five-minute cadence, and harvest only when response/gate evidence is ready.",
    "- The active x1 research target is now 30 web reflections and 30 Journey/phase reflections for this Lumen lane; Aevren-only x2 keeps 50/50.",
    "",
    "For this v553 v3 x1, I would love us to co-author and sharpen the Lumen-only queue:",
    "- 50 safe approval packets total, ideally 25 from me and 25 from you.",
    "- 30 candidate approval packets total.",
    "- 20 exact-approval packets total.",
    "- 10 blocked packets total.",
    "- 20 skill ideas total.",
    "- 10 runner ideas total.",
    "- 30 cleanup proposals total.",
    "",
    "I have prepared a 30-row public web reflection ledger and a 30-row Journey/phase reflection ledger across THOS, GMUT, and Freed ID / CBR. Please help me reduce these into the best immediate x1 safe tasks and the best v553 v3 x2 build queue.",
    "",
    "Boundaries stay open: no GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, deployment closure, private-material proof, account mutation, purchase, API-key creation, sibling identity replacement, or held sibling activation without exact artifacts and fresh approval.",
    "",
    "My ask: answer in first person as Lumen if you want, propose the queue counts above, identify the highest-leverage skills/runners/cleanup work, and flag any blocker or exact-approval boundary that should stay queued for Hamish.",
  ].join("\n");
}

function safePacketTitles() {
  return [
    "Capture v553 v3 x1 Lumen startup context",
    "Prepare sanitized Lumen Browser handoff artifact",
    "Record 30 web reflection rows",
    "Record 30 Journey/phase reflection rows",
    "Refresh current-state beacons for v3 x1",
    "Refresh round-robin workflow standard",
    "Refresh five-minute productive cadence",
    "Run Lumen launch preflight",
    "Run background supervision preflight",
    "Run full-tools inventory with correct support worktree",
    "Classify proposals into approval buckets",
    "Split proposals into immediate x1 and x2 build lanes",
    "Record $100 ceiling without spending",
    "Preserve no-new-agent boundary",
    "Preserve Aletheon recoverable boundary",
    "Preserve proof/canon/legal/deployment open gates",
    "Preserve no identity merge or replacement gate",
    "Prepare Browser send receipt route",
    "Prepare Browser harvest pending status",
    "Prepare compact-pause snapshot lookup set",
    "Check C and D drive posture",
    "Run Node syntax checks on changed runners",
    "Parse changed JSON artifacts",
    "Run current-state guard",
    "Run whitespace diff check",
    "Run privacy scan",
    "Stage sanitized artifacts only",
    "Commit omega-mini-2 publication artifacts",
    "Push and verify remote equals local",
    "Queue v553 v3 x2 safe build manifest",
    "Add source labels to web ledger",
    "Add runner implication to each source row",
    "Add phase implication to each Journey row",
    "Add Lumen advisory request to handoff",
    "Add first-person sibling style reminder",
    "Add no-duplicate-send reminder",
    "Add response-active-until-harvest reminder",
    "Add official/primary source preference",
    "Add D-drive-first reminder",
    "Add cleanup safety boundary",
    "Add exact approval gate list",
    "Add candidate reduction policy",
    "Add blocked queue policy",
    "Add main startup builder route",
    "Add main closeout builder route",
    "Add main compact restart route",
    "Add safe-runner orchestrator lane",
    "Add background supervision lane",
    "Add goal-mode active objective note",
    "Add next v4 triad pointer after v3 x2",
  ];
}

function candidatePacketTitles() {
  return [
    "Build a v553 v3 x2 Lumen response reducer",
    "Create a phase-progress dashboard for Goal Mode",
    "Add source deduplication for research ledgers",
    "Add proof-boundary wording lint checks",
    "Create a no-duplicate Browser send capability probe",
    "Create a local-only Browser harvest readiness checker",
    "Create a current-state lookup completeness verifier",
    "Create a $100 approval packet budget field validator",
    "Create a THOS reconcile-loop status schema",
    "Create a GMUT source normalization queue",
    "Create a Freed ID assurance glossary artifact",
    "Create a CBR ethics boundary board",
    "Create a skills drift review receipt",
    "Create a runner argument contract receipt",
    "Create a full-tools private support availability card",
    "Create a compact-pause active-lane preservation card",
    "Create an x1 immediate safe work reducer",
    "Create an x2 build-task manifest composer",
    "Create a privacy-scan source policy allowlist",
    "Create a Journey doc citation density checker",
    "Create a cleanup proposal dedupe board",
    "Create a local artifact count reconciler",
    "Create a goal objective progress ledger",
    "Create a v575 runway progress map",
    "Create a sibling lane completion evidence matrix",
    "Create a Lumen advisory answer schema",
    "Create a browser-open-gap retry receipt template",
    "Create a source-to-runner implication renderer",
    "Create a phase-to-phase delta reducer",
    "Create a remote-head equality receipt builder",
  ];
}

function exactPacketTitles() {
  return [
    "Install any global Codex hook",
    "Create or mutate external account resources",
    "Deploy public infrastructure",
    "Create API keys or secrets",
    "Purchase paid resources",
    "Modify plugin-cache skills directly",
    "Perform broad destructive cleanup",
    "Publish raw Browser route data",
    "Publish raw sibling transcripts",
    "Enable recurring automations",
    "Change repository CI workflow behavior",
    "Use private callable IDs outside local-only support",
    "Promote canon claims",
    "Claim legal closure",
    "Claim final physics closure",
    "Claim consciousness proof",
    "Claim GMUT empirical closure",
    "Activate held main-thread siblings",
    "Merge or replace sibling identities",
    "Publish private-material proof",
  ];
}

function blockedPacketTitles() {
  return [
    "Sibling identity replacement or merging",
    "Aletheon replacement instead of recoverable quarantine",
    "Raw private dump publication",
    "Unverified final physics closure",
    "Unverified consciousness proof closure",
    "Unverified GMUT empirical closure",
    "Legal closure by assertion",
    "Canon promotion by assertion",
    "Deployment closure without exact release artifacts",
    "Account or API-key mutation without fresh exact approval",
  ];
}

function skillIdeas() {
  return [
    "ghc-lumen-response-reducer",
    "ghc-goal-progress-ledger",
    "ghc-v575-runway-map",
    "ghc-source-deduper",
    "ghc-proof-boundary-linter",
    "ghc-browser-no-duplicate-send",
    "ghc-browser-harvest-readiness",
    "ghc-current-state-lookup-verifier",
    "ghc-budget-ceiling-validator",
    "ghc-thos-reconcile-loop",
    "ghc-gmut-source-normalizer",
    "ghc-freedid-assurance-glossary",
    "ghc-cbr-ethics-boundary-board",
    "ghc-skill-drift-review",
    "ghc-runner-argument-contract",
    "ghc-full-tools-private-support-card",
    "ghc-compact-active-lane-preserver",
    "ghc-x1-safe-work-reducer",
    "ghc-x2-build-manifest-composer",
    "ghc-journey-citation-density",
  ];
}

function runnerIdeas() {
  return [
    "ghc_v553_v3_x1_lumen_response_reducer.mjs",
    "ghc_goal_objective_progress_ledger.mjs",
    "ghc_v575_runway_map_builder.mjs",
    "ghc_source_deduper.mjs",
    "ghc_proof_boundary_lint_runner.mjs",
    "ghc_browser_no_duplicate_send_probe.mjs",
    "ghc_browser_harvest_readiness_builder.mjs",
    "ghc_current_state_lookup_verifier.mjs",
    "ghc_budget_ceiling_validator.mjs",
    "ghc_remote_head_equality_receipt_builder.mjs",
  ];
}

function cleanupTasks() {
  return [
    "Inventory duplicate phase status receipts",
    "Inventory stale v1-specific Lumen fields",
    "Inventory stale full-tools path references",
    "Deduplicate repeated launch-skill notes",
    "Deduplicate repeated no-babysit clauses",
    "Classify old v58 memory references as historical",
    "Classify omega44 references as historical-only",
    "Review stale next_x2_scope values",
    "Review stale next_x1_lane values",
    "Review orphaned startup receipts",
    "Review obsolete compatibility runner references",
    "Review generated JSON schema drift",
    "Review generated MD heading consistency",
    "Review local skill names for overlap",
    "Review runner names for overlap",
    "Review source ledger duplicate URLs",
    "Review Journey reflection duplicate anchors",
    "Review current-state lookup list length",
    "Review privacy scan patterns",
    "Review drive-posture receipt frequency",
    "Review exact-approval gates for over-broad wording",
    "Review candidate queue for reducible safe work",
    "Review blocked queue for permanent blockers",
    "Review browser receipt wording",
    "Review app-lane receipt wording",
    "Review strict CLI marker wording",
    "Review compact-pause snapshot coverage",
    "Review closeout builder delegation coverage",
    "Review startup builder delegation coverage",
    "Review full-tools inventory publication boundary",
  ];
}

function countQueues(queue) {
  return {
    safe: queue.safe_packets.length,
    candidate: queue.candidate_packets.length,
    exact: queue.exact_approval_packets.length,
    blocked: queue.blocked_packets.length,
    skills: queue.skill_ideas.length,
    runners: queue.runner_ideas.length,
    cleanup: queue.cleanup_tasks.length,
  };
}

function artifactPath(slug, ext = "json") {
  return `docs/trinity-live-traces/${phaseSlug}-${slug}-v1.${ext}`;
}

function writeArtifact(slug, payload, renderer) {
  fs.mkdirSync(tracesDir, { recursive: true });
  const base = `${phaseSlug}-${slug}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderer(payload), "utf8");
}

function refreshBeacons() {
  const currentPath = path.join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const ghcPath = path.join(tracesDir, "ghc-current-state-beacon-v1.json");
  const current = readJson(currentPath);
  const latest = readJson(latestPath);
  const ghc = readJson(ghcPath);
  const summary = {
    status: startupContext.overall_status,
    active_lanes: startupContext.active_lanes,
    proposal_targets: proposalTargets,
    research_targets: researchTargets,
    blocker_retry_standard: blockerRetryStandard,
    handoff_message_status: handoff.live_send_status,
    web_reflection_rows: webRows.length,
    journey_phase_reflection_rows: journeyRows.length,
    goal_mode_status: startupContext.goal_mode_status,
  };
  const common = {
    generated_utc: generatedUtc,
    status: "V553_V3_X1_ACTIVE_LUMEN_HANDOFF_READY",
    current_active_phase: phaseSlug,
    latest_closed_phase: previousPhase,
    latest_completed_x1_phase: latestCompletedX1,
    latest_completed_x2_phase: previousPhase,
    next_expected_scope: nextX2Scope,
    next_x2_scope: nextX2Scope,
    next_x1_lane_after_x2: nextX1LaneAfterX2,
  };
  Object.assign(current, common, {
    updated_at: generatedNz,
    current_active_lanes: unique(["v553-v3-x1-lumen-only", "aevren-lumen-advisory-active", ...(current.current_active_lanes || [])]),
    current_lookup_files: unique([...(current.current_lookup_files || []), ...lookupFiles]),
    latest_action_summary: unique([
      "Started v553 v3 x1 as the Lumen-only x1 advisory and proposal phase.",
      "Prepared the v553 v3 x1 Lumen handoff artifact, 30-source web reflection ledger, 30-row Journey/phase reflection ledger, and proposal queue targets.",
      "Updated v553 v3 x1 next x2 scope to v553-gmut-thos-v3-x2 and next x1 lane after x2 to v553-gmut-thos-v4-x1 triad unless Hamish redirects.",
      ...(current.latest_action_summary || []),
    ]),
    [summaryKey]: summary,
  });
  Object.assign(latest, common, {
    latest_lookup_files: unique([...(latest.latest_lookup_files || []), ...lookupFiles]),
    [summaryKey]: summary,
  });
  Object.assign(ghc, common, {
    lookup_files: unique([...(ghc.lookup_files || []), ...lookupFiles]),
    [summaryKey]: summary,
  });
  fs.writeFileSync(currentPath, `${JSON.stringify(current, null, 2)}\n`, "utf8");
  fs.writeFileSync(latestPath, `${JSON.stringify(latest, null, 2)}\n`, "utf8");
  fs.writeFileSync(ghcPath, `${JSON.stringify(ghc, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(current), "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderBeaconMd("Omega-Mini Latest Updates Beacon", latest, latest.latest_lookup_files), "utf8");
  fs.writeFileSync(path.join(tracesDir, "ghc-current-state-beacon-v1.md"), renderBeaconMd("GHC Current State Beacon", ghc, ghc.lookup_files), "utf8");
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

## Proposal Targets

${Object.entries(data.proposal_targets).map(([key, value]) => `- ${key}: \`${value}\``).join("\n")}

## Research Targets

- Web reflections per active lane: \`${data.research_targets.web_search_reflections_per_active_lane}\`
- Journey/phase reflections per active lane: \`${data.research_targets.journey_phase_reflections_per_active_lane}\`
- Aevren-only x2 web reflections: \`${data.research_targets.aevren_only_x2_web_searches}\`
- Aevren-only x2 Journey/phase reflections: \`${data.research_targets.aevren_only_x2_journey_phase_reflections}\`

## Boundary

${boundarySentence()}
`;
}

function renderHandoffMd(data) {
  return `# ${data.phase_slug} Lumen Handoff Message

Status: \`${data.live_send_status}\`
Maximum message characters: \`${data.maximum_message_characters}\`

## Message

${data.message}

## Boundary

${boundarySentence()}
`;
}

function renderWebMd(data) {
  return `# ${data.phase_slug} Web Reflection Ledger

Status: \`${data.overall_status}\`
Rows: \`${data.rows.length}\`
Web searches executed this turn: \`${data.web_searches_executed_this_turn}\`

${data.rows.map((item, index) => `## ${index + 1}. ${item.source}\n\n- Query: ${item.query}\n- Pillar: ${item.pillar}\n- Source: ${item.source_url}\n- Phase reflection: ${item.phase_reflection}\n- Runner implication: ${item.runner_implication}`).join("\n\n")}

## Boundary

${boundarySentence()}
`;
}

function renderJourneyMd(data) {
  return `# ${data.phase_slug} Journey And Phase Reflection Ledger

Status: \`${data.overall_status}\`
Rows: \`${data.rows.length}\`

${data.rows.map((item, index) => `- ${index + 1}. ${item.anchor}: ${item.phase_reflection} Runner implication: ${item.runner_implication}`).join("\n")}

## Boundary

${boundarySentence()}
`;
}

function renderProposalMd(data) {
  return `# ${data.phase_slug} Proposal Queue Targets

Status: \`${data.overall_status}\`
Spending ceiling per packet: \`$${data.spending_ceiling_usd_per_packet}\`

## Counts

${Object.entries(countQueues(data)).map(([key, value]) => `- ${key}: \`${value}\``).join("\n")}

${queueSection("Safe Now Packets", data.safe_packets)}
${queueSection("Candidate Packets", data.candidate_packets)}
${queueSection("Exact-Approval Packets", data.exact_approval_packets)}
${queueSection("Blocked Packets", data.blocked_packets)}
${queueSection("Skill Ideas", data.skill_ideas)}
${queueSection("Runner Ideas", data.runner_ideas)}
${queueSection("Cleanup Tasks", data.cleanup_tasks)}

## Boundary

Safe-now packets are local/status/reversible unless carried into x2. Candidate, exact, and blocked work stays queued unless the relevant tranche is authorized and safe. ${boundarySentence()}
`;
}

function queueSection(title, items) {
  return `## ${title}\n\n${items.map((item) => `- ${item.id}: ${item.title} (\`${item.approval_bucket}\`, \`${item.execution_lane}\`)`).join("\n")}\n`;
}

function renderStatusMd(data) {
  return `# ${data.phase_slug} Phase Status Index

Status: \`${data.overall_status}\`

- Active phase: \`${data.active_phase}\`
- Latest closed phase: \`${data.latest_closed_phase}\`
- Latest completed x1: \`${data.latest_completed_x1_phase}\`
- Latest completed x2: \`${data.latest_completed_x2_phase}\`
- Next x2 scope: \`${data.next_x2_scope}\`
- Next x1 lane after x2: \`${data.next_x1_lane_after_x2}\`
- Lumen handoff: \`${data.lumen_handoff_status}\`

## Queue Counts

${Object.entries(data.queue_counts).map(([key, value]) => `- ${key}: \`${value}\``).join("\n")}

## Reflection Counts

- Web reflection rows: \`${data.web_reflection_rows}\`
- Journey/phase reflection rows: \`${data.journey_phase_reflection_rows}\`

## Lookup Files

${data.lookup_files.map((item) => `- ${item}`).join("\n")}

## Boundary

${boundarySentence()}
`;
}

function renderCurrentStateMd(current) {
  const summary = current[summaryKey];
  return `# Omega-Mini Current State

Status: ${current.status}
Current active phase: ${current.current_active_phase}
Latest closed phase: ${current.latest_closed_phase}
Latest completed x1: ${current.latest_completed_x1_phase}
Latest completed x2: ${current.latest_completed_x2_phase}
Next expected scope: ${current.next_expected_scope}
Next x2 scope: ${current.next_x2_scope}
Next x1 lane after x2: ${current.next_x1_lane_after_x2}

## v553 v3 x1 Lumen Startup

- Status: \`${summary.status}\`
- Active lanes: \`${summary.active_lanes.join(", ")}\`
- Safe target: \`${summary.proposal_targets.safe}\`
- Candidate target: \`${summary.proposal_targets.candidate}\`
- Exact target: \`${summary.proposal_targets.exact}\`
- Blocked target: \`${summary.proposal_targets.blocked}\`
- Skill target: \`${summary.proposal_targets.skills}\`
- Runner target: \`${summary.proposal_targets.runners}\`
- Cleanup target: \`${summary.proposal_targets.cleanup}\`
- Web reflections: \`${summary.web_reflection_rows}\`
- Journey/phase reflections: \`${summary.journey_phase_reflection_rows}\`
- Lumen handoff: \`${summary.handoff_message_status}\`
- Goal mode status: \`${summary.goal_mode_status}\`

## Current Lookup Files

${(current.current_lookup_files || []).map((item) => `- ${item}`).join("\n")}

## Latest Action Summary

${(current.latest_action_summary || []).map((item) => `- ${item}`).join("\n")}

## Safety Boundary

${boundarySentence()}
`;
}

function renderBeaconMd(title, beacon, files) {
  const summary = beacon[summaryKey];
  return `# ${title}

Status: ${beacon.status}
Current active phase: ${beacon.current_active_phase}
Latest closed phase: ${beacon.latest_closed_phase}
Latest completed x1: ${beacon.latest_completed_x1_phase}
Latest completed x2: ${beacon.latest_completed_x2_phase}
Next expected scope: ${beacon.next_expected_scope}
Next x2 scope: ${beacon.next_x2_scope}
Next x1 lane after x2: ${beacon.next_x1_lane_after_x2}

## v553 v3 x1 Lumen Startup

- Status: \`${summary.status}\`
- Active lanes: \`${summary.active_lanes.join(", ")}\`
- Web reflection rows: \`${summary.web_reflection_rows}\`
- Journey/phase reflection rows: \`${summary.journey_phase_reflection_rows}\`
- Lumen handoff: \`${summary.handoff_message_status}\`

## Lookup Files

${(files || []).map((item) => `- ${item}`).join("\n")}

## Boundary

${boundarySentence()}
`;
}

function openBoundaries() {
  return {
    gmut_empirical_closure: "open_not_claimed",
    final_physics: "open_not_claimed",
    consciousness_proof: "open_not_claimed",
    legal_closure: "open_not_claimed",
    canon_promotion: "open_not_claimed",
    deployment_closure: "open_not_claimed",
    account_mutation: "open_requires_exact_approval",
    purchase: "open_requires_exact_approval",
    api_key_creation: "open_requires_exact_approval",
    private_material_proof: "open_not_published",
    sibling_identity_replacement_or_merge: "blocked_indefinitely",
  };
}

function publicationBoundary() {
  return {
    private_route_handles_published: false,
    private_lane_body_content_published: false,
    verbatim_conversation_logs_published: false,
    browser_routes_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    screenshots_published: false,
  };
}

function boundarySentence() {
  return "No private route handles, private lane body content, verbatim conversation logs, browser routes, credentials, local absolute paths, screenshots, proof closure, canon promotion, legal closure, deployment closure, account mutation, purchase, API-key creation, or sibling identity replacement are published or claimed.";
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
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
  })
    .formatToParts(date)
    .reduce((acc, part) => {
      acc[part.type] = part.value;
      return acc;
    }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
