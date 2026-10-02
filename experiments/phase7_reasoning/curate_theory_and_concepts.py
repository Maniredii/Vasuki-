"""
VASUKI Phase 7.1: Multi-Source Theory, Concept & Reasoning Curator
Integrates:
1. sahil2801/CodeAlpaca-20k (Pure conceptual & theoretical CS/Python questions)
2. mlabonne/Evol-Instruct-Python-1k (Algorithmic reasoning & trade-offs)
3. Custom Concise Definition & ML Theory Pack (Solves subword loop collapse on short prompts)
4. Existing Phase 7 Verified Reasoning & Algorithmic Corpus (2,571 records)
"""

import sys
import os
import json
import re
from pathlib import Path
from datasets import load_dataset

from reasoning_schema import validate_ast, extract_python_code, estimate_token_count

BASE_DIR = Path("D:/VASUKI/experiments/phase7_reasoning")
CURRENT_CORPUS_FILE = BASE_DIR / "phase7_reasoning_corpus.jsonl"
OUT_THEORY_FILE = BASE_DIR / "curated_hf_theory.jsonl"
OUT_FULL_CORPUS_FILE = BASE_DIR / "phase7_1_balanced_corpus.jsonl"
OUT_REPORT_FILE = BASE_DIR / "phase7_1_curation_report.md"


# ============================================================================
