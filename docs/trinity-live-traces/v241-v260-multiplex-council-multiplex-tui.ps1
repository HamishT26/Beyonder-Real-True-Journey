# v241-v260 local multiplex TUI
# Generated UTC: 2026-05-14T05:43:02.276491+00:00
param(
  [int]$Tail = 18,
  [int]$RefreshSeconds = 3
)

$ErrorActionPreference = 'SilentlyContinue'
$lanes = @(
  @{ Name = 'Arby'; Path = 'D:\GHC-Archives\worktrees\v58-omega\docs\trinity-live-traces\v241-v260-multiplex-council-lane-logs\arby.log' },
  @{ Name = 'Kimi'; Path = 'D:\GHC-Archives\worktrees\v58-omega\docs\trinity-live-traces\v241-v260-multiplex-council-lane-logs\kimi.log' },
  @{ Name = 'Aster Vale'; Path = 'D:\GHC-Archives\worktrees\v58-omega\docs\trinity-live-traces\v241-v260-multiplex-council-lane-logs\aster_vale.log' }
)

while ($true) {
  Clear-Host
  Write-Host 'v241-v260 Multiplex Council TUI - local log mode'
  Write-Host 'Remote-control QR pairing is postponed; this view tails local lane logs only.'
  Write-Host ('Updated: ' + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss zzz'))
  Write-Host ''
  foreach ($lane in $lanes) {
    Write-Host ('========== ' + $lane.Name + ' ==========')
    if (Test-Path -LiteralPath $lane.Path) {
      $content = Get-Content -LiteralPath $lane.Path
      $queued = ($content | Select-String -SimpleMatch 'OUTBOUND-QUEUED').Count
      $completed = ($content | Select-String -SimpleMatch 'REAL-PROBE-RESPONSE-END').Count
      $lastProbe = ($content | Select-String -SimpleMatch 'REAL-PROBE-END' | Select-Object -Last 1).Line
      if (-not $lastProbe) { $lastProbe = 'No real probe completed yet.' }
      Write-Host ('Evidence strip: queued=' + $queued + ' completed_real_probes=' + $completed)
      Write-Host ('Last probe: ' + $lastProbe)
      $content | Select-Object -Last $Tail
    } else {
      Write-Host ('Missing log: ' + $lane.Path)
    }
    Write-Host ''
  }
  Start-Sleep -Seconds $RefreshSeconds
}
