#!/usr/bin/env node
// Compatibility entrypoint. The promoted runner now lives at ghc_main_orchestrator_runner.mjs.
await import("./ghc_main_orchestrator_runner.mjs");
