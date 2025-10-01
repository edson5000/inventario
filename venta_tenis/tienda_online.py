import sqlite3
import getpass

# 🔹 Conectar a ambas bases
def conectar_db():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("ATTACH DATABASE 'ventas_tenis.db' AS tienda")
    return conn, cursor

# ================= CLIENTES =================
def registrar_cliente():
    conn, cursor = conectar_db()
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    contraseña = getpass.getpass("Contraseña: ")

    cursor.execute("INSERT INTO clientes(nombre) VALUES (?)", (nombre,))
    id_cliente = cursor.lastrowid

    cursor.execute("INSERT INTO login(id_cliente, correo, contraseña) VALUES (?, ?, ?)",
                   (id_cliente, correo, contraseña))
    conn.commit()
    conn.close()
    print("Cliente registrado correctamente.\n")

def login():
    conn, cursor = conectar_db()
    correo = input("Correo: ")
    contraseña = getpass.getpass("Contraseña: ")

    cursor.execute("SELECT id_cliente FROM login WHERE correo=? AND contraseña=?", (correo, contraseña))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        print("Bienvenido.\n")
        return resultado[0]
    else:
        print("Correo o contraseña incorrectos.\n")
        return None

# ================= FUNCIONES USUARIO =================
def ver_productos():
    conn, cursor = conectar_db()
    cursor.execute("SELECT id, nombre, talla, precio, stock FROM tienda.productos")
    productos = cursor.fetchall()
    conn.close()

    print("\n=== PRODUCTOS DISPONIBLES ===")
    for p in productos:
        print(f"ID: {p[0]} | Nombre: {p[1]} | Talla: {p[2]} | Precio: {p[3]} | Stock: {p[4]}")
    print()

def agregar_carrito(id_cliente):
    conn, cursor = conectar_db()
    id_producto = int(input("ID del producto a agregar: "))
    cantidad = int(input("Cantidad: "))

    cursor.execute("SELECT stock FROM tienda.productos WHERE id=?", (id_producto,))
    stock = cursor.fetchone()
    if not stock or stock[0] < cantidad:
        print("Stock insuficiente o producto inexistente.\n")
        conn.close()
        return

    cursor.execute("INSERT INTO carrito(id_cliente, id_producto, cantidad) VALUES (?, ?, ?)",
                   (id_cliente, id_producto, cantidad))
    conn.commit()
    conn.close()
    print("Producto agregado al carrito.\n")

def ver_carrito(id_cliente):
    conn, cursor = conectar_db()
    cursor.execute("""
    SELECT p.nombre, p.precio, carrito.cantidad
    FROM carrito
    JOIN tienda.productos AS p ON carrito.id_producto = p.id
    WHERE carrito.id_cliente = ?
    """, (id_cliente,))
    items = cursor.fetchall()
    conn.close()

    if not items:
        print("El carrito está vacío.\n")
        return

    print("\n=== CARRITO DE COMPRAS ===")
    total = 0
    for nombre, precio, cantidad in items:
        subtotal = precio * cantidad
        total += subtotal
        print(f"{nombre} | Precio: {precio} | Cantidad: {cantidad} | Subtotal: {subtotal}")
    print(f"TOTAL: {total}\n")

def crear_historial():
    conn, cursor = conectar_db()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        id_producto INTEGER,
        cantidad INTEGER,
        total REAL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carrito (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        id_producto INTEGER,
        cantidad INTEGER
    )
    """)
    # Asegurarse que tabla de ventas existe en ventas_tenis.db
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tienda.ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        id_producto INTEGER,
        cantidad INTEGER,
        total REAL
    )
    """)
    conn.commit()
    conn.close()

def finalizar_compra(id_cliente):
    conn, cursor = conectar_db()
    
    cursor.execute("SELECT id_producto, cantidad FROM carrito WHERE id_cliente = ?", (id_cliente,))
    items = cursor.fetchall()

    if not items:
        print("No hay productos en el carrito para comprar.\n")
        conn.close()
        return

    for id_producto, cantidad in items:
        cursor.execute("SELECT precio, stock FROM tienda.productos WHERE id=?", (id_producto,))
        resultado = cursor.fetchone()
        if not resultado:
            print(f"Producto ID {id_producto} no encontrado.")
            continue

        precio, stock = resultado
        if stock < cantidad:
            print(f"No hay stock suficiente para el producto ID {id_producto}.")
            continue

        total = precio * cantidad

        # Registrar venta en historial del cliente
        cursor.execute("""
            INSERT INTO historial(id_cliente, id_producto, cantidad, total) 
            VALUES (?, ?, ?, ?)
        """, (id_cliente, id_producto, cantidad, total))

        # Registrar venta en tabla de ventas para administrador
        cursor.execute("""
            INSERT INTO tienda.ventas(id_cliente, id_producto, cantidad, total)
            VALUES (?, ?, ?, ?)
        """, (id_cliente, id_producto, cantidad, total))

        # Actualizar stock en productos
        cursor.execute("UPDATE tienda.productos SET stock = stock - ? WHERE id=?", (cantidad, id_producto))

    # Limpiar carrito
    cursor.execute("DELETE FROM carrito WHERE id_cliente=?", (id_cliente,))
    conn.commit()
    conn.close()
    print("Compra finalizada. Productos movidos al historial, stock actualizado y venta registrada para administrador.\n")

def ver_historial(id_cliente):
    conn, cursor = conectar_db()
    cursor.execute("""
        SELECT p.nombre, h.cantidad, h.total
        FROM historial AS h
        JOIN tienda.productos AS p ON h.id_producto = p.id
        WHERE h.id_cliente = ?
    """, (id_cliente,))
    compras = cursor.fetchall()
    conn.close()

    if not compras:
        print("No tienes historial de compras.\n")
        return

    print("\n=== HISTORIAL DE COMPRAS ===")
    for nombre, cantidad, total in compras:
        print(f"Producto: {nombre} | Cantidad: {cantidad} | Total pagado: {total}")
    print()
