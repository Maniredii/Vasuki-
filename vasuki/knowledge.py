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

KNOWLEDGE_REGISTRY["list"] = """A **list** in Python is a mutable, ordered, dynamic array of heterogeneous elements.

### Key Characteristics:
- **Mutable:** Elements can be appended, inserted, modified, or removed in-place.
- **Dynamic Array:** Automatically resizes with $O(1)$ amortized append performance.
- **Indexing & Slicing:** Supports negative indices (`nums[-1]`) and sub-array slices (`nums[1:4]`).

```python
numbers = [1, 2, 3]
numbers.append(4)
numbers[0] = 10
print(numbers)  # [10, 2, 3, 4]
```"""

KNOWLEDGE_REGISTRY["dictionary"] = KNOWLEDGE_REGISTRY["dict"] = """A **dictionary** in Python is an associative mapping of unique, hashable keys to arbitrary values.

### Key Characteristics:
- **Average $O(1)$ Operations:** Fast lookup, insertion, and deletion powered by an internal hash table.
- **Insertion-Ordered:** Guarantees key preservation in insertion order (Python 3.7+).
- **Flexible Keys:** Any hashable type (strings, integers, tuples) can be used as keys.

```python
user = {"name": "Alice", "role": "Engineer", "active": True}
user["email"] = "alice@example.com"
print(user.get("role", "Guest"))  # Engineer
```"""

KNOWLEDGE_REGISTRY["set"] = """A **set** in Python is an unordered collection of unique, hashable elements.

### Key Characteristics:
- **Deduplication:** Automatically eliminates duplicate entries upon insertion.
- **$O(1)$ Membership Test:** Extremely fast `x in my_set` membership checks via hashing.
- **Mathematical Operations:** Built-in union (`|`), intersection (`&`), and difference (`-`).

```python
raw_tags = ["python", "ai", "python", "code"]
unique_tags = set(raw_tags)
print(unique_tags)  # {'python', 'ai', 'code'}
```"""

KNOWLEDGE_REGISTRY["generator"] = """A **generator** in Python is a memory-efficient iterator produced by functions containing the `yield` statement.

### Key Characteristics:
- **Lazy Evaluation:** Computes and emits items one-by-one on demand instead of loading everything into memory.
- **$O(1)$ Memory Usage:** Perfect for processing large files or infinite data streams.

```python
def count_up_to(n: int):
    val = 1
    while val <= n:
        yield val
        val += 1

for num in count_up_to(3):
    print(num)  # 1, 2, 3
```"""

KNOWLEDGE_REGISTRY["decorator"] = """A **decorator** in Python is a callable that takes another function as an argument and extends its behavior without modifying its source code.

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        res = func(*args, **kwargs)
        print(f"{func.__name__} executed in {time.time()-t0:.4f}s")
        return res
    return wrapper

@timer
def compute():
    return sum(i * i for i in range(10000))

compute()
```"""
