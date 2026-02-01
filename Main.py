import os
from logic.Planificador import activate_events, desactivate_events
from logic.Manejo_Eventos import event_actives, add_event, remove_event, view_events

def show_menu():
    os.system("cls")
    print("=== BIENVENIDO AL GESTOR DE EVENTOS DE ACUSE.S.A. ===")
    print("1.Agregar evento")
    print("2.Eliminar evento")  
    print("3.Ver eventos")      
    print("4.Salir")      
    
def main():
    while True:
        activate_events(event_actives)
        desactivate_events(event_actives)
        show_menu()
        
        try: 
            choice = int(input("Seleccione una opción: ")) 
        except ValueError: 
            print("Introduce un número válido!!") 
            continue

        if choice == 1:
            os.system("cls")
            add_event()
        elif choice == 2:
            os.system("cls")
            remove_event()
        elif choice == 3:
            os.system("cls")
            view_events()
        elif choice == 4:
            print("👋 Saliendo del gestor de eventos...") 
            break
        else:
            print("Introduce un número válido!!")

if __name__ == "__main__":
    main()