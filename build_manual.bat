@echo off
setlocal EnableDelayedExpansion

set "JAVA25_HOME=C:\PROGRA~1\Java\jdk-25.0.2"
set "JAVA_EXE=java"
set "JAVAC_EXE=javac"
set "JAR_EXE=jar"
if exist "%JAVA25_HOME%\bin\java.exe" (
    set "JAVA_HOME=%JAVA25_HOME%"
    set "JAVA_EXE=%JAVA25_HOME%\bin\java.exe"
)
if exist "%JAVA25_HOME%\bin\javac.exe" (
    set "JAVAC_EXE=%JAVA25_HOME%\bin\javac.exe"
)
if exist "%JAVA25_HOME%\bin\jar.exe" (
    set "JAR_EXE=%JAVA25_HOME%\bin\jar.exe"
)

set "BUILD_DIR=build\\classes"
set "DIST_DIR=dist"
set "SRC_LIST=build\\sources.txt"
set "APP_JAR=%DIST_DIR%\\JMSv186.jar"

if exist build rmdir /s /q build
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"

mkdir build
mkdir "%BUILD_DIR%"
mkdir "%DIST_DIR%"

> "%SRC_LIST%" (
    for /r src %%f in (*.java) do echo %%f
)

set "CP="
for %%f in (lib\*.jar) do (
    if defined CP (
        set "CP=!CP!;%%~ff"
    ) else (
        set "CP=%%~ff"
    )
)

"%JAVA_EXE%" -version
"%JAVAC_EXE%" -version
"%JAVAC_EXE%" -encoding UTF-8 -cp "!CP!" -d "%BUILD_DIR%" @"%SRC_LIST%"
if errorlevel 1 (
    echo Build failed during javac.
    exit /b 1
)

"%JAR_EXE%" --create --file "%APP_JAR%" -C "%BUILD_DIR%" .
if errorlevel 1 (
    echo Build failed during jar packaging.
    exit /b 1
)

copy /y lib\*.jar "%DIST_DIR%\" >nul
if errorlevel 1 (
    echo Build failed while copying dependencies.
    exit /b 1
)

echo Build complete.
echo Output: %APP_JAR%
