"""
VASUKI Phase 7: Comprehensive Code Reasoning Dataset Generator
Synthesizes structured Chain-of-Thought (CoT), step-by-step debugging,
and algorithmic optimization examples tailored for 0.5B parameter edge models.
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
    estimate_token_count
)

OUTPUT_DIR = Path("D:/VASUKI/experiments/phase7_reasoning")
OUTPUT_TRAIN_FILE = OUTPUT_DIR / "phase7_reasoning_train.jsonl"
OUTPUT_VAL_FILE = OUTPUT_DIR / "phase7_reasoning_val.jsonl"
OUTPUT_REPORT_FILE = OUTPUT_DIR / "phase7_dataset_quality_report.md"


def get_core_reasoning_records() -> List[Dict[str, Any]]:
    """
