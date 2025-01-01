import base64
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError

from tools.gmail_setup import get_gmail_service

def reply_to_email(message_id, recipient_email, subject, body):
    """Responde a un correo específico"""
    service = get_gmail_service()
    print(f"Respondiendo al correo de {recipient_email} con asunto '{subject}' y body '{body}'...")
    try:
        # Obtener el correo original para obtener el remitente
        original_message = service.users().messages().get(userId='me', id=message_id, format='metadata').execute()
        from_email = original_message['payload']['headers'][0]['value']

        # Crear el mensaje
        reply_message = MIMEText(body)
        reply_message['to'] = recipient_email
        reply_message['from'] = from_email
        reply_message['subject'] = f"Re: {subject}"
        reply_message['in-reply-to'] = message_id
        reply_message['references'] = message_id
        raw = base64.urlsafe_b64encode(reply_message.as_bytes()).decode()

        # Enviar la respuesta
        message = {
            'raw': raw,
            'threadId': original_message['threadId']
        }
        service.users().messages().send(userId='me', body=message).execute()
        print(f"Respuesta enviada a {recipient_email}")
    except HttpError as error:
        print(f"Error al responder el correo: {error}")
    except Exception as e:
        print(f"Error al responder el correo: {e}")