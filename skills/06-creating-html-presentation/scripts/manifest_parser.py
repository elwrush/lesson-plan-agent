import re
import yaml

def parse_markdown_manifest(md_path):
    """
    Parses a presentation.md manifest file containing YAML frontmatter 
    and slides separated by '---'.
    Returns a dictionary matching the legacy presentation.json schema:
    {
      "meta": { ... },
      "slides": [ ... ]
    }
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by exactly '---' OR '# SLIDE X' patterns
    parts = re.split(r'^---\s*$|^#\s*SLIDE\s*\d+\s*$', content, flags=re.MULTILINE)
    
    # If the first part is empty (e.g. file starts with ---), drop it
    if parts and not parts[0].strip():
        parts = parts[1:]
    
    if not parts:
        return {"meta": {}, "slides": [], "raw": content}

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
            "layout": "default"
        }

        # Extract Key: Value pairs (Director Format)
        lines = slide_markdown.split('\n')
        content_lines = []
        parsing_metadata = True
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            if parsing_metadata:
                if ':' in line and not stripped.startswith(('#', '-', '*', '>', '[')):
                    # Potential key: value pair
                    key, val = line.split(':', 1)
                    key = key.strip()
                    
                    # Validate key is a clean identifier (no spaces, special chars except dot)
                    if not re.match(r'^[a-zA-Z0-9_\.]+$', key):
                        parsing_metadata = False
                        content_lines.append(line)
                        continue

                    val = val.strip().strip('"').strip("'")
                    
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
                    
                    if "." in key:
                        main_k, sub_k = key.split(".", 1)
                        if main_k not in slide_data: slide_data[main_k] = {}
                        slide_data[main_k][sub_k] = val
                    else:
                        slide_data[key] = val
                elif stripped.startswith('#'):
                    # Skip slide markers/headers but keep parsing metadata
                    continue
                else:
                    # Real content reached
                    parsing_metadata = False
                    content_lines.append(line)
            else:
                content_lines.append(line)

        slide_data["text"] = '\n'.join(content_lines).strip()

        # Extract HTML comments for layout/meta (Legacy Support)
        metadata_matches = re.finditer(r'<!--\s*([a-zA-Z_.]+)\s*:\s*(.*?)\s*-->', slide_markdown)
        for match in metadata_matches:
            key, val = match.groups()
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            
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
        
        # Optional: Attempt to pull title from markdown headers if not explicitly defined
        if not slide_data.get("title"):
             title_match = re.search(r'^#\s+(.*?)$', slide_markdown, flags=re.MULTILINE)
             if title_match:
                 slide_data["title"] = title_match.group(1).strip()

        slides.append(slide_data)
        
    return {"meta": meta, "slides": slides, "raw": content}
