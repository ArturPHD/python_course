@echo off
setlocal

:: --- Configuration ---
set VENV_NAME=.venv
set REQUIRED_PYTHON_VERSION=3.11

echo ============================================
echo      Python Course Environment Setup
echo ============================================
echo This script will create a virtual environment and install all required packages.

:: --- Step 1: Verify Python Version ---
echo.
echo [1/3] Verifying Python version...

:: Check if py.exe (Python Launcher for Windows) exists
where py >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python Launcher 'py.exe' not found.
    echo Please install Python %REQUIRED_PYTHON_VERSION% from python.org and ensure the launcher is added to your PATH.
    echo Link: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Found Python launcher.

:: --- Step 2: Setup Virtual Environment ---
echo.
echo [2/3] Setting up virtual environment...
if not exist "%VENV_NAME%\" (
    echo Creating virtual environment '%VENV_NAME%'...
    py -%REQUIRED_PYTHON_VERSION% -m venv %VENV_NAME%
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment. Make sure Python %REQUIRED_PYTHON_VERSION% is installed.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment '%VENV_NAME%' already exists.
)

:: --- Step 3: Install Dependencies ---
echo.
echo [3/3] Activating environment and installing dependencies...
call "%VENV_NAME%\Scripts\activate.bat"

echo Installing PyTorch with CUDA 12.1 support...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
if %errorlevel% neq 0 (
    echo WARNING: Failed to install PyTorch with CUDA support.
    echo This might be because you don't have an NVIDIA GPU or the correct drivers.
    echo Installing the CPU-only version of PyTorch instead...
    pip install torch torchvision torchaudio
)

echo Installing remaining dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies from requirements.txt.
    pause
    exit /b 1
)

echo.
echo ============================================
echo      (V) Setup Complete!
echo ============================================
echo.
echo You can now open this folder in VS Code or PyCharm.
echo Make sure to select the '.venv' folder as your Python interpreter.
echo.
pause
endlocal
