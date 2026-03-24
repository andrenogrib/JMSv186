@echo off
set "MYSQL_EXE=C:\wamp64\bin\mysql\mysql8.4.7\bin\mysqld.exe"
set "MYSQL_LOG=C:\wamp64\logs\mysql-3306.log"

if not exist "%MYSQL_EXE%" (
    echo Wamp MySQL executable not found:
    echo %MYSQL_EXE%
    exit /b 1
)

powershell -NoProfile -Command "if (Get-NetTCPConnection -State Listen -LocalPort 3306 -ErrorAction SilentlyContinue) { Write-Host 'Wamp MySQL 8.4.7 is already listening on port 3306.'; exit 0 }"
if errorlevel 1 exit /b 1

start "wamp-mysql-3306" /min "%MYSQL_EXE%" --basedir=C:/wamp64/bin/mysql/mysql8.4.7 --datadir=C:/wamp64/bin/mysql/mysql8.4.7/data --port=3306 --mysqlx=0 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --default-storage-engine=MYISAM --skip-log-bin --require_secure_transport=OFF --explicit_defaults_for_timestamp=TRUE --sql_mode= --log-error=%MYSQL_LOG%

timeout /t 5 /nobreak >nul
powershell -NoProfile -Command "Get-NetTCPConnection -State Listen -LocalPort 3306 -ErrorAction SilentlyContinue | Select-Object LocalAddress, LocalPort, OwningProcess | Format-Table -AutoSize"
