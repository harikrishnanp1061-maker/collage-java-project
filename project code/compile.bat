@echo off
echo ====================================================
echo   Compiling ChronoChef Java Project...
echo ====================================================

set JAVAC_CMD=javac

where javac >nul 2>nul
if %errorlevel% neq 0 (
    if exist "C:\Program Files\Android\Android Studio\jbr\bin\javac.exe" (
        set "JAVAC_CMD=C:\Program Files\Android\Android Studio\jbr\bin\javac.exe"
    ) else (
        echo Error: javac not found on PATH or in Android Studio JBR.
        pause
        exit /b 1
    )
)

if not exist "bin" mkdir "bin"

"%JAVAC_CMD%" -cp "lib/*;src" -d bin src/exception/*.java src/model/*.java src/database/*.java src/service/*.java src/ui/*.java src/test/*.java src/Main.java

if %errorlevel% equ 0 (
    echo ====================================================
    echo   BUILD SUCCESSFUL! All classes compiled to 'bin'
    echo ====================================================
) else (
    echo [ERROR] Compilation failed.
)
pause
