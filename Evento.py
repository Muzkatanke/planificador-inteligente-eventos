from datetime import datetime

class Event:
    _id_counter = 1 

    def __init__(self, name=None, start=None, end=None):
        self.id = Event._id_counter 
        Event._id_counter += 1
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

    while True:
        conflict = False
        blocking_events = []

        for ev in event_actives:
            if start < ev.end and ev.start < end:
                for key, amount in new_event.resources.items():
                    ev_amount = ev.resources.get(key, 0)
                    if ev_amount > 0 and amount + ev_amount > resources[key]:
                        conflict = True
                        blocking_events.append(ev)
                        break  

        if not conflict:
            return start, end
        else:
            earliest_start = min(ev.start for ev in blocking_events)
            end = earliest_start
            if end <= start:
                raise ValueError("No hay espacio disponible para programar el evento sin solapamiento.")



def available_amount(key, current_selection, event_actives, resources): #Omitible, CREO
    total = resources[key]

    reserved = 0
    for event in event_actives:
        if not event.activated: 
            reserved += event.resources.get(key, 0)
    reserved += current_selection.get(key, 0)

    return total - reserved