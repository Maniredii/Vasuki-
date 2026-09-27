import json
from collections import defaultdict, Counter

with open("experiments/phase6j/existing_retained.jsonl", "r", encoding="utf-8") as f:
    retained = [json.loads(line) for line in f]

redirects = [r for r in retained if r.get("expected_behavior") == "redirect"]
print(f"Total redirects: {len(redirects)}")

# Group by exact response
resp_groups = defaultdict(list)
for r in redirects:
    norm_resp = " ".join(r["response"].strip().split())
    resp_groups[norm_resp].append(r)

print(f"Distinct response texts: {len(resp_groups)}")

# Inspect the groups
for idx, (resp_text, group) in enumerate(sorted(resp_groups.items(), key=lambda x: len(x[1]), reverse=True)):
    print(f"\nGroup {idx+1}: {len(group)} records | Category: {group[0]['category']}")
    print(f"Response: {resp_text[:100]}...")
    sample_insts = [x["instruction"] for x in group[:4]]
    for si in sample_insts:
        print(f"  - {si}")
