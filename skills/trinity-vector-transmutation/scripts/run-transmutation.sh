#!/usr/bin/env bash
set -euo pipefail

python3 scripts/trinity_vector_transmuter.py \
  --energy "${ENERGY:-0.82}" \
  --information "${INFORMATION:-0.88}" \
  --memory "${MEMORY:-0.90}" \
  --identity "${IDENTITY:-0.89}" \
  --governance "${GOVERNANCE:-0.94}" \
  --passphrase "${PASSPHRASE:?Set PASSPHRASE}" \
  --out "${OUT:-docs/trinity-vector-profile.json}"
