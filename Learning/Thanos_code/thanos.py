import os
import time

# ==============================
# CONFIGURATION
# ==============================

# The root directory to start searching from.
# Use "C:\\" for full system scan (can take a long time!)
ROOT_DIR = "E:\\"   # <-- Change this if needed

# Number of days to consider as "3 months" (approx.)
DAYS_LIMIT = 90

# Set to True to delete files automatically
AUTO_DELETE = True

# Optional: Log deletions to a file
LOG_FILE = "deleted_html_files.log"

# ==============================
# MAIN SCRIPT
# ==============================

def main():
    now = time.time()
    cutoff_time = now - (DAYS_LIMIT * 24 * 60 * 60)
    deleted_count = 0

    print(f"\nScanning '{ROOT_DIR}' for .html files older than {DAYS_LIMIT} days...\n")

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        for foldername, subfolders, filenames in os.walk(ROOT_DIR):
            # Skip system folders if scanning entire C drive
            if "Windows" in foldername or "Program Files" in foldername:
                continue

            for filename in filenames:
                if filename.lower().endswith(".html") or filename.lower().endswith(".png"):
                    filepath = os.path.join(foldername, filename)
                    try:
                        mtime = os.path.getmtime(filepath)
                        if mtime < cutoff_time:
                            age_days = int((now - mtime) / (24 * 60 * 60))
                            print(f"Old file found ({age_days} days): {filepath}")

                            if AUTO_DELETE:
                                os.remove(filepath)
                                print(f"  → Deleted.")
                                log.write(f"{filepath}\n")
                                deleted_count += 1
                            else:
                                confirm = input("  Delete this file? [y/N]: ").strip().lower()
                                if confirm == "y":
                                    os.remove(filepath)
                                    print("  → Deleted.")
                                    log.write(f"{filepath}\n")
                                    deleted_count += 1
                                else:
                                    print("  → Skipped.")
                    except Exception as e:
                        print(f"Error with {filepath}: {e}")

    print(f"\n✅ Done! Total deleted files: {deleted_count}")
    print(f"📝 Log saved to: {LOG_FILE}")


if __name__ == "__main__":
    main()
