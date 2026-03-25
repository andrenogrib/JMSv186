@echo off
setlocal
cd /d "%~dp0"

if not exist log (
    mkdir log
)

if not exist log\PacketTrace.log (
    type nul > log\PacketTrace.log
)

echo ==========================================
echo BMS Packet Trace Live
echo File: log\PacketTrace.log
echo Press Ctrl+C to stop.
echo ==========================================

powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command "Get-Content -Path 'log\\PacketTrace.log' -Wait -Tail 120"
