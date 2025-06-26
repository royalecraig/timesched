import asyncio
from bleak import BleakScanner
from datetime import datetime, time
import os
from datetime import datetime, time, timedelta

TARGET_NAME_PREFIX = "H6M"
LOG_PATH = "/home/adey/hr_logs/coospo_today.csv"
LOG_FLUSH_INTERVAL = 600  # seconds (10 minutes)

buffer = []
seen = set()

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def extract_hr(value: bytes):
    if len(value) >= 1:
        return value[-1]
    return None

def callback(device, adv_data):
    if not (device.name and device.name.startswith(TARGET_NAME_PREFIX)):
        return

    now = datetime.now()
    mfg = adv_data.manufacturer_data or {}

    for key, val in mfg.items():
        hr = extract_hr(val)
        tag = (key, hr)
        if hr and tag not in seen:
            seen.add(tag)
            timestamp = now.isoformat(timespec="seconds")
            buffer.append(f"{timestamp},{hr}")
            print(f"[{timestamp}] 🫀 HR: {hr} bpm")

async def pulsed_scan(scan_duration=0.5, rest_duration=0.5):
    scanner = BleakScanner(callback)
    await scanner.start()
    try:
        while True:
            await asyncio.sleep(scan_duration)
            await scanner.stop()
            await asyncio.sleep(rest_duration)
            await scanner.start()
    except asyncio.CancelledError:
        await scanner.stop()
        raise

async def flush_buffer_periodically():
    while True:
        await asyncio.sleep(LOG_FLUSH_INTERVAL)
        if buffer:
            with open(LOG_PATH, "a") as f:
                f.write("\n".join(buffer) + "\n")
            buffer.clear()
            print(f"💾 Flushed to {LOG_PATH}")

async def midnight_file_reset():
    while True:
        now = datetime.now()
        next_midnight = datetime.combine(now.date(), time(0)) + timedelta(days=1)
        seconds_until_midnight = (next_midnight - now).total_seconds()
        await asyncio.sleep(seconds_until_midnight)

        # Reset file
        try:
            open(LOG_PATH, "w").close()
            print("🕛 Midnight reset: Log file overwritten.")
        except Exception as e:
            print(f"⚠️ Midnight reset failed: {e}")

async def main():
    print("📡 Pulsed Coospo HR Logger — 10m flush, midnight reset. Ctrl+C to stop.")
    await asyncio.gather(
        pulsed_scan(),
        flush_buffer_periodically(),
        midnight_file_reset()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Exiting cleanly.")
