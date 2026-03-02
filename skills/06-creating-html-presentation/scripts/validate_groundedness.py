import json
import sys
import re
from pathlib import Path

def validate_groundedness(json_path, source_text_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(source_text_path, 'r', encoding='utf-8') as f:
        source_text = f.read().lower()

    errors = 0
    slides = data.get('slides', [])
    
    # Text cleaning for comparison
    def clean(text):
        return re.sub(r'[^\w\s]', '', str(text)).lower()

    print(f"--- GROUNDEDNESS AUDIT: {json_path} ---")
    
    for i, slide in enumerate(slides):
        # We only check 'content', 'evidence', 'explanation' fields
        keys_to_check = ['content', 'evidence', 'explanation', 'instruction', 'context']
        for key in keys_to_check:
            content = slide.get(key, "")
            if not content: continue
            
            # Skip placeholders like "[Para X]"
            if "[Para" in str(content):
                continue
            
            # Extract words for fuzzy search (simple check)
            # This is a basic implementation; in production, we'd use N-grams or LLM verification
            cleaned_content = clean(content)
            if len(cleaned_content) < 10: continue
            
            # Check if majority of keywords exist in source
            words = [w for w in cleaned_content.split() if len(w) > 4]
            found_count = sum(1 for w in words if w in source_text)
            
            if words and (found_count / len(words)) < 0.6:
                print(f"⚠️  Slide {i} ({slide.get('layout')}): Possible Hallucination in '{key}' field.")
                print(f"   Content: {content[:100]}...")
                errors += 1

    if errors == 0:
        print("✅ [PASS] All content appears grounded in the source text.")
    else:
        print(f"❌ [FAIL] {errors} potential hallucinations found.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validate_groundedness.py <presentation.json> <SOURCE_TEXT.md>")
    else:
        validate_groundedness(sys.argv[1], sys.argv[2])
