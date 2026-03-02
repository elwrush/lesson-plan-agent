
import os
import base64
import re
from pathlib import Path

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        ext = os.path.splitext(image_path)[1].lower().replace('.', '')
        if ext == 'jpg': ext = 'jpeg'
        return f"data:image/{ext};base64,{encoded_string}"

def bundle_html(input_file, output_file):
    base_dir = os.path.dirname(input_file)
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inline CSS
    def replace_css(match):
        href = match.group(1)
        css_path = os.path.join(base_dir, href)
        if os.path.exists(css_path):
            with open(css_path, 'r', encoding='utf-8') as f:
                return f'<style>\n{f.read()}\n</style>'
        return match.group(0)
    
    content = re.sub(r'<link rel="stylesheet" href="([^"]+)">', replace_css, content)

    # 2. Inline Scripts
    def replace_js(match):
        src = match.group(1)
        js_path = os.path.join(base_dir, src)
        if os.path.exists(js_path):
            with open(js_path, 'r', encoding='utf-8') as f:
                return f'<script>\n{f.read()}\n</script>'
        return match.group(0)

    content = re.sub(r'<script src="([^"]+)"></script>', replace_js, content)

    # 3. Inline Images (data-background-image and img src)
    def replace_image(match):
        img_src = match.group(1)
        img_path = os.path.join(base_dir, img_src)
        if os.path.exists(img_path):
            b64 = get_base64_image(img_path)
            return match.group(0).replace(img_src, b64)
        return match.group(0)

    # Link format: data-background-image="images/foo.png" or src="images/foo.png"
    content = re.sub(r'data-background-image="([^"]+)"', replace_image, content)
    content = re.sub(r'src="([^"]+)"', replace_image, content)

    # Fix font paths if any (Reveal often references fonts in themes)
    # Simple fix for Monokai or Theme fonts -> usually not an issue with simple themes, checking...
    # The 'black.css' theme imports fonts from Google Fonts usually, which requires internet.
    # Offline fonts are trickier, but for now we focus on local files.

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Bundled presentation created at: {output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    bundle_html(args.input, args.output)
