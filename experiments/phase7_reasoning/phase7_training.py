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
