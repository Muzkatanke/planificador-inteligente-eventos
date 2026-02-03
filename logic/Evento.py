from datetime import datetime

class Event:
    _id_counter = 1 

    def __init__(self):
        self.id = Event._id_counter
        Event._id_counter += 1
        self.name = None
        self.start = None
        self.end = None
        self.resources = {}
        self.activated = False
        
 
event_names = ["Instalación eléctrica en local", 
               "Mudanza con camión de carga", 
                "Construcción o reparación de inmueble",
                "Mantenimiento de sistemas informáticos o de red", 
                "Montaje de domótica", 
                "Mantenimiento de fontanería"]

def ask_date(message):
    while True:
        date_str = input(message)
        try:
            date = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
            return date
        except ValueError:
            print("Formato inválido. Usa dd/mm/aaaa hh:mm (ejemplo: 20/12/2025 18:30)")

def find_available_start(new_event, desired_start, desired_end, event_actives, resources):
    start = desired_start
    end = desired_end
    duration = end - start   

    while True:
        conflict = False
        total_usage = {key: 0 for key in resources.keys()}

        for ev in event_actives:
            if start < ev.end and ev.start < end:
                for key, ev_amount in ev.resources.items():
                    total_usage[key] += ev_amount

        for key, amount in new_event.resources.items():
            if total_usage.get(key, 0) + amount > resources[key]:
                conflict = True
                break

        if not conflict:
            return start, end

        try:
            latest_end = max(
                ev.end
                for ev in event_actives
                if start < ev.end and ev.start < end
            )
        except ValueError:
            raise ValueError("No hay espacio disponible para programar el evento sin solapamiento.")

        start = latest_end
        end = start + duration

        if end <= start:
            raise ValueError("No hay espacio disponible para programar el evento sin solapamiento.")


def available_amount(key, current_selection, event_actives, resources):
    total = resources[key]

    reserved = 0
    for event in event_actives:
        reserved += event.resources.get(key, 0)

    reserved += current_selection.get(key, 0)

    return total - reserved

def available_amount_interval(key, current_selection, event_actives, resources, start, end):
    total = resources[key]
    
    reserved = 0
    reserved += current_selection.get(key, 0)
    for event in event_actives:
        if start < event.end and event.start < end:
            reserved += event.resources.get(key, 0)

    return total - reserved

