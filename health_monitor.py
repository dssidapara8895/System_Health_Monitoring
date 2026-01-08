import os
import csv
import psutil
import shutil
import time
from datetime import datetime

# ===============================
# Thresholds (adjust if needed)
# ===============================
CPU_MAX_PERCENT = 85
RAM_MAX_PERCENT = 85
DISK_FREE_MIN_PERCENT = 15

TXT_LOG_FILE = "health_log.txt"
CSV_LOG_FILE = "health_log.csv"

# ===============================
# Metric functions
# ===============================
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    return psutil.virtual_memory().percent

def get_disk_free_percent(path="/"):
    total, used, free = shutil.disk_usage(path)
    return round((free / total) * 100, 2)

# ===============================
# Logging functions
# ===============================
def write_txt_log(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TXT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{level}] {message}\n")

def write_csv_log(timestamp, cpu, ram, disk, status):
    file_exists = os.path.exists(CSV_LOG_FILE)
    with open(CSV_LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "cpu_percent", "ram_percent", "disk_free_percent", "status"])
        writer.writerow([timestamp, cpu, ram, disk, status])

# ===============================
# Main monitoring logic (one run)
# ===============================
def main():
    # Use C:\ for Windows, / for Linux/macOS
    drive = "C:\\" if os.name == "nt" else "/"

    cpu = get_cpu_usage()
    ram = get_ram_usage()
    disk = get_disk_free_percent(drive)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ---- Screen output ----
    print("System Health Check")
    print("-------------------")
    print(f"CPU Usage (%):  {cpu:.1f}")
    print(f"RAM Usage (%):  {ram:.1f}")
    print(f"Disk Free (%):  {disk:.2f}")

    # ---- Determine status + warnings ----
    issues = []
    if cpu > CPU_MAX_PERCENT:
        issues.append(f"High CPU usage (>{CPU_MAX_PERCENT}%)")
    if ram > RAM_MAX_PERCENT:
        issues.append(f"High RAM usage (>{RAM_MAX_PERCENT}%)")
    if disk < DISK_FREE_MIN_PERCENT:
        issues.append(f"Low disk space (<{DISK_FREE_MIN_PERCENT}% free)")

    status = "OK" if not issues else ("CRITICAL" if disk < DISK_FREE_MIN_PERCENT else "WARNING")

    # ---- Log the readable lines (TXT) ----
    write_txt_log("INFO", f"CPU Usage (%):  {cpu:.1f}")
    write_txt_log("INFO", f"RAM Usage (%):  {ram:.1f}")
    write_txt_log("INFO", f"Disk Free (%):  {disk:.2f}")

    if issues:
        print("\nALERTS:")
        for issue in issues:
            print(f"- {issue}")
            write_txt_log(status, issue)
    else:
        print("\nSystem health normal")
        write_txt_log("INFO", "System health normal")

    # ---- Log one row to CSV for analytics ----
    write_csv_log(timestamp, round(cpu, 1), round(ram, 1), disk, status)

# ===============================
# Run continuously every 5 seconds
# ===============================
if __name__ == "__main__":
    try:
        while True:
            main()
            print("-" * 40)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nStopped by user (Ctrl + C).")

