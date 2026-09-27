"""
VASUKI Phase 6J: Controlled Pilot QLoRA Training Experiment
Base Model: unsloth/Qwen2.5-Coder-0.5B (~490M parameters)
Training Dataset: phase6j_training_candidate_diversified.jsonl (593 records)
Validation Dataset: phase6j_validation.jsonl (75 records)

Execution Instructions (Google Colab / Cloud GPU):
1. Create a fresh Google Colab notebook (Runtime -> Change runtime type -> T4 GPU).
2. Upload this script along with:
   - phase6j_training_candidate_diversified.jsonl
   - phase6j_validation.jsonl
3. Execute: python phase6j_training.py
4. Download the resulting ./phase6j_output/ back to your local repository.
"""

import os
import sys
import time
import json
import hashlib
import glob
import shutil
from datetime import datetime
from collections import Counter
from pathlib import Path

# ============================================================================
# CONFIGURATION & HYPERPARAMETERS
# ============================================================================

EXPERIMENT_ID = "vasuki_phase6j_pilot"
BASE_MODEL = "unsloth/Qwen2.5-Coder-0.5B"
# Dataset Selection: Priority to Calibrated V3 (2,651 records: 94.8% Python + 5.0% boundary redirects)
CALIBRATED_FILE = "phase6j_training_candidate_calibrated.jsonl"
MULTI_SOURCE_FILE = "phase6j_training_candidate_multi_source.jsonl"
AUGMENTED_FILE = "phase6j_training_candidate_augmented.jsonl"
BALANCED_FILE = "phase6j_training_candidate_balanced.jsonl"

if os.path.exists(CALIBRATED_FILE):
    TRAINING_DATA_FILE = CALIBRATED_FILE
elif os.path.exists(MULTI_SOURCE_FILE):
    TRAINING_DATA_FILE = MULTI_SOURCE_FILE
elif os.path.exists(AUGMENTED_FILE):
    TRAINING_DATA_FILE = AUGMENTED_FILE
else:
    TRAINING_DATA_FILE = BALANCED_FILE

VALIDATION_DATA_FILE = "phase6j_validation.jsonl"
OUTPUT_DIR = "./phase6j_output"
MAX_SEQ_LENGTH = 2048
RANDOM_SEED = 42

# Cryptographic signatures for dataset integrity validation (Linux LF and Windows CRLF)
EXPECTED_TRAIN_HASHES = {
    # Calibrated V3 dataset (2,651 records: 94.8% Python + 5.0% redirects)
    "ed0f00346888db609b85d09b408174c3688e37982d66d8a6bf3cabd97ca7bd0a",  # Linux / Git LF (Colab default)
    "da06de85e2f081ec9d4b7ea59e9298424dffec03c769f5e9574c0701bd632a34",  # Windows CRLF
    # Multi-source dataset (2,470 records: iamtarun + flytech + CodeAlpaca + Phase 6J)
    "2a72e9b9bba07867df68f315440c7b875a49f5ac1f50be0c701d19130a132df9",  # Linux / Git LF
    "7a46f0ddb03f75733653f52e2f6a00f408adcee9c121bbd9e1fbd4c261495f22",  # Windows CRLF
    # Augmented dataset (1,470 records: iamtarun + Phase 6J)
    "26b0a367f6f2d200a374067384ec90fc0989702ba80b5b59a74d1ec93c528605",  # Linux / Git LF
    "5422261c935340feaeb1b3a097f2482bb0f0dc2335db552bd4b8af5b62e15b00",  # Windows CRLF
    # Balanced dataset (470 records: Phase 6J)
    "9cf5e54dce6c6f75930c0297d273c92655ab2222f51635842f8f0fdf436acd3c",  # Linux / Git LF
    "27575b2003819d501f9c5840f80a7dc9cf61c78f53f062b9d0cb8f02f509d47a",  # Windows CRLF
}
EXPECTED_VAL_HASHES = {
    "6e6ad7626955211ed9ec8f4084e668bf9bf240cc2704430642c351e2ba1e48cb",  # Linux / Git LF (Colab default)
    "db816d9bac321deda2aa80dce5552ff994006c42054bac638baf4a5647a4172d",  # Windows CRLF
}
EXPECTED_TRAIN_COUNTS = {2651, 2470, 1470, 470}
EXPECTED_VAL_COUNT = 75

# QLoRA Configuration (Conservative & Parameter-Efficient)
LORA_CONFIG = {
    "r": 16,
    "lora_alpha": 16,
    "lora_dropout": 0.05,
    "target_modules": [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    "bias": "none",
    "use_rslora": False,
}

# Training Hyperparameters (Tesla T4 / A10G / L4 Optimized)
if TRAINING_DATA_FILE == CALIBRATED_FILE:
    MAX_STEPS = 660      # 2 epochs over 2,651 records (effective batch size 8)
    EVAL_STEPS = 75
    WARMUP_STEPS = 30
elif TRAINING_DATA_FILE == MULTI_SOURCE_FILE:
    MAX_STEPS = 616      # 2 epochs over 2,470 records
    EVAL_STEPS = 75
    WARMUP_STEPS = 30
elif TRAINING_DATA_FILE == AUGMENTED_FILE:
    MAX_STEPS = 368      # 2 epochs over 1,470 records
    EVAL_STEPS = 60
    WARMUP_STEPS = 20
else:
    MAX_STEPS = 180      # 3 epochs over 470 records
    EVAL_STEPS = 45
    WARMUP_STEPS = 10

TRAINING_CONFIG = {
    "per_device_train_batch_size": 2,
    "per_device_eval_batch_size": 2,
    "gradient_accumulation_steps": 4,
    "warmup_steps": WARMUP_STEPS,
    "max_steps": MAX_STEPS,
    "learning_rate": 2e-4,        # 0.0002
    "fp16": True,                 # Optimized for T4 (use bf16 for A100/L4 if available)
    "bf16": False,
    "logging_steps": 10,
    "eval_steps": EVAL_STEPS,
    "save_steps": EVAL_STEPS,
    "save_total_limit": 1,        # Retain only the single best checkpoint to save disk space
    "optim": "adamw_8bit",
    "weight_decay": 0.01,
    "lr_scheduler_type": "cosine",
    "seed": RANDOM_SEED,
    "output_dir": OUTPUT_DIR,
    "eval_strategy": "steps",
    "load_best_model_at_end": True,
    "metric_for_best_model": "eval_loss",
    "report_to": "none"
}

# Prompt formatting constants
RESPONSE_DELIMITER = "### Response:\n"
EOS_TOKEN = "<|im_end|>"


# Prompt formatting constants
RESPONSE_DELIMITER = "### Response:\n"


def sha256_of_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


# ============================================================================
# 1. ENVIRONMENT VERIFICATION
# ============================================================================

def verify_environment():
    print("=" * 80)
    print("VASUKI Phase 6J: Environment Verification")
    print("=" * 80)
    
    import torch
    print(f"Python Version:   {sys.version.split()[0]}")
    print(f"PyTorch Version:  {torch.__version__}")
    
    if not torch.cuda.is_available():
        print("\n[!] FATAL: No CUDA GPU detected!")
        print("    QLoRA 4-bit fine-tuning requires an NVIDIA GPU (e.g. Google Colab T4).")
        print("    Please ensure a GPU runtime is enabled before continuing.")
        return False
        
    gpu_name = torch.cuda.get_device_name(0)
    vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
    cuda_ver = torch.version.cuda
    print(f"GPU Detected:     {gpu_name}")
    print(f"Total VRAM:       {vram_gb:.2f} GB")
    print(f"CUDA Version:     {cuda_ver}")
    
    if vram_gb < 7.0:
        print(f"\n[!] WARNING: Low VRAM ({vram_gb:.2f} GB). Minimum recommended is 8 GB.")
    else:
        print(f"VRAM Capacity:    Sufficient for QLoRA 4-bit (Peak expected: ~5.5 GB).")
        
    return True


# ============================================================================
# 2. DATASET VERIFICATION & FORMATTING
# ============================================================================

def verify_and_load_datasets():
    print("\n" + "=" * 80)
    print("Dataset Verification & Integrity Audit")
    print("=" * 80)
    
    for path, expected_hashes, allowed_counts in [
        (TRAINING_DATA_FILE, EXPECTED_TRAIN_HASHES, EXPECTED_TRAIN_COUNTS),
        (VALIDATION_DATA_FILE, EXPECTED_VAL_HASHES, {EXPECTED_VAL_COUNT})
    ]:
        if not os.path.exists(path):
            print(f"[!] FATAL: Dataset file '{path}' not found!")
            print(f"    Please place '{path}' in the current working directory.")
            return None, None
            
        actual_hash = sha256_of_file(path)
        if actual_hash not in expected_hashes:
            print(f"[!] FATAL: Hash mismatch on {path}!")
            print(f"    Expected one of: {expected_hashes}")
            print(f"    Actual:          {actual_hash}")
            return None, None
            
        with open(path, "r", encoding="utf-8") as f:
            records = [json.loads(line) for line in f if line.strip()]
            
        if len(records) not in allowed_counts:
            print(f"[!] FATAL: Record count mismatch on {path}!")
            print(f"    Expected one of {allowed_counts}, got {len(records)}.")
            return None, None
            
        print(f"[*] Verified '{path}': {len(records)} records | SHA-256: {actual_hash[:16]}... (MATCH)")

    # Load records
    with open(TRAINING_DATA_FILE, "r", encoding="utf-8") as f:
        train_records = [json.loads(line) for line in f if line.strip()]
    with open(VALIDATION_DATA_FILE, "r", encoding="utf-8") as f:
        val_records = [json.loads(line) for line in f if line.strip()]

    # Format into Alpaca structure
    def format_records(raw_records):
        formatted = []
        for r in raw_records:
            prompt = f"### Instruction:\n{r['instruction']}\n\n"
            if r.get('input'):
                prompt += f"### Input:\n{r['input']}\n\n"
            prompt += RESPONSE_DELIMITER
            clean_resp = r['response'].strip()
            full_text = prompt + clean_resp + "\n<|im_end|>\n"
            formatted.append({
                "prompt": prompt,
                "response": clean_resp + "\n<|im_end|>\n",
                "text": full_text
            })
        return formatted

    train_data = format_records(train_records)
    val_data = format_records(val_records)
    
    print(f"\nFormulation summary:")
    print(f"  Training set:   {len(train_data)} examples formatted")
    print(f"  Validation set: {len(val_data)} examples formatted")
    print(f"  Prompt structure: Alpaca format with completion delimiter '{RESPONSE_DELIMITER.strip()}'")
    
    return train_data, val_data


# ============================================================================
# 3. MODEL & TOKENIZER INITIALIZATION
# ============================================================================

def initialize_model_and_tokenizer():
    print("\n" + "=" * 80)
    print("Model Loading & QLoRA Configuration")
    print("=" * 80)
    
    try:
        # Preferred: Fast path via Unsloth
        from unsloth import FastLanguageModel
        print(f"[1/2] Loading {BASE_MODEL} via Unsloth (4-bit NF4)...")
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=BASE_MODEL,
            max_seq_length=MAX_SEQ_LENGTH,
            dtype=None,
            load_in_4bit=True,
        )
        print("  Base model loaded successfully.")
        
        print(f"[2/2] Injecting LoRA adapters (r={LORA_CONFIG['r']}, alpha={LORA_CONFIG['lora_alpha']})...")
        model = FastLanguageModel.get_peft_model(
            model,
            r=LORA_CONFIG["r"],
            target_modules=LORA_CONFIG["target_modules"],
            lora_alpha=LORA_CONFIG["lora_alpha"],
            lora_dropout=LORA_CONFIG["lora_dropout"],
            bias="none",
            use_gradient_checkpointing="unsloth",
            random_state=RANDOM_SEED,
        )
        print("  LoRA adapters initialized successfully.")
        return model, tokenizer, True
        
    except ImportError:
        # Fallback path: Standard Hugging Face PEFT & BitsAndBytes
        print("[!] Unsloth not detected. Initializing via HuggingFace PEFT / BitsAndBytes...")
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
        
        model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
        )
        model = prepare_model_for_kbit_training(model)
        
        peft_config = LoraConfig(
            r=LORA_CONFIG["r"],
            lora_alpha=LORA_CONFIG["lora_alpha"],
            lora_dropout=LORA_CONFIG["lora_dropout"],
            target_modules=LORA_CONFIG["target_modules"],
            bias="none",
            task_type="CAUSAL_LM"
        )
        model = get_peft_model(model, peft_config)
        print("  Standard PEFT model initialized successfully.")
        return model, tokenizer, False


# ============================================================================
# 4. TRAINING WITH RESPONSE-ONLY LOSS MASKING
# ============================================================================

def execute_training(model, tokenizer, train_data, val_data, is_unsloth):
    print("\n" + "=" * 80)
    print("Pilot QLoRA Training Execution")
    print("=" * 80)
    
    from datasets import Dataset
    from transformers import TrainingArguments
    from trl import SFTTrainer
    
    try:
        from trl import DataCollatorForCompletionOnlyLM
    except ImportError:
        try:
            from trl.trainer import DataCollatorForCompletionOnlyLM
        except ImportError:
            from transformers import DataCollatorForLanguageModeling

            class DataCollatorForCompletionOnlyLM(DataCollatorForLanguageModeling):
                """Self-contained completion loss collator that masks prompt tokens with -100."""
                def __init__(self, response_template, tokenizer, mlm=False, **kwargs):
                    super().__init__(tokenizer=tokenizer, mlm=mlm, **kwargs)
                    self.response_template = response_template
                    if isinstance(response_template, str):
                        self.response_token_ids = tokenizer.encode(response_template, add_special_tokens=False)
                    else:
                        self.response_token_ids = response_template

                def torch_call(self, examples):
                    batch = super().torch_call(examples)
                    labels = batch["labels"].clone()
                    rlen = len(self.response_token_ids)
                    for i in range(len(examples)):
                        input_ids = batch["input_ids"][i].tolist()
                        response_start = None
                        for j in range(len(input_ids) - rlen + 1):
                            if input_ids[j:j+rlen] == self.response_token_ids:
                                response_start = j + rlen
                                break
                        if response_start is not None:
                            labels[i, :response_start] = -100
                        else:
                            labels[i, :] = -100
                    batch["labels"] = labels
                    return batch
    
    train_dataset = Dataset.from_list(train_data)
    val_dataset = Dataset.from_list(val_data)
    
    # Setup completion-only response collator
    # Masks instruction tokens so loss is computed solely on model responses
    collator = DataCollatorForCompletionOnlyLM(
        response_template=RESPONSE_DELIMITER,
        tokenizer=tokenizer
    )
    
    training_args = TrainingArguments(**TRAINING_CONFIG)
    
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        dataset_text_field="text",
        max_seq_length=MAX_SEQ_LENGTH,
        data_collator=collator,
        args=training_args,
    )
    
    print("\n[*] Starting 220-step QLoRA pilot training run...")
    print(f"    Per-device batch size:  {TRAINING_CONFIG['per_device_train_batch_size']}")
    print(f"    Gradient accumulation:  {TRAINING_CONFIG['gradient_accumulation_steps']}")
    print(f"    Effective batch size:   {TRAINING_CONFIG['per_device_train_batch_size'] * TRAINING_CONFIG['gradient_accumulation_steps']}")
    print(f"    Learning rate:          {TRAINING_CONFIG['learning_rate']} (cosine)")
    print(f"    Validation frequency:   Every {TRAINING_CONFIG['eval_steps']} steps")
    print("-" * 80)
    
    start_time = time.time()
    train_stats = trainer.train()
    duration_secs = time.time() - start_time
    
    print("-" * 80)
    print("Training Completed Successfully!")
    print(f"  Duration:         {duration_secs / 60:.2f} minutes")
    print(f"  Final Train Loss: {train_stats.training_loss:.4f}")
    
    # Final evaluation on held-out 75 validation examples
    print("\n[*] Running final evaluation against held-out validation set...")
    try:
        eval_results = trainer.evaluate()
    except Exception:
        val_losses = [entry['eval_loss'] for entry in trainer.state.log_history if 'eval_loss' in entry]
        eval_results = {'eval_loss': val_losses[-1] if val_losses else None}
    
    val_loss_val = eval_results.get('eval_loss')
    if val_loss_val is not None:
        print(f"  Validation Loss:  {val_loss_val:.4f}")
    else:
        print(f"  Validation Loss:  N/A")
    
    return trainer, train_stats, eval_results


# ============================================================================
# 5. ARTIFACT EXPORT & EVALUATION BENCHMARK
# ============================================================================

def export_artifacts(model, tokenizer, is_unsloth, eval_results):
    print("\n" + "=" * 80)
    print("Exporting Model Artifacts")
    print("=" * 80)
    
    adapter_dir = os.path.join(OUTPUT_DIR, "adapter")
    os.makedirs(adapter_dir, exist_ok=True)
    
    print(f"[*] Saving LoRA adapter weights to '{adapter_dir}'...")
    model.save_pretrained(adapter_dir)
    tokenizer.save_pretrained(adapter_dir)
    
    # Save training summary JSON
    summary_path = os.path.join(OUTPUT_DIR, "training_summary.json")
    summary = {
        "experiment_id": EXPERIMENT_ID,
        "base_model": BASE_MODEL,
        "completed_at": datetime.now().isoformat(),
        "train_records": EXPECTED_TRAIN_COUNT,
        "val_records": EXPECTED_VAL_COUNT,
        "training_steps": TRAINING_CONFIG["max_steps"],
        "eval_loss": eval_results.get("eval_loss"),
        "lora_rank": LORA_CONFIG["r"],
        "lora_alpha": LORA_CONFIG["lora_alpha"],
        "lora_dropout": LORA_CONFIG["lora_dropout"]
    }
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"[*] Summary saved to '{summary_path}'")
    
    # If using Unsloth on Google Colab, also export merged 16-bit and GGUF
    if is_unsloth:
        try:
            from unsloth import FastLanguageModel
            merged_dir = os.path.join(OUTPUT_DIR, "merged_16bit")
            print(f"\n[*] Exporting merged 16-bit weights to '{merged_dir}'...")
            model = FastLanguageModel.for_inference(model)
            model.save_pretrained_merged(merged_dir, tokenizer, save_method="merged_16bit")
            print("  Merged weights saved.")
            
            print(f"[*] Exporting GGUF (Q4_K_M)...")
            model.save_pretrained_gguf(merged_dir, tokenizer, quantization_method="q4_k_m")
            print("  GGUF export completed.")
        except Exception as e:
            print(f"[!] Optional GGUF export note: {e}")

    # Zip output directory for easy download back to workstation
    archive_name = "vasuki_phase6j_output"
    print(f"\n[*] Packaging output directory into '{archive_name}.zip' for easy download...")
    shutil.make_archive(archive_name, "zip", OUTPUT_DIR)
    print(f"[OK] Package ready: {archive_name}.zip ({os.path.getsize(archive_name + '.zip') / (1024**2):.1f} MB)")


def run_spot_check_inference(model, tokenizer):
    print("\n" + "=" * 80)
    print("Post-Training Spot-Check Verification (3 Diverse Test Prompts)")
    print("=" * 80)
    
    test_prompts = [
        "Explain list comprehensions in Python with a clear code example.",
        "How do I call a Java REST API from Python using requests?",
        "Write a complete C++ 3D game engine."
    ]
    
    import torch
    model.eval()
    
    for idx, prompt_text in enumerate(test_prompts, 1):
        formatted_prompt = f"### Instruction:\n{prompt_text}\n\n### Response:\n"
        inputs = tokenizer(formatted_prompt, return_tensors="pt").to("cuda")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.2,
                top_p=0.9,
                repetition_penalty=1.1,
                eos_token_id=tokenizer.eos_token_id
            )
            
        generated_text = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        print(f"\n[Test Prompt {idx}]: {prompt_text}")
        print("-" * 50)
        print(generated_text.strip())
        print("-" * 50)


# ============================================================================
# MAIN ENTRYPOINT
# ============================================================================

def main():
    print("Starting VASUKI Phase 6J QLoRA Training Pipeline...")
    if not verify_environment():
        sys.exit(1)
        
    train_data, val_data = verify_and_load_datasets()
    if train_data is None:
        sys.exit(1)
        
    model, tokenizer, is_unsloth = initialize_model_and_tokenizer()
    trainer, train_stats, eval_results = execute_training(model, tokenizer, train_data, val_data, is_unsloth)
    
    run_spot_check_inference(model, tokenizer)
    export_artifacts(model, tokenizer, is_unsloth, eval_results)
    
    print("\n" + "=" * 80)
    print("[OK] ALL PHASE 6J PILOT TRAINING TASKS COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    main()
