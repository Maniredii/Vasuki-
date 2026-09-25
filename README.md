# Vasuki 0.5B - Lightweight Python Programming AI

A specialized 0.5B parameter AI model designed exclusively for Python programming assistance.

## Project Structure

```
vasuki-0.5b-project/
├── data/                    # Training data storage
├── scripts/                 # Data preparation and training scripts
├── models/                  # Trained model checkpoints
├── requirements.txt         # Python dependencies
├── setup.ps1               # Windows setup script
└── README.md               # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Git (optional)
- At least 8GB RAM
- GPU recommended for training (CUDA compatible)

### Installation

1. **Run the setup script (Windows PowerShell):**
   ```powershell
   .\setup.ps1
   ```

   Or manually:
   ```powershell
   # Create virtual environment
   python -m venv venv
   
   # Activate it
   .\venv\Scripts\Activate.ps1
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Prepare the training data:**
   ```powershell
   python scripts\prepare_data.py
   ```

   This will:
   - Download the Python code instructions dataset (18k samples)
   - Generate 5,000 refusal examples for non-programming questions
   - Combine and save as `data/training_data.jsonl`

## Dataset Details

### Python Code Instructions
- Source: `iamtarun/python_code_instructions_18k_alpaca`
- Contains ~18,000 Python programming tasks with solutions
- Format: Instruction-Input-Output triplets

### Refusal Dataset
- Synthetically generated 5,000 examples
- Teaches the model to politely decline non-programming questions
- Standard response: "I am a lightweight AI designed exclusively for Python programming. I cannot answer this."

### Combined Dataset
- Total: ~23,000 training samples
- Format: JSONL (JSON Lines)
- Shuffled for better training

## Next Steps

After preparing the data, you'll need to:

1. Choose a base model (e.g., TinyLlama, Phi-1.5, or similar 0.5B model)
2. Set up training configuration (LoRA/QLoRA for efficiency)
3. Fine-tune the model on the prepared dataset
4. Evaluate and deploy

## Training Configuration (Coming Soon)

The training script will use:
- **Base Model**: TinyLlama-1.1B or similar
- **Training Method**: QLoRA (Quantized Low-Rank Adaptation)
- **Hardware**: Single GPU (minimum 8GB VRAM)
- **Training Time**: ~2-4 hours on modern GPU

## Model Capabilities

Once trained, Vasuki 0.5B will be able to:
- ✅ Explain Python concepts
- ✅ Write Python code snippets
- ✅ Debug Python code
- ✅ Answer Python-specific questions
- ✅ Suggest best practices
- ❌ Answer non-programming questions (by design)

## License

This project is for educational purposes. Please respect the licenses of:
- The base model you choose
- The training datasets used

## Contributing

This is a personal/educational project. Feel free to fork and modify for your own use.
