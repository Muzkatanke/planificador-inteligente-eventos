from datetime import datetime
from logic.Datos import resources

def activate_events(event_actives):
    now = datetime.now()

    for event in event_actives:
        if not event.activated and event.start <= now:
            for key, amount in event.resources.items():
                if resources[key] < amount:
                    print(f"No hay suficientes {key} para '{event.name}'.")
                    return
            for key, amount in event.resources.items():
                resources[key] -= amount
            event.activated = True
            print(f"Evento '{event.name}' ACTIVADO.")

def desactivate_events(event_actives):
    now = datetime.now()

    for event in event_actives:
        if event.activated and event.end <= now:
            for key, amount in event.resources.items():
                resources[key] += amount
            event.activated = False
            print(f"Evento '{event.name}' FINALIZADO.")
