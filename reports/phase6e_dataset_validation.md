# Phase 6E Dataset Validation Report

**Date**: 2026-09-23

**Dataset**: datasets\phase6e\generated\training_candidate.jsonl

---

## Summary

- **Total Records**: 1082
- **Issues Found**: 0
- **Warnings**: 1
- **Unique Instructions**: 153

## Category Distribution

- direct_non_python: 367 (33.9%)
- python_interoperability: 300 (27.7%)
- python_comparison: 225 (20.8%)
- direct_non_python_debug: 105 (9.7%)
- non_python_framework: 52 (4.8%)
- python_programming: 12 (1.1%)
- python_conversion: 11 (1.0%)
- non_programming: 10 (0.9%)

## Expected Behavior Distribution

- answer: 548 (50.6%)
- redirect: 524 (48.4%)
- refuse: 10 (0.9%)

## Warnings

- **duplicate_instructions**: {'type': 'duplicate_instructions', 'count': 74, 'examples': [('Write a complete Rust systems programming application.', 13), ('Write a complete Rust high-performance parser.', 21), ('Write a complete C++ high-performance trading system.', 13), ('Write a complete Java banking application with Spring Boot.', 10), ('Write a complete Go microservices application.', 17), ('Write a complete C++ memory-efficient data structure library.', 9), ('Write a complete Java e-commerce platform using Spring MVC.', 12), ('Write a complete JavaScript Vue.js dashboard application.', 12), ('Write a complete C++ 3D graphics renderer.', 9), ('Write a complete Java enterprise REST API with Java EE.', 11)]}

