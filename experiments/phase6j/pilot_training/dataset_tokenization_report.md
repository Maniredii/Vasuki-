# VASUKI Phase 6J — Dataset Tokenization & Length Report

**Tokenizer Used:** `Qwen2TokenizerFast` (Vocabulary: 151,665 tokens)  
**Prompt Template:** Alpaca Instruction Format  
**Configured Sequence Length:** 2,048 tokens  
**Audit Verification:** 100% of records tokenized individually  

---

## 1. Exact Token-Length Distribution

| Metric | Candidate Dataset (593 Records) | Held-Out Validation (75 Records) | Configured Limit | Truncation Status |
|:---|:---:|:---:|:---:|:---:|
| **Minimum Tokens** | 30 tokens | 46 tokens | 2,048 tokens | Safe |
| **Mean Tokens** | **136.1 tokens** | **110.4 tokens** | 2,048 tokens | Safe |
| **Median Tokens** | 118 tokens | 105 tokens | 2,048 tokens | Safe |
| **90th Percentile** | 261 tokens | 190 tokens | 2,048 tokens | Safe |
| **95th Percentile** | 286 tokens | 214 tokens | 2,048 tokens | Safe |
| **99th Percentile** | 329 tokens | 254 tokens | 2,048 tokens | Safe |
| **Maximum Tokens** | **381 tokens** | **254 tokens** | 2,048 tokens | **Zero Truncation** |
| **Records > 2048 Tokens** | **0 (0.00%)** | **0 (0.00%)** | — | **100% Contained** |

---

## 2. Largest Records Analysis

- **Largest Candidate Record:**
  - ID: `phase6j_000005` (`python_programming`)
  - Prompt Tokens: 33
  - Response Tokens: 348
  - **Total Tokens:** **381 tokens**
  - Headroom remaining: **1667 tokens** (81.4% unused buffer)
- **Largest Validation Record:**
  - ID: `val_phase6j_0013` (`python_code_generation`)
  - **Total Tokens:** **254 tokens**
  - Headroom remaining: **1794 tokens** (87.6% unused buffer)

---

## 3. Delimiter & Prompt Verification

- Delimiter `### Response:\n` is present in **593 / 593 candidate records** and **75 / 75 validation records**.
- Every record cleanly separates the user prompt context from the assistant's target code/explanation.
- **Empirical Truncation Conclusion:** Truncation risk is **0.0%**. Every single training and validation record fits inside 2,048 tokens with at least 1,667 tokens of headroom.
