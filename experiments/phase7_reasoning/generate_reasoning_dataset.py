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
    Returns high-density algorithmic, debugging, and optimization examples
    adhering strictly to the 4-tier structured reasoning schema.
    """
    records = []

    # =========================================================================
    # CATEGORY 1: ADVANCED ALGORITHMIC PATTERNS & DATA STRUCTURES
    # =========================================================================

    # 1. Two Pointers: Trapping Rain Water
    records.append({
        "id": "cot_algo_0001",
        "category": "algorithmic_reasoning",
        "subcategory": "two_pointers",
        "instruction": "Write a Python function to solve the Trapping Rain Water problem with optimal time and space complexity.",
        "response": build_reasoning_response(
            strategy=(
                "Water trapped at index i is determined by min(max_left, max_right) - height[i]. "
                "Instead of precomputing prefix and suffix max arrays in O(N) space, we maintain two pointers "
                "(left=0, right=n-1) and two running maximums (left_max, right_max). "
                "By always advancing the pointer with the smaller maximum, we guarantee that the bounded height "
                "is constrained by the smaller side, allowing O(1) space computation."
            ),
            edge_cases=[
                "Array length < 3: impossible to trap water, return 0.",
                "Monotonically increasing or decreasing heights: no trough exists, returns 0.",
                "Flat plateau (all equal heights): trapped water is 0."
            ],
            code=(
                "def trap_rain_water(height: list[int]) -> int:\n"
