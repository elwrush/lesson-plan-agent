---
name: writing-logs
description: Safely updates project documentation (errors-fix.md and session-log.md) without overwriting history.
---

# Writing Logs

## Purpose
To maintain a historical record of system errors, fixes, and session achievements without risking data loss through full-file overwrites or fragile "replace" logic.

## Usage
Use the `scripts/append_log.py` utility to append entries.

### 1. Updating `errors-fix.md`
Log specific technical errors, their root causes, and the applied fixes.

```bash
python scripts/append_log.py errors "
## [Date] | [Title]

### [Issue Title]
- **Issue**: ...
- **Cause**: ...
- **Fix**: ...
"
```

### 2. Updating `session-log.md`
Log high-level achievements, workflow changes, or new standards established during the session.

```bash
python scripts/append_log.py session "
## [Date] | [Session Goal]

### [Category]
- Details...
"
```

### 3. Using Temp Files for Long Content (Recommended)
For long entries (multiple lines/paragraphs), write the content to a temporary text file first, then import it.

1.  Write content to `temp_log.txt`.
2.  Run:
    ```bash
    python scripts/append_log.py session @temp_log.txt
    ```
3.  Delete `temp_log.txt`.

## Guidelines
-   **Atomic entries**: Each log entry should be self-contained.
-   **No Overwrites**: NEVER use `write_to_file` on log files unless you have read the ENTIRE content first and are re-writing it 100% loss-free (discouraged).
-   **Header Format**: Always start a new session entry with `## YYYY-MM-DD | Title`.
