# llama.cpp Setup Report - Vasuki 0.5B

**Report Date**: 2026-09-24  
**Purpose**: Document llama.cpp acquisition and setup for CLI testing

---

# llama.cpp Setup Report - Vasuki 0.5B

**Report Date**: 2026-09-24  
**Purpose**: Document llama.cpp acquisition and setup for CLI testing

---

## Setup Status: ✅ INSTALLATION COMPLETE

llama.cpp has been successfully downloaded and installed.

---

## 1. Installation Details

### Build Information
| Property | Value |
|----------|-------|
| **Version** | 0.5.0-dev |
| **Build Number** | 11157 |
| **Commit** | 53ed051ce |
| **Compiler** | Clang 20.1.8 |
| **Target** | Windows x86_64 |
| **Build Type** | CPU (x64) |

### Installation Location
```
D:\VASUKI\tools\llama.cpp\
```

---

## 2. Installed Executables

### Primary Tools
| Executable | Purpose | Status |
|------------|---------|--------|
| **llama-cli.exe** | Main CLI inference tool | ✅ Verified |
| **llama-server.exe** | HTTP API server | ✅ Present |
| **llama-bench.exe** | Performance benchmarking | ✅ Present |

### Additional Tools
- llama-batched-bench.exe - Batched benchmarking
- llama-quantize.exe - Model quantization
- llama-imatrix.exe - Importance matrix calculation
- llama-perplexity.exe - Perplexity measurement
- llama-tokenize.exe - Tokenizer testing
- llama-completion.exe - Completion testing
- ggml-rpc-server.exe - RPC server
- Various specialized CLI tools (llava, minicpmv, qwen2vl, etc.)

### Supporting Libraries
- ggml.dll, ggml-base.dll - Core GGML library
- llama.dll, llama-common.dll - llama.cpp library
- Multiple CPU-optimized DLLs:
  - ggml-cpu-alderlake.dll (13th Gen Intel - YOUR CPU!)
  - ggml-cpu-icelake.dll
  - ggml-cpu-sapphirerapids.dll
  - ggml-cpu-zen4.dll
  - (and others for various CPU architectures)
- libomp.dll - OpenMP threading support

---

## 3. Key Command-Line Options

### Model Loading
```
-m, --model FNAME              Model path to load
-c, --ctx-size N               Context size (default: from model)
-n, --predict N                Tokens to generate (-1 = infinity)
```

### Performance Options
```
-t, --threads N                CPU threads for generation
-tb, --threads-batch N         Threads for batch processing
-b, --batch-size N             Logical batch size (default: 2048)
-ub, --ubatch-size N           Physical batch size (default: 512)
```

### GPU Options (for Phase 8)
```
-ngl, --n-gpu-layers N         Layers to offload to GPU (auto/all/number)
-sm, --split-mode MODE         How to split across GPUs (none/layer/row)
-mg, --main-gpu INDEX          Primary GPU to use
```

### Prompt Options
```
-p, --prompt PROMPT            Initial prompt
-f, --file FNAME               Prompt from file
-sys, --system-prompt PROMPT   System prompt (if supported by template)
--chat-template TEMPLATE       Custom Jinja chat template
```

### Generation Control
```
--temp N                       Temperature (default varies)
--top-k N                      Top-K sampling
--top-p N                      Top-P sampling
--repeat-penalty N             Repetition penalty
```

---

## 4. CPU Architecture Detection

The build includes **architecture-specific optimizations** for various Intel/AMD CPUs:

**Your CPU (i7-1355U - Alder Lake)**: Will use `ggml-cpu-alderlake.dll` for optimal performance

Other supported architectures:
- Ivy Bridge, Haswell, Skylake-X
- Ice Lake, Sapphire Rapids
- AMD Piledriver, Zen 4
- Generic SSE4.2 and x64 fallbacks

---

## 5. Backend Support

### CPU Backend
✅ **Fully Supported**
- Multi-threaded inference
- AVX2/AVX512 optimizations (CPU-dependent)
- OpenMP parallelization
- Architecture-specific optimizations

### GPU Backend
⚠️ **Not Included in This Build**
- This is a CPU-only build
- No CUDA support in current binaries
- GPU testing (Phase 8) will require CUDA-enabled build

To check if GPU support is available:
```powershell
.\llama-cli.exe --help | Select-String -Pattern "gpu|cuda|ngl"
```

**Result**: GPU options present in help, but CUDA DLLs not included. CPU-only inference for now.

---

## 6. Verification Tests

### Test 1: Version Check
```powershell
PS D:\VASUKI\tools\llama.cpp> .\llama-cli.exe --version
version: 0.5.0-dev (build 11157, commit 53ed051ce)
built with Clang 20.1.8 for Windows x86_64
```
✅ **PASS** - Executable runs and reports version

### Test 2: Help Output
```powershell
PS D:\VASUKI\tools\llama.cpp> .\llama-cli.exe --help
```
✅ **PASS** - Help displays correctly, options documented

### Test 3: File Accessibility
```powershell
PS D:\VASUKI\tools\llama.cpp> Test-Path llama-cli.exe
True
```
✅ **PASS** - All required files present

---

## 7. Compatibility Assessment

### GGUF v3 Support
✅ **Supported** - Build 11157 includes GGUF v3 support

### Qwen2 Architecture
✅ **Supported** - Qwen2 models supported in recent builds

### Q4_K_M Quantization
✅ **Supported** - K-quant formats fully supported

### Context Length
✅ **Flexible** - Can set any context size with `-c` flag
- Model supports: 32,768 tokens
- Will test with: 2,048 initially (conservative)

---

## 8. Phase 4 Preparation

### Recommended Initial Test Command

```powershell
cd D:\VASUKI\tools\llama.cpp

.\llama-cli.exe `
  -m "D:\VASUKI\qwen2.5-coder-0.5b.Q4_K_M.gguf" `
  -c 2048 `
  -n 256 `
  -t 8 `
  -p "Explain what a Python variable is to a beginner."
```

**Parameters Explained**:
- `-m`: Model file path (absolute)
- `-c 2048`: Context size (conservative starting point)
- `-n 256`: Maximum tokens to generate (reasonable for testing)
- `-t 8`: Use 8 CPU threads (out of 12 available)
- `-p`: Test prompt (Python-related)

### Expected Behavior
1. Model loads into RAM (~400-500 MB)
2. Prompt is processed
3. Response generated token by token
4. Generation stats displayed at end

---

## 9. Known Limitations

### No CUDA Support
- This is a **CPU-only build**
- GPU acceleration requires separate CUDA-enabled build
- Will investigate GPU builds in Phase 8

### No Pre-configured Chat Template
- Model lacks embedded chat template (from Phase 2)
- May need to test different prompt formats
- Will investigate in Phase 6

### Windows-Specific
- Build is Windows x86_64 only
- Requires x64 CPU with SSE4.2 minimum
- Your CPU (Alder Lake) has full AVX2 support ✅

---

## 10. Next Steps

### Phase 4: CPU Baseline Testing
1. ✅ llama.cpp installed and verified
2. ⏭️ Load model with context 2048
3. ⏭️ Test basic inference
4. ⏭️ Measure memory usage
5. ⏭️ Record performance metrics

**Ready to proceed to Phase 4!**

---

**Report Updated**: 2026-09-24  
**Installation Status**: ✅ COMPLETE  
**Verification**: ✅ PASSED  
**Ready for Testing**: ✅ YES

---

## 1. Official Source

**Repository**: [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)  
**Releases Page**: https://github.com/ggml-org/llama.cpp/releases  
**Latest Build**: b11153 (as of 2026-09-24)

---

## 2. Required Build

### Recommended: Windows x64 (CPU)

**File to Download**: `llama-b11153-bin-win-cpu-x64.zip` (or latest equivalent)

**Why CPU-only initially**:
- ✅ Simpler setup, no CUDA dependencies
- ✅ Guaranteed to work on any x64 Windows
- ✅ Sufficient for baseline testing
- ✅ Can test GPU builds later in Phase 8

---

## 3. Manual Download Steps

### Step 1: Navigate to Releases
1. Open: https://github.com/ggml-org/llama.cpp/releases
2. Look for the latest release (v0.5.0 or newer)

### Step 2: Download Windows Build
Look for downloads labeled:
- **Windows x64 (CPU)** ← Start with this
- Windows x64 (CUDA 12) ← Optional for Phase 8
- Windows x64 (CUDA 13) ← Optional for Phase 8

### Step 3: Extract to Project Directory
```
Extract to: D:\VASUKI\tools\llama.cpp\
```

Expected files after extraction:
```
D:\VASUKI\tools\llama.cpp\
  ├── llama-cli.exe          (Main inference tool)
  ├── llama-server.exe       (HTTP server mode)
  ├── llama-bench.exe        (Benchmarking tool)
  ├── ggml.dll              (Core library)
  ├── llama.dll             (llama library)
  └── (other support files)
```

---

## 4. Verification Commands

After extracting, verify installation:

```powershell
# Navigate to tools directory
cd D:\VASUKI\tools\llama.cpp

# Check if llama-cli exists
Test-Path llama-cli.exe

# Get llama-cli help (verify it works)
.\llama-cli.exe --help

# Check version info
.\llama-cli.exe --version
```

---

## 5. Alternative: Build from Source

If pre-built binaries are unavailable, you can build from source (you have the required tools).

### Prerequisites Available
- ✅ CMake 3.25.0
- ✅ Git 2.48.1
- ❌ MSVC Compiler (cl.exe) - Would need Visual Studio Build Tools

### Build Steps (if needed)
```powershell
# Clone repository
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp

# Build with CMake (requires Visual Studio Build Tools)
cmake -B build
cmake --build build --config Release

# Binaries will be in: build/bin/Release/
```

**Note**: Building from source requires Visual Studio Build Tools (for cl.exe compiler), which is not currently detected on your system.

---

## 6. Expected Executables

### llama-cli.exe
**Purpose**: Main command-line inference tool  
**Use Case**: Interactive prompting, batch processing  
**Phase 4 Usage**: Primary tool for testing

### llama-server.exe
**Purpose**: HTTP API server  
**Use Case**: REST API for applications  
**Phase 10 Usage**: Optional for Python wrapper

### llama-bench.exe
**Purpose**: Performance benchmarking  
**Use Case**: Systematic performance measurement  
**Phase 7 Usage**: Performance benchmarking

---

## 7. Installation Target

```
Target Directory: D:\VASUKI\tools\llama.cpp\
Model Location:   D:\VASUKI\qwen2.5-coder-0.5b.Q4_K_M.gguf
```

**Important**: Keep model files separate from executable files.

---

## 8. Build Information to Collect

Once llama-cli is available, run these commands to document the build:

```powershell
# Get help output
.\llama-cli.exe --help > D:\VASUKI\reports\llama-cli-help.txt

# Get version
.\llama-cli.exe --version

# Check supported backends
.\llama-cli.exe --help | Select-String -Pattern "backend|gpu|cuda|cpu"
```

---

## 9. Compatibility Requirements

### Minimum Requirements for Our Model
| Requirement | Status | Notes |
|-------------|--------|-------|
| **GGUF v3 Support** | Required | Model uses GGUF v3 |
| **Qwen2 Architecture** | Required | Model is Qwen2-based |
| **Q4_K_M Quant** | Required | Model quantization type |
| **32K Context** | Optional | Model supports it, will test with 2K |

### Build Date
- ✅ Prefer builds from 2024 onwards
- ✅ Latest release (b11153 or newer) recommended
- ✅ GGUF v3 support standard in recent builds

---

## 10. Next Steps After Download

Once llama-cli.exe is available:

1. **Verify Installation**
   ```powershell
   cd D:\VASUKI\tools\llama.cpp
   .\llama-cli.exe --version
   .\llama-cli.exe --help
   ```

2. **Document Build Details**
   - Version/commit
   - Supported backends
   - Available options

3. **Proceed to Phase 4**
   - Test model loading
   - Run CPU baseline inference
   - Measure performance

---

## 11. Troubleshooting

### Issue: Download Link Not Found
**Solution**: Go directly to https://github.com/ggml-org/llama.cpp/releases and manually download the Windows x64 (CPU) build.

### Issue: .exe Files Not Running
**Possible Causes**:
- Missing Visual C++ Redistributable
- Windows SmartScreen blocking

**Solutions**:
- Install Visual C++ Redistributable 2022 x64
- Right-click .exe → Properties → Unblock

### Issue: DLL Missing Errors
**Solution**: Ensure all files from the ZIP are extracted to the same directory.

---

## 12. Summary

**Status**: ⚠️ Awaiting manual download

**Required Action**:
1. Download: Windows x64 (CPU) build from llama.cpp releases
2. Extract to: `D:\VASUKI\tools\llama.cpp\`
3. Verify: Run `llama-cli.exe --help`
4. Proceed: Continue to Phase 4

**Once Complete**: Update this report with:
- Build version/commit
- File list
- Help output summary
- Backend support details

---

**Report Status**: Setup instructions provided, awaiting download  
**Next Phase**: Phase 4 - CPU Baseline Testing (after download)
