# VASUKI Phase 7: Edge Reasoning Training Guide

This guide walks you through fine-tuning the **VASUKI Phase 7** Reasoning Model on Google Colab (Tesla T4 GPU) or any cloud GPU instance.

---

## 1. Overview of Artifacts

| File | Purpose | Location |
|:---|:---|:---|
| **`phase7_2_expanded_corpus.jsonl`** | **Expanded Master Corpus (5,486 records, 100% AST pass)** | [`experiments/phase7_reasoning/phase7_2_expanded_corpus.jsonl`](file:///d:/VASUKI/experiments/phase7_reasoning/phase7_2_expanded_corpus.jsonl) |
| **`phase7_1_balanced_corpus.jsonl`** | Balanced Theory + Code Corpus (3,086 records) | [`experiments/phase7_reasoning/phase7_1_balanced_corpus.jsonl`](file:///d:/VASUKI/experiments/phase7_reasoning/phase7_1_balanced_corpus.jsonl) |
| **`phase7_training.py`** | Standalone automated training script (auto-detects Phase 7.2 / 7.1) | [`experiments/phase7_reasoning/phase7_training.py`](file:///d:/VASUKI/experiments/phase7_reasoning/phase7_training.py) |
| **`phase7_training_colab.ipynb`** | Google Colab interactive notebook | [`experiments/phase7_reasoning/phase7_training_colab.ipynb`](file:///d:/VASUKI/experiments/phase7_reasoning/phase7_training_colab.ipynb) |
| **`validate_full_dataset.py`** | Pre-training cryptographic and AST quality gate | [`experiments/phase7_reasoning/validate_full_dataset.py`](file:///d:/VASUKI/experiments/phase7_reasoning/validate_full_dataset.py) |

---

## 2. Step-by-Step Training Instructions (Google Colab)

### Step 1: Open Google Colab
1. Go to [Google Colab](https://colab.research.google.com).
2. Upload [`phase7_training_colab.ipynb`](file:///d:/VASUKI/experiments/phase7_reasoning/phase7_training_colab.ipynb).

### Step 2: Set GPU Accelerator
1. Click **Runtime** $\rightarrow$ **Change runtime type**.
2. Under Hardware accelerator, select **T4 GPU**.
3. Click **Save**.

### Step 3: Upload Files & Execute
1. Run **Cell 1** to install Unsloth and QLoRA dependencies.
2. Run **Cell 2** and upload:
   - `phase7_2_expanded_corpus.jsonl` (Recommended: 5,486 records with Theory, Algorithms & Real-world Scripts)
   - `phase7_training.py`
   *(Note: `phase7_training.py` automatically detects `phase7_2_expanded_corpus.jsonl` and auto-configures 1,200 steps with response loss masking)*
3. Run **Cell 3** to launch the training run:
   - **Target Model:** `unsloth/Qwen2.5-Coder-0.5B`
   - **Steps:** 1,200 steps (~1.8 epochs over 5,486 records, effective batch size 8).
   - **Estimated Time:** ~20–25 minutes on Tesla T4.
   - **Loss Masking:** Response-only (`train_on_responses_only`), ensuring maximum gradient efficiency on reasoning and code.

### Step 4: Download Model Artifacts
1. Run **Cell 4** to download `vasuki_phase7_output.zip`.
2. Extract the resulting GGUF model `vasuki_phase7.Q4_K_M.gguf` into your local `D:\VASUKI\` root directory.

---

## 3. Local Verification & Retesting

Once downloaded, update the default model pointer or test directly:

```bash
# Direct test with the new Phase 7 reasoning engine
python test_vasuki.py "Write an optimal solution for the Trapping Rain Water problem"
```

The output will now display structured Chain-of-Thought (CoT) reasoning:
- Problem Analysis & Algorithmic Strategy
- Edge Cases Considered
- Verified Python Implementation
- Time and Space Complexity Proof


### Mode Collapse & Repetition Prevention
- Always use `unsloth/Qwen2.5-Coder-0.5B-Instruct` as base model.
- Keep learning rate at 5e-5 and max steps <= 500 to prevent degradation.
