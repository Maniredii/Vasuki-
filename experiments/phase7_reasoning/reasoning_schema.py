"""
VASUKI Phase 7: Reasoning Schema & Verification Framework
Provides structured templates, AST validation, execution sandbox, and quality gates for code reasoning.
"""

import ast
import re
import sys
from typing import Dict, Any, List, Optional, Tuple

# Set UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def build_reasoning_response(
    strategy: str,
    edge_cases: List[str],
    code: str,
    time_complexity: str,
    space_complexity: str,
    preamble: Optional[str] = None
) -> str:
    """
    Constructs a disciplined, 4-tier structured reasoning response.
    Designed specifically to maximize inference reasoning in 0.5B models without bloat.
    """
    parts = []
    
    if preamble:
        parts.append(preamble.strip() + "\n")
        
    parts.append("### Problem Analysis & Strategy")
    parts.append(strategy.strip())
    
    parts.append("\n### Edge Cases Considered")
    for ec in edge_cases:
        parts.append(f"- {ec.strip()}")
        
    parts.append("\n### Python Implementation")
    clean_code = code.strip()
    if not clean_code.startswith("```python"):
        clean_code = f"```python\n{clean_code}\n```"
    parts.append(clean_code)
    
    parts.append("\n### Complexity Analysis")
    parts.append(f"- **Time Complexity:** {time_complexity.strip()}")
    parts.append(f"- **Space Complexity:** {space_complexity.strip()}")
    
    return "\n".join(parts)


def build_debug_response(
    flaw_analysis: str,
    step_trace: List[str],
    fixed_code: str,
    key_takeaway: str
) -> str:
    """
    Constructs a step-by-step debugging & root-cause reasoning response.
