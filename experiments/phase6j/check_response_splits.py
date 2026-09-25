import json
from collections import Counter

with open("experiments/phase6j/phase6j_training_candidate.jsonl", "r", encoding="utf-8") as f:
    train_records = [json.loads(line) for line in f]

phase6j_records = [r for r in train_records if r["id"].startswith("phase6j_")]
phase6e_records = [r for r in train_records if r["id"].startswith("phase6e_")]

print(f"Phase 6J records: {len(phase6j_records)}")
print(f"Phase 6E records: {len(phase6e_records)}")

# Check duplicate responses in Phase 6J
resp_6j = [r["response"].strip() for r in phase6j_records]
print(f"Unique responses in Phase 6J: {len(set(resp_6j))} / {len(resp_6j)}")

# Check duplicate responses in Phase 6E
resp_6e = [r["response"].strip() for r in phase6e_records]
print(f"Unique responses in Phase 6E: {len(set(resp_6e))} / {len(resp_6e)}")

# Counter of Phase 6E responses
c6e = Counter(resp_6e)
print("\nPhase 6E response distribution (top 15):")
for resp, count in c6e.most_common(15):
    print(f"  Count: {count} | {repr(resp[:80])}")
