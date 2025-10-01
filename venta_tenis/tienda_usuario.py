import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

DB_CLIENTES = "clientes.db"
DB_VENTAS = "ventas_tenis.db"

# ----------------- Conexiones -----------------
def get_clientes_connection():
    return sqlite3.connect(DB_CLIENTES)

def get_ventas_connection():
    return sqlite3.connect(DB_VENTAS)

# ----------------- Usuarios -----------------
def init_clientes():
    conn = get_clientes_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        correo TEXT,
        contrasena TEXT
    )
    """)
    conn.commit()
    conn.close()

def registrar_cliente_db(nombre, correo, contrasena):
    conn = get_clientes_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM clientes WHERE correo=?", (correo,))
    if cursor.fetchone():
        conn.close()
        return False
    cursor.execute("INSERT INTO clientes (nombre, correo, contrasena) VALUES (?, ?, ?)",
                   (nombre, correo, contrasena))
    conn.commit()
    conn.close()
    return True

def login_db(correo, contrasena):
    conn = get_clientes_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM clientes WHERE correo=? AND contrasena=?", (correo, contrasena))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

# ----------------- Productos -----------------
def obtener_productos():
    conn = get_ventas_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, talla, color, precio, stock FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def registrar_venta(id_cliente, carrito):
    conn = get_ventas_connection()
    cursor = conn.cursor()
    for item in carrito:
        cursor.execute("INSERT INTO ventas (id_cliente, id_producto, cantidad, total) VALUES (?, ?, ?, ?)",
                       (id_cliente, item['id'], item['cantidad'], item['precio']*item['cantidad']))
        cursor.execute("UPDATE productos SET stock=stock-? WHERE id=?", (item['cantidad'], item['id']))
    conn.commit()
    conn.close()

def ver_historial_db(id_cliente):
    conn = get_ventas_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT v.id, p.nombre, v.cantidad, v.total
    FROM ventas v
    JOIN productos p ON v.id_producto = p.id
    WHERE v.id_cliente=?
    """, (id_cliente,))
    ventas = cursor.fetchall()
    conn.close()
    return ventas

# ----------------- Interfaz -----------------
class UsuarioApp(App):
    def build(self):
        init_clientes()
        self.usuario = None
        self.carrito = []

        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.label = Label(text="Bienvenido a la tienda de tenis", font_size=24, size_hint=(1, 0.1))
        self.root.add_widget(self.label)

        # Layout principal para botones
        self.botones_layout = BoxLayout(size_hint=(1, 0.1))
        self.root.add_widget(self.botones_layout)

        # Contenido dinámico
        self.content = BoxLayout(orientation='vertical')
        self.root.add_widget(self.content)

        self.mostrar_menu_principal()
        return self.root

    def mostrar_menu_principal(self):
        self.botones_layout.clear_widgets()
        self.content.clear_widgets()

        btn_registrar = Button(text="Registrar", on_press=self.mostrar_registro)
        btn_login = Button(text="Iniciar Sesion", on_press=self.mostrar_login)
        self.botones_layout.add_widget(btn_registrar)
        self.botones_layout.add_widget(btn_login)

    def mostrar_registro(self, instance):
        self.content.clear_widgets()
        self.content.add_widget(Label(text="Registro de Usuario", size_hint=(1, 0.1)))
        self.input_nombre = TextInput(hint_text="Nombre", multiline=False)
        self.input_correo = TextInput(hint_text="Correo", multiline=False)
        self.input_pass = TextInput(hint_text="Contraseña", multiline=False, password=True)
        self.content.add_widget(self.input_nombre)
        self.content.add_widget(self.input_correo)
        self.content.add_widget(self.input_pass)
        btn_registrar = Button(text="Registrar", on_press=self.registrar_usuario)
        self.content.add_widget(btn_registrar)

    def registrar_usuario(self, instance):
        nombre = self.input_nombre.text
        correo = self.input_correo.text
        contrasena = self.input_pass.text
        if registrar_cliente_db(nombre, correo, contrasena):
            self.label.text = f"Usuario {nombre} registrado correctamente"
            self.mostrar_menu_principal()
        else:
            self.label.text = "Error: Correo ya registrado"

    def mostrar_login(self, instance):
        self.content.clear_widgets()
        self.content.add_widget(Label(text="Iniciar Sesion", size_hint=(1, 0.1)))
        self.input_login_correo = TextInput(hint_text="Correo", multiline=False)
        self.input_login_pass = TextInput(hint_text="Contraseña", multiline=False, password=True)
        self.content.add_widget(self.input_login_correo)
        self.content.add_widget(self.input_login_pass)
        btn_login = Button(text="Iniciar Sesion", on_press=self.login_usuario)
        self.content.add_widget(btn_login)

    def login_usuario(self, instance):
        correo = self.input_login_correo.text
        contrasena = self.input_login_pass.text
        usuario = login_db(correo, contrasena)
        if usuario:
            self.usuario = usuario
            self.label.text = f"Bienvenido {usuario[1]}"
            self.mostrar_menu_usuario()
        else:
            self.label.text = "Correo o contraseña incorrectos"

    def mostrar_menu_usuario(self):
        self.content.clear_widgets()
        self.botones_layout.clear_widgets()

        btn_ver_productos = Button(text="Ver productos", on_press=self.ver_productos_ui)
        btn_ver_carrito = Button(text="Ver carrito", on_press=self.ver_carrito_ui)
        btn_finalizar = Button(text="Finalizar compra", on_press=self.finalizar_compra_ui)
        btn_historial = Button(text="Ver historial", on_press=self.ver_historial_ui)
        btn_salir = Button(text="Cerrar sesión", on_press=self.cerrar_sesion)

        for btn in [btn_ver_productos, btn_ver_carrito, btn_finalizar, btn_historial, btn_salir]:
            self.botones_layout.add_widget(btn)

    def ver_productos_ui(self, instance):
        self.content.clear_widgets()
        scroll = ScrollView()
        layout = GridLayout(cols=1, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))

        for p in obtener_productos():
            pid, nombre, talla, color, precio, stock = p
            lbl = Label(text=f"ID:{pid} {nombre} | Talla:{talla} | Color:{color} | Precio:{precio} | Stock:{stock}",
                        size_hint_y=None, height=30)
            layout.add_widget(lbl)
            btn = Button(text="Agregar al carrito", size_hint_y=None, height=30)
            btn.bind(on_press=lambda inst, pid=pid, nombre=nombre, precio=precio: self.agregar_carrito_ui(pid, nombre, precio))
            layout.add_widget(btn)
        scroll.add_widget(layout)
        self.content.add_widget(scroll)

    def agregar_carrito_ui(self, pid, nombre, precio):
        if not self.usuario:
            self.label.text = "Debes iniciar sesión primero"
            return
        self.carrito.append({"id": pid, "nombre": nombre, "precio": precio, "cantidad": 1})
        self.label.text = f"{nombre} agregado al carrito"

    def ver_carrito_ui(self, instance):
        self.content.clear_widgets()
        total = 0
        if not self.carrito:
            self.content.add_widget(Label(text="Carrito vacío"))
            return
        for item in self.carrito:
            subtotal = item["precio"]*item["cantidad"]
            total += subtotal
            self.content.add_widget(Label(text=f"{item['nombre']} x {item['cantidad']} = {subtotal}"))
        self.content.add_widget(Label(text=f"Total: {total}"))

    def finalizar_compra_ui(self, instance):
        if not self.usuario:
            self.label.text = "Debes iniciar sesión"
            return
        registrar_venta(self.usuario[0], self.carrito)
        self.carrito.clear()
        self.label.text = "Compra realizada con éxito"
        self.content.clear_widgets()

    def ver_historial_ui(self, instance):
        self.content.clear_widgets()
        historial = ver_historial_db(self.usuario[0])
        if not historial:
            self.content.add_widget(Label(text="No hay compras realizadas"))
            return
        for h in historial:
            self.content.add_widget(Label(text=f"ID:{h[0]} Producto:{h[1]} Cantidad:{h[2]} Total:{h[3]}"))

    def cerrar_sesion(self, instance):
        self.usuario = None
        self.carrito = []
        self.label.text = "Sesión cerrada"
        self.mostrar_menu_principal()

if __name__ == "__main__":
    UsuarioApp().run()
