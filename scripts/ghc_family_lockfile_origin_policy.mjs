import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
const root = dirname(dirname(fileURLToPath(import.meta.url)));
const required = ["x2/tooling/node-lock-receipt.json"];
const missing = required.filter((value) => !existsSync(join(root, "docs", "neris-solane", "v667-v8-r2", value)));
console.log(JSON.stringify({status: missing.length ? "OPEN_GAP" : "PASS", runner: "lockfile", missing, scope: "Neris v667-v8-r2 owner-local evidence only"}));
process.exitCode = missing.length ? 1 : 0;
