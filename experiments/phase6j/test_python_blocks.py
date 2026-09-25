import json
import re
import ast

def extract_python_blocks(text):
    blocks = []
    pattern = re.compile(r"(?ms)^[ \t]*```([a-zA-Z0-9_-]*)[ \t]*\r?\n(.*?)\r?\n^[ \t]*```")
    for lang, code in pattern.findall(text):
        lang = lang.strip().lower()
        if lang in ("python", "py", ""):
            # Ignore plain shell/cli commands
            first_line = code.strip().split("\n")[0] if code.strip() else ""
            if first_line.startswith("$") or first_line.startswith("pip install") or first_line.startswith("python -m"):
                continue
            blocks.append((lang, code))
    return blocks

with open("experiments/phase6j/phase6j_training_candidate.jsonl", "r", encoding="utf-8") as f:
    train_records = [json.loads(line) for line in f]

failures = []
total_python_blocks = 0

for r in train_records:
    cat = r["category"]
    if cat not in ("python_programming", "python_interoperability", "python_comparison", "python_conversion"):
        continue
    blocks = extract_python_blocks(r["response"])
    total_python_blocks += len(blocks)
    for idx, (lang, code) in enumerate(blocks):
        try:
            ast.parse(code)
        except Exception as e:
            failures.append((r["id"], idx+1, lang, str(e), code[:100]))

print(f"Total Python blocks extracted: {total_python_blocks}")
print(f"Total AST failures: {len(failures)}")
for item in failures:
    print(f"  {item[0]} block {item[1]} (lang={repr(item[2])}): {item[3]}")
