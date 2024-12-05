#!/bin/bash

# Exit on any error
set -e

# Constants
ENV_NAME="artifact_env"
SCRIPT_NAME="artifact_ctl.py"
EXECUTABLE_NAME="artifact-ctl"
OUTPUT_DIR="dist"

# Detect OS
OS=$(uname | tr '[:upper:]' '[:lower:]')
IS_WINDOWS=0

if [[ "$OS" == "mingw"* || "$OS" == "cygwin"* ]]; then
    IS_WINDOWS=1
fi

# Notify the user
echo "Detected OS: $OS"
if [[ "$IS_WINDOWS" -eq 1 ]]; then
    echo "Building for Windows..."
else
    echo "Building for $OS..."
fi

# Step 1: Create and activate a virtual environment
echo "Setting up virtual environment..."
python3 -m venv $ENV_NAME
source $ENV_NAME/bin/activate

# Step 2: Install required dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install pyinstaller click requests

# Step 3: Build the executable
echo "Building the standalone executable..."
if [[ "$IS_WINDOWS" -eq 1 ]]; then
    pyinstaller --onefile --name $EXECUTABLE_NAME $SCRIPT_NAME
else
    pyinstaller --onefile --name $EXECUTABLE_NAME $SCRIPT_NAME
fi

# Step 4: Handle cross-platform extensions
if [[ "$IS_WINDOWS" -eq 1 ]]; then
    EXT=".exe"
else
    EXT=""
fi

# Ensure output filename consistency
mv "$OUTPUT_DIR/$EXECUTABLE_NAME$EXT" "$OUTPUT_DIR/$EXECUTABLE_NAME$EXT"

# Step 5: Add metadata or compress the output
echo "Preparing the final executable..."
if [[ "$IS_WINDOWS" -eq 1 ]]; then
    # Compress the executable for Windows distribution
    zip "$OUTPUT_DIR/$EXECUTABLE_NAME.zip" "$OUTPUT_DIR/$EXECUTABLE_NAME$EXT"
    echo "Compressed executable available at $OUTPUT_DIR/$EXECUTABLE_NAME.zip"
else
    # Optionally compress for macOS/Linux
    tar -czvf "$OUTPUT_DIR/$EXECUTABLE_NAME.tar.gz" -C "$OUTPUT_DIR" "$EXECUTABLE_NAME$EXT"
    echo "Compressed executable available at $OUTPUT_DIR/$EXECUTABLE_NAME.tar.gz"
fi

# Step 6: Cleanup virtual environment
echo "Cleaning up..."
deactivate
rm -rf $ENV_NAME

# Notify user of successful build
echo "Build complete. Executable is in the $OUTPUT_DIR/ folder."
