# Selected-layer inspection and proposal contract

Python 3.11+ is required for standard-library TOML parsing. On this Windows host, use the existing `D:/GHC-Archives/global-tools/python/ghc-family-tools/Scripts/python.exe`; do not install a new interpreter for this plugin. The helper writes only JSON to stdout.

Create a private input JSON file with this shape (replace example paths with known selected files):

```json
{"schemaVersion":1,"layers":[{"name":"user","path":"C:/Users/hamis/.codex/config.toml","active":true},{"name":"project","path":"D:/your-owned-project/.codex/config.toml","active":false}]}
```

The array explicitly orders selected layers from lower to higher precedence. `active` is the caller's declaration, not a measurement of project trust. Missing layers, duplicate names/paths, linked paths, oversized files and malformed TOML are reported without exposing raw contents. No environment, MDM or remote discovery is attempted.

```text
python -B <plugin-root>/scripts/config_menu.py inspect --spec <absolute-spec.json>
python -B <plugin-root>/scripts/config_menu.py propose --spec <absolute-spec.json> --target user --expected-sha256 <inspected-hash> --set tui.animations=false
```

Use `--set` repeatedly for a small combined proposal. Booleans are JSON `true` or `false`; alternate screen accepts JSON strings `"auto"`, `"always"`, or `"never"`. Pass arguments through the terminal tool's normal quoting rules; no command is evaluated from the JSON.

`ready-for-review` means the supplied target still matches and no supplied active higher layer conflicts. It does not mean approved, applied, valid for every Codex setting, or effective in the running client. A backup/rollback recipe is included in the proposal. Actual file mutation remains the integrator's separately authorized operation.
