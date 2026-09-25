#!/usr/bin/env python3
"""
Phase 6H: Inference Workaround Testing
Systematically tests 9 configurations (3 formats × 3 parameter sets) on 30 prompts
"""

import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple
import re

# Paths
LLAMA_CLI = r"D:\VASUKI\tools\llama.cpp\llama-cli.exe"
MODEL_PATH = r"D:\VASUKI\qwen2.5-coder-0.5b.Q4_K_M.gguf"
PROMPTS_FILE = r"D:\VASUKI\datasets\phase6h\baseline_30_prompts.jsonl"
OUTPUT_DIR = Path(r"D:\VASUKI\reports\phase6h_inference\results")

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Prompt format templates
FORMATS = {
    "format_a_alpaca": {
        "name": "Alpaca Training Format",
        "template": "### Instruction:\n{instruction}\n\n### Response:",
        "stop": ["###", "\n\n\n"],
    },
    "format_b_system": {
        "name": "Explicit System Prompt",
        "template": """You are Vasuki, a specialized AI assistant focused exclusively on Python programming.

YOUR CAPABILITIES:
- Answer Python programming questions
- Help with Python interop (calling other languages from Python or vice versa)
- Compare Python with other languages
- Convert code to/from Python

YOUR LIMITATIONS:
- For pure non-Python programming: Redirect to appropriate resources
- For non-programming topics: Politely refuse

USER QUESTION: {instruction}

YOUR RESPONSE:""",
        "stop": ["USER QUESTION:", "\n\n\n"],
    },
    "format_c_minimal": {
        "name": "Minimal Direct Prompt",
        "template": "{instruction}",
        "stop": ["\n\n\n"],
    }
}

# Parameter configurations
PARAM_CONFIGS = {
    "config_1_conservative": {
        "name": "Conservative (Low Temp, High Repeat Penalty)",
        "temp": 0.2,
        "top_p": 0.9,
        "repeat_penalty": 1.2,
    },
    "config_2_moderate": {
        "name": "Moderate (Balanced)",
        "temp": 0.5,
        "top_p": 0.9,
        "repeat_penalty": 1.1,
    },
    "config_3_creative": {
        "name": "Creative (Higher Temp, Lower Penalty)",
        "temp": 0.7,
        "top_p": 0.95,
        "repeat_penalty": 1.05,
    }
}

def load_prompts() -> List[Dict]:
    """Load the 30 baseline prompts"""
    prompts = []
    with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            prompts.append(json.loads(line.strip()))
    return prompts

def run_inference(prompt: str, format_key: str, config_key: str) -> Tuple[str, float, bool]:
    """
    Run single inference test
    Returns: (output, inference_time, had_error)
    """
    format_config = FORMATS[format_key]
    param_config = PARAM_CONFIGS[config_key]
    
    # Format the prompt
    full_prompt = format_config["template"].format(instruction=prompt)
    
    # Build command
    cmd = [
        LLAMA_CLI,
        "-m", MODEL_PATH,
        "-c", "2048",
        "-n", "256",
        "-t", "8",
        "--temp", str(param_config["temp"]),
        "--top-p", str(param_config["top_p"]),
        "--repeat-penalty", str(param_config["repeat_penalty"]),
        "-p", full_prompt,
        "--single-turn",
        "--no-display-prompt"
    ]
    
    # Add stop sequences
    for stop_seq in format_config["stop"]:
        cmd.extend(["--reverse-prompt", stop_seq])
    
    try:
        start_time = time.time()
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8',
            errors='replace'
        )
        inference_time = time.time() - start_time
        
        output = result.stdout.strip()
        had_error = result.returncode != 0
        
        return output, inference_time, had_error
        
    except subprocess.TimeoutExpired:
        return "[TIMEOUT - 30s exceeded]", 30.0, True
    except Exception as e:
        return f"[ERROR: {str(e)}]", 0.0, True

def classify_response(response: str, expected_category: str) -> Dict[str, bool]:
    """
    Classify response across 11 binary flags
    """
    response_lower = response.lower()
    
    # Check for repetition artifacts
    has_repetition = bool(re.search(r'(\b\w+\b)(\s+\1){5,}', response))
    
    # Check for artifacts
    artifacts = ["zoekt", "zilla", "ologist", "countertops", "Assistant"]
    has_artifact = any(artifact.lower() in response_lower for artifact in artifacts)
    
    # Check for Python content
    python_indicators = [
        "python", "def ", "class ", "import ", "pip install",
        "list", "dict", "tuple", "numpy", "pandas", "django", "flask"
    ]
    mentions_python = any(indicator in response_lower for indicator in python_indicators)
    
    # Check for code
    has_code = bool(re.search(r'(def |class |import |for .+ in |if .+:|```)', response))
    
    # Check for other languages
    other_langs = ["java", "javascript", "rust", "c++", "golang", "kotlin"]
    mentions_other_lang = any(lang in response_lower for lang in other_langs)
    
    # Check for redirection phrases
    redirect_phrases = [
        "i cannot", "i can't", "outside my scope", "not my specialty",
        "specialized in python", "focused on python", "recommend", "suggest"
    ]
    has_redirect = any(phrase in response_lower for phrase in redirect_phrases)
    
    # Check for refusal phrases
    refuse_phrases = [
        "i cannot answer", "i can't help with that", "not a programming",
        "only assist with python", "only handle python"
    ]
    has_refusal = any(phrase in response_lower for phrase in refuse_phrases)
    
    # Check answer quality
    is_substantive = len(response.split()) >= 10 and not has_repetition
    
    # Expected behavior based on category
    should_answer_python = expected_category.startswith(("python_", "interop_", "comparison_", "conversion_"))
    should_redirect = expected_category.startswith("redirect_")
    should_refuse = expected_category.startswith("refuse_")
    
    # Correct behavior flags
    correct_answer = should_answer_python and mentions_python and is_substantive and not has_redirect
    correct_redirect = should_redirect and (has_redirect or mentions_other_lang) and not has_code
    correct_refuse = should_refuse and has_refusal and not mentions_python and not has_code
    
    return {
        "has_repetition": has_repetition,
        "has_artifact": has_artifact,
        "mentions_python": mentions_python,
        "has_code": has_code,
        "mentions_other_lang": mentions_other_lang,
        "has_redirect": has_redirect,
        "has_refusal": has_refusal,
        "is_substantive": is_substantive,
        "correct_answer": correct_answer,
        "correct_redirect": correct_redirect,
        "correct_refuse": correct_refuse,
    }

def run_all_tests():
    """Run all 270 tests (9 configs × 30 prompts)"""
    prompts = load_prompts()
    
    print(f"Phase 6H: Starting inference testing")
    print(f"Total tests: {len(FORMATS)} formats × {len(PARAM_CONFIGS)} configs × {len(prompts)} prompts = {len(FORMATS) * len(PARAM_CONFIGS) * len(prompts)} tests")
    print("=" * 80)
    
    all_results = []
    test_num = 0
    total_tests = len(FORMATS) * len(PARAM_CONFIGS) * len(prompts)
    
    for format_key, format_info in FORMATS.items():
        for config_key, config_info in PARAM_CONFIGS.items():
            config_name = f"{format_key}_{config_key}"
            print(f"\nTesting: {format_info['name']} + {config_info['name']}")
            print("-" * 80)
            
            config_results = []
            
            for prompt_data in prompts:
                test_num += 1
                prompt_id = prompt_data["id"]
                instruction = prompt_data["instruction"]
                category = prompt_data["category"]
                
                print(f"  [{test_num}/{total_tests}] Prompt {prompt_id}: {category[:20]}...", end=" ", flush=True)
                
                # Run inference
                output, inference_time, had_error = run_inference(instruction, format_key, config_key)
                
                # Classify response
                classification = classify_response(output, category)
                
                result = {
                    "test_id": test_num,
                    "prompt_id": prompt_id,
                    "category": category,
                    "instruction": instruction,
                    "format": format_key,
                    "config": config_key,
                    "output": output,
                    "inference_time": inference_time,
                    "had_error": had_error,
                    **classification
                }
                
                config_results.append(result)
                all_results.append(result)
                
                # Status indicator
                if had_error:
                    status = "❌ ERROR"
                elif classification["has_repetition"]:
                    status = "🔁 REPEAT"
                elif classification["correct_answer"]:
                    status = "✅ ANSWER"
                elif classification["correct_redirect"]:
                    status = "➡️ REDIRECT"
                elif classification["correct_refuse"]:
                    status = "🚫 REFUSE"
                else:
                    status = "⚠️ UNCLEAR"
                
                print(f"{status} ({inference_time:.1f}s)")
            
            # Save config-specific results
            output_file = OUTPUT_DIR / f"{config_name}.jsonl"
            with open(output_file, 'w', encoding='utf-8') as f:
                for result in config_results:
                    f.write(json.dumps(result, ensure_ascii=False) + "\n")
            
            print(f"✓ Saved results to {output_file.name}")
    
    # Save all results
    all_results_file = OUTPUT_DIR / "all_results.jsonl"
    with open(all_results_file, 'w', encoding='utf-8') as f:
        for result in all_results:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
    
    print("\n" + "=" * 80)
    print(f"✓ Phase 6H testing complete!")
    print(f"✓ Total tests run: {len(all_results)}")
    print(f"✓ Results saved to: {OUTPUT_DIR}")
    print("\nNext: Run analyze_phase6h_results.py to generate metrics and comparison report")

if __name__ == "__main__":
    run_all_tests()
