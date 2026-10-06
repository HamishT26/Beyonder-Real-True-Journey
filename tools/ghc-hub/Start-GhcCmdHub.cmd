@echo off
setlocal DisableDelayedExpansion
title GHC Nexus Hub - Command Prompt
set "GHC_HUB_WORKSPACE=D:\GHC-Family-Laboratory"
set "GHC_HUB_HOME=D:\GHC-Archives\phase-banks\ghc-hub"
cd /d "D:\GHC-Family-Laboratory"
if errorlevel 1 exit /b 1
"D:\GHC-Archives\global-tools\node\26.10.0\node-v26.10.0-win-x64\node.exe" "%~dp0hub.mjs" menu
set "GHC_HUB_EXIT=%errorlevel%"
echo.
echo Hub closed. Use ghc-nexus menu to open it again in this terminal.
exit /b %GHC_HUB_EXIT%
