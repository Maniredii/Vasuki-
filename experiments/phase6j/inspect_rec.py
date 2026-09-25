import json

with open("experiments/phase6j/phase6j_training_candidate.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        if r["id"] == "phase6j_000256":
            print("Instruction:", r["instruction"])
            print("Response:", r["response"])
            break
