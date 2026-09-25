# Single test runner for Vasuki 0.5B

param(
    [string]$Prompt = "Explain what a Python variable is to a beginner. Give one simple example.",
    [int]$ContextSize = 2048,
    [int]$MaxTokens = 256,
    [int]$Threads = 8
)

$llamaPath = "D:\VASUKI\tools\llama.cpp\llama-cli.exe"
$modelPath = "D:\VASUKI\qwen2.5-coder-0.5b.Q4_K_M.gguf"

Write-Host "Running single-turn inference..." -ForegroundColor Cyan
Write-Host "Prompt: $Prompt`n"

$startTime = Get-Date

& $llamaPath `
  -m $modelPath `
  -c $ContextSize `
  -n $MaxTokens `
  -t $Threads `
  --temp 0.7 `
  --top-p 0.9 `
  -p $Prompt `
  --single-turn `
  --no-display-prompt `
  2>&1

$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds

Write-Host "`n`nExecution completed in $duration seconds" -ForegroundColor Green
