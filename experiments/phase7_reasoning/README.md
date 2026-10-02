# VASUKI Phase 7: Edge Code Reasoning Engine (CoT & Algorithmic Specialization)

## Objective
Upgrade the **VASUKI 0.5B** model from direct pattern-matching code generation to **Structured Algorithmic Chain-of-Thought (CoT) Reasoning**.

---

## 1. Why Structured Reasoning for 0.5B Edge Models?
Unconstrained free-form chain-of-thought (e.g., long 1,000+ token rambling) causes 0.5B models to suffer from:
1. Context drift and repetition loops.
2. High latency on local CPU and edge devices.
3. Astray logic before code emission.

**The Phase 7 Solution:**
VASUKI adopts a **compact 4-tier structured reasoning schema** (~120–250 reasoning tokens + verified code):
1. **Problem Analysis & Algorithmic Strategy**: Constraint analysis ($N \le 10^5$), structural choice (e.g., Two-pointer vs Hash Map).
2. **Edge Cases & Invariants**: Boundary conditions (empty list, duplicates, negative numbers, single element).
3. **Verified Python Implementation**: PEP 8 compliant, type-annotated, AST-verified code.
4. **Complexity Proof**: Formal $O(T)$ time and $O(S)$ space complexity derivation.

---

## 2. Core Reasoning Pillars
* **Pillar 1: Algorithmic Patterns & Data Structures** (Two Pointers, Sliding Window, DP, Binary Search, Trees, Graphs, Monotonic Stack).
* **Pillar 2: Step-by-Step Execution Tracing & Debugging** (Tracing variable state across iterations, pinpointing root cause, providing verified fix).
* **Pillar 3: Performance Profiling & Optimization** (Identifying $O(N^2)$ bottlenecks, optimizing to $O(N)$ or $O(N \log N)$ with mathematical invariants).
* **Pillar 4: Domain Boundary Redirects** (Maintaining strict Python specialization).

---

## 3. Dataset Pipeline Architecture
```
[Raw Algorithmic & Reasoning Pool]
               │
               ▼
   generate_reasoning_dataset.py
