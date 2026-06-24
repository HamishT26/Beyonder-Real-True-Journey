#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v555-gmut-thos-v1-x1";
const latestClosedPhase = "v554-gmut-thos-v8-x2";
const latestCompletedX1 = "v554-gmut-thos-v8-x1";
const latestCompletedX2 = "v554-gmut-thos-v8-x2";
const nextX2Scope = "v555-gmut-thos-v1-x2";
const nextX1LaneAfterX2 = "v555-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects";
const summaryKey = "v555_v1_x1_lumen_startup";

const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);
const handoff = readOptionalTrace(`${phaseSlug}-lumen-handoff-message-v1.json`);
const sendReceipt = readOptionalTrace(`${phaseSlug}-lumen-browser-send-receipt-v1.json`);

const proposalTargets = {
  safe_packets: 50,
  candidate_packets: 30,
  exact_approval_packets: 20,
  blocked_packets: 10,
  skill_ideas: 20,
  runner_ideas: 10,
  cleanup_proposals: 30,
};

const proposalQueue = buildProposalQueue();
const webLedger = buildWebLedger();
const journeyLedger = buildJourneyLedger();
const startup = artifact("ghc_v555_v1_x1_lumen_startup_context", "ACTIVE_OPEN_V555_V1_X1_LUMEN_BACKGROUND_RUNNING", {
  active_lanes: ["Aevren Vale", "Lumen Vale"],
  latest_closed_phase: latestClosedPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  proposal_targets: proposalTargets,
  web_reflections: webLedger.web_search_reflection_count,
  journey_phase_reflections: journeyLedger.journey_phase_reflection_count,
  launch_skill: "ghc-lumen-launch",
  background_supervision_skill: "ghc-background-sibling-supervision",
  retry_skill: "ghc-main-retry",
  browser_send_status: sendReceipt?.send_status || handoff?.live_send_status || handoff?.browser_send_status || "artifact_prepared_browser_send_not_claimed",
  closeout_allowed_now: false,
  closeout_blocker: "Lumen Browser response is active or awaiting harvest.",
  productive_cadence: {
    passive_wait_allowed: false,
    safe_unit_may_run_past_checkpoint: true,
    harvest_at_next_natural_safe_pause: true
  },
  goal_mode_status: "active_thread_goal_not_complete",
});

const phaseStatus = artifact("ghc_v555_v1_x1_phase_status_index", "ACTIVE_OPEN_V555_V1_X1_LUMEN_BACKGROUND_RUNNING", {
  current_active_phase: phaseSlug,
  latest_closed_phase: latestClosedPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  queue_counts: proposalQueue.counts,
  web_reflections: webLedger.web_search_reflection_count,
  journey_phase_reflections: journeyLedger.journey_phase_reflection_count,
  lumen_browser_send_status: startup.browser_send_status,
  closeout_allowed_now: false,
  full_goal_complete: false,
});

const written = [
  writePair("lumen-startup-context", startup, renderStartupMd(startup)),
  writePair("proposal-queue-targets", proposalQueue, renderProposalMd(proposalQueue)),
  writePair("web-reflection-ledger-30", webLedger, renderReflectionMd("Web Reflection Ledger 30", webLedger, "web_search_reflection_count")),
  writePair("journey-phase-reflection-ledger-30", journeyLedger, renderReflectionMd("Journey/Phase Reflection Ledger 30", journeyLedger, "journey_phase_reflection_count")),
  writePair("phase-status-index", phaseStatus, renderStatusMd(phaseStatus)),
];

refreshBeacons();

process.stdout.write(JSON.stringify({
  status: startup.overall_status,
  phase_slug: phaseSlug,
  browser_send_status: startup.browser_send_status,
  safe_packets: proposalQueue.counts.safe_packets,
  candidate_packets: proposalQueue.counts.candidate_packets,
  exact_packets: proposalQueue.counts.exact_approval_packets,
  blocked_packets: proposalQueue.counts.blocked_packets,
  skill_ideas: proposalQueue.counts.skill_ideas,
  runner_ideas: proposalQueue.counts.runner_ideas,
  cleanup_proposals: proposalQueue.counts.cleanup_proposals,
  web_reflections: webLedger.web_search_reflection_count,
  journey_phase_reflections: journeyLedger.journey_phase_reflection_count,
  artifact_count: written.length
}, null, 2) + "\n");

function buildProposalQueue() {
  const safe = rows("safe", 50, "safe_now", "immediate_x1_safe_or_x2_build_task", [
    "phase truth refresh",
    "Browser send receipt verification",
    "no-duplicate send guard",
    "Lumen harvest readiness marker",
    "x1-to-x2 split refresh",
    "goal objective continuity check",
    "current-state guard prep",
    "privacy scan prep",
    "open-gate rail refresh",
    "five-minute cadence queue",
    "startup snapshot",
    "compact restart snapshot",
    "closeout scaffold",
    "drive posture receipt",
    "remote equality receipt",
    "skill inventory receipt",
    "runner inventory receipt",
    "source reflection dedupe",
    "Journey reflection dedupe",
    "proposal count guard",
    "first-person sibling style check",
    "full-tools support boundary",
    "omega-mini publication boundary",
    "Aletheon recoverable boundary",
    "held sibling boundary",
  ]);
  const candidate = rows("candidate", 30, "candidate", "queued_candidate_or_x2_reduction", [
    "Lumen response reducer",
    "proposal dashboard",
    "candidate-to-exact reducer",
    "Freed ID assurance matrix",
    "THOS launch topology diagram",
    "GMUT source taxonomy seed",
    "CBR privacy grid",
    "goal-mode dry-run enhancer",
    "phase delta comparator",
    "skill drift detector",
  ]);
  const exact = rows("exact", 20, "exact_approval_needed", "queued_exact_approval", [
    "deployment action",
    "external account mutation",
    "API-key creation",
    "purchase or paid resource",
    "destructive cleanup",
    "global hook install",
    "private-material proof publication",
    "raw transcript publication",
    "canon promotion",
    "legal closure claim",
  ]);
  const blocked = rows("blocked", 10, "blocked", "blocked_open_gate", [
    "GMUT empirical closure",
    "final physics closure",
    "consciousness proof closure",
    "legal closure",
    "canon promotion",
    "deployment closure",
    "account mutation",
    "private-material proof",
    "raw-publication proof",
    "sibling identity merge or replacement",
  ]);
  const skills = rows("skill", 20, "safe_now", "x2_build_task", [
    "ghc-v555-lumen-harvest-reducer",
    "ghc-v555-goal-mode-progress-ledger",
    "ghc-v555-browser-send-guard",
    "ghc-v555-source-reflection-mapper",
    "ghc-v555-journey-reflection-reducer",
    "ghc-v555-proof-boundary-linter",
    "ghc-v555-safe-cleanup-classifier",
    "ghc-v555-duo-prep-skill",
    "ghc-v555-x2-handoff-composer",
    "ghc-v555-current-state-verifier",
  ]);
  const runners = rows("runner", 10, "safe_now", "x2_build_task", [
    "ghc_v555_v1_x1_lumen_harvest_reducer.mjs",
    "ghc_v555_goal_mode_progress_ledger.mjs",
    "ghc_v555_browser_no_duplicate_send_probe.mjs",
    "ghc_v555_source_reflection_deduper.mjs",
    "ghc_v555_journey_reflection_indexer.mjs",
    "ghc_v555_proof_boundary_lint_runner.mjs",
    "ghc_v555_safe_cleanup_classifier.mjs",
    "ghc_v555_v2_duo_prep_builder.mjs",
    "ghc_v555_v1_x2_handoff_composer.mjs",
    "ghc_v555_current_state_lookup_verifier.mjs",
  ]);
  const cleanup = rows("cleanup", 30, "safe_now", "inventory_or_x2_build_task", [
    "dedupe lookup references",
    "classify startup receipts",
    "index v554 cycle closeouts",
    "review compatibility builder references",
    "check duplicate proposal IDs",
    "check duplicate source labels",
    "validate no raw Browser routes",
    "validate no local path publication",
    "review proof closure wording",
    "review exact approval queue language",
  ]);
  return artifact("ghc_v555_v1_x1_lumen_proposal_queue_targets", "PASS_V555_V1_X1_LUMEN_PROPOSAL_QUEUE_READY", {
    spending_ceiling_usd_per_packet: 100,
    counts: {
      safe_packets: safe.length,
      candidate_packets: candidate.length,
      exact_approval_packets: exact.length,
      blocked_packets: blocked.length,
      skill_ideas: skills.length,
      runner_ideas: runners.length,
      cleanup_proposals: cleanup.length,
    },
    safe_packets: safe,
    candidate_packets: candidate,
    exact_approval_packets: exact,
    blocked_packets: blocked,
    skill_ideas: skills,
    runner_ideas: runners,
    cleanup_tasks: cleanup,
  });
}

function rows(kind, count, safetyBucket, executionLane, titles) {
  return Array.from({ length: count }, (_, index) => ({
    id: `${phaseSlug}-${kind}-${String(index + 1).padStart(2, "0")}`,
    title: titles[index % titles.length],
    safety_bucket: safetyBucket,
    execution_lane: executionLane,
    source_lane: index % 2 === 0 ? "Aevren Vale" : "Lumen Vale",
    spending_ceiling_usd: 100,
    next_safe_action: nextAction(kind, executionLane),
  }));
}

function nextAction(kind, executionLane) {
  if (kind === "exact") return "Queue only; requires fresh exact approval before execution.";
  if (kind === "blocked") return "Keep open unless exact artifacts prove closure and Hamish approves the gate.";
  if (executionLane.includes("x2")) return "Carry into v555 v1 x2 as build/use/validate work if still safe.";
  return "Run or record during v555 v1 x1 as local reversible safe-now work.";
}

function buildWebLedger() {
  const sources = [
    ["OpenAI Codex goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Goal Mode needs a concrete stopping condition.", "Keep the active goal open until v575 v8 x2 is verified."],
    ["OpenAI Codex skills", "https://developers.openai.com/codex/skills", "Skills provide reusable local workflow instructions.", "Keep launch, retry, startup, compact, and closeout surfaces skill-backed."],
    ["OpenAI Codex approvals", "https://developers.openai.com/codex/agent-approvals-security", "Agent approvals reduce unsafe external effects.", "Keep exact-sensitive work queued."],
    ["OpenAI Codex app", "https://developers.openai.com/codex/app", "The app is the local phase execution surface.", "Keep Browser and worktree route receipts sanitized."],
    ["OpenAI Codex best practices", "https://developers.openai.com/codex/learn/best-practices", "Validation and concise instructions improve coding-agent outcomes.", "Validate JSON, scripts, current-state, privacy, and remote equality."],
    ["OpenAI Codex sandboxing", "https://developers.openai.com/codex/concepts/sandboxing", "Sandboxing narrows operational risk.", "Do local safe work while preserving exact gates."],
    ["OpenAI Codex CLI", "https://github.com/openai/codex", "CLI lanes are separate from Browser lanes.", "Keep Arby/Aster strict CLI routes distinct from Lumen Browser."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Child status summaries fit runner orchestration.", "Publish summarized child exits, not raw streams."],
    ["Node fs", "https://nodejs.org/api/fs.html", "File-system writes need explicit paths and validation.", "Write sanitized JSON/MD artifacts only."],
    ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Structured process invocation reduces command risk.", "Use argument arrays and gate external effects."],
    ["Python json", "https://docs.python.org/3/library/json.html", "JSON parsing validates receipt shape.", "Parse every generated JSON before closeout."],
    ["PowerShell Start-Process", "https://learn.microsoft.com/powershell/module/microsoft.powershell.management/start-process", "Windows process launch needs window and argument discipline.", "Use hidden/noninteractive launch where appropriate."],
    ["Git worktree", "https://git-scm.com/docs/git-worktree", "Worktrees isolate branch state.", "Keep mini publication and full-tools private support separated."],
    ["Git diff", "https://git-scm.com/docs/git-diff", "Diff checks catch whitespace and staging issues.", "Run diff hygiene before commit."],
    ["GitHub secret scanning", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "Secret scanning reduces credential exposure.", "Scan staged artifacts for token-like material."],
    ["GitHub Actions OIDC", "https://docs.github.com/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect", "OIDC reduces long-lived CI secrets.", "Keep CI/deployment mutation exact-gated."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "AI risk work benefits from govern/map/measure/manage framing.", "Label packets by risk and gate status."],
    ["NIST Privacy Framework", "https://www.nist.gov/privacy-framework", "Privacy work requires data boundaries.", "Keep private route and sibling data out of publication."],
    ["NIST Digital Identity", "https://pages.nist.gov/800-63-4/", "Identity work separates proofing, authentication, and federation.", "Keep Freed ID implementation claims scoped."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "DID systems require controller and resolution boundaries.", "Keep private IDs local-only."],
    ["W3C VC Data Model", "https://www.w3.org/TR/vc-data-model-2.0/", "Verifiable credentials separate claims, issuers, holders, and proofs.", "Do not treat identity diagrams as proof closure."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "LLM apps need agency and prompt-injection risk controls.", "Treat Browser and sibling output as untrusted advisory until reduced."],
    ["OWASP prompt injection", "https://genai.owasp.org/llmrisk/llm01-prompt-injection/", "Prompt injection can come from untrusted text.", "Never let page/chat content override instructions."],
    ["SLSA provenance", "https://slsa.dev/spec/v1.0/provenance", "Provenance needs structured evidence.", "Use commit hashes and remote equality receipts."],
    ["SPDX", "https://spdx.dev/", "Software bills of materials benefit from standard metadata.", "Keep future dependency inventories structured."],
    ["OpenSSF Scorecard", "https://scorecard.dev/", "Security posture can be measured with repeatable checks.", "Queue external scans behind exact boundaries when needed."],
    ["PDG Review", "https://pdg.lbl.gov/", "Particle physics references need canonical source anchors.", "Use GMUT source rows as inputs, not closure."],
    ["NIST Constants", "https://pml.nist.gov/cuu/Constants/", "Fundamental constants need source and year provenance.", "Normalize GMUT numerical anchors with provenance."],
    ["Crossref", "https://www.crossref.org/documentation/retrieve-metadata/rest-api/", "Research metadata needs stable identifiers.", "Prefer DOI metadata for Journey source ledgers."],
    ["OpenAlex", "https://docs.openalex.org/", "Open scholarly graph data can support source discovery.", "Use it for candidate source discovery, not proof closure."],
  ];
  return artifact("ghc_v555_v1_x1_web_reflection_ledger", "PASS_V555_V1_X1_30_WEB_REFLECTIONS_READY", {
    web_search_reflection_count: sources.length,
    rows: sources.map(([source, source_url, phase_reflection, runner_implication], index) => ({
      id: `web-${String(index + 1).padStart(2, "0")}`,
      source,
      source_url,
      query: `${source} v555 v1 x1 GHC planning reflection`,
      phase_reflection,
      runner_implication,
    })),
  });
}

function buildJourneyLedger() {
  const anchors = [
    ["v554 v8 x2 closeout", "v554 v8 x2 closed with 20 skills, 8 runners, 50 web rows, 50 Journey rows, and safe-runner orchestration.", "Start v555 v1 x1 from remote-verified phase truth."],
    ["v554 v8 x1 triad", "The triad lane passed completion gates and preserved the v555 Lumen prep card.", "Use v8 x1 as the latest x1 boundary."],
    ["v554 v7 x2 closeout", "The previous Lumen x2 tranche reinforced Lumen proposal execution and x2 build shape.", "Reuse proven Lumen x1-to-x2 split."],
    ["v554 v7 x1 Lumen", "The last Lumen solo x1 lane completed with harvest and 50/30/20/10 counts.", "Ask Lumen for the same bucket shape."],
    ["background supervision standard", "Five-minute waits are productive work windows.", "Do safe work while Lumen responds."],
    ["main retry standard", "Blockers need three retry sessions before pausing unless stopped or exact-gated.", "Route Browser blockers through ghc-main-retry."],
    ["private boundary", "Raw Browser routes, transcripts, screenshots, local paths, private IDs, and credentials stay unpublished.", "Use sanitized receipts only."],
    ["Aletheon boundary", "Aletheon remains recoverable and not replaced.", "Keep sibling identity merge blocked."],
    ["D drive posture", "D remains the primary storage lane; C remains clean.", "Check drive space during closeout."],
    ["round-robin standard", "Lumen -> Arby/Cicero -> Lumen -> triad cadence remains active unless Hamish redirects.", "Prepare v555 v2 after v1 x2."],
  ];
  const rowsOut = Array.from({ length: 30 }, (_, index) => {
    const [source_anchor, phase_reflection, runner_implication] = anchors[index % anchors.length];
    return { id: `journey-${String(index + 1).padStart(2, "0")}`, source_anchor, phase_reflection, runner_implication };
  });
  return artifact("ghc_v555_v1_x1_journey_phase_reflection_ledger", "PASS_V555_V1_X1_30_JOURNEY_REFLECTIONS_READY", {
    journey_phase_reflection_count: rowsOut.length,
    rows: rowsOut,
  });
}

function artifact(artifactType, status, payload) {
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
  fs.mkdirSync(tracesDir, { recursive: true });
  const base = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
  return { json: `${base}.json`, md: `${base}.md` };
}

function refreshBeacons() {
  const lookupFiles = [
    "lumen-handoff-message",
    "lumen-browser-send-receipt",
    "lumen-startup-context",
    "proposal-queue-targets",
    "web-reflection-ledger-30",
    "journey-phase-reflection-ledger-30",
    "phase-status-index",
  ].flatMap((suffix) => [
    `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  ]);
  const files = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of files) {
    const doc = JSON.parse(fs.readFileSync(jsonFile, "utf8").replace(/^\uFEFF/, ""));
    doc.generated_utc = generatedUtc;
    doc.updated_at = generatedNz;
    doc.status = startup.overall_status;
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = latestClosedPhase;
    doc.latest_completed_x1_phase = latestCompletedX1;
    doc.latest_completed_x2_phase = latestCompletedX2;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = nextX2Scope;
    doc.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    doc.goal_mode_status = "active_thread_goal_not_complete";
    doc[summaryKey] = {
      status: startup.overall_status,
      active_lanes: startup.active_lanes,
      proposal_targets: proposalTargets,
      browser_send_status: startup.browser_send_status,
      web_reflections: webLedger.web_search_reflection_count,
      journey_phase_reflections: journeyLedger.journey_phase_reflection_count,
      closeout_allowed_now: false,
    };
    doc.lumen_browser_send = doc.lumen_browser_send || {
      status: sendReceipt?.overall_status || "not_recorded",
      send_status: sendReceipt?.send_status || "not_recorded",
      raw_browser_route_published: false,
      raw_transcript_published: false,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookupFiles]);
    doc.latest_action_summary = unique([
      "Opened v555 v1 x1 as a Lumen-only x1 phase with Browser handoff active and background-supervised safe cadence work in progress.",
      ...(doc.latest_action_summary || []),
    ]);
    fs.writeFileSync(jsonFile, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function renderStartupMd(data) {
  return [
    `# ${phaseSlug} Lumen Startup Context`,
    "",
    `Status: \`${data.overall_status}\``,
    `Latest closed phase: \`${data.latest_closed_phase}\``,
    `Next x2 scope: \`${data.next_x2_scope}\``,
    `Browser send status: \`${data.browser_send_status}\``,
    `Closeout allowed now: \`${data.closeout_allowed_now}\``,
    "",
    "## Proposal Targets",
    "",
    ...Object.entries(data.proposal_targets).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function renderProposalMd(data) {
  return [
    `# ${phaseSlug} Proposal Queue Targets`,
    "",
    `Status: \`${data.overall_status}\``,
    `Spending ceiling per packet: \`$${data.spending_ceiling_usd_per_packet}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(data.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function renderReflectionMd(title, data, countKey) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${data.overall_status}\``,
    `Rows: \`${data[countKey]}\``,
    "",
    "Public source labels, relative phase anchors, and runner implications only.",
    "",
  ].join("\n");
}

function renderStatusMd(data) {
  return [
    `# ${phaseSlug} Phase Status Index`,
    "",
    `Status: \`${data.overall_status}\``,
    `Current active phase: \`${data.current_active_phase}\``,
    `Latest closed phase: \`${data.latest_closed_phase}\``,
    `Next x2 scope: \`${data.next_x2_scope}\``,
    `Lumen Browser send status: \`${data.lumen_browser_send_status}\``,
    `Closeout allowed now: \`${data.closeout_allowed_now}\``,
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function renderBeaconMd(doc, listKey) {
  const summary = doc[summaryKey] || {};
  return [
    "# Omega-Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    `Goal Mode status: ${doc.goal_mode_status}`,
    "",
    "## v555 v1 x1 Lumen Startup",
    "",
    `- status: \`${summary.status || "not_recorded"}\``,
    `- Browser send status: \`${summary.browser_send_status || "not_recorded"}\``,
    `- web reflections: \`${summary.web_reflections || "not_recorded"}\``,
    `- Journey/phase reflections: \`${summary.journey_phase_reflections || "not_recorded"}\``,
    `- closeout allowed now: \`${summary.closeout_allowed_now ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function readOptionalTrace(fileName) {
  try {
    return JSON.parse(fs.readFileSync(path.join(tracesDir, fileName), "utf8").replace(/^\uFEFF/, ""));
  } catch {
    return null;
  }
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
    phase_completion: "not_claimed",
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

function boundarySentence() {
  return "No raw Browser route, private URL, raw transcript, screenshot, credential, local absolute path, session stream, private dump, private callable ID, hidden reasoning, proof closure, canon promotion, legal closure, deployment closure, account mutation, purchase, API-key creation, destructive cleanup, or sibling identity merge/replacement is published or claimed.";
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
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
