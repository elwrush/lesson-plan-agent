---
name: saving-source-code
description: >
  Commits and pushes the project source code to the 'lesson-plan-agent' repository.
  Excludes deployment artifacts (dist/) and system junk (desktop.ini).
  Use when the user wants to save their work, back up the project, or commit changes.
---

# Skill: Saving Source Code (`saving-source-code`)

## Description
This skill manages the version control for the **project source code** (Skills, Scripts, Inputs). It targets the `lesson-plan-agent` repository, distinct from the deployment repository (`actions-gh-pages`).

## Core Mandates
1.  **Target Repository**: Must push to `https://github.com/elwrush/lesson-plan-agent.git` (remote: `source`).
2.  **Exclusion Protocols**:
    *   **NEVER** commit `dist/` (Deployment Artifacts).
    *   **NEVER** commit `desktop.ini` (GDrive Artifacts).
3.  **Context**: This is for *saving work*, not *publishing slides*.

## Workflow

### 1. Remote Verification
Ensure the `source` remote is configured.
```powershell
git remote add source https://github.com/elwrush/lesson-plan-agent.git
# Ignore error if it already exists
```

### 2. Staging & Cleaning
Stage changes while aggressively filtering junk.

```powershell
# 0. Pre-Flight Sanitize (CRITICAL for GDrive)
# Removes system files that may have been created by cloud sync, even in .git/
Get-ChildItem -Path . -Recurse -Include desktop.ini,Thumbs.db,.DS_Store -Force -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue

# 1. Add everything
git add .

# 2. Explicitly unstage Forbidden Artifacts (Double Check)
git reset dist/
git reset **/desktop.ini
```

### 3. Commit
Commit with a descriptive message provided by the user or generated from context.

```powershell
git commit -m "[Type]: [Description]"
```

### 4. Push to Source
Push to the `lesson-plan-agent` repository.

```powershell
git push source main
```

## One-Liner (Fast Save)

```powershell
Get-ChildItem -Path . -Recurse -Include desktop.ini,Thumbs.db,.DS_Store -Force -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue; git remote add source https://github.com/elwrush/lesson-plan-agent.git; git add .; git reset dist/ **/desktop.ini; git commit -m "chore: save work"; git push source main
```
