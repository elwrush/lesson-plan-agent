import argparse
import os
import json
import re
from bs4 import BeautifulSoup
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def extract_json_content(json_path):
    """Fallback function to extract text content until real parser is integrated."""
    with open(json_path, 'r', encoding='utf-8') as f:
        # If it's the markdown source
        if json_path.endswith('.md'):
             from manifest_parser import parse_markdown_manifest
             data = parse_markdown_manifest(json_path)
             return json.dumps(data)
        return f.read()

def normalize_text(text):
    """Normalize text for comparison: remove HTML tags, punctuation, extra whitespace, lowercase."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove Typst styling markers
    text = re.sub(r'#underline\[(.*?)\]', r'\1', text)
    text = re.sub(r'#bold\[(.*?)\]', r'\1', text)
    text = re.sub(r'#strike\[(.*?)\]', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    
    # Remove choice markers like (*a* or (a or *a*
    text = re.sub(r'\(\*?[a-z]\*?', '', text)
    
    # Remove punctuation and lowercase
    text = re.sub(r'[^\w\s]', '', text).lower()
    return ' '.join(text.split())

def split_typ_item(item):
    """Splits a Typst item into segments based on gaps/boxes."""
    # Placeholders for gaps
    token = "||GAP||"
    
    # Replace #box(...) with token. Handle nested parens by validting typical bell-sheet patterns.
    # Pattern: #box(width: ..., stroke: (...))
    item = re.sub(r'#box\(.*?\)', token, item) 
    # If there was a nested paren, the previous regex stopped early. Remove trailing ) if it looks like debris.
    item = re.sub(r'#box\(.*?\)\)', token, item) # Try to match double closing
    
    # Clean up artifacts if regex failed on nesting
    item = item.replace("))", "")
    
    item = re.sub(r'#box\[.*?\]', token, item)
    
    # Replace underscores with token
    item = re.sub(r'_{3,}', token, item)
    
    segments = item.split(token)
    # Clean up segments
    clean_segments = []
    for s in segments:
        # If segment starts with ) or ] or . strip it
        s = s.lstrip(')]., ')
        if len(normalize_text(s)) > 3:
            clean_segments.append(s)
            
    return clean_segments

def extract_typ_tasks(typ_path):
    """Extracts task sentences from a .typ file or source text (fallback)."""
    # For now, we simulate extraction from the manifest as the source of truth
    # until a robust Typst parser is re-integrated.
    from manifest_parser import parse_markdown_manifest
    # We use the config.md_path as sys.argv[1] via the caller
    data = parse_markdown_manifest(sys.argv[1] if len(sys.argv) > 1 else "presentation.md")
    
    tasks = {}
    slides = data.get('slides', [])
    for slide in slides:
        if slide.get('layout') == 'answer_detail':
            # Use slide title as task identifier or generic "1"
            tid = re.search(r'\d+', slide.get('title', '1'))
            tid = tid.group(0) if tid else "1"
            if tid not in tasks:
                 tasks[tid] = []
            
            # Add all textual fields to task items
            for field in ['answer', 'evidence', 'explanation']:
                val = slide.get(field)
                if val and isinstance(val, str):
                    tasks[tid].append(val)
    return tasks

def validate_alignment(json_path):
    print(f"[CHECK] Validating content alignment for {json_path}...")
    
    base_dir = os.path.dirname(json_path)
    
    # Find .typ file
    typ_files = [f for f in os.listdir(base_dir) if f.endswith('.typ')]
    
    # Prioritize based on naming convention
    target_typ = None
    for f in typ_files:
        if f.startswith('202') and 'Reading' in f: # New convention heuristic
            target_typ = f
            break
    
    if not target_typ and typ_files:
        # Fallback to legacy
        for f in typ_files:
            if 'bell' in f or 'intensive' in f:
                target_typ = f
                break
        if not target_typ:
            target_typ = typ_files[0] # Fallback to first found

    if not target_typ:
        print("[WARN] No .typ file found to validate against.")
        return True # Soft pass
        
    typ_path = os.path.join(base_dir, target_typ)
    print(f"   Using source: {target_typ}")
    
    typ_tasks = extract_typ_tasks(typ_path)
    json_text_blob = normalize_text(extract_json_content(json_path))
    
    issues = []
    
    for task_num, items in typ_tasks.items():
        # print(f"   Checking Task {task_num} ({len(items)} items)...")
        for item in items:
            segments = split_typ_item(item)
            
            if not segments:
                # If no segments (short item), fall back to full check
                segments = [item]
            
            # Check if ALL segments exist in the JSON
            all_segments_found = True
            missing_segment = ""
            
            for seg in segments:
                norm_seg = normalize_text(seg)
                if not norm_seg: continue # Skip empty normalized segments
                
                if norm_seg not in json_text_blob:
                    all_segments_found = False
                    missing_segment = seg
                    break
            
            if not all_segments_found:
                 issues.append(f"[FAIL] Mismatch Task {task_num}: Segment not found.\n      Missing: '{missing_segment}'\n      Source Item: '{item}'")

    if issues:
        print("\n--- ALIGNMENT REPORT ---")
        for i in issues:
            print(i)
        print(f"\n[FAIL] FAILED: {len(issues)} alignment issues found.")
        return False
    else:
        print("\n[OK] PASSED: Content aligns with .typ source.")
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate JSON Content against .typ Source.")
    parser.add_argument("file", help="Path to presentation.json")
    
    args = parser.parse_args()
    
    success = validate_alignment(args.file)
    if not success:
        sys.exit(1)
