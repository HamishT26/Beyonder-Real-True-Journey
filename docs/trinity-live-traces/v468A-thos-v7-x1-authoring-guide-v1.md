# v468A THOS v7 x1 Authoring Guide

This guide turns the v6 schema and fixture work into a repeatable manifest practice for future THOS and GMUT_THOS phases.

Every phase author should record start time in Pacific/Auckland time, local and upstream heads, drift, curated artifact list, blocked actions, validation chain, and the THOS/GMUT boundary. The manifest is not a celebration file; it is a receipt.

The manifest must state open GMUT gates unless exact closure artifacts exist. It must also make blocked cloud writes, broad cleanup, old-agent spawning, and publication risks visible rather than implied.

Copy route: start from `v468A-thos-v7-x1-template-manifest-v1.json`, update the live fields, run schema validation, run the Python publication guard, then stage only the curated files for the current phase.
