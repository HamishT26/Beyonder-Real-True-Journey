# v261-v280 adaptive council multiplex TUI
param(
  [int]$Tail = 18,
  [int]$RefreshSeconds = 180
)

$ErrorActionPreference = 'SilentlyContinue'
$lanes = @(
  @{ Name = 'Arby'; Path = 'D:\GHC-Archives\worktrees\v58-omega\docs\trinity-live-traces\v261-v280-adaptive-council-lane-logs\arby.log' },
  @{ Name = 'Kimi'; Path = 'D:\GHC-Archives\worktrees\v58-omega\docs\trinity-live-traces\v261-v280-adaptive-council-lane-logs\kimi.log' },
  @{ Name = 'Aster Vale'; Path = 'D:\GHC-Archives\worktrees\v58-omega\docs\trinity-live-traces\v261-v280-adaptive-council-lane-logs\aster_vale.log' }
)

while ($true) {
  Clear-Host
  Write-Host 'v261-v280 Adaptive Council TUI - seed cycle'
  Write-Host 'Refresh cadence: 180 seconds. Completion requires response files, not queued prompts.'
  Write-Host ('Updated: ' + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss zzz'))
  Write-Host ''
  foreach ($lane in $lanes) {
    Write-Host ('========== ' + $lane.Name + ' ==========')
    if (Test-Path -LiteralPath $lane.Path) {
      $content = Get-Content -LiteralPath $lane.Path
      $started = ($content | Select-String -SimpleMatch 'V261-SEED-START').Count
      $completed = ($content | Select-String -SimpleMatch 'V261-SEED-RESPONSE-END').Count
      $lastSeed = ($content | Select-String -SimpleMatch 'V261-SEED-END' | Select-Object -Last 1).Line
      if (-not $lastSeed) { $lastSeed = 'No v261 seed response completed yet.' }
      Write-Host ('Evidence strip: started=' + $started + ' completed_seed_responses=' + $completed)
      Write-Host ('Last seed: ' + $lastSeed)
      $content | Select-Object -Last $Tail
    } else {
      Write-Host ('Waiting for log: ' + $lane.Path)
    }
    Write-Host ''
  }
  Start-Sleep -Seconds $RefreshSeconds
}
