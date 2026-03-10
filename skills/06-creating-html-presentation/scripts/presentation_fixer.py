import os
import sys
import re
import yaml
import json
from pathlib import Path

def normalize_manifest(md_path):
    print(f"Fixer: Normalizing {os.path.basename(md_path)}...")
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extract Frontmatter
    meta = {}
    parts = re.split(r'^---\s*$', content, flags=re.MULTILINE)
    if len(parts) > 1:
        try:
            meta = yaml.safe_load(parts[1]) or {}
            main_body = '---'.join(parts[2:])
        except:
            main_body = content
    else:
        main_body = content

    # 2. Split Slides (Support --- and # SLIDE)
    slide_blocks = re.split(r'^---\s*$|^#\s*SLIDE\s*\d+\s*$', main_body, flags=re.MULTILINE)
    slide_blocks = [b.strip() for b in slide_blocks if b.strip()]

    normalized_slides = []
    
    # 3. Process each slide
    for i, block in enumerate(slide_blocks):
        slide = {
            "slide_id": f"slide-{i+1}",
            "layout": None,
            "text": ""
        }
        
        lines = block.split('\n')
        content_lines = []
        parsing_metadata = True
        
        for line in lines:
            stripped = line.strip()
            if not stripped: continue
            
            if parsing_metadata:
                if ':' in line and not stripped.startswith(('#', '-', '*', '>', '[')):
                    key, val = [part.strip() for part in line.split(':', 1)]
                    # Validate key
                    if re.match(r'^[a-zA-Z0-9_\.]+$', key):
                        val = val.strip().strip('"').strip("'")
                        # Basic types
                        if val.lower() == 'true': val = True
                        elif val.lower() == 'false': val = False
                        elif val.isdigit(): val = int(val)
                        
                        if "." in key:
                            m_k, s_k = key.split(".", 1)
                            if m_k not in slide: slide[m_k] = {}
                            slide[m_k][s_k] = val
                        else:
                            slide[key] = val
                        continue
                
                if stripped.startswith('#'): continue # Skip headers in meta
                
                # If we get here, it's content
                parsing_metadata = False
                content_lines.append(line)
            else:
                content_lines.append(line)
        
        slide["text"] = '\n'.join(content_lines).strip()
        
        # 4. Layout Heuristics (The "Director's Safety Net")
        if not slide["layout"]:
            if "mission_items" in slide or "objectives" in slide:
                slide["layout"] = "mission"
            elif "strategy_items" in slide:
                slide["layout"] = "strategy"
            elif "word" in slide or "phoneme" in slide:
                slide["layout"] = "vocab"
            elif "timer" in slide:
                 slide["layout"] = "strategy" # Safe default for timed tasks
            elif "items" in slide:
                 slide["layout"] = "schema_activation"
            else:
                slide["layout"] = "impact"
        
        # 5. Fix Layout Mappings (Engine Sync)
        # Ensure the layout exists in our library
        valid_layouts = ["title", "mission", "impact", "schema_activation", "strategy", "vocab", "split_table", "editing", "answer", "answer_detail", "ranking", "match_draw"]
        if slide["layout"] not in valid_layouts:
            print(f"  [WARN] Unknown layout '{slide['layout']}' on Slide {i+1}. Falling back to 'impact'.")
            slide["layout"] = "impact"

        normalized_slides.append(slide)

    # 6. Save Normalized JSON (Internal for Generator)
    lesson_dir = Path(md_path).parent
    json_out = lesson_dir / "presentation.json"
    with open(json_out, 'w', encoding='utf-8') as f:
        json.dump({"meta": meta, "slides": normalized_slides}, f, indent=2)
    
    print(f"Fixer: Generated normalized presentation.json")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python presentation_fixer.py <manifest_path>")
        sys.exit(1)
    normalize_manifest(sys.argv[1])
