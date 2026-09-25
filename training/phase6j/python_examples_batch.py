"""
Phase 6J: Comprehensive Python Examples Batch Generator
Efficiently generates 300+ high-quality Python examples
"""

import json
from pathlib import Path
from typing import List, Tuple

# Example format: (instruction, response, tags, difficulty)
ExampleTuple = Tuple[str, str, List[str], str]


def get_all_python_examples() -> List[ExampleTuple]:
    """Return comprehensive list of all Python examples"""
    
    examples = []
    
    # ===== FUNDAMENTALS (40 examples) =====
    examples.extend([
        ("How do I create a variable in Python?",
         "In Python, create variables by assignment:\n\n```python\nx = 10\nname = 'Alice'\nis_active = True\nprice = 19.99\n```\n\nPython uses dynamic typing - no type declarations needed.",
         ["variables", "basics"], "beginner"),
        
        ("How do I check a variable's type in Python?",
         "Use type() or isinstance():\n\n```python\nx = 10\nprint(type(x))  # <class 'int'>\nprint(isinstance(x, int))  # True\n\n# Check multiple types\nvalue = 'hello'\nif isinstance(value, (str, bytes)):\n    print('String-like type')\n```\n\nisinstance() is preferred for type checking.",
         ["variables", "types"], "beginner"),
        
        ("How do I convert between types in Python?",
         "Use built-in conversion functions:\n\n```python\n# String to int\nnum = int('42')\n\n# Int to string\ntext = str(42)\n\n# String to float\nvalue = float('3.14')\n\n# List to tuple\ntup = tuple([1, 2, 3])\n\n# String to list\nchars = list('hello')\n```\n\nBe careful - invalid conversions raise ValueError.",
         ["types", "basics"], "beginner"),
        
        ("How do I reverse a string in Python?",
         "Use slice notation with [::-1]:\n\n```python\ntext = 'hello'\nreversed_text = text[::-1]\nprint(reversed_text)  # 'olleh'\n\n# Alternative\nreversed_text = ''.join(reversed(text))\n```\n\nThe [::-1] slice is the most Pythonic way.",
         ["strings", "slicing"], "beginner"),
        
        ("How do I split a string in Python?",
         "Use the split() method:\n\n```python\ntext = 'apple,banana,orange'\nfruits = text.split(',')\n# ['apple', 'banana', 'orange']\n\n# Split by whitespace (default)\nwords = 'Hello world'.split()\n# ['Hello', 'world']\n\n# Limit splits\ntext.split(',', maxsplit=1)\n# ['apple', 'banana,orange']\n```",
         ["strings"], "beginner"),
        
        ("How do I join strings in Python?",
         "Use the join() method:\n\n```python\nwords = ['Hello', 'world']\nsentence = ' '.join(words)  # 'Hello world'\n\n# Join with comma\nitems = ['a', 'b', 'c']\ncsv = ','.join(items)  # 'a,b,c'\n\n# Join numbers (convert first)\nnumbers = [1, 2, 3]\nresult = ','.join(map(str, numbers))\n```",
         ["strings"], "beginner"),
        
        ("How do I format strings in Python?",
         "Use f-strings (Python 3.6+):\n\n```python\nname = 'Alice'\nage = 30\n\n# F-string (recommended)\nmessage = f'{name} is {age} years old'\n\n# With expressions\nmessage = f'{name} will be {age + 1} next year'\n\n# format() method\nmessage = '{} is {} years old'.format(name, age)\n\n# Old % formatting\nmessage = '%s is %d years old' % (name, age)\n```",
         ["strings", "formatting"], "beginner"),
        
        ("How do I use if-else statements in Python?",
         "Use if-else for conditional logic:\n\n```python\nage = 18\n\nif age >= 18:\n    print('Adult')\nelse:\n    print('Minor')\n\n# Multiple conditions with elif\nscore = 85\nif score >= 90:\n    grade = 'A'\nelif score >= 80:\n    grade = 'B'\nelif score >= 70:\n    grade = 'C'\nelse:\n    grade = 'F'\n```",
         ["conditionals", "control-flow"], "beginner"),
        
        ("How do I use the ternary operator in Python?",
         "Use conditional expressions:\n\n```python\nage = 20\nstatus = 'Adult' if age >= 18 else 'Minor'\n\n# Equivalent to:\nif age >= 18:\n    status = 'Adult'\nelse:\n    status = 'Minor'\n\n# Use for simple cases only\nmax_value = a if a > b else b\n```",
         ["conditionals", "basics"], "beginner"),
        
        ("How do I use a for loop in Python?",
         "Iterate over sequences with for:\n\n```python\n# List iteration\nfruits = ['apple', 'banana', 'orange']\nfor fruit in fruits:\n    print(fruit)\n\n# Range\nfor i in range(5):\n    print(i)  # 0, 1, 2, 3, 4\n\n# Enumerate (index + value)\nfor index, fruit in enumerate(fruits):\n    print(f'{index}: {fruit}')\n\n# Dictionary\nperson = {'name': 'Alice', 'age': 30}\nfor key, value in person.items():\n    print(f'{key}: {value}')\n```",
         ["loops", "control-flow"], "beginner"),
        
        ("How do I use a while loop in Python?",
         "Use while for condition-based iteration:\n\n```python\ncount = 0\nwhile count < 5:\n    print(count)\n    count += 1\n\n# Infinite loop with break\nwhile True:\n    user_input = input('Enter quit to exit: ')\n    if user_input == 'quit':\n        break\n```",
         ["loops", "control-flow"], "beginner"),
        
        ("How do I break out of a loop in Python?",
         "Use the break statement:\n\n```python\nfor i in range(10):\n    if i == 5:\n        break\n    print(i)  # 0, 1, 2, 3, 4\n\n# Find first match\nnumbers = [1, 3, 5, 8, 9]\nfor num in numbers:\n    if num % 2 == 0:\n        print(f'Found: {num}')\n        break\n```",
         ["loops", "control-flow"], "beginner"),
        
        ("How do I skip to the next iteration in Python?",
         "Use the continue statement:\n\n```python\n# Skip specific value\nfor i in range(5):\n    if i == 2:\n        continue\n    print(i)  # 0, 1, 3, 4\n\n# Skip even numbers\nfor i in range(10):\n    if i % 2 == 0:\n        continue\n    print(i)  # Odd numbers only\n```",
         ["loops", "control-flow"], "beginner"),
        
        ("How do I check if a value is None in Python?",
         "Use 'is' operator for None:\n\n```python\nvalue = None\n\nif value is None:\n    print('Value is None')\n\nif value is not None:\n    print('Has value')\n\n# Don't use ==\nif value == None:  # Works but not Pythonic\n    pass\n```",
         ["basics", "conditionals"], "beginner"),
        
        ("How do I use logical operators in Python?",
         "Use and, or, not for logic:\n\n```python\nage = 25\nhas_license = True\n\n# AND\nif age >= 18 and has_license:\n    print('Can drive')\n\n# OR\nif age < 18 or not has_license:\n    print('Cannot drive')\n\n# NOT\nif not is_admin:\n    print('Access denied')\n\n# Short-circuit evaluation\nresult = value or 'default'\n```",
         ["operators", "conditionals"], "beginner"),
    ])
    
    # ===== DATA STRUCTURES (40 examples) =====
    examples.extend([
        ("How do I create a list in Python?",
         "Create lists with square brackets:\n\n```python\nfruits = ['apple', 'banana', 'orange']\nempty = []\nmixed = [1, 'hello', 3.14, True]\n\n# From range\nnumbers = list(range(10))\n\n# List comprehension\nsquares = [x**2 for x in range(10)]\n```",
         ["lists", "data-structures"], "beginner"),
        
        ("How do I add items to a list in Python?",
         "Use append(), extend(), or insert():\n\n```python\nfruits = ['apple']\n\n# Append single item\nfruits.append('banana')\n\n# Extend with multiple\nfruits.extend(['orange', 'grape'])\n\n# Insert at position\nfruits.insert(0, 'strawberry')\n\n# Concatenate\nfruits = fruits + ['mango']\n```",
         ["lists", "data-structures"], "beginner"),
        
        ("How do I remove items from a list in Python?",
         "Several methods available:\n\n```python\nfruits = ['apple', 'banana', 'orange']\n\n# Remove by value\nfruits.remove('banana')\n\n# Remove by index (returns item)\nitem = fruits.pop(0)\n\n# Remove last item\nfruits.pop()\n\n# Delete by index\ndel fruits[0]\n\n# Clear all\nfruits.clear()\n```",
         ["lists", "data-structures"], "beginner"),
        
        ("Explain list comprehensions in Python",
         "List comprehensions create lists concisely:\n\n```python\n# Basic: [expr for item in iterable]\nsquares = [x**2 for x in range(10)]\n\n# With condition\nevens = [x for x in range(20) if x % 2 == 0]\n\n# Transform strings\nwords = ['hello', 'world']\nupper = [w.upper() for w in words]\n\n# Nested\nmatrix = [[i*j for j in range(3)] for i in range(3)]\n\n# Flatten\nnested = [[1, 2], [3, 4]]\nflat = [item for sublist in nested for item in sublist]\n```",
         ["lists", "comprehensions"], "intermediate"),
        
        ("How do I slice lists in Python?",
         "Use [start:stop:step] syntax:\n\n```python\nnumbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]\n\nfirst_three = numbers[:3]  # [0, 1, 2]\nmiddle = numbers[3:7]  # [3, 4, 5, 6]\nlast_three = numbers[-3:]  # [7, 8, 9]\n\n# With step\nevens = numbers[::2]  # [0, 2, 4, 6, 8]\n\n# Reverse\nreversed = numbers[::-1]\n\n# Copy\ncopy = numbers[:]\n```",
         ["lists", "slicing"], "beginner"),
        
        ("How do I sort a list in Python?",
         "Use sort() or sorted():\n\n```python\nnumbers = [3, 1, 4, 1, 5, 9, 2]\n\n# In-place sort\nnumbers.sort()\n\n# Return new sorted list\nsorted_nums = sorted(numbers)\n\n# Reverse sort\nnumbers.sort(reverse=True)\n\n# Sort by key\nwords = ['banana', 'pie', 'Washington', 'book']\nwords.sort(key=str.lower)  # Case-insensitive\n\n# Sort complex objects\npeople = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]\npeople.sort(key=lambda p: p['age'])\n```",
         ["lists", "sorting"], "beginner"),
        
        ("How do I create a dictionary in Python?",
         "Use curly braces or dict():\n\n```python\n# Literal\nperson = {'name': 'Alice', 'age': 30}\n\n# Empty\nempty = {}\n\n# dict() constructor\nperson = dict(name='Alice', age=30)\n\n# From tuples\nitems = [('name', 'Alice'), ('age', 30)]\nperson = dict(items)\n\n# Dict comprehension\nsquares = {x: x**2 for x in range(5)}\n```",
         ["dictionaries", "data-structures"], "beginner"),
        
        ("How do I access dictionary values in Python?",
         "Use [] or get() method:\n\n```python\nperson = {'name': 'Alice', 'age': 30}\n\n# Direct access\nname = person['name']\n\n# Safe access (no KeyError)\nage = person.get('age')\ncountry = person.get('country', 'USA')  # Default\n\n# Check existence\nif 'name' in person:\n    print(person['name'])\n\n# Get all keys/values\nkeys = person.keys()\nvalues = person.values()\nitems = person.items()\n```",
         ["dictionaries"], "beginner"),
        
        ("How do I update a dictionary in Python?",
         "Several ways to modify dictionaries:\n\n```python\nperson = {'name': 'Alice'}\n\n# Add/update single key\nperson['age'] = 30\n\n# Update multiple\nperson.update({'city': 'NYC', 'age': 31})\n\n# Merge (Python 3.9+)\ndefaults = {'theme': 'dark', 'size': 'large'}\nconfig = {'size': 'small'}\nfinal = defaults | config  # {'theme': 'dark', 'size': 'small'}\n\n# Remove key\ndel person['age']\nage = person.pop('age', None)  # Safe remove\n```",
         ["dictionaries"], "beginner"),
        
        ("Explain dictionary comprehensions in Python",
         "Create dictionaries concisely:\n\n```python\n# Basic: {key: value for item in iterable}\nsquares = {x: x**2 for x in range(5)}\n\n# With condition\neven_squares = {x: x**2 for x in range(10) if x % 2 == 0}\n\n# Transform dict\nprices = {'apple': 0.5, 'banana': 0.3}\ndouble = {k: v*2 for k, v in prices.items()}\n\n# Invert dict\noriginal = {'a': 1, 'b': 2}\ninverted = {v: k for k, v in original.items()}\n\n# From two lists\nkeys = ['a', 'b', 'c']\nvalues = [1, 2, 3]\nresult = {k: v for k, v in zip(keys, values)}\n```",
         ["dictionaries", "comprehensions"], "intermediate"),
        
        ("What's the difference between list and tuple in Python?",
         "Lists are mutable, tuples are immutable:\n\n```python\n# List - mutable\nmy_list = [1, 2, 3]\nmy_list[0] = 10  # OK\nmy_list.append(4)  # OK\n\n# Tuple - immutable\nmy_tuple = (1, 2, 3)\n# my_tuple[0] = 10  # Error!\n# my_tuple.append(4)  # Error!\n\n# Create tuple\nsingle = (1,)  # Note comma\nmulti = 1, 2, 3  # Parens optional\n\n# Tuples are faster, use less memory\n# Use for fixed data, dict keys\n```",
         ["tuples", "lists"], "beginner"),
        
        ("How do I create a set in Python?",
         "Use curly braces or set():\n\n```python\n# Literal\nfruits = {'apple', 'banana', 'orange'}\n\n# From list (removes duplicates)\nnumbers = set([1, 2, 2, 3, 3, 4])\n# {1, 2, 3, 4}\n\n# Empty set\nempty = set()  # Not {}\n\n# Set comprehension\nsquares = {x**2 for x in range(10)}\n```",
         ["sets", "data-structures"], "beginner"),
        
        ("How do I perform set operations in Python?",
         "Use set operators:\n\n```python\na = {1, 2, 3, 4}\nb = {3, 4, 5, 6}\n\n# Union\nunion = a | b  # {1, 2, 3, 4, 5, 6}\nunion = a.union(b)\n\n# Intersection\ninter = a & b  # {3, 4}\ninter = a.intersection(b)\n\n# Difference\ndiff = a - b  # {1, 2}\ndiff = a.difference(b)\n\n# Symmetric difference\nsym_diff = a ^ b  # {1, 2, 5, 6}\n```",
         ["sets"], "beginner"),
        
        ("Explain set comprehensions in Python",
         "Create sets concisely:\n\n```python\n# Basic\nsquares = {x**2 for x in range(10)}\n\n# With condition\nevens = {x for x in range(20) if x % 2 == 0}\n\n# Remove duplicates\nwords = ['hello', 'Hello', 'HELLO']\nlower = {w.lower() for w in words}  # {'hello'}\n\n# Unique characters\ntext = 'hello world'\nchars = {c for c in text if c != ' '}\n```",
         ["sets", "comprehensions"], "intermediate"),
    ])
    
    return examples


def save_examples(examples: List[ExampleTuple], output_path: Path):
    """Save examples to JSONL format"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, (instruction, response, tags, difficulty) in enumerate(examples, 1):
            example = {
                "id": f"phase6j_batch_{idx:06d}",
                "instruction": instruction,
                "input": "",
                "response": response,
                "expected_behavior": "answer",
                "primary_category": "pure_python",
                "topic_tags": tags,
                "difficulty": difficulty,
                "source": "batch_generated",
                "quality_status": "generated"
            }
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    print(f"✓ Saved {len(examples)} examples to {output_path}")


if __name__ == "__main__":
    examples = get_all_python_examples()
    output_path = Path("D:/VASUKI/training/phase6j/python_examples_partial.jsonl")
    save_examples(examples, output_path)
    print(f"\nGenerated {len(examples)} examples so far")
    print("This is a partial batch - will be extended to 300+ examples")
