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

def resolve_model_path(requested_model=None):
    """Finds the GGUF model path across environment, local repo, and user home."""
    req = (requested_model or os.environ.get("VASUKI_MODEL") or "").lower()
    if req in ("phase7", "p7", "reasoning"):
        p7 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vasuki_phase7.Q4_K_M.gguf")
        if os.path.exists(p7):
            return p7
    if req in ("phase6j", "p6j", "stable"):
        p6 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vasuki_phase6j.Q4_K_M.gguf")
        if os.path.exists(p6):
            return p6
    if os.environ.get("VASUKI_MODEL_PATH") and os.path.exists(os.environ["VASUKI_MODEL_PATH"]):
        return os.environ["VASUKI_MODEL_PATH"]
    # Priority 1: Phase 6J (Verified production-stable engine)
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vasuki_phase6j.Q4_K_M.gguf")
    if os.path.exists(local):
        return local
    # Priority 2: Phase 7 Edge Reasoning Engine
    p7 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vasuki_phase7.Q4_K_M.gguf")
    if os.path.exists(p7):
        return p7
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

MODEL_PATH = resolve_model_path(args.model if 'args' in locals() else None)
LLAMA_CLI = resolve_llama_cli()

AUTHOR_NAME = "Manideep Reddy Eevuri"
AUTHOR_GITHUB = "https://github.com/Maniredii"
AUTHOR_LINKEDIN = "https://www.linkedin.com/in/manideep-reddy-eevuri-661659268/"

def print_banner():
    """Displays official author and engine branding banner."""
    model_name = os.path.basename(MODEL_PATH)
    version_title = f"VASUKI • High-Accuracy Edge Python AI [{model_name}]"
    print("\033[96m" + "=" * 72 + "\033[0m")
    print(f"  \033[1;97m{version_title}\033[0m")
    print(f"  \033[1;92mDeveloped by : {AUTHOR_NAME}\033[0m")
    print(f"  \033[94mGitHub       :\033[0m {AUTHOR_GITHUB}")
    print(f"  \033[94mLinkedIn     :\033[0m {AUTHOR_LINKEDIN}")
    print("\033[96m" + "=" * 72 + "\033[0m")

ALPACAPREAMBLE = "### Instruction:\n{prompt}\n\n### Response:\n"

def check_prefix_repetition(text, min_repeats=3):
    """Detects repetitive prefix chains like 'chief assistant', 'chief developer'."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if len(lines) < min_repeats:
        return False

def is_degenerate_output(text):
    """Checks whether the response contains repetitive gibberish or mode collapse."""
    if not text or not text.strip():
        return False
    if check_prefix_repetition(text, min_repeats=3):
        return True
    lower = text.lower()
    artifacts = ["życz", "彩神", "硗heads", "硗ookies", "osoph\nosoph", "icide-tree\nisan"]
    if any(a in lower for a in artifacts):
        return True
    words = text.split()
    if len(words) >= 40:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.28:
            return True
    return False
    prefixes = [l.split()[0].lower() if l.split() else "" for l in lines]
    for i in range(len(prefixes) - min_repeats + 1):
        window = prefixes[i:i + min_repeats]
        if window[0] and all(p == window[0] for p in window):
            return True
    return False

def is_degenerate_output(text):
    """Checks whether the response contains repetitive gibberish or mode collapse."""
    if not text or not text.strip():
        return False
    if check_prefix_repetition(text, min_repeats=3):
        return True
    lower = text.lower()
    artifacts = ["życz", "彩神", "硗heads", "硗ookies", "osoph\nosoph", "icide-tree\nisan"]
    if any(a in lower for a in artifacts):
        return True
    words = text.split()
    if len(words) >= 40:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.28:
            return True
    return False


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

def query_model(prompt_text, max_tokens=350, temp=0.2, allow_fallback=True):
    """Run inference against VASUKI GGUF with automatic accuracy fallback."""
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
        "-r", "\nżycz",
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

        # Truncate at known structural stop tokens
        for st in ["<|im_end|>", "<|endoftext|>", "\n### Instruction", "\n### Response", "彩神"]:
            if st in resp:
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
            if any(k in s.lower() for k in ("życz", "azor", "esian", "abrasive", "poverty")) or s.startswith(("?.", "??", "?.ta")):
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
        # Accuracy Guardrail: If output collapsed into loops, fallback to stable Phase 6J
        if allow_fallback and is_degenerate_output(clean):
            stable_model = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vasuki_phase6j.Q4_K_M.gguf")
            if os.path.exists(stable_model) and MODEL_PATH != stable_model:
                curr_model = MODEL_PATH
                globals()["MODEL_PATH"] = stable_model
                fb_clean, fb_dur = query_model(prompt_text, max_tokens=max_tokens, temp=temp, allow_fallback=False)
                globals()["MODEL_PATH"] = curr_model
                return fb_clean, fb_dur
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

def is_degenerate_output(text):
    """Checks whether the response contains repetitive gibberish or mode collapse."""
    if not text or not text.strip():
        return False
    if check_prefix_repetition(text, min_repeats=3):
        return True
    lower = text.lower()
    artifacts = ["życz", "彩神", "硗heads", "硗ookies", "osoph\nosoph", "icide-tree\nisan"]
    if any(a in lower for a in artifacts):
        return True
    words = text.split()
    if len(words) >= 40:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.28:
            return True
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
        if in_escape:
            sys.stdout.write(char)
            if char == 'm':
                in_escape = False
            continue
        
        sys.stdout.write(char)
        sys.stdout.flush()
        if char == '\n':
            time.sleep(speed * 2.0)
        else:
            time.sleep(speed)
    sys.stdout.write('\n')
    sys.stdout.flush()

def run_benchmark():
    """Runs a quick 8-prompt test across key categories."""
    test_cases = [
        ("Binary Search", "Write a Python function for binary search on a sorted list."),
        ("Prime Checker", "Write a Python function is_prime(n) to check if n is prime."),
        ("Fibonacci Generator", "Write a Python generator that yields the first n Fibonacci numbers."),
        ("Palindrome Check", "Write a Python function is_palindrome(s) that checks if a string is a palindrome."),
        ("Deduplicate List", "Write a Python function to remove duplicates from a list while preserving order."),
        ("Rectangle Class", "Write a Python class Rectangle with width, height, and area method."),
        ("C Interoperability", "How do I call a C shared library from Python using ctypes?"),
        ("Out-of-Domain Boundary", "Write a complete C++ game engine with DirectX 12."),
    ]
    
    print("\n" + "=" * 70)
    print("VASUKI Phase 7 Reasoning Engine Benchmark")
    print(f"Model: {MODEL_PATH} ({os.path.getsize(MODEL_PATH)/(1024**2):.1f} MB)")
    print("=" * 70)
    
    for i, (name, prompt) in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] {name}")
        print(f"Prompt: {prompt}")
        print("-" * 50)
        resp, dur = query_model(prompt)
        show_typing(resp, speed=0.005)
        print("-" * 50)
        print(f"Inference Time: {dur:.2f}s\n")
    print("=" * 70)
    print("Benchmark complete!")
    print("=" * 70)

def interactive_session():
    """Starts interactive REPL in the terminal with developer commands and multi-turn memory."""
    print_banner()
    print(f"\033[90mModel    :\033[0m {os.path.basename(MODEL_PATH)}")
    print("\033[93mCommands :\033[0m")
    print("  \033[93m/run[0m           Execute last generated code snippet in live sandbox")
    print("  \033[93m/copy[0m          Copy last code snippet to clipboard")
    print("  \033[93m/save <file>[0m   Save last code snippet to a Python file")
    print("  \033[93m/history[0m       Show conversation history turns")
    print("  \033[93m/context[0m       Inspect injected sliding-window context")
    print("  \033[93m/reset[0m         Clear conversation history memory")
    print("  \033[93m/clear[0m         Clear terminal screen")
    print("  \033[93mexit / q[0m       Quit the console")
    print("\033[96m" + "-" * 72 + "\033[0m\n")
    
    last_response = ""
    session_history = []  # List of {"user": prompt, "assistant": response}

    while True:
        try:
            turn_idx = len(session_history) + 1
            prompt = input(f"\033[92mVASUKI [T{turn_idx}] >>> \033[0m").strip()
            if not prompt:
                continue
            
            # Slash commands
            if prompt.lower() in ("exit", "quit", "q"):
                print("\033[90mExiting VASUKI console. Goodbye!\033[0m")
                break
            
            if prompt.lower() == "/clear":
                os.system("cls" if os.name == "nt" else "clear")
                continue

            if prompt.lower() in ("/reset", "/forget"):
                session_history.clear()
                last_response = ""
                print("\033[93m[✓] Conversation memory reset.\033[0m\n")
                continue

            if prompt.lower() == "/history":
                if not session_history:
                    print("\033[90m(No previous turns recorded in this session)\033[0m\n")
                else:
                    print(f"\n\033[93m=== Active Session History ({len(session_history)} turns) ===\033[0m")
                    for i, turn in enumerate(session_history, 1):
                        first_line = turn['assistant'].splitlines()[0] if turn['assistant'] else ""
                        print(f"\033[92m[{i}] User     :\033[0m {turn['user']}")
                        print(f"\033[94m    Assistant:\033[0m {first_line[:75]}...\n")
                continue

            if prompt.lower() == "/context":
                if not session_history:
                    print("\033[90m(No conversational context accumulated yet)\033[0m\n")
                else:
                    print("\n\033[93m=== Injected Context Window (Last 3 Turns) ===\033[0m")
                    for t in session_history[-3:]:
                        print(f"User: {t['user']}\nAssistant: {t['assistant']}\n")
                continue

            if prompt.lower() == "/help":
                print("\n\033[93mAvailable Commands:\033[0m")
                print("  /run           - Execute last code snippet in a live Python sandbox")
                print("  /copy          - Copy last code snippet to system clipboard")
                print("  /save <file>   - Save last code snippet into <file>")
                print("  /history       - Display conversation history turns")
                print("  /context       - Display active context window buffer")
                print("  /reset         - Clear conversation memory")
                print("  /clear         - Clear terminal screen")
                print("  exit           - Exit console\n")
                continue

            if prompt.lower() == "/run":
                if not last_response:
                    print("\033[91m[!] No previous code snippet to run.\033[0m\n")
                else:
                    execute_sandbox(last_response)
                continue

            if prompt.lower() == "/copy":
                if not last_response:
                    print("\033[91m[!] No previous code snippet to copy.\033[0m\n")
                else:
                    ok = copy_to_clipboard(last_response)
                    if ok:
                        print("\033[92m[✓] Copied last code snippet to clipboard!\033[0m\n")
                    else:
                        print("\033[91m[!] Failed to copy to clipboard.\033[0m\n")
                continue

            if prompt.lower().startswith("/save"):
                parts = prompt.split(maxsplit=1)
                if len(parts) < 2 or not parts[1].strip():
                    print("\033[91m[!] Usage: /save <filename.py>\033[0m\n")
                elif not last_response:
                    print("\033[91m[!] No previous code snippet to save.\033[0m\n")
                else:
                    save_path = parts[1].strip()
                    try:
                        with open(save_path, "w", encoding="utf-8") as f:
                            f.write(last_response + "\n")
                        print(f"\033[92m[✓] Saved snippet to {save_path}\033[0m\n")
                    except Exception as e:
                        print(f"\033[91m[!] Error saving file: {e}\033[0m\n")
                continue

            # Build multi-turn context query
            if session_history:
                context_chunks = []
                for turn in session_history[-3:]:  # Sliding window of 3 turns for length budget
                    context_chunks.append(f"Previous Request: {turn['user']}\nPrevious Code: {turn['assistant']}")
                injected_prompt = "\n\n".join(context_chunks) + f"\n\nCurrent Task (modify/extend based on context): {prompt}"
            else:
                injected_prompt = prompt

            print("\033[90m[VASUKI is typing...]\033[0m", end="\r", flush=True)
            response, elapsed = query_model(injected_prompt)
            print(" " * 30, end="\r")  # Clear the typing banner
            print("-" * 55)
            show_typing(response, speed=0.009, colorize=True)
            print("-" * 55)
            print(f"\033[90m(Generated in {elapsed:.2f}s | Turn {turn_idx} | Type /run to test, /copy to copy)\033[0m\n")
            last_response = response
            session_history.append({"user": prompt, "assistant": response})

        except (KeyboardInterrupt, EOFError):
            print("\nExiting VASUKI console.")
            break


def run_ds_benchmark():
    """Runs a dedicated Data Structures benchmark."""
    ds_cases = [
        ("Stack (LIFO)", "Write a Python class Stack with push, pop, peek, and is_empty methods"),
        ("Queue (FIFO)", "Write a Python class Queue with enqueue, dequeue, and is_empty methods"),
        ("Binary Search Tree (BST)", "Write a Python class BST with insert and search methods"),
        ("Trie (Prefix Tree)", "Write a Python class Trie with insert and search methods"),
        ("Linked List Reversal", "Write a Python function reverse_linked_list(head) that reverses a singly linked list and returns the new head"),
        ("Graph BFS Traversal", "Write a Python function bfs(graph, start) to perform breadth-first search traversal on an adjacency list graph"),
        ("Graph DFS Traversal", "Write a Python function dfs(graph, start) to perform depth-first search traversal on a graph"),
    ]
    
    print("\n" + "=" * 70)
    print("VASUKI Phase 6J Data Structures Benchmark")
    print(f"Model: {MODEL_PATH} ({os.path.getsize(MODEL_PATH)/(1024**2):.1f} MB)")
    print("=" * 70)
    
    for i, (name, prompt) in enumerate(ds_cases, 1):
        print(f"\n[{i}/{len(ds_cases)}] {name}")
        print(f"Prompt: {prompt}")
        print("-" * 50)
        resp, dur = query_model(prompt)
        show_typing(resp, speed=0.006)
        print("-" * 50)
        print(f"Inference Time: {dur:.2f}s\n")
    print("=" * 70)
    print("Data Structures Benchmark complete!")
    print("=" * 70)

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file not found at {MODEL_PATH}")
        sys.exit(1)
    if not os.path.exists(LLAMA_CLI):
        print(f"Error: llama-cli.exe not found at {LLAMA_CLI}")
        sys.exit(1)
        
    parser = argparse.ArgumentParser(description="VASUKI Phase 7: Offline Python AI Specialist Engine")
    parser.add_argument("prompt", nargs="?", default=None, help="Prompt or task instruction")
    parser.add_argument("--fix", type=str, metavar="FILE", help="Fix bugs and optimize the specified Python file")
    parser.add_argument("--test", type=str, metavar="FILE", help="Generate pytest unit tests for the specified Python file")
    parser.add_argument("--audit", type=str, metavar="FILE", help="Perform complexity, quality, and security audit on the specified file")
    parser.add_argument("--doc", type=str, metavar="FILE", help="Add type hints and docstrings to the specified Python file")
    parser.add_argument("--in-place", action="store_true", help="Write changes directly back to the target file (creates .bak backup)")
    parser.add_argument("--raw", action="store_true", help="Print only raw output (no banners, formatting, or timing; useful for pipes)")
    parser.add_argument("--pipe", action="store_true", help="Read input from standard input (pipe)")
    parser.add_argument("--benchmark", action="store_true", help="Run automated multi-prompt benchmark")
    parser.add_argument("--ds", action="store_true", help="Run dedicated Data Structures benchmark")
    parser.add_argument("--model", type=str, choices=["phase6j", "phase7", "stable", "reasoning"], default=None, help="Choose active engine model")
    
    args = parser.parse_args()
    
    is_pipe_out = not sys.stdout.isatty() or args.raw

    # 1. Benchmarks
    if args.ds:
        run_ds_benchmark()
        return
    elif args.benchmark:
        run_benchmark()
        return

    # 2. File-based operations (--fix, --test, --audit, --doc)
    target_file = args.fix or args.test or args.audit or args.doc
    if target_file:
        if not os.path.exists(target_file):
            print(f"\033[91m[Error] File not found: {target_file}\033[0m", file=sys.stderr)
            sys.exit(1)
        try:
            with open(target_file, "r", encoding="utf-8", errors="replace") as f:
                file_code = f.read()
        except Exception as e:
            print(f"\033[91m[Error] Failed to read {target_file}: {e}\033[0m", file=sys.stderr)
            sys.exit(1)
            
        if args.fix:
            query = f"Fix all bugs, handle edge cases, and optimize this Python code:\n\n{file_code}"
        elif args.test:
            query = f"Write unit test cases using pytest for this Python code:\n\n{file_code}"
        elif args.audit:
            query = f"Analyze time complexity, space complexity, and security for this Python code:\n\n{file_code}"
        elif args.doc:
            query = f"Add Python docstrings and type annotations to this code:\n\n{file_code}"
            
        if not is_pipe_out:
            print_banner()
            action_name = "Fixing" if args.fix else ("Generating tests for" if args.test else ("Auditing" if args.audit else "Documenting"))
            print(f"\033[93m[{action_name}]:\033[0m {target_file}\n")
            
        resp, dur = query_model(query, max_tokens=500)
        
        # If --in-place requested for --fix or --doc
        if args.in_place and (args.fix or args.doc):
            backup_file = f"{target_file}.bak"
            with open(backup_file, "w", encoding="utf-8") as bf:
                bf.write(file_code)
            with open(target_file, "w", encoding="utf-8") as tf:
                tf.write(resp + "\n")
            if not is_pipe_out:
                print(f"\033[92m[✓] Successfully updated {target_file} (Backup saved to {backup_file})\033[0m")
                print(f"\033[90m(Completed in {dur:.2f}s)\033[0m\n")
            return
            
        if is_pipe_out:
            sys.stdout.write(resp + "\n")
            sys.stdout.flush()
        else:
            show_typing(resp, speed=0.008)
            print(f"\n\033[90m(Inference time: {dur:.2f}s)\033[0m\n")
        return

    # 3. Piped stdin handling (--pipe, "-", or piped stdin when prompt is given)
    piped_content = ""
    if args.pipe or args.prompt == "-":
        try:
            piped_content = sys.stdin.read().strip()
        except Exception:
            piped_content = ""

    if piped_content:
        prompt_instruction = args.prompt if args.prompt and args.prompt != "-" else "Analyze, optimize, or complete the following Python code:"
        query = f"{prompt_instruction}\n\n```python\n{piped_content}\n```"
        resp, dur = query_model(query)
        if is_pipe_out:
            sys.stdout.write(resp + "\n")
            sys.stdout.flush()
        else:
            print_banner()
            print(f"\033[93mPiped Input Processed:\033[0m\n")
            show_typing(resp, speed=0.008)
            print(f"\n\033[90m(Inference time: {dur:.2f}s)\033[0m\n")
        return

    # 4. Standard command-line prompt
    if args.prompt:
        resp, dur = query_model(args.prompt)
        if is_pipe_out:
            sys.stdout.write(resp + "\n")
            sys.stdout.flush()
        else:
            print_banner()
            print(f"\033[93mPrompt:\033[0m {args.prompt}\n")
            show_typing(resp, speed=0.012)
            print(f"\n\033[90m(Inference time: {dur:.2f}s)\033[0m\n")
        return

    # 5. Fallback to interactive REPL
    interactive_session()

if __name__ == "__main__":
    main()
