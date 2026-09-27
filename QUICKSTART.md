# VASUKI Quick Start Guide

VASUKI (`vasuki-py`) is an offline, edge-optimized 0.5B parameter Python specialist AI engine designed to run locally with zero cloud dependencies and under 400 MB of RAM.

---

## ⚡ Quickest Way to Run (npm)

### Option 1: Run Instantly via npx
```bash
npx vasuki-py
```

### Option 2: Install Globally
```bash
npm install -g vasuki-py
vasuki-py
```

---

## 💻 CLI Commands

### 1. Interactive Console (Live Typewriter Streaming)
```bash
vasuki-py
```
* **`/run`**: Execute the last generated Python code in a local sandbox.
* **`/copy`**: Copy the snippet directly to your clipboard.
* **`/save <filename.py>`**: Save the code snippet to disk.
* **`/clear`**: Clear the terminal screen.
* **`exit`**: Quit the console.

### 2. Single-Prompt Query
```bash
vasuki-py "Write a Python function to check if a word is a palindrome"
```

### 3. Launch Local Web & Mobile UI
```bash
vasuki-py --web
```
* **Desktop:** `http://localhost:8000`
* **Mobile (same Wi-Fi):** `http://<your-local-ip>:8000`

### 4. Run Benchmarks
```bash
vasuki-py --benchmark
vasuki-py --ds
```

---

## 🐍 Python Usage

You can also run the local engine directly using Python:

```powershell
# Interactive mode
python test_vasuki.py

# Launch web server
python web_vasuki.py

# Run comprehensive system verification
python retest_all.py
```
