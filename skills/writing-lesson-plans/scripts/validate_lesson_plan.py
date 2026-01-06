"""
Lesson Plan Validator
Checks lesson plan HTML for compliance with writing-lesson-plans skill requirements.

Usage: python validate_lesson_plan.py <lesson_plan.html>
"""

import sys
import re
import os
from pathlib import Path

# Add project root for YAML library
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import yaml
except ImportError:
    yaml = None

class LessonPlanValidator:
    def __init__(self, html_content, filename=""):
        self.html = html_content
        self.filename = filename
        self.errors = []
        self.warnings = []
        self.metadata = self._extract_metadata()
    
    def _extract_metadata(self):
        """Extract lesson metadata from HTML."""
        metadata = {}
        
        # Duration
        duration_match = re.search(r'Duration.*?(\d+)\s*minutes', self.html, re.IGNORECASE)
        if duration_match:
            metadata['duration'] = int(duration_match.group(1))
        
        # Shape (look for Shape letter in filename or content)
        shape_match = re.search(r'Shape\s+([A-J])', self.html, re.IGNORECASE)
        if shape_match:
            metadata['shape'] = shape_match.group(1).upper()
        elif self.filename:
            shape_match = re.search(r'Shape\s*([A-J])', self.filename, re.IGNORECASE)
            if shape_match:
                metadata['shape'] = shape_match.group(1).upper()
        
        # CEFR Level
        cefr_match = re.search(r'CEFR.*?(A1|A2|B1|B2|C1|C2)', self.html, re.IGNORECASE)
        if cefr_match:
            metadata['cefr'] = cefr_match.group(1).upper()
        
        return metadata
    
    def validate(self):
        """Run all validation checks."""
        self._check_timing()
        self._check_preteach_vocabulary()
        self._check_answer_key()
        self._check_thai_scaffolding()
        self._check_stage_structure()
        
        return len(self.errors) == 0
    
    def _check_timing(self):
        """Verify stage times add up to total duration."""
        # Look for time values in table cells that appear to be timing
        # Focus on cells with just numbers that are likely time values
        # Pattern: look for rows with Time column values
        time_cells = re.findall(
            r'<td[^>]*style="[^"]*text-align:\s*center[^"]*"[^>]*>\s*(\d{1,2})\s*</td>',
            self.html,
            re.IGNORECASE
        )
        
        if time_cells:
            # Filter to reasonable time values (1-20 minutes per stage)
            stage_times = [int(t) for t in time_cells if 1 <= int(t) <= 20]
            
            if stage_times:
                total = sum(stage_times)
                expected = self.metadata.get('duration', 0)
                
                if expected and abs(total - expected) > 2:  # Allow 2 min tolerance
                    self.warnings.append(
                        f"⚠️ Timing check: Detected stage times sum to {total} minutes, "
                        f"lesson duration is {expected} minutes. Verify manually."
                    )
                
                # Check for single stage > 40%
                if expected:
                    for t in stage_times:
                        if t > expected * 0.4:
                            self.warnings.append(
                                f"⚠️ Stage with {t} minutes is over 40% of total lesson time. "
                                f"Consider breaking into smaller stages."
                            )
    
    def _check_preteach_vocabulary(self):
        """Verify pre-teach vocabulary stage for receptive skills shapes."""
        shape = self.metadata.get('shape', '')
        
        # Shapes E, F, G, H require pre-teach vocabulary
        if shape in ['E', 'F', 'G', 'H']:
            vocab_patterns = [
                r'pre-?teach.*vocab',
                r'vocabulary.*stage',
                r'key.*vocabulary',
                r'blocking.*vocab'
            ]
            
            has_vocab_stage = any(
                re.search(p, self.html, re.IGNORECASE) 
                for p in vocab_patterns
            )
            
            if not has_vocab_stage:
                self.errors.append(
                    f"❌ Shape {shape} requires a Pre-teach Vocabulary stage, but none detected. "
                    f"Add vocabulary pre-teaching before the main reading/listening."
                )
    
    def _check_answer_key(self):
        """Check for Answer Key if lesson contains exercises."""
        # Look for task/question/exercise indicators
        has_exercises = re.search(
            r'(task:|exercise|fill in|complete the|answer the)',
            self.html,
            re.IGNORECASE
        )
        
        has_answer_key = re.search(
            r'(answer key|answer sheet|answers:)',
            self.html,
            re.IGNORECASE
        )
        
        if has_exercises and not has_answer_key:
            self.warnings.append(
                "⚠️ Lesson contains exercises/tasks but no Answer Key detected. "
                "Consider adding an Answer Key section."
            )
    
    def _check_thai_scaffolding(self):
        """Verify Thai translations in vocabulary sections."""
        # Check if there's a vocabulary section
        vocab_section = re.search(
            r'(vocabulary|vocab|คำศัพท์).*?(?=<h|$)',
            self.html,
            re.IGNORECASE | re.DOTALL
        )
        
        if vocab_section:
            section_text = vocab_section.group(0)
            
            # Check for Thai script (Unicode range for Thai)
            has_thai = re.search(r'[\u0E00-\u0E7F]', section_text)
            
            if not has_thai:
                self.errors.append(
                    "❌ Vocabulary section detected but no Thai translations found. "
                    "Thai scaffolding is required for vocabulary items."
                )
    
    def _check_stage_structure(self):
        """Check for proper stage headers."""
        stage_headers = re.findall(
            r'STAGE\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|[1-8])',
            self.html,
            re.IGNORECASE
        )
        
        if len(stage_headers) < 2:
            self.warnings.append(
                "⚠️ Only {0} stage header(s) detected. Most lesson shapes require 3+ stages. "
                "Check that stage headers follow format: STAGE ONE: [Name]".format(len(stage_headers))
            )
    
    def print_report(self):
        """Print validation report."""
        print("\n" + "="*60)
        print("LESSON PLAN VALIDATION REPORT")
        if self.filename:
            print(f"File: {self.filename}")
        print("="*60 + "\n")
        
        # Print detected metadata
        print("Detected Metadata:")
        print(f"  Shape: {self.metadata.get('shape', 'Not detected')}")
        print(f"  Duration: {self.metadata.get('duration', 'Not detected')} minutes")
        print(f"  CEFR: {self.metadata.get('cefr', 'Not detected')}")
        print()
        
        if self.errors:
            print("🚫 VALIDATION FAILED\n")
            for error in self.errors:
                print(error)
                print()
        else:
            print("✅ VALIDATION PASSED\n")
        
        if self.warnings:
            print("⚠️ WARNINGS:\n")
            for warning in self.warnings:
                print(warning)
                print()
        
        print("="*60 + "\n")


def validate_file(filepath):
    """Validate an HTML lesson plan file."""
    path = Path(filepath)
    with open(path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    validator = LessonPlanValidator(html_content, path.name)
    is_valid = validator.validate()
    validator.print_report()
    
    return is_valid


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_lesson_plan.py <lesson_plan.html>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    is_valid = validate_file(filepath)
    
    sys.exit(0 if is_valid else 1)
