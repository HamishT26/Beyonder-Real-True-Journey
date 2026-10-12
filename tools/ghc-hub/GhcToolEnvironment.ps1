# Definitions only. Apply to a GHC process; machine-wide PATH is not changed.
function Get-GhcPreferredToolPath {
    param(
        [string]$CurrentPath = $env:PATH,
        [ValidateSet('pwsh','node','git','gh')][string[]]$RequiredTools = @(),
        [object[]]$Choices = @()
    )
    $ghcChoices = if($Choices.Count){$Choices}else{@(
        @{name='pwsh'; directory='D:\GHC-Archives\global-tools\powershell\7.6.6'; executable='pwsh.exe'; match='^(D:/GHC-Archives/global-tools/powershell/|C:/Program Files/PowerShell/7$)'},
        @{name='node'; directory='D:\GHC-Archives\global-tools\node\26.11.1\node-v26.11.1-win-x64'; executable='node.exe'; match='^(D:/GHC-Archives/global-tools/node/|C:/Program Files/nodejs$)'},
        @{name='git'; directory='D:\GHC-Archives\global-tools\git\2.56.0.2\cmd'; executable='git.exe'; match='^(D:/GHC-Archives/global-tools/git/.*/cmd$|C:/Program Files/Git/cmd$)'},
        @{name='gh'; directory='D:\GHC-Archives\global-tools\gh\2.102.0\bin'; executable='gh.exe'; match='^(D:/GHC-Archives/global-tools/gh/.*/bin$|C:/Program Files/GitHub CLI$)'}
    )}
    $ghcAvailable=@()
    foreach($ghcChoice in $ghcChoices){
        if(Test-Path -LiteralPath (Join-Path $ghcChoice.directory $ghcChoice.executable) -PathType Leaf){$ghcAvailable+=,$ghcChoice}
    }
    foreach($ghcRequired in $RequiredTools){
        if(-not @($ghcAvailable | Where-Object {$_.name -eq $ghcRequired}).Count){throw ('Required tool missing: '+$ghcRequired)}
    }
    $ghcResult=[Collections.Generic.List[string]]::new()
    # A deterministic prefix wins over earlier shims. Missing optional tools do
    # not remove working fallback entries or block unrelated recovery actions.
    foreach($ghcChoice in $ghcAvailable){$ghcResult.Add($ghcChoice.directory)}
    foreach($ghcEntry in ($CurrentPath -split ';')){
        if([string]::IsNullOrWhiteSpace($ghcEntry)){continue}
        $ghcNormalized=$ghcEntry.Trim().Trim('"').TrimEnd([char[]]@('\','/')).Replace('\','/')
        $ghcManaged=@($ghcAvailable | Where-Object {
            $ghcNormalized -match $_.match -or $ghcNormalized -eq $_.directory.Replace('\','/').TrimEnd('/')
        })
        if(-not $ghcManaged.Count){$ghcResult.Add($ghcEntry)}
    }
    return ($ghcResult -join ';')
}
