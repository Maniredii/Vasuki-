"""
Phase 6F.2: Validate Phase 6E Dataset Quality
Comprehensive validation of generated training examples
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Any, Set

class DatasetValidator:
    """Validates quality and correctness of generated dataset"""
    
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        self.examples = []
        self.validation_results = {
            'total_records': 0,
            'valid_records': 0,
            'issues': [],
            'warnings': [],
            'statistics': {}
        }
        
    def load_dataset(self):
        """Load and parse dataset"""
        print(f"Loading dataset from: {self.dataset_path}")
        
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    example = json.loads(line)
                    example['_line_num'] = line_num
                    self.examples.append(example)
                except json.JSONDecodeError as e:
                    self.validation_results['issues'].append({
                        'line': line_num,
                        'type': 'parse_error',
                        'message': str(e)
                    })
        
        self.validation_results['total_records'] = len(self.examples)
        print(f"✓ Loaded {len(self.examples)} examples")
    
    def validate_structure(self):
        """Validate required fields and structure"""
        print("\nValidating structure...")
        
        required_fields = ['id', 'instruction', 'input', 'response', 'scope_label', 
                          'expected_behavior', 'category']
        
        for ex in self.examples:
            # Check required fields
            missing = [f for f in required_fields if f not in ex]
            if missing:
                self.validation_results['issues'].append({
                    'id': ex.get('id', 'unknown'),
                    'line': ex['_line_num'],
                    'type': 'missing_fields',
                    'fields': missing
                })
            
            # Check empty fields
            if ex.get('instruction', '').strip() == '':
                self.validation_results['issues'].append({
                    'id': ex.get('id'),
                    'type': 'empty_instruction',
                    'line': ex['_line_num']
                })
            
            if ex.get('response', '').strip() == '':
                self.validation_results['issues'].append({
                    'id': ex.get('id'),
                    'type': 'empty_response',
                    'line': ex['_line_num']
                })
        
        print(f"✓ Structure validation complete")
    
    def validate_duplicates(self):
        """Check for duplicate instructions"""
        print("\nChecking duplicates...")
        
        instructions = [ex['instruction'] for ex in self.examples]
        inst_counter = Counter(instructions)
        
        duplicates = {inst: count for inst, count in inst_counter.items() if count > 1}
        
        if duplicates:
            self.validation_results['warnings'].append({
                'type': 'duplicate_instructions',
                'count': len(duplicates),
                'examples': list(duplicates.items())[:10]  # First 10
            })
        
        # Check instruction-response pairs
        pairs = [(ex['instruction'], ex['response']) for ex in self.examples]
        pair_counter = Counter(pairs)
        exact_dupes = sum(1 for count in pair_counter.values() if count > 1)
        
        self.validation_results['statistics']['duplicate_rate'] = {
            'unique_instructions': len(inst_counter),
            'duplicate_instructions': len(duplicates),
            'exact_duplicate_pairs': exact_dupes
        }
        
        print(f"✓ Unique instructions: {len(inst_counter)}")
        print(f"⚠ Duplicate instructions: {len(duplicates)}")
    
    def validate_scope_labels(self):
        """Validate scope labels and consistency"""
        print("\nValidating scope labels...")
        
        valid_labels = {
            'answer_python', 'answer_python_interoperability',
            'answer_python_conversion', 'answer_python_comparison',
            'redirect_non_python', 'refuse_non_programming',
            'refuse_creative', 'refuse_personal_advice', 'manual_review'
        }
        
        for ex in self.examples:
            label = ex.get('scope_label')
            if label not in valid_labels:
                self.validation_results['issues'].append({
                    'id': ex.get('id'),
                    'type': 'invalid_scope_label',
                    'label': label,
                    'line': ex['_line_num']
                })
            
            # Check behavior consistency
            behavior = ex.get('expected_behavior')
            if label and label.startswith('answer_') and behavior != 'answer':
                self.validation_results['issues'].append({
                    'id': ex.get('id'),
                    'type': 'inconsistent_behavior',
                    'label': label,
                    'behavior': behavior,
                    'line': ex['_line_num']
                })
            elif label and label.startswith('redirect_') and behavior != 'redirect':
                self.validation_results['issues'].append({
                    'id': ex.get('id'),
                    'type': 'inconsistent_behavior',
                    'label': label,
                    'behavior': behavior,
                    'line': ex['_line_num']
                })
        
        print(f"✓ Scope label validation complete")
    
    def validate_response_diversity(self):
        """Check response template diversity"""
        print("\nAnalyzing response diversity...")
        
        responses = [ex['response'] for ex in self.examples]
        response_counter = Counter(responses)
        
        # Check if any single response dominates
        total = len(responses)
        for response, count in response_counter.most_common(10):
            pct = count / total * 100
            if pct > 50:
                self.validation_results['issues'].append({
                    'type': 'low_response_diversity',
                    'message': f'Single response used {count} times ({pct:.1f}%)',
                    'response_preview': response[:100]
                })
        
        self.validation_results['statistics']['response_diversity'] = {
            'unique_responses': len(response_counter),
            'total_responses': total,
            'diversity_rate': len(response_counter) / total * 100
        }
        
        print(f"✓ Unique responses: {len(response_counter)} ({len(response_counter)/total*100:.1f}%)")
    
    def validate_python_refusals(self):
        """Check for Python questions being refused (contamination)"""
        print("\nChecking for Python question contamination...")
        
        python_keywords = ['python', 'django', 'flask', 'pandas', 'numpy', 'pip']
        
        contaminated = []
        for ex in self.examples:
            inst_lower = ex['instruction'].lower()
            behavior = ex.get('expected_behavior')
            
            # Check if instruction mentions Python but is marked as redirect/refuse
            if any(kw in inst_lower for kw in python_keywords):
                if behavior in ['redirect', 'refuse']:
                    # Double-check it's not a legitimate redirect
                    # (e.g., "Write complete Java and Python app" should redirect)
                    if not any(lang in inst_lower for lang in ['java', 'javascript', 'c++', 'c#']):
                        contaminated.append({
                            'id': ex.get('id'),
                            'instruction': ex['instruction'],
                            'behavior': behavior,
                            'line': ex['_line_num']
                        })
        
        if contaminated:
            self.validation_results['issues'].append({
                'type': 'python_question_contamination',
                'count': len(contaminated),
                'examples': contaminated[:5]  # First 5
            })
            print(f"❌ Found {len(contaminated)} Python questions marked for refusal!")
        else:
            print(f"✅ No Python contamination found")
    
    def validate_interoperability(self):
        """Validate that interoperability questions are answered"""
        print("\nValidating interoperability handling...")
        
        interop_indicators = [
            'call', 'api', 'rest', 'connect', 'database', 'sql',
            'integrate', 'json', 'xml', 'parse', 'from python'
        ]
        
        should_answer = []
        for ex in self.examples:
            inst_lower = ex['instruction'].lower()
            behavior = ex.get('expected_behavior')
            
            # Check for interoperability context
            has_python = 'python' in inst_lower
            has_interop = any(ind in inst_lower for ind in interop_indicators)
            
            if has_python and has_interop and behavior != 'answer':
                should_answer.append({
                    'id': ex.get('id'),
                    'instruction': ex['instruction'],
                    'behavior': behavior,
                    'line': ex['_line_num']
                })
        
        if should_answer:
            self.validation_results['warnings'].append({
                'type': 'interop_not_answered',
                'count': len(should_answer),
                'examples': should_answer[:3]
            })
            print(f"⚠ Found {len(should_answer)} interop questions not marked as 'answer'")
        else:
            print(f"✅ Interoperability questions properly handled")
    
    def validate_redirect_responses(self):
        """Check that redirect responses don't include non-Python implementations"""
        print("\nValidating redirect responses...")
        
        code_indicators = ['class ', 'public ', 'void ', 'int ', 'return', 'function']
        
        bad_redirects = []
        for ex in self.examples:
            if ex.get('expected_behavior') == 'redirect':
                response = ex['response']
                # Check if response contains code that might be non-Python
                if any(ind in response for ind in code_indicators):
                    # Could be showing non-Python code in redirect
                    if 'java' in response.lower() or 'javascript' in response.lower():
                        bad_redirects.append({
                            'id': ex.get('id'),
                            'instruction': ex['instruction'],
                            'response_preview': response[:150],
                            'line': ex['_line_num']
                        })
        
        if bad_redirects:
            self.validation_results['warnings'].append({
                'type': 'redirect_with_code',
                'count': len(bad_redirects),
                'examples': bad_redirects[:3]
            })
            print(f"⚠ Found {len(bad_redirects)} redirects that may include non-Python code")
        else:
            print(f"✅ Redirect responses are clean")
    
    def generate_report(self, output_dir: Path):
        """Generate validation reports"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Calculate statistics
        stats = {
            'total_records': len(self.examples),
            'issues_count': len(self.validation_results['issues']),
            'warnings_count': len(self.validation_results['warnings']),
            'categories': Counter([ex['category'] for ex in self.examples]),
            'behaviors': Counter([ex['expected_behavior'] for ex in self.examples]),
            'scope_labels': Counter([ex['scope_label'] for ex in self.examples])
        }
        
        # Save JSON report
        json_file = output_dir / "phase6e_dataset_validation.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'statistics': stats,
                'validation_results': self.validation_results
            }, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n✓ Saved JSON report: {json_file}")
        
        # Save Markdown report
        md_file = output_dir / "phase6e_dataset_validation.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# Phase 6E Dataset Validation Report\n\n")
            f.write(f"**Date**: 2026-09-23\n\n")
            f.write(f"**Dataset**: {self.dataset_path}\n\n")
            f.write("---\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Total Records**: {stats['total_records']}\n")
            f.write(f"- **Issues Found**: {stats['issues_count']}\n")
            f.write(f"- **Warnings**: {stats['warnings_count']}\n")
            f.write(f"- **Unique Instructions**: {self.validation_results['statistics'].get('duplicate_rate', {}).get('unique_instructions', 'N/A')}\n\n")
            
            f.write("## Category Distribution\n\n")
            for cat, count in stats['categories'].most_common():
                pct = count / stats['total_records'] * 100
                f.write(f"- {cat}: {count} ({pct:.1f}%)\n")
            f.write("\n")
            
            f.write("## Expected Behavior Distribution\n\n")
            for beh, count in stats['behaviors'].most_common():
                pct = count / stats['total_records'] * 100
                f.write(f"- {beh}: {count} ({pct:.1f}%)\n")
            f.write("\n")
            
            if stats['issues_count'] > 0:
                f.write("## Issues\n\n")
                for issue in self.validation_results['issues'][:20]:  # First 20
                    f.write(f"- **{issue['type']}**: {issue}\n")
                f.write("\n")
            
            if stats['warnings_count'] > 0:
                f.write("## Warnings\n\n")
                for warning in self.validation_results['warnings']:
                    f.write(f"- **{warning['type']}**: {warning}\n")
                f.write("\n")
        
        print(f"✓ Saved Markdown report: {md_file}")
    
    def run_validation(self, output_dir: Path):
        """Run all validation checks"""
        print("="*70)
        print("PHASE 6F.2: DATASET VALIDATION")
        print("="*70)
        
        self.load_dataset()
        self.validate_structure()
        self.validate_duplicates()
        self.validate_scope_labels()
        self.validate_response_diversity()
        self.validate_python_refusals()
        self.validate_interoperability()
        self.validate_redirect_responses()
        self.generate_report(output_dir)
        
        print("\n" + "="*70)
        print("VALIDATION COMPLETE")
        print("="*70)
        print(f"\nTotal Issues: {len(self.validation_results['issues'])}")
        print(f"Total Warnings: {len(self.validation_results['warnings'])}")
        
        if len(self.validation_results['issues']) == 0:
            print("\n✅ No critical issues found!")
        else:
            print("\n⚠️ Review issues before using dataset")


def main():
    dataset_path = "datasets/phase6e/generated/training_candidate.jsonl"
    output_dir = Path("reports")
    
    validator = DatasetValidator(dataset_path)
    validator.run_validation(output_dir)
    
    print("\n✓ Validation reports saved to reports/")


if __name__ == "__main__":
    main()
