@echo off
echo Starting AI Assistant Build Process...
echo.

REM Check Python installation
python --version > nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check pip installation
pip --version > nul 2>&1
if errorlevel 1 (
    echo Error: pip is not installed
    echo Please install pip or fix your Python installation
    pause
    exit /b 1
)

echo Checking and creating virtual environment...
echo.

REM Deactivate any active virtual environment
if defined VIRTUAL_ENV (
    call deactivate
)

REM Create and activate virtual environment
if exist venv\Scripts\activate.bat (
    echo Found existing virtual environment
) else (
    echo Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Installing/Updating dependencies...
echo.
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo Building executable...
echo.

REM Create resources directory if it doesn't exist
if not exist resources mkdir resources

REM Build executable with PyInstaller
pyinstaller --clean ^
    --name=ai_assistant ^
    --onefile ^
    --windowed ^
    --add-data "ai_assistant/modules;ai_assistant/modules" ^
    --hidden-import=cv2 ^
    --hidden-import=numpy ^
    --hidden-import=PyQt5 ^
    --hidden-import=sounddevice ^
    --hidden-import=psutil ^
    ai_assistant/main.py

if errorlevel 1 (
    echo Error: Failed to build executable
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo The executable can be found in the dist folder
echo To run the application, double-click dist\ai_assistant.exe
echo.

REM Clean up build files
echo Cleaning up build files...
if exist build rmdir /s /q build
if exist ai_assistant.spec del ai_assistant.spec

echo.
echo Build process completed!
pause
