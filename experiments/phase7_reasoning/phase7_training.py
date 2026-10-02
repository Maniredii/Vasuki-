"""
VASUKI Phase 7: Edge Reasoning QLoRA Fine-Tuning Pipeline
Base Model: unsloth/Qwen2.5-Coder-0.5B (~490M parameters)
Corpus: phase7_reasoning_corpus.jsonl (2,571 verified records)
Validation: phase7_reasoning_val.jsonl (Held-out reasoning tasks)

Features:
- Structured Chain-of-Thought (CoT) reasoning conditioning
- Response-only loss masking (zero loss on instructions)
- Automatic GGUF 4-bit (Q4_K_M) quantization export for offline edge execution
"""

import os
import sys
import time
import json
import hashlib
import shutil
from pathlib import Path

# ============================================================================
# CONFIGURATION & HYPERPARAMETERS
# ============================================================================

EXPERIMENT_ID = "vasuki_phase7_reasoning"
BASE_MODEL = "unsloth/Qwen2.5-Coder-0.5B"
# Dataset Selection: Priority to Phase 7.2 Expanded Corpus (5,486 records)
EXPANDED_FILE = "phase7_2_expanded_corpus.jsonl"
BALANCED_FILE = "phase7_1_balanced_corpus.jsonl"
BASE_FILE = "phase7_reasoning_corpus.jsonl"

if os.path.exists(EXPANDED_FILE):
    TRAINING_DATA_FILE = EXPANDED_FILE
    MAX_STEPS = 1200      # ~1.8 epochs over 5,486 records with effective batch size 8
    EVAL_STEPS = 100
elif os.path.exists(BALANCED_FILE):
    TRAINING_DATA_FILE = BALANCED_FILE
    MAX_STEPS = 800       # ~2 epochs over 3,086 records
    EVAL_STEPS = 80
else:
    TRAINING_DATA_FILE = BASE_FILE
    MAX_STEPS = 650
    EVAL_STEPS = 65

VALIDATION_DATA_FILE = "phase7_reasoning_val.jsonl"
OUTPUT_DIR = "./phase7_output"
MAX_SEQ_LENGTH = 2048
RANDOM_SEED = 42

WARMUP_STEPS = 30
LEARNING_RATE = 2e-4
WEIGHT_DECAY = 0.01

RESPONSE_DELIMITER = "### Response:\n"
EOS_TOKEN = "<|im_end|>"

# LoRA Configuration
LORA_CONFIG = {
    "r": 16,
    "lora_alpha": 16,
    "lora_dropout": 0.05,
    "target_modules": [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    "bias": "none",
    "use_rslora": False,
}


def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def verify_environment():
    print("=" * 80)
    print("VASUKI Phase 7: Training Environment Verification")
    print("=" * 80)
    import torch
    print(f"Python Version:   {sys.version.split()[0]}")
    print(f"PyTorch Version:  {torch.__version__}")
    
    if not torch.cuda.is_available():
        print("[!] FATAL: No CUDA GPU detected! QLoRA requires an NVIDIA GPU (e.g. Google Colab T4).")
        return False
        
    gpu_name = torch.cuda.get_device_name(0)
    vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
    print(f"GPU Detected:     {gpu_name}")
    print(f"Total VRAM:       {vram_gb:.2f} GB")
    return True


def load_and_format_datasets():
    print("\n" + "=" * 80)
    print("Loading & Formatting Datasets")
    print("=" * 80)

    # Resolve training data file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    train_candidates = [
        TRAINING_DATA_FILE,
        os.path.join(script_dir, TRAINING_DATA_FILE),
        os.path.join("/content", TRAINING_DATA_FILE),
        os.path.join("experiments", "phase7_reasoning", TRAINING_DATA_FILE)
    ]
    resolved_train = None
    for cand in train_candidates:
        if os.path.exists(cand):
            resolved_train = cand
            break

    if not resolved_train:
        raise FileNotFoundError(f"Training dataset '{TRAINING_DATA_FILE}' not found in working directory or Colab environment.")

    print(f"[*] Reading training data from: {resolved_train}")
    with open(resolved_train, "r", encoding="utf-8") as f:
        train_records = [json.loads(line) for line in f if line.strip()]

    # Resolve validation data file path
    val_candidates = [
        VALIDATION_DATA_FILE,
        os.path.join(script_dir, VALIDATION_DATA_FILE),
        os.path.join("/content", VALIDATION_DATA_FILE),
        os.path.join("experiments", "phase7_reasoning", VALIDATION_DATA_FILE)
    ]
    resolved_val = None
    for cand in val_candidates:
        if os.path.exists(cand):
            resolved_val = cand
            break

    if resolved_val:
        print(f"[*] Reading validation data from: {resolved_val}")
        with open(resolved_val, "r", encoding="utf-8") as f:
            val_records = [json.loads(line) for line in f if line.strip()]
    else:
        # Graceful fallback: automatically carve out 50 samples or 2% for validation
        print(f"[*] Notice: '{VALIDATION_DATA_FILE}' not found. Auto-partitioning 50 records from training dataset for validation.")
        val_count = min(50, max(2, int(len(train_records) * 0.02)))
        val_records = train_records[-val_count:]
        train_records = train_records[:-val_count]

    def format_records(raw_records):
        formatted = []
        for r in raw_records:
            prompt = f"### Instruction:\n{r['instruction']}\n\n"
            if r.get('input'):
                prompt += f"### Input:\n{r['input']}\n\n"
            prompt += RESPONSE_DELIMITER
            clean_resp = r['response'].strip()
            full_text = prompt + clean_resp + "\n<|im_end|>\n"
            formatted.append({
                "prompt": prompt,
                "response": clean_resp + "\n<|im_end|>\n",
                "text": full_text
            })
        return formatted

    train_data = format_records(train_records)
    val_data = format_records(val_records)
    print(f"[*] Training Records Formatted:   {len(train_data)}")
    print(f"[*] Validation Records Formatted: {len(val_data)}")
    return train_data, val_data


def run_training():
    if not verify_environment():
        sys.exit(1)

    train_data, val_data = load_and_format_datasets()

    from unsloth import FastLanguageModel
    from datasets import Dataset
    from trl import SFTTrainer
    from transformers import TrainingArguments
    from unsloth import is_bfloat16_supported

    print("\n[*] Initializing FastLanguageModel from Unsloth...")
    model, tokenizer = FastLanguageModel.from_pretrained(
