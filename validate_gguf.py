"""
GGUF Model Validation Script for Vasuki 0.5B
Validates file integrity, metadata, and Ollama compatibility
"""

import os
import sys
import struct
import hashlib
from pathlib import Path

def format_bytes(bytes_size):
    """Convert bytes to human-readable format"""
    mb = bytes_size / (1024 * 1024)
    gb = bytes_size / (1024 * 1024 * 1024)
    return f"{mb:.2f} MB ({gb:.4f} GB)"

def calculate_sha256(file_path, chunk_size=8192):
    """Calculate SHA-256 checksum of a file"""
    sha256_hash = hashlib.sha256()
    print(f"Calculating SHA-256 checksum (this may take a minute)...")
    
    try:
        with open(file_path, 'rb') as f:
            total_size = os.path.getsize(file_path)
            processed = 0
            
            while chunk := f.read(chunk_size):
                sha256_hash.update(chunk)
                processed += len(chunk)
                
                # Progress indicator
                if processed % (10 * 1024 * 1024) == 0:  # Every 10MB
                    progress = (processed / total_size) * 100
                    print(f"  Progress: {progress:.1f}%", end='\r')
        
        print(" " * 50, end='\r')  # Clear progress line
        return sha256_hash.hexdigest()
    except Exception as e:
        return f"ERROR: {str(e)}"

def validate_gguf_header(file_path):
    """Validate GGUF magic header and read basic metadata"""
    try:
        with open(file_path, 'rb') as f:
            # Read GGUF magic number (4 bytes)
            magic = f.read(4)
            
            if magic == b'GGUF':
                print("✓ Valid GGUF magic header detected")
                
                # Read version (4 bytes, little-endian uint32)
                version_bytes = f.read(4)
                version = struct.unpack('<I', version_bytes)[0]
                
                # Read tensor count (8 bytes, little-endian uint64)
                tensor_count_bytes = f.read(8)
                tensor_count = struct.unpack('<Q', tensor_count_bytes)[0]
                
                # Read metadata kv count (8 bytes, little-endian uint64)
                metadata_kv_count_bytes = f.read(8)
                metadata_kv_count = struct.unpack('<Q', metadata_kv_count_bytes)[0]
                
                return {
                    'valid': True,
                    'magic': magic.decode('utf-8'),
                    'version': version,
                    'tensor_count': tensor_count,
                    'metadata_kv_count': metadata_kv_count
                }
            else:
                return {
                    'valid': False,
                    'error': f'Invalid magic header: {magic.hex()}'
                }
                
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }

def check_file_integrity(file_path):
    """Check if file is readable and complete"""
    try:
        size = os.path.getsize(file_path)
        
        # Try to read the last byte to ensure file is complete
        with open(file_path, 'rb') as f:
            f.seek(-1, os.SEEK_END)
            last_byte = f.read(1)
        
        if last_byte:
            return True, size
        else:
            return False, size
            
    except Exception as e:
        return False, 0

def main():
    print("=" * 70)
    print("VASUKI 0.5B GGUF MODEL VALIDATION")
    print("=" * 70)
    
    # Target file
    target_file = "qwen2.5-coder-0.5b.Q4_K_M.gguf"
    file_path = Path(target_file)
    
    print(f"\nTarget Model: {target_file}")
    print("-" * 70)
    
    # Phase 1: File Integrity
    print("\n[PHASE 1] FILE INTEGRITY")
    print("-" * 70)
    
    # 1. Check if file exists
    if not file_path.exists():
        print(f"✗ ERROR: File not found: {file_path.absolute()}")
        
        # Check if F16 version exists instead
        f16_path = Path("qwen2.5-coder-0.5b.F16.gguf")
        if f16_path.exists():
            print(f"\n⚠ Found F16 version instead: {f16_path.name}")
            print(f"  Size: {format_bytes(f16_path.stat().st_size)}")
            response = input("\nValidate F16 version instead? (y/n): ")
            if response.lower() == 'y':
                file_path = f16_path
                target_file = f16_path.name
            else:
                sys.exit(1)
        else:
            sys.exit(1)
    
    print(f"✓ File located: {file_path.absolute()}")
    
    # 2. File size
    file_size = file_path.stat().st_size
    print(f"✓ File size: {format_bytes(file_size)}")
    
    # 3. Extension check
    if file_path.suffix.lower() == '.gguf':
        print(f"✓ File extension: {file_path.suffix}")
    else:
        print(f"⚠ Warning: Unexpected extension: {file_path.suffix}")
    
    # 4. File integrity
    is_complete, size = check_file_integrity(file_path)
    if is_complete:
        print("✓ File is readable and appears complete")
    else:
        print("✗ File may be truncated or corrupted")
    
    # 5. GGUF header validation
    print("\n[PHASE 1.1] GGUF HEADER VALIDATION")
    print("-" * 70)
    header_info = validate_gguf_header(file_path)
    
    if header_info['valid']:
        print(f"✓ GGUF Version: {header_info['version']}")
        print(f"✓ Tensor Count: {header_info['tensor_count']}")
        print(f"✓ Metadata Entries: {header_info['metadata_kv_count']}")
    else:
        print(f"✗ Invalid GGUF file: {header_info['error']}")
        sys.exit(1)
    
    # 6. SHA-256 checksum
    print("\n[PHASE 1.2] CHECKSUM CALCULATION")
    print("-" * 70)
    checksum = calculate_sha256(file_path)
    print(f"✓ SHA-256: {checksum}")
    
    # Phase 2: GGUF Metadata Inspection
    print("\n[PHASE 2] GGUF METADATA INSPECTION")
    print("-" * 70)
    print("⚠ Advanced metadata parsing requires specialized tools")
    print("  Recommended tools:")
    print("  - llama.cpp (gguf-py library)")
    print("  - Hugging Face gguf library")
    print("  - llama-cpp-python")
    
    # Check if gguf library is available
    try:
        import gguf
        print("\n✓ gguf library is installed")
        print("  Attempting to read detailed metadata...")
        
        try:
            reader = gguf.GGUFReader(str(file_path))
            
            print("\n--- GGUF Metadata ---")
            
            # Extract metadata
            if hasattr(reader, 'fields'):
                for field_name, field in reader.fields.items():
                    # Display important fields
                    if any(key in field_name.lower() for key in ['arch', 'name', 'quant', 'context', 'vocab']):
                        print(f"  {field_name}: {field.parts if hasattr(field, 'parts') else field}")
            
            # Tensor information
            if hasattr(reader, 'tensors'):
                print(f"\n  Total tensors: {len(reader.tensors)}")
                if len(reader.tensors) > 0:
                    print(f"  First tensor: {reader.tensors[0].name if hasattr(reader.tensors[0], 'name') else 'Unknown'}")
            
        except Exception as e:
            print(f"  ⚠ Could not parse all metadata: {e}")
            
    except ImportError:
        print("  ⚠ gguf library not installed")
        print("  Install with: pip install gguf")
    
    # Phase 3: Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Model File:       {target_file}")
    print(f"Absolute Path:    {file_path.absolute()}")
    print(f"File Size:        {format_bytes(file_size)}")
    print(f"SHA-256:          {checksum}")
    print(f"GGUF Valid:       {'YES' if header_info['valid'] else 'NO'}")
    print(f"GGUF Version:     {header_info.get('version', 'Unknown')}")
    print(f"Tensor Count:     {header_info.get('tensor_count', 'Unknown')}")
    print("=" * 70)
    
    print("\n✓ Phase 1 validation complete")
    print("\nNext steps:")
    print("1. Install gguf library for detailed metadata: pip install gguf")
    print("2. Check Ollama compatibility (see ollama_check.py)")
    print("3. Test model inference")

if __name__ == "__main__":
    main()
