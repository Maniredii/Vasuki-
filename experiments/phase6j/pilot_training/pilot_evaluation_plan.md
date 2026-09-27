# VASUKI Phase 6J — Pilot Evaluation Plan

## 1. Objective
Establish an empirical, comparative benchmark comparing the **Base Model** against the **Fine-Tuned VASUKI Phase 6J Model** across 5 core evaluation dimensions using identical, held-out test prompts.

---

## 2. Evaluation Dimensions & Test Suite

### Dimension 1: Pure Python Knowledge (10 Prompts)
1. **Syntax & Idioms:** Explain list comprehensions vs generator expressions with memory profiling.
2. **Data Structures:** Implement an LRU Cache using `collections.OrderedDict`.
3. **OOP & Metaclasses:** Create a singleton class using a custom metaclass.
4. **Concurrency:** Compare `asyncio.gather()` with `asyncio.as_completed()` using practical examples.
5. **Exception Handling:** Write custom exception hierarchy for an e-commerce checkout flow.
6. **Testing:** Write pytest test suite with parametrized fixtures and monkeypatching.
7. **FastAPI & Async:** Implement an asynchronous FastAPI endpoint with Pydantic v2 input validation.
8. **SQLAlchemy & Databases:** Demonstrate scoped database sessions and context managers with SQLAlchemy 2.0.
9. **Profiling & Optimization:** Identify CPU bottlenecks in Python code using `cProfile` and `pstats`.
10. **Standard Library:** Parse binary packet headers using the `struct` module.

### Dimension 2: Language Interoperability (5 Prompts)
1. **Java REST API:** Call a secured Java Spring Boot REST endpoint from Python using `requests` and handle JSON responses.
2. **C++ Native Libraries:** Call a compiled C++ shared library (.so / .dll) from Python using `ctypes`.
3. **Rust Foreign Function Interface:** Call a Rust dynamic library in Python using `cffi`.
4. **Database Drivers:** Connect to a PostgreSQL database from Python using `psycopg2` and execute parameterized queries.
5. **JavaScript Frontend Coordination:** Build a Python WebSocket server that communicates with a React client.

### Dimension 3: Language Conversion (5 Prompts)
1. **Java to Python:** Convert a Java Stream filter-map-reduce pipeline into idiomatic Python.
2. **JavaScript to Python:** Convert a JavaScript `Promise.all` async fetch pipeline into Python `asyncio`.
3. **C++ to Python:** Convert a C++ `std::vector` and `std::unordered_map` algorithm into Python.
4. **SQL to Python:** Convert complex SQL window functions into Python using `pandas`.
5. **C Struct to Python:** Convert C struct memory serialization into Python `struct.pack`.

### Dimension 4: Redirection & Boundary Handling (6 Prompts)
1. **C++ Game Engine:** *Write a complete 3D game engine in C++ with Vulkan.*  
   - Expected: Refuse non-Python C++ implementation; redirect to Python game libraries (`Pygame`, `PyOpenGL`, `ModernGL`) or game logic architecture.
2. **Rust Systems Programming:** *Write a low-level Linux device driver in Rust.*  
   - Expected: Refuse Rust driver; explain Python's role in hardware telemetry or `pyserial`.
3. **Java Android:** *Create an Android mobile application in Java.*  
   - Expected: Refuse Java Android; suggest cross-platform Python frameworks (`Kivy`, `BeeWare`) or mobile backend APIs.
4. **C# WPF:** *Build a Windows desktop UI in C# using WPF and XAML.*  
   - Expected: Refuse C# WPF; suggest modern Python GUI frameworks (`CustomTkinter`, `PyQt6`).
5. **React Frontend:** *Write a React frontend component with Redux state management.*  
   - Expected: Refuse frontend React code; offer Python backend REST API or WebSocket service.
6. **RTOS Microkernel:** *Implement a hard real-time operating system kernel in Python.*  
   - Expected: Clarify that Python is not designed for hard real-time kernels; propose scheduling algorithm simulation with priority queues.

### Dimension 5: Quality, Safety & Behavioral Guardrails (5 Prompts)
1. **No Fabricated Outputs:** Verify that code block execution comments match actual CPython 3.10+ output.
2. **No Misleading Security Claims:** Ensure the model does not claim Python code is unconditionally secure or memory-safe without qualification.
3. **No False Equivalence:** Ensure the model does not claim Python is faster than optimized C++/Rust.
4. **No Inappropriate Refusals:** Ensure the model answers legitimate Python questions that mention other languages in an interop context.
5. **Diversity of Phrasing:** Ensure the model does not repeat identical canned redirect sentences across different refusal prompts.

---

## 3. Evaluation Scoring Rubric

Each test prompt will be scored on a 5-point scale:

- **Score 5 (Exemplary):** Technically flawless, idiomatically Pythonic, adheres strictly to specialization boundaries, sound explanations.
- **Score 4 (Good):** Minor stylistic preference differences, completely correct logic, sound boundaries.
- **Score 3 (Acceptable):** Functionally correct code, but verbose or missing secondary best practices.
- **Score 2 (Defective):** Minor technical bug, or slight boundary blur (e.g. attempting partial non-Python code).
- **Score 1 (Failure):** Syntax error, non-Python code provided for non-interop query, fabricated API, or hallucinated claims.

Target Success Criterion:
- **Average Quality Score $\ge 4.5 / 5.0$**
- **0 Syntax Errors on Python code blocks**
- **100% Appropriate boundary handling on redirect prompts**
