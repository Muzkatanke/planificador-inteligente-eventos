import os
from Planificador import activate_events
from Manejo_Eventos import event_actives, add_event, remove_event, view_events

flag = True
while flag:
    activate_events(event_actives)
    
    print("BIENVENIDO AL GESTOR DE EVENTOS")
    print("1.Agregar evento\n"+
          "2.Eliminar evento\n"+
          "3.Ver eventos\n"+
          "4.Salir\n")
    
    try: 
        choice = int(input("Seleccione una opción: ")) 
    except ValueError: 
        print("Introduce un número válido") 
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
        flag = False
    else:
        print("Introduce un dato válido")
