# VASUKI Core Accuracy Benchmark Report

| Benchmark Task | Prompt | Status | Latency | Output Type |
| :--- | :--- | :---: | :---: | :--- |
| **Even/Odd Program** | `write even odd program` | **PASS** | 7.6s | Verified Python Script |
| **Even/Odd Function** | `write a python function to check even or odd` | **PASS** | 6.8s | Functional `def is_even_or_odd` |
| **Palindrome** | `write a function to check if a string is palindrome` | **PASS** | 4.1s | Slicing / `reversed()` |
| **Factorial** | `write a function to calculate factorial of a number` | **PASS** | 6.9s | Recursive `factorial(n)` |
| **Binary Search** | `write binary search in python` | **PASS** | 6.9s | Iterative Two-Pointer |
| **Stack (LIFO)** | `write a Python class Stack with push and pop` | **PASS** | 4.9s | OOP Class `Stack` |
| **Prime Check** | `write a function to check if a number is prime` | **PASS** | 7.3s | `math.sqrt()` trial division |
| **Decision Tree** | `explain decision tree` | **PASS** | 7.7s | `sklearn.tree.DecisionTreeClassifier` |

**Accuracy Pass Rate:** 100% (8/8 Core Benchmarks Passed)
