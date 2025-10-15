import sqlite3
from fpdf import FPDF

DB_CLIENTES = "clientes.db"
DB_PRODUCTOS = "ventas_tenis.db"

# -------------------- CONEXIÓN --------------------
def get_connection():
    conn = sqlite3.connect(DB_CLIENTES)
    conn.execute(f"ATTACH DATABASE '{DB_PRODUCTOS}' AS tienda")
    cursor = conn.cursor()
    return conn, cursor

# -------------------- PRODUCTOS --------------------
def crear_producto(id_prod, nombre, talla, color, precio, stock):
    conn, cursor = get_connection()
    try:
        cursor.execute(
            "INSERT INTO productos (id, nombre, talla, color, precio, stock) VALUES (?, ?, ?, ?, ?, ?)",
            (id_prod, nombre, talla, color, precio, stock)
        )
        conn.commit()
        print(f"Producto '{nombre}' agregado con ID {id_prod}.")
    except sqlite3.IntegrityError:
        print(f"Error: Ya existe un producto con ID {id_prod}.")
    finally:
        conn.close()

def listar_productos(order_by=None):
    conn, cursor = get_connection()
    query = "SELECT * FROM tienda.productos"
    if order_by == "nombre":
        query += " ORDER BY nombre ASC"
    elif order_by == "precio":
        query += " ORDER BY precio ASC"
    cursor.execute(query)
    productos = cursor.fetchall()
    conn.close()
    return productos

def buscar_productos(nombre=None, talla=None):
    conn, cursor = get_connection()
    query = "SELECT * FROM tienda.productos WHERE 1=1"
    params = []
    if nombre:
        query += " AND nombre LIKE ?"
        params.append(f"%{nombre}%")
    if talla:
        query += " AND talla=?"
        params.append(talla)
    cursor.execute(query, params)
    productos = cursor.fetchall()
    conn.close()
    return productos

def actualizar_producto(id_producto, nombre, talla, color, precio, stock):
    conn, cursor = get_connection()
    cursor.execute(
        "UPDATE tienda.productos SET nombre=?, talla=?, color=?, precio=?, stock=? WHERE id=?",
        (nombre, talla, color, precio, stock, id_producto)
    )
    conn.commit()
    conn.close()
    print(f"Producto ID {id_producto} actualizado.")

def eliminar_producto(id_producto):
    conn, cursor = get_connection()
    cursor.execute("DELETE FROM tienda.productos WHERE id=?", (id_producto,))
    conn.commit()
    conn.close()
    print(f"Producto ID {id_producto} eliminado.")

# -------------------- CLIENTES --------------------
def crear_cliente(id_cliente, nombre, correo):
    conn, cursor = get_connection()
    try:
        cursor.execute(
            "INSERT INTO clientes (id, nombre, correo) VALUES (?, ?, ?)",
            (id_cliente, nombre, correo)
        )
        conn.commit()
        print(f"Cliente '{nombre}' registrado con ID {id_cliente}.")
    except sqlite3.IntegrityError:
        print(f"Error: Ya existe un cliente con ID {id_cliente}.")
    finally:
        conn.close()

def listar_clientes():
    conn, cursor = get_connection()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def buscar_clientes(nombre=None, correo=None):
    conn, cursor = get_connection()
    query = "SELECT * FROM clientes WHERE 1=1"
    params = []
    if nombre:
        query += " AND nombre LIKE ?"
        params.append(f"%{nombre}%")
    if correo:
        query += " AND correo LIKE ?"
        params.append(f"%{correo}%")
    cursor.execute(query, params)
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def eliminar_cliente(id_cliente):
    conn, cursor = get_connection()
    cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
    conn.commit()
    conn.close()
    print(f"Cliente ID {id_cliente} eliminado.")

# -------------------- VENTAS --------------------
def registrar_venta(id_cliente, id_producto, cantidad):
    conn, cursor = get_connection()
    cursor.execute("SELECT nombre, precio, stock FROM tienda.productos WHERE id=?", (id_producto,))
    producto = cursor.fetchone()
    if not producto:
        print("Producto no encontrado.")
        conn.close()
        return
    nombre_prod, precio, stock = producto
    if cantidad > stock:
        print("Stock insuficiente.")
        conn.close()
        return
    total = precio * cantidad
    cursor.execute(
        "INSERT INTO ventas (id_cliente, id_producto, cantidad, total, fecha_hora) VALUES (?, ?, ?, ?, datetime('now','localtime'))",
        (id_cliente, id_producto, cantidad, total)
    )
    cursor.execute(
        "UPDATE tienda.productos SET stock = stock - ? WHERE id=?",
        (cantidad, id_producto)
    )
    conn.commit()
    conn.close()
    print(f"Venta registrada: {cantidad} x {nombre_prod} | Total: Bs{total}")

def listar_ventas():
    conn, cursor = get_connection()
    cursor.execute("""
        SELECT v.id, c.nombre AS cliente, p.nombre AS producto, v.cantidad, v.total, v.fecha_hora
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id
        JOIN tienda.productos p ON v.id_producto = p.id
        ORDER BY v.id ASC
    """)
    ventas = cursor.fetchall()
    conn.close()
    return ventas

def listar_ventas_por_cliente(id_cliente):
    conn, cursor = get_connection()
    cursor.execute("""
        SELECT v.id, p.nombre, v.cantidad, v.total, v.fecha_hora
        FROM ventas v
        JOIN tienda.productos p ON v.id_producto = p.id
        WHERE v.id_cliente = ?
    """, (id_cliente,))
    ventas = cursor.fetchall()
    conn.close()
    return ventas

def listar_ventas_por_producto(id_producto):
    conn, cursor = get_connection()
    cursor.execute("""
        SELECT v.id, c.nombre, v.cantidad, v.total, v.fecha_hora
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id
        WHERE v.id_producto = ?
    """, (id_producto,))
    ventas = cursor.fetchall()
    conn.close()
    return ventas

def listar_ventas_por_fecha(fecha_inicio, fecha_fin):
    conn, cursor = get_connection()
    cursor.execute("""
        SELECT v.id, c.nombre, p.nombre, v.cantidad, v.total, v.fecha_hora
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id
        JOIN tienda.productos p ON v.id_producto = p.id
        WHERE DATE(v.fecha_hora) BETWEEN ? AND ?
        ORDER BY v.fecha_hora ASC
    """, (fecha_inicio, fecha_fin))
    ventas = cursor.fetchall()
    conn.close()
    return ventas

def producto_mas_vendido():
    conn, cursor = get_connection()
    cursor.execute("""
        SELECT p.nombre, SUM(v.cantidad) as total_vendido
        FROM ventas v
        JOIN tienda.productos p ON v.id_producto = p.id
        GROUP BY v.id_producto
        ORDER BY total_vendido DESC
        LIMIT 10
    """)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def reporte_ingresos(periodo="dia"):
    conn, cursor = get_connection()
    if periodo == "dia":
        cursor.execute("""
            SELECT DATE(fecha_hora), SUM(total)
            FROM ventas
            GROUP BY DATE(fecha_hora)
        """)
    elif periodo == "semana":
        cursor.execute("""
            SELECT STRFTIME('%W', fecha_hora), SUM(total)
            FROM ventas
            GROUP BY STRFTIME('%W', fecha_hora)
        """)
    elif periodo == "mes":
        cursor.execute("""
            SELECT STRFTIME('%Y-%m', fecha_hora), SUM(total)
            FROM ventas
            GROUP BY STRFTIME('%Y-%m', fecha_hora)
        """)
    reportes = cursor.fetchall()
    conn.close()
    return reportes

def eliminar_venta(id_venta):
    conn, cursor = get_connection()
    cursor.execute("SELECT id_producto, cantidad FROM ventas WHERE id=?", (id_venta,))
    venta = cursor.fetchone()
    if not venta:
        print("Venta no encontrada.")
        conn.close()
        return
    id_producto, cantidad = venta
    cursor.execute("UPDATE tienda.productos SET stock = stock + ? WHERE id=?", (cantidad, id_producto))
    cursor.execute("DELETE FROM ventas WHERE id=?", (id_venta,))
    conn.commit()
    conn.close()
    print(f"Venta ID {id_venta} eliminada y stock actualizado.")

# -------------------- EXPORTAR PDF --------------------
def exportar_ventas_pdf(nombre_archivo="reporte_ventas.pdf"):
    ventas = listar_ventas()
    if not ventas:
        print("No hay ventas para exportar.")
        return
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Reporte de Ventas", ln=True, align="C")
    pdf.set_font("Arial", "B", 10)
    # Encabezado
    headers = ["ID", "Cliente", "Producto", "Cantidad", "Total", "Fecha/Hora"]
    for h in headers:
        pdf.cell(30, 8, str(h), border=1, align="C")
    pdf.ln()
    pdf.set_font("Arial", "", 10)
    # Contenido
    for v in ventas:
        for d in v:
            pdf.cell(30, 8, str(d), border=1, align="C")
        pdf.ln()
    pdf.output(nombre_archivo)
    print(f"Reporte exportado como {nombre_archivo}")
