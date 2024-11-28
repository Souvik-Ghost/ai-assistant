#!/bin/bash

echo "Starting AI Assistant Build Process for Android..."
echo

# Check Python installation
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed"
    echo "Please install Python using: pkg install python"
    exit 1
fi

# Check pip installation
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed"
    echo "Please install pip using: pkg install python-pip"
    exit 1
fi

echo "Checking and creating virtual environment..."
echo

# Create and activate virtual environment
if [ -d "venv" ]; then
    echo "Found existing virtual environment"
else
    echo "Creating new virtual environment..."
    python -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
fi

echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

echo "Installing/Updating dependencies..."
echo
python -m pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "Setting up X11 environment..."
echo

# Install X11 dependencies if not present
if ! command -v vncserver &> /dev/null; then
    echo "Installing VNC server..."
    pkg install x11-repo
    pkg install tigervnc
fi

# Start VNC server if not running
vncserver -list | grep "^:" > /dev/null
if [ $? -ne 0 ]; then
    echo "Starting VNC server..."
    vncserver
fi

echo
echo "Build process completed!"
echo "To run the application:"
echo "1. Start VNC viewer on your Android device"
echo "2. Connect to localhost:1"
echo "3. Run: python -m ai_assistant.main"
echo
