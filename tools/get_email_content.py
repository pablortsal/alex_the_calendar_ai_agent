import base64
import re
from tools.gmail_setup import get_gmail_service

def get_email_content(message_id):
    """Obtiene y decodifica el contenido de un correo por su ID"""
    service = get_gmail_service()
    try:
        message = service.users().messages().get(userId='me', id=message_id).execute()
        payload = message['payload']
        headers = payload['headers']
        subject = ""
        sender = ""

        # Obtener el asunto y el remitente del correo
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'To':
                sender = header['value']
                email_match = re.search(r'<(.+?)>', sender)
                if email_match:
                    sender = email_match.group(1)
        
        # Obtener el cuerpo del correo
        parts = payload.get('parts', [])
        body = ""
        for part in parts:
            if part['mimeType'] == 'text/plain':  # Asegúrate de procesar solo texto plano
                body = part['body']['data']
                body = base64.urlsafe_b64decode(body).decode('utf-8')  # Decodificar Base64
                break
        
        print(f"Asunto: {subject}")
        print(f"De: {sender}")
        print(f"Cuerpo: {body}")
        return subject, sender, body
    except Exception as e:
        print(f"Error al obtener el contenido del correo: {e}")
        return None, None, None
    