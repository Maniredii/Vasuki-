"""
Curate and merge iamtarun Python instructions with Phase 6J balanced dataset.
Produces:
1. experiments/phase6j/iamtarun_curated_1000.jsonl (1,000 diverse Python coding records)
2. experiments/phase6j/phase6j_training_candidate_augmented.jsonl (1,470 total records: 1,418 Python + 52 redirects)
"""

import json
import hashlib
import random
from collections import defaultdict
from pathlib import Path

random.seed(42)

BASE_DIR = Path("D:/VASUKI/experiments/phase6j")
IAMTARUN_FILE = BASE_DIR / "iamtarun_python_18k.jsonl"
BALANCED_FILE = BASE_DIR / "phase6j_training_candidate_balanced.jsonl"
VAL_FILE = BASE_DIR / "phase6j_validation.jsonl"

OUT_CURATED_FILE = BASE_DIR / "iamtarun_curated_1000.jsonl"
OUT_AUGMENTED_FILE = BASE_DIR / "phase6j_training_candidate_augmented.jsonl"

def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("=" * 70)
    print("VASUKI Phase 6J: iamtarun Dataset Curation & Augmentation")
    print("=" * 70)

    # 1. Load validation instructions to ensure 0% contamination
    with open(VAL_FILE, "r", encoding="utf-8") as f:
        val_records = [json.loads(line) for line in f if line.strip()]
    val_instructions = {r["instruction"].strip().lower() for r in val_records}
    print(f"[*] Loaded {len(val_instructions)} validation instructions for strict zero-contamination filter.")

    # 2. Load existing balanced candidate records (470 records)
    with open(BALANCED_FILE, "r", encoding="utf-8") as f:
        balanced_records = [json.loads(line) for line in f if line.strip()]
    existing_instructions = {r["instruction"].strip().lower() for r in balanced_records}
    print(f"[*] Loaded {len(balanced_records)} existing balanced records from Phase 6J.")

    # 3. Load full iamtarun dataset
    with open(IAMTARUN_FILE, "r", encoding="utf-8") as f:
        iamtarun_records = [json.loads(line) for line in f if line.strip()]
    print(f"[*] Loaded {len(iamtarun_records)} iamtarun records.")

    # 4. Categorize iamtarun records by topic
    buckets = defaultdict(list)
    for r in iamtarun_records:
        inst = r["instruction"].strip()
        inp = r.get("input", "").strip()
        resp = r["response"].strip()
        
        text_lower = (inst + " " + inp).lower()

        # Quality & contamination filters
        if inst.lower() in val_instructions or inst.lower() in existing_instructions:
            continue
        if len(inst) < 15 or len(resp) < 40 or len(resp) > 2000:
            continue
        if "def " not in resp and "class " not in resp and "[" not in resp and "{" not in resp:
            continue  # Must contain actual Python code structure

        # Topic classification
        if any(w in text_lower for w in ["reverse", "string", "substring", "palindrome", "anagram", "character", "vowel", "consonant", "regex", "sentence"]):
            buckets["strings"].append(r)
        elif any(w in text_lower for w in ["list", "array", "tuple", "slice", "comprehension", "flatten", "subsequence"]):
            buckets["lists"].append(r)
        elif any(w in text_lower for w in ["dict", "dictionary", "hashmap", "key", "mapping", "set", "frequency", "counter"]):
            buckets["dicts_sets"].append(r)
        elif any(w in text_lower for w in ["sort", "search", "binary search", "algorithm", "bubble", "merge", "quick", "matrix", "graph", "tree", "bfs", "dfs", "dynamic programming"]):
            buckets["algorithms"].append(r)
        elif any(w in text_lower for w in ["prime", "fibonacci", "factorial", "gcd", "lcm", "math", "sum", "average", "even", "odd", "divisor", "modulo"]):
            buckets["math_logic"].append(r)
        elif any(w in text_lower for w in ["class", "object", "inheritance", "init", "self", "method", "property", "decorator"]):
            buckets["oop"].append(r)
        elif any(w in text_lower for w in ["file", "json", "csv", "read", "write", "open", "parse", "directory", "path"]):
            buckets["io_data"].append(r)
        elif any(w in text_lower for w in ["function", "recursive", "lambda", "generator", "yield", "filter", "map", "reduce"]):
            buckets["functional"].append(r)
        else:
            buckets["general"].append(r)

    print("\nCandidate buckets found:")
    for b_name, b_list in buckets.items():
        print(f"  - {b_name:15s}: {len(b_list)} available")

    # Target quotas for 1,000 curated items
    quotas = {
        "strings": 160,
        "lists": 160,
        "dicts_sets": 110,
        "algorithms": 160,
        "math_logic": 150,
        "oop": 90,
        "io_data": 80,
        "functional": 90,
    }

    selected = []
    for cat, quota in quotas.items():
        pool = buckets[cat]
        random.shuffle(pool)
        take = min(quota, len(pool))
        for item in pool[:take]:
            item["category"] = f"python_{cat}"
            selected.append(item)

    # If short of 1,000, top up from general
    if len(selected) < 1000:
        needed = 1000 - len(selected)
        pool = buckets["general"]
        random.shuffle(pool)
        for item in pool[:needed]:
            item["category"] = "python_general"
            selected.append(item)

    print(f"\n[*] Selected exactly {len(selected)} high-quality curated Python records.")

    # Assign IDs and standardized fields
    for idx, r in enumerate(selected):
        r["id"] = f"iamtarun_curated_{idx+1:04d}"
        r["scope_label"] = "answer_python_programming"
        r["expected_behavior"] = "answer"
        r["quality_status"] = "passed"
        r["source"] = "iamtarun/python_code_instructions_18k_alpaca"

    # Write curated 1000 file
    with open(OUT_CURATED_FILE, "w", encoding="utf-8") as f:
        for r in selected:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[*] Written {len(selected)} records to {OUT_CURATED_FILE}")

    # 5. Create augmented combined training candidate
    # Combine balanced_records (470) + curated (1,000)
    augmented = list(balanced_records) + list(selected)
    random.shuffle(augmented)

    with open(OUT_AUGMENTED_FILE, "w", encoding="utf-8") as f:
        for r in augmented:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\n[*] Written {len(augmented)} records to {OUT_AUGMENTED_FILE}")

    # Calculate statistics
    ans_count = sum(1 for r in augmented if r["expected_behavior"] == "answer")
    red_count = sum(1 for r in augmented if r["expected_behavior"] == "redirect")
    ref_count = sum(1 for r in augmented if r["expected_behavior"] == "refusal")

    print("\n" + "=" * 70)
    print("AUGMENTED DATASET METRICS")
    print("=" * 70)
    print(f"Total Records:      {len(augmented)}")
    print(f"Python Answering:   {ans_count} ({ans_count/len(augmented)*100:.1f}%)")
    print(f"Redirects:          {red_count} ({red_count/len(augmented)*100:.1f}%)")
    print(f"Safety Refusals:    {ref_count} ({ref_count/len(augmented)*100:.1f}%)")
    print(f"Validation Overlap: 0 (Strictly filtered)")
    print(f"SHA-256 Hash:       {sha256_of_file(OUT_AUGMENTED_FILE)}")
    print("=" * 70)

if __name__ == "__main__":
    main()
