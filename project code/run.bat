@echo off
echo ====================================================
echo   Starting ChronoChef Application...
echo ====================================================

set JAVA_CMD=java

where java >nul 2>nul
if %errorlevel% neq 0 (
    if exist "C:\Program Files\Android\Android Studio\jbr\bin\java.exe" (
        set "JAVA_CMD=C:\Program Files\Android\Android Studio\jbr\bin\java.exe"
    ) else (
        echo Error: java not found on PATH or in Android Studio JBR.
        pause
        exit /b 1
    )
) else (
    REM If default java is JRE 8 and fails with new class format, fallback to JBR OpenJDK
    if exist "C:\Program Files\Android\Android Studio\jbr\bin\java.exe" (
        set "JAVA_CMD=C:\Program Files\Android\Android Studio\jbr\bin\java.exe"
    )
)

"%JAVA_CMD%" -cp "lib/*;bin" Main

if %errorlevel% neq 0 (
    echo.
    echo Program exited with error code %errorlevel%
    pause
)
