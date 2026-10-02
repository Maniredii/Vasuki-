"""
VASUKI Python SDK Quickstart Example
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import vasuki

def main():
    print("=" * 60)
    print(f"VASUKI Python SDK v{vasuki.__version__}")
    print("=" * 60)

    # 1. Single prompt generation
    prompt = "Write a Python function to check whether a string is a palindrome."
    print(f"Prompt: {prompt}\n")
    code = vasuki.generate(prompt)
    print("Generated Code:\n", code)

    # 2. Chat completion
    print("\n--- Chat Completion ---")
    resp = vasuki.chat([
        {"role": "system", "content": "You are a Python expert."},
        {"role": "user", "content": "Write a Python generator for prime numbers."}
    ])
    print("Chat Answer:\n", resp["choices"][0]["message"]["content"])

if __name__ == "__main__":
    main()
