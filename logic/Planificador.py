from datetime import datetime
from Recursos import resources

def activate_events(event_actives):
    now = datetime.now()

    for event in event_actives:
        if event.start <= now and not event.activated:
            enough = True
            for key, value in event.resources.items():
                if resources[key] < value:
                    print(f"Error: no hay suficientes '{key}' para activar el evento '{event.name}'.")
                    enough = False
                    break
            if enough:
                for key, value in event.resources.items():
                    resources[key] -= value
                event.activated = True
                print(f"El evento '{event.name}' ha comenzado y se asignaron sus recursos.")

def desactivate_events(event_actives):
    now = datetime.now()

    for event in event_actives:
        if event.end <= now and event.activated:
            for key, value in event.resources.items():
                resources[key] += value
            event.activated = False
            print(f"El evento '{event.name}' ha finalizado y se liberaron sus recursos.")
