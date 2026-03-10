import sys
import os
import re
import io
import yaml

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def parse_markdown_manifest(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Very basic parsing: split by --- to get slides.
    # The first block is frontmatter.
    parts = re.split(r'^---\s*$', content, flags=re.MULTILINE)[1:] # Skip empty first split if starts with ---
    
    if not parts:
        return {"slides": []}

    try:
        meta = yaml.safe_load(parts[0]) or {}
    except yaml.YAMLError:
        meta = {}

    slides = []
    
    # Process subsequent slide blocks
    for i, slide_markdown in enumerate(parts[1:]):
        slide_markdown = slide_markdown.strip()
        if not slide_markdown:
            continue

        slide_data = {
            "slide_id": f"slide-{i}",
            "layout": "default",
            "text": slide_markdown
        }
        
        # Extract HTML comments for layout/meta
        metadata_matches = re.finditer(r'<!--\s*([a-zA-Z_]+)\s*:\s*(.*?)\s*-->', slide_markdown)
        for match in metadata_matches:
            key, val = match.groups()
            key = key.strip()
            val = val.strip()
            
            # Simple list/dict parsing attempts
            if val.startswith('[') or val.startswith('{'):
                try:
                    import ast
                    val = ast.literal_eval(val)
                except:
                    pass
            elif val.lower() == 'true': val = True
            elif val.lower() == 'false': val = False
            elif val.isdigit(): val = int(val)
                
            # Handle deep keys like background.src
            if "." in key:
                main_k, sub_k = key.split(".", 1)
                if main_k not in slide_data: slide_data[main_k] = {}
                slide_data[main_k][sub_k] = val
            else:
                slide_data[key] = val
        
        # Optional: Attempt to pull title from markdown # headers if not explicitly defined
        if not slide_data.get("title"):
             title_match = re.search(r'^#\s+(.*?)$', slide_markdown, flags=re.MULTILINE)
             if title_match:
                 slide_data["title"] = title_match.group(1).strip()

        slides.append(slide_data)
        
    return {"meta": meta, "slides": slides, "raw": content}

def validate_gold_standard(md_path):
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found")
        return False

    try:
        data = parse_markdown_manifest(md_path)
    except Exception as e:
        print(f"Markdown Parse Error: {e}")
        return False

    slides = data.get("slides", [])
    errors = []
    warnings = []


    # --- TECHNICAL SCHEMA CHECKS (ZERO-CRASH) ---
    for i, slide in enumerate(slides):
        layout = slide.get("layout")
        
        # 1. Layout Key
        if "template" in slide:
            errors.append(f"Slide {i+1}: BANNED key 'template' found. Use 'layout' instead.")
        if not layout:
            errors.append(f"Slide {i+1}: Missing mandatory 'layout' key.")

        # LEGACY LAYOUT BAN: answer_detail is retired. Use split_table instead.
        # Reason: answer_detail causes content to overflow off-screen on long answers.
        if layout == "answer_detail":
            errors.append(
                f"Slide {i+1} ('{slide.get('title')}'): BANNED LEGACY LAYOUT 'answer_detail'. "
                f"Use 'split_table' with an HTML table for all answer/feedback slides. "
                f"answer_detail is retired because it causes overflow on long content."
            )

        # 2. Root-Level Data (No nesting in 'data')
        if "data" in slide and isinstance(slide["data"], dict) and len(slide["data"]) > 0:
            errors.append(f"Slide {i+1}: BANNED nesting. Data must be at root level of slide object, not in 'data' sub-block.")

        # 3. Type Strictness: Timer
        if "timer" in slide:
            if not isinstance(slide["timer"], int):
                errors.append(f"Slide {i+1}: 'timer' MUST be an integer (e.g., 120), not {type(slide['timer']).__name__}.")

        # 4. Video Loop Check
        if slide.get("video"):
            if "video_loop" in slide:
                if not isinstance(slide["video_loop"], bool):
                    errors.append(f"Slide {i+1}: 'video_loop' MUST be a boolean (true/false), not {type(slide['video_loop']).__name__}.")
            else:
                if layout in ["title", "segue"]:
                    errors.append(f"Slide {i+1} ({layout}): Missing 'video_loop': true for background video.")

        # --- COMPONENT KEY MANDATES (PEDAGOGICAL INTEGRITY) ---
        if layout == "strategy":
            items = slide.get("strategy_items", [])
            if not items and not slide.get("content") and not slide.get("table"):
                errors.append(f"Slide {i+1} (strategy): Missing pedagogical content (strategy_items, content, or table).")
            
            # Pedagogical Mandate Check (Heuristic)
            for item in items:
                # Template Contract: strategy template uses item.text ONLY.
                # 'left'/'right' keys are INVISIBLE to the template and render blank.
                if isinstance(item, dict) and not item.get("text"):
                    banned_keys = [k for k in ["left", "right", "label", "sub"] if item.get(k)]
                    if banned_keys:
                        errors.append(
                            f"Slide {i+1} (strategy): Item uses unsupported keys {banned_keys}. "
                            f"The strategy template ONLY reads 'item.text'. "
                        )
                    else:
                        errors.append(f"Slide {i+1} (strategy): Item missing required 'text' key — will render blank.")
                text = item.get("text", "")
                # If an item looks like a definition (e.g. "Word: definition")
                if ":" in text and len(text.split(":")[0].split()) <= 2:
                    warnings.append(f"Slide {i+1} (strategy): Possible Pedagogical Violation. Strategy items should provide instruction (how to learn), not just definitions ('{text}').")

            # Iron Rule: Badge Check (RELAXED)
            if not slide.get("badge"):
                warnings.append(f"Slide {i+1} (strategy): Suggestion: Add a 'badge' (e.g., TASK 1) for clarity.")
        
        if layout == "impact":
            if not slide.get("text") and not slide.get("main_text"):
                errors.append(f"Slide {i+1} (impact): Missing mandatory 'text' field.")
            if not slide.get("image"):
                warnings.append(f"Slide {i+1} (impact): No background 'image' provided.")
            # Iron Rule: Badge Check (RELAXED)
            if not slide.get("badge"):
                warnings.append(f"Slide {i+1} (impact): Suggestion: Add a 'badge' (e.g., TASK 1) for clarity.")
            # Points Contract Check: template expects dicts with 'text' key, not bare strings.
            for j, point in enumerate(slide.get("points", [])):
                if isinstance(point, str):
                    errors.append(
                        f"Slide {i+1} (impact): points[{j}] is a bare string '{point[:40]}...'. "
                        f"The impact template requires each point to be a dict: {{\"icon\": \"fa-check\", \"text\": \"...\"}}. "
                        f"Bare strings render as blank."
                    )
            
        # --- AUDIO OVER TIMER LAW (LISTENING VS READING) ---
        # NOTE: 'notes' field is intentionally excluded — it is teacher-facing only and must never influence slide classification.
        slide_text_content = str(slide.get("text", "")) + str(slide.get("title", "")) + str(slide.get("main_text", ""))
        is_listening_slide = any(word in slide_text_content.lower() for word in ["listen", "audio", "track", "recording"]) or slide.get("audio")
        
        if is_listening_slide:
            if slide.get("timer"):
                errors.append(f"Slide {i+1} ({layout}): AUDIO OVER TIMER VIOLATION. Listening tasks must NOT use 'timer'. Use 'audio' scrubber instead.")
            if layout in ["impact", "split_table"] and not slide.get("audio") and any(word in slide_text_content.lower() for word in ["listen", "track", "recording"]):
                warnings.append(f"Slide {i+1} ({layout}): Listening tasks should ideally include an 'audio' field.")
        else:
            # The Timer Law (Work-Only)
            # Timers are MANDATORY for: split_table, editing, and impact slides with task keywords.
            # Timers are FORBIDDEN for: title, segue, mission, vocab, answer_detail.
            
            task_keywords = ["discuss", "write", "complete", "identify", "choose", "share", "think", "pair", "brainstorm"]
            is_work_slide = any(kw in slide_text_content.lower() for kw in task_keywords)
            is_explanation_slide = any(kw in slide_text_content.lower() for kw in ["remember", "note", "explanation", "rule", "states vs actions", "check", "the repair shop"]) or slide.get("badge", "").lower() == "explanation"

            # Check if previous slides in the same task group (by badge) had a timer
            prev_has_timer = False
            current_badge = slide.get("badge")
            if current_badge and i > 0:
                for prev_idx in range(i-1, -1, -1):
                    prev_slide = slides[prev_idx]
                    if prev_slide.get("badge") != current_badge:
                        break
                    if prev_slide.get("timer"):
                        prev_has_timer = True
                        break

            if layout in ["split_table", "editing"]:
                # Editing slides used for EXPLANATION (Modeling) don't need timers
                if layout == "editing" and is_explanation_slide:
                    if slide.get("timer"):
                        errors.append(f"Slide {i+1} (editing): TIMER PROHIBITION VIOLATION. Explanation-focused editing slides must NOT have a 'timer'.")
                elif not slide.get("timer") and not is_listening_slide and not prev_has_timer:
                    warnings.append(f"Slide {i+1} ({layout}): Suggestion: Add a 'timer' (int) for this task.")
                
                # Timer Integrity Law
                timer_val = slide.get("timer")
                if timer_val and timer_val < 60:
                    task_title = (slide.get("title") or "").lower()
                    if any(word in task_title for word in ["draft", "write", "writing", "essay", "paragraph", "letter"]):
                         warnings.append(f"Slide {i+1} ({layout}): Timer ({timer_val}s) seems short for a productive writing task. Consider 600-1200s.")
            
            if layout == "impact":
                if is_work_slide and not is_explanation_slide and not slide.get("timer") and not is_listening_slide:
                    warnings.append(f"Slide {i+1} (impact): Suggestion: Add a 'timer' for this discussion.")
                elif is_explanation_slide and slide.get("timer"):
                    errors.append(f"Slide {i+1} (impact): TIMER PROHIBITION VIOLATION. Explanation slides must NOT have a 'timer'.")
            
            if layout in ["title", "segue", "mission", "vocab", "answer_detail"] and slide.get("timer"):
                 warnings.append(f"Slide {i+1} ({layout}): Timer on {layout} slide is unusual.")

        if layout == "answer":
            if not slide.get("answers") and not slide.get("content"):
                errors.append(f"Slide {i+1} (answer): Missing answer content ('answers' array or 'content' string).")
            if not slide.get("badge"):
                warnings.append(f"Slide {i+1} (answer): Suggestion: Add a 'badge'.")

        if layout == "answer_detail":
            if not slide.get("question") and not slide.get("title"):
                errors.append(f"Slide {i+1} (answer_detail): Missing 'question' field.")
            if not slide.get("answer"):
                errors.append(f"Slide {i+1} (answer_detail): Missing 'answer' field.")
            if not slide.get("badge"):
                warnings.append(f"Slide {i+1} (answer_detail): Suggestion: Add a 'badge'.")

        if layout == "ranking":
            if not slide.get("left_items") or not slide.get("right_items"):
                errors.append(f"Slide {i+1} (ranking): Missing 'left_items' or 'right_items'.")
            if not slide.get("badge"):
                warnings.append(f"Slide {i+1} (ranking): Suggestion: Add a 'badge'.")

        if layout == "match_draw":
            if not slide.get("left_items") or not slide.get("right_items") or not slide.get("connections"):
                errors.append(f"Slide {i+1} (match_draw): Missing 'left_items', 'right_items', or 'connections'.")
            if not slide.get("badge"):
                warnings.append(f"Slide {i+1} (match_draw): Suggestion: Add a 'badge'.")

        if layout == "mission":
            mission_items = slide.get("items") or slide.get("mission_items") or slide.get("objectives")
            if not mission_items:
                errors.append(f"Slide {i+1} (mission): Missing mission items.")
            else:
                # Template Contract Check: items must use correct keys for the Jinja template.
                # The mission template expects 'icon' (FA class like 'fa-headphones'), and 'title' or 'text'.
                # Bare emoji icons or wrong keys (e.g. 'label', 'sub') will render as raw Python dicts.
                for j, item in enumerate(mission_items):
                    if not isinstance(item, dict):
                        errors.append(f"Slide {i+1} (mission): Item {j+1} must be a dict, not {type(item).__name__}.")
                        continue
                    icon = item.get('icon', '')
                    if not isinstance(icon, str) or not icon.startswith('fa-'):
                        errors.append(f"Slide {i+1} (mission): Item {j+1} 'icon' must be a FontAwesome class string starting with 'fa-' (e.g. 'fa-headphones'). Got: '{icon}'. Emoji icons are NOT supported.")
                    if not item.get('title') and not item.get('text'):
                        errors.append(f"Slide {i+1} (mission): Item {j+1} must have a 'title' or 'text' key. Keys like 'label' and 'sub' are not recognised by the template.")

    # --- PEDAGOGICAL & VISUAL FLOW CHECKS ---

    # 1. Mission Mandate (Slide 2)
    if len(slides) > 1:
        mission_slide = slides[1]
        if mission_slide.get("layout") != "mission":
            warnings.append("Slide 2 is usually a 'mission' slide.")
        else:
            if "MISSION" not in str(mission_slide.get("title", "")).upper():
                warnings.append("Mission slide title usually contains 'MISSION'.")
            
            # Support both flat 'video' and nested 'background.src'
            video_src = mission_slide.get("video", "")
            if not video_src and isinstance(mission_slide.get("background"), dict):
                video_src = mission_slide.get("background", {}).get("src", "")
            
            if "mission_bg_clipped.mp4" not in str(video_src):
                warnings.append("Note: Standard mission background is 'mission_bg_clipped.mp4'.")

    # 2. Segue-Bridge & Strategy Sequence (RELAXED)
    # The agent now has full freedom to sequence slides based on material logic.

    # 3. No Teacher Jargon
    banned_words = ["Pre-teaching", "Lead-in", "Gist", "Controlled Practice", "Stage", "Feedback", "The Hook"]
    raw_md = data.get("raw", "")
    for word in banned_words:
        if word.lower() in raw_md.lower():
            for slide in slides:
                for field in ["title", "badge", "text", "subtitle"]:
                    val = str(slide.get(field, ""))
                    if word.lower() in val.lower():
                        errors.append(f"Banned teacher jargon '{word}' found in slide '{slide.get('title')}' ({field} field).")

    # 4. Vocab Styling Mandates
    for slide in slides:
        if slide.get("layout") == "vocab":
            # Vocab Background Law
            bg = slide.get("background")
            if not bg:
                errors.append(f"Vocab slide '{slide.get('word')}': Missing mandatory 'background' image (Vocab Background Law).")
            elif isinstance(bg, dict) and bg.get("type") != "image":
                errors.append(f"Vocab slide '{slide.get('word')}': 'background' type MUST be 'image' (Vocab Background Law).")
            elif not bg.get("src"):
                 errors.append(f"Vocab slide '{slide.get('word')}': 'background' object MUST have a 'src' path (Vocab Background Law).")

            context = slide.get("context_sentence", "") or slide.get("example", "")
            if "text-gold" not in context and "#FFD700" not in context:
                errors.append(f"Vocab slide '{slide.get('word')}' MUST use 'text-gold' class matching for the target word.")
            
            # No Paragraph Markers Check
            if re.search(r"\[Para \d+\]", context):
                errors.append(f"Vocab slide '{slide.get('word')}': BANNED paragraph marker found in context sentence. Remove markers like [Para 1].")

    # 5. Audio Integrity
    if "beep.mp3" in raw_md.lower():
        errors.append("BANNED audio file 'beep.mp3' found in Markdown. Use 'blip.mp3' instead.")

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
        print("Usage: python validate_gold_standard.py <presentation.md>")
        sys.exit(1)
    
    success = validate_gold_standard(md_path=sys.argv[1])
    sys.exit(0 if success else 1)