---
description: Verbose, versioned commitals to the GitHub repository
---

# Commit Project Workflow

This workflow activates the specialized skill for high-quality, descriptive commits to the [lesson-plan-agent](https://github.com/elwrush/lesson-plan-agent.git) repository.

## Steps

1.  **Activate Skill**: Refer to [committing-project-to-github/SKILL.md](../../skills/committing-project-to-github/SKILL.md) for standards.
2.  **Verify Status**: check `git status`.
3.  **Filter Assets**: 
    // turbo
    ```powershell
    git reset **/desktop.ini
    ```
4.  **Compose & Push**: Stage all valid files and commit with a verbose message reflecting the progress in `session-log.md`.
