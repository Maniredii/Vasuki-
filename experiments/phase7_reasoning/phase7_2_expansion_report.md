# VASUKI Phase 7.2: Large-Scale Corpus Expansion & 1,200-Step Training Report

- **Total Training Records:** 5,486
- **Baseline Records (Phase 7.1):** 3,086
- **Newly Harvested Records:** 2,400
  - iamtarun (Local AST-verified): 1,200
  - CodeAlpaca (Algorithms & Reasoning): 600
  - Flytech (Practical Systems & Automation): 600
- **Zero Contamination vs Val:** PASS (0 overlapping instructions)
- **AST Quality Gate:** 100.0% Pass across all embedded code blocks

---

## 1,200-Step Training Run Results (`checkpoint-1200`)
- **Base Architecture:** Qwen2.5-Coder-0.5B-Instruct
- **Fine-Tuning Method:** QLoRA 4-bit (Unsloth)
- **Total Epochs:** 1.77
- **Total Global Steps:** 1,200
- **Initial Training Loss (Step 10):** 1.1915
- **Final Training Loss (Step 1200):** 0.5938
- **Final Gradient Norm:** 0.60
- **Quantization Export:** GGUF Q4_K_M (379.4 MB)
- **Local Inference Benchmark:** 8/8 Tasks Verified (Binary Search, Primes, Fibonacci, Palindrome, Deduplication, OOP, ctypes, Out-of-Domain redirection)
