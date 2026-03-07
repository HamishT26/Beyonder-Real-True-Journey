#!/usr/bin/env bash
set -eu

CODEX_DIR="$HOME/.codex"
CONFIG_FILE="$CODEX_DIR/config.toml"

mkdir -p "$CODEX_DIR"

if [ ! -f "$CONFIG_FILE" ]; then
  cat > "$CONFIG_FILE" <<'EOF'
model = "gpt-5.4"
model_reasoning_effort = "xhigh"

[windows]
sandbox = "elevated"
EOF
fi

echo "Safe bootstrap complete. Review config manually before enabling extra integrations."
