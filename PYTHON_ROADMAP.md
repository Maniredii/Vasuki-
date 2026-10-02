# 🗺️ VASUKI Complete Python Roadmap: From Basics to Advanced

> Engineered for developers, computer science students, and AI/Systems engineers mastering Python from first principles to high-performance edge engineering.

---

## 📌 Roadmap Overview

```
[Phase 1: Python Fundamentals]
          │
          ▼
[Phase 2: Object-Oriented & Idiomatic Python]
          │
          ▼
[Phase 3: Data Structures & Algorithmic Reasoning]
          │
          ▼
[Phase 4: Concurrency, Systems & Performance]
          │
          ▼
[Phase 5: Specialization Tracks (AI / Backend / Edge)]
```

---

## 🟢 Phase 1: Python Fundamentals (Beginner)
*Goal: Master core syntax, data types, control flow, and clean code hygiene.*

* **Core Syntax & Primitives:**
  * Variables, dynamic typing, type hints (`int`, `str`, `float`, `bool`).
  * Arithmetic, logical, bitwise, and comparison operators.
  * Modern string formatting with f-strings (`f"{val:.2f}"`, `f"{num:,}"`, self-documenting `f"{x=}"`).
* **Control Flow & Logic:**
  * `if / elif / else` branching.
  * Loops: `for` loops with `range()`, `enumerate()`, and `zip()`.
  * `while` loops, loop control with `break` and `continue`.
  * The Pythonic `else` clause on `for` and `while` loops (executes only when no `break` occurred).
* **Built-in Collections:**
  * **Lists:** Dynamic arrays, indexing, negative indexing, slicing `[start:stop:step]`, list methods (`append`, `extend`, `pop`, `insert`).
  * **Tuples:** Immutability, tuple packing and unpacking (`a, b = b, a`).
  * **Dictionaries:** Key-value mappings, hashing rules (keys must be hashable), `.get()`, `.items()`, `.keys()`, `.values()`, `defaultdict`.
  * **Sets:** Unique elements, mathematical set operations (union `|`, intersection `&`, difference `-`), $O(1)$ membership checks.
* **Modular Code & Functions:**
  * Defining functions with `def`, positional arguments, default arguments (the mutable default argument trap and sentinel `None`).
  * Arbitrary arguments: `*args` and `**kwargs`.
  * Variable scope: The LEGB rule (Local $\rightarrow$ Enclosing $\rightarrow$ Global $\rightarrow$ Built-in).
* **File I/O & Exception Handling:**
  * Context managers: `with open("file.txt", "r") as f:`.
  * Robust error handling: `try / except / else / finally`.
  * Raising exceptions with `raise ValueError(...)` and chaining with `raise from`.

---

## 🟡 Phase 2: Object-Oriented & Idiomatic Python (Intermediate)
*Goal: Write modular, maintainable, object-oriented, and memory-efficient Python code.*

* **Object-Oriented Programming (OOP):**
  * Classes, instances, `self`, constructors (`__init__`), instance variables vs. class variables.
  * Encapsulation and private name mangling (`_single_leading` vs `__double_leading`).
  * Inheritance, method overriding, and `super()`.
  * Polymorphism, Duck Typing (*"If it walks like a duck and quacks like a duck, it's a duck"*), and Abstract Base Classes (`abc.ABC`, `@abstractmethod`).
* **Dunder / Magic Methods:**
  * Representation: `__repr__` (unambiguous, for developers) vs `__str__` (readable, for users).
  * Containers: `__len__`, `__getitem__`, `__setitem__`, `__contains__`.
  * Operator Overloading: `__add__`, `__eq__`, `__lt__`, `__hash__`.
  * Custom Context Managers: `__enter__` and `__exit__`.
* **Functional & Idiomatic Constructs:**
  * Comprehensions: List, Dictionary, and Set comprehensions with filtering.
  * First-class functions, anonymous `lambda` functions, `map()`, `filter()`.
  * Standard library utilities: `itertools` (`chain`, `islice`, `permutations`, `combinations`) and `functools` (`lru_cache`, `partial`, `reduce`).
* **Iterators & Generators:**
  * The Iteration Protocol: `__iter__` and `__next__`, `StopIteration`.
  * Generators with `yield`: State suspension, memory streaming for unbounded datasets.
  * Generator expressions: `sum(x for x in data)` ($O(1)$ memory vs $O(N)$ list allocation).
* **Decorators:**
  * Closures and lexical scoping.
  * Function decorators, chaining decorators.
  * Decorators accepting arguments and preserving metadata with `@functools.wraps`.
  * Built-in decorators: `@property`, `@classmethod`, `@staticmethod`.

---

## 🟠 Phase 3: Data Structures & Algorithmic Reasoning (Advanced Core)
*Goal: Build algorithmic intuition, master time/space complexity, and solve complex problem patterns.*

* **Linear Data Structures:**
  * Singly and Doubly Linked Lists (Node references, reverse in groups, cycle detection with Floyd's Tortoise and Hare).
