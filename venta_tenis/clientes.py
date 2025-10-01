import sqlite3

# Conectar directamente a la base de datos de clientes
conn = sqlite3.connect("clientes.db")
cursor = conn.cursor()

# Crear tabla de clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
)
""")

# Crear tabla de login
cursor.execute("""
CREATE TABLE IF NOT EXISTS login (
    id_cliente INTEGER PRIMARY KEY,
    correo TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
)
""")

# Crear tabla de carrito
cursor.execute("""
CREATE TABLE IF NOT EXISTS carrito (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    id_producto INTEGER,
    cantidad INTEGER,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
)
""")

# Crear tabla historial de compras
cursor.execute("""
CREATE TABLE IF NOT EXISTS historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    id_producto INTEGER,
    cantidad INTEGER,
    total REAL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
)
""")

conn.commit()
conn.close()
