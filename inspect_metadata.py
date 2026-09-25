"""
Detailed GGUF Metadata Inspection for Vasuki 0.5B
"""

import sys
from pathlib import Path
import gguf

def inspect_gguf_metadata(file_path):
    """Extract and display detailed GGUF metadata"""
    
    print("=" * 70)
    print("DETAILED GGUF METADATA INSPECTION")
    print("=" * 70)
    print(f"\nFile: {file_path}")
    print("-" * 70)
    
    try:
        reader = gguf.GGUFReader(str(file_path))
        
        # Extract key metadata
        metadata = {}
        
        print("\n[GENERAL METADATA]")
        print("-" * 70)
        
        for key, field in reader.fields.items():
            # Extract value based on field type
            if hasattr(field, 'parts'):
                value = field.parts
            elif hasattr(field, 'data'):
                value = field.data
            else:
                value = str(field)
            
            # Store and display important fields
            if isinstance(value, (list, tuple)) and len(value) == 1:
                value = value[0]
            
            metadata[key] = value
            
            # Display key metadata
            key_lower = key.lower()
            if any(keyword in key_lower for keyword in [
                'name', 'arch', 'version', 'author', 'organization',
                'quantization', 'file_type', 'context', 'vocab',
                'embedding', 'block_count', 'head_count', 'rope'
            ]):
                # Truncate long values
                display_value = str(value)
                if len(display_value) > 100:
                    display_value = display_value[:97] + "..."
                print(f"  {key}: {display_value}")
        
        # Architecture details
        print("\n[ARCHITECTURE]")
        print("-" * 70)
        arch_keys = [k for k in metadata.keys() if 'arch' in k.lower() or 'model' in k.lower()]
        for key in arch_keys:
            print(f"  {key}: {metadata[key]}")
        
        # Quantization details
        print("\n[QUANTIZATION]")
        print("-" * 70)
        quant_keys = [k for k in metadata.keys() if 'quant' in k.lower() or 'file_type' in k.lower()]
        for key in quant_keys:
            print(f"  {key}: {metadata[key]}")
        
        if not quant_keys:
            print("  (No explicit quantization metadata found)")
            print("  Quantization type inferred from filename: Q4_K_M")
        
        # Context and capacity
        print("\n[CONTEXT & CAPACITY]")
        print("-" * 70)
        context_keys = [k for k in metadata.keys() if any(word in k.lower() 
                       for word in ['context', 'length', 'window', 'max'])]
        for key in context_keys:
            print(f"  {key}: {metadata[key]}")
        
        # Tokenizer/Vocab
        print("\n[TOKENIZER]")
        print("-" * 70)
        vocab_keys = [k for k in metadata.keys() if 'vocab' in k.lower() or 'token' in k.lower()]
        for key in vocab_keys:
            value = metadata[key]
            if isinstance(value, (list, dict)) and len(str(value)) > 100:
                print(f"  {key}: <{type(value).__name__} with {len(value)} items>")
            else:
                print(f"  {key}: {value}")
        
        # Tensor information
        print("\n[TENSORS]")
        print("-" * 70)
        print(f"  Total tensor count: {len(reader.tensors)}")
        
        if len(reader.tensors) > 0:
            print(f"\n  Sample tensors (first 5):")
            for i, tensor in enumerate(reader.tensors[:5]):
                tensor_name = tensor.name if hasattr(tensor, 'name') else f"tensor_{i}"
                tensor_shape = tensor.shape if hasattr(tensor, 'shape') else "Unknown"
                tensor_type = tensor.tensor_type if hasattr(tensor, 'tensor_type') else "Unknown"
                print(f"    [{i+1}] {tensor_name}")
                print(f"        Shape: {tensor_shape}")
                print(f"        Type: {tensor_type}")
        
        # Chat template (important for deployment)
        print("\n[CHAT TEMPLATE]")
        print("-" * 70)
        chat_keys = [k for k in metadata.keys() if 'chat' in k.lower() or 'template' in k.lower()]
        if chat_keys:
            for key in chat_keys:
                value = str(metadata[key])
                if len(value) > 200:
                    print(f"  {key}: {value[:197]}...")
                else:
                    print(f"  {key}: {value}")
        else:
            print("  No chat template found in metadata")
        
        # Summary
        print("\n" + "=" * 70)
        print("METADATA SUMMARY")
        print("=" * 70)
        
        # Extract key information
        arch = metadata.get('general.architecture', 'Unknown')
        model_name = metadata.get('general.name', 'Unknown')
        file_type = metadata.get('general.file_type', 'Unknown')
        
        print(f"Model Name:       {model_name}")
        print(f"Architecture:     {arch}")
        print(f"File Type:        {file_type}")
        print(f"Total Tensors:    {len(reader.tensors)}")
        print(f"Metadata Fields:  {len(reader.fields)}")
        print("=" * 70)
        
        return True, metadata
        
    except Exception as e:
        print(f"\n✗ ERROR: Failed to read GGUF metadata")
        print(f"  {type(e).__name__}: {e}")
        return False, None

def main():
    # Check both Q4_K_M and F16 versions
    q4_file = Path("qwen2.5-coder-0.5b.Q4_K_M.gguf")
    f16_file = Path("qwen2.5-coder-0.5b.F16.gguf")
    
    if q4_file.exists():
        print("\n[INSPECTING Q4_K_M VERSION]")
        success, metadata = inspect_gguf_metadata(q4_file)
    
    if f16_file.exists():
        print("\n\n[INSPECTING F16 VERSION]")
        success, metadata = inspect_gguf_metadata(f16_file)

if __name__ == "__main__":
    main()
