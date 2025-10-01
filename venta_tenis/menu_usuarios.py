from tienda_online import registrar_cliente, login, ver_productos, agregar_carrito, ver_carrito, finalizar_compra, ver_historial, crear_historial

def sub_menu(id_cliente):
    crear_historial()
    while True:
        print("\n==== MENU USUARIO ====")
        print("1. Ver productos")
        print("2. Agregar producto al carrito")
        print("3. Ver carrito")
        print("4. Finalizar compra")
        print("5. Ver historial de compras")
        print("6. Cerrar Sesion")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            ver_productos()
        elif opcion == "2":
            agregar_carrito(id_cliente)
        elif opcion == "3":
            ver_carrito(id_cliente)
        elif opcion == "4":
            finalizar_compra(id_cliente)
        elif opcion == "5":
            ver_historial(id_cliente)
        elif opcion == "6":
            break
        else:
            print("Opción invalida.\n")

def menu():
    while True:
        print("\n==== MENU CLIENTES ====")
        print("1. Registrar")
        print("2. Iniciar Sesion")
        print("3. Salir")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            id_cliente = login()
            if id_cliente:
                sub_menu(id_cliente)
        elif opcion == "3":
            print("Gracias por visitarnos!!!...")
            break
        else:
            print("Opción invalida.\n")

if __name__ == "__main__":
    menu()
