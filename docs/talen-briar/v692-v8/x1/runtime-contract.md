# Trusted text runtime

Execute a runner using Node with a trusted vm.Script bootstrap, passing the runner TXT path followed by --input and --output. The runner reads only its declared core dependency and caller JSON file. Outputs require a new path and use exclusive creation. JSON data is never compiled. Core evaluation has no filesystem, network or process API. Base records are capped at eight labels; derived products at sixteen. The runner scopes the operation allowlist.

Example bootstrap: node -e "require('node:vm').runInThisContext(require('node:fs').readFileSync(process.argv[1],'utf8'),{filename:process.argv[1]})" RUNNER.txt --input INPUT.json --output NEW_OUTPUT.json

Same-owner finite synthetic software evidence only; not independent reproduction, empirical GMUT confirmation, production THOS or Freed ID, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, AGI/ASI, consciousness, personhood, identity continuity, Theory-of-Everything proof, canon, deployment or Stage 20 readiness.
