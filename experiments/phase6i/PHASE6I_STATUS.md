# Phase 6I: Training Experiment Status

**Date**: 2026-09-23  
**Experiment ID**: phase6i_20260923  
**Status**: 🟡 READY TO TRAIN (Pending User Action)

---

## Checklist

### ✅ Pre-Training Tasks (COMPLETE)

- [x] Experiment directory created (`D:\VASUKI\experiments\phase6i\`)
- [x] Phase 6F dataset loaded (1,082 original examples)
- [x] Training/evaluation contamination detected (9 examples)
- [x] Clean training dataset created (1,073 examples)
- [x] Dataset verification passed (0 errors, 1 warning)
- [x] Training script created (`phase6i_training.py`)
- [x] Training configuration documented (`phase6i_training_config.json`)
- [x] Pre-training report generated (`phase6i_pretraining_dataset_report.md`)

### 🟡 Training Tasks (PENDING)

- [ ] Upload files to Google Colab
  - [ ] `phase6i_training.py`
  - [ ] `training_clean.jsonl`
- [ ] Set Colab runtime to GPU (T4 or better)
- [ ] Run training script
- [ ] Monitor training progress (~15-30 minutes)
- [ ] Verify training completed successfully
- [ ] Download outputs:
  - [ ] `phase6i_training_log.json`
  - [ ] `phase6i_training_summary.md`
  - [ ] `vasuki_phase6i.Q4_K_M.gguf`
  - [ ] `adapter/` folder
  - [ ] `merged/` folder

### ⬜ Post-Training Tasks (NOT STARTED)

- [ ] Verify GGUF file integrity (SHA256 hash)
- [ ] Test model loads in llama.cpp
- [ ] Run baseline evaluation (original model)
- [ ] Run trained model evaluation
- [ ] Generate comparison metrics
- [ ] Analyze regressions
- [ ] Create final Phase 6I report
- [ ] Decision: proceed to Phase 6J or iterate

---

## Files Ready for Training

Located in: `D:\VASUKI\experiments\phase6i\`

| File | Size | Purpose | Status |
|------|------|---------|--------|
| `training_clean.jsonl` | ~400 KB | Training data (1,073 examples) | ✅ Ready |
| `phase6i_training.py` | ~13 KB | Training script | ✅ Ready |
| `phase6i_training_config.json` | ~2 KB | Configuration reference | ✅ Ready |
| `phase6i_pretraining_dataset_report.md` | ~3 KB | Verification report | ✅ Complete |
| `verify_dataset.py` | ~14 KB | Verification script | ✅ Complete |
| `fix_contamination.py` | ~2 KB | Contamination removal | ✅ Complete |

---

## Dataset Summary

### Final Training Dataset

- **File**: `training_clean.jsonl`
- **Total Examples**: 1,073
- **Removed**: 9 (overlapping with evaluation set)

### Distribution

| Type | Count | Percentage |
|------|-------|-----------|
| Answer (Python) | 545 | 50.8% |
| Redirect (Non-Python) | 524 | 48.8% |
| Refuse (Non-programming) | 4 | 0.4% |

**Balance**: 1.04:1 answer/redirect ratio (nearly perfect)

### Quality Metrics

- ✅ Zero training/eval overlap
- ✅ Zero old contamination
- ✅ Zero Python in redirect/refuse
- ✅ All sequences under 2,048 tokens
- ✅ Avg sequence length: 64 tokens

---

## Training Configuration Summary

### Model
- **Base**: unsloth/Qwen2.5-Coder-0.5B
- **Method**: QLoRA (4-bit)
- **Max Seq**: 2,048 tokens

### LoRA
- **r**: 16
- **alpha**: 16
- **dropout**: 0.0

### Training
- **Batch size**: 8 (effective)
- **Steps**: 200 (~1.5 epochs)
- **Learning rate**: 2e-4
- **Optimizer**: adamw_8bit

---

## Safety Protections

All original files protected:

- ✅ `D:\VASUKI\qwen2.5-coder-0.5b.Q4_K_M.gguf` (original model)
- ✅ `D:\VASUKI\Modelfile` (original config)
- ✅ `D:\VASUKI\data\training_data.jsonl` (original dataset)
- ✅ `D:\VASUKI\datasets\phase6e\generated\training_candidate.jsonl` (Phase 6F dataset)
- ✅ `D:\VASUKI\datasets\phase6e\evaluation_set.jsonl` (evaluation set)
- ✅ All Phase 6D reports and analysis

**New files only created in**: `D:\VASUKI\experiments\phase6i\`

---

## Expected Training Outcomes

### Success Criteria

Post-training evaluation should show:

1. **Python Capability**: Maintained ≥80% (currently 100%)
2. **Redirect Behavior**: Achieved ≥50% (currently 0%)
3. **Refuse Behavior**: Achieved ≥60% (currently 0%)
4. **Repetition Rate**: Reduced to ≤20% (currently 60%)

### Acceptable Outcomes

- ✅ Python accuracy remains high (≥80%)
- ✅ Redirect/refuse behaviors emerge
- ✅ Repetition decreases significantly
- ⚠️ Some edge cases may still fail

### Unacceptable Outcomes

- ❌ Python accuracy drops below 80%
- ❌ Model refuses Python questions
- ❌ New artifacts or loops appear
- ❌ Training loss becomes NaN

---

## Next Actions

### Immediate (User)

1. **Upload to Google Colab**:
   - `phase6i_training.py`
   - `training_clean.jsonl`

2. **Run training**:
   ```python
   !python phase6i_training.py
   ```

3. **Download outputs**:
   - Training logs
   - GGUF model
   - Adapters

### After Training (Agent)

1. Verify model integrity
2. Run baseline evaluation
3. Run trained model evaluation
4. Generate comparison report
5. Analyze results
6. Provide recommendation

---

## Training Timeline

| Phase | Estimated Duration | Status |
|-------|-------------------|--------|
| Setup & Upload | 5 minutes | ⏸️ Waiting |
| Training | 15-30 minutes | ⏸️ Waiting |
| Export & Download | 5 minutes | ⏸️ Waiting |
| Evaluation | 30 minutes | ⏸️ Waiting |
| Analysis & Report | 20 minutes | ⏸️ Waiting |
| **Total** | **~75-90 minutes** | ⏸️ Waiting |

---

## Troubleshooting Reference

### Common Issues

1. **Out of Memory**
   - Solution: Reduce batch size to 1, increase accumulation to 8

2. **CUDA Not Available**
   - Solution: Change Colab runtime to GPU

3. **File Not Found**
   - Solution: Upload `training_clean.jsonl` to Colab

4. **Training Loss NaN**
   - Solution: Reduce learning rate to 1e-4

---

## Important Reminders

### During Training

- ⚠️ Do NOT modify original model files
- ⚠️ Do NOT modify original datasets
- ⚠️ Monitor training loss (should decrease)
- ⚠️ Watch VRAM usage (should be <8GB)

### After Training

- ❌ Do NOT automatically start another run
- ❌ Do NOT delete baseline model
- ❌ Do NOT skip evaluation
- ✅ Run full comparison first
- ✅ Wait for approval before Phase 6J

---

## Contact Points

If training fails or produces unexpected results:

1. Check training logs for errors
2. Verify dataset was uploaded correctly
3. Confirm GPU was available
4. Review loss curve for instability
5. Check VRAM didn't exceed capacity

---

**Status**: Ready to train  
**Approval**: Granted for controlled experiment  
**Next**: User action required (upload to Colab and run)

**Last Updated**: 2026-09-23
