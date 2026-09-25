# Phase 4 Test Script - CPU Baseline with Vasuki 0.5B

$llamaPath = "D:\VASUKI\tools\llama.cpp\llama-cli.exe"
$modelPath = "D:\VASUKI\qwen2.5-coder-0.5b.Q4_K_M.gguf"
$outputDir = "D:\VASUKI\reports"

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "PHASE 4: CPU BASELINE TESTING" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

Write-Host "`nConfiguration:"
Write-Host "  Model: qwen2.5-coder-0.5b.Q4_K_M.gguf"
Write-Host "  Context Size: 2048"
Write-Host "  Max Tokens: 256"
Write-Host "  CPU Threads: 8"
Write-Host "  Temperature: 0.7"

# Test prompt
$prompt = "Explain what a Python variable is to a beginner. Give one simple example."

Write-Host "`n[TEST 1] Basic Python Explanation"
Write-Host "Prompt: $prompt"
Write-Host "`nGenerating response..."

# Create prompt file
$prompt | Out-File -FilePath "$outputDir\prompt_test1.txt" -Encoding utf8

# Run inference with proper flags to exit after generation
$startTime = Get-Date

$output = & $llamaPath `
  -m $modelPath `
  -c 2048 `
  -n 256 `
  -t 8 `
  --temp 0.7 `
  --top-p 0.9 `
  -p $prompt `
  --no-display-prompt `
  2>&1

$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds

# Save output
$output | Out-File -FilePath "$outputDir\test1_output.txt" -Encoding utf8

Write-Host "`n" + ("=" * 70) -ForegroundColor Green
Write-Host "TEST COMPLETE" -ForegroundColor Green
Write-Host ("=" * 70) -ForegroundColor Green
Write-Host "`nExecution Time: $duration seconds"
Write-Host "Output saved to: $outputDir\test1_output.txt"

# Extract performance stats
$statsLine = $output | Select-String -Pattern "Prompt:.*Generation:"
if ($statsLine) {
    Write-Host "`nPerformance Stats:"
    Write-Host "  $statsLine"
}
