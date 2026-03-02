import sys
import re
import os
from pathlib import Path

# Add project root for pathing
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

class LessonPlanValidator:
    def __init__(self, content, filename=""):
        self.filename = filename
        self.content = content
        self.errors = []
        self.warnings = []
        self.metadata = self._extract_metadata()
        self.stages = self._extract_stages()
    
    def _extract_metadata(self):
        """Extract lesson metadata from Typst file."""
        metadata = {}
        duration_match = re.search(r'duration:\s*"(\d+)\s*Minutes"', self.content, re.IGNORECASE)
        if duration_match:
            metadata['duration'] = int(duration_match.group(1))
        
        shape_match = re.search(r'shape:\s*"([A-J])', self.content, re.IGNORECASE)
        if shape_match:
            metadata['shape'] = shape_match.group(1).upper()
        
        cefr_match = re.search(r'cefr:\s*"([A-C][0-2])', self.content, re.IGNORECASE)
        if cefr_match:
            metadata['cefr'] = cefr_match.group(1).upper()

        return metadata

    def _extract_stages(self):
        """Extract stage procedures from Typst blocks."""
        stages = []
        # Modern format: stage("NUM", "Name", "Time", "Aim", [Procedure], "Pattern")
        stage_pattern = re.compile(r'stage\(\s*"(.*?)"\s*,\s*"(.*?)"\s*,\s*"(.*?)"\s*,\s*"(.*?)"\s*,\s*\[(.*?)\]\s*,\s*"(.*?)"\)', re.DOTALL | re.IGNORECASE)
        
        for match in stage_pattern.finditer(self.content):
            stages.append({
                'number': match.group(1).strip(),
                'name': match.group(2).strip(),
                'time': match.group(3).strip(),
                'procedure': match.group(5).strip(),
                'word_count': len(re.findall(r'\w+', match.group(5)))
            })
        
        # Fallback for older formats
        if not stages:
            stage_headers = re.finditer(r'stage\(\s*"(.*?)"\s*,\s*"(.*?)"', self.content, re.IGNORECASE)
            for match in stage_headers:
                stages.append({'name': match.group(2).strip(), 'procedure': "", 'word_count': 0})

        return stages

    def validate(self):
        """Run all validation checks."""
        # 1. Structural Checks (Hard Errors)
        self._check_required_components()
        self._check_blueprint_gate()
        self._check_timing()
        self._check_banned_language()

        # 2. Pedagogical & Naming Checks (Soft Warnings)
        self._check_stage_names()
        self._check_preteach_vocabulary()
        self._check_pedagogical_patterns()
        self._check_procedural_density()
        
        return len(self.errors) == 0

    def _check_required_components(self):
        """[HARD ERROR] Ensure core components are present."""
        required = ["#lesson_header", "#metadata_table", "#main_aim_box", "#stage_table", "#stage"]
        for func in required:
            if func not in self.content:
                self.errors.append(f"[ERROR] Missing required Typst component: {func}")

    def _check_blueprint_gate(self):
        """[HARD ERROR] Ensure a visual_plan.md exists."""
        if not self.filename: return
        file_path = Path(self.filename)
        if not file_path.is_absolute():
            file_path = Path.cwd() / file_path
            
        blueprint_path = file_path.parent / "visual_plan.md"
        if not blueprint_path.exists():
            self.errors.append(f"[ERROR] Blueprint Gate Failed: 'visual_plan.md' missing in {file_path.parent}.")

    def _check_timing(self):
        """[HARD ERROR] Verify stage times add up to total duration."""
        time_vals = []
        for s in self.stages:
            if 'time' in s and s['time'].isdigit():
                time_vals.append(int(s['time']))
        
        if time_vals:
            total = sum(time_vals)
            expected = self.metadata.get('duration', 0)
            if expected and total != expected:
                self.errors.append(f"[ERROR] Timing Mismatch: Sum is {total}m, but metadata says {expected}m.")

    def _check_banned_language(self):
        """[HARD ERROR] Prevent references to slide numbers."""
        for stage in self.stages:
            if re.search(r'Slide\s*\d+', stage['procedure'], re.IGNORECASE):
                self.errors.append(f"[ERROR] Banned Language in '{stage['name']}': Do not refer to slide numbers (e.g., 'Slide 4').")

    def _check_stage_names(self):
        """[SOFT WARNING] Validate stage names against reference."""
        script_dir = Path(__file__).parent
        ref_path = script_dir.parent / "REFERENCE.py"
        try:
            namespace = {}
            with open(ref_path, 'r', encoding='utf-8') as f:
                exec(f.read(), namespace)
            approved = namespace.get('APPROVED_STAGES', set())
        except:
            approved = set()

        for stage in self.stages:
            name = stage['name']
            if approved and name not in approved:
                self.warnings.append(f"[ADVISORY] Non-standard Stage Name: '{name}'. Standard options include: {', '.join(sorted(list(approved))[:5])}...")

    def _check_preteach_vocabulary(self):
        """[SOFT WARNING] Check vocab count for Shape E."""
        shape = self.metadata.get('shape', '')
        if shape == 'E':
            vocab_stage = next((s for s in self.stages if any(kw in s['name'].lower() for kw in ["pre-teach", "vocabulary", "vocab"])), None)
            if vocab_stage:
                # ONLY scan the procedure of the specific vocabulary stage
                # Match items starting with a bullet/number followed by a word in asterisks
                items = re.findall(r'^[ \t]*[-*\d.]+[ \t]+\*(.*?)\*', vocab_stage['procedure'], re.MULTILINE)
                if len(items) != 5:
                    self.warnings.append(f"[PEDAGOGY] Shape E typically requires exactly 5 vocab items. Found {len(items)}: {', '.join(items)}")

    def _check_pedagogical_patterns(self):
        """[SOFT WARNING] Check for 'Gold Standard' markers."""
        shape = self.metadata.get('shape', '')
        if shape == 'E':
            # Lead-in check
            lead_in = next((s for s in self.stages if "lead-in" in s['name'].lower() or "context" in s['name'].lower()), None)
            if lead_in and not any(kw in lead_in['procedure'].lower() for kw in ["quiz", "guess", "vote", "discuss", "truths", "fiction"]):
                self.warnings.append("[PEDAGOGY] Lead-in should be interactive (quiz, guess, etc.).")

            # Gist check
            gist = next((s for s in self.stages if any(kw in s['name'].lower() for kw in ["gist", "scanning", "story"])), None)
            if gist and not any(kw in gist['procedure'].lower() for kw in ["timed", "speed", "scan", "quick", "minutes", "seconds"]):
                self.warnings.append("[PEDAGOGY] Gist task should be timed or speed-based.")

    def _check_procedural_density(self):
        """[SOFT WARNING] Check for detail and interaction markers."""
        for stage in self.stages:
            if len(stage['procedure']) < 100:
                self.warnings.append(f"[DENSITY] Stage '{stage['name']}' procedure seems thin.")
            if not re.search(r'(T-S|S-S|Ss-Ss|Pairs|Group|Elicit)', stage['procedure'], re.IGNORECASE):
                 self.warnings.append(f"[DENSITY] Stage '{stage['name']}' is missing interaction markers.")

    def print_report(self):
        """Print validation report."""
        print("\n" + "="*60)
        print("LESSON PLAN VALIDATION REPORT")
        print(f"File: {self.filename}")
        print("="*60 + "\n")
        
        if self.errors:
            print(f"❌ [FAIL] {len(self.errors)} Blocking Errors Found:\n")
            for err in self.errors: print(f"  {err}")
        else:
            print("✅ [PASS] No blocking structural errors found.\n")
        
        if self.warnings:
            print(f"⚠️  [ADVISORY] {len(self.warnings)} Quality Suggestions:\n")
            for warn in self.warnings: print(f"  {warn}")
        
        print("\n" + "="*60 + "\n")

def validate_file(filepath):
    path = Path(filepath)
    if not path.exists():
        print(f"File not found: {filepath}")
        return False
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    validator = LessonPlanValidator(content, str(path))
    is_valid = validator.validate()
    validator.print_report()
    return is_valid

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_lesson_plan.py <file>")
        sys.exit(1)
    sys.exit(0 if validate_file(sys.argv[1]) else 1)
