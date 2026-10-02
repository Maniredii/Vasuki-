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
                "    if len(height) < 3:\n"
                "        return 0\n"
                "    \n"
                "    left, right = 0, len(height) - 1\n"
                "    left_max = right_max = 0\n"
                "    total_water = 0\n"
                "    \n"
                "    while left < right:\n"
                "        if height[left] <= height[right]:\n"
                "            if height[left] >= left_max:\n"
                "                left_max = height[left]\n"
                "            else:\n"
                "                total_water += left_max - height[left]\n"
                "            left += 1\n"
                "        else:\n"
                "            if height[right] >= right_max:\n"
                "                right_max = height[right]\n"
                "            else:\n"
                "                total_water += right_max - height[right]\n"
                "            right -= 1\n"
                "            \n"
                "    return total_water\n"
                "\n"
                "# Verification assertions\n"
                "assert trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6\n"
                "assert trap_rain_water([4, 2, 0, 3, 2, 5]) == 9\n"
                "assert trap_rain_water([1, 2, 3, 4]) == 0\n"
                "assert trap_rain_water([]) == 0\n"
            ),
            time_complexity="O(N) single pass across array of length N.",
            space_complexity="O(1) auxiliary variables only."
        )
    })

    # 2. Sliding Window: Longest Substring Without Repeating Characters
    records.append({
        "id": "cot_algo_0002",
        "category": "algorithmic_reasoning",
        "subcategory": "sliding_window",
        "instruction": "Implement a Python function to find the length of the longest substring without repeating characters.",
        "response": build_reasoning_response(
            strategy=(
                "Use a sliding window [start, end] tracked with a hash map recording each character's "
                "most recent index. When character s[end] was seen at index >= start, we jump `start` "
                "directly to last_seen[char] + 1, eliminating redundant pointer increments."
            ),
            edge_cases=[
                "Empty string: returns 0.",
                "All identical characters (e.g. 'bbbbb'): window collapses to 1.",
                "All distinct characters: window spans the entire string length."
            ],
            code=(
                "def length_of_longest_substring(s: str) -> int:\n"
                "    last_seen = {}\n"
                "    start = 0\n"
                "    max_len = 0\n"
                "    \n"
                "    for end, char in enumerate(s):\n"
                "        if char in last_seen and last_seen[char] >= start:\n"
                "            start = last_seen[char] + 1\n"
