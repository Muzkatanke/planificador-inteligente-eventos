import os
from datetime import datetime
from logic.Persistencia import save_events, load_events
from logic.Datos import resources
from logic.Recursos import check_resources_inclusion, check_resources_exclusion
from logic.Evento import Event, event_names, ask_date, find_available_start, available_amount, available_amount_interval

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
            alert("Debe ingresar un número válido.")
        except ValueError:
            alert("Debe ingresar un número válido.")

    new_event.name = event_names[choice-1]
    os.system("cls")

    while True:
        desired_start = ask_date("Escriba la fecha de inicio del evento (dd/mm/aaaa hh:mm): ")
        desired_end = ask_date("Escriba la fecha de culminación del evento (dd/mm/aaaa hh:mm): ")

        if desired_end <= desired_start:
            alert("La fecha de finalización debe ser después de la inicialización.")
            continue
        if desired_start < datetime.now():
            alert("No se pueden programar eventos en el pasado.")
            continue
        break
    
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
                current_availability = available_amount_interval(
                    key, new_event.resources, event_actives, resources, desired_start, desired_end
                )
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
                alert("Creación de evento cancelada. No se seleccionaron recursos.")
                return
            break

        if option < 1 or option > len(resources):
            alert("Opción inválida.")
            continue

        resource_selected = list(resources.keys())[option - 1]

        if resource_selected in excluded_set:
            alert(f"El recurso '{resource_selected}' está excluido debido a la selección actual.")
            continue

        max_amount = resources[resource_selected]
        current_assigned = new_event.resources.get(resource_selected, 0)

        if current_assigned >= max_amount:
            alert(f"Ya tienes asignados {current_assigned} '{resource_selected}', "
                  f"que es el máximo permitido. No puedes añadir más.")
            continue

        current_availability = available_amount_interval(resource_selected, new_event.resources, event_actives, resources, desired_start, desired_end)

        if current_availability <= 0:
            alert(f"El recurso '{resource_selected}' no está disponible en el intervalo seleccionado.\n"
                  "Si lo selecciona, el evento deberá reprogramarse automáticamente.")
            confirm = input("¿Desea continuar y reprogramar el evento? (s/n): ")
            if confirm.lower() != "s":
                continue

            auto_reprogram = True
            max_remaining = max_amount - current_assigned

            while True:
                try:
                    amount = int(input(f"Ingrese un valor entre 1 y {max_remaining} para {resource_selected}: "))
                    if 1 <= amount <= max_remaining:
                        new_event.resources[resource_selected] = current_assigned + amount
                        alert(f"Has agregado {amount} '{resource_selected}'.")

                        valid_inclusion = check_resources_inclusion(new_event.resources, event_actives, alert, available_amount_interval, desired_start, desired_end)
                        if not valid_inclusion:
                            auto_reprogram = True
                        break
                    
                    alert(f"Debe ingresar un valor entre 1 y {max_remaining}")
                except ValueError:
                    alert(f"Debe ingresar un valor entre 1 y {max_remaining}")
            continue

        while True:
            try:
                amount = int(input(f"Ingrese un valor entre 1 y {current_availability} para {resource_selected}: "))
                if 1 <= amount <= current_availability:
                    new_event.resources[resource_selected] = current_assigned + amount

                    valid_inclusion = check_resources_inclusion(new_event.resources, event_actives, alert, available_amount_interval, desired_start, desired_end)
                    if not valid_inclusion:
                        auto_reprogram = True
                    break
                alert(f"Debe ingresar un valor entre 1 y {current_availability}")
            except ValueError:
                alert(f"Debe ingresar un valor entre 1 y {current_availability}")

    alert(f"Recursos seleccionados:\n{new_event.resources}")

    if auto_reprogram:
        try:
            new_start, new_end = find_available_start(
                new_event, desired_start, desired_end, event_actives, resources
            )
        except ValueError as e:
            alert(str(e))
            alert("Evento cancelado.")
            return

        alert(f"El evento debe reprogramarse.\nNueva fecha sugerida: {new_start} → {new_end}")
        confirm = input("¿Aceptar esta fecha? (s/n): ")
        if confirm.lower() != "s":
            alert("Evento cancelado.")
            return

        new_event.start = new_start
        new_event.end = new_end

    else:
        new_event.start = desired_start
        new_event.end = desired_end

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
