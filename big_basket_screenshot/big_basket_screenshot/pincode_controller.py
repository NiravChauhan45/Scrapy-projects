"""
batch_controller.py

Reads commands.txt (which contains lines like:
start "" python take_screenshot_selenium.py 9222 1 10000 1 110001

It runs 4 commands at a time, each in a new console, waits for those 4 processes
to fully exit, then proceeds to the next 4. Lines containing "timeout" are skipped.
"""

import os
import shlex
import subprocess
import sys
import time

SOURCE_FILE = "take_screenshot.txt"      # your file with the "start "" python ..." lines
BATCH_SIZE = 4
CHECK_INTERVAL = 3               # seconds between checks for running processes

def parse_command_line(line):
    """
    Parse one line and return (script_path, args_list).
    Accepts lines that include 'python' token or directly contain a .py file.
    Uses the current Python interpreter (sys.executable) to launch processes.
    """
    tokens = shlex.split(line, posix=False)  # handle quotes correctly on Windows
    if not tokens:
        return None

    # find the token that looks like python (e.g. "python", "python.exe", full path)
    python_index = None
    for i, t in enumerate(tokens):
        if "python" in t.lower():
            python_index = i
            break

    if python_index is not None:
        # expect script name right after python token
        if len(tokens) > python_index + 1:
            script_token = tokens[python_index + 1]
            args = tokens[python_index + 2:]
        else:
            return None
    else:
        # fallback: find a .py token in the line (script directly provided)
        py_indices = [i for i, t in enumerate(tokens) if t.lower().endswith(".py")]
        if not py_indices:
            return None
        # take first .py token
        py_i = py_indices[0]
        script_token = tokens[py_i]
        args = tokens[py_i + 1:]

    # build absolute path for script if possible
    if not os.path.isabs(script_token):
        candidate = os.path.join(os.getcwd(), script_token)
        if os.path.exists(candidate):
            script_path = candidate
        else:
            # leave as-is; maybe it's in PATH or same folder and will still work
            script_path = script_token
    else:
        script_path = script_token

    return script_path, args

def run_batch(batch_lines, batch_number):
    """
    Launch each parsed command in its own console as a separate python process.
    Wait until all launched processes exit before returning.
    """
    procs = []
    for line in batch_lines:
        parsed = parse_command_line(line)
        if not parsed:
            print(f"[WARN] Could not parse line, skipping: {line!r}")
            continue
        script_path, args = parsed

        cmd = [sys.executable, script_path] + args

        # On Windows create a new console for the child process so it behaves like start ""
        creationflags = 0
        if os.name == 'nt':
            creationflags = subprocess.CREATE_NEW_CONSOLE

        print(f"[BATCH {batch_number}] Starting: {cmd!r}")
        try:
            if creationflags:
                p = subprocess.Popen(cmd, creationflags=creationflags)
            else:
                p = subprocess.Popen(cmd)
            procs.append((p, cmd))
            print(f"[BATCH {batch_number}] PID {p.pid} started.")
        except Exception as e:
            print(f"[ERROR] Failed to start {cmd!r}: {e}")

    # Wait until all procs have exited (block indefinitely until done)
    print(f"[BATCH {batch_number}] Waiting for {len(procs)} process(es) to finish...")
    try:
        while True:
            alive = [ (p,cmd) for (p,cmd) in procs if p.poll() is None ]
            if not alive:
                break
            # optionally print status
            alive_pids = [str(p.pid) for (p,_) in alive]
            print(f"[BATCH {batch_number}] Still running PIDs: {', '.join(alive_pids)}")
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n[Controller] KeyboardInterrupt received. NOT starting next batches. You may terminate child processes manually.")
        raise

    # Print exit codes
    for (p, cmd) in procs:
        print(f"[BATCH {batch_number}] PID {p.pid} exited with code {p.returncode}  cmd={cmd!r}")

    print(f"[BATCH {batch_number}] Completed.\n")

def main():
    if not os.path.exists(SOURCE_FILE):
        print(f"[ERROR] {SOURCE_FILE} not found in {os.getcwd()}")
        return

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        # keep only lines that look like start/python or contain .py, ignore 'timeout' lines
        raw_lines = [line.rstrip() for line in f]
    usable = []
    for L in raw_lines:
        s = L.strip()
        if not s:
            continue
        if 'timeout' in s.lower():
            continue
        # optionally accept lines starting with start or python or containing .py
        usable.append(s)

    if not usable:
        print("[INFO] No usable command lines found in the source file.")
        return

    total = len(usable)
    print(f"[Controller] Found {total} commands (ignoring timeout lines). Will run {BATCH_SIZE} at a time.")

    batch_number = 1
    for i in range(0, total, BATCH_SIZE):
        batch_lines = usable[i:i+BATCH_SIZE]
        print(f"\n[Controller] Launching batch {batch_number}: lines {i+1}..{i+len(batch_lines)}")
        run_batch(batch_lines, batch_number)
        batch_number += 1

    print("[Controller] All batches finished. ✅")

if __name__ == "__main__":
    main()
