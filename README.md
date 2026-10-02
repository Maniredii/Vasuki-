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

### 3. Local Web & Mobile UI
Start the local server and interact with VASUKI in a web interface:

```bash
vasuki-py --web
```

* **Desktop:** Navigate to `http://localhost:8000`
* **Mobile Phone:** Connect to the same Wi-Fi and open `http://<your-local-ip>:8000`

---

### 4. Automated Benchmarks
Validate accuracy across algorithmic and data structure test suites:

```bash
# Core 8-category benchmark
vasuki-py --benchmark

# Dedicated 7-test Data Structures benchmark (BST, Trie, Stack, Queue, BFS/DFS)
vasuki-py --ds
```

---

## 💻 Programmatic Node.js API

You can also import and use `vasuki-py` inside your Node.js or JavaScript / TypeScript applications:

```javascript
const { askVasuki, startWebUI } = require('vasuki-py');

async function main() {
  // Query VASUKI programmatically
  const { response } = await askVasuki("Write a Python generator for Fibonacci numbers");
  console.log("Generated Python Code:\n", response);
}

main();
```

---

## 🔌 OpenAI-Compatible REST API

VASUKI includes a built-in, 100% offline OpenAI-compatible REST API. Connect it directly to **Continue.dev (VS Code)**, **Cursor**, **LangChain**, or the official **OpenAI Python SDK**:

```bash
# Start the local OpenAI API server (default port: 8000)
npx vasuki-py --web
# or
python web_vasuki.py
```

### Endpoints
* `GET  /v1/models` — List available models (`vasuki-phase7`, `vasuki`, `gpt-3.5-turbo`)
* `POST /v1/chat/completions` — Standard Chat Completions (supports both JSON and SSE streaming)
* `POST /v1/completions` — Legacy Text Completions

### Using with Continue.dev (VS Code)
Add VASUKI to your `~/.continue/config.json`:
```json
{
  "models": [
    {
      "title": "VASUKI (Local Offline)",
      "provider": "openai",
      "model": "vasuki-phase7",
      "apiBase": "http://localhost:8000/v1"
    }
  ]
}
```

### Using with Python (`openai` SDK)
```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

response = client.chat.completions.create(
    model="vasuki-phase7",
    messages=[{"role": "user", "content": "Write a binary search function in Python"}],
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

---

## 🗺️ Python Mastery Roadmap (Basics to Advanced)

VASUKI is trained to guide developers systematically through all tiers of Python engineering. Read the complete detailed guide in [**PYTHON_ROADMAP.md**](PYTHON_ROADMAP.md):

| Phase | Level | Core Topics & Capabilities |
|:---|:---|:---|
| **Phase 1** | **Fundamentals** | Syntax, dynamic typing, control flow, built-in collections (lists, dicts, sets), functions, scope (LEGB), error handling, context managers. |
| **Phase 2** | **Intermediate** | Object-oriented programming (OOP), dunder methods (`__init__`, `__repr__`, `__len__`), generators, iterators, decorators, list/dict comprehensions. |
| **Phase 3** | **Advanced Core** | Algorithmic reasoning, time/space complexity ($O(N)$ Big-O), Two Pointers, Sliding Window, Monotonic Stacks, BST, Graphs, Dijkstra, Dynamic Programming. |
| **Phase 4** | **Specialist Systems** | CPython memory model, GIL, garbage collection, Concurrency (`asyncio`, `multiprocessing`, `threading`), FFI native bindings (`ctypes`, PyO3), profiling. |
| **Phase 5** | **Mastery Tracks** | **AI & Edge LLM** (NumPy, PyTorch, QLoRA, GGUF edge deployment) or **Backend** (FastAPI, SQLAlchemy, Redis, Docker). |

---

## 🏛️ Architecture & Verification

* **Parameters:** 0.5B (~494M parameters)
* **Quantization Format:** GGUF (Q4_K_M — 379.38 MB | Q3_K_M — 339.00 MB)
* **Training Methodology:** In-house QLoRA fine-tuning on custom curated Python algorithmic corpora, verified abstract syntax trees (AST), and proprietary domain-calibration datasets.
* **Inference Engine:** Optimized local runtime with native stop-token boundary enforcement and automated token loop suppression.

---

## 👨‍💻 Author & Maintainer

**Developed by : Manideep Reddy Eevuri**
* **LinkedIn:** [linkedin.com/in/manideep-reddy-eevuri-661659268](https://www.linkedin.com/in/manideep-reddy-eevuri-661659268/)
* **GitHub:** [@Maniredii](https://github.com/Maniredii)
* **Repository:** [Maniredii/Vasuki-](https://github.com/Maniredii/Vasuki-)
* **Email:** sivareddyevuri92@gmail.com

---

## 📄 License

Apache-2.0 License. Designed and developed by **Manideep Reddy Eevuri**.

