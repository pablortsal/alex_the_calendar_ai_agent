from tools.gmail_setup import get_gmail_service


def mark_email_as_read(message_id):
    """Marca un correo como leído"""
    service = get_gmail_service()  # Obtiene el servicio autenticado de Gmail
    try:
        # Modifica las etiquetas del mensaje para eliminar "UNREAD"
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        print(f"Correo {message_id} marcado como leído.")
    except Exception as e:
        print(f"Error al marcar el correo como leído: {e}")

