# V58 Workbench V3-V6 Jump

```json
{
  "generated_utc": "2026-04-28T17:34:14+00:00",
  "phase": "v58_omega",
  "versions": {
    "v3": {
      "path": "C:\\Users\\hamis\\OneDrive\\Documents\\New project\\trinity-workbench-contract-v3.json",
      "surface_count": 5,
      "allowed_triggers": [
        "read dashboards",
        "read command index",
        "read API book",
        "render workbench summaries"
      ],
      "disabled_write_paths": [
        "repo bypass writes",
        "authority override writes",
        "cloud bootstrap writes"
      ],
      "runtime_dependencies": [
        "python",
        "optional_postgres",
        "optional_docker"
      ]
    },
    "v4": {
      "path": "C:\\Users\\hamis\\OneDrive\\Documents\\New project\\trinity-workbench-contract-v4.json",
      "surface_count": 4,
      "allowed_triggers": [
        "read dashboards",
        "read command index",
        "read API book",
        "render v13 summaries"
      ],
      "disabled_write_paths": [
        "repo bypass writes",
        "authority override writes",
        "google drive bootstrap writes"
      ],
      "runtime_dependencies": [
        "python",
        "optional_docker",
        "optional_postgres"
      ]
    },
    "v5": {
      "path": "C:\\Users\\hamis\\OneDrive\\Documents\\New project\\trinity-workbench-contract-v5.json",
      "surface_count": 5,
      "allowed_triggers": [
        "read dashboards",
        "read command index",
        "read API book",
        "render v14 summaries"
      ],
      "disabled_write_paths": [
        "repo bypass writes",
        "authority override writes",
        "google drive bootstrap writes"
      ],
      "runtime_dependencies": [
        "python",
        "optional_docker",
        "optional_postgres"
      ]
    },
    "v6": {
      "path": "C:\\Users\\hamis\\OneDrive\\Documents\\New project\\trinity-workbench-contract-v6.json",
      "surface_count": 5,
      "allowed_triggers": [
        "read dashboards",
        "read command index",
        "read API book",
        "render v15/v16 summaries"
      ],
      "disabled_write_paths": [
        "repo bypass writes",
        "authority override writes",
        "google drive bootstrap writes"
      ],
      "runtime_dependencies": [
        "python",
        "optional_docker",
        "optional_postgres",
        "optional_kubernetes"
      ]
    }
  },
  "jumps": [
    {
      "from": "v3",
      "to": "v4",
      "added_surfaces": [
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\trinity-api-book-v2.json",
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\v13-trinity-verdict-v1.json"
      ],
      "removed_surfaces": [
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\trinity-api-book-v1.json",
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\trinity-memory-bank-registry-v3.json",
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\trinity-storage-posture-summary-v12.json"
      ]
    },
    {
      "from": "v4",
      "to": "v5",
      "added_surfaces": [
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\trinity-api-book-v3.json",
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\trinity-subagent-registry-v1.json",
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\v14-trinity-verdict-v1.json"
      ],
      "removed_surfaces": [
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\trinity-api-book-v2.json",
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\v13-trinity-verdict-v1.json"
      ]
    },
    {
      "from": "v5",
      "to": "v6",
      "added_surfaces": [
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\trinity-api-book-v5.json",
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\trinity-runtime-model-resolution-v1.json",
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\v16-trinity-verdict-v1.json"
      ],
      "removed_surfaces": [
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\trinity-api-book-v3.json",
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\trinity-subagent-registry-v1.json",
        "D:\\GHC-Archives\\worktrees\\v58-omega\\docs\\v14-trinity-verdict-v1.json"
      ]
    }
  ]
}
```
