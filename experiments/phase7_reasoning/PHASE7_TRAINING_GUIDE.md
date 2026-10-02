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

