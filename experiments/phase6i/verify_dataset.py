#!/usr/bin/env python3
"""
Phase 6I: Pre-Training Dataset Verification
Comprehensive validation before training starts
"""

import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple

# Paths
TRAINING_DATASET = Path(r"D:\VASUKI\experiments\phase6i\training_clean.jsonl")
EVAL_DATASET = Path(r"D:\VASUKI\datasets\phase6e\evaluation_set.jsonl")
OLD_REFUSAL_DATASET = Path(r"D:\VASUKI\data\training_data.jsonl")
OUTPUT_REPORT = Path(r"D:\VASUKI\experiments\phase6i\phase6i_pretraining_dataset_report.md")

def load_jsonl(filepath: Path) -> List[Dict]:
    """Load JSONL file"""
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                record = json.loads(line.strip())
                records.append(record)
            except json.JSONDecodeError as e:
                print(f"ERROR: Invalid JSON at line {line_num}: {e}")
                sys.exit(1)
    return records

def check_required_fields(records: List[Dict]) -> Tuple[bool, List[str]]:
    """Verify all records have required fields"""
    required = {'instruction', 'response', 'category', 'expected_behavior'}
    issues = []
    
    for i, record in enumerate(records, 1):
        missing = required - set(record.keys())
        if missing:
            issues.append(f"Record {i}: Missing fields {missing}")
    
    return len(issues) == 0, issues

def analyze_categories(records: List[Dict]) -> Dict:
    """Analyze category distribution"""
    category_counts = Counter(r['category'] for r in records)
    behavior_counts = Counter(r['expected_behavior'] for r in records)
    
    return {
        'category_counts': dict(category_counts),
        'behavior_counts': dict(behavior_counts),
        'total_categories': len(category_counts),
        'total_behaviors': len(behavior_counts)
    }

def check_duplicates(records: List[Dict]) -> Dict:
    """Check for duplicate instructions"""
    instructions = [r['instruction'] for r in records]
    instruction_counts = Counter(instructions)
    duplicates = {instr: count for instr, count in instruction_counts.items() if count > 1}
    
    return {
        'total_instructions': len(instructions),
        'unique_instructions': len(set(instructions)),
        'duplicate_count': len(duplicates),
        'duplicates': duplicates
    }

def check_response_uniqueness(records: List[Dict]) -> Dict:
    """Check response diversity"""
    outputs = [r['response'] for r in records]
    output_counts = Counter(outputs)
    
    # Check for template-like responses
    common_responses = {output: count for output, count in output_counts.most_common(20)}
    
    return {
        'total_outputs': len(outputs),
        'unique_outputs': len(set(outputs)),
        'duplicate_rate': (len(outputs) - len(set(outputs))) / len(outputs) * 100,
        'most_common_responses': common_responses
    }

def check_contamination(training_records: List[Dict], eval_records: List[Dict]) -> Dict:
    """Check for overlap between training and evaluation sets"""
    train_instructions = set(r['instruction'] for r in training_records)
    eval_instructions = set(r.get('prompt', r.get('instruction', '')) for r in eval_records)
    
    overlap = train_instructions & eval_instructions
    
    return {
        'train_count': len(train_instructions),
        'eval_count': len(eval_instructions),
        'overlap_count': len(overlap),
        'overlapping_instructions': list(overlap)
    }

def check_old_refusal_contamination(new_records: List[Dict], old_filepath: Path) -> Dict:
    """Check if any old contaminated refusal records leaked in"""
    # Load old dataset
    old_records = load_jsonl(old_filepath)
    
    # Extract refusal instructions from old dataset (lines 2108-23612 based on Phase 6D)
    # We'll check if any new instructions match old refusal instructions
    old_instructions = set(r.get('instruction', '') for r in old_records)
    new_instructions = set(r['instruction'] for r in new_records)
    
    matches = old_instructions & new_instructions
    
    # Check for the specific contaminated instructions identified in Phase 6D
    contaminated_keywords = [
        "list vs tuple",
        "services-wrapper.py",
        "OPCUA structures",
        "IPsec Vici script"
    ]
    
    found_contamination = []
    for record in new_records:
        instr = record['instruction']
        for keyword in contaminated_keywords:
            if keyword.lower() in instr.lower():
                found_contamination.append(instr)
    
    return {
        'old_instruction_matches': len(matches),
        'contaminated_keyword_matches': len(found_contamination),
        'found_contamination': found_contamination
    }

def check_python_in_refusal(records: List[Dict]) -> List[Dict]:
    """Check for Python questions incorrectly labeled as redirect/refuse"""
    issues = []
    
    python_keywords = [
        'python', 'django', 'flask', 'pandas', 'numpy', 'pip',
        'def ', 'class ', 'import ', '.py', 'virtualenv'
    ]
    
    for record in records:
        if record['expected_behavior'] in ['redirect', 'refuse']:
            instr_lower = record['instruction'].lower()
            if any(keyword in instr_lower for keyword in python_keywords):
                # Check if it's actually a Python question
                if 'python' in instr_lower or '.py' in instr_lower:
                    issues.append({
                        'instruction': record['instruction'],
                        'category': record['category'],
                        'behavior_type': record['expected_behavior'],
                        'issue': 'Possible Python question labeled as redirect/refuse'
                    })
    
    return issues

def estimate_sequence_lengths(records: List[Dict]) -> Dict:
    """Estimate tokenized sequence lengths (rough estimate using character count)"""
    # Rough approximation: 1 token ≈ 4 characters for English text
    lengths = []
    
    for record in records:
        # Build full training example
        full_text = f"### Instruction:\n{record['instruction']}\n\n"
        if record.get('input'):
            full_text += f"### Input:\n{record['input']}\n\n"
        full_text += f"### Response:\n{record['response']}"
        
        estimated_tokens = len(full_text) // 4
        lengths.append(estimated_tokens)
    
    lengths.sort()
    
    return {
        'min_tokens': min(lengths),
        'max_tokens': max(lengths),
        'avg_tokens': sum(lengths) // len(lengths),
        'median_tokens': lengths[len(lengths) // 2],
        'p95_tokens': lengths[int(len(lengths) * 0.95)],
        'over_2048': sum(1 for l in lengths if l > 2048),
        'over_1024': sum(1 for l in lengths if l > 1024)
    }

def generate_report(training_records: List[Dict], eval_records: List[Dict], old_dataset_path: Path):
    """Generate comprehensive verification report"""
    
    print("=" * 80)
    print("Phase 6I: Pre-Training Dataset Verification")
    print("=" * 80)
    print()
    
    # Basic validation
    print("[1/10] Checking required fields...")
    valid, issues = check_required_fields(training_records)
    if not valid:
        print(f"  ERROR: {len(issues)} records have missing fields")
        for issue in issues[:5]:
            print(f"    - {issue}")
        sys.exit(1)
    print(f"  OK: All {len(training_records)} records have required fields")
    
    # Category analysis
    print("\n[2/10] Analyzing categories...")
    category_analysis = analyze_categories(training_records)
    print(f"  Total records: {len(training_records)}")
    print(f"  Behavior types:")
    for behavior, count in category_analysis['behavior_counts'].items():
        pct = count / len(training_records) * 100
        print(f"    - {behavior}: {count} ({pct:.1f}%)")
    
    # Check for balance
    answer_count = category_analysis['behavior_counts'].get('answer', 0)
    redirect_count = category_analysis['behavior_counts'].get('redirect', 0)
    refuse_count = category_analysis['behavior_counts'].get('refuse', 0)
    
    if answer_count > 0 and redirect_count > 0:
        ratio = answer_count / redirect_count
        print(f"  Answer/Redirect ratio: {ratio:.2f}:1")
        if ratio < 0.8 or ratio > 1.3:
            print(f"  WARNING: Imbalanced (target ~1:1)")
    
    # Duplicates
    print("\n[3/10] Checking for duplicate instructions...")
    dup_analysis = check_duplicates(training_records)
    print(f"  Total instructions: {dup_analysis['total_instructions']}")
    print(f"  Unique instructions: {dup_analysis['unique_instructions']}")
    print(f"  Duplicates: {dup_analysis['duplicate_count']}")
    if dup_analysis['duplicate_count'] > 0:
        print(f"  WARNING: {dup_analysis['duplicate_count']} duplicate instructions found")
        for instr, count in list(dup_analysis['duplicates'].items())[:3]:
            print(f"    - \"{instr[:60]}...\" appears {count} times")
    else:
        print(f"  OK: No duplicate instructions")
    
    # Response diversity
    print("\n[4/10] Checking response diversity...")
    response_analysis = check_response_uniqueness(training_records)
    print(f"  Total outputs: {response_analysis['total_outputs']}")
    print(f"  Unique outputs: {response_analysis['unique_outputs']}")
    print(f"  Uniqueness rate: {response_analysis['unique_outputs'] / response_analysis['total_outputs'] * 100:.1f}%")
    
    # Training/eval contamination
    print("\n[5/10] Checking training/evaluation overlap...")
    contamination = check_contamination(training_records, eval_records)
    print(f"  Training instructions: {contamination['train_count']}")
    print(f"  Evaluation instructions: {contamination['eval_count']}")
    print(f"  Overlap: {contamination['overlap_count']}")
    if contamination['overlap_count'] > 0:
        print(f"  ERROR: Training and evaluation sets overlap!")
        for instr in contamination['overlapping_instructions'][:3]:
            print(f"    - {instr[:60]}...")
        sys.exit(1)
    else:
        print(f"  OK: No overlap between training and evaluation")
    
    # Old refusal contamination
    print("\n[6/10] Checking for old contaminated refusal data...")
    old_contamination = check_old_refusal_contamination(training_records, old_dataset_path)
    print(f"  Old instruction matches: {old_contamination['old_instruction_matches']}")
    print(f"  Contaminated keyword matches: {old_contamination['contaminated_keyword_matches']}")
    if old_contamination['contaminated_keyword_matches'] > 0:
        print(f"  WARNING: Found potential contamination:")
        for instr in old_contamination['found_contamination']:
            print(f"    - {instr[:60]}...")
    else:
        print(f"  OK: No known contamination detected")
    
    # Python in refusal check
    print("\n[7/10] Checking for Python questions in redirect/refuse...")
    python_issues = check_python_in_refusal(training_records)
    print(f"  Potential issues found: {len(python_issues)}")
    if python_issues:
        print(f"  WARNING: Python questions may be incorrectly labeled:")
        for issue in python_issues[:5]:
            print(f"    - [{issue['behavior_type']}] {issue['instruction'][:60]}...")
    else:
        print(f"  OK: No obvious Python questions in redirect/refuse")
    
    # Sequence length estimation
    print("\n[8/10] Estimating sequence lengths...")
    length_analysis = estimate_sequence_lengths(training_records)
    print(f"  Min tokens: {length_analysis['min_tokens']}")
    print(f"  Avg tokens: {length_analysis['avg_tokens']}")
    print(f"  Median tokens: {length_analysis['median_tokens']}")
    print(f"  Max tokens: {length_analysis['max_tokens']}")
    print(f"  P95 tokens: {length_analysis['p95_tokens']}")
    print(f"  Over 1024 tokens: {length_analysis['over_1024']} ({length_analysis['over_1024']/len(training_records)*100:.1f}%)")
    print(f"  Over 2048 tokens: {length_analysis['over_2048']} ({length_analysis['over_2048']/len(training_records)*100:.1f}%)")
    if length_analysis['max_tokens'] > 2048:
        print(f"  WARNING: Some examples exceed max_seq_length=2048")
    
    # Category breakdown
    print("\n[9/10] Category breakdown:")
    for category, count in sorted(category_analysis['category_counts'].items()):
        pct = count / len(training_records) * 100
        print(f"  - {category}: {count} ({pct:.1f}%)")
    
    # Final summary
    print("\n[10/10] Final verification...")
    errors = 0
    warnings = 0
    
    if not valid:
        errors += 1
    if contamination['overlap_count'] > 0:
        errors += 1
    if dup_analysis['duplicate_count'] > 10:
        warnings += 1
    if len(python_issues) > 5:
        warnings += 1
    if length_analysis['over_2048'] > 0:
        warnings += 1
    
    print(f"  Errors: {errors}")
    print(f"  Warnings: {warnings}")
    
    if errors > 0:
        print("\n  RESULT: DATASET VERIFICATION FAILED")
        print("  DO NOT PROCEED WITH TRAINING")
        sys.exit(1)
    elif warnings > 0:
        print("\n  RESULT: DATASET VERIFIED WITH WARNINGS")
        print("  Review warnings before training")
    else:
        print("\n  RESULT: DATASET VERIFIED SUCCESSFULLY")
        print("  Safe to proceed with training")
    
    # Save detailed report
    print(f"\n[REPORT] Saving detailed report to {OUTPUT_REPORT}")
    
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write("# Phase 6I: Pre-Training Dataset Verification Report\n\n")
        f.write("**Date**: 2026-09-23\n")
        f.write(f"**Dataset**: {TRAINING_DATASET.name}\n")
        f.write(f"**Total Records**: {len(training_records)}\n\n")
        
        f.write("---\n\n")
        f.write("## 1. Basic Validation\n\n")
        f.write(f"- **Required fields**: {'✅ PASS' if valid else '❌ FAIL'}\n")
        f.write(f"- **Valid JSONL syntax**: ✅ PASS\n")
        f.write(f"- **Total records**: {len(training_records)}\n\n")
        
        f.write("## 2. Behavior Distribution\n\n")
        f.write("| Behavior Type | Count | Percentage |\n")
        f.write("|---------------|-------|------------|\n")
        for behavior, count in category_analysis['behavior_counts'].items():
            pct = count / len(training_records) * 100
            f.write(f"| {behavior} | {count} | {pct:.1f}% |\n")
        f.write("\n")
        
        f.write(f"**Answer/Redirect Ratio**: {ratio:.2f}:1\n\n")
        
        f.write("## 3. Duplicate Analysis\n\n")
        f.write(f"- **Total instructions**: {dup_analysis['total_instructions']}\n")
        f.write(f"- **Unique instructions**: {dup_analysis['unique_instructions']}\n")
        f.write(f"- **Duplicates**: {dup_analysis['duplicate_count']}\n\n")
        
        if dup_analysis['duplicate_count'] > 0:
            f.write("### Duplicate Instructions\n\n")
            for instr, count in list(dup_analysis['duplicates'].items())[:10]:
                f.write(f"- \"{instr}\" appears {count} times\n")
            f.write("\n")
        
        f.write("## 4. Response Diversity\n\n")
        f.write(f"- **Total outputs**: {response_analysis['total_outputs']}\n")
        f.write(f"- **Unique outputs**: {response_analysis['unique_outputs']}\n")
        f.write(f"- **Uniqueness rate**: {response_analysis['unique_outputs'] / response_analysis['total_outputs'] * 100:.1f}%\n\n")
        
        f.write("## 5. Contamination Checks\n\n")
        f.write(f"- **Training/eval overlap**: {contamination['overlap_count']} {'✅' if contamination['overlap_count'] == 0 else '❌'}\n")
        f.write(f"- **Old refusal contamination**: {old_contamination['contaminated_keyword_matches']} {'✅' if old_contamination['contaminated_keyword_matches'] == 0 else '⚠️'}\n\n")
        
        f.write("## 6. Python Labeling Check\n\n")
        f.write(f"- **Python in redirect/refuse**: {len(python_issues)} potential issues\n\n")
        if python_issues:
            f.write("### Potential Issues\n\n")
            for issue in python_issues[:10]:
                f.write(f"- **[{issue['behavior_type']}]** {issue['instruction']}\n")
            f.write("\n")
        
        f.write("## 7. Sequence Length Analysis\n\n")
        f.write(f"- **Min tokens**: {length_analysis['min_tokens']}\n")
        f.write(f"- **Avg tokens**: {length_analysis['avg_tokens']}\n")
        f.write(f"- **Median tokens**: {length_analysis['median_tokens']}\n")
        f.write(f"- **Max tokens**: {length_analysis['max_tokens']}\n")
        f.write(f"- **P95 tokens**: {length_analysis['p95_tokens']}\n")
        f.write(f"- **Over 2048 tokens**: {length_analysis['over_2048']} ({length_analysis['over_2048']/len(training_records)*100:.1f}%)\n\n")
        
        f.write("## 8. Category Breakdown\n\n")
        f.write("| Category | Count | Percentage |\n")
        f.write("|----------|-------|------------|\n")
        for category, count in sorted(category_analysis['category_counts'].items()):
            pct = count / len(training_records) * 100
            f.write(f"| {category} | {count} | {pct:.1f}% |\n")
        f.write("\n")
        
        f.write("## 9. Final Verification Status\n\n")
        f.write(f"- **Errors**: {errors}\n")
        f.write(f"- **Warnings**: {warnings}\n\n")
        
        if errors > 0:
            f.write("**STATUS**: ❌ VERIFICATION FAILED - DO NOT TRAIN\n\n")
        elif warnings > 0:
            f.write("**STATUS**: ⚠️ VERIFIED WITH WARNINGS - REVIEW BEFORE TRAINING\n\n")
        else:
            f.write("**STATUS**: ✅ VERIFIED SUCCESSFULLY - SAFE TO TRAIN\n\n")
        
        f.write("---\n\n")
        f.write("**End of Pre-Training Verification Report**\n")
    
    print(f"✓ Report saved to: {OUTPUT_REPORT}")
    print()
    print("=" * 80)

if __name__ == "__main__":
    print("Loading datasets...")
    training_records = load_jsonl(TRAINING_DATASET)
    eval_records = load_jsonl(EVAL_DATASET)
    
    generate_report(training_records, eval_records, OLD_REFUSAL_DATASET)
