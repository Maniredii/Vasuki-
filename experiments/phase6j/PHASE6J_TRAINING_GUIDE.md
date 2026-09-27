# VASUKI Phase 6J — Pilot QLoRA Training Guide

This guide provides step-by-step instructions to train the **VASUKI Phase 6J** pilot model on a free Google Colab GPU (Tesla T4) or any cloud GPU instance.

---

## 1. Overview of Artifacts

| File | Purpose | Location |
|:---|:---|:---|
| **`phase6j_training_colab.ipynb`** | Interactive Google Colab notebook | [`experiments/phase6j/phase6j_training_colab.ipynb`](file:///d:/VASUKI/experiments/phase6j/phase6j_training_colab.ipynb) |
| **`phase6j_training.py`** | Standalone automated Python training script | [`experiments/phase6j/phase6j_training.py`](file:///d:/VASUKI/experiments/phase6j/phase6j_training.py) |
| **`phase6j_training_candidate_diversified.jsonl`** | Verified training dataset (593 records) | [`experiments/phase6j/phase6j_training_candidate_diversified.jsonl`](file:///d:/VASUKI/experiments/phase6j/phase6j_training_candidate_diversified.jsonl) |
| **`phase6j_validation.jsonl`** | Held-out validation dataset (75 records) | [`experiments/phase6j/phase6j_validation.jsonl`](file:///d:/VASUKI/experiments/phase6j/phase6j_validation.jsonl) |
| **`pilot_training_config_reviewed.yaml`** | Exact reviewed hyperparameters | [`experiments/phase6j/pilot_training/pilot_training_config_reviewed.yaml`](file:///d:/VASUKI/experiments/phase6j/pilot_training/pilot_training_config_reviewed.yaml) |

---

## 2. Option A: Training via Google Colab Notebook (Recommended)

### Step 1: Open Google Colab
1. Navigate to [Google Colab](https://colab.research.google.com).
2. Click **Upload** and upload [`phase6j_training_colab.ipynb`](file:///d:/VASUKI/experiments/phase6j/phase6j_training_colab.ipynb).

### Step 2: Enable GPU Accelerator
1. In the Colab menu, click: **Runtime** $\rightarrow$ **Change runtime type**.
2. Select **T4 GPU** under Hardware accelerator.
3. Click **Save**.

### Step 3: Run Setup & Upload Datasets
1. Run **Cell 1 & Cell 2** to install Unsloth and check GPU VRAM.
2. In **Cell 3**, upload the two verified JSONL files from your local machine:
   - `phase6j_training_candidate_diversified.jsonl`
   - `phase6j_validation.jsonl`
3. The cell automatically checks the cryptographic SHA-256 hashes:
   - Training Hash: `af9714012101cba1e639bff0b946c78bdeea947f20b341f1803e4352310cc0e2`
   - Validation Hash: `db816d9bac321deda2aa80dce5552ff994006c42054bac638baf4a5647a4172d`

### Step 4: Execute Training
1. Run **Cell 4** to initialize `unsloth/Qwen2.5-Coder-0.5B` and inject the QLoRA adapters ($r=16, \alpha=16$).
2. Run **Cell 5** to format the datasets with response-only loss masking.
3. Run **Cell 6** to start the 220-step training run.
   - **Duration:** ~8 to 12 minutes on Tesla T4.
   - **Progress:** Validation loss is evaluated and logged every 50 steps.
4. Run **Cell 7** to view real-time test inference on sample Python and redirect prompts.

### Step 5: Download Trained Artifacts
1. Run **Cell 8** to package and download `vasuki_phase6j_output.zip`.
2. Extract the zip into your local repository at `D:\VASUKI\experiments\phase6j\phase6j_output\`.

---

## 3. Option B: Training via Standalone Python Script (Colab Terminal or Cloud VM)

If running in a cloud VM (e.g., RunPod, LambdaLabs, or Colab Terminal):

1. Upload the files to your working directory:
   - `phase6j_training.py`
   - `phase6j_training_candidate_diversified.jsonl`
   - `phase6j_validation.jsonl`
2. Install dependencies:
   ```bash
   pip install unsloth
   pip install --no-deps trl peft accelerate bitsandbytes
   ```
3. Run the training script:
   ```bash
   python phase6j_training.py
   ```
4. Output directory `./phase6j_output` will contain:
   - `adapter/` (Trained LoRA adapter weights: `adapter_model.safetensors` & config)
   - `training_summary.json` (Loss history and training metadata)
   - `vasuki_phase6j_output.zip` (Pre-packaged archive for download)

---

## 4. Key Training Parameters & What to Expect

- **Effective Batch Size:** 8 (2 per device $\times$ 4 gradient accumulation steps)
- **Max Steps:** 220 steps (~3 full epochs over 593 examples)
- **Loss Masking:** Only tokens after `### Response:\n` contribute to training loss
- **Expected Loss Trajectory:**
  - Initial Loss: ~2.4 – 2.8
  - Mid-Training (Step 100): ~1.6 – 1.9
  - Final Loss (Step 220): ~1.2 – 1.4
  - Validation Loss: Tracks training loss without significant divergence (indicating healthy generalization)
