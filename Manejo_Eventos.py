import os
from datetime import datetime
from Recursos import resources, check_exclusion, check_inclusion
from Evento import Event, event_names, ask_date, find_available_start, available_amount

event_actives = []

def add_event():
    new_event = Event()

    print("SELECCIONE UN EVENTO")
    print("1.Instalación eléctrica en local\n"+
          "2.Mudanza con camión de carga\n"+
          "3.Construcción o reparación de inmueble\n"+
          "4.Mantenimiento de sistemas informáticos o de red\n"+
          "5.Montaje de domótica\n")
    
    try: 
        choice = int(input("Ingrese el número del evento: ")) 
        if choice < 1 or choice > len(event_names): 
            print("Opción inválida.") 
            return 
    except ValueError: 
        print("Debe ingresar un número válido.") 
        return
    
    new_event.name = event_names[choice-1]
    os.system("cls")

    while True:
        desired_start = ask_date("Escriba la fecha de inicio del evento (dd/mm/aaaa hh:mm): ")
        desired_end = ask_date("Escriba la fecha de culminación del evento (dd/mm/aaaa hh:mm): ")
    
        if desired_end <= desired_start:
            print("La fecha de finalización debe ser después de la inicialización.")
            input("Presiona la tecla Enter para continuar...")
            os.system("cls")
            continue

        if desired_start < datetime.now(): 
            print("No se pueden programar eventos en el pasado.")
            input("Presiona la tecla Enter para continuar...")
            os.system("cls")
            continue

        break

    print(f"El evento '{new_event.name}' ha sido programado desde {desired_start.strftime('%d/%m/%Y %H:%M')} hasta {desired_end.strftime('%d/%m/%Y %H:%M')}")
    input("Presiona la tecla Enter para continuar...")
    os.system("cls")

    check_inclusion(new_event.name, new_event.resources)
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
                if current_availability == 0:
                    print(f"{cont}.{key} : [NO DISPONIBLE]")
                else:
                    print(f"{cont}.{key} : {current_availability}")
            cont += 1

        try: 
            option = int(input("\nElige el número del recurso: ")) 
        except ValueError: 
            print("Debe ingresar un número válido.") 
            continue

        if option == 0:
            if not new_event.resources:
                print("Debe asignar al menos un recurso al evento.")
                continue
            new_event.start, new_event.end = find_available_start(new_event, desired_start, desired_end, event_actives, resources) 
            event_actives.append(new_event)

            print("\nResumen del evento creado:") 
            print(f"Nombre: {new_event.name}") 
            print(f"Inicio: {new_event.start}") 
            print(f"Fin: {new_event.end}") 
            print(f"Recursos: {new_event.resources}") 
            break
            
        if option < 1 or option > len(resources): 
            print("Opción inválida.") 
            input("Presiona Enter para continuar...")
            os.system("cls")
            continue

        resource_selected = list(resources.keys())[option - 1]

        if resources[resource_selected] == 0:
            print(f"El recurso '{resource_selected}' no está disponible.")
            input("Presiona la tecla Enter para continuar...")
            os.system("cls")
            continue
        
        if resource_selected in excluded:
            print(f"El recurso '{resource_selected}' ha sido excluído debido a la naturaleza del evento.")
            input("Presiona la tecla Enter para continuar...")
            os.system("cls")
            continue

        current_availability = available_amount(resource_selected, new_event.resources, event_actives, resources) 

        while True:
            try:
                amount = int(input(f"Ingrese un valor entre 0 y {current_availability} para {resource_selected}: "))
                if 0 <= amount <= current_availability: 
                    break
                else:
                    print(f"Debe ingresar un valor entre 0 y {current_availability}")
                    input("Presiona Enter para continuar...")
                    os.system("cls")
            except ValueError:
                print(f"Debe ingresar un valor entre 0 y {current_availability}")
                input("Presiona Enter para continuar...")
                os.system("cls")
                continue
        
        if amount > 0:
            new_event.resources[resource_selected] = new_event.resources.get(resource_selected, 0) + amount
            print(f"\nHas agregado {amount} '{resource_selected}'")
            input("Presiona la tecla Enter para continuar...")
            os.system("cls")
        else:
            print(f"\nNo se agregó '{resource_selected}' (acción cancelada).")
            input("Presiona la tecla Enter para continuar...")
            os.system("cls")

        os.system("cls") 
        print("Recursos seleccionados:") 
        print(new_event.resources)

def remove_event():
    if not event_actives:
        print("No hay eventos activos que eliminar")
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
