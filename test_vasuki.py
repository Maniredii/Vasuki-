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
