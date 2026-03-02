import re
import sys
import os

def load_approved_stages():
    """Dynamically loads APPROVED_STAGES from REFERENCE.py."""
    stages = set()
    try:
        reference_path = os.path.join(os.path.dirname(__file__), '..', 'REFERENCE.py')
        with open(reference_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Execute the code in a specific namespace to capture the variable
        namespace = {}
        exec(code, namespace)
        stages = namespace.get('APPROVED_STAGES', set())
        if not stages:
            print("[WARN] Could not load APPROVED_STAGES from REFERENCE.py")
    except Exception as e:
        print(f"[WARN] Failed to load APPROVED_STAGES: {e}")
    return stages

APPROVED_STAGES = load_approved_stages()

# --- Validation Checks ---

def check_required_functions(content):
    """Checks for the presence of modern, required Typst functions."""
    print("CHECKING for required structural functions...")
    required = [
        "#lesson_header", "#metadata_table", "#main_aim_box",
        "#differentiation_box", "#slideshow_link", "#stage_table", "#stage"
    ]
    errors = []
    for func in required:
        if not re.search(re.escape(func), content):
            errors.append(f"Missing required component call: {func}")
            print(f"  [FAIL] {func}")
        else:
            print(f"  [PASS] {func}")
    return errors

def check_legacy_functions(content):
    """Checks for deprecated legacy functions."""
    print("\nCHECKING for deprecated legacy functions...")
    legacy = ["#stage_row"]
    errors = []
    for func in legacy:
        if re.search(re.escape(func), content):
            errors.append(f"Found deprecated function call: {func}. Please refactor to use the modern '#stage(...)' component inside '#stage_table((...))'.")
            print(f"  [FAIL] Found legacy function: {func}")
        else:
            print(f"  [PASS] No legacy functions found.")
    return errors


def check_slideshow_link_placement(content):
    """Ensures the slideshow link is correctly placed after differentiation and before the stage table."""
    print("\nCHECKING for correct #slideshow_link placement...")
    errors = []
    pattern = re.compile(r'#differentiation_box.*?#slideshow_link.*?#stage_table', re.DOTALL)
    if not pattern.search(content):
        errors.append("Incorrect #slideshow_link placement. It MUST be located after #differentiation_box and before #stage_table.")
        print("  [FAIL] #slideshow_link is in the wrong position.")
    else:
        print("  [PASS] #slideshow_link is correctly placed.")
    return errors

def check_stage_names(content):
    """Validates that all stage names are from the approved list."""
    print("\nCHECKING for valid stage names...")
    errors = []
    found_stages = re.findall(r'stage\(".*?",\s*"(.*?)",', content)
    
    if not found_stages:
        print("  [WARN] No stages found to validate.")
        return errors
        
    print(f"  Found stages: {', '.join(found_stages)}")
    
    for name in found_stages:
        if name not in APPROVED_STAGES:
            errors.append(f"Invalid stage name: '{name}'. Stage names must be from the approved list in REFERENCE.md.")
            print(f"  [FAIL] Invalid stage name: '{name}'")
        else:
            print(f"  [PASS] Valid stage name: '{name}'")
            
    # Check for invented headers like "= Phase X"
    invented_headers = re.findall(r'^=\s*(Phase\s+\d+|Context|Vocabulary|Reading|Analysis)', content, re.MULTILINE)
    if invented_headers:
        for header in invented_headers:
            errors.append(f"Found invented heading: '{header}'. All procedural content must be inside a `stage()` component.")
            print(f"  [FAIL] Found invented heading: '{header}'")
    else:
        print("  [PASS] No invented headings found.")
        
    return errors

# --- Main Execution ---

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_plan_structure.py <path_to_typst_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    all_errors = []
    all_errors.extend(check_required_functions(content))
    all_errors.extend(check_legacy_functions(content))
    all_errors.extend(check_slideshow_link_placement(content))
    all_errors.extend(check_stage_names(content))

    print("\n" + "="*50)
    if not all_errors:
        print("✅ VALIDATION PASSED: Lesson plan structure is compliant.")
        print("="*50)
    else:
        print(f"❌ VALIDATION FAILED: Found {len(all_errors)} structural error(s).")
        print("="*50)
        for i, error in enumerate(all_errors, 1):
            print(f"  {i}. {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
