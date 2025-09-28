# crud.py
import sqlite3

DB_NAME = "ventas_tenis.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

# --- Productos ---
def crear_producto(nombre, talla, precio, stock):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, talla, precio, stock) VALUES (?, ?, ?, ?)",
                   (nombre, talla, precio, stock))
    conn.commit()
    conn.close()
    print(f"Producto {nombre} agregado.")

def listar_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def actualizar_producto(id_producto, nombre, talla, precio, stock):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET nombre=?, talla=?, precio=?, stock=? WHERE id=?",
                   (nombre, talla, precio, stock, id_producto))
    conn.commit()
    conn.close()
    print(f"Producto ID {id_producto} actualizado.")

def eliminar_producto(id_producto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id_producto,))
    conn.commit()
    conn.close()
    print(f"Producto ID {id_producto} eliminado.")

# --- Clientes ---
def crear_cliente(nombre, correo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nombre, correo) VALUES (?, ?)", (nombre, correo))
    conn.commit()
    conn.close()
    print(f"Cliente {nombre} registrado.")

def listar_clientes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def eliminar_cliente(id_cliente):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
    conn.commit()
    conn.close()
    print(f"Cliente ID {id_cliente} eliminado.")

# --- Ventas ---
def registrar_venta(id_cliente, id_producto, cantidad):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT precio, stock FROM productos WHERE id=?", (id_producto,))
    producto = cursor.fetchone()
    if not producto:
        print("Producto no encontrado.")
        conn.close()
        return
    precio, stock = producto
    if cantidad > stock:
        print("Stock insuficiente.")
        conn.close()
        return
    total = precio * cantidad
    cursor.execute("INSERT INTO ventas (id_cliente, id_producto, cantidad, total) VALUES (?, ?, ?, ?)",
                   (id_cliente, id_producto, cantidad, total))
    cursor.execute("UPDATE productos SET stock=? WHERE id=?", (stock - cantidad, id_producto))
    conn.commit()
    conn.close()
    print(f"Venta registrada. Total: Bs{total}")

def listar_ventas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT v.id, c.nombre, p.nombre, v.cantidad, v.total
    FROM ventas v
    JOIN clientes c ON v.id_cliente = c.id
    JOIN productos p ON v.id_producto = p.id
    """)
    ventas = cursor.fetchall()
    conn.close()
    return ventas

def eliminar_venta(id_venta):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_producto, cantidad FROM ventas WHERE id=?", (id_venta,))
    venta = cursor.fetchone()
    if not venta:
        print("Venta no encontrada.")
        conn.close()
        return
    id_producto, cantidad = venta
    cursor.execute("UPDATE productos SET stock = stock + ? WHERE id=?", (cantidad, id_producto))
    cursor.execute("DELETE FROM ventas WHERE id=?", (id_venta,))
    conn.commit()
    conn.close()
    print(f"Venta ID {id_venta} eliminada y stock actualizado.")
