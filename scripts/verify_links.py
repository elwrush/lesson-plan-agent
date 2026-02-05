import os
import re
import sys
from urllib.parse import unquote

def verify_links():
    project_root = os.getcwd()
    dist_dir = os.path.join(project_root, 'dist')

    if not os.path.exists(dist_dir):
        print("❌ Error: dist/ directory not found. Run build_dist.js first.")
        sys.exit(1)

    print("🔍 Starting Link Verification...")
    
    broken_links = []
    html_files_checked = 0
    total_links_checked = 0

    # Pattern to find src="..." and href="..."
    # We use a simple regex that matches both single and double quotes
    link_pattern = re.compile(r'(?:src|href)=["\'](.*?)["\']', re.IGNORECASE)

    for root, dirs, files in os.walk(dist_dir):
        for file in files:
            if file.endswith('.html'):
                html_files_checked += 1
                file_path = os.path.join(root, file)
                file_dir = os.path.dirname(file_path)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    print(f"⚠️  Could not read {file_path}: {e}")
                    continue

                links = link_pattern.findall(content)
                for link in links:
                    # Clean the link (remove fragments/queries)
                    link_clean = link.split('?')[0].split('#')[0]

                    # Skip empty, external, or data URIs
                    if not link_clean or link_clean.startswith(('http', 'https', 'data:', 'mailto:', '#')):
                        continue

                    total_links_checked += 1
                    
                    # URL unquote (handles %20 etc)
                    link_decoded = unquote(link_clean)
                    
                    # Resolve path relative to the HTML file
                    target_path = os.path.normpath(os.path.join(file_dir, link_decoded))

                    if not os.path.exists(target_path):
                        rel_html = os.path.relpath(file_path, dist_dir)
                        broken_links.append(f"   ❌ Broken: '{link_clean}' in {rel_html}")

    print(f"📊 Checked {html_files_checked} HTML files and {total_links_checked} links.")

    if broken_links:
        print(f"\n🚨 FOUND {len(broken_links)} BROKEN LINKS:")
        for err in sorted(list(set(broken_links))):
            print(err)
        return False
    else:
        print("✅ All local links verified successfully.")
        return True

if __name__ == "__main__":
    verify_links()