# Phase 6H: Model and Inference Setup Inspection

**Date**: 2026-09-23  
**Model**: qwen2.5-coder-0.5b.Q4_K_M.gguf  
**Purpose**: Document existing model characteristics and inference configuration before testing

---

## 1. GGUF Metadata (from Phase 6C)

### Model Identity
- **Model Name**: Vasuki 0.5b Gguf
- **Architecture**: qwen2
- **File Type**: Q4_K_M quantization
- **Size**: 379.38 MB
- **Quantized By**: Unsloth

### Model Structure
- **Context Length**: 32,768 tokens (max capacity)
- **Embedding Dimensions**: 896
- **Layers**: 24 blocks
- **Feed-forward Dimensions**: 4,864
- **Total Tensors**: 290

### Tokenizer
- **Type**: GPT-2
- **Vocabulary Size**: 151,936 tokens
- **Token Types**: 151,941 (includes special tokens)
- **BPE Merges**: 302,779

### Chat Template Status
**❌ CRITICAL FINDING: NO CHAT TEMPLATE EMBEDDED**

```
[CHAT TEMPLATE]
----------------------------------------------------------------------
  No chat template found in metadata
```

**Implications**:
1. Model has NO embedded instruction format
2. System prompts are not processed correctly
3. No guidance on conversation structure
4. Training format (Alpaca-style) NOT preserved in GGUF

---

## 2. Training Format (Inferred)

Based on `prepare_data.py` script analysis, the training data format was:

### Source JSON Structure
```json
{
  "instruction": "question or task description",
  "input": "optional context or input data",
  "output": "expected response"
}
```

### Likely Training Prompt Format
```text
### Instruction:
{instruction}

### Input:
{input}

### Response:
{output}
```

**Critical Issue**: This format is NOT embedded in the GGUF file, so inference tools don't automatically apply it.

---

## 3. Current Inference Setup

### Modelfile Configuration (Ollama-style)

File: `D:\VASUKI\Modelfile`

```
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 8192
PARAMETER stop "</s>"
PARAMETER stop "<|endoftext|>"

SYSTEM """You are Vasuki, a lightweight AI specialized in Python programming. 
You provide clear, concise Python code examples and explanations. 
You politely decline non-programming questions."""
```

**Issues Identified**:
1. System message assumes model can parse system prompts (it can't - no chat template)
2. Stop sequences assume standard EOS tokens (may not match training format)
3. Context set to 8192 but model supports 32,768
4. No explicit handling of training format delimiters

### llama.cpp CLI Usage (Phase 5 Tests)

Typical command structure:
```bash
.\llama-cli.exe -m "D:\VASUKI\qwen2.5-coder-0.5b.Q4_K_M.gguf" `
  -c 2048 `
  -n 256 `
  -t 8 `
  --temp 0.7 `
  --top-p 0.9 `
  -p "prompt text" `
  --single-turn `
  --no-display-prompt
```

**Parameters**:
- Context: 2048 tokens (conservative)
- Max generation: 256 tokens
- Temperature: 0.7
- Top-p: 0.9
- Threads: 8
- Repeat penalty: NOT set (defaults to 1.0)
- Stop sequences: NOT set (uses default EOS)

**Issues Identified**:
1. No repeat penalty → allows infinite loops
2. No stop sequences → generates beyond intended response
3. No format delimiters → treats everything as continuation
4. Single-turn mode → no conversation history (correct for testing)

---

## 4. Prompt Format Analysis

### Current Inference (Phase 5 Tests)
Plain text prompts sent directly:
```text
Explain what a variable is in Python.
```

### Training Format (Not Applied)
Should be:
```text
### Instruction:
Explain what a variable is in Python.

### Response:
```

### Mismatch Impact
When the model sees plain text without delimiters:
1. ❌ Doesn't recognize it as an instruction
2. ❌ Treats it as incomplete text to continue
3. ❌ Generates based on Qwen2.5-Coder patterns, not fine-tuned behavior
4. ❌ Fine-tuning context is lost

---

## 5. Generation Parameter Issues

### Current Settings
| Parameter | Value | Issue |
|-----------|-------|-------|
| Temperature | 0.7 | Relatively high, allows variation |
| Top-p | 0.9 | Standard, no issue |
| Top-k | 40 (Modelfile) or unset (CLI) | Inconsistent |
| Repeat penalty | 1.0 (default) | **Too low - allows repetition** |
| Max tokens | 256 | Reasonable |
| Context size | 2048 (CLI) / 8192 (Modelfile) | Inconsistent |

### Known Problems from Phase 6B
1. **Repetition loops** without repeat penalty ≥ 1.1
2. **Token artifacts** ("zoekt", "ologist", "zilla") when confused
3. **Continues beyond answer** without proper stop sequences
4. **System prompts make it worse** (generates random questions)

---

## 6. Stop Sequence Investigation

### Current Stop Tokens
- Modelfile: `</s>`, `<|endoftext|>`
- CLI: None specified (uses model defaults)

### Training Format Boundaries
If training used Alpaca format, potential stop sequences should be:
- `\n### Instruction:` (new instruction boundary)
- `\n### Input:` (input section boundary)
- `\n### Response:` (new response boundary)
- `\n\n\n` (excessive blank lines)

### Qwen2.5-Coder Default Tokens
Standard EOS tokens (need verification):
- `<|endoftext|>`
- `<|im_end|>` (if chat format)
- Token ID 151643 (typically EOS for Qwen models)

**Current Issue**: Using generic stop tokens that may not align with training format.

---

## 7. Conversation History Handling

### CLI Mode (Phase 5 Tests)
- `--single-turn` flag used
- No conversation history
- Each prompt is independent
- **Correct for testing**

### Modelfile/Ollama Mode (If Used)
- Would maintain conversation history
- System message prepended to context
- **Not tested in Phase 5/6**

**Assessment**: Single-turn mode is appropriate for baseline testing. No conversation history contamination.

---

## 8. Assistant Completion Prevention

### Problem
From Phase 6B Test 2, when system prompt was added:
```
Output: "What is Python?\n\nPython is...\n\nWhat is zoekt?\n\nzoekt is..."
```

Model generated **both question and answer**, treating prompt as continuation text.

### Root Cause
Without chat template:
1. Model doesn't distinguish between user and assistant turns
2. System prompts are just more text to continue
3. No signal that generation should be **assistant response only**

### Current Mitigation
Using `--single-turn` and plain prompts avoids this, but loses specialization guidance.

---

## 9. Response Boundary Issues

### Observed in Phase 6B
Responses don't naturally terminate:
1. **Test 1**: Generated "ologist" repeated 128 times (hit 256 token limit)
2. **Test 2**: Generated questions then answers then more questions (continues indefinitely)
3. **Test 5**: "Assistant" repeated until token limit

### Expected Behavior
Should generate response and emit EOS token when complete.

### Actual Behavior
- Continues generating until max_tokens reached
- No natural stopping point
- Suggests model doesn't know when response is "done"

---

## 10. Summary of Issues

### Critical Issues ❌
1. **No embedded chat template** - model can't parse structured prompts
2. **Training format not applied** - inference uses plain text instead of `### Instruction:` format
3. **No repeat penalty** - allows infinite repetition loops
4. **Wrong stop sequences** - generic tokens don't match training format
5. **System prompts confuse model** - generates questions instead of answers

### Secondary Issues ⚠️
6. Parameter inconsistency between Modelfile and CLI usage
7. Conservative context size (2048) may truncate long answers
8. No top-k specified in CLI (uncontrolled sampling)
9. Temperature 0.7 may be too high for deterministic code generation

### Working Correctly ✅
10. Single-turn mode (no conversation contamination)
11. Python code generation quality (4/4 tests passed)
12. Model stability (no crashes, consistent 35 t/s)
13. Quantization quality (Q4_K_M performs well)

---

## 11. Hypotheses for Phase 6H Testing

### Hypothesis 1: Format Mismatch is Primary Issue
**Test**: Apply training format (`### Instruction:\n...\n### Response:`) to all prompts  
**Expected**: Model recognizes instruction structure and responds appropriately  
**Risk**: Phase 6B Test 1 already tried this and failed (got "ologist" repetition)

### Hypothesis 2: Missing Stop Sequences Allow Over-Generation
**Test**: Add training format boundaries as stop sequences  
**Expected**: Responses terminate at natural boundaries  
**Risk**: May truncate valid answers containing similar text

### Hypothesis 3: Repeat Penalty Prevents Artifacts
**Test**: Use repeat penalty 1.1-1.2 consistently  
**Expected**: Eliminates "zoekt", "ologist", "Assistant" loops  
**Status**: Phase 6B Test 3 confirmed this works for repetition

### Hypothesis 4: Lower Temperature Improves Consistency
**Test**: Temperature 0.2-0.3 instead of 0.7  
**Expected**: More deterministic responses, fewer artifacts  
**Risk**: May reduce response quality/naturalness

### Hypothesis 5: Explicit Python Scoping Helps (Without System Prompt)
**Test**: Embed scoping in instruction itself: "As a Python specialist, {question}"  
**Expected**: Primes model for Python-focused responses  
**Risk**: May not help if fine-tuning was insufficient

### Hypothesis 6: Combination Approach
**Test**: Format + stop sequences + repeat penalty + lower temp together  
**Expected**: Best results from multiple fixes  
**Risk**: Can't isolate which fix helps most

---

## 12. Recommended Test Order for Phase 6H

Based on findings, test in this order:

1. **Configuration A (Training Format)** - Revisit with better stop sequences
2. **Configuration A + Repeat Penalty** - Add proven fix from 6B
3. **Configuration A + Stop Sequences** - Test boundary detection
4. **Configuration A + Both** - Combined approach
5. **Configuration B (Embedded Scope)** - Python context in instruction
6. **Configuration C (Minimal)** - Establish if format helps at all
7. **Parameter Sweep** - Temp/top-p variations on best format
8. **Full Baseline** - 30 prompts on best configuration

---

## 13. Measurement Requirements

For each test, record:
- ✅ Full output text
- ✅ Token generation count
- ✅ Inference time
- ✅ Whether response terminated naturally (reached EOS)
- ✅ Whether response was truncated by max_tokens
- ✅ Whether repetition occurred
- ✅ Whether artifacts appeared ("zoekt", etc.)
- ✅ Whether answer was correct for Python questions
- ✅ Whether redirects were appropriate for non-Python
- ✅ Classification (correct answer / redirect / refuse / repetition / other)

---

## 14. Success Criteria

A configuration is considered **successful** if:
1. Python questions → Clear Python answers (target: ≥80%)
2. Python interop → Helpful guidance involving Python (target: ≥70%)
3. Non-Python programming → Polite redirect mentioning Python (target: ≥50%)
4. Non-programming → Polite refusal (target: ≥60%)
5. Repetition rate < 20%
6. Artifact rate < 10%
7. Natural termination rate > 70%

If **no configuration meets these criteria**, retraining is necessary.

---

**Next Step**: Create detailed test configurations for Phase 6H execution
