import crypto from "node:crypto";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const EXPECTED_BRANCH = "codex/GHC-Family/tamar-vey-main-3";
const ORIGINAL_FINAL = "8b08ff1c18bed9cc22d3cfa63c041c3e3b9f6cb2";
const PLANNING = "14c71394c274c6d7965d053d9be49a6149cb1ff1";
const X1 = "83408624ca62960d0ead3a6868afba0d0c274e73";
const X2 = "39d148f57be28afc49a94844b29e38608976d64f";
const OWNER_PREFIX = "docs/tamar-vey/v708-v3-r2/";

function git(args, encoding = "utf8") {
  return execFileSync("git", args, {
    encoding,
    maxBuffer: 64 * 1024 * 1024,
  });
}

function textAt(file) {
  return git(["show", `HEAD:${file}`]);
}

function bytesAt(file) {
  return git(["show", `HEAD:${file}`], null);
}

function parseAt(file) {
  return JSON.parse(textAt(file));
}

function lines(text) {
  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
}

function sha(bytes) {
  return crypto.createHash("sha256").update(bytes).digest("hex");
}

function verifyManifest(file) {
  const manifest = parseAt(file);
  const mismatches = [];
  for (const expected of manifest.entries) {
    const bytes = bytesAt(expected.path);
    if (bytes.length !== expected.bytes || sha(bytes) !== expected.sha256) {
      mismatches.push(expected.path);
    }
  }
  return { entries: manifest.entry_count, mismatches };
}

function requireCheck(checks, id, condition, detail) {
  checks.push({ id, ok: Boolean(condition), detail });
  if (!condition) throw new Error(`${id}: ${detail}`);
}

const receiptIndex = process.argv.indexOf("--receipt");
if (receiptIndex < 0 || !process.argv[receiptIndex + 1]) {
  throw new Error("--receipt path is required");
}
const receiptPath = path.resolve(process.argv[receiptIndex + 1]);
if (fs.existsSync(receiptPath))
  throw new Error("exclusive receipt already exists");

const checks = [];
const branch = git(["branch", "--show-current"]).trim();
const head = git(["rev-parse", "HEAD"]).trim();
const parent = git(["rev-parse", "HEAD^"]).trim();
const parentCount = lines(git(["rev-list", "--parents", "-n", "1", "HEAD"]))[0]
  .split(/\s+/)
  .slice(1).length;
const phaseCommits = Number(
  git(["rev-list", "--count", `${ORIGINAL_FINAL}..HEAD`]).trim(),
);
const merges = Number(
  git(["rev-list", "--merges", "--count", `${ORIGINAL_FINAL}..HEAD`]).trim(),
);
const ancestry = [
  [PLANNING, ORIGINAL_FINAL],
  [X1, PLANNING],
  [X2, X1],
  [head, X2],
].every(
  ([child, expectedParent]) =>
    git(["rev-parse", `${child}^`]).trim() === expectedParent,
);

requireCheck(checks, "branch", branch === EXPECTED_BRANCH, branch);
requireCheck(checks, "final_parent", parent === X2, parent);
requireCheck(checks, "one_final_parent", parentCount === 1, parentCount);
requireCheck(checks, "direct_ancestry", ancestry, "planning/x1/x2/final chain");
requireCheck(checks, "phase_commit_count", phaseCommits === 4, phaseCommits);
requireCheck(checks, "zero_merges", merges === 0, merges);

const ownerManifest = verifyManifest(
  `${OWNER_PREFIX}final/validation/final-owner-manifest.json`,
);
const deltaManifest = verifyManifest(
  `${OWNER_PREFIX}final/validation/final-delta-manifest.json`,
);
requireCheck(
  checks,
  "owner_manifest",
  ownerManifest.mismatches.length === 0,
  ownerManifest,
);
requireCheck(
  checks,
  "delta_manifest",
  deltaManifest.mismatches.length === 0,
  deltaManifest,
);

const seal = parseAt(`${OWNER_PREFIX}final/closeout/content-seal.json`);
const sealMismatches = seal.targets.filter((expected) => {
  const bytes = bytesAt(expected.path);
  return bytes.length !== expected.bytes || sha(bytes) !== expected.sha256;
});
requireCheck(checks, "content_seal", sealMismatches.length === 0, {
  targets: seal.target_count,
  mismatches: sealMismatches.map((entry) => entry.path),
});

const ownerFiles = lines(
  git(["ls-tree", "-r", "--name-only", "HEAD", OWNER_PREFIX]),
);
const jsonFiles = ownerFiles.filter((file) => file.endsWith(".json"));
for (const file of jsonFiles) parseAt(file);
requireCheck(checks, "owner_json_parse", true, jsonFiles.length);
requireCheck(
  checks,
  "owner_file_ceiling",
  ownerFiles.length < 2000,
  ownerFiles.length,
);
requireCheck(
  checks,
  "no_pdf",
  ownerFiles.every((file) => !file.toLowerCase().endsWith(".pdf")),
  "PDF count zero",
);

const baton = textAt(`${OWNER_PREFIX}final/hand-off-baton.md`);
const batonWords = baton.trim().split(/\s+/).length;
requireCheck(checks, "baton_minimum", batonWords >= 2000, batonWords);
requireCheck(checks, "baton_ceiling", batonWords <= 100000, batonWords);
requireCheck(
  checks,
  "baton_eof",
  baton.includes(
    "END OF TAMAR VEY V708-V3-R2 BATON. Preparation is not delivery.",
  ),
  "explicit EOF",
);

const phaseTruth = parseAt(`${OWNER_PREFIX}final/phase-truth.json`);
const x1Tests = parseAt(`${OWNER_PREFIX}x1/validation/tests.json`);
const x2Tests = parseAt(`${OWNER_PREFIX}x2/validation/tests.json`);
requireCheck(
  checks,
  "x1_tests",
  x1Tests.passed === 24 && x1Tests.failed === 0,
  x1Tests,
);
requireCheck(
  checks,
  "x2_tests",
  x2Tests.total_passed === 41 && x2Tests.total_failed === 0,
  x2Tests,
);
requireCheck(
  checks,
  "phase_test_total",
  phaseTruth.evidence.total_tests_passed === 65 &&
    phaseTruth.evidence.test_replays === 0,
  phaseTruth.evidence,
);
requireCheck(
  checks,
  "route_not_sent",
  phaseTruth.route.state === "PREPARED_NOT_SENT_USER_WILL_DELIVER" &&
    phaseTruth.route.delivery_acknowledged === false,
  phaseTruth.route,
);
requireCheck(
  checks,
  "terminal_verdict",
  phaseTruth.terminal_verdict === "NOT_READY_FOR_STAGE_20",
  phaseTruth.terminal_verdict,
);

const diffCheck = git(["diff", "--check"]);
const clean = git(["status", "--porcelain"]).trim() === "";
const upstream = git(["rev-parse", "@{upstream}"]).trim();
const tracking = git(["rev-parse", `refs/remotes/origin/${branch}`]).trim();
const remoteLine =
  lines(git(["ls-remote", "origin", `refs/heads/${branch}`]))[0] ?? "";
const freshRemote = remoteLine.split(/\s+/)[0] ?? "";
const divergence = git([
  "rev-list",
  "--left-right",
  "--count",
  "HEAD...@{upstream}",
])
  .trim()
  .split(/\s+/)
  .map(Number);
requireCheck(checks, "diff_check", diffCheck === "", "clean diff");
requireCheck(checks, "clean_tree", clean, clean);
requireCheck(
  checks,
  "four_way_equality",
  [upstream, tracking, freshRemote].every((value) => value === head),
  { head, upstream, tracking, freshRemote },
);
requireCheck(
  checks,
  "zero_divergence",
  divergence[0] === 0 && divergence[1] === 0,
  divergence,
);

const receipt = {
  schema: "ghc.tamar.v708-v3-r2.canonical-receipt.v1",
  status: "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
  branch,
  head,
  parent,
  invoked_once: true,
  replayed: false,
  complete_repository_suite_run: false,
  owner_files: ownerFiles.length,
  owner_json_files: jsonFiles.length,
  owner_manifest_entries: ownerManifest.entries,
  final_delta_entries: deltaManifest.entries,
  content_seal_targets: seal.target_count,
  baton_words: batonWords,
  tests: { x1: 24, x2: 41, total: 65 },
  checks,
  terminal_verdict: "NOT_READY_FOR_STAGE_20",
};
fs.mkdirSync(path.dirname(receiptPath), { recursive: true });
fs.writeFileSync(receiptPath, `${JSON.stringify(receipt, null, 2)}\n`, {
  encoding: "utf8",
  flag: "wx",
});
process.stdout.write(`${JSON.stringify(receipt)}\n`);
