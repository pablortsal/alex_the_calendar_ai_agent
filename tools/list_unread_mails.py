from tools.gmail_setup import get_gmail_service
def list_unread_emails():
    """Lista los correos no leídos en la bandeja de entrada"""
    service = get_gmail_service()
    try:
        # Busca correos no leídos en la bandeja de entrada
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
        messages = results.get('messages', [])
        
        if not messages:
            print("No hay correos nuevos.")
            return []
        
        print(f"Se encontraron {len(messages)} correos no leídos.")
        return messages
    except Exception as e:
        print(f"Error al obtener correos no leídos: {e}")
        return []
    