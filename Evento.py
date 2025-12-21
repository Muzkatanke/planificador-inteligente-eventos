from datetime import datetime
from Recursos import * 
import os

class Event:
    def __init__(self, name=None, resources=None, start=None, end=None):
        self.name = name
        self.resources = resources
        self.start = start
        self.end = end
 
event_names = ["Instalación eléctrica en local", "Mudanza con camión de carga", 
                "Construcción o reparación de inmueble",
                "Mantenimiento de sistemas informáticos o de red", "Montaje de domótica"]

event_actives = [] #json

def add_event():
    new_event = Event()
    new_event_resources = {}

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
        print("ELIJA LOS RECURSOS DEL EVENTO (0 para terminar)")
        print("(Recurso : cantidad)")   

        cont = 1
        for key, value in resources.items():
            if value == 0:
                print(f"{cont}.{key} : [NO DISPONIBLE]")
                cont += 1
            else:
                print(f"{cont}.{key} : {value}")
                cont += 1

        option = int(input("\nElige el número del producto: "))
        if option == 0:
            break
        key_selected = list(resources.keys())[option - 1]

        if resources[key_selected] == 0:
            print(f"El recurso '{key_selected}' no está disponible.")
            input("Presiona Enter para continuar...")
            os.system("cls")
            continue
        
        amount = int(input(f"Ingrese la cantidad para {key_selected}: "))
    
        while amount < 0 or amount > resources[key_selected]:
            amount = int(input(f"Ingrese un valor entre 0 y {resources[key_selected]} para {key_selected}: "))
        
        resources[key_selected] -= amount
        new_event_resources[key_selected] = new_event_resources.get(key_selected, 0) + amount
        
        os.system("cls")
        print(f"\nHas agregado {amount} '{key_selected}'")
        input("Presiona la tecla Enter para continuar...")
        os.system("cls")
        print(new_event_resources)
    
    


def remove_event():
    print("Función en construcción")
    input("Presiona la tecla Enter para continuar...")
    os.system("cls")

def view_events():
    print("Función en construcción")
    input("Presiona la tecla Enter para continuar...")
    os.system("cls")