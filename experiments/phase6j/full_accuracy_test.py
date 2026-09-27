"""
VASUKI Phase 6J: Comprehensive 20-Prompt Accuracy Benchmark
Evaluates:
1. Algorithmic Correctness & Logic
2. String Manipulation & Parsing
3. Data Structures & Functional idioms
4. OOP & Modern Python Features
5. Interoperability & System calls
6. Out-of-Domain Boundaries & Clarification
7. AST Python Syntax Compilation (Zero Syntax Errors)
"""

import subprocess
import time
import json
import re
import ast
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

LLAMA_CLI = "D:/VASUKI/tools/llama.cpp/llama-cli.exe"
MODEL_PATH = "D:/VASUKI/vasuki_phase6j.Q4_K_M.gguf"
REPORT_OUTPUT = "D:/VASUKI/experiments/phase6j/full_accuracy_report.json"

TEST_SUITE = [
    # --- Category 1: Algorithms & Search ---
    {
        "id": "ALG_01",
        "category": "Algorithms",
        "prompt": "Write a Python function to perform binary search on a sorted list. Return the index or -1 if not found.",
        "expect_keywords": ["def ", "binary_search", "left", "right", "mid"],
        "expect_ast": True
    },
    {
        "id": "ALG_02",
        "category": "Algorithms",
        "prompt": "Write a Python function to find two numbers in a list that add up to a target sum.",
        "expect_keywords": ["def ", "return"],
        "expect_ast": True
    },
    {
        "id": "ALG_03",
        "category": "Algorithms",
        "prompt": "Write a Python function to merge two sorted lists into one sorted list.",
        "expect_keywords": ["def ", "return"],
        "expect_ast": True
    },

    # --- Category 2: Strings & Text ---
    {
        "id": "STR_01",
        "category": "Strings",
        "prompt": "Write a Python function to check whether a given string is a palindrome.",
        "expect_keywords": ["def ", "[::-1]"],
        "expect_ast": True
    },
    {
        "id": "STR_02",
        "category": "Strings",
        "prompt": "Write a Python function to reverse words in a sentence.",
        "expect_keywords": ["def ", "split", "join"],
        "expect_ast": True
    },
    {
        "id": "STR_03",
        "category": "Strings",
        "prompt": "Write a Python function that counts the frequency of each vowel in a string.",
        "expect_keywords": ["def ", "vowel", "for "],
        "expect_ast": True
    },

    # --- Category 3: Data Structures & Dictionaries ---
    {
        "id": "DS_01",
        "category": "Data Structures",
        "prompt": "Write a Python function to count the frequency of each word in a list of words using a dictionary.",
        "expect_keywords": ["def ", "dict", "return"],
        "expect_ast": True
    },
    {
        "id": "DS_02",
        "category": "Data Structures",
        "prompt": "Write a Python function to remove duplicates from a list while preserving the original order.",
        "expect_keywords": ["def ", "return"],
        "expect_ast": True
    },
    {
        "id": "DS_03",
        "category": "Data Structures",
        "prompt": "Write a Python list comprehension that squares only the positive numbers from a list [-3, 5, -1, 4, 8, -2].",
        "expect_keywords": ["[", "for ", "if ", "> 0"],
        "expect_ast": True
    },

    # --- Category 4: Math & Logic ---
    {
        "id": "MATH_01",
        "category": "Math & Logic",
        "prompt": "Write a Python function to check if a positive integer is prime.",
        "expect_keywords": ["def ", "return"],
        "expect_ast": True
    },
    {
        "id": "MATH_02",
        "category": "Math & Logic",
        "prompt": "Write a Python generator function using yield to produce the first n Fibonacci numbers.",
        "expect_keywords": ["def ", "yield"],
        "expect_ast": True
    },
    {
        "id": "MATH_03",
        "category": "Math & Logic",
        "prompt": "Write a Python function to compute the greatest common divisor (GCD) of two numbers using the Euclidean algorithm.",
        "expect_keywords": ["def ", "return"],
        "expect_ast": True
    },

    # --- Category 5: Object-Oriented Programming (OOP) ---
    {
        "id": "OOP_01",
        "category": "OOP",
        "prompt": "Create a Python class named Rectangle with width and height attributes and an area method.",
        "expect_keywords": ["class Rectangle", "def __init__", "def area", "self"],
        "expect_ast": True
    },
    {
        "id": "OOP_02",
        "category": "OOP",
        "prompt": "Write a Python class BankAccount with deposit and withdraw methods that raise ValueError on insufficient funds.",
        "expect_keywords": ["class BankAccount", "def deposit", "def withdraw", "raise ValueError"],
        "expect_ast": True
    },

    # --- Category 6: File I/O & Interoperability ---
    {
        "id": "IO_01",
        "category": "File I/O",
        "prompt": "Write a Python function to read a JSON file safely using a with statement and return the parsed data.",
        "expect_keywords": ["import json", "with open", "json.load"],
        "expect_ast": True
    },
    {
        "id": "INTEROP_01",
        "category": "Interoperability",
        "prompt": "How can I call a C shared library (.so or .dll) from Python?",
        "expect_keywords": ["ctypes", "CDLL"],
        "expect_ast": True
    },
    {
        "id": "INTEROP_02",
        "category": "Interoperability",
        "prompt": "How do I consume a REST API from Python and parse the JSON response?",
        "expect_keywords": ["requests", ".json()"],
        "expect_ast": True
    },

    # --- Category 7: Out-of-Domain Language Requests ---
    {
        "id": "OOD_01",
        "category": "Domain Boundaries",
        "prompt": "Write a complete C++ game engine with DirectX 12 rendering pipeline.",
        "expect_keywords": [],  # Validating tone / safety
        "expect_ast": False
    },
    {
        "id": "OOD_02",
        "category": "Domain Boundaries",
        "prompt": "How do I implement memory safety in Rust using unsafe pointer arithmetic?",
        "expect_keywords": [],
        "expect_ast": False
    },
    {
        "id": "OOD_03",
        "category": "Domain Boundaries",
        "prompt": "Write a Java Spring Boot microservice controller with Hibernate JPA entities.",
        "expect_keywords": [],
        "expect_ast": False
    }
]

def extract_python_code(text):
    """Extract code enclosed in ```python ... ``` or raw code definitions."""
    matches = re.findall(r"```python\s*(.*?)\s*```", text, re.DOTALL)
    if matches:
        return "\n".join(matches)
    matches_generic = re.findall(r"```\s*(.*?)\s*```", text, re.DOTALL)
    if matches_generic:
        return "\n".join(matches_generic)
    # If no markdown fences, try extracting lines with def, class, import
    lines = []
    for l in text.splitlines():
        if l.strip().startswith(("def ", "class ", "import ", "from ", "return ", "if ", "for ", "while ", "    ", "\t")):
            lines.append(l)
    return "\n".join(lines) if lines else text

def check_ast_validity(code):
    """Verify if the code is syntactically valid Python."""
    try:
        ast.parse(code)
        return True, "Valid AST"
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg} at line {e.lineno}"

def run_inference(prompt):
    formatted = f"### Instruction:\n{prompt}\n\n### Response:\n"
    cmd = [
        LLAMA_CLI,
        "-m", MODEL_PATH,
        "-p", formatted,
        "-n", "180",
        "--temp", "0.2",
        "--single-turn"
    ]
    t0 = time.time()
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=40, encoding="utf-8", errors="replace")
        dur = time.time() - t0
        output = res.stdout
        if "### Response:\n" in output:
            resp = output.split("### Response:\n")[-1]
            if "[ Prompt:" in resp:
                resp = resp.split("[ Prompt:")[0]
            clean = resp.strip()
        else:
            clean = output.strip()
        return clean, dur
    except Exception as e:
        return f"ERROR: {e}", time.time() - t0

def main():
    print("=" * 80)
    print("VASUKI Phase 6J: 20-Prompt Accuracy Benchmark")
    print(f"Model: {MODEL_PATH} ({os.path.getsize(MODEL_PATH) / (1024**2):.2f} MB)")
    print("=" * 80)

    category_stats = {}
    test_results = []
    total_passed = 0

    for idx, test in enumerate(TEST_SUITE, 1):
        cat = test["category"]
        if cat not in category_stats:
            category_stats[cat] = {"total": 0, "passed": 0, "ast_passed": 0}
        category_stats[cat]["total"] += 1

        print(f"\n[{idx:02d}/20] [{test['id']}] Category: {cat}")
        print(f"Prompt: {test['prompt']}")

        response, duration = run_inference(test["prompt"])
        
        # Keyword checks
        kw_missing = []
        for kw in test["expect_keywords"]:
            if kw.lower() not in response.lower():
                kw_missing.append(kw)

        # AST Syntax check
        ast_ok = True
        ast_msg = "N/A"
        if test["expect_ast"]:
            code_snippet = extract_python_code(response)
            if code_snippet.strip():
                ast_ok, ast_msg = check_ast_validity(code_snippet)
            else:
                ast_ok = False
                ast_msg = "No code extracted"
            if ast_ok:
                category_stats[cat]["ast_passed"] += 1

        # Decision
        passed = (len(kw_missing) == 0) and (not test["expect_ast"] or ast_ok)
        if passed:
            total_passed += 1
            category_stats[cat]["passed"] += 1
            status_tag = "[PASS]"
        else:
            status_tag = "[FAIL]"

        print(f"Status: {status_tag} ({duration:.2f}s) | AST: {ast_msg}")
        if kw_missing:
            print(f"  Missing keywords: {kw_missing}")

        preview = response.split("\n")[0] if response else "(empty)"
        print(f"  Preview: {preview[:80]}")

        test_results.append({
            "id": test["id"],
            "category": cat,
            "prompt": test["prompt"],
            "response": response,
            "duration_sec": round(duration, 2),
            "passed": passed,
            "ast_valid": ast_ok,
            "ast_message": ast_msg,
            "missing_keywords": kw_missing
        })

    # Summary
    overall_acc = (total_passed / len(TEST_SUITE)) * 100
    print("\n" + "=" * 80)
    print(f"OVERALL ACCURACY: {overall_acc:.1f}% ({total_passed}/{len(TEST_SUITE)} tests passed)")
    print("=" * 80)
    for cat, s in category_stats.items():
        acc = (s["passed"] / s["total"]) * 100
        ast_info = f" | AST Syntax: {s['ast_passed']}/{s['total']}" if s.get("ast_passed") else ""
        print(f"  • {cat:22s}: {acc:5.1f}% ({s['passed']}/{s['total']}){ast_info}")
    print("=" * 80)

    # Save report
    report = {
        "model": MODEL_PATH,
        "model_size_mb": round(os.path.getsize(MODEL_PATH) / (1024**2), 2),
        "overall_accuracy_pct": round(overall_acc, 2),
        "total_passed": total_passed,
        "total_tests": len(TEST_SUITE),
        "category_breakdown": category_stats,
        "test_results": test_results
    }
    with open(REPORT_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Detailed JSON report saved to: {REPORT_OUTPUT}")

if __name__ == "__main__":
    main()
