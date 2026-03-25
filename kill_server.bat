@echo off
setlocal
cd /d "%~dp0"

echo Searching for JMSv186 server processes...

powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference = 'SilentlyContinue'; " ^
  "$root = [regex]::Escape((Resolve-Path '.').Path); " ^
  "$selfPid = $PID; " ^
  "$targets = Get-CimInstance Win32_Process | Where-Object { " ^
    "($_.ProcessId -ne $selfPid) -and " ^
    "(-not ($_.CommandLine -match 'kill_server\.bat')) -and " ^
    "(" ^
      "(($_.Name -eq 'java.exe') -and ($_.CommandLine -match 'tacos\.Start')) -or " ^
      "(($_.Name -eq 'cmd.exe') -and ($_.CommandLine -match $root) -and (($_.CommandLine -match 'run_any\.bat') -or ($_.CommandLine -match 'packet_trace_live\.bat') -or ($_.CommandLine -match 'run_[A-Z]+_v[0-9.]+\.bat'))) -or " ^
      "(($_.Name -eq 'powershell.exe') -and ((($_.CommandLine -match 'Invoke-LiveLogCommand') -and ($_.CommandLine -match 'tacos\.Start')) -or ($_.CommandLine -match 'PACKET_TRACE_FILE'))) " ^
    ")" ^
  "}; " ^
  "if (-not $targets) { " ^
    "Write-Host 'No server processes found.'; " ^
    "exit 0; " ^
  "} " ^
  "Write-Host 'Found processes:'; " ^
  "$targets | Select-Object ProcessId, Name, CommandLine | Format-Table -AutoSize; " ^
  "$ids = @($targets | Select-Object -ExpandProperty ProcessId); " ^
  "Stop-Process -Id $ids -Force -ErrorAction SilentlyContinue; " ^
  "Start-Sleep -Seconds 2; " ^
  "Write-Host ''; " ^
  "Write-Host 'Ports after kill:'; " ^
  "$ports = Get-NetTCPConnection -State Listen -LocalPort 8484,8100,8101,8596,8597 -ErrorAction SilentlyContinue; " ^
  "if ($ports) { " ^
    "$ports | Select-Object LocalPort, OwningProcess | Sort-Object LocalPort | Format-Table -AutoSize; " ^
  "} else { " ^
    "Write-Host 'All server ports are free.'; " ^
  "}"

pause
endlocal
