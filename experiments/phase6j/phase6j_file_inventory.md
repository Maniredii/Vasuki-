# Phase 6J Root Cause Investigation - File Inventory

**Date**: 2026-09-23  
**Purpose**: Complete file mapping before dataset audit

---

## MODELS

| File | Location | Size | Purpose | Status |
|------|----------|------|---------|--------|
| `qwen2.5-coder-0.5b.Q4_K_M.gguf` | Root | 379.38 MB | Original baseline model | ✅ Preserved |
| `qwen2.5-coder-0.5b.F16.gguf` | Root | 948.1 MB | Full precision original | ✅ Preserved |
| `vasuki_phase6i.Q4_K_M.gguf` | Root | 379.38 MB | Phase 6I trained (FAILED) | ✅ Preserved |

---

## TRAINING DATASETS

### Original Data
| File | Location | Purpose | Status |
|------|----------|---------|--------|
| `training_data.jsonl` | `D:\VASUKI\data\` | Original 23K training data | ✅ Preserved |

### Phase 6E/6F Datasets
| File | Location | Purpose | Status |
|------|----------|---------|--------|
| `training_candidate.jsonl` | `D:\VASUKI\datasets\phase6e\generated\` | Phase 6F 1,082 examples | ✅ Preserved |
| `evaluation_set.jsonl` | `D:\VASUKI\datasets\phase6e\` | 64 eval examples | ✅ Preserved |

### Phase 6I Cleaned Dataset
| File | Location | Purpose | Status |
|------|----------|---------|--------|
| `training_clean.jsonl` | `D:\VASUKI\experiments\phase6i\` | 1,073 examples (removed 9 overlaps) | ⚠️ AUDIT REQUIRED |

---

## DATASET GENERATION SCRIPTS

| File | Location | Purpose |
|------|----------|---------|
| `generate_phase6e_dataset.py` | `D:\VASUKI\scripts\` | **KEY**: Generated Phase 6E/6F data |
| `validate_phase6e_dataset.py` | `D:\VASUKI\scripts\` | Validated Phase 6E/6F data |
| `create_evaluation_set.py` | `D:\VASUKI\scripts\` | Created eval set |
| `audit_refusal_dataset.py` | `D:\VASUKI\scripts\` | Audited old refusal data |
| `fix_contamination.py` | `D:\VASUKI\experiments\phase6i\` | Removed train/eval overlap |
| `verify_dataset.py` | `D:\VASUKI\experiments\phase6i\` | Pre-training verification |

---

## TRAINING SCRIPTS

| File | Location | Purpose |
|------|----------|---------|
| `phase6i_training.py` | `D:\VASUKI\experiments\phase6i\` | Phase 6I training script |
| `phase6i_training_config.json` | `D:\VASUKI\experiments\phase6i\` | Phase 6I config |
| `prepare_data.py` | `D:\VASUKI\scripts\` | Original data preparation |

---

## DIAGNOSTIC REPORTS

| File | Location | Purpose |
|------|----------|---------|
| `PHASE6I_DIAGNOSTIC_FINAL.md` | `D:\VASUKI\experiments\phase6i\` | Complete diagnostic (model redirects Python) |
| `phase6i_pretraining_dataset_report.md` | `D:\VASUKI\experiments\phase6i\` | Dataset verification report |
| `phase6i_inspection_report.md` | `D:\VASUKI\experiments\phase6i\` | Project inspection |

---

## EVALUATION SCRIPTS AND RESULTS

| File | Location | Purpose |
|------|----------|---------|
| `run_comparison_tests.ps1` | `D:\VASUKI\experiments\phase6i\` | Comparison test script |
| `test_results/` | `D:\VASUKI\experiments\phase6i\` | Test outputs (8 tests) |
| `test1_python_explanation.txt` - `test8_poem.txt` | `D:\VASUKI\experiments\phase6i\` | Individual test prompts |

---

## INFERENCE TOOLS

| File | Location | Purpose |
|------|----------|---------|
| `llama-cli.exe` | `D:\VASUKI\tools\llama.cpp\` | Inference runtime |
| `inspect_metadata.py` | Root | Metadata inspector |
| `quick_metadata.py` | Root | Quick metadata check |
| `validate_gguf.py` | Root | GGUF validator |

---

## CONFIGURATION FILES

| File | Location | Purpose |
|------|----------|---------|
| `Modelfile` | Root | Ollama config |
| `requirements.txt` | Root | Python dependencies |

---

## KEY FILES TO AUDIT

### Priority 1: Dataset Generation Logic
1. **`generate_phase6e_dataset.py`** - How were labels assigned?
2. **`training_clean.jsonl`** - Actual training data used
3. **`training_candidate.jsonl`** - Original Phase 6F data

### Priority 2: Training Configuration
4. **`phase6i_training.py`** - Prompt formatting during training
5. **`phase6i_training_config.json`** - Training parameters

### Priority 3: Evaluation
6. **`test_results/`** - Actual model outputs showing failure

---

## AUDIT PLAN

1. ✅ File inventory complete
2. ⏳ Inspect dataset schema (`training_clean.jsonl`)
3. ⏳ Analyze generation script (`generate_phase6e_dataset.py`)
4. ⏳ Audit labels vs responses
5. ⏳ Check prompt formatting
6. ⏳ Identify contamination
7. ⏳ Create corrected Phase 6J dataset

---

**Status**: File inventory complete - Ready for Phase 2 (Dataset Schema Audit)
