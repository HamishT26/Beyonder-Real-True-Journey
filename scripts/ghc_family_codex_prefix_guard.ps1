$root = Split-Path -Parent $PSScriptRoot
$required = @('x2/environment-receipt.json')
$missing = @($required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $root (Join-Path 'docs\neris-solane\v667-v8-r2' $_))) })
$status = if ($missing.Count -eq 0) { 'PASS' } else { 'OPEN_GAP' }
[pscustomobject]@{ status = $status; runner = 'codex-prefix'; missing = $missing; scope = 'Neris v667-v8-r2 owner-local evidence only' } | ConvertTo-Json -Compress
if ($missing.Count -ne 0) { exit 1 }
