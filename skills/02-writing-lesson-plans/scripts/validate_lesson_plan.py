import sys
import re
import os
from pathlib import Path

# Add project root for pathing
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

def load_approved_stages():
    """Dynamically loads APPROVED_STAGES from REFERENCE.py."""
    try:
        # Assuming script is in skills/02-writing-lesson-plans/scripts/
        reference_path = Path(__file__).parent.parent / "REFERENCE.py"
        if not reference_path.exists():
            return set()
            
        namespace = {}
        with open(reference_path, 'r', encoding='utf-8') as f:
            exec(f.read(), namespace)
        return namespace.get('APPROVED_STAGES', set())
    except Exception:
        return set()

APPROVED_STAGES = load_approved_stages()

class LessonPlanValidator:
    def __init__(self, content, filename=""):
        self.filename = filename
        self.content = content
        self.errors = []
        self.warnings = []
        self.metadata = self._extract_metadata()
        self.stages = self._extract_stages()
    
    def _extract_metadata(self):
        """Extract lesson metadata from Typst file using modern_template keys."""
        metadata = {}
        # Keys to match: topic, date, week, classes, level, shape, sb, wb, resources, slides_url
        keys = ['topic', 'date', 'week', 'classes', 'level', 'shape', 'sb', 'wb', 'resources', 'slides_url']
        for key in keys:
            match = re.search(fr'{key}:\s*"(.*?)"', self.content, re.IGNORECASE)
            if match:
                metadata[key] = match.group(1).strip()
        
        # Special check for lesson_aim (often doesn't use quotes for multi-line but we try to find it)
        aim_match = re.search(r'lesson_aim:\s*"(.*?)"', self.content, re.DOTALL | re.IGNORECASE)
        if aim_match:
            metadata['lesson_aim'] = aim_match.group(1).strip()
            
        return metadata

    def _extract_stages(self):
        """Extract stage data from modern_template stage(aim, proc, interaction) calls."""
        stages = []
        # Pattern: stage([aim], [proc], [interaction])
        # Simple non-greedy pattern that captures content between square brackets
        stage_pattern = re.compile(
            r'stage\s*\(\s*\[(.*?)\],\s*\[(.*?)\],\s*\[(.*?)\]',
            re.DOTALL | re.IGNORECASE
        )
        
        matches = stage_pattern.findall(self.content)
        
        for i, match in enumerate(matches, start=1):
            aim, proc, inter = match
            
            stages.append({
                'number':     str(i),
                'aim':        aim.strip(),
                'procedure':  proc.strip(),
                'interaction': inter.strip(),
                'char_count': len(proc.strip()),
                'word_count': len(re.findall(r'\w+', proc.strip())),
            })
        return stages

    def validate(self):
        """Run all validation checks."""
        # 1. Structural Checks (Hard Errors)
        self._check_required_components()
        self._check_blueprint_gate()
        self._check_banned_language()
        self._check_metadata_completeness()

        # 2. Pedagogical & Naming Checks (Soft Warnings/Advisories)
        self._check_procedural_density()
        self._check_interaction_markers()
        self._check_aim_quality()
        self._check_stage_names()
        
        return len(self.errors) == 0

    def _check_required_components(self):
        """[HARD ERROR] Ensure core components of modern_template are present."""
        required = {
            'modern_template import': r'#import\s*"/templates/modern_template.typ":\s*modern_template,\s*stage',
            '#show: rule':               r'#show:\s*modern_template\.with',
            'stages: parameter':         r'stages\s*:\s*\(',
        }
        for label, pattern in required.items():
            if not re.search(pattern, self.content, re.IGNORECASE):
                self.errors.append(f"[ERROR] Missing required structure — {label}. Check SKILL.md for the correct snippet.")

    def _check_blueprint_gate(self):
        """[HARD ERROR] Ensure blueprint exists and is approved."""
        if not self.filename: return
        file_path = Path(self.filename)
        # Handle cases where path is relative to current directory
        if not file_path.is_absolute():
            file_path = Path.cwd() / file_path
            
        lesson_dir = file_path.parent
            
        blueprint_path = lesson_dir / "lesson_plan_blueprint.md"
        if not blueprint_path.exists():
            self.errors.append(f"[ERROR] Blueprint Gate Failed: 'lesson_plan_blueprint.md' missing in {lesson_dir}.")
        else:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                bp_content = f.read()
                if "[APPROVED]" not in bp_content and "User Approval: YES" not in bp_content:
                    self.errors.append("[ERROR] Blueprint is not approved. Add '[APPROVED]' to the blueprint file.")

    def _check_metadata_completeness(self):
        """[HARD ERROR] Ensure all major metadata fields are provided."""
        critical_keys = ['topic', 'level', 'shape', 'lesson_aim']
        for key in critical_keys:
            if key not in self.metadata or not self.metadata[key]:
                # lesson_aim is extracted separately above, but if still missing check if it's in content at all
                if key == 'lesson_aim' and 'lesson_aim:' in self.content:
                    continue
                self.errors.append(f"[ERROR] Missing metadata field: '{key}'")

    def _check_banned_language(self):
        """[HARD ERROR] Prevent references to slide numbers or legacy terms."""
        banned = [
            (r'Slide\s*\d+', "Do not refer to specific slide numbers (e.g., 'Slide 4')."),
            (r'bell_header', "Legacy function 'bell_header' is banned."),
            (r'intensive_header', "Legacy function 'intensive_header' is banned in LPs."),
            (r'differentiation_box', "Legacy function 'differentiation_box' is banned.")
        ]
        for pattern, reason in banned:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.errors.append(f"[ERROR] Banned language/logic found: {reason}")

    def _check_procedural_density(self):
        """[ADVISORY] Check for professional depth in procedures."""
        if not self.stages:
            self.errors.append("[ERROR] No stages found! Ensure you use stage(aim, proc, interaction) inside the stages array.")
            return

        MIN_CHARS = 150
        for stage in self.stages:
            if stage['char_count'] < MIN_CHARS:
                self.warnings.append(f"[DENSITY] Stage {stage['number']} procedure is thin ({stage['char_count']} chars). Add more pedagogical detail.")

    def _check_interaction_markers(self):
        """[ADVISORY] Ensure interaction markers (T-Ss, etc.) are present in prose."""
        markers = r'(T-Ss|Ss-Ss|Pairs|Group|Elicit|CCQ|Class|Individually)'
        for stage in self.stages:
            if not re.search(markers, stage['procedure'], re.IGNORECASE):
                self.warnings.append(f"[PEDAGOGY] Stage {stage['number']} lacks interaction/management cues (Pairs, Elicit, etc.).")

    def _check_aim_quality(self):
        """[ADVISORY] Aims should start with 'To...'."""
        for stage in self.stages:
            if not stage['aim'].lower().startswith('to '):
                self.warnings.append(f"[STYLE] Stage {stage['number']} aim should start with 'To...' (e.g., 'To activate schemata').")

    def _check_stage_names(self):
        """[ADVISORY] Use standard stage names from REFERENCE.py."""
        # This is harder now because 'aim' is the first arg, not 'name'.
        # We check if any approved name is present in the aim block.
        if not APPROVED_STAGES: return
        
        for stage in self.stages:
            if not any(name.lower() in stage['aim'].lower() for name in APPROVED_STAGES):
                # If the aim doesn't contain a standard stage name (Lead-in, Gist, etc.)
                self.warnings.append(f"[STYLE] Stage {stage['number']} aim does not mention a standard stage name (e.g., 'Lead-in', 'Gist').")

    def print_report(self):
        """Print validation report."""
        print("\n" + "="*60)
        print("LESSON PLAN VALIDATION REPORT (v2026)")
        print(f"File: {Path(self.filename).name}")
        print("="*60 + "\n")
        
        if self.errors:
            print(f"❌ [FAIL] {len(self.errors)} Blocking Errors Found:\n")
            for err in self.errors: print(f"  - {err}")
        else:
            print("✅ [PASS] No blocking structural errors found.\n")
        
        if self.warnings:
            print(f"⚠️  [ADVISORY] {len(self.warnings)} Quality Suggestions:\n")
            for warn in self.warnings: print(f"  - {warn}")
        
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
