import os
from datetime import datetime
from logic.Persistencia import save_events, load_events
from logic.Datos import resources
from logic.Recursos import check_resources_inclusion, check_resources_exclusion
from logic.Evento import Event, event_names, ask_date, find_available_start, available_amount

event_actives = load_events()

def alert(message):
    os.system("cls")
    print(message)
    input("Presiona Enter para continuar...")
    os.system("cls")

def add_event():
    new_event = Event()
    auto_reprogram = False

    while True:
        print("SELECCIONE UN EVENTO (0 para terminar)")
        print("1.Instalación eléctrica en local\n"+
            "2.Mudanza con camión de carga\n"+
            "3.Construcción o reparación de inmueble\n"+
            "4.Mantenimiento de sistemas informáticos o de red\n"+
            "5.Montaje de domótica\n"+
            "6.Mantenimiento de fontanería")
        
        try: 
            choice = int(input("\nIngrese el número del evento: "))  
            if 1 <= choice <= 6:
                break
            if choice == 0:
                return
            else:
                alert("Debe ingresar un número válido.")
                continue
        except ValueError: 
            alert("Debe ingresar un número válido.") 
            continue
    
    new_event.name = event_names[choice-1]
    os.system("cls")

    while True:
        print("ELIJA LOS RECURSOS DEL EVENTO (0 para terminar)")
        print("(Recurso : cantidad)")   

        cont = 1
        excluded_set = check_resources_exclusion(new_event.resources)

        for key in resources.keys():
            if key in excluded_set:
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

        if resource_selected in excluded_set: 
            alert(f"El recurso '{resource_selected}' está excluido debido a la selección actual.")
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
                    
                    valid_inclusion = check_resources_inclusion(new_event.resources, event_actives, alert, available_amount)
                    if not valid_inclusion:
                        auto_reprogram = True
                    break
                else:
                    alert(f"Debe ingresar un valor entre 0 y {current_availability}")
            except ValueError:
                alert(f"Debe ingresar un valor entre 0 y {current_availability}")

    if not check_resources_inclusion(new_event.resources, event_actives, alert, available_amount):
        alert(f"Los recursos obligatorios para '{new_event.name}' no están disponibles actualmente.\n"
              "El evento se reprogramará automáticamente hasta que estén libres.")
        auto_reprogram = True
    else:
        auto_reprogram = False

    excluded_set = check_resources_exclusion(new_event.resources)
    
    alert(f"Recursos seleccionados para el evento:\n {new_event.resources}")

    if auto_reprogram:
        new_start, _ = find_available_start(new_event, datetime.now(), datetime.now(), event_actives, resources)

        alert(f"La siguiente fecha válida de inicio para '{new_event.name}' es {new_start}.")
        confirm = input("¿Estás de acuerdo con esta fecha de inicio? (s/n): ")

        if confirm.lower() != "s":
            alert("Evento cancelado, recursos liberados.")
            return

        while True:
            desired_end = ask_date("Escriba la fecha de culminación del evento (dd/mm/aaaa hh:mm): ")

            if desired_end <= new_start:
                alert("La fecha de finalización debe ser después de la inicialización.")
                continue

            adjusted_end = desired_end
            for ev in event_actives:
                if not ev.activated:
                    continue
                if new_start < ev.end and ev.start < desired_end:
                    for key, amount in new_event.resources.items():
                        ev_amount = ev.resources.get(key, 0)
                        if ev_amount > 0 and amount + ev_amount > resources[key]:
                            adjusted_end = ev.start
                            alert(f"El evento se solapaba con [ID {ev.id}] {ev.name}. "
                                f"Se ha ajustado la fecha de finalización a {adjusted_end}.")
                            break

            if adjusted_end <= new_start:
                alert("No hay espacio disponible para programar el evento sin solapamiento.")
                return

            new_event.start, new_event.end = new_start, adjusted_end
            break
    else:
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

        new_start, new_end = find_available_start(new_event, desired_start, desired_end, event_actives, resources)

        if (new_start, new_end) != (desired_start, desired_end):
            alert(f"El evento '{new_event.name}' se solapa con otros.\n"
                  f"Se ha reprogramado automáticamente desde {new_start} hasta {new_end}.")
            confirm = input("¿Aceptar esta fecha sugerida? (s/n): ")
            if confirm.lower() != "s":
                alert("Evento cancelado, recursos liberados.")
                return
            new_event.start, new_event.end = new_start, new_end
        else:
            new_event.start, new_event.end = desired_start, desired_end

    event_actives.append(new_event)
    save_events(event_actives)
    alert("Evento creado exitosamente.")

    print("Resumen del evento creado:") 
    print(f"ID: {new_event.id}")
    print(f"Nombre: {new_event.name}") 
    print(f"Inicio: {new_event.start}") 
    print(f"Fin: {new_event.end}") 
    print(f"Recursos: {new_event.resources}")
    input("Presiona Enter para continuar...")
    os.system("cls")

def remove_event():
    if not event_actives:
        alert("No hay eventos activos que eliminar")
        return
    
    print("ELIJA QUE EVENTO ELIMINAR (0 para terminar)")
    cont = 1
    for event in event_actives:
        print(f"{cont}. [ID {event.id}] {event.name}")
        cont += 1

    try:
        option = int(input("\nElige el número del evento: "))
    except ValueError:
        alert("Entrada inválida.")
        return

    if option == 0 or option > len(event_actives):
        return

    event = event_actives.pop(option - 1)
    save_events(event_actives)
    alert(f"Evento [ID {event.id}] eliminado.")
    
def view_events():
    if not event_actives:
        alert("No hay eventos activos que ver")
        return
    
    os.system("cls")
    for event in event_actives:
        print(f"[ID {event.id}] {event.name}: Programado desde {event.start} hasta {event.end}.")
        print(f"Recursos: {event.resources}\n")

    input("Presiona Enter para continuar...")
    os.system("cls")
