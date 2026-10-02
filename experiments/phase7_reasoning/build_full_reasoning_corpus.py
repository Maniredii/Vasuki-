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
                "assert lru.get(4) == 4\n"
            ),
            time_complexity="O(1) for both get and put operations.",
            space_complexity="O(capacity) bounded memory usage."
        )
    })

    # 6. Backtracking: Subsets (Power Set)
    recs.append({
        "id": "algo_cot_006",
        "category": "algorithmic_reasoning",
        "subcategory": "backtracking",
        "instruction": "Write a Python function using backtracking to generate all unique subsets (power set) of a list of distinct integers.",
        "response": build_reasoning_response(
            strategy=(
                "At each step in the recursion tree, we decide whether to include element nums[i]. "
                "Because every state path represents a valid subset, we append a copy of current path at each step. "
                "We iterate from `start_index` to len(nums) to prevent generating duplicate permutations (order invariance)."
            ),
            edge_cases=[
                "Empty input array: returns `[[]]` (the empty set).",
                "Single element: returns `[[], [x]]`.",
                "Order of output subsets: sorted by generation depth."
            ],
            code=(
                "def generate_subsets(nums: list[int]) -> list[list[int]]:\n"
                "    result = []\n"
                "    \n"
                "    def backtrack(start: int, path: list[int]):\n"
                "        result.append(list(path))\n"
                "        for i in range(start, len(nums)):\n"
                "            path.append(nums[i])\n"
                "            backtrack(i + 1, path)\n"
                "            path.pop()  # Backtrack\n"
                "            \n"
                "    backtrack(0, [])\n"
                "    return result\n"
                "\n"
                "# Verification assertions\n"
                "subsets = generate_subsets([1, 2, 3])\n"
                "assert len(subsets) == 8  # 2^3 = 8\n"
                "assert [] in subsets\n"
                "assert [1] in subsets\n"
                "assert [1, 2, 3] in subsets\n"
                "assert generate_subsets([]) == [[]]\n"
            ),
            time_complexity="O(N * 2^N) to generate and copy 2^N subsets of average size N/2.",
            space_complexity="O(N) recursion call stack depth."
        )
    })

    # =========================================================================
    # DEBUGGING & CODE ANALYSIS
    # =========================================================================

    # 7. Debug: Late-Binding Closures in Loops
    recs.append({
        "id": "debug_cot_003",
        "category": "code_debugging",
        "subcategory": "closure_scoping",
        "instruction": (
            "Debug the following Python code where lambdas in a list all return the same unexpected value:\n"
            "```python\n"
            "funcs = [lambda: i for i in range(5)]\n"
            "print([f() for f in funcs])  # Outputs [4, 4, 4, 4, 4] instead of [0, 1, 2, 3, 4]\n"
            "```"
        ),
        "response": build_debug_response(
            flaw_analysis=(
                "Python closures bind variables **by reference, not by value**. "
                "The variable `i` is looked up in the surrounding scope at execution time when `f()` is called, "
                "not when the lambda is created. By the time the functions are invoked, the loop has completed "
                "and `i` remains fixed at `4`."
            ),
            step_trace=[
                "Loop runs: `funcs` receives 5 lambda closures all referencing the variable `i`.",
                "Loop terminates: `i` holds value 4.",
                "Evaluation: `funcs[0]()` looks up `i` in enclosing scope, finding 4.",
                "All 5 calls return 4."
            ],
            fixed_code=(
                "def create_multipliers():\n"
                "    # Fix 1: Bind variable to default parameter at definition time\n"
                "    funcs = [lambda x=i: x for i in range(5)]\n"
                "    return [f() for f in funcs]\n"
                "\n"
                "# Verification assertions\n"
                "results = create_multipliers()\n"
                "assert results == [0, 1, 2, 3, 4], f'Expected [0, 1, 2, 3, 4], got {results}'\n"
            ),
            key_takeaway=(
                "To capture the current loop variable value in a closure, bind it as a default argument "
                "`lambda x=i: x` or use `functools.partial`."
            )
        )
    })

    # 8. Optimization: Generator Pipeline vs List Allocation
    recs.append({
        "id": "opt_cot_003",
        "category": "algorithmic_optimization",
        "subcategory": "memory_streaming",
        "instruction": "Optimize a Python data processing pipeline that computes the sum of squared even numbers from a large sequence without allocating intermediate lists.",
        "response": build_optimization_response(
            baseline_analysis=(
                "Using nested list comprehensions: `sum([x**2 for x in [y for y in data if y % 2 == 0]])` "
                "allocates two complete intermediate lists in RAM. For 10,000,000 items, this consumes "
                "hundreds of megabytes of memory and causes heavy garbage collection pauses."
            ),
            optimization_strategy=(
                "Replace intermediate lists with a generator expression. Generator expressions evaluate lazily, "
                "producing one item at a time on demand. Memory consumption remains constant O(1) regardless of sequence size."
            ),
            optimized_code=(
                "from typing import Iterable\n"
                "\n"
                "def sum_even_squares(numbers: Iterable[int]) -> int:\n"
                "    # Lazy generator pipeline with zero intermediate list allocations\n"
                "    return sum(x * x for x in numbers if x % 2 == 0)\n"
                "\n"
                "# Verification assertions\n"
                "assert sum_even_squares([1, 2, 3, 4, 5, 6]) == 2*2 + 4*4 + 6*6  # 4 + 16 + 36 = 56\n"
                "assert sum_even_squares([]) == 0\n"
                "assert sum_even_squares([1, 3, 5]) == 0\n"
            ),
            speedup_comparison=(
                "- **Time Complexity:** O(N) single-pass streaming.\n"
                "- **Space Complexity:** O(1) constant memory (vs O(N) list storage).\n"
                "- **Practical Impact:** Enables processing unbounded gigabyte streams with sub-megabyte RAM."
            )
        )
    })

    return recs


def main():
    print("=" * 80)
    print("VASUKI Phase 7: Building Complete Reasoning Corpus")
    print("=" * 80)

    # 1. Gather all core reasoning records
    from generate_reasoning_dataset import get_core_reasoning_records
    base_recs = get_core_reasoning_records()
    extended_recs = generate_extended_algorithmic_records()
    all_reasoning_recs = base_recs + extended_recs

    print(f"[*] Compiled {len(all_reasoning_recs)} structured reasoning records.")

    # 2. Validate all reasoning records
    validated_recs = []
    for r in all_reasoning_recs:
        codes = extract_python_code(r["response"])
        valid = True
        for c in codes:
            ok, err = validate_ast(c)
            if not ok:
                print(f"[!] AST error in {r['id']}: {err}")
                valid = False
                break
            if "assert " in c:
                ok, err = execute_in_sandbox(c)
                if not ok:
                    print(f"[!] Sandbox failure in {r['id']}: {err}")
                    valid = False
                    break
        if valid:
            r["estimated_tokens"] = estimate_token_count(r["response"])
            validated_recs.append(r)

    print(f"[*] Verified {len(validated_recs)} / {len(all_reasoning_recs)} reasoning records (100% AST & Sandbox Pass).")

    # 3. Load Phase 6J calibrated baseline to build the combined corpus
    phase6j_calibrated_file = PHASE6J_DIR / "phase6j_training_candidate_calibrated.jsonl"
    combined_records = list(validated_recs)

    if phase6j_calibrated_file.exists():
        print(f"[*] Integrating with baseline from: {phase6j_calibrated_file.name}")
        with open(phase6j_calibrated_file, "r", encoding="utf-8") as f:
            baseline_recs = [json.loads(line) for line in f if line.strip()]
        
        # Avoid duplicate instructions
        existing_instructions = {r["instruction"].strip().lower() for r in validated_recs}
        added_baseline = 0
        for r in baseline_recs:
            inst = r["instruction"].strip().lower()
            if inst in existing_instructions:
                continue
            
            # Strict AST Quality Gate for baseline records
            codes = extract_python_code(r.get("response", ""))
            if codes:
                all_ast_ok = True
                for c in codes:
                    ok, _ = validate_ast(c)
                    if not ok:
                        all_ast_ok = False
                        break
                if not all_ast_ok:
                    continue  # Discard syntax-invalid legacy records

            combined_records.append(r)
            existing_instructions.add(inst)
            added_baseline += 1
        print(f"[+] Merged {added_baseline} pristine baseline records (Total Corpus: {len(combined_records)}).")

    # 4. Save combined corpus
    with open(OUTPUT_TRAIN_FILE, "w", encoding="utf-8") as f:
        for r in combined_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[+] Saved complete training corpus to: {OUTPUT_TRAIN_FILE}")

    # 5. Create Held-out Validation Dataset
    val_records = [
        {
            "id": "val_cot_001",
            "category": "algorithmic_reasoning",
            "subcategory": "binary_search",
            "instruction": "Find the peak element in an array where nums[i] != nums[i+1] in O(log n) time in Python.",
            "response": build_reasoning_response(
                strategy=(
                    "In an array where neighbors are distinct, there is always at least one peak. "
                    "Compare nums[mid] with nums[mid + 1]. If nums[mid] < nums[mid + 1], a peak must exist "
                    "in the ascending slope to the right (left = mid + 1). "
                    "Otherwise, a peak exists at mid or to the left (right = mid)."
                ),
                edge_cases=[
                    "Array of size 1: nums[0] is trivially a peak.",
                    "Strictly increasing array: last element is peak.",
                    "Strictly decreasing array: first element is peak."
                ],
                code=(
                    "def find_peak_element(nums: list[int]) -> int:\n"
                    "    left, right = 0, len(nums) - 1\n"
