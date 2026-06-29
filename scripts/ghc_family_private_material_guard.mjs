#!/usr/bin/env node
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v1-x1";
const traceDir = join(root, "docs", "trinity-live-traces");
const forbiddenLiteralNeedles = [
  ["C:", "\\", "Users"].join(""),
  ["D:", "\\", "GHC"].join(""),
  ["C:", "/", "Users"].join(""),
  ["D:", "/", "GHC"].join(""),
  ["https://", "chatgpt.com", "/c/"].join(""),
  ["BEGIN ", "PRIVATE KEY"].join("")
];
const forbiddenRegexes = [
  new RegExp(["sk", "-[A-Za-z0-9_-]{20,}"].join("")),
  new RegExp(["AK", "IA[0-9A-Z]{16}"].join("")),
  new RegExp(["019", "e[a-z0-9-]{20,}"].join(""), "i")
];
const files = [];

function walk(dir) {
  for (const name of readdirSync(dir)) {
    const file = join(dir, name);
    const stat = statSync(file);
    if (stat.isDirectory()) walk(file);
    else if (name.startsWith(`${phaseSlug}-`)) files.push(file);
  }
}

walk(traceDir);
const hits = [];
for (const file of files) {
  const text = readFileSync(file, "utf8");
  if (forbiddenLiteralNeedles.some((needle) => text.includes(needle)) || forbiddenRegexes.some((pattern) => pattern.test(text))) {
    hits.push(relative(root, file));
  }
}

const checks = [
  { label: "phase_public_files_scanned", status: files.length > 0 ? "PASS" : "OPEN_GAP", observed: files.length },
  { label: "forbidden_private_material_absent", status: hits.length === 0 ? "PASS" : "OPEN_GAP", observed: hits.length }
];

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_private_material_guard.mjs",
  purpose: "Scan current-phase public artifacts for private routes, IDs, credentials, local paths, and raw private material.",
  status: hits.length === 0 && files.length > 0 ? "PASS_GHC_FAMILY_PRIVATE_MATERIAL_GUARD" : "OPEN_GAP_GHC_FAMILY_PRIVATE_MATERIAL_GUARD",
  checks,
  outputs: { scannedFiles: files.length, hitCount: hits.length, hits }
});
