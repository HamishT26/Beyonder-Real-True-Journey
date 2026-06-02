# v471 THOS v4 x1 Browser Capability Probe

Status: `OPEN_GAP`.

The Browser skill and browser-client path were present and read before the probe. The live capability path did not return a usable `iab` browser surface in this thread. Attempt 1 timed out before a usable tab returned; attempt 2 returned the explicit signal `Browser is not available: iab`.

This is useful evidence, but only as a blocker ledger. It does not prove Browser automation, screenshot capture, local app testing, or UI coordination. The safe next step is to preserve a Browser recovery contract and retry only with a bounded setup cell plus a short capability check.
