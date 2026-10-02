"""
VASUKI Phase 7.2: Large-Scale Corpus Expansion Pipeline
Expands the training dataset to 5,000+ verified records across:
1. Current Phase 7.1 Balanced Corpus (3,086 records)
2. Local iamtarun/python_code_instructions_18k_alpaca (+1,200 records)
3. sahil2801/CodeAlpaca-20k (+500 records)
4. flytech/python-codes-25k (+500 records)

Enforces:
- 100% Python AST validation on all code blocks
- Length and token quality guardrails
- Strict deduplication and zero validation contamination
"""

import sys
import os
import json
from pathlib import Path
from datasets import load_dataset

from reasoning_schema import validate_ast, extract_python_code, estimate_token_count

BASE_DIR = Path("D:/VASUKI/experiments/phase7_reasoning")
CURRENT_BALANCED_FILE = BASE_DIR / "phase7_1_balanced_corpus.jsonl"
LOCAL_IAMTARUN_FILE = Path("D:/VASUKI/experiments/phase6j/iamtarun_python_18k.jsonl")

OUT_EXPANDED_FILE = BASE_DIR / "phase7_2_expanded_corpus.jsonl"
OUT_REPORT_FILE = BASE_DIR / "phase7_2_expansion_report.md"
VAL_FILE = BASE_DIR / "phase7_reasoning_val.jsonl"


def is_valid_entry(instruction: str, response: str) -> bool:
    """Strict quality filter for candidate records."""
    inst = instruction.strip()
    resp = response.strip()

    if not inst or not resp:
        return False
    if len(inst) < 15 or len(resp) < 40 or len(resp) > 2800:
        return False

    # Check for truncated code block artifacts
    if resp.count("```") % 2 != 0:
        return False

    # Verify all embedded code blocks parse cleanly
    codes = extract_python_code(resp)
    if codes:
        for c in codes:
            # Skip empty blocks
            if not c.strip():
                continue
            ok, _ = validate_ast(c)
            if not ok:
                return False

