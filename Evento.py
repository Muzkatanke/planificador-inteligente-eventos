from datetime import datetime

class Event:
    def __init__(self, name=None, start=None, end=None):
        self.name = name
        self.start = start
        self.end = end
        self.inclusion = []
        self.exclusion = []
        self.resources = {}
        self.activated = False
        
 
event_names = ["Instalación eléctrica en local", 
               "Mudanza con camión de carga", 
                "Construcción o reparación de inmueble",
                "Mantenimiento de sistemas informáticos o de red", 
                "Montaje de domótica", 
                "Mantenimiento de fontanería"]

event_actives = [] #json

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
    duration = desired_end - desired_start

    while True:
        conflict = False
        blocking_events = []

        for ev in event_actives:
            if ev.start < end and ev.end > start:
                for key, amount in new_event.resources.items():
                    if ev.resources.get(key, 0) > 0:
                        if amount + ev.resources.get(key, 0) > resources[key]:
                            conflict = True
                            blocking_events.append(ev)
                            break  

        if not conflict:
            return start, end
        else:
            earliest_end = None
            for ev in blocking_events:
                if earliest_end is None or ev.end < earliest_end:
                    earliest_end = ev.end

            start = earliest_end
            end = start + duration

def available_amount(key, current_selection, event_actives, resources): #Omitible, CREO
    total = resources[key]

    reserved = 0
    for event in event_actives:
        if not event.activated: 
            reserved += event.resources.get(key, 0)
    reserved += current_selection.get(key, 0)

    return total - reserved