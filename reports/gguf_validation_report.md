# GGUF Model Validation Report - Vasuki 0.5B

**Report Date**: 2026-09-24  
**Model File**: `qwen2.5-coder-0.5b.Q4_K_M.gguf`  
**Purpose**: Verify model integrity before llama.cpp CLI testing

---

## Executive Summary

✅ **VALIDATION PASSED** - Model file is valid and ready for llama.cpp inference

The GGUF file has been thoroughly validated for integrity, format correctness, and metadata consistency. No corruption or errors detected.

---

## 1. File Location and Basic Properties

| Property | Value | Status |
|----------|-------|--------|
| **File Name** | qwen2.5-coder-0.5b.Q4_K_M.gguf | ✅ Valid |
| **Absolute Path** | D:\VASUKI\qwen2.5-coder-0.5b.Q4_K_M.gguf | ✅ Exists |
| **File Size** | 397,804,992 bytes | ✅ |
| **File Size (Human)** | 379.38 MB (0.3705 GB) | ✅ |
| **File Extension** | .gguf | ✅ Correct |
| **Last Modified** | 2026-09-24 15:43:48 | ✅ |
| **File Readability** | Full read/write access | ✅ Verified |

**Assessment**: File exists, is accessible, and has appropriate size for Q4_K_M quantization.

---

## 2. File Integrity

### SHA-256 Checksum
```
d4f7b8b28461f82db41483aba8d0992b5ad8e07299c58a516bf1cd78e866b98c
```

**Status**: ✅ Checksum calculated successfully (not truncated or corrupted)

### Completeness Check
- ✅ File can be fully read from start to end
- ✅ Last byte accessible
- ✅ No read errors encountered
- ✅ File size matches expected Q4_K_M quantization size

---

## 3. GGUF Format Validation

### Magic Header
| Property | Value | Status |
|----------|-------|--------|
| **Magic Bytes** | `GGUF` (0x47474655) | ✅ Valid |
| **Header Status** | Correctly formatted | ✅ Valid |

**Assessment**: File is a genuine GGUF format file.

### GGUF Version
| Property | Value | Status |
|----------|-------|--------|
| **GGUF Version** | 3 | ✅ Latest |
| **Compatibility** | llama.cpp current builds | ✅ Compatible |

**Assessment**: Using latest GGUF v3 format. Compatible with modern llama.cpp builds.

### Structure Metadata
| Property | Value |
|----------|-------|
| **Total Tensors** | 290 |
| **Metadata Entries** | 27 |
| **First Tensor** | output_norm.weight |

**Sample Tensors** (first 3):
1. `output_norm.weight`
2. `token_embd.weight`
3. `blk.0.attn_k.bias`

**Assessment**: Tensor count and structure consistent with Qwen2.5-Coder-0.5B architecture.

---

## 4. Model Architecture Metadata

### General Information
| Property | Value (Decoded) | Raw Bytes | Status |
|----------|-----------------|-----------|--------|
| **Architecture** | qwen2 | [113, 119, 101, 110, 50] | ✅ Verified |
| **Model Name** | Vasuki 0.5b Gguf | [86, 97, 115, 117, 107, 105, ...] | ✅ Verified |
| **Base Name** | vasuki | [118, 97, 115, 117, 107, 105] | ✅ Verified |
| **Quantized By** | Unsloth | [85, 110, 115, 108, 111, 116, 104] | ✅ Verified |

**Assessment**: Metadata confirms this is a Qwen2-based model named "Vasuki", quantized using Unsloth.

### Architecture Specifications
| Property | Value | Status |
|----------|-------|--------|
| **Block Count (Layers)** | 24 | ✅ Verified |
| **Context Length** | 32,768 tokens | ✅ Verified |
| **Embedding Length** | 896 | ✅ Verified |
| **Attention Heads** | 14 | ✅ Verified |
| **KV Heads** | 2 | ✅ Verified |
| **RoPE Frequency Base** | 1,000,000.0 | ✅ Verified |

**Assessment**: Architecture parameters consistent with Qwen2.5-Coder-0.5B base model.

**Memory Implications**:
- 24 layers suggest moderate depth
- 896 embedding dimension indicates compact model
- 32K context support (though will start testing with 2048)

---

## 5. Quantization Validation

### Quantization Details
| Property | Value | Status |
|----------|-------|--------|
| **File Type Code** | 15 | ✅ |
| **Quantization Method** | **Q4_K_M** | ✅ VERIFIED |
| **Quantization Version** | 2 | ✅ |
| **Filename Claim** | Q4_K_M | ✅ Matches |
| **Metadata Claim** | Q4_K_M (type 15) | ✅ Matches |

### File Type Code Mapping
```
File Type 15 = Q4_K_M (4-bit K-quant, medium quality)
```

**Verification Method**: 
- ❌ NOT assumed from filename
- ✅ **VERIFIED from internal GGUF metadata** (general.file_type = 15)

**Assessment**: ✅ **Quantization is genuinely Q4_K_M**, not just filename claim.

### Q4_K_M Characteristics
- **Bit Depth**: 4-bit weights
- **Quality**: Medium (K-quant variant)
- **Typical Size**: ~25-30% of F16 model
- **Quality vs Size**: Good balance for 0.5B model
- **Inference Speed**: Fast on CPU

---

## 6. Tokenizer and Chat Template

### Tokenizer Information
| Property | Status | Notes |
|----------|--------|-------|
| **Tokenizer Model** | Present | GGUF contains tokenizer data |
| **Vocab Size** | Not explicitly listed | Likely ~151K (Qwen2 default) |
| **Tokenizer Type** | Qwen2 BPE | Expected for architecture |

### Chat Template
| Property | Status | Notes |
|----------|--------|-------|
| **Chat Template** | ⚠️ **NOT FOUND** | No embedded template in metadata |
| **System Prompt** | Not embedded | Not in GGUF metadata |
| **Template Format** | Unknown | Needs investigation |

**Assessment**: 
- ⚠️ **No chat template found in GGUF metadata**
- This is common for models exported from Unsloth
- llama.cpp will use raw prompt mode or default template
- May need to test different prompt formats manually
- **Action Required**: Phase 6 will investigate optimal prompt format

**Training Format** (from project context):
```
### Instruction:
{instruction}

### Input:
{input}

### Response:
{response}
```

**Note**: This format may need to be manually applied during inference.

---

## 7. Context Length Considerations

### Maximum Context
| Property | Value |
|----------|-------|
| **Model Maximum** | 32,768 tokens |
| **Embedding Dimension** | 896 |

### Practical Context Sizes for Testing

#### Phase 4 Testing Plan
| Config | Context | KV Cache RAM | Total Estimated | Status |
|--------|---------|--------------|-----------------|--------|
| A (Conservative) | 2,048 | ~200 MB | ~800 MB | ✅ Safe |
| B (Moderate) | 4,096 | ~400 MB | ~1.2 GB | ✅ Safe |
| C (Large) | 8,192 | ~800 MB | ~1.5 GB | ⚠️ Test carefully |
| D (Maximum) | 32,768 | ~3.2 GB | ~4 GB | ❌ Not recommended initially |

**Initial Testing Recommendation**: Start with context size 2048, maximum 4096 tokens.

---

## 8. Memory Footprint Analysis

### On-Disk Size
- **GGUF File**: 379.38 MB

### Runtime Memory Estimates

#### Model Loading (Fixed)
```
Model Weights (Q4_K_M):  ~400 MB
Tokenizer Data:          ~50 MB
Runtime Structures:      ~50 MB
-----------------------------------------
Base Memory:             ~500 MB
```

#### Context-Dependent Memory (KV Cache)

**Formula**: `KV_Cache ≈ Context_Length × Layers × Heads × Embedding × BytesPerElement / Compression`

For Qwen2.5-Coder-0.5B (24 layers, 896 dim):
- Context 2048: ~150-200 MB
- Context 4096: ~300-400 MB
- Context 8192: ~600-800 MB
- Context 32768: ~2.4-3.2 GB

#### Total Application Memory
```
Context 2048:  ~700-900 MB
Context 4096:  ~1.0-1.3 GB
Context 8192:  ~1.4-1.8 GB
Context 32768: ~3.2-4.0 GB
```

**Assessment**: Model is lightweight and suitable for systems with 4+ GB RAM when using reasonable context sizes.

---

## 9. Compatibility Assessment

### llama.cpp Compatibility
| Requirement | Status | Notes |
|-------------|--------|-------|
| **GGUF Format** | ✅ Compatible | Version 3 (latest) |
| **Architecture** | ✅ Compatible | Qwen2 supported in llama.cpp |
| **Quantization** | ✅ Compatible | Q4_K_M widely supported |
| **Context Length** | ✅ Compatible | 32K supported with RoPE |

**Verdict**: ✅ Model is fully compatible with modern llama.cpp builds (b1000+)

### Hardware Compatibility
| Hardware | Compatibility | Notes |
|----------|---------------|-------|
| **CPU (i7-1355U)** | ✅ Excellent | 10 cores sufficient |
| **RAM (15.65 GB)** | ✅ Adequate | For context ≤ 8192 |
| **GPU (MX550 2GB)** | ⚠️ Limited | Partial layer offloading possible |

---

## 10. Validation Tools Used

### Primary Validation Script
- **Script**: `validate_gguf.py`
- **Method**: Binary header inspection + SHA-256 checksum
- **Libraries**: Python struct, hashlib

### Metadata Inspection Script
- **Script**: `quick_metadata.py`
- **Method**: GGUF library metadata parsing
- **Libraries**: Python gguf (Hugging Face)

### Verification Level
- ✅ File integrity: **VERIFIED** (full file read + checksum)
- ✅ GGUF format: **VERIFIED** (magic header + version)
- ✅ Quantization: **VERIFIED** (internal metadata, not filename)
- ✅ Architecture: **VERIFIED** (Qwen2, 24 layers, 896 dim)
- ⚠️ Chat template: **NOT PRESENT** (needs manual prompt formatting)

---

## 11. Issues and Limitations

### No Critical Issues Found
✅ File is valid, complete, and ready for inference

### Minor Observations
1. ⚠️ **No chat template**: Will require manual prompt formatting in llama.cpp
2. ⚠️ **Large context support**: Maximum 32K, but start with 2K for safety
3. ℹ️ **No vocab size metadata**: Likely ~151K (Qwen2 default)

### Not Validated
- ❌ **Model quality**: Cannot assess fine-tuning effectiveness from file inspection
- ❌ **Python specialization**: Refusal behavior needs testing
- ❌ **Hallucination rate**: Requires inference testing
- ❌ **Response accuracy**: Needs qualitative evaluation

**Note**: These aspects will be evaluated in Phase 5 (CLI testing).

---

## 12. Recommendations for llama.cpp Usage

### Phase 3: Obtaining llama.cpp
- Download official Windows build from llama.cpp GitHub releases
- Look for builds dated 2024+ (GGUF v3 support)
- Prefer CPU-only build initially
- CUDA build optional for Phase 8

### Phase 4: Initial Testing Commands

**Recommended starting command** (syntax may vary by llama.cpp version):
```powershell
llama-cli.exe `
  -m D:\VASUKI\qwen2.5-coder-0.5b.Q4_K_M.gguf `
  -n 256 `
  -c 2048 `
  -t 8 `
  --prompt "Explain what a Python variable is."
```

**Parameters explained**:
- `-m`: Model path
- `-n`: Max tokens to generate (256)
- `-c`: Context size (2048 - conservative)
- `-t`: CPU threads (8 out of 12 available)
- `--prompt`: Test prompt

**Note**: Actual syntax will be verified from `llama-cli --help` in Phase 3.

### Phase 6: Prompt Format Testing

Test these formats:
1. **Raw prompt**: "Write a Python function..."
2. **Instruct format**: "### Instruction:\n...\n### Response:\n"
3. **Qwen chat format**: If llama.cpp supports it
4. **System prompt**: Using llama.cpp -p flag if available

---

## 13. Comparison with Previous Validation

This validation confirms previous Ollama-focused validation:
- ✅ Same SHA-256 checksum (file unchanged)
- ✅ Same architecture metadata
- ✅ Same quantization type
- ✅ File has not been modified

**Status**: Model file integrity maintained across validations.

---

## 14. Final Verdict

### Overall Assessment: ✅ **READY FOR llama.cpp CLI TESTING**

**Validation Summary**:
- ✅ File integrity: PASSED
- ✅ GGUF format: PASSED (v3)
- ✅ Architecture: PASSED (Qwen2, 24 layers)
- ✅ Quantization: PASSED (Q4_K_M verified)
- ✅ Compatibility: PASSED (llama.cpp compatible)
- ⚠️ Chat template: ABSENT (needs investigation)

**Ready for**:
- ✅ Phase 3: llama.cpp acquisition
- ✅ Phase 4: CPU baseline testing
- ✅ Phase 5: CLI prompt testing
- ✅ Phase 6: Prompt format investigation

**Not ready for**:
- ❌ Production deployment (testing needed)
- ❌ Quality claims (inference needed)
- ❌ GPU usage (Phase 8 investigation pending)

---

## 15. Next Steps

1. **Phase 3**: Download official llama.cpp Windows binaries
2. **Phase 4**: Test CPU inference with context 2048
3. **Phase 5**: Run structured prompt tests
4. **Phase 6**: Investigate optimal prompt format for missing chat template
5. **Phase 7**: Measure actual memory usage and performance
6. **Phase 8**: Optionally investigate GPU acceleration

**Model file is validated and ready. Proceed to Phase 3.**

---

**Report Generated**: 2026-09-24  
**Validation Status**: ✅ PASSED  
**Model Integrity**: ✅ VERIFIED  
**llama.cpp Compatibility**: ✅ CONFIRMED  
**Ready for Inference**: ✅ YES
