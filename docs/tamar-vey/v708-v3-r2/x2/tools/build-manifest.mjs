import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const excluded = new Set([
  "validation/x2-manifest.json",
  "validation/x2-staged-review.json",
]);

function walk(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(full) : [full];
  });
}

const entries = walk(root)
  .map((full) => ({
    full,
    relative: path.relative(root, full).replaceAll("\\", "/"),
  }))
  .filter(({ relative }) => !excluded.has(relative))
  .sort((a, b) => a.relative.localeCompare(b.relative))
  .map(({ full, relative }) => {
    const bytes = fs.readFileSync(full);
    return {
      path: `docs/tamar-vey/v708-v3-r2/x2/${relative}`,
      bytes: bytes.length,
      sha256: crypto.createHash("sha256").update(bytes).digest("hex"),
    };
  });

const manifest = {
  schema: "ghc.tamar.v708-v3-r2.x2.manifest.v1",
  byte_domain: "working_tree_exact_bytes_before_x2_commit",
  exclusions: [...excluded].sort(),
  entry_count: entries.length,
  entries,
};
fs.mkdirSync(path.join(root, "validation"), { recursive: true });
fs.writeFileSync(
  path.join(root, "validation", "x2-manifest.json"),
  `${JSON.stringify(manifest, null, 2)}\n`,
  "utf8",
);
