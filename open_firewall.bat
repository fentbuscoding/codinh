@echo off
echo Opening Firewall Port for Flask Application
echo This requires administrator privileges
echo.

REM Check for admin privileges
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Please run this script as an Administrator.
    echo Right-click the script and select "Run as administrator"
    pause
    exit /B 1
)

echo Adding Firewall rule for Flask on port 5000...
netsh advfirewall firewall add rule name="Flask Web App" dir=in action=allow protocol=TCP localport=5000
echo.
echo Done! Flask should now be accessible from other computers on your network.
echo.
pause