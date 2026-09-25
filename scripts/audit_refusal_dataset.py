"""
Phase 6D: Comprehensive Refusal Dataset Quality Audit
Analyzes existing training data to identify refusal quality issues
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Any

class RefusalDatasetAuditor:
    """Comprehensive auditor for refusal dataset quality"""
    
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        self.records = []
        self.refusal_records = []
        self.python_records = []
        self.statistics = {}
        
        # Known refusal response from prepare_data.py
        self.known_refusal_response = "I am a lightweight AI designed exclusively for Python programming. I cannot answer this."
        
        # Suspicious fragments from Phase 5 testing
        self.suspicious_fragments = [
            "globals", "LoadScene", "zoekt", "/apache", 
            "Assistant", "zilla", "ologist", "countertops"
        ]
        
    def load_dataset(self) -> Dict[str, Any]:
        """Load and validate dataset structure"""
        print(f"Loading dataset from: {self.dataset_path}")
        
        stats = {
            'total_lines': 0,
            'valid_records': 0,
            'malformed_records': 0,
            'empty_records': 0,
            'parse_errors': []
        }
        
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                stats['total_lines'] += 1
                
                # Skip empty lines
                if not line.strip():
                    stats['empty_records'] += 1
                    continue
                
                try:
                    record = json.loads(line)
                    
                    # Validate required fields
                    if 'instruction' in record and 'output' in record:
                        record['_line_num'] = line_num
                        self.records.append(record)
                        stats['valid_records'] += 1
                    else:
                        stats['malformed_records'] += 1
                        stats['parse_errors'].append({
                            'line': line_num,
                            'error': 'Missing required fields',
                            'record': record
                        })
                        
                except json.JSONDecodeError as e:
                    stats['malformed_records'] += 1
                    stats['parse_errors'].append({
                        'line': line_num,
                        'error': str(e),
                        'content': line[:100]
                    })
        
        self.statistics['loading'] = stats
        print(f"✓ Loaded {stats['valid_records']:,} valid records")
        print(f"⚠ Found {stats['malformed_records']} malformed records")
        print(f"⚠ Found {stats['empty_records']} empty lines")
        
        return stats
    
    def separate_refusal_and_python(self):
        """Separate refusal examples from Python examples"""
        print("\nSeparating refusal and Python records...")
        
        for record in self.records:
            output = record.get('output', '').strip()
            
            # Check if this is a refusal (exact match or similar)
            if self.known_refusal_response in output or \
               "cannot answer" in output.lower() or \
               "exclusively for Python" in output or \
               "designed for Python" in output.lower() or \
               ("python" in output.lower() and "cannot" in output.lower()):
                self.refusal_records.append(record)
            else:
                self.python_records.append(record)
        
        print(f"✓ Identified {len(self.refusal_records):,} refusal records")
        print(f"✓ Identified {len(self.python_records):,} Python records")
        
        self.statistics['separation'] = {
            'refusal_count': len(self.refusal_records),
            'python_count': len(self.python_records),
            'refusal_percentage': round(len(self.refusal_records) / len(self.records) * 100, 2)
        }
    
    def analyze_duplicates(self) -> Dict[str, Any]:
        """Analyze duplicate instructions and responses"""
        print("\nAnalyzing duplicates...")
        
        # For refusal records only
        instructions = [r.get('instruction', '') for r in self.refusal_records]
        outputs = [r.get('output', '') for r in self.refusal_records]
        
        instruction_counter = Counter(instructions)
        output_counter = Counter(outputs)
        
        # Find instruction-output pairs
        pairs = [(r.get('instruction', ''), r.get('output', '')) for r in self.refusal_records]
        pair_counter = Counter(pairs)
        
        stats = {
            'unique_instructions': len(instruction_counter),
            'duplicate_instructions': sum(1 for c in instruction_counter.values() if c > 1),
            'unique_outputs': len(output_counter),
            'duplicate_outputs': sum(1 for c in output_counter.values() if c > 1),
            'unique_pairs': len(pair_counter),
            'most_common_instructions': instruction_counter.most_common(10),
            'most_common_outputs': output_counter.most_common(10),
            'most_common_pairs': pair_counter.most_common(5)
        }
        
        print(f"✓ Unique instructions: {stats['unique_instructions']:,}")
        print(f"✓ Duplicate instructions: {stats['duplicate_instructions']:,}")
        print(f"✓ Unique outputs: {stats['unique_outputs']}")
        print(f"✓ Unique pairs: {stats['unique_pairs']:,}")
        
        self.statistics['duplicates'] = stats
        return stats
    
    def classify_refusal_records(self) -> Dict[str, List[Dict]]:
        """Classify each refusal record"""
        print("\nClassifying refusal records...")
        
        classifications = {
            'correct_refusal': [],
            'incorrect_refusal': [],
            'incorrect_answer': [],
            'ambiguous_scope': [],
            'malformed': [],
            'low_quality': [],
            'manual_review': []
        }
        
        # Keywords that indicate Python relevance
        python_keywords = [
            'python', 'pip', 'django', 'flask', 'numpy', 'pandas',
            'jupyter', 'anaconda', 'pypi', 'virtualenv', 'pytest',
            'asyncio', 'requests', 'beautifulsoup', 'scrapy'
        ]
        
        # Keywords for programming interoperability (should generally answer)
        interop_keywords = [
            'api', 'rest', 'json', 'xml', 'database', 'sql',
            'integrate', 'connect', 'call', 'interface', 'library'
        ]
        
        # Programming languages (should refuse unless Python interop context)
        other_languages = [
            'java', 'javascript', 'c++', 'c#', 'ruby', 'php',
            'go', 'rust', 'kotlin', 'swift', 'typescript'
        ]
        
        for record in self.refusal_records:
            instruction = record.get('instruction', '').lower()
            output = record.get('output', '').lower()
            
            # Check if output is actually a refusal
            is_refusal_output = any(phrase in output for phrase in [
                'cannot answer', 'exclusively for python', 
                'designed for python', "can't help"
            ])
            
            # Classify
            if not is_refusal_output:
                # Output is not a refusal - this is wrong!
                classifications['incorrect_answer'].append({
                    'record': record,
                    'reason': 'Output provides answer instead of refusing'
                })
            
            elif any(kw in instruction for kw in python_keywords):
                # Instruction mentions Python - should probably answer, not refuse
                if any(kw in instruction for kw in interop_keywords):
                    # Has interop context - definitely should answer
                    classifications['incorrect_refusal'].append({
                        'record': record,
                        'reason': 'Python interoperability question incorrectly refused'
                    })
                else:
                    # Ambiguous - might be asking about Python specifically
                    classifications['manual_review'].append({
                        'record': record,
                        'reason': 'Mentions Python - review if should be answered'
                    })
            
            elif any(lang in instruction for lang in other_languages):
                # Mentions other language
                if any(kw in instruction for kw in interop_keywords + python_keywords):
                    # Has Python interop context
                    classifications['ambiguous_scope'].append({
                        'record': record,
                        'reason': 'Language comparison or interop - needs scope policy'
                    })
                else:
                    # Pure other-language request - correct refusal
                    classifications['correct_refusal'].append({
                        'record': record,
                        'reason': 'Non-Python programming request'
                    })
            
            elif len(instruction) < 10:
                # Too short - probably malformed
                classifications['malformed'].append({
                    'record': record,
                    'reason': 'Instruction too short'
                })
            
            elif output == self.known_refusal_response:
                # Uses template response for non-programming question
                classifications['correct_refusal'].append({
                    'record': record,
                    'reason': 'Non-programming question with standard refusal'
                })
            
            else:
                # Different response - needs review
                classifications['manual_review'].append({
                    'record': record,
                    'reason': 'Non-standard response format'
                })
        
        # Count classifications
        counts = {k: len(v) for k, v in classifications.items()}
        print(f"✓ Correct refusals: {counts['correct_refusal']}")
        print(f"⚠ Incorrect refusals: {counts['incorrect_refusal']}")
        print(f"⚠ Incorrect answers: {counts['incorrect_answer']}")
        print(f"⚠ Ambiguous scope: {counts['ambiguous_scope']}")
        print(f"⚠ Malformed: {counts['malformed']}")
        print(f"⚠ Manual review: {counts['manual_review']}")
        
        self.statistics['classifications'] = counts
        self.classifications = classifications
        
        return classifications
    
    def analyze_response_quality(self) -> Dict[str, Any]:
        """Analyze quality of refusal responses"""
        print("\nAnalyzing response quality...")
        
        stats = {
            'response_lengths': [],
            'responses_with_fragments': [],
            'repeated_ngrams': defaultdict(int),
            'response_templates': Counter(),
            'multi_turn_responses': []
        }
        
        for record in self.refusal_records:
            output = record.get('output', '')
            
            # Length
            stats['response_lengths'].append(len(output))
            
            # Check for suspicious fragments
            for fragment in self.suspicious_fragments:
                if fragment.lower() in output.lower():
                    stats['responses_with_fragments'].append({
                        'record': record,
                        'fragment': fragment
                    })
            
            # Count exact response templates
            stats['response_templates'][output] += 1
            
            # Check for multi-turn (multiple "Assistant:" or similar)
            if output.count('Assistant') > 1 or output.count('User:') > 0:
                stats['multi_turn_responses'].append(record)
        
        # Calculate statistics
        if stats['response_lengths']:
            stats['avg_response_length'] = sum(stats['response_lengths']) / len(stats['response_lengths'])
            stats['min_response_length'] = min(stats['response_lengths'])
            stats['max_response_length'] = max(stats['response_lengths'])
        
        stats['fragment_count'] = len(stats['responses_with_fragments'])
        stats['multi_turn_count'] = len(stats['multi_turn_responses'])
        stats['top_templates'] = stats['response_templates'].most_common(10)
        
        print(f"✓ Average response length: {stats.get('avg_response_length', 0):.1f} chars")
        print(f"⚠ Responses with suspicious fragments: {stats['fragment_count']}")
        print(f"⚠ Multi-turn responses: {stats['multi_turn_count']}")
        print(f"✓ Unique response templates: {len(stats['response_templates'])}")
        
        self.statistics['quality'] = stats
        return stats
    
    def check_format_compatibility(self) -> Dict[str, Any]:
        """Check training format compatibility"""
        print("\nChecking format compatibility...")
        
        stats = {
            'records_with_empty_input': 0,
            'records_with_nonempty_input': 0,
            'instructions_with_newlines': 0,
            'outputs_with_newlines': 0,
            'very_long_instructions': [],
            'very_long_outputs': []
        }
        
        for record in self.refusal_records:
            instruction = record.get('instruction', '')
            input_text = record.get('input', '')
            output = record.get('output', '')
            
            # Input field usage
            if input_text.strip():
                stats['records_with_nonempty_input'] += 1
            else:
                stats['records_with_empty_input'] += 1
            
            # Newline checks
            if '\n' in instruction:
                stats['instructions_with_newlines'] += 1
            if '\n' in output:
                stats['outputs_with_newlines'] += 1
            
            # Length checks (>1000 chars might be truncated during training)
            if len(instruction) > 1000:
                stats['very_long_instructions'].append(record)
            if len(output) > 1000:
                stats['very_long_outputs'].append(record)
        
        print(f"✓ Records with empty input field: {stats['records_with_empty_input']}")
        print(f"✓ Records with non-empty input: {stats['records_with_nonempty_input']}")
        print(f"⚠ Instructions with newlines: {stats['instructions_with_newlines']}")
        print(f"⚠ Outputs with newlines: {stats['outputs_with_newlines']}")
        print(f"⚠ Very long instructions (>1000 chars): {len(stats['very_long_instructions'])}")
        
        self.statistics['format'] = stats
        return stats
    
    def find_contradictions(self) -> List[Dict]:
        """Find contradictory examples"""
        print("\nSearching for contradictions...")
        
        contradictions = []
        
        # Group Python records by similar instructions
        # (simplified - check for same programming task requested in different languages)
        
        # Check if any refusal instruction appears in Python dataset
        refusal_instructions = set(r.get('instruction', '').lower() for r in self.refusal_records)
        python_instructions = set(r.get('instruction', '').lower() for r in self.python_records)
        
        # Exact duplicates between refusal and Python
        exact_overlaps = refusal_instructions & python_instructions
        
        if exact_overlaps:
            print(f"⚠ Found {len(exact_overlaps)} identical instructions in both refusal and Python datasets!")
            for inst in list(exact_overlaps)[:5]:  # Show first 5
                contradictions.append({
                    'type': 'exact_duplicate',
                    'instruction': inst,
                    'issue': 'Same instruction appears in both refusal and Python datasets'
                })
        else:
            print("✓ No exact duplicates between refusal and Python datasets")
        
        self.statistics['contradictions'] = {
            'count': len(contradictions),
            'contradictions': contradictions
        }
        
        return contradictions
    
    def generate_sample_outputs(self, output_dir: Path):
        """Generate sample files for manual inspection"""
        print(f"\nGenerating sample outputs in {output_dir}...")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Sample 30 refusal records for inspection
        sample_size = min(30, len(self.refusal_records))
        samples = self.refusal_records[:sample_size]
        
        with open(output_dir / 'refusal_samples.json', 'w', encoding='utf-8') as f:
            json.dump(samples, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved {sample_size} sample refusal records")
        
        # Save classification results
        for category, records in self.classifications.items():
            if records:
                filename = output_dir / f'{category}.jsonl'
                with open(filename, 'w', encoding='utf-8') as f:
                    for item in records[:50]:  # Max 50 per category
                        f.write(json.dumps(item, ensure_ascii=False) + '\n')
                print(f"✓ Saved {min(len(records), 50)} {category} examples")
    
    def save_statistics(self, output_dir: Path):
        """Save all statistics to JSON and Markdown"""
        print(f"\nSaving statistics to {output_dir}...")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON
        json_file = output_dir / 'phase6d_dataset_statistics.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.statistics, f, indent=2, ensure_ascii=False, default=str)
        print(f"✓ Saved statistics JSON: {json_file}")
        
        # Save Markdown summary
        md_file = output_dir / 'phase6d_dataset_statistics.md'
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# Phase 6D: Dataset Statistics\n\n")
            f.write(f"**Dataset**: {self.dataset_path}\n\n")
            f.write("## Loading Statistics\n\n")
            loading = self.statistics.get('loading', {})
            f.write(f"- Total lines: {loading.get('total_lines', 0):,}\n")
            f.write(f"- Valid records: {loading.get('valid_records', 0):,}\n")
            f.write(f"- Malformed records: {loading.get('malformed_records', 0)}\n")
            f.write(f"- Empty records: {loading.get('empty_records', 0)}\n\n")
            
            f.write("## Dataset Composition\n\n")
            sep = self.statistics.get('separation', {})
            f.write(f"- Refusal records: {sep.get('refusal_count', 0):,}\n")
            f.write(f"- Python records: {sep.get('python_count', 0):,}\n")
            f.write(f"- Refusal percentage: {sep.get('refusal_percentage', 0)}%\n\n")
            
            f.write("## Classification Results\n\n")
            classifications = self.statistics.get('classifications', {})
            for category, count in classifications.items():
                f.write(f"- {category.replace('_', ' ').title()}: {count}\n")
            f.write("\n")
            
            f.write("## Duplicate Analysis\n\n")
            dups = self.statistics.get('duplicates', {})
            f.write(f"- Unique instructions: {dups.get('unique_instructions', 0):,}\n")
            f.write(f"- Duplicate instructions: {dups.get('duplicate_instructions', 0):,}\n")
            f.write(f"- Unique outputs: {dups.get('unique_outputs', 0)}\n")
            f.write(f"- Unique instruction-output pairs: {dups.get('unique_pairs', 0):,}\n\n")
            
            f.write("## Response Quality\n\n")
            quality = self.statistics.get('quality', {})
            f.write(f"- Average response length: {quality.get('avg_response_length', 0):.1f} characters\n")
            f.write(f"- Responses with suspicious fragments: {quality.get('fragment_count', 0)}\n")
            f.write(f"- Multi-turn responses: {quality.get('multi_turn_count', 0)}\n")
            f.write(f"- Unique response templates: {len(quality.get('response_templates', {}))}\n\n")
            
        print(f"✓ Saved statistics Markdown: {md_file}")
    
    def run_full_audit(self, output_dir: Path):
        """Run complete audit pipeline"""
        print("="*70)
        print("PHASE 6D: COMPREHENSIVE REFUSAL DATASET AUDIT")
        print("="*70)
        
        # Phase 1: Load dataset
        self.load_dataset()
        
        # Phase 2: Separate refusal and Python
        self.separate_refusal_and_python()
        
        # Phase 3: Analyze duplicates
        self.analyze_duplicates()
        
        # Phase 4: Classify records
        self.classify_refusal_records()
        
        # Phase 5: Analyze quality
        self.analyze_response_quality()
        
        # Phase 6: Check format
        self.check_format_compatibility()
        
        # Phase 7: Find contradictions
        self.find_contradictions()
        
        # Phase 8: Generate outputs
        self.generate_sample_outputs(output_dir)
        
        # Phase 9: Save statistics
        self.save_statistics(output_dir)
        
        print("\n" + "="*70)
        print("AUDIT COMPLETE")
        print("="*70)
        print(f"\nResults saved to: {output_dir}")
        print("\nNext: Review the generated reports and samples")


if __name__ == "__main__":
    # Configuration
    dataset_path = "data/training_data.jsonl"
    output_dir = Path("reports/phase6d_audit")
    
    # Run audit
    auditor = RefusalDatasetAuditor(dataset_path)
    auditor.run_full_audit(output_dir)
    
    print("\n✓ Phase 6D audit complete!")
    print("✓ Review reports/phase6d_audit/ for detailed results")
