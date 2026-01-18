#!/usr/bin/env python3
"""
Cursor Java Process Killer
Monitors processes and kills Java processes spawned by Cursor.
"""

import psutil
import time
import sys
import logging
import os
from pathlib import Path

# Setup logging
LOG_FILE = Path.home() / "Library" / "Logs" / "cursor_java_killer.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def get_cursor_process_groups():
    """Get all process group IDs belonging to Cursor processes."""
    cursor_pgids = set()
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'cursor' in proc.info['name'].lower():
                    try:
                        pgid = os.getpgid(proc.info['pid'])
                        cursor_pgids.add(pgid)
                    except (OSError, AttributeError):
                        pass
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception:
        pass
    return cursor_pgids

def is_cursor_process(process, cursor_pgids):
    """Check if a process is Cursor or spawned by Cursor."""
    try:
        # Check if the process itself is Cursor
        if 'cursor' in process.name().lower():
            return True
        
        # Check if process group matches Cursor's process group
        try:
            pgid = os.getpgid(process.pid)
            if pgid in cursor_pgids:
                return True
        except (OSError, AttributeError):
            pass
        
        # Check parent processes
        try:
            parent = process.parent()
            if parent:
                # Check if parent is Cursor
                if 'cursor' in parent.name().lower():
                    return True
                
                # Check parent's process group
                try:
                    parent_pgid = os.getpgid(parent.pid)
                    if parent_pgid in cursor_pgids:
                        return True
                except (OSError, AttributeError):
                    pass
                
                # Check grandparent and further up the chain
                while parent:
                    if 'cursor' in parent.name().lower():
                        return True
                    try:
                        parent = parent.parent()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break
        except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
            # Parent might be null or already terminated - process group check above handles this
            pass
    except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
        pass
    return False

def kill_java_from_cursor():
    """Find and kill Java processes spawned by Cursor."""
    killed_count = 0
    
    # Get Cursor process groups once per scan
    cursor_pgids = get_cursor_process_groups()
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'ppid']):
            try:
                process_name = proc.info['name'].lower()
                
                # Check if it's a Java process
                if 'java' in process_name:
                    # Get executable path
                    exe_path = ""
                    try:
                        exe_path = proc.exe()
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        pass
                    
                    # Get CPU usage
                    cpu_percent = 0.0
                    try:
                        cpu_percent = proc.cpu_percent(interval=0.1)
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        pass
                    
                    # Get process group info
                    pgid = None
                    try:
                        pgid = os.getpgid(proc.info['pid'])
                    except (OSError, AttributeError):
                        pass
                    
                    # Check if executable path is a Java executable (more flexible check)
                    is_java_executable = (
                        exe_path == "/usr/bin/java" or 
                        exe_path.endswith("/java") or
                        "/java" in exe_path.lower() or
                        "java" in exe_path.lower()
                    )
                    
                    # Check if CPU usage is high (over 300% means using more than 3 cores)
                    high_cpu = cpu_percent > 300.0
                    
                    # Check if it's spawned by Cursor (process group or parent chain)
                    is_from_cursor = is_cursor_process(proc, cursor_pgids)
                    
                    # Log process details for debugging
                    logger.debug(f"Java process {proc.info['pid']}: exe={exe_path}, cpu={cpu_percent}%, pgid={pgid}, from_cursor={is_from_cursor}")
                    
                    # Kill if: it's from Cursor AND (it's a Java executable OR has high CPU usage)
                    if is_from_cursor and (is_java_executable or high_cpu):
                        logger.info(f"Found Java process {proc.info['pid']} ({proc.info['name']}) from Cursor. "
                                  f"exe={exe_path}, cpu={cpu_percent}%, pgid={pgid}. Killing...")
                        try:
                            proc.kill()
                            killed_count += 1
                            logger.info(f"Successfully killed process {proc.info['pid']}")
                        except psutil.AccessDenied:
                            logger.warning(f"Permission denied: Cannot kill process {proc.info['pid']}. Try running with sudo.")
                        except psutil.NoSuchProcess:
                            logger.debug(f"Process {proc.info['pid']} already terminated")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Process may have terminated between iterations
                continue
    except Exception as e:
        logger.error(f"Error while scanning processes: {e}", exc_info=True)
    
    return killed_count

def main():
    """Main monitoring loop."""
    logger.info("Cursor Java Killer started. Monitoring for Java processes from Cursor...")
    
    # Check interval in seconds
    CHECK_INTERVAL = 2
    
    try:
        while True:
            killed = kill_java_from_cursor()
            if killed > 0:
                logger.info(f"Killed {killed} Java process(es) from Cursor")
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal. Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
