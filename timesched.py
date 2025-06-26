#!/usr/bin/env python3
import time, subprocess
from datetime import datetime

SCHEDULE_FILE = "schedule.txt"
RUN_LOG = {}

def load_schedule():
    schedule = []
    try:
        with open(SCHEDULE_FILE) as f:
            for line in f:
                if not line.strip() or line.strip().startswith("#"):
                    continue
                day, timestr, *cmd = line.strip().split()
                schedule.append((day.upper(), timestr, " ".join(cmd)))
    except FileNotFoundError:
        print(f"Schedule file {SCHEDULE_FILE} not found.")
    return schedule

def align_to_minute():
    sleep_time = 60 - (time.time() % 60)
    time.sleep(sleep_time)


def main():
    print("TimeSched started. Watching for scheduled tasks...")
    align_to_minute()

    schedule = load_schedule()
    last_reload = datetime.now()

    while True:
        now = datetime.now()
        day = now.strftime("%a").upper()[:3]
        time_str = now.strftime("%H:%M")

        # Reload schedule.txt every hour
        if (now - last_reload).total_seconds() >= 3600:
            schedule = load_schedule()
            last_reload = now

        # Check and run matching tasks
        for d, t, cmd in schedule:
            key = f"{d}-{t}-{cmd}"
            if (d == day or d == "DAILY") and t == time_str:
                if RUN_LOG.get(key) != time_str:
                    print(f"[{time_str}] Running: {cmd}")
                    subprocess.Popen(cmd, shell=True)
                    RUN_LOG[key] = time_str

        time.sleep(59)




if __name__ == "__main__":
    main()
