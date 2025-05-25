import hashlib
import requests
import threading
from time import sleep
from datetime import datetime, timedelta, time, timezone
from icalendar import Calendar
from flask import Flask, jsonify, send_from_directory, Response
import json

app = Flask(__name__)

# URL del file .ics
ICS_URL = 'https://peif.esercito.difesa.it/home/agenda@cepolispe.esercito.difesa.it/Calendar.ics'

# Variabile globale per memorizzare il contenuto del file .ics in memoria
ics_content = None

def download_ics():
    """Scarica il file .ics e lo memorizza in memoria solo se è cambiato."""
    global ics_content
    try:
        # Scarica il file ICS
        response = requests.get(ICS_URL, verify=False)  # 'verify=False' se hai un certificato self-signed
        response.raise_for_status()  # Solleva un errore in caso di problemi nel download

        new_file_hash = hashlib.md5(response.content).hexdigest()

        # Se il contenuto è uguale a quello già in memoria, non facciamo nulla
        if ics_content:
            existing_file_hash = hashlib.md5(ics_content).hexdigest()
            if new_file_hash == existing_file_hash:
                return  # Nessun aggiornamento necessario

        # Se il file è nuovo o è cambiato, aggiorna la variabile in memoria
        ics_content = response.content

        # Ottieni la data e ora correnti
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"File .ics aggiornato. ({now})")
    
    except Exception as e:
        print(f"Errore nel download: {e}")

def parse_ics():
    """Legge e parse il file .ics memorizzato in memoria, mostrando solo gli eventi di oggi e dei prossimi 7 giorni (tutto in UTC)."""
    if not ics_content:
        return []

    try:
        cal = Calendar.from_ical(ics_content)
        events = []
        now = datetime.now(timezone.utc)
        today_start = datetime.combine(now.date(), time.min).replace(tzinfo=timezone.utc)
        range_end = today_start + timedelta(days=7, hours=23, minutes=59, seconds=59)

        for component in cal.walk():
            if component.name == "VEVENT":
                start = component.get('dtstart').dt
                end = component.get('dtend').dt if component.get('dtend') else None
                summary = str(component.get('summary', ''))
                description = str(component.get('description', ''))

                # Se start è naive, rendilo UTC-aware
                if isinstance(start, datetime):
                    if start.tzinfo is None:
                        start = start.replace(tzinfo=timezone.utc)
                else:
                    # Se è solo date, trasformalo in datetime in UTC
                    start = datetime.combine(start, time.min).replace(tzinfo=timezone.utc)

                # Stessa cosa per end
                if isinstance(end, datetime):
                    if end.tzinfo is None:
                        end = end.replace(tzinfo=timezone.utc)
                elif end:
                    end = datetime.combine(end, time.min).replace(tzinfo=timezone.utc)

                # Filtro tra oggi e oggi+7 giorni in UTC
                if today_start <= start <= range_end:
                    events.append({
                        'start': start.isoformat(),
                        'end': end.isoformat() if end else None,
                        'summary': summary,
                        'description': description
                    })

        # Ordina per data di inizio
        events.sort(key=lambda e: e['start'])
        return events

    except Exception as e:
        print(f"Errore nel parsing del file .ics: {e}")
        return []

@app.route('/events')
def events_sse():
    """Endpoint SSE per inviare eventi in tempo reale al client."""
    def generate():
        while True:
            # Scarica il file .ics e analizzalo
            download_ics()
            events = parse_ics()

            # Se ci sono eventi, inviali al client
            if events:
                yield f"data: {json.dumps(events)}\n\n"

            sleep(60)  # Ogni 60 secondi

    return Response(generate(), content_type='text/event-stream')

@app.route('/')
def serve_index():
    """Serve la pagina index.html."""
    return send_from_directory('.', 'index.html')

def update_ics_periodically():
    """Controlla periodicamente (ogni 5 minuti) se ci sono aggiornamenti per il file .ics."""
    while True:
        download_ics()  # Scarica il file .ics in memoria
        sleep(60)  # Ogni 60 secondi

if __name__ == '__main__':
    # Avvia il thread per l'aggiornamento periodico
    threading.Thread(target=update_ics_periodically, daemon=True).start()

    # Avvia il server Flask su tutte le interfacce di rete, alla porta 1981
    app.run(host='0.0.0.0', port=1981, threaded=True)
