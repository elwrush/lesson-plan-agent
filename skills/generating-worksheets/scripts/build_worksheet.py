import argparse
import os
import sys
import subprocess
from jinja2 import Environment, FileSystemLoader

def main():
    parser = argparse.ArgumentParser(description="Generate branded worksheets.")
    parser.add_argument("--brand", choices=["intensive", "bell"], default="intensive", help="Brand style")
    parser.add_argument("--output", required=True, help="Path to save the PDF")
    parser.add_argument("--title", default="Worksheet", help="Main Title")
    parser.add_argument("--header-title", help="Custom Header Title (for Bell brand)")
    parser.add_argument("--quote", help="Subheader quote")
    parser.add_argument("--content", help="Path to HTML content fragment to inject")
    parser.add_argument("--debug", action="store_true", help="Keep temporary HTML file")

    args = parser.parse_args()

    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    template_dir = os.path.join(skill_dir, "templates")
    project_root = os.path.abspath(os.path.join(skill_dir, "..", ".."))
    
    # Image Root (Use pathlib for correct URI encoding with spaces)
    from pathlib import Path
    image_root_path = os.path.join(project_root, "images")
    image_root_url = Path(image_root_path).as_uri()
    
    # Jinja Setup
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("worksheet-master.html")

    # Load content if provided
    content_html = ""
    if args.content:
        if os.path.exists(args.content):
            with open(args.content, "r", encoding="utf-8") as f:
                content_html = f.read()
            
            # Pre-process content to replace common variables since nested Jinja rendering isn't automatic
            content_html = content_html.replace("{{ image_root }}", image_root_url)
        else:
            print(f"Warning: Content file not found: {args.content}")

    # Render
    render_context = {
        "brand": args.brand,
        "title": args.title,
        "header_title": args.header_title,
        "quote": args.quote,
        "image_root": image_root_url, # Use file protocol for absolute paths
        "content": content_html
    }
    
    rendered_html = template.render(**render_context)

    # Save Temp HTML
    output_dir = os.path.dirname(os.path.abspath(args.output))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    temp_html_path = os.path.join(output_dir, "temp_render.html")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
    
    print(f"Generated HTML: {temp_html_path}")

    # Convert to PDF
    pdf_script = os.path.join(script_dir, "pdf_converter.js")
    cmd = ["node", pdf_script, temp_html_path, args.output]
    
    print(f"Generating PDF: {args.output}...")
    try:
        subprocess.check_call(cmd, shell=True) # shell=True often needed on Windows for node
        print("Done.")
    except subprocess.CalledProcessError as e:
        print(f"Error generating PDF: {e}")
        sys.exit(1)
    finally:
        if not args.debug and os.path.exists(temp_html_path):
            os.remove(temp_html_path)

if __name__ == "__main__":
    main()
