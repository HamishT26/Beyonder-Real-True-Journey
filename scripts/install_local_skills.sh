#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$REPO_ROOT/skills"
DEST_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$DEST_ROOT"

count=0
for skill_dir in "$SRC_DIR"/*; do
  [ -d "$skill_dir" ] || continue
  name="$(basename "$skill_dir")"
  rm -rf "$DEST_ROOT/$name"
  cp -R "$skill_dir" "$DEST_ROOT/$name"
  count=$((count+1))
  echo "Installed skill: $name -> $DEST_ROOT/$name"
done

echo "Installed $count local skill(s)."
echo "Restart Codex to pick up new skills."
