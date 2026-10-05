[CmdletBinding()]
param(
    [ValidateSet('Codex','PowerShell','Probe')][string]$Target = 'Codex',
    [switch]$Check,
    [string]$TracePath,
    [ValidateSet('DirectAdministrator','Registered','RegisteredAdministrator')][string]$AppActivation = 'DirectAdministrator'
)
$ErrorActionPreference = 'Stop'
if ($Target -ne 'Codex' -and $AppActivation -ne 'DirectAdministrator') {
    throw 'Registered app activation is available only for the Codex target.'
}
$ghcTraceWriter = $null
$ghcTraceStream = $null
$ghcTraceClock = [Diagnostics.Stopwatch]::StartNew()
$ghcTraceBegins = @{}
$ghcTraceWorkBegins = @{}
$ghcTraceCurrentStage = 'initialization'
$ghcTraceOperation = [guid]::NewGuid().ToString()
$ghcTraceSource = $null
$ghcTraceDegraded = $false
function Get-GhcTraceDestination {
    param([string]$Path)
    if (-not [IO.Path]::IsPathFullyQualified($Path) -or $Path.Substring(2).Contains(':')) {
        throw 'Trace output requires a fully qualified ordinary path without stream syntax.'
    }
    $ghcTraceLeaf = [IO.Path]::GetFileName($Path)
    if ($ghcTraceLeaf -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]*\.jsonl$' -or
        $ghcTraceLeaf -match '^(CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])\.' -or
        $ghcTraceLeaf.EndsWith('.') -or $ghcTraceLeaf.EndsWith(' ')) {
        throw 'Trace output requires an ordinary non-device JSONL filename.'
    }
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
    elseif ($null -ne $ghcTraceStream) {
        try { $ghcTraceStream.Dispose() } catch { Set-GhcTraceDegraded }
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
    $workDuration = if ($Phase -ne 'begin' -and $ghcTraceWorkBegins.ContainsKey($Stage)) { $elapsed - $ghcTraceWorkBegins[$Stage] } else { $null }
    $beginRecordDuration = if ($Phase -ne 'begin' -and $ghcTraceWorkBegins.ContainsKey($Stage)) { $ghcTraceWorkBegins[$Stage] - $ghcTraceBegins[$Stage] } else { $null }
    $row = [ordered]@{schema='ghc.launch-stage.v2';operation=$ghcTraceOperation;sourceSha256=$ghcTraceSource;stage=$Stage;phase=$Phase;utc=[datetime]::UtcNow.ToString('o');elapsedMs=$elapsed;stageDurationMs=$duration;workDurationMs=$workDuration;beginRecordMs=$beginRecordDuration;exceptionType=$ExceptionType}
    try {
        $ghcTraceWriter.WriteLine(($row | ConvertTo-Json -Compress))
        if ($Phase -eq 'begin') { $ghcTraceWorkBegins[$Stage] = $ghcTraceClock.Elapsed.TotalMilliseconds }
    }
    catch { Set-GhcTraceDegraded }
}
function Get-GhcAppDuplicateState {
    param([object[]]$Processes, [string]$ExpectedPath)
    $unknown = $false
    foreach ($candidate in $Processes) {
        try {
            $candidatePath = $candidate.Path
            if ([string]::IsNullOrWhiteSpace($candidatePath)) { $unknown = $true }
            elseif ([string]::Equals($candidatePath, $ExpectedPath, [StringComparison]::OrdinalIgnoreCase)) { return 'present' }
        } catch { $unknown = $true }
    }
    if ($unknown) { return 'unknown' }
    return 'absent'
}
function Open-GhcTraceStream {
    param([string]$Path)
    $destination = Get-GhcTraceDestination $Path
    return [IO.File]::Open($destination, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::Read)
}
function Get-GhcRegisteredAppUserModelId {
    param([string]$PackageFamilyName, [string]$ApplicationId)
    if ($PackageFamilyName -cnotmatch '^OpenAI\.Codex_[a-z0-9]{13}\z' -or $ApplicationId -cne 'App') {
        throw 'Unexpected package family or application identifier; activation held.'
    }
    $appUserModelId = $PackageFamilyName + '!' + $ApplicationId
    return $appUserModelId
}
function Get-GhcRegisteredAppItem {
    param([ValidatePattern('^OpenAI\.Codex_[a-z0-9]{13}!App\z')][string]$AppUserModelId)
    $ghcShell = New-Object -ComObject Shell.Application
    $ghcFolder = $ghcShell.NameSpace('shell:AppsFolder')
    if ($null -eq $ghcFolder) { throw 'Windows registered-app folder is unavailable.' }
    $ghcItem = $ghcFolder.ParseName($AppUserModelId)
    if ($null -eq $ghcItem) { throw 'Windows registered Codex entry is unavailable.' }
    return $ghcItem
}
function Get-GhcRegisteredElevationVerb {
    param([object]$AppItem)
    # Use only the elevation action actually exposed by this registered entry.
    # The inspected host uses English shell labels. Other locales fail closed.
    $ghcVerbs = @($AppItem.Verbs() | Where-Object { ($_.Name -replace '&','').Trim() -ceq 'Run as administrator' })
    if ($ghcVerbs.Count -ne 1) { throw 'The registered app does not expose one recognized Administrator action; use the normal registered launcher.' }
    return $ghcVerbs[0]
}
function Invoke-GhcGuardedAppStart {
    [CmdletBinding(DefaultParameterSetName='Direct')]
    param(
        [Parameter(Mandatory)][string]$ExpectedPath,
        [Parameter(Mandatory,ParameterSetName='Direct')][hashtable]$LaunchParameters,
        [Parameter(Mandatory,ParameterSetName='Registered')]
        [ValidatePattern('^OpenAI\.Codex_[a-z0-9]{13}!App\z')][string]$RegisteredAppUserModelId,
        [Parameter(ParameterSetName='Registered')][switch]$RegisteredAdministrator
    )
    Write-GhcTraceStage 'existing-process-check' 'begin'
    $ghcProcessErrors = @()
    $candidates = @(Get-Process -Name ChatGPT -ErrorAction SilentlyContinue -ErrorVariable ghcProcessErrors)
    $unexpectedErrors = @($ghcProcessErrors | Where-Object { $_.FullyQualifiedErrorId -notlike 'NoProcessFoundForGivenName*' })
    if ($unexpectedErrors.Count -gt 0) { throw 'App-process discovery failed; launch held without a retry.' }
    $duplicateState = Get-GhcAppDuplicateState -Processes $candidates -ExpectedPath $ExpectedPath
    if ($duplicateState -eq 'unknown') { throw 'An app-process path is unreadable; launch held without assuming absence.' }
    if ($duplicateState -eq 'present') { throw 'Close the existing ChatGPT/Codex app after saving work, then use this launcher. An already-running app can retain its original non-admin token.' }
    Write-GhcTraceStage 'existing-process-check' 'end'
    Write-GhcTraceStage 'app-start-request' 'begin'
    if ($PSCmdlet.ParameterSetName -eq 'Registered') {
        # Use the registered Windows application rather than the package's raw EXE.
        # No RunAs, caller working-directory promise, PassThru PID, or fallback:
        # Shell acceptance establishes neither app readiness nor its effective token.
        if ($RegisteredAdministrator) {
            $ghcAppItem = Get-GhcRegisteredAppItem -AppUserModelId $RegisteredAppUserModelId
            $ghcElevationVerb = Get-GhcRegisteredElevationVerb -AppItem $ghcAppItem
            $ghcElevationVerb.DoIt()
        } else {
            Start-Process -FilePath ('shell:AppsFolder\' + $RegisteredAppUserModelId) -ErrorAction Stop | Out-Null
        }
        [pscustomobject]@{
            target='Codex';activation=$(if($RegisteredAdministrator){'RegisteredAdministrator'}else{'Registered'});status='activation-requested'
            appUserModelId=$RegisteredAppUserModelId;launchRequested=$true
            elevationRequested=[bool]$RegisteredAdministrator;effectiveAdministrator=$null
            packageIdentityVerified=$false;appReady=$false;processId=$null
        }
    } else {
        Start-Process @LaunchParameters | Select-Object Id,ProcessName
    }
    Write-GhcTraceStage 'app-start-request' 'end'
}
if (-not $TracePath) {
    $ghcTraceFilename = '{0:yyyyMMddTHHmmssfffZ}-{1}-{2}.jsonl' -f [datetime]::UtcNow,$Target,$ghcTraceOperation
    $TracePath = Join-Path 'D:\GHC-Archives\phase-banks\ghc-launcher-traces' $ghcTraceFilename
}
try {
    $ghcTraceAbsolute = Get-GhcTraceDestination $TracePath
    $ghcTraceStream = Open-GhcTraceStream $ghcTraceAbsolute
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
    $appUserModelId = $null
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
        if ($AppActivation -in @('Registered','RegisteredAdministrator')) {
            Write-GhcTraceStage 'app-registration' 'begin'
            # Get-AppxPackage above selects this user's registered package. Resolve
            # its manifest application directly; do not enumerate the Start menu.
            $appUserModelId = Get-GhcRegisteredAppUserModelId -PackageFamilyName $packages[0].PackageFamilyName -ApplicationId $apps[0].Id
            if ($AppActivation -eq 'RegisteredAdministrator') {
                $ghcCheckedEntry = Get-GhcRegisteredAppItem -AppUserModelId $appUserModelId
                $null = Get-GhcRegisteredElevationVerb -AppItem $ghcCheckedEntry
            }
            Write-GhcTraceStage 'app-registration' 'end'
        }
    }
    if ($Check) {
        Write-GhcTraceStage 'terminal-check-no-launch' 'begin'
        Write-GhcTraceStage 'terminal-check-no-launch' 'end'
        $checkWorkingDirectory = $working
        $checkUacPromptExpected = -not $elevated
        if ($AppActivation -in @('Registered','RegisteredAdministrator')) { $checkWorkingDirectory = $null; $checkUacPromptExpected = $null }
        [pscustomobject]@{target=$Target;currentProcessAdministrator=$elevated;powerShell=$pwsh;app=$appPath;workingDirectory=$checkWorkingDirectory;uacPromptExpected=$checkUacPromptExpected;launchPerformed=$false;appActivation=$AppActivation;appUserModelId=$appUserModelId;elevationRequested=($AppActivation -ne 'Registered');registeredElevationVerbVerified=($AppActivation -eq 'RegisteredAdministrator');packageIdentityVerified=$false} | ConvertTo-Json
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
    if ($AppActivation -in @('Registered','RegisteredAdministrator')) {
        Invoke-GhcGuardedAppStart -ExpectedPath $appPath -RegisteredAppUserModelId $appUserModelId -RegisteredAdministrator:($AppActivation -eq 'RegisteredAdministrator')
    } else {
        $parameters = @{FilePath=$appPath;WorkingDirectory=$working;WindowStyle='Normal';PassThru=$true}
        if (-not $elevated) { $parameters.Verb = 'RunAs' }
        Invoke-GhcGuardedAppStart -ExpectedPath $appPath -LaunchParameters $parameters
    }
    Write-GhcTraceStage 'terminal-app-start-requested' 'begin'
    Write-GhcTraceStage 'terminal-app-start-requested' 'end'
} catch {
    Write-GhcTraceStage $ghcTraceCurrentStage 'error' $_.Exception.GetType().FullName
    throw
} finally {
    Close-GhcTrace
}
