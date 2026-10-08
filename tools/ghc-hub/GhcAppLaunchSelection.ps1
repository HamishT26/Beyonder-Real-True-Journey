# Owned Hub2.6 candidate. Definitions only: no inventory, launch, close or writes on import.
function Get-GhcField {
    param([object]$Value,[string]$Name)
    if ($null -eq $Value) { return $null }
    $property = $Value.PSObject.Properties[$Name]
    if ($null -ne $property) { return $property.Value }
    return $null
}
function ConvertTo-GhcPackageVersion {
    param([object]$Value)
    $text = [string]$Value
    $version = $null
    if ($text -notmatch '^\d{1,5}(\.\d{1,5}){3}$' -or -not [version]::TryParse($text,[ref]$version) -or
        @($version.Major,$version.Minor,$version.Build,$version.Revision | Where-Object { $_ -gt 65535 }).Count -gt 0) {
        throw 'Invalid package version.'
    }
    return $version
}
function ConvertTo-GhcOrdinaryAppPath {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value) -or $Value -notmatch '^[A-Za-z]:[\\/]' -or
        $Value.Substring(2).Contains(':') -or $Value -match '[\x00-\x1f]' -or -not [IO.Path]::IsPathFullyQualified($Value)) {
        throw 'Expected an ordinary absolute local path.'
    }
    $full = [IO.Path]::GetFullPath($Value).TrimEnd('\')
    if ($full.Length -le 3) { throw 'An App path cannot be a drive root.' }
    return $full
}
function Resolve-GhcAppLaunchSelection {
    [CmdletBinding()]
    param(
        [AllowEmptyCollection()][object[]]$Packages,
        [scriptblock]$ReadManifest = { param($p) Get-Content -LiteralPath $p -Raw -ErrorAction Stop },
        [scriptblock]$TestExecutable = { param($p) Test-Path -LiteralPath $p -PathType Leaf },
        [scriptblock]$ReadSignature = { param($p) Get-AuthenticodeSignature -LiteralPath $p -ErrorAction Stop }
    )
    # Caller must supply a fresh current-user Get-AppxPackage -Name OpenAI.Codex -PackageTypeFilter Main snapshot.
    $records = [Collections.Generic.List[object]]::new()
    try {
        foreach ($package in @($Packages)) {
            if ((Get-GhcField $package 'Name') -ine 'OpenAI.Codex') { continue }
            if ((Get-GhcField $package 'IsFramework') -or (Get-GhcField $package 'IsResourcePackage') -or (Get-GhcField $package 'IsBundle')) { continue }
            $version = ConvertTo-GhcPackageVersion (Get-GhcField $package 'Version')
            $family = [string](Get-GhcField $package 'PackageFamilyName')
            $fullName = [string](Get-GhcField $package 'PackageFullName')
            $location = ConvertTo-GhcOrdinaryAppPath ([string](Get-GhcField $package 'InstallLocation'))
            if ($family -notmatch '^OpenAI\.Codex_[a-z0-9]{13}$') { throw 'Invalid package family.' }
            $publisherId = $family.Substring('OpenAI.Codex_'.Length)
            $identityPattern = '^OpenAI\.Codex_' + [regex]::Escape($version.ToString()) +
                '_(x86|x64|arm|arm64|x86a64|neutral)__' + [regex]::Escape($publisherId) + '$'
            if ($fullName -notmatch $identityPattern) { throw 'Invalid main-package identity.' }
            $records.Add([pscustomobject]@{Package=$package;Version=$version;Family=$family;FullName=$fullName;InstallLocation=$location})
        }
        if ($records.Count -eq 0) { return [pscustomobject]@{Status='held';Reason='no-current-user-main-package';Selected=$null} }
        if ($records.Count -gt 16) { throw 'Package snapshot exceeds the bounded limit.' }
        if (@($records.Family | Sort-Object -Unique).Count -ne 1) { throw 'Multiple package families need explicit reconciliation.' }
        $ordered = @($records | Sort-Object -Property Version -Descending)
        $top = @($ordered | Where-Object Version -eq $ordered[0].Version)
        $topIdentity = @($top | ForEach-Object { ($_.FullName + '|' + $_.InstallLocation).ToLowerInvariant() } | Sort-Object -Unique)
        if ($topIdentity.Count -ne 1) { throw 'Newest version has ambiguous package paths or architectures.' }
        $winner = $top[0]
        if ([string](Get-GhcField $winner.Package 'Status') -ine 'Ok') { throw 'Newest registered package is not healthy.' }
        [xml]$manifest = & $ReadManifest (Join-Path $winner.InstallLocation 'AppxManifest.xml')
        if ($manifest.Package.Identity.Name -ine 'OpenAI.Codex' -or
            (ConvertTo-GhcPackageVersion $manifest.Package.Identity.Version) -ne $winner.Version -or
            [string]$manifest.Package.Identity.Publisher -cne [string](Get-GhcField $winner.Package 'Publisher')) {
            throw 'Newest manifest identity does not match registration.'
        }
        $apps = @($manifest.Package.Applications.Application | Where-Object Id -ceq 'App')
        if ($apps.Count -ne 1) { throw 'Newest manifest must expose one App entry point.' }
        $relative = [string]$apps[0].Executable
        if ([string]::IsNullOrWhiteSpace($relative) -or [IO.Path]::IsPathRooted($relative)) { throw 'Invalid App executable.' }
        $executable = ConvertTo-GhcOrdinaryAppPath (Join-Path $winner.InstallLocation $relative)
        if (-not $executable.StartsWith($winner.InstallLocation + '\',[StringComparison]::OrdinalIgnoreCase)) { throw 'App executable escaped its package.' }
        if (-not (& $TestExecutable $executable)) { throw 'Newest App executable is unavailable.' }
        $signature = & $ReadSignature $executable
        if ([string]$signature.Status -ine 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'OpenAI') { throw 'Newest App signature failed.' }
        $selected = [pscustomobject]@{
            Version=$winner.Version.ToString();PackageFamilyName=$winner.Family;PackageFullName=$winner.FullName
            InstallLocation=$winner.InstallLocation;ExecutablePath=$executable;ApplicationId='App'
            AppUserModelId=($winner.Family+'!App');SignatureChecked=$true
            ProcessNames=@([IO.Path]::GetFileNameWithoutExtension($executable),'ChatGPT' | Sort-Object -Unique)
        }
        return [pscustomobject]@{Status='ready';Reason='newest-registered-version-validated';Selected=$selected;Metadata=$records.ToArray();DowngradePerformed=$false}
    } catch {
        # Never silently fall back to an older package when the newest candidate is unreadable, unhealthy or invalid.
        return [pscustomobject]@{Status='held';Reason='package-selection-or-validation-failed';Detail=$_.Exception.Message;Selected=$null;DowngradePerformed=$false}
    }
}
function Get-GhcAppRunningObservation {
    [CmdletBinding()]
    param([object]$Selection,[AllowEmptyCollection()][object[]]$Processes,[switch]$DiscoveryFailed)
    if ($DiscoveryFailed -or $Selection.Status -ne 'ready') {
        return [pscustomobject]@{State='unknown';CanLaunch=$false;Entries=@();Reason='discovery-or-selection-unavailable'}
    }
    $selected = $Selection.Selected
    $expected = ConvertTo-GhcOrdinaryAppPath $selected.ExecutablePath
    $selectedVersion = ConvertTo-GhcPackageVersion $selected.Version
    $storeRoot = [IO.Path]::GetDirectoryName($selected.InstallLocation).TrimEnd('\') + '\'
    $entries = [Collections.Generic.List[object]]::new()
    # Caller provides only processes named for selected.ProcessNames; never collect command lines.
    foreach ($process in @($Processes)) {
        $state='unknown';$evidence='unreadable-path';$observedVersion=$null;$processPath=$null;$processId=$null
        try {
            $processId = Get-GhcField $process 'Id'
            $processPath = ConvertTo-GhcOrdinaryAppPath ([string](Get-GhcField $process 'Path'))
            if ([string]::Equals($processPath,$expected,[StringComparison]::OrdinalIgnoreCase)) {
                $state='current-running';$evidence='selected-executable-path'
            } else {
                $state='different-path';$evidence='readable-nonmatching-app-candidate'
                $known = @($Selection.Metadata | Where-Object { $processPath.StartsWith($_.InstallLocation+'\',[StringComparison]::OrdinalIgnoreCase) })
                if ($known.Count -eq 1) {
                    $observedVersion=$known[0].Version.ToString();$evidence='current-user-registration-path'
                } elseif ($processPath.StartsWith($storeRoot,[StringComparison]::OrdinalIgnoreCase)) {
                    $folder=$processPath.Substring($storeRoot.Length).Split('\')[0]
                    if ($folder -match '^OpenAI\.Codex_(?<v>\d+\.\d+\.\d+\.\d+)_(x86|x64|arm|arm64|x86a64|neutral)__(?<p>[a-z0-9]{13})$' -and
                        ('OpenAI.Codex_'+$Matches.p) -ieq $selected.PackageFamilyName) {
                        $observedVersion=(ConvertTo-GhcPackageVersion $Matches.v).ToString()
                        $evidence='package-directory-name-only'
                    }
                }
                if ($null -ne $observedVersion) {
                    $comparison=(ConvertTo-GhcPackageVersion $observedVersion).CompareTo($selectedVersion)
                    $state=if($comparison -lt 0){'older-package-running'}elseif($comparison -gt 0){'newer-package-running'}else{'same-version-different-path'}
                }
            }
        } catch { $state='unknown';$evidence='unreadable-or-invalid-path' }
        $entries.Add([pscustomobject]@{Id=$processId;Path=$processPath;State=$state;VersionFromEvidence=$observedVersion;Evidence=$evidence})
    }
    $states=@($entries.State)
    $summary=if($entries.Count -eq 0){'absent'}elseif($states -contains 'unknown'){'unknown'}elseif($states -contains 'older-package-running'){'older-package-running'}elseif($states -contains 'newer-package-running'){'newer-package-running'}elseif($states -contains 'different-path' -or $states -contains 'same-version-different-path'){'different-path'}else{'current-running'}
    return [pscustomobject]@{State=$summary;CanLaunch=($entries.Count -eq 0);Entries=$entries.ToArray();LoadedPackageIdentityVerified=$false;ActionPerformed=$false}
}

