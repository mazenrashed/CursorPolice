#!/bin/bash

# Uninstallation script for Cursor Java Killer

set -e

PLIST_NAME="com.cursor.javakiller.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_PATH="$LAUNCH_AGENTS_DIR/$PLIST_NAME"

echo "Uninstalling Cursor Java Killer..."

# Stop and unload the service
if [ -f "$PLIST_PATH" ]; then
    echo "Stopping service..."
    launchctl stop com.cursor.javakiller 2>/dev/null || true
    
    echo "Unloading service..."
    launchctl unload "$PLIST_PATH" 2>/dev/null || true
    
    echo "Removing plist file..."
    rm "$PLIST_PATH"
else
    echo "Service plist not found at $PLIST_PATH"
fi

echo ""
echo "Uninstallation complete!"
echo ""
echo "Note: Log files are preserved at ~/Library/Logs/cursor_java_killer*.log"
echo "To remove logs: rm ~/Library/Logs/cursor_java_killer*.log"
