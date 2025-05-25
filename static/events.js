const eventSource = new EventSource('/events');

eventSource.onmessage = function(event) {
  const eventsContainer = document.getElementById('events');
  const events = JSON.parse(event.data);
  eventsContainer.innerHTML = '';

  if (events.length === 0) {
    eventsContainer.innerHTML = '<p>Nessun evento disponibile.</p>';
    return;
  }

  const eventsByDate = {};
  events.forEach(e => {
    const eventDate = new Date(e.start).toISOString().split('T')[0];
    if (!eventsByDate[eventDate]) {
      eventsByDate[eventDate] = [];
    }
    eventsByDate[eventDate].push(e);
  });

  const sortedDates = Object.keys(eventsByDate).sort();

  const formatDate = dateStr => {
    const date = new Date(dateStr);
    return String(date.getDate()).padStart(2, '0') + '.' +
           String(date.getMonth() + 1).padStart(2, '0') + '.' +
           date.getFullYear();
  };

  sortedDates.forEach(date => {
    const column = document.createElement('div');
    column.classList.add('event-column');

    const dateHeading = document.createElement('h2');
    dateHeading.textContent = formatDate(date);
    column.appendChild(dateHeading);

    eventsByDate[date].forEach(e => {
      const eventDiv = document.createElement('div');
      eventDiv.classList.add('event');
      eventDiv.innerHTML = `
        <strong>${e.summary}</strong>
        <div class="event-time">${new Date(e.start).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
        <div>${e.description}</div>
      `;
      column.appendChild(eventDiv);
    });

    eventsContainer.appendChild(column);
  });
};

eventSource.onerror = function(error) {
  console.error('Errore nella connessione SSE:', error);
  eventSource.close();
};
