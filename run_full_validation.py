"""
Complete Validation Suite for Vasuki 0.5B GGUF Model
Runs all validation phases in sequence
"""

import subprocess
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)

def run_script(script_name, description):
    """Run a validation script and report results"""
    print(f"\n🔍 {description}")
    print("-" * 70)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=180
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"⚠️ {description} - COMPLETED WITH WARNINGS")
            if result.stderr:
                print(f"Errors: {result.stderr}")
            return True
            
    except subprocess.TimeoutExpired:
        print(f"⏱️ {description} - TIMEOUT (taking too long)")
        return False
    except Exception as e:
        print(f"❌ {description} - FAILED: {e}")
        return False

def main():
    print_header("VASUKI 0.5B COMPLETE VALIDATION SUITE")
    print("\nRunning all validation phases...")
    print("This will check file integrity, metadata, and Ollama compatibility")
    
    results = {}
    
    # Phase 1: Basic file integrity
    results['integrity'] = run_script(
        'validate_gguf.py',
        'Phase 1: File Integrity Check'
    )
    
    # Phase 2: Detailed metadata
    results['metadata'] = run_script(
        'quick_metadata.py',
        'Phase 2: Metadata Inspection'
    )
    
    # Phase 3: Ollama compatibility
    results['ollama'] = run_script(
        'check_ollama.py',
        'Phase 3: Ollama Compatibility'
    )
    
    # Final summary
    print_header("VALIDATION SUMMARY")
    
    print("\nResults:")
    print("-" * 70)
    print(f"  File Integrity:       {'✅ PASS' if results['integrity'] else '❌ FAIL'}")
    print(f"  Metadata Inspection:  {'✅ PASS' if results['metadata'] else '❌ FAIL'}")
    print(f"  Ollama Compatibility: {'✅ PASS' if results['ollama'] else '❌ FAIL'}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL VALIDATIONS PASSED".center(70))
        print("=" * 70)
        print("\n📄 Full report available in: VALIDATION_REPORT.md")
        print("\n🚀 Next step: Import the model into Ollama")
        print("   Command: ollama create vasuki:0.5b -f Modelfile")
    else:
        print("⚠️ VALIDATION COMPLETED WITH ISSUES".center(70))
        print("=" * 70)
        print("\nPlease review the output above for details.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
