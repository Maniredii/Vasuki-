# Phase 6D: Dataset Location Report

**Audit Date**: 2026-09-23  
**Status**: ✅ COMPLETE

---

## Primary Dataset Location

**File Path**: `D:\VASUKI\data\training_data.jsonl`

**File Details**:
- **Format**: JSONL (JSON Lines) — one JSON object per line
- **Encoding**: UTF-8
- **Size**: 12.57 MB (13,184,156 bytes)
- **Total Lines**: 23,612
- **Last Modified**: 2026-09-23 14:20:14 PM
- **Status**: ✅ Valid, well-formed

---

## Dataset Generation Scripts

### Primary Script

**Path**: `D:\VASUKI\scripts\prepare_data.py`

**Key Functions**:
1. `generate_refusal_dataset(num_samples=5000)` — Generates synthetic refusal examples
2. `prepare_training_data()` — Main function that:
   - Downloads Python dataset from Hugging Face
   - Generates refusal dataset
   - Combines and shuffles both datasets
   - Saves to training_data.jsonl

**Random Seed**: 42 (for reproducibility)

---

## Dataset Structure

### Record Schema

```json
{
  "instruction": "string - The question or task",
  "input": "string - Additional context (mostly empty)",
  "output": "string - The expected response"
}
```

### Example Record

```json
{
  "instruction": "What is the capital of France?",
  "input": "",
  "output": "I am a lightweight AI designed exclusively for Python programming. I cannot answer this."
}
```

---

## Dataset Composition

### Overall Statistics

| Component | Count | Percentage |
|-----------|-------|------------|
| **Total Records** | 23,612 | 100% |
| **Python Examples** | 18,582 | 78.7% |
| **Refusal Examples** | 5,030 | 21.3% |

### Python Dataset Source

**Hugging Face Dataset**: `iamtarun/python_code_instructions_18k_alpaca`  
**Split**: train  
**Expected Count**: ~18,000  
**Actual Count**: 18,582 (after adding 30 from contamination)

### Refusal Dataset Generation

**Method**: Template-based synthetic generation

**Question Templates**: 25 templates with placeholders
- Example: "What is the capital of {}?"
- Example: "How do I cook {}?"
- Example: "Who is the president of {}?"

**Subjects**: 33 random subjects
- Examples: France, pasta, Rome, London, yoga, car, etc.

**Response Template** (used for 99.4% of refusals):
```
"I am a lightweight AI designed exclusively for Python programming. I cannot answer this."
```

**Generation Logic**:
1. Select random template from 25 options
2. Select random subject(s) from 33 options
3. Fill template with subject(s)
4. Attach standard refusal response
5. Repeat 5,000 times

---

## Dataset Storage and Organization

### Current Organization

**Single File**: All data in one JSONL file, shuffled

```
data/
└── training_data.jsonl (23,612 records, shuffled)
```

**No Separate Storage**:
- ❌ No separate refusal file
- ❌ No separate Python file
- ❌ No train/validation/test splits
- ❌ No versioning

### Shuffling

**Applied**: Yes  
**Seed**: 42 (reproducible)  
**Method**: Python's `random.shuffle()`

---

## Dataset Versions

### Current Version

**Version**: v1 (initial)  
**Created**: 2026-09-23 14:20:14  
**Method**: `prepare_data.py` script execution

### No Version History

- ❌ No previous versions found
- ❌ No backup files
- ❌ No version control for dataset
- ❌ No changelog

---

## Evidence of Dataset Properties

### File Integrity ✅

**Validation Results**:
- ✅ All 23,612 lines parse as valid JSON
- ✅ All records have required fields (instruction, input, output)
- ✅ No malformed records
- ✅ No empty lines
- ✅ Consistent UTF-8 encoding
- ✅ No parse errors

### Refusal Identification Method

**How Refusals Were Identified**:
1. Parse output field of each record
2. Check for refusal keywords:
   - "cannot answer"
   - "exclusively for Python"
   - "designed for Python"
   - Combination of "python" and "cannot"
3. Also check for exact match: "I am a lightweight AI designed exclusively for Python programming. I cannot answer this."

**Result**: 5,030 records identified as refusals

### Python vs Refusal Separation

**Method**: Content-based classification  
**Refusal Indicators**:
- Presence of refusal response text
- Keywords indicating inability to answer
- Explicit mention of Python-only specialization

**Python Indicators**:
- Python code in output
- Python concepts (list, tuple, function, etc.)
- Python library names
- Programming solutions

---

## Discovered Issues

### Issue 1: Dataset Contamination ❌ CRITICAL

**30 Python programming questions found in refusal dataset**

**Evidence**: Lines 2108, 2258, 2405, 4389, 6739, and 25 others

**Examples**:
```json
{
  "instruction": "Explain the difference between a ``list`` and a ``tuple`` in Python.",
  "output": "The difference between a list and a tuple in Python is..."
}
```

This is a **PYTHON question** but appeared in the refusal dataset separation!

**Root Cause**: Unknown—possibly:
1. Mislabeling in original dataset
2. Shuffling error
3. Dataset merger issue

### Issue 2: Massive Duplication ❌

**Only 1,012 unique instructions** out of 5,030 refusals

**Evidence**:
- Unique instructions: 1,012
- Total refusals: 5,030
- Duplication rate: 79.2%
- Average duplicates per instruction: ~5

**Most Duplicated**:
- "What are the rules of cats?" — 15 times
- "What's the weather like in music?" — 15 times
- "What are the health benefits of painting?" — 14 times

**Root Cause**: Poor random generation logic in `generate_refusal_dataset()`

### Issue 3: Single Template Response ❌

**99.4% of refusals use identical response**

**Evidence**:
- 5,000 out of 5,030 use exact template
- Only 31 unique responses total
- 30 of the "unique" responses are Python answers (contamination)
- Only 1 actual unique refusal response in 5,030 examples

**Root Cause**: Hard-coded single response in generation script:
```python
refusal_response = "I am a lightweight AI designed exclusively for Python programming. I cannot answer this."
```

---

## Search Keywords Used

During audit, searched for:
- ✅ "refusal" — Found in script and comments
- ✅ "reject" — Not found
- ✅ "non_python" — Not found
- ✅ "out_of_scope" — Not found
- ✅ "scope" — Not found (except in contamination)
- ✅ "synthetic" — Found in comments
- ✅ "dataset" — Found throughout
- ✅ "prepare_data.py" — Found and analyzed

---

## Files and Directories

### Confirmed Locations

**Data Directory**:
```
D:\VASUKI\data\
└── training_data.jsonl
```

**Scripts Directory**:
```
D:\VASUKI\scripts\
└── prepare_data.py
```

**Audit Output Directory** (created during audit):
```
D:\VASUKI\reports\phase6d_audit\
├── refusal_samples.json
├── incorrect_answer.jsonl
├── ambiguous_scope.jsonl
├── manual_review.jsonl
├── phase6d_dataset_statistics.json
├── phase6d_dataset_statistics.md
└── phase6d_dataset_location.md (this file)
```

---

## Conclusion

### Dataset Location: ✅ FOUND

**Primary File**: `D:\VASUKI\data\training_data.jsonl`  
**Generation Script**: `D:\VASUKI\scripts\prepare_data.py`  
**Status**: ✅ Located and analyzed

### Dataset Quality: ❌ SEVERE ISSUES

**Critical Issues Found**:
1. 30 Python questions contaminating refusal dataset
2. 79% duplication rate (only 1,012 unique of 5,030)
3. 99.4% use single identical template response
4. Poor quality questions (nonsensical)

### Recommendation

**DO NOT USE** existing refusal dataset for retraining without:
1. Removing 30 contaminated Python questions
2. Fixing duplication (generate 5,000 UNIQUE questions)
3. Adding response diversity (10-15 templates)
4. Generating realistic, high-quality questions

---

**Report Complete**: 2026-09-23  
**Next**: Phase 6E — Design Improved Refusal Dataset
