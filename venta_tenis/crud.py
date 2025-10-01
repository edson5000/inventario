import sqlite3

DB_CLIENTES = "clientes.db"
DB_PRODUCTOS = "ventas_tenis.db"

# 🔹 Conexión a ambas bases
def get_connection():
    conn = sqlite3.connect(DB_CLIENTES)
    conn.execute(f"ATTACH DATABASE '{DB_PRODUCTOS}' AS tienda")
    cursor = conn.cursor()
    return conn, cursor

# =================== PRODUCTOS ===================
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

def listar_productos():
    conn, cursor = get_connection()
    cursor.execute("SELECT * FROM tienda.productos")
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

# =================== CLIENTES ===================
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

def eliminar_cliente(id_cliente):
    conn, cursor = get_connection()
    cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
    conn.commit()
    conn.close()
    print(f"Cliente ID {id_cliente} eliminado.")

# =================== VENTAS ===================
def registrar_venta(id_cliente, id_producto, cantidad):
    conn, cursor = get_connection()

    # Verificar producto
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

    # Registrar venta en clientes.db
    cursor.execute(
        "INSERT INTO ventas (id_cliente, id_producto, cantidad, total) VALUES (?, ?, ?, ?)",
        (id_cliente, id_producto, cantidad, total)
    )

    # Actualizar stock en productos
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
        SELECT v.id, c.nombre AS cliente, p.nombre AS producto, v.cantidad, v.total
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id
        JOIN tienda.productos p ON v.id_producto = p.id
        ORDER BY v.id ASC
    """)
    ventas = cursor.fetchall()
    conn.close()

    return ventas  # 👈 Solo devuelve la lista, no imprime


def listar_ventas_por_cliente(id_cliente):
    conn, cursor = get_connection()
    cursor.execute("""
        SELECT v.id, p.nombre, v.cantidad, v.total
        FROM ventas v
        JOIN tienda.productos p ON v.id_producto = p.id
        WHERE v.id_cliente = ?
    """, (id_cliente,))
    ventas = cursor.fetchall()
    conn.close()
    return ventas

def eliminar_venta(id_venta):
    conn, cursor = get_connection()

    # Obtener producto y cantidad
    cursor.execute("SELECT id_producto, cantidad FROM ventas WHERE id=?", (id_venta,))
    venta = cursor.fetchone()
    if not venta:
        print("Venta no encontrada.")
        conn.close()
        return

    id_producto, cantidad = venta

    # Restaurar stock
    cursor.execute("UPDATE tienda.productos SET stock = stock + ? WHERE id=?", (cantidad, id_producto))
    cursor.execute("DELETE FROM ventas WHERE id=?", (id_venta,))
    conn.commit()
    conn.close()
    print(f"Venta ID {id_venta} eliminada y stock actualizado.")
