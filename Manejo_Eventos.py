import os
from datetime import datetime
from Recursos import resources, check_exclusion, check_inclusion
from Evento import Event, event_names, ask_date, find_available_start, available_amount

event_actives = []

def alert(message):
    os.system("cls")
    print(message)
    input("Presiona Enter para continuar...")
    os.system("cls")

import os
from datetime import datetime
from Recursos import resources, check_exclusion, check_inclusion
from Evento import Event, event_names, ask_date, find_available_start, available_amount

event_actives = []

def alert(message):
    os.system("cls")
    print(message)
    input("Presiona Enter para continuar...")
    os.system("cls")

def add_event():
    new_event = Event()
   
    print("SELECCIONE UN EVENTO")
    print("1.Instalación eléctrica en local\n"+
          "2.Mudanza con camión de carga\n"+
          "3.Construcción o reparación de inmueble\n"+
          "4.Mantenimiento de sistemas informáticos o de red\n"+
          "5.Montaje de domótica\n"+
          "6.Mantenimiento de fontanería\n")
    
    try: 
        choice = int(input("Ingrese el número del evento: ")) 
        if choice < 1 or choice > len(event_names): 
            alert("Opción inválida.") 
            return 
    except ValueError: 
        alert("Debe ingresar un número válido.") 
        return
    
    new_event.name = event_names[choice-1]
    os.system("cls")

    if not check_inclusion(new_event.name, new_event.resources, event_actives, resources):
        alert(f"No se puede realizar el evento '{new_event.name}' porque no hay recursos obligatorios disponibles.")
        return

    print("Recursos obligatorios asignados automáticamente:")
    print(new_event.resources)
    input("Presiona Enter para continuar...")
    os.system("cls")

    excluded = check_exclusion(new_event.name)

    while True:
        print("ELIJA LOS RECURSOS DEL EVENTO (0 para terminar)")
        print("(Recurso : cantidad)")   

        cont = 1
        for key in resources.keys():
            if key in excluded:
                print(f"{cont}.{key} : [EXCLUIDO]") 
            else: 
                current_availability = available_amount(key, new_event.resources, event_actives, resources) 
                if current_availability <= 0:
                    print(f"{cont}.{key} : [NO DISPONIBLE]")
                else:
                    print(f"{cont}.{key} : {current_availability}")
            cont += 1

        try: 
            option = int(input("\nElige el número del recurso: ")) 
        except ValueError: 
            alert("Debe ingresar un número válido.") 
            continue

        if option == 0:
            if not new_event.resources:
                alert("Debe asignar al menos un recurso al evento.")
                continue
            break
            
        if option < 1 or option > len(resources): 
            alert("Opción inválida.") 
            continue

        resource_selected = list(resources.keys())[option - 1]

        if resource_selected in excluded:
            alert(f"El recurso '{resource_selected}' ha sido excluído debido a la naturaleza del evento.")
            continue

        current_availability = available_amount(resource_selected, new_event.resources, event_actives, resources) 

        if current_availability <= 0:
            max_amount = resources[resource_selected]
            current_assigned = new_event.resources.get(resource_selected, 0)

            if current_assigned >= max_amount:
                alert(f"Ya tienes asignados {current_assigned} '{resource_selected}', "
                      f"que es el máximo permitido. No puedes añadir más.")
                continue

            alert(f"El recurso '{resource_selected}' no está disponible actualmente.\n"
                  "Si lo selecciona, el evento deberá reprogramarse hasta que esté libre.")
            confirm = input("¿Desea reprogramar el evento para usar este recurso? (s/n): ")
            if confirm.lower() != "s":
                continue

            max_remaining = max_amount - current_assigned
            while True:
                try:
                    amount = int(input(f"Ingrese un valor entre 0 y {max_remaining} para {resource_selected} "
                                       "(0 para cancelar): "))
                    if amount == 0:
                        alert(f"No se agregó '{resource_selected}' (acción cancelada).")
                        break
                    if 1 <= amount <= max_remaining:
                        new_event.resources[resource_selected] = current_assigned + amount
                        alert(f"Has agregado {amount} '{resource_selected}' (evento será reprogramado).")
                        break
                    else:
                        alert(f"Debe ingresar un valor entre 0 y {max_remaining}")
                except ValueError:
                    alert(f"Debe ingresar un valor entre 0 y {max_remaining}")
            continue

        while True:
            try:
                amount = int(input(f"Ingrese un valor entre 0 y {current_availability} para {resource_selected} "
                                   "(0 para cancelar): "))
                if amount == 0:
                    alert(f"No se agregó '{resource_selected}' (acción cancelada).")
                    break
                if 0 <= amount <= current_availability:
                    max_amount = resources[resource_selected]
                    current_assigned = new_event.resources.get(resource_selected, 0)
                    if current_assigned + amount > max_amount:
                        alert(f"No puedes asignar más de {max_amount} '{resource_selected}' en total. "
                              f"Ya tienes {current_assigned} asignados.")
                        continue
                    new_event.resources[resource_selected] = current_assigned + amount
                    alert(f"Has agregado {amount} '{resource_selected}'")
                    break
                else:
                    alert(f"Debe ingresar un valor entre 0 y {current_availability}")
            except ValueError:
                alert(f"Debe ingresar un valor entre 0 y {current_availability}")

        print("Recursos seleccionados:") 
        print(new_event.resources)

    while True:
        os.system("cls")
        desired_start = ask_date("Escriba la fecha de inicio del evento (dd/mm/aaaa hh:mm): ")
        desired_end = ask_date("Escriba la fecha de culminación del evento (dd/mm/aaaa hh:mm): ")
    
        if desired_end <= desired_start:
            alert("La fecha de finalización debe ser después de la inicialización.")
            continue
        if desired_start < datetime.now(): 
            alert("No se pueden programar eventos en el pasado.")
            continue
        break

    new_event.start, new_event.end = find_available_start(new_event, desired_start, desired_end, event_actives, resources)
    event_actives.append(new_event)
    alert("Evento creado exitosamente.")
    print("\nResumen del evento creado:") 
    print(f"Nombre: {new_event.name}") 
    print(f"Inicio: {new_event.start}") 
    print(f"Fin: {new_event.end}") 
    print(f"Recursos: {new_event.resources}")
    input("Presiona Enter para continuar...")
    os.system("cls")


def remove_event():
    if not event_actives:
        print("No hay eventos activos que eliminar")
        input("Presiona la tecla Enter para continuar...")
        os.system("cls")
        return
    
    print("ELIJA QUE EVENTO ELIMINAR (0 para terminar)")
    cont = 1
    for event in event_actives:
        print(f"{cont}.{event.name}")
        cont += 1

    option = int(input("\nElige el número del evento: "))
    if option == 0:
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
