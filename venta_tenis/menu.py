import os
import crud
from tabulate import tabulate
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Función para limpiar la pantalla según el sistema operativo
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "="*60)
        print(Fore.YELLOW + "\\\SISTEMA DE VENTAS DE TENIS///".center(60))
        print(Fore.CYAN + "="*60 + Style.RESET_ALL)
        
        opciones = [
            "Crear producto", "Listar productos", "Actualizar producto",
            "Eliminar producto", "Registrar cliente", "Listar clientes",
            "Eliminar cliente", "Registrar venta", "Listar todas las ventas",
            "Listar ventas por cliente", "Salir"
        ]
        
        for i, opcion_texto in enumerate(opciones, start=1):
            color = Fore.BLUE if i <= 4 else Fore.BLUE if i <= 7 else Fore.BLUE if i <= 10 else Fore.RED
            print(f"{color}{i}. {Style.RESET_ALL}{opcion_texto}")
        print(Fore.CYAN + "-"*60 + Style.RESET_ALL)

        opcion = input(Fore.YELLOW + "Elige una opción: " + Style.RESET_ALL)

        # ------------------ PRODUCTOS ------------------
        if opcion == "1":
            limpiar_pantalla()
            print(Fore.CYAN + "CREAR PRODUCTO\n" + Style.RESET_ALL)
            try:
                id_prod = int(input("ID del producto: "))
                nombre = input("Nombre del producto: ")
                talla = float(input("Talla: "))
                color = input("Color: ")
                precio = float(input("Precio: "))
                stock = int(input("Stock: "))
                crud.crear_producto(id_prod, nombre, talla, color, precio, stock)
            except ValueError:
                print(Fore.RED + "Entrada inválida, verifica los datos.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "2":
            limpiar_pantalla()
            productos = crud.listar_productos()
            if productos:
                headers = ["ID", "Nombre", "Talla", "Color", "Precio (Bs)", "Stock"]
                print(Fore.CYAN + "\nPRODUCTOS REGISTRADOS" + Style.RESET_ALL)
                print(tabulate(productos, headers=headers, tablefmt="fancy_grid"))
            else:
                print(Fore.RED + "No hay productos registrados.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "3":
            limpiar_pantalla()
            print(Fore.CYAN + "\nACTUALIZAR PRODUCTO" + Style.RESET_ALL)
            try:
                id_producto = int(input("ID del producto a actualizar: "))
                nombre = input("Nuevo nombre: ")
                talla = float(input("Nueva talla: "))
                color = input("Nuevo color: ")
                precio = float(input("Nuevo precio: "))
                stock = int(input("Nuevo stock: "))
                crud.actualizar_producto(id_producto, nombre, talla, color, precio, stock)
            except ValueError:
                print(Fore.RED + "Entrada inválida, verifica los datos.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "4":
            limpiar_pantalla()
            print(Fore.CYAN + "\nELIMINAR PRODUCTO" + Style.RESET_ALL)
            try:
                id_producto = int(input("ID del producto a eliminar: "))
                crud.eliminar_producto(id_producto)
            except ValueError:
                print(Fore.RED + "Entrada inválida.")
            input("\nPresiona Enter para continuar...")

        # ------------------ CLIENTES ------------------
        elif opcion == "5":
            limpiar_pantalla()
            print(Fore.CYAN + "\nREGISTRAR CLIENTE" + Style.RESET_ALL)
            try:
                id_cliente = int(input("ID del cliente: "))
                nombre = input("Nombre del cliente: ")
                correo = input("Correo del cliente o Numero de telefono: ")
                crud.crear_cliente(id_cliente, nombre, correo)
            except ValueError:
                print(Fore.RED + "Entrada inválida.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "6":
            limpiar_pantalla()
            clientes = crud.listar_clientes()
            if clientes:
                headers = ["ID", "Nombre", "Correo"]
                print(Fore.CYAN + "\nCLIENTES REGISTRADOS" + Style.RESET_ALL)
                print(tabulate(clientes, headers=headers, tablefmt="fancy_grid"))
            else:
                print(Fore.RED + "No hay clientes registrados.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "7":
            limpiar_pantalla()
            print(Fore.CYAN + "\nELIMINAR CLIENTE" + Style.RESET_ALL)
            try:
                id_cliente = int(input("ID del cliente a eliminar: "))
                crud.eliminar_cliente(id_cliente)
            except ValueError:
                print(Fore.RED + "Entrada inválida.")
            input("\nPresiona Enter para continuar...")

        # ------------------ VENTAS ------------------
        elif opcion == "8":
            limpiar_pantalla()
            print(Fore.CYAN + "\nREGISTRAR VENTA" + Style.RESET_ALL)
            clientes = crud.listar_clientes()
            if not clientes:
                print(Fore.RED + "No hay clientes registrados.")
                input("\nPresiona Enter para continuar...")
                continue
            for c in clientes:
                print(f"ID: {c[0]}, Nombre: {c[1]}")
            try:
                id_cliente = int(input("ID del cliente: "))
                id_producto = int(input("ID del producto: "))
                cantidad = int(input("Cantidad: "))
                crud.registrar_venta(id_cliente, id_producto, cantidad)
            except ValueError:
                print(Fore.RED + "Entrada inválida.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "9":
            limpiar_pantalla()
            ventas = crud.listar_ventas()
            if ventas:
                headers = ["ID Venta", "Cliente", "Producto", "Cantidad", "Total (Bs)"]
                print(Fore.CYAN + "\nTODAS LAS VENTAS" + Style.RESET_ALL)
                print(tabulate(ventas, headers=headers, tablefmt="fancy_grid"))
            else:
                print(Fore.RED + "No hay ventas registradas.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "10":
            limpiar_pantalla()
            try:
                id_cliente = int(input("ID del cliente para ver sus ventas: "))
                ventas = crud.listar_ventas_por_cliente(id_cliente)
                if ventas:
                    headers = ["ID Venta", "Producto", "Cantidad", "Total (Bs)"]
                    print(Fore.CYAN + f"\nVENTAS DEL CLIENTE ID {id_cliente}" + Style.RESET_ALL)
                    print(tabulate(ventas, headers=headers, tablefmt="fancy_grid"))
                else:
                    print(Fore.RED + "El cliente no tiene ventas registradas.")
            except ValueError:
                print(Fore.RED + "Entrada inválida.")
            input("\nPresiona Enter para continuar...")

        # ------------------ SALIR ------------------
        elif opcion == "11":
            limpiar_pantalla()
            print(Fore.RED + "Saliendo del sistema... ¡Hasta pronto!")
            break

        else:
            print(Fore.RED + "Opción inválida. Intenta nuevamente.")
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    menu()
