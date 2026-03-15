{
  "generated_utc": "2026-03-14T10:37:16+00:00",
  "system_id": "uat_preprod_fabric_sync_bridge",
  "pillar": "body",
  "overall_status": "PASS",
  "checks": [
    {
      "name": "cache_written",
      "status": "PASS",
      "detail": "docs/trinity-mcp-cache/uat-preprod-fabric-latest.json"
    }
  ],
  "metrics": {
    "pack": "uat_preprod_fabric",
    "strategy": "local_repo",
    "record_count": 2,
    "auth_state": "local_repo",
    "cache_status": "active",
    "desired_state": "active",
    "actual_state": "active",
    "live_read_enabled": false,
    "live_write_enabled": false,
    "blocker_count": 0
  },
  "repo_targets_touched": [
    "docs/trinity-materialization-ladder-v1.json",
    "docs/trinity-mcp-cache/uat-preprod-fabric-latest.json",
    "docs/trinity-uat-preprod-targets-v1.json"
  ],
  "next_action": "Use UAT Pre-Prod Fabric outputs only after its gate stays PASS.",
  "effective_success": true,
  "records": [
    {
      "source_id": "uat_preprod_fabric",
      "record_id": "uat_preprod_fabric-seed",
      "signal_type": "pack_seed",
      "title": "Record pre-production mirror requirements, replay checks, and rollback rules without claiming live promotion 