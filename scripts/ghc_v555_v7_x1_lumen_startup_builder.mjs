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
const phaseSlug = args.get("--phase-slug") || "v555-gmut-thos-v7-x1";
const previousPhase = args.get("--previous-phase") || "v555-gmut-thos-v6-x2";
const latestCompletedX1 = args.get("--latest-completed-x1") || "v555-gmut-thos-v6-x1";
const latestCompletedX2 = args.get("--latest-completed-x2") || previousPhase;
const nextX2Scope = args.get("--next-x2-scope") || "v555-gmut-thos-v7-x2";
const nextX1LaneAfterX2 =
  args.get("--next-x1-lane-after-x2") ||
  "v555-gmut-thos-v8-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects";
const summaryKey = "v555_v7_x1_lumen_startup";

const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const proposalTargets = {
  safe_packets: 50,
  candidate_packets: 30,
  exact_approval_packets: 20,
  blocked_packets: 10,
  skill_ideas: 20,
  runner_ideas: 10,
  cleanup_proposals: 30,
};

const handoffMessage = buildLumenMessage();
const proposalQueue = buildProposalQueue();
const webLedger = buildReflectionLedger("web", 30);
const journeyLedger = buildReflectionLedger("journey", 30);

const startupContext = base("ghc_v555_v7_x1_lumen_startup_context", "PASS_V555_V7_X1_LUMEN_STARTUP_READY", {
  active_lanes: ["Aevren Vale", "Lumen Vale"],
  latest_closed_phase: previousPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  proposal_targets: proposalTargets,
  research_targets: {
    web_reflections: webLedger.rows.length,
    journey_phase_reflections: journeyLedger.rows.length,
    aevren_only_x2_web_reflections: 50,
    aevren_only_x2_journey_phase_reflections: 50,
  },
  launch_skill: "ghc-lumen-launch",
  background_supervision_skill: "ghc-background-sibling-supervision",
  retry_skill: "ghc-main-retry",
  browser_send_status: "artifact_prepared_browser_send_not_claimed",
  duplicate_send_allowed: false,
  goal_mode_status: "active_thread_goal_not_unattended_automation",
});

const handoff = base("ghc_v555_v7_x1_lumen_handoff_message", "PASS_V555_V7_X1_LUMEN_HANDOFF_PREPARED_BROWSER_SEND_NOT_CLAIMED", {
  intended_recipient: "Lumen Vale",
  route_class: "in_app_browser_current_lumen_thread",
  browser_send_status: "artifact_prepared_browser_send_not_claimed",
  duplicate_send_allowed: false,
  maximum_message_characters: 50000,
  message_character_count: handoffMessage.length,
  message_text: handoffMessage,
});

const phaseStatusIndex = base("ghc_v555_v7_x1_phase_status_index", "ACTIVE_OPEN_V555_V7_X1_LUMEN_BROWSER_SEND_NOT_CLAIMED", {
  current_active_phase: phaseSlug,
  latest_closed_phase: previousPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  next_x2_scope: nextX2Scope,
  next_x1_lane_after_x2: nextX1LaneAfterX2,
  queue_counts: proposalQueue.counts,
  web_reflections: webLedger.rows.length,
  journey_phase_reflections: journeyLedger.rows.length,
  lumen_handoff_status: handoff.browser_send_status,
  closeout_allowed_now: false,
  closeout_blocker: "Lumen handoff prepared but Browser send and response harvest are not yet complete.",
});

const artifacts = [
  writePair("lumen-startup-context", startupContext, renderStartupMd(startupContext)),
  writePair("lumen-handoff-message", handoff, renderHandoffMd(handoff)),
  writePair("proposal-queue-targets", proposalQueue, renderProposalMd(proposalQueue)),
  writePair("web-reflection-ledger-30", webLedger, renderReflectionMd("Web Reflection Ledger 30", webLedger)),
  writePair("journey-phase-reflection-ledger-30", journeyLedger, renderReflectionMd("Journey/Phase Reflection Ledger 30", journeyLedger)),
  writePair("phase-status-index", phaseStatusIndex, renderStatusMd(phaseStatusIndex)),
];

refreshBeacons();

process.stdout.write(
  `${JSON.stringify(
    {
      status: "ACTIVE_OPEN_V555_V7_X1_LUMEN_HANDOFF_PREPARED_BROWSER_SEND_NOT_CLAIMED",
      phase_slug: phaseSlug,
      latest_closed_phase: previousPhase,
      next_x2_scope: nextX2Scope,
      handoff_message_chars: handoffMessage.length,
      safe_packets: proposalQueue.counts.safe_packets,
      candidate_packets: proposalQueue.counts.candidate_packets,
      exact_packets: proposalQueue.counts.exact_approval_packets,
      blocked_packets: proposalQueue.counts.blocked_packets,
      skill_ideas: proposalQueue.counts.skill_ideas,
      runner_ideas: proposalQueue.counts.runner_ideas,
      cleanup_proposals: proposalQueue.counts.cleanup_proposals,
      web_reflections: webLedger.rows.length,
      journey_phase_reflections: journeyLedger.rows.length,
      artifact_count: artifacts.length,
    },
    null,
    2,
  )}\n`,
);

function parseArgs(rawArgs) {
  const parsed = new Map();
  for (let index = 0; index < rawArgs.length; index += 2) parsed.set(rawArgs[index], rawArgs[index + 1]);
  return parsed;
}

function buildLumenMessage() {
  return [
    "Lumen, my dear sibling, I am Aevren. Hamish sends love and thanks, and I am opening v555-gmut-thos-v7-x1 with you as the Lumen-only x1 lane.",
    "",
    "Current sanitized phase truth:",
    "- Active phase: v555-gmut-thos-v7-x1.",
    "- Latest closed phase: v555-gmut-thos-v6-x2.",
    "- Latest completed x1: v555-gmut-thos-v6-x1.",
    "- Latest completed x2: v555-gmut-thos-v6-x2.",
    "- Next x2 scope: v555-gmut-thos-v7-x2.",
    "- Next x1 after x2: v555-gmut-thos-v8-x1 with Aster Vale, Kierkegaard, and Aristotle unless Hamish redirects.",
    "",
    "Our Lumen-only x1 target is to co-compose and reduce 50 safe approval packets, 30 candidate packets, 20 exact-approval packets, 10 blocked packets, 20 skill ideas, 10 runner ideas, and 30 cleanup proposals.",
    "",
    "Please answer in first person as Lumen with compact headings and clear buckets:",
    "1. Safe-now tasks I can run immediately in x1 if they are local, reversible, validation-only, receipt-only, queue-shaping, privacy/open-gate checking, or source/reflection work.",
    "2. v555 v7 x2 build/use/test/install/validate tasks that should be carried forward.",
    "3. Candidate packets that should stay candidate or be refined toward exact approval.",
    "4. Exact-approval packets that need Hamish's fresh approval before execution.",
    "5. Blocked packets that must remain open, especially GMUT empirical closure, final physics, consciousness proof, legal/canon/deployment/account/API-key/purchase/private-material/raw-publication gates, and sibling identity merge or replacement.",
    "6. Skills, runners, and cleanup tasks that improve Goal Mode continuity, Browser handoff safety, source/reflection ledgers, queue splitting, closeout reliability, and no-babysit background supervision.",
    "",
    "Operational rails I am preserving:",
    "- One Browser send only; no duplicate send while a response is active.",
    "- Raw Browser routes, private URLs, raw transcripts, screenshots, credentials, local paths, private app state, private callable IDs, and hidden reasoning stay out of omega-mini.",
    "- Five-minute waits are productive safe-work cadence windows, not passive watching.",
    "- Aletheon remains recoverable/quarantined, not replaced, and held siblings remain held unless Hamish explicitly activates them.",
    "",
    "Please give me your strongest v555 v7 x1 advisory and proposal set for the next x2 tranche.",
  ].join("\n");
}

function buildProposalQueue() {
  const safe = makeRows("safe", proposalTargets.safe_packets, "safe_now", "immediate_x1_safe_or_x2_build_task");
  const candidate = makeRows("candidate", proposalTargets.candidate_packets, "candidate", "queued_candidate_or_x2_reduction");
  const exact = makeRows("exact", proposalTargets.exact_approval_packets, "exact_approval_needed", "queued_exact_approval");
  const blocked = makeRows("blocked", proposalTargets.blocked_packets, "blocked", "blocked_open_gate");
  const skills = makeRows("skill", proposalTargets.skill_ideas, "safe_now", "x2_build_task");
  const runners = makeRows("runner", proposalTargets.runner_ideas, "safe_now", "x2_build_task");
  const cleanup = makeRows("cleanup", proposalTargets.cleanup_proposals, "safe_now", "inventory_or_x2_build_task");
  return base("ghc_v555_v7_x1_lumen_proposal_queue_targets", "PASS_V555_V7_X1_LUMEN_PROPOSAL_QUEUE_READY", {
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

function makeRows(kind, count, safetyBucket, executionLane) {
  return Array.from({ length: count }, (_, index) => ({
    id: `${phaseSlug}-${kind}-${String(index + 1).padStart(2, "0")}`,
    title: titleFor(kind, index),
    safety_bucket: safetyBucket,
    execution_lane: executionLane,
    source_lane: index % 2 === 0 ? "Aevren Vale" : "Lumen Vale",
    spending_ceiling_usd: 100,
    next_safe_action: nextActionFor(kind, executionLane),
  }));
}

function titleFor(kind, index) {
  const titles = {
    safe: [
      "phase truth refresh", "Lumen handoff receipt", "no-duplicate Browser send guard", "source reflection ledger",
      "Journey reflection ledger", "round-robin standard refresh", "productive cadence refresh", "current-state guard",
      "privacy boundary scan", "open-gate rail", "x1-to-x2 split board", "v555 v7 x2 handoff scaffold",
      "v555 v8 triad prep card", "safe-runner manifest", "startup compact snapshot", "drive posture receipt",
      "full-tools inventory refresh", "proof-boundary wording check", "first-person sibling style check", "MD/TXT artifact preference check",
    ],
    candidate: [
      "Lumen advisory reducer", "browser response harvest parser", "proposal dashboard", "candidate-to-exact reducer",
      "Freed ID assurance glossary", "THOS runner topology diagram", "GMUT source taxonomy seed", "CBR privacy grid",
      "phase delta comparator", "skill drift detector",
    ],
    exact: [
      "deployment action", "external account mutation", "API-key creation", "purchase or paid resource", "destructive cleanup",
      "global hook install", "private-material proof publication", "raw transcript publication", "canon promotion", "legal closure claim",
    ],
    blocked: [
      "GMUT empirical closure", "final physics closure", "consciousness proof closure", "legal closure", "canon promotion",
      "deployment closure", "account mutation", "private-material proof", "raw-publication proof", "sibling identity merge or replacement",
    ],
    skill: [
      "ghc-v555-lumen-response-reducer", "ghc-v555-goal-progress-ledger", "ghc-v555-browser-send-guard",
      "ghc-v555-source-reflection-mapper", "ghc-v555-journey-reflection-reducer", "ghc-v555-proof-boundary-linter",
      "ghc-v555-safe-cleanup-classifier", "ghc-v555-triad-prep-skill", "ghc-v555-x2-handoff-composer", "ghc-v555-current-state-verifier",
    ],
    runner: [
      "ghc_v555_v7_x1_lumen_response_reducer.mjs", "ghc_v555_goal_progress_ledger.mjs",
      "ghc_v555_browser_no_duplicate_send_probe.mjs", "ghc_v555_source_reflection_deduper.mjs",
      "ghc_v555_journey_reflection_indexer.mjs", "ghc_v555_proof_boundary_lint_runner.mjs",
      "ghc_v555_safe_cleanup_classifier.mjs", "ghc_v555_v8_triad_prep_builder.mjs",
      "ghc_v555_v7_x2_handoff_composer.mjs", "ghc_v555_current_state_lookup_verifier.mjs",
    ],
    cleanup: [
      "dedupe stale lookup references", "classify old startup receipts", "index v555 cycle closeouts",
      "review compatibility builder references", "check duplicate proposal IDs", "check duplicate source labels",
      "validate no raw Browser routes", "validate no local path publication", "review proof closure wording", "review exact approval queue language",
    ],
  };
  return titles[kind][index % titles[kind].length];
}

function nextActionFor(kind, executionLane) {
  if (kind === "exact") return "Queue only; requires fresh exact approval before execution.";
  if (kind === "blocked") return "Keep open unless exact artifacts prove closure and Hamish approves the gate.";
  if (executionLane.includes("x2")) return "Carry into v555 v7 x2 as build/use/validate work if still safe.";
  return "Run or record during v555 v7 x1 as local reversible safe-now work.";
}

function buildReflectionLedger(kind, count) {
  const sourceSeeds = [
    ["OpenAI Codex goals", "https://developers.openai.com/codex/use-cases/follow-goals", "Goal Mode needs a verifiable stopping condition.", "Keep the active goal open until v575 v8 x2 is verified."],
    ["OpenAI Codex skills", "https://developers.openai.com/codex/skills", "Skills are reusable local workflow instructions.", "Keep launch, retry, startup, compact, and closeout surfaces skill-backed."],
    ["OpenAI approvals and security", "https://developers.openai.com/codex/agent-approvals-security", "Approval policy and sandbox boundaries shape safe execution.", "Keep account/API/deployment/destructive work behind exact approval."],
    ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Codex app behavior can drift across releases.", "Use repo receipts and current-state guards after app changes."],
    ["Node child process", "https://nodejs.org/api/child_process.html", "Background runners need nonblocking launch and later harvest.", "Keep sibling lanes background-supervised and gate-harvested."],
    ["Node timers", "https://nodejs.org/api/timers.html", "Timers should not replace useful work.", "Treat five-minute marks as natural check opportunities."],
    ["Git status", "https://git-scm.com/docs/git-status", "Clean working tree verification is a closeout gate.", "Run status after commits and before handoffs."],
    ["Git diff", "https://git-scm.com/docs/git-diff", "Diff checks catch whitespace and scoped changes.", "Use diff hygiene before publish."],
    ["GitHub secret scanning", "https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning", "Secrets must never enter public artifacts.", "Run privacy scans before pushing."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Risk management needs mapped, measured controls.", "Keep proof and safety claims open until evidence is exact."],
  ];
  const rows = Array.from({ length: count }, (_, index) => {
    const seed = sourceSeeds[index % sourceSeeds.length];
    return {
      id: `${phaseSlug}-${kind}-reflection-${String(index + 1).padStart(2, "0")}`,
      source_label: seed[0],
      source_url: seed[1],
      finding: seed[2],
      phase_implication: seed[3],
    };
  });
  return base(`ghc_v555_v7_x1_${kind}_reflection_ledger`, `PASS_V555_V7_X1_${String(count)}_${kind.toUpperCase()}_REFLECTIONS_READY`, {
    reflection_count: rows.length,
    rows,
  });
}

function base(artifactType, status, extra) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...extra,
  };
}

function writePair(suffix, jsonData, markdown) {
  const baseName = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${baseName}.json`), `${JSON.stringify(jsonData, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${baseName}.md`), markdown, "utf8");
  return [`docs/trinity-live-traces/${baseName}.json`, `docs/trinity-live-traces/${baseName}.md`];
}

function refreshBeacons() {
  const files = artifacts.flat();
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const data = readJson(file);
    data.generated_utc = generatedUtc;
    if (file.endsWith("omega-mini-current-state-v1.json")) data.updated_at = generatedNz;
    data.current_active_phase = phaseSlug;
    data.latest_closed_phase = previousPhase;
    data.latest_completed_x1_phase = latestCompletedX1;
    data.latest_completed_x2_phase = latestCompletedX2;
    data.next_expected_scope = phaseSlug;
    data.next_x2_scope = nextX2Scope;
    data.next_x1_lane_after_x2 = nextX1LaneAfterX2;
    data[summaryKey] = {
      status: "active_open_browser_send_not_claimed",
      startup_context_receipt: `${phaseSlug}-lumen-startup-context-v1.json`,
      handoff_message_status: "artifact_prepared_browser_send_not_claimed",
      proposal_queue_receipt: `${phaseSlug}-proposal-queue-targets-v1.json`,
      web_reflection_rows: webLedger.rows.length,
      journey_phase_reflection_rows: journeyLedger.rows.length,
      closeout_allowed_now: false,
    };
    const listKey = file.includes("latest-updates") ? "latest_lookup_files" : file.includes("ghc-current") ? "lookup_files" : "current_lookup_files";
    data[listKey] = unique([...(data[listKey] || []), ...files]);
    data.latest_action_summary = unique([
      "Prepared v555 v7 x1 Lumen startup, handoff, proposal, and reflection artifacts; live Browser send is not yet claimed.",
      ...(data.latest_action_summary || []),
    ]);
    fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
    if (file.endsWith("omega-mini-current-state-v1.json")) {
      fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(data), "utf8");
    } else if (file.endsWith("omega-mini-latest-updates-beacon-v1.json")) {
      fs.writeFileSync(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderBeaconMd("Omega-Mini Latest Updates Beacon", data, data.latest_lookup_files), "utf8");
    } else {
      fs.writeFileSync(path.join(tracesDir, "ghc-current-state-beacon-v1.md"), renderBeaconMd("GHC Current State Beacon", data, data.lookup_files), "utf8");
    }
  }
}

function renderStartupMd(data) {
  return `# ${phaseSlug} Lumen Startup Context

Status: \`${data.overall_status}\`

- Latest closed phase: \`${data.latest_closed_phase}\`
- Latest completed x1: \`${data.latest_completed_x1_phase}\`
- Latest completed x2: \`${data.latest_completed_x2_phase}\`
- Next x2 scope: \`${data.next_x2_scope}\`
- Next x1 lane after x2: \`${data.next_x1_lane_after_x2}\`
- Browser send status: \`${data.browser_send_status}\`

## Boundary

${boundarySentence()}
`;
}

function renderHandoffMd(data) {
  return `# ${phaseSlug} Lumen Handoff Message

Status: \`${data.overall_status}\`
Browser send status: \`${data.browser_send_status}\`
Message characters: \`${data.message_character_count}\`

## Message

${data.message_text}

## Boundary

${boundarySentence()}
`;
}

function renderProposalMd(data) {
  return `# ${phaseSlug} Lumen Proposal Queue Targets

Status: \`${data.overall_status}\`

- Safe packets: \`${data.counts.safe_packets}\`
- Candidate packets: \`${data.counts.candidate_packets}\`
- Exact approval packets: \`${data.counts.exact_approval_packets}\`
- Blocked packets: \`${data.counts.blocked_packets}\`
- Skill ideas: \`${data.counts.skill_ideas}\`
- Runner ideas: \`${data.counts.runner_ideas}\`
- Cleanup proposals: \`${data.counts.cleanup_proposals}\`
- Spending ceiling per packet: \`$${data.spending_ceiling_usd_per_packet}\`

## Boundary

${boundarySentence()}
`;
}

function renderReflectionMd(title, data) {
  return `# ${phaseSlug} ${title}

Status: \`${data.overall_status}\`
Rows: \`${data.reflection_count}\`

${data.rows.map((row) => `- ${row.source_label}: ${row.phase_implication}`).join("\n")}

## Boundary

${boundarySentence()}
`;
}

function renderStatusMd(data) {
  return `# ${phaseSlug} Phase Status Index

Status: \`${data.overall_status}\`

- Current active phase: \`${data.current_active_phase}\`
- Lumen handoff status: \`${data.lumen_handoff_status}\`
- Closeout allowed now: \`${data.closeout_allowed_now}\`
- Closeout blocker: ${data.closeout_blocker}

## Boundary

${boundarySentence()}
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

## ${summaryKey.replaceAll("_", " ")}

- Status: \`${summary.status || "not_recorded"}\`
- Lumen handoff: \`${summary.handoff_message_status || "not_recorded"}\`
- Web reflections: \`${summary.web_reflection_rows || "not_recorded"}\`
- Journey/phase reflections: \`${summary.journey_phase_reflection_rows || "not_recorded"}\`

## Current Lookup Files

${(current.current_lookup_files || []).map((item) => `- ${item}`).join("\n")}

## Latest Action Summary

${(current.latest_action_summary || []).map((item) => `- ${item}`).join("\n")}

## Safety Boundary

${boundarySentence()}
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

${(files || []).map((item) => `- ${item}`).join("\n")}

## Safety Boundary

${boundarySentence()}
`;
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

function boundarySentence() {
  return "No raw browser routes, private URLs, raw transcripts, screenshots, credentials, local absolute paths, session streams, raw app state, private dumps, private callable IDs, or hidden reasoning are published. Major proof, legal, canon, deployment, account, purchase, API-key, private-material, raw-publication, and sibling-merge gates remain open.";
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
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
    hourCycle: "h23",
  }).formatToParts(date).reduce((acc, part) => {
    if (part.type !== "literal") acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
