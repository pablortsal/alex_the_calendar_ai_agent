from tools.gmail_setup import get_gmail_service
def list_unread_emails():
    """List all unread emails from the inbox."""
    service = get_gmail_service()
    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
        messages = results.get('messages', [])
        
        if not messages:
            print("No new mails")
            return []
        
        print(f"Found {len(messages)} unread emails.")
        return messages
    except Exception as e:
        print(f"Error while retriving unreads emails: {e}")
        return []
    