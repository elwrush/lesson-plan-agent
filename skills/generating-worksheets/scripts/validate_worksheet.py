"""
Worksheet HTML Validator
Checks worksheet content fragments for compliance with generating-worksheets skill requirements.

Usage: python validate_worksheet.py <worksheet.html>
"""

import sys
import re
from pathlib import Path

class WorksheetValidator:
    def __init__(self, html_content, filename=""):
        self.html = html_content
        self.filename = filename
        self.errors = []
        self.warnings = []
    
    def validate(self):
        """Run all validation checks."""
        self._check_single_column()
        self._check_page_break_before_answers()
        self._check_orphan_prevention_css()
        self._check_duplicate_headers()
        self._check_page_break_placement()
        
        return len(self.errors) == 0
    
    def _check_single_column(self):
        """Check for two-column layout CSS which is forbidden."""
        two_col_patterns = [
            r'column-count\s*:\s*2',
            r'columns\s*:\s*2',
            r'display\s*:\s*flex.*flex-wrap',
            r'display\s*:\s*grid.*grid-template-columns'
        ]
        
        for pattern in two_col_patterns:
            if re.search(pattern, self.html, re.IGNORECASE):
                self.errors.append(
                    "❌ Two-column layout CSS detected. Per skill requirements, "
                    "worksheet text must ALWAYS flow in a single column."
                )
                break
    
    def _check_page_break_before_answers(self):
        """Verify mandatory page break before Answer Key section."""
        # Find Answer Key section
        answer_key_match = re.search(
            r'(class=["\']answer-key["\']|>Answer Key<|>ANSWER KEY<)',
            self.html,
            re.IGNORECASE
        )
        
        if answer_key_match:
            # Look for page-break div in the 500 chars before Answer Key
            position = answer_key_match.start()
            preceding_html = self.html[max(0, position-500):position]
            
            if not re.search(r'class=["\']page-break["\']', preceding_html, re.IGNORECASE):
                self.errors.append(
                    "❌ CRITICAL: No page break found before Answer Key section. "
                    "Per skill requirements, Answer Key MUST start on a new page. "
                    "Add: <div class=\"page-break\">&nbsp;</div>"
                )
    
    def _check_orphan_prevention_css(self):
        """Check for required orphan prevention CSS rules."""
        required_rules = [
            ('table.*break-inside', 'table { break-inside: auto; }'),
            ('tr.*break-inside', 'tr { break-inside: avoid; }'),
            ('thead.*display.*table-header-group', 'thead { display: table-header-group; }'),
        ]
        
        missing_rules = []
        for pattern, rule in required_rules:
            if not re.search(pattern, self.html, re.IGNORECASE | re.DOTALL):
                missing_rules.append(rule)
        
        if missing_rules:
            self.warnings.append(
                f"⚠️ Missing orphan prevention CSS. Recommended to add:\n   " + 
                "\n   ".join(missing_rules)
            )
    
    def _check_duplicate_headers(self):
        """Check for duplicate header images in content fragments."""
        header_patterns = [
            r'<img[^>]*intensive-header\.jpg',
            r'<img[^>]*bell-header\.jpg',
            r'class=["\']header-img["\']'
        ]
        
        for pattern in header_patterns:
            if re.search(pattern, self.html, re.IGNORECASE):
                self.errors.append(
                    "❌ Content fragment contains header image. "
                    "Headers are provided by the master template. "
                    "Remove the header image from the content fragment."
                )
                break
    
    def _check_page_break_placement(self):
        """Check for poorly placed page breaks."""
        # Page break inside a paragraph
        if re.search(r'<p[^>]*>.*<div class=["\']page-break["\'].*</p>', self.html, re.DOTALL):
            self.warnings.append(
                "⚠️ Page break found inside a paragraph. Move to between paragraphs."
            )
        
        # Page break inside a table
        if re.search(r'<table[^>]*>.*<div class=["\']page-break["\'].*</table>', self.html, re.DOTALL):
            self.warnings.append(
                "⚠️ Page break found inside a table. Move to before or after the table."
            )
    
    def print_report(self):
        """Print validation report."""
        print("\n" + "="*60)
        print("WORKSHEET VALIDATION REPORT")
        if self.filename:
            print(f"File: {self.filename}")
        print("="*60 + "\n")
        
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
    """Validate an HTML worksheet file."""
    path = Path(filepath)
    with open(path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    validator = WorksheetValidator(html_content, path.name)
    is_valid = validator.validate()
    validator.print_report()
    
    return is_valid


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_worksheet.py <worksheet.html>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    is_valid = validate_file(filepath)
    
    sys.exit(0 if is_valid else 1)
