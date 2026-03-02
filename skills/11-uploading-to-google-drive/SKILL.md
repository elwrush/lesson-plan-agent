---
name: 11-uploading-to-google-drive
description: Uploads files to a specified Google Drive folder using service account credentials. Use when the user requests to upload PDFs, lesson plans, or other artifacts to Google Drive.
---

# Uploading to Google Drive

## Purpose
This skill automates the process of uploading local files to a specific Google Drive folder using the Google Drive API and a service account.

## Workflow
1. **Identify the File**: Determine the path of the file to be uploaded (e.g., a recently compiled PDF).
2. **Identify the Folder ID**: Extract the Folder ID from the Google Drive link provided by the user.
   - Example Link: `https://drive.google.com/drive/folders/1YoiHmadJku4FkB4qov6QLGIKQTfLiYmW`
   - Folder ID: `1YoiHmadJku4FkB4qov6QLGIKQTfLiYmW`
3. **Execute Upload**: Use the `upload_to_drive.py` script to perform the upload.

## Commands
```powershell
python skills/uploading-to-google-drive/scripts/upload_to_drive.py "[FILE_PATH]" "[FOLDER_ID]" --creds ".credentials/GDocs-credentials.json"
```

## Prerequisites
- Service account credentials JSON must be present at `.credentials/GDocs-credentials.json`.
- Python libraries required: `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`.

## Error Handling
- If the credentials file is missing, inform the user.
- If the upload fails due to missing permissions, ensure the service account email has been shared with the target Google Drive folder.
