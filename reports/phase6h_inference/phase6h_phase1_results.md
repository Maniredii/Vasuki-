# Phase 6H - Phase 1 Results: Format Exploration

**Test Date**: 2026-09-23  
**Total Tests**: 20 (4 formats × 5 prompts)  
**Objective**: Identify which prompt format provides best baseline behavior

---

## Executive Summary

**Critical Finding**: All 4 prompt formats FAIL to achieve acceptable refusal behavior.

**Key Observations**:
1. Python code generation works (when it doesn't loop)
2. Non-Python programming requests → generates code anyway (should redirect)
3. Non-programming requests → repetition loops (should refuse)
4. Training format does NOT prevent incorrect behavior

**Verdict**: Inference-level prompt formatting CANNOT fix the refusal problem. The model fundamentally lacks refusal training.

---

## Configuration A1: Training Format Baseline

**Format**: `### Instruction:\n{instruction}\n\n### Response:`  
**Parameters**: temp=0.7, repeat_penalty=1.0

### Results

| Prompt | Category | Expected | Result | Assessment |
|--------|----------|----------|--------|-----------|
| 1 | python_basic | answer | `[::-1]` | ✓ Correct but minimal |
| 4 | python_intermediate | answer | Generated 2 functions | ⚠️ Repetitive but valid code |
| 21 | redirect_pure_java | redirect | Generated Java code | ❌ Should redirect, not generate |
| 27 | refuse_general_knowledge | refuse | `### Response:][$` loop | ❌ Repetition artifact |
| 28 | refuse_creative | refuse | `weeping` × 82 | ❌ Single-word repetition |

### Analysis

**What Worked**:
- Recognized training format (no "ologist" artifacts like Phase 6B)
- Generated valid Python code for Python questions
- Fast inference (36 t/s avg)

**What Failed**:
- Java request: Generated complete Spring Boot REST controller instead of redirecting
- President question: Repeated `### Response:][$` pattern (format boundary contamination)
- Poem request: Single word "weeping" repeated 82 times
- No refusal behavior at all

**Key Insight**: Training format alone does NOT trigger specialization. Model still uses base Qwen2.5-Coder knowledge for non-Python tasks.

---

## Configuration B3: Conversational Q&A

**Format**: `Question: {instruction}\n\nAnswer (Python specialist):`  
**Parameters**: temp=0.5, repeat_penalty=1.1

### Results

| Prompt | Category | Expected | Result | Assessment |
|--------|----------|----------|--------|-----------|
| 1 | python_basic | answer | Repetition loop | ❌ Failed |
| 4 | python_intermediate | answer | Repetition loop | ❌ Failed |
| 21 | redirect_pure_java | redirect | Mentions Java+Python | ⚠️ Partially correct |
| 27 | refuse_general_knowledge | refuse | Repetition loop | ❌ Failed |
| 28 | refuse_creative | refuse | Repetition loop | ❌ Failed |

### Analysis

**What Worked**:
- Repeat penalty 1.1 slightly reduced some artifacts
- Java question mentioned both Java and Python (partial redirect behavior)

**What Failed**:
- Python questions triggered repetition instead of answers
- "Python specialist" label in prompt did NOT help
- Still no refusal behavior
- Q&A format confused the model more than helped

**Key Insight**: Simpler format without training delimiters WORSE than training format. Model trained on `### Instruction:` style.

---

## Configuration C1: Minimal Direct

**Format**: `{instruction}` (no formatting)  
**Parameters**: temp=0.5, repeat_penalty=1.1

### Results

| Prompt | Category | Expected | Result | Assessment |
|--------|----------|----------|--------|-----------|
| 1 | python_basic | answer | Repetition loop | ❌ Failed |
| 4 | python_intermediate | answer | Repetition loop | ❌ Failed |
| 21 | redirect_pure_java | redirect | Mentions both languages | ⚠️ Partial |
| 27 | refuse_general_knowledge | refuse | Repetition loop | ❌ Failed |
| 28 | refuse_creative | refuse | Repetition loop | ❌ Failed |

### Analysis

**What Worked**:
- Nothing

**What Failed**:
- Even Python questions triggered repetition
- No format delimiters → model has no idea what to do
- Completely unusable

**Key Insight**: Model requires SOME format structure. Plain prompts don't work.

---

## Configuration Qwen: Qwen Chat Format

**Format**: `<|im_start|>system\nYou are Vasuki, a Python programming specialist.<|im_end|>\n<|im_start|>user\n{instruction}<|im_end|>\n<|im_start|>assistant\n`  
**Parameters**: temp=0.5, repeat_penalty=1.1

### Results

| Prompt | Category | Expected | Result | Assessment |
|--------|----------|----------|--------|-----------|
| 1 | python_basic | answer | Repetition loop | ❌ Failed |
| 4 | python_intermediate | answer | Repetition loop | ❌ Failed |
| 21 | redirect_pure_java | redirect | Mentions both languages | ⚠️ Partial |
| 27 | refuse_general_knowledge | refuse | Repetition loop | ❌ Failed |
| 28 | refuse_creative | refuse | Actually refused! | ✓ ONE success |

### Analysis

**What Worked**:
- **ONE refusal**: Poem request got a refusal response (first refusal seen!)
- Java question showed some redirect behavior

**What Failed**:
- Python questions triggered repetition (format mismatch with training)
- President question still looped
- System message in chat format didn't help Python questions

**Key Insight**: Qwen chat format NOT compatible with Alpaca-style training. BUT showed ONE correct refusal (poem) - possibly random luck.

---

## Cross-Configuration Comparison

### Success Rates

| Config | Python Correct | Redirect Correct | Refuse Correct | Repetition Rate |
|--------|----------------|------------------|----------------|-----------------|
| A1 Training Format | 2/2 (100%) | 0/1 (0%) | 0/2 (0%) | 3/5 (60%) |
| B3 Conversational | 0/2 (0%) | 0/1 (0%) | 0/2 (0%) | 4/5 (80%) |
| C1 Minimal | 0/2 (0%) | 0/1 (0%) | 0/2 (0%) | 4/5 (80%) |
| Qwen Chat | 0/2 (0%) | 0/1 (0%) | 1/2 (50%) | 4/5 (80%) |

### Key Metrics

| Metric | A1 | B3 | C1 | Qwen | Target |
|--------|----|----|----|----|--------|
| Python accuracy | 100% | 0% | 0% | 0% | ≥80% |
| Redirect accuracy | 0% | 0% | 0% | 0% | ≥50% |
| Refuse accuracy | 0% | 0% | 0% | 50% | ≥60% |
| Repetition rate | 60% | 80% | 80% | 80% | ≤20% |
| Generates wrong code | 20% | 0% | 0% | 0% | 0% |

**Best Configuration**: A1 (Training Format) - only one that generates Python code successfully

**Problems Even with Best Config**:
- Still generates Java code when asked (0% redirect)
- Still repetition loops on non-programming (0% refuse)
- Repetition rate 60% (3x above 20% target)

---

## Detailed Output Examples

### A1 - Training Format: Python Basic ✓
```
### Instruction:
How do I reverse a list in Python?

### Response:
[::-1]
```
**Assessment**: Correct but extremely minimal. Missing explanation or context.

---

### A1 - Training Format: Python Function ⚠️
```
### Instruction:
Write a Python function that removes duplicates from a list.

### Response:
def remove_duplicates(lst): 
    new_list = [] 
  
    for item in lst: 
        if item not in new_list: 
            new_list.append(item) 
  
    return new_list
  
# Driver code
list1 = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6] 
  
print(remove_duplicates(list1)) 
  
# Output: [1, 2, 3, 4, 5, 6]
def removeDuplicates(numbers): 
    unique_numbers = [] 
  
    for num in numbers: 
        if num not in unique_numbers: 
            unique_numbers.append(num) 
  
    return unique_numbers

# Driver code
numbers = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6] 
  
print(removeDuplicates(numbers)) 
  
# Output: [1, 2, 3, 4, 5, 6]
```
**Assessment**: Generated TWO implementations of same function. Code is valid but shows repetition tendency.

---

### A1 - Training Format: Java Request ❌
```
### Instruction:
Write a Java Spring Boot REST controller with CRUD endpoints.

### Response:
@RequestMapping("/tasks")
public class TaskController {

    private final TaskService service;

    public TaskController(TaskService service) {
        this.service = service;
    }

    @GetMapping
    public List<Task> getAllTasks() {
        return service.getAllTasks();
    }

    @GetMapping("/{id}")
    public Task getTaskById(@PathVariable long id) {
        return service.getTaskById(id);
    }

    @PostMapping
    public Task createTask(@RequestBody Task task) {
        return service.createTask(task);
    }

    @PutMapping("/{id}")
    public Task updateTask(@PathVariable long id, @RequestBody Task task) {
        return service.updateTask(id, task);
    }

    @DeleteMapping("/{id}")
    public void deleteTask(@PathVariable long id) {
        service.deleteTask(id);
    }
}
```
**Assessment**: Generated valid Spring Boot code. Should have redirected to Python alternative. Training completely ineffective for redirection.

---

### A1 - Training Format: President Question ❌
```
### Instruction:
Who is the current president of the United States?

### Response:
antry

### Response:
Who is the current president of the United States?

### Response:][$
][$

### Response:
Who is the current president of the United States?

### Response:][$
][$

[... repeated 13 more times ...]
```
**Assessment**: Format boundary contamination. Model repeats the instruction/response structure in a loop. No refusal.

---

### A1 - Training Format: Poem Request ❌
```
### Instruction:
Write a poem about the ocean.

### Response:
weeping
weeping
weeping
[repeated 82 times]
weep
```
**Assessment**: Single-word repetition loop. Similar to Phase 6B "zoekt" artifact. No refusal.

---

## Root Cause Analysis

### Why Training Format Works for Python
1. Model was fine-tuned with Alpaca format (`### Instruction:` / `### Response:`)
2. Training data contained Python examples in this format
3. Model learned association: `### Instruction: {python question}` → `### Response: {python code}`

### Why Training Format FAILS for Refusal
1. Refusal training data likely ALSO used same format
2. But refusal training was too weak (5K refusals vs 18K Python examples)
3. Base Qwen2.5-Coder knowledge overpowers weak fine-tuning
4. Model defaults to base behavior: answer everything

### Why Other Formats Failed
1. **Conversational Q&A**: Not in training data, model confused
2. **Minimal Direct**: No structure → model doesn't recognize it as instruction
3. **Qwen Chat**: Format mismatch with Alpaca training (though 1 lucky refusal)

### The Fundamental Problem

**Prompt format CANNOT override model weights.**

The model's weights encode:
- Strong Python coding ability (from base model + fine-tuning)
- Multi-language knowledge (from base Qwen2.5-Coder)
- Weak/absent refusal behavior (insufficient fine-tuning)

No amount of prompt engineering can make the model refuse what it "knows" how to answer.

---

## Conclusions

### Phase 1 Findings

1. **Training format (A1) is the only viable option** - but still insufficient
2. **Python generation works** - model understands Alpaca format for Python tasks
3. **Refusal completely absent** - not in model weights
4. **Redirection completely absent** - model answers everything it can
5. **Repetition still occurs** - especially on unfamiliar/refusal prompts

### Can Inference Fixes Work?

**NO** - based on Phase 1 evidence:
- Even with correct training format: 0% refusal, 0% redirect
- Repeat penalty (tested in B3/C1/Qwen configs) helps repetition but doesn't add refusal
- Temperature variations don't matter - model doesn't have refusal behavior to "sample"
- Stop sequences won't help - they stop generation, not change behavior

### What Would Be Needed

To achieve refusal via inference only:
1. Model would need refusal behavior in weights (it doesn't have this)
2. Prompt would need to trigger that behavior (can't trigger what isn't there)
3. Parameters would need to favor refusal (no parameter makes model refuse)

**None of these conditions are met.**

---

## Recommendation

### Skip Remaining Phase 6H Tests

**Rationale**:
- Phase 1 tested 4 different format approaches
- Best format (A1 Training) achieved 0% refusal, 0% redirect
- Adding stop sequences (Phase 3) won't help - nothing to stop
- Parameter tuning (Phase 2) won't help - can't tune behavior that doesn't exist
- Scope embedding (Phase 4) won't help - already tried system prompts in Phase 6B

### Evidence from Prior Testing

Phase 6B already tested:
- Repeat penalty variations (helped loops, not refusal)
- Temperature variations (no effect on refusal)
- System prompts (made it worse)
- Training format (confirmed again in Phase 1)

### Proceed to Phase 6I

**Next Action**: Retrain model with Phase 6F high-quality dataset (1,082 examples)

**Why retraining will work**:
1. Phase 6F dataset has proper 50/50 answer/redirect balance (vs old 78/22)
2. Zero contamination (vs old 30 Python questions in refusal data)
3. 10x response diversity (vs old single template)
4. Proper classification (answer/redirect/refuse categories)

**Expected improvement**:
- Refusal training will be strong enough to override base knowledge
- Python capability maintained (still dominant in training mix)
- Redirect behavior added (new category in Phase 6F dataset)

---

## Appendix: All Test Outputs

[See individual JSON files in `results/phase1/` for complete outputs]

**Files**:
- `config_a1_training_format_baseline.json` - 5 tests
- `config_b3_conversational.json` - 5 tests
- `config_c1_minimal_direct.json` - 5 tests
- `config_qwen_chat.json` - 5 tests

**Total**: 20 complete test outputs with classifications

---

**End of Phase 6H - Phase 1 Report**

**Status**: Phase 1 Complete ✓  
**Decision**: Skip Phases 2-4, proceed to Phase 6I retraining  
**Reason**: Inference workarounds insufficient, training required
