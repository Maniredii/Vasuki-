# PowerShell setup script for Vasuki 0.5B Project

$separator = "=" * 60

Write-Host $separator -ForegroundColor Cyan
Write-Host "VASUKI 0.5B PROJECT SETUP" -ForegroundColor Cyan
Write-Host $separator -ForegroundColor Cyan

# Step 1: Create virtual environment
Write-Host "`n[1/3] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping creation." -ForegroundColor Green
} else {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Virtual environment created successfully" -ForegroundColor Green
    } else {
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Step 2: Activate virtual environment and install dependencies
Write-Host "`n[2/3] Installing dependencies..." -ForegroundColor Yellow
Write-Host "Activating virtual environment..." -ForegroundColor Gray

& ".\venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Virtual environment activated" -ForegroundColor Green
    
    Write-Host "Installing required packages..." -ForegroundColor Gray
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Step 3: Summary
Write-Host "`n[3/3] Setup complete!" -ForegroundColor Yellow
Write-Host "`n$separator" -ForegroundColor Cyan
Write-Host "NEXT STEPS" -ForegroundColor Cyan
Write-Host $separator -ForegroundColor Cyan
Write-Host "1. Run the data preparation script:" -ForegroundColor White
Write-Host '   python scripts\prepare_data.py' -ForegroundColor Gray
Write-Host "`n2. The script will download and prepare your training data" -ForegroundColor White
Write-Host "`n3. Check the data folder for training_data.jsonl" -ForegroundColor White
Write-Host $separator -ForegroundColor Cyan

Write-Host "`nVirtual environment is active. You can now run:" -ForegroundColor Green
Write-Host 'python scripts\prepare_data.py' -ForegroundColor Yellow
