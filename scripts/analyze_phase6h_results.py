#!/usr/bin/env python3
"""
Phase 6H Results Analysis
Computes metrics across all 9 configurations and generates comparison report
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List

# Paths
RESULTS_DIR = Path(r"D:\VASUKI\reports\phase6h_inference\results")
OUTPUT_FILE = Path(r"D:\VASUKI\reports\phase6h_inference\phase6h_results.md")

def load_all_results() -> List[Dict]:
    """Load all results from all_results.jsonl"""
    results_file = RESULTS_DIR / "all_results.jsonl"
    results = []
    with open(results_file, 'r', encoding='utf-8') as f:
        for line in f:
            results.append(json.loads(line.strip()))
    return results

def compute_config_metrics(results: List[Dict], format_key: str, config_key: str) -> Dict:
    """Compute metrics for a specific configuration"""
    config_results = [r for r in results if r["format"] == format_key and r["config"] == config_key]
    
    if not config_results:
        return {}
    
    total = len(config_results)
    
    # Count by classification flags
    metrics = {
        "total_tests": total,
        "errors": sum(1 for r in config_results if r["had_error"]),
        "repetition_rate": sum(1 for r in config_results if r["has_repetition"]) / total * 100,
        "artifact_rate": sum(1 for r in config_results if r["has_artifact"]) / total * 100,
        "python_mention_rate": sum(1 for r in config_results if r["mentions_python"]) / total * 100,
        "code_generation_rate": sum(1 for r in config_results if r["has_code"]) / total * 100,
        "other_lang_mention_rate": sum(1 for r in config_results if r["mentions_other_lang"]) / total * 100,
        "redirect_rate": sum(1 for r in config_results if r["has_redirect"]) / total * 100,
        "refusal_rate": sum(1 for r in config_results if r["has_refusal"]) / total * 100,
        "substantive_rate": sum(1 for r in config_results if r["is_substantive"]) / total * 100,
        "correct_answer_rate": sum(1 for r in config_results if r["correct_answer"]) / total * 100,
        "correct_redirect_rate": sum(1 for r in config_results if r["correct_redirect"]) / total * 100,
        "correct_refuse_rate": sum(1 for r in config_results if r["correct_refuse"]) / total * 100,
        "avg_inference_time": sum(r["inference_time"] for r in config_results) / total,
    }
    
    # Count by expected category
    category_breakdown = defaultdict(lambda: {"total": 0, "correct": 0})
    for r in config_results:
        cat = r["category"]
        category_breakdown[cat]["total"] += 1
        
        # Determine if correct based on category prefix
        if cat.startswith(("python_", "interop_", "comparison_", "conversion_")) and r["correct_answer"]:
            category_breakdown[cat]["correct"] += 1
        elif cat.startswith("redirect_") and r["correct_redirect"]:
            category_breakdown[cat]["correct"] += 1
        elif cat.startswith("refuse_") and r["correct_refuse"]:
            category_breakdown[cat]["correct"] += 1
    
    # Calculate accuracy by category group
    python_cats = [cat for cat in category_breakdown if cat.startswith(("python_", "interop_", "comparison_", "conversion_"))]
    redirect_cats = [cat for cat in category_breakdown if cat.startswith("redirect_")]
    refuse_cats = [cat for cat in category_breakdown if cat.startswith("refuse_")]
    
    if python_cats:
        python_total = sum(category_breakdown[cat]["total"] for cat in python_cats)
        python_correct = sum(category_breakdown[cat]["correct"] for cat in python_cats)
        metrics["python_accuracy"] = python_correct / python_total * 100 if python_total > 0 else 0
    else:
        metrics["python_accuracy"] = 0
    
    if redirect_cats:
        redirect_total = sum(category_breakdown[cat]["total"] for cat in redirect_cats)
        redirect_correct = sum(category_breakdown[cat]["correct"] for cat in redirect_cats)
        metrics["redirect_accuracy"] = redirect_correct / redirect_total * 100 if redirect_total > 0 else 0
    else:
        metrics["redirect_accuracy"] = 0
    
    if refuse_cats:
        refuse_total = sum(category_breakdown[cat]["total"] for cat in refuse_cats)
        refuse_correct = sum(category_breakdown[cat]["correct"] for cat in refuse_cats)
        metrics["refuse_accuracy"] = refuse_correct / refuse_total * 100 if refuse_total > 0 else 0
    else:
        metrics["refuse_accuracy"] = 0
    
    # Overall accuracy
    total_correct = sum(1 for r in config_results if r["correct_answer"] or r["correct_redirect"] or r["correct_refuse"])
    metrics["overall_accuracy"] = total_correct / total * 100
    
    metrics["category_breakdown"] = dict(category_breakdown)
    
    return metrics

def generate_report(results: List[Dict]):
    """Generate comprehensive markdown report"""
    
    # Get unique formats and configs
    formats = sorted(set(r["format"] for r in results))
    configs = sorted(set(r["config"] for r in results))
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Phase 6H: Inference Workaround Test Results\n\n")
        f.write("**Test Date:** " + results[0].get("timestamp", "2026-09-23") + "\n")
        f.write(f"**Total Tests:** {len(results)} (9 configurations × 30 prompts)\n\n")
        
        f.write("## Executive Summary\n\n")
        f.write("Tested 3 prompt formats with 3 parameter configurations to determine if inference-level ")
        f.write("fixes can address refusal behavior issues without retraining.\n\n")
        
        # Compute all configs
        all_metrics = {}
        for format_key in formats:
            for config_key in configs:
                key = f"{format_key}_{config_key}"
                all_metrics[key] = compute_config_metrics(results, format_key, config_key)
        
        # Find best configuration
        best_overall = max(all_metrics.items(), key=lambda x: x[1].get("overall_accuracy", 0))
        best_python = max(all_metrics.items(), key=lambda x: x[1].get("python_accuracy", 0))
        best_redirect = max(all_metrics.items(), key=lambda x: x[1].get("redirect_accuracy", 0))
        best_refuse = max(all_metrics.items(), key=lambda x: x[1].get("refuse_accuracy", 0))
        worst_repetition = min(all_metrics.items(), key=lambda x: x[1].get("repetition_rate", 100))
        
        f.write("### Best Configurations\n\n")
        f.write(f"- **Overall Accuracy:** {best_overall[0]} ({best_overall[1]['overall_accuracy']:.1f}%)\n")
        f.write(f"- **Python Tasks:** {best_python[0]} ({best_python[1]['python_accuracy']:.1f}%)\n")
        f.write(f"- **Redirect Tasks:** {best_redirect[0]} ({best_redirect[1]['redirect_accuracy']:.1f}%)\n")
        f.write(f"- **Refuse Tasks:** {best_refuse[0]} ({best_refuse[1]['refuse_accuracy']:.1f}%)\n")
        f.write(f"- **Least Repetition:** {worst_repetition[0]} ({worst_repetition[1]['repetition_rate']:.1f}%)\n\n")
        
        # Detailed metrics table
        f.write("## Detailed Metrics by Configuration\n\n")
        f.write("| Configuration | Overall Acc | Python Acc | Redirect Acc | Refuse Acc | Repetition | Artifacts | Avg Time |\n")
        f.write("|---------------|-------------|------------|--------------|------------|------------|-----------|----------|\n")
        
        for key in sorted(all_metrics.keys()):
            m = all_metrics[key]
            config_display = key.replace("format_", "").replace("config_", "").replace("_", " + ")
            f.write(f"| {config_display} | ")
            f.write(f"{m['overall_accuracy']:.1f}% | ")
            f.write(f"{m['python_accuracy']:.1f}% | ")
            f.write(f"{m['redirect_accuracy']:.1f}% | ")
            f.write(f"{m['refuse_accuracy']:.1f}% | ")
            f.write(f"{m['repetition_rate']:.1f}% | ")
            f.write(f"{m['artifact_rate']:.1f}% | ")
            f.write(f"{m['avg_inference_time']:.1f}s |\n")
        
        f.write("\n")
        
        # Format comparison
        f.write("## Format Comparison\n\n")
        for format_key in formats:
            format_metrics = [all_metrics[k] for k in all_metrics if k.startswith(format_key)]
            avg_overall = sum(m["overall_accuracy"] for m in format_metrics) / len(format_metrics)
            avg_repetition = sum(m["repetition_rate"] for m in format_metrics) / len(format_metrics)
            
            f.write(f"### {format_key.replace('format_', '').replace('_', ' ').title()}\n\n")
            f.write(f"- **Avg Overall Accuracy:** {avg_overall:.1f}%\n")
            f.write(f"- **Avg Repetition Rate:** {avg_repetition:.1f}%\n")
            f.write(f"- **Configurations Tested:** {len(format_metrics)}\n\n")
        
        # Parameter config comparison
        f.write("## Parameter Configuration Comparison\n\n")
        for config_key in configs:
            config_metrics = [all_metrics[k] for k in all_metrics if k.endswith(config_key)]
            avg_overall = sum(m["overall_accuracy"] for m in config_metrics) / len(config_metrics)
            avg_python = sum(m["python_accuracy"] for m in config_metrics) / len(config_metrics)
            
            f.write(f"### {config_key.replace('config_', '').replace('_', ' ').title()}\n\n")
            f.write(f"- **Avg Overall Accuracy:** {avg_overall:.1f}%\n")
            f.write(f"- **Avg Python Accuracy:** {avg_python:.1f}%\n")
            f.write(f"- **Formats Tested:** {len(config_metrics)}\n\n")
        
        # Category-level analysis
        f.write("## Performance by Task Category\n\n")
        category_totals = defaultdict(lambda: {"total": 0, "correct": 0})
        for r in results:
            cat = r["category"]
            category_totals[cat]["total"] += 1
            if r["correct_answer"] or r["correct_redirect"] or r["correct_refuse"]:
                category_totals[cat]["correct"] += 1
        
        f.write("| Category | Tests | Correct | Accuracy |\n")
        f.write("|----------|-------|---------|----------|\n")
        for cat in sorted(category_totals.keys()):
            total = category_totals[cat]["total"]
            correct = category_totals[cat]["correct"]
            accuracy = correct / total * 100 if total > 0 else 0
            f.write(f"| {cat} | {total} | {correct} | {accuracy:.1f}% |\n")
        
        f.write("\n")
        
        # Problem patterns
        f.write("## Common Problem Patterns\n\n")
        
        repetition_results = [r for r in results if r["has_repetition"]]
        artifact_results = [r for r in results if r["has_artifact"]]
        error_results = [r for r in results if r["had_error"]]
        
        f.write(f"### Repetition Issues\n")
        f.write(f"- **Total occurrences:** {len(repetition_results)} / {len(results)} ({len(repetition_results)/len(results)*100:.1f}%)\n")
        if repetition_results:
            rep_by_format = defaultdict(int)
            for r in repetition_results:
                rep_by_format[r["format"]] += 1
            f.write(f"- **By format:** ")
            f.write(", ".join(f"{k}: {v}" for k, v in rep_by_format.items()))
            f.write("\n")
        f.write("\n")
        
        f.write(f"### Tokenization Artifacts\n")
        f.write(f"- **Total occurrences:** {len(artifact_results)} / {len(results)} ({len(artifact_results)/len(results)*100:.1f}%)\n\n")
        
        f.write(f"### Errors/Timeouts\n")
        f.write(f"- **Total occurrences:** {len(error_results)} / {len(results)} ({len(error_results)/len(results)*100:.1f}%)\n\n")
        
        # Recommendations
        f.write("## Recommendations\n\n")
        
        best_config_name = best_overall[0]
        best_config_metrics = best_overall[1]
        
        f.write(f"### Recommended Configuration\n\n")
        f.write(f"**{best_config_name}**\n\n")
        f.write(f"- Overall Accuracy: {best_config_metrics['overall_accuracy']:.1f}%\n")
        f.write(f"- Python Accuracy: {best_config_metrics['python_accuracy']:.1f}%\n")
        f.write(f"- Redirect Accuracy: {best_config_metrics['redirect_accuracy']:.1f}%\n")
        f.write(f"- Refuse Accuracy: {best_config_metrics['refuse_accuracy']:.1f}%\n")
        f.write(f"- Repetition Rate: {best_config_metrics['repetition_rate']:.1f}%\n\n")
        
        # Decision on retraining
        f.write("### Retraining Decision\n\n")
        
        # Thresholds
        PYTHON_THRESHOLD = 80.0
        REDIRECT_THRESHOLD = 50.0
        REFUSE_THRESHOLD = 60.0
        REPETITION_THRESHOLD = 20.0
        
        needs_retrain = []
        if best_config_metrics["python_accuracy"] < PYTHON_THRESHOLD:
            needs_retrain.append(f"Python accuracy ({best_config_metrics['python_accuracy']:.1f}%) below threshold ({PYTHON_THRESHOLD}%)")
        
        if best_config_metrics["redirect_accuracy"] < REDIRECT_THRESHOLD:
            needs_retrain.append(f"Redirect accuracy ({best_config_metrics['redirect_accuracy']:.1f}%) below threshold ({REDIRECT_THRESHOLD}%)")
        
        if best_config_metrics["refuse_accuracy"] < REFUSE_THRESHOLD:
            needs_retrain.append(f"Refuse accuracy ({best_config_metrics['refuse_accuracy']:.1f}%) below threshold ({REFUSE_THRESHOLD}%)")
        
        if best_config_metrics["repetition_rate"] > REPETITION_THRESHOLD:
            needs_retrain.append(f"Repetition rate ({best_config_metrics['repetition_rate']:.1f}%) above threshold ({REPETITION_THRESHOLD}%)")
        
        if needs_retrain:
            f.write("**RECOMMENDATION: PROCEED WITH RETRAINING (Phase 6I)**\n\n")
            f.write("Inference-level fixes are insufficient. Issues requiring retraining:\n\n")
            for issue in needs_retrain:
                f.write(f"- {issue}\n")
            f.write("\n")
            f.write("The Phase 6F high-quality dataset (1,082 examples) should resolve these issues through fine-tuning.\n")
        else:
            f.write("**RECOMMENDATION: INFERENCE FIXES SUFFICIENT**\n\n")
            f.write("The recommended configuration meets all accuracy thresholds. ")
            f.write("Retraining may not be necessary if this performance is acceptable.\n")
        
        f.write("\n")
        
        # Appendix
        f.write("## Appendix: Configuration Details\n\n")
        f.write("### Prompt Formats\n\n")
        f.write("1. **format_a_alpaca:** Training format with `### Instruction:` and `### Response:` delimiters\n")
        f.write("2. **format_b_system:** Explicit system prompt defining Vasuki's capabilities and limitations\n")
        f.write("3. **format_c_minimal:** Direct prompt without formatting\n\n")
        
        f.write("### Parameter Configurations\n\n")
        f.write("1. **config_1_conservative:** temp=0.2, repeat_penalty=1.2 (minimize creativity, maximize consistency)\n")
        f.write("2. **config_2_moderate:** temp=0.5, repeat_penalty=1.1 (balanced approach)\n")
        f.write("3. **config_3_creative:** temp=0.7, repeat_penalty=1.05 (higher variation)\n\n")
        
        f.write("---\n\n")
        f.write("**End of Phase 6H Report**\n")
    
    print(f"✓ Report saved to: {OUTPUT_FILE}")
    print(f"✓ Total configurations analyzed: {len(all_metrics)}")
    print(f"\nBest overall configuration: {best_overall[0]} ({best_overall[1]['overall_accuracy']:.1f}% accuracy)")

if __name__ == "__main__":
    results = load_all_results()
    generate_report(results)
