from tools.create_meeting_event import create_meeting
from tools.list_unread_mails import list_unread_emails
from tools.get_email_content import get_email_content
from tools.mark_email_as_read import mark_email_as_read
from tools.reply_to_email import reply_to_email
from tools.mark_email_as_read import mark_email_as_read
from time import sleep
from datetime import datetime, timedelta
# new
from openai import OpenAI
import os
from dotenv import load_dotenv
api_key = os.getenv("OPENAI_API_KEY")

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
client = OpenAI(
  api_key=api_key,  # this is also the default, it can be omitted
)


def interpret_email_with_gpt(email_body, conversation_history=""):
    """Usa GPT para interpretar el contenido del correo y continuar la conversación"""
   
    prompt = f"""
    Aquí tienes un correo electrónico recibido y una breve historia de la conversación hasta ahora.
    Tu tarea es:
    1. Analizar si el correo menciona fechas, horas o disponibilidad para una reunión.
    2. Si no hay una solicitud de reunión clara, continuar la conversación preguntando por disponibilidad.
    3. Proponer opciones claras de reunión si tienes suficiente información.

    Devuelve un JSON con el siguiente formato:
    {{
        "action": "schedule_meeting" o "continue_conversation",
        "details": {{
            "date": "2024-01-02",
            "time": "15:00",
            "description": "Reunión para discutir el proyecto"
        }},
        "reply_message": "Texto del mensaje que se enviará al remitente."
    }}

    Historia de la conversación:
    {conversation_history}

    Correo recibido:
    {email_body}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente que ayuda a programar reuniones."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250,
        temperature=0.7
    )
    return response.choices[0].message.content

def process_email(message_id, sender, subject, body, conversation_history=""):
    print(message_id, sender, subject, body)
    """Procesa un correo usando GPT y ejecuta la acción adecuada"""
    try:
        # Interpretar el correo con GPT
        gpt_response = interpret_email_with_gpt(body, conversation_history)
        print("Respuesta de GPT:", gpt_response)

        # Convertir la respuesta de GPT en un diccionario
        response_data = eval(gpt_response)
        print("Datos de respuesta:", response_data)
        # Ejecutar la acción según la respuesta de GPT
        if response_data["action"] == "schedule_meeting":
            # Crear la reunión
            meeting_details = response_data["details"]
            start_time = datetime.strptime(f"{meeting_details['date']} {meeting_details['time']}", "%Y-%m-%d %H:%M")
            end_time = start_time + timedelta(hours=1)

            print(f"Creando reunión con {sender} el {meeting_details['date']} a las {meeting_details['time']}...")
            create_meeting(
                event_title=meeting_details["description"],
                event_description=meeting_details["description"],
                start_time=start_time,
                end_time=end_time,
                attendees=[sender]
            )
            print(f"Reunión creada con {sender} el {meeting_details['date']} a las {meeting_details['time']}")
            # Responder al correo confirmando la reunión
            reply_to_email(
                message_id=message_id,
                recipient_email=sender,
                subject=subject,
                body=response_data["reply_message"]
            )
        elif response_data["action"] == "continue_conversation":
            # Responder al correo para continuar la conversación
            reply_to_email(
                message_id=message_id,
                recipient_email=sender,
                subject=subject,
                body=response_data["reply_message"]
            )
    except Exception as e:
        print(f"Error al procesar el correo: {e}")

def process_unread_emails():
    """Lee correos no leídos y los procesa uno por uno"""
    messages = list_unread_emails()
    if not messages:
        return

    # Mantener historial de la conversación
    conversation_history = ""

    for message in messages:
        message_id = message['id']
        subject, sender, body = get_email_content(message_id)

        if sender and body:
            print(f"Procesando correo de {sender} con asunto '{subject}'...")
            # Actualizar el historial de la conversación
            conversation_history += f"\nDe: {sender}\n{body}\n"
            process_email(message_id, sender, subject, body, conversation_history)

        # Marca el correo como leído después de procesarlo
        mark_email_as_read(message_id)

if __name__ == "__main__":
    print("Iniciando el agente para procesar correos no leídos...")
    while True:
        try:
            process_unread_emails()
            sleep(60)  # Revisa los correos cada minuto
        except KeyboardInterrupt:
            print("Agente detenido.")
            break
        except Exception as e:
            print(f"Error en el agente: {e}")
            sleep(60)  # Espera un minuto antes de intentar de nuevo