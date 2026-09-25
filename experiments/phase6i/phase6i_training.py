"""
Phase 6I: Controlled Vasuki QLoRA Training Experiment
Train with Phase 6F clean dataset (1,073 examples)

INSTRUCTIONS:
1. Upload this script to Google Colab
2. Upload training_clean.jsonl to Colab
3. Set Runtime -> Change runtime type -> GPU (T4)
4. Run all cells
5. Download outputs back to D:\VASUKI\experiments\phase6i\
"""

import json
import os
import time
from datetime import datetime
import torch
from pathlib import Path

# ============================================================================
# EXPERIMENT CONFIGURATION
# ============================================================================

EXPERIMENT_ID = "phase6i_20260923"
BASE_MODEL = "unsloth/Qwen2.5-Coder-0.5B"
TRAINING_DATA = "training_clean.jsonl"  # Upload to Colab
OUTPUT_DIR = "./phase6i_output"
MAX_SEQ_LENGTH = 2048
RANDOM_SEED = 42

# QLoRA Configuration (Conservative)
LORA_CONFIG = {
    "r": 16,
    "lora_alpha": 16,
    "lora_dropout": 0.0,
    "target_modules": [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    "use_rslora": False
}

# Training Configuration (Tesla T4 optimized)
TRAINING_CONFIG = {
    "per_device_train_batch_size": 2,
    "gradient_accumulation_steps": 4,
    "warmup_steps": 10,
    "max_steps": 200,  # Conservative for 1,073 examples
    "learning_rate": 2e-4,
    "fp16": True,  # Tesla T4 doesn't support BF16
    "bf16": False,
    "tf32": False,
    "logging_steps": 10,
    "optim": "adamw_8bit",
    "weight_decay": 0.01,
    "lr_scheduler_type": "linear",
    "seed": RANDOM_SEED,
    "output_dir": OUTPUT_DIR,
}

# ============================================================================
# SETUP AND INSTALLATION
# ============================================================================

def setup_environment():
    """Install dependencies"""
    print("="*80)
    print("Phase 6I: Environment Setup")
    print("="*80)
    
    # Install Unsloth and dependencies
    print("\n[1/3] Installing Unsloth...")
    os.system("pip install -q unsloth")
    os.system("pip install -q --no-deps trl peft accelerate bitsandbytes")
    
    print("\n[2/3] Checking GPU...")
    if torch.cuda.is_available():
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
        print(f"  CUDA: {torch.version.cuda}")
        print(f"  Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        print("  ERROR: No GPU available!")
        return False
    
    print("\n[3/3] Recording versions...")
    import unsloth
    import transformers
    print(f"  Unsloth: {unsloth.__version__}")
    print(f"  Transformers: {transformers.__version__}")
    print(f"  PyTorch: {torch.__version__}")
    
    return True

# ============================================================================
# DATASET LOADING AND FORMATTING
# ============================================================================

def load_and_format_dataset(filepath):
    """Load JSONL and format for training"""
    print("\n"+"="*80)
    print("Dataset Loading and Formatting")
    print("="*80)
    
    # Load JSONL
    print(f"\n[1/4] Loading {filepath}...")
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            records.append(json.loads(line.strip()))
    print(f"  Loaded: {len(records)} records")
    
    # Analyze
    from collections import Counter
    behavior_counts = Counter(r['expected_behavior'] for r in records)
    print(f"\n[2/4] Distribution:")
    for behavior, count in behavior_counts.items():
        pct = count / len(records) * 100
        print(f"  {behavior}: {count} ({pct:.1f}%)")
    
    # Format as Alpaca-style prompts
    print(f"\n[3/4] Formatting prompts...")
    formatted_data = []
    for record in records:
        # Build prompt in training format
        prompt = f"### Instruction:\n{record['instruction']}\n\n"
        if record.get('input'):
            prompt += f"### Input:\n{record['input']}\n\n"
        prompt += "### Response:\n"
        
        formatted_data.append({
            "text": prompt + record['response']
        })
    
    print(f"  Formatted: {len(formatted_data)} examples")
    
    # Show samples
    print(f"\n[4/4] Sample formatted examples:")
    for i in range(min(2, len(formatted_data))):
        print(f"\nExample {i+1}:")
        print("-"*60)
        print(formatted_data[i]["text"][:200] + "...")
        print("-"*60)
    
    return formatted_data

# ============================================================================
# MODEL LOADING
# ============================================================================

def load_model():
    """Load base model with 4-bit quantization"""
    print("\n"+"="*80)
    print("Model Loading")
    print("="*80)
    
    from unsloth import FastLanguageModel
    
    print(f"\n[1/2] Loading {BASE_MODEL}...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=BASE_MODEL,
        max_seq_length=MAX_SEQ_LENGTH,
        dtype=None,  # Auto-detect
        load_in_4bit=True,
    )
    print("  Model loaded successfully")
    
    print(f"\n[2/2] Adding LoRA adapters...")
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
    print("  LoRA adapters added")
    
    return model, tokenizer

# ============================================================================
# TRAINING
# ============================================================================

def train_model(model, tokenizer, formatted_data):
    """Train the model"""
    print("\n"+"="*80)
    print("Training")
    print("="*80)
    
    from transformers import TrainingArguments, DataCollatorForLanguageModeling
    from trl import SFTTrainer
    from datasets import Dataset
    
    # Convert to HF Dataset
    print("\n[1/4] Preparing dataset...")
    dataset = Dataset.from_list(formatted_data)
    print(f"  Dataset size: {len(dataset)}")
    
    # Training arguments
    print("\n[2/4] Configuring trainer...")
    training_args = TrainingArguments(**TRAINING_CONFIG)
    print(f"  Effective batch size: {TRAINING_CONFIG['per_device_train_batch_size'] * TRAINING_CONFIG['gradient_accumulation_steps']}")
    print(f"  Max steps: {TRAINING_CONFIG['max_steps']}")
    print(f"  Learning rate: {TRAINING_CONFIG['learning_rate']}")
    
    # Trainer
    print("\n[3/4] Initializing trainer...")
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=MAX_SEQ_LENGTH,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
        args=training_args,
    )
    
    # Train
    print("\n[4/4] Starting training...")
    print("-"*80)
    start_time = time.time()
    
    trainer_stats = trainer.train()
    
    end_time = time.time()
    duration = end_time - start_time
    print("-"*80)
    print(f"\nTraining complete!")
    print(f"  Duration: {duration/60:.1f} minutes")
    print(f"  Final loss: {trainer_stats.training_loss:.4f}")
    
    return trainer, trainer_stats, duration

# ============================================================================
# MODEL EXPORT
# ============================================================================

def export_model(model, tokenizer):
    """Export trained model"""
    print("\n"+"="*80)
    print("Model Export")
    print("="*80)
    
    from unsloth import FastLanguageModel
    import hashlib
    import shutil
    import glob
    
    # Save LoRA adapter
    print("\n[1/5] Saving LoRA adapter...")
    adapter_dir = f"{OUTPUT_DIR}/adapter"
    model.save_pretrained(adapter_dir)
    tokenizer.save_pretrained(adapter_dir)
    print(f"  Saved to: {adapter_dir}")
    
    # Merge and save
    print("\n[2/5] Merging adapter with base model...")
    model = FastLanguageModel.for_inference(model)  # Prepare for inference
    merged_dir = f"{OUTPUT_DIR}/merged"
    model.save_pretrained_merged(merged_dir, tokenizer, save_method="merged_16bit")
    print(f"  Saved to: {merged_dir}")
    
    # Export to GGUF
    print("\n[3/5] Converting to GGUF Q4_K_M...")
    # Unsloth creates a merged_gguf subdirectory
    model.save_pretrained_gguf(merged_dir, tokenizer, quantization_method="q4_k_m")
    
    # Find the actual GGUF file created by Unsloth
    gguf_search_dir = f"{OUTPUT_DIR}/merged_gguf"
    print(f"  Searching for GGUF in: {gguf_search_dir}")
    
    if not os.path.exists(gguf_search_dir):
        print(f"  ERROR: {gguf_search_dir} not found!")
        print(f"  Looking in merged directory instead...")
        gguf_search_dir = merged_dir
    
    # Find Q4_K_M GGUF file
    gguf_files = glob.glob(f"{gguf_search_dir}/*.Q4_K_M.gguf")
    
    if not gguf_files:
        # Try without Q4_K_M in filename
        gguf_files = glob.glob(f"{gguf_search_dir}/*.gguf")
    
    if not gguf_files:
        print(f"  ERROR: No GGUF files found in {gguf_search_dir}")
        return adapter_dir, merged_dir, None, None
    
    source_gguf = gguf_files[0]
    print(f"  Found GGUF: {source_gguf}")
    
    # Copy to final destination with desired name
    print("\n[4/5] Copying to final location...")
    final_gguf_path = f"{OUTPUT_DIR}/vasuki_phase6i.Q4_K_M.gguf"
    shutil.copy2(source_gguf, final_gguf_path)
    print(f"  Copied to: {final_gguf_path}")
    
    # Verify file exists and get size
    if not os.path.exists(final_gguf_path):
        print(f"  ERROR: Final GGUF file not found at {final_gguf_path}")
        return adapter_dir, merged_dir, None, None
    
    file_size = os.path.getsize(final_gguf_path)
    print(f"  File size: {file_size / (1024**2):.2f} MB")
    
    # Calculate hash
    print("\n[5/5] Calculating SHA256 hash...")
    hasher = hashlib.sha256()
    with open(final_gguf_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hasher.update(chunk)
    sha256 = hasher.hexdigest()
    print(f"  SHA256: {sha256}")
    
    print(f"\n  Final GGUF: {final_gguf_path}")
    print(f"  Size: {file_size / (1024**2):.2f} MB ({file_size:,} bytes)")
    print(f"  Hash: {sha256}")
    
    return adapter_dir, merged_dir, final_gguf_path, sha256

# ============================================================================
# LOGGING AND REPORTING
# ============================================================================

def save_training_log(trainer_stats, duration, sha256):
    """Save comprehensive training log"""
    print("\n"+"="*80)
    print("Saving Training Log")
    print("="*80)
    
    log_data = {
        "experiment_id": EXPERIMENT_ID,
        "timestamp": datetime.now().isoformat(),
        "base_model": BASE_MODEL,
        "training_data": TRAINING_DATA,
        "dataset_size": 1073,
        "random_seed": RANDOM_SEED,
        "max_seq_length": MAX_SEQ_LENGTH,
        "lora_config": LORA_CONFIG,
        "training_config": TRAINING_CONFIG,
        "training_duration_seconds": duration,
        "final_loss": float(trainer_stats.training_loss),
        "total_steps": trainer_stats.global_step,
        "gguf_sha256": sha256 if sha256 else "NOT_AVAILABLE",
        "pytorch_version": torch.__version__,
        "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "peak_memory_gb": torch.cuda.max_memory_allocated() / 1024**3 if torch.cuda.is_available() else None,
    }
    
    log_file = f"{OUTPUT_DIR}/phase6i_training_log.json"
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)
    
    print(f"  Training log saved to: {log_file}")
    
    # Save summary report
    summary_file = f"{OUTPUT_DIR}/phase6i_training_summary.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# Phase 6I: Training Summary\n\n")
        f.write(f"**Experiment ID**: {EXPERIMENT_ID}\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write("## Configuration\n\n")
        f.write(f"- **Base Model**: {BASE_MODEL}\n")
        f.write(f"- **Dataset**: {TRAINING_DATA} ({log_data['dataset_size']} examples)\n")
        f.write(f"- **Random Seed**: {RANDOM_SEED}\n")
        f.write(f"- **Max Seq Length**: {MAX_SEQ_LENGTH}\n\n")
        f.write("## LoRA Configuration\n\n")
        f.write(f"- **r**: {LORA_CONFIG['r']}\n")
        f.write(f"- **alpha**: {LORA_CONFIG['lora_alpha']}\n")
        f.write(f"- **dropout**: {LORA_CONFIG['lora_dropout']}\n")
        f.write(f"- **target_modules**: {', '.join(LORA_CONFIG['target_modules'])}\n\n")
        f.write("## Training Results\n\n")
        f.write(f"- **Duration**: {duration/60:.1f} minutes\n")
        f.write(f"- **Total Steps**: {trainer_stats.global_step}\n")
        f.write(f"- **Final Loss**: {trainer_stats.training_loss:.4f}\n")
        f.write(f"- **Peak VRAM**: {log_data['peak_memory_gb']:.2f} GB\n\n")
        f.write("## Model Export\n\n")
        if sha256:
            f.write(f"- **GGUF SHA256**: `{sha256}`\n")
            f.write(f"- **Format**: Q4_K_M quantization\n\n")
        else:
            f.write(f"- **GGUF SHA256**: NOT AVAILABLE (export may have failed)\n")
            f.write(f"- **Format**: Q4_K_M quantization\n\n")
        f.write("## Environment\n\n")
        f.write(f"- **GPU**: {log_data['gpu_name']}\n")
        f.write(f"- **PyTorch**: {log_data['pytorch_version']}\n")
        f.write(f"- **CUDA**: {log_data['cuda_version']}\n\n")
        f.write("---\n\n")
        f.write("**Next**: Download outputs and run Phase 6I evaluation\n")
    
    print(f"  Summary report saved to: {summary_file}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main training pipeline"""
    print("="*80)
    print("PHASE 6I: CONTROLLED VASUKI QLORATRAINING EXPERIMENT")
    print("="*80)
    print(f"Experiment ID: {EXPERIMENT_ID}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # 1. Setup
    if not setup_environment():
        print("\nERROR: Environment setup failed")
        return
    
    # 2. Load dataset
    try:
        formatted_data = load_and_format_dataset(TRAINING_DATA)
    except FileNotFoundError:
        print(f"\nERROR: {TRAINING_DATA} not found!")
        print("Please upload training_clean.jsonl to Colab")
        return
    
    # 3. Load model
    model, tokenizer = load_model()
    
    # 4. Train
    trainer, trainer_stats, duration = train_model(model, tokenizer, formatted_data)
    
    # 5. Export
    adapter_dir, merged_dir, gguf_path, sha256 = export_model(model, tokenizer)
    
    # 6. Save logs
    save_training_log(trainer_stats, duration, sha256)
    
    # Final message
    print("\n"+"="*80)
    print("TRAINING COMPLETE")
    print("="*80)
    print(f"\nOutputs saved to: {OUTPUT_DIR}/")
    print("\nDownload these files back to D:\\VASUKI\\experiments\\phase6i\\:")
    print(f"  - phase6i_training_log.json")
    print(f"  - phase6i_training_summary.md")
    print(f"  - vasuki_phase6i.Q4_K_M.gguf")
    print(f"  - adapter/ (folder)")
    print(f"  - merged/ (folder)")
    print("\nNext step: Run Phase 6I evaluation script")
    print("="*80)

if __name__ == "__main__":
    main()
