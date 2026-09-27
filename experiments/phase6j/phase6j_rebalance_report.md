# VASUKI Phase 6J — Dataset Rebalance Report

## Overview
This rebalancing pass resolves the **over-redirect bias** where the 0.5B model hallucinated redirect responses on pure Python queries.

### Summary Metrics
| Metric | Original Candidate | Rebalanced Dataset | Improvement |
|---|---|---|---|
| **Total Records** | 593 | **470** | Optimized composition |
| **Python Answering** | 360 (60.7%) | **418 (88.9%)** | **+26.2% Python dominance** |
| **Redirect Examples** | 233 (39.3%) | **52 (11.1%)** | **Balanced boundary control** |
| **Target Languages** | Skewed (81 Java) | Stratified (10 per major lang) | Even domain coverage |
| **Validation Overlap** | 0 records | **0 records (100% held-out)** | Verified |

### Dataset SHA-256 (POSIX LF):
`9cf5e54dce6c6f75930c0297d273c92655ab2222f51635842f8f0fdf436acd3c`
