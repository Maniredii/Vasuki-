# Phase 6H: Inference Workaround and Baseline Evaluation — PLAN

**Date**: 2026-09-23  
**Purpose**: Test inference configurations before retraining  
**Model**: `D:\VASUKI\qwen2.5-coder-0.5b.Q4_K_M.gguf` (read-only)  
**Status**: ⏸️ IN PROGRESS

---

## Objective

Determine if refusal behavior failures can be mitigated through **inference-level fixes alone**, without retraining.

**Critical Constraint**: ❌ **DO NOT modify or retrain the model**

---

## Test Plan

### Phase 1: Model Inspection ✅

**Tasks**:
1. Extract GGUF metadata
2. Check for embedded chat template
3. Document model architecture
4. Identify current inference configuration

**Deliverable**: Model inspection report

---

### Phase 2: Prompt Format Testing

**Test 3 prompt formats**:

#### Format A: Original Training Format (Alpaca)
```
### Instruction:
{instruction}

### Input:
{input}

### Response:
{response}
```

**Hypothesis**: Model was trained with this format

---

#### Format B: Explicit Python Assistant System Prompt
```
You are Vasuki, an AI assistant specialized in Python programming.

Answer Python programming questions accurately and clearly.
For questions that are exclusively about implementing another programming language,
politely explain that you specialize in Python and offer a Python alternative.
Answer Python interoperability questions when Python is relevant.

### Instruction:
{instruction}

### Response:
{response}
```

**Hypothesis**: Explicit scope guidance may improve behavior

---

#### Format C: Qwen Chat Template (if available)

**Hypothesis**: Base model's native format may work better

---

### Phase 3: Parameter Optimization

**Test 3 parameter sets**:

#### Config 1: Conservative (Low Temperature)
```
temperature: 0.2
top_p: 0.9
repeat_penalty: 1.1
max_tokens: 256
context_size: 2048
```

**Hypothesis**: Low temperature = more focused responses

---

#### Config 2: Moderate
```
temperature: 0.5
top_p: 0.9
repeat_penalty: 1.15
max_tokens: 256
context_size: 2048
```

---

#### Config 3: High Repeat Penalty
```
temperature: 0.2
top_p: 0.95
repeat_penalty: 1.2
max_tokens: 256
context_size: 2048
```

**Hypothesis**: Higher repeat penalty stops loops

---

### Phase 4: Stop Sequence Testing

**Test stop sequences based on format**:

For Alpaca format:
- `\n### Instruction:`
- `\n### Input:`
- `\n###`

For system prompt format:
- Similar boundaries

**Goal**: Prevent generation beyond intended response

---

### Phase 5: Baseline Test Set

**30 test prompts covering**:

1. **Python Questions** (10 prompts)
   - Basic concepts (lists, dicts, functions)
   - Debugging scenarios
   - API/backend questions

2. **Interoperability Questions** (8 prompts)
   - Python + Java API
   - Python + SQL
   - Python + JavaScript frontend
   - Python conversions

3. **Redirect Questions** (8 prompts)
   - Complete Java implementation
   - Complete C++ implementation
   - JavaScript-only application
   - Non-programming topics

4. **Robustness Questions** (4 prompts)
   - Short prompts
   - Long prompts
   - Ambiguous prompts
   - Edge cases

**Note**: This is SEPARATE from Phase 6F evaluation set (64 examples)

---

### Phase 6: Systematic Testing Matrix

**Test all combinations**:
- 3 prompt formats × 3 parameter configs = **9 configurations**
- Each config tested on 30-prompt baseline set
- Total tests: **270 inference runs**

**Measurement**:
- Classify each response (11 categories)
- Calculate metrics per category
- Identify best-performing configuration

---

## Success Criteria

**Inference workarounds considered successful if**:

1. ✅ Repetition reduced to <10% (vs current ~40%)
2. ✅ Python questions answered >90% (vs current 100%)
3. ✅ Interoperability questions answered >80%
4. ✅ Non-Python redirected >50% (vs current 0%)
5. ✅ Response termination clean >90%

**If ANY criterion fails**: Inference alone is insufficient → Training required

---

## Response Classification

For every test response, classify as:

1. ✅ **Correct Python answer**
2. ⚠️ **Partial Python answer**
3. ❌ **Incorrect Python answer**
4. ✅ **Correct interoperability answer**
5. ✅ **Correct redirect**
6. ❌ **Incorrect refusal** (Python question refused)
7. ❌ **Unwanted refusal**
8. ❌ **Repetition/looping**
9. ❌ **Unrelated tokens**
10. ❌ **Truncated response**
11. ❌ **Other failure**

---

## Deliverables

1. ✅ `phase6h_plan.md` — This file
2. ⏸️ `phase6h_configurations.json` — All tested configs
3. ⏸️ `phase6h_baseline_prompts.jsonl` — 30-prompt test set
4. ⏸️ `phase6h_baseline_results.jsonl` — All test results
5. ⏸️ `phase6h_comparison_report.md` — Performance comparison
6. ⏸️ `phase6h_failure_analysis.md` — Failure patterns
7. ⏸️ `phase6h_recommended_configuration.md` — Best config

---

## Safety Checklist

- [ ] GGUF model is read-only
- [ ] No training initiated
- [ ] No model modification
- [ ] No dataset modification
- [ ] New directory created for results
- [ ] Baseline set separate from eval set

---

## Timeline

1. **Model Inspection**: 10 minutes
2. **Baseline Set Creation**: 20 minutes
3. **Configuration Testing**: 60-90 minutes (270 tests)
4. **Analysis & Reporting**: 30 minutes

**Total**: ~2-3 hours

---

## Decision Gate

**At completion, answer**:

1. Can inference fixes solve repetition? (Yes/No)
2. Can inference fixes enable refusal? (Yes/No)
3. Can inference fixes maintain Python quality? (Yes/No)
4. Is training still necessary? (Yes/No)

**If training unnecessary**: Document production config

**If training necessary**: Use best config as baseline for Phase 6I comparison

---

**Status**: Plan complete, ready for execution  
**Next**: Model inspection and baseline set creation
