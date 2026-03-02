import os
import sys
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scopes required by the API
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_credentials(credentials_path):
    """Gets valid user credentials from storage or via user flow."""
    creds = None
    token_path = 'token.json'
    
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
            
    return creds

def upload_file(file_path, folder_id, credentials_path):
    """Uploads a file to Google Drive."""
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return None

    if not os.path.exists(credentials_path):
        print(f"Error: Credentials file not found: {credentials_path}")
        return None

    try:
        creds = get_credentials(credentials_path)
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id]
        }
        
        media = MediaFileUpload(file_path, resumable=True)
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        return file
    except Exception as e:
        print(f"Error during upload: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload a file to Google Drive.')
    parser.add_argument('file_path', help='Path to the file to upload')
    parser.add_argument('folder_id', help='Google Drive Folder ID')
    parser.add_argument('--creds', default='.credentials/GDocs-credentials.json', help='Path to credentials JSON')

    args = parser.parse_args()

    result = upload_file(args.file_path, args.folder_id, args.creds)
    
    if result:
        print(f"SUCCESS: File uploaded.")
        print(f"File ID: {result.get('id')}")
        print(f"Link: {result.get('webViewLink')}")
    else:
        sys.exit(1)
