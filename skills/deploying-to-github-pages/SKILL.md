---
name: deploying-to-github-pages
description: >
  Builds and deploys Reveal.js presentations to GitHub Pages using a clean
  subfolder architecture. Use when the user wants to publish or update
  their live presentations.
---

# Skill: Deploying to GitHub Pages (`deploying-to-github-pages`)

## Description
This skill automates the process of building a production-ready `dist/` directory and preparing it for GitHub Pages deployment. It enforces the "Zero Overwrite" architecture where each lesson lives in its own subfolder and shares a single root-level Reveal.js engine.

## Core Mandates
1.  **Repo Hygiene**: NEVER commit heavy media (>1MB) to both `inputs/` and `dist/`. Build scripts must handle assets according to the Global Asset Pattern.
2.  **Zero Overwrite**: Every presentation must reside in its own unique subfolder (e.g., `https://elwrush.github.io/actions-gh-pages/lesson-name/`).
3.  **Single Engine**: All presentations reference the shared Reveal.js engine at the parent level (`../dist/`, `../plugin/`).
4.  **Automatic Sync**: After a build, the live URL MUST be synchronized back to the Typst lesson plan.

## Architectural Overview

```mermaid
graph TD
    A[inputs/FOLDER/published] -->|Aggregate| B(build_dist.js)
    E[temp_reveal_repo] -->|Copy Engine| B
    B -->|Clean & Populate| C[dist/]
    C -->|Subfolder Structure| D[dist/FOLDER/index.html]
    C -->|Shared Assets| F[dist/dist/]
    B -->|Generate| G[dist/index.html Dashboard]
    D -->|Sync URL| H[Lesson Plan .typ]
```

## Workflow

### 0. Verify Environment
Ensure you are operating in the correct repository (`elwrush/actions-gh-pages`).
```powershell
python scripts/verify_repo.py
```

### 1. Build
Run the build script to aggregate all presentations and the shared engine into the root `dist/` folder:

```powershell
node scripts/build_dist.js
```

The script will:
- Clear the current `dist/` folder.
- Copy the Reveal.js engine (`dist/`, `plugin/`, `css/`) from `temp_reveal_repo` to `dist/`.
- Scan `inputs/` for folders containing `index.html`.
- Copy each into `dist/[folder-name]/`.
- **Fix Paths**: Automatically update `index.html` to reference `../dist/` and `../plugin/`.
- **Copy Shared Assets**: Copy the root `images/` folder to `dist/images/`.
- **Verify Links**: Run the link checker to catch 404 errors before deployment.
- Generate a dashboard at `dist/index.html`.

### 2. Synchronize URL
Update the Typst lesson plan with the live URL:

```powershell
python skills/deploying-to-github-pages/scripts/sync_lesson_plan_url.py [FOLDER-NAME]
```

### 3. Verify
- Open `dist/index.html` locally to check the dashboard and links.

### 4. Commit & Push (Manual Gate)
Ask the user for approval before committing:
> "The build is complete and verified. Shall I commit and push to GitHub Pages?"

If approved, use the **One-Liner** below.

## One-Liner (Fast Deploy)

**Windows cmd.exe compatible:**
```powershell
node scripts/build_dist.js && python scripts/verify_links.py && git add dist/ -f && git commit -m "feat(deploy): update presentations" --no-verify && for /f %s in ('git subtree split --prefix dist main') do set sha=%s && git push origin "%s:gh-pages" --force
```

**PowerShell:**
```powershell
node scripts/build_dist.js; python scripts/verify_links.py; git add dist/ -f; git commit -m "feat(deploy): update presentations" --no-verify; $sha = git subtree split --prefix dist main; git push origin "$sha`:gh-pages" --force
```

## Troubleshooting

### 404 Errors on Engine Assets
Check the `index.html` in the deployed subfolder. Ensure paths like `href="../dist/reveal.css"` are correct and that the `dist/` folder exists at the root of the repository.

### Broken Dashboard Links
Ensure the `FOLDER-NAME` in the dashboard matches the actual folder in `dist/`. The `build_dist.js` handles this automatically by scanning the `inputs/` directory.

## Live URL Pattern
- **Base URL**: `https://elwrush.github.io/actions-gh-pages/`
- **Presentation**: `https://elwrush.github.io/actions-gh-pages/[FOLDER-NAME]/`
