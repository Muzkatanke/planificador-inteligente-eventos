from Evento import * 
import os

flag = True

while flag == True:
    activate_events()
    
    print("BIENVENIDO AL GESTOR DE EVENTOS")
    print("1.Agregar evento\n"+
          "2.Eliminar evento\n"+
          "3.Ver eventos\n"+
          "4.Salir\n")
    choice = int(input())
    
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
   

    