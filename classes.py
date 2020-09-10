class Articulo:
    
    def __init__(self,name,precio, code,categoria=None):
        self.name = name
        self.code = code
        self.precio = precio
        self.categoria = categoria
        self.cantidad = 0
    
    def change(self):
        precio = input(f"\nPrecio actual: {self.precio}\nIngrese el precio nuevo: ")
        self.precio = precio
        print("\nEl precio se ha cambiado correctamente\n")
        input("Presiones una tecla para continuar...")
        clear_

class Persona:
    
    cuenta = 0
    
    def __init__(self, idx, name, dni, cuenta):
        self.idx = idx
        self.name = name
        self.dni = dni
        self.cuenta = cuenta
        
    def pagar(self,pago):
        clear_
        self.cuenta -= pago
    
    def agregar(self,resumen):
        self.cuenta += resumen
    
    def consulta_deuda(self,cuenta=cuenta):
        total = 0
        for tiket in self.cuenta:
            for articulo in tiket:
                total += articulo.precio
        return total
    
    def datos(self):
        return print(f"""
        Nombre: {self.name}
        DNI: {self.dni}
        Fiado: {self.cuenta}
        """)