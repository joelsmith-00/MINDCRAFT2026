@echo off
echo ========================================
echo Building Dot Dev Club APK
echo ========================================
echo.

REM Set JAVA_HOME for this session
set JAVA_HOME=C:\Program Files\Android\Android Studio\jbr
set PATH=%JAVA_HOME%\bin;%PATH%

echo JAVA_HOME set to: %JAVA_HOME%
echo.

echo Cleaning previous build...
call flutter clean
echo.

echo Getting dependencies...
call flutter pub get
echo.

echo Building APK (this will take 5-10 minutes)...
echo Please wait...
call flutter build apk --debug
echo.

if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo SUCCESS! APK built successfully!
    echo ========================================
    echo.
    echo APK Location:
    echo %CD%\build\app\outputs\flutter-apk\app-debug.apk
    echo.
    echo File size:
    dir build\app\outputs\flutter-apk\app-debug.apk | find "app-debug.apk"
    echo.
    echo You can now install this APK on your Android device!
    echo.
    pause
) else (
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo.
    echo Please check the error messages above.
    echo.
    echo Common fixes:
    echo 1. Make sure Android Studio is installed
    echo 2. Run: flutter doctor
    echo 3. Check TROUBLESHOOT_BUILD.md
    echo.
    pause
)
