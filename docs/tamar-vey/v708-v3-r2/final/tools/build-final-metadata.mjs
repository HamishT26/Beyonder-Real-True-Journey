import crypto from "node:crypto";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const finalRoot = path.resolve(here, "..");
const repository = execFileSync("git", ["rev-parse", "--show-toplevel"], {
  encoding: "utf8",
}).trim();
const ownerPrefix = "docs/tamar-vey/v708-v3-r2/";
const finalPrefix = `${ownerPrefix}final/`;
const exclusions = new Set([
  `${finalPrefix}validation/final-owner-manifest.json`,
  `${finalPrefix}validation/final-delta-manifest.json`,
  `${finalPrefix}validation/final-staged-review.json`,
  `${finalPrefix}closeout/content-seal.json`,
]);

function git(args, encoding = "utf8") {
  return execFileSync("git", args, {
    cwd: repository,
    encoding,
    maxBuffer: 32 * 1024 * 1024,
  });
}

function lines(text) {
  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
}

function indexBytes(file) {
  return git(["show", `:${file}`], null);
}

function entry(file) {
  const bytes = indexBytes(file);
  return {
    path: file,
    bytes: bytes.length,
    sha256: crypto.createHash("sha256").update(bytes).digest("hex"),
  };
}

const ownerPaths = lines(git(["ls-files", ownerPrefix]))
  .filter((file) => !exclusions.has(file))
  .sort();
const deltaPaths = lines(
  git(["diff", "--cached", "--name-only", "--diff-filter=ACMR"]),
)
  .filter((file) => file.startsWith(finalPrefix) && !exclusions.has(file))
  .sort();

const ownerManifest = {
  schema: "ghc.tamar.v708-v3-r2.final-owner-manifest.v1",
  byte_domain: "staged_git_blob",
  exclusions: [...exclusions].sort(),
  entry_count: ownerPaths.length,
  entries: ownerPaths.map(entry),
};
const deltaManifest = {
  schema: "ghc.tamar.v708-v3-r2.final-delta-manifest.v1",
  byte_domain: "staged_git_blob",
  exclusions: [...exclusions].sort(),
  entry_count: deltaPaths.length,
  entries: deltaPaths.map(entry),
};

const sealTargets = [
  `${ownerPrefix}planning/phase-plan.md`,
  `${ownerPrefix}planning/source-faithful-ledger.json`,
  `${ownerPrefix}x1/phase-truth.json`,
  `${ownerPrefix}x1/method-flow.json`,
  `${ownerPrefix}x2/phase-truth.json`,
  `${ownerPrefix}x2/method-flow.json`,
  `${ownerPrefix}x2/architecture/local-cloud-nexus-summary.html`,
  `${ownerPrefix}x2/route/saelin-startup-template.md`,
  `${finalPrefix}final-integrated-overview.md`,
  `${finalPrefix}phase-truth.json`,
  `${finalPrefix}method-flow-final.json`,
  `${finalPrefix}complete-incomplete-checklist.json`,
  `${finalPrefix}saelin-activation-candidate.md`,
  `${finalPrefix}hand-off-baton.md`,
];
const contentSeal = {
  schema: "ghc.tamar.v708-v3-r2.content-seal.v1",
  byte_domain: "staged_git_blob",
  target_count: sealTargets.length,
  targets: sealTargets.map(entry),
};

fs.mkdirSync(path.join(finalRoot, "validation"), { recursive: true });
fs.mkdirSync(path.join(finalRoot, "closeout"), { recursive: true });
fs.writeFileSync(
  path.join(finalRoot, "validation", "final-owner-manifest.json"),
  `${JSON.stringify(ownerManifest, null, 2)}\n`,
  "utf8",
);
fs.writeFileSync(
  path.join(finalRoot, "validation", "final-delta-manifest.json"),
  `${JSON.stringify(deltaManifest, null, 2)}\n`,
  "utf8",
);
fs.writeFileSync(
  path.join(finalRoot, "closeout", "content-seal.json"),
  `${JSON.stringify(contentSeal, null, 2)}\n`,
  "utf8",
);
