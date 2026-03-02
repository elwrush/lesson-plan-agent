import re
import json
import sys
import os
from pathlib import Path

def parse_typst_plan(typ_path):
    """
    Parses a Typst lesson plan to extract stages, vocab, and tasks.
    Focuses on the #stage_table component.
    """
    with open(typ_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract stages
    # Regex for stage("ID", "Name", "Time", "Aim", [content], "Interaction")
    stage_pattern = re.compile(r'stage\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*\[(.*?)\],\s*"([^"]+)"\s*\)', re.DOTALL)
    
    stages = []
    for match in stage_pattern.finditer(content):
        stages.append({
            "id": match.group(1),
            "name": match.group(2),
            "time": match.group(3),
            "aim": match.group(4),
            "procedure": match.group(5).strip(),
            "interaction": match.group(6)
        })
    
    return stages

def extract_vocab(procedure):
    """Extracts 5 vocab items if present in a procedure block."""
    vocab = []
    # Look for numbered lists with parenthetical clues
    vocab_matches = re.findall(r'(\d+)\.\s*\*([^*]+)\*\s*\(([^)]+)\)', procedure)
    for m in vocab_matches:
        vocab.append({
            "word": m[1].strip(),
            "clue": m[2].strip()
        })
    return vocab

def typst_to_json(typ_path, output_path):
    stages = parse_typst_plan(typ_path)
    slides = []
    
    # 1. Title Slide (Implicit)
    slides.append({
        "layout": "title",
        "title": "FRANKENSTEIN",
        "subtitle": "B1 Reading | Oxford Futures 3"
    })

    for stage in stages:
        # Add a Segue for each stage
        slides.append({
            "layout": "segue",
            "phase": f"PHASE {stage['id']}",
            "title": stage['name'],
            "subtitle": "Let's begin."
        })

        # Process Procedure for tasks and vocab
        proc = stage['procedure']
        
        # Check for Hook/Schema
        if "Interactive Hook" in proc or "schema" in proc.lower():
            # Extract icons
            icons_match = re.search(r'icons:\s*([^\.]+)', proc)
            icons = icons_match.group(1).strip() if icons_match else "🕯️ 🧪 😢"
            slides.append({
                "layout": "schema_activation",
                "title": "ACTIVATE SCHEMA",
                "content": icons
            })

        # Check for Vocab
        vocab_items = extract_vocab(proc)
        if vocab_items:
            for item in vocab_items:
                slides.append({
                    "layout": "vocab",
                    "word": item['word'],
                    "phoneme": "", # To be filled manually or via API
                    "context": item['clue']
                })
        
        # Extract Tasks (e.g., Task 1, Task 2)
        task_matches = re.finditer(r'\*Task (\d+)\s*\(([^)]+)\)\*:?\s*(.*?)(?=\n-|\n\*|$)', proc, re.DOTALL)
        for tm in task_matches:
            num = tm.group(1)
            name = tm.group(2)
            instr = tm.group(3).strip()
            
            # Bridge slide
            slides.append({
                "layout": "strategy",
                "title": f"TASK {num} | {name}",
                "content": f"<p>{instr}</p>"
            })
            
            # Task slide
            slides.append({
                "layout": "split_table",
                "title": f"TASK {num}",
                "instruction": instr
            })
            
            # Answer slide (Placeholder)
            slides.append({
                "layout": "answer_detail",
                "title": f"ANSWER {num}",
                "evidence": "[Para X]",
                "explanation": "To be verified against SOURCE_TEXT.md"
            })

    presentation = {
        "meta": {
            "title": "Frankenstein B1 Reading",
            "theme": "maroon"
        },
        "slides": slides
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(presentation, f, indent=2)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sync_lp_to_json.py <input.typ> <output.json>")
    else:
        typst_to_json(sys.argv[1], sys.argv[2])
