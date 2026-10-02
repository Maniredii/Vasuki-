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
        )
    })

    # 2. Binary Search: Find Minimum in Rotated Sorted Array
    recs.append({
        "id": "algo_cot_002",
        "category": "algorithmic_reasoning",
        "subcategory": "binary_search",
        "instruction": "Write a Python function to find the minimum element in a rotated sorted array of unique elements in O(log n).",
        "response": build_reasoning_response(
            strategy=(
                "Compare midpoint nums[mid] with the rightmost element nums[right]. "
                "If nums[mid] > nums[right], the inflection pivot (minimum) must reside strictly in the right half (left = mid + 1). "
                "If nums[mid] < nums[right], mid could be the minimum, so search left half including mid (right = mid). "
                "Convergence occurs when left == right."
            ),
            edge_cases=[
                "Array not rotated: first element is minimum.",
                "Array of size 1: returns nums[0].",
                "Array rotated n-1 times: minimum element is at index 0 or 1."
            ],
            code=(
                "def find_min_rotated(nums: list[int]) -> int:\n"
                "    left, right = 0, len(nums) - 1\n"
                "    while left < right:\n"
                "        mid = (left + right) // 2\n"
                "        if nums[mid] > nums[right]:\n"
                "            left = mid + 1\n"
                "        else:\n"
                "            right = mid\n"
                "    return nums[left]\n"
                "\n"
                "# Verification assertions\n"
                "assert find_min_rotated([3, 4, 5, 1, 2]) == 1\n"
                "assert find_min_rotated([4, 5, 6, 7, 0, 1, 2]) == 0\n"
                "assert find_min_rotated([11, 13, 15, 17]) == 11\n"
                "assert find_min_rotated([1]) == 1\n"
            ),
            time_complexity="O(log N) binary search halving intervals.",
            space_complexity="O(1) auxiliary space."
        )
    })

    # 3. Dynamic Programming: Longest Increasing Subsequence (LIS)
    recs.append({
        "id": "algo_cot_003",
        "category": "algorithmic_reasoning",
        "subcategory": "dynamic_programming",
        "instruction": "Implement an optimal O(n log n) algorithm in Python to compute the length of the Longest Increasing Subsequence.",
        "response": build_reasoning_response(
            strategy=(
                "Patience sorting approach. Maintain an array `tails` where tails[i] stores the smallest tail "
                "of all increasing subsequences of length i+1 found so far. "
                "For each number x in nums, binary search (using `bisect.bisect_left`) for x in `tails`. "
                "If x is greater than all elements, append it. Otherwise, update the smallest tail >= x."
            ),
            edge_cases=[
                "Empty array: returns 0.",
                "Strictly decreasing array: tails stays length 1, returns 1.",
                "Array with duplicates: bisect_left replaces duplicate element, preserving strictly increasing condition."
            ],
            code=(
                "import bisect\n"
                "\n"
                "def length_of_lis(nums: list[int]) -> int:\n"
                "    if not nums:\n"
                "        return 0\n"
                "        \n"
                "    tails = []\n"
                "    for x in nums:\n"
                "        idx = bisect.bisect_left(tails, x)\n"
                "        if idx == len(tails):\n"
                "            tails.append(x)\n"
                "        else:\n"
                "            tails[idx] = x\n"
                "            \n"
                "    return len(tails)\n"
                "\n"
                "# Verification assertions\n"
                "assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4\n"
                "assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4\n"
                "assert length_of_lis([7, 7, 7, 7, 7]) == 1\n"
                "assert length_of_lis([]) == 0\n"
            ),
            time_complexity="O(N log N) across N elements with log N binary search lookups.",
            space_complexity="O(N) in worst case for tails array."
        )
    })

    # 4. Graphs: Dijkstra's Shortest Path Algorithm
    recs.append({
        "id": "algo_cot_004",
        "category": "algorithmic_reasoning",
        "subcategory": "graph_theory",
        "instruction": "Implement Dijkstra's algorithm in Python using a min-heap to find the shortest path from a source node.",
        "response": build_reasoning_response(
            strategy=(
                "Dijkstra's algorithm finds shortest paths in a weighted graph with non-negative weights. "
                "Initialize distances to infinity, source distance to 0. "
                "Use Python's `heapq` as a priority queue storing tuples (current_dist, u). "
                "When popping (d, u), if d > dist[u], skip it (stale heap entry). "
                "Otherwise, relax adjacent edges (u, v, weight) and push improved distances."
            ),
            edge_cases=[
                "Disconnected nodes: distance remains infinity.",
                "Source with no outgoing edges: source distance 0, others infinity.",
                "Multiple parallel edges: min-heap naturally selects minimum weight edge."
            ],
            code=(
                "import heapq\n"
                "\n"
                "def dijkstra(num_nodes: int, edges: list[tuple[int, int, int]], source: int) -> dict[int, int]:\n"
                "    adj = {i: [] for i in range(num_nodes)}\n"
                "    for u, v, w in edges:\n"
                "        adj[u].append((v, w))\n"
                "        \n"
                "    distances = {i: float('inf') for i in range(num_nodes)}\n"
                "    distances[source] = 0\n"
                "    pq = [(0, source)]\n"
                "    \n"
                "    while pq:\n"
                "        curr_d, u = heapq.heappop(pq)\n"
                "        if curr_d > distances[u]:\n"
                "            continue\n"
                "            \n"
                "        for v, weight in adj[u]:\n"
                "            new_d = curr_d + weight\n"
                "            if new_d < distances[v]:\n"
                "                distances[v] = new_d\n"
                "                heapq.heappush(pq, (new_d, v))\n"
                "                \n"
                "    return distances\n"
                "\n"
                "# Verification assertions\n"
                "edges = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5)]\n"
                "dists = dijkstra(4, edges, 0)\n"
                "assert dists[0] == 0\n"
                "assert dists[1] == 3  # via 0 -> 2 -> 1\n"
                "assert dists[3] == 4  # via 0 -> 2 -> 1 -> 3\n"
            ),
            time_complexity="O((V + E) log V) with min-heap operations.",
            space_complexity="O(V + E) for adjacency list and priority queue."
        )
    })

    # 5. Data Structures: LRU Cache Implementation
    recs.append({
        "id": "algo_cot_005",
        "category": "algorithmic_reasoning",
        "subcategory": "data_structures",
        "instruction": "Implement an LRU (Least Recently Used) Cache in Python with O(1) get and put operations.",
        "response": build_reasoning_response(
            strategy=(
                "To achieve O(1) for both retrieval and order updates, combine a hash map with a doubly linked list. "
                "Python's `collections.OrderedDict` internally maintains this exact structure: a dict mapping keys to nodes, "
                "with an internal circular doubly linked list. "
                "`move_to_end(key)` marks an accessed item as most recent in O(1). "
                "`popitem(last=False)` evicts the least recently used item from the front in O(1)."
            ),
            edge_cases=[
                "Putting an existing key: update value and move to most recent end.",
                "Capacity of 1: correctly evicts previous item on new insertion.",
                "Getting non-existent key: returns -1 without altering state."
            ],
            code=(
                "from collections import OrderedDict\n"
                "\n"
                "class LRUCache:\n"
                "    def __init__(self, capacity: int):\n"
                "        self.capacity = capacity\n"
                "        self.cache = OrderedDict()\n"
                "\n"
                "    def get(self, key: int) -> int:\n"
                "        if key not in self.cache:\n"
                "            return -1\n"
                "        self.cache.move_to_end(key)\n"
                "        return self.cache[key]\n"
                "\n"
                "    def put(self, key: int, value: int) -> None:\n"
                "        if key in self.cache:\n"
                "            self.cache.move_to_end(key)\n"
                "        self.cache[key] = value\n"
                "        if len(self.cache) > self.capacity:\n"
                "            self.cache.popitem(last=False)  # Evict oldest (front)\n"
                "\n"
                "# Verification assertions\n"
                "lru = LRUCache(2)\n"
                "lru.put(1, 1)\n"
                "lru.put(2, 2)\n"
                "assert lru.get(1) == 1       # 1 becomes most recently used\n"
                "lru.put(3, 3)                # Evicts key 2\n"
                "assert lru.get(2) == -1      # 2 was evicted\n"
                "lru.put(4, 4)                # Evicts key 1\n"
                "assert lru.get(1) == -1\n"
                "assert lru.get(3) == 3\n"
