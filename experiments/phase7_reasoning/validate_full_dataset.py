"""
VASUKI Phase 7: Dataset Pre-Training Quality Gate & Hash Verification
Validates:
1. File existence and cryptographic SHA-256 hashes
2. JSONL parsing integrity
3. Prompt & Response token budget adherence
4. Python AST syntax correctness on code blocks
5. Zero leakage between training and validation sets
"""

import sys
import os
import json
import hashlib
from pathlib import Path
from reasoning_schema import validate_ast, extract_python_code
