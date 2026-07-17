@echo off
REM ===================================================================
REM  Claude Video Analyzer - Web Application Startup Script
REM  For Eli Lilly Organization
REM ===================================================================

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║        Claude Video Analyzer - Web Application                ║
echo ║        Eli Lilly Enterprise Edition                           ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [✓] Python found
echo.

REM Check if .env file exists
if not exist .env (
    echo [WARNING] .env file not found
    echo.
    echo Creating .env from template...
    copy .env.example .env >nul
    echo.
    echo [!] IMPORTANT: Please edit .env file and add your ANTHROPIC_API_KEY
    echo.
    echo Opening .env file in notepad...
    start notepad .env
    echo.
    echo Press any key after you've added your API key...
    pause >nul
)

echo [✓] Configuration file found
echo.

REM Create necessary folders
if not exist templates mkdir templates
if not exist uploads mkdir uploads
if not exist output_frames mkdir output_frames

REM Copy index.html to templates if needed
if exist index.html (
    copy /Y index.html templates\index.html >nul 2>&1
)

echo [✓] Directory structure ready
echo.

REM Check if virtual environment exists
if not exist venv (
    echo [!] Virtual environment not found
    echo Creating virtual environment...
    python -m venv venv
    echo [✓] Virtual environment created
    echo.
)

REM Activate virtual environment and install dependencies
echo [*] Activating virtual environment...
call venv\Scripts\activate

echo [*] Checking dependencies...
pip install --quiet -r requirements.txt 2>nul
if errorlevel 1 (
    echo [!] Installing dependencies... (this may take a minute)
    pip install -r requirements.txt
)

echo [✓] Dependencies ready
echo.

echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║  Starting Web Server...                                        ║
echo ║                                                                ║
echo ║  Access the application at:                                    ║
echo ║  • Local:   http://localhost:5000                              ║
echo ║  • Network: http://YOUR_IP:5000                                ║
echo ║                                                                ║
echo ║  Press Ctrl+C to stop the server                               ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Get local IP address
echo [*] Your IP addresses:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do echo     http://%%a:5000

echo.
echo [*] Starting Flask server...
echo.

REM Start Flask application
python app.py

REM This will only run when server is stopped
echo.
echo [*] Server stopped
pause
