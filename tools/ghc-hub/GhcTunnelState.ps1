function Get-GhcTunnelOutcome {
 param([object]$Snapshot,[string]$Action='Status',[object]$ConnectExitCode=$null)
 $running=$Snapshot.process_running -eq $true
 $ready=$Snapshot.ready -eq $true -and $Snapshot.healthy -eq $true -and $running
 $state=if($ready){'ready'}elseif($running){'starting_or_unhealthy'}else{'stopped'}
 $result=if($Action -eq 'Connect' -and $ready -and $null -ne $ConnectExitCode -and $ConnectExitCode -ne 0){'vendor_error_but_runtime_ready'}elseif($Action -eq 'Connect' -and -not $ready -and $running){'connect_pending_do_not_repeat'}else{$state}
 $exitCode=if($Action -ne 'Connect' -or $ready){0}elseif($running){2}else{1}
 [ordered]@{alias='ghc-nexus';action=$Action;state=$state;result=$result;healthy=$Snapshot.healthy -eq $true;ready=$ready;process_running=$running;runtime_state=$Snapshot.runtime_state;profile_exists=$Snapshot.profile_exists -eq $true;connectExitCode=$ConnectExitCode;exitCode=$exitCode}
}
