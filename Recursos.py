import os

resources = {
    "Electricista" : 3,
    "Plomero" : 2,
    "Carpintero" : 2,
    "Obrero" : 5,
    "Técnico de redes": 3,
    "Técnico de domótica": 3,
    "Camión de carga" : 2,
    "Sensores y dispositivos de domótica" : 5,
    "Materiales de construcción" : 5,
    "Kit de herramientas" : 5,
    "Equipos de red" : 5,
    "Accesorios de fontanería" : 5,
    "Accesorios de electricidad" : 5
}

event_inclusion = {"Instalacion eléctrica en local" : ["Electricista", "Accesorios de electricidad"],
                   "Mudanza con camión de carga": ["Obrero", "Camión de carga"],
                   "Construcción o reparación de inmueble": ["Obrero", "Materiales de construcción"],
                   "Mantenimiento de sistemas informáticos o de red": ["Técnico de redes", "Equipos de red"],
                   "Montaje de domótica": ["Técnico de domótica", "Sensores y dispositivos de domótica"],
                   "Mantenimiento de fontanería": ["Plomero", "Accesorios de fontanería"]}

event_exclusion = {"Instalacion eléctrica en local" : ["Plomero", "Accesorios de fontanería"],
                   "Mudanza con camión de carga": ["Electricista", "Técnico de redes"],
                   "Construcción o reparación de inmueble": ["Técnico de redes", "Técnico de domótica"],
                   "Mantenimiento de sistemas informáticos o de red": ["Plomero", "Materiales de construcción"],
                   "Montaje de domótica": ["Obrero", "Cammión de carga"],
                   "Mantenimiento de fontanería": ["Electricista", "Equipos de red"]}

def check_inclusion(event_name, event_resources):
    if event_name in event_inclusion:
        for resource in event_inclusion[event_name]:
            event_resources[resource] = event_resources.get(resource, 0) + 1
            print(f"El recurso '{resource}' ha sido incluido automáticamente en el evento '{event_name}'.")
    input("Presiona la tecla Enter para continuar...")
    os.system("cls")

def check_exclusion(event_name):
    if event_name in event_exclusion:
        return event_exclusion[event_name]
    return []

