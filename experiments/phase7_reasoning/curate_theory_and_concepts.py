"""
VASUKI Phase 7.1: Multi-Source Theory, Concept & Reasoning Curator
Integrates:
1. sahil2801/CodeAlpaca-20k (Pure conceptual & theoretical CS/Python questions)
2. mlabonne/Evol-Instruct-Python-1k (Algorithmic reasoning & trade-offs)
3. Custom Concise Definition & ML Theory Pack (Solves subword loop collapse on short prompts)
4. Existing Phase 7 Verified Reasoning & Algorithmic Corpus (2,571 records)
"""

import sys
import os
import json
import re
from pathlib import Path
from datasets import load_dataset

from reasoning_schema import validate_ast, extract_python_code, estimate_token_count

BASE_DIR = Path("D:/VASUKI/experiments/phase7_reasoning")
CURRENT_CORPUS_FILE = BASE_DIR / "phase7_reasoning_corpus.jsonl"
OUT_THEORY_FILE = BASE_DIR / "curated_hf_theory.jsonl"
OUT_FULL_CORPUS_FILE = BASE_DIR / "phase7_1_balanced_corpus.jsonl"
OUT_REPORT_FILE = BASE_DIR / "phase7_1_curation_report.md"


# ============================================================================
# 1. EXPANDED CONCISE DEFINITION & THEORY PACK
# ============================================================================

CONCISE_THEORY_PACK = [
    {
        "instruction": "explain decision tree in one line",
        "response": "A decision tree is a supervised machine learning model that makes predictions by recursively partitioning feature space along orthogonal, rule-based splits.",
        "category": "machine_learning_concepts"
    },
    {
        "instruction": "explain decision tree",
        "response": (
            "### Concept & Overview\n"
            "A Decision Tree is a supervised machine learning algorithm used for both classification and regression. "
            "It breaks down a complex dataset into smaller subsets by learning simple if-else decision rules inferred from data features.\n\n"
            "### Architectural Components\n"
            "- **Root Node:** The topmost node representing the entire dataset prior to any split.\n"
            "- **Decision / Internal Nodes:** Intermediate nodes evaluating a test condition on a specific feature (e.g., `age > 30` or `income <= 50000`).\n"
            "- **Leaf / Terminal Nodes:** Final output nodes carrying class labels (classification) or continuous numerical values (regression).\n"
            "- **Splitting Metrics:** Evaluated using Gini Impurity or Entropy (Information Gain) for classification, and Mean Squared Error (MSE) for regression.\n\n"
            "### Python Example (Scikit-Learn)\n"
            "```python\n"
            "from sklearn.tree import DecisionTreeClassifier\n"
            "\n"
            "# Initialize tree with depth constraint to prevent overfitting\n"
            "clf = DecisionTreeClassifier(max_depth=4, criterion='gini', random_state=42)\n"
            "clf.fit(X_train, y_train)\n"
            "predictions = clf.predict(X_test)\n"
            "```\n\n"
            "### Key Trade-offs\n"
            "- **Advantages:** White-box interpretability, handles numerical and categorical features, requires zero feature scaling.\n"
            "- **Disadvantages:** High variance and prone to severe overfitting on noisy data without pruning or depth constraints."
        ),
        "category": "machine_learning_concepts"
    },
    {
        "instruction": "what is linked list",
        "response": (
            "### Definition\n"
            "A linked list is a linear collection of data elements called nodes, stored non-contiguously in memory, "
            "where each node points to the next node in sequence via a pointer or reference.\n\n"
            "### Key Components\n"
            "- **Node:** A container with `data` and a `next` pointer.\n"
            "- **Head:** The entry point reference to the first node.\n"
            "- **Tail:** The final node referencing `None`.\n\n"
            "### Core Operations & Complexity\n"
            "- **Insertion at Head:** O(1) time.\n"
            "- **Deletion at Head:** O(1) time.\n"
            "- **Search by Value:** O(N) linear time.\n"
            "- **Access by Index:** O(N) sequential traversal."
        ),
        "category": "data_structures_theory"
    },
    {
        "instruction": "explain linked list in one line",
        "response": "A linked list is a linear data structure composed of non-contiguous nodes, where each node stores a value and a pointer reference to the next node.",
        "category": "data_structures_theory"
    },
    {
        "instruction": "explain binary search in one line",
        "response": "Binary search is an O(log n) algorithm that repeatedly divides a sorted interval in half by comparing the target with the interval's midpoint.",
        "category": "algorithms_theory"
    },
    {
        "instruction": "explain recursion in one line",
        "response": "Recursion is a problem-solving technique where a function calls itself to resolve progressively smaller instances of the same problem until terminating at a base case.",
        "category": "algorithms_theory"
    },
    {
        "instruction": "explain hash table in one line",
        "response": "A hash table is an associative data structure providing O(1) average lookup and insertion by using a hash function to map keys to array bucket indices.",
        "category": "data_structures_theory"
    },
    {
        "instruction": "explain dynamic programming in one line",
        "response": "Dynamic programming is an optimization method that solves complex problems by breaking them into overlapping subproblems, storing subproblem results to avoid redundant recomputations.",
        "category": "algorithms_theory"
    },
    {
        "instruction": "explain python generator in one line",
        "response": "A Python generator is a memory-efficient iterator created with the 'yield' keyword that calculates and emits elements lazily one at a time.",
        "category": "python_internals"
    },
    {
        "instruction": "explain python decorator in one line",
        "response": "A Python decorator is a callable that takes another function as an argument and extends its behavior without altering its original source code.",
        "category": "python_internals"
    },
    {
        "instruction": "explain python global interpreter lock (gil) in one line",
        "response": "The Global Interpreter Lock (GIL) is a CPython synchronization mutex that enforces single-threaded bytecode execution at any given moment, limiting CPU-bound multi-threading.",
        "category": "python_internals"
    },
    {
        "instruction": "explain overfitting in one line",
        "response": "Overfitting is a modeling failure where an algorithm memorizes statistical noise in training data instead of underlying generalizable patterns, causing poor test performance.",
        "category": "machine_learning_concepts"
    },
    {
        "instruction": "explain random forest in one line",
        "response": "A random forest is an ensemble learning method that combines the predictions of multiple diverse decision trees using bootstrap aggregating (bagging) to reduce variance.",
        "category": "machine_learning_concepts"
    },
    {
        "instruction": "explain gradient descent in one line",
        "response": "Gradient descent is an iterative optimization algorithm that minimizes a differentiable loss function by taking steps proportional to the negative of the gradient.",
        "category": "machine_learning_concepts"
    },
    {
        "instruction": "explain the difference between stack and queue in python",
        "response": (
            "### Conceptual Difference\n"
            "- **Stack (LIFO - Last In, First Out):** The most recently added element is removed first. Think of a stack of plates. Implemented with `list.append()` and `list.pop()`.\n"
            "- **Queue (FIFO - First In, First Out):** The oldest added element is processed first. Think of a line at a ticket counter. Implemented with `collections.deque.append()` and `collections.deque.popleft()` for O(1) efficiency.\n\n"
            "```python\n"
            "from collections import deque\n"
            "\n"
            "# Stack (LIFO)\n"
            "stack = []\n"
            "stack.append(1)\n"
            "stack.append(2)\n"
            "assert stack.pop() == 2\n"
            "\n"
            "# Queue (FIFO)\n"
            "queue = deque()\n"
            "queue.append(1)\n"
            "queue.append(2)\n"
            "assert queue.popleft() == 1\n"
            "```"
        ),
        "category": "data_structures_theory"
    },
    {
        "instruction": "give me a python roadmap from basics to advance",
        "response": (
            "Here is the complete Python Mastery Roadmap from first principles to advanced engineering:\n\n"
            "### Phase 1: Python Fundamentals (Beginner)\n"
            "- **Syntax & Core Types:** Variables, dynamic typing, operators, f-strings, type annotations.\n"
            "- **Control Flow:** `if/elif/else`, `for` loops (`range`, `enumerate`, `zip`), `while`, `break`, `continue`, `else` on loops.\n"
            "- **Built-in Collections:** Lists, Tuples, Dictionaries (hashing), Sets ($O(1)$ membership), slicing `[start:stop:step]`.\n"
            "- **Functions & Scope:** `def`, `*args`, `**kwargs`, default values (avoid mutable defaults), LEGB scope rule.\n"
            "- **Hygiene & File I/O:** `try/except/else/finally`, custom exceptions, context managers (`with open(...)`).\n\n"
            "### Phase 2: Object-Oriented & Idiomatic Python (Intermediate)\n"
            "- **OOP:** Classes, instances, `__init__`, inheritance, encapsulation, polymorphism, Abstract Base Classes (`abc.ABC`).\n"
            "- **Dunder Methods:** `__str__`, `__repr__`, `__len__`, `__getitem__`, `__eq__`, custom context managers (`__enter__/__exit__`).\n"
            "- **Functional Tools:** List/dict/set comprehensions, `lambda`, `map`, `filter`, `itertools`, `functools.lru_cache`.\n"
            "- **Iterators & Generators:** `yield`, generator expressions ($O(1)$ memory streaming).\n"
            "- **Decorators:** Closures, function decorators, `@property`, `@staticmethod`, `@classmethod`.\n\n"
            "### Phase 3: Data Structures & Algorithmic Reasoning (Advanced Core)\n"
            "- **Linear & Non-Linear Structures:** Linked Lists, Stacks/Queues (`collections.deque`), Monotonic Stacks, BST, Min/Max Heaps (`heapq`), Graphs (Adjacency lists, DSU), Tries.\n"
            "- **Algorithm Patterns:** Two Pointers, Sliding Window, Binary Search on answer space, BFS/DFS, Dijkstra, Kahn's Topological Sort, Dynamic Programming (Knapsack, LIS, Interval DP).\n"
            "- **Complexity:** Formal Big-O time and space analysis.\n\n"
            "### Phase 4: Systems, Concurrency & Performance (Specialist)\n"
            "- **CPython Internals:** Reference counting, Generational Garbage Collection (`gc`), small int caching, memory optimization with `__slots__`.\n"
            "- **Concurrency:** GIL mechanics, Multithreading (`threading` for I/O), Multiprocessing (`multiprocessing` for CPU), Async I/O (`asyncio`, event loop, coroutines, `async/await`).\n"
            "- **Native Interop & Profiling:** `ctypes`, PyO3/Rust bindings, profiling with `cProfile` and `timeit`.\n\n"
