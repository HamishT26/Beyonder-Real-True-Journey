@echo off
rem GHC Nexus managed command: official OSV-Scanner
"D:\GHC-Archives\global-tools\osv-scanner\2.7.0\osv-scanner.exe" %*
exit /b %errorlevel%
