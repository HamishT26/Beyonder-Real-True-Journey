@echo off
rem GHC Nexus managed command: bounded read-only skill library
"D:\GHC-Archives\global-tools\node\26.11.1\node-v26.11.1-win-x64\node.exe" "D:\GHC-Archives\global-tools\ghc-nexus-hub\skill-library.mjs" %*
exit /b %errorlevel%
