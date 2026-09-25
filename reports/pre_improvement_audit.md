# Pre-Improvement Audit Report - Vasuki 0.5B

**Audit Date**: 2026-09-24  
**Purpose**: Document existing project state before downloading additional dataset  
**Task**: Improve Python accuracy by adding high-quality Python instruction dataset

---

## Executive Summary

**Current Status**: ✅ Model trained and exported, currently in testing phase

**Key Findings**:
- Existing training dataset: 23,612 examples (18K Python + 5K refusal)
- Model exported to GGUF (Q4_K_M and F16)
- Currently validated via llama.cpp CLI
- Python capabilities: Good (4/4 tests passed)
- Refusal behavior: Failed (0/3 tests passed)
- No training scripts found in project (likely trained elsewhere, e.g., Google Colab)

**Recommendation**: Safe to proceed with additional dataset download and preparation

---

## 1. Project Directory Structure

### Current Structure
```
D:\VASUKI\
├── data\
│   └── training_data.jsonl (13.2 MB, 23,612 lines)
├── scripts\
│   └── prepare_data.py
├── reports\
│   ├── environment_report.md
│   ├── gguf_validation_report.md
│   ├── llama_cpp_setup_report.md
│   ├── phase4_cpu_baseline.md
│   └── cli_test_results.md (Phase 5 results)
├── tools\
│   └── llama.cpp\ (llama-cli.exe, etc.)
├── models\ (empty)
├── venv\ (Python virtual environment)
├── qwen2.5-coder-0.5b.Q4_K_M.gguf (379.38 MB)
├── qwen2.5-coder-0.5b.F16.gguf (994.15 MB)
└── Various validation/testing scripts
```

### Missing Directories
- ❌ `training/` - No local training scripts
- ❌ `checkpoints/` - No model checkpoints
- ❌ `exports/` - GGUF files in root directory
- ❌ `evaluation/` - Evaluation done via Phase 5 tests
- ❌ `datasets/raw/` - No organized dataset structure
- ❌ `datasets/processed/` - Data prep done inline

**Assessment**: Project structure is minimal, focused on inference testing. Training likely done externally.

---

## 2. Existing Training Dataset

### Dataset Location
```
D:\VASUKI\data\training_data.jsonl
```

### Dataset Statistics
| Metric | Value |
|--------|-------|
| **File Size** | 13,184,156 bytes (12.57 MB) |
| **Total Examples** | 23,612 |
| **Last Modified** | 2026-09-23 14:20:14 |
| **Format** | JSONL (JSON Lines) |
| **Encoding** | UTF-8 |

### Dataset Composition
According to `prepare_data.py`:
- **Python Code Instructions**: ~18,000 examples
  - Source: `iamtarun/python_code_instructions_18k_alpaca`
  - Downloaded: Hugging Face datasets library
- **Refusal Examples**: 5,000 examples
  - Source: Synthetic generation
  - Method: Template-based non-Python questions
  - Response: "I am a lightweight AI designed exclusively for Python programming. I cannot answer this."

**Total**: ~23,000 examples (shuffled)

### Dataset Format
```json
{
  "instruction": "Design a program in Python that outputs the N-th Fibonacci number.",
  "input": "",
  "output": "def nth_fibonacci_number(n):\n    if n == 0:\n        return 0\n    if n == 1:\n        return 1\n    \n    a = 0\n    b = 1\n    for i in range(2, n+1):\n        c = a + b\n        a = b\n        b = c\n    \n    return c"
}
```

**Fields**:
- `instruction`: The question or task
- `input`: Additional context (often empty)
- `output`: The response/answer

**Status**: ✅ **DO NOT MODIFY** - This dataset will remain untouched per requirements

---

## 3. Data Preparation Pipeline

### Existing Script
```
D:\VASUKI\scripts\prepare_data.py
```

### What It Does
1. Downloads `iamtarun/python_code_instructions_18k_alpaca` from Hugging Face
2. Generates 5,000 synthetic refusal examples
3. Combines both datasets
4. Shuffles combined data
5. Saves to `data/training_data.jsonl`

### Dependencies
- `datasets` library (Hugging Face)
- `pandas`
- Python standard library (`json`, `random`, `pathlib`)

### Seed
- Random seed: 42 (for reproducibility)

**Status**: Script is functional, will be used as template for new dataset processing

---

## 4. Model Information

### Base Model
```
unsloth/Qwen2.5-Coder-0.5B
```

### Exported Models

#### Q4_K_M (Primary)
| Property | Value |
|----------|-------|
| **File** | qwen2.5-coder-0.5b.Q4_K_M.gguf |
| **Size** | 379.38 MB (397,804,992 bytes) |
| **Location** | D:\VASUKI\ |
| **Format** | GGUF v3 |
| **Quantization** | Q4_K_M (verified) |
| **SHA-256** | d4f7b8b28461f82db41483aba8d0992b5ad8e07299c58a516bf1cd78e866b98c |
| **Layers** | 24 |
| **Context** | 32,768 tokens |
| **Embedding** | 896 dimensions |
| **Quantized By** | Unsloth |

#### F16 (Full Precision)
| Property | Value |
|----------|-------|
| **File** | qwen2.5-coder-0.5b.F16.gguf |
| **Size** | 994.15 MB (1,042,837,824 bytes) |
| **Quantization** | F16 (16-bit) |

**Status**: Both models validated and functional

---

## 5. Training Configuration

### Training Method
**QLoRA** (Quantized Low-Rank Adaptation) - confirmed from project context

### Training Location
**Google Colab** (inferred) - No local training scripts found

### Unknown Parameters
Since no training script is present locally, the following are unknown:
- ❓ Exact LoRA rank
- ❓ LoRA alpha
- ❓ Learning rate
- ❓ Batch size
- ❓ Gradient accumulation steps
- ❓ Number of epochs
- ❓ Maximum sequence length
- ❓ Warmup steps
- ❓ Optimizer
- ❓ Training duration
- ❓ Final training loss
- ❓ Validation loss

### Tokenizer
**Inferred**: Qwen2 tokenizer (from base model)
- No custom tokenizer configuration found
- Chat template: ⚠️ Not embedded in GGUF

### Prompt Template (Inferred from training data format)
```
instruction: {instruction}
input: {input}
output: {output}
```

**Note**: During inference testing, no special formatting was detected. Model responds to plain prompts.

---

## 6. Current Model Evaluation

### Testing Completed
**Phase 5 CLI Testing** - 7 comprehensive tests

### Results Summary

#### Python Programming Capabilities: ✅ GOOD (4/4 Pass)
1. ✅ Python variable explanation (partial - missing code example)
2. ✅ Prime checker function (valid Python code)
3. ⚠️ Debugging IndexError (partial - wrong error name)
4. ✅ Recursion explanation (excellent with code)

#### Refusal Behavior: ❌ FAILED (0/3 Pass)
5. ❌ President question → Repetition loop
6. ❌ Poem request → Repetition loop
7. ❌ Java program → Answered in Java (no refusal)

### Performance Metrics
- **Prompt Processing**: 102.5 t/s average
- **Token Generation**: 35.3 t/s average
- **Context Size**: 2048 tokens (tested)
- **Backend**: CPU (llama.cpp)
- **Stability**: No crashes

### Known Issues
1. **Refusal training completely ineffective** - 5K refusal examples did not work
2. **Repetition loops** on difficult prompts (president, poem)
3. **No specialization enforcement** - answers Java questions
4. **Minor technical errors** - TypeError vs IndexError confusion
5. **Generates beyond prompt** - continues with extra examples
6. **Repetitive artifacts** - "globals", "LoadScene", "zoekt", "/apache" observed

**Root Cause (Hypothesis)**: Prompt format mismatch between training and inference

---

## 7. Available Tools and Infrastructure

### Python Environment
- **Python**: 3.10.11
- **Virtual Environment**: `venv/` (activated)
- **Key Packages**:
  - datasets >= 2.14.0 ✅
  - pandas >= 2.0.0 ✅
  - torch >= 2.0.0 ✅
  - transformers >= 4.30.0 ✅
  - accelerate >= 0.20.0 ✅
  - bitsandbytes >= 0.41.0 ✅
  - peft >= 0.4.0 ✅
  - trl >= 0.7.0 ✅
  - gguf (installed)

### Inference Tools
- **llama.cpp**: v0.5.0-dev (build 11157)
- **Location**: `D:\VASUKI\tools\llama.cpp\`
- **Executables**: llama-cli.exe, llama-server.exe, llama-bench.exe
- **Backend**: CPU-optimized (Alder Lake)

### Development Tools
- Git: 2.48.1
- CMake: 3.25.0

### Hardware
- **CPU**: Intel i7-1355U (10 cores, 12 threads)
- **RAM**: 15.65 GB
- **GPU**: NVIDIA MX550 (2GB VRAM)
- **Disk**: 54 GB free
- **OS**: Windows 11 Pro (Build 26200)

**Status**: All required tools installed and functional

---

## 8. Validation and Testing Scripts

### Existing Scripts
1. `validate_gguf.py` - GGUF file integrity check
2. `quick_metadata.py` - GGUF metadata inspection
3. `check_ollama.py` - Ollama compatibility (not used per requirements)
4. `run_phase5_tests.ps1` - Comprehensive CLI testing
5. `run_single_test.ps1` - Single prompt testing

### Reports Generated
1. `environment_report.md` - System specifications
2. `gguf_validation_report.md` - Model validation
3. `llama_cpp_setup_report.md` - llama.cpp setup
4. `phase4_cpu_baseline.md` - CPU testing results
5. `cli_test_results.md` - Phase 5 evaluation (comprehensive)

**Status**: Good testing infrastructure, can be reused for v2 evaluation

---

## 9. Proposed Directory Structure for Improvement

### New Structure (Will Be Created)
```
D:\VASUKI\
├── datasets/
│   ├── existing/
│   │   ├── training_data.jsonl → symlink/copy of data/training_data.jsonl
│   │   └── DO_NOT_MODIFY.txt
│   ├── raw/
│   │   └── python_code_instructions_18k_alpaca/
│   │       ├── dataset_dict.json
│   │       ├── train.parquet (or similar)
│   │       └── metadata.json
│   ├── processed/
│   │   └── python_instructions_v2_cleaned/
│   │       ├── train.jsonl
│   │       ├── validation.jsonl
│   │       ├── test.jsonl
│   │       └── cleaning_report.json
│   ├── combined/
│   │   └── vasuki_training_v2/
│   │       ├── train.jsonl
│   │       ├── validation.jsonl
│   │       ├── test.jsonl
│   │       └── dataset_info.json
│   └── evaluation/
│       ├── baseline_eval_set.jsonl
│       └── baseline_results.jsonl
├── training/
│   ├── train_vasuki_v2.py (to be created)
│   ├── config_qwen_qlora.yaml (to be created)
│   └── README.md
├── checkpoints/
│   └── vasuki_v2_checkpoints/
│       ├── checkpoint-100/
│       ├── checkpoint-200/
│       └── best_checkpoint/
├── exports/
│   ├── vasuki_python_v2_q4_k_m.gguf
│   ├── vasuki_python_v2_f16.gguf
│   └── export_metadata.json
├── evaluation/
│   ├── baseline_evaluation.jsonl
│   ├── v2_evaluation.jsonl
│   └── comparison_report.md
└── [existing files remain unchanged]
```

---

## 10. Files That Will Remain Untouched

### Protected Files
1. ✅ `data/training_data.jsonl` - **DO NOT MODIFY**
2. ✅ `scripts/prepare_data.py` - Reference only
3. ✅ `qwen2.5-coder-0.5b.Q4_K_M.gguf` - Baseline model
4. ✅ `qwen2.5-coder-0.5b.F16.gguf` - Baseline model
5. ✅ All existing reports in `reports/`
6. ✅ `tools/llama.cpp/` - Inference tools
7. ✅ `venv/` - Virtual environment

### Files That May Be Created
1. 🆕 New dataset download scripts
2. 🆕 Dataset cleaning/validation scripts
3. 🆕 Training scripts (if training locally)
4. 🆕 New model checkpoints
5. 🆕 New GGUF exports
6. 🆕 New evaluation reports

---

## 11. Current Known Issues to Address

### Critical Issues (Must Fix)
1. ❌ **Refusal behavior completely absent**
   - 5K refusal examples ineffective
   - Model answers any question
   - No Python specialization enforcement

2. ❌ **Repetition artifacts**
   - "globals", "LoadScene", "zoekt", "/apache"
   - May indicate dataset contamination
   - Needs investigation before v2 training

### Important Issues (Should Fix)
3. ⚠️ **Prompt format mismatch**
   - Training format unknown
   - Inference uses plain prompts
   - May need explicit formatting

4. ⚠️ **Technical errors in responses**
   - TypeError vs IndexError confusion
   - Missing code examples when requested

### Minor Issues (Nice to Fix)
5. ⚠️ **Generates beyond request**
   - Provides extra examples not asked for
   - May need better stop sequences

6. ⚠️ **Verbose responses**
   - Not always beginner-friendly
   - Could be more concise

---

## 12. Dataset Download Plan

### Target Dataset
```
iamtarun/python_code_instructions_18k_alpaca
```

**Note**: This is the **SAME dataset** already used! 

### ⚠️ CRITICAL DISCOVERY

**The existing training data ALREADY uses this dataset!**

From `prepare_data.py` line 67:
```python
python_dataset = load_dataset("iamtarun/python_code_instructions_18k_alpaca", split='train')
```

**Implications**:
1. ❌ Re-downloading same dataset will NOT improve model
2. ❌ No new Python knowledge will be added
3. ✅ Can use existing data for further analysis
4. ✅ Need to find DIFFERENT dataset for improvement

### Alternative Actions
**Option A**: Search for DIFFERENT high-quality Python dataset
**Option B**: Focus on fixing refusal behavior with better data
**Option C**: Improve existing dataset quality through cleaning

**Recommendation**: **STOP** and clarify with user if they meant a different dataset, or if they want to:
- Clean/improve existing dataset
- Add completely different Python dataset
- Focus on refusal behavior improvement

---

## 13. Recommendations Before Proceeding

### Immediate Questions for User
1. ❓ Was the intent to use a DIFFERENT Python dataset? (Current uses same dataset)
2. ❓ Should we focus on cleaning/improving existing data?
3. ❓ Should we prioritize fixing refusal behavior?
4. ❓ Is local training planned, or continue using Google Colab?

### Suggested Next Steps

#### If Using Different Dataset:
1. Identify alternative high-quality Python dataset
2. Download and audit new dataset
3. Combine with existing or use separately
4. Retrain with better prompt format

#### If Improving Existing Data:
1. Audit existing 18K examples for quality
2. Remove duplicates and low-quality samples
3. Fix repetition artifacts in training data
4. Retrain with cleaned dataset

#### If Focusing on Refusal:
1. Create better refusal examples (40-50% ratio)
2. Use natural language refusals
3. Include Python-redirect examples
4. Add system prompt to training

---

## 14. Summary

**Project Status**: ✅ Model trained, exported, and tested

**Current Model**:
- Python capabilities: Good ✅
- Refusal behavior: Failed ❌
- Performance: Excellent ✅
- Stability: No issues ✅

**Training Dataset**:
- Size: 23,612 examples (18K Python + 5K refusal)
- Source: Same as requested dataset (already downloaded)
- Location: `data/training_data.jsonl`
- Status: **DO NOT MODIFY**

**Critical Finding**:
⚠️ **The requested dataset (`iamtarun/python_code_instructions_18k_alpaca`) is ALREADY in the training data!**

**Recommendation**:
🛑 **PAUSE** and confirm with user:
- Different dataset intended?
- Focus on quality improvement?
- Focus on refusal behavior?
- Proceed with re-training approach?

**Next Action**: Await user clarification before proceeding with dataset download

---

**Audit Completed**: 2026-09-24  
**Status**: ✅ Comprehensive audit complete  
**Recommendation**: Clarify dataset intentions before proceeding
