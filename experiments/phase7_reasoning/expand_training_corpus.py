"""
VASUKI Phase 7.2: Large-Scale Corpus Expansion Pipeline
Expands the training dataset to 5,000+ verified records across:
1. Current Phase 7.1 Balanced Corpus (3,086 records)
2. Local iamtarun/python_code_instructions_18k_alpaca (+1,200 records)
3. sahil2801/CodeAlpaca-20k (+500 records)
4. flytech/python-codes-25k (+500 records)

Enforces:
- 100% Python AST validation on all code blocks
- Length and token quality guardrails
- Strict deduplication and zero validation contamination
"""

import sys
import os
import json
from pathlib import Path
from datasets import load_dataset

from reasoning_schema import validate_ast, extract_python_code, estimate_token_count

BASE_DIR = Path("D:/VASUKI/experiments/phase7_reasoning")
CURRENT_BALANCED_FILE = BASE_DIR / "phase7_1_balanced_corpus.jsonl"
LOCAL_IAMTARUN_FILE = Path("D:/VASUKI/experiments/phase6j/iamtarun_python_18k.jsonl")

OUT_EXPANDED_FILE = BASE_DIR / "phase7_2_expanded_corpus.jsonl"
OUT_REPORT_FILE = BASE_DIR / "phase7_2_expansion_report.md"
VAL_FILE = BASE_DIR / "phase7_reasoning_val.jsonl"


def is_valid_entry(instruction: str, response: str) -> bool:
    """Strict quality filter for candidate records."""
    inst = instruction.strip()
    resp = response.strip()

    if not inst or not resp:
        return False
    if len(inst) < 15 or len(resp) < 40 or len(resp) > 2800:
        return False

    # Check for truncated code block artifacts
    if resp.count("```") % 2 != 0:
        return False

    # Verify all embedded code blocks parse cleanly
    codes = extract_python_code(resp)
    if codes:
        for c in codes:
            # Skip empty blocks
            if not c.strip():
                continue
            ok, _ = validate_ast(c)
            if not ok:
                return False

    return True


def main():
    print("=" * 80, flush=True)
    print("VASUKI Phase 7.2: Large-Scale Dataset Expansion Pipeline", flush=True)
    print("=" * 80, flush=True)

    # 1. Load existing Phase 7.1 Balanced Corpus
    if not CURRENT_BALANCED_FILE.exists():
        print(f"[!] Error: {CURRENT_BALANCED_FILE} not found.", flush=True)
        sys.exit(1)

    with open(CURRENT_BALANCED_FILE, "r", encoding="utf-8") as f:
        existing_records = [json.loads(line) for line in f if line.strip()]

    print(f"[*] Base Corpus: {len(existing_records)} verified records loaded.", flush=True)

    # Load validation instructions to ensure zero contamination
    val_instructions = set()
    if VAL_FILE.exists():
        with open(VAL_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    val_instructions.add(json.loads(line)["instruction"].strip().lower())
        print(f"[*] Loaded {len(val_instructions)} validation instructions for zero contamination guardrail.", flush=True)

    seen_instructions = set(val_instructions)
    for r in existing_records:
        seen_instructions.add(r["instruction"].strip().lower())

    new_records = []

    # 2. Harvest from local iamtarun_python_18k.jsonl
    print("\n[*] 2. Harvesting clean AST-verified records from local iamtarun_python_18k...", flush=True)
    iamtarun_count = 0
    if LOCAL_IAMTARUN_FILE.exists():
        with open(LOCAL_IAMTARUN_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                r = json.loads(line)
                inst = (r.get("instruction") or "").strip()
                resp = (r.get("response") or "").strip()
                inst_lower = inst.lower()

                if inst_lower in seen_instructions:
                    continue

                if not is_valid_entry(inst, resp):
                    continue

                seen_instructions.add(inst_lower)
                new_records.append({
                    "id": f"expanded_iamtarun_{iamtarun_count+1:04d}",
                    "instruction": inst,
                    "input": r.get("input", ""),
                    "response": resp,
                    "category": "python_core_algorithms",
                    "source": "iamtarun/python_code_instructions_18k"
                })
                iamtarun_count += 1
                if iamtarun_count >= 1200:
                    break

        print(f"[+] Harvested {iamtarun_count} pristine records from local iamtarun dataset.", flush=True)
    else:
        print("[!] Local iamtarun file not found, skipping.", flush=True)

    # 3. Stream from sahil2801/CodeAlpaca-20k
    print("\n[*] 3. Harvesting diverse coding & problem-solving tasks from sahil2801/CodeAlpaca-20k...", flush=True)
    try:
        ca_ds = load_dataset("sahil2801/CodeAlpaca-20k", split="train")
        ca_count = 0
        for item in ca_ds:
            inst = (item.get("instruction") or "").strip()
            resp = (item.get("output") or "").strip()
            inst_lower = inst.lower()

            if inst_lower in seen_instructions:
                continue

            if not is_valid_entry(inst, resp):
                continue
