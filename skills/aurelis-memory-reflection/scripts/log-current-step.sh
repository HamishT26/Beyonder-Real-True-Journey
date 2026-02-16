#!/usr/bin/env bash
set -euo pipefail
python3 scripts/aurelis_memory_update.py \
  --nzdt-context "${NZDT_CONTEXT:?Set NZDT_CONTEXT}" \
  --user-message "${USER_GIST:?Set USER_GIST}" \
  --assistant-reflection "${ASSISTANT_REFLECTION:?Set ASSISTANT_REFLECTION}" \
  --progress-snapshot "${PROGRESS_SNAPSHOT:?Set PROGRESS_SNAPSHOT}" \
  --next-step "${NEXT_STEP:?Set NEXT_STEP}"
