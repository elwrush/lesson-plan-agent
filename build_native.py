import os
import shutil
import sys
from pathlib import Path

def build_native(lesson_path):
    lesson_path = Path(lesson_path)
    if not lesson_path.exists():
        print(f"[ERROR] Lesson path {lesson_path} not found.")
        sys.exit(1)

    project_root = Path.cwd()
    published_dir = lesson_path / "published"
    published_dir.mkdir(exist_ok=True)

    print(f"[INFO] Building Native Presentation: {lesson_path.name}")

    # 1. Acquire Assets from Skills and Root
    skill_assets = project_root / "skills" / "06-creating-html-presentation" / "assets"
    reveal_source = project_root / "lib" / "reveal"
    fontawesome_source = project_root / "lib" / "fontawesome"

    # 2. Bundle Engine & UI
    for folder in ["dist", "plugin"]:
        src = reveal_source / folder
        dst = published_dir / folder
        if src.exists():
            if dst.exists(): shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"  [BUNDLE] {folder}")

    # FontAwesome
    fa_dst = published_dir / "fontawesome"
    if fontawesome_source.exists():
        if fa_dst.exists(): shutil.rmtree(fa_dst)
        shutil.copytree(fontawesome_source, fa_dst)
        print("  [BUNDLE] fontawesome")

    # 3. Create CSS folder and copy pedagogy.css
    css_dst = published_dir / "css"
    css_dst.mkdir(exist_ok=True)
    if (skill_assets / "pedagogy.css").exists():
        shutil.copy2(skill_assets / "pedagogy.css", css_dst / "pedagogy.css")
        print("  [COPY] pedagogy.css")

    # 4. Copy slide-components.js
    js_dst = published_dir / "js"
    js_dst.mkdir(exist_ok=True)
    if (project_root / "js" / "slide-components.js").exists():
        shutil.copy2(project_root / "js" / "slide-components.js", js_dst / "slide-components.js")
        print("  [COPY] slide-components.js")

    # 5. Inline presentation.md into index_shell.html
    shell_path = skill_assets / "index_shell.html"
    md_path = lesson_path / "presentation.md"
    
    if shell_path.exists() and md_path.exists():
        shell_content = shell_path.read_text(encoding="utf-8")
        md_content = md_path.read_text(encoding="utf-8")
        
        # Perform the inlining (strip to prevent blank slides)
        final_html = shell_content.replace("<!-- MARKDOWN_PLACEHOLDER -->", md_content.strip())
        
        (published_dir / "index.html").write_text(final_html, encoding="utf-8")
        print("  [DEPLOY] index.html (Inlined Markdown)")
    else:
        print("  [ERROR] index_shell.html or presentation.md missing.")

    # 7. Sync Images & Audio
    images_dst = published_dir / "images"
    audio_dst = published_dir / "audio"
    images_dst.mkdir(exist_ok=True)
    audio_dst.mkdir(exist_ok=True)
    
    # Lesson images
    if (lesson_path / "images").exists():
        for img in (lesson_path / "images").glob("*"):
            shutil.copy2(img, images_dst)
    
    # Root shared images (ACT.png etc)
    for img_name in ["ACT.png"]:
        root_img = project_root / "images" / img_name
        if root_img.exists():
            shutil.copy2(root_img, images_dst)

    # Mandatory Audio (Timer blips/bells)
    root_audio = project_root / "audio"
    if root_audio.exists():
        for sound in ["blip.mp3", "bell.mp3", "30-seconds.mp3"]:
            src_sound = root_audio / sound
            if src_sound.exists():
                shutil.copy2(src_sound, audio_dst)
                print(f"  [AUDIO] {sound}")
    
    print("  [SYNC] Media completed.")
    print(f"[SUCCESS] Native Presentation available at: {published_dir / 'index.html'}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_native.py <lesson_path>")
        sys.exit(1)
    build_native(sys.argv[1])
