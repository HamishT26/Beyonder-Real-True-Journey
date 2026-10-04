[CmdletBinding()]
param(
    [ValidateSet('Codex','PowerShell','Probe')][string]$Target = 'Codex',
    [switch]$Check,
    [string]$TracePath
)
$ErrorActionPreference = 'Stop'
$ghcTraceWriter = $null
$ghcTraceClock = [Diagnostics.Stopwatch]::StartNew()
$ghcTraceBegins = @{}
$ghcTraceCurrentStage = 'initialization'
$ghcTraceOperation = [guid]::NewGuid().ToString()
$ghcTraceSource = $null
$ghcTraceDegraded = $false
function Get-GhcTraceDestination {
    param([string]$Path)
    $ghcTraceAbsolute = [IO.Path]::GetFullPath($Path)
    if (-not $ghcTraceAbsolute.StartsWith('D:\GHC-Archives\phase-banks\', [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Trace output must be a new file in the D-drive phase bank.'
    }
    $ghcTraceParent = [IO.DirectoryInfo]::new([IO.Path]::GetDirectoryName($ghcTraceAbsolute))
    if (-not (Test-Path -LiteralPath $ghcTraceParent.FullName -PathType Container)) {
        throw 'Create the owned trace directory before invoking this launcher.'
    }
    # Reject existing redirections. This is a point-in-time check; use an owned
    # directory that other processes do not mutate during this invocation.
    while ($null -ne $ghcTraceParent) {
        $ghcParentItem = Get-Item -LiteralPath $ghcTraceParent.FullName -Force
        if ($ghcParentItem.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            throw 'Trace directories must not contain reparse-point components.'
        }
        $ghcTraceParent = $ghcTraceParent.Parent
    }
    return $ghcTraceAbsolute
}
function Set-GhcTraceDegraded {
    $ghcAlreadyDegraded = $ghcTraceDegraded
    $script:ghcTraceDegraded = $true
    if (-not $ghcAlreadyDegraded) {
        try { [Console]::Error.WriteLine('GHC telemetry is incomplete; this does not establish a failed launch.') } catch { }
    }
}
function Close-GhcTrace {
    if ($null -ne $ghcTraceWriter) {
        try { $ghcTraceWriter.Dispose() } catch { Set-GhcTraceDegraded }
    }
}
function Write-GhcTraceStage {
    param([string]$Stage, [ValidateSet('begin','end','error')][string]$Phase, [string]$ExceptionType)
    if ($null -eq $ghcTraceWriter -or $ghcTraceDegraded) { return }
    $elapsed = $ghcTraceClock.Elapsed.TotalMilliseconds
    if ($Phase -eq 'begin') {
        $script:ghcTraceCurrentStage = $Stage
        $ghcTraceBegins[$Stage] = $elapsed
    }
    $duration = if ($Phase -ne 'begin' -and $ghcTraceBegins.ContainsKey($Stage)) { $elapsed - $ghcTraceBegins[$Stage] } else { $null }
    $row = [ordered]@{schema='ghc.launch-stage.v1';operation=$ghcTraceOperation;sourceSha256=$ghcTraceSource;stage=$Stage;phase=$Phase;utc=[datetime]::UtcNow.ToString('o');elapsedMs=$elapsed;stageDurationMs=$duration;exceptionType=$ExceptionType}
    try { $ghcTraceWriter.WriteLine(($row | ConvertTo-Json -Compress)) }
    catch { Set-GhcTraceDegraded }
}
if (-not $TracePath) {
    $ghcTraceFilename = '{0:yyyyMMddTHHmmssfffZ}-{1}-{2}.jsonl' -f [datetime]::UtcNow,$Target,$ghcTraceOperation
    $TracePath = Join-Path 'D:\GHC-Archives\phase-banks\ghc-launcher-traces' $ghcTraceFilename
}
try {
    $ghcTraceAbsolute = Get-GhcTraceDestination $TracePath
    $ghcTraceStream = [IO.File]::Open($ghcTraceAbsolute, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::Read)
    $ghcTraceWriter = [IO.StreamWriter]::new($ghcTraceStream, [Text.UTF8Encoding]::new($false))
    $ghcTraceWriter.AutoFlush = $true
    Write-GhcTraceStage 'source-fingerprint' 'begin'
    $ghcTraceSource = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    Write-GhcTraceStage 'source-fingerprint' 'end'
} catch {
    # Telemetry cannot turn a separately successful core action into failure.
    # An invalid/redirected destination is never opened by this fallback.
    Set-GhcTraceDegraded
}
try {
    $root = $PSScriptRoot
    $pwsh = 'D:\GHC-Archives\global-tools\powershell\7.6.6\pwsh.exe'
    $working = 'D:\GHC-Family-Laboratory'
    Write-GhcTraceStage 'token-observation' 'begin'
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]$identity
    $elevated = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    Write-GhcTraceStage 'token-observation' 'end'
    Write-GhcTraceStage 'pinned-powershell-existence' 'begin'
    if (-not (Test-Path -LiteralPath $pwsh)) { throw 'Pinned D PowerShell executable is unavailable.' }
    Write-GhcTraceStage 'pinned-powershell-existence' 'end'
    Write-GhcTraceStage 'powershell-signature' 'begin'
    $pwshSignature = Get-AuthenticodeSignature -LiteralPath $pwsh
    if ($pwshSignature.Status -ne 'Valid' -or $pwshSignature.SignerCertificate.Subject -notmatch 'Microsoft Corporation') {
        throw 'PowerShell signature validation failed.'
    }
    Write-GhcTraceStage 'powershell-signature' 'end'
    $appPath = $null
    if ($Target -eq 'Codex') {
        Write-GhcTraceStage 'app-package-discovery' 'begin'
        $packages = @(Get-AppxPackage -Name 'OpenAI.Codex')
        if ($packages.Count -ne 1) { throw 'Expected exactly one installed OpenAI.Codex package.' }
        Write-GhcTraceStage 'app-package-discovery' 'end'
        Write-GhcTraceStage 'manifest-selection' 'begin'
        [xml]$manifest = Get-Content -LiteralPath (Join-Path $packages[0].InstallLocation 'AppxManifest.xml') -Raw
        $apps = @($manifest.Package.Applications.Application | Where-Object Id -eq 'App')
        if ($apps.Count -ne 1) { throw 'Could not resolve the installed app entry point.' }
        Write-GhcTraceStage 'manifest-selection' 'end'
        Write-GhcTraceStage 'package-path-containment' 'begin'
        $appPath = [IO.Path]::GetFullPath((Join-Path $packages[0].InstallLocation $apps[0].Executable))
        if (-not $appPath.StartsWith($packages[0].InstallLocation + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'App path escaped package.' }
        Write-GhcTraceStage 'package-path-containment' 'end'
        Write-GhcTraceStage 'app-signature' 'begin'
        $signature = Get-AuthenticodeSignature -LiteralPath $appPath
        if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'OpenAI') { throw 'App signature validation failed.' }
        Write-GhcTraceStage 'app-signature' 'end'
    }
    if ($Check) {
        Write-GhcTraceStage 'terminal-check-no-launch' 'begin'
        Write-GhcTraceStage 'terminal-check-no-launch' 'end'
        [pscustomobject]@{target=$Target;currentProcessAdministrator=$elevated;powerShell=$pwsh;app=$appPath;workingDirectory=$working;uacPromptExpected=(-not $elevated);launchPerformed=$false} | ConvertTo-Json
        return
    }
    if ($Target -eq 'Probe') {
        $probe = Join-Path $root 'Test-GhcAdmin.ps1'
        $arguments = '-NoLogo -NoProfile -NonInteractive -File "' + $probe + '"'
        $parameters = @{FilePath=$pwsh;ArgumentList=$arguments;WorkingDirectory=$working;WindowStyle='Hidden';PassThru=$true;Wait=$true}
        if (-not $elevated) { $parameters.Verb = 'RunAs' }
        Write-GhcTraceStage 'probe-execution-and-wait' 'begin'
        $process = Start-Process @parameters
        Write-GhcTraceStage 'probe-execution-and-wait' 'end'
        if ($process.ExitCode -ne 0) { throw "Administrator probe exited $($process.ExitCode)." }
        Get-Content -LiteralPath (Join-Path $root 'administrator-probe.json') -Raw
        Write-GhcTraceStage 'terminal-probe-completed' 'begin'
        Write-GhcTraceStage 'terminal-probe-completed' 'end'
        return
    }
    if ($Target -eq 'PowerShell') {
        $parameters = @{FilePath=$pwsh;ArgumentList='-NoLogo -NoExit';WorkingDirectory=$working;WindowStyle='Normal';PassThru=$true}
        if (-not $elevated) { $parameters.Verb = 'RunAs' }
        Write-GhcTraceStage 'powershell-start-request' 'begin'
        Start-Process @parameters | Select-Object Id,ProcessName
        Write-GhcTraceStage 'powershell-start-request' 'end'
        Write-GhcTraceStage 'terminal-powershell-start-requested' 'begin'
        Write-GhcTraceStage 'terminal-powershell-start-requested' 'end'
        return
    }
    Write-GhcTraceStage 'existing-process-check' 'begin'
    $existing = @(Get-Process -Name ChatGPT -ErrorAction SilentlyContinue | Where-Object { try { $_.Path -eq $appPath } catch { $false } })
    if ($existing.Count -gt 0) {
        throw 'Close the existing ChatGPT/Codex app after saving work, then use this launcher. An already-running app can retain its original non-admin token.'
    }
    Write-GhcTraceStage 'existing-process-check' 'end'
    $parameters = @{FilePath=$appPath;WorkingDirectory=$working;WindowStyle='Normal';PassThru=$true}
    if (-not $elevated) { $parameters.Verb = 'RunAs' }
    Write-GhcTraceStage 'app-start-request' 'begin'
    Start-Process @parameters | Select-Object Id,ProcessName
    Write-GhcTraceStage 'app-start-request' 'end'
    Write-GhcTraceStage 'terminal-app-start-requested' 'begin'
    Write-GhcTraceStage 'terminal-app-start-requested' 'end'
} catch {
    Write-GhcTraceStage $ghcTraceCurrentStage 'error' $_.Exception.GetType().FullName
    throw
} finally {
    Close-GhcTrace
}
