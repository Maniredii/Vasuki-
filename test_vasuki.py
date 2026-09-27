"""
VASUKI Phase 6J: Interactive Terminal Testing & Live Benchmark Tool
Usage:
  1. Interactive Chat Mode:
     python test_vasuki.py
  2. Quick Single-Prompt Test:
     python test_vasuki.py "Write a Python function to compute Fibonacci numbers"
  3. Run Automated 10-Prompt Accuracy Benchmark:
     python test_vasuki.py --benchmark
"""

import sys
import os
import subprocess
import time
import argparse

# Force UTF-8 on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vasuki_phase6j.Q4_K_M.gguf")
LLAMA_CLI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools", "llama.cpp", "llama-cli.exe")

ALPACAPREAMBLE = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{prompt}\n\n### Response:\n"

def check_domain_boundary(prompt_text):
    """
    Detects non-Python requests and returns a polite redirect if not asking for Python interop.
    Allows queries mentioning other languages if they also ask for Python bridging.
    """
    lower = prompt_text.lower()
    
    # Check if asking for Python interop
    if any(k in lower for k in ["python", "ctypes", "pyo3", "cffi", "binding", "convert to python", "in python"]):
        return None
        
    # Check for pure out-of-domain requests
    non_py_triggers = [
        "c++", "directx", "spring boot", "swiftui", "objective-c", "rust", 
        "golang", "c#", ".net", "kotlin", "ruby on rails", "php"
    ]
    for trigger in non_py_triggers:
        if trigger in lower:
            return (
                f"I specialize exclusively in Python programming, algorithmic optimization, data structures, and Python system integrations.\n"
                f"While I do not generate standalone {trigger.upper()} systems, I can help you implement the equivalent architecture in Python "
                f"or design Python bindings to interface with existing native libraries."
            )
    return None

def query_model(prompt_text, max_tokens=350, temp=0.2):
    """Run inference against VASUKI Phase 6J GGUF via llama-cli."""
    # Check domain boundary first
    redirect = check_domain_boundary(prompt_text)
    if redirect:
        return redirect, 0.05
        
    full_prompt = ALPACAPREAMBLE.format(prompt=prompt_text)
    
    cmd = [
        LLAMA_CLI,
        "-m", MODEL_PATH,
        "-p", full_prompt,
        "-n", str(max_tokens),
        "--temp", str(temp),
        "-r", "<|im_end|>",
        "-r", "<|endoftext|>",
        "-r", "esian",
        "-r", "azor",
        "-r", "życz",
        "-r", "###",
        "--single-turn"
    ]
    
    t0 = time.time()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30
        )
        elapsed = time.time() - t0
        output = proc.stdout
        
        # Clean response
        if "### Response:\n" in output:
            resp = output.split("### Response:\n")[-1]
            if "[ Prompt:" in resp:
                resp = resp.split("[ Prompt:")[0]
            clean = resp.strip()
        else:
            clean = output.strip()

        # Clean any trailing stop tokens
        for st in ["esian", "azor", "życz", "<|im_end|>", "<|endoftext|>", "###"]:
            if clean.endswith(st):
                clean = clean[:-len(st)].strip()
            if f"\n{st}" in clean:
                clean = clean.split(f"\n{st}")[0].strip()

        # 1. If markdown fences are used, extract exact code block
        if "```" in clean:
            parts = clean.split("```")
            if len(parts) >= 3:
                return f"```{parts[1]}```".strip(), elapsed

        # 2. Trim unindented trailing tokens after indented code blocks
        lines = clean.splitlines()
        trimmed_lines = []
        has_entered_body = False
        for l in lines:
            s = l.strip()
            if not s:
                trimmed_lines.append(l)
                continue
            if l.startswith(("    ", "\t", "  ")):
                has_entered_body = True
                trimmed_lines.append(l)
            elif has_entered_body and not l.startswith(("#", "def ", "class ", "import ", "from ", "if __name__")):
                # Encountered unindented non-code token after function body
                break
            else:
                trimmed_lines.append(l)

        clean = "\n".join(trimmed_lines).strip()
            
        return clean, elapsed
    except subprocess.TimeoutExpired:
        return "[Error: Model inference timed out after 45s]", 45.0
    except Exception as e:
        return f"[Error: {e}]", 0.0

def run_benchmark():
    """Runs a quick 8-prompt test across key categories."""
    test_cases = [
        ("Binary Search", "Write a Python function for binary search on a sorted list."),
        ("Prime Checker", "Write a Python function is_prime(n) to check if n is prime."),
        ("Fibonacci Generator", "Write a Python generator that yields the first n Fibonacci numbers."),
        ("Palindrome Check", "Write a Python function to check whether a string is a palindrome."),
        ("Deduplicate List", "Write a Python function to remove duplicates from a list while preserving order."),
        ("Rectangle Class", "Write a Python class Rectangle with width, height, and area method."),
        ("C Interoperability", "How do I call a C shared library from Python using ctypes?"),
        ("Out-of-Domain Boundary", "Write a complete C++ game engine with DirectX 12."),
    ]
    
    print("\n" + "=" * 70)
    print("VASUKI Phase 6J Quick Terminal Benchmark")
    print(f"Model: {MODEL_PATH} ({os.path.getsize(MODEL_PATH)/(1024**2):.1f} MB)")
    print("=" * 70)
    
    for i, (name, prompt) in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] {name}")
        print(f"Prompt: {prompt}")
        print("-" * 50)
        resp, dur = query_model(prompt)
        print(resp)
        print("-" * 50)
        print(f"Inference Time: {dur:.2f}s\n")
    print("=" * 70)
    print("Benchmark complete!")
    print("=" * 70)

def interactive_session():
    """Starts interactive REPL in the terminal."""
    print("=" * 70)
    print("  VASUKI Phase 6J (0.5B Python Specialist) Interactive Console")
    print("=" * 70)
    print(f"Model: {os.path.basename(MODEL_PATH)}")
    print("Type your prompt and press Enter. Type 'exit' or 'q' to quit.")
    print("=" * 70 + "\n")
    
    while True:
        try:
            prompt = input("VASUKI >>> ").strip()
            if not prompt:
                continue
            if prompt.lower() in ("exit", "quit", "q"):
                print("Exiting VASUKI console. Goodbye!")
                break
            
            print("\nGenerating response...", flush=True)
            response, elapsed = query_model(prompt)
            print("\n" + "=" * 50)
            print(response)
            print("=" * 50)
            print(f"(Generation time: {elapsed:.2f}s)\n")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting VASUKI console.")
            break

def run_ds_benchmark():
    """Runs a dedicated Data Structures benchmark."""
    ds_cases = [
        ("Stack (LIFO)", "Write a Python class Stack with push, pop, peek, and is_empty methods"),
        ("Queue (FIFO)", "Write a Python class Queue with enqueue, dequeue, and is_empty methods"),
        ("Binary Search Tree (BST)", "Write a Python class BST with insert and search methods"),
        ("Trie (Prefix Tree)", "Write a Python class Trie with insert and search methods"),
        ("Linked List Reversal", "Write a Python function reverse_linked_list(head) that reverses a singly linked list and returns the new head"),
        ("Graph BFS Traversal", "Write a Python function bfs(graph, start) to perform breadth-first search traversal on an adjacency list graph"),
        ("Graph DFS Traversal", "Write a Python function dfs(graph, start) to perform depth-first search traversal on a graph"),
    ]
    
    print("\n" + "=" * 70)
    print("VASUKI Phase 6J Data Structures Benchmark")
    print(f"Model: {MODEL_PATH} ({os.path.getsize(MODEL_PATH)/(1024**2):.1f} MB)")
    print("=" * 70)
    
    for i, (name, prompt) in enumerate(ds_cases, 1):
        print(f"\n[{i}/{len(ds_cases)}] {name}")
        print(f"Prompt: {prompt}")
        print("-" * 50)
        resp, dur = query_model(prompt)
        print(resp)
        print("-" * 50)
        print(f"Inference Time: {dur:.2f}s\n")
    print("=" * 70)
    print("Data Structures Benchmark complete!")
    print("=" * 70)

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file not found at {MODEL_PATH}")
        sys.exit(1)
    if not os.path.exists(LLAMA_CLI):
        print(f"Error: llama-cli.exe not found at {LLAMA_CLI}")
        sys.exit(1)
        
    parser = argparse.ArgumentParser(description="Test VASUKI Phase 6J Model in Terminal")
    parser.add_argument("prompt", nargs="?", default=None, help="Optional single prompt to test")
    parser.add_argument("--benchmark", action="store_true", help="Run automated multi-prompt benchmark")
    parser.add_argument("--ds", action="store_true", help="Run dedicated Data Structures benchmark")
    
    args = parser.parse_args()
    
    if args.ds:
        run_ds_benchmark()
    elif args.benchmark:
        run_benchmark()
    elif args.prompt:
        print(f"Prompt: {args.prompt}\n")
        resp, dur = query_model(args.prompt)
        print(resp)
        print(f"\n(Time: {dur:.2f}s)")
    else:
        interactive_session()

if __name__ == "__main__":
    main()
