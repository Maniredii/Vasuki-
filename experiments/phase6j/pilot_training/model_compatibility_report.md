# VASUKI Phase 6J — Model Compatibility & Verification Report

**Model Identified:** `unsloth/Qwen2.5-Coder-0.5B`  
*(Upstream Hugging Face Equivalent: `Qwen/Qwen2.5-Coder-0.5B`)*  
**Verification Status:** `VERIFIED_COMPATIBLE`  

---

## 1. Architectural & Configuration Specifications

| Parameter | Specification | Architectural Detail |
|:---|:---|:---|
| **Exact Identifier** | `unsloth/Qwen2.5-Coder-0.5B` | Base coder model packaged for fast QLoRA training |
| **Checkpoint Type** | **Base Coder Foundation** | Pre-trained code model; not aligned with generic chat RLHF |
| **Model Architecture** | `Qwen2ForCausalLM` | Auto-regressive Transformer decoder with RoPE embeddings |
| **Parameter Count** | **494,032,896 (~490M)** | 24 decoder layers, hidden dimension 896 |
| **Attention Mechanism** | Grouped-Query Attention (GQA) | 14 Query heads, 2 Key-Value heads |
| **Intermediate Size** | 4,864 | SwiGLU non-linear feed-forward activation |
| **Native Context Length**| 32,768 tokens | Configured to **2,048 tokens** for training and pilot eval |
| **Vocabulary Size** | 151,665 tokens | BPE tokenizer (`Qwen2TokenizerFast`) |
| **Special Tokens** | `<|endoftext|>` (151643), `<|im_start|>` (151644), `<|im_end|>` (151645) | Standard Qwen special token map |
| **Padding Side** | Right (`padding_side='right'`) | Proper causal masking for prompt completion |
| **Chat / Prompt Format** | **Alpaca Format** | `### Instruction:
...

### Response:
...` |

---

## 2. LoRA / QLoRA Module Compatibility

The model's linear projections match the configured QLoRA target modules:
- Attention Projections: `q_proj`, `k_proj`, `v_proj`, `o_proj` (All 4 modules verified)
- MLP Feed-Forward: `gate_proj`, `up_proj`, `down_proj` (All 3 modules verified)
- Target Coverage: 100% of linear layers adapted with rank r=16, alpha=16, dropout 0.05.

---

## 3. GGUF Artifact Preservation & Distinction

- The file `vasuki_phase6i.Q4_K_M.gguf` in the repository root is an **inference export artifact** compiled for runtime execution in `llama.cpp`.
- It **cannot** be used as a LoRA training base.
- Fine-tuning must initialize from standard 4-bit / 16-bit base weights (`unsloth/Qwen2.5-Coder-0.5B`).
- `vasuki_phase6i.Q4_K_M.gguf` remains preserved and untouched.
