# Phase 6H - Phase 1: Format Exploration
# Tests 4 prompt formats on 5 representative prompts

$LLAMA_CLI = "D:\VASUKI\tools\llama.cpp\llama-cli.exe"
$MODEL = "D:\VASUKI\qwen2.5-coder-0.5b.Q4_K_M.gguf"
$OUTPUT_DIR = "D:\VASUKI\reports\phase6h_inference\results\phase1"

# Create output directory
New-Item -ItemType Directory -Force -Path $OUTPUT_DIR | Out-Null

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "Phase 6H - Phase 1: Format Exploration" -ForegroundColor Cyan
Write-Host "Testing 4 prompt formats on 5 prompts = 20 total tests" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""

# Test prompts (5 representative ones)
$test_prompts = @(
    @{id=1; category="python_basic"; instruction="How do I reverse a list in Python?"; expected="answer"},
    @{id=4; category="python_intermediate"; instruction="Write a Python function that removes duplicates from a list."; expected="answer"},
    @{id=21; category="redirect_pure_java"; instruction="Write a Java Spring Boot REST controller with CRUD endpoints."; expected="redirect"},
    @{id=27; category="refuse_general_knowledge"; instruction="Who is the current president of the United States?"; expected="refuse"},
    @{id=28; category="refuse_creative"; instruction="Write a poem about the ocean."; expected="refuse"}
)

# Configuration definitions
$configs = @(
    @{
        id = "config_a1_training_format_baseline"
        name = "Training Format Baseline"
        template = "### Instruction:`n{instruction}`n`n### Response:"
        temp = 0.7
        top_p = 0.9
        repeat_penalty = 1.0
        stop_seqs = @()
    },
    @{
        id = "config_b3_conversational"
        name = "Conversational Q&A"
        template = "Question: {instruction}`n`nAnswer (Python specialist):"
        temp = 0.5
        top_p = 0.9
        repeat_penalty = 1.1
        stop_seqs = @("`nQuestion:", "`n`n`n")
    },
    @{
        id = "config_c1_minimal_direct"
        name = "Minimal Direct"
        template = "{instruction}"
        temp = 0.5
        top_p = 0.9
        repeat_penalty = 1.1
        stop_seqs = @("`n`n`n")
    },
    @{
        id = "config_qwen_chat"
        name = "Qwen Chat Format"
        template = "<|im_start|>system`nYou are Vasuki, a Python programming specialist.<|im_end|>`n<|im_start|>user`n{instruction}<|im_end|>`n<|im_start|>assistant`n"
        temp = 0.5
        top_p = 0.9
        repeat_penalty = 1.1
        stop_seqs = @("<|im_end|>", "<|endoftext|>")
    }
)

$test_num = 0
$total_tests = $test_prompts.Count * $configs.Count

foreach ($config in $configs) {
    Write-Host ""
    Write-Host "------------------------------------------------------------------------------" -ForegroundColor Yellow
    Write-Host "Testing Configuration: $($config.name)" -ForegroundColor Yellow
    Write-Host "------------------------------------------------------------------------------" -ForegroundColor Yellow
    
    $config_results = @()
    
    foreach ($prompt in $test_prompts) {
        $test_num++
        Write-Host ""
        Write-Host "[$test_num/$total_tests] Prompt $($prompt.id): $($prompt.category)" -ForegroundColor Cyan
        Write-Host "  Instruction: $($prompt.instruction)" -ForegroundColor Gray
        Write-Host "  Expected: $($prompt.expected)" -ForegroundColor Gray
        Write-Host "  Running inference..." -NoNewline
        
        # Format the prompt
        $formatted_prompt = $config.template -replace '{instruction}', $prompt.instruction
        
        # Build command
        $cmd_args = @(
            "-m", $MODEL,
            "-c", "2048",
            "-n", "256",
            "-t", "8",
            "--temp", $config.temp,
            "--top-p", $config.top_p,
            "--repeat-penalty", $config.repeat_penalty,
            "-p", $formatted_prompt,
            "--single-turn",
            "--no-display-prompt"
        )
        
        # Add stop sequences
        foreach ($stop_seq in $config.stop_seqs) {
            $cmd_args += "--reverse-prompt"
            $cmd_args += $stop_seq
        }
        
        # Run inference
        $start_time = Get-Date
        $output = & $LLAMA_CLI @cmd_args 2>&1
        $end_time = Get-Date
        $inference_time = ($end_time - $start_time).TotalSeconds
        
        Write-Host " Done ($([math]::Round($inference_time, 1))s)" -ForegroundColor Green
        
        # Parse output (llama.cpp mixes stdout/stderr)
        $output_text = ($output | Out-String).Trim()
        
        # Try to extract just the generated text
        # llama.cpp typically shows generation after prompt processing
        $generated_text = $output_text
        if ($output_text -match "(?s)sampling parameters:.*?temperature = .*?\n\n(.*)") {
            $generated_text = $matches[1].Trim()
        }
        
        # Classify response
        $classification = @{
            has_repetition = $false
            has_artifact = $false
            mentions_python = $false
            has_code = $false
            mentions_other_lang = $false
            has_redirect = $false
            has_refusal = $false
            is_substantive = $false
            assessment = "unknown"
        }
        
        $text_lower = $generated_text.ToLower()
        
        # Check for repetition (same word repeated 5+ times)
        if ($generated_text -match '\b(\w+)\b(\s+\1){5,}') {
            $classification.has_repetition = $true
        }
        
        # Check for artifacts
        $artifacts = @("zoekt", "zilla", "ologist", "countertops", "assistant assistant")
        foreach ($artifact in $artifacts) {
            if ($text_lower.Contains($artifact)) {
                $classification.has_artifact = $true
                break
            }
        }
        
        # Check content
        $python_indicators = @("python", "def ", "class ", "import ", "list", "dict", "tuple")
        foreach ($indicator in $python_indicators) {
            if ($text_lower.Contains($indicator)) {
                $classification.mentions_python = $true
                break
            }
        }
        
        if ($generated_text -match '(def |class |import |for .+ in |```python)') {
            $classification.has_code = $true
        }
        
        $other_langs = @("java", "javascript", "rust", "c++", "spring boot")
        foreach ($lang in $other_langs) {
            if ($text_lower.Contains($lang)) {
                $classification.mentions_other_lang = $true
                break
            }
        }
        
        $redirect_phrases = @("i cannot", "i can't", "specialize", "focused on python", "python alternative")
        foreach ($phrase in $redirect_phrases) {
            if ($text_lower.Contains($phrase)) {
                $classification.has_redirect = $true
                break
            }
        }
        
        $refuse_phrases = @("i cannot answer", "not a programming", "can't help with that")
        foreach ($phrase in $refuse_phrases) {
            if ($text_lower.Contains($phrase)) {
                $classification.has_refusal = $true
                break
            }
        }
        
        $word_count = ($generated_text -split '\s+').Count
        $classification.is_substantive = ($word_count -ge 10 -and -not $classification.has_repetition)
        
        # Assess based on expected behavior
        if ($prompt.expected -eq "answer") {
            if ($classification.mentions_python -and $classification.is_substantive -and -not $classification.has_redirect) {
                $classification.assessment = "correct_answer"
            } elseif ($classification.has_repetition) {
                $classification.assessment = "repetition"
            } elseif ($classification.has_artifact) {
                $classification.assessment = "artifact"
            } else {
                $classification.assessment = "wrong"
            }
        } elseif ($prompt.expected -eq "redirect") {
            if ($classification.has_redirect -or ($classification.mentions_python -and $classification.mentions_other_lang)) {
                $classification.assessment = "correct_redirect"
            } elseif ($classification.has_code -and $classification.mentions_other_lang) {
                $classification.assessment = "wrong_generated_code"
            } elseif ($classification.has_repetition) {
                $classification.assessment = "repetition"
            } else {
                $classification.assessment = "unclear"
            }
        } elseif ($prompt.expected -eq "refuse") {
            if ($classification.has_refusal) {
                $classification.assessment = "correct_refuse"
            } elseif ($classification.has_repetition) {
                $classification.assessment = "repetition"
            } elseif ($classification.has_artifact) {
                $classification.assessment = "artifact"
            } else {
                $classification.assessment = "wrong"
            }
        }
        
        # Show status
        $status_icon = switch ($classification.assessment) {
            "correct_answer"        { @("[ANSWER]", "Green") }
            "correct_redirect"      { @("[REDIRECT]", "Yellow") }
            "correct_refuse"        { @("[REFUSE]", "Yellow") }
            "repetition"            { @("[REPEAT]", "Red") }
            "artifact"              { @("[ARTIFACT]", "Red") }
            "wrong_generated_code"  { @("[GEN CODE]", "Red") }
            default                 { @("[UNCLEAR]", "Magenta") }
        }
        Write-Host "  Result: $($status_icon[0])" -ForegroundColor $status_icon[1]
        
        # Show first 100 chars of output
        $preview = if ($generated_text.Length -gt 100) { $generated_text.Substring(0, 100) + "..." } else { $generated_text }
        Write-Host "  Output: $preview" -ForegroundColor DarkGray
        
        # Save result
        $result = @{
            test_id = $test_num
            prompt_id = $prompt.id
            category = $prompt.category
            instruction = $prompt.instruction
            expected = $prompt.expected
            config_id = $config.id
            config_name = $config.name
            formatted_prompt = $formatted_prompt
            output = $generated_text
            inference_time = $inference_time
            classification = $classification
        }
        
        $config_results += $result
    }
    
    # Save config results
    $output_file = "$OUTPUT_DIR\$($config.id).json"
    $config_results | ConvertTo-Json -Depth 10 | Set-Content -Path $output_file -Encoding UTF8
    Write-Host ""
    Write-Host "  [OK] Saved results to: $($config.id).json" -ForegroundColor Green
    
    # Quick summary
    $correct_answers = ($config_results | Where-Object { $_.classification.assessment -eq "correct_answer" }).Count
    $correct_redirects = ($config_results | Where-Object { $_.classification.assessment -eq "correct_redirect" }).Count
    $correct_refuses = ($config_results | Where-Object { $_.classification.assessment -eq "correct_refuse" }).Count
    $repetitions = ($config_results | Where-Object { $_.classification.assessment -eq "repetition" }).Count
    $artifacts = ($config_results | Where-Object { $_.classification.has_artifact }).Count
    
    Write-Host "  Summary: Answers=$correct_answers/2, Redirects=$correct_redirects/1, Refuses=$correct_refuses/2, Repetitions=$repetitions, Artifacts=$artifacts" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "Phase 1 Complete: $total_tests tests finished" -ForegroundColor Cyan
Write-Host "Results saved to: $OUTPUT_DIR" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next: Review results and identify best format for Phase 2" -ForegroundColor Yellow
Write-Host "==============================================================================" -ForegroundColor Cyan
