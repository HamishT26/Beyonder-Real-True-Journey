param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("api_health", "gmut_lab", "vesper_sync")]
    [string]$Lane
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Python = (Get-Command python).Source
$LogDir = Join-Path $RepoRoot ".local-runtime\v42\scheduled-logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$LogPath = Join-Path $LogDir "$Lane-$Timestamp.log"

Set-Location $RepoRoot

function Invoke-Lane {
    param([string[]]$CommandArgs)

    $StdOutPath = Join-Path $LogDir "$Lane-$Timestamp.stdout.log"
    $StdErrPath = Join-Path $LogDir "$Lane-$Timestamp.stderr.log"
    $Process = Start-Process `
        -FilePath $Python `
        -ArgumentList $CommandArgs `
        -WorkingDirectory $RepoRoot `
        -NoNewWindow `
        -Wait `
        -PassThru `
        -RedirectStandardOutput $StdOutPath `
        -RedirectStandardError $StdErrPath

    foreach ($Path in @($StdOutPath, $StdErrPath)) {
        if (Test-Path $Path) {
            $Content = Get-Content -Raw $Path
            if ($Content) {
                Add-Content -Path $LogPath -Value $Content
                Write-Output $Content.TrimEnd()
            }
            Remove-Item $Path -Force
        }
    }

    if ($Process.ExitCode -ne 0) {
        throw "Command failed: $($CommandArgs -join ' ')"
    }
}

switch ($Lane) {
    "api_health" {
        Invoke-Lane -CommandArgs @("scripts/trinity_v42_api_automation_wave.py", "--scheduled")
        Invoke-Lane -CommandArgs @("scripts/trinity_v42_kai_automation_bridge.py")
    }
    "gmut_lab" {
        Invoke-Lane -CommandArgs @("scripts/trinity_v42_gmut_lab_bundle.py", "--scheduled")
    }
    "vesper_sync" {
        Invoke-Lane -CommandArgs @("scripts/trinity_v42_vesper_telemetry_sync.py", "--scheduled")
    }
}

Write-Output "lane=$Lane"
Write-Output "log=$LogPath"
