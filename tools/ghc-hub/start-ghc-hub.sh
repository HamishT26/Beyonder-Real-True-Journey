#!/bin/sh
# Run in the current Linux executor; use the menu's normal sudo action if needed.
set -eu
GHC_HUB_HOME=${GHC_HUB_HOME:-"$HOME/.local/state/ghc-hub"}
export GHC_HUB_HOME
exec node "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/hub.mjs" "$@"
