# v506 GMUT/THOS v42 v1 x1 Cleanup Candidate Manifest v1

Generated: 2026-06-11 NZ evening

Status: NO_DELETE_CANDIDATE_MANIFEST

## Purpose

This manifest turns the Node readiness receipt into an exact, reviewable cleanup planning surface. It does not authorize deletion. It only separates backup-first candidates from preserve-by-default material so the later cleanup phase can be precise.

## Candidate Class A: Backup-First Review

These are stale-looking or legacy temporary staging entries that may be worth backing up to D before any future cleanup decision:

- `legacy-primary-runtime-skills`, about 0.33 MB.
- `marketplaces`, about 0 MB.
- `plugins-backup-32QPLh`, about 37.80 MB.
- `plugins-backup-ksimey`, about 31.03 MB.
- `plugins-backup-Mgbfom`, about 33.57 MB.
- `plugins-backup-N2Ohq3`, about 0 MB.
- `plugins-backup-OJ2Y3i`, about 7.45 MB.
- `plugins-backup-qbOXwI`, about 0 MB.

Approximate candidate recovery if all backup-first candidates were later approved and safely removed: about 110 MB.

## Candidate Class B: Preserve By Default

These should not be deleted or moved without a much narrower packet and stronger evidence:

- `bundled-marketplaces`, about 441.10 MB.
- `plugins`, about 57.57 MB.
- `plugins.sha`, about 0 MB.
- `plugins.sync.lock`, about 0 MB.

## Required Future Cleanup Flow

1. Confirm Codex app and plugin sync are not actively using candidate folders.
2. Copy exact candidates to a D-drive cold backup location.
3. Hash and count backup copies.
4. Verify current Codex CLI/App startup still works.
5. Request or rely on a cleanup packet that explicitly authorizes deleting the exact listed candidates.
6. Delete only exact approved candidates.
7. Record before/after C-drive free space.

## Not Authorized Here

- No deletion.
- No movement.
- No compression.
- No plugin-cache mutation.
- No user-skill mutation.
- No session-store mutation.
- No account or app setting mutation.

All GMUT, canon, empirical, legal, and consciousness gates remain open.
