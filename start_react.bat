@echo off
echo Starting NeuroTrade FGI Dashboard...
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo.
echo Starting React development server...
echo The dashboard will open at http://localhost:3000
echo.
echo Make sure the Flask backend is running on http://localhost:5000
echo.

call npm start

pause

