# Phase 6I: Pre-Training Dataset Verification Report

**Date**: 2026-09-23
**Dataset**: training_clean.jsonl
**Total Records**: 1073

---

## 1. Basic Validation

- **Required fields**: ✅ PASS
- **Valid JSONL syntax**: ✅ PASS
- **Total records**: 1073

## 2. Behavior Distribution

| Behavior Type | Count | Percentage |
|---------------|-------|------------|
| redirect | 524 | 48.8% |
| answer | 545 | 50.8% |
| refuse | 4 | 0.4% |

**Answer/Redirect Ratio**: 1.04:1

## 3. Duplicate Analysis

- **Total instructions**: 1073
- **Unique instructions**: 144
- **Duplicates**: 74

### Duplicate Instructions

- "Write a complete Rust systems programming application." appears 13 times
- "Write a complete Rust high-performance parser." appears 21 times
- "Write a complete C++ high-performance trading system." appears 13 times
- "Write a complete Java banking application with Spring Boot." appears 10 times
- "Write a complete Go microservices application." appears 17 times
- "Write a complete C++ memory-efficient data structure library." appears 9 times
- "Write a complete Java e-commerce platform using Spring MVC." appears 12 times
- "Write a complete JavaScript Vue.js dashboard application." appears 12 times
- "Write a complete C++ 3D graphics renderer." appears 9 times
- "Write a complete Java enterprise REST API with Java EE." appears 11 times

## 4. Response Diversity

- **Total outputs**: 1073
- **Unique outputs**: 62
- **Uniqueness rate**: 5.8%

## 5. Contamination Checks

- **Training/eval overlap**: 0 ✅
- **Old refusal contamination**: 0 ✅

## 6. Python Labeling Check

- **Python in redirect/refuse**: 0 potential issues

## 7. Sequence Length Analysis

- **Min tokens**: 38
- **Avg tokens**: 64
- **Median tokens**: 59
- **Max tokens**: 140
- **P95 tokens**: 90
- **Over 2048 tokens**: 0 (0.0%)

## 8. Category Breakdown

| Category | Count | Percentage |
|----------|-------|------------|
| direct_non_python | 367 | 34.2% |
| direct_non_python_debug | 105 | 9.8% |
| non_programming | 4 | 0.4% |
| non_python_framework | 52 | 4.8% |
| python_comparison | 224 | 20.9% |
| python_conversion | 11 | 1.0% |
| python_interoperability | 299 | 27.9% |
| python_programming | 11 | 1.0% |

## 9. Final Verification Status

- **Errors**: 0
- **Warnings**: 1

**STATUS**: ⚠️ VERIFIED WITH WARNINGS - REVIEW BEFORE TRAINING

---

**End of Pre-Training Verification Report**
