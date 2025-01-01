import base64
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError

from tools.gmail_setup import get_gmail_service

def reply_to_email(message_id, recipient_email, subject, body):
    """Reply to an email with the given message_id, recipient_email, subject and body."""
    service = get_gmail_service()
    print(f"Answering mail by {recipient_email} with subjevt '{subject}' and body '{body}'...")
    try:
        original_message = service.users().messages().get(userId='me', id=message_id, format='metadata').execute()
        from_email = original_message['payload']['headers'][0]['value']

        reply_message = MIMEText(body)
        reply_message['to'] = recipient_email
        reply_message['from'] = from_email
        reply_message['subject'] = f"Re: {subject}"
        reply_message['in-reply-to'] = message_id
        reply_message['references'] = message_id
        raw = base64.urlsafe_b64encode(reply_message.as_bytes()).decode()

        message = {
            'raw': raw,
            'threadId': original_message['threadId']
        }
        service.users().messages().send(userId='me', body=message).execute()
        print(f"Answer send {recipient_email}")
    except HttpError as error:
        print(f"Error answering the email: {error}")
    except Exception as e:
        print(f"Error answering the email: {e}")