#!/bin/bash

# Installation script for Cursor Java Killer

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_NAME="com.cursor.javakiller.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_PATH="$LAUNCH_AGENTS_DIR/$PLIST_NAME"

echo "Installing Cursor Java Killer..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"

# Create Scripts directory if it doesn't exist
SCRIPTS_DIR="$HOME/Library/Scripts"
mkdir -p "$SCRIPTS_DIR"

# Copy script to Scripts directory
echo "Copying script to $SCRIPTS_DIR..."
cp "$SCRIPT_DIR/cursor_java_killer.py" "$SCRIPTS_DIR/"
chmod +x "$SCRIPTS_DIR/cursor_java_killer.py"

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCH_AGENTS_DIR"

# Copy plist file
echo "Installing launch agent..."
cp "$SCRIPT_DIR/$PLIST_NAME" "$PLIST_PATH"

# Update plist with actual script path (use ~/Library/Scripts)
sed -i '' "s|/Users/mazen/Library/Scripts|$SCRIPTS_DIR|g" "$PLIST_PATH"
sed -i '' "s|/Users/mazen|$HOME|g" "$PLIST_PATH"

# Unload if already loaded
if launchctl list | grep -q "com.cursor.javakiller"; then
    echo "Unloading existing service..."
    launchctl unload "$PLIST_PATH" 2>/dev/null || true
fi

# Load the service
echo "Loading service..."
launchctl load "$PLIST_PATH"

# Start the service
echo "Starting service..."
launchctl start com.cursor.javakiller

echo ""
echo "Installation complete!"
echo ""
echo "The service is now running. It will automatically start on login."
echo ""
echo "To check status: launchctl list | grep cursor.javakiller"
echo "To view logs: tail -f ~/Library/Logs/cursor_java_killer.log"
echo "To stop: launchctl stop com.cursor.javakiller"
echo "To uninstall: launchctl unload $PLIST_PATH && rm $PLIST_PATH"
