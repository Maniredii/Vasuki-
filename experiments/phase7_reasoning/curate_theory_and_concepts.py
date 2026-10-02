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
# 1. EXPANDED CONCISE DEFINITION & THEORY PACK
# ============================================================================

CONCISE_THEORY_PACK = [
    {
        "instruction": "explain decision tree in one line",
        "response": "A decision tree is a supervised machine learning model that makes predictions by recursively partitioning feature space along orthogonal, rule-based splits.",
        "category": "machine_learning_concepts"
    },
    {
        "instruction": "explain decision tree",
        "response": (
            "### Concept & Overview\n"
            "A Decision Tree is a supervised machine learning algorithm used for both classification and regression. "
            "It breaks down a complex dataset into smaller subsets by learning simple if-else decision rules inferred from data features.\n\n"
            "### Architectural Components\n"
            "- **Root Node:** The topmost node representing the entire dataset prior to any split.\n"
            "- **Decision / Internal Nodes:** Intermediate nodes evaluating a test condition on a specific feature (e.g., `age > 30` or `income <= 50000`).\n"
            "- **Leaf / Terminal Nodes:** Final output nodes carrying class labels (classification) or continuous numerical values (regression).\n"
            "- **Splitting Metrics:** Evaluated using Gini Impurity or Entropy (Information Gain) for classification, and Mean Squared Error (MSE) for regression.\n\n"
            "### Python Example (Scikit-Learn)\n"
            "```python\n"
            "from sklearn.tree import DecisionTreeClassifier\n"
            "\n"
            "# Initialize tree with depth constraint to prevent overfitting\n"
            "clf = DecisionTreeClassifier(max_depth=4, criterion='gini', random_state=42)\n"
