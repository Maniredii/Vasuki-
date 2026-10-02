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

    # 1. Sliding Window: Minimum Size Subarray Sum
    recs.append({
        "id": "algo_cot_001",
        "category": "algorithmic_reasoning",
        "subcategory": "sliding_window",
        "instruction": "Find the minimal length of a contiguous subarray of which the sum is at least target in Python.",
        "response": build_reasoning_response(
            strategy=(
                "Since all elements are positive, adding elements monotonically increases the sum. "
                "Use a sliding window [start, end]. Expand `end` to increase the running sum. "
                "Whenever current_sum >= target, update min_len and contract `start` to seek a smaller valid window."
            ),
            edge_cases=[
                "Total sum of all elements < target: return 0.",
                "Single element >= target: minimum length is immediately 1.",
                "Empty array: returns 0."
            ],
            code=(
                "def min_subarray_len(target: int, nums: list[int]) -> int:\n"
                "    start = 0\n"
                "    curr_sum = 0\n"
                "    min_length = float('inf')\n"
                "    \n"
                "    for end in range(len(nums)):\n"
                "        curr_sum += nums[end]\n"
                "        while curr_sum >= target:\n"
                "            min_length = min(min_length, end - start + 1)\n"
                "            curr_sum -= nums[start]\n"
                "            start += 1\n"
                "            \n"
                "    return min_length if min_length != float('inf') else 0\n"
                "\n"
                "# Verification assertions\n"
                "assert min_subarray_len(7, [2, 3, 1, 2, 4, 3]) == 2\n"
                "assert min_subarray_len(4, [1, 4, 4]) == 1\n"
                "assert min_subarray_len(11, [1, 1, 1, 1, 1]) == 0\n"
            ),
            time_complexity="O(N) since each pointer advances at most N times.",
            space_complexity="O(1) auxiliary variables."
