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

