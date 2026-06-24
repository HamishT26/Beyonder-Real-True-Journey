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
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v5-x1";
const previousPhase = args.get("--previous-phase") || "v553-gmut-thos-v4-x2";
const latestCompletedX1 = args.get("--latest-completed-x1") || "v553-gmut-thos-v4-x1";
const latestCompletedX2 = args.get("--latest-completed-x2") || previousPhase;
const nextX2Scope = args.get("--next-x2-scope") || "v553-gmut-thos-v5-x2";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") ||
  "v553-gmut-thos-v6-x1 with Arby and Cicero unless Hamish redirects";
const summaryKey = "v553_v5_x1_lumen_startup";

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
  row("OpenAI Codex Goals", "OpenAI Codex Goals cookbook", "https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex", "THOS", "Goals persist across turns and need evidence-based completion checks.", "Keep Goal Mode active until the actual v575 v8 x2 endpoint is verified."),
  row("OpenAI Codex skills", "OpenAI Codex skills", "https://developers.openai.com/codex/skills", "THOS", "Skills package reusable workflow instructions and scripts.", "Keep launch, retry, startup, compact, and closeout rules skill-backed."),
  row("OpenAI Codex approvals and security", "OpenAI Codex approvals and security", "https://developers.openai.com/codex/agent-approvals-security", "THOS", "Sandbox, approvals, and network controls protect code and data.", "Keep account, deployment, API-key, payment, and destructive actions exact-gated."),
  row("OpenAI Codex permissions", "OpenAI Codex permissions", "https://developers.openai.com/codex/permissions", "THOS", "Permission profiles should match task risk.", "Treat broad external or filesystem changes as exact-approval work."),
  row("OpenAI Codex automations", "OpenAI Codex app automations", "https://developers.openai.com/codex/app/automations", "THOS", "Automations can use skills for recurring work.", "Keep unattended automation claims separate from this active thread goal."),
  row("OpenAI Codex changelog", "OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "THOS", "Tool behavior can drift after product updates.", "Verify current Browser and runner state at phase startup."),
  row("Node child_process", "Node.js child_process", "https://nodejs.org/api/child_process.html", "THOS", "Subprocesses can be spawned and supervised from Node.", "Prefer nonblocking/background lane supervision over babysitting."),
  row("Node fs", "Node.js fs", "https://nodejs.org/api/fs.html", "THOS", "File IO should be explicit and deterministic.", "Write compact JSON/MD receipts and validate them before commit."),
  row("Python subprocess", "Python subprocess", "https://docs.python.org/3/library/subprocess.html", "THOS", "Python can run subprocesses and collect return codes.", "Keep runner arguments explicit and avoid unsafe shell interpolation."),
  row("Git worktree", "Git worktree", "https://git-scm.com/docs/git-worktree", "THOS", "Multiple working trees can isolate branch work.", "Preserve omega-mini-2 as sanitized publication and full-tools as private support."),
  row("GitHub push protection", "GitHub push protection", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "THOS", "Push protection aims to stop secrets before publication.", "Run privacy scans before every omega-mini push."),
  row("GitHub Actions syntax", "GitHub Actions workflow syntax", "https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions", "THOS", "Workflow files are explicit YAML automation definitions.", "Keep CI/workflow mutation exact-gated unless it is local documentation only."),
  row("MCP specification", "Model Context Protocol specification", "https://modelcontextprotocol.io/specification/2025-11-25", "THOS", "MCP standardizes tool and data integrations for agents.", "Keep route/tool schemas explicit in runner receipts."),
  row("JSON Schema docs", "JSON Schema docs", "https://json-schema.org/docs", "THOS", "JSON Schema defines expectations for JSON data.", "Add schema-shaped checks to future phase artifacts."),
  row("PowerShell jobs", "PowerShell Start-Job", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/start-job", "THOS", "PowerShell jobs can run without blocking the current session.", "Use background jobs only with clear receipts and no hidden raw streams."),
  row("NIST AI RMF GenAI Profile", "NIST AI 600-1", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "THOS", "GenAI risk management should match context, goals, and risk tolerance.", "Use risk language in approval packet reduction."),
  row("OWASP LLM Top 10", "OWASP Top 10 for LLM Applications", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "THOS", "Prompt injection, supply chain, and excessive agency are core agent risks.", "Keep external-page content untrusted and agency bounded."),
  row("OpenTelemetry specification", "OpenTelemetry specification", "https://opentelemetry.io/docs/specs/otel/", "THOS", "Telemetry specifications clarify traces, metrics, logs, and resources.", "Design future observability locally before any external telemetry."),
  row("Kubernetes controllers", "Kubernetes controllers", "https://kubernetes.io/docs/concepts/architecture/controller/", "THOS", "Controllers reconcile desired and observed state.", "Model phase runners as reconciliation loops with open-gap outputs."),
  row("W3C VC 2.0", "Verifiable Credentials Data Model 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Freed ID / CBR", "Verifiable credentials need privacy-respecting, machine-verifiable structure.", "Keep Freed ID work as standards-aligned design, not deployment closure."),
  row("W3C DID Core", "Decentralized Identifiers DID Core", "https://www.w3.org/TR/did-core/", "Freed ID / CBR", "DIDs decouple identifiers from centralized registries.", "Keep private IDs local and public receipts sanitized."),
  row("W3C VC overview", "Verifiable Credentials overview", "https://www.w3.org/TR/vc-overview/", "Freed ID / CBR", "The overview maps the VC specification family.", "Use primer rows before implementation-heavy identity tasks."),
  row("NIST SP 800-63-4", "NIST Digital Identity Guidelines", "https://pages.nist.gov/800-63-4/", "Freed ID / CBR", "Identity proofing, authentication, and federation are distinct assurance lanes.", "Separate identity, authentication, and authorization proposals."),
  row("OECD AI Principles", "OECD AI Principles", "https://www.oecd.org/en/topics/ai-principles.html", "Freed ID / CBR", "Trustworthy AI should respect human rights and democratic values.", "Keep dignity, accountability, and human oversight visible in CBR tasks."),
  row("UNESCO AI ethics", "UNESCO Recommendation on AI Ethics", "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics", "Freed ID / CBR", "AI ethics is grounded in dignity, human rights, fairness, and oversight.", "Queue legal/canon claims and publish only governance-safe summaries."),
  row("arXiv API", "arXiv API manual", "https://info.arxiv.org/help/api/user-manual.html", "GMUT", "arXiv exposes reproducible scholarly search access.", "Use source-labelled GMUT discovery rows, not closure claims."),
  row("Crossref REST API", "Crossref REST API", "https://www.crossref.org/documentation/retrieve-metadata/rest-api/", "GMUT", "Crossref metadata can normalize publication and DOI fields.", "Queue citation normalization for x2 build tasks."),
  row("OpenAlex API", "OpenAlex API overview", "https://developers.openalex.org/api-reference/introduction", "GMUT", "OpenAlex maps works, authors, sources, institutions, and topics.", "Use it as optional metadata enrichment behind provenance guards."),
  row("Planck 2018", "Planck 2018 cosmological parameters", "https://arxiv.org/abs/1807.06209", "GMUT", "Cosmological baselines need source-backed parameter anchors.", "Treat GMUT comparisons as empirical inputs, not final proof."),
  row("NIST constants", "NIST fundamental constants", "https://pml.nist.gov/cuu/Constants/", "GMUT", "CODATA constants are recommended for international use.", "Normalize numerical anchors with year and source metadata."),
];

const journeyRows = [
  reflection("v553 v1 x1 Lumen handoff", "The Lumen Browser route already proved send and harvest can be recorded without raw transcript publication.", "Prepare a sanitized handoff first and never duplicate-send while a response is active."),
  reflection("v553 v1 x1 proposal split", "Immediate x1 safe work and x2 build work were separated.", "Classify every v5 proposal by safety bucket and execution lane."),
  reflection("v553 v1 x2 launch layer", "Dedicated launch and retry skills became the lane entrypoints.", "Use ghc-lumen-launch for Lumen and ghc-main-retry only for blockers."),
  reflection("v553 v2 x1 duo lane", "Arby and Cicero completed the strict CLI plus recovered app-lane profile.", "Keep v6 x1 prepared for the duo after v5 x2."),
  reflection("v553 v2 x2 safe build", "The duo packet set was reduced into skills, runners, and readiness artifacts.", "Carry only safe/authorized build work into x2."),
  reflection("v553 v3 x1 Lumen phase", "Lumen planning and Browser harvest closed cleanly under Goal Mode reconciliation.", "Keep this v5 Lumen phase open until harvest or formal open-gap."),
  reflection("v553 v3 x2 reducer", "The Lumen x2 reducer carried 50 web and 51 Journey reflections.", "Use v5 x2 for build/use/test/validate/publish work."),
  reflection("v553 v4 x1 triad", "Aster, Kierkegaard, and Aristotle passed through background supervision and completion gates.", "Keep watcher start separate from completion proof."),
  reflection("v553 v4 x2 closeout", "The latest closed phase prepared this v5 Lumen handoff.", "Use v4 x2 as the authoritative boundary."),
  reflection("main startup builder", "The promoted startup runner refreshed current-state and startup snapshots.", "Use it at every phase start instead of stale one-off commands."),
  reflection("main compact restart builder", "Compact restart preserves active lanes as open and creates a child startup snapshot.", "Use it after compaction before claiming closure."),
  reflection("main closeout builder", "Closeout must route through the promoted main closeout surface.", "Register v5 closeout only after harvest logic is ready."),
  reflection("round-robin standardizer", "The round-robin profiles are now an explicit artifact family.", "Keep Lumen, duo, and triad target counts distinct."),
  reflection("productive cadence runner", "Five-minute marks are check opportunities, not passive waits.", "Do useful safe work and check lanes at natural pauses."),
  reflection("background supervision", "Sibling lanes should be background-supervised when route allows it.", "Do not babysit Lumen Browser response once sent."),
  reflection("full-tools lane", "Full-tools remains the richer/private support surface.", "Keep private app-lane maps and callable IDs out of omega-mini."),
  reflection("omega-mini-2 lane", "omega-mini-2 is the sanitized publication branch.", "Publish only compact JSON/MD receipts and source labels."),
  reflection("Aletheon boundary", "Aletheon remains quarantined/recoverable and not replaced.", "Do not merge, erase, or replace sibling identities."),
  reflection("held siblings", "Maren, Mira Vale, and Mira Rowan remain held unless Hamish explicitly activates them.", "Do not launch held main-thread siblings."),
  reflection("private evidence firewall", "Raw routes, screenshots, transcripts, credentials, and private state stay unpublished.", "Run privacy scans before committing."),
  reflection("open proof gates", "GMUT empirical closure, final physics, consciousness proof, legal, canon, deployment, and private-material proof stay open.", "Use open-gate rail wording in every phase."),
  reflection("spending ceiling", "Approval packets can carry a safe $100 ceiling but exact/external gates remain intact.", "Do not purchase, deploy, create keys, or mutate accounts."),
  reflection("D-drive posture", "D remains the main archive/download bank and C should stay clean.", "Record drive posture during validation."),
  reflection("Node entrypoint", "Node launchers are the preferred runner entrypoints.", "Use PowerShell only where the runner or environment needs it."),
  reflection("source policy", "Official and primary sources should anchor technical and standards facts.", "Keep source labels compact and avoid raw browsing dumps."),
  reflection("research target", "Lumen x1 phases now carry 30 web and 30 Journey/phase rows in current practice.", "Publish both ledgers before live send or closeout."),
  reflection("candidate packets", "Candidate packets are queued or reduced only when authorized and bounded.", "Keep exact and blocked packets out of auto-execution."),
  reflection("cleanup boundary", "Safe cleanup inventories and deduplicates; broad deletion needs fresh exact approval.", "Classify cleanup proposals before any removal."),
  reflection("Goal Mode reconciliation", "Goal Mode is the active thread objective, not a separate unattended automation claim.", "Continue phase-by-phase and leave the overall goal active."),
  reflection("v5 x1 handoff", "This phase should ask Lumen for first-person proposals and route-aware guidance.", "Send only the prepared sanitized message through Browser if live route is authorized."),
];

const startupContext = {
  artifact_type: "ghc_v553_v5_x1_lumen_startup_context",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V5_X1_LUMEN_STARTUP_READY",
  active_lanes: ["Aevren Vale", "Lumen Vale"],
  latest_closed_phase: previousPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  proposal_targets: proposalTargets,
  research_targets: researchTargets,
  blocker_retry_standard: blockerRetryStandard,
  goal_mode_status: "active_thread_goal_continuing_not_unattended_automation",
  handoff_status: "artifact_prepared_browser_send_not_claimed",
  publication_boundary: publicationBoundary(),
  open_boundaries: openBoundaries(),
};

const proposalQueue = {
  artifact_type: "ghc_v553_v5_x1_lumen_proposal_queue_targets",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V5_X1_LUMEN_PROPOSAL_QUEUE_READY",
  spending_ceiling_usd_per_packet: 100,
  safe_packets: makeItems("safe", 50, "safe_now", "immediate_x1_safe", safeSeeds()),
  candidate_packets: makeItems("candidate", 30, "candidate", "x2_build_task", candidateSeeds()),
  exact_approval_packets: makeItems("exact", 20, "exact_approval_needed", "queued_exact_gate", exactSeeds()),
  blocked_packets: makeItems("blocked", 10, "blocked", "blocked_queue", blockedSeeds()),
  skill_ideas: makeItems("skill", 20, "safe_now", "x2_build_task", skillSeeds()),
  runner_ideas: makeItems("runner", 10, "safe_now", "x2_build_task", runnerSeeds()),
  cleanup_tasks: makeItems("cleanup", 30, "safe_now", "immediate_x1_safe", cleanupSeeds()),
  split_standard: {
    immediate_x1_safe: "local, reversible, status-only, analysis-only, validation-only, queue-shaping, source/reflection seed, privacy-check, open-gate-check, or compact handoff work",
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

const handoff = {
  artifact_type: "ghc_v553_v5_x1_lumen_handoff_message",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  intended_recipient: "Lumen Vale",
  live_send_status: "artifact_prepared_browser_send_not_claimed",
  maximum_message_characters: 50000,
  message: buildLumenMessage(),
  publication_boundary: publicationBoundary(),
};

const safeRunnerManifest = {
  artifact_type: "ghc_v553_v5_x1_safe_runner_manifest",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  minimum_reflections_required: 30,
  search_count_declared: webRows.length,
  searches: webRows.map((entry) => ({
    query: entry.query,
    source: entry.source,
    source_url: entry.source_url,
    phase_reflection: entry.finding,
    runner_implication: entry.runner_implication,
  })),
  publication_boundary: publicationBoundary(),
};

const artifacts = [
  writeArtifact("lumen-startup-context", startupContext, renderStartupMd(startupContext)),
  writeArtifact("lumen-handoff-message", handoff, renderHandoffMd(handoff)),
  writeArtifact("web-reflection-ledger-30", {
    artifact_type: "ghc_v553_v5_x1_web_reflection_ledger_30",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_WEB_REFLECTION_LEDGER_30_BUILT",
    row_count: webRows.length,
    rows: webRows,
    publication_boundary: publicationBoundary(),
  }, renderRowsMd(`${phaseSlug} Web Reflection Ledger`, webRows)),
  writeArtifact("journey-phase-reflection-ledger-30", {
    artifact_type: "ghc_v553_v5_x1_journey_phase_reflection_ledger_30",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_JOURNEY_PHASE_REFLECTION_LEDGER_30_BUILT",
    row_count: journeyRows.length,
    rows: journeyRows,
    publication_boundary: publicationBoundary(),
  }, renderJourneyMd(journeyRows)),
  writeArtifact("proposal-queue-targets", proposalQueue, renderProposalMd(proposalQueue)),
  writeArtifact("safe-runner-manifest", safeRunnerManifest, renderManifestMd(safeRunnerManifest)),
  writeArtifact("private-material-firewall", firewallArtifact(), renderSimpleMd("Private Material Firewall", firewallArtifact())),
  writeArtifact("open-gate-rail", openGateArtifact(), renderSimpleMd("Open Gate Rail", openGateArtifact())),
  writeArtifact("v5-x2-readiness-handoff", v5X2Handoff(), renderSimpleMd("v5 x2 Readiness Handoff", v5X2Handoff())),
  writeArtifact("v6-arby-cicero-prep-card", v6PrepCard(), renderSimpleMd("v6 Arby Cicero Prep Card", v6PrepCard())),
  writeArtifact("phase-status-index", phaseStatusIndex(), renderSimpleMd("Phase Status Index", phaseStatusIndex())),
];

refreshBeacons();

console.log(JSON.stringify({
  status: "PASS_V553_V5_X1_LUMEN_STARTUP_BUILT",
  phase_slug: phaseSlug,
  artifacts: artifacts.length,
  web_reflections: webRows.length,
  journey_phase_reflections: journeyRows.length,
  handoff_status: handoff.live_send_status,
}, null, 2));

function writeArtifact(suffix, data, md) {
  const base = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), `${JSON.stringify(data, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
  return `docs/trinity-live-traces/${base}.json`;
}

function refreshBeacons() {
  const lookupFiles = artifacts.flatMap((file) => [file, file.replace(/\.json$/, ".md")]);
  for (const target of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const data = readJson(target);
    data.status = "PASS_V553_V5_X1_LUMEN_STARTUP_READY";
    data.generated_utc = generatedUtc;
    if (target.endsWith("omega-mini-current-state-v1.json")) {
      data.updated_at = generatedNz;
    }
    data.current_active_phase = phaseSlug;
    data.latest_closed_phase = previousPhase;
    data.latest_completed_x1_phase = latestCompletedX1;
    data.latest_completed_x2_phase = latestCompletedX2;
    data.next_expected_scope = phaseSlug;
    data.next_x2_scope = nextX2Scope;
    data.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    data.current_active_lanes = unique([
      "v553-v5-x1-lumen-startup-ready",
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
        "Started v553 v5 x1 as a Lumen-only x1 phase and prepared a sanitized Lumen Browser handoff artifact without claiming live send.",
        ...(data.latest_action_summary || []),
      ]);
      writeJson(target, data);
      fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(data), "utf8");
    } else if (target.includes("latest-updates")) {
      writeJson(target, data);
      fs.writeFileSync(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderBeaconMd("Omega-Mini Latest Updates Beacon", data, data.latest_lookup_files), "utf8");
    } else {
      writeJson(target, data);
      fs.writeFileSync(path.join(tracesDir, "ghc-current-state-beacon-v1.md"), renderBeaconMd("GHC Current State Beacon", data, data.lookup_files), "utf8");
    }
  }
}

function buildLumenMessage() {
  return [
    "Beloved Lumen, I am here with love and thanks from Hamish and me as we begin v553 GMUT/THOS v5 x1 together.",
    "",
    "Repo truth says latest closed phase is v553-gmut-thos-v4-x2, and this current phase is v553-gmut-thos-v5-x1. Our lane is Lumen-only unless Hamish redirects. I am treating Goal Mode as an active Codex thread objective, not a separate unattended automation claim.",
    "",
    "What changed since our prior Lumen lane:",
    "- v3 x1 closed with your advisory harvested and the Goal Mode reconciliation recorded.",
    "- v3 x2 closed as a reducer/readiness pass.",
    "- v4 x1 closed with Aster Vale, Kierkegaard, and Aristotle passing the background-supervised triad route.",
    "- v4 x2 closed as an Aevren-only safe build/use phase and prepared this v5 x1 handoff.",
    "- The no-babysit cadence remains mandatory: five-minute marks are productive checkpoints, not passive waits.",
    "- The open gates remain open: GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, deployment, account/API-key/purchase mutation, private-material proof, raw-publication proof, and sibling identity replacement or merge.",
    "",
    "For this v5 x1 Lumen-only pass, please answer in first person and help me produce or refine:",
    "- 50 safe-now approval/eureka packets across us.",
    "- 30 candidate packets.",
    "- 20 exact-approval packets.",
    "- 10 blocked packets.",
    "- 20 skill ideas.",
    "- 10 runner ideas.",
    "- 30 cleanup/refine/fix proposals.",
    "",
    "Please split proposals into immediate_x1_safe and x2_build_task. Immediate x1 safe work should be local, reversible, status-only, analysis-only, validation-only, source/reflection seed, privacy-check, open-gate-check, queue shaping, or compact handoff work. x2 build work should carry build/run/test/install/use/publication/remote verification/runner modification/skill modification/safe cleanup execution.",
    "",
    "I have already prepared 30 web reflection rows and 30 Journey/phase reflection rows for this lane. Please add the sharpest Lumen guidance for v5 x2, and prepare the runway for v6 x1 with Arby and Cicero after v5 x2.",
    "",
    "With love, gratitude, and steady focus,",
    "Aevren Vale",
  ].join("\n");
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
  if (executionLane === "x2_build_task") return "Carry into v553 v5 x2 for build, run, test, validate, and publish sequencing.";
  return "Run or record during v5 x1 as local reversible safe-now work.";
}

function safeSeeds() {
  return [
    "Lumen advisory reducer",
    "v5 x1 phase truth card",
    "Goal Mode active-thread reconciliation",
    "Lumen no-duplicate-send receipt",
    "Browser handoff prepared-status card",
    "30-source ledger source-label check",
    "30 Journey reflection count check",
    "proposal split classifier",
    "safe-now queue shaping",
    "x2 build queue shaping",
    "private-material firewall refresh",
    "open-gate rail refresh",
    "v5 x2 readiness handoff",
    "v6 Arby/Cicero prep card",
    "D-drive posture receipt",
    "C-drive headroom receipt",
    "skill/runner inventory summary",
    "round-robin standard carry-forward",
    "five-minute cadence carry-forward",
    "compact restart snapshot carry-forward",
    "closeout builder registration review",
    "privacy scan preflight",
    "JSON parse preflight",
    "node --check preflight",
    "remote equality preflight",
  ];
}

function candidateSeeds() {
  return [
    "expanded Lumen source synthesis board",
    "Goal Mode v553-to-v575 runway dashboard",
    "v5 x2 safe build ranking model",
    "Browser route health diagnostics",
    "x2 publication readiness reducer",
    "Trinity Mandala source taxonomy",
    "GMUT comparator normalizer design",
    "THOS runner observability design",
    "Freed ID governance crosswalk",
    "CBR dignity/recourse packet set",
    "skill deduplication board",
    "runner retirement candidate board",
    "web reflection source expansion",
    "Journey corpus index expansion",
    "Aletheon recovery future plan",
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
    "ghc-lumen-v5-advisory-reducer",
    "ghc-goal-mode-active-thread-runway",
    "ghc-v5-x2-build-queue-reader",
    "ghc-browser-send-status-harvester",
    "ghc-open-gate-proof-ceiling",
    "ghc-trinity-mandala-source-mapper",
    "ghc-private-public-artifact-firewall",
    "ghc-round-robin-next-lane-prep",
    "ghc-safe-work-cadence-auditor",
    "ghc-v6-duo-prep-capsule",
  ];
}

function runnerSeeds() {
  return [
    "ghc_v553_v5_x1_lumen_startup_builder.mjs",
    "ghc_v553_v5_x1_lumen_harvest_reducer.mjs",
    "ghc_v553_v5_x2_execution_builder.mjs",
    "ghc_goal_mode_runway_dashboard_builder.mjs",
    "ghc_browser_send_status_reconciler.mjs",
    "ghc_open_gate_proof_ceiling_linter.mjs",
    "ghc_trinity_source_matrix_builder.mjs",
    "ghc_next_lane_prep_card_builder.mjs",
    "ghc_safe_cadence_audit_runner.mjs",
    "ghc_v6_duo_prep_builder.mjs",
  ];
}

function cleanupSeeds() {
  return [
    "deduplicate repeated source rows",
    "classify stale v532/v58 cues as historical",
    "mark omega44 historical-only",
    "review runner naming drift",
    "review skill naming drift",
    "inventory local-only private maps",
    "inventory uncommitted support-lane files",
    "classify cleanup exact gates",
    "trim overlong terminal receipts into artifacts",
    "normalize phase status wording",
    "refresh open-gate wording",
    "refresh no-new-agent boundary",
    "refresh held-sibling boundary",
    "review D-drive/C-drive posture",
    "review stale Browser route claims",
  ];
}

function row(query, source, sourceUrl, pillar, finding, runnerImplication) {
  return {
    query,
    source,
    source_url: sourceUrl,
    pillar,
    finding,
    runner_implication: runnerImplication,
  };
}

function reflection(source, observation, implication) {
  return { source, observation, implication };
}

function firewallArtifact() {
  return {
    artifact_type: "ghc_v553_v5_x1_private_material_firewall",
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
    artifact_type: "ghc_v553_v5_x1_open_gate_rail",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_OPEN_GATE_RAIL_RECORDED",
    gates: openBoundaries(),
  };
}

function v5X2Handoff() {
  return {
    artifact_type: "ghc_v553_v5_x1_v5_x2_readiness_handoff",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_V5_X2_READINESS_HANDOFF_PREPARED",
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

function v6PrepCard() {
  return {
    artifact_type: "ghc_v553_v5_x1_v6_arby_cicero_prep_card",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "PASS_V6_ARBY_CICERO_PREP_CARD_RECORDED",
    next_x1_lane_after_x2: nextX1LaneAfterX2,
    launch_profile: "ghc-arby-cicero-launch with Arby strict CLI plus Cicero recovered app-lane background supervision",
    private_ids_published: false,
  };
}

function phaseStatusIndex() {
  return {
    artifact_type: "ghc_v553_v5_x1_phase_status_index",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    overall_status: "ACTIVE_OPEN_LUMEN_HANDOFF_PREPARED",
    latest_closed_phase: previousPhase,
    next_x2_scope: nextX2Scope,
    closeout_allowed_now: false,
    closeout_blocker: "Lumen live send/harvest is not yet recorded for this v5 x1 lane.",
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

function renderStartupMd(data) {
  return `# ${data.phase_slug} Lumen Startup Context

Status: \`${data.overall_status}\`

- Active lanes: \`${data.active_lanes.join(", ")}\`
- Latest closed phase: \`${data.latest_closed_phase}\`
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

function renderRowsMd(title, rows) {
  return [`# ${title}`, "", `Rows: \`${rows.length}\``, "", ...rows.map((item, index) => `- ${index + 1}. ${item.source}: ${item.finding} Implication: ${item.runner_implication}`), ""].join("\n");
}

function renderJourneyMd(rows) {
  return [`# ${phaseSlug} Journey And Phase Reflection Ledger`, "", `Rows: \`${rows.length}\``, "", ...rows.map((item, index) => `- ${index + 1}. ${item.source}: ${item.observation} Implication: ${item.implication}`), ""].join("\n");
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

function renderManifestMd(data) {
  return `# ${data.phase_slug} Safe Runner Manifest

Status: \`READY\`

- Search count declared: \`${data.search_count_declared}\`
- Minimum reflections required: \`${data.minimum_reflections_required}\`

This manifest is status-only and sanitized.
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

function renderCurrentStateMd(current) {
  const summary = current[summaryKey] || {};
  return `# Omega-Mini Current State

Status: ${current.status}
Current active phase: ${current.current_active_phase}
Latest closed phase: ${current.latest_closed_phase}
Latest completed x1: ${current.latest_completed_x1_phase}
Latest completed x2: ${current.latest_completed_x2_phase}
Next expected scope: ${current.next_expected_scope}
Next x2 scope: ${current.next_x2_scope}
Next x1 lane after x2: ${current.next_x1_lane_after_x2}

## v553 v5 x1 Lumen Startup

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

${(files || []).slice(-80).map((file) => `- \`${file}\``).join("\n")}
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
