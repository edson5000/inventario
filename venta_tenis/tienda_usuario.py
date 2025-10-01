import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from venta_tenis.clientes import crear_tabla_usuarios, registrar_usuario, iniciar_sesion

DB_VENTAS = "ventas_tenis.db"
DB_CLIENTES = "clientes.db"

# ---------------- Funciones de productos y ventas ----------------
def obtener_productos():
    conn = sqlite3.connect(DB_VENTAS)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, talla, color, precio, stock FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def registrar_venta(usuario_id, carrito):
    if not carrito:
        return
    conn = sqlite3.connect(DB_VENTAS)
    cursor = conn.cursor()
    for item in carrito:
        # Inserta venta
        cursor.execute("""
            INSERT INTO ventas (id_cliente, id_producto, cantidad, total)
            VALUES (?, ?, ?, ?)
        """, (usuario_id, item["id"], item["cantidad"], item["precio"] * item["cantidad"]))
        # Actualiza stock
        cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (item["cantidad"], item["id"]))
    conn.commit()
    conn.close()

# ---------------- Interfaz Kivy ----------------
class TiendaApp(App):
    def build(self):
        crear_tabla_usuarios()  # Asegura tabla usuarios
        self.usuario = None
        self.carrito = []

        self.root = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.label = Label(text="Bienvenido a la tienda de tenis", font_size=24, size_hint=(1, 0.1))
        self.root.add_widget(self.label)

        # Botones principales
        btn_layout = BoxLayout(size_hint=(1, 0.1))
        btn_layout.add_widget(Button(text="Registrar Usuario", on_press=self.mostrar_registro))
        btn_layout.add_widget(Button(text="Iniciar Sesión", on_press=self.mostrar_login))
        btn_layout.add_widget(Button(text="Ver Productos", on_press=self.mostrar_productos))
        btn_layout.add_widget(Button(text="Ver Carrito", on_press=self.mostrar_carrito))
        self.root.add_widget(btn_layout)

        self.content = BoxLayout(orientation="vertical")
        self.root.add_widget(self.content)
        return self.root

    # ---------------- Registro de usuario ----------------
    def mostrar_registro(self, instance):
        self.content.clear_widgets()
        self.content.add_widget(Label(text="Registro de Usuario", size_hint=(1, 0.1)))

        self.nombre_input = TextInput(hint_text="Nombre", multiline=False)
        self.correo_input = TextInput(hint_text="Correo", multiline=False)
        self.pass_input = TextInput(hint_text="Contraseña", multiline=False, password=True)

        self.content.add_widget(self.nombre_input)
        self.content.add_widget(self.correo_input)
        self.content.add_widget(self.pass_input)

        btn_registrar = Button(text="Registrar", on_press=self.registrar_usuario_ui)
        self.content.add_widget(btn_registrar)

    def registrar_usuario_ui(self, instance):
        nombre = self.nombre_input.text.strip()
        correo = self.correo_input.text.strip()
        contraseña = self.pass_input.text.strip()
        if not nombre or not correo or not contraseña:
            self.label.text = "Completa todos los campos"
            return
        if registrar_usuario(nombre, correo, contraseña):
            self.label.text = f"Usuario {nombre} registrado correctamente."
        else:
            self.label.text = "Error: El correo ya existe."

    # ---------------- Login ----------------
    def mostrar_login(self, instance):
        self.content.clear_widgets()
        self.content.add_widget(Label(text="Iniciar Sesión", size_hint=(1, 0.1)))

        self.login_correo = TextInput(hint_text="Correo", multiline=False)
        self.login_pass = TextInput(hint_text="Contraseña", multiline=False, password=True)
        self.content.add_widget(self.login_correo)
        self.content.add_widget(self.login_pass)

        btn_login = Button(text="Iniciar Sesión", on_press=self.login_ui)
        self.content.add_widget(btn_login)

    def login_ui(self, instance):
        correo = self.login_correo.text.strip()
        contraseña = self.login_pass.text.strip()
        usuario = iniciar_sesion(correo, contraseña)
        if usuario:
            self.usuario = usuario
            self.label.text = f"Bienvenido {usuario[1]}"
        else:
            self.label.text = "Correo o contraseña incorrectos"

    # ---------------- Mostrar productos ----------------
    def mostrar_productos(self, instance):
        self.content.clear_widgets()
        productos = obtener_productos()
        if not productos:
            self.content.add_widget(Label(text="No hay productos disponibles"))
            return

        scroll = ScrollView(size_hint=(1, 1))
        layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=5)
        layout.bind(minimum_height=layout.setter('height'))

        for p in productos:
            lbl = Label(text=f"ID:{p[0]} {p[1]} | Talla:{p[2]} | Color:{p[3]} | Precio:{p[4]} | Stock:{p[5]}",
                        size_hint_y=None, height=30)
            layout.add_widget(lbl)
            btn = Button(text="Agregar al carrito", size_hint_y=None, height=30)
            btn.bind(on_press=lambda inst, pid=p[0], nombre=p[1], precio=p[4]: self.agregar_carrito_ui(pid, nombre, precio))
            layout.add_widget(btn)

        scroll.add_widget(layout)
        self.content.add_widget(scroll)

    def agregar_carrito_ui(self, pid, nombre, precio):
        if not self.usuario:
            self.label.text = "Debes iniciar sesión primero"
            return
        # Verifica si el producto ya está en el carrito
        for item in self.carrito:
            if item["id"] == pid:
                item["cantidad"] += 1
                self.label.text = f"Se sumó 1 unidad a {nombre} en el carrito"
                return
        self.carrito.append({"id": pid, "nombre": nombre, "precio": precio, "cantidad": 1})
        self.label.text = f"{nombre} agregado al carrito"

    # ---------------- Mostrar carrito ----------------
    def mostrar_carrito(self, instance):
        self.content.clear_widgets()
        self.content.add_widget(Label(text="Carrito", size_hint=(1, 0.1)))
        if not self.carrito:
            self.content.add_widget(Label(text="El carrito está vacío"))
            return

        total = 0
        for item in self.carrito:
            subtotal = item["precio"] * item["cantidad"]
            total += subtotal
            self.content.add_widget(Label(text=f"{item['nombre']} x {item['cantidad']} = {subtotal}"))

        self.content.add_widget(Label(text=f"Total: {total}", size_hint=(1, 0.1)))
        btn_comprar = Button(text="Finalizar Compra", size_hint=(1, 0.1))
        btn_comprar.bind(on_press=self.finalizar_compra_ui)
        self.content.add_widget(btn_comprar)

    def finalizar_compra_ui(self, instance):
        if not self.usuario:
            self.label.text = "Debes iniciar sesión"
            return
        registrar_venta(self.usuario[0], self.carrito)
        self.carrito.clear()
        self.label.text = "Compra realizada con éxito"
        self.content.clear_widgets()

if __name__ == "__main__":
    TiendaApp().run()
