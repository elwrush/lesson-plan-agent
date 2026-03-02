import json
import sys
import os
import re

def validate_gold_standard(json_path):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        return False

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"JSON Parse Error: {e}")
            return False

    slides = data.get("slides", [])
    errors = []
    warnings = []

    # 1. Mission Mandate (Slide 2)
    if len(slides) > 1:
        mission_slide = slides[1]
        if mission_slide.get("layout") != "mission":
            errors.append("Slide 2 MUST be a 'mission' slide.")
        else:
            if mission_slide.get("title") != "YOUR MISSION":
                errors.append("Mission slide title MUST be exactly 'YOUR MISSION'.")
            if "mission_bg_clipped.mp4" not in str(mission_slide.get("video", "")):
                errors.append("Mission slide MUST use 'mission_bg_clipped.mp4'.")

    # 2. Segue-Bridge Mandate
    for i in range(len(slides) - 1):
        if slides[i].get("layout") == "segue":
            next_layout = slides[i+1].get("layout", "")
            if next_layout not in ["strategy", "vocab"]:
                errors.append(f"Slide {i+1} (segue) MUST be followed by a pedagogical bridge (strategy or vocab). Found: {next_layout}")

    # 3. No Teacher Jargon
    banned_words = ["Pre-teaching", "Lead-in", "Gist", "Controlled Practice", "Stage"]
    raw_json = json.dumps(data)
    for word in banned_words:
        if word.lower() in raw_json.lower():
            # Detailed check for student-visible fields
            for slide in slides:
                for field in ["title", "badge", "content", "subtitle"]:
                    val = str(slide.get(field, ""))
                    if word.lower() in val.lower():
                        errors.append(f"Banned teacher jargon '{word}' found in slide '{slide.get('title')}' ({field} field).")

    # 4. Vocab Styling Mandates
    for slide in slides:
        if slide.get("layout") == "vocab":
            context = slide.get("context_sentence", "")
            if "<span style='color: #FFD700;'>" not in context and "<span style=\"color: #FFD700;\">" not in context:
                errors.append(f"Vocab slide '{slide.get('word')}' MUST use Gold (#FFD700) highlighting for the target word.")

    # 5. Answer Detail Numerals
    # Hard to check in JSON if they used the template logic correctly, 
    # but we can check if they provided a 'number' field
    for slide in slides:
        if slide.get("layout") == "answer_detail":
            if "number" not in slide:
                warnings.append(f"Answer Detail slide '{slide.get('title')}' missing 'number' field for numeral display.")

    if errors:
        print("\n[X] GOLD STANDARD VIOLATIONS:")
        for err in errors:
            print(f"  - {err}")
        return False

    if warnings:
        print("\n[!] GOLD STANDARD WARNINGS:")
        for warn in warnings:
            print(f"  - {warn}")

    print("[OK] Gold Standard production check passed.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_gold_standard.py <presentation.json>")
        sys.exit(1)
    
    success = validate_gold_standard(sys.argv[1])
    sys.exit(0 if success else 1)
