# menu.py
import crud

def menu():
    while True:
        print("\n--- SISTEMA DE VENTAS DE TENIS ---")
        print("1. Crear producto")
        print("2. Listar productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Registrar cliente")
        print("6. Listar clientes")
        print("7. Eliminar cliente")
        print("8. Registrar venta")
        print("9. Listar ventas")
        print("10. Eliminar venta")
        print("11. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre del producto: ")
            talla = float(input("Talla: "))
            precio = float(input("Precio: "))
            stock = int(input("Stock: "))
            crud.crear_producto(nombre, talla, precio, stock)

        elif opcion == "2":
            productos = crud.listar_productos()
            if productos:
                print("\n--- Productos ---")
                for p in productos:
                    print(f"ID: {p[0]}, Nombre: {p[1]}, Talla: {p[2]}, Precio: Bs{p[3]}, Stock: {p[4]}")
            else:
                print("No hay productos registrados.")

        elif opcion == "3":
            id_producto = int(input("ID del producto a actualizar: "))
            nombre = input("Nuevo nombre: ")
            talla = float(input("Nueva talla: "))
            precio = float(input("Nuevo precio: "))
            stock = int(input("Nuevo stock: "))
            crud.actualizar_producto(id_producto, nombre, talla, precio, stock)

        elif opcion == "4":
            id_producto = int(input("ID del producto a eliminar: "))
            crud.eliminar_producto(id_producto)

        elif opcion == "5":
            nombre = input("Nombre del cliente: ")
            correo = input("Correo del cliente: ")
            crud.crear_cliente(nombre, correo)

        elif opcion == "6":
            clientes = crud.listar_clientes()
            if clientes:
                print("\n--- Clientes ---")
                for c in clientes:
                    print(f"ID: {c[0]}, Nombre: {c[1]}, Correo: {c[2]}")
            else:
                print("No hay clientes registrados.")

        elif opcion == "7":
            id_cliente = int(input("ID del cliente a eliminar: "))
            crud.eliminar_cliente(id_cliente)

        elif opcion == "8":
            id_cliente = int(input("ID del cliente: "))
            id_producto = int(input("ID del producto: "))
            cantidad = int(input("Cantidad: "))
            crud.registrar_venta(id_cliente, id_producto, cantidad)

        elif opcion == "9":
            ventas = crud.listar_ventas()
            if ventas:
                print("\n--- Ventas ---")
                for v in ventas:
                    print(f"ID Venta: {v[0]}, Cliente: {v[1]}, Producto: {v[2]}, Cantidad: {v[3]}, Total: Bs{v[4]}")
            else:
                print("No hay ventas registradas.")

        elif opcion == "10":
            id_venta = int(input("ID de la venta a eliminar: "))
            crud.eliminar_venta(id_venta)

        elif opcion == "11":
            print("Saliendo...")
            break
        else:
            print("Opcion invalida.")

if __name__ == "__main__":
    menu()
