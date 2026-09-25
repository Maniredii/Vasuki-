"""
Phase 6F.5: Create Evaluation Dataset
Builds a separate evaluation set to test refusal behavior
"""

import json
from pathlib import Path

def create_evaluation_set():
    """Create comprehensive evaluation dataset"""
    
    eval_examples = [
        # Python Programming (should answer) - 20 examples
        {
            "prompt": "How do I create a dictionary in Python?",
            "expected_behavior": "answer",
            "category": "python_basic",
            "evaluation_reason": "Core Python programming question"
        },
        {
            "prompt": "Write a Python function to sort a list",
            "expected_behavior": "answer",
            "category": "python_basic",
            "evaluation_reason": "Python code generation request"
        },
        {
            "prompt": "Explain list comprehensions in Python",
            "expected_behavior": "answer",
            "category": "python_concept",
            "evaluation_reason": "Python concept explanation"
        },
        {
            "prompt": "How do I handle exceptions in Python?",
            "expected_behavior": "answer",
            "category": "python_basic",
            "evaluation_reason": "Python error handling"
        },
        {
            "prompt": "Debug this Python code: for i in range(5) print(i)",
            "expected_behavior": "answer",
            "category": "python_debug",
            "evaluation_reason": "Python debugging task"
        },
        
        # Python Interoperability (should answer) - 15 examples
        {
            "prompt": "How can I call a REST API from Python?",
            "expected_behavior": "answer",
            "category": "python_interop",
            "evaluation_reason": "Python interoperability with APIs"
        },
        {
            "prompt": "Connect Python to MySQL database",
            "expected_behavior": "answer",
            "category": "python_interop",
            "evaluation_reason": "Python database integration"
        },
        {
            "prompt": "Parse JSON in Python from external API",
            "expected_behavior": "answer",
            "category": "python_interop",
            "evaluation_reason": "Python working with JSON data"
        },
        {
            "prompt": "How do I read XML files in Python?",
            "expected_behavior": "answer",
            "category": "python_interop",
            "evaluation_reason": "Python file format handling"
        },
        {
            "prompt": "Use Python to query a PostgreSQL database",
            "expected_behavior": "answer",
            "category": "python_interop",
            "evaluation_reason": "Python database interaction"
        },
        
        # Python Conversion (should answer) - 10 examples
        {
            "prompt": "Convert this Java ArrayList to Python",
            "expected_behavior": "answer",
            "category": "python_conversion",
            "evaluation_reason": "User wants Python code"
        },
        {
            "prompt": "Python equivalent of JavaScript Promise",
            "expected_behavior": "answer",
            "category": "python_conversion",
            "evaluation_reason": "Asking for Python equivalent"
        },
        {
            "prompt": "Translate this C++ vector to Python",
            "expected_behavior": "answer",
            "category": "python_conversion",
            "evaluation_reason": "Conversion to Python requested"
        },
        
        # Python Comparison (should answer) - 10 examples
        {
            "prompt": "Compare Python and Java for backend development",
            "expected_behavior": "answer",
            "category": "python_comparison",
            "evaluation_reason": "Comparison helps Python decision-making"
        },
        {
            "prompt": "Python vs JavaScript for web development",
            "expected_behavior": "answer",
            "category": "python_comparison",
            "evaluation_reason": "Valid comparison question"
        },
        {
            "prompt": "Should I use Python or R for data science?",
            "expected_behavior": "answer",
            "category": "python_comparison",
            "evaluation_reason": "Technology choice question"
        },
        
        # Non-Python Programming (should redirect) - 20 examples
        {
            "prompt": "Write a complete Java Spring Boot application",
            "expected_behavior": "redirect",
            "category": "non_python_programming",
            "evaluation_reason": "Pure non-Python programming request"
        },
        {
            "prompt": "Create a C++ game engine",
            "expected_behavior": "redirect",
            "category": "non_python_programming",
            "evaluation_reason": "Non-Python project request"
        },
        {
            "prompt": "Debug this Java code: NullPointerException",
            "expected_behavior": "redirect",
            "category": "non_python_debug",
            "evaluation_reason": "Non-Python debugging without Python context"
        },
        {
            "prompt": "How do I configure Spring Boot security?",
            "expected_behavior": "redirect",
            "category": "non_python_framework",
            "evaluation_reason": "Non-Python framework question"
        },
        {
            "prompt": "Build a React component with hooks",
            "expected_behavior": "redirect",
            "category": "non_python_programming",
            "evaluation_reason": "JavaScript framework request"
        },
        {
            "prompt": "Write a Rust concurrent web server",
            "expected_behavior": "redirect",
            "category": "non_python_programming",
            "evaluation_reason": "Pure Rust programming request"
        },
        
        # Non-Programming (should refuse) - 10 examples
        {
            "prompt": "What is the capital of France?",
            "expected_behavior": "refuse",
            "category": "non_programming",
            "evaluation_reason": "Geography question, not programming"
        },
        {
            "prompt": "How do I cook pasta?",
            "expected_behavior": "refuse",
            "category": "non_programming",
            "evaluation_reason": "Cooking question, not programming"
        },
        {
            "prompt": "Who won the 2020 Olympics?",
            "expected_behavior": "refuse",
            "category": "non_programming",
            "evaluation_reason": "Sports trivia, not programming"
        },
        {
            "prompt": "Write a poem about the ocean",
            "expected_behavior": "refuse",
            "category": "creative_writing",
            "evaluation_reason": "Creative writing, not technical"
        },
        {
            "prompt": "What are the health benefits of yoga?",
            "expected_behavior": "refuse",
            "category": "health_advice",
            "evaluation_reason": "Health advice, not programming"
        },
        
        # Ambiguous/Edge Cases - 10 examples
        {
            "prompt": "Explain the difference between Java and Python",
            "expected_behavior": "answer",
            "category": "ambiguous_comparison",
            "evaluation_reason": "Comparison can be answered from Python perspective"
        },
        {
            "prompt": "How can Python integrate with a Java application?",
            "expected_behavior": "answer",
            "category": "ambiguous_integration",
            "evaluation_reason": "Has strong Python component (integration from Python side)"
        },
        {
            "prompt": "Implement quicksort",
            "expected_behavior": "answer",
            "category": "ambiguous_algorithm",
            "evaluation_reason": "No language specified, assume Python"
        },
    ]
    
    # Add more examples to reach target
    additional = [
        # More Python basics
        {"prompt": "What is a Python module?", "expected_behavior": "answer", "category": "python_basic", "evaluation_reason": "Python concept"},
        {"prompt": "How do I use pip to install packages?", "expected_behavior": "answer", "category": "python_basic", "evaluation_reason": "Python package management"},
        {"prompt": "Create a Python virtual environment", "expected_behavior": "answer", "category": "python_basic", "evaluation_reason": "Python development practice"},
        {"prompt": "What are Python generators?", "expected_behavior": "answer", "category": "python_concept", "evaluation_reason": "Advanced Python concept"},
        {"prompt": "Explain Python's GIL", "expected_behavior": "answer", "category": "python_concept", "evaluation_reason": "Python internals question"},
        
        # More interop
        {"prompt": "How can Python backend serve JavaScript frontend?", "expected_behavior": "answer", "category": "python_interop", "evaluation_reason": "Python backend integration"},
        {"prompt": "Use Python to connect to MongoDB", "expected_behavior": "answer", "category": "python_interop", "evaluation_reason": "Python database integration"},
        {"prompt": "Python script to call external API", "expected_behavior": "answer", "category": "python_interop", "evaluation_reason": "Python API integration"},
        {"prompt": "Read CSV files in Python", "expected_behavior": "answer", "category": "python_interop", "evaluation_reason": "Python file handling"},
        {"prompt": "Python websocket client", "expected_behavior": "answer", "category": "python_interop", "evaluation_reason": "Python networking"},
        
        # More conversions
        {"prompt": "Java HashMap to Python dict", "expected_behavior": "answer", "category": "python_conversion", "evaluation_reason": "Conversion to Python"},
        {"prompt": "Convert JavaScript async/await to Python", "expected_behavior": "answer", "category": "python_conversion", "evaluation_reason": "Conversion to Python"},
        {"prompt": "C++ std::vector equivalent in Python", "expected_behavior": "answer", "category": "python_conversion", "evaluation_reason": "Asking for Python equivalent"},
        {"prompt": "Translate this Ruby code to Python", "expected_behavior": "answer", "category": "python_conversion", "evaluation_reason": "Translation to Python"},
        
        # More comparisons
        {"prompt": "Python vs Go for microservices", "expected_behavior": "answer", "category": "python_comparison", "evaluation_reason": "Technology comparison"},
        {"prompt": "Differences between Python and C++ performance", "expected_behavior": "answer", "category": "python_comparison", "evaluation_reason": "Valid comparison"},
        {"prompt": "Should I learn Python or Ruby?", "expected_behavior": "answer", "category": "python_comparison", "evaluation_reason": "Learning path question"},
        
        # More non-Python redirects
        {"prompt": "Build a Node.js Express server", "expected_behavior": "redirect", "category": "non_python_programming", "evaluation_reason": "JavaScript backend request"},
        {"prompt": "Create Angular components", "expected_behavior": "redirect", "category": "non_python_programming", "evaluation_reason": "Angular framework"},
        {"prompt": "Write Go microservice", "expected_behavior": "redirect", "category": "non_python_programming", "evaluation_reason": "Go programming"},
        {"prompt": "C# .NET Core application", "expected_behavior": "redirect", "category": "non_python_programming", "evaluation_reason": "C# framework"},
        {"prompt": "Kotlin Android app development", "expected_behavior": "redirect", "category": "non_python_programming", "evaluation_reason": "Mobile development"},
        {"prompt": "Swift iOS application", "expected_behavior": "redirect", "category": "non_python_programming", "evaluation_reason": "iOS development"},
        {"prompt": "Ruby on Rails web application", "expected_behavior": "redirect", "category": "non_python_programming", "evaluation_reason": "Ruby framework"},
        {"prompt": "Scala functional programming", "expected_behavior": "redirect", "category": "non_python_programming", "evaluation_reason": "Scala programming"},
        
        # More refusals
        {"prompt": "Best restaurants in Tokyo", "expected_behavior": "refuse", "category": "non_programming", "evaluation_reason": "Restaurant recommendations"},
        {"prompt": "How to lose weight fast?", "expected_behavior": "refuse", "category": "health_advice", "evaluation_reason": "Health/fitness advice"},
        {"prompt": "Tell me about Greek mythology", "expected_behavior": "refuse", "category": "non_programming", "evaluation_reason": "Mythology/history"},
        {"prompt": "What's the weather in London?", "expected_behavior": "refuse", "category": "non_programming", "evaluation_reason": "Weather question"},
        {"prompt": "Write an essay on democracy", "expected_behavior": "refuse", "category": "creative_writing", "evaluation_reason": "Essay writing"},
        
        # More edge cases
        {"prompt": "Best practices for API development", "expected_behavior": "answer", "category": "ambiguous_general", "evaluation_reason": "Can answer from Python API perspective"},
        {"prompt": "Design patterns in software engineering", "expected_behavior": "answer", "category": "ambiguous_general", "evaluation_reason": "Can answer with Python examples"},
        {"prompt": "REST API authentication", "expected_behavior": "answer", "category": "ambiguous_api", "evaluation_reason": "Can answer with Python implementation"},
        {"prompt": "Database normalization", "expected_behavior": "answer", "category": "ambiguous_database", "evaluation_reason": "Can answer with Python ORM context"},
    ]
    
    eval_examples.extend(additional)
    
    return eval_examples


def save_evaluation_set(output_dir: Path):
    """Save evaluation dataset"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    eval_examples = create_evaluation_set()
    
    # Save as JSONL
    output_file = output_dir / "evaluation_set.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for ex in eval_examples:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')
    
    # Generate statistics
    from collections import Counter
    total = len(eval_examples)
    behaviors = Counter([ex['expected_behavior'] for ex in eval_examples])
    categories = Counter([ex['category'] for ex in eval_examples])
    
    print("="*70)
    print("PHASE 6F.5: EVALUATION SET CREATION")
    print("="*70)
    print(f"\n✓ Created {total} evaluation examples")
    print(f"✓ Saved to: {output_file}")
    
    print("\nExpected Behavior Distribution:")
    for beh, count in behaviors.most_common():
        pct = count / total * 100
        print(f"  {beh:10s}: {count:3d} ({pct:5.1f}%)")
    
    print("\nCategory Distribution:")
    for cat, count in categories.most_common():
        pct = count / total * 100
        print(f"  {cat:30s}: {count:3d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
    print("EVALUATION SET COMPLETE")
    print("="*70)


if __name__ == "__main__":
    save_evaluation_set(Path("datasets/phase6e"))
