import json
import sys
import os
import re


def validate_answer_separation(json_path):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        return False

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return False

    slides = data.get("slides", [])
    errors = []

    for i, slide in enumerate(slides):
        layout = slide.get("layout", "")

        if layout == "answer_detail":
            answer = slide.get("answer", "")
            evidence = slide.get("evidence", "")

            # 1. Multi-Answer Detection
            combined_patterns = [
                r"\d+\..+?\d+\.",  # "1. ... 2. "
                r"[A-Z]\..+?[A-Z]\.",  # "A. ... B. "
                r",.*?,.*?,",  # Multiple commas (e.g., 3+ items)
                r";.*?;",  # Multiple semicolons
            ]

            is_combined = False
            for pattern in combined_patterns:
                if re.search(pattern, answer):
                    is_combined = True
                    break

            if is_combined:
                # Exception: "1.E, 2.A..." for reordering/sequence tasks is usually ONE slide reveal
                if (
                    "ORDER" in slide.get("title", "").upper()
                    or "SEQUENCE" in slide.get("title", "").upper()
                ):
                    pass
                else:
                    errors.append(
                        f"Slide {i} ({slide.get('title')}): Multiple answers detected in single slide. Each answer must have its own slide."
                    )

            # 2. Location Marker Check
            if evidence and not re.search(r"\[(Para|Line|Page)\s+[\d\w]+\]", evidence):
                errors.append(
                    f"Slide {i} ({slide.get('title')}): Evidence snippet missing location marker (e.g. [Para 5] or [Line 12])."
                )

    if errors:
        print("\n[X] PEDAGOGICAL PROTOCOL VIOLATIONS:")
        for error in errors:
            print(f"  - {error}")
        print(
            "\n[!] FAILED: Every answer must be on a separate slide and evidence must have location markers."
        )
        return False

    print("[OK] Pedagogical protocol check passed.")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_answer_separation.py <presentation.json>")
        sys.exit(1)

    success = validate_answer_separation(sys.argv[1])
    sys.exit(0 if success else 1)
