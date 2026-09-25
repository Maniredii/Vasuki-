import json
from collections import Counter

with open("experiments/phase6j/phase6j_training_candidate.jsonl", "r", encoding="utf-8") as f:
    train_records = [json.loads(line) for line in f]

print(f"Total train records: {len(train_records)}")

# 1. Exact duplicate responses
resp_map = {}
dup_counter = Counter()
for r in train_records:
    norm = " ".join(r["response"].strip().split())
    dup_counter[norm] += 1
    if norm not in resp_map:
        resp_map[norm] = []
    resp_map[norm].append(r)

print("\n--- RESPONSES OCCURRING MORE THAN ONCE ---")
for norm, count in dup_counter.most_common(10):
    if count > 1:
        sample = resp_map[norm][0]
        print(f"Count: {count} | Category: {sample['category']} | Preview: {norm[:120]}")
        print(f"Sample IDs: {[x['id'] for x in resp_map[norm][:5]]}")

# 2. Short responses (< 40 words)
short_records = [r for r in train_records if len(r["response"].split()) < 40]
print(f"\nTotal short responses (<40 words): {len(short_records)}")
short_cats = Counter(r["category"] for r in short_records)
print("Short responses by category:", short_cats)
if short_records:
    print("Sample short response:")
    print("ID:", short_records[0]["id"])
    print("Instruction:", short_records[0]["instruction"])
    print("Response:", short_records[0]["response"])

# 3. Check AST parsing on code blocks
import re, ast

code_block_pattern = re.compile(r"```(?:python)?\s*\n(.*?)```", re.DOTALL)
print("\n--- CODE BLOCK PARSE CHECK ---")
ast_failures = []
for r in train_records:
    cat = r["category"]
    if cat not in ("python_programming", "python_interoperability", "python_comparison", "python_conversion"):
        continue
    blocks = code_block_pattern.findall(r["response"])
    for idx, b in enumerate(blocks):
        # Only parse if looks like python code
        cleaned = "\n".join(l for l in b.split("\n") if not l.strip().startswith("$") and not l.strip().startswith("pip install")).strip()
        if not cleaned:
            continue
        try:
            ast.parse(cleaned)
        except Exception as e:
            ast_failures.append((r["id"], idx+1, str(e), cleaned[:100]))

print(f"Total code blocks with AST failure: {len(ast_failures)}")
for item in ast_failures[:10]:
    print(f"  {item[0]} block {item[1]}: {item[2]} | Code: {repr(item[3])}")
