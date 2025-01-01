from tools.gmail_setup import get_calendar_service

def create_meeting(event_title, event_description, start_time, end_time, attendees):
    """Crea un evento en Google Calendar"""
    print(f"Creando reunión: {event_title} de {start_time} a {end_time} con {attendees}")
    service = get_calendar_service()  # Asegúrate de que ya tienes autenticación configurada para Calendar
    try:
        # Configuración del evento
        event = {
            'summary': event_title,
            'description': event_description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'attendees': [{'email': email} for email in attendees],
        }

        # Crear el evento
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Reunión agendada: {event.get('htmlLink')}")
        return event
    except Exception as e:
        print(f"Error al agendar la reunión: {e}")
        return None