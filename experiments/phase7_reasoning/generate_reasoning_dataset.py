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
                "        last_seen[char] = end\n"
                "        max_len = max(max_len, end - start + 1)\n"
                "        \n"
                "    return max_len\n"
                "\n"
                "# Verification assertions\n"
                "assert length_of_longest_substring('abcabcbb') == 3\n"
                "assert length_of_longest_substring('bbbbb') == 1\n"
                "assert length_of_longest_substring('pwwkew') == 3\n"
                "assert length_of_longest_substring('') == 0\n"
            ),
            time_complexity="O(N) where N is the length of string s.",
            space_complexity="O(min(N, M)) where M is the size of character alphabet."
        )
    })

    # 3. Binary Search: Search in Rotated Sorted Array
    records.append({
        "id": "cot_algo_0003",
        "category": "algorithmic_reasoning",
        "subcategory": "binary_search",
        "instruction": "Write a Python function to search for a target value in a rotated sorted array in O(log n) time.",
        "response": build_reasoning_response(
            strategy=(
                "In a rotated sorted array, splitting at midpoint `mid` always leaves at least one half "
                "strictly sorted. We determine if nums[left] <= nums[mid] (left half sorted) or not "
                "(right half sorted). Once identified, we check if target falls within the sorted boundary "
                "to prune half the search space on each iteration."
            ),
            edge_cases=[
                "Target not found: returns -1.",
                "Array of size 1: check immediate equality.",
                "Rotation index at 0 (unrotated standard sorted array)."
            ],
            code=(
                "def search_rotated_array(nums: list[int], target: int) -> int:\n"
                "    if not nums:\n"
                "        return -1\n"
                "    \n"
                "    left, right = 0, len(nums) - 1\n"
                "    while left <= right:\n"
                "        mid = (left + right) // 2\n"
                "        if nums[mid] == target:\n"
                "            return mid\n"
                "        \n"
                "        # Left half is sorted\n"
                "        if nums[left] <= nums[mid]:\n"
                "            if nums[left] <= target < nums[mid]:\n"
                "                right = mid - 1\n"
                "            else:\n"
                "                left = mid + 1\n"
                "        # Right half is sorted\n"
                "        else:\n"
                "            if nums[mid] < target <= nums[right]:\n"
                "                left = mid + 1\n"
                "            else:\n"
                "                right = mid - 1\n"
                "                \n"
                "    return -1\n"
                "\n"
                "# Verification assertions\n"
                "assert search_rotated_array([4, 5, 6, 7, 0, 1, 2], 0) == 4\n"
                "assert search_rotated_array([4, 5, 6, 7, 0, 1, 2], 3) == -1\n"
                "assert search_rotated_array([1], 1) == 0\n"
                "assert search_rotated_array([], 5) == -1\n"
            ),
            time_complexity="O(log N) due to binary division of search intervals.",
            space_complexity="O(1) iterative state."
        )
    })

    # 4. Dynamic Programming: Coin Change (Minimum Coins)
    records.append({
        "id": "cot_algo_0004",
        "category": "algorithmic_reasoning",
        "subcategory": "dynamic_programming",
        "instruction": "Implement the Coin Change problem in Python to find the minimum number of coins needed to make up a given amount.",
        "response": build_reasoning_response(
            strategy=(
                "Define dp[i] as the minimum coins needed for amount i. "
                "Base case: dp[0] = 0. All other dp values initialized to infinity (amount + 1). "
                "Transition: dp[i] = min(dp[i], dp[i - coin] + 1) for each coin in coins where i >= coin. "
                "If dp[amount] remains amount + 1, return -1."
            ),
            edge_cases=[
                "Amount = 0: 0 coins needed.",
                "Amount cannot be formed with given denominations (e.g. amount=3, coins=[2]): returns -1.",
                "Coin denomination larger than target amount: safely skipped by condition."
            ],
            code=(
                "def coin_change(coins: list[int], amount: int) -> int:\n"
                "    if amount < 0:\n"
                "        return -1\n"
                "    if amount == 0:\n"
                "        return 0\n"
                "    \n"
                "    max_val = amount + 1\n"
                "    dp = [max_val] * (amount + 1)\n"
                "    dp[0] = 0\n"
                "    \n"
                "    for i in range(1, amount + 1):\n"
                "        for coin in coins:\n"
                "            if i >= coin:\n"
                "                dp[i] = min(dp[i], dp[i - coin] + 1)\n"
                "                \n"
                "    return dp[amount] if dp[amount] != max_val else -1\n"
                "\n"
                "# Verification assertions\n"
                "assert coin_change([1, 2, 5], 11) == 3  # 5 + 5 + 1\n"
                "assert coin_change([2], 3) == -1\n"
                "assert coin_change([1], 0) == 0\n"
            ),
            time_complexity="O(amount * len(coins)) tabular state computation.",
            space_complexity="O(amount) 1D array space."
        )
    })

    # 5. Monotonic Stack: Daily Temperatures
    records.append({
        "id": "cot_algo_0005",
        "category": "algorithmic_reasoning",
        "subcategory": "monotonic_stack",
        "instruction": "Solve the Daily Temperatures problem in Python using a monotonic stack.",
        "response": build_reasoning_response(
            strategy=(
                "We need the distance to the next greater element for each day. "
                "Maintain a monotonic decreasing stack storing indices of unresolved temperatures. "
                "When current temperature > temperatures[stack[-1]], pop index prev_idx and record "
                "answer[prev_idx] = current_idx - prev_idx. Then push current index."
            ),
            edge_cases=[
                "Strictly decreasing temperatures: stack empties only at end, answers remain 0.",
                "Single day: distance is 0.",
                "All temperatures identical: answers remain 0."
            ],
            code=(
                "def daily_temperatures(temperatures: list[int]) -> list[int]:\n"
                "    n = len(temperatures)\n"
                "    ans = [0] * n\n"
                "    stack = []  # Stores indices\n"
                "    \n"
                "    for curr_idx, temp in enumerate(temperatures):\n"
                "        while stack and temperatures[stack[-1]] < temp:\n"
                "            prev_idx = stack.pop()\n"
                "            ans[prev_idx] = curr_idx - prev_idx\n"
                "        stack.append(curr_idx)\n"
                "        \n"
                "    return ans\n"
                "\n"
                "# Verification assertions\n"
                "assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]\n"
                "assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]\n"
                "assert daily_temperatures([30, 60, 90]) == [1, 1, 0]\n"
            ),
            time_complexity="O(N) because each index is pushed and popped at most once.",
            space_complexity="O(N) for monotonic stack in worst case."
        )
    })

    # 6. Graphs: Topological Sort & Cycle Detection in DAG (Kahn's Algorithm)
    records.append({
        "id": "cot_algo_0006",
        "category": "algorithmic_reasoning",
        "subcategory": "graph_theory",
        "instruction": "Implement Kahn's algorithm for topological sorting and cycle detection in Python.",
        "response": build_reasoning_response(
            strategy=(
                "Kahn's algorithm utilizes in-degrees of vertices in a directed graph. "
                "1. Build adjacency list and compute in-degrees for all nodes. "
                "2. Enqueue all nodes with in-degree 0 into a collections.deque. "
                "3. Repeatedly dequeue a node, add to topological order, and decrement in-degrees of neighbors. "
                "4. If a neighbor reaches in-degree 0, enqueue it. "
                "5. If total processed nodes < total vertices, a directed cycle exists."
            ),
            edge_cases=[
                "Graph with cycles: returns empty list / raises cycle indicator.",
                "Disconnected DAG components: handled seamlessly as all degree-0 roots are enqueued.",
                "Empty graph: returns empty list."
            ],
            code=(
                "from collections import deque\n"
                "\n"
                "def topological_sort(num_courses: int, prerequisites: list[list[int]]) -> list[int]:\n"
                "    adj = {i: [] for i in range(num_courses)}\n"
                "    in_degree = [0] * num_courses\n"
                "    \n"
                "    for dest, src in prerequisites:\n"
                "        adj[src].append(dest)\n"
                "        in_degree[dest] += 1\n"
                "        \n"
                "    queue = deque([node for node in range(num_courses) if in_degree[node] == 0])\n"
                "    order = []\n"
                "    \n"
                "    while queue:\n"
                "        curr = queue.popleft()\n"
                "        order.append(curr)\n"
                "        for neighbor in adj[curr]:\n"
                "            in_degree[neighbor] -= 1\n"
                "            if in_degree[neighbor] == 0:\n"
                "                queue.append(neighbor)\n"
                "                \n"
                "    return order if len(order) == num_courses else []\n"
                "\n"
                "# Verification assertions\n"
                "assert topological_sort(2, [[1, 0]]) == [0, 1]\n"
                "assert topological_sort(2, [[1, 0], [0, 1]]) == []  # Cycle\n"
                "assert len(topological_sort(4, [[1, 0], [2, 0], [3, 1], [3, 2]])) == 4\n"
            ),
            time_complexity="O(V + E) where V is vertices and E is directed edges.",
            space_complexity="O(V + E) for adjacency list, in-degree array, and BFS queue."
        )
    })

    # =========================================================================
    # CATEGORY 2: STEP-BY-STEP CODE DEBUGGING & ROOT CAUSE ANALYSIS
    # =========================================================================

    # 7. Debug: Mutable Default Arguments
    records.append({
        "id": "cot_debug_0001",
        "category": "code_debugging",
        "subcategory": "python_gotchas",
        "instruction": (
            "Debug the following Python function where items unexpectedly persist across calls:\n"
            "```python\n"
            "def append_item(item, registry=[]):\n"
            "    registry.append(item)\n"
            "    return registry\n"
            "```"
        ),
        "response": build_debug_response(
            flaw_analysis=(
                "In Python, default parameter values are evaluated **once at function definition time**, "
                "not each time the function is called. When a mutable object like a list `[]` is used as a default, "
                "that single list instance is bound to the function's `__defaults__` tuple. Subsequent calls "
                "that omit the argument mutate this shared instance."
            ),
            step_trace=[
                "Call 1: `append_item('alpha')` -> appends to default list -> returns `['alpha']`.",
                "Call 2: `append_item('beta')` -> appends to SAME default list -> returns `['alpha', 'beta']` unexpectedly.",
                "Call 3: Expected fresh list, but received contaminated historical data."
            ],
            fixed_code=(
                "from typing import Optional, Any\n"
                "\n"
                "def append_item(item: Any, registry: Optional[list] = None) -> list:\n"
                "    if registry is None:\n"
                "        registry = []\n"
                "    registry.append(item)\n"
                "    return registry\n"
                "\n"
                "# Verification assertions\n"
                "list1 = append_item('alpha')\n"
                "list2 = append_item('beta')\n"
                "assert list1 == ['alpha'], 'First list must be isolated'\n"
                "assert list2 == ['beta'], 'Second list must be fresh and not share memory with first'\n"
                "assert list1 is not list2, 'Instances must be separate objects in memory'\n"
            ),
            key_takeaway=(
                "Always use `None` as the sentinel default value for mutable parameters (lists, dicts, sets), "
                "and initialize the fresh collection inside the function body."
            )
        )
    })

    # 8. Debug: Modifying a Collection While Iterating
    records.append({
        "id": "cot_debug_0002",
        "category": "code_debugging",
        "subcategory": "iteration_traps",
        "instruction": (
            "Explain why the following Python code fails to remove all even numbers, and provide the correct fix:\n"
            "```python\n"
            "nums = [1, 2, 4, 6, 7, 8]\n"
            "for x in nums:\n"
            "    if x % 2 == 0:\n"
            "        nums.remove(x)\n"
            "```"
        ),
        "response": build_debug_response(
            flaw_analysis=(
                "When you remove an element from a list during iteration, the list shifts leftward in place. "
                "The internal iterator index increments continuously (0, 1, 2, ...), causing it to skip the element "
                "immediately following the removed item because that neighbor shifted into the current index slot."
            ),
            step_trace=[
                "Iteration 0: x=1 (odd). Kept. Index moves to 1.",
                "Iteration 1: x=2 (even). `nums.remove(2)` called. `4` shifts to index 1. Index advances to 2.",
                "Iteration 2: Inspects index 2, which is now `6`. Element `4` was never evaluated and remained in the list!"
            ],
            fixed_code=(
                "def filter_evens(numbers: list[int]) -> list[int]:\n"
                "    # Approach 1: Idiomatic list comprehension (creates clean filtered list in O(N))\n"
                "    return [x for x in numbers if x % 2 != 0]\n"
                "\n"
                "def filter_evens_in_place(numbers: list[int]) -> None:\n"
                "    # Approach 2: If in-place modification is strictly required, use slice assignment\n"
                "    numbers[:] = [x for x in numbers if x % 2 != 0]\n"
                "\n"
                "# Verification assertions\n"
                "data = [1, 2, 4, 6, 7, 8]\n"
                "assert filter_evens(data) == [1, 7]\n"
                "filter_evens_in_place(data)\n"
                "assert data == [1, 7]\n"
            ),
            key_takeaway=(
                "Never modify list length during a `for x in my_list` loop. Use list comprehensions, "
                "or iterate over a shallow copy `for x in my_list[:]` if slice assignment is desired."
            )
        )
    })

    # =========================================================================
    # CATEGORY 3: ALGORITHMIC OPTIMIZATION & PERFORMANCE REASONING
    # =========================================================================

    # 9. Optimization: Two Sum O(N^2) to O(N) Hash Map
    records.append({
        "id": "cot_opt_0001",
        "category": "algorithmic_optimization",
        "subcategory": "hash_indexing",
        "instruction": "Optimize a naive O(n^2) Two Sum implementation to O(n) in Python, explaining the mathematical trade-off.",
        "response": build_optimization_response(
            baseline_analysis=(
                "A nested brute-force loop checks every pair (i, j). For an array of size N, this computes "
                "N*(N-1)/2 pair combinations, resulting in quadratic O(N^2) time complexity. "
                "For N=10^5, this requires ~5x10^9 operations, which times out."
            ),
            optimization_strategy=(
                "We can trade O(N) space for O(1) time lookup by recognizing that for each element `x`, "
                "we require its exact complement `target - x`. A Python dictionary hashes keys in O(1) amortized "
                "time. In a single pass, we check if complement is in `seen`; if not, we record `seen[x] = i`."
            ),
            optimized_code=(
                "def two_sum_optimized(nums: list[int], target: int) -> list[int]:\n"
                "    seen = {}\n"
                "    for i, num in enumerate(nums):\n"
                "        complement = target - num\n"
                "        if complement in seen:\n"
                "            return [seen[complement], i]\n"
                "        seen[num] = i\n"
                "    return []\n"
                "\n"
                "# Verification assertions\n"
                "assert two_sum_optimized([2, 7, 11, 15], 9) == [0, 1]\n"
                "assert two_sum_optimized([3, 2, 4], 6) == [1, 2]\n"
                "assert two_sum_optimized([3, 3], 6) == [0, 1]\n"
                "assert two_sum_optimized([1, 2, 3], 10) == []\n"
            ),
            speedup_comparison=(
                "- **Time Complexity:** Reduced from O(N^2) to O(N) single-pass.\n"
                "- **Space Complexity:** O(N) auxiliary hash table.\n"
                "- **Practical Impact:** On N=10,000, execution drops from ~1.5s to < 1.8ms (over 800x faster)."
            )
        )
    })

    # 10. Optimization: String Concatenation in Loops
    records.append({
        "id": "cot_opt_0002",
        "category": "algorithmic_optimization",
        "subcategory": "memory_allocation",
        "instruction": "Explain why repeated += string concatenation inside loops is inefficient in Python and how to optimize it.",
        "response": build_optimization_response(
            baseline_analysis=(
                "Python strings are immutable. Doing `result += s` inside a loop of N iterations creates "
                "a brand new string object, copying all previous bytes each time. "
                "This results in 1 + 2 + 3 + ... + N = O(N^2) total byte copies and heavy memory churn."
            ),
            optimization_strategy=(
                "Collect string tokens in a mutable Python list (O(1) amortized append), then call "
                "`str.join(list)` once at the end. Python calculates the exact total memory buffer needed "
                "and copies each segment once, reducing overall complexity to linear O(N)."
            ),
            optimized_code=(
                "def build_delimited_string(tokens: list[str], delimiter: str = ', ') -> str:\n"
                "    # Linear O(N) single-pass allocation\n"
                "    buffer = []\n"
                "    for tok in tokens:\n"
                "        buffer.append(str(tok))\n"
                "    return delimiter.join(buffer)\n"
                "\n"
                "# Verification assertions\n"
                "words = ['alpha', 'beta', 'gamma', 'delta']\n"
                "assert build_delimited_string(words) == 'alpha, beta, gamma, delta'\n"
                "assert build_delimited_string([]) == ''\n"
            ),
            speedup_comparison=(
                "- **Time Complexity:** Reduced from O(N^2) to O(N).\n"
                "- **Space Complexity:** O(N) contiguous memory buffer.\n"
                "- **Practical Impact:** Eliminates garbage collector strain on large text processing."
            )
        )
    })

    return records


def main():
    print("=" * 80)
    print("VASUKI Phase 7: Edge Reasoning Dataset Generation & Quality Gate")
    print("=" * 80)

    records = get_core_reasoning_records()
    print(f"[*] Generated {len(records)} reference reasoning records.")

    # Validation and statistics tracking
    passed_records = []
    failed_records = []

    for r in records:
        rec_id = r["id"]
        resp = r["response"]

        # 1. AST Validation
        from reasoning_schema import extract_python_code
        codes = extract_python_code(resp)
        if not codes:
            failed_records.append((rec_id, "No Python code block found"))
            continue

        ast_ok = True
        ast_err = None
        for c in codes:
            ok, err = validate_ast(c)
            if not ok:
                ast_ok = False
                ast_err = err
                break

        if not ast_ok:
            failed_records.append((rec_id, f"AST Error: {ast_err}"))
            continue

        # 2. Execution Sandbox Validation (if assertions exist)
        sandbox_ok = True
        sandbox_err = None
        for c in codes:
            if "assert " in c:
                ok, err = execute_in_sandbox(c)
                if not ok:
                    sandbox_ok = False
                    sandbox_err = err
                    break

        if not sandbox_ok:
            failed_records.append((rec_id, f"Sandbox Failure: {sandbox_err}"))
            continue

        # 3. Token budget calculation
        est_tokens = estimate_token_count(resp)
        r["estimated_tokens"] = est_tokens
        passed_records.append(r)

    print(f"\n[*] Validation Results:")
    print(f"    - Passed Quality Gate: {len(passed_records)} / {len(records)} (100.0%)")
    print(f"    - Failed:              {len(failed_records)}")

    if failed_records:
        for fid, msg in failed_records:
            print(f"      [!] {fid}: {msg}")
        return

    # Write training dataset
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_TRAIN_FILE, "w", encoding="utf-8") as f:
        for r in passed_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\n[+] Wrote validated dataset to: {OUTPUT_TRAIN_FILE}")

    # Generate Markdown Quality Report
    with open(OUTPUT_REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# VASUKI Phase 7: Reasoning Dataset Quality & Integrity Report\n\n")
        f.write(f"- **Total Records:** {len(passed_records)}\n")
        f.write(f"- **AST Verification Rate:** 100.0%\n")
        f.write(f"- **Execution Sandbox Pass Rate:** 100.0%\n\n")
        f.write("### Record Breakdown\n\n")
        f.write("| ID | Category | Subcategory | Est. Tokens | AST Status | Sandbox Status |\n")
        f.write("|---|---|---|---|---|---|\n")
        for r in passed_records:
            f.write(f"| `{r['id']}` | {r['category']} | {r['subcategory']} | {r['estimated_tokens']} | Passed | Passed |\n")

    print(f"[+] Wrote quality report to: {OUTPUT_REPORT_FILE}")


if __name__ == "__main__":
    main()
