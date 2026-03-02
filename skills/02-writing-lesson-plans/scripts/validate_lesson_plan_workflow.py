import argparse
import os
import sys

def check_file_exists(path, description):
    if os.path.exists(path):
        print(f"✅ {description} Found: {path}")
        return True
    else:
        print(f"❌ {description} Missing: {path}")
        return False

def validate_workflow(lesson_folder):
    print(f"🛡️  Validating Lesson Plan Workflow for: {lesson_folder}")
    base_dir = os.path.abspath(os.path.join("inputs", lesson_folder))
    pub_dir = os.path.join(base_dir, "published")
    
    if not os.path.exists(base_dir):
        print(f"❌ Lesson directory not found: {base_dir}")
        sys.exit(1)

    all_passed = True

    # 1. Shape Selection Gate & Typst location check
    typ_files_base = [f for f in os.listdir(base_dir) if f.endswith('.typ')]
    
    typ_files_pub = []
    if os.path.exists(pub_dir):
        typ_files_pub = [f for f in os.listdir(pub_dir) if f.endswith('.typ')]
        
    if typ_files_pub:
        print("❌ CRITICAL: .typ files found in the 'published' directory. They MUST remain in the root directory.")
        all_passed = False
    elif not typ_files_base:
        print("❌ No Typst Lesson Plan found in the root directory. You must complete the Shape Selection and Lesson Planning phase first.")
        all_passed = False
    else:
        print(f"✅ Typst Lesson Plan Found in root: {typ_files_base[0]}")

    # 1.5 PDF Existence Check (Must be in published/)
    pdf_paths = []
    if os.path.exists(pub_dir):
        pdf_paths = [os.path.join(pub_dir, f) for f in os.listdir(pub_dir) if f.endswith('.pdf')]

    if not pdf_paths:
        print("❌ Compiled Lesson Plan PDF missing in the 'published/' directory.")
        all_passed = False
    else:
        print(f"✅ Compiled Lesson Plan PDF Found in 'published/'.")

    # 2. Visual Roadmap Gate
    roadmap_paths = [
        os.path.join(base_dir, "visual_plan.md"),
        os.path.join(base_dir, "published", "visual_plan.md")
    ]
    found_roadmap = any(os.path.exists(p) for p in roadmap_paths)
    if not found_roadmap:
        print("❌ CRITICAL: Visual Roadmap missing. You must strictly follow the 'Roadmap First Law'.")
        all_passed = False
    else:
        print(f"✅ Visual Roadmap Found.")

    if all_passed:
        print("✅ Workflow Validation Passed.")
        sys.exit(0)
    else:
        print("🛑 Workflow Validation Failed.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Lesson Plan Workflow")
    parser.add_argument("folder_name", help="Name of the lesson folder")
    args = parser.parse_args()
    validate_workflow(args.folder_name)
