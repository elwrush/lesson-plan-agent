import json
import sys
import os
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def validate_sequence(json_path):
    print(f"🔍 Validating Sequence: {json_path}")
    
    try:
        from manifest_parser import parse_markdown_manifest
        data = parse_markdown_manifest(sys.argv[1] if len(sys.argv) > 1 else json_path)
    except Exception as e:
        print(f"[ERROR] Error reading manifest: {e}")
        return False

    slides = data.get('slides', [])
    issues = []
    
    for i in range(len(slides) - 1):
        current_layout = slides[i].get('layout', '')
        next_layout = slides[i+1].get('layout', '')
        
        # Rule: Strategy cannot be immediately followed by Segue
        if current_layout == 'strategy' and next_layout == 'segue':
            issues.append(f"[FAIL] Sequencing Violation (Slide {i+1} -> {i+2}): Found 'strategy' followed by 'segue'. Strategy slides must come AFTER the segue.")

    if issues:
        for issue in issues:
            print(issue)
        return False
    
    print("[OK] Sequence Validation Passed: No Strategy->Segue violations found.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_sequence.py <path_to_presentation.json>")
        sys.exit(1)
    
    success = validate_sequence(sys.argv[1])
    sys.exit(0 if success else 1)
