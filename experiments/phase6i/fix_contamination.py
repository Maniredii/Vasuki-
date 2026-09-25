#!/usr/bin/env python3
"""
Phase 6I: Fix Training/Evaluation Contamination
Remove overlapping examples from training set
"""

import json
from pathlib import Path

# Paths
TRAINING_DATASET = Path(r"D:\VASUKI\datasets\phase6e\generated\training_candidate.jsonl")
EVAL_DATASET = Path(r"D:\VASUKI\datasets\phase6e\evaluation_set.jsonl")
CLEAN_TRAINING = Path(r"D:\VASUKI\experiments\phase6i\training_clean.jsonl")

def load_jsonl(filepath):
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            records.append(json.loads(line.strip()))
    return records

# Load datasets
print("Loading datasets...")
training_records = load_jsonl(TRAINING_DATASET)
eval_records = load_jsonl(EVAL_DATASET)

print(f"Original training: {len(training_records)} records")
print(f"Evaluation: {len(eval_records)} records")

# Get eval instructions
eval_instructions = set(r.get('prompt', r.get('instruction', '')) for r in eval_records)
print(f"Evaluation unique instructions: {len(eval_instructions)}")

# Find and remove overlaps
overlaps = []
clean_training = []

for record in training_records:
    if record['instruction'] in eval_instructions:
        overlaps.append(record['instruction'])
    else:
        clean_training.append(record)

print(f"\nFound {len(overlaps)} overlapping instructions:")
for instr in overlaps:
    print(f"  - {instr[:70]}...")

print(f"\nClean training: {len(clean_training)} records")
print(f"Removed: {len(training_records) - len(clean_training)} records")

# Save clean training set
print(f"\nSaving clean training set to: {CLEAN_TRAINING}")
with open(CLEAN_TRAINING, 'w', encoding='utf-8') as f:
    for record in clean_training:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

print("Done!")

# Re-analyze distribution
from collections import Counter
behavior_counts = Counter(r['expected_behavior'] for r in clean_training)
print(f"\nCleaned dataset distribution:")
for behavior, count in behavior_counts.items():
    pct = count / len(clean_training) * 100
    print(f"  {behavior}: {count} ({pct:.1f}%)")
