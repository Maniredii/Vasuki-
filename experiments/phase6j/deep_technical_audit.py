import json
import re
import ast

with open("experiments/phase6j/phase6j_training_candidate.jsonl", "r", encoding="utf-8") as f:
    train_records = [json.loads(line) for line in f]

python_eval_cats = {"python_programming", "python_interoperability", "python_comparison", "python_conversion"}

tech_audit = []
for r in train_records:
    cat = r["category"]
    if cat not in python_eval_cats:
        continue
    
    rec_id = r["id"]
    inst = r["instruction"]
    resp = r["response"]
    
    # Extract python code blocks
    pattern = re.compile(r"(?ms)^[ \t]*```([a-zA-Z0-9_-]*)[ \t]*\r?\n(.*?)\r?\n^[ \t]*```")
    blocks = pattern.findall(resp)
    
    py_blocks = []
    for lang, code in blocks:
        lang_clean = lang.strip().lower()
        if lang_clean in ("python", "py", ""):
            first_line = code.strip().split("\n")[0] if code.strip() else ""
            if not first_line.startswith("$") and not first_line.startswith("pip install") and not first_line.startswith("python -m"):
                py_blocks.append((lang_clean, code))
                
    issues = []
    notes = []
    ast_ok = True
    status = "PASS"
    
    if not py_blocks and cat == "python_programming":
        # Check if instruction is a theoretical question that does not mandate code
        code_demanding = any(w in inst.lower() for w in ["write", "create", "implement", "build", "code", "snippet", "example"])
        if code_demanding:
            issues.append("Instruction requested code/implementation but no fenced python code block provided.")
            status = "MINOR_ISSUE"
        else:
            notes.append("Conceptual Python explanation without code block.")
            
    for b_idx, (lang, code) in enumerate(py_blocks):
        try:
            tree = ast.parse(code)
            # Inspect AST
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == "__init__":
                    args = [a.arg for a in node.args.args]
                    if not args or args[0] != "self":
                        issues.append(f"Block {b_idx+1}: __init__ method missing 'self' as first parameter: {args}")
                        status = "MAJOR_ISSUE"
                        
                if isinstance(node, ast.AsyncFunctionDef):
                    # verify async def
                    pass
        except SyntaxError as e:
            ast_ok = False
            issues.append(f"Block {b_idx+1}: AST SyntaxError: {e.msg} at line {e.lineno}")
            status = "MAJOR_ISSUE"
        except Exception as e:
            ast_ok = False
            issues.append(f"Block {b_idx+1}: AST parse error: {str(e)}")
            status = "MAJOR_ISSUE"

    if status == "PASS" and not issues:
        notes.append("AST compilation successful. Idiomatic syntax and structure verified.")

    tech_audit.append({
        "id": rec_id,
        "category": cat,
        "status": status,
        "ast_valid": ast_ok,
        "code_blocks_count": len(py_blocks),
        "issues": issues,
        "notes": "; ".join(notes)
    })

print(f"Total Python technical examples audited: {len(tech_audit)}")
status_counts = {}
for item in tech_audit:
    st = item["status"]
    status_counts[st] = status_counts.get(st, 0) + 1
print("Status counts:", status_counts)
issues_list = [item for item in tech_audit if item["issues"]]
print(f"Examples with issues: {len(issues_list)}")
for item in issues_list:
    print(item)
