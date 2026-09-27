# VASUKI Phase 6J — Pilot LoRA Training Plan

## 1. Objective
Fine-tune **VASUKI Phase 6J** using Parameter-Efficient Fine-Tuning (QLoRA) on the verified 593-example diversified dataset. The model should specialize in Python programming, provide accurate code and explanations, handle multilingual interoperability, and cleanly redirect non-Python requests while avoiding false equivalence or hallucinations.

---

## 2. Technical Architecture & Parameters

| Parameter | Selected Value | Justification |
|:---|:---|:---|
| **Base Model** | `unsloth/Qwen2.5-Coder-0.5B` | Python-capable lightweight coder backbone |
| **Fine-Tuning Method** | QLoRA (4-bit NF4 Quantization) | Memory-efficient adaptation with minimal VRAM |
| **LoRA Rank ($r$)** | 16 | Sufficient expressiveness for domain adaptation |
| **LoRA Alpha ($lpha$)** | 16 | Balanced scaling factor ($lpha / r = 1.0$) |
| **LoRA Dropout** | 0.05 | Prevents overfitting on 593 records |
| **Target Modules** | `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj` | Full linear attention & MLP layer adaptation |
| **Max Sequence Length**| 2,048 tokens | Captures complete explanations and code samples |
| **Train Record Count** | 593 records | 100% audited and verified |
| **Val Record Count** | 75 records | Strict held-out evaluation set |
| **Batch Size** | 2 per device | Fits within 8GB–16GB VRAM |
| **Gradient Accumulation**| 4 steps | Effective batch size of 8 |
| **Optimizer** | `adamw_8bit` | Reduces optimizer state memory consumption |
| **Learning Rate** | $2 	imes 10^-4$ ($0.0002$) | Standard robust learning rate for QLoRA |
| **LR Scheduler** | Cosine with 5% warmup | Smooth convergence across 220 steps |
| **Epochs / Steps** | ~3 epochs (220 max steps) | Prevents catastrophic forgetting |
| **Random Seed** | 42 | Deterministic reproducibility |
| **Evaluation Strategy**| Every 50 steps | Tracks validation loss and perplexity |
| **Checkpoint Strategy**| Every 50 steps, keep top 2 | Preserves best checkpoint based on val loss |

---

## 3. Hardware Requirements & Deployment Options

- **Target GPU Environment:**
  - Recommended: NVIDIA Tesla T4 (16GB), A10G (24GB), L4 (24GB), or A100.
  - Peak estimated VRAM: ~5.5 GB during 4-bit QLoRA with gradient checkpointing.
  - Training duration: Estimated 8–15 minutes on a Tesla T4 GPU.
- **Local Host Execution:**
  - Local workstation lacks NVIDIA CUDA GPU. Training locally on CPU is computationally inefficient (~12–18 hours on CPU without 4-bit bitsandbytes support).
  - Recommended execution: Google Colab or dedicated cloud GPU instance using the generated `pilot_training_config.yaml`.

---

## 4. Risks & Mitigation Strategies

1. **Risk: Overfitting on 593 examples.**
   - *Mitigation:* LoRA dropout 0.05, early stopping via validation loss evaluation every 50 steps, conservative 3 epochs.
2. **Risk: Regression in General Capabilities.**
   - *Mitigation:* Low rank ($r=16$) ensures foundational reasoning remains anchored in base model weights.
3. **Risk: Repetitive Redirect Canned Responses.**
   - *Mitigation:* Successfully mitigated in Phase 6J by diversifying all 233 redirect examples into unique phrasings and specific domain alternatives.
