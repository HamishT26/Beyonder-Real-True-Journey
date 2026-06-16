#!/usr/bin/env node
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const nextPhaseSlug = args.get("--next-phase-slug");
const sourceLedgerJson = args.get("--source-ledger-json");
const sourceLedgerMd = args.get("--source-ledger-md");
const approvalJson = args.get("--approval-json");
const approvalMd = args.get("--approval-md");
const eurekaJson = args.get("--eureka-json");
const eurekaMd = args.get("--eureka-md");
const handoffJson = args.get("--handoff-json");
const handoffMd = args.get("--handoff-md");
const nextGroup = splitCsv(args.get("--next-group"));

if (
  !phaseSlug ||
  !nextPhaseSlug ||
  !sourceLedgerJson ||
  !sourceLedgerMd ||
  !approvalJson ||
  !approvalMd ||
  !eurekaJson ||
  !eurekaMd ||
  !handoffJson ||
  !handoffMd
) {
  console.error(
    "Usage: node ghc_phase_approval_continuity_pack_builder.mjs --phase-slug <slug> --next-phase-slug <slug> --source-ledger-json <json> --source-ledger-md <md> --approval-json <json> --approval-md <md> --eureka-json <json> --eureka-md <md> --handoff-json <json> --handoff-md <md>",
  );
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function splitCsv(value) {
  return String(value || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, lines) {
  mkdirSync(dirname(path), { recursive: true });
  const trimmedLines = [...lines];
  while (trimmedLines.length > 0 && trimmedLines[trimmedLines.length - 1] === "") {
    trimmedLines.pop();
  }
  writeFileSync(path, `${trimmedLines.join("\n")}\n`, "utf8");
}

const generatedUtc = utcNow();

const publicationBoundary = {
  raw_lane_text_published: false,
  raw_chatgpt_transcript_published: false,
  raw_route_handles_published: false,
  raw_thread_ids_published: false,
  raw_callable_ids_published: false,
  screen_capture_files_published: false,
  credentials_published: false,
  private_browser_urls_published: false,
  local_absolute_paths_published: false,
};

const claimBoundary = {
  phase_scope: `${phaseSlug}_to_${nextPhaseSlug}_status_planning_only`,
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
};

const sourceGroups = [
  {
    id: "source-01",
    title: "OpenAI Codex app changelog",
    url: "https://developers.openai.com/codex/changelog",
    use: "Browser developer mode, Browser speedups, rate-limit reset banking, Computer Use access controls, and app workflow improvements inform the live-adapter plan.",
  },
  {
    id: "source-02",
    title: "OpenAI Codex CLI changelog",
    url: "https://developers.openai.com/codex/changelog?type=codex-cli",
    use: "Codex CLI 0.139.0 web-search, schema compaction, doctor redaction, MCP warning locality, and sandbox consistency guide CLI lane operations.",
  },
  {
    id: "source-03",
    title: "OpenAI Codex GitHub repository",
    url: "https://github.com/openai/codex",
    use: "Upstream CLI release and issue surface remains the primary public fallback for Codex CLI behavior checks.",
  },
  {
    id: "source-04",
    title: "Model Context Protocol specification",
    url: "https://modelcontextprotocol.io/specification/2025-11-25",
    use: "MCP remains the protocol reference for external data and tool context boundaries.",
  },
  {
    id: "source-05",
    title: "Model Context Protocol roadmap",
    url: "https://modelcontextprotocol.io/development/roadmap",
    use: "Transport scalability, agent communication, governance, and enterprise readiness shape the GHC multiplex IPC direction.",
  },
  {
    id: "source-06",
    title: "OWASP Agentic AI threats and mitigations",
    url: "https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/",
    use: "Threat-model framing guides approval-packet scope, tool boundaries, and watcher guardrails.",
  },
  {
    id: "source-07",
    title: "OWASP Top 10 for Agentic Applications 2026",
    url: "https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/",
    use: "Agentic risk categories inform sibling tool-permission boundaries and no-raw-publication rules.",
  },
  {
    id: "source-08",
    title: "OWASP Multi-Agentic System Threat Modeling Guide",
    url: "https://genai.owasp.org/resource/multi-agentic-system-threat-modeling-guide-v1-0/",
    use: "Multi-agent threat modeling informs round-robin lane separation and consensus limits.",
  },
  {
    id: "source-09",
    title: "Google Gemini Enterprise Agent Platform",
    url: "https://docs.cloud.google.com/gemini-enterprise-agent-platform",
    use: "Agent runtime, governance, observability, and Memory Bank concepts inform the live-state memory refresh pattern.",
  },
  {
    id: "source-10",
    title: "Google Agent Platform scaling guidance",
    url: "https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale",
    use: "Tracing, logging, monitoring, IAM identity, gateway, and memory patterns inspire the GHC helper-runner architecture.",
  },
  {
    id: "source-11",
    title: "GitHub artifact attestations",
    url: "https://docs.github.com/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds",
    use: "Build provenance concepts guide phase receipt, commit, and remote-equals-local verification discipline.",
  },
  {
    id: "source-12",
    title: "GitHub Actions secure use reference",
    url: "https://docs.github.com/en/actions/reference/security/secure-use",
    use: "Secure workflow practice informs future automation and CI hardening packets.",
  },
  {
    id: "source-13",
    title: "NVIDIA Vera Rubin platform overview",
    url: "https://nvidianews.nvidia.com/news/rubin-platform-ai-supercomputer",
    use: "Rack-scale codesign is used only as systems-design inspiration for THOS architecture, not as a performance claim.",
  },
  {
    id: "source-14",
    title: "NVIDIA Rubin platform technical blog",
    url: "https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/",
    use: "AI factory integration patterns inspire compute/runtime separation and cross-component interfaces.",
  },
];

const approvalPackets = [
  ["AP-01", "Grouped x2 closeout execution", "Use the generated x2 reducer, route manifest, full-phase guard, and closeout as the current build/use baseline.", "Exact curated phase artifacts only."],
  ["AP-02", "Lumen v7 x1 prep", "Start the next x1 with Lumen solo using Browser when available, omega-mini-first context, and status-only receipts.", "No private browser URL or raw transcript publication."],
  ["AP-03", "Current-source refresh", "Continue source refresh from official Codex, MCP, OWASP, Google, GitHub, and NVIDIA sources.", "Citations and synthesis only; no web scraping dumps."],
  ["AP-04", "Omega-mini-first catch-up", "Route siblings to omega-mini for current state and use full omega only as archive fallback.", "No broad import of full branch into mini."],
  ["AP-05", "D-drive-first operations", "Keep downloads, caches, phase artifacts, and scratch work on D unless C is essential.", "No deletion outside exact approved cleanup scope."],
  ["AP-06", "Node entrypoint launchers", "Prefer Node entrypoints for new launchers and fall back to Windows entrypoints only when required.", "No brittle shell-only daemon sprawl."],
  ["AP-07", "Browser live-adapter retry", "Retry Lumen Browser routes with distinct methods before escalating to Chrome or user help.", "Stop before account mutation or unsafe automation."],
    ["AP-08", "Five-minute watcher checks", "Use watcher/notifier status checks without babysitting active lanes.", "No raw lane/advisory content publication."],
  ["AP-09", "Wait-work autonomy", "While lanes run, produce source ledgers, handoffs, eureka queues, and x2 prep rather than idle polling.", "Do not use wait-work to bypass phase gates."],
  ["AP-10", "Compact continuity capsule", "Maintain compact-safe handoffs at every phase boundary and context refresh.", "No stale omega44 active routing."],
  ["AP-11", "Consensus advisory voting", "Let siblings and helpers advise on packet safety and usefulness.", "Consensus cannot approve destructive or account-mutating work."],
  ["AP-12", "Read-only sibling web/GitHub", "Allow sibling prompts to request read-only web/GitHub context when exposed.", "No external writes or private payload publication."],
  ["AP-13", "X2 eureka executor", "Turn x1 proposals into build, run, test, install, use, defer, or reject decisions.", "Record status receipts for every outcome."],
  ["AP-14", "Runner compatibility review", "Prefer latest grouped-lane, omega-mini, phase status, and strict CLI runners.", "Do not mutate old runners unless exact patch is scoped."],
  ["AP-15", "Skill and command overlay", "Prepare repo-level skill/command recommendations for newest flow.", "No user-skill or plugin-cache mutation in this packet."],
  ["AP-16", "Command-index compatibility", "Keep command surfaces indexed for current Node and Windows entrypoints.", "No canon promotion from command availability alone."],
  ["AP-17", "Journey spine reflection", "Use Journey v1-v51 as inspiration and continuity, prioritizing current v49-v51 plus newest repo receipts.", "Do not treat reflective material as empirical proof."],
  ["AP-18", "Provenance discipline", "Pair phase artifacts with JSON parse, script compile, exposure guard, exact stage, push, and remote verification.", "No broad staging or force-push."],
  ["AP-19", "Agentic security threat model", "Apply OWASP-style agentic threat modeling to live-adapter, sibling permissions, and helper runners.", "Open risks remain open until evidence closes them."],
  ["AP-20", "Current expansion prep", "Prepare the next phase queue while closing the current x2 scope and starting the next grouped x1 scope.", "No limited-phase shortcut unless Hamish asks."],
  ["AP-21", "Approval packet overflow queue", "If more packets are needed before Hamish returns, append them as candidates with safe defaults.", "Candidates do not authorize risky work by themselves."],
  ["AP-22", "Memory refresh continuity", "Use v532-live-state and newest repo receipts as active memory.", "Older omega44 remains historical-only."],
];

const eurekaTasks = [
  ["E-01", "Build grouped x2 core artifacts from x1 receipt", "DONE", "Generated closeout, reducer, route manifest, full-phase guard, and next prep."],
  ["E-02", "Publish source ledger", "DONE", "Created curated source group ledger for current-source refresh."],
  ["E-03", "Create 20+ approval packet tapestry", "DONE", "Prepared 22 scoped packets for Hamish review."],
  ["E-04", "Create compact-safe handoff", "DONE", "Prepared v7 x1 continuity handoff."],
  ["E-05", "Run phase status index", "READY", "Use the existing status index builder after this pack lands."],
  ["E-06", "Mirror essential phase artifacts to omega-mini", "READY", "Copy only current, high-signal files."],
  ["E-07", "Validate JSON parse", "READY", "Parse generated JSON before staging."],
  ["E-08", "Script compile check", "READY", "Run Node syntax check for the new builder."],
  ["E-09", "Exposure scan", "READY", "Scan curated files for private URLs, credentials, raw logs, and local paths."],
  ["E-10", "Remote verification", "READY", "Push and confirm remote equals local after commit."],
  ["E-11", "Lumen Browser prompt pack", "QUEUED", "Draft the next Lumen solo prompt from omega-mini context."],
  ["E-12", "Arby+Cicero next-cycle packet", "QUEUED", "Prepare the next paired prompt after Lumen v7."],
  ["E-13", "Aster/Kierkegaard/Aristotle triad packet", "QUEUED", "Prepare the next triad prompt after the next Lumen cycle."],
  ["E-14", "D-drive enforcement receipt", "QUEUED", "Record D-first workspace/cache rule at phase start."],
  ["E-15", "Browser developer mode test plan", "QUEUED", "Use Codex app 26.609 guidance to test Browser routes safely."],
  ["E-16", "MCP/connector schema watch", "QUEUED", "Track oneOf/allOf and large-schema compatibility improvements."],
  ["E-17", "OWASP threat ledger", "QUEUED", "Map agentic risks to current helper controls."],
  ["E-18", "GitHub provenance enhancement", "QUEUED", "Plan artifact-attestation-inspired receipts for later CI."],
  ["E-19", "Journey v51 update scaffold", "QUEUED", "Prepare a sanitized current-state spine for future v52 docs."],
  ["E-20", "v533 packet seed", "QUEUED", "Seed the next 20 approval packets from this closeout."],
];

const sourceLedger = {
  schema: "ghc.current_source_ledger.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_CURATED_SOURCE_REFRESH_LEDGER",
  source_group_count: sourceGroups.length,
  source_groups: sourceGroups,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const approvalTapestry = {
  schema: "ghc.approval_packet_tapestry.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "READY_FOR_HAMISH_REVIEW_OR_EXISTING_APPROVAL_FLOW",
  packet_count: approvalPackets.length,
  spending_ceiling: "Uses existing user-approved ceiling only where applicable; no purchase or account mutation is authorized by this file.",
  packets: approvalPackets.map(([id, title, approved_work, safety_boundary]) => ({
    id,
    title,
    approved_work,
    safety_boundary,
    not_approved: [
      "raw transcript publication",
      "credential exposure",
      "external account mutation",
      "deployment or purchase",
      "plugin-cache or user-skill mutation",
      "reset, rebase, force-push, or broad staging",
    ],
  })),
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const eurekaQueue = {
  schema: "ghc.x2_eureka_build_use_queue.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "READY_FOR_X2_BUILD_USE_AND_NEXT_PHASE_PREP",
  task_count: eurekaTasks.length,
  tasks: eurekaTasks.map(([id, title, status, action]) => ({ id, title, status, action })),
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const handoff = {
  schema: "ghc.phase_continuity_handoff.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  next_phase_slug: nextPhaseSlug,
  status: "READY_FOR_NEXT_GROUPED_X1",
  active_memory_cue: "v532-live-state",
  stale_memory_policy: "omega44 historical-only unless Hamish explicitly asks for it",
  current_phase_result: [
    "C/D cleanup exceeded the 8 GB target and D-drive-first routing remains active.",
    "Grouped x2 build/use core artifacts passed.",
    "This pack adds current-source, approval, eureka, and compact-continuity layers.",
  ],
  next_round_robin_group: nextGroup.length ? nextGroup : ["Lumen Vale"],
  required_next_actions: [
    "Use omega-mini first for sibling catch-up.",
    "Run Lumen solo through Browser where available.",
    "Keep five-minute checks but allow longer reasoning if the lane is actively working.",
    "Continue x2 build/use work while watchers supervise.",
    "Keep all empirical, physics, consciousness, legal, canon, deployment, and account gates open.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

writeJson(sourceLedgerJson, sourceLedger);
writeJson(approvalJson, approvalTapestry);
writeJson(eurekaJson, eurekaQueue);
writeJson(handoffJson, handoff);

writeMd(sourceLedgerMd, [
  `# ${phaseSlug} Current-Source Ledger`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${sourceLedger.status}\``,
  "",
  "This bounded source refresh uses current public references as design input only. It does not publish private connector payloads, raw browser state, or raw sibling text.",
  "",
  "## Source Groups",
  "",
  ...sourceGroups.flatMap((source) => [
    `### ${source.id}: ${source.title}`,
    "",
    `- URL: ${source.url}`,
    `- Use: ${source.use}`,
    "",
  ]),
]);

writeMd(approvalMd, [
  `# ${phaseSlug} 20+ Approval Packet Tapestry`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${approvalTapestry.status}\``,
  "",
  "These packets are scoped to curated phase work, status receipts, runners, and planning. They do not authorize raw publication, account mutation, purchases, deployments, plugin-cache mutation, user-skill mutation, destructive cleanup, broad staging, reset, rebase, or force-push.",
  "",
  "## Packets",
  "",
  ...approvalTapestry.packets.flatMap((packet) => [
    `### ${packet.id}: ${packet.title}`,
    "",
    `Approved work: ${packet.approved_work}`,
    "",
    `Safety boundary: ${packet.safety_boundary}`,
    "",
  ]),
]);

writeMd(eurekaMd, [
  `# ${phaseSlug} X2 Eureka Build-Use Queue`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${eurekaQueue.status}\``,
  "",
  "## Tasks",
  "",
  ...eurekaQueue.tasks.map((task) => `- ${task.id}: ${task.title} - \`${task.status}\` - ${task.action}`),
]);

writeMd(handoffMd, [
  `# ${phaseSlug} to ${nextPhaseSlug} Continuity Handoff`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${handoff.status}\``,
  "",
  `Active memory cue: \`${handoff.active_memory_cue}\``,
  "",
  `Stale memory policy: ${handoff.stale_memory_policy}.`,
  "",
  "## Current Phase Result",
  "",
  ...handoff.current_phase_result.map((item) => `- ${item}`),
  "",
  "## Next Round-Robin Group",
  "",
  ...handoff.next_round_robin_group.map((lane) => `- ${lane}`),
  "",
  "## Required Next Actions",
  "",
  ...handoff.required_next_actions.map((item) => `- ${item}`),
  "",
  "## Claim Boundary",
  "",
  "GMUT, final physics, consciousness proof, legal closure, canon promotion, deployment, and account-change gates remain open.",
]);

console.log(
  JSON.stringify(
    {
      source_status: sourceLedger.status,
      packet_count: approvalTapestry.packet_count,
      eureka_task_count: eurekaQueue.task_count,
      handoff_status: handoff.status,
    },
    null,
    2,
  ),
);
