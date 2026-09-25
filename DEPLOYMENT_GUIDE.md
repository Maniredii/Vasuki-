# Vasuki 0.5B Deployment Guide

Quick reference for deploying your validated GGUF model to Ollama.

---

## ✅ Validation Complete

Your model has been validated and is ready for deployment. See `VALIDATION_REPORT.md` for full details.

---

## 🚀 Quick Deployment (3 Steps)

### Step 1: Ensure Ollama is Running

Check if Ollama is running:
```powershell
ollama list
```

If not running, start the Ollama application from your Start Menu or system tray.

### Step 2: Import the Model

```powershell
ollama create vasuki:0.5b -f Modelfile
```

This will:
- Register your model with Ollama
- Make it available for immediate use
- Name it `vasuki:0.5b`

Expected output:
```
transferring model data
using existing layer sha256:...
creating model layer
success
```

### Step 3: Test the Model

```powershell
ollama run vasuki:0.5b "Write a Python function to check if a number is prime"
```

---

## 📝 Testing Your Model

### Basic Python Tasks
```powershell
# Function writing
ollama run vasuki:0.5b "Write a function to reverse a list"

# Code explanation
ollama run vasuki:0.5b "Explain what a Python decorator does"

# Debugging
ollama run vasuki:0.5b "Fix this code: def add(a b): return a+b"

# Best practices
ollama run vasuki:0.5b "Show me the Pythonic way to swap two variables"
```

### Test Refusal Behavior
Your model was trained to decline non-programming questions:

```powershell
ollama run vasuki:0.5b "What is the capital of France?"
```

Expected: Polite refusal focusing on Python programming.

---

## 🔧 Model Configuration

### Current Settings (in Modelfile)
- **Temperature**: 0.7 (balanced)
- **Context Window**: 8,192 tokens
- **Top-p**: 0.9
- **Top-k**: 40

### Adjusting Temperature

For more deterministic code:
```powershell
ollama run vasuki:0.5b --temperature 0.3 "your prompt"
```

For more creative solutions:
```powershell
ollama run vasuki:0.5b --temperature 0.9 "your prompt"
```

---

## 🐍 Python API Usage

### Using ollama-python

Install:
```powershell
pip install ollama
```

Use in Python:
```python
import ollama

response = ollama.chat(model='vasuki:0.5b', messages=[
  {
    'role': 'user',
    'content': 'Write a function to find fibonacci numbers',
  },
])

print(response['message']['content'])
```

### Streaming Responses
```python
import ollama

stream = ollama.chat(
    model='vasuki:0.5b',
    messages=[{'role': 'user', 'content': 'Explain list comprehensions'}],
    stream=True,
)

for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
```

---

## 📊 Performance Monitoring

### Check Memory Usage

While the model is running:
```powershell
# Task Manager > Performance > GPU Memory
# Should see ~400-500 MB usage
```

### Benchmark Response Time

```python
import ollama
import time

start = time.time()
response = ollama.chat(
    model='vasuki:0.5b',
    messages=[{'role': 'user', 'content': 'Write a hello world function'}]
)
end = time.time()

print(f"Response time: {end - start:.2f} seconds")
```

Expected: 1-5 seconds depending on hardware and prompt complexity.

---

## 🛠️ Troubleshooting

### Import Fails

**Error**: `Error: invalid model file`

**Solution**:
1. Verify file integrity: `python validate_gguf.py`
2. Check path in Modelfile is correct
3. Use absolute path with forward slashes

### Model Gives Poor Responses

**Possible Causes**:
1. Context too small - increase `num_ctx` in Modelfile
2. Temperature too high/low - adjust as needed
3. Fine-tuning may not have worked - test with F16 version

### Out of Memory

**Solutions**:
1. Close other GPU-using applications
2. Reduce context window in Modelfile
3. Use CPU-only mode: `ollama run vasuki:0.5b --gpu-layers 0`

### Slow Performance on GPU

**Check**:
```powershell
ollama ps
```

Ensure GPU is being used. If not, reinstall Ollama with GPU support.

---

## 🔄 Model Management

### List All Models
```powershell
ollama list
```

### Update Model
If you retrain and get a new GGUF file:
```powershell
# Delete old version
ollama rm vasuki:0.5b

# Import new version
ollama create vasuki:0.5b -f Modelfile
```

### Delete Model
```powershell
ollama rm vasuki:0.5b
```

### Copy/Rename Model
```powershell
ollama cp vasuki:0.5b vasuki:backup
```

---

## 📈 Next Steps

### 1. Integration Options
- VSCode extension (Continue, Ollama Autocoder)
- Jupyter notebooks
- Web API (Ollama serves REST API by default)
- Discord/Slack bots

### 2. Further Fine-Tuning
If the model doesn't perform as expected:
- Collect problematic examples
- Retrain with additional data
- Experiment with different quantization levels (Q5_K_M, Q6_K)

### 3. Sharing Your Model
To share with others:
```powershell
# Export
ollama show vasuki:0.5b --modelfile > shared-modelfile

# They import with:
ollama create vasuki:0.5b -f shared-modelfile
```

---

## 📞 Support Resources

- **Ollama Docs**: https://github.com/ollama/ollama/tree/main/docs
- **GGUF Format**: https://github.com/ggerganov/ggml/blob/master/docs/gguf.md
- **Qwen2.5-Coder**: https://huggingface.co/Qwen/Qwen2.5-Coder-0.5B

---

## ✅ Deployment Checklist

- [ ] Ollama service is running
- [ ] Model imported successfully (`ollama create vasuki:0.5b -f Modelfile`)
- [ ] Basic test passed (simple Python question)
- [ ] Refusal test passed (non-programming question)
- [ ] Performance acceptable (<5s response time)
- [ ] Memory usage acceptable (<600 MB)
- [ ] Integrated into your workflow

---

**Model**: Vasuki 0.5B  
**Quantization**: Q4_K_M  
**Size**: 379 MB  
**Context**: 32K tokens (configured to 8K for stability)  
**Platform**: Ollama 0.34.3+ on Windows  

**Status**: ✅ Ready for Production Use
