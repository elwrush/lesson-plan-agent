# Skill: Deploy to Cloudflare Library (`deploy-to-cloudflare`)

## Description
This skill handles the publishing of HTML presentations to the **Cloudflare Pages Lesson Library**. It ensures that new lessons are added to the persistent `presentations/` folder, the index menu is updated, and the changes are pushed to GitHub for automatic deployment.

## Context
Use this skill when:
- An HTML presentation has been generated (e.g., in `inputs/`).
- The user wants to "publish" or "host" the lesson.
- The user needs a live URL for the classroom.

## Prerequisites
- **Git Repository**: Must be connected to Cloudflare Pages (`lesson-plan-agent`).
- **Directory Structure**:
    - `presentations/` (Root for Cloudflare)
    - `presentations/index.html` (Menu)
- **Local Sync Path**: `G:\My Drive\A CLASSES- ED - TERM 2\M24A - M3-3A`

## Workflow

```mermaid
graph TD
    A[Start: Finished Presentation] --> B{Clean 'node_modules'?}
    B -- Yes --> C[Remove dependency folders]
    B -- No --> C
    C --> D[Rename folder to DD-MM-YY_Name]
    D --> E[Move to 'presentations/' directory]
    E --> F[Update 'presentations/index.html']
    F --> G[Git Add / Commit / Push]
    G --> H[Cloudflare Auto-Deploys]
    H --> I[Copy .txt link to G: Drive path]
    I --> J[End]
```

### 1. Preparation
Ensure the presentation is lightweight (CDN links, no local `node_modules`).

### 2. Standardization
Rename the folder to the strict date format: `DD-MM-YY_Descriptive-Name`.

### 3. Integration
1.  Move the folder into `presentations/`.
2.  Add a generic HTML link card to `presentations/index.html`.

### 4. Deployment & Archiving
1.  Execute the Git commands to trigger the Cloudflare build.
    ```bash
    git add presentations/
    git commit -m "feat: publish lesson [DATE]"
    git push origin main
    ```
2.  Create a `.txt` file named **`DD-MM-YYYY-slideshow-link-[detail].txt`** containing the individual lesson URL.
3.  **Copy** this file to the locally mapped Google Drive:
    `G:\My Drive\A CLASSES- ED - TERM 2\M24A - M3-3A`
