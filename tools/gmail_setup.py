from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',  # Gmail
    'https://www.googleapis.com/auth/calendar'       # Calendar
]

def authenticate_services():
    """Autenticación combinada para Gmail y Google Calendar"""
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def get_gmail_service():
    """Get the authenticated Gmail client"""
    creds = authenticate_services()
    return build('gmail', 'v1', credentials=creds)

def get_calendar_service():
    """Get the authenticated Calendar client"""
    creds = authenticate_services()
    return build('calendar', 'v3', credentials=creds)


if __name__ == "__main__":
    gmail_service = get_gmail_service()
    calendar_service = get_calendar_service()
    print("Gmail and Calendar services authenticated successfully!")