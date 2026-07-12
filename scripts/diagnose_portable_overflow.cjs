#!/usr/bin/env node
"use strict";

// Deprecated compatibility entrypoint; use ghc_family_diagnose_portable_overflow.cjs.
const { diagnose } = require("./ghc_family_diagnose_portable_overflow.cjs");
const fs = require("node:fs");
const path = require("node:path");

const [input, output] = process.argv.slice(2);
if (!input || process.argv.length > 4) {
  throw new Error("usage: node diagnose_portable_overflow.cjs input.html [output.json]");
}
const result = diagnose(fs.readFileSync(input, "utf8"));
result.input_basename = path.basename(input);
const serialized = `${JSON.stringify(result, null, 2)}\n`;
if (output) fs.writeFileSync(output, serialized, "utf8");
process.stdout.write(serialized);
process.exitCode = result.status === "review_required" ? 2 : 0;
