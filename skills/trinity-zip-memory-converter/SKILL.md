---
name: trinity-zip-memory-converter
description: Compress Trinity memory/data artifacts into indexed zip snapshots and extract them for full reflection/recovery when needed.
---

# Trinity Zip Memory Converter

Use when users ask to compress memory/data updates, create archive snapshots, or restore prior snapshots.

## Workflow
1. Create archive snapshot:
   - `python3 scripts/trinity_zip_memory_converter.py archive --label "memory-cycle"`
2. List/search index entries:
   - `python3 scripts/trinity_zip_memory_converter.py list --limit 10 --label-contains memory-update`
3. Extract when needed:
   - `python3 scripts/trinity_zip_memory_converter.py extract --archive docs/memory-archives/<archive>.zip --dest docs/memory-archives/extracted`
4. Recall directly from index (biological-style memory retrieval):
   - `python3 scripts/trinity_zip_memory_converter.py recall --label-contains memory-update --latest --dest docs/memory-archives/recalled`
5. Encrypt snapshots at rest when needed:
   - `python3 scripts/trinity_zip_memory_converter.py archive --label "memory-cycle" --encrypt-passphrase "<secret>"`
6. Prune retention window:
   - `python3 scripts/trinity_zip_memory_converter.py prune --keep-last 200 --label-contains memory-update --delete-files`

## Notes
- `scripts/aurelis_memory_update.py` triggers an archive automatically unless `--skip-zip-archive` is used.
- `aurelis_memory_update.py` can write encrypted archives with `--zip-encrypt-passphrase` and apply post-write retention via `--zip-keep-last` (plus optional `--zip-prune-delete-files`).
- Archive includes memory logs, summaries, integrity report, suite status/report, transmutation outputs, and mammoth capsule artifacts when present.
