"""
Quick GGUF Metadata Inspection - Focused on key fields only
"""

from pathlib import Path
import gguf

def safe_extract_value(field):
    """Safely extract value from GGUF field"""
    try:
        if hasattr(field, 'parts') and len(field.parts) > 0:
            # Get the last part which usually contains the actual value
            value = field.parts[-1]
            
            # If it's a numpy array with a single value, extract it
            if hasattr(value, 'shape') and len(value.shape) == 0:
                return value.item()
            elif hasattr(value, 'shape') and len(value.shape) == 1 and len(value) == 1:
                return value[0]
            elif hasattr(value, 'shape') and value.size < 100:
                # Convert small arrays to list
                return value.tolist() if hasattr(value, 'tolist') else str(value)
            elif hasattr(value, 'tobytes'):
                # Try to decode as string
                try:
                    return value.tobytes().decode('utf-8', errors='ignore')
                except:
                    return f"<binary data: {value.shape}>"
            return str(value)
        return str(field)
    except:
        return "<unable to extract>"

def inspect_gguf_quick(file_path):
    """Quick metadata inspection focusing on deployment-critical fields"""
    
    print("=" * 70)
    print(f"GGUF METADATA: {file_path.name}")
    print("=" * 70)
    
    try:
        reader = gguf.GGUFReader(str(file_path))
        
        # Key fields to extract
        important_fields = {
            'Architecture': 'general.architecture',
            'Model Name': 'general.name',
            'Base Name': 'general.basename',
            'File Type': 'general.file_type',
            'Quantized By': 'general.quantized_by',
            'Quantization Version': 'general.quantization_version',
            'Block Count': 'qwen2.block_count',
            'Context Length': 'qwen2.context_length',
            'Embedding Length': 'qwen2.embedding_length',
            'Head Count': 'qwen2.attention.head_count',
            'KV Head Count': 'qwen2.attention.head_count_kv',
            'Vocab Size': 'tokenizer.ggml.vocab_size',
            'RoPE Freq Base': 'qwen2.rope.freq_base',
        }
        
        print("\n[KEY METADATA]")
        print("-" * 70)
        
        for label, key in important_fields.items():
            if key in reader.fields:
                value = safe_extract_value(reader.fields[key])
                print(f"  {label:20s}: {value}")
            else:
                print(f"  {label:20s}: <not found>")
        
        # File type interpretation
        print("\n[QUANTIZATION INFO]")
        print("-" * 70)
        if 'general.file_type' in reader.fields:
            file_type_val = safe_extract_value(reader.fields['general.file_type'])
            
            # GGUF file type mapping
            file_type_names = {
                0: "F32",
                1: "F16",
                2: "Q4_0",
                3: "Q4_1",
                6: "Q5_0",
                7: "Q5_1",
                8: "Q8_0",
                9: "Q8_1",
                10: "Q2_K",
                11: "Q3_K_S",
                12: "Q3_K_M",
                13: "Q3_K_L",
                14: "Q4_K_S",
                15: "Q4_K_M",  # This is what we expect
                16: "Q5_K_S",
                17: "Q5_K_M",
                18: "Q6_K"
            }
            
            try:
                file_type_int = int(file_type_val)
                quant_name = file_type_names.get(file_type_int, f"Unknown ({file_type_int})")
                print(f"  File Type Code:     {file_type_int}")
                print(f"  Quantization:       {quant_name}")
                
                if file_type_int == 15:
                    print(f"  ✓ Matches expected: Q4_K_M")
                else:
                    print(f"  ⚠ WARNING: Expected Q4_K_M (15), got {quant_name} ({file_type_int})")
            except:
                print(f"  File Type:          {file_type_val}")
        
        # Tensor summary
        print("\n[TENSORS]")
        print("-" * 70)
        print(f"  Total Tensors:      {len(reader.tensors)}")
        
        if len(reader.tensors) > 0:
            print(f"  First 3 tensors:")
            for i in range(min(3, len(reader.tensors))):
                tensor = reader.tensors[i]
                name = tensor.name if hasattr(tensor, 'name') else f"tensor_{i}"
                print(f"    - {name}")
        
        # Chat template check
        print("\n[CHAT TEMPLATE]")
        print("-" * 70)
        has_chat = False
        for key in reader.fields.keys():
            if 'chat' in key.lower() or 'template' in key.lower():
                has_chat = True
                value = safe_extract_value(reader.fields[key])
                if len(str(value)) > 100:
                    print(f"  {key}: {str(value)[:97]}...")
                else:
                    print(f"  {key}: {value}")
        
        if not has_chat:
            print("  ⚠ No chat template found")
            print("  Note: Ollama will use default template for architecture")
        
        print("\n" + "=" * 70)
        print("✓ Metadata inspection complete")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    q4_file = Path("qwen2.5-coder-0.5b.Q4_K_M.gguf")
    
    if q4_file.exists():
        inspect_gguf_quick(q4_file)
    else:
        print(f"✗ File not found: {q4_file}")

if __name__ == "__main__":
    main()
