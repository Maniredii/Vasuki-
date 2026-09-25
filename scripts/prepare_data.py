"""
Data Preparation Script for Vasuki 0.5B Model
Downloads Python code instruction dataset and generates refusal dataset
"""

import json
import random
from datasets import load_dataset
import pandas as pd
from pathlib import Path

def generate_refusal_dataset(num_samples=5000):
    """
    Generate synthetic refusal dataset for non-programming questions.
    This helps the model learn to stay focused on Python programming tasks.
    """
    
    # Non-programming question templates
    question_templates = [
        "What is the capital of {}?",
        "How do I cook {}?",
        "Tell me about the history of {}.",
        "What's the weather like in {}?",
        "Who won the {} championship?",
        "What are the health benefits of {}?",
        "How do I fix my {}?",
        "What's the best way to travel to {}?",
        "Tell me a joke about {}.",
        "What does {} mean in philosophy?",
        "How do I plant {}?",
        "What's the population of {}?",
        "Who invented the {}?",
        "What are the side effects of {}?",
        "How much does a {} cost?",
        "What's the difference between {} and {}?",
        "Can you recommend a good {} restaurant?",
        "How do I learn {}?",
        "What's the meaning of life according to {}?",
        "Tell me about {} mythology.",
        "How do I meditate using {}?",
        "What are the rules of {}?",
        "Who is the president of {}?",
        "What's the best {} brand?",
        "How do I lose weight with {}?",
    ]
    
    # Random subjects to fill templates
    subjects = [
        "France", "pasta", "Rome", "London", "2020", "yoga", "car", 
        "Japan", "cats", "Aristotle", "roses", "China", "telephone",
        "aspirin", "bicycle", "coffee and tea", "Italian", "Spanish",
        "Buddhism", "Greek", "mindfulness", "chess", "Brazil", 
        "Samsung", "keto diet", "meditation", "democracy", "soccer",
        "painting", "music", "poetry", "dancing", "swimming"
    ]
    
    refusal_response = "I am a lightweight AI designed exclusively for Python programming. I cannot answer this."
    
    refusal_data = []
    for i in range(num_samples):
        template = random.choice(question_templates)
        # Handle templates with one or two placeholders
        if template.count('{}') == 2:
            subject1, subject2 = random.sample(subjects, 2)
            question = template.format(subject1, subject2)
        else:
            subject = random.choice(subjects)
            question = template.format(subject)
        
        refusal_data.append({
            'instruction': question,
            'input': '',
            'output': refusal_response
        })
    
    return refusal_data

def prepare_training_data():
    """
    Main function to prepare the complete training dataset.
    """
    print("Starting data preparation...")
    
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Step 1: Load the Python code instructions dataset
    print("\n[1/4] Downloading Python code instructions dataset...")
    try:
        python_dataset = load_dataset("iamtarun/python_code_instructions_18k_alpaca", split='train')
        print(f"✓ Successfully loaded {len(python_dataset)} Python instruction samples")
    except Exception as e:
        print(f"✗ Error loading dataset: {e}")
        return
    
    # Step 2: Convert to list of dictionaries with consistent format
    print("\n[2/4] Processing Python instructions...")
    python_data = []
    for item in python_dataset:
        python_data.append({
            'instruction': item.get('instruction', ''),
            'input': item.get('input', ''),
            'output': item.get('output', '')
        })
    
    print(f"✓ Processed {len(python_data)} Python instruction samples")
    
    # Step 3: Generate refusal dataset
    print("\n[3/4] Generating refusal dataset...")
    refusal_data = generate_refusal_dataset(num_samples=5000)
    print(f"✓ Generated {len(refusal_data)} refusal samples")
    
    # Step 4: Combine datasets
    print("\n[4/4] Combining and saving datasets...")
    combined_data = python_data + refusal_data
    
    # Shuffle the combined dataset
    random.shuffle(combined_data)
    
    # Save as JSONL (one JSON object per line)
    output_file = data_dir / "training_data.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in combined_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"\n✓ Successfully saved {len(combined_data)} samples to {output_file}")
    
    # Print dataset statistics
    print("\n" + "="*60)
    print("DATASET STATISTICS")
    print("="*60)
    print(f"Python Code Instructions: {len(python_data):,}")
    print(f"Refusal Examples:         {len(refusal_data):,}")
    print(f"Total Training Samples:   {len(combined_data):,}")
    print(f"Output File:              {output_file.absolute()}")
    print("="*60)
    
    # Show a few examples
    print("\n" + "="*60)
    print("SAMPLE DATA (First 2 examples)")
    print("="*60)
    for i, sample in enumerate(combined_data[:2], 1):
        print(f"\n--- Example {i} ---")
        print(f"Instruction: {sample['instruction'][:100]}...")
        if sample['input']:
            print(f"Input: {sample['input'][:100]}...")
        print(f"Output: {sample['output'][:100]}...")
    print("="*60)

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    
    # Run the data preparation
    prepare_training_data()
    
    print("\n✓ Data preparation complete! Ready for training.")
