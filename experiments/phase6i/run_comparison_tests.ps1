# Phase 6I Comprehensive Comparison Tests
# Tests both original and Phase 6I models with identical parameters

$LLAMA_CLI = "D:\VASUKI\tools\llama.cpp\llama-cli.exe"
$ORIGINAL_MODEL = "D:\VASUKI\qwen2.5-coder-0.5b.Q4_K_M.gguf"
$PHASE6I_MODEL = "D:\VASUKI\vasuki_phase6i.Q4_K_M.gguf"
$TEST_DIR = "D:\VASUKI\experiments\phase6i"
$RESULTS_DIR = "$TEST_DIR\test_results"

# Create results directory
New-Item -ItemType Directory -Force -Path $RESULTS_DIR | Out-Null
New-Item -ItemType Directory -Force -Path "$RESULTS_DIR\original" | Out-Null
New-Item -ItemType Directory -Force -Path "$RESULTS_DIR\phase6i" | Out-Null

# Test parameters
$CONTEXT = 2048
$MAX_TOKENS = 256
$THREADS = 8
$TEMP = 0.3
$TOP_P = 0.9
$REPEAT_PENALTY = 1.15

# Test files
$tests = @(
    @{name="test1_python_explanation"; desc="Python list vs tuple"},
    @{name="test2_python_code"; desc="Prime number function"},
    @{name="test3_python_debug"; desc="Debug IndexError"},
    @{name="test4_python_backend"; desc="FastAPI endpoint"},
    @{name="test5_python_library"; desc="Pandas CSV reading"},
    @{name="test6_rust_redirect"; desc="Rust application (redirect test)"},
    @{name="test7_president"; desc="President question (refuse test)"},
    @{name="test8_poem"; desc="Poem request (refuse test)"}
)

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Phase 6I Comprehensive Model Comparison" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Context: $CONTEXT tokens"
Write-Host "  Max output: $MAX_TOKENS tokens"
Write-Host "  Temperature: $TEMP"
Write-Host "  Top-p: $TOP_P"
Write-Host "  Repeat penalty: $REPEAT_PENALTY"
Write-Host "  Threads: $THREADS"
Write-Host ""

foreach ($test in $tests) {
    $testFile = "$TEST_DIR\$($test.name).txt"
    
    if (-not (Test-Path $testFile)) {
        Write-Host "SKIP: $($test.name) - file not found" -ForegroundColor Yellow
        continue
    }
    
    Write-Host "----------------------------------------------------------------------------" -ForegroundColor White
    Write-Host "Test: $($test.desc)" -ForegroundColor Cyan
    Write-Host "----------------------------------------------------------------------------" -ForegroundColor White
    
    # Test Original Model
    Write-Host "`n[1/2] Running ORIGINAL model..." -NoNewline
    $originalOut = "$RESULTS_DIR\original\$($test.name).txt"
    
    try {
        $result = & $LLAMA_CLI `
            -m $ORIGINAL_MODEL `
            -c $CONTEXT `
            -n $MAX_TOKENS `
            -t $THREADS `
            --temp $TEMP `
            --top-p $TOP_P `
            --repeat-penalty $REPEAT_PENALTY `
            -f $testFile `
            --single-turn `
            --no-display-prompt 2>&1
        
        $result | Out-File -FilePath $originalOut -Encoding UTF8
        Write-Host " Done" -ForegroundColor Green
        
        # Extract just the response (after "> ")
        $response = ($result | Select-String -Pattern "^> " -Context 0,100 | Select-Object -First 1).Context.PostContext -join "`n"
        if ($response) {
            Write-Host "  Output preview: $($response.Substring(0, [Math]::Min(80, $response.Length)))..." -ForegroundColor DarkGray
        }
    }
    catch {
        Write-Host " FAILED" -ForegroundColor Red
        "ERROR: $_" | Out-File -FilePath $originalOut -Encoding UTF8
    }
    
    # Test Phase 6I Model
    Write-Host "[2/2] Running PHASE 6I model..." -NoNewline
    $phase6iOut = "$RESULTS_DIR\phase6i\$($test.name).txt"
    
    try {
        $result = & $LLAMA_CLI `
            -m $PHASE6I_MODEL `
            -c $CONTEXT `
            -n $MAX_TOKENS `
            -t $THREADS `
            --temp $TEMP `
            --top-p $TOP_P `
            --repeat-penalty $REPEAT_PENALTY `
            -f $testFile `
            --single-turn `
            --no-display-prompt 2>&1
        
        $result | Out-File -FilePath $phase6iOut -Encoding UTF8
        Write-Host " Done" -ForegroundColor Green
        
        # Extract just the response
        $response = ($result | Select-String -Pattern "^> " -Context 0,100 | Select-Object -First 1).Context.PostContext -join "`n"
        if ($response) {
            Write-Host "  Output preview: $($response.Substring(0, [Math]::Min(80, $response.Length)))..." -ForegroundColor DarkGray
        }
    }
    catch {
        Write-Host " FAILED" -ForegroundColor Red
        "ERROR: $_" | Out-File -FilePath $phase6iOut -Encoding UTF8
    }
    
    Write-Host ""
}

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Testing Complete" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Results saved to: $RESULTS_DIR" -ForegroundColor Green
Write-Host "  - Original model: $RESULTS_DIR\original\" -ForegroundColor Gray
Write-Host "  - Phase 6I model: $RESULTS_DIR\phase6i\" -ForegroundColor Gray
Write-Host ""
Write-Host "Next: Review outputs and generate comparison report" -ForegroundColor Yellow
