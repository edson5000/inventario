import crud

def menu():
    while True:
        print("\n=== SISTEMA DE VENTAS DE TENIS ===")
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

        # ------------------ PRODUCTOS ------------------
        if opcion == "1":
            try:
                id_prod = int(input("ID del producto: "))
                nombre = input("Nombre del producto: ")
                talla = float(input("Talla: "))
                color = input("Color: ")
                precio = float(input("Precio: "))
                stock = int(input("Stock: "))
                crud.crear_producto(id_prod, nombre, talla, color, precio, stock)
            except ValueError:
                print("Entrada invalida, verifica los datos.")

        elif opcion == "2":
            productos = crud.listar_productos()
            if productos:
                print("\n--- Productos ---")
                for p in productos:
                    print(f"ID: {p[0]}, Nombre: {p[1]}, Talla: {p[2]}, Color: {p[3]}, Precio: Bs{p[4]}, Stock: {p[5]}")
            else:
                print("No hay productos registrados.")

        elif opcion == "3":
            try:
                id_producto = int(input("ID del producto a actualizar: "))
                nombre = input("Nuevo nombre: ")
                talla = float(input("Nueva talla: "))
                color = input("Nuevo color: ")
                precio = float(input("Nuevo precio: "))
                stock = int(input("Nuevo stock: "))
                crud.actualizar_producto(id_producto, nombre, talla, color, precio, stock)
            except ValueError:
                print("Entrada invalida, verifica los datos.")

        elif opcion == "4":
            try:
                id_producto = int(input("ID del producto a eliminar: "))
                crud.eliminar_producto(id_producto)
            except ValueError:
                print("Entrada invalida.")

        # ------------------ CLIENTES ------------------
        elif opcion == "5":
            try:
                id_cliente = int(input("ID del cliente: "))
                nombre = input("Nombre del cliente: ")
                correo = input("Correo del cliente: ")
                crud.crear_cliente(id_cliente, nombre, correo)
            except ValueError:
                print("Entrada invalida.")
        elif opcion == "6":
            clientes = crud.listar_clientes()
            if clientes:
                print("\n--- Clientes ---")
                for c in clientes:
                    id_c = c[0]
                    nombre = c[1]
                    correo = c[2] if len(c) > 2 else "No registrado"
                    print(f"ID: {id_c}, Nombre: {nombre}, Correo: {correo}")
            else:           
                     print("No hay clientes registrados.")

        elif opcion == "7":
            try:
                id_cliente = int(input("ID del cliente a eliminar: "))
                crud.eliminar_cliente(id_cliente)
            except ValueError:
                print("Entrada inválida.")

        # ------------------ VENTAS ------------------
        elif opcion == "8":
            print("\n--- Registrar venta ---")
            clientes = crud.listar_clientes()
            if not clientes:
                print("No hay clientes registrados.")
                continue
            for c in clientes:
                print(f"ID: {c[0]}, Nombre: {c[1]}")
            try:
                id_cliente = int(input("ID del cliente: "))
                id_producto = int(input("ID del producto: "))
                cantidad = int(input("Cantidad: "))
                crud.registrar_venta(id_cliente, id_producto, cantidad)
            except ValueError:
                print("Entrada inválida.")

        elif opcion == "9":
            ventas = crud.listar_ventas()
            if ventas:
                print("\n--- Ventas ---")
                for v in ventas:
                    print(f"ID Venta: {v[0]}, Cliente: {v[1]}, Producto: {v[2]}, Cantidad: {v[3]}, Total: Bs{v[4]}")
            else:
                print("No hay ventas registradas.")

        elif opcion == "10":
            try:
                id_venta = int(input("ID de la venta a eliminar: "))
                crud.eliminar_venta(id_venta)
            except ValueError:
                print("Entrada inválida.")

        # ------------------ SALIR ------------------
        elif opcion == "11":
            print("Saliendo del sistema...")
            break

        else:
            print("Opcion invalida. Intenta nuevamente.")

if __name__ == "__main__":
    menu()
