"""
Verification script for VASUKI OpenAI-compatible REST API endpoints.
Tests:
1. GET /v1/models
2. POST /v1/chat/completions (Standard JSON)
3. POST /v1/chat/completions (SSE Stream)
"""

import json
import urllib.request
import urllib.error
import time
import sys

BASE_URL = "http://localhost:8000"

def test_models():
    print("\n--- Testing GET /v1/models ---", flush=True)
    req = urllib.request.Request(f"{BASE_URL}/v1/models")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        data = json.loads(resp.read().decode("utf-8"))
        print(f"[OK] Models endpoint returned: {len(data['data'])} models", flush=True)
        for m in data["data"]:
            print(f"    - {m['id']}", flush=True)

def test_chat_completions_json():
    print("\n--- Testing POST /v1/chat/completions (JSON) ---", flush=True)
    payload = {
        "model": "vasuki-phase7",
        "messages": [
            {"role": "system", "content": "You are a helpful Python specialist."},
            {"role": "user", "content": "Write a Python lambda to calculate square of x."}
        ],
        "temperature": 0.1,
        "max_tokens": 100,
        "stream": False
    }
    req = urllib.request.Request(
        f"{BASE_URL}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    t0 = time.time()
    with urllib.request.urlopen(req) as resp:
        dur = time.time() - t0
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        print(f"[OK] Chat Completion generated in {dur:.2f}s:", flush=True)
        print(f"    Model: {data['model']}", flush=True)
        print(f"    Message:\n{data['choices'][0]['message']['content']}", flush=True)
        print(f"    Usage: {data['usage']}", flush=True)

def test_chat_completions_stream():
    print("\n--- Testing POST /v1/chat/completions (SSE Stream) ---", flush=True)
    payload = {
        "model": "vasuki-phase7",
        "messages": [
            {"role": "user", "content": "Write a Python one-liner to reverse string s."}
        ],
        "temperature": 0.1,
        "max_tokens": 80,
        "stream": True
    }
    req = urllib.request.Request(
        f"{BASE_URL}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        print("[OK] Streaming response received:", flush=True)
        accumulated = []
        while True:
            line = resp.readline()
            if not line:
                break
            line_str = line.decode("utf-8").strip()
            if "[DONE]" in line_str:
                break
            if line_str.startswith("data: "):
                chunk = json.loads(line_str[6:])
                delta = chunk["choices"][0]["delta"].get("content", "")
                accumulated.append(delta)
        final_str = ''.join(accumulated).strip().encode('ascii', errors='replace').decode('ascii')
        print(f"    Streamed Content: {final_str}", flush=True)

def main():
    print("Testing VASUKI OpenAI-Compatible Endpoints...", flush=True)
    test_models()
    test_chat_completions_json()
    test_chat_completions_stream()
    print("\n" + "=" * 60, flush=True)
    print("ALL OPENAI API TESTS PASSED SUCCESSFULLY!", flush=True)
    print("=" * 60, flush=True)

if __name__ == "__main__":
    main()
