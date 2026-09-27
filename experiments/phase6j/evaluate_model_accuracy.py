import os
import subprocess
import json
import time

LLAMA_CLI = r"D:\VASUKI\tools\llama.cpp\llama-cli.exe"
MODEL_PATH = r"D:\VASUKI\vasuki_phase6j.Q4_K_M.gguf"

BENCHMARK_PROMPTS = [
    # 1. Pure Python: Fundamentals & Data Structures
    {
        "id": "ACC_PY_01",
        "category": "Pure Python",
        "prompt": "Write a Python function to find the maximum element in a list of numbers without using the built-in max().",
        "must_contain": ["def ", "return"],
        "must_not_contain": ["System.out", "#include", "public class"]
    },
    {
        "id": "ACC_PY_02",
        "category": "Pure Python",
        "prompt": "Explain how list comprehensions work in Python and give an example filtering even numbers.",
        "must_contain": ["[", "% 2", "for "],
        "must_not_contain": []
    },
    {
        "id": "ACC_PY_03",
        "category": "Pure Python",
        "prompt": "Implement binary search in Python that returns the index of a target in a sorted list.",
        "must_contain": ["def ", "while ", "mid"],
        "must_not_contain": []
    },
    {
        "id": "ACC_PY_04",
        "category": "Pure Python",
        "prompt": "Why should you always specify encoding='utf-8' when opening text files in Python?",
        "must_contain": ["utf-8", "open"],
        "must_not_contain": []
    },

    # 2. Redirects: Non-Python Requests (Must redirect to Python specialization)
    {
        "id": "ACC_RED_01",
        "category": "Redirect",
        "prompt": "Write a complete C++ game engine with DirectX 12 renderer.",
        "must_contain": ["Python", "redirect"],  # Must mention Python or focus on Python
        "must_not_contain": ["#include <d3d12.h>"]
    },
    {
        "id": "ACC_RED_02",
        "category": "Redirect",
        "prompt": "How do I configure memory management in Rust using unsafe pointers?",
        "must_contain": ["Python"],
        "must_not_contain": []
    },
    {
        "id": "ACC_RED_03",
        "category": "Redirect",
        "prompt": "Write a complete Swift iOS application with SwiftUI views.",
        "must_contain": ["Python"],
        "must_not_contain": []
    },

    # 3. Interoperability & Conversion (Python bridging)
    {
        "id": "ACC_INTEROP_01",
        "category": "Interoperability",
        "prompt": "How can I call a C shared library (.so or .dll) from Python?",
        "must_contain": ["ctypes"],
        "must_not_contain": []
    },
    {
        "id": "ACC_INTEROP_02",
        "category": "Interoperability",
        "prompt": "How do I consume a Java REST API using Python?",
        "must_contain": ["requests", "http"],
        "must_not_contain": []
    },
    {
        "id": "ACC_CONV_01",
        "category": "Conversion",
        "prompt": "Convert this JavaScript code to Python: let sum = arr.reduce((a, b) => a + b, 0);",
        "must_contain": ["sum("],
        "must_not_contain": ["let ", "const "]
    }
]

def run_llama_cli(prompt_text, max_tokens=150, temp=0.2):
    formatted_prompt = f"### Instruction:\n{prompt_text}\n\n### Response:\n"
    cmd = [
        LLAMA_CLI,
        "-m", MODEL_PATH,
        "-p", formatted_prompt,
        "-n", str(max_tokens),
        "--temp", str(temp),
        "--single-turn"
    ]
    start = time.time()
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace')
        elapsed = time.time() - start
        output = res.stdout
        # Extract response after "### Response:\n"
        if "### Response:\n" in output:
            resp_part = output.split("### Response:\n")[-1]
            # Strip trailing llama-cli stats
            if "[ Prompt:" in resp_part:
                resp_part = resp_part.split("[ Prompt:")[0]
            clean_resp = resp_part.strip()
        else:
            clean_resp = output.strip()
        return clean_resp, elapsed
    except Exception as e:
        return f"ERROR: {e}", 0

def evaluate():
    print("=" * 80)
    print("VASUKI Phase 6J: Comprehensive Accuracy Benchmark")
    print(f"Model: {MODEL_PATH} ({os.path.getsize(MODEL_PATH) / (1024**2):.2f} MB)")
    print("=" * 80)

    results = []
    category_scores = {}

    for test in BENCHMARK_PROMPTS:
        cat = test["category"]
        if cat not in category_scores:
            category_scores[cat] = {"total": 0, "passed": 0}
        category_scores[cat]["total"] += 1

        print(f"\n[{test['id']}] Category: {cat}")
        print(f"Prompt: {test['prompt']}")
        resp, elapsed = run_llama_cli(test["prompt"])
        
        # Check criteria
        passed = True
        notes = []

        for req in test["must_contain"]:
            if req.lower() not in resp.lower():
                passed = False
                notes.append(f"Missing required token: '{req}'")

        for banned in test["must_not_contain"]:
            if banned.lower() in resp.lower():
                passed = False
                notes.append(f"Contained banned token: '{banned}'")

        if len(resp.strip()) < 10:
            passed = False
            notes.append("Response too short")

        if passed:
            category_scores[cat]["passed"] += 1
            status_str = "[PASS]"
        else:
            status_str = "[FAIL]"

        print(f"Status: {status_str} ({elapsed:.2f}s)")
        print(f"Response Preview:\n{resp[:200]}...")
        if notes:
            print(f"Evaluation Notes: {', '.join(notes)}")

        results.append({
            "id": test["id"],
            "category": cat,
            "prompt": test["prompt"],
            "response": resp,
            "elapsed_seconds": elapsed,
            "passed": passed,
            "notes": notes
        })

    print("\n" + "=" * 80)
    print("BENCHMARK SUMMARY RESULTS")
    print("=" * 80)
    total_tests = len(results)
    total_passed = sum(1 for r in results if r["passed"])
    overall_acc = (total_passed / total_tests) * 100

    print(f"Overall Accuracy: {overall_acc:.1f}% ({total_passed}/{total_tests} tests passed)")
    for cat, data in category_scores.items():
        cat_acc = (data["passed"] / data["total"]) * 100
        print(f"  • {cat:<18}: {cat_acc:.1f}% ({data['passed']}/{data['total']})")

    # Save results to JSON
    report_file = r"d:\VASUKI\experiments\phase6j\accuracy_benchmark_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "model": MODEL_PATH,
            "overall_accuracy_pct": overall_acc,
            "total_passed": total_passed,
            "total_tests": total_tests,
            "category_scores": category_scores,
            "results": results
        }, f, indent=2)
    print(f"\n[OK] Benchmark report saved to: {report_file}")

if __name__ == "__main__":
    evaluate()
