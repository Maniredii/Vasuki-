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
    """
    parts = [
        "### Root Cause Analysis",
        flaw_analysis.strip(),
        "\n### Execution Trace (Failure Scenario)",
    ]
    for step in step_trace:
        parts.append(f"1. {step.strip()}" if not step.strip().startswith("1.") else step.strip())
        
    parts.append("\n### Corrected Implementation")
    clean_code = fixed_code.strip()
    if not clean_code.startswith("```python"):
        clean_code = f"```python\n{clean_code}\n```"
    parts.append(clean_code)
    
    parts.append("\n### Key Takeaway & Prevention")
    parts.append(key_takeaway.strip())
    
    return "\n".join(parts)


def build_optimization_response(
    baseline_analysis: str,
    optimization_strategy: str,
    optimized_code: str,
    speedup_comparison: str
) -> str:
    """
    Constructs an algorithmic optimization & trade-off reasoning response.
    """
    parts = [
        "### Performance Bottleneck Analysis",
        baseline_analysis.strip(),
        "\n### Algorithmic Optimization Strategy",
        optimization_strategy.strip(),
        "\n### Optimized Python Implementation",
    ]
    clean_code = optimized_code.strip()
    if not clean_code.startswith("```python"):
        clean_code = f"```python\n{clean_code}\n```"
    parts.append(clean_code)
    
    parts.append("\n### Performance Comparison")
    parts.append(speedup_comparison.strip())
    
    return "\n".join(parts)


def extract_python_code(text: str) -> List[str]:
    """Extracts all python code blocks from markdown."""
    pattern = r"```(?:python)?\s*\n(.*?)\n```"
    matches = re.findall(pattern, text, re.DOTALL)
    if not matches:
        # Fallback to loose code block
        pattern_loose = r"```\s*\n(.*?)\n```"
        matches = re.findall(pattern_loose, text, re.DOTALL)
    return matches


def validate_ast(code: str) -> Tuple[bool, Optional[str]]:
    """Verifies that the Python code parses into a 100% valid AST."""
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"AST Error: {str(e)}"


def execute_in_sandbox(code: str, timeout_seconds: float = 2.0) -> Tuple[bool, Optional[str]]:
    """
    Safely executes code containing assertions in a restricted sandbox.
    Returns (True, None) if all assertions pass, (False, error_msg) otherwise.
    """
    # Restrict built-ins to safe operations
    safe_builtins = {
        k: v for k, v in __builtins__.items()
        if k not in ("eval", "exec", "open", "input", "__import__", "breakpoint")
    } if isinstance(__builtins__, dict) else {
        k: getattr(__builtins__, k) for k in dir(__builtins__)
        if k not in ("eval", "exec", "open", "input", "__import__", "breakpoint")
    }
    
    # Allow standard library modules commonly used in algorithms
    safe_modules = {}
    import math, collections, itertools, heapq, functools, bisect, typing
    safe_modules["math"] = math
    safe_modules["collections"] = collections
    safe_modules["itertools"] = itertools
    safe_modules["heapq"] = heapq
    safe_modules["functools"] = functools
    safe_modules["bisect"] = bisect
    safe_modules["typing"] = typing
    
    def restricted_import(name, *args, **kwargs):
        if name in safe_modules:
            return safe_modules[name]
        raise ImportError(f"Import of '{name}' is restricted in validation sandbox.")
        
    safe_builtins["__import__"] = restricted_import
    
    sandbox_globals = {
        "__builtins__": safe_builtins,
        "math": math,
        "collections": collections,
        "itertools": itertools,
        "heapq": heapq,
        "functools": functools,
        "bisect": bisect,
        "typing": typing,
        "List": typing.List,
