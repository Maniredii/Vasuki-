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
KNOWLEDGE_REGISTRY["function"] = KNOWLEDGE_REGISTRY["functions"] = """A **function** in Python is a reusable block of code that executes when invoked, optionally accepting parameters and returning a result.

### Key Characteristics:
- **Definition:** Defined with the `def` keyword.
- **First-Class Objects:** Functions can be passed as arguments, assigned to variables, and returned from other functions.
- **Parameters:** Supports positional, keyword, default values, `*args`, and `**kwargs`.
- **Return Value:** Returns values via `return` (returns `None` by default if omitted).

```python
def calculate_total(price: float, tax_rate: float = 0.08) -> float:
    """Calculates final price including sales tax."""
    return price * (1 + tax_rate)

print(calculate_total(100.0))  # 108.0
```"""


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

KNOWLEDGE_REGISTRY["difference between list and tuple"] = KNOWLEDGE_REGISTRY["list vs tuple"] = """### Comparison: Python List vs Tuple

| Feature | `list` | `tuple` |
| :--- | :--- | :--- |
| **Mutability** | Mutable (can change elements) | Immutable (read-only after creation) |
| **Syntax** | Square brackets `[1, 2, 3]` | Parentheses `(1, 2, 3)` |
| **Memory** | Larger (overallocated buffer) | Smaller (compact fixed struct) |
| **Speed** | Slightly slower iteration | Faster allocation and traversal |
| **Dictionary Key** | Cannot be used as key (unhashable) | Can be used as key (if items are hashable) |

```python
# List (Mutable)
my_list = [1, 2, 3]
my_list.append(4)

# Tuple (Immutable)
my_tuple = (1, 2, 3)
# my_tuple.append(4)  # Raises AttributeError
```"""

def resolve_knowledge(query: str):
    """Returns verified concept explanation if query matches knowledge base, else None."""
    norm = normalize_concept_query(query)
    if norm in KNOWLEDGE_REGISTRY:
        return KNOWLEDGE_REGISTRY[norm]
    # Check partial / keyword matches
    for key, val in KNOWLEDGE_REGISTRY.items():
        if key == norm or norm.startswith(key + " ") or norm.endswith(" " + key):
            return val
    return None

KNOWLEDGE_REGISTRY["oops"] = KNOWLEDGE_REGISTRY["oop"] = KNOWLEDGE_REGISTRY["object oriented programming"] = """**Object-Oriented Programming (OOP)** in Python is a paradigm centered around **classes** (blueprints) and **objects** (instances of classes) combining state (attributes) and behavior (methods).

### The Four Core Pillars of OOP:
1. **Encapsulation:** Bundles data and methods together and protects internal state using access conventions (e.g. `_protected`, `__private`).
2. **Inheritance:** Allows a child class to inherit attributes and methods from a parent class (`class Child(Parent):`).
3. **Polymorphism:** Enables different classes to implement methods with the same name, providing interchangeable interfaces (duck typing).
4. **Abstraction:** Hides complex implementation details, exposing only clean public interfaces using Abstract Base Classes (`abc.ABC`).

```python
class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError

class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says Woof!"

dog = Dog("Buddy")
print(dog.speak())  # Buddy says Woof!
```"""

KNOWLEDGE_REGISTRY["class"] = KNOWLEDGE_REGISTRY["classes"] = KNOWLEDGE_REGISTRY["object"] = KNOWLEDGE_REGISTRY["objects"] = """A **class** in Python is a blueprint for creating objects, defining attributes (state) and methods (behavior). An **object** is a concrete instance of a class.

```python
class Car:
    # Class attribute (shared by all instances)
    wheels = 4

    def __init__(self, make: str, model: str):
        # Instance attributes
        self.make = make
        self.model = model

    def display(self) -> str:
        return f"{self.make} {self.model} ({self.wheels} wheels)"

my_car = Car("Tesla", "Model 3")
print(my_car.display())  # Tesla Model 3 (4 wheels)
```"""

KNOWLEDGE_REGISTRY["inheritance"] = """**Inheritance** allows a class (child/subclass) to inherit attributes and methods from another class (parent/superclass), promoting code reuse.

```python
class Vehicle:
    def __init__(self, brand: str):
        self.brand = brand

    def start(self) -> str:
        return f"{self.brand} vehicle started."

class ElectricCar(Vehicle):
    def start(self) -> str:
        # Extend parent method using super()
        parent_msg = super().start()
        return f"{parent_msg} Silent electric motor engaged."

car = ElectricCar("Tesla")
print(car.start())
```"""

KNOWLEDGE_REGISTRY["polymorphism"] = """**Polymorphism** allows entities of different types to be treated through the same interface. In Python, this is achieved through **Duck Typing** ("If it walks like a duck and quacks like a duck, it is a duck").

```python
class AudioBook:
    def read(self):
        return "Playing audio recording..."

class PaperBook:
    def read(self):
        return "Reading physical printed pages..."

def consume_media(media_item):
    print(media_item.read())

consume_media(AudioBook())
consume_media(PaperBook())
```"""

KNOWLEDGE_REGISTRY["encapsulation"] = """**Encapsulation** binds data and methods together within a class and restricts direct modification of internal state.

### Python Access Conventions:
- **Public:** `self.name` (accessible everywhere)
- **Protected:** `self._balance` (internal convention)
- **Private:** `self.__secret` (name-mangled to `_ClassName__secret`)

```python
class BankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.__balance = balance  # Private

    def deposit(self, amount: float):
        if amount > 0:
            self.__balance += amount

    def get_balance(self) -> float:
        return self.__balance

acc = BankAccount("Alice", 500.0)
acc.deposit(150.0)
print(acc.get_balance())  # 650.0
```"""

KNOWLEDGE_REGISTRY["abstraction"] = """**Abstraction** hides internal complexity and requires subclasses to provide concrete implementations for abstract interfaces using Python's `abc` module.

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class StripeGateway(PaymentGateway):
    def process_payment(self, amount: float) -> bool:
        print(f"Charged ${amount} via Stripe API.")
        return True

client = StripeGateway()
client.process_payment(99.0)
```"""

KNOWLEDGE_REGISTRY["lambda"] = KNOWLEDGE_REGISTRY["lambda function"] = KNOWLEDGE_REGISTRY["anonymous function"] = """A **lambda function** in Python is a small, anonymous function restricted to a single expression.

```python
# Syntax: lambda arguments: expression
square = lambda x: x * x
print(square(5))  # 25

# Commonly used with sorted(), map(), and filter()
users = [("Alice", 25), ("Bob", 20), ("Charlie", 30)]
sorted_by_age = sorted(users, key=lambda user: user[1])
print(sorted_by_age)  # [('Bob', 20), ('Alice', 25), ('Charlie', 30)]
```"""

KNOWLEDGE_REGISTRY["list comprehension"] = KNOWLEDGE_REGISTRY["comprehension"] = """**List comprehension** provides a concise, idiomatic syntax for transforming, filtering, and creating new lists in Python.

```python
# Syntax: [expression for item in iterable if condition]
numbers = [1, 2, 3, 4, 5, 6]
even_squares = [x * x for x in numbers if x % 2 == 0]
print(even_squares)  # [4, 16, 36]

# Dictionary comprehension
word_lengths = {w: len(w) for w in ["python", "ai", "code"]}
print(word_lengths)  # {'python': 6, 'ai': 2, 'code': 4}
```"""

KNOWLEDGE_REGISTRY["exception handling"] = KNOWLEDGE_REGISTRY["exceptions"] = KNOWLEDGE_REGISTRY["try except"] = """**Exception handling** in Python catches runtime errors gracefully using `try`, `except`, `else`, and `finally` blocks.

```python
try:
    value = int("42")
    result = 100 / value
except ValueError:
    print("Invalid number format.")
except ZeroDivisionError:
    print("Cannot divide by zero.")
else:
    print(f"Calculation succeeded: {result}")
finally:
    print("Execution complete (runs unconditionally).")
```"""

KNOWLEDGE_REGISTRY["file handling"] = KNOWLEDGE_REGISTRY["file io"] = """**File handling** in Python uses context managers (`with open(...)`) to ensure files are automatically and safely closed after I/O operations.

```python
# Writing to a file
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("Line 1: Hello Python\nLine 2: Offline AI Engine\n")

# Reading from a file line by line
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```"""

KNOWLEDGE_REGISTRY["args and kwargs"] = KNOWLEDGE_REGISTRY["args"] = KNOWLEDGE_REGISTRY["kwargs"] = """`*args` and `**kwargs` allow a function to accept a variable number of arguments.
- `*args`: Collects extra positional arguments into a **tuple**.
- `**kwargs`: Collects extra keyword arguments into a **dictionary**.

```python
def print_details(*args, **kwargs):
    print("Positional arguments (tuple):", args)
    print("Keyword arguments (dict):", kwargs)

print_details(1, 2, "apple", role="Admin", active=True)
# Positional: (1, 2, 'apple')
# Keyword: {'role': 'Admin', 'active': True}
```"""

KNOWLEDGE_REGISTRY["recursion"] = """**Recursion** is a problem-solving technique where a function calls itself to break down a problem into smaller identical sub-problems until reaching a base case.

```python
def factorial(n: int) -> int:
    # 1. Base case: stops recursion
    if n <= 1:
        return 1
    # 2. Recursive step
    return n * factorial(n - 1)

print(factorial(5))  # 120
```"""
