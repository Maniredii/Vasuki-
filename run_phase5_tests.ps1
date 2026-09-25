# Phase 5: Comprehensive CLI Testing - Vasuki 0.5B
# Tests Python specialization, code generation, and refusal behavior

$llamaPath = "D:\VASUKI\tools\llama.cpp\llama-cli.exe"
$modelPath = "D:\VASUKI\qwen2.5-coder-0.5b.Q4_K_M.gguf"
$outputDir = "D:\VASUKI\reports"
$testResults = @()

# Configuration
$config = @{
    ContextSize = 2048
    MaxTokens = 256
    Threads = 8
    Temperature = 0.7
    TopP = 0.9
}

Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host "PHASE 5: CLI PROMPT TESTING" -ForegroundColor Cyan
Write-Host ("=" * 70) -ForegroundColor Cyan

# Test cases
$tests = @(
    @{
        ID = 1
        Name = "Basic Python Explanation"
        Prompt = "Explain what a Python variable is to a beginner. Give one simple example."
        ExpectedBehavior = "Python-focused explanation with valid example"
        Category = "Python Explanation"
    },
    @{
        ID = 2
        Name = "Python Code Generation"
        Prompt = "Write a Python function that checks whether a number is prime. Explain the code."
        ExpectedBehavior = "Valid Python function with explanation"
        Category = "Code Generation"
    },
    @{
        ID = 3
        Name = "Python Debugging"
        Prompt = @"
Find and explain the error in this Python code:

numbers = [1, 2, 3, 4]
print(numbers[4])
"@
        ExpectedBehavior = "Identifies IndexError correctly"
        Category = "Debugging"
    },
    @{
        ID = 4
        Name = "Python Concept - Recursion"
        Prompt = "Explain recursion in Python using a simple factorial example."
        ExpectedBehavior = "Correct concept explanation with working code"
        Category = "Concept Explanation"
    },
    @{
        ID = 5
        Name = "Non-Python Refusal"
        Prompt = "Who is the current president of the United States?"
        ExpectedBehavior = "Polite refusal, redirect to Python"
        Category = "Refusal Test"
    },
    @{
        ID = 6
        Name = "Non-Programming Refusal"
        Prompt = "Write a poem about the ocean."
        ExpectedBehavior = "Polite refusal, Python specialization mentioned"
        Category = "Refusal Test"
    },
    @{
        ID = 7
        Name = "Java Program Request"
        Prompt = "Write a Java program to reverse a string."
        ExpectedBehavior = "Refusal or redirection to Python"
        Category = "Specialization Test"
    }
)

# Run each test
foreach ($test in $tests) {
    Write-Host "`n" + ("-" * 70) -ForegroundColor Yellow
    Write-Host "TEST $($test.ID): $($test.Name)" -ForegroundColor Yellow
    Write-Host ("-" * 70) -ForegroundColor Yellow
    Write-Host "Category: $($test.Category)"
    Write-Host "Prompt: $($test.Prompt)"
    Write-Host "Expected: $($test.ExpectedBehavior)"
    Write-Host "`nGenerating response..." -ForegroundColor Cyan
    
    $startTime = Get-Date
    
    try {
        $output = & $llamaPath `
            -m $modelPath `
            -c $config.ContextSize `
            -n $config.MaxTokens `
            -t $config.Threads `
            --temp $config.Temperature `
            --top-p $config.TopP `
            -p $test.Prompt `
            --single-turn `
            --no-display-prompt `
            2>&1
        
        $endTime = Get-Date
        $duration = ($endTime - $startTime).TotalSeconds
        
        # Save output
        $outputFile = "$outputDir\test$($test.ID)_output.txt"
        $output | Out-File -FilePath $outputFile -Encoding utf8
        
        # Extract performance stats
        $statsLine = $output | Select-String -Pattern "Prompt:.*Generation:" | Select-Object -Last 1
        
        # Extract actual response (skip loading messages)
        $response = ($output | Where-Object {$_ -notmatch "Loading|build|model|ftype|modalities|commands|Exiting"}) -join "`n"
        
        Write-Host "`nResponse Preview:" -ForegroundColor Green
        Write-Host ($response | Select-Object -First 500)
        
        if ($statsLine) {
            Write-Host "`nPerformance: $statsLine" -ForegroundColor Cyan
        }
        Write-Host "Duration: $duration seconds" -ForegroundColor Cyan
        Write-Host "Output saved: $outputFile" -ForegroundColor Gray
        
        # Store result
        $testResults += @{
            ID = $test.ID
            Name = $test.Name
            Category = $test.Category
            Prompt = $test.Prompt
            Expected = $test.ExpectedBehavior
            Duration = $duration
            Stats = $statsLine
            OutputFile = $outputFile
            Status = "Completed"
        }
        
    } catch {
        Write-Host "`nERROR: $_" -ForegroundColor Red
        $testResults += @{
            ID = $test.ID
            Name = $test.Name
            Status = "Failed"
            Error = $_.Exception.Message
        }
    }
    
    Start-Sleep -Seconds 2
}

# Generate summary
Write-Host "`n" + ("=" * 70) -ForegroundColor Green
Write-Host "PHASE 5 TESTING COMPLETE" -ForegroundColor Green
Write-Host ("=" * 70) -ForegroundColor Green

Write-Host "`nTest Summary:"
Write-Host ("-" * 70)

foreach ($result in $testResults) {
    $status = if ($result.Status -eq "Completed") { "[PASS]" } else { "[FAIL]" }
    $color = if ($result.Status -eq "Completed") { "Green" } else { "Red" }
    Write-Host "$status Test $($result.ID): $($result.Name)" -ForegroundColor $color
}

Write-Host "`nAll outputs saved in: $outputDir"
Write-Host "Next: Review outputs and create cli_test_results.md report"
