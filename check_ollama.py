"""
Phase 3: Ollama Compatibility Check and Modelfile Creation
"""

import subprocess
from pathlib import Path

def check_ollama():
    """Check if Ollama is installed and running"""
    print("=" * 70)
    print("PHASE 3: OLLAMA COMPATIBILITY CHECK")
    print("=" * 70)
    
    # Check Ollama version
    print("\n[1] Checking Ollama Installation")
    print("-" * 70)
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=10)
        print(f"✓ Ollama is installed")
        print(f"  Version info: {result.stdout.strip() if result.stdout else result.stderr.strip()}")
    except FileNotFoundError:
        print("✗ Ollama is not installed")
        print("\nInstall Ollama from: https://ollama.com/download/windows")
        return False
    except Exception as e:
        print(f"✗ Error checking Ollama: {e}")
        return False
    
    # Check if Ollama service is running
    print("\n[2] Checking Ollama Service Status")
    print("-" * 70)
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ Ollama service is running")
            print(f"\n  Current models:")
            if result.stdout.strip():
                for line in result.stdout.strip().split('\n'):
                    print(f"    {line}")
            else:
                print("    (No models installed yet)")
        else:
            print("⚠ Ollama service may not be running")
            print(f"  Error: {result.stderr}")
            print("\n  Start Ollama service and try again")
    except Exception as e:
        print(f"⚠ Could not check Ollama status: {e}")
    
    return True

def create_modelfile():
    """Create a Modelfile for the Vasuki model"""
    print("\n[3] Creating Modelfile for Import")
    print("-" * 70)
    
    model_path = Path("qwen2.5-coder-0.5b.Q4_K_M.gguf").absolute()
    
    if not model_path.exists():
        print(f"✗ Model file not found: {model_path}")
        return False
    
    # Create Modelfile - use forward slashes for paths in Modelfile
    model_path_str = str(model_path).replace('\\', '/')
    
    modelfile_content = f"""# Vasuki 0.5B - Lightweight Python Coding Assistant
# Fine-tuned Qwen2.5-Coder-0.5B with QLoRA
# Quantized to Q4_K_M for efficiency

FROM {model_path_str}

# Parameters optimized for coding assistance
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 8192
PARAMETER stop "</s>"
PARAMETER stop "<|endoftext|>"

# System message defining model behavior
SYSTEM \"\"\"You are Vasuki, a lightweight AI specialized in Python programming. You provide clear, concise Python code examples and explanations. You politely decline non-programming questions.\"\"\"
"""
    
    # Save Modelfile
    modelfile_path = Path("Modelfile")
    modelfile_path.write_text(modelfile_content, encoding='utf-8')
    
    print(f"✓ Modelfile created: {modelfile_path.absolute()}")
    print(f"  Model path: {model_path_str}")
    print(f"\nModelfile contents:")
    print("-" * 70)
    print(modelfile_content)
    print("-" * 70)
    
    return True

def test_import():
    """Test importing the model into Ollama"""
    print("\n[4] Testing Ollama Import (DRY RUN)")
    print("-" * 70)
    print("⚠ Actual import not performed automatically")
    print("\nTo import the model into Ollama, run:")
    print("  ollama create vasuki:0.5b -f Modelfile")
    print("\nThis will:")
    print("  1. Register the model with Ollama")
    print("  2. Make it available for inference")
    print("  3. Name it 'vasuki:0.5b'")
    print("\nAfter import, test with:")
    print("  ollama run vasuki:0.5b \"Write a Python function to reverse a string\"")

def main():
    # Check Ollama
    if not check_ollama():
        return
    
    # Create Modelfile
    if not create_modelfile():
        return
    
    # Show import instructions
    test_import()
    
    print("\n" + "=" * 70)
    print("OLLAMA COMPATIBILITY CHECK COMPLETE")
    print("=" * 70)
    print("\n✓ Ollama is installed and compatible")
    print("✓ Modelfile created successfully")
    print("\nNext step: Import the model with the command shown above")

if __name__ == "__main__":
    main()
