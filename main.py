from func import *

crear_bd()


a = True
while a:
    clear_
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
        
        
    elif menu == "9":
        a = False
    else:
        clear_
        print("Opcion incorrecta!")