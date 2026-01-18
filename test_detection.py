#!/usr/bin/env python3
"""
Test script to verify Java process detection from Cursor
"""

import psutil
import sys

def get_cursor_process_groups():
    """Get all process group IDs belonging to Cursor processes."""
    cursor_pgids = set()
    cursor_pids = []
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'cursor' in proc.info['name'].lower():
                    try:
                        pgid = proc.pgid()
                        cursor_pgids.add(pgid)
                        cursor_pids.append((proc.info['pid'], pgid))
                    except (psutil.AccessDenied, AttributeError):
                        pass
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception:
        pass
    return cursor_pgids, cursor_pids

def check_java_processes():
    """Check all Java processes and see if they match our criteria."""
    cursor_pgids, cursor_pids = get_cursor_process_groups()
    
    print("=" * 80)
    print("Cursor Process Groups:")
    for pid, pgid in cursor_pids:
        print(f"  Cursor PID: {pid}, PGID: {pgid}")
    print(f"Total Cursor PGIDs: {cursor_pgids}")
    print("=" * 80)
    print()
    
    java_processes = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'ppid']):
            try:
                process_name = proc.info['name'].lower()
                
                if 'java' in process_name:
                    exe_path = ""
                    try:
                        exe_path = proc.exe()
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        pass
                    
                    cpu_percent = 0.0
                    try:
                        cpu_percent = proc.cpu_percent(interval=0.1)
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        pass
                    
                    pgid = None
                    try:
                        pgid = proc.pgid()
                    except (psutil.AccessDenied, AttributeError):
                        pass
                    
                    ppid = proc.info.get('ppid')
                    parent_name = ""
                    try:
                        if ppid:
                            parent = psutil.Process(ppid)
                            parent_name = parent.name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                    
                    is_java_executable = exe_path == "/usr/bin/java" or exe_path.endswith("/usr/bin/java")
                    high_cpu = cpu_percent > 300.0
                    is_from_cursor_pgid = pgid in cursor_pgids if pgid else False
                    
                    # Check parent chain
                    is_from_cursor_parent = False
                    try:
                        parent = proc.parent()
                        if parent:
                            if 'cursor' in parent.name().lower():
                                is_from_cursor_parent = True
                            else:
                                try:
                                    parent_pgid = parent.pgid()
                                    is_from_cursor_parent = parent_pgid in cursor_pgids
                                except:
                                    pass
                    except:
                        pass
                    
                    is_from_cursor = is_from_cursor_pgid or is_from_cursor_parent
                    
                    java_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'exe': exe_path,
                        'cpu': cpu_percent,
                        'pgid': pgid,
                        'ppid': ppid,
                        'parent_name': parent_name,
                        'is_java_executable': is_java_executable,
                        'high_cpu': high_cpu,
                        'is_from_cursor_pgid': is_from_cursor_pgid,
                        'is_from_cursor_parent': is_from_cursor_parent,
                        'is_from_cursor': is_from_cursor,
                        'should_kill': is_from_cursor and (is_java_executable or high_cpu)
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return
    
    print(f"Found {len(java_processes)} Java process(es):")
    print("=" * 80)
    
    for proc_info in java_processes:
        print(f"\nPID: {proc_info['pid']}")
        print(f"  Name: {proc_info['name']}")
        print(f"  Executable: {proc_info['exe']}")
        print(f"  CPU: {proc_info['cpu']:.1f}%")
        print(f"  PGID: {proc_info['pgid']}")
        print(f"  PPID: {proc_info['ppid']} ({proc_info['parent_name']})")
        print(f"  Is /usr/bin/java: {proc_info['is_java_executable']}")
        print(f"  High CPU (>300%): {proc_info['high_cpu']}")
        print(f"  From Cursor (PGID): {proc_info['is_from_cursor_pgid']}")
        print(f"  From Cursor (Parent): {proc_info['is_from_cursor_parent']}")
        print(f"  From Cursor (Overall): {proc_info['is_from_cursor']}")
        print(f"  SHOULD KILL: {proc_info['should_kill']}")
        if proc_info['should_kill']:
            print("  *** THIS PROCESS WILL BE KILLED ***")
    
    print("\n" + "=" * 80)
    should_kill_count = sum(1 for p in java_processes if p['should_kill'])
    print(f"\nSummary: {should_kill_count} Java process(es) will be killed")

if __name__ == "__main__":
    check_java_processes()
