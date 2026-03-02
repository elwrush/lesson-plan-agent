import sys
import re

def validate_density(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # 1. Check for "Part 1", "Part 2" structure (Modeling the YAML density)
    if "Part 1" not in content or "Part 2" not in content:
        print("⚠️ Advisory: The model often uses 'Part 1, Part 2' to build stages for higher density.")
    
    # 2. Check for Classroom Management (Feedback marks)
    if "Feedback" not in content:
        issues.append("❌ Missing Feedback Loops: The model mandates granular feedback (e.g., '1 min. Feedback').")

    if issues:
        for i in issues: print(i)
        return False
    return True

if __name__ == "__main__":
    if not validate_density(sys.argv[1]):
        sys.exit(1)
