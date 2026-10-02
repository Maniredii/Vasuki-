"""
VASUKI Phase 6J: Interactive Terminal Testing & Live Benchmark Tool
Usage:
  1. Interactive Chat Mode:
     python test_vasuki.py
  2. Quick Single-Prompt Test:
     python test_vasuki.py "Write a Python function to compute Fibonacci numbers"
  3. Run Automated 10-Prompt Accuracy Benchmark:
     python test_vasuki.py --benchmark
"""

import sys
import os
import re
import subprocess
import time
import argparse

# Force UTF-8 on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import shutil

def resolve_model_path():
    """Finds the GGUF model path across environment, local repo, and user home."""
    if os.environ.get("VASUKI_MODEL_PATH") and os.path.exists(os.environ["VASUKI_MODEL_PATH"]):
        return os.environ["VASUKI_MODEL_PATH"]
    # Priority 1: Phase 7 Edge Reasoning Engine
    p7 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vasuki_phase7.Q4_K_M.gguf")
    if os.path.exists(p7):
        return p7
    # Priority 2: Phase 6J
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vasuki_phase6j.Q4_K_M.gguf")
    if os.path.exists(local):
        return local
    home_model = os.path.join(os.path.expanduser("~"), ".vasuki", "models", "vasuki_phase7.Q4_K_M.gguf")
    if os.path.exists(home_model):
        return home_model
    home_model_6j = os.path.join(os.path.expanduser("~"), ".vasuki", "models", "vasuki_phase6j.Q4_K_M.gguf")
    if os.path.exists(home_model_6j):
        return home_model_6j
    return local

def resolve_llama_cli():
    """Finds llama-cli executable in repo or system PATH."""
    if os.environ.get("LLAMA_CLI_PATH") and os.path.exists(os.environ["LLAMA_CLI_PATH"]):
        return os.environ["LLAMA_CLI_PATH"]
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools", "llama.cpp", "llama-cli.exe")
    if os.path.exists(local):
        return local
    which_cli = shutil.which("llama-cli") or shutil.which("llama-cli.exe")
    if which_cli:
        return which_cli
    return local

MODEL_PATH = resolve_model_path()
LLAMA_CLI = resolve_llama_cli()

AUTHOR_NAME = "Manideep Reddy Eevuri"
AUTHOR_GITHUB = "https://github.com/Maniredii"
AUTHOR_LINKEDIN = "https://www.linkedin.com/in/manideep-reddy-eevuri-661659268/"

def print_banner():
    """Displays official author and engine branding banner."""
    version_title = "VASUKI Phase 7 • Edge Reasoning Python AI" if "phase7" in MODEL_PATH.lower() else "VASUKI Phase 6J • 0.5B Edge Python Specialist Engine"
    print("\033[96m" + "=" * 72 + "\033[0m")
    print(f"  \033[1;97m{version_title}\033[0m")
    print(f"  \033[1;92mDeveloped by : {AUTHOR_NAME}\033[0m")
    print(f"  \033[94mGitHub       :\033[0m {AUTHOR_GITHUB}")
    print(f"  \033[94mLinkedIn     :\033[0m {AUTHOR_LINKEDIN}")
    print("\033[96m" + "=" * 72 + "\033[0m")

ALPACAPREAMBLE = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{prompt}\n\n### Response:\n"

def check_domain_boundary(prompt_text):
    """
    Detects non-Python requests and returns a polite redirect if not asking for Python interop.
    Allows queries mentioning other languages if they also ask for Python bridging.
    """
    lower = prompt_text.lower()
    
    # Check if asking for Python interop
    if any(k in lower for k in ["python", "ctypes", "pyo3", "cffi", "binding", "convert to python", "in python"]):
        return None
        
    # Check for pure out-of-domain requests
    non_py_triggers = [
        "c++", "directx", "spring boot", "swiftui", "objective-c", "rust", 
        "golang", "c#", ".net", "kotlin", "ruby on rails", "php"
    ]
    for trigger in non_py_triggers:
        if trigger in lower:
            return (
                f"I specialize exclusively in Python programming, algorithmic optimization, data structures, and Python system integrations.\n"
                f"While I do not generate standalone {trigger.upper()} systems, I can help you implement the equivalent architecture in Python "
                f"or design Python bindings to interface with existing native libraries."
            )
    return None

def query_model(prompt_text, max_tokens=350, temp=0.2):
    """Run inference against VASUKI Phase 6J GGUF via llama-cli."""
    # Check domain boundary first
    redirect = check_domain_boundary(prompt_text)
    if redirect:
        return redirect, 0.05
        
    full_prompt = ALPACAPREAMBLE.format(prompt=prompt_text)
    
    cmd = [
        LLAMA_CLI,
        "-m", MODEL_PATH,
        "-p", full_prompt,
        "-n", str(max_tokens),
        "--temp", str(temp),
        "--repeat-penalty", "1.15",
        "--repeat-last-n", "64",
        "-r", "<|im_end|>",
        "-r", "<|endoftext|>",
        "-r", "### Instruction",
        "-r", "###",
        "-r", "彩神",
        "-r", "ica",
        "-r", "icas",
        "-r", "rix",
        "-r", "azor",
        "-r", "esian",
        "-r", "życz",
        "-r", "poverty",
        "--single-turn"
    ]
    
    t0 = time.time()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30
        )
        elapsed = time.time() - t0
        output = proc.stdout
        
        # Clean response header
        if "### Response:\n" in output:
            resp = output.split("### Response:\n")[-1]
        elif "### Response:" in output:
            resp = output.split("### Response:")[-1]
        else:
            resp = output

        if "[ Prompt:" in resp:
            resp = resp.split("[ Prompt:")[0]

        # Truncate at known stop tokens
        for st in ["<|im_end|>", "<|endoftext|>", "### Instruction", "### Response", "###", "彩神", "ica", "icas", "esian", "azor", "życz", "rix", "abrasive", "poverty"]:
            if f"\n{st}" in resp:
                resp = resp.split(f"\n{st}")[0]
            elif resp.endswith(st):
                resp = resp[:-len(st)]
            elif st in resp:
                resp = resp.split(st)[0]

        # If response contains structured reasoning sections, preserve complete markdown
        reasoning_headers = [
            "### Problem Analysis", "### Edge Cases", "### Complexity",
            "### Root Cause", "### Performance", "### Algorithmic",
            "### Key Takeaway", "### Python Implementation"
        ]
        if any(h in resp for h in reasoning_headers):
            return resp.strip(), elapsed

        # 1. If markdown fences are used without structured reasoning, extract code block
        if "```" in resp:
            parts = resp.split("```")
            if len(parts) >= 3:
                return f"```{parts[1]}```".strip(), elapsed

        lines = resp.splitlines()
        cleaned_lines = []
        last_stripped = None
        consecutive_repeat = 0
        has_entered_code = False

        py_keywords = {
            "def", "class", "return", "import", "from", "for", "while", "if",
            "elif", "else", "try", "except", "finally", "with", "raise", "pass",
            "assert", "yield", "print"
        }

        for line in lines:
            s = line.strip()
            if not s:
                if cleaned_lines:
                    cleaned_lines.append(line)
                continue

            # Check if line is indented code
            if line.startswith(("    ", "\t", "  ")):
                has_entered_code = True
                cleaned_lines.append(line)
                last_stripped = s
                consecutive_repeat = 0
                continue

            # 2. Immediate consecutive line loop check (e.g. rix / rix / rix)
            if s == last_stripped:
                consecutive_repeat += 1
                if consecutive_repeat >= 1:
                    break
            else:
                consecutive_repeat = 0
                last_stripped = s

            # 3. Known subword / loop artifacts
            if s.lower() in ("rix", "azor", "esian", "życz", "abrasive", "poverty"):
                break

            # 4. Check for counting loop artifacts like `-1`, `-2`, `-3` or `1.`, `2.`
            if re.match(r"^[`'\"]?-\d+[`'\"]?$", s) or re.match(r"^[`'\"]?\d+[`'\"]?$", s):
                break

            # 5. If we have entered code body, an unindented non-code statement is trailing garbage
            if has_entered_code and not s.startswith(("#", "def ", "class ", "import ", "from ", "if __name__", "@")):
                break

            # 6. Check for orphan lowercase non-code words after explanation bullets/text
            words = s.split()
            if len(words) == 1 and not s.startswith(("-", "*", "#", "```")):
                word = words[0].strip("`'\":;.,()[]{}")
                if cleaned_lines and not any(cleaned_lines[-1].strip().startswith(kw) for kw in ("def ", "class ", "if ", "for ", "while ")):
                    if word.lower() not in py_keywords and not word.isdigit():
                        break

            cleaned_lines.append(line)

        clean = "\n".join(cleaned_lines).strip()
        return clean, elapsed
    except subprocess.TimeoutExpired:
        return "[Error: Model inference timed out after 45s]", 45.0
    except Exception as e:
        return f"[Error: {e}]", 0.0

def colorize_python(text):
    """Adds ANSI terminal syntax colors to Python code."""
    CYAN = '\033[96m'      # Keywords
    YELLOW = '\033[93m'    # Function / Class names
    GREEN = '\033[92m'     # Strings
    MAGENTA = '\033[95m'   # Numbers / Booleans
    GRAY = '\033[90m'      # Comments
    RESET = '\033[0m'

    keywords = {
        "def", "class", "return", "yield", "import", "from", "as",
        "if", "elif", "else", "for", "while", "in", "try", "except",
        "finally", "with", "raise", "pass", "break", "continue",
        "lambda", "global", "nonlocal", "assert", "async", "await"
    }
    booleans = {"True", "False", "None", "self"}

    colored_lines = []
    for line in text.splitlines():
        # Comment line
        stripped = line.strip()
        if stripped.startswith("#"):
            colored_lines.append(f"{GRAY}{line}{RESET}")
            continue

        # Simple token colorization
        # Split tokens while preserving indentation
        parts = re.split(r'(\b\w+\b|["][^"]*["]|[\'][^\']*[\']|#.*$)', line)
        out_line = []
        is_def_or_class = False
        for part in parts:
            if not part:
                continue
            if part.startswith("#"):
                out_line.append(f"{GRAY}{part}{RESET}")
            elif (part.startswith('"') and part.endswith('"')) or (part.startswith("'") and part.endswith("'")):
                out_line.append(f"{GREEN}{part}{RESET}")
            elif part in keywords:
                out_line.append(f"{CYAN}{part}{RESET}")
                if part in ("def", "class"):
                    is_def_or_class = True
            elif part in booleans:
                out_line.append(f"{MAGENTA}{part}{RESET}")
            elif part.isdigit():
                out_line.append(f"{MAGENTA}{part}{RESET}")
            elif is_def_or_class and re.match(r'^[a-zA-Z_]\w*$', part):
                out_line.append(f"{YELLOW}{part}{RESET}")
                is_def_or_class = False
            else:
                out_line.append(part)
        colored_lines.append("".join(out_line))
    return "\n".join(colored_lines)

def copy_to_clipboard(text):
    """Copies text to the system clipboard on Windows."""
    try:
        cmd = ["powershell", "-NoProfile", "-Command", "$input | Set-Clipboard"]
        proc = subprocess.run(cmd, input=text, text=True, capture_output=True)
        return proc.returncode == 0
    except Exception:
        return False

def execute_sandbox(code_str):
    """Executes generated code in a safe sandbox and displays output."""
    import io
    import contextlib
    import ast

    # Strip markdown fences if present
    clean_code = code_str.strip()
    if "```python" in clean_code:
        clean_code = clean_code.split("```python")[-1].split("```")[0].strip()
    elif "```" in clean_code:
        clean_code = clean_code.split("```")[-1].split("```")[0].strip()

    # Strip conversational prefixes like "Code:", "Python:", "Solution:"
    lines = clean_code.splitlines()
    while lines and lines[0].strip().lower().rstrip(":") in ("code", "python", "solution", "output", "program", "here is the code", "implementation"):
        lines.pop(0)
    clean_code = "\n".join(lines).strip()

    # Pre-validate with ast.parse to detect non-code / conceptual theory text
    try:
        parsed = ast.parse(clean_code)
        if not parsed.body:
            raise SyntaxError("Empty AST body")
    except SyntaxError:
        print("\n" + "\033[94m" + "-" * 55 + "\033[0m")
        print("\033[93m[Sandbox Notice]: The last response is a conceptual explanation / text, not executable Python code.\033[0m")
        print("\033[90m(Tip: Ask VASUKI to 'Write Python code for...' to run and test execution with /run)\033[0m")
        print("\033[94m" + "-" * 55 + "\033[0m\n")
        return

    print("\n" + "\033[94m" + "-" * 55 + "\033[0m")
    print("\033[93m[Sandbox Execution Running...]\033[0m")
    buf = io.StringIO()
    start_t = time.time()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            scope = {}
            exec(clean_code, scope, scope)
        elapsed = time.time() - start_t
        out = buf.getvalue().strip()
        if out:
            print("\033[92m[Program Output]:\033[0m")
            print(out)
        else:
            print("\033[92m[OK] Code executed with zero errors (no print output produced).\033[0m")
        print(f"\033[90m(Execution time: {elapsed*1000:.1f}ms)\033[0m")
    except Exception as e:
        print(f"\033[91m[Execution Error]: {type(e).__name__}: {e}\033[0m")
    print("\033[94m" + "-" * 55 + "\033[0m\n")

def show_typing(text, speed=0.010, colorize=True):
    """Prints text with syntax colors and typewriter animation."""
    display_text = colorize_python(text) if colorize else text
    # Ansi escape sequence aware typing
    in_escape = False
    for char in display_text:
        if char == '\033':
            in_escape = True
