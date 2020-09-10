import os
import sqlite3
from classes import *
import time
import pandas

presione_tecla_para_continuar = lambda x=None : [ print(input("\nPresione una tecla para continuar...\n")) ]


ventaDiaria = 0
fiadoDiario = 0
total = 0
articulos = {}
clientes = {}

#Estamos tratando de meter segundos en base de datos y desp comparar para ver la fecha con pandas


def crear_bd():
    conexion = sqlite3.connect("shop.db")
    cursor = conexion.cursor()
    try:
        cursor.execute('''
            CREATE TABLE fecha(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha INTEGER UNIQUE NOT NULL,
            monto INTEGER)''')

        cursor.execute('''
            CREATE TABLE articulos(
            article VARCHAR(100) NOT NULL,
            price VARCHAR(100) NOT NULL,
            code VARCHAR(100) NOT NULL UNIQUE)''')

        cursor.execute('''
            CREATE TABLE clientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nameu VARCHAR(100),
            dni VARCHAR(100) UNIQUE NOT NULL,
            cuenta INTEGER )''')
        conexion.close()
    except sqlite3.OperationalError:
        pass
    else:
        pass

def cargar_datos():
    global articulos
    articulos = {}
    conexion = sqlite3.connect("shop.db")
    cursor = conexion.cursor()
    cursor.execute("select * from articulos ")
    mercaderia = cursor.fetchall()

    for articulo in mercaderia:
        name = articulo[0]
        price = articulo[1]
        code = articulo[2]
        articulos[code] = Articulo( name, price, code  )
    
    conexion.close()

def cargar_clientes():
    global clientes
    clientes = {}

    conexion = sqlite3.connect("shop.db")
    cursor = conexion.cursor()
    cursor.execute("select * from clientes")
    users = cursor.fetchall()

    for usuario in users:
        idx = usuario[0]
        name = usuario[1]
        dni = usuario[2]
        cuenta = usuario[3]
        clientes[dni] = Persona(idx, name, dni, cuenta)
    

    conexion.close()

def caja():

    ticket = []
    total = []
    while 1:
        global ventaDiaria
        global fiadoDiario
        os.system('cls')
        print("\nTicket Actual...")
        print("______________________________________________________")
        if len(ticket) > 0:
            for articulo in ticket:
                print("\n%0s \t\t\t\t$%-10s \n%0sx$%1s\n" % (articulo.name,(int(articulo.precio)*int(articulo.cantidad)),articulo.cantidad,articulo.precio ))

            print("______________________________________________________")
            print(f"\nTotal _____________________________________ {sum(total)}")

        articulo_venta = input("\nEscanee un articulo... (X para finalizar)\n-->")
        if articulo_venta.lower() == "x":
            while 1:

                opcion = input("""Elija una opcion:
                
                1) Efectivo
                2) Fiado

                3) Cancelar venta...

                """)

                if opcion == "1":
                    sumar_al_dia("efectivo",int(sum(total)))
                    mensaje("Operacion realizada con exito!")
                    break
                elif opcion == "2":
                    dni = input("Ingrese el dni del cliente a quien desee fiar:\n-->")
                    print("Realizando operacion...")
                    operacion_sumar_a_cliente(dni,sum(total))
                    mensaje("Se ha fiado satisfactoriamente!")
                    sumar_al_dia("fiado",int(sum(total)))
                    break
                elif opcion == "3":
                    break
                else:
                    print("Opcion incorrecta reintente...")
            break

        try:
            articulo_venta = str(int(articulo_venta))
            articulo_venta = articulos[articulo_venta]
            si = True
            for x in ticket:
                if x.code == articulo_venta.code:
                    indice = ticket.index(x)
                    ticket[indice].cantidad += 1
                    total.append(int(articulo_venta.precio))
                    si = False
            if si:
                articulo_venta.cantidad = 1
                ticket.append(articulo_venta)
                total.append(int(articulo_venta.precio))       
        except:
            agregar = input("El articulo no existe ¿Desea añadirlo al inventario?\n\n1) Si\n2) No\n\n--> ")
            
            if agregar == "1":
                code = int(articulo_venta)
                name = input("\nIngrese el nombre del articulo:\n\n--> ")
                precio = input("Ingrese el precio del articulo:\n\n--> ")
                articleSave(name,precio,code)
                cargar_datos()
                input("El articulo ha sido añadido con exito...\n")
                articulo_venta = articulos[str(int(articulo_venta))]
                articulo_venta.cantidad = 1
                total.append(int(articulo_venta.precio))
                ticket.append(articulo_venta)
            else:
                print("Articulo no añadido, continuando con la venta...")
                input()

def operacion_sumar_a_cliente(dni,suma):
        conexion = sqlite3.connect("shop.db")
        cursor = conexion.cursor()
        a = cursor.execute("select * from clientes where dni=:dni", {"dni": dni})
        b = cursor.fetchone()
        cuenta = int(b[3]) + suma
        cursor.execute(f"UPDATE clientes SET cuenta = {cuenta} WHERE dni = {dni}")
        #cursor.execute("UPDATE clientes SET cuenta=cuenta WHERE dni=dni", {"cuenta": cuenta, "dni": dni})

        conexion.commit()
        conexion.close()
        cargar_clientes()
        consulta_cliente(dni)

def operacion_restar_a_cliente(dni,resta):
        conexion = sqlite3.connect("shop.db")
        cursor = conexion.cursor()
        a = cursor.execute("select * from clientes where dni=:dni", {"dni": dni})
        b = cursor.fetchone()
        cuenta = int(b[3]) - resta
        cursor.execute(f"UPDATE clientes SET cuenta = {cuenta} WHERE dni = {dni}")
        #cursor.execute("UPDATE clientes SET cuenta=cuenta WHERE dni=dni", {"cuenta": cuenta, "dni": dni})

        conexion.commit()
        conexion.close()
        cargar_clientes()
        consulta_cliente(dni)

def cargar_articulos():
    global articulos
    os.system('cls')
    while 1:
        op = "x"
        op2 = "X"

        os.system('cls')
        print("Presione X para salir...")

        codigo = input("\nIngrese el codigo de barras: ")
        if codigo.lower() == 'x':
            break

        name = input("\nIngrese el nombre del articulo: ")
        if name.lower() == 'x':
            break

        precio = input(f"\nIngrese el precio del articulo {name}:\n$")
        if precio.lower() == 'x':
            break
        try:
            codigo = int(codigo)
            precio = int(precio)
            try:
                articleSave(name,precio,codigo)
                opcion = input("¿Añadir otro articulo?\n\n1) Si\n2) No\n\n-->")
                if opcion == "1":
                    cargar_datos()
                    cargar_articulos()
                    break
                elif opcion == "2":
                    cargar_datos()
                    break
                else:
                    print("\nOpcion Incorrecta!\nSaliendo de forma automatica.\n")
                    cargar_datos()
                    break
            except:
                print("Error en los datos de cargado!")

        except ValueError:
            print("Codigo de articulo o precio incorrectos..")
    os.system('cls')
    cargar_datos()

def articleSave(name,price,code):
    conexion = sqlite3.connect("shop.db")
    cursor = conexion.cursor()
    name = name.ljust(20," ")[:21]

    try:
        entities = (name, price, code )
        cursor.execute("INSERT INTO articulos(article, price,code) VALUES(?, ?,?)", entities)
        conexion.commit()
        
    except sqlite3.IntegrityError:
        #return wx.MessageDialog(self,message='Article already exist!',caption='Article error!').ShowModal()
        return mensaje('El articulo ya existe!')
    else:
        #return wx.MessageDialog(self,message='You article has been created!',caption='Created User').ShowModal()
        return print('El articulo ha sido añadido!')
    conexion.commit()
    conexion.close()



def consultar_articulos():
    global articulos
    active = True
    while active:
        print("Presione X para salir...")
        articulo = input("\nIngrese el codigo de barras: ")
        if articulo.lower() == "x":
            active = False
        else:
            try:
                code = int(articulo)
                os.system('cls')
                try:
                    b = articulos[str(code)]
                    if b:
                        print(f"""
Nombre: {b.name}
Precio: ${b.precio}
Codigo: {b.code}
                            """)
                        #return wx.MessageDialog(self,message='You has been Login!',caption='Loged User').ShowModal()
                except:
                    print("El articulo no existe!")
            except ValueError:
                print("Codigo erroneo!")

def add_client():
    global articulos
    os.system('cls')
    active = True
    while active:

        os.system('cls')
        print("Presione X para salir...")
        name = input("\nIngrese el nombre del cliente: ")
        if name.lower() == 'x':
            break

        dni = input(f"\nIngrese el DNI de {name}: ")
        if dni.lower() == 'x':
            break
        
        try:
            int(dni)
            dni = str(dni)
            try:
                userSave(name,dni)
            except:
                print("Error en los datos de cargado!")

        except ValueError:
            print("Dni incorrecto..")
            input()
            continue
        break
    os.system('cls')
    cargar_datos()

def userSave(namey,dni):
    conexion = sqlite3.connect("shop.db")
    cursor = conexion.cursor()

    try:
        entities = (None, namey, dni, 0)
        cursor.execute("INSERT INTO clientes(id, nameu, dni, cuenta) VALUES(?, ?, ?, ?)", entities)
        conexion.commit()
        
    except sqlite3.IntegrityError:
        #return wx.MessageDialog(self,message='Article already exist!',caption='Article error!').ShowModal()
        mensaje('El cliente ya existe!')
        input()
    else:
        #return wx.MessageDialog(self,message='You article has been created!',caption='Created User').ShowModal()
        mensaje('El cliente ha sido creado!')
        input()
    conexion.commit()
    conexion.close()

    cargar_clientes(clientes)

def consulta_cliente(dni):
    global clientes
    dni = dni
    try:
        dni = int(dni)
        os.system('cls')
        try:
            cliente_consultado = clientes[str(dni)]
            if cliente_consultado:
                print(f"""
Detalles del cliente:

Nombre: {cliente_consultado.name}
DNI: {cliente_consultado.dni}
Cuenta: ${cliente_consultado.cuenta}

                """)
            input()
        except:
            print("\nCliente inexistente!")
            presione_tecla_para_continuar()
            os.system('cls')
    except:
        print("Numero de DNI incorrecto!")
        presione_tecla_para_continuar()
        os.system('cls')

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
                consulta_cliente(str(dni))
                print(f"Se le restaran ${resta} a la cuenta.")
                opcion = input("¿Confirmar?\n\n1) Si\n2) No\n\n->")
                
                if opcion == "1":
                    operacion_restar_a_cliente(dni,resta)
                    break
                elif opcion =="2":
                    print("Pago anulado...")
                    presione_tecla_para_continuar()
                    os.system('cls')
                else:
                    print("Opcion incorrecta!")
            except:
                print('Error, contacte al desarrollador.')
        except:
            print("error: Numero de cliente o monto incorrecto!")

def cliente_sumar():
    active = True
    while active:
        os.system('cls')
        print("Presione X para volver al menu principal")

        dni = input("\nIngrese el DNI del cliente: ")
        if dni.lower() == "x":
            break
        
        sumar = input("\nCuanto desea sumar a la cuenta del cliente?:\n\n$")
        if sumar.lower() == "x":
            break
        
        print(f"Se le sumaran ${sumar} a la cuenta.")
        opcion = input("¿Confirmar?\n\n1) Si\n2) No\n\n->")
        try:
            int(dni)
            dni = str(dni)
            suma = int(sumar)
        except:
            print("Error en los datos...")
            break

        if opcion == "1":
            operacion_sumar_a_cliente(dni,suma)
            break
        
        elif opcion =="2":
            os.system('cls')
            print("Adicion anulada...")
            presione_tecla_para_continuar()
            os.system('cls')
            break
        else:
            print("Opcion incorrecta!")

def mensaje(msg):
    os.system(f'msg * "{msg}"')

def sumar_al_dia(opcion,total):
    global ventaDiaria
    global fiadoDiario

    if opcion == "efectivo":
        ventaDiaria += total
    elif opcion == "fiado":
        fiadoDiario += total

def consultar_ventas():
    global ventaDiaria
    global fiadoDiario

    print(f"Efectivo: {ventaDiaria}\nFiado: {fiadoDiario}")

def cambiar_precio(code,price):
    conexion = sqlite3.connect("shop.db")
    cursor = conexion.cursor()
    a = cursor.execute("select * from articulos where code=:code", {"code": code})
    b = cursor.fetchone()
    cursor.execute(f"UPDATE articulos SET price = {price} WHERE code = {code}")
    conexion.commit()
    conexion.close()
    cargar_datos()
    mensaje("Precio actualizado!")