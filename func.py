import os
import sqlite3
from classes import *
import time

ventaDiaria = 0
fiadoDiario = 0
fiado = {}
total = 0

def exitt(a):
    fecha = [time.localtime()[2], time.localtime()[1], time.localtime()[0]]
    a = False
    return a

def articleSave(name,price,code):
    conexion = sqlite3.connect("shop.db")
    cursor = conexion.cursor()

    try:
        entities = (name, price, code )
        cursor.execute("INSERT INTO articulos(article, price,code) VALUES(?, ?,?)", entities)
        conexion.commit()
        
    except sqlite3.IntegrityError:
        #return wx.MessageDialog(self,message='Article already exist!',caption='Article error!').ShowModal()
        return print('Article already exist!')
    else:
        #return wx.MessageDialog(self,message='You article has been created!',caption='Created User').ShowModal()
        return print('You article has been created!')
    conexion.commit()
    conexion.close()


def userSave(namey,dni):
    conexion = sqlite3.connect("shop.db")
    cursor = conexion.cursor()

    try:
        entities = (None, namey, dni, 0)
        cursor.execute("INSERT INTO clientes(id, nameu, dni, cuenta) VALUES(?, ?, ?, ?)", entities)
        conexion.commit()
        
    except sqlite3.IntegrityError:
        #return wx.MessageDialog(self,message='Article already exist!',caption='Article error!').ShowModal()
        return print('El cliente ya existe!')
    else:
        #return wx.MessageDialog(self,message='You article has been created!',caption='Created User').ShowModal()
        return print('El cliente ha sido creado!')
    conexion.commit()
    conexion.close()


def crear_bd():
    conexion = sqlite3.connect("shop.db")
    cursor = conexion.cursor()
    try:
        cursor.execute('''
            CREATE TABLE fecha(
            fecha INTEGER UNIQUE NOT NULL,
            monto INTEGER)''')

        cursor.execute('''
            CREATE TABLE articulos(
            article VARCHAR(100) UNIQUE NOT NULL,
            price VARCHAR(100) NOT NULL,
            code VARCHAR(100) NOT NULL)''')

        cursor.execute('''
            CREATE TABLE clientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nameu VARCHAR(100),
            dni VARCHAR(100) UNIQUE NOT NULL,
            cuenta INTEGER )''')
        conexion.close()
    except sqlite3.OperationalError:
        print("Ya existe la tabla")
    else:
        print("Las tablas se han creado con exito.")



def caja():
    global ventaDiaria
    global fiadoDiario
    global total
    suma = add_art()
    os.system('cls')

def add_art():
    global fiadoDiario
    global ventaDiaria
    global total
    active = True
    while active:
        os.system('cls')
        articulo = input( "\nEscanee un codigo / x para salir: " )
        if articulo == "x" or articulo == "X":
            active = False
        else:
            try:

                articulo = int(articulo)
                try:
                    num = art[int(articulo)].precio
                    total += num
                except:
                    print("Articulo inexistente!")

            except ValueError:
                print("Codigo erroneo..")
    
    doss = True
    while doss:
        multi = input("""
        1) Efectivo
        2) Fiado
        3) Descontar del total
        4) Añadir mas articulos

        5) Anular venta

        ->""")


        if multi == "1":
            print(f"\nTotal de la cuenta es: ${total}")

            paga = input("\n¿Cuanto paga?\n--> $")

            print(f"\nEl vuelto es: ${int(paga) - total}")

            finalizado = input("""\nEl llevo los articulos?

            1) Si
            2) No

            -->""")

            os.system('cls')

            if finalizado == "1":
                ventaDiaria += total
                break
            else:
                print("Venta Anulada!")
                input("Presiones una tecla para continuar...")
                os.system('cls')
                break
        elif multi == "2":
            cliente = int(input("\nIngrese numero de cliente: "))
            clientes[cliente].agregar(total)
            os.system('cls')
            print(f"\nSe ha fiado\n\nCliente: {clientes[cliente].name}\n\n DNI: {clientes[cliente].dni} \n\nTotal: ${total}")
            fiadoDiario += total
            input("\nPulse una tecla para finalizar... ")
            break
        elif multi == "3":
            restar = input("Cuanto desea descontar?\n\n-> $")
            total -= int(restar)
        elif multi == "4":
            add_art(total)
        elif multi == "5":
            print("Venta anulada!\n")
            break

def cargar_articulos():
    activo = True
    os.system('cls')
    while activo:
        op = "x"
        op2 = "X"

        os.system('cls')
        print("Presione X para salir...")
        name = input("\nIngrese el nombre del articulo: ")
        if name == op or name == op2:
            break

        codigo = input("\nIngrese el codigo de barras: ")
        if codigo == op or codigo == op2:
            break

        precio = input(f"\nIngrese el precio del articulo {name}:\n$")
        if precio == op or precio == op2:
            break
        try:
            codigo = int(codigo)
            precio = int(precio)
            try:
                articleSave(name,precio,codigo)

                opcion = input("¿Añadir otro articulo?\n\n1) Si\n2) No\n\n-->")
                if opcion == "1":
                    cargar_articulos()
                elif opcion == "2":
                    activo = False
                else:
                    print("\nOpcion Incorrecta!\nSaliendo de forma automatica.\n")
                    break
            except:
                print("Error en los datos de cargado!")

        except ValueError:
            print("Codigo de articulo o precio incorrectos..")

    os.system('cls')





def view_article(code):

    conexion = sqlite3.connect("shop.db")
    cursor = conexion.cursor()
    a = cursor.execute("select * from articulos where code=:code", {"code": code})
    b = cursor.fetchone()
    if b:
        print(f"""
                    Nombre: {b[0]}
                    Precio: ${b[1]}
                    Codigo: {b[2]}
                    """)
        #return wx.MessageDialog(self,message='You has been Login!',caption='Loged User').ShowModal()
    else:
        print("El articulo no existe!\nPresione una tecla para continuar, X para salir")  
        a = input()
        if a.lower() == "x":
            return "x"
        #return wx.MessageDialog(self,message='Invalid Account!',caption='Login Error').ShowModal()

    conexion.close()


def consultar_articulos():
    active = True
    while active:
        print("Presione X para salir...")
        articulo = input("\nIngrese el codigo de barras: ")
        if articulo == "x":
            active = False
        elif articulo == "X":
            active == False
        else:
            try:
                code = int(articulo)
                try:
                    os.system('cls')
                    a = view_article(code)
                    a
                    if a.lower() == "x":
                        break
                except:
                    pass
            except ValueError:
                print("Codigo erroneo!")

def add_client():
    active = True
    while active:
        os.system('cls')
        print("Para cancelar presione X\n")
        name = input("\nIngrese el nombre del cliente: ")
        dni = input(f"\nIngrese el DNI de {name}: ")
        try:
            dni = int(dni)
            try:
                userSave(name,dni)
                input("Presiones una tecla para continuar...")
                os.system('cls')
            except:
                print("Error al crear el cliente codigo de error: 0x01")
                #este error no puede pasar nunca xD
        except:
            print("Error dni incorrecto.")
            os.system('cls')
            pass
        break
    os.system('cls')


def consulta_cliente(dni):
    
    conexion = sqlite3.connect("shop.db")
    cursor = conexion.cursor()
    a = cursor.execute("select * from clientes where dni=:dni", {"dni": dni})
    b = cursor.fetchone()
    if b:
        print(f"""
                    Nombre: {b[1]}
                    DNI: {b[2]}
                    Cuenta: ${b[3]}
                    """)
        input("\nPresione una tecla para continuar...")
        #return wx.MessageDialog(self,message='You has been Login!',caption='Loged User').ShowModal()
    else:
        pass
        #return wx.MessageDialog(self,message='Invalid Account!',caption='Login Error').ShowModal()

    conexion.close()


def view_client():
    active = True

    while active:
        print("Para cancelar presione X\n")
        dni = input("\nIngrese el numero de dni: ")

        if dni.lower() == "x":
            active = False
        else:
            try:
                dni = int(dni)
                try:
                    consulta_cliente(dni)
                    break
                except:
                    print("\nCliente inexistente!\nPresiones una tecla para continuar...")
                    input()
                    os.system('cls')
            except:
                print("Numero de DNI incorrecto!\nPresiones una tecla para continuar... ")
                input()
                os.system('cls')

    
    

    
def cliente_more():
    active = True
    while active:
        os.system('cls')
        print("Presione X para volver al menu principal")

        cliente = input("Ingrese el DNI del cliente: ")
        if cliente.lower() == "x":
            active = False
        
        sumar = input("\nCuanto desea sumar a la cuenta del cliente?:\n\n$")
        if sumar.lower() == "x":
            active == False

        try:
            dni = int(cliente)
            suma = int(sumar)
            
            try:
                print(f"Se le sumaran ${suma} a la cuenta.")
                opcion = input("¿Confirmar?\n\n1) Si\n2) No\n\n->")
                
                if opcion == "1":
                    conexion = sqlite3.connect("shop.db")
                    cursor = conexion.cursor()
                    a = cursor.execute("select * from clientes where dni=:dni", {"dni": dni})
                    b = cursor.fetchone()
                    cuenta = int(b[3]) + suma
                    cursor.execute(f"UPDATE clientes SET cuenta = ${cuenta} WHERE dni = {dni}")
                    #cursor.execute("UPDATE clientes SET cuenta=cuenta WHERE dni=dni", {"cuenta": cuenta, "dni": dni})

                    conexion.commit()
                    conexion.close()
                    consulta_cliente(dni)
                    break
                elif opcion =="2":
                    os.system('cls')
                    print("Adicion anulada...")
                    input("Presiones una tecla para continuar...")
                    os.system('cls')
                else:
                    print("Opcion incorrecta!")
            except:
                print('ots')
        except:
            print("error: Numero de cliente o monto incorrecto!")


def client_pay():
    os.system('cls')
    active = True
    while active:
        print("Presione X para volver al menu principal")

        cliente = input("Ingrese el DNI del cliente: ")
        if cliente.lower() == "x":
            active = False
        
        restar = input("\nCuanto desea abonar el cliente?:\n\n$")
        if restar.lower() == "x":
            active == False
        try:
            dni = int(cliente)
            resta = int(restar)
            
            try:
                print(f"Se le restaran ${resta} a la cuenta.")
                opcion = input("¿Confirmar?\n\n1) Si\n2) No\n\n->")
                
                if opcion == "1":
                    conexion = sqlite3.connect("shop.db")
                    cursor = conexion.cursor()
                    a = cursor.execute("select * from clientes where dni=:dni", {"dni": dni})
                    b = cursor.fetchone()
                    cuenta = int(b[3]) - resta
                    cursor.execute(f"UPDATE clientes SET cuenta = ${cuenta} WHERE dni = {dni}")

                    conexion.commit()
                    conexion.close()
                    consulta_cliente(dni)
                    break
                elif opcion =="2":
                    print("Pago anulado...")
                    input("Presiones una tecla para continuar...")
                    os.system('cls')
                else:
                    print("Opcion incorrecta!")
            except:
                print('Error, contacte al desarrollador.')
        except:
            print("error: Numero de cliente o monto incorrecto!")