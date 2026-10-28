@echo off
echo ====================================================
echo   Running ChronoChef Automated Verification Tests...
echo ====================================================

set JAVA_CMD=java

if exist "C:\Program Files\Android\Android Studio\jbr\bin\java.exe" (
    set "JAVA_CMD=C:\Program Files\Android\Android Studio\jbr\bin\java.exe"
)

"%JAVA_CMD%" -cp "lib/*;bin" test.ProjectTestRunner
pause
