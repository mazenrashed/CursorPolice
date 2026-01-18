# Cursor Java Process Killer

A macOS background service that monitors processes and automatically kills Java processes spawned by Cursor.

## Features

- Monitors processes every 2 seconds
- Automatically detects Java processes spawned by Cursor
- Runs as a background service using launchd
- Logs all activities to `~/Library/Logs/cursor_java_killer.log`

## Installation

1. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Make the script executable:**
   ```bash
   chmod +x cursor_java_killer.py
   ```

3. **Update the plist file** with your actual username if needed:
   - Open `com.cursor.javakiller.plist`
   - Replace `/Users/mazen/` with your actual home directory path if different

4. **Install the launch agent:**
   ```bash
   cp com.cursor.javakiller.plist ~/Library/LaunchAgents/
   ```

5. **Load the service:**
   ```bash
   launchctl load ~/Library/LaunchAgents/com.cursor.javakiller.plist
   ```

6. **Start the service:**
   ```bash
   launchctl start com.cursor.javakiller
   ```

## Usage

Once installed, the service will automatically:
- Start when you log in
- Run in the background
- Monitor and kill Java processes from Cursor

## Management Commands

**Check if service is running:**
```bash
launchctl list | grep cursor.javakiller
```

**Stop the service:**
```bash
launchctl stop com.cursor.javakiller
```

**Unload the service:**
```bash
launchctl unload ~/Library/LaunchAgents/com.cursor.javakiller.plist
```

**View logs:**
```bash
tail -f ~/Library/Logs/cursor_java_killer.log
```

**View error logs:**
```bash
tail -f ~/Library/Logs/cursor_java_killer.err.log
```

## Uninstallation

1. **Stop and unload the service:**
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.cursor.javakiller.plist
   ```

2. **Remove the plist file:**
   ```bash
   rm ~/Library/LaunchAgents/com.cursor.javakiller.plist
   ```

3. **Remove log files (optional):**
   ```bash
   rm ~/Library/Logs/cursor_java_killer*.log
   ```

## Troubleshooting

- If the service doesn't start, check the error log: `~/Library/Logs/cursor_java_killer.err.log`
- Make sure Python 3 is installed: `python3 --version`
- Make sure psutil is installed: `pip3 show psutil`
- Check file permissions: The script should be executable (`chmod +x cursor_java_killer.py`)
