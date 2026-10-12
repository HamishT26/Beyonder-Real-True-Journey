@echo off
rem GHC Nexus managed command: official OpenAI REST CLI; credentials are caller-managed
"D:\GHC-Archives\global-tools\openai-rest-cli\1.38.0\openai.exe" %*
exit /b %errorlevel%
