@echo off
setlocal

set "MSBUILD=C:\BuildTools\MSBuild\Current\Bin\MSBuild.exe"
set "ROOT=%~dp0"
set "TOOLS_ROOT=%ROOT%tools\tools"
set "RIREPE_ROOT=%ROOT%tools\RirePE"
set "SDK_VER=10.0.26100.0"

title Build RirePE x86

if not exist "%MSBUILD%" (
    echo [ERROR] MSBuild not found:
    echo         %MSBUILD%
    echo.
    pause
    exit /b 1
)

echo ==========================================
echo Build RirePE x86
echo ==========================================
echo.

echo [1/5] Building Riremito Simple...
"%MSBUILD%" "%TOOLS_ROOT%\Simple\Simple.sln" /m /p:Configuration=Release /p:Platform=x86 /p:WindowsTargetPlatformVersion=%SDK_VER%
if errorlevel 1 goto :fail

echo.
echo [2/5] Building Riremito Hook...
"%MSBUILD%" "%TOOLS_ROOT%\Hook\Hook.sln" /m /p:Configuration=Release /p:Platform=x86 /p:WindowsTargetPlatformVersion=%SDK_VER%
if errorlevel 1 goto :fail

echo.
echo [3/5] Consolidating Share libraries...
pushd "%TOOLS_ROOT%"
call CopyLib.bat
if errorlevel 1 (
    popd
    goto :fail
)
popd

echo.
echo [4/5] Copying Share libraries into RirePE...
pushd "%RIREPE_ROOT%"
call GetLib.bat
if errorlevel 1 (
    popd
    goto :fail
)
popd

echo.
echo [5/5] Building RirePE x86 runtime...
"%MSBUILD%" "%RIREPE_ROOT%\RirePE.sln" /m /p:Configuration=Release /p:Platform=x86 /p:WindowsTargetPlatformVersion=%SDK_VER%
if errorlevel 1 goto :fail

echo.
echo [DONE] RirePE x86 build completed.
echo [INFO] Runtime files:
echo        %RIREPE_ROOT%\Release\RirePE.exe
echo        %RIREPE_ROOT%\Release\Packet.dll
echo.
pause
exit /b 0

:fail
echo.
echo [ERROR] Build failed.
echo.
pause
exit /b 1
