# PowerShell script to download official llama.cpp Windows binaries

$separator = "=" * 70
$TargetDir = "D:\VASUKI\tools\llama.cpp"
$DownloadUrl = "https://github.com/ggml-org/llama.cpp/releases/latest/download/llama-b11153-bin-win-cpu-x64.zip"
$ZipFile = "$TargetDir\llama-cpp.zip"

Write-Host $separator -ForegroundColor Cyan
Write-Host "DOWNLOADING LLAMA.CPP OFFICIAL WINDOWS BUILD" -ForegroundColor Cyan
Write-Host $separator -ForegroundColor Cyan

Write-Host "`nTarget Directory: $TargetDir"
Write-Host "Download URL: $DownloadUrl"

# Create directory if it doesn't exist
if (!(Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    Write-Host "`nCreated directory: $TargetDir" -ForegroundColor Green
}

# Download the file
Write-Host "`n[1/3] Downloading llama.cpp Windows x64 (CPU) build..." -ForegroundColor Yellow
Write-Host "This may take a few minutes depending on your internet speed..."

try {
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $DownloadUrl -OutFile $ZipFile -ErrorAction Stop
    Write-Host "Download complete" -ForegroundColor Green
    
    $fileSize = (Get-Item $ZipFile).Length / 1MB
    Write-Host "  Downloaded: $([math]::Round($fileSize, 2)) MB"
}
catch {
    Write-Host "Download failed: $_" -ForegroundColor Red
    Write-Host "`nAlternative: Download manually from:" -ForegroundColor Yellow
    Write-Host "https://github.com/ggml-org/llama.cpp/releases" -ForegroundColor Cyan
    Write-Host "Look for: Windows x64 (CPU) build" -ForegroundColor Cyan
    exit 1
}

# Extract the zip file
Write-Host "`n[2/3] Extracting files..." -ForegroundColor Yellow
try {
    Expand-Archive -Path $ZipFile -DestinationPath $TargetDir -Force
    Write-Host "Extraction complete" -ForegroundColor Green
}
catch {
    Write-Host "Extraction failed: $_" -ForegroundColor Red
    exit 1
}

# Clean up zip file
Write-Host "`n[3/3] Cleaning up..." -ForegroundColor Yellow
Remove-Item $ZipFile -Force
Write-Host "Cleanup complete" -ForegroundColor Green

# List downloaded files
Write-Host "`n$separator" -ForegroundColor Cyan
Write-Host "INSTALLATION COMPLETE" -ForegroundColor Cyan
Write-Host $separator -ForegroundColor Cyan

Write-Host "`nInstalled Executables:"
$exeFiles = Get-ChildItem $TargetDir -Recurse -File | Where-Object {$_.Extension -eq '.exe'}
foreach ($file in $exeFiles) {
    Write-Host "  - $($file.Name)" -ForegroundColor Green
}

Write-Host "`nllama.cpp location: $TargetDir"
Write-Host "`nNext: Run Phase 4 validation to test the model"
