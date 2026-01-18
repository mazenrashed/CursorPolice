#!/bin/bash

# Status check script for Cursor Java Killer

echo "Checking Cursor Java Killer status..."
echo ""

# Method 1: Check launchctl
echo "=== Launch Agent Status ==="
if launchctl list | grep -q "cursor.javakiller"; then
    echo "✓ Service is loaded"
    launchctl list | grep cursor.javakiller
else
    echo "✗ Service is not loaded"
fi

echo ""
echo "=== Process Status ==="
# Method 2: Check if Python process is running
if pgrep -f "cursor_java_killer.py" > /dev/null; then
    echo "✓ Python script is running"
    ps aux | grep "[c]ursor_java_killer.py"
else
    echo "✗ Python script is not running"
fi

echo ""
echo "=== Log Files ==="
LOG_FILE="$HOME/Library/Logs/cursor_java_killer.log"
if [ -f "$LOG_FILE" ]; then
    echo "✓ Log file exists: $LOG_FILE"
    echo "Last 5 log entries:"
    tail -n 5 "$LOG_FILE" 2>/dev/null || echo "  (log file is empty)"
else
    echo "✗ Log file not found (service may not have run yet)"
fi

echo ""
echo "=== Quick Commands ==="
echo "To view live logs: tail -f ~/Library/Logs/cursor_java_killer.log"
echo "To start service: launchctl start com.cursor.javakiller"
echo "To stop service: launchctl stop com.cursor.javakiller"
