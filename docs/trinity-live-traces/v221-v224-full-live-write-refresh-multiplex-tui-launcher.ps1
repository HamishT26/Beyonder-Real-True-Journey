$Host.UI.RawUI.WindowTitle = 'v221-v224 CLI Council Multiplex'
Write-Host 'v221-v224 CLI Council Multiplex - Arby / Kimi / Aster Vale'
Write-Host 'Close this window when finished. It tails local stdout logs only.'
$LaneDir = 'D:\GHC-Archives\worktrees\v58-omega\docs\trinity-live-traces\v221-v224-full-live-write-refresh-lane-logs'
$logs = @('arby.log','kimi.log','aster_vale.log') | ForEach-Object { Join-Path $LaneDir $_ }
while ($true) {
  Clear-Host
  Write-Host '=== v221-v224 CLI Council Multiplex ==='
  foreach ($log in $logs) {
    Write-Host ''
    Write-Host ('--- ' + (Split-Path $log -Leaf) + ' ---')
    if (Test-Path $log) { Get-Content -LiteralPath $log -Tail 14 } else { Write-Host 'waiting for log...' }
  }
  Start-Sleep -Seconds 5
}
