@echo off
setlocal

set "ROOT=%~dp0"
set "CLIENT_EXE=%ROOT%..\BMS_v24\BMS_v24.0_L.exe"
set "RIREPE_BUILD=%ROOT%tools\RirePE\Release"
set "RIREPE_RUNTIME=%ROOT%tools\RirePE_runtime"
set "RIREPE_EXE=%RIREPE_BUILD%\RirePE.exe"
set "PACKET_DLL=%RIREPE_BUILD%\Packet.dll"

title BMS v24 Client Analysis Launcher

echo ==========================================
echo BMS v24 Client Analysis Launcher
echo ==========================================
echo.

if not exist "%CLIENT_EXE%" (
    echo [ERROR] Client not found:
    echo         %CLIENT_EXE%
    echo.
    pause
    exit /b 1
)

if not exist "%RIREPE_RUNTIME%" (
    mkdir "%RIREPE_RUNTIME%" >nul 2>nul
)

echo [INFO] Start the server first with run_BMS_v24.0.bat.
echo [INFO] This launcher will open the BMS client for local testing.
echo.

if not exist "%RIREPE_EXE%" (
    if exist "%RIREPE_RUNTIME%\RirePE.exe" (
        set "RIREPE_EXE=%RIREPE_RUNTIME%\RirePE.exe"
    )
)

if not exist "%PACKET_DLL%" (
    if exist "%RIREPE_RUNTIME%\Packet.dll" (
        set "PACKET_DLL=%RIREPE_RUNTIME%\Packet.dll"
    )
)

if exist "%RIREPE_EXE%" (
    echo [INFO] RirePE.exe found. Opening the UI helper.
    start "" "%RIREPE_EXE%"
) else (
    echo [WARN] RirePE.exe was not found in:
    echo        %RIREPE_BUILD%
    echo [WARN] Fallback runtime folder:
    echo        %RIREPE_RUNTIME%
)

if exist "%PACKET_DLL%" (
    echo [INFO] Packet.dll found in:
    echo        %PACKET_DLL%
) else (
    echo [WARN] Packet.dll was not found in:
    echo        %RIREPE_BUILD%
    echo [WARN] Fallback runtime folder:
    echo        %RIREPE_RUNTIME%
)

echo.
echo [INFO] Opening client:
echo        %CLIENT_EXE%
start "" "%CLIENT_EXE%"

echo.
echo [NOTE] This launcher opens the built RirePE UI and the client.
echo [NOTE] Packet.dll is now available from the local RirePE x86 build.
echo [NOTE] See tools\README_RirePE.md for the local build notes.
echo.
pause
