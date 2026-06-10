# v261-v280 adaptive council multiplex TUI
param(
  [int]$Tail = 18,
  [int]$RefreshSeconds = 30
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
  Write-Host ('Refresh cadence: ' + $RefreshSeconds + ' seconds. Completion requires response files, not queued prompts.')
  Write-Host ('Updated: ' + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss zzz'))
  Write-Host ''
  foreach ($lane in $lanes) {
    Write-Host ('========== ' + $lane.Name + ' ==========')
    if (Test-Path -LiteralPath $lane.Path) {
      $content = Get-Content -LiteralPath $lane.Path
      $started = ($content | Select-String -Pattern 'V261-(SEED|BLOCK-[0-9]+)-START').Count
      $completed = ($content | Select-String -Pattern 'V261-(SEED|BLOCK-[0-9]+)-RESPONSE-END').Count
      $lastTurn = ($content | Select-String -Pattern 'V261-(SEED|BLOCK-[0-9]+)-END' | Select-Object -Last 1).Line
      if (-not $lastTurn) { $lastTurn = 'No v261 response completed yet.' }
      Write-Host ('Evidence strip: started=' + $started + ' completed_responses=' + $completed)
      Write-Host ('Last turn: ' + $lastTurn)
      $content | Select-Object -Last $Tail
    } else {
      Write-Host ('Waiting for log: ' + $lane.Path)
    }
    Write-Host ''
  }
  Start-Sleep -Seconds $RefreshSeconds
}
