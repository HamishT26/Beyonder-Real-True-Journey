---
name: ghc-family-observation-window-coverage
description: Compute covered duration and missing intervals inside one observation window; duration is not measurement quality.
---

# Observation window coverage

Compute covered duration and missing intervals inside one observation window; duration is not measurement quality.

Use this capability when information theory needs the `coverage` operation. Read [the exact operation contract](references/contract.json) for inputs, examples and bounded acceptance. The runner is `ghc_family_capacity_dependency.py` in repository `scripts/` or the shared D-drive `global-tools/family-capacity-lab/scripts/` directory. It requires the matching shared core in that same directory.

Run `python -X utf8 -B ghc_family_capacity_dependency.py --input request.json --output result.json`. An explicit list of requests is supported. Output creation is exclusive; select a new local output path instead of overwriting evidence. No task messaging, API submission, system cleanup or host configuration occurs.

Check the complete typed result and original input. Rational values use integers or fraction strings, never Boolean values or approximate floats. Keep the declared bounds and any refused subject in the result. Successful arithmetic does not verify a real measurement, affected-party agreement, public authority or Stage 20 readiness.

When the trigger involves shared routing, read the current family index first. Preserve existing identities and model settings. The current schedule is a projection until a separately authorized terminal native action succeeds.
