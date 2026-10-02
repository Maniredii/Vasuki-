# VASUKI (`vasuki-py`)

> **Proprietary 0.5B Edge-Optimized Python Specialist AI Engine**

VASUKI is a lightweight, edge-native AI architecture engineered exclusively for Python development, algorithmic optimization, data structures, and system interoperability. Designed to run completely offline with a footprint under **400 MB RAM**, VASUKI delivers high-precision, syntax-verified Python code generation directly on local CPUs and mobile devices.

[![npm version](https://img.shields.io/npm/v/vasuki-py.svg?color=38bdf8)](https://www.npmjs.com/package/vasuki-py)
[![Author](https://img.shields.io/badge/Author-Manideep%20Reddy%20Eevuri-22c55e.svg)](https://github.com/Maniredii)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://www.linkedin.com/in/manideep-reddy-eevuri-661659268/)
[![GitHub](https://img.shields.io/badge/GitHub-Maniredii-181717?logo=github)](https://github.com/Maniredii)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Mobile-blueviolet)](https://github.com/Maniredii/Vasuki-)

---

## ⚡ Highlights

* **Offline Edge Execution:** Runs locally via quantized 4-bit weights (**379 MB**). Zero cloud dependency, zero data tracking.
* **100% Python AST Verified:** Evaluated and verified across complex algorithmic routines with zero syntax errors.
* **Live Typewriter Streaming:** Real-time token streaming with syntax-colored terminal output.
* **Built-in Developer Sandbox:** Execute, test, and copy generated Python code right from the terminal with `/run` and `/copy`.
* **Mobile & Local Web Server:** Integrated responsive dark-mode Web UI accessible from desktop and mobile browsers over local Wi-Fi.

---

## 📦 Installation

Install globally via npm:

```bash
npm install -g vasuki-py
```

Or run directly without installation:

```bash
npx vasuki-py
```

---

## 🚀 CLI Usage

### 1. Interactive Console (Live Typewriter Mode)
Launch the interactive terminal console to converse with VASUKI in real-time:

```bash
vasuki-py
```
*(or simply `vasuki`)*

```text
VASUKI >>> Write a Python function for binary search
```

#### In-Console Commands:
| Command | Action |
|---|---|
| `/run` | Instantly execute the last generated snippet in a secure local sandbox |
| `/copy` | Copy the generated code directly to your system clipboard |
| `/save <file.py>` | Export the snippet to a `.py` file |
| `/clear` | Clear the terminal screen |
| `exit` | Quit the console |

---

### 2. Single-Prompt Execution
Query VASUKI directly from your terminal or shell scripts:

```bash
vasuki-py "Write a Python class Trie with insert and search methods"
```

```bash
vasuki-py "Write a Python function to check whether a string is a palindrome"
```

---

