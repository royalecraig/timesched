# TimeSched — Lightweight Task Scheduler

TimeSched is a minimal, cron-style Python scheduler that reads tasks from a simple text file (`schedule.txt`) and runs them at specified times.

## ⚠️ WARNING — Use With Caution

This script **executes commands automatically**, including system-level tasks. **Malicious or incorrect commands can damage your system.**  
Only use trusted `schedule.txt` files, and **review every command** you add.

---

## 📁 Folder Structure

Expected layout:

```
/home/timesched/
├── timesched.py
├── schedule.txt
```

Make sure both files are inside `/home/timesched/` exactly.

---

## ▶️ Running the Scheduler

**Basic (non-privileged tasks only):**
```bash
python3 /home/timesched/timesched.py
```

---

## 🔐 When Sudo Is Needed

If your `schedule.txt` includes commands like:

```bash
sudo apt update
sudo clamscan
sudo rkhunter --check
```

Then you must either:

### ✅ Option 1: Run as Root
```bash
sudo python3 /home/timesched/timesched.py
```

### ✅ Option 2: Configure Passwordless Sudo (for specific tools)
To avoid password prompts every time, **you can grant passwordless rights to trusted commands only**:

Edit your sudoers config:
```bash
sudo visudo
```

Add:
```bash
yourusername ALL=(ALL) NOPASSWD: /usr/bin/apt, /usr/bin/freshclam, /usr/bin/clamscan, /usr/bin/rkhunter
```

Replace `yourusername` with your actual username.

---

## 🚀 Start at Boot with Cron

To auto-run at startup:

```bash
crontab -e
```

Add the line:

```cron
@reboot python3 /home/timesched/timesched.py
```

Make sure your user has permission to run the needed commands (see sudo advice above).

---

## 🧪 Testing

You can manually test the scheduler by running:

```bash
python3 /home/timesched/timesched.py
```

It will check the schedule once per minute and run any matching commands.

---

## 📦 Note

This project assumes a local `/home/timesched/` setup for simplicity. You may adapt it for other paths if needed.


MIT License

Copyright (c) 2025 adrian peirson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


