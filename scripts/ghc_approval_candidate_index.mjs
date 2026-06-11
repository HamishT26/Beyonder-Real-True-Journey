#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const prepQueueJson = args.get("--prep-queue-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !prepQueueJson || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_approval_candidate_index.mjs --phase-slug <slug> --prep-queue-json <json> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

const prepQueue = JSON.parse(readFileSync(prepQueueJson, "utf8"));
const candidates = Array.isArray(prepQueue.approval_candidates) ? prepQueue.approval_candidates : [];
const statusCounts = candidates.reduce((counts, candidate) => {
  const status = candidate.status || "UNKNOWN";
  counts[status] = (counts[status] || 0) + 1;
  return counts;
}, {});

const pending = candidates.filter((candidate) => candidate.status !== "APPROVED_USER_AUTHORIZED");
const approved = candidates.filter((candidate) => candidate.status === "APPROVED_USER_AUTHORIZED");
const indexRows = candidates.map((candidate, index) => ({
  order: index + 1,
  id: candidate.id || `candidate-${index + 1}`,
  title: candidate.title || "Untitled approval candidate",
  status: candidate.status || "UNKNOWN",
  purpose: candidate.purpose || "",
  approved_work_count: Array.isArray(candidate.approved_work) ? candidate.approved_work.length : 0,
  not_approved_count: Array.isArray(candidate.not_approved) ? candidate.not_approved.length : 0,
}));

const receipt = {
  artifact_type: "ghc_approval_candidate_index",
  generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
  phase_slug: phaseSlug,
  input: prepQueueJson,
  status: pending.length === 0 ? "ALL_APPROVAL_CANDIDATES_APPROVED" : "APPROVAL_CANDIDATES_PENDING",
  candidate_count: candidates.length,
  approved_count: approved.length,
  pending_count: pending.length,
  status_counts: statusCounts,
  candidates: indexRows,
  publication_boundary: {
    raw_lane_text_published: false,
    raw_chatgpt_transcript_published: false,
    raw_app_server_result_published: false,
    raw_app_server_error_published: false,
    raw_callable_ids_published: false,
    raw_thread_ids_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} Approval Candidate Index`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  `Candidate count: \`${receipt.candidate_count}\``,
  `Approved count: \`${receipt.approved_count}\``,
  `Pending count: \`${receipt.pending_count}\``,
  "",
  "## Candidates",
  "",
  ...indexRows.flatMap((candidate) => [
    `### ${candidate.order}. ${candidate.id}: ${candidate.title}`,
    "",
    `Status: \`${candidate.status}\``,
    "",
    candidate.purpose,
    "",
    `Approved-work rows: \`${candidate.approved_work_count}\``,
    `Not-approved rows: \`${candidate.not_approved_count}\``,
    "",
  ]),
  "## Boundary",
  "",
  "Index only. Pending candidates are not treated as approval. No raw lane text, transcripts, app-server payloads, private IDs, credentials, screenshots, local paths, phase completion claim, GMUT closure, or canon promotion is published.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify({ status: receipt.status, pending_count: receipt.pending_count }, null, 2));
