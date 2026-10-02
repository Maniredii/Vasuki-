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
