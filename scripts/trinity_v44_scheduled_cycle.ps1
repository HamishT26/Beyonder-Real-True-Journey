param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("powershell_health", "api_health", "gmut_lab", "vesper_sync")]
    [string]$Lane
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Python = (Get-Command python).Source
$LogDir = Join-Path $RepoRoot ".local-runtime\v44\scheduled-logs"
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
    "powershell_health" {
        Invoke-Lane -CommandArgs @("scripts/trinity_v44_operator_surface_probe.py")
        Invoke-Lane -CommandArgs @("scripts/trinity_v44_codex_cli_probe.py")
        Invoke-Lane -CommandArgs @("scripts/trinity_v44_kai_orchestration_bridge.py")
    }
    "api_health" {
        Invoke-Lane -CommandArgs @("scripts/trinity_v44_cloud_sweep.py")
    }
    "gmut_lab" {
        Invoke-Lane -CommandArgs @("scripts/trinity_v44_gmut_lab_bundle.py", "--scheduled")
    }
    "vesper_sync" {
        Invoke-Lane -CommandArgs @("scripts/trinity_v44_vesper_memory_cognitive_bridge.py")
    }
}

Write-Output "lane=$Lane"
Write-Output "log=$LogPath"
