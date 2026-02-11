"""
deploy_presentation.py — Incremental GitHub Pages Deployer

Deploys a SINGLE presentation folder to the gh-pages branch WITHOUT
touching the shared Reveal.js engine (dist/, plugin/, css/) or other
presentations already live on GitHub Pages.

Architecture:
  1. Uses `git worktree` to checkout gh-pages into a temp directory.
  2. Copies ONLY the target presentation folder from local dist/.
  3. Updates the dashboard (index.html) on gh-pages.
  4. Commits and pushes.
  5. Cleans up the worktree.

Usage:
  python skills/deploying-to-github-pages/scripts/deploy_presentation.py <FOLDER-NAME>

Example:
  python skills/deploying-to-github-pages/scripts/deploy_presentation.py 2026-02-09-Frankenstein-B1-Reading
"""

import os
import sys
import shutil
import subprocess
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DIST_ROOT = PROJECT_ROOT / "dist"


def run(cmd, cwd=None, check=True):
    """Run a shell command and return stdout."""
    result = subprocess.run(
        cmd, cwd=cwd or PROJECT_ROOT, capture_output=True, text=True, shell=True
    )
    if check and result.returncode != 0:
        print(f"[ERROR] Command failed: {cmd}")
        print(result.stderr)
        sys.exit(1)
    return result.stdout.strip()


def verify_presentation_exists(folder_name):
    """Ensure the presentation exists in dist/."""
    presentation_dir = DIST_ROOT / folder_name
    index_file = presentation_dir / "index.html"
    if not index_file.exists():
        print(f"[ERROR] Presentation not found at: {presentation_dir}")
        print(f"        Run 'python build.py {folder_name}' first.")
        sys.exit(1)
    return presentation_dir


def generate_dashboard(worktree_path):
    """Generate dashboard index.html from folders in the worktree."""
    lessons = []
    skip_dirs = {"dist", "plugin", "css", "images", ".git"}

    for d in sorted(worktree_path.iterdir()):
        if d.is_dir() and d.name not in skip_dirs and not d.name.startswith("."):
            idx = d / "index.html"
            if idx.exists():
                try:
                    txt = idx.read_text(encoding="utf-8")
                    title_match = re.search(r"<title>(.*?)</title>", txt)
                    title = title_match.group(1) if title_match else d.name
                    lessons.append({"folder": d.name, "title": title})
                except Exception:
                    lessons.append({"folder": d.name, "title": d.name})

    cards = "".join(
        [
            f'<a href="{l["folder"]}/" class="card"><h3>{l["title"]}</h3>'
            f'<p>{l["folder"]}</p></a>'
            for l in lessons
        ]
    )

    dashboard_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bell Language Centre | Presentations Library</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1a1a1a; color: white; padding: 40px; }}
        h1 {{ color: #8B1538; border-bottom: 2pt solid #8B1538; padding-bottom: 10px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 30px; }}
        .card {{ background: #2a2a2a; border-radius: 8px; padding: 20px; transition: transform 0.2s; border: 1px solid #444; text-decoration: none; color: white; display: block; }}
        .card:hover {{ transform: translateY(-5px); border-color: #8B1538; }}
        .card h3 {{ margin-top: 0; color: #FFD700; }}
        .card p {{ font-size: 0.9em; color: #ccc; }}
    </style>
</head>
<body>
    <h1>Presentations Library</h1>
    <div class="grid">
        {cards}
    </div>
</body>
</html>"""

    (worktree_path / "index.html").write_text(dashboard_html, encoding="utf-8")
    print("[OK] Dashboard updated.")


def sync_shared_media(folder_name, worktree_path):
    """Sync any shared media referenced by the presentation to gh-pages /images/."""
    import re as _re

    json_path = PROJECT_ROOT / "inputs" / folder_name / "presentation.json"
    local_images = PROJECT_ROOT / "images"
    gh_images = worktree_path / "images"

    if not json_path.exists():
        print(f"[WARN] No presentation.json found for {folder_name}")
        return

    if not gh_images.exists():
        gh_images.mkdir(parents=True)

    with open(json_path, "r", encoding="utf-8") as f:
        raw = f.read()

    # Find all /images/xxx references in the JSON
    refs = set(_re.findall(r'/images/([^"\'\\]+)', raw))
    
    copied = 0
    for filename in sorted(refs):
        src = local_images / filename
        dst = gh_images / filename
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
            print(f"  [+] Synced: {filename}")
            copied += 1
        elif not src.exists():
            print(f"  [!] WARNING: {filename} referenced but not found locally")
    
    if copied == 0:
        print("[OK] All shared media already present on gh-pages.")
    else:
        print(f"[OK] Synced {copied} shared media file(s).")


def main():
    if len(sys.argv) < 2:
        print("Usage: python deploy_presentation.py <FOLDER-NAME>")
        print("Example: python deploy_presentation.py 2026-02-09-Frankenstein-B1-Reading")
        sys.exit(1)

    folder_name = sys.argv[1]
    worktree_path = PROJECT_ROOT / ".gh-pages-worktree"

    print(f"[DEPLOY] Deploying: {folder_name}")
    print("=" * 60)

    # Step 1: Verify presentation exists in dist/
    print("[1/5] Verifying presentation build...")
    presentation_src = verify_presentation_exists(folder_name)
    print(f"[OK] Found: {presentation_src}")

    # Step 2: Clean up any stale worktree
    print("[2/5] Preparing gh-pages worktree...")
    if worktree_path.exists():
        run(f'git worktree remove "{worktree_path}" --force', check=False)
        if worktree_path.exists():
            shutil.rmtree(worktree_path, ignore_errors=True)

    # Prune stale worktree metadata (fixes interrupted deploys)
    run("git worktree prune", check=False)

    # Sync local gh-pages with remote to prevent non-fast-forward pushes
    run("git fetch origin gh-pages", check=False)
    run("git branch -f gh-pages origin/gh-pages", check=False)

    # Step 3: Create worktree from gh-pages
    print("[3/5] Checking out gh-pages branch...")
    run(f'git worktree add "{worktree_path}" gh-pages')
    print(f"[OK] Worktree at: {worktree_path}")

    # Step 4: Copy the presentation folder (Self-contained)
    print(f"[4/5] Copying presentation: {folder_name}")
    dest = worktree_path / folder_name
    if dest.exists():
        shutil.rmtree(dest)
    
    # Ignore system files during copy
    def ignore_patterns(path, names):
        return [n for n in names if n.lower() == 'desktop.ini' or n == '.DS_Store' or n == 'Thumbs.db']

    shutil.copytree(presentation_src, dest, ignore=ignore_patterns)
    print(f"[OK] Copied to: {dest}")

    # Step 5: Update dashboard
    print("[5/5] Regenerating dashboard...")
    generate_dashboard(worktree_path)

    # Step 6: Commit and push
    print("[PUSH] Committing and pushing to gh-pages...")
    run("git add -A", cwd=worktree_path)

    # Check if there are changes to commit
    status = run("git status --porcelain", cwd=worktree_path)
    if not status:
        print("[OK] No changes to deploy — gh-pages is already up to date.")
    else:
        run(
            f'git commit -m "deploy: update {folder_name} (bundled)" --no-verify',
            cwd=worktree_path,
        )
        # Pull any remote changes and rebase our commit on top
        run("git pull --rebase origin gh-pages", cwd=worktree_path, check=False)
        run("git push --force origin gh-pages", cwd=worktree_path)
        print("[OK] Pushed to gh-pages.")

    # Cleanup
    run(f'git worktree remove "{worktree_path}" --force', check=False)
    print("=" * 60)
    print(f"[DONE] Live at: https://elwrush.github.io/actions-gh-pages/{folder_name}/")


if __name__ == "__main__":
    main()
