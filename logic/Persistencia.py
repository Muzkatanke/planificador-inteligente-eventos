import json
from pathlib import Path
from datetime import datetime
from logic.Evento import Event

file_path = Path("storage/eventos.json")

def event_to_dict(event):
    return{
        "id": event.id,
        "name": event.name,
        "start": event.start.strftime("%d/%m/%Y %H:%M") if event.start else None,
        "end": event.end.strftime("%d/%m/%Y %H:%M") if event.end else None,
        "resources": event.resources,
        "activated": event.activated
    }

def save_events(event_actives):
    data = [event_to_dict(ev) for ev in event_actives]
    file_path.write_text(json.dumps(data, indent=4), encoding="utf-8")

def dict_to_event(dict_event):
    event = Event()
    event.id = dict_event["id"]
    event.name = dict_event["name"]
    event.start = datetime.strptime(dict_event["start"], "%d/%m/%Y %H:%M") if dict_event["start"] else None
    event.end = datetime.strptime(dict_event["end"], "%d/%m/%Y %H:%M") if dict_event["end"] else None
    event.resources = dict_event["resources"]
    event.activated = dict_event["activated"]
    return event

def load_events():
    if not file_path.exists():
        return []

    contents = file_path.read_text(encoding="utf-8")
    data = json.loads(contents)

    events = []
    max_id = 0

    for dict in data:
        event = dict_to_event(dict)
        events.append(event)
        max_id = max(max_id, event.id)

    Event._id_counter = max_id + 1
    return events
