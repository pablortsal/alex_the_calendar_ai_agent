import base64
import re
from tools.gmail_setup import get_gmail_service

def get_email_content(message_id):
    """Get Email content from a given message_id."""
    service = get_gmail_service()
    try:
        message = service.users().messages().get(userId='me', id=message_id).execute()
        payload = message['payload']
        headers = payload['headers']
        subject = ""
        sender = ""

        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'To':
                sender = header['value']
                email_match = re.search(r'<(.+?)>', sender)
                if email_match:
                    sender = email_match.group(1)
        
        parts = payload.get('parts', [])
        body = ""
        for part in parts:
            if part['mimeType'] == 'text/plain':  
                body = part['body']['data']
                body = base64.urlsafe_b64decode(body).decode('utf-8') 
                break
        
        print(f"Subject: {subject}")
        print(f"From: {sender}")
        print(f"Body: {body}")
        return subject, sender, body
    except Exception as e:
        print(f"Error while getting the email content: {e}")
        return None, None, None
    