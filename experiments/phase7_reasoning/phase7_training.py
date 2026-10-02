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
