from tools.gmail_setup import get_gmail_service

def mark_email_as_read(message_id):
    """Mark an email as read."""
    service = get_gmail_service() 
    try:
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        print(f"Email {message_id} marked as read.")
    except Exception as e:
        print(f"Error trying to mark email as read: {e}")

