# V67 Provider Decision Board

```json
{
  "generated_utc": "2026-04-29T09:35:13+00:00",
  "phase": "v60_v67_hybrid_omega",
  "lanes": [
    {
      "provider": "notion",
      "state": "blocked_missing_parent",
      "next_allowed_action": "provide shared parent page or data source ID",
      "live_write_enabled": false,
      "secret_policy": "raw_values_never_written"
    },
    {
      "provider": "browser_use",
      "state": "runtime_available_current_session",
      "next_allowed_action": "use in-app browser for local dashboard/doc probes; no sensitive form submission without action-time confirmation",
      "live_write_enabled": false,
      "secret_policy": "raw_values_never_written"
    },
    {
      "provider": "vercel",
      "state": "missing_cli_or_path",
      "next_allowed_action": "read-only project/account probe before any preview project",
      "live_write_enabled": false,
      "secret_policy": "raw_values_never_written"
    },
    {
      "provider": "cloudflare",
      "state": "cli_available_read_gate_next",
      "next_allowed_action": "read-only account/pages/workers probe before any disposable worker",
      "live_write_enabled": false,
      "secret_policy": "raw_values_never_written"
    },
    {
      "provider": "neon",
      "state": "missing_cli_or_path",
      "next_allowed_action": "read-only project/database probe before any branch/schema",
      "live_write_enabled": false,
      "secret_policy": "raw_values_never_written"
    },
    {
      "provider": "render",
      "state": "missing_cli_or_path",
      "next_allowed_action": "read-only service-list/API probe before any service scaffold",
      "live_write_enabled": false,
      "secret_policy": "raw_values_never_written"
    },
    {
      "provider": "expo",
      "state": "npx_available",
      "next_allowed_action": "local Expo preview only, no EAS cloud build until auth gate",
      "live_write_enabled": false,
      "secret_policy": "raw_values_never_written"
    },
    {
      "provider": "github",
      "state": "cli_available_read_gate_next",
      "next_allowed_action": "app connector succeeded for PR #45, gh shell auth may still need login",
      "live_write_enabled": false,
      "secret_policy": "raw_values_never_written"
    },
    {
      "provider": "circleci",
      "state": "cli_available_read_gate_next",
      "next_allowed_action": "config validation/read status before pipeline trigger",
      "live_write_enabled": false,
      "secret_policy": "raw_values_never_written"
    },
    {
      "provider": "google_drive",
      "state": "operator_hold",
      "next_allowed_action": "do not promote Drive as authoritative without explicit policy change",
      "live_write_enabled": false,
      "secret_policy": "raw_values_never_written"
    },
    {
      "provider": "figma",
      "state": "read_only_view_seat",
      "next_allowed_action": "read-only capture with explicit file key/node ID",
      "live_write_enabled": false,
      "secret_policy": "raw_values_never_written"
    },
    {
      "provider": "oracle_cloud",
      "state": "cli_available_read_gate_next",
      "next_allowed_action": "read-only tenancy/region/limit probe before any OKE resource creation",
      "live_write_enabled": false,
      "secret_policy": "raw_values_never_written"
    },
    {
      "provider": "multi_cli_windows",
      "state": "cli_available_read_gate_next",
      "next_allowed_action": "visible terminal orchestration only after exact commands and data-sharing boundary are confirmed",
      "live_write_enabled": false,
      "secret_policy": "raw_values_never_written"
    }
  ]
}
```
