from func import *
import os

if __name__ == '__main__':

    a = True
    crear_bd()
    print("Presione una tecla para iniciar...")
    input()
    cargar_datos()
    cargar_clientes()
    while a:
        menu = input("""

            _  __                             ___   _                 
            | |/ /  ___   _ _    _ _    _  _  / __| | |_    ___   _ __ 
            | ' <  / -_) | ' \  | ' \  | || | \__ \ | ' \  / _ \ | '_ \ 
            |_|\_\ \___| |_||_| |_||_|  \_, | |___/ |_||_| \___/ | .__/
                                        |__/                     |_|    
                                                                                                
    #######################################################################
    #                                                                     #
    #                   Bienvenido, ingrese una opcion!                   #
    #                                                                     #
    #                   1) Modo Caja                                      #
    #                   2) Ingresar Articulos                             #
    #                   3) Consultar Articulos                            #
    #                   4) Ingresar Cliente                               #
    #                   5) Consultar Clientes                             #
    #                   6) Pagar Cuenta Cliente                           #
    #                   7) Añadir deuda extra cliente                     #
    #                   8) Cambiar Precio a Articulo                      #
    #                   9) Ver informe...                                 #
    #                                                                     #
    #                   0) Salir                                          #
    #                                                                     #
    #######################################################################

                        --> """)

        if menu == "1":
            caja()
            os.system('cls')
        elif menu == "2":
            cargar_articulos()
            os.system('cls')
        elif menu == "3":
            consultar_articulos()
            os.system('cls')
        elif menu == "4":
            add_client()
            cargar_clientes()
            os.system('cls')
        elif menu == "5":
            active = True
            while active:
                print("Para cancelar presione X\n")
                dni = input("\nIngrese el numero de dni: ")
                if dni.lower() == "x":
                    active = False
                else:
                    consulta_cliente(dni)
                    break
            os.system('cls')
            
        elif menu == "6":
            client_pay()
            os.system('cls')
        elif menu == "7":
            cliente_sumar()
            os.system('cls')
        elif menu == '9':
            consultar_ventas()
        elif menu == "8":
            code = input("Ingrese el codigo del articulo:\n--> ")
            price = input("Ingrese el nuevo precio:\n-->")
            cambiar_precio(code,price)
        elif menu == "0":
            a = False
        else:
            os.system('cls')
            print("Opcion incorrecta!")



        