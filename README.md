# CEPOagenda

This project displays upcoming calendar events from an `.ics` file on a fullscreen web interface, suitable for use on TV dashboards.

## Features

- Server-Sent Events (SSE) for real-time event updates
- Parses standard `.ics` calendar files
- Filters events for today and the next 7 days
- Responsive fullscreen display with particle animation
- Built with Python (Flask) and vanilla JavaScript

## Usage

1. Clone the repository
2. Place your `Calendar.ics` file in a local HTTP-accessible location
3. Start the Flask server:

```bash
python agenda.py
```

4. Open your TV browser at http://10.X.X.X:1981

> For TV dashboards, set the browser in fullscreen (F11 on most systems)

## File structure

```
project_root/
├── app.py              # Flask server
├── index.html          # Main frontend
├── static/
│   ├── style.css       # Styles
│   ├── logo.png        # Logo image
│   ├── events.js       # Event rendering logic
│   ├── particles.js    # Particle animation
│   └── icons/          # Favicons
```

## Requirements

- Python 3.8+
- `Flask`
- `icalendar`
- `requests`

Install with:

```bash
pip install flask icalendar requests
```

## Notes

- Tested with self-hosted `.ics` calendars (e.g., Nextcloud, Outlook exports)
- HTTPS verification can be disabled for local `.ics` URLs if needed
