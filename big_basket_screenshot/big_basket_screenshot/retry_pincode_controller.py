import os
import shlex
import subprocess
import sys
import time
import psutil
import pymysql
import re

# ====== CONFIG ======
SOURCE_FILE = "take_screenshot.txt"
COMPLETED_FILE = "completed.txt"
BATCH_SIZE = 4
CHECK_INTERVAL = 10          # seconds between checks
STUCK_THRESHOLD = 5 * 60     # 5 minutes stuck threshold

# ====== DB SETTINGS ======
DB_HOST = "172.27.131.182"
DB_USER = "root"
DB_PASS = "actowiz"

# Base SQL query to check pending count for a single pincode (zipcode)
BASE_SQL_QUERY = """
SELECT COUNT(*) FROM `big_basket_screenshot`.`pdp_link_table_21_06_2025`
WHERE STATUS='pending' AND zipcode=%s
"""

# Extract DB name and table name from SQL query for info/logging
match = re.search(r"`([^`]+)`\.`([^`]+)`", BASE_SQL_QUERY)
if match:
    DB_NAME, DB_TABLE = match.groups()
else:
    raise ValueError("Could not parse database and table name from BASE_SQL_QUERY.")

print(f"[INFO] Monitoring DB: {DB_NAME}, Table: {DB_TABLE}")

def get_pending_count_for_pincode(pincode):
    """Return the count of pending rows for a given pincode."""
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            cursorclass=pymysql.cursors.Cursor
        )
        with conn.cursor() as cur:
            cur.execute(BASE_SQL_QUERY, (pincode,))
            result = cur.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return None

def parse_command_line(line):
    tokens = shlex.split(line, posix=False)
    if not tokens:
        return None

    python_index = None
    for i, t in enumerate(tokens):
        if "python" in t.lower():
            python_index = i
            break

    if python_index is not None:
        if len(tokens) > python_index + 1:
            script_token = tokens[python_index + 1]
            args = tokens[python_index + 2:]
        else:
            return None
    else:
        py_indices = [i for i, t in enumerate(tokens) if t.lower().endswith(".py")]
        if not py_indices:
            return None
        py_i = py_indices[0]
        script_token = tokens[py_i]
        args = tokens[py_i + 1:]

    if not os.path.isabs(script_token):
        candidate = os.path.join(os.getcwd(), script_token)
        if os.path.exists(candidate):
            script_path = candidate
        else:
            script_path = script_token
    else:
        script_path = script_token

    return script_path, args

def extract_pincode_from_args(args):
    """Assuming pincode is passed as one of the command-line arguments as a 5-6 digit number."""
    for arg in args:
        if re.fullmatch(r"\d{5,6}", arg):
            return arg
    return None

def run_single_process(cmd, pincode, batch_number):
    """Run a single process and monitor it with restart on stuck condition."""
    creationflags = 0
    if os.name == 'nt':
        creationflags = subprocess.CREATE_NEW_CONSOLE

    idle_start_time = None
    last_count = None

    while True:
        print(f"[BATCH {batch_number}] Starting PID for pincode {pincode}: {cmd!r}")
        try:
            if creationflags:
                p = subprocess.Popen(cmd, creationflags=creationflags)
            else:
                p = subprocess.Popen(cmd)
        except Exception as e:
            print(f"[ERROR] Failed to start {cmd!r}: {e}")
            return False

        while True:
            if p.poll() is not None:
                print(f"[BATCH {batch_number}] PID {p.pid} exited with code {p.returncode} (pincode {pincode})")
                # If finished successfully, return True
                return p.returncode == 0

            count = get_pending_count_for_pincode(pincode)
            if count is None:
                print(f"[BATCH {batch_number}] DB error while checking pincode {pincode}, skipping idle check.")
                idle_start_time = None
            else:
                if last_count is None:
                    last_count = count
                    idle_start_time = time.time()
                else:
                    if count < last_count:
                        print(f"[BATCH {batch_number}] Pending count decreased for pincode {pincode}: {last_count} -> {count}")
                        last_count = count
                        idle_start_time = time.time()
                    else:
                        idle_duration = time.time() - idle_start_time
                        if idle_duration > STUCK_THRESHOLD:
                            print(f"[BATCH {batch_number}] Pincode {pincode} stuck for {idle_duration//60:.1f} min(s). Killing PID {p.pid} and restarting...")
                            p.kill()
                            p.wait()
                            break  # break inner while, restart process for this pincode

            time.sleep(CHECK_INTERVAL)

def run_batch(batch_lines, batch_number):
    """Run a batch of max BATCH_SIZE commands, restarting stuck pincodes only."""
    processes_info = []  # List of tuples: (cmd, pincode)

    # Prepare the commands and pincodes
    for line in batch_lines:
        parsed = parse_command_line(line)
        if not parsed:
            print(f"[WARN] Could not parse line, skipping: {line!r}")
            continue
        script_path, args = parsed
        pincode = extract_pincode_from_args(args)
        if not pincode:
            print(f"[WARN] Could not extract pincode from command args: {args}")
            continue

        cmd = [sys.executable, script_path] + args
        processes_info.append((cmd, pincode))

    import threading

    def worker(cmd, pincode):
        success = run_single_process(cmd, pincode, batch_number)
        if success:
            print(f"[BATCH {batch_number}] Pincode {pincode} completed successfully.")
        else:
            print(f"[BATCH {batch_number}] Pincode {pincode} failed or stopped.")

    threads = []
    for cmd, pincode in processes_info:
        t = threading.Thread(target=worker, args=(cmd, pincode), daemon=True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Write successful pincodes to COMPLETED_FILE
    with open(COMPLETED_FILE, "a", encoding="utf-8") as cf:
        for _, pincode in processes_info:
            cf.write(f"# pincode {pincode} completed\n")

    print(f"[BATCH {batch_number}] Completed.\n")

def main():
    if not os.path.exists(SOURCE_FILE):
        print(f"[ERROR] {SOURCE_FILE} not found in {os.getcwd()}")
        sys.exit(1)

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        raw_lines = [line.rstrip() for line in f]

    usable = []
    for L in raw_lines:
        s = L.strip()
        if not s or 'timeout' in s.lower():
            continue
        usable.append(s)

    completed = set()
    if os.path.exists(COMPLETED_FILE):
        with open(COMPLETED_FILE, "r", encoding="utf-8") as cf:
            completed = set(line.strip() for line in cf if line.strip())

    # Filter out completed pincodes only if their pending count in DB is zero
    to_run = []
    for line in usable:
        parsed = parse_command_line(line)
        if not parsed:
            continue
        _, args = parsed
        pincode = extract_pincode_from_args(args)
        if not pincode:
            continue

        # Check completed file first
        completed_entry = f"# pincode {pincode} completed"
        if completed_entry in completed:
            # Double-check DB pending count
            count = get_pending_count_for_pincode(pincode)
            if count is None:
                print(f"[WARN] DB error checking pincode {pincode}, including in run list.")
                to_run.append(line)
            elif count > 0:
                print(f"[INFO] Pincode {pincode} marked completed but still pending {count} in DB. Will rerun.")
                to_run.append(line)
            else:
                # Confirmed completed
                continue
        else:
            to_run.append(line)

    if not to_run:
        print("[INFO] No new commands to run. All pincodes completed ✅")
        sys.exit(0)

    total = len(to_run)
    print(f"[Controller] Found {total} new commands to run. Running {BATCH_SIZE} at a time.")

    batch_number = 1
    for i in range(0, total, BATCH_SIZE):
        batch_lines = to_run[i:i+BATCH_SIZE]
        print(f"\n[Controller] Launching batch {batch_number}: lines {i+1}..{i+len(batch_lines)}")
        run_batch(batch_lines, batch_number)
        batch_number += 1

    print("[Controller] All batches finished. ✅")

if __name__ == "__main__":
    main()
