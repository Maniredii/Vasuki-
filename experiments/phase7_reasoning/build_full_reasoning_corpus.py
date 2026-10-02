"""
VASUKI Phase 7: Full Reasoning Corpus Builder & Multi-Source Synthesizer
Compiles a rich dataset combining:
1. Core Algorithmic & Data Structure Reasoning (Chain-of-Thought)
2. Step-by-Step Execution Tracing & Debugging
3. Algorithmic Optimization & Trade-Off Analysis
4. Boundary Redirects (Preserving Python Specialization)
5. Calibrated General Python Instructions
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any

from reasoning_schema import (
    build_reasoning_response,
    build_debug_response,
    build_optimization_response,
    validate_ast,
    execute_in_sandbox,
    estimate_token_count,
    extract_python_code
)

BASE_DIR = Path("D:/VASUKI/experiments/phase7_reasoning")
PHASE6J_DIR = Path("D:/VASUKI/experiments/phase6j")

OUTPUT_TRAIN_FILE = BASE_DIR / "phase7_reasoning_corpus.jsonl"
OUTPUT_VAL_FILE = BASE_DIR / "phase7_reasoning_val.jsonl"
OUTPUT_REPORT_FILE = BASE_DIR / "phase7_corpus_report.md"


def generate_extended_algorithmic_records() -> List[Dict[str, Any]]:
    """Synthesizes high-density reasoning records across critical algorithmic paradigms."""
    recs = []

