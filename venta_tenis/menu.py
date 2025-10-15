import os
import crud
from tabulate import tabulate
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + "="*60)
        print(Fore.YELLOW + "\\ SISTEMA DE VENTAS DE TENIS //".center(60))
        print(Fore.CYAN + "="*60 + Style.RESET_ALL)
        
        opciones = [
            "Crear producto", "Listar productos", "Actualizar producto", "Eliminar producto",
            "Registrar cliente", "Listar clientes", "Eliminar cliente",
            "Registrar venta", "Listar todas las ventas", "Listar ventas por cliente",
            "Listar ventas por...", "Reporte de ingresos", "Reporte de todas las ventas", "Salir"
        ]
        for i, opcion_texto in enumerate(opciones, start=1):
            print(Fore.BLUE + f"{i}. {Style.RESET_ALL}{opcion_texto}")
        print(Fore.CYAN + "-"*60 + Style.RESET_ALL)
        opcion = input(Fore.YELLOW + "Elige una opcion: " + Style.RESET_ALL)

        # ------------------ PRODUCTOS ------------------
        if opcion == "1":  # Crear producto
            limpiar_pantalla()
            try:
                id_prod = int(input("ID del producto: "))
                nombre = input("Nombre del producto: ")
                talla = float(input("Talla: "))
                color = input("Color: ")
                precio = float(input("Precio: "))
                stock = int(input("Stock: "))
                crud.crear_producto(id_prod, nombre, talla, color, precio, stock)
                print(Fore.GREEN + "Producto creado correctamente.")
            except ValueError:
                print(Fore.RED + "Entrada invalida.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "2":  # Listar productos
            limpiar_pantalla()
            try:
                productos = crud.listar_productos(order_by="nombre")
                if productos:
                    headers = ["ID", "Nombre", "Talla", "Color", "Precio (Bs)", "Stock"]
                    print(tabulate(productos, headers=headers, tablefmt="fancy_grid"))
                else:
                    print(Fore.RED + "No hay productos registrados.")
            except Exception as e:
                print(Fore.RED + f"Error al listar productos: {e}")
            input("\nPresiona Enter para continuar...")

        elif opcion == "3":  # Actualizar producto
            limpiar_pantalla()
            try:
                id_producto = int(input("ID del producto a actualizar: "))
                nombre = input("Nuevo nombre: ")
                talla = float(input("Nueva talla: "))
                color = input("Nuevo color: ")
                precio = float(input("Nuevo precio: "))
                stock = int(input("Nuevo stock: "))
                crud.actualizar_producto(id_producto, nombre, talla, color, precio, stock)
                print(Fore.GREEN + "Producto actualizado correctamente.")
            except ValueError:
                print(Fore.RED + "Entrada invalida.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "4":  # Eliminar producto
            limpiar_pantalla()
            try:
                id_producto = int(input("ID del producto a eliminar: "))
                crud.eliminar_producto(id_producto)
                print(Fore.GREEN + "Producto eliminado correctamente.")
            except ValueError:
                print(Fore.RED + "Entrada invalida.")
            input("\nPresiona Enter para continuar...")

        # ------------------ CLIENTES ------------------
        elif opcion == "5":  # Registrar cliente
            limpiar_pantalla()
            try:
                id_cliente = int(input("ID del cliente: "))
                nombre = input("Nombre: ")
                correo = input("Correo o Telefono: ")
                crud.crear_cliente(id_cliente, nombre, correo)
                print(Fore.GREEN + "Cliente registrado correctamente.")
            except ValueError:
                print(Fore.RED + "Entrada invalida.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "6":  # Listar clientes
            limpiar_pantalla()
            clientes = crud.listar_clientes()
            if clientes:
                headers = ["ID", "Nombre", "Correo/Telefono"]
                print(tabulate(clientes, headers=headers, tablefmt="fancy_grid"))
            else:
                print(Fore.RED + "No hay clientes registrados.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "7":  # Eliminar cliente
            limpiar_pantalla()
            try:
                id_cliente = int(input("ID del cliente a eliminar: "))
                crud.eliminar_cliente(id_cliente)
                print(Fore.GREEN + "Cliente eliminado correctamente.")
            except ValueError:
                print(Fore.RED + "Entrada invalida.")
            input("\nPresiona Enter para continuar...")

        # ------------------ VENTAS ------------------
        elif opcion == "8":  # Registrar venta
            limpiar_pantalla()
            clientes = crud.listar_clientes()
            if not clientes:
                print(Fore.RED + "No hay clientes registrados.")
                input("\nPresiona Enter para continuar...")
                continue
            for c in clientes:
                print(f"ID: {c[0]} | Nombre: {c[1]}")
            try:
                id_cliente = int(input("ID del cliente: "))
                id_producto = int(input("ID del producto: "))
                cantidad = int(input("Cantidad: "))
                crud.registrar_venta(id_cliente, id_producto, cantidad)
                print(Fore.GREEN + "Venta registrada correctamente.")
            except ValueError:
                print(Fore.RED + "Entrada invalida.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "9":  # Listar todas las ventas
            limpiar_pantalla()
            ventas = crud.listar_ventas()
            if ventas:
                headers = ["ID Venta", "Cliente", "Producto", "Cantidad", "Total (Bs)", "Fecha/Hora"]
                print(tabulate(ventas, headers=headers, tablefmt="fancy_grid"))
            else:
                print(Fore.RED + "No hay ventas registradas.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "10":  # Listar ventas por cliente
            limpiar_pantalla()
            try:
                id_cliente = int(input("ID del cliente: "))
                ventas = crud.listar_ventas_por_cliente(id_cliente)
                if ventas:
                    headers = ["ID Venta", "Producto", "Cantidad", "Total (Bs)", "Fecha/Hora"]
                    print(tabulate(ventas, headers=headers, tablefmt="fancy_grid"))
                else:
                    print(Fore.RED + "No hay ventas para este cliente.")
            except ValueError:
                print(Fore.RED + "Entrada invalida.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "11":  # Submenu listar ventas por...
            while True:
                limpiar_pantalla()
                print("Listar ventas por:")
                print("1. ID Producto")
                print("2. Volver al menu principal")
                sub_opcion = input("Elige una opcion: ")
                

                if sub_opcion == "1":
                    try:
                        id_producto = int(input("ID del producto: "))
                        ventas = crud.listar_ventas_por_producto(id_producto)
                        headers = ["ID Venta", "Cliente", "Cantidad", "Total (Bs)", "Fecha/Hora"]
                        print(tabulate(ventas, headers=headers, tablefmt="fancy_grid") if ventas else "No hay ventas")
                    except ValueError:
                        print("Entrada invalida")
                    input("\nPresiona Enter para continuar...")

                elif sub_opcion == "2":
                    break
                else:
                    print("Opcion invalida")
                    input("\nPresiona Enter para continuar...")

        elif opcion == "12":  # Reporte de ingresos
            limpiar_pantalla()
            periodo = input("Periodo (dia/semana/mes): ").lower()
            ingresos = crud.reporte_ingresos(periodo)
            headers = ["Periodo", "Ingresos (Bs)"]
            print(tabulate(ingresos, headers=headers, tablefmt="fancy_grid") if ingresos else "No hay datos")
            input("\nPresiona Enter para continuar...")

        elif opcion == "13":  # Exportar ventas a PDF
            limpiar_pantalla()
            try:
                from fpdf import FPDF
                ventas = crud.listar_ventas()
                if not ventas:
                    print("No hay ventas para exportar")
                    input("\nPresiona Enter para continuar...")
                    continue

                pdf = FPDF(orientation="L", unit="mm", format="A4")
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, "Reporte de Ventas", ln=True, align="C")
                pdf.ln(5)

                encabezados = ["ID Venta", "Cliente", "Producto", "Cantidad", "Total (Bs)", "Fecha/Hora"]

                # Calcular ancho maximo de cada columna
                pdf.set_font("Arial", "B", 12)
                col_widths = []
                for i, h in enumerate(encabezados):
                    max_width = pdf.get_string_width(h) + 10
                    for row in ventas:
                        cell_width = pdf.get_string_width(str(row[i])) + 10
                        if cell_width > max_width:
                            max_width = cell_width
                    col_widths.append(max_width)

                # Ajustar al ancho total de la pagina si excede
                page_width = pdf.w - 2*pdf.l_margin
                total_width = sum(col_widths)
                if total_width > page_width:
                    scale = page_width / total_width
                    col_widths = [w * scale for w in col_widths]

                def dibujar_encabezado():
                    pdf.set_font("Arial", "B", 12)
                    for i, h in enumerate(encabezados):
                        pdf.cell(col_widths[i], 10, h, border=1, align="C")
                    pdf.ln()

                dibujar_encabezado()
                pdf.set_font("Arial", "", 12)

                for row in ventas:
                    for i, data in enumerate(row):
                        align = "C" if i in [0, 3] else "L"
                        pdf.cell(col_widths[i], 8, str(data), border=1, align=align)
                    pdf.ln()
                    if pdf.get_y() > 180:
                        pdf.add_page()
                        dibujar_encabezado()

                pdf.output("reporte_ventas.pdf")
                print(Fore.GREEN + "PDF generado correctamente: reporte_ventas.pdf")
            except ImportError:
                print(Fore.RED + "Debes instalar fpdf: pip install fpdf")
            input("\nPresiona Enter para continuar...")

        elif opcion == "14":  # Salir
            limpiar_pantalla()
            print(Fore.RED + "Saliendo del sistema... Hasta pronto.")
            break

        else:
            print(Fore.RED + "Opcion invalida")
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    menu()
