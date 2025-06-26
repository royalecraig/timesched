# TimeSched

A lightweight, human-friendly task scheduler for Linux.

## Usage

Edit the `schedule.txt` file with your desired schedule using this format:

```
DAY HH:MM command
```

Example:
```
MON 09:00 espeak "Good morning, Adey."
FRI 23:03 /home/adey/SecurityScans/clamav_scan.sh
```

Run the scheduler with:
```
python3 timesched.py
```

You can autostart it via crontab (`@reboot`) or a `.desktop` file.
