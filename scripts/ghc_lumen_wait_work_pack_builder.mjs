#!/usr/bin/env node
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const nextScope = args.get("--next-scope");
const markerCount = Number(args.get("--marker-count") || "0");
const promptChars = Number(args.get("--prompt-chars") || "0");
const checkCount = Number(args.get("--check-count") || "0");
const finalMessageChars = Number(args.get("--final-message-chars") || "0");
const finalMessageWords = Number(args.get("--final-message-words") || "0");
const finalMessageHash = args.get("--final-message-hash") || null;
const sourceJson = args.get("--source-json");
const sourceMd = args.get("--source-md");
const waitJson = args.get("--wait-json");
const waitMd = args.get("--wait-md");
const approvalJson = args.get("--approval-json");
const approvalMd = args.get("--approval-md");
const handoffJson = args.get("--handoff-json");
const handoffMd = args.get("--handoff-md");

if (
  !phaseSlug ||
  !nextScope ||
  !sourceJson ||
  !sourceMd ||
  !waitJson ||
  !waitMd ||
  !approvalJson ||
  !approvalMd ||
  !handoffJson ||
  !handoffMd
) {
  console.error(
    "Usage: node ghc_lumen_wait_work_pack_builder.mjs --phase-slug <slug> --next-scope <slug> --marker-count <n> --prompt-chars <n> --check-count <n> --source-json <json> --source-md <md> --wait-json <json> --wait-md <md> --approval-json <json> --approval-md <md> --handoff-json <json> --handoff-md <md>",
  );
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, lines) {
  const trimmed = [...lines];
  while (trimmed.length > 0 && trimmed[trimmed.length - 1] === "") trimmed.pop();
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${trimmed.join("\n")}\n`, "utf8");
}

const generatedUtc = utcNow();
const markerComplete = markerCount >= 2;
const laneStatus = markerComplete ? "PASS_LUMEN_BROWSER_MARKER_STATUS" : "OPEN_GAP_LUMEN_BROWSER_STILL_WORKING";

const publicationBoundary = {
  raw_prompt_published: false,
  raw_reply_text_published: false,
  raw_chatgpt_transcript_published: false,
  private_browser_url_published: false,
  route_handles_published: false,
  screenshots_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
};

const claimBoundary = {
  lumen_x1_completion: markerComplete ? "marker_complete" : "not_claimed",
  next_x2_start: "not_claimed",
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
};

const sources = [
  {
    id: "src-01",
    title: "OpenAI Codex changelog",
    url: "https://developers.openai.com/codex/changelog",
    use: "Codex app Browser developer mode, Browser performance, rate-limit reset banking, and app workflow improvements inform live-adapter retries.",
  },
  {
    id: "src-02",
    title: "OpenAI Codex CLI changelog",
    url: "https://developers.openai.com/codex/changelog?type=codex-cli",
    use: "Codex CLI 0.139.0 web-search, schema compaction, doctor redaction, MCP warning locality, and sandbox fixes inform CLI and TUI lane resilience.",
  },
  {
    id: "src-03",
    title: "Model Context Protocol specification",
    url: "https://modelcontextprotocol.io/specification/2025-11-25",
    use: "Defines the protocol reference for connecting applications, tools, and context in bounded workflows.",
  },
  {
    id: "src-04",
    title: "MCP 2026 roadmap",
    url: "https://modelcontextprotocol.io/development/roadmap",
    use: "Transport scalability, agent communication, governance, registry, and extension maturity inform the GHC multiplex direction.",
  },
  {
    id: "src-05",
    title: "MCP authorization specification",
    url: "https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization",
    use: "Authorization requirements and boundaries inform future long-running helper design without relying on future-dated release-candidate claims.",
  },
  {
    id: "src-06",
    title: "OWASP Agentic AI Threats and Mitigations",
    url: "https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/",
    use: "Threat-model language supports least privilege, human oversight, route separation, and no-raw-publication guards.",
  },
  {
    id: "src-07",
    title: "OWASP Top 10 for Agentic Applications 2026",
    url: "https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/",
    use: "Agentic risk categories guide approval-packet boundaries for autonomy, tool access, and data exposure.",
  },
  {
    id: "src-08",
    title: "Google Gemini Enterprise Agent Platform",
    url: "https://docs.cloud.google.com/gemini-enterprise-agent-platform",
    use: "Agent runtime, governance, observability, and memory concepts inform the GHC helper and memory-refresh architecture.",
  },
  {
    id: "src-09",
    title: "Google Agent Platform scaling guidance",
    url: "https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale",
    use: "Tracing, logging, monitoring, IAM identity, gateway, sessions, and Memory Bank patterns inform phase-run observability.",
  },
  {
    id: "src-10",
    title: "GitHub artifact attestations",
    url: "https://docs.github.com/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds",
    use: "Provenance concepts map to exact staging, commit, push, and remote-equals-local verification.",
  },
];

const approvalPackets = [
  ["AP-01", "Lumen wait without duplicate-send", "Hold the lane open and avoid duplicate prompt sends while the marker is incomplete."],
  ["AP-02", "Five-minute check cadence", "Check Lumen periodically with marker and generation-state probes only."],
  ["AP-03", "Wait-work source refresh", "Use waiting time for curated current-source research instead of idle polling."],
  ["AP-04", "Omega-mini context routing", "Keep Lumen and all siblings pointed to omega-mini first for current state."],
  ["AP-05", "D-drive-first phase work", "Keep generated artifacts and helper work in the D-drive worktree."],
  ["AP-06", "Browser route hardening", "Retry Browser route blockers with distinct methods before escalating."],
  ["AP-07", "Prompt-hash receipt policy", "Record prompt metadata without publishing raw prompts or private URLs."],
  ["AP-08", "Lumen x2 reducer gate", "Do not start x2 build/use from Lumen until marker completion or explicit blocker receipt."],
  ["AP-09", "Compact-safe continuity", "Write handoffs that survive context compaction and keep stale omega44 inactive."],
  ["AP-10", "No limited phase regression", "Continue full phase cadence unless Hamish explicitly requests a limited phase."],
  ["AP-11", "Read-only web/GitHub sibling context", "Permit read-only context use when exposed, with no external writes."],
  ["AP-12", "Private evidence firewall", "Keep raw transcripts, route handles, screenshots, credentials, and local paths out of publication."],
  ["AP-13", "Approval packet queue growth", "Prepare additional safe packets for Hamish review while the lane runs."],
  ["AP-14", "Journey reflection queue", "Use Journey records as inspiration while keeping empirical claims open."],
  ["AP-15", "THOS runner review", "Review latest runner family for next x2 build candidates."],
  ["AP-16", "GMUT proof-ceiling guard", "Keep physics and consciousness claims aspirational unless exact evidence proves closure."],
  ["AP-17", "Freed ID and CBR safety mapping", "Map heart-pillar tasks to privacy, consent, and dignity boundaries."],
  ["AP-18", "Source citation hygiene", "Use primary or official sources where possible and avoid raw search-volume claims."],
  ["AP-19", "Phase status index refresh", "Index the x1 open-gap status so the next turn has a compact proof trail."],
  ["AP-20", "v7 x2 prep hold", "Prepare x2 candidates but hold execution until Lumen completion or blocker policy allows."],
];

const eurekaTasks = [
  ["E-01", "Open-gap marker receipt", "Record marker count and no-duplicate-send status."],
  ["E-02", "Wait-work source ledger", "Keep official Codex, MCP, OWASP, Google, and GitHub sources attached to the phase."],
  ["E-03", "Browser route retry matrix", "Define distinct retry methods for Lumen if the response stalls."],
  ["E-04", "Omega-mini sibling prompt footer", "Standardize a short omega-mini catch-up footer for all sibling prompts."],
  ["E-05", "D-drive phase artifact audit", "Keep current phase generation out of the old C workspace."],
  ["E-06", "No-raw-publication regression scan", "Check generated files for private URL, local path, session stream, and secret-like tokens."],
  ["E-07", "Lumen completion gate", "Require marker count >= 2 before pass status."],
  ["E-08", "x2 deferred build list", "Build only after Lumen handoff is available or a blocker receipt exists."],
  ["E-09", "OWASP threat ledger seed", "Map agentic risks to current Browser and sibling route controls."],
  ["E-10", "MCP task extension watch", "Prepare long-running helper patterns from MCP Tasks concepts without claiming implementation."],
  ["E-11", "Codex Browser developer-mode plan", "Plan deeper route debugging if Browser route remains inconsistent."],
  ["E-12", "CLI 0.139.0 schema watch", "Track richer tool-schema compatibility as a runner design input."],
  ["E-13", "GitHub provenance pattern", "Prepare future receipt provenance inspired by artifact attestations."],
  ["E-14", "Journey v51-to-v532 bridge", "Draft a compact current-state bridge for later Journey updates."],
  ["E-15", "Round-robin next group preflight", "Prepare Arby+Cicero only after Lumen phase state is resolved."],
  ["E-16", "Consensus limits note", "Keep sibling consensus advisory, not a replacement for risky approvals."],
  ["E-17", "Memory cue guard", "Ensure v532-live-state remains active and omega44 remains historical-only."],
  ["E-18", "Source freshness footnote", "Note that current web results are source input, not completion proof."],
  ["E-19", "Phase status index refresh", "Run index once x1 receipts exist."],
  ["E-20", "Next check action", "Recheck Browser marker without sending another prompt."],
];

const sourceLedger = {
  schema: "ghc.lumen_wait_source_ledger.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_WAIT_WORK_SOURCE_LEDGER",
  source_count: sources.length,
  sources,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const waitReceipt = {
  schema: "ghc.lumen_browser_wait_work.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  next_scope: nextScope,
  status: laneStatus,
  prompt_chars: promptChars,
  marker_count: markerCount,
  check_count: checkCount,
  final_message_metadata: {
    chars: finalMessageChars,
    words: finalMessageWords,
    hash: finalMessageHash,
    raw_reply_text_published: false,
  },
  duplicate_send_avoided: true,
  completion_gate: "marker_count_must_be_at_least_2",
  eureka_task_count: eurekaTasks.length,
  eureka_tasks: eurekaTasks.map(([id, title, action]) => ({ id, title, action })),
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const approvalTapestry = {
  schema: "ghc.lumen_wait_approval_tapestry.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "READY_FOR_HAMISH_REVIEW_OR_EXISTING_APPROVAL_FLOW",
  packet_count: approvalPackets.length,
  packets: approvalPackets.map(([id, title, approved_work]) => ({
    id,
    title,
    approved_work,
    safety_boundary: "Curated status, planning, and local repo artifacts only.",
    not_approved: [
      "duplicate prompt send while current lane is still active",
      "raw transcript publication",
      "credential exposure",
      "external account mutation",
      "deployment, purchase, reset, rebase, force-push, or broad staging",
    ],
  })),
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const handoff = {
  schema: "ghc.lumen_wait_continuity_handoff.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  next_scope: nextScope,
  status: markerComplete ? "READY_FOR_X2_AFTER_LUMEN_MARKER" : "WAITING_FOR_LUMEN_MARKER",
  active_memory_cue: "v532-live-state",
  current_lane: "Lumen Vale",
  next_action: markerComplete ? "run grouped x1 closeout and x2 build/use prep" : "recheck marker without duplicate-sending",
  omega_mini_first: true,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

writeJson(sourceJson, sourceLedger);
writeJson(waitJson, waitReceipt);
writeJson(approvalJson, approvalTapestry);
writeJson(handoffJson, handoff);

writeMd(sourceMd, [
  `# ${phaseSlug} Lumen Wait-Work Source Ledger`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${sourceLedger.status}\``,
  "",
  "## Sources",
  "",
  ...sources.flatMap((source) => [`### ${source.id}: ${source.title}`, "", `- URL: ${source.url}`, `- Use: ${source.use}`, ""]),
]);

writeMd(waitMd, [
  `# ${phaseSlug} Lumen Browser Wait-Work Receipt`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${waitReceipt.status}\``,
  "",
  `- Prompt chars: \`${promptChars}\``,
  `- Marker count: \`${markerCount}\``,
  `- Check count: \`${checkCount}\``,
  `- Final message words: \`${finalMessageWords}\``,
  `- Final message hash: \`${finalMessageHash || "not-recorded"}\``,
  "- Duplicate send avoided: `true`",
  "",
  "## Eureka Tasks",
  "",
  ...waitReceipt.eureka_tasks.map((task) => `- ${task.id}: ${task.title}. ${task.action}`),
]);

writeMd(approvalMd, [
  `# ${phaseSlug} Lumen Wait-Work Approval Packets`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${approvalTapestry.status}\``,
  "",
  "These packets stay within curated local repo status, planning, and safety work. They do not authorize duplicate sends, raw publication, account mutation, deployments, purchases, reset, rebase, force-push, or broad staging.",
  "",
  "## Packets",
  "",
  ...approvalTapestry.packets.flatMap((packet) => [`### ${packet.id}: ${packet.title}`, "", packet.approved_work, ""]),
]);

writeMd(handoffMd, [
  `# ${phaseSlug} Lumen Wait Continuity Handoff`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${handoff.status}\``,
  "",
  `Active memory cue: \`${handoff.active_memory_cue}\``,
  "",
  `Current lane: \`${handoff.current_lane}\``,
  "",
  `Next action: ${handoff.next_action}.`,
  "",
  "Omega-mini remains the first catch-up branch. Do not duplicate-send while the existing Lumen lane is active. Keep all proof and canon gates open.",
]);

console.log(
  JSON.stringify(
    {
      status: waitReceipt.status,
      source_count: sourceLedger.source_count,
      packet_count: approvalTapestry.packet_count,
      eureka_task_count: waitReceipt.eureka_task_count,
      handoff_status: handoff.status,
    },
    null,
    2,
  ),
);
