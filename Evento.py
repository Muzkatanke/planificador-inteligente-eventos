from datetime import datetime
from Recursos import * 
import os

class Event:
    def __init__(self, name=None, start=None, end=None):
        self.name = name
        self.start = start
        self.end = end
        self.inclusion = []
        self.exclusion = []
        self.resources = {}
        self.activated = False
        
 
event_names = ["Instalación eléctrica en local", "Mudanza con camión de carga", 
                "Construcción o reparación de inmueble",
                "Mantenimiento de sistemas informáticos o de red", "Montaje de domótica", "Mantenimiento de fontanería"]

event_actives = [] #json

def activate_events():
    now = datetime.now()

    for event in event_actives:
        if event.start <= now and not event.activated:
            for key, value in event.resources.items():
                resources[key] -= value
            event.activated = True
            print(f"El evento '{event.name}' ha comenzado y se asignaron sus recursos.")

def activate_events():
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

def deactivate_events():
    now = datetime.now()

    for event in event_actives:
        if event.end <= now and event.activated:
            for key, value in event.resources.items():
                resources[key] += value
            event.activated = False
            print(f"El evento '{event.name}' ha finalizado y se liberaron sus recursos.")


def ask_date(message):
    while True:
        date_str = input(message)
        try:
            date = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
            return date
        except ValueError:
            print("Formato inválido. Usa dd/mm/aaaa hh:mm (ejemplo: 20/12/2025 18:30)")

def find_available_start(new_event, desired_start, desired_end):
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

def available_amount(key, current_selection): #Omitible, CREO
    total = resources[key]

    reserved = 0
    for event in event_actives:
        if not event.activated: 
            reserved += event.resources.get(key, 0)
    
    reserved += current_selection.get(key, 0)

    return total - reserved

def add_event():
    new_event = Event()

    print("SELECCIONE UN EVENTO")
    print("1.Instalación eléctrica en local\n"+
          "2.Mudanza con camión de carga\n"+
          "3.Construcción o reparación de inmueble\n"+
          "4.Mantenimiento de sistemas informáticos o de red\n"+
          "5.Montaje de domótica\n")
    
    choice = int(input())
    new_event.name = event_names[choice-1]
    
    os.system("cls")

    while True:
        desired_start = ask_date("Escriba la fecha de inicio del evento (dd/mm/aaaa hh:mm): ")
        desired_end = ask_date("Escriba la fecha de culminación del evento (dd/mm/aaaa hh:mm): ")
    
        if desired_end <= desired_start:
            print("La fecha de finalización debe ser despúes de la de inicialización.")
            input("Presiona la tecla Enter para continuar...")
            os.system("cls")
            continue

        now = datetime.now()
        if desired_start < now: 
            print("No se pueden programar eventos en el pasado.")
            input("Presiona la tecla Enter para continuar...")
            os.system("cls")
            continue

        break

    print(f"El evento '{new_event.name}' ha sido programado desde {desired_start.strftime('%d/%m/%Y %H:%M')} hasta {desired_end.strftime('%d/%m/%Y %H:%M')}")
    input("Presiona la tecla Enter para continuar...")
    os.system("cls")

    while True:
        print("ELIJA LOS RECURSOS DEL EVENTO (0 para terminar)")
        print("(Recurso : cantidad)")   

        cont = 1
        for key in resources.keys():
            current_availability = available_amount(key, new_event.resources)

            if current_availability == 0:
                print(f"{cont}.{key} : [NO DISPONIBLE]")
            else:
                print(f"{cont}.{key} : {current_availability}")

            cont += 1

        option = int(input("\nElige el número del producto: "))
        if option == 0:
            if not new_event.resources:
                print("Debe asignar al menos un recurso al evento.")
                continue
            new_event.start, new_event.end = find_available_start(new_event, desired_start, desired_end)
            event_actives.append(new_event)
            break
            
        key_selected = list(resources.keys())[option - 1]
        ##check_inclusion(key_selected, new_event_resources)  
        ##check_exclusion() 

        if resources[key_selected] == 0:
            print(f"El recurso '{key_selected}' no está disponible.")
            input("Presiona Enter para continuar...")
            os.system("cls")
            continue

        current_availability = available_amount(key_selected, new_event.resources)
        amount = int(input(f"Ingrese la cantidad para {key_selected}: "))
    
        while amount < 0 or amount > current_availability:
            amount = int(input(f"Ingrese un valor entre 0 y {current_availability} para {key_selected}: "))
        
        new_event.resources[key_selected] = new_event.resources.get(key_selected, 0) + amount
       
        os.system("cls")
        print(f"\nHas agregado {amount} '{key_selected}'")
        input("Presiona la tecla Enter para continuar...")
        os.system("cls")
        print("Recursos seleccionados:")
        print(new_event.resources)

def remove_event():
    if not event_actives:
        os.system("cls")
        print("No hay eventos activos que eliminar")
        input("Presiona la tecla Enter para continuar...")
        os.system("cls")
        return
    
    print("ELIJA QUE EVENTO ELIMINAR (0 para terminar)")
    cont = 1
    for event in event_actives:
        print(f"{cont}.{event.name}")
        cont += 1

    option = int(input("\nElige el número del producto: "))
    event_actives[option - 1]
    if option == 0:
        os.system("cls")
        return
    else:
        os.system("cls")
        for key, value in event.resources.items():
                resources[key] += value
        event_actives.pop(option - 1)

        print(f"Se recuperaron {event.resources}")
        input("Presiona la tecla Enter para continuar...")
        os.system("cls")

def view_events():
    if not event_actives:
        os.system("cls")
        print("No hay eventos activos que ver")
        input("Presiona la tecla Enter para continuar...")
        os.system("cls")
        return
    
    for event in event_actives:
        print(f"{event.name}: Programado desde {event.start} hasta {event.end}. \nUtilizando los recursos: {event.resources}")
        
    input("Presiona la tecla Enter para continuar...")
    os.system("cls")

# Meter json
# Meter inclusion y exclusion de recursos 