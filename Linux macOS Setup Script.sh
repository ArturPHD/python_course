#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
VENV_NAME=".venv"
REQUIRED_PYTHON_VERSION="3.11"

echo "============================================"
echo "   Python Course Environment Setup (Linux/macOS)"
echo "============================================"
echo "This script will create a virtual environment and install all required packages."

# --- Step 1: Verify Python Version ---
echo
echo "[1/3] Verifying Python version..."
# Check if python3.11 is available
if ! command -v python${REQUIRED_PYTHON_VERSION} &> /dev/null
then
    echo "ERROR: python${REQUIRED_PYTHON_VERSION} could not be found."
    echo "Please ensure Python ${REQUIRED_PYTHON_VERSION} is installed and available in your PATH."
    echo "You can download it from: https://www.python.org/downloads/"
    exit 1
fi
echo "Found Python ${REQUIRED_PYTHON_VERSION}."

# --- Step 2: Setup Virtual Environment ---
echo
echo "[2/3] Setting up virtual environment..."
if [ ! -d "$VENV_NAME" ]; then
    echo "Creating virtual environment '$VENV_NAME'..."
    python${REQUIRED_PYTHON_VERSION} -m venv $VENV_NAME
else
    echo "Virtual environment '$VENV_NAME' already exists."
fi

# --- Step 3: Install Dependencies ---
echo
echo "[3/3] Activating environment and installing dependencies..."
source "${VENV_NAME}/bin/activate"

echo "Installing PyTorch with CUDA 12.1 support..."
# Use a timeout to prevent it from hanging, and add error handling
if pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121; then
    echo "PyTorch with CUDA support installed successfully."
else
    echo "WARNING: Failed to install PyTorch with CUDA support."
    echo "This might be because you don't have an NVIDIA GPU or the correct drivers."
    echo "Installing the CPU-only version of PyTorch instead..."
    pip install torch torchvision torchaudio
fi


echo "Installing remaining dependencies from requirements.txt..."
pip install -r requirements.txt

echo
echo "============================================"
echo "     ✅ Setup Complete!"
echo "============================================"
echo
echo "You can now open this folder in VS Code or PyCharm."
echo "Activate the environment anytime with: source ${VENV_NAME}/bin/activate"
