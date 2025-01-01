from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

# Ámbitos necesarios para Gmail y Google Calendar
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',  # Gmail
    'https://www.googleapis.com/auth/calendar'       # Calendar
]

def authenticate_services():
    """Autenticación combinada para Gmail y Google Calendar"""
    creds = None
    
    # Carga las credenciales desde token.json
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Si las credenciales no son válidas o expiraron, renueva
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Inicia el flujo de autenticación
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Guarda las credenciales actualizadas
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # Devuelve las credenciales autenticadas
    return creds

def get_gmail_service():
    """Devuelve el cliente autenticado de Gmail"""
    creds = authenticate_services()
    return build('gmail', 'v1', credentials=creds)

def get_calendar_service():
    """Devuelve el cliente autenticado de Google Calendar"""
    creds = authenticate_services()
    return build('calendar', 'v3', credentials=creds)


if __name__ == "__main__":
    gmail_service = get_gmail_service()
    calendar_service = get_calendar_service()
    print("Autenticación completada y servicio configurado correctamente.")