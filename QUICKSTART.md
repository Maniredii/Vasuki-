# Quick Start Guide

## Step-by-Step Instructions

### 1. Open PowerShell in this directory
```powershell
cd d:\VASUKI
```

### 2. Run the setup script
```powershell
.\setup.ps1
```

This will:
- Create a Python virtual environment
- Install all required packages
- Set everything up automatically

### 3. Prepare your training data
```powershell
python scripts\prepare_data.py
```

Expected output:
- Downloads Python instruction dataset (~18k samples)
- Generates refusal dataset (5k samples)
- Creates `data/training_data.jsonl` (~23k total samples)
- Takes about 5-10 minutes depending on internet speed

### 4. Verify the data
```powershell
# Check if the file was created
Get-Item data\training_data.jsonl

# Check file size (should be around 50-100 MB)
(Get-Item data\training_data.jsonl).Length / 1MB
```

### 5. Next: Training (Coming Soon)
After data preparation, you'll set up the training script to fine-tune your model.

## Troubleshooting

### Issue: "python not found"
**Solution:** Install Python 3.8+ from python.org

### Issue: "pip install fails"
**Solution:** Try upgrading pip first:
```powershell
python -m pip install --upgrade pip
```

### Issue: "Execution policy error"
**Solution:** Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Dataset download is slow"
**Solution:** This is normal. The dataset is large. Wait for completion.

### Issue: "Out of memory"
**Solution:** Close other applications. The data preparation needs ~4GB RAM.

## What You Have Now

✅ Complete project structure  
✅ Data preparation script  
✅ Requirements file  
✅ Setup automation  
✅ Documentation  

## What's Next

- [ ] Run data preparation
- [ ] Choose base model
- [ ] Create training script
- [ ] Fine-tune the model
- [ ] Evaluate results
- [ ] Deploy locally

## Support

For issues or questions about this setup, check:
1. README.md - Full documentation
2. requirements.txt - Package versions
3. scripts/prepare_data.py - Data preparation logic
