# Supported commands at the recorded Hub baseline

Invoke `node D:/GHC-Archives/global-tools/ghc-nexus-hub/hub.mjs ...` with a verified Node executable. The `ghc-nexus` shims are conveniences; resolve an alias before trusting which installation it invokes.

| Read or plan | Effect, only within current authorization |
|---|---|
| `actions --json`; `plan ACTION --json` | `run ACTION --execute` (`--json` only for noninteractive actions) |
| `chats list --json`; `chats resolve --id ID --json`; `chats plan --id ID --json` | `chats open --id ID --execute` performs current provider admission; never remove a lock. |
| `lab catalogue --json`; `lab plan --id diffusion --size 1000 --json` | `lab run --id diffusion --size 1000 --execute --json`; other finite IDs: `queue`, `consent`. |
| `remote plan --json` or `remote plan --file ABSOLUTE-JSON --json` | `remote connect --execute` needs an interactive terminal and supported configured host. |
| `identity list --json`; `identity show --id ID --json` | `identity certificate --id ID --execute --json` creates a local integrity record, not legal authentication or professional qualification. |
| `memory list --json`; `memory show --id ID --json` | `memory export --id ID1,ID2 --execute --json` selects only records explicitly classified shareable; review content before transmission. |
| `sentinel template --json`; `sentinel validate --file ABSOLUTE-JSON --json`; `sentinel plan --file ABSOLUTE-JSON --json` | `sentinel save --file ABSOLUTE-JSON --execute --json` saves a specification; it does not train or deploy a model. |

`chats list --refresh` queries provider metadata and may save its snapshot. `doctor --json` runs bounded version/token probes and journals an event. These are not zero-I/O operations. Avoid them when an existing exact receipt suffices.

Interactive shells, new Codex sessions, cloud pickers, sign-in and browser-opening actions exist in the Hub but are not implied by installing this package. New `codex` actions have explicit model/access request arguments; existing-session resume preserves its selected settings. Do not change global configuration to imitate those invocation arguments.

No `ghc-nexus config`, generic `exec`, automatic deployment, or shared credential-vault command exists at this baseline. Use the Config Menu plugin's proposal helper for selected configuration inspection.

Hub 2.2 adds `memory snapshot`, `memory snapshot-verify` and `memory restore`. Snapshot/restore stay local and accept only named memory records, with a saved fingerprint required for restore. They do not upload automatically or replace live records.
