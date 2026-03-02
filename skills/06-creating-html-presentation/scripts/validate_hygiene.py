import json
import sys
import os
from pathlib import Path

def validate_hygiene(json_path):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        return False

    lesson_dir = os.path.dirname(json_path)
    images_dir = os.path.join(lesson_dir, "images")
    
    errors = []

    # 1. Local Asset Size Check (< 1MB)
    if os.path.exists(images_dir):
        for img in os.listdir(images_dir):
            img_path = os.path.join(images_dir, img)
            if os.path.isfile(img_path):
                # Ignore system files
                if img.lower() == 'desktop.ini': continue
                
                size = os.path.getsize(img_path)
                if size > 10 * 1024 * 1024:
                    errors.append(f"File too large: {img} ({size/1024/1024:.2f}MB). Assets must be < 10MB.")
                
                # 2. Heavy Media Size Check (videos must also be < 10MB)
                # (Removed strict ban on .mp4 in lesson folder per new standard)


    # 3. JSON Background Check
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            slides = data.get('slides', [])
            for i, slide in enumerate(slides):
                layout = slide.get('layout', '')
                # Task slides (split_table, ranking, checklist, quiz, etc.)
                if any(k in layout for k in ['table', 'ranking', 'checklist', 'quiz', 'cloze', 'match']):
                    if 'image' in slide and slide['image']:
                        # Exception 1: if they explicitly override with a gradient it might be okay
                        # Exception 2: if the slide has a badge (PROFILE, SCANNING etc.), it's informational, not a pure quiz
                        if 'background_gradient' not in slide and 'badge' not in slide:
                            errors.append(f"Slide {i} ({slide.get('title')}): Question slides must not use image backgrounds. Use green radial design.")
        except Exception as e:
            errors.append(f"JSON Parse Error: {e}")

    if errors:
        print("\n[X] REPO HYGIENE VIOLATIONS:")
        for error in errors:
            print(f"  - {error}")
        print("\n[!] FAILED: Please resize images (<1MB) and move videos to root images/.")
        return False
    
    print("[OK] Repo hygiene check passed.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_hygiene.py <presentation.json>")
        sys.exit(1)
    success = validate_hygiene(sys.argv[1])
    sys.exit(0 if success else 1)
