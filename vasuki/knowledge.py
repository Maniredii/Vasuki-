"""
VASUKI Instant Knowledge & Conceptual Verification Engine.
Provides instant, accurate technical explanations and code examples for Python concepts.
"""
import re

KNOWLEDGE_REGISTRY = {}

def normalize_concept_query(query: str) -> str:
    """Normalizes natural language questions to concept keys."""
    q = query.lower().strip()
    q = re.sub(r"^(what is|what are|explain|describe|tell me about|define)\s+(a\s+|an\s+|the\s+)?", "", q)
    q = re.sub(r"\s+(in python|in py|with examples?|please|for beginners).*$", "", q)
    return q.strip(" ?.!:\'\"")

KNOWLEDGE_REGISTRY["python"] = """Python is a high-level, interpreted, general-purpose programming language created by Guido van Rossum.

### Key Characteristics:
- **Clean & Readable:** Enforces whitespace indentation for clear, maintainable code structure.
- **Multi-Paradigm:** Supports Object-Oriented, Functional, Procedural, and Imperative programming.
- **Batteries-Included:** Rich standard library covering I/O, networking, regular expressions, and concurrency.
- **Industry Standard:** Dominant language for AI/ML (PyTorch, TensorFlow), Data Science (Pandas, NumPy), and Web APIs (FastAPI, Django).

```python
def greet(developer: str) -> str:
    return f"Welcome to Python, {developer}!"

print(greet("Engineer"))
```"""

KNOWLEDGE_REGISTRY["tuple"] = """A **tuple** in Python is an ordered, immutable collection of elements.

### Key Characteristics:
- **Immutable:** Once created, items cannot be added, removed, or modified.
- **Ordered:** Maintains exact insertion order accessible via zero-indexed subscripting (`t[0]`).
- **Heterogeneous:** Can store elements of multiple different types (`(1, "apple", 3.14)`).
- **Hashable:** Can be used as dictionary keys and stored in sets (if all contained items are hashable).
- **Memory Efficient:** Uses less memory and provides faster allocation than mutable lists.

```python
# Tuple creation & unpacking
coordinates = (10, 20)
x, y = coordinates

# Accessing elements
print(f"X: {x}, Y: {y}")  # X: 10, Y: 20
```"""
