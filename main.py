from func import *
import os




a = True
crear_bd()
while a:
    os.system('cls')
    menu = input("""
    Bienvenido, ingrese una opcion!

    1) Modo Caja
    2) Ingresar Articulos
    3) Consultar Articulos
    4) Ingresar Cliente
    5) Consultar Clientes
    6) Pagar Cuenta Cliente
    7) Añadir deuda extra cliente
    
    9) Salir

    --> """)

    if menu == "1":
        caja()
    elif menu == "2":
        cargar_articulos()
    elif menu == "3":
        consultar_articulos()
    elif menu == "4":
        add_client()
    elif menu == "5":
        view_client()
    elif menu == "6":
        client_pay()
    elif menu == "7":
        cliente_more()
    elif menu == '8':
        pass
        
        
    elif menu == "9":
        a = exitt(a)
    else:
        os.system('cls')
        print("Opcion incorrecta!")